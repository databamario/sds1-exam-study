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
         "The range is 82"],
        ["a", "c", "e"],
        "Ordered, the values are 22, 23, 42, 43, 104, so the middle value and therefore "
        "the median is 42. The single large value 104 drags the mean (46.8) well above "
        "the median, and the range is 104 - 22 = 82. There is no repeated value, so "
        "there is no mode.",
        PDF, "p.17", code="y <- c(43, 23, 22, 104, 42)\nmedian(y)",
        r_functions=["median", "mean", "range", "sort"], origin="adapted_HT25"))

    out.append(mc(
        "L3-MC-002", 3, "Measures of central tendency",
        "A distribution is strongly right-skewed. What does that imply?",
        ["mean is smaller than median",
         "mean is larger than median",
         "mean and median are always equal",
         "the mode cannot be identified",
         "the variance must be zero"],
        ["b"],
        "In a right-skewed distribution the long tail pulls the mean upward, so the mean "
        "exceeds the median. The left-skewed case is the mirror image.",
        PDF, "p.23"))

    out.append(mc(
        "L3-MC-003", 3, "Measures of central tendency",
        "Which statements about the three measures of central tendency are TRUE?",
        ["The mean uses every observation.",
         "The median is robust to extreme values.",
         "The mode is the only measure that works for categorical data.",
         "The mean is always reported with a standard deviation.",
         "The mode can be multimodal."],
        ["a", "b", "c", "e"],
        "The mean uses all values and the median resists outliers, but a standard "
        "deviation is not a compulsory companion of the mean, so (d) is false.",
        PDF, "p.19"))

    out.append(mc(
        "L3-MC-004", 3, "Measures of central tendency",
        "Without doing the calculation, what is the mean of `x = c(2, 4, 6, 8)`?",
        ["2",
         "4",
         "5",
         "6",
         "It cannot be determined without computing it"],
        ["c"],
        "The values are evenly spaced and symmetric around 5, and the formula "
        "`xbar = sum(x)/n = (2+4+6+8)/4` gives 20/4 = 5. You do not need to do the "
        "arithmetic on the exam.",
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
         "`s^2 = sum(x_i - xbar)`",
         "`s^2 = sqrt((1/(n-1)) * sum((x_i - xbar)^2))`"],
        ["b"],
        "The sample variance divides the sum of squared deviations by n - 1, an unbiased "
        "correction. Option (a) is the population variance, (c) omits subtracting the "
        "mean, and (e) is the standard deviation rather than the variance.",
        PDF, "p.27", origin="adapted_HT25"))

    out.append(mc(
        "L3-MC-007", 3, "Measures of spread",
        "Why is the mean a poor measure of spread for a heavily right-skewed sample?",
        ["Because the mean cannot be computed for skewed data",
         "Because the extreme right tail contributes very large squared deviations",
         "Because the mean is always equal to the median",
         "Because skewness only affects categorical data",
         "Because the standard deviation is undefined for skewed data"],
        ["b"],
        "Variance squares each deviation, so a single very large value is amplified and "
        "the variance becomes dominated by the tail. That is exactly why the "
        "interquartile range is preferred for skewed data.",
        PDF, "p.26"))

    out.append(mc(
        "L3-MC-008", 3, "Quantiles, quartiles and box plots",
        "What is the interquartile range?",
        ["Q3 - Q1",
         "x_max - x_min",
         "Q2",
         "Q3 + Q1",
         "The difference between the mean and the median"],
        ["a"],
        "The IQR spans the middle 50% of the data, from the first quartile to the third, "
        "so it is Q3 - Q1. The range is the maximum minus the minimum.",
        PDF, "p.35", code="IQR(x)", r_functions=["IQR", "quantile"],
        origin="adapted_HT25"))

    out.append(mc(
        "L3-MC-009", 3, "Quantiles, quartiles and box plots",
        "Which statements about a standard box plot are TRUE?",
        ["The box spans Q1 to Q3.",
         "The line inside the box is the median.",
         "The whiskers extend to the most extreme observed values by default.",
         "Points beyond the whiskers are always errors in the data.",
         "A box plot shows the shape of the whole distribution."],
        ["a", "b", "c"],
        "Points plotted beyond the whiskers are flagged as potential outliers, not "
        "declared errors, so (d) is false. A box plot summarises spread and centre but "
        "does not reveal the shape of the distribution, so (e) is false too.",
        PDF, "p.35"))

    out.append(mc(
        "L3-MC-010", 3, "Quantiles, quartiles and box plots",
        "Consider `y <- c(43, 23, 22, 104, 42)`. Which statement is TRUE?",
        ["The IQR is large, so the data are not skewed",
         "The IQR is 20, which is far smaller than the range of 82, indicating the "
         "spread is driven by the extreme value",
         "The IQR equals the range",
         "The IQR cannot be computed for a sample of 5",
         "The IQR is larger than the standard deviation"],
        ["b"],
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
         "A bar plot",
         "A contingency table",
         "A frequency table"],
        ["b"],
        "A scatterplot places one numerical variable on each axis so you can see the "
        "direction, shape and strength of the relationship.",
        PDF, "p.41"))

    out.append(mc(
        "L3-MC-013", 3, "Describing two variables",
        "You want to compare the distribution of a numerical variable across the levels "
        "of a categorical variable. Which approach does the lecture use?",
        ["Side-by-side box plots grouped by the categorical variable",
         "A single box plot of the pooled data",
         "A bar plot of the means only",
         "A scatterplot with colour",
         "A contingency table"],
        ["a"],
        "Grouped box plots let you compare centre, spread and outliers across groups at "
        "once, rather than only comparing summary numbers.",
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
         "Explicit conversion is needed to go from character back to numeric."],
        ["a", "b", "d", "e"],
        "Coercion only ever moves UP the hierarchy, never down, so (c) is false. Going "
        "from character back to numeric requires an explicit `as.numeric()`.",
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
         "1, because only the first element is numeric"],
        ["b"],
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
        ["5 rows, covering ids 1 to 5",
         "4 rows, covering ids 1 to 4",
         "3 rows, covering ids 2 to 4",
         "3 rows, covering ids 2 to 5",
         "4 rows, with NA scores for id 1"],
        ["c"],
        "An inner join keeps only ids present in BOTH tables, which here is 2, 3 and 4. "
        "Id 1 is missing from scores and id 5 from students, so both are dropped.",
        PDF, "p.61", r_functions=["inner_join", "dplyr"]))

    out.append(mc(
        "L3-MC-018", 3, "Merging data",
        "Consider the same tables. Which statements about the joins are TRUE?",
        ["`left_join(students, scores)` keeps all 4 students, giving Alice an NA score.",
         "`right_join(students, scores)` keeps all 4 scores, giving id 5 an NA name.",
         "`full_join(students, scores)` keeps all 5 rows.",
         "`inner_join(students, scores)` keeps 5 rows.",
         "A left join and a right join return the same rows here."],
        ["a", "b", "c"],
        "The inner join keeps only the 3 overlapping ids, so (d) is false. A left join "
        "keeps the 4 left rows and a right join keeps the 4 right rows, which differ, so "
        "(e) is false.",
        PDF, "p.62", r_functions=["left_join", "right_join", "full_join", "inner_join"]))

    out.append(mc(
        "L3-MC-019", 3, "Merging data",
        "You need every row of `students` preserved, even if a student has no matching "
        "score. Which join do you use?",
        ["`inner_join`",
         "`left_join(students, scores, by = \"id\")`",
         "`right_join(students, scores, by = \"id\")`",
         "`full_join(students, scores, by = \"id\")`",
         "No join; filter the scores table first"],
        ["b"],
        "A left join keeps every row of the left-hand table and fills unmatched columns "
        "with NA. A full join would also pull in id 5 from scores, which is not wanted "
        "here.",
        PDF, "p.62", r_functions=["left_join"]))

    out.append(mc(
        "L3-MC-020", 3, "Merging data",
        "Why is merging data useful in this course?",
        ["To increase the sample size",
         "To bring together information stored in different tables and align datasets "
         "collected from different sources",
         "To convert character columns to numbers",
         "To remove duplicate rows",
         "To compute a correlation coefficient"],
        ["b"],
        "The lecture gives exactly these reasons: combining information from different "
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
        "The interquartile range spans the middle 50% of the data, from Q1 to Q3, so it "
        "is Q3 - Q1. The standard deviation squares every deviation from the mean, so a "
        "single very large value inflates it heavily. Because the IQR depends only on "
        "the middle half of the ordered data, it ignores the extreme tail and is "
        "therefore much more stable for skewed data.",
        [rb("IQR defined as Q3 - Q1 and described as the middle 50%", 2),
         rb("Explains that squaring amplifies the influence of extreme values", 2),
         rb("Concludes the IQR is therefore preferable for skewed data")],
        1, PDF, "p.35", r_functions=["IQR", "quantile"]))

    out.append(wa(
        "L3-WA-003", 3, "Type hierarchy and implicit coercion",
        "Explain R's type hierarchy for implicit coercion, and describe the common pitfall "
        "with `c(1, 2, \"3\")`.",
        "When types are combined R promotes them up the hierarchy logical -> integer -> "
        "double -> character, so TRUE becomes 1 and numbers can become strings. The "
        "pitfall is that `c(1, 2, \"3\")` is coerced entirely to character, and calling "
        "`mean()` on it returns NA with a warning because R will not convert strings for "
        "you. The fix is an explicit conversion, `mean(as.numeric(c(1, 2, \"3\")))`.",
        [rb("Hierarchy stated in order, lowest to highest flexibility", 2),
         rb("Notes coercion only goes upward, never downward", 2),
         rb("Identifies that `c(1,2,\"3\")` becomes character", 2),
         rb("States mean() returns NA and that as.numeric() is the fix", 2)],
        1, PDF, "p.58", code="mean(c(1, 2, \"3\"))\nmean(as.numeric(c(1, 2, \"3\")))",
        r_functions=["c", "mean", "as.numeric"]))

    out.append(wa(
        "L3-WA-004", 3, "Merging data",
        "Explain the difference between an inner join and a left join, and give a "
        "situation where you would need a left join rather than an inner join.",
        "An inner join keeps only the rows whose key appears in both tables, so any "
        "unmatched row on either side is silently discarded. A left join keeps every row "
        "of the left-hand table and fills unmatched columns with NA. You would need a "
        "left join when the left table is the list of interest, for example keeping all "
        "students even when some have no recorded score, because an inner join would "
        "quietly drop those students and change who is in the study.",
        [rb("Inner join described as keeping only rows matched in both", 2),
         rb("Left join described as keeping all left rows and filling with NA", 2),
         rb("Gives a concrete situation where dropping rows would be wrong", 2)],
        1, PDF, "p.62", r_functions=["inner_join", "left_join"]))

    out.append(wa(
        "L3-WA-005", 3, "Describing two variables",
        "Write down the R code to compute the correlation between two numerical vectors, "
        "and say what values close to -1, 0 and +1 indicate.",
        "```r\ncor(x, y)\n```\nA value close to +1 means a strong positive linear "
        "relationship, close to -1 a strong negative linear relationship, and close to 0 "
        "little or no linear relationship. Correlation measures linear association only, "
        "so a value near 0 does not rule out a curved relationship.",
        [rb("`cor()` used to compute the correlation"),
         rb("+1 described as a strong positive linear relationship"),
         rb("-1 described as a strong negative linear relationship"),
         rb("0 described as little or no LINEAR relationship")],
        1, PDF, "p.42", code="cor(x, y)", r_functions=["cor"]))

    out.append(wa(
        "L3-WA-006", 3, "Measures of central tendency",
        "A dataset has mean 46.8 and median 42. Explain what this tells you about the "
        "shape of the distribution and name one statistic you would report alongside the "
        "mean.",
        "The mean sitting above the median indicates a right-skewed distribution, because "
        "a long right tail of large values pulls the mean upward. A sensible companion to "
        "the mean here would be the standard deviation for a roughly symmetric "
        "distribution, or the interquartile range when the skew is strong.",
        [rb("Identifies right skew from mean exceeding median", 2),
         rb("Explains that a long right tail pulls the mean up", 2),
         rb("Names a suitable accompanying statistic and justifies it")],
        1, PDF, "p.23", r_functions=["mean", "median", "sd", "IQR"]))

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
        "A bar plot treats the categories on the axis as separate labels with gaps "
        "between them, which suits nominal categories but wastes the fact that numerical "
        "values are ordered and evenly spaced. A histogram places values into ordered "
        "bins with no gaps, so the shape of the distribution, its centre and any skewness "
        "become visible.",
        [rb("Bar plot treats categories as unordered labels", 2),
         rb("Histogram uses ordered bins with no gaps", 2),
         rb("Notes this reveals distribution shape, centre and skewness")],
        1, PDF, "p.47", r_functions=["geom_histogram", "geom_bar"]))

    return out