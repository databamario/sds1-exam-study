"""Lecture 8 - Correlation, ANOVA and chi-squared tests."""

from .common import mc, rb, wa

PDF = "lecture8_after.pdf"


def questions():
    out = []

    out.append(mc(
        "L8-MC-001", 8, "Correlation",
        "Which statements about correlation are TRUE?",
        ["A correlation of 1 indicates a perfect positive linear relationship.",
         "A correlation of -1 indicates a perfect negative linear relationship.",
         "A correlation of 0 means the variables are unrelated.",
         "Correlation is a specific measure of association between two continuous "
         "variables.",
         "Correlation requires the two variables to be categorical."],
        ["a", "b", "d"],
        "A correlation near 0 means no LINEAR relationship only, so it can still hide a "
        "strong non-linear pattern, which is why (c) is false. Correlation is defined for "
        "two continuous variables, so (e) is false.",
        PDF, "p.8", r_functions=["cor"]))

    out.append(mc(
        "L8-MC-002", 8, "Testing for correlation",
        "Consider this R output: `t = 5.4738, df = 48, p-value = 1.579e-06`, "
        "`cor = 0.6199323`. Which statements are TRUE?",
        ["The sample correlation is about 0.62.",
         "The test rejects H0: rho = 0 at the 5% level.",
         "There is evidence that income and high-school graduation are positively "
         "correlated.",
         "The 95% confidence interval of about (0.41, 0.77) contains 0.",
         "The test has 48 degrees of freedom."],
        ["a", "b", "c", "e"],
        "The 95% CI of (0.4128, 0.7661) excludes 0, so the statement that it contains 0 is "
        "false. That is also exactly why the test rejects, since a null value outside the "
        "interval means rejection at that level.",
        PDF, "p.16", code="cor.test(states$hs_grad, states$income)",
        r_functions=["cor.test", "cor"], origin="adapted_HT25"))

    out.append(mc(
        "L8-MC-003", 8, "Testing for correlation",
        "Under H0 that rho = 0, what is the standard error of the sample correlation r, and "
        "how many degrees of freedom does the test statistic have?",
        ["SE(r) = sqrt((1 - r^2)/(n - 2)) with n - 2 degrees of freedom",
         "SE(r) = sqrt(r^2/(n - 1)) with n - 1 degrees of freedom",
         "SE(r) = (1 - r^2)/n with n degrees of freedom",
         "SE(r) = sqrt((1 - r^2)/(n - 1)) with n - 1 degrees of freedom",
         "SE(r) = r/sqrt(n) with n degrees of freedom"],
        ["a"],
        "The standard error of r is sqrt((1 - r squared)/(n - 2)) and the statistic follows "
        "a t distribution with n - 2 degrees of freedom, because r is built from two "
        "estimated means rather than one. The lecture also notes this standard error is "
        "only valid when rho = 0.",
        PDF, "p.14", code="sqrt(1 - r^2) / sqrt(n - 2)", r_functions=["sqrt"]))

    out.append(mc(
        "L8-MC-004", 8, "Spearman's correlation",
        "Which statements about Spearman's correlation are TRUE?",
        ["It is the Pearson correlation computed on the ranks of the variables.",
         "It measures monotonic association rather than only linear association.",
         "It is robust to outliers.",
         "It is obtained in R with `cor.test(x, y, method = \"spearman\")`.",
         "It cannot detect a relationship where larger states are richer but not linearly."],
        ["a", "b", "c", "d"],
        "Spearman's coefficient is specifically designed to capture monotonic patterns "
        "that Pearson misses, which is the whole point of the Alaska example where "
        "Pearson said yes and Spearman said no. So the final statement is false.",
        PDF, "p.19", code="cor.test(x, y, method = \"spearman\")",
        r_functions=["cor.test", "method"]))

    out.append(mc(
        "L8-MC-005", 8, "Correlation matrix",
        "Which statements about a correlation matrix are TRUE?",
        ["The matrix is symmetric, so r_xy equals r_yx.",
         "The diagonal is always 1 because each variable is perfectly correlated with itself.",
         "The strongest association in the states matrix is between income and high-school "
         "graduates.",
         "The strongest association in the states matrix is between murder and frost.",
         "A correlation matrix can be computed in R with `select(...) |> cor() |> round(2)`."],
        ["a", "b", "e"],
        "Reading the matrix, the largest off-diagonal value in absolute terms is 0.78 "
        "between murder and life expectancy, so both (c) and (d) are wrong.",
        PDF, "p.20",
        code="states |>\n  select(income, hs_grad, illiteracy, life_exp, murder, frost) |>\n  cor() |> round(2)",
        r_functions=["select", "cor", "round", "|>"]))

    out.append(mc(
        "L8-MC-006", 8, "Analysis of variance",
        "What is the F-statistic in a one-way ANOVA?",
        ["The ratio of the variance between groups to the variance within groups",
         "The ratio of the variance within groups to the variance between groups",
         "The difference between the largest and smallest group means",
         "The total number of observations divided by the number of groups",
         "The ratio of the between-group mean square to the overall mean"],
        ["a"],
        "F is between-group variance over within-group variance. A large F means the group "
        "means differ a lot relative to the noise inside the groups, so the formula is "
        "definitely not the reverse as in (b).",
        PDF, "p.26", origin="adapted_HT25"))

    out.append(mc(
        "L8-MC-007", 8, "Analysis of variance",
        "Which statements about ANOVA are TRUE?",
        ["ANOVA compares means across multiple groups.",
         "The null hypothesis is that all group means are equal.",
         "The alternative is that at least one group mean differs.",
         "Rejecting H0 tells you which specific groups differ.",
         "ANOVA with only two groups gives exactly the same p-value as the two-sample "
         "t-test with equal variances."],
        ["a", "b", "c", "e"],
        "ANOVA is an omnibus test: rejecting H0 only says something differs, not what. "
        "Identifying the differing pairs needs post-hoc tests such as `pairwise.t.test()`, "
        "which the lecture mentions but does not cover, so (d) is false.",
        PDF, "p.29", code="oneway.test(height ~ city, data = heights, var.equal = TRUE)",
        r_functions=["oneway.test", "pairwise.t.test"]))

    out.append(mc(
        "L8-MC-008", 8, "Omnibus tests and multiple testing",
        "The lecture notes that for alpha = 0.05 and m = 190 separate tests, the "
        "probability of at least one Type I error is about 99.3%. What is the consequence "
        "for practice?",
        ["Each individual test should be run at a much smaller alpha.",
         "We should use omnibus tests that make a single decision for all groups at once.",
         "The probability of at least one Type I error is bounded by 0.05.",
         "More tests automatically increase the power of each test.",
         "Type II errors disappear when many tests are performed."],
        ["b"],
        "Because repeated separate decisions accumulate false positives, the solution is a "
        "single omnibus test such as ANOVA, which controls the overall Type I error rate. "
        "Merely shrinking alpha for each test wastes power and does not fix the underlying "
        "problem of repeated decisions.",
        PDF, "p.25"))

    out.append(mc(
        "L8-MC-009", 8, "Chi-squared tests",
        "Which statements are TRUE?",
        ["The chi-squared statistic compares observed counts to expected counts.",
         "A goodness-of-fit test checks whether one variable matches an expected "
         "distribution.",
         "A test for homogeneity checks whether a distribution is the same across groups.",
         "A test for independence checks whether two categorical variables are associated.",
         "The goodness-of-fit degrees of freedom is k, where k is the number of categories."],
        ["a", "b", "c", "d"],
        "For a goodness-of-fit test the degrees of freedom are k - 1, because one parameter "
        "is used up fitting the total, so (e) is false.",
        PDF, "p.30", r_functions=["chisq.test", "pchisq"]))

    out.append(mc(
        "L8-MC-010", 8, "Chi-squared tests",
        "Which of the following are TRUE statements about chi-squared tests?",
        ["For a 2x2 table, the chi-squared test gives the same p-value as the two-proportion "
         "z-test.",
         "Chi-squared tests follow a chi-squared distribution.",
         "A large chi-squared p-value is evidence that the die is unfair.",
         "Goodness-of-fit tests can be carried out in R with `chisq.test()`.",
         "Chi-squared tests can only be applied to continuous variables."],
        ["a", "b", "d"],
        "A p-value of 0.96 is very high, so we fail to reject the hypothesis that the die is "
        "fair, which is the opposite of evidence that it is unfair, so (c) is false. "
        "Chi-squared tests are for categorical and discrete variables, not continuous ones, "
        "so (e) is false.",
        PDF, "p.33", code="chisq.test(observed, p = rep(1/6, 6))",
        r_functions=["chisq.test", "rep"]))

    # ---------------------------------------------- zero-correct special cases
    out.append(mc(
        "L8-MC-011", 8, "Reading R output",
        "Consider this R output. Which statements about it are true?",
        ["X-squared = 1",
         "df = 5",
         "p-value = 0.9626",
         "The test provides evidence that the die is unfair",
         "The expected count for each face is 10"],
        [],
        "Every option here is true. R reports X-squared = 1, df = 5 and p-value = 0.9626, "
        "the die has 60 rolls over 6 faces so each expected count is 10, and a p-value of "
        "0.96 is high, meaning we FAIL to reject the fair-die hypothesis - so there is no "
        "evidence the die is unfair. Remember that on the real exam a question like this "
        "scores the full point if you mark nothing.",
        PDF, "p.33", code="chisq.test(c(8, 10, 9, 12, 11, 10), p = rep(1/6, 6))",
        r_functions=["chisq.test", "rep"]))

    out.append(mc(
        "L8-MC-012", 8, "Reading R output",
        "Consider this ANOVA output from `oneway.test()`. Which statements about it are "
        "true?",
        ["F = 13.915",
         "num df = 2 and denom df = 297",
         "p-value = 1.673e-06",
         "We accept the null hypothesis that all city means are equal",
         "There is significant evidence that average height differs between the cities"],
        [],
        "Every option here is true. R reports F = 13.915 with numerator df 2 and denominator "
        "df 297 and a p-value of 1.673e-06, and such a small p-value means we REJECT H0, "
        "so the cities do differ significantly in mean height. Option (d) states the "
        "opposite of what the output implies. Mark nothing here to score the full point.",
        PDF, "p.29", code="oneway.test(height ~ city, data = heights, var.equal = TRUE)",
        r_functions=["oneway.test"]))

    out.append(mc(
        "L8-MC-013", 8, "Reading R output",
        "Which statements about the following correlation output are true? "
        "`t = 5.4738, df = 48, p-value = 1.579e-06, cor = 0.6199323`.",
        ["The test statistic is 5.4738",
         "The degrees of freedom are 48",
         "The sample correlation is 0.6199323",
         "We fail to reject H0 because the p-value is large",
         "The data provide evidence of a positive correlation"],
        [],
        "Every option here is true. The output reports t = 5.4738, df = 48, p = 1.579e-06 "
        "and cor = 0.6199, and because that p-value is far below any usual significance "
        "level we REJECT H0 and conclude there is a positive correlation. Option (d) says "
        "the opposite. Leaving everything unmarked scores the full point.",
        PDF, "p.16", code="cor.test(states$hs_grad, states$income)",
        r_functions=["cor.test"]))

    # ----------------------------------------------------------------- written
    out.append(wa(
        "L8-WA-001", 8, "Correlation and association",
        "Explain what the correlation coefficient measures, and give one situation where a "
        "correlation near zero would be misleading.",
        "Correlation measures the strength and direction of the LINEAR association between "
        "two continuous variables, running from -1 through 0 to 1. A value near zero only "
        "rules out a linear relationship, so it can be misleading when the true pattern is "
        "curved or driven by an outlier, as in the states example where Alaska alone "
        "produces a moderate Pearson r but almost no Spearman correlation.",
        [rb("Defined as the strength and direction of LINEAR association", 2),
         rb("Notes zero rules out only a linear relationship", 2),
         rb("Gives a valid non-linear or outlier example")],
        1, PDF, "p.18", r_functions=["cor", "cor.test"]))

    out.append(wa(
        "L8-WA-002", 8, "Analysis of variance",
        "Explain what the F-statistic in a one-way ANOVA is, what a large value means, and "
        "what rejecting the null hypothesis does NOT tell you.",
        "The F-statistic is the ratio of the variance between groups to the variance within "
        "groups, and it follows an F distribution with degrees of freedom determined by the "
        "number of groups and the sample size. A large F means the group means differ "
        "substantially relative to the noise inside the groups. Rejecting H0 only shows "
        "that at least one group differs; it does not reveal which groups, which requires "
        "post-hoc tests such as `pairwise.t.test()`.",
        [rb("F defined as between-group variance over within-group variance", 2),
         rb("Explains what a large F indicates", 2),
         rb("Notes the F distribution and its degrees of freedom"),
         rb("States rejection does not identify which groups differ", 2)],
        1, PDF, "p.26", r_functions=["oneway.test", "pairwise.t.test"]))

    out.append(wa(
        "L8-WA-003", 8, "Chi-squared tests",
        "Name the three main types of chi-squared test and state the degrees of freedom for "
        "a goodness-of-fit test with k categories.",
        "The three types are the goodness-of-fit test, which checks whether one variable "
        "matches an expected distribution, the test for homogeneity, which checks whether a "
        "distribution is the same across different populations or groups, and the test for "
        "independence, which checks whether two categorical variables are associated. For "
        "a goodness-of-fit test the degrees of freedom are k - 1, so for a die with k = 6 "
        "faces we get df = 5.",
        [rb("All three test types named with correct purpose", 3),
         rb("Degrees of freedom given as k - 1 with the die example giving 5", 2)],
        1, PDF, "p.31", r_functions=["chisq.test", "pchisq"]))

    out.append(wa(
        "L8-WA-004", 8, "Working in R for a chi-squared test",
        "Write the R code for a goodness-of-fit test of a fair die, given observed counts of "
        "8, 10, 9, 12, 11 and 10 over 60 rolls.",
        "```r\nobserved <- c(8, 10, 9, 12, 11, 10)\nchisq.test(observed, p = rep(1/6, 6))\n```\n"
        "`chisq.test()` with a vector of expected probabilities performs the "
        "goodness-of-fit test; the output is X-squared = 1, df = 5, p-value = 0.9626. Since "
        "the p-value is very high we fail to reject H0 and find no evidence the die is "
        "unfair.",
        [rb("`chisq.test()` used with the observed counts", 2),
         rb("Expected probabilities given as `rep(1/6, 6)`", 2),
         rb("Reports the correct output and conclusion", 2)],
        1, PDF, "p.33",
        code="chisq.test(c(8, 10, 9, 12, 11, 10), p = rep(1/6, 6))",
        r_functions=["chisq.test", "rep", "c"]))

    out.append(wa(
        "L8-WA-005", 8, "Correlation matrix",
        "Explain two properties a correlation matrix always has, and describe how you would "
        "compute one in R for a data.frame with many numeric variables.",
        "A correlation matrix is symmetric, because r_xy equals r_yx, and its diagonal is "
        "always 1, since each variable is perfectly correlated with itself. In R you select "
        "the numeric columns of interest and pipe into `cor()`, typically rounding for "
        "readability, for example `states |> select(income, hs_grad) |> cor() |> round(2)`, "
        "and then read off the strongest off-diagonal entries.",
        [rb("Symmetry correctly identified and justified", 2),
         rb("Diagonal of 1 correctly identified and justified", 2),
         rb("R pipeline with select, cor and round given correctly", 2)],
        1, PDF, "p.20",
        code="states |> select(income, hs_grad) |> cor() |> round(2)",
        r_functions=["select", "cor", "round", "|>"]))

    out.append(wa(
        "L8-WA-006", 8, "Choosing the right test",
        "For each scenario, name the appropriate test: comparing average height across "
        "three cities; whether smoking is independent of eye colour; whether a die is fair; "
        "and whether two continuous variables move together.",
        "Comparing a mean across three cities uses a one-way ANOVA, for example "
        "`oneway.test()`. Whether smoking is independent of eye colour is a chi-squared test "
        "for independence. Whether a die is fair is a chi-squared goodness-of-fit test. And "
        "whether two continuous variables move together is tested with Pearson correlation "
        "via `cor.test()`, or Spearman if the association is non-linear or there are "
        "outliers.",
        [rb("ANOVA correctly matched to comparing three city means", 2),
         rb("Chi-squared independence correctly matched to smoking and eye colour", 2),
         rb("Chi-squared goodness-of-fit correctly matched to the fair die", 2),
         rb("Correlation correctly matched to two continuous variables", 2)],
        1, PDF, "p.40",
        r_functions=["oneway.test", "chisq.test", "cor.test"]))

    return out