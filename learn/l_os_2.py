"""OS part 2: deadlocks, memory management, virtual memory, file systems & disks."""
import math

from content import g_os as O
from learn import Ex, lesson

S = "OS"


def banker(alloc, mx, avail):
    n, m = len(alloc), len(avail)
    need = [[mx[i][j] - alloc[i][j] for j in range(m)] for i in range(n)]
    work, fin, seq = list(avail), [False] * n, []
    while True:
        for i in range(n):
            if not fin[i] and all(need[i][j] <= work[j] for j in range(m)):
                fin[i] = True
                seq.append(i)
                work = [work[j] + alloc[i][j] for j in range(m)]
                break
        else:
            break
    return need, all(fin), seq


def min_res_no_deadlock(n, k):
    """smallest R such that n processes each needing at most k units can never deadlock (brute-force check of worst state)"""
    for R in range(1, n * k + 2):
        # worst case: every process holds k-1 units; deadlock possible iff all of them are blocked with no free unit
        worst_held = n * (k - 1)
        if R > worst_held:
            return R
    return n * k


def fit(parts, procs, how):
    parts, placed = list(parts), []
    for p in procs:
        cand = [i for i, s in enumerate(parts) if s >= p]
        if not cand:
            placed.append(None)
            continue
        if how == "first":
            i = cand[0]
        elif how == "best":
            i = min(cand, key=lambda i: parts[i])
        else:
            i = max(cand, key=lambda i: parts[i])
        placed.append(parts[i])
        parts[i] -= p
    return placed


