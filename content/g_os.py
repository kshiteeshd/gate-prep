"""Operating Systems — parametric generators (answers computed by simulation)."""
import math
from fractions import Fraction

from content.kit import *

S = "OS"
T_PROC, T_CPU, T_SYNC, T_DL, T_MEM, T_FS = ("Processes, Threads & Syscalls", "CPU Scheduling", "Synchronization",
                                           "Deadlocks", "Memory Management & Paging", "File Systems & Disk Scheduling")


def human(b):
    for u, d in (("GB", 2 ** 30), ("MB", 2 ** 20), ("KB", 2 ** 10)):
        if b >= d:
            v = b / d
            return ("%g" % round(v, 2)) + " " + u
    return "%d B" % b


# ---------- schedulers ----------
def sjf_np(procs):
    t, ct, rem = 0, {}, list(procs)
    while rem:
        av = [p for p in rem if p[1] <= t]
        if not av:
            t = min(p[1] for p in rem)
            continue
        p = min(av, key=lambda p: (p[2], p[1], p[0]))
        t += p[2]
        ct[p[0]] = t
        rem.remove(p)
    return ct


def srtf(procs):
    rem = {p[0]: p[2] for p in procs}
    at = {p[0]: p[1] for p in procs}
    t, ct = 0, {}
    while rem:
        av = [i for i in rem if at[i] <= t]
        if not av:
            t = min(at[i] for i in rem)
            continue
        i = min(av, key=lambda i: (rem[i], at[i], i))
        rem[i] -= 1
        t += 1
        if rem[i] == 0:
            ct[i] = t
            del rem[i]
    return ct


def rr(procs, q):
    procs = sorted(procs, key=lambda p: (p[1], p[0]))
    rem = {p[0]: p[2] for p in procs}
    n, t, i, ct, queue = len(procs), 0, 0, {}, []
    while i < n and procs[i][1] <= t:
        queue.append(procs[i][0]); i += 1
    while len(ct) < n:
        if not queue:
            t = procs[i][1]
            while i < n and procs[i][1] <= t:
                queue.append(procs[i][0]); i += 1
            continue
        p = queue.pop(0)
        run = min(q, rem[p])
        t += run
        rem[p] -= run
        while i < n and procs[i][1] <= t:
            queue.append(procs[i][0]); i += 1
        if rem[p] > 0:
            queue.append(p)
        else:
            ct[p] = t
    return ct


def table(procs, arrivals=True):
    head = "Process  Arrival  Burst\n" if arrivals else "Process  Burst\n"
    return "```\n" + head + "\n".join(("P%d       %-7d  %d" % (p[0], p[1], p[2])) if arrivals else ("P%d       %d" % (p[0], p[2])) for p in procs) + "\n```"


def mkprocs(r, n, maxat=6, maxbt=9):
    return [(i + 1, r.randint(0, maxat), r.randint(1, maxbt)) for i in range(n)]


def avg(vals):
    return Fraction(sum(vals), len(vals))


@gen(S, T_CPU, "FCFS", n=30, diff="easy")
def os_fcfs(r):
    n = r.randint(3, 5)
    bt = [r.randint(2, 12) for _ in range(n)]
    t, wt = 0, []
    for b in bt:
        wt.append(t); t += b
    v = avg(wt)
    ps = [(i + 1, 0, b) for i, b in enumerate(bt)]
    return nat(r, "Processes arrive at time 0 in the order P1, P2, … and are scheduled by FCFS.\n" + table(ps, False) +
               "\nWhat is the average waiting time? (up to 2 decimals)", round(float(v), 2),
               "Waiting times: %s → average = %s." % (wt, fmt(round(float(v), 2))), tol=0.01)


