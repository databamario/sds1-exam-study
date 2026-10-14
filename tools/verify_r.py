"""Execute every R snippet embedded in the question bank.

This is the correctness gate for the R-flavoured questions: if a snippet does
not run, the question is wrong and must be fixed.

Run:  python tools/verify_r.py
Requires Rscript on PATH (or pass --rscript "<path>").

Important: this gate proves the snippet RUNS and calls the right API. It does
NOT prove the numbers a question quotes -- the fixture below is synthetic.
Number checking is a separate gate, tools/verify_numbers.py, which either
recomputes the value in R or anchors it to the printed output on the slide.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.loader import load_bank  # noqa: E402

# The slides are run in the lecturer's session, where these objects already
# exist. The snippets in the bank are fragments lifted out of that session, so we
# declare stand-ins with the same names, columns and column types. Sizes are
# small on purpose: the gate must stay fast and must not imply anything about
# the real values.
FIXTURE = r"""
suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
})
titanic_data <- data.frame(
  class     = factor(rep(c("1st", "2nd", "3rd"), each = 4)),
  survived  = factor(c("no", "yes", "yes", "no", "yes", "no", "no", "no",
                       "no", "yes", "yes", "yes")),
  fare      = c(71.2, 12.0, 8.05, 26.55, 13.0, 10.5, 7.9, 10.5,
                13.6, 21.8, 7.9, 26.5),
  age       = c(38, 29, 26, 35, 27, 25, 33, 24, 30, 28, 32, 22),
  stringsAsFactors = FALSE
)
states <- data.frame(
  area       = c(248, 49, 41, 155, 25, 17, 52, 63),
  population = c(1.2, 0.4, 0.5, 2.1, 0.4, 0.3, 2.4, 1.8),
  murder     = c(13.2, 4.7, 2.6, 10.8, 3.4, 2.1, 1.0, 0.6),
  hs_grad    = c(62.3, 52.6, 40.6, 64.2, 48.6, 38.3, 87.1, 83.0),
  illiteracy = c(2.8, 1.0, 0.7, 0.9, 2.4, 2.0, 0.6, 1.2),
  income     = c(21.0, 10.0, 13.0, 16.0, 9.5, 8.4, 16.4, 13.0),
  frost      = c(48, 12, 5, 20, 3, 2, 4, 6),
  life_exp   = c(70.8, 69.5, 69.1, 66.7, 71.6, 70.6, 72.7, 71.4),
  stringsAsFactors = FALSE
)
x       <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
y       <- c(2, 4, 5, 4, 6, 7, 8, 9, 10, 12)
N       <- 100
n       <- 25
heights <- data.frame(
  height = c(180, 175, 190, 182, 168, 177, 185, 172, 180, 176, 181, 179),
  city   = rep(c("Linkoping", "Norrkoping"), each = 6),
  stringsAsFactors = FALSE
)
t_stat  <- 2.5
p_hat   <- 0.62
r       <- 0.5
sampl   <- c(1, 2, 3, 4, 5)
"""

# Questions whose code must not be executed by this gate, with the reason shown
# in the output so a skip is always visible and never silent.
SNIPPETS_NOT_RUN = {
    "L2-MC-009": "the snippet is `install.packages(\"ggplot2\")`, which must not be "
                 "run during an exam; the question is a comparison of two lines, "
                 "not a program. Running it would need a CRAN mirror and would "
                 "reach the network.",
}

MISSING_RE = re.compile(r"object '([^']+)' not found")


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


def wrap(code: str, fixture: str = FIXTURE) -> str:
    """Build an R script that evaluates the snippet and reports what happened.

    The snippet is emitted as real code. Warnings are counted but never fail
    the gate: two questions are NA-with-warning by design (a character vector
    silently becomes NaN in mean()).

    Failure is signalled through an explicit FAILED flag rather than by
    inspecting the printed value, so an error can never be mistaken for output.
    """
    lines = [fixture, "", "nwarn <- 0L", "err <- NULL", "res <- withCallingHandlers(",
             "  tryCatch({"]
    lines += ["    " + ln for ln in code.splitlines()]
    lines += [
        "  }, error = function(e) { err <<- conditionMessage(e); NULL }),",
        "  warning = function(w) { nwarn <<- nwarn + 1L; invokeRestart('muffleWarning') }",
        ")",
        # print() rather than as.character(): a snippet may legitimately end in a
        # function definition, environment or S4 object, none of which as.character
        # can handle.
        "val <- if (is.null(err)) tryCatch(",
        "         paste(capture.output(print(res)), collapse = ' '),",
        "         error = function(e) '<value not printable>') else ''",
        "cat('FAILED:', if (is.null(err)) 0 else 1, '\\n')",
        "cat('WARNINGS:', nwarn, '\\n')",
        "cat('ERRMSG:', if (is.null(err)) '' else err, '\\n')",
        "cat('OUT:', val, '\\n')",
    ]
    return "\n".join(lines)


def run_snippet(rscript: str, code: str, script: Path) -> tuple[int, str, str]:
    script.write_text(wrap(code), encoding="utf-8")
    proc = subprocess.run([rscript, "--vanilla", str(script)],
                          capture_output=True, text=True, timeout=120)
    value = ""
    nwarn = 0
    failed = "0"
    errmsg = ""
    for line in proc.stdout.splitlines():
        if line.startswith("OUT:"):
            value = line[4:].strip()
        elif line.startswith("WARNINGS:"):
            nwarn = int(line[9:].strip() or 0)
        elif line.startswith("ERRMSG:"):
            errmsg = line[7:].strip()
        elif line.startswith("FAILED:"):
            failed = line[7:].strip()

    detail = ""
    if failed != "0":
        detail = errmsg or "snippet raised an error"
    elif proc.returncode != 0:
        err = proc.stderr.strip().splitlines()
        detail = err[0] if err else "Rscript exited %d" % proc.returncode
    return nwarn, value, detail


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rscript", default=None)
    ap.add_argument("--verbose", action="store_true",
                    help="print the full R output of every snippet")
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
    runnable = [q for q in questions if q["id"] not in SNIPPETS_NOT_RUN]
    print("Found %d questions containing R code (%d to run, %d skipped)\n"
          % (len(questions), len(runnable), len(questions) - len(runnable)))

    ok = 0
    failures: list[tuple[str, str, str]] = []
    missing: Counter[str] = Counter()
    warned = 0

    with tempfile.TemporaryDirectory() as td:
        script = Path(td) / "check.R"
        for q in runnable:
            nwarn, value, detail = run_snippet(rscript, q["code"], script)
            label = "%-10s %-40s" % (q["id"], (q.get("topic") or "")[:40])
            if detail:
                ok += 0
                m = MISSING_RE.search(detail)
                if m:
                    missing[m.group(1)] += 1
                failures.append((q["id"], q.get("topic") or "", detail))
                print("  FAIL %s -> %s" % (label, detail))
            else:
                ok += 1
                if nwarn:
                    warned += 1
                flag = "  (%d warning%s)" % (nwarn, "" if nwarn == 1 else "s") if nwarn else ""
                print("  ok   %s -> %s%s"
                      % (label, (value or "(no value)")[:46], flag))
            if args.verbose:
                print("       code: %s" % q["code"].replace("\n", " ; "))

    print("\n%d snippets executed cleanly, %d failed, %d skipped."
          % (ok, len(failures), len(questions) - len(runnable)))
    if warned:
        print("(%d snippet(s) produced warnings -- counted, not failures.)" % warned)

    if failures:
        print("\nFailures needing attention:")
        for qid, topic, detail in failures:
            print("  %s  %s\n      %s" % (qid, topic, detail))
        if missing:
            print("\nObjects the fixtures still do not provide:")
            for name, count in missing.most_common():
                print("  %-16s used by %d snippet(s)" % (name, count))
        return 1
    print("Every embedded R snippet runs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
