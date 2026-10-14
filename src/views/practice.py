"""Practice views: MC and WA as two separate study modes.

Both modes run through the same one-question-at-a-time loop in ``ui`` so the
mechanics are identical whichever one you are in.
"""

from __future__ import annotations

import streamlit as st

from .. import loader, ui


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
        seed = st.session_state.get(key + "_seed")
        if seed is None:
            seed = st.session_state[key + "_seed"] = int(st.session_state.get(
                "_seed_counter", 0)) + 1
            st.session_state["_seed_counter"] = seed
        pool = loader.shuffled(pool, seed=seed)
        if st.button("Shuffle again", key=key + "_reshuffle"):
            st.session_state[key + "_seed"] = seed + 1
            st.rerun()
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
        "Write your answer first, then reveal the model answer and tap the points "
        "you covered. The exam asks for at most 3 sentences and allows partial "
        "credit."
    )
    questions = loader.of_type(bank, loader.WA)
    if not questions:
        st.info("No WA questions available yet.")
        return
    pool = _pick(questions, "wa", "Lecture")
    ui.question_loop(pool, "WA", conn)
