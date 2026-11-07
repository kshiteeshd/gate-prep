"""Engineering Mathematics — Discrete Maths part 1: Logic, Sets, Relations, Functions."""
import itertools
import math
from fractions import Fraction

from learn import Ex, lesson

S = "ENGM"

# ======================================================================================================
lesson(subject=S, chapter="Mathematical Logic", ch_no=1, no=1, slug="engm-logic-propositions", title="Propositions, Connectives & Truth Tables",
       topic="Propositional & First-Order Logic", minutes=16, weight=5, widget="truth",
       widget_hint="Type any formula (p, q, r, s with ! & | ^ -> <->). Compare two formulas to test logical equivalence instantly.",
       key="A proposition is a statement that is either true or false. Connectives (¬ ∧ ∨ → ↔) build bigger statements whose truth value is fixed by a truth table — and p → q is false in exactly ONE case: p true, q false.",
       analogy=("📜", "Think of implication as a promise",
                "“If you finish your homework, I will buy you ice cream.” The promise is **broken** only if you did the homework and got no ice cream. If you skipped the homework, nothing was promised — so whatever happens, the promise is not broken. That is exactly why p → q is true whenever p is false."),
       sections=[
           dict(h="What is a proposition?", md="""A **proposition** is a declarative sentence that is definitely true or definitely false (never both, never undecided).

- “2 + 3 = 5” — proposition (true).
- “Delhi is in Kerala” — proposition (false).
- “x + 1 = 4” — **not** a proposition: it depends on x. (It becomes one once we fix x, or quantify it — see the next lesson.)
- “Close the door!” and “Is it raining?” — not propositions (command / question).

We name propositions with letters **p, q, r, …** and combine them. With **n** different propositional variables there are **2ⁿ** possible truth assignments (rows of a truth table). This number appears in many GATE counting questions."""),
           dict(h="The six connectives", md="""| p | q | ¬p | p ∧ q | p ∨ q | p ⊕ q | p → q | p ↔ q |
|---|---|---|---|---|---|---|---|
| T | T | F | T | T | F | T | T |
| T | F | F | F | T | T | F | F |
| F | T | T | F | T | T | T | F |
| F | F | T | F | F | F | T | T |

Read them in plain English:

- **¬p** (not): flips the value.
- **p ∧ q** (and): true only if *both* are true.
- **p ∨ q** (or): *inclusive* — true if at least one is true.
- **p ⊕ q** (xor): true if *exactly one* is true.
- **p → q** (implies): false only for (T, F). “If p then q”, “p only if q”, “q whenever p” all mean p → q.
- **p ↔ q** (iff): true when p and q have the *same* value.""",
                formulas=[("p → q  ≡  ¬p ∨ q", "the definition you will use most"), ("p ↔ q  ≡  (p → q) ∧ (q → p)", "biconditional")],
                call=[("tip", "Remember the shape", "**Implication is false only in one row.** In every GATE problem about →, find that one row first.")]),
           dict(h="Converse, inverse, contrapositive", md="""Start from the implication **p → q**:

| Name | Form | Equivalent to p → q? |
|---|---|---|
| Converse | q → p | ✘ No |
| Inverse | ¬p → ¬q | ✘ No |
| **Contrapositive** | **¬q → ¬p** | **✔ Yes — always** |

Example: “If it rains, the match is cancelled.” Its contrapositive is “If the match is **not** cancelled, it did **not** rain” — says exactly the same thing. The converse “If the match is cancelled, it rained” does **not** follow (maybe it was cancelled for another reason).""",
                call=[("trap", "Most common mistake", "Treating the **converse** as if it were equivalent. Only the **contrapositive** is. The converse and the inverse are equivalent to *each other*, but not to the original.")]),
           dict(h="Equivalences you must know cold", md="""Two formulas are **logically equivalent (≡)** when they have the same truth value in every row.

| Law | Statement |
|---|---|
| Double negation | ¬¬p ≡ p |
| De Morgan | ¬(p ∧ q) ≡ ¬p ∨ ¬q   and   ¬(p ∨ q) ≡ ¬p ∧ ¬q |
| Implication | p → q ≡ ¬p ∨ q ≡ ¬q → ¬p |
| Negation of implication | ¬(p → q) ≡ p ∧ ¬q |
| Distributive | p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r) |
| Absorption | p ∨ (p ∧ q) ≡ p   and   p ∧ (p ∨ q) ≡ p |
| Biconditional | p ↔ q ≡ (p ∧ q) ∨ (¬p ∧ ¬q) |
| Xor | p ⊕ q ≡ (p ∨ q) ∧ ¬(p ∧ q) ≡ ¬(p ↔ q) |

A formula that is always true is a **tautology** (e.g. p ∨ ¬p), always false a **contradiction** (p ∧ ¬p), otherwise a **contingency** (satisfiable, but not valid). *Satisfiable* just means at least one row is true."""),
           dict(h="Normal forms, counting and completeness", md="""- **DNF** (disjunctive normal form): an OR of ANDs, e.g. (p ∧ q) ∨ (¬p ∧ r). Each true row of the truth table gives one AND term (a *minterm*).
- **CNF** (conjunctive normal form): an AND of ORs, e.g. (p ∨ q) ∧ (¬p ∨ r). Each false row gives one OR term (a *maxterm*).
- Number of distinct Boolean functions of n variables: **2^(2ⁿ)** (each of the 2ⁿ rows can be T or F). For n = 2 that is 16.
- A set of connectives is **functionally complete** if every formula can be built from it. {¬, ∧}, {¬, ∨}, {¬, →} and the single connective NAND are complete; **{∧, ∨} is not** (it can never produce a negation).

**Rules of inference** (valid argument forms, all tautologies in disguise):

| Rule | Form |
|---|---|
| Modus ponens | p, p → q ⊢ q |
| Modus tollens | ¬q, p → q ⊢ ¬p |
| Hypothetical syllogism | p → q, q → r ⊢ p → r |
| Disjunctive syllogism | p ∨ q, ¬p ⊢ q |
| Resolution | p ∨ q, ¬p ∨ r ⊢ q ∨ r |"""),
       ],
       examples=[
           Ex("Is the hypothetical syllogism a tautology?", "Decide whether  ((p → q) ∧ (q → r)) → (p → r)  is a tautology.",
              ["The only way an implication A → B fails is **A true and B false**. So try to make it fail: need (p → q) ∧ (q → r) true while p → r is false.",
               "p → r false forces **p = T and r = F**.",
               "Then p → q true forces q = T (since p = T). But then q → r = (T → F) = F, so the antecedent is false — contradiction.",
               "The formula can never fail, so it is **valid**."],
              "Yes — it is a **tautology**.", verify=lambda: "Yes" if all((not ((not p or q) and (not q or r))) or (not p or r) for p, q, r in itertools.product([0, 1], repeat=3)) else "No"),
           Ex("Counting satisfying assignments", "How many of the 8 assignments to p, q, r satisfy  (p ∨ q) ∧ (¬p ∨ r) ?",
              ["Split on p.", "If **p = F**: first clause needs q = T; second clause (¬p ∨ r) is already true. So q = T, r free → **2** assignments.",
               "If **p = T**: first clause already true; second needs r = T. q free → **2** assignments.", "Total = 2 + 2 = **4**."],
              "**4** of the 8 assignments.", verify=lambda: str(sum(1 for p, q, r in itertools.product([0, 1], repeat=3) if (p or q) and ((not p) or r)))),
           Ex("Negating an implication", "Write the negation of “If a program compiles, then it runs correctly.”",
              ["Let p = “compiles”, q = “runs correctly”. The statement is p → q.", "¬(p → q) ≡ ¬(¬p ∨ q) ≡ p ∧ ¬q (De Morgan).", "In words: “The program compiles **and** it does not run correctly.”"],
              "p ∧ ¬q : “It compiles but does not run correctly.”", verify=lambda: "p ∧ ¬q" if all((not (not p or q)) == (p and not q) for p, q in itertools.product([0, 1], repeat=2)) else "mismatch"),
           Ex("Which of these is equivalent to p → q?", "Choose all that are equivalent to p → q:  (a) ¬q → ¬p   (b) q → p   (c) ¬p ∨ q   (d) p ∧ ¬q",
              ["(a) contrapositive — equivalent ✔.", "(b) converse — not equivalent ✘ (they differ at p = F, q = T: p → q is true but q → p is false).", "(c) the definition of → — equivalent ✔.",
               "(d) is the *negation* of p → q, so it is the opposite ✘."],
              "(a) and (c).", verify=lambda: " and ".join("(%s)" % x for x, f in {"a": lambda p, q: q or not p, "b": lambda p, q: (not q) or p, "c": lambda p, q: (not p) or q, "d": lambda p, q: p and not q}.items() if all(bool(f(p, q)) == bool((not p) or q) for p, q in itertools.product([0, 1], repeat=2))) + "."),
       ],
       traps=[("Converse ≠ contrapositive", "p → q is equivalent to ¬q → ¬p, **not** to q → p. GATE loves offering the converse as an option."),
              ("Vacuous truth", "If p is false, p → q is **true** regardless of q. “If 1 = 2 then the moon is cheese” is a true statement."),
              ("Inclusive or", "In logic, p ∨ q is true when **both** are true. Everyday “or” is often exclusive — don't carry that habit into proofs."),
              ("Wrong De Morgan", "¬(p ∧ q) is ¬p **∨** ¬q — the connective flips. Writing ¬p ∧ ¬q is the most common slip.")],
       quick=[("Which of the following is **always** equivalent to p → q?", ["q → p", "¬q → ¬p", "¬p → ¬q", "p ∧ ¬q"], 1, "The contrapositive ¬q → ¬p is the only equivalent form; q → p and ¬p → ¬q are not, and p ∧ ¬q is the negation."),
              ("For how many of the 4 truth assignments to (p, q) is p → q false?", ["0", "1", "2", "3"], 1, "Only when p = T and q = F."),
              ("How many distinct Boolean functions of 3 variables exist?", ["8", "64", "256", "512"], 2, "2^(2³) = 2⁸ = 256."),
              ("Which set of connectives is NOT functionally complete?", ["{¬, ∧}", "{¬, →}", "{∧, ∨}", "{NAND}"], 2, "{∧, ∨} can never produce a negation (all its outputs are monotone).")],
       summary=["Proposition = statement with a definite truth value; n variables → 2ⁿ rows.", "p → q ≡ ¬p ∨ q; false only for p = T, q = F.", "Contrapositive ¬q → ¬p is equivalent; converse and inverse are not.",
                "De Morgan: ¬(p ∧ q) ≡ ¬p ∨ ¬q and ¬(p ∨ q) ≡ ¬p ∧ ¬q.", "Tautology = always true; contradiction = always false; contingency = in between.", "{∧, ∨} is not functionally complete; {¬,∧}, {¬,∨}, NAND are."])

