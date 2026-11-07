"""Computer Organization & Architecture — parametric generators."""
import math
from collections import OrderedDict

from content.kit import *

S = "COA"
IF_, DP, PL, CM, IO = ("Instruction Formats & Addressing Modes", "Datapath & Control Unit", "Pipelining",
                       "Cache & Memory Hierarchy", "I/O, Interrupts & DMA")
lg = lambda x: int(math.ceil(math.log2(x)))


# ---------------- instruction formats ----------------
@gen(S, IF_, "Instruction encoding", n=70, diff="easy")
def i_enc(r):
    L, regs, ops = r.choice([16, 24, 32, 32, 32]), r.choice([8, 16, 32, 64]), r.choice([16, 32, 64, 100, 128, 200])
    kind = r.choice(["imm", "two_reg", "words", "mar", "addr_lines", "bytes"])
    if kind == "imm": return nat(r, "A %d-bit instruction format has an opcode field for %d distinct operations, two source-register fields and one destination-register field (%d registers in the machine), plus an immediate field. How many bits remain for the immediate?" % (L, ops, regs),
                                 L - lg(ops) - 3 * lg(regs), "Opcode %d bits; registers 3 × %d bits; immediate = %d − %d − %d." % (lg(ops), lg(regs), L, lg(ops), 3 * lg(regs)))
    if kind == "two_reg": return nat(r, "A register-register instruction has an opcode of %d bits and two register operands for a machine with %d registers. What is the minimum instruction length in bits?" % (lg(ops), regs), lg(ops) + 2 * lg(regs), "opcode + 2·⌈log₂ R⌉.")
    if kind == "words":
        m, w = r.choice([64, 256, 1024, 4096]), r.choice([16, 32, 64])
        return nat(r, "A byte-addressable memory has %d KB and the word size is %d bits. How many words does it hold?" % (m, w), m * 1024 * 8 // w, "bytes × 8 / word size.")
    if kind == "mar":
        m = r.choice([64, 128, 256, 1024, 4096, 16384])
        return nat(r, "A byte-addressable main memory has capacity %d KB. How many bits are needed in the MAR?" % m, lg(m * 1024), "log₂(capacity in bytes).")
    if kind == "addr_lines":
        m = r.choice([1, 2, 4, 8, 16, 64])
        return nat(r, "Number of address lines needed for a byte-addressable memory of %d GB?" % m, lg(m * 2 ** 30), "log₂ of bytes.")
    k = r.choice([4, 8, 16, 32, 64, 128, 256])
    return nat(r, "A processor has a %d-bit address bus. What is the size of the addressable space in KB (byte-addressable)?" % (lg(k) + 10), k, "2^addr bytes.")


@gen(S, IF_, "Expanding opcodes", n=60, diff="hard", marks=2)
def i_expand(r):
    w = r.choice([3, 4, 5])
    n3 = r.randint(1, 2 ** w - 2)
    two = (2 ** w - n3) * 2 ** w
    n2 = r.randint(1, two - 1)
    one = (two - n2) * 2 ** w
    n1 = r.randint(1, one - 1)
    zero = (one - n1) * 2 ** w
    head = ("A processor has fixed-length instructions of %d bits made of four %d-bit fields: an opcode field followed by three operand fields. "
            "Using the expanding-opcode technique (unused codes of a field are extended into the next field) it supports %d three-address instructions and %d two-address instructions" % (4 * w, w, n3, n2))
    if r.random() < 0.5:
        return nat(r, head + ". What is the maximum number of one-address instructions possible?", one, "Two-address codes available (2^w − %d)·2^w = %d; remaining %d extend by 2^w ⇒ %d." % (n3, two, two - n2, one))
    return nat(r, head + " and %d one-address instructions. What is the maximum number of zero-address instructions possible?" % n1, zero, "One-address codes = %d; remaining %d extend by 2^w ⇒ %d." % (one, one - n1, zero))


@gen(S, IF_, "Addressing modes", n=80, diff="medium", marks=2)
def i_addr(r):
    base, off = r.choice([100, 200, 400, 1000]), r.choice([4, 8, 12, 20, 40])
    pc = r.choice([2000, 3000, 5000])
    mem = {base + off: r.randint(500, 900) * 4, base: r.randint(100, 400), 2 * base: r.randint(10, 99)}
    reg = base
    mode = r.choice(["direct", "indirect", "regind", "indexed", "pcrel", "regval"])
    if mode == "direct":
        a = base + off
        return nat(r, "Memory contents (address → value): %s. With DIRECT addressing and address field %d, the operand loaded is" % ({k: v for k, v in mem.items()}, a), mem[a], "Operand = M[%d] = %d." % (a, mem[a]))
    if mode == "indirect":
        a = base + off
        mem2 = dict(mem); mem2[a] = base
        return nat(r, "Memory: %s. With INDIRECT addressing and address field %d, the operand loaded is" % (mem2, a), mem2[base], "Pointer M[%d] = %d; operand = M[%d] = %d." % (a, base, base, mem2[base]))
    if mode == "regind":
        return nat(r, "Register R1 = %d. Memory: %s. Operand using REGISTER INDIRECT mode (R1) is" % (reg, {k: v for k, v in mem.items()}), mem[reg], "EA = R1 = %d." % reg)
    if mode == "indexed":
        return nat(r, "Register R1 = %d, instruction displacement = %d. Memory: %s. Operand using INDEXED mode off(R1) is" % (reg, off, {k: v for k, v in mem.items()}), mem[reg + off], "EA = R1 + off = %d." % (reg + off))
    if mode == "pcrel":
        ln = r.choice([2, 4])
        return nat(r, "A %d-byte branch instruction at address %d has a PC-relative offset of %d (target = PC after fetch + offset). What is the branch target address?" % (ln, pc, off), pc + ln + off, "PC after fetch = %d; target = %d." % (pc + ln, pc + ln + off))
    n = r.randint(2, 5)
    return nat(r, "How many memory references (excluding instruction fetch) are needed to fetch an operand using a %d-level indirect addressing chain?" % n, n + 1, "n pointer reads plus the final operand read.")


@gen(S, IF_, "Endianness", n=40, diff="easy")
def i_endian(r):
    v = r.randint(0x10000000, 0xFFFFFFFF)
    b = v.to_bytes(4, "big")
    off = r.randint(0, 3)
    little = r.random() < 0.5
    stored = b[::-1] if little else b
    base = r.choice([0x1000, 0x2000, 0x8000])
    return mcq(r, "The 32-bit word 0x%08X is stored at address 0x%X on a %s-endian machine. The byte at address 0x%X is" % (v, base, "little" if little else "big", base + off), "0x%02X" % stored[off],
               ["0x%02X" % x for x in set(b) if x != stored[off]] + ["0x%02X" % ((stored[off] + 1) % 256), "0x%02X" % ((stored[off] ^ 0xF0))], "Byte order in memory: %s." % " ".join("%02X" % x for x in stored))


# ---------------- datapath / performance ----------------
@gen(S, DP, "CPU performance", n=80, diff="medium")
def p_cpi(r):
    kind = r.choice(["cpi", "time", "amdahl", "mips", "speedup"])
    fr = [0.4, 0.3, 0.2, 0.1]
    cpis = [r.randint(1, 3), r.randint(2, 5), r.randint(3, 8), r.randint(4, 12)]
    ic = r.choice([10 ** 6, 5 * 10 ** 6, 10 ** 8, 2 * 10 ** 9])
    f = r.choice([500, 1000, 2000, 2500, 3000])
    avg = sum(a * b for a, b in zip(fr, cpis))
    if kind == "cpi": return nat(r, "Instruction mix: 40%% type A (CPI %d), 30%% type B (CPI %d), 20%% type C (CPI %d), 10%% type D (CPI %d). Average CPI? (up to 2 decimals)" % tuple(cpis), round(avg, 2), "Σ fraction × CPI = %.2f." % avg, tol=0.01)
    if kind == "time":
        t = ic * avg / (f * 1e6)
        return nat(r, "A program has %.0e instructions with average CPI %.2f on a %d MHz processor. Execution time in seconds? (up to 3 decimals)" % (ic, avg, f), round(t, 3), "T = IC × CPI / f = %.3f s." % t, tol=0.002)
    if kind == "amdahl":
        fe, s = r.choice([0.4, 0.5, 0.6, 0.8, 0.9]), r.choice([2, 4, 5, 10, 20])
        return nat(r, "%d%% of a program's time is spent in a part that is made %d times faster. Overall speedup (Amdahl)? (up to 3 decimals)" % (fe * 100, s), round(1 / ((1 - fe) + fe / s), 3), "1/((1−f) + f/s).", tol=0.002)
    if kind == "mips": return nat(r, "A %d MHz processor has an average CPI of %.2f. Its MIPS rating is? (up to 2 decimals)" % (f, avg), round(f / avg, 2), "MIPS = f(MHz)/CPI.", tol=0.01)
    c1, c2 = r.choice([2, 3, 4]), r.choice([5, 6, 8])
    return nat(r, "Machine X runs a program in %d s; machine Y in %d s. How many times faster is X than Y? (up to 2 decimals)" % (c1, c2 * c1), round(c2, 2), "Ratio of execution times.", tol=0.01)


@gen(S, DP, "Microprogrammed control", n=60, diff="medium", marks=2)
def d_micro(r):
    sig, cs, groups = r.choice([32, 40, 48, 64]), r.choice([256, 512, 1024, 2048, 4096]), [r.randint(2, 15) for _ in range(r.randint(3, 5))]
    kind = r.choice(["horiz", "vert", "next", "cs", "mar"])
    if kind == "horiz": return nat(r, "A horizontal microprogrammed control unit has %d control signals (one bit each) and a %d-bit next-address field. Width of a microinstruction (bits)?" % (sig, lg(cs)), sig + lg(cs), "signals + next-address bits.")
    if kind == "vert":
        w = sum(lg(g + 1) for g in groups)
        return nat(r, "Control signals form mutually-exclusive groups of sizes %s (a group needs one extra code for 'no signal'). With vertical (encoded) microinstructions, how many control bits are needed?" % groups, w, "Σ ⌈log₂(g+1)⌉ = %d." % w)
    if kind == "next": return nat(r, "A control store holds %d microinstructions. Minimum number of bits in the next-microinstruction address field?" % cs, lg(cs), "⌈log₂ N⌉.")
    if kind == "cs": return nat(r, "A control store has %d words of %d bits each. Its total capacity in KB is? (up to 2 decimals)" % (cs, sig + lg(cs)), round(cs * (sig + lg(cs)) / 8 / 1024, 2), "words × width / 8 / 1024.", tol=0.01)
    ops, rt = r.choice([32, 64, 128, 256]), r.choice([3, 4, 6, 8])
    return nat(r, "A processor has %d distinct opcodes and each opcode's routine is exactly %d micro-instructions long. Minimum number of control-store words?" % (ops, rt), ops * rt, "opcodes × routine length.")


# ---------------- pipelining ----------------
def pipeline_cycles(instrs, forwarding):
    """instrs: list of (op, dest, srcs). 5-stage IF ID EX MEM WB; reg file written first half / read second half."""
    ids, last_writer = [], {}
    for i, (op, d, srcs) in enumerate(instrs):
        need = ids[-1] + 1 if ids else 2
        for s in srcs:
            if s in last_writer:
                j, jop = last_writer[s]
                if not forwarding: need = max(need, ids[j] + 3)
                elif jop == "LW": need = max(need, ids[j] + 2)
        ids.append(need)
        if d: last_writer[d] = (i, op)
    return ids[-1] + 3


def prog_str(instrs):
    out = []
    for op, d, s in instrs:
        out.append("LW  %s, 0(%s)" % (d, s[0]) if op == "LW" else "ADD %s, %s, %s" % (d, s[0], s[1]) if op == "ADD" else "SW  %s, 0(%s)" % (s[0], s[1]))
    return "\n".join(out)


@gen(S, PL, "Hazards (cycle-accurate)", n=90, diff="hard", marks=2)
def pl_hazard(r):
    regs = ["R%d" % i for i in range(1, 7)]
    n = r.randint(4, 6)
    ins = []
    for _ in range(n):
        if r.random() < 0.35:
            ins.append(("LW", r.choice(regs), [r.choice(regs)]))
        else:
            ins.append(("ADD", r.choice(regs), [r.choice(regs), r.choice(regs)]))
    fw = r.random() < 0.5
    c = pipeline_cycles(ins, fw)
    return nat(r, "Classic 5-stage pipeline (IF, ID, EX, MEM, WB) with in-order issue. The register file is written in the first half of a cycle and read in the second half. "
                  "%s. Dependent instructions stall in ID until their operands are available.\n```\n%s\n```\nTotal number of cycles to complete all instructions?" % (
                      "Full forwarding is implemented (a load result is usable only after MEM, so load-use costs one stall)" if fw else "There is NO forwarding", prog_str(ins)),
               c, "Simulate ID-stage times: ideal = n + 4 = %d; with stalls = %d." % (n + 4, c))


@gen(S, PL, "Pipeline speedup", n=70, diff="medium")
def pl_speed(r):
    k = r.choice([4, 5, 6, 8])
    stages = [r.choice([20, 30, 40, 50, 60, 80]) for _ in range(k)]
    ov = r.choice([0, 2, 5, 10])
    n = r.choice([100, 500, 1000, 10 ** 4])
    kind = r.choice(["cycle", "speed", "time", "ideal", "throughput", "branch"])
    if kind == "cycle": return nat(r, "A %d-stage pipeline has stage delays %s ns and %d ns of latch overhead per stage. The minimum clock period (ns) is" % (k, stages, ov), max(stages) + ov, "max(stage) + overhead.")
    if kind == "speed":
        sp = (sum(stages) / (max(stages) + ov))
        return nat(r, "A non-pipelined processor takes %d ns per instruction (sum of stages %s). The pipelined version has %d ns latch overhead per stage. Ignoring stalls, the steady-state speedup is? (up to 2 decimals)" % (sum(stages), stages, ov), round(sp, 2), "Σstage / (max stage + overhead).", tol=0.01)
    if kind == "time":
        cyc = max(stages) + ov
        return nat(r, "A %d-stage pipeline with clock period %d ns executes %d instructions with no stalls. Total time in ns?" % (k, cyc, n), (k + n - 1) * cyc, "(k + n − 1) × T.")
    if kind == "ideal": return nat(r, "Number of cycles to execute %d instructions on an ideal %d-stage pipeline (no hazards)?" % (n, k), k + n - 1, "k + n − 1.")
    if kind == "throughput":
        cyc = max(stages) + ov
        return nat(r, "A pipeline with a %d ns clock completes one instruction per cycle in steady state. Throughput in million instructions per second (MIPS)? (up to 2 decimals)" % cyc, round(1000 / cyc, 2), "1/T.", tol=0.01)
    f, p = r.choice([0.1, 0.15, 0.2, 0.25]), r.choice([1, 2, 3, 4])
    return nat(r, "In a pipeline with ideal CPI 1, %d%% of instructions are branches and each causes %d stall cycle(s). Effective CPI? (up to 2 decimals)" % (f * 100, p), round(1 + f * p, 2), "1 + f·penalty.", tol=0.01)


@gen(S, PL, "Dependences", n=35, diff="easy")
def pl_dep(r):
    a, b = r.sample(["R1", "R2", "R3", "R4", "R5"], 2)
    c = r.choice(["R6", "R7"])
    kind = r.choice(["RAW", "WAR", "WAW"])
    if kind == "RAW": i1, i2 = "I1: ADD %s, %s, %s" % (a, b, c), "I2: SUB %s, %s, %s" % (c if False else "R8", a, b)
    elif kind == "WAR": i1, i2 = "I1: ADD R8, %s, %s" % (a, b), "I2: SUB %s, %s, %s" % (a, b, c)
    else: i1, i2 = "I1: ADD %s, %s, %s" % (a, b, c), "I2: SUB %s, R7, R6" % a
    return mcq(r, "Consider\n```\n%s\n%s\n```\nThe dependence of I2 on I1 is a" % (i1, i2), kind + " hazard", [x + " hazard" for x in ("RAW", "WAR", "WAW", "control") if x != kind], "RAW = read after write, WAR = write after read, WAW = write after write.")


# ---------------- cache & memory ----------------
@gen(S, CM, "Cache address breakdown", n=100, diff="easy")
def m_cachebits(r):
    cs, bs, assoc, addr = r.choice([4, 8, 16, 32, 64, 128]) * 1024, r.choice([16, 32, 64, 128]), r.choice([1, 2, 4, 8, 0]), r.choice([24, 32, 36, 40, 48])
    lines = cs // bs
    sets = 1 if assoc == 0 else lines // assoc
    off, idx = lg(bs), lg(sets)
    tag = addr - off - idx
    kind = r.choice(["tag", "index", "off", "sets", "lines", "tagstore"])
    d = "%d KB cache, %d-byte blocks, %s, %d-bit physical address" % (cs // 1024, bs, "direct-mapped" if assoc == 1 else "fully associative" if assoc == 0 else "%d-way set-associative" % assoc, addr)
    if kind == "tag": return nat(r, "%s. Number of tag bits?" % d, tag, "Offset %d, index %d, tag = %d − %d − %d = %d." % (off, idx, addr, off, idx, tag))
    if kind == "index": return nat(r, "%s. Number of index (set-select) bits?" % d, idx, "sets = %d ⇒ %d bits." % (sets, idx))
    if kind == "off": return nat(r, "%s. Number of block-offset bits?" % d, off, "log₂(block size).")
    if kind == "sets": return nat(r, "%s. Number of sets?" % d, sets, "lines / associativity.")
    if kind == "lines": return nat(r, "%s. Number of cache lines?" % d, lines, "cache size / block size.")
    return nat(r, "%s. Each line also has 1 valid bit. Total tag-store size in bits (tags + valid bits only)?" % d, lines * (tag + 1), "lines × (tag + valid) = %d × %d." % (lines, tag + 1))


def sim_cache(blocks, sets, ways, policy):
    c = [OrderedDict() for _ in range(sets)]
    hit = 0
    for b in blocks:
        s = c[b % sets]
        if b in s:
            hit += 1
            if policy == "LRU": s.move_to_end(b)
        else:
            if len(s) >= ways: s.popitem(last=False)
            s[b] = 1
    return hit


@gen(S, CM, "Cache simulation", n=90, diff="medium", marks=2)
def m_sim(r):
    ways, sets = r.choice([(1, 4), (2, 2), (4, 1), (2, 4), (1, 8)])
    pol = r.choice(["LRU", "FIFO"])
    blocks = [r.randint(0, 11) for _ in range(r.randint(12, 18))]
    h = sim_cache(blocks, sets, ways, pol)
    kind = r.choice(["hits", "miss"])
    org = "direct-mapped with %d lines" % sets if ways == 1 else "fully associative with %d lines" % ways if sets == 1 else "%d-way set-associative with %d sets (%d lines)" % (ways, sets, sets * ways)
    q = "A cache is %s%s. Memory block numbers are accessed in this order (cache initially empty):\n%s\n" % (org, "" if ways == 1 else " using %s replacement" % pol, " ".join(map(str, blocks)))
    if kind == "hits": return nat(r, q + "Number of cache HITS?", h, "Simulation: %d hits, %d misses." % (h, len(blocks) - h))
    return nat(r, q + "Number of cache MISSES?", len(blocks) - h, "Simulation: %d hits, %d misses." % (h, len(blocks) - h))


@gen(S, CM, "AMAT", n=80, diff="medium")
def m_amat(r):
    h1, m1, h2, m2, mem = r.choice([1, 2]), r.choice([0.02, 0.05, 0.1, 0.08]), r.choice([8, 10, 12]), r.choice([0.1, 0.2, 0.25, 0.3, 0.4]), r.choice([80, 100, 120, 200])
    kind = r.choice(["one", "two", "cpi", "hit", "wt"])
    if kind == "one": return nat(r, "Cache hit time %d cycle(s), miss rate %.0f%%, miss penalty %d cycles. Average memory access time (cycles)? (up to 2 decimals)" % (h1, m1 * 100, mem // 4), round(h1 + m1 * (mem // 4), 2), "AMAT = hit + miss rate × penalty.", tol=0.01)
    if kind == "two": return nat(r, "L1: hit time %d cycle, miss rate %.0f%%. L2: hit time %d cycles, local miss rate %.0f%%. Main memory: %d cycles. AMAT (cycles)? (up to 2 decimals)" % (h1, m1 * 100, h2, m2 * 100, mem), round(h1 + m1 * (h2 + m2 * mem), 2), "H1 + m1(H2 + m2·Pmem).", tol=0.01)
    if kind == "cpi":
        mpi = r.choice([0.01, 0.02, 0.03, 0.05])
        return nat(r, "A processor has base CPI 1.2. Instruction mix: 30%% of instructions access memory. Cache miss rate %.0f%%, miss penalty %d cycles (instruction fetches always hit). Effective CPI? (up to 2 decimals)" % (m1 * 100, mem // 4), round(1.2 + 0.3 * m1 * (mem // 4), 2), "1.2 + refs/instr × miss rate × penalty.", tol=0.01)
    if kind == "hit":
        tc, tm = r.choice([2, 5, 10]), r.choice([50, 100, 200])
        eff = r.choice([0.90, 0.95, 0.98])
        t = eff * tc + (1 - eff) * (tc + tm)
        return nat(r, "Cache access time %d ns, main memory access time %d ns, hit ratio %.2f (memory accessed after a miss is detected). Average access time in ns? (up to 2 decimals)" % (tc, tm, eff), round(t, 2), "h·tc + (1−h)(tc + tm).", tol=0.01)
    w, lines = r.choice([0.2, 0.3, 0.4]), r.choice([100, 200, 500])
    return nat(r, "Write-through cache: %d%% of %d memory references are writes and every write goes to memory. How many writes reach main memory?" % (w * 100, lines * 10), int(lines * 10 * w), "Each write is propagated.")


@gen(S, CM, "Main memory", n=60, diff="medium")
def m_mem(r):
    kind = r.choice(["chips", "interleave", "refresh", "bw", "decoder"])
    if kind == "chips":
        tot, w, cap, cw = r.choice([(64, 32, 16, 8), (128, 16, 32, 8), (256, 32, 64, 8), (32, 8, 8, 1)])
        # total words tot K x w bits ; chip cap K x cw bits
        n = (tot // cap) * (w // cw)
        return nat(r, "A memory of %dK × %d bits is to be built from chips of %dK × %d bits. How many chips are needed?" % (tot, w, cap, cw), n, "(%d/%d) × (%d/%d) = %d." % (tot, cap, w, cw, n))
    if kind == "interleave":
        k, n, t = r.choice([2, 4, 8]), r.choice([8, 16, 32]), r.choice([40, 60, 80])
        return nat(r, "Memory is %d-way low-order interleaved with %d ns access time per module. Time (ns) to read %d consecutive words if the modules are accessed in parallel and each batch of %d words takes one access time?" % (k, t, n, k), (n // k) * t, "Batches = n/k; each costs one access time.")
    if kind == "refresh":
        rows, t, per = r.choice([4096, 8192]), r.choice([50, 60, 100]), r.choice([8, 16, 64])
        return nat(r, "A DRAM has %d rows; refreshing one row takes %d ns and every row must be refreshed every %d ms. Percentage of time spent refreshing? (up to 3 decimals)" % (rows, t, per), round(rows * t / (per * 1e6) * 100, 3), "rows × t_row / interval.", tol=0.002)
    if kind == "bw":
        w, f = r.choice([32, 64, 128]), r.choice([100, 200, 400, 800])
        return nat(r, "A memory bus is %d bits wide and transfers one word per cycle at %d MHz. Peak bandwidth in MB/s?" % (w, f), w // 8 * f, "bytes/cycle × MHz.")
    n = r.randint(8, 24)
    return nat(r, "A RAM chip has %d address lines and a single data line. Its capacity in Kbits is" % n, 2 ** n / 1024, "2^n bits ÷ 1024.")


# ---------------- I/O ----------------
@gen(S, IO, "I/O transfer methods", n=80, diff="medium", marks=2)
def o_io(r):
    kind = r.choice(["poll", "int", "dma", "rate", "cycles"])
    if kind == "poll":
        rate, cyc, f = r.choice([10, 50, 100, 200]), r.choice([100, 200, 400]), r.choice([500, 1000, 2000])
        return nat(r, "A device is polled %d times per second; each poll takes %d clock cycles. For a %d MHz CPU, what percentage of CPU time is used for polling? (up to 4 decimals)" % (rate * 1000, cyc, f), round(rate * 1000 * cyc / (f * 1e6) * 100, 4), "polls/s × cycles / f.", tol=0.0005)
    if kind == "int":
        t, b = r.choice([2, 4, 5, 10]), r.choice([1, 4, 8])
        return nat(r, "Servicing an interrupt takes %d µs and transfers %d byte(s). What is the maximum data rate (in KB/s, 1 KB = 1000 B) interrupt-driven I/O can sustain?" % (t, b), b / t * 1000, "bytes per interrupt / service time.")
    if kind == "dma":
        sz, bw, setup = r.choice([4, 8, 16, 64]) * 1024, r.choice([10, 20, 40, 100]), r.choice([100, 200, 500])
        return nat(r, "A DMA transfer moves %d bytes over a bus that provides %d MB/s (1 MB = 10^6 bytes). The CPU spends %d cycles setting up a 1 GHz processor. Total DMA transfer time in µs, including setup? (up to 2 decimals)" % (sz, bw, setup), round(sz / (bw * 1e6) * 1e6 + setup / 1000, 2), "transfer time + setup.", tol=0.02)
    if kind == "rate":
        words, cy = r.choice([128, 256, 512]), r.choice([2, 4])
        return nat(r, "In DMA cycle stealing, the DMA controller takes the bus for %d cycles per word. To transfer %d words, how many bus cycles does the CPU lose?" % (cy, words), cy * words, "Stolen cycles = words × cycles per word.")
    n = r.randint(3, 8)
    return nat(r, "In a daisy-chain priority interrupt system, devices are connected in a chain with device 1 nearest the CPU. If devices 1..%d all request interrupts simultaneously, which device is served first? (answer with its number)" % n, 1, "The device nearest the CPU in the chain has the highest priority.")
