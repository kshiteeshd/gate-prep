"""Theory of Computation — parametric generators."""
import itertools
import math
import re

from content.kit import *

S = "TOC"
RL, CF, CL, TM = ("Regular Languages & Finite Automata", "Context-Free Languages & PDA", "Closure & Pumping Lemma", "Turing Machines & Decidability")


# ---------------- DFA toolkit ----------------
class DFA:
    def __init__(self, start, delta, accept, alpha="01"):
        self.alpha = alpha
        seen, order, q = {start}, [start], [start]
        self.t = {}
        while q:
            s = q.pop(0)
            for c in alpha:
                n = delta(s, c)
                self.t[(s, c)] = n
                if n not in seen:
                    seen.add(n); order.append(n); q.append(n)
        self.states, self.start = order, start
        self.acc = {s for s in order if accept(s)}

    def run(self, w):
        s = self.start
        for c in w: s = self.t[(s, c)]
        return s in self.acc

    def minimize(self):
        part = {s: (s in self.acc) for s in self.states}
        while True:
            sig = {s: (part[s],) + tuple(part[self.t[(s, c)]] for c in self.alpha) for s in self.states}
            ids = {}
            new = {s: ids.setdefault(sig[s], len(ids)) for s in self.states}
            if len(set(new.values())) == len(set(part.values())):
                return len(set(new.values()))
            part = new

    def count(self, n):
        cur = {self.start: 1}
        for _ in range(n):
            nxt = {}
            for s, v in cur.items():
                for c in self.alpha: nxt[self.t[(s, c)]] = nxt.get(self.t[(s, c)], 0) + v
            cur = nxt
        return sum(v for s, v in cur.items() if s in self.acc)


def kmp_dfa(pat, mode):
    L = len(pat)

    def step(s, c):
        if mode == "contains" and s == L: return L
        t = pat[:s] + c if s < L else pat + c
        for k in range(min(len(t), L), -1, -1):
            if t.endswith(pat[:k]): return k
    return DFA(0, step, lambda s: s == L)


def mod_dfa(k):
    return DFA(0, lambda s, c: (2 * s + int(c)) % k, lambda s: s == 0)


def rbits(r, n):
    return "".join(r.choice("01") for _ in range(n))


@gen(S, RL, "Minimal DFA", n=90, diff="medium")
def r_mindfa(r):
    kind = r.choice(["div", "contains", "ends", "mod_len", "count_mod", "prod"])
    if kind == "div":
        k = r.randint(2, 12)
        return nat(r, "Number of states in the minimal DFA over {0,1} accepting binary strings (MSB first) whose value is divisible by %d?" % k, mod_dfa(k).minimize(), "States = remainders mod %d; all reachable and pairwise distinguishable." % k)
    if kind == "contains":
        p = rbits(r, r.randint(2, 5))
        return nat(r, "Number of states in the minimal DFA (complete, including any dead/trap state) accepting strings over {0,1} that CONTAIN the substring %s?" % p, kmp_dfa(p, "contains").minimize(), "KMP automaton with absorbing accept state: |p| + 1.")
    if kind == "ends":
        p = rbits(r, r.randint(2, 5))
        return nat(r, "Number of states in the minimal DFA over {0,1} accepting strings that END with %s?" % p, kmp_dfa(p, "ends").minimize(), "Track the longest suffix matching a prefix of the pattern.")
    if kind == "mod_len":
        m = r.randint(2, 9)
        return nat(r, "Minimal DFA states for the language of strings over {a} whose length is divisible by %d?" % m, m, "One state per residue class.")
    if kind == "count_mod":
        m, k = r.randint(2, 5), r.randint(2, 4)
        d = DFA((0, 0), lambda s, c: ((s[0] + (c == "0")) % m, (s[1] + (c == "1")) % k), lambda s: s == (0, 0))
        return nat(r, "Minimal DFA states for strings over {0,1} where (#0s mod %d = 0) and (#1s mod %d = 0)?" % (m, k), d.minimize(), "Product automaton of two counters: %d × %d." % (m, k))
    a, b = r.randint(2, 4), r.randint(2, 5)
    d = DFA((0, 0), lambda s, c: ((s[0] + 1) % a if c == "0" else s[0], (s[1] + 1) % b if c == "1" else s[1]), lambda s: s[0] == 0 or s[1] == 0)
    return nat(r, "Minimal DFA states for strings over {0,1} where (#0s mod %d = 0) OR (#1s mod %d = 0)?" % (a, b), d.minimize(), "Product automaton; minimise by partition refinement.")


