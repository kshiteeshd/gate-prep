"""Textbook-style long-form teaching text: Programming and Data Structures."""
from learn import elab

elab("pds-c-operators-bits",
 ("How C stores numbers", """
A computer stores everything as bits. A C variable of type `int` typically occupies 4 bytes (32 bits), `char` 1 byte, `short` 2 bytes, `long long` 8 bytes, `float` 4 bytes, `double` 8 bytes. The *type* tells the compiler how many bits to use and how to interpret them.

Signed integers use **two's complement**: the top bit has a negative weight. In 8 bits, `1111 1111` is $-1$, `1000 0000` is $-128$ and `0111 1111` is $127$. The range of an $n$-bit signed integer is $-2^{n-1}$ to $2^{n-1}-1$; an unsigned one ranges from $0$ to $2^n-1$.

When a value does not fit, it **wraps around** (for unsigned types this is well-defined: $255+1=0$ in 8 bits). For *signed* overflow the C standard does not define the result, so exam questions about it usually ask what typical hardware does.
"""),
 ("Operators: precedence, associativity and evaluation", """
When an expression has several operators, **precedence** decides which is applied first and **associativity** decides the order among operators of equal precedence. Roughly from high to low: postfix (`++`, `--`, `[]`, `->`), prefix and unary (`!`, `~`, `++`, `*`, `&`, `sizeof`), multiplicative (`* / %`), additive, shifts, relational, equality, bitwise `&`, `^`, `|`, logical `&&`, `||`, conditional `?:`, assignment, comma.

Two rules cause most exam surprises:

- **Integer division truncates toward zero**: `7/2` is 3 and `-7/2` is $-3$. `%` has the sign of the left operand: `-7 % 2` is $-1$.
- **Short-circuit evaluation**: in `a && b`, if `a` is false then `b` is *not evaluated at all*; in `a || b`, if `a` is true, `b` is skipped. Side effects in `b` (like `i++`) therefore may not happen.

Also remember that `=` is assignment and `==` is comparison; in `if (x = 5)` the condition is the *value assigned* (5, true).
"""),
 ("Bitwise tricks", """
The bitwise operators work on each bit independently: `&` (and), `|` (or), `^` (xor), `~` (not), `<<` (left shift), `>>` (right shift).

- `x << k` multiplies by $2^k$; `x >> k` divides by $2^k$ (rounding down for non-negative numbers).
- `x & 1` tests whether `x` is odd. `x & (x-1)` clears the lowest set bit, so `x & (x-1) == 0` tests for a power of two (for $x>0$).
- `x ^ x = 0`, and `a ^ b ^ a = b`, which is how a pair of equal values cancels in "find the single non-repeated element".
- To set bit $k$: `x | (1<<k)`; to clear it: `x & ~(1<<k)`; to toggle it: `x ^ (1<<k)`.

**Code with no defined meaning.** Modifying a variable twice between sequence points (`i = i++ + ++i`) has no defined result; exam questions about this often accept "undefined".
"""),
)

elab("pds-pointers-memory",
 ("What a pointer really is", """
Memory is a long row of numbered byte-sized boxes. The number of a box is its **address**. A **pointer** is simply a variable whose value is an address. If `int x = 5;` lives at address 1000, then `int *p = &x;` stores 1000 in `p`. The expression `*p` means "the thing at the address in `p`", so `*p` is 5. Writing `*p = 9;` changes `x`.

The pointer's type matters for **arithmetic**: if `p` points to an `int` (4 bytes), `p + 1` is the address 4 bytes further on, not 1 byte. In general `p + k` moves by `k * sizeof(*p)` bytes.
"""),
 ("Arrays, strings and 2-D arrays", """
An array is a block of consecutive elements, and the name of the array *decays* to a pointer to its first element in most expressions. That is why `a[i]` is exactly `*(a + i)`. The address of element `a[i]` is `base + i * sizeof(element)`.

A 2-D array `int m[R][C]` is stored **row by row** (row-major order), so the address of `m[i][j]` is `base + (i*C + j) * sizeof(int)`.

A C **string** is an array of `char` ending with the null character `'\\0'`. `strlen` counts characters before the null; the array holding "abc" needs 4 bytes. Comparing strings requires `strcmp`, not `==`, which would compare addresses.
"""),
 ("Structs, memory layout and storage classes", """
A `struct` groups fields. The compiler inserts **padding** so that each field starts at an address that is a multiple of its own size (its *alignment*), and the total size is rounded up to a multiple of the largest alignment. `struct { char c; int i; }` is usually 8 bytes, not 5. A `union` stores all its fields at the same address, so its size is that of its largest field.

A program's memory has regions: the **code** (text), **static/global data**, the **stack** (local variables and function calls, growing and shrinking automatically) and the **heap** (memory obtained by `malloc` and released by `free`). Forgetting `free` causes a **memory leak**; using a pointer after freeing it (a **dangling pointer**) is a bug.

Storage classes: `auto` (default for locals), `static` (lives for the whole program; a `static` local keeps its value between calls), `extern` (declared elsewhere), `register` (a hint).
"""),
)

