"""Textbook-style long-form teaching text: Engineering Mathematics (discrete mathematics)."""
from learn import elab

elab("engm-logic-propositions",
 ("Statements and truth", """
Logic is the study of correct reasoning. A **proposition** is a sentence that is either true or false, never both: "7 is prime" is a proposition; "Close the door" and "$x>3$" (with $x$ unknown) are not. We name propositions by letters $p,q,r$ and combine them with **connectives**:

| Connective | Symbol | True when |
|---|---|---|
| Negation | $\\lnot p$ | $p$ is false |
| Conjunction | $p\\land q$ | both are true |
| Disjunction | $p\\lor q$ | at least one is true |
| Implication | $p\\to q$ | not ($p$ true and $q$ false) |
| Biconditional | $p\\leftrightarrow q$ | $p$ and $q$ have the same truth value |

Implication surprises beginners: "if $p$ then $q$" is **false only when $p$ is true and $q$ is false**. If $p$ is false the implication is automatically true (we call it *vacuously* true).
"""),
 ("Equivalences you must know", """
Two formulas are **logically equivalent** if they have the same truth table. The most useful equivalences:

- $p\\to q\\equiv\\lnot p\\lor q$
- Contrapositive: $p\\to q\\equiv\\lnot q\\to\\lnot p$ (equivalent). The **converse** $q\\to p$ and the **inverse** $\\lnot p\\to\\lnot q$ are *not* equivalent to the original.
- De Morgan: $\\lnot(p\\land q)\\equiv\\lnot p\\lor\\lnot q$ and $\\lnot(p\\lor q)\\equiv\\lnot p\\land\\lnot q$
- $p\\leftrightarrow q\\equiv(p\\to q)\\land(q\\to p)$

A **tautology** is always true, a **contradiction** always false, and a formula that is neither is a **contingency**. A formula with $n$ variables has a truth table of $2^n$ rows.
"""),
 ("Arguments and inference", """
An **argument** is valid if the conclusion is true whenever all premises are true. Standard valid rules: **modus ponens** ($p,\\ p\\to q\\ \\therefore\\ q$), **modus tollens** ($\\lnot q,\\ p\\to q\\ \\therefore\\ \\lnot p$), **hypothetical syllogism** ($p\\to q,\\ q\\to r\\ \\therefore\\ p\\to r$) and **disjunctive syllogism** ($p\\lor q,\\ \\lnot p\\ \\therefore\\ q$). Two famous fallacies: **affirming the consequent** ($p\\to q,\\ q\\ \\therefore\\ p$) and **denying the antecedent** ($p\\to q,\\ \\lnot p\\ \\therefore\\ \\lnot q$). To test validity, check whether any truth assignment makes all premises true and the conclusion false.
"""),
)

elab("engm-logic-quantifiers",
 ("Talking about many objects", """
Propositional logic cannot say "every student passed" or "some student failed". **Predicate logic** adds **predicates** (properties like $P(x)$: "$x$ is even") and **quantifiers**: the **universal** quantifier $\\forall x\\,P(x)$ ("for all $x$") and the **existential** quantifier $\\exists x\\,P(x)$ ("there exists an $x$").

The domain (what $x$ ranges over) matters. Typical translations: "All students are clever" is $\\forall x\\,(S(x)\\to C(x))$ — use $\\to$ with $\\forall$. "Some student is clever" is $\\exists x\\,(S(x)\\land C(x))$ — use $\\land$ with $\\exists$. Swapping these is the most common mistake.
"""),
 ("Negation and nested quantifiers", """
To negate a quantified statement, flip the quantifier and negate inside:

$$\\lnot\\forall x\\,P(x)\\equiv\\exists x\\,\\lnot P(x)\\qquad\\lnot\\exists x\\,P(x)\\equiv\\forall x\\,\\lnot P(x)$$

With two quantifiers, **order matters**. $\\forall x\\,\\exists y\\,(y>x)$ says "every number has a larger one" (true on the integers). $\\exists y\\,\\forall x\\,(y>x)$ says "there is a number larger than all" (false). You may swap quantifiers of the *same* kind, but not $\\forall$ with $\\exists$. The valid direction is $\\exists x\\,\\forall y\\,P\\Rightarrow\\forall y\\,\\exists x\\,P$, not the reverse.
"""),
)

