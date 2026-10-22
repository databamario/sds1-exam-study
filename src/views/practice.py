"""Practice views: MC and WA as two separate study modes.

Both modes run through the same one-question-at-a-time loop in ``ui`` so the
mechanics are identical whichever one you are in.
"""

from __future__ import annotations

import streamlit as st

from .. import loader, ui


def _new_seed() -> int:
    """Fresh seed for a new shuffled order.

    Earlier this read 1 once and never changed - the seed was stashed in
    ``st.session_state``, which persists across reloads on cloud deploys,
    so every visit produced the same shuffled order. ``SystemRandom`` is
    fine for shuffling (you just want unpredictability here, not secrecy),
    and ``setdefault`` only fires the first time so a user revisiting the
    same quiz mid-practice sees the same order, which is what they want.

    Bounded to 2**31 to match ``mock_exam._new_seed``: anything wider does
    not buy a more varied order for a ~50-question pool and risks overflow
    if a future change decides to display the value.
    """
    import random
    return random.SystemRandom().randrange(2**31)


def _pick(questions, key, label):
    """Lecture / ordering controls shared by both practice modes."""
    lectures = sorted({q["lecture"] for q in questions})
    cols = st.columns([2, 3])
    with cols[0]:
        lec = st.selectbox(
            label, lectures,
            format_func=lambda n: "%d - %s" % (n, loader.LECTURES[n]),
            key=key + "_lec",
        )
    with cols[1]:
        order = st.radio(
            "Order", ["Lecture order", "Shuffled"], horizontal=True, key=key + "_ord"
        )
    pool = [q for q in questions if q["lecture"] == lec]
    if order == "Shuffled":
        seed_key = key + "_seed"
        if st.button("Shuffle again", key=key + "_reshuffle"):
            st.session_state[seed_key] = _new_seed()
            st.rerun()
        seed = st.session_state.setdefault(seed_key, _new_seed())
        pool = loader.shuffled(pool, seed=seed)
    return pool


def mc_practice(bank, conn):
    st.subheader("Multiple-choice practice")
    st.caption(
        "One point each: 1.0 for every correct option marked and nothing extra, "
        "0.5 for exactly one mistake, 0.0 for two or more."
    )
    questions = loader.of_type(bank, loader.MC)
    if not questions:
        st.info("No MC questions available yet.")
        return
    pool = _pick(questions, "mc", "Lecture")
    ui.question_loop(pool, "MC", conn)


def wa_practice(bank, conn):
    st.subheader("Written-answer practice")
    st.caption(
        "Write your answer, then mark yourself against the checklist. The model "
        "answer stays hidden until you ask for it, which is the only way the "
        "self-grading is worth anything. The exam asks for at most 3 sentences and "
        "allows partial credit."
    )
    questions = loader.of_type(bank, loader.WA)
    if not questions:
        st.info("No WA questions available yet.")
        return
    pool = _pick(questions, "wa", "Lecture")
    ui.question_loop(pool, "WA", conn)
