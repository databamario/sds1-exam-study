"""Question bank loading, schema validation and filtering."""

from __future__ import annotations

import json
import random
import re
from pathlib import Path
from typing import Any, Iterable

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
QUESTIONS_PATH = DATA_DIR / "questions.json"
IMAGES_DIR = DATA_DIR / "images"

LECTURES = {
    1: "What is statistics? + R basics",
    2: "Descriptive stats for categorical data + R fundamentals",
    3: "Descriptive stats for continuous data + joins",
    4: "Probability and sampling theory",
    5: "Random variables and probability distributions",
    6: "Statistical inference and hypothesis testing",
    7: "Tests for means and proportions, confidence intervals",
    8: "Correlation, ANOVA and chi-squared tests",
    9: "Simulation-based inference (Monte Carlo, bootstrapping)",
}

MC = "MC"
WA = "WA"

# The shape of a multiple-choice question, as the exam actually uses it.
#
# The mock exam's own worked example is "a multiple-choice question with 5
# options (a, b, c, d, e), where a and b are correct", and the questions in it
# mix three, four and five options. So the bank trains exactly that:
#
#   five options  -> exactly two correct
#   three or four -> one or two correct
#   never more than two correct, at any option count
#
# The last line is the load-bearing one. A student who has only ever met
# questions with three or four correct options can be caught out by a single
# question with three, and a bank that lets that happen teaches the wrong
# reflex.
FIVE_OPTION_CORRECT = 2
MAX_CORRECT_OPTIONS = 2


def mc_format_problems(q: dict) -> list[str]:
    """Return the reason(s) a multiple-choice question breaks the format rule.

    Empty list means the question is the right shape. Kept here rather than in
    the validator so that the rule has one definition, and so that a bank which
    is mid-migration still loads: the app runs against a half-converted bank
    without the schema check refusing to open it.
    """
    options = q.get("options") or {}
    correct = q.get("correct") or []
    n_options = len(options)
    n_correct = len(correct)
    where = q.get("id", "<no id>")

    if n_correct == 0:
        # The exam permits a question with no correct option, and scores an
        # unmarked answer as a full point in that case. src/scoring.py does not
        # implement that special case, so the bank does not use it.
        return ["%s: 0 correct options; the exam allows this but scoring.py "
                "does not implement the 'mark nothing' rule" % where]

    if n_correct > MAX_CORRECT_OPTIONS:
        return ["%s: %d correct options, the exam never uses more than %d"
                % (where, n_correct, MAX_CORRECT_OPTIONS)]

    if n_options == 5 and n_correct != FIVE_OPTION_CORRECT:
        return ["%s: 5 options but %d correct; a five-option question must "
                "have exactly %d" % (where, n_correct, FIVE_OPTION_CORRECT)]

    if n_options < 5 and n_correct not in (1, 2):
        return ["%s: %d options with %d correct; a question with fewer than "
                "five options has one or two" % (where, n_options, n_correct)]

    return []


class QuestionBankError(ValueError):
    """Raised when questions.json violates the schema."""


def load_bank(path: Path | None = None) -> list[dict[str, Any]]:
    path = path or QUESTIONS_PATH
    if not path.exists():
        raise QuestionBankError(
            "Question bank not found at %s\n"
            "Run `python tools/validate.py` to see what is expected." % path
        )
    with path.open(encoding="utf-8") as fh:
        payload = json.load(fh)
    questions = payload["questions"] if isinstance(payload, dict) else payload
    if not isinstance(questions, list):
        raise QuestionBankError("questions must be a JSON list")
    return questions


# ---------------------------------------------------------------- validation

def _require(q: dict, key: str, types, where: str) -> Any:
    if key not in q:
        raise QuestionBankError("%s: missing %r" % (where, key))
    val = q[key]
    if not isinstance(val, types):
        raise QuestionBankError(
            "%s: %r should be %s, got %s"
            % (where, key, types, type(val).__name__)
        )
    return val


def validate_question(q: dict) -> None:
    where = q.get("id", "<no id>")

    if not isinstance(q, dict):
        raise QuestionBankError("not an object: %r" % (q,))

    _require(q, "id", str, where)
    _require(q, "lecture", int, where)
    _require(q, "type", str, where)
    _require(q, "topic", str, where)
    _require(q, "stem", str, where)
    _require(q, "points", (int, float), where)

    if q["lecture"] not in LECTURES:
        raise QuestionBankError("%s: lecture %s not in 1-9" % (where, q["lecture"]))
    if q["type"] not in (MC, WA):
        raise QuestionBankError("%s: type must be MC or WA" % where)
    if q["points"] < 0:
        raise QuestionBankError("%s: negative points" % where)

    src = _require(q, "source", dict, where)
    _require(src, "pdf", str, where + ".source")
    _require(src, "slide", str, where + ".source")

    if q["type"] == MC:
        _validate_mc(q, where)
    else:
        _validate_wa(q, where)