@gen(S, T_CPU, "SJF (non-preemptive)", n=40, diff="medium")
def os_sjf(r):
    ps = mkprocs(r, r.randint(4, 5))
    ct = sjf_np(ps)
    wt = [ct[p[0]] - p[1] - p[2] for p in ps]
    v = round(float(avg(wt)), 2)
    return mcq(r, "Non-preemptive SJF is used (ties: earlier arrival, then lower PID).\n" + table(ps) + "\nAverage waiting time is", v,
               near(r, v) + [round(v + 0.5, 2), round(v - 0.5, 2)],
               "Completion times %s; WT = CT − AT − BT = %s; average %s." % (dict(sorted(ct.items())), wt, fmt(v)))


@gen(S, T_CPU, "SRTF (preemptive SJF)", n=40, diff="hard", marks=2)
def os_srtf(r):
    ps = mkprocs(r, r.randint(4, 5), 5, 8)
    ct = srtf(ps)
    tat = [ct[p[0]] - p[1] for p in ps]
    v = round(float(avg(tat)), 2)
    return nat(r, "Shortest Remaining Time First (preemptive) scheduling is used. A running process is preempted only if a newly arrived process has strictly smaller remaining time.\n" +
               table(ps) + "\nAverage turnaround time = ? (up to 2 decimals)", v,
               "Completion times %s; TAT = CT − AT = %s; average = %s." % (dict(sorted(ct.items())), tat, fmt(v)), tol=0.01)


@gen(S, T_CPU, "Round Robin", n=45, diff="hard", marks=2)
def os_rr(r):
    ps = mkprocs(r, r.randint(3, 5), 5, 9)
    q = r.choice([2, 3, 4])
    ct = rr(ps, q)
    wt = [ct[p[0]] - p[1] - p[2] for p in ps]
    v = round(float(avg(wt)), 2)
    return nat(r, "Round Robin scheduling with time quantum %d. A newly arriving process is placed in the ready queue before a pre-empted process rejoins at the same instant.\n" % q +
               table(ps) + "\nAverage waiting time = ? (up to 2 decimals)", v,
               "Completion: %s → WT = CT − AT − BT = %s → average %s." % (dict(sorted(ct.items())), wt, fmt(v)), tol=0.01)


@gen(S, T_CPU, "Round Robin", n=25, diff="medium")
def os_rr_ctx(r):
    n, bt, q = r.randint(3, 6), r.randint(10, 40), r.choice([3, 4, 5, 6])
    bts = [r.randint(3, 20) for _ in range(n)]
    sw = sum(math.ceil(b / q) for b in bts) - 1
    return nat(r, "%d processes arrive at time 0 with CPU bursts %s ms. Round Robin with quantum %d ms is used. How many context switches occur, "
                  "if the switch at the very start and the one after the last process finishes are NOT counted?" % (n, bts, q), sw,
               "Each process needs ⌈burst/q⌉ slices; total slices = %d; switches = slices − 1 = %d." % (sw + 1, sw))


# ---------- memory ----------
def fifo(ref, k):
    fr, f = [], 0
    for x in ref:
        if x not in fr:
            f += 1
            if len(fr) == k:
                fr.pop(0)
            fr.append(x)
    return f


def lru(ref, k):
    fr, f = [], 0
    for x in ref:
        if x in fr:
            fr.remove(x)
        else:
            f += 1
            if len(fr) == k:
                fr.pop(0)
        fr.append(x)
    return f


def opt(ref, k):
    fr, f = [], 0
    for i, x in enumerate(ref):
        if x in fr:
            continue
        f += 1
        if len(fr) < k:
            fr.append(x)
        else:
            def nxt(p):
                return ref.index(p, i + 1) if p in ref[i + 1:] else 10 ** 9
            fr.remove(max(fr, key=nxt))
            fr.append(x)
    return f


def refstring(r, n=14, pages=6):
    return [r.randint(1, pages) for _ in range(n)]


@gen(S, T_MEM, "Page replacement", n=40, diff="easy")
def os_fifo(r):
    ref, k = refstring(r), r.choice([3, 4])
    v = fifo(ref, k)
    return nat(r, "Reference string: %s\nHow many page faults occur with FIFO replacement and %d frames (initially empty)?" % (" ".join(map(str, ref)), k), v,
               "Simulate FIFO: faults = %d." % v)


