"""The browser half of the storage layer, checked against the real files.

``src/progress.py`` and ``_progress_component/index.js`` each hold their own
copy of the blob handling: one in a Python string that becomes a ``<script>``,
the other in the component's JavaScript. They have to agree, and they cannot be
tested by running them - AppTest does not execute JavaScript, and there is no
build step to compile one from the other. So the agreement is asserted here
instead, on the text.

This is not a style gate. It exists because the two copies have already drifted
once: ``exam`` was added to both, and a rename in one would leave the other
writing a key nothing reads - which looks like working code right up until a
refresh loses something. Every field and every operation name has to appear in
both files, and the op names in the Python string have to be exactly the op
names the JavaScript handles.

Run via ``tools/check_all.py`` (the ninth gate) or on its own:
``python tools/test_storage_parity.py``.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src import progress  # noqa: E402

JS_PATH = REPO / "_progress_component" / "index.js"

# Every key the blob is made of. Both copies must know all three, or one of
# them silently drops a field on the way through.
FIELDS = ("attempts", "prefs", "exam")

# Every op the Python side can send. Each one has a matching branch in the
# component's applyOp, and nothing may be sent that is not handled there.
OPS = ("record", "reset", "set_pref", "set_exam")


def _python_blob_js() -> str:
    """The JavaScript embedded in progress.py's _write()."""
    from src import progress as p
    import inspect
    src = inspect.getsource(p._write)
    return src


def _js() -> str:
    return JS_PATH.read_text(encoding="utf-8")


def test_fields_present_in_both_copies() -> None:
    py, js = _python_blob_js(), _js()
    for field in FIELDS:
        if field not in py:
            raise AssertionError(
                "progress.py's localStorage script never mentions %r, so it "
                "drops that field on write" % field
            )
        if field not in js:
            raise AssertionError(
                "index.js never mentions %r, so it drops that field on read"
                % field
            )


def test_both_copies_default_exam_to_null() -> None:
    """An absent or unparseable exam must read as null, never as a stray dict.

    Both readBlob() and the inline read() hand back a literal default when
    storage is empty. If one of them returns {} for exam and the other returns
    null, then a first-ever visit and a torn write disagree about the shape,
    and progress.read_exam() has to guess which one it got.
    """
    py, js = _python_blob_js(), _js()
    if "exam: null" not in py:
        raise AssertionError("progress.py's default blob has no 'exam: null'")
    if "exam: null" not in js:
        raise AssertionError("index.js's default blob has no 'exam: null'")


def test_ops_sent_are_all_handled() -> None:
    """Every op progress.py can send must be handled by the component.

    ``applyOp`` is a plain if/else chain with no default, so an unhandled op is
    not an error - it is a silent no-op. The write appears to succeed and the
    field never changes.
    """
    js = _js()
    apply_op = js[js.index("function applyOp"):js.index("function send")]
    for op in OPS:
        if '"%s"' % op not in apply_op and "'%s'" % op not in apply_op:
            raise AssertionError(
                "progress.py can send op %r but index.js's applyOp does not "
                "handle it, so the write would be silently dropped" % op
            )


def test_every_op_sent_is_in_the_known_list() -> None:
    """The Python side may only send ops this test knows about.

    Without this, a new op added to _write and to the component would pass the
    test above while nothing here had recorded that it exists.
    """
    py = _python_blob_js()
    sent = set(re.findall(r'_write\(\s*"([a-z_]+)"', py))
    sent.add("read")  # hydrate() passes op="read" as a keyword, not via _write
    unknown = sent - set(OPS) - {"read"}
    if unknown:
        raise AssertionError(
            "progress.py sends ops this gate does not know about: %s. Add them "
            "to OPS here and to index.js, or the write is unverifiable."
            % ", ".join(sorted(unknown))
        )


def test_reset_keeps_the_exam() -> None:
    """Clearing the answer log must not clear an exam in progress.

    ``reset`` is the progress screen's "start again" button. An exam you are
    halfway through is not a log entry, and wiping it as a side effect of
    tidying history would be the same silent loss as never saving it.
    """
    js = _js()
    apply_op = js[js.index("function applyOp"):js.index("function send")]
    reset_branch = apply_op[apply_op.index('"reset"'):
                            apply_op.index('"set_pref"')]
    if "exam" in reset_branch:
        raise AssertionError(
            "index.js's reset op touches exam; resetting progress must leave "
            "an exam in progress alone"
        )


def main() -> int:
    checks = [
        ("test_fields_present_in_both_copies", test_fields_present_in_both_copies),
        ("test_both_copies_default_exam_to_null", test_both_copies_default_exam_to_null),
        ("test_ops_sent_are_all_handled", test_ops_sent_are_all_handled),
        ("test_every_op_sent_is_in_the_known_list",
         test_every_op_sent_is_in_the_known_list),
        ("test_reset_keeps_the_exam", test_reset_keeps_the_exam),
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