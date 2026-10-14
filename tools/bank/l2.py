"""Lecture 2 - Descriptive statistics for categorical data + R fundamentals."""

from .common import mc, rb, wa

PDF = "lecture2.pdf"


def questions():
    out = []

    # ------------------------------------------------------- categorical basics
    out.append(mc(
        "L2-MC-001", 2, "Categorical vs numerical variables",
        "Which of the following variables are CATEGORICAL rather than numerical?",
        ["Number of siblings",
         "Educational level",
         "Height in cm",
         "Whether a person owns a car",
         "Age in years"],
        ["b", "d"],
        "Educational level and car ownership name categories rather than measuring a "
        "quantity. Siblings, height and age all take numeric values that can be "
        "meaningfully compared and averaged.",
        PDF, "p.14"))

    out.append(mc(
        "L2-MC-002", 2, "Frequency tables and proportions",
        "You count 1 'yes' and 3 'no' in a sample. What does "
        "`prop.table(table(x))` return?",
        ["The counts 1 and 3",
         "The proportions 0.25 and 0.75",
         "The percentages 1 and 3",
         "The counts divided by the number of columns",
         "A cumulative distribution"],
        ["b"],
        "`table()` gives counts; `prop.table()` converts them to proportions that sum "
        "to 1, so here 1/4 = 0.25 and 3/4 = 0.75.",
        PDF, "p.29", code="x <- c(\"yes\", \"no\", \"no\", \"no\")\nprop.table(table(x))",
        r_functions=["table", "prop.table"]))

    out.append(mc(
        "L2-MC-003", 2, "Contingency tables",
        "What is the purpose of a contingency table?",
        ["To summarise the mean of a numeric variable",
         "To display the counts of two categorical variables crossed against each other",
         "To compute the variance of a sample",
         "To plot two continuous variables",
         "To store the levels of a factor in a specific order"],
        ["b"],
        "A contingency table crosses two categorical variables so you can see how their "
        "counts co-occur. In R you build one with a two-argument table(), e.g. "
        "`table(x$class, x$survived)`.",
        PDF, "p.30", code="table(titanic_data$class, titanic_data$survived)",
        r_functions=["table"]))

    out.append(mc(
        "L2-MC-004", 2, "Contingency tables",
        "Consider the following R code and its output. What does the call do?",
        ["It computes row proportions for each group",
         "It computes column proportions for each group",
         "It computes overall proportions for each group",
         "It computes the difference in proportions between groups",
         "It computes a chi-squared statistic"],
        ["a"],
        "`prop.table(x, margin = 1)` normalises each row so it sums to 1, giving the "
        "proportions within each group. margin = 2 would instead normalise columns.",
        PDF, "p.31", code="table(titanic_data$class, titanic_data$survived) |>\n  prop.table(margin = 1)",
        r_functions=["table", "prop.table", "|>"]))

    out.append(mc(
        "L2-MC-005", 2, "Visualising categorical data",
        "Which plot is the natural choice for summarising a single categorical "
        "variable?",
        ["A histogram",
         "A bar plot",
         "A scatterplot",
         "A density plot",
         "A box plot"],
        ["b"],
        "Bar plots compare counts or proportions across discrete categories. "
        "Histograms, density plots, scatterplots and box plots are all for numerical "
        "data.",
        PDF, "p.32", r_functions=["geom_bar", "ggplot"]))

    out.append(mc(
        "L2-MC-006", 2, "Visualising categorical data",
        "In a grouped bar plot of two categorical variables, what does `fill =` most "
        "naturally encode?",
        ["The variable whose categories become the different bar colours",
         "The size of the bars",
         "The statistical significance of the comparison",
         "The order of the x-axis",
         "The missing values in the data"],
        ["a"],
        "You map one variable to `aes(x = ...)` for the axis and another to `fill = ...` "
        "so the categories of the second variable become the bar colours.",
        PDF, "p.34",
        code="ggplot(titanic_data, aes(x = class, fill = survived)) +\n  geom_bar()",
        r_functions=["ggplot", "aes", "fill", "geom_bar"]))

    # -------------------------------------------------------------- R functions
    out.append(mc(
        "L2-MC-007", 2, "Anatomy of functions",
        "Consider `calc_percent <- function(x, total) (x / total) * 100`. Which "
        "statements about calling it are TRUE?",
        ["`calc_percent(25, 100)` passes arguments by position",
         "`calc_percent(total = 100, x = 25)` passes arguments by name",
         "The arguments must always be given in the order they are defined",
         "`calc_percent(25)` works because `x` defaults to 25",
         "The function returns 25 in both of the first two calls"],
        ["a", "b", "e"],
        "R allows arguments to be passed positionally or by name, so the first two are "
        "both valid and give the same result of 25. Order is not forced, and `x` has no "
        "default, so the fourth claim is false.",
        PDF, "p.44", code="calc_percent <- function(x, total) (x / total) * 100",
        r_functions=["function", "<-"], origin="adapted_HT25"))

    out.append(mc(
        "L2-MC-008", 2, "Anatomy of functions",
        "Consider `calc_percent_default <- function(x, total = 100) (x / total) * 100`. "
        "What does `calc_percent_default(25)` return?",
        ["An error, because `total` is missing",
         "0.25",
         "25",
         "2500",
         "NA"],
        ["c"],
        "`total = 100` is a default, so it fills in automatically: 25/100 * 100 = 25.",
        PDF, "p.44",
        code="calc_percent_default <- function(x, total = 100) (x / total) * 100\ncalc_percent_default(25)",
        r_functions=["function"]))

    out.append(mc(
        "L2-MC-009", 2, "R functions and packages",
        "What is the difference between the two lines below?",
        ["`install.packages(\"ggplot2\")` downloads and installs the package; "
         "`library(ggplot2)` attaches it for use in the current session.",
         "They are exact synonyms for each other.",
         "`install.packages()` attaches the package; `library()` installs it.",
         "`library()` can only be run once per year.",
         "Neither line is needed if ggplot2 is already installed."],
        ["a"],
        "Installation puts the package on disk so it persists; library() merely makes it "
        "available in the session you are working in, and must be run again in each new "
        "session.",
        PDF, "p.43",
        code="install.packages(\"ggplot2\")\nlibrary(ggplot2)",
        r_functions=["install.packages", "library"]))

    out.append(mc(
        "L2-MC-010", 2, "Subsetting a data.frame",
        "Which of the following are TRUE statements about subsetting?",
        ["`df$age` accesses the single column `age`",
         "`df[1, ]` returns the first row",
         "`df[, 3]` returns the third column",
         "`df[, 3]` returns the third row",
         "`df[4:9, 2]` returns rows 4 to 9 of column 2"],
        ["a", "b", "c", "e"],
        "The first index is the row and the second is the column, so `[, 3]` is a column, "
        "not a row. Only (d) is false.",
        PDF, "p.48", code="titanic_data[1, ]\ntitanic_data[, 3]\ntitanic_data[4:9, 2]",
        r_functions=["[", "$"]))

    out.append(mc(
        "L2-MC-011", 2, "Subsetting a data.frame",
        "Which of the following commands return EXACTLY the value `3`?",
        ["`c(1, 3, 3)[2]`",
         "`c(1, 3, 3)[3]`",
         "`c(1, 3, 3)[c(1, 3, 3) == 3]`",
         "`c(1, 3, 3) == 3`",
         "`c(1, 3, 3)[-1]`"],
        ["a"],
        "`[2]` returns the single element 3. `[3]` also returns 3 but that is not among "
        "the options here, the logical selection returns TWO elements (3 and 3), "
        "`== 3` returns a logical vector, and `[-1]` drops the first element.",
        PDF, "p.49", code="x <- c(1, 3, 3)\nx[2]",
        r_functions=["c", "[", "=="], origin="adapted_HT25"))

    out.append(mc(
        "L2-MC-012", 2, "The pipe operator",
        "What is the main advantage of the pipe `|>`?",
        ["It makes R run faster",
         "It lets you chain operations, passing the result forward, for more readable code",
         "It automatically removes missing values",
         "It is required in order to load a package",
         "It converts a vector into a data.frame"],
        ["b"],
        "The pipe takes the value on its left and passes it as the first argument of the "
        "function on its right, which removes deeply nested parentheses and reads more "
        "like a sequence of steps. It does not change speed, missing values, or data "
        "types.",
        PDF, "p.51",
        code="titanic_data |>\n  arrange(fare) |>\n  head(3)",
        r_functions=["|>"]))

    out.append(mc(
        "L2-MC-013", 2, "The pipe operator",
        "Which of the following statements about the pipe are TRUE?",
        ["The pipe was introduced in R 4.1.0 (2021).",
         "The magrittr pipe `%>%` was the standard before that.",
         "`%>%` can only be used after loading dplyr.",
         "The pipe changes the value being passed, so results differ from nested calls.",
         "Both pipes work in current versions of R."],
        ["a", "b", "e"],
        "The pipe only changes how the call is written, never the result, so (d) is "
        "false. `%>%` comes from the magrittr package, and the grouped "
        "examples do use `dplyr::` prefixes.",
        PDF, "p.51", r_functions=["|>", "%>%"]))

    # --------------------------------------------------------------- dplyr verbs
    out.append(mc(
        "L2-MC-014", 2, "dplyr verbs",
        "You want to keep only rows where `class == \"3rd\"`. Which is the idiomatic "
        "dplyr way?",
        ["`select(titanic_data, class == \"3rd\")`",
         "`titanic_data |> filter(class == \"3rd\")`",
         "`titanic_data |> arrange(class == \"3rd\")`",
         "`titanic_data |> summarise(class == \"3rd\")`",
         "`titanic_data |> mutate(class == \"3rd\")`"],
        ["b"],
        "filter() keeps or drops ROWS. select() chooses columns, arrange() sorts rows, "
        "summarise() collapses the data, and mutate() adds or changes columns.",
        PDF, "p.79",
        code="titanic_data |> dplyr::filter(class == \"3rd\")",
        r_functions=["filter", "|>", "dplyr"]))

    out.append(mc(
        "L2-MC-015", 2, "dplyr verbs",
        "Which statements about these verbs are TRUE?",
        ["`select()` picks out columns",
         "`mutate()` adds or modifies columns",
         "`arrange()` sorts rows",
         "`arrange(desc(fare))` sorts from largest to smallest",
         "`arrange(desc(fare))` sorts from smallest to largest"],
        ["a", "b", "c", "d"],
        "`desc()` requests descending order, so (d) is right and (e) is wrong. A bare "
        "`arrange(fare)` would sort ascending.",
        PDF, "p.109",
        code="titanic_data |>\n  arrange(desc(fare))",
        r_functions=["arrange", "desc", "select", "mutate"]))

    out.append(mc(
        "L2-MC-016", 2, "Grouped operations",
        "Consider the following code. What does it return?",
        ["One mean fare for the whole dataset",
         "One mean fare per class, plus a grouped object",
         "One mean fare per class, ungrouped, in one row",
         "A new column on every row",
         "A contingency table of class by survival"],
        ["b"],
        "`group_by(class) |> summarize(...) |> ungroup()` produces one row per class "
        "AND leaves the result grouped, because `ungroup()` is applied afterwards. "
        "Dropping the trailing `ungroup()` gives the ungrouped one-row-per-class "
        "answer.",
        PDF, "p.134",
        code="titanic_data |>\n  group_by(class) |>\n  summarize(mean_fare = mean(fare, na.rm = TRUE)) |>\n  ungroup()",
        r_functions=["group_by", "summarize", "ungroup", "mean", "na.rm"]))

    out.append(mc(
        "L2-MC-017", 2, "Grouped operations",
        "What is the difference between `.by = class` inside `mutate()` and using "
        "`group_by(class)` first?",
        ["`.by` only works inside summarise(), never mutate()",
         "`.by` performs the grouping for that one call without leaving the result "
         "grouped",
         "`group_by()` is faster than `.by`",
         "`.by` ignores missing values",
         "There is no difference; they are exactly the same"],
        ["b"],
        "`.by` groups only for the duration of that call and returns an ungrouped "
        "object, which avoids the extra ungroup() step and the risk of forgetting it.",
        PDF, "p.139",
        code="titanic_data |>\n  mutate(mean_fare = mean(fare, na.rm = TRUE), .by = class)",
        r_functions=["mutate", ".by", "group_by"]))

    # ------------------------------------------------------ data.frame sense
    out.append(mc(
        "L2-MC-018", 2, "Getting a sense of the data",
        "Which statements about these functions are TRUE?",
        ["`str()` summarises the structure of a data.frame, showing column types",
         "`summary()` gives distributional summaries such as mean and median",
         "`dim()` returns the number of rows and columns",
         "`str()` returns the arithmetic mean of a column",
         "`dim()` returns the column names"],
        ["a", "b", "c"],
        "`str()` shows structure rather than statistics, so (d) is false. `dim()` gives "
        "the two dimensions, and the column names come from `names()` or `colnames()`.",
        PDF, "p.47",
        code="str(titanic_data)\nsummary(titanic_data)\ndim(titanic_data)",
        r_functions=["str", "summary", "dim"]))

    out.append(mc(
        "L2-MC-019", 2, "Factors and ordering",
        "A bar plot of a factor with levels High school, Bachelor, Master, PhD puts the "
        "categories in alphabetical order by default, which puts Bachelor first. What is "
        "the fix?",
        ["Rename the categories so they happen to sort in the intended order",
         "Set the order of the levels explicitly with `factor(levels = ...)`",
         "Use `arrange()` on the plotting data",
         "Convert the factor to character",
         "Use `mutate()` to rename each value"],
        ["b"],
        "ggplot2 sorts a factor by its level order, not alphabetically, so setting the "
        "levels explicitly is the direct fix. The education variable is a "
            "case where this matters.",
        PDF, "p.66", r_functions=["factor", "levels", "ggplot"]))

    out.append(mc(
        "L2-MC-020", 2, "Ordering data",
        "Which R code sorts `titanic_data` by fare from largest to smallest?",
        ["`arrange(titanic_data, fare)`",
         "`titanic_data[order(titanic_data$fare, decreasing = TRUE), ]`",
         "`titanic_data[order(titanic_data$fare), ]`",
         "`select(titanic_data, order(fare))`",
         "`sort(titanic_data$fare)`"],
        ["b"],
        "`order()` returns the positions that would put the values in order, and "
        "`decreasing = TRUE` reverses it. Using the result as a row index returns the "
        "sorted rows. A bare `sort()` returns only the sorted fares, losing every other "
        "column.",
        PDF, "p.89",
        code="titanic_data[order(titanic_data$fare, decreasing = TRUE), ]",
        r_functions=["order", "decreasing", "sort", "arrange"]))

    out.append(mc(
        "L2-MC-021", 2, "Frequency tables",
        "Consider the vector `x <- c(\"a\", \"b\", \"a\", NA)`. What does "
        "`table(x)` return?",
        ["Counts a = 1, b = 1, and NA = 1",
         "Counts a = 2, b = 1, and does not include NA by default",
         "Counts a = 2, b = 1, and includes NA = 1",
         "Returns the proportions directly",
         "Returns an error because of the missing value"],
        ["b"],
        "`table()` ignores missing values unless you ask for them with "
        "`useNA = \"ifany\"`. So a = 2 and b = 1, and the NA is silently dropped.",
        PDF, "p.28", code="x <- c(\"a\", \"b\", \"a\", NA)\ntable(x)",
        r_functions=["table", "NA"]))

    out.append(mc(
        "L2-MC-022", 2, "Elements of a graph",
        "Which statements about graphs are TRUE?",
        ["A graph's title states what is being shown",
         "The x-axis and y-axis name the variables and their units",
         "A legend explains what colours or shapes mean",
         "A graph should never include a source note",
         "Axis labels should be omitted when the variable names are obvious"],
        ["a", "b", "c"],
        "Title, labelled axes with units, and a legend are the standard elements to "
            "include. Citing the source is good practice rather than something to "
        "omit, so (d) is false; and omitting axis labels is never right.",
        PDF, "p.37"))

    # ------------------------------------------------------------ written answers
    out.append(wa(
        "L2-WA-001", 2, "Frequency tables and proportions",
        "Write the R code that counts how many observations fall in each of the "
        "`class` categories of `titanic_data`, and then converts those counts to "
        "proportions. No need to give the numerical output.",
        "```r\ntable(titanic_data$class) |>\n  prop.table()\n```\n`table()` produces "
        "the counts and `prop.table()` divides them by the total so they sum to 1.",
        [rb("`table()` used to get the counts"),
         rb("`prop.table()` applied to convert to proportions")],
        1, PDF, "p.29",
        code="table(titanic_data$class) |> prop.table()",
        r_functions=["table", "prop.table", "|>", "$"]))

    out.append(wa(
        "L2-WA-002", 2, "Contingency tables",
        "Write the R code that produces a two-way table of `class` by `survived`, and "
        "then shows the proportion within each class.",
        "```r\ntable(titanic_data$class, titanic_data$survived) |>\n  prop.table(margin = "
        "1)\n```\nA two-argument `table()` builds the contingency table, and "
        "`margin = 1` normalises within each row so each class sums to 1.",
        [rb("Two-argument `table()` used to cross the two variables"),
         rb("`prop.table(margin = 1)` used for within-class proportions")],
        1, PDF, "p.31",
        code="table(titanic_data$class, titanic_data$survived) |> prop.table(margin = 1)",
        r_functions=["table", "prop.table", "margin"]))

    out.append(wa(
        "L2-WA-003", 2, "Grouped operations",
        "Write the R code that computes the mean fare for each passenger class using "
        "dplyr.",
        "```r\ntitanic_data |>\n  group_by(class) |>\n  summarize(mean_fare = mean(fare, "
        "na.rm = TRUE))\n```\n`group_by()` splits the data by class, `summarize()` "
        "computes the mean within each group, and `na.rm = TRUE` drops missing fares.",
        [rb("`group_by(class)` used to split by class"),
         rb("`summarize()` with `mean(fare, na.rm = TRUE)` used for the mean"),
         rb("Pipe used to chain the steps")],
        1, PDF, "p.134",
        code="titanic_data |>\n  group_by(class) |>\n  summarize(mean_fare = mean(fare, na.rm = TRUE))",
        r_functions=["group_by", "summarize", "mean", "na.rm", "|>"]))

    out.append(wa(
        "L2-WA-004", 2, "The pipe operator",
        "Explain what the pipe operator `|>` does, and why it arrived in R 4.1.0 rather "
        "than being available from the start.",
        "The pipe passes the value on its left in as the first argument of the call on its right, so operations chain as steps rather than nested parentheses. Before R 4.1.0 it came only from the magrittr package as `%>%`.",
        [rb("Describes passing the left value as the first argument of the right call", 2),
         rb("Mentions readability / avoiding nested calls", 2),
         rb("Notes R 4.1.0 (2021) and the magrittr `%>%` predecessor", 2)],
        1, PDF, "p.51", r_functions=["|>", "%>%"],
        detail="The native pipe is slightly faster and needs no library call, which is "
               "why it works in a fresh R session without loading anything. The two "
               "operators are near-interchangeable for this purpose, so reading older "
               "code with `%>%` is not a sign of an old R version."))

    out.append(wa(
        "L2-WA-005", 2, "Anatomy of functions",
        "Explain the difference between passing an argument by position and by name, and "
        "say how a default value is set.",
        "Positional matching assigns arguments in the order of the function definition. Named matching writes `name = value` and stays correct if the definition order changes. A default is set with an equals sign in the definition, as in `function(x, total = 100)`.",
        [rb("Position explained as order-based assignment", 2),
         rb("Name explained as explicit `name = value`", 2),
         rb("Default explained as `arg = value` in the definition", 2)],
        1, PDF, "p.44",
        code="calc_percent <- function(x, total = 100) (x / total) * 100",
        r_functions=["function", "<-"],
        detail="Partial matching is allowed but deprecated, so naming arguments in full "
               "is the safer habit. Arguments are also matched lazily in R, which is "
               "why the order of evaluation can produce surprises when defaults refer "
               "to other arguments."))

    out.append(wa(
        "L2-WA-006", 2, "Subsetting a data.frame",
        "Give three ways to select rows of `titanic_data` where `class == \"3rd\"` and "
        "`survived == \"yes\"`, and say which dplyr verb is preferred.",
        "Base R indexing: "
        "`titanic_data[titanic_data$class == \"3rd\" & titanic_data$survived == "
        "\"yes\", ]`. The `subset()` function: `subset(titanic_data, class =="
        "\"3rd\" & survived == \"yes\")`. The preferred dplyr version is "
        "`titanic_data |> dplyr::filter(class == \"3rd\" & survived == \"yes\")`.",
        [rb("Base R logical indexing given"),
         rb("`subset()` given"),
         rb("`dplyr::filter()` given and identified as preferred")],
        1, PDF, "p.77",
        code="titanic_data |> dplyr::filter(class == \"3rd\" & survived == \"yes\")",
        r_functions=["filter", "subset", "|>", "&", "$"],
        detail="All three return the same rows, but only `filter()` returns a data "
               "frame directly. Base R indexing is the easiest to get wrong, because "
               "forgetting the trailing comma drops the column selection and can return "
               "a vector instead of a table. `filter()` also handles missing values by "
               "dropping rows where the condition is NA, which is usually what you "
               "want but is worth knowing."))

    out.append(wa(
        "L2-WA-007", 2, "Visualising categorical data",
        "Write the R code for a grouped bar plot showing the count of passengers in each "
        "class, split by whether they survived.",
        "```r\nggplot(titanic_data, aes(x = class, fill = survived)) +\n  geom_bar()\n```"
        "\n`class` goes on the x-axis and `survived` is mapped to `fill` so the bars are "
        "split and coloured by survival.",
        [rb("`ggplot()` call mapping `x = class`"),
         rb("`fill = survived` used to split and colour the bars"),
         rb("`geom_bar()` layer added")],
        1, PDF, "p.34",
        code="ggplot(titanic_data, aes(x = class, fill = survived)) +\n  geom_bar()",
        r_functions=["ggplot", "aes", "fill", "geom_bar"],
        detail="Mapping to `fill` rather than to `position` is what produces side-by-"
               "side bars, because `geom_bar()` defaults to a stacked position. Add "
               "`position = \"dodge\"` to the `geom_bar()` call to make that explicit. "
               "Because the default stack normalises to proportions, you should be "
               "careful comparing bar heights when the group sizes differ."))

    out.append(wa(
        "L2-WA-008", 2, "Grouped operations",
        "Explain the difference between `group_by(class) |> summarize(...) |> ungroup()` "
        "and `summarize(..., .by = class)`, and say which is the modern alternative.",
        "With `group_by()` the grouped state persists across later calls, so `ungroup()` is needed or downstream operations stay grouped. With `.by = class` the grouping applies only inside that one call and the result comes back ungrouped, which is why `.by` is the modern alternative.",
        [rb("`group_by()` state persists and needs explicit `ungroup()`", 2),
         rb("`.by` scopes grouping to one call and returns ungrouped", 2),
         rb("`.by` correctly identified as the modern alternative")],
        1, PDF, "p.139",
        code="titanic_data |>\n  summarize(mean_fare = mean(fare, na.rm = TRUE), .by = class)",
        r_functions=[".by", "group_by", "ungroup", "summarize"],
        detail="A forgotten `ungroup()` is a common source of confusing output, because "
               "later `mutate()` or `arrange()` calls then operate per group without "
               "warning. `.by` removes the failure mode entirely at the cost of not "
               "supporting the more elaborate grouped operations. Both give the same "
               "numbers for this question."))

    return out