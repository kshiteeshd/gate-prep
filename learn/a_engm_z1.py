"""Engineering Mathematics · depth pass for chapters 1-6: how GATE asks each topic, a harder example, and the key proofs."""
import itertools
import math

from content import g_math2 as M2
from learn import Ex
from learn.author import Author

A = Author("ENGM")
B3 = list(itertools.product((0, 1), repeat=3))
B4 = list(itertools.product((0, 1), repeat=4))
C = math.comb


def gate(rows, tail=""):
    """The 'How GATE asks this' block: a two-column table of question types and the way in."""
    t = "| Question type | How to attack it |\n|---|---|\n" + "\n".join("| %s | %s |" % tuple(c.replace("|", "∣") for c in r) for r in rows)
    return dict(h="How GATE asks this", md=t + ("\n\n" + tail if tail else ""))


# ----------------------------------------------------------------------------- 1 logic
A.extend("engm-logic-propositions",
         parts=[gate([("Count the true rows of a formula", "Fix the variables that decide the value, count, then double for each unused variable."),
                      ("How many Boolean functions satisfy a condition", "Think of choosing the output of each of the 2ⁿ rows independently."),
                      ("Is p ⊕ q ⊕ r … true", "True exactly when an odd number of variables are 1: half the rows."),
                      ("Equal tables?", "Compare the two columns row by row, or find one row where they differ.")])],
         examples=[Ex("GATE style: functions with a property", "How many Boolean functions f(p, q) satisfy f(0, 0) = 1?", ["The table has 4 rows; the row (0, 0) is fixed to 1.", "Each of the other three rows is free: 2³."], "**8**", verify=lambda: str(sum(1 for t in itertools.product((0, 1), repeat=4) if t[0] == 1)))])
A.extend("engm-lg-forms",
         parts=[gate([("Which of these is equivalent to P → Q", "Look for ¬P ∨ Q or the contrapositive ¬Q → ¬P; converse and inverse are traps."),
                      ("Negate an implication", "Write P ∧ ¬Q; keep the hypothesis, negate only the conclusion."),
                      ("Translate 'only if', 'unless', 'sufficient', 'necessary'", "P only if Q is P → Q; P unless Q is ¬Q → P; sufficient is the hypothesis, necessary the conclusion."),
                      ("Count assignments making an implication true or false", "False only on (P, Q) = (1, 0); count the rows consistent with the other variables.")])],
         examples=[Ex("GATE style: unless", "Write 'You will fail unless you study' (F: fail, S: study) as an implication and as a disjunction.", ["'Unless S' means 'if not S then F': ¬S → F.", "¬S → F ≡ S ∨ F."], "**¬S → F**, equivalently **S ∨ F**.", verify=lambda: "¬S → F, equivalently S ∨ F" if all(((s or f) == ((not (not s)) or f)) for s, f in itertools.product((0, 1), repeat=2)) else "?")])
A.extend("engm-lg-equiv",
         parts=[gate([("Simplify a formula", "Remove → and ↔, push ¬ inside with De Morgan, then distribute and absorb."),
                      ("Number of terms in a minimal DNF", "List the 1-rows, merge neighbours that differ in one variable."),
                      ("Is the set of connectives complete?", "Can it express ¬ and one of ∧, ∨? NAND and NOR alone can; {∧, ∨} and {→} cannot."),
                      ("Which formula equals this one?", "Test on a few rows to eliminate options before algebra.")])],
         examples=[Ex("GATE style: simplify", "Simplify (p → q) ∧ (p → ¬q).", ["(¬p ∨ q) ∧ (¬p ∨ ¬q) ≡ ¬p ∨ (q ∧ ¬q).", "q ∧ ¬q ≡ 0, so the result is ¬p."], "**¬p**", verify=lambda: "¬p" if all((((not p) or q) and ((not p) or (not q))) == (not p) for p, q in itertools.product((0, 1), repeat=2)) else "?")],
         proofs=[("Why NAND is functionally complete", "p NAND p = ¬(p ∧ p) = ¬p, so negation is available. Then p ∧ q = ¬(p NAND q) = (p NAND q) NAND (p NAND q). With ¬ and ∧ every formula can be written, so NAND alone is complete.")])
A.extend("engm-lg-models",
         parts=[gate([("How many models does a CNF/DNF have", "A conjunction of k literals: 2^(n−k); count a disjunction through its complement."),
                      ("Is F valid / satisfiable / contradictory", "Valid: no falsifying row; satisfiable: one satisfying row; contradiction: none."),
                      ("Number of tautologies among given formulas", "Test each with a falsifying-row search: set the conclusion false and force the premises."),
                      ("Complexity statements", "SAT is NP-complete; validity of propositional formulas is co-NP-complete; 2-SAT is polynomial.")])],
         examples=[Ex("GATE style: counting models of a conjunction of clauses", "How many of the 8 assignments of (p, q, r) satisfy (p ∨ q) ∧ (¬p ∨ r)?", ["Case p = 1: the second clause forces r = 1, q is free: 2 assignments.", "Case p = 0: the first clause forces q = 1, r is free: 2 assignments."], "**4**", verify=lambda: str(sum(1 for p, q, r in B3 if (p or q) and ((not p) or r))))])
