"""Engineering Mathematics — Discrete Maths part 2: Posets, Groups, Graph Theory, Combinatorics."""
import itertools
import math
from fractions import Fraction

from learn import Ex, lesson

S = "ENGM"


def _divs(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def _is_prime(p):
    return p > 1 and all(p % q for q in range(2, int(p ** 0.5) + 1))


# ======================================================================================================
def _max_antichain_pset(n):
    subs = list(range(1 << n))
    best = 0
    for r in range(1, len(subs) + 1):
        found = any(all((x & y) not in (x, y) for x, y in itertools.combinations(c, 2)) for c in itertools.combinations(subs, r))
        if found:
            best = r
        elif r > best + 1:
            break
    return best


def _circular_pair_together(n):
    """Fix person 0 at seat 0 to remove rotations; person 1 must be adjacent (seat 1 or n-1)."""
    return sum(1 for perm in itertools.permutations(range(1, n)) if perm.index(1) in (0, n - 2))


def _hasse_edges(n):
    ds = _divs(n)
    return sum(1 for a in ds for b in ds if b > a and b % a == 0 and _is_prime(b // a))


lesson(subject=S, chapter="Partial Orders & Lattices", ch_no=3, no=1, slug="engm-posets-lattices", title="Posets, Hasse Diagrams & Lattices",
       topic="Partial Orders & Lattices", minutes=20, weight=4, widget="hasse",
       widget_hint="Enter n to draw the divisor lattice D_n. Click two elements to see their join (lcm) and meet (gcd); the tool also tells you whether D_n is a Boolean algebra.",
       key="A partial order ranks some pairs and leaves others incomparable. A lattice is a poset where every two elements have a least upper bound (join) and a greatest lower bound (meet); a Boolean algebra is a complemented distributive lattice and always has 2ⁿ elements.",
       analogy=("🌳", "A family tree of ‘divides’", "On the numbers 1, 2, 3, 6 ordered by divisibility, 2 and 3 are not comparable (neither divides the other), but they have a common ‘ancestor above’ (6 — the lcm) and a common ‘ancestor below’ (1 — the gcd). A poset is exactly this kind of branching picture; a lattice is one where every pair has a unique meeting point above and below."),
       sections=[
           dict(h="Partial orders and Hasse diagrams", md="""A **partial order** ≤ on a set is **reflexive, antisymmetric and transitive**. The pair (A, ≤) is a **poset**. Examples: (ℤ, ≤), (P(S), ⊆), (ℕ, divides).

Two elements are **comparable** if a ≤ b or b ≤ a; otherwise **incomparable**. If all pairs are comparable it is a **total order (chain)**.

A **Hasse diagram** draws only the *cover* relations: b covers a if a < b with nothing strictly between. Rules: no loops (reflexivity is implicit), no transitive edges, and ‘larger’ goes upward so no arrowheads are needed."""),
           dict(h="Extremal elements and bounds", md="""| Term | Meaning |
|---|---|
| **Maximal** element | nothing is strictly above it (there may be several) |
| **Minimal** element | nothing is strictly below it (several possible) |
| **Greatest** element | ≥ **every** element (at most one) |
| **Least** element | ≤ every element (at most one) |
| **Upper bound** of S | an element ≥ every member of S |
| **lub / join (∨)** | the *least* upper bound of S, if it exists |
| **glb / meet (∧)** | the *greatest* lower bound of S, if it exists |

A greatest element is always maximal, but a maximal element need not be greatest. In (D₁₂, |) the greatest element is 12 and the least is 1.""",
                call=[("trap", "Maximal ≠ greatest", "A poset can have two maximal elements and no greatest one (e.g. {a, b} with no relation). Greatest means *comparable to and above everything*.")]),
           dict(h="Chains, antichains and the two theorems", md="""A **chain** is a set of pairwise-comparable elements; an **antichain** is a set of pairwise-incomparable ones.

- **Dilworth's theorem:** the minimum number of chains needed to cover the poset equals the size of the **largest antichain**.
- **Mirsky's theorem (dual):** the minimum number of antichains needed to partition the poset equals the length of the **longest chain**.
- In the power-set lattice (P(S), ⊆) with |S| = n, the largest antichain has size **C(n, ⌊n/2⌋)** (Sperner's theorem).""",
                formulas=[("max antichain in (P(S),⊆) = C(n, ⌊n/2⌋)", "Sperner")]),
           dict(h="Lattices", md="""A **lattice** is a poset in which **every pair** {a, b} has a join a ∨ b and a meet a ∧ b. Examples: (ℤ, ≤) with max/min; (P(S), ⊆) with ∪/∩; (D_n, |) with **lcm/gcd**.

A lattice is **bounded** if it has a greatest (1) and least (0) element; every finite lattice is bounded. In a bounded lattice, b is a **complement** of a if a ∨ b = 1 and a ∧ b = 0.

- **Distributive:** a ∧ (b ∨ c) = (a ∧ b) ∨ (a ∧ c). A lattice is distributive iff it has **no sublattice isomorphic to N₅ (pentagon) or M₃ (diamond)**.
- **Complemented:** every element has a complement.
- **Boolean algebra** = complemented distributive bounded lattice. Every finite Boolean algebra is isomorphic to (P(S), ⊆) and so has **2ⁿ elements** (n = number of atoms).""",
                call=[("key", "Divisor lattices", "D_n is **distributive always**. D_n is a **Boolean algebra iff n is square-free** (no repeated prime factor). Example: D₃₀ (30 = 2·3·5) is Boolean with 8 elements; D₁₂ (12 = 2²·3) is not.")]),
       ],
       examples=[
           Ex("Hasse diagram edges of D₆₀", "How many edges does the Hasse diagram of (D₆₀, |) have?",
              ["60 = 2²·3·5, so D₆₀ is the product of chains of lengths 3, 2 and 2 (exponent + 1 elements each); |D₆₀| = 3·2·2 = 12.", "An edge joins a and b when b = a·p for a prime p. For a product of chains, edges = Σᵢ eᵢ · Πⱼ≠ᵢ (eⱼ + 1).",
               "= 2·(2·2) + 1·(3·2) + 1·(3·2) = 8 + 6 + 6 = **20**."],
              "**20** edges (12 elements).", verify=lambda: str(_hasse_edges(60))),
           Ex("Largest antichain", "What is the size of the largest antichain in (P({1,2,3,4}), ⊆)?",
              ["By Sperner's theorem the middle layer is largest: subsets of size 2.", "C(4, 2) = **6**."],
              "**6**", verify=lambda: str(_max_antichain_pset(4))),
           Ex("Complements in D₁₂", "How many elements of (D₁₂, |) have a complement?",
              ["Divisors: 1, 2, 3, 4, 6, 12. Complement of a is b with gcd(a,b) = 1 and lcm(a,b) = 12 (so ab = 12 and coprime).", "1 ↔ 12 ✔, 3 ↔ 4 ✔ (gcd 1, product 12). For 2 we would need a coprime b with ab = 12 → b = 6, but gcd(2,6) = 2 ✘. Similarly 6 has none.",
               "Elements with a complement: 1, 12, 3, 4 → **4**. Hence D₁₂ is not complemented, not Boolean."],
              "**4** of the 6 elements.", verify=lambda: str(sum(1 for a in _divs(12) if any(math.gcd(a, b) == 1 and a * b == 12 for b in _divs(12))))),
           Ex("Maximal chains in D₃₀", "How many maximal chains run from 1 to 30 in (D₃₀, |)?",
              ["Each step multiplies by one new prime. A maximal chain is an ordering of the primes 2, 3, 5.", "3! = **6** chains."],
              "**6**", verify=lambda: str(math.factorial(3))),
       ],
       traps=[("Maximal vs greatest", "Several maximal elements are possible; greatest (if it exists) is unique."),
              ("Including transitive edges in a Hasse diagram", "Only cover relations are drawn. If 1 | 2 | 4 do not draw 1—4."),
              ("Thinking incomparable means unrelated in a lattice", "Incomparable elements still have a join and meet in a lattice — it is just not one of them."),
              ("Boolean ⇔ square-free", "D_n is Boolean iff n is **square-free**. Powers of a single prime (D₈) form a chain, which is distributive but not complemented.")],
       quick=[("In (D₃₀, |) the join of 6 and 10 is", ["2", "30", "60", "15"], 1, "Join = lcm(6, 10) = 30."),
              ("How many elements does a finite Boolean algebra with 4 atoms have?", ["8", "16", "24", "4"], 1, "2⁴ = 16."),
              ("Which divisor lattice is a Boolean algebra?", ["D₁₂", "D₁₈", "D₃₀", "D₈"], 2, "30 = 2·3·5 is square-free."),
              ("The minimum number of chains covering a poset equals", ["the longest chain length", "the largest antichain size", "the number of maximal elements", "the number of elements"], 1, "Dilworth's theorem.")],
       summary=["Poset = reflexive + antisymmetric + transitive; Hasse diagram shows cover relations only.", "Greatest/least are unique; maximal/minimal may be several.", "Lattice: every pair has a join (lub) and meet (glb); D_n uses lcm/gcd.",
                "Boolean algebra = complemented distributive lattice ⇒ 2ⁿ elements; D_n is Boolean iff n square-free.", "Dilworth: min chain cover = max antichain; Mirsky: min antichain partition = longest chain.", "Sperner: largest antichain in P(S) is C(n, ⌊n/2⌋)."])

# ======================================================================================================
def _is_group(elems, op):
    E = set(elems)
    if any(op(a, b) not in E for a in E for b in E):
        return False
    ident = [e for e in E if all(op(e, a) == a == op(a, e) for a in E)]
    return bool(ident) and all(any(op(a, b) == ident[0] for b in E) for a in E)


lesson(subject=S, chapter="Groups & Monoids", ch_no=4, no=1, slug="engm-groups", title="Groups, Subgroups, Cyclic Groups & Lagrange",
       topic="Groups & Monoids", minutes=20, weight=3, widget="group",
       widget_hint="Pick a modulus and either addition mod n or the multiplicative group of units. The Cayley table highlights the cyclic subgroup of the chosen element and lists the generators.",
       key="A group is a set with an associative operation, an identity, and inverses. Lagrange's theorem — the order of a subgroup divides the order of the group — is the single most useful fact for GATE counting questions.",
       analogy=("🔄", "Symmetries of a clock", "Rotate a 12-hour clock face by any whole number of hours. Doing one rotation then another is another rotation (closure), rotating by 0 does nothing (identity), and every rotation can be undone (inverse). That is the group (Z₁₂, +)."),
       sections=[
           dict(h="Algebraic structures ladder", md="""| Structure | Requirements on (G, ∗) |
|---|---|
| **Groupoid / magma** | closure |
| **Semigroup** | closure + associativity |
| **Monoid** | semigroup + **identity** |
| **Group** | monoid + **inverse** for every element |
| **Abelian group** | group + commutativity |

Examples: (ℕ, +) is a monoid (identity 0) but not a group; (ℤ, +) is an abelian group; (ℤ, ×) is a monoid; non-zero rationals under × form a group; n × n invertible matrices under multiplication form a **non-abelian** group.""",
                call=[("tip", "Quick group test", "Check in order: closure → identity → inverses (associativity is usually inherited). A single failure disproves ‘group’.")]),
           dict(h="Key examples: Zₙ, Zₙ* and Sₙ", md="""- **(Zₙ, +)** — integers 0..n−1 with addition mod n: an abelian group of order n, always cyclic (generated by 1).
- **(Zₙ*, ×)** — numbers in 1..n−1 **coprime to n** with multiplication mod n: order **φ(n)**. It is a group for every n; Zₙ itself under × is *not* (0 has no inverse).
- **Sₙ** — all permutations of n objects under composition: order **n!**, non-abelian for n ≥ 3.

For a permutation written as disjoint cycles, its **order is the lcm of the cycle lengths**. A permutation is *even* if it is a product of an even number of transpositions; a k-cycle has parity k − 1."""),
           dict(h="Subgroups, order, Lagrange", md="""A subset H ⊆ G is a **subgroup** if it is itself a group under G's operation. **One-step test:** H non-empty and a, b ∈ H ⇒ a ∗ b⁻¹ ∈ H.

The **order of an element** a is the smallest k ≥ 1 with aᵏ = e. The **order of a group** |G| is its number of elements.""",
                formulas=[("Lagrange: |H| divides |G|", "for every subgroup H of a finite group G"), ("order(a) divides |G|", "and a^|G| = e")],
                call=[("key", "Consequences you can quote", "Every group of **prime order is cyclic**. A group of order 6 cannot have a subgroup of order 4. The number of cosets of H in G is |G|/|H|. The *converse* of Lagrange fails in general (A₄ has order 12 but no subgroup of order 6).")]),
           dict(h="Cyclic groups", md="""A group is **cyclic** if one element g (a *generator*) produces everything: G = {gᵏ}. Facts for a cyclic group of order n:

- Every subgroup is cyclic, and there is **exactly one subgroup for each divisor of n**.
- Number of **generators** = **φ(n)**.
- Number of elements of order d (for d | n) = **φ(d)**.
- An element aᵏ has order n / gcd(k, n).

Z_p* for a prime p is cyclic of order p − 1. The group (Z₈*, ×) = {1, 3, 5, 7} is **not** cyclic (every element has order ≤ 2) — it is the Klein four-group."""),
       ],
       examples=[
           Ex("Generators of Z₁₂", "How many generators does the cyclic group (Z₁₂, +) have, and what are they?",
              ["An element k generates Z₁₂ iff gcd(k, 12) = 1.", "Numbers in 1..11 coprime to 12: 1, 5, 7, 11.", "Count = φ(12) = 12·(1 − ½)(1 − ⅓) = **4**."],
              "**4** generators: 1, 5, 7, 11.", verify=lambda: str(sum(1 for k in range(1, 12) if math.gcd(k, 12) == 1))),
           Ex("Order of a permutation", "Find the order of the permutation (1 2 3)(4 5) in S₅.",
              ["It is a product of disjoint cycles of lengths 3 and 2.", "Order = lcm(3, 2) = **6**."],
              "**6**", verify=lambda: str(math.lcm(3, 2))),
           Ex("Is it a group?", "Is {1, 2, 3, 4} under multiplication mod 5 a group?",
              ["Closure: all products mod 5 stay in {1,2,3,4} (no product is divisible by 5) ✔.", "Identity: 1 ✔.", "Inverses: 1⁻¹=1, 2⁻¹=3, 3⁻¹=2, 4⁻¹=4 ✔. Associativity is inherited from ℤ.",
               "So it is a group — in fact **cyclic of order 4**, generated by 2 (2, 4, 3, 1)."],
              "Yes, a cyclic group of order 4.", verify=lambda: "Yes" if _is_group([1, 2, 3, 4], lambda a, b: (a * b) % 5) else "No"),
           Ex("Subgroups of Z₁₈", "How many subgroups does Z₁₈ have?",
              ["A cyclic group has exactly one subgroup per divisor of its order.", "Divisors of 18: 1, 2, 3, 6, 9, 18 → **6** subgroups."],
              "**6**", verify=lambda: str(len(_divs(18)))),
           Ex("Elements of a given order", "How many elements of order 4 does Z₁₂ have?",
              ["4 divides 12, so the count is φ(4).", "φ(4) = 2 (the elements 3 and 9)."],
              "**2**", verify=lambda: str(sum(1 for a in range(12) if 12 // math.gcd(a, 12) == 4))),
       ],
       traps=[("Zₙ under multiplication", "(Zₙ, ×) is not a group (0 has no inverse). The group is Zₙ* — only units."),
              ("Converse of Lagrange", "A divisor of |G| need not be the order of a subgroup. Only for cyclic groups does every divisor appear."),
              ("Order of a permutation = sum of cycle lengths", "It is the **lcm**, not the sum or product."),
              ("Subgroup test", "A non-empty closed subset of a *finite* group is a subgroup, but for infinite groups you must check inverses (ℕ ⊂ ℤ is closed but not a subgroup).")],
       quick=[("A group has order 17. How many subgroups does it have?", ["1", "2", "17", "16"], 1, "17 is prime, so only {e} and G."),
              ("Number of generators of Z₁₀:", ["2", "4", "5", "9"], 1, "φ(10) = 4 (1, 3, 7, 9)."),
              ("Which cannot be the order of a subgroup of a group of order 20?", ["4", "5", "8", "10"], 2, "8 does not divide 20."),
              ("Order of the 4-cycle (1 2 3 4) in S₄:", ["2", "3", "4", "24"], 2, "A k-cycle has order k.")],
       summary=["Group = closure + associativity + identity + inverses.", "Zₙ under + is a cyclic group of order n; Zₙ* under × has order φ(n).", "Order of a permutation = lcm of its cycle lengths; |Sₙ| = n!.",
                "Lagrange: subgroup order divides group order; prime order ⇒ cyclic.", "Cyclic of order n: φ(n) generators, one subgroup per divisor, φ(d) elements of order d.", "(Z₈*, ×) is not cyclic."])

# ======================================================================================================
def _degseq_edges(seq):
    return sum(seq) // 2


lesson(subject=S, chapter="Graph Theory", ch_no=5, no=1, slug="engm-graph-basics", title="Graphs: Degrees, Paths, Euler & Hamilton",
       topic="Graph Theory", minutes=18, weight=5, widget="graph",
       widget_hint="Type edges like A-B, B-C or pick a preset. The tool reports degrees, connectivity, bipartiteness, Euler path/circuit, chromatic number and the planarity edge bound.",
       key="A graph is vertices joined by edges. The handshake lemma (sum of degrees = 2·edges) and the Euler-circuit rule (connected and every degree even) answer a large fraction of GATE graph questions.",
       analogy=("🌉", "The bridges of Königsberg", "Can you walk across every bridge exactly once and return home? Euler solved it in 1736 by ignoring the geography: only the *number of bridges at each land mass* matters. If any land mass has an odd number of bridges, a closed walk is impossible. That insight started graph theory."),
       sections=[
           dict(h="Vocabulary", md="""A **graph** G = (V, E). *Simple* means no loops or multiple edges. The **degree** of a vertex is the number of edges at it.

- **Walk / trail / path:** a walk may repeat anything; a trail repeats no edge; a **path** repeats no vertex. A **cycle** is a closed path.
- **Connected:** a path exists between every pair. The maximal connected pieces are **components**.
- **Subgraph**, **spanning subgraph**, **induced subgraph**; the **complement** Ḡ has the missing edges.
- **Directed graph:** edges have direction; each vertex has *in-degree* and *out-degree*."""),
           dict(h="The handshake lemma", md="""Every edge has two ends, so:""",
                formulas=[("Σ deg(v) = 2·|E|", "handshake lemma")],
                call=[("key", "Immediate consequences", "The number of **odd-degree vertices is always even**. A graph with degrees (3, 3, 2, 2, 2) has (3+3+2+2+2)/2 = **6** edges. A degree sequence with an odd sum is impossible.")]),
           dict(h="Special graphs and their counts", md="""| Graph | Vertices | Edges | Notes |
|---|---|---|---|
| Complete **Kₙ** | n | **n(n−1)/2** | every pair adjacent, χ = n |
| Cycle **Cₙ** | n | n | bipartite iff n even |
| Path **Pₙ** | n | n − 1 | a tree |
| Complete bipartite **K_{m,n}** | m + n | **m·n** | bipartite, χ = 2 |
| Wheel **Wₙ** | n + 1 | 2n | hub + Cₙ |
| Hypercube **Qₙ** | **2ⁿ** | **n·2ⁿ⁻¹** | n-regular, bipartite |
| Petersen | 10 | 15 | 3-regular, non-planar |

A graph is **bipartite** iff it has **no odd cycle** (equivalently, 2-colourable). The complement of a graph with e edges on n vertices has n(n−1)/2 − e edges."""),
           dict(h="Euler and Hamilton", md="""**Euler** (every *edge* once):

- Connected graph has an **Euler circuit** ⇔ **every vertex has even degree**.
- It has an **Euler path** (not closed) ⇔ **exactly two** vertices have odd degree (the path starts and ends there).
- Directed version: in-degree = out-degree at every vertex.

**Hamilton** (every *vertex* once): no simple characterisation (NP-complete). Useful sufficient conditions: **Dirac** — if n ≥ 3 and every vertex has degree ≥ n/2, a Hamiltonian cycle exists; **Ore** — deg(u) + deg(v) ≥ n for every non-adjacent pair.""",
                call=[("trap", "Euler ≠ Hamilton", "Euler is about edges and has a clean degree test. Hamilton is about vertices and has no clean test. A graph can have one without the other.")]),
           dict(h="Connectivity", md="""A **cut vertex** (articulation point) is a vertex whose removal disconnects the graph; a **bridge** is an edge with that property. The **vertex connectivity** κ(G) is the minimum number of vertices to remove; **edge connectivity** λ(G) the minimum edges, with κ ≤ λ ≤ δ (min degree).

A disconnected simple graph on n vertices has at most **C(n−1, 2)** edges (take K_{n−1} plus an isolated vertex). A connected graph needs at least **n − 1** edges."""),
       ],
       examples=[
           Ex("Edges from a degree sequence", "A simple graph has degrees (3, 3, 2, 2, 2). How many edges does it have?",
              ["Sum of degrees = 3 + 3 + 2 + 2 + 2 = 12.", "Handshake: |E| = 12 / 2 = **6**."],
              "**6**", verify=lambda: str(_degseq_edges([3, 3, 2, 2, 2]))),
           Ex("Hypercube Q₄", "How many edges does the 4-dimensional hypercube Q₄ have?",
              ["Q₄ has 2⁴ = 16 vertices, each of degree 4.", "Edges = 16·4/2 = **32** (formula n·2ⁿ⁻¹ = 4·8)."],
              "**32**", verify=lambda: str(sum(1 for u in range(16) for v in range(u + 1, 16) if bin(u ^ v).count("1") == 1))),
           Ex("Euler circuit test", "A connected graph has degrees (4, 4, 2, 2, 2, 2). Does it have an Euler circuit? What if the degrees are (4, 3, 3, 2, 2, 2)?",
              ["First: all degrees are even ⇒ **Euler circuit exists**.", "Second: two vertices (the 3s) have odd degree ⇒ **no circuit**, but an **Euler path** exists between them."],
              "First: circuit; second: only an Euler path.", verify=lambda: "circuit" if all(d % 2 == 0 for d in (4, 4, 2, 2, 2, 2)) and sum(d % 2 for d in (4, 3, 3, 2, 2, 2)) == 2 else "no"),
           Ex("Maximum edges when disconnected", "What is the maximum number of edges in a simple graph with 8 vertices that is NOT connected?",
              ["The best you can do is a complete graph on 7 vertices plus one isolated vertex.", "C(7, 2) = **21**."],
              "**21**", verify=lambda: str(math.comb(7, 2))),
       ],
       traps=[("Odd degree sum", "Σdeg must be even; if a question lists degrees summing to an odd number, no such graph exists."),
              ("Confusing Euler and Hamilton", "Euler circuit ⇔ all degrees even (connected). Hamilton has no such test — don't invent one."),
              ("K_{m,n} edge count", "m·n, not m + n."),
              ("Forgetting connectivity in Euler's theorem", "Even degrees alone are not enough: two disjoint triangles have all degrees 2 but no circuit through everything.")],
       quick=[("Number of edges in K₁₀:", ["45", "90", "10", "55"], 0, "10·9/2 = 45."),
              ("A connected graph has an Euler circuit iff", ["it has no cycle", "all vertices have even degree", "exactly two vertices have odd degree", "it is bipartite"], 1, "Euler's theorem."),
              ("A simple graph has 5 vertices with degrees (4, 4, 4, 4, x). The largest possible integer x is", ["4", "3", "2", "0"], 0, "A degree 4 in a 5-vertex simple graph means adjacent to all, so x must be 4 (K₅)."),
              ("A bipartite graph can never contain", ["a cycle of length 4", "an odd cycle", "a path of length 5", "a vertex of degree 3"], 1, "Odd cycles destroy 2-colourability.")],
       summary=["Handshake: Σdeg = 2|E|; the number of odd-degree vertices is even.", "Kₙ has n(n−1)/2 edges; K_{m,n} has mn; Qₙ has n·2ⁿ⁻¹.", "Euler circuit ⇔ connected + all degrees even; Euler path ⇔ exactly 2 odd vertices.",
                "Hamilton has no clean test; Dirac (deg ≥ n/2) is sufficient.", "Bipartite ⇔ no odd cycle ⇔ 2-colourable.", "Disconnected simple graph: at most C(n−1, 2) edges."])

# ======================================================================================================
def _spanning_trees(n):
    # Kirchhoff: determinant of Laplacian with one row/col removed, for K_n
    L = [[(n - 1 if i == j else -1) for j in range(n - 1)] for i in range(n - 1)]
    M = [[Fraction(x) for x in r] for r in L]
    det = Fraction(1)
    for c in range(n - 1):
        p = next(i for i in range(c, n - 1) if M[i][c] != 0)
        if p != c:
            M[c], M[p] = M[p], M[c]; det *= -1
        det *= M[c][c]
        for i in range(c + 1, n - 1):
            f = M[i][c] / M[c][c]
            M[i] = [a - f * b for a, b in zip(M[i], M[c])]
    return int(det)


def _chi(n, edges):
    for k in range(1, n + 1):
        for col in itertools.product(range(k), repeat=n):
            if all(col[a] != col[b] for a, b in edges):
                return k


def _wheel(n):
    return [(0, i) for i in range(1, n + 1)] + [(i, i % n + 1) for i in range(1, n + 1)]


def _cycle_colourings(n, k):
    return sum(1 for col in itertools.product(range(k), repeat=n) if all(col[i] != col[(i + 1) % n] for i in range(n)))


lesson(subject=S, chapter="Graph Theory", ch_no=5, no=2, slug="engm-graph-trees-planar-colouring", title="Trees, Planarity, Colouring & Matching",
       topic="Graph Theory", minutes=20, weight=5, widget="graph",
       widget_hint="Try K4, K3,3 and Cycle C5 from the presets and read off the chromatic number and the planar edge bound E ≤ 3V − 6.",
       key="A tree is a connected graph with no cycle (n − 1 edges). Planar graphs satisfy V − E + F = 2 and E ≤ 3V − 6; colouring asks for the fewest colours χ(G); and in bipartite graphs, max matching = min vertex cover (König).",
       analogy=("📻", "Frequency assignment", "Radio stations that are close must use different frequencies. Draw a vertex per station and an edge between stations that interfere: the **fewest frequencies** needed is the chromatic number. A tree of relay links, meanwhile, is the cheapest network that still connects everyone."),
       sections=[
           dict(h="Trees", md="""A **tree** is a connected acyclic graph. For a graph on n vertices the following are all equivalent to being a tree: connected with **n − 1 edges**; acyclic with n − 1 edges; **unique path** between every pair; minimally connected (removing any edge disconnects it).

- A tree with n ≥ 2 has **at least two leaves** (degree-1 vertices).
- A **spanning tree** of a connected graph is a tree using all its vertices. Number of labelled trees on n vertices (= spanning trees of Kₙ): **nⁿ⁻²** (Cayley). Spanning trees of K_{m,n}: m^(n−1)·n^(m−1); of the cycle Cₙ: n.
- A **forest** with c components on n vertices has n − c edges.
- **Rooted tree** facts: a full m-ary tree with i internal nodes has m·i + 1 vertices and (m − 1)·i + 1 leaves.""",
                formulas=[("# labelled trees on n vertices = n^(n−2)", "Cayley"), ("leaves = (m−1)·i + 1", "full m-ary tree with i internal nodes")]),
           dict(h="Planar graphs", md="""A graph is **planar** if it can be drawn in the plane with no crossing edges. For a connected planar graph, with F counting the outer face:""",
                formulas=[("V − E + F = 2", "Euler's formula (connected planar)"), ("E ≤ 3V − 6", "simple planar, V ≥ 3"), ("E ≤ 2V − 4", "simple planar with no triangle (e.g. bipartite)")],
                call=[("key", "Kuratowski", "A graph is non-planar iff it contains a subdivision of **K₅** or **K₃,₃**. Both violate the edge bounds: K₅ has 10 > 3·5−6 = 9 edges; K₃,₃ has 9 > 2·6−4 = 8 edges. The sum of face degrees equals 2E.")]),
           dict(h="Graph colouring", md="""A **proper colouring** gives adjacent vertices different colours; **χ(G)** is the minimum number of colours.

- χ(Kₙ) = n; χ(bipartite with an edge) = 2; χ(Cₙ) = 2 if n even, **3 if n odd**; χ(tree) = 2.
- **Wheel Wₙ** (hub + Cₙ): χ = 3 if n even, **4 if n odd**.
- Lower bound: χ ≥ size of the largest clique ω. Upper bound: χ ≤ Δ + 1, and (**Brooks**) χ ≤ Δ unless G is a complete graph or an odd cycle.
- **Four colour theorem:** every planar graph has χ ≤ 4.
- Chromatic polynomial: P(Kₙ, k) = k(k−1)…(k−n+1); P(tree on n, k) = k(k−1)ⁿ⁻¹; P(Cₙ, k) = (k−1)ⁿ + (−1)ⁿ(k−1)."""),
           dict(h="Matchings, covers and independent sets", md="""- A **matching** is a set of edges with no shared endpoint; a **perfect matching** covers every vertex (needs an even number of vertices).
- **Hall's theorem** (bipartite, sides X and Y): X can be matched into Y iff |N(S)| ≥ |S| for every subset S ⊆ X.
- A **vertex cover** is a vertex set touching every edge; an **independent set** has no two adjacent vertices. For any graph: **max independent set + min vertex cover = n**.
- **König's theorem:** in a bipartite graph, **maximum matching = minimum vertex cover**.
- Perfect matchings in K₂ₙ: (2n − 1)!! = (2n−1)(2n−3)…3·1."""),
       ],
       examples=[
           Ex("Faces of a planar graph", "A connected planar graph has 10 vertices and 15 edges. How many faces does it have?",
              ["Euler: V − E + F = 2.", "10 − 15 + F = 2 ⇒ F = **7**."],
              "**7** faces (including the outer face).", verify=lambda: str(2 - 10 + 15)),
           Ex("Spanning trees of K₅", "How many spanning trees does K₅ have?",
              ["Cayley's formula: nⁿ⁻² = 5³ = **125**.", "(Check with Kirchhoff's matrix-tree theorem: the determinant of the 4×4 reduced Laplacian of K₅ is also 125.)"],
              "**125**", verify=lambda: str(_spanning_trees(5))),
           Ex("Chromatic number of a wheel", "Find χ(W₅), the wheel with a hub joined to a 5-cycle.",
              ["The 5-cycle is an odd cycle, so it needs 3 colours.", "The hub is adjacent to every rim vertex, so it needs a 4th colour.", "χ(W₅) = **4**."],
              "**4**", verify=lambda: str(_chi(6, _wheel(5)))),
           Ex("Proper 3-colourings of a 4-cycle", "In how many ways can the vertices of C₄ be properly coloured with 3 colours?",
              ["Use P(Cₙ, k) = (k − 1)ⁿ + (−1)ⁿ (k − 1).", "= 2⁴ + 2 = 16 + 2 = **18**."],
              "**18**", verify=lambda: str(_cycle_colourings(4, 3))),
           Ex("Why K₃,₃ is not planar", "Use an edge bound to show K₃,₃ is not planar.",
              ["K₃,₃ has V = 6, E = 9 and contains no triangle (it is bipartite).", "For a triangle-free planar graph E ≤ 2V − 4 = 8.", "9 > 8, so K₃,₃ **cannot** be planar."],
              "9 edges exceed the bound 2V − 4 = 8, so K₃,₃ is non-planar."),
       ],
       traps=[("Using E ≤ 3V − 6 as a planarity test", "It is only a necessary condition. K₃,₃ satisfies 9 ≤ 12 yet is non-planar — use the triangle-free bound 2V − 4 or Kuratowski."),
              ("Forgetting the outer face", "Euler's formula counts the unbounded face too."),
              ("χ of an odd cycle or odd wheel", "Odd cycle → 3 colours; odd wheel → 4. Even versions drop by one."),
              ("Cayley's formula counts labelled trees", "It counts spanning trees of the *labelled* complete graph; unlabelled trees on n vertices are far fewer.")],
       quick=[("A tree has 12 vertices. Its number of edges is", ["11", "12", "13", "66"], 0, "n − 1 = 11."),
              ("Which graph is NOT planar?", ["K₄", "C₇", "K₃,₃", "a tree"], 2, "K₃,₃ is one of Kuratowski's two forbidden graphs."),
              ("The chromatic number of any non-empty tree is", ["1", "2", "3", "depends on the degree"], 1, "Trees are bipartite."),
              ("In a bipartite graph, the size of a maximum matching equals", ["the minimum vertex cover", "the number of edges", "the maximum degree", "the number of vertices / 2"], 0, "König's theorem.")],
       summary=["Tree: connected + acyclic ⇔ connected with n − 1 edges ⇔ unique paths; ≥ 2 leaves.", "Labelled trees on n vertices: nⁿ⁻² (Cayley).", "Planar: V − E + F = 2; E ≤ 3V − 6; triangle-free E ≤ 2V − 4; K₅ and K₃,₃ are non-planar.",
                "χ(Kₙ)=n; χ(Cₙ)=2 or 3; χ(Wₙ)=3 or 4; every planar graph is 4-colourable.", "Max independent set + min vertex cover = n; König: bipartite max matching = min vertex cover.", "Hall: X matches into Y iff |N(S)| ≥ |S| for all S ⊆ X."])

# ======================================================================================================
def _count_mississippi():
    from collections import Counter
    w = "MISSISSIPPI"
    return math.factorial(len(w)) // math.prod(math.factorial(c) for c in Counter(w).values())


lesson(subject=S, chapter="Combinatorics & Recurrences", ch_no=6, no=1, slug="engm-counting-basics", title="Counting: Permutations, Combinations & Stars-and-Bars",
       topic="Combinatorics & Recurrences", minutes=20, weight=5, widget="counting",
       widget_hint="Enter n and k to see n!, P(n,k), C(n,k), the stars-and-bars count, derangements and Catalan numbers, with Pascal's triangle highlighted.",
       key="Multiply when you make independent choices (product rule), add when you pick one of several disjoint cases (sum rule). Order matters → permutations P(n,k); order doesn't → combinations C(n,k); identical items into boxes → stars and bars.",
       analogy=("🍕", "Building a pizza order", "Choose 1 of 3 crusts AND 1 of 5 sauces AND 1 of 4 toppings: independent choices multiply → 3·5·4 = 60 pizzas. If instead you choose *either* a vegetarian *or* a non-vegetarian special (disjoint menus), you add the menu sizes."),
       sections=[
           dict(h="The two basic rules", md="""- **Product rule:** if a task has k steps with n₁, n₂, …, n_k options (each independent of the choices made earlier), there are **n₁·n₂·…·n_k** ways.
- **Sum rule:** if a task can be done in exactly one of several mutually exclusive ways with m₁, m₂, … options, there are **m₁ + m₂ + …** ways.

Technique: split into cases (sum rule) and within each case count by stages (product rule). *Count the complement* when “at least one” is easier as “total − none”."""),
           dict(h="Permutations and combinations", md="""| Situation | Count |
|---|---|
| Arrange all n distinct objects in a row | **n!** |
| Arrange k of n distinct objects (order matters) | **P(n,k) = n!/(n−k)!** |
| Choose k of n (order doesn't matter) | **C(n,k) = n!/(k!(n−k)!)** |
| Arrange n objects in a **circle** (rotations equal) | **(n−1)!** |
| Arrange n objects with repeats (m₁ of one kind, m₂ of another, …) | **n!/(m₁! m₂! …)** |

Symmetry: C(n,k) = C(n, n−k). Pascal: C(n,k) = C(n−1,k−1) + C(n−1,k). Also Σₖ C(n,k) = 2ⁿ and Σₖ (−1)ᵏ C(n,k) = 0.""",
                call=[("tip", "Order or no order?", "Ask: if I swap two chosen items, is it a different outcome? Yes → permutation. No → combination. A committee is a combination; a president/secretary pair is a permutation.")]),
           dict(h="Repetition and stars-and-bars", md="""Distributing **k identical** items into **n distinct** boxes:""",
                formulas=[("non-negative solutions of x₁+…+xₙ = k :  C(k+n−1, n−1)", "stars and bars"), ("positive solutions (each xᵢ ≥ 1) :  C(k−1, n−1)", "give 1 to each first")],
                call=[("key", "Lower bounds", "For xᵢ ≥ aᵢ, subtract the minimums first: substitute yᵢ = xᵢ − aᵢ and count non-negative solutions of the reduced equation.")]),
           dict(h="Binomial theorem and lattice paths", md="""**(x + y)ⁿ = Σₖ C(n,k) xᵏ yⁿ⁻ᵏ.** The coefficient of xᵏyⁿ⁻ᵏ in (ax + by)ⁿ is **C(n,k)·aᵏ·bⁿ⁻ᵏ**. The multinomial version: (x₁+…+x_r)ⁿ has coefficients n!/(k₁!…k_r!).

**Grid paths:** moving only right/up from (0,0) to (a,b) takes a rights and b ups in some order: **C(a+b, a)** paths. Paths that must pass through a given point multiply the two segment counts.

**Catalan numbers** Cₙ = C(2n,n)/(n+1) count binary trees with n nodes, balanced bracket strings of n pairs, and monotone lattice paths that never cross the diagonal: 1, 1, 2, 5, 14, 42, 132…"""),
       ],
       examples=[
           Ex("Arranging letters with repeats", "How many distinct arrangements of the letters of MISSISSIPPI are there?",
              ["11 letters: M×1, I×4, S×4, P×2.", "Arrangements = 11! / (1!·4!·4!·2!) = 39916800 / (24·24·2) = **34650**."],
              "**34650**", verify=lambda: str(_count_mississippi())),
           Ex("Stars and bars with lower bounds", "Find the number of integer solutions of x₁ + x₂ + x₃ + x₄ = 12 with each xᵢ ≥ 2.",
              ["Put yᵢ = xᵢ − 2 ≥ 0. Then y₁ + … + y₄ = 12 − 8 = 4.", "Non-negative solutions: C(4 + 4 − 1, 4 − 1) = C(7, 3) = **35**."],
              "**35**", verify=lambda: str(sum(1 for t in itertools.product(range(13), repeat=4) if sum(t) == 12 and min(t) >= 2))),
           Ex("Circular arrangement with a pair together", "In how many ways can 7 people sit around a round table if two particular people must sit together?",
              ["Glue the pair into one block: now 6 objects around a circle → (6 − 1)! = 120 arrangements.", "The pair can swap inside the block: ×2.", "Total = 120 × 2 = **240**."],
              "**240**", verify=lambda: str(_circular_pair_together(7))),
           Ex("Coefficient extraction", "Find the coefficient of x³y² in the expansion of (2x + y)⁵.",
              ["General term C(5,k)(2x)ᵏ yⁿ⁻ᵏ; we need k = 3.", "C(5,3)·2³·1² = 10·8 = **80**."],
              "**80**", verify=lambda: str(math.comb(5, 3) * 2 ** 3)),
           Ex("Lattice paths", "How many shortest paths go from (0,0) to (4,3) using steps right and up?",
              ["Each path has 4 rights and 3 ups = 7 steps.", "Choose which 3 of the 7 steps are ups: C(7,3) = **35**."],
              "**35**", verify=lambda: str(math.comb(7, 3))),
       ],
       traps=[("Using nᵏ for selection without repetition", "Picking k distinct items from n with order is P(n,k), not nᵏ (that is *with* repetition)."),
              ("Circular arrangements", "Divide by n for rotations: (n−1)!, not n!. For necklaces that can also be flipped, divide by 2 again."),
              ("Stars and bars with bounds", "Subtract the lower bounds **before** applying C(k+n−1, n−1)."),
              ("Double counting", "If you count by choosing a ‘first item’ then the rest, make sure each outcome arises exactly once.")],
       quick=[("Number of ways to choose a committee of 3 from 8 people:", ["24", "56", "336", "512"], 1, "C(8,3) = 56."),
              ("Non-negative integer solutions of a + b + c = 7:", ["36", "15", "21", "35"], 0, "C(9,2) = 36."),
              ("Distinct arrangements of the letters in BANANA:", ["60", "120", "720", "30"], 0, "6!/(3!·2!) = 60."),
              ("Σₖ C(10, k) equals", ["100", "512", "1024", "2048"], 2, "2¹⁰ = 1024.")],
       summary=["Product rule for stages, sum rule for disjoint cases; count the complement for ‘at least one’.", "P(n,k) = n!/(n−k)!; C(n,k) = n!/(k!(n−k)!); circular: (n−1)!.", "Repeats: n!/(m₁!m₂!…).",
                "Stars and bars: C(k+n−1, n−1) non-negative; C(k−1, n−1) positive.", "Binomial: coefficient of xᵏyⁿ⁻ᵏ in (ax+by)ⁿ is C(n,k)aᵏbⁿ⁻ᵏ.", "Grid paths C(a+b, a); Catalan Cₙ = C(2n,n)/(n+1)."])

# ======================================================================================================
def _der(n):
    d = [1, 0]
    for i in range(2, n + 1):
        d.append((i - 1) * (d[-1] + d[-2]))
    return d[n]


def _rec(n):
    a, b = 1, 4
    for _ in range(n - 1):
        a, b = b, 5 * b - 6 * a
    return b if n >= 1 else a


lesson(subject=S, chapter="Combinatorics & Recurrences", ch_no=6, no=2, slug="engm-pie-pigeonhole-recurrence", title="Inclusion–Exclusion, Derangements, Pigeonhole & Recurrences",
       topic="Combinatorics & Recurrences", minutes=22, weight=5, widget="counting",
       widget_hint="Use the calculator for derangements D(n) and Catalan numbers; compare D(n) with n!/e.",
       key="Inclusion–exclusion counts objects avoiding several properties (derangements, onto functions, coprimes); the pigeonhole principle proves that some collision must happen; and linear recurrences are solved through their characteristic equation.",
       analogy=("🧦", "Socks in a dark room", "You have 4 colours of socks mixed in a drawer. In the dark, how many must you grab to be **sure** of a matching pair? Four grabs could all differ, so the **fifth** guarantees a pair. That is the pigeonhole principle: more items than boxes forces two in one box."),
       sections=[
           dict(h="Inclusion–exclusion for ‘avoid all properties’", md="""To count objects having **none** of the properties P₁…P_m:""",
                formulas=[("N(none) = N − Σ N(Pᵢ) + Σ N(Pᵢ∧Pⱼ) − Σ N(Pᵢ∧Pⱼ∧Pₖ) + …", "alternating sum")],
                call=[("tip", "Uses", "Euler's φ(n) (numbers ≤ n with none of the prime factors), onto functions, derangements, and ‘no two adjacent’ arrangements are all instances of this one formula.")]),
           dict(h="Derangements", md="""A **derangement** is a permutation with **no fixed point** (nobody gets their own hat). Using inclusion–exclusion on ‘object i is fixed’:""",
                formulas=[("Dₙ = n! · Σ_{k=0..n} (−1)ᵏ / k!", "≈ n!/e (rounded)"), ("Dₙ = (n−1)(Dₙ₋₁ + Dₙ₋₂)", "recurrence;  D₀=1, D₁=0")],
                call=[("key", "Values to remember", "D₂ = 1, D₃ = 2, D₄ = 9, D₅ = 44, D₆ = 265. Probability that a random permutation is a derangement → 1/e ≈ 0.368.")]),
           dict(h="Pigeonhole principle", md="""- **Basic:** placing n + 1 objects into n boxes puts at least 2 in some box.
- **Generalised:** N objects in k boxes ⇒ some box has at least **⌈N/k⌉** objects.
- To **guarantee** r objects of the same kind with k kinds you need **k(r − 1) + 1** objects.

Typical GATE phrasing: socks/gloves, birthdays (367 people guarantee a shared birthday), numbers divisible by n (among any n + 1 integers two have the same remainder mod n), and subsets of {1..2n} forcing a pair summing to 2n+1 (choose n + 1 numbers)."""),
           dict(h="Linear recurrence relations", md="""A **linear homogeneous recurrence with constant coefficients** of order 2: aₙ = c₁aₙ₋₁ + c₂aₙ₋₂. Solve via the **characteristic equation** r² − c₁r − c₂ = 0.

- **Distinct roots r₁, r₂:** aₙ = A·r₁ⁿ + B·r₂ⁿ.
- **Repeated root r:** aₙ = (A + Bn)·rⁿ.
- **Complex roots:** use polar form (rare in GATE).
- Find A, B from the two initial conditions.

**Non-homogeneous** (extra term f(n)): total solution = homogeneous part + a particular solution (try a constant, a polynomial of the same degree, or c·sⁿ matching f). Classic recurrences: Fibonacci Fₙ = Fₙ₋₁ + Fₙ₋₂; Tower of Hanoi Tₙ = 2Tₙ₋₁ + 1 ⇒ **2ⁿ − 1**; binary-search/merge-style Tₙ = 2Tₙ/₂ + n.""",
                call=[("trap", "Don't forget initial conditions", "A and B come from a₀ and a₁ — the general solution alone is not the answer.")]),
           dict(h="Generating functions in one minute", md="""The generating function of a sequence is G(x) = Σ aₙxⁿ. Key series: 1/(1−x) = Σxⁿ; 1/(1−x)^k has coefficient **C(n+k−1, k−1)** of xⁿ; (1+x)ⁿ has coefficient C(n,k).

A counting problem ‘choose objects from several types with limits’ becomes a **product of polynomials**, and the answer is the coefficient of xᵏ. For example the number of non-negative solutions of x₁+x₂+x₃ = 5 is the coefficient of x⁵ in (1/(1−x))³ = C(7,2) = 21."""),
       ],
       examples=[
           Ex("Derangements of 5", "How many ways can 5 people each take a hat so that nobody gets their own?",
              ["D₅ = 5!(1 − 1 + 1/2 − 1/6 + 1/24 − 1/120).", "= 120·(1/2 − 1/6 + 1/24 − 1/120) = 60 − 20 + 5 − 1 = **44**.", "Check with the recurrence: D₅ = 4(D₄ + D₃) = 4(9 + 2) = 44."],
              "**44**", verify=lambda: str(sum(1 for p in itertools.permutations(range(5)) if all(p[i] != i for i in range(5))))),
           Ex("Solve a recurrence", "Solve aₙ = 5aₙ₋₁ − 6aₙ₋₂ with a₀ = 1, a₁ = 4, and find a₁₀.",
              ["Characteristic equation r² − 5r + 6 = 0 ⇒ r = 2, 3.", "aₙ = A·2ⁿ + B·3ⁿ. From a₀: A + B = 1; from a₁: 2A + 3B = 4 ⇒ B = 2, A = −1.", "So aₙ = 2·3ⁿ − 2ⁿ. Check a₂: 5·4 − 6·1 = 14 and 2·9 − 4 = 14 ✔.",
               "a₁₀ = 2·3¹⁰ − 2¹⁰ = 2·59049 − 1024 = **117074**."],
              "aₙ = 2·3ⁿ − 2ⁿ, so a₁₀ = **117074**.", verify=lambda: str(_rec(10))),
           Ex("Pigeonhole with socks", "A drawer has socks of 4 colours. What is the minimum number you must pick (without looking) to be sure of 3 socks of the same colour?",
              ["Worst case: 2 of each colour = 8 socks with no triple.", "The 9th sock forces a triple: k(r − 1) + 1 = 4·2 + 1 = **9**."],
              "**9**", verify=lambda: str(4 * (3 - 1) + 1)),
           Ex("Coprime counting", "How many integers from 1 to 30 are coprime to 30?",
              ["Prime factors of 30: 2, 3, 5. Count integers divisible by none of them.", "30 − (15 + 10 + 6) + (5 + 3 + 2) − 1 = 30 − 31 + 10 − 1 = **8**.", "Equals φ(30) = 30·(1/2)(2/3)(4/5) = 8."],
              "**8**", verify=lambda: str(sum(1 for k in range(1, 31) if math.gcd(k, 30) == 1))),
           Ex("Generating-function coefficient", "How many non-negative integer solutions does x₁ + x₂ + x₃ = 5 have?",
              ["The generating function is (1/(1−x))³.", "Coefficient of x⁵ = C(5 + 3 − 1, 3 − 1) = C(7, 2) = **21**."],
              "**21**", verify=lambda: str(sum(1 for t in itertools.product(range(6), repeat=3) if sum(t) == 5))),
       ],
       traps=[("Derangement recurrence", "Dₙ = (n−1)(Dₙ₋₁ + Dₙ₋₂), **not** n·Dₙ₋₁. Check with D₃ = 2·(0 + 1) = 2."),
              ("Pigeonhole ‘guarantee’", "For r of one kind among k kinds you need k(r−1) + 1, not k·r."),
              ("Forgetting initial conditions", "The characteristic roots give a family of solutions; the initial values pick the right one."),
              ("Repeated roots", "If r is a double root the solution is (A + Bn)rⁿ — using A·rⁿ + B·rⁿ collapses to one constant and loses a solution.")],
       quick=[("D₄, the number of derangements of 4 objects, is", ["6", "9", "12", "24"], 1, "D₄ = 4!(1 − 1 + 1/2 − 1/6 + 1/24) = 9."),
              ("Among any 13 people, at least ___ share a birth month.", ["1", "2", "3", "13"], 1, "13 people, 12 months ⇒ ⌈13/12⌉ = 2."),
              ("The recurrence Tₙ = 2Tₙ₋₁ + 1 with T₀ = 0 has solution", ["2ⁿ", "2ⁿ − 1", "2ⁿ + 1", "n²"], 1, "T₁ = 1, T₂ = 3, T₃ = 7 …"),
              ("Characteristic roots of aₙ = 4aₙ₋₁ − 4aₙ₋₂:", ["2 and 2", "1 and 4", "2 and −2", "4 and 4"], 0, "r² − 4r + 4 = (r−2)²: a repeated root.")],
       summary=["Inclusion–exclusion: N − Σ singles + Σ pairs − … counts objects avoiding all properties.", "Dₙ = n!Σ(−1)ᵏ/k! = (n−1)(Dₙ₋₁ + Dₙ₋₂): 1, 0, 1, 2, 9, 44, 265.", "Pigeonhole: N objects, k boxes ⇒ ⌈N/k⌉ in some box; guarantee r of a kind needs k(r−1)+1.",
                "Characteristic equation: distinct roots A r₁ⁿ + B r₂ⁿ; repeated root (A + Bn)rⁿ; use initial conditions.", "Tower of Hanoi: 2ⁿ − 1; Fibonacci grows like φⁿ.", "Generating functions turn counting into coefficient extraction."])
