"""Local progress tracking.

Everything is stored in a SQLite file next to the app so that progress
survives restarts without needing any server or account. The file is
gitignored.
"""

from __future__ import annotations

import sqlite3
import time
from pathlib import Path
from typing import Any, Iterable

DB_PATH = Path(__file__).resolve().parents[1] / "progress.sqlite3"

SCHEMA = """
CREATE TABLE IF NOT EXISTS attempts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT    NOT NULL,
    qtype       TEXT    NOT NULL,
    lecture     INTEGER NOT NULL,
    mode        TEXT    NOT NULL,
    score       REAL    NOT NULL,
    max_score   REAL    NOT NULL,
    created_at  REAL    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_attempts_qid ON attempts(question_id);
CREATE INDEX IF NOT EXISTS idx_attempts_lecture ON attempts(lecture);

CREATE TABLE IF NOT EXISTS prefs (
    name  TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path or DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def record(conn: sqlite3.Connection, q: dict[str, Any], mode: str,
           score: float, max_score: float | None = None) -> None:
    conn.execute(
        "INSERT INTO attempts (question_id, qtype, lecture, mode, score,"
        " max_score, created_at) VALUES (?,?,?,?,?,?,?)",
        (q["id"], q["type"], q["lecture"], mode, float(score),
         float(max_score if max_score is not None else q["points"]),
         time.time()),
    )
    conn.commit()


def attempts_for(conn: sqlite3.Connection,
                 question_ids: Iterable[str]) -> dict[str, dict]:
    """Latest score per question id, restricted to the given ids."""
    ids = list(question_ids)
    if not ids:
        return {}
    out: dict[str, dict] = {}
    chunk = 400
    for i in range(0, len(ids), chunk):
        part = ids[i:i + chunk]
        placeholders = ",".join("?" * len(part))
        rows = conn.execute(
            "SELECT question_id, score, max_score, created_at FROM attempts"
            " WHERE question_id IN (%s) ORDER BY created_at" % placeholders,
            part,
        ).fetchall()
        for r in rows:
            out[r["question_id"]] = dict(r)
    return out


def by_lecture(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(
        "SELECT lecture, qtype, COUNT(*) AS n, SUM(score) AS got,"
        " SUM(max_score) AS poss, MAX(created_at) AS last_at"
        " FROM attempts GROUP BY lecture, qtype ORDER BY lecture, qtype"
    ).fetchall()
    return [dict(r) for r in rows]


def overall(conn: sqlite3.Connection) -> dict:
    row = conn.execute(
        "SELECT COUNT(*) AS n, SUM(score) AS got, SUM(max_score) AS poss"
        " FROM attempts"
    ).fetchone()
    return {
        "attempts": row["n"] or 0,
        "got": row["got"] or 0.0,
        "possible": row["poss"] or 0.0,
    }


def reset(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM attempts")
    conn.commit()


def export_rows(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(
        "SELECT question_id, qtype, lecture, mode, score, max_score, created_at"
        " FROM attempts ORDER BY created_at"
    ).fetchall()
    return [dict(r) for r in rows]


def get_pref(conn: sqlite3.Connection, name: str, default: str) -> str:
    """Read a setting. Preferences live here so they survive a restart, which
    session_state does not."""
    row = conn.execute("SELECT value FROM prefs WHERE name = ?", (name,)).fetchone()
    return row["value"] if row else default


def set_pref(conn: sqlite3.Connection, name: str, value: str) -> None:
    conn.execute(
        "INSERT INTO prefs (name, value) VALUES (?, ?)"
        " ON CONFLICT(name) DO UPDATE SET value = excluded.value",
        (name, str(value)),
    )
    conn.commit()