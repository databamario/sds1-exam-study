"""An in-progress mock exam, kept in the browser so a refresh does not lose it.

The exam lived entirely in ``st.session_state``, which lives in the memory of
one Streamlit session. Press F5 and that memory is gone: the page comes back at
Home, and opening Mock exam again shows "Start the 4-hour exam" with an empty
paper. For a four-hour paper that is not a cosmetic annoyance, it is the work.

So the exam is saved to the same browser storage that already holds progress,
through :mod:`src.progress`, and read back when a new session starts.

Two rules this module exists to enforce:

**Never write before the browser has answered.** A component's value arrives on
the run *after* the call, so the first run of every session sees an empty blob.
Treating that as "there is no saved exam" and writing it back destroys the saved
exam before anyone has read it. :func:`progress.hydrated` distinguishes "nothing
is stored" from "we have not found out yet", and :func:`save` refuses to write
until they can be told apart.

**Never trust a saved paper.** The paper is stored by question id. If a deploy
changes the bank, an id can stop existing, and rendering a missing question
would take the page down with a ``TypeError`` on ``None``. :func:`load` drops a
paper with any unknown id and says so, rather than rendering half of an exam
that no longer adds up.
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from . import progress

# Set once per session, by the first load(). Without it, every later rerun would
# look at the stored exam again and adopt it over the top of whatever the
# person is doing now - including re-adopting a paper they just replaced.
LOADED_KEY = "_sds_exam_state_loaded"
# Why the last load() declined, for the view to render.
NOTICE_KEY = "_sds_exam_notice"


def _valid_ids(bank: list[dict]) -> set[str]:
    return {q["id"] for q in bank}


def _paper_is_intact(paper: Any, ids: set[str]) -> bool:
    if not isinstance(paper, list) or not paper:
        return False
    return all(isinstance(q, dict) and q.get("id") in ids for q in paper)


def load(conn: Any, bank: list[dict]) -> None:
    """Adopt a saved exam into this session, if there is one worth adopting.

    Does nothing at all on the first run of a session, because the browser has
    not answered yet. Streamlit re-runs the script by itself when the component
    value arrives, so the second run is where the exam appears - which is why
    the restore notice lives in session state rather than being printed here.
    """
    if st.session_state.get(LOADED_KEY):
        return
    st.session_state[LOADED_KEY] = True
    st.session_state.pop(NOTICE_KEY, None)

    saved = progress.read_exam(conn)
    if not saved:
        return

    ids = _valid_ids(bank)
    if not _paper_is_intact(saved.get("paper"), ids):
        st.session_state[NOTICE_KEY] = (
            "The exam you had in progress could not be resumed: the question "
            "bank has changed since it was saved. Start a fresh paper below."
        )
        return

    started = bool(saved.get("started"))
    if not started:
        # Saved by an earlier version, or saved on the way into the start
        # screen. Nothing to resume, but the seed is worth keeping so the
        # paper offered is the one that was going to be sat.
        seed = saved.get("seed")
        if seed is not None:
            st.session_state["exam_seed"] = int(seed)
        return

    st.session_state["exam_started"] = True
    st.session_state["exam_start_ts"] = saved.get("start_ts")
    st.session_state["exam_answers"] = saved.get("answers") or {}
    st.session_state["exam_idx"] = int(saved.get("idx") or 0)
    st.session_state["exam_seed"] = saved.get("seed")
    st.session_state["paper"] = saved["paper"]
    st.session_state[NOTICE_KEY] = (
        "Picked your exam back up where you left it."
    )


def save(conn: Any) -> None:
    """Snapshot the exam to browser storage, if there is one in progress.

    Safe to call on every run. Does nothing before hydration, and does nothing
    once the exam has been handed in, so a refresh after finishing cannot bring
    a marked paper back.
    """
    if not progress.hydrated():
        return
    if not st.session_state.get("exam_started"):
        progress.set_exam(conn, None)
        return
    progress.set_exam(
        conn,
        {
            "started": True,
            "start_ts": st.session_state.get("exam_start_ts"),
            "paper": st.session_state.get("paper") or [],
            "idx": st.session_state.get("exam_idx") or 0,
            "answers": st.session_state.get("exam_answers") or {},
            "seed": st.session_state.get("exam_seed"),
        },
    )


def notice() -> str | None:
    """The message from the last :func:`load`, for the view to show."""
    return st.session_state.get(NOTICE_KEY)


def discard(conn: Any) -> None:
    """Drop the saved exam without touching the running session.

    Used by the "start a fresh paper" button on the restore notice, so the next
    refresh does not resurrect what the person just chose to abandon.
    """
    progress.set_exam(conn, None)