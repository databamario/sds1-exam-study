"""Run every gate, in the order that makes them meaningful.

This exists because of a trap that has caught twice now. ``build_bank.py``
merges ``tools/bank/*.py`` into ``data/questions.json``. If a source file has a
syntax error, the build fails - and then every *other* gate still goes green,
because they read the ``questions.json`` that was left over from the last
successful build. That file is perfectly valid, so nothing complains. The suite
reports seven green gates while the bank has not been rebuilt at all, and the
one thing that matters - that the shipped bank matches its sources - is not
checked by anything.

So two things happen here that did not happen before:

1. The build runs first and a failure stops everything. There is no reading of
   seven greens over a stale bank.

2. After a successful build, ``data/questions.json`` is compared against git.
   If the rebuild changed it, the committed bank is out of date and that is a
   failure, not a detail. This catches the case where the build *succeeds* but
   somebody edited a question in ``tools/bank/`` and never rebuilt, which no
   exit code would ever reveal.

Usage::

    python tools/check_all.py          # run everything
    python tools/check_all.py -v       # also print each gate's output

Exit status is 0 only when every gate passed.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BANK = REPO / "data" / "questions.json"

# The build is not a gate like the others: it produces the thing the others
# check, so it has to come first and it has to be allowed to stop the run.
BUILD = "tools/build_bank.py"

# Every other gate, in the order they were added.
GATES = [
    "tools/validate.py",
    "tools/test_answer_format.py",
    "tools/test_scoring.py",
    "tools/test_progress.py",
    "tools/verify_r.py",
    "tools/verify_numbers.py",
]


def run(step: str, verbose: bool) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, str(REPO / step)],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    out = ((proc.stdout or "") + (proc.stderr or "")).strip()
    if verbose and out:
        print(out)
    return proc.returncode == 0, out


def bank_is_stale() -> bool:
    """True when rebuilding produced a different questions.json than git holds."""
    proc = subprocess.run(
        ["git", "diff", "--quiet", "--", str(BANK.relative_to(REPO))],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    if proc.returncode not in (0, 1):
        # No git, or not a repository. Not a reason to fail the suite.
        return False
    return proc.returncode == 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="print each gate's output as well")
    args = ap.parse_args()

    failures: list[str] = []

    ok, out = run(BUILD, args.verbose)
    print("%-28s %s" % (BUILD, "ok" if ok else "FAILED"))
    if not ok:
        print()
        print("The bank did not build, so nothing below it means anything:")
        print("every other gate would read the questions.json left over from")
        print("the last successful build and go green. Fix this first.")
        if out:
            print()
            print(out)
        return 1

    if bank_is_stale():
        failures.append(
            "data/questions.json differs from what tools/bank/ produces. "
            "A question was edited without rebuilding the bank, so the shipped "
            "questions are not the ones in the source files."
        )
        print("%-28s STALE" % "data/questions.json")
    else:
        print("%-28s ok" % "data/questions.json up to date")

    for gate in GATES:
        ok, out = run(gate, args.verbose)
        print("%-28s %s" % (gate, "ok" if ok else "FAILED"))
        if not ok:
            failures.append(gate)
            if out:
                print()
                print(out)
                print()

    print()
    if failures:
        print("SUITE FAILED (%d):" % len(failures))
        for f in failures:
            print("  -", f)
        return 1
    print("SUITE GREEN: build is current and all %d gates passed." % len(GATES))
    return 0


if __name__ == "__main__":
    sys.exit(main())