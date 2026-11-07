"""PDS + Algorithms — curated concept questions."""
from content.kit import C

# ===================== PDS =====================
C("PDS", "C Programming & Pointers", "Concepts", [
    ("e", 1, "s", "A static local variable in C", ["retains its value between function calls", "is allocated on the stack each call", "is visible in other functions", "is initialised at every call"], 0, "It lives for the whole program but has local scope."),
    ("e", 1, "s", "In C, the name of an array used in an expression usually", ["decays to a pointer to its first element", "is a copy of the array", "is a pointer variable that can be reassigned", "stores the array length"], 0, "Except as an operand of sizeof or &."),
    ("m", 1, "s", "Dereferencing a NULL pointer in C results in", ["undefined behaviour", "a compile-time error always", "a value of 0", "a guaranteed exception"], 0, "Usually a segmentation fault."),
    ("m", 2, "s", "A dangling pointer is a pointer", ["that refers to memory that has been freed or gone out of scope", "that is NULL", "that points to the heap", "that has the wrong type"], 0, "Using it is undefined behaviour."),
    ("m", 2, "s", "A memory leak occurs when", ["dynamically allocated memory is not freed and becomes unreachable", "the stack overflows", "an array index exceeds bounds", "a pointer is NULL"], 0, "The heap shrinks for the rest of the run."),
    ("m", 1, "s", "const int *p means", ["p points to an int that cannot be modified through p", "p itself cannot change", "both cannot change", "p is NULL"], 0, "int * const p would make the pointer itself constant."),
    ("h", 2, "s", "For `int a[5]; int *p = a;`, the expression sizeof(a) / sizeof(*p) evaluates to", ["5", "1", "the size of a pointer", "undefined"], 0, "sizeof(a) is the whole array."),
    ("h", 2, "m", "Which of the following invoke undefined behaviour in C? (select all)", ["Signed integer overflow", "Modifying a variable twice between sequence points, e.g. i = i++ + 1", "Reading an uninitialised local variable", "Unsigned integer overflow"], [0, 1, 2], "Unsigned overflow wraps modulo 2^n and is well defined."),
    ("m", 1, "s", "Which storage class specifier gives a variable internal linkage at file scope?", ["static", "extern", "auto", "register"], 0, "static restricts visibility to the translation unit."),
    ("h", 2, "s", "`char *s = \"abc\"; s[0] = 'x';` results in", ["undefined behaviour (string literal is read-only)", "s becoming \"xbc\"", "a compile error", "a copy being modified"], 0, "Use char s[] = \"abc\" for a modifiable array."),
])

C("PDS", "Recursion", "Concepts", [
    ("e", 1, "s", "Every recursive function must have", ["a base case", "a loop", "global variables", "a pointer argument"], 0, "Otherwise recursion never terminates."),
    ("m", 1, "s", "The memory region that holds activation records of recursive calls is the", ["stack", "heap", "data segment", "code segment"], 0, "Deep recursion can cause stack overflow."),
    ("m", 2, "s", "Tail recursion can be optimised by the compiler into", ["iteration, using constant stack space", "a loop with extra memory", "a goto to main", "dynamic allocation"], 0, "The recursive call is the last operation."),
    ("m", 1, "s", "Naive recursive Fibonacci has time complexity", ["exponential", "linear", "quadratic", "logarithmic"], 0, "T(n) = T(n−1) + T(n−2) + 1."),
    ("h", 2, "s", "Memoization turns the naive recursive Fibonacci into", ["O(n) time with O(n) space", "O(log n) time", "O(2^n) time", "O(1) time"], 0, "Each subproblem is computed once."),
    ("h", 2, "s", "Mutual recursion between f and g", ["is allowed provided each function is declared before use", "is impossible in C", "needs dynamic memory", "makes the stack unnecessary"], 0, "A forward declaration solves ordering."),
])

