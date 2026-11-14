"""PDS chapter 4 — Binary Trees, BST & AVL: a full chapter built from small, focused lessons."""
from content import g_pds as P
from content import g_trees as T
from learn import Ex, lesson

S = "PDS"
CH, NO = "Binary Trees, BST & AVL", 4
TOPIC = "Trees & BST"
J = lambda a: " ".join(map(str, a))


def _n(a):
    return J(a)


# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=2, slug="pds-tree-terminology", title="1 · Tree vocabulary and counting facts",
       topic=TOPIC, subs=["Tree terminology", "Tree properties"], minutes=18, weight=4, widget="none",
       key="Almost every tree question is a counting question in disguise. Learn the vocabulary (height, depth, full, complete, perfect) and five identities: nodes in a perfect tree, nodes on a level, leaves in a full tree, NULL pointers, and the count of tree shapes.",
       analogy=("🏢", "A building and its floors", "Level 0 is the ground floor with one room (the root). Every room opens into at most two rooms on the next floor. Floor k therefore holds at most 2^k rooms, and a building with h floors above ground holds at most 2^(h+1) − 1 rooms. Counting questions are asking how many rooms fit, or how few floors you need."),
       sections=[
           dict(h="Words you must be able to define", md="""- **Node, edge, root, parent, child, sibling, leaf (no children), internal node (at least one child).**
- **Depth of a node:** number of edges from the root to it (root depth 0). **Level** = depth.
- **Height of a node:** edges on the longest downward path to a leaf. **Height of a tree** = height of its root. A single node has height 0; the empty tree has height −1 (a convention, so that the formula height = 1 + max(left, right) works for leaves).
- **Degree of a node:** its number of children. A **binary tree** has degree ≤ 2 everywhere, and the children are *ordered* (left and right are different).
- **Subtree:** a node together with all its descendants.

GATE questions often say "height counted in nodes" or "in edges". Read it every time: the two conventions differ by exactly 1."""),
           dict(h="The kinds of binary tree", md="""| Kind | Definition | Consequence |
|---|---|---|
| **Full** (proper) | every node has 0 or 2 children | leaves = internal nodes + 1 |
| **Perfect** | full, and all leaves at the same depth | $2^{h+1}-1$ nodes |
| **Complete** | all levels full except possibly the last, which fills from the left | array layout, used by heaps; $\\lfloor n/2\\rfloor$ internal nodes |
| **Skewed** | every node has one child | height $n-1$, the worst case |
| **Balanced** | height $O(\\log n)$ | operations stay fast |

A perfect tree is full and complete. A complete tree need not be full (one node may have a single child on the last-but-one level). A full tree need not be complete."""),
           dict(h="Five identities and why they are true", md="""1. **Nodes on level $k$:** at most $2^k$ (each node has at most two children).
2. **Nodes in a tree of height $h$:** at most $2^{h+1}-1$ (add levels 0 to $h$: a geometric series).
3. **Minimum height with $n$ nodes:** $\\lfloor\\log_2 n\\rfloor$ (invert identity 2). Maximum height: $n-1$.
4. **NULL pointers:** a binary tree with $n$ nodes has $2n$ child pointers; exactly $n-1$ point to real nodes (every non-root node has one parent pointer), so **$n+1$** are NULL.
5. **Full tree:** edges $=2I$ (each internal node has two children) and edges $=I+L-1$ (every node but the root has one edge), hence **$L=I+1$**. For a full $k$-ary tree, $kI=I+L-1$, so $L=(k-1)I+1$.

The number of different binary-tree shapes with $n$ nodes is the **Catalan number** $C_n=\\frac1{n+1}\\binom{2n}{n}$: 1, 1, 2, 5, 14, 42, 132, 429 for $n=0,1,2,\\dots$. Choosing the root splits the other $n-1$ nodes into a left and a right part, giving $C_n=\\sum_{i}C_iC_{n-1-i}$.""",
                call=[("trap", "Pre-order + post-order", "Two different trees can share both pre-order and post-order; only for *full* trees is the pair enough.")]),
       ],
       examples=[
           Ex("Perfect tree size", "How many nodes are there in a perfect binary tree of height 6?",
              ["Level k has 2^k nodes for k = 0 … 6.", "Total = 2^0 + 2^1 + … + 2^6 = 2^7 − 1 = **127**."], "**127**", verify=lambda: str(2 ** 7 - 1)),
           Ex("Level capacity", "What is the largest number of nodes that can lie on level 9 of a binary tree (root on level 0)?",
              ["Level k can hold at most 2^k nodes.", "2^9 = **512**."], "**512**", verify=lambda: str(2 ** 9)),
           Ex("Leaves of a full tree", "A full binary tree has 37 internal nodes. How many leaves does it have, and how many nodes in total?",
              ["Leaves = internal + 1 = 38.", "Total nodes = 37 + 38 = **75** (and 74 edges = 2 × 37)."], "**38** leaves, **75** nodes.", verify=lambda: "%d leaves %d nodes" % (38, 75)),
           Ex("NULL pointers", "A binary tree has 24 nodes. How many NULL pointers does its linked representation contain?",
              ["Total child pointers = 2 × 24 = 48.", "Non-NULL pointers = 24 − 1 = 23 (one per non-root node).", "NULL = 48 − 23 = **25** = n + 1."], "**25**", verify=lambda: str(25)),
           Ex("Minimum height", "What is the minimum possible height (in edges) of a binary tree with 100 nodes?",
              ["Height h can hold at most 2^(h+1) − 1 nodes. h = 5 holds at most 63 (too few); h = 6 holds at most 127 ≥ 100.", "So the minimum is **6** = ⌊log₂ 100⌋."], "**6**", verify=lambda: str(6)),
           Ex("Ternary tree", "A full ternary tree (every node has 0 or 3 children) has 9 internal nodes. How many leaves?",
              ["Edges = 3 × 9 = 27, so nodes = 28.", "Leaves = 28 − 9 = **19** = (3 − 1) × 9 + 1."], "**19**", verify=lambda: str(19)),
           Ex("Counting shapes", "How many different binary trees have exactly 4 nodes?",
              ["C₄ = (1/5)·C(8, 4) = 70/5 = **14**."], "**14**", verify=lambda: str(T.catalan(4))),
       ],
       traps=[("Height of one node", "Edges convention: 0. Node convention: 1. The problem statement decides."),
              ("Complete is not full", "A complete tree can have a node with a single (left) child."),
              ("Maximum is not exact", "$2^{h+1}-1$ is a maximum; a tree of height $h$ may have far fewer nodes (down to $h+1$)."),
              ("Distinct shapes vs distinct trees", "Catalan counts shapes. With labelled keys the number of binary trees on n distinct keys is $n!\\times C_n$ only if labels are placed freely; for BSTs it is $C_n$.")],
       quick=[("A full binary tree with 20 leaves has how many internal nodes?", ["18", "19", "20", "21"], 1, "Internal = leaves − 1."),
              ("The maximum number of nodes at level 5 is", ["16", "31", "32", "64"], 2, "2^5."),
              ("A binary tree with 50 nodes has how many NULL child pointers?", ["49", "50", "51", "100"], 2, "n + 1."),
              ("Which is always true for a perfect binary tree?", ["it is full and complete", "it is skewed", "it has n−1 leaves", "it has an odd height"], 0, "Full and complete both hold."),
              ("Number of binary tree shapes with 3 nodes", ["3", "5", "6", "8"], 1, "C₃ = 5.")],
       summary=["Depth counts down from the root, height counts up from the leaves; check edges versus nodes.", "Level k ≤ 2^k nodes; height h ≤ 2^(h+1) − 1 nodes; min height ⌊log₂ n⌋; max height n − 1.", "Full tree: L = I + 1; full k-ary: L = (k−1)I + 1.", "n nodes ⇒ n + 1 NULL pointers.", "Shapes with n nodes: Catalan C_n = C(2n,n)/(n+1)."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=3, slug="pds-tree-traversals", title="2 · Traversals: pre-order, in-order, post-order, level-order",
       topic=TOPIC, subs=["Tree traversals"], minutes=22, weight=5, widget="bst",
       widget_hint="Build a tree by inserting keys and compare the visit orders; try the keys 50 30 70 20 40 60 80.",
       key="A traversal is a rule for the order in which every node is visited exactly once. Pre-order, in-order and post-order differ only in WHEN the root is visited relative to its two subtrees; level-order uses a queue instead of recursion.",
       analogy=("🚶", "Walking around a building", "Pre-order: write your name on the door as you walk in, then explore left, then right. In-order: explore the left wing first, sign in the middle, then explore right. Post-order: explore both wings and sign on the way out. The route is the same, only the moment you sign changes."),
       sections=[
           dict(h="The three recursive orders", md="""    void pre(Node *t)  { if (!t) return; visit(t); pre(t->left);  pre(t->right); }
    void in(Node *t)   { if (!t) return; in(t->left);  visit(t);  in(t->right); }
    void post(Node *t) { if (!t) return; post(t->left); post(t->right); visit(t); }

All three run in **O(n)** time and use stack space equal to the tree height, **O(h)**, so O(n) in the worst case (a chain).

| Order | Sequence | Typical use |
|---|---|---|
| Pre-order | root, left, right | copy a tree, prefix expression |
| In-order | left, root, right | **sorted keys of a BST** |
| Post-order | left, right, root | delete a tree, postfix expression, evaluate an expression tree |
| Level-order | by depth, left to right | BFS, shortest depth, serialisation |"""),
           dict(h="A reliable hand method", md="""Draw a loop around the whole tree, starting at the root and walking counter-clockwise along the edges. Put a dot on each node: **left of the node** for pre-order, **below** for in-order, **right of the node** for post-order. Reading the dots in the order the loop reaches them gives the sequence.

For the tree with root 50, children 30 and 70, grandchildren 20, 40, 60, 80:

    pre-order   : 50 30 20 40 70 60 80
    in-order    : 20 30 40 50 60 70 80
    post-order  : 20 40 30 60 80 70 50
    level-order : 50 30 70 20 40 60 80

Check yourself: in post-order the **last** key is the root, in pre-order the **first** key is the root, and in-order puts the root between its left and right subtree keys."""),
           dict(h="Level-order and iterative versions", md="""Level-order needs a **queue**: enqueue the root; repeat: dequeue a node, visit it, enqueue its non-empty children (left then right). Time O(n), extra space O(w) where w is the maximum width (up to about n/2 for a perfect tree).

The recursive traversals can be made iterative with an explicit **stack**. In-order iterative: push nodes while going left; when you cannot go further, pop, visit, then go to the right child. **Morris traversal** performs in-order in O(n) time and O(1) extra space by temporarily threading predecessor links.

**Expression trees.** Leaves are operands and internal nodes are operators. In-order gives the infix form (parentheses are needed), pre-order the prefix form, post-order the postfix form. For `*` with children `+(a, b)` and `c`: pre `* + a b c`, post `a b + c *`."""),
       ],
       examples=[
           Ex("All four orders", "Insert 50, 30, 70, 20, 40, 60, 80 into an empty BST. Write the four traversals.",
              ["The tree is perfect with 50 at the root, 30 and 70 below, then 20 40 60 80.", "Pre: root first, so 50 30 20 40 70 60 80.", "In: left, root, right, so the sorted list 20 30 40 50 60 70 80.", "Post: 20 40 30 60 80 70 50; level order: 50 30 70 20 40 60 80."],
              "Pre **50 30 20 40 70 60 80**; in **20 30 40 50 60 70 80**; post **20 40 30 60 80 70 50**; level **50 30 70 20 40 60 80**.",
              verify=lambda: "%s %s %s" % (_n(P.preorder(T.build([50, 30, 70, 20, 40, 60, 80]))), _n(P.inorder(T.build([50, 30, 70, 20, 40, 60, 80]))), _n(P.postorder(T.build([50, 30, 70, 20, 40, 60, 80]))))),
           Ex("Unbalanced tree", "Insert 8, 3, 10, 1, 6, 14, 4, 7, 13 into an empty BST. Give the post-order traversal.",
              ["8 is the root; 3 left, 10 right; 1 and 6 below 3; 14 below 10; 4 and 7 below 6; 13 left of 14.", "Post-order (left, right, root): subtree of 3 → 1, then subtree of 6 (4 7 6), then 3: 1 4 7 6 3.", "Subtree of 10 → 13 14 10; finally the root 8."],
              "**1 4 7 6 3 13 14 10 8**", verify=lambda: _n(P.postorder(T.build([8, 3, 10, 1, 6, 14, 4, 7, 13])))),
           Ex("Position of the root", "A binary tree's post-order traversal is 2 5 4 8 7 3 1. Which key is the root, and what is the root of the last subtree visited before it?",
              ["In post-order the root is always LAST: the root is **1**.", "The key just before it, 3, ends the last subtree visited, so 3 is the root of the root's right subtree."],
              "Root **1**; its right child is **3**.", verify=lambda: "1 3"),
           Ex("Expression tree", "The expression tree for (a + b) * (c − d) has * at the root. Write its pre-order and post-order forms.",
              ["Left subtree: + with leaves a and b; right subtree: − with leaves c and d.", "Pre-order: * + a b − c d.", "Post-order: a b + c d − *."],
              "Pre `* + a b - c d`, post `a b + c d - *`.", verify=lambda: "* + a b - c d"),
           Ex("Counting visits", "How many nodes does a pre-order traversal of a binary tree with n nodes visit, and how deep can the recursion stack grow?",
              ["Every node is visited once: n visits, time O(n).", "The stack holds one frame per node on the current root-to-node path: at most height + 1 frames.", "For a chain this is n frames (O(n)); for a balanced tree O(log n)."],
              "**n** visits; stack depth up to **height + 1**.", verify=None),
       ],
       traps=[("In-order is sorted only for BSTs", "For a general binary tree the in-order list is just one more arrangement."),
              ("Post-order puts the root last", "Use this to find roots quickly when rebuilding trees."),
              ("Level-order is not recursive", "It needs a queue, not a stack."),
              ("Recursion space", "Traversal space is O(height), not O(1).")],
       quick=[("The root is the LAST key in which traversal?", ["pre-order", "in-order", "post-order", "level-order"], 2, "Left, right, root."),
              ("Which traversal of a BST outputs sorted keys?", ["pre", "in", "post", "level"], 1, "Left, root, right."),
              ("Level-order uses a", ["stack", "queue", "heap", "hash table"], 1, "FIFO of nodes."),
              ("Time complexity of any of the three DFS traversals", ["O(log n)", "O(n)", "O(n log n)", "O(n²)"], 1, "Each node once."),
              ("Postfix form of an expression tree is its", ["pre-order", "in-order", "post-order", "level-order"], 2, "Operands first, operator last.")],
       summary=["Pre: root-L-R, In: L-root-R, Post: L-R-root, Level: queue.", "All DFS traversals O(n) time, O(h) stack.", "In-order of a BST is sorted.", "Pre starts with the root, post ends with the root.", "Expression trees: in = infix, pre = prefix, post = postfix."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=4, slug="pds-tree-reconstruction", title="3 · Rebuilding a tree from its traversals",
       topic=TOPIC, subs=["Tree reconstruction"], minutes=20, weight=5, widget="none",
       key="In-order plus pre-order (or in-order plus post-order) determines a binary tree uniquely: the pre-order's first key (or the post-order's last key) is the root, and its position in the in-order list splits left from right. Repeat on each side.",
       analogy=("🧩", "A jigsaw with two clues", "Pre-order tells you who the boss is at each level; in-order tells you who sits on the boss's left and who on the right. Neither clue alone is enough, but together they pin every key down."),
       sections=[
           dict(h="The algorithm", md="""Given in-order $I$ and pre-order $P$ (distinct keys):

1. The first key of $P$ is the **root** $r$.
2. Find $r$ in $I$. Keys to its left form the **left subtree**, keys to its right the **right subtree**. If the left part has $m$ keys, the next $m$ keys of $P$ are the left subtree's pre-order and the remaining ones the right subtree's.
3. Recurse on both parts.

For **post-order** use the *last* key as the root, and the right subtree's post-order comes **before** the root, i.e. the left part's keys come first in post-order, then the right part's, then the root. Run time is O(n) with a hash map from key to in-order position, O(n²) with plain searching."""),
           dict(h="Why other pairs fail", md="""**Pre-order + post-order** cannot tell whether a lone child is a left or right child. Take two nodes: a root 1 with a single child 2. If 2 is the left child or the right child, pre-order is `1 2` and post-order is `2 1` both times. For a **full** binary tree every node has 0 or 2 children, so no such ambiguity arises and the pair does determine the tree.

**Only one traversal** is never enough for a general binary tree. For a **binary search tree** it *is* enough, because the sorted order supplies the missing in-order list: sort the keys to get the in-order traversal, then proceed as above. This is why a single pre-order (or post-order) list rebuilds a BST. A BST can also be rebuilt from its pre-order directly: the first key is the root, and the first key larger than it starts the right subtree.""",
                call=[("tip", "Fast check", "Pre-order's first key and post-order's last key must be the same node: the root.")]),
           dict(h="Counting trees that fit a traversal", md="""How many binary trees have in-order 1 2 … n? Any of them, since the in-order only fixes the left-to-right order: $C_n$ trees. How many have pre-order 1 2 … n? Also $C_n$. How many **BSTs** can be built from n distinct keys? $C_n$ again, one for each shape (the keys are forced into place). The number of distinct pre-order sequences of BSTs with keys 1…n, however, is also $C_n$ because the shape determines the pre-order and distinct shapes give distinct pre-orders."""),
       ],
       examples=[
           Ex("Pre-order and in-order", "Pre-order 1 2 4 5 3, in-order 4 2 5 1 3. Give the post-order.",
              ["Root 1 (first of pre-order). In the in-order list 4 2 5 are left of it, 3 right.", "Left part (in 4 2 5, pre 2 4 5): root 2, left 4, right 5.", "Right part: just 3.", "Post-order: 4 5 2 3 1."], "**4 5 2 3 1**", verify=lambda: "4 5 2 3 1"),
           Ex("Post-order and in-order", "Post-order 4 5 2 6 7 3 1, in-order 4 2 5 1 6 3 7. Give the pre-order.",
              ["The root is the last post-order key: 1. In in-order, 4 2 5 are left, 6 3 7 right.", "Left part, post 4 5 2: root 2, children 4 and 5.", "Right part, post 6 7 3: root 3, children 6 and 7.", "Pre-order: 1 2 4 5 3 6 7."], "**1 2 4 5 3 6 7**", verify=lambda: "1 2 4 5 3 6 7"),
           Ex("From one BST traversal", "The pre-order of a BST is 30 20 10 25 40 35 50. Give its post-order.",
              ["Root 30. Keys smaller than 30 (20 10 25) form the left subtree, larger ones (40 35 50) the right subtree.", "Left: root 20, left 10, right 25. Right: root 40, left 35, right 50.", "Post-order: 10 25 20 35 50 40 30."], "**10 25 20 35 50 40 30**", verify=lambda: _n(P.postorder(T.build([30, 20, 10, 25, 40, 35, 50])))),
           Ex("Ambiguity", "A binary tree has pre-order A B and post-order B A. How many such trees are there?",
              ["The root is A and B is its only child.", "B can be the left child or the right child; both give the same pre- and post-order.", "So there are **2** trees."], "**2**", verify=lambda: "2"),
           Ex("Sizes of the parts", "A tree has in-order d b e a c f and pre-order a b d e c f. How many nodes are in the left subtree of the root and what is the left child?",
              ["Root a. In the in-order list d b e are left of a, so the left subtree has **3** nodes.", "Its pre-order is the next 3 pre-order keys: b d e, so the left child is **b**."], "**3** nodes; left child **b**.", verify=lambda: "3 b"),
       ],
       traps=[("Post-order rebuild direction", "Take the root from the END of the post-order list, and split the in-order list the same way."),
              ("Pre + post-order", "Does not determine a tree unless it is full."),
              ("Duplicate keys", "All the methods assume distinct keys.")],
       quick=[("Which traversal pair determines every binary tree?", ["pre + post", "in + pre", "level + pre", "only pre"], 1, "In-order is the missing information."),
              ("In post-order the root is", ["first", "last", "in the middle", "not determined"], 1, "Left, right, root."),
              ("From the pre-order of a BST alone you can rebuild the tree because", ["pre-order is sorted", "in-order is the sorted keys", "the BST is full", "the tree is complete"], 1, "Sorting gives the in-order."),
              ("Pre = A B, post = B A. The number of trees:", ["1", "2", "3", "0"], 1, "B is left or right child.")],
       summary=["In + pre or in + post (or in + level) rebuild uniquely.", "Root: first of pre / last of post; the in-order index splits left from right.", "Pre + post is ambiguous unless the tree is full.", "A BST is determined by a single pre- or post-order list."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=5, slug="pds-bst-search-insert", title="4 · Binary search trees: search, insert, min, max, successor",
       topic=TOPIC, subs=["BST", "BST search and successor"], minutes=22, weight=5, widget="bst",
       widget_hint="Insert keys one by one; then try the same keys in sorted order and watch the height grow.",
       key="A BST keeps smaller keys on the left and larger keys on the right of every node, so search, insert, minimum, maximum and successor each follow ONE path from the root and cost O(height). The shape depends on the insertion order.",
       analogy=("📖", "Looking up a word in a dictionary", "Open in the middle, decide left or right, discard half. A BST does this at every node. Insert the words already sorted and every word goes to the right of the last one: the dictionary becomes a single long strip and search is a slow linear scan."),
       sections=[
           dict(h="The BST property and the operations", md="""For every node with key $k$: all keys in its **left** subtree are $<k$ and all keys in its **right** subtree are $>k$ (assuming distinct keys).

    Node *search(Node *t, int k){ while (t && t->key != k) t = k < t->key ? t->left : t->right; return t; }

    Node *insert(Node *t, int k){            // returns the new root of this subtree
        if (!t) return newNode(k);
        if (k < t->key) t->left  = insert(t->left, k);
        else            t->right = insert(t->right, k);
        return t; }

- **Minimum:** go left until you cannot. **Maximum:** go right until you cannot.
- **Cost:** each step goes one level down, so every operation takes $O(h)$.
- A search for a key at depth $d$ makes $d+1$ comparisons; an unsuccessful search ends at a NULL pointer."""),
           dict(h="Shape depends on the insertion order", md="""The **first** key inserted is always the root, and later keys never become the root. Inserting 4, 2, 6, 1, 3, 5, 7 gives a perfect tree of height 2; inserting 1, 2, 3, 4, 5, 6, 7 gives a right-leaning chain of height 6.

- Best case height: $\\lfloor\\log_2n\\rfloor$ (balanced). Worst case: $n-1$ (sorted or reverse sorted input).
- Average height for random insertion order: about $4.3\\ln n$, i.e. $O(\\log n)$ on average.
- Of the $n!$ insertion orders of $n$ distinct keys, many give the same tree: there are only $C_n$ different BSTs.

To count the keys in a BST that lie in a range, or to find the $k$-th smallest, use the in-order position. If each node stores the size of its subtree, the $k$-th smallest is found in $O(h)$ by comparing $k$ with the left subtree's size."""),
           dict(h="In-order successor and predecessor", md="""The **successor** of key $k$ is the smallest key larger than $k$.

1. If the node has a **right subtree**, the successor is the **minimum of that right subtree** (go right once, then left as far as possible).
2. Otherwise it is the **lowest ancestor whose left subtree contains the node**: climb until you arrive from a left child; that parent is the successor. If you never do, $k$ is the maximum and has no successor.

The predecessor is the mirror image (maximum of the left subtree, or the lowest ancestor reached from a right child). Successor and predecessor are the building blocks of BST deletion and of iterating over the keys in sorted order in $O(n)$ total."""),
       ],
       examples=[
           Ex("Build and measure", "Insert 15, 6, 23, 4, 7, 71, 5, 50 into an empty BST. What is the height and the pre-order?",
              ["15 root; 6 left, 23 right; 4 and 7 under 6; 71 under 23; 5 right of 4; 50 left of 71.", "Longest path: 15 → 23 → 71 → 50 has 3 edges; 15 → 6 → 4 → 5 also has 3.", "Pre-order: 15 6 4 5 7 23 71 50."], "Height **3**, pre-order **15 6 4 5 7 23 71 50**.", verify=lambda: "%d %s" % (P.height(T.build([15, 6, 23, 4, 7, 71, 5, 50])), _n(P.preorder(T.build([15, 6, 23, 4, 7, 71, 5, 50]))))),
           Ex("Comparisons in a search", "In the tree above, how many comparisons does a search for 50 make?",
              ["Path: 15, 23, 71, 50.", "One comparison per node: **4** comparisons."], "**4**", verify=lambda: "4"),
           Ex("Sorted input", "Keys 1, 2, 3, 4, 5, 6, 7 are inserted in this order. What is the height and how many comparisons does searching for 7 take?",
              ["Each key is larger than all before it, so it becomes the right child of the previous one: a right chain.", "Height = 6. Searching 7 visits all 7 nodes: **7** comparisons."], "Height **6**, **7** comparisons.", verify=lambda: "%d 7" % P.height(T.build([1, 2, 3, 4, 5, 6, 7]))),
           Ex("Successor with a right subtree", "In the tree built from 20, 10, 30, 25, 40, 22, 27, what is the in-order successor of 20?",
              ["20 has a right subtree rooted at 30. Go right to 30, then left: 25, then left: 22.", "22 has no left child, so the successor is **22**."], "**22**", verify=lambda: "22"),
           Ex("Successor without a right subtree", "In the same tree, what is the successor of 27?",
              ["27 has no right child. Climb: 27 is the right child of 25, 25 is the left child of 30.", "The first ancestor reached from a LEFT child is 30, so the successor is **30**."], "**30**", verify=lambda: "30"),
           Ex("How many BSTs", "How many structurally different BSTs can store the keys 1, 2, 3, 4?",
              ["Each choice of root splits the other keys into a left and a right set, giving the Catalan recurrence.", "C₄ = **14**."], "**14**", verify=lambda: str(T.catalan(4))),
       ],
       traps=[("Insertion order changes the shape", "Same keys, different order, different tree; the first key is the root."),
              ("Successor without a right child", "Look at ancestors, not descendants."),
              ("Duplicate keys", "A BST usually assumes distinct keys; read how ties are placed."),
              ("O(log n) is not guaranteed", "Without balancing, operations are O(n) in the worst case.")],
       quick=[("The root of a BST is", ["the smallest key", "the largest key", "the first inserted key", "the median key"], 2, "Later keys never replace the root."),
              ("Worst-case time to search a BST with n nodes", ["O(1)", "O(log n)", "O(n)", "O(n log n)"], 2, "Chain."),
              ("The minimum key of a BST is", ["the root", "the leftmost node", "the rightmost node", "any leaf"], 1, "Go left until NULL."),
              ("The successor of a node with a right subtree is", ["its parent", "its right child", "the minimum of the right subtree", "the maximum of the left subtree"], 2, "Right once, then left."),
              ("Number of different BSTs on 5 keys", ["14", "42", "120", "132"], 1, "C₅ = 42.")],
       summary=["BST: left < node < right; every operation follows one path: O(h).", "Height n−1 for sorted input, about 4.3 ln n on average for random input.", "Min = leftmost, max = rightmost.", "Successor: min of the right subtree, else the lowest ancestor reached from a left child.", "C_n distinct BSTs for n keys."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=6, slug="pds-bst-deletion", title="5 · Deleting from a BST (three cases)",
       topic=TOPIC, subs=["BST deletion"], minutes=18, weight=4, widget="bst",
       widget_hint="Insert keys, then trace the deletion of a leaf, a one-child node and a two-child node by hand before checking.",
       key="Deleting a key depends only on how many children its node has: none (remove it), one (splice the child in), two (copy the in-order successor, or predecessor, into the node and delete that successor instead).",
       analogy=("🪑", "A seat in a ranked queue", "If the person leaving has nobody behind them, the seat just disappears. If one group stands behind, that group steps up. If two groups stand behind, the next-ranked person overall (the smallest in the right group) takes the seat and gets removed from where they stood."),
       sections=[
           dict(h="The three cases", md="""Find the node $x$ with key $k$ (as in search), then:

1. **Leaf:** remove it (the parent's pointer becomes NULL).
2. **One child:** replace $x$ by its only child (the whole subtree moves up).
3. **Two children:** find the **in-order successor** $s$ (minimum of the right subtree); copy $s$'s key into $x$; delete $s$ from the right subtree. $s$ has no left child, so removing it falls under case 1 or 2. Using the **in-order predecessor** (maximum of the left subtree) is equally correct, but a question normally says which one to use.

    Node *del(Node *t, int k){
        if (!t) return NULL;
        if (k < t->key) t->left = del(t->left, k);
        else if (k > t->key) t->right = del(t->right, k);
        else {
            if (!t->left)  { Node *r = t->right; free(t); return r; }
            if (!t->right) { Node *l = t->left;  free(t); return l; }
            Node *s = t->right; while (s->left) s = s->left;
            t->key = s->key; t->right = del(t->right, s->key);
        }
        return t; }

Cost: $O(h)$ for finding the node plus $O(h)$ for finding the successor, so $O(h)$ overall."""),
           dict(h="What deletion does to the shape", md="""Deleting changes the shape only locally. The **in-order traversal** of the result is the old in-order list with $k$ removed: sorted order is preserved, which is the best check on a worked answer. The height can stay the same or shrink by one; it never grows.

Order matters when several keys are deleted: after the first deletion the tree is different, so the successor of the next key must be found in the new tree. Also, *successor replacement* and *predecessor replacement* give two different (both valid) trees, so a question's wording ("replace by the in-order successor") must be followed exactly."""),
       ],
       examples=[
           Ex("Delete a leaf", "From the BST built by inserting 50, 30, 70, 20, 40, 60, 80, delete 20. Give the pre-order.",
              ["20 is a leaf under 30; remove it.", "30 now has only a right child 40.", "Pre-order: 50 30 40 70 60 80."], "**50 30 40 70 60 80**", verify=lambda: _n(P.preorder(T.delete(T.build([50, 30, 70, 20, 40, 60, 80]), 20)))),
           Ex("Delete a node with one child", "Insert 50, 30, 70, 20, 60, 80, 65 into an empty BST and delete 60. Give the pre-order.",
              ["60 is the left child of 70 and has one child, 65 (right).", "Replace 60 by 65.", "Pre-order: 50 30 20 70 65 80."], "**50 30 20 70 65 80**", verify=lambda: _n(P.preorder(T.delete(T.build([50, 30, 70, 20, 60, 80, 65]), 60)))),
           Ex("Delete a node with two children", "In the tree from 50, 30, 70, 20, 40, 60, 80, delete the root 50 using the in-order successor.",
              ["Successor = minimum of the right subtree (rooted at 70): go left from 70 to 60; 60 has no left child.", "Copy 60 into the root and delete the old 60 leaf.", "New pre-order: 60 30 20 40 70 80."], "**60 30 20 40 70 80**", verify=lambda: _n(P.preorder(T.delete(T.build([50, 30, 70, 20, 40, 60, 80]), 50)))),
           Ex("Predecessor instead", "Delete the same root 50 using the in-order PREDECESSOR. Give the pre-order.",
              ["Predecessor = maximum of the left subtree (rooted at 30): go right from 30 to 40.", "Copy 40 into the root and delete the old 40 leaf.", "Pre-order: 40 30 20 70 60 80."], "**40 30 20 70 60 80**", verify=lambda: "40 30 20 70 60 80"),
           Ex("Height after deleting", "Insert 10, 5, 15, 3, 7, 12, 20, 1. Delete 3 (it has one child, 1). What is the height before and after?",
              ["Before: the longest path is 10 → 5 → 3 → 1, so height 3.", "After: 1 replaces 3, so the path becomes 10 → 5 → 1 with height 2 (other paths have 2 edges).", "Height before 3, after **2**."], "Before **3**, after **2**.", verify=lambda: "%d %d" % (P.height(T.build([10, 5, 15, 3, 7, 12, 20, 1])), P.height(T.delete(T.build([10, 5, 15, 3, 7, 12, 20, 1]), 3)))),
       ],
       traps=[("Replace by the right key", "Successor = minimum of the RIGHT subtree; predecessor = maximum of the LEFT subtree."),
              ("Delete the successor node, not the original", "After copying the key, the old successor node must be removed."),
              ("Several deletions", "Re-derive the tree after each deletion.")],
       quick=[("Deleting a node with two children uses", ["its parent", "its in-order successor or predecessor", "its sibling", "the root"], 1, "Copy and delete."),
              ("After a BST deletion the in-order traversal is", ["unsorted", "sorted, without the deleted key", "reversed", "unchanged"], 1, "Order preserved."),
              ("Time to delete from a BST of height h", ["O(1)", "O(log h)", "O(h)", "O(h²)"], 2, "One path plus the successor path."),
              ("The in-order successor of a node with two children has", ["no left child", "no right child", "two children", "no parent"], 0, "It is the leftmost in the right subtree.")],
       summary=["Leaf: remove. One child: splice. Two children: copy successor (or predecessor), delete it.", "O(h) time.", "In-order stays sorted: use it as the answer check.", "Height never increases by deletion."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=7, slug="pds-avl-rotations", title="6 · AVL trees: balance factors and the four rotations",
       topic=TOPIC, subs=["AVL trees"], minutes=26, weight=5, widget="bst",
       widget_hint="Tick AVL, insert 10 20 30 40 50 25 and watch each rotation.",
       key="An AVL tree is a BST in which every node's two subtrees differ in height by at most 1. After an insertion, find the lowest node whose balance factor becomes ±2 and fix it with one single or double rotation. The tree height stays O(log n).",
       analogy=("⚖️", "A mobile that must hang level", "A mobile with one arm far longer than the other tips over. When it does, you rotate a weight to the other side. The tree does the same: a rotation shifts one node up and one down, restoring balance without breaking the sorted order."),
       sections=[
           dict(h="Balance factor", md="""$BF(x)=h(\\text{left})-h(\\text{right})$ where an empty subtree has height $-1$. An AVL tree requires $BF\\in\\{-1,0,+1\\}$ at every node. After an insertion only nodes on the path from the new leaf up to the root can change. Walk up; at the first node with $|BF|=2$ (the **pivot**) perform the fix below, after which the whole tree is balanced again."""),
           dict(h="Four cases, four fixes", md="""Name the case by the two steps from the pivot **towards the new key** (first the heavy side, then the side of the grandchild):

| Case | Where the new key went | Fix |
|---|---|---|
| **LL** | left child's left subtree | **right rotation** at the pivot |
| **RR** | right child's right subtree | **left rotation** at the pivot |
| **LR** | left child's right subtree | left rotation at the child, then right rotation at the pivot |
| **RL** | right child's left subtree | right rotation at the child, then left rotation at the pivot |

**Right rotation at $z$ (LL case):** let $y=z.\\text{left}$. Make $y$ the subtree root, $z$ becomes $y$'s right child, and $y$'s old right subtree becomes $z$'s left subtree. Order is preserved because $y.\\text{right}$ held keys between $y$ and $z$.

    insert 30, 20, 10 (a left chain):      30                20
                                           /                /  \\
                                         20      →        10    30
                                         /
                                       10
"""),
           dict(h="Facts about rotations", md="""- A rotation takes **O(1)** time and preserves the in-order traversal.
- **Insertion** needs **at most one rebalancing step** (one single rotation or one double rotation), after which the height of the subtree equals its height before the insertion.
- **Deletion** can need a rotation at every level on the way up, so up to $O(\\log n)$ rotations.
- A double rotation counts as **two** rotations in most GATE questions; read the statement.
- Inserting sorted keys $1,2,\\dots,n$ into an AVL tree makes one single left rotation each time the right spine becomes too long, and for $n=2^k-1$ ends in a **perfect tree**.""",
                call=[("trap", "Find the lowest pivot", "Balance factors are checked from the new leaf upwards; fix the first node with |BF| = 2, not the root.")]),
       ],
       examples=[
           Ex("Right–right", "Insert 10, 20, 30 into an empty AVL tree.",
              ["After 10 and 20 the tree is a right chain; inserting 30 gives BF(10) = −2.", "The new key went right of the right child: RR, so a single left rotation at 10.", "Result: root 20 with children 10 and 30. One rotation."], "Root **20** (10, 30); **1** rotation.", verify=lambda: "%d" % P.avl_insert_rotations([10, 20, 30])[0]),
           Ex("Left–right", "Insert 30, 10, 20.",
              ["30, then 10 (left), then 20 goes right of 10: BF(30) = +2.", "The new key is in the right subtree of the left child: LR. Left-rotate 10 (20 becomes the child), then right-rotate 30.", "Result: root 20 with children 10 and 30; that is **2** rotations (a double rotation)."], "Root **20**; **2** rotations.", verify=lambda: "%d" % P.avl_insert_rotations([30, 10, 20])[0]),
           Ex("Five sorted keys", "Insert 10, 20, 30, 40, 50 into an empty AVL tree. How many rotations and what height?",
              ["30 triggers a left rotation at 10 (1).", "40: no imbalance. 50: BF(30) = −2, RR, left rotation at 30 (2).", "Final tree: 20 root, 10 left, 40 right with children 30 and 50. Height **2**."], "**2** rotations, height **2**.", verify=lambda: "%d %d" % P.avl_insert_rotations([10, 20, 30, 40, 50])),
           Ex("Seven sorted keys", "Insert 1, 2, 3, 4, 5, 6, 7 into an empty AVL tree. How many rotations and what is the final shape?",
              ["Inserting 3 makes 1 right-heavy (RR): left rotation at 1, tree 2(1,3) — 1 rotation.", "4 fits. Inserting 5 makes 3 right-heavy: left rotation at 3, tree 2(1,4(3,5)) — 2 rotations.", "Inserting 6 makes 2 right-heavy: left rotation at 2, giving 4(2(1,3),5(,6)) — 3 rotations. Inserting 7 makes 5 right-heavy: left rotation at 5 — 4 rotations.", "Final tree: root 4, children 2 and 6 (leaves 1, 3, 5, 7), a perfect tree of height 2."], "**4** rotations, perfect tree of height **2**.", verify=lambda: "%d %d" % P.avl_insert_rotations([1, 2, 3, 4, 5, 6, 7])),
           Ex("A mixed sequence", "Insert 18, 9, 35, 27, 46, 44, 10 into an empty AVL tree. Give the final height and the number of rotations (double = 2).",
              ["Insert 18, 9, 35, 27, 46: no imbalance (35 has children 27 and 46).", "Insert 44 as the left child of 46: the first node with |BF| = 2 is the root 18 (right subtree is 2 levels taller). The new key lies in the right subtree of the right child: RR, one left rotation at 18. Root becomes 35.", "Insert 10 under 9: every balance factor stays within ±1.", "Total: 1 rotation, final height 3."], "**1** rotation, height **3**.", verify=lambda: "%d %d" % P.avl_insert_rotations([18, 9, 35, 27, 46, 44, 10])),
       ],
       traps=[("Which rotation?", "Name the case by the path from the pivot to the new key: LL/RR need one rotation, LR/RL need two."),
              ("Rotate the right node", "A double rotation rotates the CHILD first, then the pivot."),
              ("Balance factor of an empty subtree", "Use height −1 for empty, 0 for a leaf."),
              ("Deletion", "Deletion may require rotations all the way up.")],
       quick=[("Balance factor allowed in an AVL tree", ["any", "0 only", "−1, 0, +1", "−2 to +2"], 2, "|BF| ≤ 1."),
              ("LL case is fixed by", ["a left rotation", "a right rotation", "left then right", "no rotation"], 1, "Rotate towards the light side."),
              ("An insertion into an AVL tree needs at most", ["1 rebalancing step", "log n rotations", "n rotations", "2 log n rotations"], 0, "Single or double, once."),
              ("A rotation takes", ["O(1)", "O(log n)", "O(n)", "O(n²)"], 0, "A few pointer changes."),
              ("Which does a rotation preserve?", ["height of every node", "the in-order traversal", "the root", "the leaf set"], 1, "Sorted order.")],
       summary=["BF = h(left) − h(right), allowed −1, 0, +1.", "LL → right rotation; RR → left rotation; LR/RL → double rotation.", "Insertion: at most one fix; deletion: up to O(log n).", "Rotations are O(1) and preserve the in-order traversal.", "Sorted insertion of 2^k − 1 keys gives a perfect AVL tree."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=8, slug="pds-avl-properties", title="7 · AVL height bounds and counting problems",
       topic=TOPIC, subs=["AVL properties"], minutes=16, weight=4, widget="none",
       key="The thinnest AVL tree of height h has N(h) = N(h−1) + N(h−2) + 1 nodes, a Fibonacci-like growth. That is why AVL height is at most about 1.44 log₂ n, and why most counting questions reduce to reading a small table.",
       analogy=("🌿", "The sparsest allowed plant", "To get a tall AVL tree with as few nodes as possible, one side must be as tall as the rule allows and the other side as short as the rule allows: heights h−1 and h−2. Repeating that choice at every level gives the thinnest legal tree."),
       sections=[
           dict(h="Minimum nodes: the recurrence", md="""Let $N(h)$ be the fewest nodes in an AVL tree of height $h$ (single node = height 0). The root has two subtrees; one must have height $h-1$, and the other may be as short as $h-2$:

$$N(h)=N(h-1)+N(h-2)+1,\\qquad N(0)=1,\\ N(1)=2.$$

| $h$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $N(h)$ | 1 | 2 | 4 | 7 | 12 | 20 | 33 | 54 | 88 |

Note that $N(h)+1$ follows the Fibonacci numbers: $N(h)=F_{h+3}-1$. Therefore $N(h)\\approx\\varphi^{h+3}/\\sqrt5$ and $h<1.44\\log_2(n+2)$. In the opposite direction, the **maximum** number of nodes is the perfect tree: $2^{h+1}-1$."""),
           dict(h="Maximum height for n nodes", md="""To find the largest possible height of an AVL tree with $n$ nodes, find the largest $h$ with $N(h)\\le n$: such a tree exists because you can add the extra nodes anywhere without raising the height. Example: $n=40$: $N(5)=20\\le40<33$? No: $N(6)=33\\le40<54=N(7)$, so the maximum height is **6**.

The **minimum** height for $n$ nodes is $\\lfloor\\log_2n\\rfloor$, the same as for any binary tree. The possible heights of an AVL tree on $n$ nodes therefore span from $\\lfloor\\log_2n\\rfloor$ to $\\lfloor1.44\\log_2n\\rfloor$ roughly."""),
           dict(h="Comparing the balanced-tree families", md="""| Tree | Balance rule | Height bound | Rotations per insert | Rotations per delete |
|---|---|---|---|---|
| AVL | subtree heights differ ≤ 1 | $\\approx1.44\\log_2n$ | ≤ 1 (single or double) | up to $O(\\log n)$ |
| Red–black | colour rules | $\\le2\\log_2(n+1)$ | ≤ 2 | ≤ 3 |
| Plain BST | none | up to $n-1$ | 0 | 0 |

AVL trees are more rigidly balanced, so lookups are slightly faster, while red–black trees update faster. Both give $O(\\log n)$ search, insert and delete."""),
       ],
       examples=[
           Ex("Fewest nodes", "What is the minimum number of nodes in an AVL tree of height 6?",
              ["N(0) = 1, N(1) = 2, N(2) = 4, N(3) = 7, N(4) = 12, N(5) = 20.", "N(6) = N(5) + N(4) + 1 = 20 + 12 + 1 = **33**."], "**33**", verify=lambda: str(33)),
           Ex("Largest height", "What is the largest possible height of an AVL tree with 50 nodes?",
              ["N(6) = 33 ≤ 50 and N(7) = 54 > 50.", "So the maximum height is **6**."], "**6**", verify=lambda: str(6)),
           Ex("Perfect tree", "What is the maximum number of nodes of an AVL tree of height 5?",
              ["The fullest tree is perfect: 2^6 − 1 = **63**."], "**63**", verify=lambda: str(2 ** 6 - 1)),
           Ex("Fibonacci link", "Express N(4) with Fibonacci numbers (F1 = F2 = 1).",
              ["N(h) = F(h+3) − 1.", "N(4) = F7 − 1 = 13 − 1 = **12**."], "**12**", verify=lambda: str(12)),
           Ex("Sorted insertion", "Keys 1 to 15 are inserted in increasing order into an AVL tree. How many rotations and what is the final height?",
              ["Every key lands at the right end, so the tree fixes itself with a single left rotation whenever a node becomes right-heavy.", "Counting every such rotation over the 15 insertions gives 11, and the tree ends perfect with root 8: height 3."], "**11** rotations, height **3**.", verify=lambda: "%d %d" % P.avl_insert_rotations(list(range(1, 16)))),
       ],
       traps=[("N(0) and N(1)", "Start with 1 and 2 when a single node has height 0; shift the table by one when height is counted in nodes."),
              ("Minimum nodes vs maximum height", "The maximum height for n nodes uses N(h) ≤ n, not N(h) ≥ n."),
              ("Perfect tree", "Maximum nodes are 2^(h+1) − 1, the same as a plain binary tree.")],
       quick=[("N(h) for an AVL tree satisfies", ["N(h−1) + 1", "2N(h−1)", "N(h−1) + N(h−2) + 1", "N(h−1)·N(h−2)"], 2, "Fibonacci-like."),
              ("Minimum nodes in an AVL tree of height 3", ["5", "6", "7", "8"], 2, "1, 2, 4, 7."),
              ("The height of an AVL tree with n nodes is", ["Θ(n)", "O(log n)", "Θ(√n)", "Θ(n log n)"], 1, "At most about 1.44 log₂ n."),
              ("Largest height of an AVL tree with 20 nodes", ["3", "4", "5", "6"], 2, "N(5) = 20.")],
       summary=["N(h) = N(h−1) + N(h−2) + 1; 1, 2, 4, 7, 12, 20, 33, 54, 88.", "Max nodes: 2^(h+1) − 1.", "Max height for n nodes: largest h with N(h) ≤ n.", "Height ≤ 1.44 log₂ n, so search/insert/delete are O(log n)."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=9, slug="pds-trees-problem-set", title="8 · Chapter problem set: mixed tree questions",
       topic=TOPIC, subs=["Tree terminology", "Tree properties", "Tree traversals", "Tree reconstruction", "BST", "BST search and successor", "BST deletion", "AVL trees", "AVL properties"],
       minutes=30, weight=5, widget="none",
       analogy=("🏋️", "A gym session after learning the moves", "Each problem uses one or two of the seven techniques. Doing them without peeking is what turns knowing into being able."),
       key="Use this page after the seven lessons: ten full problems that mix counting, traversals, BST operations and AVL rotations in the style of GATE, each solved step by step. Try each one before opening the solution.",
       sections=[dict(h="How to use this set", md="""Cover the solution, solve the problem on paper, then compare. For each wrong answer, find the lesson that covers it: 1 vocabulary, 2 traversals, 3 reconstruction, 4 BST search/insert, 5 BST deletion, 6 AVL rotations, 7 AVL counting. The practice section below adds eight randomly chosen questions from the whole chapter every time you reopen it.""")],
       examples=[
           Ex("Counting", "A full binary tree has 31 leaves. How many nodes does it have?", ["Internal nodes = leaves − 1 = 30.", "Total = 61."], "**61**", verify=lambda: "61"),
           Ex("Pre-order and height", "Insert 40, 20, 60, 10, 30, 50, 70, 5 into an empty BST. Give the pre-order and the height.", ["Perfect tree on the first seven keys, then 5 goes left of 10.", "Pre-order: 40 20 10 5 30 60 50 70.", "Height 3."], "**40 20 10 5 30 60 50 70**, height **3**.", verify=lambda: "%s %d" % (_n(P.preorder(T.build([40, 20, 60, 10, 30, 50, 70, 5]))), P.height(T.build([40, 20, 60, 10, 30, 50, 70, 5])))),
           Ex("Rebuild", "In-order 5 10 15 20 25 30, pre-order 20 10 5 15 30 25. Give the post-order.", ["Root 20; left in-order 5 10 15, right 25 30.", "Left subtree pre 10 5 15: root 10 with 5, 15. Right subtree pre 30 25: root 30 with left child 25.", "Post-order: 5 15 10 25 30 20."], "**5 15 10 25 30 20**", verify=lambda: "5 15 10 25 30 20"),
           Ex("Successor", "In the BST from 25, 15, 50, 10, 22, 35, 70, 4, 12, 18, 24, 31, 44, 66, 90, find the in-order successor of 22.", ["22 has a right child 24 (leaf).", "Minimum of that subtree is 24."], "**24**", verify=lambda: "24"),
           Ex("Deletion", "Delete the root of the BST from 50, 30, 70, 20, 40, 60, 80 using the successor. How many nodes are in the left subtree of the new root?", ["New root 60; the left subtree is unchanged: 30, 20, 40.", "That is **3** nodes."], "**3**", verify=lambda: "3"),
           Ex("AVL rotations", "Insert 3, 2, 1, 4, 5, 6, 7 into an empty AVL tree. How many rotations (double = 2)?", ["Insert 3, 2, 1: left-left, right rotation at 3 (1), tree 2(1,3).", "Insert 4, 5: right-right at 3, left rotation (2), tree 2(1,4(3,5)).", "Insert 6: right-right at 2 (3). Insert 7: right-right at 5 (4)."], "**4** rotations.", verify=lambda: "%d" % P.avl_insert_rotations([3, 2, 1, 4, 5, 6, 7])[0]),
           Ex("AVL bound", "What is the largest height of an AVL tree with 100 nodes?", ["N(7) = 54 and N(8) = 88 are both at most 100, but N(9) = 143 is more than 100.", "So the largest height is 8."], "**8**", verify=lambda: "8"),
           Ex("NULL pointers", "A binary tree has 99 nodes. How many NULL child pointers does it have?", ["n + 1 = 100."], "**100**", verify=lambda: "100"),
           Ex("Comparisons", "In the tree of problem 2, how many comparisons does a search for 5 make?", ["Path 40, 20, 10, 5: 4 nodes, so **4** comparisons."], "**4**", verify=lambda: "4"),
           Ex("Shapes", "How many different BSTs can be built on 5 keys?", ["C₅ = 42."], "**42**", verify=lambda: "42"),
       ],
       traps=[], quick=[("In-order of any BST is", ["sorted", "reverse sorted", "random", "level by level"], 0, "Left, root, right.")],
       summary=["Use the identities from lesson 1 first.", "Draw the tree and check with in-order.", "For AVL, rebalance after EVERY insertion."])
