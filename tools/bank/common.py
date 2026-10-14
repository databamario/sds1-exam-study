"""Small constructors so question authoring stays readable and consistent."""


def mc(qid, lecture, topic, stem, options, correct, explanation,
       pdf, slide, points=1, code=None, r_functions=None,
       origin="new", r_flavoured=False):
    """Build a multiple-choice question.

    ``correct`` is a list of option labels. Pass ``[]`` for the zero-correct
    special case from the exam instructions.
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
        "source": {"pdf": pdf, "slide": slide},
        "origin": origin,
    }
    if code:
        q["code"] = code
    return q


def wa(qid, lecture, topic, stem, answer, rubric, points, pdf, slide,
       code=None, r_functions=None, origin="new", bullets=None):
    """Build a written-answer question with a self-grading rubric.

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
        "rubric": rubric,
        "r_flavoured": bool(code) or bool(r_functions),
        "r_functions": list(r_functions or []),
        "source": {"pdf": pdf, "slide": slide},
        "origin": origin,
    }
    if code:
        q["code"] = code
    if bullets:
        q["bullets"] = bullets
    return q


def rb(text, elements=1):
    """Rubric checkpoint."""
    return {"text": text, "elements": elements}