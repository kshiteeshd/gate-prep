"""Engineering Mathematics · Chapter 3 Partial Orders & Lattices."""
import itertools
import math

from learn import Ex
from learn.author import Author

A = Author("ENGM")
A.chapter("Partial Orders & Lattices")


def divs(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def lcm(a, b):
    return a * b // math.gcd(a, b)


def minimal(X):
    return [a for a in X if not any(b != a and a % b == 0 for b in X)]


def maximal(X):
    return [a for a in X if not any(b != a and b % a == 0 for b in X)]


# ------------------------------------------------------------------------------------------------ 3.1
A.lesson("engm-posets-lattices", "Partial orders and Hasse diagrams",
         key="A partial order is a relation that is reflexive, antisymmetric and transitive. A Hasse diagram draws a finite poset economically, showing only the covering pairs, with larger elements higher.",
         analogy=("🏢", "An organisation chart", "A manager is above everyone below in the chain. Two people in different branches are not comparable; you draw only the direct reporting lines, since the longer chains follow from them."),
         defs=[("Partial order ≤", "A relation that is reflexive, antisymmetric and transitive; a set with a partial order is a poset."),
               ("Comparable", "Elements a and b with a ≤ b or b ≤ a."),
               ("Covers", "b covers a if a < b and there is no c with a < c < b."),
               ("Hasse diagram", "A drawing of a finite poset showing one edge per covering pair, with larger elements higher.")],
         parts=[dict(h="What makes an order partial", md="""A **partial** order allows incomparable elements; a **total** order (chain) compares every pair. Standard posets:

- (ℕ⁺, |): a ≤ b means a divides b. Reflexive (a | a), antisymmetric (a | b and b | a ⇒ a = b for positive integers) and transitive.
- (P(S), ⊆): subsets ordered by inclusion; {1} and {2} are incomparable.
- (ℤ, ≤): a total order.

On ℤ (with negatives) divisibility is not antisymmetric: 1 | −1 and −1 | 1 but 1 ≠ −1."""),
                 dict(h="Drawing a Hasse diagram", md="""1. Draw a vertex for every element, placing a below b whenever a < b.
2. Join a to b only if b **covers** a.
3. Omit loops (implied by reflexivity), arrowheads (everything points upwards) and edges implied by transitivity.

For the divisors of 12: the covering pairs are 1–2, 1–3, 2–4, 2–6, 3–6, 4–12, 6–12. The edge 1–4 is omitted because 1 < 2 < 4. A finite poset's order is recovered as "a ≤ b iff there is an upward path from a to b"."""),
                 dict(h="Reading a diagram", md="""- Two elements are comparable iff an upward path joins them.
- The number of edges of the Hasse diagram is the number of covering pairs, not the number of pairs a < b.
- For (P(S), ⊆) with |S| = n, the Hasse diagram is the n-dimensional cube: 2ⁿ vertices and n·2ⁿ⁻¹ edges.""")],
         examples=[
             Ex("Is it a partial order?", "Is 'x divides y' a partial order on the integers (including negative ones)?", ["Reflexive and transitive hold.", "Antisymmetry fails: 1 | −1 and −1 | 1 but 1 ≠ −1."], "**No**; it is a partial order only on the positive integers.", verify=lambda: "No" if (-1 % 1 == 0 and 1 % -1 == 0 and 1 != -1) else "?"),
             Ex("Hasse edges of D₁₂", "How many edges does the Hasse diagram of the divisors of 12 under divisibility have?", ["Covering pairs are those where the quotient is a prime: 1–2, 1–3, 2–4, 2–6, 3–6, 4–12, 6–12."], "**7**", verify=lambda: str(sum(1 for a in divs(12) for b in divs(12) if b % a == 0 and b // a in (2, 3)))),
             Ex("Comparability", "In the divisor poset of 12, are 4 and 6 comparable? Are 2 and 12?", ["4 ∤ 6 and 6 ∤ 4: not comparable.", "2 | 12: comparable."], "4 and 6 are **incomparable**; 2 and 12 are **comparable**.", verify=lambda: "4 and 6 are incomparable; 2 and 12 are comparable" if 6 % 4 and 4 % 6 and 12 % 2 == 0 else "?"),
             Ex("The cube", "How many edges does the Hasse diagram of (P({a, b, c}), ⊆) have?", ["n·2ⁿ⁻¹ with n = 3: 3·4 = 12."], "**12**", verify=lambda: str(3 * 2 ** 2)),
             Ex("GATE style: order of a relation", "On {1, 2, 3, 4}, R = {(a, b): a ≤ b and a divides b}. Is R a partial order? How many pairs does it contain?", ["Divisibility is already a partial order, and a | b implies a ≤ b, so R is divisibility.", "Pairs: (1,1)(1,2)(1,3)(1,4)(2,2)(2,4)(3,3)(4,4)."], "Yes; **8** pairs.", verify=lambda: "Yes; %d pairs" % sum(1 for a in range(1, 5) for b in range(1, 5) if a <= b and b % a == 0))],
         traps=[("Drawing transitive edges", "Do not draw 1–4 when 1 < 2 < 4."),
                ("Comparable means related", "Divisors like 4 and 6 are not comparable; the order is partial."),
                ("Antisymmetry on negatives", "Divisibility on ℤ is not antisymmetric."),
                ("Counting edges", "Edges count covering pairs, not all related pairs.")],
         quick=[("A partial order must be", ["symmetric", "antisymmetric", "total", "irreflexive"], 1, "Reflexive, antisymmetric, transitive."),
                ("⊆ on the subsets of a set is", ["a total order", "a partial order", "an equivalence", "not transitive"], 1, "Some sets are incomparable."),
                ("Edges in the Hasse diagram of the subsets of a 4-set", ["16", "24", "32", "64"], 2, "n·2ⁿ⁻¹ = 4·8."),
                ("In a Hasse diagram an edge from a up to b means", ["a < b", "b covers a", "a and b are equal", "a divides b only"], 1, "Only covering pairs are drawn.")],
         summary=["A partial order is reflexive, antisymmetric and transitive; some pairs may be incomparable.", "Divisibility on ℕ⁺ and ⊆ on subsets are the standard posets.", "A Hasse diagram draws covering pairs only, upwards, without loops or implied edges.", "a ≤ b iff an upward path leads from a to b.", "The subset poset of an n-set is the n-cube."],
         subs=["Posets"], widget="hasse", hint="Pick a set of divisors and see its Hasse diagram.")

# ------------------------------------------------------------------------------------------------ 3.2
A.lesson("engm-po-extremal", "Extremal elements, bounds, chains and antichains",
         key="Minimal and maximal elements have nothing below or above them; a least or greatest element must lie below or above everything. Chains are sets of pairwise comparable elements, antichains are sets of pairwise incomparable ones, and Dilworth's theorem links the two.",
         analogy=("🏔️", "Peaks of a mountain range", "A range can have several peaks (maximal elements) without one summit that is higher than every other point (a greatest element)."),
         defs=[("Minimal / maximal element", "An element with no element strictly below / above it."),
               ("Least / greatest element", "An element below / above every element of the poset."),
               ("Upper bound and lub", "An element above both a and b; the least upper bound is the smallest such element."),
               ("Chain / antichain", "A subset in which every two elements are comparable / no two are comparable.")],
         parts=[dict(h="Minimal versus least", md="""| Term | Meaning | How many can exist |
|---|---|---|
| Minimal element | nothing strictly below it | any number |
| Least element | below *every* element | at most one |
| Maximal element | nothing strictly above it | any number |
| Greatest element | above *every* element | at most one |

A greatest element is always maximal; the converse fails. In {2, 3, 6, 12, 18} under divisibility the minimal elements are 2 and 3, there is no least element; the maximal elements are 12 and 18, there is no greatest. Every finite non-empty poset has at least one minimal and one maximal element."""),
                 dict(h="Upper and lower bounds", md="""For a subset S of a poset, an **upper bound** is an element above every member of S. The **lub** (supremum) is the least of the upper bounds if it exists; similarly **glb** (infimum). In (ℕ⁺, |) the lub of a and b is lcm(a, b) and the glb is gcd(a, b). Bounds may lie outside S, and a lub need not exist (two minimal upper bounds mean there is no least one)."""),
                 dict(h="Chains and antichains", md="""A chain in the divisor poset of 12 is {1, 2, 4, 12}; an antichain is {4, 6} (neither divides the other). Two theorems:

- **Mirsky:** the maximum chain length equals the minimum number of antichains needed to cover the poset.
- **Dilworth:** the maximum antichain size equals the minimum number of chains needed to cover the poset.

So to cover a poset with the fewest chains, find its largest antichain; to find the longest chain, count levels.""")],
         examples=[
             Ex("Minimal and maximal", "How many minimal and how many maximal elements does ({2, 3, 4, 6, 12, 24, 36}, |) have?", ["Minimal: 2 and 3 (nothing else divides them).", "Maximal: 24 and 36 (neither divides the other, nothing larger)."], "**2** minimal and **2** maximal.", verify=lambda: "%d minimal and %d maximal" % (len(minimal([2, 3, 4, 6, 12, 24, 36])), len(maximal([2, 3, 4, 6, 12, 24, 36])))),
             Ex("Least and greatest", "Does ({1, 2, 3, 6, 12}, |) have a least or greatest element?", ["1 divides everything: least element 1.", "12 is divisible by 1, 2, 3, 6: greatest element 12."], "Least **1** and greatest **12**.", verify=lambda: "Least %d and greatest %d" % (1, 12) if all(x % 1 == 0 and 12 % x == 0 for x in (1, 2, 3, 6, 12)) else "?"),
             Ex("Least upper bound", "In (ℕ⁺, |), find the lub and glb of 8 and 12.", ["lub = lcm(8, 12) = 24.", "glb = gcd(8, 12) = 4."], "lub **24**, glb **4**.", verify=lambda: "lub %d, glb %d" % (lcm(8, 12), math.gcd(8, 12))),
             Ex("Largest antichain", "What is the largest antichain in the divisor poset of 30?", ["Divisors: 1, 2, 3, 5, 6, 10, 15, 30. The primes {2, 3, 5} form an antichain of size 3, and so do {6, 10, 15}.", "No antichain of size 4 exists."], "**3**", verify=lambda: str(max(len(c) for k in range(1, 9) for c in itertools.combinations(divs(30), k) if all(a % b and b % a for a, b in itertools.combinations(c, 2))))),
             Ex("GATE style: minimum chain cover", "The divisor poset of 60 has largest antichain of size 4 (for example {4, 6, 10, 15}). By Dilworth's theorem, what is the minimum number of chains needed to cover it?", ["Dilworth: minimum chain cover = maximum antichain size."], "**4**", verify=lambda: str(max(len(c) for k in range(1, 13) for c in itertools.combinations(divs(60), k) if all(a % b and b % a for a, b in itertools.combinations(c, 2)))))],
         traps=[("Maximal is not greatest", "Several maximal elements mean no greatest element."),
                ("Least needs comparability to all", "An element is least only if it is below *every* element."),
                ("lub need not exist", "Two minimal upper bounds mean no least upper bound."),
                ("Chain versus antichain", "Chain: all comparable; antichain: none comparable.")],
         quick=[("{2, 3, 6} under divisibility has minimal elements", ["2 only", "2 and 3", "6", "none"], 1, "Neither 2 nor 3 divides the other."),
                ("A finite non-empty poset always has", ["a least element", "a greatest element", "a minimal element", "a total order"], 2, "Follow downward chains until they stop."),
                ("lub of 6 and 10 under divisibility", ["2", "15", "30", "60"], 2, "lcm(6, 10)."),
                ("Dilworth: minimum number of chains covering a poset equals", ["its height", "its largest antichain", "its number of elements", "its number of edges"], 1, "Width equals minimum chain cover.")],
         summary=["Minimal / maximal: nothing below / above. Least / greatest: below / above everything.", "A greatest element is maximal; a poset can have many maximal elements and no greatest.", "lub and glb in divisibility are lcm and gcd.", "Chain: pairwise comparable; antichain: pairwise incomparable.", "Dilworth: minimum chain cover = largest antichain."],
         subs=["Extremal elements"])

# ------------------------------------------------------------------------------------------------ 3.3
A.lesson("engm-po-lattice-props", "Lattices",
         key="A lattice is a poset in which every two elements have a least upper bound (join) and a greatest lower bound (meet). Most questions give a poset and ask whether it is a lattice, or ask for the join and meet of two elements.",
         analogy=("🧗", "Meeting points", "Take two climbers on a mountain of routes. A lattice promises that for any two climbers there is a lowest point above both of them and a highest point below both of them."),
         defs=[("Lattice", "A poset in which every pair a, b has a least upper bound a ∨ b (join) and a greatest lower bound a ∧ b (meet)."),
               ("Bounded lattice", "A lattice with a least element 0 and a greatest element 1."),
               ("Sublattice", "A subset closed under the join and meet of the lattice.")],
         parts=[dict(h="Joins and meets", md="""In a lattice, a ∨ b is the smallest element that is above both, and a ∧ b the largest that is below both. Examples:

| Lattice | Join | Meet |
|---|---|---|
| (ℕ⁺, divides) | lcm | gcd |
| (P(S), ⊆) | union | intersection |
| (ℝ, ≤) or any chain | max | min |

Because ∨ and ∧ are associative and commutative, the join or meet of any finite set exists. Idempotent and absorption laws hold: a ∨ (a ∧ b) = a and a ∧ (a ∨ b) = a. Also a ≤ b ⇔ a ∨ b = b ⇔ a ∧ b = a."""),
                 dict(h="Is a poset a lattice?", md="""Check the joins and meets of the *suspicious* pairs, usually incomparable ones.

1. List the upper bounds of a and b.
2. If there is a unique smallest one, that is a ∨ b; if there are two minimal ones, there is no join, so the poset is **not a lattice**.
3. Repeat for lower bounds (meets).

Counter-example: the poset with a, b below both c and d. The pair (a, b) has two minimal upper bounds c and d, so a ∨ b does not exist. A finite poset with a greatest element and meets for all pairs is automatically a lattice."""),
                 dict(h="Finite lattices and bounds", md="""Every finite lattice is **bounded**: its join of all elements is 1 and its meet of all elements is 0. Every chain is a lattice. Subsets of a lattice need not be sublattices: {2, 3, 12} in the divisor lattice of 12 is not, since 2 ∨ 3 = 6 is outside it.""")],
         examples=[
             Ex("Join and meet in a divisor poset", "In ({1, 2, 3, 4, 6, 12}, |) find 4 ∨ 6 and 4 ∧ 6.", ["4 ∨ 6 = lcm(4, 6) = 12.", "4 ∧ 6 = gcd(4, 6) = 2."], "**12** and **2**.", verify=lambda: "%d and %d" % (lcm(4, 6), math.gcd(4, 6))),
             Ex("A chain", "Is the chain 1 < 2 < 3 < 4 a lattice?", ["The join of a and b is their maximum and the meet their minimum, both in the set."], "**Yes**, every chain is a lattice.", verify=lambda: "Yes, every chain is a lattice"),
             Ex("Not a lattice", "Elements a, b lie below c and d, and nothing else. Is the poset a lattice?", ["The upper bounds of {a, b} are c and d, and they are incomparable, so there is no least upper bound."], "**Not a lattice.**", verify=lambda: "Not a lattice"),
             Ex("Join and meet in D₃₀", "In the divisor lattice of 30 find 6 ∨ 10 and 6 ∧ 10.", ["6 ∨ 10 = lcm = 30.", "6 ∧ 10 = gcd = 2."], "**30** and **2**.", verify=lambda: "%d and %d" % (lcm(6, 10), math.gcd(6, 10))),
             Ex("GATE style: sublattice", "Is S = {1, 2, 3, 12} a sublattice of the divisor lattice of 12?", ["2 ∨ 3 = lcm(2, 3) = 6, which is not in S.", "S is not closed under join."], "**No.**", verify=lambda: "No" if lcm(2, 3) not in (1, 2, 3, 12) else "Yes")],
         traps=[("Every poset is a lattice?", "No: a pair may have no unique lub or glb."),
                ("Meet is not intersection of elements", "Meet is the greatest lower bound, which depends on the order, not a set operation, unless the order is ⊆."),
                ("Subsets that are not sublattices", "A subset can be a lattice by itself without being closed under the parent's join."),
                ("Bounded", "Finite lattices always have 0 and 1; infinite ones may not.")],
         quick=[("A finite lattice always has", ["a least and greatest element", "complements", "a unique atom", "a Boolean structure"], 0, "It is bounded."),
                ("In (ℕ⁺, |) the join of 4 and 6 is", ["2", "10", "12", "24"], 2, "lcm."),
                ("Two incomparable upper bounds with no common lower one among them means", ["a lattice", "no join", "no meet", "a chain"], 1, "The least upper bound is missing."),
                ("a ≤ b is equivalent to", ["a ∨ b = a", "a ∨ b = b", "a ∧ b = b", "a ∨ b = 1"], 1, "The join of a smaller element with a larger one is the larger.")],
         summary=["A lattice has a join (lub) and meet (glb) for every pair.", "Divisor lattice: join lcm, meet gcd; subsets: union, intersection; chains: max, min.", "Two minimal upper bounds mean the poset is not a lattice.", "Finite lattices are bounded; chains are lattices.", "A subset is a sublattice only if closed under ∨ and ∧."],
         subs=["Lattice basics"])

# ------------------------------------------------------------------------------------------------ 3.4
A.lesson("engm-po-divisor", "Divisor lattices",
         key="The divisors of n under divisibility form the lattice Dₙ with join lcm and meet gcd. Its size, height, atoms and Hasse edges all follow from the prime factorisation of n.",
         analogy=("🧬", "Exponent grids", "Write each divisor of n = p^a·q^b as the pair of exponents (i, j). Divisibility is then the componentwise ≤ order on a grid, which makes chains, antichains and covering pairs easy to see."),
         defs=[("Divisor lattice Dₙ", "The set of positive divisors of n ordered by divisibility; join = lcm, meet = gcd."),
               ("Atom", "An element covering the least element; in Dₙ these are the primes dividing n."),
               ("Square-free", "Not divisible by the square of any prime."),
               ("Height", "The number of edges in a longest chain from the least to the greatest element.")],
         parts=[dict(h="Structure from the factorisation", md="""Write n = p₁^a₁ · p₂^a₂ ⋯ p_k^a_k. A divisor is p₁^i₁ ⋯ p_k^i_k with 0 ≤ iⱼ ≤ aⱼ, so

| Fact | Formula |
|---|---|
| number of elements | (a₁ + 1)(a₂ + 1)⋯(a_k + 1) |
| least and greatest element | 1 and n |
| longest chain from 1 to n | a₁ + a₂ + ⋯ + a_k edges |
| atoms | the k primes p₁, …, p_k |
| join, meet | lcm, gcd |
| Hasse edge | a to b when b/a is a prime |

For n = 72 = 2³·3²: (3 + 1)(2 + 1) = 12 elements, longest chain 5 edges, atoms 2 and 3."""),
                 dict(h="Chains and antichains in Dₙ", md="""A maximal chain from 1 to n multiplies by one prime at a time, so it corresponds to an ordering of the prime factors with multiplicity. For a square-free n with k primes there are k! maximal chains; D₃₀ has 3! = 6. The largest antichain is a "middle level" of the lattice; D₃₀ has a middle level of size 3 (the primes, or 6, 10, 15)."""),
                 dict(h="Hasse diagram of Dₙ", md="""Connect a to b when b = a·p for a prime p. D₃₀ is the 3-dimensional cube (8 vertices, 12 edges). D₁₂ = D_{2²·3} has 6 vertices and 7 edges: a 3 × 2 grid. For a prime power pᵏ the lattice is the chain 1 < p < p² < … < pᵏ.""")],
         examples=[
             Ex("Size", "How many elements does the divisor lattice of 72 have?", ["72 = 2³·3²: (3 + 1)(2 + 1)."], "**12**", verify=lambda: str(len(divs(72)))),
             Ex("Height", "How many edges does a longest chain from 1 to 72 have?", ["The prime factors with multiplicity are 2, 2, 2, 3, 3: five."], "**5**", verify=lambda: str(3 + 2)),
             Ex("Join and meet", "In D₃₆ find the join and meet of 4 and 6.", ["lcm(4, 6) = 12 and gcd(4, 6) = 2."], "**12** and **2**.", verify=lambda: "%d and %d" % (lcm(4, 6), math.gcd(4, 6))),
             Ex("Largest antichain of D₃₀", "Find the size of the largest antichain of D₃₀.", ["The primes {2, 3, 5} are pairwise incomparable; so are {6, 10, 15}.", "No four divisors of 30 are pairwise incomparable."], "**3**", verify=lambda: str(max(len(c) for k in range(1, 9) for c in itertools.combinations(divs(30), k) if all(a % b and b % a for a, b in itertools.combinations(c, 2))))),
             Ex("GATE style: maximal chains", "How many maximal chains from 1 to 30 are there in D₃₀?", ["Order the three primes: 3! = 6.", "For example 1 < 2 < 6 < 30 and 1 < 5 < 10 < 30."], "**6**", verify=lambda: str(math.factorial(3)))],
         traps=[("Join is lcm, not the product", "lcm(4, 6) = 12, not 24."),
                ("Boolean needs square-free", "D₁₂ is not Boolean because 12 = 2²·3."),
                ("Chain length versus elements", "A chain with e edges has e + 1 elements."),
                ("Hasse edges", "Only prime-quotient links, never 1–4 in D₁₂.")],
         quick=[("Number of elements of D₆₀ (60 = 2²·3·5)", ["8", "12", "6", "10"], 1, "3·2·2."),
                ("Atoms of D₃₀", ["1", "2", "3", "5"], 2, "The primes 2, 3, 5."),
                ("The join in a divisor lattice is", ["gcd", "lcm", "sum", "product"], 1, "Least common multiple."),
                ("Longest chain in D₁₀₀ (100 = 2²·5²) has how many edges?", ["2", "3", "4", "9"], 2, "2 + 2.")],
         summary=["|Dₙ| = (a₁ + 1)⋯(a_k + 1) for n = p₁^a₁⋯p_k^a_k.", "Longest chain from 1 to n has a₁ + … + a_k edges; atoms are the primes.", "Join = lcm, meet = gcd; a Hasse edge joins a to ap for a prime p.", "For square-free n with k primes there are k! maximal chains.", "A prime power's lattice is a chain."],
         subs=["Divisor poset facts", "Divisor lattice"])

# ------------------------------------------------------------------------------------------------ 3.5
A.lesson("engm-po-boolean", "Distributive, complemented and Boolean lattices",
         key="A lattice is distributive if meet distributes over join, complemented if every element has a complement, and Boolean if both. Finite Boolean lattices are exactly the power sets, with 2ᵏ elements, and Dₙ is Boolean iff n is square-free.",
         analogy=("💡", "Banks of light switches", "A Boolean lattice is every on/off pattern of k switches. The complement of a pattern flips every switch, and combining patterns with 'either' and 'both' mimics union and intersection."),
         defs=[("Complement of a", "An element b with a ∨ b = 1 and a ∧ b = 0."),
               ("Complemented lattice", "A bounded lattice in which every element has at least one complement."),
               ("Distributive lattice", "A lattice with a ∧ (b ∨ c) = (a ∧ b) ∨ (a ∧ c) for all a, b, c."),
               ("Boolean lattice", "A complemented distributive lattice; every finite one is isomorphic to a power set.")],
         parts=[dict(h="Complements", md="""In a bounded lattice with bottom 0 and top 1, b is a complement of a if a and b together reach the top and have nothing in common:

$$a\\vee b=1,\\qquad a\\wedge b=0 .$$

In the power set of {1, 2, 3} the complement of {1} is {2, 3}. In the chain 0 < a < 1 the element a has no complement: a ∨ x = 1 forces x = 1, but a ∧ 1 = a ≠ 0. In a general lattice an element may have several complements; in a distributive lattice it has at most one."""),
                 dict(h="Distributivity and the two forbidden shapes", md="""A lattice is distributive iff it contains neither of two small lattices as a sublattice:

- the **diamond M₃**: 0, 1 and three pairwise incomparable middle elements;
- the **pentagon N₅**: 0 < a < b < 1 and a third element c incomparable with both a and b.

Every chain, every power set and every divisor lattice Dₙ is distributive. The lattice of subspaces of a vector space, or of partitions of a set, is generally not."""),
                 dict(h="Boolean lattices", md="""A **Boolean lattice** (Boolean algebra) is a complemented distributive lattice. Facts:

- every finite Boolean lattice is isomorphic to (P(S), ⊆) for some set S, so it has **2ᵏ elements** where k is its number of atoms;
- the complement of every element is unique, and De Morgan's laws hold;
- sizes such as 6 or 12 are impossible.

For the divisor lattice: d has a complement in Dₙ iff gcd(d, n/d) = 1, and the complement is n/d. So Dₙ is Boolean exactly when n is **square-free**. D₃₀ is Boolean (8 elements, the cube). In D₁₂ the elements 2 and 6 have no complement, so D₁₂ is distributive but not Boolean.""")],
         examples=[
             Ex("Size of a Boolean lattice", "A Boolean lattice has 5 atoms. How many elements does it have?", ["It is isomorphic to the power set of a 5-set."], "**32**", verify=lambda: str(2 ** 5)),
             Ex("Impossible sizes", "Which of 6, 8, 12, 16 can be the size of a finite Boolean lattice?", ["Sizes are powers of 2."], "**8** and **16**.", verify=lambda: " and ".join("%d" % n for n in (6, 8, 12, 16) if n & (n - 1) == 0).replace(" and ", " and ")),
             Ex("A complement in a divisor lattice", "In D₃₀ find the complement of 6.", ["30/6 = 5, and gcd(6, 5) = 1, lcm(6, 5) = 30."], "**5**", verify=lambda: str(30 // 6)),
             Ex("Missing complements", "In D₁₂, which elements have no complement?", ["d has a complement iff gcd(d, 12/d) = 1. Check: 1 and 12 (gcd 1), 3 and 4 (gcd 1).", "2: gcd(2, 6) = 2; 6: gcd(6, 2) = 2."], "**2** and **6**.", verify=lambda: " and ".join(str(d) for d in divs(12) if math.gcd(d, 12 // d) != 1)),
             Ex("GATE style: is it Boolean?", "Is (D₇₂, |) a Boolean algebra, a distributive lattice, or neither?", ["Every divisor lattice is distributive.", "72 = 2³·3² is not square-free, so it is not complemented."], "Distributive, **not** Boolean.", verify=lambda: "Distributive, not Boolean" if any(72 % (p * p) == 0 for p in (2, 3)) else "?")],
         traps=[("Complement versus inverse", "A complement needs both a ∨ b = 1 and a ∧ b = 0."),
                ("Chains are not complemented", "The middle elements of a chain of length ≥ 3 have no complement."),
                ("Distributive is not Boolean", "Dₙ is always distributive; it is Boolean only when n is square-free."),
                ("Sizes", "A Boolean lattice always has 2ᵏ elements.")],
         quick=[("Which size is possible for a finite Boolean lattice?", ["6", "12", "16", "20"], 2, "A power of 2."),
                ("In D₃₀ the complement of 10 is", ["3", "5", "6", "15"], 0, "30/10."),
                ("The pentagon N₅ is", ["distributive", "non-distributive", "Boolean", "a chain"], 1, "It is one of the two forbidden sublattices."),
                ("D₁₈ (18 = 2·3²) is", ["Boolean", "distributive but not Boolean", "not a lattice", "not bounded"], 1, "18 is not square-free.")],
         summary=["Complement of a: b with a ∨ b = 1 and a ∧ b = 0.", "Distributive ⇔ no M₃ or N₅ sublattice; complements are then unique.", "Boolean = complemented + distributive; finite ones have 2ᵏ elements.", "Dₙ is Boolean iff n is square-free; the complement of d is n/d.", "Divisor lattices and power sets are always distributive."],
         subs=["Boolean lattices"])
