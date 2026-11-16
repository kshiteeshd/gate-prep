"""Engineering Mathematics · Section 1 Discrete Mathematics · Chapter 1 Propositional & First-Order Logic."""
import itertools

from content import g_engm2 as G2
from learn import Ex
from learn.author import Author

A = Author("ENGM")
A.section("Discrete Mathematics")
A.chapter("Propositional & First-Order Logic")
B3 = list(itertools.product((0, 1), repeat=3))
B2 = list(itertools.product((0, 1), repeat=2))

# ------------------------------------------------------------------------------------------------ 1.1
A.lesson("engm-logic-propositions", "Propositions, connectives and truth tables",
         key="Logic starts from statements that are true or false. Connectives combine them, and a truth table lists the value of a combined statement for every possible assignment, so any question about one formula can be answered by reading its table.",
         analogy=("💡", "Switches and bulbs", "Each proposition is a switch that is on (true) or off (false). A formula is a circuit of switches: the truth table lists every way the switches can be set and whether the bulb lights."),
         defs=[("Proposition", "A declarative statement that is either true or false, but not both."),
               ("Connective", "An operator that builds a compound proposition from simpler ones: ¬, ∧, ∨, →, ↔, ⊕."),
               ("Truth table", "A table giving the value of a formula for each of the 2ⁿ assignments to its n variables."),
               ("Boolean function", "A function from {0, 1}ⁿ to {0, 1}; every formula in n variables defines one.")],
         parts=[dict(h="Statements and variables", md="""A **proposition** makes a claim that can be judged true or false: "7 is prime" is a proposition; "close the door" and "x + 1 = 5" (until x is fixed) are not. Letters p, q, r stand for propositions and each takes the value 1 (true) or 0 (false).

Compound statements are built with connectives. Read each as an everyday word, with one precision: **or is inclusive** in logic (true when either or both sides hold)."""),
                 dict(h="The six connectives", md="""| p | q | ¬p | p ∧ q | p ∨ q | p → q | p ↔ q | p ⊕ q |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 1 | 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| 1 | 1 | 0 | 1 | 1 | 1 | 1 | 0 |

- **∧ (and)** is true only when both sides are true; **∨ (or)** is false only when both are false.
- **→ (implies)** is false only for p = 1, q = 0. A false hypothesis makes the implication true.
- **↔** is true when p and q have the same value; **⊕ (exclusive or)** is true when they differ, so p ⊕ q ≡ ¬(p ↔ q).

When brackets are missing, apply ¬ first, then ∧, then ∨, then →, then ↔."""),
                 dict(h="Building a truth table", md="""1. List the variables and write the 2ⁿ rows in binary order (000, 001, …, 111 for n = 3).
2. Add one column for every sub-formula, working from the innermost brackets outwards.
3. The last column is the formula; read off the rows you need.

A formula in n variables has **2ⁿ rows**, and there are **2^(2ⁿ) different Boolean functions** of n variables, because each row of the table may independently hold 0 or 1. For n = 2 that is 16 functions; for n = 3 it is 256."""),
                 dict(h="Counting rows with a given value", md="""Many GATE questions ask "for how many assignments is the formula true?". Do not write the whole table: fix the variables that decide the answer first.

- p ∧ q ∧ r is true in exactly 1 of 8 rows; p ∨ q ∨ r is false in exactly 1 of 8.
- An exclusive or of n variables is true when an odd number of them are 1: exactly half of the 2ⁿ rows.
- Variables that do not appear in the formula still double the number of rows.""")],
         examples=[
             Ex("Reading a table", "For how many of the 8 assignments of (p, q, r) is (p ∨ q) ∧ ¬r true?",
                ["¬r forces r = 0, which leaves 4 rows.", "Among those, p ∨ q is false only for p = q = 0, so 3 rows remain.", "The formula is true in **3** assignments."], "**3**",
                verify=lambda: str(sum(1 for p, q, r in B3 if (p or q) and not r))),
             Ex("Biconditional and XOR", "Show that p ↔ ¬q has the same table as p ⊕ q.", ["p ↔ ¬q is true when p equals ¬q, i.e. when p and q differ.", "p ⊕ q is true exactly when p and q differ, so the two columns are identical."], "They agree in all 4 rows, so **p ↔ ¬q ≡ p ⊕ q**.",
                verify=lambda: "They agree in all %d rows, so p ↔ ¬q ≡ p ⊕ q" % sum(1 for p, q in B2 if (p == (not q)) == (p != q))),
             Ex("Number of functions", "How many Boolean functions of 3 variables exist, and how many have exactly one 1 in their table?", ["The table has 2³ = 8 rows and each row holds 0 or 1: 2⁸ = 256 functions.", "A function with exactly one 1 is fixed by choosing the row: 8 functions."], "**256** functions; **8** of them have a single 1.",
                verify=lambda: "%d functions; %d of them have a single 1" % (2 ** 8, 8)),
             Ex("Exclusive or of three", "For how many assignments of (p, q, r) is p ⊕ q ⊕ r true?", ["The value is 1 when an odd number of variables are 1.", "Exactly one 1: 3 rows. All three 1: 1 row. Total 3 + 1 = **4**, which is half of 8."], "**4**",
                verify=lambda: str(sum(1 for t in B3 if sum(t) % 2))),
             Ex("GATE style: implication chain", "How many of the 8 assignments of (p, q, r) make (p → q) ∧ (q → r) true?", ["Allowed (p, q, r): p → q forbids (1, 0, ·); q → r forbids (·, 1, 0).", "The remaining rows are 000, 001, 011, 111: 4 rows."], "**4**",
                verify=lambda: str(sum(1 for p, q, r in B3 if ((not p) or q) and ((not q) or r))))],
         traps=[("Implication with a false premise", "p → q is true whenever p is false. 'If 2 + 2 = 5 then the moon is cheese' is true."),
                ("Exclusive or versus or", "p ∨ q is true when both are true; p ⊕ q is false then."),
                ("Rows versus functions", "A formula in n variables has 2ⁿ rows, but there are 2^(2ⁿ) functions."),
                ("Missing brackets", "p ∨ q ∧ r means p ∨ (q ∧ r), because ∧ binds tighter than ∨.")],
         quick=[("p → q is false exactly when", ["p = 0, q = 0", "p = 0, q = 1", "p = 1, q = 0", "p = 1, q = 1"], 2, "True hypothesis, false conclusion is the only failing case."),
                ("The truth table of a formula in 4 variables has", ["8 rows", "16 rows", "32 rows", "64 rows"], 1, "2⁴ = 16."),
                ("p ⊕ q is equivalent to", ["p ↔ q", "¬(p ↔ q)", "p → q", "p ∧ q"], 1, "Exclusive or is true exactly when the values differ."),
                ("For how many of the 4 rows is p ∨ q true?", ["1", "2", "3", "4"], 2, "Only (0, 0) makes it false.")],
         summary=["A proposition is a statement that is true or false, never both.", "∨ is inclusive; ⊕ excludes the case where both are true.", "p → q is false only when p is true and q is false.", "An n-variable formula has 2ⁿ rows and there are 2^(2ⁿ) Boolean functions of n variables.", "Count true rows by fixing the deciding variables first; unused variables double the count."],
         subs=["Boolean functions count", "Logical forms"], widget="truth", hint="Type a formula and watch the truth table fill in, one row per assignment.", weight=5)

