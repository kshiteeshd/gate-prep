"""In-depth material for the Programming & Data Structures lessons."""
from learn import deepen

deepen("pds-c-operators-bits",
       proofs=[
           ("Why x & (x − 1) clears the lowest set bit, and the power-of-two test",
            """Write x = (prefix) 1 (zeros): the lowest set bit is followed by k zeros. Subtracting 1 turns that lowest 1 into 0 and the k zeros into ones, leaving the prefix unchanged: x − 1 = (prefix) 0 (ones). ANDing, the prefix survives and everything from the lowest 1 downwards becomes 0: x & (x − 1) = (prefix) 0 (zeros), i.e. x with its lowest set bit cleared. A positive x is a power of two exactly when it has a single set bit, i.e. when x & (x − 1) == 0. Repeating the operation until x becomes 0 counts the set bits (Kernighan's popcount) in as many steps as there are ones."""),
           ("Two's complement: −x = ~x + 1 and signed ranges",
            """In n-bit two's complement the bit pattern b has the value −bₙ₋₁2ⁿ⁻¹ + Σ bᵢ2ⁱ. Flipping every bit gives (2ⁿ − 1) − x because the all-ones pattern is 2ⁿ − 1 as an unsigned number; adding 1 gives 2ⁿ − x, which represents −x modulo 2ⁿ. So −x = ~x + 1. The range is −2ⁿ⁻¹ … 2ⁿ⁻¹ − 1 (for n = 32: −2,147,483,648 … 2,147,483,647). Negating INT_MIN gives INT_MIN again (overflow, undefined behaviour in C), and shifting a negative value right is implementation-defined (usually arithmetic)."""),
           ("Left and right shifts as multiplication and division",
            """x << k multiplies the unsigned value by 2ᵏ (modulo 2ⁿ), since each bit moves to a position of weight 2ᵏ larger. x >> k on a non-negative number equals ⌊x/2ᵏ⌋: the low k bits (the remainder) are discarded. An arithmetic right shift of a negative number rounds towards −∞ (−5 >> 1 = −3) whereas C division rounds towards zero (−5 / 2 = −2). x % 2ᵏ equals x & (2ᵏ − 1) for non-negative x."""),
       ],
       notes=[
           ("Precedence, associativity and evaluation traps",
            """Highest to lowest: postfix (`++ -- () [] . ->`), unary (`! ~ ++ -- + - * & sizeof`), `* / %`, `+ -`, shifts, relational, equality, `&`, `^`, `|`, `&&`, `||`, `?:`, assignment, comma. Remember that `==` binds tighter than `&`, so `x & 1 == 0` means `x & (1 == 0)`. Unary operators and assignment are right-associative. **Order of evaluation of operands is unspecified**, so `i = i++ + ++i` or `f(i++, i++)` is undefined behaviour; only `&&`, `||`, `?:` and the comma operator have sequence points that guarantee left-to-right evaluation with short-circuiting."""),
           ("Types, conversions and overflow",
            """Integer promotion converts `char` and `short` to `int` in expressions; in mixed signed/unsigned comparisons the signed operand is converted to unsigned (so `-1 < 1u` is false). Signed overflow is undefined, unsigned overflow wraps modulo 2ⁿ. Integer division truncates toward zero and `%` has the sign of the dividend: `-7 / 2 == -3`, `-7 % 2 == -1`. Floating-point `0.1 + 0.2 != 0.3` because of binary representation. `sizeof` is evaluated at compile time and returns `size_t`; `sizeof(char)` is 1 by definition."""),
       ])

