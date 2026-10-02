"""SQLite storage for subjects, Notes Studio decks and study progress."""

import json
import sqlite3
import time
from datetime import date, timedelta
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "storage" / "studyhub.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS subjects (
    id TEXT PRIMARY KEY,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    created REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS decks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id TEXT NOT NULL,
    title TEXT NOT NULL,
    source_name TEXT NOT NULL,
    source_type TEXT NOT NULL,
    status TEXT NOT NULL,          -- processing | ready | failed
    engine TEXT,                   -- claude | offline
    error TEXT,
    data TEXT,                     -- generated study pack (JSON)
    source_text TEXT NOT NULL DEFAULT '',
    created REAL NOT NULL,
    updated REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS progress (
    key TEXT PRIMARY KEY,          -- cn:27  or  deck:3:card:5
    status TEXT,                   -- correct | wrong | seen | known | learning
    bookmarked INTEGER NOT NULL DEFAULT 0,
    updated REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL NOT NULL,
    day TEXT NOT NULL,             -- local date, YYYY-MM-DD
    kind TEXT NOT NULL,            -- question | card | focus
    key TEXT,                      -- cn:27 | deck:3:card:5
    result TEXT,                   -- correct | wrong | again | hard | good | easy | done
    unit INTEGER,
    minutes REAL NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS activity_day ON activity(day);
CREATE TABLE IF NOT EXISTS srs (
    key TEXT PRIMARY KEY,          -- spaced-repetition state for a card or question
    ease REAL NOT NULL DEFAULT 2.5,
    interval INTEGER NOT NULL DEFAULT 0,
    reps INTEGER NOT NULL DEFAULT 0,
    lapses INTEGER NOT NULL DEFAULT 0,
    due TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""

SEED_SUBJECTS = [
    ("eef", "EEF", "EEF", "Demo space. Upload your EEF notes in Notes Studio to generate detailed notes and flashcards here."),
]


@contextmanager
def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init():
    with connect() as c:
        c.executescript(SCHEMA)
        for sid, code, name, desc in SEED_SUBJECTS:
            c.execute(
                "INSERT OR IGNORE INTO subjects (id, code, name, description, created) VALUES (?, ?, ?, ?, ?)",
                (sid, code, name, desc, time.time()),
            )
        # A server restart interrupts any generation that was running.
        c.execute(
            "UPDATE decks SET status = 'failed', error = 'Generation was interrupted by a server restart. Press Regenerate.' "
            "WHERE status = 'processing'"
        )


# ---- subjects -------------------------------------------------------------

def list_subjects():
    with connect() as c:
        rows = c.execute(
            "SELECT s.*, (SELECT COUNT(*) FROM decks d WHERE d.subject_id = s.id) AS deck_count "
            "FROM subjects s ORDER BY s.created"
        ).fetchall()
    return [dict(r) for r in rows]


def get_subject(sid):
    with connect() as c:
        row = c.execute("SELECT * FROM subjects WHERE id = ?", (sid,)).fetchone()
    return dict(row) if row else None


def create_subject(sid, code, name, description):
    with connect() as c:
        c.execute(
            "INSERT INTO subjects (id, code, name, description, created) VALUES (?, ?, ?, ?, ?)",
            (sid, code, name, description, time.time()),
        )
    return get_subject(sid)


def update_subject(sid, code, name, description):
    with connect() as c:
        c.execute(
            "UPDATE subjects SET code = ?, name = ?, description = ? WHERE id = ?",
            (code, name, description, sid),
        )
    return get_subject(sid)


# ---- decks ----------------------------------------------------------------

def _deck(row, full=True):
    d = dict(row)
    d["data"] = json.loads(d["data"]) if d.get("data") else None
    if not full:
        d.pop("source_text", None)
        if d["data"]:
            data = d["data"]
            d["stats"] = {
                "sections": len(data.get("sections", [])),
                "flashcards": len(data.get("flashcards", [])),
                "key_terms": len(data.get("key_terms", [])),
            }
            d["summary"] = data.get("summary", "")
        d.pop("data")
    return d


def create_deck(subject_id, title, source_name, source_type, source_text):
    now = time.time()
    with connect() as c:
        cur = c.execute(
            "INSERT INTO decks (subject_id, title, source_name, source_type, status, source_text, created, updated) "
            "VALUES (?, ?, ?, ?, 'processing', ?, ?, ?)",
            (subject_id, title, source_name, source_type, source_text, now, now),
        )
        return cur.lastrowid


def finish_deck(deck_id, engine, data):
    with connect() as c:
        c.execute(
            "UPDATE decks SET status = 'ready', engine = ?, data = ?, error = NULL, updated = ? WHERE id = ?",
            (engine, json.dumps(data), time.time(), deck_id),
        )


def fail_deck(deck_id, error):
    with connect() as c:
        c.execute(
            "UPDATE decks SET status = 'failed', error = ?, updated = ? WHERE id = ?",
            (error, time.time(), deck_id),
        )


def mark_processing(deck_id):
    with connect() as c:
        c.execute("UPDATE decks SET status = 'processing', error = NULL, updated = ? WHERE id = ?", (time.time(), deck_id))


def list_decks(subject_id=None):
    with connect() as c:
        if subject_id:
            rows = c.execute("SELECT * FROM decks WHERE subject_id = ? ORDER BY created DESC", (subject_id,)).fetchall()
        else:
            rows = c.execute("SELECT * FROM decks ORDER BY created DESC").fetchall()
    return [_deck(r, full=False) for r in rows]


def get_deck(deck_id, full=True):
    with connect() as c:
        row = c.execute("SELECT * FROM decks WHERE id = ?", (deck_id,)).fetchone()
    return _deck(row, full) if row else None


def delete_deck(deck_id):
    with connect() as c:
        c.execute("DELETE FROM decks WHERE id = ?", (deck_id,))
        c.execute("DELETE FROM progress WHERE key LIKE ?", (f"deck:{deck_id}:%",))
        c.execute("DELETE FROM srs WHERE key LIKE ?", (f"deck:{deck_id}:%",))


# ---- progress -------------------------------------------------------------

def all_progress():
    with connect() as c:
        rows = c.execute("SELECT key, status, bookmarked FROM progress").fetchall()
    return {r["key"]: {"status": r["status"], "bookmarked": bool(r["bookmarked"])} for r in rows}


def set_progress(key, status=None, bookmarked=None, clear_status=False):
    """status=None keeps the stored status; clear_status=True erases it (e.g. unticking a topic)."""
    with connect() as c:
        row = c.execute("SELECT status, bookmarked FROM progress WHERE key = ?", (key,)).fetchone()
        cur_status = row["status"] if row else None
        cur_bm = row["bookmarked"] if row else 0
        new_status = None if clear_status else status if status is not None else cur_status
        new_bm = int(bookmarked) if bookmarked is not None else cur_bm
        c.execute(
            "INSERT INTO progress (key, status, bookmarked, updated) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET status = excluded.status, bookmarked = excluded.bookmarked, updated = excluded.updated",
            (key, new_status, new_bm, time.time()),
        )
    return {"status": new_status, "bookmarked": bool(new_bm)}


def reset_progress(prefix):
    with connect() as c:
        c.execute("DELETE FROM progress WHERE key LIKE ?", (prefix + "%",))


# ---- activity log (streaks, analytics) ----------------------------------------

def today():
    return date.today().isoformat()


def log_activity(kind, key=None, result=None, unit=None, minutes=0.0):
    with connect() as c:
        c.execute(
            "INSERT INTO activity (ts, day, kind, key, result, unit, minutes) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (time.time(), today(), kind, key, result, unit, minutes),
        )


def activity_by_day(since):
    with connect() as c:
        rows = c.execute(
            "SELECT day, kind, "
            "SUM(CASE WHEN kind != 'focus' THEN 1 ELSE 0 END) AS n, "
            "SUM(CASE WHEN result IN ('correct', 'good', 'easy') THEN 1 ELSE 0 END) AS ok, "
            "SUM(CASE WHEN kind = 'question' THEN 1 ELSE 0 END) AS questions, "
            "SUM(minutes) AS minutes "
            "FROM activity WHERE day >= ? GROUP BY day, kind",
            (since,),
        ).fetchall()
    return [dict(r) for r in rows]


def active_days():
    with connect() as c:
        return [r["day"] for r in c.execute("SELECT DISTINCT day FROM activity ORDER BY day").fetchall()]


# ---- spaced repetition (SM-2, tuned for exam cramming) --------------------------

GRADES = {"again": 0, "hard": 3, "good": 4, "easy": 5}


def srs_review(key, grade):
    """Update a card's schedule. Returns the new state with its next due date."""
    q = GRADES[grade]
    with connect() as c:
        row = c.execute("SELECT * FROM srs WHERE key = ?", (key,)).fetchone()
        ease, interval, reps, lapses = (row["ease"], row["interval"], row["reps"], row["lapses"]) if row else (2.5, 0, 0, 0)
        if q < 3:
            reps, interval, lapses = 0, 0, lapses + 1     # see it again in this session
        else:
            reps += 1
            if reps == 1:
                interval = 1
            elif reps == 2:
                interval = 3
            else:
                interval = max(interval + 1, round(interval * ease))
            if grade == "hard":
                interval = max(1, round(interval * 0.6))
            elif grade == "easy":
                interval = round(interval * 1.4) + 1
        ease = max(1.3, ease + 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        due = (date.today() + timedelta(days=interval)).isoformat()
        c.execute(
            "INSERT INTO srs (key, ease, interval, reps, lapses, due) VALUES (?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET ease = excluded.ease, interval = excluded.interval, "
            "reps = excluded.reps, lapses = excluded.lapses, due = excluded.due",
            (key, ease, interval, reps, lapses, due),
        )
    return {"key": key, "ease": round(ease, 2), "interval": interval, "reps": reps, "due": due}


def srs_states(prefix):
    with connect() as c:
        rows = c.execute("SELECT * FROM srs WHERE key LIKE ?", (prefix + "%",)).fetchall()
    return {r["key"]: dict(r) for r in rows}


def srs_due(prefix, on=None):
    on = on or today()
    with connect() as c:
        rows = c.execute("SELECT key FROM srs WHERE key LIKE ? AND due <= ? ORDER BY due", (prefix + "%", on)).fetchall()
    return [r["key"] for r in rows]


def srs_reset(prefix):
    with connect() as c:
        c.execute("DELETE FROM srs WHERE key LIKE ?", (prefix + "%",))


# ---- settings -------------------------------------------------------------------

def get_settings():
    with connect() as c:
        rows = c.execute("SELECT key, value FROM settings").fetchall()
    return {r["key"]: json.loads(r["value"]) for r in rows}


def set_setting(key, value):
    with connect() as c:
        if value is None:
            c.execute("DELETE FROM settings WHERE key = ?", (key,))
        else:
            c.execute(
                "INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, json.dumps(value)),
            )
