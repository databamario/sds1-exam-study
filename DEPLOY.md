# Deploy plan

How this app goes from "26 commits on my laptop" to "a link my classmates can
use". Written down before starting, because the order matters more than it
looks: doing these in the wrong order means pushing and deploying three times
instead of once.

## Status

| Phase | State |
|---|---|
| 1 — finish the citation review | **in progress**, the only open work |
| 2 — progress in the browser | **done** |
| 3 — push the repo | **done** 16 Oct 2025 |
| 4 — deploy to Streamlit | **done**, live on Community Cloud |
| 5 — interface sounds | **done**, after an incident. See below |

The app is live, public, and has no build step of any kind. The rest of this file
is the original plan, annotated where reality turned out to differ from it. The
sections that are most likely to mislead are Phase 2 (it describes a design that
was never built) and the incident report at the end.

## Decisions already taken

| Question | Decision |
|---|---|
| Repo visibility | **Public** |
| Legal risk of publishing | **None.** No PDF, no third-party material, no exam text in the repo (checked: `git ls-files` has 57 files, zero `.pdf`) |
| Progress storage | **Per browser**, via a custom component writing `localStorage`. No server, no accounts |
| Cross-device progress | **Not wanted.** Study on the laptop, progress is in the laptop |
| Existing local progress | **Starting from zero.** `progress.sqlite3` is not migrated |
| Two GitHub accounts | `databamario` is active for `gh`, protocol HTTPS, scopes include `repo` |

Why the repo can be public without worrying: 181 of the 243 questions were
written from scratch against publicly taught statistics topics; the other 62
are rewritten, not transcribed, from a paper the professor handed out for study.
The lecture PDFs and the exam PDF are **not in the repo** and never were.

## Phase 1 - finish the citation review (in progress)

The bank is 243 questions. `tools/validate.py` proves every citation names a
real file and a page inside it, which is now true of all 243. But a citation
can be well formed and still point at the wrong slide.

Read by hand so far: **113**. Found and fixed **34** real errors. Remaining:
**~130**, grouped by how badly the cited slide matches the question:

```
band   score      left
A      < 0.10       done
B      0.10-0.15    done
C      0.15-0.20    done
D      0.20-0.30    done
E      > 0.30      ~99   (27 read so far)
```

Band E is the largest and the weakest-signal: a high score means the slide
*does* match, so it is the least likely to hide an error. It is read last, and
it is read anyway.

Per batch: read with `python tools/show_citation.py --band LO HI`, fix only what
the slide text proves, re-derive the correct page from the PDF rather than from
any table written earlier, run the full gate suite, commit.

Band E is half the remaining work and has the weakest signal. It is read anyway,
because band C returned 0/11 and the very next band returned 3/8: the trend
already lied once.

One improvement worth making first: most of the errors found so far are not
"wrong page" but "right page, content on the *next* slide". That is mechanically
detectable, so `tools/verify_citations.py` should learn to rank by **proximity**
- does the decisive term appear on the cited page, or on the page after it -
rather than by word overlap alone.

## Phase 2 - progress in the browser  **DONE**

Everything below the banner is the plan as written before the work. It describes a build
pipeline that was never needed and a component shape that is not what shipped: the shipped
component is **two hand-written files, `index.html` and `index.js`, with no bundler and no
`dist/`**. Read it for the reasoning, not for the file layout. What actually shipped is in
`_progress_component/`.

### The problem

`src/progress.py` writes `progress.sqlite3` into the repo root:

```python
DB_PATH = Path(__file__).resolve().parents[1] / "progress.sqlite3"
```

Local and sensible. On a shared cloud deployment it is wrong twice over:

1. **Everyone shares one history.** The file is per-app, not per-user, so my
   progress and a classmate's would interleave in the same statistics view.
2. **It is wiped on every redeploy.** Cloud Community's disk is ephemeral.

The file is gitignored, so it is not committed - which means today the progress
feature only works for whoever is sitting at my desk.

### The shape of the fix

`progress.py` is a thin SQLite layer behind a small interface. Every function
takes a `conn` and issues SQL. Nothing above it knows SQLite exists:

