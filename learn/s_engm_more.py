"""Engineering Mathematics: extra examples, checks, traps and explanations so every sub-chapter is complete on its own."""
import itertools
import math
from fractions import Fraction as F

from content import g_engm2 as G2
from content import g_la as LA
from learn import Ex
from learn.s_engm import s

C = math.comb
P3 = list(itertools.product((0, 1), repeat=3))

# ---------------- logic
s.more("engm-logic-propositions",
       sections=[dict(h="Building a truth table", md="""List the 2ⁿ assignments in binary order (000, 001, …, 111), then add one column per sub-formula from the inside out. The final column is the formula. With three variables there are 8 rows; with four, 16.

| p | q | p ∧ q | p ∨ q | p → q | p ↔ q | p ⊕ q |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 | 1 | 0 |""")],
       examples=[Ex("Exclusive or", "For how many of the 8 assignments is p ⊕ q ⊕ r true?", ["⊕ is true when an odd number of inputs are 1.", "Rows with one or three 1s: 3 + 1 = **4**."], "**4**", verify=lambda: str(sum(1 for t in P3 if sum(t) % 2)))],
       quick=[("p → q is false when", ["p = 0, q = 0", "p = 0, q = 1", "p = 1, q = 0", "p = 1, q = 1"], 2, "True implies false."), ("Rows in the truth table of a 4-variable formula", ["8", "16", "32", "4"], 1, "2⁴.")],
       traps=[("Implication with false premise", "p → q is TRUE when p is false."), ("XOR vs OR", "p ⊕ q is false when both are true; p ∨ q is true.")])
s.more("engm-lg-equiv",
       quick=[("p → q ≡", ["q → p", "¬p ∨ q", "p ∧ ¬q", "¬q → p"], 1, "Implication law.")],
       traps=[("Distributing ¬", "¬(p ∧ q) is ¬p ∨ ¬q, not ¬p ∧ ¬q."), ("CNF vs DNF", "CNF is an AND of clauses; DNF an OR of terms.")],
       examples=[Ex("Simplify", "Simplify (p ∧ q) ∨ (p ∧ ¬q).", ["Distribution: p ∧ (q ∨ ¬q) = p ∧ T.", "= **p**."], "**p**", verify=lambda: "p" if all(((p and q) or (p and not q)) == p for p, q, _ in P3) else "?")])
s.more("engm-lg-fol",
       examples=[Ex("Negating a translation", "Negate ‘every student passed some exam’, ∀x ∃y P(x, y).", ["¬∀x ∃y P ≡ ∃x ∀y ¬P(x, y).", "‘Some student failed every exam.’"], "**∃x ∀y ¬P(x, y)**", verify=lambda: "∃x ∀y ¬P(x, y)")],
       sections=[dict(h="A translation procedure", md="""1. Fix the domain and name the predicates (S(x): x is a student, P(x, y): x passed y).
2. Find the quantifier words: every/all/each → ∀; some/there is/at least one → ∃; no/none → ∀ … ¬ (or ¬∃).
3. Attach the restricting predicate with → under ∀ and with ∧ under ∃.
4. Keep the order of quantifiers as the sentence states it.
5. Check on a tiny model (two elements) that the formula says what the sentence says.""")])
s.more("engm-sets-counting",
       quick=[("A × ∅ =", ["A", "∅", "{∅}", "undefined"], 1, "No pairs."), ("|P(P(∅))|", ["0", "1", "2", "4"], 2, "P(∅) = {∅} has 1 element; its power set has 2.")],
       sections=[dict(h="Set identities", md="""- Commutative, associative and distributive laws hold for ∪ and ∩.
- De Morgan: (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ, (A ∩ B)ᶜ = Aᶜ ∪ Bᶜ.
- A − B = A ∩ Bᶜ; A Δ B = (A ∪ B) − (A ∩ B).
- A ⊆ B ⇔ A ∪ B = B ⇔ A ∩ B = A.
- |A × B| = |A|·|B|, and A × B ≠ B × A unless A = B or one is empty.""")])
s.more("engm-st-incl", traps=[("Using the product for overlaps", "Overlaps of ‘divisible by a’ and ‘by b’ use lcm(a, b), not a·b, when a and b share a factor.")],
       sections=[dict(h="Three-set formula", md="""|A ∪ B ∪ C| = |A| + |B| + |C| − |A ∩ B| − |A ∩ C| − |B ∩ C| + |A ∩ B ∩ C|.

The number of elements in **none** of the sets is the total minus this union. For k sets the signs alternate: + for odd-sized intersections, − for even-sized ones.""")])
s.more("engm-relations",
       examples=[Ex("Checking properties", "R = {(1,1), (2,2), (3,3), (1,2), (2,1)} on {1, 2, 3}. Which properties hold?", ["All diagonal pairs present: reflexive.", "(1,2) and (2,1) both present: symmetric, not antisymmetric.", "Transitivity: (1,2),(2,1) ⇒ (1,1) ✓; all checks pass: transitive.", "So R is an **equivalence relation** with classes {1, 2} and {3}."], "Reflexive, symmetric, transitive (an equivalence relation).", verify=lambda: "Reflexive, symmetric, transitive (an equivalence relation)."),
                 Ex("Antisymmetric and symmetric", "Which relation on {1, 2} is both symmetric and antisymmetric and reflexive?", ["Symmetric + antisymmetric forbids any (a, b) with a ≠ b.", "Reflexive adds (1,1), (2,2): **R = {(1,1), (2,2)}**, the equality relation."], "**{(1,1), (2,2)}**", verify=lambda: "{(1,1), (2,2)}")])
