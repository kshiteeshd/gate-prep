"""Algorithms — parametric generators (every answer is computed by running the algorithm)."""
import heapq
import itertools
import math
from fractions import Fraction

from content.kit import *

S = "ALGO"
AS, RC, SS, GR, DP, GA_, CC = ("Asymptotic Analysis", "Recurrences & Divide and Conquer", "Sorting & Searching",
                               "Greedy Algorithms", "Dynamic Programming", "Graph Algorithms", "Complexity Classes")

# ---------------- asymptotics ----------------
FUNCS = [("100", 0), ("log log n", 1), ("log n", 2), ("log(n²)", 2), ("√n", 3), ("5√n", 3), ("n", 4), ("3n + 7", 4),
         ("n log n", 5), ("n log(n²)", 5), ("n^1.5", 6), ("n²", 7), ("n² + n log n", 7), ("n² log n", 8), ("n³", 9),
         ("2ⁿ", 10), ("2ⁿ⁺¹", 10), ("3ⁿ", 11), ("4ⁿ", 12), ("n!", 13), ("nⁿ", 14)]


def distinct_classes(r, k):
    while True:
        f = r.sample(FUNCS, k)
        if len({c for _, c in f}) == k:
            return f


@gen(S, AS, "Growth rates", n=40, diff="easy")
def a_growth_max(r):
    f = distinct_classes(r, 4)
    hi = max(f, key=lambda x: x[1])
    return mcq(r, "Which of the following functions grows the fastest asymptotically?", hi[0], [x[0] for x in f if x != hi], "Order by class: %s." % ", ".join(x[0] for x in sorted(f, key=lambda x: x[1])))


@gen(S, AS, "Growth rates", n=40, diff="medium")
def a_growth_order(r):
    f = distinct_classes(r, 4)
    srt = sorted(f, key=lambda x: x[1])
    ans = " < ".join(x[0] for x in srt)
    wrong = []
    for _ in range(12):
        p = r.sample(f, 4)
        s = " < ".join(x[0] for x in p)
        if s != ans:
            wrong.append(s)
    return mcq(r, "Arrange in increasing order of asymptotic growth:\n" + ",  ".join(x[0] for x in f), ans, wrong, "Slowest to fastest: " + ans)


@gen(S, AS, "Asymptotic notation", n=60, diff="medium", marks=2)
def a_notation_msq(r):
    f, g = r.sample(FUNCS, 2)
    if f[1] == g[1] and r.random() < 0.5:
        raise Skip()
    cands = [("f(n) = O(g(n))", f[1] <= g[1]), ("f(n) = Ω(g(n))", f[1] >= g[1]), ("f(n) = Θ(g(n))", f[1] == g[1]),
             ("f(n) = o(g(n))", f[1] < g[1]), ("f(n) = ω(g(n))", f[1] > g[1]), ("g(n) = O(f(n))", g[1] <= f[1])]
    t = [s for s, v in cands if v]
    fa = [s for s, v in cands if not v]
    if not t or len(fa) < 1:
        raise Skip()
    k = min(len(t), 2)
    ts = r.sample(t, k)
    fs = r.sample(fa, min(len(fa), 4 - k))
    if len(ts) + len(fs) < 4:
        raise Skip()
    return msq(r, "Let f(n) = %s and g(n) = %s. Select ALL true statements." % (f[0], g[0]), ts, fs, "Classes: f in class %d, g in class %d (higher = faster growth)." % (f[1], g[1]))


