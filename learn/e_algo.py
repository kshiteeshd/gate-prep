"""Textbook-style long-form teaching text: Algorithms."""
from learn import elab

elab("algo-asymptotics",
 ("Why we need asymptotic notation", """
Suppose two programs solve the same problem. On your laptop, program A takes 0.8 seconds and program B takes 1.1 seconds. Is A better? Not necessarily: a faster machine, a different language or a different input could reverse that. What we really want to know is **how the running time grows as the input gets bigger**, because that is what stays true on every machine.

We measure the input size by a number $n$ (the number of elements to sort, the number of vertices in a graph, the number of bits in a number). We count the *basic steps* the algorithm performs as a function $T(n)$ and then describe how $T(n)$ grows, ignoring constant factors and small terms. If $T(n)=3n^2+10n+7$, the term $3n^2$ dominates once $n$ is large, so we say $T(n)$ is "of order $n^2$".

This is why $n^2$ always loses to $n\\log n$ for large enough $n$: no constant factor can rescue it.
"""),
 ("The three notations, one at a time", """
**Big-O: an upper bound.** $f(n)=O(g(n))$ means that, for large $n$, $f$ grows *no faster than* $g$. Formally, there are constants $c>0$ and $n_0$ such that $f(n)\\le c\\,g(n)$ for all $n\\ge n_0$. So $3n^2+10n+7=O(n^2)$ — and also $O(n^3)$, since an upper bound need not be tight.

**Big-Omega: a lower bound.** $f(n)=\\Omega(g(n))$ means $f$ grows *at least as fast as* $g$: $f(n)\\ge c\\,g(n)$ for large $n$.

**Big-Theta: a tight bound.** $f(n)=\\Theta(g(n))$ means both: $f$ is squeezed between two constant multiples of $g$. Then $f$ and $g$ have the same growth rate.

A good picture: O is "at most", Ω is "at least", Θ is "exactly, up to constants". A common confusion is to treat O as "the worst case". It is not: O describes how a *function* grows. Worst case, best case and average case are statements about *which input* we are analysing; each of them can have its own O, Ω and Θ.
"""),
 ("Comparing functions and counting loops", """
To rank functions, remember the ladder from slowest to fastest growth:

$$1 \\ll \\log n \\ll \\sqrt n \\ll n \\ll n\\log n \\ll n^2 \\ll n^3 \\ll 2^n \\ll n! \\ll n^n$$

Any polynomial beats any logarithm, any exponential beats any polynomial. When two expressions look close, take logarithms of both sides: $n^{\\log n}$ versus $2^{\\sqrt n}$ becomes $(\\log n)^2$ versus $\\sqrt n\\,\\log 2$, and the square root wins eventually.

**Counting loop iterations.** A loop `for (i = 1; i <= n; i++)` runs $n$ times. A loop `for (i = 1; i <= n; i *= 2)` runs about $\\log_2 n$ times, because $i$ doubles. Nested loops multiply, *unless* the inner bound depends on the outer variable: `for i in 1..n: for j in 1..i` does $1+2+\\dots+n=\\frac{n(n+1)}{2}=\\Theta(n^2)$ steps.

**Amortised cost** averages the cost over a *sequence* of operations. Appending to a dynamic array costs $O(1)$ most of the time and $O(n)$ when it must grow, but doubling the capacity makes the average cost per append $O(1)$.
"""),
)