# ------------------------------------------------------------------------------------------------ 1.2
A.lesson("engm-lg-forms", "Implication, converse and contrapositive",
         key="Four statements can be made from P → Q. Only the contrapositive ¬Q → ¬P says the same thing; the converse and the inverse say something else. The negation of an implication is the single case P ∧ ¬Q.",
         analogy=("🤝", "A promise", "'If you pass, I will treat you.' The promise is broken in exactly one situation: you pass and I do not treat you. If you fail, the promise holds whatever I do."),
         defs=[("Implication P → Q", "A statement that is false only when the hypothesis P is true and the conclusion Q is false."),
               ("Converse and inverse", "Of P → Q these are Q → P and ¬P → ¬Q."),
               ("Contrapositive", "¬Q → ¬P, which is logically equivalent to P → Q."),
               ("Vacuous truth", "An implication with a false hypothesis is true, whatever the conclusion.")],
         parts=[dict(h="What an implication says", md="""P → Q claims: *whenever P holds, Q holds*. It is refuted by exactly one situation, P true and Q false. Therefore

$$P \\to Q \\;\\equiv\\; \\neg P \\lor Q \\qquad\\text{and}\\qquad \\neg(P \\to Q) \\;\\equiv\\; P \\land \\neg Q .$$

Everyday phrases for P → Q: "if P then Q", "P only if Q", "Q if P", "P is sufficient for Q", "Q is necessary for P"."""),
                 dict(h="The four related statements", md="""| Name | Form | Same as P → Q? |
|---|---|---|
| Implication | P → Q | itself |
| Converse | Q → P | no |
| Inverse | ¬P → ¬Q | no |
| Contrapositive | ¬Q → ¬P | **yes** |

The contrapositive is just the implication read backwards through negation, so proving ¬Q → ¬P is a standard way to prove P → Q. The converse and the inverse are the contrapositives of each other, so they are equivalent to each other but not to the original.

Counter-example for the converse: "if x is even then x² is even" is true, but "if x² is even then x is even" is a different claim (it is also true, which is why the check must be made by the table, not by wording)."""),
                 dict(h="The biconditional", md="""P ↔ Q means (P → Q) ∧ (Q → P): "P if and only if Q". It is true when P and Q have the same value. To prove a biconditional, prove both directions, or chain equivalences."""),
                 dict(h="How to test two statements", md="""To decide whether two implications are equivalent, look for a row where they differ. For P → Q and Q → P that row is (P, Q) = (1, 0) versus (0, 1): the first is false in one, the second in the other, so they are not equivalent.""")],
         examples=[
             Ex("Contrapositive in words", "Write the contrapositive of \"if a number is divisible by 6, then it is divisible by 3\".", ["P: divisible by 6; Q: divisible by 3. The contrapositive is ¬Q → ¬P.", "**If a number is not divisible by 3, then it is not divisible by 6.**"], "If a number is not divisible by 3, then it is not divisible by 6.", verify=lambda: "If a number is not divisible by 3, then it is not divisible by 6."),
             Ex("Negating an implication", "Which formula is equivalent to ¬(P → Q)?", ["P → Q ≡ ¬P ∨ Q. By De Morgan, ¬(¬P ∨ Q) ≡ P ∧ ¬Q.", "It is the single failing row P = 1, Q = 0."], "**P ∧ ¬Q**", verify=lambda: "P ∧ ¬Q" if all((not ((not p) or q)) == (p and not q) for p, q in B2) else "?"),
             Ex("Converse is different", "Show that P → Q and Q → P are not equivalent.", ["Take P = 0, Q = 1.", "P → Q is true (false hypothesis) but Q → P is false."], "The row **P = 0, Q = 1** separates them.", verify=lambda: "The row P = 0, Q = 1 separates them" if [(p, q) for p, q in B2 if (((not p) or q) != ((not q) or p))] == [(0, 1), (1, 0)] else "?"),
             Ex("Currying", "Is p → (q → r) equivalent to (p ∧ q) → r?", ["p → (q → r) ≡ ¬p ∨ ¬q ∨ r.", "(p ∧ q) → r ≡ ¬(p ∧ q) ∨ r ≡ ¬p ∨ ¬q ∨ r. Same formula."], "**Yes**, they are equivalent.", verify=lambda: "Yes" if all(((not p) or ((not q) or r)) == ((not (p and q)) or r) for p, q, r in B3) else "No"),
             Ex("GATE style: how often is it false", "In how many of the 8 assignments of (p, q, r) is (p ∧ q) → r false?", ["An implication fails only if its hypothesis is true and its conclusion is false.", "p ∧ q true needs p = q = 1, and r = 0: one assignment."], "**1**", verify=lambda: str(sum(1 for p, q, r in B3 if (p and q) and not r)))],
         traps=[("Using the converse", "Q → P does not follow from P → Q. Only ¬Q → ¬P does."),
                ("Vacuous truth", "If P is false, P → Q is true. Do not look for a 'reason' linking P and Q."),
                ("Negating an implication", "The negation is P ∧ ¬Q, not ¬P → ¬Q."),
                ("Necessary versus sufficient", "'P is sufficient for Q' is P → Q; 'P is necessary for Q' is Q → P.")],
         quick=[("¬(P → Q) is equivalent to", ["¬P → ¬Q", "P ∧ ¬Q", "¬P ∨ Q", "Q → P"], 1, "The implication fails exactly when P is true and Q false."),
                ("The contrapositive of P → Q is", ["Q → P", "¬P → ¬Q", "¬Q → ¬P", "P → ¬Q"], 2, "Negate both and swap them."),
                ("When P is false, P → Q is", ["false", "true", "equal to Q", "undefined"], 1, "Vacuous truth."),
                ("'P only if Q' means", ["P → Q", "Q → P", "P ↔ Q", "P ∧ Q"], 0, "If P holds then Q must hold.")],
         summary=["P → Q ≡ ¬P ∨ Q, false only when P is true and Q is false.", "The contrapositive ¬Q → ¬P is equivalent to P → Q; the converse and inverse are not.", "¬(P → Q) ≡ P ∧ ¬Q.", "p → (q → r) ≡ (p ∧ q) → r.", "'P is sufficient for Q' means P → Q; 'necessary' means Q → P."],
         subs=["Logical forms"])

