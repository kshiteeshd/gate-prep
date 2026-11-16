"""ENGM: hand-written chapters for logic, sets/relations/functions, posets, groups, graphs, combinatorics, calculus and probability.
Each chapter keeps its existing overview lessons and adds focused lessons with worked examples and per-lesson practice."""
import itertools
import math
from fractions import Fraction as F

from content import g_math2 as M
from learn import Ex, lesson

S = "ENGM"
LG, ST, PO, GP, GR, CB, CA, PB = ("Mathematical Logic", "Sets, Relations & Functions", "Partial Orders & Lattices", "Groups & Monoids", "Graph Theory",
                                   "Combinatorics & Recurrences", "Calculus", "Probability & Statistics")
T_LG, T_ST, T_PO, T_GP, T_GR, T_CB = ("Propositional & First-Order Logic", "Sets, Relations & Functions", "Partial Orders & Lattices", "Groups & Monoids", "Graph Theory", "Combinatorics & Recurrences")
T_LIM, T_INT, T_PB, T_RV = ("Limits, Continuity & Differentiation", "Maxima, Minima & Integration", "Probability Basics & Bayes", "Random Variables & Distributions")
C = math.comb


def lc(a, b):
    return a * b // math.gcd(a, b)


# ====================================================== LOGIC ======================================================
lesson(subject=S, chapter=LG, ch_no=1, no=3, slug="engm-lg-forms", title="3 · Implications, converses and equivalent forms",
       topic=T_LG, subs=["Logical forms", "Equivalences", "Boolean functions count"], minutes=16, weight=4, widget="none",
       key="P → Q is false in exactly one case (P true, Q false) and equals ¬P ∨ Q. Its contrapositive is equivalent; its converse and inverse are not. Most equivalence questions reduce to this one rewrite plus De Morgan.",
       analogy=("🤝", "A promise", "'If you pass, I buy lunch.' The promise is broken only if you pass and I do not buy lunch. If you fail, whatever I do keeps the promise true."),
       sections=[
           dict(h="Implication and its relatives", md="""| Statement | Form | Equivalent to P → Q? |
|---|---|---|
| Implication | P → Q | itself (≡ ¬P ∨ Q) |
| Converse | Q → P | no |
| Inverse | ¬P → ¬Q | no (it is the converse's contrapositive) |
| Contrapositive | ¬Q → ¬P | **yes** |
| Negation | P ∧ ¬Q | the opposite of P → Q |

P ↔ Q is (P → Q) ∧ (Q → P) and is true when P and Q have the same truth value. P ⊕ Q is true when they differ."""),
           dict(h="Rewrite rules", md="""- De Morgan: ¬(P ∧ Q) ≡ ¬P ∨ ¬Q and ¬(P ∨ Q) ≡ ¬P ∧ ¬Q.
- Distribution: P ∧ (Q ∨ R) ≡ (P ∧ Q) ∨ (P ∧ R).
- Absorption: P ∨ (P ∧ Q) ≡ P.
- Implication to disjunction: P → Q ≡ ¬P ∨ Q; P → (Q → R) ≡ (P ∧ Q) → R.

**Counting:** a formula on n variables has 2ⁿ truth-table rows and there are 2^(2ⁿ) different Boolean functions of n variables. Exactly half of the rows of an n-variable XOR are true."""),
       ],
       examples=[
           Ex("Contrapositive", "Write the contrapositive of \"if x is even then x² is even\".", ["Negate and swap: ¬Q → ¬P.", "**If x² is odd then x is odd.**"], "If x² is odd then x is odd.", verify=lambda: "If x² is odd then x is odd."),
           Ex("Negation of an implication", "Which formula is equivalent to ¬(P → Q)?", ["P → Q ≡ ¬P ∨ Q; negate: P ∧ ¬Q."], "**P ∧ ¬Q**", verify=lambda: "P ∧ ¬Q" if all((not ((not p) or q)) == (p and not q) for p in (0, 1) for q in (0, 1)) else "?"),
           Ex("Number of functions", "How many Boolean functions of 3 variables are there?", ["The truth table has 2³ = 8 rows, each 0 or 1.", "2⁸ = **256**."], "**256**", verify=lambda: str(2 ** (2 ** 3))),
           Ex("Implication false cases", "In how many of the 8 assignments of (p, q, r) is (p ∧ q) → r false?", ["False only when p ∧ q is true and r is false: p = q = 1, r = 0.", "Exactly **1** assignment."], "**1**", verify=lambda: str(sum(1 for p, q, r in itertools.product((0, 1), repeat=3) if (p and q) and not r))),
           Ex("Currying", "Is p → (q → r) equivalent to (p ∧ q) → r?", ["p → (q → r) ≡ ¬p ∨ ¬q ∨ r ≡ ¬(p ∧ q) ∨ r ≡ (p ∧ q) → r.", "**Yes.**"], "**Yes**", verify=lambda: "Yes" if all(((not p) or ((not q) or r)) == ((not (p and q)) or r) for p, q, r in itertools.product((0, 1), repeat=3)) else "No"),
       ],
       traps=[("Converse is not equivalent", "Only the contrapositive is equivalent to the original."),
              ("Vacuous truth", "P → Q is true whenever P is false."),
              ("Functions vs rows", "2ⁿ rows but 2^(2ⁿ) functions."),
              ("Negating implication", "The negation is P ∧ ¬Q, not ¬P → ¬Q.")],
       quick=[("¬(P → Q) ≡", ["¬P → ¬Q", "P ∧ ¬Q", "¬P ∨ Q", "Q → P"], 1, "The only failing case."),
              ("Boolean functions of 2 variables", ["4", "8", "16", "32"], 2, "2^(2²)."),
              ("P → Q is equivalent to", ["Q → P", "¬Q → ¬P", "¬P → ¬Q", "P ∧ Q"], 1, "Contrapositive."),
              ("When is P → Q true if P is false?", ["never", "always", "if Q is true", "if Q is false"], 1, "Vacuous truth.")],
       summary=["P → Q ≡ ¬P ∨ Q; false only for T → F.", "Contrapositive ≡ original; converse and inverse are not.", "¬(P → Q) ≡ P ∧ ¬Q.", "n variables: 2ⁿ rows, 2^(2ⁿ) functions.", "De Morgan flips ∧ and ∨.", "p → (q → r) ≡ (p ∧ q) → r."])

lesson(subject=S, chapter=LG, ch_no=1, no=4, slug="engm-lg-fol", title="4 · Translating English into first-order logic",
       topic=T_LG, subs=["FOL translation", "First-order logic"], minutes=18, weight=4, widget="none",
       key="Quantifier order matters: ∀x ∃y means 'each x has its own y', ∃y ∀x means 'one y serves every x'. Negation flips each quantifier and negates the body. Every GATE translation question tests exactly these two facts.",
       analogy=("🔑", "Keys and doors", "∀door ∃key: every door has some key that opens it. ∃key ∀door: one master key opens every door. The second is a far stronger claim."),
       sections=[
           dict(h="Patterns", md="""| English | Logic |
|---|---|
| Every x has some y with R | ∀x ∃y R(x, y) |
| One y works for all x | ∃y ∀x R(x, y) |
| All A are B | ∀x (A(x) → B(x)) |
| Some A is B | ∃x (A(x) ∧ B(x)) |
| No A is B | ∀x (A(x) → ¬B(x)) |

Note the connective: **∀ goes with →, ∃ goes with ∧**. Writing ∀x (A(x) ∧ B(x)) says everything is both A and B, usually false and not intended; ∃x (A(x) → B(x)) is true whenever anything is not A."""),
           dict(h="Negation and order", md="""¬∀x P(x) ≡ ∃x ¬P(x) and ¬∃x P(x) ≡ ∀x ¬P(x). Push the negation inward flipping each quantifier. ∀x∀y and ∃x∃y can be swapped freely; mixed ∀∃ cannot: ∃y ∀x R(x, y) ⊨ ∀x ∃y R(x, y) but not the other way round."""),
       ],
       examples=[
           Ex("Every has some", "Express 'every student takes some course' with T(x, y) meaning x takes y.", ["Each student picks a (possibly different) course.", "**∀x ∃y T(x, y)**."], "**∀x ∃y T(x, y)**", verify=lambda: "∀x ∃y T(x, y)"),
           Ex("Negation", "Negate ∀x ∃y (x < y).", ["Flip each quantifier and negate the body: ∃x ∀y ¬(x < y).", "i.e. **∃x ∀y (y ≤ x)**: a largest element exists."], "**∃x ∀y (y ≤ x)**", verify=lambda: "∃x ∀y (y ≤ x)"),
           Ex("All are", "Translate 'all prime numbers greater than 2 are odd'.", ["∀x ((P(x) ∧ x > 2) → Odd(x))."], "**∀x ((P(x) ∧ x > 2) → Odd(x))**", verify=lambda: "∀x ((P(x) ∧ x > 2) → Odd(x))"),
           Ex("Which implies which", "Does ∃y ∀x R(x, y) imply ∀x ∃y R(x, y)?", ["If one y works for all x, then for every x that same y works.", "**Yes**; the converse fails (R(x, y) = x = y over two elements)."], "**Yes**", verify=lambda: "Yes"),
           Ex("Counterexample", "Over {1, 2} with R(x, y) meaning x = y, which of ∀x∃y R and ∃y∀x R holds?", ["∀x∃y: each x equals itself: true.", "∃y∀x: no single y equals both 1 and 2: false.", "Only **∀x ∃y R**."], "Only **∀x ∃y R**", verify=lambda: "Only ∀x ∃y R" if all(any(x == y for y in (1, 2)) for x in (1, 2)) and not any(all(x == y for x in (1, 2)) for y in (1, 2)) else "?"),
       ],
       traps=[("∀ with ∧", "∀x (A(x) ∧ B(x)) says everything is A and B."),
              ("∃ with →", "∃x (A(x) → B(x)) is true if anything is not A."),
              ("Swapping quantifiers", "∀∃ and ∃∀ are different statements."),
              ("Negation", "¬∀x P ≡ ∃x ¬P, never ∀x ¬P.")],
       quick=[("'Some A is B' is", ["∃x (A→B)", "∃x (A∧B)", "∀x (A∧B)", "∀x (A→B)"], 1, "∃ pairs with ∧."),
              ("¬∀x P(x) ≡", ["∀x ¬P", "∃x ¬P", "∃x P", "¬∃x ¬P"], 1, "Flip the quantifier."),
              ("∃y∀x R(x,y) implies", ["∀x∃y R", "nothing", "∀y∃x R", "¬∀x∃y R"], 0, "The master key opens every door."),
              ("'No A is B'", ["∀x (A → ¬B)", "∃x (A ∧ ¬B)", "∀x (A ∧ ¬B)", "∃x (A → ¬B)"], 0, "Universal with implication.")],
       summary=["∀ with →, ∃ with ∧.", "∃y∀x is stronger than ∀x∃y.", "Negation flips quantifiers and negates the body.", "Same-type quantifiers commute.", "'No A is B' = ∀x (A → ¬B).", "Test claims on a two-element model."])

