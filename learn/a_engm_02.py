"""Engineering Mathematics · Chapter 2 Sets, Relations & Functions."""
import itertools
import math

from content import g_math2 as M2
from learn import Ex
from learn.author import Author

A = Author("ENGM")
A.chapter("Sets, Relations & Functions")
C = math.comb

# ------------------------------------------------------------------------------------------------ 2.1
A.lesson("engm-sets-counting", "Sets, subsets and power sets",
         key="A set is a collection of distinct objects. Union, intersection, difference and complement combine sets; the power set of an n-element set has 2ⁿ elements; and the Cartesian product A × B has |A|·|B| ordered pairs.",
         analogy=("🧺", "Baskets of labelled items", "A set is a basket where order and repeats do not matter, only membership. A subset is a smaller basket taken from it, and the power set is the collection of every such smaller basket."),
         defs=[("Set", "An unordered collection of distinct objects, called its elements."),
               ("Subset A ⊆ B", "Every element of A is an element of B; A is a proper subset if also A ≠ B."),
               ("Power set P(A)", "The set of all subsets of A, including ∅ and A; |P(A)| = 2ⁿ when |A| = n."),
               ("Cartesian product A × B", "The set of ordered pairs (a, b) with a ∈ A and b ∈ B.")],
         parts=[dict(h="Elements, subsets and the empty set", md="""Membership uses ∈ ("is an element of"); inclusion uses ⊆ ("is a subset of"). They are different things: 2 ∈ {1, 2, 3}, but {2} ⊆ {1, 2, 3}. The empty set ∅ has no elements and is a subset of every set; note that ∅ ≠ {∅}, because {∅} has one element.

Two sets are equal when they have the same elements, so A = B exactly when A ⊆ B and B ⊆ A. This two-way inclusion is the standard way to prove a set identity."""),
                 dict(h="Operations", md="""| Operation | Meaning |
|---|---|
| A ∪ B | in A or B or both |
| A ∩ B | in both |
| A − B | in A but not in B |
| Aᶜ | not in A (inside the universe U) |
| A Δ B | in exactly one of A, B |

Sizes: the number of elements of A ∪ B is |A| + |B| − |A ∩ B|; of A − B it is |A| − |A ∩ B|; of Aᶜ it is |U| − |A|; of A Δ B it is |A| + |B| − 2|A ∩ B|.

De Morgan's laws for sets: (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ and (A ∩ B)ᶜ = Aᶜ ∪ Bᶜ. Also A − B = A ∩ Bᶜ, and A ⊆ B ⇔ A ∪ B = B ⇔ A ∩ B = A."""),
                 dict(h="Power sets and products", md="""A subset of an n-element set is decided by saying yes or no to each element, so there are 2ⁿ of them, and C(n, k) of size k. Consequently

- |P(A)| = 2ⁿ, and P(A) ∩ P(B) = P(A ∩ B);
- |P(P(∅))| = 2, because P(∅) = {∅} has one element;
- |A × B| = |A|·|B|, and A × B ≠ B × A unless A = B or one of them is empty.

An element of A × B is an *ordered* pair: (1, 2) ≠ (2, 1)."""),
                 dict(h="Proving identities", md="""To prove X = Y, show x ∈ X ⇒ x ∈ Y and the reverse. Example: A − (B ∪ C) = (A − B) ∩ (A − C). If x ∈ A − (B ∪ C) then x ∈ A and x ∉ B and x ∉ C, which is exactly x ∈ A − B and x ∈ A − C. The steps are reversible, so the sets are equal.""")],
         examples=[
             Ex("Operations on small sets", "A = {1, 2, 3, 4, 5}, B = {4, 5, 6, 7}. Find |A ∪ B|, |A ∩ B|, |A − B| and |A Δ B|.", ["A ∩ B = {4, 5}, so 2.", "A ∪ B = {1, …, 7}: 5 + 4 − 2 = 7.", "A − B = {1, 2, 3}: 3.   A Δ B = {1, 2, 3, 6, 7}: 5."], "**7**, **2**, **3** and **5**.", verify=lambda: "%d, %d, %d and %d" % (len({1, 2, 3, 4, 5} | {4, 5, 6, 7}), len({1, 2, 3, 4, 5} & {4, 5, 6, 7}), len({1, 2, 3, 4, 5} - {4, 5, 6, 7}), len({1, 2, 3, 4, 5} ^ {4, 5, 6, 7}))),
             Ex("Counting subsets", "How many subsets of a 6-element set have exactly 2 elements, and how many have at most 2?", ["Exactly 2: C(6, 2) = 15.", "At most 2: C(6, 0) + C(6, 1) + C(6, 2) = 1 + 6 + 15 = 22."], "**15** and **22**.", verify=lambda: "%d and %d" % (C(6, 2), C(6, 0) + C(6, 1) + C(6, 2))),
             Ex("Power set of an intersection", "|A| = 6, |B| = 5, |A ∩ B| = 3. How many sets are subsets of both A and B?", ["A set that is a subset of both A and B is a subset of A ∩ B.", "2³ = **8**."], "**8**", verify=lambda: str(2 ** 3)),
             Ex("Nested power sets", "How many elements does P(P({a})) have?", ["|{a}| = 1, so |P({a})| = 2.", "Then |P(P({a}))| = 2² = **4**."], "**4**", verify=lambda: str(2 ** (2 ** 1))),
             Ex("GATE style: pairs of nested subsets", "How many ordered pairs (X, Y) of subsets of a 4-element set satisfy X ⊆ Y?", ["Each element has three states: in neither, in Y only, or in both X and Y.", "3 choices per element: 3⁴ = 81."], "**81**", verify=lambda: str(sum(1 for X in range(16) for Y in range(16) if X & Y == X)))],
         traps=[("∈ versus ⊆", "2 ∈ {1, 2, 3} but {2} ⊆ {1, 2, 3}; {2} ∈ {1, 2, 3} is false."),
                ("Empty set", "∅ ≠ {∅}; the first has no elements, the second has one."),
                ("Power set size", "|P(A)| = 2ⁿ, not n² or 2n."),
                ("Ordered pairs", "(a, b) ≠ (b, a), so A × B ≠ B × A in general.")],
         quick=[("|P(A)| for a set with 5 elements", ["10", "25", "32", "120"], 2, "2⁵."),
                ("|A × B| when |A| = 3 and |B| = 4", ["7", "12", "81", "64"], 1, "3·4."),
                ("A × ∅ is", ["A", "∅", "{∅}", "undefined"], 1, "There are no pairs."),
                ("|A Δ B| equals", ["|A| + |B|", "|A| + |B| − |A ∩ B|", "|A| + |B| − 2|A ∩ B|", "|A − B|"], 2, "Remove the common part from both.")],
         summary=["∈ relates an element to a set; ⊆ relates two sets.", "A = B iff A ⊆ B and B ⊆ A.", "|P(A)| = 2ⁿ for |A| = n, and P(A) ∩ P(B) = P(A ∩ B).", "|A × B| = |A|·|B| and pairs are ordered.", "|A ∪ B| = |A| + |B| − |A ∩ B|; |A Δ B| = |A| + |B| − 2|A ∩ B|."],
         subs=["Set operations"], widget="venn", hint="Shade regions of the Venn diagram to see union, intersection and difference.")

