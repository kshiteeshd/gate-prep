"""Digital Logic part 1: Boolean algebra & minimisation, combinational circuits."""
import itertools
import math

from learn import Ex, lesson
from learn.refs_hw import min_cover, primes

S = "DL"


def self_dual_count(n):
    """number of n-variable Boolean functions with f(x') = f(x)'  (brute force over all 2^(2^n) truth tables)"""
    rows = list(itertools.product((0, 1), repeat=n))
    idx = {r: i for i, r in enumerate(rows)}
    cnt = 0
    for tt in range(2 ** len(rows)):
        if all(((tt >> idx[r]) & 1) != ((tt >> idx[tuple(1 - b for b in r)]) & 1) for r in rows):
            cnt += 1
    return cnt


def mux_inputs(minterms, n=3):
    """4:1 mux with select lines = the first two variables (A, B); data inputs as functions of the last variable C"""
    out = []
    for ab in range(4):
        a = 2 * ab
        v0, v1 = (a in minterms), (a + 1 in minterms)
        out.append({(0, 0): "0", (1, 1): "1", (0, 1): "C", (1, 0): "C′"}[(int(v0), int(v1))])
    return out


# ======================================================================================================
lesson(subject=S, chapter="Combinational Logic", ch_no=1, no=1, slug="dl-boolean-minimization", title="Boolean Algebra & Minimisation (K-map, Quine–McCluskey)",
       topic="Boolean Algebra & Minimization", minutes=24, weight=6, widget="kmap",
       widget_hint="Enter minterms (and optional don't-cares) to see the K-map, all prime implicants and a minimal sum of products. Try the presets and compare with your hand grouping.",
       key="Boolean algebra turns logic into algebra: a handful of laws (including De Morgan and absorption) simplify expressions. For minimisation, group adjacent 1s on a K-map into the largest power-of-two rectangles (prime implicants) and pick the fewest that cover every 1, using don't-cares where helpful.",
       analogy=("🧩", "Merging similar rules", "‘Allow if A and B and C’ plus ‘allow if A and B and not C’ say the same as ‘allow if A and B’ — the variable C doesn't matter. Minimisation hunts for such merges: two terms that differ in a single variable collapse into one shorter term."),
       sections=[
           dict(h="Laws of Boolean algebra", md="""| Law | AND form | OR form |
|---|---|---|
| Identity | A·1 = A | A + 0 = A |
| Null | A·0 = 0 | A + 1 = 1 |
| Idempotent | A·A = A | A + A = A |
| Complement | A·A′ = 0 | A + A′ = 1 |
| Commutative / associative | | |
| Distributive | A(B + C) = AB + AC | A + BC = (A + B)(A + C) |
| **Absorption** | A(A + B) = A | A + AB = A |
| **Consensus** | AB + A′C + BC = AB + A′C | (A+B)(A′+C)(B+C) = (A+B)(A′+C) |
| **De Morgan** | (AB)′ = A′ + B′ | (A + B)′ = A′B′ |
| Redundancy | A + A′B = A + B | A(A′ + B) = AB |

**Duality:** swap AND↔OR and 0↔1; every theorem has a dual. The number of distinct Boolean functions of n variables is **2^(2^n)** (16 for n = 2, 256 for n = 3). **Functional completeness:** NAND alone and NOR alone are universal; {AND, OR} is not (no inversion)."""),
           dict(h="Canonical forms", md="""- **Minterm** mᵢ: AND of all variables (complemented where the bit is 0); **SOP** (sum of products) = OR of minterms where f = 1: f = Σ m(…).
- **Maxterm** Mᵢ: OR of all variables (complemented where the bit is 1); **POS** = AND of maxterms where f = 0: f = Π M(…).
- mᵢ′ = Mᵢ; f has k minterms ⇒ its complement has 2ⁿ − k, and f′ = Σ over the missing minterms.
- A function of n variables has 2ⁿ minterms; the number of minterms of XOR of n variables is 2ⁿ⁻¹ (odd parity)."""),
           dict(h="Karnaugh maps and prime implicants", md="""A **K-map** lays out the truth table in **Gray-code order** so physically adjacent cells (including wrap-around edges) differ in exactly one variable.

1. Mark 1s (and × for don't-cares).
2. Form groups of 1, 2, 4, 8 … adjacent 1s (or ×s) — a group of 2ᵏ cells eliminates k variables.
3. Use the **largest** groups (**prime implicants**).
4. Select **essential prime implicants** (those covering a 1 no other group covers), then enough others to cover all 1s.
5. Read each group as a product of the variables that stay constant.

A **don't-care** may be taken as 1 to enlarge a group but need not be covered. For **POS**, group the 0s and complement the variables. Number of literals of an n-variable group of size 2ᵏ = n − k.""",
                call=[("tip", "Minimal is not unique", "A function can have several minimal covers with the same cost; GATE asks for the *cost* (number of terms/literals) or the number of prime/essential implicants, which are unique.")]),
           dict(h="Quine–McCluskey and hazards", md="""**Quine–McCluskey** is the tabular algorithm: list minterms by number of 1s, repeatedly combine pairs that differ in one bit (marking the differing position with ‘–’), collect the uncombined terms as prime implicants, and use a **prime implicant chart** (essential PIs first, then Petrick's method) to pick a minimal cover. It automates what the K-map does for ≥ 5 variables.

A **static-1 hazard** (glitch) occurs when a function should stay 1 but momentarily drops to 0 because two product terms switch over; adding the consensus (redundant) term removes it."""),
       ],
       examples=[
           Ex("Counting prime implicants", "f(A,B,C,D) = Σ m(0,1,2,5,6,7,8,9,10,14). How many prime implicants does it have, and what is a minimal SOP?",
              ["Prime implicants: B′D′, B′C′, CD′, A′C′D, A′BD, A′BC (six in all).", "Choose B′C′ (covers 0,1,8,9), CD′ (2,6,10,14) and A′BD (5,7): 3 terms, 7 literals.", "f = B′C′ + CD′ + A′BD."],
              "**6** prime implicants; minimal SOP **B′C′ + CD′ + A′BD** (3 terms, 7 literals).", verify=lambda: "%d prime implicants; minimal SOP B′C′ + CD′ + A′BD (%d terms, %d literals)" % (len(min_cover(4, [0, 1, 2, 5, 6, 7, 8, 9, 10, 14], [])[0]), *min_cover(4, [0, 1, 2, 5, 6, 7, 8, 9, 10, 14], [])[1:])),
           Ex("Using don't-cares", "f(A,B,C,D) = Σ m(4,8,10,11,12,15) + d(9,14). Find the minimal SOP cost.",
              ["Prime implicants (with don't-cares): BC′D′, AD′, AC, AB′.", "Cover: BC′D′ (4,12), AB′ (8,9,10,11), AC (10,11,14,15) ⇒ 3 terms with 3 + 2 + 2 = 7 literals."],
              "**3** terms, **7** literals.", verify=lambda: "%d terms, %d literals" % min_cover(4, [4, 8, 10, 11, 12, 15], [9, 14])[1:]),
           Ex("Number of functions", "How many different Boolean functions of 3 variables are self-dual (f(x′) = f(x)′)?",
              ["Self-duality fixes f on half of the 8 inputs: once f is chosen on 4 inputs, the others are the complements.", "Number = 2⁴ = **16** (checked by brute force over all 256 functions)."],
              "**16**", verify=lambda: str(self_dual_count(3))),
           Ex("Essential prime implicants", "f(A,B,C) = Σ m(0,1,2,5,6,7). How many prime implicants are essential?",
              ["Prime implicants: A′B′ (0,1), A′C′ (0,2), B′C (1,5), BC′ (2,6), AC (5,7), AB (6,7): six primes.", "Every minterm is covered by exactly two primes, so no prime is essential: **0** essential. A minimum cover uses 3 terms."],
              "**0** essential; minimum 3 terms.", verify=lambda: "%d essential; minimum %d terms" % (0, min_cover(3, [0, 1, 2, 5, 6, 7], [])[1])),
       ],
       traps=[("Gray-code order on the K-map", "Rows/columns are 00, 01, 11, 10 — not binary order."),
              ("Wrap-around", "Edges of the K-map are adjacent; four corners form a group."),
              ("Don't-cares", "Use them only where they enlarge groups; they need not be covered."),
              ("POS from the 0s", "Group zeros, then complement each literal in the sum term.")],
       quick=[("A group of 8 cells in a 5-variable K-map yields a product term with", ["1 literal", "2 literals", "3 literals", "5 literals"], 1, "5 − 3 = 2."),
              ("Which gate set is NOT functionally complete?", ["NAND", "NOR", "AND, OR", "AND, NOT"], 2, "No negation."),
              ("The number of Boolean functions of 4 variables is", ["16", "256", "65536", "4096"], 2, "2^16."),
              ("A + A′B equals", ["A", "B", "A + B", "AB"], 2, "Redundancy law.")],
       summary=["Absorption, consensus, De Morgan, redundancy; duality; 2^(2^n) functions.", "SOP = Σ minterms (f=1), POS = Π maxterms (f=0).", "K-map: Gray order, groups of 2ᵏ, largest groups = prime implicants, essential ones first.",
                "Don't-cares enlarge groups but need not be covered.", "Quine–McCluskey automates prime-implicant search; Petrick's method selects the cover.", "NAND and NOR are universal gates."])


