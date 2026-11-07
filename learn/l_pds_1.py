"""Programming & Data Structures — part 1: C, pointers & memory, recursion, arrays/stacks/queues."""
import itertools
import math

from content import g_pds as P
from learn import Ex, lesson

S = "PDS"


def _kernighan(x):
    c = 0
    while x:
        x &= x - 1
        c += 1
    return c


def _prints(n):
    out = []

    def f(k):
        if k > 0:
            out.append(k); f(k - 1); out.append(k)
    f(n)
    return " ".join(map(str, out))


# ======================================================================================================
lesson(subject=S, chapter="C Programming", ch_no=1, no=1, slug="pds-c-operators-bits", title="C Basics: Types, Operators, Precedence & Bit Manipulation",
       topic="C Programming & Pointers", minutes=20, weight=5, widget="bits",
       widget_hint="Enter two 8-bit numbers and a shift amount. The table shows the binary result of every bitwise operator — try x & (x−1) mentally on x = 44, then check.",
       key="C evaluates integer arithmetic exactly as the hardware does: division truncates toward zero, unsigned values wrap around, and precedence/short-circuit rules decide the order. Most GATE ‘output of the program’ questions reduce to these few rules.",
       analogy=("⚙️", "A very literal calculator", "C does precisely what you wrote, using fixed-size boxes. An 8-bit box holds 0–255; put 250 + 10 in it and it silently wraps to 4 — no warning. Division throws away the fraction instead of rounding. Knowing these ‘box rules’ lets you predict any output without running the code."),
       sections=[
           dict(h="Types and sizes", md="""GATE normally states the sizes; the usual assumption (modern 32/64-bit machines) is:

| Type | Size (bytes) | Notes |
|---|---|---|
| `char` | 1 | an 8-bit integer, range −128..127 (or 0..255 if unsigned) |
| `short` | 2 | |
| `int` | **4** | −2³¹ .. 2³¹−1 |
| `long` / `long long` | 8 | |
| `float` / `double` | 4 / 8 | |
| pointer | 8 (4 on a 32-bit system) | size independent of the pointed-to type |

`sizeof` is evaluated at compile time and counts bytes. **Signed overflow is undefined behaviour**, while **unsigned arithmetic wraps modulo 2ⁿ** (well defined): `unsigned char c = 250; c = c + 10;` leaves 4."""),
           dict(h="Integer arithmetic rules", md="""- **Integer division truncates toward zero** (C99): `7/2 = 3`, `-7/2 = -3`, `-7/-2 = 3`.
- **`%` takes the sign of the dividend:** `-7 % 2 = -1`, `7 % -2 = 1`. The identity (a/b)·b + a%b = a always holds.
- If an operand is a `float`/`double` the whole operation is floating-point; `5/2` is 2 but `5/2.0` is 2.5.
- **Implicit conversion:** a signed int compared with an unsigned int is converted to unsigned, so `-1 < 1u` is **false** (−1 becomes 4294967295). `char` and `short` are promoted to `int` in expressions.
- **Integer overflow** of signed types is undefined; shifting by a negative amount or by ≥ the bit width is undefined."""),
           dict(h="Operator precedence and short-circuit evaluation", md="""From highest to lowest precedence:

| Level | Operators | Associativity |
|---|---|---|
| 1 | `()` `[]` `->` `.` postfix `++ --` | left → right |
| 2 | prefix `++ --`, unary `+ - ! ~ * &`, `sizeof`, casts | **right → left** |
| 3 | `* / %` | left → right |
| 4 | `+ -` | left → right |
| 5 | `<< >>` | left → right |
| 6 | `< <= > >=` | left → right |
| 7 | `== !=` | left → right |
| 8–10 | `&`, then `^`, then bitwise OR (single bar) | left → right |
| 11–12 | `&&`, then logical OR (double bar) | left → right |
| 13 | `?:` | right → left |
| 14 | `=` `+=` … | right → left |

**Short-circuit:** in `a && b` the right side is evaluated only if a is true; in `a || b` only if a is false. So `if (x > 0 || y++ > 0)` never increments y when x > 0.""",
                call=[("trap", "Comparison before bitwise", "`x & 1 == 0` parses as `x & (1 == 0)` — equality binds tighter than `&`. Write `(x & 1) == 0`.")]),
           dict(h="Increments, sequence points and undefined behaviour", md="""`i++` yields the old value then increments; `++i` increments then yields the new value. Modifying the same variable twice between sequence points is **undefined behaviour** — `i = i++ + 1`, `a[i] = i++`, `printf("%d %d", i++, i++)`. GATE avoids these in well-posed questions, so if you see them the safe answer is ‘undefined’.

Other classic UB: dereferencing NULL or a dangling pointer, reading an uninitialised local, signed overflow, out-of-bounds array access, shifting too far."""),
           dict(h="Bit tricks you should know", md="""| Expression | Effect |
|---|---|
| `x & (x - 1)` | clears the **lowest set bit** (Kernighan's popcount loop runs once per 1-bit) |
| `x & -x` | isolates the lowest set bit |
| `(x & (x - 1)) == 0` | true iff x is a power of two (or 0) |
| `x << k` | multiply by 2ᵏ (if no overflow) |
| `x >> k` | divide by 2ᵏ (arithmetic shift keeps the sign for signed types) |
| `x ^ x` | 0;   `a ^= b; b ^= a; a ^= b;` swaps without a temporary |
| `~x` | bitwise complement: −x − 1 in two's complement |
| OR with `(1 << k)`; AND with `~(1 << k)`; XOR with `(1 << k)` | set / clear / toggle bit k |"""),
       ],
       examples=[
           Ex("Division and remainder with negatives", "What does `printf(\"%d %d\", -7 / 2, -7 % 2);` print?",
              ["`/` truncates toward zero: −7 / 2 = −3.", "The remainder keeps the sign of the dividend: −7 − (−3·2) = −7 + 6 = −1.", "Output: **-3 -1**."],
              "**-3 -1**", verify=lambda: "%d %d" % (P.cdiv(-7, 2), P.cmod(-7, 2))),
           Ex("Unsigned wrap-around", "`unsigned char c = 250; c = c + 10; printf(\"%d\", c);`",
              ["250 + 10 = 260, which does not fit in 8 bits.", "Unsigned arithmetic is modulo 256: 260 mod 256 = **4**."],
              "**4**", verify=lambda: str((250 + 10) % 256)),
           Ex("Counting set bits", "How many times does the loop body run for x = 44?  `while (x) { x = x & (x - 1); count++; }`",
              ["44 = 101100₂ has three 1-bits.", "Each iteration clears the lowest set bit: 44 → 40 → 32 → 0.", "So the loop runs **3** times (count = number of 1s)."],
              "**3**", verify=lambda: str(_kernighan(44))),
           Ex("Precedence", "What is the value of `2 + 3 * 4 % 5`?",
              ["`*` and `%` have the same precedence and associate left to right: (3 * 4) % 5 = 12 % 5 = 2.", "Then 2 + 2 = **4**."],
              "**4**", verify=lambda: str(2 + (3 * 4) % 5)),
           Ex("Short-circuit", "`int a = 3, b = 0; if (a > 0 || b++ > 0) b += 10; printf(\"%d\", b);`",
              ["`a > 0` is true, so `||` short-circuits and `b++` is never evaluated.", "The body runs once: b = 0 + 10 = **10**."],
              "**10**", verify=lambda: str(10)),
       ],
       traps=[("Rounding in integer division", "C truncates toward zero — it does not floor. −7/2 is −3, not −4."),
              ("Sign of %", "The remainder follows the dividend, so −7 % 2 = −1 (not 1)."),
              ("Signed vs unsigned comparison", "`-1 < 1u` is false because −1 is converted to a huge unsigned value."),
              ("Bitwise vs equality precedence", "`a & b == c` is `a & (b == c)`; always parenthesise bit tests.")],
       quick=[("In C99, `-9 / 4` evaluates to", ["-2", "-3", "-2.25", "2"], 0, "Truncates toward zero."),
              ("`x & (x - 1)` for a power of two x gives", ["x", "x − 1", "0", "1"], 2, "A power of two has a single 1-bit, which gets cleared."),
              ("In `a && b++`, if a is 0 then", ["b is incremented", "b is not evaluated", "the result is 1", "undefined behaviour"], 1, "Short-circuit."),
              ("After `unsigned char c = 255; c++;` the value of c is", ["256", "0", "255", "undefined"], 1, "Wraps modulo 256.")],
       summary=["Integer `/` truncates toward zero; `%` takes the dividend's sign; unsigned wraps modulo 2ⁿ; signed overflow is undefined.", "int = 4 bytes, long/pointer = 8, char = 1 (unless the question says otherwise).",
                "Precedence: unary > * / % > + − > shifts > relational > equality > & > ^ > | > && > || > ?: > =.", "`&&` and `||` short-circuit.", "Modifying a variable twice between sequence points is undefined.", "x & (x−1) clears the lowest set bit; (x & (x−1)) == 0 ⇒ power of two."])