# ======================================================================================================
lesson(subject=S, chapter="Mathematical Logic", ch_no=1, no=2, slug="engm-logic-quantifiers", title="Predicates, Quantifiers & Inference",
       topic="Propositional & First-Order Logic", minutes=15, weight=4, widget="none",
       key="A predicate P(x) becomes a proposition when we say *for all* x (∀) or *there exists* an x (∃). The order of nested quantifiers matters, and negating a quantifier swaps ∀ and ∃.",
       analogy=("🏫", "A class of students", "∀x Passed(x) says **every** student passed — one failure breaks it. ∃x Passed(x) says **at least one** student passed — one success is enough. To refute “everyone passed” you only need one counterexample; to refute “someone passed” you must check everybody."),
       sections=[
           dict(h="Predicates and the universe of discourse", md="""A **predicate** is a statement with a variable, e.g. P(x): “x is even”. It has no truth value until we choose x or quantify it.

The **domain** (universe of discourse) says which values x may take — always check it. “∀x (x² ≥ 0)” is true over the reals, while “∃x (x² = 2)” is true over ℝ but false over ℤ or ℚ.

- **Universal** ∀x P(x): P(x) holds for *every* x in the domain.
- **Existential** ∃x P(x): P(x) holds for *at least one* x.
- A variable that is quantified is **bound**; otherwise it is **free**. A formula with no free variables is a proposition (a *sentence*)."""),
           dict(h="Negation rules", md="""Move the negation inward and flip the quantifier:""",
                formulas=[("¬∀x P(x)  ≡  ∃x ¬P(x)", "“not everyone” = “someone doesn't”"), ("¬∃x P(x)  ≡  ∀x ¬P(x)", "“no one” = “everyone doesn't”")],
                call=[("tip", "Combine with De Morgan", "¬∀x (P(x) → Q(x)) ≡ ∃x (P(x) ∧ ¬Q(x)). In words: the negation of “all P are Q” is “some P is not Q”.")]),
           dict(h="Translating English — the two patterns you must remember", md="""| English | Logic |
|---|---|
| All dogs are mammals | ∀x (Dog(x) **→** Mammal(x)) |
| Some dogs are brown | ∃x (Dog(x) **∧** Brown(x)) |
| No dog is a cat | ∀x (Dog(x) → ¬Cat(x)) |
| Not all dogs bark | ∃x (Dog(x) ∧ ¬Bark(x)) |

**Rule of thumb:** ∀ goes with **→**, ∃ goes with **∧**.

Why? ∀x (Dog(x) ∧ Mammal(x)) would claim *everything* is a dog — absurd. And ∃x (Dog(x) → Mammal(x)) is true even if no dogs exist (pick any non-dog, the implication is vacuously true) — so it says almost nothing.""",
                call=[("trap", "GATE favourite", "∀x (P(x) → Q(x)) is **not** the same as (∀x P(x)) → (∀x Q(x)). The first is much stronger-per-element; the second only compares the two global statements.")]),
           dict(h="Nested quantifiers — order matters", md="""Take the domain of people and L(x, y): “x loves y”.

- **∀x ∃y L(x, y)**: everybody loves *someone* (the beloved may differ per person).
- **∃y ∀x L(x, y)**: there is *one person loved by everybody*.
- **∃x ∀y L(x, y)**: someone loves everybody.
- **∀y ∃x L(x, y)**: everybody is loved by *someone*.

The strong form implies the weak one but **not conversely**:""",
                formulas=[("∃x ∀y P(x,y)  →  ∀y ∃x P(x,y)", "valid"), ("∀x ∃y P(x,y)  →  ∃y ∀x P(x,y)", "NOT valid in general")],
                call=[("tip", "Same-type quantifiers commute", "∀x∀y ≡ ∀y∀x and ∃x∃y ≡ ∃y∃x. Only mixed ∀/∃ pairs are order sensitive.")]),
           dict(h="Quantifier laws and inference", md="""- ∀x (P ∧ Q) ≡ (∀x P) ∧ (∀x Q) — ∀ distributes over ∧.
- ∃x (P ∨ Q) ≡ (∃x P) ∨ (∃x Q) — ∃ distributes over ∨.
- ∀x P ∨ ∀x Q → ∀x (P ∨ Q) is valid, but **not** the reverse.
- ∃x (P ∧ Q) → ∃x P ∧ ∃x Q is valid, but **not** the reverse.

**Inference rules:** *Universal instantiation* (from ∀x P(x) conclude P(c)); *Existential generalisation* (from P(c) conclude ∃x P(x)); *Universal generalisation* (P(c) for arbitrary c ⊢ ∀x P(x)); *Existential instantiation* (∃x P(x) ⊢ P(c) for a fresh c)."""),
       ],
       examples=[
           Ex("Evaluate on a finite domain", "Domain {1,2,3}, R = {(1,2),(2,3),(3,1)}. Is ∀x ∃y R(x, y) true? Is ∃y ∀x R(x, y) true?",
              ["∀x ∃y: x = 1 → y = 2 ✔, x = 2 → y = 3 ✔, x = 3 → y = 1 ✔. Every x has some y, so the statement is **true**.",
               "∃y ∀x: for y = 1 we need R(1,1), R(2,1), R(3,1) — only R(3,1) holds. Similarly y = 2 and y = 3 fail. So it is **false**.",
               "This is the standard example showing ∀∃ does **not** imply ∃∀."],
              "∀x ∃y R(x,y) is **true**; ∃y ∀x R(x,y) is **false**.",
              verify=lambda: "∀x ∃y R(x,y) is %s; ∃y ∀x R(x,y) is %s." % tuple(str(v).lower() for v in (all(any((x, y) in {(1, 2), (2, 3), (3, 1)} for y in (1, 2, 3)) for x in (1, 2, 3)), any(all((x, y) in {(1, 2), (2, 3), (3, 1)} for x in (1, 2, 3)) for y in (1, 2, 3))))),
           Ex("Negate a quantified statement", "Negate: “Every student who studies passes.”",
              ["Write it as ∀x (Studies(x) → Passes(x)).", "Negate: ∃x ¬(Studies(x) → Passes(x)).", "Use ¬(A → B) ≡ A ∧ ¬B: ∃x (Studies(x) ∧ ¬Passes(x))."],
              "“Some student studies but does not pass.”"),
           Ex("Translate and check validity", "Is the argument valid? “All engineers are logical. Rita is an engineer. Therefore Rita is logical.”",
              ["∀x (E(x) → L(x))  and  E(r).", "Universal instantiation: E(r) → L(r).", "Modus ponens with E(r): **L(r)**. The argument is valid."],
              "Valid (universal instantiation + modus ponens)."),
       ],
       traps=[("∀ with ∧, ∃ with →", "Writing ∀x (Dog(x) ∧ Mammal(x)) or ∃x (Dog(x) → Mammal(x)) is the classic wrong translation."),
              ("Swapping ∀∃ order", "∀x∃y P ≠ ∃y∀x P. Test with a relation where each x has a different partner."),
              ("Forgetting the domain", "Always read the domain. An ∃ statement can flip from true to false when the domain shrinks."),
              ("Negating only one half", "¬∀x P(x) is ∃x ¬P(x), **not** ∀x ¬P(x). “Not everyone passed” ≠ “everyone failed”.")],
       quick=[("¬∀x (P(x) → Q(x)) is equivalent to", ["∀x (P(x) ∧ ¬Q(x))", "∃x (P(x) ∧ ¬Q(x))", "∃x (¬P(x) → ¬Q(x))", "∀x (¬P(x) ∨ Q(x))"], 1, "Negate ∀ → ∃, then ¬(P → Q) ≡ P ∧ ¬Q."),
              ("“No bird is a mammal” in logic:", ["∃x (B(x) ∧ M(x))", "∀x (B(x) → ¬M(x))", "∀x (B(x) ∧ ¬M(x))", "¬∀x (B(x) → M(x))"], 1, "No B is M means every B is a non-M."),
              ("Which implication is valid?", ["∀x∃y P(x,y) → ∃y∀x P(x,y)", "∃x∀y P(x,y) → ∀y∃x P(x,y)", "∀x P(x) ∨ ∀x Q(x) ← ∀x (P(x) ∨ Q(x))", "∃x P(x) ∧ ∃x Q(x) → ∃x (P(x) ∧ Q(x))"], 1, "One person loving everyone means everyone is loved by someone. The others are invalid."),
              ("Over an empty domain, ∀x P(x) is", ["false", "true (vacuously)", "undefined", "equal to ∃x P(x)"], 1, "There is no counterexample, so it holds vacuously; ∃x P(x) is false.")],
       summary=["∀ ↔ ∃ under negation: ¬∀x P ≡ ∃x ¬P and ¬∃x P ≡ ∀x ¬P.", "Translate with ∀ + →  and ∃ + ∧.", "Order of mixed quantifiers matters; ∃∀ is stronger than ∀∃.", "∀ distributes over ∧, ∃ distributes over ∨ (only).",
                "Rules: universal/existential instantiation and generalisation; modus ponens still applies.", "Always check the domain — empty domain makes ∀ true and ∃ false."])

