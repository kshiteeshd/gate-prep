"""In-depth material (proofs, derivations, detailed notes) for the Engineering & Discrete Mathematics lessons."""
from learn import deepen

deepen("engm-logic-propositions",
       proofs=[
           ("De Morgan's laws and P → Q ≡ ¬P ∨ Q",
            """Two formulas are **equivalent** when they have the same truth value under every assignment, so a truth table on the relevant variables is a complete proof.

| P | Q | ¬(P ∧ Q) | ¬P ∨ ¬Q | P → Q | ¬P ∨ Q |
|---|---|---|---|---|---|
| T | T | F | F | T | T |
| T | F | T | T | F | F |
| F | T | T | T | T | T |
| F | F | T | T | T | T |

The columns 3 and 4 agree in all four rows, so ¬(P ∧ Q) ≡ ¬P ∨ ¬Q; columns 5 and 6 agree, so P → Q ≡ ¬P ∨ Q. The second De Morgan law ¬(P ∨ Q) ≡ ¬P ∧ ¬Q follows by applying the first to ¬P and ¬Q and negating both sides. The contrapositive law follows: ¬Q → ¬P ≡ ¬¬Q ∨ ¬P ≡ Q ∨ ¬P ≡ ¬P ∨ Q ≡ P → Q."""),
           ("There are exactly 2^(2^n) Boolean functions of n variables",
            """A function of n Boolean variables is determined by its truth table, which has one row for each of the 2ⁿ input combinations. For every row we may choose the output independently as 0 or 1. By the product rule the number of tables is 2 × 2 × … × 2 (2ⁿ factors) = **2^(2ⁿ)**. For n = 2 this gives 16 (AND, OR, XOR, NAND, implication, the constants and so on), for n = 3 it gives 256."""),
           ("{¬, ∧} is functionally complete",
            """We must express every connective with only negation and conjunction.

- P ∨ Q ≡ ¬(¬P ∧ ¬Q) by De Morgan.
- P → Q ≡ ¬P ∨ Q ≡ ¬(P ∧ ¬Q).
- P ↔ Q ≡ (P → Q) ∧ (Q → P).
- P ⊕ Q ≡ ¬(P ↔ Q).

Since every formula is built from these connectives (and any truth table can be written in disjunctive normal form), {¬, ∧} suffices. Similarly {¬, ∨} is complete, and NAND alone is complete because ¬P ≡ P NAND P and P ∧ Q ≡ ¬(P NAND Q)."""),
       ],
       notes=[
           ("Operator precedence and the implication trap",
            """The usual order of binding is ¬, then ∧, then ∨, then →, then ↔. Implication is **right associative**: P → Q → R means P → (Q → R), which is *not* the same as (P → Q) → R. The conditional is false in exactly one situation (true antecedent, false consequent); a conditional with a false antecedent is **vacuously true**, which is why ‘if 1 = 2 then the moon is cheese’ is a true statement.

Memorise the related forms of P → Q: the **converse** Q → P and the **inverse** ¬P → ¬Q are equivalent to each other but not to the original; the **contrapositive** ¬Q → ¬P is equivalent to the original."""),
           ("Counting tautologies and satisfying assignments",
            """A formula in n variables has 2ⁿ rows. It is a **tautology** if it is true in all of them, a **contradiction** if it is false in all of them and **satisfiable** if it is true in at least one. A formula is valid exactly when its negation is unsatisfiable, which is the idea behind resolution and SAT solvers. For GATE count carefully: for example P → (Q → P) is a tautology because when P is true the inner implication is true, and when P is false the outer implication is vacuously true. A single disjunction of k distinct variables is false in exactly one assignment, so it has 2ⁿ − 1 satisfying assignments when all n variables occur."""),
       ])

deepen("engm-logic-quantifiers",
       proofs=[
           ("Negation of quantifiers: ¬∀x P(x) ≡ ∃x ¬P(x)",
            """Over a domain D, ∀x P(x) is true exactly when every element of D satisfies P. So it is false precisely when at least one element fails P, i.e. when ∃x ¬P(x) holds. Hence ¬∀x P(x) ≡ ∃x ¬P(x). Applying this to ¬P gives ¬∃x P(x) ≡ ∀x ¬P(x). Rule of thumb: pushing a negation through a quantifier flips the quantifier and negates the body; repeat from the outside in."""),
           ("∀ distributes over ∧ but not over ∨; ∃ distributes over ∨ but not over ∧",
            """**∀x (P(x) ∧ Q(x)) ≡ ∀x P(x) ∧ ∀x Q(x)**: if every element satisfies both, then every element satisfies P and every element satisfies Q, and conversely.

**∀x (P(x) ∨ Q(x)) is not equivalent to ∀x P(x) ∨ ∀x Q(x).** Counter-example: domain the integers, P(x) = ‘x is even’, Q(x) = ‘x is odd’. Every integer is even or odd, but it is false that all integers are even and false that all are odd.

Dually **∃x (P ∨ Q) ≡ ∃x P ∨ ∃x Q**, while ∃x (P ∧ Q) only implies ∃x P ∧ ∃x Q: take P = ‘x is even’ and Q = ‘x is odd’; the right side is true but no number is both."""),
           ("Validity of modus ponens and hypothetical syllogism",
            """Modus ponens: from P and P → Q infer Q. The only row of the truth table in which both premises are true is P = T, Q = T, and there the conclusion Q is true, so the argument is valid.

Hypothetical syllogism: from P → Q and Q → R infer P → R. Suppose both premises hold and P is true. Then Q is true by the first premise and R is true by the second, so P → R cannot be false. An argument is valid exactly when (premise₁ ∧ … ∧ premiseₖ) → conclusion is a tautology."""),
       ],
       notes=[
           ("Translating English into logic",
            """‘All A are B’ is ∀x (A(x) → B(x)); it is wrong to write ∀x (A(x) ∧ B(x)) because that claims everything is an A. ‘Some A are B’ is ∃x (A(x) ∧ B(x)); writing ∃x (A(x) → B(x)) is wrong because it is made true by any element that is not an A. ‘No A is B’ is ∀x (A(x) → ¬B(x)). ‘Only A are B’ means ∀x (B(x) → A(x)).

**Order of quantifiers matters:** ∀x ∃y (x < y) is true over the integers (every number has a larger one) but ∃y ∀x (x < y) is false (no single number is larger than all). Swapping two like quantifiers (∀∀ or ∃∃) is harmless; swapping unlike ones is not, although ∃y ∀x P always implies ∀x ∃y P."""),
           ("Rules of inference and resolution",
            """Universal instantiation (∀x P(x) ⊢ P(c)), universal generalisation (P(c) for an arbitrary c ⊢ ∀x P(x)), existential instantiation (∃x P(x) ⊢ P(c) for a fresh c) and existential generalisation (P(c) ⊢ ∃x P(x)) are the four quantifier rules. **Resolution** combines clauses: from (A ∨ B) and (¬A ∨ C) infer (B ∨ C). It is sound and, together with a conversion to clausal form (prenex form, Skolemisation), complete for refutation: to prove a conclusion, add its negation to the premises and derive the empty clause."""),
       ])

