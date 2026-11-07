"""Programming & Data Structures — parametric generators (answers by running equivalent Python)."""
import itertools
import math
from collections import deque

from content.kit import *

S = "PDS"
CP, RE, ASQ, LL, TR, HH, GR = ("C Programming & Pointers", "Recursion", "Arrays, Stacks & Queues", "Linked Lists", "Trees & BST", "Heaps & Hashing", "Graph Representation")


def cdiv(a, b):
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q


def cmod(a, b):
    return a - b * cdiv(a, b)


# ---------------- C programming ----------------
@gen(S, CP, "Operators & arithmetic", n=100, diff="easy")
def c_ops(r):
    kind = r.choice(["div", "mod", "bit", "shift", "prec", "uchar", "inc", "short", "ternary"])
    a, b = r.randint(-30, 40), r.choice([3, 4, 5, 7, -3, -4, -5, 6])
    if a == 0: a = 7
    if kind == "div": return nat(r, "What does the following print?\n```c\nint a = %d, b = %d;\nprintf(\"%%d\", a / b);\n```" % (a, b), cdiv(a, b), "C truncates integer division toward zero.")
    if kind == "mod": return nat(r, "What does the following print? (C99 semantics)\n```c\nint a = %d, b = %d;\nprintf(\"%%d\", a %% b);\n```" % (a, b), cmod(a, b), "The sign of the remainder follows the dividend.")
    x, y = r.randint(1, 255), r.randint(1, 255)
    if kind == "bit":
        op = r.choice(["&", "|", "^"])
        return nat(r, "What does the following print?\n```c\nunsigned char x = %d, y = %d;\nprintf(\"%%d\", x %s y);\n```" % (x, y, op), {"&": x & y, "|": x | y, "^": x ^ y}[op], "Bitwise %s of %s and %s." % (op, bin(x), bin(y)))
    if kind == "shift":
        k = r.randint(1, 4)
        return nat(r, "What does the following print?\n```c\nunsigned char x = %d;\nx = x << %d;\nprintf(\"%%d\", x);\n```" % (x, k), (x << k) & 255, "The result wraps modulo 256 when stored in an 8-bit unsigned char.")
    if kind == "prec":
        c, d, e = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
        return nat(r, "What does the following print?\n```c\nint a = %d, b = %d, c = %d;\nprintf(\"%%d\", a + b * c %% 4);\n```" % (c, d, e), c + (d * e) % 4, "*, % bind tighter than +, left to right: b·c mod 4 first.")
    if kind == "uchar":
        v, k = r.randint(200, 255), r.randint(5, 80)
        return nat(r, "What does the following print?\n```c\nunsigned char c = %d;\nc = c + %d;\nprintf(\"%%d\", c);\n```" % (v, k), (v + k) % 256, "Arithmetic wraps modulo 256.")
    if kind == "inc":
        i = r.randint(1, 9)
        return nat(r, "What does the following print?\n```c\nint i = %d;\nint j = i++ * 2;\nint k = ++i * 2;\nprintf(\"%%d\", j + k);\n```" % i, i * 2 + (i + 2) * 2, "j uses the old i; k uses the incremented value (i+2).")
    if kind == "short":
        n = r.randint(1, 6)
        return nat(r, "What does the following print?\n```c\nint a = %d, b = 0;\nif (a > 0 || b++ > 0) b += 10;\nprintf(\"%%d\", b);\n```" % n, 10, "|| short-circuits: b++ is never evaluated.")
    x, y = r.randint(1, 20), r.randint(1, 20)
    return nat(r, "What does the following print?\n```c\nint x = %d, y = %d;\nprintf(\"%%d\", x > y ? x - y : y - x);\n```" % (x, y), abs(x - y), "The ternary yields |x − y|.")


@gen(S, CP, "Pointers & arrays", n=90, diff="medium")
def c_ptr(r):
    kind = r.choice(["deref", "addr", "diff", "sizeof", "arr2d", "ptrptr", "strlen"])
    c, d, k, j = r.randint(2, 9), r.randint(0, 9), r.randint(0, 3), r.randint(0, 3)
    if kind == "deref":
        return nat(r, "What does the following print?\n```c\nint a[8];\nfor (int i = 0; i < 8; i++) a[i] = i * %d + %d;\nint *p = a + %d;\nprintf(\"%%d\", *(p + %d));\n```" % (c, d, k, j), (k + j) * c + d, "p points to a[%d]; *(p+%d) = a[%d]." % (k, j, k + j))
    if kind == "addr":
        base, t = r.choice([1000, 2000, 4000]), r.choice([("char", 1), ("short", 2), ("int", 4), ("double", 8), ("long long", 8)])
        n = r.randint(2, 9)
        return nat(r, "A %s array starts at address %d and sizeof(%s) = %d. What is the address of element a[%d]?" % (t[0], base, t[0], t[1], n), base + n * t[1], "base + index × size.")
    if kind == "diff":
        n = r.randint(3, 9)
        return nat(r, "What does the following print?\n```c\nint a[20];\nint *p = &a[%d], *q = &a[%d];\nprintf(\"%%d\", (int)(q - p));\n```" % (n, n + j + 2), j + 2, "Pointer subtraction yields the number of elements between them.")
    if kind == "sizeof":
        n = r.randint(3, 12)
        return nat(r, "Assuming sizeof(int) = 4, what does the following print?\n```c\nint a[%d];\nprintf(\"%%d\", (int)(sizeof(a) / sizeof(a[0])) * 100 + (int)sizeof(a[0]));\n```" % n, n * 100 + 4, "Number of elements × 100 + element size.")
    if kind == "arr2d":
        R, C, i, jj = r.randint(3, 6), r.randint(3, 6), r.randint(0, 2), r.randint(0, 2)
        base, sz = r.choice([1000, 2000]), r.choice([2, 4, 8])
        return nat(r, "A %d × %d int array (sizeof(int) = %d) is stored in row-major order starting at address %d. Address of a[%d][%d]?" % (R, C, sz, base, i, jj), base + (i * C + jj) * sz, "base + (i·cols + j)·size.")
    if kind == "ptrptr":
        x = r.randint(1, 50)
        return nat(r, "What does the following print?\n```c\nint x = %d, *p = &x, **q = &p;\n**q = **q + %d;\nprintf(\"%%d\", x);\n```" % (x, c), x + c, "**q refers to x.")
    s = r.choice(["hello", "world", "compiler", "gate", "pointer", "datastructure"])
    return nat(r, "What does the following print?\n```c\nchar s[] = \"%s\";\nprintf(\"%%d\", (int)sizeof(s) - (int)strlen(s));\n```" % s, 1, "sizeof counts the terminating NUL; strlen does not.")


