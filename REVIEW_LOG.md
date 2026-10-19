# Citation review log

Which questions have been read against their slide, and what the reading found.

This file exists because the answer used to live only in whoever was doing the
reviewing. That cost an entire handover: the state was lost, the surviving count
was wrong, and work that had already been done had to be guessed at rather than
resumed. A list that only exists in a conversation is a list that does not exist.

Append one line per question as it is judged. `ok` means the cited page really
does carry the fact the question asserts. Anything else goes in the right-hand
column with what was actually wrong, so a later reader does not have to rediscover
it.

## Bands

`tools/show_citation.py --band LO HI` sorts by a mechanical score, low first: a
low score means the citation looks more likely to be wrong. The bands were:

| band | range | read | wrong |
|------|-------|------|-------|
| A | worst 6 | 6 | 4 |
| B | next 18 | 18 | 5 |
| C | 11 | 11 | 0 |
| D | 58 | 58 | 27 / 22 |
| E | 127 | see below | not countable - see below |

Band E is where the mistakes stopped being common: 9% against 67% in band A.
That is the reason for the remaining work rather than a reason to skip it, since
even 9% of 127 is about a dozen wrong citations sitting in a study tool.

Correcting a question moves it out of its band, because a fixed citation scores
better. So a question missing from band E has either been fixed or never been
risky enough to be listed - and that is exactly why this log is needed to say
which is which.

## Entries

**The progress count in this file was wrong until now, and it is not derivable
from the table.** The table holds 42 entries, 13 of them flagged wrong. But the
earlier band passes were never transcribed into it - they live in the commit
messages - so "read so far: 27" could not be reconstructed, and the previous
version of this section asserted it anyway while its own table contradicted it
twice over (24 rows, "2 wrong", and a third wrong question named in the prose
with no row at all). Rather than carry a number forward or invent a new one,
the numbers that can be counted are given and the rest is left open.
`L7-WA-008` is known to be wrong and still has no row.

What can be said: band E holds 127 questions, the two batches logged at the
bottom of this table read 18 of them, and the error rate in those two batches was
11 of 18 - far above the 9% the band is supposed to average, because a batch read
in score order starts at the most suspicious end of the band.

Two shapes account for most of the errors, and both are structural rather than
careless:

- **A question that needs two pages.** Its two correct options are both true, but
  only one is on the cited page. A citation is one page, so such a question is
  always half wrong, and `validate.py` reports it as perfectly formed every time.
- **An answer whose second half is true and unciteable.** "A p-value is not the
  probability that the null is true" and "the CLT is what lets you use z-scores"
  are taught everywhere and printed nowhere in these 16 PDFs. The fix is the same
  in both shapes: keep what the slide carries, drop what it does not, and never
  keep a good fact by citing a page that does not hold it.