```
connect()       app.py:49
record()        ui.py:637, ui.py:707, mock_exam.py:178
attempts_for()  read, to filter out questions already answered
by_lecture()    src/views/progress_view.py:23
overall()       src/views/progress_view.py:12
reset()         src/views/progress_view.py:47
get_pref/set_pref   app.py:74-81   the sound toggle
```

So the change is to swap the implementation of these functions and leave the
eight call sites untouched. That is the whole reason this is a contained change
rather than a rewrite.

### Two candidate mechanisms, and one must be tested first

`src/celebrate.py` already uses `components.html` for the sounds. Its docstring
says *"``components.html`` renders a sandboxed iframe"*, which raises the
question of whether an iframe can reach the parent's `localStorage`.

**Tested, 16 October 2025, against Streamlit 1.45.1 in a real browser.** The
answer changes the plan, so it is worth recording exactly:

- A throwaway Streamlit page rendered `components.html` whose script wrote a
  marker to `window.localStorage`.
- Read back from the **main** document: the marker was there.
- After a full page reload: the marker was still there.
- The iframe reported `window.parent !== window` and a *second* marker written
  through `window.parent.localStorage` also appeared in the page's storage.

So `components.html` **is** same-origin and reaches the browser's real,
persistent `localStorage`. The "sandboxed iframe" wording in the docstring does
not prevent it. No `declare_component`, no webpack, no React, no build step on
the cloud.

### But reading it back needs a return channel

One thing the probe settled only halfway. Writing *into* `localStorage` from
`components.html` works. Getting data *out* to Python does not: `components.html`
has no return value, and `src/progress.py` has to read as well as write -
`attempts_for()`, `by_lecture()`, `overall()` and `export_rows()` all read, and
the progress screen is built from those numbers.

Python therefore needs a channel back from the browser, and only a declared
component has one: `model.setComponentValue()` returns a value to the next
script run.

So the design is a small declared component for reads, and `components.html`
would not have sufficed. Two consequences for the cloud deploy:

- ~~The component must be **built and its `dist/` committed**, so the deploy needs
  no `npm install` and no build step. Node 22 and npm 10.9.2 are available
  locally, so the bundle is produced here and checked in.~~ **Not what happened.**
  No bundler was needed. The component is two plain files that Streamlit serves
  as-is, so there is no build step and nothing to regenerate.
- `components.html` stayed in use for the sounds at the time of this plan. It no
  longer does — see the incident report below.

Still to confirm by running the real thing, not the probe: whether the
component's return arrives in time for the next question. A declared component
returns on the *following* script run, so `record()` and `attempts_for()` must
not be called in the same run or the screen would show one question stale.
Worth checking against the practice loop before trusting it.

### What is involved

A search of the call sites turned up less surface than the estimate assumed.
Of the nine functions, **two are dead code**:

```
attempts_for   never called
export_rows    never called
```

They only exist in their own definitions. So the real surface is seven:

```
connect()      app.py:49
record()       ui.py:637, ui.py:707, mock_exam.py:178
by_lecture()   src/views/progress_view.py:23, loader.py:244
overall()      src/views/progress_view.py:12
reset()        src/views/progress_view.py:47
get_pref/set_pref   app.py:74-81, the sound toggle
```

Both dead functions get deleted rather than ported. That also dissolves the lag
worry in part: `attempts_for` was the one reader called in the middle of the
practice loop, and it is not called at all. What is left reads only on the
progress screen, which loads fresh.

The sound toggle is the one interactive read, and a component returns its value
on the *following* script run, so leaving it purely in localStorage would make
the switch take effect one interaction late. The fix is to mirror the live
value in `st.session_state` and treat localStorage as the thing that survives a
restart, which is what it is actually good for.

- A small JS component holding one JSON blob, `{"attempts": [...],
  "prefs": {...}}`, committed with its built `dist/` so no build is needed on
  the cloud.
- `progress.py` rewritten on top of it, keeping the seven function names.
- `localStorage` has no query language, so `by_lecture` becomes a load, a
  group-by in Python, and a return. Realistic size: **~110 lines**, against the
  ~130 first estimated once the dead code is removed.
- Tests for the new layer, plus the existing suite kept green.

### What is deliberately not being done

