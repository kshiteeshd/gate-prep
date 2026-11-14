"""Extra, step-by-step textbook sections for Programming & Data Structures and Algorithms."""
from learn import elab

# ------------------------------------------------------------------ PDS
elab("pds-recursion",
 ("Following one call all the way down and back", r"""
Every recursive call gets its **own stack frame** holding its parameters, local variables and a return address. A call is *paused* at the line where it calls itself and resumes only when the inner call returns. To trace, draw the frames as a stack: push on each call, pop on each return.

Take `int f(int n){ if(n==0) return 0; return n + f(n-1); }` with `f(3)`:

    f(3): needs 3 + f(2)
      f(2): needs 2 + f(1)
        f(1): needs 1 + f(0)
          f(0): returns 0          <- base case, deepest frame
        f(1): returns 1 + 0 = 1
      f(2): returns 2 + 1 = 3
    f(3): returns 3 + 3 = 6

Two phases appear in every recursion. On the way **down** the code *before* the recursive call runs; on the way **up** the code *after* it runs. That is why printing before the call lists values in call order, while printing after the call lists them in reverse.

    void p(int n){ if(n==0) return; printf("%d ", n); p(n-1); }   // 3 2 1
    void q(int n){ if(n==0) return; q(n-1); printf("%d ", n); }   // 1 2 3
"""),
 ("Counting calls, depth and cost", r"""
Three numbers are often confused. The **depth** is the longest chain of pending frames, which decides stack space. The **number of calls** is the size of the recursion tree, which decides time. The **work per call** is what each frame does besides recursing.

For $f(n)=f(n-1)+1$ the tree is a single chain: $n+1$ calls, depth $n+1$, space $O(n)$. For the naive Fibonacci $F(n)=F(n-1)+F(n-2)$ the tree branches, so the calls number $2F(n+1)-1\approx\varphi^{n}$, but the depth is still only $n$, so space stays $O(n)$ while time is exponential. The reason is repeated work: $F(3)$ is recomputed inside both $F(5)$ and $F(4)$. Storing results (memoisation) cuts the tree to $n+1$ distinct calls.

| Recursion | Calls | Depth | Time | Stack space |
|---|---|---|---|---|
| `f(n-1)` one call, O(1) work | $n$ | $n$ | $O(n)$ | $O(n)$ |
| `f(n/2)` one call | $\log n$ | $\log n$ | $O(\log n)$ | $O(\log n)$ |
| `f(n-1)+f(n-2)` | $\approx1.6^n$ | $n$ | $O(1.6^n)$ | $O(n)$ |
| `f(n/2)+f(n/2)`, O(n) merge | $2n-1$ | $\log n$ | $O(n\log n)$ | $O(\log n)$ |
"""),
 ("Tail recursion, infinite recursion and the usual traps", r"""
A call is a **tail call** if nothing remains to be done after it returns: `return g(n-1, acc*n);` is tail recursive, `return n * g(n-1);` is not (the multiplication waits). A compiler may reuse the frame for tail calls, turning recursion into a loop with $O(1)$ stack. C compilers are *allowed* but not required to do so.

Check three things before trusting any recursive function. (1) A **base case** exists and is reachable. (2) Every call moves its argument **towards** the base case (`n-1`, `n/2`), never away. (3) The return value is **used**: a recursive call whose result is dropped does nothing useful. Missing a base case, or recursing on `n+1` while testing `n==0`, overflows the stack.

Watch variables with `static` storage or globals inside recursion: they are shared by all frames, unlike locals. A classic output question is `static int c=0; ... c++;` where every frame sees the same `c`.
"""),
)

elab("pds-linked-lists",
 ("Pointer surgery, one picture at a time", r"""
Most list questions come down to rewiring `next` pointers in the right order. Always **save what you are about to lose before overwriting a pointer**.

*Insert after node `p`:* new node `n`.

    n->next = p->next;   // step 1: n takes over p's successor
    p->next = n;         // step 2: p now points to n

Swapping the two lines loses the rest of the list, because `p->next` would be overwritten before it was copied.

*Delete the node after `p`:*

    t = p->next;  p->next = t->next;  free(t);

*Delete a node when you hold only its pointer `x` (and it is not the tail):* copy the successor's data into `x`, then delete the successor. This is $O(1)$, and it works because we change what the node *contains* rather than which node is linked.

    x->data = x->next->data;  t = x->next;  x->next = t->next;  free(t);

Always handle three special cases: the **empty list**, the **head** (insert or delete at position 0 changes the head pointer itself, so you need `*head` or a returned pointer) and the **tail** (`next == NULL`).
"""),
 ("Reversing a list: the three-pointer walk", r"""
Reversal keeps three names: `prev`, `cur`, `nxt`. At each step save `cur->next`, flip the link, then slide all three pointers one place right.

    prev = NULL; cur = head;
    while (cur) { nxt = cur->next; cur->next = prev; prev = cur; cur = nxt; }
    head = prev;

Trace on `1 -> 2 -> 3`:

| step | prev | cur | list after the flip |
|---|---|---|---|
| start | NULL | 1 | 1→2→3 |
| 1 | 1 | 2 | 1→NULL, 2→3 |
| 2 | 2 | 3 | 2→1→NULL, 3 |
| 3 | 3 | NULL | 3→2→1→NULL |

Time $O(n)$, extra space $O(1)$. The recursive version reverses the tail first and then makes `head->next->next = head`; it uses $O(n)$ stack.
"""),
 ("Slow and fast pointers, and what each operation costs", r"""
Moving `slow` one step and `fast` two steps per iteration gives three tricks. **Middle node:** when `fast` reaches the end, `slow` is at the middle (the second middle for even length). **Cycle detection (Floyd):** if there is a loop, `fast` eventually laps `slow` and they meet; if not, `fast` hits NULL. **Cycle start:** after they meet, put one pointer back at the head and move both one step at a time; they meet again exactly at the first node of the cycle.

| Operation | Singly | Doubly | Circular, tail pointer kept |
|---|---|---|---|
| Insert at head | $O(1)$ | $O(1)$ | $O(1)$ |
| Insert at tail | $O(n)$ (or $O(1)$ with tail pointer) | $O(1)$ with tail | $O(1)$ |
| Delete given a pointer to the node | $O(n)$ (need predecessor) | $O(1)$ | $O(n)$ |
| Search | $O(n)$ | $O(n)$ | $O(n)$ |
| Access the $i$-th element | $O(i)$ | $O(i)$ | $O(i)$ |

Linked lists win on cheap insertion and deletion at a known position and lose on random access and cache behaviour. Each node also costs one extra pointer (two in a doubly linked list).
"""),
)