# ------------------------------------------------------------------------------------------------ 2.2
A.lesson("engm-st-incl", "Inclusion–exclusion and divisibility counting",
         key="To count a union, add the sizes, subtract the pairwise overlaps, add back the triple overlaps, and continue with alternating signs. The standard GATE use counts integers divisible by some of a few numbers, where each overlap is a multiple of the lcm.",
         analogy=("🎯", "Overlapping circles", "Count each circle, notice the overlaps were counted twice and take them away once, then repair the very middle, which was added three times and removed three times."),
         defs=[("Inclusion–exclusion principle", "|A₁ ∪ … ∪ A_k| is the sum of single set sizes, minus the sizes of all pairwise intersections, plus all triple intersections, and so on with alternating signs."),
               ("⌊N/a⌋", "The number of multiples of a among 1, 2, …, N."),
               ("lcm(a, b)", "The least positive integer divisible by both a and b; the common multiples of a and b are the multiples of lcm(a, b)."),
               ("Euler's φ(n)", "The number of integers in 1..n that are coprime to n.")],
         parts=[dict(h="Two and three sets", md="""$$|A\\cup B| = |A|+|B|-|A\\cap B|$$

$$|A\\cup B\\cup C| = |A|+|B|+|C|-|A\\cap B|-|A\\cap C|-|B\\cap C|+|A\\cap B\\cap C|$$

The signs alternate with the size of the intersection: plus for one set and three, minus for two. For k sets the same pattern holds, with C(k, j) terms of size j.

"None of" is the complement: the number of elements outside every set is the total minus the union."""),
                 dict(h="Counting multiples", md="""Among 1, 2, …, N exactly ⌊N/a⌋ numbers are divisible by a. A number is divisible by both a and b iff it is divisible by lcm(a, b), so the overlap counts ⌊N/lcm(a, b)⌋. When a and b are coprime, lcm(a, b) = ab, but when they share a factor (say 4 and 6) the lcm is smaller than the product, which is the usual trap.

Template for "divisible by at least one of a, b, c":

⌊N/a⌋ + ⌊N/b⌋ + ⌊N/c⌋ − ⌊N/lcm(a,b)⌋ − ⌊N/lcm(a,c)⌋ − ⌊N/lcm(b,c)⌋ + ⌊N/lcm(a,b,c)⌋."""),
                 dict(h="Coprime counts and survey problems", md="""The numbers in 1..n coprime to n are those divisible by none of its prime factors, so φ(n) = n·Π(1 − 1/p) over the primes p dividing n. For 30 = 2·3·5 that is 30·(1/2)(2/3)(4/5) = 8.

Survey problems are the same principle: a Venn diagram with the numbers of people in each region, filled from the inside out (start with the triple overlap, then the pairwise-only regions, then the single-only regions).""")],
         examples=[
             Ex("Two conditions", "How many integers from 1 to 100 are divisible by 3 or 5?", ["⌊100/3⌋ = 33, ⌊100/5⌋ = 20, ⌊100/15⌋ = 6.", "33 + 20 − 6 = **47**."], "**47**", verify=lambda: str(sum(1 for k in range(1, 101) if k % 3 == 0 or k % 5 == 0))),
             Ex("A shared factor", "How many integers from 1 to 120 are divisible by 4 or 6?", ["⌊120/4⌋ = 30, ⌊120/6⌋ = 20. The overlap uses lcm(4, 6) = 12: ⌊120/12⌋ = 10.", "30 + 20 − 10 = **40**."], "**40**", verify=lambda: str(sum(1 for k in range(1, 121) if k % 4 == 0 or k % 6 == 0))),
             Ex("None of three", "How many integers from 1 to 60 are divisible by none of 2, 3 and 5?", ["Union: 30 + 20 + 12 − 10 − 6 − 4 + 2 = 44.", "60 − 44 = **16**, which is φ(60)."], "**16**", verify=lambda: str(sum(1 for k in range(1, 61) if k % 2 and k % 3 and k % 5))),
             Ex("A survey", "In a class of 50, 30 take Maths, 25 take Physics and 10 take neither. How many take both?", ["At least one subject: 50 − 10 = 40.", "|M ∩ P| = 30 + 25 − 40 = **15**."], "**15**", verify=lambda: str(30 + 25 - (50 - 10))),
             Ex("GATE style: three sets", "|A| = 20, |B| = 25, |C| = 15, |A ∩ B| = 8, |A ∩ C| = 5, |B ∩ C| = 6, |A ∩ B ∩ C| = 3. Find |A ∪ B ∪ C|.", ["20 + 25 + 15 = 60; subtract 8 + 5 + 6 = 19; add 3.", "60 − 19 + 3 = **44**."], "**44**", verify=lambda: str(20 + 25 + 15 - 8 - 5 - 6 + 3))],
         traps=[("Using the product for overlaps", "The overlap of 'divisible by a' and 'by b' is ⌊N/lcm⌋. The product ab is the lcm only when a and b are coprime."),
                ("Stopping early", "Three sets need the triple intersection added back."),
                ("Rounding", "Use the floor ⌊N/a⌋, never N/a."),
                ("Counting the wrong complement", "'None of' means total − union, not total − each single set.")],
         quick=[("Multiples of 7 in 1..100", ["13", "14", "15", "16"], 1, "⌊100/7⌋ = 14."),
                ("|A ∪ B| with |A| = 10, |B| = 7, |A ∩ B| = 3", ["14", "17", "20", "21"], 0, "10 + 7 − 3."),
                ("Integers in 1..30 divisible by neither 2 nor 3", ["8", "10", "12", "15"], 1, "30 − (15 + 10 − 5) = 10."),
                ("Number of terms in the inclusion–exclusion sum for 3 sets", ["3", "5", "7", "8"], 2, "3 + 3 + 1.")],
         summary=["|A ∪ B| = |A| + |B| − |A ∩ B|; for three sets add the triple intersection back.", "Multiples of a up to N: ⌊N/a⌋.", "Overlaps of divisibility conditions use the lcm, not the product.", "'None of' = total − union.", "φ(n) = n·Π(1 − 1/p) over the primes dividing n."],
         subs=["Inclusion–exclusion", "Divisibility counting"])