deepen("engm-sets-counting",
       proofs=[
           ("|P(S)| = 2ⁿ for a set with n elements",
            """Fix an ordering s₁, …, sₙ of S. Each subset A corresponds to the bit string b₁ … bₙ where bᵢ = 1 exactly when sᵢ ∈ A. This correspondence is a bijection (different subsets give different strings, and every string comes from a subset). There are 2ⁿ bit strings, hence 2ⁿ subsets.

Induction gives the same result: for n = 0 the only subset of ∅ is ∅, so |P(∅)| = 1 = 2⁰. If S has n + 1 elements, pick one element x; the subsets of S not containing x are the 2ⁿ subsets of S ∖ {x}, and those containing x are obtained by adding x to each of these, another 2ⁿ. Total 2·2ⁿ = 2ⁿ⁺¹."""),
           ("Inclusion–exclusion for two and three sets",
            """|A| + |B| counts every element of A ∩ B twice and every other element of A ∪ B once, so subtracting |A ∩ B| once gives |A ∪ B| = |A| + |B| − |A ∩ B|.

For three sets, count |A| + |B| + |C|. An element lying in exactly two sets is counted twice, in all three thrice. Subtract the pairwise intersections: elements in exactly two sets are now counted once, but elements in all three have been counted 3 − 3 = 0 times. Add back |A ∩ B ∩ C| to restore the count of 1:

**Result:** ∣A ∪ B ∪ C∣ = Σ∣A∣ − Σ∣A ∩ B∣ + ∣A ∩ B ∩ C∣.

In general each element in exactly m ≥ 1 of the sets is counted Σ(−1)^(k+1) C(m, k) = 1 time, because Σ_{k=0}^{m} (−1)^k C(m, k) = (1 − 1)^m = 0."""),
           ("The set N × N is countable (zig-zag)",
            """List the pairs by the sum of their coordinates: (0,0); (0,1), (1,0); (0,2), (1,1), (2,0); and so on. Diagonal d contains d + 1 pairs, so every pair (a, b) appears at a finite position, namely d(d + 1)/2 + a with d = a + b. This defines a bijection with N, hence N × N is countable. By contrast, **P(N) is uncountable** (Cantor): if f : N → P(N) were onto, the set D = {n : n ∉ f(n)} would differ from every f(n) at n, a contradiction."""),
       ],
       notes=[
           ("Set identities worth memorising",
            """Absorption A ∪ (A ∩ B) = A; De Morgan (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ; A ∖ B = A ∩ Bᶜ; A Δ B = (A ∖ B) ∪ (B ∖ A) = (A ∪ B) ∖ (A ∩ B), and |A Δ B| = |A| + |B| − 2|A ∩ B|. Counting functions: the number of subsets of S of size k is C(n, k); the number of **partitions** of an n-element set into non-empty blocks is the Bell number Bₙ (1, 1, 2, 5, 15, 52, 203 …). The Cartesian product has |A × B| = |A|·|B|, and a relation from A to B is just a subset of A × B, so there are 2^(|A||B|) of them."""),
           ("Venn-diagram word problems",
            """Write the number of elements in each of the 2ᵏ regions and solve in order from the innermost region (all sets) outwards. With three sets, |A ∪ B ∪ C| = N − |none|, so the count in exactly one set = Σ|A| − 2Σ|A ∩ B| + 3|A ∩ B ∩ C|, and in exactly two sets = Σ|A ∩ B| − 3|A ∩ B ∩ C|. Typical GATE traps: ‘at least one’ vs ‘exactly one’, and forgetting the elements outside all sets."""),
       ])

deepen("engm-relations",
       proofs=[
           ("Counting relations on an n-element set",
            """A relation on A is a subset of A × A, which has n² pairs, so there are **2^(n²)** relations.

- **Reflexive:** the n pairs (a, a) are forced; the other n² − n are free: 2^(n²−n).
- **Symmetric:** pick, for each of the n diagonal pairs and each of the n(n − 1)/2 unordered off-diagonal pairs {a, b}, whether it is present (both orientations come together): 2^(n(n+1)/2).
- **Antisymmetric:** each diagonal pair is free (2ⁿ choices); for each unordered pair {a, b} with a ≠ b we may include neither, only (a, b), or only (b, a) — 3 choices: 2ⁿ · 3^(n(n−1)/2).
- **Asymmetric** (irreflexive and antisymmetric): 3^(n(n−1)/2).
- **Reflexive and symmetric:** 2^(n(n−1)/2)."""),
           ("An equivalence relation is the same as a partition",
            """Let ~ be an equivalence relation on A and let [a] = {x : x ~ a}. Reflexivity gives a ∈ [a], so the classes cover A. If [a] ∩ [b] contains c then c ~ a and c ~ b; by symmetry and transitivity a ~ b, and for any x ∈ [a] we get x ~ a ~ b, so [a] ⊆ [b] and symmetrically [b] ⊆ [a]. Thus two classes are either equal or disjoint: the classes form a partition.

Conversely, given a partition, define a ~ b when a and b lie in the same block. This is reflexive, symmetric and transitive. Hence the number of equivalence relations on an n-set equals the number of partitions, the Bell number Bₙ."""),
           ("Warshall's algorithm computes the transitive closure",
            """Let Rₖ[i][j] be true if there is a path from i to j using only the first k vertices as intermediates. R₀ is the relation itself. A path using vertices 1..k either avoids k (then Rₖ₋₁[i][j] holds) or passes through k once, splitting into a path i → k and a path k → j that use only vertices 1..k−1 internally: Rₖ₋₁[i][k] ∧ Rₖ₋₁[k][j]. Hence **Rₖ[i][j] = Rₖ₋₁[i][j] ∨ (Rₖ₋₁[i][k] ∧ Rₖ₋₁[k][j])**, and Rₙ is the transitive closure. The cost is Θ(n³), the same triple loop as Floyd–Warshall."""),
       ],
       notes=[
           ("Properties at a glance and how to test them",
            """With the matrix M of a relation: reflexive ⇔ all diagonal entries are 1; symmetric ⇔ M = Mᵀ; antisymmetric ⇔ no off-diagonal pair (i, j) and (j, i) both 1; transitive ⇔ M² ≤ M entrywise (Boolean product). The **composition** R∘S has matrix MₛMᵣ in the Boolean product, and Rⁿ has matrix Mⁿ. The **reflexive–transitive closure** is R* = ⋃ Rᵏ for k = 0 … n − 1 on an n-set. The smallest equivalence relation containing R is the transitive closure of R ∪ R⁻¹ ∪ identity."""),
           ("Common GATE patterns",
            """‘Is R reflexive / symmetric / transitive?’ for divisibility, ‘x − y is even’, ‘x ≤ y’, ‘x² = y²’. Remember that the empty relation is symmetric, antisymmetric and transitive but not reflexive (on a non-empty set); the universal relation is an equivalence relation with a single class; and a relation can be both symmetric and antisymmetric (it must then be a subset of the identity). The number of equivalence relations on a 3-set is B₃ = 5; on a 4-set B₄ = 15."""),
       ])

deepen("engm-functions",
       proofs=[
           ("Counting functions, injections, bijections and surjections",
            """A function f : A → B with |A| = m and |B| = n assigns to each of the m inputs one of n outputs independently: **nᵐ** functions. For an injection the outputs must be distinct: the first input has n choices, the second n − 1, … so P(n, m) = n!/(n − m)! (zero if m > n). A bijection needs m = n and gives n!.

**Surjections.** Let Sᵢ be the set of functions whose image misses the i-th element of B. By inclusion–exclusion the number of functions missing at least one element is Σ(−1)^(k+1) C(n, k)(n − k)ᵐ, so the surjections number **Σ_{k=0}^{n} (−1)^k C(n, k) (n − k)ᵐ**. Example: onto functions from a 4-set to a 2-set: 2⁴ − 2·1⁴ = 14; from a 3-set onto a 3-set: 27 − 3·8 + 3·1 = 6 = 3!."""),
           ("Composition: if g∘f is injective then f is injective; if g∘f is onto then g is onto",
            """Suppose g∘f is injective and f(a) = f(b). Applying g gives g(f(a)) = g(f(b)), i.e. (g∘f)(a) = (g∘f)(b), so a = b. Hence f is injective (g need not be).

Suppose g∘f is onto C. For any c ∈ C there is a with g(f(a)) = c, so c is the image of f(a) under g: g is onto (f need not be). The composition of two injections is an injection and of two surjections is a surjection."""),
           ("A function has an inverse exactly when it is a bijection",
            """If f : A → B is injective and surjective, define f⁻¹(b) as the unique a with f(a) = b: it exists by surjectivity and is unique by injectivity. Then f⁻¹(f(a)) = a and f(f⁻¹(b)) = b. Conversely, if f has a two-sided inverse g then f(a) = f(b) implies a = g(f(a)) = g(f(b)) = b (injective), and every b equals f(g(b)) (surjective)."""),
       ],
       notes=[
           ("Pigeonhole consequences for functions",
            """If |A| > |B| no function A → B is injective; if |A| < |B| none is onto; for finite sets of equal size injective ⇔ surjective ⇔ bijective. For infinite sets this fails (n ↦ n + 1 on ℕ is injective but not onto). The floor and ceiling functions satisfy ⌊x⌋ ≤ x < ⌊x⌋ + 1, ⌈x⌉ = −⌊−x⌋, and ⌊n/2⌋ + ⌈n/2⌉ = n. The number of functions from an m-set to an n-set that are **non-decreasing** is C(n + m − 1, m) (stars and bars)."""),
           ("Special functions worth recognising",
            """Identity, constant (not injective unless the domain is a single point), characteristic function of a subset (gives the bijection P(A) ↔ {0,1}^A), the hash function (many-to-one by design), and the modular map x ↦ x mod m (a surjection ℤ → ℤₘ). Counting the **fixed-point-free bijections** of an n-set gives the derangements Dₙ; counting bijections with a given cycle structure leads to Stirling numbers of the first kind."""),
       ])

