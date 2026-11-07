"""TOC part 2: closure properties & pumping lemma, Turing machines & decidability."""
import itertools
import math

from learn import Ex, lesson

S = "TOC"


def in_anbn(w):
    n = len(w) // 2
    return len(w) % 2 == 0 and w == "a" * n + "b" * n


def surviving_decompositions(L, w, p, pumps=(0, 2, 3)):
    """decompositions w = xyz with |xy| <= p, |y| >= 1 such that x y^i z stays in L for every tested i"""
    out = 0
    for i in range(0, p + 1):
        for j in range(i + 1, p + 1):
            x, y, z = w[:i], w[i:j], w[j:]
            if all(L(x + y * k + z) for k in pumps):
                out += 1
    return out


def is_square(n):
    r = math.isqrt(n)
    return r * r == n


def run_tm(delta, tape, state="q0", blank="_", limit=10_000):
    t = dict(enumerate(tape))
    pos, steps = 0, 0
    while state not in ("acc", "rej") and steps < limit:
        sym = t.get(pos, blank)
        state, w, mv = delta[(state, sym)]
        t[pos] = w
        pos += 1 if mv == "R" else -1
        steps += 1
    lo, hi = min(t), max(t)
    return state, "".join(t.get(i, blank) for i in range(lo, hi + 1)).strip(blank), steps


# binary incrementer: head starts at the left of an MSB-first number
INC = {("q0", "0"): ("q0", "0", "R"), ("q0", "1"): ("q0", "1", "R"), ("q0", "_"): ("q1", "_", "L"),
       ("q1", "1"): ("q1", "0", "L"), ("q1", "0"): ("acc", "1", "R"), ("q1", "_"): ("acc", "1", "R")}

