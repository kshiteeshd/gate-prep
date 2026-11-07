"""Textbook-style long-form teaching text: Computer Organisation and Digital Logic."""
from learn import elab

elab("coa-instruction-addressing",
 ("How a processor runs a program", """
A processor repeats one cycle forever: **fetch** the next instruction from memory (the address is in the **program counter, PC**), **decode** it to see what it asks for, **execute** it, and update the PC. Instructions come from an **instruction set architecture (ISA)**, the contract between software and hardware.

An instruction is a binary word with fields: an **opcode** saying what to do and **operand specifiers** saying where the data is. With a $k$-bit opcode you can have $2^k$ different operations; with a register field of $r$ bits you can name $2^r$ registers. So instruction width $=$ opcode bits $+$ the sum of all operand field bits.
"""),
 ("Addressing modes", """
An **addressing mode** is a rule for turning an operand field into the actual data.

- **Immediate:** the operand *is* the data (`ADD R1, #5`).
- **Direct:** the field is the memory address of the data.
- **Indirect:** the field gives the address of a location that holds the data's address (two memory accesses).
- **Register / register indirect:** the data is in a register / the register holds the address.
- **Indexed / base + displacement:** effective address $=$ register $+$ constant; used for arrays and for local variables on the stack.
- **Relative (PC-relative):** effective address $=$ PC $+$ offset; used for branches, and it makes code relocatable.
- **Auto-increment / decrement:** the register is changed after/before use, handy for stepping through arrays.

To answer a question, compute the **effective address (EA)** first, then say what is fetched from it. Count the memory accesses: immediate needs 0 for the operand, direct 1, indirect 2.
"""),
 ("Instruction formats and types", """
Instructions can have 0, 1, 2 or 3 addresses. A **stack machine** has zero-address instructions (operands are on the stack: `ADD` pops two and pushes the sum). **RISC** machines use fixed-length instructions and only load/store touch memory; **CISC** machines have complex variable-length instructions. **Expanding opcodes** lets some instructions use fewer address bits so more opcodes fit: if 4 bits are used for 15 two-address operations leaving 1 code to extend, the extra bits can encode many one-address operations.
"""),
)

elab("coa-datapath-control-performance",
 ("The datapath and the control unit", """
The **datapath** is the hardware that moves and transforms data: registers, the **ALU** (arithmetic logic unit), buses and multiplexers. The **control unit** generates the signals that tell the datapath what to do in each step. There are two designs: **hardwired control** (logic gates and a state counter; fast but inflexible) and **microprogrammed control** (each instruction is a sequence of **micro-instructions** in a small control memory; easy to change, slower).

In a microprogrammed design, the **control word** is stored in the control memory. **Horizontal** microcode has one bit per control signal (wide, fast, no decoding); **vertical** microcode encodes signals into fields (narrow, needs decoders). A field encoding $k$ mutually exclusive signals needs $\\lceil\\log_2(k+1)\\rceil$ bits (the $+1$ covers "no signal").
"""),
 ("Measuring performance", """
The CPU time of a program is

$$T=\\frac{IC\\times CPI}{f}$$

where $IC$ is the instruction count, $CPI$ the average clock cycles per instruction and $f$ the clock frequency. Faster clock, fewer instructions, or fewer cycles per instruction all help, but changing one often hurts another (a simpler instruction set raises $IC$, for example).

**Amdahl's law.** If a fraction $F$ of the execution time is sped up by a factor $S$, the overall speedup is

$$\\text{Speedup}=\\frac{1}{(1-F)+\\dfrac{F}{S}}$$

Even with infinite $S$ the speedup cannot exceed $\\frac{1}{1-F}$: the part you did not improve limits everything.
"""),
)

elab("coa-pipelining",
 ("Overlapping instructions", """
A non-pipelined processor finishes one instruction completely before starting the next. A **pipeline** splits instruction execution into stages — say **fetch, decode, execute, memory, write-back** — and starts a new instruction every cycle, so while one instruction executes, the next is being decoded and the one after fetched, like cars on an assembly line. Pipelining does not shorten the time of a single instruction; it increases **throughput**.

For a $k$-stage pipeline with no stalls, $n$ instructions take $k+(n-1)$ cycles, so the speedup over a non-pipelined machine is $\\frac{nk}{k+n-1}$, which approaches $k$ for large $n$.
"""),
 ("Hazards", """
Things that prevent the next instruction from entering the pipeline when expected are **hazards**.

- **Structural hazard:** two instructions need the same hardware in the same cycle (e.g. one memory used for both instruction fetch and data access).
- **Data hazard:** an instruction needs a result that an earlier one has not yet produced. **RAW** (read after write) is the real, common one; WAR and WAW arise only when instructions can be reordered. Fixes: **stalling** (inserting bubbles), and **forwarding (bypassing)**, which sends a result straight from the ALU output to the next instruction's input, without waiting for write-back.
- **Control hazard:** a branch's outcome is not known until later, so instructions fetched after it may be wrong. Fixes: stall, **branch prediction**, **delayed branches**.

To count stalls, draw a pipeline diagram with one row per instruction and one column per cycle and delay any instruction that reads a register before the value is available.
"""),
 ("Performance with stalls", """
If every instruction would ideally take 1 cycle, then with an average of $s$ stall cycles per instruction, $CPI=1+s$. A branch instruction that costs a 2-cycle penalty and appears in 20% of instructions adds $0.2\\times2=0.4$ to the CPI. Deeper pipelines allow faster clocks but increase the cost of hazards and mispredicted branches.
"""),
)

