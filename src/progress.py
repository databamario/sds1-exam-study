"""Progress tracking, kept in the browser rather than in a file.

This used to be a SQLite database next to the app, which is right on one
machine and wrong on a deployed one. The file belongs to the app, not to the
person using it, so on a shared deployment everyone's history lands in the same
table and the progress screen shows numbers that are not yours. And the cloud
disk is ephemeral, so the history disappears at the next deploy.

Local storage in the browser fixes both. There is no server, no account, and
nothing to sign in to. The price is that progress belongs to one browser: study
on the laptop and it is there, and it does not follow you to the phone.

Two mechanisms are used, because they are good at different things.

``components.html`` writes. It renders an iframe, and that iframe turned out to
be same-origin and able to reach the page's real, persistent local storage -
tested rather than assumed, after the docstring calling it "sandboxed" suggested
it might not be. What it cannot do is return a value, which is fine for a write.

A small declared component reads, because reading is needed: the progress screen
is built from these numbers, and only ``setComponentValue`` carries anything
back to Python. Its build output is committed, so a deploy needs no npm.

The public functions keep the names and signatures they had, including the
``store`` argument that used to be a database connection. Nothing above this
module has to change, and nothing above it ever knew what SQLite was.
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Iterable

import streamlit as st
import streamlit.components.v1 as components

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPONENT_DIR = os.path.join(REPO, "_progress_component")

STORAGE_KEY = "sds1-progress-v1"
SESSION_KEY = "_sds1_progress_blob"
NONCE_KEY = "_sds1_progress_nonce"
HYDRATED_KEY = "_sds1_progress_hydrated"

# ``exam`` holds an in-progress mock exam: the paper, the question index, the
# answers and the wall-clock start time. It lives in the same blob as progress
# because it is the same kind of thing - something the person using the app
# would be furious to lose to a browser refresh - and because this module is
# already the one place that knows how to read and write browser storage.
_EMPTY: dict[str, Any] = {"attempts": [], "prefs": {}, "exam": None}

MAX_ATTEMPTS = 20000


class Store:
    """A handle, in the spirit of the connection object this replaced.

    It carries no state worth having. Reads come from the session mirror and
    writes go straight to the browser, so the object exists only so that the
    call sites that thread a handle through the app - and pass it to
    ``record()`` when an answer is graded - keep working unchanged.
    """

    __slots__ = ()

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return "<progress store: browser local storage>"


def _component():
    return components.declare_component(
        "sds1_progress", path=COMPONENT_DIR
    )


def _decode(raw: Any) -> dict:
    """The blob, whatever shape it arrives in.

    The component hands back a dict on a healthy run, but a default of ``None``
    arrives on the first run of a session, and a hand-edited or truncated value
    in local storage should not take the app down. Anything unusable becomes an
    empty progress rather than an exception.
    """
    if isinstance(raw, dict):
        attempts = raw.get("attempts")
        prefs = raw.get("prefs")
        exam = raw.get("exam")
        return {
            "attempts": list(attempts) if isinstance(attempts, list) else [],
            "prefs": dict(prefs) if isinstance(prefs, dict) else {},
            "exam": dict(exam) if isinstance(exam, dict) else None,
        }
    if isinstance(raw, str) and raw.strip():
        try:
            return _decode(json.loads(raw))
        except (ValueError, TypeError):
            pass
    return dict(_EMPTY)


def _mirror() -> dict:
    return st.session_state.get(SESSION_KEY) or dict(_EMPTY)


def hydrate() -> dict:
    """Ask the browser for the stored progress and keep it in the session.

    Called once per run from :func:`connect`. A component's value arrives on the
    run *after* the call, so on the very first run of a session there is nothing
    to read yet and the app renders with empty progress for that one frame. That
    is fine, and deliberately not optimised away.

    This used to call ``st.rerun()`` to hide that first empty frame, and on a
    deployed app it took the whole thing down: the component was never loading,
    so the value never arrived, so ``st.rerun()`` fired again, forever. The script
    never finished, no deltas were ever sent, and the page stayed blank with no
    error anywhere - just a Stop button that never became a Rerun button. The
    rerun was unnecessary as well as fatal: passing ``key=`` makes Streamlit
    store the component value and rerun *by itself* when that value changes,
    which is the one rerun this function actually wanted. So there is none here.

    The general lesson, since it cost an hour: a loop waiting for a value that
    may never arrive must be bounded, and if it cannot be bounded it must not
    exist. A missing component should cost the progress screen, not the app.
    """
    nonce = st.session_state.get(NONCE_KEY, 0) + 1
    st.session_state[NONCE_KEY] = nonce

    returned = _component()(
        op="read", payload=None, nonce=nonce, key="sds1_progress", default=None
    )
    if returned is not None:
        st.session_state[SESSION_KEY] = _decode(returned)
        # Only a value that actually came back counts as hydrated. Until this
        # flips, ``_mirror()`` is the empty default and knows nothing about the
        # browser - so anything that would *write* based on it has to hold off,
        # or the first run of a fresh session overwrites real stored data with
        # the absence of it.
        st.session_state[HYDRATED_KEY] = True

    st.session_state[SESSION_KEY] = _decode(st.session_state.get(SESSION_KEY))
    return st.session_state[SESSION_KEY]


def hydrated() -> bool:
    """True once the browser's stored blob has actually arrived this session.

    False on the first run of every session, and stays false if the component
    never loads. That is the point: it is the difference between "there is
    nothing stored" and "we have not found out yet", and :func:`set_exam` uses
    it to refuse to write before the second one.
    """
    return bool(st.session_state.get(HYDRATED_KEY))


def _write(op: str, payload: Any = None) -> None:
    """Apply a change in the browser, and in the session mirror.

    ``components.html`` runs its script as soon as it is rendered, so the write
    is durable immediately rather than a run later, which matters because the
    session does not outlive the browser tab. The mirror is updated here too so
    that anything reading progress in this same run sees the change.
    """
    components.html(
        """
        <script>
        (function () {
          var KEY = %s;
          function read() {
            try {
              var raw = window.localStorage.getItem(KEY);
              if (!raw) return { attempts: [], prefs: {}, exam: null };
              var p = JSON.parse(raw);
              return {
                attempts: Array.isArray(p.attempts) ? p.attempts : [],
                prefs: p.prefs && typeof p.prefs === "object" ? p.prefs : {},
                exam: p.exam && typeof p.exam === "object" ? p.exam : null
              };
            } catch (e) { return { attempts: [], prefs: {}, exam: null }; }
          }
          function write(b) {
            if (b.attempts.length > %d) {
              b.attempts = b.attempts.slice(b.attempts.length - %d);
            }
            try { window.localStorage.setItem(KEY, JSON.stringify(b)); }
            catch (e) { /* quota or private mode: the session mirror still has it */ }
          }
          var blob = read();
          var op = %s, payload = %s;
          if (op === "record") { blob.attempts.push(payload); }
          else if (op === "reset") { blob.attempts = []; }
          else if (op === "set_pref") { blob.prefs[payload.name] = String(payload.value); }
          else if (op === "set_exam") { blob.exam = payload; }
          write(blob);
        })();
        </script>
        """
        % (json.dumps(STORAGE_KEY), MAX_ATTEMPTS, MAX_ATTEMPTS,
           json.dumps(op), json.dumps(payload)),
        height=0,
    )


def connect(db_path=None) -> Store:
    """Open the progress store.

    ``db_path`` is accepted and ignored. It used to name the SQLite file; nothing
    passes it any more, and refusing to accept it would mean changing the one
    call site in ``app.py`` for no gain.
    """
    hydrate()
    return Store()


def record(store: Any, q: dict, mode: str, score: float,
           max_score: float | None = None) -> None:
    """Record one graded answer."""
    row = {
        "question_id": q["id"],
        "qtype": q["type"],
        "lecture": q["lecture"],
        "mode": mode,
        "score": float(score),
        "max_score": float(max_score if max_score is not None else q["points"]),
        "created_at": time.time(),
    }
    blob = _mirror()
    blob["attempts"] = (list(blob.get("attempts") or []) + [row])[-MAX_ATTEMPTS:]
    st.session_state[SESSION_KEY] = blob
    _write("record", row)


def _rows() -> list[dict]:
    return [r for r in (_mirror().get("attempts") or []) if isinstance(r, dict)]


def attempts_for(store: Any, question_ids: Iterable[str]) -> dict[str, dict]:
    """Latest score for each of the given question ids.

    Retained from the database version, and it is the one function here that no
    call site uses. Kept because it is the natural companion to ``record()`` and
    costs six lines; it can go if a future change wants it gone.
    """
    wanted = set(question_ids)
    latest: dict[str, dict] = {}
    for row in _rows():
        qid = row.get("question_id")
        if qid in wanted:
            latest[qid] = row
    return latest


def by_lecture(store: Any) -> list[dict]:
    """Attempts grouped by lecture and question type, as the progress table wants."""
    groups: dict[tuple, dict] = {}
    for row in _rows():
        key = (row.get("lecture"), row.get("qtype"))
        g = groups.setdefault(key, {"lecture": key[0], "qtype": key[1],
                                    "n": 0, "got": 0.0, "poss": 0.0,
                                    "last_at": 0.0})
        g["n"] += 1
        g["got"] += float(row.get("score") or 0.0)
        g["poss"] += float(row.get("max_score") or 0.0)
        g["last_at"] = max(g["last_at"], float(row.get("created_at") or 0.0))
    return sorted(groups.values(),
                  key=lambda g: (g["lecture"] or 0, str(g["qtype"])))


def overall(store: Any) -> dict:
    """Totals for the progress screen."""
    rows = _rows()
    return {
        "attempts": len(rows),
        "got": sum(float(r.get("score") or 0.0) for r in rows),
        "possible": sum(float(r.get("max_score") or 0.0) for r in rows),
    }


def reset(store: Any) -> None:
    """Throw the history away.

    The in-progress exam is left alone. Progress is a record of what you have
    done; an exam you are halfway through is work in hand, and wiping the
    record should not silently throw that out too. It goes when you press
    "Start the 4-hour exam" or finish and grade, both of which call
    :func:`set_exam` explicitly.
    """
    # The mirror keeps the exam, because the JS below only clears attempts.
    # Dropping it here would make the mirror disagree with local storage, and
    # the next set_exam() would then write that disagreement through.
    blob = _mirror()
    blob["attempts"] = []
    st.session_state[SESSION_KEY] = blob
    _write("reset")


def export_rows(store: Any) -> list[dict]:
    """Every attempt, oldest first."""
    return sorted(_rows(), key=lambda r: float(r.get("created_at") or 0.0))


def get_pref(store: Any, name: str, default: str) -> str:
    """Read a setting, for instance whether the sound is on."""
    prefs = _mirror().get("prefs") or {}
    value = prefs.get(name)
    return default if value is None else str(value)


def set_pref(store: Any, name: str, value: str) -> None:
    """Store a setting so it survives a restart."""
    blob = _mirror()
    prefs = dict(blob.get("prefs") or {})
    prefs[name] = str(value)
    blob["prefs"] = prefs
    st.session_state[SESSION_KEY] = blob
    _write("set_pref", {"name": name, "value": value})


def read_exam(store: Any) -> dict | None:
    """The in-progress mock exam, or ``None`` if there is none.

    Returns ``None`` when the browser has not been read yet, and also when it
    has and holds no exam. The caller cannot tell those apart, which is
    deliberate: from :mod:`src.exam_state` they need the same answer, namely
    "do not adopt anything", and the one case where the difference matters -
    writing - is gated on :func:`hydrated` instead.
    """
    exam = _mirror().get("exam")
    return dict(exam) if isinstance(exam, dict) else None


def set_exam(store: Any, exam: dict | None) -> None:
    """Save, or clear with ``None``, the in-progress mock exam.

    Refuses to write before the browser has answered, because the mirror is the
    empty default until then and writing would replace a real saved exam with
    the knowledge that none was found. See :func:`hydrated`.
    """
    if not hydrated():
        return
    blob = _mirror()
    blob["exam"] = dict(exam) if isinstance(exam, dict) else None
    st.session_state[SESSION_KEY] = blob
    _write("set_exam", blob["exam"])