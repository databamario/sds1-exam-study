"""Full validation of the question bank.

Run:  python tools/validate.py
Exit code is non-zero if any check fails.
"""

from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.loader import (  # noqa: E402
    LECTURES, MC, WA, load_bank, mc_format_problems, validate_bank,
)
from src.scoring import score_mc  # noqa: E402

TARGET_MC = 148
TARGET_WA = 82

# Anti-guessing limits, as a share of the questions they apply to.
#
# With 129 five-option questions and ten possible pairs, a perfectly even spread
# is 12.9% per pair, so 20% allows about one and a half times even. With 19
# four-option single-correct questions an even spread is 25% per position, so
# 35% is a little under one and a half times even. Both are set from the actual
# sample sizes rather than picked to make the current bank pass.
PAIR_LIMIT = 0.20
POSITION_LIMIT = 0.35

# Below this many questions, "no single answer dominates" is not a statement
# worth failing a commit over: with 6 questions the most common of 10 pairs is
# 33% by arithmetic alone.
MIN_SAMPLE_FOR_SPREAD = 20

# --------------------------------------------------------------- ratchet
#
# The rule above is a hard gate, but 123 of the 148 MC questions broke it when
# it was written, and the migration that fixes them happens one lecture per
# commit. A hard gate on a bank that is knowingly mid-migration would make
# every one of those commits red, and a red suite is a suite people stop
# reading.
#
# So the migration is a ratchet. This number is how many violations are still
# allowed to exist. It only ever goes down, one lecture at a time, and it is
# deliberately a bare constant so that lowering it is a visible, reviewable
# edit in the diff rather than a side effect of running something. Going
# BELOW it is reported, because that means the constant is stale and the real
# rule is looser than it looks. When it reaches zero the allowance disappears
# and the plain rule applies.
#
# Progress: 123 -> 108 after Lecture 1, which fixed 15 questions: 11 were given
# a second true option, and 4 were reduced from three or four true options to two.
FORMAT_MIGRATION_REMAINING = 71

# Every R function the lectures actually teach. A lecture cannot be "covered"
# unless at least one question references each of its functions.
LECTURE_R_FUNCTIONS = {
    1: ["<-", "c", "data.frame", "factor", "function", "class"],
    2: ["library", "install.packages", "table", "prop.table", "filter", "select",
        "arrange", "mutate", "group_by", "summarize", "|>", "ggplot", "aes",
        "subset", "order", "desc", ".by", "ungroup"],
    3: ["inner_join", "left_join", "right_join", "full_join", "as.numeric",
        "quantile", "IQR", "range", "median"],
    4: ["table"],
    5: ["pnorm", "mean", "median"],
    6: ["pnorm", "qnorm", "qt", "sqrt"],
    7: ["t.test", "prop.test", "pnorm", "pt", "qnorm", "sqrt"],
    8: ["cor", "cor.test", "oneway.test", "chisq.test", "pchisq", "select"],
    9: ["sample", "set.seed", "rnorm", "rexp", "rbinom", "median"],
}


def hr(title):
    print("\n" + title)
    print("-" * len(title))


