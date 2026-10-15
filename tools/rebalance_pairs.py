"""Rebalance which pairs of option letters carry the correct answers.

Run:  python tools/rebalance_pairs.py            (dry run, prints the plan)
      python tools/rebalance_pairs.py --apply    (rewrite the question sources)

Why this exists
---------------
Every five-option question in the exam has exactly two correct options, so
there are ten possible keys. If one of them is much more common than the rest,
a student who always ticks those two letters scores well without reading
anything. The bank drifted that way while the questions were being reshaped,
because the natural place to put a second true option was often next to the
first, and the most common key ended up at 22% of the questions.

How a move works
----------------
Reordering the options of a question changes its key without changing a single
word of it, so it is safe as long as two things hold: nothing in the question
refers to a position ("the first plot", "the second bar"), and nothing refers
to a letter ("so (c) is false"). Both are checked before a question is touched,
and a question failing either check is never rotated.

Rotation preserves the relative order of the options, which keeps the true
options reading in a sensible sequence, and it reaches only five of the ten
keys from any given start, because the move is a shift of a five-element
cycle. The planner accounts for that and only proposes reachable targets.

The rewrite goes through ast, so the option list is cut out of the source by
exact line and column rather than by matching text, and the result is checked
to be a permutation of the original before it is written.
"""

from __future__ import annotations

import argparse
import ast
import collections
import itertools
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "data" / "questions.json"
TOOLS = ROOT / "tools"
BANK_DIR = TOOLS / "bank"

LETTERS = "abcde"
TARGET_SHARE = 0.20

# The gate allows 20%, but merely dipping under it leaves a lopsided bank: at
# the time this was written the rarest key appeared zero times and the next
# rarest five times, which passes the gate while still handing a student who
# noticed the pattern a real edge. So the planner aims for an even spread
# instead, and only falls back to the gate's limit if evenness is unreachable.
EVEN_MAX = 15

# A question that mentions a position or a letter cannot be rotated without
# rewriting its own text, so it is left alone.
LETTER_REF = re.compile(r"\(([a-e])\)|\boption\s+[a-e]\b", re.I)
ORDER_REF = re.compile(
    r"\b(first|second|third|fourth|fifth|last|final|previous|above|below|top|"
    r"bottom|latter|former)\b", re.I)


def pairs() -> list[tuple[int, int]]:
    return list(itertools.combinations(range(5), 2))


PAIR_NAME = {"".join(LETTERS[i] for i in p): p for p in pairs()}


def reachable(pair: tuple[int, int]) -> dict[tuple[int, int], int]:
    """Map each rotation shift to the pair of letters it produces."""
    out = {}
    for r in range(5):
        tgt = tuple(sorted(((pair[0] + r) % 5, (pair[1] + r) % 5)))
        out[tgt] = r
    return out


def rotatable(q: dict) -> bool:
    if q.get("type") != "MC":
        return False
    if len(q.get("options") or {}) != 5 or len(q.get("correct") or []) != 2:
        return False
    text = " ".join(str(q.get(k) or "") for k in ("stem", "explanation", "detail"))
    text += " " + " ".join(str(v) for v in q["options"].values())
    return not (LETTER_REF.search(text) or ORDER_REF.search(text))