No backend, no database, no user accounts, no sync between devices. Progress
lives in the browser that earned it. That is the trade: one line of code that
does not need a server, in exchange for progress that does not follow you to
your phone. Both were considered and this was the choice.

## Phase 3 - one push  **DONE 16 October 2025**

```
repo     databamario/sds1-exam-study
visibility  PUBLIC
commits  30 of 30
files    58 of 58
https://github.com/databamario/sds1-exam-study
```

Two things went as predicted, and both needed handling rather than retrying:

- `gh repo create` created the repo and then failed with *"Unable to add remote
  origin"*, because `origin` already pointed at the same URL. Re-running `create`
  would have failed with "already exists", so the push was done separately.
- The push needed credentials, so the token went into the remote URL for the
  duration of one push and was removed immediately afterwards. `.git/config` was
  then grepped for `ghp_`/`gh[ous]_` and confirmed clean, and the remote is back
  to the plain URL. The company account's git configuration was never touched:
  no `gh auth setup-git`, no change to `credential.helper`.

Checked on GitHub afterwards, not just assumed: 58 blobs, extensions `.py` 36,
`.png` 10, `.wav` 4, `.md` 2, and one each of `.bat`, `.sh`, `.gitignore`,
`.toml`, `.json`, `.txt`. **No PDF, no SQLite, no `.env`, no secrets** - which is
the point, and is why public was safe.

## Phase 4 - Streamlit  **DONE**

This part needs a browser session with Mario's own account, so it cannot be
automated from here. The app is already deployable-shaped:

```
requirements.txt        one line: streamlit>=1.40
.streamlit/config.toml  DELETED. It existed only to turn on enableStaticServing
                        for the sounds, which does not work. See below.
secrets.toml            does not exist, nothing to leak
paths in src/           all relative via Path(__file__).resolve(), no C:\ anywhere
```

Deployed and live:

```
https://sds1-exam-study-fynxrc3p2g8nhwzxdyclbb.streamlit.app/
```

The app sleeps after a period of inactivity, because the free Community plan
does that. The first visitor after a quiet period waits 20-30 seconds while it
wakes. That is the plan working, not a failure, and it is written up in the
README so nobody reports it as a bug.

Steps at <https://share.streamlit.io>: Deploy, authorise GitHub, pick
`sds1-exam-study`, wait 3-5 minutes for the first build, then set a password in
the app's settings.

**It can be deployed now.** The only thing Phase 2 changes is where progress
lives, and until that lands the app keeps working exactly as it does locally -
the exam practice, the mock exam, the review screens, the figures and the sounds.
What is degraded on the cloud is the progress history: shared between users, and
wiped on redeploy. Worth deploying first and fixing second, so there is a URL to
try before anything else changes.

## What is deliberately not being done

- **Not staying private.** It buys nothing here: there is no material in the
  repo worth hiding, and a private repo cannot be deployed on the free
  Community plan anyway - private sources need a paid plan. Public it is.
- **Not migrating the local progress.** Decided: start from zero.

---

# Incident: the interface sounds were silent in production

Worth more than everything above it. Four mechanisms were tried; the first
three failed for reasons that were not visible from the code, and the fourth
works. If you are about to change anything about sound, or about any asset the
app loads at runtime, read this first.

## Symptom

Working perfectly on a laptop, completely silent on the deployed app. No error,
no exception, nothing in the logs. A correct answer produced no sound at all.

## Attempt 1 - serve the WAVs from `static/`

The obvious design: put the four `.wav` files in `static/sfx/` and turn on
`server.enableStaticServing` in `.streamlit/config.toml`, then point an
`<audio>` tag at them.

What actually happened on the deployed app:

```
GET /app/static/sfx/correct.wav
  200 OK
  content-type: text/html
  content-length: 9782
```

**The app was serving the Streamlit shell to a request for a WAV file.** 9782
bytes of `text/html` is the size of the single-page app, not of a 25 KB audio
file. The file "loaded", decoded nothing, and failed silently.

The obvious first guess is a mount-prefix problem - is it `/app/static/...` or
`app/static/...`, is there a leading slash - and that guess is wrong and
misleading. The path was right. The server simply does not serve that directory
as static content in this configuration, and returns the SPA for anything it
does not recognise rather than a 404.