# ======================================================================================================
lesson(subject=S, chapter="C Programming", ch_no=1, no=2, slug="pds-pointers-memory", title="Pointers, Arrays, Strings, Structs & Memory Layout",
       topic="C Programming & Pointers", minutes=24, weight=5, widget="none",
       key="A pointer holds an address; pointer arithmetic moves in steps of the pointed-to type's size; an array name decays to a pointer to its first element, so a[i] is *(a + i). Structs are laid out with alignment padding, and C passes everything by value.",
       analogy=("🏠", "Houses and addresses", "A variable is a house; a pointer is a piece of paper with the house's address written on it. Adding 1 to the address on an array of 4-byte ints moves you to the *next house* — 4 bytes along, not 1 — because the compiler knows how big each house is. Copying the paper (passing a pointer) does not copy the house."),
       sections=[
           dict(h="Pointer basics", md="""- `int x = 5; int *p = &x;` — `p` holds the address of `x`; `*p` is the value at that address (**dereference**).
- `int **pp = &p;` — pointer to pointer: `**pp` is x.
- **NULL** (0) means ‘points nowhere’; dereferencing it is undefined (typically a crash). A pointer to freed memory is **dangling**.
- `void *` is a generic pointer (cannot be dereferenced without a cast).
- **Pointer arithmetic is scaled:** if `p` is `T *`, then `p + k` is the address `p + k·sizeof(T)`; `q − p` (for two pointers into the same array) is the number of **elements** between them, not bytes.""",
                formulas=[("address of a[i]  =  base + i · sizeof(element)", "1-D array"), ("a[i]  ≡  *(a + i)  ≡  i[a]", "indexing is pointer arithmetic")]),
           dict(h="Arrays and 2-D arrays", md="""The name of an array **decays** to a pointer to its first element in most expressions — except as the operand of `sizeof` or `&`. Hence for `int a[10]`: `sizeof(a)` = 40 but inside a function receiving `int *p`, `sizeof(p)` = 8 (the pointer). An array parameter is really a pointer.

C stores 2-D arrays in **row-major** order. For `T a[R][C]` with base address B:""",
                formulas=[("address of a[i][j]  =  B + (i·C + j) · sizeof(T)", "row-major (C)"), ("column-major would be  B + (j·R + i) · sizeof(T)", "Fortran / MATLAB")],
                call=[("tip", "Number of elements", "`sizeof(a) / sizeof(a[0])` gives the element count of a true array (not of a pointer).")]),
           dict(h="Strings", md="""A C string is a `char` array ending with a **NUL** byte `'\\0'`. So `char s[] = "gate";` occupies **5** bytes: `sizeof(s)` = 5 but `strlen(s)` = 4 (it stops at the NUL and does not count it).

`char *p = "gate";` points to a **read-only string literal** — modifying `p[0]` is undefined behaviour — whereas `char s[] = "gate";` is a modifiable copy. `strcpy` and friends can overflow a too-small buffer."""),
           dict(h="Structs, unions and alignment", md="""A **struct** stores members in declaration order. Each member is aligned to a multiple of its own size, so the compiler inserts **padding**, and the total size is rounded up to a multiple of the largest member's alignment.

    struct S { char c; int i; char d; double e; };

c at offset 0 (1 byte); int needs offset 4; d at offset 8; double needs offset 16 → ends at 24, a multiple of 8 ⇒ `sizeof(struct S)` = **24**. Reordering members (double, int, char, char) shrinks it to 16.

A **union** stores all members at the **same address**; its size is that of its largest member (padded). Only the last-written member is meaningful. An **enum** is an integer type with named constants starting at 0."""),
           dict(h="Storage classes and the memory layout", md="""| Class | Lifetime | Where | Notes |
|---|---|---|---|
| `auto` (default locals) | until the block ends | **stack** | uninitialised garbage |
| `register` | block | register (hint) | cannot take its address |
| `static` (local) | whole program | **data / bss** | initialised once, keeps value between calls |
| `static` (global) | whole program | data / bss | file-private (internal linkage) |
| `extern` | whole program | data / bss | declared here, defined elsewhere |
| `malloc`/`calloc` | until `free` | **heap** | must be freed to avoid a **leak** |

A process has code (text), initialised data, uninitialised data (bss), the heap (grows up) and the stack (grows down; function frames). **C always passes arguments by value** — to modify a caller's variable pass its address. Forgetting `free` leaks memory; using memory after `free` is a dangling-pointer bug."""),
       ],
       examples=[
           Ex("Address of an array element", "An `int` array (4 bytes per int) starts at address 1000. What is the address of `a[7]`?",
              ["Element i lies i × sizeof(int) bytes after the base address.", "address = 1000 + 7 × 4 = **1028**."],
              "**1028**", verify=lambda: str(1000 + 7 * 4)),
           Ex("2-D array address", "`int a[3][4]` is stored in row-major order starting at address 2000 (int = 4 bytes). What is the address of `a[2][1]`?",
              ["Offset (in elements) = i·C + j = 2·4 + 1 = 9.", "Address = 2000 + 9 × 4 = **2036**."],
              "**2036**", verify=lambda: str(2000 + (2 * 4 + 1) * 4)),
           Ex("Size of a struct", "Assuming char = 1, int = 4, double = 8 and natural alignment, what is `sizeof(struct { char c; int i; char d; double e; })`?",
              ["c: offset 0. i: aligned to 4 → offset 4 (padding 3). d: offset 8.", "e: aligned to 8 → offset 16 (padding 7), ends at 24.", "24 is already a multiple of the largest alignment (8): **24 bytes**."],
              "**24**", verify=lambda: str(P.csizeof(["char", "int", "char", "double"]))),
           Ex("Pointer difference", "`int a[20]; int *p = &a[3], *q = &a[9]; printf(\"%d\", (int)(q - p));`",
              ["Pointer subtraction counts **elements**, not bytes.", "9 − 3 = **6**."],
              "**6**", verify=lambda: str(9 - 3)),
           Ex("sizeof vs strlen", "`char s[] = \"compiler\"; printf(\"%d %d\", (int)sizeof(s), (int)strlen(s));`",
              ["“compiler” has 8 letters; the array also stores the terminating NUL.", "sizeof(s) = 9, strlen(s) = 8 → output **9 8**."],
              "**9 8**", verify=lambda: "%d %d" % (len("compiler") + 1, len("compiler"))),
       ],
       traps=[("Pointer arithmetic is scaled", "`p + 1` advances by sizeof(*p) bytes, not 1 byte."),
              ("sizeof on an array parameter", "Inside the function the array is a pointer, so sizeof gives the pointer's size."),
              ("String literals are read-only", "`char *p = \"hi\"; p[0] = 'H';` is undefined; use `char p[] = \"hi\";`."),
              ("Struct size ≠ sum of members", "Add padding for alignment and round the total to the largest alignment.")],
       quick=[("For `int *p` with p = 2000, `p + 3` equals (int = 4 bytes)", ["2003", "2012", "2004", "2006"], 1, "2000 + 3·4."),
              ("`sizeof(\"hello\")` (a string literal) is", ["5", "6", "8", "undefined"], 1, "5 letters + NUL."),
              ("A union of `int` (4 bytes) and `double` (8 bytes) has size", ["4", "8", "12", "16"], 1, "The largest member."),
              ("C passes function arguments", ["by reference", "by value", "by name", "by copy-restore"], 1, "Always by value; pointers are copied.")],
       summary=["Pointer arithmetic is scaled by sizeof(T); q − p counts elements; a[i] ≡ *(a + i).", "Array name decays to a pointer (except with sizeof and &); array parameters are pointers.", "Row-major address: B + (i·C + j)·size.",
                "String = chars + NUL: sizeof counts it, strlen does not; literals are read-only.", "Struct layout: align each member, pad, round total to the largest alignment; union size = largest member.", "Stack = locals; heap = malloc/free; static/global = data segment; C is pass-by-value."])