# ======================================================================================================
def _pie_100():
    return sum(1 for n in range(1, 101) if n % 2 == 0 or n % 3 == 0 or n % 5 == 0)


lesson(subject=S, chapter="Sets, Relations & Functions", ch_no=2, no=1, slug="engm-sets-counting", title="Sets, Power Sets & Inclusion–Exclusion",
       topic="Sets, Relations & Functions", minutes=14, weight=4, widget="venn",
       widget_hint="Enter the sizes of A, B, C and their overlaps; the Venn diagram fills in every region and gives |A ∪ B ∪ C|.",
       key="Counting elements of a union of overlapping sets: add the sets, subtract the pairwise overlaps, add back the triple overlap, and so on (inclusion–exclusion). A set with n elements has 2ⁿ subsets.",
       analogy=("🎟️", "Club memberships", "A school has a chess club and a music club. Adding the two membership lists counts students in **both** clubs twice — so subtract the overlap once. With three clubs you over-subtract the triple overlap, so you add it back. That is the whole principle."),
       sections=[
           dict(h="Sets and the basic operations", md="""A **set** is an unordered collection of distinct objects. Basic operations on subsets of a universe U:

- **Union** A ∪ B, **intersection** A ∩ B, **difference** A − B (in A but not B), **complement** Aᶜ = U − A.
- **Symmetric difference** A Δ B = (A − B) ∪ (B − A) — elements in exactly one of the two.
- **Subset** A ⊆ B; **proper subset** A ⊂ B. **Disjoint** means A ∩ B = ∅.
- **Cartesian product** A × B = all ordered pairs (a, b). Its size is **|A|·|B|**.

**Set De Morgan laws:** (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ and (A ∩ B)ᶜ = Aᶜ ∪ Bᶜ. Distributive: A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C).""",
                formulas=[("|A × B| = |A|·|B|", "Cartesian product"), ("|P(A)| = 2^|A|", "number of subsets (power set)")]),
           dict(h="Power sets and counting subsets", md="""The **power set** P(A) is the set of all subsets of A (including ∅ and A itself). For |A| = n: |P(A)| = **2ⁿ** — each element is either in or out.

Useful counts for |A| = n:

- subsets of size k: **C(n, k)**,
- non-empty subsets: 2ⁿ − 1, proper subsets: 2ⁿ − 1, non-empty proper subsets: 2ⁿ − 2,
- ordered pairs of subsets (X, Y) with X ⊆ Y: **3ⁿ** (each element is in neither, in Y only, or in both).""",
                call=[("tip", "Binary trick", "Subsets of {a, b, c} correspond to 3-bit strings: 101 means {a, c}. This is why the answer is 2ⁿ.")]),
           dict(h="Inclusion–exclusion principle", md="""For two sets: |A ∪ B| = |A| + |B| − |A ∩ B|.

For three sets:""",
                formulas=[("|A∪B∪C| = |A|+|B|+|C| − |A∩B| − |B∩C| − |A∩C| + |A∩B∩C|", "memorise the alternating signs")],
                call=[("key", "General rule", "Add all singles, subtract all pairs, add all triples, subtract all quadruples, … Signs alternate with the number of sets intersected.")]),
           dict(h="The typical GATE use: divisibility counting", md="""“How many integers in 1..N are divisible by a or b?” Use floors:

|A| = ⌊N/a⌋, |B| = ⌊N/b⌋, |A ∩ B| = ⌊N/lcm(a, b)⌋. Careful: the overlap uses the **lcm**, not the product, when a and b share a factor.

“Divisible by neither” = N − |A ∪ B|. “Divisible by exactly one” = |A| + |B| − 2|A ∩ B|."""),
       ],
       examples=[
           Ex("Divisible by 2, 3 or 5", "How many integers from 1 to 100 are divisible by at least one of 2, 3, 5?",
              ["|A₂| = 50, |A₃| = 33, |A₅| = 20.", "Pairs: |A₂∩A₃| = ⌊100/6⌋ = 16, |A₂∩A₅| = ⌊100/10⌋ = 10, |A₃∩A₅| = ⌊100/15⌋ = 6.", "Triple: ⌊100/30⌋ = 3.", "Total = 50 + 33 + 20 − 16 − 10 − 6 + 3 = **74**."],
              "**74**", verify=lambda: str(_pie_100())),
           Ex("Survey problem", "In a group of 100 people, 60 like tea, 50 like coffee and 20 like neither. How many like both?",
              ["People who like at least one drink = 100 − 20 = 80.", "|T ∪ C| = |T| + |C| − |T ∩ C| ⇒ 80 = 60 + 50 − |T ∩ C|.", "|T ∩ C| = 110 − 80 = **30**."],
              "**30**", verify=lambda: str(60 + 50 - (100 - 20))),
           Ex("Counting pairs of nested subsets", "A has 4 elements. How many ordered pairs (X, Y) of subsets satisfy X ⊆ Y ⊆ A?",
              ["Each element has three independent options: not in Y (so not in X), in Y but not in X, or in both.", "That gives 3 choices per element, so 3⁴ = **81** pairs."],
              "**81**", verify=lambda: str(sum(1 for X in range(16) for Y in range(16) if X & Y == X))),
       ],
       traps=[("Using the product instead of the lcm", "Numbers divisible by both 4 and 6 are counted with lcm = 12, not 24."),
              ("Forgetting to add back the triple overlap", "Three-set inclusion–exclusion ends with **+** |A ∩ B ∩ C|."),
              ("Power set size", "|P(A)| = 2ⁿ, not n² or n!. Non-empty proper subsets are 2ⁿ − 2."),
              ("Confusing ⊂ and ∈", "{1} ⊆ {1,2} but 1 ∈ {1,2}. And ∅ is a subset of every set, but ∅ ∈ A only if A contains it as an element.")],
       quick=[("A has 5 elements. How many subsets does it have?", ["10", "25", "32", "120"], 2, "2⁵ = 32."),
              ("|A| = 8, |B| = 5, |A ∩ B| = 3. Then |A ∪ B| is", ["10", "13", "16", "11"], 0, "8 + 5 − 3 = 10."),
              ("How many integers from 1 to 60 are divisible by 4 or 6?", ["25", "20", "15", "30"], 1, "15 + 10 − 5 (lcm 12 → ⌊60/12⌋ = 5) = 20."),
              ("|A × B| when |A| = 3 and |B| = 4 is", ["7", "12", "81", "64"], 1, "3 × 4 = 12.")],
       summary=["|P(A)| = 2ⁿ; non-empty proper subsets = 2ⁿ − 2.", "|A × B| = |A||B|.", "Inclusion–exclusion: alternate signs; overlaps of divisibility use the lcm.",
                "Set De Morgan: complement of union = intersection of complements.", "Exactly-one count = |A| + |B| − 2|A ∩ B|.", "Pairs X ⊆ Y ⊆ A: 3ⁿ."])