elab("coa-cache-memory",
 ("Why we need a cache", """
Fast memory is small and expensive; large memory is slow and cheap. A **memory hierarchy** combines them: registers, then **cache**, then main memory, then disk. It works because of **locality**: **temporal locality** (a recently used item will likely be used again soon) and **spatial locality** (items near a recently used one will likely be used soon). A **cache** keeps copies of recently used blocks of memory.

A request that finds its data in the cache is a **hit**; otherwise a **miss**, and the block is fetched from memory. The **hit ratio** $h$ is the fraction of hits.
"""),
 ("Mapping: where can a block go?", """
Main memory is divided into **blocks** of a fixed size; the cache has **lines** of the same size. The mapping decides which lines a block may occupy.

- **Direct mapped:** block $b$ goes to line $b\\bmod C$ (where $C$ is the number of lines). Simple and fast, but two blocks that map to the same line keep evicting each other (**conflict misses**).
- **Fully associative:** a block may go in *any* line. Fewest conflicts, but every line's tag must be compared.
- **$k$-way set associative:** the cache is divided into sets of $k$ lines; a block goes to set $b\\bmod(\\text{number of sets})$ and may occupy any line of that set.

A memory address is split into **tag | index (set) | block offset**. The offset has $\\log_2(\\text{block size})$ bits, the index $\\log_2(\\text{number of sets})$ bits, and the tag is the rest. The tag is stored with each line to identify which block it currently holds.
"""),
 ("Replacement, writes and performance", """
When a set is full, a **replacement policy** picks the victim: **LRU**, **FIFO** or random. For writes: **write-through** updates both cache and memory (simple, but slow without a write buffer); **write-back** updates only the cache and marks the line **dirty**, writing it to memory only on eviction. On a write miss, **write-allocate** loads the block first; **no-write-allocate** writes directly to memory.

Misses are classified as **compulsory** (first reference), **capacity** (cache too small) and **conflict** (mapping). The **average memory access time** is

$$\\text{AMAT}=t_{\\text{hit}}+\\text{miss rate}\\times\\text{miss penalty}$$
"""),
)

elab("coa-io-interrupts-dma",
 ("Talking to devices", """
Input/output devices (disk, keyboard, network card) are far slower than the CPU and operate asynchronously. The CPU talks to them through **device controllers** with registers. There are three ways to move data.

**Programmed I/O (polling):** the CPU repeatedly checks the device's status register until it is ready. Simple, but the CPU wastes time waiting.

**Interrupt-driven I/O:** the device sends an **interrupt** signal when it is ready; the CPU finishes the current instruction, saves its state, runs an **interrupt service routine (ISR)** and then resumes. No time is wasted waiting, but each transfer of a word still costs the ISR overhead.
"""),
 ("Direct memory access", """
For large transfers, the CPU would spend all its time copying bytes. In **DMA**, a **DMA controller** moves the data between the device and memory by itself. The CPU only sets up the transfer (device, memory address, count) and is interrupted *once at the end*. During the transfer the DMA controller needs the memory bus: in **burst mode** it takes the bus for the whole block; in **cycle stealing** it takes the bus one word at a time, slowing the CPU slightly.

**Comparing overheads.** In interrupt-driven I/O at data rate $r$ bytes/s with word size $w$ bytes, there are $r/w$ interrupts per second, and the CPU fraction is $\\frac{r}{w}\\times t_{ISR}$. With DMA, the CPU cost is only the set-up plus one interrupt per block.
"""),
 ("Interrupts in detail", """
Interrupts may be **maskable** (can be disabled) or **non-maskable**; **vectored** (the device supplies the address of its ISR) or not. With several devices raising interrupts at once, a **priority** scheme (daisy chain or priority controller) picks which is served first. A **software interrupt** (trap) is raised by an instruction, such as a system call.
"""),
)

