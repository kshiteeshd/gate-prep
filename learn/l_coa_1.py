"""COA part 1: instruction formats & addressing, datapath/control/performance, pipelining."""
import math

from learn import Ex, lesson
from learn.refs_hw import pipe_sim

S = "COA"


def expand(levels, bits=4):
    """expanding opcodes: levels = instructions used at each level; returns codes left for the next level"""
    avail = 2 ** bits
    for c in levels:
        avail = (avail - c) * 2 ** bits
    return avail


def I(dst, src, load=False, branch=False):
    return {"dst": dst, "src": src, "load": load, "branch": branch}


# ======================================================================================================
lesson(subject=S, chapter="Instruction Set & CPU", ch_no=1, no=1, slug="coa-instruction-addressing", title="Instruction Formats & Addressing Modes",
       topic="Instruction Formats & Addressing Modes", minutes=22, weight=5, widget="none",
       key="An instruction packs an opcode and operand specifiers into a fixed number of bits. The addressing mode tells the CPU how to turn an operand field into an effective address; GATE asks you to compute effective addresses, instruction widths and how many instructions an encoding supports.",
       analogy=("📮", "Addresses on an envelope", "A letter can say ‘deliver to 5 Main Street’ (direct), ‘deliver to whoever is named at the address written on this card’ (indirect), or ‘deliver to the house 3 doors down from the post office’ (relative). Addressing modes are exactly these ways of naming where the data lives."),
       sections=[
           dict(h="Instruction format and the instruction cycle", md="""An instruction has an **opcode** (what to do) and zero to three **operand fields** (registers, memory addresses or immediates). The basic cycle is **fetch → decode → execute (→ memory/write-back)**: the PC supplies the address, the instruction goes to the IR, the PC is incremented, and the control unit issues signals.

Instruction **length** can be fixed (RISC: simple decode) or variable (CISC). The number of address fields gives **0-, 1-, 2- and 3-address** machines:

| Machine | Example of X = (A + B) * (C + D) |
|---|---|
| **3-address** | ADD R1, A, B; ADD R2, C, D; MUL X, R1, R2 |
| **2-address** | MOV R1, A; ADD R1, B; MOV R2, C; ADD R2, D; MUL R1, R2; MOV X, R1 |
| **1-address (accumulator)** | LOAD A; ADD B; STORE T; LOAD C; ADD D; MUL T; STORE X |
| **0-address (stack)** | PUSH A; PUSH B; ADD; PUSH C; PUSH D; ADD; MUL; POP X |"""),
           dict(h="Addressing modes", md="""| Mode | Effective address (EA) | Memory refs for the operand |
|---|---|---|
| **Immediate** | operand is in the instruction | 0 |
| **Direct (absolute)** | EA = address field | 1 |
| **Indirect** | EA = M[address field] | 2 |
| **Register** | operand is in the register | 0 |
| **Register indirect** | EA = R | 1 |
| **Indexed** | EA = address field + Rindex | 1 |
| **Base-register** | EA = address field + Rbase (relocation) | 1 |
| **PC-relative** | EA = PC + offset (position-independent code, branches) | 1 |
| **Auto-increment / decrement** | EA = R, then R ± size (stack, arrays) | 1 |

Use **relative** addressing for branches (small offsets, relocatable); **base** for relocation; **indexed** for arrays; **indirect** for pointers. Note that the PC already points to the **next** instruction when the offset is added (check the question statement)."""),
           dict(h="Sizing an instruction", md="""For a word-addressable machine with 2ᵐ words of memory, a direct address needs m bits. For R registers, a register field needs ⌈log₂ R⌉ bits.

Instruction width = opcode bits + Σ operand-field bits. Maximum number of distinct opcodes = 2^(opcode bits).

**Branch range:** a k-bit signed PC-relative offset reaches from −2^(k−1) to 2^(k−1) − 1 instructions (or bytes) around the PC.""",
                formulas=[("width = opcode + Σ field bits;  register field = ⌈log₂ R⌉ bits", "instruction sizing")]),
           dict(h="Expanding opcodes", md="""To fit more instructions, unused opcode patterns of a short opcode are **extended** into longer ones. With a 16-bit instruction and 4-bit fields (3-address instruction = 4-bit opcode + three 4-bit addresses):

- 4-bit opcode gives 16 codes; if 14 are used for 3-address instructions, 2 remain.
- Each remaining code extends with the next 4 bits ⇒ 2 × 16 = 32 two-address codes; use 31 ⇒ 1 remains.
- That one extends to 1 × 16 = **16** one-address instructions (and so on to zero-address).

General rule: remaining = (previous remaining − used) × 2^(field bits).""",
                call=[("trap", "Subtract before you multiply", "At each level subtract the instructions you actually use from the available codes, then multiply by 2^(field bits) to get the next level.")]),
       ],
       examples=[
           Ex("Expanding opcode capacity", "A 16-bit instruction has 4-bit address fields. 14 three-address and 31 two-address instructions are defined. What is the maximum number of one-address instructions?",
              ["Level 1: 16 − 14 = 2 codes remain, each extended by 4 bits ⇒ 32 two-address codes. Use 31 ⇒ 1 remains.", "That one extends by 4 bits ⇒ **16** one-address instructions."],
              "**16**", verify=lambda: str(expand([14, 31]))),
           Ex("Effective address", "Memory: M[200] = 500, M[500] = 600; R1 = 300; the instruction has address field 200, PC = 100. Find the effective address for direct, indirect, register-indirect (R1) and indexed (R1) modes.",
              ["Direct: EA = 200. Indirect: EA = M[200] = 500.", "Register indirect: EA = R1 = 300. Indexed: EA = 200 + R1 = 500."],
              "Direct **200**, indirect **500**, register-indirect **300**, indexed **500**.", verify=lambda: "Direct %d, indirect %d, register-indirect %d, indexed %d" % (200, {200: 500, 500: 600}[200], 300, 200 + 300)),
           Ex("Instruction width", "A machine has 64 registers, 16 MB of byte-addressable memory and 120 opcodes. How many bits are needed for a 2-address instruction with one register and one direct memory address?",
              ["Opcode: ⌈log₂ 120⌉ = 7 bits. Register: log₂ 64 = 6 bits. Memory address: 16 MB = 2²⁴ ⇒ 24 bits.", "Total = 7 + 6 + 24 = **37** bits."],
              "**37** bits.", verify=lambda: str(math.ceil(math.log2(120)) + 6 + 24)),
           Ex("Branch range", "A 12-bit signed PC-relative offset counts instructions. How far can a branch jump forward and backward?",
              ["A 12-bit signed (two's complement) offset ranges over −2¹¹ … 2¹¹ − 1.", "That is −2048 … +2047 instructions around the PC."],
              "−**2048** to +**2047** instructions.", verify=lambda: "−%d to +%d instructions" % (2 ** 11, 2 ** 11 - 1)),
       ],
       traps=[("Indirect = two memory references", "Fetch the pointer then the operand."),
              ("Opcodes needed", "Round up: ⌈log₂ n⌉ bits for n opcodes."),
              ("Relative offset base", "Offset is added to the PC after the increment unless the question says otherwise."),
              ("Immediate has no EA", "The operand is in the instruction itself.")],
       quick=[("Which addressing mode is best for array traversal?", ["immediate", "indexed", "direct", "PC-relative"], 1, "Index register steps through."),
              ("Indirect addressing requires how many memory accesses for the operand?", ["0", "1", "2", "3"], 2, "Pointer then data."),
              ("PC-relative addressing helps with", ["position-independent code", "recursion", "floating point", "DMA"], 0, "Relocatable code."),
              ("The number of registers R requires how many bits?", ["R", "log₂ R rounded up", "R²", "2R"], 1, "⌈log₂ R⌉.")],
       summary=["Instruction = opcode + operands; fetch → decode → execute.", "0/1/2/3-address machines; stack machines use PUSH/POP.", "Addressing modes: immediate, direct, indirect, register, register indirect, indexed, base, relative, auto-inc/dec.",
                "Width = opcode + field bits; ⌈log₂ n⌉ bits to name n things.", "Expanding opcodes: (remaining − used) × 2^field bits at each level.", "Relative branch of k bits reaches −2^(k−1)…2^(k−1)−1."])


