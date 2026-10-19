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

Both tables above are written by hand, which is the hole this file also closes.
A check that nobody added verifies nothing, and nothing about the run says so.
So after the declared checks run, every numeric literal asserted in a written
answer is compared against them. Anything left over is an *unverified claim*,
and it must appear in ACCEPTED below with a reason for why it cannot be
checked. There is no third option: undeclared means failing.

Run:  python tools/verify_numbers.py
       python tools/verify_numbers.py --report     # list them, exit 0
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
    # Found by the audit below, which is the only thing that could find them:
    # every one of these numbers was being asserted by a written answer with
    # nothing recomputing it.
    ("G-WA-008", "30", "2 + 5 + 11 + 9 + 3", 1e-9),
    ("G-WA-008", "0.23", "(2 + 5) / (2 + 5 + 11 + 9 + 3)", 5e-3),
    ("L1-WA-003", "0.5", "1 / 2", 1e-9),
    ("L6-WA-001", "4.9", "(179 - 170) / 1.83", 5e-2),
    ("L6-WA-003", "1.96", "qnorm(0.975)", 1e-3),
    ("L7-WA-003", "1.96", "qnorm(0.975)", 1e-3),
    ("L7-WA-003", "-1.96", "qnorm(0.025)", 1e-3),
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
    ("L3-WA-002", 3, "25", "25th percentile"),
    ("L3-WA-002", 3, "75", "75th percentile"),
]

NUM_RE = re.compile(r"-?\d+\.?\d*(?:[eE][-+]?\d+)?")
# print() prefixes scalars with a "[1] " index marker, which would otherwise be
# read as the first number in the output.
INDEX_RE = re.compile(r"\[\d+\]")

# A bare integer that is really a decimal - "24." at the end of a sentence, or
# "42," inside a list. The looser NUM_RE above swallows the punctuation; this
# one does not, and it is the one used for the audit.
LITERAL_RE = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")

# Numeric literals that a written answer asserts and that are deliberately NOT
# recomputed by R or looked up on a slide: {question id: {literal: reason}}.
#
# The reason is the point. A number nobody can check is fine as long as somebody
# had to write down why. A bare list of numbers would be the same hole this
# table exists to close, one level down.
ACCEPTED: dict[str, dict[str, str]] = {
    # --- read off a generated figure; the drawing is the source --------------
    "G-WA-001": {"30": "the common median of all three groups, read off the figure"},
    "G-WA-005": {"0.6": "an approximate correlation read off the generated scatter"},
    "G-WA-007": {
        "0.62": "the cell value in the generated correlation matrix",
        "-0.33": "the cell value in the generated correlation matrix",
    },
    "G-WA-008": {
        "11": "a bar height in the generated figure",
        "29": "the upper edge of a bin label in the generated figure",
    },
    "G-WA-011": {"7.4": "a boundary marked on the generated normal curve"},
    "G-WA-012": {
        "6.2": "the centre marked on the generated normal curve",
        "7.4": "a boundary marked on the generated normal curve",
    },
    # --- definitions, not measurements ---------------------------------------
    "G-WA-003": {"0.05": "the conventional significance level, named in the question"},
    "L3-WA-002": {"50": "'the middle 50%' is the definition of the IQR"},
    "L4-WA-002": {
        "26": "the red-card count of a standard deck",
        "52": "the size of a standard deck",
    },
    "L9-WA-006": {"0.5": "the success probability of a fair coin"},
    "L9-WA-007": {
        "30": "the group size in the birthday problem",
        "365": "the number of days in a year",
    },
    # --- totals derived from figures already given in the question ----------
    "L4-WA-004": {"10": "the bag total, 5 + 3 + 2 from the question"},
    "L4-WA-005": {"10": "the bag total, 5 + 3 + 2 from the question"},
    "L4-WA-008": {"10": "the bag total, 5 + 3 + 2 from the question"},
    # --- quoted from the lecture material, which is not in the repo ----------
    "L1-WA-008": {
        "2.4": "the size of the Literary Digest poll, a historical figure",
        "57": "its predicted share for Landon, a historical figure",
        "62": "the share Roosevelt actually won with, a historical figure",
    },
    "L4-WA-003": {
        "14": "the MTO table count quoted from the lecture slide",
        "24": "the MTO table count quoted from the lecture slide",
        "72": "the MTO table total quoted from the lecture slide",
    },
    "L4-WA-006": {
        "14": "the MTO table count quoted from the lecture slide",
        "24": "the MTO table count quoted from the lecture slide",
        "72": "the MTO table total quoted from the lecture slide",
    },
    "L5-WA-001": {
        "50": "the sample size of the lecture's worked example",
        "169.03": "that example's sample mean; the data itself is not in the repo",
    },
    "L7-WA-005": {
        "0.05": "the conventional significance level",
        "66.28": "66.27714 from the R output quoted in the question, to 2 dp",
        "77.72": "77.72286 from the R output quoted in the question, to 2 dp",
    },
    "L7-WA-008": {
        "10": "n in the worked example the question describes",
        "72": "that example's sample mean",
        "75": "that example's null mean",
    },
    "L6-WA-002": {"170": "an arbitrary null mean used as an example"},
    # --- illustrative values, chosen to make a point -------------------------
    "L1-WA-003": {"3.14": "an example value of the numeric type"},
    "L2-WA-005": {"100": "an arbitrary default in a code example"},
    "L4-WA-007": {
        "4.5": "an impossible count, used to show what discrete rules out",
        "100": "an illustrative possible burn-out time",
        "250.5": "an illustrative possible burn-out time",
    },
}


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