elab("engm-sets-counting",
 ("Sets", """
A **set** is a collection of distinct objects, written $\\{1,2,3\\}$. We write $x\\in A$ for membership and $A\\subseteq B$ if every element of $A$ is in $B$. The **empty set** $\\emptyset$ is a subset of every set. Operations: union $A\\cup B$, intersection $A\\cap B$, difference $A\\setminus B$, complement $\\bar A$ and **Cartesian product** $A\\times B=\\{(a,b)\\}$. The **power set** $\\mathcal P(A)$ is the set of all subsets of $A$.

Sizes: $|A\\times B|=|A|\\cdot|B|$ and $|\\mathcal P(A)|=2^{|A|}$. A set with $n$ elements has $\\binom nk$ subsets of size $k$.
"""),
 ("Inclusion–exclusion", """
To count elements in a union without counting overlaps twice, add the sets, subtract pairwise overlaps, add back the triple overlap:

$$|A\\cup B|=|A|+|B|-|A\\cap B|$$

$$|A\\cup B\\cup C|=|A|+|B|+|C|-|A\\cap B|-|B\\cap C|-|A\\cap C|+|A\\cap B\\cap C|$$

A Venn diagram makes these concrete: start by filling in the innermost region (the triple overlap) and work outwards, subtracting from each overlap you have already used.
"""),
 ("Multisets and counting arrangements", """
The **multiplication rule**: if one thing can be chosen in $m$ ways and another in $n$ ways, both can be chosen in $mn$ ways. The **addition rule**: if the choices are disjoint alternatives, add them. Arrangements of $n$ distinct objects: $n!$. If $n_1,n_2,\\dots$ are identical, the number of distinct arrangements is $\\frac{n!}{n_1!\\,n_2!\\cdots}$.
"""),
)

elab("engm-relations",
 ("What a relation is", """
A **relation** from $A$ to $B$ is any subset of $A\\times B$; a relation **on** a set $A$ is a subset of $A\\times A$. $(a,b)\\in R$ is written $aRb$. Examples: "less than" on numbers, "divides" on positive integers, "is a friend of" on people.

For a set with $n$ elements there are $2^{n^2}$ relations on it (each of the $n^2$ ordered pairs is in or out).
"""),
 ("Properties", """
A relation $R$ on $A$ is:

- **Reflexive** if $aRa$ for every $a$ (all diagonal pairs present).
- **Symmetric** if $aRb$ implies $bRa$.
- **Antisymmetric** if $aRb$ and $bRa$ imply $a=b$.
- **Transitive** if $aRb$ and $bRc$ imply $aRc$.

Counts on an $n$-element set: reflexive $2^{n^2-n}$; symmetric $2^{n(n+1)/2}$; antisymmetric $2^n\\cdot3^{n(n-1)/2}$. Note that *symmetric* and *antisymmetric* are not opposites: the identity relation is both.
"""),
 ("Equivalence relations and closures", """
A relation that is reflexive, symmetric and transitive is an **equivalence relation**. It splits the set into disjoint **equivalence classes** (a **partition**), and conversely every partition defines an equivalence relation. The number of partitions of an $n$-element set is the **Bell number** $B_n$ ($1,1,2,5,15,52,\\dots$). Congruence modulo $m$ is the standard example, with $m$ classes.

The **transitive closure** is the smallest transitive relation containing $R$; **Warshall's algorithm** computes it. A relation that is reflexive, antisymmetric and transitive is a **partial order**.
"""),
)

elab("engm-functions",
 ("Functions", """
A **function** $f:A\\to B$ assigns to every element of $A$ exactly one element of $B$. $A$ is the **domain**, $B$ the **codomain**, and the set of actual outputs is the **range**. The number of functions from an $m$-element set to an $n$-element set is $n^m$: each of the $m$ inputs independently chooses an output.
"""),
 ("One-to-one, onto and bijective", """
$f$ is **one-to-one (injective)** if different inputs give different outputs. It exists only when $m\\le n$, and the number of injective functions is $P(n,m)=\\frac{n!}{(n-m)!}$. $f$ is **onto (surjective)** if every element of the codomain is hit. It needs $m\\ge n$ and the number of onto functions is $\\sum_{i=0}^{n}(-1)^i\\binom ni(n-i)^m$ (inclusion–exclusion). $f$ is a **bijection** if both; then $m=n$ and there are $n!$ bijections.

A function has an **inverse** exactly when it is a bijection. The **composition** $g\\circ f$ applies $f$ first. The composition of injections is an injection, of surjections a surjection.
"""),
 ("Counting with the pigeonhole principle", """
If more than $kn$ objects are placed into $n$ boxes, some box contains more than $k$ objects. In particular, if $n+1$ objects go into $n$ boxes, two share a box. The function view: there is no injective function from a larger set to a smaller one.
"""),
)

