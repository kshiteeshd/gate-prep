"""Concept notes, part B: COA, DBMS, DL."""
from content.notes_a import n, N  # noqa: F401  (shared registry)

# ---------------- COA ----------------
n("COA", "AMAT", "Average memory access time: AMAT = hit time + miss rate × miss penalty; for two levels AMAT = H₁ + m₁(H₂ + m₂·Pₘₑₘ), with m₂ the local miss rate of L2.",
  "Work outward from the last level: compute the L2 average, plug it in as the L1 miss penalty, then add the L1 hit time.",
  "Use local miss rates for each level consistently, or the global rate with the right product.")
n("COA", "Cache address breakdown", "A physical address splits into tag | index | offset. Offset bits = log₂(block size), index bits = log₂(number of sets), tag = the rest. Direct-mapped: sets = lines; k-way: sets = lines/k.",
  "Compute the number of lines = cache size / block size, sets = lines / associativity, then subtract index and offset bits from the address width for the tag.",
  "Fully associative caches have no index bits; tag size grows with associativity.")
n("COA", "Cache simulation", "Simulate the cache: each reference maps to a set; a hit needs a matching tag, a miss loads the block and may evict by the replacement policy (LRU/FIFO).",
  "Convert addresses to block numbers, track set contents and recency, mark hit or miss for every access.",
  "Count compulsory, capacity and conflict misses separately if asked; block numbers, not byte addresses, decide the set.")
n("COA", "Main memory", "Main memory is organised in banks/words; capacity = words × bits per word; the address needs ⌈log₂ words⌉ bits; interleaving lets consecutive blocks be fetched from different banks.",
  "Translate sizes to powers of two, derive address and data line widths, and compute bandwidth as words per cycle.",
  "Address bits depend on addressable units (byte vs word).")
n("COA", "CPU performance", "CPU time = instruction count × CPI × clock cycle time; speedup = old time / new time; Amdahl: S = 1 / ((1 − f) + f/s).",
  "Write the performance equation for both machines, change only the stated factor, and take the ratio.",
  "A higher clock rate does not mean higher performance if CPI worsens; MIPS can mislead.")
n("COA", "Microprogrammed control", "Microprogrammed control stores control words in a control memory; horizontal microcode has wide words (one bit per control signal), vertical microcode encodes signals and needs decoders.",
  "Count signals for horizontal width; for vertical encode groups of mutually exclusive signals with ⌈log₂(k+1)⌉ bits.",
  "Control-store size = number of microinstructions × width.")
n("COA", "DMA & interrupts", "DMA moves a block between memory and a device with the CPU only starting and finishing the transfer; cycle stealing takes bus cycles from the CPU. Interrupt latency and handling time determine overhead.",
  "Compute transfer time (size / rate), the fraction of cycles the CPU loses, and compare with programmed I/O or interrupt-driven I/O.",
  "In burst mode the CPU is blocked for the whole transfer; in cycle stealing it loses one cycle per word.")
n("COA", "I/O transfer methods", "Programmed I/O polls the device; interrupt-driven I/O interrupts the CPU per transfer; DMA transfers blocks without the CPU. CPU utilisation increases in that order.",
  "Compute cycles spent per byte for each method and compare the fraction of CPU time consumed.",
  "Polling wastes cycles waiting; interrupts cost context-switch overhead per transfer.")
n("COA", "Addressing modes", "Immediate (operand in instruction), direct (address in instruction), indirect (address of address), register, register indirect, indexed, base-register, PC-relative. Effective address EA defines where the operand lives.",
  "Compute EA for the stated mode, then count memory references: immediate 0, register 0, direct 1, indirect 2 (1 pointer read + 1 operand).",
  "Relative addressing adds the updated PC, usually the address of the next instruction.")
n("COA", "Endianness", "Little-endian stores the least significant byte at the lowest address; big-endian stores the most significant byte first.",
  "Write the bytes of the word in significance order and place them in memory order for the stated convention.",
  "Bits within a byte are not reordered; only byte order changes.")
