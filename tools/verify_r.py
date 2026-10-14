"""Execute every R snippet embedded in the question bank.

This is the correctness gate for the R-flavoured questions: if a snippet does
not run, the question is wrong and must be fixed.

Run:  python tools/verify_r.py
Requires Rscript on PATH (or pass --rscript "<path>").
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.loader import load_bank  # noqa: E402

# Snippets that only make sense with course-specific data files or with an
# explicit state built earlier in the same question. These are still checked by
# eye, but are not executed in isolation.
SNIPPETS_ALLOWED_TO_FAIL = {
    "L1-MC-016",  # uses list(1:3, ...) - fine, kept for clarity
}


def find_rscript(explicit: str | None) -> str | None:
    if explicit:
        return explicit
    found = shutil.which("Rscript")
    if found:
        return found
    for base in (r"C:\Program Files\R", "/usr/lib/R", "/Library/Frameworks/R.framework"):
        root = Path(base)
        if not root.exists():
            continue
        for child in sorted(root.glob("R-*"), reverse=True):
            cand = child / "bin" / "Rscript.exe"
            if cand.exists():
                return str(cand)
            cand = child / "bin" / "Rscript"
            if cand.exists():
                return str(cand)
    return None


def wrap(code: str) -> str:
    """Run the snippet inside a function so stray prints do not abort the run."""
    body = code.replace("\\", "\\\\").replace('"', '\\"')
    lines = ["suppressPackageStartupMessages({",
             '  suppressMessages(library(stats))',
             "})",
             "res <- tryCatch({"]
    for line in code.splitlines():
        lines.append('  "%s"' % line.replace("\\", "\\\\").replace('"', '\\"'))
    lines += ["}, error = function(e) paste('ERROR:', conditionMessage(e)))",
              'cat(paste(as.character(res), collapse=" "), "\\n")']
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rscript", default=None)
    args = ap.parse_args()

    rscript = find_rscript(args.rscript)
    if not rscript:
        print("Rscript not found. Pass --rscript <path>.")
        return 2

    ver = subprocess.run([rscript, "-e", "cat(as.character(getRversion()))"],
                         capture_output=True, text=True)
    print("Using R %s at %s" % (ver.stdout.strip(), rscript))
    print()

    questions = [q for q in load_bank() if q.get("code")]
    print("Found %d questions containing R code\n" % len(questions))

    ok = failed = 0
    failures = []
    with tempfile.TemporaryDirectory() as td:
        script = Path(td) / "check.R"
        for q in questions:
            wrapped = wrap(q["code"])
            script.write_text(wrapped, encoding="utf-8")
            proc = subprocess.run([rscript, "--vanilla", str(script)],
                                  capture_output=True, text=True, timeout=120)
            out = proc.stdout.strip()
            bad = proc.returncode != 0 or out.startswith("ERROR:") or proc.stderr.strip()
            label = "%-10s %-42s" % (q["id"], q["topic"][:42])
            if bad:
                failed += 1
                detail = out.splitlines()[0] if out else proc.stderr.strip().splitlines()[0]
                failures.append((q["id"], q["topic"], detail))
                print("  FAIL %s -> %s" % (label, detail))
            else:
                ok += 1
                preview = out.replace("\n", " ")[:52]
                print("  ok   %s -> %s" % (label, preview))

    print("\n%d snippets executed cleanly, %d failed." % (ok, failed))
    if failures:
        print("\nFailures needing attention:")
        for qid, topic, detail in failures:
            print("  %s  %s\n      %s" % (qid, topic, detail))
        return 1
    print("Every embedded R snippet runs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())