deepen("engm-posets-lattices",
       proofs=[
           ("The divisibility order on the divisors of n is a lattice",
            """Order the divisors of n by ‘a divides b’. This is reflexive, antisymmetric (a ∣ b and b ∣ a give a = b for positive integers) and transitive, so it is a poset. For divisors a and b, gcd(a, b) divides both and is divisible by every common divisor, so it is the **greatest lower bound**; lcm(a, b) divides n (it divides n because n is a common multiple of a and b), is a multiple of both and divides every common multiple, so it is the **least upper bound**. Every pair has a glb and lub, hence the poset is a lattice. D₃₀ is isomorphic to the Boolean lattice on three atoms {2, 3, 5}."""),
           ("In a lattice the lub and glb are unique, and a lattice with a greatest and least element is bounded",
            """If u and u′ are both least upper bounds of {a, b}, each is an upper bound and each is below every upper bound, so u ≤ u′ and u′ ≤ u; by antisymmetry u = u′. The same argument proves uniqueness of the greatest lower bound. In a **finite** non-empty lattice the join of all elements is a top and the meet of all elements is a bottom, so every finite lattice is bounded."""),
           ("Every finite poset has a minimal element, and a chain/antichain bound",
            """Take any element x₀. If it is not minimal there is x₁ < x₀; if x₁ is not minimal there is x₂ < x₁, and so on. Because the poset is finite the elements cannot repeat (they strictly decrease), so the process stops at a minimal element.

**Mirsky / Dilworth consequence:** if the longest chain has k elements, the poset can be partitioned into k antichains (put each element in the layer given by the longest chain ending at it). In particular a poset with more than rs elements has a chain of length r + 1 or an antichain of size s + 1."""),
       ],
       notes=[
           ("Hasse diagrams and key vocabulary",
            """Draw an edge from x up to y when y covers x (x < y with nothing strictly between). **Maximal/minimal** elements exist in every finite poset; **greatest/least** elements need not. An **antichain** is a set of pairwise incomparable elements; a **chain** is a totally ordered subset. The power set P(S) under ⊆ is a Boolean lattice with 2ⁿ elements, n atoms, and **complements** unique. The number of elements covered by or covering an element, the height (longest chain) and width (largest antichain) are common GATE questions; the width of P(S) is C(n, ⌊n/2⌋) (Sperner)."""),
           ("Distributive, complemented and Boolean lattices",
            """A lattice is **distributive** if a ∧ (b ∨ c) = (a ∧ b) ∨ (a ∧ c) for all a, b, c. A lattice is distributive exactly when it contains no sub-lattice isomorphic to the pentagon N₅ or the diamond M₃. In a distributive lattice complements, when they exist, are unique. A **Boolean lattice** is a complemented distributive lattice with 0 and 1; every finite one is isomorphic to P(S) for some S, so its order is a power of 2. A chain is always distributive; it is complemented only when it has at most two elements."""),
       ])

deepen("engm-groups",
       proofs=[
           ("Uniqueness of the identity and of inverses",
            """If e and e′ are both identities then e = e·e′ (as e′ is an identity) and e·e′ = e′ (as e is an identity), so e = e′. If b and c are both inverses of a, then b = b·e = b·(a·c) = (b·a)·c = e·c = c. The cancellation laws follow: a·b = a·c implies b = c by multiplying on the left by a⁻¹."""),
           ("Lagrange's theorem: |H| divides |G|",
            """Let H be a subgroup of the finite group G. The left coset of g is gH = {gh : h ∈ H}.

1. **Each coset has |H| elements:** h ↦ gh is a bijection H → gH by cancellation.
2. **Two cosets are equal or disjoint:** if x ∈ gH ∩ g′H then x = gh = g′h′, so g′⁻¹g = h′h⁻¹ ∈ H and therefore g′H = gH.
3. **The cosets cover G**, since g ∈ gH.

So G is a disjoint union of k cosets each of size |H|, giving |G| = k·|H|. Corollaries: the order of every element divides |G| (apply the theorem to ⟨g⟩); a group of **prime order p is cyclic** (any non-identity element generates a subgroup of order dividing p, hence p); and aᵖ⁻¹ ≡ 1 (mod p) (Fermat) follows by applying the corollary to the group of non-zero residues."""),
           ("Subgroup test and elements of a cyclic group",
            """**One-step test:** a non-empty subset H of G is a subgroup iff a·b⁻¹ ∈ H for all a, b ∈ H (take a = b to get e, then e·b⁻¹ for inverses, then a·(b⁻¹)⁻¹ for closure).

In a cyclic group ⟨g⟩ of order n, gᵏ has order n/gcd(n, k): the powers of gᵏ return to the identity exactly when n ∣ km, i.e. m is a multiple of n/gcd(n, k). Therefore there are **φ(d) elements of order d for each divisor d of n**, φ(n) generators, and exactly one subgroup of each order d ∣ n."""),
       ],
       notes=[
           ("Standard groups and their orders",
            """(ℤₙ, +) is cyclic of order n; (ℤₙ*, ×) has φ(n) elements; Sₙ has n! elements (not abelian for n ≥ 3); the Klein four-group {e, a, b, ab} is abelian, every element has order 2 and it is not cyclic. A group where every element satisfies x² = e is abelian (ab = (ab)⁻¹ = b⁻¹a⁻¹ = ba). A semigroup is closed and associative; a monoid adds an identity; a group adds inverses. (ℤ, −) is not even a semigroup and (ℕ, +) is a monoid but not a group."""),
           ("Counting problems",
            """Number of groups of order p, p², pq (p < q primes, p ∤ q − 1): 1, 2, 1; the order of a product element in an abelian group satisfies ord(ab) ∣ lcm(ord(a), ord(b)); the number of subgroups of ℤₙ is the number of divisors of n; if |G| is even there is an element of order 2 (pair x with x⁻¹: an odd number of elements are self-inverse, including e, so another one exists)."""),
       ])

