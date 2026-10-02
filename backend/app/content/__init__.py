"""Builds the Computer Networks course from the practice book + unit modules."""

import json
import re
from functools import lru_cache
from pathlib import Path

from app.solver import expand

from . import extras, syllabus, u01, u02, u03, u04, u05, u06, u07, u08, u09, u10

DATA = Path(__file__).resolve().parent.parent / "data"
UNIT_MODULES = [u01, u02, u03, u04, u05, u06, u07, u08, u09, u10]

# TIA-598 fibre colour code: strand 1 = blue, 2 = orange, ...
FIBRE = [
    ("Blue", "#1f63c6"), ("Orange", "#e8761b"), ("Green", "#2f9a52"), ("Brown", "#8a5a34"),
    ("Slate", "#6b7b86"), ("White", "#d9dedb"), ("Red", "#d23a3a"), ("Black", "#22262a"),
    ("Yellow", "#e6b800"), ("Violet", "#7d4cc2"),
]


def _clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^(_+\s*)+", "", text)
    text = re.sub(r"_{3,}(\s*_{3,})*", "_____", text)
    text = re.sub(r"\s+\.\s*_____$", " _____.", text)
    return text


@lru_cache
def load_course() -> dict:
    raw = json.loads((DATA / "practice_book.json").read_text(encoding="utf-8"))
    units = []
    questions = []
    for idx, mod in enumerate(UNIT_MODULES, start=1):
        fixes = getattr(mod, "TEXT_FIX", {})
        nums = sorted(int(k) for k, q in raw.items() if int(q["u"]) == idx)
        unit_qs = []
        for n in nums:
            q = raw[str(n)]
            sol = mod.SOL.get(n)
            if sol is None:
                raise ValueError(f"Q{n} has no solution in {mod.__name__}")
            options = [_clean(o) for o in q["o"]]
            is_mcq = any(options) and q["a"] in "ABCD" and len(q["a"]) == 1
            if is_mcq:
                answer, explanation = q["a"], sol[1] if isinstance(sol, tuple) else sol
                answer_text = options["ABCD".index(answer)]
                kind = "mcq"
            else:
                answer_text, explanation = sol if isinstance(sol, tuple) else (q["a"], sol)
                answer = None
                options = []
                kind = "numerical" if n in mod.NUMERICAL else "theory"
            diagram = DATA / "diagrams" / f"q{n}.png"
            item = {
                "id": n,
                "unit": idx,
                "text": fixes.get(n, _clean(q["q"])),
                "kind": kind,
                "marks": int(q["m"] or 1),
                "options": options,
                "answer": answer,
                "answer_text": answer_text,
                "explanation": expand(explanation),
                "diagram": f"/api/diagrams/q{n}.png" if diagram.exists() else None,
                "source": "practice_book",
            }
            unit_qs.append(item)
        # Syllabus topics the practice book skips: extra questions (ids 1000+).
        for qid, kind, marks, text, options, answer, answer_text, explanation in extras.QUESTIONS.get(idx, []):
            unit_qs.append({
                "id": qid, "unit": idx, "text": text, "kind": kind, "marks": marks,
                "options": options, "answer": answer, "answer_text": answer_text,
                "explanation": expand(explanation), "diagram": None, "source": "syllabus",
            })
        questions.extend(unit_qs)
        notes = dict(mod.NOTES)
        notes["sections"] = mod.NOTES["sections"] + extras.NOTES.get(idx, [])
        notes["formulas"] = mod.NOTES["formulas"] + extras.FORMULAS.get(idx, [])
        syl = syllabus.UNITS[idx]
        colour_name, colour = FIBRE[idx - 1]
        counts = {k: sum(q["kind"] == k for q in unit_qs) for k in ("mcq", "numerical", "theory")}
        units.append({
            "id": idx,
            "title": mod.TITLE,
            "source": mod.SOURCE,
            "fibre": colour_name,
            "colour": colour,
            # White and black strands disappear on one of the two themes; use theme ink for text/bars.
            "accent": {"White": "var(--faint)", "Black": "var(--ink)"}.get(colour_name, colour),
            "range": [nums[0], nums[-1]],
            "counts": counts,
            "total": len(unit_qs),
            "notes": notes,
            "qids": [q["id"] for q in unit_qs],
            "weight": syl["weight"],
            "hours": syl["hours"],
            "test": syl["test"],
            "topics": [{"code": c, "title": t, "questions": [q for q in refs if q in {x["id"] for x in unit_qs}]}
                       for c, t, refs in syl["topics"]],
        })
    return {
        "id": "cn",
        "code": "CN",
        "name": "Computer Networks",
        "term": "Sem V, ODD 2025",
        "builtin": True,
        "units": units,
        "questions": questions,
        "tests": syllabus.TESTS,
        "evaluation": syllabus.EVALUATION,
        "outcomes": syllabus.COURSE_OUTCOMES,
        "books": syllabus.BOOKS,
    }
