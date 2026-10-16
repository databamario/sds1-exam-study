# SDS1 Exam Study App

A practice app for the **Statistics and Data Science I (771A15 / 771A16)** final exam.

**243 questions** — 158 multiple-choice (MC) and 85 written-answer (WA) — built from all
9 lectures, with the *exact* multiple-choice marking rules from the official exam paper.
30 of them put a **graph in front of you** and ask you to infer from its shape, the way the
real paper does.

> Everything runs locally on your own machine. Nothing is uploaded, nothing is tracked,
> no account needed. Your progress is kept in your own browser, so it is yours alone and
> follows you to a new device only if you move it.

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
>
> The real exam also permits a question with **no** correct option, and awards a full point
> for leaving it blank. `src/scoring.py` does not implement that special case, so the bank
> does not use it. If a question like that is ever added, `validate.py` will reject it with
> a message saying so rather than let it be marked wrong.

### How many options are correct

The exam's own worked example is *"a multiple-choice question with 5 options (a, b, c, d, e),
where a and b are correct"*, and its questions mix three, four and five options. The bank
trains exactly that shape:

| Options | Correct options |
|---|---|
| **5** | **exactly 2** |
| 3 or 4 | 1 or 2 |
| any | **never 3 or 4** |

`tools/validate.py` enforces this. The reason it is a hard rule rather than a preference:
a student who has only ever met questions with three or four correct options cannot be
caught out by a question with three, so a bank that allows them teaches the wrong reflex.

It also checks **where** the answers sit. With five options and two correct, the giveaway is
a *pair* — a student who always ticks (a) and (b) is right on every question whose key
happens to be {a,b}. With four options and one correct it is a single position. Neither may
exceed 20% and 35% of the questions they apply to. An earlier version of the suite checked
the position of the single *false* option instead, which is a different game entirely and
left single-correct questions completely unguarded.

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
| **Study WA** | Written-answer practice. Write your answer, tick the points you covered, then open the model answer if you want it. |
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
   missed. The options are then re-shown as a marked-up list: **green** for a correct
   one, **red** for one you marked wrongly, with a line saying which of the two happened.
3. The explanation sits under a collapsed **"Why?"** panel, so you can move on fast or
   dig in.
4. **Next** moves on. Anything not answered at full marks is queued and comes back in a
   second round, and keeps coming back until you get it.

A row of dots above the question tracks the set: green for full marks, amber for part,
red for none. The end-of-set summary gives your score, how many were at full marks, and
how many are still outstanding.

**Written answers are graded blind.** You write your answer, tick the checklist, and only
then decide whether to open the model answer. It used to appear as soon as you revealed
your answer, which meant the checklist underneath could be filled by reading it rather
than by remembering what you had written.

**No question ever refers to the lectures.** The wording talks about the statistics, not
about what you were taught or which slide it was on. The source citation is kept in the
Answer key, where it is useful for you, and hidden during practice.

---

## Feedback and streaks

A streak counter sits next to the question number and tracks consecutive full marks.
Its size depends on the streak, and at **five in a row** the confetti comes out, growing
with the streak from there.

| Sound | When |
|---|---|
| tap | a very short tick whenever you mark an option |
| correct | a full-mark answer |
| celebrate | five or more correct in a row |
| wrong | a zero |

**Sound and confetti** in the sidebar turns all of it off, and the choice is stored in the
database, so it stays off when you restart. The confetti also disappears on its own if
your system asks for reduced motion, which is worth having: it is an animation that
flashes across the whole screen.

All four sounds are generated from one recording by `tools/make_sfx.py`, which cuts the
long tail, downmixes to mono and sets the peak, then derives the other three from it by
raising and lowering the pitch, so they belong to the same family. Re-run it if you want
to retune them:

```bash
python tools/make_sfx.py     # rewrites static/sfx/
```

---

## Question coverage

| # | Lecture | MC | WA | Total | With a graph |
|---|---|---:|---:|---:|---:|
| 1 | What is statistics? + R basics | 17 | 8 | 25 |  |
| 2 | Descriptive stats for categorical data + R fundamentals | 27 | 11 | 38 | 5 |
| 3 | Descriptive stats for continuous data + joins | 28 | 12 | 40 | 12 |
| 4 | Probability and sampling theory | 12 | 7 | 19 |  |
| 5 | Random variables and probability distributions | 16 | 11 | 27 | 2 |
| 6 | Statistical inference and hypothesis testing | 13 | 8 | 21 |  |
| 7 | Tests for means and proportions, confidence intervals | 18 | 11 | 29 | 5 |
| 8 | Correlation, ANOVA and chi-squared tests | 18 | 9 | 27 | 6 |
| 9 | Simulation-based inference (Monte Carlo, bootstrapping) | 9 | 8 | 17 |  |
| | **Total** | **158** | **85** | **243** | **30** |

