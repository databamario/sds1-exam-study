"""Graph-reading questions.

These sit alongside the other lecture modules and are collected by
``tools/build_bank.py``. Every one of them points at a figure produced by
``tools/figures.py`` via the ``image`` field.

The questions are deliberately about *inferring* from a shape rather than
reading a number off it, because that is what the exam asks for: which group
has the most variance, does the interval clear the reference line, is the mean
above or below the median. Reading a bar height is the easy case and gets far
less emphasis.
"""

from .common import mc, rb, wa

# Citations point at the slide where the same skill is taught. A single figure
# can carry more than one skill, so the citation is per question rather than per
# figure or per lecture: the three histogram questions split across "the mean
# reacts to skew" (SKEW_MM), "read the shape off a histogram" (SHAPE) and
# "wider therefore larger variance" (SPREAD). One tuple per lecture is what
# sent all of these to a single wrong page in the first place.
#
# Slide titles in the comment are the first line of that page, checked by hand
# against the PDFs. tools/validate.py re-checks that the name is a real file
# and that the page is inside it, and tools/audit_citations.py holds the
# expected value for every question below.
BOXPLOT = ("lecture3.pdf", "p.35")        # Quartiles and box plot
SKEW_MM = ("lecture3.pdf", "p.21")        # Measures of central tendency
SHAPE = ("lecture3.pdf", "p.24")          # Distribution and shape
DENSITY = ("lecture3.pdf", "p.25")        # Distribution and shape (cont.)
SPREAD = ("lecture3.pdf", "p.27")         # Variance and standard deviation
VARTYPE = ("lecture2.pdf", "p.23")        # Types of variables
FREQ = ("lecture2.pdf", "p.28")           # Frequency tables
PROP = ("lecture2.pdf", "p.29")           # Proportions
STACK = ("lecture2.pdf", "p.34")          # Grouped bar plots (position = "stack")
NORMALQ = ("lecture5_after.pdf", "p.28")  # Normal-curve area practice
CI = ("lecture7_after.pdf", "p.10")       # Sample distribution with 95% CI
SCATTER = ("lecture8_after.pdf", "p.12")  # Correlation example (the scatterplot)
CORR = ("lecture8_after.pdf", "p.20")     # Correlation matrix


