"""Lecture 4 - Probability and sampling theory."""

from .common import mc, rb, wa

PDF = "lecture4_after.pdf"
PDF5 = "lecture5_after.pdf"


def questions():
    out = []

    out.append(mc(
        "L4-MC-001", 4, "Basic probability",
        "Which statements about a probability are TRUE?",
        ["P(A) can never be negative.",
         "P(A) = 0 means event A will never happen.",
         "P(A) = 1 means event A is impossible, and P(A) = 0 means it is certain.",
         "P(A) can be greater than 1 if an event is very likely.",
         "P(A) must be expressed as a percentage, not a decimal."],
        ["a", "b"],
        "A probability lies between 0 and 1, so it can be written as a decimal such as "
        "0.5 or as the equivalent 50%. A probability of 0 means the event never occurs and "
        "a probability of 1 means it always occurs, so the claim that 0 means certain is "
        "exactly backwards. It cannot exceed 1 however likely the event is.",
        PDF, "p.11"))

    out.append(mc(
        "L4-MC-002", 4, "Disjoint and joint events",
        "Drawing a red card and drawing a black card from a single draw from a full 52-card "
        "deck. How are these events related?",
        ["Joint, because both are possible in a deck",
         "Disjoint, because they cannot happen at the same time",
         "Independent, because colour is unrelated to the draw",
         "Complementary, because together they account for every card in the deck",
         "Equally likely"],
        ["b", "d"],
        "They are disjoint (mutually exclusive) since one card cannot be both red and "
        "black, so the probability of the intersection is 0. They are also complementary: "
        "every card in a deck is either red or black, because face cards are coloured too, "
        "so the two together cover the entire sample space. Disjoint and complementary are "
        "not exclusive of each other.",
        PDF, "p.17", also=['p.16']))

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
        "For a shuffled deck, P(red or black) = 26/52 + 26/52 = 1. Which two statements "
        "about this probability are TRUE?",
        ["The two events are independent",
         "The two events are complementary: they are disjoint and together cover the "
         "whole sample space",
         "Every card has probability 1",
         "Red and black are joint events",
         "Here \"or\" is inclusive: A or B means A, or B, or both, which is written A∪B"],
        ["b", "e"],
        "Red and black are disjoint and their union is the entire deck, so they are "
        "complements, and for disjoint events the addition rule reduces to simple "
        "addition, which is why the probabilities sum to exactly 1. The notation matters "
        "too: \"or\" is inclusive, so A or B counts an outcome satisfying both, which "
        "changes nothing here only because the two events cannot overlap.",
        PDF, "p.17"))

    out.append(mc(
        "L4-MC-005", 4, "Addition rule",
        "What is the general addition rule for any two events A and B?",
        ["P(A and B) = P(A) x P(B)",
         "P(A or B) = P(A) + P(B) - P(A and B)",
         "P(A or B) = P(A) + P(B)",
         "P(A) = P(A or B) - P(B)",
         "If A and B are disjoint the intersection is 0, so the rule collapses to "
         "P(A or B) = P(A) + P(B)"],
        ["b", "e"],
        "The subtraction of the intersection is required whenever A and B are not "
        "disjoint, because the overlapping cases would otherwise be counted twice. For "
        "disjoint events the intersection is 0 and the rule collapses to simple addition, "
        "which is why the third option is right only in that special case. Rearranging the "
        "rule gives P(A) = P(A or B) - P(B) + P(A and B), not what the fourth option says.",
        PDF, "p.21", origin="adapted_HT25"))

    out.append(mc(
        "L4-MC-006", 4, "Addition rule",
        "What is the probability of drawing a red jack or a black queen from a shuffled "
        "52-card deck, and how are the two events related?",
        ["4/52",
         "8/52",
         "6/52",
         "9/52",
         "The events are disjoint, because no single card is both a red jack and a black "
         "queen"],
        ["a", "e"],
        "A deck has two red jacks and two black queens, and no card is both, so the "
        "events are disjoint: 2/52 + 2/52 = 4/52. The 8/52 answer is what you would get "
        "for a jack or a queen of any colour, which is a different pair of events: a red "
        "jack and a black queen account for only four of the 52 cards.",
        PDF, "p.21"))

    out.append(mc(
        "L4-MC-007", 4, "Conditional probability",
        "Which statement correctly defines a conditional probability?",
        ["P(A and B) / P(B)",
         "P(A) / P(B)",
         "P(A and B) x P(B)",
         "The probability of A among the cases in which B is already known to hold",
         "P(B) / P(A and B)"],
        ["a", "d"],
        "A conditional probability P(A|B) restricts the sample space to B, so it is the "
        "joint probability divided by P(B), which is the same as asking for the "
        "probability of A among the cases where B is known to hold. Swapping numerator "
        "and denominator would instead give the reverse conditional probability.",
        PDF, "p.44"))

    out.append(mc(
        "L4-MC-008", 4, "Conditional probability",
        "In the MTO experiment, 72 teenagers were followed and 24 were enrolled in "
        "college. What is P(enrolled), and what kind of probability is it?",
        ["14/24",
         "24/72",
         "48/72",
         "14/72",
         "It is a marginal probability, because it does not condition on the treatment "
         "group"],
        ["b", "e"],
        "The marginal probability of enrolment is the column total over the grand total, "
        "24/72. It is marginal because it ignores which group the teenager was in. Note "
        "this is different from P(enrolled | low-poverty voucher), which conditions on "
        "the row and comes out much higher.",
        PDF, "p.40", r_functions=["table", "prop.table"], origin="adapted_HT25"))

    out.append(mc(
        "L4-MC-009", 4, "Conditional probability",
        "In the MTO experiment, what is P(enrolled | low-poverty voucher)?",
        ["24/72",
         "14/24",
         "14/72",
         "10/24",
         "About 0.58, which is higher than the overall 0.33 because enrolment depended "
         "on which group the teenager was in"],
        ["b", "e"],
        "Conditioning on the voucher restricts to the 24 teenagers who received one, of "
        "whom 14 enrolled, giving 14/24. This is the ratio (14/72)/(24/72), "
        "which simplifies to 14/24. It comes out well above the marginal 24/72, and that "
        "gap is the evidence that enrolment depended on the treatment.",
        PDF, "p.43", origin="adapted_HT25"))

    out.append(mc(
        "L4-MC-010", 4, "Independence",
        "The probability of walking to school is 0.30 overall, 0.50 for 9th graders and "
        "0.10 for 12th graders. What does this show?",
        [
        "Grade level is a binary variable",
        "The three probabilities must sum to 1",
        "Walking to school and grade level are independent",
        "Walking to school and grade level are dependent",
        "Because 0.50 and 0.10 differ from the overall 0.30, knowing the grade level "
                 "changes the probability of walking",
         ],
        ["d", "e"],
        "For independence the probability of walking would be the same whether or not B "
        "occurs. Since 0.50 and 0.10 differ from each other and from the overall 0.30, "
        "knowing the grade level changes the probability, so the variables are dependent. "
        "The three numbers are not meant to sum to 1: each is a probability of walking "
        "within a different group, and those groups overlap.",
        PDF, "p.29"))

    out.append(mc(
        "L4-MC-011", 4, "Independence",
        "Which statements are TRUE?",
        ["Two events are independent if the probability of one occurring is the same "
         "whether or not the other occurs.",
         "Drawing two cards without replacement gives independent outcomes.",
         "For two independent coin tosses, P(two tails in a row) = 1/4, because "
         "(1/2) x (1/2) = (1/2)^2.",
         "Two events are independent whenever they are disjoint.",
         "For independent events, P(A and B) = P(A) + P(B)."],
        ["a", "c"],
        "Independence means the probability of A is the same whether or not B occurs, "
        "which is the conditional form on the page before the product rule. For two "
        "independent coin tosses the joint probability is the product, 1/2 x 1/2 = 1/4. "
        "Disjointness is not independence: for a fair coin the two tosses are "
        "independent yet the heads and tails events are disjoint, whereas two disjoint "
        "events in an asymmetric deck can still be dependent. Drawing without "
        "replacement makes the second draw depend on the first, and independence "
        "multiplies rather than adds.",
        PDF, "p.30", also=["p.29"]))

    out.append(mc(
        "L4-MC-012", 4, "Sampling with and without replacement",
        "A bag holds 5 red, 3 blue and 2 orange balls. You draw a blue ball first and do "
        "NOT replace it. What is the probability of drawing a blue ball second?",
        ["3/10",
         "2/9",
         "2/10",
         "This differs from the 3/10 chance on the first draw, which is exactly what "
         "makes the two draws dependent",
         "9/100"],
        ["b", "d"],
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
        PDF, "p.37", also=['p.36']))

    out.append(mc(
        "L4-MC-014", 5, "Random variables",
        "Which of the following are examples of random variables?",
        ["The outcome of rolling a six-sided die",
         "The average number of heads in 10 tosses, which is always 5",
         "The height of a randomly chosen adult in Norrkoping",
         "The total size in bytes of every email currently in your inbox",
         "The area of Sweden"],
        ["a", "c"],
        "A random variable is a numerical value that varies from one random outcome to "
        "the next, so a die roll and an adult's height both qualify. The other three are "
        "constants: the expected number of heads in 10 fair tosses is fixed at 5, and the "
        "size of a given inbox and the area of Sweden do not move between draws. The count "
        "of emails arriving in an hour would qualify, since that does vary.",
        PDF5, "p.13"))

    out.append(mc(
        "L4-MC-015", 5, "Discrete vs continuous",
        "Which random variables are DISCRETE, meaning their support is a finite or "
        "countable set of values?",
        ["The number of heads in 10 coin tosses",
         "The number of emails received in an hour",
         "The outcome of rolling a die, because the die is a physical object",
         "The height of a randomly chosen adult",
         "The time until a light bulb burns out"],
        ["a", "b"],
        "Heads and emails take countable whole-number values, so both are discrete. A die "
        "roll is discrete too, but not because the die is a physical object; that has "
        "nothing to do with whether the support is countable. Height and burn-out time can "
        "take any real value in a range, so they are continuous.",
        PDF5, "p.13"))

    # ----------------------------------------------------------------- written
    out.append(wa(
        "L4-WA-001", 4, "Basic probability",
        "Explain the difference between disjoint events and joint events, using a "
        "card example.",
        "Disjoint events cannot occur together, so their intersection is empty and the probability of both is 0; a red card and a black card in one draw is an example. Joint events can occur together, so a red card and a queen is joint.",
        [rb("Disjoint defined as unable to occur together, intersection probability 0", 2),
         rb("Joint defined as able to occur together", 2),
         rb("Correct card example given for each", 2)],
        1, PDF, "p.15", also=['p.16'],
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
        "Define independence of two events, and explain why drawing without "
        "replacement from a bag of 5 red, 3 blue and 2 orange balls gives "
        "dependent outcomes.",
        "Two events are independent if knowing whether B occurred gives no useful information about A, written P(A|B) = P(A|Bc) = P(A). Drawing without replacement is dependent, because the first draw changes what remains.",
        [rb("Independence defined via P(A|B) = P(A|Bc) = P(A)", 2),
         rb("Explains the first draw changes what remains", 2),
         rb("Uses the 3/10 versus 2/9 contrast as evidence")],
        1, PDF, "p.29", also=['p.37'],
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
        1, PDF, "p.22", also=['p.21']))

    out.append(wa(
        "L4-WA-006", 4, "Joint and conditional probability",
        "Explain the difference between a marginal probability and a conditional "
        "probability, using the MTO example.",
        "A marginal probability ignores the other variable and uses an overall total, for example P(enrolled) = 24/72. A conditional probability restricts to the condition and divides the joint probability by it, for example P(enrolled | voucher) = (14/72)/(24/72) = 14/24.",
        [rb("Marginal defined as using an overall total and ignoring the other variable", 2),
         rb("Conditional defined as joint probability divided by the condition", 2),
         rb("Correct MTO figures 24/72 and 14/24 used")],
        1, PDF, "p.43", also=['p.40'],
        detail="The two differ, which is itself evidence of an association. A conditional probability is always read inside the given condition, so the denominator is the total for that condition rather than the grand total. This is the calculation behind a comparison of two conditional probabilities that produces a chi-squared test for independence."))

    out.append(wa(
        "L4-WA-007", 5, "Random variables",
        "Explain what makes a random variable discrete or continuous, and classify the "
        "time until a light bulb burns out.",
        "A random variable is discrete when its support is a finite or countable set of values, such as die rolls or counts per hour, and continuous when it can take any value in a range. The time until a bulb burns out is continuous.",
        [rb("Discrete defined via finite or countable support", 2),
         rb("Continuous defined via any value in a range", 2),
         rb("Bulb burn-out time correctly classified as continuous with justification")],
        1, PDF5, "p.20",
        detail="The bulb lifetime could be 100 hours, 250.5 hours, or any other positive real number, so no value is excluded. A count of cars per hour is discrete because 4.5 cars is meaningless. The distinction matters because continuous variables can be described by density functions and their probabilities come from areas, whereas discrete ones use probability masses that sum to 1."))

    out.append(wa(
        "L4-WA-008", 4, "Sampling with and without replacement",
        "Explain what distinguishes sampling with replacement from sampling without "
        "replacement.",
        "With replacement, after drawing a unit you put it back into the population "
        "before drawing again. Without replacement, you do not put it back, so the "
        "composition of the population changes as the sample is drawn.",
        [rb("With replacement defined as putting the unit back before drawing again", 2),
         rb("Without replacement defined as not putting it back", 2),
         rb("Notes the population composition changes across draws", 2)],
        1, PDF, "p.33",
        detail="Whether the draws are independent follows directly from this. In a bag with 10 balls of which 3 are blue, the second draw is 3/10 with replacement because the bag is back to 10 balls, and 2/9 without it because the first blue is gone. Those two values are equal exactly when the draws are independent, which is what makes them the standard test of the distinction."))

    return out
