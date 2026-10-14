"""SDS1 exam study app - local Streamlit app.

Run with:  streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from src import loader, progress, ui
from src.views import mock_exam, practice, progress_view, review

st.set_page_config(
    page_title="SDS1 Exam Study",
    page_icon="📊",
    layout="centered",
)

ui.inject_css()


@st.cache_data(show_spinner=False)
def _bank_cached(_mtime):
    return loader.load_bank()


def load_bank():
    path = loader.QUESTIONS_PATH
    if not path.exists():
        st.error(
            "The question bank is missing (data/questions.json).\n\n"
            "Build it with:  python tools/build_bank.py"
        )
        st.stop()
    return _bank_cached(path.stat().st_mtime)


bank = load_bank()

st.title("Statistics and Data Science I - exam study")
n_mc = len(loader.of_type(bank, loader.MC))
n_wa = len(loader.of_type(bank, loader.WA))
st.caption(
    "Course 771A15 / 771A16 &middot; %d questions &middot; %d multiple-choice, "
    "%d written-answer &middot; final exam Fri 23 Oct 2026"
    % (len(bank), n_mc, n_wa)
)

conn = progress.connect()

PAGES = {
    "Home": "home",
    "Study MC": "practice.mc",
    "Study WA": "practice.wa",
    "Mock exam": "mock",
    "Answer key": "key",
    "Progress": "progress",
    "R coverage": "coverage",
}

with st.sidebar:
    st.markdown("### Sections")
    choice = st.radio("Go to", list(PAGES), label_visibility="collapsed")
    st.divider()
    st.caption(
        "MC: mark **all** correct options - there may be none, or more than one.\n\n"
        "WA: short answer, max 3 sentences. Partial credit is possible."
    )

target = PAGES[choice]

if target == "home":
    st.markdown(
        """
        ### How the real exam marks you

        **Multiple-choice (MC)** - mark *all* correct options. There may be none,
        or more than one. Each question is worth at most 1 point.

        | Your answer | Score | Why |
        |---|---|---|
        | all correct, nothing extra | **1.0** | no mistakes |
        | (0 correct options, nothing marked) | **1.0** | special case |
        | exactly one mistake | **0.5** | one correct missed, or one wrong marked |
        | two or more mistakes | **0.0** | |

        **Written-answer (WA)** - short and succinct, max 3 sentences unless
        stated otherwise. Partial credit for partial answers.

        **Calculations** - you are not asked to grind numbers. Give the formula
        with the values substituted, e.g. `Xbar = sum(x)/n = (1+2+3)/3`.
        """
    )
    st.markdown("### Suggested order")
    st.markdown(
        "1. **Study MC** and **Study WA** lecture by lecture - these are two "
        "different kinds of practice and worth doing separately.\n"
        "2. **R coverage** to see what the lectures taught and what is tested.\n"
        "3. **Mock exam** once you have worked through the lectures - it mirrors "
        "the real 41-point, 4-hour paper.\n"
        "4. **Answer key** to review, revise, and flag anything wrong."
    )
    if st.session_state.get("exam_result"):
        st.divider()
        mock_exam.render_result(bank)

elif target == "practice.mc":
    practice.mc_practice(bank, conn)
elif target == "practice.wa":
    practice.wa_practice(bank, conn)
elif target == "mock":
    mock_exam.mock_exam(bank, conn)
    if st.session_state.get("exam_result"):
        st.divider()
        mock_exam.render_result(bank)
elif target == "key":
    review.answer_key(bank)
elif target == "progress":
    progress_view.dashboard(bank, conn)
elif target == "coverage":
    review.r_coverage(bank)