elab("algo-recurrences-dc",
 ("Divide and conquer in plain words", """
Many efficient algorithms follow one pattern: **split the problem into smaller copies of itself, solve each copy (recursively), and combine the answers**. Merge sort sorts the two halves of an array and merges them. Binary search discards half the array each time. Quick sort partitions the array and sorts each side.

Because the algorithm calls itself, its running time is described by a **recurrence**, an equation that expresses $T(n)$ in terms of $T$ on smaller inputs. For merge sort:

$$T(n)=2\\,T\\!\\left(\\frac n2\\right)+n$$

The two recursive calls each work on half the array, and merging costs about $n$. Our task is to turn such an equation into a closed form like $\\Theta(n\\log n)$.
"""),
 ("Solving recurrences by hand", """
**Substitution (unrolling).** Expand the recurrence a few times and look for the pattern. For $T(n)=T(n-1)+n$:

$$T(n)=n+(n-1)+(n-2)+\\dots+1=\\frac{n(n+1)}{2}=\\Theta(n^2)$$

**The recursion tree.** Draw the calls as a tree. Each node is labelled with the work done *at that call* (excluding recursive calls). The total running time is the sum of all labels. In merge sort, level 0 costs $n$, level 1 has two nodes costing $n/2$ each (total $n$), and so on: every level costs $n$, and there are $\\log_2 n$ levels, so the total is $n\\log_2 n$.

The tree also shows *where the work concentrates*: at the top (the combine step dominates), at the bottom (the leaves dominate), or evenly across all levels. That is exactly what the Master theorem sorts into three cases.
"""),
 ("The Master theorem, understood rather than memorised", """
For recurrences of the form $T(n)=a\\,T(n/b)+f(n)$ with $a\\ge1,\\ b>1$, compare $f(n)$ with $n^{\\log_b a}$, which is the total cost of the *leaves* of the recursion tree.

- **Case 1:** $f(n)$ grows *polynomially slower* than $n^{\\log_b a}$ ⇒ the leaves dominate: $T(n)=\\Theta(n^{\\log_b a})$.
- **Case 2:** $f(n)=\\Theta(n^{\\log_b a}\\log^k n)$ ⇒ every level contributes about equally: $T(n)=\\Theta(n^{\\log_b a}\\log^{k+1}n)$.
- **Case 3:** $f(n)$ grows *polynomially faster* and satisfies the regularity condition ⇒ the root dominates: $T(n)=\\Theta(f(n))$.

**Example.** $T(n)=4T(n/2)+n$. Here $\\log_2 4=2$, so the leaves cost $n^2$ and $f(n)=n$ is smaller ⇒ Case 1, $T(n)=\\Theta(n^2)$.

**Example.** $T(n)=2T(n/2)+n$. $\\log_2 2=1$, so $n^{1}$ equals $f(n)$ ⇒ Case 2, $T(n)=\\Theta(n\\log n)$.

The theorem does **not** apply when the subproblems are of unequal size ($T(n)=T(n/3)+T(2n/3)+n$), when $a$ is not constant, or when $f(n)$ falls in the gap between the cases (like $n^{\\log_b a}/\\log n$). Then use the recursion tree.
"""),
)

elab("algo-sorting-searching",
 ("What sorting is, and why so many algorithms exist", """
Sorting means rearranging a list into increasing (or decreasing) order. It matters because sorted data is easy to search, to merge and to compare. There are many sorting algorithms because each makes a different trade-off between **speed**, **extra memory**, **stability** (equal keys keep their original order) and **behaviour on special inputs** (already sorted, nearly sorted, many duplicates).

A **comparison sort** only learns about the data by comparing two elements at a time. We will see that any comparison sort needs at least about $n\\log_2 n$ comparisons in the worst case.
"""),
 ("The simple quadratic sorts", """
**Bubble sort** repeatedly swaps adjacent elements that are out of order; after each pass the largest remaining element "bubbles" to the end. It takes $\\Theta(n^2)$ comparisons; with an early-exit flag it takes only $O(n)$ on an already-sorted array.

**Selection sort** repeatedly finds the minimum of the unsorted part and places it at the front. It always does $\\Theta(n^2)$ comparisons but only $O(n)$ swaps.

**Insertion sort** grows a sorted prefix: take the next element and slide it left until it is in place. Its cost is $\\Theta(n+I)$ where $I$ is the number of **inversions** (pairs out of order). On a sorted array $I=0$ (linear time); on a reversed array $I=\\frac{n(n-1)}{2}$ (quadratic). It is stable, in place, and the best of the three for small or nearly sorted inputs.
"""),
 ("Merge sort, quick sort and heap sort", """
**Merge sort** splits the array in half, sorts each half, and merges. Merging two sorted lists of total size $n$ takes $\\Theta(n)$ by repeatedly taking the smaller front element. The recurrence $T(n)=2T(n/2)+\\Theta(n)$ gives $\\Theta(n\\log n)$ in *every* case. It is stable but needs $\\Theta(n)$ extra space.

**Quick sort** picks a **pivot**, partitions the array into elements smaller and larger than the pivot, and recurses on both sides. If the pivot splits evenly, $T(n)=2T(n/2)+n$ and the cost is $\\Theta(n\\log n)$; if the pivot is always the smallest or largest (e.g. sorted input with the first element as pivot) the splits are $0$ and $n-1$, giving $T(n)=T(n-1)+n=\\Theta(n^2)$. Average case is $\\Theta(n\\log n)$, and random pivots make the bad case very unlikely. It sorts in place and is usually the fastest in practice.

**Heap sort** builds a max-heap in $O(n)$ and then repeatedly extracts the maximum, $O(\\log n)$ each: $\\Theta(n\\log n)$ in all cases, in place, but not stable.
"""),
 ("Beating the barrier: linear-time sorts and the lower bound", """
**Why $n\\log n$ is a barrier.** A comparison sort can be drawn as a binary decision tree whose leaves are the possible orderings. There are $n!$ orderings, so the tree has at least $n!$ leaves and hence height at least $\\log_2(n!)=\\Theta(n\\log n)$. No comparison sort can beat this.

**Counting sort** avoids comparisons: for integer keys in $0..k$, count how many times each value appears, compute running totals, and place each element directly. It runs in $\\Theta(n+k)$ and is stable. **Radix sort** sorts by one digit at a time using a stable sort, in $\\Theta(d(n+k))$ for $d$-digit keys. **Bucket sort** distributes values into buckets and sorts each; it is $\\Theta(n)$ on average for uniformly distributed inputs.

**Searching.** Linear search takes $O(n)$. **Binary search** needs a *sorted* array: compare the middle element and discard half, so it takes $O(\\log n)$. Selecting the $k$-th smallest element can be done in $O(n)$ expected time by quick-select.
"""),
)

