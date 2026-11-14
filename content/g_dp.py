"""ALGO chapter 'Dynamic Programming': extra generators; every explanation shows the table that produces the answer."""
from content.kit import *

S = "ALGO"
DPT = "Dynamic Programming"


def row(label, vals):
    return "%s: %s" % (label, " ".join(map(str, vals)))


def lcs_table(a, b):
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = d[i - 1][j - 1] + 1 if a[i - 1] == b[j - 1] else max(d[i - 1][j], d[i][j - 1])
    return d


def lcs_string(a, b, d):
    i, j, out = len(a), len(b), []
    while i and j:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1]); i -= 1; j -= 1
        elif d[i - 1][j] >= d[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))


def edit_table(a, b):
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        d[i][0] = i
    for j in range(len(b) + 1):
        d[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    return d


def knap_table(items, W):
    K = [[0] * (W + 1) for _ in range(len(items) + 1)]
    for i, (v, w) in enumerate(items, 1):
        for c in range(W + 1):
            K[i][c] = K[i - 1][c] if w > c else max(K[i - 1][c], v + K[i - 1][c - w])
    return K


def mcm_table(d):
    n = len(d) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    sp = [[0] * (n + 1) for _ in range(n + 1)]
    for L in range(2, n + 1):
        for i in range(1, n - L + 2):
            j = i + L - 1
            m[i][j], sp[i][j] = min((m[i][k] + m[k + 1][j] + d[i - 1] * d[k] * d[j], k) for k in range(i, j))
    return m, sp


def paren(sp, i, j):
    if i == j:
        return "A%d" % i
    k = sp[i][j]
    return "(%s%s)" % (paren(sp, i, k), paren(sp, k + 1, j))


@gen(S, DPT, "DP states and cost", n=60, diff="easy")
def p_states(r):
    kind = r.choice(["lcs", "knap", "mcm", "fibmemo", "fibnaive", "space", "lis"])
    if kind == "lcs":
        m, n = r.randint(5, 40), r.randint(5, 40)
        return nat(r, "The LCS table of strings of length %d and %d (including the empty-prefix row and column) has how many cells?" % (m, n), (m + 1) * (n + 1),
                   "Row index i runs over 0…%d and column index j over 0…%d, so there are (%d + 1)(%d + 1) = %d cells. Each cell is one subproblem and takes O(1) work." % (m, n, m, n, (m + 1) * (n + 1)))
    if kind == "knap":
        n, W = r.randint(3, 12), r.randint(10, 60)
        return nat(r, "0/1 knapsack with %d items and capacity %d is solved with a full table K[0..n][0..W]. How many cells does the table have?" % (n, W), (n + 1) * (W + 1),
                   "Rows 0…%d (the first is 'no items') and columns 0…%d: (%d + 1)(%d + 1) = %d. The running time O(nW) counts these cells." % (n, W, n, W, (n + 1) * (W + 1)))
    if kind == "mcm":
        n = r.randint(4, 20)
        return nat(r, "For a chain of %d matrices, how many distinct subproblems M[i][j] with i ≤ j does the matrix-chain DP have?" % n, n * (n + 1) // 2,
                   "One subproblem per pair i ≤ j: n + (n − 1) + … + 1 = n(n + 1)/2 = %d. Each needs O(n) work for the split point, hence O(n³) overall." % (n * (n + 1) // 2))
    if kind == "fibmemo":
        n = r.randint(10, 60)
        return nat(r, "Fibonacci is computed by memoised recursion (fib(0)=0, fib(1)=1, every value stored after its first computation). For n = %d, how many distinct values fib(k) are computed?" % n, n + 1,
                   "Each of fib(0), fib(1), …, fib(%d) is computed exactly once and then looked up, so %d values; the running time is Θ(n) instead of Θ(φⁿ)." % (n, n + 1))
    if kind == "fibnaive":
        n = r.randint(5, 12)
        a, b = 1, 1
        calls = [1, 1]
        for _ in range(2, n + 1):
            calls.append(calls[-1] + calls[-2] + 1)
        return nat(r, "Plain recursive fib(n) = fib(n−1) + fib(n−2) with fib(0)=fib(1)=1 (no memoisation). How many calls (including the first) does fib(%d) make in total?" % n, calls[n],
                   "Let C(k) be the number of calls: C(0)=C(1)=1 and C(k) = C(k−1) + C(k−2) + 1. This gives %s, so C(%d) = %d. The same subproblems are recomputed again and again, which is exactly what DP removes." % (", ".join(map(str, calls[:n + 1])), n, calls[n]))
    if kind == "space":
        return mcq(r, "Only the LENGTH of the LCS of two strings of lengths m and n (m ≥ n) is needed. Which space bound is achievable?", "O(n)",
                   ["O(m·n) is necessary", "O(log n)", "O(1)", "O(m + n)²"],
                   "Row i of the table depends only on row i − 1, so keeping two rows of length n + 1 suffices: O(n) space. (Recovering the subsequence itself needs the whole table or a divide-and-conquer trick.)")
    n = r.randint(6, 30)
    return mcq(r, "For an array of n = %d numbers, the O(n²) LIS dynamic programme L[i] = 1 + max{L[j] : j < i, a[j] < a[i]} performs at most how many comparisons a[j] < a[i]?" % n, n * (n - 1) // 2,
               [n * n, n, 2 * n, n * (n + 1) // 2],
               "Element i is compared with all i earlier elements: 0 + 1 + … + (n − 1) = n(n − 1)/2 = %d comparisons, i.e. Θ(n²)." % (n * (n - 1) // 2))


@gen(S, DPT, "Coin change table", n=70, diff="medium")
def p_coin(r):
    kind = r.choice(["ways", "ways_cell", "min", "greedy", "ways_order"])
    N = r.randint(7, 16)
    if kind in ("ways", "ways_cell"):
        coins = sorted(r.sample([1, 2, 3, 4, 5, 6], r.randint(2, 3)))
        w = [1] + [0] * N
        trace = []
        for c in coins:
            for i in range(c, N + 1):
                w[i] += w[i - c]
            trace.append(row("after coin %d" % c, w))
        txt = "\n".join("    " + t for t in trace)
        if kind == "ways":
            return nat(r, "In how many ways can %d be paid with unlimited coins of values %s? (Different orders of the same coins count once.)" % (N, coins), w[N],
                       "Let ways[i] = number of combinations that sum to i, with ways[0] = 1. Take the coins one at a time and do ways[i] += ways[i − coin] for i = coin…%d. Using one coin per round counts every combination once, irrespective of order. Entries 0…%d after each coin:\n\n%s\n\nways[%d] = %d." % (N, N, txt, N, w[N]))
        i = r.randint(N // 2, N)
        return nat(r, "Coins %s, unlimited supply. After the coins have been processed in the order %s with the update ways[i] += ways[i − coin], what is ways[%d]?" % (coins, coins, i), w[i],
                   "The table after the last coin (index 0…%d):\n\n%s\n\nways[%d] = %d." % (N, "    " + trace[-1], i, w[i]))
    if kind == "ways_order":
        coins = sorted(r.sample([1, 2, 3, 4], 2))
        n = r.randint(5, 9)
        seq = [1] + [0] * n
        for i in range(1, n + 1):
            seq[i] = sum(seq[i - c] for c in coins if c <= i)
        comb = [1] + [0] * n
        for c in coins:
            for i in range(c, n + 1):
                comb[i] += comb[i - c]
        return nat(r, "How many ORDERED sequences of coins from %s (unlimited) add up to %d? (1+2 and 2+1 are different.)" % (coins, n), seq[n],
                   "For ordered sequences let f[i] = Σ f[i − c] over all coins c ≤ i, with f[0] = 1 (the loop over amounts is OUTSIDE, the loop over coins inside). Values f[0…%d] = %s, so f[%d] = %d. The unordered count would be %d: swapping the loops changes the problem." % (n, " ".join(map(str, seq)), n, seq[n], comb[n]))
    coins = sorted(r.sample([1, 3, 4, 5, 6, 7, 9, 10], r.randint(3, 4)))
    if 1 not in coins:
        coins = [1] + coins[:3]
    INF = 10 ** 9
    N = r.randint(9, 24)
    m = [0] + [INF] * N
    for i in range(1, N + 1):
        m[i] = 1 + min(m[i - c] for c in coins if c <= i)
    if kind == "min":
        return nat(r, "Minimum number of coins needed to pay %d using unlimited coins of values %s?" % (N, coins), m[N],
                   "min[i] = 1 + min over coins c ≤ i of min[i − c], with min[0] = 0. Values for i = 0…%d:\n\n    %s\n\nmin[%d] = %d." % (N, " ".join(map(str, m)), N, m[N]))
    g, rest = 0, N
    for c in sorted(coins, reverse=True):
        g += rest // c
        rest %= c
    if g == m[N]:
        raise Skip()
    return nat(r, "Coins %s, unlimited supply. A greedy cashier always gives the largest coin that still fits, to pay %d. How many MORE coins does the greedy method use than the optimal dynamic programme?" % (coins, N), g - m[N],
               "Greedy uses %d coins. The DP table min[0…%d] = %s gives the optimum %d. Difference = %d. Greedy is only guaranteed for canonical coin systems such as 1, 2, 5, 10." % (g, N, " ".join(map(str, m)), m[N], g - m[N]))


@gen(S, DPT, "LIS table", n=60, diff="medium")
def p_lis(r):
    a = [r.randint(1, 30) for _ in range(r.randint(7, 10))]
    L = [1] * len(a)
    for i in range(len(a)):
        for j in range(i):
            if a[j] < a[i]:
                L[i] = max(L[i], L[j] + 1)
    kind = r.choice(["len", "cell", "tails"])
    tab = "\n    a = %s\n    L = %s" % (" ".join(map(str, a)), " ".join(map(str, L)))
    if kind == "len":
        return nat(r, "Length of the longest strictly increasing subsequence of %s?" % J(a), max(L),
                   "L[i] = length of the longest increasing subsequence that ENDS at position i = 1 + max L[j] over earlier j with a[j] < a[i]:" + tab + "\n\nThe answer is the maximum entry, %d (not the last entry)." % max(L))
    if kind == "cell":
        i = r.randint(len(a) // 2, len(a) - 1)
        return nat(r, "In the DP L[i] = 1 + max{L[j] : j < i, a[j] < a[i]} for the array %s (positions 1-indexed), what is L[%d]?" % (J(a), i + 1), L[i],
                   "Fill L from left to right:" + tab + "\n\nL[%d] = %d." % (i + 1, L[i]))
    tails = []
    import bisect
    for x in a:
        p = bisect.bisect_left(tails, x)
        if p == len(tails):
            tails.append(x)
        else:
            tails[p] = x
    return nat(r, "The O(n log n) LIS method keeps an array 'tails' where tails[k] is the smallest possible last element of an increasing subsequence of length k + 1. For %s, what is the final length of 'tails'?" % J(a), len(tails),
               "Process the elements, replacing the first tail ≥ x (binary search) or appending when x is larger than all tails. Final tails = %s, whose length is the LIS length %d. (The array itself is not the LIS.)" % (J(tails), len(tails)))


def J(a):
    return " ".join(map(str, a))


@gen(S, DPT, "LCS table", n=70, diff="medium", marks=2)
def p_lcs(r):
    al = "ABCD"
    a = "".join(r.choice(al) for _ in range(r.randint(5, 7)))
    b = "".join(r.choice(al) for _ in range(r.randint(5, 7)))
    d = lcs_table(a, b)
    kind = r.choice(["len", "cell", "str", "cells0", "sub", "idx"])
    tab = "\n".join("    " + " ".join(str(x) for x in rw) for rw in d)
    head = "Rows are the prefixes of \"%s\" (i = 0…%d), columns the prefixes of \"%s\" (j = 0…%d):\n\n%s\n\n" % (a, len(a), b, len(b), tab)
    if kind == "len":
        return nat(r, "Length of the longest common subsequence of \"%s\" and \"%s\"?" % (a, b), d[-1][-1],
                   head + "Each cell is the diagonal + 1 on a match, else the larger of the cell above and the cell to the left. The bottom-right cell is %d." % d[-1][-1])
    if kind in ("cell", "cells0"):
        i, j = r.randint(2, len(a)), r.randint(2, len(b))
        return nat(r, "Let L[i][j] be the LCS length of the first i letters of \"%s\" and the first j letters of \"%s\". What is L[%d][%d]?" % (a, b, i, j), d[i][j],
                   head + "Reading row %d, column %d gives %d." % (i, j, d[i][j]))
    if kind == "str":
        s = lcs_string(a, b, d)
        return mcq(r, "A longest common subsequence of \"%s\" and \"%s\" is" % (a, b), s,
                   [s[::-1] if s[::-1] != s else s + a[0], "".join(sorted(set(a) & set(b))) + a[0], (s + b)[:len(s) + 1], a[:len(s)] if a[:len(s)] != s else b[:len(s)] + "D"],
                   head + "Trace back from the bottom-right cell: on a match step diagonally and record the letter, otherwise move towards the larger neighbour. The letters recorded, reversed, give \"%s\" (length %d)." % (s, len(s)))
    if kind == "sub":
        best, bi = 0, ""
        for i in range(len(a)):
            for j in range(len(b)):
                k = 0
                while i + k < len(a) and j + k < len(b) and a[i + k] == b[j + k]:
                    k += 1
                if k > best:
                    best, bi = k, a[i:i + k]
        return nat(r, "Length of the longest common SUBSTRING (contiguous) of \"%s\" and \"%s\"?" % (a, b), best,
                   "For substrings the recurrence is S[i][j] = S[i−1][j−1] + 1 on a match and 0 otherwise (the run is broken). The largest entry is %d, for the substring \"%s\". The LCS (gaps allowed) is %d, never smaller." % (best, bi, d[-1][-1]))
    return nat(r, "The longest palindromic subsequence of \"%s\" can be found as the LCS of the string and its reverse. What is its length?" % a, lcs_table(a, a[::-1])[-1][-1],
               "LPS(s) = LCS(s, reverse(s)). Here LCS(\"%s\", \"%s\") = %d." % (a, a[::-1], lcs_table(a, a[::-1])[-1][-1]))


@gen(S, DPT, "Edit distance table", n=70, diff="medium", marks=2)
def p_edit(r):
    al = "ABCDE"
    a = "".join(r.choice(al) for _ in range(r.randint(4, 6)))
    b = "".join(r.choice(al) for _ in range(r.randint(4, 6)))
    d = edit_table(a, b)
    tab = "\n".join("    " + " ".join(str(x) for x in rw) for rw in d)
    head = "Table D[i][j] (rows: prefixes of \"%s\", columns: prefixes of \"%s\"); the first row and column are 0…n, then D = D[i−1][j−1] on equal letters else 1 + min(up, left, diagonal):\n\n%s\n\n" % (a, b, tab)
    kind = r.choice(["dist", "cell", "lev_only", "bound", "lcs_rel"])
    if kind == "dist":
        return nat(r, "Minimum edit distance (insert, delete, substitute: cost 1 each) from \"%s\" to \"%s\"?" % (a, b), d[-1][-1], head + "The answer is the bottom-right cell, %d." % d[-1][-1])
    if kind == "cell":
        i, j = r.randint(2, len(a)), r.randint(2, len(b))
        return nat(r, "With D[i][j] the edit distance between the first i letters of \"%s\" and the first j letters of \"%s\", what is D[%d][%d]?" % (a, b, i, j), d[i][j], head + "D[%d][%d] = %d." % (i, j, d[i][j]))
    if kind == "lev_only":
        ind = min(len(a), len(b))
        dd = edit_table(a, b)[-1][-1]
        ni = sum(1 for _ in a) + 0
        sub_only = None
        if len(a) == len(b):
            sub_only = sum(x != y for x, y in zip(a, b))
            return nat(r, "Two strings of equal length: \"%s\" and \"%s\". The Hamming distance (substitutions only) is %d. What is their EDIT distance (insert/delete/substitute allowed)?" % (a, b, sub_only), dd,
                       head + "Edit distance never exceeds the Hamming distance, and can be smaller: here %d." % dd)
        raise Skip()
    if kind == "bound":
        lo, hi = abs(len(a) - len(b)), max(len(a), len(b))
        return nat(r, "For strings of lengths %d and %d, the edit distance is at least L and at most U. What is L + U?" % (len(a), len(b)), lo + hi,
                   "At least |%d − %d| = %d insertions or deletions are unavoidable, and max(%d, %d) = %d operations always suffice (substitute the overlap, insert or delete the rest). L + U = %d." % (len(a), len(b), lo, len(a), len(b), hi, lo + hi))
    L = lcs_table(a, b)[-1][-1]
    ins_del = len(a) + len(b) - 2 * L
    return nat(r, "If only insertions and deletions are allowed (no substitution), the minimum number of operations to turn \"%s\" into \"%s\" is |a| + |b| − 2·LCS. What is it?" % (a, b), ins_del,
               "LCS(\"%s\", \"%s\") = %d, so %d + %d − 2·%d = %d. Keep the common subsequence, delete the other letters of a, insert the other letters of b." % (a, b, L, len(a), len(b), L, ins_del))


@gen(S, DPT, "Knapsack table", n=70, diff="medium", marks=2)
def p_knap(r):
    kind = r.choice(["best", "cell", "subset", "unbounded", "greedyfail", "count"])
    if kind == "subset":
        nums = r.sample(range(2, 20), r.randint(4, 6))
        T = r.randint(8, 40)
        reach = {0}
        for x in nums:
            reach |= {s + x for s in reach if s + x <= T}
        cnt = [1] + [0] * T
        for x in nums:
            for s in range(T, x - 1, -1):
                cnt[s] += cnt[s - x]
        if r.random() < .5:
            return mcq(r, "Is there a subset of %s with sum exactly %d?" % (J(nums), T), "Yes" if T in reach else "No", ["Only if the numbers are sorted", "Cannot be decided in polynomial time in n and the target", "Yes, because the total is larger" if T not in reach else "No, because the total is smaller"],
                       "Let reach[s] be true if some subset sums to s. Start with reach[0] = true; for each number x set reach[s] |= reach[s − x] for s = T…x (downwards, so each number is used once). The reachable sums up to %d are %s. %d is %s." % (T, J(sorted(reach)), T, "reachable" if T in reach else "not reachable"))
        return nat(r, "How many subsets of %s have sum exactly %d?" % (J(nums), T), cnt[T],
                   "count[s] += count[s − x] for s = T down to x, one number at a time, starting with count[0] = 1. Final count[%d] = %d." % (T, cnt[T]))
    n = r.randint(3, 5)
    items = [(r.randint(5, 40), r.randint(1, 8)) for _ in range(n)]
    W = r.randint(8, 16)
    K = knap_table(items, W)
    tab = "\n".join("    item %d (v=%d, w=%d): %s" % (i, items[i - 1][0], items[i - 1][1], " ".join(map(str, K[i]))) for i in range(1, n + 1))
    base = "Table K[i][c], columns c = 0…%d (row 0 is all zeros):\n\n%s\n\n" % (W, tab)
    if kind == "best":
        return nat(r, "0/1 knapsack, capacity %d, items (value, weight) = %s. Maximum total value?" % (W, items), K[n][W],
                   base + "K[i][c] = K[i−1][c] if the item does not fit, else max(K[i−1][c], v + K[i−1][c − w]). The answer is K[%d][%d] = %d." % (n, W, K[n][W]))
    if kind == "cell":
        i, c = r.randint(1, n), r.randint(W // 2, W)
        return nat(r, "0/1 knapsack with items (value, weight) = %s. If K[i][c] is the best value using only the first i items with capacity c, what is K[%d][%d]?" % (items, i, c), K[i][c],
                   base + "Reading row %d, column %d gives %d." % (i, c, K[i][c]))
    if kind == "unbounded":
        best = [0] * (W + 1)
        for c in range(1, W + 1):
            best[c] = max([best[c - 1]] + [best[c - w] + v for v, w in items if w <= c])
        return nat(r, "Items (value, weight) = %s may be taken ANY number of times (unbounded knapsack), capacity %d. Maximum value?" % (items, W), best[W],
                   "best[c] = max over items with w ≤ c of best[c − w] + v (also allowing best[c − 1], unused space). Values for c = 0…%d: %s. The answer is %d. For 0/1 the answer would be %d." % (W, J(best), best[W], K[n][W]))
    if kind == "greedyfail":
        ordr = sorted(items, key=lambda t: -t[0] / t[1])
        g, cap = 0, W
        for v, w in ordr:
            if w <= cap:
                g += v
                cap -= w
        if g == K[n][W]:
            raise Skip()
        return nat(r, "0/1 knapsack, capacity %d, items (value, weight) = %s. A greedy method takes items in decreasing value/weight order whenever they fit. By how much is its total below the optimum?" % (W, items), K[n][W] - g,
                   "Greedy (by ratio) collects %d. The DP optimum is K[%d][%d] = %d. Difference %d: ratio-greedy is optimal only for the FRACTIONAL knapsack." % (g, n, W, K[n][W], K[n][W] - g))
    return nat(r, "A 0/1 knapsack DP with n = %d items and capacity W = %d fills a table row by row. How many times is the recurrence evaluated if cells for c = 0…W of every item row 1…n are computed?" % (n, W), n * (W + 1),
               "n rows × (W + 1) columns = %d·%d = %d evaluations; O(nW) time. Because W is a NUMBER, not the input size, this is pseudo-polynomial." % (n, W + 1, n * (W + 1)))


@gen(S, DPT, "Matrix chain table", n=60, diff="hard", marks=2)
def p_mcm(r):
    n = r.randint(3, 5)
    d = [r.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30]) for _ in range(n + 1)]
    m, sp = mcm_table(d)
    kind = r.choice(["cost", "cell", "paren", "single", "left"])
    dims = " × ".join(map(str, d))
    rows = "\n".join("    M[%d][%d] = %d (split after A%d)" % (i, j, m[i][j], sp[i][j]) for L in range(2, n + 1) for i in range(1, n - L + 2) for j in [i + L - 1])
    base = "Matrix Ai is d[i−1] × d[i], with d = (%s). Cost of splitting at k is M[i][k] + M[k+1][j] + d[i−1]·d[k]·d[j]. Best values, by increasing chain length:\n\n%s\n\n" % (J(d), rows)
    if kind == "cost":
        return nat(r, "Matrices A1…A%d have dimensions %s. Minimum scalar multiplications to compute A1·A2·…·A%d?" % (n, dims, n), m[1][n], base + "M[1][%d] = %d." % (n, m[1][n]))
    if kind == "cell":
        i = r.randint(1, n - 1)
        j = r.randint(i + 1, n)
        return nat(r, "d = (%s) for matrices A1…A%d. In the matrix-chain DP, what is M[%d][%d]?" % (J(d), n, i, j), m[i][j], base + "M[%d][%d] = %d." % (i, j, m[i][j]))
    if kind == "paren":
        def allp(i, j):
            if i == j:
                return [("A%d" % i, 0, d[i - 1], d[i])]
            out = []
            for k in range(i, j):
                for l in allp(i, k):
                    for rr in allp(k + 1, j):
                        out.append(("(%s%s)" % (l[0], rr[0]), l[1] + rr[1] + l[2] * l[3] * rr[3], l[2], rr[3]))
            return out
        allv = allp(1, n)
        best = min(x[1] for x in allv)
        good = [x[0] for x in allv if x[1] == best]
        if len(good) != 1:
            raise Skip()
        bad = [x[0] for x in allv if x[1] > best]
        return mcq(r, "Matrices A1…A%d have d = (%s). Which parenthesisation multiplies the chain with the fewest scalar multiplications?" % (n, J(d)), good[0], bad,
                   base + "Following the split points from M[1][%d] downwards gives %s with cost %d." % (n, good[0], best))
    if kind == "single":
        a, b, c = r.sample([2, 3, 4, 5, 6, 8, 10, 20, 30, 40], 3)
        return nat(r, "Multiplying a %d × %d matrix by a %d × %d matrix by ordinary row-by-column multiplication takes how many scalar multiplications?" % (a, b, b, c), a * b * c,
                   "The product is %d × %d with %d·%d entries; each is a dot product of length %d, so %d·%d·%d = %d multiplications." % (a, c, a, c, b, a, b, c, a * b * c))
    left = d[0] * d[1] * d[2]
    cur = d[2]
    tot = left
    for k in range(3, n + 1):
        tot += d[0] * d[k - 1] * d[k]
    return nat(r, "d = (%s) for A1…A%d. How many scalar multiplications does the strictly left-to-right order (…((A1A2)A3)…)A%d need?" % (J(d), n, n), tot,
               "After each step the left result is %d × d[k−1]. Cost of step k is %d·d[k−1]·d[k]: %s = %d. The optimum (%d) is never larger." % (d[0], d[0], " + ".join("%d·%d·%d" % (d[0], d[k - 1], d[k]) for k in range(2, n + 1)), tot, m[1][n]))


@gen(S, DPT, "Choosing DP, greedy or D&C", n=45, diff="easy")
def p_choose(r):
    pool = [
        ("longest common subsequence of two strings", "dynamic programming", "Overlapping subproblems on prefixes; no local choice is safe."),
        ("0/1 knapsack", "dynamic programming", "A locally best item can block a better combination, so every include/exclude choice must be examined with stored sub-answers."),
        ("fractional knapsack", "greedy", "Taking the highest value per weight first is provably optimal when items can be split."),
        ("activity selection (maximum number of non-overlapping intervals)", "greedy", "Always take the interval that finishes first; an exchange argument proves it."),
        ("merge sort", "divide and conquer", "The two halves are disjoint subproblems: nothing overlaps, so storing results gains nothing."),
        ("matrix-chain multiplication order", "dynamic programming", "Different splits share the same sub-chains M[i][j]."),
        ("Huffman coding", "greedy", "Repeatedly merging the two least frequent symbols is optimal."),
        ("minimum number of coins for an arbitrary coin system", "dynamic programming", "Greedy can fail (coins 1, 3, 4 and amount 6); the DP min[i] = 1 + min min[i − c] is always right."),
        ("edit distance between two strings", "dynamic programming", "Subproblems are pairs of prefixes and overlap heavily."),
        ("binary search", "divide and conquer", "A single subproblem of half size; nothing is repeated."),
        ("single-source shortest paths with non-negative weights", "greedy", "Dijkstra permanently fixes the closest unfinished vertex each step."),
    ]
    q = r.choice(pool)
    wrong = [x for x in ("dynamic programming", "greedy", "divide and conquer", "backtracking with no pruning") if x != q[1]]
    return mcq(r, "Which technique gives a correct and efficient algorithm for: %s?" % q[0], q[1], wrong, q[2])