s.more("engm-st-relations-count", take=[("engm-relations", "Q1")], traps=[("Counting ordered pairs", "A set of n elements has n² ordered pairs, not C(n, 2).")])
s.more("engm-functions",
       examples=[Ex("Inverse function", "f(x) = (2x + 1)/3 on ℝ. Find f⁻¹(5).", ["Solve 5 = (2x + 1)/3: 2x + 1 = 15, x = **7**."], "**7**", verify=lambda: str((5 * 3 - 1) // 2)),
                 Ex("Is it a function?", "Is {(1, a), (2, b), (1, c)} a function from {1, 2} to {a, b, c}?", ["1 is paired with two outputs (a and c).", "**No**: each input needs exactly one output."], "**No**", verify=lambda: "No")],
       quick=[("x ↦ x³ on ℝ → ℝ is", ["injective only", "surjective only", "bijective", "neither"], 2, "Strictly increasing and unbounded."), ("If g∘f is onto, then", ["f is onto", "g is onto", "both are onto", "neither need be"], 1, "g must hit everything.")],
       traps=[("Codomain matters", "x² is onto [0, ∞) but not onto ℝ.")])
s.more("engm-posets-lattices",
       examples=[Ex("Is it a partial order?", "Is ‘x divides y’ on ℤ (including negatives) a partial order?", ["1 | −1 and −1 | 1 but 1 ≠ −1: antisymmetry fails.", "**No** (it is a partial order only on the positive integers)."], "**No**", verify=lambda: "No"),
                 Ex("Hasse diagram of D₁₂", "How many edges does the Hasse diagram of the divisors of 12 have?", ["Covering pairs (quotient prime): 1–2, 1–3, 2–4, 2–6, 3–6, 4–12, 6–12.", "**7** edges."], "**7**", verify=lambda: str(sum(1 for a in [1, 2, 3, 4, 6, 12] for b in [1, 2, 3, 4, 6, 12] if b % a == 0 and b // a in (2, 3))))],
       quick=[("A partial order must be", ["symmetric", "antisymmetric", "total", "irreflexive"], 1, "Reflexive, antisymmetric, transitive."), ("⊆ on the subsets of a set is", ["a total order", "a partial order", "an equivalence", "not transitive"], 1, "Sets can be incomparable.")])
s.more("engm-po-extremal", quick=[("{2, 3, 6} under divisibility: minimal elements", ["2 only", "2 and 3", "6", "none"], 1, "Neither divides the other.")])
s.more("engm-groups", quick=[("(ℤ, −) is", ["a group", "not associative", "a monoid", "abelian"], 1, "(a − b) − c ≠ a − (b − c).")])
s.more("engm-gr-special", take=[("engm-gr-counting", "Q3")],
       examples=[Ex("Hypercube", "Edges of Q₅?", ["n·2ⁿ⁻¹ = 5·16 = **80**."], "**80**", verify=lambda: str(5 * 2 ** 4))],
       traps=[("Bipartite test", "One odd cycle is enough to rule it out.")])
s.more("engm-counting-basics",
       examples=[Ex("Committees with a condition", "A committee of 4 from 6 men and 5 women must contain at least one woman. How many?", ["Total C(11, 4) = 330; all-men C(6, 4) = 15.", "330 − 15 = **315**."], "**315**", verify=lambda: str(C(11, 4) - C(6, 4))),
                 Ex("Ordered vs unordered", "From 8 runners, how many ways to award gold, silver, bronze? How many ways to pick 3 finalists?", ["Ordered: P(8, 3) = 336.", "Unordered: C(8, 3) = 56."], "**336** and **56**", verify=lambda: "%d and %d" % (math.perm(8, 3), C(8, 3)))],
       quick=[("P(7, 2)", ["21", "42", "49", "14"], 1, "7·6."), ("C(10, 8)", ["45", "90", "80", "10"], 0, "= C(10, 2).")])
s.more("engm-cb-methods", quick=[("Positive solutions of x + y + z = 7", ["15", "21", "36", "6"], 0, "C(6, 2).")], traps=[("Distinct objects", "Stars and bars is for identical objects; distinct objects into k boxes give kⁿ.")])
s.more("engm-cb-binomial",
       examples=[Ex("Sum of coefficients", "Sum of the coefficients of (2x − 1)⁷?", ["Put x = 1: (2 − 1)⁷ = **1**."], "**1**", verify=lambda: str((2 - 1) ** 7))],
       quick=[("Coefficient of x² in (1 + x)⁵", ["5", "10", "20", "1"], 1, "C(5, 2)."), ("Shortest paths from (0,0) to (2,2)", ["4", "6", "8", "2"], 1, "C(4, 2).")],
       traps=[("Forgetting the constant's power", "In (ax + b)ⁿ the term carries aⁿ⁻ᵏbᵏ."), ("Alternating sum", "Σ(−1)ᵏC(n, k) = 0 for n ≥ 1."), ("Path counts", "Count steps, not grid squares.")],
       sections=[dict(h="Identities worth knowing", md="""- Σₖ C(n, k) = 2ⁿ; Σₖ (−1)ᵏC(n, k) = 0.
- Σₖ k·C(n, k) = n·2ⁿ⁻¹.
- Vandermonde: Σₖ C(m, k)C(n, r − k) = C(m + n, r).
- Hockey stick: Σᵢ₌ᵣⁿ C(i, r) = C(n + 1, r + 1).
- Catalan number Cₙ = C(2n, n)/(n + 1) counts lattice paths that never go above the diagonal.""")])
s.more("engm-cb-genfun", quick=[("x/(1 − x) generates", ["1, 1, 1, …", "0, 1, 1, 1, …", "1, 2, 3, …", "0, 1, 2, …"], 1, "Starts at x¹.")])
s.more("engm-matrices-determinants", take=[("engm-matrices-determinants", "T2")], traps=[("AB = 0", "Neither factor need be the zero matrix.")])
s.more("engm-la-inverse",
       quick=[("Inverse of an orthogonal matrix", ["A", "Aᵀ", "−A", "adj A"], 1, "AᵀA = I.")],
       sections=[dict(h="Inverse by row reduction", md="""Write [A | I] and row-reduce until the left block becomes I; the right block is then A⁻¹. If a zero row appears on the left, A is singular. For 3 × 3 matrices this is often quicker than computing nine cofactors.""")])
s.more("engm-la-cayley", quick=[("For 2×2 A with trace 5 and det 6, A² =", ["5A − 6I", "6A − 5I", "5A + 6I", "A + I"], 0, "A² − 5A + 6I = 0.")],
       traps=[("Repeated eigenvalues", "Need as many independent eigenvectors as the multiplicity.")])
s.more("engm-differentiation-mvt",
       sections=[dict(h="Standard derivatives", md="""| f(x) | f′(x) |
|---|---|
| xⁿ | nxⁿ⁻¹ |
| eˣ, aˣ | eˣ, aˣ ln a |
| ln x | 1/x |
| sin x, cos x | cos x, −sin x |
| tan x | sec² x |
| sin⁻¹ x | 1/√(1 − x²) |
| tan⁻¹ x | 1/(1 + x²) |

**Logarithmic differentiation:** for y = xˣ, ln y = x ln x, so y′/y = ln x + 1 and y′ = xˣ(ln x + 1).""")])
s.more("engm-ca-mvt",
       quick=[("MVT for f(x) = x² on [2, 6]: c =", ["3", "4", "5", "8"], 1, "Midpoint.")],
       traps=[("Open vs closed interval", "Continuity on [a, b], differentiability on (a, b)."), ("Rolle needs equal values", "f(a) = f(b) is required.")],
       sections=[dict(h="Using the theorems", md="""- To **find c**, solve f′(c) = (f(b) − f(a))/(b − a) and keep only roots inside (a, b).
- To **bound a function**: if |f′| ≤ M on [a, b] then |f(b) − f(a)| ≤ M(b − a).
- To **count roots**: between two roots of f there is a root of f′ (Rolle), so a polynomial of degree n has at most n real roots.""")])
s.more("engm-ca-taylor", traps=[("Factorials", "The xᵏ coefficient divides by k!."), ("Harmonic series", "Σ1/n diverges although its terms → 0.")],
       examples=[Ex("Taylor about a point", "Coefficient of (x − 1)² in the Taylor series of eˣ about x = 1?", ["f″(1)/2! = e/2."], "**e/2**", verify=lambda: "e/2")])
s.more("engm-ca-integration-tech", take=[("engm-ca-optimise-integrate", "E5")])
s.more("engm-pb-bayes", quick=[("P(B) by total probability with P(A)=0.3, P(B|A)=0.5, P(B|Aᶜ)=0.2", ["0.29", "0.35", "0.15", "0.7"], 0, "0.15 + 0.14.")])

s.more("engm-po-boolean", sections=[dict(h="Complements and distributivity", md="""In a bounded lattice with bottom 0 and top 1, b is a **complement** of a when a ∨ b = 1 and a ∧ b = 0.

- **Complemented:** every element has at least one complement.
- **Distributive:** a ∧ (b ∨ c) = (a ∧ b) ∨ (a ∧ c) for all a, b, c. In a distributive lattice each element has **at most one** complement.
- The two smallest non-distributive lattices are the diamond **M₃** (0, 1 and three incomparable middle elements) and the pentagon **N₅**. A lattice is distributive iff neither appears as a sublattice.
- **Boolean lattice:** complemented and distributive. Every finite one is isomorphic to the power set of its atoms, so it has 2ᵏ elements."""),
       dict(h="Divisor lattices as Boolean lattices", md="""In Dₙ the bottom is 1, the top is n, join is lcm and meet is gcd. A divisor d has a complement iff gcd(d, n/d) = 1, and the complement is n/d. So Dₙ is Boolean exactly when n is **square-free** (no prime squared divides n): D₃₀ is Boolean (8 elements, a cube), D₁₂ is not (2 and 6 have no complement).""")])
s.more("engm-cb-arrange", sections=[dict(h="Arrangements with repeated objects", md="""n objects of which n₁ are alike of one kind, n₂ of another, …: the n! orderings overcount each distinct word n₁!·n₂!·… times, so

    distinct arrangements = n! / (n₁! · n₂! · …)

MISSISSIPPI (11 letters: I×4, S×4, P×2, M×1) has 11!/(4!·4!·2!) = 34650 arrangements."""),
       dict(h="Circles, necklaces and position constraints", md="""- **Circular**: n people round a table, rotations equal: (n − 1)!.
- **Necklace / garland** (can be turned over): (n − 1)!/2 for n ≥ 3.
- **Together**: glue the k people into a block → (n − k + 1)!·k!.
- **Never adjacent**: arrange the others, then choose gaps: e.g. m boys then k girls in the m + 1 gaps: m!·P(m + 1, k).
- **Fixed relative order** of k items: divide by k!.""")])
s.more("engm-gr-trees", sections=[dict(h="Equivalent definitions and counting leaves", md="""For a graph G on n vertices the following are equivalent: G is a tree; G is connected with n − 1 edges; G is acyclic with n − 1 edges; between any two vertices there is exactly one path; G is minimally connected (every edge is a bridge).

**Leaves:** from Σdeg = 2(n − 1), a tree with nᵢ vertices of degree i satisfies n₁ = 2 + n₃ + 2n₄ + 3n₅ + … (degree-2 vertices do not matter). Every tree with at least 2 vertices has at least 2 leaves.""")])
s.more("engm-pb-conditional", sections=[dict(h="Independence of several events", md="""A, B, C are **mutually independent** if every sub-collection multiplies: P(A ∩ B) = P(A)P(B), P(A ∩ C) = P(A)P(C), P(B ∩ C) = P(B)P(C) and P(A ∩ B ∩ C) = P(A)P(B)P(C). Pairwise independence alone is weaker.

If A and B are independent, so are A and Bᶜ, Aᶜ and B, Aᶜ and Bᶜ. The chain rule for three events: P(A ∩ B ∩ C) = P(A)·P(B | A)·P(C | A ∩ B), which is how draws without replacement are computed.""")])
s.more("engm-st-relations-count", sections=[dict(h="Why the formulas hold", md="""Picture the n × n relation matrix. The n diagonal cells and the n(n − 1)/2 symmetric pairs of off-diagonal cells are independent choices:

- **reflexive** fixes the diagonal to 1: 2 to the power of the n² − n off-diagonal cells;
- **symmetric** makes each off-diagonal pair one choice: 2ⁿ · 2^(n(n−1)/2) = 2^(n(n+1)/2);
- **antisymmetric** allows, for each off-diagonal pair, 00, 10 or 01 (not 11): 2ⁿ · 3^(n(n−1)/2);
- **asymmetric** is antisymmetric with an empty diagonal: 3^(n(n−1)/2).""")])
s.more("engm-posets-lattices", traps=[("Hasse diagram direction", "Smaller elements are drawn lower; arrows are omitted.")])
s.more("engm-counting-basics", traps=[("Order matters?", "Decide before choosing P or C.")])
s.more("engm-la-inverse", traps=[("Singular matrices", "No inverse when det = 0, even if no row is zero.")])
s.more("engm-differentiation-mvt", quick=[("d/dx tan⁻¹ x", ["1/(1 + x²)", "1/√(1 − x²)", "sec² x", "−1/(1 + x²)"], 0, "Standard."), ("d/dx xˣ", ["x·xˣ⁻¹", "xˣ ln x", "xˣ(1 + ln x)", "ln x"], 2, "Logarithmic differentiation.")])

# ---------------- audit (2026-11-16): one explanation per idea, every piece under the sub-topic it belongs to
LGP, LGQ, LGF, LGO = "engm-logic-propositions", "engm-logic-quantifiers", "engm-lg-forms", "engm-lg-fol"
s.more("engm-lg-equiv", drop=[(LGF, "S1")])
s.more("engm-logic-quantifiers", drop=[(LGO, "S1")])
s.more("engm-lg-fol", drop=[(LGQ, "S2")])
s.more("engm-sets-counting", drop=[("engm-sets-counting", "B2")])
s.more("engm-cb-arrange", take=[("engm-sets-counting", "B2")])
s.more("engm-po-lattice-props", drop=[("engm-po-lattice-props", "S0")])
s.more("engm-groups", drop=[("engm-groups", "S0")])
s.more("engm-gp-cyclic", drop=[("engm-groups", "S3"), ("engm-gp-cyclic", "E3")])
s.more("engm-gr-euler", drop=[("engm-gr-colour", "S1")])
s.more("engm-gr-colour", drop=[("engm-gr-colour", "S0")])
s.more("engm-cb-methods", drop=[("engm-counting-basics", "S2")])
s.more("engm-matrices-determinants", drop=[("engm-matrices-determinants", "S0")])
s.more("engm-la-determinants", drop=[("engm-matrices-determinants", "S1")])
s.more("engm-la-inverse", drop=[("engm-matrices-determinants", "S2 E3")])
s.more("engm-la-rank", drop=[("engm-matrices-determinants", "S3")])
s.more("engm-la-systems", drop=[("engm-linear-systems-eigen", "S0")])
s.more("engm-la-eigen-compute", drop=[("engm-linear-systems-eigen", "S1"), ("engm-la-eigen-compute", "E0")])
s.more("engm-la-eigen-functions", drop=[("engm-linear-systems-eigen", "S2")])
s.more("engm-la-cayley", drop=[("engm-la-eigen-compute", "S2"), ("engm-la-problem-set", "S0 S1 E5")])
s.more("engm-limits-continuity", drop=[("engm-limits-continuity", "S1"), ("engm-ca-limits-technique", "E0")], take=[("engm-limits-continuity", "P0")])
s.more("engm-ca-continuity", drop=[("engm-limits-continuity", "P0")])
s.more("engm-ca-taylor", drop=[("engm-ca-derivatives", "S0 S1")])
s.more("engm-ca-maxmin", drop=[("engm-ca-optimise-integrate", "S0")])
s.more("engm-maxima-minima-integration", drop=[("engm-ca-optimise-integrate", "S1")])
s.more("engm-pb-bayes", drop=[("engm-pb-bayes", "S0")])
s.more("engm-pb-distributions", drop=[("engm-random-variables-distributions", "S2")])
s.more("engm-probability-bayes", drop=[("engm-pb-problems", "E3")])
s.more("engm-gr-planar", drop=[("engm-gr-problems", "E3")])
s.more("engm-la-systems", drop=[("engm-la-problem-set", "E5")])
s.more("engm-maxima-minima-integration", drop=[("engm-ca-optimise-integrate", "E4")])
s.more("engm-gp-cyclic", sections=[dict(h="Subgroups and elements of a cyclic group", md="""Let G = ⟨g⟩ have order n. Then:

- every subgroup of G is cyclic, and for each divisor d of n there is **exactly one** subgroup of order d, namely ⟨g^(n/d)⟩;
- gᵏ has order n/gcd(k, n), so gᵏ generates G exactly when gcd(k, n) = 1, giving φ(n) generators;
- the number of elements of order d is φ(d), and summing over the divisors gives Σ φ(d) = n.

Example: in Z₁₂ the subgroups have orders 1, 2, 3, 4, 6, 12, and the elements of order 6 are 2 and 10 (φ(6) = 2).""")])
# repeated checks and mistake cards (one of each pair kept)
s.more("engm-functions", drop=[("engm-functions", "Q2")])
s.more("engm-st-functions-count", drop=[("engm-functions", "Q0")])
s.more("engm-gp-structure", drop=[("engm-gp-cyclic", "T0")])
s.more("engm-gp-perm", drop=[("engm-gp-cyclic", "T1")])
s.more("engm-ca-mvt", drop=[("engm-ca-derivatives", "T0 Q1")])
s.more("engm-ca-taylor", drop=[("engm-ca-limits-technique", "T3")])
s.more("engm-probability-bayes", drop=[("engm-pb-problems", "Q0")])
s.more("engm-gr-trees", drop=[("engm-gr-counting", "Q1 T3")])
s.more("engm-limits-continuity", drop=[("engm-ca-limits-technique", "Q0")])
s.more("engm-functions", quick=[("f: ℝ → ℝ, f(x) = 3x − 2 is", ["one-to-one only", "onto only", "bijective", "neither"], 2, "Linear with non-zero slope."),
                                ("A function from {1, 2, 3} to {a, b} can be", ["one-to-one", "onto", "bijective", "none of these"], 1, "3 inputs, 2 outputs: onto is possible, one-to-one is not.")])
s.more("engm-gr-trees", quick=[("Number of labelled trees on 4 vertices", ["4", "12", "16", "64"], 2, "4² by Cayley."), ("Every tree with n ≥ 2 vertices has at least", ["1 leaf", "2 leaves", "n/2 leaves", "no leaves"], 1, "The ends of a longest path.")],
       traps=[("Adding an edge", "One extra edge always creates exactly one cycle."), ("Forest edge count", "A forest with c trees has n − c edges, not n − 1.")])
s.more("engm-ca-mvt", quick=[("Rolle's theorem applies to |x| on [−1, 1]?", ["yes", "no", "only at 0", "only for c = 0"], 1, "Not differentiable at 0.")])
s.more("engm-ca-taylor", traps=[("Ratio test limit 1", "L = 1 decides nothing; use another test."), ("Expanding about the wrong point", "Taylor about a uses powers of (x − a).")])