elab("algo-greedy",
 ("The greedy idea", """
A **greedy algorithm** builds a solution step by step and, at every step, picks the choice that looks best *right now*, never reconsidering. Greedy is wonderfully simple and fast — but a locally best choice is not always part of a globally best solution. A greedy algorithm is correct only for problems that have two properties:

- **Greedy-choice property:** some optimal solution contains the greedy first choice.
- **Optimal substructure:** after making that choice, what remains is a smaller problem of the same kind, and an optimal solution to it combines with the choice to give an optimal whole.

To *prove* a greedy algorithm correct you typically use an **exchange argument**: take any optimal solution, and show that swapping one of its choices for the greedy choice does not make it worse.
"""),
 ("Activity selection and fractional knapsack", """
**Activity selection.** Given activities with start and finish times, choose the maximum number that do not overlap. The greedy rule is: *always pick the activity that finishes earliest* among those compatible with what has been chosen. Why does it work? The earliest-finishing activity leaves the most room for the others, so any optimal schedule can be modified to start with it.

(Greedy rules that sound plausible but fail: "shortest activity first" and "earliest start first".)

**Fractional knapsack.** Items have weights and values, and you may take fractions. Sort by **value per unit weight** and take items in that order, taking a fraction of the last one. It is optimal because every unit of capacity should hold the most valuable material available.

The **0/1 knapsack** (items cannot be split) is different: the greedy ratio rule can fail, and the problem needs dynamic programming.
"""),
 ("Huffman coding and greedy on graphs", """
**Huffman coding** compresses text using shorter bit strings for frequent characters. Build a tree by repeatedly **merging the two least-frequent nodes** into a new node whose frequency is their sum. The code for a character is the path from the root (0 for left, 1 for right). Because only leaves carry characters, no code is the prefix of another, so decoding is unambiguous. Using a min-heap, the construction takes $O(n\\log n)$.

**Greedy on graphs.** Kruskal's and Prim's algorithms for minimum spanning trees and Dijkstra's algorithm for shortest paths are greedy: each repeatedly takes the cheapest allowable edge or vertex. Dijkstra fails with negative edge weights, which is a reminder that a greedy method is only as good as the property that makes it correct.

**Job sequencing with deadlines.** Each job takes unit time, has a deadline and a profit. Sort jobs by decreasing profit and place each in the latest free slot on or before its deadline.
"""),
)