elab("engm-posets-lattices",
 ("Partial orders", """
A **partially ordered set (poset)** is a set with a relation $\\le$ that is reflexive, antisymmetric and transitive. "Partial" because two elements may be **incomparable** (neither $a\\le b$ nor $b\\le a$): under divisibility, 2 and 3 are incomparable. A **total order** has every pair comparable.

A **Hasse diagram** draws a poset compactly: one node per element, an edge going upward from $a$ to $b$ if $a<b$ and nothing lies strictly between them. Reflexive loops and edges implied by transitivity are omitted.
"""),
 ("Special elements", """
In a poset: a **maximal** element has nothing above it; the **greatest** element is above *everything* (there is at most one). Similarly for **minimal** and **least**. A **chain** is a totally ordered subset; an **antichain** is a set of pairwise incomparable elements. The largest antichain in the power set of an $n$-set ordered by inclusion has size $\\binom n{\\lfloor n/2\\rfloor}$ (Sperner).

An **upper bound** of a subset is an element above all of them; the **least upper bound (join, lub)** is the smallest of those. The **greatest lower bound (meet, glb)** is defined dually.
"""),
 ("Lattices", """
A **lattice** is a poset in which every pair has both a lub and a glb. Divisibility on the divisors of $n$ is a lattice (lub = lcm, glb = gcd), and so is the power set under inclusion (union, intersection). A lattice is **bounded** if it has a least and greatest element, **distributive** if meet distributes over join, and **complemented** if every element has a complement. A **Boolean algebra** is a complemented distributive lattice with 0 and 1; it has $2^n$ elements. The lattices $M_3$ and $N_5$ are the forbidden sub-structures that make a lattice non-distributive.
"""),
)

elab("engm-groups",
 ("Algebraic structures", """
An **algebraic structure** is a set with operations. The levels, each adding conditions to the one before:

- **Magma / groupoid:** closed under the operation.
- **Semigroup:** also **associative**.
- **Monoid:** also has an **identity** $e$ with $ae=ea=a$.
- **Group:** also every element has an **inverse** $a^{-1}$ with $aa^{-1}=e$.
- **Abelian group:** also commutative.

Integers under addition form an abelian group; non-zero reals under multiplication too; the integers under multiplication are only a monoid (2 has no integer inverse).
"""),
 ("Subgroups and Lagrange's theorem", """
A **subgroup** $H$ of $G$ is a subset that is itself a group under the same operation. **Lagrange's theorem:** if $G$ is finite then $|H|$ divides $|G|$. Consequently, the order of every element divides the order of the group, and a group of prime order has no proper non-trivial subgroups.

A **cyclic group** is generated by one element $a$: $G=\\{a^0,a^1,\\dots\\}$. $\\mathbb Z_n$ under addition mod $n$ is cyclic of order $n$, and its generators are the numbers coprime to $n$. Every subgroup of a cyclic group is cyclic.
"""),
 ("Reading a Cayley table", """
A **Cayley table** lists the products of all pairs. In a group each row and each column contains every element exactly once (a Latin square). To test for a group from a table: check closure (all entries are in the set), find the identity (the row that repeats the header), check that each row has the identity (inverses), and test associativity (hardest — usually given or checked by example).
"""),
)

elab("engm-graph-basics",
 ("Graphs", """
A **graph** $G=(V,E)$ is a set of vertices and edges joining pairs of vertices. The **degree** of a vertex is the number of edges touching it. The **handshake lemma** says $\\sum_v\\deg(v)=2|E|$, so the number of vertices with odd degree is always even. A **simple** graph has no loops or parallel edges; a simple graph on $n$ vertices has at most $\\frac{n(n-1)}2$ edges, achieved by the **complete graph** $K_n$.

A **path** is a sequence of distinct vertices joined by edges; a **cycle** is a closed path. A graph is **connected** if any two vertices are joined by a path.
"""),
 ("Euler and Hamilton", """
An **Euler circuit** uses every *edge* exactly once and returns to the start: it exists iff the graph is connected and every vertex has **even degree**. An **Euler path** (not necessarily closed) exists iff exactly 0 or 2 vertices have odd degree.

A **Hamilton cycle** visits every *vertex* exactly once. There is no simple criterion (the problem is NP-complete); **Dirac's theorem** gives a sufficient condition: if $n\\ge3$ and every vertex has degree $\\ge n/2$, a Hamilton cycle exists.
"""),
 ("Special graphs and isomorphism", """
A **bipartite** graph has vertices split into two groups with edges only between the groups; it has no odd cycle. $K_{m,n}$ has $mn$ edges. A graph is **regular** if all degrees are equal ($k$-regular graph on $n$ vertices has $\\frac{nk}2$ edges). Two graphs are **isomorphic** if there is a relabelling of vertices mapping edges to edges; to disprove isomorphism, find an invariant that differs (number of vertices, edges, degree sequence, cycles).
"""),
)

