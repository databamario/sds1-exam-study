# SDS1 Exam Study App

A practice app for the **Statistics and Data Science I (771A15 / 771A16)** final exam.

**230 questions** — 148 multiple-choice (MC) and 82 written-answer (WA) — built from all
9 lectures, with the *exact* multiple-choice marking rules from the official exam paper.
30 of them put a **graph in front of you** and ask you to infer from its shape, the way the
real paper does.

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

Mark **all** correct options — *there may be more than one*. Each question is worth at
most 1 point.

| Your answer | Score | Why |
|---|---|---|
| All correct marked, nothing extra marked | **1.0** | no mistakes |
| Exactly one mistake | **0.5** | one correct option missed, **or** one incorrect option marked |
| Two or more mistakes | **0.0** | |
| Nothing marked | **0.0** | every question has a correct option to find |

> Every question in this app has at least one correct option, so leaving the answer blank
> never scores the full point. `tools/validate.py` enforces this.

### Written-answer (WA)

Short and succinct — **max 3 sentences** unless the question says otherwise. Partial
credit is possible for partial answers, so the app shows the model answer and then lets
you tap each point your answer covered.

You do **not** need to grind through calculations. The exam says: *show how you would
solve it — give the formula with the values substituted.* For example, write

```
Xbar = sum(x)/n = (1+2+3)/3
```

and stop there. Doing the final arithmetic is optional and earns nothing extra.

Every model answer is kept short on purpose — the median is 42 words — with any longer
reasoning tucked under a **"Why?"** panel that stays collapsed until you ask for it.

---

## What's in the app

| Section | What it does |
|---|---|
| **Home** | The marking rules and a suggested study order. |
| **Study MC** | Multiple-choice practice, lecture by lecture. One question at a time, instant marking and explanation. |
| **Study WA** | Written-answer practice. Write your answer, reveal the model answer, then tap the points you covered. |
| **Mock exam** | A timed paper that mirrors the real one: **41 points, 4 hours**, mixed MC and WA. MC is marked automatically; WA you self-grade. Change the seed to get a different paper. |
| **Answer key** | Every question with answers, model answers, explanations and the source slide. Filter by lecture and type. **Flag anything you think is wrong** so it is easy to report. |
| **Progress** | Points earned per lecture, and which lectures you are weakest on. One-click reset. |
| **R coverage** | Every R function the lectures teach, and which questions test it. Use this to confirm nothing from the course was skipped. |

**MC and WA are separate study modes on purpose.** They are different kinds of practice:
MC trains careful reading and holding several facts at once; WA trains writing a correct
method under a 3-sentence limit. Practise them separately, then mix them in the mock exam.

### How practice works

Both study modes run the same loop, so nothing feels like a different app halfway
through:

1. One question on screen — the stem, then the figure if it has one.
2. You commit an answer and see the verdict straight away, with the score and what you
   missed.
3. The explanation sits under a collapsed **"Why?"** panel, so you can move on fast or
   dig in.
4. **Next** moves on. Anything not answered at full marks is queued and comes back in a
   second round, and keeps coming back until you get it.

A row of dots above the question tracks the set: green for full marks, amber for part,
red for none. The end-of-set summary gives your score, how many were at full marks, and
how many are still outstanding.

**No question ever refers to the lectures.** The wording talks about the statistics, not
about what you were taught or which slide it was on. The source citation is kept in the
Answer key, where it is useful for you, and hidden during practice.

---

## Question coverage

| # | Lecture | MC | WA | Total | With a graph |
|---|---|---:|---:|---:|---:|
| 1 | What is statistics? + R basics | 17 | 8 | 25 | |
| 2 | Descriptive stats for categorical data + R fundamentals | 23 | 10 | 33 | 4 |
| 3 | Descriptive stats for continuous data + joins | 25 | 11 | 36 | 9 |
| 4 | Probability and sampling theory | 17 | 9 | 26 | 4 |
| 5 | Random variables and probability distributions | 13 | 10 | 23 | 2 |
| 6 | Statistical inference and hypothesis testing | 12 | 8 | 20 | |
| 7 | Tests for means and proportions, confidence intervals | 16 | 10 | 26 | 5 |
| 8 | Correlation, ANOVA and chi-squared tests | 16 | 8 | 24 | 6 |
| 9 | Simulation-based inference (Monte Carlo, bootstrapping) | 9 | 8 | 17 | |
| | **Total** | **148** | **82** | **230** | **30** |

