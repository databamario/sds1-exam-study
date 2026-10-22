"""Run every gate, in the order that makes them meaningful.

This exists because of a trap that has caught twice now. ``build_bank.py``
merges ``tools/bank/*.py`` into ``data/questions.json``. If a source file has a
syntax error, the build fails - and then every *other* gate still goes green,
because they read the ``questions.json`` that was left over from the last
successful build. That file is perfectly valid, so nothing complains. The suite
reports seven green gates while the bank has not been rebuilt at all, and the
one thing that matters - that the shipped bank matches its sources - is not
checked by anything.

So two things happen here that did not happen before:

1. The build runs first and a failure stops everything. There is no reading of
   seven greens over a stale bank.

2. After a successful build, ``data/questions.json`` is compared against git.
   If the rebuild changed it, the committed bank is out of date and that is a
   failure, not a detail. This catches the case where the build *succeeds* but
   somebody edited a question in ``tools/bank/`` and never rebuilt, which no
   exit code would ever reveal.

Usage::

    python tools/check_all.py          # run everything
    python tools/check_all.py -v       # also print each gate's output

Exit status is 0 only when every gate passed.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BANK = REPO / "data" / "questions.json"

# The build is not a gate like the others: it produces the thing the others
# check, so it has to come first and it has to be allowed to stop the run.
BUILD = "tools/build_bank.py"

# Same arrangement for the embedded sounds. src/sfx_data.py is generated from
# assets/sfx/*.wav, and the app plays what is in the generated module, so an
# edited wav that was never rebuilt means the repository and the running app
# disagree about what the interface sounds like.
BUILD_SFX = "tools/build_sfx.py"

# Every other gate, in the order they were added.
GATES = [
    "tools/validate.py",
    "tools/test_answer_format.py",
    "tools/test_scoring.py",
    "tools/test_progress.py",
    "tools/verify_r.py",
    "tools/verify_numbers.py",
    "tools/verify_second_pages.py",
    # Booting the full app via AppTest, not just the data tools. Caught the
    # ``TypeError: html() got an unexpected keyword argument 'key'`` regression
    # from ``7cb8327``; without it, the deployed app crashes for an hour before
    # anyone notices. Kept last so a failure in this gate does not mask the
    # data checks.
    "tools/test_app_smoke.py",
    # A mock exam must survive a browser refresh. The load/save logic, and the
    # guard that stops the first run of a session overwriting the saved exam
    # before anything has read it.
    "tools/test_exam_state.py",
    # progress.py and index.js each hold their own copy of the blob format and
    # have no build step to keep them in step. See the module docstring.
    "tools/test_storage_parity.py",
    # Figures must be inlined as data URIs. Served from /media/, Streamlit
    # deletes them as soon as no running script references them, which showed up
    # as figures that render fine and then break on the next click.
    "tools/test_figures_inline.py",
]


def run(step: str, verbose: bool) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, str(REPO / step)],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    out = ((proc.stdout or "") + (proc.stderr or "")).strip()
    if verbose and out:
        print(out)
    return proc.returncode == 0, out


def generated_is_stale(relative: str) -> bool:
    """True when a generated file differs from what git holds.

    Same question as :func:`bank_is_stale`, asked of a second generated file.
    """
    proc = subprocess.run(
        ["git", "diff", "--quiet", "--", relative],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    if proc.returncode not in (0, 1):
        return False
    return proc.returncode == 1


def bank_is_stale() -> bool:
    """True when rebuilding produced a different questions.json than git holds."""
    proc = subprocess.run(
        ["git", "diff", "--quiet", "--", str(BANK.relative_to(REPO))],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    if proc.returncode not in (0, 1):
        # No git, or not a repository. Not a reason to fail the suite.
        return False
    return proc.returncode == 1


def declared_streamlit() -> str:
    """The Streamlit requirement exactly as written in requirements.txt."""
    req = REPO / "requirements.txt"
    if not req.exists():
        return ""
    for line in req.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line.lower().startswith("streamlit"):
            return line
    return ""


def version_mismatch() -> str | None:
    """A complaint when the deployed Streamlit is not the one being tested.

    The deployed app served a blank page for an hour because ``requirements.txt``
    said ``streamlit>=1.40``: a floor and no ceiling, so the cloud took 1.66.0
    while every test on this machine had run against 1.45.1. A component written
    for one version simply did not load on the other, and because nothing anywhere
    compared the two, "it works here" and "it works there" quietly stopped being
    the same claim.

    That is the whole reason this check exists. ``test_progress.py`` passes against
    whatever Streamlit is installed locally and says nothing about what the cloud
    resolves, so the suite was green and the deployed app was broken at the same
    time. A loose floor is a promise nobody checks.

    So the rule is narrow on purpose: if the requirement would accept a version
    other than the one installed, fail. An exact pin always passes. A range fails
    only when the installed version falls outside it.
    """
    import re

    declared = declared_streamlit()
    if not declared:
        return None

    try:
        import streamlit
        installed = streamlit.__version__
    except Exception:
        return None

    bounds = re.findall(r"(\d+(?:\.\d+)*)", declared)
    if len(bounds) < 2:
        # "streamlit>=1.45" with no upper bound: same trap as before, closed.
        return (
            "requirements.txt says %r, which accepts any version >= %s. The "
            "cloud resolved a different Streamlit from this machine and the app "
            "did not start. Pin it (for example ==%s) or add a ceiling."
            % (declared, bounds[0] if bounds else "?", installed)
        )

    low, high = bounds[0], bounds[-1]
    if low != high and not (low <= installed < high):
        return (
            "Streamlit %s is installed here but requirements.txt (%r) would let "
            "the cloud deploy something else. Tests pass locally and the "
            "deployed app can still be broken." % (installed, declared)
        )
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="print each gate's output as well")
    args = ap.parse_args()

    failures: list[str] = []

    ok, out = run(BUILD, args.verbose)
    print("%-28s %s" % (BUILD, "ok" if ok else "FAILED"))
    if not ok:
        print()
        print("The bank did not build, so nothing below it means anything:")
        print("every other gate would read the questions.json left over from")
        print("the last successful build and go green. Fix this first.")
        if out:
            print()
            print(out)
        return 1

    if bank_is_stale():
        failures.append(
            "data/questions.json differs from what tools/bank/ produces. "
            "A question was edited without rebuilding the bank, so the shipped "
            "questions are not the ones in the source files."
        )
        print("%-28s STALE" % "data/questions.json")
    else:
        print("%-28s ok" % "data/questions.json up to date")

    complaint = version_mismatch()
    if complaint:
        failures.append(complaint)
        print("%-28s MISMATCH" % "requirements.txt streamlit")
    else:
        try:
            import streamlit
            ver = streamlit.__version__
        except Exception:
            ver = "?"
        print("%-28s ok" % ("streamlit %s pinned" % ver))

    ok, out = run(BUILD_SFX, args.verbose)
    print("%-28s %s" % (BUILD_SFX, "ok" if ok else "FAILED"))
    if not ok:
        failures.append(
            "src/sfx_data.py could not be rebuilt from assets/sfx/. The app "
            "imports that module, so without it no sound can play."
        )
        if out:
            print()
            print(out)
            print()

    if generated_is_stale("src/sfx_data.py"):
        failures.append(
            "src/sfx_data.py differs from what tools/build_sfx.py produces. A "
            "sound was edited in assets/sfx/ without rebuilding, so the app "
            "plays the old audio while the repository claims a new one."
        )
        print("%-28s STALE" % "src/sfx_data.py")
    else:
        print("%-28s ok" % "src/sfx_data.py up to date")

    for gate in GATES:
        ok, out = run(gate, args.verbose)
        print("%-28s %s" % (gate, "ok" if ok else "FAILED"))
        if not ok:
            failures.append(gate)
            if out:
                print()
                print(out)
                print()

    print()
    if failures:
        print("SUITE FAILED (%d):" % len(failures))
        for f in failures:
            print("  -", f)
        return 1
    print("SUITE GREEN: build is current and all %d gates passed." % len(GATES))
    return 0


if __name__ == "__main__":
    sys.exit(main())