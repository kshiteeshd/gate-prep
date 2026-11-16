"""Engineering Mathematics · Section 4 Probability & Statistics · Chapters 11 and 12."""
import itertools
import math
from fractions import Fraction as F

from learn import Ex
from learn.author import Author

A = Author("ENGM")
A.section("Probability & Statistics")
A.chapter("Probability Basics & Bayes")
C = math.comb


def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


# ------------------------------------------------------------------------------------------------ 11.1
A.lesson("engm-probability-bayes", "Sample spaces, events and counting probability",
         key="With equally likely outcomes, P(A) = favourable outcomes / total outcomes. The axioms give P(Aᶜ) = 1 − P(A) and P(A ∪ B) = P(A) + P(B) − P(A ∩ B). Most of the work is counting the sample space correctly, keeping track of whether order matters.",
         analogy=("🎲", "Counting equally likely worlds", "Imagine every way the experiment could turn out written on a card, all equally likely. The probability of an event is the fraction of cards on which the event happens."),
         defs=[("Sample space S", "The set of all possible outcomes of an experiment."),
               ("Event", "A subset of the sample space."),
               ("Probability", "A function P on events with P(A) ≥ 0, P(S) = 1 and P(A ∪ B) = P(A) + P(B) for disjoint events A and B."),
               ("Mutually exclusive events", "Events that cannot occur together: A ∩ B = ∅.")],
         parts=[dict(h="Equally likely outcomes", md="""If the outcomes of S are equally likely, then

$$P(A)=\\frac{|A|}{|S|}.$$

The whole difficulty lies in describing S so that its outcomes really are equally likely. For two dice treat the dice as distinguishable and list the 36 ordered pairs (a, b), not the 21 unordered ones; for cards use C(52, k) hands or ordered draws consistently, in both numerator and denominator."""),
                 dict(h="Rules of probability", md="""- 0 ≤ P(A) ≤ 1, P(∅) = 0, P(S) = 1.
- **Complement:** P(Aᶜ) = 1 − P(A).
- **Addition:** P(A ∪ B) = P(A) + P(B) − P(A ∩ B); for exclusive events the last term vanishes.
- **"At least one"** = 1 − P(none). For independent trials this turns a long union into one product.
- If A ⊆ B then P(A) ≤ P(B).
- Three events: P(A ∪ B ∪ C) = ΣP − ΣP(pairs) + P(A ∩ B ∩ C)."""),
                 dict(h="Standard experiments", md="""| Experiment | Sample space | Useful counts |
|---|---|---|
| n coin tosses | 2ⁿ outcomes | exactly k heads: C(n, k) |
| two dice | 36 ordered pairs | sum 7: 6 outcomes; the sum 2 or 12: 1 outcome |
| k cards from 52 | C(52, k) hands | exactly j aces: C(4, j)·C(48, k − j) |
| a random permutation of n | n! orders | none fixed: Dₙ/n! → 1/e |

Drawing **with replacement** keeps the probabilities the same at every draw; drawing **without replacement** changes them (use products like (4/52)(3/51) or combinations).""")],
         examples=[
             Ex("Two dice", "Two fair dice are rolled. Find the probability that the sum is 8.", ["Favourable ordered pairs: (2,6), (3,5), (4,4), (5,3), (6,2): 5 of 36."], "**5/36**", verify=lambda: str(F(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 8), 36))),
             Ex("At least one head", "A fair coin is tossed 4 times. Find the probability of at least one head.", ["P(no head) = (1/2)⁴ = 1/16."], "**15/16**", verify=lambda: str(1 - F(1, 16))),
             Ex("Cards", "Five cards are drawn from a deck. Find the probability of exactly 2 aces.", ["Favourable: C(4, 2)·C(48, 3) = 6·17296 = 103776.", "Total: C(52, 5) = 2598960."], "**103776/2598960 ≈ 0.0399**", verify=lambda: "%d/%d ≈ %.4f" % (C(4, 2) * C(48, 3), C(52, 5), C(4, 2) * C(48, 3) / C(52, 5))),
             Ex("Union of events", "P(A) = 0.5, P(B) = 0.4 and P(A ∩ B) = 0.2. Find P(A ∪ B) and P(neither).", ["P(A ∪ B) = 0.5 + 0.4 − 0.2 = 0.7.", "P(neither) = 1 − 0.7."], "**0.7** and **0.3**.", verify=lambda: "%.1f and %.1f" % (0.5 + 0.4 - 0.2, 1 - (0.5 + 0.4 - 0.2))),
             Ex("GATE style: without replacement", "A bag has 4 red and 6 blue balls. Two balls are drawn without replacement. Find the probability that they have the same colour.", ["Both red: (4/10)(3/9) = 12/90. Both blue: (6/10)(5/9) = 30/90.", "Total 42/90."], "**7/15**", verify=lambda: str(F(4 * 3 + 6 * 5, 10 * 9)))],
         traps=[("Dice as unordered pairs", "The 36 ordered pairs are equally likely; the 21 unordered ones are not."),
                ("At least one", "Use the complement 1 − P(none), not a sum of probabilities."),
                ("Adding non-exclusive events", "Subtract P(A ∩ B) when the events can overlap."),
                ("Replacement", "Without replacement the probabilities change after each draw.")],
         quick=[("P(sum = 7) with two fair dice", ["1/6", "1/12", "5/36", "7/36"], 0, "6 of 36."),
                ("P(at least one six in 3 rolls)", ["1/2", "91/216", "125/216", "1/6"], 1, "1 − (5/6)³."),
                ("P(A ∪ B) with P(A) = 0.3, P(B) = 0.5, P(A ∩ B) = 0.1", ["0.7", "0.8", "0.9", "0.65"], 0, "0.3 + 0.5 − 0.1."),
                ("Number of equally likely outcomes of 3 coin tosses", ["3", "6", "8", "9"], 2, "2³.")],
         summary=["Equally likely outcomes: P(A) = |A|/|S|; choose S so that the outcomes are equally likely.", "P(Aᶜ) = 1 − P(A); P(A ∪ B) = P(A) + P(B) − P(A ∩ B).", "'At least one' = 1 − P(none).", "Two dice: 36 ordered pairs; sum 7 has probability 1/6.", "Without replacement, update the counts after each draw."],
         subs=["Dice & coins"], widget="prob", hint="Simulate dice and coins and compare the frequencies with the exact probabilities.")

