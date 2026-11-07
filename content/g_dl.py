"""Digital Logic — parametric generators."""
import itertools
import math
import struct

from content.kit import *

S = "DL"
BA, CC, NS, SQ = ("Boolean Algebra & Minimization", "Combinational Circuits", "Number Systems & Arithmetic", "Sequential Circuits")


# ---------- Quine-McCluskey ----------
def prime_implicants(minterms, n):
    cur = {(m, 0) for m in minterms}
    pis = set()
    while cur:
        nxt, used = set(), set()
        lst = sorted(cur)
        for i, a in enumerate(lst):
            for b in lst[i + 1:]:
                if a[1] == b[1]:
                    d = a[0] ^ b[0]
                    if d and d & (d - 1) == 0:
                        nxt.add((a[0] & ~d, a[1] | d)); used |= {a, b}
        pis |= cur - used
        cur = nxt
    return sorted(pis)


def covers(pi, m):
    return (m & ~pi[1]) == pi[0]


def lits(pi, n):
    return n - bin(pi[1]).count("1")


def analyse(minterms, n):
    pis = prime_implicants(minterms, n)
    ess = {pi for m in minterms for pi in [[p for p in pis if covers(p, m)]] if len(pi) == 1 for pi in pi}
    best = None
    for k in range(1, len(pis) + 1):
        for sub in itertools.combinations(pis, k):
            if all(any(covers(p, m) for p in sub) for m in minterms):
                lit = sum(lits(p, n) for p in sub)
                if best is None or (len(sub), lit) < best[:2]:
                    best = (len(sub), lit, sub)
        if best:
            break
    # minimum literals among minimum-term covers is what we report; also compute global min literals
    glob = None
    for k in range(1, len(pis) + 1):
        for sub in itertools.combinations(pis, k):
            if all(any(covers(p, m) for p in sub) for m in minterms):
                lit = sum(lits(p, n) for p in sub)
                glob = lit if glob is None else min(glob, lit)
    return pis, ess, best, glob


def pi_str(pi, n):
    names = "ABCD"[:n]
    s = ""
    for i in range(n):
        bit = 1 << (n - 1 - i)
        if pi[1] & bit: continue
        s += names[i] + ("" if pi[0] & bit else "'")
    return s or "1"


@gen(S, BA, "K-map / Quine-McCluskey", n=70, diff="medium")
def d_qm(r):
    n = r.choice([3, 4, 4])
    mt = sorted(r.sample(range(2 ** n), r.randint(4, 2 ** n - 4)))
    pis, ess, best, glob = analyse(mt, n)
    kind = r.choice(["npi", "nepi", "lit", "terms"])
    desc = "F(%s) = Σm(%s)" % (",".join("ABCD"[:n]), ", ".join(map(str, mt)))
    if kind == "npi": return nat(r, "%s. How many prime implicants does F have?" % desc, len(pis), "PIs: %s." % ", ".join(pi_str(p, n) for p in pis))
    if kind == "nepi": return nat(r, "%s. How many ESSENTIAL prime implicants does F have?" % desc, len(ess), "Essential PIs cover a minterm no other PI covers: %s." % ", ".join(pi_str(p, n) for p in ess))
    if kind == "terms": return nat(r, "%s. Minimum number of product terms in a minimal sum-of-products expression?" % desc, best[0], "Minimal cover: %s." % " + ".join(pi_str(p, n) for p in best[2]))
    return nat(r, "%s. Minimum total number of literals in a minimal SOP expression?" % desc, glob, "Minimal cover found by exhaustive search: %d literals." % glob)


@gen(S, BA, "K-map / Quine-McCluskey", n=40, diff="hard", marks=2)
def d_qm_dc(r):
    n = 4
    pool = list(range(16))
    r.shuffle(pool)
    mt, dc = sorted(pool[:r.randint(5, 8)]), sorted(pool[8:8 + r.randint(2, 4)])
    pis = prime_implicants(mt + dc, n)
    pis_useful = [p for p in pis if any(covers(p, m) for m in mt)]
    best = None
    for k in range(1, len(pis_useful) + 1):
        for sub in itertools.combinations(pis_useful, k):
            if all(any(covers(p, m) for p in sub) for m in mt):
                lit = sum(lits(p, n) for p in sub)
                if best is None or lit < best[0]: best = (lit, sub)
        if best: break
    return nat(r, "F(A,B,C,D) = Σm(%s) + d(%s) (d = don't care). Using don't-cares optimally, what is the minimum number of product terms in a minimal SOP?" % (", ".join(map(str, mt)), ", ".join(map(str, dc))), len(best[1]),
               "Minimal cover: %s." % " + ".join(pi_str(p, n) for p in best[1]))


