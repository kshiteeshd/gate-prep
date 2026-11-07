"""Algorithms — part 1: asymptotics, recurrences & divide-and-conquer, sorting & searching, greedy."""
import heapq
import itertools
import math

from content import g_algo as A
from learn import Ex, lesson

S = "ALGO"


# ======================================================================================================
def _nested_geo(n):
    c, i = 0, 1
    while i < n:
        for _ in range(i):
            c += 1
        i *= 2
    return c


def _harmonic_loop(n):
    return sum(1 for i in range(1, n + 1) for _ in range(i, n + 1, i))


def _doubling_copies(n):
    cap, size, copies = 1, 0, 0
    for _ in range(n):
        if size == cap:
            copies += size
            cap *= 2
        size += 1
    return copies


lesson(subject=S, chapter="Analysis of Algorithms", ch_no=1, no=1, slug="algo-asymptotics", title="Asymptotic Analysis: Big-O, Ω, Θ & Loop Counting",
       topic="Asymptotic Analysis", minutes=20, weight=5, widget="growth",
       widget_hint="Drag n and watch how quickly the curves separate. Notice that 2ⁿ and n! leave everything else behind almost immediately.",
       key="Asymptotic notation compares how running time grows as the input gets large, ignoring constants and lower-order terms. Big-O is an upper bound, Ω a lower bound, Θ a tight bound — and the order 1 < log n < √n < n < n log n < n² < n³ < 2ⁿ < n! must be second nature.",
       analogy=("🚗", "Cars on a long road", "Compare a bicycle that starts 10 km ahead with a car that is faster. For a short trip the bicycle wins; over a long enough distance the car always wins. Asymptotic analysis asks only *who wins on a long enough road* — which is why constants and small terms are ignored."),
       sections=[
           dict(h="Big-O, Ω and Θ", md="""For positive functions f and g:

- **f(n) = O(g(n))** — f grows **no faster** than g: there are constants c, n₀ with f(n) ≤ c·g(n) for all n ≥ n₀. (*upper bound*)
- **f(n) = Ω(g(n))** — f grows **at least as fast**: f(n) ≥ c·g(n). (*lower bound*)
- **f(n) = Θ(g(n))** — both: f is sandwiched, so they grow at the **same rate**. (*tight bound*)
- **o(g)** and **ω(g)** — *strictly* slower / strictly faster.

**Limit test** (the fastest way in GATE): compute L = lim f(n)/g(n).

| L | Conclusion |
|---|---|
| 0 | f = o(g) — so f = O(g) but not Θ |
| a finite constant > 0 | f = Θ(g) |
| ∞ | f = ω(g) — so f = Ω(g) but not Θ |""",
                formulas=[("f = Θ(g)  ⇔  f = O(g) and f = Ω(g)", ""), ("f + g = Θ(max(f, g))   ·   f·g = Θ(f·g)", "sum and product rules")],
                call=[("trap", "Big-O is only an upper bound", "Saying ‘insertion sort is O(n³)’ is true but useless. When a question asks for the *tightest* bound, give Θ.")]),
           dict(h="The ordering of common functions", md="""Memorise this chain — GATE asks you to sort or compare these constantly:

    1  <  log log n  <  log n  <  √n  <  n  <  n log n  <  n²  <  n³  <  2ⁿ  <  n!  <  nⁿ

Useful facts: **logₐ n and log_b n differ by a constant**, so the base of a logarithm never matters inside Θ. Any polynomial beats any polylog (n^0.01 ≫ log¹⁰⁰ n) and any exponential beats any polynomial. **log(n!) = Θ(n log n)** (Stirling). 2ⁿ⁺¹ = Θ(2ⁿ) but **2²ⁿ = 4ⁿ is NOT O(2ⁿ)**; n^(log n) grows faster than any polynomial but slower than 2ⁿ."""),
           dict(h="Counting loop iterations", md="""Turn nested loops into sums:

| Pattern | Iterations |
|---|---|
| `for (i=1; i<=n; i++)` | n |
| `for (i=1; i<n; i*=2)` or `i/=2` | ⌈log₂ n⌉ |
| nested, independent: n × n | n² |
| `for i in 1..n: for j in 1..i` | n(n+1)/2 = Θ(n²) |
| `for (i=1; i<n; i*=2) for (j=0; j<i; j++)` | 1 + 2 + 4 + … < 2n = **Θ(n)** (geometric) |
| `for i in 1..n: for (j=i; j<=n; j+=i)` | Σ n/i = n·Hₙ = **Θ(n log n)** (harmonic) |
| `for (i=2; i<n; i=i*i)` | Θ(log log n) |

The geometric series is dominated by its **last term** (so it is linear); the harmonic series gives the extra log factor."""),
           dict(h="Best, worst, average — and amortised cost", md="""- **Worst case:** the maximum time over all inputs of size n (what Big-O usually reports). **Best case:** the minimum. **Average case:** expected time over a distribution of inputs.
- **Space complexity** counts extra memory beyond the input (recursion stack included).
- **Amortised analysis:** the average cost per operation over a *sequence*. Example: a dynamic array that **doubles** its capacity when full — a single insert can cost O(n) (copying), but n inserts copy at most 1 + 2 + 4 + … < 2n elements in total, so each insert costs **O(1) amortised**."""),
       ],
       examples=[
           Ex("A geometric nested loop", "How many times does the inner statement execute for n = 1024?  `for (i = 1; i < n; i *= 2) for (j = 0; j < i; j++) count++;`  What is the asymptotic order?",
              ["i takes the values 1, 2, 4, …, 512 (powers of 2 below 1024).", "The inner loop runs i times, so the total is 1 + 2 + 4 + … + 512 = 2¹⁰ − 1 = **1023**.", "In general the sum is < 2n, so the order is **Θ(n)** — not n log n, as the nested look suggests."],
              "**1023** iterations — Θ(n).", verify=lambda: str(_nested_geo(1024))),
           Ex("A harmonic loop", "For n = 1000 how many times does count++ run?  `for (i = 1; i <= n; i++) for (j = i; j <= n; j += i) count++;`",
              ["For a fixed i the inner loop runs ⌊n/i⌋ times (j = i, 2i, 3i, …).", "Total = Σ_{i=1..n} ⌊n/i⌋ = n·Hₙ ≈ n ln n = Θ(n log n); exactly **7069** for n = 1000."],
              "**7069** — Θ(n log n).", verify=lambda: str(_harmonic_loop(1000))),
           Ex("Comparing growth", "Is 2ⁿ⁺¹ = O(2ⁿ)? Is 2²ⁿ = O(2ⁿ)?",
              ["2ⁿ⁺¹ = 2·2ⁿ, so the ratio is the constant 2 ⇒ **yes** (even Θ).", "2²ⁿ / 2ⁿ = 2ⁿ → ∞ ⇒ **no**, 4ⁿ grows strictly faster."],
              "2ⁿ⁺¹ = O(2ⁿ): **yes**; 2²ⁿ = O(2ⁿ): **no**.", verify=lambda: "2ⁿ⁺¹ = O(2ⁿ): yes; 2²ⁿ = O(2ⁿ): no." if (2 ** 21) / (2 ** 20) == 2 and (2 ** 40) / (2 ** 20) > 1000 else "bad"),
           Ex("Amortised cost of a doubling array", "Starting from an empty array of capacity 1 that doubles when full, how many element copies occur in total while inserting 1024 elements?",
              ["Resizes happen at sizes 1, 2, 4, …, 512, copying that many elements each time.", "Total copies = 1 + 2 + … + 512 = **1023** < 2·1024.", "So n inserts cost O(n) in total — **O(1) amortised** per insert."],
              "**1023** copies — O(1) amortised.", verify=lambda: str(_doubling_copies(1024))),
       ],
       traps=[("Treating geometric sums as n log n", "Nested loops whose inner bound doubles with the outer index give a **linear** total, not n log n."),
              ("Constants and bases", "log₂ n, ln n and log₁₀ n are all Θ(log n); 100n and n/100 are both Θ(n)."),
              ("2ⁿ vs 4ⁿ", "Exponents multiply the base: 2²ⁿ = 4ⁿ is **not** O(2ⁿ), whereas 2ⁿ⁺ᶜ is."),
              ("Using O when Θ is asked", "O gives only an upper bound; for ‘tightest’ use Θ.")],
       quick=[("lim f/g = 5 (finite, positive) means", ["f = o(g)", "f = Θ(g)", "f = ω(g)", "nothing"], 1, "A finite non-zero limit means the same growth rate: Θ."),
              ("Which grows fastest?", ["n¹⁰⁰", "2ⁿ", "n^(log n)", "(log n)ⁿ"], 3, "(log n)ⁿ eventually beats 2ⁿ because log n > 2; n^(log n) is only quasi-polynomial."),
              ("The running time of `for (i = n; i >= 1; i /= 2)` is", ["Θ(n)", "Θ(log n)", "Θ(n log n)", "Θ(√n)"], 1, "n is halved each time."),
              ("log(n!) is", ["Θ(n)", "Θ(n log n)", "Θ(n²)", "Θ(log n)"], 1, "Stirling's approximation.")],
       summary=["O = upper, Ω = lower, Θ = tight; use lim f/g to decide.", "Order: 1 < log n < √n < n < n log n < n² < n³ < 2ⁿ < n! < nⁿ.", "Log base is irrelevant; polynomials beat polylogs; exponentials beat polynomials.",
                "Geometric nested loops → linear; harmonic loops → n log n; i = i² → log log n.", "Amortised: doubling array gives O(1) per insert.", "f + g = Θ(max), f·g = Θ(f·g)."])


