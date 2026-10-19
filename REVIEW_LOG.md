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
| E | 127 | see below | 8 so far |

Band E is where the mistakes stopped being common: 9% against 67% in band A.
That is the reason for the remaining work rather than a reason to skip it, since
9% of 127 is still about a dozen wrong citations sitting in a study tool.

Correcting a question moves it out of its band, because a fixed citation scores
better. So a question missing from band E has either been fixed or never been
risky enough to be listed - and that is exactly why this log is needed to say
which is which.

## Entries

Read so far: 33. Eight wrong, and **four of those eight were one structural
mistake rather than four separate ones**: a question whose two correct options
are both true, but only one of which the cited page can actually reach. A
citation is one page, so a question that needs two pages is always half-wrong,
and `validate.py` reports it as perfectly formed every time.

A count correction, because this file is only worth having if it is right: the
previous entry said 27 read and "2 wrong", while its own table listed 24 rows and
flagged 2 of them wrong, and the prose named a third (`L7-WA-008`) that was
never given a table row. The figures now above are recounted from the table and
from the batch entries, not carried forward. `L7-WA-008` is still missing a row.

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
| L2-MC-019 | **wrong** | same split across two pages: the alphabetical-sort premise is on p.54, the `factor(levels = ...)` fix on p.51. Reframed on p.51 alone, which means dropping the bar-plot premise. The "passenger class" example in option (e) was also not on p.51 and became "these levels carry a meaningful order", which is |
