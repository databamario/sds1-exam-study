"""Lecture 4 - Probability and sampling theory."""

from .common import mc, rb, wa

PDF = "lecture4_after.pdf"


def questions():
    out = []

    out.append(mc(
        "L4-MC-001", 4, "Basic probability",
        "Which statements about a probability are TRUE?",
        ["P(A) can never be negative.",
         "P(A) = 0 means event A will never happen.",
         "P(A) = 1 means event A will always happen.",
         "P(A) can be greater than 1 if an event is very likely.",
         "P(A) must be expressed as a percentage, not a decimal."],
        ["a", "b", "c"],
        "A probability lies between 0 and 1, so it can be written as a decimal such as "
        "0.5 or as the equivalent 50%. It cannot exceed 1 however likely the event is.",
        PDF, "p.11"))

    out.append(mc(
        "L4-MC-002", 4, "Disjoint and joint events",
        "Drawing a red card and drawing a black card from a single draw. How are these "
        "events related?",
        ["Joint, because both are possible in a deck",
         "Disjoint, because they cannot happen at the same time",
         "Independent, because colour is unrelated to the draw",
         "Complementary, because they cover the sample space",
         "Equally likely"],
        ["b"],
        "They are disjoint (mutually exclusive) since one card cannot be both red and "
        "black, so the probability of the intersection is 0. They are not complementary, "
        "because they do not cover the whole sample space - there are also face cards "
        "that are neither.",
        PDF, "p.14"))

    out.append(mc(
        "L4-MC-003", 4, "Disjoint and joint events",
        "Which pairs of events are DISJOINT?",
        ["A student fails the class and a student gets an A",
         "Drawing a red card and drawing a queen",
         "It rains on Monday and it rains on Tuesday",
         "A person is a smoker and a person is a non-smoker",
         "Drawing a heart and drawing a king"],
        ["a", "d"],
        "Failing and getting an A cannot both happen to one student, and a person cannot "
        "both smoke and not smoke, so those pairs are mutually exclusive. Red and queen "
        "can coincide, as can rain on two different days.",
        PDF, "p.15"))

    out.append(mc(
        "L4-MC-004", 4, "Complementary events",
        "Why is P(red or black) = 26/52 + 26/52 = 1 for a shuffled deck?",
        ["Because the two events are independent",
         "Because the two events are complementary: they are disjoint and together cover "
         "the whole sample space",
         "Because every card has probability 1",
         "Because red and black are joint events",
         "Because the deck has 52 equally likely cards"],
        ["b"],
        "Red and black are disjoint and their union is the entire deck, so they are "
        "complements. For disjoint events the addition rule reduces to simple addition, "
        "which is why the probabilities sum to exactly 1.",
        PDF, "p.17"))

    out.append(mc(
        "L4-MC-005", 4, "Addition rule",
        "What is the general addition rule for any two events A and B?",
        ["P(A and B) = P(A) x P(B)",
         "P(A or B) = P(A) + P(B) - P(A and B)",
         "P(A or B) = P(A) + P(B)",
         "P(A) = P(A or B) - P(B)",
         "P(A or B) = 1 - P(A and B)"],
        ["b"],
        "The subtraction of the intersection is required whenever A and B are not "
        "disjoint, because the overlapping cases would otherwise be counted twice. For "
        "disjoint events the intersection is 0 and the rule collapses to (c).",
        PDF, "p.22", origin="adapted_HT25"))

    out.append(mc(
        "L4-MC-006", 4, "Addition rule",
        "What is the probability of drawing a red jack or a black queen from a shuffled "
        "52-card deck?",
        ["4/52",
         "8/52",
         "6/52",
         "9/52",
         "It cannot be computed without knowing the deck order"],
        ["b"],
        "There are 4 red jacks and 4 black queens, and no card is both, so the events are "
        "disjoint and the probability is 4/52 + 4/52 = 8/52.",
        PDF, "p.20"))

    out.append(mc(
        "L4-MC-007", 4, "Conditional probability",
        "Which statement correctly defines a conditional probability?",
        ["P(A and B) / P(B)",
         "P(A) / P(B)",
         "P(A and B) x P(B)",
         "P(A) - P(B)",
         "P(B) / P(A and B)"],
        ["a"],
        "A conditional probability P(A|B) restricts the sample space to B, so it is the "
        "joint probability divided by P(B). Swapping numerator and denominator would "
        "instead give the reverse conditional probability.",
        PDF, "p.25"))

    out.append(mc(
        "L4-MC-008", 4, "Conditional probability",
        "In the MTO experiment, 72 teenagers were followed and 24 were enrolled in "
        "college. What is P(enrolled)?",
        ["14/24",
         "24/72",
         "48/72",
         "14/72",
         "24/48"],
        ["b"],
        "The marginal probability of enrolment is the column total over the grand total, "
        "24/72. Note this is different from P(enrolled | low-poverty voucher), which "
        "conditions on the row.",
        PDF, "p.40", r_functions=["table", "prop.table"], origin="adapted_HT25"))

    out.append(mc(
        "L4-MC-009", 4, "Conditional probability",
        "In the MTO experiment, what is P(enrolled | low-poverty voucher)?",
        ["24/72",
         "14/24",
         "14/72",
         "10/24",
         "48/72"],
        ["b"],
        "Conditioning on the voucher restricts to the 24 teenagers who received one, of "
        "whom 14 enrolled, giving 14/24. This is the ratio (14/72)/(24/72), "
        "which simplifies to 14/24.",
        PDF, "p.43", origin="adapted_HT25"))

    out.append(mc(
        "L4-MC-010", 4, "Independence",
        "The probability of walking to school is 0.30 overall, 0.50 for 9th graders and "
        "0.10 for 12th graders. What does this show?",
        ["Walking to school and grade level are independent",
         "Walking to school and grade level are dependent",
         "Walking to school has probability 0.50",
         "Grade level is a binary variable",
         "The three probabilities must sum to 1"],
        ["b"],
        "For independence the probability of walking would be the same whether or not B "
        "occurs. Since 0.50 and 0.10 differ from each other and from the overall 0.30, "
        "knowing the grade level changes the probability, so the variables are dependent.",
        PDF, "p.29"))

    out.append(mc(
        "L4-MC-011", 4, "Independence",
        "Which statements are TRUE?",
        ["Tossing a coin twice gives independent outcomes.",
         "Drawing two cards without replacement gives independent outcomes.",
         "P(A) = P(A|B) = P(A|Bc) is the condition for independence.",
         "For independent events, P(A and B) = P(A) x P(B).",
         "Two events are independent whenever they are disjoint."],
        ["a", "c", "d"],
        "Drawing without replacement makes the second draw depend on the first, so (b) "
        "is false. Disjointness does not imply independence: for a fair coin the two "
        "tosses are independent yet the two heads/tails events are disjoint, whereas two "
        "disjoint events in an asymmetric deck can still be dependent. So (e) is false.",
        PDF, "p.30"))

    out.append(mc(
        "L4-MC-012", 4, "Sampling with and without replacement",
        "A bag holds 5 red, 3 blue and 2 orange balls. You draw a blue ball first and do "
        "NOT replace it. What is the probability of drawing a blue ball second?",
        ["3/10",
         "2/9",
         "2/10",
         "1/10",
         "9/100"],
        ["b"],
        "With one blue removed there are 2 blue left out of 9 balls total, giving 2/9, "
        "which is not equal to the first-draw probability of 3/10. That inequality is "
        "precisely why draws without replacement are dependent.",
        PDF, "p.37", origin="adapted_HT25"))

    out.append(mc(
        "L4-MC-013", 4, "Sampling with and without replacement",
        "Which statements about sampling are TRUE?",
        ["Sampling with replacement keeps the draws independent.",
         "Sampling without replacement makes later draws dependent on earlier ones.",
         "Sampling with replacement always changes the composition of the population.",
         "Sampling without replacement guarantees the sample is unbiased.",
         "Without replacement, the second draw probability is 3/9 in the bag example."],
        ["a", "b"],
        "Replacing restores the bag to its original composition, so draws stay "
        "independent. Without replacement, after a blue is removed the probability of a "
        "second blue is 2/9, not 3/9, because one blue and one ball overall have been "
        "taken out.",
        PDF, "p.37"))

    out.append(mc(
        "L4-MC-014", 4, "Random variables",
        "Which of the following are examples of random variables?",
        ["The outcome of rolling a six-sided die",
         "The number of heads in 10 tosses of a fair coin",
         "The height of a randomly chosen adult in Norrkoping",
         "The number of emails received in an hour",
         "The area of Sweden"],
        ["a", "b", "c", "d"],
        "A random variable maps outcomes to a numerical value. Sweden's area is a fixed "
        "constant, not something that varies randomly, so it is not a random variable.",
        PDF, "p.13"))

    out.append(mc(
        "L4-MC-015", 4, "Discrete vs continuous",
        "Which random variables are DISCRETE, meaning their support is a finite or "
        "countable set of values?",
        ["The number of heads in 10 coin tosses",
         "The number of emails received in an hour",
         "The outcome of rolling a die",
         "The height of a randomly chosen adult",
         "The time until a light bulb burns out"],
        ["a", "b", "c"],
        "Heads, emails and die rolls take countable whole-number values. Height and "
        "burn-out time can take any real value in a range, so they are continuous.",
        PDF, "p.13"))

    # ----------------------------------------------------------------- written
    out.append(wa(
        "L4-WA-001", 4, "Basic probability",
        "Explain the difference between disjoint events and joint events, using a "
        "card example.",
        "Disjoint events cannot occur together, so their intersection is empty and the probability of both is 0; a red card and a black card in one draw is an example. Joint events can occur together, so a red card and a queen is joint.",
        [rb("Disjoint defined as unable to occur together, intersection probability 0", 2),
         rb("Joint defined as able to occur together", 2),
         rb("Correct card example given for each", 2)],
        1, PDF, "p.15",
        detail="The two are easy to confuse because the word joint is used loosely in everyday speech. In probability a joint probability is simply the probability of an intersection, whether or not that intersection is empty. Disjoint is a special case of mutually exclusive, and the pair red-and-black in a single draw is the clearest classroom example because a card genuinely cannot be both."))

    out.append(wa(
        "L4-WA-002", 4, "Complementary events",
        "Explain what makes two events complementary, and show why P(red or black) equals "
        "1 for a shuffled deck.",
        "Two events are complementary when they are disjoint and their union covers the entire sample space. A card is either red or black and cannot be both, so P(red or black) = P(red) + P(black) = 26/52 + 26/52 = 1.",
        [rb("Complementary defined as disjoint plus covering the whole sample space", 2),
         rb("Addition rule correctly applied to disjoint events", 2),
         rb("Substitutes 26/52 + 26/52 and concludes the probability is 1")],
        1, PDF, "p.17",
        detail="Complementary is stronger than disjoint: two events are disjoint whenever they cannot co-occur, but they are complementary only when nothing is left over. That is why complementary events always sum to exactly 1, which makes them useful for finding the remaining case without computing it directly."))

    out.append(wa(
        "L4-WA-003", 4, "Conditional probability",
        "In the MTO experiment, write down the formula for P(enrolled | low-poverty "
        "voucher) and substitute the values. You do not need to calculate the final "
        "number.",
        "`P(enrolled | low-poverty voucher) = P(enrolled and low-poverty voucher) / "
        "P(low-poverty voucher) = (14/72) / (24/72) = 14/24`",
        [rb("Correct ratio of joint probability over conditioning probability"),
         rb("Substitutes 14/72 for the joint and 24/72 for the condition"),
         rb("Simplifies to 14/24")],
        1, PDF, "p.43", r_functions=["table", "prop.table"], origin="adapted_HT25"))

    out.append(wa(
        "L4-WA-004", 4, "Independence",
        "Define independence of two events, and explain why drawing two cards without "
        "replacement gives dependent outcomes.",
        "Two events are independent if knowing whether B occurred gives no useful information about A, written P(A|B) = P(A|Bc) = P(A). Drawing without replacement is dependent, because the first card changes what remains.",
        [rb("Independence defined via P(A|B) = P(A|Bc) = P(A)", 2),
         rb("Explains the first draw changes what remains", 2),
         rb("Uses the 3/10 versus 2/9 contrast as evidence")],
        1, PDF, "p.30",
        detail="In the bag example the probability of a second blue drops from 3/10 to 2/9 once a blue is removed, so the second draw depends on the first. Independence is what allows the multiplication rule P(A and B) = P(A) * P(B) to be used; without it you need the conditional form instead."))

    out.append(wa(
        "L4-WA-005", 4, "Addition rule",
        "A bag holds 5 red, 3 blue and 2 orange balls. Without calculating, write down the "
        "formula for the probability of drawing a red or an orange ball.",
        "`P(red or orange) = P(red) + P(orange) - P(red and orange) = 5/10 + 2/10 - 0 = "
        "7/10`, because a single ball cannot be both red and orange so the intersection "
        "is empty.",
        [rb("Addition rule written in full including the subtraction term"),
         rb("Substitutes 5/10 and 2/10"),
         rb("Justifies the zero intersection as the events being disjoint")],
        1, PDF, "p.22"))

    out.append(wa(
        "L4-WA-006", 4, "Joint and conditional probability",
        "Explain the difference between a marginal probability and a conditional "
        "probability, using the MTO example.",
        "A marginal probability ignores the other variable and uses an overall total, for example P(enrolled) = 24/72. A conditional probability restricts to the condition and divides the joint probability by it, for example P(enrolled | voucher) = (14/72)/(24/72) = 14/24.",
        [rb("Marginal defined as using an overall total and ignoring the other variable", 2),
         rb("Conditional defined as joint probability divided by the condition", 2),
         rb("Correct MTO figures 24/72 and 14/24 used")],
        1, PDF, "p.43",
        detail="The two differ, which is itself evidence of an association. A conditional probability is always read inside the given condition, so the denominator is the total for that condition rather than the grand total. This is the calculation behind a comparison of two conditional probabilities that produces a chi-squared test for independence."))

    out.append(wa(
        "L4-WA-007", 4, "Random variables",
        "Explain what makes a random variable discrete or continuous, and classify the "
        "time until a light bulb burns out.",
        "A random variable is discrete when its support is a finite or countable set of values, such as die rolls or counts per hour, and continuous when it can take any value in a range. The time until a bulb burns out is continuous.",
        [rb("Discrete defined via finite or countable support", 2),
         rb("Continuous defined via any value in a range", 2),
         rb("Bulb burn-out time correctly classified as continuous with justification")],
        1, PDF, "p.13",
        detail="The bulb lifetime could be 100 hours, 250.5 hours, or any other positive real number, so no value is excluded. A count of cars per hour is discrete because 4.5 cars is meaningless. The distinction matters because continuous variables can be described by density functions and their probabilities come from areas, whereas discrete ones use probability masses that sum to 1."))

    out.append(wa(
        "L4-WA-008", 4, "Sampling with and without replacement",
        "Explain the difference between sampling with and without replacement, and state "
        "what happens to the probability of a second blue ball in each case.",
        "With replacement the ball is returned after each draw, so the bag is unchanged, the draws are independent, and the second blue has probability 3/10. Without replacement the bag becomes 2 blue out of 9, giving 2/9, so the draws are dependent.",
        [rb("With-replacement behaviour described as restoring the bag and independence", 2),
         rb("Without-replacement behaviour described as changing the composition", 2),
         rb("Both probabilities 3/10 and 2/9 correctly stated")],
        1, PDF, "p.37",
        detail="The two values 3/10 and 2/9 are the standard test of independence: they are equal exactly when the draws are independent. Replacement is the case that makes repeated draws behave like repeated copies of the same experiment, which is what justifies using the product rule repeatedly. Note that 3/10 comes from 3 blue out of 10 balls."))

    return out