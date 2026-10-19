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

What can be said: band E holds 127 questions, the four batches logged at the
bottom of this table read 34 of them, and 15 of the 58 entries in this table
are wrong.

The error rate by batch is the interesting part, because the batches were read
in score order and the rate is not flat:

| batch | score range read | read | wrong |
|-------|------------------|-----:|------:|
| 1 | 0.301 - 0.351 | 6 | 4 |
| 2 | 0.357 - 0.403 | 12 | 6 |
| 3 | 0.401 - 0.403 | 8 | 2 |
| 4 | 0.403 - 0.419 | 8 | 0 |

67%, then 50%, then 25%, then nothing. That is the concentration hypothesis
holding up: the errors sit at the low end of band E, not evenly through it. It
also means the band's headline "9%" was measured somewhere else and does not
describe its first 34 questions. Extrapolating either number to the remaining 93
would be guessing, and the two guesses differ by a factor of four.

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
| L8-MC-002 | **superseded** | read twice, once in an early batch and once in band E. Both verdicts were ok and p.16 does print the cor.test block, so nothing is in dispute; the second entry, further down, is the fuller one. Row kept rather than deleted so the double read stays visible. Any count of this log must deduplicate by id: this one id appears twice |
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
| L4-MC-004 | **wrong** | p.17 carries the deck, the sum, and the complementary definition - but the P(Aá¶œ) = 1 - P(A) rule in option (e) is on p.49 (and p.18). One page cannot reach both. Option (e) reworded to the inclusive-or note p.17 does carry, and the stem changed from "why" to "which two statements", since inclusive-or is a clarification rather than the reason the sum is 1 |
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
| L1-MC-005 | **wrong** | p.25 ends on "Large sample size doesn't fix biased sampling!", but option (c) also said it "reduces random error" - `find_slide.py "random error"` returns nothing in Lecture 1, and the same phrase opens the explanation. Trimmed the option and rewrote the explanation off the page's own sentences. Same defect as L3-MC-002: a correct option that is half on the page and half imported |
| L2-MC-006 | ok | p.34 is the grouped bar plot itself: `aes(x = class, fill = survived)` with `position = "stack"`, which is both keyed options |
| L2-MC-010 | ok | p.48 carries `[1, ]` as the first row, `[, 3]` as the third column, and the positional-index note. Read it wrong the first time and nearly "fixed" a key that was already right - the lesson from rebalance_pairs, repeated |
| L5-MC-003 | ok | p.21 defines PMF, PDF and CDF in three clauses and the keyed two are verbatim |
| L5-MC-016 | ok | p.39 defines independent and identically distributed in the keyed words, with the coin-toss examples |
| L5-WA-003 | **wrong** | p.38 carries the whole derivation and "the variance of the sample mean decreases, making the sample mean a more precise estimate". The answer added "approaching zero only in the limit", which the page does not say. Trimmed |
| L7-MC-015 | ok | p.52 states the independence assumption, the before-and-after pairing, and that sleep is paired data - so the keyed pair and the three distractors are all on the page |
| L9-MC-009 | ok | p.16 gives the code, the 30 and 365, the exact answer and the counter, which contradicts distractors (d) and (e) directly |
| L5-WA-007 | ok | p.15 names all three distributions with the same three examples the stem uses: coin tosses, events per fixed interval, and heights as natural measurements |
| L9-MC-003 | ok | p.6 carries both keyed options verbatim, the law of large numbers and the standard errors / confidence intervals / p-values sentence |
| L7-MC-005 | ok | p.35 defines alpha, beta, power, and the trade-off. Option (e) says reducing alpha "always" reduces beta, which the same page contradicts with "often increases" |
| L8-MC-014 | ok | p.9 carries the formula and the two sentences behind both keyed options, including "unitless" |
| L9-MC-007 | ok | p.19 prints `numeric(N)` and then the `bootstrap_means[i] <- ...` line, which is both keyed options |
| L2-MC-004 | ok | p.31 output shows every row summing to 1, which is the keyed second option; margin = 1 is in the printed code |
| L1-MC-016 | ok | p.51 prints the list with `[[1]]` numeric and `[[2]]` character, so two of the five options are decided by the page alone |
| L9-WA-002 | ok | p.12 prints the whole pipeline including `rnorm(N, mean = 3, sd = 1)` and 0.25186. The R check already covers the 0.25 claim |
| L2-MC-021 | **wrong** | the question tested `table()` on a vector with an NA and keyed "does not include NA by default". p.28 shows `table(titanic_data$class)` and its counts and says nothing about missing values - and `find_slide.py` finds no Lecture 2 page on NA in table. Reframed on the frequency table p.28 does print. The NA behaviour is true R and has no slide, so it is gone from the answer |
| L9-MC-006 | **wrong** | the question was "why is `set.seed()` used", keyed on reproducibility. `set.seed` appears in four Lecture 9 pages and is explained in none, and `find_slide.py "reproducib"` returns **zero hits in the entire course**. Reframed onto what p.16 does carry: the simulated 0.7103 against the exact 0.706, and what the product formula counts |
| L3-MC-020 | ok | p.60 lists all three reasons for merging and two are keyed. Nearly "fixed" a key that was already right - the reading snapshot wraps long option lines and the second asterisk is easy to lose |
| L2-MC-015 | ok | p.52 shows `arrange(fare, descending = TRUE)` and `select(...)` with both comments, so the keyed pair is demonstrated. The option writes `desc(fare)` where the slide writes `descending = TRUE`; the behaviour is the page's, only the syntax is imported |
| L4-WA-003 | ok | p.43 prints the MTO table and the whole 14/72 over 24/72 = 14/24 = 0.58 chain. The three literals are already carried in ACCEPTED for this question |
| L5-MC-004 | ok | p.30 ends "The CDF is a step function that increases at each possible outcome", which is option (e) verbatim, and the printed CDF column gives 0.67 at x = 4. Worth knowing: the slide *asks* about P(X <= 4) and then works the example through P(X <= 3) = 1/2. The option is still right, from the CDF values, but the slide is off by one |
| L6-WA-008 | ok | p.19 prints the pnorm call in three equivalent forms with 4.370914e-07, and the answer uses the first. Already logged in an earlier pass; re-read and unchanged |
| L8-MC-013 | ok | p.16 prints the whole cor.test block including `sample estimates: cor 0.6199323` and the sentence about positive correlation, so both keyed options are on the page |
| G-MC-003 | **wrong** | not a citation error: the question is broken. tools/figures.py draws group A as min 10, Q1 22, median 30, Q3 38, max 50, so "The range of group A is 40" and "At least 75% of the values lie between 10 and 50" are both **true of the figure the question points at**, and neither was keyed. The explanation dodged this by claiming "the whiskers are not necessarily the true extremes", which is a convention, not a fact about this drawing. Three distractors rewritten against the actual five numbers |
| L3-WA-002 | **wrong** | p.35 defines the quartiles and the five numbers of a box plot, and nothing else. The answer's second half - the variance squares deviations, so prefer the IQR under skew - is p.28 and p.21, not p.35. Reframed on the quartiles alone. The skew argument survives in the detail, marked as a property of the measures rather than a claim of the page |
| L2-MC-023 | ok | p.23 is the type table itself: gender and country are the two Nominal rows, and the other three distractors are Continuous, Ordinal and Binary on the same page |
| L3-MC-014 | ok | p.57 prints `z <- c(TRUE, "FALSE")` and the note "z becomes character". A three-option question with one correct, inside the format rule |
| L4-MC-015 | ok | p.13 lists all five random variables with their supports. Option (c) is false because of its justification, not its subject: the die *is* discrete, but not because it is a physical object |
| L5-MC-009 | ok | p.37 carries both keyed options: "on average, it hits the true population mean", and "with small samples, there is still a lot of variability" |
| L7-MC-008 | ok | p.41 states both directions verbatim, including "the (1 - alpha) CI contains all values of mu0 that would not be rejected at the alpha significance level for this particular sample" |
| L6-MC-003 | **wrong** | p.17 has the computation and the SE reading, but the "~95% within +/-2 SE" rule in option (c) is on **p.18** - another page, same shape. Rather than leave a five-option question needing two pages, option (c) is gone and the question is now four options with one correct, which the format rule allows. The rule itself is not lost: it is in the p.18 material and is worth its own question later |
| L8-MC-007 | **correction** | this entry was wrong when first written and said the two-group identity was printed nowhere. It is printed on **p.29**, in the next sentence after the post-hoc note: "ANOVA with only two groups gives exactly the same p-value as the two-sample t-test (with equal variances)." Option (e) was correct and on the page, and the rewrite that replaced it has been reverted. The error was a bad search: `find_slide.py "t-test"` misses the sentence because it says "two groups", and the follow-up search for "two groups" hit the page but its output was cut off by `Select-Object -First 6` before reaching Lecture 8. **A negative result from find_slide.py is not evidence of absence until the search phrase matches how the slide actually words it** |
| L1-MC-010 | ok | p.41 prints `2 + 2` giving 4, then `a <- 2 + 2` and `a` giving 4, so both the value and the assignment claim are on the page |
| L2-MC-024 | ok | p.23 is the type table; survived is Logical and class is Ordered factor, and the three distractors are the other three rows of the same table |
| L5-MC-002 | ok | p.15 names all three distributions with their defining phrases, which are the two keyed options |
| L7-MC-010 | ok | p.54 step 3 prints the SE of a proportion and step 5 prints "0.52 +/- 1.96 x 0.022", so both keyed options are on the page |
| L2-MC-008 | ok | p.45 prints the exact function definition, the exact call, and the comment "total defaults to 100, returns 25" |
| L3-MC-004 | ok | p.15 gives the sum-over-n formula in words and in symbols; the arithmetic is the reader's |
| L7-MC-006 | ok | p.38 defines the acceptance region as mu +/- 1.96 s/sqrt(n) and its complement as the rejection region, which is both keyed options |
| L7-WA-003 | ok | p.38 prints the two rejection conditions on the statistic and on the sample mean in the same form the answer uses. The 1.96 and -1.96 claims are now covered by the qnorm checks added with the numeric audit |
| L9-WA-004 | ok | p.4 carries both halves: the definition of non-parametric and the small-sample unreliability of the standard tests |
| L3-MC-015 | **wrong** | not a citation error: option (b) said "TRUE can be coerced to 1 and FALSE to 0", which p.56 states verbatim in its own bullet list, and it was not keyed - so the question had three true options against a two-option key. Reworded to the opposite claim, which the same page contradicts |
| L1-MC-014 | ok | p.52 is the object table itself: "Use L suffix to force integer type" and "x <- 3.14 numeric" are both keyed options, and the other three are contradicted by their own rows |
| L1-MC-015 | ok | p.52 defines matrix as "2D array of same type" and data.frame as "Table of vectors... Columns can be different types", which makes the matrix option false and the data frame option true. Both keys were already right; the reading snapshot was misread, for the fourth time on this review |
| L2-WA-005 | ok | p.45 prints "# by position", "# by name" and the default-valued definition, and the answer's three claims are those three lines |
| L3-MC-005 | ok | p.28 prints the average squared deviation, the s = sqrt(s^2) line and the 10-years example that establishes the unit, so the squared-units claim is the page's own wording |
| L4-MC-014 | ok | p.13 lists the die and the adult height with their supports, and both are keyed. Worth noting rather than fixing: this is a Lecture 4 question citing **Lecture 5**, so it shows up in the Lecture 4 section while its content belongs to the next lecture. Moving it would change the per-lecture counts the validator pins, so it stays and is recorded here |
| L5-MC-007 | ok | p.35 defines all three terms in sequence, and both keyed options are the page's own examples |
| L5-WA-001 | ok | p.35 carries all three definitions and the n = 50, 169.03 example. The two literals are already carried in ACCEPTED for this question |
| L8-WA-002 | **wrong** | p.26 carries the F definition and the alternative "at least one group mean is different", but the post-hoc sentence in the answer is on **p.29**. Trimmed to stop at "not which one", which p.26 does say |
| L1-MC-001 | ok | p.7 prints the study and labels the descriptive and inferential versions in its own words, and both keyed options are those two sentences |
| L3-MC-017 | ok | p.61 is "Keeps only rows with matches in both datasets" with an output showing ids 2, 3 and 4, so both keyed options are on the page. Read as a single-keyed question first and was wrong: the source has ["a", "c"] |
| L9-MC-002 | ok | p.6 gives the definition sentence and the three numbered steps, and both are keyed. Also read as single-keyed first; the source has ["b", "c"] |
| L7-MC-001 | ok | p.25 states "For a given alpha, the confidence level for a one-sided test is 1 - alpha, while for a two-sided test it is 1 - alpha/2" and the tail placement for each, which is both keyed options and the negation of the distractor |
| L8-MC-004 | ok | p.19 defines Spearman as Pearson on the ranks, calls it monotonic and robust to outliers, and gives `method = "spearman"` - so the two distractors that name Kendall or the values are contradicted by the same line |
| L6-MC-001 | **wrong** | p.21 has the four numbered steps, but option (d) defined the standard error as "the standard deviation of the sampling distribution of the estimate", which is **p.15**. Reworded to the formula p.21 does print: the test statistic is the point estimate minus the null value over the standard error |
| L5-WA-004 | **wrong** | p.21 defines the three functions and nothing else. The answer added "a fair die has 1/6 at each face" and "gives no probability at a point", neither of which the page says. Trimmed to its three definitions, keeping the tie to the discrete die that the stem asks for |
| L7-WA-004 | **wrong** | the answer framed the duality as "the 1 - alpha CI contains the null value", which is p.41. p.39 frames it the other way round, as the CI being the acceptance region. Rewritten in p.39's terms, which keeps the same numbers and the same conclusion |
| L2-WA-003 | ok | p.54 prints the pipeline verbatim, output included, plus the `.by` variant. The answer omits `ungroup()`, which is a deliberate omission |
| L3-MC-008 | ok | p.35 prints Q1 as the 25th percentile, Q2 as the median at the 50th and Q3 as the 75th, which is option (e) verbatim and makes Q3 - Q1 a one-step consequence of the page rather than an imported fact. `find_slide.py "IQR"` shows the term itself appears only in two topic lists, so the option rests on the percentiles and not on the name |
| L5-MC-017 | ok | p.46 carries all three keyed claims: more accurate with larger samples, Xbar a consistent estimator, and the extension to proportions, variances and medians. The distractor about medians is contradicted by the same line |
| L6-WA-002 | ok | p.21 gives all four steps with the same mu = 170 example and the p ~ 0 conclusion |
| L7-MC-004 | ok | p.35 defines Type I as rejecting H0 when it is true (false positive). Option (e)'s trailing gloss explains the page's own term rather than adding a new fact, which is the difference between keeping it and the cases that were trimmed |
| L7-WA-002 | ok | p.35 carries both definitions with their symbols, power as 1 - beta, and "reducing one often increases the other", which is the direction the answer's trade-off takes |
| L8-MC-002 | ok | p.16 prints the whole cor.test block and the sentence rejecting H0 with a positive correlation, which is both keyed options |
| L8-MC-006 | ok | p.26 carries the F ratio verbatim and the homoscedasticity assumption with Welch's variant relaxing it, which is option (e) |
| L1-MC-006 | ok | p.26 defines all four terms with exactly the examples in the stem, and the same page's "ideally the same, but are often not the same" is what makes the last distractor false |
| L4-MC-006 | ok | p.21 asks this exact question and answers it: 2/52 + 2/52 = 4/52, disjoint because no card is both. Both keyed options are the page |
| L4-MC-010 | ok | p.29 prints the three conditional probabilities and concludes dependence in one line, which is both keyed options |
| L4-WA-002 | ok | p.17 prints 26/52 + 26/52 = 1 and the complementary definition in the same words the answer uses |
| L6-MC-002 | ok | p.22 prints the general formula, defines each of its three terms, and states the sentence that is option (e) verbatim |
| L7-MC-002 | ok | p.26 is the light-bulb example and carries "at least 1000 hours", which makes H0: mu >= 1000 a one-step consequence and the reversed option the distractor |
| L7-WA-005 | ok | p.31 prints the whole t.test block the question quotes, including the CI endpoints to five decimals |
| L8-MC-012 | **wrong** | not a citation error: the question had **three** true options against a two-option key. Option (a) was "F = 13.915", which p.29 prints, and option (e) was "there is significant evidence that average height differs", which is also on the page - the explanation even said so, while not keying it. Rewritten: (a) now misattributes 1.673 to F, and (e) claims the output identifies which pairs differ, which p.29 explicitly denies with "though we don't know which". Key unchanged at [b, c] |
| L1-MC-009 | ok | p.29 is this exact study - Ph.D. student, friends and department - and prints "introducing sampling bias" and "bias in sampling will lead to incorrect conclusions" in the same order as the two keyed options |
| L2-MC-009 | ok | p.42 labels the two lines "install a package (once per computer)" and "load a package (each new session)", which is both keyed options; attaching is one step from loading |
| L2-WA-004 | ok | p.51 gives R 4.1.0 (2021) and magrittr's %>% verbatim, and its first bullet "chaining operations left-to-right" is the mechanism the answer describes |
| L2-WA-007 | ok | p.34 prints the same ggplot call; the answer drops position="stack", the manual fill colours and the labels, which are styling rather than the mapping the question asks for |
| L6-WA-005 | ok | p.29 lists attrition and item non-response by name and states both consequences - larger standard error, lower power, bias when not random |
| L7-MC-007 | **wrong** | not a citation error: options (c) and (d) were the same sentence, "because the null value 175 lies inside the interval" and "because 175 lies inside the interval". One was keyed and one was not, and the explanation spelled out the duplicate again. Option (d) now says the hypothesis is *accepted*, which p.39 and the rest of the course treat as the error it is; key unchanged at [b, c] |
| L7-WA-001 | ok | p.25 gives the two null/alternative pairs, the tail locations, and the confidence levels 1 - a and 1 - a/2 in the same words the answer uses |
| L7-WA-008 | ok | p.31 prints the t.test call, the statistic and 2 * pt(t_stat, df = 9); n - 1 is the one step from n = 10 with df = 9 |
| L7-WA-009 | ok | p.52 states the independence assumption, names before-and-after on the same subjects as paired, and prescribes differencing within pairs plus paired = TRUE |
| L8-MC-009 | ok | p.31 prints the chi-squared formula and all three test types; the keyed options are its words for the statistic and for independence, the distractors swap the three definitions between them |
| L1-MC-004 | ok | p.25 is the whole Literary Digest story in the same order as the question, ending on "Large sample size doesn't fix biased sampling!", which is option (e) verbatim |
| L1-WA-003 | **wrong** | minor: the answer gave `2L` as the integer example and "SDS1" for character. p.46 prints integer examples 3 and 1 and character examples "sds1" and "norrkoping". `2L` is correct R but is not on the page, so it is now 3; "sds1" was already right, I had only mis-cased it |
| L1-WA-008 | ok | p.25 carries the whole example. The opening clause "reduces random error" is not printed there, but it is the counterpart of the sentence that is, and the load-bearing claim - large sample cannot repair bias - is verbatim. Judgement call, recorded rather than cut |
| L2-WA-006 | ok | p.49 prints all three row-selection forms under "many ways of doing the same thing", character for character, including the dplyr filter it prefers |
| L6-MC-007 | ok | p.29 defines attrition and item non-response in the keyed words, and the last option is a clean trap: the page says missing data *increases* the standard error |
| L8-MC-003 | ok | p.14 prints SE(r) = sqrt((1 - r^2)/(n - 2)), says the statistic is t with n - 2 df, and states H0: rho = 0 vs H1: rho not equal to 0 |
| L8-WA-003 | **wrong** | the question needed two pages. The three types are on p.31; df = k - 1 is on p.32, and p.31 only says df "depends on the number of categories and groups". Dropped the degrees-of-freedom half from stem, answer and rubric, leaving the part p.31 actually prints. **Not lost:** p.32 gives df = k - 1 with k = 6 giving df = 5, and L8-WA-004 still shows df = 5 in its output, so the fact stays in the bank |
| L8-WA-004 | ok | p.33 prints the observed vector, the chisq.test call and the output including X-squared = 1, df = 5, p = 0.9626, and concludes we fail to reject |
| L8-WA-007 | ok | p.9 says the numerator measures the covariance and the denominator standardises by the product of the two standard deviations so r is unitless and between -1 and 1 |
| L9-WA-001 | ok | p.6 numbers the three steps, names the law of large numbers, and defines the simulation in the same sentence the answer uses |
| **correction** | batch 15 commit message | the message ended "Twelve questions left in band E". That is wrong: batch 15 was the last ten and the band is finished. Recomputed against `bandE.txt`, all 126 questions in band E are now in the log. The message also claims "only two of the twenty-eight wrong rows are a fact the slide fails to support", which I have not actually counted and should not have asserted. What is established is the part stated as established: five defects in batches 13-15 were defects of the question rather than of the citation. Left in the history rather than amended, so the record keeps the error visible |
| **correction** | the counting pattern used to track this review | every figure I reported for the last several batches came from the regex `[LG]\d-(?:MC|WA)-\d+`, which requires a digit straight after the letter. The figure questions are named `G-MC-003`, with no lecture digit, so **they were never counted at all**. With that pattern the log showed 136 rows and 0 of the 30 G-* questions, and the "108 pending" figure was really 107: it included G-MC-003, which was already logged. Correct pattern is `(?:[LG]\d|G)-(?:MC|WA)-\d+`. What survives the correction: band E was genuinely finished, because `bandE.txt` contains only L-* ids and all 126 of them are in the log. What does not survive: the claim that the review had covered a stated fraction of the bank, which was never measured correctly |
| **correction** | two mechanical gates proposed after batch 15 | I proposed detecting duplicate options and detecting non-keyed options the explanation echoes, on the reasoning that both defect classes are automatable. Both were implemented and run against all 243 questions before being adopted. Duplicate detection returned 47 candidates, almost all legitimate contrast pairs (row vs column proportions, H0 <= 1000 vs H0 >= 1000), plus normalisation artefacts that strip the operators and report `Q3 + Q1` identical to `Q3 - Q1`. Explanation-echo returned 28 candidates, almost all good explanations: refuting a distractor naturally reuses its words. Neither is adopted. The underlying defect - two options that are the same sentence, one keyed and one not - is not mechanically detectable, because a distractor is designed to be nearly identical to its neighbour |
| **correction** | "the score is a bad signal and the defects are question defects" | that was overstated from 28 questions. Across the whole review the 29 wrong rows are 23 citation-or-page defects, 4 broken questions and 2 content moved aside, so citation defects still dominate at 79 per cent. The score is a poor signal for the G-* family specifically, and for no established reason elsewhere |