n("COA", "Expanding opcodes", "An expanding opcode scheme reuses unused opcode patterns of shorter instructions as prefixes for longer-format instructions, fitting more instructions into a fixed length.",
  "Count total codes (2^bits), subtract those used by the first format, multiply the remaining prefixes by the next format's address-field combinations.",
  "Each format's free patterns must be counted after reserving codes for the extension.")
n("COA", "Instruction encoding", "An instruction word contains opcode, mode and operand fields; the word length determines how many instructions and registers can be encoded: bits = opcode + fields.",
  "Sum the field widths needed (⌈log₂ count⌉ for each) and compare with the instruction length.",
  "Remember the mode bits and any immediate field.")
n("COA", "Dependences", "Data hazards arise from RAW (true), WAR and WAW (name) dependences; control hazards come from branches; structural hazards from resource conflicts.",
  "List each instruction's reads and writes and compare pairs for the dependence type.",
  "Only RAW causes stalls in an in-order five-stage pipeline without forwarding gaps; WAR/WAW arise with out-of-order execution.")
n("COA", "Hazards (cycle-accurate)", "In a five-stage pipeline a dependent instruction must read its operand after the producer writes it; without forwarding stalls are 2–3 cycles, with forwarding a load-use still costs 1.",
  "Draw the pipeline diagram cycle by cycle, inserting stalls until each read follows the needed write.",
  "Register-file write in the first half and read in the second half of a cycle can remove one stall.")
n("COA", "Pipeline speedup", "Ideal speedup of a k-stage pipeline approaches k; with n instructions time = (k + n − 1) cycles, versus n·k unpipelined. Stalls reduce speedup to k / (1 + stall cycles per instruction).",
  "Compute pipelined and non-pipelined times and divide; include stalls as extra cycles.",
  "Unequal stage delays: the clock must fit the slowest stage plus latch overhead.")
for t in ("Cache & Memory Hierarchy", "Datapath & Control Unit", "I/O, Interrupts & DMA", "Instruction Formats & Addressing Modes", "Pipelining"):
    n("COA", "Concepts", "Computer organisation links instruction set, datapath, memory hierarchy and I/O; performance trade-offs come from latency, bandwidth and hit rates.",
      "Identify which component the statement concerns and recall its defining equation or rule.",
      "Do not mix up latency and throughput, or hit time and miss penalty.", topic=t)

# ---------------- DBMS ----------------
n("DBMS", "Cardinality", "ER cardinality (1:1, 1:N, M:N) constrains how many entities relate; participation can be total or partial. M:N relationships need their own relation.",
  "Read the constraint from each side to get the ratio; then decide keys (1:N: key of the N side).",
  "Total participation uses a double line; cardinality is read towards the other entity.")
n("DBMS", "ER to relational", "Map entities to tables with their keys, M:N relationships to tables with both keys, and 1:N relationships by adding the foreign key to the N side; weak entities include the owner's key.",
  "Count entity tables plus separate relationship tables (only where needed) to get the number of relations.",
  "Merge a 1:1 or 1:N relationship into an existing table to reduce the count.")
n("DBMS", "Closure & keys", "The closure X⁺ is the set of attributes determined by X using the FDs; X is a superkey if X⁺ contains all attributes and a candidate key if no proper subset does.",
  "Start with X, repeatedly add right sides of FDs whose left side is contained, until nothing changes. Attributes never on any right side must be in every key.",
  "A candidate key is minimal; the number of superkeys grows with every extra attribute added to keys.")
n("DBMS", "Decomposition", "A decomposition must be lossless (no spurious tuples) and ideally dependency-preserving. A binary decomposition R → R₁, R₂ is lossless iff R₁ ∩ R₂ → R₁ or R₂.",
  "Test losslessness with the intersection rule (or the chase for more relations) and dependency preservation by checking each FD lies within a projected relation (or its closure).",
  "A lossless decomposition may still lose dependencies; 3NF always has a lossless dependency-preserving decomposition, BCNF not always.")
n("DBMS", "FD theory", "Armstrong's axioms (reflexivity, augmentation, transitivity) are sound and complete; a canonical cover has single-attribute right sides, no extraneous attributes and no redundant FDs.",
  "Derive consequences with the axioms; to minimise, remove extraneous attributes and redundant FDs one at a time.",
  "Check redundancy using closures with the FD removed.")
