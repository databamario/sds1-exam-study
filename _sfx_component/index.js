// Sound effect component.
//
// These four sounds used to be loaded from `/app/static/sfx/<name>.wav`, which
// depends on Streamlit's `server.enableStaticServing`. That is on, and it is in
// the committed config, and it still did not work on the deployed app: the URL
// came back 200 but with `text/html`, 9782 bytes, because no static route was
// registered and the request fell through to the single-page app's own shell. So
// the browser got an HTML document where it expected audio, `play()` rejected,
// and the rejection was swallowed - which is why the buttons were silent and
// nothing anywhere said why. Two lessons, both paid for in an hour: a silent
// failure is the expensive kind, and a default worth double-checking is not a
// default to rely on.
//
// A declared component serves its own directory, relative to wherever it is
// mounted, so `./tap.wav` resolves without anyone configuring a static path. It
// is the mechanism already proven on the cloud by the progress component, which
// is the reason to reuse it rather than invent a second one.
//
// There is no React and no build step, for the reason given in index.html.
//
// Protocol, apiVersion 1:
//   out  streamlit:componentReady      once, on load
//   in   streamlit:render              carries the sound name and volume
//   out  streamlit:setFrameHeight      this component draws nothing
//
// It deliberately never sends setComponentValue: a component that reports a value
// makes Streamlit rerun the script, and a sound must not cost a rerun. Python
// calls this with no `key` for the same reason.

(function () {
  "use strict";

  // Mirrors _SOUND_VOLUME in src/celebrate.py. Python validates the name before
  // it is sent, and this checks again, so a bad value can never become an
  // arbitrary path no matter what reaches the function.
  var KNOWN = { tap: true, correct: true, wrong: true, celebrate: true };

  var audio = null;

  function send(type, extra) {
    var msg = { isStreamlitMessage: true, type: type };
    for (var k in extra) {
      if (Object.prototype.hasOwnProperty.call(extra, k)) msg[k] = extra[k];
    }
    window.parent.postMessage(msg, "*");
  }

  window.addEventListener("message", function (event) {
    if (!event.data || event.data.type !== "streamlit:render") return;

    var args = event.data.args || {};
    var name = args.name;
    if (typeof name !== "string" || !KNOWN[name]) return;

    if (!audio) {
      audio = new Audio();
      audio.preload = "auto";
    }
    audio.volume = typeof args.volume === "number" ? args.volume : 0.5;
    // Rewinding matters: a repeat of the same sound within one session would
    // otherwise have already finished, and a finished element does not replay
    // when its src is reassigned to the same value.
    audio.src = "./" + name + ".wav";
    audio.currentTime = 0;

    // Browsers refuse to start audio before the reader has interacted with the
    // page, and they reject rather than throw. That has to degrade to silence:
    // a missing sound is not worth taking the app down for. It also means a
    // sound can never be the first thing a page does, which is why playing one
    // is always something the reader just triggered.
    var p = audio.play();
    if (p && p.catch) p.catch(function () {});
  });

  send("streamlit:setFrameHeight", { height: 0 });
  send("streamlit:componentReady", { apiVersion: 1 });
})();