elab("pds-recursion",
 ("How recursion works", """
A recursive function calls itself on a smaller input. Every correct recursive function has two parts: a **base case**, which returns without calling itself, and a **recursive case**, which reduces the problem towards the base case. Without a base case the calls never stop.

Each call gets its own **stack frame** holding its parameters and local variables. The frames are stacked up as calls go deeper and popped as they return. This is why very deep recursion can overflow the stack.
"""),
 ("Tracing recursive code", """
To trace a recursive function, write the calls as a tree and note what happens *before* the recursive call (pre-order) and *after* it (post-order).

    void f(int n) {
        if (n == 0) return;
        printf("%d ", n);   // before the call
        f(n - 1);
        printf("%d ", n);   // after the call
    }

For `f(3)` this prints `3 2 1 1 2 3`: the first `printf` runs on the way *down*, the second on the way *back up*. Always check which line is before and which after the recursive call.
"""),
 ("Counting calls and recognising patterns", """
The naive Fibonacci function `fib(n) = fib(n-1) + fib(n-2)` makes a number of calls equal to $2F(n+1)-1$, which is exponential. With **memoisation** (remembering results) it makes only $2n-1$ calls.

**Tail recursion** is when the recursive call is the very last thing the function does; a compiler can turn it into a loop. **Mutual recursion** is when two functions call each other.

Classic recursive programs to know: factorial, Fibonacci, GCD (`gcd(a,b) = gcd(b, a % b)`), power by squaring ($x^n=(x^{n/2})^2$), Tower of Hanoi ($2^n-1$ moves), binary search and tree traversals.
"""),
)

elab("pds-arrays-stacks-queues",
 ("Arrays: the foundation", """
An array stores items one after another in memory, so the item at index $i$ is found in constant time by arithmetic on the address. The price: inserting or deleting in the *middle* means shifting all later items, which takes $O(n)$. Arrays are best when you know the size in advance and need fast random access.
"""),
 ("Stacks and queues", """
A **stack** is last-in, first-out (LIFO), like a pile of plates. Its main operations are `push` (add on top), `pop` (remove the top) and `peek`. Stacks are used for function calls, undo operations, expression evaluation and checking balanced brackets. All operations take $O(1)$.

A **queue** is first-in, first-out (FIFO), like people in a line. `enqueue` adds at the rear, `dequeue` removes from the front. Queues are used in scheduling and in breadth-first search.

In an array-based queue, a plain implementation wastes space as the front moves forward. A **circular queue** wraps the indices around using the remainder operator, so the array is reused. With `front` and `rear` indices, a common convention is that the queue is *full* when `(rear + 1) % N == front` and *empty* when `front == rear`, which wastes one cell.
"""),
 ("Deques and priority queues", """
A **deque** (double-ended queue) allows insertion and deletion at both ends. A **priority queue** always removes the element with the highest (or lowest) priority, regardless of arrival order; it is usually built on a **heap**, giving $O(\\log n)$ for insert and delete.

A very common exam topic is **evaluating expressions with a stack**: to evaluate a postfix expression, read tokens left to right, push numbers, and when you read an operator pop two operands, apply it, and push the result. To convert infix to postfix, use a stack for operators, popping those with higher or equal precedence first.
"""),
)