lesson(subject=S, chapter=LG, ch_no=1, no=5, slug="engm-lg-models", title="5 · Satisfiability, validity and counting models",
       topic=T_LG, subs=["Satisfiability", "Counting models", "Equivalences", "Logical forms"], minutes=18, weight=4, widget="none",
       key="A formula is valid (a tautology) if true under every assignment, satisfiable if true under some, unsatisfiable if under none. Counting models of an n-variable formula is counting rows; use the structure of the formula rather than a full table.",
       analogy=("🔍", "Searching rows", "Think of the truth table as a list of 2ⁿ worlds. Valid means every world agrees, satisfiable means at least one does, and a model count tells you how many do."),
       sections=[
           dict(h="Three kinds of formula", md="""- **Tautology (valid):** true in all 2ⁿ rows. Example: P ∨ ¬P, (P → Q) ∨ (Q → P).
- **Contradiction (unsatisfiable):** true in no row. Example: P ∧ ¬P.
- **Contingent:** true in some rows, false in others.

F is valid iff ¬F is unsatisfiable. SAT (is there a satisfying assignment?) is NP-complete; checking validity of a propositional formula is co-NP-complete."""),
           dict(h="Counting models quickly", md="""- A conjunction of k distinct literals over distinct variables has 2^(n−k) models.
- A disjunction of k literals is false in only 1 of 2^k combinations: 2ⁿ − 2^(n−k) models.
- P → Q is false in exactly ¼ of the rows (when P = 1, Q = 0): ¾ of 2ⁿ models.
- If F and G use disjoint variables, models multiply.
- XOR/parity of n variables is true in 2^(n−1) rows.""")],
       examples=[
           Ex("Models of a clause", "How many of the 16 assignments of p, q, r, s satisfy p ∨ q ∨ r?", ["p ∨ q ∨ r is false only when p = q = r = 0 (s free: 2 assignments).", "16 − 2 = **14**."], "**14**", verify=lambda: str(sum(1 for p, q, r, s in itertools.product((0, 1), repeat=4) if p or q or r))),
           Ex("Implication models", "How many assignments of (p, q) satisfy p → q?", ["False only for p = 1, q = 0.", "4 − 1 = **3**."], "**3**", verify=lambda: str(sum(1 for p, q in itertools.product((0, 1), repeat=2) if (not p) or q))),
           Ex("Tautology?", "Is (p → q) ∨ (q → p) a tautology?", ["If q is true, p → q is true. If q is false, q → p is true.", "Always true: **yes**."], "**Yes**", verify=lambda: "Yes" if all(((not p) or q) or ((not q) or p) for p, q in itertools.product((0, 1), repeat=2)) else "No"),
           Ex("Conjunction of literals", "How many of the 2⁶ assignments satisfy p₁ ∧ ¬p₂ ∧ p₃?", ["Three variables are fixed, three are free: 2³ = **8**."], "**8**", verify=lambda: str(sum(1 for t in itertools.product((0, 1), repeat=6) if t[0] and not t[1] and t[2]))),
           Ex("Parity", "How many assignments of 5 variables make p₁ ⊕ … ⊕ p₅ true?", ["Odd number of trues: half of the 32 assignments = **16**."], "**16**", verify=lambda: str(sum(1 for t in itertools.product((0, 1), repeat=5) if sum(t) % 2 == 1))),
       ],
       traps=[("Satisfiable vs valid", "Valid means true in EVERY row."),
              ("Forgetting free variables", "Variables not in the formula still double the count."),
              ("¬F", "F valid ⇔ ¬F unsatisfiable."),
              ("SAT difficulty", "SAT is NP-complete; validity is co-NP-complete.")],
       quick=[("p ∧ ¬p is", ["a tautology", "a contradiction", "contingent", "valid"], 1, "Never true."),
              ("Models of p ∨ q over 3 variables (p, q, r)", ["3", "6", "7", "8"], 1, "3 of 4 for (p,q), times 2 for r."),
              ("A formula is valid iff its negation is", ["satisfiable", "unsatisfiable", "contingent", "a tautology"], 1, "Duality."),
              ("A conjunction of 3 literals over 5 variables has how many models", ["2", "4", "8", "16"], 1, "2^(5−3).")],
       summary=["Valid = every row, satisfiable = some row, contradiction = no row.", "F valid ⇔ ¬F unsatisfiable.", "k-literal conjunction: 2^(n−k) models.", "k-literal clause: 2ⁿ − 2^(n−k).", "P → Q false only for (1, 0).", "SAT is NP-complete."])

# ====================================================== SETS, RELATIONS, FUNCTIONS ======================================================
lesson(subject=S, chapter=ST, ch_no=2, no=4, slug="engm-st-relations-count", title="4 · Counting relations by property",
       topic=T_ST, subs=["Counting relations on a set", "Counting relations & functions", "Relation properties"], minutes=20, weight=5, widget="none",
       key="A relation on an n-element set is a subset of its n² ordered pairs. Each property pins some pairs and leaves the others free, so the count is 2 to the power of the free choices. Equivalence relations correspond to set partitions (Bell numbers).",
       analogy=("🎛️", "A board of switches", "Each ordered pair is a light switch. Reflexive says the n diagonal switches are forced on; symmetric says paired switches move together; antisymmetric forbids both partners being on."),
       sections=[
           dict(h="The counting table", md="""For a set with n elements (n² ordered pairs, n diagonal pairs, n(n−1)/2 unordered off-diagonal pairs):

| Property | Count |
|---|---|
| any relation | 2^(n²) |
| reflexive | 2^(n²−n) |
| irreflexive | 2^(n²−n) |
| symmetric | 2^(n(n+1)/2) |
| antisymmetric | 2ⁿ · 3^(n(n−1)/2) |
| asymmetric | 3^(n(n−1)/2) |
| reflexive and symmetric | 2^(n(n−1)/2) |
| equivalence | Bell number B(n): 1, 2, 5, 15, 52, 203, … |

For each unordered pair {a, b} an antisymmetric relation chooses among 3 options: neither, only (a, b), only (b, a)."""),
           dict(h="Properties of a given relation", md="""Test from the definition: reflexive (all (a, a) present), symmetric ((a, b) ⇒ (b, a)), antisymmetric ((a, b) and (b, a) ⇒ a = b), transitive ((a, b), (b, c) ⇒ (a, c)). Note that the empty relation is symmetric, antisymmetric and transitive but not reflexive (for non-empty sets); the relation = is reflexive, symmetric, antisymmetric and transitive at once.""")],
       examples=[
           Ex("Reflexive count", "How many reflexive relations exist on a 4-element set?", ["16 pairs, 4 forced: 12 free. 2¹² = **4096**."], "**4096**", verify=lambda: str(2 ** (16 - 4))),
           Ex("Symmetric count", "How many symmetric relations exist on a 3-element set?", ["n(n+1)/2 = 6 free choices (3 diagonal + 3 pairs).", "2⁶ = **64**."], "**64**", verify=lambda: str(2 ** 6)),
           Ex("Antisymmetric count", "How many antisymmetric relations exist on a 3-element set?", ["Diagonal: 2³. Each of 3 pairs: 3 choices: 3³.", "8 · 27 = **216**."], "**216**", verify=lambda: str(2 ** 3 * 3 ** 3)),
           Ex("Equivalence count", "How many equivalence relations exist on a 4-element set?", ["Count partitions: S(4,1) + S(4,2) + S(4,3) + S(4,4) = 1 + 7 + 6 + 1 = **15**."], "**15**", verify=lambda: str(M.bell(4))),
           Ex("Both reflexive and symmetric", "How many relations on a 5-element set are reflexive and symmetric?", ["10 unordered pairs free: 2¹⁰ = **1024**."], "**1024**", verify=lambda: str(2 ** 10)),
       ],
       traps=[("Antisymmetric vs not symmetric", "Antisymmetric allows diagonal pairs and forbids symmetric off-diagonal pairs."),
              ("Equivalence counts", "They are Bell numbers, not 2-powers."),
              ("Empty relation", "It is symmetric, antisymmetric and transitive."),
              ("Mixing n² and n(n+1)/2", "Symmetric counts diagonal pairs as free choices.")],
       quick=[("Reflexive relations on a 3-set", ["8", "64", "512", "256"], 1, "2^(9−3)."),
              ("Number of partitions of a 3-set", ["3", "5", "6", "8"], 1, "B(3) = 5."),
              ("Asymmetric relations on a 2-set", ["3", "4", "8", "16"], 0, "3^1."),
              ("Symmetric relations on a 2-set", ["4", "8", "16", "2"], 1, "2^3.")],
       summary=["All: 2^(n²). Reflexive: 2^(n²−n). Symmetric: 2^(n(n+1)/2).", "Antisymmetric: 2ⁿ·3^(n(n−1)/2). Asymmetric: 3^(n(n−1)/2).", "Equivalence: Bell(n).", "Each property pins pairs; count the free ones.", "= is reflexive, symmetric, antisymmetric and transitive.", "The empty relation is not reflexive."])

lesson(subject=S, chapter=ST, ch_no=2, no=5, slug="engm-st-functions-count", title="5 · Counting functions: injective, surjective, bijective",
       topic=T_ST, subs=["Counting functions", "Counting relations & functions"], minutes=20, weight=5, widget="none",
       key="From an m-set to an n-set: nᵐ functions, P(n, m) injective ones, n!·S(m, n) surjective ones (inclusion–exclusion), n! bijections when m = n. Each count is a product of independent choices or an inclusion–exclusion sum.",
       analogy=("📮", "Posting letters", "Each of m letters is put into one of n boxes: nᵐ ways. Injective means no box gets two letters; surjective means no box stays empty."),
       sections=[
           dict(h="The formulas", md="""| Functions f from A to B (m inputs, n outputs) | Count |
|---|---|
| all | nᵐ |
| one-to-one (needs m ≤ n) | n(n−1)…(n−m+1) = P(n, m) |
| onto (needs m ≥ n) | Σ (−1)ʲ C(n, j)(n − j)ᵐ = n!·S(m, n) |
| bijections (m = n) | n! |
| constant | n |
| partial functions | (n + 1)ᵐ |
| subsets of A | 2ᵐ |

The inclusion–exclusion for onto functions: start with nᵐ, remove those missing at least one element of B, and correct."""),
           dict(h="Facts to remember", md="""A function between finite sets of equal size is injective iff surjective iff bijective. If m > n, no injection exists (pigeonhole); if m < n, no surjection exists. The number of subsets of size k is C(n, k).""")],
       examples=[
           Ex("Injections", "How many one-to-one functions from a 3-set to a 6-set?", ["6 × 5 × 4 = **120**."], "**120**", verify=lambda: str(math.perm(6, 3))),
           Ex("Onto", "How many onto functions from a 4-set to a 2-set?", ["Total 2⁴ = 16; subtract the two constant functions: 14."], "**14**", verify=lambda: str(2 ** 4 - 2)),
           Ex("Onto 5 to 3", "How many onto functions from a 5-set to a 3-set?", ["3⁵ − 3·2⁵ + 3·1⁵ = 243 − 96 + 3 = **150**."], "**150**", verify=lambda: str(3 ** 5 - 3 * 2 ** 5 + 3)),
           Ex("Partial functions", "How many partial functions from a 3-set to a 2-set?", ["Each input is undefined or maps to 2 outputs: 3³ = **27**."], "**27**", verify=lambda: str(3 ** 3)),
           Ex("Equal sizes", "f: A → A with |A| = 5 is injective. How many such f?", ["Injective on a finite set to itself means bijective: 5! = **120**."], "**120**", verify=lambda: str(math.factorial(5))),
       ],
       traps=[("nᵐ vs mⁿ", "Functions A → B number |B|^|A|."),
              ("Onto needs inclusion–exclusion", "Do not just use P(n, m)."),
              ("Equal sizes", "Injective ⇔ surjective only when |A| = |B|."),
              ("Subsets", "A set of m elements has 2ᵐ subsets.")],
       quick=[("Functions from a 3-set to a 4-set", ["12", "64", "81", "24"], 1, "4³."),
              ("Injections from a 2-set to a 5-set", ["10", "20", "25", "32"], 1, "5·4."),
              ("Onto functions from a 3-set to a 3-set", ["3", "6", "9", "27"], 1, "3!."),
              ("Number of subsets of a 6-set", ["12", "36", "64", "720"], 2, "2⁶.")],
       summary=["All: nᵐ.", "Injective: P(n, m).", "Onto: n!·S(m, n) by inclusion–exclusion.", "Bijections: n!.", "Equal finite sizes: injective ⇔ onto.", "Partial: (n + 1)ᵐ."])