@gen(S, RL, "Counting accepted strings", n=60, diff="medium")
def r_count(r):
    k = r.randint(2, 5)
    n = r.randint(5, 10)
    kind = r.choice(["div", "contains", "ends", "noconsec"])
    if kind == "div": d, desc = mod_dfa(k), "whose value (binary, MSB first, leading zeros allowed) is divisible by %d" % k
    elif kind == "contains":
        p = rbits(r, 2); d, desc = kmp_dfa(p, "contains"), "that contain the substring %s" % p
    elif kind == "ends":
        p = rbits(r, 3); d, desc = kmp_dfa(p, "ends"), "that end with %s" % p
    else:
        d = DFA(0, lambda s, c: 2 if s == 2 else (1 if c == "1" else 0) if s != 1 or c == "0" else 2, lambda s: s != 2)
        desc = "that contain no two consecutive 1s"
    return nat(r, "How many binary strings of length %d are there %s?" % (n, desc), d.count(n), "Count paths of length %d ending in an accepting state: %d." % (n, d.count(n)))


@gen(S, RL, "Subset construction", n=70, diff="hard", marks=2)
def r_nfa(r):
    n = r.randint(3, 5)
    delta = {}
    for s in range(n):
        for c in "ab":
            delta[(s, c)] = {t for t in range(n) if r.random() < 0.3}
    if not any(delta.values()): raise Skip()
    start = frozenset([0])
    seen, q = {start}, [start]
    while q:
        S_ = q.pop()
        for c in "ab":
            T = frozenset(t for s in S_ for t in delta[(s, c)])
            if T not in seen:
                seen.add(T); q.append(T)
    desc = "; ".join("δ(q%d,%s)={%s}" % (s, c, ",".join("q%d" % t for t in sorted(delta[(s, c)]))) for s in range(n) for c in "ab" if delta[(s, c)])
    return nat(r, "An NFA over {a,b} (no ε-moves) has states q0..q%d, start state q0, and transitions: %s (all unlisted transitions are empty). How many states does the subset-construction DFA have, counting only subsets reachable from {q0} (including ∅ if reachable)?" % (n - 1, desc), len(seen),
               "Reachable subsets: %d." % len(seen))


REGEX = [("(0+1)*00(0+1)*", "(0|1)*00(0|1)*"), ("0*1*", "0*1*"), ("(01)*", "(01)*"), ("(0+1)*1", "(0|1)*1"), ("1(0+1)*0", "1(0|1)*0"), ("0*10*10*", "0*10*10*"),
         ("(00+11)*", "(00|11)*"), ("(0+1)(0+1)(0+1)*", "(0|1)(0|1)(0|1)*"), ("(0+10)*", "(0|10)*"), ("1*(01*0 1*)*".replace(" ", ""), "1*(01*01*)*"), ("(0+1)*0(0+1)(0+1)", "(0|1)*0(0|1)(0|1)"),
         ("0(0+1)*1", "0(0|1)*1"), ("(0*1*)*", "(0*1*)*"), ("(1+01)*(0+ε)", "(1|01)*(0|)")]


@gen(S, RL, "Regular expressions", n=90, diff="easy")
def r_regex(r):
    (disp, py) = r.choice(REGEX)
    n = r.randint(3, 8)
    cnt = sum(1 for w in itertools.product("01", repeat=n) if re.fullmatch(py, "".join(w)))
    if r.random() < 0.7:
        return nat(r, "How many strings of length %d over {0,1} belong to the language of the regular expression  %s  (+ denotes union)?" % (n, disp), cnt, "Brute force over all 2^%d strings." % n)
    short = next(L for L in range(0, 10) if any(re.fullmatch(py, "".join(w)) for w in itertools.product("01", repeat=L)))
    return nat(r, "What is the length of the shortest string in the language of  %s  (+ denotes union)?" % disp, short, "Smallest L with a matching string.")


