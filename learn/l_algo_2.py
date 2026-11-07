"""Algorithms — part 2: dynamic programming, graph algorithms, complexity classes."""
import itertools
import math
import random

from content import g_algo as A
from content import g_extra as X
from learn import Ex, lesson

S = "ALGO"


def _coin_ways(coins, n):
    w = [1] + [0] * n
    for c in coins:
        for i in range(c, n + 1):
            w[i] += w[i - c]
    return w[n]


def _lis_n2(a):
    L = [1] * len(a)
    for i in range(len(a)):
        for j in range(i):
            if a[j] < a[i]:
                L[i] = max(L[i], L[j] + 1)
    return max(L)


def _knap_brute(items, W):
    best = 0
    for m in range(1 << len(items)):
        v = sum(items[i][0] for i in range(len(items)) if m >> i & 1)
        w = sum(items[i][1] for i in range(len(items)) if m >> i & 1)
        if w <= W:
            best = max(best, v)
    return best


# ======================================================================================================
lesson(subject=S, chapter="Dynamic Programming", ch_no=3, no=1, slug="algo-dynamic-programming", title="Dynamic Programming: LCS, Edit Distance, Knapsack & Matrix Chain",
       topic="Dynamic Programming", minutes=26, weight=5, widget="dp",
       widget_hint="Choose LCS, edit distance or knapsack and change the inputs. The table is filled exactly as the recurrence says — the highlighted bottom-right cell is the answer.",
       key="Dynamic programming solves a problem by storing the answers to overlapping subproblems instead of recomputing them. Define the subproblem, write the recurrence, fill a table in dependency order — the table size is usually the running time.",
       analogy=("🗺️", "Remembering directions", "If you ask a friend how to get from every street corner to the station, and later someone asks about a corner you already asked about, you simply reuse the stored answer instead of walking the whole route again. DP is that notebook: solve each distinct subproblem once, write the answer down, look it up later."),
       sections=[
           dict(h="When to use DP", md="""DP applies when a problem has:

- **Optimal substructure:** an optimal solution is built from optimal solutions to subproblems.
- **Overlapping subproblems:** the same subproblems recur many times (otherwise it is plain divide-and-conquer, e.g. merge sort).

Recipe: (1) define the state, e.g. `dp[i][j]`; (2) write the recurrence; (3) set base cases; (4) fill the table in an order that respects dependencies; (5) read off the answer (and backtrack if you need the solution itself). **Memoisation** (top-down recursion + cache) and **tabulation** (bottom-up loops) compute the same thing; time ≈ (number of states) × (work per state)."""),
           dict(h="Longest common subsequence (LCS)", md="""LCS of X[1..m] and Y[1..n] (a *subsequence* keeps order but need not be contiguous):""",
                formulas=[("L[i][j] = L[i−1][j−1] + 1   if X[i] = Y[j]", ""), ("L[i][j] = max(L[i−1][j], L[i][j−1])   otherwise", "L[0][*] = L[*][0] = 0")],
                call=[("key", "Cost", "Time and space **O(mn)** (a table of (m+1)(n+1) cells). Space can be reduced to O(min(m,n)) if only the length is needed.")]),
           dict(h="Edit distance and 0/1 knapsack", md="""**Edit distance** (insert, delete, substitute each cost 1), D[i][j] = distance between the first i letters of X and first j of Y:

    D[i][0] = i,  D[0][j] = j
    D[i][j] = D[i-1][j-1]                         if X[i] = Y[j]
            = 1 + min(D[i-1][j], D[i][j-1], D[i-1][j-1])   otherwise

**0/1 knapsack** (each item once; capacity W; item i has value vᵢ and weight wᵢ): K[i][c] = best value using the first i items with capacity c:

    K[i][c] = K[i-1][c]                      if wᵢ > c
            = max(K[i-1][c], vᵢ + K[i-1][c - wᵢ])   otherwise

Time O(nW) — **pseudo-polynomial**, because W is a number whose size is exponential in its bit-length."""),
           dict(h="Matrix-chain multiplication", md="""Multiplying A₁…Aₙ where Aᵢ is d[i−1]×d[i]: the cost depends on the *parenthesisation*. Let M[i][j] = minimum scalar multiplications for Aᵢ…Aⱼ:

    M[i][i] = 0
    M[i][j] = min over i ≤ k < j of  M[i][k] + M[k+1][j] + d[i-1]·d[k]·d[j]

O(n²) subproblems, O(n) work each ⇒ **O(n³)** time, O(n²) space. Multiplying a p×q matrix by a q×r matrix costs p·q·r scalar multiplications."""),
           dict(h="More classics", md="""- **Longest increasing subsequence (LIS):** L[i] = 1 + max L[j] over j < i with a[j] < a[i] — O(n²); O(n log n) with patience sorting (binary search on tails).
- **Coin change:** *number of ways* ways[i] += ways[i − c] over coins (order does not matter); *minimum coins* dp[i] = 1 + min dp[i − c].
- **Rod cutting**, **subset sum**, **partition** and **Floyd–Warshall** (all-pairs shortest paths, O(V³)) are DP too.
- **Fibonacci** with memoisation drops from Θ(φⁿ) to Θ(n); the Catalan numbers and optimal BSTs are further examples.

**DP vs greedy vs divide-and-conquer:** greedy commits to one choice without looking back; DP considers all choices but reuses sub-answers; D&C subproblems do not overlap."""),
       ],
       examples=[
           Ex("LCS length", "Find the length of the longest common subsequence of ABCBDAB and BDCABA.",
              ["Fill the 8 × 7 table with the recurrence above.", "The bottom-right cell is 4 (for example BCBA or BDAB)."],
              "**4**", verify=lambda: str(A.lcs("ABCBDAB", "BDCABA"))),
           Ex("Edit distance", "What is the edit distance between “kitten” and “sitting”?",
              ["k→s (substitute), e→i (substitute), and insert g at the end.", "That is 3 operations, and the DP table confirms 3 is the minimum."],
              "**3**", verify=lambda: str(A.edit("kitten", "sitting"))),
           Ex("0/1 knapsack", "Capacity 50 and items (value, weight) = (60, 10), (100, 20), (120, 30). What is the best total value if items cannot be split?",
              ["Options: items 1+2 weigh 30 → 160; items 1+3 weigh 40 → 180; items 2+3 weigh 50 → **220**; all three weigh 60 > 50.", "Best = 220 (note the greedy ratio rule would give 160 — it is wrong for 0/1)."],
              "**220**", verify=lambda: str(_knap_brute([(60, 10), (100, 20), (120, 30)], 50))),
           Ex("Matrix-chain", "Dimensions d = (10, 20, 30, 40, 30) for four matrices A₁…A₄. What is the minimum number of scalar multiplications?",
              ["Try all splits with M[i][j] = min M[i][k] + M[k+1][j] + d[i−1]·d[k]·d[j].", "The best split is ((A₁A₂)A₃)A₄: A₁A₂ costs 10·20·30 = 6000 (giving 10×30); times A₃ costs 10·30·40 = 12000 (giving 10×40); times A₄ costs 10·40·30 = 12000.", "Total = 6000 + 12000 + 12000 = **30000**, and the DP table confirms nothing is cheaper."],
              "**30000**", verify=lambda: str(A.mcm([10, 20, 30, 40, 30]))),
           Ex("Counting coin combinations", "In how many ways can 10 be made from coins {2, 5, 3, 6} (unlimited supply, order ignored)?",
              ["Process coins one at a time: ways[i] += ways[i − coin].", "The final entry is **5**. The five combinations are: 2+2+2+2+2, 2+2+3+3, 2+2+6, 2+3+5 and 5+5."],
              "**5**", verify=lambda: str(_coin_ways([2, 5, 3, 6], 10))),
       ],
       traps=[("Subsequence vs substring", "LCS allows gaps (subsequence); the longest common *substring* needs contiguity and has a different recurrence."),
              ("Greedy for 0/1 knapsack", "Picking by value/weight fails; the DP considers include/exclude for every item."),
              ("Knapsack is not polynomial", "O(nW) is pseudo-polynomial; the problem is NP-complete."),
              ("Wrong fill order", "Each cell must be computed after the cells it depends on (top-left to bottom-right for LCS/edit distance).")],
       quick=[("The time to compute the LCS of strings of length m and n by DP is", ["O(m + n)", "O(mn)", "O(2^m)", "O(m log n)"], 1, "One cell per (i, j) pair."),
              ("Matrix-chain multiplication DP runs in", ["O(n²)", "O(n³)", "O(n log n)", "O(2ⁿ)"], 1, "n² states × O(n) splits."),
              ("0/1 knapsack with n items and capacity W has DP time", ["O(n log W)", "O(nW)", "O(2ⁿ)", "O(n + W)"], 1, "Pseudo-polynomial."),
              ("Memoisation turns Fibonacci from exponential to", ["O(log n)", "O(n)", "O(n²)", "O(1)"], 1, "Each fib(k) computed once.")],
       summary=["DP = optimal substructure + overlapping subproblems; store sub-answers.", "LCS: match → diagonal + 1, else max(up, left); O(mn).", "Edit distance: 1 + min(insert, delete, substitute) on mismatch.",
                "0/1 knapsack: max(exclude, include); O(nW) pseudo-polynomial.", "Matrix chain: min over splits of M[i][k] + M[k+1][j] + d[i−1]d[k]d[j]; O(n³).", "Greedy ≠ DP: greedy fails for 0/1 knapsack and coin change."])