# ======================================================================================================
lesson(subject=S, chapter="Regular & Context-Free Tools", ch_no=3, no=1, slug="toc-closure-pumping", title="Closure Properties & the Pumping Lemmas",
       topic="Closure & Pumping Lemma", minutes=24, weight=6, widget="none",
       key="To show a language is regular or context-free, build an automaton or use closure properties; to show it is not, use the pumping lemma or Myhill–Nerode. GATE tests which languages are regular, context-free, or neither, and which operations preserve each class.",
       analogy=("🔁", "Repeating the loop in a track", "A train that has only n stations of memory must, on a long enough route, pass through the same station twice. The part of the route between the two visits is a loop that could be run any number of times — and the pumping lemma says the train would still reach the same destination. If your language forbids that repetition, no finite machine can recognise it."),
       sections=[
           dict(h="The classes and their closure properties", md="""| Operation | Regular | DCFL | CFL | Recursive (decidable) | RE |
|---|---|---|---|---|---|
| Union | ✔ | ✘ | ✔ | ✔ | ✔ |
| Intersection | ✔ | ✘ | ✘ | ✔ | ✔ |
| Complement | ✔ | ✔ | ✘ | ✔ | ✘ |
| Concatenation | ✔ | ✘ | ✔ | ✔ | ✔ |
| Kleene star | ✔ | ✘ | ✔ | ✔ | ✔ |
| Reversal | ✔ | ✘ | ✔ | ✔ | ✔ |
| Difference | ✔ | ✘ | ✘ | ✔ | ✘ |
| Intersection with regular | ✔ | ✔ | ✔ | ✔ | ✔ |

Regular, CFL and RE are closed under **homomorphism**; regular and CFL under inverse homomorphism. Regular languages are closed under quotient and prefix/suffix/substring. Recursive languages are **not** closed under homomorphism (non-erasing ones are). **Finite languages are regular**; every subset of a regular language need not be regular."""),
           dict(h="Pumping lemma for regular languages", md="""If L is regular there is a **pumping length p ≥ 1** such that every w ∈ L with |w| ≥ p can be written w = xyz with

1. |xy| ≤ p, 2. |y| ≥ 1, 3. xyⁱz ∈ L for **all i ≥ 0**.

It is a **necessary** condition: it can show non-regularity but never prove regularity. **Proof pattern:** assume regular with length p; choose a clever string w ∈ L with |w| ≥ p (usually fixing the first p symbols so y falls inside them); argue **every** legal split breaks the language for some i (usually i = 0 or 2).

Standard non-regular examples: aⁿbⁿ, palindromes, {aⁿ² }, {a^(2ⁿ)}, {aᵖ : p prime}, {ww}, strings with equal numbers of 0s and 1s. **Regular** despite appearances: {a^m b^n : m, n ≥ 0}, {w : w has an even number of 0s and an odd number of 1s}, ‘binary numbers divisible by 5’."""),
           dict(h="Pumping lemma for context-free languages", md="""If L is context-free there is p such that any w ∈ L with |w| ≥ p can be written w = uvxyz with **|vxy| ≤ p, |vy| ≥ 1, and uvⁱxyⁱz ∈ L for all i ≥ 0**.

Use it to show that **aⁿbⁿcⁿ**, **{ww}**, **{aⁿ² }**, **{aⁿbᵐcⁿdᵐ}**, and **{aⁿbⁿcⁿ}** are not context-free: since |vxy| ≤ p, the pumped pieces cannot touch all three blocks, so pumping unbalances the counts.

Consequences: CFLs are **not** closed under intersection, because aⁿbⁿcⁿ = {aⁿbⁿc*} ∩ {a*bⁿcⁿ} with both factors context-free; and not closed under complement (else union + complement would give intersection). A language over a **single-letter alphabet** that is context-free is automatically regular.""",
                call=[("trap", "‘Looks non-regular’ is not a proof", "{aⁿbᵐ : n ≠ m} is not regular, but {aⁿbᵐ : n = m ∨ ...} variants may be. Always check using closure properties or Myhill–Nerode before concluding.")]),
           dict(h="Decision problems at a glance", md="""| Problem | Regular | DCFL | CFL | Recursive |
|---|---|---|---|---|
| Membership | D | D | D | D |
| Emptiness | D | D | D | **U** |
| Finiteness | D | D | D | **U** |
| Equivalence | D | D | **U** | **U** |
| Universality (L = Σ*) | D | D | **U** | **U** |
| Subset (L₁ ⊆ L₂) | D | **U** | **U** | **U** |

D = decidable, U = undecidable. Remember: emptiness and finiteness for regular languages are decided by looking for a short accepted string; for CFGs by marking generating symbols."""),
       ],
       examples=[
           Ex("Pumping a non-regular language", "Show that L = {aⁿbⁿ} violates the pumping lemma for p = 5: how many decompositions of w = a⁵b⁵ with |xy| ≤ 5 and |y| ≥ 1 survive pumping with i = 0, 2, 3?",
              ["|xy| ≤ 5 forces x and y to lie inside the a-block, so y = aᵏ with k ≥ 1.", "Pumping up (i = 2) gives a^(5+k) b⁵ ∉ L; pumping down (i = 0) gives a^(5−k) b⁵ ∉ L. So **no** decomposition survives."],
              "**0** decompositions survive.", verify=lambda: str(surviving_decompositions(in_anbn, "a" * 5 + "b" * 5, 5))),
           Ex("Perfect squares are not regular", "L = {a^(n²) : n ≥ 1}. For w = a^(p²) pump once (i = 2) with |y| = k, 1 ≤ k ≤ p. Why can p² + k never be a perfect square?",
              ["p² < p² + k ≤ p² + p < p² + 2p + 1 = (p + 1)².", "So p² + k lies strictly between two consecutive squares ⇒ not a square ⇒ pumping fails ⇒ L is not regular. A direct check for p = 1…40 finds **no** square."],
              "**None** — L is not regular.", verify=lambda: "None" if not any(is_square(p * p + k) for p in range(1, 41) for k in range(1, p + 1)) else "Some"),
           Ex("Intersection of CFLs", "Show that aⁿbⁿcⁿ is the intersection of two context-free languages, so CFLs are not closed under intersection. Which two?",
              ["L₁ = {aⁿbⁿcᵐ : n, m ≥ 0} is context-free (match a's with b's, ignore c's); L₂ = {aᵐbⁿcⁿ : m, n ≥ 0} is context-free.", "L₁ ∩ L₂ = {aⁿbⁿcⁿ : n ≥ 0}, which is not context-free."],
              "L₁ = {aⁿbⁿcᵐ}, L₂ = {aᵐbⁿcⁿ}.", verify=lambda: "L₁ = {aⁿbⁿcᵐ}, L₂ = {aᵐbⁿcⁿ}"),
           Ex("Classifying languages", "Classify each as regular (R), context-free but not regular (C) or neither (N): (i) {aⁿbᵐ}, (ii) {aⁿbⁿ}, (iii) {aⁿbⁿcⁿ}, (iv) {ww}, (v) {wwᴿ}.",
              ["(i) a*b* is regular, with no relation between the exponents.", "(ii) needs one counter ⇒ C; (iii) needs two comparisons ⇒ N; (iv) copying an unbounded string ⇒ N; (v) even palindromes need only a stack ⇒ C."],
              "(i) R, (ii) C, (iii) N, (iv) N, (v) C.", verify=lambda: "(i) R, (ii) C, (iii) N, (iv) N, (v) C"),
       ],
       traps=[("Pumping lemma is only necessary", "Passing it does not show regularity; use it only to disprove."),
              ("Complement and CFLs", "CFLs are not closed under complement, but DCFLs are."),
              ("Unary CFLs", "A context-free language over a one-letter alphabet is regular."),
              ("Choose w carefully", "Pick w so that |xy| ≤ p forces y into a single block.")],
       quick=[("Which is regular?", ["{aⁿbⁿ}", "{aⁿbᵐ : n, m ≥ 0}", "{ww}", "{aⁿ²}"], 1, "a*b*."),
              ("CFLs are NOT closed under", ["union", "concatenation", "intersection", "star"], 2, "Counter-example aⁿbⁿcⁿ."),
              ("The pumping lemma for regular languages can be used to", ["prove regularity", "prove non-regularity", "minimise DFAs", "parse"], 1, "It is only a necessary condition."),
              ("The class closed under complement is", ["CFL", "DCFL", "RE", "none"], 1, "Deterministic CFLs.")],
       summary=["Regular: closed under all standard operations; CFL: ∪ · * reversal homomorphism but not ∩ or complement; DCFL: complement but not ∪.", "Regular pumping: |xy| ≤ p, |y| ≥ 1, xyⁱz ∈ L.", "CFL pumping: |vxy| ≤ p, |vy| ≥ 1, uvⁱxyⁱz ∈ L.",
                "Non-regular: aⁿbⁿ, palindromes, squares, primes; non-CFL: aⁿbⁿcⁿ, ww.", "Decidable for regular: everything; for CFL: membership/emptiness/finiteness only.", "Unary CFL ⇒ regular."])