# ---------------- classification & closure ----------------
LANGS = [("{aⁿbⁿ | n ≥ 0}", "CFL"), ("{aⁿbᵐ | n, m ≥ 0}", "REG"), ("{aⁿbⁿcⁿ | n ≥ 0}", "CSL"), ("{wwᴿ | w ∈ {a,b}*}", "CFL"), ("{ww | w ∈ {a,b}*}", "CSL"),
         ("{aⁿ | n is prime}", "CSL"), ("{a^(2ⁿ) | n ≥ 0}", "CSL"), ("{w | #a(w) = #b(w)}", "CFL"), ("{a^i b^j c^k | i = j or j = k}", "CFL"), ("{aⁿ | n is even}", "REG"),
         ("{w ∈ {a,b}* | w contains the substring ab}", "REG"), ("{aⁿbⁿ cᵐ | n, m ≥ 0}", "CFL"), ("{aⁿbᵐcⁿ⁺ᵐ | n, m ≥ 0}", "CFL"), ("{aⁿ² | n ≥ 0}", "CSL"),
         ("{aⁿbᵐ | n ≠ m}", "CFL"), ("{a^i b^j | i ≥ j}", "CFL"), ("{w | |w| mod 3 = 0}", "REG"), ("{aⁿbⁿ | n ≤ 100}", "REG"), ("{0ⁿ1ⁿ0ⁿ1ⁿ | n ≥ 1}", "CSL")]
NAMES = {"REG": "regular", "CFL": "context-free but not regular", "CSL": "not context-free"}


@gen(S, CL, "Language classification", n=60, diff="medium")
def l_class(r):
    lang, cls = r.choice(LANGS)
    return mcq(r, "The language  L = %s  is" % lang, NAMES[cls], [v for k, v in NAMES.items() if k != cls] + ["not recursively enumerable"], "Pumping lemma / construct a machine: L is %s." % NAMES[cls])


@gen(S, CL, "Language classification", n=60, diff="hard", marks=2)
def l_class_msq(r):
    ls = r.sample(LANGS, 5)
    kind = r.choice(["REG", "CFL_ok"])
    if kind == "REG":
        t = [l for l, c in ls if c == "REG"]; f = [l for l, c in ls if c != "REG"]
        q = "Which of the following languages are regular?"
    else:
        t = [l for l, c in ls if c in ("REG", "CFL")]; f = [l for l, c in ls if c == "CSL"]
        q = "Which of the following languages are context-free?"
    if not t or not f or len(t) + len(f) < 4: raise Skip()
    return msq(r, q + " (select all)", t[:2], f[:3] if len(t[:2]) + len(f[:3]) >= 4 else f, "Classify each language with the pumping lemma / known machines.")


CLOSURE = {"regular": dict(union=1, intersection=1, complement=1, concatenation=1, Kleene_star=1, reversal=1, difference=1, homomorphism=1, inverse_homomorphism=1),
           "context-free": dict(union=1, intersection=0, complement=0, concatenation=1, Kleene_star=1, reversal=1, difference=0, homomorphism=1, inverse_homomorphism=1),
           "deterministic context-free": dict(union=0, intersection=0, complement=1, concatenation=0, Kleene_star=0, reversal=0, difference=0, inverse_homomorphism=1),
           "recursive (decidable)": dict(union=1, intersection=1, complement=1, concatenation=1, Kleene_star=1, reversal=1, difference=1, inverse_homomorphism=1),
           "recursively enumerable": dict(union=1, intersection=1, complement=0, concatenation=1, Kleene_star=1, reversal=1, difference=0, homomorphism=1, inverse_homomorphism=1)}


@gen(S, CL, "Closure properties", n=70, diff="medium", marks=2)
def l_closure(r):
    cls = r.choice(list(CLOSURE))
    d = CLOSURE[cls]
    yes = [k.replace("_", " ") for k, v in d.items() if v]
    no = [k.replace("_", " ") for k, v in d.items() if not v]
    if len(yes) < 2 or len(no) < 2: raise Skip()
    return msq(r, "The class of %s languages is closed under which of the following operations? (select all)" % cls, r.sample(yes, 2), r.sample(no, 2), "Standard closure table for the Chomsky hierarchy.")