def plan(questions: list[dict]) -> list[tuple[str, str, str, int]]:
    """Choose rotations until no key exceeds the target share.

    Returns a list of (question id, from key, to key, shift).
    """
    counts = collections.Counter("".join(sorted(q["correct"]))
                                 for q in questions
                                 if q.get("type") == "MC"
                                 and len(q["options"]) == 5
                                 and len(q["correct"]) == 2)
    # A Counter has no key for a pair that never occurs, so the emptiest target
    # would be invisible to the search. Seed all ten.
    for name in PAIR_NAME:
        counts.setdefault(name, 0)
    total = sum(counts.values())
    limit = TARGET_SHARE * total
    by_pair = collections.defaultdict(list)
    for q in questions:
        if rotatable(q):
            by_pair["".join(sorted(q["correct"]))].append(q["id"])

    moves: list[tuple[str, str, str, int]] = []
    counts = collections.Counter(counts)
    stop_reason = "evenly spread"
    for _ in range(4000):
        worst = max(counts.items(), key=lambda kv: (kv[1], kv[0]))
        if worst[1] <= EVEN_MAX:
            break
        src_name, src = worst[0], PAIR_NAME[worst[0]]
        reach = reachable(src)
        # Pick the emptiest key that this pair can actually rotate into.
        target = None
        for cand, n in sorted(counts.items(), key=lambda kv: (kv[1], kv[0])):
            if n < worst[1] and PAIR_NAME[cand] in reach:
                target = cand
                break
        if target is None:
            stop_reason = "no reachable emptier key for %s" % src_name
            break
        if not by_pair[src_name]:
            stop_reason = "no rotatable question left with key %s" % src_name
            break
        qid = by_pair[src_name].pop()
        moves.append((qid, src_name, target, reach[PAIR_NAME[target]]))
        counts[src_name] -= 1
        counts[target] += 1
    if stop_reason != "evenly spread":
        print("stopped early: %s" % stop_reason)
        print("most common key still at %.1f%% against a %.0f%% limit"
              % (max(counts.values()) / total * 100, TARGET_SHARE * 100))
    return moves


def find_call(tree: ast.AST, qid: str):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "mc":
            if node.args and isinstance(node.args[0], ast.Constant) \
                    and node.args[0].value == qid:
                return node
    return None


def segment(src_lines: list[str], node) -> str:
    seg = ast.get_source_segment("\n".join(src_lines), node)
    return seg if seg is not None else ""


def rebuild_list(node, lines: list[str], raw_segments: list[str]) -> str:
    """Re-emit a list literal from per-element raw source, same layout."""
    if not node.elts:
        return "[]"
    close_indent = re.match(r"[ \t]*", lines[node.end_lineno - 1]).group(0)
    prefix = re.match(r"[ \t]*", lines[node.elts[0].lineno - 1]).group(0)
    parts = [prefix + raw.replace("\n", "\n" + prefix) for raw in raw_segments]
    return "[\n" + ",\n".join(parts) + ",\n" + close_indent + "]"


def offsets(text: str, lineno: int, col: int) -> int:
    """Character offset of a (1-based line, 0-based column) position."""
    lines = text.split("\n")
    return sum(len(l) + 1 for l in lines[:lineno - 1]) + col


def apply_moves(moves, apply: bool) -> int:
    """Rewrite the option order and key of each question in place.

    The replacement is done by character offset taken from the parse tree, not
    by searching for the old text. An earlier version searched, and a key like
    ["a"] occurs in dozens of questions in the same file, so the search happily
    rewrote a different question's key. Offsets cannot be confused that way.
    """
    by_file = collections.defaultdict(list)
    for m in moves:
        by_file[group_of(m[0])].append(m)
    total = 0
    for fname, group in by_file.items():
        path = BANK_DIR / fname
        text = path.read_text(encoding="utf-8")
        if any(ord(ch) > 127 for ch in text):
            raise SystemExit("%s: non-ascii source, column offsets unsafe" % fname)
        lines = text.split("\n")
        tree = ast.parse(text)
        edits = []
        for qid, src_key, dst_key, shift in group:
            call = find_call(tree, qid)
            if call is None:
                raise SystemExit("no mc() call found for %s in %s" % (qid, fname))
            opts, correct = call.args[4], call.args[5]
            raws = [segment(lines, el) for el in opts.elts]
            if len(raws) != 5:
                raise SystemExit("%s: expected 5 options, found %d"
                                 % (qid, len(raws)))
            rotated = (raws[-shift:] + raws[:-shift]) if shift else list(raws)
            if sorted(rotated) != sorted(raws):
                raise SystemExit("%s: rotation is not a permutation" % qid)
            # the new key must be a rotation of the old one, not an arbitrary pair
            src_pair = PAIR_NAME[src_key]
            if PAIR_NAME[dst_key] not in reachable(src_pair):
                raise SystemExit("%s: %s -> %s is not a rotation" % (qid, src_key, dst_key))
            new_opts = rebuild_list(opts, lines, rotated)
            new_correct = "[" + ", ".join('"%s"' % c for c in sorted(dst_key)) + "]"
            edits.append((offsets(text, opts.lineno, opts.col_offset),
                          offsets(text, opts.end_lineno, opts.end_col_offset),
                          new_opts, qid))
            edits.append((offsets(text, correct.lineno, correct.col_offset),
                          offsets(text, correct.end_lineno, correct.end_col_offset),
                          new_correct, qid))
        edits.sort(key=lambda e: -e[0])
        for start, end, new, qid in edits:
            text = text[:start] + new + text[end:]
            total += 1
        ast.parse(text)  # refuse to write source that no longer parses
        if apply:
            path.write_text(text, encoding="utf-8")
    return total


