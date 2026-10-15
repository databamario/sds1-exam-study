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
        "A distribution is strongly right-skewed. What does that imply?",
        ["mean is smaller than median",
         "mean is larger than median",
         "the median is robust to extreme values and skewness",
         "mean and median are always equal",
         "the mode cannot be identified"],
        ["b", "c"],
        "In a right-skewed distribution the long tail pulls the mean upward, so the mean "
        "exceeds the median, and the median is left where it is because only the middle of "
        "the ordered data defines it. The left-skewed case is the mirror image.",
        PDF, "p.21"))

    out.append(mc(
        "L3-MC-003", 3, "Measures of central tendency",
        "Which statements about the three measures of central tendency are TRUE?",
        ["The mean is always reported with a standard deviation.",
         "The median is robust to extreme values.",
         "The mode is the only measure that works for categorical data.",
         "the mode can be multimodal.",
         "The median is pulled towards extreme values in a skewed sample."],
        ["b", "c"],
        "The median resists outliers and skewness because it only looks at the middle of "
        "the ordered data, and it is the mode that is meaningful for a categorical "
        "variable, where taking an average of the categories would be meaningless. A mode "
        "need not be unique, so a dataset can have more than one, and the median is not "
        "what gets pulled towards extreme values; the mean is.",
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
        PDF, "p.27"))

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
        ["Because the mean cannot be computed for skewed data",
         "Because the extreme right tail contributes very large squared deviations",
         "A spread measure that does not square its deviations, such as the "
         "interquartile range, is not distorted by that same extreme value",
         "Because the mean is always equal to the median",
         "Because skewness only affects categorical data"],
        ["b", "c"],
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
        PDF, "p.34", code="y <- c(43, 23, 22, 104, 42)\nIQR(y)",
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
        ["A box plot",
         "A scatterplot",
         "In the GDP example the horizontal axis is on a log scale, so equal distances "
         "along it mean equal ratios rather than equal differences",
         "A contingency table",
         "A frequency table"],
        ["b", "c"],
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
         "TRUE can be coerced to 1 and FALSE to 0.",
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

    out.append(mc(
        "L3-MC-018", 3, "Merging data",
        "Consider the same tables. Which statements about the joins are TRUE?",
        ["`left_join(students, scores)` keeps all 4 students, giving Alice an NA score.",
         "`right_join(students, scores)` keeps all 4 students, giving Alice an NA score.",
         "`full_join(students, scores)` keeps all 5 rows, filling the gaps with NA.",
         "`inner_join(students, scores)` keeps 5 rows.",
         "A left join and a right join return the same rows here."],
        ["a", "c"],
        "The inner join keeps only the 3 overlapping ids, so the claim that it keeps 5 rows "
        "is false. A left join keeps the 4 left rows and a right join keeps the 4 right "
        "rows, which differ here, so they are not interchangeable. A full join keeps every "
        "row from both sides, 5 in total, filling the gaps with NA.",
        PDF, "p.64", r_functions=["left_join", "right_join", "full_join", "inner_join"]))

    out.append(mc(
        "L3-MC-019", 3, "Merging data",
        "You need every row of `students` preserved, even if a student has no matching "
        "score. Which join do you use?",
        ["`inner_join`",
         "`left_join(students, scores, by = \"id\")`",
         "To add the variables from one table onto the rows of another, enriching it "
         "without recomputing anything",
         "`right_join(students, scores, by = \"id\")`",
         "`full_join(students, scores, by = \"id\")`"],
        ["b", "c"],
        "A left join keeps every row of the left-hand table and fills unmatched columns "
        "with NA, which is what preserves a student who has no score. A right join would "
        "keep the scores side instead, and a full join would also pull in id 5, neither "
        "of which is wanted here.",
        PDF, "p.62", r_functions=["left_join"]))

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
        1, PDF, "p.27", code="x <- c(2, 4, 6, 8)",
        r_functions=["mean", "var", "sd"], origin="adapted_HT25"))

    out.append(wa(
        "L3-WA-002", 3, "Quantiles, quartiles and box plots",
        "Explain what the interquartile range measures and why it is preferable to the "
        "standard deviation for a right-skewed distribution.",
        "The interquartile range spans the middle 50% of the data, from Q1 to Q3, so it is Q3 - Q1. The standard deviation squares every deviation from the mean, so a single very large value inflates it heavily.",
        [rb("IQR defined as Q3 - Q1 and described as the middle 50%", 2),
         rb("Explains that squaring amplifies the influence of extreme values", 2),
         rb("Concludes the IQR is therefore preferable for skewed data")],
        1, PDF, "p.35", r_functions=["IQR", "quantile"],
        detail="Because the IQR depends only on the middle half of the ordered data, it ignores the extreme tail and is far more stable for skewed data. That is why the IQR is the preferred measure of spread whenever the distribution is not roughly symmetric, and why income-type variables are routinely summarised with a median and IQR rather than a mean and standard deviation."))

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
        "Explain the difference between an inner join and a left join, and give a "
        "situation where you would need a left join rather than an inner join.",
        "An inner join keeps only rows whose key appears in both tables, discarding unmatched rows. A left join keeps every row of the left table and fills unmatched columns with NA. You need a left join when the left table is the list of interest.",
        [rb("Inner join described as keeping only rows matched in both", 2),
         rb("Left join described as keeping all left rows and filling with NA", 2),
         rb("Gives a concrete situation where dropping rows would be wrong", 2)],
        1, PDF, "p.62", r_functions=["inner_join", "left_join"],
        detail="Keeping all students even when some have no recorded score is the motivating case: an inner join would quietly drop those students and change who is in the study. Right joins and full joins complete the family. The danger of an inner join is that it rarely errors, so a row count before and after is the cheapest safety check available."))

    out.append(wa(
        "L3-WA-005", 3, "Describing two variables",
        "Write down the R code to compute the correlation between two numerical vectors, "
        "and say what values close to -1, 0 and +1 indicate.",
        "```r" 
                "```r "
                "cor(x, y) "
                "``` "
                "A value near +1 means a strong positive linear relationship, near -1 a strong negative one, and near 0 little or no linear relationship.",
        [rb("`cor()` used to compute the correlation"),
         rb("+1 described as a strong positive linear relationship"),
         rb("-1 described as a strong negative linear relationship"),
         rb("0 described as little or no LINEAR relationship")],
        1, PDF, "p.42", code="cor(x, y)", r_functions=["cor"],
        detail="Correlation measures linear association only, so a value near 0 does not rule out a curved relationship. Two clearly curved clouds can correlate at almost zero. It is also unit-free and unaffected by linear rescaling, but it is not a measure of cause, and a high value in observational data can still be explained by a confounding variable."))

    out.append(wa(
        "L3-WA-006", 3, "Measures of central tendency",
        "A dataset has mean 46.8 and median 42. Explain what this tells you about the "
        "shape of the distribution and name one statistic you would report alongside the "
        "mean.",
        "A mean sitting above the median indicates a right-skewed distribution, because a long right tail of large values pulls the mean upward. A sensible companion is the standard deviation if the distribution is roughly symmetric, or the interquartile range when the skew is strong.",
        [rb("Identifies right skew from mean exceeding median", 2),
         rb("Explains that a long right tail pulls the mean up", 2),
         rb("Names a suitable accompanying statistic and justifies it")],
        1, PDF, "p.23", r_functions=["mean", "median", "sd", "IQR"],
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
        1, PDF, "p.47", r_functions=["geom_histogram", "geom_bar"],
        detail="The gap is the tell: if the axis could sensibly carry intermediate values, a histogram is the right choice. A histogram of a categorical variable is not meaningful because the bin edges would imply a numeric spacing that the categories do not have. The number of bins also controls how much detail you see, and it is a display choice rather than part of the data."))

    return out