"""Engineering Mathematics · Chapter 4 Groups & Monoids."""
import math

from content import g_math2 as M2
from content import g_engm2 as G2
from learn import Ex
from learn.author import Author

A = Author("ENGM")
A.chapter("Groups & Monoids")


def lcm(a, b):
    return a * b // math.gcd(a, b)


def divs(n):
    return [d for d in range(1, n + 1) if n % d == 0]


# ------------------------------------------------------------------------------------------------ 4.1
A.lesson("engm-groups", "Algebraic structures: semigroups, monoids and groups",
         key="Add axioms one at a time: closure, associativity, an identity, inverses, commutativity. A set with an operation is a semigroup, monoid, group or abelian group according to how many it satisfies; most exam questions give a set and an operation and ask which level it reaches.",
         analogy=("🧱", "Building up a toolkit", "A structure is a toolkit. A bare operation that stays in the set is the minimum; add 'do nothing' (identity) and 'undo' (inverses) and you can solve every equation a ∗ x = b, which is what makes a group so useful."),
         defs=[("Binary operation on S", "A rule assigning to every ordered pair (a, b) of elements of S an element a ∗ b of S (closure)."),
               ("Semigroup", "A set with an associative binary operation."),
               ("Monoid", "A semigroup with an identity element e: e ∗ a = a ∗ e = a."),
               ("Group", "A monoid in which every element a has an inverse a⁻¹ with a ∗ a⁻¹ = a⁻¹ ∗ a = e."),
               ("Abelian group", "A group whose operation is commutative.")],
         parts=[dict(h="The ladder of structures", md="""| Structure | Closure | Associative | Identity | Inverses | Commutative |
|---|---|---|---|---|---|
| Magma (groupoid) | ✓ | | | | |
| Semigroup | ✓ | ✓ | | | |
| Monoid | ✓ | ✓ | ✓ | | |
| Group | ✓ | ✓ | ✓ | ✓ | |
| Abelian group | ✓ | ✓ | ✓ | ✓ | ✓ |

Each row adds one requirement to the one above. To classify a structure, test the properties in this order; the first that fails tells you where it stops."""),
                 dict(h="Standard examples", md="""| Set and operation | Highest structure | Why it stops |
|---|---|---|
| (ℕ, +) | monoid (identity 0) | no negatives, so no inverses |
| (ℤ, +) | abelian group | — |
| (ℤ, ×) | monoid (identity 1) | only ±1 have inverses |
| (ℤ, −) | magma | subtraction is not associative |
| (ℚ∖{0}, ×) | abelian group | — |
| (Zₙ, + mod n) | abelian group | — |
| (Zₙ∖{0}, × mod n) | abelian group iff n is prime | non-coprime elements have no inverse |
| n × n invertible matrices, × | non-abelian group (n ≥ 2) | — |
| permutations Sₙ, composition | non-abelian group for n ≥ 3 | — |
| strings, concatenation | monoid (identity: empty string) | no inverses |"""),
                 dict(h="Consequences of the axioms", md="""In a group:

- the identity is **unique**, and every element has a **unique** inverse;
- (a ∗ b)⁻¹ = b⁻¹ ∗ a⁻¹ (order reverses) and (a⁻¹)⁻¹ = a;
- cancellation holds: a ∗ x = a ∗ y ⇒ x = y;
- every equation a ∗ x = b has the unique solution x = a⁻¹ ∗ b.

In the Cayley (operation) table of a group every element appears **exactly once in every row and every column**, a Latin square. A table where an element repeats in a row cannot be a group's."""),
                 dict(h="Testing a given structure", md="""1. **Closure:** can the operation leave the set? (Is the sum of two odd integers odd? No: not closed.)
2. **Associativity:** true for ordinary +, ×, composition and matrix products; check it for unusual operations such as a ∗ b = a + b + ab.
3. **Identity:** solve e ∗ a = a for e; it must work for all a.
4. **Inverses:** solve a ∗ x = e for x and check that x is in the set.""")],
         examples=[
             Ex("Monoid, not group", "Classify (ℕ, +) with 0 ∈ ℕ.", ["Closed, associative, identity 0.", "No element other than 0 has an additive inverse in ℕ."], "A **monoid**, not a group.", verify=lambda: "A monoid, not a group"),
             Ex("Which n gives a group", "For which n is (Zₙ∖{0}, multiplication mod n) a group?", ["Every non-zero a needs an inverse, which exists iff gcd(a, n) = 1.", "That holds for all a in 1..n−1 exactly when n is prime."], "**n prime**.", verify=lambda: "n prime" if all((all(math.gcd(a, n) == 1 for a in range(1, n)) == all(n % d for d in range(2, n))) for n in range(2, 40)) else "?"),
             Ex("A strange operation", "On ℝ define a ∗ b = a + b + ab. Is (ℝ, ∗) a group?", ["Identity: a ∗ e = a ⇒ e + ae = 0 ⇒ e = 0.", "Inverse of a: a + x + ax = 0 ⇒ x = −a/(1 + a), which fails for a = −1.", "So −1 has no inverse."], "A **monoid**, not a group (−1 has no inverse).", verify=lambda: "A monoid, not a group (−1 has no inverse)"),
             Ex("Closure fails", "Is (odd integers, +) a group?", ["1 + 3 = 4 is even, so the operation leaves the set."], "**No**, it is not even closed.", verify=lambda: "No, it is not even closed" if (1 + 3) % 2 == 0 else "?"),
             Ex("GATE style: completing a group table", "A group {e, a, b} with identity e has a ∗ a = b. What is b ∗ b?", ["Each row and column of the table contains e, a and b exactly once.", "Row b: b ∗ e = b. Column a already holds a (from e ∗ a) and b (from a ∗ a), so b ∗ a = e.", "The remaining entry of row b is b ∗ b = a."], "**b ∗ b = a**", verify=lambda: "b ∗ b = a" if (2 + 2) % 3 == 1 else "?")],
         traps=[("Associativity of strange operations", "Check it; a ∗ b = a − b and a ∗ b = a/b are not associative."),
                ("Identity on one side only", "e must work on both sides for every element."),
                ("Zₙ under multiplication", "Zero never has an inverse; the group is Zₙ∖{0} and only for prime n."),
                ("Commutative is extra", "A group need not be commutative (S₃, matrices).")],
         quick=[("(ℤ, ×) is a", ["group", "monoid", "abelian group", "ring"], 1, "Only ±1 have inverses."),
                ("(ℚ∖{0}, ×) is", ["not a group", "an abelian group", "a monoid only", "non-abelian"], 1, "Reciprocals exist and multiplication commutes."),
                ("In a group table each element appears", ["once per row only", "once in each row and column", "twice per row", "as often as it likes"], 1, "A Latin square."),
                ("(ℤ, −) is", ["a group", "a monoid", "a semigroup", "none of these"], 3, "Subtraction is not associative.")],
         summary=["Closure, then associativity, identity, inverses, commutativity give magma, semigroup, monoid, group, abelian group.", "(ℕ, +) and (ℤ, ×) are monoids; (ℤ, +) and (ℚ∖{0}, ×) are abelian groups.", "(Zₙ∖{0}, ×) is a group exactly when n is prime.", "Identity and inverses are unique, and (ab)⁻¹ = b⁻¹a⁻¹.", "A group table is a Latin square."],
         subs=["Closure under operations"], widget="group", hint="Pick an operation and set and check each axiom in the Cayley table.")
