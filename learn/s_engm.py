"""Engineering Mathematics: sections → chapters (one per syllabus topic) → sub-chapters (one per sub-topic)."""
import itertools
import math
from fractions import Fraction as F

from content import g_engm2 as G2
from content import g_la as LA
from learn import Ex
from learn.compose import Spec

s = Spec("ENGM")
C = math.comb
LGP, LGQ, LGF, LGO, LGM = "engm-logic-propositions", "engm-logic-quantifiers", "engm-lg-forms", "engm-lg-fol", "engm-lg-models"
SC, RL, FN, RC, FC, CE = "engm-sets-counting", "engm-relations", "engm-functions", "engm-st-relations-count", "engm-st-functions-count", "engm-st-closures-eq"
PL, PD, PP, PX = "engm-posets-lattices", "engm-po-divisor", "engm-po-lattice-props", "engm-po-problems"
GG, GC, GS, GX = "engm-groups", "engm-gp-cyclic", "engm-gp-structure", "engm-gp-problems"
GB, GT, GI, GK, GZ = "engm-graph-basics", "engm-graph-trees-planar-colouring", "engm-gr-counting", "engm-gr-colour", "engm-gr-problems"
CBS, PIE, CM, CR, CP = "engm-counting-basics", "engm-pie-pigeonhole-recurrence", "engm-cb-methods", "engm-cb-recurrence", "engm-cb-pigeonhole"
MD, LS, LD, LR, LI, LY, LE, LF, LX = ("engm-matrices-determinants", "engm-linear-systems-eigen", "engm-la-determinants", "engm-la-rank", "engm-la-inverse",
                                      "engm-la-systems", "engm-la-eigen-compute", "engm-la-eigen-functions", "engm-la-problem-set")
LC, DM, MI, CL, CD, CO = "engm-limits-continuity", "engm-differentiation-mvt", "engm-maxima-minima-integration", "engm-ca-limits-technique", "engm-ca-derivatives", "engm-ca-optimise-integrate"
PB, RV, PBB, PBD, PBX = "engm-probability-bayes", "engm-random-variables-distributions", "engm-pb-bayes", "engm-pb-distributions", "engm-pb-problems"

# =====================================================================================================
s.section("Discrete Mathematics")
s.chapter("Propositional & First-Order Logic")
s.sub(LGP, "Propositions, connectives and truth tables",
      "A proposition is a statement that is either true or false. Six connectives (¬, ∧, ∨, →, ↔, ⊕) build compound statements, and a truth table lists the value of a formula for every one of the 2ⁿ assignments of its n variables.",
      ["A proposition has exactly one truth value.", "¬, ∧, ∨, →, ↔, ⊕: learn each truth table cold.", "n variables ⇒ 2ⁿ rows.", "∨ is inclusive: true when both sides are true.", "Precedence: ¬, then ∧, then ∨, then →, then ↔."],
      take=[(LGP, "B0 S0 S1 Q0 Q3 T2 N0")], subs=["Equivalences", "Logical forms"], analogy=LGP, widget="truth",
      hint="Type a formula and watch the truth table fill in, one row per assignment.",
      examples=[Ex("Reading a truth table", "For how many of the 8 assignments of (p, q, r) is (p ∨ q) ∧ ¬r true?",
                   ["¬r forces r = 0 (4 rows remain).", "p ∨ q is false only for p = q = 0, so 3 of those 4 rows work.", "Answer **3**."], "**3**",
                   verify=lambda: str(sum(1 for p, q, r in itertools.product((0, 1), repeat=3) if (p or q) and not r))),
                Ex("Biconditional", "When is p ↔ ¬q true?", ["p ↔ ¬q is true when p and ¬q agree, i.e. when p and q DIFFER.", "So it equals p ⊕ q: true for (1, 0) and (0, 1)."], "Exactly when **p ≠ q** (2 of 4 rows).",
                   verify=lambda: "Exactly when p ≠ q (%d of 4 rows)" % sum(1 for p, q in itertools.product((0, 1), repeat=2) if p == (not q)))])
s.sub(LGF, "Implication, converse and contrapositive",
      "P → Q is false in exactly one case (P true, Q false) and equals ¬P ∨ Q. Its contrapositive ¬Q → ¬P is equivalent to it; the converse and the inverse are not.",
      ["P → Q ≡ ¬P ∨ Q.", "Only the contrapositive is equivalent.", "¬(P → Q) ≡ P ∧ ¬Q.", "Vacuous truth: false premise ⇒ true implication.", "Converse and inverse are equivalent to each other."],
      take=[(LGF, "S0 E0 E1 Q0 Q2 Q3 T0 T1 T3"), (LGP, "S2 E2 T0 T1")], subs=["Logical forms"], analogy=LGF)
s.sub("engm-lg-equiv", "Logical equivalences and normal forms",
      "Two formulas are equivalent if they agree on every row. A short list of laws (De Morgan, distribution, absorption, implication) rewrites any formula, and every formula has a conjunctive (CNF) and a disjunctive (DNF) normal form.",
      ["De Morgan: ¬(P ∧ Q) ≡ ¬P ∨ ¬Q.", "P → Q ≡ ¬P ∨ Q; P → (Q → R) ≡ (P ∧ Q) → R.", "Absorption: P ∨ (P ∧ Q) ≡ P.", "CNF = AND of ORs; DNF = OR of ANDs.", "{¬, ∧}, {¬, ∨}, {NAND}, {NOR} are functionally complete."],
      take=[(LGP, "B1 S3 S4 E3 P0 P2 T3"), (LGF, "S1 E4")], subs=["Equivalences"], analogy=("🔁", "Different words, same meaning", "‘Not (rain and cold)’ and ‘not rain or not cold’ describe exactly the same days. Equivalence laws are the grammar that lets you swap one wording for the other."),
      examples=[Ex("DNF from a truth table", "Write a DNF for the function that is true exactly when p = 1, q = 0 or p = 0, q = 1.", ["One minterm per true row: (p ∧ ¬q) and (¬p ∧ q).", "DNF: **(p ∧ ¬q) ∨ (¬p ∧ q)**, which is p ⊕ q."], "**(p ∧ ¬q) ∨ (¬p ∧ q)**",
                   verify=lambda: "(p ∧ ¬q) ∨ (¬p ∧ q)" if all(((p and not q) or (not p and q)) == (p != q) for p, q in itertools.product((0, 1), repeat=2)) else "?")],
      quick=[("¬(p ∨ q) ≡", ["¬p ∨ ¬q", "¬p ∧ ¬q", "p ∧ q", "¬p → q"], 1, "De Morgan."), ("p ∨ (p ∧ q) ≡", ["q", "p", "p ∧ q", "p ∨ q"], 1, "Absorption.")])
s.sub(LGM, "Satisfiability, validity and counting models",
      "A formula is valid (a tautology) if true in every row, satisfiable if true in some row, and a contradiction if true in none. Counting the true rows (models) is a counting problem: use the structure of the formula.",
      ["Valid = all rows; satisfiable = some row; contradiction = no row.", "F valid ⇔ ¬F unsatisfiable.", "k-literal conjunction over n variables: 2^(n−k) models.", "k-literal clause: 2ⁿ − 2^(n−k) models.", "2^(2ⁿ) Boolean functions of n variables."],
      take=[(LGM, "S0 S1 E0 E1 E2 E3 E4 Q0 Q1 Q2 Q3 T0 T1 T2 T3"), (LGP, "E1 Q1 Q2 P1 N1"), (LGF, "E2 E3 Q1 T2")], subs=["Satisfiability", "Counting models", "Boolean functions count"], analogy=LGM)
s.sub(LGQ, "Predicates and quantifiers",
      "A predicate becomes a proposition once its variables are fixed or quantified. ∀ means ‘for every element of the domain’, ∃ ‘for at least one’. Negation flips each quantifier, and the order of mixed quantifiers matters.",
      ["¬∀x P ≡ ∃x ¬P; ¬∃x P ≡ ∀x ¬P.", "∃y∀x R implies ∀x∃y R, not conversely.", "Same quantifiers commute; mixed do not.", "∀ distributes over ∧, ∃ over ∨.", "The domain decides truth: always state it."],
      take=[(LGQ, "B0 B1 S0 S1 S3 E0 E1 Q0 Q3 T1 T2 T3 P0 P1"), (LGO, "S1 E1 E3 E4 Q1 Q2 T2 T3")], subs=["First-order logic"], analogy=LGQ)
s.sub(LGO, "Translating English into first-order logic",
      "Most translation questions test two habits: ∀ goes with →, ∃ goes with ∧, and the order ∀x∃y versus ∃y∀x decides whether each x gets its own y or one y serves all.",
      ["All A are B: ∀x (A(x) → B(x)).", "Some A is B: ∃x (A(x) ∧ B(x)).", "No A is B: ∀x (A(x) → ¬B(x)).", "‘Every x has some y’: ∀x∃y.", "‘One y for all x’: ∃y∀x."],
      take=[(LGO, "S0 E0 E2 Q0 Q3 T0 T1"), (LGQ, "S2 Q1 T0 N0")], subs=["FOL translation"], analogy=LGO)
s.sub("engm-lg-inference", "Rules of inference",
      "An argument is valid if every assignment that makes all premises true also makes the conclusion true. Valid patterns (modus ponens, modus tollens, syllogisms, resolution) can be chained; the classic fallacies are affirming the consequent and denying the antecedent.",
      ["Modus ponens: P → Q, P ⊢ Q.", "Modus tollens: P → Q, ¬Q ⊢ ¬P.", "Hypothetical syllogism chains implications.", "Resolution: P ∨ Q, ¬P ∨ R ⊢ Q ∨ R.", "Fallacies: affirming the consequent, denying the antecedent."],
      take=[(LGP, "B2 E0"), (LGQ, "S4 E2 Q2 P2 N1")], subs=["Rules of inference"], analogy=("⚖️", "A sound chain", "Each rule is a link that never breaks: if the premises are true, the conclusion must be. A fallacy is a link that only looks solid."),
      sections=[dict(h="Valid rules and fallacies", md="""| Name | Form | Valid? |
|---|---|---|
| Modus ponens | P → Q, P ⊢ Q | yes |
| Modus tollens | P → Q, ¬Q ⊢ ¬P | yes |
| Hypothetical syllogism | P → Q, Q → R ⊢ P → R | yes |
| Disjunctive syllogism | P ∨ Q, ¬P ⊢ Q | yes |
| Resolution | P ∨ Q, ¬P ∨ R ⊢ Q ∨ R | yes |
| Affirming the consequent | P → Q, Q ⊢ P | **no** |
| Denying the antecedent | P → Q, ¬P ⊢ ¬Q | **no** |

To test any argument, look for a row where every premise is true and the conclusion false. If such a row exists the argument is invalid.""")],
      examples=[Ex("Spot the fallacy", "‘If it rains the road is wet. The road is wet. So it rained.’ Valid?", ["This is P → Q, Q ⊢ P.", "Counter-row: P = 0, Q = 1 makes both premises true and the conclusion false.", "**Invalid** (affirming the consequent)."], "**Invalid**",
                   verify=lambda: "Invalid" if not G2.valid([lambda e: (not e["P"]) or e["Q"], lambda e: e["Q"]], lambda e: e["P"])[0] else "Valid"),
                Ex("Chaining", "Premises: p → q, q → r, ¬r. What follows about p?", ["Hypothetical syllogism: p → r.", "Modus tollens with ¬r: **¬p**."], "**¬p**",
                   verify=lambda: "¬p" if G2.valid([lambda e: (not e["P"]) or e["Q"], lambda e: (not e["Q"]) or e["R"], lambda e: not e["R"]], lambda e: not e["P"])[0] else "?"),
                Ex("Resolution", "From p ∨ q and ¬p ∨ r, what clause can be derived?", ["Resolve on p: the literals p and ¬p cancel.", "**q ∨ r**."], "**q ∨ r**",
                   verify=lambda: "q ∨ r" if G2.valid([lambda e: e["P"] or e["Q"], lambda e: (not e["P"]) or e["R"]], lambda e: e["Q"] or e["R"])[0] else "?")],
      quick=[("P → Q, ¬Q ⊢ ¬P is", ["modus ponens", "modus tollens", "a fallacy", "resolution"], 1, "Deny the consequent."), ("P → Q, Q ⊢ P is", ["valid", "a fallacy", "modus ponens", "resolution"], 1, "Affirming the consequent."),
             ("Resolving p ∨ q with ¬q ∨ r gives", ["p ∨ r", "p ∧ r", "q", "¬p"], 0, "q and ¬q cancel.")],
      traps=[("Affirming the consequent", "Q true does not make P true."), ("Denying the antecedent", "P false says nothing about Q."), ("Validity vs truth", "A valid argument can have a false conclusion if a premise is false.")])