# ------------------------------------------------------------------------------------------------ 11.2
A.lesson("engm-pb-conditional", "Conditional probability and independence",
         key="P(A | B) = P(A ∩ B)/P(B) is the probability of A when B is known to have happened. Events are independent when P(A ∩ B) = P(A)P(B). Mutually exclusive events with positive probability are never independent.",
         analogy=("🔍", "Zooming into the evidence", "Conditioning on B throws away every outcome outside B and rescales what is left. What matters afterwards is only how large A is inside B."),
         defs=[("Conditional probability P(A | B)", "P(A ∩ B)/P(B), the probability of A given that B has occurred (P(B) > 0)."),
               ("Independent events", "Events A and B with P(A ∩ B) = P(A)·P(B); equivalently P(A | B) = P(A)."),
               ("Multiplication rule", "P(A ∩ B) = P(A)·P(B | A).")],
         parts=[dict(h="Conditional probability", md="""$$P(A\\mid B)=\\frac{P(A\\cap B)}{P(B)},\\qquad P(B)>0 .$$

Rearranged, this is the **multiplication rule** P(A ∩ B) = P(B)·P(A | B), which extends to chains: P(A ∩ B ∩ C) = P(A)·P(B | A)·P(C | A ∩ B). Draws without replacement are computed this way. To find P(A | B) by counting, restrict the sample space to B: "given the sum is 8, what is the chance the first die shows 3?" has sample space the 5 pairs with sum 8, and the answer is 1/5."""),
                 dict(h="Independence", md="""A and B are **independent** iff P(A ∩ B) = P(A)P(B), i.e. learning B does not change P(A). Then A and Bᶜ, Aᶜ and B, Aᶜ and Bᶜ are independent too, and P(A ∪ B) = 1 − P(Aᶜ)P(Bᶜ).

- **Mutually exclusive ≠ independent.** If P(A), P(B) > 0 and A ∩ B = ∅, then P(A ∩ B) = 0 ≠ P(A)P(B): knowing A occurred tells you B did not.
- Several events are *mutually* independent only if every sub-collection multiplies; pairwise independence is weaker.
- Independence is about probabilities, not about causation or disjointness."""),
                 dict(h="Conditioning on partial information", md="""Classic traps: "two children, at least one is a boy" (sample space BB, BG, GB: P(both boys) = 1/3) versus "the older child is a boy" (sample space BB, BG: probability 1/2). Always list the equally likely outcomes consistent with the information, then count.""")],
         examples=[
             Ex("Conditioning on a sum", "Two dice are rolled and the sum is 8. Find the probability that the first die shows 3.", ["Outcomes with sum 8: (2,6), (3,5), (4,4), (5,3), (6,2).", "Exactly one has first die 3."], "**1/5**", verify=lambda: str(F(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 8 and a == 3), sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 8)))),
             Ex("From the definition", "P(A ∩ B) = 0.2 and P(B) = 0.5. Find P(A | B).", ["0.2/0.5."], "**0.4**", verify=lambda: str(0.2 / 0.5)),
             Ex("Union of independent events", "A and B are independent with P(A) = 0.5 and P(B) = 0.4. Find P(A ∪ B).", ["P(A ∩ B) = 0.2.", "0.5 + 0.4 − 0.2."], "**0.7**", verify=lambda: str(round(0.5 + 0.4 - 0.5 * 0.4, 10))),
             Ex("Without replacement", "Two cards are drawn from a deck without replacement. Find the probability that both are aces.", ["P(first ace) = 4/52; P(second ace | first) = 3/51."], "**1/221**", verify=lambda: str(F(4, 52) * F(3, 51))),
             Ex("GATE style: two children", "A family has two children and at least one is a boy. What is the probability that both are boys?", ["Equally likely: BB, BG, GB, GG; the information removes GG.", "One of three remaining outcomes is BB."], "**1/3**", verify=lambda: str(F(1, 3)))],
         traps=[("Confusing P(A|B) with P(B|A)", "They are different numbers; only Bayes' theorem relates them."),
                ("Exclusive means independent?", "Exclusive events with positive probability are dependent."),
                ("Forgetting to restrict the sample space", "Conditioning shrinks the sample space to B."),
                ("Replacement", "Without replacement the second draw depends on the first.")],
         quick=[("P(A | B) =", ["P(A)P(B)", "P(A ∩ B)/P(B)", "P(B | A)", "P(A)/P(B)"], 1, "The definition."),
                ("Independent events satisfy", ["P(A ∩ B) = P(A) + P(B)", "P(A ∩ B) = P(A)P(B)", "P(A ∩ B) = 0", "P(A) = P(B)"], 1, "The product rule."),
                ("Two mutually exclusive events with P > 0 are", ["independent", "dependent", "equal", "complementary"], 1, "P(A ∩ B) = 0 ≠ P(A)P(B)."),
                ("If A and B are independent, P(Aᶜ ∩ B) =", ["P(A)P(B)", "(1 − P(A))P(B)", "1 − P(A)P(B)", "0"], 1, "Aᶜ and B are independent.")],
         summary=["P(A | B) = P(A ∩ B)/P(B): restrict the sample space to B.", "Multiplication rule: P(A ∩ B) = P(A)P(B | A); chains extend it.", "Independent ⇔ P(A ∩ B) = P(A)P(B), and then complements are independent too.", "Mutually exclusive events with positive probability are not independent.", "List the outcomes consistent with the information before counting."],
         subs=["Independence"])