# ======================================================================================================
lesson(subject=S, chapter="Recursion", ch_no=2, no=1, slug="pds-recursion", title="Recursion: Call Stack, Tracing & Complexity",
       topic="Recursion", minutes=20, weight=4, widget="rectree",
       widget_hint="Slide n to see the recursion tree of fib(n). Notice how many identical subproblems appear — then tick ‘memoise’ and watch the number of calls collapse.",
       key="A recursive function calls itself on a smaller problem until it reaches a base case. Each call gets its own stack frame, so the call tree — and the order of any prints — can be traced by hand; naive branching recursion (like Fibonacci) is exponential, which memoisation fixes.",
       analogy=("🪆", "Russian nesting dolls", "To count the dolls you open one and ask the next doll the same question, until you reach the smallest doll (the base case) with nothing inside. Then the answers come back out, each adding one. If there were no smallest doll you would open dolls forever — infinite recursion and a stack overflow."),
       sections=[
           dict(h="Anatomy of a recursive function", md="""Every correct recursion has:

1. a **base case** that returns without recursing,
2. a **recursive case** that calls the function on a **strictly smaller** input,
3. progress toward the base case (otherwise → infinite recursion → *stack overflow*).

Each call pushes an **activation record** (parameters, locals, return address) on the call stack and pops it on return. Maximum recursion depth = peak stack size; for `f(n) = ... f(n-1)` it is about n frames, so space is **O(n)**."""),
           dict(h="Tracing: pre-order vs post-order output", md="""Where the `printf` sits relative to the recursive call decides the output order:

    void f(int n) {
        if (n > 0) {
            printf("%d ", n);   /* before the call: pre-order, counts down */
            f(n - 1);
            printf("%d ", n);   /* after the call: post-order, counts up on the way out */
        }
    }

`f(3)` prints **3 2 1 1 2 3**: the first three prints happen on the way *in*, the last three on the way *out*. Draw the call tree and read prints off in execution order."""),
           dict(h="Counting calls and complexity", md="""- **Linear recursion** `f(n) = ... f(n−1)`: n + 1 calls, depth n, time O(n).
- **Binary recursion without sharing** such as `fib(n) = fib(n−1) + fib(n−2)`: the number of calls C(n) = C(n−1) + C(n−2) + 1 grows as **Θ(φⁿ) ≈ 1.618ⁿ**; exactly C(n) = 2·F(n+1) − 1 where F is the Fibonacci sequence.
- **Halving recursion** `f(n) = f(n/2) + 1`: log₂ n calls (binary search, fast exponentiation).
- **Memoisation** (cache each result) makes each distinct argument computed once: fib needs only **2n − 1 calls**, O(n) time.""",
                formulas=[("calls(fib n) = 2·F(n+1) − 1", "n = 10 → 177 calls"), ("memoised fib: 2n − 1 calls", "n = 10 → 19 calls")]),
           dict(h="Tail recursion, mutual recursion and classics", md="""A call is **tail-recursive** if it is the very last action (nothing happens after it returns). A compiler can reuse the frame, turning it into a loop with O(1) stack — `gcd(a, b) = b == 0 ? a : gcd(b, a % b)` is tail recursive; `n * fact(n−1)` is not.

**Mutual recursion** (`isEven`/`isOdd` calling each other) needs a forward declaration in C.

Classics: factorial; Fibonacci; GCD (Euclid, O(log min(a,b)) depth); fast power `power(b, e)` using e/2 (O(log e)); **Tower of Hanoi** (T(n) = 2T(n−1) + 1 = 2ⁿ − 1 moves); permutations/subsets generation (n! and 2ⁿ outputs); Ackermann (grows faster than any primitive recursive function); the McCarthy 91 function."""),
       ],
       examples=[
           Ex("Number of calls", "How many calls (including the first) are made when evaluating the naive `fib(10)`?  `int fib(int n) { return n < 2 ? n : fib(n-1) + fib(n-2); }`",
              ["C(n) = 1 + C(n−1) + C(n−2) with C(0) = C(1) = 1.", "C(2)=3, C(3)=5, C(4)=9, C(5)=15, C(6)=25, C(7)=41, C(8)=67, C(9)=109, C(10)=**177**.", "Check: 2·F(11) − 1 = 2·89 − 1 = 177."],
              "**177**", verify=lambda: str(P.calls(10))),
           Ex("Trace the output order", "What does `f(3)` print for the pre/post-order function above?",
              ["f(3) prints 3, calls f(2) → prints 2, calls f(1) → prints 1, calls f(0) → returns.", "Back in f(1): prints 1; back in f(2): prints 2; back in f(3): prints 3.", "Output: **3 2 1 1 2 3**."],
              "**3 2 1 1 2 3**", verify=lambda: _prints(3)),
           Ex("Euclid's recursion depth", "How many recursive calls (excluding the first) does `gcd(48, 18)` make?  `int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }`",
              ["gcd(48,18) → gcd(18,12) → gcd(12,6) → gcd(6,0) → returns 6.", "The calls after the first are gcd(18,12), gcd(12,6), gcd(6,0) = **3**."],
              "**3**", verify=lambda: "3" if (lambda a, b: (lambda f: f(f, a, b))(lambda f, a, b: 0 if b == 0 else 1 + f(f, b, a % b)))(48, 18) == 3 else "bad"),
           Ex("The Ackermann function", "Evaluate A(2, 3), where A(0,n)=n+1; A(m,0)=A(m−1,1); A(m,n)=A(m−1, A(m, n−1)).",
              ["A(1, n) = n + 2 and A(2, n) = 2n + 3.", "So A(2, 3) = 2·3 + 3 = **9**."],
              "**9**", verify=lambda: str((lambda A: A(A, 2, 3))(lambda A, m, n: n + 1 if m == 0 else A(A, m - 1, 1) if n == 0 else A(A, m - 1, A(A, m, n - 1))))),
           Ex("Tower of Hanoi", "How many moves does the optimal solution need for 5 disks?",
              ["T(n) = 2T(n−1) + 1 with T(0) = 0 solves to 2ⁿ − 1.", "T(5) = 32 − 1 = **31**."],
              "**31**", verify=lambda: str((lambda T: T(T, 5))(lambda T, n: 0 if n == 0 else 2 * T(T, n - 1) + 1))),
       ],
       traps=[("Print before vs after the call", "A print placed after the recursive call runs on the way **out**, in reverse order."),
              ("Counting calls", "Include the very first call and the base-case calls — C(n) = 1 + C(n−1) + C(n−2), not F(n)."),
              ("Tail recursion needs nothing after the call", "`return n * f(n-1)` is **not** tail recursive (a multiplication remains)."),
              ("Missing or unreachable base case", "Leads to infinite recursion and stack overflow.")],
       quick=[("The number of calls of naive fib(n) grows", ["linearly", "quadratically", "exponentially", "logarithmically"], 2, "Θ(φⁿ)."),
              ("Which is tail recursive?", ["return n * f(n-1);", "return f(n-1) + f(n-2);", "return g(a, b % a);  (where g is the same function)", "printf after the call"], 2, "The recursive call is the last operation."),
              ("Memoised fib(10) makes how many calls?", ["10", "19", "55", "177"], 1, "2n − 1 = 19."),
              ("Tower of Hanoi with 6 disks needs", ["12", "36", "63", "64"], 2, "2⁶ − 1.")],
       summary=["Base case + smaller recursive case; each call has a stack frame, so depth n ⇒ O(n) space.", "Prints before the call appear in call order; prints after appear in reverse (post-order).", "Naive fib: C(n) = 2F(n+1) − 1 calls; memoised: 2n − 1.",
                "Halving recursion → O(log n); tail recursion → O(1) stack with optimisation.", "Hanoi: 2ⁿ − 1 moves; gcd depth O(log min).", "Draw the call tree to count calls and trace output."])


