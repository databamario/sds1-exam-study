"""Lecture 3 - Descriptive statistics for continuous data + joins."""

from .common import mc, rb, wa

PDF = "lecture3.pdf"


def questions():
    out = []

    # ------------------------------------------------------ central tendency
    out.append(mc(
        "L3-MC-001", 3, "Measures of central tendency",
        "Consider the vector `y = c(43, 23, 22, 104, 42)`. Which statements are TRUE?",
        ["The median is 42",
         "The median is 46.8",
         "The mean is pulled upward relative to the median by the value 104",
         "The mode is 42",
         "The standard deviation is 82"],
        ["a", "c"],
        "Ordered, the values are 22, 23, 42, 43, 104, so the middle value and therefore "
        "the median is 42. The single large value 104 drags the mean (46.8) well above "
        "the median. 82 is the range, 104 - 22, not a standard deviation, and there is "
        "no repeated value, so there is no mode.",
        PDF, "p.17", code="y <- c(43, 23, 22, 104, 42)\nmedian(y)",
        r_functions=["median", "mean", "range", "sort"], origin="adapted_HT25"))

    out.append(mc(
        "L3-MC-002", 3, "Measures of central tendency",
        "A distribution contains a few extreme values. Which two statements about the "
        "measures of central tendency are TRUE?",
        ["the mean is sensitive to outliers and skewed data",
         "the median is robust to outliers and skewness",
         "the median takes the magnitude of extreme values into account",
         "the mode is unique and informative for a continuous distribution",
         "the mean is robust to outliers"],
        ["a", "b"],
        "The comparison is between a measure that reacts to extreme values and one that "
        "does not: the mean is pulled around by outliers and by skewed data, while the "
        "median depends only on the middle of the ordered values. Robustness is not free - "
        "the median ignores the magnitude of the extreme values, and the mode may be "
        "neither unique nor informative for continuous data.",
        PDF, "p.21"))

    out.append(mc(
        "L3-MC-003", 3, "Measures of central tendency",
        "Which statements about the three measures of central tendency are TRUE?",
        ["The mean is always reported with a standard deviation.",
         "The median is robust to extreme values.",
         "The mode is useful for categorical or bimodal distributions.",
         "a data set can have at most one mode, since the mode is a single value.",
         "The median is pulled towards extreme values in a skewed sample."],
        ["b", "c"],
        "The median resists outliers and skewness because it only looks at the middle of "
        "the ordered data, and a mode is the measure worth reaching for on a "
        "categorical or bimodal variable, where averaging the categories would be "
        "meaningless. A mode need not be unique, so a dataset can have more than "
        "one, and the median is not what gets pulled towards extreme values; the "
        "mean is.",
        PDF, "p.21"))

    out.append(mc(
        "L3-MC-004", 3, "Measures of central tendency",
        "Without doing the calculation, what is the mean of `x = c(2, 4, 6, 8)`?",
        ["2",
         "4",
         "5",
         "6",
         "The mean is the sum of the values divided by the number of observations"],
        ["c", "e"],
        "The values are evenly spaced and symmetric around 5, and the formula "
        "`xbar = sum(x)/n = (2+4+6+8)/4` gives 20/4 = 5. You do not need to do the "
        "arithmetic on the exam, but you do need the formula: the mean is always the sum "
        "divided by how many values there are.",
        PDF, "p.15", code="x <- c(2, 4, 6, 8)\nmean(x)",
        r_functions=["mean", "sum"], origin="adapted_HT25"))

    # ----------------------------------------------------------- measures of spread
    out.append(mc(
        "L3-MC-005", 3, "Measures of spread",
        "Which statements about the variance and standard deviation are TRUE?",
        ["The standard deviation is the square root of the variance.",
         "The variance and standard deviation have the same units as the data.",
         "The variance has squared units.",
         "The standard deviation is always larger than the variance.",
         "The sample variance divides by n, not by n - 1."],
        ["a", "c"],
        "Taking the square root of a squared-unit quantity returns the original units, so "
        "the standard deviation shares the data's units and the variance has squared "
        "units. The standard deviation is usually the smaller of the two, and the sample "
        "variance divides by n - 1.",
        PDF, "p.28"))

    out.append(mc(
        "L3-MC-006", 3, "Measures of spread",
        "Which formula gives the sample variance?",
        ["`s^2 = (1/n) * sum((x_i - xbar)^2)`",
         "`s^2 = (1/(n-1)) * sum((x_i - xbar)^2)`",
         "`s^2 = (1/(n-1)) * sum(x_i^2)`",
         "`s^2 = sqrt((1/(n-1)) * sum((x_i - xbar)^2))`"],
        ["b"],
        "The sample variance divides the sum of squared deviations by n - 1, an unbiased "
        "correction. The first is the population variance, the third omits subtracting the "
        "mean, and the last is the standard deviation rather than the variance.",
        PDF, "p.28", origin="adapted_HT25"))

    out.append(mc(
        "L3-MC-007", 3, "Measures of spread",
        "Why is the mean a poor measure of spread for a heavily right-skewed sample?",
        [
        "Because the mean is always equal to the median",
        "Because skewness only affects categorical data",
        "Because the mean cannot be computed for skewed data",
        "Because the extreme right tail contributes very large squared deviations",
        "A spread measure that does not square its deviations, such as the "
                 "interquartile range, is not distorted by that same extreme value",
         ],
        ["d", "e"],
        "Variance squares each deviation, so a single very large value is amplified and "
        "the variance becomes dominated by the tail. That is exactly why the "
        "interquartile range is preferred for skewed data: it is built from the quartiles "
        "and never looks at how far the extreme value sits from the centre.",
        PDF, "p.28"))

    out.append(mc(
        "L3-MC-008", 3, "Quantiles, quartiles and box plots",
        "What is the interquartile range?",
        ["Q3 - Q1",
         "x_max - x_min",
         "Q2",
         "Q3 + Q1",
         "The median is the second quartile, Q2"],
        ["a", "e"],
        "The IQR spans the middle 50% of the data, from the first quartile to the third, "
        "so it is Q3 - Q1. The range is the maximum minus the minimum, Q2 is the median "
        "rather than a spread, and the quartiles are cut points so the median is Q2.",
        PDF, "p.35", code="IQR(x)", r_functions=["IQR", "quantile"],
        origin="adapted_HT25"))

    out.append(mc(
        "L3-MC-009", 3, "Quantiles, quartiles and box plots",
        "Which statements about a standard box plot are TRUE?",
        ["The box spans Q1 to Q3.",
         "The line inside the box is the median.",
         "The whiskers reach the smallest and largest observed values, so nothing is ever "
         "plotted beyond them.",
         "Points beyond the whiskers are always errors in the data.",
         "A box plot shows the shape of the whole distribution."],
        ["a", "b"],
        "The box covers the middle 50% of the data and the line inside it is the median, "
        "which is the second of the five numbers a box plot is built from. The whiskers do "
        "not necessarily reach the extremes: R stops them at 1.5 times the IQR by default "
        "and plots anything further out on its own as a possible outlier. That is why a "
        "claim that nothing ever falls beyond them is false, and also why points beyond "
        "them are candidates for scrutiny rather than declared errors. A box plot "
        "summarises centre and spread but not the shape of the distribution.",
        PDF, "p.35"))

    out.append(mc(
        "L3-MC-010", 3, "Quantiles, quartiles and box plots",
        "Consider `y <- c(43, 23, 22, 104, 42)`. Which statement is TRUE?",
        ["The middle 50% of the values lie between Q1 = 23 and Q3 = 43",
         "The IQR is 20, which is far smaller than the range of 82, indicating the "
         "spread is driven by the extreme value",
         "The IQR equals the range",
         "The IQR cannot be computed for a sample of 5",
         "The IQR is larger than the standard deviation"],
        ["a", "b"],
        "Q1 = 23 and Q3 = 43, so IQR = 20, while the range is 104 - 22 = 82. The large "
        "gap is the signature of a single extreme value.",
        PDF, "p.38", code="y <- c(43, 23, 22, 104, 42)\nIQR(y)",
        r_functions=["IQR", "quantile", "range"]))

    out.append(mc(
        "L3-MC-011", 3, "Visualising continuous data",
        "Which of the following plots are the natural choices for numerical data?",
        ["Histogram",
         "Box plot",
         "Density plot",
         "Scatterplot",
         "Bar plot of counts per category"],
        ["a", "b", "c", "d"],
        "Histogram, box plot, density plot and scatterplot all summarise numerical "
        "data. A bar plot of category counts belongs to categorical data.",
        PDF, "p.47"))

    out.append(mc(
        "L3-MC-012", 3, "Describing two variables",
        "Which plot is used to show the relationship between two numerical variables?",
        [
        "A contingency table",
        "A frequency table",
        "A box plot",
        "A scatterplot",
        "In the GDP example the horizontal axis is on a log scale, so equal distances "
                 "along it mean equal ratios rather than equal differences",
         ],
        ["d", "e"],
        "A scatterplot places one numerical variable on each axis so you can see the "
        "direction, shape and strength of the relationship. Watch the axis scales: on a "
        "log scale the spacing between ticks is a ratio rather than a difference, so a "
        "relationship can look curved on a linear axis and nearly straight on a log one.",
        PDF, "p.41"))

    out.append(mc(
        "L3-MC-013", 3, "Describing two variables",
        "You want to compare the distribution of a numerical variable across the levels "
        "of a categorical variable. Which approach is used?",
        ["Side-by-side box plots grouped by the categorical variable",
         "A single box plot of the pooled data",
         "A bar plot of the means only",
         "Comparing the medians and the spreads of the groups, which is what the "
         "side-by-side boxes are there to show",
         "A scatterplot with colour"],
        ["a", "d"],
        "Grouped box plots let you compare centre, spread and outliers across groups at "
        "once, rather than only comparing summary numbers. Comparing the medians and the "
        "spreads is exactly what those boxes are drawn to let you do, which a bar plot of "
        "means alone cannot.",
        PDF, "p.45"))

    # ------------------------------------------------------------ type coercion
    out.append(mc(
        "L3-MC-014", 3, "Type hierarchy and implicit coercion",
        "Consider the following code. What is the class of `z`?",
        ["logical",
         "numeric",
         "integer",
         "character"],
        ["d"],
        "`c(TRUE, \"FALSE\")` combines a logical with a character, and the hierarchy "
        "logical -> integer -> double -> character means the result is coerced to the "
        "highest type, character.",
        PDF, "p.57", code="z <- c(TRUE, \"FALSE\")\nclass(z)",
        r_functions=["c", "class"], origin="adapted_HT25"))

    out.append(mc(
        "L3-MC-015", 3, "Type hierarchy and implicit coercion",
        "Which statements about R's type hierarchy are TRUE?",
        ["The hierarchy runs logical -> integer -> double -> character.",
         "TRUE cannot be coerced to a number, because logical is the lowest type in the "
         "hierarchy.",
         "Characters can be coerced to numbers implicitly.",
         "Integers and doubles can be coerced to characters.",
         "Explicit conversion is never needed, because R coerces characters to numbers "
         "automatically."],
        ["a", "d"],
        "Coercion only ever moves UP the hierarchy, never down, so the claim that "
        "characters become numbers implicitly is false, and going back from character to "
        "numeric needs an explicit `as.numeric()`. TRUE becoming 1 happens automatically "
        "without that call, because a logical combined with a number is promoted to "
        "numeric.",
        PDF, "p.56", code="class(c(TRUE, 2))",
        r_functions=["as.numeric", "class", "c"], origin="adapted_HT25"))

    out.append(mc(
        "L3-MC-016", 3, "Common pitfall: coercion",
        "Consider the code below. What does `mean(x)` return, and why?",
        ["2, because R converts the string to a number",
         "NA with a warning, because x is a character vector and R will not convert it "
         "for you",
         "An error that stops the script",
         "\"2\", a character result",
         "Converting with `as.numeric()` first makes the mean work and returns 2"],
        ["b", "e"],
        "`c(1, 2, \"3\")` is coerced entirely to character, so mean() refuses it and "
        "returns NA with a warning rather than an error. The fix is "
        "`mean(as.numeric(x))`, which gives 2.",
        PDF, "p.58",
        code="x <- c(1, 2, \"3\")\nclass(x)\nmean(x)\nmean(as.numeric(x))",
        r_functions=["c", "mean", "as.numeric", "class"]))

    # -------------------------------------------------------------------- joins
    out.append(mc(
        "L3-MC-017", 3, "Merging data",
        "Consider `students` with ids 1-4 and `scores` with ids 2-5. What does "
        "`inner_join(students, scores, by = \"id\")` return?",
        ["Only the ids that appear in both tables are kept",
         "4 rows, covering ids 1 to 4",
         "3 rows, covering ids 2 to 4",
         "3 rows, covering ids 2 to 5",
         "4 rows, with NA scores for id 1"],
        ["a", "c"],
        "An inner join keeps only ids present in BOTH tables, which here is 2, 3 and 4. "
        "Id 1 is missing from scores and id 5 from students, so both are dropped.",
        PDF, "p.61", r_functions=["inner_join", "dplyr"]))

    # ---- The four joins sit on four consecutive pages: inner p.61, left p.62,
        # right p.63, full p.64. This question was cited to p.64 while one of its
        # two correct options was about left_join, which is on p.62, so the cited
        # page supported only half the answer. Reframed around full_join alone,
        # which p.64 shows in full: five rows, NA on whichever side is missing.

    out.append(mc(
        "L3-MC-018", 3, "Merging data",
        "Look at the output of `full_join(students, scores)`. Which statements are TRUE?",
        ["It keeps 5 rows: all 4 students plus the score that has no student.",
         "It keeps only the ids that appear in both tables.",
         "Rows present in just one table are kept, with NA on the missing side.",
         "Alice keeps a score, because her id is in the first table.",
         "It returns the same rows as `inner_join()` here."],
        ["a", "c"],
        "The output on p.64 has five rows: the four students and the one score with no "
        "student, so the claim that it keeps only shared ids is false. Alice has no score, "
        "which is the missing side filled with NA, and the score-only row has NA for the "
        "name. An inner join would keep only the 3 shared ids, so the two differ here.",
        PDF, "p.64", r_functions=["full_join", "inner_join"]))

    # ---- right_join is offered as a distractor in this question, so it is named
        # in r_functions. It is still the one join of the four with no question
        # devoted to it; worth adding when the bank grows.
    out.append(mc(
        "L3-MC-019", 3, "Merging data",
        "You need every row of `students` preserved, even if a student has no matching "
        "score. Which join do you use?",
        [
        "`full_join(students, scores, by = \"id\")`",
        "`inner_join`",
        "`left_join(students, scores, by = \"id\")`",
        "To add the variables from one table onto the rows of another, enriching it "
                 "without recomputing anything",
        "`right_join(students, scores, by = \"id\")`",
         ],
        ["c", "d"],
        "A left join keeps every row of the left-hand table and fills unmatched columns "
        "with NA, which is what preserves a student who has no score. A right join would "
        "keep the scores side instead, and a full join would also pull in id 5, neither "
        "of which is wanted here.",
        PDF, "p.62", r_functions=["left_join", "right_join"]))

    out.append(mc(
        "L3-MC-020", 3, "Merging data",
        "Why is merging data useful?",
        ["To increase the sample size",
         "To bring together information stored in different tables and align datasets "
         "collected from different sources",
         "To convert character columns to numbers",
         "To enrich the data with new variables",
         "To compute a correlation coefficient"],
        ["b", "d"],
        "The reasons are: combining information from different "
        "tables, enriching data with new variables, and aligning datasets from "
        "different sources. Merging neither adds observations nor changes types.",
        PDF, "p.60", r_functions=["left_join", "inner_join"]))


    # ---------------------------------------------------------------- written
    out.append(wa(
        "L3-WA-001", 3, "Measures of central tendency",
        "Consider the vector `x = c(2, 4, 6, 8)`. Without doing the actual "
        "calculations, write down the formula you would use for the mean, the variance "
        "and the standard deviation.",
        "Mean: `xbar = sum(x)/n = (2+4+6+8)/4`. Variance: `s^2 = (1/(n-1)) * "
        "sum((x_i - xbar)^2)` with n = 4 and xbar = 5. Standard deviation: "
        "`s = sqrt(s^2) = sqrt((1/(4-1)) * sum((x_i - 5)^2))`. No final numbers are "
        "needed.",
        [rb("Mean formula written as sum(x)/n with the values substituted"),
         rb("Sample variance formula written with 1/(n-1) and deviations from the mean"),
         rb("Standard deviation given as the square root of the variance")],
        1, PDF, "p.38", code="x <- c(2, 4, 6, 8)",
        r_functions=["mean", "var", "sd"], origin="adapted_HT25"))

    out.append(wa(
        "L3-WA-002", 3, "Quantiles, quartiles and box plots",
        "What does the interquartile range measure, in terms of the quartiles?",
        "The interquartile range spans the middle 50% of the data, running from Q1 to "
        "Q3, so it is Q3 - Q1. Quartiles divide the data into four equal parts, with "
        "Q1 the 25th percentile and Q3 the 75th.",
        [rb("IQR described as running from Q1 to Q3", 2),
         rb("Q3 - Q1 given as the formula", 2),
         rb("Q1 named as the 25th percentile and Q3 the 75th", 2)],
        1, PDF, "p.35",
        detail="Because the median is the 50th percentile, half the data falls below it and half above, which is the one dividing point a box plot marks exactly. Preferring the IQR over the standard deviation when a distribution is skewed is a sound habit, but it is a property of the two measures rather than something this page states."))

    out.append(wa(
        "L3-WA-003", 3, "Type hierarchy and implicit coercion",
        "Explain R's type hierarchy for implicit coercion, and describe the common pitfall "
        "with `c(1, 2, \"3\")`.",
        "R promotes types up the hierarchy logical, integer, double, character, so `c(1, 2, \"3\")` becomes entirely character. `mean()` on that returns NA with a warning, because R will not convert strings for you.",
        [rb("Hierarchy stated in order, lowest to highest flexibility", 2),
         rb("Notes coercion only goes upward, never downward", 2),
         rb("Identifies that `c(1,2,\"3\")` becomes character", 2),
         rb("States mean() returns NA and that as.numeric() is the fix", 2)],
        1, PDF, "p.58", code="mean(c(1, 2, \"3\"))\nmean(as.numeric(c(1, 2, \"3\")))",
        r_functions=["c", "mean", "as.numeric"],
        detail="The fix is an explicit conversion, `mean(as.numeric(c(1, 2, \"3\")))`. This is the single most common source of NA results in practice, and it usually appears when a numeric column has picked up a stray non-numeric entry such as a dash or a space. `str()` on the column will reveal the type, and `is.numeric()` tests it."))

    out.append(wa(
        "L3-WA-004", 3, "Merging data",
        "Compare a left join and an inner join in terms of what happens to rows "
        "that have no match in the other table, and give a situation where each "
        "one is the right choice.",
        "A left join keeps every row of the left dataset and fills unmatched ones "
        "with NA. An inner join keeps only rows matched in both, dropping the "
        "rest. Use left when the left table is the list of interest, inner to "
        "compare on shared cases.",
        [rb("Left join described as keeping all left rows", 2),
         rb("Unmatched rows filled with NA rather than dropped", 2),
         rb("Inner join described as keeping only rows matched in both", 2),
         rb("Contrasts the two and gives a situation for each", 2)],
        1, PDF, "p.62", r_functions=["left_join", "inner_join"], also=["p.61"],
        detail="The two slides are one comparison split across a page break: one "
               "states what the inner join keeps, the other what the left join "
               "keeps. An inner join rarely errors, which is why comparing row "
               "counts before and after is the cheapest safety check available. "
               "Right joins and full joins complete the family."))

    out.append(wa(
        "L3-WA-005", 3, "Describing two variables",
        "What does a correlation coefficient measure, and what do the values -1, 0 and "
        "+1 mean?",
        "A correlation coefficient quantifies the strength and direction of the "
        "linear relationship between two continuous variables. The most common is "
        "Pearson's r, ranging from -1 to 1: 1 is a perfect positive linear "
        "relationship, -1 a perfect negative one, and 0 no linear relationship.",
        [rb("Pearson correlation coefficient named as the most common measure"),
         rb("Strength AND direction of the LINEAR relationship between two continuous variables"),
         rb("Range from -1 to 1"),
         rb("1 = perfect positive, -1 = perfect negative, 0 = no linear relationship", 2)],
        1, PDF, "p.42",
        detail="Correlation measures linear association only, so a value near 0 does not rule out a curved relationship. Two clearly curved clouds can correlate at almost zero. It is also unit-free and unaffected by linear rescaling, but it is not a measure of cause, and a high value in observational data can still be explained by a confounding variable."))

    out.append(wa(
        "L3-WA-006", 3, "Measures of central tendency",
        "A dataset has mean 46.8 and median 42. Explain what this tells you about the "
        "shape of the distribution, why the median is the safer summary here, and which "
        "measure of spread you would report alongside it.",
        "A mean above the median indicates right skew, because a long right tail pulls the "
        "mean upward. The median is safer: it is robust to outliers and skew, the mean "
        "is sensitive to both. Report the standard deviation, or Q1 and Q3 for quartiles.",
        [rb("Identifies right skew from mean exceeding median", 2),
         rb("Explains that a long right tail pulls the mean up", 2),
         rb("Names the median as the robust choice, citing its resistance to skew", 2),
         rb("Standard deviation named as the spread to report", 2),
         rb("Q1 and Q3 offered as the quartile alternative", 1)],
        1, PDF, "p.21", also=["p.28", "p.35"],
        r_functions=["mean", "median", "sd", "IQR"],
        detail="The order of mean and median is a quick diagnostic: mean above median means right skew, mean below median means left skew, and the two roughly equal suggests symmetry. A grouped box plot by category is the natural way to spot it, since a category that stands out on a log-scaled income variable is usually a mixture rather than a single skewed population."))

    out.append(wa(
        "L3-WA-007", 3, "Measures of spread",
        "Without doing the actual calculations, what is the median of "
        "`y = c(43, 23, 22, 104, 42)`? Explain your reasoning.",
        "Order the data first: 22, 23, 42, 43, 104. With n = 5 the median is the third "
        "value, so the median is 42. The value 104 is far too large to affect the median "
        "at all, which is the point of using it here.",
        [rb("Data ordered correctly as 22, 23, 42, 43, 104"),
         rb("Identifies the middle position for n = 5"),
         rb("States the median is 42"),
         rb("Notes the median is unaffected by the extreme value")],
        1, PDF, "p.17", code="y <- c(43, 23, 22, 104, 42)\nmedian(y)",
        r_functions=["median", "sort"], origin="adapted_HT25"))

    out.append(wa(
        "L3-WA-008", 3, "Visualising continuous data",
        "Explain why you would generally prefer a histogram to a bar plot for summarising "
        "a numerical variable.",
        "A bar plot treats axis categories as separate labels with gaps, which suits nominal categories but wastes the fact that numerical values are ordered and evenly spaced. A histogram places values into ordered bins with no gaps, so shape, centre and skewness become visible.",
        [rb("Bar plot treats categories as unordered labels", 2),
         rb("Histogram uses ordered bins with no gaps", 2),
         rb("Notes this reveals distribution shape, centre and skewness")],
        1, PDF, "p.24", r_functions=["geom_histogram", "geom_bar"],
        detail="The gap is the tell: if the axis could sensibly carry intermediate values, a histogram is the right choice. A histogram of a categorical variable is not meaningful because the bin edges would imply a numeric spacing that the categories do not have. The number of bins also controls how much detail you see, and it is a display choice rather than part of the data."))

    return out