n("DBMS", "Normal forms", "1NF: atomic values. 2NF: no partial dependency on part of a key. 3NF: for every FD X→A, X is a superkey or A is prime. BCNF: every determinant is a superkey.",
  "Find the candidate keys, list prime attributes, and test each FD against the 2NF/3NF/BCNF conditions; the highest satisfied form is the answer.",
  "BCNF ⊂ 3NF ⊂ 2NF ⊂ 1NF; a relation with only prime attributes is in 3NF.")
n("DBMS", "B+ trees", "In a B+ tree of order p every node holds up to p−1 keys; leaves are linked, data pointers sit in leaves, and all leaves are at the same depth. Height ≈ ⌈log_fanout N⌉.",
  "Compute fanout from block size, key and pointer sizes, then the maximum keys per level or the number of levels for N records.",
  "Minimum occupancy of internal nodes is ⌈p/2⌉ children; splitting promotes (internal) or copies (leaf) the middle key.")
n("DBMS", "Blocks & index sizes", "Blocking factor = ⌊block size / record size⌋; file blocks = ⌈records / blocking factor⌉. Dense index: one entry per record; sparse index: one per block.",
  "Compute record counts, blocks, then index entries and index blocks; a binary search over b blocks needs ⌈log₂ b⌉ accesses.",
  "Round at every step (floor for records per block, ceil for blocks).")
n("DBMS", "Hashing & file organization", "Static hashing maps keys to buckets by h(k); extendible and linear hashing grow the directory or bucket set dynamically. Heap files give O(n) search, sorted files O(log n), hashed files O(1) expected.",
  "Compute the cost in block accesses for the access pattern (equality vs range) on each organisation.",
  "Hashing does not support range queries efficiently.")
n("DBMS", "Operator results", "Relational algebra operators: σ (select rows), π (project columns, removes duplicates), ⋈ (join), ∪, ∩, − (set operations), ÷ (division), ρ (rename).",
  "Evaluate step by step on the given instances, remembering that results are sets (no duplicate tuples).",
  "Division returns tuples related to every tuple of the divisor; natural join matches on all common attributes.")
n("DBMS", "Size bounds", "Result sizes bound by operator: |σ| ≤ |R|; |R ⋈ S| ≤ |R|·|S| (cross product) and at least 0; for union max(|R|,|S|) ≤ |R ∪ S| ≤ |R|+|S|; projection never increases rows.",
  "Find the extremes by choosing instances (all keys equal / all distinct) that maximise or minimise the result.",
  "A foreign-key join returns at most |R| tuples; NULLs never match in a join.")
n("DBMS", "Aggregates", "SQL aggregates (COUNT, SUM, AVG, MIN, MAX) ignore NULLs except COUNT(*); GROUP BY forms groups, HAVING filters groups after aggregation, WHERE before.",
  "Evaluate the query in logical order: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY.",
  "AVG over zero non-NULL values is NULL; COUNT(col) skips NULLs.")
n("DBMS", "Query results", "Evaluate SQL logically: FROM/JOIN, WHERE, GROUP BY, HAVING, SELECT, DISTINCT, ORDER BY. NULL comparisons are UNKNOWN, so they fail WHERE; IN/NOT IN and outer joins have special NULL behaviour.",
  "Work through the tables row by row following the logical order and note where NULLs appear.",
  "NOT IN with a NULL in the subquery returns no rows; COUNT(*) counts NULL rows, COUNT(col) does not.")
n("DBMS", "Counting schedules", "The number of interleavings of transactions with n₁, n₂, … operations is (Σ nᵢ)! / Π nᵢ! (order within each transaction fixed).",
  "Apply the multinomial formula; for serial schedules count the n! orders of transactions.",
  "Only conflict-equivalent schedules count as the same serial order, not every interleaving.")
n("DBMS", "Recoverability", "Schedule classes: Strict ⊂ ACA (cascadeless) ⊂ Recoverable. Recoverable: a transaction commits only after every transaction it read from commits; ACA: reads only committed values; strict: no read or write of uncommitted data.",
  "For each read of a value written by an uncommitted transaction, check that the writer commits before the reader commits (recoverable) and whether such reads exist at all (ACA).",
  "Serializable does not imply recoverable; recoverability concerns commit order.")
