"""Engineering Mathematics — parametric generators (answers by brute force / exact arithmetic)."""
import itertools
import math
from fractions import Fraction
from functools import lru_cache

from content.kit import *

S = "ENGM"
LOGIC, SETS, POSET, GROUP, GRAPH, COMB, MAT, LIN, LIM, INT, PROB, RV = (
    "Propositional & First-Order Logic", "Sets, Relations & Functions", "Partial Orders & Lattices", "Groups & Monoids",
    "Graph Theory", "Combinatorics & Recurrences", "Matrices & Determinants", "Linear Equations & Eigenvalues",
    "Limits, Continuity & Differentiation", "Maxima, Minima & Integration", "Probability Basics & Bayes",
    "Random Variables & Distributions")
C_ = math.comb
F = Fraction


def ratstr(x):
    return fmt(F(x).limit_denominator(10 ** 6))


def dec(x, d=4):
    return round(float(x), d)


# =============== LOGIC ===============
PF = [("p → q", lambda p, q, r: (not p) or q), ("¬p ∨ q", lambda p, q, r: (not p) or q), ("¬q → ¬p", lambda p, q, r: q or (not p)),
      ("q → p", lambda p, q, r: (not q) or p), ("¬(p ∧ ¬q)", lambda p, q, r: not (p and not q)), ("p ∧ ¬q", lambda p, q, r: p and not q),
      ("p ↔ q", lambda p, q, r: p == q), ("¬p ∨ ¬q", lambda p, q, r: not (p and q)), ("(p ∧ q) ∨ (¬p ∧ ¬q)", lambda p, q, r: p == q),
      ("p ⊕ q", lambda p, q, r: p != q), ("p ∨ q", lambda p, q, r: p or q), ("¬p → q", lambda p, q, r: p or q), ("p ∧ q", lambda p, q, r: p and q),
      ("¬(¬p ∨ ¬q)", lambda p, q, r: p and q), ("q → (p → q)", lambda p, q, r: True), ("p ∨ ¬p", lambda p, q, r: True),
      ("p ∧ ¬p", lambda p, q, r: False), ("(p → q) ∧ (q → p)", lambda p, q, r: p == q), ("¬p ∧ ¬q", lambda p, q, r: not (p or q)),
      ("(p ∨ q) ∧ ¬p", lambda p, q, r: q and not p), ("p → (q → r)", lambda p, q, r: (not p) or (not q) or r),
      ("(p ∧ q) → r", lambda p, q, r: (not (p and q)) or r), ("(p → q) → p", lambda p, q, r: p), ("p ∧ (q ∨ r)", lambda p, q, r: p and (q or r)),
      ("(p ∧ q) ∨ (p ∧ r)", lambda p, q, r: (p and q) or (p and r))]


def tt(f):
    return tuple(f(*v) for v in itertools.product([False, True], repeat=3))


@gen(S, LOGIC, "Equivalences", n=55, diff="medium", marks=2)
def l_equiv(r):
    base = r.choice(PF)
    eq = [x for x in PF if tt(x[1]) == tt(base[1]) and x[0] != base[0]]
    ne = [x for x in PF if tt(x[1]) != tt(base[1])]
    if not eq or len(ne) < 2:
        raise Skip()
    cs = r.sample(eq, min(len(eq), r.choice([1, 2])))
    ws = r.sample(ne, 4 - len(cs))
    return msq(r, "Select ALL formulas logically equivalent to  %s" % base[0], [c[0] for c in cs], [w[0] for w in ws], "Compare truth tables over p, q, r.")


@gen(S, LOGIC, "Satisfiability", n=45, diff="easy")
def l_classify(r):
    f = r.choice(PF)
    t = tt(f[1])
    kind = "tautology" if all(t) else "contradiction" if not any(t) else "contingency (satisfiable but not valid)"
    return mcq(r, "The formula  %s  is" % f[0], kind, [k for k in ["tautology", "contradiction", "contingency (satisfiable but not valid)", "valid only when p is true"] if k != kind], "Truth table column: %s." % ["T" if x else "F" for x in t])


def rand_formula(r, vs, depth):
    if depth == 0 or r.random() < 0.25:
        v = r.choice(vs)
        return (v, lambda e, v=v: e[v]) if r.random() < 0.7 else ("¬" + v, lambda e, v=v: not e[v])
    s1, f1 = rand_formula(r, vs, depth - 1)
    s2, f2 = rand_formula(r, vs, depth - 1)
    op = r.choice(["∧", "∨", "→", "⊕", "↔"])
    fn = {"∧": lambda a, b: a and b, "∨": lambda a, b: a or b, "→": lambda a, b: (not a) or b, "⊕": lambda a, b: a != b, "↔": lambda a, b: a == b}[op]
    return "(%s %s %s)" % (s1, op, s2), lambda e: fn(f1(e), f2(e))


@gen(S, LOGIC, "Counting models", n=60, diff="medium")
def l_models(r):
    k = r.choice([3, 4])
    vs = list("pqrs"[:k])
    s, f = rand_formula(r, vs, 3)
    c = sum(1 for v in itertools.product([False, True], repeat=k) if f(dict(zip(vs, v))))
    if len(s) < 11:
        raise Skip()
    return nat(r, "How many of the %d truth assignments to %s satisfy  %s ?" % (2 ** k, ", ".join(vs), s), c, "Brute-force truth table: %d satisfying rows." % c)


@gen(S, LOGIC, "Boolean functions count", n=15, diff="easy")
def l_count(r):
    n = r.randint(1, 4)
    kind = r.choice(["fn", "nontriv"])
    if kind == "fn":
        return nat(r, "Number of distinct Boolean functions of %d variables?" % n, 2 ** (2 ** n), "2^(2^n) = 2^%d = %d." % (2 ** n, 2 ** (2 ** n)))
    return nat(r, "A propositional formula uses %d variables. How many distinct truth assignments are there (rows of the truth table)?" % (n + 2), 2 ** (n + 2), "2^k = %d." % 2 ** (n + 2))


@gen(S, LOGIC, "First-order logic", n=70, diff="hard", marks=2)
def l_fol(r):
    n = r.randint(3, 4)
    rel = {(a, b) for a in range(1, n + 1) for b in range(1, n + 1) if r.random() < 0.45}
    D = range(1, n + 1)
    R = lambda a, b: (a, b) in rel
    stm = [("∀x ∃y R(x,y)", all(any(R(x, y) for y in D) for x in D)), ("∃x ∀y R(x,y)", any(all(R(x, y) for y in D) for x in D)),
           ("∀x ∀y (R(x,y) → R(y,x))", all((not R(x, y)) or R(y, x) for x in D for y in D)), ("∃x R(x,x)", any(R(x, x) for x in D)),
           ("∀x R(x,x)", all(R(x, x) for x in D)), ("∃y ∀x R(x,y)", any(all(R(x, y) for x in D) for y in D)),
           ("∀x ∃y (R(x,y) ∧ x ≠ y)", all(any(R(x, y) and x != y for y in D) for x in D)),
           ("∀x ∀y ∀z ((R(x,y) ∧ R(y,z)) → R(x,z))", all((not (R(x, y) and R(y, z))) or R(x, z) for x in D for y in D for z in D))]
    t = [s for s, v in stm if v]
    f = [s for s, v in stm if not v]
    if not t or not f:
        raise Skip()
    ts = r.sample(t, min(len(t), r.choice([1, 2])))
    fs = r.sample(f, 4 - len(ts)) if len(f) >= 4 - len(ts) else None
    if not fs:
        raise Skip()
    return msq(r, "Domain {%s}, and R = {%s}. Select ALL true statements." % (", ".join(map(str, D)), ", ".join("(%d,%d)" % p for p in sorted(rel))), ts, fs, "Check each quantified statement over the finite domain.")


# =============== SETS / RELATIONS / FUNCTIONS ===============
BELL = [1, 1, 2, 5, 15, 52, 203, 877, 4140]


def surj(m, n):
    return sum((-1) ** i * C_(n, i) * (n - i) ** m for i in range(n + 1))


