"""Programming & Data Structures — part 2: linked lists, trees, heaps, hashing, graph representation."""
import itertools
import math
from collections import deque

from content import g_algo as A
from content import g_pds as P
from learn import Ex, lesson

S = "PDS"


def _reverse_list(L):
    return list(reversed(L))


def _floyd_meet(mu, lam):
    nxt = lambda i: i + 1 if i < mu + lam - 1 else mu
    s = f = 0
    t = 0
    while True:
        s, f = nxt(s), nxt(nxt(f)); t += 1
        if s == f:
            return t


def _build_bst(keys):
    t = P.BST()
    for k in keys:
        t.insert(k)
    return t.root


# ======================================================================================================
lesson(subject=S, chapter="Linear Data Structures", ch_no=3, no=2, slug="pds-linked-lists", title="Linked Lists: Singly, Doubly, Circular & Pointer Tricks",
       topic="Linked Lists", minutes=20, weight=4, widget="llist",
       widget_hint="Insert, delete and reverse nodes, then make a cycle. Watch which operations are O(1) and which must walk the list.",
       key="A linked list stores each element in a node with a pointer to the next one: insertion and deletion at a known node are O(1), but reaching the k-th element costs O(k). Reversal, middle-finding and cycle detection (Floyd) are the classic pointer manipulations.",
       analogy=("🚂", "A train of coupled carriages", "Each carriage is only connected to the next one. To reach carriage 7 you must walk through carriages 1 to 6 — no instant jump (unlike an array). But adding a carriage in the middle just means uncoupling and re-coupling two links: you never have to shift the whole train."),
       sections=[
           dict(h="Node structure and variants", md="""    struct Node { int data; struct Node *next; };

- **Singly linked:** `next` only; traversal one way. **Doubly linked:** also `prev` — can walk backwards and delete a node given just a pointer to it.
- **Circular:** the last node points back to the first (useful for round-robin scheduling). A **dummy/sentinel head node** removes special cases for the empty list.
- A list is accessed through its **head** pointer (and often a **tail** pointer). The last node's `next` is NULL.

Compared with arrays: no wasted capacity and cheap insert/delete, but **no random access**, extra memory for pointers (a pointer per node), and poor cache locality."""),
           dict(h="Operation costs", md="""| Operation | Singly linked (head only) | Singly + tail pointer | Doubly linked |
|---|---|---|---|
| Insert at head | **O(1)** | O(1) | O(1) |
| Insert at tail | O(n) | **O(1)** | O(1) |
| Delete head | O(1) | O(1) | O(1) |
| Delete tail | **O(n)** (need the second-last node) | O(n) | **O(1)** |
| Delete a given node (pointer known) | O(n) (find predecessor) | O(n) | **O(1)** |
| Search / access k-th | O(n) | O(n) | O(n) |

*Trick:* to delete a node `p` in a singly linked list when only `p` is known (and it is not the tail), copy the next node's data into `p` and unlink the next node — O(1)."""),
           dict(h="Reversing a list", md="""Iterative reversal with three pointers:

    prev = NULL; cur = head;
    while (cur) { next = cur->next; cur->next = prev; prev = cur; cur = next; }
    head = prev;

O(n) time, **O(1)** extra space; every node's `next` is rewritten (n pointer changes). The recursive version uses O(n) stack. Related: reversing in groups of k, and printing a list backwards by recursion."""),
           dict(h="Fast and slow pointers (Floyd's algorithm)", md="""Move `slow` one step and `fast` two steps at a time.

- **Middle node:** when `fast` reaches the end, `slow` is at the middle.
- **Cycle detection:** if there is a cycle, `fast` eventually meets `slow` inside it; otherwise `fast` reaches NULL. O(n) time, **O(1)** space (vs. O(n) with a hash set).
- If the list has μ nodes before the cycle and the cycle has λ nodes, they first meet after at most about μ + λ steps; restarting one pointer from the head and moving both at the same speed makes them meet at the **cycle's start**.
- Other classics: merge two sorted lists O(m + n), find the k-th node from the end with two pointers k apart, detect a palindrome list."""),
       ],
       examples=[
           Ex("Reverse a list", "After reversing the singly linked list 3 → 8 → 1 → 5, what does it look like and how many next-pointers are changed?",
              ["The nodes' links flip: 5 → 1 → 8 → 3 (new head is 5).", "Every one of the 4 nodes gets a new `next` (the old head's next becomes NULL), so **4** pointer changes, O(n) time, O(1) space."],
              "5 → 1 → 8 → 3, with **4** pointer changes.", verify=lambda: " → ".join(map(str, _reverse_list([3, 8, 1, 5]))) + ", with 4 pointer changes"),
           Ex("Where do slow and fast meet?", "A list has μ = 3 nodes before a cycle and the cycle has λ = 4 nodes. Floyd's `slow`/`fast` both start at the head. After how many iterations do they first meet?",
              ["Number the nodes 0–6; node 6 links back to node 3 (μ = 3 nodes before the cycle, cycle of 4: nodes 3, 4, 5, 6). Each iteration slow moves 1 step and fast moves 2.", "Iteration 1: slow = 1, fast = 2. Iteration 2: slow = 2, fast = 4. Iteration 3: slow = 3, fast = 6 (it wraps 6 → 3 on its next step).", "Iteration 4: slow = 4, fast = 6 → 3 → 4. They meet at node 4 after **4** iterations."],
              "**4** iterations.", verify=lambda: str(_floyd_meet(3, 4))),
           Ex("Delete a node given only its pointer", "You are given a pointer p to a node (not the tail) of a singly linked list but not to the head. How can you delete it in O(1)?",
              ["Copy the data of `p->next` into `p`.", "Set `p->next = p->next->next` (and free the skipped node).", "The list looks as if `p` was removed — O(1) time, no predecessor needed."],
              "Copy the next node's data into p and unlink the next node — **O(1)**."),
       ],
       traps=[("Deleting the tail of a singly linked list", "You need the second-last node, so it is O(n) even with a tail pointer."),
              ("Forgetting the head update", "Inserting or deleting at the head changes the head pointer itself — pass the address of the head pointer, or return the new head."),
              ("Array vs list access", "k-th element is O(1) in an array but O(k) in a linked list."),
              ("Memory leak", "Each unlinked node must be freed explicitly in C.")],
       quick=[("Insertion at the head of a singly linked list takes", ["O(1)", "O(log n)", "O(n)", "O(n²)"], 0, "Two pointer updates."),
              ("Floyd's cycle detection uses", ["O(n) extra space", "O(1) extra space", "O(log n) extra space", "a stack"], 1, "Two pointers only."),
              ("In a doubly linked list, deleting a node given a pointer to it takes", ["O(1)", "O(n)", "O(log n)", "O(√n)"], 0, "prev and next are both available."),
              ("To reverse a singly linked list of n nodes in place you change", ["1 pointer", "n pointers", "n² pointers", "log n pointers"], 1, "Every next pointer.")],
       summary=["Node = data + next (+ prev); head (and tail) pointers; circular and sentinel variants.", "O(1): insert head, delete head, insert tail with tail pointer, delete given node in a doubly linked list; O(n): search, delete tail (singly).", "Reverse: prev/cur/next, O(n) time O(1) space.",
                "Floyd: slow 1, fast 2 — middle node and cycle detection in O(1) space.", "No random access: k-th element is O(k).", "Delete a middle node with only its pointer: copy next's data, unlink next."])


