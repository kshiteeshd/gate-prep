"""OS part 1: processes & threads, CPU scheduling, synchronization."""
from functools import lru_cache

from content import g_os as O
from learn import Ex, lesson

S = "OS"
PS = [(1, 0, 7), (2, 1, 4), (3, 2, 1), (4, 3, 4)]   # (pid, arrival, burst)


def fcfs(ps):
    t, ct = 0, {}
    for p in sorted(ps, key=lambda p: (p[1], p[0])):
        t = max(t, p[1]) + p[2]
        ct[p[0]] = t
    return ct


def avg_wt(ct, ps):
    return sum(ct[p[0]] - p[1] - p[2] for p in ps) / len(ps)


def avg_tat(ct, ps):
    return sum(ct[p[0]] - p[1] for p in ps) / len(ps)


def forks(prog):
    """Process count for a fork program: 'F' = fork(); 'IFC' = if (fork() == 0) fork();"""
    n = 1
    for step in prog:
        if step == "F":
            n *= 2
        elif step == "IFC":      # if (fork() == 0) fork();  each process gains a child and a grandchild
            n *= 3
    return n


def race_range(N):
    """exhaustive interleavings of two threads each doing N times: load; inc; store on a shared counter"""
    @lru_cache(None)
    def go(p0, p1, r0, r1, x):
        if p0 == 3 * N and p1 == 3 * N:
            return frozenset([x])
        out = set()
        for t in (0, 1):
            p = (p0, p1)[t]
            if p == 3 * N:
                continue
            ph = p % 3
            r = (r0, r1)[t]
            nx = x
            if ph == 0:
                r = x
            elif ph == 1:
                r += 1
            else:
                nx = r
            n0, n1, nr0, nr1 = p0, p1, r0, r1
            if t == 0:
                n0 += 1
                nr0 = r
            else:
                n1 += 1
                nr1 = r
            out |= go(n0, n1, nr0, nr1, nx)
        return frozenset(out)
    s = go(0, 0, 0, 0, 0)
    return min(s), max(s)


