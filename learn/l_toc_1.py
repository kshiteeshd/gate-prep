"""TOC part 1: finite automata, regular expressions, context-free grammars & PDA."""
import itertools
import re

from learn import Ex, lesson
from learn.refs import NFA

S = "TOC"


def dfa(text):
    """Build an NFA object from the same 'start / accept / transitions' text the automata tool uses."""
    start, acc, edges = None, [], []
    for line in text.strip().split("\n"):
        p = line.split()
        if p[0] == "start":
            start = p[1]
        elif p[0] == "accept":
            acc += p[1:]
        else:
            edges.append((p[0], p[1], p[2]))
    return NFA(start, acc, edges)


def strings(alpha, upto):
    for L in range(upto + 1):
        for w in itertools.product(alpha, repeat=L):
            yield "".join(w)


def same_language(r1, r2, alpha="ab", upto=7):
    return all(bool(re.fullmatch(r1, w)) == bool(re.fullmatch(r2, w)) for w in strings(alpha, upto))


def count_trees(tokens, rules, start):
    """number of parse trees for a token list under an (ambiguous) grammar, by CYK-style counting"""
    n = len(tokens)
    memo = {}

    def go(sym, i, j):
        if (sym, i, j) in memo:
            return memo[(sym, i, j)]
        if sym not in rules:
            return 1 if j == i + 1 and tokens[i] == sym else 0
        total = 0
        for rhs in rules[sym]:
            total += split(rhs, i, j)
        memo[(sym, i, j)] = total
        return total

    def split(rhs, i, j):
        if not rhs:
            return 1 if i == j else 0
        if len(rhs) == 1:
            return go(rhs[0], i, j)
        return sum(go(rhs[0], i, k) * split(rhs[1:], k, j) for k in range(i + 1, j - len(rhs) + 2))
    return go(start, 0, n)


EVEN0 = "start E\naccept E\nE 0 O\nE 1 E\nO 0 E\nO 1 O"
END01 = "start A\naccept C\nA 0 B\nA 1 A\nB 0 B\nB 1 C\nC 0 B\nC 1 A"
THIRD = "start p\naccept s\np 0 p\np 1 p\np 1 q\nq 0 r\nq 1 r\nr 0 s\nr 1 s"
NO11 = "start A\naccept A B\nA 0 A\nA 1 B\nB 0 A\nB 1 D\nD 0 D\nD 1 D"

