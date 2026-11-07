"""COA + Digital Logic — curated concept questions."""
from content.kit import C

# ===================== COA =====================
C("COA", "Instruction Formats & Addressing Modes", "Concepts", [
    ("e", 1, "s", "Which addressing mode makes it easy to write position-independent code?", ["PC-relative", "Absolute (direct)", "Immediate", "Register direct"], 0, "Offsets from the PC remain valid wherever the code is loaded."),
    ("e", 1, "s", "Accessing the elements of an array in a loop is most naturally supported by", ["indexed addressing", "immediate addressing", "implied addressing", "direct addressing only"], 0, "EA = base + index."),
    ("e", 1, "s", "In immediate addressing, the operand is", ["contained in the instruction itself", "in a register", "at the address given in the instruction", "on top of the stack"], 0, "No extra memory access for the operand."),
    ("m", 2, "m", "Which are typical characteristics of a RISC architecture? (select all)", ["Fixed-length instructions", "Load/store architecture", "Hardwired control unit", "Many complex memory addressing modes", "Heavily microprogrammed control"], [0, 1, 2], "CISC typically has variable length instructions, many modes and microcode."),
    ("m", 1, "s", "A zero-address instruction format is typical of", ["stack machines", "accumulator machines", "load/store machines", "VLIW machines"], 0, "Operands are implicitly on the stack."),
    ("m", 2, "s", "Register indirect addressing needs how many memory accesses to fetch the operand (excluding instruction fetch)?", ["1", "0", "2", "3"], 0, "The register supplies the address; one read gets the operand."),
    ("h", 2, "s", "Which of the following addressing modes requires the MOST memory references to access an operand?", ["Memory indirect", "Direct", "Register indirect", "Indexed"], 0, "Memory indirect needs 2 data-memory references (pointer, then operand)."),
    ("m", 1, "s", "The base-register addressing mode is chiefly useful for", ["program relocation", "loop counters", "constants", "stack operations only"], 0, "Changing the base moves the whole program."),
    ("m", 1, "s", "Auto-increment addressing is helpful for", ["stepping through arrays / implementing stacks", "branching", "constants", "I/O ports only"], 0, "The register is incremented after each access."),
])

C("COA", "Datapath & Control Unit", "Concepts", [
    ("e", 1, "s", "Compared with a microprogrammed control unit, a hardwired control unit is generally", ["faster but less flexible", "slower and easier to modify", "cheaper for complex ISAs", "unable to run pipelined code"], 0, "Microcode is slower but easy to change."),
    ("m", 1, "s", "In horizontal microprogramming the microinstruction", ["has one bit per control signal and can specify many parallel micro-operations", "encodes signals into few fields requiring decoders", "is always narrower than vertical", "cannot control the ALU"], 0, "Vertical microcode is narrower but needs decoding."),
    ("m", 2, "s", "Booth's multiplication algorithm is especially efficient when the multiplier has", ["long runs of 1s", "alternating 0s and 1s", "only zeros", "a negative sign only"], 0, "A run of 1s is replaced by one subtraction and one addition."),
    ("m", 1, "s", "The MDR (memory data register) holds", ["the word being read from or written to memory", "the address of the next instruction", "the opcode", "status flags"], 0, "MAR holds the address."),
    ("m", 1, "s", "The overflow flag in an ALU is set when", ["a signed arithmetic result cannot be represented in the available bits", "a carry comes out of the MSB for unsigned numbers", "the result is zero", "the result is negative"], 0, "Carry flag handles unsigned overflow."),
    ("h", 2, "s", "For a processor with an instruction fetch followed by decode, operand fetch, execute and write-back, the 'cycle stealing' technique is used by", ["DMA controllers", "pipeline stalls", "branch predictors", "cache controllers"], 0, "DMA takes bus cycles when the CPU is not using the bus."),
    ("m", 1, "s", "Amdahl's law states that the speedup from improving part of a system is limited by", ["the fraction of time that part is used", "the clock frequency", "the number of registers", "the pipeline depth"], 0, "Overall speedup = 1/((1 − f) + f/s)."),
    ("h", 2, "s", "Which of the following reduces CPU execution time T = IC × CPI / f?", ["Improving any one of IC, CPI, or clock frequency while others remain unchanged", "Only increasing the clock frequency", "Only reducing instruction count", "Only reducing CPI"], 0, "Execution time depends on all three factors."),
])