# ---------------------------------------------------------------- Digital logic
elab("dl-boolean-minimization",
 ("Boolean algebra", """
Digital circuits work with two values, 0 and 1. A **Boolean function** assigns an output to each combination of inputs. The basic operations are **AND** ($A\\cdot B$), **OR** ($A+B$) and **NOT** ($\\bar A$). **NAND** and **NOR** are **universal gates**: any circuit can be built from either alone.

The laws you need: identity ($A+0=A$, $A\\cdot1=A$), null ($A+1=1$, $A\\cdot0=0$), complement ($A+\\bar A=1$, $A\\cdot\\bar A=0$), idempotent ($A+A=A$), absorption ($A+AB=A$), and **De Morgan's laws**:

$$\\overline{A+B}=\\bar A\\cdot\\bar B\\qquad\\overline{A\\cdot B}=\\bar A+\\bar B$$

The **dual** of an identity is obtained by swapping AND with OR and 0 with 1; it is also true.
"""),
 ("Canonical forms and minimisation", """
A **minterm** is an AND of all variables (each complemented or not) that is 1 for exactly one input combination; a **maxterm** is an OR that is 0 for exactly one combination. A function is written as a **sum of minterms** ($\\sum m$) or **product of maxterms** ($\\prod M$). A function of $n$ variables has $2^n$ minterms and $2^{2^n}$ possible functions.

To make a circuit cheaper we **minimise** the expression. A **Karnaugh map (K-map)** arranges the minterms in a grid where neighbouring cells differ in one variable (Gray code order). Circle groups of 1s of size 1, 2, 4, 8, … (powers of two, rectangular, wrapping at edges), as large as possible. Each group becomes one product term in which the variables that change inside the group drop out. **Don't-care** conditions (inputs that never occur) can be treated as 0 or 1, whichever makes bigger groups.
"""),
 ("Prime implicants", """
An **implicant** is a product term covering only 1s of the function. A **prime implicant** cannot be enlarged. An **essential prime implicant** is the only one covering some minterm, so it *must* appear in the minimal expression. The Quine–McCluskey method finds prime implicants by repeatedly combining minterms that differ in one bit, then picks a smallest set covering all minterms.
"""),
)

elab("dl-combinational-circuits",
 ("Circuits without memory", """
In a **combinational circuit** the output depends only on the *current* inputs; there is no memory. Several standard building blocks appear in exams.

**Half adder:** adds two bits: $\\text{Sum}=A\\oplus B$, $\\text{Carry}=AB$. **Full adder:** adds two bits and a carry-in: $\\text{Sum}=A\\oplus B\\oplus C_{in}$, $C_{out}=AB+C_{in}(A\\oplus B)$. Chaining $n$ full adders gives a **ripple-carry adder**, whose delay grows with $n$ because each carry waits for the previous. A **carry-lookahead adder** computes carries in parallel using **generate** $g_i=A_iB_i$ and **propagate** $p_i=A_i\\oplus B_i$ signals: $C_{i+1}=g_i+p_iC_i$.
"""),
 ("Multiplexers, decoders and encoders", """
A **multiplexer (MUX)** with $n$ select lines chooses one of $2^n$ data inputs to send to the output. A $2^n$-to-1 MUX can implement **any** function of $n+1$ variables (use $n$ variables as selects and feed $0$, $1$, the last variable or its complement into the data inputs); a $4$-to-$1$ MUX implements any 3-variable function.

A **decoder** with $n$ inputs has $2^n$ outputs, exactly one active; it generates all minterms, so a function can be built with a decoder plus an OR gate. An **encoder** does the reverse. A **demultiplexer** routes one input to one of $2^n$ outputs. A **comparator** compares two numbers; a **priority encoder** outputs the index of the highest active input.
"""),
 ("Hazards and delay", """
Gate delays can cause brief wrong output values called **hazards** (glitches). A **static-1 hazard** occurs when an output that should stay at 1 dips to 0 for a moment; it can be removed by adding a redundant product term covering the transition in the K-map. The **critical path** is the longest delay from any input to the output and sets the clock speed of the circuit it belongs to.
"""),
)