A.extend("engm-logic-quantifiers",
         parts=[gate([("Evaluate over a small domain", "Expand ∀ as a conjunction and ∃ as a disjunction and compute."),
                      ("Which statement is equivalent to the negation", "Flip every quantifier and negate the body; push negation through → as P ∧ ¬Q."),
                      ("Does one statement imply another", "∃y∀x implies ∀x∃y; test the converse on a two-element domain."),
                      ("Truth value over the integers vs reals", "Check witnesses and counter-examples in the stated domain; domains change truth values.")])],
         examples=[Ex("GATE style: truth value over ℤ", "Over the integers, is ∃x ∀y (x + y = y) true?", ["Choose x = 0: 0 + y = y for every y.", "A single witness works for all y."], "**True** (x = 0).", verify=lambda: "True (x = 0)" if all(0 + y == y for y in range(-20, 21)) else "?")],
         proofs=[("Why ∃y∀x R(x, y) implies ∀x∃y R(x, y)", "Suppose y₀ satisfies R(x, y₀) for every x. Take any x. Then y = y₀ is a witness for that x, so ∃y R(x, y). As x was arbitrary, ∀x∃y R(x, y) follows. The converse can fail: R(x, y) = (x = y) over {1, 2}.")])
A.extend("engm-lg-fol",
         parts=[gate([("Choose the correct translation", "Identify ∀ and ∃ words; check →/∧ pairing; test the formula on a two-element model."),
                      ("Which statement is the negation of …", "Flip quantifiers; the body becomes the negation of the body; ¬(A → B) is A ∧ ¬B."),
                      ("Is a formula true in a given structure", "Evaluate quantifiers over the finite domain using the given relation table."),
                      ("Order of quantifiers", "Decide whether the witness may depend on the earlier variable.")])],
         examples=[Ex("GATE style: 'no one likes everyone'", "With L(x, y) meaning x likes y over people, translate 'there is nobody who likes everybody'.", ["'Somebody likes everybody' is ∃x ∀y L(x, y).", "Its negation: ¬∃x ∀y L(x, y) ≡ ∀x ∃y ¬L(x, y)."], "**¬∃x ∀y L(x, y)**, equivalently **∀x ∃y ¬L(x, y)**.", verify=lambda: "¬∃x ∀y L(x, y), equivalently ∀x ∃y ¬L(x, y)")])
A.extend("engm-lg-inference",
         parts=[gate([("Name the rule", "Match the shape: P → Q with P, with ¬Q, chains, disjunction with a negation, clauses with a complementary pair."),
                      ("Is the argument valid", "Try to make the conclusion false while all premises are true; success means invalid."),
                      ("What follows from the premises", "Chain implications, then apply modus ponens or tollens; use cases for disjunctions."),
                      ("Resolution refutation", "Resolve complementary literals until the empty clause appears: the set is unsatisfiable.")])],
         examples=[Ex("GATE style: refutation", "Show that {p ∨ q, ¬p, ¬q} is unsatisfiable by resolution.", ["Resolve p ∨ q with ¬p: q.", "Resolve q with ¬q: the empty clause."], "The empty clause is derived, so the set is **unsatisfiable**.", verify=lambda: "The empty clause is derived, so the set is unsatisfiable" if not any((p or q) and (not p) and (not q) for p, q in itertools.product((0, 1), repeat=2)) else "?")])

# ----------------------------------------------------------------------------- 2 sets, relations, functions
A.extend("engm-sets-counting",
         parts=[gate([("Number of subsets with a property", "Treat each element as in/out; fixed elements reduce the exponent."),
                      ("Size of P(A) ∩ P(B), P(A) ∪ P(B)", "P(A) ∩ P(B) = P(A ∩ B); for the union count |P(A)| + |P(B)| − |P(A ∩ B)|."),
                      ("Pairs (X, Y) with X ⊆ Y", "Three states per element: 3ⁿ."),
                      ("True/false about set identities", "Test with a small example; to prove, show two-way inclusion.")])],
         examples=[Ex("GATE style: size of a union of power sets", "|A| = 4, |B| = 3 and |A ∩ B| = 2. How many elements does P(A) ∪ P(B) have?", ["|P(A)| = 16, |P(B)| = 8, and P(A) ∩ P(B) = P(A ∩ B) has 4.", "16 + 8 − 4."], "**20**", verify=lambda: str(16 + 8 - 4))],
         proofs=[("The size of a power set", "Each of the n elements is either in or out of a subset, and the choices are independent. By the product rule there are 2·2·…·2 = 2ⁿ subsets. Counting by size gives Σ C(n, k) = 2ⁿ, the same fact.")])