Questions are weighted by how much material each lecture covers, not spread evenly. About
53% of all questions involve R code, R output or R tooling.

Every question records the lecture slide it came from, shown in the answer key.

### Graph questions

30 questions put a figure in front of you. The figures are generated by
`tools/figures.py` with matplotlib — sharp at any size, reproducible with one command,
and carrying no course material. They deliberately mirror the kinds of plot the real
paper uses: grouped bars, box plots, histograms, estimates with confidence intervals,
a normal curve with shaded regions, scatter plots, overlapping densities and a
correlation matrix.

Most ask you to **infer** from a shape rather than read a number off it — which group has
the largest variance, whether a confidence interval clears the reference line, whether the
mean sits above or below the median.

### Not covered, on purpose

**Linear regression is not included.** Lecture 8 states explicitly: *"More on correlation
and linear regression in SDS2!"* No lecture teaches it in this course, and the mock exam
never tested it. If your lecturer announces otherwise, this app will not have covered it.

---

## Where the answers come from

- **168 questions** written fresh from the lecture slides.
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
│   ├── ui.py               shared components + the practice loop
│   └── views/              one module per screen
├── data/
│   ├── questions.json      the 230 questions
│   └── images/             the 10 generated figures
└── tools/
    ├── build_bank.py       rebuild data/questions.json from tools/bank/
    ├── figures.py          regenerate data/images/ (matplotlib)
    ├── validate.py         full validation (schema, counts, R coverage, keys)
    ├── test_scoring.py     regression tests vs the official marking table
    ├── verify_r.py         executes every R snippet in the bank
    ├── verify_numbers.py   checks every number a question asserts
    └── bank/               question sources, one file per lecture, + graphs.py
```

## Contributing questions

Questions live in `tools/bank/l1.py` … `l9.py`, with the graph questions in
`tools/bank/graphs.py`. To change one:

```bash
python tools/build_bank.py     # rebuild data/questions.json
python tools/validate.py       # check schema, counts, keys and R coverage
python tools/verify_r.py       # run every R snippet
python tools/verify_numbers.py # check every number a question asserts
python tools/test_scoring.py   # re-run the grading regression tests
```

All five must pass before opening a pull request.

Two of these exist because the first version of the R gate was decorative: it
turned each snippet into a string literal instead of running it, so invalid R
reported PASS. Both are now proven to fail — each was run against the bank as it
stood before these checks were added, and both reported the real problems.

- `verify_r.py` really executes every snippet. Because most snippets are
  fragments lifted out of the lecturer's session, it prepends a fixture holding
  stand-ins for the objects the slides already define. The fixture proves the
  code *runs and calls the right API*; it says nothing about values, because the
  values are synthetic.
- `verify_numbers.py` covers the values. Each check names a number the question
  claims, requires that claim to still be in the question text, and then either
  recomputes it in R or looks it up in the source slide. Editing a number in the
  bank breaks the check instead of silently passing it.

`validate.py` also fails if an MC question loses its correct option, if an
explanation contradicts its own answer key, if a written answer runs long, if a
question refers to the course rather than to the statistics, or if a referenced
figure file is missing.

### Where the wrong option goes

In a multi-select question with exactly one wrong option, its position is a
free guess for anyone who notices the pattern. This bank originally had 20 of its
22 such questions with the wrong option at (d) or (e), which made "leave the
last two boxes" worth 20 questions on its own. `validate.py` now fails when one
position holds the wrong option for more than 30% of them; the bank sits at
27.3%.

So when you add a multi-select question, put the wrong option where it reads
naturally rather than last, and say *what* is wrong in the explanation rather
than naming a letter. An explanation that says "(d) is false" silently becomes a
lie the moment the options are reordered.


---

## Academic use

This is a study aid built from the course's own lecture material for exam preparation.
The lecture PDFs themselves are **not** included in this repository — only questions
citing them by filename and slide number. The HT25 mock exam questions have been
paraphrased rather than reproduced verbatim.