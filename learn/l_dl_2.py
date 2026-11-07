"""Digital Logic part 2: number systems & arithmetic, floating point, sequential circuits."""
import math

from learn import Ex, lesson
from learn.refs_hw import add_signed, ieee_bits, ieee_value, twos

S = "DL"


def hexbits(x, bits=32):
    return "%0*X" % (bits // 4, int(ieee_bits(x, bits), 2))


def gray(n):
    return n ^ (n >> 1)


def sim_counter(kind, n, steps):
    """state sequences for common shift-register counters"""
    s = [1] + [0] * (n - 1) if kind == "ring" else [0] * n
    seen = []
    for _ in range(steps):
        seen.append(tuple(s))
        s = [s[-1] if kind == "ring" else 1 - s[-1]] + s[:-1]
    return seen


def period(kind, n):
    seq = sim_counter(kind, n, 4 * n)
    return seq.index(seq[0], 1)


def t_counter(n, steps):
    q = [0] * n
    out = []
    for _ in range(steps):
        out.append(sum(b << i for i, b in enumerate(q)))
        t = [1] + [int(all(q[:i])) for i in range(1, n)]
        q = [b ^ ti for b, ti in zip(q, t)]
    return out


# ======================================================================================================
lesson(subject=S, chapter="Number Systems", ch_no=2, no=1, slug="dl-number-systems", title="Number Systems, Complements & Binary Arithmetic",
       topic="Number Systems & Arithmetic", minutes=22, weight=5, widget="numsys",
       widget_hint="Enter a decimal number and a word size to see its binary, hex and two's-complement forms; then add two numbers to see carry and signed overflow.",
       key="Computers store integers in binary using sign-magnitude, one's complement or (almost always) two's complement. In n-bit two's complement the range is −2ⁿ⁻¹ … 2ⁿ⁻¹ − 1, subtraction is addition of the complement, and signed overflow occurs when two operands of the same sign give a result of the opposite sign.",
       analogy=("🧭", "A clock face", "On a 12-hour clock, going back 3 hours is the same as going forward 9. Two's complement is that wrap-around idea in binary: −3 in 4 bits is simply 16 − 3 = 13 (1101), and ordinary addition just works."),
       sections=[
           dict(h="Positional systems and conversion", md="""A number in base r: dₙ…d₁d₀.d₋₁d₋₂ = Σ dᵢ·rⁱ.

- **Integer part to base r:** repeatedly divide by r, collect remainders (last remainder is the MSB).
- **Fraction part to base r:** repeatedly multiply by r, collect the integer parts.
- **Binary ↔ octal / hex:** group bits in threes / fours from the radix point.
- (1011.101)₂ = 8 + 2 + 1 + 0.5 + 0.125 = **11.625**.
- Digits needed: n-bit unsigned represents 0 … 2ⁿ − 1; to represent N values you need ⌈log₂ N⌉ bits; a decimal number D needs ⌈log₂(D + 1)⌉ bits."""),
           dict(h="Signed number representations", md="""| Scheme | Negative of x | Range (n bits) | Zeros |
|---|---|---|---|
| **Sign-magnitude** | flip the sign bit | −(2ⁿ⁻¹ − 1) … 2ⁿ⁻¹ − 1 | two |
| **One's complement** | flip all bits | −(2ⁿ⁻¹ − 1) … 2ⁿ⁻¹ − 1 | two |
| **Two's complement** | flip all bits, add 1 | **−2ⁿ⁻¹ … 2ⁿ⁻¹ − 1** | one |
| **Excess-k (biased)** | x + k | depends | one |

Two's complement of x equals 2ⁿ − x. Sign extension: replicate the sign bit to widen a number. The value of a two's complement number is −b₍ₙ₋₁₎2ⁿ⁻¹ + Σ bᵢ2ⁱ. The most negative number (1000…0) has no positive counterpart, and negating it overflows.""",
                formulas=[("range of n-bit two's complement: −2ⁿ⁻¹ … 2ⁿ⁻¹ − 1", "signed integers")]),
           dict(h="Addition, overflow and carry", md="""Binary addition works the same in two's complement for signed and unsigned numbers; only the *interpretation* of flags differs:

- **Carry out of the MSB** signals *unsigned* overflow.
- **Signed overflow** occurs when the operands have the **same sign** and the result has the **opposite sign** — equivalently, **carry into the MSB ≠ carry out of the MSB**. Adding numbers of different signs can never overflow.
- Subtraction A − B = A + (−B): invert B and add with carry-in 1. In 8 bits, 100 + 45 = 145 > 127 ⇒ overflow (result 10010001 = −111)."""),
           dict(h="BCD, Gray code and parity", md="""- **BCD:** each decimal digit in 4 bits (0000–1001); a 4-digit BCD number uses 16 bits. BCD addition adds 6 (0110) when a digit sum exceeds 9. **Excess-3** is self-complementing.
- **Gray code:** consecutive values differ in one bit; g = n ⊕ (n ≫ 1). 3-bit Gray: 000, 001, 011, 010, 110, 111, 101, 100. It is used in K-maps and position encoders.
- **Parity:** an even-parity bit makes the number of 1s even; detects any single-bit (odd number of) errors. **Hamming code** with r check bits corrects one error when 2ʳ ≥ m + r + 1 (m data bits)."""),
       ],
       examples=[
           Ex("Two's complement range and encoding", "What is the 8-bit two's complement representation of −37, and what is the range?",
              ["37 = 00100101; invert: 11011010; add 1: 11011011.", "Range = −128 … +127."],
              "**11011011**; range −**128** … **127**.", verify=lambda: "%s; range −%d … %d" % (twos(-37, 8), 2 ** 7, 2 ** 7 - 1)),
           Ex("Signed overflow", "In 8-bit two's complement, add 100 and 45. What are the result bits, the interpreted value, carry-out and overflow?",
              ["100 = 01100100, 45 = 00101101; sum = 10010001.", "Interpreted as signed this is −111 (wrong). Carry-out is 0 but both operands were positive and the result negative ⇒ overflow = 1."],
              "10010001 = −111, carry 0, overflow **1**.", verify=lambda: (lambda r: "%s = %d, carry %d, overflow %d" % (r["sum"], r["value"], r["carry"], r["overflow"]))(add_signed(100, 45, 8))),
           Ex("Bits needed", "How many bits are needed to represent the unsigned decimal number 1000, and in BCD?",
              ["Binary: ⌈log₂ 1001⌉ = 10 bits (2¹⁰ = 1024).", "BCD: 4 digits × 4 bits = 16 bits."],
              "**10** bits binary; **16** bits BCD.", verify=lambda: "%d bits binary; %d bits BCD" % (math.ceil(math.log2(1001)), 4 * 4)),
           Ex("Gray code", "What is the Gray code of decimal 11, and how many bit changes occur between Gray(7) and Gray(8)?",
              ["Gray(11) = 1011 ⊕ 0101 = 1110.", "Gray(7) = 0100, Gray(8) = 1100 differ in 1 bit."],
              "Gray(11) = **1110**; **1** bit changes.", verify=lambda: "Gray(11) = %s; %d bit changes" % (format(gray(11), "04b"), bin(gray(7) ^ gray(8)).count("1"))),
       ],
       traps=[("Overflow vs carry", "Carry out is for unsigned numbers; signed overflow compares the carries into and out of the MSB."),
              ("Most negative number", "−2ⁿ⁻¹ cannot be negated within n bits."),
              ("Sign extension", "Replicate the sign bit, do not pad with zeros for negative numbers."),
              ("Sign-magnitude / one's complement", "Both have +0 and −0.")],
       quick=[("Range of 6-bit two's complement is", ["−32…31", "−31…31", "0…63", "−64…63"], 0, "−2⁵ … 2⁵−1."),
              ("Signed overflow occurs when", ["there is a carry out", "operands have same sign and result differs", "operands differ in sign", "result is zero"], 1, "Same sign in, different sign out."),
              ("(1011.101)₂ equals", ["11.5", "11.625", "13.625", "10.625"], 1, "8+2+1+0.5+0.125."),
              ("Consecutive Gray codes differ in", ["1 bit", "2 bits", "all bits", "it varies"], 0, "By definition.")],
       summary=["Convert by division (integer) and multiplication (fraction); group bits for octal/hex.", "Two's complement: invert and add 1; range −2ⁿ⁻¹…2ⁿ⁻¹−1; one zero.", "Sign-magnitude and one's complement have two zeros.",
                "Signed overflow: same-sign operands, opposite-sign result (C_in ≠ C_out at MSB).", "BCD uses 4 bits per digit; Gray code changes one bit per step.", "Hamming: 2ʳ ≥ m + r + 1."])


# ======================================================================================================
lesson(subject=S, chapter="Number Systems", ch_no=2, no=2, slug="dl-floating-point", title="Floating-Point Numbers (IEEE 754)",
       topic="Number Systems & Arithmetic", minutes=20, weight=4, widget="ieee",
       widget_hint="Type a decimal value to see its sign, biased exponent and fraction bits, or paste a bit pattern to decode it. Try 0.1, −5.75, 1e-40 and a pattern with exponent all ones.",
       key="IEEE 754 stores a number as sign, biased exponent and fraction with an implicit leading 1: value = (−1)^s × 1.f × 2^(e − bias). Single precision has 1 + 8 + 23 bits (bias 127), double has 1 + 11 + 52 (bias 1023); special exponents encode zero, denormals, infinity and NaN.",
       analogy=("🔬", "Scientific notation in binary", "Writing 5,750 as 5.75 × 10³ separates the digits from the scale. IEEE 754 does the same in base 2: a fraction, a power of two and a sign. Only finitely many bits for each, so most real numbers are rounded."),
       sections=[
           dict(h="The format", md="""| Format | Sign | Exponent | Fraction | Bias |
|---|---|---|---|---|
| **Single (32-bit)** | 1 | 8 | 23 | 127 |
| **Double (64-bit)** | 1 | 11 | 52 | 1023 |

For a **normal** number (exponent field 1 … max − 1): value = (−1)ˢ × (1 + F/2^m) × 2^(E − bias), where m is the fraction width. The leading 1 is *implicit* (hidden bit), giving m + 1 bits of precision.

Special exponent fields:

- exponent 0, fraction 0: **±0**.
- exponent 0, fraction ≠ 0: **denormal**, value (−1)ˢ × 0.F × 2^(1 − bias).
- exponent all 1s, fraction 0: **±∞**.
- exponent all 1s, fraction ≠ 0: **NaN**."""),
           dict(h="Encoding a number", md="""To encode x: (1) convert |x| to binary; (2) normalise to 1.xxx × 2ᵉ; (3) store the biased exponent e + bias; (4) store the bits after the point as the fraction (rounded to nearest even); (5) set the sign bit.

Example: −5.75 = −101.11₂ = −1.0111 × 2² ⇒ sign 1, exponent 2 + 127 = 129 = 10000001, fraction 0111000…0 ⇒ **C0B80000** in hex.""",
                call=[("trap", "0.1 is not exact", "Decimal 0.1 has an infinite binary expansion, so the stored value is a rounded approximation (single: 0x3DCCCCCD ≈ 0.100000001490116).")]),
           dict(h="Range, precision and arithmetic", md="""- **Largest single:** (2 − 2⁻²³) × 2¹²⁷ ≈ 3.4 × 10³⁸. **Smallest normal:** 2⁻¹²⁶ ≈ 1.2 × 10⁻³⁸. **Smallest denormal:** 2⁻¹⁴⁹.
- **Machine epsilon** (gap above 1.0) = 2⁻²³ single, 2⁻⁵² double. Relative precision ≈ 7 decimal digits (single), ≈ 16 (double).
- The gap between neighbouring numbers doubles every time the exponent increases: large numbers are less precise in absolute terms.
- **Addition:** align exponents (shift the smaller mantissa right), add, normalise, round. Floating-point addition is **not associative**; adding a very small number to a very large one may lose it completely.
- **Rounding modes:** nearest-even (default), toward 0, toward +∞, toward −∞. NaN ≠ NaN. Comparing floating-point numbers for equality is therefore risky: compare with a tolerance instead. Converting an integer with more than 24 significant bits to single precision loses its low-order bits, which is why 16,777,217 cannot be stored exactly."""),
       ],
       examples=[
           Ex("Encode a number", "Give the IEEE 754 single-precision hexadecimal representation of −5.75.",
              ["−5.75 = −1.0111 × 2²; exponent field = 2 + 127 = 129 = 10000001; fraction = 0111 followed by zeros.", "Bits: 1 10000001 01110000000000000000000 = **C0B80000**."],
              "**C0B80000**", verify=lambda: hexbits(-5.75)),
           Ex("Decode a number", "What value does the single-precision pattern 0x41C80000 represent?",
              ["Binary 0 10000011 10010000…: exponent 131 − 127 = 4; mantissa 1.1001 = 1.5625.", "Value = 1.5625 × 2⁴ = **25.0**."],
              "**25**", verify=lambda: "%g" % ieee_value("{:032b}".format(0x41C80000))),
           Ex("Largest single-precision number", "What is the largest finite single-precision value (approximately)?",
              ["Exponent field 11111110 = 254 ⇒ 2^127; fraction all ones ⇒ 1.111…1 = 2 − 2⁻²³.", "Value = (2 − 2⁻²³) × 2¹²⁷ ≈ **3.40 × 10³⁸**."],
              "≈ **3.40 × 10³⁸**", verify=lambda: "%.2f × 10³⁸" % ((2 - 2 ** -23) * 2 ** 127 / 1e38)),
           Ex("Precision loss", "In single precision, is 16777216 + 1 equal to 16777217?",
              ["16777216 = 2²⁴ and 24 bits of mantissa precision are exhausted: the spacing of floats near 2²⁴ is 2.", "So 16777217 rounds to 16777216: **no**."],
              "**No**, it rounds back to 16777216.", verify=lambda: "No" if ieee_value(ieee_bits(16777217.0, 32)) == 16777216.0 else "Yes"),
       ],
       traps=[("Bias", "Subtract 127 (single) or 1023 (double) from the exponent field; denormals use 1 − bias."),
              ("Hidden bit", "Normal numbers have an implicit leading 1; denormals have an implicit 0."),
              ("Associativity", "Floating-point addition is not associative."),
              ("Exponent all 1s", "Infinity or NaN — not a huge ordinary number.")],
       quick=[("Single-precision bias is", ["63", "127", "255", "1023"], 1, "8-bit exponent."),
              ("Exponent field 0 and nonzero fraction means", ["NaN", "denormal", "infinity", "normal"], 1, "Denormal."),
              ("Number of precision bits in single precision (with hidden bit)", ["23", "24", "32", "8"], 1, "23 + 1."),
              ("NaN compared with itself using == is", ["true", "false", "undefined", "zero"], 1, "NaN ≠ NaN.")],
       summary=["Single 1/8/23 bias 127; double 1/11/52 bias 1023.", "Normal: (−1)ˢ 1.F 2^(E−bias); denormal: 0.F 2^(1−bias).", "E = 0: zero/denormal; E = all ones: infinity/NaN.",
                "Encode: normalise, bias the exponent, store the fraction bits.", "Max single ≈ 3.4e38, epsilon 2⁻²³.", "Floating-point addition is not associative."])


# ======================================================================================================
lesson(subject=S, chapter="Sequential Logic", ch_no=3, no=1, slug="dl-sequential-circuits", title="Flip-Flops, Counters & State Machines",
       topic="Sequential Circuits", minutes=24, weight=6, widget="none",
       key="Sequential circuits have memory: outputs depend on inputs and the stored state. Latches and flip-flops (SR, D, JK, T) store bits; registers and counters are built from them; finite-state machines (Moore and Mealy) are designed from state tables and excitation equations.",
       analogy=("💡", "A light switch versus a push button", "A combinational circuit is a push button: the light is on only while you press. A sequential circuit is a toggle switch: it remembers its last state, and what happens next depends on both the press and what it was before."),
       sections=[
           dict(h="Latches and flip-flops", md="""| Device | Next state Q⁺ | Notes |
|---|---|---|
| **SR** | S + R′Q (S = R = 1 forbidden) | set / reset / hold |
| **D** | D | follows D at the clock edge |
| **JK** | JQ′ + K′Q | J=K=0 hold, 01 reset, 10 set, 11 **toggle** |
| **T** | T ⊕ Q | toggles when T = 1 |

A **latch** is level-sensitive (transparent while enabled); a **flip-flop** is edge-triggered (master–slave). **Race-around** in a JK latch with J = K = 1 is cured by edge triggering. Conversions: JK→T tie J = K = T; JK→D set J = D, K = D′; D→T use D = T ⊕ Q. **Setup time** t_su before the edge and **hold time** t_h after must be respected; the **maximum clock frequency** is 1 / (t_clk→Q + t_logic + t_su)."""),
           dict(h="Registers and counters", md="""- **Shift register** (n flip-flops): serial-in serial-out, serial-in parallel-out, etc.
- **Ring counter:** a one-hot bit circulating; n flip-flops ⇒ **n** states.
- **Johnson (twisted-ring) counter:** inverted last output fed back; n flip-flops ⇒ **2n** states.
- **Asynchronous (ripple) counter:** each flip-flop clocks the next; simple, but delay accumulates: a mod-2ⁿ ripple counter needs the clock period ≥ n·t_pd; the count can show glitches.
- **Synchronous counter:** all flip-flops share the clock; for a binary counter with T flip-flops Tᵢ = Q₀Q₁…Qᵢ₋₁.
- A **mod-N counter** needs ⌈log₂ N⌉ flip-flops; a counter with a reset on state N is a **truncated** counter.""",
                formulas=[("flip-flops for N states = ⌈log₂ N⌉", "state encoding")]),
           dict(h="Finite-state machine design", md="""A **Moore** machine's outputs depend on the state only; a **Mealy** machine's outputs depend on the state **and** the inputs (typically needs fewer states and reacts one cycle earlier).

Design steps: (1) state diagram from the spec; (2) state table; (3) state assignment; (4) choose flip-flops and derive **excitation equations** from the excitation table (for JK: Q→Q⁺ = 0→0: J=0 K=X; 0→1: J=1 K=X; 1→0: J=X K=1; 1→1: J=X K=0); (5) output equations; (6) draw the circuit.

A **sequence detector** for pattern 101 (overlapping) needs 3 states (Mealy) — remembering the longest matching prefix: ‘’, ‘1’, ‘10’. Unused states in a state assignment should be treated as don't-cares and made self-correcting."""),
           dict(h="Timing and clocking", md="""Synchronous design requires: t_clk→Q(min) + t_logic(min) ≥ t_hold (no hold violation) and T ≥ t_clk→Q + t_logic(max) + t_setup. Minimum clock period is set by the **critical path** between registers. **Metastability** can occur when an asynchronous input violates setup/hold; synchronisers (two flip-flops in series) reduce its probability."""),
       ],
       examples=[
           Ex("Flip-flops for a counter", "How many flip-flops are needed for a mod-20 counter, and how many unused states remain?",
              ["⌈log₂ 20⌉ = 5 flip-flops give 32 states.", "Unused states = 32 − 20 = **12**."],
              "**5** flip-flops; **12** unused states.", verify=lambda: "%d flip-flops; %d unused states" % (math.ceil(math.log2(20)), 2 ** math.ceil(math.log2(20)) - 20)),
           Ex("Ring versus Johnson counter", "How many distinct states do a 4-bit ring counter and a 4-bit Johnson counter (both started in a valid state) cycle through?",
              ["Ring: the single 1 visits each of the 4 positions ⇒ 4 states.", "Johnson: 2n = 8 states."],
              "Ring **4**, Johnson **8**.", verify=lambda: "Ring %d, Johnson %d" % (period("ring", 4), period("johnson", 4))),
           Ex("Synchronous counter with T flip-flops", "A 3-bit synchronous binary up-counter uses T flip-flops with T₀ = 1, T₁ = Q₀, T₂ = Q₀Q₁. What is the count sequence from 000?",
              ["Each bit toggles when all lower bits are 1.", "Sequence 0,1,2,3,4,5,6,7 and then back to 0 (period 8)."],
              "0, 1, 2, 3, 4, 5, 6, 7, 0", verify=lambda: ", ".join(str(x) for x in t_counter(3, 9))),
           Ex("Ripple-counter frequency", "A 4-bit ripple counter uses flip-flops with propagation delay 10 ns each. What is the maximum clock frequency so the count settles before the next clock edge?",
              ["Worst case the change ripples through all 4 flip-flops: 4 × 10 ns = 40 ns.", "Maximum frequency = 1 / 40 ns = **25 MHz**."],
              "**25 MHz**", verify=lambda: "%d MHz" % round(1 / (4 * 10e-9) / 1e6)),
       ],
       traps=[("JK with J=K=1", "Toggles; SR with S=R=1 is forbidden."),
              ("Ring vs Johnson", "n flip-flops give n states (ring) versus 2n (Johnson)."),
              ("Mealy vs Moore", "Mealy outputs may change asynchronously with inputs; Moore only on clock edges."),
              ("Clock period", "Includes clock-to-Q, worst-case logic delay and setup, not hold.")],
       quick=[("A T flip-flop with T = 1 on every clock", ["holds", "toggles", "resets", "sets"], 1, "Q⁺ = Q′."),
              ("States of an n-bit Johnson counter", ["n", "2n", "2ⁿ", "n²"], 1, "2n."),
              ("Which has outputs depending on input as well as state?", ["Moore", "Mealy", "ring counter", "latch"], 1, "Mealy."),
              ("Flip-flops needed for 9 states", ["3", "4", "5", "9"], 1, "⌈log₂ 9⌉.")],
       summary=["SR, D, JK, T: Q⁺ = S+R′Q, D, JQ′+K′Q, T⊕Q.", "Latch = level-sensitive; flip-flop = edge-triggered.", "Ring n states, Johnson 2n, binary counter 2ⁿ; mod-N needs ⌈log₂ N⌉ flip-flops.",
                "Ripple counters accumulate delay; synchronous counters use Tᵢ = Q₀…Qᵢ₋₁.", "Moore (state-only outputs) vs Mealy (state and inputs).", "Clock period ≥ t_clk→Q + t_logic + t_setup."])
