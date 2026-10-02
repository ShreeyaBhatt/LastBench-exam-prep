"""Small TF-IDF retriever over course notes, solved questions and studio decks.

Ask AI uses it to ground answers in the student's own material; it is also the
offline answer when no Claude credentials are configured.
"""

import math
import re
from collections import Counter

from app import db
from app.content import load_course

STOP = set("""a an the of to in on for and or is are was were be been by with as at from that this these those it its
which what when where who whom why how do does did can could will would should may might must not no yes if then than
so such into about over under between there their them they we you your our i me my he she his her also any all each
more most other some only own same too very just using use used per vs via""".split())


def tokens(text):
    return [t for t in re.findall(r"[a-z0-9]+(?:/[a-z0-9]+)?", text.lower()) if t not in STOP and len(t) > 1]


def _docs_for(subject_id):
    docs = []
    if subject_id == "cn":
        course = load_course()
        for u in course["units"]:
            n = u["notes"]
            for s in n["sections"]:
                docs.append({
                    "kind": "notes", "ref": f"Unit {u['id']} notes: {s['h']}", "unit": u["id"],
                    "text": f"{s['h']}\n" + "\n".join(f"- {p}" for p in s["points"]),
                })
            docs.append({
                "kind": "notes", "ref": f"Unit {u['id']} formulas", "unit": u["id"],
                "text": "\n".join(f"- {a}: {b}" for a, b in n["formulas"]) + "\n" + "\n".join(f"- Trap: {t}" for t in n["traps"]),
            })
        for q in course["questions"]:
            opts = "\n".join(f"{'ABCD'[i]}. {o}" for i, o in enumerate(q["options"]))
            ans = f"Answer: {q['answer']}. {q['answer_text']}" if q["answer"] else f"Answer: {q['answer_text']}"
            docs.append({
                "kind": "question", "ref": f"Q{q['id']} (Unit {q['unit']})", "unit": q["unit"], "qid": q["id"],
                "text": f"Q{q['id']}. {q['text']}\n{opts}\n{ans}\n{q['explanation']}",
            })
    for deck in db.list_decks(subject_id):
        full = db.get_deck(deck["id"])
        data = full.get("data") or {}
        for s in data.get("sections", []):
            docs.append({
                "kind": "deck", "ref": f"{full['title']}: {s['heading']}", "deck": full["id"],
                "text": f"{s['heading']}\n{s['content_md']}\n" + "\n".join(f"- {p}" for p in s.get("key_points", [])),
            })
        terms = data.get("key_terms", [])
        if terms:
            docs.append({
                "kind": "deck", "ref": f"{full['title']}: key terms", "deck": full["id"],
                "text": "\n".join(f"- {t['term']}: {t['definition']}" for t in terms),
            })
        if not data and full.get("source_text"):
            for i, chunk in enumerate(_chunks(full["source_text"])):
                docs.append({"kind": "deck", "ref": f"{full['title']} (part {i + 1})", "deck": full["id"], "text": chunk})
    return docs


def _chunks(text, size=1200):
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    buf, out = "", []
    for p in paras:
        if len(buf) + len(p) > size and buf:
            out.append(buf)
            buf = ""
        buf += p + "\n\n"
    if buf:
        out.append(buf)
    return out


def search(subject_id, query, k=6, unit=None, qid=None):
    docs = _docs_for(subject_id)
    if not docs:
        return []
    tok_docs = [Counter(tokens(d["text"])) for d in docs]
    df = Counter()
    for td in tok_docs:
        df.update(td.keys())
    n = len(docs)
    q = tokens(query)
    # Exact question references ("Q146") pull that question in directly.
    refs = {int(x) for x in re.findall(r"\bq\s*(\d{1,3})\b", query.lower())}
    if qid:
        refs.add(qid)
    scored = []
    for d, td in zip(docs, tok_docs):
        length = sum(td.values()) or 1
        s = sum((td[t] / length) ** 0.5 * math.log(1 + n / (1 + df[t])) for t in q if t in td)
        if d.get("qid") in refs:
            s += 100
        if unit and d.get("unit") == unit:
            s *= 1.3
        if s > 0:
            scored.append((s, d))
    scored.sort(key=lambda x: -x[0])
    return [d for _, d in scored[:k]]