C("COA", "Pipelining", "Concepts", [
    ("e", 1, "s", "A structural hazard occurs when", ["two instructions need the same hardware resource in the same cycle", "an instruction needs a result not yet produced", "a branch changes the PC", "an interrupt arrives"], 0, "E.g., a single memory port used for IF and MEM."),
    ("e", 1, "s", "A RAW (read-after-write) hazard is a type of", ["data hazard", "structural hazard", "control hazard", "cache miss"], 0, "The second instruction reads a register before the first writes it."),
    ("m", 1, "s", "Data forwarding (bypassing) can eliminate stalls for", ["ALU-to-ALU dependencies", "all load-use dependencies", "branch hazards", "structural hazards"], 0, "A load-use dependency still costs one stall cycle in the classic pipeline."),
    ("m", 2, "m", "Which techniques reduce the penalty of control hazards? (select all)", ["Branch prediction", "Delayed branches", "Branch target buffer", "Forwarding"], [0, 1, 2], "Forwarding addresses data hazards."),
    ("m", 1, "s", "Pipelining improves", ["instruction throughput", "the latency of a single instruction", "the cycle time of each stage to zero", "memory capacity"], 0, "Latency of one instruction does not decrease (may increase slightly)."),
    ("h", 2, "s", "WAR and WAW hazards occur in", ["out-of-order execution pipelines", "in-order 5-stage pipelines with a single write stage", "single-cycle processors", "microprogrammed control only"], 0, "In an in-order pipeline writes happen in program order at WB."),
    ("h", 2, "s", "Increasing the number of pipeline stages generally", ["raises the clock frequency but increases hazard penalties", "lowers the clock frequency", "removes hazards", "reduces the CPI below 1 on scalar machines"], 0, "Deeper pipelines have shorter stages but costlier flushes."),
    ("m", 2, "s", "A superscalar processor", ["issues more than one instruction per cycle using multiple functional units", "executes one instruction per cycle", "uses only microcode", "has no pipeline"], 0, "CPI can drop below 1."),
])

C("COA", "Cache & Memory Hierarchy", "Concepts", [
    ("e", 1, "s", "Which of the following misses can be eliminated by making a cache fully associative (same capacity)?", ["Conflict misses", "Compulsory misses", "Capacity misses", "Coherence misses"], 0, "Conflict misses come from limited associativity."),
    ("e", 1, "s", "Compulsory (cold) misses are caused by", ["the first access to a block", "cache size limits", "mapping conflicts", "invalidations"], 0, "Prefetching or larger blocks reduce them."),
    ("m", 1, "s", "In a write-back cache a line is written to memory", ["when it is evicted while dirty", "on every store", "only at program end", "on every load"], 0, "A dirty bit tracks modification."),
    ("m", 1, "s", "Write-through caches generally", ["generate more memory traffic but keep memory up to date", "use a dirty bit", "never need write buffers", "have lower miss rates always"], 0, "Write buffers hide the latency."),
    ("m", 2, "s", "Increasing the block size (keeping cache size constant) typically", ["reduces compulsory misses up to a point but can increase conflict misses and miss penalty", "always reduces the miss rate", "removes the need for tags", "reduces the hit time to zero"], 0, "There is a U-shaped miss-rate curve."),
    ("m", 1, "s", "Spatial locality is exploited by", ["bringing in whole blocks on a miss", "LRU replacement", "write-back", "TLBs only"], 0, "Neighbouring words are fetched together."),
    ("h", 2, "s", "A direct-mapped cache has", ["exactly one possible location for each memory block", "the highest associativity", "no index bits", "no tag bits"], 0, "Hence conflicts, but fast hit time."),
    ("h", 2, "m", "Which statements about DRAM and SRAM are TRUE? (select all)", ["SRAM is faster and more expensive per bit", "DRAM needs periodic refresh", "Caches are usually built with SRAM", "DRAM uses six transistors per bit"], [0, 1, 2], "A DRAM cell uses one transistor and one capacitor."),
    ("h", 2, "s", "Memory interleaving improves", ["bandwidth for sequential accesses by overlapping module access times", "the capacity of a single module", "the read latency of a single word", "the cache hit rate"], 0, "Consecutive words come from different modules."),
    ("h", 2, "s", "In a physically-indexed, physically-tagged cache, the TLB lookup", ["must complete before the cache can be accessed", "can be skipped on hits", "is done in parallel for the tag only", "is not needed"], 0, "VIPT designs overlap the TLB with the index."),
])