# ------------------------------------------------------------------------------------------------ 1.3
A.lesson("engm-lg-equiv", "Logical equivalences and normal forms",
         key="Two formulas are equivalent when they agree on every row. A short list of laws lets you rewrite any formula into a simpler or standard shape, and every formula has a disjunctive (DNF) and a conjunctive (CNF) normal form read straight from its truth table.",
         analogy=("🔁", "Different words, same meaning", "'Not (rain and cold)' and 'no rain or no cold' describe exactly the same days. Equivalence laws are the grammar rules that let you swap one wording for another."),
         defs=[("Logical equivalence F ≡ G", "F and G have the same truth value under every assignment, so F ↔ G is a tautology."),
               ("Literal, clause, term", "A literal is a variable or its negation; a clause is an OR of literals; a term is an AND of literals."),
               ("CNF and DNF", "Conjunctive normal form is an AND of clauses; disjunctive normal form is an OR of terms."),
               ("Functionally complete set", "A set of connectives from which every Boolean function can be built, such as {¬, ∧}, {¬, ∨} or {NAND}.")],
         parts=[dict(h="The laws", md="""| Law | Statement |
|---|---|
| De Morgan | ¬(p ∧ q) ≡ ¬p ∨ ¬q;  ¬(p ∨ q) ≡ ¬p ∧ ¬q |
| Double negation | ¬¬p ≡ p |
| Distribution | p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r);  p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r) |
| Absorption | p ∨ (p ∧ q) ≡ p;  p ∧ (p ∨ q) ≡ p |
| Implication | p → q ≡ ¬p ∨ q ≡ ¬q → ¬p |
| Biconditional | p ↔ q ≡ (p → q) ∧ (q → p) ≡ (p ∧ q) ∨ (¬p ∧ ¬q) |
| Idempotent, identity | p ∨ p ≡ p;  p ∨ 0 ≡ p;  p ∧ 1 ≡ p;  p ∨ ¬p ≡ 1;  p ∧ ¬p ≡ 0 |

To simplify, first remove → and ↔ using the implication law, push negations inward with De Morgan, then distribute and absorb."""),
                 dict(h="Normal forms", md="""**DNF from a truth table:** for every row where the formula is 1, write the term that is true exactly in that row (a variable if its value is 1, its negation if 0), and OR the terms. These are the *minterms*.

**CNF from a truth table:** for every row where the formula is 0, write the clause that is false exactly in that row (a variable if its value is 0, its negation if 1), and AND the clauses. These are the *maxterms*.

Example: the formula with 1s at (1, 0) and (0, 1) has DNF (p ∧ ¬q) ∨ (¬p ∧ q) and CNF (p ∨ q) ∧ (¬p ∨ ¬q); both describe p ⊕ q."""),
                 dict(h="Functional completeness", md="""Because p ∨ q ≡ ¬(¬p ∧ ¬q) and p → q ≡ ¬p ∨ q, the set {¬, ∧} (and {¬, ∨}) already expresses every connective. NAND alone is complete: ¬p ≡ p NAND p and p ∧ q ≡ ¬(p NAND q). NOR alone is complete as well. The sets {∧, ∨} and {→} are **not** complete: they can only build functions with f(1, …, 1) = 1."""),
                 dict(h="Checking an equivalence", md="""Two ways: compare the truth tables, or transform one side into the other with the laws. For a quick refutation, find one row where the formulas differ.""")],
         examples=[
             Ex("De Morgan", "Simplify ¬(p ∨ ¬q).", ["De Morgan: ¬(p ∨ ¬q) ≡ ¬p ∧ ¬¬q.", "Double negation gives **¬p ∧ q**."], "**¬p ∧ q**", verify=lambda: "¬p ∧ q" if all((not (p or not q)) == ((not p) and q) for p, q in B2) else "?"),
             Ex("Absorbing a term", "Simplify (p ∧ q) ∨ (p ∧ ¬q).", ["Factor p: p ∧ (q ∨ ¬q).", "q ∨ ¬q ≡ 1, so the result is **p**."], "**p**", verify=lambda: "p" if all(((p and q) or (p and not q)) == p for p, q in B2) else "?"),
             Ex("DNF from a table", "Find a DNF for the function that is 1 exactly on (p, q) = (1, 0) and (0, 1).", ["One minterm per 1-row: p ∧ ¬q and ¬p ∧ q.", "OR them together."], "**(p ∧ ¬q) ∨ (¬p ∧ q)**", verify=lambda: "(p ∧ ¬q) ∨ (¬p ∧ q)" if all((((p and not q) or (not p and q)) == (p != q)) for p, q in B2) else "?"),
             Ex("CNF from a table", "Find a CNF for the same function.", ["The 0-rows are (0, 0) and (1, 1).", "Row (0, 0): clause p ∨ q. Row (1, 1): clause ¬p ∨ ¬q. AND them."], "**(p ∨ q) ∧ (¬p ∨ ¬q)**", verify=lambda: "(p ∨ q) ∧ (¬p ∨ ¬q)" if all((((p or q) and ((not p) or (not q))) == (p != q)) for p, q in B2) else "?"),
             Ex("GATE style: spot the equivalent", "Which of these is equivalent to p → (q ∨ r): (a) (p → q) ∨ (p → r), (b) (p → q) ∧ (p → r), (c) (p ∧ q) → r?", ["p → (q ∨ r) ≡ ¬p ∨ q ∨ r.", "(p → q) ∨ (p → r) ≡ (¬p ∨ q) ∨ (¬p ∨ r) ≡ ¬p ∨ q ∨ r. (b) is stronger and (c) is different."], "**(a)**", verify=lambda: "(a)" if all((((not p) or (q or r)) == (((not p) or q) or ((not p) or r))) for p, q, r in B3) else "?")],
         traps=[("De Morgan", "¬(p ∧ q) is ¬p ∨ ¬q. Forgetting to flip the connective is the most common slip."),
                ("Distribution over the other connective", "p ∨ (q ∧ r) distributes too, giving (p ∨ q) ∧ (p ∨ r); beginners only remember one direction."),
                ("CNF clauses are read from the 0-rows", "A CNF uses the rows where the formula is false, with the variables negated."),
                ("{∧, ∨} is not complete", "Without negation you cannot express ¬p.")],
         quick=[("¬(p ∨ q) is equivalent to", ["¬p ∨ ¬q", "¬p ∧ ¬q", "p ∧ q", "¬p → q"], 1, "De Morgan."),
                ("p ∨ (p ∧ q) simplifies to", ["q", "p", "p ∧ q", "1"], 1, "Absorption."),
                ("A DNF is read from the rows where the formula is", ["0", "1", "undefined", "unused"], 1, "One minterm per true row."),
                ("Which set of connectives is functionally complete?", ["{∧, ∨}", "{→}", "{NAND}", "{⊕}"], 2, "NAND alone builds ¬ and ∧.")],
         summary=["Two formulas are equivalent when their truth tables are identical.", "De Morgan flips ∧ and ∨ when a negation is pushed inside.", "p → q ≡ ¬p ∨ q; use it first to remove implications.", "DNF comes from the 1-rows, CNF from the 0-rows of the table.", "{¬, ∧}, {¬, ∨}, {NAND} and {NOR} are functionally complete."],
         subs=["Equivalences"])