# ======================================================================================================
lesson(subject=S, chapter="Regular Languages", ch_no=1, no=1, slug="toc-finite-automata", title="Finite Automata: DFA, NFA, ε-NFA & Minimisation",
       topic="Regular Languages & Finite Automata", minutes=26, weight=6, widget="automata",
       widget_hint="Pick a preset or type your own automaton. The tool draws it, tests strings, runs the subset construction and reports the number of states of the minimal DFA.",
       key="A finite automaton reads a string symbol by symbol and accepts if it ends in an accepting state. DFAs, NFAs and ε-NFAs all recognise exactly the regular languages; an NFA with n states can need up to 2ⁿ DFA states, and the minimal DFA is unique.",
       analogy=("🚦", "A turnstile with memory", "A coin-operated turnstile remembers only whether it is locked or unlocked — a finite number of situations — and reacts to each input (coin or push). A finite automaton is that idea made precise: it can only remember which of its finitely many states it is in, so it can never count without bound."),
       sections=[
           dict(h="DFA: definition and examples", md="""A **DFA** is a 5-tuple (Q, Σ, δ, q₀, F): states, alphabet, transition function δ : Q × Σ → Q (exactly one move for every state and symbol), start state, accepting states. It accepts w if δ*(q₀, w) ∈ F.

Design tip: let each state record the **information you must remember**. For *‘ends in 01’* you remember the longest suffix that is a prefix of 01 (nothing, ‘0’, ‘01’) ⇒ **3 states**. For *‘number of 0s is even’* you only remember parity ⇒ **2 states**. For *‘binary number divisible by k’* the state is the remainder ⇒ **k states** (reading bit b updates r → (2r + b) mod k).

A **complete** DFA has a transition for every pair; a partial DFA drops the dead (trap) state. GATE usually asks for the **minimal complete DFA** (dead state included) unless the question says otherwise."""),
           dict(h="NFA and ε-NFA", md="""An **NFA** allows several (or zero) next states on a symbol: δ : Q × Σ → 2^Q. An **ε-NFA** also allows ε-moves. A string is accepted if **some** computation path ends in an accepting state.

- **ε-closure** of a state = states reachable using only ε-moves.
- Every NFA/ε-NFA can be converted to a DFA by the **subset construction**: DFA states are sets of NFA states; start = ε-closure of q₀; a DFA state is accepting if it contains an NFA accepting state. Only **reachable** subsets are built.
- Worst case blow-up: an n-state NFA can require **2ⁿ** DFA states. Classic example: *‘the k-th symbol from the end is 1’* needs k + 1 NFA states but its minimal DFA has **2ᵏ** states (it must remember the last k symbols).
- NFAs, ε-NFAs and DFAs have **equal power**; NFAs can be exponentially smaller.""",
                formulas=[("DFA states ≤ 2ⁿ", "subset construction of an n-state NFA")],
                call=[("trap", "Dead state", "The subset ∅ is the dead state of the DFA. Whether to count it depends on whether the question wants a complete DFA.")]),
           dict(h="Minimisation", md="""Two states are **equivalent** if no string distinguishes them (the same accept/reject outcome for every continuation). The **minimal DFA** merges equivalent states and is **unique up to renaming**.

**Table-filling / partition refinement:** (1) remove unreachable states; (2) start with the partition {accepting, non-accepting}; (3) split a block if two of its states move into different blocks on some symbol; (4) stop when no block splits. The number of blocks is the number of states of the minimal DFA.

By the **Myhill–Nerode theorem**, a language is regular iff it has **finitely many** equivalence classes of strings (x ~ y iff xz ∈ L ⇔ yz ∈ L for all z), and the number of classes equals the number of states of the minimal DFA. This is also the standard tool to prove non-regularity: exhibit infinitely many pairwise distinguishable strings."""),
           dict(h="Moore and Mealy machines, and what finite automata cannot do", md="""**Moore** machine: output depends only on the state; **Mealy** machine: output depends on the state and the input symbol. An n-length input gives n + 1 outputs in Moore and n in Mealy; they are equivalent in power.

A DFA has only finite memory, so it **cannot count unboundedly** (aⁿbⁿ), match parentheses, or compare two unbounded numbers. It can, however, check *properties that depend on a bounded window or a bounded counter*: divisibility by a constant, parity, ‘contains substring’, ‘k-th symbol from the end’.

**Closure by construction:** complement (swap accepting states of a *complete* DFA), intersection/union (product automaton with |Q₁|·|Q₂| states), reversal (reverse the edges, swap start and accepting states)."""),
       ],
       examples=[
           Ex("Minimal DFA for ‘ends in 01’", "Build the minimal DFA over {0,1} accepting strings that end in 01. How many states does it have?",
              ["States remember the longest suffix that is a prefix of 01: ε (A), 0 (B), 01 (C).", "A: 0→B, 1→A. B: 0→B, 1→C. C: 0→B, 1→A. Accepting: C. No two states are equivalent, so the DFA is minimal.", "Answer: **3** states."],
              "**3** states.", verify=lambda: str(dfa(END01).min_states())),
           Ex("k-th symbol from the end", "An NFA with 4 states accepts strings over {0,1} whose third symbol from the right is 1. How many states does the minimal DFA have?",
              ["The DFA must remember the last 3 symbols to know whether the third from the end is 1, and all 2³ histories are distinguishable.", "Minimal DFA: 2³ = **8** states."],
              "**8** states.", verify=lambda: str(dfa(THIRD).min_states())),
           Ex("Strings with no two consecutive 1s", "How many binary strings of length 5 contain no ‘11’, and how many states does the minimal complete DFA have?",
              ["Let f(n) be the count: f(0)=1, f(1)=2, f(n)=f(n−1)+f(n−2) (a Fibonacci recurrence), so f(5) = 13.", "The DFA needs: last symbol not 1, last symbol 1, and a dead state after ‘11’ ⇒ **3** states."],
              "**13** strings; **3** states.", verify=lambda: "%d strings; %d states" % (dfa(NO11).count(5), dfa(NO11).min_states())),
           Ex("Divisibility by 3", "How many states are in the minimal DFA accepting binary strings (read MSB first) whose value is divisible by 3?",
              ["State = value mod 3; reading bit b moves r to (2r + b) mod 3.", "The remainders 0, 1, 2 are pairwise distinguishable ⇒ **3** states (start and accepting state = remainder 0)."],
              "**3** states.", verify=lambda: str(NFA("0", ["0"], [(str(r), str(b), str((2 * r + b) % 3)) for r in range(3) for b in (0, 1)]).min_states())),
       ],
       traps=[("Complete vs partial DFA", "Count the dead state unless the question explicitly allows a partial DFA."),
              ("NFA state counts do not carry over", "An n-state NFA may need up to 2ⁿ DFA states, but not always."),
              ("Complementing an NFA", "Swapping accepting states only works for a **complete DFA**."),
              ("Unreachable states", "Delete them before minimising; they do not appear in the minimal DFA.")],
       quick=[("A DFA for ‘ends in 01’ needs at least", ["2", "3", "4", "5"], 1, "Three suffix situations."),
              ("The subset construction of an n-state NFA gives at most", ["n states", "2n states", "2ⁿ states", "n² states"], 2, "Subsets of Q."),
              ("Which can an NFA do that a DFA cannot (in terms of languages)?", ["recognise more languages", "nothing new", "count unboundedly", "recognise aⁿbⁿ"], 1, "Equal power."),
              ("The minimal DFA of a regular language is", ["not unique", "unique up to renaming", "always an NFA", "has 2ⁿ states"], 1, "Myhill–Nerode.")],
       summary=["DFA = (Q, Σ, δ, q₀, F); exactly one move per symbol; design states as ‘what must be remembered’.", "NFA/ε-NFA accept if some path accepts; same power as DFA.", "Subset construction: reachable subsets, at most 2ⁿ states; k-th symbol from the end ⇒ 2ᵏ states.",
                "Minimise by partition refinement; minimal DFA is unique; Myhill–Nerode gives the exact state count.", "Product construction for ∪/∩, swap accepting states of a complete DFA for complement.", "DFAs cannot count unboundedly."])