elab("algo-dynamic-programming",
 ("From recursion to dynamic programming", """
Consider computing Fibonacci numbers with $F(n)=F(n-1)+F(n-2)$. The plain recursion recomputes the same values again and again, and takes exponential time. The fix is simple: **compute each subproblem once and remember the answer**. That is dynamic programming (DP).

DP applies when a problem has:

- **Optimal substructure:** the best answer is built from best answers to smaller subproblems.
- **Overlapping subproblems:** the same subproblems appear again and again.

There are two ways to write a DP solution. **Top-down (memoisation)** keeps the recursion and stores each result in a table the first time it is computed. **Bottom-up (tabulation)** fills a table in order from the smallest subproblems to the largest, without recursion.
"""),
 ("A recipe for designing a DP", """
1. **Define the state.** What small set of numbers identifies a subproblem? For the longest common subsequence it is $(i,j)$, the prefixes $X[1..i]$ and $Y[1..j]$.
2. **Write the recurrence.** Express the answer to a state using answers to smaller states.
3. **Set base cases.** The smallest subproblems, usually with $i=0$ or $j=0$.
4. **Pick the order** in which to fill the table so every dependency is ready.
5. **Read off the answer** and, if needed, trace back to recover the actual solution.

The running time is usually *(number of states) × (work per state)*.
"""),
 ("Worked classics: LCS, knapsack, edit distance", """
**Longest common subsequence (LCS).** If the last characters match, extend the best answer for the shorter prefixes; otherwise drop one character from either string:

$$L[i][j]=\\begin{cases}L[i-1][j-1]+1 & X[i]=Y[j]\\\\ \\max(L[i-1][j],\\,L[i][j-1]) & \\text{otherwise}\\end{cases}$$

The table has $m\\times n$ cells, so the time is $\\Theta(mn)$.

**0/1 knapsack.** Let $K[i][w]$ be the best value using the first $i$ items with capacity $w$. Either skip item $i$, or take it (if it fits):

$$K[i][w]=\\max\\bigl(K[i-1][w],\\;v_i+K[i-1][w-w_i]\\bigr)$$

The time is $\\Theta(nW)$ — polynomial in the *numeric value* $W$ but exponential in the number of bits of $W$ (pseudo-polynomial).

**Edit distance.** The minimum number of insertions, deletions and substitutions to turn one string into another uses the same grid: from a cell you can come from the left (insert), above (delete) or diagonal (match or substitute), each with a cost.
"""),
 ("Matrix-chain multiplication and other patterns", """
Multiplying matrices is associative, so we can choose the order of the multiplications, and different orders can cost vastly different amounts. For a chain $A_1\\cdots A_n$ where $A_i$ is $p_{i-1}\\times p_i$, let $M[i][j]$ be the cheapest way to multiply $A_i\\cdots A_j$:

$$M[i][j]=\\min_{i\\le k<j}\\bigl(M[i][k]+M[k+1][j]+p_{i-1}p_kp_j\\bigr)$$

The table has $O(n^2)$ entries and each takes $O(n)$ to compute: $O(n^3)$ in total. Other DP patterns you should recognise: **longest increasing subsequence** ($O(n^2)$, or $O(n\\log n)$ with binary search), **coin change**, **rod cutting**, **subset sum** and the **Floyd–Warshall** algorithm for all-pairs shortest paths.
"""),
)

elab("algo-graph-traversal",
 ("Graphs and what it means to traverse one", """
A graph is a set of **vertices** (things) joined by **edges** (connections). Roads between cities, links between web pages and prerequisites between courses are all graphs. A **traversal** visits every vertex reachable from a starting vertex, each exactly once, following edges. The two basic traversals differ only in *which vertex they explore next*.
"""),
 ("Breadth-first search", """
BFS explores the graph in **layers**: first the start vertex, then all its neighbours, then all of their unvisited neighbours, and so on. It uses a **queue** (first in, first out). You mark a vertex as visited when you add it to the queue.

Because it visits vertices in order of their distance, BFS finds **shortest paths measured in number of edges** in an unweighted graph. The running time is $O(V+E)$ with adjacency lists, since each vertex is queued once and each edge is looked at once or twice.

A graph is **bipartite** exactly when its vertices can be 2-coloured so that no edge joins two vertices of the same colour. BFS can test this: colour layers alternately and check every edge.
"""),
 ("Depth-first search", """
DFS goes **as deep as possible** along one path before backing up. It can be written recursively (the call stack is the stack) or with an explicit stack. Record two times for each vertex: a **discovery time** when first reached and a **finish time** when all its neighbours have been explored.

The edges of a DFS fall into four types: **tree edges** (to a new vertex), **back edges** (to an ancestor — these exist exactly when the graph has a **cycle**), **forward edges** (to a descendant already visited) and **cross edges** (to a vertex in another subtree).

**Topological sort** of a directed acyclic graph (DAG) lists vertices so every edge goes from earlier to later. Run DFS and output the vertices in **decreasing finish time**. The graph has a valid ordering only if it has no cycle.
"""),
 ("Strongly connected components", """
In a directed graph, two vertices are in the same **strongly connected component (SCC)** if each can reach the other. Kosaraju's algorithm finds all SCCs in $O(V+E)$:

1. Run DFS on the graph and record the finish times.
2. Reverse every edge (the transpose graph).
3. Run DFS on the transpose, starting vertices in **decreasing finish time**. Each DFS tree is one SCC.

If you contract every SCC to a single vertex, the result is always a DAG, which is why SCCs reveal the "big picture" structure of a directed graph.
"""),
)

