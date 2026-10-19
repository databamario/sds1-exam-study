"""Lecture 9 - Simulation-based inference."""

from .common import mc, rb, wa

PDF = "lecture9_after.pdf"


def questions():
    out = []

    out.append(mc(
        "L9-MC-001", 9, "Non-parametric methods",
        "All the tests seen so far rely on a known sampling distribution such as z, t, F or "
        "chi-squared. What is the non-parametric alternative?",
        ["Bootstrapping",
         "The bootstrap permutation test",
         "Bagging",
         "Cross-validation",
         "A method that does not assume a specific form for the population distribution"],
        ["a", "e"],
        "Non-parametric methods assume no specific form "
        "for the population distribution, and states that it focuses on bootstrapping as the "
        "workable option, estimating standard errors, confidence intervals and p-values "
        "directly from the sample.",
        PDF, "p.4", r_functions=["sample", "replicate"]))

    out.append(mc(
        "L9-MC-002", 9, "Monte-Carlo simulations",
        "What are the steps of a Monte-Carlo simulation?",
        ["Collect real data, fit a model, test, report",
         "Define the data generating process and statistic, generate many random samples, "
         "compute the statistic for each",
         "Generating random samples from a specified distribution to approximate the "
         "sampling distribution of a statistic",
         "Choose alpha, compute the p-value, decide",
         "Generate samples, bootstrap them, report a confidence interval"],
        ["b", "c"],
        "The three steps are to define the DGP and the statistic of interest, generate a "
        "large number of random samples from that DGP, and calculate the statistic for each "
        "sample so the resulting distribution approximates the sampling distribution.",
        PDF, "p.6", r_functions=["rnorm", "runif", "replicate"]))

    out.append(mc(
        "L9-MC-003", 9, "Monte-Carlo simulations",
        "What does a Monte-Carlo simulation rely on to become accurate?",
        ["The central limit theorem",
         "The law of large numbers",
         "It can estimate standard errors, confidence intervals and p-values when the "
         "analytical solution is difficult or impossible to obtain",
         "The chi-squared approximation",
         "Having an exactly normal population"],
        ["b", "c"],
        "Monte-Carlo works by repeated sampling, so its accuracy improves as the number of "
        "simulations grows, which is precisely the law of large numbers. The CLT is about "
        "the shape of a sampling distribution, a different statement.",
        PDF, "p.6", r_functions=["replicate", "rnorm"]))

    out.append(mc(
        "L9-MC-004", 9, "Monte-Carlo simulations",
        "Consider this R code. What does `H` end up counting?",
        ["The number of simulated draws where X is less than Y",
         "The number of simulated draws where X is greater than Y",
         "The sum of X across all simulations",
         "The number of simulations, N",
         "Dividing H by N estimates the probability that X is less than Y, which is "
         "awkward to solve analytically here"],
        ["a", "e"],
        "`H <- sum(X < Y)` counts the cases where the comparison is true, so dividing H by N "
        "gives the simulated probability P(X < Y). Only the true comparisons are summed, "
        "which is why (e) as 'half of them' was wrong: every draw is either true or false "
        "and only the true ones are counted. This is used to "
        "estimate a probability that is analytically awkward, here for X normal and Y "
        "exponential.",
        PDF, "p.12",
        code="X <- rnorm(N, mean = 3, sd = 1)\nY <- rexp(N, rate = 0.5)\nH <- sum(X < Y)\nH / N",
        r_functions=["rnorm", "rexp", "sum"]))

    out.append(mc(
        "L9-MC-005", 9, "Bootstrapping",
        "What does the bootstrapping procedure do?",
        ["It resamples from the fitted normal distribution",
         "It repeatedly resamples the observed data with replacement to estimate standard "
         "errors, confidence intervals and p-values",
         "It splits the data into a training and a test set",
         "It computes the exact analytic solution",
         "It needs only the observed sample, and works for any statistic including the "
         "median"],
        ["b", "e"],
        "Bootstrapping samples repeatedly from the empirical distribution of the observed "
        "data with replacement and recomputes the statistic each time, giving an estimated "
        "sampling distribution without assuming a parametric form.",
        PDF, "p.18",
        code="income <- c(18, 21, 22, 24, 25, 26, 28, 29, 31, 34, 38, 95)\n"
             "N <- 10000\n"
             "boot_medians <- numeric(N)\n"
             "for (i in 1:N) {\n"
             "  boot_sample <- sample(income, length(income), replace = TRUE)\n"
             "  boot_medians[i] <- median(boot_sample)\n"
             "}",
        r_functions=["sample", "replace", "median", "numeric", "for"]))

    out.append(mc(
        "L9-MC-006", 9, "Monte-Carlo accuracy",
        "The birthday simulation returns 0.7103, while the exact answer is written "
        "1 - (365 x 364 x ... x 336) / 365^30 = 0.706. Which two statements about these "
        "two numbers are true?",
        ["The simulated value and the exact value agree to about two decimal places",
         "The exact value comes from the product formula, and the simulation only "
         "approximates it",
         "The numerator 365 x 364 x ... x 336 counts all possible birthday assignments",
         "The simulated value becomes exactly the true probability once N is large enough",
         "The exact value is itself an estimate, obtained by running the simulation with "
         "a larger N"],
        ["a", "b"],
        "The product in the numerator counts the assignments with no repeated day, so "
        "subtracting it from the total 365^30 leaves the assignments containing at least "
        "one match, which is the exact probability. The simulation arrives at the same "
        "quantity by repeating the draw and keeping the fraction of iterations that "
        "contained a match, which is why it lands near the exact value rather than on it.",
        PDF, "p.16", origin="adapted_HT25"))

    out.append(mc(
        "L9-MC-007", 9, "Bootstrapping",
        "Consider this code. What is the purpose of `numeric(N)`?",
        ["To create N random numbers",
         "To create an empty numeric vector of length N that will hold one bootstrap "
         "statistic per iteration",
         "To create a vector of N observations to resample",
         "To reserve the storage before the loop, so each iteration can write its result "
         "into position i",
         "To set the random seed N times"],
        ["b", "d"],
        "`numeric(N)` allocates an empty numeric vector of length N so R can store one "
        "bootstrap result in each position. Without pre-allocation R would have to grow the "
        "vector inside the loop, which is slower.",
        PDF, "p.19",
        code="boot_medians <- numeric(N)\nfor (i in 1:N) {\n  boot_sample <- sample(x, length(x), replace = TRUE)\n  boot_medians[i] <- median(boot_sample)\n}",
        r_functions=["numeric", "sample", "median", "for"]))

    # ----------------------------------------------- all-true-except-one traps
    out.append(mc(
        "L9-MC-008", 9, "Reading R code",
        "Consider this code. Which statements about it are true? "
        "`N <- 100000; X <- rnorm(N, 3, 1); Y <- rexp(N, rate = 0.5); "
        "H <- sum(X < Y); H / N`",
        ["`N <- 100000` sets the number of simulations",
         "`X <- rnorm(N, mean = 3, sd = 1)` draws N values from an exponential "
         "distribution",
         "`H <- sum(X < Y)` counts the draws where X is greater than Y",
         "`H / N` gives an estimate of P(X < Y)",
         "The result is the exact analytical probability of P(X < Y)"],
        ["a", "d"],
        "The code sets the number of simulations, draws N values from each distribution, "
        "counts the draws in which X is less than Y, and divides by N to estimate P(X < Y). "
        "The result is a simulation-based approximation that becomes more accurate as N "
        "grows, not an exact closed-form answer, so (e) is false.",
        PDF, "p.11",
        code="N <- 100000\nX <- rnorm(N, mean = 3, sd = 1)\nY <- rexp(N, rate = 0.5)\nH <- sum(X < Y)\nH / N",
        r_functions=["rnorm", "rexp", "sum"]))

    out.append(mc(
        "L9-MC-009", 9, "Reading R code",
        "Which statements about the birthday problem simulation are true? "
        "`bdays <- sample(1:365, 30, replace = TRUE)`, repeated for `N` iterations.",
        ["`sample(1:365, 30, replace = TRUE)` simulates 30 people's birthdays",
         "The replacement is inappropriate, because two people cannot share a birthday",
         "The simulation estimates the probability of at least one shared birthday",
         "The simulation would be exact regardless of how large N is",
         "Increasing N beyond some point makes the estimate exact"],
        ["a", "c"],
        "Sampling 30 birthdays with replacement from 1 to 365 models birthdays as "
        "independent, which is what allows two people to share one. Repeating the simulation "
        "estimates the probability of at least one shared birthday, and raising N improves "
        "accuracy through the law of large numbers. No finite N gives an exact answer, so "
        "(d) is false.",
        PDF, "p.16", code="bdays <- sample(1:365, 30, replace = TRUE)",
        r_functions=["sample", "replace"]))

    # ----------------------------------------------------------------- written
    out.append(wa(
        "L9-WA-001", 9, "Monte-Carlo simulations",
        "Explain what Monte-Carlo simulation is, list its three steps, and say which "
        "theoretical result it relies on.",
        "Monte-Carlo simulation generates many random samples from a data generating process to approximate the sampling distribution of a statistic. The steps: define the process and the statistic, generate many samples, compute the statistic for each. It relies on the law of large numbers.",
        [rb("Defined as approximating a sampling distribution by repeated sampling", 2),
         rb("All three steps listed", 3),
         rb("Law of large numbers correctly named as the basis", 2),
         rb("Notes use for standard errors, CIs or p-values when analytics are hard")],
        1, PDF, "p.6", r_functions=["rnorm", "replicate", "sample"]))

    out.append(wa(
        "L9-WA-002", 9, "Monte-Carlo example",
        "Assume X is normal with mean 3 and standard deviation 1, and Y is exponential with "
        "rate 0.5. Describe how you would use a simulation to estimate P(X < Y), writing "
        "the relevant R code.",
        "Generate N values from each distribution, count how often the comparison holds, and divide by N. In R: `X <- rnorm(N, 3, 1)`, `Y <- rexp(N, 0.5)`, `H <- sum(X < Y)`, then `H / N` estimates the probability, near 0.25 for large N.",
        [rb("Both distributions generated with `rnorm()` and `rexp()` and correct "
            "parameters", 3),
         rb("Count of favourable cases computed with `sum(X < Y)`", 2),
         rb("Estimate obtained as the count divided by N", 2)],
        1, PDF, "p.12",
        code="X <- rnorm(N, mean = 3, sd = 1)\nY <- rexp(N, rate = 0.5)\nH <- sum(X < Y)\nH / N",
        r_functions=["rnorm", "rexp", "sum"]))

    out.append(wa(
        "L9-WA-003", 9, "Bootstrapping",
        "Explain how you would bootstrap a median, writing the R code, and say why you "
        "cannot simply do this with a mean on the exam.",
        "Resample the observed data with replacement many times, compute the median of each resample, and use the distribution of those medians to form a confidence interval. In R pre-allocate `boot_medians <- numeric(N)`, then in a loop take `sample(x, length(x), replace = TRUE)` and store `median(boot_sample)`.",
        [rb("Resampling with replacement correctly described", 2),
         rb("Median computed for each resample and stored", 2),
         rb("R code given including pre-allocation with `numeric(N)`", 2),
         rb("Notes the bootstrap approximates rather than computes exactly")],
        1, PDF, "p.18",
        code="boot_medians <- numeric(N)\nfor (i in 1:N) {\n  boot_sample <- sample(x, length(x), replace = TRUE)\n  boot_medians[i] <- median(boot_sample)\n}",
        r_functions=["sample", "median", "numeric"]))

    out.append(wa(
        "L9-WA-004", 9, "Non-parametric methods",
        "Explain what a non-parametric method is, and why simulation-based inference is "
        "needed at all given that we already have z, t, F and chi-squared tests.",
        "A non-parametric method makes no assumption about the specific form of the population distribution, unlike parametric tests that rely on a known sampling distribution. Simulation is needed because when normality is violated, especially with small samples, the standard tests can give unreliable results.",
        [rb("Defined as making no assumption about the population distribution form", 2),
         rb("Contrasts with the parametric tests relying on known sampling distributions", 2),
         rb("Notes unreliability when normality is violated, especially at small n", 2),
         rb("Notes analytic solutions can be too difficult to obtain")],
        1, PDF, "p.4", r_functions=["rnorm", "sample"]))

    out.append(wa(
        "L9-WA-005", 9, "Reproducibility",
        "Explain the purpose of `set.seed()` and describe what happens to your simulated "
        "results if you do not use it.",
        "`set.seed()` fixes the initial state of R's random number generator, so the same seed always produces the same sequence of pseudo-random draws. Without it each run starts from a different state, so a Monte-Carlo or bootstrap result differs every time and cannot be reproduced.",
        [rb("Explains it fixes the random number generator state", 2),
         rb("States that the same seed reproduces the same draws", 2),
         rb("Explains results differ between runs without it", 2)],
        1, PDF, "p.16", code="set.seed(42)", r_functions=["set.seed", "rnorm", "sample"]))

    out.append(wa(
        "L9-WA-006", 9, "Comparing analytic and simulation approaches",
        "A probability can be checked analytically, or estimated by simulating it. Give "
        "the analytic approach and the simulation approach for the probability of obtaining "
        "1, 5 or 9 heads in 10 tosses of a fair coin.",
        "The count of heads in 10 tosses is binomial(n = 10, p = 0.5), so the probability is P(X = 1) + P(X = 5) + P(X = 9) \u2248 0.2656. The simulation draws many samples and uses the matching fraction as the estimate.",
        [rb("Identifies the binomial distribution with n = 10 and p = 0.5", 2),
         rb("Correctly sums P(X=1), P(X=5) and P(X=9) and gives about 0.2656", 2),
         rb("Describes the simulation as repeated draws with a sample fraction", 2),
         rb("Notes convergence to the analytic value as N grows", 2)],
        1, PDF, "p.7", code="sum(dbinom(c(1, 5, 9), size = 10, prob = 0.5))",
        r_functions=["dbinom", "rbinom", "sample"]))

    out.append(wa(
        "L9-WA-007", 9, "The birthday problem",
        "Describe how the birthday problem would be simulated in R, and explain why the "
        "sampling is done with replacement.",
        "Draw 30 birthdays with `sample(1:365, 30, replace = TRUE)`, check whether any day repeats, and record whether a match occurred. Repeat for many iterations and divide matches by the total to estimate the probability. Replacement is correct because two people really can share a birthday.",
        [rb("30 birthdays drawn from 1 to 365", 2),
         rb("Describes detecting a repeated day and averaging over iterations", 2),
         rb("Justifies replacement by independence of different people", 2),
         rb("Notes without replacement a match would be impossible", 2)],
        1, PDF, "p.16", code="bdays <- sample(1:365, 30, replace = TRUE)",
        r_functions=["sample", "replace", "any", "duplicated"]))

    out.append(wa(
        "L9-WA-008", 9, "Scope of the course and next steps",
        "Summarise what simulation-based inference adds, and state which statistical "
        "topic is deferred to SDS2.",
        "Simulation-based inference covers Monte-Carlo simulation to approximate sampling distributions and awkward probabilities, and bootstrapping to estimate standard errors, confidence intervals and p-values without assuming a parametric form. Linear regression and a fuller treatment of correlation are deferred to SDS2.",
        [rb("Identifies Monte-Carlo simulation as the addition", 2),
         rb("Identifies bootstrapping as the second addition", 2),
         rb("Correctly defers linear regression to SDS2", 2)],
        1, PDF, "p.18", r_functions=["sample", "rnorm", "median"],
        origin="adapted_HT25"))

    return out