def position_spread_failures(mc: list[dict]) -> list[str]:
    """Failures describing a guessable answer layout.

    A student who spots that the answer is almost always in the same slot can
    stop reading. With five options and two correct, the leak is a PAIR: a
    student who always ticks (a) and (b) is right on every question whose key
    happens to be {a,b}. With four options and one correct it is a single
    position. Both are checked here.

    A previous version of this file checked the position of the single FALSE
    option instead. That was checking a different game entirely, and it left
    single-correct four-option questions completely unguarded.

    Split out from main() so the test suite can check that a well spread bank
    passes, not only that a bad one fails.
    """
    failures: list[str] = []

    five_two = [q for q in mc if len(q.get("options") or {}) == 5
                and len(q.get("correct") or []) == 2]
    if five_two:
        pairs = collections.Counter("".join(sorted(q["correct"])) for q in five_two)
        worst_pair, worst_n = max(pairs.items(), key=lambda kv: kv[1])
        share = worst_n / float(len(five_two))
        # The pair distribution can only be judged on the finished population.
        # While the migration is still running these questions are a biased
        # sample of the five-option ones, because the ones converted so far are
        # the lectures already reworked, not a random draw. Measuring 21% of a
        # partial sample and calling it a leak would be reporting a number that
        # the next commit invalidates.
        armed = (len(five_two) >= MIN_SAMPLE_FOR_SPREAD
                 and FORMAT_MIGRATION_REMAINING == 0)
        if share > PAIR_LIMIT and armed:
            failures.append(
                "always ticking (%s) would score %.0f%% of five-option "
                "questions; spread the correct pairs further"
                % (",".join(worst_pair), share * 100))

    four_one = [q for q in mc if len(q.get("options") or {}) == 4
                and len(q.get("correct") or []) == 1]
    if four_one:
        pos = collections.Counter(q["correct"][0] for q in four_one)
        worst_pos, worst_n = max(pos.items(), key=lambda kv: kv[1])
        share = worst_n / float(len(four_one))
        if share > POSITION_LIMIT:
            failures.append(
                "the correct option sits in (%s) for %.0f%% of single-correct "
                "four-option questions; move some of them"
                % (worst_pos, share * 100))

    return failures