## Attempt 2 - a declared component

Write a small custom component and have it fetch the WAV. This one got
further, which is what made it the most misleading.

The files *were* served correctly now - `audio/vnd.wave`, a valid RIFF header,
real bytes. So the network layer was finally doing what it should.

But **no iframe appeared in the DOM at all**. No element, no error, no log
line. The component was declared, registered, and simply not rendered.

## Attempt 3 - `components.html` from inside a helper

This is where most of the time went, and where the wrong conclusions came from.

The call site was deep inside the practice loop - `ui.py`, several frames below
the top of the script. `st.components.html(...)` executed, returned, and
produced **no iframe and no error**.

The natural reading is "the sandboxed iframe cannot reach what it needs".
Wrong. The actual rule, confirmed by isolating one call at the top level of the
script:

> **`components.html` only renders an iframe when it is called from the top
> level of the Streamlit script.** Called from a function that is itself
> running inside a rerun, it executes, returns normally, and produces nothing.

Identical code, identical arguments, opposite behaviour, determined only by the
depth of the call stack. There is no exception and no warning to tell you this.

## Attempt 4 - queue, then draw once at the end

This is what shipped. Two changes:

1. **`celebrate.play()` only queues.** It appends to
   `st.session_state` and returns. It never touches the page.
2. **`celebrate.flush()` draws.** It is called **once**, at the very end of
   `app.py`, from the top level - where `components.html` actually renders.

A second Streamlit fact surfaced on the way, and it is the reason `play()` could
not have stayed where it was even if the depth were correct:

> **`st.rerun()` aborts the run before the end of the script.** Anything below
> it - including a `flush()` at the bottom - never executes for that run. The
> queue has to survive to the next run, and be drained by the *last* call site
> rather than the first.

Final architecture:

```
celebrate.play(name)        -> st.session_state["_sfx_pending"]   (never draws)
celebrate.flush()           -> one components.html at the end of app.py,
                               drawing only what is still pending
```

`flush()` tracks a sequence number (`_SEQ_KEY`) against the last one drawn
(`_DRAWN_KEY`), so a sound queued and then discarded by a rerun does not replay.

## The assets themselves

Once the render path worked, the files were embedded rather than fetched.
`tools/build_sfx.py` turns `assets/sfx/*.wav` into `src/sfx_data.py`: four base64
data URIs in a dict, 135 KB total. No request, no MIME type, no mount prefix, no
`server.enableStaticServing`, nothing to configure on the platform. The problem
was never the audio - it was every layer that could have stood between the file
and the speaker, and this one has none of them.

The WAVs were also resampled from 48 kHz to 16 kHz mono, which took them from
301 KB to 100 KB before base64. These are interface ticks and a short fanfare;
nothing above about 16 kHz is audible on them, and correlation with the
originals stayed between 0.995 and 0.999.

## Do not

- Do not recreate `static/` or `server.enableStaticServing`. It was measured not
  to serve the files, and the whole failure was silent.
- Do not call `components.html` from anything below the top level of the script.
- Do not rely on any code after a `st.rerun()` running in that same pass.

`src/celebrate.py` documents all three mechanisms inline, and the
`celebrate.flush()` call in `app.py` carries the reason it sits there.

## How this was actually diagnosed, and the process failure in it

The fix took four rounds of hands-on browser driving, in six-step batches, one
hypothesis per batch. That produced three wrong conclusions before the right
one, for reasons that have nothing to do with Streamlit:

- Conclusions were drawn from the **outer document**, where the app's iframes are
  not. A watcher sat in the wrong DOM the whole time and reported "nothing
  happened" when something had.
- `srcdoc` iframes were never inspected directly, so a render that had
  half-happened read as a render that had not.
- Each batch changed several things at once, so when the result improved there
  was no way to know which change did it.

The thing that actually settled it was one call, isolated, at the top level of
the script. Everything before that was inference from a measurement setup that
could not see the thing being measured.

**When a silent failure is the symptom, the diagnosis deserves more rigour than
the fix, not less.** Budget for the diagnostic, and make it observe the right
thing.