elab("pds-arrays-stacks-queues",
 ("Index arithmetic you must be able to do blindly", r"""
In C an array of $n$ elements is a block of consecutive memory. With base address $B$ and element size $w$ bytes, the address of `A[i]` is $B+i\cdot w$ for 0-based indexing, or $B+(i-L)\cdot w$ when the lower bound is $L$. A 2-D array `A[R][C]` in **row-major** order places `A[i][j]` at $B+(i\cdot C+j)\cdot w$; **column-major** uses $B+(j\cdot R+i)\cdot w$. Example: base 1000, 4-byte ints, `A[5][8]`, element `A[2][3]` sits at $1000+(2\cdot8+3)\cdot4=1076$.

Remember that `A[i]` means `*(A+i)`, and pointer addition scales by the element size. Hence `i[A]` is legal, `A+1` skips one element, and `&A[3]-&A[0]` equals 3 (elements, not bytes).
"""),
 ("Stack: last in, first out, with traces", r"""
Push and pop work at one end only, so all operations are $O(1)$. A stack has a natural partner in anything that must be undone in reverse order.

**Balanced brackets:** push each opener; on a closer, the top must be its matching opener. The string is balanced iff every closer matched and the stack is empty at the end.

**Postfix evaluation:** scan left to right; push operands; on an operator pop *two* values (the first popped is the **right** operand), apply, push the result. For `5 3 2 * + 4 -`:

    push 5, 3, 2     ->  [5 3 2]
    *  : 3*2 = 6     ->  [5 6]
    +  : 5+6 = 11    ->  [11]
    push 4           ->  [11 4]
    -  : 11-4 = 7    ->  [7]      answer 7

**Infix to postfix:** operands go straight to the output; an operator first pops every stack operator of **higher or equal** precedence (for left-associative operators), then is pushed; `(` is pushed, `)` pops until the matching `(`. At the end pop everything. `a+b*c` becomes `abc*+` because `*` stays above `+`.

**Stack permutations:** with input 1, 2, 3 pushed in order, the outputs possible are all permutations except those that need an element to jump the queue; for $n$ elements the count is the Catalan number $\frac{1}{n+1}\binom{2n}{n}$ (5 for $n=3$; the impossible one is 3 1 2).
"""),
 ("Queues: circular arrays and the full/empty puzzle", r"""
A queue is first in, first out: enqueue at the rear, dequeue from the front. A plain array wastes space as `front` creeps forward, so use a **circular** array of size $N$ with `front` and `rear` updated modulo $N$.

The difficulty is telling **full** from **empty**, since in both cases `front` and `rear` can look alike. Three standard fixes: keep a count; leave one slot unused, so the queue is *full* when `(rear+1) % N == front` and *empty* when `front == rear` (capacity is then $N-1$); or use a flag. GATE questions nearly always use the "one slot empty" convention, so check which one is stated.

**Queue using two stacks:** push onto stack 1; to dequeue, if stack 2 is empty move everything from stack 1 to stack 2 (reversing the order), then pop stack 2. Each element moves at most twice, so the **amortised** cost per operation is $O(1)$ although a single dequeue can cost $O(n)$. **Stack using two queues** needs either an $O(n)$ push or an $O(n)$ pop.
"""),
)

elab("pds-heaps",
 ("Seeing a heap as an array", r"""
A binary heap is a **complete** binary tree stored level by level in an array. With 1-based indexing the parent of $i$ is $\lfloor i/2\rfloor$ and the children are $2i$ and $2i+1$ (with 0-based indexing use $\lfloor(i-1)/2\rfloor$, $2i+1$, $2i+2$). In a **max-heap** every node is $\ge$ its children, so the maximum is at index 1; a min-heap is the mirror. Note that a heap is **not sorted**: only the parent–child order is guaranteed, siblings may be in any order.

Useful facts: height is $\lfloor\log_2 n\rfloor$; there are $\lceil n/2\rceil$ leaves, occupying indices $\lfloor n/2\rfloor+1\ldots n$; and a heap with $n$ elements has $\lfloor n/2\rfloor$ internal nodes. The largest element is the root, the smallest is some leaf, and the second largest is a child of the root.
"""),
 ("Insert, extract and build, traced", r"""
**Insert** places the new key in the first free slot and **sifts up** while it is larger than its parent (max-heap). Insert 8 into the max-heap `[10, 6, 9, 3, 5]`:

    [10 6 9 3 5 8]   8 at index 6, parent is index 3 (value 9)
    8 < 9, so it stays.   result [10 6 9 3 5 8]

Insert 12 instead: it swaps with 9, then with 10, giving `[12 6 10 3 5 9]`. Cost is at most the height: $O(\log n)$.

**Extract-max** removes the root, moves the **last** element to the root and **sifts down**, swapping with the *larger* child each time. From `[10 6 9 3 5]`: take 10, move 5 to the root, `[5 6 9 3]`; larger child of 5 is 9, swap: `[9 6 5 3]`. Cost $O(\log n)$.

**Build-heap** calls sift-down on nodes $\lfloor n/2\rfloor$ down to 1 (leaves are already heaps). It costs $O(n)$, not $O(n\log n)$, because most nodes are near the bottom and sift only a short way: $\sum_h \frac{n}{2^{h+1}}\cdot h=O(n)$. Inserting $n$ elements one by one does cost $\Theta(n\log n)$ in the worst case.
"""),
 ("Operations cost table and the typical exam moves", r"""
| Operation | Binary heap |
|---|---|
| Find max (min-heap: find min) | $O(1)$ |
| Insert | $O(\log n)$ |
| Extract root | $O(\log n)$ |
| Increase or decrease key (position known) | $O(\log n)$ |
| Delete an arbitrary element (position known) | $O(\log n)$ |
| Search for a given value | $O(n)$ |
| Build from $n$ keys | $O(n)$ |
| Find the $k$-th largest with a size-$k$ min-heap | $O(n\log k)$ |

**Heap sort:** build a max-heap, then repeat: swap root with the last element, shrink the heap by one, sift down. Always $\Theta(n\log n)$, in place, not stable. **Typical question:** "after inserting these keys one by one, what is the array?" Do each insertion with its sift-up; the result depends on the order of insertion, whereas build-heap on the same keys can give a different valid array.
"""),
)