C("PDS", "Arrays, Stacks & Queues", "Concepts", [
    ("e", 1, "s", "A stack follows", ["LIFO order", "FIFO order", "random order", "priority order"], 0, "Last in, first out."),
    ("e", 1, "s", "Which data structure is best suited for implementing a breadth-first search?", ["Queue", "Stack", "Heap", "Binary search tree"], 0, "FIFO ordering visits level by level."),
    ("m", 1, "s", "Function-call management and expression evaluation (postfix) use a", ["stack", "queue", "deque", "priority queue"], 0, "Operands/activation records are pushed and popped."),
    ("m", 2, "s", "In an array-based circular queue of size n, the queue is full when", ["(rear + 1) mod n == front (with one slot left empty)", "rear == front", "rear == n", "front == 0"], 0, "Equality of front and rear denotes empty."),
    ("m", 1, "s", "The time complexity of enqueue and dequeue in a linked-list queue with head and tail pointers is", ["O(1) each", "O(n) each", "O(log n)", "O(1) and O(n)"], 0, "No traversal needed."),
    ("h", 2, "s", "Accessing arr[i][j] of a row-major 2D array with C columns uses address", ["base + (i·C + j)·size", "base + (j·R + i)·size", "base + (i + j)·size", "base + i·j·size"], 0, "Column-major swaps the roles."),
    ("h", 2, "m", "Which operations can be done in O(1) on a stack implemented with an array? (select all)", ["push", "pop", "peek", "search for a given value"], [0, 1, 2], "Searching requires scanning."),
    ("h", 2, "s", "A deque supports", ["insertion and deletion at both ends", "insertion at one end only", "random access only", "sorted insertion"], 0, "Double-ended queue."),
])

C("PDS", "Linked Lists", "Concepts", [
    ("e", 1, "s", "Compared with arrays, linked lists", ["allow O(1) insertion/deletion at a known position but have O(n) random access", "have O(1) random access", "use less memory per element", "cannot grow"], 0, "Pointers add overhead."),
    ("m", 1, "s", "Deleting a node whose address is known in a SINGLY linked list (without the previous pointer) normally takes", ["O(n)", "O(1)", "O(log n)", "O(n²)"], 0, "You must find the predecessor (unless you copy the next node's data)."),
    ("m", 1, "s", "In a doubly linked list, deleting a node given a pointer to it takes", ["O(1)", "O(n)", "O(log n)", "O(√n)"], 0, "Both neighbours are directly reachable."),
    ("m", 2, "s", "Floyd's tortoise-and-hare algorithm detects", ["a cycle in O(n) time and O(1) space", "the middle node only", "the largest element", "palindromes"], 0, "The fast pointer eventually meets the slow one inside a cycle."),
    ("h", 2, "s", "Reversing a singly linked list iteratively takes", ["O(n) time and O(1) extra space", "O(n log n) time", "O(n) extra space", "O(n²) time"], 0, "Three pointers: prev, cur, next."),
    ("h", 2, "s", "Which structure allows the fastest insertion at the head and removal from the head with no resizing?", ["Singly linked list", "Dynamic array", "Sorted array", "Binary heap"], 0, "Both operations are O(1)."),
])

C("PDS", "Trees & BST", "Concepts", [
    ("e", 1, "s", "An inorder traversal of a binary search tree produces keys in", ["sorted (ascending) order", "descending order", "level order", "random order"], 0, "Left, root, right."),
    ("e", 1, "s", "The height of a balanced BST with n nodes is", ["O(log n)", "O(n)", "O(n log n)", "O(1)"], 0, "Skewed BSTs have height O(n)."),
    ("m", 1, "s", "In an AVL tree the balance factor of every node is", ["−1, 0 or +1", "0 only", "any integer", "≥ 0"], 0, "Height difference of the subtrees."),
    ("m", 2, "s", "An AVL tree insertion requires at most", ["one single or one double rotation", "log n rotations", "n rotations", "two double rotations"], 0, "After the first rebalancing, heights are restored."),
    ("m", 1, "s", "The worst-case time to search a BST with n nodes is", ["O(n)", "O(log n)", "O(1)", "O(n log n)"], 0, "A chain-like (skewed) tree."),
    ("h", 2, "s", "Deleting a BST node with two children is done by replacing it with its", ["inorder successor (or predecessor)", "parent", "root", "leftmost leaf of the left subtree only"], 0, "Then delete that node, which has at most one child."),
    ("h", 2, "s", "A red-black tree guarantees", ["height at most 2·log₂(n+1)", "perfect balance", "O(1) search", "no rotations ever"], 0, "Path lengths differ by at most a factor of 2."),
    ("h", 2, "m", "Which traversal pairs uniquely determine a binary tree (with distinct keys)? (select all)", ["Inorder + preorder", "Inorder + postorder", "Preorder + postorder", "Inorder + level order"], [0, 1, 3], "Preorder + postorder is ambiguous unless the tree is full."),
])