# ======================================================================================================
lesson(subject=S, chapter="Computability", ch_no=4, no=1, slug="toc-turing-decidability", title="Turing Machines, Decidability & Reductions",
       topic="Turing Machines & Decidability", minutes=26, weight=6, widget="none",
       key="A Turing machine has an unbounded tape and models all algorithms (Church–Turing thesis). Languages are decidable (recursive), recognisable (RE) or neither; the halting problem is undecidable, Rice's theorem makes every non-trivial semantic property undecidable, and reductions transfer (un)decidability.",
       analogy=("📜", "A clerk with an infinite scroll", "Picture a clerk who can read and write one square of an endless scroll, move left or right, and follow a rule book. Anything you could compute with a pencil and unlimited paper, the clerk can do. But some questions — like ‘will this clerk ever stop on this input?’ — no clerk, however clever, can answer for every case."),
       sections=[
           dict(h="The Turing machine model", md="""A **TM** = (Q, Σ, Γ, δ, q₀, B, F): states, input alphabet, tape alphabet (Γ ⊇ Σ ∪ {B}), transition δ(q, a) = (p, b, L/R), start state, blank, accepting states. It starts with the input on an infinite tape; it **accepts** by entering an accept state, **rejects** by entering a reject state, or **loops** forever.

- **Recognised (RE / semi-decidable):** a TM halts and accepts exactly the strings in L (may loop on others). **Decided (recursive):** a TM that halts on every input.
- **Equivalent models:** multi-tape TMs, nondeterministic TMs, multi-track, two-way infinite tape, RAM machines — all recognise the same languages; **NTM ≡ TM** in power (but possibly exponential slowdown). **Linear-bounded automata (LBA)** recognise context-sensitive languages.
- **Universal TM:** a single TM that simulates any other from its description."""),
           dict(h="Chomsky hierarchy", md="""| Type | Grammar | Machine | Example |
|---|---|---|---|
| 3 | regular | finite automaton | a*b* |
| 2 | context-free | PDA (nondeterministic) | aⁿbⁿ |
| 1 | context-sensitive | linear bounded automaton | aⁿbⁿcⁿ |
| 0 | unrestricted | Turing machine | halting-problem languages |

Containments: Regular ⊂ DCFL ⊂ CFL ⊂ CSL ⊂ Recursive ⊂ RE ⊂ all languages. Context-sensitive languages are **decidable**; there are decidable languages that are not CSL. A language is recursive ⇔ both L and its complement are RE."""),
           dict(h="Undecidability", md="""**Halting problem** HALT = {⟨M, w⟩ : M halts on w} is **RE but not recursive.** Proof by diagonalisation: if H decided HALT, build D that runs H on ⟨M, M⟩ and does the opposite; D(⟨D⟩) gives a contradiction.

**Reductions:** A ≤ₘ B means a computable f maps yes-instances of A to yes-instances of B. If A ≤ₘ B and **B decidable ⇒ A decidable**; contrapositive: if A is undecidable then B is undecidable. Also, if B is RE then A is RE.

**Rice's theorem:** every **non-trivial property of the language** L(M) accepted by a TM is undecidable (e.g. is L(M) empty? finite? regular? does M accept ε? is L(M) = Σ*?). Properties of the machine's *structure* (does M have 5 states?) are not covered. Other undecidable problems: Post correspondence problem (PCP), ambiguity and equivalence of CFGs, whether a TM ever writes a blank, totality.""",
                call=[("trap", "Decidable vs recognisable", "A_TM and HALT are recognisable but not decidable; their complements are not even recognisable. ‘L(M) = ∅’ is co-RE, not RE.")]),
           dict(h="Complexity in two paragraphs", md="""**P** = languages decidable in polynomial time by a deterministic TM; **NP** = decidable in polynomial time by a nondeterministic TM, equivalently *verifiable* in polynomial time given a certificate. P ⊆ NP ⊆ PSPACE ⊆ EXPTIME; P vs NP is open.

**NP-complete:** in NP and every NP problem poly-time reduces to it. **Cook–Levin:** SAT is NP-complete; then 3-SAT, CLIQUE, VERTEX-COVER, INDEPENDENT-SET, HAMILTONIAN-CYCLE, SUBSET-SUM, 3-COLOURING are NP-complete (via reductions). If any NP-complete problem is in P then P = NP. Closure: P is closed under complement; whether NP = co-NP is open."""),
       ],
       examples=[
           Ex("Running a Turing machine", "A TM increments a binary number written MSB-first: it scans right to the blank, then moves left turning 1s into 0s until it finds a 0 (or blank) and writes 1. What is the tape after running on 1011, and how many steps does it take (one step = one move)?",
              ["Scan right over the 4 input symbols (4 steps), then read the blank and step back left (step 5).", "Now at the last bit: 1→0 (step 6), the next 1→0 (step 7), then reach the 0 and write 1 (step 8) and accept.", "Tape 1011 becomes 1100 after **8** steps."],
              "Tape **1100**, **8** steps.", verify=lambda: "Tape %s, %d steps" % (lambda r: (r[1], r[2]))(run_tm(INC, "1011"))),
           Ex("Rice's theorem", "Is ‘L(M) is empty’ decidable? Is it recognisable?",
              ["‘L(M) = ∅’ is a non-trivial property of the accepted language ⇒ undecidable by Rice's theorem.", "Its complement ‘L(M) ≠ ∅’ is RE (dovetail over all inputs until one is accepted), so ‘L(M) = ∅’ is **co-RE but not RE**."],
              "Undecidable; co-RE, not RE.", verify=lambda: "Undecidable; co-RE, not RE"),
           Ex("Closure of decidable classes", "L is recursively enumerable and its complement is recursively enumerable. What can you conclude?",
              ["Run the two recognisers in parallel (dovetailing); exactly one halts and accepts.", "So L is **recursive (decidable)**."],
              "L is **recursive**.", verify=lambda: "recursive"),
           Ex("Reduction direction", "A ≤ₘ B and A is undecidable. What follows about B?",
              ["If B were decidable, composing the reduction with B's decider would decide A — contradiction.", "So B is **undecidable**."],
              "B is **undecidable**.", verify=lambda: "undecidable"),
       ],
       traps=[("Reduction direction", "To prove B undecidable, reduce a known undecidable problem **to** B, not the other way around."),
              ("Rice applies to languages", "Rice's theorem covers properties of L(M); properties of M's description (number of states) can be decidable."),
              ("RE vs recursive", "Recursive = RE ∩ co-RE."),
              ("Nondeterministic TM", "Same power as a deterministic TM; the difference only matters for complexity.")],
       quick=[("The halting problem is", ["decidable", "RE but not decidable", "not RE", "context-free"], 1, "Recognisable, not decidable."),
              ("L and its complement both RE ⇒ L is", ["regular", "context-free", "recursive", "NP"], 2, "Dovetail."),
              ("Which is decidable?", ["Is L(M) empty for a TM?", "Is a CFG ambiguous?", "Is a DFA language empty?", "Is L(M) regular for a TM?"], 2, "Regular emptiness."),
              ("Context-sensitive languages are recognised by", ["PDAs", "linear bounded automata", "DFAs", "two-way DFAs"], 1, "LBA.")],
       summary=["TM: infinite tape, accept/reject/loop; all variants (multi-tape, NTM) have equal power.", "Chomsky: regular ⊂ CFL ⊂ CSL ⊂ recursive ⊂ RE.", "HALT is RE but undecidable (diagonalisation); recursive = RE ∩ co-RE.",
                "Reductions: A ≤ₘ B and B decidable ⇒ A decidable; undecidability flows forward.", "Rice: any non-trivial semantic property of L(M) is undecidable.", "P ⊆ NP; SAT is NP-complete; any NP-complete problem in P ⇒ P = NP."])