elab("pds-graph-representation",
 ("The same graph, three ways", r"""
Take vertices 0–3 and edges 0–1, 0–2, 1–2, 2–3 (undirected).

**Adjacency matrix** $M$ is $V\times V$ with $M[i][j]=1$ when an edge exists.

    0 1 1 0
    1 0 1 0
    1 1 0 1
    0 0 1 0

Undirected graphs give a **symmetric** matrix with a zero diagonal (no self-loops). Row sums give degrees; for a directed graph row sums give out-degrees and column sums in-degrees.

**Adjacency list** stores, for each vertex, the list of its neighbours: `0:[1,2] 1:[0,2] 2:[0,1,3] 3:[2]`. **Edge list** is just the set of pairs `(0,1),(0,2),(1,2),(2,3)`.
"""),
 ("Costs, and which representation to choose", r"""
| Question | Matrix | Adjacency list |
|---|---|---|
| Space | $\Theta(V^2)$ | $\Theta(V+E)$ |
| Is there an edge $(u,v)$? | $O(1)$ | $O(\deg u)$ |
| List all neighbours of $u$ | $O(V)$ | $O(\deg u)$ |
| Visit every edge (BFS/DFS) | $O(V^2)$ | $O(V+E)$ |
| Add an edge | $O(1)$ | $O(1)$ |
| Remove an edge | $O(1)$ | $O(\deg u)$ |

A graph is **sparse** if $E=O(V)$ and **dense** if $E=\Theta(V^2)$. Use lists for sparse graphs (most real graphs), the matrix for dense graphs or when constant-time edge tests dominate (Floyd–Warshall works naturally on a matrix). Remember the edge counts: a simple undirected graph has at most $\frac{V(V-1)}{2}$ edges, a simple directed graph at most $V(V-1)$, and a tree has exactly $V-1$. In an adjacency list of an undirected graph each edge appears **twice**, so the total list length is $2E$.
"""),
 ("Matrix tricks that show up in questions", r"""
The entry $(i,j)$ of $M^k$ counts the **walks of length $k$** from $i$ to $j$; the diagonal of $M^3$ gives twice the number of triangles through each vertex in an undirected graph. A directed graph is acyclic exactly when a topological order exists, equivalently when the matrix can be permuted to be strictly upper triangular. The **transpose** of a directed graph (all arcs reversed) has matrix $M^T$ and is used in Kosaraju's SCC algorithm; building it from adjacency lists takes $O(V+E)$.
"""),
)

elab("pds-pointers-memory",
 ("Reading pointer code without fear", r"""
Treat a pointer as an integer holding an **address**; the type tells the compiler how many bytes a dereference reads and how far `p+1` moves. Declare `int x=5; int *p=&x;`. Then `*p` is `x` itself, `p` is the address of `x`, `&p` is the address of the pointer variable, and `*p=9` changes `x`.

Pointer arithmetic is scaled: for `int *p` at address 1000 and 4-byte ints, `p+3` is 1012 and `(p+3)-p` is 3. Two pointers into the same array can be subtracted; the result counts **elements**.

Precedence trips people up: `*p++` reads `*(p++)` (use the old value, then move the pointer), `(*p)++` increments the pointee, `*++p` moves first then reads. Trace `int a[]={10,20,30}; int *p=a; printf("%d %d", *p++, *p);` carefully: the order of argument evaluation is unspecified, so well-posed exam questions avoid it.
"""),
 ("Passing by value, and how swap really works", r"""
C passes arguments **by value**. `void swap(int a,int b)` swaps copies and leaves the caller untouched. To change the caller's variables pass their addresses and dereference:

    void swap(int *a, int *b){ int t=*a; *a=*b; *b=t; }   // call swap(&x,&y)

The same idea explains why `scanf` needs `&x`, why an array parameter really receives a pointer (`sizeof` inside the function gives the pointer size, not the array size), and why a function returning the address of a local variable is a bug: the frame is gone after return, leaving a **dangling pointer**.

**Memory regions.** Code, global/static data (initialised to 0 by default), the **stack** (locals, grows per call), and the **heap** (`malloc`/`free`, lives until freed). Forgetting `free` is a **leak**, using memory after `free` is a dangling pointer, and `free`-ing twice is undefined behaviour. `malloc` returns uninitialised memory; `calloc` zeroes it.
"""),
 ("Arrays, strings and double pointers", r"""
A string is a `char` array ending with `'\0'`; `strlen` does not count the terminator but `sizeof` of a char array does. For `char s[]="hello";` `sizeof(s)` is 6 and `strlen(s)` is 5, while for `char *s="hello";` `sizeof(s)` is the size of a pointer. String literals must not be modified.

For `int a[3][4]`, `a[i]` is a one-dimensional array of 4 ints, `a[i][j]` is `*(*(a+i)+j)`, and `a+1` moves a whole **row** (16 bytes with 4-byte ints). A `int **pp` can hold the address of a pointer; `**pp` reaches the value. Use it when a function must change **which object a pointer points to**, for example inserting at the head of a list.
"""),
)