deepen("pds-pointers-memory",
       proofs=[
           ("Array indexing is pointer arithmetic: a[i] ≡ *(a + i)",
            """For an array a with elements of type T, the expression a decays to a pointer to its first element. Pointer arithmetic is scaled by the element size: a + i points to address a + i·sizeof(T). By definition a[i] means *(a + i), so the address of element i is base + i·sizeof(T), which is exactly why indexing starts at 0 (offset zero for the first element). Because addition is commutative, `i[a]` is also valid and equal to `a[i]`. For a two-dimensional array `T a[R][C]` in row-major order the address of a[i][j] is base + (i·C + j)·sizeof(T): the i complete rows before it contribute i·C elements."""),
           ("Pointer subtraction and the difference of two pointers",
            """If p and q point into the same array, p − q is the number of **elements** between them, (address(p) − address(q))/sizeof(T), of type ptrdiff_t. Subtracting pointers into different arrays is undefined. Likewise `p++` advances by sizeof(*p) bytes. For `int *p = a; p += 3;` the address increases by 12 when sizeof(int) = 4. A pointer to an array of 5 ints advances by 20 bytes."""),
           ("Stack frame layout and why returning the address of a local is a bug",
            """Each call pushes an activation record holding the return address, saved registers, parameters and local variables. When the function returns the record is popped and its memory is reused by the next call. A pointer to a local variable therefore becomes a **dangling pointer**: it still holds the old address, but that location may be overwritten by the very next function call. Static variables and memory from `malloc` live outside the stack frame and stay valid until the program ends or `free` is called. Common faults: use after free, double free, buffer overflow, and memory leaks (losing the only pointer to an allocated block)."""),
       ],
       notes=[
           ("Reading complicated declarations",
            """Use the right–left (spiral) rule: start at the identifier, read to the right while you see `[]` or `()`, then to the left for `*`. `int *p[3]` is an array of 3 pointers to int; `int (*p)[3]` is a pointer to an array of 3 ints; `int (*f)(int)` is a pointer to a function taking int and returning int; `int *f(int)` is a function returning a pointer to int. `const int *p` cannot modify `*p`; `int * const p` cannot change `p`. Strings are null-terminated char arrays: `sizeof("abc")` is 4 while `strlen("abc")` is 3, and `char s[] = "abc"` is modifiable whereas `char *s = "abc"` points to a read-only literal."""),
           ("Structs, unions and padding",
            """A struct's members are laid out in order with **padding** so that each member is aligned to its own size and the whole struct to its largest member: `struct { char c; int i; }` occupies 8 bytes (c at 0, 3 bytes of padding, i at 4) and reordering members as `{ int i; char c; }` is still 8 because of trailing padding to a multiple of 4. A union stores all members at the same address and has the size of its largest member. Arrays of structs are contiguous; `p->x` is `(*p).x`."""),
       ])

deepen("pds-recursion",
       proofs=[
           ("Correctness of a recursive function by induction (factorial)",
            """Claim: fact(n) returns n! for all n ≥ 0 where fact(0) = 1 and fact(n) = n·fact(n − 1). Base case: fact(0) = 1 = 0!. Inductive step: assume fact(n − 1) = (n − 1)!. Then fact(n) = n·(n − 1)! = n!. The same two-step pattern (base case, then assume smaller instances are correct) proves any recursive algorithm; termination is shown by a measure (here n) that strictly decreases and is bounded below."""),
           ("Number of calls of naive Fibonacci",
            """Let C(n) be the number of calls of fib(n) = fib(n − 1) + fib(n − 2). Then C(0) = C(1) = 1 and C(n) = C(n − 1) + C(n − 2) + 1. The substitution D(n) = C(n) + 1 gives D(n) = D(n − 1) + D(n − 2), the Fibonacci recurrence, with D(0) = D(1) = 2, so C(n) = 2F(n + 1) − 1 = Θ(φⁿ). Exponential time arises because the same subproblems are recomputed; memoisation or the iterative loop makes it Θ(n) time."""),
           ("Tower of Hanoi needs 2ⁿ − 1 moves",
            """To move n disks from A to C: move the top n − 1 disks to B (T(n − 1) moves), move the largest disk (1 move), then move the n − 1 disks onto C (T(n − 1) moves): T(n) = 2T(n − 1) + 1, T(0) = 0, so T(n) = 2ⁿ − 1. Optimality: the largest disk must move at least once, and when it does the other n − 1 disks must all be on the third peg, requiring at least T(n − 1) moves before and again after."""),
       ],
       notes=[
           ("Tracing recursion and call-stack depth",
            """Draw the call tree and evaluate returns bottom-up. The maximum stack depth equals the longest chain of active calls: n for linear recursion such as sum(n) = n + sum(n − 1), log n for binary search, Θ(n) in the worst case for quick sort. **Tail recursion** (the recursive call is the last action) can be converted to a loop by a compiler. The order of printing relative to the recursive call matters: printing before the call outputs the sequence going down, printing after it outputs it coming back up (reversing the order). Mutual recursion and recursion with static or global variables need careful tracking of shared state."""),
           ("Typical GATE recursion results",
            """f(n) = f(n − 1) + f(n − 1) with f(0) = 1 returns 2ⁿ; the Ackermann function grows faster than any primitive recursive function; gcd(a, b) = gcd(b, a mod b) makes O(log min(a, b)) calls (Lamé: the worst case is consecutive Fibonacci numbers); binary-to-decimal conversion by recursion prints the remainder after the recursive call; the number of ways to climb n stairs with steps 1 and 2 is Fₙ₊₁."""),
       ])