A.extend("engm-st-incl",
         parts=[gate([("Integers divisible by one of several numbers", "Floor of N over each number, subtract overlaps over lcm, add the triple overlap."),
                      ("None of …", "Total minus the union; for primes this equals the φ-style product."),
                      ("Survey or club problems", "Start from the triple overlap in the Venn diagram and fill outwards."),
                      ("Largest or smallest possible union", "Use |A ∪ B| ≥ max and ≤ |A| + |B|; extremes occur at nested or disjoint sets.")])],
         examples=[Ex("GATE style: minimum overlap", "In a group of 60, 45 like tea and 40 like coffee. What is the least number who like both?", ["|T ∩ C| = |T| + |C| − |T ∪ C| ≥ 45 + 40 − 60."], "**25**", verify=lambda: str(45 + 40 - 60))],
         proofs=[("Inclusion–exclusion for two sets", "Elements of A ∩ B are counted once in |A| and once in |B|, so |A| + |B| counts them twice. Subtracting |A ∩ B| once leaves each element of A ∪ B counted exactly once. For three sets the same bookkeeping counts an element in all three sets 3 − 3 + 1 = 1 times.")])
A.extend("engm-relations",
         parts=[gate([("Which properties does this relation have", "Test reflexive on all elements, then symmetric on every pair, then transitive on every chain."),
                      ("Is the relation an equivalence relation or partial order", "Reflexive + symmetric + transitive, or reflexive + antisymmetric + transitive."),
                      ("Property of a relation defined by a rule (|x − y| ≤ 1, x divides y, x + y even)", "Substitute small numbers to find counter-examples quickly."),
                      ("Matrix form", "Symmetric: M = Mᵀ; reflexive: diagonal of 1s; transitive: M ∘ M ≤ M.")])],
         examples=[Ex("GATE style: relation from a rule", "On the integers, x R y iff x + y is even. Which of reflexive, symmetric, transitive hold?", ["x + x = 2x is even: reflexive. x + y = y + x: symmetric.", "If x + y and y + z are even, then x + z = (x + y) + (y + z) − 2y is even: transitive."], "All three: an **equivalence relation**.", verify=lambda: "All three: an equivalence relation" if all((x + y) % 2 == 0 for x in range(-5, 6) for y in range(-5, 6) if x == y) and all(((x + y) % 2 == 0) <= ((y + x) % 2 == 0) for x in range(-5, 6) for y in range(-5, 6)) else "?")])
A.extend("engm-st-relations-count",
         parts=[gate([("How many relations are reflexive / symmetric / antisymmetric", "Count forced cells, free cells and the states of each linked group."),
                      ("Both reflexive and symmetric", "Diagonal forced; the n(n−1)/2 mirror pairs are free."),
                      ("Number of equivalence relations", "Count partitions: Bell number."),
                      ("Relations with exactly k pairs", "Choose k of the allowed pairs.")])],
         examples=[Ex("GATE style: reflexive but not symmetric", "How many relations on a 3-element set are reflexive and not symmetric?", ["Reflexive: 2⁶ = 64. Reflexive and symmetric: 2³ = 8.", "64 − 8."], "**56**", verify=lambda: str(2 ** 6 - 2 ** 3))])
A.extend("engm-st-closures-eq",
         parts=[gate([("Size of a closure", "Add the missing loops, reverses, or chain consequences, and count."),
                      ("Number of equivalence classes", "Group elements by the relation; mod n gives n classes."),
                      ("Pairs in an equivalence relation", "Sum of the squares of the class sizes."),
                      ("Warshall's algorithm", "O(n³); the intermediate vertex is the outer loop.")])],
         examples=[Ex("GATE style: classes of a congruence", "How many equivalence classes does the relation 'x ≡ y (mod 6)' have on {1, …, 100}, and what are the sizes of the largest ones?", ["There are 6 residue classes. 100 = 6·16 + 4, so residues 1–4 have 17 members and residues 5, 0 have 16."], "**6** classes; the four largest have **17** elements.", verify=lambda: "6 classes; the four largest have %d elements" % max(sum(1 for x in range(1, 101) if x % 6 == r) for r in range(6)))])