# ======================================================================================================
lesson(subject=S, chapter="Binary Trees, BST & AVL", ch_no=4, no=1, slug="pds-trees-bst-avl", title="Trees, BST and AVL at a glance (chapter overview)",
       topic="Trees & BST", minutes=26, weight=5, widget="bst",
       widget_hint="Insert keys in the given order and watch the shape. Tick AVL to see the tree rebalance and count rotations — try sorted input like 10 20 30 40 50 both ways.",
       key="A binary tree node has at most two children. In-order traversal of a binary search tree gives sorted keys; a BST is only fast (O(log n)) if it stays balanced — AVL trees guarantee it with rotations.",
       analogy=("📖", "A phone-book search", "Open the book in the middle: is the name before or after? You throw away half the book each time. A BST is that idea as a data structure — every node splits the remaining keys into ‘smaller’ and ‘larger’. If the data is already sorted and you insert it one by one, the tree degenerates into a list and the speed-up vanishes — hence balanced trees."),
       sections=[
           dict(h="Terminology and counting facts", md="""- **Root, parent, child, leaf, internal node.** The **depth** of a node = edges from the root; the **height** of a tree = edges on the longest root-to-leaf path (a single node has height 0; empty tree −1).
- **Full** binary tree: every node has 0 or 2 children ⇒ leaves = internal nodes + 1. **Complete:** all levels full except possibly the last, filled left to right (heaps). **Perfect:** all leaves at the same depth, 2ʰ⁺¹ − 1 nodes.
- A binary tree of height h has **at most 2ʰ⁺¹ − 1** nodes; with n nodes its height is at least ⌊log₂ n⌋ and at most n − 1.
- A binary tree with n nodes has **n + 1 NULL pointers**; there are Cₙ = C(2n, n)/(n+1) distinct binary tree shapes (Catalan)."""),
           dict(h="Traversals", md="""| Order | Visit | Used for |
|---|---|---|
| **Pre-order** | root, left, right | copying a tree, prefix expressions |
| **In-order** | left, root, right | **sorted output of a BST** |
| **Post-order** | left, right, root | deleting a tree, postfix expressions |
| **Level-order** | level by level (queue) | BFS |

All depth-first traversals take **O(n)** time. **Reconstruction:** a tree is determined uniquely by in-order together with pre-order *or* post-order (or level-order) — but **pre-order + post-order alone is ambiguous** unless the tree is full. In pre-order the root comes first; find it in the in-order list to split left and right subtrees."""),
           dict(h="Binary search trees", md="""**BST property:** for every node, all keys in the left subtree are smaller and all in the right subtree are larger.

- **Search / insert:** compare and go left or right — O(h), where h is the height: **O(log n) if balanced, O(n) in the worst case** (sorted insertion order gives a chain).
- **Delete:** a leaf is simply removed; a node with one child is replaced by it; a node with two children is replaced by its **in-order successor** (leftmost node of the right subtree) or predecessor, which is then deleted.
- **Minimum** = leftmost node, **maximum** = rightmost. The **in-order successor** of a node with a right child is the minimum of that right subtree.
- The number of distinct BSTs with n keys is the Catalan number Cₙ (5 for n = 3, 14 for n = 4).""",
                call=[("trap", "Order matters for the shape", "The same set of keys inserted in a different order gives a different BST. The first key inserted is always the root.")]),
           dict(h="AVL trees and rotations", md="""An **AVL tree** is a BST in which the **balance factor** (height of left subtree − height of right subtree) of every node is −1, 0 or +1. This keeps the height **O(log n)** (at most about 1.44·log₂ n), so search, insert and delete are O(log n).

After an insertion, find the lowest unbalanced node z and fix it with rotations:

| Case | Insertion location | Fix |
|---|---|---|
| **LL** | into the left subtree of z's left child | one **right** rotation at z |
| **RR** | into the right subtree of z's right child | one **left** rotation at z |
| **LR** | into the right subtree of z's left child | left rotation at the child, then right at z (**double**) |
| **RL** | into the left subtree of z's right child | right rotation at the child, then left at z (**double**) |

Insertion needs **at most one rebalancing step** (a single or a double rotation); deletion may need O(log n). The minimum number of nodes N(h) in an AVL tree of height h satisfies **N(h) = N(h−1) + N(h−2) + 1** (1, 2, 4, 7, 12, 20, 33, …). Red–black trees give height ≤ 2·log₂(n + 1) with fewer rotations."""),
       ],
       examples=[
           Ex("Traversals of a BST", "Insert the keys 50, 30, 70, 20, 40, 60, 80, 10 into an empty BST. Give the pre-order and the height.",
              ["Root 50; 30 and 70 are its children; 20 and 40 under 30; 60 and 80 under 70; 10 under 20.", "Pre-order (root, left, right): 50, 30, 20, 10, 40, 70, 60, 80.", "Longest path 50–30–20–10 has 3 edges: height **3**."],
              "Pre-order **50 30 20 10 40 70 60 80**, height **3**.", verify=lambda: "Pre-order %s, height %d" % (" ".join(map(str, P.preorder(_build_bst([50, 30, 70, 20, 40, 60, 80, 10])))), P.height(_build_bst([50, 30, 70, 20, 40, 60, 80, 10])))),
           Ex("Reconstruct from pre-order and in-order", "Pre-order = 1 2 4 5 3 and in-order = 4 2 5 1 3. What is the post-order?",
              ["Pre-order's first element 1 is the root. In in-order, 4 2 5 are left of 1 and 3 is right.", "Left subtree: pre 2 4 5, in 4 2 5 ⇒ root 2 with children 4 and 5. Right subtree: just 3.", "Post-order (left, right, root): 4 5 2 3 1."],
              "**4 5 2 3 1**", verify=lambda: " ".join(map(str, P.postorder(P.rebuild([1, 2, 4, 5, 3], [4, 2, 5, 1, 3]))))),
           Ex("AVL rotations", "Keys 10, 20, 30, 40, 50 are inserted in this order into an empty AVL tree. How many rotations occur (a double rotation counts as 2) and what is the final height?",
              ["Insert 10, 20 fine; 30 makes the root unbalanced (RR): left rotation — 1 rotation.", "Insert 40: fine. Insert 50: the node 30 is unbalanced (RR): left rotation — 2 rotations.", "Final tree: root 20, left 10, right 40 (children 30, 50): height **2**."],
              "**2** rotations, height **2**.", verify=lambda: "%d rotations, height %d" % P.avl_insert_rotations([10, 20, 30, 40, 50])),
           Ex("Maximum nodes", "What is the maximum number of nodes in a binary tree of height 5 (single node = height 0)?",
              ["The tree is largest when every level is full: level k holds 2ᵏ nodes, for k = 0 … 5.", "Total = 2⁰ + … + 2⁵ = 2⁶ − 1 = **63**."],
              "**63**", verify=lambda: str(2 ** 6 - 1)),
           Ex("Minimum nodes in an AVL tree", "What is the minimum number of nodes in an AVL tree of height 4?",
              ["N(0) = 1, N(1) = 2, then N(h) = N(h−1) + N(h−2) + 1.", "N(2) = 4, N(3) = 7, N(4) = 7 + 4 + 1 = **12**."],
              "**12**", verify=lambda: str((lambda N: N(N, 4))(lambda N, h: 1 if h == 0 else 2 if h == 1 else N(N, h - 1) + N(N, h - 2) + 1))),
       ],
       traps=[("Height conventions", "Check whether a single node has height 0 (edges) or 1 (nodes); GATE usually says."),
              ("In-order and sorting", "In-order gives sorted keys **only for a BST**."),
              ("Pre + post-order ambiguity", "Pre-order with post-order does not determine the tree uniquely (unless it is full)."),
              ("AVL double rotation counting", "A double rotation is two single rotations — read whether the question counts it as 1 or 2.")],
       quick=[("An in-order traversal of a BST visits keys in", ["random order", "descending order", "ascending order", "level order"], 2, "Left, root, right."),
              ("A binary tree with 15 nodes has how many NULL pointers?", ["14", "15", "16", "30"], 2, "n + 1 = 16."),
              ("Sorted keys inserted one by one into an ordinary BST give a tree of height", ["log n", "n/2", "n − 1", "1"], 2, "A chain."),
              ("Which traversal pair does NOT uniquely determine a binary tree?", ["in-order + pre-order", "in-order + post-order", "pre-order + post-order", "in-order + level-order"], 2, "Ambiguous unless full.")],
       summary=["Height of one node = 0; max nodes in height h = 2ʰ⁺¹ − 1; n nodes ⇒ n + 1 NULL pointers; full tree: leaves = internal + 1.", "Pre: root-L-R; In: L-root-R (sorted for BST); Post: L-R-root; level-order uses a queue.",
                "BST ops O(h): balanced log n, skewed n; delete uses the in-order successor; Cₙ shapes with n nodes.", "AVL: |balance factor| ≤ 1; LL/RR single rotation, LR/RL double; one fix per insertion; N(h) = N(h−1) + N(h−2) + 1.", "In-order + pre/post-order reconstructs uniquely; pre + post does not.", "First inserted key is the root."])