n("DBMS", "Serializability", "A schedule is conflict-serializable iff its precedence graph is acyclic; edges Tᵢ → Tⱼ come from conflicting operations (R-W, W-R, W-W on the same item) of different transactions with Tᵢ first.",
  "List the conflicting pairs, draw the graph and test for cycles; an acyclic graph's topological order is an equivalent serial schedule.",
  "View-serializable schedules can exist that are not conflict-serializable (blind writes).")
n("DBMS", "Timestamp ordering", "Basic timestamp ordering assigns each transaction a timestamp; a read of X is rejected if TS < W-ts(X), a write if TS < R-ts(X) or TS < W-ts(X) (Thomas's write rule ignores obsolete writes).",
  "Track R-ts and W-ts of each item and process operations in schedule order, aborting violators.",
  "Rejected transactions restart with a new timestamp.")
n("DBMS", "Concurrency facts", "Two-phase locking guarantees conflict-serializability; strict 2PL also guarantees strictness; 2PL can deadlock, timestamp ordering cannot.",
  "Recall the property guaranteed by each protocol and the price paid (deadlock, abort).",
  "2PL does not prevent deadlock; conservative 2PL does.")
n("DBMS", "Aggregates", "SQL aggregates (COUNT, SUM, AVG, MIN, MAX) ignore NULLs except COUNT(*); GROUP BY forms groups, HAVING filters groups.",
  "Evaluate in logical order and treat NULLs carefully.",
  "AVG of an empty/NULL-only group is NULL.")
for t in ("ER Model", "Functional Dependencies & Normalization", "Indexing & File Organization", "Relational Algebra & Calculus", "SQL", "Transactions & Concurrency"):
    n("DBMS", "Concepts", "Database design moves from conceptual (ER) to relational schema, normalised to avoid anomalies, queried with relational algebra/SQL and protected by transactions.",
      "Identify the layer of the problem (design, query, storage, concurrency) and apply its definition.",
      "Mixing up superkey, candidate key and primary key is the classic slip.", topic=t)

# ---------------- DL ----------------
n("DL", "Boolean identities", "Boolean algebra laws: De Morgan (AB)' = A' + B', (A + B)' = A'B'; absorption A + AB = A; consensus AB + A'C + BC = AB + A'C; XOR: A ⊕ B = AB' + A'B.",
  "Apply identities to simplify, or compare truth tables when in doubt.",
  "Complementing both a function and its inputs (duality) is not the same as De Morgan.")
n("DL", "Gates", "NAND and NOR are universal gates; XOR outputs 1 when inputs differ, XNOR when equal; every function can be built from NAND alone.",
  "Rewrite the function with the target gate using De Morgan, counting gates.",
  "A NAND with tied inputs is an inverter.")
n("DL", "K-map / Quine-McCluskey", "A K-map groups adjacent minterms (powers of two, wrapping around edges) to find minimal sum-of-products; prime implicants cover groups, essential prime implicants cover a minterm no other group does.",
  "Mark minterms and don't-cares, form the largest groups, pick essential prime implicants first, then cover the rest with as few terms as possible.",
  "Don't-cares may be used to enlarge groups but need not be covered.")
n("DL", "Minterms & functions", "A function of n variables has 2ⁿ minterms and 2^(2ⁿ) distinct truth tables; a minterm is true for exactly one input combination.",
  "Translate the description to a list of minterm indices (in binary order) or to a count.",
  "Maxterms index the rows where the function is 0.")
n("DL", "Adders", "A half adder computes sum = A ⊕ B, carry = AB; a full adder computes sum = A ⊕ B ⊕ Cᵢₙ and carry = AB + Cᵢₙ(A ⊕ B).",
  "Evaluate the sum and carry for the given inputs bit by bit, propagating carries.",
  "An n-bit ripple-carry adder has delay proportional to n.")