@gen(S, T_MEM, "Page replacement", n=40, diff="medium")
def os_lru(r):
    ref, k = refstring(r, 15, 7), r.choice([3, 4])
    v = lru(ref, k)
    return mcq(r, "Reference string: %s\nNumber of page faults under LRU with %d frames (initially empty) is" % (" ".join(map(str, ref)), k), v,
               near(r, v) + [fifo(ref, k), opt(ref, k)], "LRU simulation gives %d faults." % v)


@gen(S, T_MEM, "Page replacement", n=40, diff="hard", marks=2)
def os_opt(r):
    ref, k = refstring(r, 16, 7), r.choice([3, 4])
    a, b, c = fifo(ref, k), lru(ref, k), opt(ref, k)
    if len({a, b, c}) < 3:
        raise Skip()
    return nat(r, "Reference string: %s\nWith %d frames, let F, L, O be the page-fault counts for FIFO, LRU and Optimal replacement. Compute F + L + O." % (" ".join(map(str, ref)), k),
               a + b + c, "F = %d, L = %d, O = %d → sum %d." % (a, b, c, a + b + c))


@gen(S, T_MEM, "Page replacement", n=15, diff="hard", marks=2)
def os_belady(r):
    base = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    labels = r.sample(range(1, 10), 5)
    ref = [labels[x - 1] for x in base]
    if r.random() < 0.5:
        ref = ref + [labels[r.randrange(5)]] if False else ref
    f3, f4 = fifo(ref, 3), fifo(ref, 4)
    if f4 <= f3:
        raise Skip()
    return mcq(r, "For the reference string %s, FIFO page replacement is run with 3 frames and again with 4 frames. Which statement is correct?" % " ".join(map(str, ref)),
               "More faults with 4 frames (%d) than with 3 frames (%d) — Belady's anomaly" % (f4, f3),
               ["Fewer faults with 4 frames than with 3 frames", "Same number of faults in both cases", "Belady's anomaly cannot occur with FIFO"],
               "FIFO: 3 frames → %d faults, 4 frames → %d faults." % (f3, f4))


@gen(S, T_MEM, "Paging arithmetic", n=30, diff="easy")
def os_ptsize(r):
    v, p, e = r.choice([32, 36, 40]), r.choice([12, 13, 14]), r.choice([4, 8])
    size = 2 ** (v - p) * e / 2 ** 20
    return nat(r, "A system has a %d-bit virtual address space, page size 2^%d bytes and %d-byte page-table entries. Size of the single-level page table in MB?" % (v, p, e), size,
               "Entries = 2^%d; size = 2^%d × %d B = %s MB." % (v - p, v - p, e, fmt(size)))


@gen(S, T_MEM, "Multi-level paging", n=25, diff="hard", marks=2)
def os_levels(r):
    v, p, e = r.choice([40, 44, 48, 52]), r.choice([12, 13, 14]), r.choice([4, 8])
    per = (p - int(math.log2(e)))
    lv = math.ceil((v - p) / per)
    return nat(r, "A %d-bit virtual address uses pages of 2^%d bytes; each page-table entry is %d bytes and every page-table level must fit exactly in one page. "
                  "Minimum number of page-table levels required?" % (v, p, e), lv,
               "Index bits per level = %d − log2(%d) = %d. Bits to translate = %d − %d = %d → ⌈%d/%d⌉ = %d." % (p, e, per, v, p, v - p, v - p, per, lv))


@gen(S, T_MEM, "TLB / EAT", n=40, diff="medium")
def os_eat(r):
    h = r.choice([0.7, 0.8, 0.9, 0.95])
    m, t = r.choice([100, 120, 200]), r.choice([10, 20])
    v = h * (t + m) + (1 - h) * (t + 2 * m)
    return mcq(r, "In a single-level paging system the TLB lookup takes %d ns and a memory access takes %d ns. With TLB hit ratio %.2f, the effective memory access time (ns) is" % (t, m, h),
               round(v, 2), [round(h * m + (1 - h) * 2 * m, 2), round(v + t, 2), round(h * t + (1 - h) * 2 * m, 2), round(m * 2 - h * m, 2)],
               "EAT = h(t+m) + (1−h)(t+2m) = %.2f ns." % v)