# ------------------------------------------------------------------------------------------------ 11.3
A.lesson("engm-pb-bayes", "Total probability and Bayes' theorem",
         key="Split the sample space into causes A₁, …, A_k. The law of total probability gives P(B) = ΣP(Aᵢ)P(B | Aᵢ), and Bayes' theorem reverses the conditioning: P(Aⱼ | B) = P(Aⱼ)P(B | Aⱼ)/P(B). A tree or a table of counts makes every such problem mechanical.",
         analogy=("🌳", "A tree of causes", "A positive test result came either from a sick person or a healthy one. Bayes' theorem works backwards from the result: out of all positive results, what fraction came from the sick branch?"),
         defs=[("Partition of S", "Events A₁, …, A_k that are mutually exclusive and together cover S."),
               ("Prior and posterior", "P(Aᵢ) before the evidence is seen, and P(Aᵢ | B) after observing B."),
               ("Likelihood", "P(B | Aᵢ): how probable the evidence is under each cause.")],
         parts=[dict(h="Total probability and Bayes", md="""If A₁, …, A_k partition the sample space, then for any event B:

$$P(B)=\\sum_i P(A_i)\\,P(B\\mid A_i),\\qquad P(A_j\\mid B)=\\frac{P(A_j)\\,P(B\\mid A_j)}{\\sum_i P(A_i)\\,P(B\\mid A_i)} .$$

The first line says: add up the probability of B along every cause. The second divides the share of cause j by the total."""),
                 dict(h="Method: a probability tree", md="""1. Name the partition: disease/healthy, urn 1/urn 2, machine A/B/C.
2. Write each **prior** P(Aᵢ) and **likelihood** P(B | Aᵢ).
3. Multiply along each branch and add the branches that end in B: that is P(B).
4. The **posterior** is the branch for the cause you ask about divided by P(B).

**Natural frequencies** make the same computation concrete. With a disease affecting 1% of people, a test that detects 90% of cases and wrongly flags 5% of healthy people, imagine 10 000 people: 100 sick (90 flagged) and 9 900 healthy (495 flagged). Of 585 flagged people only 90 are sick: 15.4%."""),
                 dict(h="Reading the result", md="""A positive result from a good test can still be weak evidence when the condition is rare, because the many healthy people produce more false positives than the few sick people produce true ones. The posterior depends on the prior and the likelihood ratio together; equal priors cancel. Do not confuse P(positive | sick) with P(sick | positive): the prosecutor's fallacy.""")],
         examples=[
             Ex("A factory", "Machine M₁ makes 60% of items and 2% of them are defective; machine M₂ makes 40% and 5% of them are defective. A defective item is found. What is the probability it came from M₁?", ["P(D) = 0.6·0.02 + 0.4·0.05 = 0.012 + 0.020 = 0.032.", "P(M₁ | D) = 0.012/0.032."], "**0.375**", verify=lambda: str(F(6, 10) * F(2, 100) / (F(6, 10) * F(2, 100) + F(4, 10) * F(5, 100)))),
             Ex("A medical test", "1% of people have a disease. A test is positive for 99% of the sick and for 5% of the healthy. Find P(sick | positive).", ["P(+) = 0.01·0.99 + 0.99·0.05 = 0.0099 + 0.0495 = 0.0594.", "P(sick | +) = 0.0099/0.0594."], "**1/6 ≈ 0.167**", verify=lambda: "%s ≈ %.3f" % (F(99, 100) * F(1, 100) / (F(99, 100) * F(1, 100) + F(99, 100) * F(5, 100)), float(F(99, 100) * F(1, 100) / (F(99, 100) * F(1, 100) + F(99, 100) * F(5, 100))))),
             Ex("Two urns", "Urn A has 3 red and 1 blue ball; urn B has 1 red and 3 blue. An urn is chosen at random and a red ball is drawn. What is the probability the urn was A?", ["P(red) = ½·¾ + ½·¼ = ½.", "P(A | red) = (3/8)/(1/2)."], "**3/4**", verify=lambda: str(F(1, 2) * F(3, 4) / (F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4)))),
             Ex("Total probability", "P(A) = 0.3, P(B | A) = 0.5, P(B | Aᶜ) = 0.2. Find P(B).", ["0.3·0.5 + 0.7·0.2 = 0.15 + 0.14."], "**0.29**", verify=lambda: str(round(0.3 * 0.5 + 0.7 * 0.2, 10))),
             Ex("GATE style: three machines", "Three machines produce 50%, 30% and 20% of items with defect rates 1%, 2% and 3%. A defective item is chosen. Find the probability it came from the third machine.", ["P(D) = 0.5·0.01 + 0.3·0.02 + 0.2·0.03 = 0.005 + 0.006 + 0.006 = 0.017.", "P(M₃ | D) = 0.006/0.017."], "**6/17 ≈ 0.353**", verify=lambda: "%s ≈ %.3f" % (F(6, 17), 6 / 17) if F(5, 1000) + F(6, 1000) + F(6, 1000) == F(17, 1000) else "?")],
         traps=[("Reversing the conditioning", "P(sick | positive) is not P(positive | sick)."),
                ("Forgetting the denominator", "P(B) must add up every branch that ends in B."),
                ("Ignoring the prior", "A rare condition keeps the posterior small even for an accurate test."),
                ("Partition", "The causes must be exclusive and cover the sample space.")],
         quick=[("P(B) by total probability with priors 0.4, 0.6 and likelihoods 0.5, 0.2", ["0.26", "0.32", "0.7", "0.1"], 1, "0.2 + 0.12."),
                ("Bayes' theorem reverses", ["P(A ∩ B)", "the conditioning", "independence", "the sample space"], 1, "From P(B | A) to P(A | B)."),
                ("With equal priors, the posterior depends on", ["the likelihoods", "nothing", "only the number of causes", "the variance"], 0, "The priors cancel."),
                ("A partition consists of events that are", ["independent", "exclusive and exhaustive", "equally likely", "complementary pairs only"], 1, "They cover S without overlap.")],
         summary=["P(B) = ΣP(Aᵢ)P(B | Aᵢ) over a partition.", "P(Aⱼ | B) = P(Aⱼ)P(B | Aⱼ)/P(B).", "Draw a tree: priors on the first branches, likelihoods on the second.", "Rare conditions give small posteriors even with accurate tests.", "Natural frequencies (counts out of 10 000) make Bayes problems concrete."],
         subs=["Bayes with tables", "Bayes & conditional"])

