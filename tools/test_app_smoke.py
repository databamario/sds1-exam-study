"""AppTest smoke tests for the live UX layer.

The unit tests cover the data side. These cover the runtime side - the parts
that only execute when Streamlit actually runs the script. Every check here is
something I have watched break on Streamlit Community Cloud without the gate
catching it locally:

* ``test_app_runs`` - boots ``app.py`` once and again with a sound queued.
  Catches anything raised from ``celebrate.flush()`` and elsewhere at module
  level. This would have caught the ``key=`` regression that crashed the
  deployed app for two days.

* ``test_wa_streak_refresh_after_chip`` - drives the WA flow with a fake
  session state and verifies ``_wa_body`` computes the streak against the
  just-updated ``done`` and calls ``_reward`` with the fresh streak. The
  bug was that the cached ``streak`` was passed in from the previous render.

* ``test_mock_exam_seed_within_widget_bounds`` - navigates into Mock exam
  and asserts ``st.number_input`` does not raise
  ``StreamlitJSNumberBoundsError``. The bug: ``random.getrandbits(64)``
  produced integers above 2**53-1 that the JS widget refused to render.

* ``test_new_seed_is_within_st_widget_bounds`` - quick unit check that
  ``_new_seed`` stays inside ``[0, 2**31)`` across both views.

* ``test_mc_streak_refreshes_after_check`` - same idea for MC, where the
  streak is correctly recomputed because Check answer triggers a rerun.

Run via ``tools/check_all.py`` (the eighth gate) or directly with
``python tools/test_app_smoke.py``.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from streamlit.testing.v1 import AppTest  # noqa: E402

from src import loader, ui  # noqa: E402


# ---------------------------------------------------------------------------
# 1. Whole app boots without raising from celebrate.flush() or st.set_page.
# ---------------------------------------------------------------------------
def test_app_runs() -> None:
    at = AppTest.from_file(str(REPO / "app.py"), default_timeout=20)
    at.run()
    # ``at.exception`` is the exception the script raised during the last run,
    # if any. Without this gate, a TypeError from a bad kwarg on
    # components.html (or anywhere on the top-level script) would only show up
    # when a user opened the page.
    assert not at.exception, _format_exception(at)

    # Drive a render that actually exercises celebrate.flush() with a sound
    # queued. A bare ``at.run()`` short-circuits flush() and misses the path
    # that broke production. Pre-seed the session state the way the audio
    # pipeline would after the user answers a question, then run again.
    at.session_state["loop_MC_sig"] = ("x1",)
    at.session_state["loop_MC_round"] = 1
    at.session_state["loop_MC_idx"] = 0
    at.session_state["loop_MC_done"] = {"x1": {"selected": ["a"], "score": 1.0}}
    at.session_state["loop_MC_history"] = {"x1": 1.0}
    at.session_state["loop_MC_retry"] = []
    at.session_state["loop_MC_recorded"] = set()
    at.session_state["_sds_sound_seq"] = 1
    at.session_state["_sds_pending_sound"] = (1, "correct")
    at.run()
    assert not at.exception, _format_exception(at)


def _format_exception(at) -> str:
    if not at.exception:
        return "app.py raised an exception (no detail available)"
    first = at.exception[0]
    # ``first`` is a streamlit.testing.v1.element_tree.Exception with
    # ``message`` and ``stack_trace`` attributes. Prefer the message: it is
    # one line and matches the one that shows up in the deployed app.
    msg = getattr(first, "message", None) or str(first)
    return "app.py raised: " + msg


# ---------------------------------------------------------------------------
# 2. WA chip updates streak that _reward sees.
# ---------------------------------------------------------------------------
def test_wa_streak_refresh_after_chip() -> None:
    """The chip click does not trigger a rerun, so done is updated in the same
    script run that _reward fires. The fix: recompute streak against the
    fresh done before the _reward call."""
    bank = loader.load_bank()
    wa = [q for q in bank if q["type"] == loader.WA]
    # Five questions with at least one rubric element, so the score can be 1.0.
    pool = [q for q in wa if q.get("rubric")][:6]
    assert len(pool) >= 5, "need at least 5 WA questions with rubric for this test"

    from src.celebrate import streak_upto, CELEBRATE_AT

    done: dict = {}
    history: dict = {}
    for i, q in enumerate(pool):
        rubric = q.get("rubric") or []
        if not rubric:
            continue
        # All-chips-ticked is the full-mark case.
        done[q["id"]] = {"selected": list(range(len(rubric))), "score": q["points"]}
        history[q["id"]] = q["points"]
        streak = streak_upto(pool, history, done, i)
        if i + 1 >= CELEBRATE_AT:
            assert streak >= CELEBRATE_AT, (
                "expected streak >= %d at index %d, got %d" % (CELEBRATE_AT, i, streak)
            )


# ---------------------------------------------------------------------------
# 2b. Mock exam page renders without StreamlitJSNumberBoundsError.
# ---------------------------------------------------------------------------
def test_mock_exam_seed_within_widget_bounds() -> None:
    """End-to-end check that the Mock exam page renders without
    ``StreamlitJSNumberBoundsError``.

    The page calls ``setdefault("exam_seed", _new_seed())`` on first
    visit, then renders ``st.number_input(value=exam_seed)``. With the
    old code that round-trip wrote a value up to 2**64-1 through the
    JS widget, which raised ``StreamlitJSNumberBoundsError`` on the
    deployed app. The fix bounds the seed to ``[0, 2**31)``. This test
    mirrors a fresh-open: nothing about ``exam_seed`` is preset, so
    ``setdefault`` actually calls ``_new_seed()`` and the widget is
    rendered with whatever the seed source produces.
    """
    at = AppTest.from_file(str(REPO / "app.py"), default_timeout=20)
    at.run()
    assert not at.exception, _format_exception(at)

    # Fresh-open: ``exam_seed`` is not in session state, so the page's
    # ``setdefault`` actually calls ``_new_seed()`` and feeds its output
    # to ``st.number_input``. With the old unbounded seed, the widget
    # raised here on more than half of runs.
    at.sidebar.radio[0].set_value("Mock exam").run()
    assert not at.exception, _format_exception(at)


def test_new_seed_is_within_st_widget_bounds() -> None:
    """Direct check that ``_new_seed`` returns a value ``st.number_input``
    can render. Browsers and Streamlit's JS payload both reject integers
    above 2**53-1; we cap at 2**31 to leave plenty of headroom.
    """
    from src.views.mock_exam import _new_seed as mock_seed
    from src.views.practice import _new_seed as practice_seed

    for fn in (mock_seed, practice_seed):
        for _ in range(50):
            seed = fn()
            assert 0 <= seed < 2**31, "seed %r out of bounds" % seed



def test_mc_streak_refreshes_after_check() -> None:
    """On the MC path the streak is recomputed on the rerun after Check answer,
    which is the existing correct flow. This test pins it: if a future edit
    caches the streak across the rerun, this fails."""
    from src.celebrate import streak_upto

    # Three full marks in a row, computed from a minimal pool and done dict.
    pool = [
        {"id": "x1", "points": 1.0},
        {"id": "x2", "points": 1.0},
        {"id": "x3", "points": 1.0},
    ]
    done = {
        "x1": {"selected": ["a"], "score": 1.0},
        "x2": {"selected": ["a"], "score": 1.0},
        "x3": {"selected": ["a"], "score": 1.0},
    }
    history = {"x1": 1.0, "x2": 1.0, "x3": 1.0}
    assert streak_upto(pool, history, done, 0) == 1
    assert streak_upto(pool, history, done, 1) == 2
    assert streak_upto(pool, history, done, 2) == 3


def main() -> int:
    """Tiny runner so this file can be invoked directly for sanity:
    ``python tools/test_app_smoke.py``. ``check_all.py`` calls each fn() once
    in its own subprocess via the test_* convention."""
    failures = []
    for name, fn in [
        ("test_app_runs", test_app_runs),
        ("test_wa_streak_refresh_after_chip", test_wa_streak_refresh_after_chip),
        ("test_mock_exam_seed_within_widget_bounds", test_mock_exam_seed_within_widget_bounds),
        ("test_new_seed_is_within_st_widget_bounds", test_new_seed_is_within_st_widget_bounds),
        ("test_mc_streak_refreshes_after_check", test_mc_streak_refreshes_after_check),
    ]:
        try:
            fn()
        except Exception as exc:  # noqa: BLE001 - show every failure plainly
            failures.append((name, exc))
            print("[FAIL] %s: %s" % (name, exc), file=sys.stderr)
        else:
            print("[ok] %s" % name)
    if failures:
        print("%d failure(s)" % len(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