@gen(S, SETS, "Counting relations & functions", n=60, diff="easy")
def s_count(r):
    n, m = r.randint(2, 5), r.randint(2, 5)
    kind = r.choice(["rel", "refl", "sym", "anti", "fn", "inj", "surj", "bij", "pow", "eqv", "asym", "irrefl"])
    if kind == "rel": return nat(r, "Number of binary relations on a set with %d elements?" % n, 2 ** (n * n), "2^(n²) = 2^%d." % (n * n))
    if kind == "refl": return nat(r, "Number of reflexive relations on a set with %d elements?" % n, 2 ** (n * n - n), "Diagonal fixed ⇒ 2^(n²−n).")
    if kind == "irrefl": return nat(r, "Number of irreflexive relations on a set with %d elements?" % n, 2 ** (n * n - n), "Diagonal excluded ⇒ 2^(n²−n).")
    if kind == "sym": return nat(r, "Number of symmetric relations on a set with %d elements?" % n, 2 ** (n * (n + 1) // 2), "2^(n(n+1)/2).")
    if kind == "anti": return nat(r, "Number of antisymmetric relations on a set with %d elements?" % n, 2 ** n * 3 ** (n * (n - 1) // 2), "2^n · 3^(n(n−1)/2).")
    if kind == "asym": return nat(r, "Number of asymmetric relations on a set with %d elements?" % n, 3 ** (n * (n - 1) // 2), "No diagonal pairs; each unordered pair has 3 choices: 3^(n(n−1)/2).")
    if kind == "fn": return nat(r, "Number of functions from a set of %d elements to a set of %d elements?" % (n, m), m ** n, "m^n = %d." % m ** n)
    if kind == "inj":
        if m < n: m, n = n, m
        return nat(r, "Number of one-to-one (injective) functions from a %d-element set to a %d-element set?" % (n, m), math.perm(m, n), "P(m,n) = %d." % math.perm(m, n))
    if kind == "surj":
        if m > n: m, n = n, m
        return nat(r, "Number of onto functions from a %d-element set to a %d-element set?" % (n, m), surj(n, m), "Inclusion–exclusion: Σ(−1)^i C(m,i)(m−i)^n = %d." % surj(n, m))
    if kind == "bij": return nat(r, "Number of bijections from a %d-element set onto itself?" % n, math.factorial(n), "n! = %d." % math.factorial(n))
    if kind == "pow": return nat(r, "Number of elements in the power set of a set with %d elements?" % (n + 3), 2 ** (n + 3), "2^n.")
    return nat(r, "Number of equivalence relations on a set with %d elements?" % n, BELL[n], "Bell number B%d = %d." % (n, BELL[n]))


def rel_props(rel, n):
    D = range(n)
    refl = all((i, i) in rel for i in D)
    sym = all((j, i) in rel for i, j in rel)
    anti = all(not ((j, i) in rel and i != j) for i, j in rel)
    trans = all((i, k) in rel for i, j in rel for j2, k in rel if j == j2)
    return refl, sym, anti, trans


@gen(S, SETS, "Relation properties", n=80, diff="medium", marks=2)
def s_props(r):
    n = r.randint(3, 4)
    rel = {(i, j) for i in range(n) for j in range(n) if r.random() < 0.4}
    refl, sym, anti, trans = rel_props(rel, n)
    stm = [("reflexive", refl), ("symmetric", sym), ("antisymmetric", anti), ("transitive", trans), ("an equivalence relation", refl and sym and trans),
           ("a partial order", refl and anti and trans), ("irreflexive", all((i, i) not in rel for i in range(n)))]
    t = [s for s, v in stm if v]
    f = [s for s, v in stm if not v]
    if not t or len(f) < 2:
        raise Skip()
    ts = r.sample(t, min(len(t), 2))
    fs = r.sample(f, 4 - len(ts)) if len(f) >= 4 - len(ts) else None
    if not fs:
        raise Skip()
    return msq(r, "On A = {1..%d}, R = {%s}. Select ALL properties R has: R is ..." % (n, ", ".join("(%d,%d)" % (a + 1, b + 1) for a, b in sorted(rel))), ts, fs, "Test each property directly on the pairs.")


@gen(S, SETS, "Closures", n=50, diff="medium")
def s_closure(r):
    n = r.randint(4, 5)
    rel = {(r.randrange(n), r.randrange(n)) for _ in range(r.randint(3, 6))}
    tc = set(rel)
    ch = True
    while ch:
        ch = False
        for a, b in list(tc):
            for c, d in list(tc):
                if b == c and (a, d) not in tc:
                    tc.add((a, d)); ch = True
    kind = r.choice(["trans", "refl", "sym"])
    desc = ", ".join("(%d,%d)" % (a + 1, b + 1) for a, b in sorted(rel))
    if kind == "trans": return nat(r, "R = {%s} on {1..%d}. How many ordered pairs are in the transitive closure of R?" % (desc, n), len(tc), "Warshall's algorithm gives %d pairs." % len(tc))
    if kind == "refl": return nat(r, "R = {%s} on {1..%d}. How many pairs are in the reflexive closure of R?" % (desc, n), len(rel | {(i, i) for i in range(n)}), "R ∪ identity.")
    return nat(r, "R = {%s} on {1..%d}. How many pairs are in the symmetric closure of R?" % (desc, n), len(rel | {(b, a) for a, b in rel}), "R ∪ R⁻¹.")


@gen(S, SETS, "Inclusion–exclusion", n=45, diff="medium")
def s_incl(r):
    a, b, c = r.randint(20, 60), r.randint(20, 60), r.randint(20, 60)
    ab, bc, ac = r.randint(3, 15), r.randint(3, 15), r.randint(3, 15)
    abc = r.randint(1, min(ab, bc, ac))
    return nat(r, "|A| = %d, |B| = %d, |C| = %d, |A∩B| = %d, |B∩C| = %d, |A∩C| = %d, |A∩B∩C| = %d. Find |A ∪ B ∪ C|." % (a, b, c, ab, bc, ac, abc), a + b + c - ab - bc - ac + abc,
               "Σ singles − Σ pairs + triple.")


@gen(S, SETS, "Divisibility counting", n=45, diff="easy")
def s_div(r):
    N = r.choice([100, 200, 500, 1000, 360, 600, 999])
    a, b = r.sample([2, 3, 4, 5, 6, 7, 9, 10, 15], 2)
    kind = r.choice(["either", "neither", "both"])
    l = a * b // math.gcd(a, b)
    e, bo = N // a + N // b - N // l, N // l
    return nat(r, "How many integers in 1..%d are divisible by %s %d and %d?" % (N, {"either": "either", "neither": "neither of", "both": "both"}[kind], a, b),
               {"either": e, "neither": N - e, "both": bo}[kind], "N/a + N/b − N/lcm = %d; both = %d." % (e, bo))


# =============== POSETS / LATTICES ===============
def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def squarefree(n):
    return all(n % (p * p) for p in range(2, int(n ** 0.5) + 1))


@gen(S, POSET, "Divisor lattice", n=60, diff="medium")
def p_div(r):
    n = r.choice([12, 18, 24, 30, 36, 42, 48, 60, 64, 72, 84, 90, 96, 100, 105, 120, 126, 150, 180, 210])
    ds = divisors(n)
    kind = r.choice(["size", "hasse", "bool", "comp", "atoms", "chains"])
    if kind == "size": return nat(r, "Number of elements in the poset (D%d, |) of divisors of %d under divisibility?" % (n, n), len(ds), "Number of divisors = %d." % len(ds))
    if kind == "hasse":
        e = sum(1 for a in ds for b in ds if a != b and b % a == 0 and not any(c not in (a, b) and c % a == 0 and b % c == 0 for c in ds))
        return nat(r, "Number of edges in the Hasse diagram of (D%d, |)?" % n, e, "Count covering pairs: %d." % e)
    if kind == "bool":
        return mcq(r, "Is the lattice (D%d, |) a Boolean algebra?" % n, "Yes" if squarefree(n) else "No", ["No" if squarefree(n) else "Yes", "Only if %d is prime" % n, "Cannot be decided"], "D_n is Boolean iff n is square-free (here n = %d)." % n)
    if kind == "comp":
        c = sum(1 for a in ds if any(math.gcd(a, b) == 1 and a * b // 1 == n for b in ds))
        return nat(r, "How many elements of (D%d, |) have a complement?" % n, c, "a has a complement iff gcd(a, n/a) = 1; count = %d." % c)
    if kind == "atoms":
        at = sum(1 for d in ds if d > 1 and all(not (e > 1 and e < d and d % e == 0) for e in ds))
        return nat(r, "Number of atoms (elements covering the bottom) in (D%d, |)?" % n, at, "Atoms are the primes dividing %d: %d of them." % (n, at))
    # maximal chains = number of prime factors with multiplicity! / prod(e_i!)
    m, f, p = n, [], 2
    while m > 1:
        c = 0
        while m % p == 0: m //= p; c += 1
        if c: f.append(c)
        p += 1
    ch = math.factorial(sum(f)) // math.prod(math.factorial(x) for x in f)
    return nat(r, "Number of maximal chains from 1 to %d in (D%d, |)?" % (n, n), ch, "Multinomial (Σe)! / Πe_i! = %d." % ch)


@gen(S, POSET, "Lattice basics", n=40, diff="easy")
def p_lub(r):
    a, b = r.randint(2, 60), r.randint(2, 60)
    kind = r.choice(["lub", "glb"])
    l, g = a * b // math.gcd(a, b), math.gcd(a, b)
    return mcq(r, "In the poset (ℕ, divisibility), the %s of %d and %d is" % ("least upper bound (join)" if kind == "lub" else "greatest lower bound (meet)", a, b), l if kind == "lub" else g,
               [g if kind == "lub" else l, a * b if a * b not in (l, g) else a + b, max(a, b), l + g], "lub = lcm = %d, glb = gcd = %d." % (l, g))


@gen(S, POSET, "Posets", n=35, diff="medium")
def p_count(r):
    n = r.randint(3, 8)
    kind = r.choice(["totalorders", "powerset", "antichain", "bool"])
    if kind == "totalorders": return nat(r, "Number of different total orders (linear orderings) possible on a set of %d elements?" % n, math.factorial(n), "n! = %d." % math.factorial(n))
    if kind == "powerset": return nat(r, "Number of edges in the Hasse diagram of the power-set lattice (2^S, ⊆) when |S| = %d?" % min(n, 6), min(n, 6) * 2 ** (min(n, 6) - 1), "n·2^(n−1).")
    if kind == "antichain": return nat(r, "Size of the largest antichain in the power-set poset (2^S, ⊆) with |S| = %d (Sperner)?" % n, C_(n, n // 2), "C(n, ⌊n/2⌋) = %d." % C_(n, n // 2))
    return nat(r, "A finite Boolean algebra has %d atoms. How many elements does it have?" % n, 2 ** n, "2^n = %d." % 2 ** n)


# =============== GROUPS ===============
def phi(n):
    return sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)


def perm_order(cycles):
    return math.lcm(*cycles)


@gen(S, GROUP, "Cyclic groups", n=60, diff="easy")
def g_cyc(r):
    n = r.choice([6, 8, 10, 12, 15, 18, 20, 24, 30, 36, 40, 48])
    a = r.randint(1, n - 1)
    kind = r.choice(["ord", "gen", "subgrp", "ordk"])
    if kind == "ord": return nat(r, "Order of the element %d in the group (Z%d, +)?" % (a, n), n // math.gcd(a, n), "n / gcd(a, n) = %d." % (n // math.gcd(a, n)))
    if kind == "gen": return nat(r, "Number of generators of the cyclic group (Z%d, +)?" % n, phi(n), "φ(%d) = %d." % (n, phi(n)))
    if kind == "subgrp": return nat(r, "Number of subgroups of (Z%d, +)?" % n, len(divisors(n)), "One subgroup per divisor of n: %d." % len(divisors(n)))
    k = r.choice(divisors(n))
    return nat(r, "Number of elements of order %d in (Z%d, +)?" % (k, n), phi(k), "φ(%d) = %d." % (k, phi(k)))


@gen(S, GROUP, "Permutation groups", n=40, diff="medium")
def g_perm(r):
    cyc = [r.randint(2, 6) for _ in range(r.randint(2, 3))]
    n = sum(cyc)
    kind = r.choice(["ord", "parity", "size"])
    if kind == "ord":
        return nat(r, "A permutation in S%d is a product of disjoint cycles of lengths %s. Its order is" % (n, cyc), perm_order(cyc), "lcm of cycle lengths = %d." % perm_order(cyc))
    if kind == "parity":
        odd = sum(c - 1 for c in cyc) % 2
        return mcq(r, "A permutation in S%d is a product of disjoint cycles of lengths %s. It is" % (n, cyc), "an odd permutation" if odd else "an even permutation", ["an even permutation" if odd else "an odd permutation", "neither even nor odd", "an identity permutation"],
                   "Parity = Σ(len−1) = %d." % sum(c - 1 for c in cyc))
    m = r.randint(3, 7)
    return nat(r, "Order of the symmetric group S%d?" % m, math.factorial(m), "m! = %d." % math.factorial(m))


@gen(S, GROUP, "Lagrange / group facts", n=45, diff="medium")
def g_lag(r):
    n = r.choice([12, 18, 20, 24, 28, 30, 36, 40, 42, 60])
    kind = r.choice(["nsub", "units", "subord"])
    if kind == "units": return nat(r, "Order of the multiplicative group (Z%d*, ×) of units modulo %d?" % (n, n), phi(n), "φ(%d) = %d." % (n, phi(n)))
    if kind == "nsub":
        ds = divisors(n)
        return mcq(r, "A group G has order %d. Which of the following CANNOT be the order of a subgroup of G?" % n, [d for d in range(2, n) if n % d][0] if True else 0, [d for d in ds if 1 < d < n][:4] or [2, 3, 4], "By Lagrange's theorem a subgroup order must divide |G|.")
    d = r.choice([x for x in divisors(n) if 1 < x < n])
    return nat(r, "A subgroup H of a finite group G has order %d and index %d. What is |G|?" % (d, n // d), n, "|G| = |H| × [G:H] = %d." % n)


@gen(S, GROUP, "Closure under operations", n=55, diff="hard", marks=2)
def g_struct(r):
    m = r.choice([5, 6, 7, 8, 9, 10, 12])
    S_ = list(range(m))
    ops = {"addition modulo %d" % m: lambda a, b: (a + b) % m, "multiplication modulo %d" % m: lambda a, b: (a * b) % m}
    name = r.choice(list(ops))
    op = ops[name]
    if "multiplication" in name:
        U = [a for a in S_ if math.gcd(a, m) == 1]
        full_group = False
        # {1..m-1} under multiplication is a group iff m prime
        sub = list(range(1, m))
        closed = all(op(a, b) in sub for a in sub for b in sub)
        grp = closed and all(any(op(a, b) == 1 for b in sub) for a in sub)
        return mcq(r, "Is the set {1, 2, …, %d} a group under %s?" % (m - 1, name), "Yes" if grp else "No",
                   ["No" if grp else "Yes", "Yes, but only when m is even", "Cannot be decided without checking associativity"],
                   "It is a group iff m is prime (closure and inverses fail otherwise). Here m = %d." % m)
    return nat(r, "In the group (Z%d, +), what is the inverse of %d? (give the element)" % (m, 3 % m or 1), (m - (3 % m or 1)) % m, "Inverse of a is m − a.")


# =============== GRAPH THEORY ===============
def comps(n, edges):
    p = list(range(n))

    def f(x):
        while p[x] != x:
            p[x] = p[p[x]]; x = p[x]
        return x
    for a, b in edges: p[f(a)] = f(b)
    return len({f(i) for i in range(n)})


def chromatic_number(n, edges):
    for k in range(1, n + 1):
        for col in itertools.product(range(k), repeat=n):
            if all(col[a] != col[b] for a, b in edges): return k


def rand_graph(r, n, pr=0.5):
    return sorted({tuple(sorted((a, b))) for a in range(n) for b in range(a + 1, n) if r.random() < pr})


@gen(S, GRAPH, "Degrees & counting", n=60, diff="easy")
def gr_basic(r):
    kind = r.choice(["hand", "cayley", "kmn", "euler", "planar", "faces", "cycle_st", "matching", "tree_leaf"])
    n = r.randint(4, 12)
    if kind == "hand":
        e = r.randint(5, 30)
        return nat(r, "A simple graph has %d edges. What is the sum of degrees of all its vertices?" % e, 2 * e, "Handshake lemma: Σdeg = 2|E| = %d." % (2 * e))
    if kind == "cayley": return nat(r, "Number of labelled spanning trees of K%d?" % min(n, 8), min(n, 8) ** (min(n, 8) - 2), "Cayley: n^(n−2).")
    if kind == "kmn":
        a, b = r.randint(2, 5), r.randint(2, 5)
        return nat(r, "Number of spanning trees of the complete bipartite graph K%d,%d?" % (a, b), a ** (b - 1) * b ** (a - 1), "m^(n−1) · n^(m−1).")
    if kind == "euler": return mcq(r, "A connected simple graph has an Euler circuit iff", "every vertex has even degree", ["it has at most two odd-degree vertices", "it is Hamiltonian", "every vertex has degree ≥ n/2"], "Euler's theorem.")
    if kind == "planar": return nat(r, "Maximum number of edges in a simple connected planar graph with %d vertices (n ≥ 3)?" % n, 3 * n - 6, "3n − 6 = %d." % (3 * n - 6))
    if kind == "faces":
        e = r.randint(n, 3 * n - 6)
        return nat(r, "A connected planar graph has %d vertices and %d edges. Number of faces (including the outer face)?" % (n, e), 2 - n + e, "Euler: V − E + F = 2.")
    if kind == "cycle_st": return nat(r, "Number of spanning trees of the cycle graph C%d?" % n, n, "Remove any one edge: n = %d." % n)
    if kind == "matching": return nat(r, "Number of perfect matchings in the complete graph K%d?" % (2 * (n // 2 or 2)), math.prod(range(1, 2 * (n // 2 or 2), 2)), "(2k−1)!! for K_2k.")
    return nat(r, "A tree has %d vertices and every non-leaf vertex has degree 3. How many leaves does it have? (n must be even)" % (2 * (n // 2) + 2 if False else 2 * (n // 2 or 2)), (2 * (n // 2 or 2)) // 2 + 1 if False else (2 * (n // 2 or 2) + 2) // 2,
               "n₁ = (n+2)/2 for a tree whose internal vertices have degree 3.")


@gen(S, GRAPH, "Chromatic & connectivity", n=70, diff="medium")
def gr_chrom(r):
    n = r.randint(4, 6)
    e = rand_graph(r, n, r.choice([0.4, 0.55, 0.7]))
    if len(e) < n - 1: raise Skip()
    lbl = lambda a, b: "%s%s" % (chr(65 + a), chr(65 + b))
    es = ", ".join(lbl(a, b) for a, b in e)
    if r.random() < 0.55:
        c = chromatic_number(n, e)
        return nat(r, "Undirected graph on vertices %s with edges {%s}. What is its chromatic number?" % (",".join(chr(65 + i) for i in range(n)), es), c, "Try k = 1,2,… colourings; smallest valid k = %d." % c)
    k = comps(n, e)
    deg = [sum(1 for ed in e if i in ed) for i in range(n)]
    return nat(r, "Undirected graph on vertices %s with edges {%s}. What is the maximum vertex degree?" % (",".join(chr(65 + i) for i in range(n)), es), max(deg), "Degrees: %s." % deg)


@gen(S, GRAPH, "Chromatic & connectivity", n=30, diff="medium")
def gr_known(r):
    n = r.randint(4, 9)
    kind = r.choice(["cyc", "wheel", "bip", "petersen", "kn", "tree", "cliq"])
    if kind == "cyc": return nat(r, "Chromatic number of the cycle graph C%d?" % n, 2 if n % 2 == 0 else 3, "Even cycles are bipartite (2); odd cycles need 3.")
    if kind == "wheel": return nat(r, "Chromatic number of the wheel graph W%d (a hub joined to a cycle of %d vertices)?" % (n, n), 3 if n % 2 == 0 else 4, "Hub needs its own colour; the rim needs 2 (even) or 3 (odd).")
    if kind == "bip": return nat(r, "Chromatic number of the complete bipartite graph K%d,%d?" % (r.randint(2, 6), r.randint(2, 6)), 2, "Bipartite with at least one edge ⇒ 2.")
    if kind == "petersen": return nat(r, "Number of edges in the Petersen graph (10 vertices, 3-regular)?", 15, "10·3/2 = 15.")
    if kind == "kn": return nat(r, "Size of the largest clique forces chromatic number ≥ that size. What is the chromatic number of K%d?" % n, n, "Every vertex adjacent to every other.")
    if kind == "tree": return nat(r, "Chromatic number of any tree with at least 2 vertices?", 2, "Trees are bipartite.")
    k = r.randint(3, 8)
    return nat(r, "Maximum number of edges in a simple graph with %d vertices that is NOT connected?" % k, C_(k - 1, 2), "Take K_{n−1} plus an isolated vertex: C(n−1, 2).")


# =============== COMBINATORICS ===============
def derange(n):
    a, b = 1, 0
    for i in range(2, n + 1): a, b = b, (i - 1) * (a + b)
    return b if n > 1 else 0


def derangement(n):
    d = [1, 0]
    for i in range(2, n + 1): d.append((i - 1) * (d[-1] + d[-2]))
    return d[n]


@gen(S, COMB, "Counting", n=90, diff="easy")
def c_basic(r):
    kind = r.choice(["comb", "perm", "circ", "stars", "bars_lb", "word", "grid", "cat", "der", "handshake", "bin"])
    n = r.randint(5, 12)
    k = r.randint(2, 4)
    if kind == "comb": return nat(r, "In how many ways can a committee of %d be chosen from %d people?" % (k, n), C_(n, k), "C(%d,%d) = %d." % (n, k, C_(n, k)))
    if kind == "perm": return nat(r, "How many ways can %d distinct books be arranged on a shelf choosing %d of %d books?" % (k, k, n), math.perm(n, k), "P(%d,%d) = %d." % (n, k, math.perm(n, k)))
    if kind == "circ": return nat(r, "In how many ways can %d people sit around a circular table (rotations considered identical)?" % n, math.factorial(n - 1), "(n−1)! = %d." % math.factorial(n - 1))
    if kind == "stars": return nat(r, "Number of non-negative integer solutions of x₁ + x₂ + … + x%d = %d?" % (k + 1, n), C_(n + k, k), "C(n+k, k) with k+1 variables = %d." % C_(n + k, k))
    if kind == "bars_lb":
        return nat(r, "Number of positive integer solutions of x₁ + x₂ + … + x%d = %d?" % (k + 1, n + k), C_(n + k - 1, k), "Each xᵢ ≥ 1: C(%d, %d) = %d." % (n + k - 1, k, C_(n + k - 1, k)))
    if kind == "word":
        w = r.choice(["MISSISSIPPI", "BANANA", "LETTER", "COMMITTEE", "STATISTICS", "ENGINEERING", "ASSESSMENT", "PROGRAMMING", "MATHEMATICS"])
        from collections import Counter
        v = math.factorial(len(w)) // math.prod(math.factorial(c) for c in Counter(w).values())
        return nat(r, "Number of distinct arrangements of all letters of the word %s?" % w, v, "n! / Π(mᵢ!) = %d." % v)
    if kind == "grid":
        a, b = r.randint(2, 7), r.randint(2, 7)
        return nat(r, "A robot moves only right or up from (0,0) to (%d,%d) on a grid. Number of distinct shortest paths?" % (a, b), C_(a + b, a), "C(%d,%d) = %d." % (a + b, a, C_(a + b, a)))
    if kind == "cat":
        m = r.randint(3, 9)
        v = C_(2 * m, m) // (m + 1)
        return nat(r, "Number of structurally distinct binary search trees with %d nodes (equivalently, valid ways to fully parenthesise %d+1 factors)?" % (m, m), v, "Catalan number C%d = %d." % (m, v))
    if kind == "der":
        m = r.randint(3, 8)
        return nat(r, "Number of derangements (no element in its original position) of %d distinct objects?" % m, derangement(m), "D_n = (n−1)(D_{n−1} + D_{n−2}) gives %d." % derangement(m))
    if kind == "handshake": return nat(r, "At a party of %d people everyone shakes hands with everyone else exactly once. Total number of handshakes?" % n, C_(n, 2), "C(n,2) = %d." % C_(n, 2))
    return nat(r, "Value of the sum  C(%d,0) + C(%d,1) + … + C(%d,%d)?" % (n, n, n, n), 2 ** n, "Σ C(n,k) = 2^n.")


@gen(S, COMB, "Pigeonhole & advanced counting", n=50, diff="medium")
def c_adv(r):
    kind = r.choice(["pigeon", "pigeon2", "digits", "evenodd", "binom_coef", "dist"])
    if kind == "pigeon":
        b, k = r.randint(5, 40), r.randint(2, 5)
        return nat(r, "Minimum number of objects that must be placed in %d boxes to guarantee some box has at least %d objects?" % (b, k), b * (k - 1) + 1, "b(k−1)+1 = %d." % (b * (k - 1) + 1))
    if kind == "pigeon2":
        n = r.randint(3, 10)
        return nat(r, "How many integers must be chosen from {1,2,…,%d} to guarantee that two of them sum to %d?" % (2 * n, 2 * n + 1), n + 1, "Pair up (i, %d−i): %d pairs ⇒ n+1 = %d." % (2 * n + 1, n, n + 1))
    if kind == "digits":
        d = r.randint(3, 5)
        return nat(r, "How many %d-digit positive integers have all distinct digits?" % d, 9 * math.perm(9, d - 1), "First digit 9 ways (non-zero), remaining P(9,%d)." % (d - 1))
    if kind == "evenodd":
        d = r.randint(3, 5)
        return nat(r, "How many %d-digit numbers are divisible by 5?" % d, 9 * 10 ** (d - 2) * 2, "Last digit 0/5 (2 choices), first digit 9, middle %d free digits." % (d - 2))
    if kind == "binom_coef":
        n, k = r.randint(4, 10), r.randint(1, 4)
        a, b = r.randint(1, 3), r.randint(1, 3)
        return nat(r, "Coefficient of x^%d in the expansion of (%dx + %d)^%d?" % (k, a, b, n), C_(n, k) * a ** k * b ** (n - k), "C(n,k)·a^k·b^(n−k).")
    n, k = r.randint(4, 9), r.randint(2, 4)
    return nat(r, "Number of ways to distribute %d identical balls into %d distinct boxes with each box getting at least one ball?" % (n + k, k), C_(n + k - 1, k - 1), "Stars and bars with positive parts: C(%d,%d)." % (n + k - 1, k - 1))


def lin_rec(c1, c2, a0, a1, n):
    x, y = a0, a1
    for _ in range(n - 1): x, y = y, c1 * y + c2 * x
    return y if n >= 1 else a0


@gen(S, COMB, "Recurrence relations", n=70, diff="medium", marks=2)
def c_rec(r):
    c1, c2, a0, a1, n = r.randint(1, 4), r.randint(-2, 3), r.randint(0, 3), r.randint(1, 4), r.randint(4, 8)
    if c2 == 0: raise Skip()
    v = lin_rec(c1, c2, a0, a1, n)
    sign = "+ %d" % c2 if c2 > 0 else "− %d" % -c2
    return nat(r, "Sequence: a₀ = %d, a₁ = %d, aₙ = %d·aₙ₋₁ %s·aₙ₋₂. Find a%d." % (a0, a1, c1, sign, n), v, "Iterate the recurrence: a%d = %d." % (n, v))


@gen(S, COMB, "Recurrence relations", n=40, diff="hard", marks=2)
def c_rec_char(r):
    r1, r2 = r.sample([1, 2, 3, 4, -1, -2], 2)
    c1, c2 = r1 + r2, -r1 * r2
    n = r.randint(3, 7)
    kind = r.choice(["roots", "val"])
    if kind == "roots":
        return mcq(r, "The recurrence aₙ = %d·aₙ₋₁ %s %d·aₙ₋₂ has characteristic roots" % (c1, "+" if c2 >= 0 else "−", abs(c2)), "%d and %d" % tuple(sorted((r1, r2))),
                   ["%d and %d" % (-r1, -r2), "%d and %d" % (r1 + 1, r2 + 1), "%d and %d" % (r1, -r2), "%d and %d" % (c1, c2)], "Solve x² − %d x %s %d = 0." % (c1, "+" if -c2 >= 0 else "−", abs(c2)))
    a0, a1 = 1, r1 + r2
    return nat(r, "aₙ = %d·aₙ₋₁ %s %d·aₙ₋₂ with a₀ = 1, a₁ = %d. Find a%d." % (c1, "+" if c2 >= 0 else "−", abs(c2), a1, n), lin_rec(c1, c2, a0, a1, n), "Iterate: a%d = %d." % (n, lin_rec(c1, c2, a0, a1, n)))


# =============== MATRICES ===============
def det3(m):
    a, b, c = m[0]; d, e, f = m[1]; g, h, i = m[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def rank_of(rows):
    m = [[F(x) for x in row] for row in rows]
    rk, cols = 0, len(m[0])
    for c in range(cols):
        piv = next((i for i in range(rk, len(m)) if m[i][c] != 0), None)
        if piv is None: continue
        m[rk], m[piv] = m[piv], m[rk]
        for i in range(len(m)):
            if i != rk and m[i][c] != 0:
                f = m[i][c] / m[rk][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[rk])]
        rk += 1
    return rk


def mstr(m):
    return "\n".join("[ " + "  ".join("%3d" % x for x in row) + " ]" for row in m)


@gen(S, MAT, "Determinants", n=60, diff="easy")
def m_det(r):
    n = r.choice([2, 3, 3])
    m = [[r.randint(-4, 6) for _ in range(n)] for _ in range(n)]
    d = m[0][0] * m[1][1] - m[0][1] * m[1][0] if n == 2 else det3(m)
    return nat(r, "Determinant of the matrix\n```\n%s\n```" % mstr(m), d, "Expand along the first row: %d." % d)


@gen(S, MAT, "Determinant properties", n=60, diff="medium")
def m_detprop(r):
    n, d = r.randint(2, 4), r.choice([-3, -2, 2, 3, 4, 5])
    k = r.choice([2, 3, -1])
    kind = r.choice(["scalar", "adj", "inv", "pow", "prod", "tr"])
    if kind == "scalar": return nat(r, "A is a %d × %d matrix with det(A) = %d. Find det(%dA)." % (n, n, d, k), k ** n * d, "det(kA) = kⁿ·det(A) = %d." % (k ** n * d))
    if kind == "adj": return nat(r, "A is a %d × %d invertible matrix with det(A) = %d. Find det(adj(A))." % (n, n, d), d ** (n - 1), "det(adj A) = det(A)^(n−1) = %d." % d ** (n - 1))
    if kind == "inv": return mcq(r, "A is invertible with det(A) = %d. Then det(A⁻¹) equals" % d, F(1, d), [d, -d, F(1, d * d), d * d], "det(A⁻¹) = 1/det(A).")
    if kind == "pow": return nat(r, "det(A) = %d for a 3 × 3 matrix A. Find det(A³)." % d, d ** 3, "det(Aᵏ) = det(A)ᵏ.")
    if kind == "prod":
        e = r.choice([2, 3, -2, 4])
        return nat(r, "A and B are n × n matrices, det(A) = %d, det(B) = %d. Find det(AB)." % (d, e), d * e, "det(AB) = det(A)det(B).")
    return nat(r, "A is a 3 × 3 matrix with det(A) = %d. Find det(Aᵀ·A)." % d, d * d, "det(AᵀA) = det(A)².")


@gen(S, MAT, "Rank", n=60, diff="medium")
def m_rank(r):
    kind = r.choice(["dep", "full", "lowrank"])
    n = 3
    base = [[r.randint(-3, 4) for _ in range(4)] for _ in range(2)]
    rows = [base[0], base[1], [a * 2 + b * -1 for a, b in zip(*base)] if kind == "dep" else [r.randint(-3, 4) for _ in range(4)]]
    if kind == "lowrank":
        rows = [base[0], [x * r.choice([2, -1, 3]) for x in base[0]], [x * 2 for x in base[0]]]
    rk = rank_of(rows)
    return mcq(r, "Rank of the matrix\n```\n%s\n```" % mstr(rows), rk, [x for x in range(0, 4) if x != rk], "Row-reduce: rank = %d." % rk)


@gen(S, MAT, "Rank-nullity", n=40, diff="easy")
def m_nullity(r):
    m, n = r.randint(3, 8), r.randint(3, 8)
    rk = r.randint(1, min(m, n))
    kind = r.choice(["null", "free", "left"])
    if kind == "null": return nat(r, "A is %d × %d with rank %d. Dimension of the null space of A?" % (m, n, rk), n - rk, "Rank–nullity: n − rank = %d." % (n - rk))
    if kind == "free": return nat(r, "A homogeneous system Ax = 0 has %d equations in %d unknowns and the coefficient matrix has rank %d. Number of free variables?" % (m, n, rk), n - rk, "n − rank.")
    return nat(r, "A is %d × %d with rank %d. Dimension of the null space of Aᵀ?" % (m, n, rk), m - rk, "Aᵀ is %d × %d, nullity = m − rank." % (n, m))


# =============== LINEAR EQUATIONS & EIGENVALUES ===============
@gen(S, LIN, "Eigenvalues", n=70, diff="medium")
def e_basic(r):
    l1, l2 = r.sample(range(-4, 8), 2)
    P = [[1, r.randint(1, 3)], [r.randint(0, 2), 1]]
    det = P[0][0] * P[1][1] - P[0][1] * P[1][0]
    if det == 0: raise Skip()
    Pi = [[F(P[1][1], det), F(-P[0][1], det)], [F(-P[1][0], det), F(P[0][0], det)]]
    D = [[l1, 0], [0, l2]]
    A = [[sum(P[i][k] * D[k][k2] for k in range(2)) for k2 in range(2)] for i in range(2)]
    A = [[sum(A[i][k] * Pi[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    if any(F(x).denominator != 1 for row in A for x in row): raise Skip()
    A = [[int(x) for x in row] for row in A]
    kind = r.choice(["sum", "prod", "max", "sq", "inv", "shift"])
    mt = "```\n%s\n```" % mstr(A)
    if kind == "sum": return nat(r, "Sum of the eigenvalues of\n%s" % mt, l1 + l2, "Sum of eigenvalues = trace = %d." % (A[0][0] + A[1][1]))
    if kind == "prod": return nat(r, "Product of the eigenvalues of\n%s" % mt, l1 * l2, "Product = determinant = %d." % (l1 * l2))
    if kind == "max": return nat(r, "Largest eigenvalue of\n%s" % mt, max(l1, l2), "Characteristic polynomial roots: %d and %d." % (l1, l2))
    if kind == "sq": return nat(r, "Sum of the eigenvalues of A² where A =\n%s" % mt, l1 ** 2 + l2 ** 2, "Eigenvalues of A² are λ²: %d, %d." % (l1 ** 2, l2 ** 2))
    if kind == "shift":
        c = r.randint(1, 5)
        return nat(r, "Sum of eigenvalues of A + %dI where A =\n%s" % (c, mt), l1 + l2 + 2 * c, "Each eigenvalue shifts by %d." % c)
    if 0 in (l1, l2): raise Skip()
    return mcq(r, "Sum of the eigenvalues of A⁻¹ where A =\n%s" % mt, F(1, l1) + F(1, l2), [l1 + l2, F(1, l1 + l2) if l1 + l2 else 7, F(1, l1) - F(1, l2), l1 * l2], "Eigenvalues of A⁻¹ are 1/λ.")


@gen(S, LIN, "Eigenvalue facts", n=50, diff="easy")
def e_facts(r):
    n = r.randint(3, 5)
    ev = [r.randint(-3, 6) for _ in range(n)]
    kind = r.choice(["trace", "det", "tri", "sing", "nil"])
    if kind == "trace": return nat(r, "A %d × %d matrix has eigenvalues %s. Its trace is" % (n, n, ev), sum(ev), "Trace = sum of eigenvalues.")
    if kind == "det": return nat(r, "A %d × %d matrix has eigenvalues %s. Its determinant is" % (n, n, ev), math.prod(ev), "det = product of eigenvalues.")
    if kind == "tri":
        d = [r.randint(1, 9) for _ in range(n)]
        return nat(r, "An upper-triangular %d × %d matrix has diagonal entries %s. The sum of its eigenvalues is" % (n, n, d), sum(d), "Eigenvalues of a triangular matrix are its diagonal entries.")
    if kind == "sing": return mcq(r, "A square matrix is singular iff", "0 is an eigenvalue", ["1 is an eigenvalue", "all eigenvalues are distinct", "its trace is zero"], "det = Πλ = 0 ⇔ some λ = 0.")
    k = r.randint(2, 6)
    return nat(r, "A nilpotent matrix of order %d (Aᵏ = 0 for some k) has trace" % n, 0, "All eigenvalues of a nilpotent matrix are 0.")


@gen(S, LIN, "Linear systems", n=60, diff="medium", marks=2)
def e_system(r):
    kind = r.choice(["unique", "inf", "none"])
    A = [[r.randint(-3, 4) for _ in range(3)] for _ in range(2)]
    A.append([x + y for x, y in zip(A[0], A[1])])
    b = [r.randint(-3, 5) for _ in range(2)]
    b3 = {"inf": b[0] + b[1], "none": b[0] + b[1] + r.randint(1, 3), "unique": None}[kind]
    if kind == "unique":
        A = [[r.randint(-3, 4) for _ in range(3)] for _ in range(3)]
        if det3(A) == 0: raise Skip()
        b3 = r.randint(-3, 5)
    b = [b[0], b[1], b3]
    aug = [A[i] + [b[i]] for i in range(3)]
    rA, rAb = rank_of(A), rank_of(aug)
    res = "a unique solution" if rA == rAb == 3 else ("infinitely many solutions" if rA == rAb else "no solution")
    eq = "\n".join("%+d x %+d y %+d z = %d" % (A[i][0], A[i][1], A[i][2], b[i]) for i in range(3))
    return mcq(r, "The system\n```\n%s\n```\nhas" % eq, res, [x for x in ["a unique solution", "infinitely many solutions", "no solution", "exactly two solutions"] if x != res],
               "rank(A) = %d, rank([A|b]) = %d, unknowns = 3." % (rA, rAb))


@gen(S, LIN, "Linear systems", n=30, diff="easy")
def e_solcount(r):
    m, n, rk = r.randint(3, 6), r.randint(3, 6), r.randint(1, 3)
    rk = min(rk, m, n)
    return nat(r, "A consistent linear system Ax = b has an m × n coefficient matrix (m = %d equations, n = %d unknowns) of rank %d. How many free parameters does the general solution contain?" % (m, n, rk), n - rk, "n − rank = %d." % (n - rk))


# =============== CALCULUS ===============
@gen(S, LIM, "Limits", n=80, diff="easy")
def k_lim(r):
    a, b = r.randint(1, 9), r.randint(1, 9)
    kind = r.choice(["sin", "tan", "rat", "ratdeg", "exp", "cos", "euler", "ln"])
    if kind == "sin": return mcq(r, "lim (x→0) sin(%dx)/(%dx)·x/x ... evaluate lim (x→0) sin(%dx) / %dx" % (a, b, a, b) if False else "Evaluate lim (x→0) sin(%dx) / (%dx)." % (a, b), F(a, b), [F(b, a), 1, 0, a * b], "sin(ax)/(bx) → a/b.")
    if kind == "tan": return mcq(r, "Evaluate lim (x→0) tan(%dx) / (%dx)." % (a, b), F(a, b), [F(b, a), 1, 0, a + b], "tan(ax)/x → a.")
    if kind == "rat":
        c, d = r.randint(1, 9), r.randint(1, 9)
        return mcq(r, "Evaluate lim (x→∞) (%dx² + %dx) / (%dx² + %d)." % (a, b, c, d), F(a, c), [0, "∞", F(b, c), F(a + b, c + d)], "Ratio of leading coefficients.")
    if kind == "ratdeg": return mcq(r, "Evaluate lim (x→∞) (%dx + %d) / (x² + %d)." % (a, b, r.randint(1, 5)), 0, [a, "∞", 1, b], "Denominator has higher degree ⇒ 0.")
    if kind == "exp": return mcq(r, "Evaluate lim (x→0) (e^(%dx) − 1) / x." % a, a, [1, 0, "e", F(1, a)], "(e^{ax}−1)/x → a.")
    if kind == "cos": return mcq(r, "Evaluate lim (x→0) (1 − cos x) / x²." % () if False else "Evaluate lim (x→0) (1 − cos(%dx)) / x²." % a, F(a * a, 2), [F(a, 2), a, 0, F(1, 2)], "1 − cos(ax) ≈ a²x²/2.")
    if kind == "euler": return mcq(r, "Evaluate lim (x→∞) (1 + %d/x)^x." % a, "e^%d" % a, ["e", "e^%d" % -a, "%d" % a, "1"], "(1 + a/x)^x → e^a.")
    return nat(r, "Evaluate lim (x→1) (x^%d − 1) / (x − 1)." % (a + 1), a + 1, "Derivative of x^n at 1 is n = %d." % (a + 1))


@gen(S, LIM, "Continuity", n=45, diff="medium", marks=2)
def k_cont(r):
    a, b = r.randint(1, 5), r.randint(1, 5)
    c = r.randint(1, 4)
    # f(x)=a x + b for x<c ; k x^2 for x>=c  -> continuous: a c + b = k c^2
    num, den = a * c + b, c * c
    k = F(num, den)
    return mcq(r, "f(x) = %dx + %d for x < %d and f(x) = kx² for x ≥ %d. For which value of k is f continuous at x = %d?" % (a, b, c, c, c), k, [F(den, num), k + 1, k * 2, a], "Match left and right limits at x = %d: %d = k·%d." % (c, num, den))


@gen(S, LIM, "Differentiation", n=80, diff="easy")
def k_diff(r):
    a, b, c, x0 = r.randint(1, 6), r.randint(-5, 6), r.randint(-5, 8), r.randint(-3, 4)
    kind = r.choice(["poly", "prod", "quot", "chain", "second", "exp", "mvt"])
    if kind == "poly":
        return nat(r, "If f(x) = %dx³ %+dx² %+dx + 5, find f′(%d)." % (a, b, c, x0), 3 * a * x0 ** 2 + 2 * b * x0 + c, "f′(x) = %dx² %+dx %+d." % (3 * a, 2 * b, c))
    if kind == "prod":
        return nat(r, "If f(x) = (%dx + %d)(x² %+d), find f′(%d)." % (a, b, c, x0), a * (x0 ** 2 + c) + (a * x0 + b) * 2 * x0, "Product rule.")
    if kind == "quot":
        x0 = abs(x0) + 1
        return nat(r, "If f(x) = x² / (x + %d), find f′(%d). (up to 3 decimals)" % (a, x0), dec(F(2 * x0 * (x0 + a) - x0 * x0, (x0 + a) ** 2), 3), "Quotient rule.", tol=0.002)
    if kind == "chain": return nat(r, "If f(x) = (%dx + %d)⁴, find f′(0)." % (a, b), 4 * b ** 3 * a, "Chain rule: 4(ax+b)³·a at 0.")
    if kind == "second": return nat(r, "If f(x) = x⁴ %+dx³ + %dx, find f″(%d)." % (b, c, x0), 12 * x0 ** 2 + 6 * b * x0, "f″ = 12x² + 6bx.")
    if kind == "exp": return nat(r, "If f(x) = x·e^{%dx}, find f′(0)." % a, 1, "f′ = e^{ax}(1 + ax) ⇒ f′(0) = 1.")
    lo = r.randint(0, 2)
    hi = lo + 2 * r.randint(1, 3)
    return nat(r, "By the Mean Value Theorem, find c in (%d, %d) with f′(c) = (f(%d)−f(%d))/%d for f(x) = x²." % (lo, hi, hi, lo, hi - lo), (lo + hi) / 2, "f′(c) = 2c = (hi+lo) ⇒ c = (lo+hi)/2.")


@gen(S, INT, "Maxima & minima", n=70, diff="medium")
def k_opt(r):
    kind = r.choice(["cubic_max", "cubic_val", "quad_min", "crit_count", "inflect"])
    p, q = r.sample(range(-4, 5), 2)
    if p == q: raise Skip()
    lo, hi = min(p, q), max(p, q)
    # f(x) = x^3/3 - (p+q)x^2/2 + p q x ; f'(x) = (x-p)(x-q)
    f = lambda x: F(x ** 3, 3) - F(p + q, 2) * x * x + p * q * x
    fx = "x³/3 %s x² %s x" % (("− %s" % ratstr(F(p + q, 2))) if p + q >= 0 else ("+ %s" % ratstr(F(-(p + q), 2))), ("+ %d" % (p * q)) if p * q >= 0 else ("− %d" % -(p * q)))
    if kind == "cubic_max": return nat(r, "f(x) = %s. Find the x-coordinate of its local maximum." % fx, lo, "f′(x) = (x−%d)(x−%d); f′ goes + to − at the smaller root %d." % (p, q, lo))
    if kind == "cubic_val": return nat(r, "f(x) = %s. Find the local maximum value (up to 3 decimals)." % fx, dec(f(lo), 3), "Evaluate f at x = %d." % lo, tol=0.002)
    if kind == "inflect": return nat(r, "f(x) = %s. At what x does f have a point of inflection? (up to 2 decimals)" % fx, dec(F(p + q, 2), 2), "f″ = 2x − (p+q) = 0.", tol=0.01)
    if kind == "crit_count": return nat(r, "How many critical points does f(x) = %s have?" % fx, 2, "f′(x) = (x−%d)(x−%d) has two real roots." % (p, q))
    a, b, c = r.randint(1, 5), r.randint(-8, 8), r.randint(-5, 9)
    return nat(r, "Minimum value of f(x) = %dx² %+dx %+d?" % (a, b, c), dec(F(4 * a * c - b * b, 4 * a), 3), "c − b²/(4a).", tol=0.002)


@gen(S, INT, "Definite integrals", n=80, diff="easy")
def k_int(r):
    a, n, lo, hi = r.randint(1, 6), r.randint(1, 5), 0, r.randint(1, 4)
    kind = r.choice(["poly", "exp", "sin", "avg", "area", "by_parts", "ln"])
    if kind == "poly": return nat(r, "Evaluate ∫ from %d to %d of %dx^%d dx. (up to 3 decimals)" % (lo, hi, a, n), dec(F(a * hi ** (n + 1), n + 1), 3), "a·x^{n+1}/(n+1).", tol=0.002)
    if kind == "exp": return nat(r, "Evaluate ∫ from 0 to ln(%d) of e^x dx." % (a + 1), a, "e^{ln(a+1)} − 1 = %d." % a)
    if kind == "sin": return mcq(r, "Evaluate ∫ from 0 to π of sin(x) dx.", 2, [0, 1, math.pi, -2], "[−cos x] from 0 to π = 2.")
    if kind == "avg": return nat(r, "Average value of f(x) = x² on [0, %d]. (up to 3 decimals)" % (hi + 1), dec(F((hi + 1) ** 2, 3), 3), "(1/b)∫x² = b²/3.", tol=0.002)
    if kind == "area": return nat(r, "Area under y = %dx from x = 0 to x = %d?" % (a, hi + 1), F(a * (hi + 1) ** 2, 2), "Triangle: ½·base·height.")
    if kind == "by_parts": return nat(r, "Evaluate ∫ from 0 to 1 of x·e^x dx. (up to 3 decimals)", 1, "Integration by parts gives [(x−1)e^x]₀¹ = 1.")
    return nat(r, "Evaluate ∫ from 1 to e^%d of (1/x) dx." % a, a, "ln(e^a) − ln 1 = a.")


# =============== PROBABILITY ===============
@gen(S, PROB, "Dice & coins", n=80, diff="easy")
def pr_dice(r):
    kind = r.choice(["sum", "atleast", "coins", "twodice", "cards", "balls", "cond"])
    if kind == "sum":
        s = r.randint(2, 12)
        c = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s)
        return mcq(r, "Two fair dice are rolled. Probability that the sum is %d?" % s, F(c, 36), [F(c + 1, 36), F(c, 18), F(c, 6), F(max(c - 1, 1), 36)], "%d favourable outcomes out of 36." % c)
    if kind == "atleast":
        n, k = r.randint(2, 5), r.randint(1, 6)
        v = 1 - F(5, 6) ** n
        return mcq(r, "A fair die is rolled %d times. Probability of getting at least one six?" % n, v, [F(1, 6) ** n, 1 - F(1, 6) ** n, F(n, 6), F(5, 6) ** n], "1 − (5/6)^%d." % n)
    if kind == "coins":
        n, k = r.randint(4, 8), r.randint(1, 4)
        return mcq(r, "A fair coin is tossed %d times. Probability of exactly %d heads?" % (n, k), F(C_(n, k), 2 ** n), [F(C_(n, k + 1), 2 ** n), F(1, 2 ** n), F(k, n), F(C_(n, k), 2 ** (n - 1))], "C(n,k)/2^n.")
    if kind == "twodice":
        t = r.randint(7, 11)
        c = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b >= t)
        return nat(r, "Two fair dice are thrown. Number of outcomes (out of 36) in which the sum is at least %d?" % t, c, "Enumerate outcomes.")
    if kind == "cards":
        return mcq(r, "A card is drawn at random from a standard 52-card deck. Probability that it is a %s?" % ("king or a heart" if kind == "cards" else ""), F(16, 52), [F(17, 52), F(15, 52), F(4, 52), F(13, 52)], "4 + 13 − 1 = 16 favourable cards.")
    if kind == "balls":
        a, b = r.randint(3, 8), r.randint(3, 8)
        return mcq(r, "A bag has %d red and %d blue balls. Two are drawn without replacement. Probability both are red?" % (a, b), F(a * (a - 1), (a + b) * (a + b - 1)), [F(a * a, (a + b) ** 2), F(a, a + b), F(a * (a - 1), (a + b) ** 2), F(2 * a, a + b)], "(a/(a+b))·((a−1)/(a+b−1)).")
    return mcq(r, "Two fair dice are rolled and the sum is known to be 8. Probability that at least one die shows 3?", F(2, 5), [F(1, 3), F(11, 36), F(1, 5), F(5, 36)], "Sum 8: 5 outcomes; with a 3: (3,5),(5,3) = 2 ⇒ 2/5.")


@gen(S, PROB, "Bayes & conditional", n=70, diff="medium", marks=2)
def pr_bayes(r):
    pa = F(r.choice([1, 2, 3, 5, 10, 20]), 100)
    pba, pbn = F(r.choice([60, 70, 80, 90, 95]), 100), F(r.choice([5, 10, 20, 30]), 100)
    pb = pa * pba + (1 - pa) * pbn
    post = pa * pba / pb
    kind = r.choice(["post", "total"])
    if kind == "total":
        return nat(r, "P(A) = %s, P(B|A) = %s, P(B|¬A) = %s. Find P(B). (up to 4 decimals)" % (fmt(float(pa)), fmt(float(pba)), fmt(float(pbn))), dec(pb), "Total probability.", tol=0.0006)
    return nat(r, "A test detects a condition with probability %s when present and gives a false alarm with probability %s when absent. The condition affects %s of the population. "
                  "If a test is positive, what is the probability the condition is present? (up to 4 decimals)" % (fmt(float(pba)), fmt(float(pbn)), fmt(float(pa))), dec(post), "Bayes: P(A)P(B|A) / P(B) = %.4f." % post, tol=0.0006)


@gen(S, PROB, "Independence", n=45, diff="easy")
def pr_ind(r):
    a, b = F(r.randint(1, 9), 10), F(r.randint(1, 9), 10)
    kind = r.choice(["and", "or", "cond", "dep"])
    if kind == "and": return nat(r, "A and B are independent with P(A) = %s and P(B) = %s. Find P(A ∩ B)." % (fmt(float(a)), fmt(float(b))), float(a * b), "P(A)P(B).", tol=0.0005)
    if kind == "or": return nat(r, "A and B are independent with P(A) = %s and P(B) = %s. Find P(A ∪ B)." % (fmt(float(a)), fmt(float(b))), float(a + b - a * b), "P(A)+P(B)−P(A)P(B).", tol=0.0005)
    if kind == "cond":
        i = F(r.randint(1, 4), 10)
        p = F(r.randint(5, 9), 10)
        return nat(r, "P(A) = %s and P(A ∩ B) = %s. Find P(B | A)." % (fmt(float(p)), fmt(float(i))), float(i / p), "P(A∩B)/P(A).", tol=0.001)
    return nat(r, "P(A) = %s, P(B) = %s and A, B are mutually exclusive. Find P(A ∪ B)." % (fmt(float(a / 2)), fmt(float(b / 2))), float(a / 2 + b / 2), "Add the probabilities.", tol=0.0005)


# =============== RANDOM VARIABLES ===============
@gen(S, RV, "Expectation & variance", n=90, diff="medium")
def rv_ev(r):
    kind = r.choice(["die", "binE", "binV", "geo", "lin", "linvar", "unif", "poisson", "exp", "twoE", "indic"])
    if kind == "die": return nat(r, "Expected value of the maximum of two fair dice? (up to 4 decimals)" if False else "Expected value of the square of the number shown by a fair die? (up to 4 decimals)", dec(F(91, 6)), "(1+4+9+16+25+36)/6.", tol=0.001)
    if kind == "binE":
        n, p = r.randint(5, 40), r.choice([F(1, 4), F(1, 2), F(1, 5), F(3, 10)])
        return nat(r, "X ~ Binomial(n = %d, p = %s). Find E[X]." % (n, ratstr(p)), dec(n * p), "np.", tol=0.001)
    if kind == "binV":
        n, p = r.randint(5, 40), r.choice([F(1, 4), F(1, 2), F(1, 5), F(3, 10)])
        return nat(r, "X ~ Binomial(n = %d, p = %s). Find Var(X)." % (n, ratstr(p)), dec(n * p * (1 - p)), "np(1−p).", tol=0.001)
    if kind == "geo":
        p = r.choice([F(1, 2), F(1, 3), F(1, 4), F(1, 5), F(1, 6), F(1, 10)])
        return nat(r, "A trial succeeds with probability %s. Expected number of trials until the first success?" % ratstr(p), dec(1 / p), "Geometric: 1/p.", tol=0.001)
    if kind == "lin":
        a, b, m = r.randint(2, 6), r.randint(-5, 9), r.randint(1, 9)
        return nat(r, "E[X] = %d. Find E[%dX %+d]." % (m, a, b), a * m + b, "Linearity of expectation.")
    if kind == "linvar":
        a, b, v = r.randint(2, 6), r.randint(-5, 9), r.randint(1, 9)
        return nat(r, "Var(X) = %d. Find Var(%dX %+d)." % (v, a, b), a * a * v, "Var(aX + b) = a²Var(X).")
    if kind == "unif":
        a, b = r.randint(0, 5), r.randint(6, 20)
        return nat(r, "X is uniformly distributed on [%d, %d]. Find Var(X). (up to 3 decimals)" % (a, b), dec(F((b - a) ** 2, 12), 3), "(b−a)²/12.", tol=0.002)
    if kind == "poisson":
        l = r.randint(2, 9)
        return nat(r, "X ~ Poisson(λ = %d). Find E[X²]." % l, l * l + l, "Var + mean² = λ + λ².")
    if kind == "exp":
        l = r.choice([2, 4, 5, 10])
        return nat(r, "X is exponential with rate λ = %d. Find E[X]. (up to 3 decimals)" % l, dec(F(1, l), 3), "1/λ.", tol=0.001)
    if kind == "twoE":
        k = r.randint(2, 6)
        return nat(r, "%d fair dice are rolled. Expected value of the sum of the numbers? (up to 2 decimals)" % k, k * 3.5, "k × 3.5.", tol=0.01)
    n = r.randint(5, 20)
    return nat(r, "%d people each put their hat in a box and each takes one hat at random. Expected number of people who get their own hat?" % n, 1, "Sum of n indicators, each with probability 1/n ⇒ 1.")


@gen(S, RV, "Distributions", n=60, diff="hard", marks=2)
def rv_dist(r):
    kind = r.choice(["binP", "poisP", "geoP", "normal", "hh", "memless", "coupon"])
    if kind == "binP":
        n, k = r.randint(4, 8), r.randint(1, 3)
        p = F(1, r.choice([2, 3, 4]))
        v = C_(n, k) * p ** k * (1 - p) ** (n - k)
        return nat(r, "X ~ Binomial(n = %d, p = %s). Find P(X = %d). (up to 4 decimals)" % (n, ratstr(p), k), dec(v), "C(n,k)p^k(1−p)^(n−k).", tol=0.0006)
    if kind == "poisP":
        l, k = r.randint(1, 4), r.randint(0, 3)
        v = math.exp(-l) * l ** k / math.factorial(k)
        return nat(r, "X ~ Poisson(λ = %d). Find P(X = %d). (up to 4 decimals)" % (l, k), dec(v), "e^{−λ}λ^k/k!.", tol=0.0006)
    if kind == "geoP":
        p, k = F(1, r.choice([2, 3, 4, 5])), r.randint(2, 5)
        return nat(r, "A trial succeeds with probability %s. Probability that the first success occurs exactly on trial %d? (up to 4 decimals)" % (ratstr(p), k), dec((1 - p) ** (k - 1) * p), "(1−p)^{k−1}p.", tol=0.0006)
    if kind == "normal":
        m, s = r.randint(10, 100), r.randint(2, 10)
        return mcq(r, "X ~ N(μ = %d, σ = %d). Approximately what fraction of observations lie within [%d, %d]?" % (m, s, m - 2 * s, m + 2 * s), "95%", ["68%", "99.7%", "50%"], "Empirical rule: ±2σ ≈ 95%.")
    if kind == "hh":
        k = r.randint(2, 4)
        return nat(r, "A fair coin is tossed repeatedly. Expected number of tosses until %d consecutive heads first appear?" % k, 2 ** (k + 1) - 2, "E_k = 2^{k+1} − 2.")
    if kind == "memless":
        l = r.choice([1, 2, 3])
        return mcq(r, "An exponential random variable X satisfies P(X > s + t | X > s) =", "P(X > t)", ["P(X > s)·P(X > t)·2", "P(X > s + t)/2", "1 − P(X > t)"], "Memorylessness.")
    n = r.randint(3, 8)
    return nat(r, "Coupon collector: expected number of draws to collect all %d distinct coupons (each draw uniformly random)? (up to 2 decimals)" % n, dec(n * sum(F(1, i) for i in range(1, n + 1)), 2), "n·H_n.", tol=0.01)
