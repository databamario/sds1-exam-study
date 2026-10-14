"""Practice views: MC and WA as two separate study modes."""

from __future__ import annotations

import streamlit as st

from .. import loader, progress, ui
from ..scoring import wa_partial_credit


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
    st.subheader("Multiple-choice practice (MC)")
    st.caption(
        "Mark ALL correct options - there may be none, or more than one. "
        "Each question is worth 1 point: 1.0 for all correct and nothing extra, "
        "0.5 for exactly one mistake, 0.0 for two or more."
    )
    questions = loader.of_type(bank, loader.MC)
    if not questions:
        st.info("No MC questions available yet.")
        return
    pool = _pick(questions, "mc", "Lecture")
    ui.grade_mc_session(pool, conn)
    _summary(pool)


def _summary(pool):
    done = st.session_state.get("mc_done", {})
    if not done:
        return
    total = 0.0
    for q in pool:
        if q["id"] in done:
            from ..scoring import score_mc
            total += score_mc(q["correct"], done[q["id"]])
    st.divider()
    st.metric("Points so far", "%.1f / %d" % (total, len(pool)))


def wa_practice(bank, conn):
    st.subheader("Written-answer practice (WA)")
    st.caption(
        "Write your answer first, then reveal the model answer and grade yourself "
        "against the checklist. The exam allows partial credit for partial answers, "
        "and asks for a short and succinct answer (max 3 sentences) unless stated "
        "otherwise."
    )
    questions = loader.of_type(bank, loader.WA)
    if not questions:
        st.info("No WA questions available yet.")
        return
    pool = _pick(questions, "wa", "Lecture")

    st.session_state.setdefault("wa_idx", 0)
    st.session_state.setdefault("wa_graded", {})

    if not pool:
        st.info("No questions for this lecture yet.")
        return

    i = min(st.session_state.wa_idx, len(pool) - 1)
    q = pool[i]
    st.caption("Question %d of %d" % (i + 1, len(pool)))
    ui.render_stem(q)

    graded = q["id"] in st.session_state.wa_graded
    answer = st.text_area(
        "Your answer",
        value=st.session_state.get("wa_draft_%s" % q["id"], ""),
        height=150,
        disabled=graded,
        key="wa_in_%s" % q["id"],
    )
    st.session_state["wa_draft_%s" % q["id"]] = answer

    if not graded:
        left, right = st.columns(2)
        with left:
            if st.button("Reveal model answer", type="primary",
                         use_container_width=True):
                st.session_state.wa_graded[q["id"]] = 0.0
                st.rerun()
        with right:
            if st.button("Skip", use_container_width=True):
                st.session_state.wa_idx = (i + 1) % len(pool)
                st.rerun()
    else:
        ui.render_wa_key(q)
        st.markdown("**Self-grade**")
        total = 0.0
        n_el = 0
        hits_map = {}
        for idx, item in enumerate(q["rubric"]):
            elements = item["elements"]
            n_el += elements
            cols = st.columns([6, 1])
            with cols[0]:
                st.markdown("- %s" % item["text"])
            with cols[1]:
                hit = st.number_input(
                    "hits", min_value=0, max_value=elements, value=0,
                    step=1, key="wa_hit_%s_%d" % (q["id"], idx),
                    label_visibility="collapsed",
                )
            hits_map[idx] = int(hit)
        total = sum(wa_partial_credit(hits_map[i], q["rubric"][i]["elements"],
                                      q["points"]) for i in hits_map)
        st.metric("Your score", "%.1f / %d pt" % (total, q["points"]))
        if st.button("Save and continue", type="primary"):
            progress.record(conn, q, "WA practice", total, q["points"])
            st.session_state.wa_idx = (i + 1) % len(pool)
            st.rerun()
        if st.button("Save and stay"):
            progress.record(conn, q, "WA practice", total, q["points"])
            st.rerun()