# ------------------------------------------------------------------------------------------------ 1.4
A.lesson("engm-lg-models", "Satisfiability, validity and counting models",
         key="A formula is valid when it is true in every row, satisfiable when true in at least one, and a contradiction when true in none. Counting its true rows (its models) is a counting problem solved by structure, not by writing the table.",
         analogy=("🔍", "Searching the rows", "Imagine the truth table as a list of 2ⁿ possible worlds. Valid means every world agrees, satisfiable means some world does, and counting models counts how many do."),
         defs=[("Model", "An assignment of truth values under which a formula is true."),
               ("Tautology (valid)", "A formula true under every assignment."),
               ("Satisfiable", "A formula true under at least one assignment."),
               ("Contradiction (unsatisfiable)", "A formula true under no assignment.")],
         parts=[dict(h="Three kinds of formula", md="""| Kind | True in | Example |
|---|---|---|
| Tautology | all 2ⁿ rows | p ∨ ¬p,  (p → q) ∨ (q → p) |
| Contingent | some rows, not all | p ∧ q |
| Contradiction | no row | p ∧ ¬p |

F is valid exactly when ¬F is unsatisfiable. Every tautology is satisfiable; a formula that is satisfiable but not valid is called contingent.

**Complexity.** Deciding whether a formula in CNF is satisfiable (SAT) is NP-complete; deciding validity is co-NP-complete. For GATE the interesting question is how to *count* models quickly."""),
                 dict(h="Counting models by structure", md="""Let the formula use n variables in total.

- A conjunction of k literals on distinct variables has **2^(n−k)** models: k variables are forced, the rest are free.
- A clause (OR) of k literals on distinct variables has **2ⁿ − 2^(n−k)** models: it fails only in the single combination that falsifies every literal.
- p → q fails only for p = 1, q = 0, so it has ¾·2ⁿ models.
- If two formulas use disjoint variables, the model counts multiply.
- An exclusive or of n variables has 2ⁿ⁻¹ models.

Variables that never appear in the formula are free and double the count each time."""),
                 dict(h="Method", md="""1. Decide which variables the formula really constrains.
2. Count assignments of those variables that make it true, using the rules above or a short case split.
3. Multiply by 2 for each unconstrained variable.

To test validity, look for a falsifying row; to test satisfiability, look for a satisfying row. One row settles either question.""")],
         examples=[
             Ex("A clause", "How many of the 16 assignments of p, q, r, s satisfy p ∨ q ∨ r?", ["The clause fails only when p = q = r = 0; s is free, so 2 failing assignments.", "16 − 2 = **14**."], "**14**", verify=lambda: str(sum(1 for p, q, r, s in itertools.product((0, 1), repeat=4) if p or q or r))),
             Ex("A conjunction of literals", "How many of the 64 assignments of p₁ … p₆ satisfy p₁ ∧ ¬p₂ ∧ p₃?", ["Three variables are forced; three are free.", "2³ = **8**."], "**8**", verify=lambda: str(sum(1 for t in itertools.product((0, 1), repeat=6) if t[0] and not t[1] and t[2]))),
             Ex("Is it a tautology?", "Is (p → q) ∨ (q → p) a tautology?", ["If q is true, p → q is true. If q is false, q → p is true.", "Every row satisfies it."], "**Yes**, it is valid.", verify=lambda: "Yes" if all(((not p) or q) or ((not q) or p) for p, q in B2) else "No"),
             Ex("Models of an implication chain", "How many of the 8 assignments of (p, q, r) satisfy (p → q) ∧ (q → r)?", ["The forbidden patterns are p = 1, q = 0 and q = 1, r = 0.", "Surviving rows: 000, 001, 011, 111."], "**4**", verify=lambda: str(sum(1 for p, q, r in B3 if ((not p) or q) and ((not q) or r)))),
             Ex("GATE style: satisfiable but not valid", "Classify (p ∨ q) ∧ (¬p ∨ ¬q) and give the number of models.", ["The first clause excludes (0, 0); the second excludes (1, 1).", "Models: (0, 1) and (1, 0): true in 2 of 4 rows, so it is satisfiable but not valid. It is p ⊕ q."], "Satisfiable, not valid, **2** models.", verify=lambda: "Satisfiable, not valid, %d models" % sum(1 for p, q in B2 if (p or q) and ((not p) or (not q))))],
         traps=[("Valid versus satisfiable", "Valid means true in every row; satisfiable only needs one."),
                ("Forgetting free variables", "A formula on 3 of 5 variables has its model count multiplied by 2²."),
                ("Negation", "F is valid iff ¬F is unsatisfiable, not iff ¬F is valid."),
                ("Difficulty", "SAT is NP-complete; do not claim a polynomial test.")],
         quick=[("p ∧ ¬p is", ["a tautology", "a contradiction", "contingent", "valid"], 1, "It is false in every row."),
                ("Models of p ∨ q over the three variables p, q, r", ["3", "6", "7", "8"], 1, "3 of 4 rows for (p, q), times 2 for r."),
                ("F is valid iff ¬F is", ["satisfiable", "unsatisfiable", "contingent", "valid"], 1, "No row falsifies F."),
                ("A conjunction of 3 literals over 5 variables has how many models?", ["2", "4", "8", "16"], 1, "2^(5−3)."),],
         summary=["Valid = true in all rows; satisfiable = true in some row; contradiction = true in none.", "F is valid exactly when ¬F is unsatisfiable.", "A k-literal conjunction has 2^(n−k) models; a k-literal clause has 2ⁿ − 2^(n−k).", "Variables not in the formula double the count.", "SAT is NP-complete."],
         subs=["Satisfiability", "Counting models"])