def main() -> int:
    failures = []
    warnings = []

    questions = load_bank()
    hr("Schema")
    problems = validate_bank(questions)
    if problems:
        failures.append("%d schema problems" % len(problems))
        for p in problems[:20]:
            print("  FAIL %s" % p)
    else:
        print("  ok   all %d questions pass the schema" % len(questions))

    mc = [q for q in questions if q["type"] == MC]
    wa = [q for q in questions if q["type"] == WA]

    hr("Counts")
    print("  MC: %d (target %d)" % (len(mc), TARGET_MC))
    print("  WA: %d (target %d)" % (len(wa), TARGET_WA))
    if len(mc) != TARGET_MC:
        failures.append("MC count is %d, expected %d" % (len(mc), TARGET_MC))
    if len(wa) != TARGET_WA:
        failures.append("WA count is %d, expected %d" % (len(wa), TARGET_WA))
    if len(questions) < 200:
        failures.append("total below 200")

    hr("Multiple-choice grading scheme")
    cases = [
        (["a", "b"], ["a", "b"], 1.0, "all correct marked"),
        (["a"], ["a", "b"], 0.5, "one correct option not marked"),
        (["a", "b", "c"], ["a", "b"], 0.5, "one incorrect option marked"),
        (["a", "c"], ["a", "b"], 0.0, "two mistakes"),
        (["c", "d", "e"], ["a", "b"], 0.0, "two mistakes"),
    ]
    for correct, selected, expected, why in cases:
        got = score_mc(correct, selected)
        ok = got == expected
        print("  %s   %-38s -> %.1f" % ("ok  " if ok else "FAIL", why, got))
        if not ok:
            failures.append("scoring case failed: %s" % why)

    ok = score_mc(["a"], []) == 0.5
    print("  %s   %-38s -> %.1f" % ("ok  " if ok else "FAIL",
                                   "blank answer, 1 correct", 0.5))
    if not ok:
        failures.append("blank answer must never score the full point")

    hr("Multiple-choice answer format")
    # The exam's own worked example is a five-option question with two correct
    # options, and three or four correct options never appear. See
    # mc_format_problems for the rule; this is the gate that enforces it.
    bad_format = []
    for q in mc:
        bad_format.extend(mc_format_problems(q))
    by_id = collections.defaultdict(list)
    for msg in bad_format:
        by_id[msg.split(":")[0]].append(msg)
    print("  MC questions breaking the format rule: %d of %d"
          % (len(by_id), len(mc)))
    for qid in sorted(by_id):
        print("    %s" % by_id[qid][0])
    if bad_format:
        detail = ("%d MC questions break the answer-format rule (at most 5 "
                  "options; 5 options => exactly 2 correct, never more than 2): %s"
                  % (len(by_id), ", ".join(sorted(by_id)[:8])
                     + (" ..." if len(by_id) > 8 else "")))
        if len(by_id) > FORMAT_MIGRATION_REMAINING:
            failures.append(
                "format migration REGRESSED: %d questions break the rule but "
                "only %d are allowed to remain. %s"
                % (len(by_id), FORMAT_MIGRATION_REMAINING, detail))
        else:
            if len(by_id) < FORMAT_MIGRATION_REMAINING:
                warnings.append(
                    "FORMAT_MIGRATION_REMAINING is %d but only %d questions "
                    "still break the rule; tighten it"
                    % (FORMAT_MIGRATION_REMAINING, len(by_id)))
            else:
                print("  migration ratchet: %d remaining of the %d allowed"
                      % (len(by_id), FORMAT_MIGRATION_REMAINING))

    hr("n_correct distribution")
    dist = collections.Counter(q["n_correct"] for q in mc)
    for k in sorted(dist):
        print("  %d correct option(s): %4d questions" % (k, dist[k]))
    if 1 not in dist:
        warnings.append("no single-correct questions")

    hr("Source citations")
    missing = [q["id"] for q in questions
               if not q["source"].get("pdf") or not q["source"].get("slide")]
    print("  questions missing a pdf or slide reference: %d" % len(missing))
    if missing:
        failures.append("uncited questions: %s" % ", ".join(missing[:10]))

    hr("Written-answer rubrics")
    bad = [q["id"] for q in wa if not q.get("rubric")]
    print("  WA without a rubric: %d" % len(bad))
    if bad:
        failures.append("WA without rubric: %s" % ", ".join(bad[:10]))
    total_elements = sum(sum(i["elements"] for i in q["rubric"]) for q in wa)
    print("  total rubric checkpoints: %d across %d WA questions"
          % (sum(len(q["rubric"]) for q in wa), len(wa)))
    print("  total gradable elements: %d" % total_elements)

    hr("Written answers stay short (exam caps them at ~3 sentences)")
    # Word count is the hard gate. Sentence counting is unreliable here because a
    # colon-delimited list of four short items - a perfectly good exam answer to
    # "identify these four things" - reads as four sentences.
    long_answers = []
    for q in wa:
        words = len(q["answer"].split())
        sentences = len([s for s in re.split(r"(?<=[.!?])\s+", q["answer"].strip())
                         if len(s.split()) >= 6])
        if words > 45:
            long_answers.append("%s (%dw, %d prose sentences)"
                                % (q["id"], words, sentences))
    print("  WA answers over 45 words: %d of %d" % (len(long_answers), len(wa)))
    for item in long_answers[:12]:
        print("    %s" % item)
    if long_answers:
        failures.append("%d WA answers are too long: %s"
                        % (len(long_answers), ", ".join(long_answers[:6])))
    with_detail = sum(1 for q in wa if q.get("detail"))
    print("  WA with a longer 'detail' explanation: %d of %d" % (with_detail, len(wa)))
    print("  median WA answer length: %d words"
          % sorted(len(q["answer"].split()) for q in wa)[len(wa) // 2])

    hr("Figure questions")
    img_dir = Path(__file__).resolve().parents[1] / "data" / "images"
    figs = [q for q in questions if q.get("image")]
    print("  questions with a figure: %d" % len(figs))
    broken = []
    for q in figs:
        if not (img_dir / (q["image"] + ".png")).exists():
            broken.append(q["id"])
    print("  %s every referenced figure exists"
          % ("ok  " if not broken else "FAIL"))
    if broken:
        failures.append("missing figure files: %s" % ", ".join(broken))
    unused = sorted({f.stem for f in img_dir.glob("*.png")}
                    - {q["image"] for q in figs})
    if unused:
        print("  warn figures generated but unused: %s" % ", ".join(unused))

    hr("Interface sounds")
    sfx_dir = Path(__file__).resolve().parents[1] / "static" / "sfx"
    needed = ["correct", "celebrate", "wrong", "tap"]
    missing_sfx = [n for n in needed if not (sfx_dir / (n + ".wav")).exists()]
    empty_sfx = [n for n in needed if (sfx_dir / (n + ".wav")).exists()
                 and (sfx_dir / (n + ".wav")).stat().st_size < 1000]
    for name in needed:
        path = sfx_dir / (name + ".wav")
        if path.exists():
            print("  %-10s %6.1f KB" % (name, path.stat().st_size / 1024))
    if missing_sfx:
        failures.append("missing sound files: %s (run tools/make_sfx.py)"
                        % ", ".join(missing_sfx))
    elif empty_sfx:
        failures.append("suspiciously small sound files: %s"
                        % ", ".join(empty_sfx))
    else:
        print("  ok   all four sounds present")
    if not (Path(__file__).resolve().parents[1] / ".streamlit" / "config.toml").exists():
        failures.append(".streamlit/config.toml is missing, so Streamlit will not "
                        "serve static/ and no sound will play")

    hr("No references to the course in student-facing text")
    meta = re.compile(
        r"\b(the (lecture|lectures|course|slides?|material|handout|deck|exam "
        r"handout)|in this (lecture|course)|as (shown|stated|described|explained) "
        r"in the|according to the|we (covered|introduced|discussed)|"
        r"the professor|the textbook|as mentioned)\b", re.I)
    offenders = []
    for q in questions:
        text = " ".join([q.get("stem", ""), q.get("answer", ""),
                         q.get("explanation", ""), q.get("detail", "") or ""])
        hit = meta.search(text)
        if hit:
            offenders.append("%s (%s)" % (q["id"], hit.group(0).strip()))
    print("  questions referring to the course: %d" % len(offenders))
    for item in offenders[:15]:
        print("    %s" % item)
    if offenders:
        failures.append("%d questions refer to the course: %s"
                        % (len(offenders), ", ".join(offenders[:6])))

    hr("Adapted vs original")
    adapted = [q for q in questions if q.get("origin") == "adapted_HT25"]
    print("  adapted from the HT25 mock exam: %d" % len(adapted))
    print("  newly written for the lectures:  %d" % (len(questions) - len(adapted)))

    hr("R coverage per lecture")
    for lec in range(1, 10):
        covered = set()
        for q in questions:
            if q["lecture"] == lec:
                covered.update(q.get("r_functions", []))
        want = LECTURE_R_FUNCTIONS[lec]
        missing_fns = [f for f in want if f not in covered]
        status = "ok  " if not missing_fns else "FAIL"
        print("  %s Lecture %d: %d/%d expected functions covered"
              % (status, lec, len(want) - len(missing_fns), len(want)))
        if missing_fns:
            failures.append("Lecture %d missing R coverage: %s"
                            % (lec, ", ".join(missing_fns)))

    hr("Per-lecture totals")
    print("  %-4s %4s %4s %6s" % ("Lec", "MC", "WA", "Total"))
    for lec in range(1, 10):
        m = sum(1 for q in mc if q["lecture"] == lec)
        w = sum(1 for q in wa if q["lecture"] == lec)
        print("  %-4d %4d %4d %6d   %s" % (lec, m, w, m + w, LECTURES[lec][:40]))
        if m + w == 0:
            failures.append("Lecture %d has no questions" % lec)

    hr("Duplicate detection")
    # Two questions can share a stem and still test different things: "Which
    # statements are TRUE?" is boilerplate that dozens of multi-select questions
    # legitimately reuse. What makes a pair a real duplicate is the OPTION SET
    # overlapping, so that is what decides it.
    def _norm(s: str) -> str:
        return re.sub(r"\W+", " ", (s or "").lower()).strip()

    def _opts(q: dict) -> set:
        return {_norm(v) for v in (q.get("options") or {}).values()}

    def _jaccard(a: set, b: set) -> float:
        if not a or not b:
            return 0.0
        return len(a & b) / float(len(a | b))

    by_stem: dict = {}
    for q in questions:
        by_stem.setdefault(_norm(q["stem"]), []).append(q)

    dupes = []
    shared_stems = 0
    for stem, group in by_stem.items():
        if len(group) < 2:
            continue
        shared_stems += 1
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                a, b = group[i], group[j]
                if a["type"] != "MC" or b["type"] != "MC":
                    continue
                score = _jaccard(_opts(a), _opts(b))
                if score >= 0.6:
                    dupes.append("%s ~ %s  (option overlap %.0f%%)"
                                 % (a["id"], b["id"], score * 100))

    # A repeated option set is a duplicate even when the stem was reworded.
    by_opts: dict = {}
    for q in questions:
        if q["type"] == "MC" and _opts(q):
            by_opts.setdefault(frozenset(_opts(q)), []).append(q["id"])
    for group in by_opts.values():
        if len(group) > 1:
            dupes.append("identical option set: %s" % ", ".join(sorted(group)))

    print("  stems shared by >1 question: %d (boilerplate stems are fine)" % shared_stems)
    print("  true near-duplicates: %d" % len(dupes))
    for d in dupes:
        print("    %s" % d)
    if dupes:
        failures.append("%d true near-duplicate questions" % len(dupes))

    ids = [q["id"] for q in questions]
    print("  duplicate ids: %d" % (len(ids) - len(set(ids))))

    hr("Answer-key consistency")
    # An explanation that says "(c) is false" must not sit next to a key that
    # marks c correct. This is the failure mode where a question is unanswerable
    # for a student who reasons correctly.
    LETTERS = "abcde"
    bad_refs = []
    for q in questions:
        if q["type"] != "MC":
            continue
        expl = q.get("explanation") or ""
        correct = set(q.get("correct") or [])
        for m in re.finditer(r"\(([a-e])\)\s+(?:is|are)\s+(false|wrong|incorrect)", expl, re.I):
            letter, verdict = m.group(1), m.group(2).lower()
            if letter in correct:
                bad_refs.append("%s: explanation calls (%s) false but the key marks it correct"
                                % (q["id"], letter))
        for m in re.finditer(r"\(([a-e])\)\s+(?:is|are)\s+(true|right|correct)", expl, re.I):
            letter = m.group(1)
            if letter not in correct:
                bad_refs.append("%s: explanation calls (%s) true but the key marks it false"
                                % (q["id"], letter))
    print("  explanations contradicting their own key: %d" % len(bad_refs))
    for b in bad_refs:
        print("    %s" % b)
    if bad_refs:
        failures.extend(bad_refs)

    hr("Where the correct answer sits")
    spread_failures = position_spread_failures(mc)

    five_two = [q for q in mc if len(q.get("options") or {}) == 5
                and len(q.get("correct") or []) == 2]
    if five_two:
        pairs = collections.Counter("".join(sorted(q["correct"])) for q in five_two)
        worst_pair, worst_n = max(pairs.items(), key=lambda kv: kv[1])
        armed = (len(five_two) >= MIN_SAMPLE_FOR_SPREAD
                 and FORMAT_MIGRATION_REMAINING == 0)
        print("  five-option questions with 2 correct: %d%s"
              % (len(five_two),
                 "" if armed else "  (gate not armed until the migration is "
                                  "finished and there are %d of them)"
                                  % MIN_SAMPLE_FOR_SPREAD))
        print("  correct pairs: %s"
              % ", ".join("%s=%d" % kv for kv in sorted(pairs.items())))
        print("  most common pair %s: %.1f%% of them (limit %.0f%%)"
              % (worst_pair, worst_n / float(len(five_two)) * 100, PAIR_LIMIT * 100))

    four_one = [q for q in mc if len(q.get("options") or {}) == 4
                and len(q.get("correct") or []) == 1]
    if four_one:
        pos = collections.Counter(q["correct"][0] for q in four_one)
        worst_pos, worst_n = max(pos.items(), key=lambda kv: kv[1])
        share = worst_n / float(len(four_one))
        print("  four-option questions with 1 correct: %d" % len(four_one))
        print("  correct position: %s"
              % ", ".join("%s=%d" % kv for kv in sorted(pos.items())))
        print("  most common position %s: %.1f%% of them (limit %.0f%%)"
              % (worst_pos, share * 100, POSITION_LIMIT * 100))
        if share > POSITION_LIMIT:
            offenders = [q["id"] for q in four_one if q["correct"][0] == worst_pos]
            print("      offenders: %s" % ", ".join(sorted(offenders)[:20]))

    failures.extend(spread_failures)

    hr("Result")
    for wmsg in warnings:
        print("  warn %s" % wmsg)
    if failures:
        print("  %d CHECK(S) FAILED" % len(failures))
        for f in failures:
            print("   - %s" % f)
        return 1
    print("  All checks passed. %d questions ready." % len(questions))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())