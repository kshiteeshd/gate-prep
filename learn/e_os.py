"""Textbook-style long-form teaching text: Operating Systems."""
from learn import elab

elab("os-processes-threads",
 ("What an operating system does", """
A computer's hardware — CPU, memory, disks, network — is shared by many programs. The **operating system (OS)** is the software that manages these resources: it decides which program runs when, gives each program its own memory, controls access to files and devices, and provides a clean interface (system calls) so programs don't have to know hardware details.

A **program** is a file of instructions sitting on disk. A **process** is a program *in execution*: the instructions plus the current values of the registers, the program counter, the stack, the heap and the open files. One program can run as many processes.
"""),
 ("Process states and the PCB", """
During its life a process moves between states: **new** (being created), **ready** (waiting for the CPU), **running** (executing on the CPU), **waiting/blocked** (waiting for I/O or an event) and **terminated**. The OS keeps a **process control block (PCB)** for each process, which stores its state, program counter, registers, memory information and scheduling data. Switching the CPU from one process to another is a **context switch**: save the old PCB, load the new one. It is pure overhead, because no useful work is done during it.

A new process is created with `fork()` in Unix: the child is a copy of the parent. `fork()` returns 0 in the child and the child's PID in the parent. A program that calls `fork()` $n$ times in a row (without conditions) produces $2^n$ processes in total, i.e. $2^n-1$ children.
"""),
 ("Threads", """
A **thread** is a unit of execution *inside* a process. Threads of the same process **share** the code, data, heap and open files, but each has its **own** stack, registers and program counter. Because they share memory, threads are cheap to create and communicate easily, but they must be synchronised to avoid corrupting shared data.

**User-level threads** are managed by a library; the OS sees a single process, so one blocking call can block all threads. **Kernel-level threads** are managed by the OS, can run on different CPUs, and a blocking call blocks only one thread.
"""),
)

elab("os-cpu-scheduling",
 ("The scheduling problem", """
When several processes are ready, the OS must choose which gets the CPU next. A **scheduling algorithm** makes that choice. Different goals pull in different directions: high CPU utilisation, high throughput (jobs per second), low **turnaround time**, low **waiting time**, and low **response time**.

For one process define:

- **Arrival time (AT)** — when it enters the ready queue.
- **Burst time (BT)** — CPU time it needs.
- **Completion time (CT)** — when it finishes.
- **Turnaround time (TAT)** $=CT-AT$.
- **Waiting time (WT)** $=TAT-BT$.
"""),
 ("The main algorithms", """
**FCFS (first come, first served)** runs processes in order of arrival. It is simple but suffers the **convoy effect**: a long job at the front makes all short jobs wait.

**SJF (shortest job first)** picks the shortest next burst and gives the **minimum average waiting time**. Its preemptive version is **SRTF (shortest remaining time first)**. The difficulty is knowing burst times in advance, and long jobs may **starve**.

**Round robin (RR)** gives each process a fixed **time quantum** in turn, then moves it to the back of the queue. It is fair and gives good response time. If the quantum is very large RR behaves like FCFS; if it is very small the context-switch overhead dominates.

**Priority scheduling** runs the highest-priority process; low-priority processes may starve, which is fixed by **aging** (gradually increasing the priority of waiting processes).
"""),
 ("How to solve a scheduling problem", """
Draw a **Gantt chart**: a timeline showing which process runs in each interval. For preemptive algorithms, re-decide whenever a new process arrives. Then compute CT for each process directly from the chart, and TAT and WT from the formulas. In round robin, a process that arrives *at the same time* as another's quantum expires is conventionally queued *before* the preempted process, unless the question says otherwise.
"""),
)

