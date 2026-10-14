"""Full validation of the question bank.

Run:  python tools/validate.py
Exit code is non-zero if any check fails.
"""

from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.loader import LECTURES, MC, WA, load_bank, validate_bank  # noqa: E402
from src.scoring import score_mc  # noqa: E402

TARGET_MC = 130
TARGET_WA = 70
MIN_ZERO_CORRECT = 4

# Every R function the lectures actually teach. A lecture cannot be "covered"
# unless at least one question references each of its functions.
LECTURE_R_FUNCTIONS = {
    1: ["<-", "c", "data.frame", "factor", "function", "class"],
    2: ["library", "install.packages", "table", "prop.table", "filter", "select",
        "arrange", "mutate", "group_by", "summarize", "|>", "ggplot", "aes",
        "subset", "order", "desc", ".by", "ungroup"],
    3: ["inner_join", "left_join", "right_join", "full_join", "as.numeric",
        "quantile", "IQR", "range", "median"],
    4: ["table"],
    5: ["pnorm", "mean", "median"],
    6: ["pnorm", "qnorm", "qt", "sqrt"],
    7: ["t.test", "prop.test", "pnorm", "pt", "qnorm", "sqrt"],
    8: ["cor", "cor.test", "oneway.test", "chisq.test", "pchisq", "select"],
    9: ["sample", "set.seed", "rnorm", "rexp", "rbinom", "median"],
}


def hr(title):
    print("\n" + title)
    print("-" * len(title))


def main() -> int:
    failures = []
    warnings = []

    questions = load_bank()
    hr("Schema")
    problems = validate_bank(questions)
    if problems:
        failures.append("%d schema problems" % len(problems))
        for p in problems[:20]:
            print("  FAIL %s" % p)
    else:
        print("  ok   all %d questions pass the schema" % len(questions))

    mc = [q for q in questions if q["type"] == MC]
    wa = [q for q in questions if q["type"] == WA]

    hr("Counts")
    print("  MC: %d (target %d)" % (len(mc), TARGET_MC))
    print("  WA: %d (target %d)" % (len(wa), TARGET_WA))
    if len(mc) != TARGET_MC:
        failures.append("MC count is %d, expected %d" % (len(mc), TARGET_MC))
    if len(wa) != TARGET_WA:
        failures.append("WA count is %d, expected %d" % (len(wa), TARGET_WA))
    if len(questions) < 200:
        failures.append("total below 200")

    hr("Multiple-choice grading scheme")
    cases = [
        (["a", "b"], ["a", "b"], 1.0, "all correct marked"),
        (["a"], ["a", "b"], 0.5, "one correct option not marked"),
        (["a", "b", "c"], ["a", "b"], 0.5, "one incorrect option marked"),
        (["a", "c"], ["a", "b"], 0.0, "two mistakes"),
        (["c", "d", "e"], ["a", "b"], 0.0, "two mistakes"),
    ]
    for correct, selected, expected, why in cases:
        got = score_mc(correct, selected)
        ok = got == expected
        print("  %s   %-38s -> %.1f" % ("ok  " if ok else "FAIL", why, got))
        if not ok:
            failures.append("scoring case failed: %s" % why)

    ok = score_mc([], []) == 1.0
    print("  %s   %-38s -> %.1f" % ("ok  " if ok else "FAIL",
                                   "0 correct options, none marked", 1.0))
    if not ok:
        failures.append("zero-correct special case failed")

    hr("Zero-correct questions (exam special case)")
    zero = [q for q in mc if q["n_correct"] == 0]
    print("  found %d (minimum %d)" % (len(zero), MIN_ZERO_CORRECT))
    for q in zero:
        print("    %s  %s" % (q["id"], q["topic"][:48]))
    if len(zero) < MIN_ZERO_CORRECT:
        failures.append("only %d zero-correct MC questions" % len(zero))

    hr("n_correct distribution")
    dist = collections.Counter(q["n_correct"] for q in mc)
    for k in sorted(dist):
        print("  %d correct option(s): %4d questions" % (k, dist[k]))
    if 0 not in dist:
        failures.append("no zero-correct questions at all")
    if 1 not in dist:
        warnings.append("no single-correct questions")

    hr("Source citations")
    missing = [q["id"] for q in questions
               if not q["source"].get("pdf") or not q["source"].get("slide")]
    print("  questions missing a pdf or slide reference: %d" % len(missing))
    if missing:
        failures.append("uncited questions: %s" % ", ".join(missing[:10]))

    hr("Written-answer rubrics")
    bad = [q["id"] for q in wa if not q.get("rubric")]
    print("  WA without a rubric: %d" % len(bad))
    if bad:
        failures.append("WA without rubric: %s" % ", ".join(bad[:10]))
    total_elements = sum(sum(i["elements"] for i in q["rubric"]) for q in wa)
    print("  total rubric checkpoints: %d across %d WA questions"
          % (sum(len(q["rubric"]) for q in wa), len(wa)))
    print("  total gradable elements: %d" % total_elements)

    hr("Adapted vs original")
    adapted = [q for q in questions if q.get("origin") == "adapted_HT25"]
    print("  adapted from the HT25 mock exam: %d" % len(adapted))
    print("  newly written for the lectures:  %d" % (len(questions) - len(adapted)))

    hr("R coverage per lecture")
    for lec in range(1, 10):
        covered = set()
        for q in questions:
            if q["lecture"] == lec:
                covered.update(q.get("r_functions", []))
        want = LECTURE_R_FUNCTIONS[lec]
        missing_fns = [f for f in want if f not in covered]
        status = "ok  " if not missing_fns else "FAIL"
        print("  %s Lecture %d: %d/%d expected functions covered"
              % (status, lec, len(want) - len(missing_fns), len(want)))
        if missing_fns:
            failures.append("Lecture %d missing R coverage: %s"
                            % (lec, ", ".join(missing_fns)))

    hr("Per-lecture totals")
    print("  %-4s %4s %4s %6s" % ("Lec", "MC", "WA", "Total"))
    for lec in range(1, 10):
        m = sum(1 for q in mc if q["lecture"] == lec)
        w = sum(1 for q in wa if q["lecture"] == lec)
        print("  %-4d %4d %4d %6d   %s" % (lec, m, w, m + w, LECTURES[lec][:40]))
        if m + w == 0:
            failures.append("Lecture %d has no questions" % lec)

    hr("Duplicate detection")
    seen_stem = {}
    dupes = []
    for q in questions:
        key = re.sub(r"\W+", " ", q["stem"].lower()).strip()[:90]
        if key in seen_stem:
            dupes.append("%s ~ %s" % (q["id"], seen_stem[key]))
        seen_stem[key] = q["id"]
    print("  near-duplicate stems: %d" % len(dupes))
    for d in dupes:
        print("    %s" % d)
    if dupes:
        warnings.append("%d duplicate stems" % len(dupes))

    ids = [q["id"] for q in questions]
    print("  duplicate ids: %d" % (len(ids) - len(set(ids))))

    hr("Result")
    for wmsg in warnings:
        print("  warn %s" % wmsg)
    if failures:
        print("  %d CHECK(S) FAILED" % len(failures))
        for f in failures:
            print("   - %s" % f)
        return 1
    print("  All checks passed. %d questions ready." % len(questions))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())