deepen("engm-graph-basics",
       proofs=[
           ("Handshake lemma: Σ deg(v) = 2|E|",
            """Every edge has exactly two end points, so when the degrees of all vertices are added each edge contributes 1 to each of its two ends: the total is 2|E|. Consequently the sum of degrees is even, and so the number of vertices of odd degree is even (the even-degree vertices contribute an even amount, so the odd ones must too)."""),
           ("Euler circuits exist iff the graph is connected and every degree is even",
            """**Necessity.** Along an Euler circuit every visit to a vertex uses one incoming and one outgoing edge, so the degree of each vertex is even.

**Sufficiency (sketch).** Start at any vertex and keep walking along unused edges. Because all degrees are even, whenever we enter a vertex other than the start there is an unused edge to leave by, so the walk can only get stuck at the start vertex, having formed a closed trail C. Remove C; every vertex still has even degree. If some edges remain, connectivity gives a vertex on C that is incident to a remaining edge; build a closed trail from there and splice it into C. Repeat until all edges are used. A graph has an Euler **path** (not circuit) iff it is connected with exactly two odd-degree vertices, which must be the end points."""),
           ("Edge bounds in simple graphs",
            """A simple graph on n vertices has at most C(n, 2) = n(n − 1)/2 edges (each unordered pair at most once), so there are 2^(C(n,2)) labelled graphs. A **connected** graph has at least n − 1 edges: if it had fewer, removing edges from a spanning structure would leave a component count above 1 since each edge reduces the number of components by at most one. A graph with n vertices and **more than C(n − 1, 2) edges is necessarily connected**: the maximum for a disconnected graph is obtained by a complete K_{n−1} plus an isolated vertex, with C(n − 1, 2) edges."""),
       ],
       notes=[
           ("Hamiltonian conditions and counts",
            """No simple criterion is both necessary and sufficient. **Dirac:** a simple graph with n ≥ 3 vertices and minimum degree ≥ n/2 is Hamiltonian. **Ore:** if deg(u) + deg(v) ≥ n for every non-adjacent pair, the graph is Hamiltonian. The complete graph Kₙ has (n − 1)!/2 distinct Hamilton cycles; the complete bipartite graph K_{m,n} with m ≠ n has none (a cycle alternates sides). Counting facts: the number of edges in Kₙ is n(n − 1)/2, in K_{m,n} is mn, in a d-regular graph nd/2, in the hypercube Qₙ is n·2ⁿ⁻¹ (with 2ⁿ vertices of degree n)."""),
           ("Degree sequences and standard families",
            """A sequence is **graphical** if some simple graph realises it; Havel–Hakimi: delete the largest d, subtract 1 from the next d largest, and repeat. The cycle Cₙ is 2-regular, the path Pₙ has two vertices of degree 1, the wheel Wₙ has 2(n − 1) edges, the Petersen graph is 3-regular on 10 vertices (not Hamiltonian, not planar). Walk, trail, path and circuit differ in whether edges/vertices may repeat; **connectivity** is measured by the minimum number of vertices or edges whose removal disconnects the graph."""),
       ])

deepen("engm-graph-trees-planar-colouring",
       proofs=[
           ("A tree on n vertices has n − 1 edges",
            """Induct on n. A tree with one vertex has 0 edges. A tree with n ≥ 2 vertices has a leaf (take a longest path; its end point has no other neighbour, otherwise the path could be extended or would close a cycle). Delete the leaf and its edge: the result is still connected and acyclic, a tree with n − 1 vertices, which by induction has n − 2 edges. Hence the original has n − 1 edges. Equivalently: connected + n − 1 edges ⇒ tree; acyclic + n − 1 edges ⇒ tree."""),
           ("Euler's formula v − e + f = 2 and the planar edge bound",
            """For a connected plane graph, induct on the number of edges. If the graph is a tree, e = v − 1 and f = 1 (only the outer face), so v − e + f = v − (v − 1) + 1 = 2. Otherwise the graph contains a cycle; remove one cycle edge, which merges two faces (f decreases by 1) and reduces e by 1, leaving v − e + f unchanged.

**Bound.** In a simple connected planar graph with v ≥ 3 each face is bounded by at least 3 edges and each edge borders at most 2 faces, so 3f ≤ 2e. Substituting f = 2 − v + e gives 3(2 − v + e) ≤ 2e, i.e. **e ≤ 3v − 6**. If the graph has no triangles each face has ≥ 4 sides and e ≤ 2v − 4. Consequences: K₅ has 10 > 3·5 − 6 = 9 edges, so it is not planar; K₃,₃ has 9 > 2·6 − 4 = 8 edges and no triangles, so it is not planar either."""),
           ("Greedy colouring bound and bipartite graphs",
            """Colour vertices one by one with the smallest colour not used by an already-coloured neighbour. A vertex has at most Δ neighbours, so at most Δ colours are forbidden and a colour from {1, …, Δ + 1} is always available: **χ(G) ≤ Δ + 1**. A graph is **bipartite iff it has no odd cycle**: a bipartite graph alternates sides along a cycle so cycles have even length; conversely, in a graph without odd cycles colour each vertex by the parity of its distance from a root in its component — an edge joining two vertices of the same parity would create an odd cycle. Hence trees and even cycles are 2-colourable; χ(Kₙ) = n; every planar graph is 4-colourable (Four-Colour Theorem), 5-colourable by an elementary proof."""),
       ],
       notes=[
           ("Spanning trees and counting",
            """**Cayley's formula:** there are n^(n−2) labelled trees on n vertices (Prüfer sequences give a bijection with sequences of length n − 2 over n symbols). The number of spanning trees of a connected graph is any cofactor of its Laplacian matrix (Kirchhoff's matrix-tree theorem); for a cycle Cₙ it is n and for K₃,₃ it is 81. A tree has at least two leaves, every edge is a bridge, and the number of leaves of a tree with degree sequence is 2 + Σ(deg(v) − 2) over vertices of degree ≥ 3. A rooted binary tree with n internal nodes (each with 0 or 2 children) has n + 1 leaves."""),
           ("Matching and independent sets",
            """**Hall's theorem:** a bipartite graph with sides X and Y has a matching saturating X iff |N(S)| ≥ |S| for every S ⊆ X. König's theorem: in bipartite graphs the size of a maximum matching equals the size of a minimum vertex cover. For any graph, independence number α(G) + vertex cover number τ(G) = n. A perfect matching in a graph with n vertices has n/2 edges. For planar graphs, the **face-edge relation** Σ(face degrees) = 2e is the basis of many counting questions."""),
       ])

deepen("engm-counting-basics",
       proofs=[
           ("Derivation of the formulas for P(n, r) and C(n, r)",
            """To arrange r objects chosen from n in order, pick the first in n ways, the second in n − 1 ways, …, the r-th in n − r + 1 ways: P(n, r) = n(n − 1)…(n − r + 1) = n!/(n − r)!. Each unordered selection (combination) of r objects corresponds to exactly r! orderings, so P(n, r) = C(n, r)·r!, giving **C(n, r) = n!/(r!(n − r)!)**. Symmetry C(n, r) = C(n, n − r) holds because choosing r objects to take is the same as choosing n − r to leave."""),
           ("Pascal's identity and the binomial theorem",
            """**C(n, r) = C(n − 1, r − 1) + C(n − 1, r).** Fix one object x. The r-subsets that contain x correspond to (r − 1)-subsets of the other n − 1 objects, and those that do not contain x are r-subsets of the other n − 1. Adding gives the identity.

**(x + y)ⁿ = Σ C(n, k) xᵏ yⁿ⁻ᵏ:** expanding the product of n factors (x + y), a term xᵏyⁿ⁻ᵏ arises by choosing x from exactly k of the n factors, which can be done in C(n, k) ways. Setting x = y = 1 gives Σ C(n, k) = 2ⁿ; setting x = 1, y = −1 gives Σ(−1)ᵏ C(n, k) = 0, so the even-indexed and odd-indexed sums are both 2ⁿ⁻¹."""),
           ("Stars and bars",
            """The number of non-negative integer solutions of x₁ + … + x_k = n equals the number of arrangements of n identical stars and k − 1 identical bars in a row: choose which k − 1 of the n + k − 1 positions hold bars, **C(n + k − 1, k − 1)**. If every xᵢ ≥ 1, first give each variable one unit and distribute the remaining n − k: C(n − 1, k − 1). If xᵢ ≥ aᵢ, substitute yᵢ = xᵢ − aᵢ and reduce n by Σaᵢ. The same count gives the number of multisets of size n from k kinds of objects."""),
       ],
       notes=[
           ("Arrangements with repetition, circular and restricted",
            """Arrangements of n objects with repeated kinds (n₁ of one, n₂ of another …): n!/(n₁! n₂! …). In a circle, rotations are identical, so n distinct objects give (n − 1)! arrangements (and (n − 1)!/2 if reflections also count, as for necklaces). If two particular objects must be adjacent, glue them: (n − 1)!·2 linear arrangements; if they must be apart, subtract this from n!. Words of length n over an alphabet of size k number kⁿ; words using only distinct letters number P(k, n). The number of ways to place n distinguishable balls into k labelled boxes is kⁿ, and into identical boxes is a Stirling-number sum."""),
           ("Paths on a grid and the Catalan numbers",
            """The number of monotone lattice paths from (0, 0) to (a, b) is C(a + b, a). Paths that never rise above the diagonal from (0, 0) to (n, n) number the Catalan number Cₙ = C(2n, n)/(n + 1), which also counts balanced parenthesisations, binary trees with n nodes, triangulations of an (n + 2)-gon and valid stack-pop sequences. The first values are 1, 1, 2, 5, 14, 42, 132."""),
       ])