C("COA", "I/O, Interrupts & DMA", "Concepts", [
    ("e", 1, "s", "In memory-mapped I/O", ["device registers are accessed with ordinary load/store instructions", "special I/O instructions are required", "devices have separate address buses", "DMA is impossible"], 0, "Part of the address space is assigned to devices."),
    ("m", 1, "s", "DMA transfers data between", ["a device and memory without CPU intervention per word", "CPU registers and cache", "two registers", "memory and the ALU"], 0, "The CPU only programs the DMA controller."),
    ("m", 1, "s", "In burst mode DMA", ["the controller holds the bus for the whole block transfer", "it steals one cycle at a time", "it never uses the bus", "the CPU supplies data"], 0, "Cycle stealing interleaves with CPU bus use."),
    ("m", 2, "s", "A vectored interrupt means the device", ["supplies the address (vector) of its service routine", "is polled by software", "uses DMA", "cannot be masked"], 0, "Reduces interrupt latency."),
    ("m", 1, "s", "Compared with programmed I/O, interrupt-driven I/O", ["frees the CPU from busy waiting", "is always faster for high data rates", "needs no hardware support", "uses DMA"], 0, "For high data rates DMA is better."),
    ("h", 2, "s", "A non-maskable interrupt (NMI) is typically used for", ["critical events such as power failure or hardware errors", "keyboard input", "timer ticks only", "software traps"], 0, "It cannot be disabled by the CPU."),
    ("h", 2, "s", "Daisy-chaining of interrupt requests", ["gives priority by physical position in the chain", "gives equal priority to all devices", "needs a separate wire per device", "disables nesting"], 0, "The device closest to the CPU wins."),
])

# ===================== DIGITAL LOGIC =====================
C("DL", "Boolean Algebra & Minimization", "Concepts", [
    ("e", 1, "s", "According to De Morgan's theorem, (A + B)' equals", ["A'·B'", "A' + B'", "A·B", "(A·B)'"], 0, "The complement of a sum is the product of complements."),
    ("e", 1, "s", "The dual of the Boolean expression A + B·C is", ["A · (B + C)", "A' · (B' + C')", "A + (B + C)", "A · B + C"], 0, "Swap AND/OR and 0/1 (do not complement variables)."),
    ("m", 1, "s", "A ⊕ A ⊕ A equals", ["A", "0", "1", "A'"], 0, "A ⊕ A = 0, 0 ⊕ A = A."),
    ("m", 2, "s", "A static-1 hazard in a two-level AND–OR circuit can be removed by", ["adding the consensus (redundant) product term", "adding an inverter", "using a slower gate", "making the circuit sequential"], 0, "The extra term covers the transition between adjacent minterms."),
    ("m", 1, "s", "In a K-map, adjacent cells (including wrap-around) differ in", ["exactly one variable", "two variables", "all variables", "no variables"], 0, "That is why Gray code ordering is used."),
    ("h", 2, "s", "A group of 8 adjacent 1s in a 4-variable K-map eliminates how many variables from the product term?", ["3", "2", "4", "1"], 0, "2^k cells remove k variables: 8 = 2^3."),
    ("m", 2, "m", "Which gates are universal? (select all)", ["NAND", "NOR", "XOR", "AND"], [0, 1], "Any Boolean function can be built with only NAND or only NOR."),
    ("m", 1, "s", "The number of Boolean functions of n variables is", ["2^(2^n)", "2^n", "n²", "2n"], 0, "Each of the 2^n rows can be 0 or 1."),
    ("h", 2, "s", "Which expression is a prime implicant that is also essential in F = Σm(0,1,2,5,6,7)?", ["There is no essential prime implicant in this cyclic function", "A'B'", "AB", "BC'"], 0, "Each minterm is covered by two prime implicants; the function is cyclic."),
])

C("DL", "Combinational Circuits", "Concepts", [
    ("e", 1, "s", "A full adder has", ["3 inputs and 2 outputs", "2 inputs and 2 outputs", "3 inputs and 1 output", "2 inputs and 1 output"], 0, "Inputs A, B, Cin; outputs Sum and Cout."),
    ("e", 1, "s", "The sum output of a full adder is", ["A ⊕ B ⊕ Cin", "A·B + Cin", "A + B + Cin", "(A·B) ⊕ Cin"], 0, "Cout = AB + BCin + ACin."),
    ("m", 1, "s", "A 4-to-1 multiplexer (with some inverters/constants available) can implement ANY Boolean function of at most", ["three variables (two on the select lines, the third on the data lines)", "two variables only", "four variables", "one variable only"], 0, "Two select lines pick one of four data inputs, each of which can be 0, 1, C or C′."),
    ("m", 2, "s", "A decoder with n inputs and an enable line can be used to implement", ["any function as an OR of its minterm outputs", "only AND functions", "only XOR functions", "only a single minterm"], 0, "Each output is a minterm."),
    ("m", 1, "s", "A half adder is built from", ["one XOR gate and one AND gate", "two XOR gates", "one OR gate and one AND gate", "two AND gates and an OR gate"], 0, "Sum = A⊕B, Carry = AB."),
    ("h", 2, "s", "A carry-lookahead adder is faster than a ripple-carry adder because", ["carries are computed in parallel from generate and propagate signals", "it uses fewer gates", "it avoids the sum XOR", "it uses sequential logic"], 0, "Ci+1 = Gi + Pi·Ci expanded."),
    ("h", 2, "s", "A priority encoder differs from a simple encoder in that it", ["handles multiple active inputs by encoding the highest-priority one", "has more output lines", "is sequential", "needs a clock"], 0, "A simple encoder assumes only one active input."),
    ("m", 1, "s", "A magnitude comparator for two n-bit numbers has outputs", ["A>B, A=B, A<B", "sum and carry", "n select lines", "only A=B"], 0, "Three mutually exclusive outputs."),
])