elab("pds-c-operators-bits",
 ("Evaluation order, in detail", r"""
Precedence says which operator **binds** tighter; associativity breaks ties among equals; neither says which operand is **evaluated** first. From highest to lowest, the groups to remember: postfix `() [] -> . ++ --`; unary `! ~ ++ -- + - * & sizeof`; `* / %`; `+ -`; shifts `<< >>`; relational `< <= > >=`; equality `== !=`; `&`; `^`; `|`; `&&`; `||`; `?:`; assignment; comma. Unary and assignment operators associate right to left, the rest left to right.

Hence `a & b == c` is `a & (b == c)`, a notorious trap, and `a+b<<c` is `(a+b)<<c`. The **short-circuit** operators `&&` and `||` do guarantee left-to-right evaluation and skip the right operand when the result is already known: `if (x != 0 && 10/x > 1)` is safe, and in `i++ || j++` the right side runs only when `i` was 0. Modifying a variable twice between sequence points, as in `i = i++ + ++i`, is undefined: GATE questions that print a definite answer avoid it, or ask for the compiler-independent rule.
"""),
 ("Integer arithmetic: division, overflow and conversions", r"""
Integer division truncates **towards zero**: `7/2` is 3, `-7/2` is -3, and `%` takes the sign of the dividend, so `-7%3` is -1. Mixed expressions convert to the wider type, so `5/2` is 2 but `5/2.0` is 2.5, and `(float)(5/2)` is still 2.0. Characters are small integers: `'a'+1` is 98 and `'a'-'A'` is 32.

For a $k$-bit **two's-complement** signed integer the range is $-2^{k-1}\ldots 2^{k-1}-1$. The negative of $x$ is `~x+1`. A signed overflow is undefined in C; unsigned arithmetic wraps modulo $2^k$. Converting a negative signed value to unsigned adds $2^k$: `(unsigned char)-1` is 255. Comparing a signed with an unsigned value converts the signed one first, so `-1 < 1u` is **false**.
"""),
 ("Bit tricks you can compute by hand", r"""
Work in binary, aligning the columns. `12 & 10`: `1100 & 1010 = 1000 = 8`; `12 | 10 = 1110 = 14`; `12 ^ 10 = 0110 = 6`. A left shift by $k$ multiplies by $2^k$ (until overflow); a right shift divides by $2^k$ rounding down for non-negative numbers.

| Goal | Expression |
|---|---|
| Test bit $i$ | `(x >> i) & 1` |
| Set bit $i$ | `x \| (1<<i)` |
| Clear bit $i$ | `x & ~(1<<i)` |
| Toggle bit $i$ | `x ^ (1<<i)` |
| Clear the lowest set bit | `x & (x-1)` |
| Isolate the lowest set bit | `x & -x` |
| Is $x$ a power of two? | `x>0 && (x&(x-1))==0` |
| Swap without a temp | `a^=b; b^=a; a^=b;` |

Counting set bits by repeating `x &= x-1` until zero takes exactly as many iterations as there are 1-bits (Kernighan's method), which is the usual loop-count question.
"""),
)

elab("pds-trees-bst-avl",
 ("Traversals traced on one tree", r"""
Take the BST built by inserting 50, 30, 70, 20, 40, 60, 80:

          50
        /    \
      30      70
     /  \    /  \
    20  40  60  80

**Inorder** (left, root, right): 20 30 40 50 60 70 80, sorted, as always for a BST. **Preorder** (root, left, right): 50 30 20 40 70 60 80. **Postorder** (left, right, root): 20 40 30 60 80 70 50. **Level order** uses a queue: 50 30 70 20 40 60 80.

To rebuild a tree from two traversals you need the inorder plus either preorder or postorder: the preorder's first element (or postorder's last) is the root, and its position in the inorder splits left from right. Preorder and postorder alone do not determine a tree in general (they do for a *full* binary tree). The number of distinct binary trees with $n$ nodes is the Catalan number $C_n$.
"""),
 ("BST operations: search, insert and delete, step by step", r"""
Search and insert follow one path from the root, going left when the key is smaller and right when larger: cost $O(h)$, where $h$ is the height. For $n$ nodes $h$ ranges from $\lfloor\log_2 n\rfloor$ (balanced) to $n-1$ (inserting sorted keys makes a chain).

**Delete** has three cases. A **leaf** is simply removed. A node with **one child** is replaced by that child. A node with **two children** is replaced by its **inorder successor** (the smallest key in its right subtree) or its inorder predecessor, and then that node is deleted instead. In the tree above, deleting 50 copies 60 into the root and removes the old 60 leaf, giving the root 60 with left subtree 30 and right subtree 70 (children 80 only).

Useful identities: the minimum is the leftmost node, the maximum the rightmost; the successor of a node with a right child is the leftmost node of that right subtree, otherwise the first ancestor whose left subtree contains it.
"""),
 ("AVL rotations, one case at a time", r"""
An AVL tree keeps $|h(\text{left})-h(\text{right})|\le1$ at every node, which forces $h<1.44\log_2 n$. After an insertion, walk up to the first node whose **balance factor** becomes $\pm2$ and fix it with one of four cases (named by where the new key went relative to the unbalanced node $z$):

| Case | Shape | Fix |
|---|---|---|
| Left–Left | new key in left subtree of the left child | single **right** rotation at $z$ |
| Right–Right | right subtree of the right child | single **left** rotation at $z$ |
| Left–Right | right subtree of the left child | left rotation at the child, then right rotation at $z$ |
| Right–Left | left subtree of the right child | right rotation at the child, then left rotation at $z$ |

Example: insert 10, 20, 30. After 30 the node 10 has balance $-2$ with a right–right shape, so rotate left: 20 becomes the root with children 10 and 30. Insert 30, 10, 20 instead: 30 has a left child 10 whose right child is 20 (left–right). Rotate 10 left, which makes 30–20–10 a straight left line, then rotate 30 right: again 20 becomes the root with children 10 and 30.

The **minimum number of nodes** in an AVL tree of height $h$ obeys $N(h)=N(h-1)+N(h-2)+1$ with $N(0)=1,\ N(1)=2$, giving 1, 2, 4, 7, 12, 20, ...; the **maximum** is the perfect tree, $2^{h+1}-1$. Insertion needs at most one rotation (single or double); deletion may need $O(\log n)$ of them.
"""),
)