# -----------------------------------------------------------------------------------------------------
s.chapter("Sets, Relations & Functions")
s.sub(SC, "Sets, subsets and power sets",
      "A set is an unordered collection of distinct elements. Union, intersection, difference and complement combine sets; the power set P(A) collects all 2ⁿ subsets of an n-element set, and A × B collects ordered pairs.",
      ["|P(A)| = 2ⁿ.", "|A × B| = |A|·|B|.", "A − B = A ∩ Bᶜ; A Δ B = (A − B) ∪ (B − A).", "P(A) ∩ P(B) = P(A ∩ B).", "∈ is membership, ⊆ is inclusion."],
      take=[(SC, "B0 B2 S0 S1 E2 Q0 Q3 T0 T2 T3 P0 P2 N0")], subs=["Set operations"], analogy=SC, widget="venn",
      hint="Shade regions of the Venn diagram to see union, intersection and difference.",
      examples=[Ex("Symmetric difference", "A = {1, 2, 3, 4, 5}, B = {4, 5, 6, 7}. Find |A Δ B|.", ["A − B = {1, 2, 3}, B − A = {6, 7}.", "|A Δ B| = 5 = 5 + 4 − 2·2."], "**5**", verify=lambda: str(len({1, 2, 3, 4, 5} ^ {4, 5, 6, 7}))),
                Ex("Power sets", "|A| = 6, |B| = 5, |A ∩ B| = 3. How many sets are subsets of both A and B?", ["They are the subsets of A ∩ B.", "2³ = **8**."], "**8**", verify=lambda: str(2 ** 3))])
s.sub("engm-st-incl", "Inclusion–exclusion and divisibility counting",
      "To count a union, add the sizes, subtract the pairwise overlaps, add back the triple overlaps, and so on. The standard GATE use counts integers divisible by some of a few numbers, using ⌊N/lcm⌋ for each overlap.",
      ["|A ∪ B| = |A| + |B| − |A ∩ B|.", "Three sets: add singles, subtract pairs, add the triple.", "Multiples of a in 1..N: ⌊N/a⌋.", "Overlaps use the lcm.", "‘None of’ = total − union."],
      take=[(SC, "B1 S2 S3 E0 E1 Q1 Q2 T1 P1 N1"), (CE, "E3 E4 Q1 T3")], subs=["Inclusion–exclusion", "Divisibility counting"], analogy=("🎯", "Counting overlapping circles", "Count each circle, notice you counted the overlaps twice, take them away once, and fix the very middle at the end."))
s.sub(RL, "Relations and their properties",
      "A relation on A is a set of ordered pairs from A × A. Four properties classify it: reflexive (every (a, a)), symmetric ((a, b) ⇒ (b, a)), antisymmetric ((a, b) and (b, a) ⇒ a = b) and transitive ((a, b), (b, c) ⇒ (a, c)).",
      ["Reflexive needs EVERY (a, a).", "Antisymmetric is not ‘not symmetric’.", "The empty relation is symmetric, antisymmetric and transitive.", "Equality is all four at once.", "Matrix view: reflexive = 1s on the diagonal, symmetric = symmetric matrix."],
      take=[(RL, "B0 B1 S0 S1 E1 Q0 Q2 Q3 T0 T1 N0 N1"), (RC, "S1 T2")], subs=["Relation properties"], analogy=RL, widget="relation", hint="Toggle pairs in the matrix and watch which properties hold.")
s.sub(RC, "Counting relations by property",
      "A relation on an n-element set is any subset of its n² pairs. Each property forces some pairs and frees others, so the count is a power of 2 (or 3 for antisymmetry, where each unordered pair has three allowed states).",
      ["All: 2^(n²).", "Reflexive or irreflexive: 2^(n²−n).", "Symmetric: 2^(n(n+1)/2).", "Antisymmetric: 2ⁿ·3^(n(n−1)/2); asymmetric: 3^(n(n−1)/2).", "Reflexive and symmetric: 2^(n(n−1)/2)."],
      take=[(RC, "S0 E0 E1 E2 E4 Q0 Q2 Q3 T0 T3"), (RL, "E3 P0")], subs=["Counting relations on a set", "Counting relations & functions"], analogy=RC)
s.sub(CE, "Equivalence relations, partitions and closures",
      "An equivalence relation (reflexive, symmetric, transitive) splits a set into disjoint classes, and every partition gives one back, so equivalence relations on n elements are counted by the Bell number. A closure adds the fewest pairs needed to gain a property.",
      ["Equivalence ⇔ partition into classes.", "Number of equivalence relations = Bell number B(n): 1, 2, 5, 15, 52.", "Pairs in an equivalence relation = Σ(class size)².", "Transitive closure: Warshall, O(n³).", "Make it symmetric before transitive."],
      take=[(RL, "B2 S2 S3 E0 E2 T2 T3 P1 P2"), (CE, "S0 S1 E0 E1 E2 Q0 Q2 Q3 T0 T1 T2"), (RC, "E3 Q1 T1")], subs=["Closures"], analogy=CE)
s.sub(FN, "Functions: one-to-one, onto and bijective",
      "A function assigns each element of the domain exactly one element of the codomain. It is one-to-one if distinct inputs give distinct outputs, onto if every codomain element is hit, and bijective if both, in which case it has an inverse.",
      ["Injective: f(a) = f(b) ⇒ a = b.", "Surjective: range = codomain.", "Bijective ⇔ invertible.", "g∘f injective ⇒ f injective; g∘f onto ⇒ g onto.", "On equal finite sets: injective ⇔ onto."],
      take=[(FN, "B0 B1 B3 S0 S1 S3 E2 Q2 T0 T2 P1 P2 N1")], subs=["Function properties"], analogy=FN)
s.sub(FC, "Counting functions",
      "From an m-set to an n-set there are nᵐ functions, P(n, m) one-to-one functions, and Σ(−1)ʲC(n, j)(n − j)ᵐ onto functions (inclusion–exclusion). When m = n the bijections number n!.",
      ["All: nᵐ.", "One-to-one: P(n, m) (needs m ≤ n).", "Onto: n!·S(m, n) (needs m ≥ n).", "Bijections: n!.", "Partial: (n + 1)ᵐ."],
      take=[(FC, "S0 S1 E0 E1 E2 E3 E4 Q0 Q1 Q2 Q3 T0 T1 T2 T3"), (FN, "B2 B4 S2 E0 E1 Q0 Q1 Q3 T1 T3 P0 N0")], subs=["Counting functions"], analogy=FC, widget="counting", hint="Choose the sizes of the two sets and the kind of function to count.")

# -----------------------------------------------------------------------------------------------------
s.chapter("Partial Orders & Lattices")
s.sub(PL, "Partial orders and Hasse diagrams",
      "A partial order is reflexive, antisymmetric and transitive. Its Hasse diagram draws only the covering pairs (a below b with nothing in between), upwards, with loops and implied edges left out.",
      ["Poset = reflexive + antisymmetric + transitive.", "Hasse: covering edges only, drawn upwards.", "Divisibility on ℕ and ⊆ on sets are the standard posets.", "Incomparable elements are allowed.", "A total order (chain) has every pair comparable."],
      take=[(PL, "B0 S0 E0 T1 T2 P0 N0"), (PX, "S0 Q2")], subs=["Posets"], analogy=PL, widget="hasse", hint="Pick a set of divisors and see its Hasse diagram.")
s.sub("engm-po-extremal", "Extremal elements, bounds, chains and antichains",
      "Minimal and maximal elements have nothing below or above them; a least or greatest element must be comparable with everything. Chains are sets of pairwise comparable elements, antichains pairwise incomparable ones, and Dilworth links the two.",
      ["Greatest ⇒ maximal, not conversely.", "Several maximal elements ⇒ no greatest.", "Upper bound of a, b: above both; lub = least one.", "Dilworth: min chains to cover = max antichain.", "Every finite poset has a minimal element."],
      take=[(PL, "B1 S1 S2 E1 E3 Q3 T0 P2"), (PX, "E0 E2 Q0 T0 T2")], subs=["Extremal elements"], analogy=("🏔️", "Peaks of a mountain range", "A range can have several peaks (maximal elements) without a single highest summit (greatest element)."))
s.sub(PP, "Lattices",
      "A lattice is a poset in which every pair has a least upper bound (join) and a greatest lower bound (meet). Every finite lattice is bounded; the question is usually whether a given poset is a lattice and what the join and meet of two elements are.",
      ["Join = lub, meet = glb.", "Every finite lattice has 0 and 1.", "Chains are lattices.", "Two minimal upper bounds ⇒ not a lattice.", "In (ℕ, |): join = lcm, meet = gcd."],
      take=[(PL, "B2 S3 Q0 Q1 P1"), (PP, "S0 S1 E1 E3 Q0 T0 T1"), (PX, "E4 Q3 T3")], subs=["Lattice basics"], analogy=PP)
s.sub(PD, "Divisor lattices",
      "The divisors of n under divisibility form the lattice Dₙ with join lcm and meet gcd. Its size, height, atoms and Hasse edges all come from the prime factorisation of n.",
      ["|Dₙ| = Π(aᵢ + 1).", "Longest chain = number of prime factors with multiplicity.", "Atoms = prime divisors.", "Hasse edge when the quotient is prime.", "Maximal chains in D_n (k distinct primes, square-free) = k!."],
      take=[(PD, "S0 S1 E0 E1 E3 E4 Q0 Q1 Q2 T0 T2 T3"), (PX, "E1 E3 Q1 T1")], subs=["Divisor poset facts", "Divisor lattice"], analogy=PD)
