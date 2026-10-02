"""Claude integration: grounded Ask AI answers and Notes Studio study packs."""

import base64
import json
import os
from pathlib import Path

import anthropic

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


def _load_env_file():
    """Read KEY=value lines from backend/.env without overriding real env vars."""
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip().strip('"').strip("'")
        if value:
            os.environ.setdefault(key.strip(), value)


_load_env_file()

MODEL = os.environ.get("STUDYHUB_MODEL", "claude-opus-5")
FALLBACK_BETA = "server-side-fallback-2026-07-01"


class AIUnavailable(Exception):
    pass


def ai_configured():
    """True when the SDK can find credentials (env key/token or an `ant auth login` profile)."""
    if os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"):
        return True
    return (Path.home() / ".config" / "anthropic").exists()


_client = None


def client():
    global _client
    if not ai_configured():
        raise AIUnavailable("No Claude credentials found. Set ANTHROPIC_API_KEY and restart the server.")
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def friendly_error(e):
    if isinstance(e, AIUnavailable):
        return str(e)
    if isinstance(e, anthropic.AuthenticationError):
        return "Claude rejected the API key. Check ANTHROPIC_API_KEY and restart the server."
    if isinstance(e, anthropic.RateLimitError):
        return "Claude is rate-limiting requests right now. Wait a minute and try again."
    if isinstance(e, anthropic.APIConnectionError):
        return "Could not reach the Claude API. Check your internet connection."
    if isinstance(e, anthropic.APIStatusError):
        if "credit balance" in str(e.message).lower():
            return ("Your Anthropic account has no credits left, so Claude cannot answer. "
                    "Add credits at console.anthropic.com → Plans & Billing, then try again.")
        return f"Claude API error ({e.status_code}): {e.message}"
    return f"Unexpected error: {e}"


# ---- Ask AI ---------------------------------------------------------------

ASK_SYSTEM = """You are an exam tutor inside a student's study app for {subject}.

You receive excerpts from the student's own course material (notes, solved practice-book questions, and notes the student uploaded). Answer the student's question so they can write it in an exam:
- Base the answer on the provided material first. When the material shows a convention (for example how Hamming code bits are numbered, or how the practice book counts Go-Back-N transmissions), follow that convention and say so.
- For numericals: list the given values, write the formula, substitute with units, and box the final answer in bold. Convert units explicitly.
- For theory: lead with a one-line definition, then points or a comparison table, sized to the marks if the student mentions them.
- If the material does not cover the question, answer from general knowledge and add one line saying it is not in their notes.
- Mention the source question numbers (e.g. "see Q146") when an excerpt is directly relevant.
- Use Markdown: short headings, bullet lists, tables. Keep it compact; no filler."""


def build_context(sources):
    parts = []
    for i, s in enumerate(sources, 1):
        parts.append(f"<excerpt id=\"{i}\" source=\"{s['ref']}\">\n{s['text'][:3500]}\n</excerpt>")
    return "\n\n".join(parts) if parts else "(no matching excerpts)"


def ask_stream(subject_name, question, history, sources):
    """Yield text deltas of a grounded answer."""
    c = client()
    messages = []
    for turn in history[-8:]:
        if turn.get("role") in ("user", "assistant") and turn.get("content"):
            messages.append({"role": turn["role"], "content": turn["content"]})
    while messages and messages[0]["role"] != "user":
        messages.pop(0)
    messages.append({
        "role": "user",
        "content": f"Course material excerpts:\n\n{build_context(sources)}\n\nStudent's question:\n{question}",
    })
    with c.beta.messages.stream(
        model=MODEL,
        max_tokens=16000,
        system=ASK_SYSTEM.format(subject=subject_name),
        thinking={"type": "adaptive"},
        output_config={"effort": "medium"},
        betas=[FALLBACK_BETA],
        fallbacks="default",
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text
        final = stream.get_final_message()
    if final.stop_reason == "refusal":
        yield "\n\n_Claude declined to answer this request._"
    elif final.stop_reason == "max_tokens":
        yield "\n\n_The answer was cut off because it hit the length limit._"


# ---- Notes Studio ---------------------------------------------------------

PACK_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["title", "summary", "sections", "key_terms", "formulas", "flashcards", "exam_questions"],
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "sections": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["heading", "content_md", "key_points"],
                "properties": {
                    "heading": {"type": "string"},
                    "content_md": {"type": "string"},
                    "key_points": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        "key_terms": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["term", "definition"],
                "properties": {"term": {"type": "string"}, "definition": {"type": "string"}},
            },
        },
        "formulas": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["name", "expression", "note"],
                "properties": {"name": {"type": "string"}, "expression": {"type": "string"}, "note": {"type": "string"}},
            },
        },
        "flashcards": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["front", "back", "topic"],
                "properties": {"front": {"type": "string"}, "back": {"type": "string"}, "topic": {"type": "string"}},
            },
        },
        "exam_questions": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["question", "marks", "answer_md"],
                "properties": {
                    "question": {"type": "string"},
                    "marks": {"type": "integer"},
                    "answer_md": {"type": "string"},
                },
            },
        },
    },
}

PACK_PROMPT = """These are a student's class notes for {subject}{title_hint}. Turn them into a study pack for exam revision.

- sections: follow the order of the notes. For each topic write detailed, self-contained notes in Markdown (content_md): definitions, how things work, worked examples copied or derived from the notes, comparison tables where the notes compare things. Expand terse bullet points into full explanations, but do not invent facts that contradict the notes. key_points = 3-6 one-line takeaways for last-minute revision.
- summary: 2-3 sentences on what the material covers.
- key_terms: every important term with a one-sentence definition.
- formulas: every formula, rule or numeric relationship, with a short note on when to use it (empty list if none).
- flashcards: 15-40 cards covering definitions, differences, steps of procedures, formulas and common traps. Front = a specific question, back = a short exact answer. topic = the section heading it belongs to.
- exam_questions: 5-10 likely exam questions (mix of 2, 3, 4 and 7 marks) with model answers sized to the marks.
- title: a short title for the material."""


def generate_pack(subject_name, title, source_type, raw_bytes, text):
    c = client()
    hint = f' (file: "{title}")' if title else ""
    prompt = PACK_PROMPT.format(subject=subject_name, title_hint=hint)
    if source_type == "pdf":
        content = [
            {"type": "document", "source": {"type": "base64", "media_type": "application/pdf",
                                             "data": base64.standard_b64encode(raw_bytes).decode()}},
            {"type": "text", "text": prompt},
        ]
    else:
        content = f"<notes>\n{text}\n</notes>\n\n{prompt}"
    with c.beta.messages.stream(
        model=MODEL,
        max_tokens=64000,
        thinking={"type": "adaptive"},
        output_config={"effort": "high", "format": {"type": "json_schema", "schema": PACK_SCHEMA}},
        betas=[FALLBACK_BETA],
        fallbacks="default",
        messages=[{"role": "user", "content": content}],
    ) as stream:
        final = stream.get_final_message()
    if final.stop_reason == "refusal":
        raise RuntimeError("Claude declined to process this document.")
    if final.stop_reason == "max_tokens":
        raise RuntimeError("The notes were too long to finish in one pass. Split the file into smaller chapters and upload them separately.")
    body = next(b.text for b in final.content if b.type == "text")
    return json.loads(body)