elab("pds-hashing",
 ("A hash table traced by hand", r"""
Insert keys 12, 25, 35, 26, 15 into a table of size 10 with $h(k)=k\bmod10$ and **chaining**:

    index 2: 12
    index 5: 25 -> 35 -> 15      (new items go to the head or tail: read the question)
    index 6: 26

The **load factor** is $\alpha=n/m$. With chaining and uniform hashing an unsuccessful search examines about $\alpha$ items and a successful one about $1+\alpha/2$; both are $O(1)$ when $\alpha$ is a constant. A table can have $\alpha>1$ with chaining but never with open addressing.

A good hash function is fast, spreads keys uniformly, and ideally uses all of the key. Table sizes that are **primes** not close to a power of 2 reduce clustering for the division method; `k mod 10` throws away all but the last digit, which is why patterns in the data hurt.
"""),
 ("Open addressing: linear, quadratic and double hashing", r"""
All keys live in the table itself; on a collision we **probe** a sequence of slots. Same keys, size 10, **linear probing** $h(k,i)=(k+i)\bmod10$:

| Insert | Probes | Placed at |
|---|---|---|
| 12 | 2 | 2 |
| 25 | 5 | 5 |
| 35 | 5, 6 | 6 |
| 26 | 6, 7 | 7 |
| 15 | 5, 6, 7, 8 | 8 |

Notice the **primary clustering**: a long run of occupied cells grows faster the longer it is. **Quadratic probing** $h(k)+c_1i+c_2i^2$ avoids that but suffers a milder secondary clustering and may not reach every slot unless the table size and constants are chosen well (a prime size and $\alpha<\tfrac12$ is safe). **Double hashing** $h_1(k)+i\cdot h_2(k)$ has the best spread; $h_2(k)$ must never be 0 and should be coprime with the table size.

**Deletion** in open addressing cannot just empty the slot, because later searches stop at an empty cell. Mark it **deleted** (a tombstone): searches skip it, insertions may reuse it. Expected probes for an unsuccessful search are about $\frac1{1-\alpha}$, and for a successful one $\frac1\alpha\ln\frac1{1-\alpha}$.
"""),
)

# ------------------------------------------------------------------ ALGO
elab("algo-complexity-classes",
 ("What P, NP, NP-hard and NP-complete actually mean", r"""
A **decision problem** has a yes/no answer. **P** is the set solvable by a deterministic algorithm in polynomial time. **NP** is the set whose "yes" answers can be **verified** in polynomial time given a certificate (a proposed solution): checking that a list of cities is a tour of length $\le L$ is easy, finding one may not be. Every problem in P is in NP, so $P\subseteq NP$; whether $P=NP$ is open.

A problem is **NP-hard** if every problem in NP reduces to it in polynomial time; it need not itself be in NP. It is **NP-complete** if it is both in NP and NP-hard. So NP-complete problems are the hardest problems *inside* NP, and a polynomial algorithm for any one of them would give $P=NP$.

    NP-complete = NP  ∩  NP-hard          P ⊆ NP        NP-complete ⊆ NP

The halting problem is NP-hard but not in NP (it is undecidable), which is the standard example separating NP-hard from NP-complete.
"""),
 ("Reductions: the direction matters", r"""
$A\le_p B$ ("$A$ reduces to $B$") means we can transform any instance of $A$ into an instance of $B$ in polynomial time so that the answers agree. Read it as "$B$ is at least as hard as $A$". Two consequences are used constantly. If $B$ is in P then $A$ is in P. If $A$ is NP-hard then $B$ is NP-hard.

To prove a new problem $X$ is NP-complete: (1) show $X\in NP$ by describing a polynomial-time verifier; (2) pick a **known** NP-complete problem $Y$ and show $Y\le_p X$. Getting the direction wrong is the classic mistake: reducing $X$ to $Y$ proves nothing about $X$'s hardness.

The chain to remember: **SAT** is NP-complete (Cook–Levin) $\to$ **3-SAT** $\to$ **Independent set / Clique / Vertex cover** $\to$ **Hamiltonian cycle** $\to$ **Travelling salesman (decision)**; also **Subset sum**, **0/1 knapsack (decision)** and **Graph colouring ($k\ge3$)**. Note that **2-SAT is in P**, 2-colouring is in P (bipartiteness), and finding a shortest path or MST is in P even though the longest simple path is NP-hard.
"""),
 ("Exam checklist for the classes", r"""
| Statement | Verdict |
|---|---|
| Every problem in P is in NP | True |
| Every NP-complete problem is NP-hard | True |
| If one NP-complete problem is in P then $P=NP$ | True |
| NP means "not polynomial" | False: it means *nondeterministic polynomial* |
| Sorting is in NP-complete | False (it is in P) |
| A problem in NP is solvable in exponential time by brute force | True |
| $P=NP$ is proved | False: open |

When a question gives you a new problem and a reduction, first work out which direction it goes, then decide what it proves: a reduction **from** an NP-complete problem **to** $X$ shows $X$ is NP-hard; a reduction **from** $X$ to a problem in P shows $X$ is in P.
"""),
)

