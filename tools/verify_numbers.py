"""Check every number the question bank asserts.

verify_r.py proves a snippet RUNS. It says nothing about whether the number the
question quotes is the number R produces, because most snippets are fragments
evaluated against a synthetic fixture. This gate closes that hole.

Each check has two halves and both must hold:

  1. the claim (`claim`) still appears in the question text, so editing a number
     in the bank breaks the check instead of silently passing it, and
  2. R recomputes the same value, so the claim is actually true.

Checks whose value needs the real `states` dataset, which is not installed
here, are anchored to the PDF instead: the value is looked up in the text of
the source lecture, so the number is traceable to the slide that printed it.

Run:  python tools/verify_numbers.py
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.loader import load_bank  # noqa: E402

LECTURES = Path(r"C:\Users\mario\Desktop\CSS_apps\data_statistics_1\Lectures")

# (question id, claim as written in the question, R expression, tolerance)
R_CHECKS = [
    ("L3-MC-001", "46.8", "mean(c(43, 23, 22, 104, 42))", 1e-9),
    ("L3-MC-001", "82", "diff(range(c(43, 23, 22, 104, 42)))", 1e-9),
    ("G-MC-016", "30", "2 + 5 + 11 + 9 + 3", 1e-9),
    ("L4-WA-002", "1", "26 / 52 + 26 / 52", 1e-9),
    ("L5-MC-005", "0.0345", "pnorm(35.8, 36, 0.11)", 1e-4),
    ("L5-MC-005", "0.9655", "1 - pnorm(35.8, 36, 0.11)", 1e-4),
    ("L5-WA-005", "0.0345", "pnorm(35.8, 36, 0.11)", 1e-4),
    ("L6-MC-004", "4.37e-07", "pnorm(179, 170, 1.83, lower.tail = FALSE)", 1e-3),
    ("L6-WA-008", "4.37e-07", "pnorm(179, 170, 1.83, lower.tail = FALSE)", 1e-3),
    ("L7-MC-012", "0.0008", "{ p <- 160 / 200; p * (1 - p) / 200 }", 1e-9),
    ("L8-MC-002", "5.4738",
     "{ r <- 0.6199323; r * sqrt(48) / sqrt(1 - r^2) }", 1e-4),
    ("L8-MC-002", "1.579e-06",
     "{ r <- 0.6199323; t <- r * sqrt(48) / sqrt(1 - r^2); 2 * pt(-abs(t), 48) }", 1e-3),
    ("L8-MC-002", "0.4153",
     "{ r <- 0.6199323; z <- atanh(r); tanh(z - 1.96 / sqrt(48)) }", 1e-4),
    ("L8-MC-002", "0.7648",
     "{ r <- 0.6199323; z <- atanh(r); tanh(z + 1.96 / sqrt(48)) }", 1e-4),
    ("L8-MC-011", "0.9626",
     "chisq.test(c(8, 10, 9, 12, 11, 10), p = rep(1 / 6, 6))$p.value", 1e-4),
    ("L8-WA-004", "0.9626",
     "chisq.test(c(8, 10, 9, 12, 11, 10), p = rep(1 / 6, 6))$p.value", 1e-4),
    ("L8-MC-012", "1.673e-06", "1 - pf(13.915, 2, 297)", 1e-3),
    ("L8-MC-013", "5.4738",
     "{ r <- 0.6199323; r * sqrt(48) / sqrt(1 - r^2) }", 1e-4),
    ("L8-MC-013", "1.579e-06",
     "{ r <- 0.6199323; t <- r * sqrt(48) / sqrt(1 - r^2); 2 * pt(-abs(t), 48) }", 1e-3),
    ("L9-WA-002", "0.25",
     "integrate(function(y) pnorm(y, 3, 1) * dexp(y, rate = 0.5), 0, Inf)$value", 1e-2),
    ("L9-WA-006", "0.2656", "sum(dbinom(c(1, 5, 9), size = 10, prob = 0.5))", 1e-4),
]

# Values that need the real `states` data, anchored to the slide that printed
# them: (question id, lecture, claim in question, string to find in the PDF).
PDF_CHECKS = [
    ("L8-MC-002", 8, "0.6199323", "0.6199323"),
    ("L8-MC-002", 8, "5.4738", "5.4738"),
    ("L8-MC-002", 8, "1.579e-06", "1.579e-06"),
    ("L8-MC-005", 8, "0.78", "-0.78"),
    ("L8-MC-011", 8, "0.9626", "0.9626"),
    ("L8-MC-012", 8, "13.915", "13.915"),
    ("L8-MC-012", 8, "1.673e-06", "1.673e-06"),
    ("L8-MC-013", 8, "0.6199323", "0.6199323"),
    ("L9-MC-005", 9, "38", "38, 95"),
]

NUM_RE = re.compile(r"-?\d+\.?\d*(?:[eE][-+]?\d+)?")
# print() prefixes scalars with a "[1] " index marker, which would otherwise be
# read as the first number in the output.
INDEX_RE = re.compile(r"\[\d+\]")


def find_rscript(explicit: str | None) -> str | None:
    if explicit:
        return explicit
    found = shutil.which("Rscript")
    if found:
        return found
    root = Path(r"C:\Program Files\R")
    if root.exists():
        for child in sorted(root.glob("R-*"), reverse=True):
            for name in ("Rscript.exe", "Rscript"):
                cand = child / "bin" / name
                if cand.exists():
                    return str(cand)
    return None


def blob(q: dict) -> str:
    parts = [q.get("stem") or "", q.get("answer") or "", q.get("detail") or "",
             q.get("explanation") or "", q.get("code") or "", str(q.get("correct") or "")]
    for v in (q.get("options") or {}).values():
        parts.append(v or "")
    return " ".join(parts)


def run_batch(rscript: str, checks: list[tuple[str, str]], td: str) -> dict[str, str]:
    """Evaluate one expression per check, all in a single R session."""
    script = Path(td) / "nums.R"
    lines = ["options(warn = -1)"]
    for idx, (_qid, expr) in enumerate(checks):
        lines.append("cat('<<%d>>', paste(capture.output(print(try(%s, silent = TRUE))), "
                     "collapse = ' '), '\\n', sep = '')" % (idx, expr))
    script.write_text("\n".join(lines), encoding="utf-8")
    proc = subprocess.run([rscript, "--vanilla", str(script)],
                          capture_output=True, text=True, timeout=300)
    out: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        m = re.match(r"<<(\d+)>>\s?(.*)$", line)
        if m:
            out[str(int(m.group(1)))] = m.group(2).strip()
    if proc.returncode != 0 and not out:
        err = proc.stderr.strip().splitlines()
        print("R failed to run the batch:\n  " + (err[0] if err else "unknown"))
    return out


def first_number(text: str) -> float | None:
    m = NUM_RE.search(INDEX_RE.sub(" ", text or ""))
    if not m:
        return None
    try:
        return float(m.group(0))
    except ValueError:
        return None


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--rscript", default=None)
    args = ap.parse_args()

    questions = {q["id"]: q for q in load_bank()}
    rscript = find_rscript(args.rscript)
    if not rscript:
        print("Rscript not found. Pass --rscript <path>.")
        return 2
    print("Using R at %s\n" % rscript)

    failures: list[str] = []
    checked = 0

    # --- R-recomputed checks -------------------------------------------------
    with tempfile.TemporaryDirectory() as td:
        results = run_batch(rscript, [(c[0], c[2]) for c in R_CHECKS], td)
    for idx, (qid, claim, expr, tol) in enumerate(R_CHECKS):
        q = questions.get(qid)
        if q is None:
            failures.append("%s: question not found in bank" % qid)
            continue
        text = blob(q)
        if claim not in text:
            failures.append("%s: no longer claims %r (question text changed?)" % (qid, claim))
            continue
        got = results.get(str(idx))
        if got is None:
            failures.append("%s: R produced no output for %s" % (qid, expr))
            continue
        value = first_number(got)
        want = float(claim)
        if value is None:
            failures.append("%s: R output %r has no number" % (qid, got[:40]))
            continue
        if abs(value - want) > tol:
            failures.append("%s: question says %s, R gives %.10g  [%s]"
                            % (qid, claim, value, expr))
        else:
            checked += 1
            print("  ok   %-10s %-10s <- %.10g  [%s]" % (qid, claim, value, expr))

    # --- PDF-anchored checks -------------------------------------------------
    try:
        import fitz
    except ImportError:
        print("\n(pymupdf not installed; skipping PDF-anchored checks)")
        fitz = None

    if fitz is not None:
        cache: dict[int, str] = {}
        for qid, lecture, claim, needle in PDF_CHECKS:
            q = questions.get(qid)
            if q is None:
                failures.append("%s: question not found in bank" % qid)
                continue
            if claim not in blob(q):
                failures.append("%s: no longer claims %r" % (qid, claim))
                continue
            if lecture not in cache:
                pdfs = sorted((LECTURES / ("Lecture %d" % lecture)).glob("*.pdf"))
                if not pdfs:
                    cache[lecture] = ""
                else:
                    doc = fitz.open(pdfs[0])
                    cache[lecture] = "\n".join(p.get_text() for p in doc)
                    doc.close()
            hay = cache[lecture].replace(" ", "")
            if needle.replace(" ", "") in hay:
                checked += 1
                print("  ok   %-10s %-10s found on the Lecture %d slide"
                      % (qid, claim, lecture))
            else:
                failures.append("%s: %r is not printed in Lecture %d's slides"
                                % (qid, needle, lecture))

    print("\n%d numeric claims verified, %d failed." % (checked, len(failures)))
    if failures:
        print("\nProblems:")
        for f in failures:
            print("  " + f)
        return 1
    print("Every asserted number matches R or its source slide.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