# ------------------------------------------------------------------------------------------------ 2.3
A.lesson("engm-relations", "Relations and their properties",
         key="A relation on A is a set of ordered pairs from A × A. Four properties classify it: reflexive, symmetric, antisymmetric and transitive. Each is tested pair by pair, and each shows a clear pattern in the matrix of the relation.",
         analogy=("🗺️", "Roads between towns", "A relation is a map of one-way roads between towns. Reflexive means every town has a loop road; symmetric means every road has a return road; transitive means a two-step trip always has a shortcut."),
         defs=[("Binary relation on A", "A subset R of A × A; we write a R b when (a, b) ∈ R."),
               ("Reflexive", "(a, a) ∈ R for every a ∈ A."),
               ("Symmetric", "Whenever (a, b) ∈ R, also (b, a) ∈ R."),
               ("Antisymmetric", "Whenever (a, b) ∈ R and (b, a) ∈ R, a = b."),
               ("Transitive", "Whenever (a, b) ∈ R and (b, c) ∈ R, also (a, c) ∈ R.")],
         parts=[dict(h="Representing a relation", md="""A relation on a finite set can be shown as a list of pairs, as a directed graph, or as a 0/1 matrix M with Mᵢⱼ = 1 when aᵢ R aⱼ. The properties read off the matrix:

| Property | In the matrix | In the graph |
|---|---|---|
| Reflexive | 1s on the whole diagonal | a loop at every vertex |
| Symmetric | M = Mᵀ | every edge has a reverse edge |
| Antisymmetric | no pair of 1s at (i, j) and (j, i) with i ≠ j | no two-way edge between different vertices |
| Transitive | M² has no 1 where M has a 0 | every two-step path has a direct edge |"""),
                 dict(h="Checking the properties", md="""Test each property on the list of pairs; one violation settles it.

- **Reflexive:** is every (a, a) present? Missing even one loop fails it.
- **Symmetric:** for each (a, b), is (b, a) present?
- **Antisymmetric:** is there a pair (a, b), a ≠ b, with (b, a) also present? If so it fails.
- **Transitive:** for each chain (a, b), (b, c), is (a, c) present?

Symmetric and antisymmetric are not opposites. A relation can have both (equality), or neither ({(1, 2), (2, 1), (2, 3)} is not symmetric and not antisymmetric)."""),
                 dict(h="Standard examples", md="""| Relation | Reflexive | Symmetric | Antisymmetric | Transitive |
|---|---|---|---|---|
| = on ℤ | yes | yes | yes | yes |
| ≤ on ℤ | yes | no | yes | yes |
| < on ℤ | no | no | yes | yes |
| divides on ℕ⁺ | yes | no | yes | yes |
| ≡ mod n on ℤ | yes | yes | no | yes |
| ∅ on a non-empty set | no | yes | yes | yes |

A relation that is reflexive, antisymmetric and transitive is a partial order; one that is reflexive, symmetric and transitive is an equivalence relation.""")],
         examples=[
             Ex("Reading properties", "R = {(1,1), (2,2), (3,3), (1,2), (2,1)} on {1, 2, 3}. Which properties hold?", ["Every (a, a) is present: reflexive.", "(1, 2) and (2, 1) both present: symmetric, and not antisymmetric.", "Transitivity: (1,2),(2,1) force (1,1) and (2,2), both present; no other chains. It holds."], "Reflexive, symmetric and transitive: an **equivalence relation**.", verify=lambda: "Reflexive, symmetric and transitive: an equivalence relation"),
             Ex("Not transitive", "R = {(1,2), (2,3)} on {1, 2, 3}. Is R transitive? What is the fewest pairs to add so it is?", ["(1,2) and (2,3) force (1,3), which is missing: not transitive.", "Adding (1,3) creates no new chain, so one pair suffices."], "Not transitive; add **1** pair, (1,3).", verify=lambda: "Not transitive; add 1 pair, (1,3)"),
             Ex("Both symmetric and antisymmetric", "Which reflexive relations on {1, 2} are both symmetric and antisymmetric?", ["Symmetric plus antisymmetric forbids any pair (a, b) with a ≠ b.", "Reflexive then forces exactly the diagonal."], "Only **{(1,1), (2,2)}**.", verify=lambda: "Only {(1,1), (2,2)}"),
             Ex("Divisibility", "Is 'x divides y' on {1, 2, 3, 6} reflexive, antisymmetric and transitive?", ["x | x always; x | y and y | x give x = y for positive integers; x | y and y | z give x | z."], "**Yes**, it is a partial order.", verify=lambda: "Yes, it is a partial order" if all(((a, a) in {(x, y) for x in (1, 2, 3, 6) for y in (1, 2, 3, 6) if y % x == 0}) for a in (1, 2, 3, 6)) else "?"),
             Ex("GATE style: matrix test", "A relation on {1, 2, 3} has matrix rows 110, 011, 001. Is it reflexive, symmetric, transitive?", ["Diagonal is 1, 1, 1: reflexive.", "(1,2) is present but (2,1) is not: not symmetric.", "(1,2), (2,3) force (1,3), and row 1 has 0 in column 3: not transitive."], "Reflexive only.", verify=lambda: "Reflexive only")],
         traps=[("Reflexive on the whole set", "One missing loop destroys reflexivity, even if the relation 'looks' reflexive on the elements that appear."),
                ("Symmetric versus antisymmetric", "They are not opposites; equality is both, some relations are neither."),
                ("The empty relation", "On a non-empty set it is symmetric, antisymmetric and transitive but not reflexive."),
                ("Checking transitivity", "Look at every chain (a, b), (b, c), including those with a = c.")],
         quick=[("Which relation on ℤ is reflexive and symmetric but not transitive?", ["x = y", "|x − y| ≤ 1", "x ≤ y", "x < y"], 1, "1 R 2 and 2 R 3 but not 1 R 3."),
                ("'x divides y' on the positive integers is", ["symmetric", "antisymmetric", "irreflexive", "an equivalence"], 1, "x | y and y | x force x = y."),
                ("The matrix of a symmetric relation satisfies", ["M = I", "M = Mᵀ", "M² = M", "M = 0"], 1, "Mirror image across the diagonal."),
                ("A relation that is both symmetric and antisymmetric is contained in", ["the empty set", "the diagonal", "A × A", "the complement of the diagonal"], 1, "Only (a, a) pairs can appear.")],
         summary=["Reflexive: all (a, a); symmetric: M = Mᵀ; antisymmetric: no two-way pair between different elements.", "Transitive: every two-step chain has a direct pair.", "Symmetric and antisymmetric are independent properties.", "Reflexive + antisymmetric + transitive = partial order; reflexive + symmetric + transitive = equivalence.", "Test each property by searching for one violating pair or chain."],
         subs=["Relation properties"], widget="relation", hint="Toggle pairs in the matrix and watch which properties hold.")

