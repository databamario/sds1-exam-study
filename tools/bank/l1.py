"""Lecture 1 - What is statistics? + R basics."""

from .common import mc, rb, wa

PDF = "lecture1.pdf"


def questions():
    out = []

    # ---------------------------------------------------- descriptive/inferential
    out.append(mc(
        "L1-MC-001", 1, "Descriptive vs inferential statistics",
        "A study surveys 1,500 adults about pet ownership and stress. Among cat "
        "owners the average stress score is 2.5; among non-owners it is 3.0. Which "
        "statement is an INFERENTIAL claim?",
        ["In our sample, cat owners reported 20% lower stress than non-cat owners.",
         "Cat ownership is associated with a 20% reduction in stress among all adults.",
         "The sample contained 1,500 adults.",
         "The mean stress of cat owners was 2.5.",
         "The box plot of stress scores had two groups."],
        ["b"],
        "Descriptive statements stay inside the sample we observed. The inferential "
        "statement generalises to the broader adult population, which is the whole "
        "point of moving from the sample to the population.",
        PDF, "p.7"))

    out.append(mc(
        "L1-MC-002", 1, "Descriptive vs inferential statistics",
        "Which of the following are examples of INFERENTIAL statistics rather than "
        "descriptive statistics?",
        ["Computing the median income of the survey respondents.",
         "Performing a hypothesis test comparing a sample mean to a known population mean.",
         "Creating a box plot of test scores.",
         "Estimating the population proportion using sample data.",
         "Computing the standard deviation of a sample."],
        ["b", "d"],
        "Inferential statistics generalise from a sample to a population: hypothesis "
        "testing (b) and estimating a population proportion (d). The others only "
        "summarise the data at hand.",
        PDF, "p.5", origin="adapted_HT25"))

    out.append(mc(
        "L1-MC-003", 1, "Sources of uncertainty",
        "Uncertainty in a conclusion can come from several "
        "places. Which of the following are listed as sources of uncertainty?",
        ["An incorrect sampling strategy.",
         "An incorrect measurement of stress.",
         "A small sample size.",
         "The use of decimals in the dataset.",
         "Choosing to report a median instead of a mode."],
        ["a", "b", "c"],
        "The three sources named are an incorrect sampling strategy, incorrect "
        "measurement, and small sample size. Cosmetic reporting choices do not "
        "themselves create uncertainty about the population.",
        PDF, "p.9"))

    # ------------------------------------------------------------- Literary Digest
    out.append(mc(
        "L1-MC-004", 1, "Sampling bias",
        "In the 1936 Literary Digest poll, 2.4 million people were surveyed and "
        "Landon was predicted to win with 57% of the vote. Roosevelt actually won "
        "with 62%. Why did such a large poll fail?",
        ["The sample size was too small to be reliable.",
         "The magazine polled its subscribers and car owners, who during the Great "
         "Depression were mostly wealthy Republicans.",
         "The poll was conducted before the election was decided.",
         "The responses were counted incorrectly by the magazine.",
         "The poll used a random sampling method, which is unsuitable for elections."],
        ["b"],
        "The poll was enormous but biased: it surveyed the magazine's own subscribers "
        "and car owners, who were disproportionately wealthy Republicans. The lesson "
        "is explicit: a large sample size does not fix a biased "
        "sampling strategy.",
        PDF, "p.25"))

    out.append(mc(
        "L1-MC-005", 1, "Sampling bias",
        "Which statement about sample size and sampling bias is true?",
        ["A large sample size can compensate for a biased sampling strategy.",
         "A large sample size guarantees the sample is representative.",
         "A large sample size reduces random error but does not fix a biased "
         "sampling strategy.",
         "Sample size is irrelevant whenever probability sampling is used.",
         "Bias can only occur when the sample is smaller than the population."],
        ["c"],
        "Sample size reduces random error, i.e. sampling variability. It cannot "
        "repair a systematically unrepresentative sampling frame. The Literary "
        "Digest poll is exactly this kind of example.",
        PDF, "p.25"))

    # ------------------------------------------------------ target/sampled/sample
    out.append(mc(
        "L1-MC-006", 1, "Study design terminology",
        "A researcher wants to say something about elderly women living in Sweden "
        "but ends up sampling only women living in elderly care facilities. Which "
        "statement is correct?",
        ["The target population and the sampled population are different groups.",
         "The sampled population is a subset of the sample.",
         "The sample is the full group the researcher wants to generalise to.",
         "The observation unit is the elderly care facility.",
         "Target and sampled populations are identical unless the sample is random."],
        ["a"],
        "The target population is everyone you want to say something about (elderly "
        "women in Sweden); the sampled population is the group you could actually "
        "reach (those in care facilities). They are ideally the same but often are "
        "not, because some individuals are unreachable.",
        PDF, "p.26"))

    out.append(mc(
        "L1-MC-007", 1, "Study design terminology",
        "Which of the following are TRUE statements about study design terminology?",
        ["The observation unit is the unit you actually study.",
         "In the CSS programme the observation unit is most often the individual.",
         "The sampled population is always larger than the sample.",
         "A sample is the full group you want to make claims about.",
         "The target population and the sampled population may differ when some "
         "individuals are unreachable."],
        ["a", "b", "e"],
        "The observation unit is what you study (usually individuals); target and "
        "sampled populations can diverge because some people are unreachable; and "
        "the sample is by definition a subset of the sampled population, so it is "
        "smaller, not larger. A sample is never the full target group.",
        PDF, "p.26"))

    out.append(mc(
        "L1-MC-008", 1, "Study design terminology",
        "A Ph.D. student draws a lottery among ALL Ph.D. students at LiU and "
        "randomly selects 10. Which statement is correct?",
        ["The target population is not equal to the sampled population here.",
         "This is a random sample because each student has an equal chance of selection.",
         "This introduces sampling bias because 10 is a small number.",
         "The observation unit is the department rather than the student.",
         "This is a convenience sample because the student chose the number 10."],
        ["b"],
        "A lottery over the complete list is random sampling, and the target and "
        "sampled populations coincide. Small n causes imprecision, not bias. Choosing "
        "n = 10 in advance is not what makes a sample a convenience sample.",
        PDF, "p.28"))

    out.append(mc(
        "L1-MC-009", 1, "Study design terminology",
        "A Ph.D. student is asked to recruit respondents for a study of how long a "
        "Ph.D. at LiU takes, and chooses their friends and department colleagues. "
        "Which statement is correct?",
        ["The target population equals the sampled population in this design.",
         "This is a random sample because the student chose the participants personally.",
         "The target population is not equal to the sampled population, and sampling "
         "bias has been introduced.",
         "The only problem is the small sample size, not who was selected.",
         "The observation unit becomes the department rather than the individual."],
        ["c"],
        "Picking your own friends and colleagues produces a non-representative "
        "sample and breaks the link between the sampled population and the target "
        "population. Bias in sampling leads to incorrect conclusions about the "
        "population.",
        PDF, "p.29"))

    # --------------------------------------------------------------- R: objects
    out.append(mc(
        "L1-MC-010", 1, "R objects and assignment",
        "Consider the following R code. What is the value of `a` after the code runs?",
        ["2 + 2",
         "4",
         "Hello",
         "World",
         "The code produces an error, because a is a reserved word."],
        ["b"],
        "R evaluates the right-hand side and stores the result. `a <- 2 + 2` stores 4 "
        "in a, so printing `a` gives 4.",
        PDF, "p.41", code="a <- 2 + 2\na", r_functions=["<-", "+"]))

    out.append(mc(
        "L1-MC-011", 1, "R objects and assignment",
        "Consider the following R code. What is printed?",
        ["Hello",
         "World",
         "Hello World",
         "An error, because a is overwritten",
         "Nothing, because assignment does not print"],
        ["b"],
        "The second assignment replaces the contents of `a`. Assignment overwrites "
        "without warning, so the object ends up holding \"World\".",
        PDF, "p.41", code="a <- \"Hello\"\na <- \"World\"\na",
        r_functions=["<-"], origin="adapted_HT25"))

    out.append(mc(
        "L1-MC-012", 1, "R objects and functions",
        "Consider the following R code. What is printed?",
        ["10",
         "4",
         "6",
         "2 4 6 8",
         "An error, because a and b are numbers not vectors"],
        ["a"],
        "`d * 2` recycles the scalar 2 across the vector, giving 2 4 6 8, while "
        "`a + b` is arithmetic on two single stored values, 4 + 6 = 10.",
        PDF, "p.42", code="a <- 2 + 2\nb <- 3 * 2\na + b",
        r_functions=["<-", "+", "*"]))

    out.append(mc(
        "L1-MC-013", 1, "R objects and functions",
        "Consider the following R code. What is printed by the last line?",
        ["4",
         "2.5",
         "3",
         "10",
         "An error, because var() needs a data.frame"],
        ["a"],
        "`mean(c(2,3,4,5,6))` is 20/5 = 4. Note that `var()` on the same vector is "
        "2.5, which is a common trap in this kind of question.",
        PDF, "p.43", code="numbers <- c(2, 3, 4, 5, 6)\nmean(numbers)",
        r_functions=["c", "mean"]))

    out.append(mc(
        "L1-MC-014", 1, "R data types",
        "Which of the following statements about R data types are TRUE?",
        ["`x <- 2L` creates an integer, because the L suffix forces integer type.",
         "`x <- 3.14` creates a numeric value.",
         "`x <- \"hello\"` creates a character vector.",
         "`x <- TRUE` creates a logical vector.",
         "`x <- 2L` creates a numeric value, because integers are a subset of numerics."],
        ["a", "b", "c", "d"],
        "The L suffix explicitly forces integer type, so (e) is false even though R "
        "will happily do arithmetic with integers. All of (a) to (d) are true.",
        PDF, "p.52", code="x <- 2L\nclass(x)",
        r_functions=["<-", "class"]))

    out.append(mc(
        "L1-MC-015", 1, "R data structures",
        "Which of the following statements about R data structures are TRUE?",
        ["A vector is a one-dimensional list of elements of the same data type.",
         "A matrix is a two-dimensional list of elements of the same data type.",
         "A data frame is a two-dimensional list of vectors that may have different types.",
         "A list may contain elements of different types.",
         "A data frame can only contain numeric columns."],
        ["a", "b", "c", "e"],
        "A vector is a one-dimensional list of elements of the same data type. A matrix "
        "is a two-dimensional list of elements of the same data type. A data frame is a "
        "two-dimensional list of vectors that may have different types. A list may contain "
        "elements of different types. Only (e) is false.",
        PDF, "p.50", r_functions=["data.frame", "c", "matrix", "list", "factor"]))

    out.append(mc(
        "L1-MC-019", 1, "Defining functions in R",
        "Consider the following R code. What does `f(3)` return?",
        ["6",
         "9",
         "3",
         "An error, because f is not a built-in function",
         "The function definition itself"],
        ["b"],
        "The assignment stores a function in `f`, so calling it applies `x^2` to the "
        "argument. Note that the right-hand side is evaluated before the assignment, so "
        "`f` exists as a function object only after that line runs.",
        PDF, "p.43", code="f <- function(x) x^2\nf(3)",
        r_functions=["function", "<-", "^"]))

    out.append(mc(
        "L1-MC-016", 1, "R data structures",
        "Consider the output below from R. Which statements are true?",
        ["The output is a data.frame with two elements.",
         "The first element is a character vector.",
         "The second element is a character vector.",
         "The output is a matrix with two rows.",
         "The output is a list with two elements."],
        ["c", "e"],
        "The [[1]] / [[2]] indexing is the signature of a list, and the elements have "
        "different types, which is exactly what distinguishes a list from a matrix or "
        "a data frame column set. The first element 1 2 3 is numeric, not character.",
        PDF, "p.51", code="l <- list(1:3, c(\"a\",\"b\",\"c\"))\nl",
        r_functions=["list"], origin="adapted_HT25"))

    out.append(mc(
        "L1-MC-017", 1, "R syntax",
        "Which of the following are TRUE statements about R syntax?",
        ["R is case sensitive, so A is not the same as a.",
         "Anything after the hash symbol (#) is ignored by R.",
         "A series of commands can be grouped using braces { }.",
         "R commands can never be separated by a semicolon.",
         "The > prompt indicates where you type commands in the console."],
        ["a", "b", "c", "e"],
        "Commands are generally separated by a new line but a semicolon can also be "
        "used, although a semicolon is rarely needed. That makes (d) false.",
        PDF, "p.44"))

    out.append(mc(
        "L1-MC-018", 1, "R objects and functions",
        "You want a factor with the levels in the order Low, Medium, High. Which R "
        "code is correct?",
        ["factor(x, levels = c(\"Low\", \"Medium\", \"High\"))",
         "factor(x) - it always sorts alphabetically, which is what we want",
         "levels(x) = c(\"Low\", \"Medium\", \"High\")",
         "as.character(x) <- c(\"Low\", \"Medium\", \"High\")",
         "sort(x, levels = c(\"Low\", \"Medium\", \"High\"))"],
        ["a"],
        "You set the level order by passing `levels` to `factor()`. Bare `factor(x)` "
        "takes the levels in alphabetical order, which would give High, Low, Medium.",
        PDF, "p.46", r_functions=["factor", "levels"]))

    # -------------------------------------------------------------- written answers
    out.append(wa(
        "L1-WA-001", 1, "Study design terminology",
        "A survey draws 50 adults aged 20-64 from each of 5 urban districts, using the "
        "national population register, and 2,150 people respond. Identify the target "
        "population, the sampled population, the sample and the observation unit.",
        "Target population: all Swedish adults aged 20-64. Sampled population: the "
        "register-listed adults aged 20-64 that were drawn from. Sample: the 2,150 "
        "responders. Observation unit: the individual adult.",
        [rb("Target population identified as all Swedish adults aged 20-64"),
         rb("Sampled population identified as the register-based group that could "
            "actually be drawn from"),
         rb("Sample identified as the 2,150 responders"),
         rb("Observation unit identified as the individual person")],
        2, PDF, "p.26",
        origin="adapted_HT25",
        detail="The distinction that trips people up is between the sampled population "
               "and the sample. The sampled population is the group the sampling frame "
               "could have reached, and the sample is the subset that actually took "
               "part. Non-response is what separates them here: 2,150 is the sample, "
               "while everyone reachable through the register is the sampled "
               "population."))

    out.append(wa(
        "L1-WA-002", 1, "R data structures",
        "Explain how a vector, a matrix, a data frame and a list differ in R.",
        "A vector is one-dimensional with a single type, made with `c()`. A matrix is the two-dimensional version and still holds one type. A data frame is two-dimensional but its columns may differ in type, and a list may hold elements of differing types.",
        [rb("Vector described as 1-dimensional, single type, made with c()", 2),
         rb("Matrix described as 2-dimensional, still single type", 2),
         rb("Data frame described as 2-dimensional columns that may differ in type", 2),
         rb("List described as a collection whose elements may differ in type", 2)],
        1, PDF, "p.48",
        detail="The single-type rule is what separates the first two from the last "
               "two. A matrix is essentially a vector with a `dim` attribute, so it "
               "inherits the restriction that everything inside must share a type. A "
               "data frame drops that restriction by treating each column as its own "
               "vector, which is why a data frame can hold a numeric column next to a "
               "character one. The list is the most permissive of the four."))

    out.append(wa(
        "L1-WA-003", 1, "R data types",
        "R has six data types. Name the four that matter for this exam and give one "
        "example value of each.",
        "Numeric (3.14), integer (2L), logical (TRUE or NA) and character (\"SDS1\"). "
        "The two types not used here are complex and raw.",
        [rb("Numeric and integer both named"),
         rb("Logical and character both named"),
         rb("Complex and raw correctly identified as the excluded types")],
        1, PDF, "p.46",
        detail="`numeric` and `integer` are stored the same way but behave differently "
               "in arithmetic: `1/2` gives 0.5 but `1L/2L` gives 0, which is why a "
               "count read from a file often needs `as.numeric()`. Logical values can "
               "hold TRUE, FALSE or NA. Complex numbers and raw vectors exist in R but "
               "do not appear in this material."))

    out.append(wa(
        "L1-WA-004", 1, "R syntax",
        "Explain what happens to the text after a hash symbol (#) in an R script, and "
        "why you would use it.",
        "R ignores everything after the hash symbol and never runs it, so it is a "
        "comment. Comments annotate code so a reader can follow the logic.",
        [rb("Text after # is ignored / not executed"),
         rb("Purpose given as documenting or annotating code")],
        1, PDF, "p.44",
        detail="A `#` inside a quoted string is not a comment, because R only treats "
               "it as one outside of strings. This is why a variable holding a colour "
               "like \"#FF0000\" still works."))

    out.append(wa(
        "L1-WA-005", 1, "R objects and functions",
        "Explain why `x <- x + 1` does not change the original `x`, and what `<-` does "
        "when the name already exists.",
        "The right-hand side is evaluated first and the result is then assigned to the "
        "name on the left, so the original value survives until the assignment "
        "completes. When the name already exists, `<-` overwrites the previous contents "
        "without warning.",
        [rb("Right-hand side evaluated first, then assigned"),
         rb("`<-` overwrites an existing object without warning")],
        1, PDF, "p.41", code="x <- 5\nx <- x + 1",
        r_functions=["<-"],
        detail="Because the overwrite is silent, reusing a common name like `a` for an "
               "unrelated object is a frequent source of confusion later. A function "
               "body is evaluated in its own environment, so assigning `x` inside a "
               "function does not change the `x` in the global environment."))

    out.append(wa(
        "L1-WA-006", 1, "R objects and functions",
        "Write the R code that creates a vector containing the values 1, 2, 3, 4, and "
        "then doubles every element of it. No need to give the final printed result.",
        "```r\nd <- c(1, 2, 3, 4)\nd * 2\n```\nThe scalar 2 is recycled across the "
        "vector, giving 2 4 6 8.",
        [rb("Vector created with c(1, 2, 3, 4)"),
         rb("Doubling performed by multiplying the vector by 2")],
        1, PDF, "p.42", code="d <- c(1, 2, 3, 4)\nd * 2",
        r_functions=["c", "*"],
        detail="Recycling is what lets a single-element vector combine with a longer "
               "one: R repeats the shorter operand until it matches the longer. The "
               "same rule applies to `/` and `+`, which is why `1:5 - 1` subtracts one "
               "from every element."))

    out.append(wa(
        "L1-WA-007", 1, "Factors",
        "A factor stores integers with labels attached. Explain what that means in "
        "practice, and why it matters when you need a specific order of categories.",
        "The integer codes are not meaningful on their own, so the labels and the order "
        "of the levels carry the information. Level order controls sorting and "
        "plotting, so categories appear in the order of their levels rather than "
        "alphabetically.",
        [rb("Explanation that storage is integer codes plus a label mapping", 2),
         rb("Levels control ordering, so order must sometimes be set explicitly", 2)],
        1, PDF, "p.52",
        detail="A frequent symptom of this is a bar chart whose categories come out in "
               "the wrong order, with \"High\" before \"Low\". Setting the levels with "
               "`factor(x, levels = c(\"Low\", \"Medium\", \"High\"), ordered = TRUE)` "
               "fixes both the plot and any subsequent arithmetic. The distinction "
               "between a factor's stored codes and its printed labels is also why "
               "`mean(x)` fails on a factor: the codes are meaningless as numbers."))

    out.append(wa(
        "L1-WA-008", 1, "Sampling bias",
        "Explain why a very large sample does not guarantee a correct conclusion, using "
        "the Literary Digest poll as an example.",
        "A large sample reduces random error but cannot repair a biased sampling "
        "strategy. Literary Digest polled 2.4 million people but only its subscribers "
        "and car owners, who were mostly wealthy Republicans, so it predicted Landon at "
        "57% while Roosevelt won with 62%.",
        [rb("Large sample reduces random error but not bias"),
         rb("Literary Digest mechanism described: subscribers and car owners"),
         rb("Correct consequence given: wrong prediction despite huge n")],
        1, PDF, "p.25",
        detail="The distinction is between random error and bias. Random error shrinks "
               "as the sample grows, roughly with the square root of n, so it is fixed "
               "by collecting more. Bias comes from how units were chosen and does not "
               "shrink at all: a frame of car owners stays unrepresentative no matter "
               "how many of them answer. Precision is not the same thing as being "
               "right, and this poll had extreme precision and was still wrong."))

    return out