elab("algo-asymptotics",
 ("Counting loops carefully", r"""
Count how many times the innermost statement runs, then simplify. A single loop `for(i=1;i<=n;i++)` runs $n$ times. **Nested independent loops** multiply: $n\cdot m$. **A dependent inner loop** needs a sum: `for(i=1;i<=n;i++) for(j=1;j<=i;j++)` runs $1+2+\dots+n=\frac{n(n+1)}2=\Theta(n^2)$.

**Multiplicative steps** give logarithms: `for(i=1;i<n;i*=2)` runs $\lceil\log_2n\rceil$ times, since $i$ takes the values $1,2,4,\dots$. Halving `while(n>1) n/=2` is the same. A loop with `i*=i` (squaring) grows like $\log\log n$ iterations.

**Mixed:** `for(i=1;i<=n;i++) for(j=1;j<=n;j+=i)` costs $\sum_{i=1}^{n}\frac ni=n\,H_n=\Theta(n\log n)$, the harmonic series. And `for(i=1;i<=n;i*=2) for(j=1;j<=i;j++)` costs $1+2+4+\dots+n\approx2n=\Theta(n)$ because the geometric series is dominated by its last term.
"""),
 ("Ordering functions by growth", r"""
The standard ladder, slow to fast: $1<\log\log n<\log n<\sqrt n<n<n\log n<n^2<n^3<2^n<n!<n^n$. Polylogarithms beat nothing polynomial: $(\log n)^k=o(n^\epsilon)$ for every $\epsilon>0$, and every polynomial is $o(c^n)$ for $c>1$.

To compare two messy functions, take the **limit of the ratio** $f/g$: $0$ means $f=o(g)$, a finite positive constant means $f=\Theta(g)$, $\infty$ means $f=\omega(g)$. Or take logarithms: $2^{\sqrt{\log n}}$ against $n$: $\sqrt{\log n}$ against $\log n$, so $n$ grows faster. Also remember $\log(n!)=\Theta(n\log n)$ by Stirling, $n^{\log n}$ is faster than any polynomial but slower than $2^n$, and constant bases in logs never matter inside $O(\cdot)$, though exponents do: $2^{2n}=4^n\ne\Theta(2^n)$.
"""),
 ("Best, worst and average, and what each notation claims", r"""
Big-O, Big-$\Omega$ and Big-$\Theta$ are statements about **functions**, not about cases. "The running time of insertion sort is $O(n^2)$" is a worst-case upper bound; "it is $\Omega(n)$" is true for the best case; "its worst case is $\Theta(n^2)$" is tight. Saying "Big-O is the worst case" mixes up two independent ideas: you can state an upper bound for the best case as well.

Quick properties that settle many options: $f=\Theta(g)\iff f=O(g)\wedge f=\Omega(g)$; transitivity holds for all notations; symmetry holds only for $\Theta$; $f=O(g)\iff g=\Omega(f)$; and $O(f)+O(g)=O(\max(f,g))$. If $f=O(g)$ it is **not** automatically true that $2^{f}=O(2^{g})$ (take $f=2n,g=n$).
"""),
)

elab("algo-recurrences-dc",
 ("Solving a recurrence by expanding it", r"""
Expansion (unrolling) is the most reliable method. Solve $T(n)=2T(n/2)+n$, $T(1)=1$:

    T(n) = 2T(n/2) + n
         = 2[2T(n/4) + n/2] + n    = 4T(n/4) + 2n
         = 4[2T(n/8) + n/4] + n... = 8T(n/8) + 3n
         ...
         = 2^k T(n/2^k) + k n

Stop when $n/2^k=1$, i.e. $k=\log_2n$: $T(n)=n\cdot1+n\log_2n=\Theta(n\log n)$. Each level of the recursion tree does $n$ work in total, and there are $\log n$ levels. Drawing the **recursion tree** and summing per level is the same idea: for $T(n)=3T(n/2)+n$ level $i$ costs $(3/2)^in$, a growing geometric series dominated by the last level, giving $\Theta(n^{\log_23})$.

Linear recurrences with subtraction expand the other way: $T(n)=T(n-1)+n$ gives $\frac{n(n+1)}2=\Theta(n^2)$; $T(n)=2T(n-1)+1$ gives $2^n-1$, because each unit of $n$ doubles the work (Tower of Hanoi).
"""),
 ("Master theorem as a comparison of two forces", r"""
For $T(n)=aT(n/b)+f(n)$ compute the **watershed** $n^{\log_ba}$, which is the total work done at the leaves, and compare it with $f(n)$, the work at the root.

| Comparison | Who wins | Result |
|---|---|---|
| $f(n)=O(n^{\log_ba-\epsilon})$ | leaves | $\Theta(n^{\log_ba})$ |
| $f(n)=\Theta(n^{\log_ba}\log^kn)$, $k\ge0$ | tie | $\Theta(n^{\log_ba}\log^{k+1}n)$ |
| $f(n)=\Omega(n^{\log_ba+\epsilon})$ and $af(n/b)\le cf(n)$, $c<1$ | root | $\Theta(f(n))$ |

Examples. $T=4T(n/2)+n$: $n^{2}$ against $n$, leaves win, $\Theta(n^2)$. $T=2T(n/2)+n$: $n$ against $n$, tie, $\Theta(n\log n)$. $T=2T(n/2)+n^2$: root wins, $\Theta(n^2)$. $T=2T(n/2)+n\log n$: $n\log n$ is **not** polynomially larger than $n$, so case 3 fails, but the extended case 2 with $k=1$ gives $\Theta(n\log^2n)$. The theorem does **not** apply when $a$ is not a constant ($2^nT(n/2)$), when $a<1$, or when $f(n)$ is not positive (such as $T=T(n/2)-n$), or when subproblems are different sizes (use a recursion tree: $T(n)=T(n/3)+T(2n/3)+n$ is $\Theta(n\log n)$).
"""),
)

