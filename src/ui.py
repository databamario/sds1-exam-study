"""Shared Streamlit components and styling."""

from __future__ import annotations

import html
import zlib
from io import BytesIO

import streamlit as st
from PIL import Image

from . import loader
from . import celebrate
from .scoring import mc_feedback, score_mc

POINTS_PER_MC = 1.0


def inject_css() -> None:
    st.markdown(
        """
        <style>
          .block-container { max-width: 1000px; padding-top: 2rem; }

          /* The page is read in three registers and they must never blur into
             each other: the question is the loudest thing, the worked example
             or R code is clearly material beside it, and the answer is set
             apart in green. Every block sets its own colours so it stays
             readable in both the light and the dark Streamlit theme. */

          /* -- the question ---------------------------------------------- */
          .sds-card {
            border: 1px solid #dbe3ec; border-left: 5px solid #2f6f9f;
            border-radius: 10px; padding: 1rem 1.2rem; margin: 0.4rem 0 0.6rem;
            background:#ffffff; color:#0f172a;
            box-shadow: 0 1px 2px rgba(15,23,42,.05);
          }
          .sds-qid {
            font-size: .74rem; color:#64748b; letter-spacing:.06em;
            text-transform:uppercase; margin-bottom:.35rem;
          }
          .sds-stem {
            font-size: 1.16rem; line-height:1.6; font-weight:600; color:#0f172a;
          }
          /* The stem is a block, so a code span inside it still needs to read
             as code rather than as prose. */
          .sds-stem code {
            background:#eef2f7; border:1px solid #dbe3ec; border-radius:4px;
            padding:0 .3em; font-size:.92em;
            font-family:ui-monospace,Menlo,Consolas,monospace;
          }

          /* -- material: R code, examples, figures ----------------------- */
          .sds-exwrap { margin:.5rem 0 .6rem; }
          .sds-exlabel {
            font-size:.7rem; letter-spacing:.07em; text-transform:uppercase;
            color:#92400e; margin-bottom:.2rem;
          }
          .sds-code {
            background:#0f172a; color:#e2e8f0; padding:.8rem 1rem;
            border-left:5px solid #f59e0b; border-radius:8px;
            font-family:ui-monospace,Menlo,Consolas,monospace;
            font-size:.9rem; line-height:1.5; overflow-x:auto; white-space:pre;
          }
          .sds-fig { text-align:center; margin:.5rem 0 .2rem; }
          .sds-figcap { font-size:.74rem; color:#94a3b8; margin-top:.15rem; }
          div[data-testid="stImage"] img {
            border:1px solid #dbe3ec; border-radius:8px; background:#ffffff;
          }

          /* -- options --------------------------------------------------- */
          div[data-testid="stCheckbox"] label {
            font-size:1rem; line-height:1.5; padding:.2rem 0;
          }
          /* After grading the options become a static review list, because a
             disabled checkbox cannot show which one was actually right. */
          .sds-optrow {
            display:flex; align-items:flex-start; gap:.6rem;
            padding:.45rem .6rem; margin:.3rem 0; border-radius:8px;
            border:1px solid #e2e8f0; background:#fbfcfe; color:#1f2933;
            font-size:1rem; line-height:1.5;
          }
          .sds-optrow .sds-badge {
            flex:0 0 1.55rem; height:1.55rem; margin-top:.05rem;
            display:flex; align-items:center; justify-content:center;
            border-radius:50%; background:#e2e8f0; color:#334155;
            font-size:.82rem; font-weight:700;
          }
          .sds-optrow.hit     { border-color:#86efac; background:#f0fdf4; color:#14532d; }
          .sds-optrow.hit .sds-badge     { background:#22c55e; color:#ffffff; }
          .sds-optrow.missed  { border-color:#86efac; background:#f0fdf4; color:#14532d; }
          .sds-optrow.missed .sds-badge  { background:#22c55e; color:#ffffff; }
          .sds-optrow.over    { border-color:#fca5a5; background:#fef2f2; color:#7f1d1d; }
          .sds-optrow.over .sds-badge    { background:#dc2626; color:#ffffff; }
          .sds-optrow.dim     { opacity:.6; }
          .sds-opttag {
            display:block; font-size:.72rem; font-weight:700;
            letter-spacing:.05em; text-transform:uppercase; margin-top:.1rem;
          }
          .sds-optrow.over .sds-opttag { color:#b91c1c; }
          .sds-optrow.missed .sds-opttag { color:#15803d; }

          /* -- the answer ------------------------------------------------ */
          .sds-model {
            border:1px solid #86efac; border-left:5px solid #22c55e;
            border-radius:8px; padding:.75rem .95rem; margin:.4rem 0;
            background:#f0fdf4; color:#14532d; line-height:1.55;
          }
          .sds-model .sds-model-label {
            font-size:.7rem; letter-spacing:.07em; text-transform:uppercase;
            color:#15803d; margin-bottom:.3rem; font-weight:700;
          }
          .sds-model code {
            background:#dcfce7; border:1px solid #86efac; border-radius:4px;
            padding:0 .25em; font-size:.9em;
            font-family:ui-monospace,Menlo,Consolas,monospace;
          }

          /* -- verdict, hints, chrome ------------------------------------- */
          .sds-verdict { border-radius:8px; padding:.7rem .9rem; margin:.4rem 0;
                         line-height:1.55; font-size:1rem; }
          .sds-verdict.ok   { background:#f0fdf4; border:1px solid #86efac; color:#14532d; }
          .sds-verdict.half { background:#fffbeb; border:1px solid #fcd34d; color:#78350f; }
          .sds-verdict.bad  { background:#fef2f2; border:1px solid #fca5a5; color:#7f1d1d; }
          .sds-verdict b    { font-size:1.05rem; }
          .sds-hint {
            font-size:.85rem; color:#92400e; background:#fffbeb;
            border:1px solid #fde68a; border-radius:8px;
            padding:.5rem .75rem; margin:.4rem 0;
          }
          .sds-src { font-size:.75rem; color:#94a3b8; }

          /* -- driving-test header ---------------------------------------- */
          .sds-crumb {
            display:flex; align-items:center; gap:.6rem; flex-wrap:wrap;
            font-size:.8rem; color:#94a3b8; margin-bottom:.2rem;
          }
          .sds-streak {
            display:inline-block; padding:.05rem .5rem; border-radius:999px;
            background:#fef3c7; border:1px solid #fcd34d; color:#92400e;
            font-weight:700; font-size:.75rem;
          }
          .sds-streak.hot {
            background:#fee2e2; border-color:#fca5a5; color:#9f1239;
          }
          .sdots { display:flex; flex-wrap:wrap; gap:5px; margin:.35rem 0 .5rem; }
          .sdot {
            width:11px; height:11px; border-radius:50%;
            background:#e2e8f0; border:1px solid #cbd5e1;
          }
          .sdot.ok   { background:#22c55e; border-color:#22c55e; }
          .sdot.half { background:#f0a92e; border-color:#f0a92e; }
          .sdot.bad  { background:#dc2626; border-color:#dc2626; }
          .sdot.now  { outline:2px solid #2f6f9f; outline-offset:2px; }
          .sds-kbd {
            display:inline-block; background:#eef2f7; border:1px solid #cbd5e1;
            border-radius:5px; padding:0 .35rem; font-size:.8rem;
          }
          div[data-testid="stMetricValue"] { font-size:1.5rem; }

          /* The blocks above are light on purpose so they read in both themes,
             but a pure white card on a dark page is harsh. Streamlit follows
             the system colour scheme by default, so the same blocks get dark
             surfaces here. */
          @media (prefers-color-scheme: dark) {
            .sds-card {
              background:#111827; border-color:#1f2937; color:#e5e7eb;
              box-shadow:none;
            }
            .sds-stem { color:#f1f5f9; }
            .sds-qid { color:#94a3b8; }
            .sds-stem code { background:#1e293b; border-color:#334155; color:#e2e8f0; }

            .sds-optrow { background:#111827; border-color:#1f2937; color:#e5e7eb; }
            .sds-optrow .sds-badge { background:#334155; color:#e2e8f0; }
            .sds-optrow.hit, .sds-optrow.missed {
              background:#052e16; border-color:#166534; color:#bbf7d0;
            }
            .sds-optrow.hit .sds-badge, .sds-optrow.missed .sds-badge {
              background:#22c55e; color:#052e16;
            }
            .sds-optrow.missed .sds-opttag { color:#4ade80; }
            .sds-optrow.over { background:#2a0f0f; border-color:#7f1d1d; color:#fecaca; }
            .sds-optrow.over .sds-badge { background:#dc2626; color:#ffffff; }
            .sds-optrow.over .sds-opttag { color:#fca5a5; }

            .sds-model { background:#052e16; border-color:#166534; color:#bbf7d0; }
            .sds-model .sds-model-label { color:#4ade80; }
            .sds-model code { background:#14532d; border-color:#166534; color:#d1fae5; }

            .sds-verdict.ok   { background:#052e16; border-color:#166534; color:#bbf7d0; }
            .sds-verdict.half { background:#2a1a05; border-color:#78350f; color:#fde68a; }
            .sds-verdict.bad  { background:#2a0f0f; border-color:#7f1d1d; color:#fecaca; }

            .sds-streak { background:#422006; border-color:#78350f; color:#fcd34d; }
            .sds-streak.hot { background:#450a0a; border-color:#7f1d1d; color:#fca5a5; }
            .sds-figcap { color:#64748b; }
            div[data-testid="stImage"] img { border-color:#1f2937; }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def esc(text: str) -> str:
    return html.escape(str(text))


def md_inline(text: str) -> str:
    """Markdown that has already been escaped, so emphasis and code still work."""
    return esc(text).replace("\n", "<br>")


def render_code(code: str, label: str = "R code") -> None:
    st.markdown(
        '<div class="sds-exwrap"><div class="sds-exlabel">%s</div>'
        '<div class="sds-code">%s</div></div>'
        % (esc(label), esc(code)),
        unsafe_allow_html=True,
    )


def render_model_answer(text: str, label: str = "Model answer") -> None:
    st.markdown(
        '<div class="sds-model"><div class="sds-model-label">%s</div>%s</div>'
        % (esc(label), md_inline(text)),
        unsafe_allow_html=True,
    )


def lecture_label(lec: int) -> str:
    return "Lecture %d - %s" % (lec, loader.LECTURES[lec])


def render_stem(q: dict, show_source: bool = True) -> None:
    st.markdown(
        '<div class="sds-card"><div class="sds-qid">%s &middot; %d pt</div>'
        '<div class="sds-stem">%s</div></div>'
        % (esc(q["id"]), q["points"], md_inline(q["stem"])),
        unsafe_allow_html=True,
    )
    render_figure(q)
    if q.get("code"):
        render_code(q["code"])
    if q.get("bullets"):
        st.markdown('<div class="sds-exwrap">%s</div>'
                    % "".join("<div>- %s</div>" % md_inline(b) for b in q["bullets"]),
                    unsafe_allow_html=True)
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
    st.markdown(
        '<div class="sds-figcap">Figure &mdash; read the axes and the shape '
        "before the options</div>",
        unsafe_allow_html=True,
    )


def render_mc_review(q: dict, selected: list[str], context: str = "practice") -> None:
    """Show the options as a static, colour-coded list.

    A disabled checkbox cannot show which option was the right one, so after
    answering the options stop being controls and become a marked-up list: green
    for a correct option, red for one that was marked wrongly, and a tag saying
    in words what went wrong.

    ``context="key"`` is for the answer key, where nothing has been attempted:
    there the correct options are simply highlighted, with no "you missed this
    one" tag that would mean nothing.
    """
    chosen = set(selected)
    right = set(q["correct"])
    parts = []
    for label, text in q["options"].items():
        is_right = label in right
        is_chosen = label in chosen
        if context == "key":
            cls, tag = ("hit", "") if is_right else ("dim", "")
        elif is_right and is_chosen:
            cls, tag = "hit", "correct"
        elif is_right:
            cls, tag = "missed", "you missed this one"
        elif is_chosen:
            cls, tag = "over", "you marked this one wrongly"
        else:
            cls, tag = "dim", ""
        parts.append(
            '<div class="sds-optrow %s"><span class="sds-badge">%s</span>'
            "<span><b>%s</b> %s%s</span></div>"
            % (cls, esc(label.upper()), esc(label), md_inline(text),
               '<span class="sds-opttag">%s</span>' % esc(tag) if tag else "")
        )
    st.markdown("".join(parts), unsafe_allow_html=True)


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
    """Render checkbox options and return the labels marked.

    A short tick plays the first time an option is marked, which is the only
    feedback that lands while the student is still deciding, so it is the one
    worth having. It is deliberately quiet: this can fire several times a
    question.
    """
    chosen = []
    for label, text in q["options"].items():
        if st.checkbox(
            "%s)  %s" % (label, text),
            key="%s_%s_%s" % (key_prefix, q["id"], label),
            disabled=disabled,
        ):
            chosen.append(label)

    mark_key = key_prefix + "_marked"
    already = set(st.session_state.get(mark_key, []))
    if set(chosen) - already:
        celebrate.play("tap", st.session_state.get("sound_on", True))
    st.session_state[mark_key] = list(chosen)
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
    st.markdown("**How each option went**")
    render_mc_review(q, selected)
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
    streak = celebrate.streak_upto(queue, history, done, i) if answered else 0
    best = st.session_state.setdefault(key + "_best_streak", 0)
    if streak > best:
        st.session_state[key + "_best_streak"] = best = streak

    crumb = "&middot;".join(
        [("Round 2" if in_retry else "Round 1"),
         "Question %d of %d" % (i + 1, len(queue)),
         "%.1f / %d pt" % (scored, maximum)]
    )
    if best:
        hot = " hot" if best >= celebrate.CELEBRATE_AT else ""
        crumb += ('&nbsp;&nbsp;<span class="sds-streak%s">streak %d'
                  '<span style="font-weight:400"> &middot; best %d</span>'
                  "</span>" % (hot, streak, best))
    st.markdown('<div class="sds-crumb">%s</div>' % crumb, unsafe_allow_html=True)
    progress_dots(queue, {k: {"score": v} for k, v in history.items()}, i)

    # The stem comes before the figure, because the questions refer to "the
    # plot below" the same way the real exam does.
    st.markdown(
        '<div class="sds-card"><div class="sds-qid">%s &middot; %d pt</div>'
        '<div class="sds-stem">%s</div></div>'
        % (esc(q["id"]), q["points"], md_inline(q["stem"])),
        unsafe_allow_html=True,
    )
    render_figure(q)
    if q.get("code"):
        render_code(q["code"])
    if q.get("bullets"):
        st.markdown('<div class="sds-exwrap">%s</div>'
                    % "".join("<div>- %s</div>" % md_inline(b) for b in q["bullets"]),
                    unsafe_allow_html=True)

    if q["type"] == loader.MC:
        # In round 2 the options start unticked: the previous wrong selection
        # is still shown in the round-1 feedback, so a retry should be a fresh
        # attempt rather than a resubmit. WA keeps its draft, which is useful.
        opt_key = key + ("_retry_" if in_retry else "_")
        if not answered:
            # Once answered the controls are replaced by the colour-coded review
            # list, so the same five options are never listed twice on screen.
            chosen = mc_options_ui(q, opt_key)
            st.caption("Mark every correct option. There may be more than one.")
            if st.button("Check answer", key=key + "_check", type="primary"):
                st.session_state[key + "_done"][q["id"]] = {
                    "selected": list(chosen),
                    "score": score_mc(q["correct"], chosen),
                }
                st.rerun()
        else:
            render_mc_feedback(q, entry["selected"])
            _reward(q, entry["score"], streak, key, round_no)
            _record_once(conn, q, entry["score"], kind, key)
    else:
        _wa_body(q, kind, key, entry, answered, conn, streak)

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


def _wa_body(q, kind, key, entry, answered, conn, streak=0) -> None:
    """Written answer: type it, grade it blind, then look if you want to.

    The rubric chips come before the model answer on purpose. Previously the
    model answer appeared the moment the answer was revealed, which meant the
    chips underneath could be filled by reading it rather than by remembering
    what you wrote. Grading blind also mirrors the real thing, where nobody
    hands you the mark scheme.
    """
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
        st.caption("Write your answer, then mark yourself. The model answer stays "
                   "hidden until you say so.")
        if st.button("Mark my answer", key=key + "_reveal", type="primary"):
            st.session_state[key + "_done"][q["id"]] = {"selected": [], "score": 0.0}
            st.rerun()
        return

    n_el = sum(item["elements"] for item in q["rubric"])
    # Checkpoints worth more than one element get a suffix on the pill, so the
    # selection is matched back by position rather than by text.
    labels = [
        item["text"] if item["elements"] == 1
        else "%s  (%d parts)" % (item["text"], item["elements"])
        for item in q["rubric"]
    ]
    hits = st.pills(
        "Tick every point your answer covered",
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
                   "Tick anything above you did cover but have not yet, then "
                   "press Next to save the score.")
    _reward(q, score, streak, key, 1 if st.session_state.get(key + "_round", 1) == 1 else 2)

    peek = key + "_peeked_" + q["id"]
    if st.session_state.get(peek):
        render_model_answer(q["answer"])
        render_why(q.get("detail", ""), "Why? The longer explanation")
    else:
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("Show the model answer", key=key + "_peek"):
                st.session_state[peek] = True
                st.rerun()
        with c2:
            st.caption("Reading it is fine. It is just easier to mark yourself "
                       "honestly first.")
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


def _reward(q: dict, score: float, streak: int, key: str, round_no: int) -> None:
    """Sound, and confetti once the streak is long enough.

    Guarded on (question, round, score) so it fires once per attempt. Without
    the guard, walking back to a question you have already answered would replay
    the celebration, and every rerun is a fresh page.
    """
    sound_on = st.session_state.get("sound_on", True)
    seen = st.session_state.setdefault(key + "_rewarded", set())
    token = (q["id"], round_no, round(score, 3))
    if token in seen:
        return
    seen.add(token)

    full = score >= q["points"] - 1e-9
    if full and celebrate.should_celebrate(streak):
        # Deterministic per question and streak, so the same burst does not
        # change shape on every rerun.
        seed = zlib.crc32(("%s|%d" % (q["id"], streak)).encode()) % 100000
        celebrate.celebrate(min(streak - celebrate.CELEBRATE_AT + 1, 8), seed)
        celebrate.play("celebrate", sound_on)
    elif full:
        celebrate.play("correct", sound_on)
    elif score > 0:
        celebrate.play("tap", sound_on)
    else:
        celebrate.play("wrong", sound_on)


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