elab("os-synchronization",
 ("Why synchronisation is needed", """
Two threads running `counter++` can interfere. The statement is really three steps: load the value, add 1, store it back. If both threads load 5, both add 1, and both store 6, one update is lost. When the result depends on the *timing* of threads, this is a **race condition**.

A **critical section** is a piece of code that touches shared data and must be executed by only one thread at a time. A correct solution to the critical-section problem must provide:

- **Mutual exclusion:** at most one thread is inside.
- **Progress:** if nobody is inside, a thread that wants to enter is not delayed indefinitely by threads that don't.
- **Bounded waiting:** no thread waits forever.
"""),
 ("Semaphores", """
A **semaphore** is an integer variable accessed only through two atomic operations: `wait(S)` (also P): decrease $S$ and block if the result would be negative; and `signal(S)` (also V): increase $S$ and wake a waiting thread if any. A **binary semaphore** (0 or 1) acts as a lock. A **counting semaphore** controls access to a pool of $n$ identical resources.

Classic problems:

- **Producer–consumer (bounded buffer):** semaphores `empty` (initially $N$), `full` (initially 0) and a `mutex`. The producer does `wait(empty); wait(mutex); add; signal(mutex); signal(full)`.
- **Readers–writers:** many readers may read together; a writer needs exclusive access.
- **Dining philosophers:** five philosophers and five forks; a naive "pick left, then right" can deadlock.

**Order matters:** acquiring `mutex` *before* `empty` in the producer can deadlock.
"""),
 ("Software and hardware solutions", """
**Peterson's solution** for two processes uses a `flag[2]` array and a `turn` variable: a process sets its flag, gives the turn to the other, and waits while the other's flag is set *and* it is the other's turn. It satisfies all three requirements. Simple "just a lock variable" or "strict alternation" solutions fail (the first lacks mutual exclusion, the second lacks progress).

On real machines, the hardware provides **atomic instructions** such as `test-and-set` and `compare-and-swap`, from which locks are built. A lock that makes a thread loop while waiting is a **spinlock**, which wastes CPU but avoids a context switch for very short waits.
"""),
)

elab("os-deadlocks",
 ("What a deadlock is", """
A set of processes is **deadlocked** when each is waiting for a resource held by another in the set, so none can ever proceed. Picture four cars at a crossroads, each waiting for the car on its right to move.

Four conditions must hold **simultaneously** (the Coffman conditions):

1. **Mutual exclusion** — a resource is held by at most one process.
2. **Hold and wait** — a process holding resources waits for more.
3. **No preemption** — resources can only be released voluntarily.
4. **Circular wait** — a cycle of processes, each waiting for the next.

Remove any one of them and deadlock cannot occur.
"""),
 ("Resource-allocation graphs and handling deadlock", """
In a **resource-allocation graph** there are process nodes and resource nodes; an edge from a resource to a process means it is allocated, and from a process to a resource means it is requested. A cycle is **necessary** for deadlock; if every resource has a *single instance*, a cycle is also **sufficient**. With several instances, a cycle alone does not prove deadlock.

Approaches: **prevention** (break one Coffman condition, e.g. impose a global ordering on resources to stop circular wait), **avoidance** (grant a request only if the system stays in a *safe state*), **detection and recovery** (allow deadlocks, find them, abort or roll back a process), or **ignore** the problem, as most general-purpose OSs do.
"""),
 ("The banker's algorithm", """
A state is **safe** if there is some order in which all processes can run to completion with the available resources. The **banker's algorithm** keeps, for each process, the maximum need, the current allocation, and so $\\text{Need}=\\text{Max}-\\text{Allocation}$. To test safety:

1. Let $\\text{Work}=\\text{Available}$ and mark all processes unfinished.
2. Find an unfinished process whose Need $\\le$ Work. If none exists, go to step 4.
3. Pretend it finishes: add its Allocation to Work, mark it finished, and repeat step 2.
4. The state is safe if and only if all processes finished. The order found is a **safe sequence**.

A request is granted only if, after pretending to grant it, the state is still safe.
"""),
)

elab("os-memory-paging",
 ("Giving each process its own memory", """
Programs refer to **logical (virtual) addresses**; the hardware, via the **memory management unit (MMU)**, translates them into **physical addresses** in RAM. This lets each process behave as if it owned all memory, and protects processes from each other.

**Paging** divides logical memory into equal-sized **pages** and physical memory into **frames** of the same size. A logical address is split into a **page number** and an **offset** within the page. If the page size is $2^k$ bytes, the low $k$ bits are the offset.
"""),
 ("Translating an address", """
The **page table** of a process maps each page number to a frame number. The physical address is (frame number, offset). If the logical address has $n$ bits and the page size is $2^k$, the page table has $2^{n-k}$ entries, so its size is $2^{n-k}\\times(\\text{entry size})$.

Reading the page table costs one extra memory access per reference, so a small fast cache called the **TLB (translation lookaside buffer)** holds recent translations. With hit ratio $h$, TLB time $t$ and memory time $m$:

$$\\text{EMAT}=h\\,(t+m)+(1-h)\\,(t+2m)$$

For large address spaces the page table itself is paged: **multi-level paging**. **Inverted page tables** store one entry per physical frame.
"""),
 ("Segmentation and fragmentation", """
**Segmentation** divides memory by *meaning* (code, stack, heap) into variable-sized segments, each with a base and limit. It matches the programmer's view but suffers from **external fragmentation** — enough free memory exists in total, but not in one piece. Paging has no external fragmentation, only **internal fragmentation** (the unused part of the last page, on average half a page per process).

For variable-size allocation, **first fit** (first hole big enough), **best fit** (smallest hole big enough) and **worst fit** (largest hole) are the standard policies.
"""),
)