# ====================================================================================================
A.chapter("Random Variables & Distributions")

# ------------------------------------------------------------------------------------------------ 12.1
A.lesson("engm-random-variables-distributions", "Random variables, PMF, PDF and CDF",
         key="A random variable assigns a number to each outcome. A discrete one has a probability mass function p(x); a continuous one has a density f(x) whose areas are probabilities. The cumulative distribution function F(x) = P(X ≤ x) rises from 0 to 1 in both cases.",
         analogy=("🎰", "A number on every outcome", "A random variable is a rule turning each outcome into a number, such as the sum of two dice. The distribution tells you how likely each number is."),
         defs=[("Random variable X", "A function assigning a real number to every outcome of an experiment."),
               ("PMF p(x)", "p(x) = P(X = x) for a discrete random variable."),
               ("PDF f(x)", "A density function with P(a ≤ X ≤ b) = ∫ₐᵇ f(x) dx for a continuous random variable."),
               ("CDF F(x)", "F(x) = P(X ≤ x); non-decreasing from 0 to 1.")],
         parts=[dict(h="Discrete and continuous", md="""| | Discrete | Continuous |
|---|---|---|
| describes | p(x) = P(X = x) | density f(x) |
| conditions | p(x) ≥ 0, Σp(x) = 1 | f(x) ≥ 0, ∫f = 1 |
| P(a ≤ X ≤ b) | Σ p(x) over the values | ∫ₐᵇ f(x) dx |
| P(X = a) | p(a) | **0** |
| CDF F(x) | Σ_{t ≤ x} p(t) (a step function) | ∫₋∞ˣ f(t) dt (continuous) |

For a continuous X, endpoints do not matter: P(X < a) = P(X ≤ a). A density can exceed 1 (areas are what must total 1)."""),
                 dict(h="Using the CDF", md="""- F is non-decreasing, F(−∞) = 0, F(+∞) = 1.
- P(a < X ≤ b) = F(b) − F(a).
- For continuous X, f(x) = F′(x), so the CDF of f(x) = 2x on [0, 1] is F(x) = x².
- The **median** m solves F(m) = 1/2; the **mode** is where p or f is largest."""),
                 dict(h="Finding constants", md="""If p(x) = k·g(x) or f(x) = c·g(x), find the constant from the normalisation: Σp = 1 or ∫f = 1. Example: P(X = x) = kx for x = 1, …, 4 gives k(1 + 2 + 3 + 4) = 1, so k = 1/10. For f(x) = cx² on [0, 3], ∫₀³ cx² dx = 9c = 1, so c = 1/9.""")],
         examples=[
             Ex("Normalising a PMF", "P(X = x) = kx for x = 1, 2, 3, 4. Find k.", ["k(1 + 2 + 3 + 4) = 10k = 1."], "**k = 1/10**", verify=lambda: str(F(1, 10))),
             Ex("Normalising a PDF", "f(x) = cx² on [0, 3] (zero elsewhere). Find c.", ["∫₀³ cx² dx = c·27/3 = 9c = 1."], "**c = 1/9**", verify=lambda: str(F(1, 9))),
             Ex("Using the CDF", "X has density f(x) = 2x on [0, 1]. Find P(1/4 < X ≤ 1/2).", ["F(x) = x².", "F(1/2) − F(1/4) = 1/4 − 1/16."], "**3/16**", verify=lambda: str(F(1, 4) - F(1, 16))),
             Ex("A median", "Find the median of the exponential distribution with rate 2.", ["F(m) = 1 − e^(−2m) = 1/2, so m = ln 2/2."], "**ln 2 / 2 ≈ 0.347**", verify=lambda: "ln 2 / 2 ≈ %.3f" % (math.log(2) / 2)),
             Ex("GATE style: a point probability", "X is continuous with density f(x) = 3x² on [0, 1]. Find P(X = 0.5) and P(X ≤ 0.5).", ["For a continuous variable P(X = 0.5) = 0.", "F(x) = x³ so P(X ≤ 0.5) = 1/8."], "**0** and **1/8**.", verify=lambda: "%d and %s" % (0, F(1, 8)))],
         traps=[("Density versus probability", "f(x) is not P(X = x); areas give probabilities."),
                ("Endpoints", "For continuous X, < and ≤ give the same probability."),
                ("Forgetting to normalise", "Find the constant first."),
                ("CDF direction", "F(x) = P(X ≤ x), so F increases to 1.")],
         quick=[("For continuous X, P(X = 2) is", ["f(2)", "0", "F(2)", "1"], 1, "A single point has zero area."),
                ("A CDF is always", ["decreasing", "non-decreasing", "periodic", "bounded by 1/2"], 1, "It accumulates probability."),
                ("f(x) = 3x² on [0, 1]. F(1/2) =", ["1/8", "3/4", "1/2", "3/8"], 0, "x³ at 1/2."),
                ("The PMF of a discrete variable must satisfy", ["Σp = 1", "∫p = 1", "p ≤ 1/2", "Σp = 0"], 0, "Probabilities total 1.")],
         summary=["PMF: p ≥ 0 and Σp = 1; PDF: f ≥ 0 and ∫f = 1.", "P(a < X ≤ b) = F(b) − F(a); for continuous X, f = F′.", "A continuous variable has P(X = a) = 0.", "The median solves F(m) = 1/2.", "Find constants from the normalisation condition."],
         subs=["Random variables"])

