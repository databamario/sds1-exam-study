"""Regression tests for the MC scoring engine.

The cases come verbatim from the grading table printed in the mock exam
(mock_exam_ht26 (1).pdf, page 1). Five options (a,b,c,d,e) where a and b are
correct. If this file fails, the whole app is scoring students wrong.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.scoring import mc_feedback, mc_mistakes, score_mc  # noqa: E402

CORRECT = ["a", "b"]

# (student answer, expected score, expected reason keyword)
CASES = [
    (["a", "b"], 1.0, "no mistakes"),
    (["a"], 0.5, "not marked"),
    (["a", "b", "c"], 0.5, "incorrect option marked"),
    (["a", "c"], 0.0, "Two or more mistakes"),
    (["c", "d", "e"], 0.0, "Two or more mistakes"),
]

ZERO_CORRECT = []


def main() -> int:
    failures = []

    print("Mock exam grading table (correct = a, b)")
    print("-" * 58)
    for selected, expected, _ in CASES:
        got = score_mc(CORRECT, selected)
        mark = "ok " if got == expected else "FAIL"
        print("  %s  answer %-12s -> %.1f  (expected %.1f)"
              % (mark, ",".join(selected), got, expected))
        if got != expected:
            failures.append("answer %s: got %.1f expected %.1f"
                            % (selected, got, expected))

    print()
    print("Zero-correct special case")
    print("-" * 58)
    zero_checks = [
        ([], 1.0, "nothing marked -> full point"),
        (["a"], 0.5, "one incorrect marked"),
        (["a", "b"], 0.0, "two incorrect marked"),
    ]
    for selected, expected, note in zero_checks:
        got = score_mc(ZERO_CORRECT, selected)
        mark = "ok " if got == expected else "FAIL"
        print("  %s  answer %-12s -> %.1f  (expected %.1f)  %s"
              % (mark, ",".join(selected) or "(none)", got, expected, note))
        if got != expected:
            failures.append("zero-correct %s: got %.1f expected %.1f"
                            % (selected, got, expected))

    print()
    print("Mistake counting")
    print("-" * 58)
    assert mc_mistakes(CORRECT, CORRECT) == 0
    assert mc_mistakes(CORRECT, ["a"]) == 1            # one correct missed
    assert mc_mistakes(CORRECT, ["a", "b", "c"]) == 1  # one incorrect marked
    assert mc_mistakes(CORRECT, ["a", "c"]) == 2       # missed b + marked c
    print("  ok   mistake counts match the table")

    print()
    print("Feedback wording")
    print("-" * 58)
    fb = mc_feedback(CORRECT, ["a", "b"])
    print("  full credit : %s" % fb["explanation"])
    fb = mc_feedback(CORRECT, ["a"])
    print("  half credit : %s" % fb["explanation"])
    fb = mc_feedback(ZERO_CORRECT, [])
    print("  zero-correct: %s" % fb["explanation"])

    print()
    if failures:
        print("FAILED (%d)" % len(failures))
        for f in failures:
            print("  - %s" % f)
        return 1
    print("All scoring regression tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())