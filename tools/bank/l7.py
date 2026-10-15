"""Lecture 7 - More tests and more confidence intervals."""

from .common import mc, rb, wa

PDF = "lecture7_after.pdf"


def questions():
    out = []

    out.append(mc(
        "L7-MC-001", 7, "One-sided vs two-sided tests",
        "How do one-sided and two-sided tests differ?",
        [
        "They differ only in the sample size required.",
        "A one-sided test always uses the t-distribution; a two-sided test uses the normal.",
        "For a given alpha the confidence level of a one-sided test is 1 - alpha while "
                 "that of a two-sided test is 1 - alpha over 2.",
        "A one-sided test has rejection regions in both tails; a two-sided test has "
                 "only one.",
        "A two-sided test has rejection regions in both tails; a one-sided test has the "
                 "rejection region in only one tail.",
         ],
        ["c", "e"],
        "The alternative hypothesis decides the shape: mu != mu0 needs both tails, while "
        "mu > mu0 or mu < mu0 needs one. Consequently the critical values and p-values "
        "differ between the two, and the confidence level that goes with a given alpha is "
        "not the same either: a one-sided test at alpha puts the whole of alpha in one "
        "tail, so it lines up with a confidence level of 1 - alpha, whereas a two-sided "
        "test splits it and lines up with 1 - alpha over 2.",
        PDF, "p.25", origin="adapted_HT25"))

    out.append(mc(
        "L7-MC-002", 7, "One-sided vs two-sided tests",
        "A manufacturer claims light bulbs last at least 1000 hours on average. A sample "
        "of 20 bulbs gives a mean of 975 and a standard deviation of 50. Which test is "
        "appropriate?",
        ["Two-sided, H0: mu = 1000 versus Ha: mu != 1000",
         "One-sided, H0: mu <= 1000 versus Ha: mu > 1000",
         "One-sided, H0: mu >= 1000 versus Ha: mu < 1000",
         "Two-sided, H0: mu = 975 versus Ha: mu = 1000",
         "A one-sided test is right here because the claim being tested is a direction, "
         "at least 1000 hours, rather than an exact value"],
        ["c", "e"],
        "The claim to be challenged is that the mean is at least 1000, so the null sets "
        "mu >= 1000 and the alternative is that the mean is lower. The observed 975 is "
        "below the claimed value, confirming the direction.",
        PDF, "p.26"))

    out.append(mc(
        "L7-MC-003", 7, "One-sided vs two-sided tests",
        "Which statements are TRUE?",
        ["Two-sided tests are more common in practice unless there is strong "
         "justification for a one-sided test.",
         "For a given alpha, the two-sided confidence level is 1 - alpha/2.",
         "For a given alpha, the one-sided confidence level is 1 - alpha.",
         "A one-sided test always yields the same p-value as the two-sided test on the "
         "same data.",
         "A one-sided test has the rejection region in only one tail."],
        ["a", "b", "c", "e"],
        "The p-values do differ because a one-sided test puts all of alpha in one tail, "
        "so (d) is false.",
        PDF, "p.25"))

    out.append(mc(
        "L7-MC-004", 7, "Type I and Type II errors",
        "What is a Type I error?",
        [
        "Using the wrong critical value",
        "Choosing a one-sided test instead of a two-sided one",
        "Failing to reject H0 when it is false",
        "Rejecting H0 when it is true",
        "It is also known as a false positive, since nothing is actually there",
         ],
        ["d", "e"],
        "A Type I error is a false positive: rejecting a null hypothesis that is actually "
        "true. Its probability is the significance level alpha. Failing to reject a false "
        "null is the Type II error.",
        PDF, "p.35", origin="adapted_HT25"))

    out.append(mc(
        "L7-MC-005", 7, "Type I and Type II errors",
        "Which statements are TRUE?",
        ["The significance level alpha is the probability of making a Type I error.",
         "Beta is the probability of a Type I error.",
         "The power of a test is beta rather than one minus beta.",
         "Power is the probability of correctly rejecting H0 when it is false.",
         "Reducing alpha always reduces beta, so power improves."],
        ["a", "d"],
        "There is a trade-off: tightening alpha to reduce false positives typically makes "
        "it harder to reject, which raises beta and lowers power. So the final statement "
        "has the relationship backwards.",
        PDF, "p.35", origin="adapted_HT25"))

    out.append(mc(
        "L7-MC-006", 7, "Acceptance and rejection regions",
        "For a two-sided test at alpha = 0.05, within which values of the test statistic do "
        "you FAIL to reject H0?",
        [
        "z < 1.645",
        "-1.645 <= z <= 1.645",
        "The rejection regions are the two tails beyond plus and minus 1.96, which leave "
                 "the middle as the set of values that do not lead to rejection",
        "z < -1.96 or z > 1.96",
        "-1.96 <= z <= 1.96",
         ],
        ["c", "e"],
        "The rejection regions are the two tails beyond plus or minus 1.96, so the "
        "acceptance region is the interval from -1.96 to 1.96. Using 1.645 would be the "
        "region for a 90% two-sided interval, not 95%.",
        PDF, "p.38", origin="adapted_HT25"))

    out.append(mc(
        "L7-MC-007", 7, "Acceptance and rejection regions",
        "The 95% CI computed for a sample mean is (172.06, 177.94). You test "
        "H0: mu = 175 at the 5% significance level. What is the conclusion, given the "
        "observed sample mean is 173.0?",
        ["Reject H0, because 173.0 is below the interval",
         "Fail to reject H0, because 173.0 lies inside the acceptance region",
         "Fail to reject H0, because the null value 175 lies inside the interval",
         "Fail to reject H0, because 175 lies inside the interval",
         "The test cannot be performed without the standard error"],
        ["b", "c"],
        "For a two-sided test at alpha = 0.05 you fail to reject exactly when the observed "
        "estimate lies inside the corresponding 95% CI. Since 173.0 is between 172.06 and "
        "177.94, H0 is not rejected, and equivalently 175 lies inside the CI.",
        PDF, "p.39", origin="adapted_HT25"))

    out.append(mc(
        "L7-MC-008", 7, "Connection between tests and CIs",
        "What is the relationship between a two-sided hypothesis test at significance "
        "level alpha and a confidence interval?",
        ["A 95% CI always corresponds to a one-sided test at alpha = 0.05",
         "Failing to reject H0 at level alpha is equivalent to the (1 - alpha) confidence "
         "interval containing the null value",
         "The (1 - alpha) CI contains exactly those values of the null parameter that "
         "would not be rejected at the alpha level for this sample",
         "They are unrelated quantities",
         "A 99% CI corresponds to a test at alpha = 0.01 one-sided"],
        ["b", "c"],
        "This duality is the standard link: the null value falls outside the interval "
        "exactly when the test rejects at that level. So (b) and its logic are correct, "
        "while (c) states the opposite of the truth.",
        PDF, "p.43", origin="adapted_HT25"))

    out.append(mc(
        "L7-MC-009", 7, "Differences between means",
        "What is the standard error for the difference between two independent sample "
        "means?",
        ["The two variances are added under the square root, so it is not the sum of the "
         "two standard errors",
         "SE = sqrt(s1^2/n1) + sqrt(s2^2/n2)",
         "SE = sqrt(s1^2/n1 + s2^2/n2)",
         "SE = (s1 + s2)/n",
         "SE = sqrt(s1^2 + s2^2)"],
        ["a", "c"],
        "The variances of the two independent sample means add, so the standard error is "
        "the square root of the sum of s1 squared over n1 and s2 squared over n2. Option "
        "(b) incorrectly adds the two standard errors rather than the two variances.",
        PDF, "p.47", code="se_diff <- sqrt(15^2 / 100 + 20^2 / 100)",
        r_functions=["sqrt", "se_diff"], origin="adapted_HT25"))

    out.append(mc(
        "L7-MC-010", 7, "Proportions",
        "Which statements are TRUE?",
        [
        "Proportions can only be used for continuous variables.",
        "A hypothesis test for a single proportion uses the t-distribution, because the "
                 "population proportion is unknown.",
        "A confidence interval for a proportion is point estimate plus or minus critical "
                 "value times the standard error of the proportion.",
        "The standard error of a sample proportion involves sqrt(p-hat times (1 - p-hat) "
                 "over n).",
        "The standard error of a difference in proportions adds the two standard errors "
                 "rather than the two variances.",
         ],
        ["c", "d"],
        "The proportion machinery is built on the normal approximation to the binomial, "
        "which is why the SE has the familiar squaring form. The claim that proportions "
        "can only be used for continuous variables is false, because proportions are for "
        "categorical, binary-type variables.",
        PDF, "p.54", r_functions=["prop.test", "p_hat"]))

    out.append(mc(
        "L7-MC-011", 7, "Proportions",
        "Consider this R code. What is its purpose?",
        ["To compute the sample proportions directly",
         "To run a two-sample test for equality of proportions between the two groups",
         "To compute a confidence interval for a single proportion",
         "It takes the successes and the totals for each group and compares the resulting "
         "sample proportions",
         "To compute a chi-squared test for independence"],
        ["b", "d"],
        "`prop.test()` with two sets of successes and totals performs a two-sample test of "
        "equal proportions, which is the default alternative, whereas a single vector of "
        "successes and totals would test one proportion.",
        PDF, "p.58", code="prop.test(c(160, 90), c(200, 150))",
        r_functions=["prop.test"], origin="adapted_HT25"))

    out.append(mc(
        "L7-MC-012", 7, "Proportions",
        "Consider this R code. What is the value of `p1_hat_se`?",
        [
        "0.04",
        "0.08",
        "0.0008",
        "Despite its name, the quantity stored in p1_hat_se is a variance, so its square "
                 "root, about 0.028, is the standard error itself",
        "0.0016",
         ],
        ["c", "d"],
        "`p1_hat <- 160/200` is 0.8, and the code computes p1_hat * (1 - p1_hat) / 200 = "
        "0.8 * 0.2 / 200 = 0.0008. Note the misleading name: the quantity computed is a "
        "variance, not a standard error, and its square root 0.028 is the standard error "
        "itself.",
        PDF, "p.48", code="p1_hat <- 160 / 200\np1_hat_se <- p1_hat * (1 - p1_hat) / 200",
        r_functions=["<-", "sqrt"], origin="adapted_HT25"))

    out.append(mc(
        "L7-MC-013", 7, "Choosing the right distribution",
        "When should a t-test be used rather than a z-test?",
        [
        "Only when testing a proportion",
        "When the null hypothesis is one-sided",
        "Always, because R has no z-test function",
        "When the population standard deviation is unknown, so the sample standard "
                "deviation is substituted",
        "With an unknown population standard deviation the t-distribution has heavier "
                 "tails, which absorb the extra uncertainty of estimating the standard deviation",
         ],
        ["d", "e"],
        "The z-test requires knowing the population sigma, which is rarely available, so "
        "substituting s leads to the t-test and its t-distribution. Neither sample size nor "
        "the direction of the alternative decides this.",
        PDF, "p.21", r_functions=["t.test", "pnorm", "qt"], origin="adapted_HT25"))

    out.append(mc(
        "L7-MC-014", 7, "Computing p-values in R",
        "Consider the code below. What does it compute?",
        ["A one-sided p-value from a z-statistic",
         "A two-sided p-value for a t-test with 9 degrees of freedom",
         "It doubles the lower-tail probability so that both tails are counted, which is "
         "what makes the result two-sided",
         "The critical value for a 95% t interval",
         "The probability of a t statistic equal to t_stat"],
        ["b", "c"],
        "`2 * pt(t_stat, df = 9)` takes the lower tail and doubles it, which is how you get "
        "a two-sided p-value from a t statistic, and `df = 9` fixes the degrees of freedom "
        "at 9. The normal equivalent would use `pnorm()` instead of `pt()`.",
        PDF, "p.58",
        code="p_value <- 2 * pt(t_stat, df = 9)",
        r_functions=["pt", "pnorm", "t_stat"]))

    # ----------------------------------------------------------------- written
    out.append(wa(
        "L7-WA-001", 7, "One-sided vs two-sided tests",
        "Explain the difference between a one-sided and a two-sided hypothesis test, and "
        "state how the confidence level differs between them for a given alpha.",
        "A two-sided test has the alternative mu != mu0, with the rejection region in both tails; a one-sided test has mu > mu0 or mu < mu0, in one tail. A one-sided test matches level 1 - alpha, a two-sided test 1 - alpha/2.",
        [rb("Two-sided described as alternative mu != mu0 with both tails", 2),
         rb("One-sided described as one direction with a single tail", 2),
         rb("Correctly gives confidence levels 1 - alpha and 1 - alpha/2", 2),
         rb("Notes the critical values and p-values therefore differ")],
        1, PDF, "p.25", r_functions=["pnorm", "qnorm"], origin="adapted_HT25"))

    out.append(wa(
        "L7-WA-002", 7, "Type I and Type II errors",
        "Define a Type I and a Type II error, give the symbol for each, and explain the "
        "trade-off between them.",
        "A Type I error, probability alpha, is rejecting a true H0. A Type II error, probability beta, is failing to reject a false H0, and power is 1 - beta. Tightening alpha makes rejection harder, which raises beta and lowers power.",
        [rb("Type I defined as rejecting a true H0, symbol alpha", 2),
         rb("Type II defined as failing to reject a false H0, symbol beta", 2),
         rb("Power correctly given as 1 - beta", 2),
         rb("Trade-off between alpha and beta explained")],
        1, PDF, "p.35", origin="adapted_HT25"))

    out.append(wa(
        "L7-WA-003", 7, "Acceptance and rejection regions",
        "For a two-sided z-test at alpha = 0.05, write down the condition on the test "
        "statistic under which you reject H0, and the corresponding condition on the "
        "sample mean.",
        "You reject H0 when the statistic falls outside plus or minus 1.96, that is when `(xbar - mu0) / (s/sqrt(n))` is below -1.96 or above 1.96. Equivalently `xbar < mu0 - 1.96 * s/sqrt(n)` or `xbar > mu0 + 1.96 * s/sqrt(n)`.",
        [rb("Rejection condition on the test statistic given as beyond plus or minus 1.96", 2),
         rb("Equivalent condition on the sample mean derived", 2),
         rb("Acceptance region identified as mu0 plus or minus 1.96 times s/sqrt(n)", 2)],
        1, PDF, "p.38", r_functions=["qnorm", "sqrt", "sd", "mean"], origin="adapted_HT25"))

    out.append(wa(
        "L7-WA-004", 7, "Connection between tests and CIs",
        "Explain how a hypothesis test and a confidence interval relate, using an example "
        "with a 95% CI of (172.06, 177.94) and a test of H0: mu = 175.",
        "For a two-sided test you fail to reject H0 exactly when the corresponding 1 - alpha confidence interval contains the null value. Here 175 lies inside (172.06, 177.94), so at the 5% level we fail to reject H0.",
        [rb("Duality between test at level alpha and the 1 - alpha CI stated", 2),
         rb("States that rejection happens when the null value is outside the interval", 2),
         rb("175 correctly identified as lying inside the interval"),
         rb("Conclusion of failing to reject correctly drawn", 2)],
        1, PDF, "p.39", origin="adapted_HT25"))

    out.append(wa(
        "L7-WA-005", 7, "Working in R for a hypothesis test",
        "Explain how this R output should be read: `t = -1.1859, df = 9, p-value = 0.266`, "
        "`alternative hypothesis: true mean is not equal to 75`, "
        "`95 percent confidence interval: 66.27714 77.72286`, `mean of x 72`.",
        "One-sample two-sided t-test of the sample mean against 75, statistic -1.1859 on "
        "9 df. The p-value 0.266 is above 0.05, so we fail to reject H0; consistently, "
        "the 95% CI (66.28, 77.72) contains 75. The sample mean is 72.",
        [rb("Identifies the test as a one-sample t-test against a null value of 75", 2),
         rb("States the alternative is two-sided, mean not equal to 75"),
         rb("Reports the test statistic and degrees of freedom"),
         rb("Draws the correct decision at the 5% level from p = 0.266", 2),
         rb("Links the decision to the CI containing 75")],
        2, PDF, "p.27", code="t.test(sampl, mu = 75, alternative = \"two.sided\")",
        r_functions=["t.test"],
        origin="adapted_HT25"))

    out.append(wa(
        "L7-WA-006", 7, "Differences between means",
        "Two independent groups have sample standard deviations 15 and 20 with sample "
        "sizes 100 and 100. Without calculating the final number, write down the formula "
        "for the standard error of the difference in means.",
        "`SE(xbar1 - xbar2) = sqrt(s1^2/n1 + s2^2/n2) = sqrt(15^2/100 + 20^2/100)`, "
        "obtained by adding the two variances under the square root because the samples "
        "are independent. If the samples were paired you would instead work with the "
        "differences within pairs.",
        [rb("Formula given as sqrt of the sum of the two variances", 2),
         rb("Substitutes 15^2/100 and 20^2/100"),
         rb("Notes the independence assumption", 2)],
        1, PDF, "p.47", code="se_diff <- sqrt(15^2 / 100 + 20^2 / 100)",
        r_functions=["sqrt", "se_diff"]))

    out.append(wa(
        "L7-WA-007", 7, "Proportions",
        "Without doing calculations, write down the formula for the standard error of a "
        "sample proportion p-hat from a sample of size n.",
        "`SE(p-hat) = sqrt(p-hat * (1 - p-hat) / n)`. It takes the same shape as the "
        "standard error of the mean, and a confidence interval is then p-hat plus or minus "
        "the critical value times this standard error.",
        [rb("Formula given as sqrt of p-hat(1 - p-hat)/n", 2),
         rb("Connects it to the CI form estimate plus or minus critical times SE", 2)],
        1, PDF, "p.54", code="se <- sqrt(p_hat * (1 - p_hat) / 500)",
        r_functions=["sqrt", "p_hat"], origin="adapted_HT25"))

    out.append(wa(
        "L7-WA-008", 7, "Choosing the right distribution",
        "Explain why a t-test is used when the population standard deviation is unknown, "
        "and write the R code for a two-sided one-sample t-test.",
        "A z-test requires the population standard deviation sigma, which is never known. Substituting s makes the statistic follow a t-distribution with n - 1 df, so critical values come from `qt()`. Two samples use `t.test(x, y)`, one against a null `t.test(x, mu = 50)`.",
        [rb("Explains the z-test needs the unknown population sigma", 2),
         rb("States that substituting s gives a t-distribution with n - 1 df", 2),
         rb("Gives the R code for a two-sided one-sample t-test", 2)],
        1, PDF, "p.21", code="t.test(x, mu = 50)", r_functions=["t.test", "qt", "qnorm"],
        origin="adapted_HT25"))

    # ---- paired data, L7 p.52. The bank had nothing on it: the two-sample
    # interval and test that L7-WA-006 practises both rest on independence,
    # and the slide that says so is a single paragraph later.
    out.append(mc(
        "L7-MC-015", 7, "Paired data and independence",
        "Which statements about paired data and the independence assumption "
        "are true?",
        ["The confidence interval and the test for a difference in means assume "
         "the two samples are independent",
         "Two measurements taken from the same subject can be analysed as "
         "independent samples",
         "Taking two draws from the same population satisfies the independence "
         "assumption",
         "For before-and-after measurements on the same subjects, the pairing "
         "must be accounted for",
         "The sleep dataset is an example of two independent samples"],
        ["a", "d"],
        "Both the interval and the test rest on the two samples being "
        "independent, and paired measurements on the same subjects break that, "
        "so (a) and (d) are correct. Two values from one subject share "
        "everything about that subject, which is exactly the mistake (b) makes. "
        "Drawing twice from a single population says nothing about whether the "
        "same individuals were measured twice, so (c) does not follow. The "
        "sleep dataset is paired, not independent, so (e) is wrong.",
        PDF, "p.52"))

    out.append(mc(
        "L7-MC-016", 7, "Analysing paired data",
        "The samples are paired. What is the correct way to analyse them?",
        ["Pass paired = TRUE to t.test()",
         "Run two separate one-sample tests and compare their p-values",
         "Count each pair as two observations to double the sample size",
         "Compute the difference within each pair and analyse those differences "
         "as a single sample",
         "Discard one measurement from each pair so that the data become "
         "independent"],
        ["a", "d"],
        "For paired data the differences within each pair are computed and then "
        "analysed as a single sample, and paired = TRUE is what makes t.test() "
        "do that, so (a) and (d) are correct. Two separate one-sample tests "
        "never compare the two conditions against each other, so (b) does not "
        "answer the question. Counting a pair as two observations pretends the "
        "same subject contributes independent information twice, and discarding "
        "a measurement simply throws data away; neither is what pairing "
        "requires.",
        PDF, "p.52"))

    out.append(wa(
        "L7-WA-009", 7, "Paired data",
        "A study measures each subject's resting heart rate before and after a "
        "training programme. Why is it wrong to treat the two sets of "
        "measurements as independent samples, and what should be done instead?",
        "The two samples are paired, not independent: each before value and "
        "its after value come from the same subject. Compute the difference "
        "within each pair and analyse those differences as a single sample, "
        "using paired = TRUE in t.test().",
        [rb("Identifies the two samples as paired rather than independent"),
         rb("Explains that each pair comes from the same subject"),
         rb("Says to compute the within-pair differences"),
         rb("Says to analyse those differences as a single sample")],
        1, PDF, "p.52",
        r_functions=["t.test"]))

    return out