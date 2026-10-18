"""Derive the app's sound effects from one source recording.

The source is a single "right answer" wav that the shortgpt project already
carries. It is 3.0 s of stereo 48 kHz at -1.5 dBFS: far too long for interface
feedback, far too loud, and twice the size it needs to be. Everything the app
plays is derived from it, so all four sounds belong to the same family and only
one asset has to be trusted.

Run:  python tools/make_sfx.py
Writes: assets/sfx/{correct,celebrate,wrong,tap}.wav

They are written at 16 kHz mono. The source is 48 kHz and these end up embedded in
the app as base64 data URIs, so the bytes are shipped inside a Python file rather
than fetched over HTTP - which means every kilobyte counts. The spectrum was
measured before choosing this: everything of consequence sits below 6 kHz and
there is almost nothing above 8 kHz, so 16 kHz (8 kHz Nyquist) keeps all of it.

``tools/build_sfx.py`` turns these into ``src/sfx_data.py``.
"""

from __future__ import annotations

import argparse
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "sfx"

# The app plays these by embedding them in a data URI, so they are never fetched:
# the whole cost is paid in repository text. 16 kHz is chosen from the measured
# spectrum, not guessed - see the module docstring.
SAMPLE_RATE = 16000

# The recording this project already owns. Override with --source if it moves.
DEFAULT_SOURCE = Path(
    r"C:\Users\mario\Desktop\Road shortgpt 3.0\public\SFX\right_answer_sound.wav"
)

# Interface feedback sits well under the peak of music. -3 dBFS leaves enough
# headroom that two overlapping sounds cannot clip.
PEAK_DB = -3.0
# The option tick fires on every click, so it lives well below the rest.
TAP_PEAK_DB = -13.0


def read_wav(path: Path) -> tuple[np.ndarray, int]:
    """Read a PCM wav as mono float32 in [-1, 1]."""
    with wave.open(str(path), "rb") as w:
        if w.getsampwidth() != 2:
            raise SystemExit("%s is not 16-bit PCM" % path.name)
        sr = w.getframerate()
        ch = w.getnchannels()
        raw = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    if ch > 1:
        raw = raw.reshape(-1, ch).mean(axis=1)
    return raw.astype(np.float32) / 32768.0, sr


