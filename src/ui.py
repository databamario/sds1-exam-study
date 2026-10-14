"""Shared Streamlit components and styling."""

from __future__ import annotations

import html
from io import BytesIO

import streamlit as st
from PIL import Image

from . import loader
from .scoring import mc_feedback, score_mc

POINTS_PER_MC = 1.0


def inject_css() -> None:
    st.markdown(
        """
        <style>
          .block-container { max-width: 1000px; padding-top: 2rem; }
          /* Every custom block sets its own colours so it stays readable in
             both the light and the dark Streamlit theme. */
          .sds-card {
            border: 1px solid #e2e8f0; border-radius: 10px;
            padding: 0.9rem 1.1rem; margin: 0.5rem 0;
            background:#fbfcfe; color:#1f2933;
          }
          .sds-qid { font-size: 0.78rem; color:#64748b; letter-spacing:.02em; }
          .sds-stem { font-size: 1.02rem; line-height:1.55; color:#1f2933; }
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

          /* driving-test question header */
          .sds-crumb { font-size:0.8rem; color:#94a3b8; margin-bottom:.15rem; }
          .sdots { display:flex; flex-wrap:wrap; gap:5px; margin:.35rem 0 .1rem; }
          .sdot {
            width:11px; height:11px; border-radius:50%;
            background:#e2e8f0; border:1px solid #cbd5e1;
          }
          .sdot.ok   { background:#22a06b; border-color:#22a06b; }
          .sdot.half { background:#e0a33a; border-color:#e0a33a; }
          .sdot.bad  { background:#d64545; border-color:#d64545; }
          .sdot.now  { outline:2px solid #2f6f9f; outline-offset:2px; }
          .sds-fig { text-align:center; margin:.4rem 0 .2rem; }
          div[data-testid="stImage"] img {
            border:1px solid #e2e8f0; border-radius:8px; background:#ffffff;
          }
          .sds-verdict { border-radius:8px; padding:.55rem .8rem; margin:.3rem 0;
                         line-height:1.5; }
          .sds-verdict.ok   { background:#f0fdf4; border:1px solid #bbf7d0; color:#14532d; }
          .sds-verdict.half { background:#fffbeb; border:1px solid #fde68a; color:#78350f; }
          .sds-verdict.bad  { background:#fef2f2; border:1px solid #fecaca; color:#7f1d1d; }
          .sds-opt { padding:.15rem 0; }
          div[data-testid="stCheckbox"] label { font-size:1rem; }
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
    render_figure(q)
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


def dot_class(score: float, maximum: float) -> str:
    if maximum <= 0:
        return ""
    if score / maximum >= 1.0:
        return "ok"
    if score > 0:
        return "half"
    return "bad"


def render_figure(q: dict, max_height: int = 300, max_width: int = 680) -> None:
    """Draw the question's figure, if it has one.

    The bytes are read and handed to st.image rather than passing a path: a
    path makes Streamlit register the file in its media cache, and that entry
    is evicted between reruns, which shows up as a broken image. Inlining the
    bytes keeps the figure on screen every time.

    The size is capped so the question and its options stay on one screen - an
    uncapped figure pushes the stem below the fold.
    """
    name = q.get("image")
    if not name:
        return
    path = loader.IMAGES_DIR / (name + ".png")
    if not path.exists():
        return
    try:
        data = path.read_bytes()
        with Image.open(BytesIO(data)) as im:
            w, h = im.size
    except Exception:
        st.image(str(path))
        return
    width = min(max_width, int(max_height * w / h))
    st.image(data, width=width)


def progress_dots(pool: list[dict], done: dict, current: int) -> None:
    """One dot per question, coloured by result, ringed on the current one."""
    parts = ['<div class="sdots">']
    for idx, q in enumerate(pool):
        cls = "sdot"
        entry = done.get(q["id"])
        if entry is not None:
            cls += " " + dot_class(entry["score"], q["points"])
        if idx == current:
            cls += " now"
        parts.append('<span class="%s"></span>' % cls)
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def render_verdict(score: float, maximum: float, headline: str, body: str) -> None:
    cls = dot_class(score, maximum)
    st.markdown(
        '<div class="sds-verdict %s"><b>%s</b><br>%s</div>'
        % (cls, esc(headline), body),
        unsafe_allow_html=True,
    )


def render_why(text: str, label: str = "Why?") -> None:
    if text:
        with st.expander(label):
            st.markdown(text)


def mc_options_ui(q: dict, key_prefix: str, disabled: bool = False) -> list[str]:
    """Render checkbox options in one column. Returns the labels marked."""
    chosen = []
    for label, text in q["options"].items():
        if st.checkbox(
            "%s)  %s" % (label, text),
            key="%s_%s_%s" % (key_prefix, q["id"], label),
            disabled=disabled,
        ):
            chosen.append(label)
    return chosen


def render_mc_feedback(q: dict, selected: list[str]) -> dict:
    """Show the graded result for one MC answer."""
    fb = mc_feedback(q["correct"], selected)
    verdict = dot_class(fb["score"], POINTS_PER_MC)
    mark = "Correct" if fb["score"] >= 1.0 else ("Partly right" if fb["score"] > 0
                                                else "Not correct")
    body = esc(fb["explanation"])
    if fb["missed"]:
        body += "<br><b>You missed:</b> %s" % esc(", ".join(fb["missed"]))
    if fb["extra"]:
        body += "<br><b>You marked extra:</b> %s" % esc(", ".join(fb["extra"]))
    render_verdict(fb["score"], POINTS_PER_MC,
                   "%s  \u00b7  %.1f / 1.0 pt" % (mark, fb["score"]), body)
    correct_txt = ", ".join(
        "%s) %s" % (k, q["options"][k]) for k in q["correct"]
    )
    st.markdown("**Correct answer:** %s" % correct_txt)
    render_why(q["explanation"])
    return fb


def question_loop(pool: list[dict], kind: str, conn=None) -> None:
    """One question at a time, same mechanics for MC and WA.

    The loop is: show the question, commit an answer, see the verdict and the
    short explanation, then advance. Anything not answered at full marks is
    queued to come round again, and keeps coming back until it is.

    Two pieces of state do the work. ``done`` holds the current attempt, which
    is what decides whether the question is still open. ``history`` holds the
    best score per question and drives the dots and the end-of-set summary, so
    a re-attempt can improve on the first try without losing the earlier mark.
    """
    key = "loop_%s" % kind
    sig = tuple(q["id"] for q in pool)
    for name, default in (("_sig", None), ("_round", 1), ("_idx", 0),
                          ("_done", {}), ("_history", {}), ("_retry", []),
                          ("_recorded", set())):
        st.session_state.setdefault(key + name, default)

    if st.session_state[key + "_sig"] != sig:
        st.session_state[key + "_sig"] = sig
        st.session_state[key + "_round"] = 1
        st.session_state[key + "_idx"] = 0
        st.session_state[key + "_done"] = {}
        st.session_state[key + "_history"] = {}
        st.session_state[key + "_retry"] = []
        st.session_state[key + "_recorded"] = set()

    if not pool:
        st.info("No questions for this selection.")
        return

    round_no = st.session_state[key + "_round"]
    idx = st.session_state[key + "_idx"]
    retry = st.session_state[key + "_retry"]
    done = st.session_state[key + "_done"]
    history = st.session_state[key + "_history"]

    # Round 1 walks the whole pool. Round 2 walks only what was queued, and
    # only starts once round 1 has actually been walked to the end - queueing a
    # question must not cut the rest of the first pass short.
    queue = list(pool) if round_no == 1 else [q for q in pool if q["id"] in retry]

    if idx >= len(queue):
        if round_no == 1 and retry:
            st.session_state[key + "_round"] = 2
            st.session_state[key + "_idx"] = 0
            # Make the queued questions answerable again; history keeps the mark.
            for qid in retry:
                done.pop(qid, None)
            st.rerun()
        _loop_summary(pool, kind)
        if st.button("Practise these again", key=key + "_again",
                     type="primary"):
            st.session_state[key + "_sig"] = None
            st.rerun()
        return

    i = idx
    q = queue[i]
    in_retry = round_no == 2
    entry = done.get(q["id"])
    answered = entry is not None

    scored = sum(history.values())
    maximum = sum(x["points"] for x in pool)
    crumbs = "&middot;".join(
        [("Round 2" if in_retry else "Round 1"),
         "Question %d of %d" % (i + 1, len(queue)),
         "%.1f / %d pt" % (scored, maximum)]
    )
    st.markdown('<div class="sds-crumb">%s</div>' % crumbs, unsafe_allow_html=True)
    progress_dots(queue, {k: {"score": v} for k, v in history.items()}, i)

    # The stem comes before the figure, because the questions refer to "the
    # plot below" the same way the real exam does.
    st.markdown(
        '<div class="sds-card"><div class="sds-qid">%s &middot; %d pt</div>'
        '<div class="sds-stem">%s</div></div>'
        % (esc(q["id"]), q["points"],
           esc(q["stem"]).replace("\n", "<br>")),
        unsafe_allow_html=True,
    )
    render_figure(q)
    if q.get("code"):
        render_code(q["code"])
    if q.get("bullets"):
        for b in q["bullets"]:
            st.markdown("- %s" % b)

    if q["type"] == loader.MC:
        # In round 2 the options start unticked: the previous wrong selection
        # is still shown in the round-1 feedback, so a retry should be a fresh
        # attempt rather than a resubmit. WA keeps its draft, which is useful.
        opt_key = key + ("_retry_" if in_retry else "_")
        chosen = mc_options_ui(q, opt_key, disabled=answered)
        if not answered:
            st.caption("Mark every correct option. There may be more than one.")
            if st.button("Check answer", key=key + "_check", type="primary"):
                st.session_state[key + "_done"][q["id"]] = {
                    "selected": list(chosen),
                    "score": score_mc(q["correct"], chosen),
                }
                st.rerun()
        else:
            render_mc_feedback(q, entry["selected"])
            _record_once(conn, q, entry["score"], kind, key)
    else:
        _wa_body(q, kind, key, entry, answered, conn)

    left, mid, right = st.columns([1, 1, 1])
    if answered:
        with left:
            if st.button("Next", key=key + "_next", type="primary",
                         use_container_width=True):
                _advance(q, key, queue, i)
                st.rerun()
        with right:
            if st.button("Back", key=key + "_back", disabled=i == 0,
                         use_container_width=True):
                st.session_state[key + "_idx"] = i - 1
                st.rerun()
    else:
        with mid:
            if st.button("Skip", key=key + "_skip", use_container_width=True):
                # A skipped question is an unattempted one, so it counts as 0
                # and is queued to come round again rather than being lost.
                st.session_state[key + "_done"].setdefault(
                    q["id"], {"selected": [], "score": 0.0})
                _advance(q, key, queue, i)
                st.rerun()


def _wa_body(q, kind, key, entry, answered, conn) -> None:
    """Written answer: type it, reveal, then tap the points you covered."""
    draft_key = "wa_draft_%s" % q["id"]
    st.session_state.setdefault(draft_key, "")
    answer = st.text_area(
        "Your answer (max 3 sentences)",
        height=130,
        disabled=answered,
        key=key + "_input_" + q["id"],
        value=st.session_state[draft_key],
    )
    st.session_state[draft_key] = answer

    if not answered:
        st.caption("Write your answer, then reveal the model answer to check it.")
        if st.button("Reveal", key=key + "_reveal", type="primary"):
            st.session_state[key + "_done"][q["id"]] = {"selected": [], "score": 0.0}
            st.rerun()
        return

    st.markdown("**Model answer**")
    st.markdown(q["answer"])
    render_why(q.get("detail", ""), "Why? The longer explanation")

    n_el = sum(item["elements"] for item in q["rubric"])
    # Checkpoints worth more than one element get a suffix on the pill, so the
    # selection is matched back by position rather than by text.
    labels = [
        item["text"] if item["elements"] == 1
        else "%s  (%d parts)" % (item["text"], item["elements"])
        for item in q["rubric"]
    ]
    hits = st.pills(
        "Tap every point your answer covered",
        labels,
        selection_mode="multi",
        key=key + "_chips_" + q["id"],
    ) or []
    chosen = {labels.index(h) for h in hits if h in labels}
    earned = sum(q["rubric"][i]["elements"] for i in chosen)
    score = q["points"] * (earned / n_el) if n_el else 0.0
    st.session_state[key + "_done"][q["id"]]["score"] = score

    verdict = dot_class(score, q["points"])
    render_verdict(score, q["points"],
                   "%.1f / %d pt  \u00b7  %d of %d points covered"
                   % (score, q["points"], earned, n_el),
                   "Tap any point above you did cover but have not yet, then "
                   "press Next to save the score.")
    _record_once(conn, q, score, kind, key)


def _record_once(conn, q, score, kind, key) -> None:
    if conn is None:
        return
    recorded = st.session_state[key + "_recorded"]
    if q["id"] in recorded:
        return
    from . import progress
    progress.record(conn, q, "%s practice" % kind, score, q["points"])
    recorded.add(q["id"])


def _advance(q, key, queue, i) -> None:
    """Move on, queueing anything not answered at full marks for round 2."""
    done = st.session_state[key + "_done"]
    history = st.session_state[key + "_history"]
    retry = st.session_state[key + "_retry"]
    entry = done.get(q["id"])
    score = entry["score"] if entry else 0.0
    history[q["id"]] = max(history.get(q["id"], 0.0), score)
    if history[q["id"]] < q["points"] - 1e-9:
        if q["id"] not in retry:
            retry.append(q["id"])
    elif q["id"] in retry:
        retry.remove(q["id"])
    st.session_state[key + "_idx"] = i + 1


def _loop_summary(pool: list[dict], kind: str) -> None:
    history = st.session_state.get("loop_%s_history" % kind, {})
    if not history:
        return
    scored = sum(history.values())
    maximum = sum(q["points"] for q in pool)
    full = sum(1 for q in pool
               if history.get(q["id"], 0.0) >= q["points"] - 1e-9)
    st.markdown("---")
    st.markdown("### Set complete")
    c1, c2, c3 = st.columns(3)
    c1.metric("Score", "%.1f / %d" % (scored, maximum))
    c2.metric("Full marks", "%d / %d" % (full, len(pool)))
    c3.metric("Seen", "%d" % len(history))
    if full < len(pool):
        st.caption("%d question(s) still to master - they came back round "
                   "rather than being dropped." % (len(pool) - full))


def _record(conn, q: dict, score: float) -> None:
    from . import progress
    progress.record(conn, q, "MC practice", score, POINTS_PER_MC)