C("DL", "Number Systems & Arithmetic", "Concepts", [
    ("e", 1, "s", "Two's complement representation has", ["a single representation of zero", "two representations of zero", "no negative numbers", "a symmetric range"], 0, "The range is −2^(n−1) … 2^(n−1) − 1."),
    ("e", 1, "s", "The two's complement of the 8-bit number 00010100 is", ["11101100", "11101011", "10010100", "00010100"], 0, "Invert (11101011) and add 1."),
    ("m", 1, "s", "Signed overflow in two's complement addition occurs when", ["the carry into the MSB differs from the carry out of the MSB", "there is a carry out of the MSB", "the result is zero", "the operands have opposite signs"], 0, "Equivalently, two operands of the same sign give a result of the opposite sign."),
    ("m", 2, "s", "In IEEE 754 single precision the exponent field is", ["8 bits with bias 127", "11 bits with bias 1023", "8 bits with bias 128", "7 bits with bias 64"], 0, "Double precision uses 11 bits and bias 1023."),
    ("m", 1, "s", "In IEEE 754, an all-ones exponent field with a non-zero fraction represents", ["NaN", "infinity", "zero", "a denormal"], 0, "Infinity has a zero fraction."),
    ("h", 2, "s", "The hidden (implicit) leading 1 in IEEE 754 normalised numbers", ["is not stored, giving one extra bit of precision", "is stored in the sign bit", "is always 0", "applies only to denormals"], 0, "Denormals have an implicit leading 0."),
    ("h", 2, "s", "Sign extension of the 4-bit two's complement number 1010 to 8 bits gives", ["11111010", "00001010", "10001010", "11110101"], 0, "Replicate the sign bit."),
    ("m", 1, "s", "Gray code is useful because", ["successive values differ in exactly one bit", "it is faster to add", "it uses fewer bits", "it is self-complementing for all n"], 0, "Reduces glitches in encoders."),
])

C("DL", "Sequential Circuits", "Concepts", [
    ("e", 1, "s", "A D flip-flop's next state equals", ["D", "D'", "Q ⊕ D", "Q·D"], 0, "Q⁺ = D."),
    ("e", 1, "s", "A level-triggered JK latch with J = K = 1 and a long clock pulse shows", ["the race-around condition", "stable memory", "a forbidden state", "no output change"], 0, "Master-slave or edge-triggered designs avoid it."),
    ("m", 1, "s", "The characteristic equation of a T flip-flop is", ["Q⁺ = T ⊕ Q", "Q⁺ = T", "Q⁺ = T·Q", "Q⁺ = T + Q"], 0, "T = 1 toggles the state."),
    ("m", 2, "s", "In a Moore machine the output depends on", ["the present state only", "present state and input", "input only", "the next state"], 0, "In a Mealy machine, output depends on both."),
    ("m", 1, "s", "A synchronous counter compared with an asynchronous (ripple) counter", ["has all flip-flops clocked together, so less propagation delay", "is always smaller", "uses the output of one flip-flop as clock for the next", "cannot count up"], 0, "Ripple counters accumulate delay."),
    ("h", 2, "s", "An n-bit ring counter has", ["n states", "2n states", "2^n states", "n² states"], 0, "A Johnson counter has 2n states."),
    ("h", 2, "s", "Setup time of a flip-flop is the time", ["data must be stable before the active clock edge", "data must be stable after the clock edge", "the clock stays high", "the output takes to change"], 0, "Hold time is the time after the edge."),
    ("h", 2, "s", "Metastability in a flip-flop is typically caused by", ["violating setup/hold times, e.g., sampling an asynchronous input", "using too many gates", "high supply voltage", "a faulty clock tree only"], 0, "Synchroniser chains reduce its probability."),
    ("h", 2, "m", "Which of the following are TRUE for an edge-triggered D flip-flop? (select all)", ["It samples D at the active clock edge", "It can be built from two latches in master–slave form", "It is transparent while the clock is high", "It can be used to build a shift register"], [0, 1, 3], "Transparency during a clock level is a property of latches."),
])