@gen(S, BA, "Minterms & functions", n=50, diff="easy")
def d_min(r):
    n = r.randint(3, 6)
    k = r.randint(1, n)
    kind = r.choice(["cover", "total", "dual", "maxterm", "nand"])
    if kind == "cover": return nat(r, "In a Boolean function of %d variables, a product term has %d literals. How many minterms does the term cover?" % (n, k), 2 ** (n - k), "2^(n−k) = %d." % 2 ** (n - k))
    if kind == "total": return nat(r, "Number of distinct minterms possible for %d Boolean variables?" % n, 2 ** n, "2^n.")
    if kind == "dual": return nat(r, "A function of %d variables has %d minterms (value 1). How many maxterms (value 0) does it have?" % (n, 2 ** (n - 1) - 1), 2 ** n - 2 ** (n - 1) + 1, "Total 2^n minus the minterms.")
    if kind == "maxterm": return mcq(r, "The complement of the function F = Σm(0,1,%d) over 3 variables is the function Σm of" % (r.randint(3, 7)), "the remaining five minterms", ["the same minterms", "the same three minterms inverted", "the maxterms 0,1"], "Complement swaps 1s and 0s: 8 − 3 = 5 minterms.")
    return nat(r, "Minimum number of 2-input NAND gates needed to realise XOR(A,B)?", 4, "Classic: N1 = NAND(A,B); N2 = NAND(A,N1); N3 = NAND(B,N1); N4 = NAND(N2,N3).")


BAEXPR = [("AB + A'C + BC", lambda A, B, C: (A and B) or ((not A) and C) or (B and C)), ("AB + A'C", lambda A, B, C: (A and B) or ((not A) and C)),
          ("A + A'B", lambda A, B, C: A or B), ("A + B", lambda A, B, C: A or B), ("A(A + B)", lambda A, B, C: A), ("A", lambda A, B, C: A),
          ("(A + B)(A + C)", lambda A, B, C: A or (B and C)), ("A + BC", lambda A, B, C: A or (B and C)), ("AB + AB'", lambda A, B, C: A),
          ("(A + B')B", lambda A, B, C: A and B), ("AB", lambda A, B, C: A and B), ("A'B + AB'", lambda A, B, C: A != B), ("A ⊕ B", lambda A, B, C: A != B),
          ("(A + B)(A' + B')", lambda A, B, C: A != B), ("(AB)'", lambda A, B, C: not (A and B)), ("A' + B'", lambda A, B, C: (not A) or (not B)),
          ("(A + B)'", lambda A, B, C: not (A or B)), ("A'B'", lambda A, B, C: (not A) and (not B)), ("AB + A'B'", lambda A, B, C: A == B), ("(A ⊕ B)'", lambda A, B, C: A == B),
          ("A ⊕ B ⊕ C", lambda A, B, C: (A != B) != C), ("ABC + AB'C' + A'BC' + A'B'C", lambda A, B, C: (A != B) != C), ("AB + BC + CA", lambda A, B, C: (A + B + C) >= 2),
          ("A + A'", lambda A, B, C: True), ("AA'", lambda A, B, C: False), ("A(B + C)", lambda A, B, C: A and (B or C)), ("AB + AC", lambda A, B, C: A and (B or C))]


def btt(f):
    return tuple(bool(f(*v)) for v in itertools.product([False, True], repeat=3))


@gen(S, BA, "Boolean identities", n=60, diff="medium", marks=2)
def d_equiv(r):
    base = r.choice(BAEXPR)
    eq = [x for x in BAEXPR if btt(x[1]) == btt(base[1]) and x[0] != base[0]]
    ne = [x for x in BAEXPR if btt(x[1]) != btt(base[1])]
    if not eq or len(ne) < 3: raise Skip()
    cs = r.sample(eq, min(len(eq), r.choice([1, 2])))
    ws = r.sample(ne, 4 - len(cs))
    return msq(r, "Which of the following expressions are equivalent to  %s ?  (select all)" % base[0], [c[0] for c in cs], [w[0] for w in ws], "Compare truth tables for A, B, C.")


