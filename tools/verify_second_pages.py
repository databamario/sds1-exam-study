"""Every extra cited page has to earn its place.

The bank now lets a question cite two pages. A real number of questions are
answered by a pair - one page states the problem, another carries the formula,
the code or the numbers - and when only one page was allowed the only fix left
was to delete real course content from the answer.

That opened a door. If adding a second page silences the checker, then any
question can look cited no matter how wrong it is, which is the exact defect
this feature exists to remove. So the extra page has to *supply* something the
primary does not: it must carry at least one of the question's terms that the
primary page leaves unexplained.

A question citing two pages and getting nothing from the second fails here the
same way a question citing a page it does not use fails there. The gate is what
keeps the feature honest, and it was written with the feature for that reason -
if the second page were allowed in unchecked, it would be a way to launder a
wrong citation rather than a way to fix one.

What it does not do is decide whether the extra page is *needed*. One incidental
word passing the bar is enough, and a page that genuinely carries the missing
half can rest on a single word that happens to be too common for the scorer.
So the gate reports what each extra page supplied and leaves that to a reader.

Exits 0 when every extra page supplies something, 1 otherwise.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from verify_citations import (  # noqa: E402
    _cited,
    build_idf,
    expand,
    find_pdfs,
    load_bank,
    question_text,
    slide_texts,
    terms,
)


def audit(questions: list[dict], slides: dict, idf: dict):
    """Return (problems, supply) for every extra page a question cites.

    ``supply`` is what each extra page contributed, so a passing gate can
    still be read rather than trusted: one incidental word is enough to pass,
    and the reader is the one who knows whether that word was load-bearing.
    """
    problems: list[str] = []
    supply: list[tuple[str, int, list[str]]] = []
    for q in questions:
        pages = _cited(q)
        if len(pages) < 2:
            continue
        pdf = q["source"].get("pdf")
        primary = pages[0]

        # What the question wants that its primary page does not already give.
        want = expand(terms(question_text(q)))
        base = expand(terms(slides.get((pdf, primary), "")))
        spare = {t for t in (want - base) if idf.get(t, 0.0) > 0}
        if not spare:
            problems.append(
                "%s: cites %s as well, but p.%d already covers the question "
                "on its own" % (q["id"],
                                ", ".join("p.%d" % p for p in pages[1:]),
                                primary))
            supply.extend((q["id"], p, []) for p in pages[1:])
            continue

        for page in pages[1:]:
            supplied = sorted(spare & expand(terms(slides.get((pdf, page), ""))))
            supply.append((q["id"], page, supplied))
            if not supplied:
                problems.append(
                    "%s: p.%d adds nothing p.%d did not already cover"
                    % (q["id"], page, primary))
    return problems, supply


def main() -> int:
    questions = load_bank()
    pdfs = find_pdfs()
    if not pdfs:
        print("No lecture PDFs found, so a second page cannot be judged.")
        print("Skipping, as the other PDF-backed gates do.")
        return 0
    try:
        slides = slide_texts(pdfs)
    except ImportError:
        print("PyMuPDF is not installed, so the slide text cannot be read.")
        print("  pip install pymupdf")
        return 0

    idf = build_idf(slides)
    multi = [q for q in questions if len(_cited(q)) > 1]
    problems, supply = audit(questions, slides, idf)

    print("Second cited pages")
    print("=" * 66)
    print("  %d of %d questions cite more than one page"
          % (len(multi), len(questions)))
    got = dict(((qid, page), terms) for qid, page, terms in supply)
    for q in multi:
        pages = _cited(q)
        print("    %-11s p.%s" % (q["id"], ", p.".join(str(p) for p in pages)))
        for page in pages[1:]:
            terms_hit = got.get((q["id"], page), [])
            print("        p.%-3d supplies %s"
                  % (page, ", ".join(terms_hit) if terms_hit else "nothing"))
    print()
    if problems:
        print("  %d extra page(s) supply nothing:" % len(problems))
        for line in problems:
            print("    %s" % line)
        print()
        print("Drop the page, or cite one that carries what is missing.")
        return 1
    print("  every extra cited page supplies something the primary lacked.")
    print()
    print("One incidental word is enough to pass that, so read the list above")
    print("rather than the verdict alone. L1-MC-019 cited a second page that")
    print("supplied only the word 'lists' and was dropped: the page it cited")
    print("already said everything the question asks. The opposite also")
    print("happens - L3-WA-004's extra page supplies one word too, but that")
    print("one word is the whole reason the second page is there.")
    return 0


if __name__ == "__main__":
    sys.exit(main())