lesson(subject=S, chapter=ST, ch_no=2, no=6, slug="engm-st-closures-eq", title="6 · Closures, equivalence classes and divisibility",
       topic=T_ST, subs=["Closures", "Inclusion–exclusion", "Divisibility counting", "Relation properties"], minutes=20, weight=4, widget="none",
       key="Closures add the fewest pairs needed for a property: reflexive adds the diagonal, symmetric adds reverses, transitive needs repeated composition (Warshall). Equivalence relations partition the set; divisibility counts are inclusion–exclusion on multiples.",
       analogy=("🌐", "Friend circles", "A relation is who knows whom. The transitive closure adds every friend-of-a-friend until nothing new appears; an equivalence relation is a set of closed circles that never overlap."),
       sections=[
           dict(h="Closures", md="""- **Reflexive closure:** R ∪ {(a, a)}.
- **Symmetric closure:** R ∪ {(b, a) : (a, b) ∈ R}.
- **Transitive closure:** keep adding (a, c) when (a, b) and (b, c) are present, until stable. On n elements Warshall's algorithm does it in O(n³).

Equivalence closure = transitive closure of the symmetric closure of the reflexive closure. Order matters when combining: do reflexive and symmetric first, then transitive."""),
           dict(h="Equivalence classes and counting multiples", md="""An equivalence relation splits the set into disjoint classes; the number of pairs in the relation is the sum of (class size)². For multiples among 1..N: ⌊N/a⌋ multiples of a, ⌊N/lcm(a, b)⌋ of both, and |A ∪ B| = |A| + |B| − |A ∩ B| (add the three-way term for three sets).""")],
       examples=[
           Ex("Reflexive closure size", "R = {(1,2), (2,3)} on {1, 2, 3}. How many pairs in its reflexive closure?", ["Add (1,1), (2,2), (3,3): 2 + 3 = **5**."], "**5**", verify=lambda: str(2 + 3)),
           Ex("Transitive closure", "R = {(1,2), (2,3), (3,4)}. How many pairs in its transitive closure?", ["Add (1,3), (2,4), (1,4): 3 + 3 = **6**."], "**6**", verify=lambda: str(len({(1, 2), (2, 3), (3, 4), (1, 3), (2, 4), (1, 4)}))),
           Ex("Pairs in an equivalence relation", "An equivalence relation on 6 elements has classes of sizes 3, 2, 1. How many ordered pairs does it contain?", ["9 + 4 + 1 = **14**."], "**14**", verify=lambda: str(9 + 4 + 1)),
           Ex("Multiples", "How many integers in 1..100 are divisible by 3 or 5?", ["33 + 20 − 6 = **47**."], "**47**", verify=lambda: str(sum(1 for k in range(1, 101) if k % 3 == 0 or k % 5 == 0))),
           Ex("Divisible by none", "How many integers in 1..60 are divisible by none of 2, 3, 5?", ["60·(1/2)(2/3)(4/5) = **16** (this is φ(60))."], "**16**", verify=lambda: str(sum(1 for k in range(1, 61) if k % 2 and k % 3 and k % 5))),
       ],
       traps=[("Closure order", "Make it symmetric before transitive."),
              ("Adding too much", "A closure adds only forced pairs."),
              ("Equivalence pair count", "Sum of squares of class sizes."),
              ("Inclusion–exclusion signs", "Add singles, subtract pairs, add triples.")],
       quick=[("Reflexive closure of {(1,2)} on {1,2}", ["{(1,2),(1,1),(2,2)}", "{(1,2),(2,1)}", "{(1,1),(2,2)}", "{(1,2)}"], 0, "Add the diagonal."),
              ("Numbers ≤ 30 divisible by 2 or 3", ["20", "15", "25", "10"], 0, "15 + 10 − 5."),
              ("Equivalence classes are", ["overlapping", "disjoint", "nested", "ordered"], 1, "They partition."),
              ("Warshall's algorithm time", ["O(n)", "O(n²)", "O(n³)", "O(2ⁿ)"], 2, "Three loops.")],
       summary=["Closure = add the fewest forced pairs.", "Reflexive: diagonal. Symmetric: reverses.", "Transitive: repeat until stable (Warshall O(n³)).", "Equivalence ⇒ partition into disjoint classes.", "Pairs = Σ size².", "Multiples: inclusion–exclusion with lcm."])

# ====================================================== POSETS ======================================================
lesson(subject=S, chapter=PO, ch_no=3, no=2, slug="engm-po-divisor", title="2 · Divisor posets: chains, antichains and Hasse edges",
       topic=T_PO, subs=["Divisor poset facts", "Divisor lattice", "Posets"], minutes=18, weight=4, widget="none",
       key="In (Dₙ, |) the elements are the divisors of n, the join is lcm and the meet is gcd. It is a Boolean lattice exactly when n is square-free. Heights, atoms and antichains are read off the prime factorisation.",
       analogy=("🧬", "Exponent grids", "Write each divisor of n = p^a·q^b as the pair of exponents (i, j). Divisibility is the componentwise ≤ order on a grid, which makes chains and antichains easy to see."),
       sections=[
           dict(h="Structure of Dₙ", md="""For n = p₁^a₁ ⋯ p_k^a_k:

- number of elements: (a₁ + 1)(a₂ + 1)…(a_k + 1);
- longest chain from 1 to n has a₁ + … + a_k edges;
- atoms (covering 1) are the primes p₁ … p_k;
- join = lcm, meet = gcd; the lattice is distributive;
- **Boolean (complemented) iff n is square-free**, and then Dₙ ≅ the power set of the k primes (2ᵏ elements)."""),
           dict(h="Chains, antichains and Hasse diagrams", md="""A **chain** is a set of pairwise comparable elements, an **antichain** a set of pairwise incomparable ones. Dilworth: the minimum number of chains covering the poset equals the maximum antichain size. In the Hasse diagram, a is joined to b exactly when b/a is a prime (b covers a). Draw only these edges.""")],
       examples=[
           Ex("Elements", "How many elements are in D₇₂ (72 = 2³·3²)?", ["(3 + 1)(2 + 1) = **12**."], "**12**", verify=lambda: str(len(M.divs(72)))),
           Ex("Longest chain", "Edges in a longest chain from 1 to 72 in D₇₂?", ["3 + 2 = **5** prime factors with multiplicity."], "**5**", verify=lambda: str(3 + 2)),
           Ex("Boolean?", "Is D₃₀ Boolean? Is D₁₂?", ["30 = 2·3·5 is square-free: Boolean (8 elements).", "12 = 2²·3 is not: 2 has no complement."], "D₃₀ yes, D₁₂ no.", verify=lambda: "D₃₀ yes, D₁₂ no."),
           Ex("Largest antichain", "Size of the largest antichain in D₃₀?", ["Atoms {2, 3, 5} form an antichain of size 3, and so does {6, 10, 15}.", "Maximum **3**."], "**3**", verify=lambda: str(max(len(c) for k in range(1, 9) for c in itertools.combinations(M.divs(30), k) if all(a % b and b % a for a, b in itertools.combinations(c, 2))))),
           Ex("Join and meet", "In D₃₆, what are the join and meet of 4 and 6?", ["join = lcm(4, 6) = 12; meet = gcd(4, 6) = 2."], "join **12**, meet **2**", verify=lambda: "join %d, meet %d" % (lc(4, 6), math.gcd(4, 6))),
       ],
       traps=[("Join is lcm", "Not the product."),
              ("Boolean needs square-free", "Repeated primes break complements."),
              ("Chain length vs elements", "Edges = elements − 1."),
              ("Hasse edges", "Only prime-ratio links, no transitive edges.")],
       quick=[("Elements of D₆₀ (2²·3·5)", ["8", "12", "6", "10"], 1, "3·2·2."),
              ("Atoms of D₃₀", ["1", "2", "3", "5"], 2, "2, 3 and 5."),
              ("Join in a divisor lattice is", ["gcd", "lcm", "sum", "product"], 1, "Least upper bound."),
              ("D₁₈ is Boolean", ["yes", "no", "only if prime", "only if odd"], 1, "18 = 2·3²")],
       summary=["Dₙ has Π(aᵢ + 1) elements.", "Join = lcm, meet = gcd.", "Boolean iff n is square-free.", "Longest chain = number of prime factors with multiplicity.", "Atoms = prime divisors.", "Hasse edge when quotient is prime."])

lesson(subject=S, chapter=PO, ch_no=3, no=3, slug="engm-po-lattice-props", title="3 · Lattice properties and counting orders",
       topic=T_PO, subs=["Lattice basics", "Posets", "Divisor poset facts"], minutes=16, weight=3, widget="none",
       key="A lattice is a poset where every pair has a join (lub) and a meet (glb). Bounded, complemented and distributive lattices are the three refinements tested in GATE. The pentagon N₅ and diamond M₃ are the two forbidden shapes for distributivity.",
       analogy=("🧗", "Meeting points", "In a family tree of climbing routes, any two climbers have a lowest meeting point above them (join) and a highest meeting point below them (meet). A lattice guarantees both always exist."),
       sections=[
           dict(h="Definitions", md="""- **Poset:** reflexive, antisymmetric, transitive relation.
- **Lattice:** every pair has a least upper bound and greatest lower bound.
- **Bounded:** has a least element 0 and greatest element 1 (every finite lattice is bounded).
- **Complement** of a: an element b with a ∨ b = 1 and a ∧ b = 0. **Complemented:** every element has one.
- **Distributive:** a ∧ (b ∨ c) = (a ∧ b) ∨ (a ∧ c). A lattice is distributive iff it has no sublattice isomorphic to the diamond M₃ or the pentagon N₅. In a distributive lattice complements are unique.
- **Boolean lattice:** complemented distributive; the power set of an n-set with 2ⁿ elements."""),
           dict(h="Quick tests", md="""A finite poset with a unique maximal and unique minimal element where every pair has a join is a lattice. Total orders (chains) are lattices and distributive. The set of subsets under ⊆ is a Boolean lattice; the partitions of a set under refinement and the subspaces of a vector space form non-distributive lattices.""")],
       examples=[
           Ex("Boolean sizes", "Possible sizes of a finite Boolean lattice up to 40?", ["Always 2ⁿ: 2, 4, 8, 16, 32.", "**2, 4, 8, 16, 32**."], "**2, 4, 8, 16, 32**", verify=lambda: ", ".join(str(2 ** k) for k in range(1, 6))),
           Ex("Total order", "Is the chain 1 < 2 < 3 < 4 a lattice, and is it complemented?", ["Join = max, meet = min: a lattice.", "Element 2 has no complement (2 ∨ x = 4 needs x = 4, but 2 ∧ 4 = 2 ≠ 1): **not complemented**."], "Lattice, **not** complemented.", verify=lambda: "Lattice, not complemented."),
           Ex("Complement count", "In the Boolean lattice of subsets of {a, b, c}, how many complements does {a} have?", ["Complement of a set is its set complement {b, c}: unique, **1**."], "**1**", verify=lambda: str(1)),
           Ex("Not a lattice", "The poset with elements a, b below c and d (both c and d above both a and b), is it a lattice?", ["a and b have two minimal upper bounds c and d, no least one.", "**Not a lattice**."], "**Not a lattice**", verify=lambda: "Not a lattice"),
       ],
       traps=[("Every poset is a lattice?", "No: pairs may lack a unique lub or glb."),
              ("Complement ≠ inverse", "Complements need both ∨ = 1 and ∧ = 0."),
              ("Distributive tests", "M₃ and N₅ are the forbidden sublattices."),
              ("Chains", "Distributive but usually not complemented.")],
       quick=[("A finite lattice always has", ["a least and greatest element", "complements", "a unique atom", "a Boolean structure"], 0, "Bounded."),
              ("Boolean lattice sizes are", ["any", "powers of 2", "primes", "squares"], 1, "2ⁿ."),
              ("The pentagon N₅ is", ["distributive", "non-distributive", "Boolean", "a chain"], 1, "Forbidden sublattice."),
              ("Complement of {a} in P({a,b,c})", ["{b,c}", "{a,b}", "∅", "{c}"], 0, "Set complement.")],
       summary=["Lattice: every pair has lub and glb.", "Finite lattices are bounded.", "Complemented, distributive, Boolean.", "M₃ and N₅ detect non-distributivity.", "Boolean lattices have 2ⁿ elements.", "Chains are distributive."])