# ------------------------------------------------------------------------------------------------ 12.2
A.lesson("engm-pb-expectation", "Expectation and variance",
         key="E[X] = Σx·p(x) (or ∫x·f(x) dx) is the long-run average; Var(X) = E[X²] − (E[X])² measures spread. Expectation is linear even without independence; variances add only for independent variables; and Var(aX + b) = a²Var(X).",
         analogy=("⚖️", "A balance point", "The mean is where a seesaw carrying the probability weights would balance; the variance tells how far the weights are scattered from that point."),
         defs=[("Expectation E[X]", "Σ x·p(x) for discrete X, ∫ x·f(x) dx for continuous X: the long-run average."),
               ("Variance Var(X)", "E[(X − μ)²] = E[X²] − (E[X])², where μ = E[X]."),
               ("Standard deviation σ", "The square root of the variance.")],
         parts=[dict(h="Expectation and its rules", md="""- E[g(X)] = Σ g(x)·p(x) (law of the unconscious statistician): never replace E[g(X)] by g(E[X]).
- **Linearity:** E[aX + bY + c] = aE[X] + bE[Y] + c, **always**, even for dependent variables.
- Independent X, Y: E[XY] = E[X]E[Y].
- **Indicator variables:** if X = I₁ + … + Iₙ with Iₖ ∈ {0, 1}, then E[X] = ΣP(Iₖ = 1). Example: the expected number of fixed points of a random permutation of n objects is n·(1/n) = 1."""),
                 dict(h="Variance and its rules", md="""$$\\operatorname{Var}(X)=E[X^2]-(E[X])^2 .$$

- Var(aX + b) = a²Var(X): shifting does nothing, scaling squares.
- For **independent** X and Y: Var(X ± Y) = Var X + Var Y (the minus sign disappears).
- In general Var(X + Y) = Var X + Var Y + 2Cov(X, Y), and Cov(X, Y) = E[XY] − E[X]E[Y].
- Var(X) ≥ 0, with equality only for a constant."""),
                 dict(h="Moments and bounds", md="""The kth moment is E[Xᵏ]. Useful inequalities: **Markov** P(X ≥ a) ≤ E[X]/a for X ≥ 0; **Chebyshev** P(|X − μ| ≥ kσ) ≤ 1/k². The correlation coefficient ρ = Cov(X, Y)/(σ_Xσ_Y) lies in [−1, 1]; independent variables have Cov = 0, but Cov = 0 does not imply independence.""")],
         examples=[
             Ex("A fair die", "Find E[X] and Var(X) for one roll of a fair die.", ["E[X] = (1 + … + 6)/6 = 3.5.", "E[X²] = (1 + 4 + 9 + 16 + 25 + 36)/6 = 91/6, so Var = 91/6 − 49/4 = 35/12."], "**3.5** and **35/12**.", verify=lambda: "%s and %s" % (F(7, 2), F(91, 6) - F(49, 4))),
             Ex("Linearity", "E[X] = 3 and E[Y] = 5 (not necessarily independent). Find E[2X − Y + 4].", ["2·3 − 5 + 4."], "**5**", verify=lambda: str(2 * 3 - 5 + 4)),
             Ex("A linear combination", "X and Y are independent with Var(X) = 3 and Var(Y) = 5. Find Var(2X − Y).", ["4·3 + 1·5."], "**17**", verify=lambda: str(4 * 3 + 5)),
             Ex("Indicator variables", "A random permutation of 10 items is chosen. What is the expected number of items left in place?", ["Ten indicators, each with probability 1/10: 10·(1/10)."], "**1**", verify=lambda: str(10 * F(1, 10))),
             Ex("GATE style: shift and scale", "Var(X) = 2. Find Var(3X + 7) and the standard deviation of 3X + 7.", ["Var(3X + 7) = 9·2 = 18.", "σ = √18 = 3√2 ≈ 4.243."], "**18** and **4.243**.", verify=lambda: "%d and %.3f" % (9 * 2, math.sqrt(18)))],
         traps=[("Variance of a difference", "Variances add, even for X − Y."),
                ("Linearity needs no independence", "E[X + Y] = E[X] + E[Y] always."),
                ("g(E[X]) versus E[g(X)]", "In general E[X²] ≠ (E[X])²; the difference is the variance."),
                ("Var(aX + b)", "The constant b vanishes and a is squared.")],
         quick=[("Var(3X) =", ["3Var(X)", "9Var(X)", "Var(X)", "Var(X) + 3"], 1, "a²."),
                ("E[X + Y] for dependent X and Y", ["E[X]E[Y]", "E[X] + E[Y]", "cannot be found", "0"], 1, "Linearity holds always."),
                ("If E[X] = 2 and E[X²] = 9, Var(X) =", ["5", "7", "11", "3"], 0, "9 − 4."),
                ("For independent X, Y with Var 1 and 4, Var(X − Y) =", ["3", "5", "−3", "9"], 1, "1 + 4.")],
         summary=["E[aX + bY + c] = aE[X] + bE[Y] + c always.", "Var(X) = E[X²] − (E[X])²; Var(aX + b) = a²Var(X).", "Independent: Var(X ± Y) = Var X + Var Y and E[XY] = E[X]E[Y].", "Indicator variables turn counts into sums of probabilities.", "Chebyshev: P(|X − μ| ≥ kσ) ≤ 1/k²."],
         subs=["Expectation & variance"])

