"""Turn the sound files into a Python module of base64 data URIs.

Why embed them at all. Playing a sound in Streamlit means the browser has to be
handed the audio somehow, and every route to the filesystem has failed here. The
first attempt asked for ``/app/static/sfx/<name>.wav``, which needs
``server.enableStaticServing``; that was enabled, committed, and on the deployed
app the URL still answered 200 with ``text/html`` - 9782 bytes of the single-page
app's own shell, because no static route was registered and the request fell
through to it. The browser got an HTML document where it expected audio, ``play()``
rejected, and the rejection was swallowed. Silent buttons, no error anywhere.

The second attempt put the files in a declared component's directory. The files
then served correctly - verified on the deployed app as ``audio/vnd.wave`` with a
RIFF header and byte counts matching the originals - but the component never
rendered, so nothing played them. Two mechanisms, two different silences.

A data URI removes the question. The audio travels inside the HTML, so there is
no route to register, no config to set, and no component for the browser to fail
to draw. The cost is that the bytes live in a Python file: 100 KB of WAV becomes
roughly 134 KB of base64. That is the trade, made knowingly, because a sound that
never plays is worth nothing.

Run:  python tools/build_sfx.py
Reads: assets/sfx/{correct,celebrate,wrong,tap}.wav
Writes: src/sfx_data.py
"""

from __future__ import annotations

import base64
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets" / "sfx"
OUT = ROOT / "src" / "sfx_data.py"

NAMES = ["tap", "correct", "wrong", "celebrate"]

HEADER = '''"""The interface sounds, embedded. GENERATED - do not edit.

Built by ``tools/build_sfx.py`` from ``assets/sfx/*.wav``. Edit the wav files and
rebuild rather than touching this file, or the next run will overwrite you.

Each value is a complete ``data:`` URI, so it can go straight into an ``<audio>``
``src`` attribute with no server, no path and no configuration. See that script for
why the sounds are embedded instead of served.
"""

SOUNDS = {
'''


def build() -> int:
    missing = [n for n in NAMES if not (SRC / (n + ".wav")).exists()]
    if missing:
        print("Missing sound files in %s: %s" % (SRC, ", ".join(missing)), file=sys.stderr)
        print("Run tools/make_sfx.py first.", file=sys.stderr)
        return 2

    lines = [HEADER]
    total = 0
    for name in NAMES:
        raw = (SRC / (name + ".wav")).read_bytes()
        total += len(raw)
        uri = "data:audio/wav;base64," + base64.b64encode(raw).decode("ascii")
        lines.append('    "%s": "%s",\n' % (name, uri))
        print("  %-10s %7.1f KB -> %7.1f KB base64"
              % (name, len(raw) / 1024, len(uri) / 1024))
    lines.append("}\n")

    OUT.write_text("".join(lines), encoding="utf-8")

    written = OUT.stat().st_size
    print("\n%d sounds, %.0f KB of wav -> %s (%.0f KB of source)"
          % (len(NAMES), total / 1024, OUT.relative_to(ROOT), written / 1024))
    return 0


if __name__ == "__main__":
    raise SystemExit(build())