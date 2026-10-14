"""Timed mock exam mirroring the real paper: mixed MC and WA, 41 points, 4 hours."""

from __future__ import annotations

import time

import streamlit as st

from .. import loader, progress, ui
from ..scoring import score_mc

EXAM_MINUTES = 240
EXAM_POINTS = 41

# The HT25 mock had 9 MC out of 29 questions, so roughly a third of the paper
# is multiple-choice. We aim for a similar split by points rather than filling
# greedily, which otherwise produces an all-written-answer paper.
MC_POINT_SHARE = 0.33


def _build_paper(bank, seed=None):
    """Build a mixed MC/WA paper worth about EXAM_POINTS."""
    seed = st.session_state.get("exam_seed", 42) if seed is None else seed
    mc_pool = loader.shuffled(loader.of_type(bank, loader.MC), seed=seed)
    wa_pool = loader.shuffled(loader.of_type(bank, loader.WA), seed=seed + 1)

    paper: list[dict] = []
    total = 0.0
    mc_points = 0.0
    mc_budget = EXAM_POINTS * MC_POINT_SHARE

    for q in mc_pool:
        if mc_points >= mc_budget or total + q["points"] > EXAM_POINTS:
            break
        paper.append(q)
        mc_points += q["points"]
        total += q["points"]

    wa_added = False
    for q in wa_pool:
        if total >= EXAM_POINTS:
            break
        if total + q["points"] > EXAM_POINTS:
            continue
        paper.append(q)
        wa_added = True
        total += q["points"]

    # Top up with any remaining MC so the paper really lands on EXAM_POINTS.
    if total < EXAM_POINTS:
        for q in mc_pool:
            if total >= EXAM_POINTS:
                break
            if q in paper:
                continue
            if total + q["points"] > EXAM_POINTS:
                continue
            paper.append(q)
            total += q["points"]

    # Interleave so the paper alternates rather than being all MC then all WA.
    paper.sort(key=lambda q: (0 if q["type"] == loader.MC else 1, q["id"]))
    return paper


def mock_exam(bank, conn):
    st.subheader("Mock exam")
    st.caption(
        "Mirrors the real paper: mixed MC and WA, %d points, %d minutes. "
        "As on the exam you are not asked to grind through calculations - show the "
        "formula with the values substituted." % (EXAM_POINTS, EXAM_MINUTES)
    )

    if "exam_started" not in st.session_state:
        st.session_state.exam_started = False
        st.session_state.exam_start_ts = None
        st.session_state.exam_answers = {}
        st.session_state.exam_seed = 42
        st.session_state.exam_idx = 0

    if not st.session_state.exam_started:
        paper = _build_paper(bank)
        if not paper:
            st.info("Not enough questions to build a paper yet.")
            return
        n_mc = sum(1 for q in paper if q["type"] == loader.MC)
        n_wa = len(paper) - n_mc
        st.markdown(
            "**This paper:** %d points across %d questions "
            "(%d MC, %d WA)." % (sum(q["points"] for q in paper), len(paper),
                                 n_mc, n_wa)
        )
        seed_in = st.number_input("Paper seed (change to get a different paper)",
                                  value=st.session_state.exam_seed,
                                  step=1, key="exam_seed_in")
        if st.button("Start the 4-hour exam", type="primary"):
            st.session_state.exam_seed = int(seed_in)
            st.session_state.paper = _build_paper(bank)
            st.session_state.exam_started = True
            st.session_state.exam_start_ts = time.time()
            st.session_state.exam_answers = {}
            st.session_state.exam_idx = 0
            st.rerun()
        return

    paper = st.session_state.get("paper", [])
    if not paper:
        st.session_state.exam_started = False
        st.rerun()

    elapsed = time.time() - st.session_state.exam_start_ts
    left = max(0.0, EXAM_MINUTES * 60 - elapsed)
    hh, rem = divmod(int(left), 3600)
    mm, ss = divmod(rem, 60)
    timer = st.empty()
    timer.metric("Time remaining", "%02d:%02d:%02d" % (hh, mm, ss))

    if left <= 0:
        st.error("Time is up. Submit your answers.")
        st.session_state.exam_started = False

    idx = min(st.session_state.exam_idx, len(paper) - 1)
    q = paper[idx]
    answers = st.session_state.exam_answers

    st.caption("Question %d of %d" % (idx + 1, len(paper)))
    ui.render_stem(q)

    if q["type"] == loader.MC:
        chosen = answers.get(q["id"], {})
        st.markdown("**Mark ALL correct options.**")
        opts = []
        for label, text in q["options"].items():
            key = "exam_%s_%s" % (q["id"], label)
            if st.checkbox("%s) %s" % (label, text), value=chosen.get(label, False),
                           key=key):
                opts.append(label)
            answers[q["id"]] = {l: (l in opts) for l in q["options"]}
    else:
        key = "exam_wa_%s" % q["id"]
        val = answers.get(q["id"], "")
        new = st.text_area("Your answer (max 3 sentences unless stated otherwise)",
                           value=val, height=140, key=key)
        answers[q["id"]] = new

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Previous", disabled=idx == 0, use_container_width=True):
            st.session_state.exam_idx = idx - 1
            st.rerun()
    with c2:
        if st.button("Next", disabled=idx >= len(paper) - 1,
                     use_container_width=True):
            st.session_state.exam_idx = idx + 1
            st.rerun()
    with c3:
        if st.button("Finish and grade", type="primary", use_container_width=True):
            _grade(bank, conn, paper, answers)
            st.session_state.exam_started = False
            st.rerun()


def _grade(bank, conn, paper, answers):
    """Grade MC automatically, collect WA for self-grading."""
    mc_total = 0.0
    mc_n = 0
    wa_pending = []
    for q in paper:
        if q["type"] == loader.MC:
            marked = [l for l, on in (answers.get(q["id"], {}) or {}).items() if on]
            mc_total += score_mc(q["correct"], marked)
            mc_n += 1
            progress.record(conn, q, "Mock exam", score_mc(q["correct"], marked), 1.0)
        else:
            wa_pending.append(q)

    st.session_state.exam_result = {
        "mc_total": mc_total,
        "mc_n": mc_n,
        "wa_pending": wa_pending,
        "paper": paper,
        "answers": answers,
    }


def render_result(bank):
    res = st.session_state.get("exam_result")
    if not res:
        return
    st.subheader("Result")
    st.metric("MC score", "%.1f / %d" % (res["mc_total"], res["mc_n"]))
    st.caption(
        "WA questions are graded by you below against the model answers, mirroring "
        "how partial credit works on the real paper."
    )
    paper = {q["id"]: q for q in res["paper"]}
    answers = res["answers"]
    for q in res["wa_pending"]:
        with st.expander("%s  (%d pt)" % (q["id"], q["points"])):
            st.markdown("**Your answer**")
            st.write(answers.get(q["id"]) or "_(not answered)_")
            st.markdown("**Model answer**")
            st.markdown(q["answer"])
            for item in q["rubric"]:
                st.markdown("- %s" % item["text"])
    if st.button("Clear result"):
        st.session_state.exam_result = None
        st.rerun()