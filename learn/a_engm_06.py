"""Engineering Mathematics · Chapter 6 Combinatorics & Recurrences."""
import itertools
import math

from learn import Ex
from learn.author import Author

A = Author("ENGM")
A.chapter("Combinatorics & Recurrences")
C = math.comb


def derangements(n):
    d = [1, 0]
    for k in range(2, n + 1):
        d.append((k - 1) * (d[-1] + d[-2]))
    return d[n]


# ------------------------------------------------------------------------------------------------ 6.1
A.lesson("engm-counting-basics", "Counting rules, permutations and combinations",
         key="Multiply the number of choices for independent stages and add the counts of disjoint cases. Selecting k of n objects in order is a permutation P(n, k); selecting them without regard to order is a combination C(n, k). Always decide first whether order matters.",
         analogy=("🍽️", "Planning a menu", "Choosing a starter, a main and a dessert multiplies the options. Choosing the order in which three runners finish is a ranking (a permutation); choosing which three runners go to the finals is a selection (a combination)."),
         defs=[("Product rule", "If a task has k stages with n₁, …, n_k choices, there are n₁·n₂⋯n_k outcomes."),
               ("Sum rule", "If a task can be done in one of several mutually exclusive ways, add the counts of the ways."),
               ("Permutation P(n, k)", "An ordered selection of k distinct objects from n: n!/(n − k)!."),
               ("Combination C(n, k)", "An unordered selection of k objects from n: n!/(k!(n − k)!).")],
         parts=[dict(h="The two basic rules", md="""**Product rule (AND).** A licence plate with 2 letters then 3 digits has 26·26·10·10·10 possibilities. The choices must be independent stages.

**Sum rule (OR).** A committee chairperson may be a man (8 ways) or a woman (5 ways): 13 ways. The cases must not overlap; if they do, subtract the overlap (inclusion–exclusion, see 2.2).

**Complement.** When "at least one" is hard to count, count the opposite and subtract from the total."""),
                 dict(h="Permutations and combinations", md="""Ordered selection of k distinct objects from n: $P(n,k) = n(n-1)\\cdots(n-k+1) = \\dfrac{n!}{(n-k)!}$. In particular n! arrangements of all n objects.

Unordered selection: $C(n,k)=\\dbinom nk=\\dfrac{n!}{k!\\,(n-k)!}=\\dfrac{P(n,k)}{k!}$. Each unordered set of k objects can be ordered in k! ways, which is why dividing by k! converts a permutation count into a combination count.

Symmetry and Pascal: C(n, k) = C(n, n − k), and C(n, k) = C(n − 1, k − 1) + C(n − 1, k) (choose a special element or not)."""),
                 dict(h="Choosing the right tool", md="""1. Does **order** matter? (positions, ranks, passwords: yes; committees, hands of cards: no.)
2. Are repetitions allowed? (digits of a PIN: yes; distinct runners: no.)
3. Are there **conditions**? Handle them first: "must include" fixes some choices; "at least one" is a complement; "together" glues objects into a block.

Examples: PINs of 4 digits with repetition allowed: 10⁴; with all digits different: P(10, 4) = 5040; a 4-person committee from 10: C(10, 4) = 210.""")],
         examples=[
             Ex("Product rule", "How many 3-letter words (not necessarily meaningful) can be formed using distinct letters from the 26-letter alphabet?", ["Ordered selection without repetition: 26·25·24."], "**15600**", verify=lambda: str(math.perm(26, 3))),
             Ex("Ordered versus unordered", "From 8 runners, in how many ways can gold, silver and bronze be awarded, and in how many ways can 3 finalists be chosen?", ["Medals (ordered): P(8, 3) = 336.", "Finalists (unordered): C(8, 3) = 56."], "**336** and **56**.", verify=lambda: "%d and %d" % (math.perm(8, 3), C(8, 3))),
             Ex("At least one", "A committee of 4 is chosen from 6 men and 5 women and must contain at least one woman. How many committees?", ["All committees: C(11, 4) = 330.", "Committees of men only: C(6, 4) = 15.", "330 − 15."], "**315**", verify=lambda: str(C(11, 4) - C(6, 4))),
             Ex("A sum of cases", "How many 5-card hands from a 52-card deck contain exactly 2 aces?", ["Choose the 2 aces from 4: C(4, 2) = 6.", "Choose the 3 other cards from the 48 non-aces: C(48, 3) = 17296."], "**103776**", verify=lambda: str(C(4, 2) * C(48, 3))),
             Ex("GATE style: conditions", "How many 4-digit numbers (first digit non-zero) have all digits different?", ["First digit: 9 choices (1–9). The remaining digits come from 9, 8, 7 unused digits (zero is now allowed)."], "**4536**", verify=lambda: str(9 * 9 * 8 * 7))],
         traps=[("Order", "Decide whether order matters before choosing P or C."),
                ("Overlapping cases", "The sum rule needs disjoint cases; subtract overlaps."),
                ("Leading zero", "A number cannot start with 0; fix the first digit first."),
                ("Dividing by k!", "C(n, k) = P(n, k)/k!, not P(n, k)·k!.")],
         quick=[("P(7, 2)", ["21", "42", "49", "14"], 1, "7·6."),
                ("C(10, 8)", ["45", "90", "80", "10"], 0, "C(10, 2)."),
                ("Ways to rank the top 3 of 10 contestants", ["120", "720", "1000", "30"], 1, "P(10, 3)."),
                ("Committees of 3 from 7 people", ["21", "35", "42", "210"], 1, "C(7, 3).")],
         summary=["Product rule for independent stages (AND); sum rule for disjoint cases (OR).", "P(n, k) = n!/(n − k)! counts ordered selections; C(n, k) = P(n, k)/k! counts unordered ones.", "C(n, k) = C(n, n − k) and C(n, k) = C(n − 1, k − 1) + C(n − 1, k).", "For 'at least one', count the complement.", "Handle conditions (first digit, must include) before the free choices."],
         subs=["Counting"], widget="counting", hint="Pick n and k and compare ordered and unordered counts.")

