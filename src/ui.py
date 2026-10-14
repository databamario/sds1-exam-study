"""Shared Streamlit components and styling."""

from __future__ import annotations

import html

import streamlit as st

from . import loader
from .scoring import mc_feedback, score_mc

POINTS_PER_MC = 1.0


def inject_css() -> None:
    st.markdown(
        """
        <style>
          .block-container { max-width: 1000px; padding-top: 2rem; }
          .sds-card {
            border: 1px solid #e2e8f0; border-radius: 10px;
            padding: 0.9rem 1.1rem; margin: 0.5rem 0; background:#fbfcfe;
          }
          .sds-qid { font-size: 0.78rem; color:#64748b; letter-spacing:.02em; }
          .sds-stem { font-size: 1.02rem; line-height:1.55; }
          .sds-hint {
            font-size:0.85rem; color:#92400e; background:#fffbeb;
            border:1px solid #fde68a; border-radius:8px;
            padding:.5rem .75rem; margin:.4rem 0;
          }
          .sds-src { font-size:0.75rem; color:#94a3b8; }
          .sds-score { font-weight:600; }
          .sds-ok   { color:#15803d; }
          .sds-half { color:#b45309; }
          .sds-bad  { color:#b91c1c; }
          .sds-code {
            background:#0f172a; color:#e2e8f0; padding:.7rem .9rem;
            border-radius:8px; font-family:ui-monospace,Menlo,Consolas,monospace;
            font-size:0.86rem; overflow-x:auto; white-space:pre;
          }
          .sds-kbd {
            display:inline-block; background:#eef2f7; border:1px solid #cbd5e1;
            border-radius:5px; padding:0 .35rem; font-size:0.8rem;
          }
          div[data-testid="stMetricValue"] { font-size:1.5rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def esc(text: str) -> str:
    return html.escape(str(text))


def render_code(code: str) -> None:
    st.markdown('<div class="sds-code">%s</div>' % esc(code), unsafe_allow_html=True)


def lecture_label(lec: int) -> str:
    return "Lecture %d - %s" % (lec, loader.LECTURES[lec])


def render_stem(q: dict, show_source: bool = True) -> None:
    st.markdown(
        '<div class="sds-card"><div class="sds-qid">%s &middot; %d pt</div>'
        '<div class="sds-stem">%s</div></div>'
        % (esc(q["id"]), q["points"], esc(q["stem"]).replace("\n", "<br>")),
        unsafe_allow_html=True,
    )
    if q.get("code"):
        render_code(q["code"])
    if q.get("bullets"):
        for b in q["bullets"]:
            st.markdown("- %s" % b)
    if show_source:
        src = q["source"]
        st.markdown(
            '<div class="sds-src">source: %s, %s</div>'
            % (esc(src["pdf"]), esc(src["slide"])),
            unsafe_allow_html=True,
        )


def zero_correct_notice(q: dict) -> None:
    if q["type"] == loader.MC and q.get("n_correct") == 0:
        st.markdown(
            '<div class="sds-hint"><b>Careful.</b> This question has <b>0 correct '
            "options</b>. Leaving everything unmarked scores the full 1 point.</div>",
            unsafe_allow_html=True,
        )


def score_colour(score: float, maximum: float) -> str:
    if maximum <= 0:
        return "sds-score"
    ratio = score / maximum
    if ratio >= 1.0:
        return "sds-score sds-ok"
    if ratio > 0:
        return "sds-score sds-half"
    return "sds-score sds-bad"


def render_mc_feedback(q: dict, selected: list[str]) -> dict:
    """Show the graded result for one MC answer."""
    fb = mc_feedback(q["correct"], selected)
    cls = score_colour(fb["score"], POINTS_PER_MC)
    st.markdown(
        '<div class="sds-card"><span class="%s">%.1f / 1.0 pt</span> &nbsp; %s</div>'
        % (cls, fb["score"], esc(fb["explanation"])),
        unsafe_allow_html=True,
    )
    if fb["correct"]:
        correct_txt = ", ".join(
            "%s) %s" % (k, q["options"][k]) for k in q["correct"]
        )
        st.success("Correct option(s): %s" % correct_txt)
    else:
        st.info(
            "There are no correct options here - the full point comes from "
            "marking nothing."
        )
    st.markdown("**Why:** %s" % q["explanation"])
    return fb


def mc_options_ui(q: dict, key_prefix: str, disabled: bool = False) -> list[str]:
    """Render checkbox options. Returns the labels the student marked."""
    chosen = []
    cols = st.columns(min(2, max(1, len(q["options"]))))
    n = len(q["options"])
    per_col = (n + len(cols) - 1) // len(cols)
    for idx, (label, text) in enumerate(q["options"].items()):
        col = cols[min(idx // per_col, len(cols) - 1)]
        with col:
            if st.checkbox("%s) %s" % (label, text),
                           key="%s_%s_%s" % (key_prefix, q["id"], label),
                           disabled=disabled):
                chosen.append(label)
    return chosen


def grade_mc_session(qs: list[dict], conn=None) -> None:
    """One-at-a-time MC practice loop with inline feedback."""
    st.session_state.setdefault("mc_idx", 0)
    st.session_state.setdefault("mc_done", {})
    st.session_state.setdefault("mc_recorded", set())
    st.session_state.setdefault("mc_key", None)

    if st.session_state.mc_key != tuple(q["id"] for q in qs):
        st.session_state.mc_key = tuple(q["id"] for q in qs)
        st.session_state.mc_idx = 0
        st.session_state.mc_done = {}

    if not qs:
        st.info("No questions for this selection yet.")
        return

    i = st.session_state.mc_idx
    q = qs[i]
    st.caption("Question %d of %d" % (i + 1, len(qs)))
    render_stem(q)
    zero_correct_notice(q)
    st.markdown("**Mark ALL correct options.** There may be none, or more than one.")

    answered = q["id"] in st.session_state.mc_done
    chosen = mc_options_ui(q, "mc", disabled=answered)

    if answered:
        fb = render_mc_feedback(q, st.session_state.mc_done[q["id"]])
        if conn is not None and q["id"] not in st.session_state.mc_recorded:
            _record(conn, q, fb["score"])
            st.session_state.mc_recorded.add(q["id"])

    left, right = st.columns(2)
    if answered:
        with left:
            if st.button("Next question", type="primary", use_container_width=True):
                st.session_state.mc_idx = (i + 1) % len(qs)
                st.rerun()
        with right:
            if st.button("Back", disabled=i == 0, use_container_width=True):
                st.session_state.mc_idx -= 1
                st.rerun()
    else:
        with left:
            if st.button("Check answer", type="primary", use_container_width=True):
                st.session_state.mc_done[q["id"]] = list(chosen)
                st.rerun()
        with right:
            if st.button("Skip", use_container_width=True):
                st.session_state.mc_idx = (i + 1) % len(qs)
                st.rerun()


def _record(conn, q: dict, score: float) -> None:
    from . import progress
    progress.record(conn, q, "MC practice", score, POINTS_PER_MC)


def render_wa_key(q: dict, show_answer: bool = True) -> None:
    if not show_answer:
        return
    st.markdown("**Model answer**")
    st.markdown(q["answer"])
    st.markdown("**What the marker is looking for**")
    for item in q["rubric"]:
        st.markdown("- %s" % item["text"])