@gen(S, BA, "Gates", n=20, diff="easy")
def d_gates(r):
    n = r.randint(2, 8)
    kind = r.choice(["xor_odd", "nand_and", "universal", "fanin", "xnor"])
    if kind == "xor_odd": return nat(r, "An n-input XOR gate outputs 1 iff an odd number of inputs are 1. For n = %d, how many of the %d input combinations give output 1?" % (n, 2 ** n), 2 ** (n - 1), "Exactly half of the combinations have odd parity.")
    if kind == "nand_and": return nat(r, "Minimum number of 2-input NAND gates needed to implement a 2-input AND gate?", 2, "NAND followed by NAND with both inputs tied (inverter).")
    if kind == "universal": return mcq(r, "Which pair of gate sets is functionally complete (universal)?", "{NAND} alone", ["{AND, OR}", "{XOR, AND}" if False else "{AND, OR, XOR} without constants", "{XOR, XNOR}"], "NAND (and NOR) alone can build NOT, AND and OR.")
    if kind == "fanin": return nat(r, "Minimum number of 2-input gates needed to build a %d-input AND gate (tree of 2-input ANDs)?" % n, n - 1, "n − 1 two-input gates.")
    return nat(r, "A 2-input XNOR gate: for how many of the 4 input combinations is the output 1?", 2, "XNOR is 1 when inputs are equal.")


# ---------- combinational circuits ----------
@gen(S, CC, "MUX / Decoder", n=55, diff="easy")
def c_mux(r):
    kind = r.choice(["sel", "tree", "mux_from_2", "dec", "dec_tree", "mux_func", "rom", "enc"])
    k = r.randint(2, 6)
    if kind == "sel": return nat(r, "How many select lines does a %d:1 multiplexer have?" % 2 ** k, k, "log₂ %d = %d." % (2 ** k, k))
    if kind == "tree": return nat(r, "Minimum number of 4:1 multiplexers needed to build a %d:1 multiplexer?" % 4 ** min(k, 3), sum(4 ** i for i in range(min(k, 3))), "Tree: 1 + 4 + … = %d." % sum(4 ** i for i in range(min(k, 3))))
    if kind == "mux_from_2": return nat(r, "Minimum number of 2:1 multiplexers needed to build a %d:1 multiplexer?" % 2 ** k, 2 ** k - 1, "N − 1 two-to-one muxes.")
    if kind == "dec": return nat(r, "A %d-to-%d decoder has how many output lines?" % (k, 2 ** k), 2 ** k, "2^k outputs.")
    if kind == "dec_tree": return nat(r, "Minimum number of 3-to-8 decoders (with enable) needed to build a 5-to-32 decoder?", 5, "Four decoders for the 32 outputs plus one more to drive their enables.")
    if kind == "mux_func": return nat(r, "A Boolean function of %d variables is implemented with ONE multiplexer: %d variables drive the select lines and the remaining variable (or its complement, or constants) drives the data inputs. How many data inputs must the multiplexer have?" % (k + 1, k), 2 ** k, "k select lines ⇒ 2^k data inputs.")
    if kind == "rom": return nat(r, "A ROM has %d address lines and %d data lines. How many bits can it store?" % (k + 4, 2 ** (k % 3 + 1)), 2 ** (k + 4) * 2 ** (k % 3 + 1), "2^address × width.")
    return nat(r, "A binary encoder has %d input lines (only one active at a time). How many output lines?" % 2 ** k, k, "log₂ of inputs.")


@gen(S, CC, "Adders", n=50, diff="medium")
def c_adder(r):
    n, d = r.choice([4, 8, 16, 32, 64]), r.choice([1, 2, 3, 4])
    kind = r.choice(["ripple", "fa", "cla", "ha", "gates", "sub"])
    if kind == "ripple": return nat(r, "An %d-bit ripple-carry adder has a carry propagation delay of %d ns per full adder. What is the worst-case delay (ns) to produce the final carry-out?" % (n, d), n * d, "n × carry delay = %d ns." % (n * d))
    if kind == "fa": return nat(r, "How many full adders are needed to build an %d-bit ripple-carry adder (assume a carry-in is available)?" % n, n, "One per bit.")
    if kind == "cla": return nat(r, "In a 4-bit carry-look-ahead adder each generate/propagate term takes 1 gate delay, the look-ahead carry takes 2 gate delays and each sum bit XOR takes 1 more. Delay (gate delays) to produce all sum bits?", 4, "1 (g,p) + 2 (carry) + 1 (sum) = 4.")
    if kind == "ha": return nat(r, "A full adder is built from two half adders and one OR gate. A half adder consists of one XOR gate and one AND gate. Total number of 2-input gates in the full adder?", 5, "2 × (XOR + AND) + OR = 5 gates.")
    if kind == "gates": return nat(r, "Minimum number of 2-input NAND gates required to implement one half adder (sum and carry)?", 5, "Classic NAND-only half adder uses 5 NAND gates.")
    return mcq(r, "To subtract B from A in n-bit two's complement using an adder, we", "complement B bitwise, add 1 (carry-in), and add to A", ["complement A and add B", "add A and B then complement the sum", "subtract using a half adder only"], "A − B = A + ~B + 1.")


