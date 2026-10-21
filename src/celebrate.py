"""Feedback effects: streak counting, confetti and interface sound.

The confetti is plain CSS injected into the page, not an iframe. That choice is
deliberate: ``components.html`` renders a sandboxed iframe, and inside a
zero-height iframe there is no viewport, so a ``position: fixed`` overlay has
nothing to be fixed against and never shows. Markup added through
``st.markdown`` lands in the page itself, so ``position: fixed`` overlays
everything, ``pointer-events: none`` keeps it from swallowing a click, and
Streamlit discards it on the next rerun.

The particle physics is a port of the ConfettiCelebration component from the
remotion project: the same mulberry32 seeding and the same decay, gravity and
lifetime curve, with the numbers baked into CSS keyframes so there is no
JavaScript and no animation library to load.
"""

from __future__ import annotations

import os
import sys

import streamlit as st
import streamlit.components.v1 as components

from .sfx_data import SOUNDS as _SOUND_URI

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The streak the celebration waits for, as chosen: sound on every correct
# answer, confetti only once this many land in a row.
CELEBRATE_AT = 5

PALETTE = ["#22c55e", "#3b82f6", "#eab308", "#ec4899", "#8b5cf6", "#f97316"]

# The confetti overlay, emitted once per celebration together with its particles.
_CONFETTI_CSS = """
<style>
  @keyframes sds-confetti-fall {
    0%   { transform: translate(-50%,-50%) rotate(0deg);    opacity: 0; }
    8%   { opacity: 1; }
    82%  { opacity: 1; }
    100% { transform: translate(calc(-50% + var(--dx)), calc(-50% + var(--dy)))
                     rotate(var(--spin));                     opacity: 0; }
  }
  .sds-confetti {
    position: fixed; inset: 0; overflow: hidden;
    pointer-events: none; z-index: 9999;
  }
  .sds-confetti i {
    position: absolute;
    top: var(--top); left: var(--left);
    width: var(--size); height: calc(var(--size) * .62);
    background: var(--color); border-radius: 2px;
    animation: sds-confetti-fall var(--dur) cubic-bezier(.18,.7,.4,1) forwards;
    animation-delay: var(--delay);
  }
  /* Respect the system setting: no movement if the reader has asked for none. */
  @media (prefers-reduced-motion: reduce) {
    .sds-confetti { display: none; }
  }
</style>
"""


def _mulberry32(seed: int):
    """The same PRNG the remotion component uses, so a seed reproduces a burst."""
    state = seed & 0xFFFFFFFF

    def rng() -> float:
        nonlocal state
        state = (state + 0x6D2B79F5) & 0xFFFFFFFF
        t = state
        t = ((t ^ (t >> 15)) * (t & 0x1 | 1)) & 0xFFFFFFFF
        t ^= (t + ((t ^ (t >> 7)) * (t & 0x61 | 1))) & 0xFFFFFFFF
        t &= 0xFFFFFFFF
        t ^= t >> 14
        return (t & 0xFFFFFFFF) / 4294967296.0

    return rng


def _burst(seed: int, count: int) -> list[str]:
    """One particle as a CSS custom-property block, falling across the top."""
    rng = _mulberry32(seed)
    parts = []
    for _ in range(count):
        # Launched from the top, spread across the width, drifting downwards.
        left = rng() * 100.0
        top = -4.0 - rng() * 6.0
        size = 6.0 + rng() * 9.0
        color = PALETTE[int(rng() * len(PALETTE))]
        # dx is a share of the viewport width, dy of its height.
        dx = (rng() - 0.5) * 26.0
        dy = 60.0 + rng() * 55.0
        spin = (rng() - 0.5) * 1440.0
        dur = 1.5 + rng() * 0.9
        delay = rng() * 0.35
        parts.append(
            '<i style="--left:%.1f%%;--top:%.1f%%;--size:%.1fpx;--color:%s;'
            "--dx:%.1fvw;--dy:%.1fvh;--spin:%.0fdeg;--dur:%.2fs;--delay:%.2fs\"></i>"
            % (left, top, size, color, dx, dy, spin, dur, delay)
        )
    return parts


def confetti_html(intensity: int = 1, seed: int = 0) -> str:
    """Confetti sized by how long the streak is, so it visibly escalates."""
    if intensity <= 0:
        return ""
    count = 46 + min(intensity, 8) * 16
    particles = _burst(seed or 1, count)
    return (_CONFETTI_CSS
            + '<div class="sds-confetti">' + "".join(particles) + "</div>")


def celebrate(intensity: int = 1, seed: int = 0) -> None:
    st.markdown(confetti_html(intensity, seed), unsafe_allow_html=True)


_SOUND_VOLUME = {
    "correct": 0.55,
    "celebrate": 0.7,
    "wrong": 0.45,
    "tap": 0.3,
}


