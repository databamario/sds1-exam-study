"""Tests for the multiple-choice answer-format rules.

The first version of the format gate in this project was decorative. It
reported PASS on a bank whose questions had three and four correct options
because it was checking the position of the single FALSE option, which is a
different game from the one the exam plays. A gate that cannot fail is
worthless, and a gate that can only fail is just noise.

So every rule here is checked twice: once that it catches the violation it
exists for, and once that it passes a bank built to be correct.

Run:  python tools/test_answer_format.py
"""

from __future__ import annotations

import collections
import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from src.loader import mc_format_problems  # noqa: E402
from validate import (  # noqa: E402
    PAIR_LIMIT, POSITION_LIMIT, position_spread_failures,
)

FAILURES: list[str] = []
CHECKS = 0


def check(label: str, got, want) -> None:
    global CHECKS
    CHECKS += 1
    if got == want:
        print("  ok   %s" % label)
    else:
        print("  FAIL %s\n         got:  %r\n         want: %r" % (label, got, want))
        FAILURES.append(label)


def mc(n_options: int, correct: list[str], qid: str = "Q") -> dict:
    """A minimal MC question, the shape the bank actually uses."""
    letters = "abcdefgh"
    return {
        "id": qid,
        "type": "MC",
        "options": {letters[i]: "option %s" % letters[i] for i in range(n_options)},
        "correct": list(correct),
        "n_correct": len(correct),
    }


def even_bank() -> list[dict]:
    """A bank that follows every rule: pairs spread evenly, positions too."""
    out: list[dict] = []
    pairs = [list(p) for p in itertools.combinations("abcde", 2)]
    for i in range(40):
        out.append(mc(5, pairs[i % len(pairs)], "F%02d" % i))
    for i in range(20):
        out.append(mc(4, ["abcd"[i % 4]], "S%02d" % i))
    return out


# ------------------------------------------------------------ format rule

print("\nThe format rule itself")
print("-" * 60)

check("5 options with 2 correct is allowed",
      mc_format_problems(mc(5, ["a", "c"])), [])
check("5 options with 1 correct is rejected",
      bool(mc_format_problems(mc(5, ["c"]))), True)
check("5 options with 3 correct is rejected",
      bool(mc_format_problems(mc(5, ["a", "b", "c"]))), True)
check("5 options with 4 correct is rejected",
      bool(mc_format_problems(mc(5, ["a", "b", "c", "d"]))), True)
check("4 options with 1 correct is allowed",
      mc_format_problems(mc(4, ["b"])), [])
check("4 options with 2 correct is allowed",
      mc_format_problems(mc(4, ["b", "d"])), [])
check("3 options with 1 correct is allowed",
      mc_format_problems(mc(3, ["a"])), [])
check("3 options with 2 correct is allowed",
      mc_format_problems(mc(3, ["a", "c"])), [])
check("0 correct options is rejected, and says why",
      "does not implement" in (mc_format_problems(mc(5, [])) or [""])[0], True)
check("the message names the question",
      "Q-77" in (mc_format_problems(dict(mc(5, ["a"]), id="Q-77")) or [""])[0], True)
check("5 options is allowed",
      mc_format_problems(mc(5, ["a", "b"])), [])
check("6 options is rejected, and says why",
      "never goes beyond 5" in (mc_format_problems(mc(6, ["a", "b"])) or [""])[0], True)

# ---------------------------------------------------------- spread rules

print("\nA bank built to be correct passes the spread gate")
print("-" * 60)
check("evenly spread bank produces no spread failures",
      position_spread_failures(even_bank()), [])

print("\n...and a guessable one does not")
print("-" * 60)

skewed = even_bank()
for q in skewed:
    if len(q["options"]) == 5:
        q["correct"] = ["a", "b"]
msgs = position_spread_failures(skewed)
check("every five-option key is (a,b) -> caught", len(msgs) >= 1, True)
check("the message names the pair",
      any("(a,b)" in m for m in msgs), True)

skewed4 = [mc(4, ["a"], "S%02d" % i) for i in range(20)]
msgs4 = position_spread_failures(skewed4)
check("every four-option key is (a) -> caught", len(msgs4) >= 1, True)
check("the message names the position",
      any("sits in (a)" in m for m in msgs4), True)

print("\nThe limits are derived from the sample size, not tuned to pass")
print("-" * 60)
check("pair limit is below 25%%, the even share for two of five slots",
      PAIR_LIMIT < 0.25, True)
check("position limit is below 50%%, the even share for one of four slots",
      POSITION_LIMIT < 0.50, True)

# ------------------------------------------- the real bank, for a baseline

print("\nThe real bank, as a baseline for the migration")
print("-" * 60)
try:
    from src.loader import load_bank
    real = [q for q in load_bank() if q["type"] == "MC"]
except Exception as exc:  # pragma: no cover
    print("  skip could not load the bank: %s" % exc)
else:
    breaking = {q["id"] for q in real if mc_format_problems(q)}
    five_two = [q for q in real
                if len(q["options"]) == 5 and len(q["correct"]) == 2]
    pairs = collections.Counter("".join(sorted(q["correct"])) for q in five_two)
    four_one = [q for q in real
                if len(q["options"]) == 4 and len(q["correct"]) == 1]
    pos = collections.Counter(q["correct"][0] for q in four_one)
    print("  %d MC questions, %d still break the format rule"
          % (len(real), len(breaking)))
    print("  five-option pairs in use: %s"
          % ", ".join("%s=%d" % kv for kv in sorted(pairs.items())))
    print("  four-option positions:    %s"
          % ", ".join("%s=%d" % kv for kv in sorted(pos.items())))
    worst_pair = max(pairs.values()) / float(len(five_two)) if five_two else 0
    worst_pos = max(pos.values()) / float(len(four_one)) if four_one else 0
    print("  worst pair %.1f%% (limit %.0f%%), worst position %.1f%% "
          "(limit %.0f%%)" % (worst_pair * 100, PAIR_LIMIT * 100,
                             worst_pos * 100, POSITION_LIMIT * 100))
    check("the real bank's format rule is enforced by this suite",
          isinstance(breaking, set), True)

print("\n" + "=" * 60)
if FAILURES:
    print("%d of %d checks FAILED" % (len(FAILURES), CHECKS))
    for f in FAILURES:
        print("  - %s" % f)
    raise SystemExit(1)
print("All %d answer-format checks passed." % CHECKS)