# ---------- number systems ----------
def to_base(n, b):
    digs = "0123456789ABCDEF"
    if n == 0: return "0"
    s = ""
    while n:
        s = digs[n % b] + s; n //= b
    return s


@gen(S, NS, "Base conversion", n=70, diff="easy")
def n_base(r):
    v = r.randint(20, 4000)
    a, b = r.sample([2, 8, 10, 16], 2)
    return mcq(r, "Convert (%s)%s to base %d." % (to_base(v, a), {2: "₂", 8: "₈", 10: "₁₀", 16: "₁₆"}[a], b), to_base(v, b),
               [to_base(v + d, b) for d in (1, -1, 8, -8, 16, 2)], "Value = %d in decimal; in base %d it is %s." % (v, b, to_base(v, b)))


@gen(S, NS, "Two's complement", n=80, diff="medium")
def n_twos(r):
    bits = r.choice([4, 5, 6, 8, 12, 16])
    kind = r.choice(["range_min", "range_max", "repr", "decode", "overflow", "sign_ext", "count", "ones"])
    lo, hi = -2 ** (bits - 1), 2 ** (bits - 1) - 1
    if kind == "range_min": return nat(r, "Smallest integer representable in %d-bit two's complement?" % bits, lo, "−2^(n−1) = %d." % lo)
    if kind == "range_max": return nat(r, "Largest integer representable in %d-bit two's complement?" % bits, hi, "2^(n−1) − 1 = %d." % hi)
    if kind == "repr":
        v = r.randint(lo, -1)
        h = format(v & (2 ** bits - 1), "0%db" % bits)
        return mcq(r, "Representation of %d in %d-bit two's complement is" % (v, bits), h, [format((-v) & (2 ** bits - 1) ^ (1 << r.randrange(bits)), "0%db" % bits), format(abs(v), "0%db" % bits), format((~abs(v)) & (2 ** bits - 1), "0%db" % bits), format((v - 1) & (2 ** bits - 1), "0%db" % bits)], "Invert |v| and add 1: %s." % h)
    if kind == "decode":
        pat = r.randint(0, 2 ** bits - 1)
        v = pat - 2 ** bits if pat >= 2 ** (bits - 1) else pat
        return nat(r, "The %d-bit pattern %s is interpreted as a two's complement number. Its decimal value is" % (bits, format(pat, "0%db" % bits)), v, "Sign bit weight is −2^%d." % (bits - 1))
    if kind == "overflow":
        a, b = r.randint(lo, hi), r.randint(lo, hi)
        ov = not (lo <= a + b <= hi)
        return mcq(r, "In %d-bit two's complement, adding %d and %d" % (bits, a, b), "produces overflow" if ov else "does not overflow", ["does not overflow" if ov else "produces overflow", "always sets the carry flag", "gives a result of 0"],
                   "True sum %d is %s the range [%d, %d]." % (a + b, "outside" if ov else "inside", lo, hi))
    if kind == "sign_ext":
        v = r.randint(lo, hi)
        return nat(r, "A %d-bit two's complement number with value %d is sign-extended to %d bits. What is its decimal value?" % (bits, v, bits * 2), v, "Sign extension preserves value.")
    if kind == "count": return nat(r, "How many distinct numerical values can an n = %d bit sign-magnitude representation hold (+0 and −0 are the same value)?" % bits, 2 ** bits - 1, "2^n patterns but +0 and −0 are the same value ⇒ 2^n − 1.")
    return nat(r, "Smallest integer in %d-bit ones' complement?" % bits, -(2 ** (bits - 1) - 1), "−(2^(n−1) − 1).")


def hexf(x):
    return struct.pack(">f", x).hex().upper()


def f_from_hex(h):
    return struct.unpack(">f", bytes.fromhex(h))[0]