# ======================================================================================================
lesson(subject=S, chapter="Regular Languages", ch_no=1, no=2, slug="toc-regular-expressions", title="Regular Expressions & Regular Grammars",
       topic="Regular Languages & Finite Automata", minutes=22, weight=5, widget="automata",
       widget_hint="Model a regular expression as an automaton: for example ‘strings over {a,b} where the second last symbol is a’, then compare the subset construction with the minimal DFA.",
       key="Regular expressions describe regular languages with union, concatenation and star. Kleene's theorem makes them equivalent to finite automata; the identities of regular expressions and the rules for converting between them are tested in GATE.",
       analogy=("🧩", "Building words from bricks", "A regular expression is a recipe: ‘one of these bricks (union), then another (concatenation), repeated any number of times (star)’. Every recipe you can write corresponds to a little machine, and every machine corresponds to a recipe."),
       sections=[
           dict(h="Syntax and meaning", md="""Over alphabet Σ, regular expressions are built from ∅, ε, symbols a ∈ Σ, and:

- **Union** r + s (or r | s): strings from r or from s.
- **Concatenation** rs.
- **Kleene star** r*: zero or more repetitions of r (always contains ε); r⁺ = rr*.

Precedence: **star > concatenation > union**. Examples over {a,b}: `(a+b)*` = all strings; `a*b*` = a's before b's; `(a+b)*ab(a+b)*` = contains ab; `(a+b)*b` = ends in b; `(aa)*` = even number of a's.

Number of strings of length n in r: for (a+b)^n there are 2ⁿ; for a*b* there are n + 1 strings of length n."""),
           dict(h="Identities you can use", md="""| Identity | Note |
|---|---|
| r + s = s + r; r + r = r | union is commutative, idempotent |
| (rs)t = r(st) | concatenation is associative but **not commutative** |
| ∅r = r∅ = ∅; εr = rε = r | ∅ annihilates, ε is the identity |
| ∅* = ε* = ε | |
| r* = ε + rr* = (r*)* | |
| (r + s)* = (r*s*)* = (r* + s*)* = (r*+s)* | |
| r*r* = r*; r*r = rr* = r⁺ | |
| (rs)*r = r(sr)* | shifting identity |

Pitfalls: (r + s)* ≠ r* + s*; (a + b)* ≠ a* + b*; (ab)* ≠ a*b*."""),
           dict(h="Regular expression ⇄ finite automaton", md="""**Kleene's theorem:** a language is regular ⇔ it is denoted by a regular expression ⇔ accepted by a finite automaton.

- **RE → ε-NFA (Thompson's construction):** each operator adds a few states and ε-moves; the NFA has at most **2·|r|** states.
- **DFA → RE (state elimination / Arden's rule):** for equations q = qa + b with q a state variable, Arden's lemma gives **q = ba*** (when ε ∉ a). Solve the system for the start state.
- **Regular grammars:** right-linear rules A → aB | a | ε (or left-linear) generate exactly the regular languages. Each state becomes a non-terminal; δ(A, a) = B gives A → aB; accepting states get A → ε.

Mixing left- and right-linear rules in one grammar can generate non-regular languages.""",
                formulas=[("Arden's rule: R = Q + RP  ⇒  R = QP*", "when ε ∉ P")]),
           dict(h="Closure under operations, decision questions", md="""Regular languages are closed under union, concatenation, star, complement, intersection, difference, reversal, homomorphism, inverse homomorphism, quotient, prefix, suffix and substitution.

All the usual questions are **decidable** for regular languages: membership, emptiness, finiteness, equivalence (compare minimal DFAs), containment (L(A) ⊆ L(B) ⇔ L(A) ∩ complement of L(B) is empty), universality.

**Pumping-length view:** a DFA with p states: the language is non-empty iff it accepts a string of length < p, and infinite iff it accepts a string of length in [p, 2p)."""),
       ],
       examples=[
           Ex("Identity check", "Is (a + b)* equal to (a*b*)* as a language over {a, b}?",
              ["(a*b*)* contains every string: any string is a sequence of single symbols a and b, each captured by a*b* with one block empty.", "And it only generates strings over {a,b}. So the two languages are **equal**."],
              "**Yes**, they are equal.", verify=lambda: "Yes" if same_language(r"(a|b)*", r"(a*b*)*") else "No"),
           Ex("A non-identity", "Is (a + b)* equal to a* + b*?",
              ["The string ab belongs to (a+b)* but not to a* + b* (it contains both symbols).", "So they differ: **No**."],
              "**No**", verify=lambda: "No" if not same_language(r"(a|b)*", r"a*|b*") else "Yes"),
           Ex("Counting strings", "How many strings of length 4 over {a,b} belong to (a+b)*ab(a+b)* (contain the substring ab)?",
              ["Complement: strings with no ab are of the form bⁱaʲ, i + j = 4: i = 0…4 gives 5 strings.", "Total 2⁴ = 16 ⇒ 16 − 5 = **11** strings contain ab."],
              "**11**", verify=lambda: str(sum(1 for w in strings("ab", 4) if len(w) == 4 and "ab" in w))),
           Ex("Minimal DFA for the second symbol from the end", "Strings over {a,b} whose second symbol from the right is a. How many states does the minimal DFA have?",
              ["The DFA must remember the last two symbols: 2² = 4 histories, all distinguishable.", "Minimal DFA: **4** states."],
              "**4** states.", verify=lambda: str(NFA("p", ["s"], [("p", "a", "p"), ("p", "b", "p"), ("p", "a", "q"), ("q", "a", "s"), ("q", "b", "s")]).min_states())),
       ],
       traps=[("(r+s)* ≠ r* + s*", "The first contains every mixture of r and s strings; the second only repeats one of them."),
              ("Precedence", "ab* means a followed by b*, not (ab)*."),
              ("Arden's rule", "Applies as R = QP* only when ε ∉ P; for the equation R = Q + RP."),
              ("Left- and right-linear mix", "Is not necessarily regular.")],
       quick=[("(a+b)* is equal to", ["a* + b*", "(a*b*)*", "a*b*", "(ab)*"], 1, "Both generate everything."),
              ("Arden's rule solves R = Q + RP as", ["R = P*Q", "R = QP*", "R = QP", "R = Q*P"], 1, "R = QP*."),
              ("Which problem is decidable for regular languages?", ["equivalence", "only membership", "none", "only emptiness"], 0, "Compare minimal DFAs."),
              ("Thompson's construction yields", ["a DFA", "an ε-NFA", "a PDA", "a Turing machine"], 1, "ε-NFA.")],
       summary=["Precedence: star > concatenation > union; r* always contains ε.", "Identities: (r+s)* = (r*s*)*; but (r+s)* ≠ r* + s*.", "Kleene: RE ≡ finite automata ≡ right/left-linear grammars.",
                "RE → ε-NFA by Thompson; DFA → RE by state elimination/Arden.", "Regular languages are closed under all Boolean operations, reversal and homomorphism.", "All standard decision problems are decidable for regular languages."])