# ======================================================================================================
lesson(subject=S, chapter="Processes & Scheduling", ch_no=1, no=1, slug="os-processes-threads", title="Processes, Threads & System Calls",
       topic="Processes, Threads & Syscalls", minutes=20, weight=4, widget="none",
       key="A process is a program in execution with its own address space and a process control block; threads share the process's memory but have separate stacks and registers. System calls are the controlled gateway from user mode into the kernel, and fork() is the classic way to create processes.",
       analogy=("🏭", "A factory and its workers", "A process is a factory: it owns the building (address space), machines (open files) and paperwork (PCB). Threads are the workers inside — they share the factory's tools but each has their own desk and notepad (stack and registers). Hiring another worker (thread) is cheap; building another factory (process) is expensive."),
       sections=[
           dict(h="Process: states and the PCB", md="""A process has code (text), data, heap and stack. The OS tracks it in a **Process Control Block (PCB)**: PID, state, program counter, registers, scheduling info, memory-management info (page-table pointer), open files, accounting.

**Five-state model:** *New → Ready → Running → Terminated*, with *Running → Waiting (blocked)* on I/O and *Waiting → Ready* when the event completes. Running → Ready happens on **pre-emption** (timer interrupt). Medium-term scheduling adds *suspended* states by swapping.

- **Long-term (job) scheduler:** admits jobs; controls the degree of multiprogramming.
- **Short-term (CPU) scheduler:** picks the next ready process; runs very often.
- **Medium-term scheduler:** swaps processes in/out.
- **Dispatcher:** performs the context switch; **dispatch latency** is the time it takes."""),
           dict(h="Context switching and modes", md="""A **context switch** saves the state of the running process in its PCB and loads another's. It is **pure overhead** (no useful work) and costly because of register saves and cache/TLB effects.

The CPU has **user mode** and **kernel mode**. Privileged instructions (I/O, halting, changing the MMU) run only in kernel mode. A **system call** executes a trap instruction that switches to kernel mode; an **interrupt** is an asynchronous hardware event, a **trap/exception** is synchronous (system call, page fault, divide by zero).

Typical system calls: fork, exec, wait, exit, open, read, write, close, pipe, kill, mmap."""),
           dict(h="Threads", md="""| | Process | Thread |
|---|---|---|
| Address space | own | **shared** with its process |
| Code, data, heap, open files | own | shared |
| Registers, stack, PC | own | **own** |
| Creation / context switch | expensive | cheap |
| Failure | isolated | one bad thread can kill the whole process |

**User-level threads** are managed by a library — switching is fast and needs no kernel mode, but a blocking system call blocks the whole process and threads cannot run in parallel on multiple cores. **Kernel-level threads** are scheduled by the OS (true parallelism, one blocks without blocking others). Models: many-to-one, one-to-one, many-to-many."""),
           dict(h="fork(), exec() and wait()", md="""`fork()` creates a **child** that is a copy of the parent; it returns **0 in the child** and the child's PID in the parent (−1 on failure). Both continue from the instruction after fork.

- After n sequential `fork()` calls (no conditions) there are **2ⁿ** processes in total (2ⁿ − 1 new ones).
- `exec()` replaces the process image; it does **not** create a new process.
- `wait()` makes the parent block until a child terminates; a child that has exited but not been waited on is a **zombie**; a child whose parent exited is an **orphan** (adopted by init).
- Copy-on-write lets parent and child share pages until one writes.

For `if (fork() == 0) fork();` count carefully: the original forks (2 processes), only the child continues into the second fork (3 processes total).""",
                call=[("trap", "Counting forks", "Draw the process tree. Each fork() doubles every process that reaches it, but a condition on the return value limits who executes the next fork.")]),
       ],
       examples=[
           Ex("Number of processes", "How many processes (including the original) exist after the code `fork(); fork(); fork();`?",
              ["Each fork() doubles the number of processes: 1 → 2 → 4 → 8.", "Total processes = 2³ = **8** (7 new children)."],
              "**8**", verify=lambda: str(forks(["F", "F", "F"]))),
           Ex("Conditional fork", "How many processes (including the original) exist after `if (fork() == 0) fork();` executes?",
              ["The first fork creates a child: 2 processes. Only the child (return value 0) executes the second fork, creating a grandchild.", "Total = 1 original + 1 child + 1 grandchild = **3**."],
              "**3**", verify=lambda: str(forks(["IFC"]))),
           Ex("Race on a shared counter", "Two threads each execute `count = count + 1` N times without synchronisation (each iteration is load, add, store). With N = 2, what are the minimum and maximum final values of count starting from 0?",
              ["Maximum: no interference gives 2 × N = 4.", "Minimum: a thread can overwrite the other's updates with stale loads; exhaustive interleaving of all 6 + 6 operations shows the smallest reachable value is **2** (and for larger N it is still 2)."],
              "Minimum **2**, maximum **4**.", verify=lambda: "Minimum %d, maximum %d" % race_range(2)),
           Ex("Context-switch overhead", "A CPU runs a time slice of 10 ms and each context switch takes 1 ms. What fraction of CPU time is useful work?",
              ["Each cycle is 10 ms of work + 1 ms of switching = 11 ms.", "Useful fraction = 10 / 11 ≈ **0.909** (about 90.9%)."],
              "≈ **0.909**", verify=lambda: "%.3f" % (10 / 11)),
       ],
       traps=[("Threads share the heap, not the stack", "Each thread has its own stack and registers; code, data, heap and files are shared."),
              ("exec does not create a process", "exec replaces the current image; fork creates the process."),
              ("Interrupt vs trap", "Interrupts are asynchronous (hardware); traps are synchronous (caused by the running instruction)."),
              ("User-level threads and blocking", "A blocking call in one user-level thread blocks them all.")],
       quick=[("fork() returns what in the child?", ["the child's PID", "0", "−1", "the parent's PID"], 1, "0 in the child."),
              ("Which is NOT shared between threads of a process?", ["heap", "global variables", "stack", "open files"], 2, "Each thread has its own stack."),
              ("A system call switches the CPU to", ["user mode", "kernel mode", "real mode", "idle"], 1, "Via a trap."),
              ("After 5 sequential fork() calls the number of processes is", ["5", "10", "25", "32"], 3, "2⁵ = 32.")],
       summary=["PCB stores a process's state; states: new, ready, running, waiting, terminated.", "Context switch is overhead; dispatcher performs it; long/short/medium-term schedulers.", "User vs kernel mode; syscalls trap into the kernel; interrupts are asynchronous.",
                "Threads share code/data/heap/files, own stack and registers; user-level threads block together.", "fork returns 0 in the child; n sequential forks give 2ⁿ processes.", "Zombie = exited, not waited; orphan = parent exited."])