# ======================================================================================================
def _bfs_dfs(n, edges):
    adj = {i: [] for i in range(n)}
    for a, b in edges:
        adj[a].append(b); adj[b].append(a)
    for k in adj:
        adj[k].sort()
    from collections import deque
    seen, q, bfs = {0}, deque([0]), []
    while q:
        u = q.popleft(); bfs.append(u)
        for v in adj[u]:
            if v not in seen:
                seen.add(v); q.append(v)
    dfs, vis = [], set()

    def go(u):
        vis.add(u); dfs.append(u)
        for v in adj[u]:
            if v not in vis:
                go(v)
    go(0)
    return "".join(chr(65 + i) for i in bfs), "".join(chr(65 + i) for i in dfs)


def _topo_count(n, edges):
    return sum(1 for p in itertools.permutations(range(n)) if all(p.index(a) < p.index(b) for a, b in edges))


def _scc_count(n, edges):
    reach = [[i == j for j in range(n)] for i in range(n)]
    for a, b in edges:
        reach[a][b] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if reach[i][k] and reach[k][j]:
                    reach[i][j] = True
    seen, c = set(), 0
    for i in range(n):
        if i not in seen:
            c += 1
            seen |= {j for j in range(n) if reach[i][j] and reach[j][i]}
    return c