def _validate_mc(q: dict, where: str) -> None:
    options = _require(q, "options", dict, where)
    correct = _require(q, "correct", list, where)
    n_correct = _require(q, "n_correct", int, where)

    if len(options) < 2:
        raise QuestionBankError("%s: needs at least 2 options" % where)
    labels = list(options.keys())
    if labels != sorted(labels):
        raise QuestionBankError("%s: option labels not sorted: %s" % (where, labels))

    texts = [v.strip().lower() for v in options.values()]
    if len(set(texts)) != len(texts):
        dupes = [t for t in set(texts) if texts.count(t) > 1]
        raise QuestionBankError("%s: duplicate option text %s" % (where, dupes))

    if n_correct != len(correct):
        raise QuestionBankError(
            "%s: n_correct=%d but len(correct)=%d" % (where, n_correct, len(correct))
        )
    for label in correct:
        if label not in options:
            raise QuestionBankError(
                "%s: correct option %r is not among %s" % (where, label, labels)
            )
    if len(set(correct)) != len(correct):
        raise QuestionBankError("%s: duplicate entries in correct" % where)
    _require(q, "explanation", str, where)


def _validate_wa(q: dict, where: str) -> None:
    _require(q, "answer", str, where)
    _require(q, "detail", str, where)
    rubric = _require(q, "rubric", list, where)
    if not rubric:
        raise QuestionBankError("%s: WA needs a non-empty rubric" % where)
    for item in rubric:
        if not isinstance(item, dict):
            raise QuestionBankError("%s: rubric items must be objects" % where)
        _require(item, "text", str, where + ".rubric")
        elements = _require(item, "elements", int, where + ".rubric")
        if elements < 1:
            raise QuestionBankError("%s: rubric elements must be >= 1" % where)


def validate_question_figure(q: dict) -> Path | None:
    """Return the figure path a question points at, checking it exists.

    Figures are optional. When one is referenced it must be present, otherwise
    the student would silently get a question they cannot answer.
    """
    name = q.get("image")
    if not name:
        return None
    if not isinstance(name, str):
        raise QuestionBankError("%s: image should be a string" % q.get("id"))
    path = IMAGES_DIR / (name + ".png")
    if not path.exists():
        raise QuestionBankError(
            "%s: missing figure %s (run `python tools/figures.py`)"
            % (q.get("id"), path.name)
        )
    return path


def validate_bank(questions: Iterable[dict]) -> list[str]:
    """Validate every question. Returns a list of problems (empty means ok)."""
    problems: list[str] = []
    seen_ids: dict[str, int] = {}
    for idx, q in enumerate(questions):
        try:
            validate_question(q)
            validate_question_figure(q)
        except QuestionBankError as exc:
            problems.append("question[%d]: %s" % (idx, exc))
            continue
        qid = q["id"]
        if qid in seen_ids:
            problems.append("duplicate id %s (also at index %d)"
                            % (qid, seen_ids[qid]))
        seen_ids[qid] = idx
    return problems


# ------------------------------------------------------------------ filtering

def by_lecture(questions: Iterable[dict]) -> dict[int, list[dict]]:
    grouped: dict[int, list[dict]] = {n: [] for n in LECTURES}
    for q in questions:
        grouped[q["lecture"]].append(q)
    return grouped


def of_type(questions: Iterable[dict], qtype: str) -> list[dict]:
    return [q for q in questions if q["type"] == qtype]


def is_r_flavoured(q: dict) -> bool:
    """True when the question asks about R code, R output or R tooling."""
    if q.get("r_functions"):
        return True
    if q.get("code"):
        return True
    return bool(re.search(r"\bR\b|\bRStudio\b", q.get("stem", "")))


def shuffled(questions: list[dict], seed: int | None = None) -> list[dict]:
    out = list(questions)
    random.Random(seed).shuffle(out)
    return out


def total_points(questions: Iterable[dict]) -> float:
    return float(sum(q["points"] for q in questions))