## Figure audit (F1 and F2)

`tools/figures.py` draws the ten figures rather than cropping them from the
slides, so every number a G-* question shows on screen exists only in that file.
Verifying the figures against the PDFs - which is what phase F1 was going to do
- is therefore impossible: there is nothing to verify them against.

What can be checked is internal consistency, and doing that for all thirty
figure questions turned up more defects per question than the slide-reading pass
ever managed. Nine questions were wrong; seven are fixed here, and two are
listed as still open below.

| id | figure | verdict |
|---|---|---|
| G-MC-016 | freq_bars | ok - 30 students is 2+5+11+9+3, the figure's own bars |
| G-MC-017 | freq_bars | ok - fewer than 20 books is 2+5=7 of 30 |
| G-MC-018 | freq_bars | ok - books read is quantitative discrete |
| G-WA-008 | freq_bars | ok - total, mode (the bar of 11 at 20-29) and 7/30 all check out |
| G-WA-010 | bar_stacked | **wrong**, fixed - the answer said women's bars "shrink steadily from Never" and that men read more often, but the data were women [29, 30, 27, 14] against men [18, 22, 34, 26]: the two groups had the *same* mean of 25, and women's bars rose before they fell. A figure meant to teach "compare counts across two groups" that shows no difference at all is a bad teaching object, so the data were changed to women [36, 22, 14, 13] and the answer rewritten to match |
| G-MC-001 | boxplots_h | ok - B has the largest IQR (20 against 16 and 2) and the widest range |
| G-MC-002 | boxplots_h | ok - all three medians are drawn at 30 |
| G-MC-003 | boxplots_h | ok - re-verified in this pass; option (a) "about 75% between 22 and 38" is false because the box spans 50%, which the explanation already says |
| G-WA-001 | boxplots_h | ok - widest box and longest whiskers are both B |
| G-MC-004 | hist_skewed | **wrong**, fixed - the explanation claimed the median was "near 2.3". The generated sample has a median of 3.28. The number was replaced with a non-numeric statement, because any specific median is a snapshot of a seeded sample that drifts between runs, which is the same trap as G-MC-008 |
| G-MC-005 | hist_skewed | **wrong, still open** - the stem asks which of "the first plot" and "the second plot" is right-skewed and the explanation discusses "the second", but only one histogram is displayed. The question cannot be answered from the screen |
| G-WA-002 | hist_skewed | ok - the long right tail is what pulls the mean up |
| G-MC-006 | hist_symmetric | **weak, still open** - the stem posits two histograms while one is shown. The answer is right for the hypothetical, but nothing on screen matches the stem |
| G-WA-009 | hist_symmetric | **weak, still open** - same mismatch as G-MC-006 |
| G-MC-012 | density_overlay | ok - B is centred further right and drawn wider |
| G-MC-013 | density_overlay | **wrong, still open** - the stem says "the area under a density curve for one group is much larger", but a density is normalised to total area 1, which the explanation itself says. The premise is impossible on the figure that is displayed |
| G-WA-006 | density_overlay | ok - B is flatter and wider, A taller and narrower |
| G-WA-011 | normal_shaded | **wrong**, fixed - the answer gave P(5 < X < 6.2) as P(a) + P(b). Region a is shaded 5 to 6.2 and region b 6.2 to 7.4, so adding b gives P(5 < X < 7.4). The answer's own reasoning was self-defeating: it named both boundaries and then claimed the sum stopped at 6.2 |
| G-WA-012 | normal_shaded | ok - the rightmost region is P(X > 7.4) = P(c) |
| G-MC-007 | ci_dotplot | **wrong**, fixed - the explanation quoted A's interval as 48.6 to 56.2, the bounds from before this audit changed them |
| G-MC-008 | ci_dotplot | **wrong**, fixed - the explanation said "Group A's spans about 7.6 units and Group B's about 3.8". Both spans are 7.6; 3.8 is B's *half* width. Option (a) "They are equal" was therefore true and unkeyed |
| G-MC-009 | ci_dotplot | ok - an interval containing the reference means the difference is not significant at 5% |
| G-WA-003 | ci_dotplot | ok - A's interval sits entirely above the reference |
| G-WA-004 | ci_dotplot | **wrong**, fixed by the same change - "about twice as wide" was false while both spans were 7.6 |
| G-MC-010 | scatter_trend | ok - the generated sample has r near 0.50, positive and moderate |
| G-MC-011 | scatter_trend | ok - r = 0 is a cloud with no trend |
| G-WA-005 | scatter_trend | ok - positive, moderate rather than strong |
| G-MC-014 | corr_heatmap | ok - Hours and Screen at 0.62 is the largest off-diagonal cell |
| G-MC-015 | corr_heatmap | ok - -0.28 is weak and negative |
| G-WA-007 | corr_heatmap | ok - strongest positive 0.62, strongest negative -0.33 |

### Why the figure numbers were never checked

Every G-* number was outside the reach of `verify_numbers.py`, which resolves
numbers against R or against the slide text. A figure's numbers exist in
neither. The `ACCEPTED` table already had G-* entries saying "read off the
figure" - which documented the hole rather than closing it.

Three changes close it:

1. The data each figure draws is hoisted into `FIG_DATA` at module level, so
   there is one place to change a number and it can be imported.
2. `verify_numbers.py` reads that data and checks every number a figure
   question asserts in its answer, explanation, detail or rubric against it,
   allowing derived quantities such as interval widths. It found the stale
   bounds in G-MC-007 and the invented median in G-MC-004 the moment it ran.
3. Multiple-choice explanations are now audited at all. They were not before,
   and an explanation is where a question does its own arithmetic - which is
   where G-MC-008 went wrong.

### What this gate does not catch

It catches numbers with no basis in the figure. It does **not** catch a number
that is wrong but happens to be derivable: in the original `ci_dotplot`, 3.8
was a legitimate half-width of one of the two intervals, so a gate built on
"is this number derivable" would have passed the very sentence that was wrong.
Getting G-MC-008 required reading the sentence, not matching its number.