elab("algo-sorting-searching",
 ("Quick comparison table, with the reasons", r"""
| Algorithm | Best | Average | Worst | Extra space | Stable |
|---|---|---|---|---|---|
| Bubble (with early exit) | $n$ | $n^2$ | $n^2$ | 1 | yes |
| Selection | $n^2$ | $n^2$ | $n^2$ | 1 | no |
| Insertion | $n$ | $n^2$ | $n^2$ | 1 | yes |
| Merge | $n\log n$ | $n\log n$ | $n\log n$ | $n$ | yes |
| Quick (last-element pivot) | $n\log n$ | $n\log n$ | $n^2$ | $\log n$ stack | no |
| Heap | $n\log n$ | $n\log n$ | $n\log n$ | 1 | no |
| Counting (keys $0..k$) | $n+k$ | $n+k$ | $n+k$ | $k$ | yes |
| Radix ($d$ digits) | $d(n+k)$ | same | same | $n+k$ | yes |

**Why the extremes behave as they do.** Insertion sort does work proportional to the number of **inversions** (pairs out of order), so a sorted array costs $n$ and a reversed one $\frac{n(n-1)}2$ inversions. Selection sort always scans the whole unsorted part, so it never speeds up, but it makes only $n-1$ swaps. Quick sort with a last-element pivot meets its worst case on an already sorted array, because each partition peels off one element: $T(n)=T(n-1)+n$.
"""),
 ("Partitioning traced, and the lower bound", r"""
Lomuto partition with the last element as pivot on `[3, 7, 8, 5, 2, 1, 9, 5, 4]`, pivot 4: scan, move every element $\le4$ to the front: `3 2 1` go left, then the pivot lands after them:

    [3 2 1 | 4 | 8 5 7 9 5]     pivot 4 is now in its final position

Quick sort recurses on both sides; the pivot is never touched again. If the pivot always splits evenly, $T(n)=2T(n/2)+n$; if it always splits 1 to $n-1$, $T(n)=T(n-1)+n$. A random pivot gives expected $O(n\log n)$.

**Merge sort** merges two sorted lists with a comparison of the two front elements: merging lengths $a$ and $b$ needs at most $a+b-1$ comparisons. **Any comparison sort** needs $\lceil\log_2(n!)\rceil=\Omega(n\log n)$ comparisons, because a decision tree must have $n!$ leaves, one per permutation. Counting, radix and bucket sort escape it by not comparing elements. To merge $k$ sorted lists with a heap costs $O(N\log k)$ for $N$ total elements.

**Binary search** halves the range each time: at most $\lfloor\log_2n\rfloor+1$ comparisons on a sorted array, $O(\log n)$. Linear search is the only option for unsorted data without preparation.
"""),
)

elab("algo-greedy",
 ("Why greedy sometimes works and sometimes fails", r"""
A greedy algorithm commits to the choice that looks best **right now** and never reconsiders. It is correct only when the problem has the **greedy-choice property** (some optimal solution contains that local choice) and **optimal substructure** (what remains is a smaller instance of the same problem). The standard proof is an **exchange argument**: take any optimal solution, swap in the greedy choice, and show it is still optimal.

Counter-example showing the danger: coins $\{1,3,4\}$ and amount 6. Greedy takes 4, then 1, 1, a total of 3 coins, while 3+3 uses 2. The coin system $\{1,5,10,25\}$ happens to be greedy-safe. **0/1 knapsack** fails the same way (use DP), whereas **fractional knapsack** succeeds because items can be split, taking the highest value-to-weight ratio first.
"""),
 ("Activity selection and Huffman, traced", r"""
**Activity selection:** sort activities by **finish time**, pick the first, then repeatedly pick the next one starting after the last pick. Activities (start, finish): (1,4), (3,5), (0,6), (5,7), (3,9), (5,9), (6,10), (8,11), (8,12), (2,14), (12,16). Sorted by finish, pick (1,4); skip (3,5), (0,6); pick (5,7); skip (3,9), (5,9), (6,10); pick (8,11); skip (8,12), (2,14); pick (12,16). Four activities, the maximum. Sorting by start time or by duration is **wrong**.

**Huffman coding:** repeatedly merge the two least frequent nodes. Frequencies a:5, b:9, c:12, d:13, e:16, f:45. Merge 5+9=14; now {12,13,14,16,45}; merge 12+13=25; {14,16,25,45}; merge 14+16=30; {25,30,45}; merge 25+30=55; {45,55}; merge 100. The code lengths are f:1, c:3, d:3, a:4, b:4, e:3. The total cost is $\sum f_i\cdot\text{depth}_i=45\cdot1+(12+13+16)\cdot3+(5+9)\cdot4=224$ bits. With a binary heap the algorithm takes $O(n\log n)$.

**Job scheduling with deadlines and profits:** sort by profit descending, place each job in the latest free slot at or before its deadline. **Minimising total waiting time:** run the shortest jobs first.
"""),
)

