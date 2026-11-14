"""ALGO chapter 3 — Dynamic Programming: a full chapter built from small, focused lessons."""
import itertools

from content import g_algo as A
from content import g_dp as D
from learn import Ex, lesson

S = "ALGO"
CH, NO = "Dynamic Programming", 3
TOPIC = "Dynamic Programming"


def _ways(coins, n):
    w = [1] + [0] * n
    for c in coins:
        for i in range(c, n + 1):
            w[i] += w[i - c]
    return w


def _mincoins(coins, n):
    m = [0] + [10 ** 9] * n
    for i in range(1, n + 1):
        m[i] = 1 + min(m[i - c] for c in coins if c <= i)
    return m


def _lis(a):
    L = [1] * len(a)
    for i in range(len(a)):
        for j in range(i):
            if a[j] < a[i]:
                L[i] = max(L[i], L[j] + 1)
    return L


def _fibcalls(n):
    c = [1, 1]
    for _ in range(2, n + 1):
        c.append(c[-1] + c[-2] + 1)
    return c[n]


# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=2, slug="algo-dp-method", title="1 · The DP method: states, recurrence, order",
       topic=TOPIC, subs=["DP states and cost"], minutes=18, weight=5, widget="none",
       key="Every DP problem is solved by the same four decisions: what a table cell means, how a cell is computed from smaller cells, which cells are known at the start, and in what order to fill the rest. Running time = (number of cells) × (work per cell).",
       analogy=("🧱", "Building with stored bricks", "A mason who has already built the wall up to row 5 does not rebuild rows 1 to 5 for row 6: he stands on them. A DP table is the wall: each new cell is placed on cells you have already built."),
       sections=[
           dict(h="Why plain recursion explodes", md="""The recursion fib(n) = fib(n−1) + fib(n−2) calls fib(n−2) once directly and again inside fib(n−1). Each of these repeats the same argument again, and the number of calls satisfies C(n) = C(n−1) + C(n−2) + 1, which grows like $\\varphi^n$ (about $1.618^n$). Only n + 1 *different* values exist, so almost all the work is repeated work.

DP removes the repetition in either of two equivalent ways:

- **Memoisation (top-down):** keep the recursion, but store each result in a dictionary or array the first time it is computed and look it up afterwards.
- **Tabulation (bottom-up):** fill an array from the smallest argument upwards, so that when a cell is needed it is already there."""),
           dict(h="The four decisions", md="""1. **State:** what do the indices mean? Example: `L[i][j]` = LCS length of the first i letters of X and first j letters of Y. Pick the *smallest* set of indices that determines the answer to a subproblem.
2. **Recurrence:** the value of a state in terms of smaller states. It usually tries every possible *last choice* and takes the best (max, min or sum).
3. **Base cases:** the states with no smaller state: empty prefix, zero capacity, single matrix.
4. **Order:** an order in which every state is computed after all states it depends on (increasing i, increasing j, increasing chain length, ...).

The answer is a specific cell (often the corner) or an aggregate over the last row (for example LIS takes the maximum of all L[i])."""),
           dict(h="Running time and space from the table", md="""| Problem | States | Work per state | Time | Space |
|---|---|---|---|---|
| Fibonacci | n | O(1) | O(n) | O(1) with two variables |
| LCS / edit distance | mn | O(1) | O(mn) | O(mn), or O(min(m, n)) for the length only |
| 0/1 knapsack | nW | O(1) | O(nW) | O(W) with one row, filled right to left |
| Matrix chain | n²/2 | O(n) splits | O(n³) | O(n²) |
| LIS (simple) | n | O(n) | O(n²) | O(n) |

**Pseudo-polynomial:** O(nW) depends on the *value* W, not the number of bits of W, so it is exponential in the input size. Knapsack remains NP-complete."""),
           dict(h="When does DP apply?", md="""Two properties are needed:

- **Optimal substructure:** an optimal solution to the problem contains optimal solutions to its subproblems.
- **Overlapping subproblems:** the same subproblem is needed again and again. If the subproblems are disjoint (merge sort, binary search) the technique is plain divide and conquer, and storing results gains nothing.

If a *single* locally best choice is always safe, greedy is simpler and faster. DP is the fallback when you must compare all choices.""",
                call=[("trap", "Counting states", "Do not forget the row and column for the empty prefix: an LCS table for lengths m and n has (m+1)(n+1) cells, not mn.")]),
       ],
       examples=[
           Ex("Naive Fibonacci calls", "Plain recursion with fib(0) = fib(1) = 1. How many calls does fib(8) make in total (including the first call)?",
              ["C(0) = C(1) = 1 and C(k) = C(k−1) + C(k−2) + 1.", "C: 1, 1, 3, 5, 9, 15, 25, 41, **67**."], "**67** calls.", verify=lambda: str(_fibcalls(8))),
           Ex("Memoised Fibonacci", "With memoisation, how many distinct values fib(k) are computed for fib(40)?",
              ["Each of fib(0), …, fib(40) is computed once and then reused.", "That is **41** values; the time drops from about 1.6^40 calls to Θ(n)."], "**41**", verify=lambda: str(41)),
           Ex("LCS table size", "Strings of length 12 and 9 are compared with the LCS DP. How many table cells are filled (empty-prefix row and column included)?",
              ["(12 + 1)(9 + 1) = 13 × 10 = **130**.", "Every cell costs O(1), so the running time is Θ(mn)."], "**130**", verify=lambda: str(13 * 10)),
           Ex("Matrix-chain subproblems", "A chain of 10 matrices is multiplied with the DP M[i][j] (i ≤ j). How many subproblems exist?",
              ["One per pair i ≤ j: 10 + 9 + … + 1 = 10·11/2 = **55**.", "Each takes up to n − 1 candidate splits, giving the O(n³) bound."], "**55**", verify=lambda: str(55)),
           Ex("Space saving", "The knapsack table has n = 40 items and capacity W = 500. How many cells with the full table, and how many with the one-row version?",
              ["Full: (40 + 1)(500 + 1) = 41 × 501 = 20541.", "One row of W + 1 = **501** cells suffices if you update from c = W down to c = w (so each item is used once)."], "**20541** cells and **501** cells.", verify=lambda: "%d cells and %d cells" % (41 * 501, 501)),
       ],
       traps=[("Memoisation without a base case", "Missing base cases give infinite recursion or index errors."),
              ("Wrong fill direction", "In the one-row 0/1 knapsack, filling c upwards lets one item be used several times (that is the unbounded problem)."),
              ("DP is not always polynomial", "Pseudo-polynomial time O(nW) is exponential in the bit-length of W."),
              ("Disjoint subproblems", "If subproblems never repeat, memoisation only adds overhead.")],
       quick=[("Naive recursive Fibonacci takes", ["O(n)", "O(n²)", "Θ(φⁿ)", "O(log n)"], 2, "Calls grow like the Fibonacci numbers themselves."),
              ("The LCS table of lengths m and n has", ["mn cells", "(m+1)(n+1) cells", "m+n cells", "2^(m+n) cells"], 1, "The empty-prefix row and column count."),
              ("Which problem lacks overlapping subproblems?", ["Edit distance", "Merge sort", "Matrix chain", "LCS"], 1, "Merge sort halves are disjoint."),
              ("Time of a DP = ", ["states + work", "states × work per state", "states²", "2^states"], 1, "Multiply.")],
       summary=["DP = store answers to overlapping subproblems.", "Define state, recurrence, base cases, order.", "Time = number of states × work per state.", "Memoisation = top-down, tabulation = bottom-up; same cost.",
                "O(nW) is pseudo-polynomial.", "Disjoint subproblems mean divide and conquer, not DP."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=3, slug="algo-dp-1d", title="2 · One-dimensional DP: coin change and LIS",
       topic=TOPIC, subs=["Coin change table", "LIS table", "Coin change / LIS"], minutes=22, weight=5, widget="none",
       key="With one index the table is a single row. Coin change counts combinations or minimises coins; LIS stores, for each position, the best subsequence ending there. The loop order decides whether you count combinations or arrangements.",
       analogy=("🪙", "Paying exact change", "To pay 11 with coins 1, 5, 6, think about the LAST coin you hand over. Whatever it is, the rest is a smaller payment you have already solved."),
       sections=[
           dict(h="Coin change: number of combinations", md="""State: `ways[i]` = number of multisets of coins that add up to i. Base: `ways[0] = 1` (the empty set).

    for coin in coins:
        for i in range(coin, N + 1):
            ways[i] += ways[i - coin]

The coin loop is **outside**. Each coin is introduced once; after processing coin c the table counts the combinations that use only the coins seen so far. Because 2+3 and 3+2 are produced by the same pair of coins, they are counted once.

**If you swap the loops** (amount outside, coin inside) you count *ordered sequences* (compositions), so 2+3 and 3+2 are two different ways. This swap is a favourite exam trap."""),
           dict(h="Coin change: minimum coins", md="""State: `m[i]` = fewest coins that make i, `m[0] = 0`.

    m[i] = 1 + min(m[i - c] for c in coins if c <= i)

Time O(N·k) for k denominations. **Greedy fails** for some systems: with coins 1, 3, 4 and amount 6, greedy takes 4 + 1 + 1 (3 coins) but the optimum is 3 + 3 (2 coins). The DP is always right; greedy is right only for canonical systems like 1, 2, 5, 10, 20, 50."""),
           dict(h="Longest increasing subsequence", md="""State: `L[i]` = length of the longest strictly increasing subsequence that **ends at position i**.

    L[i] = 1 + max(L[j] for j < i if a[j] < a[i]),  or 1 if there is no such j

The answer is **max over all i of L[i]**, not L[n]. Time O(n²) (n states, up to n comparisons each).

**O(n log n) version.** Keep `tails`, where tails[k] is the smallest possible last element of an increasing subsequence of length k + 1. For each x, binary-search the first tail ≥ x and replace it (or append x if none). The length of `tails` at the end is the LIS length, but `tails` itself is *not* a valid subsequence in general."""),
           dict(h="Other one-dimensional classics", md="""- **Rod cutting:** best[n] = max over j of price[j] + best[n − j].
- **House robber / maximum sum with no two adjacent:** f[i] = max(f[i−1], f[i−2] + a[i]).
- **Maximum subarray (Kadane):** best ending at i = max(a[i], best ending at i−1 + a[i]).
- **Climbing stairs:** f[i] = f[i−1] + f[i−2]: the Fibonacci recurrence again.

All are "decide what the last item or step is, then reuse the smaller answer"."""),
       ],
       examples=[
           Ex("Number of combinations", "In how many ways can 10 be paid with unlimited coins of 2, 3 and 5 (order ignored)?",
              ["ways starts [1,0,0,…]. After coin 2: 1 0 1 0 1 0 1 0 1 0 1.", "After coin 3: indices 0…10 become 1 0 1 1 1 1 2 1 2 2 2.", "After coin 5 the table is 1 0 1 1 1 2 2 2 3 3 4, so ways[10] = **4**.", "The four ways: 2+2+2+2+2, 2+2+3+3, 2+3+5 and 5+5."], "**4**", verify=lambda: str(_ways([2, 3, 5], 10)[10])),
           Ex("Ordered sequences", "Coins {1, 2}. How many ordered sequences add up to 5?",
              ["f[0] = 1, f[i] = f[i−1] + f[i−2].", "f = 1, 1, 2, 3, 5, **8**. These are the Fibonacci numbers: 8 compositions of 5 with parts 1 and 2.", "Unordered combinations would be only 3 (all-ones, one 2, two 2s)."], "**8** (versus 3 unordered).",
              verify=lambda: "%d (versus %d unordered)" % ([1, 1, 2, 3, 5, 8][5], _ways([1, 2], 5)[5])),
           Ex("Greedy fails", "Coins {1, 3, 4}. Compare greedy and optimal for the amount 6.",
              ["Greedy: 4, then 1, then 1: 3 coins.", "DP: m = 0 1 2 1 1 2 **2** for i = 0…6, so 3 + 3 = 2 coins.", "Difference: 1 extra coin."], "Greedy 3 coins, optimum **2**.", verify=lambda: "Greedy 3 coins, optimum %d" % _mincoins([1, 3, 4], 6)[6]),
           Ex("Minimum coins", "Coins {1, 5, 6, 9}. Minimum number of coins for 11?",
              ["m[0..11] = 0 1 2 3 4 1 1 2 3 1 2 2.", "m[11] = 1 + min(m[10], m[6], m[5], m[2]) = 1 + min(2, 1, 1, 2) = **2** (5 + 6)."], "**2**", verify=lambda: str(_mincoins([1, 5, 6, 9], 11)[11])),
           Ex("LIS table", "Find the LIS length of 10, 22, 9, 33, 21, 50, 41, 60.",
              ["L = 1, 2, 1, 3, 2, 4, 4, 5.", "L[8] = 5 comes from 10, 22, 33, 50, 60 (or 41 before 60).", "The maximum entry is **5**."], "**5**", verify=lambda: str(max(_lis([10, 22, 9, 33, 21, 50, 41, 60])))),
           Ex("LIS by tails", "Run the O(n log n) method on 3, 1, 4, 1, 5, 9, 2, 6. What is the final length of tails and what does it equal?",
              ["Process: [3] → [1] → [1,4] → [1,4] (1 replaces 1) → [1,4,5] → [1,4,5,9] → [1,2,5,9] → [1,2,5,6].", "Length **4** = LIS length (for example 1, 4, 5, 9)."], "**4**", verify=lambda: str(max(_lis([3, 1, 4, 1, 5, 9, 2, 6])))),
       ],
       traps=[("Loop order in coin change", "Coins outside = combinations. Amount outside = ordered sequences."),
              ("Greedy for general coins", "Only canonical systems let you take the largest coin each time."),
              ("LIS answer", "Take max L[i], not the last entry; the subsequence need not end at the last element."),
              ("Strict vs non-strict", "Non-decreasing LIS uses a[j] ≤ a[i] (and bisect_right in the tails method).")],
       quick=[("Number of coin combinations with coins {1,2} for 4 (order ignored)", ["2", "3", "5", "8"], 1, "1111, 112, 22."),
              ("Number of ordered sequences with coins {1,2} for 4", ["3", "4", "5", "8"], 2, "f = 1, 1, 2, 3, 5."),
              ("O(n²) LIS time comes from", ["n log n states", "n states with O(n) work each", "2^n subsequences", "sorting"], 1, "n × n."),
              ("Which coin system makes greedy fail?", ["1, 2, 5, 10", "1, 5, 10, 25", "1, 3, 4", "1, 2, 4, 8"], 2, "6 = 3 + 3 beats 4 + 1 + 1.")],
       summary=["Coin combinations: coins outside, ways[i] += ways[i − c].", "Min coins: 1 + min m[i − c].", "Greedy works only for canonical coin systems.", "LIS: L[i] = 1 + max L[j] with a[j] < a[i]; answer = max L.",
                "O(n log n) LIS: tails array with binary search.", "Reasoning pattern: choose the last item, then reuse the sub-answer."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=4, slug="algo-dp-lcs", title="3 · Longest common subsequence",
       topic=TOPIC, subs=["LCS table", "LCS"], minutes=22, weight=5, widget="dp",
       widget_hint="Choose LCS and enter two strings. Watch each cell take the diagonal + 1 on a match, else the larger of up and left.",
       key="LCS compares prefixes of two strings. A match extends the diagonal; otherwise one of the two strings loses its last letter. The table gives the length; tracing back gives a subsequence. Variants (substring, palindrome, edit with only insert/delete) all reuse the same table.",
       analogy=("🧬", "Aligning two DNA strands", "Lay two strands side by side and draw lines between equal letters without letting lines cross. The most lines you can draw is the LCS length."),
       sections=[
           dict(h="Definition and recurrence", md="""A **subsequence** keeps the order but may skip letters (ACE is a subsequence of ABCDE). A **substring** must be contiguous.

State `L[i][j]` = LCS length of the first i letters of X and the first j letters of Y.

    L[i][0] = L[0][j] = 0
    L[i][j] = L[i-1][j-1] + 1            if X[i] = Y[j]
    L[i][j] = max(L[i-1][j], L[i][j-1])  otherwise

Why a match is safe to take: if the last letters are equal, some optimal subsequence ends with that letter; matching them can never hurt. If they differ, at least one of the two last letters is unused, so drop one and keep the better result."""),
           dict(h="Filling the table by hand", md="""Row by row, left to right. For X = ABCB and Y = BDCAB:

| | ε | B | D | C | A | B |
|---|---|---|---|---|---|---|
| **ε** | 0 | 0 | 0 | 0 | 0 | 0 |
| **A** | 0 | 0 | 0 | 0 | 1 | 1 |
| **B** | 0 | 1 | 1 | 1 | 1 | 2 |
| **C** | 0 | 1 | 1 | 2 | 2 | 2 |
| **B** | 0 | 1 | 1 | 2 | 2 | 3 |

The corner is **3**. Two checks that catch slips: values never decrease along a row or a column, and neighbouring cells differ by at most 1."""),
           dict(h="Recovering the subsequence", md="""Start at the corner (m, n). While i > 0 and j > 0:

- if X[i] = Y[j]: record the letter, move to (i−1, j−1);
- else move to the neighbour with the larger value (up if tied, by convention).

The recorded letters read backwards give one LCS. There may be several LCS strings with the same length; GATE asks for the length or checks that a given string is a valid LCS. Time O(m + n) for the trace-back after O(mn) for the table."""),
           dict(h="Variants that reuse the table", md="""- **Longest common substring:** S[i][j] = S[i−1][j−1] + 1 on a match, **0** on a mismatch; the answer is the maximum entry anywhere.
- **Longest palindromic subsequence:** LCS(s, reverse(s)).
- **Shortest common supersequence:** |X| + |Y| − LCS(X, Y).
- **Insert/delete-only edit distance:** |X| + |Y| − 2·LCS(X, Y).
- **Space:** two rows are enough if only the length is needed: O(min(m, n)).
- **Time lower bound:** Θ(mn) for the general problem; O(mn / log n) with the Four Russians method (not required)."""),
       ],
       examples=[
           Ex("LCS length", "Find the LCS length of ABCBDAB and BDCABA.", ["Fill the 8 × 7 table with the recurrence.", "The corner is **4**, for example BCBA or BDAB."], "**4**", verify=lambda: str(A.lcs("ABCBDAB", "BDCABA"))),
           Ex("Reading the table", "For X = AGGTAB and Y = GXTXAYB, what is the LCS length and an LCS?",
              ["The matches are G, T, A, B in order.", "Length **4**, the subsequence GTAB."], "**4** (GTAB).", verify=lambda: "%d (GTAB)" % A.lcs("AGGTAB", "GXTXAYB")),
           Ex("Longest common substring", "Longest common substring of ABABC and BABCA?",
              ["Compare runs: BABC (positions 2 to 5 of the first, 1 to 4 of the second) matches 4 letters in a row.", "Length **4**."], "**4** (BABC).", verify=lambda: "%d (BABC)" % max(k for k in range(1, 6) if any(s in "BABCA" for s in ["ABABC"[i:i + k] for i in range(0, 6 - k)]))),
           Ex("Palindromic subsequence", "Longest palindromic subsequence of BBABCBCAB?",
              ["LPS = LCS(s, reverse(s)).", "reverse = BACBCBABB; the LCS is **7** (BABCBAB)."], "**7**", verify=lambda: str(A.lcs("BBABCBCAB", "BBABCBCAB"[::-1]))),
           Ex("Insert/delete distance", "Minimum insertions and deletions (no substitutions) to turn ABCDE into ACE?",
              ["LCS(ABCDE, ACE) = 3.", "|X| + |Y| − 2·LCS = 5 + 3 − 6 = **2** (delete B and D)."], "**2**", verify=lambda: str(5 + 3 - 2 * A.lcs("ABCDE", "ACE"))),
       ],
       traps=[("Substring vs subsequence", "Different recurrences: substring resets to 0 on a mismatch."),
              ("Forgetting the answer is the corner", "For LCS the answer is L[m][n]; for the common substring it is the maximum entry."),
              ("LCS is not unique", "Different LCS strings can have the same length; check what the question asks."),
              ("Using L[i-1][j-1] on a mismatch", "A mismatch takes max(up, left); the diagonal is only for matches.")],
       quick=[("LCS table time for strings of length m and n", ["O(m + n)", "O(mn)", "O(m²n)", "O(2^n)"], 1, "One O(1) cell per pair."),
              ("On a mismatch, L[i][j] =", ["L[i-1][j-1]", "max(L[i-1][j], L[i][j-1])", "L[i-1][j-1] + 1", "0"], 1, "Drop a letter from one string."),
              ("Shortest common supersequence length", ["LCS", "|X|+|Y|−LCS", "|X|+|Y|", "|X|·|Y|"], 1, "Common letters are shared once."),
              ("Longest palindromic subsequence equals", ["LCS(s, s)", "LCS(s, reverse(s))", "edit(s, reverse(s))", "|s|/2"], 1, "Palindrome reads the same backwards.")],
       summary=["L[i][j] = diagonal + 1 on a match, else max(up, left).", "Corner = LCS length; trace back for the string.", "Time and space O(mn); O(min(m,n)) space for the length only.",
                "Substring: reset to 0 on mismatch.", "SCS = m + n − LCS; insert/delete distance = m + n − 2·LCS.", "LPS = LCS with the reverse."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=5, slug="algo-dp-edit", title="4 · Edit distance",
       topic=TOPIC, subs=["Edit distance table", "Edit distance"], minutes=18, weight=4, widget="dp",
       widget_hint="Choose edit distance. Each cell is the cheapest of delete, insert and substitute (free if the letters match).",
       key="Edit distance counts the fewest insertions, deletions and substitutions that turn one string into another. The table mirrors LCS but each cell is a minimum over three moves instead of a maximum over two.",
       analogy=("✏️", "Fixing a typo", "To turn 'kitten' into 'sitting' you can delete a letter, add a letter or replace one. The table finds the cheapest way and each cell asks: what was the last edit?"),
       sections=[
           dict(h="The recurrence", md="""State `D[i][j]` = edit distance between the first i letters of X and first j letters of Y.

    D[i][0] = i      (delete i letters)
    D[0][j] = j      (insert j letters)
    D[i][j] = D[i-1][j-1]                                  if X[i] = Y[j]
    D[i][j] = 1 + min(D[i-1][j],      # delete X[i]
                      D[i][j-1],      # insert Y[j]
                      D[i-1][j-1])    # substitute X[i] by Y[j]     otherwise

(Some texts take min of all three including a free diagonal on a match; the result is the same.) Time and space O(mn), reducible to O(min(m, n)) space for the distance alone."""),
           dict(h="A full table", md="""X = SUN, Y = SAT:

| | ε | S | A | T |
|---|---|---|---|---|
| **ε** | 0 | 1 | 2 | 3 |
| **S** | 1 | 0 | 1 | 2 |
| **U** | 2 | 1 | 1 | 2 |
| **N** | 3 | 2 | 2 | 2 |

Distance **2**: for example substitute U→A and N→T. Read the path back from the corner: a diagonal step is a substitution (or a free match), a vertical step a deletion, a horizontal step an insertion."""),
           dict(h="Bounds and relatives", md="""- **Lower bound:** |m − n| (the length difference must be bridged by insertions or deletions).
- **Upper bound:** max(m, n) (substitute the overlap, insert or delete the rest).
- If lengths are equal, edit distance ≤ the Hamming distance (number of differing positions).
- With **substitution cost 2** (or substitution disallowed) the distance is m + n − 2·LCS.
- **Triangle inequality** holds, so edit distance is a metric.
- With unequal costs, the recurrence is the same with the costs in place of the 1s."""),
       ],
       examples=[
           Ex("kitten to sitting", "Edit distance between kitten and sitting?", ["Substitute k→s, substitute e→i, insert g.", "Three operations; the table confirms none better exists."], "**3**", verify=lambda: str(A.edit("kitten", "sitting"))),
           Ex("SUN to SAT", "Edit distance between SUN and SAT?", ["Fill the 4 × 4 table (above): the corner is 2.", "S matches, then two substitutions."], "**2**", verify=lambda: str(A.edit("SUN", "SAT"))),
           Ex("A single cell", "In the table for X = ABCD and Y = ACBD, what is D[3][3] (prefixes ABC and ACB)?",
              ["ABC → ACB: substitute B→C and C→B: 2.", "Could we do it in 1? Deleting one letter and inserting another also costs 2. So **2**."], "**2**", verify=lambda: str(D.edit_table("ABCD", "ACBD")[3][3])),
           Ex("Bounds", "Two strings have lengths 9 and 4. Lower and upper bounds on their edit distance?",
              ["At least |9 − 4| = 5 insertions or deletions.", "At most max(9, 4) = 9.", "So between **5** and **9**."], "Between **5** and **9**.", verify=lambda: "Between %d and %d" % (5, 9)),
           Ex("Insert and delete only", "Fewest insertions and deletions that turn HORSE into ROS?",
              ["In HORSE the letters come in the order H, O, R, S, E; ROS needs R, O, S in that order. The longest common subsequence is RS (or OS), length 2.", "Operations = 5 + 3 − 2·2 = **4**."], "**4**", verify=lambda: str(5 + 3 - 2 * A.lcs("HORSE", "ROS"))),
       ],
       traps=[("Forgetting free matches", "On equal letters the diagonal is free (cost 0), not +1."),
              ("Base row and column", "D[i][0] = i and D[0][j] = j, not 0."),
              ("Substituting costs 1", "In the standard model; some problems say substitution costs 2: then use m + n − 2·LCS."),
              ("Distance is not LCS", "Do not mix the recurrences: edit takes a min over three moves.")],
       quick=[("D[i][0] =", ["0", "i", "i + 1", "∞"], 1, "Delete all i letters."),
              ("Edit distance between equal strings", ["0", "n", "1", "undefined"], 0, "Nothing to do."),
              ("Lower bound on edit distance of strings of length 7 and 3", ["0", "3", "4", "10"], 2, "|7 − 3|."),
              ("Time of the standard algorithm", ["O(m + n)", "O(mn)", "O(m²n²)", "O(2^m)"], 1, "mn cells.")],
       summary=["Match → diagonal, mismatch → 1 + min(up, left, diagonal).", "Base: D[i][0] = i, D[0][j] = j.", "Time O(mn); O(min(m,n)) space for the distance.", "|m − n| ≤ distance ≤ max(m, n).",
                "Insert/delete only: m + n − 2·LCS.", "Path in the table = sequence of edits."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=6, slug="algo-dp-knapsack", title="5 · Knapsack, subset sum and their relatives",
       topic=TOPIC, subs=["Knapsack table", "0/1 Knapsack"], minutes=22, weight=5, widget="dp",
       widget_hint="Choose knapsack and change the items. Each row adds one item: take it or leave it.",
       key="For each item decide: leave it, or take it and use the remaining capacity for the earlier items. The table is items by capacity; its running time O(nW) is pseudo-polynomial. Subset sum is the yes/no version; the unbounded version lets items repeat.",
       analogy=("🎒", "Packing a rucksack", "Go through your gear one item at a time. For each, either leave it (the best you could do before) or take it (its value plus the best you could do with the weight that remains)."),
       sections=[
           dict(h="0/1 knapsack recurrence", md="""State `K[i][c]` = best value from the first i items with capacity c. Row 0 and column 0 are 0.

    K[i][c] = K[i-1][c]                          if w_i > c
    K[i][c] = max(K[i-1][c], v_i + K[i-1][c - w_i])   otherwise

Answer K[n][W]. Time and space O(nW). **One-row version:** keep only K[c], and for each item update `for c from W down to w_i` — downwards, so K[c − w_i] still holds the *previous* row's value. Filling upwards allows the same item more than once (that is unbounded knapsack)."""),
           dict(h="Subset sum and counting", md="""**Subset sum:** can some subset of the numbers sum to T? reach[0] = true; for each number x (downwards over s): reach[s] |= reach[s − x]. Time O(nT).

**Counting subsets** with sum T: count[s] += count[s − x] (downwards), count[0] = 1.

**Partition into two equal halves** = subset sum with T = total/2 (impossible if the total is odd). These are weakly NP-complete: polynomial in the *value* T, so pseudo-polynomial."""),
           dict(h="Unbounded knapsack and rod cutting", md="""When items may be used any number of times:

    best[c] = max( best[c - 1],  max over items with w ≤ c of  best[c - w] + v )

Rod cutting is exactly this with item j of weight j and value price[j]. The one-row loop goes **upwards** in c. Coin change is the same shape: counting combinations, or minimising coins."""),
           dict(h="Greedy versus DP", md="""The **fractional** knapsack (items can be split) is solved greedily by value/weight ratio. The **0/1** knapsack is not: with capacity 50 and items (60, 10), (100, 20), (120, 30), ratio-greedy takes the first two for 160, while the optimum is 100 + 120 = 220.

Why DP is allowed yet "polynomial" is misleading: the input size is n log W bits, so O(nW) is exponential in log W. The problem is NP-complete, but has this pseudo-polynomial algorithm."""),
       ],
       examples=[
           Ex("0/1 knapsack", "Capacity 50, items (value, weight) = (60, 10), (100, 20), (120, 30). Best value?", ["Subsets under 50: {2,3} weighs 50 and gives 220; {1,3} gives 180; {1,2} gives 160.", "Best **220**."], "**220**", verify=lambda: str(D.knap_table([(60, 10), (100, 20), (120, 30)], 50)[3][50])),
           Ex("Reading K", "Items (value, weight) = (10, 5), (40, 4), (30, 6), (50, 3), capacity 10. Best value?",
              ["Try the best pairs: 40 + 50 = 90 (weights 4 + 3 = 7), plus a 6 does not fit (13 > 10).", "40 + 30 + ... weights 4 + 6 = 10 gives 70; 50 + 30 = 80 (3 + 6 = 9).", "The best is 40 + 50 = **90**."], "**90**", verify=lambda: str(D.knap_table([(10, 5), (40, 4), (30, 6), (50, 3)], 10)[4][10])),
           Ex("Greedy gap", "Same data as the first example: how far below the optimum is greedy by value/weight?",
              ["Ratios: 6, 5, 4. Greedy takes item 1 (weight 10) and item 2 (weight 20); item 3 (weight 30) does not fit in the 20 left: value 160.", "Optimum 220. Difference **60**."], "**60**", verify=lambda: str(220 - 160)),
           Ex("Subset sum", "Can {3, 34, 4, 12, 5, 2} make 9? And how many subsets sum to 9?",
              ["Reachable sums include 9 = 4 + 5 and 9 = 3 + 4 + 2.", "Exactly 2 subsets: {4, 5} and {3, 4, 2}. Answer: yes, **2** subsets."], "Yes, **2** subsets.",
              verify=lambda: "Yes, %d subsets" % sum(1 for m in range(1 << 6) if sum(x for k, x in enumerate([3, 34, 4, 12, 5, 2]) if m >> k & 1) == 9)),
           Ex("Unbounded", "Items (value, weight) = (10, 2), (30, 5) may repeat. Capacity 12. Best value?",
              ["Take two of the (30, 5) items: weight 10, value 60, then one (10, 2) item: weight 12, value 70.", "Alternatives: six items of the first kind = 60. So **70**."], "**70**", verify=lambda: str(max(30 * a + 10 * b for a in range(3) for b in range(7) if 5 * a + 2 * b <= 12))),
           Ex("Counting evaluations", "n = 8 items and capacity W = 25. How many cell evaluations does the table need (excluding row 0)?", ["8 rows, each with W + 1 = 26 cells.", "8 × 26 = **208**."], "**208**", verify=lambda: str(8 * 26)),
       ],
       traps=[("Fill direction in one row", "Downwards for 0/1, upwards for unbounded."),
              ("Greedy on 0/1", "Ratio greedy is optimal only for the fractional version."),
              ("Not polynomial", "O(nW) is pseudo-polynomial; knapsack is NP-complete."),
              ("Wrong base", "K[0][c] = 0 for every c: no items, no value.")],
       quick=[("0/1 knapsack with n items and capacity W runs in", ["O(n log W)", "O(nW)", "O(n + W)", "O(2^W)"], 1, "n·W cells."),
              ("The one-row 0/1 update runs over c", ["upwards", "downwards", "either way", "only odd c"], 1, "Avoids reusing the item."),
              ("Fractional knapsack is solved by", ["DP", "greedy by ratio", "backtracking", "no known method"], 1, "Take the best ratio first."),
              ("Partition into equal halves is a case of", ["LCS", "subset sum", "matrix chain", "Dijkstra"], 1, "Target = total / 2.")],
       summary=["K[i][c] = max(leave, take) with the item's weight subtracted.", "O(nW) is pseudo-polynomial; the problem is NP-complete.", "One row: downwards for 0/1, upwards for unbounded.", "Subset sum: reach[s] |= reach[s − x].",
                "Greedy by ratio works only for fractional knapsack.", "Partition = subset sum with half the total."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=7, slug="algo-dp-matrix-chain", title="6 · Matrix-chain multiplication and interval DP",
       topic=TOPIC, subs=["Matrix chain table", "Matrix chain"], minutes=22, weight=5, widget="none",
       key="Multiplication of a chain is associative, but the cost depends on the order. The DP tries every last split point k and combines two sub-chains. It is the model for interval DP: states are intervals, filled by increasing length, with O(n³) time.",
       analogy=("📚", "Stacking boxes of different widths", "Merging two piles is cheap when the shapes line up and costly otherwise. Which two piles you merge last determines the whole bill, so you try every last merge and reuse the cost of the smaller piles."),
       sections=[
           dict(h="Cost of one multiplication", md="""A p × q matrix times a q × r matrix gives a p × r matrix and needs **p·q·r scalar multiplications**. The inner dimensions must agree. For a chain A₁…Aₙ with Aᵢ of size d[i−1] × d[i], different parenthesisations give very different totals: with 10 × 100, 100 × 5, 5 × 50, the order (A₁A₂)A₃ costs 10·100·5 + 10·5·50 = 7500, while A₁(A₂A₃) costs 100·5·50 + 10·100·50 = 75000."""),
           dict(h="The recurrence", md="""State `M[i][j]` = minimum cost of multiplying Aᵢ…Aⱼ.

    M[i][i] = 0
    M[i][j] = min over i ≤ k < j of  M[i][k] + M[k+1][j] + d[i-1]·d[k]·d[j]

The last multiplication joins (Aᵢ…Aₖ), of size d[i−1] × d[k], with (Aₖ₊₁…Aⱼ), of size d[k] × d[j]. Fill by **increasing chain length** L = 2, 3, …, n, because a chain of length L depends only on shorter ones. Store the best k in a second table to print the parenthesisation.

**Complexity:** n(n+1)/2 states, up to n − 1 splits each, so Θ(n³) time and Θ(n²) space."""),
           dict(h="A worked table", md="""d = (10, 20, 30, 40, 30): A₁ 10×20, A₂ 20×30, A₃ 30×40, A₄ 40×30.

| Chain | M | split k |
|---|---|---|
| A₁A₂ | 6000 | 1 |
| A₂A₃ | 24000 | 2 |
| A₃A₄ | 36000 | 3 |
| A₁A₂A₃ | 18000 | 2 |
| A₂A₃A₄ | 32000 | 2 |
| A₁…A₄ | **30000** | 3 |

Optimal order: **((A₁A₂)A₃)A₄**. For example M[1][4] with k = 3 is M[1][3] + M[4][4] + 10·40·30 = 18000 + 0 + 12000 = 30000."""),
           dict(h="Other interval problems", md="""The same shape (try every split of an interval, combine two halves) solves:

- **Optimal binary search tree** (best root for a key range, O(n³) with the plain recurrence),
- **Polygon triangulation** with minimum total cost,
- **Optimal parenthesisation of expressions**, **burst balloons**, **palindrome partitioning**.

The number of different parenthesisations of n matrices is the Catalan number C(n−1), exponential, which is why brute force fails."""),
       ],
       examples=[
           Ex("Single product", "Cost of multiplying a 12 × 7 matrix by a 7 × 5 matrix?", ["p·q·r = 12 × 7 × 5 = **420**."], "**420**", verify=lambda: str(12 * 7 * 5)),
           Ex("Orders compared", "Matrices of size 10×100, 100×5, 5×50. Cost of (A₁A₂)A₃ and of A₁(A₂A₃)?", ["(A₁A₂)A₃: 10·100·5 + 10·5·50 = 5000 + 2500 = 7500.", "A₁(A₂A₃): 100·5·50 + 10·100·50 = 25000 + 50000 = 75000."], "**7500** and **75000**.", verify=lambda: "%d and %d" % (10 * 100 * 5 + 10 * 5 * 50, 100 * 5 * 50 + 10 * 100 * 50)),
           Ex("Full DP", "d = (10, 20, 30, 40, 30). Minimum scalar multiplications for A₁A₂A₃A₄?", ["Compute M for chains of length 2, 3, 4 as in the table.", "M[1][4] = **30000**."], "**30000**", verify=lambda: str(A.mcm([10, 20, 30, 40, 30]))),
           Ex("Number of subproblems", "How many entries M[i][j] with i ≤ j for n = 6 matrices?", ["6 + 5 + 4 + 3 + 2 + 1 = **21**."], "**21**", verify=lambda: str(21)),
           Ex("Number of orders", "In how many different ways can 5 matrices be fully parenthesised?", ["C(n−1) = C₄ = 14."], "**14**", verify=lambda: str(14)),
           Ex("Split table", "d = (5, 10, 3, 12, 5). Optimal cost and parenthesisation?", ["Compute M for chains of length 2, 3 and 4 and record the best split.", "The best top-level split is after A₂, giving the order (A₁A₂)(A₃A₄): 5·10·3 + 3·12·5 + 5·3·5 = 150 + 180 + 75 = **405**."], "Cost **405**.", verify=lambda: "Cost %d" % D.mcm_table([5, 10, 3, 12, 5])[0][1][4]),
       ],
       traps=[("p·q·r", "Multiply the three outer dimensions, not the sums."),
              ("Fill order", "By chain length, not row by row."),
              ("Number of orders", "Catalan(n−1), not n!."),
              ("Splitting k", "k runs from i to j − 1; the right chain starts at k + 1.")],
       quick=[("Matrix chain DP time", ["O(n²)", "O(n³)", "O(n log n)", "O(2ⁿ)"], 1, "n² states × n splits."),
              ("Cost of a (p×q)(q×r) product", ["p+q+r", "pqr", "pr", "q²"], 1, "p·r dot products of length q."),
              ("Number of subproblems for n matrices", ["n", "n²", "n(n+1)/2", "2ⁿ"], 2, "One per i ≤ j."),
              ("The table is filled in order of", ["row", "column", "increasing chain length", "decreasing k"], 2, "Shorter chains first.")],
       summary=["Cost of (p×q)(q×r) is pqr.", "M[i][j] = min over k of M[i][k] + M[k+1][j] + d[i−1]d[k]d[j].", "Fill by increasing chain length.", "Time Θ(n³), space Θ(n²).", "Orders: Catalan(n−1).", "Interval DP: try every split of an interval."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=8, slug="algo-dp-problem-set", title="7 · Choosing the method and mixed problem set",
       topic=TOPIC, subs=["Choosing DP, greedy or D&C", "DP states and cost", "Coin change table", "LIS table", "LCS table", "Edit distance table", "Knapsack table", "Matrix chain table"], minutes=25, weight=5, widget="none",
       key="Decide first whether a single safe choice exists (greedy), whether subproblems are disjoint (divide and conquer) or overlap (DP). Then write the state, recurrence and order, and read the running time off the table. This lesson practises that decision and mixes every DP family.",
       analogy=("🧭", "Choosing the right tool", "A carpenter does not hammer every nail with the same swing. Here the question is: is there a safe local choice, do the pieces overlap, or can I split without overlap?"),
       sections=[
           dict(h="A decision checklist", md="""1. **Can a local choice be proved safe** (exchange argument)? Greedy: activity selection, Huffman, fractional knapsack, Dijkstra, Kruskal and Prim.
2. **Are the subproblems disjoint?** Divide and conquer: merge sort, quicksort, binary search, closest pair.
3. **Do subproblems repeat and does an optimal solution contain optimal sub-solutions?** DP: LCS, edit distance, 0/1 knapsack, matrix chain, coin change, LIS, Floyd–Warshall, Bellman–Ford.
4. **Is the structure a set of all subsets or permutations with no useful sub-structure?** Exhaustive search or an NP-hardness argument."""),
           dict(h="Reading the answer off the table", md="""| Family | Table | Answer cell |
|---|---|---|
| Coin combinations | one row, coins outside | last entry |
| Min coins | one row | last entry |
| LIS | one row | **maximum** entry |
| LCS, edit distance | (m+1)×(n+1) | bottom-right |
| Common substring | (m+1)×(n+1) | **maximum** entry |
| 0/1 knapsack | (n+1)×(W+1) | bottom-right |
| Matrix chain | n×n upper triangle | M[1][n] |"""),
           dict(h="Exam shortcuts", md="""- Checking a given answer is faster than filling the table: for LCS exhibit a common subsequence of that length and argue it cannot be longer.
- Table values grow slowly: neighbouring cells of LCS and edit tables differ by at most 1.
- For knapsack, check small subsets by brute force when n ≤ 5: there are only 32 subsets.
- For matrix chain with 3 matrices, compute just the two orders.
- State the complexity as (cells) × (work per cell)."""),
       ],
       examples=[
           Ex("Pick the method", "Is longest common subsequence a greedy problem?", ["Taking a match early can block a longer one later, and the subproblems (prefix pairs) repeat.", "So it needs DP: **dynamic programming**."], "**Dynamic programming.**", verify=lambda: "Dynamic programming."),
           Ex("Coin combinations", "Coins {1, 2, 5}, amount 11. How many combinations?", ["Process coins in order: ways ends as 1 1 2 2 3 4 5 6 7 8 10 11.", "ways[11] = **11**."], "**11**", verify=lambda: str(_ways([1, 2, 5], 11)[11])),
           Ex("LCS + edit", "X = ABCBDAB, Y = BDCABA. LCS length and the insert/delete-only distance?", ["LCS = 4.", "7 + 6 − 2·4 = **5**."], "LCS **4**, distance **5**.", verify=lambda: "LCS %d, distance %d" % (A.lcs("ABCBDAB", "BDCABA"), 7 + 6 - 2 * A.lcs("ABCBDAB", "BDCABA"))),
           Ex("Knapsack with ties", "Items (6, 2), (10, 2), (12, 3), capacity 5. Best value?", ["Options within weight 5: {1,2} = 16 (weight 4), {1,3} = 18 (weight 5), {2,3} = 22 (weight 5).", "Best **22**."], "**22**", verify=lambda: str(D.knap_table([(6, 2), (10, 2), (12, 3)], 5)[3][5])),
           Ex("Matrix chain", "d = (30, 35, 15, 5, 10, 20, 25) (the textbook example). Minimum cost?", ["Fill the 6 × 6 table by chain length.", "M[1][6] = **15125**."], "**15125**", verify=lambda: str(A.mcm([30, 35, 15, 5, 10, 20, 25]))),
           Ex("LIS", "LIS length of 5, 2, 8, 6, 3, 6, 9, 7?", ["L = 1, 1, 2, 2, 2, 3, 4, 4.", "Maximum **4**."], "**4**", verify=lambda: str(max(_lis([5, 2, 8, 6, 3, 6, 9, 7])))),
       ],
       traps=[("Taking DP for greedy", "A plausible local rule is not proof; test it on a small counterexample."),
              ("Mixing the answer cells", "Corner for LCS, maximum for LIS and substring."),
              ("Order of loops", "Coin and subset-sum loops encode what you count."),
              ("Quoting O(nW) as polynomial", "It is pseudo-polynomial.")],
       quick=[("Which problem is NOT solved by DP in polynomial time in the input size?", ["LCS", "Edit distance", "0/1 knapsack", "Matrix chain"], 2, "Knapsack is pseudo-polynomial."),
              ("Dijkstra's algorithm is an example of", ["DP only", "greedy", "divide and conquer", "backtracking"], 1, "It fixes the closest vertex each step."),
              ("LIS answer is", ["last L entry", "maximum L entry", "sum of L", "first L entry"], 1, "Subsequences can end anywhere."),
              ("The answer to the LCS problem is", ["maximum of the table", "bottom-right cell", "first column", "sum of diagonal"], 1, "Whole strings = full prefixes.")],
       summary=["Greedy needs a proof of a safe local choice.", "Divide and conquer: disjoint subproblems.", "DP: overlapping subproblems and optimal substructure.", "Time = cells × work per cell.",
                "Know the answer cell of each family.", "Knapsack is pseudo-polynomial."])