# ======================================================================================================
lesson(subject=S, chapter="Processes & Scheduling", ch_no=1, no=2, slug="os-cpu-scheduling", title="CPU Scheduling Algorithms",
       topic="CPU Scheduling", minutes=24, weight=6, widget="cpusched",
       widget_hint="Enter arrival and burst times, choose FCFS, SJF, SRTF, Round Robin or Priority, and read the Gantt chart with completion, turnaround and waiting times.",
       key="A CPU scheduler picks which ready process runs next. FCFS is simple but suffers the convoy effect, SJF/SRTF minimise average waiting time, Round Robin gives fairness through a time quantum, and priority scheduling needs aging to avoid starvation. GATE asks you to compute Gantt charts and averages.",
       analogy=("🛒", "Checkout queues", "At a supermarket, serving customers strictly in arrival order (FCFS) lets one big trolley hold up everyone behind it. Serving the smallest basket first (SJF) minimises the average wait but big baskets may wait forever. Giving each person a fixed 2-minute turn (Round Robin) is fair but adds switching overhead."),
       sections=[
           dict(h="Definitions you must use correctly", md="""For each process: **AT** arrival time, **BT** burst time, **CT** completion time.

- **Turnaround time** TAT = CT − AT.
- **Waiting time** WT = TAT − BT (time spent in the ready queue).
- **Response time** = first CPU time − AT.
- **Throughput** = processes completed per unit time; **CPU utilisation** = busy time / total time.

**Preemptive** algorithms can take the CPU from a running process; **non-preemptive** ones wait until it blocks or finishes. Idle gaps appear when nothing has arrived yet.""",
                formulas=[("TAT = CT − AT;  WT = TAT − BT", "per process")]),
           dict(h="FCFS, SJF and SRTF", md="""- **FCFS** (non-preemptive): run in arrival order. Easy, but the **convoy effect** (short jobs stuck behind a long one) inflates waiting time.
- **SJF** (non-preemptive): pick the ready process with the shortest burst. **Optimal for minimum average waiting time** among non-preemptive algorithms, but needs burst prediction (exponential averaging τ_{n+1} = α·t_n + (1 − α)·τ_n) and can **starve** long jobs.
- **SRTF** (preemptive SJF): whenever a process arrives, compare its burst with the *remaining* time of the running one. Gives the minimum average waiting time overall.

Tie-breaking: unless stated otherwise, break ties by arrival time and then by process number."""),
           dict(h="Round Robin and priority scheduling", md="""**Round Robin (RR):** a FIFO ready queue with time quantum q. A process runs for min(q, remaining); if unfinished it goes to the **back** of the queue. Newly arrived processes join the queue before the pre-empted one if they arrive at the moment the quantum ends.

- q → ∞ makes RR behave like FCFS; q → 0 gives processor sharing but context-switch overhead dominates. A good q is larger than most CPU bursts.
- With n processes and quantum q, any process waits at most (n − 1)·q before its next turn.
- **Priority scheduling** (preemptive or not): lowest number (or highest, as stated) first. **Starvation** of low-priority processes is cured by **aging**.
- **Multilevel queue / feedback queue** use several queues; feedback lets processes move between them (CPU-bound drift down).""",
                call=[("trap", "Queue order in RR", "When a quantum expires at the same instant a new process arrives, the new arrival is placed in the queue *before* the pre-empted process, unless the question says otherwise.")]),
           dict(h="Which algorithm for which goal", md="""| Goal | Best choice |
|---|---|
| Minimum average waiting time (non-preemptive) | **SJF** |
| Minimum average waiting time (preemptive) | **SRTF** |
| Fair, good response time | **Round Robin** |
| Simplest; no starvation | **FCFS** |
| Real-time deadlines | EDF / rate-monotonic |
| Interactive + batch mix | multilevel feedback queue |

FCFS and RR never starve; SJF, SRTF and priority can."""),
       ],
       examples=[
           Ex("FCFS and SJF averages", "Processes (AT, BT): P1 (0,7), P2 (1,4), P3 (2,1), P4 (3,4). Compute the average waiting time under FCFS and under non-preemptive SJF.",
              ["FCFS order P1, P2, P3, P4: completion 7, 11, 12, 16; WT = 0, 6, 9, 9 ⇒ average 24/4 = 6.", "SJF: P1 runs 0–7. At t = 7 ready are P2(4), P3(1), P4(4) ⇒ P3 (to 8), then P2 (to 12), then P4 (to 16). WT = 0, 7, 5, 9 ⇒ 21/4 = 5.25."],
              "FCFS **6**, SJF **5.25**.", verify=lambda: "FCFS %g, SJF %g" % (avg_wt(fcfs(PS), PS), avg_wt(O.sjf_np(PS), PS))),
           Ex("SRTF", "For the same four processes find the average waiting time under SRTF.",
              ["t=0 P1 runs; at t=1 P2 (4) < P1 remaining 6, switch; at t=2 P3 (1) < 3, switch; P3 finishes at 3.", "Then P2 (remaining 3) finishes at 6 (P4 arrives at 3 with burst 4, longer); P4 runs 6–10; P1 finishes at 16.", "CT: P1=16, P2=6, P3=3, P4=10 ⇒ WT = 9, 1, 0, 3 ⇒ 13/4 = **3.25**."],
              "**3.25**", verify=lambda: "%g" % avg_wt(O.srtf(PS), PS)),
           Ex("Round Robin", "Same processes, Round Robin with quantum 2. What is the completion time of P1 and the average waiting time?",
              ["Simulating the queue (new arrivals queue before the pre-empted process): completion times are P3 = 5, P2 = 11, P4 = 15, P1 = 16.", "WT = CT − AT − BT = 9, 6, 2, 8 ⇒ average 25/4 = **6.25**; P1 completes at **16**."],
              "P1 completes at **16**; average WT **6.25**.", verify=lambda: "P1 completes at %d; average WT %g" % (O.rr(PS, 2)[1], avg_wt(O.rr(PS, 2), PS))),
           Ex("Turnaround from waiting", "A process has burst time 12 ms and waits a total of 18 ms. What are its turnaround time and, if it arrived at t = 5 ms, its completion time?",
              ["TAT = WT + BT = 18 + 12 = 30 ms.", "CT = AT + TAT = 5 + 30 = **35 ms**."],
              "TAT **30** ms, CT **35** ms.", verify=lambda: "TAT %d ms, CT %d ms" % (18 + 12, 5 + 18 + 12)),
       ],
       traps=[("Waiting time includes only ready-queue time", "WT = TAT − BT, not CT − BT."),
              ("SRTF compares with remaining time", "A new arrival pre-empts only if its burst is less than the running process's remaining time."),
              ("Idle CPU", "If nothing is ready, the clock jumps to the next arrival — do not add idle time to any process's waiting time."),
              ("Starvation", "SJF, SRTF and priority scheduling can starve; FCFS and RR cannot.")],
       quick=[("Which gives the minimum average waiting time among all algorithms?", ["FCFS", "RR", "SRTF", "Priority"], 2, "SRTF is optimal."),
              ("The convoy effect is associated with", ["RR", "FCFS", "SRTF", "MLFQ"], 1, "Short jobs queue behind a long one."),
              ("As the RR quantum becomes very large, RR behaves like", ["SJF", "FCFS", "SRTF", "priority"], 1, "No pre-emption."),
              ("Aging is used to prevent", ["deadlock", "starvation", "thrashing", "fragmentation"], 1, "Priority increases while waiting.")],
       summary=["TAT = CT − AT; WT = TAT − BT; response = first run − AT.", "FCFS: convoy effect; SJF optimal non-preemptive; SRTF optimal overall.", "RR: quantum q; large q → FCFS; fair, no starvation.",
                "Priority scheduling starves low priorities — use aging.", "SJF/SRTF/priority can starve; FCFS/RR cannot.", "Tie-break by arrival time then process number."])


