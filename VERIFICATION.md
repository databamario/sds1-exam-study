# What "it works" has to mean

A note written after nearly rewriting a working system, kept because the near-miss
is more useful than the fix would have been.

## What happened

`progress.record()` appeared not to persist on the deployed app. Progress writes go
through `st.components.v1.html()`, which renders an iframe whose script updates
`localStorage` and returns nothing to Python - there is no channel back, so
nothing in the Python layer can tell whether the write happened. Reading
`localStorage` from the browser after grading a question showed an empty `attempts`
array, while `prefs` was writing correctly. That is a convincing shape for a real
bug: one code path works, its sibling silently does not, and the app's main
feature is dead in production.

The plan was to collapse both paths onto the declared component, which does have a
return channel, on the reasoning that fewer mechanisms are better.

## What was actually true

`record()` worked the whole time. On the deployed app, grading a question produced:

```
{"attempts": [{"question_id": "L1-MC-001", "score": 0.5, "max_score": 1, ...}],
 "prefs": {"sound": "0"}}
```

The Progress screen then read *Attempts 1 · 0.5 / 1.0 · 50%*, and still read it
after a full page reload. Record, write, read back, persist: the whole cycle,
in production, on the deployed version.

The empty `attempts` came from the measurement, not the app. The test harness was
clicking option labels that it then reported as not marked, while the app graded
the question anyway - a contradiction that was the tell. A harness reporting "I
clicked it" and then "nothing is checked" is not measuring the thing it claims to
measure, and its readings should not be believed until that is resolved.

## Why the plan was wrong anyway

Even had the bug been real, the fix was chosen before the diagnosis finished. The
first real test - toggle a preference twice and read the value back - showed
`"sound": "0" -> "1" -> "0"`, which means the write mechanism was fine and the
fault lay elsewhere. That result arrived *before* any code was touched, and it
would have redirected the whole approach.

There was also a real cost to the wrong plan. Collapsing the write path onto the
declared component means every answer the user gives now waits on a round trip
through a component, instead of an iframe that has already run. Trading a
non-existent reliability problem for a real latency and coupling cost is a bad
trade, and the only reason it nearly happened was that the diagnosis was skipped
in favour of a plausible story.

## What to hold to

- **A write path with no return channel cannot be verified from Python.** That is
  not an argument against `components.html`; it is an argument for checking the
  browser, where the write happens.
- **Verify in the environment that matters.** Local passed the whole cycle and was
  no evidence at all about the deployment. The difference here was not subtle -
  it was everything.
- **Run the discriminating test first.** One toggle-in, toggle-out, read-back
  separated "the mechanism is broken" from "this payload is broken" in under a
  minute. A plausible mechanism story felt like progress and was not.
- **Believe the harness last.** It disagreed with itself before I believed it
  against the app.