# ======================================================================================================
lesson(subject=S, chapter="Deadlocks", ch_no=3, no=1, slug="os-deadlocks", title="Deadlocks: Conditions, Detection & Banker's Algorithm",
       topic="Deadlocks", minutes=22, weight=5, widget="banker",
       widget_hint="Enter the Allocation and Max matrices and the Available vector; the tool computes Need, checks safety and lists a safe sequence. Test whether a request can be granted.",
       key="A deadlock is a set of processes each waiting for a resource held by another in the set. It needs four simultaneous conditions; the OS can prevent, avoid (Banker's algorithm), detect-and-recover, or ignore it. Banker's algorithm keeps the system in a safe state.",
       analogy=("🚗", "Gridlock at a crossroads", "Four cars enter an intersection together; each occupies one lane and needs the lane in front, which another car holds. Nobody can move and nobody will back up. Removing any one of the four conditions — shared lanes, hold-and-wait, no pre-emption, circular wait — would break the gridlock."),
       sections=[
           dict(h="The four necessary conditions (Coffman)", md="""A deadlock can occur only if **all four** hold at the same time:

1. **Mutual exclusion** — some resource is non-shareable.
2. **Hold and wait** — a process holds resources while waiting for others.
3. **No pre-emption** — resources can only be released voluntarily.
4. **Circular wait** — a cycle P₁ → P₂ → … → P₁ in which each waits for a resource held by the next.

**Prevention** negates one condition: acquire all resources at once (hold-and-wait), allow pre-emption, or impose a **total ordering** on resource types and request in increasing order (circular wait). Mutual exclusion cannot usually be removed."""),
           dict(h="Resource-allocation graph", md="""Nodes: processes and resources (with instance dots). Edges: request P → R, assignment R → P.

- No cycle ⇒ **no deadlock**.
- Cycle with **single-instance** resources ⇒ **deadlock**.
- Cycle with **multiple instances** ⇒ *possible* deadlock (not certain).

Detection for multi-instance resources uses an algorithm like Banker's on the *current* requests; for single instances it is a **cycle search in the wait-for graph** (O(n²))."""),
           dict(h="Safe state and the Banker's algorithm", md="""A state is **safe** if there is an order (a **safe sequence**) in which every process can run to completion using the available resources plus those released by earlier processes. Unsafe ⇏ deadlock, but **deadlock ⇒ unsafe**; a safe state never deadlocks.

For n processes and m resource types: **Allocation**, **Max**, **Need = Max − Allocation**, **Available**.

**Safety algorithm:** Work = Available, Finish all false. Find i with Finish[i] = false and Need[i] ≤ Work; set Work += Allocation[i], Finish[i] = true; repeat. If all can finish, the state is safe.

**Resource-request algorithm** for Pᵢ requesting Request: check Request ≤ Need[i] and ≤ Available, pretend to grant, then run the safety check; grant only if the resulting state is safe.""",
                formulas=[("Need = Max − Allocation", "per process, per resource")],
                call=[("tip", "Safe sequences are not unique", "Any order that works is a safe sequence. If a question asks for 'the' sequence it normally means the first one found by scanning processes in index order.")]),
           dict(h="Counting problems and recovery", md="""**Minimum resources that guarantee no deadlock:** n processes each needing at most k units of a single resource type. The worst case is every process holding k − 1 units and waiting for one more, so deadlock is impossible whenever the total R satisfies **R ≥ n(k − 1) + 1**.

**Recovery** from deadlock: terminate all deadlocked processes or one at a time (choose a victim by priority, progress, resources held), or pre-empt resources with rollback — watch for starvation of the victim."""),
       ],
       examples=[
           Ex("Safe sequence", "Allocation = P0(0,1,0) P1(2,0,0) P2(3,0,2) P3(2,1,1) P4(0,0,2); Max = P0(7,5,3) P1(3,2,2) P2(9,0,2) P3(2,2,2) P4(4,3,3); Available = (3,3,2). Is the state safe? Give the first safe sequence found scanning from P0.",
              ["Need = Max − Allocation: P0(7,4,3) P1(1,2,2) P2(6,0,0) P3(0,1,1) P4(4,3,1).", "Work (3,3,2): P0 no; P1 (1,2,2) fits ⇒ Work (5,3,2). Scan again: P0 no, P2 no, P3 fits ⇒ Work (7,4,3). Then P0 fits ⇒ (7,5,3); P2 fits ⇒ (10,5,5); P4 fits.", "Safe sequence: **P1, P3, P0, P2, P4**."],
              "Safe: **P1, P3, P0, P2, P4**.", verify=lambda: "Safe: " + ", ".join("P%d" % i for i in banker([[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]], [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]], [3, 3, 2])[2])),
           Ex("Minimum resources", "Four processes each need at most 3 units of a single resource type. What is the minimum number of units that makes deadlock impossible?",
              ["Worst case: each holds 2 units (= k − 1) and waits for the third: 4 × 2 = 8 units are in use.", "With 8 units all four may be stuck; with **9** one process can always finish."],
              "**9** units.", verify=lambda: str(min_res_no_deadlock(4, 3))),
           Ex("Granting a request", "In the previous system P1 requests (1,0,2). Can it be granted?",
              ["Request (1,0,2) ≤ Need[P1] (1,2,2) and ≤ Available (3,3,2). Pretend to grant: Available (2,3,0), Allocation[P1] = (3,0,2), Need[P1] = (0,2,0).", "Run the safety algorithm: P1 can finish (Need (0,2,0) ≤ (2,3,0)) ⇒ (5,3,2); the rest follow as before ⇒ safe, so the request **can** be granted."],
              "**Yes**, it is granted.", verify=lambda: "Yes" if banker([[0, 1, 0], [3, 0, 2], [3, 0, 2], [2, 1, 1], [0, 0, 2]], [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]], [2, 3, 0])[1] else "No"),
       ],
       traps=[("Cycle ≠ deadlock", "With multiple resource instances a cycle only signals possible deadlock."),
              ("Unsafe ≠ deadlocked", "An unsafe state may still avoid deadlock, but deadlocked states are always unsafe."),
              ("Need vs Max", "Compare Need (= Max − Allocation) with Work, not Max."),
              ("Prevent mutual exclusion?", "Cannot be removed for non-shareable resources like printers.")],
       quick=[("A state with a deadlock is always", ["safe", "unsafe", "reachable only by Banker's", "none"], 1, "Deadlock ⇒ unsafe."),
              ("Ordering resource types and requesting in order breaks", ["mutual exclusion", "hold and wait", "no pre-emption", "circular wait"], 3, "Ordering prevents cycles."),
              ("Banker's algorithm is a", ["prevention", "avoidance", "detection", "recovery"], 1, "It avoids unsafe states."),
              ("Need matrix equals", ["Allocation + Max", "Max − Allocation", "Available − Max", "Allocation"], 1, "Remaining demand.")],
       summary=["Coffman: mutual exclusion, hold-and-wait, no pre-emption, circular wait — all four needed.", "RAG: no cycle ⇒ no deadlock; single-instance cycle ⇒ deadlock; multi-instance cycle ⇒ maybe.", "Safe state: a safe sequence exists; deadlock ⇒ unsafe.",
                "Need = Max − Allocation; safety algorithm with Work/Finish.", "Minimum resources for deadlock freedom: n(k−1) + 1.", "Recovery: terminate or pre-empt victims; avoid starvation."])


