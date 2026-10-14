"""Lecture 9 - Simulation-based inference."""

from .common import mc, rb, wa

PDF = "lecture9_after.pdf"


def questions():
    out = []

    out.append(mc(
        "L9-MC-001", 9, "Non-parametric methods",
        "All the tests seen so far rely on a known sampling distribution such as z, t, F or "
        "chi-squared. What is the non-parametric alternative discussed in this lecture?",
        ["Bootstrapping",
         "The bootstrap permutation test",
         "Bagging",
         "Cross-validation",
         "The jackknife confidence interval"],
        ["a"],
        "The lecture defines non-parametric methods as those not assuming a specific form "
        "for the population distribution, and states that it focuses on bootstrapping as the "
        "workable option, estimating standard errors, confidence intervals and p-values "
        "directly from the sample.",
        PDF, "p.4", r_functions=["sample", "replicate"]))

    out.append(mc(
        "L9-MC-002", 9, "Monte-Carlo simulations",
        "What are the steps of a Monte-Carlo simulation as given in the lecture?",
        ["Collect real data, fit a model, test, report",
         "Define the data generating process and statistic, generate many random samples, "
         "compute the statistic for each",
         "Simulate one sample, plot it, conclude",
         "Choose alpha, compute the p-value, decide",
         "Generate samples, bootstrap them, report a confidence interval"],
        ["b"],
        "The three steps are to define the DGP and the statistic of interest, generate a "
        "large number of random samples from that DGP, and calculate the statistic for each "
        "sample so the resulting distribution approximates the sampling distribution.",
        PDF, "p.6", r_functions=["rnorm", "runif", "replicate"]))

    out.append(mc(
        "L9-MC-003", 9, "Monte-Carlo simulations",
        "What does a Monte-Carlo simulation rely on to become accurate?",
        ["The central limit theorem",
         "The law of large numbers",
         "The fact that R is fast",
         "The chi-squared approximation",
         "Having an exactly normal population"],
        ["b"],
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
         "The mean of X"],
        ["a"],
        "`H <- sum(X < Y)` counts the cases where the comparison is true, so dividing H by N "
        "gives the simulated probability P(X < Y). The lecture uses exactly this to "
        "estimate a probability that is analytically awkward, here for X normal and Y "
        "exponential.",
        PDF, "p.11",
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
         "It removes outliers before analysing the data"],
        ["b"],
        "Bootstrapping samples repeatedly from the empirical distribution of the observed "
        "data with replacement and recomputes the statistic each time, giving an estimated "
        "sampling distribution without assuming a parametric form.",
        PDF, "p.17",
        code="boot_sample <- sample(x, length(x), replace = TRUE)\nboot_medians[i] <- median(boot_sample)",
        r_functions=["sample", "replace", "median"]))

    out.append(mc(
        "L9-MC-006", 9, "Bootstrapping",
        "Why is `set.seed()` used before a simulation?",
        ["It makes the simulation run faster",
         "It makes the random numbers reproducible so results can be recovered",
         "It increases the number of simulations",
         "It ensures the data are normally distributed",
         "It removes the need for a bootstrap"],
        ["b"],
        "`set.seed()` fixes the starting state of the random number generator, so the same "
        "seed reproduces the same pseudo-random draws. That is essential when a result needs "
        "to be reported or checked by someone else.",
        PDF, "p.15", code="set.seed(42)", r_functions=["set.seed"],
        origin="adapted_HT25"))

    out.append(mc(
        "L9-MC-007", 9, "Bootstrapping",
        "Consider this code. What is the purpose of `numeric(N)`?",
        ["To create N random numbers",
         "To create an empty numeric vector of length N that will hold one bootstrap "
         "statistic per iteration",
         "To create a vector of N observations to resample",
         "To pre-allocate a data.frame with N rows",
         "To set the random seed N times"],
        ["b"],
        "`numeric(N)` allocates an empty numeric vector of length N so R can store one "
        "bootstrap result in each position. Without pre-allocation R would have to grow the "
        "vector inside the loop, which is slower.",
        PDF, "p.18",
        code="boot_medians <- numeric(N)\nfor (i in 1:N) {\n  boot_sample <- sample(x, length(x), replace = TRUE)\n  boot_medians[i] <- median(boot_sample)\n}",
        r_functions=["numeric", "sample", "median", "for"]))

    # ---------------------------------------------- zero-correct special cases
    out.append(mc(
        "L9-MC-008", 9, "Reading R code",
        "Consider this code. Which statements about it are true?",
        ["`N <- 100000` sets the number of simulations",
         "`X <- rnorm(N, mean = 3, sd = 1)` draws N values from a normal distribution",
         "`H <- sum(X < Y)` counts the draws where X is less than Y",
         "`H / N` gives an estimate of P(X < Y)",
         "The result is the exact analytical probability of P(X < Y)"],
        [],
        "Every option here is true. The code sets the simulation count, draws from the two "
        "distributions, counts the favourable cases and divides by N to estimate P(X < Y). "
        "The final option overstates it: this is a simulation-based approximation, accurate "
        "as N grows by the law of large numbers, not an exact closed-form answer. Mark "
        "nothing to score the full point.",
        PDF, "p.11",
        code="N <- 100000\nX <- rnorm(N, mean = 3, sd = 1)\nY <- rexp(N, rate = 0.5)\nH <- sum(X < Y)\nH / N",
        r_functions=["rnorm", "rexp", "sum"]))

    out.append(mc(
        "L9-MC-009", 9, "Reading R code",
        "Which statements about the birthday problem simulation are true?",
        ["`sample(1:365, 30, replace = TRUE)` simulates 30 people's birthdays",
         "The replacement is appropriate because two people can share a birthday",
         "The simulation estimates the probability of at least one shared birthday",
         "The simulation would be exact regardless of how large N is",
         "Increasing N generally improves the accuracy of the estimate"],
        [],
        "Every option here is true. Sampling 30 birthdays with replacement from 1 to 365 "
        "models independent birthdays, repeating it estimates the probability of a shared "
        "birthday, and raising N improves accuracy through the law of large numbers. The "
        "fourth option is wrong: no finite N gives an exact answer. Mark nothing to score "
        "the full point.",
        PDF, "p.15", code="bdays <- sample(1:365, 30, replace = TRUE)",
        r_functions=["sample", "replace"]))

    # ----------------------------------------------------------------- written
    out.append(wa(
        "L9-WA-001", 9, "Monte-Carlo simulations",
        "Explain what Monte-Carlo simulation is, list its three steps, and say which "
        "theoretical result it relies on.",
        "A Monte-Carlo simulation generates a large number of random samples from a "
        "specified data generating process to approximate the sampling distribution of a "
        "statistic, which is useful for standard errors, confidence intervals and p-values "
        "when analytic solutions are difficult. The steps are to define the data generating "
        "process and the statistic of interest, generate a large number of random samples, "
        "and calculate the statistic for each sample. It relies on the law of large numbers, "
        "since the approximation improves as the number of simulations grows.",
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
        "Generate N values from each distribution, count how often the comparison holds, "
        "and divide by N. In R: `X <- rnorm(N, mean = 3, sd = 1)`, `Y <- rexp(N, rate = "
        "0.5)`, `H <- sum(X < Y)`, then `H / N` is the estimated probability, which for "
        "large N settles near 0.25. The analytic solution is awkward, which is exactly the "
        "case simulation is meant for.",
        [rb("Both distributions generated with `rnorm()` and `rexp()` and correct "
            "parameters", 3),
         rb("Count of favourable cases computed with `sum(X < Y)`", 2),
         rb("Estimate obtained as the count divided by N", 2)],
        1, PDF, "p.11",
        code="X <- rnorm(N, mean = 3, sd = 1)\nY <- rexp(N, rate = 0.5)\nH <- sum(X < Y)\nH / N",
        r_functions=["rnorm", "rexp", "sum"]))

    out.append(wa(
        "L9-WA-003", 9, "Bootstrapping",
        "Explain how you would bootstrap a median, writing the R code, and say why you "
        "cannot simply do this with a mean on the exam.",
        "Resample the observed data with replacement many times, compute the median of each "
        "resample, and use the distribution of those medians to form a confidence interval. "
        "In R: pre-allocate with `boot_medians <- numeric(N)`, then in a loop over "
        "`i in 1:N` take `boot_sample <- sample(x, length(x), replace = TRUE)` and store "
        "`boot_medians[i] <- median(boot_sample)`. The bootstrap is an approximation that "
        "improves with N, not an exact calculation, so you describe the procedure rather "
        "than compute a number.",
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
        "A non-parametric method makes no assumption about the specific form of the "
        "population distribution, unlike the parametric tests that rely on a known sampling "
        "distribution justified by normality or the central limit theorem. Simulation is "
        "needed because when the normality assumption is violated, especially with small "
        "samples, the standard tests can give unreliable results, and sometimes the "
        "mathematics of the analytic solution is simply too hard.",
        [rb("Defined as making no assumption about the population distribution form", 2),
         rb("Contrasts with the parametric tests relying on known sampling distributions", 2),
         rb("Notes unreliability when normality is violated, especially at small n", 2),
         rb("Notes analytic solutions can be too difficult to obtain")],
        1, PDF, "p.4", r_functions=["rnorm", "sample"]))

    out.append(wa(
        "L9-WA-005", 9, "Reproducibility",
        "Explain the purpose of `set.seed()` and describe what happens to your simulated "
        "results if you do not use it.",
        "`set.seed()` fixes the initial state of R's random number generator, so the same "
        "seed always produces the same sequence of pseudo-random draws. Without it, each run "
        "starts from a different state, so a Monte-Carlo or bootstrap result will differ "
        "slightly every time you run it, which makes results impossible to reproduce, "
        "report or have checked by someone else.",
        [rb("Explains it fixes the random number generator state", 2),
         rb("States that the same seed reproduces the same draws", 2),
         rb("Explains results differ between runs without it", 2)],
        1, PDF, "p.15", code="set.seed(42)", r_functions=["set.seed", "rnorm", "sample"]))

    out.append(wa(
        "L9-WA-006", 9, "Comparing analytic and simulation approaches",
        "The lecture checks a probability analytically and then suggests simulating it. Give "
        "the analytic approach and the simulation approach for the probability of obtaining "
        "1, 5 or 9 heads in 10 tosses of a fair coin.",
        "Analytically, the number of heads in 10 tosses follows a binomial distribution with "
        "n = 10 and p = 0.5, so the probability is P(X = 1) + P(X = 5) + P(X = 9), which "
        "evaluates to about 0.2656. The simulation approach instead draws many samples of 10 "
        "coin tosses, counts the fraction of samples with 1, 5 or 9 heads, and uses that "
        "fraction as an estimate that converges on the analytic value as N grows.",
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
        "Draw 30 birthdays at random from the 365 possible days with `sample(1:365, 30, "
        "replace = TRUE)`, check whether any day repeats within that draw, and record "
        "whether a match occurred. Repeat this for a large number of iterations and divide "
        "the number of iterations with a match by the total to estimate the probability. "
        "Replacement is correct because different people are independent, so two of them "
        "really can share a birthday; sampling without replacement would make a shared "
        "birthday impossible.",
        [rb("30 birthdays drawn from 1 to 365", 2),
         rb("Describes detecting a repeated day and averaging over iterations", 2),
         rb("Justifies replacement by independence of different people", 2),
         rb("Notes without replacement a match would be impossible", 2)],
        1, PDF, "p.15", code="bdays <- sample(1:365, 30, replace = TRUE)",
        r_functions=["sample", "replace", "any", "duplicated"]))

    out.append(wa(
        "L9-WA-008", 9, "Scope of the course and next steps",
        "Summarise what this lecture adds to the course, and state which statistical topic "
        "the lectures explicitly defer to the next course.",
        "This lecture adds simulation-based inference: Monte-Carlo simulation to approximate "
        "sampling distributions and awkward probabilities, and bootstrapping to estimate "
        "standard errors, confidence intervals and p-values without assuming a parametric "
        "form. Linear regression, along with a fuller treatment of correlation, is "
        "explicitly deferred to the next course in the programme, SDS2.",
        [rb("Identifies Monte-Carlo simulation as the addition", 2),
         rb("Identifies bootstrapping as the second addition", 2),
         rb("Correctly defers linear regression to SDS2", 2)],
        1, PDF, "p.17", r_functions=["sample", "rnorm", "median"],
        origin="adapted_HT25"))

    return out