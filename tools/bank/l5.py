"""Lecture 5 - Random variables and probability distributions."""

from .common import mc, rb, wa

PDF = "lecture5_after.pdf"


def questions():
    out = []

    out.append(mc(
        "L5-MC-001", 5, "Probability distributions",
        "Which phenomenon is the standard example of a BINOMIAL distribution?",
        ["The height of a randomly chosen adult",
         "The number of heads in 10 tosses of a fair coin",
         "The number of emails received in an hour",
         "The waiting time for a bus",
         "The outcome of a single die roll"],
        ["b"],
        "Binomial counts successes across repeated Bernoulli trials with two outcomes. "
        "Heads in 10 tosses is exactly that. Email counts per interval are Poisson, "
        "height is normal, and a single die roll is a uniform distribution.",
        PDF, "p.15"))

    out.append(mc(
        "L5-MC-002", 5, "Probability distributions",
        "Which statements are TRUE?",
        ["The normal distribution is also called the Gaussian distribution or bell curve.",
         "The Poisson distribution counts events occurring in a fixed interval.",
         "The binomial distribution counts successes in repeated trials.",
         "The number of emails received per hour follows a binomial distribution.",
         "Heights and weights are typical examples of a normal distribution."],
        ["a", "b", "c", "e"],
        "Emails per hour is a Poisson example, not binomial, so (d) is "
        "false. The rest are correct as stated.",
        PDF, "p.15"))

    out.append(mc(
        "L5-MC-003", 5, "PMF, PDF and CDF",
        "Which statements about the three ways of describing a distribution are TRUE?",
        ["A PMF gives the probability of each outcome for a discrete variable.",
         "A PDF describes relative likelihood for a continuous variable.",
         "A CDF gives the probability that a variable is less than or equal to a value.",
         "A PMF can be used for continuous variables.",
         "A CDF is always a step function."],
        ["a", "b", "c"],
        "A PMF is only for discrete variables, and a CDF is a step function only for "
        "discrete variables such as a die; for a continuous variable the CDF is a smooth "
        "curve. Both (d) and (e) are therefore false.",
        PDF, "p.21"))

    out.append(mc(
        "L5-MC-004", 5, "PMF, PDF and CDF",
        "For a fair six-sided die with X the outcome of a roll, what is P(X <= 4)?",
        ["1/6",
         "4/6",
         "3/6",
         "5/6",
         "1/4"],
        ["b"],
        "The CDF adds the probabilities of every outcome up to 4, which is 4 * 1/6 = "
        "4/6 = 2/3. Note this differs from P(X = 4) = 1/6, which is a common confusion.",
        PDF, "p.30", code="sum(rep(1/6, 6)[1:4])",
        r_functions=["rep", "sum", "dbinom"], origin="adapted_HT25"))

    out.append(mc(
        "L5-MC-005", 5, "PMF, PDF and CDF",
        "Consider the R code below. What does it return?",
        ["About 0.034, the probability that a bottle contains less than 35.8 mL",
         "About 0.966, the probability that a bottle contains more than 35.8 mL",
         "About 0.93, the probability that a bottle falls between the two fill bounds",
         "36.2",
         "An error, because sd must be a whole number"],
        ["a"],
        "`pnorm(x, mean, sd)` returns P(X <= x) for a normal variable, which here is the "
        "area under the PDF to the left of 35.8, about 0.0345. Note that the complementary "
        "value 0.9655 is what you would get from 1 minus this.",
        PDF, "p.27", code="pnorm(35.8, mean = 36, sd = 0.11)",
        r_functions=["pnorm"], origin="adapted_HT25"))

    out.append(mc(
        "L5-MC-006", 5, "Parameters and statistics",
        "Which statements about parameters and statistics are TRUE?",
        ["A parameter describes a population characteristic.",
         "A statistic is calculated from a sample.",
         "A parameter changes from sample to sample.",
         "The population mean is written mu and the sample mean with an x-bar.",
         "A statistic is fixed once the population is defined."],
        ["a", "b", "d"],
        "Parameters are fixed population quantities while statistics vary with the "
        "sample, so (c) and (e) are both wrong. The summary is that "
        "parameters are what we want to know and statistics are what we can compute.",
        PDF, "p.34", origin="adapted_HT25"))

    out.append(mc(
        "L5-MC-007", 5, "Estimand, estimator, estimate",
        "Match each term to the correct example for estimating the mean height of all "
        "Norrkoping residents. Which statement is TRUE?",
        ["The estimand is 169.03 cm",
         "The estimator is the sample mean formula",
         "The estimate is mu",
         "The estimand and the estimate are the same thing",
         "The estimator is a fixed number, not a formula"],
        ["b"],
        "The estimand is the unknown population quantity mu, the estimator is the rule or "
        "formula used (here the sample mean), and the estimate is the particular number "
        "obtained from one sample, such as 169.03 cm.",
        PDF, "p.35", origin="adapted_HT25"))

    out.append(mc(
        "L5-MC-008", 5, "Estimand, estimator, estimate",
        "Which statements about an estimator are TRUE?",
        ["An estimator is a function of the data.",
         "An estimator is a random variable.",
         "An estimator is a single fixed number once defined.",
         "The sample mean is an unbiased estimator of the population mean.",
         "An estimator maps the sample space onto numerical values."],
        ["a", "b", "d", "e"],
        "An estimator is a rule rather than a number, and precisely because it maps the "
        "sample space onto values it is itself a random variable. That is what (c) gets "
        "wrong.",
        PDF, "p.35", origin="adapted_HT25"))

    out.append(mc(
        "L5-MC-009", 5, "Sampling distribution and variance",
        "The sample mean is an unbiased estimator of the population mean. What does "
        "\"unbiased\" mean?",
        ["The sample mean always equals the population mean",
         "On average the sample mean hits the true population mean, i.e. E[Xbar] = mu",
         "The sample mean has zero variance",
         "The sample mean is normally distributed",
         "The sample mean is always smaller than the population mean"],
        ["b"],
        "Unbiasedness is a statement about expectation, not about any single sample: the "
        "sample mean can be above or below mu in a given sample, but its expected value "
        "equals mu. The variance is sigma squared over n, which is not zero.",
        PDF, "p.37", origin="adapted_HT25"))

    out.append(mc(
        "L5-MC-010", 5, "Sampling distribution and variance",
        "What happens to the variance of the sample mean as the sample size n increases?",
        ["It increases",
         "It decreases, because Var(Xbar) = sigma^2 / n",
         "It stays constant",
         "It becomes equal to sigma^2",
         "It becomes zero for any n"],
        ["b"],
        "The variance of the sample mean is sigma squared over n, so larger samples give a "
        "more precise estimate. It approaches zero but only reaches it in the limit, so "
        "(e) is false.",
        PDF, "p.38", r_functions=["var", "sqrt", "length"]))

    out.append(mc(
        "L5-MC-011", 5, "Law of large numbers",
        "What does the law of large numbers state?",
        ["As n grows, the sample mean converges to the population mean",
         "As n grows, the sample variance becomes exactly zero",
         "The sample mean is normally distributed for large n",
         "The population is normally distributed",
         "The median always equals the mean for large n"],
        ["a"],
        "The LLN says the sample mean gets arbitrarily close to the population mean as n "
        "grows. Making the sample mean approximately normal is the central limit theorem, "
        "which is a separate and stronger claim, so (c) is not the LLN.",
        PDF, "p.41"))

    out.append(mc(
        "L5-MC-012", 5, "Central limit theorem",
        "What does the central limit theorem state?",
        ["The sample mean converges to the population mean as n grows",
         "For large n the sampling distribution of the sample mean is approximately "
         "normal, whatever the shape of the population",
         "The population must be normally distributed for inference to work",
         "The standard deviation of the sample equals the population standard deviation",
         "The sample size must exceed the population size"],
        ["b"],
        "The CLT is what makes z-based inference possible without knowing the population "
        "shape: the sample mean is approximately normal for large n even when the "
        "population itself is not. Approximate convergence of the mean is the LLN, so (a) "
        "is not the CLT.",
        PDF, "p.47", origin="adapted_HT25"))

    out.append(mc(
        "L5-MC-013", 5, "Central limit theorem",
        "Which statements are TRUE?",
        ["The CLT requires the population to be normal.",
         "The CLT works for any underlying population distribution.",
         "The approximation improves as n grows.",
         "The CLT says the sample mean equals the population mean exactly.",
         "The CLT concerns the sampling distribution of the sample mean."],
        ["b", "c", "e"],
        "Requiring normality is the opposite of the CLT's power, and the theorem is about "
        "the shape of the sampling distribution, not about any sample equalling mu, so "
        "(a) and (d) are false.",
        PDF, "p.50", origin="adapted_HT25"))

    out.append(mc(
        "L5-MC-014", 5, "Random variables",
        "Which statements are TRUE?",
        ["A parameter is a fixed value describing a population characteristic.",
         "A statistic is a value calculated from the sample.",
         "An estimate is the actual value obtained from applying the estimator to one "
         "sample.",
         "An estimator is sometimes called an estimand.",
         "An estimand is a random variable."],
        ["a", "b", "c", "d"],
        "The estimator is sometimes called an estimand, though it is "
        "more precisely the estimand that is the target quantity. The estimand is the "
        "population parameter and so is fixed, not random, which rules out (e).",
        PDF, "p.34"))

    out.append(mc(
        "L5-MC-015", 5, "Shape of a distribution",
        "A distribution is strongly right-skewed. Which statement is TRUE?",
        ["The mean is smaller than the median.",
         "The mean is larger than the median.",
         "The mean and median are always equal for a symmetric distribution.",
         "The median is more affected by outliers than the mean.",
         "The mode cannot be identified for a skewed distribution."],
        ["b"],
        "A long right tail pulls the mean upward, so the mean exceeds the median. The "
        "median is the more robust of the two, which is why the last two options have it "
        "backwards.",
        PDF, "p.23", r_functions=["mean", "median", "quantile"]))

    # ----------------------------------------------------------------- written
    out.append(wa(
        "L5-WA-001", 5, "Estimand, estimator, estimate",
        "For a study estimating the average height of all Norrkoping residents, state the "
        "estimand, the estimator and the estimate.",
        "The estimand is the population mean height of all residents. The estimator is the rule used to compute it, the sample mean Xbar = (1/n) sum of X_i. The estimate is the number that rule produces from one sample, 169.03 cm for n = 50.",
        [rb("Estimand correctly identified as the unknown population mean mu", 2),
         rb("Estimator correctly identified as the sample mean formula", 2),
         rb("Estimate correctly identified as the observed value from one sample")],
        1, PDF, "p.35", origin="adapted_HT25"))

    out.append(wa(
        "L5-WA-002", 5, "Central limit theorem",
        "Explain what the central limit theorem states and why it matters for inference.",
        "The CLT states that for large n the sampling distribution of the sample mean is approximately normal even when the population is not. It matters because it lets us use z-scores and confidence intervals without knowing the population's shape, which is rarely available in practice.",
        [rb("States the approximate normality of the sampling distribution of the mean", 2),
         rb("Notes it holds regardless of the population shape", 2),
         rb("Explains it enables normal-based inference without knowing the population")],
        1, PDF, "p.47", origin="adapted_HT25"))

    out.append(wa(
        "L5-WA-003", 5, "Sampling distribution and variance",
        "Write down the formula for the variance of the sample mean, and explain what "
        "happens to it as n increases.",
        "`Var(Xbar_n) = (1/n^2) * sum of Var(X_i) = (n sigma^2) / n^2 = sigma^2 / n`, using the independence of the observations. As n grows the variance shrinks, so the sample mean becomes a more precise estimate, approaching zero only in the limit.",
        [rb("Variance of sample mean given as sigma squared over n", 2),
         rb("Derivation or intermediate term involving n sigma squared over n squared "
            "shown", 2),
         rb("Explains that larger n gives a more precise estimate")],
        1, PDF, "p.38", r_functions=["var", "mean"]))

    out.append(wa(
        "L5-WA-004", 5, "PMF, PDF and CDF",
        "Explain the difference between a probability mass function, a probability density "
        "function and a cumulative distribution function, and say which applies to a fair "
        "die.",
        "A PMF gives the probability of each individual outcome and applies to discrete variables, so a fair die has 1/6 at each face. A PDF describes relative likelihood across a continuous range and gives no probability at a point. A CDF gives P(X <= x).",
        [rb("PMF defined as the probability of each discrete outcome", 2),
         rb("PDF defined as relative likelihood for a continuous variable", 2),
         rb("CDF defined as P(X <= x) and distinguished as step versus smooth", 2),
         rb("Correctly states the PMF applies to a fair die with value 1/6")],
        1, PDF, "p.21", r_functions=["dbinom", "pbinom", "dnorm", "pnorm"]))

    out.append(wa(
        "L5-WA-005", 5, "Working with the normal distribution",
        "Shampoo bottles have a nominal fill of 36 mL with a standard deviation of 0.11. "
        "Without calculating, write down the R code for the probability that a bottle "
        "contains less than 35.8 mL.",
        "```r\npnorm(35.8, mean = 36, sd = 0.11)\n```\n`pnorm()` returns P(X <= x) for a "
        "normal variable, so this is the area under the PDF to the left of 35.8. The value "
        "is about 0.0345, which is normally rounded to 0.0344.",
        [rb("`pnorm()` used as the correct function", 2),
         rb("Mean and standard deviation supplied as named arguments", 2),
         rb("States that this is P(X <= 35.8), the area to the left")],
        1, PDF, "p.27", code="pnorm(35.8, mean = 36, sd = 0.11)",
        r_functions=["pnorm"]))

    out.append(wa(
        "L5-WA-006", 5, "Law of large numbers",
        "Explain the law of large numbers and how it differs from the central limit "
        "theorem.",
        "The law of large numbers says the sample mean converges to the population mean as the sample grows, so it concerns where the sample mean ends up. The CLT adds that the sampling distribution is approximately normal for large n, a statement about shape.",
        [rb("LLN stated as convergence of the sample mean to the population mean", 2),
         rb("CLT stated as approximate normality of the sampling distribution", 2),
         rb("Relationship between the two explained", 2)],
        1, PDF, "p.47"))

    out.append(wa(
        "L5-WA-007", 5, "Choosing a distribution",
        "For each situation, name the distribution you would expect to model it and give "
        "the reason: the number of heads in 20 coin tosses, the number of customers "
        "arriving in an hour, and the height of a randomly chosen adult.",
        "Heads in 20 tosses is binomial, counting successes across a fixed number of independent trials with two outcomes. Customers in an hour is Poisson, counting events in a fixed interval. Adult height is normal, a roughly symmetric bell-shaped measurement.",
        [rb("Binomial correctly matched to coin tosses with a reason", 2),
         rb("Poisson correctly matched to arrivals per interval with a reason", 2),
         rb("Normal correctly matched to height with a reason")],
        1, PDF, "p.15"))

    out.append(wa(
        "L5-WA-008", 5, "Unbiasedness",
        "Explain what it means to say the sample mean is an unbiased estimator of the "
        "population mean, and why small samples are still a problem even when the "
        "estimator is unbiased.",
        "Unbiased means E[Xbar] = mu, so the estimator is on target in the long run even though a single sample can fall above or below mu. Small samples remain a problem because at small n the variance sigma squared over n is still large.",
        [rb("Unbiasedness explained via E[Xbar] = mu", 2),
         rb("Notes that a single sample may still deviate from mu", 2),
         rb("Explains that large variance at small n causes wide fluctuation")],
        1, PDF, "p.37", r_functions=["mean", "var"]))

    return out