Questions are weighted by how much material each lecture covers, not spread evenly. About
51% of all questions involve R code, R output or R tooling.

Every question records the lecture slide it came from, shown in the answer key.

`tools/validate.py` checks mechanically that every citation names a real lecture file and
a page inside it — all 243 pass. That is not the same as being the *right* page.

**34 citations pointing at the wrong lecture or the wrong slide have been found and
fixed**, out of the 113 read by hand. The remaining ~130 have not been, so 34 is a floor
rather than an estimate.

The reading was done in score bands using `tools/verify_citations.py`, and the hit rate
was measured rather than assumed: 67% in the worst band, 28% in the next, then 0% in the
band after that, then 38% on a probe of the band below it, and then 27% and 22% on the two
batches that followed. The zero in the middle is the reason the reading did not stop
there: one empty band was a gap in the signal, not the end of it, and the bands on either
side of it both gave errors. About a third of any shortlist is false alarm, where the
slide says "quantitative" and the question says "numerical".

`tools/show_citation.py` prints a question beside the text of the slide it cites, which
is the only thing that has found these. `validate.py` reports every one of them as
perfectly formed. The dominant cause is structural: a question inherits its lecture's
citation wholesale even when the content belongs elsewhere, so one wrong page silently
mis-cites every question sharing it. Three questions about random variables sat in
Lecture 4 citing a slide about drawing cards.

The commonest single cause is narrower than that, though, and it is mechanically
avoidable: the slide is split across two PDF pages, and the cited one holds the statement
of the problem while the *next* one holds the code, the formula or the worked numbers.
Forty-one questions now sit on the first page of such a pair — a question asking for R
code cited the page that explains the idea; a question about a variance definition cited
the page that introduces variance; a question asking for three formulas cited a page
that contains none of them.

So treat the source line in the answer key as the one part of this app that is not fully
checked, and report it if it looks wrong when you open the slide.

Note that the page number is an **index into the PDF**, not the number printed in the
slide footer. Reading it as the footer scores 26% against the slides; reading it as an
index scores 78%. There is no systematic offset to correct in bulk, which is why every
page was read by hand.

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

Two topics are named in the course syllabus and are **not** in this app, because the
lectures do not teach them. Both notes are here so that a gap reads as a syllabus
discrepancy rather than an oversight.

**Linear regression.** The syllabus lists *"Basics of linear regression"* and the
timetable assigns OpenIntro 8.1 to Lecture 9, which is what makes it look like exam
material. The lectures defer it three separate times:

- Lecture 1 p.13 — *"Regression analysis (Controlling for other factors) (More in SDS2
  next semester)"*
- Lecture 8 p.22 — *"More on correlation and linear regression in SDS2!"*
- Lecture 9 is titled *"Simulation-based inference"* and does not return to it

There is no `lm(`, `predict(`, residual or slope anywhere in the 16 lecture PDFs, and
the mock exam never tests it. Lecture 8 does cover correlation, and that is covered
here.

**Bayes' theorem.** It does not appear on any slide in the course. The only thing that
puts it within reach is that OpenIntro 3.5 is the reading assigned to Lecture 4, so a
lecturer could in principle set a Bayes question from it. Nothing in the slides
supports one, so there is nothing here to anchor a question to.

**Reading an R documentation page.** The mock exam asks for two points on this: given
a help page, name the function, name its package, name two arguments, and write the code
that opens the page. No lecture slide covers the anatomy of a help page — there is no
slide on `Usage`, `Arguments` or `vignette()` anywhere in the 16 PDFs. What the lectures
*do* teach, on L2 p.41, is that functions are organised in packages, that the basic
functions ship with R, and the difference between `install.packages()` and `library()`.
That is covered here (`L2-MC-025`); the rest of the help-page question is not, because
there is nothing in the course to anchor it to.

If your lecturer announces that either will be tested, this app will not have covered
it, and the reading is the place to start.

---

## Where the answers come from

- **181 questions** written fresh from the lecture slides.
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
*Reset all progress*. You can also clear it in the browser: open the developer
tools on the app page and delete the `sds1-progress-v1` entry under Local Storage.

---

## Project layout