elab("pds-linked-lists",
 ("What a linked list is", """
A linked list stores each item in a separate **node** that holds the data and a **pointer** to the next node. The list is reached through a pointer to its first node, the **head**. Unlike an array, nodes can live anywhere in memory, so inserting a node needs only two pointer changes and no shifting.

The price is that you cannot jump to the $i$-th item; you must walk from the head, so access by position is $O(n)$.
"""),
 ("Variants and the cost of operations", """
- **Singly linked:** each node has `next`.
- **Doubly linked:** each node also has `prev`, so you can walk backwards and delete a given node in $O(1)$.
- **Circular:** the last node points back to the first.

Typical costs for a singly linked list: insert at the head $O(1)$; insert at the tail $O(n)$ unless you keep a tail pointer; delete after a known node $O(1)$; search $O(n)$.

To **reverse** a list, walk through it keeping three pointers (`prev`, `curr`, `next`) and turn each node's `next` to point to the previous node. It takes $O(n)$ time and $O(1)$ extra space.
"""),
 ("Fast and slow pointers", """
Floyd's **tortoise and hare** technique moves one pointer one step at a time and another two steps at a time. If there is a **cycle** the fast pointer eventually catches the slow one; if there is none, the fast pointer reaches the end. To find the **middle** of a list, run both pointers: when the fast one reaches the end, the slow one is at the middle. These tricks use $O(1)$ extra space.
"""),
)

elab("pds-trees-bst-avl",
 ("Trees from the beginning", """
A **tree** is a connected structure with no cycles: one **root** at the top, and every other node has exactly one **parent**. Nodes with no children are **leaves**. The **height** of a tree is the number of edges on the longest path from the root to a leaf. In a **binary tree** each node has at most two children (left and right).

Facts that appear often: a tree with $n$ nodes has $n-1$ edges; a binary tree of height $h$ has at most $2^{h+1}-1$ nodes; and a *full* binary tree with $L$ leaves has $L-1$ internal nodes.
"""),
 ("Traversals and binary search trees", """
Three standard depth-first orders: **preorder** (node, left, right), **inorder** (left, node, right) and **postorder** (left, right, node). Level-order visits the tree layer by layer using a queue.

A **binary search tree (BST)** keeps the rule: every key in the left subtree is smaller than the node, every key in the right subtree is larger. The consequence is that an **inorder traversal prints the keys in sorted order**. Searching, inserting and deleting all follow one path from the root, so they take $O(h)$, where $h$ is the height. In a balanced tree that is $O(\\log n)$, but inserting keys in sorted order into a plain BST creates a chain of height $n-1$ and makes every operation $O(n)$.

Deleting a node with two children: replace it with its **inorder successor** (smallest key in the right subtree) or predecessor, then delete that node.
"""),
 ("Keeping a tree balanced: AVL trees", """
An **AVL tree** is a BST in which for every node the heights of the left and right subtrees differ by at most 1. The **balance factor** is $\\text{height}(\\text{left})-\\text{height}(\\text{right})\\in\\{-1,0,1\\}$. After an insertion or deletion, walk back up; if some node's balance factor becomes $\\pm2$, fix it with **rotations**:

- **LL case** (inserted into the left subtree of the left child): one right rotation.
- **RR case:** one left rotation.
- **LR case:** a left rotation on the child, then a right rotation on the node.
- **RL case:** a right rotation on the child, then a left rotation.

The minimum number of nodes in an AVL tree of height $h$ satisfies $N(h)=N(h-1)+N(h-2)+1$, which makes the height $O(\\log n)$ and all operations $O(\\log n)$.
"""),
)

elab("pds-heaps",
 ("What a heap is", """
A **binary heap** is a *complete* binary tree (every level full except possibly the last, which is filled from the left) in which every node obeys the **heap property**: in a **max-heap** each parent is at least as large as its children; in a **min-heap** each parent is at most as large. The maximum (or minimum) is therefore always at the root.

Because the tree is complete, it is stored in an **array** without pointers. With 0-based indexing, the children of index $i$ are $2i+1$ and $2i+2$, and the parent is $\\lfloor (i-1)/2\\rfloor$.
"""),
 ("Insert, extract and build", """
**Insert.** Put the new element at the end of the array, then **sift up**: swap with its parent while it violates the heap property. The tree has height $\\lfloor\\log_2 n\\rfloor$, so insert takes $O(\\log n)$.

**Extract-max.** Take the root, move the last element to the root, then **sift down**: swap with the larger child until the property holds. $O(\\log n)$.

**Build-heap.** To turn an arbitrary array into a heap, sift down every non-leaf node from the last one back to the root. A careful count shows this costs only $O(n)$, not $O(n\\log n)$, because most nodes are near the bottom and sift only a short way.
"""),
 ("Heap sort and priority queues", """
**Heap sort** builds a max-heap, then repeatedly swaps the root with the last element of the heap, shrinks the heap by one, and sifts down. It takes $O(n\\log n)$ time, uses $O(1)$ extra space, and is not stable.

A heap is the natural implementation of a **priority queue**: insertion and extract-min/max are both $O(\\log n)$, and reading the extreme element is $O(1)$. Heaps are used in Dijkstra's and Prim's algorithms, in finding the $k$ largest elements, and in merging many sorted lists. Searching for an arbitrary key in a heap is $O(n)$ because the heap gives no ordering between siblings.
"""),
)