@gen(S, T_MEM, "Demand paging", n=25, diff="medium")
def os_pf(r):
    m, s, p = r.choice([100, 200]), r.choice([5, 8, 10]) * 10 ** 6, r.choice([1 / 1000, 1 / 2000, 1 / 5000, 1 / 10000])
    v = (1 - p) * m + p * s
    return nat(r, "Memory access time is %d ns and servicing a page fault takes %d ms. If the page-fault rate is 1 in %d accesses, the effective access time in ns is? (up to 1 decimal)" % (m, s // 10 ** 6, round(1 / p)),
               round(v, 1), "EAT = (1−p)m + p·S = %.1f ns." % v, tol=0.1)


@gen(S, T_MEM, "Fragmentation", n=25, diff="easy")
def os_intfrag(r):
    ps, n = r.choice([2048, 4096, 1024, 512]), r.randint(3, 8)
    sizes = [r.randint(ps // 3, ps * 5) for _ in range(n)]
    fr = sum((ps - s % ps) % ps for s in sizes)
    return nat(r, "Page size is %d bytes. Processes of sizes %s bytes are loaded. Total internal fragmentation (bytes)?" % (ps, sizes), fr,
               "Per process internal fragmentation = (page − size mod page) mod page; total = %d." % fr)


@gen(S, T_MEM, "Contiguous allocation", n=40, diff="medium", marks=2)
def os_fit(r):
    holes = [r.choice([100, 150, 200, 250, 300, 350, 500]) for _ in range(5)]
    reqs = [r.choice([80, 120, 180, 220, 260, 300, 340]) for _ in range(4)]
    strat = r.choice(["first fit", "best fit", "worst fit"])
    h, ok = list(holes), 0
    for q in reqs:
        c = [i for i in range(len(h)) if h[i] >= q]
        if not c:
            continue
        i = c[0] if strat == "first fit" else (min(c, key=lambda i: (h[i], i)) if strat == "best fit" else max(c, key=lambda i: (h[i], -i)))
        h[i] -= q
        ok += 1
    return nat(r, "Free memory holes (in KB, in address order): %s. Processes requesting %s KB arrive in this order and are allocated using %s (the remainder of a hole stays as a smaller hole). "
                  "How many requests are satisfied?" % (holes, reqs, strat), ok, "Simulate %s: holes end as %s; satisfied = %d." % (strat, h, ok))


# ---------- disk / file systems ----------
def disk_fcfs(h, reqs):
    t = 0
    for x in reqs:
        t += abs(x - h); h = x
    return t


def disk_sstf(h, reqs):
    left, t = list(reqs), 0
    while left:
        x = min(left, key=lambda x: (abs(x - h), x))
        t += abs(x - h); h = x; left.remove(x)
    return t


def disk_scan(h, reqs, top):
    low = [x for x in reqs if x < h]
    return (top - h) + ((top - min(low)) if low else 0)


def disk_look(h, reqs):
    up = [x for x in reqs if x >= h]
    low = [x for x in reqs if x < h]
    if not up:
        return h - min(low)
    return (max(up) - h) + ((max(up) - min(low)) if low else 0)


@gen(S, T_FS, "Disk scheduling", n=40, diff="medium")
def os_disk(r):
    reqs = r.sample(range(5, 195), r.randint(5, 7))
    h = r.randint(40, 120)
    alg = r.choice(["FCFS", "SSTF", "SCAN", "LOOK"])
    fn = {"FCFS": lambda: disk_fcfs(h, reqs), "SSTF": lambda: disk_sstf(h, reqs), "SCAN": lambda: disk_scan(h, reqs, 199), "LOOK": lambda: disk_look(h, reqs)}[alg]
    v = fn()
    note = {"SCAN": " SCAN moves towards higher cylinders first, goes up to the last cylinder (199), then reverses.", "LOOK": " LOOK moves towards higher cylinders first, up to the largest request, then reverses.", "FCFS": "", "SSTF": ""}[alg]
    return nat(r, "A disk has cylinders 0–199. The head is at cylinder %d. Pending requests: %s. Using %s, total head movement (in cylinders)?%s" % (h, reqs, alg, note), v,
               "Compute head movement for %s = %d." % (alg, v))


@gen(S, T_FS, "Disk access time", n=30, diff="medium", marks=2)
def os_disktime(r):
    rpm, seek, spt, k = r.choice([5400, 7200, 10000, 15000]), r.choice([4, 6, 8, 10]), r.choice([100, 200, 400]), r.choice([1, 2, 4, 5])
    rot = 60000 / rpm
    tot = seek + rot / 2 + rot * k / spt
    return nat(r, "A disk rotates at %d RPM with %d sectors per track. Average seek time is %d ms. Using average rotational latency, time (ms) to read %d consecutive sectors on one track? (up to 2 decimals)" % (rpm, spt, seek, k),
               round(tot, 2), "Rotation = %.3f ms; latency = %.3f; transfer = k·rot/spt = %.3f; total = %.2f ms." % (rot, rot / 2, rot * k / spt, tot), tol=0.02)


@gen(S, T_FS, "Inodes", n=30, diff="hard", marks=2)
def os_inode(r):
    B, P, D = r.choice([1024, 2048, 4096]), r.choice([4, 8]), r.choice([10, 12])
    n = B // P
    full = (D + n + n ** 2 + n ** 3) * B
    wrong = [(D + n + n ** 2) * B, (n + n ** 2 + n ** 3) * B, (D + n + n ** 2 + n ** 3) * B + B, D * B + n * B]
    kb = lambda b: "%d KB" % (b // 1024)
    return mcq(r, "A Unix-like file system has block size %d B, disk-block pointers of %d B, and each inode has %d direct pointers plus one single-, one double- and one triple-indirect pointer. "
                  "Maximum file size supported is" % (B, P, D), kb(full), [kb(w) for w in wrong],
               "Pointers per block n = %d. Blocks = %d + n + n² + n³ = %d → size = %s (%s)." % (n, D, D + n + n ** 2 + n ** 3, kb(full), human(full)))


# ---------- deadlocks ----------
def safe_single(avail, mx, al):
    need = [m - a for m, a in zip(mx, al)]
    done, seq, prog = [False] * len(mx), [], True
    while prog:
        prog = False
        for i in range(len(mx)):
            if not done[i] and need[i] <= avail:
                avail += al[i]; done[i] = True; seq.append(i + 1); prog = True
    return all(done), seq


@gen(S, T_DL, "Banker's algorithm", n=45, diff="medium")
def os_banker(r):
    n = r.randint(3, 4)
    mx = [r.randint(4, 10) for _ in range(n)]
    al = [r.randint(1, m - 1) for m in mx]
    tot = sum(al) + r.randint(0, 3)
    avail = tot - sum(al)
    ok, seq = safe_single(avail, mx, al)
    rows = "\n".join("P%d      %-6d %d" % (i + 1, al[i], mx[i]) for i in range(n))
    return mcq(r, "A single resource type has %d units in total. Current state:\n```\nProcess Alloc  Max\n%s\n```\nAvailable = %d. The system is" % (tot, rows, avail),
               "in a safe state" if ok else "in an unsafe state",
               ["in an unsafe state" if ok else "in a safe state", "already deadlocked, with all processes blocked",
                "not analysable without the Need matrix", "safe only if processes request in index order"],
               ("Safe sequence: " + " → ".join("P%d" % s for s in seq)) if ok else "No process can ever be completed in an order that releases enough resources: unsafe.")


@gen(S, T_DL, "Banker's algorithm", n=30, diff="hard", marks=2)
def os_banker_min(r):
    n = r.randint(3, 4)
    mx = [r.randint(5, 11) for _ in range(n)]
    al = [r.randint(1, m - 2) for m in mx]
    for a in range(0, 40):
        if safe_single(a, mx, al)[0]:
            break
    return nat(r, "%d processes hold %s units of a single resource and have declared maximum needs %s. What is the minimum number of free units that makes the state safe?" % (n, al, mx), a,
               "Try Available = 0,1,2,…; the smallest value that yields a complete safe sequence is %d." % a)


@gen(S, T_DL, "Deadlock-free resource count", n=25, diff="easy")
def os_dlmin(r):
    n, m = r.randint(3, 9), r.randint(2, 6)
    v = n * (m - 1) + 1
    return nat(r, "%d processes each need at most %d units of an identical resource, requesting one unit at a time. Minimum total units that guarantee deadlock-freedom?" % (n, m), v,
               "Worst case each holds m−1 = %d; one more unit guarantees someone finishes: n(m−1)+1 = %d." % (m - 1, v))


@gen(S, T_DL, "Deadlock-free resource count", n=20, diff="medium")
def os_dlmax(r):
    m, R = r.randint(2, 5), r.randint(10, 30)
    n = (R - 1) // (m - 1)
    return nat(r, "A system has %d identical resource units. Each process needs at most %d units. What is the maximum number of processes that can run with no possibility of deadlock?" % (R, m), n,
               "Need n(m−1)+1 ≤ R → n ≤ (R−1)/(m−1) = %d." % n)


# ---------- synchronization ----------
@gen(S, T_SYNC, "Semaphores", n=35, diff="easy")
def os_sem(r):
    s, x, y = r.randint(2, 12), r.randint(3, 15), r.randint(1, 10)
    v = s - x + y
    return nat(r, "A counting semaphore is initialised to %d. Then %d wait (P) and %d signal (V) operations complete (classic implementation in which the value can go negative). Final value of the semaphore?" % (s, x, y), v,
               "Value = %d − %d + %d = %d (negative ⇒ that many blocked processes)." % (s, x, y, v))


@gen(S, T_SYNC, "Semaphores", n=25, diff="medium")
def os_sem2(r):
    k, n = r.randint(2, 5), r.randint(6, 12)
    return nat(r, "A binary-semaphore-protected resource is replaced by a counting semaphore initialised to %d. %d processes execute wait() once, none execute signal(). How many processes are blocked?" % (k, n), n - k,
               "%d acquire it; the remaining %d − %d = %d block." % (k, n, k, n - k))


# ---------- processes ----------
@gen(S, T_PROC, "fork()", n=30, diff="easy")
def os_fork(r):
    n = r.randint(2, 7)
    style = r.choice(["seq", "loop"])
    code = ("fork();\n" * n) if style == "seq" else "for (i = 0; i < %d; i++)\n    fork();" % n
    return nat(r, "How many processes (including the original one) exist after the following C program fragment finishes?\n```c\n%s\n```" % code, 2 ** n,
               "Every fork() doubles the number of processes: 2^%d = %d." % (n, 2 ** n))


@gen(S, T_PROC, "fork()", n=20, diff="medium")
def os_fork2(r):
    n = r.randint(2, 8)
    return nat(r, "How many child processes are created in total (the original is not counted)?\n```c\nfor (i = 0; i < %d; i++) {\n    if (fork() == 0)\n        break;\n}\n```" % n, n,
               "A child breaks out of the loop immediately, so only the parent keeps forking: n = %d children." % n)


@gen(S, T_PROC, "fork()", n=25, diff="hard", marks=2)
def os_fork3(r):
    n = r.randint(2, 6)
    return nat(r, "How many times is \"X\" printed (assume stdout is unbuffered)?\n```c\nint main() {\n    int i;\n    for (i = 0; i < %d; i++)\n        fork();\n    printf(\"X\");\n    return 0;\n}\n```" % n, 2 ** n,
               "There are 2^%d processes at the end and each prints once." % n)
