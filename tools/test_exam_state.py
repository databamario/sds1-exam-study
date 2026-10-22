"""Exam persistence: a refresh must not throw away an exam in progress.

Four checks. The second is the one that matters - the other three would all
still pass with the storage layer removed, because they only prove a value
survives a round trip. ``test_first_run_does_not_clobber`` is the one that
fails if someone drops the hydration guard, because the failure it prevents is
silent: the saved exam gets overwritten with the *absence* of one, on the very
first run of a fresh session, before anything has had a chance to read it.

Each check runs as one script inside a single ``AppTest`` session, so the
session state being asserted on is the same one the code under test wrote to.
Splitting setup and assertion across two AppTest instances does not work: they
have separate sessions, and assigning into ``session_state`` from outside a run
is not supported. Doing it all in one script is also closer to what happens in
the app, where it is all one run.

The browser half of the round trip - the component carrying the blob to and
from local storage - cannot run under AppTest. That is checked by hand, in
Chromium, as described in DEVELOPMENT.md.

Run via ``tools/check_all.py`` (the ninth gate) or on its own:
``python tools/test_exam_state.py``.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from streamlit.testing.v1 import AppTest  # noqa: E402


PREAMBLE = """
import json
import sys
sys.path.insert(0, %r)
import streamlit as st
from src import exam_state, progress

BANK = [{"id": "T-1", "points": 1.0, "type": "mc"},
        {"id": "T-2", "points": 2.0, "type": "wa"}]

def paper():
    return [{"id": "T-1"}, {"id": "T-2"}]

def stored(**over):
    saved = {"started": True, "start_ts": 1000.0, "paper": paper(), "idx": 1,
             "answers": {"T-1": {"a": True}, "T-2": "my written answer"},
             "seed": 4242}
    saved.update(over)
    return saved

def plant(exam, hydrated):
    \"\"\"Put a blob and a hydration flag in the session, as the browser would.\"\"\"
    st.session_state[progress.SESSION_KEY] = {
        "attempts": [], "prefs": {}, "exam": exam}
    if hydrated:
        st.session_state[progress.HYDRATED_KEY] = True

def fail(msg):
    raise AssertionError(msg)

""" % str(REPO)


def _run(body: str) -> None:
    """Run ``body`` as a Streamlit script; surface its exception as a failure."""
    at = AppTest.from_string(PREAMBLE + body + "\nst.text('done')\n")
    at.run()
    if at.exception:
        first = at.exception[0]
        msg = getattr(first, "message", None) or str(first)
        raise AssertionError(msg)


# ---------------------------------------------------------------------------
# 1. A saved exam comes back with its answers and its position.
# ---------------------------------------------------------------------------
def test_restore_brings_back_answers() -> None:
    _run(
        """
plant(stored(), hydrated=True)
conn = progress.connect()
exam_state.load(conn, BANK)
s = st.session_state
if not s.get("exam_started"):        fail("exam_started not restored")
if s.get("exam_idx") != 1:            fail("exam_idx not restored: %r" % s.get("exam_idx"))
if s.get("exam_answers", {}).get("T-1") != {"a": True}:
    fail("MC answers not restored: %r" % s.get("exam_answers"))
if s.get("exam_answers", {}).get("T-2") != "my written answer":
    fail("WA answers not restored: %r" % s.get("exam_answers"))
if not s.get("paper"):               fail("paper not restored")
if s.get("paper")[0].get("id") != "T-1": fail("wrong paper restored")
if s.get("exam_start_ts") != 1000.0:  fail("start_ts not restored")
if s.get("exam_seed") != 4242:        fail("seed not restored")
"""
    )


# ---------------------------------------------------------------------------
# 2. The first run of a session must not write what it does not know yet.
# ---------------------------------------------------------------------------
def test_first_run_does_not_clobber() -> None:
    """The guard, on the state that actually exists on the first run of a session.

    Before the browser answers, the session mirror holds the empty default while
    the real exam sits unread in local storage. That is the moment the guard
    exists for: the mirror says "no exam", and writing on that belief replaces
    the stored one with the absence of it.

    Asserting on the mirror cannot catch that - the mirror already holds None,
    so a write of None is invisible in it. The damage is in the browser, so the
    spy stands in for the browser: it records every op that would have been sent
    to local storage. With the guard removed this sees a ``set_exam`` carrying
    None, which is precisely the overwrite that loses the exam.
    """
    _run(
        """
SENT = []
real_write = progress._write
def spy(op, payload=None):
    SENT.append((op, payload))
progress._write = spy

# The first run of a session: empty mirror, hydration flag unset.
plant(None, hydrated=False)
if progress.hydrated():
    fail("a non-hydrated session reported hydrated")

# connect() once only: hydrate() renders a component with a fixed key, so a
# second call in the same run trips Streamlit's duplicate-key check.
conn = progress.connect()
if progress.read_exam(conn) is not None:
    fail("fixture is wrong: nothing should be readable before hydration")

exam_state.load(conn, BANK)
exam_state.save(conn)

clobbers = [p for op, p in SENT if op == "set_exam"]
if clobbers:
    fail("save() sent %r to local storage before the browser had been read; "
         "that overwrites the stored exam with the absence of one" % clobbers)

progress._write = real_write
"""
    )


# ---------------------------------------------------------------------------
# 3. A paper naming a question the bank no longer has is dropped, not rendered.
# ---------------------------------------------------------------------------
def test_stale_paper_is_discarded() -> None:
    _run(
        """
plant(stored(paper=[{"id": "T-1"}, {"id": "REMOVED-IN-A-DEPLOY"}]), hydrated=True)
exam_state.load(progress.connect(), BANK)
if st.session_state.get("exam_started"):
    fail("a paper with a missing question was adopted; rendering it would raise")
notice = exam_state.notice()
if not notice or "could not be resumed" not in notice:
    fail("no notice explaining the dropped exam: %r" % notice)
"""
    )


# ---------------------------------------------------------------------------
# 4. Handing the paper in clears it, so a later refresh cannot revive it.
# ---------------------------------------------------------------------------
def test_finish_clears_exam() -> None:
    _run(
        """
plant(stored(), hydrated=True)
conn = progress.connect()
exam_state.load(conn, BANK)
if st.session_state[progress.SESSION_KEY]["exam"] is None:
    fail("nothing was saved to clear")
st.session_state["exam_started"] = False
exam_state.save(conn)
if st.session_state[progress.SESSION_KEY]["exam"] is not None:
    fail("a handed-in paper was left resumable")
"""
    )


def main() -> int:
    failures = []
    for name, fn in [
        ("test_restore_brings_back_answers", test_restore_brings_back_answers),
        ("test_first_run_does_not_clobber", test_first_run_does_not_clobber),
        ("test_stale_paper_is_discarded", test_stale_paper_is_discarded),
        ("test_finish_clears_exam", test_finish_clears_exam),
    ]:
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            failures.append(name)
            print("[FAIL] %s: %s" % (name, exc), file=sys.stderr)
        else:
            print("[ok] %s" % name)
    if failures:
        print("%d failure(s): %s" % (len(failures), ", ".join(failures)),
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())