C("PDS", "Heaps & Hashing", "Concepts", [
    ("e", 1, "s", "A binary heap is a", ["complete binary tree with the heap-order property", "full binary search tree", "balanced AVL tree", "linked list"], 0, "Stored compactly in an array."),
    ("m", 1, "s", "Building a heap from n unsorted elements with Floyd's method takes", ["O(n)", "O(n log n)", "O(log n)", "O(n²)"], 0, "Most nodes are near the leaves."),
    ("m", 1, "s", "Extract-min from a binary min-heap has complexity", ["O(log n)", "O(1)", "O(n)", "O(n log n)"], 0, "Sift down after moving the last element to the root."),
    ("m", 2, "s", "In open addressing, clustering is a problem mostly associated with", ["linear probing", "double hashing", "chaining", "perfect hashing"], 0, "Primary clustering builds long runs."),
    ("m", 1, "s", "With chaining, the expected cost of an unsuccessful search under simple uniform hashing is", ["Θ(1 + α)", "Θ(log n)", "Θ(n)", "Θ(α²)"], 0, "α = n/m is the load factor."),
    ("h", 2, "s", "Open addressing requires the load factor α to be", ["less than 1", "greater than 1", "exactly 1", "unrestricted"], 0, "All keys live in the table itself."),
    ("h", 2, "s", "A good hash function should", ["distribute keys uniformly and be fast to compute", "map all keys to similar values", "be reversible", "depend on the table address"], 0, "Uniform distribution minimises collisions."),
])

C("PDS", "Graph Representation", "Concepts", [
    ("e", 1, "s", "The adjacency matrix of an undirected graph is always", ["symmetric", "diagonal", "upper triangular", "singular"], 0, "A[i][j] = A[j][i]."),
    ("m", 1, "s", "For sparse graphs the preferred representation is", ["adjacency lists", "adjacency matrix", "incidence matrix always", "edge matrix with weights"], 0, "O(V + E) space."),
    ("m", 1, "s", "Space used by an adjacency matrix for a graph with V vertices is", ["Θ(V²)", "Θ(V + E)", "Θ(E)", "Θ(V log V)"], 0, "Independent of the number of edges."),
    ("m", 2, "s", "Checking whether edge (u, v) exists takes O(1) in", ["an adjacency matrix", "an adjacency list", "an edge list", "a linked list of edges"], 0, "Direct indexing."),
    ("h", 2, "s", "BFS and DFS on a graph using adjacency lists run in", ["O(V + E)", "O(V²)", "O(E log V)", "O(V·E)"], 0, "Each vertex and edge is processed once."),
    ("h", 2, "s", "The sum of in-degrees of all vertices of a directed graph with E edges equals", ["E", "2E", "V", "E/2"], 0, "Each edge contributes one in-degree and one out-degree."),
])

# ===================== ALGORITHMS =====================
C("ALGO", "Asymptotic Analysis", "Concepts", [
    ("e", 1, "s", "Which of the following is TRUE?", ["2^(n+1) = O(2^n)", "2^(2n) = O(2^n)", "n! = O(2^n)", "n² = O(n log n)"], 0, "2^(n+1) = 2·2^n; 4^n grows faster than 2^n."),
    ("m", 1, "s", "log(n!) is", ["Θ(n log n)", "Θ(n)", "Θ(log n)", "Θ(n²)"], 0, "Stirling's approximation."),
    ("m", 2, "m", "Which of the following are TRUE? (select all)", ["n² + n = Θ(n²)", "3n = O(n²)", "n log n = Ω(n)", "n = Θ(n log n)"], [0, 1, 2], "n log n grows strictly faster than n."),
    ("m", 1, "s", "If f(n) = O(g(n)) and g(n) = O(h(n)), then", ["f(n) = O(h(n))", "f(n) = Θ(h(n))", "h(n) = O(f(n))", "nothing can be concluded"], 0, "Big-O is transitive."),
    ("h", 2, "s", "The solution of T(n) = T(√n) + 1 is", ["Θ(log log n)", "Θ(log n)", "Θ(√n)", "Θ(n)"], 0, "Let n = 2^m ⇒ T(m) = T(m/2) + 1."),
    ("h", 2, "s", "The solution of T(n) = 2T(n/2) + n log n is", ["Θ(n log² n)", "Θ(n log n)", "Θ(n²)", "Θ(n)"], 0, "Master theorem extended case: log^{k+1}."),
    ("h", 2, "s", "T(n) = T(n − 1) + n has solution", ["Θ(n²)", "Θ(n log n)", "Θ(n)", "Θ(2^n)"], 0, "Sum of 1..n."),
    ("m", 1, "s", "Binary search on a sorted array of n elements has worst-case time", ["Θ(log n)", "Θ(n)", "Θ(1)", "Θ(n log n)"], 0, "Halves the search space each step."),
])

