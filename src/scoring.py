"""Scoring engines for the SDS1 exam study app.

MC scoring follows the mock exam (HT25) grading scheme exactly:

    1.0  All correct options marked AND no incorrect options marked.
    0.5  Exactly one mistake (one correct option missed, OR one incorrect
          option marked).
    0.0  Two or more mistakes.

Every MC question has at least one correct option (enforced by
``tools/validate.py``), so marking nothing is always at least one mistake and
never scores the full point.

WA questions are self-graded against a rubric, mirroring the instruction that
"You can get partial credits for partial answers."
"""

from __future__ import annotations

from typing import Iterable, Sequence

MC_MAX_POINTS = 1.0
MC_HALF_POINTS = 0.5


def mc_mistakes(correct: Iterable[str], selected: Iterable[str]) -> int:
    """Number of mistakes: correct options missed + incorrect options marked."""
    correct_set = set(correct)
    selected_set = set(selected)
    return len(correct_set - selected_set) + len(selected_set - correct_set)


def score_mc(correct: Sequence[str] | Iterable[str],
             selected: Sequence[str] | Iterable[str]) -> float:
    """Score one multiple-choice answer, per the exam's grading scheme."""
    mistakes = mc_mistakes(correct, selected)
    if mistakes == 0:
        return MC_MAX_POINTS
    if mistakes == 1:
        return MC_HALF_POINTS
    return 0.0


def mc_feedback(correct: Iterable[str],
                selected: Iterable[str]) -> dict:
    """Explain an MC score the way the mock exam's table explains it."""
    correct_set = set(correct)
    selected_set = set(selected)
    missed = sorted(correct_set - selected_set)
    extra = sorted(selected_set - correct_set)
    mistakes = len(missed) + len(extra)
    score = score_mc(correct_set, selected_set)

    if mistakes == 0:
        explanation = "All correct options marked, no mistakes."
    elif mistakes == 1:
        parts = []
        if missed:
            parts.append("one correct option not marked (%s)" % ", ".join(missed))
        if extra:
            parts.append("one incorrect option marked (%s)" % ", ".join(extra))
        explanation = "Exactly one mistake: %s." % " and ".join(parts)
    else:
        parts = []
        if missed:
            parts.append("correct option(s) not marked: %s" % ", ".join(missed))
        if extra:
            parts.append("incorrect option(s) marked: %s" % ", ".join(extra))
        explanation = "Two or more mistakes: %s." % "; ".join(parts)

    return {
        "score": score,
        "mistakes": mistakes,
        "missed": missed,
        "extra": extra,
        "correct": sorted(correct_set),
        "selected": sorted(selected_set),
        "explanation": explanation,
    }


def score_wa(rubric_hit_counts: Sequence[int]) -> float:
    """Award partial credit from a self-grading pass over the rubric.

    ``rubric_hit_counts`` is one entry per rubric checkpoint: how many of the
    expected elements of that checkpoint the student's answer contained
    (0, 1, or 2 where a checkpoint has two required elements). Each checkpoint
    contributes its hit count over its element count, scaled to the question's
    point value by the caller.
    """
    if not rubric_hit_counts:
        return 0.0
    return float(sum(rubric_hit_counts))


def wa_partial_credit(hits: int, elements: int, points: float) -> float:
    """Credit for one rubric checkpoint, allowing genuine partial credit."""
    if elements <= 0:
        return 0.0
    return points * (hits / elements)