# Deploy plan

How this app goes from "26 commits on my laptop" to "a link my classmates can
use". Written down before starting, because the order matters more than it
looks: doing these in the wrong order means pushing and deploying three times
instead of once.

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

Read by hand so far: 63. Found and fixed 22 real errors. Remaining: **169**,
grouped by how badly the cited slide matches the question:

```
band   score      left
A      < 0.10       done
B      0.10-0.15    done
C      0.15-0.20    done
D      0.20-0.30    48
E      > 0.30      121
```

Per batch: read with `python tools/show_citation.py --band LO HI`, fix only what
the slide text proves, re-derive the correct page from the PDF rather than from
any table written earlier, run the full gate suite, commit.

Band E is half the remaining work and has the weakest signal - a high score
means the slide *does* match, so it is the least likely to hide an error. It is
read last, and it is read, because band C returned 0/11 and the very next band
returned 3/8. The trend already lied once.

One improvement worth making first: most of the errors found so far are not
"wrong page" but "right page, content on the *next* slide". That is mechanically
detectable, so `tools/verify_citations.py` should learn to rank by **proximity**
- does the decisive term appear on the cited page, or on the page after it -
rather than by word overlap alone.

## Phase 2 - progress in the browser

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

- The component must be **built and its `dist/` committed**, so the deploy needs
  no `npm install` and no build step. Node 22 and npm 10.9.2 are available
  locally, so the bundle is produced here and checked in.
- `components.html` stays in use for the sounds, where it already works and
  where no return value is needed.

Still to confirm by running the real thing, not the probe: whether the
component's return arrives in time for the next question. A declared component
returns on the *following* script run, so `record()` and `attempts_for()` must
not be called in the same run or the screen would show one question stale.
Worth checking against the practice loop before trusting it.

### What is involved

- A small JS component, committed to the repo, that reads and writes one
  `localStorage` key.
- `progress.py` rewritten on top of it, keeping the same nine function names.
- `attempts_for` and `by_lecture` are real queries; `localStorage` has no query
  language, so both become a load, filter in Python, and return. Realistic
  size: **~130 lines**, not the ~40 I first guessed - the estimate was too
  optimistic because I forgot there is no SQL underneath any more.
- Tests for the new layer, plus the existing suite kept green.

### What is deliberately not being done

No backend, no database, no user accounts, no sync between devices. Progress
lives in the browser that earned it. That is the trade: one line of code that
does not need a server, in exchange for progress that does not follow you to
your phone. Both were considered and this was the choice.

## Phase 3 - one push

Everything above lands first, then:

```powershell
$env:GITHUB_TOKEN = $null     # a 93-char token in User scope shadows gh and 401s it
gh repo create databamario/sds1-exam-study --public --source=. --remote=origin --push
```

Two accounts are now registered in the `gh` keyring, `databamario` active, so
the command runs as Mario's personal account and not as the company one. If
`gh` objects that `origin` already exists, remove it first and let `gh` recreate
it - the URL is identical, so nothing else changes. If the push fails on
credentials while the repo was created, the repo exists and only the push is
missing: do **not** re-run `create`, it will fail with "already exists".

The pre-push check is already done: 57 files, 1.44 MB, no PDFs, no databases,
no secrets.

## Phase 4 - Streamlit

This part needs a browser session with Mario's own account, so it cannot be
automated from here. The app is already deployable-shaped:

```
requirements.txt        one line: streamlit>=1.40
.streamlit/config.toml enableStaticServing = true   already set, for the sounds
secrets.toml            does not exist, nothing to leak
paths in src/           all relative via Path(__file__).resolve(), no C:\ anywhere
```

Steps at <https://share.streamlit.io>: Deploy, authorise GitHub, pick
`sds1-exam-study`, wait 3-5 minutes for the first build, then set a password in
the app's settings.

Password on Streamlit Community Cloud shows a password prompt to anyone with the
link, which is the point - the link is shareable, the app is not open.

## What is deliberately not being done

- **Not staying private.** It buys nothing here: there is no material in the
  repo worth hiding, and a private repo cannot be deployed on the free
  Community plan anyway - private sources need a paid plan. Public it is.
- **Not migrating the local progress.** Decided: start from zero.