# ======================================================================================================
def _master_ref(a, b, k):
    L = math.log(a, b)
    if abs(L - k) < 1e-9:
        return "Θ(n^%d log n)" % k if k > 1 else ("Θ(n log n)" if k == 1 else "Θ(log n)")
    if L > k:
        return "Θ(n^%s)" % (("%d" % round(L)) if abs(L - round(L)) < 1e-9 else ("%.3f" % L).rstrip("0"))
    return "Θ(n^%d)" % k if k > 1 else ("Θ(n)" if k == 1 else "Θ(1)")


def _t_exact(n, a, b, k):
    from functools import lru_cache

    @lru_cache(None)
    def T(m):
        return 1 if m <= 1 else a * T(m // b) + m ** k
    return T(n)


lesson(subject=S, chapter="Analysis of Algorithms", ch_no=1, no=2, slug="algo-recurrences-dc", title="Recurrences, the Master Theorem & Divide-and-Conquer",
       topic="Recurrences & Divide and Conquer", minutes=22, weight=5, widget="master",
       widget_hint="Set a, b, k (and p for log factors) or pick a classic — merge sort, binary search, Strassen. The tool names the Master-theorem case and the solution.",
       key="A divide-and-conquer algorithm solves a problem by splitting it into a subproblems of size n/b and combining the answers in f(n) time: T(n) = aT(n/b) + f(n). Compare f(n) with n^(log_b a) — whichever is larger (or equal, giving an extra log) decides the answer.",
       analogy=("📚", "Sorting a stack of exam papers", "Split the pile into two halves, give each half to a friend (who splits again), and finally merge the two sorted halves. The recursion has log n levels, each level does about n units of merging work in total — so n log n. The Master theorem is just a quick way to add up the work level by level."),
       sections=[
           dict(h="Setting up the recurrence", md="""Write the cost as **T(n) = a·T(n/b) + f(n)** where a ≥ 1 subproblems each of size n/b, plus f(n) work to divide and combine. Always state the base case T(1) = Θ(1).

| Algorithm | Recurrence | Solution |
|---|---|---|
| Binary search | T(n) = T(n/2) + 1 | Θ(log n) |
| Merge sort | T(n) = 2T(n/2) + n | Θ(n log n) |
| Quick sort (best/avg split) | T(n) = 2T(n/2) + n | Θ(n log n) |
| Quick sort (worst split) | T(n) = T(n−1) + n | Θ(n²) |
| Max & min (D&C) | T(n) = 2T(n/2) + 2 | Θ(n), exactly 3n/2 − 2 comparisons |
| Karatsuba | T(n) = 3T(n/2) + n | Θ(n^1.585) |
| Strassen | T(n) = 7T(n/2) + n² | Θ(n^2.807) |"""),
           dict(h="The Master theorem", md="""Let T(n) = aT(n/b) + Θ(nᵏ) with a ≥ 1, b > 1 and let **c = log_b a** (the *critical exponent*). Compare c with k:

| Case | Condition | Who dominates | Result |
|---|---|---|---|
| **1** | c > k | the leaves | **Θ(n^c)** = Θ(n^(log_b a)) |
| **2** | c = k | every level equally | **Θ(nᵏ log n)** |
| **3** | c < k | the root | **Θ(nᵏ)** (regularity holds for polynomials) |

Extended Case 2: if f(n) = Θ(nᶜ logᵖ n) with p ≥ 0 then T(n) = Θ(nᶜ logᵖ⁺¹ n). For example T(n) = 2T(n/2) + n log n = Θ(n log² n).""",
                formulas=[("c = log_b a ;  compare c with k", "the whole Master theorem")],
                call=[("tip", "Memorise the three cases by picture", "Draw the recursion tree: the work per level grows (leaves win), stays the same (every level ties, multiply by depth log n) or shrinks (root wins).")]),
           dict(h="When the Master theorem does not apply", md="""Use **iteration/substitution** or the **recursion tree**:

- **T(n) = T(n−1) + f(n):** unroll — T(n) = T(0) + Σ f(i). For f(n) = n this is Θ(n²); for f(n) = 1 it is Θ(n).
- **T(n) = T(n−1) + T(n−2) + 1** (Fibonacci-like): exponential, Θ(φⁿ) with φ ≈ 1.618.
- **T(n) = 2T(n−1) + 1:** Θ(2ⁿ) (Tower of Hanoi, exactly 2ⁿ − 1 moves).
- **T(n) = T(√n) + 1:** substitute n = 2ᵐ ⇒ Θ(log log n).
- **T(n) = T(n/3) + T(2n/3) + n:** unbalanced but each level costs at most n and there are log_{3/2} n levels ⇒ Θ(n log n)."""),
           dict(h="Classic divide-and-conquer algorithms", md="""- **Merge sort:** split, sort halves, merge in O(n) — Θ(n log n) always, O(n) extra space.
- **Quick sort:** partition around a pivot; balanced splits give n log n, a sorted input with a bad pivot gives n².
- **Counting inversions:** modified merge sort, O(n log n).
- **Closest pair of points:** O(n log n). **Strassen:** multiplies matrices with 7 sub-multiplications instead of 8.
- **Finding the max and min together:** a pairing trick needs only **⌈3n/2⌉ − 2** comparisons instead of 2n − 2.
- **Binary search** needs ⌊log₂ n⌋ + 1 comparisons in the worst case."""),
       ],
       examples=[
           Ex("Master theorem, Case 1", "Solve T(n) = 8T(n/2) + n².",
              ["a = 8, b = 2, so c = log₂ 8 = 3. Here f(n) = n², k = 2.", "c = 3 > k = 2 ⇒ Case 1: the leaves dominate.", "T(n) = Θ(n³)."],
              "**Θ(n³)**", verify=lambda: _master_ref(8, 2, 2)),
           Ex("Master theorem, Case 2", "Solve T(n) = 4T(n/2) + n².",
              ["a = 4, b = 2 ⇒ c = log₂ 4 = 2, and k = 2.", "c = k ⇒ Case 2: every level costs n², and there are log n levels.", "T(n) = Θ(n² log n)."],
              "**Θ(n² log n)**", verify=lambda: _master_ref(4, 2, 2)),
           Ex("Master theorem, Case 3", "Solve T(n) = 2T(n/2) + n².",
              ["a = 2, b = 2 ⇒ c = 1 < k = 2 ⇒ Case 3: the root dominates.", "T(n) = Θ(n²). (The geometric series n² + n²/2 + n²/4 + … sums to 2n².)"],
              "**Θ(n²)**", verify=lambda: _master_ref(2, 2, 2)),
           Ex("Karatsuba's exponent", "Solve T(n) = 3T(n/2) + n and give the exponent to 3 decimals.",
              ["c = log₂ 3 ≈ 1.585 and k = 1, so c > k: Case 1.", "T(n) = Θ(n^1.585)."],
              "**Θ(n^1.585)**", verify=lambda: _master_ref(3, 2, 1)),
           Ex("Max and min comparisons", "How many comparisons does the pairing method need to find both the max and the min of n = 10 distinct numbers?",
              ["Compare the 5 pairs: 5 comparisons; the 5 winners contain the max, the 5 losers contain the min.", "Max among 5 winners: 4; min among 5 losers: 4.", "Total = 5 + 4 + 4 = 13 = ⌈3·10/2⌉ − 2 = **13**."],
              "**13**", verify=lambda: str(5 + 4 + 4)),
       ],
       traps=[("Applying the theorem to T(n) = T(n−1) + n", "The subproblem size must shrink by a **factor** (n/b), not by a constant. Use unrolling instead."),
              ("Wrong critical exponent", "log_b a — the base is b (the shrink factor), the argument is a (the branching). log₂ 8 = 3, not 8/2."),
              ("Forgetting the extra log in Case 2", "When f(n) = nᶜ exactly, the answer is nᶜ log n, not nᶜ."),
              ("Quick sort's worst case", "Merge sort is always n log n; quick sort degrades to n² when every pivot is the min or max.")],
       quick=[("T(n) = 2T(n/2) + n has solution", ["Θ(n)", "Θ(n log n)", "Θ(n²)", "Θ(log n)"], 1, "c = 1 = k ⇒ Case 2."),
              ("T(n) = T(n/2) + 1 is the recurrence of", ["merge sort", "binary search", "Strassen", "quick sort"], 1, "One recursive call on half, constant work."),
              ("T(n) = 7T(n/2) + n² gives", ["Θ(n²)", "Θ(n² log n)", "Θ(n^2.81)", "Θ(n³)"], 2, "c = log₂ 7 ≈ 2.807 > 2."),
              ("T(n) = 2T(n − 1) + 1 has solution", ["Θ(n)", "Θ(n²)", "Θ(2ⁿ)", "Θ(log n)"], 2, "Tower of Hanoi.")],
       summary=["T(n) = aT(n/b) + Θ(nᵏ): compare c = log_b a with k.", "c > k ⇒ Θ(nᶜ); c = k ⇒ Θ(nᵏ log n); c < k ⇒ Θ(nᵏ).", "T(n−1) + n → n²; 2T(n−1) + 1 → 2ⁿ; T(√n) + 1 → log log n.",
                "Merge sort Θ(n log n); binary search Θ(log n); Strassen Θ(n^2.807); Karatsuba Θ(n^1.585).", "Max & min together: ⌈3n/2⌉ − 2 comparisons.", "Master theorem needs shrink by a factor, not a constant."])


# ======================================================================================================
def _tournament_minmax(n):
    import random
    xs = random.Random(5).sample(range(1000), n)
    c = 0
    mx = mn = None
    i = 0
    if n % 2:
        mx = mn = xs[0]; i = 1
    else:
        c += 1
        mx, mn = (xs[0], xs[1]) if xs[0] > xs[1] else (xs[1], xs[0]); i = 2
    while i < n:
        a, b = xs[i], xs[i + 1]
        c += 1
        hi, lo = (a, b) if a > b else (b, a)
        c += 1
        mx = hi if hi > mx else mx
        c += 1
        mn = lo if lo < mn else mn
        i += 2
    return c


lesson(subject=S, chapter="Sorting, Searching & Greedy", ch_no=2, no=1, slug="algo-sorting-searching", title="Sorting Algorithms & Searching",
       topic="Sorting & Searching", minutes=24, weight=5, widget="sort",
       widget_hint="Type an array, choose an algorithm and step through it. Compare the comparison and swap counters across algorithms on the same input — try an already sorted array and a reversed one.",
       key="Know each classic sort's best/average/worst time, extra space and whether it is stable. Comparison sorts cannot beat Ω(n log n); counting-style sorts reach O(n) by not comparing. Insertion sort's work equals the number of inversions.",
       analogy=("🃏", "Sorting a hand of cards", "Insertion sort is how most people sort playing cards: pick up the next card and slide it into place among the cards you already hold. If your hand is almost sorted, each card hardly moves — that is why insertion sort is fast on nearly-sorted data."),
       sections=[
           dict(h="The comparison table to memorise", md="""| Algorithm | Best | Average | Worst | Extra space | Stable? |
|---|---|---|---|---|---|
| Bubble sort | n (with early exit) | n² | n² | 1 | yes |
| Selection sort | n² | n² | n² | 1 | no |
| Insertion sort | **n** | n² | n² | 1 | yes |
| Merge sort | n log n | n log n | n log n | **n** | yes |
| Quick sort | n log n | n log n | **n²** | log n (stack) | no |
| Heap sort | n log n | n log n | n log n | 1 | no |
| Counting sort | n + k | n + k | n + k | k | yes |
| Radix sort | d(n + k) | d(n + k) | d(n + k) | n + k | yes |

A sort is **stable** if equal keys keep their original relative order. **In-place** means O(1) (or O(log n)) extra space."""),
           dict(h="Quadratic sorts and inversions", md="""An **inversion** is a pair i < j with a[i] > a[j]. A sorted array has 0 inversions; a reversed array has n(n−1)/2.

- **Bubble sort** swaps only adjacent elements, so the number of swaps = number of inversions.
- **Insertion sort** shifts each element left past larger ones: shifts = inversions, comparisons ≈ n − 1 + inversions. Running time Θ(n + I).
- **Selection sort** always makes n(n−1)/2 comparisons but at most **n − 1 swaps** — the fewest writes of any simple sort.""",
                formulas=[("max inversions = n(n−1)/2", "reversed array"), ("insertion sort time = Θ(n + #inversions)", "")]),
           dict(h="Merge sort, quick sort, heap sort", md="""- **Merge sort:** divide, sort halves recursively, merge with n − 1 comparisons at most. Always Θ(n log n); needs an auxiliary array; stable.
- **Quick sort:** pick a pivot, **partition** so smaller elements go left and larger right, recurse. Lomuto (last pivot) scans with index i and swaps; Hoare uses two converging pointers. Worst case Θ(n²) (already-sorted input with first/last pivot); average Θ(n log n); **randomised** pivots make the worst case unlikely. Not stable.
- **Heap sort:** build a max-heap in O(n), then repeatedly swap the root to the end and sift down: O(n log n), in place, not stable. (Heaps get their own lesson.)""",
                call=[("key", "Partition facts", "After one partition the pivot is in its **final sorted position**; elements to its left are ≤ pivot and to its right are > pivot. The returned index equals the number of elements smaller than or equal to the pivot.")]),
           dict(h="Lower bound and linear-time sorts", md="""Any comparison-based sort is a binary **decision tree** with at least n! leaves, so its height — the worst-case comparisons — is at least **⌈log₂ n!⌉ = Ω(n log n)**. (For n = 5 that is 7 comparisons.)

Non-comparison sorts beat it by using the *values* of the keys:

- **Counting sort:** keys are integers in 0..k; count occurrences, prefix-sum, place elements. O(n + k), stable.
- **Radix sort:** sort by each digit with a stable sort, least-significant first. O(d(n + k)).
- **Bucket sort:** distribute uniformly distributed reals into n buckets, sort each; O(n) expected."""),
           dict(h="Searching and selection", md="""- **Linear search:** Θ(n). **Binary search** on a sorted array: Θ(log n); at most ⌊log₂ n⌋ + 1 probes.
- **Hash table search:** O(1) expected (see the hashing lesson).
- **Selection (k-th smallest):** **Quickselect** averages O(n) (worst n²); **median of medians** guarantees O(n). Finding both the min and max needs **⌈3n/2⌉ − 2** comparisons; the second smallest needs **n + ⌈log₂ n⌉ − 2**."""),
       ],
       examples=[
           Ex("Counting inversions", "Insertion sort is run on [5, 2, 9, 1, 7, 3, 8]. How many element shifts does it perform?",
              ["Each shift removes exactly one inversion, so shifts = number of inversions.", "Count pairs (i<j) with a[i] > a[j]: 5 has 3 smaller after it (2,1,3); 2 has 1 (1); 9 has 4 (1,7,3,8); 1 has 0; 7 has 1 (3); 3 has 0; 8 has 0.", "Total = 3 + 1 + 4 + 0 + 1 = **9**."],
              "**9** shifts.", verify=lambda: str(A.inversions([5, 2, 9, 1, 7, 3, 8]))),
           Ex("Quick sort partition", "Lomuto partition (pivot = last element) is applied to [8, 3, 5, 1, 9, 2, 6]. At which index does the pivot end up?",
              ["Pivot = 6. Elements ≤ 6 are 3, 5, 1, 2 — four of them.", "So the pivot lands at index **4** (0-based), with those four elements before it."],
              "**4**", verify=lambda: str(A.lomuto([8, 3, 5, 1, 9, 2, 6])[1])),
           Ex("Decision-tree lower bound", "What is the minimum number of comparisons that guarantees sorting 5 distinct elements in the worst case?",
              ["5! = 120 possible orderings, so the decision tree needs at least 120 leaves.", "Height ≥ ⌈log₂ 120⌉ = ⌈6.9⌉ = **7**."],
              "**7**", verify=lambda: str(math.ceil(math.log2(math.factorial(5))))),
           Ex("Selection sort swaps", "How many swaps does selection sort (swap only when needed) make on [64, 25, 12, 22, 11]?",
              ["Pass 1: min of all is 11 → swap with 64 ⇒ [11, 25, 12, 22, 64].", "Pass 2: min of rest is 12 → swap ⇒ [11, 12, 25, 22, 64].", "Pass 3: min is 22 → swap ⇒ [11, 12, 22, 25, 64].", "Pass 4: 25 and 64 already in order — no swap. Total = **3** swaps."],
              "**3**", verify=lambda: str(A.selection_swaps([64, 25, 12, 22, 11]))),
           Ex("Max and min with pairing", "How many comparisons does the pairing method use to find the max and min of 10 numbers (counted by simulation)?",
              ["Compare the first pair (1), then process 4 more pairs: each costs 1 (within the pair) + 1 (vs max) + 1 (vs min) = 3.", "Total = 1 + 4·3 = **13** = ⌈3·10/2⌉ − 2."],
              "**13**", verify=lambda: str(_tournament_minmax(10))),
       ],
       traps=[("Insertion sort on nearly sorted data", "It is Θ(n + inversions), so it can beat merge sort on almost-sorted input. Don't say ‘always n²’."),
              ("Quick sort ‘always n log n’", "Average only. Worst case is n² (and not stable)."),
              ("Stability of selection and heap sort", "Both are **not** stable (long-distance swaps). Merge, insertion, bubble and counting sort are."),
              ("Lower bound scope", "Ω(n log n) applies to **comparison** sorts only; counting/radix sort are linear.")],
       quick=[("Which sorting algorithm has the best worst-case time among these?", ["Quick sort", "Merge sort", "Insertion sort", "Selection sort"], 1, "Merge sort is Θ(n log n) in the worst case."),
              ("A reversed array of n elements has how many inversions?", ["n", "n log n", "n(n−1)/2", "2ⁿ"], 2, "Every pair is out of order."),
              ("Which sorts are stable?", ["Merge and insertion", "Quick and heap", "Selection and heap", "Quick and selection"], 0, "Merge, insertion, bubble and counting sort are stable."),
              ("Counting sort on n integers in 0..k runs in", ["Θ(n log n)", "Θ(n + k)", "Θ(nk)", "Θ(k log n)"], 1, "Count, prefix-sum, place.")],
       summary=["Insertion: best n, worst n², Θ(n + inversions), stable. Selection: n² always, ≤ n − 1 swaps. Bubble: swaps = inversions.", "Merge: n log n always, O(n) space, stable. Quick: avg n log n, worst n², not stable. Heap: n log n, in place, not stable.",
                "Comparison-sort lower bound ⌈log₂ n!⌉ = Ω(n log n).", "Counting O(n + k), radix O(d(n + k)), bucket O(n) expected.", "Binary search ⌊log₂ n⌋ + 1; min & max ⌈3n/2⌉ − 2; second smallest n + ⌈log₂ n⌉ − 2.", "After partition the pivot is in its final position."])


# ======================================================================================================
def _huffman_cost(freqs):
    h = list(freqs)
    heapq.heapify(h)
    tot = 0
    while len(h) > 1:
        a, b = heapq.heappop(h), heapq.heappop(h)
        tot += a + b
        heapq.heappush(h, a + b)
    return tot


def _activity(acts):
    cnt, end = 0, -1
    for s, e in sorted(acts, key=lambda x: (x[1], x[0])):
        if s >= end:
            cnt += 1; end = e
    return cnt


def _greedy_coin_fail():
    coins = [1, 3, 4]
    g, n = 0, 6
    for c in sorted(coins, reverse=True):
        g += n // c; n %= c
    best = min(a + b for a in range(7) for b in range(7) for c in range(7) if 4 * a + 3 * b + c == 6 for a, b in [(a, b)]) if False else None
    dp = [0] + [99] * 6
    for i in range(1, 7):
        dp[i] = min(dp[i - c] + 1 for c in coins if c <= i)
    return g, dp[6]


lesson(subject=S, chapter="Sorting, Searching & Greedy", ch_no=2, no=2, slug="algo-greedy", title="Greedy Algorithms: Activity Selection, Huffman & Knapsack",
       topic="Greedy Algorithms", minutes=20, weight=4, widget="none",
       key="A greedy algorithm makes the locally best choice at each step and never reconsiders. It works only when the problem has the greedy-choice property and optimal substructure — proved by an exchange argument. Greedy is optimal for activity selection, Huffman codes, fractional knapsack and MST, but not for 0/1 knapsack or general coin change.",
       analogy=("🧳", "Packing a suitcase by value per kilo", "If you may break items into pieces (sand, rice), you simply fill the bag with the most valuable-per-kilo stuff first — and you are guaranteed the best. If items are indivisible (a TV, a laptop) the same rule can fail, because a big item may leave awkward unused space."),
       sections=[
           dict(h="What makes greedy work", md="""A greedy algorithm builds a solution step by step, always taking the option that looks best *right now*. To be correct the problem needs:

- **Greedy-choice property:** some optimal solution contains the greedy first choice.
- **Optimal substructure:** after the choice, the rest is an optimal solution of a smaller problem.

The standard proof is an **exchange argument**: take any optimal solution and swap its first element for the greedy one without making it worse. Greedy algorithms are usually simple and fast — typically O(n log n) because of a sort or a heap."""),
           dict(h="Activity selection", md="""Given n activities with start and finish times, choose the **maximum number** of mutually compatible (non-overlapping) activities.

**Greedy rule:** sort by **earliest finish time**; repeatedly take the next activity whose start ≥ the finish time of the last chosen one. Time O(n log n). (Earliest *start*, shortest duration, or fewest conflicts are all **wrong** rules.)"""),
           dict(h="Fractional knapsack and job sequencing", md="""**Fractional knapsack** (items can be split): sort by **value/weight ratio** descending; take whole items until the next does not fit, then take the fraction that fills the knapsack. Optimal, O(n log n). The **0/1 knapsack** (no splitting) is *not* solved by this rule — it needs dynamic programming.

**Job sequencing with deadlines** (unit-time jobs, each with a profit and a deadline): sort by **profit descending**; place each job in the **latest free slot** on or before its deadline; skip it if none is free. Maximises total profit."""),
           dict(h="Huffman coding", md="""Build an optimal **prefix-free** binary code for symbols with frequencies fᵢ:

1. Put all symbols in a min-heap keyed by frequency.
2. Repeatedly remove the two smallest, merge them into a node whose weight is their sum, and push it back.
3. Continue until one node remains — the code tree. Left = 0, right = 1.

The total encoded length is **Σ fᵢ·(depth of symbol i)** = the **sum of the weights of all internal (merged) nodes**. Frequent symbols get short codes. Time O(n log n). Huffman codes are optimal among prefix codes but not unique (ties)."""),
           dict(h="Greedy for graphs, and when it fails", md="""**Kruskal** and **Prim** (minimum spanning trees) and **Dijkstra** (shortest paths with non-negative weights) are greedy algorithms — covered in the graph lessons.

**Greedy fails** for: 0/1 knapsack; the longest path; general **coin change** — with coins {1, 3, 4} and amount 6 greedy picks 4 + 1 + 1 (3 coins) but the optimum is 3 + 3 (2 coins). Greedy coin change is optimal only for special systems (like 1, 5, 10, 25)."""),
       ],
       examples=[
           Ex("Huffman cost", "Symbols have frequencies 5, 9, 12, 13, 16, 45. What is the total number of bits in the Huffman encoding (Σ frequency × code length)?",
              ["Merge 5 + 9 = 14; merge 12 + 13 = 25; merge 14 + 16 = 30; merge 25 + 30 = 55; merge 45 + 55 = 100.", "Sum of all merged weights = 14 + 25 + 30 + 55 + 100 = **224**."],
              "**224** bits.", verify=lambda: str(_huffman_cost([5, 9, 12, 13, 16, 45]))),
           Ex("Activity selection", "Activities (start, finish): (1,4), (3,5), (0,6), (5,7), (3,9), (5,9), (6,10), (8,11), (8,12), (2,14), (12,16). How many can be chosen?",
              ["Sort by finish time and pick greedily: (1,4) → next start ≥ 4: (5,7) → next start ≥ 7: (8,11) → next start ≥ 11: (12,16).", "Total = **4**."],
              "**4**", verify=lambda: str(_activity([(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]))),
           Ex("Fractional knapsack", "Capacity 50; items (value, weight): (60, 10), (100, 20), (120, 30). Find the maximum value with fractional items.",
              ["Ratios: 6, 5, 4. Take item 1 (10 kg, 60), item 2 (20 kg, 100): 30 kg used.", "Remaining 20 kg of item 3: fraction 20/30 → value 120·(2/3) = 80.", "Total = 60 + 100 + 80 = **240**."],
              "**240**", verify=lambda: str(sum(v if i < 2 else v * 20 / 30 for i, (v, w) in enumerate([(60, 10), (100, 20), (120, 30)])))),
           Ex("Greedy coin change fails", "Coins {1, 3, 4}, amount 6. How many coins does the greedy method use, and what is the optimum?",
              ["Greedy: take 4 (remaining 2), then 1, then 1 → **3** coins.", "Optimum: 3 + 3 → **2** coins.", "So the greedy rule is not optimal for this coin system."],
              "Greedy uses **3** coins; the optimum is **2**.", verify=lambda: "%d, %d" % _greedy_coin_fail()),
       ],
       traps=[("Wrong activity-selection rule", "Earliest finish time is the correct rule; earliest start or shortest duration have counter-examples."),
              ("Greedy for 0/1 knapsack", "Value/weight greedy is optimal only for the fractional version."),
              ("Huffman cost", "Add the **merged** weights (all internal nodes), not the leaf frequencies."),
              ("Assuming greedy always works", "Always look for a counter-example (coin systems, longest path) before trusting a greedy rule.")],
       quick=[("In activity selection the greedy choice is the activity with the", ["earliest start", "shortest duration", "earliest finish", "fewest conflicts"], 2, "Earliest finish leaves the most room for the rest."),
              ("Fractional knapsack is solved optimally by sorting on", ["value", "weight", "value/weight", "weight/value ascending"], 2, "Highest value per unit weight first."),
              ("Huffman coding produces", ["a fixed-length code", "an optimal prefix-free code", "a non-prefix code", "an error-correcting code"], 1, "Optimal among prefix codes."),
              ("Which problem is NOT solved optimally by a greedy algorithm?", ["MST", "Activity selection", "0/1 knapsack", "Huffman coding"], 2, "0/1 knapsack needs DP.")],
       summary=["Greedy = locally best choice; needs greedy-choice property + optimal substructure; proof by exchange argument.", "Activity selection: sort by finish time. Fractional knapsack: sort by value/weight. Job sequencing: profit descending, latest free slot.",
                "Huffman: merge the two smallest repeatedly; cost = sum of merged weights; O(n log n).", "Greedy is optimal for MST, Dijkstra (non-negative), Huffman; fails for 0/1 knapsack and general coin change.", "Typical running time O(n log n) from sorting / heaps.", "Always test greedy against a counter-example."])