_PENDING_KEY = "_sds_pending_sound"
_SEQ_KEY = "_sds_sound_seq"
_DRAWN_KEY = "_sds_sound_drawn"

_PLAYER = """
<audio id="sds-sfx" preload="auto" src="%s"></audio>
<script>
  var a = document.getElementById('sds-sfx');
  a.volume = %s;
  a.currentTime = 0;
  var p = a.play();
  if (p && p.catch) { p.catch(function () {}); }
</script>
"""


def play(name: str, enabled: bool = True) -> None:
    """Queue one short effect, to be drawn by :func:`flush`.

    Queueing rather than rendering is the whole trick, and it was found by
    measurement rather than reasoning. The identical ``components.html`` call was
    run from two places in the same process: called at the top level of the script
    it produced an iframe holding a decoded ``<audio>`` - ``readyState`` 4, no
    error, duration 0.085 s, matching the source wav exactly. Called from deep
    inside the question-rendering helpers it produced no iframe at all, no error
    and no sound. Same function, same arguments. So the sound is queued here, and
    drawn from the one place it is known to work.

    The audio rides inside the markup as a ``data:`` URI, which is the third
    mechanism tried here. The first two are worth recording so the afternoon is
    not spent a fourth time.

    It used to load from ``/app/static/sfx/<name>.wav``, which needs Streamlit's
    ``server.enableStaticServing``. That was enabled and committed, and on the
    deployed app the URL still answered 200 with ``text/html`` - 9782 bytes of the
    single-page app's own shell, because no static route was registered and the
    request fell through to it. The browser received an HTML document where it
    expected audio, ``play()`` rejected, and the rejection was swallowed. Silent
    buttons, and nothing anywhere said why.

    The files then moved into a declared component's directory, which does serve
    them: verified on the deployed app as ``audio/vnd.wave`` with RIFF headers and
    byte counts matching the originals. That was not the problem either, which is
    what took the longest to accept.

    A data URI needs no route, no configuration and no component: the audio
    arrives with the page. The cost is size - 100 KB of wav becomes 135 KB of
    base64 - which is worth paying for a sound that cannot fail to be playable.
    """
    if not enabled or name not in _SOUND_VOLUME:
        return
    seq = st.session_state.get(_SEQ_KEY, 0) + 1
    st.session_state[_SEQ_KEY] = seq
    st.session_state[_PENDING_KEY] = (seq, name)


def flush() -> None:
    """Draw the queued sound, once, from the top level of the script run.

    Nothing is cleared when the sound is drawn. Answering a question ends with
    ``st.rerun()``, which unwinds the script immediately - so a run that queues a
    sound usually never reaches the end of the file, and a queue that was emptied
    at that point would take the sound down with it. Instead each queued sound
    carries a sequence number, and it is considered drawn only once that number has
    actually been rendered. The run after the rerun draws it.

    A sound queued but never drawn would otherwise repeat forever on every
    subsequent run, which is why the drawn marker exists rather than just leaving
    the queue in place.

    ``.play()`` has its rejection swallowed. Browsers refuse to start audio before
    the reader has interacted with the page, and that has to degrade to silence
    rather than raise.
    """
    pending = st.session_state.get(_PENDING_KEY)
    if pending is None:
        return
    seq, name = pending
    if st.session_state.get(_DRAWN_KEY) == seq:
        return
    uri = _SOUND_URI.get(name)
    if not uri:
        print("[celebrate] no embedded audio for %r" % (name,), file=sys.stderr)
        st.session_state[_DRAWN_KEY] = seq
        return
    # A stable per-sequence key so Streamlit's component tracker does not
    # tear down and rebuild the iframe on every rerun. Without it, any widget
    # interaction (Check answer, Next, a chip) replaces the audio element
    # mid-playback and the sound cuts. The bump keyed on seq makes each new
    # sound its own component while keeping the old one alive until the new
    # one is drawn.
    components.html(_PLAYER % (uri, _SOUND_VOLUME[name]), height=0,
                    key="sds-sfx-%d" % seq)
    st.session_state[_DRAWN_KEY] = seq


def streak_upto(queue: list[dict], history: dict, done: dict, index: int) -> int:
    """Consecutive full marks ending at ``index``, counting back through the queue.

    Derived from state rather than accumulated in a counter, so pressing Back and
    coming forward again cannot double-count, and a re-attempt that improves the
    mark updates the streak on its own.
    """
    count = 0
    for i in range(index, -1, -1):
        q = queue[i]
        entry = done.get(q["id"])
        score = entry["score"] if entry is not None else history.get(q["id"], 0.0)
        if score >= q["points"] - 1e-9:
            count += 1
        else:
            break
    return count


def should_celebrate(streak: int) -> bool:
    return streak >= CELEBRATE_AT