deepen("engm-pie-pigeonhole-recurrence",
       proofs=[
           ("The derangement number Dₙ = n! Σ (−1)ᵏ/k!",
            """Let Aᵢ be the set of permutations of 1..n that fix i. A permutation with no fixed point lies in none of the Aᵢ. The intersection of any k of the sets (fixing k specified points) has (n − k)! elements, and there are C(n, k) such choices. By inclusion–exclusion

Dₙ = n! − C(n, 1)(n − 1)! + C(n, 2)(n − 2)! − … + (−1)ⁿ C(n, n) 0! = Σ_{k=0}^{n} (−1)ᵏ n!/k!.

The values are D₁ = 0, D₂ = 1, D₃ = 2, D₄ = 9, D₅ = 44, D₆ = 265 and Dₙ is the nearest integer to n!/e. They also satisfy Dₙ = (n − 1)(Dₙ₋₁ + Dₙ₋₂): element n goes to one of n − 1 positions i, and either i goes to n (the rest is a derangement of n − 2 elements) or it does not (equivalent to a derangement of n − 1 elements)."""),
           ("The generalised pigeonhole principle",
            """If N objects are placed in k boxes then some box contains at least ⌈N/k⌉ objects. Proof: if every box held at most ⌈N/k⌉ − 1 < N/k objects, the total would be less than k·(N/k) = N, a contradiction. Typical use: among any 13 people two share a birth month; in any set of n + 1 integers two have the same remainder mod n; among any five points in a unit square two are within √2/2 of each other."""),
           ("Solving a linear homogeneous recurrence with constant coefficients",
            """Try aₙ = rⁿ in aₙ = c₁aₙ₋₁ + c₂aₙ₋₂. Dividing by rⁿ⁻² gives the **characteristic equation r² − c₁r − c₂ = 0**. If it has distinct roots r₁, r₂ then every combination aₙ = A r₁ⁿ + B r₂ⁿ is a solution (the recurrence is linear), and A, B are fixed by the two initial values. If there is a repeated root r, then aₙ = (A + Bn)rⁿ (n rⁿ is also a solution since substituting shows the derivative of the characteristic polynomial vanishes at r). For Fibonacci, r² = r + 1 gives r = (1 ± √5)/2 and the closed form **Fₙ = (φⁿ − ψⁿ)/√5** (Binet). For an inhomogeneous recurrence add a particular solution (try a polynomial or exponential of the same form as the forcing term)."""),
       ],
       notes=[
           ("Standard recurrences and their solutions",
            """T(n) = T(n − 1) + c gives cn; T(n) = T(n − 1) + n gives n(n + 1)/2; T(n) = 2T(n − 1) + 1 with T(0) = 0 gives 2ⁿ − 1 (Tower of Hanoi moves); T(n) = 2T(n/2) + n gives n log n; the number of binary strings of length n without two consecutive 1s satisfies aₙ = aₙ₋₁ + aₙ₋₂ with a₁ = 2, a₂ = 3 (Fibonacci shifted); the number of regions formed by n lines in general position is 1 + n(n + 1)/2; the number of ways to tile a 2 × n strip with dominoes is Fₙ₊₁."""),
           ("Inclusion–exclusion template for ‘none’ and ‘onto’ counts",
            """Number of integers in 1..N divisible by none of p₁ … pₖ (pairwise coprime) = N − Σ⌊N/pᵢ⌋ + Σ⌊N/(pᵢpⱼ)⌋ − …; for Euler's φ(n) = n Π(1 − 1/p) over primes p dividing n this gives the familiar product. The number of solutions of x₁ + … + x_k = n with all xᵢ ≤ m is found by subtracting cases where some xᵢ ≥ m + 1 using stars and bars. Always state the universe, the ‘bad’ properties and the size of each intersection before summing."""),
       ])

deepen("engm-matrices-determinants",
       proofs=[
           ("Basic properties of determinants and why A · adj(A) = det(A) · I",
            """From the Leibniz expansion det A = Σ sign(σ) Π aᵢ,σ(i): (1) swapping two rows swaps the sign of every permutation, so det changes sign; hence a matrix with two equal rows has det = −det, i.e. det = 0. (2) Multiplying a row by c multiplies every term by c. (3) det(Aᵀ) = det A because inverting the permutation preserves its sign. (4) Adding a multiple of one row to another leaves det unchanged: the extra term is a determinant with two equal rows.

For the adjugate, the (i, j) entry of A·adj(A) is Σₖ aᵢₖ Cⱼₖ, where Cⱼₖ is the cofactor. If i = j this is the cofactor expansion along row i and equals det A. If i ≠ j it is the expansion of the determinant of a matrix with rows i and j equal, which is 0. Therefore A·adj(A) = det(A)·I and, when det A ≠ 0, **A⁻¹ = adj(A)/det(A)**."""),
           ("det(AB) = det(A) det(B) and det(kA) = kⁿ det(A)",
            """If A is singular, then AB is singular and both sides are 0. If A is invertible it is a product of elementary matrices; each elementary matrix E satisfies det(EB) = det(E)·det(B) (swap: −1, scale: c, shear: 1), so det(AB) = det(E₁)…det(Eₖ)det(B) = det(A)det(B). Scaling every one of the n rows by k multiplies the determinant by kⁿ, so det(kA) = kⁿ det(A). Consequences: det(A⁻¹) = 1/det A, det(Aᵐ) = (det A)ᵐ, det(adj A) = (det A)ⁿ⁻¹."""),
           ("Rank–nullity and the equality of row and column rank",
            """For an m × n matrix A, the map x ↦ Ax has kernel (null space) of dimension nullity(A) and image (column space) of dimension rank(A); the rank–nullity theorem says rank + nullity = n. Reason: extend a basis of the kernel to a basis of ℝⁿ; the images of the added vectors are independent and span the column space, so their number is rank(A). Row operations preserve the row space and the solution set, so row rank equals the number of pivots in the echelon form, which equals the number of independent columns: row rank = column rank."""),
       ],
       notes=[
           ("Computation shortcuts",
            """det of a triangular matrix is the product of the diagonal. Row operations: swap changes the sign, scaling a row by c multiplies det by c, adding a multiple of a row changes nothing. det A = 0 ⇔ rows dependent ⇔ A not invertible ⇔ rank < n. For the 2 × 2 matrix [[a, b], [c, d]] the inverse is (1/(ad − bc))·[[d, −b], [−c, a]]. rank(AB) ≤ min(rank A, rank B); rank(A + B) ≤ rank A + rank B; the rank of a non-zero matrix of the form u vᵀ is 1; for a square matrix with n ≥ 2, rank(adj A) is n if rank A = n, 1 if rank A = n − 1, and 0 otherwise."""),
           ("Special matrices",
            """Symmetric: A = Aᵀ; skew-symmetric: Aᵀ = −A (zero diagonal, odd order ⇒ det 0); orthogonal: AᵀA = I (det = ±1, preserves lengths); idempotent: A² = A (eigenvalues 0 or 1); nilpotent: Aᵏ = 0 (all eigenvalues 0); involutory: A² = I. Every square matrix is the sum of a symmetric and a skew-symmetric matrix, (A + Aᵀ)/2 and (A − Aᵀ)/2. The trace is linear and tr(AB) = tr(BA)."""),
       ])