# ------------------------------------------------------------------------------------------------ 1.5
A.lesson("engm-logic-quantifiers", "Predicates and quantifiers",
         key="A predicate becomes a proposition when its variable is replaced by a value or bound by a quantifier. ∀ means for every element, ∃ means for at least one. Negation flips the quantifier, and with mixed quantifiers their order matters.",
         analogy=("🔑", "Keys and doors", "∀door ∃key: every door has some key that opens it. ∃key ∀door: one master key opens every door. The second claim is much stronger than the first."),
         defs=[("Predicate P(x)", "A statement containing a variable that becomes a proposition once the variable is given a value."),
               ("Universal quantifier ∀x P(x)", "True when P(x) holds for every x in the domain."),
               ("Existential quantifier ∃x P(x)", "True when P(x) holds for at least one x in the domain."),
               ("Domain of discourse", "The set of values over which the quantified variables range.")],
         parts=[dict(h="Quantifiers over a domain", md="""Over a finite domain {a₁, …, aₙ} the quantifiers are shorthand: ∀x P(x) ≡ P(a₁) ∧ … ∧ P(aₙ) and ∃x P(x) ≡ P(a₁) ∨ … ∨ P(aₙ). This is the safest way to check a statement: expand it over a small domain.

The truth value depends on the domain. "∀x (x² ≥ x)" is false over the reals (x = ½) but true over the integers. Always read the domain first."""),
                 dict(h="Negation", md="""Push the negation through, flipping each quantifier and negating the body:

$$\\neg\\forall x\\,P(x)\\equiv\\exists x\\,\\neg P(x),\\qquad \\neg\\exists x\\,P(x)\\equiv\\forall x\\,\\neg P(x).$$

For nested statements flip every quantifier in turn: ¬∀x∃y R(x, y) ≡ ∃x∀y ¬R(x, y). For an implication body use ¬(A → B) ≡ A ∧ ¬B."""),
                 dict(h="Nested quantifiers and order", md="""- ∀x∀y and ∃x∃y: the order does not matter.
- ∀x∃y R(x, y): every x has *its own* y (the y may depend on x).
- ∃y∀x R(x, y): *one* y works for every x.

The second implies the first, never the other way round. Test with R(x, y) = "x = y" over {1, 2}: ∀x∃y holds (take y = x) but ∃y∀x fails."""),
                 dict(h="Laws worth knowing", md="""- ∀ distributes over ∧: ∀x (A ∧ B) ≡ ∀x A ∧ ∀x B. ∃ distributes over ∨.
- ∀x (A ∨ B) is **not** equivalent to ∀x A ∨ ∀x B; only ∀x A ∨ ∀x B ⇒ ∀x (A ∨ B) holds.
- ∃x (A ∧ B) ⇒ ∃x A ∧ ∃x B, but not conversely.
- Over an empty domain ∀x P(x) is true and ∃x P(x) is false.""")],
         examples=[
             Ex("Evaluating on a finite domain", "Domain {1, 2, 3}. Is ∀x ∃y (x + y = 4) true?", ["x = 1: y = 3. x = 2: y = 2. x = 3: y = 1.", "Every x has a partner in the domain."], "**True**.", verify=lambda: "True" if all(any(x + y == 4 for y in (1, 2, 3)) for x in (1, 2, 3)) else "False"),
             Ex("Swapping the order", "Same domain. Is ∃y ∀x (x + y = 4) true?", ["One y would need to work for x = 1, 2 and 3: y = 3, 2 and 1 respectively.", "No single y works."], "**False**; swapping the quantifiers changed the truth value.", verify=lambda: "False; swapping the quantifiers changed the truth value" if not any(all(x + y == 4 for x in (1, 2, 3)) for y in (1, 2, 3)) else "?"),
             Ex("Negating a statement", "Negate ∀x ∃y (x < y) over the integers and decide which version is true.", ["Flip quantifiers: ∃x ∀y ¬(x < y), i.e. ∃x ∀y (y ≤ x).", "That says a largest integer exists: false. So the original is **true**."], "Negation: **∃x ∀y (y ≤ x)** (false); the original is true.", verify=lambda: "Negation: ∃x ∀y (y ≤ x) (false); the original is true"),
             Ex("Distributing", "Is ∀x (P(x) ∨ Q(x)) equivalent to ∀x P(x) ∨ ∀x Q(x)?", ["Let the domain be {1, 2}, P true only at 1 and Q true only at 2.", "Every x satisfies P ∨ Q, yet neither ∀x P nor ∀x Q holds."], "**No**; only one direction holds.", verify=lambda: "No" if all((p or q) for p, q in [(1, 0), (0, 1)]) and not all(p for p, q in [(1, 0), (0, 1)]) and not all(q for p, q in [(1, 0), (0, 1)]) else "Yes"),
             Ex("GATE style: empty domain", "Over an empty domain, what are the truth values of ∀x P(x) and ∃x P(x)?", ["∀ is a conjunction over no elements: vacuously true.", "∃ is a disjunction over no elements: false."], "∀ is **true**, ∃ is **false**.", verify=lambda: "∀ is %s, ∃ is %s" % (str(all([])).lower(), str(any([])).lower()))],
         traps=[("Swapping ∀ and ∃", "∀x∃y and ∃y∀x are different statements."),
                ("Negating only one half", "¬∀x P is ∃x ¬P; it is not ∀x ¬P."),
                ("Forgetting the domain", "Truth values change with the domain; state it."),
                ("Distribution", "∀ distributes over ∧, not over ∨.")],
         quick=[("¬∀x P(x) is equivalent to", ["∀x ¬P(x)", "∃x ¬P(x)", "∃x P(x)", "¬∃x ¬P(x)"], 1, "Flip the quantifier and negate the body."),
                ("∃y∀x R(x, y) implies", ["∀x∃y R(x, y)", "nothing", "∀y∃x R(x, y)", "¬∀x∃y R(x, y)"], 0, "The master key opens every door."),
                ("Over an empty domain ∀x P(x) is", ["false", "true", "undefined", "equal to ∃x P(x)"], 1, "Vacuously true."),
                ("∃x (A(x) ∧ B(x)) implies", ["∃x A(x) ∧ ∃x B(x)", "∀x A(x)", "∀x B(x)", "nothing"], 0, "The same witness works for both.")],
         summary=["Over a finite domain, ∀ is a conjunction and ∃ a disjunction.", "¬∀x P ≡ ∃x ¬P and ¬∃x P ≡ ∀x ¬P.", "∃y∀x implies ∀x∃y, never the reverse.", "∀ distributes over ∧, ∃ over ∨.", "Over an empty domain, ∀ is true and ∃ is false."],
         subs=["First-order logic"])

