"""Put a question next to the slide it cites, so a human can judge the citation.

``tools/validate.py`` proves a citation names a real file and a real page.
``tools/verify_citations.py`` ranks the ones that look worst. Neither can tell
you whether the page is the *right* page, because that needs reading both sides.
This tool is the reading surface: it prints the question, its keyed answer, and
the text of the slide it points at, for a batch at a time.

It exists because the mechanical gates cannot catch the failure that matters
most. When a question inherited its lecture's citation wholesale, every question
sharing that page inherited the error too, and validate.py reported all of them
as perfectly formed. Reading them side by side is the only thing that found it.

Usage::

    python tools/show_citation.py --band 0 0.10     # the 22 worst, unreviewed
    python tools/show_citation.py --band 0.10 0.15
    python tools/show_citation.py L7-MC-013 L9-MC-006
    python tools/show_citation.py --band 0 0.10 --list-only

Bands are on the score from verify_citations.py. Those scores are compressed and
noisy: roughly a third of anything this shows is a false alarm where the slide
says "quantitative" and the question says "numerical". Judging is the point.

Without the lecture PDFs on this machine it exits cleanly having done nothing,
so it is safe to call from a checkout that has only the repo.
"""

from __future__ import annotations

import argparse
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


def _load_verify_module():
    path = os.path.join(HERE, "verify_citations.py")
    spec = importlib.util.spec_from_file_location("verify_citations", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="*", help="question ids to show")
    ap.add_argument("--band", nargs=2, type=float, metavar=("LO", "HI"),
                    help="show every question whose score falls in this range")
    ap.add_argument("--list-only", action="store_true",
                    help="print just the ids and scores, no slide text")
    args = ap.parse_args()

    if not args.ids and not args.band:
        ap.error("give question ids or --band LO HI")

    vc = _load_verify_module()
    questions = vc.load_bank()
    pdfs = vc.find_pdfs()

    if args.ids:
        wanted = [q for q in questions if q["id"] in set(args.ids)]
        if not wanted:
            print("no question matched %s" % ", ".join(args.ids))
            return 1
        if not pdfs:
            print("no lecture PDFs on this machine, so slides cannot be shown")
            return 0
        slides, idf = vc.slide_texts(pdfs), None
    else:
        if not pdfs:
            print("No lecture PDFs found, so scores cannot be computed.")
            for root in vc.SEARCH_ROOTS:
                print("  %s%s" % (root, "" if os.path.isdir(root) else "  (absent)"))
            return 0
        slides = vc.slide_texts(pdfs)
        idf = vc.build_idf(slides)
        lo, hi = args.band
        rows = []
        for q in questions:
            s, _ = vc.score(q, slides, idf)
            if lo <= s < hi:
                rows.append((s, q))
        rows.sort(key=lambda r: (r[0], r[1]["id"]))
        if not rows:
            print("no questions score in [%.3f, %.3f)" % (lo, hi))
            return 0
        wanted = [q for _, q in rows]
        if args.list_only:
            for s, q in rows:
                print("  %6.3f  %-11s %-22s %s"
                      % (s, q["id"], q["source"]["pdf"], q["source"]["slide"]))
            print("\n  %d questions in [%.3f, %.3f)" % (len(rows), lo, hi))
            return 0

    cache = {}
    for q in wanted:
        src = q["source"]
        page = int(str(src.get("slide", "")).lstrip("pP.") or 0)
        key = (src.get("pdf"), page)
        if key not in cache:
            cache[key] = _slide_text(vc, pdfs, key)
        print("=" * 78)
        print("%s  [L%d]  ->  %s %s"
              % (q["id"], q["lecture"], src.get("pdf"), src.get("slide")))
        print("  topic : %s" % q.get("topic"))
        print("  STEM  : %s" % q.get("stem"))
        # 66 of the 79 questions that carry a `code` block ask about code the
        # stem only refers to, and reading without it means judging a third of
        # the question blind. It is also most of why those questions score low:
        # the matcher sees the stem and the slide, not this field.
        if q.get("code"):
            print("  CODE  :")
            for line in str(q["code"]).splitlines():
                print("       | %s" % line)
        if q["type"] == "MC":
            for letter, text in (q.get("options") or {}).items():
                mark = "*" if letter in q["correct"] else " "
                print("     %s%s. %s" % (mark, letter, text))
        else:
            print("  ANSWER: %s" % q.get("answer"))
        print("  SLIDE : %s" % (cache[key][:620] or "<page has no text layer>"))
        print()
    return 0


def _slide_text(vc, pdfs, key) -> str:
    import fitz
    pdf, page = key
    path = pdfs.get(pdf)
    if not path or page < 1:
        return ""
    doc = fitz.open(path)
    try:
        if page > doc.page_count:
            return ""
        return " ".join(doc[page - 1].get_text().split())
    finally:
        doc.close()


if __name__ == "__main__":
    sys.exit(main())