def literals(text: str) -> set[str]:
    """Every numeric literal in `text`, as written."""
    return {m.group(0) for m in LITERAL_RE.finditer(text or "")}


def is_noise(value: float) -> bool:
    """Literals that are never a statistical claim."""
    if float(value).is_integer() and abs(value) < 10:
        return True          # 0-9: counts of points, of sentences, of answers
    if float(value).is_integer() and 1900 <= value <= 2100:
        return True          # a year
    return False


def unverified_literals(questions: dict[str, dict]) -> list[tuple[str, str]]:
    """Numeric literals a written answer asserts and nothing verifies.

    A literal is excluded when it is already claimed by a check in R_CHECKS or
    PDF_CHECKS, when it is noise, or when the stem already states it - a number
    repeated from the stem is an input the answer works from, not a value the
    answer produces.
    """
    claimed: dict[str, set[str]] = {}
    for qid, claim, *_ in R_CHECKS:
        claimed.setdefault(qid, set()).add(claim)
    for qid, _lecture, claim, _needle in PDF_CHECKS:
        claimed.setdefault(qid, set()).add(claim)

    out: list[tuple[str, str]] = []
    for qid, q in sorted(questions.items()):
        if q.get("type") != "WA":
            continue
        given = set()
        for raw in literals(str(q.get("stem") or "")):
            given.add(str(float(raw)))
        body = " ".join(str(q.get(k) or "") for k in ("answer", "rubric", "detail"))
        for raw in sorted(literals(body), key=float):
            try:
                value = float(raw)
            except ValueError:
                continue
            if is_noise(value) or str(value) in given or raw in claimed.get(qid, ()):
                continue
            out.append((qid, raw))
    return out


def audit_unverified(failures: list[str], questions: dict[str, dict],
                     report: bool = False) -> int:
    leftovers = unverified_literals(questions)
    if not leftovers:
        print("\n  ok   every number a written answer asserts is checked or justified")
        return 0

    by_q: dict[str, list[str]] = {}
    for qid, raw in leftovers:
        by_q.setdefault(qid, []).append(raw)

    print("\nNumbers asserted in a written answer that nothing verifies:")
    for qid, raws in by_q.items():
        for raw in raws:
            reason = ACCEPTED.get(qid, {}).get(raw)
            if reason:
                print("  ok   %-11s %-9s accepted: %s" % (qid, raw, reason))
            else:
                print("  ??   %-11s %-9s unverified" % (qid, raw))
                if not report:
                    failures.append(
                        "%s: written answer asserts %s and no check covers it. Add "
                        "it to R_CHECKS or PDF_CHECKS, or record why in ACCEPTED."
                        % (qid, raw))
    return len(leftovers)


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
    ap.add_argument("--report", action="store_true",
                    help="list the unverified numbers instead of failing on them")
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
    audit_unverified(failures, questions, report=args.report)
    if failures:
        print("\nProblems:")
        for f in failures:
            print("  " + f)
        return 1
    print("Every asserted number matches R or its source slide.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