deepen("engm-linear-systems-eigen",
       proofs=[
           ("Sum of eigenvalues = trace, product = determinant",
            """The eigenvalues are the roots of det(A − λI) = 0, a degree-n polynomial p(λ) = (−1)ⁿ(λ − λ₁)…(λ − λₙ). Expanding det(A − λI), the coefficient of λⁿ⁻¹ is (−1)ⁿ⁻¹ × (sum of diagonal entries) = (−1)ⁿ⁻¹ tr A, while expanding the factored form gives (−1)ⁿ × (−Σλᵢ) = (−1)ⁿ⁻¹ Σλᵢ. Comparing, **Σλᵢ = tr A**. Setting λ = 0 gives p(0) = det A = (−1)ⁿ(−1)ⁿ Πλᵢ = **Πλᵢ**."""),
           ("Eigenvalues of Aᵏ, A⁻¹ and Aᵀ; triangular matrices",
            """If Av = λv then A²v = A(λv) = λ²v and in general Aᵏv = λᵏv; if A is invertible, v = A⁻¹Av = λA⁻¹v so A⁻¹v = (1/λ)v (λ ≠ 0 because A is invertible). Aᵀ has the same characteristic polynomial since det(Aᵀ − λI) = det((A − λI)ᵀ) = det(A − λI), so it has the same eigenvalues (but generally different eigenvectors). For a triangular matrix A − λI is triangular, so its determinant is Π(aᵢᵢ − λ): the eigenvalues are the diagonal entries. For any polynomial q, q(A) has eigenvalues q(λᵢ); a matrix with A² = A can only have eigenvalues 0 or 1 because λ² = λ."""),
           ("Symmetric real matrices have real eigenvalues and orthogonal eigenvectors for distinct eigenvalues",
            """Let Av = λv with v ≠ 0 possibly complex. Then v̄ᵀAv = λ v̄ᵀv. Taking the conjugate transpose of Av = λv and using A real symmetric gives v̄ᵀA = λ̄ v̄ᵀ, so v̄ᵀAv = λ̄ v̄ᵀv. Since v̄ᵀv = Σ|vᵢ|² > 0, λ = λ̄: λ is real. If Av = λv and Aw = μw with λ ≠ μ, then λ(vᵀw) = (Av)ᵀw = vᵀAᵀw = vᵀAw = μ(vᵀw), so (λ − μ)vᵀw = 0 and vᵀw = 0. Hence a symmetric matrix is orthogonally diagonalisable."""),
           ("Cayley–Hamilton for 2 × 2 and consistency of linear systems",
            """For A = [[a, b], [c, d]] the characteristic polynomial is λ² − (a + d)λ + (ad − bc); direct multiplication confirms A² − (a + d)A + (ad − bc)I = 0, so every matrix satisfies its own characteristic equation (the theorem holds for every n). It gives A⁻¹ = (tr A·I − A)/det A in the 2 × 2 case.

**Rouché–Capelli:** Ax = b is consistent iff rank(A) = rank([A | b]). If this common rank r equals the number of unknowns n the solution is unique; if r < n there are infinitely many, with n − r free parameters. A homogeneous system always has the trivial solution and has non-trivial solutions iff rank < n (in particular whenever there are more unknowns than equations)."""),
       ],
       notes=[
           ("Eigenvector facts and diagonalisation",
            """Eigenvectors for distinct eigenvalues are linearly independent, so n distinct eigenvalues guarantee diagonalisability A = PDP⁻¹; with repeated eigenvalues you must check that the geometric multiplicity (dimension of the eigenspace) equals the algebraic multiplicity. Then Aᵏ = PDᵏP⁻¹. A matrix is singular ⇔ 0 is an eigenvalue. The algebraic multiplicity is at least the geometric one. A Markov (stochastic) matrix has eigenvalue 1."""),
           ("Solving systems quickly",
            """Reduce the augmented matrix to row echelon form; a row of the form [0 … 0 | c] with c ≠ 0 means inconsistent. For a square system, Cramer's rule gives xᵢ = det(Aᵢ)/det(A) when det(A) ≠ 0. In GATE questions with a parameter, find the values making det = 0 and then examine consistency separately for those values: it is a common trap that det = 0 gives either no solution or infinitely many depending on the right-hand side."""),
       ])

deepen("engm-limits-continuity",
       proofs=[
           ("Squeeze theorem and lim_{x→0} sin x / x = 1",
            """**Squeeze:** if g(x) ≤ f(x) ≤ h(x) near a and g and h both tend to L, then f tends to L: for any ε, eventually both g and h lie within ε of L, and f is trapped between them.

For 0 < x < π/2 compare the areas of the triangle OAB (sector's inscribed triangle), the circular sector and the larger triangle OAT in the unit circle: ½ sin x < ½ x < ½ tan x. Divide by ½ sin x: 1 < x/sin x < 1/cos x, so cos x < sin x / x < 1. As x → 0⁺ cos x → 1, so the squeeze gives the limit 1; the function sin x / x is even, so the left-hand limit is also 1. Consequently lim (1 − cos x)/x² = ½ (multiply by 1 + cos x) and lim tan x / x = 1."""),
           ("The limit (1 + 1/n)ⁿ exists and equals e",
            """By the binomial theorem aₙ = (1 + 1/n)ⁿ = Σ C(n, k)/nᵏ = Σ (1/k!)(1 − 1/n)(1 − 2/n)…(1 − (k − 1)/n). Each term increases with n and a new non-negative term is added, so aₙ is increasing; it is bounded above by Σ 1/k! ≤ 1 + 1 + ½ + ¼ + … < 3. A bounded increasing sequence converges; its limit is defined to be e ≈ 2.71828. Taking logarithms and using the continuity of exp gives lim (1 + a/x)ˣ = eᵃ, the standard form 1^∞ → e^(lim of g·(f − 1)) used in GATE limit problems."""),
           ("Differentiable ⇒ continuous; the Intermediate Value Theorem",
            """If f′(a) exists then f(a + h) − f(a) = h · (f(a + h) − f(a))/h → 0 · f′(a) = 0, so f is continuous at a. The converse is false: |x| is continuous but not differentiable at 0.

**IVT:** let f be continuous on [a, b] with f(a) < c < f(b) (the other case is similar). Bisect: let m be the midpoint; one of [a, m], [m, b] again has f below c at the left end and above at the right end. Repeating yields nested intervals shrinking to a point x₀; by continuity f(x₀) can be neither < c nor > c, so f(x₀) = c. This is why a continuous function on a closed interval takes every value between its end values, and why a polynomial of odd degree has a real root."""),
       ],
       notes=[
           ("Limit techniques",
            """Algebraic simplification (factor and cancel, rationalise), standard limits (sin x/x → 1, (eˣ − 1)/x → 1, ln(1 + x)/x → 1, (1 + x)^(1/x) → e, (aˣ − 1)/x → ln a), L'Hôpital's rule for 0/0 and ∞/∞ (differentiate numerator and denominator separately; repeat if needed), series expansions near 0 (sin x = x − x³/6 + …, cos x = 1 − x²/2 + …, eˣ = 1 + x + x²/2 + …) which turn hard limits into polynomials. Indeterminate forms 1^∞, 0⁰ and ∞⁰ are handled by taking logarithms. Limits at infinity of rational functions compare the leading terms: equal degrees give the ratio of leading coefficients."""),
           ("Continuity checks",
            """f is continuous at a if the left and right limits exist and equal f(a). Types of discontinuity: removable (limit exists but ≠ f(a)), jump (one-sided limits differ), infinite and oscillating. Piecewise functions need the one-sided limits at the break points; sums, products, quotients (denominator ≠ 0) and compositions of continuous functions are continuous. A continuous function on a closed bounded interval is bounded and attains its maximum and minimum (extreme value theorem)."""),
       ])