# ======================================================================================================
lesson(subject=S, chapter="Instruction Set & CPU", ch_no=1, no=2, slug="coa-datapath-control-performance", title="Datapath, Control Unit & CPU Performance",
       topic="Datapath & Control Unit", minutes=22, weight=5, widget="none",
       key="The datapath (registers, ALU, buses) executes instructions under the direction of the control unit, which is either hardwired logic or a microprogram. CPU performance is CPU time = instruction count × CPI × clock period, and Amdahl's law bounds the benefit of any improvement.",
       analogy=("🎼", "An orchestra and its conductor", "The instruments (ALU, registers, buses) can play, but nothing happens until the conductor (control unit) cues them in the right order. A hardwired conductor memorises the score as fixed wiring; a microprogrammed conductor reads it from a sheet (control store) that can be edited."),
       sections=[
           dict(h="Datapath and the control unit", md="""The **datapath** contains the register file, ALU, shifter, internal buses and memory interface (MAR, MDR). A single-cycle datapath executes each instruction in one (long) clock cycle; a **multicycle** design splits instructions over several short cycles (IF, ID, EX, MEM, WB) reusing hardware, so cycle time is set by the slowest *step* instead of the slowest *instruction*.

The **control unit** generates the control signals (ALU operation, register load, memory read/write, bus selects).

| | **Hardwired** | **Microprogrammed** |
|---|---|---|
| Implementation | logic gates/PLA | control store (ROM) of microinstructions |
| Speed | fast | slower |
| Flexibility | hard to change | easy to change/extend |
| Used in | RISC | CISC |"""),
           dict(h="Microprogramming: horizontal and vertical", md="""A **microinstruction** specifies control signals and (optionally) the address of the next microinstruction. A **control store** holds the microprogram for every instruction.

- **Horizontal:** one bit per control signal — wide words, high parallelism, **no decoding**, fast.
- **Vertical:** signals are *encoded* in fields — narrow words, needs decoders, slower.

Width of a vertical field for a group of k mutually exclusive signals (plus ‘none’) = ⌈log₂(k + 1)⌉ bits. A **nanoprogram** adds a second level to save space. Control-store size = number of microinstructions × microinstruction width.""",
                formulas=[("vertical field bits = ⌈log₂(k + 1)⌉ for k exclusive signals (+ no-op)", "control-word encoding")]),
           dict(h="Performance equations", md="""CPU time = **IC × CPI × T** = IC × CPI / f. With an instruction mix, **CPI = Σ fᵢ·CPIᵢ**.

- **MIPS** = f / (CPI × 10⁶) (misleading across ISAs).
- **Speedup** = old time / new time.
- **Amdahl's law:** if a fraction F of execution time is sped up by a factor S, overall speedup = 1 / ((1 − F) + F/S); the limit as S → ∞ is 1/(1 − F).
- Pipelined time for n instructions on a k-stage pipeline: (k + n − 1) cycles; ideal speedup → k.""",
                formulas=[("T_cpu = IC × CPI / f", "CPU time"), ("Speedup = 1 / ((1 − F) + F / S)", "Amdahl's law")]),
           dict(h="Buses, registers and ALU operations", md="""A **bus** transfers data between components; a single-bus datapath needs several cycles per instruction since only one transfer happens per cycle; three-bus designs perform two reads and a write at once. The ALU performs arithmetic/logic; the **status register** holds flags (zero, sign, carry, overflow). Typical micro-operation sequence for an ADD: PC → MAR; read memory → MDR → IR; PC + 1 → PC; decode; registers → ALU; result → register."""),
       ],
       examples=[
           Ex("CPI from an instruction mix", "40% of instructions are ALU (CPI 1), 30% loads (CPI 2), 10% stores (CPI 2), 20% branches (CPI 3). Find the CPI.",
              ["Weight each class's CPI by its frequency: 0.4×1 + 0.3×2 + 0.1×2 + 0.2×3.", "= 0.4 + 0.6 + 0.2 + 0.6 = **1.8**."],
              "**1.8**", verify=lambda: "%.1f" % (0.4 * 1 + 0.3 * 2 + 0.1 * 2 + 0.2 * 3)),
           Ex("CPU time", "A program has 2×10⁹ instructions, CPI 1.8 and the clock is 2 GHz. What is the execution time?",
              ["CPU time = IC × CPI / f.", "= 2×10⁹ × 1.8 / (2×10⁹) = **1.8 seconds**."],
              "**1.8** seconds.", verify=lambda: "%.1f seconds" % (2e9 * 1.8 / 2e9)),
           Ex("Amdahl's law", "60% of a program's time is improved by a factor of 4. What is the overall speedup?",
              ["Speedup = 1 / (0.4 + 0.6/4) = 1 / 0.55 ≈ **1.82**.", "Even with an infinite speedup of that part the limit is 1/0.4 = 2.5."],
              "≈ **1.82**", verify=lambda: "%.2f" % (1 / (0.4 + 0.6 / 4))),
           Ex("Microinstruction width", "A control unit has three groups of mutually exclusive signals with 8, 4 and 5 signals. Compare horizontal and vertical encoding widths.",
              ["Horizontal: 8 + 4 + 5 = 17 bits.", "Vertical: ⌈log₂ 9⌉ + ⌈log₂ 5⌉ + ⌈log₂ 6⌉ = 4 + 3 + 3 = **10** bits."],
              "Horizontal **17**, vertical **10**.", verify=lambda: "Horizontal %d, vertical %d" % (8 + 4 + 5, math.ceil(math.log2(9)) + math.ceil(math.log2(5)) + math.ceil(math.log2(6)))),
       ],
       traps=[("Average CPI", "Weight each CPI by its instruction frequency."),
              ("MIPS misleads", "Different ISAs do different amounts of work per instruction."),
              ("Amdahl's fraction", "F is a fraction of the *original execution time*, not of the instruction count."),
              ("Horizontal vs vertical", "Horizontal is wide and fast; vertical is narrow but needs decoders.")],
       quick=[("Hardwired control compared with microprogrammed is", ["slower", "faster", "equally flexible", "always larger"], 1, "Fixed logic is faster."),
              ("CPU time equals", ["IC / CPI", "IC × CPI × cycle time", "CPI / f only", "IC + CPI"], 1, "IC × CPI × T."),
              ("Vertical microprogramming uses", ["one bit per signal", "encoded fields", "no control store", "pipelines"], 1, "Encoded fields."),
              ("The max speedup by enhancing 50% of the time is", ["1.5", "2", "∞", "4"], 1, "1/(1−0.5) = 2.")],
       summary=["Single-cycle vs multicycle datapaths; control unit issues signals.", "Hardwired = fast, inflexible; microprogrammed = flexible, slower.", "Horizontal microcode = wide/no decode; vertical = encoded/narrow.",
                "CPU time = IC × CPI × T; CPI = Σ fᵢ CPIᵢ.", "Amdahl: 1/((1−F) + F/S); limit 1/(1−F).", "MIPS = f/(CPI·10⁶)."])