# ======================================================================================================
lesson(subject=S, chapter="Memory Management", ch_no=4, no=1, slug="os-memory-paging", title="Memory Management, Paging & Address Translation",
       topic="Memory Management & Paging", minutes=24, weight=6, widget="addr",
       widget_hint="Choose the virtual-address size, page size and page-table entry size to see the address split, the page-table size, the number of levels and the effective access time with a TLB.",
       key="Memory management gives each process an isolated address space. Paging divides memory into fixed-size frames, eliminating external fragmentation; the page table maps pages to frames, multi-level tables keep it small and the TLB makes translation fast.",
       analogy=("🏨", "Hotel rooms and a guest directory", "A guest only knows their room number within their floor plan (the virtual page). The front desk (page table) knows the real room (frame) they were given, and a small cheat-sheet at the desk (TLB) remembers recent guests so lookups are instant."),
       sections=[
           dict(h="Contiguous allocation and fragmentation", md="""With **variable partitions**, free memory splits into holes:

- **First fit:** first hole big enough (fast). **Best fit:** smallest hole that fits (leaves tiny slivers). **Worst fit:** largest hole (leaves usable remainders but wastes big blocks). First and best fit are usually better than worst fit.
- **External fragmentation:** free memory exists but not contiguously; fixed by **compaction** or paging. **Internal fragmentation:** waste *inside* an allocated block (fixed partitions, last page).

**Logical (virtual) address** is generated by the CPU, **physical address** is what the memory sees; the MMU translates. **Base + limit registers** implement protection in contiguous schemes."""),
           dict(h="Paging", md="""Logical memory is divided into **pages**, physical memory into **frames** of the same size (a power of two). A logical address splits into **page number p** and **offset d**; the **page table** maps p to a frame f, and the physical address is (f, d).

- Address bits: VA = p + d bits, with d = log₂(page size); number of pages = 2^(VA − d).
- **Page-table size** = (#pages) × (PTE size). PTE holds frame number plus valid, protection, reference and dirty bits.
- **Internal fragmentation** averages half a page per process.
- Shared pages (read-only code) are possible by mapping the same frame.

**Inverted page table:** one entry per physical frame, searched by hash; saves space but makes lookup harder.""",
                formulas=[("page-table size = 2^(VA − log₂ page) × PTE size", "single level"),
                          ("levels = ⌈(VA − offset bits) / bits per level⌉", "bits per level = log₂(page size / PTE size)")]),
           dict(h="Multi-level paging and the TLB", md="""A single-level table for a 48-bit address is far too large, so the page table is itself paged (**two-level, four-level**). Each level should fit in **one page**: with page size P and PTE size e, one level indexes log₂(P / e) bits. Each extra level adds a memory access on a TLB miss.

The **TLB** caches recent page→frame translations. With hit ratio h, TLB lookup time t and memory time m, single-level paging:

    EAT = h·(t + m) + (1 − h)·(t + 2m)

For k-level paging replace the miss term by t + (k + 1)·m. If the TLB is searched in parallel with nothing else, t is added in both cases (as above).""",
                call=[("tip", "Read the wording", "Some questions ignore the TLB lookup time (t = 0) or give the 'cache hit' differently; always take the formula from the data stated.")]),
           dict(h="Segmentation and swapping", md="""**Segmentation** divides the address space into logical units (code, stack, heap); an address is (segment, offset) checked against the segment's limit; it has external fragmentation but no internal. **Segmented paging** pages each segment (e.g. x86).

**Swapping** moves whole processes between memory and a backing store; the degree of multiprogramming can exceed physical memory but swap time is dominated by transfer time of the process size."""),
       ],
       examples=[
           Ex("Single-level page-table size", "A system has a 32-bit virtual address, 4 KB pages and 4-byte page-table entries. What is the size of the single-level page table?",
              ["Offset = log₂(4096) = 12 bits ⇒ page number = 32 − 12 = 20 bits ⇒ 2²⁰ entries.", "Size = 2²⁰ × 4 B = 4 MB."],
              "**4 MB**", verify=lambda: "%d MB" % (2 ** 20 * 4 // 2 ** 20)),
           Ex("Number of levels", "A 48-bit virtual address uses 8 KB pages and 8-byte page-table entries; every page-table level must fit exactly in one page. How many levels are needed?",
              ["Offset = 13 bits; page number = 48 − 13 = 35 bits.", "One page holds 8192 / 8 = 1024 entries ⇒ 10 index bits per level ⇒ ⌈35 / 10⌉ = **4** levels."],
              "**4** levels.", verify=lambda: str(math.ceil((48 - 13) / int(math.log2(8192 // 8))))),
           Ex("Effective access time", "TLB lookup 20 ns, memory access 100 ns, TLB hit ratio 90 %, single-level paging. Compute the effective memory access time.",
              ["Hit: 20 + 100 = 120 ns. Miss: 20 + 100 (page table) + 100 (data) = 220 ns.", "EAT = 0.9 × 120 + 0.1 × 220 = 108 + 22 = **130 ns**."],
              "**130 ns**", verify=lambda: "%g ns" % (0.9 * 120 + 0.1 * 220)),
           Ex("Fit strategies", "Holes of 100, 500, 200, 300 and 600 KB (in order) must serve requests of 212, 417, 112 and 426 KB. Which requests can be satisfied with first fit and with best fit?",
              ["First fit: 212 → 500 (leaves 288); 417 → 600 (leaves 183); 112 → 288 (the 500 hole's remainder); 426 → no hole ≥ 426 left ⇒ fails.", "Best fit: 212 → 300; 417 → 500; 112 → 200; 426 → 600 ⇒ all four are placed."],
              "First fit places **3** of 4; best fit places **all 4**.", verify=lambda: "First fit places %d of 4; best fit places all %d" % (sum(1 for x in fit([100, 500, 200, 300, 600], [212, 417, 112, 426], "first") if x), sum(1 for x in fit([100, 500, 200, 300, 600], [212, 417, 112, 426], "best") if x))),
           Ex("Internal fragmentation", "A process of 72,766 bytes is placed in 2,048-byte pages. How many pages are needed and how much internal fragmentation results?",
              ["72,766 / 2,048 = 35.53, so 36 pages are needed.", "Allocated 36 × 2,048 = 73,728 bytes ⇒ fragmentation = 73,728 − 72,766 = **962** bytes."],
              "**36** pages, **962** bytes.", verify=lambda: "%d pages, %d bytes" % (math.ceil(72766 / 2048), math.ceil(72766 / 2048) * 2048 - 72766)),
       ],
       traps=[("Page-table level sizing", "Bits per level are log₂(page size / PTE size), not log₂(page size)."),
              ("External vs internal fragmentation", "Paging removes external fragmentation but adds internal fragmentation."),
              ("EAT with TLB", "A TLB miss costs an extra memory access per page-table level."),
              ("Frames vs pages", "Page size = frame size; the number of frames depends on physical memory, the number of pages on the virtual address space.")],
       quick=[("Paging eliminates", ["internal fragmentation", "external fragmentation", "both", "neither"], 1, "Only external."),
              ("Offset bits for a 4 KB page", ["10", "11", "12", "13"], 2, "log₂4096 = 12."),
              ("Which strategy leaves the smallest leftover hole?", ["first fit", "best fit", "worst fit", "next fit"], 1, "Best fit."),
              ("A TLB stores", ["page→frame translations", "disk blocks", "instructions", "interrupt vectors"], 0, "Translation cache.")],
       summary=["First/best/worst fit; external fragmentation (compaction) vs internal fragmentation (waste inside a block).", "Address = page number + offset; page-table size = #pages × PTE size.", "Levels: ⌈(VA − offset)/ log₂(P/e)⌉; each level fits in a page.",
                "EAT = h(t+m) + (1−h)(t+2m) for single level.", "Segmentation: logical units, external fragmentation; swapping moves whole processes.", "Inverted page table: one entry per frame."])


# ======================================================================================================
lesson(subject=S, chapter="Memory Management", ch_no=4, no=2, slug="os-virtual-memory", title="Virtual Memory & Page Replacement",
       topic="Memory Management & Paging", minutes=24, weight=6, widget="pagerep",
       widget_hint="Enter a page-reference string and the number of frames, then compare FIFO, LRU and Optimal. Try the Belady string 1 2 3 4 1 2 5 1 2 3 4 5 with 3 and then 4 frames.",
       key="Virtual memory lets a process run with only some of its pages in RAM. A page fault loads a missing page on demand; when frames are full a replacement algorithm (FIFO, LRU, Optimal) chooses a victim. Too little memory causes thrashing.",
       analogy=("🧳", "A small desk and a big filing cabinet", "Your desk holds only a few documents (frames); the rest are in the cabinet (disk). When you need one that isn't on the desk you fetch it — slow! — and must put one back. A good replacement policy puts back the document you're least likely to need soon."),
       sections=[
           dict(h="Demand paging and page faults", md="""In **demand paging** a page is brought in only when referenced. If its valid bit is 0, the hardware raises a **page fault**: the OS finds a free frame (or replaces one), reads the page from disk, updates the page table, and restarts the instruction.

**Effective access time** with fault probability p, memory access m and page-fault service time s:

    EAT = (1 − p)·m + p·s

Because s (milliseconds) ≫ m (nanoseconds), even tiny p dominates. **Locality of reference** (temporal and spatial) is why demand paging works. A **dirty bit** avoids writing back unmodified pages.""",
                formulas=[("EAT = (1 − p)·m + p·s", "demand paging")]),
           dict(h="Page replacement algorithms", md="""| Algorithm | Victim | Notes |
|---|---|---|
| **FIFO** | oldest loaded page | simple; suffers **Belady's anomaly** |
| **Optimal (OPT)** | page used farthest in the future | minimum faults, not implementable; benchmark |
| **LRU** | least recently used page | good approximation of OPT; **stack algorithm** |
| **Clock / second chance** | FIFO with a reference bit | cheap LRU approximation |
| **LFU / MFU** | least / most frequently used | counting-based |

**Belady's anomaly:** with FIFO, more frames can cause *more* faults (reference string 1 2 3 4 1 2 5 1 2 3 4 5: 9 faults with 3 frames, 10 with 4). **Stack algorithms** (OPT, LRU) never show it. Count every first reference as a fault; "faults" often exclude nothing — read whether initial faults count.""",
                call=[("trap", "Counting hits correctly", "Track the frame contents after each reference. For LRU update recency on every hit, for FIFO a hit does NOT change the order.")]),
           dict(h="Frame allocation, thrashing and working set", md="""- **Allocation:** equal, proportional to process size, or priority based. **Global** replacement takes frames from any process; **local** only from the faulting process's own frames.
- **Thrashing:** the system spends most of its time paging because processes lack enough frames — CPU utilisation collapses as the degree of multiprogramming rises. Cure: reduce multiprogramming, or use the **working-set model** (WS = pages referenced in the last Δ references) / page-fault-frequency control.
- **Minimum frames** per process is set by the instruction set (maximum pages one instruction touches)."""),
           dict(h="Other virtual-memory concepts", md="""- **Copy-on-write:** parent and child share pages until one writes.
- **Memory-mapped files** map a file into the address space.
- **Page size trade-off:** large pages reduce page-table size and increase TLB reach but increase internal fragmentation and transfer time per fault; small pages do the opposite. The optimal size is about √(2 · s · e) for average process size s and entry size e.
- **Kernel memory:** buddy system (power-of-two blocks, easy coalescing) and slab allocation."""),
       ],
       examples=[
           Ex("Faults for the textbook string", "Reference string 7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1 with 3 frames. How many page faults under FIFO, LRU and OPT?",
              ["Simulate each algorithm, tracking frame contents (all initial loads are faults).", "FIFO: 15 faults, LRU: 12 faults, OPT: 9 faults — the well-known textbook figures."],
              "FIFO **15**, LRU **12**, OPT **9**.", verify=lambda: "FIFO %d, LRU %d, OPT %d" % (O.fifo([7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1], 3), O.lru([7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1], 3), O.opt([7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1], 3))),
           Ex("Belady's anomaly", "Reference string 1 2 3 4 1 2 5 1 2 3 4 5 under FIFO: how many faults with 3 frames and with 4 frames?",
              ["3 frames: 9 faults. 4 frames: 10 faults.", "More frames gave **more** faults: the anomaly."],
              "3 frames **9**, 4 frames **10**.", verify=lambda: "3 frames %d, 4 frames %d" % (O.fifo([1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3), O.fifo([1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 4))),
           Ex("Effective access time with faults", "Memory access time is 200 ns, a page fault takes 8 ms (8,000,000 ns) and the page-fault rate is 1 in 1000 references. Compute the EAT.",
              ["EAT = (1 − p)·200 + p·8,000,000 with p = 0.001.", "= 199.8 + 8000 = **8199.8 ns** — about 41 times slower than no faults."],
              "**8199.8 ns**", verify=lambda: "%.1f ns" % ((1 - 0.001) * 200 + 0.001 * 8_000_000)),
           Ex("Required fault rate", "With the same timings, what page-fault rate keeps the EAT below 220 ns (10 % slowdown)?",
              ["EAT = 200 + p(8,000,000 − 200) < 220 ⇒ p < 20 / 7,999,800.", "p < about 2.5 × 10⁻⁶ ⇒ fewer than **1 fault in 400,000** accesses."],
              "p < **2.5 × 10⁻⁶**", verify=lambda: "p < %.1f × 10⁻⁶" % (20 / 7_999_800 * 1e6)),
       ],
       traps=[("FIFO hits don't reorder", "A page hit under FIFO does not change its position; under LRU it moves to most-recent."),
              ("Belady's anomaly", "Only FIFO-like algorithms; LRU and OPT are stack algorithms and immune."),
              ("Count the initial faults", "Unless stated otherwise every first reference is a page fault."),
              ("Thrashing", "More multiprogramming past a point lowers CPU utilisation.")],
       quick=[("Which algorithm gives the minimum page faults?", ["FIFO", "LRU", "OPT", "Clock"], 2, "Optimal."),
              ("Belady's anomaly can occur with", ["LRU", "OPT", "FIFO", "all stack algorithms"], 2, "FIFO."),
              ("Thrashing is caused by", ["too many frames", "too little memory for the working sets", "large pages", "TLB hits"], 1, "Constant paging."),
              ("A dirty bit tells the OS", ["the page was referenced", "the page was modified", "the page is shared", "the page is invalid"], 1, "It must be written back.")],
       summary=["Page fault → load page, update table, restart; EAT = (1−p)m + p·s.", "FIFO (Belady), OPT (minimum), LRU (stack algorithm), clock approximates LRU.", "Textbook string with 3 frames: FIFO 15, LRU 12, OPT 9.",
                "Thrashing: insufficient frames; fix via working set or less multiprogramming.", "Copy-on-write, memory-mapped files, page-size trade-offs.", "Initial references count as faults."])


# ======================================================================================================
lesson(subject=S, chapter="Storage", ch_no=5, no=1, slug="os-file-systems-disks", title="File Systems, Disk Scheduling & RAID",
       topic="File Systems & Disk Scheduling", minutes=24, weight=5, widget="disk",
       widget_hint="Enter the head position, the request queue and the disk size to see the head movement under FCFS, SSTF, SCAN, C-SCAN, LOOK and C-LOOK.",
       key="A file system maps names to disk blocks using allocation schemes (contiguous, linked, indexed/inode). The disk's access time is seek + rotation + transfer, and scheduling algorithms reorder requests to reduce head movement. RAID combines disks for speed and reliability.",
       analogy=("📼", "A record player", "To fetch a track the arm must swing to the right groove (seek), wait for the record to spin to the start of the track (rotational latency), then play it (transfer). Scheduling is about visiting the requested grooves in an order that minimises arm swings."),
       sections=[
           dict(h="Files, directories and allocation", md="""A **file** is a named collection of blocks; the **directory** maps names to file metadata (in Unix the **inode**: size, permissions, timestamps, block pointers — the name is in the directory entry).

| Allocation | Pros | Cons |
|---|---|---|
| **Contiguous** | fast sequential and direct access, tiny metadata | external fragmentation, files can't grow |
| **Linked** | no external fragmentation, files grow | slow random access, pointer overhead, a lost pointer breaks the chain |
| **FAT** | linked list kept in a table (cacheable) | table must be in memory |
| **Indexed / inode** | direct access, no external fragmentation | index block overhead |

**Unix inode:** d direct pointers + 1 single-indirect + 1 double-indirect + 1 triple-indirect. With block size B and pointer size P, a block holds n = B / P pointers, so
**maximum file size = (d + n + n² + n³) × B**.""",
                formulas=[("max file size = (d + n + n² + n³) · B,  n = B / P", "Unix inode with direct + 3 indirect levels")]),
           dict(h="Disk structure and access time", md="""A disk has platters, **tracks**, **sectors** and cylinders. Access time = **seek time + rotational latency + transfer time**.

- **Rotational latency** (average) = ½ rotation = ½ · 60 / RPM seconds.
- **Transfer time** for one sector = rotation time / sectors per track; for a block = (block size / track size) × rotation time.
- Sequential throughput = track size × rotations per second (no seeks).

SSDs have no seek or rotation, but limited write endurance and erase-before-write.""",
                formulas=[("avg rotational latency = ½ · (60 / RPM)", "seconds")]),
           dict(h="Disk scheduling algorithms", md="""Requests are cylinder numbers; the head is at h; total head movement is the sum of distances.

| Algorithm | Behaviour |
|---|---|
| **FCFS** | serve in arrival order; fair but wanders |
| **SSTF** | nearest request first; can starve far requests |
| **SCAN** (elevator) | sweep in one direction to the **end of the disk**, then reverse |
| **C-SCAN** | sweep one way to the end, jump back to 0, sweep again (uniform wait) |
| **LOOK / C-LOOK** | like SCAN/C-SCAN but turn around at the last request, not the disk end |

The textbook example (head 53, queue 98 183 37 122 14 124 65 67, cylinders 0–199): FCFS 640, SSTF 236, the SCAN result depends on the initial direction, so always read it. For SCAN moving up first: (199 − 53) + (199 − 14) = 331; LOOK up first: (183 − 53) + (183 − 14) = 299."""),
           dict(h="RAID", md="""| Level | Idea | Usable capacity (N disks) | Fault tolerance |
|---|---|---|---|
| **RAID 0** | striping | N | none |
| **RAID 1** | mirroring | N / 2 | 1 disk per pair |
| **RAID 5** | striping + distributed parity | N − 1 | any 1 disk |
| **RAID 6** | double parity | N − 2 | any 2 disks |
| **RAID 10** | mirrored stripes | N / 2 | 1 per mirror pair |

RAID 5 small writes need 4 I/Os (read old data and parity, write new data and parity). Journaling file systems log metadata changes first for fast crash recovery. **I/O methods:** programmed I/O, interrupt-driven, DMA."""),
       ],
       examples=[
           Ex("Maximum file size", "Block size 1 KB, pointer size 4 bytes, an inode has 10 direct pointers and one single-, one double- and one triple-indirect pointer. What is the maximum file size?",
              ["n = 1024 / 4 = 256 pointers per block.", "Blocks = 10 + 256 + 256² + 256³ = 10 + 256 + 65,536 + 16,777,216 = 16,843,018.", "Size = 16,843,018 KB ≈ **16.06 GB**."],
              "16,843,018 blocks ≈ **16.06 GB**.", verify=lambda: "%d blocks ≈ %.2f GB" % (10 + 256 + 256 ** 2 + 256 ** 3, (10 + 256 + 256 ** 2 + 256 ** 3) * 1024 / 2 ** 30)),
           Ex("Disk scheduling", "Head at 53, requests 98 183 37 122 14 124 65 67, cylinders 0–199. Total head movement under FCFS, SSTF, SCAN (moving up first) and LOOK (up first)?",
              ["FCFS: 45 + 85 + 146 + 85 + 108 + 110 + 59 + 2 = 640.", "SSTF visits 65, 67, 37, 14, 98, 122, 124, 183 ⇒ 236.", "SCAN up first: to 199 then back to 14 ⇒ 146 + 185 = 331. LOOK up first: to 183 then to 14 ⇒ 130 + 169 = 299."],
              "FCFS **640**, SSTF **236**, SCAN **331**, LOOK **299**.", verify=lambda: "FCFS %d, SSTF %d, SCAN %d, LOOK %d" % (O.disk_fcfs(53, [98, 183, 37, 122, 14, 124, 65, 67]), O.disk_sstf(53, [98, 183, 37, 122, 14, 124, 65, 67]), O.disk_scan(53, [98, 183, 37, 122, 14, 124, 65, 67], 199), O.disk_look(53, [98, 183, 37, 122, 14, 124, 65, 67]))),
           Ex("Disk access time", "A 7200 RPM disk has 200 sectors per track and an average seek of 6 ms. Find the average time to read one sector.",
              ["One rotation = 60 / 7200 s = 8.33 ms; average rotational latency = 4.17 ms.", "Transfer of one sector = 8.33 / 200 = 0.0417 ms.", "Total = 6 + 4.17 + 0.04 = **10.21 ms**."],
              "≈ **10.21 ms**", verify=lambda: "%.2f ms" % (6 + 0.5 * 60000 / 7200 + 60000 / 7200 / 200)),
           Ex("RAID capacity", "Six 2 TB disks are arranged as RAID 5, RAID 10 and RAID 0. What is the usable capacity in each case?",
              ["RAID 5 loses one disk to parity: (6 − 1) × 2 = 10 TB.", "RAID 10 mirrors every disk: 6/2 × 2 = 6 TB; RAID 0 uses all six: 6 × 2 = 12 TB."],
              "RAID 5 **10 TB**, RAID 10 **6 TB**, RAID 0 **12 TB**.", verify=lambda: "RAID 5 %d TB, RAID 10 %d TB, RAID 0 %d TB" % ((6 - 1) * 2, 6 // 2 * 2, 6 * 2)),
       ],
       traps=[("SCAN vs LOOK", "SCAN goes all the way to the disk end; LOOK turns at the last request."),
              ("Initial direction", "Disk-scheduling answers change with the initial direction; read it in the problem."),
              ("Pointers per block", "n = block size / pointer size, then raise to the 2nd and 3rd power for double/triple indirect."),
              ("Rotational latency", "The average is half a rotation, not a full rotation.")],
       quick=[("Which scheduling algorithm can starve requests?", ["FCFS", "SSTF", "C-SCAN", "LOOK"], 1, "SSTF."),
              ("Which allocation suffers from external fragmentation?", ["indexed", "linked", "contiguous", "FAT"], 2, "Contiguous."),
              ("RAID 5 tolerates the failure of", ["no disk", "any one disk", "two disks", "all disks"], 1, "Single parity."),
              ("The file name in Unix is stored in", ["the inode", "the directory entry", "the superblock", "the data block bitmap"], 1, "Inodes hold metadata but not the name.")],
       summary=["Allocation: contiguous (fast, fragmentation), linked/FAT (slow random), indexed/inode.", "Max file size (d + n + n² + n³)·B with n = B/P.", "Access time = seek + ½ rotation + transfer.",
                "FCFS, SSTF (starvation), SCAN, C-SCAN, LOOK, C-LOOK; textbook FCFS 640, SSTF 236.", "RAID 0 striping, 1 mirror, 5 single parity, 6 double parity.", "Journaling gives fast crash recovery."])