deepen("engm-differentiation-mvt",
       proofs=[
           ("Rolle's theorem and the Mean Value Theorem",
            """**Rolle:** let f be continuous on [a, b], differentiable on (a, b) and f(a) = f(b). By the extreme value theorem f attains a maximum and a minimum on [a, b]. If both occur at the end points then f is constant and f′ = 0 everywhere. Otherwise an extremum occurs at an interior point c; at an interior extremum the difference quotients have opposite signs on the two sides, so f′(c) = 0.

**MVT:** define g(x) = f(x) − f(a) − ((f(b) − f(a))/(b − a))(x − a). Then g(a) = g(b) = 0, so Rolle gives c with g′(c) = 0, i.e. **f′(c) = (f(b) − f(a))/(b − a)**. Consequences: f′ ≥ 0 on an interval ⇒ f is non-decreasing; f′ = 0 ⇒ f is constant; |f(x) − f(y)| ≤ M|x − y| if |f′| ≤ M."""),
           ("Product rule, chain rule and the derivative of xⁿ",
            """Product: (fg)′ = lim [f(x + h)g(x + h) − f(x)g(x)]/h = lim [f(x + h)(g(x + h) − g(x)) + g(x)(f(x + h) − f(x))]/h = f g′ + g f′ (using continuity of f). Chain rule: for y = f(u), u = g(x), Δy/Δx = (Δy/Δu)(Δu/Δx) → f′(g(x))g′(x). For xⁿ with n a positive integer, the binomial theorem gives ((x + h)ⁿ − xⁿ)/h = n xⁿ⁻¹ + terms with h, which tend to n xⁿ⁻¹; the quotient rule follows from the product and chain rules applied to f·g⁻¹."""),
           ("Taylor's theorem with the Lagrange remainder",
            """Define R_n(x) = f(x) − Σ_{k=0}^{n} f⁽ᵏ⁾(a)(x − a)ᵏ/k!. Repeated application of Rolle's theorem to the auxiliary function F(t) = f(x) − Σ f⁽ᵏ⁾(t)(x − t)ᵏ/k! − K (x − t)ⁿ⁺¹ with K chosen so that F(a) = 0 (and F(x) = 0) yields a point ξ between a and x with **Rₙ(x) = f⁽ⁿ⁺¹⁾(ξ)(x − a)ⁿ⁺¹/(n + 1)!**. When the remainder tends to 0 the Taylor series converges to f; this proves that eˣ, sin x and cos x equal their Maclaurin series for every x because their derivatives are bounded by e^|x| or 1."""),
       ],
       notes=[
           ("Standard derivatives and tests",
            """(xⁿ)′ = nxⁿ⁻¹, (eˣ)′ = eˣ, (ln x)′ = 1/x, (sin x)′ = cos x, (tan x)′ = sec² x, (aˣ)′ = aˣ ln a, (sin⁻¹ x)′ = 1/√(1 − x²), (tan⁻¹ x)′ = 1/(1 + x²). A function is differentiable at a point when the left and right derivatives exist and are equal: for |x| they are −1 and +1 at 0. For the product f·g: if f is differentiable and g is not, the product can still be differentiable (e.g. x·|x| at 0). Implicit differentiation and logarithmic differentiation handle xˣ-type functions: (xˣ)′ = xˣ(1 + ln x)."""),
           ("Series convergence tests",
            """Geometric Σrⁿ converges iff |r| < 1; the p-series Σ1/nᵖ converges iff p > 1 (the harmonic series diverges); the ratio test (limit |aₙ₊₁/aₙ| < 1 converges, > 1 diverges, = 1 inconclusive); the root test; the comparison and limit-comparison tests with a known series; the alternating series test (terms decrease to 0). A necessary but not sufficient condition for Σaₙ to converge is aₙ → 0. Power series have a radius of convergence R = lim |aₙ/aₙ₊₁|."""),
       ])

deepen("engm-maxima-minima-integration",
       proofs=[
           ("The second-derivative test and Fermat's necessary condition",
            """If f has a local maximum or minimum at an interior point c and is differentiable there, then f′(c) = 0: near a maximum the difference quotient (f(c + h) − f(c))/h is ≤ 0 for h > 0 and ≥ 0 for h < 0, so the only value its limit can take is 0. If additionally f″(c) > 0, then f′ is increasing near c with f′(c) = 0, so f′ < 0 to the left and f′ > 0 to the right: f decreases then increases, a local minimum. If f″(c) < 0 the same argument gives a local maximum; if f″(c) = 0 the test fails (x³ has an inflection and x⁴ a minimum at 0). For a function of two variables the analogue uses the Hessian: with D = f_xx f_yy − f_xy² > 0 and f_xx > 0 it is a minimum, D > 0 and f_xx < 0 a maximum, D < 0 a saddle."""),
           ("The Fundamental Theorem of Calculus and integration by parts",
            """Let F(x) = ∫ₐˣ f(t) dt for continuous f. Then (F(x + h) − F(x))/h = (1/h)∫ₓˣ⁺ʰ f(t) dt, which lies between the minimum and maximum of f on [x, x + h]; by continuity it tends to f(x), so **F′ = f**. If G is any antiderivative of f then G − F is constant, giving ∫ₐᵇ f = G(b) − G(a).

**Integration by parts** is the product rule integrated: (uv)′ = u′v + uv′ gives ∫u v′ dx = uv − ∫u′ v dx. Choose u by the ILATE order (inverse trig, logarithm, algebraic, trigonometric, exponential). Example: ∫x eˣ dx = x eˣ − ∫eˣ dx = (x − 1)eˣ + C."""),
           ("The Gaussian integral ∫₀^∞ e^(−x²) dx = √π / 2",
            """Let I = ∫₀^∞ e^(−x²) dx. Then I² = ∫₀^∞∫₀^∞ e^(−(x² + y²)) dx dy. Switch to polar coordinates over the first quadrant: x = r cos θ, y = r sin θ, dx dy = r dr dθ, so I² = ∫₀^{π/2}∫₀^∞ e^(−r²) r dr dθ = (π/2)·[−½ e^(−r²)]₀^∞ = (π/2)(½) = π/4. Hence I = √π/2 and the integral over the whole line is √π. This is the normalising constant of the normal distribution and gives Γ(½) = √π."""),
           ("Properties of definite integrals used for shortcuts",
            """**King's property:** ∫ₐᵇ f(x) dx = ∫ₐᵇ f(a + b − x) dx (substitute u = a + b − x). Adding the two forms, ∫₀^{π/2} sin x/(sin x + cos x) dx = π/4 because the integrand and its reflection sum to 1. For an even function ∫₋ₐᵃ f = 2∫₀ᵃ f; for an odd function it is 0. For a periodic function with period T, ∫₀^{nT} f = n∫₀ᵀ f. **Leibniz rule:** d/dx ∫_{u(x)}^{v(x)} f(t) dt = f(v)v′ − f(u)u′."""),
       ],
       notes=[
           ("Optimisation procedure",
            """Find the critical points (f′ = 0 or f′ undefined), compare the values there with the end-point values on a closed interval (the global extrema), and classify using f″ or the sign change of f′. Word problems: write the quantity to optimise in a single variable using the constraint. Typical results: the rectangle of maximum area with fixed perimeter is a square; the maximum of a·sin x + b·cos x is √(a² + b²); the minimum of x + 1/x for x > 0 is 2 at x = 1."""),
           ("Integrals to know",
            """∫xⁿ dx = xⁿ⁺¹/(n + 1) (n ≠ −1), ∫1/x dx = ln|x|, ∫eᵃˣ = eᵃˣ/a, ∫sin = −cos, ∫cos = sin, ∫sec² = tan, ∫1/(1 + x²) = tan⁻¹ x, ∫1/√(1 − x²) = sin⁻¹ x; the Beta/Gamma functions Γ(n) = (n − 1)! for integers and ∫₀^{π/2} sinᵐ x cosⁿ x dx = ½ B((m + 1)/2, (n + 1)/2); **Wallis' formula** ∫₀^{π/2} sinⁿ x dx = ((n − 1)/n)·((n − 3)/(n − 2))… (times π/2 if n is even). Improper integrals converge when ∫₁^∞ x⁻ᵖ dx with p > 1 and ∫₀¹ x⁻ᵖ dx with p < 1."""),
       ])