# ======================================================================================================
lesson(subject=S, chapter="Instruction Set & CPU", ch_no=1, no=3, slug="coa-pipelining", title="Pipelining & Hazards",
       topic="Pipelining", minutes=26, weight=7, widget="pipeline",
       widget_hint="Type MIPS-style instructions, toggle forwarding and the branch penalty, and watch the stall bubbles appear in the cycle-by-cycle table.",
       key="Pipelining overlaps the stages of consecutive instructions, aiming for one instruction per cycle. Structural, data (RAW, WAR, WAW) and control hazards cause stalls; forwarding removes most data stalls except load-use, and branch prediction reduces control stalls.",
       analogy=("🧺", "A laundry line", "Washing, drying and folding each take a step. Instead of waiting for load 1 to be folded before washing load 2, you start washing load 2 as soon as the washer is free. Everything proceeds in parallel — until one load needs something that is not ready yet, and the line has to wait."),
       sections=[
           dict(h="The 5-stage pipeline and ideal speedup", md="""Stages: **IF** (fetch), **ID** (decode, register read), **EX** (ALU), **MEM** (data memory), **WB** (register write). Pipeline registers separate the stages; the clock period equals the slowest stage plus register overhead.

For k stages and n instructions: **cycles = k + n − 1**; non-pipelined time = n·k cycles (if equal stages), so **speedup = nk / (k + n − 1) → k** as n → ∞. **Throughput** improves; the latency of a single instruction does not.""",
                formulas=[("cycles = k + n − 1;  speedup = n·k / (k + n − 1)", "ideal k-stage pipeline")]),
           dict(h="Hazards", md="""- **Structural:** two instructions need the same hardware in the same cycle (single memory port for IF and MEM). Fix by duplicating resources or stalling.
- **Data:** an instruction needs a result not yet written. **RAW** (read after write, true dependence) is the main one; **WAR** and **WAW** only arise with out-of-order execution/register renaming.
- **Control:** a branch changes the PC after later instructions have been fetched.

**Without forwarding**, a RAW dependent instruction must wait until the producer's WB (register file written in the first half of the cycle, read in the second half): an **adjacent** dependent instruction stalls **2** cycles, one with a single instruction in between stalls **1**, and with two or more in between there is no stall. (Without the same-cycle write/read trick the adjacent case costs 3.)

**With forwarding (bypassing)** results go straight from EX/MEM or MEM/WB to the ALU inputs: dependent ALU instructions need **no stall**, but a **load-use** dependence still costs **1 stall** (data only exists after MEM).""",
                call=[("trap", "Same-cycle write and read", "If the register file writes in the first half-cycle and reads in the second, the consumer's ID can coincide with the producer's WB. The tool below assumes this convention.")]),
           dict(h="Control hazards and branch handling", md="""A branch resolved in EX (or MEM) causes a penalty of 1–3 cycles for the instructions fetched in the shadow.

- **Stall** until the branch resolves (penalty = stages before resolution).
- **Predict not taken** (continue sequentially, flush if taken); **predict taken**.
- **Delayed branch:** the instruction(s) after the branch always execute; the compiler fills the **delay slot**.
- **Dynamic prediction:** 1-bit or 2-bit saturating counters in a branch history table; branch target buffer.

Effective CPI = 1 + (branch frequency × misprediction rate × penalty) + other stalls."""),
           dict(h="Beyond the simple pipeline", md="""**Superscalar** issues several instructions per cycle; **dynamic scheduling** (Tomasulo, scoreboarding) executes out of order; **VLIW** leaves the scheduling to the compiler; **superpipelining** uses very deep pipelines. Pipelines also complicate **precise exceptions**."""),
       ],
       examples=[
           Ex("Ideal speedup", "A 5-stage pipeline executes 100 instructions with no stalls. Compare with a non-pipelined machine of 5 cycles per instruction.",
              ["Pipelined: 5 + 100 − 1 = 104 cycles. Non-pipelined: 100 × 5 = 500 cycles.", "Speedup = 500 / 104 ≈ **4.81**."],
              "≈ **4.81**", verify=lambda: "%.2f" % (100 * 5 / (5 + 100 - 1))),
           Ex("Stalls without forwarding", "Program: LW R1,0(R2); ADD R3,R1,R4; SUB R5,R3,R6; SW R5,0(R7) on the 5-stage pipeline without forwarding. How many cycles does it take?",
              ["Each instruction depends on the previous one (R1, R3, R5), and each consumer must wait for the producer's WB: 2 stall cycles per dependency (same-cycle write/read).", "Ideal = 4 + 4 = 8 cycles; stalls = 3 × 2 = 6 ⇒ **14** cycles."],
              "**14** cycles.", verify=lambda: str(pipe_sim([I("R1", ["R2"], True), I("R3", ["R1", "R4"]), I("R5", ["R3", "R6"]), I(None, ["R5", "R7"])], False))),
           Ex("Forwarding and the load-use hazard", "The same program with forwarding: how many cycles?",
              ["ADD can take R1 from the MEM/WB register but only after the load's MEM stage ⇒ 1 stall. SUB and SW get their operands by forwarding with no stall.", "Cycles = 8 + 1 = **9**."],
              "**9** cycles.", verify=lambda: str(pipe_sim([I("R1", ["R2"], True), I("R3", ["R1", "R4"]), I("R5", ["R3", "R6"]), I(None, ["R5", "R7"])], True))),
           Ex("Effective CPI with branches", "20% of instructions are branches, 60% of which are taken, and each taken branch costs 3 stall cycles (predict not taken). Ideal CPI is 1. Compute the CPI.",
              ["Taken-branch frequency = 0.2 × 0.6 = 0.12.", "CPI = 1 + 0.12 × 3 = **1.36**."],
              "**1.36**", verify=lambda: "%.2f" % (1 + 0.2 * 0.6 * 3)),
       ],
       traps=[("Latency vs throughput", "Pipelining improves throughput; single-instruction latency stays the same or grows."),
              ("Load-use stall", "Forwarding cannot remove it completely: 1 stall remains."),
              ("Only RAW in an in-order pipeline", "WAR/WAW hazards appear with out-of-order execution."),
              ("Branch penalty", "Count the stages before the branch is resolved.")],
       quick=[("Ideal speedup of a k-stage pipeline approaches", ["1", "k/2", "k", "2k"], 2, "k."),
              ("A load followed immediately by a dependent ALU op needs, with forwarding,", ["0 stalls", "1 stall", "2 stalls", "3 stalls"], 1, "Load-use."),
              ("Which hazard is a 'true' dependence?", ["WAR", "WAW", "RAW", "structural"], 2, "Data really flows."),
              ("A delay slot is filled by", ["the hardware", "the compiler", "the OS", "the user"], 1, "Delayed branch.")],
       summary=["IF, ID, EX, MEM, WB; cycles = k + n − 1; speedup → k.", "Hazards: structural, data (RAW/WAR/WAW), control.", "Forwarding removes ALU–ALU stalls; load-use still costs 1.",
                "Without forwarding a RAW dependency costs 2 stalls (write first half, read second half).", "Control: predict, delay slot, dynamic prediction; CPI = 1 + stalls per instruction.", "Superscalar, out-of-order and VLIW go beyond the in-order pipeline."])