lesson(subject=S, chapter="Graph Algorithms", ch_no=4, no=1, slug="algo-graph-traversal", title="Graph Traversal: BFS, DFS, Topological Sort & SCC",
       topic="Graph Algorithms", minutes=22, weight=5, widget="traverse",
       widget_hint="Choose BFS or DFS and a start vertex to see the visit order. Switch to topological sort or strongly connected components (these use directed edges: u->v).",
       key="BFS explores layer by layer with a queue and finds fewest-edge paths; DFS dives deep with a stack/recursion and powers cycle detection, topological sort and strongly connected components — both run in O(V + E) with adjacency lists.",
       analogy=("🏛️", "Exploring a building", "BFS is checking every room on the current floor before taking the stairs up — you find the *closest* exit first. DFS is following one corridor all the way to its dead end, then backing up to the last junction — good for exploring every nook and for noticing when a corridor loops back on itself."),
       sections=[
           dict(h="BFS and DFS", md="""| | BFS | DFS |
|---|---|---|
| Data structure | queue | stack / recursion |
| Visits | all neighbours first | one branch to the end first |
| Shortest paths | **yes**, fewest edges (unweighted) | no |
| Time (adjacency list) | **O(V + E)** | **O(V + E)** |
| Time (adjacency matrix) | O(V²) | O(V²) |
| Extra space | O(V) (queue) | O(V) (stack / recursion depth) |

Both visit every vertex of a component exactly once; running them from every unvisited vertex finds all **connected components**. The visit order depends on the order in which neighbours are examined — questions usually say ‘alphabetical’."""),
           dict(h="DFS timestamps and edge types", md="""DFS records **discovery** and **finish** times. In a DFS of a **directed** graph every edge is one of four kinds:

- **Tree edge:** leads to an undiscovered vertex (forms the DFS forest).
- **Back edge:** goes to an ancestor — its presence means the graph has a **cycle**.
- **Forward edge:** to a descendant that is not a tree child. **Cross edge:** between different subtrees.

In an **undirected** graph every non-tree edge is a back edge (no forward or cross edges). A directed graph is a **DAG** iff DFS finds no back edge."""),
           dict(h="Topological sort", md="""A **topological order** of a DAG lists the vertices so that every edge u → v has u before v. It exists **iff the graph is acyclic**, and is generally **not unique**.

- **DFS method:** output vertices in **decreasing finish time** (reverse post-order).
- **Kahn's method:** repeatedly remove a vertex of in-degree 0 (queue); if vertices remain at the end there is a cycle.

Both take O(V + E). Uses: task scheduling, build systems, course prerequisites."""),
           dict(h="Strongly connected components and bipartiteness", md="""A **strongly connected component (SCC)** of a directed graph is a maximal set of vertices in which every vertex can reach every other. Contracting each SCC gives a DAG.

**Kosaraju's algorithm** (O(V + E)): (1) run DFS on G and record finish order; (2) build the **transpose** Gᵀ (reverse every edge); (3) run DFS on Gᵀ visiting vertices in **decreasing finish time** — each DFS tree is one SCC.

**Bipartite test:** BFS/DFS 2-colouring; the graph is bipartite iff no edge joins two vertices of the same colour (equivalently, no odd cycle). Also: a **bridge** or **articulation point** can be found with DFS low-link values in O(V + E)."""),
       ],
       examples=[
           Ex("BFS and DFS order", "Undirected graph on A–F with edges AB, AC, BD, CD, CE, DF, EF. Neighbours are taken alphabetically. Give the BFS and DFS orders from A.",
              ["BFS: A; its neighbours B, C; then B's new neighbour D and C's new neighbour E; then F (from D). Order **A B C D E F**.", "DFS: A → B → D → C (D's first unvisited neighbour) → E → F. Order **A B D C E F**."],
              "BFS = **ABCDEF**, DFS = **ABDCEF**.", verify=lambda: "BFS = %s, DFS = %s" % _bfs_dfs(6, [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5)])),
           Ex("Number of topological orders", "A DAG on A–D has edges A→B, A→C, B→D, C→D. How many topological orderings are there?",
              ["A must come first and D last.", "B and C can appear in either order: A B C D and A C B D.", "So there are **2**."],
              "**2**", verify=lambda: str(_topo_count(4, [(0, 1), (0, 2), (1, 3), (2, 3)]))),
           Ex("Strongly connected components", "Directed graph with edges 1→2, 2→3, 3→1, 3→4, 4→5, 5→4. How many SCCs does it have?",
              ["{1, 2, 3} form a cycle — one SCC.", "{4, 5} form a cycle — another SCC.", "The edge 3→4 only goes one way, so they do not merge. Total **2**."],
              "**2**", verify=lambda: str(_scc_count(5, [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 3)]))),
           Ex("Cycle detection by Kahn's algorithm", "If Kahn's algorithm removes only 3 of the 5 vertices of a directed graph before running out of in-degree-0 vertices, what does that mean?",
              ["The remaining 2 vertices all have an incoming edge from within the remaining set.", "That is only possible if they lie on (or are reachable from) a cycle."],
              "The graph contains a **cycle** (it is not a DAG)."),
       ],
       traps=[("DFS and shortest paths", "Only BFS gives fewest-edge paths in unweighted graphs; a DFS path can be arbitrarily long."),
              ("Adjacency matrix cost", "With a matrix, finding the neighbours of a vertex costs O(V), so BFS/DFS become O(V²)."),
              ("Topological order uniqueness", "There can be many valid orders; the answer is unique only if the DAG has a Hamiltonian path."),
              ("Back edge in undirected DFS", "The edge to the parent is the tree edge — don't count it as a back edge when detecting cycles.")],
       quick=[("BFS uses a ___ and DFS uses a ___.", ["stack, queue", "queue, stack", "heap, queue", "queue, heap"], 1, "FIFO vs LIFO."),
              ("A directed graph has a topological order iff it is", ["strongly connected", "a DAG", "a tree", "bipartite"], 1, "No cycles."),
              ("The time of BFS on an adjacency-list graph is", ["O(V)", "O(V + E)", "O(V²)", "O(E log V)"], 1, "Each vertex and edge once."),
              ("Kosaraju's SCC algorithm runs DFS twice, the second time on", ["the same graph", "the transpose graph", "the complement", "an MST"], 1, "Reverse all edges.")],
       summary=["BFS (queue) = shortest paths in unweighted graphs; DFS (stack) = cycle detection, topo sort, SCC; both O(V + E) with lists.", "Directed DFS edge types: tree, back (cycle!), forward, cross; undirected: only tree and back.",
                "Topological sort: decreasing finish time, or Kahn's in-degree removal; exists iff DAG; not unique.", "Kosaraju: DFS on G, then DFS on Gᵀ in decreasing finish order.", "Bipartite ⇔ 2-colourable ⇔ no odd cycle.", "Adjacency matrix makes traversal O(V²)."])


