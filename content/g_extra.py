"""Extra generators for thin topics: NP problems, fork simulation, synchronization, combinational logic, I/O, verbal."""
import itertools
import math

from content.kit import *

# =================== ALGO: complexity classes (brute-force NP problems) ===================
AL = "ALGO"
CCT = "Complexity Classes"


def rgraph(r, n, p):
    return sorted({(a, b) for a in range(n) for b in range(a + 1, n) if r.random() < p})


def max_indep(n, e):
    best = 0
    for m in range(1 << n):
        if all(not (m >> a & 1 and m >> b & 1) for a, b in e): best = max(best, bin(m).count("1"))
    return best


def max_clique(n, e):
    s = set(e)
    best = 1
    for m in range(1 << n):
        v = [i for i in range(n) if m >> i & 1]
        if all((a, b) in s for a, b in itertools.combinations(v, 2)): best = max(best, len(v))
    return best


def ham_cycle(n, e):
    s = set(e) | {(b, a) for a, b in e}
    for p in itertools.permutations(range(1, n)):
        path = (0,) + p
        if all((path[i], path[(i + 1) % n]) in s for i in range(n)): return True
    return False


@gen(AL, CCT, "NP problems on small graphs", n=90, diff="medium", marks=2)
def np_graph(r):
    n = r.randint(5, 7)
    e = rgraph(r, n, r.choice([0.35, 0.5, 0.6]))
    if len(e) < n - 1: raise Skip()
    es = ", ".join("%s%s" % (chr(65 + a), chr(65 + b)) for a, b in e)
    ctx = "Undirected graph on vertices %s with edges {%s}." % (",".join(chr(65 + i) for i in range(n)), es)
    kind = r.choice(["mis", "vc", "clique", "ham"])
    if kind == "mis": return nat(r, ctx + " What is the size of a maximum independent set?", max_indep(n, e), "Brute force over all 2^n subsets.")
    if kind == "vc": return nat(r, ctx + " What is the size of a minimum vertex cover?", n - max_indep(n, e), "Minimum vertex cover = n − maximum independent set.")
    if kind == "clique": return nat(r, ctx + " What is the size of the largest clique?", max_clique(n, e), "Brute force over subsets.")
    h = ham_cycle(n, e)
    return mcq(r, ctx + " Does the graph contain a Hamiltonian cycle?", "Yes" if h else "No", ["No" if h else "Yes", "Only if it is bipartite", "Only if every degree is even"], "Searched all vertex orderings.")