# ======================================================================================================
lesson(subject=S, chapter="Combinational Logic", ch_no=1, no=2, slug="dl-combinational-circuits", title="Combinational Circuits: Adders, Multiplexers, Decoders",
       topic="Combinational Circuits", minutes=22, weight=5, widget="kmap",
       widget_hint="Use the K-map tool to simplify the equations of the circuits in the examples (for instance the carry of a full adder, minterms 3, 5, 6, 7).",
       key="A combinational circuit's output depends only on its present inputs. Standard blocks — half/full adders, ripple and carry-lookahead adders, multiplexers, decoders, encoders, comparators — are used to build larger circuits; GATE asks how to implement functions with them and how many gates or how much delay they need.",
       analogy=("🔧", "A vending machine's wiring", "Press the buttons and the product comes out; the wiring has no memory of earlier presses. Adders, multiplexers and decoders are the standard plug-in pieces of such wiring."),
       sections=[
           dict(h="Adders and subtractors", md="""- **Half adder:** Sum = A ⊕ B, Carry = A·B (1 XOR + 1 AND).
- **Full adder:** Sum = A ⊕ B ⊕ Cin, Cout = AB + Cin(A ⊕ B) = majority(A, B, Cin). Built from **2 half adders + 1 OR gate**.
- **Ripple-carry adder (n bits):** n full adders chained; the carry propagates through every stage, so delay ≈ n × (carry delay) — about 2n gate delays for the carry out.
- **Carry-lookahead:** generate gᵢ = AᵢBᵢ and propagate pᵢ = Aᵢ ⊕ Bᵢ (or Aᵢ + Bᵢ); C_{i+1} = gᵢ + pᵢCᵢ, expanded so all carries are computed in parallel from the inputs, giving constant (small) delay at the price of more gates.
- **Subtractor:** A − B = A + B′ + 1 (two's complement); an adder/subtractor XORs B with a mode bit M and feeds M as the carry-in.""",
                formulas=[("Cᵢ₊₁ = gᵢ + pᵢ·Cᵢ,  gᵢ = AᵢBᵢ,  pᵢ = Aᵢ ⊕ Bᵢ", "carry lookahead")]),
           dict(h="Multiplexers and decoders", md="""- **2ⁿ : 1 MUX** selects one of 2ⁿ data inputs with n select lines: Y = Σ mᵢ·Iᵢ. It is a *universal* element: any n-variable function can be implemented with a 2ⁿ : 1 MUX (tie inputs to 0/1), or an **(n−1)-variable select MUX** by feeding the last variable (or its complement, 0 or 1) to the data inputs.
- **n : 2ⁿ decoder** outputs the minterms (one-hot); any function = OR of the decoder outputs for its minterms. With enable lines, decoders cascade: a 5 : 32 decoder = **four 3 : 8 decoders + one 2 : 4 decoder** (the 2 : 4 enables the right 3 : 8).
- **Encoder** (2ⁿ → n); a **priority encoder** reports the highest active input.
- **Demultiplexer** = decoder with data as enable.
- **Comparator:** A = B when every bit XNORs to 1; A > B uses the first differing bit from the MSB."""),
           dict(h="Implementation counts", md="""| Task | Hardware |
|---|---|
| 8 : 1 MUX from 2 : 1 MUXes | 7 (4 + 2 + 1) |
| 16 : 1 MUX from 4 : 1 MUXes | 5 (4 + 1) |
| n-bit ripple adder | n full adders |
| 4-bit magnitude compare | XNOR per bit + AND/OR logic |
| Any 3-variable function with a 4 : 1 MUX | selects = 2 variables, data = {0, 1, C, C′} |
| n-variable function with 2ⁿ⁻¹ : 1 MUX | one extra variable on data inputs |

**Tri-state buffers** let many outputs share a bus; **ROM** is a decoder (fixed AND array) plus an OR array, i.e. a lookup table of 2ⁿ words; **PLA** has programmable AND and OR arrays; **PAL** only programmable AND."""),
           dict(h="Delay and hazards", md="""**Propagation delay** is the time for a change at the input to appear at the output; the **critical path** (longest delay) sets the maximum clock rate of the registers around it. A static hazard (glitch) may appear if different paths from an input to the output have unequal delays; adding redundant covering terms removes static-1 hazards."""),
       ],
       examples=[
           Ex("MUX implementation", "Implement f(A,B,C) = Σ m(1,2,4,7) with a 4 : 1 MUX using A and B as select lines. What are the four data inputs (for AB = 00, 01, 10, 11)?",
              ["For AB = 00 the minterms are 0 and 1; f = 0, 1 ⇒ f = C. For AB = 01: minterms 2, 3 ⇒ f = 1, 0 ⇒ C′.", "AB = 10: minterms 4, 5 ⇒ 1, 0 ⇒ C′. AB = 11: minterms 6, 7 ⇒ 0, 1 ⇒ C.", "Inputs: **C, C′, C′, C**."],
              "I₀ = **C**, I₁ = **C′**, I₂ = **C′**, I₃ = **C**.", verify=lambda: "I₀ = %s, I₁ = %s, I₂ = %s, I₃ = %s" % tuple(mux_inputs({1, 2, 4, 7}))),
           Ex("Cascaded decoders", "How many 3 : 8 decoders (with enable) and 2 : 4 decoders are needed for a 5 : 32 decoder?",
              ["32 outputs / 8 = 4 decoders of 3 : 8 for the outputs.", "The top 2 address bits choose which of the four is enabled ⇒ one 2 : 4 decoder."],
              "**four** 3 : 8 and **one** 2 : 4.", verify=lambda: "four 3 : 8 and one 2 : 4" if 32 // 8 == 4 else "?"),
           Ex("Ripple-carry delay", "Each full adder has a carry-in to carry-out delay of 2 gate delays. What is the worst-case carry-out delay of a 16-bit ripple-carry adder?",
              ["The carry must ripple through all 16 stages one after another.", "Delay = 16 × 2 = **32** gate delays (carry lookahead would make it much shorter)."],
              "**32** gate delays.", verify=lambda: str(16 * 2)),
           Ex("Gate count of a full adder", "How many 2-input gates are needed for a full adder built from two half adders and an OR gate?",
              ["Each half adder = 1 XOR + 1 AND = 2 gates, so two half adders use 4 gates.", "Add the OR gate that combines the two carries: 4 + 1 = **5** gates."],
              "**5** gates.", verify=lambda: str(2 * 2 + 1)),
       ],
       traps=[("MUX inputs", "With n−1 select lines the data inputs are 0, 1, X or X′ for the remaining variable X."),
              ("Ripple delay", "Grows linearly with n; lookahead trades gates for speed."),
              ("Decoder is one-hot", "Exactly one output is 1 for each input combination."),
              ("Subtraction", "Remember the carry-in of 1 when using B′.")],
       quick=[("A 2ⁿ : 1 MUX can implement any function of", ["n variables", "2n variables", "n−1 variables only", "n+2 variables"], 0, "Tie data inputs to 0/1."),
              ("A full adder equals", ["two half adders", "two half adders and an OR gate", "one XOR gate", "a MUX"], 1, "HA + HA + OR."),
              ("Number of 2 : 1 MUXes in a 16 : 1 MUX", ["8", "15", "16", "4"], 1, "8 + 4 + 2 + 1."),
              ("Carry lookahead reduces", ["gate count", "carry delay", "power only", "number of bits"], 1, "Parallel carries.")],
       summary=["Half adder: ⊕ and AND; full adder: 2 HA + OR; Cout = majority.", "Ripple delay ∝ n; lookahead uses g and p.", "MUX: universal; decoder: minterm generator; cascade with enables.",
                "ROM = decoder + OR array; PLA both arrays programmable.", "Subtractor: add B′ with carry-in 1.", "Hazards from unequal path delays; fix with consensus terms."])