# ======================================================================================================
def _fw_ops(v):
    return v ** 3


lesson(subject=S, chapter="Graph Algorithms", ch_no=4, no=2, slug="algo-shortest-paths-mst", title="Shortest Paths & Minimum Spanning Trees",
       topic="Graph Algorithms", minutes=24, weight=5, widget="traverse",
       widget_hint="Pick Dijkstra, Bellman–Ford, Kruskal or Prim on the sample weighted graph (edit the weights freely) and compare the results. Tick ‘directed’ and use a negative weight to see Bellman–Ford catch a negative cycle.",
       key="Dijkstra finds single-source shortest paths when no edge is negative; Bellman–Ford allows negative edges and detects negative cycles; Floyd–Warshall does all pairs in O(V³). Kruskal and Prim build a minimum spanning tree greedily using the cut/cycle properties.",
       analogy=("🛣️", "Road trips and cheapest networks", "Shortest path: the quickest way from your house to every town, one traveller. Minimum spanning tree: the cheapest set of roads that connects *all* towns together, no matter who travels where. Different questions — one is about distances from a source, the other about total cost of a connected network."),
       sections=[
           dict(h="Dijkstra's algorithm", md="""**Single-source shortest paths, non-negative weights.** Keep a tentative distance d[v] (∞ initially, 0 for the source). Repeatedly pick the unfinished vertex u with the smallest d, finalise it, and **relax** its edges: if d[u] + w(u,v) < d[v] set d[v] = d[u] + w(u,v).

| Implementation | Time |
|---|---|
| Array (linear minimum search) | O(V²) |
| Binary heap + adjacency list | **O((V + E) log V)** |
| Fibonacci heap | O(E + V log V) |

It is **greedy** and fails with negative edge weights (a finalised vertex could later be improved).""",
                call=[("trap", "Negative edges", "One negative edge can break Dijkstra even without a negative cycle. Adding a constant to all weights does **not** fix it (it changes which path is shortest).")]),
           dict(h="Bellman–Ford and Floyd–Warshall", md="""**Bellman–Ford:** relax **every edge V − 1 times**. Time **O(VE)**. Works with negative edges; after V − 1 rounds, if some edge can still be relaxed there is a **negative cycle** reachable from the source.

**Floyd–Warshall:** all-pairs shortest paths by dynamic programming over intermediate vertices: d[i][j] = min(d[i][j], d[i][k] + d[k][j]) for k = 1..V. Time **O(V³)**, space O(V²); handles negative edges (not negative cycles).

| Problem | Best choice |
|---|---|
| One source, non-negative weights | Dijkstra |
| One source, negative edges | Bellman–Ford |
| All pairs, dense graph | Floyd–Warshall |
| Unweighted | BFS, O(V + E) |
| DAG | topological order + one pass, O(V + E) |"""),
           dict(h="Minimum spanning tree: Kruskal and Prim", md="""A **spanning tree** connects all V vertices with V − 1 edges; the **MST** has the least total weight.

- **Kruskal:** sort edges by weight; add an edge if it does **not form a cycle** (union–find). Time **O(E log E) = O(E log V)**. Good for sparse graphs.
- **Prim:** grow one tree from a start vertex, always adding the cheapest edge leaving the tree. Time O(V²) with an array, **O(E log V)** with a heap. Good for dense graphs.

Both are greedy and give the same total weight. If all edge weights are **distinct**, the MST is **unique**. The MST also minimises the *maximum* edge (bottleneck) on the path between any two vertices."""),
           dict(h="Why they are correct: cut and cycle properties", md="""- **Cut property:** for any cut of the vertices, the **lightest edge crossing the cut** belongs to some MST. (This justifies both Prim and Kruskal.)
- **Cycle property:** the **heaviest edge on any cycle** (if unique) belongs to no MST.

An MST has exactly V − 1 edges. Adding any non-tree edge creates exactly one cycle. The number of spanning trees of Kₙ is nⁿ⁻² (Cayley), but the *minimum* one has V − 1 edges whatever the weights."""),
       ],
       examples=[
           Ex("Dijkstra distances", "Undirected graph with edges A–B 4, A–C 2, B–C 1, B–D 5, C–D 8, C–E 10, D–E 2. Find the shortest distance from A to E.",
              ["d(A) = 0. Relax A: B = 4, C = 2.", "Pick C (2): B improves to 3 (via C–B), D = 10, E = 12. Pick B (3): D improves to 8.", "Pick D (8): E improves to 10. Final d(E) = **10** (path A–C–B–D–E)."],
              "**10**", verify=lambda: str(A.dijkstra(5, [(0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5), (2, 3, 8), (2, 4, 10), (3, 4, 2)], 0)[4])),
           Ex("MST weight", "For the same graph find the weight of a minimum spanning tree.",
              ["Sort edges: B–C 1, A–C 2, D–E 2, A–B 4, B–D 5, C–D 8, C–E 10.", "Kruskal: add B–C (1), A–C (2), D–E (2), skip A–B (cycle), add B–D (5) connecting {A,B,C} with {D,E}.", "Total = 1 + 2 + 2 + 5 = **10**."],
              "**10**", verify=lambda: str(A.mst_weight(5, [(0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5), (2, 3, 8), (2, 4, 10), (3, 4, 2)]))),
           Ex("Floyd–Warshall cost", "About how many basic steps does Floyd–Warshall perform on a graph with 40 vertices?",
              ["Floyd–Warshall has three nested loops (k, i, j), each over all V vertices.", "Total relaxations = V³ = 40³ = **64000**."],
              "**64000**", verify=lambda: str(_fw_ops(40))),
           Ex("Bellman–Ford rounds", "How many rounds of edge relaxation does Bellman–Ford need on a graph with 8 vertices to guarantee correct distances when there is no negative cycle?",
              ["A shortest path has at most V − 1 edges, and each round fixes one more edge of every path.", "Rounds needed = V − 1 = **7** (an 8th round that still improves signals a negative cycle)."],
              "**7**", verify=lambda: str(8 - 1)),
       ],
       traps=[("Dijkstra with negative edges", "Not valid — use Bellman–Ford."),
              ("Kruskal vs Prim", "Both give the same MST weight; the choice is about implementation and density (Kruskal O(E log E), Prim O(E log V))."),
              ("MST ≠ shortest-path tree", "The MST minimises total weight; the shortest-path tree minimises distances from the source. They differ in general."),
              ("Uniqueness", "An MST is unique if edge weights are distinct; with ties there may be several (all of equal weight).")],
       quick=[("Dijkstra with a binary heap runs in", ["O(V²)", "O((V + E) log V)", "O(VE)", "O(V³)"], 1, "Heap operations per edge."),
              ("Which algorithm detects negative cycles?", ["Dijkstra", "Prim", "Bellman–Ford", "Kruskal"], 2, "A V-th round that still improves."),
              ("Floyd–Warshall time complexity:", ["O(V²)", "O(V³)", "O(VE)", "O(E log V)"], 1, "Three nested loops."),
              ("An MST of a graph with 12 vertices has how many edges?", ["11", "12", "13", "66"], 0, "V − 1.")],
       summary=["Dijkstra: non-negative weights; O((V+E) log V) with a heap, O(V²) with an array.", "Bellman–Ford: O(VE), negative edges OK, detects negative cycles (V − 1 rounds).", "Floyd–Warshall: all pairs, O(V³).",
                "MST has V − 1 edges: Kruskal O(E log E) with union–find; Prim O(E log V) with a heap.", "Cut property justifies both; distinct weights ⇒ unique MST.", "BFS for unweighted shortest paths; topological order for DAGs."])