lesson(subject=S, chapter=PO, ch_no=3, no=4, slug="engm-po-problems", title="4 · Poset mixed problem set",
       topic=T_PO, subs=["Divisor poset facts", "Divisor lattice", "Lattice basics", "Posets"], minutes=20, weight=4, widget="none",
       key="Poset questions are short once you list the elements and the covering pairs: draw the Hasse diagram, find maximal and minimal elements, then answer.",
       analogy=("🗂️", "Drawing before answering", "Draw the Hasse diagram first. Chains, antichains, atoms and complements are visible at a glance."),
       sections=[dict(h="Method", md="""1. List the elements and the covering relation.
2. Identify minimal and maximal elements (a poset can have several).
3. For lattice questions check lub and glb for the troublesome pairs only.
4. For divisor posets read everything from the prime factorisation.
5. Count chains with the longest path; count antichains with the middle level.""")],
       examples=[
           Ex("Maximal elements", "In ({2, 3, 4, 6, 12, 24, 36}, |) how many maximal elements?", ["24 and 36 are not divisors of each other and nothing larger exists: **2**."], "**2**", verify=lambda: str(len([x for x in [2, 3, 4, 6, 12, 24, 36] if not any(y != x and y % x == 0 for y in [2, 3, 4, 6, 12, 24, 36])]))),
           Ex("Divisors of 30", "How many Hasse edges in D₃₀?", ["Cube: 8 vertices, 12 edges."], "**12**", verify=lambda: str(len([1 for a in M.divs(30) for b in M.divs(30) if b % a == 0 and b // a in (2, 3, 5)]))),
           Ex("Chain count", "Number of maximal chains from 1 to 30 in D₃₀?", ["Order the three primes in any way: 3! = **6**."], "**6**", verify=lambda: str(math.factorial(3))),
           Ex("Subsets lattice", "Number of elements covering ∅ in the power set of a 5-set?", ["The 5 singletons: **5**."], "**5**", verify=lambda: str(5)),
           Ex("Join", "lub of 8 and 12 in (ℕ, |)?", ["lcm = **24**."], "**24**", verify=lambda: str(lc(8, 12))),
       ],
       traps=[("Maximal vs greatest", "A poset may have several maximal elements and no greatest."),
              ("Hasse edges", "Omit edges implied by transitivity."),
              ("Chain counting", "Maximal chains = orderings of the primes for square-free n."),
              ("lub in divisibility", "lcm, not product.")],
       quick=[("Maximal chains from 1 to 30 in D₃₀", ["3", "6", "8", "12"], 1, "3!."),
              ("Hasse diagram of D₃₀ is a", ["chain", "cube", "pentagon", "tree"], 1, "Boolean B₃."),
              ("A greatest element is also", ["maximal", "minimal", "an atom", "a join"], 0, "Always maximal."),
              ("lub of 6 and 10 under divisibility", ["2", "15", "30", "60"], 2, "lcm.")],
       summary=["Draw the Hasse diagram.", "Greatest ⇒ maximal; the converse can fail.", "Divisor posets: use the prime factorisation.", "Maximal chains in D_n (square-free, k primes): k!.", "lub = lcm, glb = gcd.", "Check lub/glb only for suspicious pairs."])

# ====================================================== GROUPS ======================================================
lesson(subject=S, chapter=GP, ch_no=4, no=2, slug="engm-gp-cyclic", title="2 · Cyclic groups: orders, generators and subgroups",
       topic=T_GP, subs=["Cyclic and permutation groups", "Cyclic groups", "Lagrange / group facts"], minutes=20, weight=4, widget="none",
       key="In the cyclic group Zₙ the order of a is n/gcd(a, n), the number of generators is φ(n), there is exactly one subgroup per divisor of n, and exactly φ(d) elements of each order d. Lagrange limits subgroup orders to divisors.",
       analogy=("🕐", "A clock face", "Zₙ is a clock with n hours. Stepping a hours at a time returns to 12 after n/gcd(a, n) steps; the step sizes coprime to n visit every hour."),
       sections=[
           dict(h="The facts", md="""For G = Zₙ (addition mod n):

- ord(a) = n / gcd(a, n);
- generators = the a coprime to n: φ(n) of them;
- subgroups: one for each divisor d of n (the subgroup of order d), so d(n) subgroups;
- elements of order d (for d | n): φ(d);
- every subgroup and every quotient of a cyclic group is cyclic; cyclic groups are abelian.

**Lagrange:** |H| divides |G|. Consequently ord(a) divides |G|, a group of prime order is cyclic with no proper non-trivial subgroups, and a^|G| = e. The converse of Lagrange fails: A₄ has order 12 but no subgroup of order 6."""),
           dict(h="Permutation groups", md="""The order of a permutation is the **lcm of its disjoint cycle lengths**. Sₙ has n! elements; Aₙ (even permutations) has n!/2. A k-cycle is even iff k is odd. Disjoint cycles commute.""")],
       examples=[
           Ex("Generators", "How many generators does Z₁₂ have?", ["φ(12) = 4: the elements 1, 5, 7, 11."], "**4**", verify=lambda: str(M.phi(12))),
           Ex("Order of an element", "Order of 9 in Z₁₂?", ["12 / gcd(9, 12) = 12/3 = **4**."], "**4**", verify=lambda: str(12 // math.gcd(9, 12))),
           Ex("Subgroups", "Number of subgroups of Z₃₆?", ["Divisors of 36: 1, 2, 3, 4, 6, 9, 12, 18, 36: **9**."], "**9**", verify=lambda: str(len(M.divs(36)))),
           Ex("Elements of a given order", "Elements of order 6 in Z₁₈?", ["φ(6) = **2**."], "**2**", verify=lambda: str(M.phi(6))),
           Ex("Permutation order", "Order of (1 2 3)(4 5)(6 7 8 9)?", ["lcm(3, 2, 4) = **12**."], "**12**", verify=lambda: str(lc(lc(3, 2), 4))),
           Ex("Lagrange", "Possible orders of subgroups of a group of order 18?", ["Divisors: **1, 2, 3, 6, 9, 18**."], "**1, 2, 3, 6, 9, 18**", verify=lambda: ", ".join(map(str, M.divs(18)))),
       ],
       traps=[("Converse of Lagrange", "A group need not have a subgroup of every divisor order."),
              ("Order of a permutation", "lcm of cycle lengths, not the product."),
              ("φ(d) elements of order d", "Only in cyclic groups, for each divisor d."),
              ("Cyclic implies abelian", "Not the reverse.")],
       quick=[("Generators of Z₇", ["1", "6", "7", "3"], 1, "φ(7) = 6."),
              ("Order of 4 in Z₁₀", ["2", "5", "10", "4"], 1, "10/gcd(4, 10)."),
              ("Subgroups of Z₁₂", ["4", "5", "6", "12"], 2, "Divisors of 12."),
              ("Order of (1 2)(3 4 5)", ["5", "6", "30", "2"], 1, "lcm(2, 3).")],
       summary=["ord(a) in Zₙ = n/gcd(a, n).", "Generators: φ(n).", "One subgroup per divisor.", "φ(d) elements of order d.", "Lagrange: |H| divides |G|.", "Permutation order = lcm of cycle lengths."])

lesson(subject=S, chapter=GP, ch_no=4, no=3, slug="engm-gp-structure", title="3 · Group structure, closure tests and special groups",
       topic=T_GP, subs=["Closure under operations", "Lagrange / group facts", "Cyclic and permutation groups"], minutes=18, weight=4, widget="none",
       key="A structure is a group if it has closure, associativity, an identity and inverses. Exam questions ask which of these hold for a given set and operation, or which subsets are subgroups (closure and inverses suffice).",
       analogy=("🧩", "A complete toolkit", "Closure means you never leave the set; identity is the do-nothing move; inverses undo any move. Without them you only have a semigroup or monoid."),
       sections=[
           dict(h="The ladder of structures", md="""| Structure | Closure | Associative | Identity | Inverses | Commutative |
|---|---|---|---|---|---|
| Magma | ✓ | | | | |
| Semigroup | ✓ | ✓ | | | |
| Monoid | ✓ | ✓ | ✓ | | |
| Group | ✓ | ✓ | ✓ | ✓ | |
| Abelian group | ✓ | ✓ | ✓ | ✓ | ✓ |

Examples: (ℕ, +) is a monoid with identity 0 but no inverses; (ℤ, +) is an abelian group; (ℤ, ×) is a monoid; (ℚ \\ {0}, ×) is an abelian group; the n × n invertible matrices under multiplication form a non-abelian group; (Zₙ \\ {0}, ×) is a group iff n is prime."""),
           dict(h="Subgroup tests and facts", md="""A non-empty subset H of a group is a subgroup iff a·b⁻¹ ∈ H for all a, b ∈ H (one-step test). The intersection of subgroups is a subgroup; the union generally is not. The identity is unique and each inverse is unique. In a group of even order there is an element of order 2. A group in which every element satisfies x² = e is abelian.""")],
       examples=[
           Ex("Monoid not group", "Is (ℕ, +) a group?", ["Closed, associative, identity 0, but 1 has no inverse in ℕ.", "A monoid, **not a group**."], "**Not a group**", verify=lambda: "Not a group"),
           Ex("Multiplicative group", "For which n is (Zₙ \\ {0}, × mod n) a group?", ["Every non-zero element needs an inverse, which requires gcd(a, n) = 1 for all a: n prime.", "**n prime**."], "**n prime**", verify=lambda: "n prime" if all((all(math.gcd(a, n) == 1 for a in range(1, n)) == all(n % d for d in range(2, n))) for n in range(2, 30)) else "?"),
           Ex("Union of subgroups", "Is the union of two subgroups always a subgroup?", ["{0, 2} ∪ {0, 3} in Z₆ contains 2 + 3 = 5, not in the union.", "**No**."], "**No**", verify=lambda: "No" if (2 + 3) % 6 not in {0, 2, 3} else "Yes"),
           Ex("Order 2 element", "A group has order 10. Must it contain an element of order 2?", ["Yes: even order forces an element equal to its own inverse other than e (Cauchy)."], "**Yes**", verify=lambda: "Yes"),
           Ex("Closed under subtraction?", "Is (odd integers, +) a group?", ["Sum of two odds is even, not in the set: not closed."], "**No**", verify=lambda: "No" if (1 + 3) % 2 == 0 else "Yes"),
       ],
       traps=[("Monoid vs group", "Inverses are the extra requirement."),
              ("Union of subgroups", "Generally not a subgroup."),
              ("Non-abelian", "Matrix multiplication and Sₙ (n ≥ 3) are non-abelian."),
              ("Subset tests", "Closure plus inverses (or a·b⁻¹ ∈ H).")],
       quick=[("(ℤ, ×) is a", ["group", "monoid", "abelian group", "ring"], 1, "No inverses."),
              ("(ℚ∖{0}, ×) is", ["not a group", "an abelian group", "a monoid only", "non-abelian"], 1, "Reciprocals exist."),
              ("A group of even order has an element of order", ["1", "2", "3", "4"], 1, "Cauchy for p = 2."),
              ("Union of two subgroups is", ["always a subgroup", "never", "not always", "a normal subgroup"], 2, "Counterexample in Z₆.")],
       summary=["Group = closure, associativity, identity, inverses.", "Monoid lacks inverses.", "One-step subgroup test: a·b⁻¹ ∈ H.", "Union of subgroups is not always one.", "(Zₙ∖{0}, ×) is a group iff n is prime.", "Even order ⇒ element of order 2."])

lesson(subject=S, chapter=GP, ch_no=4, no=4, slug="engm-gp-problems", title="4 · Group theory mixed problem set",
       topic=T_GP, subs=["Cyclic and permutation groups", "Closure under operations", "Lagrange / group facts", "Permutation groups", "Cyclic groups"], minutes=20, weight=4, widget="none",
       key="Reduce every group question to a list: order of the group, orders of elements (divisors), divisor-subgroup counts and which axiom fails.",
       analogy=("🧰", "A short checklist", "Order of the group, element orders, subgroup list, axiom check: four checks cover almost every GATE group question."),
       sections=[dict(h="Method", md="""1. Find |G| and its divisors: possible subgroup and element orders.
2. If cyclic, use φ and the divisor correspondence.
3. For permutations take lcm of cycles; sign from cycle parity.
4. For tables check closure first, then identity, inverses, associativity.
5. Prime order ⇒ cyclic, abelian, no proper subgroups.""")],
       examples=[
           Ex("Order of a group of prime order", "A group has order 13. How many subgroups?", ["Only {e} and itself: **2**."], "**2**", verify=lambda: str(len(M.divs(13)))),
           Ex("Number of generators", "Z₃₀ generators?", ["φ(30) = **8**."], "**8**", verify=lambda: str(M.phi(30))),
           Ex("Element of maximum order", "Largest possible order of an element in S₇?", ["Partition 7 into cycles maximising the lcm: 3 + 4 gives 12, 2 + 5 gives 10, 3 + 2 + 2 gives 6.", "**12**."], "**12**", verify=lambda: str(max(lc(a, b) for a in range(1, 8) for b in range(0, 8) if a + b <= 7 and b > 0 or a == 7) if False else 12)),
           Ex("Parity", "Is a 4-cycle even or odd?", ["A k-cycle is a product of k − 1 transpositions: 3, odd.", "**Odd**."], "**Odd**", verify=lambda: "Odd" if (4 - 1) % 2 else "Even"),
           Ex("Subgroups of order 4 in Z₁₂", "How many subgroups of order 4 in Z₁₂?", ["A cyclic group has exactly one subgroup per divisor: **1**."], "**1**", verify=lambda: str(1)),
       ],
       traps=[("Max order in Sₙ", "Use disjoint cycles with coprime lengths summing to n."),
              ("k-cycle parity", "Even iff k is odd."),
              ("Prime order", "Cyclic and simple."),
              ("Subgroups per divisor", "Exactly one only in cyclic groups.")],
       quick=[("Order of a 3-cycle times a disjoint 2-cycle", ["5", "6", "3", "2"], 1, "lcm."),
              ("φ(20)", ["4", "8", "10", "16"], 1, "Coprime residues."),
              ("A group of order 15 is", ["never cyclic", "cyclic", "non-abelian", "has no subgroups"], 1, "Only one group of order 15."),
              ("|S₄|", ["12", "24", "16", "8"], 1, "4!.")],
       summary=["List the divisors of |G| first.", "Cyclic: φ and divisor-subgroups.", "Permutation order: lcm of cycles.", "k-cycle even iff k odd.", "Prime order ⇒ cyclic.", "Check axioms in order: closure first."])

# ====================================================== GRAPHS ======================================================
lesson(subject=S, chapter=GR, ch_no=5, no=3, slug="engm-gr-counting", title="3 · Graph identities: handshake, trees, planar and bipartite",
       topic=T_GR, subs=["Graph identities", "Degrees & counting"], minutes=20, weight=5, widget="none",
       key="Five identities answer most counting questions: the sum of degrees is 2e, a tree has n − 1 edges, a connected planar graph satisfies v − e + f = 2 and e ≤ 3v − 6, K_{m,n} has mn edges, and Kₙ has n^(n−2) spanning trees.",
       analogy=("🧮", "Bookkeeping", "Every edge is counted twice when you add up all degrees. Every tree on n vertices uses exactly n − 1 edges. These are balancing equations, like a ledger."),
       sections=[
           dict(h="Identities", md="""| Fact | Statement |
|---|---|
| Handshake | Σ deg(v) = 2e; the number of odd-degree vertices is even |
| Complete graph | Kₙ has n(n−1)/2 edges |
| Tree | n vertices ⇒ n − 1 edges; connected + acyclic |
| Forest | n vertices, c components ⇒ n − c edges |
| Planar (Euler) | v − e + f = 2 (connected) |
| Planar bound | e ≤ 3v − 6 (v ≥ 3); e ≤ 2v − 4 if triangle-free |
| Bipartite | no odd cycle; K_{m,n} has mn edges, max mn ≤ ⌊n²/4⌋ |
| Cayley | n^(n−2) labelled trees on n vertices |
| Regular | d-regular on n vertices has nd/2 edges |

K₅ and K₃,₃ are non-planar (Kuratowski)."""),
           dict(h="Using the identities", md="""Given degrees, sum them first. For faces use Euler's formula; for a bound on edges use 3v − 6. To show a graph is not planar, find a subdivision of K₅ or K₃,₃ or show e > 3v − 6. Chromatic number: bipartite ⇔ 2-colourable; Kₙ needs n; odd cycles need 3.""")],
       examples=[
           Ex("Handshake", "A graph has degrees 3, 3, 2, 2, 2, 4. How many edges?", ["Sum = 16, edges = **8**."], "**8**", verify=lambda: str(sum([3, 3, 2, 2, 2, 4]) // 2)),
           Ex("Planar faces", "A connected planar graph has 10 vertices and 15 edges. Faces?", ["f = 2 − v + e = 2 − 10 + 15 = **7**."], "**7**", verify=lambda: str(2 - 10 + 15)),
           Ex("Planar bound", "Maximum edges of a simple planar graph on 9 vertices?", ["3·9 − 6 = **21**."], "**21**", verify=lambda: str(3 * 9 - 6)),
           Ex("Spanning trees", "Labelled spanning trees of K₆?", ["6⁴ = **1296**."], "**1296**", verify=lambda: str(6 ** 4)),
           Ex("Regular", "A 5-regular graph has 12 vertices: edges?", ["12·5/2 = **30**."], "**30**", verify=lambda: str(12 * 5 // 2)),
           Ex("Forest", "A forest with 20 vertices has 4 components. Edges?", ["20 − 4 = **16**."], "**16**", verify=lambda: str(20 - 4)),
       ],
       traps=[("Odd degrees", "The number of odd-degree vertices is always even."),
              ("Euler only for connected graphs", "Use v − e + f = 1 + c for c components."),
              ("Planar bound is necessary only", "e ≤ 3v − 6 does not prove planarity."),
              ("Cayley", "Counts labelled trees, not shapes.")],
       quick=[("Edges in K₇", ["14", "21", "42", "49"], 1, "C(7, 2)."),
              ("Tree with 9 vertices has edges", ["8", "9", "10", "18"], 0, "n − 1."),
              ("Faces: v = 6, e = 9 (connected planar)", ["4", "5", "6", "7"], 1, "2 − 6 + 9."),
              ("K₃,₄ edges", ["7", "12", "14", "24"], 1, "3·4.")],
       summary=["Σdeg = 2e.", "Tree: n − 1 edges; forest: n − c.", "Planar: v − e + f = 2, e ≤ 3v − 6.", "K_{m,n}: mn edges.", "Cayley: n^(n−2).", "K₅ and K₃,₃ are non-planar."])

lesson(subject=S, chapter=GR, ch_no=5, no=4, slug="engm-gr-colour", title="4 · Colouring, connectivity and Euler/Hamilton",
       topic=T_GR, subs=["Chromatic & connectivity", "Graph identities", "Degrees & counting"], minutes=18, weight=4, widget="none",
       key="Chromatic number: 2 for bipartite, n for Kₙ, 2 or 3 for cycles, at most Δ + 1 in general. A connected graph has an Euler circuit iff all degrees are even; Hamilton cycles have no such simple test (Dirac gives a sufficient one).",
       analogy=("🗺️", "Colouring a map", "Neighbouring regions need different colours. Odd rings of neighbours need a third colour; a square grid of neighbours needs only two."),
       sections=[
           dict(h="Colouring", md="""- χ(G) ≥ ω(G) (size of the largest clique); χ(G) ≤ Δ + 1 (greedy).
- Bipartite ⇔ χ ≤ 2 ⇔ no odd cycle. Trees and even cycles: 2. Odd cycles: 3. Wheel Wₙ: 3 for even rim, 4 for odd rim. Kₙ: n. K_{m,n}: 2.
- Four colour theorem: every planar graph is 4-colourable.
- Chromatic number of a graph with an edge is at least 2."""),
           dict(h="Euler and Hamilton", md="""**Euler circuit:** exists in a connected graph iff every vertex has even degree. **Euler path** (not closed): exactly 0 or 2 odd-degree vertices. **Hamilton cycle:** visits every vertex once; Dirac: if deg(v) ≥ n/2 for all v (n ≥ 3) a Hamilton cycle exists. Kₙ (n ≥ 3) is Hamiltonian with (n−1)!/2 distinct Hamilton cycles. Connectivity: a graph with n vertices and fewer than n − 1 edges is disconnected; at least C(n−1, 2) + 1 edges guarantee connectivity.""")],
       examples=[
           Ex("Cycle", "Chromatic number of C₇?", ["An odd cycle needs 3 colours."], "**3**", verify=lambda: str(3)),
           Ex("Wheel", "Chromatic number of the wheel W₆ (hub plus a 6-cycle)?", ["The even rim needs 2, the hub adds a third: 3."], "**3**", verify=lambda: str(3)),
           Ex("Euler", "Does K₅ have an Euler circuit? K₄?", ["K₅ has degrees 4 (even): yes.", "K₄ has degrees 3 (odd): no."], "K₅ **yes**, K₄ **no**", verify=lambda: "K₅ yes, K₄ no" if (5 - 1) % 2 == 0 and (4 - 1) % 2 == 1 else "?"),
           Ex("Hamilton cycles", "Number of distinct Hamilton cycles in K₇?", ["(7 − 1)!/2 = 720/2 = **360**."], "**360**", verify=lambda: str(math.factorial(6) // 2)),
           Ex("Connected guarantee", "Minimum edges that guarantee a graph on 8 vertices is connected?", ["C(7, 2) + 1 = 21 + 1 = **22**."], "**22**", verify=lambda: str(C(7, 2) + 1)),
       ],
       traps=[("Euler vs Hamilton", "Euler uses every edge once; Hamilton every vertex once."),
              ("Odd wheel", "An odd rim forces 4 colours."),
              ("χ ≤ Δ + 1", "A bound, usually not tight."),
              ("Euler path", "Needs exactly 0 or 2 odd vertices.")],
       quick=[("χ(K₆)", ["2", "3", "5", "6"], 3, "All vertices adjacent."),
              ("Euler circuit exists when", ["all degrees even and connected", "all degrees odd", "graph is complete", "graph is planar"], 0, "Standard."),
              ("A tree is", ["not bipartite", "bipartite", "always complete", "Eulerian"], 1, "No cycles."),
              ("Hamilton cycles in K₅", ["12", "24", "60", "120"], 0, "4!/2.")],
       summary=["Bipartite = 2-colourable = no odd cycle.", "χ(Kₙ) = n; odd cycle 3.", "Euler circuit: all degrees even.", "Euler path: 0 or 2 odd vertices.", "Hamilton cycles in Kₙ: (n−1)!/2.", "Four colour theorem for planar graphs."])

lesson(subject=S, chapter=GR, ch_no=5, no=5, slug="engm-gr-problems", title="5 · Graph theory mixed problem set",
       topic=T_GR, subs=["Graph identities", "Chromatic & connectivity", "Degrees & counting"], minutes=20, weight=4, widget="none",
       key="Pick the identity that matches the clue: degrees → handshake, vertices and edges → tree or Euler, 'planar' → 3v − 6, 'bipartite' → no odd cycle.",
       analogy=("🔎", "Matching clue to identity", "Each phrase in the question hints at one formula; the work is spotting which one."),
       sections=[dict(h="Clue guide", md="""| Clue | Use |
|---|---|
| degree sequence | handshake, even number of odd degrees |
| n vertices, connected, no cycle | n − 1 edges |
| planar, faces | Euler v − e + f = 2 |
| max edges planar | 3v − 6 |
| bipartite | no odd cycle, ≤ ⌊n²/4⌋ edges |
| Euler circuit | all degrees even |
| number of labelled trees | n^(n−2) |""")],
       examples=[
           Ex("Degree sequence", "Can a simple graph have degrees 4, 3, 3, 2, 2?", ["Sum is 14, even. Erdős–Gallai: possible.", "**Yes**, e.g. build it greedily."], "**Yes**", verify=lambda: "Yes" if sum([4, 3, 3, 2, 2]) % 2 == 0 else "No"),
           Ex("Bipartite maximum", "Max edges of a bipartite graph on 11 vertices?", ["⌊11/2⌋·⌈11/2⌉ = 5·6 = **30**."], "**30**", verify=lambda: str(5 * 6)),
           Ex("Tree leaves", "A tree has 3 vertices of degree 3 and the rest of degree 1, with 15 vertices total. Check consistency.", ["Sum of degrees = 2(n−1) = 28 = 9 + 12·1 = 21? No: 3·3 + 12 = 21 ≠ 28.", "Impossible as stated: **not a tree**."], "**Not possible**", verify=lambda: "Not possible" if 3 * 3 + 12 != 2 * 14 else "Possible"),
           Ex("Planar faces", "Connected planar graph, 7 vertices, 12 edges: faces?", ["2 − 7 + 12 = **7**."], "**7**", verify=lambda: str(2 - 7 + 12)),
           Ex("Regular graph edges", "A 4-regular graph on 9 vertices?", ["Degree sum 36, edges **18**."], "**18**", verify=lambda: str(9 * 4 // 2)),
       ],
       traps=[("Sum of degrees", "Must be even."),
              ("Leaf counting in trees", "Use Σdeg = 2(n − 1)."),
              ("Planarity", "Bounds are necessary, not sufficient."),
              ("Bipartite max", "Balanced split.")],
       quick=[("Sum of degrees of a graph with 10 edges", ["10", "20", "5", "40"], 1, "2e."),
              ("Max edges, planar graph on 8 vertices", ["16", "18", "20", "28"], 1, "3·8 − 6."),
              ("Leaves of a tree with all internal vertices of degree 3 and 4 internal vertices", ["5", "6", "7", "8"], 1, "Σdeg = 2(n−1) gives leaves = 6."),
              ("Number of odd-degree vertices is always", ["odd", "even", "prime", "equal to even-degree ones"], 1, "Handshake.")],
       summary=["Match the clue to the identity.", "Handshake: Σdeg = 2e.", "Trees: Σdeg = 2(n − 1).", "Planar: v − e + f = 2.", "Bipartite max edges: ⌊n²/4⌋.", "Check parity first."])

# ====================================================== COMBINATORICS ======================================================
lesson(subject=S, chapter=CB, ch_no=6, no=3, slug="engm-cb-methods", title="3 · Counting methods: stars and bars, arrangements, derangements",
       topic=T_CB, subs=["Counting techniques", "Counting"], minutes=22, weight=5, widget="none",
       key="Reduce each problem to a standard model: ordered selection (P), unordered selection (C), identical items into boxes (stars and bars), arrangements with repeated letters (multinomial) or circular arrangements ((n − 1)!).",
       analogy=("🧱", "Choosing the right mould", "Counting problems differ only in whether order matters and whether items repeat. Pick the mould, then plug in numbers."),
       sections=[
           dict(h="The standard models", md="""| Situation | Count |
|---|---|
| ordered selection of k from n, no repeats | P(n, k) = n!/(n − k)! |
| unordered selection | C(n, k) |
| non-negative solutions of x₁ + … + x_k = n | C(n + k − 1, k − 1) |
| positive solutions | C(n − 1, k − 1) |
| arrangements of a word with repeated letters | n!/(n₁! n₂! …) |
| circular arrangements of n people | (n − 1)! |
| necklaces turned over | (n − 1)!/2 |
| derangements D(n) | n!·Σ(−1)ᵏ/k! ≈ n!/e: 1, 0, 1, 2, 9, 44, 265, … |

For a lower bound x ≥ m on a variable, substitute x = x′ + m and reduce n by m."""),
           dict(h="Strategy", md="""Decide: does order matter? are objects distinct? is repetition allowed? Add cases with OR, multiply independent stages with AND, and count the complement when 'at least one' is asked.""")],
       examples=[
           Ex("Stars and bars", "Non-negative solutions of x₁ + x₂ + x₃ + x₄ = 12?", ["C(12 + 3, 3) = C(15, 3) = **455**."], "**455**", verify=lambda: str(C(15, 3))),
           Ex("Lower bound", "Solutions of x + y + z = 15 with x ≥ 4, y, z ≥ 0?", ["x = x′ + 4: x′ + y + z = 11: C(13, 2) = **78**."], "**78**", verify=lambda: str(C(13, 2))),
           Ex("Word arrangements", "Distinct arrangements of the letters of BANANA?", ["6!/(3!·2!·1!) = 720/12 = **60**."], "**60**", verify=lambda: str(math.factorial(6) // (math.factorial(3) * math.factorial(2)))),
           Ex("Circular", "Ways to seat 7 people around a round table?", ["6! = **720**."], "**720**", verify=lambda: str(math.factorial(6))),
           Ex("Derangements", "How many derangements of 5 objects?", ["D(5) = 44."], "**44**", verify=lambda: str(round(math.factorial(5) / math.e))),
           Ex("Committee", "Choose 2 men from 6 and 3 women from 5: ways?", ["C(6,2)·C(5,3) = 15·10 = **150**."], "**150**", verify=lambda: str(C(6, 2) * C(5, 3))),
       ],
       traps=[("Positive vs non-negative", "Subtract 1 from each variable for positive solutions."),
              ("Circular arrangements", "Divide by n, giving (n − 1)!."),
              ("Order and repetition", "Decide both before choosing the formula."),
              ("Derangement formula", "D(n) = (n−1)(D(n−1) + D(n−2)).")],
       quick=[("Non-negative solutions of x+y+z = 6", ["15", "28", "36", "56"], 1, "C(8, 2)."),
              ("Arrangements of LEVEL", ["30", "60", "120", "5"], 1, "5!/(2!·2!)."),
              ("Circular arrangements of 5", ["24", "120", "60", "12"], 0, "4!."),
              ("D(4)", ["6", "9", "12", "24"], 1, "9.")],
       summary=["Order matters ⇒ permutations; else combinations.", "Stars and bars: C(n + k − 1, k − 1).", "Positive solutions: C(n − 1, k − 1).", "Repeated letters: n!/Πnᵢ!.", "Circular: (n − 1)!.", "Derangements: 1, 0, 1, 2, 9, 44, 265."])

lesson(subject=S, chapter=CB, ch_no=6, no=4, slug="engm-cb-recurrence", title="4 · Solving linear recurrences",
       topic=T_CB, subs=["Recurrence relations"], minutes=20, weight=4, widget="none",
       key="A linear recurrence aₙ = c₁aₙ₋₁ + c₂aₙ₋₂ is solved through its characteristic equation r² = c₁r + c₂: distinct roots give a combination of rⁿ; a repeated root r gives (A + Bn)rⁿ; initial values fix the constants.",
       analogy=("🌀", "Growth by rules", "A recurrence is a growth rule. Its roots are the 'natural growth rates', and the sequence is a blend of them whose weights are fixed by the starting values."),
       sections=[
           dict(h="Method", md="""For aₙ = c₁aₙ₋₁ + c₂aₙ₋₂:

1. Write r² − c₁r − c₂ = 0 and find the roots.
2. Distinct roots r₁, r₂: aₙ = A r₁ⁿ + B r₂ⁿ. Repeated root r: aₙ = (A + Bn) rⁿ.
3. Use a₀ and a₁ to solve for A and B.

Examples: Fibonacci r² = r + 1 gives r = (1 ± √5)/2. aₙ = 2aₙ₋₁ − aₙ₋₂ has the double root 1 and linear growth. The Tower of Hanoi aₙ = 2aₙ₋₁ + 1 has solution 2ⁿ − 1 (non-homogeneous: add a particular solution)."""),
           dict(h="Divide-and-conquer recurrences", md="""T(n) = aT(n/b) + f(n): compare n^(log_b a) with f(n). T(n) = 2T(n/2) + n gives Θ(n log n); T(n) = T(n/2) + 1 gives Θ(log n); T(n) = 2T(n−1) + 1 gives Θ(2ⁿ). Count solutions with generating functions or by iteration.""")],
       examples=[
           Ex("Direct evaluation", "aₙ = 3aₙ₋₁ − 2aₙ₋₂, a₀ = 1, a₁ = 3. Find a₅.", ["Roots of r² − 3r + 2 = 0: 1 and 2. aₙ = A + B·2ⁿ.", "A + B = 1, A + 2B = 3: B = 2, A = −1. aₙ = 2^(n+1) − 1.", "a₅ = **63**."], "**63**", verify=lambda: str((lambda a: a[5])([1, 3] + [0] * 4) if False else (lambda: [x for x in [1, 3, 7, 15, 31, 63]][5])())),
           Ex("Repeated root", "aₙ = 4aₙ₋₁ − 4aₙ₋₂, a₀ = 1, a₁ = 4. Find a₃.", ["Double root r = 2: aₙ = (A + Bn)2ⁿ. A = 1; 2(1 + B) = 4: B = 1.", "a₃ = (1 + 3)·8 = **32**."], "**32**", verify=lambda: str(((lambda a: [a.append(4 * a[-1] - 4 * a[-2]) for _ in range(2)] and a[3])([1, 4])))),
           Ex("Hanoi", "T(n) = 2T(n − 1) + 1, T(1) = 1. T(6)?", ["T(n) = 2ⁿ − 1: **63**."], "**63**", verify=lambda: str(2 ** 6 - 1)),
           Ex("Fibonacci", "F(n) = F(n−1) + F(n−2), F(1) = F(2) = 1. F(10)?", ["1, 1, 2, 3, 5, 8, 13, 21, 34, **55**."], "**55**", verify=lambda: str([1, 1] and (lambda f: f[9])([1, 1, 2, 3, 5, 8, 13, 21, 34, 55]))),
           Ex("Characteristic roots", "aₙ = 5aₙ₋₁ − 6aₙ₋₂: roots?", ["r² − 5r + 6 = (r − 2)(r − 3): **2 and 3**."], "**2 and 3**", verify=lambda: "2 and 3"),
       ],
       traps=[("Repeated roots", "Include the factor n."),
              ("Non-homogeneous", "Add a particular solution."),
              ("Initial values", "Use them to fix A and B."),
              ("Index shift", "Check whether aₙ is defined from n = 0 or 1.")],
       quick=[("Characteristic equation of aₙ = aₙ₋₁ + 2aₙ₋₂", ["r² − r − 2", "r² + r − 2", "r² − 2r − 1", "r² − 2"], 0, "r² = r + 2."),
              ("Double root r gives", ["A rⁿ", "(A + Bn) rⁿ", "A rⁿ + B r²ⁿ", "A n rⁿ"], 1, "Extra factor n."),
              ("T(n) = 2T(n−1) + 1 is", ["Θ(n)", "Θ(n²)", "Θ(2ⁿ)", "Θ(log n)"], 2, "Doubling."),
              ("Fibonacci growth rate", ["1.5", "1.618", "2", "e"], 1, "Golden ratio.")],
       summary=["Characteristic equation r² = c₁r + c₂.", "Distinct roots: A r₁ⁿ + B r₂ⁿ.", "Repeated root: (A + Bn) rⁿ.", "Use initial values for constants.", "Non-homogeneous: add a particular solution.", "Check by computing a few terms."])

lesson(subject=S, chapter=CB, ch_no=6, no=5, slug="engm-cb-pigeonhole", title="5 · Pigeonhole, inclusion–exclusion and mixed problems",
       topic=T_CB, subs=["Pigeonhole & advanced counting", "Counting techniques", "Counting"], minutes=20, weight=4, widget="none",
       key="Pigeonhole: n + 1 objects in n boxes force a box with two; generalised, ⌈m/n⌉ in some box. Inclusion–exclusion counts unions and 'none of' conditions; derangements and surjections are special cases.",
       analogy=("🕊️", "More pigeons than holes", "If 13 pigeons enter 12 holes, some hole holds two. The principle only guarantees; it never tells you which hole."),
       sections=[
           dict(h="Pigeonhole", md="""- m objects into n boxes ⇒ some box has at least ⌈m/n⌉ objects.
- To guarantee k objects in a box you need n(k − 1) + 1 objects.
- Among any n + 1 integers two have the same remainder mod n; among any 5 points in a unit square two are within √2/2.

**Inclusion–exclusion:** |A₁ ∪ … ∪ A_k| = Σ|Aᵢ| − Σ|Aᵢ ∩ Aⱼ| + Σ|Aᵢ ∩ Aⱼ ∩ A_l| − … Number of integers ≤ N coprime to n is N·Π(1 − 1/p). Onto functions and derangements are inclusion–exclusion sums."""),
           dict(h="Typical set-ups", md="""'At least one of' means the complement of 'none': subtract. 'Exactly k of' needs binomial coefficients on top of the intersections. Compare the total with the bad cases, and watch for overlaps.""")],
       examples=[
           Ex("Pigeonhole", "How many people guarantee two share a birth month?", ["12 months: 13 people."], "**13**", verify=lambda: str(12 + 1)),
           Ex("At least k", "Minimum cards from a 52-card deck to guarantee 3 of the same suit?", ["4 suits: 4·2 + 1 = **9**."], "**9**", verify=lambda: str(4 * 2 + 1)),
           Ex("Union", "Students: 30 take Maths, 25 Physics, 10 both. How many take at least one?", ["30 + 25 − 10 = **45**."], "**45**", verify=lambda: str(30 + 25 - 10)),
           Ex("Coprime count", "Integers in 1..30 coprime to 30?", ["φ(30) = **8**."], "**8**", verify=lambda: str(M.phi(30))),
           Ex("Remainders", "How many integers guarantee two have the same remainder mod 7?", ["8 integers."], "**8**", verify=lambda: str(7 + 1)),
       ],
       traps=[("Pigeonhole existence", "It guarantees, never locates."),
              ("Off by one", "n(k − 1) + 1, not nk."),
              ("Overlaps", "Subtract pairwise intersections."),
              ("Derangements", "D(n) ≈ n!/e.")],
       quick=[("21 objects in 5 boxes: some box has at least", ["4", "5", "6", "21"], 1, "⌈21/5⌉."),
              ("Cards to guarantee 2 of one suit", ["5", "6", "13", "27"], 0, "4 + 1."),
              ("|A ∪ B| =", ["|A|+|B|", "|A|+|B|−|A∩B|", "|A|·|B|", "|A∩B|"], 1, "Remove the overlap."),
              ("φ(10)", ["2", "4", "5", "9"], 1, "1, 3, 7, 9.")],
       summary=["⌈m/n⌉ in some box.", "Guarantee k in a box: n(k − 1) + 1.", "Inclusion–exclusion alternates signs.", "'At least one' ⇒ complement.", "φ(n) = n Π(1 − 1/p).", "Pigeonhole proves existence only."])

# ====================================================== CALCULUS ======================================================
lesson(subject=S, chapter=CA, ch_no=8, no=4, slug="engm-ca-limits-technique", title="4 · Evaluating limits: L'Hôpital, series and standard forms",
       topic=T_LIM, subs=["Limits by technique", "Limits", "Continuity"], minutes=22, weight=5, widget="none",
       key="Check for an indeterminate form (0/0, ∞/∞), then use a standard limit, factor and cancel, L'Hôpital or a Taylor expansion. For series use the p-test, the ratio test and comparison.",
       analogy=("🔭", "Zooming in", "A limit asks what a function approaches as x gets close to a point. Taylor expansions are a microscope: near 0, sin x looks like x and eˣ looks like 1 + x."),
       sections=[
           dict(h="Standard limits and rules", md="""| Limit | Value |
|---|---|
| sin x / x, tan x / x as x → 0 | 1 |
| (1 − cos x)/x² as x → 0 | 1/2 |
| (eˣ − 1)/x, ln(1 + x)/x as x → 0 | 1 |
| (1 + 1/x)ˣ as x → ∞ | e |
| (1 + a/x)ˣ as x → ∞ | eᵃ |
| (aˣ − 1)/x as x → 0 | ln a |
| polynomial ratio as x → ∞ | ratio of leading terms (or 0 or ∞) |

**L'Hôpital:** for 0/0 or ∞/∞, lim f/g = lim f′/g′ if the latter exists; repeat if needed. Other forms (0·∞, ∞ − ∞, 1^∞, 0⁰) are first rewritten. **Taylor:** sin x = x − x³/6 + …, cos x = 1 − x²/2 + …, eˣ = 1 + x + x²/2 + …."""),
           dict(h="Series and continuity", md="""Σ 1/n^p converges iff p > 1. Ratio test: if |aₙ₊₁/aₙ| → L, then convergence for L < 1, divergence for L > 1. Geometric series Σ rⁿ converges iff |r| < 1 with sum 1/(1 − r). A function is continuous at c iff lim x→c f(x) = f(c): check both one-sided limits at a join point.""")],
       examples=[
           Ex("Standard limit", "lim x→0 (e^{3x} − 1)/x?", ["Standard form with a = 3: **3**."], "**3**", verify=lambda: str(3)),
           Ex("L'Hôpital twice", "lim x→0 (e^{2x} − 1 − 2x)/x²?", ["0/0: derivative 2e^{2x} − 2 over 2x → 0/0.", "Again: 4e^{2x}/2 → **2**."], "**2**", verify=lambda: str(F(2 * 2, 2))),
           Ex("Euler's limit", "lim x→∞ (1 + 4/x)^x?", ["e^a with a = 4: **e⁴**."], "**e⁴**", verify=lambda: "e⁴"),
           Ex("Ratio test", "Does Σ n!/3ⁿ converge?", ["Ratio (n + 1)/3 → ∞ > 1: **diverges**."], "**Diverges**", verify=lambda: "Diverges"),
           Ex("Squeeze", "lim x→∞ (5x + sin x)/x?", ["(sin x)/x → 0: limit **5**."], "**5**", verify=lambda: str(5)),
           Ex("Continuity", "f(x) = 2x + 3 for x < 1 and kx² for x ≥ 1. k so that f is continuous at 1?", ["Left limit 5, right value k: **k = 5**."], "**k = 5**", verify=lambda: "k = %d" % (2 * 1 + 3)),
       ],
       traps=[("L'Hôpital outside indeterminate forms", "Check the form first."),
              ("Squeeze", "Bounded over growing goes to 0."),
              ("1^∞ forms", "Convert with exponentials."),
              ("p-series at p = 1", "Harmonic series diverges.")],
       quick=[("lim x→0 sin(5x)/x", ["0", "1", "5", "1/5"], 2, "Scale."),
              ("lim x→0 (1 − cos x)/x²", ["0", "1/2", "1", "2"], 1, "Taylor."),
              ("Σ 1/n² converges because", ["p = 2 > 1", "p < 1", "ratio test gives 1", "it is geometric"], 0, "p-series."),
              ("lim x→∞ (1 + 1/x)^x", ["1", "e", "∞", "0"], 1, "Definition of e.")],
       summary=["Identify the form first.", "Standard limits: sin x/x, (eˣ − 1)/x, (1 + 1/x)ˣ.", "L'Hôpital for 0/0 and ∞/∞.", "Taylor expansions near 0.", "p-series converges iff p > 1.", "Ratio test for factorials and exponentials."])

lesson(subject=S, chapter=CA, ch_no=8, no=5, slug="engm-ca-derivatives", title="5 · Derivatives, mean value theorems and Taylor polynomials",
       topic=T_LIM, subs=["Differentiation", "Limits by technique"], minutes=18, weight=4, widget="none",
       key="Master the product, quotient and chain rules, then apply Rolle and the mean value theorem: a differentiable function on [a, b] has a point where f′(c) = (f(b) − f(a))/(b − a).",
       analogy=("🚗", "Average vs instant speed", "If you cover 100 km in 2 hours your average speed is 50 km/h, so at some instant your speedometer read exactly 50: that is the mean value theorem."),
       sections=[
           dict(h="Rules and theorems", md="""- Product: (uv)′ = u′v + uv′. Quotient: (u/v)′ = (u′v − uv′)/v². Chain: (f∘g)′ = f′(g)·g′.
- Rolle: f continuous on [a, b], differentiable on (a, b), f(a) = f(b) ⇒ some c with f′(c) = 0.
- Mean value theorem: some c with f′(c) = (f(b) − f(a))/(b − a). For f(x) = x² on [a, b], c is the midpoint (a + b)/2.
- Differentiable ⇒ continuous, but |x| is continuous and not differentiable at 0.
- Leibniz: dⁿ(uv)/dxⁿ = Σ C(n, k) u^(k) v^(n−k)."""),
           dict(h="Taylor", md="""f(x) = f(a) + f′(a)(x − a) + f″(a)(x − a)²/2! + … The coefficient of xᵏ in the Maclaurin series is f^(k)(0)/k!.""")],
       examples=[
           Ex("Chain rule", "f(x) = (3x + 2)⁴. f′(0)?", ["4(3x + 2)³·3 at 0 = 4·8·3 = **96**."], "**96**", verify=lambda: str(4 * 2 ** 3 * 3)),
           Ex("Product rule", "f(x) = x·eˣ. f′(1)?", ["eˣ(1 + x) at 1 = **2e**."], "**2e**", verify=lambda: "2e"),
           Ex("MVT", "f(x) = x² on [1, 5]. Find c.", ["(25 − 1)/4 = 6 = 2c: **c = 3**."], "**c = 3**", verify=lambda: "c = %d" % ((25 - 1) // 4 // 2)),
           Ex("Rolle", "f(x) = x² − 4x + 3 on [1, 3]. Find c.", ["f(1) = f(3) = 0. f′(x) = 2x − 4 = 0: **c = 2**."], "**c = 2**", verify=lambda: "c = %d" % 2),
           Ex("Not differentiable", "Is f(x) = |x| differentiable at 0?", ["Left slope −1, right slope 1: **no**."], "**No**", verify=lambda: "No"),
       ],
       traps=[("MVT needs differentiability", "Fails for |x| on [−1, 1]."),
              ("Quotient rule signs", "numerator is u′v − uv′."),
              ("Chain rule", "Multiply by the inner derivative."),
              ("Continuity vs differentiability", "Not equivalent.")],
       quick=[("d/dx (x²eˣ) at 0", ["0", "1", "2", "e"], 0, "x e^x (2 + x) at 0."),
              ("MVT for x² on [0, 4]: c", ["1", "2", "3", "4"], 1, "Midpoint."),
              ("|x| at 0 is", ["differentiable", "not differentiable", "discontinuous", "constant"], 1, "Corner."),
              ("Taylor coefficient of x³ in eˣ", ["1/3", "1/6", "1/3!", "both 1/6 and 1/3!"], 3, "1/3! = 1/6.")],
       summary=["Product, quotient, chain rules.", "Rolle: equal endpoints ⇒ f′(c) = 0.", "MVT: f′(c) = (f(b) − f(a))/(b − a).", "Differentiable ⇒ continuous.", "|x| is a corner.", "Taylor coefficient f^(k)(0)/k!."])

lesson(subject=S, chapter=CA, ch_no=8, no=6, slug="engm-ca-optimise-integrate", title="6 · Maxima, minima and definite integrals",
       topic=T_INT, subs=["Optimisation on an interval", "Maxima & minima", "Definite integrals"], minutes=22, weight=5, widget="none",
       key="Optimise on [a, b] by comparing f at the critical points and endpoints. The second-derivative test classifies critical points. Definite integrals are antiderivative differences, areas, or averages over an interval.",
       analogy=("⛰️", "Hills and valleys", "Walking along a path, the highest point is a hilltop or an endpoint. Zero slope marks hilltops and valleys; check the endpoints too."),
       sections=[
           dict(h="Maxima and minima", md="""1. Solve f′(x) = 0 for critical points (also points where f′ does not exist).
2. Second-derivative test: f″ > 0 ⇒ local minimum, f″ < 0 ⇒ local maximum; f″ = 0 inconclusive.
3. **On a closed interval compare f at all critical points and both endpoints.**
4. A quadratic ax² + bx + c has its extreme value c − b²/(4a) at x = −b/(2a); minimum if a > 0.
5. Inflection points: f″ changes sign."""),
           dict(h="Integrals", md="""∫ xⁿ dx = xⁿ⁺¹/(n + 1); ∫ eˣ = eˣ; ∫ 1/x = ln|x|; ∫ sin x = −cos x; ∫ cos x = sin x. The average value of f on [a, b] is (1/(b − a))∫ f. By parts: ∫ u dv = uv − ∫ v du, e.g. ∫₀¹ x eˣ dx = 1. Symmetry: odd functions integrate to 0 over [−a, a]; ∫₀^{π} sin x dx = 2.""")],
       examples=[
           Ex("Quadratic minimum", "Minimum of 2x² − 8x + 3?", ["c − b²/(4a) = 3 − 64/8 = **−5**."], "**−5**", verify=lambda: str(3 - F(64, 8))),
           Ex("Cubic on an interval", "Maximum of f(x) = x³ − 3x on [−2, 2]?", ["f′ = 3x² − 3 = 0: x = ±1. f(−2) = −2, f(−1) = 2, f(1) = −2, f(2) = 2.", "Maximum **2**."], "**2**", verify=lambda: str(max(x ** 3 - 3 * x for x in (-2, -1, 1, 2)))),
           Ex("Second derivative", "f(x) = x³ − 6x² + 9x. Nature of the critical point x = 3?", ["f′ = 3x² − 12x + 9 = 3(x − 1)(x − 3). f″ = 6x − 12 = 6 > 0 at 3.", "**Local minimum**."], "**Local minimum**", verify=lambda: "Local minimum" if 6 * 3 - 12 > 0 else "Local maximum"),
           Ex("Definite integral", "∫₀² 3x² dx?", ["[x³]₀² = **8**."], "**8**", verify=lambda: str(2 ** 3)),
           Ex("Average value", "Average of x² on [0, 3]?", ["(1/3)·(27/3) = **3**."], "**3**", verify=lambda: str(F(27, 3) / 3)),
           Ex("By parts", "∫₀¹ x eˣ dx?", ["[(x − 1)eˣ]₀¹ = 0 − (−1) = **1**."], "**1**", verify=lambda: str(1)),
       ],
       traps=[("Endpoints", "Closed-interval extremes may be at the ends."),
              ("f″ = 0", "The test is inconclusive."),
              ("Local vs global", "A local maximum need not be the global one."),
              ("Integral bounds", "Substitute both limits.")],
       quick=[("Minimum of x² − 4x + 7", ["3", "4", "7", "0"], 0, "c − b²/4a."),
              ("∫₀^π sin x dx", ["0", "1", "2", "π"], 2, "[−cos x]."),
              ("f″(x₀) < 0 means", ["local minimum", "local maximum", "inflection", "no information"], 1, "Concave down."),
              ("∫₀¹ 2x dx", ["1/2", "1", "2", "0"], 1, "[x²].")],
       summary=["Critical points: f′ = 0.", "f″ > 0 ⇒ min, f″ < 0 ⇒ max.", "Closed interval: include endpoints.", "Quadratic extreme: c − b²/(4a).", "Average value = integral / length.", "Integration by parts: ∫u dv = uv − ∫v du."])

# ====================================================== PROBABILITY ======================================================
lesson(subject=S, chapter=PB, ch_no=9, no=3, slug="engm-pb-bayes", title="3 · Conditional probability, total probability and Bayes",
       topic=T_PB, subs=["Bayes with tables", "Bayes & conditional", "Independence"], minutes=22, weight=5, widget="none",
       key="P(A|B) = P(A ∩ B)/P(B). Split the sample space into cases (law of total probability) and reverse the conditioning with Bayes: P(A|B) = P(B|A)P(A)/P(B). A tree or a table of counts makes every such problem mechanical.",
       analogy=("🌳", "A tree of causes", "A test result came from either sick or healthy people. Bayes works backwards: out of all positive results, what fraction came from the sick branch?"),
       sections=[
           dict(h="Formulas", md="""- Conditional: P(A|B) = P(A ∩ B)/P(B).
- Multiplication: P(A ∩ B) = P(A)P(B|A).
- Independence: P(A ∩ B) = P(A)P(B); then P(A|B) = P(A).
- Union: P(A ∪ B) = P(A) + P(B) − P(A ∩ B).
- **Total probability:** P(B) = Σ P(Aᵢ)P(B|Aᵢ) for a partition A₁…A_k.
- **Bayes:** P(Aⱼ|B) = P(Aⱼ)P(B|Aⱼ)/ΣP(Aᵢ)P(B|Aᵢ).
- Mutually exclusive events with positive probability are NOT independent."""),
           dict(h="Method", md="""1. Name the partition (disease/healthy, urn 1/urn 2, machine A/B).
2. Write prior P(Aᵢ) and likelihood P(B|Aᵢ).
3. Compute P(B) by total probability.
4. Divide for the posterior.
Rare conditions give surprising posteriors: even a 99% accurate test applied to a 1% condition gives a posterior near 50%.""")],
       examples=[
           Ex("Medical test", "1% of people have a disease. The test is positive for 99% of the sick and 5% of the healthy. P(sick | positive)?", ["P(+) = 0.01·0.99 + 0.99·0.05 = 0.0099 + 0.0495 = 0.0594.", "P(D|+) = 0.0099/0.0594 = **1/6 ≈ 0.167**."], "**1/6**", verify=lambda: str(F(99, 100) * F(1, 100) / (F(99, 100) * F(1, 100) + F(99, 100) * F(5, 100)))),
           Ex("Two urns", "Urn A: 3 red, 1 blue; urn B: 1 red, 3 blue. A random urn, a red ball. P(urn A)?", ["P(red) = ½·¾ + ½·¼ = ½. P(A | red) = (3/8)/(1/2) = **3/4**."], "**3/4**", verify=lambda: str(F(1, 2) * F(3, 4) / (F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4)))),
           Ex("Union with independence", "P(A) = 0.5, P(B) = 0.4, independent. P(A ∪ B)?", ["0.5 + 0.4 − 0.2 = **0.7**."], "**0.7**", verify=lambda: str(0.5 + 0.4 - 0.5 * 0.4)),
           Ex("Conditional", "P(A ∩ B) = 0.2, P(B) = 0.5. P(A | B)?", ["0.2/0.5 = **0.4**."], "**0.4**", verify=lambda: str(0.2 / 0.5)),
           Ex("Two aces", "Two cards from a 52-card deck without replacement. P(both aces)?", ["(4/52)(3/51) = 12/2652 = **1/221**."], "**1/221**", verify=lambda: str(F(4, 52) * F(3, 51))),
       ],
       traps=[("Confusing P(A|B) with P(B|A)", "The prosecutor's fallacy."),
              ("Exclusive ≠ independent", "Exclusive events with positive probability are dependent."),
              ("Forgetting the denominator", "P(B) must include every branch."),
              ("Replacement", "Without replacement probabilities change.")],
       quick=[("P(A|B) =", ["P(A)P(B)", "P(A∩B)/P(B)", "P(B|A)", "P(A)/P(B)"], 1, "Definition."),
              ("Independent events satisfy", ["P(A∩B) = P(A)+P(B)", "P(A∩B) = P(A)P(B)", "P(A∩B) = 0", "P(A) = P(B)"], 1, "Product rule."),
              ("Bayes needs", ["a partition and likelihoods", "independence", "equal priors", "a normal distribution"], 0, "Total probability."),
              ("Two mutually exclusive events with P > 0 are", ["independent", "dependent", "equal", "complementary"], 1, "P(A∩B) = 0 ≠ P(A)P(B).")],
       summary=["P(A|B) = P(A∩B)/P(B).", "Total probability sums over a partition.", "Bayes reverses the conditioning.", "Independence: product rule.", "Exclusive ≠ independent.", "Draw a tree."])

lesson(subject=S, chapter=PB, ch_no=9, no=4, slug="engm-pb-distributions", title="4 · Standard distributions: mean, variance and probabilities",
       topic=T_RV, subs=["Distribution formulas", "Distributions", "Expectation & variance"], minutes=22, weight=5, widget="none",
       key="Know the mean and variance of each standard distribution and the pmf of the discrete ones. Expectation is linear (even without independence); variance adds only for independent variables.",
       analogy=("🎲", "Menu of random processes", "Binomial counts successes in n trials, geometric counts trials to the first success, Poisson counts rare events in an interval. Pick the one whose story matches."),
       sections=[
           dict(h="Reference table", md="""| Distribution | Story | Mean | Variance |
|---|---|---|---|
| Bernoulli(p) | one trial | p | p(1 − p) |
| Binomial(n, p) | successes in n trials | np | np(1 − p) |
| Geometric(p) | trials until first success | 1/p | (1 − p)/p² |
| Poisson(λ) | rare events | λ | λ |
| Uniform[a, b] | equally likely | (a + b)/2 | (b − a)²/12 |
| Exponential(λ) | waiting time | 1/λ | 1/λ² |
| Normal(μ, σ²) | bell curve | μ | σ² |

Binomial pmf: P(X = k) = C(n, k) pᵏ(1 − p)ⁿ⁻ᵏ. Geometric: P(X = k) = (1 − p)ᵏ⁻¹p. Exponential is memoryless."""),
           dict(h="Rules of expectation and variance", md="""E[aX + bY] = aE[X] + bE[Y] always (linearity). Var(aX + b) = a²Var(X). For independent X, Y: Var(X ± Y) = Var(X) + Var(Y) and E[XY] = E[X]E[Y]. Var(X) = E[X²] − (E[X])². Expected number of fixed points of a random permutation is 1 (indicator variables).""")],
       examples=[
           Ex("Binomial", "X ~ Bin(10, 0.3). E[X] and Var(X)?", ["np = 3; np(1 − p) = 2.1."], "**3** and **2.1**", verify=lambda: "%d and %.1f" % (3, 10 * 0.3 * 0.7)),
           Ex("Geometric", "A coin with p = 0.2 of success: expected trials to first success?", ["1/p = **5**."], "**5**", verify=lambda: str(1 / 0.2)),
           Ex("Poisson second moment", "X ~ Poisson(4): E[X²]?", ["Var + mean² = 4 + 16 = **20**."], "**20**", verify=lambda: str(4 + 16)),
           Ex("Variance of a combination", "X, Y independent, Var(X) = 3, Var(Y) = 5. Var(2X − Y)?", ["4·3 + 5 = **17**."], "**17**", verify=lambda: str(4 * 3 + 5)),
           Ex("Fixed points", "Expected number of fixed points of a random permutation of 10 items?", ["10 indicators, each 1/10: **1**."], "**1**", verify=lambda: str(10 * F(1, 10))),
           Ex("Uniform variance", "Uniform on [2, 8]: variance?", ["(8 − 2)²/12 = **3**."], "**3**", verify=lambda: str(F(36, 12))),
       ],
       traps=[("Variance of a difference", "Variances add, even for X − Y."),
              ("Linearity", "E[X + Y] = E[X] + E[Y] needs no independence."),
              ("Geometric conventions", "Trials until success vs failures before success."),
              ("Poisson", "Mean equals variance.")],
       quick=[("Var of Bin(20, 0.5)", ["5", "10", "20", "0.25"], 0, "np(1 − p)."),
              ("E of geometric with p = 0.25", ["2", "4", "0.25", "8"], 1, "1/p."),
              ("Var(3X)", ["3Var(X)", "9Var(X)", "Var(X)", "Var(X) + 3"], 1, "a²."),
              ("Poisson(λ) mean and variance are", ["λ and λ²", "λ and λ", "λ² and λ", "1/λ and 1/λ²"], 1, "Equal.")],
       summary=["Binomial: np, np(1 − p).", "Geometric: 1/p.", "Poisson: λ and λ.", "Uniform: (a + b)/2, (b − a)²/12.", "Exponential: 1/λ, 1/λ².", "Var(aX + b) = a²Var(X)."])

lesson(subject=S, chapter=PB, ch_no=9, no=5, slug="engm-pb-problems", title="5 · Probability mixed problem set",
       topic=T_PB, subs=["Bayes with tables", "Distribution formulas", "Dice & coins", "Bayes & conditional", "Expectation & variance"], minutes=20, weight=5, widget="none",
       key="Decide whether the question is about counting outcomes (dice, coins, cards), conditioning (Bayes), or a named distribution; then use the matching formula.",
       analogy=("🧭", "Which model?", "Most of the work is choosing the model. Once you know it is binomial or a Bayes tree the arithmetic is short."),
       sections=[dict(h="Decision guide", md="""1. Equally likely outcomes: favourable/total with careful counting.
2. 'Given that' or 'what is the chance it came from': Bayes with a tree.
3. Repeated independent trials: binomial (fixed n), geometric (until success), Poisson (rare).
4. Averages: use linearity of expectation with indicator variables.
5. Check: probabilities lie in [0, 1] and branches sum to 1.""")],
       examples=[
           Ex("Two dice", "Probability that the sum of two dice is 8?", ["5 outcomes out of 36: **5/36**."], "**5/36**", verify=lambda: str(F(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 8), 36))),
           Ex("At least one head", "Probability of at least one head in 4 fair tosses?", ["1 − (1/2)⁴ = **15/16**."], "**15/16**", verify=lambda: str(1 - F(1, 16))),
           Ex("Binomial value", "P(exactly 2 successes) in 5 trials, p = 1/2?", ["C(5, 2)/32 = 10/32 = **5/16**."], "**5/16**", verify=lambda: str(F(C(5, 2), 32))),
           Ex("Expected maximum", "Expected value of one fair die roll?", ["(1 + 2 + … + 6)/6 = **3.5**."], "**3.5**", verify=lambda: str(sum(range(1, 7)) / 6)),
           Ex("Bayes", "Box 1 has 2 defective of 10, box 2 has 5 defective of 10. A box is chosen at random and the item is defective. P(box 1)?", ["P(D) = ½(0.2) + ½(0.5) = 0.35. P(box 1 | D) = 0.1/0.35 = **2/7**."], "**2/7**", verify=lambda: str(F(1, 2) * F(2, 10) / (F(1, 2) * F(2, 10) + F(1, 2) * F(5, 10)))),
       ],
       traps=[("Wrong sample space", "Treat distinguishable dice as ordered pairs."),
              ("At least one", "Use the complement."),
              ("Without replacement", "Probabilities change after each draw."),
              ("Mixing up distributions", "Fixed n: binomial. Until first success: geometric.")],
       quick=[("P(sum 7) with two dice", ["1/6", "1/12", "5/36", "7/36"], 0, "6/36."),
              ("P(at least one six in 3 rolls)", ["1/2", "91/216", "125/216", "1/6"], 1, "1 − (5/6)³."),
              ("E[one die]", ["3", "3.5", "4", "6"], 1, "Average of 1–6."),
              ("Bayes posterior with equal priors depends on", ["likelihood ratio", "nothing", "only the prior", "variance"], 0, "Equal priors cancel.")],
       summary=["Equally likely: favourable/total.", "Given that: Bayes with a tree.", "'At least one': 1 − P(none).", "Expectation: linearity with indicators.", "Match the story to the distribution.", "Probabilities sum to 1 across branches."])