# ------------------------------------------------------------------------------------------------ 2.4
A.lesson("engm-st-relations-count", "Counting relations by property",
         key="A relation on an n-element set is any subset of its n² ordered pairs. Each property pins some pairs and frees the others, so the number of relations with that property is a power of 2 (or of 3 for antisymmetry, where each unordered pair has three allowed states).",
         analogy=("🎛️", "A board of switches", "Each ordered pair is a switch that is on or off. Reflexive welds the diagonal switches on; symmetric ties each pair of mirror switches together; antisymmetric forbids a mirror pair from both being on."),
         defs=[("Irreflexive", "No pair (a, a) belongs to R."),
               ("Asymmetric", "(a, b) ∈ R implies (b, a) ∉ R; equivalently, irreflexive and antisymmetric."),
               ("Unordered pair {a, b}", "Two distinct elements, with (a, b) and (b, a) as its two mirror positions in the matrix.")],
         parts=[dict(h="The count behind each formula", md="""Picture the n × n matrix. It has n diagonal cells and n(n − 1)/2 mirror pairs of off-diagonal cells, and every cell may be 0 or 1 independently *unless* a property links them.

| Property | Free choices | Count |
|---|---|---|
| any relation | all n² cells | 2^(n²) |
| reflexive | diagonal forced to 1; n² − n cells free | 2^(n²−n) |
| irreflexive | diagonal forced to 0 | 2^(n²−n) |
| symmetric | n diagonal cells and n(n−1)/2 mirror pairs | 2^(n(n+1)/2) |
| antisymmetric | n diagonal cells (2 each); each mirror pair has 3 states | 2ⁿ·3^(n(n−1)/2) |
| asymmetric | diagonal 0; each mirror pair has 3 states | 3^(n(n−1)/2) |
| reflexive and symmetric | mirror pairs only | 2^(n(n−1)/2) |

For a mirror pair of an antisymmetric relation the allowed states are: neither pair, only (a, b), only (b, a); the state "both" is forbidden."""),
                 dict(h="Using the formulas", md="""1. Count the cells that are forced and the cells that are free.
2. For linked cells, count the allowed *states* of the link (2 for a symmetric pair, 3 for an antisymmetric pair).
3. Multiply the numbers of states of all independent groups.

Check with n = 2 (four cells): 16 relations in all, 4 reflexive, 8 symmetric, 12 antisymmetric, and 2 that are reflexive and symmetric (only the one mirror pair is free)."""),
                 dict(h="Equivalence relations", md="""The number of equivalence relations on an n-set equals the number of partitions of the set, the **Bell number** B(n): 1, 1, 2, 5, 15, 52, 203, … for n = 0, 1, 2, … . B(n) is the sum over k of the Stirling numbers S(n, k) of partitions into k blocks. Transitive relations have no closed formula.""")],
         examples=[
             Ex("Reflexive", "How many reflexive relations are there on a 4-element set?", ["There are 16 cells and the 4 diagonal ones are forced.", "2¹² = **4096**."], "**4096**", verify=lambda: str(2 ** (16 - 4))),
             Ex("Symmetric", "How many symmetric relations are there on a 3-element set?", ["3 diagonal cells and 3 mirror pairs: 6 free choices.", "2⁶ = **64**."], "**64**", verify=lambda: str(2 ** 6)),
             Ex("Antisymmetric", "How many antisymmetric relations are there on a 3-element set?", ["Diagonal: 2³ = 8 choices. Three mirror pairs: 3 states each, 3³ = 27.", "8·27 = **216**."], "**216**", verify=lambda: str(2 ** 3 * 3 ** 3)),
             Ex("Equivalence relations", "How many equivalence relations are there on a 4-element set?", ["Count partitions: S(4,1) + S(4,2) + S(4,3) + S(4,4) = 1 + 7 + 6 + 1."], "**15**", verify=lambda: str(M2.bell(4))),
             Ex("GATE style: reflexive and symmetric", "How many relations on a 5-element set are both reflexive and symmetric?", ["The diagonal is forced; the 10 mirror pairs are free.", "2¹⁰ = **1024**."], "**1024**", verify=lambda: str(2 ** 10))],
         traps=[("Counting n² cells for symmetric", "Mirror cells are linked; count n(n+1)/2 independent choices."),
                ("Equivalence count", "It is a Bell number (partitions), not a power of 2."),
                ("Antisymmetric", "Each mirror pair has 3 states, not 4; each diagonal cell still has 2."),
                ("Forgetting the diagonal", "For asymmetric relations the diagonal must be empty.")],
         quick=[("Reflexive relations on a 3-element set", ["8", "64", "256", "512"], 1, "2^(9−3)."),
                ("Number of partitions of a 3-element set", ["3", "5", "6", "8"], 1, "B(3) = 5."),
                ("Asymmetric relations on a 2-element set", ["3", "4", "8", "16"], 0, "3^1."),
                ("Symmetric relations on a 2-element set", ["4", "8", "16", "2"], 1, "2^(2·3/2) = 2³.")],
         summary=["All relations: 2^(n²); reflexive and irreflexive: 2^(n²−n).", "Symmetric: 2^(n(n+1)/2); reflexive and symmetric: 2^(n(n−1)/2).", "Antisymmetric: 2ⁿ·3^(n(n−1)/2); asymmetric: 3^(n(n−1)/2).", "Equivalence relations: Bell number B(n).", "Count forced cells, free cells and the states of each linked group."],
         subs=["Counting relations on a set", "Counting relations & functions"])