elab("pds-hashing",
 ("The idea of hashing", """
Suppose you want to store keys and find any of them almost instantly. A **hash table** uses a **hash function** $h(k)$ to turn a key into an array index between $0$ and $m-1$, and stores the key there. A typical simple hash function is $h(k)=k\\bmod m$.

Because there are more possible keys than slots, two keys can map to the same index. This is a **collision**, and every hash table needs a policy for it. The **load factor** is $\\alpha=n/m$, the number of stored keys divided by the number of slots; the lower it is, the fewer collisions.
"""),
 ("Collision resolution: chaining", """
In **separate chaining**, each slot holds a linked list of all keys that hash to it. Inserting is $O(1)$ (add to the front); searching means scanning one chain, whose expected length is $\\alpha$. Under uniform hashing, an unsuccessful search takes about $1+\\alpha$ probes and a successful one about $1+\\alpha/2$. The table can hold more keys than slots ($\\alpha>1$).
"""),
 ("Collision resolution: open addressing", """
In **open addressing** every key is stored in the table itself, so $\\alpha\\le1$. If the slot is taken, we **probe** other slots in a fixed sequence:

- **Linear probing:** try $h(k),\\,h(k)+1,\\,h(k)+2,\\dots$ (mod $m$). Simple, but creates long runs of filled slots (*primary clustering*).
- **Quadratic probing:** try $h(k)+1^2,\\,h(k)+2^2,\\dots$. Reduces primary clustering.
- **Double hashing:** the step size comes from a second hash function, $h_1(k)+i\\,h_2(k)$.

**Deleting** in open addressing needs care: simply emptying a slot would break the probe sequence for keys inserted after it, so deleted slots are marked with a special "deleted" tombstone. The average cost of a search degrades sharply as $\\alpha$ approaches 1.
"""),
)

elab("pds-graph-representation",
 ("Two ways to store a graph", """
To process a graph in a program we must store its vertices and edges. The two standard representations differ in what they make easy.

**Adjacency matrix.** A $V\\times V$ table where entry $[i][j]$ is 1 (or the weight) if there is an edge from $i$ to $j$. Checking whether an edge exists takes $O(1)$; listing the neighbours of a vertex takes $O(V)$; the memory is $\\Theta(V^2)$ whatever the number of edges. For an undirected graph the matrix is symmetric.
"""),
 ("Adjacency lists and edge lists", """
**Adjacency list.** For each vertex, a list of its neighbours. Memory is $\\Theta(V+E)$. Listing the neighbours of $v$ takes time proportional to its degree; checking one specific edge takes $O(\\deg v)$. In an undirected graph each edge appears twice (once in each endpoint's list).

**Edge list.** Just a list of all edges. It is compact and is exactly what Kruskal's algorithm needs (sort the edges), but finding the neighbours of a vertex requires scanning everything.
"""),
 ("Choosing a representation", """
- **Sparse graph** ($E$ much smaller than $V^2$): use adjacency lists. BFS and DFS then take $O(V+E)$.
- **Dense graph** ($E$ close to $V^2$) or when you need constant-time edge lookups: use the matrix. BFS and DFS take $O(V^2)$ with a matrix.
- The number of edges in a simple undirected graph is at most $\\frac{V(V-1)}{2}$, so a complete graph is as dense as it can be.
- For the matrix of an undirected graph, the sum of a row equals the degree of that vertex; for a directed graph, row sums give out-degrees and column sums give in-degrees.
"""),
)