C("ALGO", "Sorting & Searching", "Concepts", [
    ("e", 1, "s", "Which of the following sorting algorithms is NOT stable (in its typical implementation)?", ["Quick sort", "Merge sort", "Insertion sort", "Bubble sort"], 0, "Partitioning can reorder equal keys."),
    ("e", 1, "s", "The worst-case time complexity of quicksort is", ["O(n²)", "O(n log n)", "O(n)", "O(log n)"], 0, "Occurs on already sorted input with a poor pivot choice."),
    ("m", 1, "s", "Merge sort requires", ["O(n) auxiliary space", "O(1) auxiliary space", "O(log n) auxiliary space only", "no extra space"], 0, "For arrays; lists can be merged in place."),
    ("m", 1, "s", "Heap sort has worst-case time", ["O(n log n) and sorts in place", "O(n²)", "O(n) with O(n) space", "O(n log n) but is stable"], 0, "It is not stable."),
    ("m", 2, "s", "Counting sort on n integers in the range 0..k runs in", ["O(n + k)", "O(n log n)", "O(n k)", "O(k log n)"], 0, "No comparisons are made."),
    ("m", 2, "m", "Which sorting algorithms run in Θ(n²) time in the average AND worst case? (select all)", ["Selection sort", "Bubble sort", "Insertion sort", "Merge sort"], [0, 1, 2], "Insertion sort is Θ(n) in the best case only."),
    ("h", 2, "s", "Any comparison-based sorting algorithm needs at least how many comparisons in the worst case?", ["⌈log₂ n!⌉ = Ω(n log n)", "n − 1", "n²", "log n"], 0, "Decision-tree lower bound."),
    ("h", 2, "s", "The best-case time of insertion sort is", ["Θ(n)", "Θ(n log n)", "Θ(n²)", "Θ(1)"], 0, "Already sorted input: one comparison per element."),
    ("h", 2, "s", "Randomised quicksort has expected running time", ["O(n log n) on every input", "O(n²) on every input", "O(n) on every input", "O(n log n) only for random inputs"], 0, "Randomness is in the algorithm."),
])

C("ALGO", "Greedy Algorithms", "Concepts", [
    ("e", 1, "s", "Kruskal's algorithm picks edges in", ["increasing order of weight, avoiding cycles", "decreasing order of weight", "random order", "BFS order"], 0, "Uses union–find."),
    ("m", 1, "s", "Dijkstra's algorithm may fail if the graph contains", ["negative-weight edges", "cycles", "directed edges", "parallel edges"], 0, "A finalised vertex distance could later improve."),
    ("m", 2, "s", "If all edge weights are distinct, the minimum spanning tree is", ["unique", "never unique", "a shortest path tree", "a BFS tree"], 0, "Cut property."),
    ("m", 1, "s", "Huffman coding produces", ["an optimal prefix code", "a fixed-length code", "a non-prefix code", "a code with the same length for all symbols"], 0, "By merging the two least-frequent symbols repeatedly."),
    ("h", 2, "s", "The greedy strategy fails for the", ["0/1 knapsack problem", "fractional knapsack problem", "activity selection problem", "Huffman coding"], 0, "Fractional knapsack is greedy; 0/1 needs DP."),
    ("h", 2, "s", "Time complexity of Prim's algorithm with a binary heap and adjacency lists is", ["O(E log V)", "O(V²)", "O(E + V)", "O(V log E)"], 0, "Each edge may cause a decrease-key."),
    ("h", 2, "m", "Which problems have optimal greedy solutions? (select all)", ["Activity selection", "Fractional knapsack", "Minimum spanning tree", "0/1 knapsack"], [0, 1, 2], "0/1 knapsack requires dynamic programming."),
])