elab("os-virtual-memory",
 ("The idea of virtual memory", """
**Virtual memory** lets a program use more memory than physically exists, by keeping only the pages currently needed in RAM and the rest on disk. It works because of **locality of reference**: programs tend to use the same pages repeatedly.

With **demand paging** a page is brought into memory only when first used. Each page table entry has a **valid bit**. A reference to a page not in memory causes a **page fault**: the OS finds the page on disk, loads it into a free frame (choosing a victim if none is free), updates the page table, and restarts the instruction.
"""),
 ("Page replacement algorithms", """
When memory is full and a page fault occurs, the OS must evict a page.

- **FIFO:** evict the oldest page. It can suffer **Belady's anomaly**: more frames can give *more* faults.
- **Optimal (OPT):** evict the page that will not be used for the longest time; gives the fewest possible faults, but needs knowledge of the future, so it is used as a benchmark.
- **LRU (least recently used):** evict the page unused for the longest time; a good approximation of OPT and free of Belady's anomaly (it is a *stack algorithm*).

To solve a problem, simulate the reference string, tracking the frames and counting a fault for each miss. **Hit ratio** = hits ÷ references.
"""),
 ("Performance and thrashing", """
The **effective access time** with page-fault rate $p$, memory time $m$ and page-fault service time $s$ is

$$\\text{EAT}=(1-p)\\,m+p\\,s$$

Since $s$ is millions of times larger than $m$, even a tiny $p$ hurts badly. **Thrashing** occurs when a process has too few frames: it spends most of its time faulting instead of executing, and CPU utilisation collapses. The **working-set model** keeps in memory the pages used in the recent window, and a process is suspended if its working set cannot fit.
"""),
)

elab("os-file-systems-disks",
 ("Files and directories", """
A **file** is a named collection of related data. The OS stores a file's data in disk **blocks** and records its **attributes** (name, size, owner, permissions, location of its blocks). Directories map names to files and are organised as a tree.

In Unix, this information lives in an **inode**: a record containing the attributes and pointers to the file's blocks. The directory entry maps a name to an inode number.
"""),
 ("Allocation methods", """
- **Contiguous allocation:** the file occupies consecutive blocks. Fast sequential and random access, but suffers external fragmentation and files are hard to grow.
- **Linked allocation:** each block points to the next. No external fragmentation, but random access is slow, and one lost pointer breaks the file. A **FAT** variant keeps all links in a table in memory.
- **Indexed allocation:** an index block lists all the file's blocks. Supports direct access without fragmentation.

A Unix **inode** has direct pointers, a single-indirect, a double-indirect and a triple-indirect pointer. With block size $B$ and pointer size $P$, an indirect block holds $n=B/P$ pointers, so the maximum file size is $(d+n+n^2+n^3)\\times B$ for $d$ direct pointers.
"""),
 ("Disk scheduling", """
A hard disk reads a block after the head moves to the right **track** (**seek time**), the disk rotates the block under the head (**rotational latency**, on average half a revolution, $\\tfrac12\\cdot\\frac{60}{\\text{RPM}}$ seconds), and the data is transferred. Seek time dominates, so the OS orders pending requests to reduce head movement:

- **FCFS** serves requests in order.
- **SSTF** serves the closest request next (can starve far ones).
- **SCAN (elevator)** moves in one direction serving requests, then reverses. **C-SCAN** returns to the start without serving, giving a more uniform wait. **LOOK** and **C-LOOK** turn around at the last request rather than the disk's end.

Total head movement is the sum of the absolute differences between successive track positions.
"""),
)
