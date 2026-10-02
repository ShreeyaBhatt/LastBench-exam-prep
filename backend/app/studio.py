"""Notes Studio: turn uploaded notes into detailed notes, flashcards and exam questions.

Claude does the generation when credentials are configured. Without them an
offline extractor builds a rougher pack from the text so the feature still works.
"""

import re
from collections import Counter

import pymupdf

from app import ai, db

ALLOWED = {".pdf": "pdf", ".txt": "text", ".md": "text", ".markdown": "text"}
MAX_BYTES = 30 * 1024 * 1024


def extract_text(source_type, raw):
    if source_type == "pdf":
        with pymupdf.open(stream=raw, filetype="pdf") as doc:
            return "\n\n".join(page.get_text() for page in doc)
    for enc in ("utf-8", "utf-16", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return ""


def run_generation(deck_id, subject_name, raw, source_type):
    deck = db.get_deck(deck_id)
    text = deck["source_text"]
    notice = None
    if ai.ai_configured():
        try:
            db.finish_deck(deck_id, "claude", ai.generate_pack(subject_name, deck["title"], source_type, raw, text))
            return
        except Exception as e:  # noqa: BLE001 - fall back to the offline draft below
            notice = ai.friendly_error(e)
    # No AI, or the AI call failed: an offline draft is better than nothing if the file has text.
    if len(text.strip()) < 50:
        db.fail_deck(deck_id, notice or "This file has no selectable text. Scanned notes need Claude.")
        return
    try:
        data = offline_pack(deck["title"], text)
        if notice:
            data["notice"] = notice
        db.finish_deck(deck_id, "offline", data)
    except Exception as e:  # noqa: BLE001 - surface any failure on the deck
        db.fail_deck(deck_id, notice or ai.friendly_error(e))


# ---- offline generator ----------------------------------------------------

def _is_heading(line):
    s = line.strip()
    if not 3 <= len(s) <= 70 or s.endswith((".", ",", ";")):
        return False
    if re.match(r"^(\d+(\.\d+)*[.)]?|[IVX]+\.|unit\s+\d+|chapter\s+\d+)\s+\S", s, re.I):
        return True
    words = s.split()
    return len(words) <= 8 and (s.isupper() or sum(w[0].isupper() for w in words if w[0].isalpha()) >= max(1, len(words) - 1))


def _sentences(text):
    text = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text) if 25 <= len(s.strip()) <= 320]


DEF_PATTERNS = [
    re.compile(r"^(?P<term>[A-Z][\w\s/()-]{1,40}?)\s+(?:is|are|refers to|means|is called|is defined as)\s+(?P<def>.+)$"),
    re.compile(r"^(?P<term>[A-Z][\w\s/()-]{1,40}?)\s*[:–—-]\s+(?P<def>.{12,})$"),
]


BULLET_GLYPHS = "●○▪■•➢⮚❖✔✓►▶→"
NOT_TERMS = {"there", "this", "that", "these", "those", "it", "they", "he", "she", "we", "you", "here", "which", "what", "example", "note", "e.g", "i.e"}


def normalize(text):
    text = re.sub(r"[​‌‍﻿]", "", text)
    text = re.sub(rf"\s*[{BULLET_GLYPHS}]\s*", "\n- ", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text


def _clean_heading(h):
    h = re.sub(r"^[-\s]+", "", h)
    return re.sub(r"\s*[:\-–]+\s*$", "", h).strip()


def offline_pack(title, text):
    text = normalize(text)
    lines = [l.rstrip() for l in text.splitlines()]
    sections, current = [], {"heading": "Overview", "lines": []}
    for line in lines:
        if not line.strip():
            current["lines"].append("")
            continue
        if _is_heading(line) and current["lines"] and any(x.strip() for x in current["lines"]):
            sections.append(current)
            current = {"heading": _clean_heading(line), "lines": []}
        elif _is_heading(line) and not any(x.strip() for x in current["lines"]):
            current["heading"] = _clean_heading(line)
        else:
            current["lines"].append(line.strip())
    sections.append(current)
    # "Advantages" or "Example" alone means nothing on a flashcard; attach the parent topic.
    parent = None
    for s in sections:
        if re.fullmatch(r"(dis)?advantages?|merits?|demerits?|examples?|notes?|applications?|uses|features?|types?", s["heading"], re.I):
            if parent:
                s["heading"] = f"{parent}: {s['heading']}"
        else:
            parent = s["heading"]
    sections = [s for s in sections if sum(len(x) for x in s["lines"]) > 40][:40]

    out_sections, terms, formulas, cards = [], {}, [], []
    for s in sections:
        body = "\n".join(s["lines"]).strip()
        paras = [re.sub(r"\s+", " ", p) for p in re.split(r"\n\s*\n", body) if p.strip()]
        sents = _sentences(body)
        bullets = [l.lstrip("-*•●○ ").strip() for l in s["lines"] if re.match(r"^\s*([-*•●○]|\d+[.)])\s+", l)]
        content = "\n\n".join(paras[:12])
        if bullets:
            content += "\n\n" + "\n".join(f"- {b}" for b in bullets[:15])
        key_points = (bullets or sents)[:5]
        out_sections.append({"heading": s["heading"], "content_md": content, "key_points": key_points})

        for sent in sents + bullets:
            for pat in DEF_PATTERNS:
                m = pat.match(sent)
                if m:
                    term = m.group("term").strip()
                    if len(term.split()) <= 5 and term.lower() not in terms and term.lower() not in NOT_TERMS and len(m.group("def").split()) >= 4:
                        definition = m.group("def").strip().rstrip(".") + "."
                        terms[term.lower()] = {"term": term, "definition": definition}
                        cards.append({"front": f"What is {term}?", "back": definition, "topic": s["heading"]})
                    break
        for l in s["lines"]:
            if "=" in l and 5 <= len(l) <= 90 and re.search(r"[A-Za-z]", l):
                name, _, expr = l.partition("=")
                formulas.append({"name": name.strip()[:60] or "Formula", "expression": l.strip(), "note": f"From: {s['heading']}"})
        for pt in [p for p in key_points if len(p.split()) >= 6][:2]:
            words = [w for w in re.findall(r"[A-Za-z][A-Za-z-]{4,}", pt)]
            common = Counter(w.lower() for w in words)
            if not common:
                continue
            blank = max(words, key=lambda w: (len(w), -common[w.lower()]))
            cards.append({
                "front": "Fill in the blank: " + re.sub(rf"\b{re.escape(blank)}\b", "_____", pt, count=1),
                "back": blank,
                "topic": s["heading"],
            })

    summary_src = _sentences(text)[:2]
    return {
        "title": title,
        "summary": " ".join(summary_src) or f"Notes extracted from {title}.",
        "sections": out_sections,
        "key_terms": list(terms.values())[:60],
        "formulas": formulas[:30],
        "flashcards": cards[:60],
        "exam_questions": [
            {"question": f"Explain {s['heading']}.", "marks": 3, "answer_md": "\n".join(f"- {p}" for p in s["key_points"])}
            for s in out_sections[:8]
        ],
        "offline": True,
    }