C("ALGO", "Dynamic Programming", "Concepts", [
    ("e", 1, "s", "Dynamic programming is applicable when a problem has", ["optimal substructure and overlapping subproblems", "only independent subproblems", "no recursive structure", "a greedy choice property only"], 0, "Divide and conquer has non-overlapping subproblems."),
    ("m", 1, "s", "The time complexity of the standard LCS algorithm for strings of lengths m and n is", ["O(mn)", "O(m + n)", "O(2^m)", "O(m log n)"], 0, "Table with (m+1)(n+1) entries."),
    ("m", 2, "s", "The 0/1 knapsack DP with n items and capacity W runs in", ["O(nW), which is pseudo-polynomial", "O(n log W), polynomial", "O(2^n)", "O(W²)"], 0, "Exponential in the number of bits of W."),
    ("m", 1, "s", "Floyd–Warshall computes", ["all-pairs shortest paths in O(V³)", "single-source shortest paths in O(V)", "MST in O(V³)", "max flow"], 0, "Works with negative edges but no negative cycles."),
    ("h", 2, "s", "Matrix-chain multiplication DP has time complexity", ["O(n³)", "O(n²)", "O(n log n)", "O(2^n)"], 0, "Three nested loops."),
    ("h", 2, "s", "Bellman–Ford can", ["detect negative-weight cycles reachable from the source", "not handle negative edges", "run in O(V)", "find MSTs"], 0, "A V-th relaxation round that still improves a distance signals a negative cycle."),
])

C("ALGO", "Graph Algorithms", "Concepts", [
    ("e", 1, "s", "BFS finds shortest paths (fewest edges) in", ["unweighted graphs", "graphs with negative weights", "only DAGs", "only trees"], 0, "Layer-by-layer exploration."),
    ("m", 1, "s", "A topological ordering exists for a directed graph iff it is", ["a DAG", "strongly connected", "a tree", "bipartite"], 0, "Cycles prevent any linear order."),
    ("m", 2, "s", "In a DFS of an undirected graph, every non-tree edge is a", ["back edge", "cross edge", "forward edge", "tree edge"], 0, "There are no cross edges in undirected DFS."),
    ("m", 1, "s", "Kosaraju's algorithm finds", ["strongly connected components in O(V + E)", "minimum spanning trees", "shortest paths with negative weights", "maximum flow"], 0, "Two DFS passes (on G and on Gᵀ)."),
    ("h", 2, "s", "A vertex whose removal increases the number of connected components is called", ["an articulation point (cut vertex)", "a bridge", "a leaf", "a centre"], 0, "A bridge is the corresponding edge notion."),
    ("h", 2, "s", "Dijkstra's algorithm with a Fibonacci heap runs in", ["O(E + V log V)", "O(V²)", "O(E log E)", "O(VE)"], 0, "Decrease-key is O(1) amortised."),
    ("h", 2, "m", "Which of the following are TRUE for a connected undirected graph with V vertices? (select all)", ["It has at least V − 1 edges", "A spanning tree has exactly V − 1 edges", "It always contains a cycle", "BFS visits all vertices"], [0, 1, 3], "A tree is connected and has no cycle."),
])

C("ALGO", "Complexity Classes", "Concepts", [
    ("e", 1, "s", "Which of the following is known to be true?", ["P ⊆ NP", "NP ⊆ P", "P = NP", "NP ⊂ P strictly"], 0, "Any deterministic poly-time algorithm is also a nondeterministic one."),
    ("m", 1, "s", "A problem is NP-complete if it is", ["in NP and every problem in NP reduces to it in polynomial time", "in P and NP-hard", "NP-hard only", "undecidable"], 0, "Cook–Levin: SAT is NP-complete."),
    ("m", 2, "m", "Which of the following problems are NP-complete? (select all)", ["3-SAT", "Vertex cover (decision)", "2-SAT", "Hamiltonian cycle", "Shortest path in a graph"], [0, 1, 3], "2-SAT and shortest path are in P."),
    ("m", 1, "s", "If A ≤p B and B ∈ P, then", ["A ∈ P", "B ∈ NP-complete", "A is NP-complete", "P = NP"], 0, "Compose the reduction with B's algorithm."),
    ("h", 2, "s", "The halting problem is", ["NP-hard but not in NP", "NP-complete", "in P", "decidable"], 0, "It is undecidable, so it is not in NP."),
    ("h", 2, "s", "Which statement is TRUE if some NP-complete problem is solved in polynomial time?", ["P = NP", "P ≠ NP", "Every problem becomes decidable", "NP = EXPTIME"], 0, "Every NP problem reduces to it."),
    ("h", 2, "m", "Which of the following are TRUE? (select all)", ["Graph 2-colourability is in P", "Graph 3-colourability is NP-complete", "Euler circuit existence is in P", "Subset-sum is solvable in polynomial time in the input size"], [0, 1, 2], "Subset-sum is NP-complete (weakly)."),
    ("h", 2, "s", "A language L is in co-NP if", ["its complement is in NP", "it is in NP", "it is undecidable", "it is in P only"], 0, "Unsatisfiability is co-NP-complete."),
])
