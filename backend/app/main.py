"""LastBench API: CN exam prep, Notes Studio and Ask AI."""

import json
import random
import re
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response, StreamingResponse
from pydantic import BaseModel, Field

from app import ai, db, pdf_export, search, studio
from app.content import load_course

APP_DIR = Path(__file__).resolve().parent
DIAGRAMS = APP_DIR / "data" / "diagrams"
FRONTEND_DIST = APP_DIR.parent.parent / "frontend" / "dist"

app = FastAPI(title="LastBench", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
db.init()


def course():
    return load_course()


# Questions that can't stand alone (Q236's forwarding table is missing from the practice book).
NOT_FOR_PRACTICE = {236}


def practice_pool():
    return [q for q in course()["questions"] if q["id"] not in NOT_FOR_PRACTICE]


def _unit_summary(u):
    return {k: u[k] for k in ("id", "title", "fibre", "colour", "accent", "range", "counts", "total", "source",
                              "qids", "weight", "hours", "test", "topics")} | {
        "summary": u["notes"]["summary"]
    }


# ---- health / subjects -------------------------------------------------------

@app.get("/api/health")
def health():
    return {"ok": True, "ai": {"available": ai.ai_configured(), "model": ai.MODEL}}


@app.get("/api/subjects")
def subjects():
    c = course()
    builtin = {
        "id": "cn", "code": c["code"], "name": c["name"], "term": c["term"], "builtin": True,
        "description": "Practice book solutions, one-minute notes and quizzes for all 10 units.",
        "question_count": len(c["questions"]), "unit_count": len(c["units"]),
        "deck_count": len(db.list_decks("cn")),
    }
    others = [s | {"builtin": False} for s in db.list_subjects()]
    return [builtin] + others


class SubjectIn(BaseModel):
    code: str = Field(min_length=1, max_length=12)
    name: str = Field(min_length=1, max_length=80)
    description: str = Field(default="", max_length=300)


@app.post("/api/subjects")
def create_subject(body: SubjectIn):
    sid = re.sub(r"[^a-z0-9]+", "-", body.code.lower()).strip("-") or "subject"
    if sid == "cn" or db.get_subject(sid):
        raise HTTPException(409, f"A subject with code {body.code} already exists.")
    return db.create_subject(sid, body.code.strip(), body.name.strip(), body.description.strip())


@app.put("/api/subjects/{sid}")
def update_subject(sid: str, body: SubjectIn):
    if not db.get_subject(sid):
        raise HTTPException(404, "Subject not found.")
    return db.update_subject(sid, body.code.strip(), body.name.strip(), body.description.strip())


@app.get("/api/subjects/{sid}")
def subject_detail(sid: str):
    if sid == "cn":
        c = course()
        return {"id": "cn", "code": c["code"], "name": c["name"], "term": c["term"], "builtin": True,
                "units": [_unit_summary(u) for u in c["units"]], "decks": db.list_decks("cn")}
    s = db.get_subject(sid)
    if not s:
        raise HTTPException(404, "Subject not found.")
    return s | {"builtin": False, "units": [], "decks": db.list_decks(sid)}


# ---- CN course -----------------------------------------------------------------

@app.get("/api/cn/units/{uid}")
def unit(uid: int):
    c = course()
    u = next((x for x in c["units"] if x["id"] == uid), None)
    if not u:
        raise HTTPException(404, "Unit not found.")
    return u | {"questions": [q for q in c["questions"] if q["unit"] == uid]}


@app.get("/api/cn/units/{uid}/pdf")
def unit_pdf(uid: int):
    c = course()
    u = next((x for x in c["units"] if x["id"] == uid), None)
    if not u:
        raise HTTPException(404, "Unit not found.")
    pdf = pdf_export.unit_pdf(c, u, [q for q in c["questions"] if q["unit"] == uid], DIAGRAMS)
    name = f"CN-Unit-{uid}-{re.sub(r'[^A-Za-z0-9]+', '-', u['title']).strip('-')}.pdf"
    return Response(pdf, media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="{name}"'})


@app.get("/api/cn/questions")
def questions(q: str = "", unit: int | None = None, kind: str | None = None):
    items = course()["questions"]
    if unit:
        items = [x for x in items if x["unit"] == unit]
    if kind:
        items = [x for x in items if x["kind"] == kind]
    if q.strip():
        m = re.fullmatch(r"\s*q?\s*(\d{1,3})\s*", q, re.I)
        if m:
            items = [x for x in items if x["id"] == int(m.group(1))]
        else:
            terms = [t for t in q.lower().split() if t]
            items = [x for x in items if all(t in (x["text"] + " " + " ".join(x["options"]) + " " + x["answer_text"]).lower() for t in terms)]
    return items


@app.get("/api/cn/formulas")
def formulas():
    return [{"unit": u["id"], "title": u["title"], "colour": u["colour"], "accent": u["accent"], "formulas": u["notes"]["formulas"],
             "traps": u["notes"]["traps"]} for u in course()["units"]]


@app.get("/api/cn/formulas/pdf")
def formulas_pdf():
    c = course()
    return Response(pdf_export.formulas_pdf(c), media_type="application/pdf",
                    headers={"Content-Disposition": f'attachment; filename="{c["code"]}-Formula-Sheet.pdf"'})


@app.get("/api/cn/quiz")
def quiz(units: str = "", n: int = 10):
    wanted = {int(x) for x in units.split(",") if x.strip().isdigit()}
    pool = [q for q in practice_pool() if q["kind"] == "mcq" and (not wanted or q["unit"] in wanted)]
    random.shuffle(pool)
    return pool[: max(1, min(n, 50))]


@app.get("/api/cn/daily")
def daily(day: str):
    """Question of the day: the same MCQ for everyone on a given date (YYYY-MM-DD)."""
    pool = [q for q in practice_pool() if q["kind"] == "mcq"]
    return random.Random(day).choice(pool)


@app.get("/api/diagrams/{name}")
def diagram(name: str):
    path = (DIAGRAMS / name).resolve()
    if path.parent != DIAGRAMS.resolve() or not path.exists():
        raise HTTPException(404, "Diagram not found.")
    return FileResponse(path, media_type="image/png")


# ---- progress ------------------------------------------------------------------

class ProgressIn(BaseModel):
    status: str | None = None
    bookmarked: bool | None = None


@app.get("/api/progress")
def get_progress():
    return db.all_progress()


@app.put("/api/progress/{key}")
def put_progress(key: str, body: ProgressIn):
    if not re.fullmatch(r"(cn:\d{1,4}|deck:\d+:card:\d+|syl:\d{1,2}\.\d|lab:[pj]\d{1,2})", key):
        raise HTTPException(400, "Unknown progress key.")
    if key.startswith("cn:") and body.status in ("correct", "wrong"):
        qid = int(key[3:])
        q = next((x for x in course()["questions"] if x["id"] == qid), None)
        db.log_activity("question", key, body.status, q["unit"] if q else None)
        # Missed questions join the revision queue; getting one right later pushes it back.
        if body.status == "wrong":
            db.srs_review(key, "again")
        elif key in db.srs_states(key):
            db.srs_review(key, "good")
    # An explicit {"status": null} clears it; leaving status out keeps it.
    clear = "status" in body.model_fields_set and body.status is None
    return db.set_progress(key, body.status, body.bookmarked, clear_status=clear)


@app.delete("/api/progress")
def clear_progress(prefix: str):
    db.reset_progress(prefix)
    db.srs_reset(prefix)
    return {"ok": True}


# ---- spaced repetition, focus sessions, stats, planner, settings ------------------

class ReviewIn(BaseModel):
    key: str
    grade: str


@app.post("/api/review")
def review(body: ReviewIn):
    if body.grade not in db.GRADES or not re.fullmatch(r"deck:\d+:card:\d+", body.key):
        raise HTTPException(400, "Unknown card or grade.")
    state = db.srs_review(body.key, body.grade)
    db.log_activity("card", body.key, body.grade)
    db.set_progress(body.key, "known" if body.grade in ("good", "easy") else "learning")
    return state


@app.get("/api/review/states")
def review_states(prefix: str):
    return db.srs_states(prefix)


@app.get("/api/review/due")
def review_due():
    """Everything due today: flashcards from every deck, plus missed CN questions."""
    cards = []
    titles = {}
    for key in db.srs_due("deck:"):
        _, deck_id, _, idx = key.split(":")
        deck_id, idx = int(deck_id), int(idx)
        if deck_id not in titles:
            d = db.get_deck(deck_id, full=True)
            titles[deck_id] = d
        d = titles[deck_id]
        if not d or not d.get("data"):
            continue
        fc = d["data"].get("flashcards", [])
        if idx < len(fc):
            cards.append({"key": key, "deck_id": deck_id, "deck_title": d["title"], "subject_id": d["subject_id"], **fc[idx]})
    # Unseen cards from each ready deck count as new; offer a few per deck each day.
    new_cards = []
    for meta in db.list_decks():
        if meta["status"] != "ready":
            continue
        d = titles.get(meta["id"]) or db.get_deck(meta["id"], full=True)
        seen = db.srs_states(f"deck:{meta['id']}:card:")
        fresh = [i for i in range(len(d["data"].get("flashcards", []))) if f"deck:{meta['id']}:card:{i}" not in seen]
        for i in fresh[:10]:
            new_cards.append({"key": f"deck:{meta['id']}:card:{i}", "deck_id": meta["id"], "deck_title": d["title"],
                              "subject_id": d["subject_id"], "new": True, **d["data"]["flashcards"][i]})
    questions = [int(k[3:]) for k in db.srs_due("cn:")]
    return {"cards": cards, "new_cards": new_cards, "questions": questions}


class FocusIn(BaseModel):
    minutes: float = Field(gt=0, le=180)


@app.post("/api/focus")
def focus(body: FocusIn):
    db.log_activity("focus", result="done", minutes=body.minutes)
    return {"ok": True}


def _streaks(days):
    if not days:
        return 0, 0
    from datetime import date as _d, timedelta as _t
    ds = sorted({_d.fromisoformat(d) for d in days})
    best = run = 1
    for a, b in zip(ds, ds[1:]):
        run = run + 1 if (b - a).days == 1 else 1
        best = max(best, run)
    today = _d.today()
    current = 0
    cursor = today if ds[-1] == today else today - _t(days=1)
    s = set(ds)
    while cursor in s:
        current += 1
        cursor -= _t(days=1)
    return current, best


@app.get("/api/stats")
def stats():
    from datetime import date as _d, timedelta as _t
    today = _d.today()
    since = (today - _t(days=83)).isoformat()
    rows = db.activity_by_day(since)
    by_day = {}
    for r in rows:
        d = by_day.setdefault(r["day"], {"day": r["day"], "items": 0, "correct": 0, "questions": 0, "focus_minutes": 0})
        if r["kind"] == "focus":
            d["focus_minutes"] += r["minutes"] or 0
        else:
            d["items"] += r["n"] or 0
            d["questions"] += r["questions"] or 0
            if r["kind"] == "question":
                d["correct"] += r["ok"] or 0
    heatmap = []
    for i in range(84):
        day = (today - _t(days=83 - i)).isoformat()
        heatmap.append(by_day.get(day, {"day": day, "items": 0, "correct": 0, "questions": 0, "focus_minutes": 0}))
    current, best = _streaks(db.active_days())
    progress = db.all_progress()
    units = []
    for u in course()["units"]:
        st = [progress.get(f"cn:{i}", {}).get("status") for i in u["qids"]]
        tried = sum(s in ("correct", "wrong") for s in st)
        right = sum(s == "correct" for s in st)
        units.append({"id": u["id"], "title": u["title"], "colour": u["colour"], "accent": u["accent"],
                      "total": u["total"], "attempted": tried, "correct": right, "test": u["test"], "weight": u["weight"],
                      "accuracy": round(right / tried, 3) if tried else None})
    week = heatmap[-7:]
    return {
        "streak": current, "best_streak": best,
        "today": heatmap[-1],
        "week": {"items": sum(d["items"] for d in week), "focus_minutes": round(sum(d["focus_minutes"] for d in week))},
        "heatmap": heatmap,
        "units": units,
        "due": {"questions": len(db.srs_due("cn:")), "cards": len(db.srs_due("deck:"))},
    }


@app.get("/api/settings")
def get_settings():
    return db.get_settings()


class SettingIn(BaseModel):
    value: object | None = None


@app.put("/api/settings/{key}")
def put_setting(key: str, body: SettingIn):
    if not re.fullmatch(r"(exam:[a-z0-9-]+|daily_goal|reading_font|text_size|plan_mode)", key):
        raise HTTPException(400, "Unknown setting.")
    db.set_setting(key, body.value)
    return db.get_settings()


@app.get("/api/plan")
def plan(subject_id: str = "cn", test: str | None = None, mode: str = "questions"):
    """A day-by-day roadmap from today to the exam date, sized to the questions still left.

    For CN, each test (T1 = units 1-4, T2 = units 5-10) has its own date. Numericals come
    first inside each unit because they carry 25 of the 50 marks. mode="syllabus" walks the
    official syllabus topic by topic instead (see _syllabus_plan).
    """
    from datetime import date as _d, timedelta as _t
    settings = db.get_settings()
    today = _d.today()
    if subject_id == "cn":
        dates = {t: settings.get(f"exam:cn-{t.lower()}") for t in ("T1", "T2")}
        if not test:
            upcoming = sorted((d, t) for t, d in dates.items() if d and _d.fromisoformat(d) > today)
            test = upcoming[0][1] if upcoming else None
        exam = dates.get(test) if test else None
    else:
        exam = settings.get(f"exam:{subject_id}")
    if not exam:
        return {"exam": None, "test": test, "days": []}
    left = (_d.fromisoformat(exam) - today).days
    if left <= 0:
        return {"exam": exam, "test": test, "days_left": left, "days": []}
    if subject_id != "cn":
        decks = [d for d in db.list_decks(subject_id) if d["status"] == "ready"]
        days = []
        for i in range(left):
            day = today + _t(days=i)
            tasks = ([{"type": "deck", "deck": decks[i % len(decks)]["id"], "label": f"Study pack: {decks[i % len(decks)]['title']}"}]
                     if decks else [{"type": "upload", "label": "Upload this subject's notes in Notes Studio"}])
            tasks.append({"type": "review", "label": "Review today's due flashcards"})
            days.append({"date": day.isoformat(), "tasks": tasks})
        return {"exam": exam, "days_left": left, "days": days}

    progress = db.all_progress()
    if mode == "syllabus":
        return _syllabus_plan(test, exam, left, today, progress)
    by_id = {q["id"]: q for q in course()["questions"]}
    order = {"numerical": 0, "mcq": 1, "theory": 2}
    queue = []          # (unit, [question ids still to do], numericals first)
    for u in course()["units"]:
        if u["id"] not in syllabus_units(test):
            continue
        todo = [i for i in u["qids"] if progress.get(f"cn:{i}", {}).get("status") != "correct"]
        todo.sort(key=lambda i: (order[by_id[i]["kind"]], i))
        if todo:
            queue.append((u, todo))
    revision_days = 0 if left == 1 else (1 if left <= 4 else 2)
    study_days = max(1, left - revision_days)
    total = sum(len(t) for _, t in queue)
    per_day = max(1, -(-total // study_days)) if total else 0
    days, qi, offset = [], 0, 0
    for i in range(left):
        day = today + _t(days=i)
        tasks = []
        if i < study_days and qi < len(queue):
            budget = per_day
            while budget > 0 and qi < len(queue):
                u, todo = queue[qi]
                chunk = todo[offset: offset + budget]
                if offset == 0:
                    tasks.append({"type": "notes", "unit": u["id"], "label": f"Read Unit {u['id']} one-minute notes"})
                nums = sum(by_id[q]["kind"] == "numerical" for q in chunk)
                label = f"Unit {u['id']}: {len(chunk)} questions" + (f" ({nums} numerical)" if nums else "")
                tasks.append({"type": "questions", "unit": u["id"], "count": len(chunk),
                              "kind": "numerical" if nums == len(chunk) else None, "label": label})
                budget -= len(chunk)
                offset += len(chunk)
                if offset >= len(todo):
                    qi, offset = qi + 1, 0
            tasks.append({"type": "review", "label": "Clear today's revision queue"})
        elif i < study_days:
            tasks = [{"type": "quiz", "label": "Smart quiz: 20 questions"}, {"type": "review", "label": "Clear today's revision queue"}]
        else:
            tasks = [{"type": "mock", "test": test, "label": f"Timed mock {test} paper (50 marks)"},
                     {"type": "formulas", "label": "Read the formula sheet"},
                     {"type": "review", "label": "Revise every question marked 'Revise'"}]
        days.append({"date": day.isoformat(), "tasks": tasks})
    return {"exam": exam, "test": test, "days_left": left, "remaining_questions": total, "per_day": per_day, "days": days}


# Reading a topic costs about as much as a couple of questions, so a topic with every
# question already right still gets a slot to revise and tick off.
TOPIC_READ_COST = 2


def _syllabus_plan(test, exam, left, today, progress):
    """Covers every syllabus topic not yet ticked as revised, in syllabus order.

    Topics are never split across days. Each one starts on the day where its share of the
    workload begins, so heavy topics (5.2 has 17 questions) get a day nearly to themselves,
    and with more days than topics the gaps become smart-quiz days.
    """
    from datetime import timedelta as _t
    queue = []          # (unit, topic, [question ids not yet right])
    total_topics = 0
    for u in course()["units"]:
        if u["id"] not in syllabus_units(test):
            continue
        for tp in u["topics"]:
            total_topics += 1
            if progress.get(f"syl:{tp['code']}", {}).get("status") == "done":
                continue
            todo = [i for i in tp["questions"] if progress.get(f"cn:{i}", {}).get("status") != "correct"]
            queue.append((u, tp, todo))
    revision_days = 0 if left == 1 else (1 if left <= 4 else 2)
    study_days = max(1, left - revision_days)
    loads = [len(todo) + TOPIC_READ_COST for _, _, todo in queue]
    total_load = sum(loads)
    by_day = [[] for _ in range(study_days)]
    cum = 0
    for item, load in zip(queue, loads):
        by_day[min(study_days - 1, int(cum / total_load * study_days))].append(item)
        cum += load
    started = set()     # units whose notes are already scheduled
    days = []
    for i in range(left):
        day = today + _t(days=i)
        if i < study_days and by_day[i]:
            tasks = []
            for u, tp, todo in by_day[i]:
                if u["id"] not in started:
                    started.add(u["id"])
                    tasks.append({"type": "notes", "unit": u["id"], "label": f"Read Unit {u['id']} one-minute notes"})
                label = f"{tp['code']} {tp['title']}: " + (f"{len(todo)} questions" if todo else "revise, all questions done")
                tasks.append({"type": "topic", "unit": u["id"], "topic": tp["code"], "count": len(todo), "label": label})
            tasks.append({"type": "syllabus", "label": "Tick off today's topics in the syllabus tracker"})
        elif i < study_days:
            tasks = [{"type": "quiz", "label": "Smart quiz: 20 questions"}, {"type": "review", "label": "Clear today's revision queue"}]
        else:
            tasks = [{"type": "mock", "test": test, "label": f"Timed mock {test} paper (50 marks)"},
                     {"type": "formulas", "label": "Read the formula sheet"},
                     {"type": "review", "label": "Revise every question marked 'Revise'"}]
        days.append({"date": day.isoformat(), "tasks": tasks})
    return {"exam": exam, "test": test, "mode": "syllabus", "days_left": left,
            "remaining_topics": len(queue), "total_topics": total_topics,
            "remaining_questions": sum(len(t) for _, _, t in queue),
            "per_day": round(len(queue) / study_days, 1), "days": days}


def syllabus_units(test):
    return course()["tests"][test]["units"] if test in course()["tests"] else [u["id"] for u in course()["units"]]


@app.get("/api/cn/syllabus")
def syllabus_view():
    c = course()
    return {
        "units": [_unit_summary(u) for u in c["units"]],
        "tests": c["tests"], "evaluation": c["evaluation"], "outcomes": c["outcomes"], "books": c["books"],
    }


@app.get("/api/cn/labs")
def labs_view():
    from app.content import labs
    return {"practicals": labs.PRACTICALS, "projects": labs.PROJECTS}


@app.get("/api/cn/mock")
def mock(test: str = "T1", seed: int | None = None):
    """A paper in the LJU pattern: 20 MCQ marks, 5 descriptive, 25 numerical, weighted by unit."""
    tests = course()["tests"]
    if test not in tests:
        raise HTTPException(400, "Test must be T1 or T2.")
    spec = tests[test]
    rng = random.Random(seed)
    units = {u["id"]: u for u in course()["units"] if u["id"] in spec["units"]}
    pool = [q for q in practice_pool() if q["unit"] in units]

    def pick(kind, target):
        cands = [q for q in pool if q["kind"] == kind]
        # Weight each question so every unit's share of picks follows its syllabus weight.
        per_unit = {uid: sum(1 for q in cands if q["unit"] == uid) or 1 for uid in units}
        best = ([], 0)
        for _ in range(200):          # random greedy fill; retry until the marks add up exactly
            chosen, total = [], 0
            while total < target:
                fit = [q for q in cands if q not in chosen and q["marks"] <= target - total]
                if not fit:
                    break
                q = rng.choices(fit, weights=[units[x["unit"]]["weight"] / per_unit[x["unit"]] for x in fit])[0]
                chosen.append(q)
                total += q["marks"]
            if total > best[1]:
                best = (chosen, total)
            if total == target:
                break
        chosen, total = best
        return sorted(chosen, key=lambda q: (q["unit"], q["id"])), total

    sections = []
    for kind, title in (("mcq", "Section A: Multiple choice"), ("theory", "Section B: Descriptive"), ("numerical", "Section C: Numericals")):
        qs, marks = pick(kind, spec["pattern"][kind])
        sections.append({"kind": kind, "title": title, "target": spec["pattern"][kind], "marks": marks, "questions": qs})
    return {"test": test, "units": spec["units"], "duration_min": spec["duration_min"],
            "total": sum(s["marks"] for s in sections), "sections": sections}


@app.get("/api/cn/smart-quiz")
def smart_quiz(n: int = 10):
    """Adaptive MCQ set: missed questions first, then the weakest units, then fresh ones."""
    n = max(1, min(n, 50))
    qs = [q for q in practice_pool() if q["kind"] == "mcq"]
    progress = db.all_progress()
    due = set(db.srs_due("cn:"))
    acc = {}
    for u in course()["units"]:
        st = [progress.get(f"cn:{i}", {}).get("status") for i in u["qids"]]
        tried = sum(s in ("correct", "wrong") for s in st)
        right = sum(s == "correct" for s in st)
        acc[u["id"]] = (right + 1) / (tried + 2)          # smoothed accuracy; untried units sit at 0.5

    def weight(q):
        status = progress.get(f"cn:{q['id']}", {}).get("status")
        w = 1.0
        if f"cn:{q['id']}" in due or status == "wrong":
            w += 6
        elif status is None:
            w += 2
        elif status == "correct":
            w *= 0.25
        return w * (1.5 - acc[q["unit"]])                 # weaker unit, higher chance

    rng = random.Random()
    chosen = []
    pool = qs[:]
    while pool and len(chosen) < n:
        pick = rng.choices(pool, weights=[weight(q) for q in pool])[0]
        chosen.append(pick)
        pool.remove(pick)
    return chosen


# ---- Notes Studio --------------------------------------------------------------

def _subject_name(sid):
    if sid == "cn":
        return course()["name"]
    s = db.get_subject(sid)
    if not s:
        raise HTTPException(404, "Subject not found.")
    return s["name"] if s["name"] == s["code"] else f"{s['name']} ({s['code']})"


@app.post("/api/studio/upload")
async def upload(background: BackgroundTasks, file: UploadFile = File(...), subject_id: str = Form(...), title: str = Form("")):
    subject_name = _subject_name(subject_id)
    ext = Path(file.filename or "").suffix.lower()
    source_type = studio.ALLOWED.get(ext)
    if not source_type:
        raise HTTPException(400, "Upload a PDF, TXT or Markdown file.")
    raw = await file.read()
    if len(raw) > studio.MAX_BYTES:
        raise HTTPException(400, "The file is larger than 30 MB. Split it into chapters and upload them one by one.")
    if not raw:
        raise HTTPException(400, "The file is empty.")
    try:
        text = studio.extract_text(source_type, raw)
    except Exception:
        raise HTTPException(400, "Could not read this file. If it is a PDF, check that it is not password-protected.")
    if source_type == "text" and len(text.strip()) < 50:
        raise HTTPException(400, "The file has too little text to make notes from.")
    if source_type == "pdf" and len(text.strip()) < 50 and not ai.ai_configured():
        raise HTTPException(400, "This PDF looks scanned (no selectable text). Scanned notes need Claude: set ANTHROPIC_API_KEY and restart.")
    deck_title = title.strip() or Path(file.filename).stem.replace("_", " ").replace("-", " ").strip()
    deck_id = db.create_deck(subject_id, deck_title, file.filename, source_type, text)
    _save_source(deck_id, ext, raw)
    background.add_task(studio.run_generation, deck_id, subject_name, raw, source_type)
    return db.get_deck(deck_id, full=False)


SOURCES = APP_DIR.parent / "storage" / "uploads"


def _save_source(deck_id, ext, raw):
    SOURCES.mkdir(parents=True, exist_ok=True)
    (SOURCES / f"{deck_id}{ext}").write_bytes(raw)


@app.get("/api/studio/decks")
def decks(subject_id: str | None = None):
    return db.list_decks(subject_id)


@app.get("/api/studio/decks/{deck_id}")
def deck(deck_id: int):
    d = db.get_deck(deck_id)
    if not d:
        raise HTTPException(404, "Deck not found.")
    d.pop("source_text", None)
    return d


@app.post("/api/studio/decks/{deck_id}/regenerate")
def regenerate(deck_id: int, background: BackgroundTasks):
    d = db.get_deck(deck_id)
    if not d:
        raise HTTPException(404, "Deck not found.")
    src = next(iter(SOURCES.glob(f"{deck_id}.*")), None)
    if not src:
        raise HTTPException(410, "The original upload is missing. Delete this deck and upload the file again.")
    db.mark_processing(deck_id)
    background.add_task(studio.run_generation, deck_id, _subject_name(d["subject_id"]), src.read_bytes(), d["source_type"])
    return db.get_deck(deck_id, full=False)


@app.delete("/api/studio/decks/{deck_id}")
def remove_deck(deck_id: int):
    db.delete_deck(deck_id)
    for f in SOURCES.glob(f"{deck_id}.*"):
        f.unlink(missing_ok=True)
    return {"ok": True}


@app.get("/api/studio/decks/{deck_id}/pdf")
def deck_pdf(deck_id: int):
    d = db.get_deck(deck_id)
    if not d or d["status"] != "ready":
        raise HTTPException(404, "This deck is not ready yet.")
    sid = d["subject_id"]
    subj = {"code": "CN", "name": course()["name"]} if sid == "cn" else db.get_subject(sid)
    pdf = pdf_export.deck_pdf(subj, d)
    name = re.sub(r"[^A-Za-z0-9]+", "-", d["title"]).strip("-") or "notes"
    return Response(pdf, media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="{name}-study-pack.pdf"'})


# ---- Ask AI ----------------------------------------------------------------------

class AskIn(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    subject_id: str = "cn"
    unit: int | None = None
    question_id: int | None = None
    history: list[dict] = []


def _sse(obj):
    return f"data: {json.dumps(obj)}\n\n"


@app.post("/api/ask")
def ask(body: AskIn):
    subject_name = _subject_name(body.subject_id)
    query = body.question
    if body.question_id:
        q = next((x for x in course()["questions"] if x["id"] == body.question_id), None)
        if q:
            query += f"\n(About practice book Q{q['id']}: {q['text']})"
    sources = search.search(body.subject_id, query, k=6, unit=body.unit, qid=body.question_id)

    def events():
        yield _sse({"type": "sources", "items": [
            {"ref": s["ref"], "kind": s["kind"], "unit": s.get("unit"), "qid": s.get("qid"), "deck": s.get("deck")} for s in sources
        ]})
        if not ai.ai_configured():
            yield _sse({"type": "mode", "mode": "offline"})
            yield _sse({"type": "delta", "text": _offline_answer(sources)})
            yield _sse({"type": "done"})
            return
        yield _sse({"type": "mode", "mode": "claude"})
        sent = False
        try:
            for text in ai.ask_stream(subject_name, query, body.history, sources):
                sent = True
                yield _sse({"type": "delta", "text": text})
        except Exception as e:  # noqa: BLE001
            yield _sse({"type": "error", "message": ai.friendly_error(e)})
            if not sent:
                # Still give the student something useful: the closest matches from their material.
                yield _sse({"type": "mode", "mode": "offline"})
                yield _sse({"type": "delta", "text": _offline_answer(sources, reason=False)})
        yield _sse({"type": "done"})

    return StreamingResponse(events(), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})


def _offline_answer(sources, reason=True):
    if not sources:
        return "Nothing in your material matches this question. Try different keywords." + (
            " Set `ANTHROPIC_API_KEY` and restart the server for written AI answers." if reason else "")
    out = [("**Claude is not connected**, so here is the closest match from your material. "
            "Set `ANTHROPIC_API_KEY` and restart the server for written answers.\n") if reason
           else "Here is the closest match from your material:\n"]
    for s in sources[:3]:
        out.append(f"### {s['ref']}\n\n{s['text'][:1800]}\n")
    return "\n".join(out)


# ---- frontend (production build) ------------------------------------------------

if FRONTEND_DIST.exists():
    ASSETS = FRONTEND_DIST / "assets"

    @app.get("/assets/{name}")
    def asset(name: str):
        target = (ASSETS / name).resolve()
        if target.parent == ASSETS.resolve() and target.is_file():
            # Hashed file names change on every build, so these can be cached for good.
            return FileResponse(target, headers={"Cache-Control": "public, max-age=31536000, immutable"})
        # A page cached before a rebuild asks for bundles that no longer exist. Hand it the
        # current bundle of the same type instead of a 404 (which would leave a blank page).
        suffix = Path(name).suffix
        current = sorted(ASSETS.glob(f"index-*{suffix}"), key=lambda p: p.stat().st_mtime)
        if suffix in (".js", ".css") and current:
            return FileResponse(current[-1], headers={"Cache-Control": "no-cache"})
        raise HTTPException(404, "Not found.")

    @app.get("/{path:path}")
    def spa(path: str):
        target = (FRONTEND_DIST / path).resolve()
        if path and target.is_file() and FRONTEND_DIST.resolve() in target.parents:
            return FileResponse(target)
        # The page shell must never be cached: after a rebuild it points to new hashed JS files,
        # and a stale copy would request deleted ones and render a blank page.
        return FileResponse(FRONTEND_DIST / "index.html", headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