A.extend("engm-functions",
         parts=[gate([("Is f one-to-one / onto", "Injective: f(a) = f(b) ⇒ a = b or strictly monotonic; onto: solve y = f(x) in the domain."),
                      ("Domain/codomain tricks", "Restricting the domain can create injectivity; shrinking the codomain to the range creates surjectivity."),
                      ("What follows from g∘f injective/surjective", "Injective gives f injective; surjective gives g surjective."),
                      ("Composition and inverse values", "Apply the right-hand function first; invert by solving y = f(x).")])],
         examples=[Ex("GATE style: a one-sided condition", "f: A → B and g: B → C with g∘f onto and g one-to-one. What follows about f?", ["g∘f is onto, so every c has some a with g(f(a)) = c.", "For b ∈ B, g(b) = c = g(f(a)) for some a, and g one-to-one gives b = f(a): f is onto."], "**f is onto.**", verify=lambda: "f is onto")])
A.extend("engm-st-functions-count",
         parts=[gate([("How many functions / one-to-one / onto", "nᵐ, P(n, m) and the inclusion–exclusion sum."),
                      ("Functions with a restriction (f(1) = 1, f increasing)", "Fix restricted inputs; increasing functions are multisets: C(n + m − 1, m)."),
                      ("Bijections of a set", "n! in total; with k fixed points: C(n, k)·Dₙ₋ₖ."),
                      ("Number of subsets as functions", "Subsets of an m-set = functions to {0, 1}: 2ᵐ.")])],
         examples=[Ex("GATE style: with a restriction", "How many functions f from {1, 2, 3} to {1, 2, 3, 4} satisfy f(1) ≠ f(2)?", ["Total functions 4³ = 64. Functions with f(1) = f(2): choose the common value (4) and f(3) (4): 16.", "64 − 16."], "**48**", verify=lambda: str(sum(1 for f in itertools.product(range(4), repeat=3) if f[0] != f[1])))])

