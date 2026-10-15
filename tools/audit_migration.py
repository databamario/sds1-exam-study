"""Print the answer key of every question changed since a git ref, for reading.

Run:  python tools/audit_migration.py [<git-ref>]

Reworking a question means editing its option list and then marking two of
them correct. Those two steps drift apart easily: an option inserted in the
middle shifts every letter after it, and a key written from memory of the old
layout then marks whatever landed in that slot. That happened twice while
reshaping Lectures 1 to 3, and in both cases the question passed every gate,
because nothing in the suite can tell a true statement from a false one.

So this is a reading tool, not a checker. It prints the currently keyed text of
every question that differs from the given ref, so the keys can be read against
the options instead of trusted. Use it after any batch of edits and before
committing.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "data" / "questions.json"
DEFAULT_REF = "c40e8cb"


def load_current() -> dict[str, dict]:
    payload = json.loads(BANK.read_text(encoding="utf-8"))
    return {q["id"]: q for q in payload["questions"]}


def load_at(ref: str) -> dict[str, dict]:
    proc = subprocess.run(
        ["git", "show", "%s:data/questions.json" % ref],
        cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8",
    )
    if proc.returncode != 0:
        raise SystemExit("cannot read %s: %s" % (ref, proc.stderr.strip()))
    return {q["id"]: q for q in json.loads(proc.stdout)["questions"]}


def fingerprint(q: dict) -> str:
    return json.dumps(q, sort_keys=True)


def main(argv: list[str]) -> int:
    ref = argv[1] if len(argv) > 1 else DEFAULT_REF
    new = load_current()
    old = load_at(ref)

    changed = sorted(i for i in new
                     if fingerprint(new[i]) != fingerprint(old.get(i, {})))
    if not changed:
        print("no questions differ from %s" % ref)
        return 0

    by_group: dict[str, int] = {}
    for qid in changed:
        # Group on the id, not the lecture field. The graph questions carry the
        # lecture of the slide they came from, so grouping them by lecture
        # scatters them across L2, L3, L4, L7 and L8 and makes it look as
        # though untouched lectures had been edited.
        prefix = "graph" if qid.startswith("G-") else "L%d" % new[qid]["lecture"]
        by_group[prefix] = by_group.get(prefix, 0) + 1

    print("changed since %s: %d questions" % (ref, len(changed)))
    print("  " + ", ".join("%s=%d" % kv for kv in sorted(by_group.items())))
    print()
    print("Read every KEYED line below and confirm it is actually true.")
    print("An option that reads like a distractor is the classic symptom of a")
    print("key that did not follow its option when the list was reordered.")
    print()

    bad_shape = 0
    for qid in changed:
        q = new[qid]
        opts = q.get("options") or {}
        correct = q.get("correct") or []
        print("%s   key=%s   topic=%s"
              % (qid, ",".join(correct), q.get("topic", "")))
        for label, text in opts.items():
            if label in correct:
                print("    KEYED  (%s) %s" % (label, text))
        if len(correct) != 2 and len(opts) == 5:
            print("    !! five options but %d correct" % len(correct))
            bad_shape += 1
        if len(opts) > 5:
            print("    !! %d options" % len(opts))
            bad_shape += 1
        print()

    print("%d questions to read, %d shape problems flagged mechanically."
          % (len(changed), bad_shape))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