@gen(S, NS, "IEEE 754", n=80, diff="hard", marks=2)
def n_ieee(r):
    m = r.randint(1, 31)
    e = r.randint(-6, 8)
    s = r.choice([1, -1])
    x = s * (1 + m / 32) * 2 ** e
    h = hexf(x)
    kind = r.choice(["enc", "dec", "exp", "bias"])
    if kind == "enc":
        wrong = {hexf(-x), hexf(x * 2), hexf(x / 2), hexf(s * (1 + (m ^ 1) / 32) * 2 ** e)}
        return mcq(r, "IEEE 754 single-precision (32-bit) hexadecimal representation of %s is" % fmt(x), "0x" + h, ["0x" + w for w in wrong], "sign=%d, exponent=%d+127=%d, mantissa=%s." % (s < 0, e, e + 127, format(m, "05b") + "0" * 18))
    if kind == "dec":
        return nat(r, "The 32-bit pattern 0x%s is an IEEE 754 single-precision number. Its decimal value is (up to 4 decimals)" % h, dec4(x), "Decode sign, exponent − 127, 1.mantissa.", tol=0.0005)
    if kind == "exp": return nat(r, "For the IEEE 754 single-precision number 0x%s, what is the unbiased exponent (decimal)?" % h, e, "Biased exponent − 127 = %d." % e)
    return nat(r, "In IEEE 754 single precision the stored (biased) exponent field of the number %s is" % fmt(x), e + 127, "Stored = true exponent + 127 = %d." % (e + 127))


def dec4(x):
    return round(x, 4)


@gen(S, NS, "Number facts", n=35, diff="easy")
def n_misc(r):
    kind = r.choice(["bits", "gray", "bcd", "excess", "ieee_facts"])
    n = r.randint(10, 5000)
    if kind == "bits": return nat(r, "Minimum number of bits needed to represent %d distinct values?" % n, math.ceil(math.log2(n)), "⌈log₂ n⌉.")
    if kind == "gray":
        g = n ^ (n >> 1)
        return mcq(r, "Gray code of the binary number %s is" % format(n, "b"), format(g, "b"), [format(n ^ (n >> 2), "b"), format(n, "b")[::-1], format(g ^ 1, "b"), format(~n & (2 ** n.bit_length() - 1), "b")], "g = b XOR (b >> 1).")
    if kind == "bcd": return nat(r, "Number of bits needed to store the decimal number %d in BCD?" % n, 4 * len(str(n)), "4 bits per decimal digit.")
    if kind == "excess": return nat(r, "In IEEE 754 double precision the exponent bias is", 1023, "11-bit exponent: bias = 2^10 − 1 = 1023.")
    return nat(r, "Number of bits in the mantissa (fraction) field of IEEE 754 single precision?", 23, "1 sign + 8 exponent + 23 fraction.")


# ---------- sequential ----------
@gen(S, SQ, "Flip-flops", n=45, diff="medium")
def q_ff(r):
    kind = r.choice(["jk", "d", "t", "excite", "sr"])
    q = r.randint(0, 1)
    if kind == "jk":
        j, k = r.randint(0, 1), r.randint(0, 1)
        nq = (j & (1 - q)) | ((1 - k) & q)
        return nat(r, "A JK flip-flop has current state Q = %d, J = %d, K = %d. What is Q after the next clock edge?" % (q, j, k), nq, "Q⁺ = JQ' + K'Q = %d." % nq)
    if kind == "d":
        d = r.randint(0, 1)
        return nat(r, "A D flip-flop currently has Q = %d. D = %d at the clock edge. Next Q?" % (q, d), d, "Q⁺ = D.")
    if kind == "t":
        t = r.randint(0, 1)
        return nat(r, "A T flip-flop has Q = %d and T = %d. Q after the clock edge?" % (q, t), q ^ t, "Q⁺ = T ⊕ Q.")
    if kind == "sr":
        return mcq(r, "In an SR flip-flop built from NOR gates, the forbidden input combination is", "S = 1, R = 1", ["S = 0, R = 0", "S = 1, R = 0", "S = 0, R = 1"], "Both outputs would be forced to 0, and the next state is unpredictable.")
    a, b = r.randint(0, 1), r.randint(0, 1)
    table = {(0, 0): "J = 0, K = X", (0, 1): "J = 1, K = X", (1, 0): "J = X, K = 1", (1, 1): "J = X, K = 0"}
    return mcq(r, "To make a JK flip-flop go from Q = %d to Q⁺ = %d, the required inputs are" % (a, b), table[(a, b)], [v for k, v in table.items() if k != (a, b)], "JK excitation table.")