elab("dl-number-systems",
 ("Writing numbers in other bases", """
A **base-$b$ number** uses digits $0..b-1$; the digit in position $i$ (counting from 0 on the right) has weight $b^i$. So $1011_2=1\\cdot8+0\\cdot4+1\\cdot2+1=11$. To convert a decimal integer to base $b$, divide repeatedly by $b$ and read the remainders from last to first. For a fraction, multiply repeatedly by $b$ and read the integer parts. Binary $\\leftrightarrow$ octal and binary $\\leftrightarrow$ hex are done by grouping bits in threes and fours.
"""),
 ("Representing negative numbers", """
- **Sign–magnitude:** one sign bit plus the magnitude. Two zeros ($+0$ and $-0$).
- **One's complement:** negate by flipping all bits. Still two zeros.
- **Two's complement:** negate by flipping all bits and adding 1. One zero, and addition works the same for signed and unsigned numbers. This is what real machines use.

For $n$ bits the range of two's complement is $-2^{n-1}$ to $2^{n-1}-1$ (one more negative value than positive). To find the value of a negative two's-complement number, take its two's complement again and put a minus sign. **Sign extension** copies the sign bit into the new high bits.

**Overflow** in signed addition occurs exactly when the two operands have the same sign but the result has a different sign (equivalently, the carry into the sign bit differs from the carry out).
"""),
 ("BCD and codes", """
**BCD** stores each decimal digit in 4 bits ($47_{10}=0100\\,0111$). **Gray code** changes only one bit between consecutive numbers (used in K-maps and position encoders). A **parity bit** detects single-bit errors; a **Hamming code** with $r$ check bits can correct a single error if $2^r\\ge m+r+1$ for $m$ data bits.
"""),
)

elab("dl-floating-point",
 ("Why floating point", """
Fixed-point numbers cannot represent both very large and very small values in a fixed number of bits. **Floating point** works like scientific notation: a number is $\\pm\\,\\text{mantissa}\\times2^{\\text{exponent}}$. The **IEEE 754** standard fixes the layout.

**Single precision (32 bits):** 1 sign bit, 8 exponent bits (bias 127), 23 fraction bits. **Double precision (64 bits):** 1 sign, 11 exponent (bias 1023), 52 fraction.
"""),
 ("Decoding an IEEE 754 number", """
For a *normalised* number the stored exponent field $E$ is between 1 and 254 (single), and

$$\\text{value}=(-1)^{s}\\times1.f\\times2^{E-127}$$

The leading 1 is **implied** (not stored), giving an extra bit of precision. Special cases: $E=0$ with $f=0$ is zero; $E=0$ with $f\\ne0$ is a **denormalised** number (value $0.f\\times2^{-126}$) that fills the gap near zero; $E=255$ with $f=0$ is $\\pm\\infty$; $E=255$ with $f\\ne0$ is **NaN**.

*Example.* $-6.5=-110.1_2=-1.101\\times2^2$. Sign 1, exponent $2+127=129=10000001_2$, fraction $101000\\dots0$.
"""),
 ("Precision and rounding", """
Most decimal fractions (like 0.1) have no exact binary representation, so floating-point arithmetic is approximate and the order of operations can change results. Adding a very small number to a very large one may lose the small one completely. The standard rounding mode is **round to nearest, ties to even**. The gap between neighbouring representable numbers grows with the magnitude of the number.
"""),
)

elab("dl-sequential-circuits",
 ("Circuits with memory", """
A **sequential circuit** has memory: its output depends on the inputs *and* on the stored state. The basic memory element is the **flip-flop**, which stores one bit and changes only at a clock edge.

- **SR:** set/reset; $S=R=1$ is forbidden.
- **D:** $Q^+=D$; simply copies the input.
- **JK:** like SR but $J=K=1$ toggles; $Q^+=J\\bar Q+\\bar KQ$.
- **T:** $Q^+=T\\oplus Q$; toggles when $T=1$.

A **latch** is level-sensitive, whereas a **flip-flop** is edge-triggered.
"""),
 ("Counters and registers", """
A **register** is a group of flip-flops holding a word; a **shift register** moves bits one position per clock. A **counter** cycles through a sequence of states. A **ripple (asynchronous) counter** chains flip-flops so each clocks the next (simple, but delays add up); a **synchronous counter** clocks all flip-flops together. A **mod-$N$ counter** needs $\\lceil\\log_2N\\rceil$ flip-flops. A **ring counter** with $n$ flip-flops has $n$ states; a **Johnson (twisted-ring) counter** has $2n$.
"""),
 ("Analysing a state machine", """
A **finite-state machine** is described by a **state table** (next state and output for each state and input). In a **Moore** machine the output depends only on the state; in a **Mealy** machine it depends on the state and the input. To analyse a circuit, write the flip-flop input equations, build the excitation and state tables, and trace the state sequence. **Timing:** the clock period must exceed the flip-flop delay plus the longest combinational path plus the **setup time**; **hold time** is the interval after the clock edge during which the input must stay stable.
"""),
)