# ------------------------------------------------------------------------------------------------ 12.3
A.lesson("engm-pb-distributions", "Discrete distributions: binomial, geometric and Poisson",
         key="Binomial(n, p) counts successes in n independent trials; geometric(p) counts trials until the first success; Poisson(λ) counts rare events and approximates the binomial when n is large and p small (λ = np). Know each pmf, mean and variance.",
         analogy=("🎲", "A menu of random processes", "Each distribution is the answer to a story. Counting heads in 10 tosses is binomial; waiting for the first six is geometric; counting phone calls in a minute is Poisson."),
         defs=[("Bernoulli trial", "An experiment with two outcomes, success with probability p and failure with probability 1 − p."),
               ("Binomial(n, p)", "The number of successes in n independent Bernoulli trials."),
               ("Geometric(p)", "The number of independent trials up to and including the first success."),
               ("Poisson(λ)", "A count of rare events in a fixed interval with average rate λ.")],
         parts=[dict(h="The three distributions", md="""| Distribution | pmf | Mean | Variance |
|---|---|---|---|
| Bernoulli(p) | p, 1 − p | p | p(1 − p) |
| Binomial(n, p) | C(n, k)pᵏ(1 − p)ⁿ⁻ᵏ, k = 0..n | np | np(1 − p) |
| Geometric(p) | (1 − p)ᵏ⁻¹p, k = 1, 2, … | 1/p | (1 − p)/p² |
| Poisson(λ) | e^(−λ)λᵏ/k!, k = 0, 1, … | λ | λ |

The geometric distribution is **memoryless**: P(X > s + t | X > s) = P(X > t). Poisson has mean equal to variance, so E[X²] = λ + λ²."""),
                 dict(h="Which distribution?", md="""| The story | Distribution |
|---|---|
| number of successes in a fixed number n of independent trials | Binomial(n, p) |
| number of trials until the first success | Geometric(p) |
| number of rare events in a fixed interval, average rate λ | Poisson(λ) |
| one trial, success or failure | Bernoulli(p) |

When n is large and p is small, Binomial(n, p) ≈ Poisson(np). A sum of independent Binomial(n₁, p) and Binomial(n₂, p) is Binomial(n₁ + n₂, p); a sum of independent Poissons adds the rates."""),
                 dict(h="Working with the pmfs", md="""Probabilities of the form "at most k" add terms of the pmf; "at least one" uses the complement 1 − P(X = 0). For the binomial: P(X ≥ 1) = 1 − (1 − p)ⁿ. For the geometric: P(X > k) = (1 − p)ᵏ. For Poisson: P(X = 0) = e^(−λ). Always confirm the parametrisation: some texts define the geometric variable as the number of *failures* before the first success, with mean (1 − p)/p.""")],
         examples=[
             Ex("Binomial mean and variance", "X ~ Binomial(10, 0.3). Find E[X] and Var(X).", ["np = 3 and np(1 − p) = 10·0.3·0.7."], "**3** and **2.1**.", verify=lambda: "%d and %.1f" % (3, 10 * 0.3 * 0.7)),
             Ex("A binomial probability", "A fair coin is tossed 5 times. Find P(exactly 2 heads).", ["C(5, 2)/2⁵ = 10/32."], "**5/16**", verify=lambda: str(F(C(5, 2), 32))),
             Ex("Geometric", "A trial succeeds with probability 0.2. Find the expected number of trials until the first success.", ["1/p."], "**5**", verify=lambda: str(round(1 / 0.2, 6))),
             Ex("Poisson", "X ~ Poisson(4). Find E[X²].", ["Var + mean² = 4 + 16."], "**20**", verify=lambda: str(4 + 16)),
             Ex("GATE style: at least one", "Calls arrive as a Poisson process with rate 2 per minute. Find P(at least one call in a minute) to 3 decimals.", ["P(none) = e^(−2).", "1 − e^(−2)."], "**0.865**", verify=lambda: "%.3f" % (1 - math.exp(-2)))],
         traps=[("Variance of a difference", "Variances add, even for X − Y."),
                ("Geometric conventions", "Trials until success (mean 1/p) versus failures before success (mean (1 − p)/p)."),
                ("Poisson", "Mean equals variance; E[X²] = λ + λ²."),
                ("Binomial pmf", "Do not forget the factor C(n, k).")],
         quick=[("Var of Binomial(20, 0.5)", ["5", "10", "20", "0.25"], 0, "np(1 − p)."),
                ("Mean of a geometric variable with p = 0.25", ["2", "4", "0.25", "8"], 1, "1/p."),
                ("Poisson(λ) has mean and variance", ["λ and λ²", "λ and λ", "λ² and λ", "1/λ and 1/λ²"], 1, "They are equal."),
                ("P(at least one success) in n trials with probability p", ["np", "1 − (1 − p)ⁿ", "pⁿ", "1 − pⁿ"], 1, "The complement of no success.")],
         summary=["Binomial(n, p): pmf C(n, k)pᵏ(1 − p)ⁿ⁻ᵏ, mean np, variance np(1 − p).", "Geometric(p): pmf (1 − p)ᵏ⁻¹p, mean 1/p, memoryless.", "Poisson(λ): pmf e^(−λ)λᵏ/k!, mean = variance = λ.", "Binomial(n, p) ≈ Poisson(np) for large n and small p.", "'At least one' = 1 − P(none)."],
         subs=["Distribution formulas", "Distributions"])

