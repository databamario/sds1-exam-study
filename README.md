# SDS1 Exam Study

Practice for the **Statistics and Data Science I** final exam (subjects 771A15 / 771A16).

**[Open the app →](https://sds1-exam-study-fynxrc3p2g8nhwzxdyclbb.streamlit.app/)**

No install, no account, no sign-up. Open the link and start.

---

## What it is

**243 questions** covering all nine lectures: **158 multiple-choice** and **85 written-answer**,
in the same two formats the real exam uses, grouped lecture by lecture so you can work through
the course in order or jump to whatever is weakest.

- **Study MC** — multiple-choice, one question at a time, marked instantly with an explanation.
- **Study WA** — written answers. You write yours, tick off the points you covered, then compare.
- **Mock exam** — a full timed paper: 41 points, 4 hours, MC and WA mixed, marked the same way.
- **Answer key** — every question with its answer, model answer, and the lecture slide it came from.
- **Progress** — points per lecture, so you can see where you actually are.

No question mentions the lectures. They ask about the statistics, not about what you were taught,
so you are practising the exam and not the slides.

---

## The marking is the real marking

This is the part people get wrong on the day, so the app marks it the way the paper does.

**Multiple-choice.** Mark **all** correct options — there is often more than one. One mistake
costs you half a point.

| You do this | You get |
|---|---|
| All the correct ones, nothing extra | **1.0** |
| Exactly one mistake — a correct one missed, or a wrong one ticked | **0.5** |
| Two or more mistakes | **0** |

**Written answers.** Short. Three sentences unless the question says otherwise, and you can get
partial credit for partial answers. You are not expected to grind through arithmetic — writing
the formula with the numbers substituted is enough. Doing the final calculation earns nothing
extra.

**30 of the questions are graphs.** They show you a plot and ask you to read it — which group has
the larger spread, whether a confidence interval clears the line, whether the mean sits above the
median. This is the part of the exam that is hardest to revise from notes alone.

---

## Coverage

| Lecture | MC | WA | Total |
|---|---:|---:|---:|
| 1 — What is statistics, R basics | 17 | 8 | 25 |
| 2 — Categorical data | 27 | 11 | 38 |
| 3 — Continuous data, joins | 28 | 12 | 40 |
| 4 — Probability and sampling | 12 | 7 | 19 |
| 5 — Random variables, distributions | 16 | 11 | 27 |
| 6 — Inference and hypothesis testing | 13 | 8 | 21 |
| 7 — Tests for means and proportions, confidence intervals | 18 | 11 | 29 |
| 8 — Correlation, ANOVA, chi-squared | 18 | 9 | 27 |
| 9 — Simulation, Monte Carlo, bootstrapping | 9 | 8 | 17 |
| **Total** | **158** | **85** | **243** |

Questions are weighted by how much each lecture is worth, not spread evenly. Just over half of
them involve R — code, R output, or using R itself.

181 questions were written from the lecture slides. 62 are adapted from a past mock exam, so
they are calibrated to a real paper. Every R snippet in the app has been run, and the numeric
answers have been checked against what R actually outputs.

---

## Two things worth knowing

**Linear regression and Bayes' theorem are not in here.** Both are named in the course outline,
but the lectures defer them to SDS2 and never teach them, so there is nothing to write questions
against. If your lecturer announces either will be tested, start with the reading.

**The source slide in the answer key is the one part that is not fully verified.** Every question
records which slide it came from, and each one has been checked to point at a real slide in the
right lecture — but some point at the right slide rather than the *exact* one. If you open one and
it is not what the question is about, it is wrong. Tell us and it gets fixed.

---

## If the page looks dead

The app is hosted on the free Streamlit plan, which puts it to sleep when nobody is using it.
The first person to open it after a quiet period waits 20–30 seconds while it wakes up. That is
normal and it only happens once. If the page never loads after that, it is an actual problem —
open an issue.

There is a sound and some confetti when you get five correct in a row. Both are off with one
toggle in the sidebar.

---

## Use this as a tool, not as a syllabus

This is a practice app built from the course material by someone who sat the exam. It is not a
replacement for the lectures, the slides, or doing the exercises, and it is not a guarantee of
anything. Treat a good score here as a sign you have understood a topic, not as evidence you
will get it in the hall. Nobody knows the paper better than the person who sets it.

If you find a question that is wrong, ambiguous, or marked badly, flag it in the Answer key or
open an issue.

---

## Contributing

Questions are added one lecture at a time from `tools/bank/l1.py` … `l9.py`, and a gate suite has
to pass before anything is committed. See [DEVELOPMENT.md](DEVELOPMENT.md).

---

Built from the course's own lecture material for exam preparation. The lecture PDFs are not
included in the repository — only questions citing them by lecture and slide number. Questions
adapted from a past mock exam have been reworded rather than copied.