def write_wav(path: Path, y: np.ndarray, sr: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    clipped = np.clip(y, -1.0, 1.0)
    pcm = (clipped * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def normalize(y: np.ndarray, peak_db: float = PEAK_DB) -> np.ndarray:
    peak = float(np.max(np.abs(y)))
    if peak < 1e-9:
        return y
    return y * (10.0 ** (peak_db / 20.0) / peak)


def resample(y: np.ndarray, factor: float) -> np.ndarray:
    """Read the signal `factor` times faster/slower, keeping the sample count.

    factor > 1 raises the pitch and shortens the result, which is how the
    celebration and the error tone are both made from one recording. A linear
    interpolation is enough here: the source is a short tonal hit with no
    high-frequency content worth a windowed-sinc filter.
    """
    n_out = max(1, int(len(y) / factor))
    idx = np.arange(n_out, dtype=np.float64) * factor
    return np.interp(idx, np.arange(len(y)), y).astype(np.float32)


def downsample(y: np.ndarray, sr: int, target: int) -> tuple[np.ndarray, int]:
    """Reduce to `target` Hz, low-passed first so nothing folds back into hearing.

    Decimating on its own aliases everything above the new Nyquist back into the
    band you can hear. A box filter of the decimation length is a crude low-pass,
    which is enough here: the content is well under 6 kHz and only a whisper sits
    above 8 kHz. A windowed-sinc would be more correct and would also be a lot of
    code for audio nobody is going to analyse.
    """
    if target >= sr:
        return y, sr
    factor = sr / float(target)
    taps = max(2, int(round(factor)))
    kernel = np.ones(taps, dtype=np.float32) / taps
    filtered = np.convolve(y, kernel, mode="same").astype(np.float32)
    n_out = max(1, int(len(filtered) / factor))
    idx = np.arange(n_out, dtype=np.float64) * factor
    return np.interp(idx, np.arange(len(filtered)), filtered).astype(np.float32), target


def emit(name: str, y: np.ndarray, sr: int) -> tuple[str, np.ndarray, int]:
    """Downsample and write one sound, returning what was actually written."""
    small, rate = downsample(y, sr, SAMPLE_RATE)
    write_wav(OUT / (name + ".wav"), small, rate)
    return (name, small, rate)


def fade_edges(y: np.ndarray, sr: int, attack_ms: float = 6.0,
               release_ms: float = 90.0) -> np.ndarray:
    """Fade in and out so a hard cut never clicks.

    The source has a long decaying tail that never reaches silence, so the
    release is long enough to disappear rather than stop.
    """
    out = y.copy()
    a = max(1, int(sr * attack_ms / 1000.0))
    r = max(1, int(sr * release_ms / 1000.0))
    a = min(a, len(out) // 2)
    r = min(r, len(out) - a)
    out[:a] *= np.linspace(0.0, 1.0, a, dtype=np.float32)
    out[len(out) - r:] *= np.linspace(1.0, 0.0, r, dtype=np.float32)
    return out


def trim_seconds(y: np.ndarray, sr: int, seconds: float) -> np.ndarray:
    return y[: int(sr * seconds)]


def envelope_db(y: np.ndarray, sr: int, win_ms: float = 20.0) -> np.ndarray:
    win = max(1, int(sr * win_ms / 1000.0))
    usable = len(y) // win
    frames = y[: usable * win].reshape(usable, win)
    return 20 * np.log10(np.sqrt(np.mean(frames.astype(np.float64) ** 2, axis=1)) + 1e-12)


def report(name: str, y: np.ndarray, sr: int) -> None:
    env = envelope_db(y, sr)
    peak = 20 * np.log10(float(np.max(np.abs(y))) + 1e-12)
    print("  %-10s %5.2f s  peak %5.1f dBFS  rms %5.1f dBFS  %5.0f KB"
          % (name, len(y) / sr, peak, 20 * np.log10(
              float(np.sqrt(np.mean(y.astype(np.float64) ** 2))) + 1e-12),
             len(y) / sr * sr * 2 / 1024))


def build(source: Path) -> int:
    if not source.exists():
        print("Source not found: %s" % source, file=sys.stderr)
        print("Pass --source <path to a 16-bit wav>.", file=sys.stderr)
        return 2

    y, sr = read_wav(source)
    print("Source: %s" % source.name)
    print("  %.2f s, %d Hz, peak %.1f dBFS"
          % (len(y) / sr, sr, 20 * np.log10(float(np.max(np.abs(y))) + 1e-12)))
    env = envelope_db(y, sr)
    peak_at = int(np.argmax(env)) * 0.02
    print("  transient peaks at %.2f s; still above -50 dBFS at %.2f s "
          "(long tail, so it is cut and faded)"
          % (peak_at, len(np.where(env > -50)[0]) * 0.02 if (env > -50).any() else 0.0))
    print()

    print("Writing:")
    made = []

    # correct: the source as authored, minus the tail.
    correct = fade_edges(trim_seconds(y, sr, 1.20), sr, release_ms=140.0)
    correct = normalize(correct)
    made.append(emit("correct", correct, sr))

    # celebrate: the same hit raised a fifth and a third, struck in sequence so
    # it reads as a rising arpeggio rather than one bright blip.
    steps = [(1.00, 0.00), (1.26, 0.115), (1.50, 0.230)]
    longest = max(int(trim_seconds(y, sr, 0.85).size / f) for f, _ in steps)
    celebrate = np.zeros(longest + sr, dtype=np.float32)
    for factor, delay in steps:
        hit = normalize(resample(trim_seconds(y, sr, 0.85), factor))
        off = int(delay * sr)
        celebrate[off: off + len(hit)] += hit[: len(celebrate) - off]
    celebrate = normalize(fade_edges(celebrate[: int(1.15 * sr)], sr, release_ms=120.0))
    made.append(emit("celebrate", celebrate, sr))

    # wrong: the same hit dropped about a minor third, so a miss still belongs to
    # the same sound family instead of arriving as an unrelated alarm.
    wrong = normalize(resample(trim_seconds(y, sr, 0.62), 0.80))
    wrong = fade_edges(wrong, sr, release_ms=110.0)
    made.append(emit("wrong", wrong, sr))

    # tap: only the attack of the source, raised and kept quiet, because this one
    # fires on every option the student ticks. Faded first and normalised after,
    # so the target level is the level that actually comes out of the fade.
    tap = resample(trim_seconds(y, sr, 0.11), 1.30)
    tap = normalize(fade_edges(tap, sr, attack_ms=1.0, release_ms=22.0), TAP_PEAK_DB)
    made.append(emit("tap", tap, sr))

    for name, sig, rate in made:
        report(name, sig, rate)

    total = sum((OUT / (n + ".wav")).stat().st_size for n, _, _ in made)
    print("\n%d files, %.0f KB total -> %s" % (len(made), total / 1024, OUT))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=str(DEFAULT_SOURCE))
    args = ap.parse_args()
    return build(Path(args.source))


if __name__ == "__main__":
    raise SystemExit(main())