FILE_OF = {}
for _p in sorted(BANK_DIR.glob("*.py")):
    FILE_OF[_p.stem] = _p.name


def group_of(qid: str) -> str:
    if qid.startswith("G-"):
        return "graphs.py"
    lec = qid[1]
    return "l%s.py" % lec


def snapshot(questions: list[dict]) -> dict:
    """For every MC question: the set of option texts, and the set of TRUE texts."""
    out = {}
    for q in questions:
        if q.get("type") != "MC":
            continue
        opts = q.get("options") or {}
        out[q["id"]] = (
            frozenset(opts.values()),
            frozenset(opts[k] for k in (q.get("correct") or []) if k in opts),
            q.get("stem"),
            q.get("explanation"),
        )
    return out


def verify(questions: list[dict], before: dict) -> list[str]:
    """Every question must keep the same options, the same true options and the
    same stem and explanation. Only the order and the letters may move."""
    problems = []
    for q in questions:
        if q.get("type") != "MC":
            continue
        opts = q.get("options") or {}
        now = (
            frozenset(opts.values()),
            frozenset(opts[k] for k in (q.get("correct") or []) if k in opts),
            q.get("stem"),
            q.get("explanation"),
        )
        was = before.get(q["id"])
        if was is None:
            problems.append("%s: new question appeared" % q["id"])
            continue
        for i, label in enumerate(("options", "true options", "stem",
                                   "explanation")):
            if now[i] != was[i]:
                problems.append("%s: %s changed" % (q["id"], label))
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    questions = json.loads(BANK.read_text(encoding="utf-8"))["questions"]
    before = snapshot(questions)
    moves = plan(questions)
    if not moves:
        print("no rotations needed")
        return 0

    counts = collections.Counter("".join(sorted(q["correct"])) for q in questions
                                 if q.get("type") == "MC" and len(q["options"]) == 5
                                 and len(q["correct"]) == 2)
    print("before: %s" % ", ".join("%s=%d" % kv for kv in sorted(counts.items())))
    total = sum(counts.values())
    print("most common key at %.1f%% (limit %.0f%%), across %d questions"
          % (max(counts.values()) / total * 100, TARGET_SHARE * 100, total))
    print()
    for qid, a, b, r in moves:
        print("  %-12s %s -> %s  (right shift by %d)" % (qid, a, b, r))
    print()
    print("%d rotations planned" % len(moves))
    if not args.apply:
        print("dry run; pass --apply to write")
        return 0
    n = apply_moves(moves, True)
    print("applied %d edits" % n)

    # The bank is rebuilt from source, then every question is compared with the
    # snapshot taken before the rewrite. A rotation that moved a key onto the
    # wrong option, or that touched a question it was not planned for, fails
    # here rather than in a student's face.
    import subprocess
    subprocess.run([sys.executable, str(TOOLS / "build_bank.py")],
                   cwd=str(ROOT), check=True, capture_output=True)
    after = json.loads(BANK.read_text(encoding="utf-8"))["questions"]
    problems = verify(after, before)
    if problems:
        print("\nVERIFICATION FAILED, %d problems:" % len(problems))
        for p in problems[:20]:
            print("  " + p)
        return 1
    counts = collections.Counter("".join(sorted(q["correct"])) for q in after
                                 if q.get("type") == "MC" and len(q["options"]) == 5
                                 and len(q["correct"]) == 2)
    total = sum(counts.values())
    print("verified: every question kept its options, its true options, its "
          "stem and its explanation")
    print("after:  %s" % ", ".join("%s=%d" % kv for kv in sorted(counts.items())))
    print("most common key now %.1f%% (limit %.0f%%)"
          % (max(counts.values()) / total * 100, TARGET_SHARE * 100))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
