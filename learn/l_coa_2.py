"""COA part 2: cache & memory hierarchy, I/O, interrupts and DMA."""
import math

from learn import Ex, lesson
from learn.refs_hw import cache_sim

S = "COA"

# ======================================================================================================
lesson(subject=S, chapter="Memory & I/O", ch_no=2, no=1, slug="coa-cache-memory", title="Cache & Memory Hierarchy",
       topic="Cache & Memory Hierarchy", minutes=26, weight=7, widget="cache",
       widget_hint="Set the cache size, block size and associativity, then enter a byte-address sequence. Compare direct-mapped (1 way), 2-way and fully associative caches on the same trace.",
       key="A memory hierarchy exploits locality: small fast caches hold recently used blocks of the big slow main memory. The address splits into tag, index and offset; mapping (direct, set-associative, fully associative) and replacement determine hits, and AMAT = hit time + miss rate × miss penalty.",
       analogy=("🗄️", "Desk, shelf and warehouse", "The few papers on your desk (cache) are instant to reach; the shelf (main memory) takes a walk; the warehouse (disk) takes a drive. You keep on the desk what you used recently (temporal locality) and what lies next to it (spatial locality) — and when the desk fills up you decide which paper to send back."),
       sections=[
           dict(h="Locality and the hierarchy", md="""**Temporal locality:** recently used items are likely to be used again. **Spatial locality:** items near a used one are likely to be used soon. Hierarchy: registers → L1 → L2 → L3 → main memory → disk, with smaller, faster, costlier levels near the CPU.

- **Block (line):** unit of transfer between levels. **Hit:** the block is in the cache; **miss:** it is fetched from the next level. **Hit ratio** h; **miss rate** 1 − h.
- **Miss types (3 C's):** *compulsory* (first access), *capacity* (cache too small), *conflict* (too many blocks map to one set; absent in fully associative caches)."""),
           dict(h="Address breakdown and mapping", md="""For a byte address of A bits, block size B bytes, cache size C bytes and associativity k:

- Offset bits = log₂ B.
- Number of sets = C / (B · k); **index bits** = log₂(sets).
- **Tag bits** = A − index − offset.

| Mapping | Where may a block go? | k |
|---|---|---|
| **Direct-mapped** | exactly one line: (block number) mod (lines) | 1 |
| **k-way set associative** | any of k lines in set (block number) mod (sets) | k |
| **Fully associative** | any line | C/B (no index bits) |

Total tag storage = lines × tag bits (plus valid, dirty bits). Associativity reduces conflict misses but increases hit time and comparator cost.""",
                formulas=[("sets = C / (B·k);  tag = A − log₂(sets) − log₂ B", "address split")]),
           dict(h="Replacement and write policies", md="""**Replacement** (within a set): LRU, FIFO, random (LFU less common). LRU is a **stack algorithm**; FIFO may show Belady's anomaly in caches too.

**Write hit:** *write-through* (write cache and memory; simple, needs a write buffer) or *write-back* (write only the cache and mark the line **dirty**; write memory on eviction). **Write miss:** *write-allocate* (fetch the block, then write) or *no-write-allocate* (write straight to memory). Typical pairs: write-back + write-allocate; write-through + no-write-allocate."""),
           dict(h="AMAT and multilevel caches", md="""**Average memory access time:** AMAT = hit time + miss rate × miss penalty.

For two levels: AMAT = t_L1 + m_L1 × (t_L2 + m_L2 × t_mem) (with local miss rates). CPI with memory stalls = base CPI + (memory accesses per instruction) × miss rate × miss penalty.

**Main-memory organisation:** memory interleaving (low-order bits select the module) lets consecutive addresses be fetched in parallel; the time to fetch a block of n words from a 4-way-interleaved memory is far less than n × access time.""",
                formulas=[("AMAT = t_hit + miss rate × miss penalty", "single level"), ("CPI = CPI_base + (accesses/instr) × miss rate × penalty", "with memory stalls")]),
       ],
       examples=[
           Ex("Address breakdown", "A byte-addressable machine has 32-bit addresses and a 16 KB 4-way set-associative cache with 32-byte blocks. How many tag, index and offset bits?",
              ["Offset = log₂ 32 = 5 bits. Sets = 16384 / (32 × 4) = 128 ⇒ index = 7 bits.", "Tag = 32 − 7 − 5 = **20** bits."],
              "Tag **20**, index **7**, offset **5**.", verify=lambda: "Tag %d, index %d, offset %d" % (32 - int(math.log2(16384 // (32 * 4))) - 5, int(math.log2(16384 // (32 * 4))), 5)),
           Ex("Direct-mapped simulation", "A direct-mapped cache has 4 blocks of 16 bytes. Byte addresses accessed: 0, 16, 32, 48, 64, 0, 16, 80, 0, 64. How many hits?",
              ["Blocks 0–3 fill lines 0–3: four compulsory misses. Address 64 is block 4, which maps to line 0 and evicts block 0 (miss); address 0 then misses again and evicts block 4.", "Address 16 (line 1) hits; address 80 is block 5 → line 1 and misses, evicting block 1; address 0 (line 0) hits; address 64 evicts it (miss).", "Totals: **2** hits and 8 misses."],
              "**2** hits, **8** misses.", verify=lambda: "%d hits, %d misses" % cache_sim([0, 16, 32, 48, 64, 0, 16, 80, 0, 64], 64, 16, 1, "lru")),
           Ex("Same trace, 2-way set associative", "Same 64-byte cache and trace, now 2-way set associative with LRU. How many hits?",
              ["Now there are 2 sets of 2 lines; blocks 0 and 4 map to set 0 together and no longer evict each other immediately.", "Simulating: **3** hits, 7 misses (conflict misses removed)."],
              "**3** hits, **7** misses.", verify=lambda: "%d hits, %d misses" % cache_sim([0, 16, 32, 48, 64, 0, 16, 80, 0, 64], 64, 16, 2, "lru")),
           Ex("AMAT", "Hit time 1 ns, miss rate 5%, miss penalty 100 ns. Compute the AMAT.",
              ["AMAT = hit time + miss rate × miss penalty.", "= 1 + 0.05 × 100 = **6 ns**."],
              "**6 ns**", verify=lambda: "%g ns" % (1 + 0.05 * 100)),
           Ex("Two-level cache", "L1: 1 ns, local miss rate 10%; L2: 10 ns, local miss rate 20%; memory 100 ns. What is the AMAT?",
              ["The L1 miss goes to L2, whose own miss goes to memory: AMAT = t_L1 + m_L1 (t_L2 + m_L2 t_mem).", "= 1 + 0.1 × (10 + 0.2 × 100) = 1 + 0.1 × 30 = **4 ns**."],
              "**4 ns**", verify=lambda: "%g ns" % (1 + 0.1 * (10 + 0.2 * 100))),
       ],
       traps=[("Index vs tag", "Index selects the set; the tag disambiguates blocks within the set."),
              ("Fully associative", "Has no index bits and no conflict misses."),
              ("Write-back needs a dirty bit", "Write-through does not."),
              ("Local vs global miss rate", "L2 miss rate quoted ‘locally’ is relative to L1 misses only.")],
       quick=[("A direct-mapped cache is a k-way set-associative cache with k equal to", ["0", "1", "number of lines", "2"], 1, "k = 1."),
              ("Conflict misses do not occur in a", ["direct-mapped cache", "fully associative cache", "2-way cache", "write-back cache"], 1, "Any block can go anywhere."),
              ("Spatial locality is exploited by", ["bigger blocks", "write-through", "smaller caches", "LRU only"], 0, "Fetching neighbours."),
              ("Write-back caches mark modified lines with", ["valid bit", "dirty bit", "tag bit", "parity"], 1, "Dirty.")],
       summary=["Offset = log₂ B; index = log₂(sets); tag = rest.", "Direct-mapped k=1; fully associative: no index; set-associative in between.", "3 C's: compulsory, capacity, conflict.",
                "Write-through vs write-back (dirty bit); allocate vs no-allocate on write miss.", "AMAT = hit + miss rate × penalty; multilevel by nesting.", "Interleaved memory parallelises consecutive addresses."])


# ======================================================================================================
lesson(subject=S, chapter="Memory & I/O", ch_no=2, no=2, slug="coa-io-interrupts-dma", title="I/O Organisation, Interrupts & DMA",
       topic="I/O, Interrupts & DMA", minutes=20, weight=4, widget="none",
       key="The CPU talks to devices through I/O controllers using programmed I/O, interrupt-driven I/O or DMA. Interrupts let a device ask for attention; DMA lets a controller move whole blocks to memory with almost no CPU involvement, stealing bus cycles.",
       analogy=("🛎️", "Waiting for a parcel", "Polling is opening the door every minute to see if the courier has arrived (the CPU wastes its time). An interrupt is the doorbell: you do other work until it rings. DMA is the courier putting the parcel straight into your storeroom while you keep working and only telling you when the whole delivery is done."),
       sections=[
           dict(h="Ways to do I/O", md="""| Method | Who moves the data? | CPU involvement |
|---|---|---|
| **Programmed I/O (polling)** | CPU, word by word, busy-waiting on a status bit | 100% during the transfer |
| **Interrupt-driven I/O** | CPU, in an interrupt service routine per word/byte | overhead per interrupt |
| **DMA** | DMA controller, directly device ⇄ memory | only setup + completion interrupt |

**Memory-mapped I/O:** device registers occupy ordinary addresses, so normal load/store instructions are used. **Isolated (port-mapped) I/O:** separate address space and special IN/OUT instructions."""),
           dict(h="Interrupts", md="""An **interrupt** transfers control to a service routine: the CPU finishes the current instruction, saves the PC and state, identifies the source, jumps to the **interrupt service routine (ISR)**, then returns.

- **Types:** hardware (external, maskable/non-maskable), software (**trap/syscall**), exceptions (divide-by-zero, page fault).
- **Identifying the source:** software polling; **vectored** interrupt (the device supplies a vector); **daisy-chain** priority (closest device wins); a priority encoder or interrupt controller (8259).
- **Masking** disables lower-priority (or all) interrupts; **nested interrupts** allow a higher-priority interrupt to pre-empt an ISR.
- **Interrupt latency** = time from request to first ISR instruction.

Traps and exceptions are **synchronous**; device interrupts are **asynchronous**."""),
           dict(h="DMA", md="""A **DMA controller** has address, count and control registers. The CPU programs: memory start address, byte count, direction, device; the controller then requests the bus (**HOLD/HLDA** or BUS REQUEST/GRANT), transfers data and interrupts the CPU when the count reaches zero.

- **Burst (block) mode:** the DMA keeps the bus for the entire block; the CPU is blocked meanwhile.
- **Cycle stealing:** the DMA takes the bus for one word at a time between CPU cycles; the CPU is slowed but not stopped.
- **Transparent mode:** DMA uses the bus only when the CPU is not using it.

The percentage of **CPU time stolen** by cycle stealing = (time DMA uses per word) / (word transfer period)."""),
           dict(h="Performance calculations", md="""Typical GATE questions give the device data rate, per-interrupt service time and CPU clock and ask for the fraction of CPU time consumed.

- **Polling/interrupt per word:** interrupts per second = rate / word size; CPU fraction = interrupts per second × (ISR time).
- **DMA:** one setup + one completion interrupt per block, so CPU time ≈ (setup + completion ISR) per block, plus stolen cycles.
- A **bus** is characterised by width and clock: bandwidth = width × clock rate (× transfers per clock).""",
                formulas=[("CPU fraction (interrupt I/O) = (rate / word size) × ISR time", "per-word interrupts")]),
       ],
       examples=[
           Ex("CPU time for interrupt-driven I/O", "A device delivers 4-byte words at 100 KB/s (1 KB = 1000 B). Each interrupt takes 5 µs of CPU time. What fraction of the CPU is used by I/O?",
              ["Interrupts per second = 100,000 / 4 = 25,000.", "CPU time per second = 25,000 × 5 µs = 0.125 s ⇒ **12.5 %**."],
              "**12.5 %**", verify=lambda: "%.1f %%" % (100000 / 4 * 5e-6 * 100)),
           Ex("The same device with DMA", "Same device, but DMA transfers blocks of 4000 bytes. Setup plus completion interrupt costs 100 µs of CPU time per block. What fraction of the CPU is used now?",
              ["Blocks per second = 100,000 / 4000 = 25.", "CPU time = 25 × 100 µs = 2.5 ms per second ⇒ **0.25 %**."],
              "**0.25 %**", verify=lambda: "%.2f %%" % (100000 / 4000 * 100e-6 * 100)),
           Ex("Cycle stealing", "A DMA device moves 1 byte per 1 µs; each stolen cycle takes 0.2 µs of bus time. What fraction of CPU bus time is lost?",
              ["Each byte takes 1 µs, and each stolen cycle holds the bus for 0.2 µs.", "So the DMA uses 0.2 / 1 = **20 %** of the bus time; the CPU keeps 80 %."],
              "**20 %**", verify=lambda: "%d %%" % round(0.2 / 1.0 * 100)),
           Ex("Bus bandwidth", "A 64-bit bus runs at 100 MHz and transfers data on both clock edges (double data rate). What is the peak bandwidth in MB/s?",
              ["Bytes per transfer = 8; transfers per second = 2 × 100 M = 200 M.", "Bandwidth = 8 × 200 M = 1600 MB/s."],
              "**1600 MB/s**", verify=lambda: "%d MB/s" % (8 * 2 * 100)),
       ],
       traps=[("Polling cost", "Busy-waiting wastes CPU even when the device is idle."),
              ("DMA still needs interrupts", "A completion interrupt tells the CPU the block has been moved."),
              ("Trap vs interrupt", "Traps/exceptions are synchronous; hardware interrupts are asynchronous."),
              ("Cycle stealing vs burst", "Burst blocks the CPU for the whole transfer; cycle stealing interleaves.")],
       quick=[("Which method has the least CPU involvement per byte?", ["polling", "interrupt-driven I/O", "DMA", "programmed I/O"], 2, "DMA."),
              ("A vectored interrupt means the device supplies", ["the data", "the ISR address/vector", "the clock", "the stack pointer"], 1, "Vector number."),
              ("Memory-mapped I/O uses", ["special IN/OUT instructions", "ordinary load/store instructions", "DMA only", "no addresses"], 1, "Registers appear as addresses."),
              ("Cycle stealing", ["halts the CPU for the full block", "takes the bus a word at a time", "disables interrupts", "uses a separate bus"], 1, "Interleaved.")],
       summary=["Programmed I/O (polling), interrupt-driven, DMA; memory-mapped vs isolated I/O.", "Interrupt sequence: finish instruction, save PC/state, identify source, run ISR, return.", "Vectored, daisy-chain, priority and masking resolve multiple devices.",
                "DMA: CPU sets address/count; controller steals cycles or bursts; completion interrupt.", "Fraction of CPU = interrupts/s × service time.", "Bus bandwidth = width × clock × transfers per cycle."])