# ------------------------------------------------------------------------------------------------ 2.5
A.lesson("engm-st-closures-eq", "Equivalence relations, partitions and closures",
         key="An equivalence relation splits a set into disjoint classes, and every partition gives back an equivalence relation. A closure adds the fewest pairs needed to gain a property; the transitive closure is computed by repeated composition (Warshall's algorithm).",
         analogy=("🌐", "Friend circles", "Being in the same circle is reflexive, symmetric and transitive: that is an equivalence relation, and the circles are its classes. The transitive closure is 'friends of friends of friends…' until nothing new appears."),
         defs=[("Equivalence relation", "A relation that is reflexive, symmetric and transitive."),
               ("Equivalence class [a]", "The set of all elements related to a; the classes of a relation partition the set."),
               ("Partition", "A collection of non-empty, pairwise disjoint subsets whose union is the whole set."),
               ("Closure of R", "The smallest relation containing R that has the required property (reflexive, symmetric or transitive).")],
         parts=[dict(h="Equivalence relations and partitions", md="""If R is an equivalence relation, the classes [a] = {x : a R x} are either equal or disjoint, and together they cover the set: a **partition**. Conversely, any partition defines the relation "x and y lie in the same block", which is an equivalence relation. So the two notions are the same thing seen from two sides.

Standard example: congruence modulo n on ℤ has n classes, {…, −n, 0, n, …}, {…, 1, n + 1, …}, and so on.

If the classes have sizes s₁, …, s_k, the relation contains **Σ sᵢ²** ordered pairs, because each class contributes all pairs inside it."""),
                 dict(h="Closures", md="""- **Reflexive closure:** R ∪ {(a, a) : a ∈ A}, adding the missing loops.
- **Symmetric closure:** R ∪ {(b, a) : (a, b) ∈ R}, adding the missing reverses.
- **Transitive closure R⁺:** repeatedly add (a, c) whenever (a, b) and (b, c) are present, until nothing new appears. Equivalently R⁺ = R ∪ R² ∪ R³ ∪ …, where Rᵏ is "a path of exactly k steps".

The **equivalence closure** is the transitive closure of the symmetric closure of the reflexive closure: make it reflexive and symmetric first, and *then* transitive. Doing transitivity first can leave new violations."""),
                 dict(h="Warshall's algorithm", md="""Warshall computes the transitive closure of a relation on n elements in O(n³): for each intermediate element k, for each pair (i, j), set Mᵢⱼ = Mᵢⱼ OR (Mᵢₖ AND Mₖⱼ). After processing all k, Mᵢⱼ = 1 exactly when a directed path leads from i to j. The loop order matters: k must be the outermost loop.""")],
         examples=[
             Ex("Reflexive closure", "Let R = {(1,2), (2,3)} on the set {1, 2, 3}. How many pairs does the reflexive closure of R contain?", ["Add (1,1), (2,2), (3,3).", "2 + 3 = **5**."], "**5**", verify=lambda: str(2 + 3)),
             Ex("Transitive closure", "R = {(1,2), (2,3), (3,4)}. How many pairs does its transitive closure contain?", ["Chains of two steps: (1,3), (2,4). Three steps: (1,4).", "3 + 3 = **6**."], "**6**", verify=lambda: str(len({(1, 2), (2, 3), (3, 4), (1, 3), (2, 4), (1, 4)}))),
             Ex("Pairs in an equivalence relation", "An equivalence relation on 6 elements has classes of sizes 3, 2 and 1. How many ordered pairs does it contain?", ["Each class contributes size² pairs: 9 + 4 + 1.", "**14**."], "**14**", verify=lambda: str(9 + 4 + 1)),
             Ex("Counting equivalence relations", "How many equivalence relations exist on {a, b, c, d}?", ["Count partitions by the number of blocks: 1 + 7 + 6 + 1."], "**15**", verify=lambda: str(M2.bell(4))),
             Ex("GATE style: smallest equivalence relation", "For the relation {(1,2), (2,3)} on {1, 2, 3}, how many pairs are in the smallest equivalence relation that contains it?", ["Reflexive and symmetric first: (1,1), (2,2), (3,3), (2,1), (3,2) plus the originals: 7 pairs.", "Transitive step adds (1,3) and (3,1): 9 pairs, i.e. one class of size 3."], "**9**", verify=lambda: str(3 ** 2))],
         traps=[("Closure order", "Make the relation reflexive and symmetric before taking the transitive closure."),
                ("Adding too much", "A closure adds only the forced pairs, nothing else."),
                ("Pairs in an equivalence relation", "It is the sum of the squares of the class sizes, not the sum of the sizes."),
                ("Classes are disjoint", "Two classes either coincide or share nothing.")],
         quick=[("Equivalence classes are always", ["overlapping", "disjoint or equal", "nested", "ordered"], 1, "They partition the set."),
                ("The reflexive closure of {(1,2)} on {1, 2} is", ["{(1,2)}", "{(1,2), (1,1), (2,2)}", "{(1,2), (2,1)}", "{(1,1), (2,2)}"], 1, "Add the missing loops."),
                ("Warshall's algorithm runs in time", ["O(n)", "O(n²)", "O(n³)", "O(2ⁿ)"], 2, "Three nested loops."),
                ("Number of classes of ≡ mod 5 on ℤ", ["1", "4", "5", "infinitely many"], 2, "One per remainder.")],
         summary=["An equivalence relation is the same as a partition into disjoint classes.", "An equivalence relation with classes of sizes sᵢ has Σ sᵢ² pairs.", "A closure adds only the forced pairs; the transitive closure is R ∪ R² ∪ R³ ∪ ….", "Take reflexive and symmetric closures before the transitive one.", "Warshall computes the transitive closure in O(n³)."],
         subs=["Closures"])