@gen(S, CL, "Closure properties", n=30, diff="easy")
def l_closure_one(r):
    cls = r.choice(list(CLOSURE))
    op = r.choice(list(CLOSURE[cls]))
    v = CLOSURE[cls][op]
    return mcq(r, "Is the class of %s languages closed under %s?" % (cls, op.replace("_", " ")), "Yes" if v else "No", ["No" if v else "Yes", "Only for finite languages", "Only for unary alphabets"], "Standard closure table.")


# ---------------- decidability ----------------
DEC = [("Emptiness of a DFA's language", 1), ("Equivalence of two DFAs", 1), ("Whether a CFG generates the empty language", 1), ("Membership of a string in a CFG's language", 1),
       ("Whether a CFG is ambiguous", 0), ("Equivalence of two CFGs", 0), ("Whether a CFG generates Σ*", 0), ("Whether a Turing machine halts on a given input", 0),
       ("Whether a TM accepts the empty string", 0), ("Whether L(M) is empty for a TM M", 0), ("Whether two TMs accept the same language", 0), ("Whether L(M) is regular, for a TM M", 0),
       ("Whether L(M) is finite, for a TM M", 0), ("Membership of a string in a context-sensitive grammar's language", 1), ("Emptiness of a PDA's language", 1), ("Equivalence of two regular expressions", 1),
       ("Post Correspondence Problem", 0), ("Whether a DFA accepts a finite language", 1), ("Whether the intersection of two CFLs is empty", 0), ("Whether a given number is prime", 1),
       ("Whether a TM halts on every input (is total)", 0), ("Emptiness of a context-sensitive grammar's language", 0), ("Whether a regular language is a subset of another regular language", 1), ("Whether two PDAs accept the same language", 0)]


@gen(S, TM, "Decidability", n=80, diff="medium", marks=2)
def t_dec_msq(r):
    und = [x for x, v in DEC if not v]
    dd = [x for x, v in DEC if v]
    if r.random() < 0.5:
        return msq(r, "Which of the following problems are UNDECIDABLE? (select all)", r.sample(und, r.choice([1, 2])), r.sample(dd, 3), "Rice's theorem, reductions from the halting problem and known results.") if False else \
            msq(r, "Which of the following problems are UNDECIDABLE? (select all)", r.sample(und, 2), r.sample(dd, 2), "Rice's theorem, reductions from the halting problem and known results.")
    return msq(r, "Which of the following problems are DECIDABLE? (select all)", r.sample(dd, 2), r.sample(und, 2), "DFAs/PDAs/CFGs have decision algorithms for emptiness/membership; equivalence is decidable only for DFAs.")


@gen(S, TM, "Decidability", n=30, diff="easy")
def t_dec_one(r):
    x, v = r.choice(DEC)
    return mcq(r, "The problem “%s” is" % x, "decidable" if v else "undecidable",
               ["undecidable", "semi-decidable but not decidable", "decidable only for unary alphabets"] if v else ["decidable", "decidable in polynomial time", "decidable only for deterministic machines"], "Known result.")


@gen(S, TM, "Complexity of automata", n=50, diff="medium")
def t_nfa(r):
    n = r.randint(2, 12)
    kind = r.choice(["subset", "rev", "compl", "pda_stack", "tm_states", "states_nfa"])
    if kind == "subset": return nat(r, "An NFA with %d states is converted to an equivalent DFA by subset construction. What is the maximum possible number of DFA states?" % n, 2 ** n, "Power set: 2^n.")
    if kind == "rev": return nat(r, "A minimal DFA for L has %d states. Maximum number of states of a minimal DFA for the REVERSE of L?" % min(n, 8), 2 ** min(n, 8), "Reversal can cause an exponential blow-up in the worst case.")
    if kind == "compl": return nat(r, "A complete minimal DFA for L has %d states. How many states does the minimal DFA for the complement of L have?" % n, n, "Swap accepting and non-accepting states.")
    if kind == "pda_stack": return mcq(r, "A language accepted by a PDA with two independent unbounded stacks is equivalent in power to", "a Turing machine", ["a finite automaton", "a deterministic PDA", "a linear bounded automaton"], "Two stacks can simulate a tape.")
    if kind == "tm_states": return nat(r, "A DFA over alphabet {0,1} with %d states has how many transitions (complete DFA)?" % n, 2 * n, "|Σ| × |Q|.")
    return nat(r, "Number of final-state subsets: an NFA has %d states. How many different sets of accepting states are possible?" % min(n, 10), 2 ** min(n, 10), "Any subset of states can be accepting: 2^n.")