deepen("pds-arrays-stacks-queues",
       proofs=[
           ("The number of valid stack-pop sequences of n pushes is the Catalan number Cₙ",
            """Encode a valid sequence of pushes (U) and pops (D) as a path of n up-steps and n down-steps that never goes below zero (the stack height is never negative). The number of unrestricted paths is C(2n, n). **Reflection argument:** a path that does touch height −1 can be reflected after its first visit to −1 to give a path ending at height −2, i.e. with n − 1 ups and n + 1 downs; this is a bijection between bad paths and all such paths, so there are C(2n, n − 1) bad ones. Hence the number of good paths is C(2n, n) − C(2n, n − 1) = C(2n, n)/(n + 1) = Cₙ. Also: a sequence is an output permutation of 1..n iff it avoids the pattern 'c, a, b' with a < b < c (3-1-2 pattern in this convention)."""),
           ("Circular queue: size and the full/empty ambiguity",
            """With capacity N and indices front and rear moving modulo N, the elements stored are (rear − front + N) mod N when one slot is kept unused, because front == rear would otherwise denote both an empty and a full queue. Keeping one slot free gives N − 1 usable cells; alternatively maintain a count. Enqueue: a[rear] = x; rear = (rear + 1) mod N. Dequeue: x = a[front]; front = (front + 1) mod N. All operations are O(1)."""),
           ("Implementing a queue with two stacks (amortised O(1))",
            """Push onto stack S₁; to dequeue, if S₂ is empty pop everything from S₁ onto S₂ (reversing the order) and then pop S₂. Each element is moved from S₁ to S₂ at most once, so the cost of n operations is at most 3n elementary push/pop steps: the amortised cost per operation is O(1), even though a single dequeue may cost Θ(n). A stack can be implemented with two queues, but then one of the operations costs Θ(n) per call."""),
       ],
       notes=[
           ("Applications of stacks",
            """Matching brackets; converting infix to postfix with an operator stack (output operands immediately, pop operators of higher or equal precedence before pushing the current one, right-associative operators like ^ are not popped on equal precedence); evaluating postfix by pushing operands and applying each operator to the top two; function calls and recursion; depth-first search; undo operations; next-greater-element in O(n). Queues: BFS, scheduling, buffering. Deques support insertion and deletion at both ends in O(1). A priority queue is not a queue in the FIFO sense."""),
           ("Array facts for GATE",
            """Insertion into the middle of an array is O(n) (shifting), access by index O(1). A sorted array with binary search has O(log n) search but O(n) insert. The element address formulas: 1-D base + (i − lb)·w; 2-D row-major base + ((i − r₀)·C + (j − c₀))·w; column-major base + ((j − c₀)·R + (i − r₀))·w. For a lower-triangular n × n matrix stored by rows, element (i, j) with i ≥ j is at index i(i − 1)/2 + (j − 1) (1-based). A sparse matrix with k non-zero entries is stored in O(k) in triple form."""),
       ])

