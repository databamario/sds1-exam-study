"""Timed mock exam mirroring the real paper: mixed MC and WA, 41 points, 4 hours."""

from __future__ import annotations

import time

import streamlit as st

from .. import celebrate, exam_state, loader, progress, ui
from ..scoring import score_mc

EXAM_MINUTES = 240
EXAM_POINTS = 41

# The HT25 mock had 9 MC out of 29 questions, so roughly a third of the paper
# is multiple-choice. We aim for a similar split by points rather than filling
# greedily, which otherwise produces an all-written-answer paper.
MC_POINT_SHARE = 0.33


def _new_seed() -> int:
    """Fresh seed for a new mock exam paper.

    Earlier this defaulted to 42 once and never changed - the seed was
    stashed in ``st.session_state``, which persists across reloads on
    cloud deploys, so every visit produced the same paper. The seed input
    still defaults to 42 in the UI for stability, but the first time
    someone opens the mock exam after a fresh deploy the value is a real
    random number instead, and a Randomize button next to the input
    lets them swap to a different paper mid-session without rerunning the
    script.

    The range is bounded to a 31-bit unsigned integer. ``getrandbits(64)``
    produced values up to 2**64-1, which JavaScript - and therefore
    Streamlit's number_input widget - cannot represent exactly: the JS
    number sends half of them through as floating-point and the widget
    raises ``StreamlitJSNumberBoundsError`` at render. 2**31 covers every
    case the paper builder actually needs to vary.
    """
    import random
    return random.SystemRandom().randrange(2**31)


def _build_paper(bank, seed=None):
    """Build a mixed MC/WA paper worth about EXAM_POINTS."""
    if seed is None:
        seed = st.session_state.setdefault("exam_seed", _new_seed())
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

    # Before the defaults below, because load() is what fills them in. It is a
    # no-op on the first run of a session - the browser has not been read yet -
    # and Streamlit re-runs this script by itself when the value arrives.
    exam_state.load(conn, bank)

    if "exam_started" not in st.session_state:
        st.session_state.exam_started = False
        st.session_state.exam_start_ts = None
        st.session_state.exam_answers = {}
        st.session_state.setdefault("exam_seed", _new_seed())
        st.session_state.exam_idx = 0

    saved_notice = exam_state.notice()
    if saved_notice and st.session_state.exam_started:
        st.info(saved_notice)

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
        cols = st.columns([3, 1])
        with cols[0]:
            seed_in = st.number_input(
                "Paper seed",
                value=st.session_state.exam_seed,
                step=1,
                key="exam_seed_in",
                help="Type a number to pin the paper, or click Randomize for a new one.",
            )
        with cols[1]:
            if st.button("Randomize"):
                st.session_state.exam_seed = _new_seed()
                exam_state.save(conn)
                st.rerun()
        if st.button("Start the 4-hour exam", type="primary"):
            # Any exam already in progress is replaced, deliberately and without
            # asking. The button says what it does.
            st.session_state.exam_seed = int(seed_in)
            st.session_state.paper = _build_paper(bank)
            st.session_state.exam_started = True
            st.session_state.exam_start_ts = time.time()
            st.session_state.exam_answers = {}
            st.session_state.exam_idx = 0
            exam_state.save(conn)
            st.rerun()
        # Nothing in progress, so make sure a finished or abandoned exam cannot
        # be resumed by a later refresh.
        exam_state.save(conn)
        return

    paper = st.session_state.get("paper", [])
    if not paper:
        st.session_state.exam_started = False
        exam_state.save(conn)
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
        exam_state.save(conn)

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
        # Same tick as in practice, so marking options feels the same on paper.
        marked_key = "exam_marked_" + q["id"]
        if set(opts) - set(st.session_state.get(marked_key, [])):
            celebrate.play("tap", st.session_state.get("sound_on", True))
        st.session_state[marked_key] = list(opts)
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
            exam_state.save(conn)
            st.rerun()
    with c2:
        if st.button("Next", disabled=idx >= len(paper) - 1,
                     use_container_width=True):
            st.session_state.exam_idx = idx + 1
            exam_state.save(conn)
            st.rerun()
    with c3:
        if st.button("Finish and grade", type="primary", use_container_width=True):
            _grade(bank, conn, paper, answers)
            st.session_state.exam_started = False
            # Handed in: clear it, so a refresh cannot bring the paper back.
            exam_state.save(conn)
            st.rerun()

    # Last, so it captures the MC ticks and the WA text typed on this run. The
    # buttons above save before rerunning, because a rerun unwinds the script
    # and never reaches this line.
    exam_state.save(conn)


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
            ui.render_model_answer(q["answer"])
            if q.get("detail"):
                # Inline, because Streamlit does not allow nested expanders.
                st.markdown(
                    '<div class="sds-exwrap">'
                    '<div class="sds-exlabel">Longer explanation</div>'
                    '<div class="sds-model">%s</div></div>' % ui.md_inline(q["detail"]),
                    unsafe_allow_html=True,
                )
            st.markdown("**What the marker is looking for**")
            for item in q["rubric"]:
                st.markdown("- %s" % item["text"])
    if st.button("Clear result"):
        st.session_state.exam_result = None
        st.rerun()