# ======================================================================================================
def _stack_perms(n):
    def ok(seq):
        st, nxt = [], 1
        for x in seq:
            while (not st or st[-1] != x) and nxt <= n:
                st.append(nxt); nxt += 1
            if not st or st[-1] != x:
                return False
            st.pop()
        return True
    return sum(1 for p in itertools.permutations(range(1, n + 1)) if ok(p))


def _circ_count(front, rear, cap):
    return (rear - front) % cap + 1


lesson(subject=S, chapter="Linear Data Structures", ch_no=3, no=1, slug="pds-arrays-stacks-queues", title="Arrays, Stacks & Queues",
       topic="Arrays, Stacks & Queues", minutes=22, weight=5, widget="stackq",
       widget_hint="Type an infix expression to see its postfix form and value — the same conversion GATE asks for, done with a stack (shunting-yard).",
       key="A stack is last-in-first-out (push/pop at one end); a queue is first-in-first-out (enqueue at the rear, dequeue at the front). Both give O(1) operations; stacks power expression evaluation and function calls, queues power BFS and scheduling.",
       analogy=("🥞", "Pancakes and queues", "A stack is a pile of pancakes: you add and take from the top only — the last pancake placed is the first eaten. A queue is the line at a ticket counter: the person who arrived first is served first. Same data, opposite order."),
       sections=[
           dict(h="Arrays", md="""An **array** stores elements contiguously, giving **O(1) random access**; insertion or deletion in the middle costs O(n) (shifting). Searching an unsorted array is O(n); in a sorted array, binary search is O(log n).

Address formulas: 1-D `base + i·size`; 2-D row-major `base + (i·C + j)·size`; column-major `base + (j·R + i)·size`. For a lower bound L: `base + (i − L)·size`. A **sparse** matrix is better stored as a list of (row, col, value) triples."""),
           dict(h="Stack (LIFO)", md="""Operations **push**, **pop**, **peek/top**, **isEmpty** — each **O(1)** with an array or a linked list.

Applications:
- **Function calls:** the call stack of activation records.
- **Expression evaluation:** evaluate a postfix expression with one stack; convert infix → postfix with an operator stack (**shunting-yard**).
- **Balanced parentheses** and syntax checking; **undo** history; DFS; backtracking.

**Postfix evaluation:** scan left to right; push operands; on an operator pop two (second popped is the *left* operand), apply, push the result.
**Infix → postfix:** operands go straight to output; for an operator pop operators of higher (or equal, for left-associative) precedence first; `(` is pushed and `)` pops until `(`.""",
                call=[("key", "Stack permutations", "Pushing 1, 2, …, n in order with pops interleaved, the number of distinct pop sequences is the **Catalan number** Cₙ = C(2n, n)/(n + 1): for n = 4 it is 14. A sequence is impossible if it forces a smaller element to pop *after* a larger one that was above it (like 3 1 2).")]),
           dict(h="Queue, circular queue, deque, priority queue", md="""**Queue (FIFO):** enqueue at the rear, dequeue at the front — O(1) each with a linked list or a circular array.

**Circular queue** in an array of size N: `rear = (rear + 1) % N`, `front = (front + 1) % N`. If one slot is left empty to distinguish full from empty, the capacity is **N − 1**; the queue is full when `(rear + 1) % N == front` and empty when `front == rear`. If `front` indexes the first element and `rear` the last, the number of elements is `(rear − front + N) % N + 1`.

**Deque:** insert/delete at both ends. **Priority queue:** removes the element with the highest priority — usually a heap (O(log n) per operation).

**Two-stack queue:** enqueue by pushing on stack A; dequeue by popping from stack B, refilling B from A (reversing) when B is empty — **O(1) amortised** per operation. A stack from two queues needs one expensive operation (O(n))."""),
           dict(h="Complexity table", md="""| Operation | Array (unsorted) | Stack | Queue | Linked list (head only) |
|---|---|---|---|---|
| Access k-th | O(1) | – | – | O(k) |
| Insert at end | O(1)* | push O(1) | enqueue O(1) | O(n) (no tail pointer) |
| Insert at front | O(n) | – | – | O(1) |
| Delete | O(n) | pop O(1) | dequeue O(1) | O(1) at head |
| Search | O(n) | O(n) | O(n) | O(n) |

\\* amortised, if the array grows by doubling."""),
       ],
       examples=[
           Ex("Infix to postfix", "Convert a + b * c − d / e to postfix.",
              ["* and / bind tighter than + and −. b*c becomes `bc*` and d/e becomes `de/`.", "Then a + (bc*) → `abc*+`, and subtracting (de/) gives `abc*+de/-`."],
              "**abc*+de/-**", verify=lambda: "".join(P.to_postfix(list("a+b*c-d/e")))),
           Ex("Evaluate a postfix expression", "Evaluate 8 2 3 * + 4 −  (tokens separated by spaces).",
              ["Push 8, 2, 3. `*` pops 3 and 2 → 6; push → stack 8, 6.", "`+` pops 6 and 8 → 14; push. Push 4. `−` pops 4 and 14 → 14 − 4 = **10**."],
              "**10**", verify=lambda: str(P.postfix_eval("8 2 3 * + 4 -".split()))),
           Ex("Stack permutations", "Elements 1, 2, 3, 4 are pushed in order (pops may be interleaved). How many different pop sequences are possible?",
              ["Valid pop sequences of a stack fed with 1..n in order are counted by the Catalan number Cₙ = C(2n, n)/(n + 1).", "C₄ = C(8,4)/5 = 70/5 = **14**."],
              "**14**", verify=lambda: str(_stack_perms(4))),
           Ex("Elements in a circular queue", "A circular queue has capacity 8 (indices 0..7). front = 5 points at the first element and rear = 1 at the last. How many elements does it hold?",
              ["The queue wraps around: (rear − front + N) mod N + 1 = (1 − 5 + 8) mod 8 + 1.", "= 4 + 1 = **5** elements (indices 5, 6, 7, 0, 1)."],
              "**5**", verify=lambda: str(_circ_count(5, 1, 8))),
       ],
       traps=[("Postfix operand order", "For `a b -` pop b first, then a: the result is a − b. Reversing them is the classic wrong answer."),
              ("Same-precedence operators", "Left-associative ones (`-`, `/`) pop equal-precedence operators first; `^` is right-associative and does not."),
              ("Circular queue capacity", "With the ‘one slot empty’ convention the usable capacity is N − 1."),
              ("Array insertion cost", "Inserting at the **front** shifts n elements; only inserting at the end is O(1) (amortised).")],
       quick=[("A stack follows", ["FIFO", "LIFO", "random access", "priority order"], 1, "Last in, first out."),
              ("Which is NOT a stack application?", ["Function call management", "Expression evaluation", "BFS traversal", "Parentheses matching"], 2, "BFS uses a queue."),
              ("Postfix of (a + b) * c is", ["ab+c*", "abc+*", "ab*c+", "a+bc*"], 0, "Add first, then multiply by c."),
              ("A circular queue array of size 10 (one slot kept empty) can hold at most", ["9", "10", "11", "5"], 0, "N − 1 elements.")],
       summary=["Array: O(1) access, O(n) middle insert/delete; row-major address B + (i·C + j)·size.", "Stack = LIFO, all ops O(1); used for calls, postfix, parentheses, DFS.", "Queue = FIFO, O(1); circular queue uses (index + 1) % N; one empty slot ⇒ capacity N − 1.",
                "Infix → postfix with an operator stack; evaluate postfix with an operand stack (second pop = left operand).", "Pop sequences from pushing 1..n: Catalan Cₙ (14 for n = 4).", "Queue from two stacks: O(1) amortised."])
