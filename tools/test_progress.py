"""Tests for the browser-stored progress layer.

``src/progress.py`` kept its public names when it moved from SQLite to browser
local storage, which is what made the change cheap - but it also means the tests
have to be about the arithmetic and the shapes rather than about SQL, since
there is no longer a database to query.

These run bare: no Streamlit server, no browser. The functions under test read
the session mirror, so the tests fill that in directly. What they cannot cover
here is the browser half - that local storage really is written and really is
read back - and that was checked by hand in a real browser instead, which is the
only place it can honestly be checked.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import src.progress as progress  # noqa: E402

FAILURES: list[str] = []


def check(label: str, got, want) -> None:
    if got != want:
        FAILURES.append("%s: got %r, want %r" % (label, got, want))


def set_blob(attempts, prefs=None) -> None:
    """Put a progress blob into the session mirror, as a browser round trip would."""
    progress.st.session_state[progress.SESSION_KEY] = {
        "attempts": list(attempts),
        "prefs": dict(prefs or {}),
    }


def attempt(qid="L1-MC-001", qtype="MC", lecture=1, mode="MC practice",
            score=1.0, max_score=1.0, when=1000.0) -> dict:
    return {
        "question_id": qid,
        "qtype": qtype,
        "lecture": lecture,
        "mode": mode,
        "score": score,
        "max_score": max_score,
        "created_at": when,
    }


def test_decode_is_forgiving() -> None:
    """Anything unusable has to become empty progress, never an exception.

    The value arrives from a browser, so it can be None on the first run of a
    session, and local storage can hold something hand-edited or truncated. A
    corrupt value must not take the app down.
    """
    # exam: None is the third field of the blob - a mock exam in progress, or
    # null. It came with the exam persistence work; these expectations carry it
    # so the shape of the empty blob is pinned in both directions.
    empty = {"attempts": [], "prefs": {}, "exam": None}
    check("decode none", progress._decode(None), empty)
    check("decode empty string", progress._decode(""), empty)
    check("decode junk", progress._decode("not json"), empty)
    check("decode wrong shapes",
          progress._decode({"attempts": "no", "prefs": 5}),
          empty)
    check("decode good",
          progress._decode({"attempts": [1], "prefs": {"a": "b"}}),
          {"attempts": [1], "prefs": {"a": "b"}, "exam": None})
    # a JSON string is accepted too, since that is how a raw store looks
    check("decode from json text",
          progress._decode('{"attempts": [], "prefs": {"sound": "0"}}'),
          {"attempts": [], "prefs": {"sound": "0"}, "exam": None})
    # An exam survives, but only if it is a dict. A string or a list in that
    # slot is corruption, and read_exam() has to be able to say no to it.
    check("decode keeps a saved exam",
          progress._decode({"attempts": [], "prefs": {}, "exam": {"idx": 2}}),
          {"attempts": [], "prefs": {}, "exam": {"idx": 2}})
    check("decode rejects a junk exam",
          progress._decode({"attempts": [], "prefs": {}, "exam": "no"}),
          empty)


def test_overall_sums_scores() -> None:
    set_blob([attempt(score=1.0), attempt(qid="L1-MC-002", score=0.5),
              attempt(qid="L2-WA-001", qtype="WA", lecture=2, score=2.0,
                      max_score=3.0)])
    check("overall", progress.overall(None),
          {"attempts": 3, "got": 3.5, "possible": 5.0})


def test_overall_on_empty_history() -> None:
    set_blob([])
    check("overall empty", progress.overall(None),
          {"attempts": 0, "got": 0.0, "possible": 0.0})


def test_by_lecture_groups_and_sums() -> None:
    set_blob([attempt(qid="a", lecture=1, score=1.0),
              attempt(qid="b", lecture=1, qtype="WA", score=2.0, max_score=3.0),
              attempt(qid="c", lecture=2, score=0.0)])
    rows = progress.by_lecture(None)
    check("by_lecture row count", len(rows), 3)
    check("first lecture", (rows[0]["lecture"], rows[0]["qtype"], rows[0]["n"]),
          (1, "MC", 1))
    check("first lecture got", rows[0]["got"], 1.0)
    check("second row is WA", (rows[1]["qtype"], rows[1]["n"], rows[1]["poss"]),
          ("WA", 1, 3.0))
    check("third lecture", (rows[2]["lecture"], rows[2]["got"]), (2, 0.0))


def test_by_lecture_keeps_the_latest_time() -> None:
    set_blob([attempt(qid="a", when=500.0), attempt(qid="b", when=900.0)])
    rows = progress.by_lecture(None)
    check("last_at is the newest", rows[0]["last_at"], 900.0)


def test_attempts_for_gives_the_latest_per_question() -> None:
    set_blob([attempt(qid="L1-MC-001", score=0.0, when=100.0),
              attempt(qid="L1-MC-001", score=1.0, when=200.0),
              attempt(qid="L9-MC-009", score=1.0, when=300.0)])
    got = progress.attempts_for(None, ["L1-MC-001"])
    check("only the asked-for id", list(got), ["L1-MC-001"])
    check("latest wins", got["L1-MC-001"]["score"], 1.0)


def test_attempts_for_ignores_unknown_ids() -> None:
    set_blob([attempt(qid="L1-MC-001")])
    check("unknown id yields nothing", progress.attempts_for(None, ["L7-MC-013"]), {})


def test_prefs_round_trip() -> None:
    set_blob([], {"sound": "0"})
    check("pref read", progress.get_pref(None, "sound", "1"), "0")
    check("missing pref falls back", progress.get_pref(None, "nope", "fallback"),
          "fallback")


def test_export_rows_is_oldest_first() -> None:
    set_blob([attempt(qid="b", when=300.0), attempt(qid="a", when=100.0),
              attempt(qid="c", when=200.0)])
    check("export order", [r["question_id"] for r in progress.export_rows(None)],
          ["a", "c", "b"])


def test_junk_rows_do_not_break_the_aggregates() -> None:
    """A row that is not a dict should be skipped, not crash the progress screen."""
    set_blob([attempt(qid="a"), "not a row", None, 42])
    check("junk skipped", progress.overall(None)["attempts"], 1)
    check("junk skipped in export", len(progress.export_rows(None)), 1)


def main() -> int:
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
            except Exception as exc:  # a raising test is a failing test
                FAILURES.append("%s raised %s: %s"
                                % (name, type(exc).__name__, exc))
    if FAILURES:
        print("Progress layer: %d failure(s)" % len(FAILURES))
        for f in FAILURES:
            print("  -", f)
        return 1
    print("Progress layer: all checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())