```
sds1-exam-study/
├── app.py                  Streamlit entry point
├── requirements.txt
├── start.bat / start.sh    one-click launcher
├── .streamlit/
│   └── config.toml         turns on static/ serving, which the sounds need
├── src/
│   ├── scoring.py          MC marking engine (the exam rules)
│   ├── loader.py           question loading + schema validation
│   ├── progress.py         browser-stored progress and preferences
│   ├── celebrate.py        streaks, confetti and the interface sounds
│   ├── ui.py               shared components + the practice loop
│   └── views/              one module per screen
├── data/
│   ├── questions.json      the 243 questions
│   └── images/             the 10 generated figures
├── static/
│   └── sfx/                the 4 interface sounds, generated by make_sfx.py
├── _progress_component/    browser-local storage for progress. Two files, no build step
└── tools/
    ├── build_bank.py       rebuild data/questions.json from tools/bank/
    ├── figures.py          regenerate data/images/ (matplotlib)
    ├── make_sfx.py         regenerate static/sfx/ from one source recording
    ├── validate.py         full validation (schema, counts, R coverage, keys)
    ├── test_scoring.py     regression tests vs the official marking table
    ├── test_progress.py    tests the browser-stored progress layer
    ├── verify_r.py         executes every R snippet in the bank
    ├── verify_numbers.py   checks every number a question asserts
    ├── test_answer_format.py  proves the MC format rules can pass as well as fail
    ├── verify_citations.py  reading list for citations that may point at the wrong slide
    ├── show_citation.py    prints a question next to the slide it cites, for checking by hand
    ├── rebalance_pairs.py  rotates options when the answer key piles onto one pair
    ├── audit_migration.py  prints the keyed text of questions changed since a given commit
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
python tools/check_all.py             # build + all gates, in the right order
python tools/test_answer_format.py  # re-run the MC format rules
python tools/test_progress.py       # the browser-stored progress layer
```

All six must pass before opening a pull request.

`verify_citations.py` is deliberately **not** one of them: it needs the lecture PDFs and
produces a ranking, not a verdict, so it cannot pass or fail.

```bash
python tools/verify_citations.py             # the 25 worst-matched citations
python tools/verify_citations.py --figures   # which slide each figure's questions cite
python tools/verify_citations.py --id L7-MC-016   # the question beside its slide
python tools/verify_citations.py --proximity   # citations whose content is on the next page
```

Two of these exist because the first version of the R gate was decorative: it
turned each snippet into a string literal instead of running it, so invalid R
reported PASS. Both are now proven to fail — each was run against the bank as it
stood before these checks were added, and both reported the real problems.

`test_answer_format.py` exists for the same reason, about the answer-format
rules. A gate that can only fail is noise, and a gate that cannot fail is
worse, so every rule in it is checked twice: once that it catches the violation
it exists for, and once that a bank built to be correct passes it. It also
prints the live bank's current pair and position spread, as a baseline to
compare against as the format migration proceeds.

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

### Where the answers go

Position is a free guess for anyone who notices the pattern, and the shape of
that free guess depends on the question.

With **five options and two correct**, the giveaway is a *pair*: a student who
always ticks (a) and (b) is right on every question whose key happens to be
{a,b}. With **four options and one correct**, it is a single position.
`validate.py` fails when one pair holds more than 20% of the five-option
questions, or one position more than 35% of the single-correct four-option ones.
Both limits come from the sample size, not from whatever the bank happens to do.

This replaced an earlier check that watched the position of the single **false**
option instead. That was checking a different game, and it had a blind spot: it
only looked at questions with more than one correct option, so the
single-correct ones went entirely unchecked. Fifteen of the nineteen four-option
questions in the bank had the answer at (a) — "tick the first box" was worth 79%
of them — and nothing reported it.

So when you add a question, spread the key rather than letting it fall where it
falls, and say *what* is wrong in the explanation rather than naming a letter.
An explanation that says "(d) is false" silently becomes a lie the moment the
options are reordered. Where an explanation does name a letter — which is often,
because it is the clearest way to justify a distractor — `validate.py` checks the
name against the key, including the two-letter form "(a) and (d) are correct"
that an earlier version of that check could not see.

The bank is now in the right shape throughout: **137** five-option questions
with exactly two correct, **20** four-option questions with one, and nothing
with more than two correct anywhere. The most common key pair holds 13.2% of the
five-option questions, against an even spread of 13.6% across the ten possible
pairs.

`tools/rebalance_pairs.py` fixes a lopsided key distribution by rotating
options, which moves the key without changing a word of the question. It
refuses to touch any question that refers to a position ("the first plot") or a
letter ("so (c) is false"), since rotating those would contradict their own
text, and after writing it rebuilds the bank and checks that every question
kept its options, its true options, its stem and its explanation.


---

## Academic use

This is a study aid built from the course's own lecture material for exam preparation.
The lecture PDFs themselves are **not** included in this repository — only questions
citing them by filename and slide number. The HT25 mock exam questions have been
paraphrased rather than reproduced verbatim.