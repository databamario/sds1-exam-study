"""Lecture 5 - Random variables and probability distributions."""

from .common import mc, rb, wa

PDF = "lecture5_after.pdf"
PDF3 = "lecture3.pdf"


def questions():
    out = []

    out.append(mc(
        "L5-MC-001", 5, "Probability distributions",
        "Which phenomenon is the standard example of a BINOMIAL distribution?",
        [
        "The waiting time for a bus",
        "The outcome of a single die roll",
        "The height of a randomly chosen adult",
        "The number of heads in 10 tosses of a fair coin",
        "The number of yes answers in 10 yes/no survey questions",
         ],
        ["d", "e"],
        "Binomial counts successes across repeated Bernoulli trials with two outcomes. "
        "Heads in 10 tosses is exactly that, and so is the number of yes answers in 10 "
        "yes/no questions. Email counts per interval are Poisson, height is normal, and a "
        "single die roll is a uniform distribution.",
        PDF, "p.15"))

    out.append(mc(
        "L5-MC-002", 5, "Probability distributions",
        "Which statements are TRUE?",
        ["The number of emails received per hour follows a binomial distribution.",
         "The normal distribution is also called the Poisson distribution.",
         "The Poisson distribution counts events occurring in a fixed interval.",
         "The binomial distribution counts successes in repeated trials.",
         "Heights and weights are typical examples of a binomial distribution."],
        ["c", "d"],
        "The two counting distributions are Poisson, for events in a fixed interval such "
        "as emails per hour, and binomial, for successes across repeated trials with two "
        "outcomes. The normal is the bell curve and is the one heights and weights follow, "
        "not the binomial, and it is not another name for the Poisson.",
        PDF, "p.15"))

    out.append(mc(
        "L5-MC-003", 5, "PMF, PDF and CDF",
        "Which statements about the three ways of describing a distribution are TRUE?",
        ["A PMF gives the probability of each outcome for a discrete variable.",
         "A PDF gives the probability of a continuous variable taking one exact value.",
         "A CDF gives the probability that a variable is less than or equal to a value.",
         "A PMF can be used for continuous variables.",
         "A CDF is always a step function."],
        ["a", "c"],
        "A PMF is only for discrete variables, and a CDF is a step function only for "
        "discrete variables such as a die; for a continuous variable the CDF is a smooth "
        "curve. A PDF is a density rather than a probability, and the probability of a "
        "continuous variable landing on one exact value is 0, which is why probabilities "
"are read off a PDF as an area over a range.",
      PDF, "p.21"))

    out.append(mc(
        "L5-MC-004", 5, "PMF, PDF and CDF",
        "For a fair six-sided die with X the outcome of a roll, what is P(X <= 4)?",
        ["1/6",
         "4/6",
         "3/6",
         "5/6",
         "For a discrete variable the CDF is a step function that jumps at each possible "
         "outcome"],
        ["b", "e"],
        "The CDF adds the probabilities of every outcome up to 4, which is 4 * 1/6 = "
        "4/6 = 2/3. Note this differs from P(X = 4) = 1/6, which is a common confusion, and "
        "that 3/6 is the answer to P(X <= 3) rather than to this question.",
        PDF, "p.30", code="sum(rep(1/6, 6)[1:4])",
        r_functions=["rep", "sum", "dbinom"], origin="adapted_HT25"))

    out.append(mc(
        "L5-MC-005", 5, "PMF, PDF and CDF",
        "Consider the R code below. What does it return?",
        ["About 0.034, the probability that a bottle contains less than 35.8 mL",
         "About 0.966, the probability that a bottle contains more than 35.8 mL",
         "About 0.93, the probability that a bottle falls between the two fill bounds",
         "The area under the density curve to the left of 35.8, which is the probability "
         "of being at or below it",
         "An error, because sd must be a whole number"],
        ["a", "d"],
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
         "The population mean is written x-bar and the sample mean with mu.",
         "A statistic is fixed once the population is defined."],
        ["a", "b"],
        "Parameters are fixed population quantities while statistics vary with the "
        "sample, so the claim that a parameter changes from sample to sample is wrong, as "
        "is the claim that a statistic is fixed once the population is defined. The "
        "notation goes the other way round: mu for the population mean, x-bar for the "
        "sample mean. The summary is that parameters are what we want to know and "
        "statistics are what we can compute.",
        PDF, "p.34", origin="adapted_HT25"))

    out.append(mc(
        "L5-MC-007", 5, "Estimand, estimator, estimate",
        "Match each term to the correct example for estimating the mean height of all "
        "Norrkoping residents. Which statement is TRUE?",
        [
        "The estimand and the estimate are the same thing",
        "The estimator is a fixed number, not a formula",
        "The estimand is 169.03 cm",
        "The estimator is the sample mean formula",
        "The estimate is the number obtained after applying that formula to one sample, "
                 "such as 169.03 cm",
         ],
        ["d", "e"],
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
         "The sample mean is a biased estimator of the population mean.",
         "An estimator produces one fixed number that does not change between samples."],
        ["a", "b"],
        "An estimator is a rule rather than a number, and precisely because it maps the "
        "sample space onto values it is itself a random variable. The sample mean is in "
        "fact an unbiased estimator of the population mean, so the claim that it is biased "
        "gets that backwards; and an estimator does not collapse to a fixed number, it "
        "gives a different one for every sample.",
        PDF, "p.37", origin="adapted_HT25"))

    out.append(mc(
        "L5-MC-009", 5, "Sampling distribution and variance",
        "The sample mean is an unbiased estimator of the population mean. What does "
        "\"unbiased\" mean?",
        ["The sample mean always equals the population mean",
         "On average the sample mean hits the true population mean, i.e. E[Xbar] = mu",
         "It says where the estimator is centred, not how spread out it is, so an "
         "unbiased estimator can still vary a lot from sample to sample",
         "The sample mean is normally distributed",
         "The sample mean is always smaller than the population mean"],
        ["b", "c"],
        "Unbiasedness is a statement about expectation, not about any single sample: the "
        "sample mean can be above or below mu in a given sample, but its expected value "
        "equals mu. It says nothing about the spread, so an unbiased estimator can still "
        "vary a lot between samples. The variance is sigma squared over n, which is not "
        "zero.",
        PDF, "p.37", origin="adapted_HT25"))

    out.append(mc(
        "L5-MC-010", 5, "Sampling distribution and variance",
        "What happens to the variance of the sample mean as the sample size n increases?",
        ["It increases",
         "It decreases, as the plotted standard deviations fall from 4.47 at n = 5 to "
         "1.41 at n = 50",
         "It stays constant",
         "The standard deviation of the sample mean shrinks like 1 over the square root "
         "of n, so it is divided by ten when n is multiplied by a hundred",
         "It becomes zero for any n"],
        ["b", "d"],
        "The plotted standard deviations fall steadily as n grows, so the variance of the "
        "sample mean decreases and the sample mean becomes a more precise estimate. The "
        "standard deviation falls like 1 over the square root of n rather than like 1 over "
        "n, which is why going from 5 to 50 observations cuts the spread by about three "
        "times and not ten: 4.47 times the square root of 5 and 1.41 times the square root "
        "of 50 are both about 10. The variance approaches zero but only reaches it in the "
        "limit, so the claim that it is zero for any n is false.",
        PDF, "p.40", r_functions=["var", "sqrt", "length"]))

    out.append(mc(
        "L5-MC-011", 5, "Law of large numbers",
        "What does the law of large numbers state?",
        ["As n grows, the sample mean converges to the population mean",
         "As n grows, the sample variance becomes exactly zero",
         "The sample mean is normally distributed for large n",
         "It does not require the population to be normally distributed",
         "The median always equals the mean for large n"],
        ["a", "d"],
        "The LLN says the sample mean gets arbitrarily close to the population mean as n "
        "grows, and it needs no assumption at all about the shape of the population. "
        "Making the sample mean approximately normal is the central limit theorem, which "
        "is a separate and stronger claim, so the normality option is not the LLN.",
        PDF, "p.42"))

    out.append(mc(
        "L5-MC-012", 5, "Central limit theorem",
        "What does the central limit theorem state?",
        ["The sample mean converges to the population mean as n grows",
         "For large n the sampling distribution of the sample mean is approximately "
         "normal, whatever the shape of the population",
         "The population must be normally distributed for inference to work",
         "The standard deviation of that sampling distribution is sigma over the square "
         "root of n",
         "The sample size must exceed the population size"],
        ["b", "d"],
        "The CLT is what makes z-based inference possible without knowing the population "
        "shape: the sample mean is approximately normal for large n even when the "
        "population itself is not, and its spread is sigma over the square root of n. "
        "Approximate convergence of the mean is the LLN, so the first option is not the CLT.",
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
        "L5-MC-015", 3, "Shape of a distribution",
        "A distribution is strongly right-skewed. Which statement is TRUE?",
        ["The mean is smaller than the median.",
         "The mean is larger than the median.",
         "The mean and median are always equal for a symmetric distribution.",
         "The median is more affected by outliers than the mean.",
         "A right-skewed distribution is not a symmetric one, so it is not a case where "
         "the mean and median coincide."],
        ["b", "e"],
        "A long right tail pulls the mean upward, so the mean exceeds the median. The "
        "median is the more robust of the two, which is why the option claiming it is more "
        "affected has it backwards. The mode is still perfectly well defined for a skewed "
        "distribution, and the mean and median coincide only in the symmetric case, which "
        "a right-skewed distribution is not.",
        PDF3, "p.21", r_functions=["mean", "median", "quantile"]))

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
        "State the central limit theorem, and say which other statistics it covers.",
        "For i.i.d. variables with distribution F(mu, sigma^2), for large n the sample "
        "mean is approximately normal regardless of the shape of F. The theorem extends "
        "to a statistic written as a sum or average of i.i.d. variables, such as sample "
        "proportions and variances.",
        [rb("States the approximate normality of the sampling distribution of the mean", 2),
         rb("Notes it holds regardless of the population shape", 2),
         rb("Names the extension to sums or averages, e.g. proportions and variances", 2)],
        1, PDF, "p.47", origin="adapted_HT25"))

    out.append(wa(
        "L5-WA-003", 5, "Sampling distribution and variance",
        "Write down the formula for the variance of the sample mean, and explain what "
        "happens to it as n increases.",
        "`Var(Xbar_n) = (1/n^2) * sum of Var(X_i) = (n sigma^2) / n^2 = sigma^2 / n`, using the independence of the observations. As n grows the variance shrinks, so the sample mean becomes a more precise estimate.",
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
        "A PMF gives the probability of each outcome and applies to discrete variables, so it is the one for a fair die. A PDF describes the relative likelihood. A CDF gives the probability of a variable being less than or equal to a value.",
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
        "is about 0.0345.",
        [rb("`pnorm()` used as the correct function", 2),
         rb("Mean and standard deviation supplied as named arguments", 2),
         rb("States that this is P(X <= 35.8), the area to the left")],
        1, PDF, "p.27", code="pnorm(35.8, mean = 36, sd = 0.11)",
        r_functions=["pnorm"]))

    out.append(wa(
        "L5-WA-006", 5, "Law of large numbers",
        "Explain what the law of large numbers says, and what it leaves for the "
        "central limit theorem to answer.",
        "The LLN says the estimate of the population mean becomes more accurate as the "
        "sample grows: Xbar is a consistent estimator of mu. It does not describe the "
        "distribution of the sample mean for finite n; that is what the CLT is for.",
        [rb("LLN stated as the estimate of the population mean becoming more accurate", 2),
         rb("Xbar named as a consistent estimator of the population mean", 2),
         rb("Notes it says nothing about the sample mean's distribution for finite n", 2)],
        1, PDF, "p.46"))

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
        "Unbiased means E[Xbar] = mu, so the estimator is on target in the long run even though a single sample can fall above or below mu. Small samples remain a problem because the estimate still varies a lot from sample to sample.",
        [rb("Unbiasedness explained via E[Xbar] = mu", 2),
         rb("Notes that a single sample may still deviate from mu", 2),
         rb("Explains that small samples still leave the estimate highly variable")],
        # p.37 ends mid-sentence - "But exac[tly how much? We ...]" - and the
        # Var(Xbar) = sigma^2/n derivation is overleaf on p.38. The answer used
        # to quote that formula, so the cited page did not contain it. The
        # formula is gone and the point is made the way p.37 makes it, as
        # variability rather than as an expression.
        1, PDF, "p.37", r_functions=["mean", "var"]))

    # ---- i.i.d. random variables, stated explicitly on L5 p.39. The bank had
    # no question on it: "i.i.d." appears in the sample-mean variance proof on
    # p.38 and is then defined in an aside on p.39, so it was easy to read past.
    out.append(mc(
        "L5-MC-016", 5, "i.i.d. random variables",
        "Which statements about i.i.d. random variables are true?",
        ["Independent means the occurrence of one event does not affect the "
         "probability of another",
         "Identically distributed means all the random variables have the same "
         "probability distribution",
         "Independence by itself is enough for a sample to be i.i.d.",
         "i.i.d. additionally requires the variables to be normally distributed",
         "Identically distributed means sharing the same mean, even when the "
         "spreads differ"],
        ["a", "b"],
        "Independence means the occurrence of one event does not affect the "
        "probability of another, and identically distributed means the variables "
        "share one probability distribution, so (a) and (b) are correct. "
        "Independence alone is not enough: two coin tosses with coins of "
        "different denominations are independent but not identically "
        "distributed, so (c) and (d) fail, and nothing in the definition "
        "requires normality. Sharing a mean is not sharing a distribution, "
        "since a variable can have the same mean with a different spread, so "
        "(e) is wrong.",
        PDF, "p.39"))

    # ---- the law of large numbers, L5 p.44-46. Lecture 5 used to reach its
    # `median` coverage through a skew question that was never Lecture 5's:
    # lecture 5 never mentions skew, and the mean-versus-median material is on
    # L3 p.21. Moving that question to its real lecture left lecture 5 without
    # the median, and p.46 is the slide that genuinely earns it.
    out.append(mc(
        "L5-MC-017", 5, "Law of large numbers",
        "Which statements about the law of large numbers are true?",
        ["As the sample size grows, the sample mean converges to the population "
         "mean",
         "The law of large numbers applies only to the sample mean and not to "
         "medians",
         "The law of large numbers extends to sample proportions, variances "
         "and medians",
         "The law of large numbers describes the distribution of the sample "
         "mean for a finite sample size",
         "With larger samples, the estimate of the population mean becomes "
         "less accurate"],
        ["a", "c"],
        "As the sample size grows the sample mean settles onto the population "
        "mean, so (a) is correct, and the law of large numbers is not confined "
        "to the mean: it extends to sample proportions, variances and medians, "
        "so (c) is correct and (b) is wrong. Describing the distribution of "
        "the sample mean at a finite sample size is the central limit theorem's "
        "job, not the law of large numbers, which rules out (d). Larger "
        "samples make the estimate of the population mean more accurate, so "
        "(e) is backwards.",
        PDF, "p.46",
        r_functions=["median"]))

    return out