# ------------------------------------------------------------------------------------------------ 1.6
A.lesson("engm-lg-fol", "Translating English into first-order logic",
         key="Every translation question tests two habits: ∀ goes with →, ∃ goes with ∧, and the order of mixed quantifiers decides whether each x gets its own y or one y serves all.",
         analogy=("🗣️", "Reading the sentence twice", "First find the quantifier words (every, some, no). Then ask whether the thing they pick may depend on an earlier choice. The answer fixes the order."),
         defs=[("Restricted quantifier", "A quantifier whose range is limited by a predicate: all A are B is ∀x (A(x) → B(x))."),
               ("Quantifier word", "Every, all, each → ∀; some, there is, at least one → ∃; no, none → ¬∃ or ∀ … ¬."),
               ("Dependence", "In ∀x∃y the witness y may depend on x; in ∃y∀x it may not.")],
         parts=[dict(h="Standard patterns", md="""| English | First-order logic |
|---|---|
| All A are B | ∀x (A(x) → B(x)) |
| Some A is B | ∃x (A(x) ∧ B(x)) |
| No A is B | ∀x (A(x) → ¬B(x))  (≡ ¬∃x (A(x) ∧ B(x))) |
| Some A is not B | ∃x (A(x) ∧ ¬B(x)) |
| Every x has some y with R | ∀x ∃y R(x, y) |
| One y works for all x | ∃y ∀x R(x, y) |

The pairing is not arbitrary. ∀x (A ∧ B) would claim that *everything* is an A and a B; ∃x (A → B) is true as soon as anything is not an A. Both are rarely what the sentence says."""),
                 dict(h="Translation procedure", md="""1. Name the predicates and fix the domain: S(x) "x is a student", T(x, y) "x takes y".
2. Mark the quantifier words in the order they appear.
3. Put each restricting predicate under its quantifier: → under ∀, ∧ under ∃.
4. Keep the quantifier order of the sentence.
5. Test the formula on a tiny model (two elements) to see that it says what the sentence says.

Example: "Every student takes some course" becomes ∀x (S(x) → ∃y (C(y) ∧ T(x, y)))."""),
                 dict(h="Negating a translation", md="""The negation of "every student passed some exam", ∀x ∃y P(x, y), is ∃x ∀y ¬P(x, y): some student failed every exam. Translating a negative sentence directly, "no student passed every exam", gives ¬∃x ∀y P(x, y), which is the same as ∀x ∃y ¬P(x, y).""")],
         examples=[
             Ex("Every has some", "Express \"every student takes some course\", with T(x, y) meaning x takes y.", ["Each student picks a (possibly different) course.", "Put ∀ outside, ∃ inside."], "**∀x ∃y T(x, y)**", verify=lambda: "∀x ∃y T(x, y)"),
             Ex("One for all", "Express \"there is one course taken by every student\".", ["A single course y works for all x.", "Put ∃y first."], "**∃y ∀x T(x, y)**", verify=lambda: "∃y ∀x T(x, y)"),
             Ex("All are", "Translate \"all prime numbers greater than 2 are odd\".", ["The restriction is 'prime and greater than 2', so it goes in the hypothesis of the implication."], "**∀x ((P(x) ∧ x > 2) → Odd(x))**", verify=lambda: "∀x ((P(x) ∧ x > 2) → Odd(x))"),
             Ex("Negating a translation", "Negate ∀x ∃y P(x, y) and read it in English for 'every student passed some exam'.", ["Flip both quantifiers and negate the body: ∃x ∀y ¬P(x, y).", "English: some student passed no exam."], "**∃x ∀y ¬P(x, y)**", verify=lambda: "∃x ∀y ¬P(x, y)"),
             Ex("GATE style: which formula fits", "Over {1, 2} with R(x, y) meaning x = y, which of ∀x∃y R(x, y) and ∃y∀x R(x, y) is true?", ["∀x∃y: each x equals itself: true.", "∃y∀x: no single y equals both 1 and 2: false."], "Only **∀x ∃y R(x, y)**.", verify=lambda: "Only ∀x ∃y R(x, y)" if all(any(x == y for y in (1, 2)) for x in (1, 2)) and not any(all(x == y for x in (1, 2)) for y in (1, 2)) else "?")],
         traps=[("∀ with ∧", "∀x (A(x) ∧ B(x)) says everything is both A and B."),
                ("∃ with →", "∃x (A(x) → B(x)) is true if anything fails A."),
                ("Reversing the order", "'Every x has some y' and 'some y for every x' are different formulas."),
                ("Negating by adding ¬ in front only", "¬∀x P is ∃x ¬P; it is not ∀x ¬P.")],
         quick=[("'Some A is B' is", ["∃x (A → B)", "∃x (A ∧ B)", "∀x (A ∧ B)", "∀x (A → B)"], 1, "∃ pairs with ∧."),
                ("'No A is B' is", ["∀x (A → ¬B)", "∃x (A ∧ ¬B)", "∀x (A ∧ ¬B)", "∃x (A → ¬B)"], 0, "Universal with an implication."),
                ("'Every x has some y' is", ["∃y ∀x R", "∀x ∃y R", "∀x ∀y R", "∃x ∃y R"], 1, "Each x gets its own y."),
                ("The negation of ∀x ∃y P(x, y) is", ["∀x ∃y ¬P", "∃x ∀y ¬P", "∃x ∃y ¬P", "∀x ∀y ¬P"], 1, "Flip both quantifiers.")],
         summary=["All A are B: ∀x (A → B). Some A is B: ∃x (A ∧ B).", "No A is B: ∀x (A → ¬B).", "'Every x has some y' is ∀x∃y; 'one y for all x' is ∃y∀x.", "Negation flips each quantifier and negates the body.", "Test a formula on a two-element model before trusting it."],
         subs=["FOL translation"])