n("DL", "Adders & arithmetic circuits", "Subtraction is addition of the two's complement: A − B = A + B' + 1. Overflow in two's complement occurs when the carries into and out of the sign bit differ.",
  "Perform bitwise addition with carries (or complement and add), then check overflow from the sign bits.",
  "Unsigned subtraction produces a borrow, not an overflow flag.")
n("DL", "MUX / Decoder", "A 2ⁿ:1 multiplexer has n select lines and implements any n-variable function when inputs are tied to constants; an n-to-2ⁿ decoder generates all minterms.",
  "Use a MUX with n−1 selects and the last variable (or its complement) as data inputs, or OR the decoder outputs for the minterms.",
  "A 4:1 MUX implements any 3-variable function with the third variable on the data lines.")
n("DL", "SOP cost from minimisation", "The cost of a minimal sum-of-products is counted in product terms and literals after Karnaugh minimisation.",
  "Minimise, then count AND gates (terms with ≥ 2 literals), the OR gate, and inverters as the question specifies.",
  "Shared terms count once; complemented literals may need extra inverters.")
n("DL", "Base conversion", "To convert between bases, expand positional weights (Σ dᵢ·bⁱ) for decimal, divide repeatedly for the target base, and group bits for octal (3) and hex (4).",
  "Convert to decimal if needed, then repeatedly divide (integer part) or multiply (fractional part).",
  "Read remainders from last to first; fractions may not terminate.")
n("DL", "IEEE 754", "Single precision: 1 sign bit, 8-bit exponent with bias 127, 23-bit mantissa with an implicit leading 1: value = (−1)^s × 1.m × 2^(e−127). Double: 11-bit exponent with bias 1023, 52-bit mantissa.",
  "Normalise the number to 1.m × 2ᵏ, add the bias to k, and write sign | exponent | mantissa.",
  "Exponent all-zeros denotes zero/denormals and all-ones infinity/NaN.")
n("DL", "Two's complement", "In n-bit two's complement the range is −2ⁿ⁻¹ … 2ⁿ⁻¹ − 1; negate by inverting all bits and adding 1; sign extension replicates the sign bit.",
  "Interpret the MSB as −2ⁿ⁻¹ and add the remaining bits' weights, or negate to read negative values.",
  "There is one more negative than positive number; −(−2ⁿ⁻¹) overflows.")
n("DL", "Number facts", "Number-representation facts: n bits represent 2ⁿ values; BCD uses 4 bits per decimal digit; Gray code changes one bit between consecutive values; signed-magnitude has two zeros.",
  "Recall the definition of the representation and test it on the stated value.",
  "Different representations share bit patterns but not meanings.")
n("DL", "Counters & registers", "An n-bit ripple counter cycles through 2ⁿ states; a mod-N counter resets at N; shift registers shift data one bit per clock (ring counter N states, Johnson 2N states).",
  "Simulate the state sequence for the clock pulses and read the final value, or compute the modulus from the reset condition.",
  "Asynchronous counters accumulate propagation delay; synchronous ones share one clock.")
n("DL", "Flip-flops", "SR, JK, D and T flip-flops: D copies the input, T toggles when T = 1, JK toggles on J = K = 1; characteristic equations: Q⁺ = D, Q⁺ = T ⊕ Q, Q⁺ = JQ' + K'Q.",
  "Apply the characteristic equation for each clock edge.",
  "SR has an invalid input S = R = 1; JK resolves it by toggling.")
n("DL", "Timing & FSM", "A finite state machine has next-state logic and a register; the clock period must exceed clock-to-Q + logic delay + setup time, and hold time constraints limit minimum delays.",
  "Add the delays along the critical path to get the minimum clock period and f = 1/T.",
  "Moore outputs depend only on state; Mealy outputs also depend on inputs.")
for t in ("Boolean Algebra & Minimization", "Combinational Circuits", "Number Systems & Arithmetic", "Sequential Circuits"):
    n("DL", "Concepts", "Digital logic builds circuits from Boolean functions: combinational blocks compute outputs from current inputs, sequential blocks add memory (flip-flops).",
      "Write the Boolean function or the state table, then reason with identities or simulation.",
      "Check whether the circuit has memory before treating it as combinational.", topic=t)