def csizeof(fields):
    off, al = 0, 1
    for t in fields:
        sz = {"char": 1, "short": 2, "int": 4, "float": 4, "double": 8, "long": 8}[t]
        al = max(al, sz)
        off = (off + sz - 1) // sz * sz + sz
    return (off + al - 1) // al * al


@gen(S, CP, "Structs & memory", n=70, diff="hard", marks=2)
def c_struct(r):
    ts = [r.choice(["char", "short", "int", "double", "char", "int"]) for _ in range(r.randint(3, 5))]
    union = r.random() < 0.25
    body = "\n".join("    %s f%d;" % (t, i) for i, t in enumerate(ts))
    if union:
        sz = max({"char": 1, "short": 2, "int": 4, "double": 8}[t] for t in ts)
        return nat(r, "Assuming char=1, short=2, int=4, double=8 bytes, what is sizeof of this union?\n```c\nunion U {\n%s\n};\n```" % body, sz, "A union is as large as its largest member (alignment-padded).")
    return nat(r, "Assuming char=1, short=2, int=4, double=8 bytes and natural alignment (each member aligned to its own size, struct size a multiple of the largest alignment), what is sizeof(struct S)?\n```c\nstruct S {\n%s\n};\n```" % body, csizeof(ts), "Lay out members with padding: total %d." % csizeof(ts))


def fn_loop(r):
    n, k = r.randint(8, 30), r.randint(2, 5)
    return n, k


