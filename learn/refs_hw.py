"""Independent Python references for the hardware tools (used by lessons to verify worked examples and by
tools/make_hw_tests.py to test the JavaScript implementations)."""
import itertools
import struct


# ---------------- IEEE 754 ----------------
def ieee_bits(x, bits=32):
    fmt, n = (">f", 4) if bits == 32 else (">d", 8)
    return "".join(format(b, "08b") for b in struct.pack(fmt, x))


def ieee_value(s):
    bits = len(s)
    fmt, n = (">f", 4) if bits == 32 else (">d", 8)
    return struct.unpack(fmt, int(s, 2).to_bytes(n, "big"))[0]


# ---------------- two's complement ----------------
def twos(n, bits):
    return format(n % (1 << bits), "0%db" % bits)


def add_signed(a, b, bits):
    lo, hi = -(1 << (bits - 1)), (1 << (bits - 1)) - 1
    s = a + b
    raw = (a % (1 << bits)) + (b % (1 << bits))
    wrapped = ((s - lo) % (1 << bits)) + lo
    return {"sum": twos(wrapped, bits), "value": wrapped, "carry": 1 if raw >= (1 << bits) else 0, "overflow": 0 if lo <= s <= hi else 1}


# ---------------- Boolean minimisation (enumerate all cubes) ----------------
def cube_minterms(c):
    free = [i for i, ch in enumerate(c) if ch == "-"]
    base = [ch for ch in c]
    out = []
    for vals in itertools.product("01", repeat=len(free)):
        for i, v in zip(free, vals):
            base[i] = v
        out.append(int("".join(base), 2))
    return out


def primes(n, on, dc):
    allowed = set(on) | set(dc)
    cubes = ["".join(t) for t in itertools.product("01-", repeat=n)]
    good = [c for c in cubes if set(cube_minterms(c)) <= allowed and cube_minterms(c)]
    # maximal cubes only
    out = []
    for c in good:
        mc = set(cube_minterms(c))
        if not any(d != c and mc < set(cube_minterms(d)) for d in good):
            out.append(c)
    return sorted(out)


def min_cover(n, on, dc):
    P = primes(n, on, dc)
    if not on:
        return P, 0, 0
    lits = lambda c: len(c.replace("-", ""))
    for k in range(1, len(P) + 1):
        best = None
        for combo in itertools.combinations(P, k):
            cov = set()
            for c in combo:
                cov |= set(cube_minterms(c))
            if set(on) <= cov:
                L = sum(lits(c) for c in combo)
                if best is None or L < best:
                    best = L
        if best is not None:
            return P, k, best
    return P, 0, 0


# ---------------- cache ----------------
def cache_sim(addrs, size, block, assoc, policy):
    sets = max(1, size // (block * assoc))
    S = [[] for _ in range(sets)]
    hits = 0
    for a in addrs:
        blk = a // block
        s, tag = blk % sets, blk // sets
        if tag in S[s]:
            hits += 1
            if policy == "lru":
                S[s].remove(tag)
                S[s].append(tag)
        else:
            if len(S[s]) == assoc:
                S[s].pop(0)
            S[s].append(tag)
    return hits, len(addrs) - hits


# ---------------- 5-stage pipeline: cycle-by-cycle simulation ----------------
def pipe_sim(instrs, fwd, bp=0):
    """instrs: list of dicts {dst, src, load, branch}; returns total cycles"""
    n = len(instrs)
    stage = [-1] * n          # -1 = not fetched, 0 IF .. 4 WB, 5 finished
    ex_c = [None] * n
    mem_c = [None] * n
    wb_c = [None] * n
    id_c = [None] * n
    occ = [None] * 5
    cycle = 0
    nxt = 1
    occ[0] = 0                     # instruction 0 is in IF during cycle 1
    stage[0] = 0
    while any(s != 5 for s in stage):
        cycle += 1
        for s in (4, 3, 2, 1, 0):
            i = occ[s]
            if i is None:
                continue
            if s == 4:
                wb_c[i] = cycle
                stage[i] = 5
                occ[4] = None
                continue
            if s == 1:  # ID -> EX: operand availability
                ok = True
                for reg in set(instrs[i]["src"]):
                    prod = None
                    for j in range(i - 1, -1, -1):
                        if instrs[j]["dst"] == reg:
                            prod = j
                            break
                    if prod is None:
                        continue
                    if not fwd:
                        ok = ok and wb_c[prod] is not None and wb_c[prod] <= cycle
                    elif instrs[prod]["load"]:
                        ok = ok and mem_c[prod] is not None and mem_c[prod] <= cycle
                    else:
                        ok = ok and ex_c[prod] is not None and ex_c[prod] <= cycle
                if not ok:
                    continue
                id_c[i] = cycle
            if s == 0:  # IF -> ID: branch penalty
                if i > 0 and instrs[i - 1]["branch"]:
                    if id_c[i - 1] is None or cycle + 1 < id_c[i - 1] + 1 + bp:
                        continue
            if occ[s + 1] is None:
                occ[s + 1] = i
                occ[s] = None
                stage[i] = s + 1
                if s + 1 == 2:
                    ex_c[i] = cycle + 1
                if s + 1 == 3:
                    mem_c[i] = cycle + 1
        if nxt < n and occ[0] is None:
            occ[0] = nxt
            stage[nxt] = 0
            nxt += 1
    return cycle