elab("algo-shortest-paths-mst",
 ("The shortest-path problem", """
In a **weighted graph** each edge has a cost. The **shortest path** from a source $s$ to a vertex $v$ is the path of least total cost. BFS only works when every edge costs 1. For general weights we need algorithms that handle different costs, and the right algorithm depends on whether negative weights exist.

Every shortest-path algorithm uses **relaxation**: if going to $v$ through $u$ is cheaper than the best-known route, update the estimate: if $d[u]+w(u,v)<d[v]$, set $d[v]=d[u]+w(u,v)$.
"""),
 ("Dijkstra, Bellman–Ford and Floyd–Warshall", """
**Dijkstra's algorithm** (non-negative weights) repeatedly takes the unvisited vertex with the smallest estimate, fixes it as final, and relaxes its outgoing edges. It is greedy: once a vertex is finalised, no later path can be shorter, because all edges are non-negative. With a binary heap it takes $O((V+E)\\log V)$; with an array, $O(V^2)$.

**Bellman–Ford** allows negative edges. It relaxes **all** edges $V-1$ times, in $O(VE)$. If another round still improves something, there is a **negative cycle** reachable from the source.

**Floyd–Warshall** computes shortest paths between **all pairs**, $O(V^3)$. Let $d_k[i][j]$ be the shortest path from $i$ to $j$ using only vertices $1..k$ as intermediates:

$$d_k[i][j]=\\min\\bigl(d_{k-1}[i][j],\\;d_{k-1}[i][k]+d_{k-1}[k][j]\\bigr)$$
"""),
 ("Minimum spanning trees", """
A **spanning tree** connects all vertices of a connected graph with $V-1$ edges and no cycle. A **minimum spanning tree (MST)** has the smallest total weight.

**Kruskal's algorithm.** Sort the edges by weight, then add each edge unless it would form a cycle (checked with a union–find structure). Time $O(E\\log E)$.

**Prim's algorithm.** Start from any vertex and repeatedly add the cheapest edge that connects the current tree to a new vertex. With a heap: $O(E\\log V)$.

Both rely on the **cut property**: for any way of splitting the vertices into two groups, the lightest edge crossing the split belongs to some MST. And on the **cycle property**: the heaviest edge on any cycle (if unique) belongs to no MST. If all edge weights are distinct, the MST is unique.
"""),
)

elab("algo-complexity-classes",
 ("Easy versus hard problems", """
Some problems can be solved in time bounded by a polynomial in the input size (sorting, shortest path); we call them **tractable**. For others, the best known algorithms take exponential time, and nobody has proved that no fast algorithm exists. Complexity theory organises problems into classes.

- **P**: decision problems solvable in polynomial time.
- **NP**: decision problems where a proposed solution (a "certificate") can be **verified** in polynomial time. Example: given a set of numbers and a target, a subset that sums to the target is easy to check, even if finding it seems hard.
- **co-NP**: problems whose *no* answers have short certificates.

Every problem in P is in NP, so $P\\subseteq NP$. Whether $P=NP$ is the most famous open question in computer science.
"""),
 ("Reductions and NP-completeness", """
A problem $A$ **reduces** to $B$ ($A\\le_p B$) if we can turn any instance of $A$ into an instance of $B$ in polynomial time, preserving the yes/no answer. If $B$ is easy, so is $A$; equivalently, if $A$ is hard, so is $B$.

A problem is **NP-hard** if every problem in NP reduces to it. It is **NP-complete** if it is NP-hard *and* in NP. The first NP-complete problem was **SAT** (Cook–Levin theorem); then, by chains of reductions, thousands of others were shown NP-complete: 3-SAT, vertex cover, clique, independent set, Hamiltonian cycle, subset sum, 0/1 knapsack (decision form), graph colouring with 3 or more colours.

To show that a new problem $X$ is NP-complete you must (1) show $X\\in NP$ and (2) reduce a *known* NP-complete problem *to* $X$ (direction matters).
"""),
 ("What to remember for the exam", """
- If any NP-complete problem is solved in polynomial time, then $P=NP$.
- **2-SAT is in P**, but 3-SAT is NP-complete. Shortest path and minimum spanning tree are in P; longest simple path is NP-hard.
- **Halting problem** is *undecidable* — no algorithm exists at all — which is a much stronger statement than NP-hardness.
- A **pseudo-polynomial** algorithm (such as the DP for knapsack in $O(nW)$) runs in time polynomial in the *value* of the numbers, but not in their bit-length.
"""),
)
