"""Lecture 6 - Statistical inference and hypothesis testing."""

from .common import mc, rb, wa

PDF = "lecture6_after.pdf"


def questions():
    out = []

    out.append(mc(
        "L6-MC-001", 6, "Hypothesis testing steps",
        "What are the steps of a hypothesis test?",
        ["Compute the p-value, then reject H0, then state the hypotheses",
         "Formulate H0, compute the test statistic, calculate the p-value, draw "
         "conclusions",
         "Collect data, then choose the test, then report",
         "The standard error used is the standard deviation of the sampling distribution "
         "of the estimate",
         "State Ha, compute the standard error, then stop"],
        ["b", "d"],
        "The four steps are: formulate the null hypothesis, compute the test statistic "
        "which measures how far the estimate sits from what H0 predicts, compute the "
        "p-value of a statistic at least as extreme under H0, and then draw the "
        "conclusion.",
        PDF, "p.21", origin="adapted_HT25"))

    out.append(mc(
        "L6-MC-002", 6, "Test statistic and standard error",
        "What is the general formula for the test statistic?",
        ["test statistic = point estimate / null value",
         "test statistic = (point estimate - null value) / standard error of the estimate",
         "test statistic = point estimate - null value",
         "test statistic = standard error / point estimate",
         "Test statistics follow different distributions depending on the estimator and "
         "the sample size, for example normal, t or chi-squared"],
        ["b", "e"],
        "The test statistic measures how many standard errors the estimate lies from the "
        "null value, so it is the difference divided by the standard error. Reversing the "
        "numerator, as in option (e), only flips the sign and breaks the usual "
        "right-tail convention.",
        PDF, "p.22", origin="adapted_HT25"))

    out.append(mc(
        "L6-MC-003", 6, "Z-scores and the standard error",
        "The population mean is 170 cm, the sample mean is 179 cm and the standard error "
        "is 1.83. What is the z-score, and what does it mean?",
        ["z is about 0.05, so the sample mean is very close to the population mean",
         "z is about 4.9, so the sample mean is about 4.9 standard errors above the "
         "population mean",
         "About 95% of sample means fall within 2 standard errors of the population mean",
         "z is about 4.9, so the sample mean is 4.9 cm above the population mean",
         "z cannot be computed without knowing the standard deviation"],
        ["b", "c"],
        "z = (179 - 170)/1.83 is about 4.9. Because the statistic is in units of standard "
        "errors rather than centimetres, the number describes how many SE away the value "
        "sits, not a distance in cm.",
        PDF, "p.17", code="z <- (179 - 170) / 1.83",
        r_functions=["<-", "-", "/"], origin="adapted_HT25"))

    out.append(mc(
        "L6-MC-004", 6, "Z-scores and the standard error",
        "Consider the R code below. What does it return?",
        ["0.0345",
         "0.9655",
         "4.37e-07",
         "lower.tail = FALSE switches to the upper tail, so this is the probability of "
         "being at or above 179",
         "1.83"],
        ["c", "d"],
        "`lower.tail = FALSE` returns the upper-tail area beyond the value, which is the "
        "p-value here, about 4.37e-07. The value 0.9655 is the lower tail and 0.0345 "
        "belongs to the bottle example from Lecture 5.",
        PDF, "p.19",
        code="pnorm(179, mean = 170, sd = 1.83, lower.tail = FALSE)",
        r_functions=["pnorm", "lower.tail"], origin="adapted_HT25"))

    out.append(mc(
        "L6-MC-005", 6, "P-values",
        "The p-value of a test is about 4.4e-07. What is the correct interpretation?",
        ["There is a 4.4e-07 probability that the null hypothesis is true.",
         "If the null hypothesis were true, the probability of a test statistic at least "
         "as extreme as the observed one is about 4.4e-07.",
         "There is a 4.4e-07 probability that the result is a fluke.",
         "Random sampling variability alone would very rarely produce a result this "
         "extreme if the null hypothesis were true.",
         "4.4e-07 of the sample data are outliers."],
        ["b", "d"],
        "The p-value is always conditional on H0 being true and describes the observed or "
        "more extreme statistic. It is not the probability that H0 is true, and it never "
        "proves anything with certainty.",
        PDF, "p.21", origin="adapted_HT25"))

    out.append(mc(
        "L6-MC-006", 6, "Bias",
        "What is the definition of bias for an estimator?",
        ["Bias(theta-hat) = E[theta-hat] + theta",
         "Bias(theta-hat) = E[theta-hat] - theta",
         "Bias(theta-hat) = theta - E[theta-hat] / n",
         "An estimator is unbiased when its expected value equals the true parameter, "
         "that is when its bias is 0",
         "Bias(theta-hat) = p-value"],
        ["b", "d"],
        "Bias is the expected value of the estimator minus the true parameter, so an "
        "unbiased estimator has Bias = 0. Note that option (c) has the opposite sign, "
        "which would just be a negated bias.",
        PDF, "p.26", origin="adapted_HT25"))

    out.append(mc(
        "L6-MC-007", 6, "Bias and missing data",
        "Which statements are TRUE?",
        ["Missing data can introduce bias only if it is random.",
         "Sampling bias is a type of measurement error rather than of missing data.",
         "Attrition means individuals drop out of a longitudinal study.",
         "Item non-response means individuals skip certain questions in a survey.",
         "Missing data reduces the effective sample size, which decreases the standard "
         "error."],
        ["c", "d"],
        "It is missing data that is NOT random that can introduce bias and invalidate "
        "inference, which is the opposite of the claim that bias arises only when "
        "missingness is random.",
        PDF, "p.29", origin="adapted_HT25"))

    out.append(mc(
        "L6-MC-008", 6, "Confidence intervals",
        "What critical value do you use for a 95% confidence interval for a mean with a "
        "large sample?",
        ["1.28",
         "1.645",
         "1.96",
         "A 95% confidence level corresponds to alpha = 0.05",
         "2.33"],
        ["c", "d"],
        "The two-sided 95% critical value is the 97.5th percentile of the standard normal, "
        "1.96. A common trap is 1.645, which is the 95th percentile and therefore the "
        "critical value for a 90% interval, not 95%.",
        PDF, "p.39", code="qnorm(0.975)", r_functions=["qnorm", "pnorm"],
        origin="adapted_HT25"))

    out.append(mc(
        "L6-MC-009", 6, "Confidence intervals",
        "Which statements about confidence intervals are TRUE?",
        ["A confidence interval is an interval estimate of plausible values for the "
         "population parameter.",
         "About 95% of the sample means would fall inside a given 95% CI.",
         "About 95% of the data points would fall inside a given 95% CI.",
         "Increasing the confidence level from 95% to 99% makes the interval wider.",
         "A single 95% CI lets you be certain the true parameter is inside it."],
        ["a", "d"],
        "The 95% refers to how often intervals computed across many samples cover the "
        "true parameter, not to the data or the sampling distribution, so (b) and (c) are "
        "both wrong. And a single interval still contains uncertainty, so (e) is wrong.",
        PDF, "p.7"))

    out.append(mc(
        "L6-MC-014", 6, "Working with the t-distribution",
        "Which of the following are TRUE statements about the t-distribution functions in "
        "R?",
        ["`dt()` gives quantiles of the t distribution",
         "`pt()` gives the probability of one exact t value rather than a cumulative one",
         "`pt()` gives the cumulative distribution function",
         "`qt()` gives quantiles",
         "`rt()` returns a fixed critical value rather than a random draw"],
        ["c", "d"],
        "`pt()` and `qt()` are the two the code actually uses, and they are inverses of "
        "each other: `qt()` returns the t value at a given tail area, `pt()` returns the "
        "area at or below a given t value. `dt()` is a density and `rt()` draws random "
        "samples, so the claims about them are both wrong. `pt()` is the t-distribution "
        "CDF, not something reserved for the normal.",
        PDF, "p.49", code="pt(qt(0.975, df = 7 - 1), df = 7 - 1)",
        r_functions=["dt", "pt", "qt", "rt"]))

    out.append(mc(
        "L6-MC-010", 6, "Confidence intervals",
        "Why does increasing the confidence level produce a wider interval?",
        ["A higher confidence level requires a smaller critical value",
         "A higher confidence level requires a larger critical value, and the interval "
         "half-width is critical value times standard error",
         "The standard error does not depend on the confidence level, so the widening "
         "comes entirely from the critical value",
         "A higher confidence level increases alpha"],
        ["b", "c"],
        "The interval is point estimate plus or minus critical value times standard "
        "error, and a higher confidence level needs a larger critical value while the "
        "standard error is unchanged. That is the whole reason the interval widens: the "
        "standard error is a property of the estimator and the sample size, and the "
        "confidence level never touches it. A higher confidence level lowers alpha, not "
        "raises it. This is the trade-off: a wider interval is more likely to contain the "
        "parameter but less informative.",
        PDF, "p.48"))

    out.append(mc(
        "L6-MC-011", 6, "Confidence intervals",
        "A 95% confidence interval computed from a population with mean 170 is "
        "(172.06, 177.94). Which statement is TRUE?",
        ["The population mean is 175",
         "The standard error of the sample mean is 1.5",
         "The sample mean is 175",
         "95% of the population falls inside this interval",
         "The interval must contain the true mean because it is a 95% interval"],
        ["b", "c"],
        "The half-width 2.94 equals 1.96 times the standard error, so the standard error is "
        "about 1.5. The interval is built as the point estimate plus or minus that "
        "half-width, so its centre, 175, is the sample mean rather than the population mean. "
        "A confidence interval is an interval for the population parameter, not for the "
        "population values or the sample mean, and even then it is not a certainty.",
        PDF, "p.39"))

    out.append(mc(
        "L6-MC-012", 6, "Confidence intervals",
        "Which statements about the 68-95-99.7 rule are TRUE?",
        ["About 68% of values fall within one standard deviation of the mean.",
         "About 95% fall within two standard deviations.",
         "About 99.7% fall within three standard deviations.",
         "The rule applies to the standard normal distribution and to a normal population.",
         "It says that 95% of confidence intervals contain the population mean."],
        ["a", "b", "c", "d"],
        "That last statement is a true fact but it is about confidence intervals, not the "
        "68-95-99.7 rule, which concerns where individual values fall relative to the "
        "mean.",
        PDF, "p.18"))

    # ----------------------------------------------------------------- written
    out.append(wa(
        "L6-WA-001", 6, "Z-scores and the standard error",
        "The population mean height is 170 cm and the standard error of the sample mean is "
        "1.83 cm. A sample of 30 gives a mean of 179 cm. Without calculating, write down "
        "the formula you would use for the test statistic.",
        "`z = (xbar - mu) / SE = (179 - 170) / 1.83`, which is a z-score of about 4.9, "
        "meaning the observed sample mean sits roughly 4.9 standard errors above the "
        "hypothesised population mean.",
        [rb("Test statistic written as (xbar - mu)/SE", 2),
         rb("Values 179, 170 and 1.83 correctly substituted"),
         rb("States the interpretation in standard error units")],
        1, PDF, "p.17", code="z <- (179 - 170) / 1.83", r_functions=["<-", "-", "/"],
        origin="adapted_HT25"))

    out.append(wa(
        "L6-WA-002", 6, "Hypothesis testing steps",
        "Describe the four steps of a hypothesis test, and state the conclusion when the "
        "resulting p-value is approximately 0.",
        "Formulate the null hypothesis, for example that the sample comes from a population with mean 170. Compute the test statistic, which measures how far the estimate sits from the null in standard-error units, and the p-value. Then conclude: with p near 0, reject H0.",
        [rb("Hypothesis formulation given as step 1", 2),
         rb("Test statistic explained as distance in SE units", 2),
         rb("P-value defined as an H0-conditional tail probability", 2),
         rb("Conclusion of rejecting H0 correctly stated", 2)],
        2, PDF, "p.21", origin="adapted_HT25"))

    out.append(wa(
        "L6-WA-003", 6, "Confidence intervals",
        "Without doing calculations, write down the formula for the 95% confidence interval "
        "for a population mean, and state the formula for any confidence level.",
        "The interval is point estimate plus or minus critical value times standard error, so for 95% it is `(xbar - 1.96 * s/sqrt(n), xbar + 1.96 * s/sqrt(n))`. Sigma is preferred, but s is used when sigma is unknown and n is large enough.",
        [rb("General form given as estimate plus or minus critical value times SE", 2),
         rb("95% critical value 1.96 correctly used"),
         rb("Standard error written as s/sqrt(n)"),
         rb("Notes sigma is preferred but s is used when unknown and n is large")],
        1, PDF, "p.39", r_functions=["qnorm", "sqrt", "sd", "mean"]))

    out.append(wa(
        "L6-WA-004", 6, "Bias",
        "Define bias in terms of the estimator and the true parameter, and explain how "
        "sampling bias would affect a height study.",
        "Bias is the expected value of the estimator minus the true parameter, `Bias(theta-hat) = E[theta-hat] - theta`, and an estimator is unbiased when that is zero. Sampling mainly basketball players would shift the expected sample mean upward, giving positive bias.",
        [rb("Bias defined as E[estimator] minus the true parameter", 2),
         rb("Unbiased estimator correctly identified as having bias of zero", 2),
         rb("Basketball club example used to illustrate upward bias of the mean")],
        1, PDF, "p.26", origin="adapted_HT25"))

    out.append(wa(
        "L6-WA-005", 6, "Bias and missing data",
        "Name two ways missing data can arise besides sampling bias, and explain the "
        "consequence of missing data for a hypothesis test.",
        "Two further sources are attrition, where individuals drop out of a study, and item non-response, where individuals skip particular questions. Missing data reduces the effective sample size, raising the standard error and lowering power, and non-random missing data also introduces bias.",
        [rb("Attrition and item non-response both named", 2),
         rb("Reduced sample size linked to a larger standard error", 2),
         rb("Reduced power correctly identified as the consequence", 2),
         rb("Non-random missing data linked to bias and invalid inference")],
        1, PDF, "p.29", r_functions=["mean", "sd", "sqrt"]))

    out.append(wa(
        "L6-WA-006", 6, "Interpreting a confidence interval",
        "Explain what a 95% confidence interval does and does not tell you, and why it is "
        "described as a random interval.",
        "A 95% CI is an interval of plausible values for the population parameter: across many samples about 95% of intervals built this way would contain the true parameter. It is random because its endpoints move from sample to sample.",
        [rb("Describes the repeated-samples coverage meaning of 95%", 2),
         rb("Explicitly rules out the claim about sample means or data points", 2),
         rb("Explains randomness via sample mean and SE changing between samples", 2)],
        1, PDF, "p.34", r_functions=["qnorm", "pnorm"]))

    out.append(wa(
        "L6-WA-007", 6, "P-values",
        "Explain what a p-value is and state one thing it is NOT.",
        "A p-value is the probability, assuming the null is true, of observing a statistic at least as extreme as the one obtained. It is not the probability that the null is true, and it does not measure the size of an effect.",
        [rb("P-value defined as an H0-conditional tail probability", 2),
         rb("States that it is NOT the probability that H0 is true"),
         rb("Notes it says nothing about effect size or importance")],
        1, PDF, "p.21", r_functions=["pnorm"], origin="adapted_HT25"))

    out.append(wa(
        "L6-WA-008", 6, "Working with the normal distribution",
        "Write the R code to compute the p-value for an observed sample mean of 179 when "
        "the hypothesised mean is 170 and the standard error is 1.83, for an upper-tailed "
        "test.",
        "```r" 
                "```r "
                "pnorm(179, mean = 170, sd = 1.83, lower.tail = FALSE) "
                "``` "
                "`lower.tail = FALSE` returns the upper-tail probability, which is the p-value for an upper-tailed test, about 4.37e-07.",
        [rb("`pnorm()` used with the observed value as the first argument", 2),
         rb("`lower.tail = FALSE` used to obtain the upper tail"),
         rb("Mean 170 and sd 1.83 correctly supplied")],
        1, PDF, "p.19",
        code="pnorm(179, mean = 170, sd = 1.83, lower.tail = FALSE)",
        r_functions=["pnorm", "lower.tail"], origin="adapted_HT25"))

    return out