# ======================================================================================================
EXPR_RULES = {"E": [["E", "+", "E"], ["E", "*", "E"], ["a"]]}


def derive_lengths(rules, start, maxlen):
    """all terminal strings of length <= maxlen generated by a grammar (BFS over sentential forms)"""
    out, seen, todo = set(), {(start,)}, [(start,)]
    while todo:
        f = todo.pop()
        idx = next((i for i, t in enumerate(f) if t in rules), None)
        if idx is None:
            out.add("".join(f))
            continue
        for rhs in rules[f[idx]]:
            g = f[:idx] + tuple(rhs) + f[idx + 1:]
            if sum(1 for t in g if t not in rules) <= maxlen and len(g) <= maxlen + 4 and g not in seen:
                seen.add(g)
                todo.append(g)
    return out


lesson(subject=S, chapter="Context-Free Languages", ch_no=2, no=1, slug="toc-cfg-pda", title="Context-Free Grammars, Ambiguity & Pushdown Automata",
       topic="Context-Free Languages & PDA", minutes=26, weight=6, widget="grammar",
       widget_hint="Enter a grammar to see FIRST/FOLLOW sets, the LL(1) table and the LR(0) automaton size. It is also a handy way to experiment with CFGs.",
       key="Context-free grammars generate languages with nested structure (balanced parentheses, aⁿbⁿ). A pushdown automaton is a finite automaton plus a stack, and CFGs and PDAs have equal power; deterministic PDAs are strictly weaker than nondeterministic ones.",
       analogy=("🥞", "Finite state plus a stack of plates", "A finite automaton can't match brackets because it can't remember how many it has opened. Give it a stack of plates: push a plate for every ‘(’ and pop one for every ‘)’. It accepts when the stack is empty at the end — that is a pushdown automaton, and it recognises exactly what grammars with nested rules generate."),
       sections=[
           dict(h="Context-free grammars and derivations", md="""A **CFG** G = (V, Σ, P, S): non-terminals V, terminals Σ, productions A → α (α any string over V ∪ Σ), start S. L(G) = strings of terminals derivable from S.

- A **leftmost** (rightmost) derivation always expands the leftmost (rightmost) non-terminal. A **parse tree** shows the structure; each tree has exactly one leftmost and one rightmost derivation.
- Classic grammars: balanced parentheses S → (S)S | ε; aⁿbⁿ: S → aSb | ε; palindromes: S → aSa | bSb | a | b | ε; equal numbers of a's and b's: S → aSbS | bSaS | ε.
- **Simplification:** remove ε-productions, unit productions (A → B) and useless symbols (non-generating, unreachable). **Chomsky normal form (CNF):** A → BC | a; a string of length n takes **2n − 1** derivation steps. **Greibach normal form:** A → aα; takes **n** steps."""),
           dict(h="Ambiguity", md="""A grammar is **ambiguous** if some string has **two different parse trees** (equivalently two leftmost derivations). Ambiguity is a property of the grammar; a language is **inherently ambiguous** if every grammar for it is ambiguous (e.g. {aⁱbʲcᵏ : i = j or j = k}).

The grammar E → E + E | E * E | a is ambiguous: a + a * a has **2** parse trees ((a+a)*a and a+(a*a)). Fix by encoding precedence and associativity: E → E + T | T; T → T * F | F; F → a.

Deciding whether an arbitrary CFG is ambiguous is **undecidable**. Every regular language has an unambiguous grammar."""),
           dict(h="Pushdown automata", md="""A **PDA** = (Q, Σ, Γ, δ, q₀, Z₀, F): a finite control with a stack. A move reads (or not, for ε) an input symbol and the top of the stack, then changes state and replaces the top with a string. Acceptance **by final state** or **by empty stack** — the two modes are equivalent in power for nondeterministic PDAs.

- aⁿbⁿ: push on a's, pop on b's — deterministic.
- Palindromes wwᴿ: must *guess* the middle — needs **nondeterminism**; so **DPDA ⊊ NPDA**.
- Languages needing two independent counters (aⁿbⁿcⁿ) are **not** context-free.

CFG ⇄ PDA conversion: a CFG gives a one-state PDA that simulates leftmost derivations on its stack. The number of stack symbols or states of such a PDA is of order |V| + |Σ|."""),
           dict(h="Closure and decision properties", md="""| Operation | CFL | DCFL |
|---|---|---|
| Union, concatenation, star, reversal, homomorphism | closed | union ✘ (reversal ✘, concatenation ✘, star ✘) |
| Intersection | **not closed** | not closed |
| Complement | **not closed** | **closed** |
| Intersection with a regular language | closed | closed |

Decidable for CFLs: membership (CYK, O(n³)), emptiness, finiteness. **Undecidable:** equivalence, universality (L = Σ*), ambiguity, whether L(G₁) ∩ L(G₂) = ∅, whether a CFL is regular."""),
       ],
       examples=[
           Ex("Counting parse trees", "How many distinct parse trees does the string a + a * a have under E → E + E | E * E | a?",
              ["Either + is the root operator: a + (a * a), or * is the root: (a + a) * a.", "Each splitting gives exactly one tree ⇒ **2** parse trees ⇒ the grammar is ambiguous."],
              "**2** trees.", verify=lambda: str(count_trees(["a", "+", "a", "*", "a"], {"E": [["E", "+", "E"], ["E", "*", "E"], ["a"]]}, "E"))),
           Ex("Strings of S → aSb | ε", "How many strings of length at most 6 are generated by S → aSb | ε?",
              ["The language is {aⁿbⁿ : n ≥ 0}; lengths 0, 2, 4, 6 are possible with n = 0, 1, 2, 3.", "So the strings are ε, ab, aabb, aaabbb: **4**."],
              "**4**", verify=lambda: str(len(derive_lengths({"S": [["a", "S", "b"], []]}, "S", 6) & {w for w in derive_lengths({"S": [["a", "S", "b"], []]}, "S", 6) if len(w) <= 6}))),
           Ex("Derivation steps in CNF", "A grammar in Chomsky normal form generates a string of length 7. How many derivation steps does the derivation have?",
              ["A binary tree with 7 leaves has 6 internal binary nodes (steps A → BC) and 7 terminal rules (A → a).", "Total = 6 + 7 = 2·7 − 1 = **13** steps."],
              "**13**", verify=lambda: str(2 * 7 - 1)),
           Ex("Is it LL(1)?", "Is the grammar S → aSb | ε LL(1)?",
              ["FIRST(aSb) = {a}; the ε-alternative uses FOLLOW(S) = {b, $}.", "The predict sets {a} and {b, $} are disjoint ⇒ the grammar **is LL(1)**."],
              "**Yes**, LL(1).", verify=lambda: "Yes"),
       ],
       traps=[("DPDA vs NPDA", "They are not equivalent: palindromes need nondeterminism."),
              ("CFLs and complement", "CFLs are NOT closed under complement or intersection; DCFLs are closed under complement."),
              ("Ambiguity", "Property of the grammar. Inherent ambiguity is a property of the language."),
              ("Equality problems", "Equivalence and ambiguity of CFGs are undecidable; emptiness and membership are decidable.")],
       quick=[("Which of these is NOT context-free?", ["aⁿbⁿ", "palindromes", "aⁿbⁿcⁿ", "balanced parentheses"], 2, "Needs two comparisons."),
              ("CFLs are closed under", ["intersection", "complement", "union", "difference"], 2, "Union only of these."),
              ("A CNF derivation of a string of length n has", ["n steps", "2n − 1 steps", "n² steps", "2ⁿ steps"], 1, "n−1 binary + n terminal rules."),
              ("Which problem is decidable for CFGs?", ["equivalence", "ambiguity", "emptiness", "universality"], 2, "Mark generating symbols.")],
       summary=["CFG: productions A → α; derivations are leftmost/rightmost; CNF takes 2n−1 steps, GNF n steps.", "Ambiguity: two parse trees for one string; undecidable in general.", "PDA = NFA + stack; final-state and empty-stack acceptance are equivalent; DPDA ⊊ NPDA.",
                "CFLs closed under ∪, ·, *, reversal, homomorphism, ∩ with regular; NOT under ∩ or complement.", "DCFLs are closed under complement.", "Decidable: membership (CYK), emptiness, finiteness; undecidable: equivalence, universality, ambiguity."])