# ------------------------------------------------------------------------------------------------ 1.7
A.lesson("engm-lg-inference", "Rules of inference",
         key="An argument is valid if no assignment makes all premises true and the conclusion false. A few valid patterns (modus ponens, modus tollens, syllogisms, resolution) can be chained; two look-alike patterns, affirming the consequent and denying the antecedent, are fallacies.",
         analogy=("⚖️", "A sound chain", "Each rule is a link that never breaks: if the premises hold, the conclusion must. A fallacy is a link that only looks solid; one counter-example row snaps it."),
         defs=[("Argument", "A list of premises followed by a conclusion."),
               ("Valid argument", "One in which every assignment making all premises true also makes the conclusion true."),
               ("Rule of inference", "A valid argument form used as a step in a proof."),
               ("Fallacy", "An argument form that looks valid but has a counter-example row.")],
         parts=[dict(h="Valid rules and fallacies", md="""| Name | Premises ⊢ Conclusion | Valid? |
|---|---|---|
| Modus ponens | P → Q, P ⊢ Q | yes |
| Modus tollens | P → Q, ¬Q ⊢ ¬P | yes |
| Hypothetical syllogism | P → Q, Q → R ⊢ P → R | yes |
| Disjunctive syllogism | P ∨ Q, ¬P ⊢ Q | yes |
| Resolution | P ∨ Q, ¬P ∨ R ⊢ Q ∨ R | yes |
| Addition, simplification | P ⊢ P ∨ Q;  P ∧ Q ⊢ P | yes |
| Affirming the consequent | P → Q, Q ⊢ P | **no** |
| Denying the antecedent | P → Q, ¬P ⊢ ¬Q | **no** |"""),
                 dict(h="Testing an argument", md="""To test validity, search for a row where every premise is true and the conclusion false.

1. Write the premises and the conclusion.
2. Make the conclusion false and try to make every premise true.
3. If that is possible, the argument is **invalid**, and the row is a counter-example. If every attempt forces a contradiction, it is **valid**.

Affirming the consequent fails on P = 0, Q = 1: both premises P → Q and Q are true, the conclusion P is false."""),
                 dict(h="Chaining rules in a proof", md="""A proof is a list of lines, each a premise or obtained from earlier lines by a rule. Example: from p → q, q → r and ¬r, derive ¬p.

1. p → q (premise)   2. q → r (premise)   3. ¬r (premise)
4. p → r (hypothetical syllogism, 1 and 2)   5. ¬p (modus tollens, 4 and 3)

Resolution is the rule behind automated provers: from two clauses containing a complementary pair, derive the clause of the remaining literals. A set of clauses is unsatisfiable iff the empty clause can be derived."""),
                 dict(h="Validity is not truth", md="""A valid argument may have a false conclusion if some premise is false; an invalid argument may have a true conclusion by luck. Validity concerns only the form: *no row* makes the premises true and the conclusion false.""")],
         examples=[
             Ex("Name the rule", "Name the rule used in: (1) if it rains the road is wet; (2) the road is not wet; so (3) it did not rain.", ["P: it rains; Q: the road is wet. The pattern is P → Q, ¬Q ⊢ ¬P."], "**Modus tollens**", verify=lambda: "Modus tollens" if G2.valid([lambda e: (not e["P"]) or e["Q"], lambda e: not e["Q"]], lambda e: not e["P"])[0] else "?"),
             Ex("Spot the fallacy", "Is P → Q, Q ⊢ P valid?", ["Look for a row with true premises and false conclusion.", "P = 0, Q = 1 gives P → Q true, Q true, P false."], "**Invalid** (affirming the consequent).", verify=lambda: "Invalid" if not G2.valid([lambda e: (not e["P"]) or e["Q"], lambda e: e["Q"]], lambda e: e["P"])[0] else "Valid"),
             Ex("Chain", "From p → q, q → r and ¬r, what follows about p?", ["Hypothetical syllogism gives p → r.", "Modus tollens with ¬r gives ¬p."], "**¬p**", verify=lambda: "¬p" if G2.valid([lambda e: (not e["P"]) or e["Q"], lambda e: (not e["Q"]) or e["R"], lambda e: not e["R"]], lambda e: not e["P"])[0] else "?"),
             Ex("Resolution", "From p ∨ q and ¬p ∨ r, what clause is derived?", ["Resolve on p: the complementary pair p, ¬p cancels.", "What remains is q ∨ r."], "**q ∨ r**", verify=lambda: "q ∨ r" if G2.valid([lambda e: e["P"] or e["Q"], lambda e: (not e["P"]) or e["R"]], lambda e: e["Q"] or e["R"])[0] else "?"),
             Ex("GATE style: is the conclusion forced?", "Premises: p ∨ q, p → r, q → r. Does r follow?", ["Case p: p → r gives r. Case q: q → r gives r.", "One of p, q holds, so r holds either way (proof by cases)."], "**Yes**, r follows.", verify=lambda: "Yes" if G2.valid([lambda e: e["P"] or e["Q"], lambda e: (not e["P"]) or e["R"], lambda e: (not e["Q"]) or e["R"]], lambda e: e["R"])[0] else "No")],
         traps=[("Affirming the consequent", "Q true does not make P true."),
                ("Denying the antecedent", "P false says nothing about Q."),
                ("Valid versus true", "An argument can be valid with a false conclusion when a premise is false."),
                ("Resolution needs a complementary pair", "p ∨ q and p ∨ r share no complementary literals, so nothing follows.")],
         quick=[("P → Q, ¬Q ⊢ ¬P is called", ["modus ponens", "modus tollens", "resolution", "a fallacy"], 1, "Deny the consequent, deny the antecedent."),
                ("P → Q, Q ⊢ P is", ["valid", "a fallacy", "modus ponens", "resolution"], 1, "Counter-example P = 0, Q = 1."),
                ("Resolving p ∨ q with ¬q ∨ r gives", ["p ∨ r", "p ∧ r", "q", "¬p"], 0, "q and ¬q cancel."),
                ("A valid argument with true premises always has", ["a true conclusion", "a false conclusion", "an unknown conclusion", "no conclusion"], 0, "That is what validity guarantees.")],
         summary=["Valid means no row makes all premises true and the conclusion false.", "Modus ponens, modus tollens, hypothetical and disjunctive syllogism and resolution are valid.", "Affirming the consequent and denying the antecedent are fallacies.", "Test an argument by trying to make the conclusion false with true premises.", "Validity concerns form, not whether the statements are actually true."],
         subs=["Rules of inference"])