deepen("pds-linked-lists",
       proofs=[
           ("Reversing a singly linked list in place is correct",
            """Maintain three pointers prev (initially NULL), cur (head) and nxt. Loop invariant: before each iteration, prev points to the reversed list of the nodes already visited and cur to the unvisited suffix. Iteration: nxt = cur->next; cur->next = prev; prev = cur; cur = nxt. It preserves the invariant: the visited node is attached in front of the reversed prefix and the suffix shrinks by one. When cur becomes NULL the whole list has been reversed and prev is the new head. Time Θ(n), extra space Θ(1)."""),
           ("Floyd's cycle detection and finding the start of the cycle",
            """Move a slow pointer one step and a fast pointer two steps. If there is no cycle the fast pointer reaches NULL. If there is a cycle, both eventually enter it; once both are inside, the gap between them changes by 1 each step (modulo the cycle length), so it reaches 0: they meet within one cycle length. **Start of the cycle:** let the tail (distance to the cycle entrance) be μ and the cycle length λ. At the meeting point the slow pointer has travelled i steps and the fast 2i, so i is a multiple of λ. Reset one pointer to the head; moving both one step at a time, they meet exactly at the entrance after μ steps, because the pointer inside the cycle has also advanced i + μ ≡ μ (mod λ) from the entrance."""),
           ("Finding the middle and deleting a node when only its pointer is known",
            """With slow/fast pointers, when the fast pointer reaches the end the slow pointer is at the middle (position ⌈n/2⌉ for odd n): fast has made n/2 double steps, so slow made n/2 single steps. To delete a node X given only a pointer to X (not the head) and X is not the last node, copy the data and next pointer from X->next into X and free the following node: the list contains the same sequence of values without ever touching the predecessor. This fails for the last node (no successor to copy)."""),
       ],
       notes=[
           ("Complexities and variants",
            """Singly linked list: insert at head O(1), insert at tail O(n) (O(1) with a tail pointer), delete a given node O(n) (needs the predecessor) but O(1) with the copy trick, search O(n), no random access. Doubly linked: delete a given node O(1), extra pointer per node, traversal both ways. Circular lists allow round-robin traversal and make the tail point to the head; a circular list with only a tail pointer gives O(1) insertion at both ends. XOR-linked lists store prev ⊕ next to save space. Memory overhead per node: the data plus one (or two) pointers."""),
           ("Typical pointer-manipulation pitfalls",
            """Always handle the empty list and the single-node list; update the head when the first node changes (pass the head by reference or return the new head); free a node only after saving its next pointer; in a loop `while (p->next)` versus `while (p)` determines whether you stop at the last node or after it. Merging two sorted lists takes Θ(m + n) and O(1) extra space; sorting a linked list is best done with merge sort Θ(n log n) since random access is unavailable."""),
       ])

deepen("pds-trees-bst-avl",
       proofs=[
           ("A binary tree of height h has at most 2^(h+1) − 1 nodes, and n nodes need height ≥ ⌊log₂ n⌋",
            """Level k of a binary tree has at most 2ᵏ nodes (each node has at most two children), so a tree of height h (levels 0..h) has at most Σ_{k=0}^{h} 2ᵏ = 2^(h+1) − 1 nodes. Solving n ≤ 2^(h+1) − 1 gives h ≥ ⌈log₂(n + 1)⌉ − 1 ≥ ⌊log₂ n⌋, so no binary tree with n nodes is shorter than ⌊log₂ n⌋. A full binary tree (every node has 0 or 2 children) with i internal nodes has i + 1 leaves: count edges — 2i = (number of nodes) − 1 = i + L − 1 gives L = i + 1."""),
           ("The minimum number of nodes of an AVL tree of height h satisfies N(h) = N(h − 1) + N(h − 2) + 1",
            """An AVL tree of height h whose size is as small as possible has a root with two subtrees whose heights differ by exactly 1 (balance factor ±1 allows the smaller subtree), each itself minimal: N(h) = 1 + N(h − 1) + N(h − 2) with N(0) = 1, N(1) = 2. Then N(h) + 1 follows the Fibonacci recurrence, so N(h) = F(h + 3) − 1 ≈ φ^(h+3)/√5 − 1, which gives N(2) = 4, N(3) = 7, N(4) = 12, N(5) = 20. Inverting, h < 1.44 log₂(n + 2), so an AVL tree with n nodes has height Θ(log n): search, insert and delete take O(log n)."""),
           ("Why in-order traversal of a BST is sorted, and deletion cases",
            """By the BST property every key in a left subtree is smaller than the root and every key in the right subtree is larger. In-order visits left subtree, root, right subtree, so by induction on the subtree size the output is sorted. **Deletion:** a leaf is simply removed; a node with one child is replaced by that child; a node with two children is replaced by its in-order successor (the minimum of the right subtree, which has no left child) or predecessor, and then that node is deleted by one of the easy cases. Insertion in sorted order gives a degenerate tree of height n − 1 (Θ(n) per operation), which is the motivation for balancing."""),
           ("Rotations restore the AVL balance and preserve BST order",
            """A single right rotation at z whose left child y is left-heavy replaces z by y, makes z the right child of y and passes y's old right subtree T to z as its left subtree. In-order is unchanged (…y T z…), so the BST property holds, and heights recompute locally: the subtrees under y and z end up with heights that differ by at most 1 again. The four cases are LL (single right), RR (single left), LR (left rotation at the child, then right rotation) and RL (mirror). An insertion needs at most one rebalancing step (one single or double rotation), a deletion up to O(log n)."""),
       ],
       notes=[
           ("Traversal facts and tree reconstruction",
            """A binary tree is uniquely determined by its in-order sequence together with either its pre-order or its post-order sequence (not by pre-order and post-order alone, except for full trees). Pre-order of a BST alone determines the tree. The number of distinct binary trees with n nodes is the Catalan number Cₙ, and the number of BSTs on n distinct keys is also Cₙ. A complete binary tree stored in an array has children of i at 2i + 1 and 2i + 2 (0-based). The number of NULL pointers in a binary tree with n nodes is n + 1."""),
           ("Properties of binary trees",
            """In any non-empty binary tree n₀ = n₂ + 1 where n₀ is the number of leaves and n₂ the number of nodes with two children (count edges: n − 1 = n₁ + 2n₂, with n = n₀ + n₁ + n₂). The height of a tree with one node is 0 in most GATE questions but some texts use 1 — read the definition. A BST search costs O(h); the average height of a random BST is O(log n). Threaded trees use the NULL pointers to store in-order predecessors/successors."""),
       ])