# ---------------- CFL counting ----------------
LANGPRED = [("equal number of a's and b's", lambda w: w.count("a") == w.count("b")), ("more a's than b's", lambda w: w.count("a") > w.count("b")),
            ("palindromes", lambda w: w == w[::-1]), ("of the form aⁿbⁿ", lambda w: re.fullmatch(r"(a*)(b*)", w) and w.count("a") == w.count("b")),
            ("of the form aⁿbᵐ with n ≥ m", lambda w: re.fullmatch(r"a*b*", w) and w.count("a") >= w.count("b")), ("balanced when a = ( and b = )", None)]


def balanced(w):
    d = 0
    for c in w:
        d += 1 if c == "a" else -1
        if d < 0: return False
    return d == 0


@gen(S, CF, "Counting strings", n=70, diff="medium")
def cf_count(r):
    name, pred = r.choice(LANGPRED)
    if pred is None: pred = balanced
    n = r.randint(4, 10)
    c = sum(1 for w in itertools.product("ab", repeat=n) if pred("".join(w)))
    return nat(r, "How many strings of length %d over {a,b} are %s?" % (n, name), c, "Enumerate all 2^%d strings: %d qualify." % (n, c))


GRAM = {"S → aSb | ε": ("aⁿbⁿ", lambda n: 1 if n % 2 == 0 else 0), "S → aS | bS | ε": ("all strings", lambda n: 2 ** n), "S → aSa | bSb | a | b | ε": ("palindromes", lambda n: 2 ** ((n + 1) // 2)),
        "S → SS | (S) | ε": ("balanced parentheses", lambda n: math.comb(n, n // 2) // (n // 2 + 1) if n % 2 == 0 else 0), "S → AB, A → aA | ε, B → bB | ε": ("a*b*", lambda n: n + 1)}


@gen(S, CF, "Grammars", n=40, diff="medium")
def cf_gram(r):
    g, (name, f) = r.choice(list(GRAM.items()))
    n = r.randint(2, 10)
    return nat(r, "Grammar:  %s.  How many distinct strings of length exactly %d does it generate (terminals over the alphabet used in the rules)?" % (g, n), f(n), "Language is %s; count by formula = %d." % (name, f(n)))


@gen(S, CF, "Ambiguity & parse trees", n=40, diff="medium")
def cf_parse(r):
    k = r.randint(2, 8)
    cat = math.comb(2 * k, k) // (k + 1)
    return nat(r, "Grammar E → E + E | E * E | id (ambiguous). Number of distinct parse trees for a string with %d operators (e.g. id + id * id for 2 operators)?" % k, cat, "Catalan number C_%d = %d." % (k, cat))


@gen(S, CF, "Pushdown automata", n=30, diff="easy")
def cf_pda(r):
    n = r.randint(2, 9)
    kind = r.choice(["stack_len", "pushes"])
    if kind == "stack_len": return nat(r, "A PDA accepts {aⁿbⁿ} by pushing one symbol per 'a'. After reading aⁿ with n = %d (and the initial stack symbol Z₀), how many symbols are on the stack?" % n, n + 1, "n pushes plus Z₀.")
    w = "".join(r.choice("ab") for _ in range(n))
    return nat(r, "A PDA for {wcwᴿ | w ∈ {a,b}*} is run on the input %s%s%s. How many push operations (excluding the initial Z₀) occur before the marker c is read?" % (w, "c", w[::-1]), n, "One push per symbol of w.")