@gen(S, SQ, "Counters & registers", n=70, diff="easy")
def q_cnt(r):
    kind = r.choice(["modn", "ring", "johnson", "after", "freq", "ripple", "shift", "states", "johnson_after"])
    n = r.randint(5, 200)
    k = r.randint(3, 10)
    if kind == "modn": return nat(r, "Minimum number of flip-flops needed to build a mod-%d counter?" % n, math.ceil(math.log2(n)), "⌈log₂ N⌉.")
    if kind == "ring": return nat(r, "A ring counter built from %d flip-flops has how many distinct states in its normal cycle?" % k, k, "n states.")
    if kind == "johnson": return nat(r, "A Johnson (twisted-ring) counter built from %d flip-flops has how many distinct states in its normal cycle?" % k, 2 * k, "2n states.")
    if kind == "after":
        w, init, c = r.choice([3, 4, 5, 6]), 0, r.randint(10, 100)
        init = r.randint(0, 2 ** w - 1)
        return nat(r, "A %d-bit binary up-counter currently holds %d. What decimal value does it hold after %d clock pulses?" % (w, init, c), (init + c) % 2 ** w, "(init + pulses) mod 2^%d." % w)
    if kind == "freq":
        f, m = r.choice([1, 2, 4, 8, 16, 32]), r.randint(3, 8)
        return nat(r, "A clock of %d MHz drives a %d-bit ripple counter. What is the frequency (in kHz) at the MSB output? (up to 3 decimals)" % (f, m), round(f * 1000 / 2 ** m, 3), "f / 2^n.", tol=0.001)
    if kind == "ripple":
        d, m = r.choice([5, 10, 20]), r.randint(3, 8)
        return nat(r, "Each flip-flop in an asynchronous %d-bit ripple counter has a propagation delay of %d ns. Minimum clock period (ns) so all outputs settle before the next clock edge (ignore setup)?" % (m, d), m * d, "Delays accumulate through the chain: n × t_pd.")
    if kind == "states": return nat(r, "A sequential circuit with %d flip-flops can have at most how many distinct states?" % k, 2 ** k, "2^n.")
    if kind == "johnson_after":
        w, c = r.choice([4, 5, 6]), r.randint(1, 20)
        st = 0
        for _ in range(c): st = ((st << 1) | (1 - (st >> (w - 1) & 1))) & (2 ** w - 1)
        return nat(r, "A %d-bit Johnson counter starts at 0 and shifts left feeding back the complement of the MSB. After %d clock pulses the register holds the value (decimal)?" % (w, c), st, "Simulate the shift/feedback.")
    w, bits = r.choice([4, 5, 6, 8]), None
    return nat(r, "A %d-bit serial-in shift register needs how many clock pulses to load a complete %d-bit word?" % (w, w), w, "One bit per clock.")


@gen(S, SQ, "Timing & FSM", n=45, diff="medium", marks=2)
def q_fsm(r):
    kind = r.choice(["fmax", "states_mealy", "moore", "ff", "setup"])
    if kind == "fmax":
        tpd, tc, ts = r.choice([2, 3, 5]), r.choice([8, 10, 12, 15, 20]), r.choice([1, 2, 3])
        return nat(r, "In a synchronous circuit, flip-flop clock-to-Q delay is %d ns, combinational logic delay %d ns and setup time %d ns (ignore skew). Maximum clock frequency in MHz? (up to 2 decimals)" % (tpd, tc, ts), round(1000 / (tpd + tc + ts), 2), "f = 1/(t_cq + t_comb + t_setup).", tol=0.01)
    if kind == "states_mealy":
        L = r.randint(3, 6)
        pat = "".join(r.choice("01") for _ in range(L))
        return nat(r, "Minimum number of states in a MEALY machine that detects the (overlapping) sequence %s on a serial input?" % pat, L, "A Mealy detector for a length-L pattern needs L states.")
    if kind == "moore":
        L = r.randint(3, 6)
        pat = "".join(r.choice("01") for _ in range(L))
        return nat(r, "Minimum number of states in a MOORE machine that detects the (overlapping) sequence %s?" % pat, L + 1, "Moore needs L + 1 states.")
    if kind == "ff":
        s = r.randint(5, 40)
        return nat(r, "A finite state machine has %d states. Minimum number of flip-flops needed for a binary state encoding?" % s, math.ceil(math.log2(s)), "⌈log₂ s⌉.")
    return mcq(r, "A flip-flop's hold time violation can be fixed by", "adding delay to the data path", ["reducing the clock frequency", "increasing the supply voltage", "removing the flip-flop reset"], "Hold violations are independent of clock period; extra data-path delay fixes them.")
