"""Small constructors so question authoring stays readable and consistent."""


def _source(pdf, slide, also):
    """Build the citation block for a question.

    ``slide`` is the page the answer mostly lives on, and it stays the field
    everything else already reads, so a question that cites one page and one
    that cites two are shaped the same at the front.

    Some questions genuinely need two pages: the cited page states the problem
    and a second one carries the formula, the code or the numbers. Citing only
    the first made those questions unfixable without deleting real course
    content, so the extra page is passed as ``also``.

    ``slides`` is the full set and always starts with ``slide``.
    ``tools/validate.py`` checks that agreement and that every page exists;
    ``tools/verify_second_pages.py`` checks the extra page earns its place.
    """
    src = {"pdf": pdf, "slide": slide}
    pages = [slide] + [p for p in (also or []) if p != slide]
    if len(pages) > 1:
        src["slides"] = pages
    return src


def mc(qid, lecture, topic, stem, options, correct, explanation,
       pdf, slide, points=1, code=None, r_functions=None,
       origin="new", r_flavoured=False, image=None, also=None):
    """Build a multiple-choice question.

    ``correct`` is a list of option labels and must never be empty: every
    question has at least one correct option, so leaving the answer blank is
    always at least one mistake.
    """
    q = {
        "id": qid,
        "lecture": lecture,
        "type": "MC",
        "topic": topic,
        "stem": stem,
        "options": {k: v for k, v in zip("abcdefgh", options)},
        "correct": list(correct),
        "n_correct": len(correct),
        "points": points,
        "explanation": explanation,
        "r_flavoured": bool(code) or bool(r_functions) or r_flavoured,
        "r_functions": list(r_functions or []),
        "source": _source(pdf, slide, also),
        "origin": origin,
    }
    if code:
        q["code"] = code
    if image:
        q["image"] = image
    return q


def wa(qid, lecture, topic, stem, answer, rubric, points, pdf, slide,
       code=None, r_functions=None, origin="new", bullets=None,
       detail=None, image=None, also=None):
    """Build a written-answer question with a self-grading rubric.

    ``answer`` is what the exam asks for and must stay short - the exam caps
    written answers at roughly three sentences. Put anything longer in
    ``detail``, which the app shows under a collapsed "Why?" panel.

    Each rubric entry is ``{"text": ..., "elements": n}`` where ``n`` is how
    many separate things the answer must contain, so partial credit is possible.
    """
    q = {
        "id": qid,
        "lecture": lecture,
        "type": "WA",
        "topic": topic,
        "stem": stem,
        "points": points,
        "answer": answer,
        "detail": detail or "",
        "rubric": rubric,
        "r_flavoured": bool(code) or bool(r_functions),
        "r_functions": list(r_functions or []),
        "source": _source(pdf, slide, also),
        "origin": origin,
    }
    if code:
        q["code"] = code
    if bullets:
        q["bullets"] = bullets
    if image:
        q["image"] = image
    return q


def rb(text, elements=1):
    """Rubric checkpoint."""
    return {"text": text, "elements": elements}