deepen("pds-heaps",
       proofs=[
           ("Index relations of a heap stored in an array",
            """Store a complete binary tree level by level. With 0-based indexing the node at index i has children 2i + 1 and 2i + 2 and parent ⌊(i − 1)/2⌋: level k occupies indices 2ᵏ − 1 … 2^(k+1) − 2, and the j-th node of level k (offset j) has children at offsets 2j and 2j + 1 in level k + 1, i.e. indices 2^(k+1) − 1 + 2j = 2(2ᵏ − 1 + j) + 1 and the next one. The same calculation with 1-based indices gives 2i and 2i + 1. The leaves occupy indices ⌊n/2⌋ … n − 1, so there are ⌈n/2⌉ leaves and ⌊n/2⌋ internal nodes."""),
           ("Heapify is O(n), insert and extract are O(log n)",
            """Insert: add at the end and sift up; each step swaps with the parent, at most h = ⌊log₂ n⌋ steps. Extract-max: move the last element to the root and sift down, again at most h levels (each level costs two comparisons). Building the heap bottom-up costs Σ_h (n/2ʰ⁺¹)·h = O(n) (see the heap sort proof in the algorithms lessons); building by n insertions costs Θ(n log n) in the worst case. Finding the k-th largest of n numbers with a size-k min-heap costs O(n log k)."""),
           ("Number of heaps and the position of the minimum",
            """In a max-heap the minimum is at one of the leaves, so finding it needs ⌈n/2⌉ − 1 comparisons — not O(1). The number of different max-heaps on distinct keys 1..n satisfies H(n) = C(n − 1, L) H(L) H(n − 1 − L), where L is the number of nodes in the left subtree of the complete tree shape: the root is the maximum, and any L of the other n − 1 keys can go left. For n = 3 this gives 2, for n = 4 it gives 3, for n = 5 it gives 8."""),
       ],
       notes=[
           ("Heap vs BST vs sorted array",
            """Find-max: heap O(1), BST O(h), sorted array O(1). Insert: heap O(log n), BST O(h), sorted array O(n). Search for an arbitrary key: heap O(n) (no ordering between siblings), BST O(h), sorted array O(log n). Heaps are the standard implementation of priority queues (Dijkstra, Prim, event simulation, Huffman). **Decrease-key** is O(log n) given the index. Merging two binary heaps costs O(n); binomial/Fibonacci heaps improve this."""),
           ("Typical array-heap questions",
            """Given an array, decide whether it is a max-heap by checking a[i] ≥ a[2i + 1], a[2i + 2] for every internal node. After inserting a sequence into an initially empty min-heap, write the array after each sift-up. The height of a heap with n nodes is ⌊log₂ n⌋. The second largest element of a max-heap is a child of the root, so it can be found in O(1) comparisons; the third largest is among the four nodes at depth ≤ 2 other than the root and the largest child."""),
       ])