def questions():
    out = []

    # ================================================== multiple choice (18)
    # ---- box plots: spread and centre
    out.append(mc(
        "G-MC-001", 3, "Reading a box plot",
        "Three groups are compared. Based on the plot, which group has the "
        "highest variance?",
        ["Group A", "Group B", "Group C",
         "They all have the same variance"],
        ["b"],
        "Group B has both the widest box, so the largest interquartile range, and "
        "the longest whiskers, so the widest overall spread. Group C is tightly "
        "clustered around 30 and therefore has by far the smallest variance.",
        BOXPLOT[0], BOXPLOT[1], image="boxplots_h"))

    out.append(mc(
        "G-MC-002", 3, "Reading a box plot",
        "Based on the plot, what can you say about the medians of the three "
        "groups?",
        ["Group B has the highest median",
         "Group A has the lowest median",
         "All three groups have the same median",
         "The medians cannot be compared from a box plot"],
        ["c"],
        "The dark line inside each box sits at 30 in all three groups, so the "
        "medians are equal even though the spreads differ. A box plot is built "
        "precisely so the median can be read off directly.",
        BOXPLOT[0], BOXPLOT[1], image="boxplots_h"))

    out.append(mc(
        "G-MC-003", 3, "Reading a box plot",
        "A box plot shows a box covering the middle 50% of the data. Which "
        "statement about group A in the plot is correct?",
        ["At least 75% of the values lie between 10 and 50",
         "The range of group A is 40",
         "About 25% of the values lie above 38",
         "The standard deviation of group A is 16"],
        ["c"],
        "The top edge of the box is the third quartile at 38, so roughly the top "
        "25% of values lie above it. A range of 40 would mean 50 minus 10, but "
        "the whiskers are not necessarily the true extremes, and the standard "
        "deviation cannot be read off a box plot at all.",
        BOXPLOT[0], BOXPLOT[1], image="boxplots_h"))

    # ---- skew and centre
    out.append(mc(
        "G-MC-004", 3, "Skew and centre",
        "Based on the shape of the histogram, would you expect the mean of this "
        "variable to be higher or lower than the median?",
        ["The mean is always higher for any right-skewed distribution",
         "Higher, because the long right tail pulls the mean up",
         "Lower, because the long right tail pulls the mean down",
         "They are always equal for this shape"],
        ["b"],
        "The distribution has a long tail to the right. The mean uses every value, "
        "so the few large values pull it up, while the median only cares about the "
        "middle observation and stays lower. Here the mean sits around 4 while the "
        "median is near 2.3.",
        SKEW_MM[0], SKEW_MM[1], image="hist_skewed"))

    out.append(mc(
        "G-MC-005", 3, "Skew and centre",
        "Which distribution is right-skewed, meaning it has a long tail to the "
        "right?",
        ["The one shown in the first plot",
         "The one shown in the second plot",
         "Both are right-skewed",
         "Neither is right-skewed"],
        ["a"],
        "The first plot has its mass on the left and a tail stretching to the "
        "right. A symmetric histogram such as the second has its centre in the "
        "middle and no long tail on either side.",
        SHAPE[0], SHAPE[1], image="hist_skewed"))

    out.append(mc(
        "G-MC-006", 3, "Shape and spread",
        "Two histograms have the same shape and the same centre but one is more "
        "spread out than the other. What is true of the more spread-out one?",
        ["Its variance is larger",
         "Its variance is smaller",
         "Its variance is zero because the shape is the same",
         "Its mean and median are further apart"],
        ["a"],
        "Variance measures how far values sit from the centre, so spreading the "
        "same shape out increases it. Identical shapes that differ only in width "
        "differ in variance and standard deviation but not in shape or centre.",
        SPREAD[0], SPREAD[1], image="hist_symmetric"))

    # ---- confidence intervals
    out.append(mc(
        "G-MC-007", 7, "Interpreting a confidence interval",
        "The plot shows a mean and a 95% confidence interval for two groups "
        "against a reference value. Which group differs significantly from the "
        "reference at the 5% level?",
        ["Neither group", "Group A only", "Group B only", "Both groups"],
        ["b"],
        "Group A's interval runs from about 48.6 to 56.2 and does not touch the "
        "reference line at 44, so the difference is significant. Group B's interval "
        "runs from about 41.3 to 48.9 and does contain 44, so it is not significant.",
        CI[0], CI[1], image="ci_dotplot"))

    out.append(mc(
        "G-MC-008", 7, "Interpreting a confidence interval",
        "Based on the plot, which group has the larger margin of error?",
        ["They are equal", "This cannot be determined", "Group A", "Group B"],
        ["c"],
        "The margin of error is half the width of the interval. Group A's spans "
        "about 7.6 units and Group B's about 3.8, so Group A's is larger and its "
        "estimate is less precise.",
        CI[0], CI[1], image="ci_dotplot"))

    out.append(mc(
        "G-MC-009", 7, "Interpreting a confidence interval",
        "What does it mean when a 95% confidence interval contains the reference "
        "value, as it does for group B?",
        ["There is a 95% probability the reference value is wrong",
         "The estimate is definitely equal to the reference value",
         "The sample size was too small to compute the interval",
         "The difference from the reference is not significant at the 5% level"],
        ["d"],
        "An interval that contains the reference value means the data are "
        "compatible with no difference, so we cannot reject the null hypothesis at "
        "the 5% level. It is not a probability statement about the reference value.",
        CI[0], CI[1], image="ci_dotplot"))

    # ---- scatter plot
    out.append(mc(
        "G-MC-010", 8, "Reading a scatter plot",
        "Based on the scatter plot, how would you describe the relationship "
        "between study hours and final score?",
        ["Positive and moderately strong",
         "Negative and strong",
         "No relationship at all",
         "Perfectly positive, since the points lie on a line"],
        ["a"],
        "The points drift upward from left to right, so more study hours go with "
        "higher scores, which is a positive association. The points are scattered "
        "around the trend rather than lying on a line, so the relationship is "
        "moderate rather than perfect.",
        SCATTER[0], SCATTER[1], image="scatter_trend"))

    out.append(mc(
        "G-MC-011", 8, "Reading a scatter plot",
        "If the correlation between the two variables were exactly 0, what would "
        "the scatter plot look like?",
        ["A set of distinct parallel groups",
         "A diffuse cloud with no upward or downward trend",
         "A tight upward-sloping line",
         "A tight downward-sloping line"],
        ["b"],
        "A correlation of 0 means no linear association, so the points form a "
        "cloud with no direction. A tight upward line would be a correlation near 1 "
        "and a tight downward line a correlation near -1.",
        SCATTER[0], SCATTER[1], image="scatter_trend"))

    # ---- densities
    out.append(mc(
        "G-MC-012", 3, "Comparing distributions",
        "The plot shows the densities of two groups. Which statement is correct?",
        ["Both groups have the same mean and the same spread",
         "Group A has the higher mean but the smaller spread",
         "Group B has the higher mean and the larger spread",
         "Group A has the higher mean and the larger spread"],
        ["c"],
        "Group B's curve peaks further to the right, so its values are typically "
        "larger, and it is much flatter and wider, so it is more spread out. Group "
        "A's curve is taller and narrower.",
        DENSITY[0], DENSITY[1], image="density_overlay"))

    out.append(mc(
        "G-MC-013", 3, "Comparing distributions",
        "The area under a density curve for one group is much larger than the "
        "area for the other. What does that tell you?",
        ["That group has a larger total value",
         "That group has a higher variance",
         "That group's mean is larger",
         "That group contains more observations"],
        ["d"],
        "Density curves are each normalised so the total area is 1 regardless of "
        "how many observations were collected. A larger area on the plot comes "
        "from a wider distribution, not a larger sample.",
        DENSITY[0], DENSITY[1], image="density_overlay"))

    # ---- correlation matrix
    out.append(mc(
        "G-MC-014", 8, "Reading a correlation matrix",
        "Based on the correlation matrix, which pair of variables has the "
        "strongest linear relationship?",
        ["Hours and Screen", "Hours and Sleep", "Sleep and Stress",
         "Screen and Caff"],
        ["a"],
        "Hours and Screen have a correlation of 0.62, the largest positive value "
        "in the matrix apart from the diagonal. Sleep and Stress is the strongest "
        "in absolute terms only by comparison with the other listed pairs at 0.33, "
        "which is still well below 0.62.",
        CORR[0], CORR[1], image="corr_heatmap"))

    out.append(mc(
        "G-MC-015", 8, "Reading a correlation matrix",
        "Which statement about the Hours and Sleep correlation of -0.28 is "
        "correct?",
        ["It is zero, so the variables are unrelated",
         "It is weak and negative",
         "It is strong and negative",
         "It is strong and positive"],
        ["b"],
        "The sign is negative, so the two move in opposite directions, and the "
        "magnitude is only 0.28, so the linear association is weak. It is not zero, "
        "so the variables are not unrelated.",
        CORR[0], CORR[1], image="corr_heatmap"))

    # ---- frequency bars
    out.append(mc(
        "G-MC-016", 2, "Reading a frequency table",
        "The bar chart shows how many students read each number of books last "
        "year. How many students are there in total?",
        ["30", "11", "20", "9"],
        ["a"],
        "Add the bar heights: 2 + 5 + 11 + 9 + 3 = 30. Reading only the tallest "
        "bar would give 11, which is just the modal group.",
        FREQ[0], FREQ[1], image="freq_bars"))

    out.append(mc(
        "G-MC-017", 2, "Reading a frequency table",
        "Using the same bar chart, what proportion of students read fewer than 20 "
        "books?",
        ["11/30", "2/30", "20/30", "7/30"],
        ["d"],
        "Fewer than 20 books covers the first two bars, 2 + 5 = 7 students out of "
        "30 in total, so the proportion is 7/30.",
        PROP[0], PROP[1], image="freq_bars"))

    out.append(mc(
        "G-MC-018", 2, "Reading a frequency table",
        "The same bar chart shows books read per student. Which variable type and "
        "measurement level does it represent?",
        ["Quantitative discrete",
         "Quantitative continuous",
         "Categorical nominal",
         "Categorical ordinal"],
        ["a"],
        "Books is a count, so it is quantitative and discrete because you cannot "
        "read 2.5 books. It is not categorical, because the categories would have "
        "to be labels rather than numbers.",
        VARTYPE[0], VARTYPE[1], image="freq_bars"))

    # ======================================================= written answers (12)
    out.append(wa(
        "G-WA-001", 3, "Reading a box plot",
        "Based on the plot, explain which group has the highest variance and why.",
        "Group B has the highest variance. Its box is the widest, so it has the largest interquartile range, and its whiskers extend furthest, so it covers the widest overall range. Group C is tightly clustered around 30 and has the smallest variance.",
        [rb("Names group B as having the highest variance"),
         rb("Refers to the width of the box or interquartile range"),
         rb("Refers to the length of the whiskers or the overall range",
            elements=2)],
        2, BOXPLOT[0], BOXPLOT[1], image="boxplots_h",
        detail="The variance measures average squared distance from the mean, so a "
               "wider spread always gives a larger variance. Here the three medians "
               "are all 30, so the groups differ only in spread, which makes this a "
               "clean comparison: same centre, different variance."))

    out.append(wa(
        "G-WA-002", 3, "Skew and centre",
        "Based on the histogram, do you expect the mean of this variable to be "
        "higher or lower than the median? Justify your answer.",
        "The mean is higher than the median. The distribution is right-skewed, so its long right tail holds a few large values, and the mean uses every value and is pulled up by that tail. The median depends only on the middle observation.",
        [rb("States that the mean is higher than the median"),
         rb("Identifies the distribution as right-skewed with a long right tail"),
         rb("Explains that the tail pulls the mean up but not the median")],
        2, SKEW_MM[0], SKEW_MM[1], image="hist_skewed",
        detail="A quick way to read this off a histogram is to look for an "
               "asymmetry: a long thin tail on one side is what separates the mean "
               "from the median. The reverse happens for a left-skewed "
               "distribution, where the mean falls below the median. Neither the "
               "mean nor the median can be read exactly from a histogram, only "
               "compared."))

    out.append(wa(
        "G-WA-003", 7, "Interpreting a confidence interval",
        "The plot shows a mean and a 95% confidence interval for each group "
        "against a reference value. Which group differs significantly from the "
        "reference, and what does that mean?",
        "Group A differs significantly from the reference at the 5% level, because its interval lies entirely above the reference line so the reference is not a plausible population mean. Group B's interval contains the reference, so for group B we cannot reject the null.",
        [rb("Names group A as the significant one"),
         rb("Notes that group A's interval excludes the reference value"),
         rb("Notes that group B's interval contains the reference value"),
         rb("Links this to rejecting or not rejecting the null hypothesis")],
        3, CI[0], CI[1], image="ci_dotplot",
        detail="This is the whole logic of a hypothesis test expressed as a "
               "picture. A 95% interval that misses the value you are testing "
               "against corresponds to a p-value below 0.05, and one that contains "
               "it corresponds to a p-value above 0.05. Note that the interval "
               "describes the precision of the estimate, not the probability that "
               "the true mean lies inside it."))

    out.append(wa(
        "G-WA-004", 7, "Interpreting a confidence interval",
        "Using the same plot, which group has the larger margin of error, and "
        "what does that tell you about the two estimates?",
        "Group A has the larger margin of error, because its interval is about twice as wide as group B's. Group A's estimate is therefore less precise, so we are less certain about its population mean even though its point estimate sits further from the reference.",
        [rb("Names group A as having the larger margin of error"),
         rb("Relates the margin of error to the width of the interval"),
         rb("Explains that group A's estimate is less precise")],
        2, CI[0], CI[1], image="ci_dotplot",
        detail="A wider interval usually means a larger standard error, which "
               "typically comes from a smaller sample size or more variability in "
               "the data. Precision and statistical significance are different "
               "things: a wide interval can still miss the reference value, and a "
               "narrow one can still contain it."))

    out.append(wa(
        "G-WA-005", 8, "Reading a scatter plot",
        "Describe the relationship between study hours and final score shown in "
        "the plot, and say whether you would describe it as strong or weak.",
        "The relationship is positive: more study hours go with higher final scores. I would call it moderate rather than strong, because the points are scattered widely around the upward trend instead of hugging a single line. The direction is clear but much variation is unexplained.",
        [rb("Identifies the relationship as positive"),
         rb("Describes the strength as moderate or imperfect, not strong"),
         rb("Mentions that the points are scattered around the trend")],
        2, SCATTER[0], SCATTER[1], image="scatter_trend",
        detail="Strength here refers to how tightly the points follow the trend, "
               "not to whether a trend exists at all. A visible upward drift with a "
               "wide cloud still counts as a positive association, and the "
               "correlation coefficient would land somewhere around 0.6. Remember "
               "that association is not causation: nothing in this plot shows that "
               "the study hours caused the scores."))

    out.append(wa(
        "G-WA-006", 3, "Comparing distributions",
        "The plot shows the densities of two groups. Compare their centres and "
        "their spreads.",
        "Group B is centred further right than group A, so it has the higher typical "
        "value. Group B is also flatter and wider, so it has the larger spread, "
        "while Group A's curve is taller and narrower.",
        [rb("States that group B has the higher centre or mean"),
         rb("States that group B has the larger spread or variance"),
         rb("Notes that group A's curve is narrower and more concentrated")],
        2, DENSITY[0], DENSITY[1], image="density_overlay",
        detail="A taller peak does not mean a larger total, because each density is "
               "normalised to have area 1. Height and width trade off: the curve "
               "that is spread out must be flatter for its area to stay the same. "
               "Overlapping curves like these indicate the groups are not perfectly "
               "separated, so some individuals could belong to either."))

    out.append(wa(
        "G-WA-007", 8, "Reading a correlation matrix",
        "Using the correlation matrix, identify the strongest positive pair and the "
        "strongest negative pair, and say what the values mean.",
        "The strongest positive pair is Hours and Screen at 0.62, meaning that more "
        "screen time goes with more study hours, moderately strongly. The strongest "
        "negative pair is Sleep and Stress at -0.33, meaning more sleep goes with "
        "less stress, but only weakly.",
        [rb("Names Hours and Screen as the strongest positive pair at about 0.62"),
         rb("Names Sleep and Stress as the strongest negative pair at about -0.33"),
         rb("Explains that the signs give direction and the sizes give strength")],
        3, CORR[0], CORR[1], image="corr_heatmap",
        detail="The diagonal is always 1 because every variable is perfectly "
               "correlated with itself, so it is ignored when comparing. Note that "
               "-0.33 and 0.62 are both fairly weak to moderate linear "
               "relationships, and none of these values is close to 1 or -1, which "
               "would look like a tight straight line in a scatter plot."))

    out.append(wa(
        "G-WA-008", 2, "Reading a frequency table",
        "Using the bar chart, state the total number of students, the modal number "
        "of books, and the proportion who read fewer than 20 books.",
        "There are 30 students, since the bars add to 2 + 5 + 11 + 9 + 3. The mode is 20 to 29 books, the tallest bar. Fewer than 20 books is (2 + 5) / 30 = 7/30, about 0.23.",
        [rb("Gives the total as 30"),
         rb("Gives the mode as the 20 to 29 group"),
         rb("Computes the proportion as 7/30")],
        3, FREQ[0], FREQ[1], image="freq_bars",
        detail="The mode is the most frequent value and is read off the tallest bar, "
               "not off the axis. For the proportion, the denominator is the total "
               "across all bars, while the numerator sums only the bars below the "
               "cut-off. A cumulative frequency table answers the same question and "
               "is the more efficient way to do it once the cut-off moves."))

    out.append(wa(
        "G-WA-009", 3, "Shape and spread",
        "Compare the two histograms: do they have the same shape, and which has the "
        "larger variance?",
        "The two histograms have the same shape and the same centre but different "
        "spreads. The more spread-out histogram has the larger variance, because "
        "variance measures average squared distance from the centre and stretching "
        "the same shape over a wider range increases every such distance.",
        [rb("States that the shape is the same in both"),
         rb("Identifies the more spread-out histogram as having the larger variance"),
         rb("Explains variance as distance from the centre")],
        2, SPREAD[0], SPREAD[1], image="hist_symmetric",
        detail="Shape, centre and spread are three separate properties of a "
               "distribution, and two histograms can agree on the first two while "
               "differing on the third. Keeping them apart is the point of "
               "summarising a distribution with several numbers at once."))

    out.append(wa(
        "G-WA-010", 2, "Reading a grouped bar chart",
        "The chart compares how often men and women read a book. Describe the main "
        "difference between the two groups in two or three sentences.",
        "Women report reading less often than men: their bars shrink steadily from the 'Never' category, while the men's peak in the middle. The clearest contrast is at the extremes, where reading often is about twice as common among men. The middle categories are much closer.",
        [rb("Identifies that women report reading less often"),
         rb("Cites the contrast between the extreme categories"),
         rb("Notes that the middle categories are similar")],
        2, STACK[0], STACK[1], image="bar_stacked",
        detail="A grouped bar chart with an ordered categorical variable like this "
               "is best read by looking at the shape of each group's profile rather "
               "than at individual bar heights. Note that this is an association "
               "between two categorical variables, so a comparison of proportions "
               "within each group is more informative than a comparison of raw "
               "counts."))

    out.append(wa(
        "G-WA-011", 5, "Areas under a curve",
        "For the normal curve shown, the shaded regions are marked a, b and c from "
        "left to right. Write P(5 < X < 6.2) in terms of these regions.",
        "P(5 < X < 6.2) is regions a and b added, written P(a) + P(b). Region a covers 5 to 6.2 and b covers 6.2 to 7.4, and the boundary point 6.2 adds no area, so together they are the interval.",
        [rb("Identifies the correct regions as a and b"),
         rb("States the answer as P(a) + P(b) or P(a and b)"),
         rb("Notes that the single boundary point adds no area")],
        2, NORMALQ[0], NORMALQ[1], image="normal_shaded",
        detail="The rule for splitting an interval at an interior point is that "
               "the probabilities of the pieces add up, because the events are "
               "mutually exclusive. A single value has probability zero under a "
               "continuous distribution, which is why the endpoints never cause "
               "trouble. The same logic gives P(X < 6.2) = P(a) + P(b) and "
               "P(X > 7.4) = P(c)."))

    out.append(wa(
        "G-WA-012", 5, "Areas under a curve",
        "Using the same curve, express the probability of the rightmost shaded "
        "region on its own, and say what you would need in order to compute it as a "
        "number.",
        "The rightmost region is P(X > 7.4), written P(c). To compute it you need the mean and standard deviation, so you can standardise 7.4 to a z-score and read the area to its right from the normal table.",
        [rb("Identifies the region as P(X > 7.4) or P(c)"),
         rb("States that the mean and standard deviation are needed"),
         rb("Mentions standardising to a z-score and using the normal table")],
        2, NORMALQ[0], NORMALQ[1], image="normal_shaded",
        detail="A picture tells you which region is meant but not its numerical "
               "value, because the drawing is not drawn to a measurable scale. That "
               "is the whole reason the normal table exists: it stores the area to "
               "the left of each z-score so that any region can be read off after "
               "standardising. The symmetry of the normal distribution also gives "
               "P(c) = P(X < 5) in this figure, since 5 and 7.4 sit equally far from "
               "the centre at 6.2."))

    return out
