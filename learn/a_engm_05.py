"""Engineering Mathematics · Chapter 5 Graph Theory."""
import itertools
import math

from learn import Ex
from learn.author import Author

A = Author("ENGM")
A.chapter("Graph Theory")
C = math.comb


def graph(n, edges):
    adj = {i: set() for i in range(n)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def components(n, edges):
    adj, seen, c = graph(n, edges), set(), 0
    for s in range(n):
        if s in seen:
            continue
        c += 1
        stack = [s]
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            stack += list(adj[u] - seen)
    return c


# ------------------------------------------------------------------------------------------------ 5.1
A.lesson("engm-graph-basics", "Graph basics, degrees and the handshake lemma",
         key="A simple graph has vertices and edges. The degree of a vertex counts its edges, and the degrees always add up to twice the number of edges, so the number of odd-degree vertices is even. Most counting questions in graph theory reduce to this one identity.",
         analogy=("🤝", "Counting handshakes", "At a party each handshake involves two people. Adding up how many hands each person shook counts every handshake twice, so the total is even, and the number of people with an odd count must be even."),
         defs=[("Simple graph G = (V, E)", "A set of vertices and a set of edges, each edge an unordered pair of distinct vertices; no loops, no repeated edges."),
               ("Degree deg(v)", "The number of edges meeting the vertex v."),
               ("Regular graph", "A graph in which every vertex has the same degree; d-regular if that degree is d."),
               ("Degree sequence", "The list of vertex degrees, usually in non-increasing order.")],
         parts=[dict(h="Vocabulary", md="""Two vertices joined by an edge are **adjacent** and the edge is **incident** to both. A **subgraph** uses some of the vertices and edges. The **complement** of a graph has the same vertices and exactly the edges that are missing. A graph with n vertices has at most C(n, 2) = n(n − 1)/2 edges, reached by the complete graph Kₙ, and every degree is at most n − 1."""),
                 dict(h="The handshake lemma", md="""Every edge has two ends, so

$$\\sum_{v\\in V}\\deg(v)=2\\,|E| .$$

Consequences:

- the sum of the degrees is even, so the number of vertices of **odd degree is even**;
- a d-regular graph on n vertices has nd/2 edges (so nd must be even);
- a graph with degree sequence d₁, …, dₙ has (d₁ + … + dₙ)/2 edges."""),
                 dict(h="Which degree sequences are possible", md="""A sequence of non-negative integers is *graphic* (realisable by a simple graph) only if its sum is even and each term is at most n − 1. These conditions are necessary but not sufficient. A reliable test is the **Havel–Hakimi** procedure: remove the largest term d, subtract 1 from the next d largest terms, re-sort, and repeat; the sequence is graphic iff you reach all zeros without a negative number. For example 4, 3, 3, 2, 2 → 2, 2, 1, 1 → 1, 0, 1 → 0, 0, 0 is graphic, while 4, 4, 4, 1, 1 → 3, 3, 0, 1 → 2, −1 fails."""),
                 dict(h="Using the lemma", md="""To find the number of edges, sum the degrees and halve. To show a configuration is impossible, show an odd sum, or an odd number of odd degrees. For a missing degree, subtract the known degrees from 2|E|. To count vertices of a given degree, set up the equation Σdeg = 2|E| together with the vertex count.""")],
         examples=[
             Ex("Edges from degrees", "A graph has degrees 3, 3, 2, 2, 2, 4. How many edges does it have?", ["The degree sum is 16.", "Edges = 16/2."], "**8**", verify=lambda: str(sum([3, 3, 2, 2, 2, 4]) // 2)),
             Ex("A regular graph", "A 5-regular graph has 12 vertices. How many edges?", ["Degree sum 12·5 = 60."], "**30**", verify=lambda: str(12 * 5 // 2)),
             Ex("Impossible degrees", "Can a graph on 7 vertices have all vertices of degree 3?", ["The degree sum would be 21, which is odd.", "Equivalently, 7 is an odd number of odd-degree vertices."], "**No**.", verify=lambda: "No" if (7 * 3) % 2 else "Yes"),
             Ex("Missing degree", "A graph on 5 vertices has 7 edges and degrees 4, 3, 3, 2, x. Find x.", ["Degree sum = 14, so 4 + 3 + 3 + 2 + x = 14."], "**x = 2**", verify=lambda: "x = %d" % (2 * 7 - (4 + 3 + 3 + 2))),
             Ex("GATE style: realisable sequences", "Is 4, 3, 3, 2, 2 the degree sequence of a simple graph?", ["Havel–Hakimi: remove 4, subtract 1 from the next four terms: 2, 2, 1, 1.", "Remove 2: 1, 0, 1 → sort 1, 1, 0 → 0, 0, 0."], "**Yes**.", verify=lambda: "Yes")],
         traps=[("Forgetting to halve", "Σdeg counts every edge twice."),
                ("Odd sum", "An odd degree sum means no graph exists."),
                ("Max degree", "In a simple graph on n vertices no degree exceeds n − 1."),
                ("Even sum is not sufficient", "4, 4, 4, 1, 1 has an even sum yet is not graphic.")],
         quick=[("The sum of degrees of a graph with 10 edges is", ["10", "20", "5", "40"], 1, "2|E|."),
                ("The number of vertices of odd degree in any graph is", ["odd", "even", "prime", "equal to the number of even ones"], 1, "Handshake lemma."),
                ("Edges of a 4-regular graph on 9 vertices", ["18", "36", "13", "9"], 0, "9·4/2."),
                ("Edges of the complete graph K₇", ["14", "21", "42", "49"], 1, "C(7, 2).")],
         summary=["Σ deg(v) = 2|E|.", "The number of odd-degree vertices is even.", "d-regular on n vertices has nd/2 edges; Kₙ has n(n − 1)/2 edges.", "A graphic sequence has an even sum and each term at most n − 1 (necessary, not sufficient).", "Havel–Hakimi decides whether a sequence is realisable."],
         subs=["Degrees & counting"], widget="graph", hint="Draw a graph and watch the degree sum stay even.")

# ------------------------------------------------------------------------------------------------ 5.2
A.lesson("engm-gr-special", "Special graphs, bipartite graphs and isomorphism",
         key="Complete, bipartite, cycle, wheel and hypercube graphs appear constantly, so their vertex and edge counts must be known. A graph is bipartite exactly when it has no odd cycle, and isomorphic graphs share every structural invariant.",
         analogy=("🧱", "Standard building blocks", "Most exam graphs are built from a handful of named shapes. Knowing their counts saves drawing them: a cycle is a ring, a wheel is a ring with a hub, a hypercube is a cube of any dimension."),
         defs=[("Complete graph Kₙ", "n vertices with every pair adjacent."),
               ("Bipartite graph", "A graph whose vertices split into two sets with every edge between the sets."),
               ("Complete bipartite K_{m,n}", "Parts of sizes m and n with every cross pair adjacent."),
               ("Isomorphic graphs", "Graphs related by a bijection of vertices that preserves adjacency.")],
         parts=[dict(h="Counts for the standard graphs", md="""| Graph | Vertices | Edges | Notes |
|---|---|---|---|
| Kₙ | n | n(n − 1)/2 | (n − 1)-regular |
| path Pₙ | n | n − 1 | a tree |
| cycle Cₙ | n | n | 2-regular, bipartite iff n even |
| wheel Wₙ (hub plus Cₙ) | n + 1 | 2n | |
| K_{m,n} | m + n | m·n | bipartite |
| hypercube Qₙ | 2ⁿ | n·2ⁿ⁻¹ | n-regular, bipartite |
| Petersen graph | 10 | 15 | 3-regular, non-planar |"""),
                 dict(h="Bipartite graphs", md="""A graph is bipartite iff it contains **no odd cycle**; equivalently it can be 2-coloured. Trees, even cycles, hypercubes and K_{m,n} are bipartite; triangles and odd cycles are not. A bipartite graph on n vertices has at most ⌊n²/4⌋ edges, reached by K_{⌊n/2⌋,⌈n/2⌉}. The test is a breadth-first search that alternates colours; a clash on an edge reveals an odd cycle."""),
                 dict(h="Isomorphism", md="""Two graphs are isomorphic if a vertex relabelling turns one into the other. Isomorphic graphs agree on: number of vertices and edges, degree sequence, number of components, number of cycles of each length, planarity and chromatic number. Different values of any one invariant prove two graphs are **not** isomorphic; agreement on all of them is not a proof of isomorphism, so exhibit an explicit bijection. A graph and its complement may be isomorphic (self-complementary), as C₅ and P₄ are.""")],
         examples=[
             Ex("Hypercube", "How many vertices and edges does the hypercube Q₅ have?", ["Vertices 2⁵ = 32; each vertex has degree 5.", "Edges = 32·5/2."], "**32** vertices and **80** edges.", verify=lambda: "%d vertices and %d edges" % (2 ** 5, 5 * 2 ** 4)),
             Ex("Maximum bipartite edges", "What is the largest number of edges in a simple bipartite graph on 11 vertices?", ["The best split is 5 and 6: K₅,₆ has 5·6 edges."], "**30**", verify=lambda: str((11 // 2) * (11 - 11 // 2))),
             Ex("Is it bipartite?", "Is the cycle C₇ bipartite? Is the wheel W₆?", ["C₇ is an odd cycle: not bipartite.", "W₆ contains triangles (hub with two adjacent rim vertices): not bipartite."], "**No** for both.", verify=lambda: "No for both"),
             Ex("Wheel", "How many edges does the wheel with a hub and an 8-cycle have?", ["8 rim edges + 8 spokes."], "**16**", verify=lambda: str(2 * 8)),
             Ex("GATE style: non-isomorphic", "Two graphs both have 6 vertices, 7 edges and degree sequence 3, 3, 2, 2, 2, 2. One contains a triangle and the other does not. Are they isomorphic?", ["Isomorphic graphs have the same number of triangles.", "So they cannot be isomorphic, although all counts agree."], "**No.**", verify=lambda: "No")],
         traps=[("Bipartite needs no odd cycle", "One odd cycle is enough to rule it out."),
                ("Counting wheel vertices", "Wₙ has n + 1 vertices (the hub plus the rim)."),
                ("Equal degree sequences", "They do not prove isomorphism."),
                ("Hypercube edges", "Qₙ has n·2ⁿ⁻¹ edges, not n·2ⁿ.")],
         quick=[("Number of edges in K₃,₄", ["7", "12", "14", "24"], 1, "3·4."),
                ("A graph is bipartite iff it has no", ["even cycle", "odd cycle", "triangle only", "bridge"], 1, "Odd cycles obstruct 2-colouring."),
                ("Edges of Q₄", ["16", "24", "32", "64"], 2, "4·2³."),
                ("Maximum edges of a bipartite graph on 10 vertices", ["20", "25", "45", "50"], 1, "5·5.")],
         summary=["Kₙ: n(n − 1)/2 edges. Cₙ: n edges. Wₙ: 2n edges. K_{m,n}: mn edges. Qₙ: n·2ⁿ⁻¹ edges.", "A graph is bipartite iff it has no odd cycle iff it is 2-colourable.", "A bipartite graph on n vertices has at most ⌊n²/4⌋ edges.", "Isomorphic graphs share all invariants; one differing invariant proves non-isomorphism.", "Trees and even cycles are bipartite."],
         subs=["Graph identities"])

# ------------------------------------------------------------------------------------------------ 5.3
A.lesson("engm-gr-euler", "Connectivity, Euler and Hamilton paths",
         key="A connected graph has an Euler circuit exactly when every degree is even, and an Euler path when exactly 0 or 2 degrees are odd. Hamilton cycles visit every vertex once; no simple test exists, only sufficient conditions such as Dirac's.",
         analogy=("🌉", "The bridges of Königsberg", "Euler showed that the famous walk crossing each bridge once was impossible because four land masses each touched an odd number of bridges. Hamilton asks a different question: visit every town once."),
         defs=[("Walk, path, cycle", "A walk is a sequence of adjacent vertices; a path repeats no vertex; a cycle is a closed path."),
               ("Connected graph", "A graph in which every two vertices are joined by a path; its maximal connected pieces are the components."),
               ("Euler circuit / path", "A closed / open walk using every edge exactly once."),
               ("Hamilton cycle", "A cycle visiting every vertex exactly once.")],
         parts=[dict(h="Connectivity", md="""A graph with n vertices and c components has at least n − c edges. Hence fewer than n − 1 edges means the graph is disconnected. The *maximum* number of edges of a disconnected simple graph on n vertices is C(n − 1, 2) (a complete graph on n − 1 vertices plus an isolated vertex), so **C(n − 1, 2) + 1 edges guarantee connectivity**. With k components the maximum is C(n − k + 1, 2).

A **bridge** is an edge whose removal disconnects the graph; a **cut vertex** is a vertex with the same property. Every edge of a tree is a bridge."""),
                 dict(h="Euler circuits and paths", md="""For a connected graph:

- **Euler circuit** exists iff every vertex has even degree;
- **Euler path** (not closed) exists iff exactly 0 or 2 vertices have odd degree; with two odd vertices the path runs between them.

Kₙ has an Euler circuit iff n is odd (degrees n − 1 are even). Reading the degrees is the whole test, so counting odd-degree vertices decides every such question. For directed graphs the condition is in-degree = out-degree at every vertex."""),
                 dict(h="Hamilton cycles", md="""A Hamilton cycle visits every vertex once. No degree test characterises such graphs; deciding the question is NP-complete. Useful facts:

- **Dirac:** if n ≥ 3 and every vertex has degree ≥ n/2, the graph is Hamiltonian.
- Kₙ (n ≥ 3) is Hamiltonian and contains (n − 1)!/2 distinct Hamilton cycles (fix a start, order the others, and identify a cycle with its reverse).
- A bipartite graph with parts of unequal size has no Hamilton cycle.
- A cut vertex whose removal leaves 2 or more components rules a Hamilton cycle out.""")],
         examples=[
             Ex("Euler circuit of Kₙ", "Does K₅ have an Euler circuit? Does K₄?", ["K₅ has all degrees 4: even, so yes.", "K₄ has all degrees 3: odd, so no."], "K₅ **yes**, K₄ **no**.", verify=lambda: "K₅ yes, K₄ no" if (5 - 1) % 2 == 0 and (4 - 1) % 2 == 1 else "?"),
             Ex("Euler path", "A connected graph has degrees 2, 2, 3, 3, 4. Which of Euler circuit / Euler path exists?", ["Exactly two odd-degree vertices (the two 3s).", "So an Euler path exists, but not a circuit."], "An Euler **path** but no circuit.", verify=lambda: "An Euler path but no circuit" if sum(d % 2 for d in [2, 2, 3, 3, 4]) == 2 else "?"),
             Ex("Hamilton cycles in a complete graph", "How many distinct Hamilton cycles does K₇ have?", ["(7 − 1)!/2 = 720/2."], "**360**", verify=lambda: str(math.factorial(6) // 2)),
             Ex("Guaranteeing connectivity", "What is the least number of edges that guarantees a simple graph on 8 vertices is connected?", ["The largest disconnected graph is K₇ plus an isolated vertex, with C(7, 2) = 21 edges.", "One more edge forces connectivity."], "**22**", verify=lambda: str(C(7, 2) + 1)),
             Ex("GATE style: components", "A graph with 12 vertices and 8 edges has at least how many components?", ["A graph with c components has at least n − c edges.", "8 ≥ 12 − c gives c ≥ 4."], "**4**", verify=lambda: str(12 - 8))],
         traps=[("Euler versus Hamilton", "Euler uses every edge once; Hamilton visits every vertex once."),
                ("Euler needs connectivity", "Even degrees alone are not enough if the graph is disconnected."),
                ("Counting Hamilton cycles", "Divide by 2 because a cycle and its reverse coincide."),
                ("Dirac is sufficient only", "Graphs below Dirac's bound may still be Hamiltonian (cycles).")],
         quick=[("An Euler circuit exists in a connected graph when", ["all degrees are even", "all degrees are odd", "the graph is complete", "the graph is planar"], 0, "Degree parity is the whole test."),
                ("A connected graph with exactly two odd-degree vertices has", ["an Euler circuit", "an Euler path but no circuit", "neither", "a Hamilton cycle"], 1, "The path joins the two odd vertices."),
                ("Hamilton cycles in K₅", ["12", "24", "60", "120"], 0, "4!/2."),
                ("Minimum edges guaranteeing a connected graph on 6 vertices", ["6", "10", "11", "15"], 2, "C(5, 2) + 1.")],
         summary=["Euler circuit ⇔ connected with all degrees even; Euler path ⇔ 0 or 2 odd degrees.", "Kₙ has an Euler circuit iff n is odd.", "Dirac: degree ≥ n/2 everywhere ⇒ Hamiltonian; Kₙ has (n − 1)!/2 Hamilton cycles.", "C(n − 1, 2) + 1 edges force a graph on n vertices to be connected.", "A graph with c components has at least n − c edges."],
         subs=["Connectivity & paths"])

# ------------------------------------------------------------------------------------------------ 5.4
A.lesson("engm-gr-trees", "Trees and spanning trees",
         key="A tree is a connected graph without cycles: n vertices, n − 1 edges, a unique path between any two vertices, and every edge a bridge. Cayley's formula counts the nⁿ⁻² labelled trees on n vertices, which equals the number of spanning trees of Kₙ.",
         analogy=("🌳", "A family tree", "Exactly one line of descent joins any two relatives. Add one extra link between relatives and a loop appears; remove any link and the family splits in two."),
         defs=[("Tree", "A connected graph with no cycles."),
               ("Forest", "A graph with no cycles; each component is a tree."),
               ("Leaf", "A vertex of degree 1."),
               ("Spanning tree", "A subgraph that is a tree and contains every vertex of the graph.")],
         parts=[dict(h="Equivalent descriptions of a tree", md="""For a graph on n vertices the following are equivalent:

- G is a tree (connected and acyclic);
- G is connected with exactly n − 1 edges;
- G is acyclic with exactly n − 1 edges;
- there is exactly one path between every two vertices;
- G is minimally connected: removing any edge disconnects it.

A forest with c components on n vertices has n − c edges. Adding one edge to a tree creates exactly one cycle."""),
                 dict(h="Leaves and degrees", md="""Every tree with n ≥ 2 vertices has at least two leaves (the ends of a longest path). Because Σdeg = 2(n − 1), a tree with nᵢ vertices of degree i satisfies

$$n_1 = 2 + n_3 + 2n_4 + 3n_5 + \\cdots,$$

and degree-2 vertices do not affect the count. In a full m-ary tree with i internal vertices there are mi + 1 vertices and (m − 1)i + 1 leaves."""),
                 dict(h="Counting spanning trees", md="""- **Cayley's formula:** Kₙ has nⁿ⁻² spanning trees; this is also the number of labelled trees on n vertices (3 for n = 3, 16 for n = 4, 125 for n = 5).
- The cycle Cₙ has n spanning trees (remove any one edge).
- K_{m,n} has mⁿ⁻¹·nᵐ⁻¹.
- For a general graph use the Matrix-Tree theorem: the number of spanning trees equals any cofactor of the Laplacian matrix L = D − A.

A spanning tree of a connected graph has n − 1 edges, and a graph is connected exactly when it has a spanning tree.""")],
         examples=[
             Ex("Edges of a tree", "How many edges does a tree with 25 vertices have, and how many does a forest with 25 vertices and 4 trees have?", ["Tree: n − 1 = 24.", "Forest: n − c = 25 − 4 = 21."], "**24** and **21**.", verify=lambda: "%d and %d" % (25 - 1, 25 - 4)),
             Ex("Leaves", "A tree has 3 vertices of degree 3, 2 of degree 4, and every other vertex is a leaf. How many leaves?", ["n₁ = 2 + n₃ + 2n₄ = 2 + 3 + 2·2."], "**9**", verify=lambda: str(2 + 3 + 2 * 2)),
             Ex("Labelled trees", "How many labelled trees are there on 5 vertices?", ["Cayley: 5³."], "**125**", verify=lambda: str(5 ** 3)),
             Ex("Spanning trees of a cycle", "How many spanning trees does C₈ have?", ["Remove any one of the 8 edges."], "**8**", verify=lambda: str(8)),
             Ex("GATE style: full ternary tree", "A full 3-ary tree has 7 internal vertices. How many vertices and how many leaves does it have?", ["Vertices: mi + 1 = 3·7 + 1 = 22.", "Leaves: 22 − 7 = 15."], "**22** vertices and **15** leaves.", verify=lambda: "%d vertices and %d leaves" % (3 * 7 + 1, 3 * 7 + 1 - 7))],
         traps=[("Cayley counts labelled trees", "It counts spanning trees of the labelled Kₙ, not unlabelled shapes."),
                ("Forest edge count", "A forest with c components has n − c edges, not n − 1."),
                ("Leaves from degrees", "Use Σdeg = 2(n − 1) and ignore degree-2 vertices."),
                ("Adding an edge", "One extra edge creates exactly one cycle.")],
         quick=[("Edges in a tree with 9 vertices", ["8", "9", "10", "18"], 0, "n − 1."),
                ("Labelled trees on 4 vertices", ["4", "12", "16", "64"], 2, "4²."),
                ("Every tree with n ≥ 2 vertices has at least", ["one leaf", "two leaves", "n/2 leaves", "no leaves"], 1, "The ends of a longest path."),
                ("Spanning trees of the cycle C₆", ["1", "5", "6", "36"], 2, "Remove any edge.")],
         summary=["A tree is connected and acyclic: n − 1 edges, a unique path between any two vertices, every edge a bridge.", "A forest with c components has n − c edges.", "n₁ = 2 + n₃ + 2n₄ + … fixes the number of leaves of a tree.", "Cayley: nⁿ⁻² labelled trees; Cₙ has n spanning trees.", "A full m-ary tree with i internal vertices has mi + 1 vertices."],
         subs=["Trees & spanning trees"])

# ------------------------------------------------------------------------------------------------ 5.5
A.lesson("engm-gr-planar", "Planar graphs and Euler's formula",
         key="A planar graph can be drawn without crossings. For a connected planar graph v − e + f = 2, which with 3f ≤ 2e gives e ≤ 3v − 6 (e ≤ 2v − 4 without triangles). K₅ and K₃,₃ are the two basic non-planar graphs.",
         analogy=("🗺️", "Roads without flyovers", "Planarity asks whether the roads of a network can be drawn on flat paper with no crossings. Euler's formula counts the regions the roads cut the paper into."),
         defs=[("Planar graph", "A graph that can be drawn in the plane with no two edges crossing."),
               ("Face", "A region of the plane bounded by edges of a planar drawing; the unbounded region is the outer face."),
               ("Subdivision", "A graph obtained by inserting new vertices of degree 2 into edges.")],
         parts=[dict(h="Euler's formula", md="""For a connected planar graph drawn without crossings, with v vertices, e edges and f faces (including the outer one):

$$v-e+f=2 .$$

For a planar graph with c components the formula becomes v − e + f = 1 + c. Every drawing of the same graph has the same number of faces."""),
                 dict(h="Edge bounds", md="""Every face is bounded by at least 3 edges and every edge borders at most 2 faces, so 3f ≤ 2e. With Euler's formula this gives, for a simple planar graph with v ≥ 3:

- **e ≤ 3v − 6**;
- if there is no triangle (every face has at least 4 edges): **e ≤ 2v − 4**.

These are *necessary* conditions: failing one proves a graph non-planar, passing one proves nothing. Also, every planar graph has a vertex of degree at most 5."""),
                 dict(h="Non-planar graphs", md="""- **K₅** has 10 edges but 3·5 − 6 = 9: non-planar.
- **K₃,₃** has 9 edges but, being triangle-free, 2·6 − 4 = 8: non-planar.
- **Kuratowski's theorem:** a graph is planar iff it contains no subdivision of K₅ or K₃,₃. (Wagner: iff no minor of either.)
- The Petersen graph is non-planar; K₄, the cube Q₃ and every K₂,ₙ are planar.

To disprove planarity, find a subdivision of K₅ or K₃,₃ or break an edge bound; to prove it, draw the graph without crossings.""")],
         examples=[
             Ex("Faces", "A connected planar graph has 10 vertices and 15 edges. How many faces does any drawing have?", ["f = 2 − v + e = 2 − 10 + 15."], "**7**", verify=lambda: str(2 - 10 + 15)),
             Ex("Maximum edges", "What is the largest number of edges of a simple planar graph on 9 vertices?", ["3v − 6 = 27 − 6."], "**21**", verify=lambda: str(3 * 9 - 6)),
             Ex("Triangle-free planar", "What is the largest number of edges of a simple triangle-free planar graph on 9 vertices?", ["2v − 4 = 18 − 4."], "**14**", verify=lambda: str(2 * 9 - 4)),
             Ex("Why K₃,₃ is not planar", "Use an edge bound to show K₃,₃ is not planar.", ["K₃,₃ has v = 6, e = 9 and no triangle (it is bipartite).", "A triangle-free planar graph has e ≤ 2v − 4 = 8, but 9 > 8."], "**Not planar**: 9 edges exceed the bound 8.", verify=lambda: "Not planar: %d edges exceed the bound %d" % (9, 2 * 6 - 4)),
             Ex("GATE style: regular faces", "A connected planar graph has every face bounded by exactly 4 edges and has 8 faces. How many edges and vertices does it have?", ["Each edge borders two faces: 4f = 2e gives e = 16.", "Euler: v = 2 + e − f = 2 + 16 − 8."], "**16** edges and **10** vertices.", verify=lambda: "%d edges and %d vertices" % (4 * 8 // 2, 2 + 16 - 8))],
         traps=[("Using the bound as a test", "e ≤ 3v − 6 can hold for a non-planar graph; it only disproves planarity."),
                ("Forgetting the outer face", "f counts the unbounded face too."),
                ("Disconnected graphs", "Use v − e + f = 1 + c."),
                ("Triangle-free bound", "Use 2v − 4 when there are no triangles.")],
         quick=[("Faces of a connected planar graph with v = 6, e = 9", ["4", "5", "6", "7"], 1, "2 − 6 + 9."),
                ("Maximum edges of a simple planar graph on 8 vertices", ["16", "18", "20", "28"], 1, "3·8 − 6."),
                ("Which graph is non-planar?", ["K₄", "K₅", "the cube", "K₂,₅"], 1, "10 edges exceed 9."),
                ("Kuratowski's theorem concerns", ["K₅ and K₃,₃", "K₄ and K₃,₂", "trees", "bipartite graphs"], 0, "Forbidden subdivisions.")],
         summary=["Connected planar: v − e + f = 2; with c components v − e + f = 1 + c.", "Simple planar graphs satisfy e ≤ 3v − 6, and e ≤ 2v − 4 if triangle-free.", "The bounds disprove planarity but never prove it.", "K₅ and K₃,₃ are non-planar; a graph is planar iff it has no subdivision of either.", "Every planar graph has a vertex of degree at most 5."],
         subs=["Planar graphs"])

# ------------------------------------------------------------------------------------------------ 5.6
A.lesson("engm-gr-colour", "Graph colouring",
         key="The chromatic number χ(G) is the fewest colours that colour the vertices so adjacent vertices differ. Bipartite graphs need 2, odd cycles need 3, Kₙ needs n, and every planar graph needs at most 4. A clique gives a lower bound and Δ + 1 an upper bound.",
         analogy=("🎨", "Colouring a map", "Neighbouring countries must get different colours. An odd ring of neighbours cannot be coloured with two colours, so a third is forced."),
         defs=[("Proper colouring", "An assignment of colours to the vertices so that adjacent vertices receive different colours."),
               ("Chromatic number χ(G)", "The fewest colours in a proper colouring."),
               ("Clique", "A set of pairwise adjacent vertices; ω(G) is the size of a largest one.")],
         parts=[dict(h="Bounds on χ", md="""- **Lower bound:** χ(G) ≥ ω(G), since a clique needs distinct colours. Also χ ≥ 2 as soon as there is an edge.
- **Upper bound:** χ(G) ≤ Δ(G) + 1 (greedy colouring); Brooks: χ ≤ Δ unless G is a complete graph or an odd cycle.
- **Four colour theorem:** every planar graph has χ ≤ 4. Five colours always suffice by a short proof.
- χ(G) = 1 iff there are no edges."""),
                 dict(h="Values to know", md="""| Graph | χ |
|---|---|
| Kₙ | n |
| bipartite graph, tree, even cycle | 2 |
| odd cycle | 3 |
| wheel Wₙ (n-cycle rim) | 3 if n even, 4 if n odd |
| K_{m,n} | 2 |
| Petersen graph | 3 |

A graph is 2-colourable iff it is bipartite iff it has no odd cycle."""),
                 dict(h="Counting colourings", md="""The number of proper colourings with k colours is the **chromatic polynomial** P(G, k). For a tree on n vertices P = k(k − 1)ⁿ⁻¹; for Kₙ, k(k − 1)…(k − n + 1); for the cycle Cₙ, (k − 1)ⁿ + (−1)ⁿ(k − 1). The deletion–contraction rule P(G) = P(G − e) − P(G / e) computes it for other graphs.""")],
         examples=[
             Ex("Odd cycle", "What is the chromatic number of C₇?", ["An odd cycle cannot be 2-coloured and 3 colours suffice."], "**3**", verify=lambda: str(3)),
             Ex("A wheel", "What is the chromatic number of the wheel with hub and an 8-cycle? And with a 7-cycle?", ["Even rim: the rim needs 2 colours, the hub a third: 3.", "Odd rim: the rim needs 3, the hub a fourth: 4."], "**3** and **4**.", verify=lambda: "%d and %d" % (2 + 1, 3 + 1)),
             Ex("Proper colourings of a path", "How many proper 3-colourings does a path on 4 vertices have?", ["First vertex 3 choices, each next vertex 2 choices (different from its neighbour): 3·2·2·2."], "**24**", verify=lambda: str(3 * 2 ** 3)),
             Ex("A bound", "A graph contains K₅ as a subgraph and has maximum degree 6. What can χ be?", ["χ ≥ ω ≥ 5 and χ ≤ Δ + 1 = 7."], "**5, 6 or 7**.", verify=lambda: "5, 6 or 7"),
             Ex("GATE style: complete bipartite", "What is the chromatic number of K₃,₄, and how many proper colourings with k colours does K₂,₁ (a path on 3 vertices) have?", ["K₃,₄ is bipartite with an edge: χ = 2.", "A path on 3 vertices is a tree: k(k − 1)²."], "χ = **2**; **k(k − 1)²** colourings.", verify=lambda: "χ = 2; k(k − 1)² colourings")],
         traps=[("χ and degree", "Δ + 1 is only an upper bound; trees have Δ large but χ = 2."),
                ("Odd wheel", "An odd rim forces four colours."),
                ("Four colour theorem", "It bounds planar graphs only; K₅ needs 5."),
                ("Clique versus colouring", "A graph can need more colours than its largest clique (odd cycles: ω = 2, χ = 3).")],
         quick=[("χ(K₆)", ["2", "3", "5", "6"], 3, "All vertices are mutually adjacent."),
                ("χ of a tree with an edge", ["1", "2", "3", "depends on Δ"], 1, "Trees are bipartite."),
                ("χ of an even cycle", ["2", "3", "4", "n"], 0, "It is bipartite."),
                ("Every planar graph is colourable with at most", ["3 colours", "4 colours", "5 colours only", "6 colours only"], 1, "The four colour theorem.")],
         summary=["χ(G) ≥ ω(G) and χ(G) ≤ Δ + 1.", "Bipartite ⇔ χ ≤ 2 ⇔ no odd cycle.", "χ(Kₙ) = n; odd cycle 3; wheel 3 or 4.", "Every planar graph has χ ≤ 4.", "A tree has k(k − 1)ⁿ⁻¹ proper k-colourings."],
         subs=["Chromatic & connectivity"])

# ------------------------------------------------------------------------------------------------ 5.7
A.lesson("engm-gr-matching", "Matchings, vertex covers and independent sets",
         key="A matching is a set of edges with no shared vertex; a vertex cover is a set of vertices touching every edge; an independent set has no two adjacent vertices. A set is independent iff its complement is a vertex cover, and in bipartite graphs the maximum matching equals the minimum vertex cover.",
         analogy=("💃", "Pairing dancers", "Each dancer may have at most one partner, so a matching is a set of dancing pairs. A vertex cover is a set of people who, between them, belong to every possible pair."),
         defs=[("Matching", "A set of edges, no two of which share a vertex; it is perfect if it covers every vertex."),
               ("Vertex cover", "A set of vertices such that every edge has an endpoint in the set; β(G) is the minimum size."),
               ("Independent set", "A set of pairwise non-adjacent vertices; α(G) is the maximum size."),
               ("Edge cover", "A set of edges touching every vertex.")],
         parts=[dict(h="Four numbers and how they relate", md="""| Quantity | Meaning | Relations |
|---|---|---|
| ν(G) | size of a maximum matching | ν ≤ ⌊n/2⌋ and ν ≤ β |
| β(G) | size of a minimum vertex cover | α + β = n |
| α(G) | size of a maximum independent set | α + β = n |
| ρ(G) | size of a minimum edge cover (no isolated vertices) | ν + ρ = n (Gallai) |

The relation α + β = n holds because a set S is independent exactly when every edge has an endpoint outside S, i.e. when the complement of S is a vertex cover."""),
                 dict(h="Bipartite graphs", md="""**König's theorem:** in a bipartite graph, the maximum matching size equals the minimum vertex cover size, ν = β. It fails otherwise: a triangle has ν = 1 but β = 2.

**Hall's theorem:** a bipartite graph with parts X and Y has a matching covering X iff every subset S ⊆ X has at least |S| neighbours. A **perfect matching** needs an even number of vertices; K₂ₖ has (2k − 1)!! = (2k − 1)(2k − 3)⋯1 of them."""),
                 dict(h="Values for standard graphs", md="""| Graph | Max matching ν | Independence α |
|---|---|---|
| Kₙ | ⌊n/2⌋ | 1 |
| K_{m,n} | min(m, n) | max(m, n) |
| path Pₙ | ⌊n/2⌋ | ⌈n/2⌉ |
| cycle Cₙ | ⌊n/2⌋ | ⌊n/2⌋ |""")],
         examples=[
             Ex("A path", "Find the maximum matching, independence number and minimum vertex cover of the path P₇.", ["Matching: every other edge, ⌊7/2⌋ = 3.", "Independent set: vertices 1, 3, 5, 7, so α = 4, hence β = 7 − 4 = 3 (= ν, since a path is bipartite)."], "ν = **3**, α = **4**, β = **3**.", verify=lambda: "ν = %d, α = %d, β = %d" % (7 // 2, (7 + 1) // 2, 7 - (7 + 1) // 2)),
             Ex("Complete bipartite", "What is the minimum vertex cover of K₃,₅?", ["The graph is bipartite, so β = ν = min(3, 5)."], "**3**", verify=lambda: str(min(3, 5))),
             Ex("Perfect matchings", "How many perfect matchings does K₆ have?", ["Vertex 1 has 5 choices of partner, then the next unmatched vertex has 3, then 1."], "**15**", verify=lambda: str(5 * 3 * 1)),
             Ex("Gallai's relation", "A graph on 10 vertices has a minimum vertex cover of size 4. What is its independence number?", ["α = n − β."], "**6**", verify=lambda: str(10 - 4)),
             Ex("GATE style: König fails", "Find ν and β for the triangle K₃ and say why König's theorem does not apply.", ["Any two edges of a triangle share a vertex: ν = 1.", "One vertex covers only 2 of the 3 edges, so β = 2.", "A triangle is not bipartite."], "ν = **1**, β = **2**; K₃ is not bipartite.", verify=lambda: "ν = %d, β = %d; K₃ is not bipartite" % (1, 2))],
         traps=[("Matching versus cover", "A matching selects edges; a cover selects vertices."),
                ("König outside bipartite graphs", "In a triangle ν = 1 but β = 2."),
                ("Perfect matchings need even n", "A graph on an odd number of vertices has none."),
                ("Counting perfect matchings", "Multiply (2k − 1)(2k − 3)…1, not (2k)!.")],
         quick=[("Maximum matching in K₇", ["3", "4", "6", "7"], 0, "⌊7/2⌋."),
                ("α + β equals", ["|E|", "n", "2n", "ν"], 1, "Complements."),
                ("König's theorem holds for", ["all graphs", "bipartite graphs", "planar graphs", "trees only"], 1, "ν = β there."),
                ("Perfect matchings of K₄", ["2", "3", "6", "24"], 1, "3·1.")],
         summary=["ν ≤ ⌊n/2⌋ and ν ≤ β; α + β = n; ν + ρ = n.", "König: for bipartite graphs ν = β.", "Hall: X can be matched iff |N(S)| ≥ |S| for all S ⊆ X.", "K_{m,n}: ν = min(m, n); path Pₙ: ν = ⌊n/2⌋; Kₙ: ν = ⌊n/2⌋.", "K₂ₖ has (2k − 1)!! perfect matchings."],
         subs=["Matching & covers"])