@gen(S, CP, "Loops & control flow", n=90, diff="medium")
def c_loop(r):
    n, k = fn_loop(r)
    kind = r.choice(["sumk", "gcd", "digits", "rev", "xor", "stars", "cont", "while_pow", "collatz"])
    if kind == "sumk": return nat(r, "What does the following print?\n```c\nint s = 0;\nfor (int i = 1; i <= %d; i++)\n    if (i %% %d == 0) s += i;\nprintf(\"%%d\", s);\n```" % (n, k), sum(i for i in range(1, n + 1) if i % k == 0), "Sum of multiples of %d up to %d." % (k, n))
    if kind == "gcd":
        a, b = r.randint(10, 200), r.randint(10, 200)
        return nat(r, "What does the following print?\n```c\nint a = %d, b = %d;\nwhile (b) { int t = b; b = a %% b; a = t; }\nprintf(\"%%d\", a);\n```" % (a, b), math.gcd(a, b), "Euclid's algorithm.")
    if kind == "digits":
        v = r.randint(100, 99999)
        return nat(r, "What does the following print?\n```c\nint n = %d, s = 0;\nwhile (n > 0) { s += n %% 10; n /= 10; }\nprintf(\"%%d\", s);\n```" % v, sum(map(int, str(v))), "Sum of decimal digits.")
    if kind == "rev":
        v = r.randint(100, 9999)
        return nat(r, "What does the following print?\n```c\nint n = %d, r = 0;\nwhile (n > 0) { r = r * 10 + n %% 10; n /= 10; }\nprintf(\"%%d\", r);\n```" % v, int(str(v)[::-1]), "Digit reversal.")
    if kind == "xor":
        m = r.randint(5, 40)
        x = 0
        for i in range(1, m + 1): x ^= i
        return nat(r, "What does the following print?\n```c\nint x = 0;\nfor (int i = 1; i <= %d; i++) x ^= i;\nprintf(\"%%d\", x);\n```" % m, x, "Cumulative XOR.")
    if kind == "stars":
        m = r.randint(3, 12)
        return nat(r, "How many times is '*' printed?\n```c\nfor (int i = 1; i <= %d; i++)\n    for (int j = 1; j <= i; j++)\n        printf(\"*\");\n```" % m, m * (m + 1) // 2, "1 + 2 + … + n.")
    if kind == "cont":
        m, a = r.randint(10, 30), r.randint(2, 5)
        s = 0
        for i in range(1, m + 1):
            if i % a == 0: continue
            if i > m - 3: break
            s += i
        return nat(r, "What does the following print?\n```c\nint s = 0;\nfor (int i = 1; i <= %d; i++) {\n    if (i %% %d == 0) continue;\n    if (i > %d) break;\n    s += i;\n}\nprintf(\"%%d\", s);\n```" % (m, a, m - 3), s, "Simulate continue/break.")
    if kind == "while_pow":
        b, e = r.randint(2, 5), r.randint(3, 8)
        return nat(r, "How many times does the loop body execute?\n```c\nint x = 1, c = 0;\nwhile (x < %d) { x *= %d; c++; }\n```" % (b ** e + 1, b), e + 1 if b ** e < b ** e + 1 else e, "x takes the values 1, %d, … until it reaches %d." % (b, b ** e + 1))
    s0 = r.randint(3, 40)
    steps, x = 0, s0
    while x != 1:
        x = x // 2 if x % 2 == 0 else 3 * x + 1
        steps += 1
    return nat(r, "What does the following print?\n```c\nint n = %d, c = 0;\nwhile (n != 1) { n = (n %% 2 == 0) ? n / 2 : 3 * n + 1; c++; }\nprintf(\"%%d\", c);\n```" % s0, steps, "Collatz steps for %d." % s0)


@gen(S, CP, "Macros & scope", n=50, diff="hard", marks=2)
def c_macro(r):
    a, b = r.randint(2, 9), r.randint(2, 9)
    kind = r.choice(["sq", "static", "byval", "max"])
    if kind == "sq": return nat(r, "What does the following print?\n```c\n#define SQ(x) x * x\nint a = %d, b = %d;\nprintf(\"%%d\", SQ(a + b));\n```" % (a, b), a + a * b + b, "Macro expands textually: a + b * a + b (no parentheses).")
    if kind == "static":
        n = r.randint(3, 8)
        return nat(r, "What does the following print?\n```c\nint f() { static int c = %d; c += 2; return c; }\nint main() {\n    int s = 0;\n    for (int i = 0; i < %d; i++) s = f();\n    printf(\"%%d\", s);\n}\n```" % (a, n), a + 2 * n, "A static local persists across calls.")
    if kind == "byval": return nat(r, "What does the following print?\n```c\nvoid f(int x) { x = x + %d; }\nint main() {\n    int a = %d;\n    f(a);\n    printf(\"%%d\", a);\n}\n```" % (b, a), a, "C passes arguments by value.")
    return nat(r, "What does the following print?\n```c\n#define MAX(x, y) ((x) > (y) ? (x) : (y))\nint a = %d, b = %d;\nint m = MAX(a++, b++);\nprintf(\"%%d\", a + b + m);\n```" % (a, b), _macro_max(a, b), "Both a++ and b++ are evaluated once in the condition; the chosen operand is evaluated again."
               )


def _macro_max(a, b):
    # ((a++) > (b++) ? (a++) : (b++))
    ta, tb = a, b
    cond = ta > tb
    a, b = a + 1, b + 1
    if cond:
        m = a; a += 1
    else:
        m = b; b += 1
    return a + b + m


# ---------------- recursion ----------------
def fibc(n):
    return n if n < 2 else fibc(n - 1) + fibc(n - 2)


def calls(n):
    return 1 if n < 2 else 1 + calls(n - 1) + calls(n - 2)


@gen(S, RE, "Recursive functions", n=100, diff="medium")
def r_rec(r):
    kind = r.choice(["fib", "calls", "sumdig", "pow", "ack", "bin", "gcd", "f2", "tri", "collatz", "mccarthy"])
    n = r.randint(4, 12)
    if kind == "fib": return nat(r, "What does f(%d) return?\n```c\nint f(int n) { return n < 2 ? n : f(n - 1) + f(n - 2); }\n```" % n, fibc(n), "Fibonacci numbers.")
    if kind == "calls": return nat(r, "How many times is f called (including the first call) when evaluating f(%d)?\n```c\nint f(int n) { if (n < 2) return n; return f(n - 1) + f(n - 2); }\n```" % n, calls(n), "calls(n) = 1 + calls(n−1) + calls(n−2).")
    if kind == "sumdig":
        v = r.randint(100, 99999)
        return nat(r, "What does f(%d) return?\n```c\nint f(int n) { return n == 0 ? 0 : n %% 10 + f(n / 10); }\n```" % v, sum(map(int, str(v))), "Digit sum.")
    if kind == "pow":
        b, e = r.randint(2, 4), r.randint(5, 14)
        return nat(r, "What does p(%d, %d) return?\n```c\nint p(int b, int e) {\n    if (e == 0) return 1;\n    int h = p(b, e / 2);\n    return e %% 2 ? h * h * b : h * h;\n}\n```" % (b, e), b ** e, "Fast exponentiation computes b^e.")
    if kind == "ack":
        m, k = r.randint(0, 2), r.randint(0, 4)

        def A(m, n): return n + 1 if m == 0 else A(m - 1, 1) if n == 0 else A(m - 1, A(m, n - 1))
        return nat(r, "What does A(%d, %d) return?\n```c\nint A(int m, int n) {\n    if (m == 0) return n + 1;\n    if (n == 0) return A(m - 1, 1);\n    return A(m - 1, A(m, n - 1));\n}\n```" % (m, k), A(m, k), "Evaluate the Ackermann recursion.")
    if kind == "bin":
        nn, k = r.randint(4, 10), r.randint(1, 4)
        return nat(r, "What does C(%d, %d) return?\n```c\nint C(int n, int k) { return (k == 0 || k == n) ? 1 : C(n - 1, k - 1) + C(n - 1, k); }\n```" % (nn, k), math.comb(nn, k), "Pascal's rule gives the binomial coefficient.")
    if kind == "gcd":
        a, b = r.randint(10, 300), r.randint(10, 300)
        def g(a, b, d=0):
            return (a, d) if b == 0 else g(b, a % b, d + 1)
        res = g(a, b)
        return nat(r, "How many recursive calls (excluding the first call) are made while evaluating g(%d, %d)?\n```c\nint g(int a, int b) { return b == 0 ? a : g(b, a %% b); }\n```" % (a, b), res[1], "Euclid's recursion depth.")
    if kind == "f2":
        return nat(r, "What does f(%d) return?\n```c\nint f(int n) { if (n <= 1) return 1; return f(n - 1) + f(n - 2) + 1; }\n```" % n, (lambda f: f(f, n))(lambda f, n: 1 if n <= 1 else f(f, n - 1) + f(f, n - 2) + 1), "T(n) = T(n−1) + T(n−2) + 1.")
    if kind == "tri": return nat(r, "What does f(%d) return?\n```c\nint f(int n) { return n == 0 ? 0 : n + f(n - 1); }\n```" % (n * 3), n * 3 * (n * 3 + 1) // 2, "Sum 1..n.")
    if kind == "collatz":
        s0 = r.randint(5, 30)
        def c(n): return 0 if n == 1 else 1 + c(n // 2 if n % 2 == 0 else 3 * n + 1)
        return nat(r, "What does f(%d) return?\n```c\nint f(int n) { if (n == 1) return 0; return 1 + f(n %% 2 ? 3 * n + 1 : n / 2); }\n```" % s0, c(s0), "Collatz steps.")
    k = r.randint(50, 110)
    def mc(n): return n - 10 if n > 100 else mc(mc(n + 11))
    return nat(r, "What does M(%d) return?\n```c\nint M(int n) { return n > 100 ? n - 10 : M(M(n + 11)); }\n```" % k, mc(k), "McCarthy 91 function: 91 for n ≤ 100, otherwise n − 10.")


@gen(S, RE, "Recursion traces", n=60, diff="medium")
def r_trace(r):
    n = r.randint(2, 5)
    kind = r.choice(["pre_post", "depth", "stack"])
    if kind == "pre_post":
        out = []
        def f(k):
            if k > 0:
                out.append(k); f(k - 1); out.append(k)
        f(n)
        s = "".join(map(str, out))
        return mcq(r, "What is printed by the call f(%d)?\n```c\nvoid f(int n) {\n    if (n > 0) {\n        printf(\"%%d\", n);\n        f(n - 1);\n        printf(\"%%d\", n);\n    }\n}\n```" % n, s, ["".join(map(str, sorted(out))), "".join(map(str, range(n, 0, -1))), "".join(map(str, range(1, n + 1))), s[::-1] if s != s[::-1] else "".join(map(str, list(range(n, 0, -1)) + [0] + list(range(1, n + 1))))], "Pre-order prints on the way down, post-order on the way up: %s." % s)
    if kind == "depth":
        d = r.randint(5, 20)
        return nat(r, "Function f(n) calls f(n/2) (integer division) while n > 1. What is the maximum recursion depth (number of simultaneously active calls) for f(%d)?" % (2 ** d), d + 1, "Calls for n = 2^d, …, 2, 1: d + 1.")
    out = []
    def g(k):
        if k == 0: return 0
        out.append(k)
        return g(k - 1) + g(k - 2 if k >= 2 else 0)
    g(n + 1)
    return nat(r, "How many times is g invoked in total for g(%d)?\n```c\nint g(int k) { if (k == 0) return 0; return g(k - 1) + g(k >= 2 ? k - 2 : 0); }\n```" % (n + 1), _gcalls(n + 1), "Count calls recursively.")


def _gcalls(k):
    if k == 0: return 1
    return 1 + _gcalls(k - 1) + _gcalls(k - 2 if k >= 2 else 0)


# ---------------- arrays, stacks, queues ----------------
def postfix_eval(tokens):
    st = []
    for t in tokens:
        if t.lstrip("-").isdigit(): st.append(int(t))
        else:
            b, a = st.pop(), st.pop()
            st.append({"+": a + b, "-": a - b, "*": a * b, "/": cdiv(a, b)}[t])
    return st[0]


@gen(S, ASQ, "Expression evaluation", n=80, diff="medium")
def a_postfix(r):
    n = r.randint(3, 5)
    toks = [str(r.randint(1, 9)), str(r.randint(1, 9))]
    nums_left = n - 2
    ops_left = n - 1
    out = list(toks)
    depth = 2
    while nums_left or ops_left:
        if nums_left and (depth < 2 or r.random() < 0.5):
            out.append(str(r.randint(1, 9))); nums_left -= 1; depth += 1
        elif ops_left and depth >= 2:
            out.append(r.choice("+-*")); ops_left -= 1; depth -= 1
        else:
            out.append(str(r.randint(1, 9))); nums_left -= 1; depth += 1
    if depth != 1: raise Skip()
    v = postfix_eval(out)
    return nat(r, "Evaluate the postfix expression:  %s" % " ".join(out), v, "Use a stack; result %d." % v)


def to_postfix(tokens):
    prec = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
    out, st = [], []
    for t in tokens:
        if t.isalpha(): out.append(t)
        elif t == "(": st.append(t)
        elif t == ")":
            while st[-1] != "(": out.append(st.pop())
            st.pop()
        else:
            while st and st[-1] != "(" and (prec[st[-1]] > prec[t] or (prec[st[-1]] == prec[t] and t != "^")): out.append(st.pop())
            st.append(t)
    while st: out.append(st.pop())
    return out


@gen(S, ASQ, "Expression evaluation", n=60, diff="medium", marks=2)
def a_infix(r):
    vs = list("abcdef")
    k = r.randint(3, 5)
    toks = []
    for i in range(k):
        toks.append(vs[i])
        if i < k - 1: toks.append(r.choice("+-*/"))
    if r.random() < 0.6 and k >= 4:
        i = 2 * r.randint(0, k - 3)
        toks = toks[:i] + ["("] + toks[i:i + 3] + [")"] + toks[i + 3:]
    p = to_postfix(toks)
    s = " ".join(p)
    wrong = {" ".join(to_postfix([t for t in toks if t not in "()"]))}
    wrong |= {" ".join(p[::-1]), " ".join(sorted(p, key=lambda x: not x.isalpha()))}
    alt = list(p)
    for i in range(len(alt) - 1):
        if not alt[i].isalpha() and alt[i + 1].isalpha():
            alt[i], alt[i + 1] = alt[i + 1], alt[i]; break
    wrong.add(" ".join(alt))
    return mcq(r, "Convert the infix expression  %s  to postfix (standard precedence, left associative)." % " ".join(toks), s, list(wrong), "Shunting-yard algorithm.")


@gen(S, ASQ, "Stack permutations", n=60, diff="hard", marks=2)
def a_stackperm(r):
    n = r.randint(4, 5)
    def possible(seq):
        st, nxt = [], 1
        for x in seq:
            while (not st or st[-1] != x) and nxt <= n:
                st.append(nxt); nxt += 1
            if not st or st[-1] != x: return False
            st.pop()
        return True
    perms = list(itertools.permutations(range(1, n + 1)))
    good = [p for p in perms if possible(p)]
    bad = [p for p in perms if not possible(p)]
    if r.random() < 0.5:
        return nat(r, "Elements 1, 2, …, %d are pushed in this order onto a stack, with pops interleaved arbitrarily. How many different pop sequences are possible?" % n, len(good), "Catalan number C_%d = %d." % (n, len(good)))
    t = r.sample(good, 2); f = r.sample(bad, 2)
    return msq(r, "Elements 1..%d are pushed in order onto an initially empty stack (pops may be interleaved). Which of the following can be the order in which they are popped? (select all)" % n,
               ["".join(map(str, x)) for x in t], ["".join(map(str, x)) for x in f], "Simulate push/pop; a sequence is valid iff each pop matches the stack top.")


@gen(S, ASQ, "Queues", n=70, diff="easy")
def a_queue(r):
    cap = r.randint(5, 12)
    kind = r.choice(["count", "full", "maxsz", "front"])
    f = r.randint(0, cap - 1)
    k = r.randint(0, cap - 1)
    rear = (f + k) % cap
    if kind == "count": return nat(r, "A circular queue of capacity %d (array indices 0..%d) uses variables front and rear where front is the index of the first element and rear the index of the LAST element. If front = %d and rear = %d and the queue is non-empty and holds fewer than %d elements, how many elements does it hold?" % (cap, cap - 1, f, rear, cap + 1), (rear - f) % cap + 1, "(rear − front) mod cap + 1.")
    if kind == "full": return nat(r, "A circular queue implemented in an array of size %d keeps one slot empty to distinguish full from empty. Maximum number of elements it can hold?" % cap, cap - 1, "n − 1.")
    if kind == "maxsz": return nat(r, "Two queues are used to implement one stack. Pushing is O(1) and popping moves n−1 elements. Total element moves to pop everything from a stack holding %d items?" % cap, sum(range(cap)), "Pops move n−1, n−2, …, 0 elements.")
    ops = [r.choice(["E", "D"]) for _ in range(r.randint(8, 14))]
    q, ok = deque(), 0
    seq = []
    for i, o in enumerate(ops):
        if o == "E": q.append(i);
        elif q: q.popleft()
    return nat(r, "Starting from an empty queue, the following operations are applied in order (E = enqueue a distinct element, D = dequeue; dequeue on an empty queue does nothing): %s. How many elements remain?" % " ".join(ops), len(q), "Simulate.")


# ---------------- linked lists ----------------
@gen(S, LL, "List operations", n=70, diff="medium")
def ll_ops(r):
    L = r.sample(range(1, 30), r.randint(4, 6))
    cur = list(L)
    steps = []
    for _ in range(r.randint(3, 5)):
        op = r.choice(["insf", "insr", "delf", "delr", "rev"])
        v = r.randint(31, 60)
        if op == "insf": cur.insert(0, v); steps.append("insert %d at the head" % v)
        elif op == "insr": cur.append(v); steps.append("insert %d at the tail" % v)
        elif op == "delf" and len(cur) > 1: cur.pop(0); steps.append("delete the head")
        elif op == "delr" and len(cur) > 1: cur.pop(); steps.append("delete the tail")
        elif op == "rev": cur.reverse(); steps.append("reverse the list")
    k = r.randint(0, len(cur) - 1)
    return nat(r, "A singly linked list initially holds %s (head first). Operations applied in order: %s. What is the value of the node at position %d (0 = head) in the final list?" % (L, "; ".join(steps), k), cur[k], "Final list: %s." % cur)


@gen(S, LL, "Cycle detection", n=50, diff="hard", marks=2)
def ll_cycle(r):
    mu, lam = r.randint(1, 8), r.randint(2, 9)
    kind = r.choice(["meet", "len", "ptrs"])
    nxt = lambda i: i + 1 if i < mu + lam - 1 else mu
    if kind == "meet":
        s = f = 0
        t = 0
        while True:
            s, f = nxt(s), nxt(nxt(f)); t += 1
            if s == f: break
        return nat(r, "A singly linked list has %d nodes before a cycle begins and the cycle has %d nodes (the tail points back to the first node of the cycle). Floyd's algorithm starts both `slow` (1 step) and `fast` (2 steps) at the head. After how many iterations do they first meet?" % (mu, lam), t, "Simulate: meeting after %d iterations." % t)
    if kind == "len": return nat(r, "A linked list has %d distinct nodes reachable from the head; the last node points back to node number %d (1-indexed). How many nodes are in the cycle?" % (mu + lam, mu + 1), lam, "Cycle length = total − (index of re-entry − 1).")
    n = r.randint(4, 12)
    return nat(r, "Number of pointer (next) fields that must be changed to reverse a singly linked list of %d nodes in place (head pointer excluded)?" % n, n, "Every node's next field is changed (the old head's next becomes NULL).")


# ---------------- trees ----------------
class BST:
    def __init__(self): self.root = None

    def insert(self, k):
        if self.root is None: self.root = [k, None, None]; return
        n = self.root
        while True:
            i = 1 if k < n[0] else 2
            if n[i] is None: n[i] = [k, None, None]; return
            n = n[i]


def height(n): return -1 if n is None else 1 + max(height(n[1]), height(n[2]))
def inorder(n): return [] if n is None else inorder(n[1]) + [n[0]] + inorder(n[2])
def preorder(n): return [] if n is None else [n[0]] + preorder(n[1]) + preorder(n[2])
def postorder(n): return [] if n is None else postorder(n[1]) + postorder(n[2]) + [n[0]]
def leaves(n): return 0 if n is None else (1 if n[1] is None and n[2] is None else leaves(n[1]) + leaves(n[2]))


@gen(S, TR, "BST", n=100, diff="easy")
def t_bst(r):
    keys = r.sample(range(1, 60), r.randint(6, 9))
    t = BST()
    for k in keys: t.insert(k)
    kind = r.choice(["h", "pre", "post", "leaves", "root_left", "depth"])
    ks = " ".join(map(str, keys))
    if kind == "h": return nat(r, "Keys %s are inserted in this order into an initially empty BST. Height of the tree (edges on the longest root-to-leaf path)?" % ks, height(t.root), "Build the BST: height %d." % height(t.root))
    if kind == "pre": return mcq(r, "Keys %s are inserted into an empty BST. Its preorder traversal is" % ks, " ".join(map(str, preorder(t.root))), [" ".join(map(str, postorder(t.root))), " ".join(map(str, inorder(t.root))), " ".join(map(str, keys[::-1])), " ".join(map(str, sorted(keys, reverse=True)))], "Build the BST then traverse root-left-right.")
    if kind == "post": return mcq(r, "Keys %s are inserted into an empty BST. Its postorder traversal is" % ks, " ".join(map(str, postorder(t.root))), [" ".join(map(str, preorder(t.root))), " ".join(map(str, inorder(t.root))), " ".join(map(str, keys)), " ".join(map(str, sorted(keys, reverse=True)))], "Left-right-root.")
    if kind == "leaves": return nat(r, "Keys %s are inserted into an empty BST. How many leaf nodes does it have?" % ks, leaves(t.root), "Nodes with no children.")
    if kind == "root_left": return nat(r, "Keys %s are inserted into an empty BST. How many nodes are in the LEFT subtree of the root?" % ks, len(inorder(t.root[1])), "Keys smaller than the root %d." % keys[0])
    k = keys[-1]
    d, n = 0, t.root
    while n[0] != k: n = n[1] if k < n[0] else n[2]; d += 1
    return nat(r, "Keys %s are inserted into an empty BST. What is the depth (edges from the root) of the node with key %d?" % (ks, k), d, "Follow the search path.")


def rebuild(pre, ino):
    if not pre: return None
    root = pre[0]
    i = ino.index(root)
    return [root, rebuild(pre[1:i + 1], ino[:i]), rebuild(pre[i + 1:], ino[i + 1:])]


@gen(S, TR, "Tree traversals", n=70, diff="medium", marks=2)
def t_rebuild(r):
    keys = r.sample(range(1, 30), r.randint(6, 8))
    t = BST()
    for k in keys: t.insert(k)
    pre, ino = preorder(t.root), inorder(t.root)
    kind = r.choice(["post", "height"])
    if kind == "post":
        # structure from pre+in; use arbitrary (non-BST) labels for variety
        lab = r.sample("ABCDEFGHJK", len(pre))
        m = dict(zip(sorted(keys), lab))
        pr, io = [m[k] for k in pre], [m[k] for k in ino]
        po = [m[k] for k in postorder(t.root)]
        return mcq(r, "A binary tree has preorder  %s  and inorder  %s . Its postorder traversal is" % (" ".join(pr), " ".join(io)), " ".join(po), [" ".join(po[::-1]), " ".join(io[::-1]), " ".join(pr[::-1]), " ".join(sorted(po))], "Rebuild the tree using the root from preorder and the split from inorder.")
    return nat(r, "A binary tree has preorder %s and inorder %s. What is its height (edges on the longest path)?" % (pre, ino), height(t.root), "Rebuild: height %d." % height(t.root))


@gen(S, TR, "Tree properties", n=70, diff="easy")
def t_props(r):
    n = r.randint(5, 40)
    h = r.randint(2, 7)
    kind = r.choice(["maxnodes", "minh", "nulls", "leaves", "avl", "internal", "complete_leaves", "kary"])
    if kind == "maxnodes": return nat(r, "Maximum number of nodes in a binary tree of height %d (height = edges on the longest path)?" % h, 2 ** (h + 1) - 1, "2^(h+1) − 1.")
    if kind == "minh": return nat(r, "Minimum possible height (edges) of a binary tree with %d nodes?" % n, math.floor(math.log2(n)), "⌊log₂ n⌋.")
    if kind == "nulls": return nat(r, "A binary tree has %d nodes. How many NULL child pointers does its standard linked representation contain?" % n, n + 1, "n nodes have 2n pointers, n−1 are used ⇒ n + 1 are NULL.")
    if kind == "leaves": return nat(r, "A full binary tree (every node has 0 or 2 children) has %d internal nodes. How many leaves does it have?" % n, n + 1, "L = I + 1.")
    if kind == "avl":
        N = [1, 2]
        while len(N) <= h: N.append(N[-1] + N[-2] + 1)
        return nat(r, "Minimum number of nodes in an AVL tree of height %d (a single node has height 0)?" % h, N[h] if False else [1, 2, 4, 7, 12, 20, 33, 54][h], "N(h) = N(h−1) + N(h−2) + 1 with N(0) = 1, N(1) = 2.")
    if kind == "internal": return nat(r, "A complete binary tree has %d nodes. How many are leaves?" % n, n - n // 2, "⌈n/2⌉ leaves.")
    k = r.randint(3, 5)
    return nat(r, "In a full %d-ary tree with %d internal nodes, how many leaves are there?" % (k, h + 1), (k - 1) * (h + 1) + 1, "L = (k − 1)·I + 1.")


def avl_insert_rotations(keys):
    rot = [0]

    def h(n): return n["h"] if n else 0
    def upd(n): n["h"] = 1 + max(h(n["l"]), h(n["r"]))
    def rr(y):
        x = y["l"]; y["l"] = x["r"]; x["r"] = y; upd(y); upd(x); rot[0] += 1; return x
    def rl(x):
        y = x["r"]; x["r"] = y["l"]; y["l"] = x; upd(x); upd(y); rot[0] += 1; return y
    def ins(n, k):
        if not n: return {"k": k, "l": None, "r": None, "h": 1}
        if k < n["k"]: n["l"] = ins(n["l"], k)
        else: n["r"] = ins(n["r"], k)
        upd(n)
        b = h(n["l"]) - h(n["r"])
        if b > 1:
            if k > n["l"]["k"]: n["l"] = rl(n["l"])
            return rr(n)
        if b < -1:
            if k < n["r"]["k"]: n["r"] = rr(n["r"])
            return rl(n)
        return n
    root = None
    for k in keys: root = ins(root, k)
    return rot[0], h(root) - 1


@gen(S, TR, "AVL trees", n=80, diff="hard", marks=2)
def t_avl(r):
    keys = r.sample(range(1, 50), r.randint(6, 9))
    rot, ht = avl_insert_rotations(keys)
    if r.random() < 0.5: return nat(r, "Keys %s are inserted one by one into an empty AVL tree (a single left or right rotation counts as 1, a double rotation counts as 2). Total number of rotations performed?" % keys, rot, "Simulate AVL insertions with rebalancing.")
    return nat(r, "Keys %s are inserted into an empty AVL tree. What is the height of the final tree (single node = 0)?" % keys, ht, "Simulate AVL insertions.")


# ---------------- heaps & hashing ----------------
@gen(S, HH, "Binary heaps", n=70, diff="medium")
def h_heap(r):
    keys = r.sample(range(1, 50), r.randint(5, 8))
    import heapq
    h = []
    for k in keys: h.append(k); i = len(h) - 1;
    arr = []
    for k in keys:
        arr.append(k); i = len(arr) - 1
        while i > 0 and arr[(i - 1) // 2] > arr[i]:
            arr[(i - 1) // 2], arr[i] = arr[i], arr[(i - 1) // 2]; i = (i - 1) // 2
    kind = r.choice(["arr", "extract", "last"])
    ks = " ".join(map(str, keys))
    if kind == "arr": return mcq(r, "Keys %s are inserted one at a time into an empty MIN-heap (array representation, sift-up). The final array is" % ks, str(arr), [str(sorted(keys)), str(sorted(keys, reverse=True)), str(keys), str(arr[::-1])], "Insert at the end, then swap with parent while smaller.")
    if kind == "extract":
        a = list(arr); a[0] = a.pop(); i = 0; n = len(a)
        while True:
            l, rr_, m = 2 * i + 1, 2 * i + 2, i
            if l < n and a[l] < a[m]: m = l
            if rr_ < n and a[rr_] < a[m]: m = rr_
            if m == i: break
            a[i], a[m] = a[m], a[i]; i = m
        return mcq(r, "Keys %s are inserted into an empty min-heap (sift-up), then extract-min is performed (last element moved to the root, then sifted down). The resulting array is" % ks, str(a), [str(arr[1:]), str(sorted(arr)[1:]), str(arr[::-1][:-1]), str(a[::-1])], "Replace root with last element and sift down.")
    return nat(r, "Keys %s are inserted into an empty min-heap using sift-up. What is the value stored in the last position of the array?" % ks, arr[-1], "Final array: %s." % arr)


@gen(S, HH, "d-ary heaps & indices", n=40, diff="easy")
def h_idx(r):
    d, i = r.choice([2, 3, 4]), r.randint(4, 40)
    kind = r.choice(["parent", "child", "levels"])
    if kind == "parent": return nat(r, "In a %d-ary heap stored in a 0-indexed array, what is the index of the parent of the element at index %d?" % (d, i), (i - 1) // d, "⌊(i − 1)/d⌋.")
    if kind == "child": return nat(r, "In a %d-ary heap stored in a 0-indexed array, what is the index of the FIRST child of the element at index %d?" % (d, i), d * i + 1, "d·i + 1.")
    n = r.randint(10, 500)
    h, tot, w = 0, 1, 1
    while tot < n: w *= d; tot += w; h += 1
    return nat(r, "Height (in edges) of a complete %d-ary heap with %d nodes?" % (d, n), h, "Smallest h with (d^(h+1) − 1)/(d − 1) ≥ n.")


@gen(S, HH, "Hash tables", n=60, diff="medium")
def h_hash(r):
    m = r.choice([5, 7, 8, 10, 11])
    keys = r.sample(range(10, 200), r.randint(6, 10))
    tab = [[] for _ in range(m)]
    for k in keys: tab[k % m].append(k)
    kind = r.choice(["longest", "empty", "load", "probes"])
    h = "h(k) = k mod %d" % m
    ks = " ".join(map(str, keys))
    if kind == "longest": return nat(r, "Keys %s are inserted into a hash table with chaining, %s. Length of the longest chain?" % (ks, h), max(map(len, tab)), "Bucket sizes: %s." % [len(x) for x in tab])
    if kind == "empty": return nat(r, "Keys %s are inserted into a hash table with chaining, %s. How many buckets remain empty?" % (ks, h), sum(1 for x in tab if not x), "Bucket sizes: %s." % [len(x) for x in tab])
    if kind == "load": return nat(r, "A hash table of %d slots using chaining stores %d keys. Load factor (up to 3 decimals)?" % (m, len(keys)), round(len(keys) / m, 3), "n/m.", tol=0.001)
    srch = sum(len(x) * (len(x) + 1) // 2 for x in tab)
    return nat(r, "Keys %s are inserted into a hash table with chaining (new keys appended at the END of a chain), %s. If every key is searched exactly once, the total number of key comparisons for successful searches is" % (ks, h), srch, "Position-in-chain summed over all keys: %d." % srch)


# ---------------- graph representation ----------------
def rand_dgraph(r, n, p, directed=False):
    e = set()
    for a in range(n):
        for b in range(n):
            if a != b and r.random() < p:
                if directed or (b, a) not in e: e.add((a, b))
    return sorted(e)


def adj(n, e, directed):
    a = {i: [] for i in range(n)}
    for x, y in e:
        a[x].append(y)
        if not directed: a[y].append(x)
    return {k: sorted(v) for k, v in a.items()}


def bfs(a, s):
    seen, q, out = {s}, deque([s]), []
    while q:
        u = q.popleft(); out.append(u)
        for v in a[u]:
            if v not in seen: seen.add(v); q.append(v)
    return out


def dfs(a, s, seen=None, out=None):
    seen = seen if seen is not None else set(); out = out if out is not None else []
    seen.add(s); out.append(s)
    for v in a[s]:
        if v not in seen: dfs(a, v, seen, out)
    return out


@gen(S, GR, "Traversals", n=90, diff="medium")
def g_trav(r):
    n = r.randint(5, 7)
    e = rand_dgraph(r, n, 0.35)
    if len(e) < n: raise Skip()
    a = adj(n, e, False)
    nm = lambda i: chr(65 + i)
    kind = r.choice(["bfs", "dfs", "comp"])
    es = ", ".join(nm(x) + nm(y) for x, y in e)
    ctx = "Undirected graph on vertices A–%s with edges %s. Neighbours are visited in alphabetical order." % (nm(n - 1), es)
    if kind == "comp":
        seen, c = set(), 0
        for i in range(n):
            if i not in seen: c += 1; dfs(a, i, seen)
        return nat(r, ctx + " Number of connected components?", c, "Run DFS from each unvisited vertex.")
    order = bfs(a, 0) if kind == "bfs" else dfs(a, 0)
    s = "".join(map(nm, order))
    wrong = {"".join(map(nm, sorted(order))), "".join(map(nm, (dfs(a, 0) if kind == "bfs" else bfs(a, 0)))), "".join(map(nm, order[::-1]))}
    o2 = list(order)
    if len(o2) > 3: o2[1], o2[2] = o2[2], o2[1]
    wrong.add("".join(map(nm, o2)))
    return mcq(r, ctx + " A %s starting from A visits the vertices in the order" % ("BFS" if kind == "bfs" else "DFS"), s, list(wrong), "Simulate the traversal.")


@gen(S, GR, "Representation costs", n=70, diff="easy")
def g_rep(r):
    n, e = r.randint(10, 200), r.randint(10, 400)
    kind = r.choice(["mat", "list", "edges", "indeg", "tc", "degsum"])
    if kind == "mat": return nat(r, "An adjacency matrix of an unweighted directed graph on %d vertices stores one BIT per entry. How many bytes (rounded up) does it need?" % n, math.ceil(n * n / 8), "n²/8.")
    if kind == "list": return nat(r, "An undirected graph with %d vertices and %d edges is stored as adjacency lists. How many list entries (neighbour nodes) are stored in total?" % (n, e), 2 * e, "Each undirected edge appears twice.")
    if kind == "edges":
        m = r.randint(4, 9)
        mat = [[1 if (i != j and r.random() < 0.4) else 0 for j in range(m)] for i in range(m)]
        sym = [[mat[i][j] | mat[j][i] for j in range(m)] for i in range(m)]
        return nat(r, "The adjacency matrix of an undirected simple graph is\n```\n%s\n```\nHow many edges does the graph have?" % "\n".join(" ".join(map(str, row)) for row in sym), sum(map(sum, sym)) // 2, "Sum of entries / 2.")
    if kind == "indeg":
        m = r.randint(4, 7)
        ed = rand_dgraph(r, m, 0.4, True)
        v = r.randrange(m)
        return nat(r, "Directed graph on vertices 0..%d with edges %s. Compute the in-degree of vertex %d." % (m - 1, ed, v), sum(1 for x, y in ed if y == v), "Count edges ending at the vertex.")
    if kind == "tc":
        return nat(r, "A graph on %d vertices is stored as an adjacency matrix. How many matrix entries must be scanned to list ALL neighbours of one given vertex?" % n, n, "One full row (or column) of n entries.")
    return nat(r, "A simple undirected graph has degrees %s. How many edges does it have?" % (lambda d: sorted(d))([2, 3, 3, 2, 4, 2]), 8, "Σdeg / 2 = 16/2.")