# ------------------------------------------------------------------------------------------------ 6.2
A.lesson("engm-cb-arrange", "Arrangements with repetition and circular arrangements",
         key="Arranging n objects of which some are identical gives n!/(n₁!n₂!…). Around a circle divide by the n rotations: (n − 1)!, and by 2 again if the arrangement can be turned over. Position conditions ('together', 'never adjacent') are handled by gluing or by choosing gaps.",
         analogy=("💺", "Seating plans", "A round table has no head seat, so rotating everyone gives the same plan. Letters in a word are different only if you can tell them apart, so identical letters swapped give the same word."),
         defs=[("Multiset permutation", "An arrangement in a row of objects of which some are identical: n!/(n₁!n₂!⋯n_k!)."),
               ("Circular arrangement", "An arrangement around a circle in which rotations count as the same arrangement."),
               ("Necklace", "A circular arrangement of beads that may also be turned over, so reflections count as the same.")],
         parts=[dict(h="Arrangements of repeated objects", md="""Arrange n objects of which n₁ are of one kind, n₂ of another, …: the n! orderings count each distinct arrangement n₁!·n₂!⋯ times (once for every reshuffle of identical objects), so

$$\\frac{n!}{n_1!\\,n_2!\\cdots n_k!}.$$

MISSISSIPPI has 11 letters (I×4, S×4, P×2, M×1): 11!/(4!·4!·2!) = 34650 arrangements. If a condition fixes some letters, remove them first and count the rest."""),
                 dict(h="Circular arrangements and necklaces", md="""For n distinct people at a round table, fix one person's seat to remove the n rotations: **(n − 1)!**. If clockwise and anticlockwise are also considered the same (a necklace or garland, n ≥ 3), halve: **(n − 1)!/2**. If some people must sit together or apart, glue or place them after fixing the circle."""),
                 dict(h="Position conditions", md="""- **Together:** glue the k people into one block. The block and the other n − k objects form n − k + 1 units, arranged in (n − k + 1)! ways, and the block's members in k! ways inside: (n − k + 1)!·k!.
- **Never adjacent:** place the others first, then put the restricted objects into the gaps. For m boys in a row there are m + 1 gaps; k girls with no two adjacent: m!·P(m + 1, k).
- **A fixed relative order of k objects:** divide by k!.
- **Subtract** the unwanted arrangements from the total when that is simpler: two people not adjacent = total − (arrangements with them together).""")],
         examples=[
             Ex("Repeated letters", "How many distinct arrangements of the letters of BANANA are there?", ["6 letters: B once, A three times, N twice.", "6!/(3!·2!) = 720/12."], "**60**", verify=lambda: str(math.factorial(6) // (math.factorial(3) * math.factorial(2)))),
             Ex("Circular seating", "In how many ways can 7 people sit around a round table?", ["Fix one person; arrange the other six: 6!."], "**720**", verify=lambda: str(math.factorial(6))),
             Ex("Together", "In how many ways can 6 people stand in a row if two particular people must stand together?", ["Glue them: 5 units, 5! ways; the pair inside: 2! ways."], "**240**", verify=lambda: str(math.factorial(5) * 2)),
             Ex("Not adjacent", "4 boys and 3 girls stand in a row with no two girls adjacent. How many arrangements?", ["Arrange the boys: 4! = 24 ways, leaving 5 gaps.", "Choose and order 3 gaps for the girls: P(5, 3) = 60."], "**1440**", verify=lambda: str(math.factorial(4) * math.perm(5, 3))),
             Ex("GATE style: necklace", "How many different necklaces can be made from 6 distinct beads if rotations and flips give the same necklace?", ["(6 − 1)!/2 = 120/2."], "**60**", verify=lambda: str(math.factorial(5) // 2))],
         traps=[("Forgetting identical objects", "Divide by the factorial of each repeated count."),
                ("Circular versus linear", "Around a table there are (n − 1)! plans, not n!."),
                ("Necklaces", "Flipping the necklace halves the count (for n ≥ 3)."),
                ("Gluing", "Do not forget the arrangements inside the glued block.")],
         quick=[("Distinct arrangements of LEVEL", ["30", "60", "120", "5"], 1, "5!/(2!·2!)."),
                ("Circular arrangements of 5 distinct people", ["24", "120", "60", "12"], 0, "4!."),
                ("Arrangements of 5 people in a row with two named people together", ["24", "48", "60", "120"], 1, "4!·2."),
                ("Necklaces from 5 distinct beads", ["12", "24", "60", "120"], 0, "4!/2.")],
         summary=["n objects with repeats: n!/(n₁!n₂!⋯).", "Circular arrangement: (n − 1)!; necklace: (n − 1)!/2.", "'Together': glue, then multiply by the arrangements inside the block.", "'Never adjacent': place the others, then choose gaps.", "Total minus the bad arrangements is often the simplest route."],
         subs=["Arrangements"])

# ------------------------------------------------------------------------------------------------ 6.3
A.lesson("engm-cb-methods", "Distributing objects: stars and bars",
         key="Placing n identical objects into k distinct boxes is the same as counting the non-negative integer solutions of x₁ + … + x_k = n, which is C(n + k − 1, k − 1). Lower bounds are handled by substitution and upper bounds by inclusion–exclusion.",
         analogy=("⭐", "Stars and bars", "Write the n objects as stars in a row and insert k − 1 bars to split them into k boxes. Every arrangement of n stars and k − 1 bars is a distribution, so we count positions for the bars."),
         defs=[("Stars and bars", "The bijection between distributions of n identical objects into k boxes and arrangements of n stars and k − 1 bars."),
               ("Composition", "An ordered list of positive integers with a given sum; counted by C(n − 1, k − 1) when it has k parts.")],
         parts=[dict(h="The basic count", md="""The number of non-negative integer solutions of x₁ + x₂ + … + x_k = n is

$$\\binom{n+k-1}{k-1}.$$

Reason: lay out n stars and k − 1 bars, n + k − 1 positions in all; choose which k − 1 positions hold bars. For example x + y + z = 6 has C(8, 2) = 28 solutions."""),
                 dict(h="Conditions on the variables", md="""- **Positive solutions** (each xᵢ ≥ 1): put yᵢ = xᵢ − 1 ≥ 0; then Σyᵢ = n − k and the count is C(n − 1, k − 1).
- **Lower bounds** xᵢ ≥ mᵢ: substitute xᵢ = yᵢ + mᵢ and reduce n by Σmᵢ.
- **Upper bounds** xᵢ ≤ uᵢ: count without the bound, then subtract the solutions that violate it (inclusion–exclusion): xᵢ ≥ uᵢ + 1 is a lower-bound problem.
- **Inequality** x₁ + … + x_k ≤ n: add a slack variable, giving C(n + k, k).
- **Distinct objects** into k boxes are a different problem: kⁿ ways."""),
                 dict(h="Recognising the model", md="""Words that signal stars and bars: "identical balls", "number of solutions", "non-negative integers", "distribute n similar items". Words that do not: "different books", "labelled people" (use powers k^n), and "each box gets at least one distinct item".""")],
         examples=[
             Ex("Non-negative solutions", "How many non-negative integer solutions does x₁ + x₂ + x₃ + x₄ = 12 have?", ["n = 12, k = 4: C(12 + 3, 3) = C(15, 3)."], "**455**", verify=lambda: str(C(15, 3))),
             Ex("Positive solutions", "How many solutions in positive integers does x + y + z = 10 have?", ["Substitute yᵢ = xᵢ − 1: the sum becomes 7, so C(7 + 2, 2) = C(9, 2)."], "**36**", verify=lambda: str(C(9, 2))),
             Ex("A lower bound", "How many non-negative integer solutions does x + y + z = 15 have with x ≥ 4?", ["Put x = x′ + 4, x′ ≥ 0: x′ + y + z = 11.", "C(13, 2)."], "**78**", verify=lambda: str(C(13, 2))),
             Ex("An upper bound", "How many non-negative solutions of x + y + z = 10 have each variable at most 6?", ["Total: C(12, 2) = 66.", "Solutions with x ≥ 7: substitute x = x′ + 7: C(5, 2) = 10; the same for y and z. No two variables can be ≥ 7 together (14 > 10).", "66 − 3·10."], "**36**", verify=lambda: str(sum(1 for x in range(11) for y in range(11) for z in range(11) if x + y + z == 10 and max(x, y, z) <= 6))),
             Ex("GATE style: balls and boxes", "In how many ways can 10 identical balls be placed in 4 distinct boxes so that no box is empty?", ["Positive solutions of x₁ + … + x₄ = 10: C(9, 3)."], "**84**", verify=lambda: str(C(9, 3)))],
         traps=[("Positive versus non-negative", "For xᵢ ≥ 1 use C(n − 1, k − 1), not C(n + k − 1, k − 1)."),
                ("Distinct objects", "Stars and bars is for identical objects; distinct objects give kⁿ."),
                ("Upper bounds", "Use inclusion–exclusion; do not just subtract the bound."),
                ("Inequality", "A ≤ constraint needs one extra slack variable.")],
         quick=[("Non-negative solutions of x + y + z = 6", ["15", "28", "36", "56"], 1, "C(8, 2)."),
                ("Positive solutions of x + y + z = 7", ["15", "21", "36", "6"], 0, "C(6, 2)."),
                ("Ways to put 5 identical balls into 3 boxes", ["10", "15", "21", "243"], 2, "C(7, 2)."),
                ("Ways to put 5 different balls into 3 boxes", ["21", "125", "243", "15"], 2, "3⁵.")],
         summary=["Non-negative solutions of x₁ + … + x_k = n: C(n + k − 1, k − 1).", "Positive solutions: C(n − 1, k − 1).", "A lower bound xᵢ ≥ m: substitute xᵢ = yᵢ + m.", "Upper bounds use inclusion–exclusion; inequalities add a slack variable.", "Distinct objects into k boxes: kⁿ."],
         subs=["Counting techniques"])

# ------------------------------------------------------------------------------------------------ 6.4
A.lesson("engm-cb-binomial", "Binomial theorem and lattice paths",
         key="(x + y)ⁿ expands as Σ C(n, k)xⁿ⁻ᵏyᵏ. The coefficients obey Pascal's identity and add up to 2ⁿ. A shortest lattice path from (0, 0) to (a, b) is a word of a right-steps and b up-steps, so there are C(a + b, a) of them.",
         analogy=("🔺", "Pascal's triangle", "Each entry is the sum of the two above it, and row n lists the coefficients of (x + y)ⁿ. The same numbers count the ways to walk down the triangle."),
         defs=[("Binomial coefficient C(n, k)", "The number of k-element subsets of an n-set; the coefficient of xᵏ in (1 + x)ⁿ."),
               ("Lattice path", "A path on the integer grid using unit steps right (R) and up (U)."),
               ("Catalan number Cₙ", "C(2n, n)/(n + 1); the number of lattice paths from (0, 0) to (n, n) that never rise above the diagonal.")],
         parts=[dict(h="The binomial theorem", md="""$$(x+y)^n=\\sum_{k=0}^{n}\\binom nk x^{n-k}y^{k}.$$

Choose which k of the n factors contribute y; the others contribute x. The (k + 1)-th term is C(n, k)xⁿ⁻ᵏyᵏ. For (ax + by)ⁿ the term is C(n, k)aⁿ⁻ᵏbᵏxⁿ⁻ᵏyᵏ. To extract a coefficient, set the power of x and read k. A constant term arises when the powers of x cancel: in (x + 1/x)ⁿ the term C(n, k)xⁿ⁻²ᵏ is constant for k = n/2."""),
                 dict(h="Identities", md="""- Σₖ C(n, k) = 2ⁿ (put x = y = 1) and Σₖ (−1)ᵏC(n, k) = 0 for n ≥ 1 (put x = 1, y = −1).
- Σₖ k·C(n, k) = n·2ⁿ⁻¹.
- Pascal: C(n, k) = C(n − 1, k − 1) + C(n − 1, k).
- Vandermonde: Σₖ C(m, k)C(n, r − k) = C(m + n, r).
- Hockey stick: Σᵢ₌ᵣⁿ C(i, r) = C(n + 1, r + 1).
- The sum of the coefficients of a polynomial p(x) is p(1)."""),
                 dict(h="Lattice paths", md="""A shortest path from (0, 0) to (a, b) has a right-steps and b up-steps in some order: **C(a + b, a)** paths. Passing through (c, d) multiplies the counts of the two legs: C(c + d, c)·C(a + b − c − d, a − c). Avoiding a point subtracts the paths through it. Paths that stay on or below the diagonal from (0, 0) to (n, n) are counted by the Catalan number C(2n, n)/(n + 1): 1, 1, 2, 5, 14, 42, …""")],
         examples=[
             Ex("A coefficient", "Find the coefficient of x²y³ in (2x + 3y)⁵.", ["C(5, 3)·2²·3³ = 10·4·27."], "**1080**", verify=lambda: str(C(5, 3) * 2 ** 2 * 3 ** 3)),
             Ex("A constant term", "Find the constant term in the expansion of (x + 1/x)⁶.", ["The term C(6, k)x^(6 − 2k) is constant for k = 3."], "**20**", verify=lambda: str(C(6, 3))),
             Ex("Sum of coefficients", "Find the sum of the coefficients of (2x − 1)⁷.", ["Set x = 1: (2 − 1)⁷."], "**1**", verify=lambda: str((2 - 1) ** 7)),
             Ex("Lattice paths", "How many shortest right/up paths lead from (0, 0) to (5, 3)?", ["8 steps, 5 of them right: C(8, 5)."], "**56**", verify=lambda: str(C(8, 5))),
             Ex("GATE style: through a point", "How many shortest right/up lattice paths go from (0, 0) to (6, 4) passing through (2, 2)?", ["Paths to (2, 2): C(4, 2) = 6.", "Paths from (2, 2) to (6, 4): 4 right, 2 up: C(6, 2) = 15.", "6·15."], "**90**", verify=lambda: str(C(4, 2) * C(6, 2)))],
         traps=[("Forgetting the constants in (ax + by)ⁿ", "The term carries aⁿ⁻ᵏbᵏ as well as C(n, k)."),
                ("Alternating sum", "Σ(−1)ᵏC(n, k) is 0, not 2ⁿ."),
                ("Path counts", "Count steps, not grid squares: (a, b) needs a + b steps."),
                ("Through a point", "Multiply the two legs; do not add them.")],
         quick=[("Coefficient of x² in (1 + x)⁵", ["5", "10", "20", "1"], 1, "C(5, 2)."),
                ("Shortest right/up paths from (0,0) to (2,2)", ["4", "6", "8", "2"], 1, "C(4, 2)."),
                ("Σ C(8, k) for k = 0..8", ["64", "128", "256", "512"], 2, "2⁸."),
                ("Sum of the coefficients of (x + 2)⁴", ["16", "64", "81", "256"], 2, "Put x = 1: 3⁴.")],
         summary=["(x + y)ⁿ = Σ C(n, k)xⁿ⁻ᵏyᵏ; Σ C(n, k) = 2ⁿ and Σ (−1)ᵏC(n, k) = 0.", "Pascal: C(n, k) = C(n − 1, k − 1) + C(n − 1, k).", "Sum of the coefficients of p(x) is p(1).", "Shortest lattice paths to (a, b): C(a + b, a); through a point, multiply the legs.", "Catalan numbers count paths that never cross the diagonal."],
         subs=["Binomial coefficients"])

# ------------------------------------------------------------------------------------------------ 6.5
A.lesson("engm-cb-derange", "Inclusion–exclusion and derangements",
         key="Inclusion–exclusion counts arrangements that avoid every bad property by alternately adding and subtracting overlaps. Its best-known case is the derangement number Dₙ, the permutations with no fixed point: Dₙ = n!·Σ(−1)ᵏ/k! ≈ n!/e.",
         analogy=("✉️", "Letters in the wrong envelopes", "A secretary stuffs n letters into n addressed envelopes at random. A derangement is a stuffing in which no letter lands in its own envelope."),
         defs=[("Derangement", "A permutation with no fixed point; Dₙ is the number of derangements of n objects."),
               ("Fixed point", "An element that the permutation maps to itself."),
               ("Bad property", "A condition Pᵢ to be avoided; the set Aᵢ is the set of arrangements that have Pᵢ.")],
         parts=[dict(h="Counting arrangements that avoid every property", md="""If Aᵢ is the set of arrangements with bad property i, the number with **none** of them is

$$N-\\sum|A_i|+\\sum|A_i\\cap A_j|-\\sum|A_i\\cap A_j\\cap A_k|+\\cdots$$

For symmetric problems every intersection of j sets has the same size, so the terms are C(k, j)·(common size). Example: permutations of n objects with no fixed point. The set Aᵢ (object i fixed) has (n − 1)! elements, an intersection of j of them has (n − j)!, so

$$D_n=\\sum_{j=0}^{n}(-1)^j\\binom nj (n-j)! = n!\\sum_{j=0}^n\\frac{(-1)^j}{j!}.$$"""),
                 dict(h="Derangement numbers", md="""D₀ = 1, D₁ = 0, D₂ = 1, D₃ = 2, D₄ = 9, D₅ = 44, D₆ = 265, D₇ = 1854. The recurrences are

- Dₙ = (n − 1)(Dₙ₋₁ + Dₙ₋₂);
- Dₙ = n·Dₙ₋₁ + (−1)ⁿ.

Dₙ is the nearest integer to n!/e, and the probability that a random permutation has no fixed point tends to 1/e ≈ 0.368. The number of permutations with exactly k fixed points is C(n, k)·Dₙ₋ₖ (choose the fixed points, derange the rest)."""),
                 dict(h="Other uses", md="""**Onto functions.** The number of onto functions from an m-set to an n-set is Σ(−1)ʲC(n, j)(n − j)ᵐ.

**Integers coprime to n.** The numbers in 1..n divisible by none of the primes p₁, …, p_k dividing n number n·Π(1 − 1/pᵢ) = φ(n).

**Bounded solutions.** Solutions of x₁ + … + x_k = n with an upper bound on each variable: subtract those violating a bound, add back double violations, and so on.""")],
         examples=[
             Ex("Derangements", "How many derangements of 5 objects are there?", ["Use D₅ = 4(D₄ + D₃) = 4(9 + 2)."], "**44**", verify=lambda: str(derangements(5))),
             Ex("Exactly k fixed points", "In how many permutations of 6 objects are exactly 2 objects fixed?", ["Choose the 2 fixed objects: C(6, 2) = 15.", "Derange the other 4: D₄ = 9."], "**135**", verify=lambda: str(C(6, 2) * derangements(4))),
             Ex("At least one fixed point", "In how many permutations of 5 objects is at least one object fixed?", ["Total 5! = 120 minus the derangements D₅ = 44."], "**76**", verify=lambda: str(math.factorial(5) - derangements(5))),
             Ex("Integers avoiding three primes", "How many integers from 1 to 210 are divisible by none of 2, 3, 5 and 7?", ["210·(1/2)(2/3)(4/5)(6/7) = φ(210)."], "**48**", verify=lambda: str(sum(1 for k in range(1, 211) if all(k % p for p in (2, 3, 5, 7))))),
             Ex("GATE style: onto functions", "How many onto functions are there from a 4-element set to a 3-element set?", ["3⁴ − C(3, 1)·2⁴ + C(3, 2)·1⁴ = 81 − 48 + 3."], "**36**", verify=lambda: str(3 ** 4 - 3 * 2 ** 4 + 3))],
         traps=[("Signs", "Alternate: subtract single violations, add pairs, subtract triples."),
                ("Dₙ recurrence", "Dₙ = (n − 1)(Dₙ₋₁ + Dₙ₋₂), not n·Dₙ₋₁."),
                ("Exactly k fixed", "Multiply by C(n, k) before the derangement of the rest."),
                ("Fixed point probability", "The limit 1/e is for no fixed point, not at least one.")],
         quick=[("D₄", ["6", "9", "12", "24"], 1, "9."),
                ("Permutations of 4 objects with no fixed point", ["9", "12", "14", "15"], 0, "D₄."),
                ("Onto functions from a 3-set to a 2-set", ["2", "6", "8", "9"], 1, "2³ − 2."),
                ("The probability that a random permutation has no fixed point tends to", ["1/2", "1/e", "1/n", "0"], 1, "Dₙ/n! → 1/e.")],
         summary=["Inclusion–exclusion alternates signs over intersections of the bad sets.", "Dₙ = n!·Σ(−1)ʲ/j! and Dₙ = (n − 1)(Dₙ₋₁ + Dₙ₋₂): 1, 0, 1, 2, 9, 44, 265.", "Exactly k fixed points: C(n, k)·Dₙ₋ₖ.", "Onto functions are inclusion–exclusion over the missed outputs.", "φ(n) counts integers up to n avoiding every prime factor."],
         subs=["Derangements & exclusion"])

# ------------------------------------------------------------------------------------------------ 6.6
A.lesson("engm-cb-pigeonhole", "Pigeonhole principle",
         key="If more than n objects go into n boxes, some box holds at least two. More generally some box holds at least ⌈m/n⌉ of m objects, and n(k − 1) + 1 objects guarantee k in one box. The principle proves existence; it never says which box.",
         analogy=("🕊️", "More pigeons than holes", "If 13 pigeons fly into 12 holes, some hole receives two pigeons. You cannot say which hole, only that one must."),
         defs=[("Pigeonhole principle", "If more than n objects are placed in n boxes, some box contains at least two objects."),
               ("Generalised pigeonhole principle", "If m objects are placed in n boxes, some box contains at least ⌈m/n⌉ objects.")],
         parts=[dict(h="The principle", md="""**Basic form.** n + 1 objects into n boxes: some box has at least 2.

**General form.** m objects into n boxes: some box has at least ⌈m/n⌉. To *guarantee* k objects in one box you need n(k − 1) + 1 objects, because n(k − 1) objects can still be spread with k − 1 in each box.

Proof of the general form: if every box held at most ⌈m/n⌉ − 1 < m/n objects, the total would be less than m."""),
                 dict(h="Using it", md="""1. Decide what the **objects** are and what the **boxes** are (categories into which each object falls).
2. Count the boxes n.
3. The worst case puts k − 1 objects in each box, so n(k − 1) + 1 objects force k in one box.

Typical boxes: remainders mod n (n boxes), birthdays/months (12), suits (4), colours of socks, pairs, parity classes. Example: among any 5 integers two have the same remainder mod 4."""),
                 dict(h="Classic applications", md="""- Among any n + 1 integers two have a difference divisible by n.
- In any group of 2 or more people two have the same number of friends within the group.
- Among 5 points in a unit square two are at distance at most √2/2 (divide into four small squares).
- A sequence of n² + 1 distinct numbers contains an increasing or decreasing subsequence of length n + 1 (Erdős–Szekeres).""")],
         examples=[
             Ex("Birth months", "How many people guarantee that two share a birth month?", ["12 months: 12 + 1."], "**13**", verify=lambda: str(12 + 1)),
             Ex("Guarantee k", "How many cards must be drawn from a 52-card deck to guarantee 3 of the same suit?", ["4 suits: 4(3 − 1) + 1."], "**9**", verify=lambda: str(4 * 2 + 1)),
             Ex("Remainders", "How many integers guarantee that two of them have the same remainder on division by 7?", ["7 boxes: 7 + 1."], "**8**", verify=lambda: str(7 + 1)),
             Ex("The general form", "21 objects are placed in 5 boxes. At least how many objects must some box contain?", ["⌈21/5⌉ = 5."], "**5**", verify=lambda: str(-(-21 // 5))),
             Ex("GATE style: socks", "A drawer has 10 black, 8 white and 6 blue socks. How many must be drawn in the dark to be sure of a matching pair, and to be sure of 2 black socks?", ["Pair: 3 colours, so 3 + 1 = 4.", "Two black: in the worst case draw all 8 white and 6 blue first: 14 + 2."], "**4** and **16**.", verify=lambda: "%d and %d" % (3 + 1, 8 + 6 + 2))],
         traps=[("Existence only", "It says some box has many objects, not which one."),
                ("Off by one", "n(k − 1) + 1, not nk."),
                ("Choosing the boxes", "The boxes must be categories every object falls into."),
                ("Worst case", "Guarantees assume the unluckiest draw.")],
         quick=[("21 objects in 5 boxes: some box has at least", ["4", "5", "6", "21"], 1, "⌈21/5⌉ = 5."),
                ("Cards needed to guarantee 2 of one suit", ["5", "6", "13", "27"], 0, "4 + 1."),
                ("To guarantee 4 in one of 6 boxes you need", ["19", "24", "18", "25"], 0, "6·3 + 1."),
                ("Among any 11 integers, two have a difference divisible by", ["10", "11", "5", "2"], 0, "Ten remainders mod 10.")],
         summary=["n + 1 objects in n boxes force a box with two.", "m objects in n boxes force a box with at least ⌈m/n⌉.", "To guarantee k in a box you need n(k − 1) + 1 objects.", "Choose boxes as categories: remainders, suits, months, colours.", "It proves existence only."],
         subs=["Pigeonhole & advanced counting"])

# ------------------------------------------------------------------------------------------------ 6.7
A.lesson("engm-cb-recurrence", "Recurrence relations",
         key="A linear recurrence aₙ = c₁aₙ₋₁ + c₂aₙ₋₂ is solved through its characteristic equation r² = c₁r + c₂. Distinct roots give A r₁ⁿ + B r₂ⁿ, a repeated root gives (A + Bn)rⁿ, and the initial values fix A and B. Non-homogeneous terms add a particular solution.",
         analogy=("🌀", "Growth by a rule", "A recurrence is a rule that produces each term from earlier ones. Its characteristic roots are the natural growth rates of the sequence, and the starting values decide how much of each rate you get."),
         defs=[("Recurrence relation", "An equation expressing aₙ in terms of earlier terms, together with initial values."),
               ("Linear homogeneous recurrence with constant coefficients", "aₙ = c₁aₙ₋₁ + … + c_kaₙ₋ₖ with constants cᵢ."),
               ("Characteristic equation", "rᵏ = c₁rᵏ⁻¹ + … + c_k; its roots give the general solution.")],
         parts=[dict(h="Solving aₙ = c₁aₙ₋₁ + c₂aₙ₋₂", md="""1. Form the characteristic equation r² − c₁r − c₂ = 0 and find its roots.
2. If the roots r₁ ≠ r₂ are distinct: aₙ = A·r₁ⁿ + B·r₂ⁿ. If r₁ = r₂ = r: aₙ = (A + B·n)·rⁿ. For complex roots r = ρe^{±iθ}: aₙ = ρⁿ(A cos nθ + B sin nθ).
3. Use a₀ and a₁ to solve for A and B.
4. Check against the first few terms computed from the recurrence.

Example: aₙ = 5aₙ₋₁ − 6aₙ₋₂ has r² − 5r + 6 = (r − 2)(r − 3), roots 2 and 3, so aₙ = A·2ⁿ + B·3ⁿ."""),
                 dict(h="Non-homogeneous recurrences", md="""For aₙ = c₁aₙ₋₁ + c₂aₙ₋₂ + f(n), the general solution is the homogeneous solution plus any particular solution. Trial forms for the particular solution: f(n) constant → a constant; f(n) = n → an + b; f(n) = sⁿ → C·sⁿ (use C·n·sⁿ if s is already a root).

Famous examples: Tower of Hanoi, aₙ = 2aₙ₋₁ + 1 with a₁ = 1, has solution 2ⁿ − 1. Fibonacci, Fₙ = Fₙ₋₁ + Fₙ₋₂, has roots (1 ± √5)/2, and the growth rate φ = (1 + √5)/2 ≈ 1.618."""),
                 dict(h="Recurrences in algorithms", md="""For divide-and-conquer recurrences T(n) = aT(n/b) + f(n) compare n^(log_b a) with f(n) (Master theorem). T(n) = 2T(n/2) + n gives Θ(n log n); T(n) = T(n/2) + 1 gives Θ(log n); T(n) = T(n − 1) + n gives Θ(n²); T(n) = 2T(n − 1) + 1 gives Θ(2ⁿ).""")],
         examples=[
             Ex("Solve and evaluate", "aₙ = 3aₙ₋₁ − 2aₙ₋₂ with a₀ = 1, a₁ = 3. Find a₅.", ["Roots of r² − 3r + 2: 1 and 2, so aₙ = A + B·2ⁿ.", "A + B = 1 and A + 2B = 3 give B = 2, A = −1: aₙ = 2ⁿ⁺¹ − 1.", "a₅ = 2⁶ − 1."], "**63**", verify=lambda: str(2 ** 6 - 1)),
             Ex("A repeated root", "aₙ = 4aₙ₋₁ − 4aₙ₋₂ with a₀ = 1, a₁ = 4. Find a₃.", ["Double root r = 2: aₙ = (A + Bn)2ⁿ.", "a₀ = A = 1; a₁ = 2(1 + B) = 4 gives B = 1.", "a₃ = (1 + 3)·8."], "**32**", verify=lambda: str((1 + 3) * 2 ** 3)),
             Ex("Tower of Hanoi", "T(n) = 2T(n − 1) + 1 with T(1) = 1. Find T(6).", ["T(n) = 2ⁿ − 1."], "**63**", verify=lambda: str(2 ** 6 - 1)),
             Ex("Fibonacci", "F₁ = F₂ = 1, Fₙ = Fₙ₋₁ + Fₙ₋₂. Find F₁₀.", ["1, 1, 2, 3, 5, 8, 13, 21, 34, 55."], "**55**", verify=lambda: str(55)),
             Ex("GATE style: characteristic roots", "Find the roots of the characteristic equation of aₙ = 6aₙ₋₁ − 9aₙ₋₂ and the form of the solution.", ["r² − 6r + 9 = (r − 3)².", "Double root 3."], "Root **3** (twice); aₙ = **(A + Bn)·3ⁿ**.", verify=lambda: "Root 3 (twice); aₙ = (A + Bn)·3ⁿ")],
         traps=[("Repeated roots", "Include the factor n: (A + Bn)rⁿ."),
                ("Initial values", "Use them to fix A and B."),
                ("Non-homogeneous", "Add a particular solution to the homogeneous one."),
                ("Indexing", "Check whether the sequence starts at n = 0 or n = 1.")],
         quick=[("Characteristic equation of aₙ = aₙ₋₁ + 2aₙ₋₂", ["r² − r − 2 = 0", "r² + r − 2 = 0", "r² − 2r − 1 = 0", "r² − 2 = 0"], 0, "r² = r + 2."),
                ("A double root r gives the general solution", ["A rⁿ", "(A + Bn) rⁿ", "A rⁿ + B r²ⁿ", "A n rⁿ"], 1, "An extra factor n."),
                ("T(n) = 2T(n − 1) + 1 grows like", ["n", "n²", "2ⁿ", "log n"], 2, "Doubling each step."),
                ("The Fibonacci growth rate is", ["1.5", "(1 + √5)/2", "2", "e"], 1, "The golden ratio.")],
         summary=["Solve r² = c₁r + c₂; distinct roots give Ar₁ⁿ + Br₂ⁿ, a double root gives (A + Bn)rⁿ.", "Initial values fix the constants.", "Non-homogeneous: add a particular solution.", "Hanoi: 2ⁿ − 1; Fibonacci grows like ((1 + √5)/2)ⁿ.", "Always verify against the first terms."],
         subs=["Recurrence relations"])

# ------------------------------------------------------------------------------------------------ 6.8
A.lesson("engm-cb-genfun", "Generating functions",
         key="A sequence a₀, a₁, a₂, … is packed into the power series Σaₙxⁿ. Multiplying series counts combined choices, 1/(1 − x)ᵏ counts stars-and-bars distributions, and the coefficient of xⁿ is the answer to a counting question.",
         analogy=("🧺", "A basket of choices", "Each factor lists how many of one kind of item you may take; multiplying the factors lists every combined basket, and the coefficient of xⁿ counts the baskets with exactly n items."),
         defs=[("Ordinary generating function", "For a sequence a₀, a₁, …, the formal power series A(x) = Σ aₙxⁿ."),
               ("Coefficient [xⁿ]A(x)", "The term aₙ, read off as the answer to a counting question.")],
         parts=[dict(h="Building a generating function", md="""For each kind of item write a polynomial whose exponents are the numbers you may take:

- usable 0, 1 or 2 times: 1 + x + x²;
- usable any number of times: 1 + x + x² + … = 1/(1 − x);
- usable at least once: x + x² + … = x/(1 − x);
- usable only in even numbers: 1 + x² + x⁴ + … = 1/(1 − x²).

Multiply the factors; the coefficient of xⁿ in the product is the number of selections with n items in total."""),
                 dict(h="Standard series", md="""| Generating function | Coefficient of xⁿ |
|---|---|
| 1/(1 − x) | 1 |
| 1/(1 − ax) | aⁿ |
| 1/(1 − x)ᵏ | C(n + k − 1, k − 1) |
| x/(1 − x)² | n |
| (1 + x)ᵐ | C(m, n) |
| eˣ (exponential generating function) | 1/n! |

Multiplying A(x)·B(x) gives the convolution Σ aᵢbₙ₋ᵢ; multiplying by 1/(1 − x) gives partial sums."""),
                 dict(h="From recurrences to closed forms", md="""To solve aₙ = c₁aₙ₋₁ + c₂aₙ₋₂ with generating functions, multiply by xⁿ and sum, giving A(x) = P(x)/(1 − c₁x − c₂x²) with P fixed by the initial values; then expand into partial fractions. The same method gives Fibonacci: Σ Fₙxⁿ = x/(1 − x − x²).""")],
         examples=[
             Ex("Limited supply", "In how many ways can 4 be written as a + b with 0 ≤ a ≤ 2 and 0 ≤ b ≤ 3?", ["The coefficient of x⁴ in (1 + x + x²)(1 + x + x² + x³).", "Pairs (1, 3) and (2, 2)."], "**2**", verify=lambda: str(sum(1 for a in range(3) for b in range(4) if a + b == 4))),
             Ex("Stars and bars by series", "Find the coefficient of x⁵ in 1/(1 − x)³.", ["C(5 + 2, 2)."], "**21**", verify=lambda: str(C(7, 2))),
             Ex("Two dice", "In how many ways can two dice total 9?", ["The coefficient of x⁹ in (x + x² + … + x⁶)²: pairs (3,6), (4,5), (5,4), (6,3)."], "**4**", verify=lambda: str(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 9))),
             Ex("A geometric series", "Find the coefficient of x³ in 1/(1 − 2x).", ["2³."], "**8**", verify=lambda: str(2 ** 3)),
             Ex("GATE style: coins", "In how many ways can 6 be paid with unlimited coins of 1, 2 and 3 (order ignored)?", ["The coefficient of x⁶ in 1/((1 − x)(1 − x²)(1 − x³)).", "Count partitions of 6 into parts at most 3: 7."], "**7**", verify=lambda: str(sum(1 for a in range(7) for b in range(4) for c in range(3) if a + 2 * b + 3 * c == 6)))],
         traps=[("Starting index", "x/(1 − x) starts at x¹, not x⁰."),
                ("Coefficient versus value", "The answer is a coefficient, not the value of the function."),
                ("Unlimited supply", "Use 1/(1 − x), not a finite polynomial."),
                ("Order of factors", "Multiply the factors of all item types, one factor per type.")],
         quick=[("Coefficient of x³ in 1/(1 − 2x)", ["3", "6", "8", "2"], 2, "2³."),
                ("1/(1 − x)² generates", ["1, 1, 1, …", "1, 2, 3, …", "1, 2, 4, …", "0, 1, 2, …"], 1, "aₙ = n + 1."),
                ("x/(1 − x) generates", ["1, 1, 1, …", "0, 1, 1, 1, …", "1, 2, 3, …", "0, 1, 2, …"], 1, "It starts at x¹."),
                ("Number of ways two dice total 7", ["5", "6", "7", "36"], 1, "Coefficient of x⁷.")],
         summary=["Each item type contributes a factor; the coefficient of xⁿ in the product counts selections of size n.", "1/(1 − x)ᵏ has coefficients C(n + k − 1, k − 1).", "1/(1 − ax) = Σaⁿxⁿ; x/(1 − x)² = Σ n xⁿ.", "Multiplying series convolves their coefficients.", "Recurrences turn into rational generating functions."],
         subs=["Generating functions"])