| question | verdict | finding |
|----------|---------|---------|
| L2-MC-007 | ok | p.45 carries both the positional and named call |
| L2-MC-012 | ok | p.51 lists the three chaining advantages |
| L2-WA-009 | ok | p.23 table has all four statistical types |
| L5-WA-005 | **wrong** | answer said "about 0.0345, rounded to 0.0344"; R gives 0.034518, so 0.0345 is right and 0.0344 is the slide's own value. Rounding direction was backwards |
| L9-WA-007 | ok | p.16 carries the birthday simulation |
| L8-WA-005 | ok | p.20 carries both matrix properties and how to compute |
| L8-MC-002 | ok | p.16 shows the output and the rejection |
| L8-MC-001 | ok | key is ['a','b']; both are on p.8 |
| L8-MC-005 | ok | key is ['a','b']; both are on p.20 |
| L6-MC-015 | ok | p.39 gives 1.96 and 2.576; the 1.28 in (c) is a trap, the slide says 1.645 |
| L1-MC-008 | ok | p.28 states the equal-chance and target-equals-sample points verbatim |
| L2-MC-020 | ok | p.50 shows the exact `order(..., decreasing = TRUE)` line; the reordered rows support (c) |
| L2-WA-001 | ok | p.29 demonstrates prop.table on table(class) |
| L4-MC-009 | ok | p.43 carries the table and the 14/24 = 0.58 calculation |
| L5-WA-008 | **wrong** | answer quoted Var(Xbar) = sigma^2/n, which is on p.38; p.37 ends mid-sentence at "But exac...". Formula removed, point kept as variability |
| L6-WA-006 | ok | p.34 carries the randomness argument. The phrase "interval of plausible values" is loose for a question that asks what the interval does *not* tell you, but the citation is right |
| L2-MC-014 | ok | p.49 lists filter and subset as many ways of the same thing |
| L6-MC-008 | ok | p.39 gives 1.96. The alpha = 0.05 answer is derived from z(0.025), not printed |
| L3-MC-006 | ok | p.28 gives s^2 with n-1. Four options, one correct - inside the format rule |
| L1-WA-002 | ok | p.52 has all four structures, matrix included as a 2D array of same type |
| L5-MC-001 | ok | p.15 names coin tosses and yes/no questions as the binomial example |
| L6-WA-001 | ok | p.17 gives z = (179-170)/1.83 = 4.93 |
| L2-WA-008 | ok | p.54 shows both forms. But "the modern alternative" for .by is not on the page - it offers the two as equals |
| L3-MC-018 | **wrong** | two correct options: one about full_join (p.64), one about left_join (p.62). The four joins take one page each - inner 61, left 62, right 63, full 64 - so one citation can never reach both. Reframed on full_join alone |
| L1-MC-003 | ok | p.9 lists "incorrect sampling strategy" and "incorrect measurement of stress" verbatim, and the three distractors are none of them |
| L5-MC-005 | ok | p.27 carries both halves: the area-to-the-left reading and the pnorm call. Slide prints 0.0344, option says "about 0.034" - consistent |
| L3-MC-002 | **wrong** | "a strongly right-skewed distribution implies mean > median" is printed **nowhere in the course** - `find_slide.py "skew"` returns only the p.21 pros/cons table and a Lecture 5 caption. p.20 says the mean is pulled *down* by low outliers, which is the other direction. Reframed on what p.21 actually prints: mean sensitive to outliers and skew, median robust to them. The fact itself is true and commonly taught, but there is no slide to cite it to, which is the whole constraint |
| L3-WA-005 | **wrong** | p.42 explains correlation and the -1/0/+1 readings, but never prints `cor(`; `find_slide.py "cor("` returns exactly two hits, both in Lecture 8's correlation matrix. Half the question was unciteable. Dropped the code half rather than moving the citation to another lecture, because the -1/0/+1 content is what the slide teaches |
| L4-MC-004 | **wrong** | p.17 carries the deck, the sum, and the complementary definition - but the P(Aᶜ) = 1 - P(A) rule in option (e) is on p.49 (and p.18). One page cannot reach both. Option (e) reworded to the inclusive-or note p.17 does carry, and the stem changed from "why" to "which two statements", since inclusive-or is a clarification rather than the reason the sum is 1 |
| L2-MC-019 | **wrong** | same split across two pages: the alphabetical-sort premise is on p.54, the `factor(levels = ...)` fix on p.51. Reframed on p.51 alone, which means dropping the bar-plot premise. The "passenger class" example in option (e) was also not on p.51 and became "these levels carry a meaningful order" |
| L1-MC-007 | ok | p.26 defines all four terms; the keyed pair (observation unit, sample) is verbatim and option (e) is contradicted by the same page's "ideally the same, but are often not the same" |
| L2-WA-002 | ok | p.31 prints the pipeline verbatim. The answer omits the `round(3)` the slide adds, which is a deliberate omission, not an error |
| L3-MC-003 | **wrong** | option (c) said the mode is the "only" measure that works for categorical data. p.21 says mode is "useful for categorical/bimodal distributions" - "only" is an overstatement the page does not carry. Dropped the word; the key is unchanged and the option is now verbatim |
| L5-MC-006 | ok | p.34 defines parameter and statistic in the keyed words, and its x-bar / mu example is reversed in option (d), so the distractor works |
| L8-MC-011 | ok | p.33 prints X-squared, df = 5, p = 0.9626 and `rep(10, 6)`. Three of the four distractors are contradicted by the same page |
| L9-MC-001 | ok | p.4 carries both: the definition of non-parametric verbatim, and "we will focus on bootstrapping" |
| L2-MC-025 | ok | p.41 carries the base-packages list with mean() and sum() named, and the bundle-of-functions line that option (c) paraphrases |
| L6-WA-007 | **wrong** | the definition half is on p.21 verbatim, but the "state one thing it is NOT" half - the P(H0 true) misconception - appears in no Lecture 6 page; `find_slide.py "p-value"` returns six hits and none of them says it. Stem reworded to ask what the p-value conditions on and what probability is computed, both of which p.21 does print. The misconception is the most valuable thing a student can know here, and it is now absent rather than mis-cited |
| L8-WA-001 | **wrong** | p.18 carries the definition and the curved-relationship warning verbatim, but the answer also offered "driven by an outlier", which the page never mentions. Trimmed to the non-linear case. Also dropped "running from -1 through 0 to 1", which is not on p.18 either |
| L4-WA-008 | **wrong** | the bag example runs over four pages: with replacement on p.34-35, without on p.36-37, and the cited p.37 carries only the second half. Reframed on p.33, which defines both in one sentence each. The 3/10 against 2/9 contrast survives in the detail panel, where it is not the asserted answer |
| L5-WA-002 | **wrong** | p.47 states the CLT precisely and says which statistics it extends to, but "it matters because it lets us use z-scores and confidence intervals" is on no page of Lecture 5. Stem changed to ask for the statement plus the extension, both verbatim on p.47 |
| L5-WA-006 | **wrong** | p.46 says the LLN makes the estimate more accurate, calls Xbar a consistent estimator, and says it does not describe the sample mean's distribution for finite n - which is the whole of the comparison. But stating what the CLT *does* give is p.47. Answer rewritten to stay on p.46 and still answer the question |