deepen("engm-probability-bayes",
       proofs=[
           ("Addition rule, conditional probability and the multiplication rule",
            """From the axioms, P(A ∪ B) = P(A) + P(B) − P(A ∩ B): split A ∪ B into the disjoint pieces A, and B ∖ A, then P(B ∖ A) = P(B) − P(A ∩ B). Conditional probability is defined by P(A ∣ B) = P(A ∩ B)/P(B) for P(B) > 0, restricting the sample space to B and renormalising. Rearranging gives P(A ∩ B) = P(B)P(A ∣ B), and by induction P(A₁ ∩ … ∩ Aₙ) = P(A₁)P(A₂ ∣ A₁)…P(Aₙ ∣ A₁ ∩ … ∩ Aₙ₋₁). Events are **independent** when P(A ∩ B) = P(A)P(B); then A and Bᶜ are independent too, because P(A ∩ Bᶜ) = P(A) − P(A)P(B) = P(A)(1 − P(B))."""),
           ("Total probability and Bayes' theorem",
            """If B₁, …, Bₖ partition the sample space then any event A splits into the disjoint parts A ∩ Bᵢ, so **P(A) = Σ P(A ∣ Bᵢ)P(Bᵢ)** (total probability). Writing P(A ∩ Bⱼ) in two ways, P(Bⱼ ∣ A)P(A) = P(A ∣ Bⱼ)P(Bⱼ), and dividing by P(A) gives **Bayes' theorem P(Bⱼ ∣ A) = P(A ∣ Bⱼ)P(Bⱼ) / Σ P(A ∣ Bᵢ)P(Bᵢ)**. Example: a disease with prevalence 1% and a test with 95% sensitivity and 5% false-positive rate: P(disease ∣ positive) = 0.95·0.01/(0.95·0.01 + 0.05·0.99) = 0.0095/0.059 ≈ 0.161, much lower than most people expect."""),
           ("The birthday paradox",
            """With n people and 365 equally likely birthdays, the probability that all birthdays are different is (365/365)(364/365)…((365 − n + 1)/365) = Π(1 − k/365) ≈ e^(−n(n−1)/730). Setting this to ½ gives n(n − 1) ≈ 730 ln 2 ≈ 506, so n ≈ 23: with 23 people the probability of a shared birthday exceeds ½. The same reasoning bounds collisions in hashing: with m slots, about √m keys give a collision with probability near ½."""),
       ],
       notes=[
           ("Counting-based probability and standard setups",
            """For equally likely outcomes P(A) = |A|/|Ω|. Two dice: 36 outcomes, P(sum = 7) = 6/36; at least one six: 11/36. Drawing without replacement uses combinations: the probability of k red balls in a draw of n from R red and B blue is C(R, k)C(B, n − k)/C(R + B, n) (hypergeometric). ‘At least one’ is usually 1 − P(none). Monty Hall: switching wins with probability 2/3. Mutually exclusive does not mean independent: for non-trivial events exclusivity actually makes them dependent (P(A ∩ B) = 0 ≠ P(A)P(B))."""),
           ("Common conditional-probability traps",
            """Confusing P(A ∣ B) with P(B ∣ A) (the prosecutor's fallacy); forgetting that the sample space shrinks when you condition; treating dependent draws as independent; the two-children problem, where ‘at least one is a boy’ gives 1/3 for two boys but ‘the older is a boy’ gives 1/2. When unsure, draw a tree diagram or build the table of joint probabilities and read off the required ratio."""),
       ])

deepen("engm-random-variables-distributions",
       proofs=[
           ("Linearity of expectation and Var(X) = E[X²] − (E[X])²",
            """E[X + Y] = ΣΣ (x + y)p(x, y) = Σ x Σ p(x, y) + Σ y Σ p(x, y) = E[X] + E[Y] — this needs **no independence**. Also E[aX + b] = aE[X] + b. For the variance, Var(X) = E[(X − μ)²] = E[X² − 2μX + μ²] = E[X²] − 2μ·μ + μ² = E[X²] − μ². Var(aX + b) = a² Var(X), and for independent X and Y, Var(X + Y) = Var X + Var Y because the covariance term E[(X − μₓ)(Y − μᵧ)] = E[X − μₓ]E[Y − μᵧ] = 0."""),
           ("Mean and variance of the binomial, geometric and Poisson distributions",
            """**Binomial B(n, p):** X = X₁ + … + Xₙ with independent indicators, E[Xᵢ] = p and Var(Xᵢ) = p − p² = pq, so E[X] = np and Var X = npq. **Geometric** (number of trials to the first success, P(X = k) = q^(k−1)p): E[X] = Σ k q^(k−1) p = p/(1 − q)² = 1/p; the variance is q/p². **Poisson(λ)** as the limit of B(n, λ/n): P(X = k) = C(n, k)(λ/n)ᵏ(1 − λ/n)^(n−k) → e^(−λ)λᵏ/k! since C(n, k)/nᵏ → 1/k! and (1 − λ/n)ⁿ → e^(−λ). Its mean and variance are both λ: Σ k e^(−λ)λᵏ/k! = λ e^(−λ) Σ λ^(k−1)/(k − 1)! = λ."""),
           ("The exponential distribution is memoryless",
            """If T is exponential with rate λ then P(T > t) = e^(−λt). Hence P(T > s + t ∣ T > s) = e^(−λ(s+t))/e^(−λs) = e^(−λt) = P(T > t): the waiting time already spent does not change the distribution of the remaining time. The exponential is the only continuous memoryless distribution and the geometric is its discrete analogue. Mean 1/λ, variance 1/λ². The time between events of a Poisson process of rate λ is exponential."""),
       ],
       notes=[
           ("Distribution cheat-sheet",
            """Uniform on {1..n}: mean (n + 1)/2, variance (n² − 1)/12. Continuous uniform on [a, b]: mean (a + b)/2, variance (b − a)²/12. Bernoulli(p): mean p, variance pq. Normal N(μ, σ²): symmetric about μ, about 68%, 95% and 99.7% of the mass within 1, 2 and 3 σ; standardise with Z = (X − μ)/σ, and the sum of independent normals is normal with added means and variances. For a fair die E[X] = 3.5 and Var = 35/12. The **expected number of trials** for all n coupons to be collected is n·Hₙ ≈ n ln n."""),
           ("Moments, covariance and bounds",
            """Cov(X, Y) = E[XY] − E[X]E[Y]; independence implies zero covariance but not conversely. Markov's inequality P(X ≥ a) ≤ E[X]/a for X ≥ 0; Chebyshev P(|X − μ| ≥ kσ) ≤ 1/k². For a continuous variable the pdf integrates to 1 and the cdf is its integral; E[g(X)] = ∫g(x)f(x)dx. The **median** m has F(m) = ½; for symmetric distributions mean = median. In GATE, typical tasks are to compute a missing constant by normalisation, an expectation by linearity, or a conditional probability with Bayes."""),
       ])

deepen("engm-pie-pigeonhole-recurrence",
       notes=[
           ("Summation toolkit",
            """Telescoping: Σ[f(k + 1) − f(k)] = f(n + 1) − f(1), e.g. Σ 1/(k(k + 1)) = Σ(1/k − 1/(k + 1)) = 1 − 1/(n + 1). The sum of a geometric series Σ_{k=0}^{n} rᵏ = (rⁿ⁺¹ − 1)/(r − 1); Σ k rᵏ is found by differentiating this expression with respect to r; Σ_{k=1}^{n} k·2ᵏ = (n − 1)2ⁿ⁺¹ + 2. The harmonic number Hₙ = Σ 1/k ≈ ln n + 0.5772. To prove a closed form by induction, check n = 1, assume it for n, add the (n + 1)-th term and simplify. Sums of the form Σ C(n, k) are evaluated with the binomial theorem (Σ C(n, k) = 2ⁿ), and Σ k·C(n, k) = n·2ⁿ⁻¹ because k·C(n, k) = n·C(n − 1, k − 1)."""),
       ])