elab("algo-dynamic-programming",
 ("Reading a DP table: LCS traced", r"""
$L[i][j]$ is the length of the LCS of the first $i$ letters of $X$ and the first $j$ of $Y$. If $x_i=y_j$ then $L[i][j]=L[i-1][j-1]+1$, else $\max(L[i-1][j],\,L[i][j-1])$. For $X=\text{ABCB}$, $Y=\text{BDCB}$:

| | ∅ | B | D | C | B |
|---|---|---|---|---|---|
| ∅ | 0 | 0 | 0 | 0 | 0 |
| A | 0 | 0 | 0 | 0 | 0 |
| B | 0 | 1 | 1 | 1 | 1 |
| C | 0 | 1 | 1 | 2 | 2 |
| B | 0 | 1 | 1 | 2 | **3** |

The answer is 3 (BCB). Time and space are $O(mn)$; to recover the string walk back from the corner, going diagonally on a match and towards the larger neighbour otherwise. If only the length is wanted, two rows suffice.

**Edit distance** uses the same grid with $\min$ of three moves: delete ($D[i-1][j]+1$), insert ($D[i][j-1]+1$), replace or match ($D[i-1][j-1]+[x_i\ne y_j]$).
"""),
 ("Knapsack and matrix chain, traced", r"""
**0/1 knapsack.** $K[i][w]$ is the best value using the first $i$ items with capacity $w$: either skip item $i$, $K[i-1][w]$, or take it, $v_i+K[i-1][w-w_i]$. Items (weight, value): (1,1), (3,4), (4,5), (5,7), capacity 7. Two good candidates: items 2 and 3 (weight 7, value 4+5=9) and items 1 and 4 (weight 6, value 1+7=8). The table finds the best, 9. Time $O(nW)$ is **pseudo-polynomial**: polynomial in the number $W$, but exponential in its bit length, which is why the problem is still NP-complete.

**Matrix chain.** For matrices with dimensions $p_0,p_1,\dots,p_n$, $m[i][j]=\min_{i\le k<j}\big(m[i][k]+m[k+1][j]+p_{i-1}p_kp_j\big)$. For $A_1{:}10\times30,\ A_2{:}30\times5,\ A_3{:}5\times60$: $(A_1A_2)A_3$ costs $10\cdot30\cdot5+10\cdot5\cdot60=1500+3000=4500$ while $A_1(A_2A_3)$ costs $30\cdot5\cdot60+10\cdot30\cdot60=9000+18000=27000$. Table size $O(n^2)$, time $O(n^3)$.

**When to use DP:** the problem has **overlapping subproblems** (the same sub-instance appears many times) and optimal substructure. Top-down memoisation computes only the needed states; bottom-up tabulation is usually faster and enables space tricks.
"""),
)

elab("algo-graph-traversal",
 ("BFS and DFS traced on the same graph", r"""
Graph (adjacency lists in increasing order): `A:[B,C] B:[A,D,E] C:[A,F] D:[B] E:[B,F] F:[C,E]`.

**BFS from A** uses a queue and visits by distance: queue `A`; pop A, enqueue B,C; pop B, enqueue D,E; pop C, enqueue F; pop D, pop E, pop F. Order **A B C D E F**, with levels {A}, {B,C}, {D,E,F}. BFS gives **shortest paths in an unweighted graph**: $\text{dist}(F)=2$.

**DFS from A** uses recursion (a stack): A → B → D (dead end, back) → E → F → C. Order **A B D E F C**. Record a **discovery** and a **finish** time for each vertex: A is discovered first and finished last, and every descendant's interval (discovery to finish) nests inside its ancestor's.

Both cost $O(V+E)$ with lists and $O(V^2)$ with a matrix. BFS needs space for a whole level (up to $O(V)$), DFS needs the depth of the recursion.
"""),
 ("What DFS tells you: edge types, cycles, topological order", r"""
In a DFS of a directed graph every edge is one of four types: **tree** (to a white vertex), **back** (to an ancestor still on the stack, grey), **forward** (to a finished descendant) or **cross** (to a finished vertex in another branch). **A directed graph has a cycle if and only if DFS finds a back edge.** In an undirected graph any non-tree edge closes a cycle.

**Topological order** of a DAG is the vertices sorted by **decreasing finish time**; equivalently repeatedly remove a vertex of in-degree 0 (Kahn). A DAG can have several valid orders; the number of orders is 1 exactly when a Hamiltonian path exists.

**Connected components:** run a traversal from each unvisited vertex; the number of starts is the number of components. **Bipartite test:** BFS colouring with two colours; an edge between equal colours means an odd cycle. **Articulation points and bridges** use DFS low-link values; **SCCs** use two DFS passes (Kosaraju) or one (Tarjan), both $O(V+E)$.
"""),
)

elab("algo-shortest-paths-mst",
 ("Dijkstra traced, and why negative edges break it", r"""
Graph: S–A 4, S–B 1, B–A 2, A–C 1, B–C 5. Start at S with distance 0; all others $\infty$.

| Step | Settle | Distances (A, B, C) |
|---|---|---|
| 0 | S (0) | 4, 1, ∞ |
| 1 | B (1) | 3 (via B), 1, 6 |
| 2 | A (3) | 3, 1, 4 (via A) |
| 3 | C (4) | final: A=3, B=1, C=4 |

At each step take the unsettled vertex with the **smallest** tentative distance, then **relax** its outgoing edges: $d[v]=\min(d[v],\,d[u]+w)$. Complexity $O(V^2)$ with an array, $O((V+E)\log V)$ with a binary heap, $O(E+V\log V)$ with a Fibonacci heap. Dijkstra assumes that once a vertex is settled no cheaper path can appear, which is false when an edge is **negative**; then use Bellman–Ford.

**Bellman–Ford** relaxes every edge $V-1$ times: $O(VE)$. A further pass that still improves some distance reveals a **negative cycle** reachable from the source. **Floyd–Warshall** computes all pairs in $O(V^3)$ with $d[i][j]=\min(d[i][j],\,d[i][k]+d[k][j])$ for $k=1..V$, working with negative edges but not negative cycles.
"""),
 ("Kruskal and Prim, and facts about MSTs", r"""
**Kruskal:** sort edges by weight; take an edge if it joins two different components (checked with union–find), skip it if it closes a cycle. Edges (A,B,1), (B,C,2), (A,C,3), (C,D,4), (B,D,5): take 1, take 2, skip 3 (cycle), take 4, stop (3 edges for 4 vertices). Weight 7. Cost $O(E\log E)=O(E\log V)$, dominated by sorting.

**Prim:** grow one tree from a start vertex, always adding the cheapest edge leaving the tree: $O(E\log V)$ with a heap, $O(V^2)$ with a matrix. Both are correct because of the **cut property**: the lightest edge crossing any cut belongs to some MST.

Facts to remember: an MST has exactly $V-1$ edges; if all edge weights are **distinct** the MST is **unique**; an MST also minimises the **maximum** edge on the path between any two vertices (it is a bottleneck tree), but it does **not** give shortest paths; changing every weight by the same increasing function (squaring positive weights) keeps the same MST, yet it can change shortest paths. The **heaviest edge of a cycle** is never in every MST.
"""),
)
