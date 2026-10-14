"""Merge per-lecture question modules into data/questions.json and validate."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.loader import MC, WA, validate_bank  # noqa: E402

MODULES = ["l1", "l2", "l3", "l4", "l5", "l6", "l7", "l8", "l9"]
OUT = ROOT / "data" / "questions.json"

# Retired: these were valid but duplicated another question's learning objective,
# so they were cut to land the bank on exactly 130 MC / 70 WA.
RETIRED = {
    "L2-MC-013",  # pipe statements - duplicated L2-MC-012
    "L4-MC-003",  # disjoint pairs  - duplicated L4-MC-002
    "L5-MC-014",  # parameter/statistic statements - duplicated L5-MC-006
    "L6-MC-012",  # 68-95-99.7      - tangential to inference core
    "L7-MC-003",  # one-sided statements - duplicated L7-MC-001
    "L8-MC-010",  # chi2 statements - duplicated L8-MC-009
    "L1-MC-017",  # syntax statements - lowest-value item in Lecture 1
    "L3-MC-011",  # which plots suit numeric data - low specificity
    "L5-MC-013",  # CLT statements  - duplicated L5-MC-012
    "L1-MC-013",  # data-types statements - duplicated L1-MC-014
}


def collect() -> list[dict]:
    questions: list[dict] = []
    for name in MODULES:
        try:
            mod = importlib.import_module("tools.bank.%s" % name)
        except ModuleNotFoundError:
            continue
        got = [q for q in mod.questions() if q["id"] not in RETIRED]
        print("  %-4s %3d questions" % (name, len(got)))
        questions.extend(got)
    return questions


def main() -> int:
    print("Collecting question modules")
    questions = collect()

    questions.sort(key=lambda q: (q["lecture"], q["type"], q["id"]))

    problems = validate_bank(questions)
    if problems:
        print("\nSCHEMA PROBLEMS (%d)" % len(problems))
        for p in problems[:40]:
            print("  - %s" % p)
        if len(problems) > 40:
            print("  ... and %d more" % (len(problems) - 40))
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as fh:
        json.dump({"questions": questions}, fh, ensure_ascii=False, indent=1)

    mc = [q for q in questions if q["type"] == MC]
    wa = [q for q in questions if q["type"] == WA]
    zero = [q for q in mc if q["n_correct"] == 0]
    rq = [q for q in questions if q.get("r_flavoured")]

    print("\nWrote %s" % OUT.relative_to(ROOT))
    print("  total questions : %d" % len(questions))
    print("  MC              : %d  (target 130)" % len(mc))
    print("  WA              : %d  (target 70)" % len(wa))
    print("  zero-correct MC : %d  (exam special case)" % len(zero))
    print("  R-flavoured     : %d  (%.0f%%)" % (len(rq), 100 * len(rq) / max(len(questions), 1)))
    print()
    print("  %-4s %5s %5s %6s" % ("Lec", "MC", "WA", "Total"))
    for lec in range(1, 10):
        m = sum(1 for q in mc if q["lecture"] == lec)
        w = sum(1 for q in wa if q["lecture"] == lec)
        print("  %-4d %5d %5d %6d" % (lec, m, w, m + w))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())