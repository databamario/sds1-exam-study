// Progress storage component.
//
// Progress used to live in a SQLite file beside the app. That is fine on one
// machine and wrong on a deployed one: the file belongs to the app rather than
// to the person using it, so on a shared deployment everyone's history lands in
// the same table and the progress screen shows numbers that are not yours. The
// cloud disk is also ephemeral, so the history vanishes at the next deploy.
//
// Browser local storage fixes both, with no server and no account. The price is
// that progress belongs to one browser: study on the laptop and it is there, and
// it does not follow you to the phone.
//
// Why this is a component and not components.html: components.html can reach the
// same storage - it is same-origin and it persists, which was tested rather than
// assumed - but it cannot send a value back to Python. Progress has to be read,
// because the progress screen is built from these numbers, so it needs a return
// channel.
//
// There is no React and no build step. Streamlit's component API is a
// postMessage protocol and this speaks it directly, which is why the bundle is
// one plain file with no toolchain behind it: a Streamlit deploy runs
// `streamlit run`, never `npm install`, so anything that had to be compiled would
// be a liability on the cloud.
//
// Protocol, apiVersion 1:
//   out  streamlit:componentReady      once, on load
//   in   streamlit:render              carries args on every script run
//   out  streamlit:setComponentValue   carries the stored progress back
//   out  streamlit:setFrameHeight      this component draws nothing
//
// The blob has three fields: attempts (graded answers), prefs (settings such as
// sound on/off) and exam (a mock exam in progress). exam is null when there is
// none. It survives the attempt trim on purpose - the ceiling exists to stop
// the answer log growing forever, and an exam you are sitting is not that.

(function () {
  "use strict";

  var KEY = "sds1-progress-v1";
  var MAX_ATTEMPTS = 20000; // a ceiling, not a policy

  function readBlob() {
    try {
      var raw = window.localStorage.getItem(KEY);
      if (!raw) return { attempts: [], prefs: {}, exam: null };
      var parsed = JSON.parse(raw);
      return {
        attempts: Array.isArray(parsed.attempts) ? parsed.attempts : [],
        prefs:
          parsed.prefs && typeof parsed.prefs === "object" ? parsed.prefs : {},
        exam:
          parsed.exam && typeof parsed.exam === "object" ? parsed.exam : null,
      };
    } catch (e) {
      // A corrupt or unreadable value must not take the app down. Start clean.
      return { attempts: [], prefs: {}, exam: null };
    }
  }

  function writeBlob(blob) {
    if (blob.attempts.length > MAX_ATTEMPTS) {
      blob.attempts = blob.attempts.slice(blob.attempts.length - MAX_ATTEMPTS);
    }
    try {
      window.localStorage.setItem(KEY, JSON.stringify(blob));
    } catch (e) {
      // Quota exceeded, or private browsing. The Python-side mirror still has
      // the value for this session, so the app carries on rather than throwing.
    }
    return blob;
  }

  function applyOp(blob, op, payload) {
    if (op === "record") blob.attempts.push(payload);
    else if (op === "reset") blob.attempts = [];
    else if (op === "set_pref") blob.prefs[payload.name] = String(payload.value);
    else if (op === "set_exam") blob.exam = payload || null;
    return blob;
  }

  function send(type, extra) {
    var msg = { isStreamlitMessage: true, type: type };
    for (var k in extra) if (Object.prototype.hasOwnProperty.call(extra, k)) msg[k] = extra[k];
    window.parent.postMessage(msg, "*");
  }

  window.addEventListener("message", function (event) {
    if (!event.data || event.data.type !== "streamlit:render") return;
    var args = event.data.args || {};
    var blob = readBlob();
    if (args.op && args.op !== "read") blob = writeBlob(applyOp(blob, args.op, args.payload));
    // Always hand back the current state, so Python reads a whole picture
    // rather than having to reason about what a call changed.
    send("streamlit:setComponentValue", { value: blob, dataType: "json", fromUi: true });
  });

  send("streamlit:setFrameHeight", { height: 0 });
  send("streamlit:componentReady", { apiVersion: 1 });
})();