deepen("pds-hashing",
       proofs=[
           ("Expected chain length with simple uniform hashing and the load factor",
            """Under simple uniform hashing each key is equally likely to land in any of m slots, independently of the others. With n keys stored, the expected length of any one chain is n/m = α, the **load factor**. An unsuccessful search examines the whole chain: expected cost Θ(1 + α). A successful search examines on average 1 + α/2 − α/(2n) elements (the element itself plus half of the others in the chain), also Θ(1 + α). So chained hashing gives O(1) expected time as long as α = O(1), i.e. m = Ω(n)."""),
           ("Open addressing with linear probing: clustering and the probe bound",
            """With open addressing every slot holds at most one key (α ≤ 1) and a collision follows a probe sequence h(k, 0), h(k, 1), …. Under the uniform hashing assumption the expected number of probes of an unsuccessful search is at most 1/(1 − α): each probe hits an occupied slot with probability about α, so the number of probes is geometric with success (empty slot) probability 1 − α. A successful search needs about (1/α) ln(1/(1 − α)) probes. Linear probing, h(k, i) = (h′(k) + i) mod m, suffers from primary clustering (long runs of occupied slots grow faster); quadratic probing reduces it but causes secondary clustering; double hashing h₁(k) + i·h₂(k) is closest to uniform if h₂(k) is coprime to m."""),
           ("Why deletion needs tombstones in open addressing",
            """A search stops at the first empty slot, assuming that the key would have been placed no later than that. If a deleted key's slot is simply marked empty, keys that were inserted after a collision with it become unreachable (the probe sequence now stops too early). Marking the slot as **deleted** (a tombstone) lets searches continue through it while insertions may reuse it. With many deletions the table must periodically be rehashed."""),
       ],
       notes=[
           ("Hash functions",
            """Division method h(k) = k mod m works best with m prime and not close to a power of 2 (a power of two keeps only the low-order bits of k). Multiplication method h(k) = ⌊m·(kA mod 1)⌋ with A ≈ (√5 − 1)/2 ≈ 0.618 (Knuth) is insensitive to the choice of m. A good hash function spreads keys uniformly and is cheap. Collisions are unavoidable: by the pigeonhole principle any function from a universe larger than m to m slots maps two keys to the same slot. By the birthday bound the first collision is expected after about √m insertions."""),
           ("Counting collisions in GATE problems",
            """Insert the keys in order, compute h(k), and count a collision whenever the home slot is occupied (for open addressing also list every probe). Example: keys 10, 22, 31, 4, 15, 28, 17, 88, 59 into a table of 11 slots with h(k) = k mod 11 and linear probing — the trace is exact in the lesson. With chaining, the number of slots used and the maximum chain length are asked frequently. A table with m slots and n = m keys under uniform hashing has an expected maximum chain length of Θ(log n / log log n)."""),
       ])

deepen("pds-graph-representation",
       proofs=[
           ("Space and time of the two standard representations",
            """An adjacency matrix has V² entries regardless of E, so it needs Θ(V²) space (V²/8 bytes with bits) and answers 'is (u, v) an edge?' in O(1) and 'list the neighbours of u' in Θ(V). An adjacency list stores each edge once for a directed graph and twice for an undirected one: Θ(V + E) space, edge query O(deg u), neighbour listing O(deg u). Hence adjacency lists are preferable for sparse graphs (E ≪ V²) and matrices for dense graphs or when constant-time edge lookup or matrix algebra is needed. The sum of all list lengths is E (directed) or 2E (undirected) by the handshake lemma."""),
           ("Powers of the adjacency matrix count walks",
            """Claim: the (i, j) entry of Aᵏ is the number of walks of length k from i to j. For k = 1 it is the number of edges. Induction: (Aᵏ⁺¹)ᵢⱼ = Σₘ (Aᵏ)ᵢₘ Aₘⱼ counts walks of length k from i to some intermediate vertex m followed by an edge m → j; every walk of length k + 1 decomposes uniquely this way. Consequences: trace(A³)/6 is the number of triangles in a simple undirected graph (each triangle is counted 6 times as a closed walk of length 3: 3 starting points × 2 directions), and j is reachable from i iff some Aᵏ has a positive (i, j) entry for k < V."""),
       ],
       notes=[
           ("Choosing a representation and edge counts",
            """Dense graphs (E = Θ(V²)): matrix. Sparse graphs: list. An undirected graph without self loops has at most V(V − 1)/2 edges, a directed graph without self loops V(V − 1). The matrix of an undirected graph is symmetric with zero diagonal; the incidence matrix has V rows and E columns (each column has two 1s in the undirected case). Edge-list representation is convenient for Kruskal. The in-degree of vertex j in a directed graph is the sum of column j and the out-degree is the sum of row j."""),
           ("Typical questions",
            """Total entries in the adjacency lists of an undirected graph with V vertices and E edges: 2E. Number of non-zero entries in the matrix: 2E. Time to find all neighbours of every vertex: Θ(V²) matrix, Θ(V + E) list. Time to detect whether a graph is a star in the matrix representation: O(V²) for a naive check, but a degree count of each row is enough: one row with V − 1 ones and every other row a single one. Finding a universal sink (a vertex with in-degree V − 1 and out-degree 0) can be done in O(V) probes of the matrix."""),
       ])
