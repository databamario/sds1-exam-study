"""Find the slide that actually prints something.

Every citation fix needs the same two questions: does the cited page really
carry this fact, and if not, which page does? ``show_citation.py`` answers the
first by printing one page. Nothing answered the second, so it was answered by
opening the PDF by hand every time.

This searches the slide text of every lecture for a phrase and prints the
matching pages with their number. Re-derive the page from here and then open it
with show_citation.py to confirm the context reads right - a keyword hit is a
candidate, not a verdict.

Usage::

    python tools/find_slide.py "complement"
    python tools/find_slide.py "alphabetic" --lecture 3
    python tools/find_slide.py "cor(" --context 200
    python tools/find_slide.py "mean.*median" --regex

Without the lecture PDFs it exits cleanly having done nothing, like the rest of
the reading tools.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _load_verify_module():
    import importlib.util
    path = os.path.join(HERE, "verify_citations.py")
    spec = importlib.util.spec_from_file_location("verify_citations", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("phrase")
    ap.add_argument("--lecture", type=int, default=None,
                    help="restrict to one lecture number")
    ap.add_argument("--context", type=int, default=90,
                    help="characters of surrounding text to show")
    ap.add_argument("--regex", action="store_true", help="treat the phrase as a regex")
    ap.add_argument("--ignore-case", action="store_true", default=True)
    ap.add_argument("--case", action="store_true", help="match case exactly")
    args = ap.parse_args()

    vc = _load_verify_module()
    pdfs = vc.find_pdfs()
    if not pdfs:
        print("No lecture PDFs found. Looked in:")
        for root in vc.SEARCH_ROOTS:
            print("  %s%s" % (root, "" if os.path.isdir(root) else "  (absent)"))
        return 0

    flags = 0 if args.case else re.IGNORECASE
    pattern = re.compile(args.phrase if args.regex else re.escape(args.phrase), flags)

    try:
        import fitz
    except ImportError:
        print("pymupdf not installed, so the PDFs cannot be read")
        return 2

    total = 0
    for name in sorted(pdfs, key=_lecture_number):
        if args.lecture is not None and _lecture_number(name) != args.lecture:
            continue
        doc = fitz.open(pdfs[name])
        try:
            for i in range(doc.page_count):
                text = " ".join(doc[i].get_text().split())
                for m in pattern.finditer(text):
                    total += 1
                    lo = max(0, m.start() - args.context)
                    hi = min(len(text), m.end() + args.context)
                    print("%-22s p.%-3d ...%s..." % (name, i + 1, text[lo:hi]))
        finally:
            doc.close()

    print("\n%d hit%s" % (total, "" if total == 1 else "s"))
    return 0


def _lecture_number(name: str) -> int:
    m = re.search(r"(\d+)", name)
    return int(m.group(1)) if m else 0


if __name__ == "__main__":
    sys.exit(main())