# ------------------------------------------------------------------------------------------------ 2.6
A.lesson("engm-functions", "Functions: one-to-one, onto and bijective",
         key="A function gives every input exactly one output. It is one-to-one when different inputs never share an output, onto when every element of the codomain is an output, and bijective when both, which is exactly when an inverse function exists.",
         analogy=("🎟️", "Seats and ticket holders", "A function seats each person in exactly one seat. One-to-one means no two people share a seat; onto means no seat is empty; bijective means a perfect pairing, so you can also go from seat back to person."),
         defs=[("Function f: A → B", "A rule assigning to each a ∈ A exactly one f(a) ∈ B; A is the domain and B the codomain."),
               ("Range", "The set {f(a) : a ∈ A} of values actually taken, a subset of the codomain."),
               ("One-to-one (injective)", "f(a) = f(b) implies a = b."),
               ("Onto (surjective)", "For every b ∈ B there is an a ∈ A with f(a) = b."),
               ("Bijective", "Both one-to-one and onto.")],
         parts=[dict(h="Domain, codomain and range", md="""A function is more than a formula: it is the formula *together with* its domain and codomain. f(x) = x² is one-to-one on [0, ∞) but not on ℝ, and onto [0, ∞) but not onto ℝ. Two things make a rule a function: **every** input has an output, and **only one** output. {(1, a), (2, b), (1, c)} fails the second condition."""),
                 dict(h="One-to-one and onto", md="""| Property | Meaning | How to test |
|---|---|---|
| One-to-one | no output is used twice | f(a) = f(b) ⇒ a = b; strictly monotonic on ℝ |
| Onto | every codomain element is hit | solve y = f(x) for x in the domain; range = codomain |
| Bijective | a perfect pairing | both of the above |

Size facts for finite sets: a one-to-one function A → B needs |A| ≤ |B|; an onto function needs |A| ≥ |B|; a bijection needs |A| = |B|. When |A| = |B|, one-to-one, onto and bijective are all equivalent. These rules are the pigeonhole principle in functional form."""),
                 dict(h="Composition and inverse", md="""The composition (g∘f)(x) = g(f(x)) applies f first. Facts:

- if f and g are one-to-one (onto), so is g∘f;
- if g∘f is one-to-one, then f is one-to-one (but g need not be);
- if g∘f is onto, then g is onto (but f need not be).

A function has an inverse f⁻¹: B → A exactly when it is bijective. To find the inverse, solve y = f(x) for x. Composition is associative but not commutative.""")],
         examples=[
             Ex("From a table", "f: {a, b, c, d} → {1, 2, 3} sends a → 1, b → 2, c → 3, d → 1. Is f one-to-one? onto?", ["1 is used twice (a and d): not one-to-one.", "Outputs 1, 2, 3 are all used: onto."], "**Onto but not one-to-one.**", verify=lambda: "Onto but not one-to-one" if len({1, 2, 3, 1}) == 3 and len([1, 2, 3, 1]) == 4 else "?"),
             Ex("Real functions", "Classify f(x) = x³ − x from ℝ to ℝ.", ["It takes every real value (a cubic is continuous and unbounded both ways): onto.", "f(0) = f(1) = 0, so it is not one-to-one."], "**Onto, not one-to-one.**", verify=lambda: "Onto, not one-to-one" if (0 ** 3 - 0) == (1 ** 3 - 1) else "?"),
             Ex("Composition", "f(x) = 2x + 1 and g(x) = x² − 3. Find (g∘f)(2) and (f∘g)(2).", ["f(2) = 5, then g(5) = 22.", "g(2) = 1, then f(1) = 3."], "**22** and **3**; composition is not commutative.", verify=lambda: "%d and %d; composition is not commutative" % ((lambda f, g: g(f(2)))(lambda x: 2 * x + 1, lambda x: x * x - 3), (lambda f, g: f(g(2)))(lambda x: 2 * x + 1, lambda x: x * x - 3))),
             Ex("Inverse", "f(x) = (2x + 1)/3 is a bijection of ℝ. Find f⁻¹(5).", ["Solve 5 = (2x + 1)/3: 2x + 1 = 15, x = 7."], "**7**", verify=lambda: str((5 * 3 - 1) // 2)),
             Ex("GATE style: composition and injectivity", "If g∘f is one-to-one, what can be said about f and g?", ["If f(a) = f(b), then g(f(a)) = g(f(b)), so a = b: f is one-to-one.", "g can fail to be one-to-one outside the range of f."], "**f must be one-to-one**; g need not be.", verify=lambda: "f must be one-to-one; g need not be")],
         traps=[("Codomain matters", "x² is onto [0, ∞) but not onto ℝ."),
                ("Not a function", "An input with two outputs, or an input with none, breaks the definition."),
                ("Composition order", "g∘f applies f first."),
                ("One-to-one needs only the domain", "A function can be one-to-one without being onto.")],
         quick=[("x ↦ x³ from ℝ to ℝ is", ["one-to-one only", "onto only", "bijective", "neither"], 2, "Strictly increasing and unbounded."),
                ("If g∘f is onto then", ["f is onto", "g is onto", "both are onto", "neither need be"], 1, "g must reach everything."),
                ("A function from {1, 2, 3} to {a, b} can be", ["one-to-one", "onto", "bijective", "none of these"], 1, "Three inputs, two outputs: onto is possible, one-to-one is not."),
                ("A function has an inverse iff it is", ["one-to-one", "onto", "bijective", "continuous"], 2, "It must be a perfect pairing.")],
         summary=["A function needs one output for every input; domain and codomain are part of it.", "One-to-one: f(a) = f(b) ⇒ a = b. Onto: range = codomain.", "On finite sets of equal size, one-to-one ⇔ onto ⇔ bijective.", "g∘f one-to-one ⇒ f one-to-one; g∘f onto ⇒ g onto.", "An inverse exists exactly for bijections."],
         subs=["Function properties"])

# ------------------------------------------------------------------------------------------------ 2.7
A.lesson("engm-st-functions-count", "Counting functions",
         key="From an m-element set to an n-element set there are nᵐ functions, P(n, m) one-to-one functions, and Σ(−1)ʲC(n, j)(n − j)ᵐ onto functions. For m = n the bijections number n!.",
         analogy=("📮", "Posting letters", "Each of m letters goes into one of n boxes: nᵐ ways. One-to-one means no box gets two letters; onto means no box stays empty."),
         defs=[("P(n, m)", "n(n − 1)…(n − m + 1), the number of ways to choose m distinct images in order."),
               ("Stirling number S(m, n)", "The number of ways to partition an m-set into n non-empty unlabelled blocks."),
               ("Partial function", "A function defined only on part of its domain: each input has at most one output.")],
         parts=[dict(h="The counts", md="""Let |A| = m and |B| = n.

| Functions A → B | Count | Reason |
|---|---|---|
| all | nᵐ | m inputs, n free choices each |
| one-to-one (m ≤ n) | n(n−1)…(n−m+1) = P(n, m) | outputs must differ: n, then n − 1, … |
| onto (m ≥ n) | Σⱼ (−1)ʲ C(n, j)(n − j)ᵐ = n!·S(m, n) | inclusion–exclusion on missed outputs |
| bijections (m = n) | n! | one-to-one on equal sets |
| constant | n | the common output |
| partial | (n + 1)ᵐ | each input is undefined or one of n outputs |"""),
                 dict(h="Why the onto formula works", md="""Start with all nᵐ functions. Subtract those that miss at least one output: choose which j outputs are missed, C(n, j) ways, and map into the remaining n − j outputs, (n − j)ᵐ ways. Inclusion–exclusion then alternates signs:

$$\\#\\text{onto}=n^m-\\binom n1(n-1)^m+\\binom n2(n-2)^m-\\cdots$$

Check with m = 4, n = 2: 2⁴ − 2·1⁴ = 14, which equals the 16 functions minus the 2 constant ones."""),
                 dict(h="Counting with a rule", md="""For a function with extra conditions, treat each input in turn and multiply the number of allowed outputs, unless the conditions link the inputs. Examples: "f(1) = 1" fixes one input and leaves nᵐ⁻¹ functions; "f is increasing" turns the count into a multiset problem, C(n + m − 1, m).""")],
         examples=[
             Ex("One-to-one", "How many one-to-one functions are there from a 3-set to a 6-set?", ["6 × 5 × 4 = 120."], "**120**", verify=lambda: str(math.perm(6, 3))),
             Ex("Onto, small case", "How many onto functions are there from a 4-set to a 2-set?", ["Total 2⁴ = 16; subtract the two constant functions."], "**14**", verify=lambda: str(2 ** 4 - 2)),
             Ex("Onto, by inclusion–exclusion", "How many onto functions are there from a 5-set to a 3-set?", ["3⁵ − 3·2⁵ + 3·1⁵ = 243 − 96 + 3 = 150."], "**150**", verify=lambda: str(3 ** 5 - 3 * 2 ** 5 + 3)),
             Ex("Partial functions", "How many partial functions are there from a 3-set to a 2-set?", ["Each input is undefined or maps to one of 2 outputs: 3 options each.", "3³ = **27**."], "**27**", verify=lambda: str(3 ** 3)),
             Ex("GATE style: increasing functions", "How many non-decreasing functions are there from {1, 2, 3} to {1, 2, 3, 4}?", ["A non-decreasing function is a multiset of size 3 chosen from 4 values (listed in order).", "C(4 + 3 − 1, 3) = C(6, 3) = 20."], "**20**", verify=lambda: str(sum(1 for f in itertools.product(range(4), repeat=3) if f[0] <= f[1] <= f[2])))],
         traps=[("nᵐ versus mⁿ", "Functions from A to B number |B|^|A|: outputs to the power of inputs."),
                ("Onto needs inclusion–exclusion", "P(n, m) counts one-to-one functions, not onto ones."),
                ("Impossible cases", "One-to-one needs m ≤ n; onto needs m ≥ n; otherwise the count is 0."),
                ("Subsets", "A set with m elements has 2ᵐ subsets, which equals the number of functions to {0, 1}.")],
         quick=[("Functions from a 3-element set to a 4-element set", ["12", "64", "81", "24"], 1, "4³."),
                ("One-to-one functions from a 2-element set to a 5-element set", ["10", "20", "25", "32"], 1, "5·4."),
                ("Onto functions from a 3-set to a 3-set", ["3", "6", "9", "27"], 1, "They are bijections: 3!."),
                ("Number of subsets of a 6-element set", ["12", "36", "64", "720"], 2, "2⁶.")],
         summary=["All functions: nᵐ, with n outputs and m inputs.", "One-to-one: P(n, m); bijections: n!.", "Onto: n!·S(m, n) = Σ (−1)ʲ C(n, j)(n − j)ᵐ.", "Partial functions: (n + 1)ᵐ.", "A function into {0, 1} is a subset: 2ᵐ of them."],
         subs=["Counting functions"], widget="counting", hint="Choose the sizes of the two sets and the kind of function to count.")