# ======================================================================================================
def _bell(n):
    b = [1]
    for i in range(n):
        b.append(sum(math.comb(i, k) * b[k] for k in range(i + 1)))
    return b[n]


def _tc(pairs, n):
    R = set(pairs)
    ch = True
    while ch:
        ch = False
        for (a, b) in list(R):
            for (c, d) in list(R):
                if b == c and (a, d) not in R:
                    R.add((a, d)); ch = True
    return len(R)


lesson(subject=S, chapter="Sets, Relations & Functions", ch_no=2, no=2, slug="engm-relations", title="Relations: Properties, Closures & Equivalence",
       topic="Sets, Relations & Functions", minutes=18, weight=5, widget="relation",
       widget_hint="Click cells to build a relation on {1,2,3,4}. The tool tells you instantly which of the properties hold, and lets you take closures.",
       key="A relation on a set A is a set of ordered pairs. Four properties (reflexive, symmetric, antisymmetric, transitive) classify it — reflexive + symmetric + transitive is an equivalence relation (partitions the set); reflexive + antisymmetric + transitive is a partial order.",
       analogy=("🤝", "Who is related to whom?", "Picture a social network on n people. “x is a friend of y” is a relation. If friendship is mutual it is *symmetric*; if everyone counts as their own friend it is *reflexive*; if “a friend of my friend is my friend” it is *transitive*. When all three hold, the network splits into separate friend-groups — the equivalence classes."),
       sections=[
           dict(h="Definition and representation", md="""A **binary relation** R on a set A is a subset of A × A. We write aRb or (a, b) ∈ R.

Two handy views for a finite set with n elements:

- **Matrix:** an n × n 0/1 matrix, entry (i, j) = 1 iff (i, j) ∈ R.
- **Digraph:** an arrow i → j for each pair.

There are 2^(n²) relations on an n-element set (each of the n² pairs is in or out)."""),
           dict(h="The four properties", md="""| Property | Meaning | Matrix test |
|---|---|---|
| **Reflexive** | (a, a) ∈ R for **every** a | all diagonal entries are 1 |
| **Irreflexive** | (a, a) ∉ R for every a | all diagonal entries are 0 |
| **Symmetric** | (a, b) ∈ R ⇒ (b, a) ∈ R | matrix equals its transpose |
| **Antisymmetric** | (a, b) and (b, a) ∈ R ⇒ a = b | no pair of 1s mirrored off the diagonal |
| **Asymmetric** | (a, b) ∈ R ⇒ (b, a) ∉ R | antisymmetric **and** irreflexive |
| **Transitive** | (a, b), (b, c) ∈ R ⇒ (a, c) ∈ R | M² ≤ M (entrywise) |

Note that **symmetric and antisymmetric are not opposites**: the identity relation is both; a relation can be neither.""",
                call=[("trap", "Vacuous cases", "The empty relation on a non-empty set is symmetric, antisymmetric and transitive (vacuously) but **not** reflexive. Always test the definition, not your intuition.")]),
           dict(h="Equivalence relations and partitions", md="""An **equivalence relation** is reflexive, symmetric and transitive. It splits A into disjoint **equivalence classes** [a] = {x : xRa}, and every partition of A gives back an equivalence relation. So:

> number of equivalence relations on an n-set = number of partitions of the set = **Bell number Bₙ**.

B₀…B₅ = 1, 1, 2, 5, 15, 52. Example: “same remainder mod 3” on the integers has exactly 3 classes.""",
                formulas=[("B_n : 1, 1, 2, 5, 15, 52, 203, 877", "Bell numbers"), ("# relations: reflexive 2^(n²−n), symmetric 2^(n(n+1)/2), antisymmetric 2ⁿ·3^(n(n−1)/2)", "counting formulas")]),
           dict(h="Closures and partial orders", md="""The **closure** of R with respect to a property is the smallest relation containing R that has that property:

- **Reflexive closure:** R ∪ {(a, a)}.
- **Symmetric closure:** R ∪ R⁻¹.
- **Transitive closure R⁺:** keep adding (a, c) whenever (a, b), (b, c) ∈ R — computed by **Warshall's algorithm** in O(n³).

A **partial order (poset)** is reflexive, **antisymmetric**, transitive (e.g. ≤, ⊆, divisibility). A **total order** also makes every pair comparable. (Posets get their own lesson.)"""),
       ],
       examples=[
           Ex("Number of equivalence relations", "How many equivalence relations exist on a set of 4 elements?",
              ["Equivalence relations ↔ partitions. Count partitions of a 4-set by block structure.", "1 block: 1 way. Blocks 3+1: C(4,1) = 4. Blocks 2+2: 3. Blocks 2+1+1: C(4,2) = 6. Blocks 1+1+1+1: 1.", "Total = 1 + 4 + 3 + 6 + 1 = **15** (the Bell number B₄)."],
              "**15**", verify=lambda: str(_bell(4))),
           Ex("Which properties does the relation have?", "On A = {1,2,3}, R = {(1,1),(2,2),(3,3),(1,2),(2,1)}. List its properties.",
              ["Reflexive: (1,1),(2,2),(3,3) ∈ R ✔.", "Symmetric: (1,2) ∈ R and (2,1) ∈ R ✔ (diagonal pairs are self-symmetric).", "Antisymmetric: (1,2) and (2,1) both present with 1 ≠ 2 ✘.",
               "Transitive: check pairs (1,2),(2,1) → (1,1) ✔; (2,1),(1,2) → (2,2) ✔; (1,2),(2,2) → (1,2) ✔; all others fine ✔.", "So R is reflexive, symmetric and transitive — an **equivalence relation** with classes {1,2} and {3}."],
              "Reflexive, symmetric, transitive (an equivalence relation); **not** antisymmetric.", verify=lambda: "equivalence"),
           Ex("Size of a transitive closure", "R = {(1,2),(2,3),(3,4)} on {1,2,3,4}. How many ordered pairs are in its transitive closure?",
              ["Start: (1,2),(2,3),(3,4).", "Add (1,3) from (1,2),(2,3); add (2,4) from (2,3),(3,4); then add (1,4) from (1,3),(3,4).", "Total = 3 + 3 = **6** pairs."],
              "**6**", verify=lambda: str(_tc([(1, 2), (2, 3), (3, 4)], 4))),
           Ex("Counting symmetric relations", "How many symmetric relations exist on a 4-element set?",
              ["A symmetric relation is determined by its diagonal (4 pairs) and the unordered off-diagonal pairs C(4,2) = 6.", "That is 4 + 6 = 10 independent yes/no choices.", "Number = 2¹⁰ = **1024** (formula 2^(n(n+1)/2) with n = 4)."],
              "**1024**", verify=lambda: str(2 ** (4 * 5 // 2))),
       ],
       traps=[("Reflexive needs EVERY diagonal pair", "One missing (a, a) ruins it — even for an element that appears in no other pair of the set A."),
              ("Symmetric vs antisymmetric", "They are independent. The identity is both; {(1,2),(2,1)} is symmetric only; {(1,2)} is antisymmetric only."),
              ("Forgetting the elements outside any pair", "If A = {1,2,3} and R = {(1,1),(2,2)}, R is **not** reflexive on A because (3,3) is missing."),
              ("Equivalence ≠ one class", "Equivalence relations can have many classes; every element lies in exactly one class.")],
       quick=[("Which relation on {1,2,3} is an equivalence relation?", ["{(1,1),(2,2),(3,3)}", "{(1,2),(2,1)}", "{(1,1),(1,2)}", "∅"], 0, "The identity is reflexive, symmetric and transitive."),
              ("Number of reflexive relations on a 4-element set:", ["2¹⁶", "2¹²", "2⁴", "4!"], 1, "Diagonal is forced; the other 16 − 4 = 12 pairs are free: 2¹²."),
              ("‘x divides y’ on the positive integers is", ["an equivalence relation", "a partial order", "symmetric", "irreflexive"], 1, "Reflexive, antisymmetric and transitive ⇒ partial order."),
              ("A relation that is both symmetric and antisymmetric must be", ["empty or a subset of the identity", "the whole A × A", "reflexive", "total"], 0, "Any off-diagonal pair would violate one of the two properties.")],
       summary=["Relation on A = subset of A × A; there are 2^(n²) of them.", "Equivalence = reflexive + symmetric + transitive ⇒ partition into classes; count = Bell number.", "Partial order = reflexive + antisymmetric + transitive.",
                "Counts: reflexive 2^(n²−n), symmetric 2^(n(n+1)/2), antisymmetric 2ⁿ·3^(n(n−1)/2), asymmetric 3^(n(n−1)/2).", "Transitive closure by Warshall in O(n³).", "Symmetric and antisymmetric are independent properties."])

# ======================================================================================================
def _onto(m, n):
    return sum((-1) ** i * math.comb(n, i) * (n - i) ** m for i in range(n + 1))


lesson(subject=S, chapter="Sets, Relations & Functions", ch_no=2, no=3, slug="engm-functions", title="Functions: One-to-one, Onto & Counting",
       topic="Sets, Relations & Functions", minutes=15, weight=4, widget="counting",
       widget_hint="Use the calculator for P(n,k), C(n,k) and factorials — the same numbers that count functions.",
       key="A function f: A → B assigns each element of A exactly one element of B. One-to-one (injective) means no two inputs share an output; onto (surjective) means every element of B is hit; both = bijection, which is exactly when an inverse exists.",
       analogy=("🎓", "Students and seats", "Functions A → B: each student (A) picks exactly one seat (B). *One-to-one*: no two students share a seat. *Onto*: no seat is left empty. *Bijection*: perfect pairing — everyone has their own seat and every seat is used (only possible when the counts match)."),
       sections=[
           dict(h="Definition, domain, codomain, range", md="""A function f: A → B sends **every** element of A (the *domain*) to **exactly one** element of B (the *codomain*). The **range** (image) is the set of values actually taken: f(A) ⊆ B.

A relation fails to be a function if some a has **no** image or **more than one**. (Vertical line test.)"""),
           dict(h="Injective, surjective, bijective", md="""- **One-to-one (injective):** f(x) = f(y) ⇒ x = y. Needs |A| ≤ |B|.
- **Onto (surjective):** for every b ∈ B there is some a with f(a) = b. Needs |A| ≥ |B|.
- **Bijective:** both. Then |A| = |B| and f has an inverse f⁻¹.

Examples on the reals: f(x) = 2x + 1 is a bijection; f(x) = x² is neither (f(2) = f(−2); negatives never hit); f(x) = eˣ is one-to-one but not onto ℝ (never ≤ 0).""",
                call=[("tip", "Finite sets shortcut", "For |A| = |B| finite: injective ⇔ surjective ⇔ bijective. For different sizes this equivalence fails.")]),
           dict(h="Counting functions between finite sets", md="""Let |A| = m and |B| = n.""",
                formulas=[("all functions: n^m", "each of m inputs chooses among n outputs"), ("one-to-one: P(n, m) = n!/(n−m)!", "needs m ≤ n"), ("onto: Σ (−1)^i C(n,i) (n−i)^m", "inclusion–exclusion; needs m ≥ n"), ("bijections (m = n): n!", "")],
                call=[("key", "Onto counts to remember", "Onto functions from an m-set to a 2-set: 2^m − 2. Onto from 4 to 3: 36. From 5 to 3: 150. From 5 to 2: 30.")]),
           dict(h="Composition and inverse", md="""The composition (g∘f)(x) = g(f(x)). Facts GATE tests:

- If g∘f is **injective** then **f** is injective (but g need not be).
- If g∘f is **surjective** then **g** is surjective (but f need not be).
- Composition of bijections is a bijection; (g∘f)⁻¹ = f⁻¹∘g⁻¹ (order reverses). Think of putting on socks then shoes: to undo, remove the shoes first.
- Composition is associative but **not commutative**.

**Pigeonhole link:** if |A| > |B| no function A → B can be one-to-one.

**Special functions worth knowing:** the *identity* function (maps every x to itself, a bijection), a *constant* function (neither injective nor surjective unless the sets are tiny), and the *characteristic function* of a subset S ⊆ U (1 if x ∈ S else 0) — which is why subsets of an n-set correspond to the 2ⁿ functions U → {0, 1}."""),
       ],
       examples=[
           Ex("Onto functions", "How many onto (surjective) functions are there from a 5-element set to a 3-element set?",
              ["Inclusion–exclusion over the 3 target elements that might be missed.", "Total functions 3⁵ = 243. Subtract those missing at least one target: 3·2⁵ = 96. Add back those missing two: 3·1⁵ = 3.", "243 − 96 + 3 = **150**."],
              "**150**", verify=lambda: str(_onto(5, 3))),
           Ex("One-to-one functions", "How many one-to-one functions exist from a 3-element set to a 5-element set?",
              ["First element has 5 choices, second 4 (cannot reuse), third 3.", "5 × 4 × 3 = **60** = P(5,3)."],
              "**60**", verify=lambda: str(math.perm(5, 3))),
           Ex("Composition and injectivity", "f: A → B and g: B → C with g∘f injective. Must g be injective? Must f?",
              ["Suppose f(x) = f(y). Then g(f(x)) = g(f(y)), so by injectivity of g∘f, x = y. Hence **f is injective**.", "But g need not be: let A = {1}, B = {1,2}, C = {c}, f(1) = 1, g(1) = g(2) = c. Then g∘f is injective while g is not."],
              "f must be injective; g need not be."),
       ],
       traps=[("Mixing up injective and surjective in compositions", "g∘f injective ⇒ **f** injective. g∘f surjective ⇒ **g** surjective. Easy to swap."),
              ("Counting injections as nᵐ", "One-to-one needs falling factorial n(n−1)…(n−m+1), not nᵐ."),
              ("Assuming x² is a bijection", "Over ℝ it is neither; over the non-negative reals it is a bijection onto the non-negative reals."),
              ("Onto needs |A| ≥ |B|", "No onto function exists from a 3-set to a 5-set — the formula gives 0.")],
       quick=[("Number of functions from a 3-element set to a 4-element set:", ["12", "64", "81", "24"], 1, "4³ = 64."),
              ("A function from a 6-element set to a 4-element set can be", ["one-to-one", "onto", "a bijection", "neither one-to-one nor onto is impossible"], 1, "Since 6 > 4 it cannot be one-to-one, but it can be onto."),
              ("If g∘f is onto, then", ["f is onto", "g is onto", "both are onto", "both are one-to-one"], 1, "Every output of g∘f is an output of g."),
              ("Onto functions from a 4-set to a 2-set:", ["16", "14", "8", "12"], 1, "2⁴ − 2 = 14.")],
       summary=["Function: every input has exactly one output.", "Injective: no collisions; surjective: nothing missed; bijective: both ⇒ inverse exists.", "Counts: all nᵐ; injective P(n,m); bijections n!; onto by inclusion–exclusion.",
                "g∘f injective ⇒ f injective; g∘f surjective ⇒ g surjective.", "|A| > |B| ⇒ no injection (pigeonhole).", "(g∘f)⁻¹ = f⁻¹∘g⁻¹."])