# ======================================================================================================
lesson(subject=S, chapter="Heaps & Hashing", ch_no=5, no=1, slug="pds-heaps", title="Binary Heaps, Priority Queues & Heap Sort",
       topic="Heaps & Hashing", minutes=20, weight=4, widget="heap",
       widget_hint="Insert and extract values and watch the array and the tree stay in sync. Use ‘Build from list’ to see Floyd's bottom-up construction and its swap count.",
       key="A binary heap is a complete binary tree stored in an array where every parent is ≤ (min-heap) or ≥ (max-heap) its children. Insert and extract-root cost O(log n); building a heap from n items costs only O(n); heap sort is O(n log n) in place.",
       analogy=("🏆", "A knock-out tournament bracket", "In a max-heap the strongest player sits at the top. When the champion leaves, the last player is moved to the top and then ‘sinks’ by repeatedly swapping with the stronger child until the bracket is valid again. Only one root-to-leaf path is touched — so it costs log n, not n."),
       sections=[
           dict(h="Structure and array layout", md="""A heap is a **complete binary tree** (all levels full except the last, which fills left to right) with the **heap-order property**. Because it is complete, it is stored in an array with no pointers. For 0-indexed position i:

- left child **2i + 1**, right child **2i + 2**, parent **⌊(i − 1)/2⌋**.
- (1-indexed: children 2i and 2i + 1, parent ⌊i/2⌋.)
- Height = **⌊log₂ n⌋**; the leaves are the last ⌈n/2⌉ elements; the root holds the minimum (min-heap) or maximum (max-heap).
- A *d*-ary heap uses children d·i + 1 … d·i + d and parent ⌊(i − 1)/d⌋.""",
                formulas=[("children of i:  2i+1, 2i+2     parent:  ⌊(i−1)/2⌋", "0-indexed array")]),
           dict(h="Insert, extract and build", md="""- **Insert:** append at the end, then **sift up** (swap with the parent while out of order). O(log n).
- **Extract-min/max:** take the root, move the **last** element to the root, then **sift down** (swap with the better child). O(log n).
- **Peek:** O(1). **Delete an arbitrary element** given its index: O(log n). **Search** for a value: O(n) — a heap is not a search structure.
- **Build-heap (Floyd):** call sift-down on every internal node from ⌊n/2⌋ − 1 down to 0. Total cost **O(n)** (not n log n) because most nodes are near the leaves. Repeated insertion would cost O(n log n).
- The **maximum of a min-heap** is in one of the leaves — finding it takes Θ(n) (about n/2 candidates)."""),
           dict(h="Heap sort and priority queues", md="""**Heap sort:** build a max-heap in O(n); then n − 1 times swap the root with the last unsorted element, shrink the heap and sift down. **O(n log n)** in every case, **in place** (O(1) extra space), **not stable**.

A **priority queue** supports insert and extract-highest-priority; a binary heap implements both in O(log n). Applications: Dijkstra and Prim, Huffman coding, event simulation, k-largest elements (a min-heap of size k gives the answer in O(n log k)), merging k sorted lists.

| Structure | Insert | Extract-min | Find-min |
|---|---|---|---|
| Binary heap | O(log n) | O(log n) | O(1) |
| Unsorted array | O(1) | O(n) | O(n) |
| Sorted array | O(n) | O(1) | O(1) |
| Balanced BST | O(log n) | O(log n) | O(log n) |"""),
       ],
       examples=[
           Ex("Build a max-heap", "Apply Floyd's bottom-up build-heap (max-heap) to [9, 4, 7, 1, 8, 2, 6]. What is the final array and how many swaps are needed?",
              ["Internal nodes are indices 2, 1, 0. Sift down index 2 (7): children 2, 6 → no swap. Index 1 (4): children 1, 8 → swap with 8 → [9, 8, 7, 1, 4, 2, 6].", "Index 0 (9): children 8 and 7 → already larger, no swap.", "Final array [9, 8, 7, 1, 4, 2, 6] with **1** swap."],
              "[9, 8, 7, 1, 4, 2, 6] with **1** swap.", verify=lambda: "%s with %d swap" % A.build_heap([9, 4, 7, 1, 8, 2, 6])),
           Ex("Min-heap insertions", "Insert 5, 3, 8, 1, 9, 2 one at a time into an empty min-heap (sift-up). What is the final array?",
              ["After 5: [5]. After 3: [3, 5]. After 8: [3, 5, 8]. After 1: [1, 3, 8, 5].", "After 9: [1, 3, 8, 5, 9]. After 2: appended at index 5, parent index 2 (8 > 2) → swap → [1, 3, 2, 5, 9, 8]."],
              "[1, 3, 2, 5, 9, 8]", verify=lambda: str(__import__("functools").reduce(_hins, [5, 3, 8, 1, 9, 2], []))),
           Ex("Parent and child indices", "In a 0-indexed binary max-heap array, what are the indices of the parent and children of the element at index 11?",
              ["Parent = ⌊(11 − 1)/2⌋ = 5.", "Children = 2·11 + 1 = 23 and 2·11 + 2 = 24."],
              "Parent **5**; children **23** and **24**.", verify=lambda: "Parent %d; children %d and %d" % ((11 - 1) // 2, 2 * 11 + 1, 2 * 11 + 2)),
           Ex("Height and leaves", "A binary heap has 100 elements. What is its height and how many leaves does it have?",
              ["Height = ⌊log₂ 100⌋ = 6 (since 2⁶ = 64 ≤ 100 < 128).", "Leaves = n − ⌊n/2⌋ = 100 − 50 = **50**."],
              "Height **6**, **50** leaves.", verify=lambda: "Height %d, %d leaves" % (math.floor(math.log2(100)), 100 - 100 // 2)),
       ],
       traps=[("Build-heap complexity", "Floyd's method is **O(n)**; n successive inserts is O(n log n)."),
              ("Heap is not sorted", "Only parent-child order is guaranteed — siblings and cousins are unordered; an array in heap order is not sorted."),
              ("Index conventions", "0-indexed: 2i+1, 2i+2, ⌊(i−1)/2⌋; 1-indexed: 2i, 2i+1, ⌊i/2⌋. Check which one the question uses."),
              ("Searching a heap", "Finding an arbitrary key is O(n); only the root is cheap to find.")],
       quick=[("Building a heap from n unsorted elements with Floyd's method takes", ["O(n)", "O(n log n)", "O(log n)", "O(n²)"], 0, "Most nodes sit near the leaves."),
              ("Extract-min from a binary heap costs", ["O(1)", "O(log n)", "O(n)", "O(n log n)"], 1, "Sift down one path."),
              ("The maximum element of a min-heap is always at", ["the root", "the last index", "one of the leaves", "the middle"], 2, "It has no children, so it is a leaf."),
              ("Heap sort is", ["stable and in place", "unstable and in place", "stable, not in place", "unstable, not in place"], 1, "In place but long-distance swaps break stability.")],
       summary=["Complete binary tree in an array: children 2i+1, 2i+2, parent ⌊(i−1)/2⌋; height ⌊log₂ n⌋.", "Insert (sift up) and extract (move last to root, sift down) are O(log n); peek is O(1).", "Floyd build-heap is O(n); heap sort O(n log n), in place, not stable.",
                "Priority queue = heap; used by Dijkstra, Prim, Huffman, k-largest.", "Heap order only constrains parent vs child; search is O(n).", "Max of a min-heap lies in a leaf."])


def _hins(a, k):
    a = a + [k]
    i = len(a) - 1
    while i > 0 and a[(i - 1) // 2] > a[i]:
        a[(i - 1) // 2], a[i] = a[i], a[(i - 1) // 2]
        i = (i - 1) // 2
    return a


# ======================================================================================================
def _chains(keys, m):
    ch = [[] for _ in range(m)]
    for k in keys:
        ch[k % m].append(k)
    return ch


lesson(subject=S, chapter="Heaps & Hashing", ch_no=5, no=2, slug="pds-hashing", title="Hashing: Hash Functions, Chaining & Open Addressing",
       topic="Heaps & Hashing", minutes=20, weight=4, widget="hash",
       widget_hint="Enter keys and a table size, then switch between linear probing, quadratic probing, double hashing and chaining to compare collisions and the final layout.",
       key="A hash table maps a key to an array slot with a hash function, giving O(1) expected search, insert and delete. Collisions are resolved by chaining (a list per slot) or open addressing (probe for another slot); the load factor α = n/m controls performance.",
       analogy=("🗄️", "A filing cabinet with labelled drawers", "Instead of reading every file, you compute which drawer a name belongs in (say, from the first letter) and go straight there. Trouble starts when two names map to the same drawer — a collision. You either keep a small pile inside the drawer (chaining) or put the file in the next free drawer (probing)."),
       sections=[
           dict(h="Hash functions and the load factor", md="""A **hash function** h(k) maps a key to an index 0..m − 1. A good one is fast and spreads keys **uniformly**. Common choices: **division** h(k) = k mod m (pick m prime, not a power of 2), **multiplication** ⌊m·frac(k·A)⌋ with A ≈ 0.618, and string hashes combining characters.

The **load factor α = n / m** (stored keys ÷ table size). Under *simple uniform hashing* the expected cost of a search is Θ(1 + α) for chaining. Keep α below about 0.7 (open addressing) and **rehash** into a larger table when it grows too high.""",
                formulas=[("load factor  α = n / m", ""), ("chaining: unsuccessful search ≈ 1 + α, successful ≈ 1 + α/2", "expected probes")]),
           dict(h="Collision resolution: chaining", md="""**Separate chaining:** each slot holds a linked list of the keys that hash to it. Insert at the head is O(1); search is O(1 + chain length). Works for any α (even α > 1) and deletion is easy. The table can use extra memory for the lists. Worst case, every key lands in one chain: search is O(n).

Facts: the longest chain is the worst-case search cost; the number of **empty slots** shows how uneven the hash is."""),
           dict(h="Collision resolution: open addressing", md="""All keys live **in the table itself** (so α ≤ 1). On a collision, probe a sequence of slots h(k, 0), h(k, 1), …:

| Method | Probe sequence h(k, i) | Problem |
|---|---|---|
| **Linear probing** | (h(k) + i) mod m | **primary clustering** — long runs of occupied slots |
| **Quadratic probing** | (h(k) + c₁i + c₂i²) mod m | secondary clustering; may not visit every slot |
| **Double hashing** | (h₁(k) + i·h₂(k)) mod m | best; h₂(k) must be coprime to m |

**Deletion** needs care: simply emptying a slot would break probe chains, so use a **tombstone** marker. Search stops at an empty slot (never at a tombstone). Expected probes for an unsuccessful search ≈ 1/(1 − α) under uniform probing.""",
                call=[("trap", "Table full", "With open addressing you cannot insert more than m keys, and probing can fail to find a free slot even when one exists if the probe sequence does not cover the table.")]),
           dict(h="Comparison", md="""| | Chaining | Open addressing |
|---|---|---|
| Memory | pointers + lists | only the table |
| α can exceed 1? | yes | **no** (α ≤ 1) |
| Deletion | easy | needs tombstones |
| Cache behaviour | poor (pointer chasing) | good (contiguous) |
| Clustering | none | yes (linear/quadratic) |
| Worst-case search | O(n) | O(n) |

Perfect hashing gives O(1) worst-case search for a static key set. Hash tables do **not** support ordered operations (min, range queries) efficiently — use a balanced BST for those."""),
       ],
       examples=[
           Ex("Linear probing", "Keys 12, 25, 38, 51, 64, 9, 22 are inserted in this order into a table of size 11 with h(k) = k mod 11 and linear probing. How many collisions (occupied slots probed) occur?",
              ["12 → slot 1; 25 → 3; 38 → 5; 51 → 7; 64 → 9 (all free).", "9 → slot 9 is taken by 64 → probe 10: 1 collision. 22 → slot 0 is free.", "Total collisions = **1**."],
              "**1** collision.", verify=lambda: str(A.hash_insert([12, 25, 38, 51, 64, 9, 22], 11, lambda k, i, m: (k + i) % m)[1])),
           Ex("Longest chain", "With chaining, h(k) = k mod 7, the keys 15, 22, 29, 36, 8, 14 are inserted. What is the length of the longest chain?",
              ["15, 22, 29, 36, 8 all ≡ 1 (mod 7); 14 ≡ 0.", "Slot 1 holds five keys → longest chain **5**."],
              "**5**", verify=lambda: str(max(map(len, _chains([15, 22, 29, 36, 8, 14], 7))))),
           Ex("Load factor", "A chained hash table with 100 slots stores 250 keys. What is the load factor and the expected length of a chain?",
              ["α = n/m = 250/100 = **2.5**.", "Under uniform hashing the average chain length equals α = 2.5."],
              "α = **2.5**.", verify=lambda: str(250 / 100)),
           Ex("Total collisions", "Keys 10, 22, 31, 4, 15, 28, 17, 88, 59 are inserted in this order into a table of size 11 with h(k) = k mod 11 and linear probing. How many collisions (occupied slots probed) occur in total?",
              ["10 → slot 10; 22 → slot 0; 31 → slot 9; 4 → slot 4 (all free).", "15 → slot 4 is taken, so probe slot 5: 1 collision. 28 → slot 6 (free).", "17 → slot 6 is taken, probe slot 7: 1 collision. 88 → slot 0 is taken, probe slot 1: 1 collision.",
               "59 → slot 4 is taken, then 5, 6, 7 are taken, so it lands in slot 8 after 4 collisions.", "Total = 1 + 1 + 1 + 4 = **7** collisions."],
              "**7** collisions.", verify=lambda: str(A.hash_insert([10, 22, 31, 4, 15, 28, 17, 88, 59], 11, lambda k, i, m: (k + i) % m)[1])),       ],
       traps=[("Open addressing capacity", "Never more than m keys; keep α well below 1."),
              ("Deleting in open addressing", "Use a tombstone — emptying the slot breaks later searches."),
              ("Worst case", "O(1) is the *expected* cost; a bad hash or adversarial keys give O(n)."),
              ("Choosing m", "A power of two with division hashing uses only the low bits of the key — prefer a prime.")],
       quick=[("A hash table has 50 slots and 100 keys with chaining. α =", ["0.5", "1", "2", "50"], 2, "n/m."),
              ("Primary clustering is a problem of", ["chaining", "double hashing", "linear probing", "perfect hashing"], 2, "Long runs grow longer."),
              ("Open addressing requires the load factor to be", ["> 1", "≤ 1", "exactly 1", "irrelevant"], 1, "All keys are in the table."),
              ("Average search time in a hash table with chaining is", ["Θ(1 + α)", "Θ(log n)", "Θ(n)", "Θ(α²)"], 0, "Hash + scan the chain.")],
       summary=["h(k) = k mod m with m prime; load factor α = n/m.", "Chaining: list per slot, α may exceed 1, expected search Θ(1 + α).", "Open addressing: α ≤ 1; linear (primary clustering), quadratic, double hashing (best); deletions need tombstones.",
                "Expected O(1), worst case O(n).", "Hash tables don't support ordered queries.", "Rehash when α gets too large."])


# ======================================================================================================
def _count_edges_matrix(m):
    return sum(map(sum, m)) // 2


lesson(subject=S, chapter="Graphs", ch_no=6, no=1, slug="pds-graph-representation", title="Graph Representation: Adjacency Matrix, Adjacency List & Edge List",
       topic="Graph Representation", minutes=16, weight=3, widget="traverse",
       widget_hint="Enter the same graph and run BFS or DFS: the traversal result does not depend on representation — only the cost of finding neighbours does.",
       key="A graph can be stored as an adjacency matrix (O(V²) space, O(1) edge lookup) or adjacency lists (O(V + E) space, fast neighbour iteration). Choose the matrix for dense graphs, lists for sparse ones — and remember how this changes BFS/DFS cost.",
       analogy=("🚇", "A metro map: table vs. station signs", "An adjacency matrix is the big grid in the ticket office that says for every pair of stations whether a direct line exists — a lot of mostly empty boxes. Adjacency lists are the signs on each platform: just the stations you can reach directly. For a sparse network the signs are far smaller."),
       sections=[
           dict(h="Adjacency matrix", md="""A V × V matrix A with A[i][j] = 1 (or the weight) if there is an edge from i to j.

- **Space:** Θ(V²), regardless of the number of edges.
- **Edge lookup** (is (u, v) an edge?): **O(1)**. **Neighbours of u:** scan a row — **O(V)**. **Add/remove an edge:** O(1).
- An undirected graph's matrix is **symmetric** (A = Aᵀ), with 2E ones; a simple graph has zeros on the diagonal. Row sum = out-degree, column sum = in-degree.
- Matrix powers count walks: (Aᵏ)[i][j] is the number of walks of length k from i to j; the **transitive closure** can be computed by Warshall's algorithm in O(V³)."""),
           dict(h="Adjacency list and edge list", md="""**Adjacency list:** an array of V lists; list u contains the neighbours of u.

- **Space:** Θ(V + E) — an undirected edge appears twice (2E entries).
- **Neighbours of u:** O(deg(u)). **Edge lookup:** O(deg(u)) (or O(1) expected with hash sets). **Add edge:** O(1).
- **In-degree** of v in a directed graph requires scanning all lists (O(V + E)) unless you also store the reverse graph.

**Edge list:** just a list of (u, v, w) triples — Θ(E) space, ideal for Kruskal (sort by weight); poor for neighbour queries. **Incidence matrix:** V × E, rarely used."""),
           dict(h="Choosing a representation", md="""| | Adjacency matrix | Adjacency list |
|---|---|---|
| Space | Θ(V²) | Θ(V + E) |
| Edge (u,v)? | **O(1)** | O(deg u) |
| List neighbours of u | O(V) | **O(deg u)** |
| BFS / DFS | **O(V²)** | **O(V + E)** |
| Best for | dense graphs (E ≈ V²), edge queries | sparse graphs (E ≈ V) |

A graph is **sparse** when E = O(V), **dense** when E = Θ(V²). A simple undirected graph has at most V(V−1)/2 edges; a simple directed graph at most V(V−1). The transpose Gᵀ (all edges reversed) is the transposed matrix, or built from the lists in O(V + E)."""),
       ],
       examples=[
           Ex("Number of edges from a matrix", "The adjacency matrix of a simple undirected graph is [[0,1,1,0],[1,0,1,1],[1,1,0,0],[0,1,0,0]]. How many edges does it have?",
              ["Sum of all entries = 2 + 3 + 2 + 1 = 8.", "Each undirected edge is counted twice, so E = 8/2 = **4**."],
              "**4**", verify=lambda: str(_count_edges_matrix([[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [0, 1, 0, 0]]))),
           Ex("List entries", "An undirected graph has 1000 vertices and 4000 edges. How many entries do its adjacency lists hold in total?",
              ["In an undirected graph an edge {u, v} is stored in u's list and in v's list.", "Entries = 2 × 4000 = **8000**."],
              "**8000**", verify=lambda: str(2 * 4000)),
           Ex("Matrix size in bytes", "A directed graph on 200 vertices is stored as an adjacency matrix using one bit per entry. How many bytes are needed?",
              ["200 × 200 = 40000 bits.", "40000 / 8 = **5000** bytes."],
              "**5000** bytes.", verify=lambda: str(200 * 200 // 8)),
           Ex("In-degree from lists", "A directed graph is stored as adjacency lists: 0: [1, 2], 1: [2], 2: [0, 3], 3: [2]. What is the in-degree of vertex 2?",
              ["Count how many lists contain 2: vertex 0, vertex 1 and vertex 3 each list it.", "In-degree = **3**."],
              "**3**", verify=lambda: str(sum(1 for l in ([1, 2], [2], [0, 3], [2]) if 2 in l))),
       ],
       traps=[("BFS/DFS with a matrix", "Finding neighbours costs O(V) per vertex, so the traversal is O(V²), not O(V + E)."),
              ("Undirected edge count", "A matrix has 2E ones and lists have 2E entries; E = sum / 2."),
              ("Dense vs sparse", "For a nearly complete graph the matrix is better; for a tree (E = V − 1) lists are far smaller."),
              ("Directed in-degree", "Lists give out-degree cheaply; in-degree needs a full scan or a reverse list.")],
       quick=[("Space of an adjacency matrix for V vertices:", ["Θ(V)", "Θ(V + E)", "Θ(V²)", "Θ(E)"], 2, "Independent of E."),
              ("Checking whether edge (u, v) exists is O(1) in", ["adjacency list", "adjacency matrix", "edge list", "both lists and matrix"], 1, "Direct indexing."),
              ("BFS on an adjacency list runs in", ["O(V)", "O(V + E)", "O(V²)", "O(E²)"], 1, "Each edge examined twice at most."),
              ("The matrix of an undirected simple graph is", ["upper triangular", "symmetric with zero diagonal", "diagonal", "the identity"], 1, "A = Aᵀ, no self-loops.")],
       summary=["Matrix: Θ(V²) space, O(1) edge lookup, O(V) neighbours; lists: Θ(V + E) space, O(deg) neighbours.", "BFS/DFS: O(V + E) with lists, O(V²) with a matrix.", "Undirected: matrix has 2E ones, lists have 2E entries.",
                "Sparse (E ≈ V) → lists; dense (E ≈ V²) → matrix; edge list suits Kruskal.", "Row sum = out-degree, column sum = in-degree; Aᵏ counts walks of length k.", "Transpose graph = reverse every edge."])