# ======================================================================================================
lesson(subject=S, chapter="Concurrency", ch_no=2, no=1, slug="os-synchronization", title="Synchronization: Critical Sections, Semaphores & Classic Problems",
       topic="Synchronization", minutes=24, weight=6, widget="none",
       key="Processes sharing data must coordinate. A correct critical-section solution gives mutual exclusion, progress and bounded waiting. Semaphores (P/V, wait/signal) and monitors solve it; producer–consumer, readers–writers and dining philosophers are the standard problems.",
       analogy=("🚻", "A single-occupancy restroom", "Only one person may be inside at a time (mutual exclusion). If it's empty, someone waiting must be allowed in without deliberation (progress), and nobody should wait forever while others keep cutting in (bounded waiting). A semaphore is the key hanging on the hook outside."),
       sections=[
           dict(h="Race conditions and the critical-section problem", md="""A **race condition** arises when the result depends on the interleaving of accesses to shared data (e.g. `count++` is load–add–store, not atomic).

A solution to the **critical-section problem** must satisfy:

1. **Mutual exclusion** — at most one process in its critical section.
2. **Progress** — if no one is in the CS and some want in, the choice of who enters can't be postponed indefinitely and only processes in their entry section decide.
3. **Bounded waiting** — a limit on how many times others can enter before a waiting process gets its turn.

(No assumption about speeds or number of CPUs.)"""),
           dict(h="Software and hardware solutions", md="""- **Peterson's algorithm** (two processes): shared `flag[2]` and `turn`. To enter, set `flag[i] = true; turn = j;` then wait while `flag[j] && turn == j`. Satisfies mutual exclusion, progress and bounded waiting.
- **Strict alternation** (`while (turn != i);`) gives mutual exclusion but **violates progress**.
- **Lock variable** (test then set, non-atomic) fails mutual exclusion.
- **Hardware atomics:** `TestAndSet`, `Swap`, compare-and-swap. A spinlock built from TestAndSet gives mutual exclusion and progress but **not bounded waiting**.
- **Disabling interrupts** only works on a single CPU and is unsafe for user code."""),
           dict(h="Semaphores", md="""A **semaphore** S is an integer accessed only through two atomic operations:

    wait(S) / P(S):   S = S − 1;  if (S < 0) block the caller
    signal(S) / V(S): S = S + 1;  if (S ≤ 0) wake one blocked process

- **Binary semaphore** (0/1, a *mutex*) gives mutual exclusion; initial value 1.
- **Counting semaphore** controls a pool of k identical resources; initial value k.
- When S < 0, |S| = number of blocked processes. **Final value** = initial − (#P) + (#V) if no operation blocks the final count.
- Using a semaphore for **ordering**: initialise to 0 and make the later process wait on it.

Wrong order of P operations leads to **deadlock**; forgetting V causes starvation of others; reversing P and V breaks mutual exclusion."""),
           dict(h="Classic problems", md="""**Bounded buffer (producer–consumer)**, buffer size n:

    semaphore mutex = 1, empty = n, full = 0
    Producer: P(empty); P(mutex); put item; V(mutex); V(full)
    Consumer: P(full);  P(mutex); take item; V(mutex); V(empty)

Swapping the two P's in either process (P(mutex) before P(empty)) can **deadlock** when the buffer is full/empty.

**Readers–writers:** many readers or one writer. The first-readers-writers solution (reader preference) uses `read_count` protected by a mutex and a `write` semaphore; it can **starve writers**.

**Dining philosophers** (5 philosophers, 5 forks): picking up left then right fork can deadlock if all hold one fork. Fixes: allow at most 4 to sit, pick up both forks atomically, or break symmetry (one philosopher picks right first / odd–even ordering).

**Monitors** encapsulate shared data with automatic mutual exclusion and **condition variables** (wait/signal)."""),
       ],
       examples=[
           Ex("Semaphore value", "A counting semaphore is initialised to 5. Then 12 P (wait) and 4 V (signal) operations are performed in some order. What is the final value, and how many processes are blocked?",
              ["Final value = 5 − 12 + 4 = −3.", "A negative value −k means k processes are blocked: 3 blocked."],
              "Value **−3**; **3** blocked.", verify=lambda: "Value %d; %d blocked" % (5 - 12 + 4, -(5 - 12 + 4))),
           Ex("Bounded-buffer capacity", "Producer–consumer with empty = 10, full = 0, mutex = 1. The producer completes 14 items while the consumer has consumed 6. What are the values of empty and full (no one is blocked)?",
              ["Producer has done 14 P(empty), consumer 6 V(empty): empty = 10 − 14 + 6 = 2.", "Producer did 14 V(full), consumer 6 P(full): full = 0 + 14 − 6 = 8. Items in buffer = 8, free slots = 2, and 8 + 2 = 10 ✔."],
              "empty = **2**, full = **8**.", verify=lambda: "empty = %d, full = %d" % (10 - 14 + 6, 0 + 14 - 6)),
           Ex("Unsynchronised counter", "Two threads each increment a shared counter (starting at 0) 3 times with no locks. Which final values are possible? (give the minimum)",
              ["Maximum 6 when increments never overlap. Stale loads can lose updates; exhaustive interleavings of load/add/store show the smallest reachable value is **2**.", "(For N = 3 per thread the minimum is still 2 — a classic result.)"],
              "Minimum **2**, maximum **6**.", verify=lambda: "Minimum %d, maximum %d" % race_range(3)),
           Ex("Peterson versus alternation", "Which of mutual exclusion, progress and bounded waiting does the strict-alternation solution (`while (turn != i);`) violate?",
              ["Only one process can be in the CS at once, so mutual exclusion holds.", "A process that wants in must wait for its turn even if the other process is not interested ⇒ **progress is violated**."],
              "**Progress**", verify=lambda: "Progress"),
       ],
       traps=[("TestAndSet spinlock", "Provides mutual exclusion and progress, but not bounded waiting."),
              ("Order of P operations", "P(mutex) before P(empty) in the producer can deadlock the system."),
              ("Negative semaphore value", "Its magnitude is the number of blocked processes."),
              ("Peterson's algorithm", "Works for two processes only; with reordering on modern CPUs it needs memory barriers.")],
       quick=[("A binary semaphore is initialised to", ["0 always", "1", "the buffer size", "−1"], 1, "1 for mutual exclusion."),
              ("Strict alternation fails", ["mutual exclusion", "progress", "bounded waiting only", "none"], 1, "It makes a process wait even when the other is not interested."),
              ("Dining philosophers deadlock can be avoided by", ["allowing 5 to sit", "allowing at most 4 to sit", "using more spoons per bowl", "none"], 1, "At most n − 1 contenders."),
              ("In the bounded buffer, the 'full' semaphore initially equals", ["n", "1", "0", "n − 1"], 2, "No items yet.")],
       summary=["Critical section needs mutual exclusion, progress, bounded waiting.", "Peterson: flag[] + turn; strict alternation breaks progress; TestAndSet spinlock lacks bounded waiting.", "wait: S−−, block if S<0; signal: S++, wake if S≤0; |negative S| = blocked processes.",
                "Bounded buffer: mutex=1, empty=n, full=0; wrong P order deadlocks.", "Readers–writers (reader preference) can starve writers.", "Dining philosophers: limit to n−1, atomic pick-up or asymmetric order."])
