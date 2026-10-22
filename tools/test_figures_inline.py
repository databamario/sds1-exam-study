"""Figures must be inlined in the page, not served from Streamlit's media store.

``st.image(bytes)`` registers the image in Streamlit's media file manager and
serves it from ``/media/<hash>.png``. That entry is deleted whenever no running
script references it - ``script_runner`` clears session refs with no session id
at the start of every run, so the references are global, and
``remove_orphaned_files`` runs at the end and drops whatever is left
unreferenced. So navigating away from a question with a figure deletes that
figure from the server while the URL in any DOM still holding it is unchanged.
Measured on the running app: 200 while rendered, 404 after navigating away.

A data URI carries its own bytes, so there is nothing on the server to lose.
This gate pins that, because the failure it prevents is invisible to every
other gate: the figure renders perfectly on the first load and breaks later,
which reads as "the images are flaky" rather than as a regression.

Run via ``tools/check_all.py`` (the eleventh gate) or on its own:
``python tools/test_figures_inline.py``.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from streamlit.testing.v1 import AppTest  # noqa: E402

from src import loader, ui  # noqa: E402


def _figure_questions(bank) -> list[dict]:
    with_figure = [q for q in bank if q.get("image")]
    assert with_figure, "the bank has no figure questions, so this gate tests nothing"
    return with_figure


def test_render_figure_emits_a_data_uri() -> None:
    """Every figure in the bank must render as an inline data URI.

    Rendered under AppTest, which does not need a browser: the assertion is on
    the markup Streamlit produced, not on pixels.
    """
    bank = loader.load_bank()
    figures = _figure_questions(bank)
    for q in figures:
        ui._FIGURE_URI.pop(q["image"], None)
        ui._FIGURE_SIZE.pop(q["image"], None)

    at = AppTest.from_string(
        "import sys\n"
        "sys.path.insert(0, %r)\n"
        "from src import loader, ui\n"
        "import streamlit as st\n"
        "bank = loader.load_bank()\n"
        "for q in bank:\n"
        "    if q.get('image'):\n"
        "        ui.render_figure(q)\n" % str(REPO)
    )
    at.run()
    assert not at.exception, [str(e) for e in at.exception]

    blocks = [m.value for m in at.markdown]
    img_blocks = [b for b in blocks if "<img" in b]
    assert len(img_blocks) == len(figures), (
        "expected %d rendered figures, found %d" % (len(figures), len(img_blocks))
    )
    for block in img_blocks:
        if "/media/" in block:
            raise AssertionError(
                "a figure is still served from Streamlit's media store, which "
                "deletes it as soon as nothing references it: %r"
                % block[:120]
            )
        if 'src="data:image/png;base64,' not in block:
            raise AssertionError(
                "a figure is not a png data URI either: %r" % block[:120]
            )
        if "alt=" not in block:
            raise AssertionError("a figure has no alt text: %r" % block[:120])


def test_figures_are_encoded_once_and_reused() -> None:
    """Encoding is cached for the life of the process.

    Not a micro-optimisation: twelve figures is 528 KB of PNG, so base64 on
    every rerun is 704 KB re-encoded per interaction, and the encode is the
    expensive part. The cache is what makes inlining affordable.
    """
    bank = loader.load_bank()
    q = _figure_questions(bank)[0]
    ui._FIGURE_URI.pop(q["image"], None)
    ui._FIGURE_SIZE.pop(q["image"], None)

    at = AppTest.from_string(
        "import sys\n"
        "sys.path.insert(0, %r)\n"
        "from src import loader, ui\n"
        "bank = loader.load_bank()\n"
        "q = [x for x in bank if x.get('image')][0]\n"
        "ui.render_figure(q)\n"
        "first = ui._FIGURE_URI[q['image']]\n"
        "ui.render_figure(q)\n"
        "assert ui._FIGURE_URI[q['image']] is first, 're-encoded instead of reusing'\n"
        % str(REPO)
    )
    at.run()
    assert not at.exception, [str(e) for e in at.exception]


def test_missing_figure_renders_nothing() -> None:
    """A figure file that has gone missing must not take the page down.

    ``validate.py`` already fails the build for a missing figure, so this is
    the belt to that braces: if one appears anyway - a deploy, say, that lands
    before the figures are built - the question still reads.
    """
    at = AppTest.from_string(
        "import sys\n"
        "sys.path.insert(0, %r)\n"
        "from src import ui\n"
        "ui.render_figure({'id': 'x', 'image': 'no-such-figure'})\n" % str(REPO)
    )
    at.run()
    assert not at.exception, [str(e) for e in at.exception]


def main() -> int:
    checks = [
        ("test_render_figure_emits_a_data_uri", test_render_figure_emits_a_data_uri),
        ("test_figures_are_encoded_once_and_reused",
         test_figures_are_encoded_once_and_reused),
        ("test_missing_figure_renders_nothing", test_missing_figure_renders_nothing),
    ]
    failures = []
    for name, fn in checks:
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            failures.append(name)
            print("[FAIL] %s: %s" % (name, exc), file=sys.stderr)
        else:
            print("[ok] %s" % name)
    if failures:
        print("%d failure(s): %s" % (len(failures), ", ".join(failures)),
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())