# SDS1 Exam Study App

A practice app for the **Statistics and Data Science I (771A15 / 771A16)** final exam.

**200 questions** — 130 multiple-choice (MC) and 70 written-answer (WA) — built from all
9 lectures, with the *exact* multiple-choice marking rules from the official exam paper.

> Everything runs locally on your own machine. Nothing is uploaded, nothing is tracked,
> no account needed. Your progress is saved to a local file you can delete any time.

---

## Quick start

You need [Python](https://www.python.org/downloads/) 3.9 or newer. Check with `python --version`.

**macOS / Linux / Git Bash on Windows**

```bash
git clone https://github.com/databamario/sds1-exam-study.git
cd sds1-exam-study
python -m venv .venv
source .venv/bin/activate        # Windows Git Bash:  source .venv/Scripts/activate
pip install -r requirements.txt
streamlit run app.py
```

**Windows (PowerShell or Command Prompt)**

```bash
git clone https://github.com/databamario/sds1-exam-study.git
cd sds1-exam-study
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Your browser opens automatically at <http://localhost:8501>. If it does not, copy that
address into your browser. To stop the app press `Ctrl + C` in the terminal.

### One-click alternative

After the first install, just run **`start.bat`** (Windows) or **`./start.sh`** (macOS/Linux).

---

## How the exam marks you

The app reproduces the real grading scheme exactly.

### Multiple-choice (MC)

Mark **all** correct options — *there may be none, or more than one*. Each question is
worth at most 1 point.

| Your answer | Score | Why |
|---|---|---|
| All correct marked, nothing extra marked | **1.0** | no mistakes |
| 0 correct options, nothing marked | **1.0** | special case in the instructions |
| Exactly one mistake | **0.5** | one correct option missed, **or** one incorrect option marked |
| Two or more mistakes | **0.0** | |

> ⚠️ **Watch out.** 5 of the 130 MC questions have **zero correct options**. In those,
> marking *nothing* earns the full point. The app flags them in yellow before you answer.

### Written-answer (WA)

Short and succinct — **max 3 sentences** unless the question says otherwise. Partial
credit is possible for partial answers, so the app gives you a checklist after you
write your answer and lets you score yourself point by point.

You do **not** need to grind through calculations. The exam says: *show how you would
solve it — give the formula with the values substituted.* For example, write

```
Xbar = sum(x)/n = (1+2+3)/3
```

and stop there. Doing the final arithmetic is optional and earns nothing extra.

---

## What's in the app

| Section | What it does |
|---|---|
| **Home** | The marking rules and a suggested study order. |
| **Study MC** | Multiple-choice practice, lecture by lecture. Instant marking and explanation. |
| **Study WA** | Written-answer practice. Write your answer, then reveal the model answer and self-grade against the checklist. |
| **Mock exam** | A timed paper that mirrors the real one: **41 points, 4 hours**, mixed MC and WA. MC is marked automatically; WA you self-grade. Change the seed to get a different paper. |
| **Answer key** | Every question with answers, model answers, explanations and the source slide. Filter by lecture and type. **Flag anything you think is wrong** so it is easy to report. |
| **Progress** | Points earned per lecture, and which lectures you are weakest on. One-click reset. |
| **R coverage** | Every R function the lectures teach, and which questions test it. Use this to confirm nothing from the course was skipped. |

**MC and WA are separate study modes on purpose.** They are different kinds of practice:
MC trains careful reading and holding several facts at once; WA trains writing a correct
method under a 3-sentence limit. Practise them separately, then mix them in the mock exam.

---

## Question coverage

| # | Lecture | MC | WA | Total |
|---|---|---:|---:|---:|
| 1 | What is statistics? + R basics | 17 | 8 | 25 |
| 2 | Descriptive stats for categorical data + R fundamentals | 21 | 8 | 29 |
| 3 | Descriptive stats for continuous data + joins | 19 | 8 | 27 |
| 4 | Probability and sampling theory | 14 | 8 | 22 |
| 5 | Random variables and probability distributions | 13 | 8 | 21 |
| 6 | Statistical inference and hypothesis testing | 12 | 8 | 20 |
| 7 | Tests for means and proportions, confidence intervals | 13 | 8 | 21 |
| 8 | Correlation, ANOVA and chi-squared tests | 12 | 6 | 18 |
| 9 | Simulation-based inference (Monte Carlo, bootstrapping) | 9 | 8 | 17 |
| | **Total** | **130** | **70** | **200** |

Questions are weighted by how much material each lecture covers, not spread evenly. About
60% of all questions involve R code, R output or R tooling.

Every question records the lecture slide it came from, shown under the question and in the
answer key.

### Not covered, on purpose

**Linear regression is not included.** Lecture 8 states explicitly: *"More on correlation
and linear regression in SDS2!"* No lecture teaches it in this course, and the mock exam
never tested it. If your lecturer announces otherwise, this app will not have covered it.

---

## Where the answers come from

- **138 questions** written fresh from the lecture slides.
- **62 questions** adapted from the HT25 mock exam, reworded and re-tagged. They are
  marked `adapted_HT25` so you can see which are calibrated to a real paper.

Every R code snippet in the question bank is **executed in R** during validation, and the
numeric answers are checked against real R output. The scoring engine is regression-tested
against the marking table printed in the official exam instructions.

---

## Troubleshooting

**`python: command not found`** — install Python from <https://www.python.org/downloads/>
and tick *Add Python to PATH* during setup.

**`streamlit: command not found`** after activating the venv — run `pip install -r requirements.txt` again.

**Port 8501 already in use** — `streamlit run app.py --server.port 8502`.

**Activation fails on Windows** — try `.venv\Scripts\activate` in PowerShell, or run
`start.bat` which does not need activation.

**Want to start over** — Answer key → *Reset all progress and flags*, or Progress →
*Reset all progress*. You can also just delete `progress.sqlite3`.

---

## Project layout

```
sds1-exam-study/
├── app.py                  Streamlit entry point
├── requirements.txt
├── start.bat / start.sh    one-click launcher
├── src/
│   ├── scoring.py          MC marking engine (the exam rules)
│   ├── loader.py           question loading + schema validation
│   ├── progress.py         local SQLite progress
│   ├── ui.py               shared components
│   └── views/              one module per screen
├── data/questions.json     the 200 questions
└── tools/
    ├── build_bank.py       rebuild data/questions.json from tools/bank/
    ├── validate.py         full validation (schema, counts, R coverage)
    ├── test_scoring.py     regression tests vs the official marking table
    ├── verify_r.py         executes every R snippet in the bank
    └── bank/               question sources, one file per lecture
```

## Contributing questions

Questions live in `tools/bank/l1.py` … `l9.py`. To change one:

```bash
python tools/build_bank.py     # rebuild data/questions.json
python tools/validate.py       # check schema, counts and R coverage
python tools/verify_r.py       # run every R snippet
python tools/test_scoring.py   # re-run the grading regression tests
```

All four must pass before opening a pull request. `validate.py` fails if any lecture loses
R coverage, so you cannot silently drop a topic.

---

## Academic use

This is a study aid built from the course's own lecture material for exam preparation.
The lecture PDFs themselves are **not** included in this repository — only questions
citing them by filename and slide number. The HT25 mock exam questions have been
paraphrased rather than reproduced verbatim.