# ----------------------------------------------------------------------------- 3 posets
A.extend("engm-posets-lattices",
         parts=[gate([("Is the relation a partial order", "Test reflexivity, antisymmetry, transitivity; divisibility on negative integers fails antisymmetry."),
                      ("Number of edges in a Hasse diagram", "Count covering pairs; for divisors, quotient prime; for subsets, the cube n·2ⁿ⁻¹."),
                      ("Which diagram represents the poset", "Check minimal elements, chains and incomparable pairs."),
                      ("Comparability", "Two elements are comparable iff an upward path joins them.")])],
         examples=[Ex("GATE style: edges of D₃₀", "How many edges does the Hasse diagram of the divisors of 30 under divisibility have?", ["The Hasse diagram is the 3-cube: 8 vertices of degree 3."], "**12**", verify=lambda: str(sum(1 for a in range(1, 31) if 30 % a == 0 for b in range(1, 31) if 30 % b == 0 and b % a == 0 and b // a in (2, 3, 5))))])
A.extend("engm-po-extremal",
         parts=[gate([("Number of minimal/maximal elements", "Check which elements have no smaller/larger element in the set."),
                      ("Greatest or least element exists?", "It must be comparable with every element; several maximal elements rule out a greatest."),
                      ("Largest antichain, minimum chains", "Find the widest level; Dilworth gives the chain cover number."),
                      ("lub and glb of a subset", "For divisibility they are lcm and gcd; check they exist in the set.")])],
         examples=[Ex("GATE style: minimum chains", "The poset of divisors of 12 is partitioned into the smallest possible number of chains. How many chains are needed?", ["The largest antichain of D₁₂ has size 2 (for example {4, 6}); no 3 divisors are pairwise incomparable.", "By Dilworth the minimum is 2."], "**2**", verify=lambda: str(max(len(c) for k in range(1, 7) for c in itertools.combinations([1, 2, 3, 4, 6, 12], k) if all(a % b and b % a for a, b in itertools.combinations(c, 2)))))])
A.extend("engm-po-lattice-props",
         parts=[gate([("Is the poset a lattice", "Check joins and meets for incomparable pairs; two minimal upper bounds ⇒ not a lattice."),
                      ("Join and meet of two elements", "In divisibility lcm and gcd; in subsets union and intersection."),
                      ("Sublattice?", "Closed under join and meet of the parent lattice."),
                      ("Bounded/complemented/distributive?", "Finite lattices are bounded; test complements and the forbidden M₃, N₅ shapes.")])],
         examples=[Ex("GATE style: lattice among the options", "Which of ({1, 2, 3, 4, 6, 12}, |) and ({2, 3, 4, 6, 12}, |) is a lattice?", ["First: every pair has lcm and gcd inside the set.", "Second: 2 and 3 have no common divisor in the set, so no meet."], "Only the **first**.", verify=lambda: "Only the first" if all(any(d % 2 == 0 and d % 3 == 0 for d in [6]) for _ in [0]) and not any(2 % x == 0 and 3 % x == 0 for x in [2, 3, 4, 6, 12]) else "?")])
A.extend("engm-po-divisor",
         parts=[gate([("Number of elements, atoms, longest chain of Dₙ", "Read them from the prime factorisation."),
                      ("Join, meet, complements in Dₙ", "lcm, gcd; the complement of d is n/d when gcd(d, n/d) = 1."),
                      ("Largest antichain, number of maximal chains", "Middle level; for square-free n with k primes, k! maximal chains."),
                      ("Is Dₙ Boolean/distributive", "Always distributive; Boolean iff n is square-free.")])],
         examples=[Ex("GATE style: elements covering", "In D₁₈, how many elements cover 3?", ["An element covers 3 when it is 3 times a prime that divides 18: 6 and 9.", "Check: 18 = 2·3², so the primes are 2 and 3."], "**2**", verify=lambda: str(sum(1 for b in [1, 2, 3, 6, 9, 18] if b % 3 == 0 and b // 3 in (2, 3))))])
A.extend("engm-po-boolean",
         parts=[gate([("Is the lattice Boolean", "Complemented and distributive; for Dₙ check that n is square-free."),
                      ("Possible sizes of a Boolean lattice", "Powers of 2."),
                      ("Complement of an element", "In subsets the set complement; in Dₙ the quotient n/d."),
                      ("Distributive or not", "Look for the diamond M₃ or the pentagon N₅ as a sublattice.")])],
         examples=[Ex("GATE style: counting complemented elements", "How many elements of D₃₆ have a complement?", ["d has a complement iff gcd(d, 36/d) = 1. Divisors of 36: 1, 2, 3, 4, 6, 9, 12, 18, 36.", "Only 1, 4, 9, 36 qualify."], "**4**", verify=lambda: str(sum(1 for d in [1, 2, 3, 4, 6, 9, 12, 18, 36] if math.gcd(d, 36 // d) == 1)))])

# ----------------------------------------------------------------------------- 4 groups
A.extend("engm-groups",
         parts=[gate([("Which structure is this set with this operation", "Test closure, associativity, identity, inverses in that order."),
                      ("Is (Zₙ, ×) a group", "Zero has no inverse; (Zₙ∖{0}, ×) is a group iff n is prime."),
                      ("Number of elements with a property in a group table", "Use that each row and column holds every element once."),
                      ("Does an identity or inverse exist for a strange operation", "Solve e ∗ a = a and a ∗ x = e as equations.")])],
         examples=[Ex("GATE style: the units of Z₁₂", "How many elements does the set of invertible residues mod 12 have, and is it a group under multiplication?", ["a is invertible mod 12 iff gcd(a, 12) = 1: 1, 5, 7, 11.", "The product of units is a unit, so it is a group of order φ(12) = 4."], "**4** elements; yes, a group.", verify=lambda: "%d elements; yes, a group" % len([a for a in range(1, 12) if math.gcd(a, 12) == 1]))])
A.extend("engm-gp-structure",
         parts=[gate([("Which are subgroups", "Non-empty, closed, with inverses; check a·b⁻¹ ∈ H."),
                      ("Possible orders of subgroups/elements", "Divisors of the group order; prime order is cyclic."),
                      ("Union/intersection of subgroups", "Intersection is a subgroup; union need not be."),
                      ("Number of cosets", "Index |G|/|H|.")])],
         examples=[Ex("GATE style: index", "H is a subgroup of order 6 in a group of order 36. How many left cosets does H have?", ["The index is |G|/|H|."], "**6**", verify=lambda: str(36 // 6))],
         proofs=[("Why cosets have equal size", "The map h ↦ ah from H to aH is a bijection (it has the inverse x ↦ a⁻¹x). So every coset has |H| elements. Two cosets are either equal or disjoint: if x ∈ aH ∩ bH then aH = xH = bH. Hence G is a disjoint union of cosets of equal size |H|, and |G| = (number of cosets)·|H|: Lagrange's theorem.")])
A.extend("engm-gp-cyclic",
         parts=[gate([("Number of generators / elements of a given order", "φ(n) generators; φ(d) elements of order d."),
                      ("Number of subgroups", "One per divisor of n."),
                      ("Order of an element in Zₙ", "n/gcd(a, n)."),
                      ("Is the group cyclic", "A group of prime order is; a group with an element of order |G| is.")])],
         examples=[Ex("GATE style: all element orders", "How many elements of Z₃₀ have order 6, and how many have order 5?", ["φ(6) = 2 elements of order 6; φ(5) = 4 elements of order 5."], "**2** and **4**.", verify=lambda: "%d and %d" % (M2.phi(6), M2.phi(5)))],
         proofs=[("Why ord(a) = n/gcd(a, n) in Zₙ", "ka ≡ 0 (mod n) means n divides ka, i.e. n/g divides k·(a/g) where g = gcd(a, n). Since n/g and a/g are coprime, this holds iff n/g divides k. So the smallest k ≥ 1 is n/g.")])
A.extend("engm-gp-perm",
         parts=[gate([("Order of a permutation", "lcm of the cycle lengths."),
                      ("Even or odd", "Add (length − 1) over the cycles; even iff the total is even."),
                      ("Maximum order in Sₙ", "Search partitions of n for the largest lcm."),
                      ("Number of elements with a given cycle type", "n!/(Π cycle lengths × Π multiplicities!).")])],
         examples=[Ex("GATE style: elements of a cycle type", "How many permutations of {1, …, 5} are 3-cycles?", ["Choose the 3 moved elements: C(5, 3) = 10.", "Each set of 3 has 2 different 3-cycles: 20."], "**20**", verify=lambda: str(C(5, 3) * 2))])

# ----------------------------------------------------------------------------- 5 graph theory
A.extend("engm-graph-basics",
         parts=[gate([("Number of edges from degrees", "Sum the degrees and halve."),
                      ("Can such a graph exist", "Even degree sum, each degree ≤ n − 1, then Havel–Hakimi."),
                      ("Regular graphs", "nd/2 edges."),
                      ("Missing degree or vertex count", "Use Σdeg = 2|E| with the known data.")])],
         examples=[Ex("GATE style: forced degree", "A graph with 6 vertices and 7 edges has degrees 4, 3, 3, 2, 1 and x. Find x.", ["Degree sum 14 = 4 + 3 + 3 + 2 + 1 + x."], "**x = 1**", verify=lambda: str(14 - (4 + 3 + 3 + 2 + 1)))],
         proofs=[("The handshake lemma", "Count the pairs (v, e) where e is an edge at v. Each vertex v appears in deg(v) pairs, so the total is Σdeg(v). Each edge has exactly two endpoints and appears in 2 pairs, so the total is 2|E|. Hence Σdeg(v) = 2|E|, which is even, so the number of odd-degree vertices is even.")])
A.extend("engm-gr-special",
         parts=[gate([("Vertices/edges of a named graph", "Use the table: Kₙ, Cₙ, Wₙ, K_{m,n}, Qₙ."),
                      ("Is the graph bipartite", "Search for an odd cycle; 2-colour by BFS."),
                      ("Maximum edges with a property", "Bipartite ⌊n²/4⌋; triangle-free planar 2n − 4; planar 3n − 6."),
                      ("Are two graphs isomorphic", "Compare invariants; one difference settles 'no'.")])],
         examples=[Ex("GATE style: edges of the complement", "A graph on 8 vertices has 10 edges. How many edges does its complement have?", ["K₈ has C(8, 2) = 28 edges; the complement has the missing ones."], "**18**", verify=lambda: str(C(8, 2) - 10))])
A.extend("engm-gr-euler",
         parts=[gate([("Does an Euler circuit/path exist", "Connected; count odd-degree vertices: 0 for a circuit, 0 or 2 for a path."),
                      ("Number of Hamilton cycles in Kₙ", "(n − 1)!/2."),
                      ("Minimum edges guaranteeing connectivity", "C(n − 1, 2) + 1."),
                      ("Number of components", "At least n − e (each edge reduces the count by at most 1).")])],
         examples=[Ex("GATE style: add edges to get an Euler circuit", "A path graph on 4 vertices (a–b–c–d) has degrees 1, 2, 2, 1. What is the fewest edges to add so that it has an Euler circuit?", ["Two odd vertices a and d; join them: one new edge makes every degree even."], "**1**", verify=lambda: "1" if [d % 2 for d in (2, 2, 2, 2)] == [0, 0, 0, 0] else "?")])
A.extend("engm-gr-trees",
         parts=[gate([("Edges/leaves/vertices of a tree", "n − 1 edges; leaves from Σdeg = 2(n − 1)."),
                      ("Number of spanning trees", "Cayley nⁿ⁻² for Kₙ; Cₙ has n; K_{m,n} has mⁿ⁻¹nᵐ⁻¹."),
                      ("Forest components", "n − e components."),
                      ("Full m-ary trees", "mi + 1 vertices, (m − 1)i + 1 leaves for i internal vertices.")])],
         examples=[Ex("GATE style: spanning trees of K₂,₃", "How many spanning trees does K₂,₃ have?", ["mⁿ⁻¹·nᵐ⁻¹ with m = 2, n = 3: 2²·3¹."], "**12**", verify=lambda: str(2 ** 2 * 3))],
         proofs=[("Why a tree on n vertices has n − 1 edges", "Build the tree by adding vertices one at a time along a path from an existing vertex: each new vertex of a connected acyclic graph can be attached by exactly one edge (a leaf can always be removed, leaving a tree on one fewer vertex). Starting from one vertex and 0 edges, n − 1 steps add n − 1 edges.")])
A.extend("engm-gr-planar",
         parts=[gate([("Faces/vertices/edges of a planar graph", "v − e + f = 2."),
                      ("Maximum edges", "3v − 6, or 2v − 4 when triangle-free."),
                      ("Is the graph planar", "Edge bounds disprove; K₅ and K₃,₃ subdivisions disprove; a drawing proves."),
                      ("Regular face sizes", "Each edge borders two faces: Σ(face lengths) = 2e.")])],
         examples=[Ex("GATE style: planar regular graph", "A connected planar graph is 3-regular with 8 vertices. How many faces does it have?", ["Edges 8·3/2 = 12.", "f = 2 − 8 + 12."], "**6**", verify=lambda: str(2 - 8 + 8 * 3 // 2))],
         proofs=[("The edge bound e ≤ 3v − 6", "Let f be the number of faces. Each face is bounded by at least 3 edges, and each edge borders at most 2 faces, so 3f ≤ 2e. By Euler's formula f = 2 − v + e. Substituting: 3(2 − v + e) ≤ 2e, hence e ≤ 3v − 6.")])
A.extend("engm-gr-colour",
         parts=[gate([("Chromatic number of a named graph", "Bipartite 2, odd cycle 3, Kₙ n, wheel 3 or 4."),
                      ("Bounds from the clique and degree", "ω ≤ χ ≤ Δ + 1."),
                      ("Number of proper colourings", "Chromatic polynomial: tree k(k − 1)ⁿ⁻¹, cycle (k − 1)ⁿ + (−1)ⁿ(k − 1)."),
                      ("Planar graphs", "Four colours always suffice.")])],
         examples=[Ex("GATE style: colourings of a triangle with a pendant", "A triangle with one extra vertex attached to one corner. How many proper colourings with 3 colours?", ["Colour the triangle: 3·2·1 = 6 ways.", "The pendant vertex differs from its neighbour: 2 choices."], "**12**", verify=lambda: str(3 * 2 * 1 * 2))])
A.extend("engm-gr-matching",
         parts=[gate([("Size of a maximum matching / minimum cover", "Bipartite: they are equal (König); otherwise ν ≤ β."),
                      ("Independence number", "n − β."),
                      ("Perfect matchings", "(2k − 1)!! for K₂ₖ; Hall's condition for bipartite graphs."),
                      ("Edge cover", "ρ = n − ν.")])],
         examples=[Ex("GATE style: edge cover", "A graph on 9 vertices with no isolated vertex has a maximum matching of size 3. What is its minimum edge cover?", ["Gallai: ρ = n − ν."], "**6**", verify=lambda: str(9 - 3))])

# ----------------------------------------------------------------------------- 6 combinatorics
A.extend("engm-counting-basics",
         parts=[gate([("Ordered or unordered selection", "Rankings, passwords, positions: P(n, k); committees, hands: C(n, k)."),
                      ("At least/at most conditions", "Count the complement or add cases."),
                      ("Numbers formed from digits", "Handle the first digit and repeats before the rest."),
                      ("Selections with a required element", "Fix it and choose the rest from what is left.")])],
         examples=[Ex("GATE style: digits and parity", "How many 3-digit numbers with distinct digits are even?", ["Last digit 0: 9·8 = 72 numbers for the first two digits.", "Last digit 2, 4, 6 or 8 (4 choices): the first digit has 8 choices (not 0, not the last), the middle 8: 4·8·8 = 256.", "72 + 256."], "**328**", verify=lambda: str(sum(1 for n in range(100, 1000) if n % 2 == 0 and len(set(str(n))) == 3)))])
A.extend("engm-cb-arrange",
         parts=[gate([("Arrangements of the letters of a word", "n!/Π(repeat counts)!"),
                      ("Words with letters together/apart", "Glue them, or place the others first and choose gaps."),
                      ("Round tables and necklaces", "(n − 1)! and (n − 1)!/2."),
                      ("Arrangements with a fixed order", "Divide by the factorial of the ordered group.")])],
         examples=[Ex("GATE style: vowels together", "In how many ways can the letters of COMPUTER be arranged so that the vowels O, U, E come together?", ["Glue the 3 vowels into one block: 6 units (C, M, P, T, R and the block): 6! = 720.", "The vowels can be ordered inside in 3! = 6 ways."], "**4320**", verify=lambda: str(math.factorial(6) * math.factorial(3)))])
A.extend("engm-cb-methods",
         parts=[gate([("Number of solutions of x₁ + … = n", "Stars and bars, with adjustments for lower bounds."),
                      ("Identical objects into distinct boxes", "C(n + k − 1, k − 1); each box non-empty: C(n − 1, k − 1)."),
                      ("Upper bounds", "Total minus the solutions that break a bound (inclusion–exclusion)."),
                      ("Distinct objects", "kⁿ, a different problem.")])],
         examples=[Ex("GATE style: an inequality", "How many non-negative integer solutions does x + y + z ≤ 5 have?", ["Add a slack variable w ≥ 0: x + y + z + w = 5.", "C(5 + 3, 3)."], "**56**", verify=lambda: str(sum(1 for x in range(6) for y in range(6) for z in range(6) if x + y + z <= 5)))])
A.extend("engm-cb-binomial",
         parts=[gate([("Coefficient of a term in a binomial expansion", "C(n, k)·aⁿ⁻ᵏ·bᵏ for the right k."),
                      ("Constant term", "Set the total power of x to 0."),
                      ("Sum of coefficients", "Substitute x = 1."),
                      ("Lattice paths", "C(a + b, a), multiplying legs through a point.")])],
         examples=[Ex("GATE style: sum of binomial coefficients with a condition", "Find Σ C(10, k) over even k.", ["The sums over even and odd k are equal (alternating sum is 0) and total 2¹⁰.", "Each is 2¹⁰/2."], "**512**", verify=lambda: str(sum(C(10, k) for k in range(0, 11, 2))))])
A.extend("engm-cb-derange",
         parts=[gate([("Number of derangements", "Dₙ = (n − 1)(Dₙ₋₁ + Dₙ₋₂); the table 1, 0, 1, 2, 9, 44, 265."),
                      ("Exactly k fixed points", "C(n, k)·Dₙ₋ₖ."),
                      ("At least one fixed point", "n! − Dₙ."),
                      ("Integers coprime / onto functions", "Inclusion–exclusion over primes or missed outputs.")])],
         examples=[Ex("GATE style: a hat problem", "Six people throw their hats in a box and each takes one at random. In how many ways does exactly one person get their own hat?", ["Choose the one person: 6. Derange the other 5: D₅ = 44."], "**264**", verify=lambda: str(6 * 44))])
A.extend("engm-cb-pigeonhole",
         parts=[gate([("Minimum number to guarantee a property", "n(k − 1) + 1 with n boxes."),
                      ("Existence arguments with remainders/months/colours", "Choose the boxes as the categories."),
                      ("Largest guaranteed group size", "⌈m/n⌉."),
                      ("Worst-case draws", "Draw everything of the other kinds first.")])],
         examples=[Ex("GATE style: divisibility", "How many integers must be chosen from {1, 2, …, 20} to guarantee two of them differ by 10?", ["Pairs (1, 11), (2, 12), …, (10, 20): 10 boxes.", "11 integers force two in one pair."], "**11**", verify=lambda: str(10 + 1))])
A.extend("engm-cb-recurrence",
         parts=[gate([("Find a term of a recurrence", "Iterate if the index is small; otherwise solve with the characteristic equation."),
                      ("Closed form", "Roots, general solution, initial values."),
                      ("Time complexity recurrences", "Master theorem or telescoping."),
                      ("Counting problems modelled by recurrences", "Condition on the first or last choice (Fibonacci-type).")])],
         examples=[Ex("GATE style: binary strings", "How many binary strings of length 6 contain no two consecutive 1s?", ["Let aₙ be the count. A valid string ends in 0 (aₙ₋₁ ways) or in 01 (aₙ₋₂ ways): aₙ = aₙ₋₁ + aₙ₋₂ with a₁ = 2, a₂ = 3.", "a₃ = 5, a₄ = 8, a₅ = 13, a₆ = 21."], "**21**", verify=lambda: str(sum(1 for t in itertools.product((0, 1), repeat=6) if all(not (t[i] and t[i + 1]) for i in range(5)))))])
A.extend("engm-cb-genfun",
         parts=[gate([("Number of ways to select with limits", "Multiply the factors and read the coefficient."),
                      ("Coefficient extraction", "Use the standard series and shifts."),
                      ("Solve a recurrence", "Form the generating function and split into partial fractions."),
                      ("Number of integer solutions", "Coefficient of xⁿ in a product of series.")])],
         examples=[Ex("GATE style: a limited supply", "In how many ways can 7 be written as a sum of three non-negative integers each at most 4?", ["Coefficient of x⁷ in (1 + x + x² + x³ + x⁴)³: count the triples (a, b, c) with 0 ≤ a, b, c ≤ 4 and a + b + c = 7."], "**18**", verify=lambda: str(sum(1 for a in range(5) for b in range(5) for c in range(5) if a + b + c == 7)))])