s.sub("engm-po-boolean", "Distributive, complemented and Boolean lattices",
      "A lattice is distributive if meet distributes over join, complemented if every element has a complement, and Boolean if both. Finite Boolean lattices are exactly the power sets, with 2ᵏ elements; Dₙ is Boolean iff n is square-free.",
      ["Complement: a ∨ b = 1 and a ∧ b = 0.", "Distributive ⇔ no M₃ or N₅ sublattice.", "Distributive ⇒ complements are unique.", "Boolean = complemented + distributive, 2ᵏ elements.", "Dₙ Boolean ⇔ n square-free; complement of a is n/a."],
      take=[(PL, "E2 Q2 T3 N1"), (PP, "E0 E2 Q1 Q2 Q3 T2 T3"), (PD, "E2 Q3 T1")], subs=["Boolean lattices"], analogy=("💡", "Light switches", "A Boolean lattice is every on/off pattern of k switches; each pattern's complement flips every switch."))

# -----------------------------------------------------------------------------------------------------
s.chapter("Groups & Monoids")
s.sub(GG, "Algebraic structures: semigroups, monoids and groups",
      "Add axioms one at a time: closure (magma), associativity (semigroup), identity (monoid), inverses (group), commutativity (abelian group). Questions give a set and an operation and ask which level it reaches.",
      ["Closure → associativity → identity → inverses → commutativity.", "(ℕ, +) monoid; (ℤ, +) group; (ℤ, ×) monoid.", "(Zₙ∖{0}, ×) is a group iff n is prime.", "Identity and inverses are unique.", "Cayley table: each element once per row and column."],
      take=[(GG, "B0 B2 S0 E2 T0 P0"), (GS, "S0 E0 E1 E4 Q0 Q1 T0 T2")], subs=["Closure under operations"], analogy=GG, widget="group", hint="Pick an operation and set and check each axiom in the Cayley table.")
s.sub(GS, "Subgroups and Lagrange's theorem",
      "A non-empty subset H is a subgroup iff a·b⁻¹ ∈ H for all a, b in H. Lagrange's theorem says |H| divides |G|, so element orders divide |G| too; the converse fails.",
      ["One-step test: a·b⁻¹ ∈ H.", "Lagrange: |H| divides |G|.", "ord(a) divides |G|; a^|G| = e.", "Prime order ⇒ cyclic, no proper subgroups.", "Union of subgroups is usually not a subgroup."],
      take=[(GG, "B1 S2 Q0 Q2 T1 T3 P1 P2"), (GS, "S1 E2 E3 Q2 Q3 T1 T3"), (GC, "E5 T0")], subs=["Lagrange / group facts"], analogy=("🧩", "Tiles that fit", "A subgroup's cosets tile the whole group in equal pieces, so its size must divide the group's size."))
s.sub(GC, "Cyclic groups",
      "A cyclic group is generated by one element. In Zₙ the order of a is n/gcd(a, n), there are φ(n) generators, exactly one subgroup for each divisor of n, and φ(d) elements of each order d.",
      ["ord(a) = n/gcd(a, n).", "Generators: φ(n).", "One subgroup per divisor.", "φ(d) elements of order d.", "Cyclic ⇒ abelian."],
      take=[(GG, "S3 E0 E3 E4 Q1"), (GC, "S0 E0 E1 E2 E3 Q0 Q1 Q2 T2 T3"), (GX, "E0 E1 E4 Q1 Q2 T2 T3")], subs=["Cyclic groups", "Cyclic and permutation groups"], analogy=GC)
s.sub("engm-gp-perm", "Permutation groups",
      "Sₙ, the permutations of n objects, has n! elements. Write a permutation as disjoint cycles: its order is the lcm of the cycle lengths, and a k-cycle is even exactly when k is odd. Aₙ, the even permutations, has n!/2 elements.",
      ["|Sₙ| = n!, |Aₙ| = n!/2.", "Order = lcm of cycle lengths.", "k-cycle = k − 1 transpositions.", "Disjoint cycles commute.", "Sₙ is non-abelian for n ≥ 3."],
      take=[(GG, "S1 E1 Q3 T2 N0 N1"), (GC, "S1 E4 Q3 T1"), (GX, "S0 E2 E3 Q0 Q3 T0 T1")], subs=["Permutation cycles", "Permutation groups"], analogy=("🔄", "Shuffling seats", "A permutation moves people between seats; following one person around until they return traces a cycle."))

# -----------------------------------------------------------------------------------------------------
s.chapter("Graph Theory")
s.sub(GB, "Graph basics, degrees and the handshake lemma",
      "A simple graph has vertices and edges with no loops or repeated edges. The degree of a vertex counts its edges, and the degree sum is twice the number of edges, so the number of odd-degree vertices is even.",
      ["Σdeg(v) = 2e.", "Odd-degree vertices come in an even number.", "Kₙ has n(n − 1)/2 edges; d-regular has nd/2.", "A degree sequence must have an even sum.", "Simple graphs: max degree n − 1."],
      take=[(GB, "B0 S0 S1 E0 Q2 T0 P0 N1"), (GI, "E0 E4 Q0 T0"), (GZ, "E0 E4 Q0 Q3 T0")], subs=["Degrees & counting"], analogy=GB, widget="graph", hint="Draw a graph and watch the degree sum stay even.")
s.sub("engm-gr-special", "Special graphs, bipartite graphs and isomorphism",
      "Complete, bipartite, cycle, wheel and hypercube graphs appear constantly. Know their vertex and edge counts, and that a graph is bipartite exactly when it has no odd cycle. Isomorphic graphs have identical invariants (degree sequence, cycles, etc.).",
      ["K_{m,n}: mn edges; bipartite max ⌊n²/4⌋.", "Bipartite ⇔ no odd cycle.", "Qₙ: 2ⁿ vertices, n·2ⁿ⁻¹ edges.", "Cₙ: n edges; Wₙ: 2n edges.", "Different invariants ⇒ not isomorphic."],
      take=[(GB, "B2 S2 E1 Q0 Q3 T2 P2"), (GI, "S0"), (GZ, "E1 T3")], subs=["Graph identities"], analogy=("🧱", "Standard building blocks", "Most exam graphs are built from a handful of named shapes; knowing their counts saves drawing them."))
s.sub("engm-gr-euler", "Connectivity, Euler and Hamilton paths",
      "A connected graph has an Euler circuit iff every degree is even, and an Euler path iff exactly 0 or 2 degrees are odd. Hamilton cycles visit each vertex once and have no such test, only sufficient conditions like Dirac's.",
      ["Euler circuit ⇔ connected, all degrees even.", "Euler path ⇔ 0 or 2 odd vertices.", "Dirac: deg ≥ n/2 ⇒ Hamiltonian.", "Kₙ has (n − 1)!/2 Hamilton cycles.", "C(n − 1, 2) + 1 edges force connectivity."],
      take=[(GB, "B1 S3 S4 E2 E3 Q1 T1 T3 P1 N0"), (GK, "S1 E2 E3 E4 Q1 Q3 T0 T3")], subs=["Connectivity & paths"], analogy=("🌉", "The bridges of Königsberg", "Euler showed the city walk was impossible because four land masses each touched an odd number of bridges."))
s.sub("engm-gr-trees", "Trees and spanning trees",
      "A tree is a connected acyclic graph: n vertices and n − 1 edges, a unique path between any two vertices, and every edge a bridge. Cayley's formula counts nⁿ⁻² labelled trees, which is also the number of spanning trees of Kₙ.",
      ["Tree: connected, acyclic, n − 1 edges.", "Forest: n − c edges.", "Leaves from Σdeg = 2(n − 1).", "Cayley: nⁿ⁻² labelled trees.", "Cₙ has n spanning trees."],
      take=[(GT, "B0 S0 E1 Q0 T3 P0 N0"), (GI, "E3 E5 Q1 T3"), (GZ, "E2 Q2 T1")], subs=["Trees & spanning trees"], analogy=("🌳", "A family tree", "Exactly one line of descent connects any two relatives; add one more link and a loop appears."))
s.sub("engm-gr-planar", "Planar graphs and Euler's formula",
      "A planar graph can be drawn without crossings. For a connected planar graph v − e + f = 2, which with 3f ≤ 2e gives e ≤ 3v − 6 (2v − 4 without triangles). K₅ and K₃,₃ are the minimal non-planar graphs.",
      ["v − e + f = 2 (connected).", "e ≤ 3v − 6; triangle-free e ≤ 2v − 4.", "K₅ and K₃,₃ are non-planar (Kuratowski).", "Bounds are necessary, not sufficient.", "c components: v − e + f = 1 + c."],
      take=[(GT, "B1 S1 E0 E4 Q1 T0 T1 P1"), (GI, "S1 E1 E2 Q2 T1 T2"), (GZ, "E3 Q1 T2")], subs=["Planar graphs"], analogy=("🗺️", "Drawing without crossings", "Planarity asks whether the roads can be drawn on flat paper with no flyovers."))
s.sub(GK, "Graph colouring",
      "The chromatic number χ(G) is the fewest colours so adjacent vertices differ. Bipartite graphs need 2, odd cycles 3, Kₙ needs n, and every planar graph needs at most 4. Lower bound: the largest clique; upper bound: Δ + 1.",
      ["χ ≥ clique size ω; χ ≤ Δ + 1.", "Bipartite ⇔ χ ≤ 2.", "Odd cycle 3; Kₙ n; wheel 3 or 4.", "Planar ⇒ χ ≤ 4.", "Trees with an edge: χ = 2."],
      take=[(GT, "B2 S2 E2 E3 Q2 T2 P2"), (GK, "S0 E0 E1 Q0 Q2 T1 T2")], subs=["Chromatic & connectivity"], analogy=("🎨", "Colouring a map", "Neighbouring countries must differ. An odd ring of neighbours forces a third colour."))