@gen(AL, CCT, "Subset sum & SAT", n=70, diff="medium")
def np_misc(r):
    kind = r.choice(["subset", "sat", "partition"])
    if kind == "subset":
        a = [r.randint(2, 20) for _ in range(r.randint(5, 7))]
        t = r.randint(10, sum(a) - 5)
        ways = sum(1 for m in range(1 << len(a)) if sum(a[i] for i in range(len(a)) if m >> i & 1) == t)
        return nat(r, "Numbers %s, target %d. In how many different subsets (by position) do the elements sum exactly to the target?" % (a, t), ways, "Enumerate all 2^n subsets.")
    if kind == "sat":
        n = 4
        cl = [tuple(r.choice([-1, 1]) * v for v in r.sample(range(1, n + 1), 3)) for _ in range(r.randint(4, 7))]
        c = sum(1 for m in range(1 << n) if all(any((m >> (abs(l) - 1) & 1) == (1 if l > 0 else 0) for l in cl_) for cl_ in cl))
        f = " ∧ ".join("(" + " ∨ ".join(("x%d" % l) if l > 0 else ("¬x%d" % -l) for l in cl_) + ")" for cl_ in cl)
        return nat(r, "How many of the 16 assignments to x1..x4 satisfy the 3-CNF formula  %s ?" % f, c, "Evaluate every assignment.")
    a = [r.randint(1, 12) for _ in range(r.randint(5, 7))]
    tot = sum(a)
    ok = tot % 2 == 0 and any(sum(a[i] for i in range(len(a)) if m >> i & 1) == tot // 2 for m in range(1 << len(a)))
    return mcq(r, "Can the multiset %s be split into two groups with EQUAL sums (partition problem)?" % a, "Yes" if ok else "No", ["No" if ok else "Yes", "Only if its size is even", "Only if all numbers are distinct"], "Total = %d." % tot)


CLS = [("Shortest path in a weighted graph (non-negative weights)", "P"), ("Minimum spanning tree", "P"), ("2-SAT", "P"), ("Bipartiteness testing", "P"), ("Maximum bipartite matching", "P"),
       ("Maximum flow", "P"), ("Primality testing", "P"), ("Eulerian circuit existence", "P"), ("Linear programming", "P"), ("2-colourability of a graph", "P"), ("Topological sorting", "P"),
       ("3-SAT", "NPC"), ("Vertex cover (decision)", "NPC"), ("Clique (decision)", "NPC"), ("Independent set (decision)", "NPC"), ("Hamiltonian cycle", "NPC"), ("Travelling salesman (decision)", "NPC"),
       ("3-colourability of a graph", "NPC"), ("Subset sum", "NPC"), ("Set cover (decision)", "NPC"), ("0/1 knapsack (decision)", "NPC"), ("Bin packing (decision)", "NPC"), ("Longest simple path (decision)", "NPC"),
       ("The halting problem", "UND"), ("Whether a program prints 'hello' on some input", "UND"), ("Post correspondence problem", "UND"), ("Equivalence of two Turing machines", "UND")]
CNAME = {"P": "in P", "NPC": "NP-complete", "UND": "undecidable"}
WHY = {
    "Shortest path in a weighted graph (non-negative weights)": "Dijkstra's algorithm solves it in O((V + E) log V).",
    "Minimum spanning tree": "Kruskal and Prim both run in polynomial time (O(E log V)).",
    "2-SAT": "Each clause (a ∨ b) is two implications; satisfiability reduces to strongly connected components of the implication graph in linear time.",
    "Bipartiteness testing": "A BFS/DFS 2-colouring decides it in O(V + E): the graph is bipartite iff it has no odd cycle.",
    "Maximum bipartite matching": "Augmenting paths (Hopcroft–Karp) find it in polynomial time.",
    "Maximum flow": "Ford–Fulkerson/Edmonds–Karp/Dinic solve it in polynomial time.",
    "Primality testing": "The AKS algorithm decides primality in polynomial time in the number of bits.",
    "Eulerian circuit existence": "A connected graph has an Euler circuit iff every vertex has even degree, which is checked in linear time.",
    "Linear programming": "The ellipsoid and interior-point methods solve LPs in polynomial time (the simplex method is fast in practice).",
    "2-colourability of a graph": "Same as bipartiteness: two-colour by BFS and look for a conflict.",
    "Topological sorting": "DFS finishing order (or Kahn's algorithm) sorts a DAG in O(V + E).",
    "3-SAT": "3-SAT is the classic NP-complete problem (Cook–Levin); it is in NP because a satisfying assignment is verified in polynomial time.",
    "Vertex cover (decision)": "NP-complete: reduce from independent set/3-SAT; a proposed cover is checked in polynomial time.",
    "Clique (decision)": "NP-complete (reduction from 3-SAT); a clique is easy to verify.",
    "Independent set (decision)": "NP-complete; S is independent iff V − S is a vertex cover, so it is equivalent to vertex cover.",
    "Hamiltonian cycle": "NP-complete (Karp's list); verifying a given cycle is polynomial.",
    "Travelling salesman (decision)": "NP-complete: Hamiltonian cycle reduces to it by giving edges cost 1 and non-edges cost 2.",
    "3-colourability of a graph": "NP-complete even though 2-colourability is in P.",
    "Subset sum": "NP-complete; its dynamic program O(nS) is only pseudo-polynomial.",
    "Set cover (decision)": "NP-complete (vertex cover is a special case).",
    "0/1 knapsack (decision)": "NP-complete (weakly), solvable in pseudo-polynomial time by dynamic programming.",
    "Bin packing (decision)": "NP-complete, via a reduction from partition.",
    "Longest simple path (decision)": "NP-complete: Hamiltonian path asks for a simple path of length |V| − 1.",
    "The halting problem": "Turing's diagonal argument shows no algorithm decides whether an arbitrary program halts.",
    "Whether a program prints 'hello' on some input": "A non-trivial semantic property of programs, so Rice's theorem makes it undecidable.",
    "Post correspondence problem": "Undecidable by reduction from the halting problem (it is semi-decidable).",
    "Equivalence of two Turing machines": "A non-trivial property of the recognised language, undecidable by Rice's theorem.",
}


@gen(AL, CCT, "Classification", n=110, diff="easy")
def np_class(r):
    p, c = r.choice(CLS)
    return mcq(r, "The problem “%s” is" % p, CNAME[c], [v for k, v in CNAME.items() if k != c] + ["in co-NP but not in NP"], "%s — %s" % (CNAME[c].capitalize(), WHY[p]))


@gen(AL, CCT, "Classification", n=110, diff="medium", marks=2)
def np_class_msq(r):
    want = r.choice(["P", "NPC"])
    yes = [p for p, c in CLS if c == want]
    no = [p for p, c in CLS if c != want]
    ys, ns = r.sample(yes, 2), r.sample(no, 2)
    why = "Correct: " + " ".join("%s — %s" % (p, WHY[p]) for p in ys) + " Not %s: " % CNAME[want] + " ".join("%s is %s — %s" % (p, CNAME[dict(CLS)[p]], WHY[p]) for p in ns)
    return msq(r, "Which of the following problems are %s? (select all)" % CNAME[want], ys, ns, why)


@gen(AL, CCT, "Reductions", n=40, diff="medium")
def np_red(r):
    n = r.randint(6, 30)
    k = r.randint(2, n - 2)
    kind = r.choice(["vc_is", "clique_is", "cnf", "sat_size"])
    if kind == "vc_is": return nat(r, "A graph with %d vertices has an independent set of size %d. What is the size of the complementary vertex cover?" % (n, k), n - k, "V − S is a vertex cover when S is independent.")
    if kind == "clique_is": return nat(r, "A graph G on %d vertices has a clique of size %d. What is the size of the largest independent set guaranteed in the COMPLEMENT graph?" % (n, k), k, "Cliques of G are independent sets of the complement.")
    if kind == "cnf": return nat(r, "Reducing a CNF clause with %d literals to 3-CNF (using the standard chain of new variables) yields how many 3-literal clauses? (clause has more than 3 literals)" % (k + 3), k + 1, "A clause of size m > 3 becomes m − 2 clauses.")
    return nat(r, "Number of 3-literal clauses and variables are %d and %d. A 3-SAT instance is reduced to CLIQUE with one vertex per literal occurrence. How many vertices does the clique graph have?" % (n, k), 3 * n, "3 vertices per clause.")


# =================== OS: fork simulator, synchronization ===================
OSP = "Processes, Threads & Syscalls"
OSS = "Synchronization"


def forks(prog):
    """Total number of fork() calls executed (= processes created) by `prog` (CPS interpreter)."""
    def ev(e, k):
        t = e[0]
        if t == "f":
            return 1 + k(True) + k(False)           # parent sees true, child sees false (0)
        if t == "and":
            return ev(e[1], lambda v: ev(e[2], k) if v else k(False))
        return ev(e[1], lambda v: k(True) if v else ev(e[2], k))

    def run(stmts, k):
        if not stmts: return k()
        s, rest = stmts[0], stmts[1:]
        if s[0] == "x": return ev(s[1], lambda v: run(rest, k))
        return ev(s[1], lambda v: (run(s[2] + rest, k) if v else run(rest, k)))
    return run(prog, lambda: 0)


def src(prog, ind=""):
    def es(e): return "fork()" if e[0] == "f" else "(%s %s %s)" % (es(e[1]), "&&" if e[0] == "and" else "||", es(e[2]))
    out = []
    for s in prog:
        if s[0] == "x": out.append(ind + es(s[1]) + ";")
        else: out.append(ind + "if (%s) {\n%s\n%s}" % (es(s[1]), src(s[2], ind + "    "), ind))
    return "\n".join(out)


def rexpr(r, d):
    if d == 0 or r.random() < 0.45: return ("f",)
    return (r.choice(["and", "or"]), rexpr(r, d - 1), rexpr(r, d - 1))


@gen(OS_ := "OS", OSP, "fork() with conditions", n=120, diff="hard", marks=2)
def os_fork_cond(r):
    prog = []
    for _ in range(r.randint(1, 3)):
        if r.random() < 0.4: prog.append(("if", rexpr(r, 1), [("x", ("f",))]))
        else: prog.append(("x", rexpr(r, 2)))
    f = forks(prog)
    if f > 40 or f < 1: raise Skip()
    return nat(r, "How many processes exist in total (including the original) after this C fragment completes? Evaluate && and || with short-circuiting.\n```c\n%s\n```" % src(prog), 1 + f,
               "Each fork() executed by any process adds one process; short-circuit evaluation decides which forks run in the child (returns 0) and in the parent. Total forks = %d." % f)


@gen("OS", OSP, "Overheads", n=60, diff="easy")
def os_over(r):
    q, s = r.choice([2, 4, 5, 10, 20]), r.choice([0.1, 0.2, 0.5, 1])
    kind = r.choice(["eff", "total", "threads", "ctx_total"])
    if kind == "eff": return nat(r, "Round-robin time quantum is %g ms and each context switch costs %g ms. CPU efficiency in percent for CPU-bound processes? (up to 2 decimals)" % (q, s), round(q / (q + s) * 100, 2), "q/(q + s).", tol=0.01)
    if kind == "total":
        n, b = r.randint(3, 8), r.choice([10, 20, 30, 40])
        sl = math.ceil(b / q)
        return nat(r, "%d CPU-bound processes each need %d ms. Quantum %g ms, context switch %g ms (counted after every slice including the last). Total elapsed time (ms)?" % (n, b, q, s), round(n * sl * (q if b % q == 0 else 0) + (n * (b) if b % q else 0) + n * sl * s, 2) if False else round(n * b + n * sl * s, 2), "Useful time n·b plus one switch per slice.", tol=0.01)
    if kind == "threads":
        t = r.randint(2, 8)
        return nat(r, "A process has %d threads sharing a code section of 40 KB, a heap and each thread has a 1 MB stack. Total stack memory in MB (all threads)?" % t, t, "One stack per thread.")
    n, sw = r.randint(100, 2000), r.choice([5, 10, 20])
    return nat(r, "A system performs %d context switches per second, each taking %d µs. Percentage of CPU time spent on switching? (up to 2 decimals)" % (n, sw), round(n * sw / 1e6 * 100, 2), "n·t/1s.", tol=0.01)


@gen("OS", OSS, "Semaphore counting", n=100, diff="medium")
def os_sync(r):
    kind = r.choice(["pc", "phil", "cs", "readers", "bakery", "mutex_count"])
    N = r.randint(4, 12)
    if kind == "pc":
        p, c = r.randint(N // 2, N + 3), r.randint(0, N // 2)
        return nat(r, "Bounded-buffer problem: empty = %d, full = 0, mutex = 1 initially. The producer has completed %d full iterations of (wait(empty); put; signal(full)) and the consumer %d iterations of (wait(full); get; signal(empty)) with no one blocked. What is the value of 'empty' now? (the buffer holds at most %d items)" % (N, min(p, N + c), c, N), N - min(p, N + c) + c, "empty = N − produced + consumed.")
    if kind == "phil":
        n = r.randint(3, 9)
        return nat(r, "In the dining-philosophers problem with %d philosophers and %d forks (each philosopher needs two adjacent forks), what is the maximum number of philosophers that can eat simultaneously?" % (n, n), n // 2, "⌊n/2⌋.")
    if kind == "cs":
        k, n = r.randint(2, 5), r.randint(6, 12)
        return nat(r, "A counting semaphore initialised to %d guards a resource pool. %d processes execute wait() before using the pool and none has released yet. How many are inside the pool?" % (k, n), k, "At most k enter; the rest block.")
    if kind == "readers":
        rd, wr = r.randint(2, 8), r.randint(1, 3)
        return nat(r, "In a readers–writers solution %d readers are reading. How many writers can write at the same time?" % rd, 0, "A writer needs exclusive access, so none can write while readers are active.")
    if kind == "bakery":
        n = r.randint(3, 8)
        return nat(r, "In Lamport's bakery algorithm %d processes want to enter the critical section. If they pick token numbers %s, which process (1-indexed) enters first? (smallest token wins; ties broken by lower process id)" % (n, (lambda t: t)(tk := [r.randint(1, 6) for _ in range(n)])), tk.index(min(tk)) + 1, "Lowest (token, id) pair.")
    n = r.randint(3, 10)
    return nat(r, "A binary semaphore (initial value 1) protects a critical section. %d processes each execute wait() and then signal() once, in any interleaving. What is the final value of the semaphore?" % n, 1, "Every wait is matched by a signal.")


# =================== DL: combinational ===================
DLC = "Combinational Circuits"


@gen("DL", DLC, "Adders & arithmetic circuits", n=110, diff="medium")
def dl_arith(r):
    kind = r.choice(["add", "sub", "ovf", "carry", "mult", "gate_delay", "xor_tree", "dec_or", "cmp"])
    n = r.choice([4, 5, 6, 8])
    a, b = r.randint(0, 2 ** n - 1), r.randint(0, 2 ** n - 1)
    if kind == "add": return nat(r, "A %d-bit adder adds %s and %s (unsigned). The %d-bit sum output, as a decimal, is" % (n, format(a, "0%db" % n), format(b, "0%db" % n), n), (a + b) % 2 ** n, "Sum modulo 2^%d (carry-out discarded)." % n)
    if kind == "carry": return nat(r, "A %d-bit adder adds %s and %s (unsigned). What is the carry-out (0 or 1)?" % (n, format(a, "0%db" % n), format(b, "0%db" % n)), int(a + b >= 2 ** n), "Carry-out = 1 iff the true sum needs n+1 bits.")
    if kind == "sub": return nat(r, "A %d-bit adder/subtractor computes A − B for A = %s, B = %s using two's complement (A + ~B + 1). The %d-bit result as an UNSIGNED decimal is" % (n, format(a, "0%db" % n), format(b, "0%db" % n), n), (a - b) % 2 ** n, "(A − B) mod 2^n.")
    if kind == "ovf":
        lo, hi = -2 ** (n - 1), 2 ** (n - 1) - 1
        x, y = r.randint(lo, hi), r.randint(lo, hi)
        return mcq(r, "Two's complement addition of %d and %d in %d bits sets the overflow flag?" % (x, y, n), "Yes" if not lo <= x + y <= hi else "No", ["No" if not lo <= x + y <= hi else "Yes", "Only if there is a carry out", "Only if the result is negative"], "The true sum %d is %s [%d, %d]." % (x + y, "outside" if not lo <= x + y <= hi else "inside", lo, hi))
    if kind == "mult":
        p, q = r.randint(2, 6), r.randint(2, 6)
        return nat(r, "Using an array multiplier built from AND gates and full adders, a %d-bit × %d-bit unsigned multiplier needs how many AND gates for the partial products?" % (p, q), p * q, "One AND per bit pair.")
    if kind == "gate_delay":
        d, k = r.choice([1, 2, 3]), r.randint(3, 8)
        return nat(r, "A balanced tree of 2-input AND gates computes the AND of %d inputs; each gate has a delay of %d ns. Worst-case delay in ns?" % (2 ** k, d), k * d, "Depth log₂N × gate delay.")
    if kind == "xor_tree": return nat(r, "Minimum number of 2-input XOR gates to build an %d-bit parity generator?" % (n + 4), n + 3, "n − 1 gates.")
    if kind == "dec_or":
        m = r.randint(2, 6)
        return nat(r, "A 3-to-8 decoder is used to implement a 3-variable function with %d minterms using one OR gate. How many inputs does the OR gate need?" % m, m, "One input per minterm output.")
    return nat(r, "A %d-bit magnitude comparator is built by cascading 1-bit comparators. How many 1-bit comparator stages are needed?" % n, n, "One per bit.")


@gen("DL", DLC, "SOP cost from minimisation", n=60, diff="hard", marks=2)
def dl_cost(r):
    from content.g_dl import analyse
    n = 4
    mt = sorted(r.sample(range(16), r.randint(5, 10)))
    pis, ess, best, glob = analyse(mt, n)
    terms = best[0]
    kind = r.choice(["gates", "inputs"])
    if kind == "gates": return nat(r, "F(A,B,C,D) = Σm(%s). Implemented in minimal two-level AND–OR form (complemented inputs available for free). How many gates (AND gates + the output OR gate) are needed? (a single-literal term needs no AND gate; count only gates with ≥ 2 inputs)" % ", ".join(map(str, mt)),
                                  sum(1 for p in best[2] if (4 - bin(p[1]).count("1")) >= 2) + (1 if terms >= 2 else 0), "Minimal cover: %d terms." % terms)
    return nat(r, "F(A,B,C,D) = Σm(%s). In the minimal sum-of-products form, what is the total number of literals?" % ", ".join(map(str, mt)), glob, "Exhaustive minimal cover.")


# =================== COA: I/O ===================
@gen("COA", "I/O, Interrupts & DMA", "DMA & interrupts", n=100, diff="medium", marks=2)
def io2(r):
    kind = r.choice(["dma_pct", "int_lat", "burst", "poll_dev", "bus", "intr_rate", "buf"])
    if kind == "dma_pct":
        rate, bus = r.choice([2, 5, 10, 20]), r.choice([100, 200, 400])
        return nat(r, "A device transfers data at %d MB/s through cycle-stealing DMA on a memory bus of %d MB/s. What fraction of the memory bandwidth (percent) does the device consume?" % (rate, bus), round(rate / bus * 100, 2), "rate / bus bandwidth.", tol=0.01)
    if kind == "int_lat":
        inst, f = r.choice([20, 40, 100]), r.choice([100, 500, 1000])
        return nat(r, "An interrupt handler executes %d instructions with CPI 2 on a %d MHz CPU, plus 10 µs of save/restore overhead. How long (µs) does one interrupt take to service? (up to 2 decimals)" % (inst, f), round(inst * 2 / f + 10, 2), "instr·CPI/f + overhead.", tol=0.01)
    if kind == "burst":
        w, c, tb = r.choice([256, 512, 1024]), r.choice([2, 4]), r.choice([10, 20])
        return nat(r, "DMA moves a block of %d words in burst mode. Each word needs %d bus cycles and the bus cycle is %d ns. Time the CPU is locked out of the bus in µs? (up to 2 decimals)" % (w, c, tb), round(w * c * tb / 1000, 2), "words × cycles × cycle time.", tol=0.01)
    if kind == "poll_dev":
        n, t = r.randint(2, 10), r.choice([10, 20, 50])
        return nat(r, "A CPU polls %d devices in turn; checking one device takes %d µs. Worst-case time (µs) before a ready device is noticed (full polling round)?" % (n, t), n * t, "n × t.")
    if kind == "bus":
        w, f = r.choice([16, 32, 64]), r.choice([100, 200, 500])
        return nat(r, "A synchronous bus is %d bits wide and runs at %d MHz with one transfer per cycle. Peak transfer rate in MB/s?" % (w, f), w // 8 * f, "bytes × frequency.")
    if kind == "intr_rate":
        d, b = r.choice([100, 500, 1000]), r.choice([1, 2, 4])
        return nat(r, "A device produces %d KB/s and interrupts the CPU once for every %d byte(s) it delivers (1 KB = 1000 B). Interrupts per second?" % (d, b), d * 1000 // b, "rate / bytes per interrupt.")
    return nat(r, "A printer buffer of %d KB is filled at 100 KB/s and drained at %d KB/s. Seconds until a full buffer is drained, if no more data arrives?" % (r.choice([200, 400]), 20), 0, "") if False else \
        (lambda B, d: nat(r, "A buffer holds %d KB and is drained at %d KB/s when no more data arrives. How many seconds to drain it completely?" % (B, d), B / d, "size / rate.", tol=0.01))(r.choice([200, 400, 800]), r.choice([20, 40, 50, 100]))


# =================== GA: vocabulary & usage banks ===================
GA, VB = "GA", "Verbal Ability"
SYN = [("abate", "subside"), ("aberrant", "deviant"), ("abstain", "refrain"), ("acumen", "insight"), ("adept", "skilful"), ("adversity", "hardship"), ("affable", "friendly"), ("alleviate", "relieve"),
       ("ambiguous", "unclear"), ("ameliorate", "improve"), ("arduous", "laborious"), ("austere", "stern"), ("banal", "trite"), ("belligerent", "hostile"), ("benign", "harmless"), ("blithe", "carefree"),
       ("brevity", "conciseness"), ("candour", "frankness"), ("capricious", "unpredictable"), ("cogent", "convincing"), ("complacent", "self-satisfied"), ("conspicuous", "noticeable"),
       ("copious", "abundant"), ("cursory", "hasty"), ("dearth", "scarcity"), ("diligent", "hardworking"), ("elated", "overjoyed"), ("eloquent", "articulate"), ("enigma", "puzzle"), ("fervent", "passionate"),
       ("frugal", "thrifty"), ("gregarious", "sociable"), ("haughty", "arrogant"), ("impeccable", "flawless"), ("indolent", "lazy"), ("inept", "clumsy"), ("lucid", "clear"), ("meticulous", "careful"),
       ("mundane", "ordinary"), ("novice", "beginner"), ("opulent", "luxurious"), ("pragmatic", "practical"), ("quaint", "charming"), ("reticent", "reserved"), ("scrutinise", "examine"), ("tenacious", "persistent"),
       ("tranquil", "peaceful"), ("ubiquitous", "omnipresent"), ("vivid", "bright"), ("zealous", "enthusiastic")]
ANT = [("abundant", "scarce"), ("ancient", "modern"), ("arrogant", "humble"), ("barren", "fertile"), ("brave", "cowardly"), ("brittle", "flexible"), ("cautious", "reckless"), ("coarse", "smooth"),
       ("conceal", "reveal"), ("diligent", "idle"), ("economical", "wasteful"), ("expand", "shrink"), ("fragile", "sturdy"), ("generous", "stingy"), ("genuine", "fake"), ("hostile", "friendly"),
       ("humble", "proud"), ("inferior", "superior"), ("lenient", "strict"), ("optimist", "pessimist"), ("permanent", "temporary"), ("rigid", "pliable"), ("scarce", "plentiful"), ("transparent", "opaque"),
       ("vague", "precise"), ("victory", "defeat"), ("zenith", "nadir"), ("ascend", "descend"), ("accept", "reject"), ("inflate", "deflate")]
ONE = [("a person who loves books", "bibliophile"), ("one who can speak two languages", "bilingual"), ("a government by the people", "democracy"), ("one who walks in sleep", "somnambulist"),
       ("a person who does not believe in God", "atheist"), ("study of birds", "ornithology"), ("one who eats human flesh", "cannibal"), ("a person who is present everywhere", "omnipresent"),
       ("incapable of being corrected", "incorrigible"), ("that which cannot be read", "illegible"), ("a place where birds are kept", "aviary"), ("one who knows everything", "omniscient"),
       ("a medicine that cures all diseases", "panacea"), ("a speech delivered without preparation", "extempore"), ("one who hates mankind", "misanthrope"), ("a person who is new to a field", "novice"),
       ("fear of heights", "acrophobia"), ("fear of open spaces", "agoraphobia"), ("the study of ancient societies from remains", "archaeology"), ("a rule of one person with absolute power", "autocracy")]
PREP = [("depend", "on"), ("good", "at"), ("interested", "in"), ("afraid", "of"), ("fond", "of"), ("capable", "of"), ("married", "to"), ("responsible", "for"), ("sensitive", "to"), ("aware", "of"),
        ("accuse someone", "of"), ("congratulate someone", "on"), ("prevent someone", "from"), ("rely", "on"), ("suffer", "from"), ("believe", "in"), ("ashamed", "of"), ("proud", "of"),
        ("jealous", "of"), ("superior", "to"), ("different", "from"), ("keen", "on"), ("insist", "on"), ("comply", "with")]
IDI = [("a piece of cake", "something very easy"), ("hit the nail on the head", "describe exactly what is causing a problem"), ("break the ice", "start a conversation in a tense setting"),
       ("let the cat out of the bag", "reveal a secret accidentally"), ("under the weather", "feeling slightly ill"), ("cost an arm and a leg", "be very expensive"),
       ("spill the beans", "reveal secret information"), ("the ball is in your court", "it is your turn to act"), ("beat around the bush", "avoid the main topic"),
       ("a dark horse", "a person with unexpected abilities"), ("add fuel to the fire", "make a bad situation worse"), ("call it a day", "stop working for now"), ("cut corners", "do something the cheap or easy way"),
       ("kill two birds with one stone", "achieve two goals with one action"), ("pull someone's leg", "joke with someone"), ("the last straw", "the final problem that makes a situation unbearable")]


def other(r, items, idx, k=3):
    pool = [x for i, x in enumerate(items) if i != idx]
    return r.sample(pool, k)


@gen(GA, VB, "Vocabulary", n=30, diff="medium")
def va_syn(r):
    i = r.randrange(len(SYN))
    w, s = SYN[i]
    return mcq(r, "Choose the word most nearly SIMILAR in meaning to '%s'." % w.upper(), s, [x[1] for x in other(r, SYN, i)], "%s means %s." % (w.capitalize(), s))


@gen(GA, VB, "Vocabulary", n=25, diff="medium")
def va_ant(r):
    i = r.randrange(len(ANT))
    w, a = ANT[i]
    wrong = [x[0] for x in other(r, ANT, i, 3)]
    return mcq(r, "Choose the word most nearly OPPOSITE in meaning to '%s'." % w.upper(), a, [x for x in wrong if x != w] + [w + "ly" if False else "similar"], "The antonym of %s is %s." % (w, a))


@gen(GA, VB, "One-word substitution", n=40, diff="easy")
def va_one(r):
    i = r.randrange(len(ONE))
    d, w = ONE[i]
    return mcq(r, "One word for: “%s”" % d, w, [x[1] for x in other(r, ONE, i)], "%s = %s." % (w.capitalize(), d))


@gen(GA, VB, "Prepositions", n=20, diff="easy")
def va_prep(r):
    i = r.randrange(len(PREP))
    w, p = PREP[i]
    wrong = [x for x in ["on", "at", "in", "of", "to", "for", "from", "with", "by"] if x != p]
    verb = w.split()[0] in ("depend", "rely", "suffer", "believe", "insist", "comply", "accuse", "congratulate", "prevent")
    q = ("She will %s ____ it." % w) if verb else ("He is %s ____ this matter." % w)
    return mcq(r, "Fill in the blank with the correct preposition: " + q, p, wrong, "The correct collocation is “%s %s”." % (w, p))


@gen(GA, VB, "Idioms", n=40, diff="medium")
def va_idiom(r):
    i = r.randrange(len(IDI))
    ph, m = IDI[i]
    return mcq(r, "What does the idiom “%s” mean?" % ph, m, [x[1] for x in other(r, IDI, i)], "“%s” means %s." % (ph, m))