# ------------------------------------------------------------------------------------------------ 12.4
A.lesson("engm-pb-continuous", "Continuous distributions: uniform, exponential and normal",
         key="Uniform[a, b] spreads probability evenly; the exponential distribution models waiting times and is memoryless; the normal N(μ, σ²) is the bell curve, handled by standardising with z = (x − μ)/σ and reading Φ.",
         analogy=("🔔", "The bell curve", "Add up many small independent effects and the total settles into the same bell shape, wherever the effects came from. That is why the normal distribution appears everywhere."),
         defs=[("Uniform[a, b]", "A continuous distribution with constant density 1/(b − a) on [a, b]."),
               ("Exponential(λ)", "A distribution with density λe^(−λx) for x ≥ 0; the waiting time between events of a Poisson process."),
               ("Normal N(μ, σ²)", "The bell-shaped distribution with mean μ and variance σ²."),
               ("Standard score z", "z = (x − μ)/σ, the distance from the mean in standard deviations.")],
         parts=[dict(h="Reference table", md="""| Distribution | Density | Mean | Variance |
|---|---|---|---|
| Uniform[a, b] | 1/(b − a) | (a + b)/2 | (b − a)²/12 |
| Exponential(λ) | λe^(−λx), x ≥ 0 | 1/λ | 1/λ² |
| Normal N(μ, σ²) | (1/(σ√(2π)))e^(−(x − μ)²/(2σ²)) | μ | σ² |

For the exponential: P(X > t) = e^(−λt), the median is (ln 2)/λ, and it is **memoryless**: P(X > s + t | X > s) = P(X > t). It is the only continuous memoryless distribution."""),
                 dict(h="The normal distribution", md="""N(μ, σ²) is symmetric about μ, with mean = median = mode = μ. To find a probability, **standardise**: Z = (X − μ)/σ is N(0, 1), and P(X ≤ x) = Φ((x − μ)/σ). Useful values: Φ(0) = 0.5, Φ(1) ≈ 0.8413, Φ(2) ≈ 0.9772, Φ(3) ≈ 0.9987, and Φ(−z) = 1 − Φ(z).

- About 68% of values lie within 1σ of the mean, 95% within 2σ, 99.7% within 3σ.
- A sum of independent normals is normal: means add and variances add."""),
                 dict(h="Working with them", md="""Uniform probabilities are length ratios. Exponential probabilities use e^(−λt); "given that it has already lasted s" changes nothing because of memorylessness. For the normal, always write the z-score first and then use the table values given in the question. The rate λ and the mean 1/λ are easy to confuse: a mean of 10 minutes means λ = 0.1 per minute.""")],
         examples=[
             Ex("Standardising", "X ~ N(50, 4²). Find P(X ≤ 58) using Φ(2) = 0.9772.", ["z = (58 − 50)/4 = 2."], "**0.9772**", verify=lambda: "%.4f" % 0.9772),
             Ex("A symmetric interval", "X ~ N(100, 15²). Find P(85 < X < 115) using Φ(1) = 0.8413.", ["z-scores −1 and 1: Φ(1) − Φ(−1) = 2Φ(1) − 1."], "**0.6826**", verify=lambda: "%.4f" % (2 * 0.8413 - 1)),
             Ex("Memorylessness", "The lifetime of a component is exponential with mean 10 hours. It has already survived 5 hours. What is the probability it lasts at least 10 more hours?", ["λ = 1/10. By memorylessness the answer is P(X > 10) = e^(−10/10)."], "**e⁻¹ ≈ 0.368**", verify=lambda: "e⁻¹ ≈ %.3f" % math.exp(-1)),
             Ex("Uniform", "X is uniform on [2, 8]. Find the mean, the variance and P(3 ≤ X ≤ 5).", ["Mean (2 + 8)/2 = 5; variance 36/12 = 3.", "P = (5 − 3)/6 = 1/3."], "**5**, **3** and **1/3**.", verify=lambda: "%d, %d and %s" % ((2 + 8) // 2, 36 // 12, F(2, 6))),
             Ex("GATE style: exponential rate", "Customers arrive at rate 3 per hour (a Poisson process). Find the probability that the waiting time to the next arrival exceeds 20 minutes.", ["λ = 3 per hour, t = 1/3 hour.", "P(X > 1/3) = e^(−3·(1/3)) = e⁻¹."], "**e⁻¹ ≈ 0.368**", verify=lambda: "e⁻¹ ≈ %.3f" % math.exp(-3 * (1 / 3)))],
         traps=[("σ versus σ²", "N(μ, σ²) lists the variance; standardise with σ."),
                ("Φ(−z)", "Φ(−z) = 1 − Φ(z)."),
                ("Rate versus mean", "The exponential mean is 1/λ."),
                ("Memorylessness", "The time already survived does not change the future probability.")],
         quick=[("Z = (X − μ)/σ has mean and variance", ["0 and 1", "μ and σ", "1 and 0", "0 and σ²"], 0, "The standard normal."),
                ("The exponential distribution is", ["memoryless", "symmetric", "bounded", "discrete"], 0, "P(X > s + t | X > s) = P(X > t)."),
                ("Variance of uniform[0, 12]", ["1", "6", "12", "144"], 2, "12²/12."),
                ("About what fraction of a normal distribution lies within 2σ of the mean?", ["68%", "95%", "99.7%", "50%"], 1, "The 68–95–99.7 rule.")],
         summary=["Uniform[a, b]: mean (a + b)/2, variance (b − a)²/12; probabilities are length ratios.", "Exponential(λ): P(X > t) = e^(−λt), mean 1/λ, memoryless.", "Normal: standardise with z = (x − μ)/σ and read Φ; Φ(−z) = 1 − Φ(z).", "68–95–99.7 rule for ±1σ, ±2σ, ±3σ.", "Sums of independent normals are normal: means and variances add."],
         subs=["Continuous distributions"])

# ------------------------------------------------------------------------------------------------ 12.5
A.lesson("engm-pb-stats", "Mean, median, mode and standard deviation",
         key="For data, the mean is the average, the median is the middle value of the sorted list and the mode is the most frequent value. The variance is the average squared deviation from the mean and the standard deviation its square root. Shifting data moves the centre, scaling data scales the spread.",
         analogy=("📊", "Summing up a class", "One number for the typical mark (mean or median) and one number for how scattered the marks are (standard deviation)."),
         defs=[("Mean", "The sum of the values divided by their number."),
               ("Median", "The middle value of the sorted data; the average of the two middle values when the count is even."),
               ("Mode", "The most frequent value."),
               ("Standard deviation", "The square root of the average squared deviation from the mean.")],
         parts=[dict(h="Measures of centre", md="""- **Mean** x̄ = (x₁ + … + xₙ)/n. It uses every value and is sensitive to outliers.
- **Median:** sort the data; the middle value for odd n, the average of the two middle values for even n. It is robust to outliers.
- **Mode:** the most frequent value; there may be several, or none.

For a symmetric distribution mean = median = mode; for right-skewed data typically mean > median > mode. For moderately skewed data, mode ≈ 3·median − 2·mean."""),
                 dict(h="Measures of spread", md="""- **Range** = maximum − minimum.
- **Variance** σ² = Σ(xᵢ − x̄)²/n = (Σxᵢ²)/n − x̄². (The *sample* variance divides by n − 1; the question says which.)
- **Standard deviation** σ = √σ².

If yᵢ = a·xᵢ + b, then ȳ = a·x̄ + b, the median and mode transform the same way, and σ_y = |a|·σ_x: adding b does not change the spread."""),
                 dict(h="Grouped data and combined groups", md="""For values xᵢ with frequencies fᵢ: x̄ = Σfᵢxᵢ/Σfᵢ. The mean of two combined groups is the weighted mean (n₁x̄₁ + n₂x̄₂)/(n₁ + n₂). The correlation r = Cov(X, Y)/(σ_Xσ_Y) lies in [−1, 1] and measures linear association; regression of y on x has slope r·σ_y/σ_x.""")],
         examples=[
             Ex("Mean, median, mode", "Find the mean, median and mode of 4, 8, 6, 5, 3, 8, 7.", ["Sum 41 with n = 7: mean 41/7.", "Sorted: 3 4 5 6 7 8 8, so the median is 6.", "8 occurs twice: mode 8."], "Mean **41/7 ≈ 5.86**, median **6**, mode **8**.", verify=lambda: "Mean %s ≈ %.2f, median %d, mode %d" % (F(41, 7), 41 / 7, sorted([4, 8, 6, 5, 3, 8, 7])[3], 8)),
             Ex("Variance", "Find the population variance and standard deviation of 2, 4, 4, 4, 5, 5, 7, 9.", ["Mean 40/8 = 5. Squared deviations: 9, 1, 1, 1, 0, 0, 4, 16: sum 32.", "Variance 32/8 = 4."], "Variance **4**, standard deviation **2**.", verify=lambda: "Variance %d, standard deviation %d" % (sum((x - 5) ** 2 for x in [2, 4, 4, 4, 5, 5, 7, 9]) // 8, 2)),
             Ex("A transformation", "Data have mean 20 and standard deviation 5. Every value is doubled and then 3 is subtracted. Find the new mean and standard deviation.", ["Mean 2·20 − 3 = 37.", "Standard deviation 2·5 = 10; subtracting 3 does not change the spread."], "Mean **37**, standard deviation **10**.", verify=lambda: "Mean %d, standard deviation %d" % (2 * 20 - 3, 2 * 5)),
             Ex("Combined mean", "Group A has 10 students with mean 60; group B has 30 students with mean 80. Find the combined mean.", ["(10·60 + 30·80)/40 = 3000/40."], "**75**", verify=lambda: str((10 * 60 + 30 * 80) // 40)),
             Ex("GATE style: median of an even count", "Find the median of 1, 3, 3, 7, 10, 12.", ["n = 6: average the middle values 3 and 7."], "**5**", verify=lambda: str((3 + 7) / 2))],
         traps=[("Median of an even count", "Average the two middle values."),
                ("Population versus sample variance", "Divide by n or n − 1 as the question states."),
                ("Standard deviation under scaling", "Multiply by |a|; adding b changes nothing."),
                ("Outliers", "They move the mean much more than the median.")],
         quick=[("Median of 1, 3, 3, 7, 10, 12", ["3", "5", "6", "7"], 1, "(3 + 7)/2."),
                ("Adding 5 to every value changes the standard deviation by", ["+5", "×5", "nothing", "+25"], 2, "A shift does not change the spread."),
                ("Which measure is most affected by an outlier?", ["mean", "median", "mode", "none"], 0, "The mean uses every value."),
                ("Variance of 3, 3, 3, 3", ["0", "3", "9", "1"], 0, "No spread.")],
         summary=["Mean = Σx/n; median = middle of the sorted data; mode = most frequent value.", "Variance = Σ(x − x̄)²/n = mean of squares − square of the mean.", "Standard deviation = √variance; range = maximum − minimum.", "Adding c shifts the mean, median and mode by c and leaves the spread unchanged; multiplying by a scales the spread by |a|.", "The combined mean of two groups is the weighted mean."],
         subs=["Descriptive statistics"])