elab("engm-graph-trees-planar-colouring",
 ("Trees", """
A **tree** is a connected graph with no cycles. Equivalent facts for a graph on $n$ vertices: it is a tree iff it is connected with $n-1$ edges, iff it has no cycles and $n-1$ edges, iff there is a unique path between any two vertices. A tree with $n\\ge2$ vertices has at least two leaves. **Cayley's formula:** there are $n^{n-2}$ labelled trees on $n$ vertices. In a full $m$-ary tree with $i$ internal nodes, the number of leaves is $(m-1)i+1$.

A **spanning tree** of a connected graph connects all vertices using $n-1$ of its edges.
"""),
 ("Planar graphs", """
A graph is **planar** if it can be drawn in the plane without crossing edges. **Euler's formula** for a connected planar graph: $V-E+F=2$, where $F$ counts faces including the outer one. From it follow bounds for a simple planar graph with $V\\ge3$: $E\\le3V-6$, and if it has no triangles, $E\\le2V-4$. $K_5$ and $K_{3,3}$ are non-planar (**Kuratowski**: a graph is planar iff it contains no subdivision of $K_5$ or $K_{3,3}$).
"""),
 ("Colouring", """
A **proper colouring** gives adjacent vertices different colours; the **chromatic number** $\\chi(G)$ is the fewest colours needed. A graph is 2-colourable iff it is bipartite; $\\chi(K_n)=n$; a cycle of odd length needs 3 colours. Every planar graph is 4-colourable (**Four Colour Theorem**). Always $\\chi(G)\\ge$ size of the largest clique, and $\\chi(G)\\le\\Delta+1$, where $\\Delta$ is the maximum degree.
"""),
)

elab("engm-counting-basics",
 ("Permutations and combinations", """
A **permutation** is an arrangement where order matters; a **combination** is a selection where it does not. Choosing and arranging $r$ out of $n$ distinct objects: $P(n,r)=\\frac{n!}{(n-r)!}$. Choosing $r$ out of $n$ without caring about order: $\\binom nr=\\frac{n!}{r!(n-r)!}$. Remember $\\binom nr=\\binom n{n-r}$ and Pascal's rule $\\binom nr=\\binom{n-1}{r-1}+\\binom{n-1}r$.

Circular arrangements of $n$ distinct people: $(n-1)!$ (rotations are the same).
"""),
 ("Distributing objects", """
The number of ways to write $x_1+x_2+\\dots+x_n=k$ in **non-negative integers** is $\\binom{k+n-1}{n-1}$ ("stars and bars": $k$ stars and $n-1$ dividers). If each $x_i\\ge1$ (positive), first give one to each: $\\binom{k-1}{n-1}$. Distributing $k$ identical balls into $n$ distinct boxes uses the same formula; distinct balls go $n^k$ ways.
"""),
 ("The binomial theorem", """
$$(x+y)^n=\\sum_{k=0}^n\\binom nkx^{n-k}y^k$$

Setting $x=y=1$ gives $\\sum_k\\binom nk=2^n$ (the number of subsets); setting $x=1,y=-1$ shows the even- and odd-sized subsets are equally many. The coefficient of $x^k$ in $(1+x)^n$ is $\\binom nk$.
"""),
)

elab("engm-pie-pigeonhole-recurrence",
 ("Inclusion–exclusion and derangements", """
The number of elements in none of the properties $P_1,\\dots,P_m$ is
$N-\\sum N(P_i)+\\sum N(P_i\\land P_j)-\\cdots$. A **derangement** is a permutation with no fixed point; the number is $D_n=n!\\sum_{k=0}^n\\frac{(-1)^k}{k!}$, approximately $\\frac{n!}{e}$, with the recurrence $D_n=(n-1)(D_{n-1}+D_{n-2})$ and $D_1=0,D_2=1$.
"""),
 ("The pigeonhole principle, more generally", """
If $N$ objects are put into $k$ boxes, some box holds at least $\\lceil N/k\\rceil$ objects. To use it, identify the "pigeons" and the "holes" carefully. Example: among any 13 people, two were born in the same month; among any $n+1$ integers, two have the same remainder modulo $n$.
"""),
 ("Recurrence relations", """
A **recurrence** defines a sequence in terms of earlier terms. A linear homogeneous recurrence with constant coefficients, $a_n=c_1a_{n-1}+c_2a_{n-2}$, is solved by the **characteristic equation** $r^2=c_1r+c_2$. If it has distinct roots $r_1,r_2$ then $a_n=Ar_1^n+Br_2^n$, where $A,B$ come from the initial values; if it has a repeated root $r$ then $a_n=(A+Bn)r^n$. For Fibonacci, $r^2=r+1$ gives $r=\\frac{1\\pm\\sqrt5}2$. Non-homogeneous recurrences add a particular solution.
"""),
)
