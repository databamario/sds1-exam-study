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
    print("A blank answer never scores the full point")
    print("-" * 58)
    # Every MC has at least one correct option, so marking nothing always
    # misses it. This is the guard against the "mark nothing" exploit.
    blank_checks = [
        (["a", "b"], [], 0.0, "2 correct missed"),
        (["a"], [], 0.5, "1 correct missed"),
    ]
    for correct, selected, expected, note in blank_checks:
        got = score_mc(correct, selected)
        mark = "ok " if got == expected else "FAIL"
        print("  %s  correct=%-10s blank -> %.1f  (expected %.1f)  %s"
              % (mark, ",".join(correct), got, expected, note))
        if got != expected:
            failures.append("blank answer on %s: got %.1f expected %.1f"
                            % (correct, got, expected))

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
    fb = mc_feedback(CORRECT, [])
    print("  blank      : %s" % fb["explanation"])

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