def loop_src(kind, n, c):
    return {
        "mul": ("for (i = 1; i < n; i = i * %d)\n    count++;" % c, lambda: sum(1 for _ in iter_mul(n, c))),
        "div": ("for (i = n; i >= 1; i = i / %d)\n    count++;" % c, lambda: sum(1 for _ in iter_div(n, c))),
        "tri": ("for (i = 1; i <= n; i++)\n    for (j = 1; j <= i; j++)\n        count++;", lambda: n * (n + 1) // 2),
        "nlog": ("for (i = 1; i <= n; i++)\n    for (j = 1; j < n; j = j * %d)\n        count++;" % c, lambda: n * sum(1 for _ in iter_mul(n, c))),
        "dep": ("for (i = 1; i <= n; i = i * %d)\n    for (j = 1; j <= i; j++)\n        count++;" % c, lambda: sum(i for i in iter_mul(n + 1, c, True))),
        "step": ("for (i = 0; i < n; i += %d)\n    count++;" % c, lambda: -(-n // c)),
        "tri2": ("for (i = 1; i <= n; i++)\n    for (j = i; j <= n; j += i)\n        count++;", lambda: sum(n // i for i in range(1, n + 1))),
    }[kind]


def iter_mul(n, c, incl=False):
    i = 1
    while (i <= n - 1 if incl else i < n):
        yield i
        i *= c


def iter_div(n, c):
    i = n
    while i >= 1:
        yield i
        i //= c


@gen(S, AS, "Loop analysis", n=70, diff="easy")
def a_loops(r):
    kind = r.choice(["mul", "div", "tri", "step", "dep", "tri2", "nlog"])
    c = r.choice([2, 3, 4]) if kind not in ("tri", "tri2") else 0
    n = r.choice([8, 16, 32, 64, 100, 81, 27, 10, 12, 20, 30, 50, 64, 128]) if kind in ("mul", "div", "nlog", "dep", "step") else r.randint(4, 20)
    src, fn = loop_src(kind, n, c)
    v = fn()
    if v > 5000 or v < 2:
        raise Skip()
    return nat(r, "What is the final value of count (initially 0) for n = %d?\n```c\n%s\n```" % (n, src), v, "Simulating the loop gives %d." % v)


@gen(S, AS, "Loop analysis", n=20, diff="medium")
def a_loops_o(r):
    opts = {"for (i = 1; i <= n; i++) for (j = 1; j <= i; j++) k++;": "Θ(n²)", "for (i = 1; i <= n; i *= 2) k++;": "Θ(log n)",
            "for (i = 1; i <= n; i++) for (j = 1; j <= n; j *= 2) k++;": "Θ(n log n)", "for (i = 1; i <= n; i *= 2) for (j = 1; j <= i; j++) k++;": "Θ(n)",
            "for (i = n; i >= 1; i /= 2) for (j = 1; j <= n; j++) k++;": "Θ(n log n)", "for (i = 1; i * i <= n; i++) k++;": "Θ(√n)",
            "for (i = 1; i <= n; i++) for (j = i; j <= n; j += i) k++;": "Θ(n log n)", "for (i = 2; i <= n; i = i * i) k++;": "Θ(log log n)"}
    src, ans = r.choice(list(opts.items()))
    return mcq(r, "The running time of the following fragment is\n```c\n%s\n```" % src, ans, [x for x in ["Θ(n²)", "Θ(log n)", "Θ(n log n)", "Θ(n)", "Θ(√n)", "Θ(log log n)", "Θ(n³)"] if x != ans], "Count iterations of the loops.")


# ---------------- recurrences ----------------
@gen(S, RC, "Master theorem", n=60, diff="medium")
def a_master(r):
    a, b = r.choice([(1, 2), (2, 2), (3, 2), (4, 2), (8, 2), (9, 3), (2, 4), (4, 4), (7, 2), (1, 3), (3, 3), (16, 4)])
    k = r.choice([0, 1, 2, 3])
    L = math.log(a, b)
    if abs(L - k) < 1e-9:
        res = "Θ(n^%d log n)" % k if k > 1 else ("Θ(n log n)" if k == 1 else "Θ(log n)")
    elif L > k:
        e = round(L, 3)
        res = "Θ(n^%s)" % fmt(e) if not float(L).is_integer() else "Θ(n^%d)" % int(L) if int(L) > 1 else "Θ(n)"
    else:
        res = "Θ(n^%d)" % k if k > 1 else ("Θ(n)" if k == 1 else "Θ(1)")
    rhs = {0: "1", 1: "n", 2: "n²", 3: "n³"}[k]
    ws = ["Θ(n^%s)" % fmt(round(L, 3)), "Θ(n log n)", "Θ(n²)", "Θ(n)", "Θ(log n)", "Θ(n² log n)", "Θ(n³)", "Θ(1)", "Θ(n^%d log n)" % max(k, 1), "Θ(n^%d)" % (k + 1)]
    return mcq(r, "Solve T(n) = %sT(n/%d) + %s (T(1) = 1) using the Master theorem:" % ("" if a == 1 else str(a), b, rhs), res, ws,
               "log_%d %d = %s vs f(n) = Θ(n^%d)." % (b, a, fmt(round(L, 3)), k))


@gen(S, RC, "Recurrence evaluation", n=50, diff="easy")
def a_rec_val(r):
    kind = r.choice(["lin", "half", "dbl", "fib", "sq"])
    if kind == "lin":
        c, n0 = r.randint(1, 5), r.randint(5, 12)
        v = 1 + sum(c * i for i in range(2, n0 + 1))
        t = "T(n) = T(n − 1) + %sn, T(1) = 1" % ("" if c == 1 else c)
        n = n0
    elif kind == "half":
        k = r.randint(3, 8)
        n = 2 ** k
        v = 1 + k * 1
        t = "T(n) = T(n/2) + 1, T(1) = 1"
    elif kind == "dbl":
        k = r.randint(2, 6)
        n = 2 ** k
        v = n + k * n
        t = "T(n) = 2T(n/2) + n, T(1) = 1"
    elif kind == "fib":
        n = r.randint(6, 14)
        a, b = 1, 1
        for _ in range(n - 2):
            a, b = b, a + b
        v = b
        t = "T(n) = T(n − 1) + T(n − 2), T(1) = T(2) = 1"
    else:
        n = r.randint(3, 9)
        v = 1
        for i in range(2, n + 1):
            v = v + 2 * i - 1
        t = "T(n) = T(n − 1) + 2n − 1, T(1) = 1"
    return nat(r, "For the recurrence %s, the value of T(%d) is" % (t, n), v, "Expand/iterate the recurrence: T(%d) = %d." % (n, v))


@gen(S, RC, "Binary search / merge", n=40, diff="easy")
def a_dc_basic(r):
    kind = r.choice(["bs", "merge", "maxmin", "second"])
    if kind == "bs":
        n = r.choice([15, 31, 100, 127, 255, 1000, 1023, 2000, 500, 64, 10 ** 6])
        return nat(r, "Worst-case number of element comparisons in binary search on a sorted array of %d elements (one three-way comparison per probe counted as one)?" % n, math.floor(math.log2(n)) + 1,
                   "⌊log₂ n⌋ + 1 = %d." % (math.floor(math.log2(n)) + 1))
    if kind == "merge":
        m, n = r.randint(3, 40), r.randint(3, 40)
        return nat(r, "Two sorted lists of %d and %d elements are merged into one sorted list. Worst-case number of comparisons?" % (m, n), m + n - 1, "m + n − 1 = %d." % (m + n - 1))
    if kind == "maxmin":
        n = r.randint(5, 100)
        return nat(r, "Minimum number of comparisons needed in the worst case to find BOTH the maximum and the minimum of %d distinct numbers?" % n, math.ceil(3 * n / 2) - 2, "⌈3n/2⌉ − 2 = %d." % (math.ceil(3 * n / 2) - 2))
    n = r.choice([4, 8, 16, 32, 64, 100, 1000])
    v = n + math.ceil(math.log2(n)) - 2
    return nat(r, "Minimum comparisons in the worst case to find the SECOND smallest of %d distinct elements?" % n, v, "n + ⌈log₂ n⌉ − 2 = %d." % v)


@gen(S, RC, "Divide and conquer", n=30, diff="medium", marks=2)
def a_dc_adv(r):
    k = r.randint(2, 7)
    kind = r.choice(["strassen", "karatsuba", "mergecmp", "hanoi"])
    if kind == "strassen":
        return nat(r, "Strassen's algorithm multiplies two %d × %d matrices (n = 2^%d) by recursing down to 1 × 1 blocks. How many scalar multiplications does it perform?" % (2 ** k, 2 ** k, k), 7 ** k, "T(n) = 7T(n/2) ⇒ 7^%d = %d." % (k, 7 ** k))
    if kind == "karatsuba":
        return nat(r, "Karatsuba multiplication of two %d-digit numbers (n = 2^%d) splits into 3 half-size products until single-digit. Number of single-digit multiplications?" % (2 ** k, k), 3 ** k, "T(n) = 3T(n/2), T(1) = 1 ⇒ 3^%d = %d." % (k, 3 ** k))
    if kind == "hanoi":
        n = r.randint(3, 12)
        return nat(r, "Minimum number of moves to solve the Tower of Hanoi with %d disks?" % n, 2 ** n - 1, "T(n) = 2T(n−1) + 1 ⇒ 2^n − 1 = %d." % (2 ** n - 1))
    n = 2 ** k

    def mc(n):
        return 0 if n == 1 else mc(n // 2) * 2 + n - 1
    return nat(r, "Merge sort sorts n = %d distinct elements; merging two sorted halves of total size m costs at most m − 1 comparisons. Worst-case comparisons in total?" % n, mc(n), "Recurrence C(n) = 2C(n/2) + n − 1, C(1) = 0 ⇒ n log n − n + 1 = %d." % mc(n))


# ---------------- sorting & searching ----------------
def inversions(a):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


def insertion_cmp(a):
    a, c = list(a), 0
    for i in range(1, len(a)):
        k, j = a[i], i - 1
        while j >= 0:
            c += 1
            if a[j] > k:
                a[j + 1] = a[j]; j -= 1
            else:
                break
        a[j + 1] = k
    return c


def selection_swaps(a):
    a, s = list(a), 0
    for i in range(len(a) - 1):
        m = min(range(i, len(a)), key=lambda x: (a[x], x))
        if m != i:
            a[i], a[m] = a[m], a[i]; s += 1
    return s


def lomuto(a):
    a = list(a)
    p, i, sw = a[-1], -1, 0
    for j in range(len(a) - 1):
        if a[j] <= p:
            i += 1
            if i != j:
                a[i], a[j] = a[j], a[i]; sw += 1
    a[i + 1], a[-1] = a[-1], a[i + 1]
    sw += 1 if i + 1 != len(a) - 1 else 0
    return a, i + 1, sw


def rnd_arr(r, n=None, lo=1, hi=40):
    n = n or r.randint(6, 9)
    return r.sample(range(lo, hi), n)


@gen(S, SS, "Sorting counts", n=60, diff="easy")
def s_inv(r):
    a = rnd_arr(r)
    kind = r.choice(["inv", "ins", "sel", "bub"])
    if kind == "inv":
        return nat(r, "Array: %s. How many inversions (pairs i < j with a[i] > a[j]) does it contain?" % a, inversions(a), "Count pairs directly: %d." % inversions(a))
    if kind == "bub":
        return nat(r, "Bubble sort (adjacent swaps only) sorts %s. Number of swaps performed?" % a, inversions(a), "Each adjacent swap removes exactly one inversion ⇒ #swaps = #inversions = %d." % inversions(a))
    if kind == "ins":
        return nat(r, "Insertion sort (inner loop compares a[j] with the key until a[j] <= key or j < 0) is run on %s. Total key comparisons?" % a, insertion_cmp(a), "Simulation: %d comparisons." % insertion_cmp(a))
    return nat(r, "Selection sort (swap only when the minimum is not already in place) is run on %s. Number of swaps?" % a, selection_swaps(a), "Simulation: %d swaps." % selection_swaps(a))


@gen(S, SS, "Quicksort partition", n=50, diff="medium", marks=2)
def s_part(r):
    a = rnd_arr(r, r.randint(6, 9))
    res, pos, sw = lomuto(a)
    kind = r.choice(["pos", "arr"])
    code = "partition(A, lo, hi): pivot = A[hi]; i = lo − 1;\n  for j = lo to hi − 1: if A[j] <= pivot: i++, swap(A[i], A[j]);\n  swap(A[i+1], A[hi]); return i + 1"
    if kind == "pos":
        return nat(r, "Lomuto partition (last element as pivot):\n```\n%s\n```\nFor A = %s (0-indexed), what index does partition return?" % (code, a), pos, "Pivot %d has %d smaller-or-equal elements before it ⇒ index %d." % (a[-1], pos, pos))
    s = str(res)
    return mcq(r, "Lomuto partition (last element as pivot):\n```\n%s\n```\nAfter one call on A = %s, the array is" % (code, a), s, [str(sorted(a)), str(a[::-1]), str(res[:pos] + res[pos + 1:] + [res[pos]]), str(sorted(res[:pos]) + [res[pos]] + sorted(res[pos + 1:]))], "Simulate the partition: %s." % s)


def build_heap(a):
    a, sw = list(a), 0
    n = len(a)

    def sift(i):
        nonlocal sw
        while True:
            l, rr_, m = 2 * i + 1, 2 * i + 2, i
            if l < n and a[l] > a[m]: m = l
            if rr_ < n and a[rr_] > a[m]: m = rr_
            if m == i: return
            a[i], a[m] = a[m], a[i]; sw += 1; i = m
    for i in range(n // 2 - 1, -1, -1):
        sift(i)
    return a, sw


@gen(S, SS, "Heaps", n=45, diff="medium")
def s_heap(r):
    a = rnd_arr(r, r.randint(6, 9))
    h, sw = build_heap(a)
    if r.random() < 0.5:
        return mcq(r, "Build-Max-Heap (bottom-up, Floyd) is applied to %s. The resulting array is" % a, str(h), [str(sorted(a, reverse=True)), str(sorted(a)), str(build_heap(a[::-1])[0]), str(h[:2] + h[2:][::-1])], "Heapify from index ⌊n/2⌋−1 down to 0.")
    return nat(r, "Build-Max-Heap (bottom-up, Floyd) is applied to %s. How many element swaps are performed in total?" % a, sw, "Simulate sift-down from the last internal node: %d swaps." % sw)


@gen(S, SS, "Heaps", n=25, diff="hard", marks=2)
def s_heap_n(r):
    n = r.randint(8, 200)
    kind = r.choice(["height", "leaves", "ncmp"])
    if kind == "height":
        return nat(r, "Height (edges on the longest root-to-leaf path) of a binary heap with %d nodes?" % n, math.floor(math.log2(n)), "⌊log₂ n⌋ = %d." % math.floor(math.log2(n)))
    if kind == "leaves":
        return nat(r, "Number of leaf nodes in a binary heap with %d nodes?" % n, n - n // 2, "Leaves = n − ⌊n/2⌋ = %d." % (n - n // 2))
    return nat(r, "A min-heap stores %d distinct elements in an array. In the worst case, how many leaf nodes must be examined to locate the maximum element?" % n, n - n // 2, "The max of a min-heap lies in a leaf; there are ⌈n/2⌉ = %d leaves." % (n - n // 2))


def hash_insert(keys, m, probe):
    t = [None] * m
    coll = 0
    for k in keys:
        for i in range(m):
            pos = probe(k, i, m)
            if t[pos] is None:
                t[pos] = k
                break
            coll += 1
    return t, coll


@gen(S, SS, "Hashing", n=60, diff="medium")
def s_hash(r):
    m = r.choice([7, 8, 10, 11, 13])
    keys = r.sample(range(10, 100), r.randint(5, min(8, m - 1)))
    kind = r.choice(["lin", "quad", "dbl"])
    if kind == "lin":
        probe = lambda k, i, m: (k + i) % m
        nm = "linear probing h(k, i) = (k + i) mod %d" % m
    elif kind == "quad":
        m = r.choice([7, 11, 13])
        keys = keys[:min(len(keys), m - 2)]
        probe = lambda k, i, m: (k + i * i) % m
        nm = "quadratic probing h(k, i) = (k + i²) mod %d" % m
    else:
        probe = lambda k, i, m: (k % m + i * (1 + k % (m - 1))) % m
        nm = "double hashing h(k, i) = (k mod %d + i·(1 + k mod %d)) mod %d" % (m, m - 1, m)
    try:
        t, coll = hash_insert(keys, m, probe)
    except Exception:
        raise Skip()
    if any(k not in t for k in keys):
        raise Skip()
    if r.random() < 0.5:
        return nat(r, "Keys %s are inserted in this order into an empty hash table of size %d using %s. Total number of collisions (occupied slots probed) during all insertions?" % (keys, m, nm), coll, "Table: %s." % t)
    last = t.index(keys[-1])
    return nat(r, "Keys %s are inserted in this order into an empty hash table of size %d using %s. At which slot (0-indexed) does the last key %d end up?" % (keys, m, nm, keys[-1]), last, "Final table: %s." % t)


@gen(S, SS, "Lower bounds", n=25, diff="medium")
def s_lb(r):
    n = r.randint(4, 12)
    return nat(r, "Any comparison-based sort of %d distinct elements needs at least how many comparisons in the worst case (information-theoretic lower bound ⌈log₂ n!⌉)?" % n, math.ceil(math.log2(math.factorial(n))), "n! = %d ⇒ ⌈log₂⌉ = %d." % (math.factorial(n), math.ceil(math.log2(math.factorial(n)))))


# ---------------- greedy ----------------
@gen(S, GR, "Huffman coding", n=50, diff="medium", marks=2)
def g_huff(r):
    n = r.randint(4, 7)
    f = [r.randint(1, 30) for _ in range(n)]
    h = list(f)
    heapq.heapify(h)
    tot = 0
    while len(h) > 1:
        a, b = heapq.heappop(h), heapq.heappop(h)
        tot += a + b
        heapq.heappush(h, a + b)
    return nat(r, "Symbols have frequencies %s. The total number of bits in the Huffman-encoded message (sum of frequency × code length) is" % f, tot, "Sum of all internal-node weights created while merging = %d." % tot)


@gen(S, GR, "Activity selection", n=45, diff="easy")
def g_act(r):
    n = r.randint(5, 8)
    acts = []
    for _ in range(n):
        s = r.randint(0, 12)
        acts.append((s, s + r.randint(1, 5)))
    cnt, end = 0, -1
    for s, e in sorted(acts, key=lambda x: (x[1], x[0])):
        if s >= end:
            cnt += 1; end = e
    return nat(r, "Activities (start, finish): %s. The maximum number of mutually non-overlapping activities (an activity may start exactly when another finishes) is" % acts, cnt, "Greedy by earliest finish time selects %d activities." % cnt)


@gen(S, GR, "Knapsack (fractional)", n=45, diff="medium")
def g_frac(r):
    n = r.randint(3, 5)
    items = [(r.randint(5, 40), r.randint(5, 25)) for _ in range(n)]
    cap = r.randint(15, 50)
    left, val = cap, 0.0
    for v, w in sorted(items, key=lambda x: -x[0] / x[1]):
        t = min(left, w)
        val += v * t / w
        left -= t
        if not left: break
    return nat(r, "Fractional knapsack with capacity %d. Items (value, weight): %s. Maximum total value? (up to 2 decimals)" % (cap, items), round(val, 2), "Take items in decreasing value/weight ratio, fractionally for the last: %.2f." % val, tol=0.01)


@gen(S, GR, "Job sequencing", n=40, diff="medium")
def g_job(r):
    n = r.randint(4, 7)
    jobs = [(r.randint(10, 60), r.randint(1, 4)) for _ in range(n)]
    slots = [None] * (max(d for _, d in jobs) + 1)
    tot = 0
    for p, d in sorted(jobs, key=lambda x: -x[0]):
        for t in range(d, 0, -1):
            if slots[t] is None:
                slots[t] = p; tot += p; break
    return nat(r, "Unit-time jobs with (profit, deadline): %s. Each job takes 1 time unit and must finish by its deadline; one job runs at a time. Maximum total profit?" % jobs, tot, "Greedy by profit, placing each in the latest free slot ≤ deadline: %d." % tot)


# ---------------- dynamic programming ----------------
def lcs(a, b):
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = d[i - 1][j - 1] + 1 if a[i - 1] == b[j - 1] else max(d[i - 1][j], d[i][j - 1])
    return d[-1][-1]


def edit(a, b):
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1): d[i][0] = i
    for j in range(len(b) + 1): d[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    return d[-1][-1]


def rstr(r, n, al="ABCD"):
    return "".join(r.choice(al) for _ in range(n))


@gen(S, DP, "LCS", n=45, diff="medium")
def d_lcs(r):
    a, b = rstr(r, r.randint(5, 8)), rstr(r, r.randint(5, 8))
    return nat(r, "Length of the longest common subsequence of \"%s\" and \"%s\"?" % (a, b), lcs(a, b), "Fill the DP table: LCS = %d." % lcs(a, b))


@gen(S, DP, "Edit distance", n=45, diff="hard", marks=2)
def d_edit(r):
    a, b = rstr(r, r.randint(4, 7), "ABCDE"), rstr(r, r.randint(4, 7), "ABCDE")
    return nat(r, "Minimum edit distance (insert, delete, substitute each cost 1) between \"%s\" and \"%s\"?" % (a, b), edit(a, b), "Wagner–Fischer DP gives %d." % edit(a, b))


@gen(S, DP, "0/1 Knapsack", n=45, diff="medium", marks=2)
def d_knap(r):
    n = r.randint(3, 5)
    items = [(r.randint(3, 40), r.randint(1, 9)) for _ in range(n)]
    W = r.randint(8, 20)
    best = [0] * (W + 1)
    for v, w in items:
        for c in range(W, w - 1, -1):
            best[c] = max(best[c], best[c - w] + v)
    return nat(r, "0/1 knapsack, capacity %d, items (value, weight): %s. Maximum achievable value?" % (W, items), best[W], "Classic DP over capacity gives %d." % best[W])


def mcm(d):
    n = len(d) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    for L in range(2, n + 1):
        for i in range(1, n - L + 2):
            j = i + L - 1
            m[i][j] = min(m[i][k] + m[k + 1][j] + d[i - 1] * d[k] * d[j] for k in range(i, j))
    return m[1][n]


@gen(S, DP, "Matrix chain", n=45, diff="hard", marks=2)
def d_mcm(r):
    n = r.randint(3, 5)
    d = [r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20]) for _ in range(n + 1)]
    return nat(r, "Matrices A1..A%d have dimensions %s (Ai is d[i−1] × d[i]). Minimum number of scalar multiplications to compute A1·A2·…·A%d?" % (n, " × ".join(map(str, d)), n), mcm(d),
               "Matrix-chain DP gives %d." % mcm(d))


@gen(S, DP, "Coin change / LIS", n=55, diff="medium")
def d_coin(r):
    kind = r.choice(["ways", "min", "lis", "rod"])
    if kind == "ways":
        coins = sorted(r.sample([1, 2, 3, 4, 5, 6, 10], r.randint(2, 4)))
        N = r.randint(6, 18)
        w = [1] + [0] * N
        for c in coins:
            for i in range(c, N + 1): w[i] += w[i - c]
        return nat(r, "Number of ways (order does not matter) to make change for %d using unlimited coins of denominations %s?" % (N, coins), w[N], "DP over coins: %d ways." % w[N])
    if kind == "min":
        coins = sorted(r.sample([1, 3, 4, 5, 6, 7, 9, 10], r.randint(3, 4)))
        N = r.randint(8, 30)
        INF = 10 ** 9
        m = [0] + [INF] * N
        for i in range(1, N + 1):
            for c in coins:
                if c <= i and m[i - c] + 1 < m[i]: m[i] = m[i - c] + 1
        if m[N] >= INF: raise Skip()
        return nat(r, "Minimum number of coins from denominations %s (unlimited supply) needed to make %d?" % (coins, N), m[N], "DP: %d coins." % m[N])
    if kind == "lis":
        a = [r.randint(1, 30) for _ in range(r.randint(7, 10))]
        L = [1] * len(a)
        for i in range(len(a)):
            for j in range(i):
                if a[j] < a[i]: L[i] = max(L[i], L[j] + 1)
        return nat(r, "Length of the longest strictly increasing subsequence of %s?" % a, max(L), "L[i] table: %s." % L)
    p = [r.randint(1, 20) for _ in range(5)]
    p = sorted(p)
    n = r.randint(4, 8)
    best = [0] * (n + 1)
    for i in range(1, n + 1):
        best[i] = max(p[j - 1] + best[i - j] for j in range(1, min(i, 5) + 1))
    return nat(r, "Rod cutting: a piece of length j (1 ≤ j ≤ 5) sells for prices %s respectively; longer pieces cannot be sold. Maximum revenue from a rod of length %d?" % (p, n), best[n], "Best-revenue table: %s." % best)


# ---------------- graph algorithms ----------------
def rand_wgraph(r, n, extra):
    edges = {}
    nodes = list(range(n))
    r.shuffle(nodes)
    for i in range(1, n):
        edges[tuple(sorted((nodes[i], nodes[r.randrange(i)])))] = r.randint(1, 15)
    tries = 0
    while len(edges) < n - 1 + extra and tries < 60:
        a, b = r.sample(range(n), 2)
        edges.setdefault(tuple(sorted((a, b))), r.randint(1, 15))
        tries += 1
    return [(a, b, w) for (a, b), w in sorted(edges.items())]


def estr(edges):
    return ", ".join("%s–%s (%d)" % (chr(65 + a), chr(65 + b), w) for a, b, w in edges)


def mst_weight(n, edges):
    p = list(range(n))

    def f(x):
        while p[x] != x:
            p[x] = p[p[x]]; x = p[x]
        return x
    tot = 0
    for a, b, w in sorted(edges, key=lambda e: e[2]):
        if f(a) != f(b):
            p[f(a)] = f(b); tot += w
    return tot


def dijkstra(n, edges, s):
    adj = {i: [] for i in range(n)}
    for a, b, w in edges:
        adj[a].append((b, w)); adj[b].append((a, w))
    d = {s: 0}
    pq = [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > d.get(u, 1e18): continue
        for v, w in adj[u]:
            if du + w < d.get(v, 1e18):
                d[v] = du + w; heapq.heappush(pq, (d[v], v))
    return d


@gen(S, GA_, "MST", n=50, diff="medium")
def gr_mst(r):
    n = r.randint(5, 7)
    e = rand_wgraph(r, n, r.randint(3, 5))
    return nat(r, "Undirected weighted graph with vertices A–%s and edges: %s. Weight of a minimum spanning tree?" % (chr(64 + n), estr(e)), mst_weight(n, e), "Kruskal's algorithm gives total %d." % mst_weight(n, e))


@gen(S, GA_, "Shortest paths", n=50, diff="medium", marks=2)
def gr_dij(r):
    n = r.randint(5, 7)
    e = rand_wgraph(r, n, r.randint(3, 5))
    d = dijkstra(n, e, 0)
    t = r.randint(2, n - 1)
    return nat(r, "Undirected weighted graph, vertices A–%s, edges: %s. Length of the shortest path from A to %s?" % (chr(64 + n), estr(e), chr(65 + t)), d[t], "Dijkstra distances from A: %s." % {chr(65 + k): v for k, v in sorted(d.items())})


@gen(S, GA_, "Topological order", n=35, diff="hard", marks=2)
def gr_topo(r):
    n = 5
    ed = set()
    order = list(range(n)); r.shuffle(order)
    for _ in range(r.randint(3, 6)):
        i, j = sorted(r.sample(range(n), 2))
        ed.add((order[i], order[j]))
    ed = sorted(ed)
    cnt = sum(1 for p in itertools.permutations(range(n)) if all(p.index(a) < p.index(b) for a, b in ed))
    return nat(r, "A DAG on vertices A–E has edges: %s. How many distinct topological orderings does it have?" % ", ".join("%s→%s" % (chr(65 + a), chr(65 + b)) for a, b in ed), cnt, "Count permutations that respect every edge: %d." % cnt)


@gen(S, GA_, "SCC / components", n=45, diff="medium")
def gr_scc(r):
    n = r.randint(5, 8)
    ed = set()
    for _ in range(r.randint(n - 1, n + 3)):
        a, b = r.sample(range(n), 2)
        ed.add((a, b))
    ed = sorted(ed)
    reach = [[i == j for j in range(n)] for i in range(n)]
    for a, b in ed: reach[a][b] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if reach[i][k] and reach[k][j]: reach[i][j] = True
    seen, comp = set(), 0
    for i in range(n):
        if i not in seen:
            comp += 1
            seen |= {j for j in range(n) if reach[i][j] and reach[j][i]}
    return nat(r, "Directed graph on vertices 1..%d with edges: %s. How many strongly connected components?" % (n, ", ".join("%d→%d" % (a + 1, b + 1) for a, b in ed)), comp, "Mutual reachability classes: %d." % comp)


@gen(S, GA_, "Graph counting", n=35, diff="easy")
def gr_count(r):
    n = r.randint(4, 12)
    kind = r.choice(["kn", "tree", "bip", "cyc"])
    if kind == "kn":
        return nat(r, "Number of edges in the complete graph K%d?" % n, n * (n - 1) // 2, "C(n,2) = %d." % (n * (n - 1) // 2))
    if kind == "tree":
        return nat(r, "Number of edges in any spanning tree of a connected graph with %d vertices?" % n, n - 1, "n − 1 = %d." % (n - 1))
    if kind == "bip":
        a = r.randint(2, 9); b = r.randint(2, 9)
        return nat(r, "Maximum number of edges in a simple bipartite graph with parts of sizes %d and %d?" % (a, b), a * b, "a·b = %d." % (a * b))
    return nat(r, "Maximum number of edges in a simple undirected graph on %d vertices that contains NO cycle?" % n, n - 1, "A forest has at most n − 1 edges = %d." % (n - 1))