# ======================================================================================================
def _vc_c5():
    n = 5
    e = [(i, (i + 1) % n) for i in range(n)]
    e = [tuple(sorted(x)) for x in e]
    return n - X.max_indep(n, e)


lesson(subject=S, chapter="Complexity", ch_no=5, no=1, slug="algo-complexity-classes", title="Complexity Classes: P, NP, NP-complete & Reductions",
       topic="Complexity Classes", minutes=22, weight=4, widget="none",
       key="P problems can be solved in polynomial time; NP problems can have a solution verified in polynomial time; NP-complete problems are the hardest in NP — if any one has a polynomial algorithm then P = NP. Reductions are how we prove hardness.",
       analogy=("🧩", "Sudoku", "Checking a completed Sudoku takes seconds — that is membership in NP. Finding the solution from scratch seems to need exhaustive search. Whether every puzzle whose answers are *easy to check* is also *easy to solve* is the P vs NP question — still open."),
       sections=[
           dict(h="P, NP, co-NP", md="""- **P:** decision problems solvable by a deterministic algorithm in **polynomial time** (shortest path, MST, sorting, primality testing, 2-SAT, bipartite matching, linear programming).
- **NP:** decision problems whose **‘yes’ answers can be verified** in polynomial time given a certificate (witness) — equivalently, solvable in polynomial time by a **non-deterministic** machine.
- **co-NP:** problems whose complement is in NP (e.g. unsatisfiability).

**P ⊆ NP** (an efficient algorithm is its own verifier). Whether P = NP is unknown; almost everyone believes P ≠ NP.""",
                formulas=[("P ⊆ NP   ·   P ⊆ co-NP", ""), ("P = NP ?   open", "")]),
           dict(h="Reductions, NP-hard and NP-complete", md="""A problem A **reduces** to B (A ≤ₚ B) if an instance of A can be converted in polynomial time into an instance of B with the same answer. Consequences: if B ∈ P then A ∈ P; if A is hard then B is hard.

- **NP-hard:** at least as hard as every problem in NP (every NP problem reduces to it). It need **not** be in NP (the halting problem is NP-hard but undecidable).
- **NP-complete = NP ∩ NP-hard.** The first one, **SAT**, was proved NP-complete by the **Cook–Levin theorem**. To prove a new problem X is NP-complete: (1) show X ∈ NP; (2) reduce a *known* NP-complete problem to X.""",
                call=[("key", "If one NPC problem is in P", "Then **every** problem in NP is in P, i.e. P = NP. And if P ≠ NP, no NP-complete problem has a polynomial algorithm.")]),
           dict(h="The classic NP-complete problems", md="""| NP-complete | Easy (in P) look-alike |
|---|---|
| **3-SAT** | **2-SAT** |
| Vertex cover, Clique, Independent set | Maximum matching, Min cut |
| **Hamiltonian cycle**, Travelling salesman (decision) | **Euler circuit** |
| **3-colourability** | **2-colourability** (bipartite) |
| Subset sum, Partition, 0/1 knapsack (decision) | Fractional knapsack |
| Set cover, Bin packing, Longest simple path | Shortest path |

Useful relations: a set S is an independent set ⇔ its complement V \\ S is a vertex cover, so **max independent set + min vertex cover = |V|**; a clique in G is an independent set in the complement graph. 3-SAT reduces to Clique, to Vertex Cover, and to 3-Colouring."""),
           dict(h="Pseudo-polynomial time and undecidability", md="""- An algorithm is **pseudo-polynomial** if it is polynomial in the *numeric value* of the input rather than its bit-length — e.g. the O(nW) knapsack DP. Subset sum and knapsack are **weakly** NP-complete for this reason.
- **Approximation:** for NP-hard optimisation problems we often settle for guaranteed ratios — a simple matching-based algorithm gives a 2-approximation for vertex cover.
- **Undecidable** problems (halting problem, equivalence of programs) have *no algorithm at all*; they are harder than NP. NP-hard ⊄ NP in general, and undecidable problems are NP-hard.""",
                call=[("trap", "NP does not mean ‘not polynomial’", "NP stands for **non-deterministic polynomial**. Every problem in P is also in NP.")]),
       ],
       examples=[
           Ex("Vertex cover from independent set", "The cycle C₅ has a maximum independent set of size 2. What is the size of its minimum vertex cover?",
              ["A set is a vertex cover exactly when its complement is independent.", "Min vertex cover = |V| − max independent set = 5 − 2 = **3**."],
              "**3**", verify=lambda: str(_vc_c5())),
           Ex("What follows from a polynomial algorithm for 3-SAT?", "Suppose someone finds a polynomial-time algorithm for 3-SAT. What can you conclude?",
              ["3-SAT is NP-complete, so every problem in NP reduces to it in polynomial time.", "Composing the reduction with the new algorithm solves every NP problem in polynomial time: **P = NP**."],
              "**P = NP**."),
           Ex("Classify the problem", "Is deciding whether a graph has an Euler circuit in P or NP-complete? Whether it has a Hamiltonian cycle?",
              ["Euler circuit ⇔ connected and all degrees even — checkable in linear time: **P**.", "Hamiltonian cycle has no known polynomial algorithm and is NP-complete."],
              "Euler circuit: **P**; Hamiltonian cycle: **NP-complete**."),
           Ex("Subset sum is pseudo-polynomial", "Subset sum with n numbers and target T can be solved in O(nT) time. Does that put it in P?",
              ["The input size is about n·log T bits, but the running time grows with the *value* T = 2^(log T).", "That is exponential in the input size, so it is **not** a polynomial-time algorithm — the problem is NP-complete."],
              "No — it is **pseudo-polynomial**, not polynomial."),
       ],
       traps=[("NP-hard vs NP-complete", "NP-complete needs membership in NP; NP-hard problems (like halting) may lie outside NP."),
              ("‘NP’ means not polynomial", "It means non-deterministic polynomial; P ⊆ NP."),
              ("2-SAT / 2-colouring", "Fixing the number to 2 makes SAT and colouring easy; 3 makes them NP-complete."),
              ("Reduction direction", "To prove X hard, reduce a known hard problem **to** X, not X to it.")],
       quick=[("Which is known?", ["P = NP", "P ⊆ NP", "NP ⊆ P", "P ≠ NP"], 1, "Deterministic ⊆ non-deterministic."),
              ("To prove X is NP-complete you show X ∈ NP and", ["X ≤ₚ SAT only", "a known NP-complete problem ≤ₚ X", "X ∈ P", "X is undecidable"], 1, "Reduce a known NPC problem to X."),
              ("Which problem is in P?", ["3-SAT", "Hamiltonian cycle", "2-SAT", "Vertex cover"], 2, "2-SAT has a linear-time algorithm."),
              ("For any graph, max independent set + min vertex cover =", ["|E|", "|V|", "2|V|", "|V| − 1"], 1, "They are complements of each other.")],
       summary=["P ⊆ NP; NP = poly-time verifiable; P vs NP open.", "NP-complete = in NP + NP-hard; SAT first (Cook–Levin); one polynomial NPC algorithm ⇒ P = NP.", "Prove hardness by reducing a known NPC problem to your problem.",
                "3-SAT, vertex cover, clique, Hamiltonian cycle, TSP, 3-colouring, subset sum are NPC; 2-SAT, matching, Euler circuit, 2-colouring are in P.", "Independent set ↔ vertex cover (complement); clique ↔ independent set in the complement graph.", "Pseudo-polynomial ≠ polynomial; halting problem is undecidable and NP-hard but not in NP."])