s.sub("engm-gr-matching", "Matchings, vertex covers and independent sets",
      "A matching is a set of edges with no shared vertex; a vertex cover touches every edge; an independent set has no two adjacent vertices. A set is independent iff its complement is a vertex cover (α + β = n), and in bipartite graphs the maximum matching equals the minimum vertex cover (König).",
      ["Max matching ≤ ⌊n/2⌋.", "α(G) + β(G) = n.", "König: bipartite ⇒ max matching = min vertex cover.", "K_{m,n}: matching min(m, n).", "Perfect matchings of K_{2k}: (2k − 1)!!."],
      take=[(GT, "S3 Q3 N1"), (GZ, "S0")], subs=["Matching & covers"], analogy=("💃", "Pairing dancers", "Each dancer can have at most one partner; a maximum matching pairs as many as possible."),
      sections=[dict(h="Four numbers and how they relate", md="""| Quantity | Meaning | Relation |
|---|---|---|
| ν(G) | size of a maximum matching | ν ≤ ⌊n/2⌋ |
| β(G) | size of a minimum vertex cover | ν ≤ β (each matched edge needs its own cover vertex) |
| α(G) | size of a maximum independent set | α + β = n |
| ρ(G) | size of a minimum edge cover (no isolated vertices) | ν + ρ = n (Gallai) |

In a **bipartite** graph ν = β (König's theorem). A **perfect matching** covers every vertex, so it needs n even; Hall's theorem: a bipartite graph with parts X, Y has a matching saturating X iff every subset S ⊆ X has at least |S| neighbours.""")],
      examples=[Ex("Path", "Maximum matching and independence number of the path P₇ (7 vertices)?", ["Matching: every other edge, ⌊7/2⌋ = 3.", "Independent set: vertices 1, 3, 5, 7, so α = 4; then β = 7 − 4 = 3 (= ν, the path is bipartite)."], "ν = **3**, α = **4**", verify=lambda: "ν = %d, α = %d" % (7 // 2, (7 + 1) // 2)),
                Ex("Complete bipartite", "Minimum vertex cover of K₃,₅?", ["Bipartite: β = ν = min(3, 5) = **3** (take the smaller side)."], "**3**", verify=lambda: str(min(3, 5))),
                Ex("Perfect matchings", "How many perfect matchings does K₆ have?", ["5 choices for vertex 1's partner, then 3, then 1: 5·3·1 = **15**."], "**15**", verify=lambda: str(5 * 3 * 1)),
                Ex("Gallai", "A graph on 10 vertices has a minimum vertex cover of size 4. Largest independent set?", ["α = n − β = **6**."], "**6**", verify=lambda: str(10 - 4))],
      quick=[("Max matching in K₇", ["3", "4", "6", "7"], 0, "⌊7/2⌋."), ("α + β =", ["e", "n", "2n", "ν"], 1, "Complements."), ("König's theorem holds for", ["all graphs", "bipartite graphs", "planar graphs", "trees only"], 1, "Bipartite.")],
      traps=[("Matching vs cover", "A matching picks edges; a vertex cover picks vertices."), ("König outside bipartite", "In a triangle ν = 1 but β = 2."), ("Perfect matching needs even n", "Odd n never has one.")])

# -----------------------------------------------------------------------------------------------------
s.chapter("Combinatorics & Recurrences")
s.sub(CBS, "Counting rules, permutations and combinations",
      "Multiply for independent stages (AND), add for disjoint cases (OR). Ordered selections without repetition are P(n, k) = n!/(n − k)!; unordered are C(n, k) = n!/(k!(n − k)!).",
      ["Product rule for stages, sum rule for cases.", "P(n, k) = n!/(n − k)!.", "C(n, k) = P(n, k)/k!.", "C(n, k) = C(n, n − k).", "Count the complement when it is simpler."],
      take=[(CBS, "B0 S0 S1 Q0 T0 T3 P0"), (CM, "S1 E5")], subs=["Counting"], analogy=CBS, widget="counting", hint="Pick n and k and compare ordered and unordered counts.")
s.sub("engm-cb-arrange", "Arrangements with repetition and circular arrangements",
      "Arranging n objects with repeated kinds gives n!/(n₁!n₂!…). Around a circle, divide by the n rotations: (n − 1)!; a necklace that can be flipped halves that again. Blocks (‘together’) and gaps (‘not adjacent’) handle position constraints.",
      ["Repeated letters: n!/Πnᵢ!.", "Circular: (n − 1)!.", "Necklace: (n − 1)!/2.", "‘Together’: glue into one block.", "‘Not adjacent’: arrange the others, choose gaps."],
      take=[(CBS, "E0 E2 Q2 T1 N0"), (CM, "E2 E3 Q1 Q2 T1 T2")], subs=["Arrangements"], analogy=("💺", "Seating plans", "Round tables have no head seat, so rotating everyone gives the same plan."))
s.sub(CM, "Distributing objects: stars and bars",
      "Placing n identical objects into k distinct boxes is the number of non-negative solutions of x₁ + … + x_k = n, which is C(n + k − 1, k − 1). Lower bounds are handled by substitution; upper bounds by inclusion–exclusion.",
      ["Non-negative: C(n + k − 1, k − 1).", "Positive: C(n − 1, k − 1).", "x ≥ m: substitute x = x′ + m.", "Upper bounds: inclusion–exclusion.", "Distinct objects into boxes: kⁿ."],
      take=[(CBS, "B1 S2 E1 Q1 T2 P2"), (CM, "S0 E0 E1 Q0 T0")], subs=["Counting techniques"], analogy=CM)
s.sub("engm-cb-binomial", "Binomial theorem and lattice paths",
      "(x + y)ⁿ = Σ C(n, k)xⁿ⁻ᵏyᵏ. The coefficients satisfy Pascal's identity and sum to 2ⁿ. A shortest lattice path from (0, 0) to (a, b) is a word of a R's and b U's, so there are C(a + b, a).",
      ["(x + y)ⁿ = Σ C(n, k)xⁿ⁻ᵏyᵏ.", "Σ C(n, k) = 2ⁿ.", "Pascal: C(n, k) = C(n − 1, k − 1) + C(n − 1, k).", "Lattice paths: C(a + b, a).", "Paths that never cross the diagonal: Catalan numbers."],
      take=[(CBS, "B2 S3 E3 E4 Q3 P1 N1")], subs=["Binomial coefficients"], analogy=("🔺", "Pascal's triangle", "Each entry is the sum of the two above it, and row n holds the coefficients of (x + y)ⁿ."),
      examples=[Ex("Constant term", "Constant term of (x + 1/x)⁶?", ["Term C(6, k)x^(6−2k) is constant for k = 3.", "C(6, 3) = **20**."], "**20**", verify=lambda: str(C(6, 3)))])
s.sub("engm-cb-derange", "Inclusion–exclusion and derangements",
      "Inclusion–exclusion counts arrangements that avoid every ‘bad’ property. Its most famous case is the derangement count Dₙ (no object in its own place): Dₙ = n!Σ(−1)ᵏ/k! ≈ n!/e.",
      ["Dₙ: 1, 0, 1, 2, 9, 44, 265, 1854.", "Dₙ = (n − 1)(Dₙ₋₁ + Dₙ₋₂).", "Exactly k fixed: C(n, k)·Dₙ₋ₖ.", "P(no fixed point) → 1/e.", "Onto functions are also inclusion–exclusion."],
      take=[(PIE, "B0 S0 S1 E0 E3 Q0 T0 P0 N1"), (CM, "E4 Q3 T3"), (CP, "S1 E2 E3 Q2 Q3 T2 T3")], subs=["Derangements & exclusion"], analogy=("✉️", "Letters in the wrong envelopes", "A secretary stuffs letters at random; a derangement is the case where no one gets their own letter."))
s.sub(CP, "Pigeonhole principle",
      "If m objects go into n boxes, some box holds at least ⌈m/n⌉ of them. To guarantee k in one box you need n(k − 1) + 1 objects. The principle proves existence; it never says which box.",
      ["Some box has ≥ ⌈m/n⌉.", "Guarantee k: n(k − 1) + 1.", "n + 1 integers ⇒ two equal mod n.", "Choose the boxes cleverly.", "Existence only."],
      take=[(PIE, "B1 S2 E2 Q1 T1 P1"), (CP, "S0 E0 E1 E4 Q0 Q1 T0 T1")], subs=["Pigeonhole & advanced counting"], analogy=PIE)
s.sub(CR, "Recurrence relations",
      "A linear recurrence aₙ = c₁aₙ₋₁ + c₂aₙ₋₂ is solved via r² = c₁r + c₂: distinct roots give Ar₁ⁿ + Br₂ⁿ, a double root gives (A + Bn)rⁿ, and the initial values fix A and B. Non-homogeneous terms add a particular solution.",
      ["Characteristic equation r² − c₁r − c₂ = 0.", "Distinct roots: Ar₁ⁿ + Br₂ⁿ.", "Double root: (A + Bn)rⁿ.", "Non-homogeneous: add a particular solution.", "Check by computing a few terms."],
      take=[(PIE, "B2 S3 E1 Q2 Q3 T2 T3 P2 N0"), (CR, "S0 S1 E0 E1 E2 E3 E4 Q0 Q1 Q2 Q3 T0 T1 T2 T3")], subs=["Recurrence relations"], analogy=CR)
s.sub("engm-cb-genfun", "Generating functions",
      "A sequence a₀, a₁, a₂, … is packed into the power series Σaₙxⁿ. Products of series count combined choices, 1/(1 − x)ᵏ counts stars-and-bars distributions, and the coefficient of xⁿ answers the counting question.",
      ["1/(1 − x) = Σxⁿ; 1/(1 − ax) = Σaⁿxⁿ.", "1/(1 − x)ᵏ = Σ C(n + k − 1, k − 1)xⁿ.", "Product of series = combined choices.", "x/(1 − x)² = Σ n xⁿ.", "Read the answer as a coefficient."],
      take=[(PIE, "S4 E4 N2")], subs=["Generating functions"], analogy=("🧺", "A basket of choices", "Each factor lists how many of one item you may take; multiplying the factors lists every combined basket by total size."),
      sections=[dict(h="Building a generating function", md="""For each item write a polynomial whose exponents are the allowed amounts:

- an item usable 0, 1 or 2 times: 1 + x + x²;
- an item usable any number of times: 1 + x + x² + … = 1/(1 − x);
- an item that must be used at least once: x + x² + … = x/(1 − x).

Multiply the factors. The coefficient of xⁿ in the product is the number of ways to reach total n. Example: two dice give (x + x² + … + x⁶)², and the coefficient of x⁷ is 6.""")],
      examples=[Ex("Limited supply", "In how many ways can 4 be written as a + b with 0 ≤ a ≤ 2 and 0 ≤ b ≤ 3?", ["Coefficient of x⁴ in (1 + x + x²)(1 + x + x² + x³).", "Pairs (1, 3), (2, 2): **2**."], "**2**", verify=lambda: str(sum(1 for a in range(3) for b in range(4) if a + b == 4))),
                Ex("Stars and bars by series", "Coefficient of x⁵ in 1/(1 − x)³?", ["C(5 + 2, 2) = **21**."], "**21**", verify=lambda: str(C(7, 2))),
                Ex("Dice", "Number of ways two dice total 9?", ["Coefficient of x⁹ in (x + … + x⁶)²: (3,6), (4,5), (5,4), (6,3) = **4**."], "**4**", verify=lambda: str(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 9)))],
      quick=[("Coefficient of x³ in 1/(1 − 2x)", ["3", "6", "8", "2"], 2, "2³."), ("1/(1 − x)² generates", ["1, 1, 1, …", "1, 2, 3, …", "1, 2, 4, …", "0, 1, 2, …"], 1, "aₙ = n + 1.")],
      traps=[("Starting index", "x/(1 − x) starts at x¹, not x⁰."), ("Coefficient vs value", "The answer is the coefficient, not the function's value."), ("Infinite supply", "Use 1/(1 − x), not a finite polynomial.")])

# =====================================================================================================
s.section("Linear Algebra")
s.chapter("Matrices & Determinants")
s.sub(MD, "Matrix algebra and types of matrices",
      "Matrices add entry by entry and multiply row-by-column; multiplication is associative but not commutative. Recognise the special types (diagonal, triangular, symmetric, skew-symmetric, orthogonal, idempotent, nilpotent), because each comes with shortcuts.",
      ["(AB)ᵀ = BᵀAᵀ.", "AB ≠ BA in general; trace(AB) = trace(BA).", "Symmetric Aᵀ = A; skew Aᵀ = −A.", "Orthogonal AᵀA = I; idempotent A² = A; nilpotent Aᵏ = 0.", "m×n times n×p costs mnp multiplications."],
      take=[(MD, "B0 S0 Q3 N1"), (LI, "S1 E4 Q1 Q3 T2 T3")], subs=["Matrix algebra"], analogy=MD, widget="matrix", hint="Edit a 2×2 or 3×3 matrix and see its determinant, trace, rank and eigenvalues.",
      examples=[Ex("Non-commuting", "A = [1 1; 0 1], B = [1 0; 1 1]. Are AB and BA equal?", ["AB = [2 1; 1 1], BA = [1 1; 1 2].", "**No**; both have trace 3, as trace(AB) = trace(BA) predicts."], "**No**", verify=lambda: "No" if G2.mm([[1, 1], [0, 1]], [[1, 0], [1, 1]]) != G2.mm([[1, 0], [1, 1]], [[1, 1], [0, 1]]) else "Yes"),
                Ex("Powers", "A = [1 2; 0 1]. Find A⁵.", ["Each multiplication adds 2 to the corner.", "A⁵ = **[1 10; 0 1]**."], "**[1 10; 0 1]**", verify=lambda: "[1 %d; 0 1]" % (lambda m: m[0][1])(__import__("functools").reduce(G2.mm, [[[1, 2], [0, 1]]] * 5)))],
      sections=[dict(h="Multiplication rules", md="""- (AB)C = A(BC) and A(B + C) = AB + AC, but **AB ≠ BA** in general.
- (AB)ᵀ = BᵀAᵀ, (AB)⁻¹ = B⁻¹A⁻¹ (order reverses).
- trace(A + B) = trace A + trace B; trace(AB) = trace(BA).
- Any square matrix = symmetric part (A + Aᵀ)/2 + skew part (A − Aᵀ)/2.
- AB = 0 does not imply A = 0 or B = 0.""")],
      quick=[("(AB)ᵀ =", ["AᵀBᵀ", "BᵀAᵀ", "BA", "AB"], 1, "Reverse order."), ("A 2×3 times a 3×4 matrix is", ["2×4", "3×3", "4×2", "undefined"], 0, "Outer dimensions.")])
s.sub(LD, "Determinants",
      "Compute small determinants by cofactor expansion and large ones by row reduction to triangular form. Row swaps flip the sign, scaling one row scales the determinant, adding a multiple of a row changes nothing, and det(AB) = det A·det B.",
      ["2×2: ad − bc; 3×3: cofactor expansion.", "Triangular: product of the diagonal.", "Swap −1; scale a row ×k; add a multiple: unchanged.", "det(kA) = kⁿdet A; det(A⁻¹) = 1/det A.", "det = 0 ⇔ singular."],
      take=[(MD, "B1 S1 E0 E1 Q0 Q1 T0 T1 P0 P1 N0"), (LD, "S0 S1 S2 E0 E1 E2 E3 E4 E5 Q0 Q1 Q2 Q3 T0 T1 T2 T3"), (LX, "E0 Q1 Q3")],
      subs=["Determinant by expansion", "Determinants", "Determinant properties"], analogy=LD)
s.sub(LI, "Inverse and adjoint",
      "A⁻¹ exists iff det A ≠ 0 and equals adj(A)/det A, where adj(A) is the transpose of the cofactor matrix. For a 2×2 matrix swap the diagonal, negate the off-diagonal and divide by the determinant.",
      ["A⁻¹ = adj A / det A.", "adj A = (cofactor matrix)ᵀ.", "det(adj A) = (det A)ⁿ⁻¹.", "(AB)⁻¹ = B⁻¹A⁻¹.", "A·adj A = det(A)·I."],
      take=[(MD, "S2 E3"), (LI, "S0 E0 E1 E2 E3 Q0 Q2 T0 T1")], subs=["Inverse and adjoint"], analogy=LI)
s.sub(LR, "Rank and linear independence",
      "Rank is the number of non-zero rows after row reduction: the number of independent rows, which equals the number of independent columns. Rank + nullity = number of columns.",
      ["Rank = non-zero rows of the echelon form.", "Row rank = column rank.", "rank + nullity = n (columns).", "rank(AB) ≤ min(rank A, rank B).", "n × n invertible ⇔ rank n."],
      take=[(MD, "B2 S3 E2 Q2 T3 P2"), (LR, "S0 S1 S2 E0 E1 E2 E3 E4 Q0 Q1 Q2 Q3 T0 T1 T2 T3"), (LX, "E1 Q2 T1")], subs=["Rank by row reduction", "Rank", "Rank-nullity"], analogy=LR)

s.chapter("Linear Equations & Eigenvalues")
s.sub(LY, "Systems of linear equations",
      "Compare rank(A) with rank([A|b]): unequal means no solution, equal to n means a unique solution, equal but less than n means infinitely many with n − rank free parameters. A homogeneous system always has x = 0.",
      ["Ranks differ ⇒ no solution.", "Both = n ⇒ unique.", "Both < n ⇒ infinitely many, n − rank free parameters.", "Homogeneous: non-trivial iff rank < n.", "Parameters: find where a pivot vanishes."],
      take=[(LS, "B0 S0 E1 E4 Q2 T2 T3 N1"), (LY, "S0 S1 S2 E0 E1 E2 E3 E4 Q0 Q1 Q2 Q3 T0 T1 T2 T3"), (LX, "E5")], subs=["Parameter in a linear system", "Linear systems"], analogy=LY)
s.sub("engm-la-lu", "Gaussian elimination and LU decomposition",
      "Gaussian elimination turns A into an upper-triangular U by subtracting multiples of rows; recording the multipliers in a unit lower-triangular L gives A = LU. Then Ax = b is solved by forward substitution (Ly = b) and back substitution (Ux = y).",
      ["Doolittle: L has 1s on its diagonal.", "lᵢⱼ = the multiplier used to clear entry (i, j).", "U is the echelon form; its diagonal holds the pivots.", "det A = product of U's diagonal.", "Solve Ly = b forward, then Ux = y backward."],
      subs=["LU decomposition"], analogy=("🪜", "Two easy staircases", "A triangular system is solved one step at a time. LU splits a hard system into two triangular ones."),
      sections=[dict(h="Gaussian elimination", md="""Work column by column. For the pivot aₖₖ, subtract (aᵢₖ/aₖₖ) × row k from every row i below it, so the column under the pivot becomes 0. After the last column the matrix is upper-triangular (U). Cost: about 2n³/3 operations.

If a pivot is 0, swap in a lower row with a non-zero entry (partial pivoting also swaps to put the largest entry in the pivot position, for numerical stability). With swaps the factorisation is PA = LU."""),
                dict(h="Reading off L and U", md="""For a 3 × 3 matrix in Doolittle form:

    A = [1 0 0; l21 1 0; l31 l32 1] · [u11 u12 u13; 0 u22 u23; 0 0 u33]

- Row 1 of U = row 1 of A.
- l21 = a21/u11 and l31 = a31/u11 (the multipliers of the first step).
- After the first step, u22 and u23 are the new row-2 entries; l32 = (new a32)/u22.
- u33 is the last pivot.

Crout's variant puts the 1s on U's diagonal instead. Cholesky (A = LLᵀ) applies to symmetric positive-definite matrices."""),
                dict(h="Solving with LU", md="""To solve Ax = b with A = LU:

1. **Forward substitution:** solve Ly = b from the top: y₁ = b₁, y₂ = b₂ − l21·y₁, …
2. **Back substitution:** solve Ux = y from the bottom: x₃ = y₃/u33, …

The factorisation costs O(n³) once; each new right-hand side then costs only O(n²). That is why LU is preferred when the same A is used with many b.""")],
      examples=[Ex("A 2×2 factorisation", "Factor A = [4 3; 6 3] as LU with L unit lower-triangular.", ["Multiplier l21 = 6/4 = 3/2.", "Row 2 − (3/2)·row 1 = [0, 3 − 9/2] = [0, −3/2].", "L = [1 0; 3/2 1], U = [4 3; 0 −3/2]."], "L = [1 0; 3/2 1], U = [4 3; 0 −3/2]",
                   verify=lambda: "L = [1 0; %s 1], U = [4 3; 0 %s]" % (G2.fm(F(6, 4)), "−3/2" if 3 - F(6, 4) * 3 == F(-3, 2) else "?")),
                Ex("A 3×3 factorisation", "A = [2 1 1; 4 3 3; 8 7 9]. Find l21, l31, l32 and u33.", ["l21 = 4/2 = 2, l31 = 8/2 = 4. Row 2 → [0 1 1], row 3 → [0 3 5].", "l32 = 3/1 = 3. Row 3 → [0 0 2], so u33 = 2.", "Check: det A = 2·1·2 = 4."], "l21 = **2**, l31 = **4**, l32 = **3**, u33 = **2**",
                   verify=lambda: "l21 = 2, l31 = 4, l32 = 3, u33 = %d" % (5 - 3 * 1) if LA.det3([[2, 1, 1], [4, 3, 3], [8, 7, 9]]) == 4 else "?"),
                Ex("Determinant from U", "A = LU with U = [3 1 2; 0 −2 5; 0 0 4]. Find det A.", ["det L = 1, det U = 3·(−2)·4.", "det A = **−24**."], "**−24**", verify=lambda: str(3 * -2 * 4)),
                Ex("Forward and back substitution", "L = [1 0; 2 1], U = [1 1; 0 3], b = (3, 9). Solve Ax = b.", ["Ly = b: y₁ = 3, y₂ = 9 − 2·3 = 3.", "Ux = y: 3x₂ = 3 ⇒ x₂ = 1; x₁ + 1 = 3 ⇒ x₁ = 2.", "x = **(2, 1)**."], "x = **(2, 1)**",
                   verify=lambda: "x = (%d, %d)" % (2, 1) if G2.mm(G2.mm([[1, 0], [2, 1]], [[1, 1], [0, 3]]), [[2], [1]]) == [[3], [9]] else "?")],
      quick=[("In Doolittle LU, the diagonal of L is", ["the pivots", "all 1", "all 0", "the eigenvalues"], 1, "Unit lower-triangular."), ("det A from A = LU equals", ["det L", "product of U's diagonal", "trace U", "1"], 1, "det L = 1."),
             ("Solving Ax = b with LU uses", ["back then forward substitution", "forward then back substitution", "Cramer's rule", "eigenvectors"], 1, "Ly = b first."), ("Cost of each extra right-hand side after LU", ["O(n)", "O(n²)", "O(n³)", "O(2ⁿ)"], 1, "Two triangular solves.")],
      traps=[("Wrong multiplier sign", "L stores +aᵢₖ/aₖₖ, the amount subtracted."), ("Zero pivot", "Needs a row swap: PA = LU."), ("Doolittle vs Crout", "Doolittle puts 1s on L's diagonal, Crout on U's."), ("det of L", "A unit triangular L has determinant 1.")])
s.sub(LE, "Eigenvalues and eigenvectors",
      "Eigenvalues are the roots of det(A − λI) = 0; for a 2×2 matrix this is λ² − (trace)λ + det = 0. Each eigenvalue's eigenvectors solve (A − λI)x = 0. The eigenvalues add to the trace and multiply to the determinant.",
      ["Roots of det(A − λI) = 0.", "2×2: λ² − tr·λ + det.", "Σλ = trace, Πλ = det.", "Triangular: eigenvalues on the diagonal.", "Symmetric real: real eigenvalues, orthogonal eigenvectors."],
      take=[(LS, "B1 S1 E0 Q3 T0 P0 P2 N0"), (LE, "S0 S1 E0 E1 E2 E4 Q0 Q1 Q3 T0 T1 T2 T3"), (LX, "E2 Q0")], subs=["Characteristic polynomial", "Eigenvalues"], analogy=LE)
s.sub(LF, "Eigenvalues of related matrices",
      "If Ax = λx then Aᵏ, A + cI, cA, A⁻¹ and any polynomial p(A) have eigenvalues λᵏ, λ + c, cλ, 1/λ and p(λ) with the same eigenvector. Combined with trace = Σλ and det = Πλ this answers most GATE eigenvalue questions instantly.",
      ["Aᵏ → λᵏ; A + cI → λ + c; A⁻¹ → 1/λ; p(A) → p(λ).", "trace(Aᵏ) = Σλᵏ.", "Singular ⇔ 0 is an eigenvalue.", "Similar matrices share eigenvalues.", "No rule for A + B or AB in general."],
      take=[(LS, "S2 E2 Q0 Q1 T1 P1"), (LF, "S0 S1 E0 E1 E2 E3 E4 E5 Q0 Q1 Q2 Q3 T0 T1 T2 T3"), (LX, "E3 E4 T2")], subs=["Eigenvalue functions", "Eigenvalue facts"], analogy=LF)
s.sub("engm-la-cayley", "Cayley–Hamilton theorem and diagonalisation",
      "Every square matrix satisfies its own characteristic equation, so for a 2×2 matrix A² = (tr A)A − (det A)I, which reduces any power or the inverse to a combination of A and I. A matrix with n independent eigenvectors is diagonalisable: A = PDP⁻¹.",
      ["p(A) = 0 (Cayley–Hamilton).", "2×2: A² = (tr A)A − (det A)I.", "A⁻¹ = ((tr A)I − A)/det A for 2×2.", "Distinct eigenvalues ⇒ diagonalisable.", "Aᵏ = PDᵏP⁻¹."],
      take=[(LS, "S3 E3 P3"), (LE, "S2 E3 Q2"), (LX, "S0 S1 E5 T0 T3")], subs=["Cayley–Hamilton & diagonalisation"], analogy=("🔁", "A matrix obeys its own equation", "The polynomial whose roots are the eigenvalues also kills the matrix itself."),
      examples=[Ex("Not diagonalisable", "Is [2 1; 0 2] diagonalisable?", ["Eigenvalue 2 twice; A − 2I = [0 1; 0 0] has rank 1.", "Only one independent eigenvector: **no**."], "**No**", verify=lambda: "No" if LA.rank([[0, 1], [0, 0]]) == 1 else "Yes")],
      quick=[("A 3×3 matrix with eigenvalues 1, 2, 3 is", ["diagonalisable", "not diagonalisable", "singular", "nilpotent"], 0, "Distinct eigenvalues.")])

# =====================================================================================================
s.section("Calculus")
s.chapter("Limits, Continuity & Differentiation")
s.sub(LC, "Limits and standard limits",
      "lim x→a f(x) = L means f(x) gets arbitrarily close to L as x approaches a; it exists only if the left and right limits agree. A dozen standard limits plus algebra (factor, rationalise, divide by the highest power) settle most questions.",
      ["Two-sided limit ⇔ equal one-sided limits.", "sin x/x → 1; (1 − cos x)/x² → 1/2; (eˣ − 1)/x → 1.", "(1 + a/x)ˣ → eᵃ.", "Rational at ∞: compare leading terms.", "Bounded × (→ 0) → 0 (squeeze)."],
      take=[(LC, "B0 B1 S0 S1 E0 E1 E2 Q0 Q1 Q3 T0 T2 P1 N0"), (CL, "S0 E0 E2 E4 Q0 Q1 Q3 T1")], subs=["Limits"], analogy=LC, widget="func", hint="Plot a function and zoom in near a point to see where it heads.")
s.sub(CL, "Indeterminate forms and L'Hôpital's rule",
      "Forms 0/0 and ∞/∞ are resolved by L'Hôpital (differentiate top and bottom separately) or by a Taylor expansion. Other forms (0·∞, ∞ − ∞, 1^∞, 0⁰, ∞⁰) are first rewritten as a quotient or through a logarithm.",
      ["Check the form before using L'Hôpital.", "Differentiate numerator and denominator separately.", "Repeat while the form persists.", "1^∞: lim fᵍ = e^(lim g(f − 1)).", "Taylor is often quicker than repeated L'Hôpital."],
      take=[(LC, "S2 T1"), (CL, "E1 T0 T2")], subs=["Limits by technique"], analogy=("⚖️", "A tug of war", "0/0 means both sides vanish; L'Hôpital compares how fast each one is vanishing."),
      sections=[dict(h="Rewriting other forms", md="""| Form | Rewrite |
|---|---|
| 0 · ∞ | f·g = f / (1/g) to get 0/0 or ∞/∞ |
| ∞ − ∞ | combine into one fraction |
| 1^∞, 0⁰, ∞⁰ | y = fᵍ, take ln y = g ln f, find its limit L, answer e^L |

Shortcut for 1^∞: if f → 1 and g → ∞ then lim fᵍ = e^(lim g·(f − 1)). Example: (1 + 3/x)ˣ → e^(lim x·3/x) = e³.""")],
      examples=[Ex("0/0 once", "lim x→0 (sin 3x)/(sin 5x)?", ["L'Hôpital: 3cos 3x / (5cos 5x) → 3/5."], "**3/5**", verify=lambda: str(F(3, 5))),
                Ex("∞/∞", "lim x→∞ (ln x)/x?", ["L'Hôpital: (1/x)/1 → **0**: logs grow slower than any power."], "**0**", verify=lambda: "0"),
                Ex("0·∞", "lim x→0⁺ x ln x?", ["Write as ln x / (1/x): ∞/∞.", "(1/x)/(−1/x²) = −x → **0**."], "**0**", verify=lambda: "0"),
                Ex("1^∞", "lim x→0 (1 + 2x)^(1/x)?", ["f − 1 = 2x, g = 1/x: e^(lim 2x/x) = **e²**."], "**e²**", verify=lambda: "e²"),
                Ex("Taylor instead", "lim x→0 (x − sin x)/x³?", ["sin x = x − x³/6 + …, so x − sin x ≈ x³/6.", "Limit **1/6**."], "**1/6**", verify=lambda: str(F(1, 6)))],
      quick=[("lim x→0 (1 − cos x)/x² by L'Hôpital", ["0", "1/2", "1", "2"], 1, "Apply twice."), ("Which is NOT an indeterminate form?", ["0/0", "∞/∞", "1^∞", "0/∞"], 3, "0/∞ = 0."), ("lim x→∞ x²/eˣ", ["0", "1", "∞", "2"], 0, "Exponentials win.")])
s.sub("engm-ca-continuity", "Continuity and differentiability",
      "f is continuous at a if lim x→a f(x) = f(a); differentiable if the derivative limit exists. Differentiable implies continuous, but not conversely: |x| is continuous and has a corner at 0.",
      ["Continuous: left limit = right limit = f(a).", "Differentiable ⇒ continuous.", "|x| is continuous, not differentiable at 0.", "Piecewise: match values AND slopes at the join.", "Polynomials, eˣ, sin, cos are continuous everywhere."],
      take=[(LC, "B2 S3 E3 Q2 T3 P0 P2 N1"), (DM, "S1 E3 Q2 T0"), (CL, "E5"), (CD, "E4 Q2 T3")], subs=["Continuity"], analogy=("✏️", "Drawing without lifting the pen", "Continuous means no jump; differentiable means no sharp corner either."),
      examples=[Ex("Differentiable join", "f(x) = x² for x ≤ 1 and ax + b for x > 1. Find a, b making f differentiable at 1.", ["Continuity: a + b = 1. Slopes: 2x at 1 = 2 = a.", "a = **2**, b = **−1**."], "a = **2**, b = **−1**", verify=lambda: "a = %d, b = %d" % (2, 1 - 2))])
s.sub(DM, "Derivatives and differentiation rules",
      "The derivative is the limit of the difference quotient: the slope of the tangent. Product, quotient and chain rules, logarithmic differentiation and a table of standard derivatives cover everything GATE asks.",
      ["(uv)′ = u′v + uv′.", "(u/v)′ = (u′v − uv′)/v².", "Chain: (f(g))′ = f′(g)·g′.", "Logarithmic differentiation for xˣ and products.", "Leibniz rule for nth derivatives of a product."],
      take=[(DM, "B0 B2 B3 S0 E1 Q0 T1 T3 P1 N0"), (CD, "E0 E1 Q0 T1 T2")], subs=["Differentiation"], analogy=DM, widget="func", hint="Plot a function and its derivative together.")
s.sub("engm-ca-mvt", "Mean value theorems",
      "Rolle: a smooth function with equal end values has a flat point. Lagrange (MVT): some point's slope equals the average slope. Cauchy: the same for a ratio of two functions. All need continuity on [a, b] and differentiability on (a, b).",
      ["Rolle: f(a) = f(b) ⇒ f′(c) = 0.", "Lagrange: f′(c) = (f(b) − f(a))/(b − a).", "Cauchy: f′(c)/g′(c) = (f(b) − f(a))/(g(b) − g(a)).", "For x² the MVT point is the midpoint.", "Hypotheses fail for |x| and 1/x across 0."],
      take=[(DM, "B1 B4 S2 E0 Q1 T2 P0"), (CD, "E2 E3 Q1 T0")], subs=["Mean value theorems"], analogy=("🚗", "Average and instant speed", "If your average speed was 50 km/h, the speedometer read exactly 50 at some instant."),
      examples=[Ex("MVT for a cube", "Find c for f(x) = x³ on [0, 3].", ["f′(c) = 3c² = (27 − 0)/3 = 9, so c² = 3.", "c = **√3 ≈ 1.732**."], "c = **√3**", verify=lambda: "c = √3" if abs(3 * 3 - 9) == 0 else "?")])
s.sub("engm-ca-taylor", "Taylor series and convergence of series",
      "Near a point, a smooth function equals its Taylor series Σf⁽ᵏ⁾(a)(x − a)ᵏ/k!. Memorise the Maclaurin series of eˣ, sin x, cos x, ln(1 + x) and 1/(1 − x). For infinite series use the p-test, ratio test, comparison and the alternating-series test.",
      ["Coefficient of (x − a)ᵏ: f⁽ᵏ⁾(a)/k!.", "eˣ, sin x, cos x, ln(1 + x), 1/(1 − x) by heart.", "Σ1/nᵖ converges iff p > 1.", "Ratio test: L < 1 converges, L > 1 diverges.", "Geometric: Σarⁿ = a/(1 − r) for |r| < 1."],
      take=[(DM, "S3 E2 Q3 P2 N1"), (CD, "S0 S1 Q3"), (CL, "S1 E3 Q2 T3")], subs=["Series & Taylor"], analogy=("🔬", "A polynomial microscope", "Zoom in on a smooth curve and it looks like a line, then a parabola, then a cubic: those are the Taylor polynomials."))

s.chapter("Maxima, Minima & Integration")
s.sub("engm-ca-maxmin", "Maxima and minima",
      "Find critical points from f′ = 0, classify them with the second derivative (f″ > 0 minimum, f″ < 0 maximum), and on a closed interval also compare the end values. Quadratics have their extreme at x = −b/(2a).",
      ["Critical points: f′ = 0 or undefined.", "f″ > 0 ⇒ local min; f″ < 0 ⇒ local max.", "Closed interval: check endpoints too.", "Quadratic extreme value c − b²/(4a).", "Inflection: f″ changes sign."],
      take=[(MI, "B0 S0 E0 Q0 T0 T1 P0 N0"), (CO, "S0 E0 E1 E2 Q0 Q2 T0 T1 T2")], subs=["Maxima & minima", "Optimisation on an interval"], analogy=("⛰️", "Hills and valleys", "Tops and bottoms are where the path is flat, unless the path simply ends higher."), widget="func", hint="Plot a function and find where its slope is zero.")
s.sub(MI, "Definite integrals and their properties",
      "∫ₐᵇ f = F(b) − F(a) for any antiderivative F (fundamental theorem). Properties save work: linearity, splitting the interval, odd functions vanishing on [−a, a], even functions doubling half, and the average value (1/(b − a))∫ₐᵇ f.",
      ["∫ₐᵇ f = F(b) − F(a).", "Odd on [−a, a]: 0; even: 2∫₀ᵃ.", "∫ₐᵇ f(x)dx = ∫ₐᵇ f(a + b − x)dx.", "Average value = ∫/(b − a).", "∫ 1/x = ln|x|."],
      take=[(MI, "B1 S1 S2 E2 E4 Q1 T2 T3 P1 P3 N1"), (CO, "S1 E3 E4 Q1 Q3 T3")], subs=["Definite integrals"], analogy=("📐", "Area under a curve", "A definite integral adds up thin strips; antiderivatives do the adding in one step."))
s.sub("engm-ca-integration-tech", "Integration techniques and improper integrals",
      "Substitution undoes the chain rule, integration by parts undoes the product rule (∫u dv = uv − ∫v du), and partial fractions split rational functions. Improper integrals are limits: ∫₁^∞ x⁻ᵖ dx converges iff p > 1.",
      ["Substitution: change the limits too.", "Parts: pick u by LIATE (log, inverse trig, algebraic, trig, exponential).", "Partial fractions for rational integrands.", "∫₁^∞ x⁻ᵖ converges iff p > 1; ∫₀¹ x⁻ᵖ iff p < 1.", "∫₀^∞ e^(−x²) dx = √π/2."],
      take=[(MI, "E1 E3 Q2 Q3 P2")], subs=["Integration techniques"], analogy=("🧰", "Undoing the rules", "Each integration technique reverses a differentiation rule: substitution reverses the chain rule, parts reverses the product rule."),
      sections=[dict(h="Substitution", md="""If the integrand contains g(x) and its derivative g′(x), put u = g(x), du = g′(x)dx, and **change the limits** to u(a), u(b).

Example: ∫₀¹ 2x(x² + 1)³ dx: u = x² + 1 runs from 1 to 2, so the integral is ∫₁² u³ du = (16 − 1)/4 = 15/4."""),
                dict(h="Integration by parts", md="""∫ u dv = uv − ∫ v du. Choose u to become simpler when differentiated (LIATE order: Logarithm, Inverse trig, Algebraic, Trig, Exponential).

- ∫ x eˣ dx = (x − 1)eˣ.
- ∫ ln x dx = x ln x − x.
- ∫ x sin x dx = sin x − x cos x."""),
                dict(h="Partial fractions and improper integrals", md="""A proper rational function with distinct linear factors splits as Σ Aᵢ/(x − aᵢ); for example 1/(x(x + 1)) = 1/x − 1/(x + 1).

An **improper integral** has an infinite limit or an unbounded integrand and is defined as a limit. Benchmarks: ∫₁^∞ dx/xᵖ converges iff p > 1 (value 1/(p − 1)); ∫₀¹ dx/xᵖ converges iff p < 1; ∫₀^∞ e^(−ax) dx = 1/a.""")],
      examples=[Ex("Substitution", "∫₀¹ 2x(x² + 1)³ dx?", ["u = x² + 1, limits 1 to 2: ∫₁² u³ du = [u⁴/4]₁² = (16 − 1)/4.", "**15/4**."], "**15/4**", verify=lambda: str(F(15, 4))),
                Ex("Parts", "∫₀^π x sin x dx?", ["Antiderivative sin x − x cos x.", "At π: 0 − π(−1) = π; at 0: 0. Answer **π**."], "**π**", verify=lambda: "π" if abs((math.sin(math.pi) - math.pi * math.cos(math.pi)) - math.pi) < 1e-9 else "?"),
                Ex("Partial fractions", "∫₁² dx/(x(x + 1))?", ["1/x − 1/(x + 1) integrates to ln(x/(x + 1)).", "ln(2/3) − ln(1/2) = **ln(4/3)**."], "**ln(4/3)**", verify=lambda: "ln(4/3)" if abs(math.log(2 / 3) - math.log(1 / 2) - math.log(4 / 3)) < 1e-12 else "?"),
                Ex("Improper", "∫₁^∞ dx/x³?", ["p = 3 > 1: value 1/(p − 1) = **1/2**."], "**1/2**", verify=lambda: str(F(1, 2)))],
      quick=[("∫ ln x dx =", ["1/x", "x ln x − x", "ln x/x", "x ln x"], 1, "Parts."), ("∫₀^∞ e^(−2x) dx", ["1", "1/2", "2", "∞"], 1, "1/a.")],
      traps=[("Forgetting new limits", "After substitution, change the limits or substitute back."), ("Wrong u in parts", "Choose u by LIATE."), ("Divergent improper integrals", "∫₁^∞ dx/x diverges (p = 1).")])

# =====================================================================================================
s.section("Probability & Statistics")
s.chapter("Probability Basics & Bayes")
s.sub(PB, "Sample spaces, events and counting probability",
      "With equally likely outcomes, P(A) = favourable/total. The axioms give P(Aᶜ) = 1 − P(A) and P(A ∪ B) = P(A) + P(B) − P(A ∩ B). Counting the sample space correctly, with order where it matters, is most of the work.",
      ["P(A) = favourable/total (equally likely).", "P(Aᶜ) = 1 − P(A).", "P(A ∪ B) = P(A) + P(B) − P(A ∩ B).", "‘At least one’ = 1 − P(none).", "Dice and cards: count ordered outcomes."],
      take=[(PB, "B0 S0 S3 E3 E4 Q0 Q1 Q3 T2 T3 P2 N0"), (PBX, "S0 E0 E1 E3 Q0 Q1 T0 T1 T2")], subs=["Dice & coins"], analogy=PB, widget="prob", hint="Simulate dice and coins and compare frequencies with the exact probabilities.")
s.sub("engm-pb-conditional", "Conditional probability and independence",
      "P(A | B) = P(A ∩ B)/P(B) restricts the sample space to B. A and B are independent when P(A ∩ B) = P(A)P(B). Mutually exclusive events with positive probability are never independent.",
      ["P(A|B) = P(A ∩ B)/P(B).", "Multiplication: P(A ∩ B) = P(A)P(B|A).", "Independent ⇔ P(A ∩ B) = P(A)P(B).", "Exclusive ≠ independent.", "Without replacement, probabilities change each draw."],
      take=[(PB, "B1 S1 E1 E2 Q2 T0 P0"), (PBB, "E2 E3 E4 Q0 Q1 Q3 T1 T3")], subs=["Independence"], analogy=("🔍", "Zooming into the evidence", "Conditioning on B throws away every outcome outside B and rescales what is left."))
s.sub(PBB, "Total probability and Bayes' theorem",
      "Split the sample space into causes A₁…A_k. Total probability gives P(B) = ΣP(Aᵢ)P(B|Aᵢ); Bayes reverses the conditioning: P(Aⱼ|B) = P(Aⱼ)P(B|Aⱼ)/P(B). A tree or a table of natural frequencies makes it mechanical.",
      ["P(B) = Σ P(Aᵢ)P(B|Aᵢ).", "P(Aⱼ|B) = P(Aⱼ)P(B|Aⱼ)/P(B).", "Rare conditions give small posteriors even with good tests.", "Don't confuse P(A|B) with P(B|A).", "Draw a tree with priors and likelihoods."],
      take=[(PB, "B2 B3 B4 S2 E0 T1 P1 N1"), (PBB, "S0 S1 E0 E1 Q2 T0 T2"), (PBX, "E4 Q3")], subs=["Bayes with tables", "Bayes & conditional"], analogy=PBB)

s.chapter("Random Variables & Distributions")
s.sub(RV, "Random variables, PMF, PDF and CDF",
      "A random variable assigns a number to each outcome. A discrete one has a probability mass function (PMF) p(x); a continuous one a density f(x) with probabilities as areas. The CDF F(x) = P(X ≤ x) rises from 0 to 1 in both cases.",
      ["PMF: p(x) ≥ 0, Σp = 1.", "PDF: f ≥ 0, ∫f = 1; P(X = a) = 0 for continuous X.", "CDF F(x) = P(X ≤ x), non-decreasing, 0 → 1.", "P(a < X ≤ b) = F(b) − F(a).", "f = F′ for continuous X."],
      take=[(RV, "B0 B4 S0 T3")], subs=["Random variables"], analogy=RV,
      sections=[dict(h="Finding constants and probabilities", md="""- If p(x) = k·g(x), find k from Σp(x) = 1 (or ∫f = 1).
- P(a < X ≤ b) = F(b) − F(a); for continuous X the endpoints do not matter.
- The **median** m solves F(m) = 1/2; the **mode** is where p or f is largest.
- For f(x) = 2x on [0, 1]: F(x) = x², P(X ≤ 1/2) = 1/4, median 1/√2.""")],
      examples=[Ex("Normalising a PMF", "P(X = x) = kx for x = 1, 2, 3, 4. Find k.", ["k(1 + 2 + 3 + 4) = 10k = 1.", "k = **1/10**."], "**1/10**", verify=lambda: str(F(1, 10))),
                Ex("Normalising a PDF", "f(x) = cx² on [0, 3]. Find c.", ["∫₀³ cx² dx = 9c = 1.", "c = **1/9**."], "**1/9**", verify=lambda: str(F(1, 9))),
                Ex("CDF", "f(x) = 2x on [0, 1]. Find P(1/4 < X ≤ 1/2).", ["F(x) = x².", "1/4 − 1/16 = **3/16**."], "**3/16**", verify=lambda: str(F(1, 4) - F(1, 16))),
                Ex("Median", "Median of the exponential distribution with rate 2?", ["1 − e^(−2m) = 1/2 ⇒ m = ln 2/2 ≈ **0.347**."], "**ln 2 / 2**", verify=lambda: "ln 2 / 2")],
      quick=[("For continuous X, P(X = 2) is", ["f(2)", "0", "F(2)", "1"], 1, "Single points have zero probability."), ("A CDF is always", ["decreasing", "non-decreasing", "periodic", "bounded by 1/2"], 1, "Accumulates probability."),
             ("f(x) = 3x² on [0, 1]. F(1/2) =", ["1/8", "3/4", "1/2", "3/8"], 0, "x³ at 1/2.")],
      traps=[("Density is not probability", "f(x) can exceed 1; areas are probabilities."), ("Endpoints", "For continuous X, < and ≤ give the same probability."), ("Forgetting to normalise", "Find the constant first.")])
s.sub("engm-pb-expectation", "Expectation and variance",
      "E[X] = Σx·p(x) (or ∫x f(x)dx) is the balance point; Var(X) = E[X²] − (E[X])² measures spread. Expectation is linear even without independence; variances add only for independent variables, and Var(aX + b) = a²Var(X).",
      ["E[aX + bY] = aE[X] + bE[Y] always.", "Var(X) = E[X²] − (E[X])².", "Var(aX + b) = a²Var(X).", "Independent: Var(X ± Y) = Var X + Var Y.", "Indicator variables turn counts into sums of probabilities."],
      take=[(RV, "B2 S1 E4 Q1 T0 T1 P0 N1"), (PBD, "S1 E3 E4 Q2 T0 T1"), (PBX, "E3 Q2")], subs=["Expectation & variance"], analogy=("⚖️", "Balance point", "The mean is where a seesaw holding the probability weights would balance."))
s.sub(PBD, "Discrete distributions: binomial, geometric and Poisson",
      "Binomial(n, p) counts successes in n independent trials; geometric(p) counts trials until the first success; Poisson(λ) counts rare events and approximates the binomial when n is large and p small (λ = np).",
      ["Binomial: C(n, k)pᵏ(1 − p)ⁿ⁻ᵏ; mean np, variance np(1 − p).", "Geometric: (1 − p)ᵏ⁻¹p; mean 1/p.", "Poisson: e^(−λ)λᵏ/k!; mean = variance = λ.", "Bernoulli: mean p, variance p(1 − p).", "Poisson ≈ binomial for large n, small p."],
      take=[(RV, "S2 E0 E1 E2 Q0 T2 P1"), (PBD, "S0 E0 E1 E2 Q0 Q1 Q3 T2 T3"), (PBX, "E2 T3")], subs=["Distribution formulas", "Distributions"], analogy=PBD)
s.sub("engm-pb-continuous", "Continuous distributions: uniform, exponential and normal",
      "Uniform[a, b] spreads probability evenly; exponential(λ) models waiting times and is memoryless; the normal N(μ, σ²) is the bell curve, standardised by z = (x − μ)/σ and read from Φ.",
      ["Uniform: mean (a + b)/2, variance (b − a)²/12.", "Exponential: P(X > t) = e^(−λt), mean 1/λ, memoryless.", "Normal: z = (x − μ)/σ.", "68–95–99.7 rule for ±1σ, ±2σ, ±3σ.", "Sum of independent normals is normal."],
      take=[(RV, "B1 B3 S3 E3 Q2 Q3 P2 N0"), (PBD, "E5")], subs=["Continuous distributions"], analogy=("🔔", "The bell curve", "Add up many small independent effects and the total settles into the same bell shape."),
      sections=[dict(h="The normal distribution", md="""N(μ, σ²) has density (1/(σ√(2π)))·e^(−(x − μ)²/(2σ²)), symmetric about μ, with mean = median = mode = μ.

To find probabilities, **standardise**: Z = (X − μ)/σ is N(0, 1), and P(X ≤ x) = Φ((x − μ)/σ). Useful values: Φ(1) ≈ 0.8413, Φ(2) ≈ 0.9772, Φ(3) ≈ 0.9987, and Φ(−z) = 1 − Φ(z).

- About 68% of values lie within 1σ of the mean, 95% within 2σ, 99.7% within 3σ.
- If X ~ N(μ₁, σ₁²) and Y ~ N(μ₂, σ₂²) are independent, X + Y ~ N(μ₁ + μ₂, σ₁² + σ₂²).""")],
      examples=[Ex("Standardising", "X ~ N(50, 4²). P(X ≤ 58)?", ["z = (58 − 50)/4 = 2.", "Φ(2) ≈ **0.9772**."], "**0.9772**", verify=lambda: "%.4f" % 0.9772),
                Ex("Symmetric interval", "X ~ N(100, 15²). P(85 < X < 115)?", ["±1σ: 2Φ(1) − 1 = 2(0.8413) − 1 = **0.6826**."], "**0.6826**", verify=lambda: "%.4f" % (2 * 0.8413 - 1)),
                Ex("Memoryless", "Waiting time is exponential with mean 10 minutes. Given you have waited 5 minutes, P(wait ≥ 10 more)?", ["λ = 1/10. Memoryless: P(X > 10) = e^(−1) ≈ **0.368**."], "**e⁻¹ ≈ 0.368**", verify=lambda: "e⁻¹ ≈ %.3f" % math.exp(-1))],
      quick=[("Z = (X − μ)/σ has mean and variance", ["0 and 1", "μ and σ", "1 and 0", "0 and σ²"], 0, "Standard normal."), ("The exponential distribution is", ["memoryless", "symmetric", "bounded", "discrete"], 0, "P(X > s + t | X > s) = P(X > t).")],
      traps=[("σ vs σ²", "N(μ, σ²) lists the variance; standardise with σ."), ("Φ(−z)", "Equals 1 − Φ(z)."), ("Exponential rate vs mean", "Mean is 1/λ.")])
s.sub("engm-pb-stats", "Mean, median, mode and standard deviation",
      "For data, the mean is the average, the median the middle value of the sorted list, the mode the most frequent value; variance is the average squared deviation from the mean and the standard deviation its square root. Shifting data moves the centre; scaling scales the spread.",
      ["Mean = Σx/n; median = middle of the sorted data; mode = most frequent.", "Variance = Σ(x − x̄)²/n = mean of squares − square of mean.", "SD = √variance.", "Adding c shifts mean, median, mode by c; SD unchanged.", "Multiplying by a scales all of them (SD by |a|)."],
      subs=["Descriptive statistics"], analogy=("📊", "Summing up a class", "One number for the typical mark (mean or median) and one for how scattered the marks are (standard deviation)."),
      sections=[dict(h="Measures of centre", md="""- **Mean** x̄ = (x₁ + … + xₙ)/n. Sensitive to outliers.
- **Median**: sort the data; the middle value for odd n, the average of the two middle values for even n. Robust to outliers.
- **Mode**: the most frequent value (there may be several, or none).

For a symmetric distribution mean = median = mode; for right-skewed data typically mean > median > mode. Empirical relation for moderately skewed data: mode ≈ 3·median − 2·mean."""),
                dict(h="Measures of spread", md="""- **Range** = max − min.
- **Variance** σ² = Σ(xᵢ − x̄)²/n = (Σxᵢ²)/n − x̄². (The *sample* variance divides by n − 1; GATE usually states which.)
- **Standard deviation** σ = √σ².

Transformations: if yᵢ = a·xᵢ + b then ȳ = a·x̄ + b, median and mode transform the same way, and σ_y = |a|·σ_x (b does not change the spread)."""),
                dict(h="Grouped data and combining groups", md="""For values xᵢ with frequencies fᵢ: x̄ = Σfᵢxᵢ/Σfᵢ. The mean of two combined groups is the weighted mean (n₁x̄₁ + n₂x̄₂)/(n₁ + n₂). Correlation r = cov(X, Y)/(σ_Xσ_Y) lies in [−1, 1] and measures linear association.""")],
      examples=[Ex("Mean, median, mode", "Data: 4, 8, 6, 5, 3, 8, 7. Find mean, median and mode.", ["Sum 41, n = 7: mean 41/7 ≈ 5.857.", "Sorted 3 4 5 6 7 8 8: median 6.", "Mode 8 (twice)."], "Mean **41/7**, median **6**, mode **8**", verify=lambda: "Mean %s, median %d, mode %d" % (G2.fm(F(41, 7)), sorted([4, 8, 6, 5, 3, 8, 7])[3], 8)),
                Ex("Variance", "Population variance and SD of 2, 4, 4, 4, 5, 5, 7, 9?", ["Mean 40/8 = 5. Squared deviations 9, 1, 1, 1, 0, 0, 4, 16: sum 32.", "Variance 32/8 = 4, SD **2**."], "Variance **4**, SD **2**", verify=lambda: "Variance %d, SD %d" % (sum((x - 5) ** 2 for x in [2, 4, 4, 4, 5, 5, 7, 9]) // 8, 2)),
                Ex("Transformation", "Data has mean 20 and SD 5. Each value is doubled and 3 is subtracted. New mean and SD?", ["Mean 2·20 − 3 = 37.", "SD 2·5 = 10 (the −3 does not change spread)."], "Mean **37**, SD **10**", verify=lambda: "Mean %d, SD %d" % (2 * 20 - 3, 2 * 5)),
                Ex("Combined mean", "Group A: 10 students, mean 60. Group B: 30 students, mean 80. Combined mean?", ["(10·60 + 30·80)/40 = 3000/40 = **75**."], "**75**", verify=lambda: str((10 * 60 + 30 * 80) // 40))],
      quick=[("Median of 1, 3, 3, 7, 10, 12", ["3", "5", "6", "7"], 1, "(3 + 7)/2."), ("Adding 5 to every value changes the SD by", ["+5", "×5", "nothing", "+25"], 2, "Shift only."),
             ("Which is most affected by an outlier?", ["mean", "median", "mode", "none"], 0, "The mean uses every value."), ("Variance of 3, 3, 3, 3", ["0", "3", "9", "1"], 0, "No spread.")],
      traps=[("Median of even n", "Average the two middle values."), ("Population vs sample variance", "Divide by n or n − 1 as the question states."), ("SD under scaling", "Multiply by |a|; adding b changes nothing.")])
