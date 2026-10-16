"""Triage the citations that the mechanical gate cannot judge.

``tools/validate.py`` proves that every citation names a real file and a page
inside it. That is a necessary condition and it is now satisfied by all 230
questions, but it says nothing about whether the page is the *right* page: a
citation can be perfectly well formed and still point at an unrelated slide.

This tool ranks questions by how badly the cited slide matches the question, so
that the worst ones can be read by hand. It works on the same signal that a
first pass produced a misleading 23% hit rate with, so it is deliberately
conservative:

* Terms are weighted by inverse document frequency across every slide in the
  lectures. "the", "of" and "data" carry almost no weight; "quartile",
  "shapiro" or "kde" carry a lot. An unweighted word count ranks a question
  that happens to share many common words above one that shares the single
  decisive term.
* A question matches the slides it cites, not just any slide, and the reported
  score is how well the *named* slide does. A question whose slide scores well
  is not necessarily correctly cited - the slide could be a relative of the
  right one - so the output is a reading list, not a verdict.

The scores are not comparable across runs: they depend on the lecture PDFs, and
the count of terms per slide changes when a lecture is revised. Compare the
orderings, not the numbers.

Usage::

    python tools/verify_citations.py              # the 25 worst
    python tools/verify_citations.py --limit 60
    python tools/verify_citations.py --id G-MC-001 # explain one question
    python tools/verify_citations.py --figures     # check the graph citations

Without the lecture PDFs on this machine the tool reports that and exits
cleanly, so it is safe to call from a checkout that has only the repo.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANK = os.path.join(REPO, "data", "questions.json")

# Where the lecture PDFs live, relative to wherever this repo was cloned.
SEARCH_ROOTS = [
    os.path.join(REPO, "..", "data_statistics_1", "Lectures"),
    r"C:\Users\mario\Desktop\CSS_apps\data_statistics_1\Lectures",
]

WORD = re.compile(r"[a-z0-9_.]+")

# Some decks set their titles in a letter-spaced face and PyMuPDF returns one or
# two letters per line, so the leading title of such a slide arrives as
# "Di s tr ib uti on o f th e s ampl e x". An earlier version of this file tried
# to reassemble those runs and made things worse: it also swallowed the decks'
# second, normally spaced copy of the same title, turning "with 95% CI for the
# mean" into "95%ciforthe". Every affected slide carries the readable copy
# further down the page, so the text is left exactly as extracted and the
# letterspaced fragment is simply noise that the length filter drops.

# Words that carry no signal about which slide a question came from. Kept as a
# list rather than a stopword set from a library so the behaviour is visible.
STOP = set("""
a an the and or but if then than that this these those is are was were be been
being to of in on at by for with from as it its into not no nor so such i we you
he she they them our your their my me do does did done have has had can could
will would shall should may might must about over under between each per any all
one two three four five how what which who whom whose when where why there here
also just only very more most less least other another same both few many much
value values data variable variables result results using use used gives give
answer answers correct right wrong option options question questions mean means
mean average median number numbers total
# Connectives and framing words: they belong to the question, not to the slide,
# so counting them as misses drowns the terms that carry the actual content.
interpreting interpret shows show shown based plot plots plotted statement
statements describes describe describing against differ differs difference
same another given expect expects expected read reading reads according able
following above below left right group groups distribution distributions
""".split())

# The decks abbreviate and the questions do not, so a question that is correctly
# cited can score near zero on vocabulary alone: L7 p.10 says "95% CI" and the
# question says "confidence interval", and nothing lexical connects them. This
# maps the abbreviations this course actually uses onto the words the questions
# use. It is a hand-written list and it is incomplete by design - it is there to
# stop the ranking being dominated by vocabulary, not to decide anything.
SYNONYMS = {
    "ci": "confidence",
    "sd": "deviation",
    "var": "variance",
    "se": "error",
    "df": "degrees",
    "q1": "quartile",
    "q3": "quartile",
    "corr": "correlation",
    "coef": "coefficient",
    "resid": "residual",
    "null": "hypothesis",
    "alt": "alternative",
    "hyp": "hypothesis",
    "pred": "predict",
    "obs": "observation",
    "n": "sample",
    "p": "probability",
    "pois": "poisson",
    "binom": "binomial",
    "norm": "normal",
    "geom": "geometric",
    "quantile": "quartile",
    "percentile": "quartile",
}


def expand(ws: set[str]) -> set[str]:
    """Add the expansion of any abbreviation present, both ways.

    A question saying "CI" and a slide saying "confidence" then meet in the
    middle, which is what makes the score mean something.
    """
    out = set(ws)
    for short, long in SYNONYMS.items():
        if short in ws:
            out.add(long)
        if long in ws:
            out.add(short)
    return out



def load_bank() -> list[dict]:
    with open(BANK, encoding="utf-8") as fh:
        return json.load(fh)["questions"]


def find_pdfs() -> dict[str, str]:
    """Map every lecture PDF name to a path, or {} if the machine has none."""
    found: dict[str, str] = {}
    for root in SEARCH_ROOTS:
        if not os.path.isdir(root):
            continue
        for lecture in sorted(os.listdir(root)):
            here = os.path.join(root, lecture)
            if not os.path.isdir(here):
                continue
            for name in sorted(os.listdir(here)):
                if name.lower().endswith(".pdf") and name not in found:
                    found[name] = os.path.join(here, name)
    return found


def slide_texts(pdfs: dict[str, str]) -> dict[tuple[str, int], str]:
    """(pdf, page) -> normalised text, 1-indexed like a citation."""
    import fitz  # PyMuPDF, only needed when the PDFs are actually present

    out: dict[tuple[str, int], str] = {}
    for name, path in pdfs.items():
        doc = fitz.open(path)
        for n in range(doc.page_count):
            out[(name, n + 1)] = " ".join(doc[n].get_text().split()).lower()
        doc.close()
    return out


def terms(text: str) -> set[str]:
    # Known abbreviations survive the length filter even when they are two
    # letters long, otherwise "ci" is discarded here and expand() below never
    # gets to turn it into "confidence".
    return {w for w in WORD.findall(text.lower())
            if w not in STOP and (len(w) > 2 or w in SYNONYMS)}


def build_idf(slides: dict[tuple[str, int], str]) -> dict[str, float]:
    """Inverse document frequency of each term over slides, not over questions.

    A term that appears on half the slides tells you nothing about which slide
    is meant. A term on one slide in the whole course is close to a signature.
    """
    df: Counter[str] = Counter()
    for text in slides.values():
        df.update(terms(text))
    total = len(slides)
    return {t: math.log(total / n) for t, n in df.items() if n}


def question_text(q: dict) -> str:
    parts = [q.get("stem", ""), q.get("topic", ""), q.get("explanation", "")]
    for value in (q.get("options") or {}).values():
        parts.append(value)
    parts.append(q.get("answer", ""))
    return " ".join(parts)


def score(q: dict, slides: dict, idf: dict[str, float]) -> tuple[float, list[str]]:
    """Fraction of the question's distinctive terms present on its own slide.

    Weighted by idf, so agreeing on "quartile" counts for far more than
    agreeing on "variable". An empty question carries no score and returns 1.0
    rather than dividing by zero.
    """
    want = terms(question_text(q))
    if not want:
        return 1.0, []
    page = q["source"].get("slide") or ""
    key = (q["source"].get("pdf"), _page(page))
    have = expand(terms(slides.get(key, "")))
    want = expand(want)
    total = sum(idf.get(t, 0.0) for t in want)
    if total <= 0:
        return 1.0, []
    hit = sum(idf.get(t, 0.0) for t in want & have)
    missed = sorted(want - have, key=lambda t: -idf.get(t, 0.0))[:6]
    return hit / total, missed


def _page(slide: str) -> int:
    try:
        return int(str(slide).lstrip("pP."))
    except ValueError:
        return 0


def proximity(q: dict, slides: dict, idf: dict[str, float]) -> dict:
    """Look for the failure that reading by hand kept finding.

    The commonest wrong citation is not an unrelated slide. It is the *right*
    slide split across two PDF pages: the cited page states the problem and the
    page after it carries the code, the formula or the worked numbers. A
    question asking for R code then cites the page that explains the idea.

    Word overlap cannot see this, because the stated problem shares plenty with
    the question. What separates the two is that the decisive terms are missing
    here and present next door. So: take the question's distinctive terms, drop
    the ones the cited page already explains, and see where the rest turn up.

    Returns a verdict plus the terms that decided it.
    """
    want = expand(terms(question_text(q)))
    if not want:
        return {"verdict": "empty", "where": 0, "terms": [], "relieved": 0.0}

    here = _page(q["source"].get("slide"))
    pdf = q["source"].get("pdf")
    if here <= 0:
        return {"verdict": "no-page", "where": 0, "terms": [], "relieved": 0.0}

    missing = want - expand(terms(slides.get((pdf, here), "")))
    missing = {t for t in missing if idf.get(t, 0.0) > 0}
    if not missing:
        return {"verdict": "complete", "where": 0, "terms": [], "relieved": 0.0}

    total = sum(idf.get(t, 0.0) for t in missing)
    best_where, best_relieved, best_terms = 0, 0.0, []
    for offset in (-2, -1, 1, 2):
        neighbour = expand(terms(slides.get((pdf, here + offset), "")))
        found = missing & neighbour
        if not found:
            continue
        weight = sum(idf.get(t, 0.0) for t in found)
        top = sorted(found, key=lambda t: -idf.get(t, 0.0))[:5]
        if weight > best_relieved or (weight == best_relieved and top < best_terms):
            best_where, best_relieved, best_terms = offset, weight, top

    if best_relieved <= 0:
        return {"verdict": "nowhere", "where": 0, "terms": [], "relieved": 0.0}

    # How much of what the cited page failed to explain the neighbour supplies.
    share = best_relieved / total if total else 0.0
    if share >= 0.45 and best_where == 1:
        verdict = "next-page"
    elif share >= 0.30:
        verdict = "neighbour"
    else:
        verdict = "weak"
    return {"verdict": verdict, "where": best_where,
            "terms": best_terms, "relieved": share}


def report_proximity(questions: list[dict], slides: dict, idf: dict) -> int:
    """List the citations whose missing terms turn up on the neighbouring page."""
    rows = []
    for q in questions:
        p = proximity(q, slides, idf)
        if p["verdict"] in ("next-page", "neighbour"):
            rows.append((-p["relieved"], q["id"], q["source"], p))
    rows.sort(key=lambda r: (r[0], r[1]))

    print("Citations whose missing terms appear on an adjacent page")
    print("=" * 74)
    print("  %-11s %-11s %-22s %-6s %s"
          % ("relieved", "verdict", "pdf", "slide", "id"))
    for neg, qid, src, p in rows:
        print("  %-11.0f%% %-11s %-22s %-6s %s"
              % (-neg * 100, p["verdict"], src["pdf"], src["slide"], qid))
        print("       found %+d: %s"
              % (p["where"], ", ".join(p["terms"])))

    counts = {"next-page": 0, "neighbour": 0, "weak": 0, "nowhere": 0,
              "complete": 0, "empty": 0, "no-page": 0}
    for q in questions:
        counts[proximity(q, slides, idf)["verdict"]] += 1
    print()
    print("  every question, by verdict:")
    for name in ("complete", "next-page", "neighbour", "weak", "nowhere"):
        print("    %-11s %d" % (name, counts[name]))
    print()
    print("Read the top of this list by hand. 'next-page' is the split-slide")
    print("failure that reading found most often, but this is a hint and not a")
    print("verdict, and the false-positive rate is high. Two questions already")
    print("confirmed correct by hand score above the cut here: L4-WA-001, whose")
    print("question uses a card example while the slide it cites uses a student")
    print("one, and L7-WA-005, fixed to p.31 and still flagged from p.30. The")
    print("detector cannot tell an example's words appearing elsewhere from the")
    print("teaching being elsewhere, so nothing here is settled until read.")
    return 0


def report_rankings(questions: list[dict], slides: dict, idf: dict,
                    limit: int) -> int:
    ranked = []
    for q in questions:
        s, missed = score(q, slides, idf)
        ranked.append((s, q["id"], q["source"], missed))
    ranked.sort(key=lambda r: (r[0], r[1]))

    print("Reading list, worst match first")
    print("=" * 74)
    print("  %-10s %-22s %-6s %s" % ("score", "pdf", "slide", "id"))
    for s, qid, src, missed in ranked[:limit]:
        print("  %-10.3f %-22s %-6s %s"
              % (s, src["pdf"], src["slide"], qid))
        if missed:
            print("             not on that slide: %s" % ", ".join(missed))
    print()
    print("  %d of %d questions scored below 0.5" % (
        sum(1 for r in ranked if r[0] < 0.5), len(ranked)))
    print()
    print("Read the top of this list by hand, but read the number with care.")
    print("The scores are compressed - the questions are in the student's voice")
    print("and the slides are terse, so even a correct citation rarely scores")
    print("above about 0.3. A low score is usually vocabulary, not a wrong page:")
    print("the matcher cannot see that a slide's '95% CI' is the question's")
    print("'confidence interval'. Use --id to see the slide and judge it, and")
    print("--figures to see which slide each figure's questions cite.")
    return 0


def report_one(questions: list[dict], slides: dict, idf: dict, qid: str) -> int:
    q = next((x for x in questions if x["id"] == qid), None)
    if q is None:
        print("no question with id %r" % qid)
        return 1
    src = q["source"]
    key = (src["pdf"], _page(src["slide"]))
    s, missed = score(q, slides, idf)
    print("=" * 74)
    print("%s   lecture %s   cites %s %s" % (q["id"], q["lecture"],
                                              src["pdf"], src["slide"]))
    print("=" * 74)
    print("\nstem\n----")
    print(q["stem"])
    if q.get("explanation"):
        print("\nkeyed answer\n------------")
        print(q["explanation"][:400])
    print("\ncited slide\n------------")
    print(" ".join(slides.get(key, "<page not found>").split())[:900])
    print("\nmatch %.3f" % s)
    if missed:
        print("question terms absent from that slide: %s" % ", ".join(missed))
    print()
    print("Compare the slide above with the question. If it teaches something")
    print("else, fix the tuple in tools/bank/<lecture>.py and rebuild.")
    return 0


def report_figures(questions: list[dict], slides: dict, idf: dict) -> int:
    """Group the figure questions by figure and show the cited page per figure.

    All 30 figure questions used to share one citation per lecture, so a single
    wrong choice silently mis-cited a whole lecture's worth of questions. The
    citation is now per question, and this makes the grouping visible.
    """
    by_image: dict[str, list[dict]] = defaultdict(list)
    for q in questions:
        if q.get("image"):
            by_image[q["image"]].append(q)

    print("Figure questions by figure")
    print("=" * 74)
    spread = 0
    for image in sorted(by_image):
        group = by_image[image]
        cites = sorted({(q["source"]["pdf"], q["source"]["slide"])
                        for q in group})
        lecs = sorted({q["lecture"] for q in group})
        flag = "" if len(cites) == 1 else "  <-- more than one slide, on purpose"
        if len(cites) > 1:
            spread += 1
        print("  %-16s %d questions   lecture %s" % (
            image, len(group), ",".join(str(x) for x in lecs)))
        for pdf, slide in cites:
            s, _ = score(next(q for q in group
                              if (q["source"]["pdf"], q["source"]["slide"])
                              == (pdf, slide)), slides, idf)
            print("        %-22s %-6s  match %.3f" % (pdf, slide, s))
        print("        %s" % ", ".join(q["id"] for q in group))
        if flag:
            print("       %s" % flag.strip())
        print()
    print("  %d of %d figures deliberately cite more than one slide, because a"
          % (spread, len(by_image)))
    print("  single figure can be used to ask about more than one skill.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--limit", type=int, default=25,
                    help="how many to list (default 25)")
    ap.add_argument("--id", help="explain a single question")
    ap.add_argument("--figures", action="store_true",
                    help="group the figure questions by cited slide")
    ap.add_argument("--proximity", action="store_true",
                    help="flag citations whose missing terms appear next door")
    args = ap.parse_args()

    questions = load_bank()
    pdfs = find_pdfs()
    if not pdfs:
        print("No lecture PDFs found, so citations cannot be checked.")
        print("Looked in:")
        for root in SEARCH_ROOTS:
            print("  %s%s" % (root, "" if os.path.isdir(root) else "  (absent)"))
        print()
        print("tools/validate.py still runs the mechanical check (known file,")
        print("page inside it) without the PDFs. This tool needs the text.")
        return 0

    try:
        slides = slide_texts(pdfs)
    except ImportError:
        print("PyMuPDF is not installed, so the slide text cannot be read.")
        print("  pip install pymupdf")
        return 0

    idf = build_idf(slides)
    if args.id:
        return report_one(questions, slides, idf, args.id)
    if args.figures:
        return report_figures(questions, slides, idf)
    if args.proximity:
        return report_proximity(questions, slides, idf)
    return report_rankings(questions, slides, idf, args.limit)


if __name__ == "__main__":
    sys.exit(main())
