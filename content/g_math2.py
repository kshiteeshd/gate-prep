"""ENGM: extra generators with worked explanations for the hand-written chapters (logic, sets, posets, groups, graphs, counting, calculus, probability)."""
import itertools
import math
from fractions import Fraction as F

from content.kit import *

S = "ENGM"
LOGIC, SETS, POSET, GROUP, GRAPH, COMB, LIM, INT, PROB, RV = (
    "Propositional & First-Order Logic", "Sets, Relations & Functions", "Partial Orders & Lattices", "Groups & Monoids",
    "Graph Theory", "Combinatorics & Recurrences", "Limits, Continuity & Differentiation", "Maxima, Minima & Integration",
    "Probability Basics & Bayes", "Random Variables & Distributions")


def fm(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)


def stirling2(n, k):
    return sum((-1) ** j * math.comb(k, j) * (k - j) ** n for j in range(k + 1)) // math.factorial(k)


def bell(n):
    return sum(stirling2(n, k) for k in range(n + 1))


def phi(n):
    return sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)


def divs(n):
    return [d for d in range(1, n + 1) if n % d == 0]


# ============================ LOGIC ============================
@gen(S, LOGIC, "Logical forms", n=60, diff="easy")
def lg_forms(r):
    kind = r.choice(["contra", "conv", "rows", "taut", "neg", "xor", "implcount"])
    p, q = r.choice([("it rains", "the match is cancelled"), ("x is even", "x² is even"), ("n is prime", "n is odd or n = 2"), ("a student studies", "the student passes")])
    if kind == "contra":
        return mcq(r, "The contrapositive of \"if %s then %s\" is" % (p, q), "if not (%s) then not (%s)" % (q, p),
                   ["if %s then not (%s)" % (q, p), "if %s then %s" % (q, p), "if not (%s) then not (%s)" % (p, q)],
                   "The contrapositive of P → Q is ¬Q → ¬P and is always logically equivalent to P → Q. The converse (Q → P) and the inverse (¬P → ¬Q) are equivalent to each other but NOT to the original.")
    if kind == "conv":
        return mcq(r, "The converse of \"if %s then %s\" is" % (p, q), "if %s then %s" % (q, p), ["if not (%s) then not (%s)" % (q, p), "if not (%s) then not (%s)" % (p, q), "%s and %s" % (p, q)],
                   "The converse swaps the two parts: Q → P.")
    if kind == "rows":
        n = r.randint(3, 7)
        return nat(r, "A formula has %d distinct propositional variables. How many rows does its truth table have?" % n, 2 ** n, "Each variable is true or false independently: 2^%d = %d rows." % (n, 2 ** n))
    if kind == "taut":
        n = r.randint(2, 4)
        return nat(r, "How many different Boolean functions of %d variables exist?" % n, 2 ** (2 ** n),
                   "A function assigns 0 or 1 to each of the 2^%d = %d input rows, so there are 2^%d = %d functions." % (n, 2 ** n, 2 ** n, 2 ** (2 ** n)))
    if kind == "neg":
        return mcq(r, "The negation of P → Q is equivalent to", "P ∧ ¬Q", ["¬P → ¬Q", "¬P ∧ Q", "¬P ∨ Q"],
                   "P → Q ≡ ¬P ∨ Q. By De Morgan, ¬(¬P ∨ Q) ≡ P ∧ ¬Q. The implication fails exactly when P is true and Q false.")
    if kind == "xor":
        n = r.randint(3, 6)
        return nat(r, "Of the 2^%d rows of the truth table of p₁ ⊕ p₂ ⊕ … ⊕ p%d (exclusive or), in how many is the formula true?" % (n, n), 2 ** (n - 1),
                   "XOR of n variables is true when an odd number of them are true. Exactly half of the 2^%d assignments have odd parity: 2^%d = %d." % (n, n - 1, 2 ** (n - 1)))
    n = r.randint(2, 5)
    return nat(r, "How many of the %d truth assignments of p₁ … p%d make the implication (p₁ ∧ p₂ ∧ … ∧ p%d) → q false when q is FALSE?" % (2 ** n, n, n), 1,
               "An implication is false only if its antecedent is true and consequent false. With q false we need p₁ ∧ … ∧ p%d true: exactly one assignment (all true)." % n)


@gen(S, LOGIC, "FOL translation", n=70, diff="medium", marks=2)
def lg_fol(r):
    A = ["student", "person", "bird", "number", "program"]
    B = ["course", "friend", "nest", "factor", "bug"]
    a, b = r.choice(list(zip(A, B)))
    R = "R(x, y)"
    templates = [
        ("Every %s has some %s (related by R)." % (a, b), "∀x ∃y R(x, y)", ["∃y ∀x R(x, y)", "∀x ∀y R(x, y)", "∃x ∀y R(x, y)"],
         "\"Every x has SOME y\": for each x we may pick a different y, so ∀x comes first, then ∃y. Swapping the quantifiers gives the much stronger \"one y works for all x\"."),
        ("There is one %s related to every %s." % (b, a), "∃y ∀x R(x, y)", ["∀x ∃y R(x, y)", "∀y ∃x R(x, y)", "∃x ∃y R(x, y)"],
         "A single y that works for ALL x: ∃y first, then ∀x. ∀x ∃y only says every x has its own partner."),
        ("No %s is related to every %s." % (a, b), "¬∃x ∀y R(x, y)", ["∀x ∃y R(x, y)", "∃x ∀y ¬R(x, y)", "∀x ∀y ¬R(x, y)"],
         "\"No x relates to all y\" negates ∃x ∀y R(x, y). Equivalently ∀x ∃y ¬R(x, y): every x misses at least one y."),
        ("Some %s is related to no %s." % (a, b), "∃x ∀y ¬R(x, y)", ["∀x ∃y ¬R(x, y)", "¬∃x ∃y R(x, y) is false", "∃x ∃y ¬R(x, y)"],
         "A particular x that avoids every y: ∃x ∀y ¬R(x, y)."),
    ]
    t = r.choice(templates)
    wrong = [w for w in t[2] if "is false" not in w]
    if len(wrong) < 3:
        wrong += ["∀y ∃x ¬R(x, y)"]
    return mcq(r, "Translate into first-order logic, with R(x, y) meaning \"x is related to y\": %s" % t[0], t[1], wrong[:3], t[3])


# ============================ SETS / RELATIONS / FUNCTIONS ============================
@gen(S, SETS, "Counting relations on a set", n=70, diff="medium")
def st_rel(r):
    n = r.randint(2, 6)
    kind = r.choice(["all", "refl", "sym", "irrefl", "antisym", "equiv", "refl_sym", "asym"])
    if kind == "all":
        return nat(r, "How many binary relations are there on a set with %d elements?" % n, 2 ** (n * n), "A relation is any subset of A × A, which has %d pairs: 2^%d = %d." % (n * n, n * n, 2 ** (n * n)))
    if kind == "refl":
        return nat(r, "How many reflexive relations are there on a set with %d elements?" % n, 2 ** (n * n - n), "The %d diagonal pairs are forced in; each of the other %d pairs is free: 2^%d = %d." % (n, n * n - n, n * n - n, 2 ** (n * n - n)))
    if kind == "irrefl":
        return nat(r, "How many irreflexive relations are there on a set with %d elements?" % n, 2 ** (n * n - n), "No diagonal pair is allowed and each of the other %d pairs is free: 2^%d = %d." % (n * n - n, n * n - n, 2 ** (n * n - n)))
    if kind == "sym":
        e = n * (n + 1) // 2
        return nat(r, "How many symmetric relations are there on a set with %d elements?" % n, 2 ** e, "Choose each diagonal pair freely (%d) and each unordered pair {a, b} (%d) as a unit: n(n+1)/2 = %d free choices, so 2^%d = %d." % (n, n * (n - 1) // 2, e, e, 2 ** e))
    if kind == "antisym":
        v = 2 ** n * 3 ** (n * (n - 1) // 2)
        return nat(r, "How many antisymmetric relations are there on a set with %d elements?" % n, v, "Each diagonal pair is free (2 choices each: 2^%d). For each of the %d unordered pairs {a, b} we may include (a,b), (b,a) or neither, but not both: 3 choices. Total 2^%d · 3^%d = %d." % (n, n * (n - 1) // 2, n, n * (n - 1) // 2, v))
    if kind == "asym":
        v = 3 ** (n * (n - 1) // 2)
        return nat(r, "How many asymmetric relations are there on a set with %d elements?" % n, v, "Asymmetric = irreflexive and antisymmetric: no diagonal pairs, and 3 choices (neither, (a,b) or (b,a)) for each of the %d unordered pairs: 3^%d = %d." % (n * (n - 1) // 2, n * (n - 1) // 2, v))
    if kind == "refl_sym":
        e = n * (n - 1) // 2
        return nat(r, "How many relations on a set with %d elements are both reflexive and symmetric?" % n, 2 ** e, "The diagonal is forced. Each of the %d unordered pairs {a, b} is in or out: 2^%d = %d." % (e, e, 2 ** e))
    return nat(r, "How many equivalence relations are there on a set with %d elements?" % n, bell(n),
               "Equivalence relations correspond to partitions, so the count is the Bell number B(%d) = %s = %d." % (n, " + ".join("S(%d,%d)" % (n, k) for k in range(1, n + 1)), bell(n)))


@gen(S, SETS, "Counting functions", n=70, diff="medium")
def st_fun(r):
    m, n = r.randint(2, 6), r.randint(2, 7)
    kind = r.choice(["all", "inj", "onto", "bij", "subsets", "partial", "const"])
    if kind == "all":
        return nat(r, "How many functions are there from a set of %d elements to a set of %d elements?" % (m, n), n ** m, "Each of the %d inputs independently chooses one of %d outputs: %d^%d = %d." % (m, n, n, m, n ** m))
    if kind == "inj":
        if m > n:
            m, n = n, m
        v = math.perm(n, m)
        return nat(r, "How many one-to-one (injective) functions are there from a set of %d elements to a set of %d elements?" % (m, n), v, "Choose distinct images in order: %s = P(%d, %d) = %d." % (" × ".join(str(n - i) for i in range(m)), n, m, v))
    if kind == "onto":
        if m < n:
            m, n = n, m
        v = math.factorial(n) * stirling2(m, n)
        inc = sum((-1) ** j * math.comb(n, j) * (n - j) ** m for j in range(n + 1))
        return nat(r, "How many onto (surjective) functions are there from a set of %d elements to a set of %d elements?" % (m, n), v,
                   "By inclusion–exclusion: Σ (−1)^j C(%d, j)(%d − j)^%d = %d. Equivalently %d!·S(%d, %d) = %d." % (n, n, m, inc, n, m, n, v))
    if kind == "bij":
        n = r.randint(3, 8)
        return nat(r, "How many bijections are there from a set of %d elements to itself?" % n, math.factorial(n), "A bijection of a finite set to itself is a permutation: %d! = %d." % (n, math.factorial(n)))
    if kind == "subsets":
        k = r.randint(2, 5)
        n = r.randint(6, 10)
        return nat(r, "How many subsets of a %d-element set have exactly %d elements?" % (n, k), math.comb(n, k), "C(%d, %d) = %d." % (n, k, math.comb(n, k)))
    if kind == "partial":
        return nat(r, "How many PARTIAL functions (defined on some subset of the domain) are there from a set of %d elements to a set of %d elements?" % (m, n), (n + 1) ** m,
                   "Each input is either undefined or maps to one of %d outputs: (%d + 1)^%d = %d." % (n, n, m, (n + 1) ** m))
    return nat(r, "How many constant functions are there from a set of %d elements to a set of %d elements?" % (m, n), n, "A constant function is fixed by its single output value: %d choices." % n)


# ============================ POSETS ============================
@gen(S, POSET, "Divisor poset facts", n=60, diff="medium")
def po_div(r):
    n = r.choice([12, 18, 20, 24, 30, 36, 42, 48, 60, 72, 90, 120])
    ds = divs(n)
    kind = r.choice(["size", "height", "width", "atoms", "complement", "chains"])
    pr = [p for p in range(2, n + 1) if n % p == 0 and all(p % q for q in range(2, p))]
    if kind == "size":
        return nat(r, "How many elements does the divisor lattice (D_%d, |) have?" % n, len(ds), "The elements are the divisors of %d: %s. That is %d of them." % (n, ", ".join(map(str, ds)), len(ds)))
    if kind == "height":
        e = 0
        m = n
        for p in pr:
            while m % p == 0:
                m //= p
                e += 1
        return nat(r, "What is the length (number of edges) of a longest chain from 1 to %d in the divisor lattice D_%d?" % (n, n), e,
                   "Each step multiplies by one prime. The number of prime factors of %d with multiplicity is %d, so the longest chain from 1 to %d has %d edges." % (n, e, n, e))
    if kind == "width":
        w = 0
        for mask in range(1 << len(ds)):
            sub = [ds[i] for i in range(len(ds)) if mask >> i & 1]
            if len(sub) > w and all(a % b and b % a for a, b in itertools.combinations(sub, 2)):
                w = len(sub)
        return nat(r, "What is the size of the largest antichain in (D_%d, |)?" % n, w, "An antichain is a set of divisors none of which divides another. Checking the possibilities gives a maximum of %d (for example %s)." % (w, "a middle level of the lattice"))
    if kind == "atoms":
        return nat(r, "How many atoms (elements covering the bottom 1) does the divisor lattice D_%d have?" % n, len(pr), "The atoms are the primes dividing %d: %s, so %d of them." % (n, ", ".join(map(str, pr)), len(pr)))
    if kind == "complement":
        sf = all(n % (p * p) for p in pr)
        return mcq(r, "Is the divisor lattice (D_%d, |) a complemented (Boolean) lattice?" % n, "Yes" if sf else "No", ["Yes" if not sf else "No", "Only when n is prime", "Only when n is even"],
                   "D_n is Boolean exactly when n is square-free (no prime repeated). %d = %s is %s." % (n, " · ".join(str(p) for p in pr) if sf else "not square-free", "square-free" if sf else "not square-free, so some element has no complement"))
    e = len([1 for a in ds for b in ds if a != b and b % a == 0 and not any(c not in (a, b) and c % a == 0 and b % c == 0 for c in ds)])
    return nat(r, "How many edges does the Hasse diagram of (D_%d, |) have?" % n, e, "An edge joins a to b when b/a is a prime. Counting such pairs among the divisors %s gives %d." % (", ".join(map(str, ds)), e))


# ============================ GROUPS ============================
@gen(S, GROUP, "Cyclic and permutation groups", n=70, diff="medium")
def gp_facts(r):
    n = r.choice([6, 8, 9, 10, 12, 14, 15, 18, 20, 24, 30, 36])
    kind = r.choice(["gens", "order", "subs", "cyc", "lagr", "abelian", "elts_ord"])
    if kind == "gens":
        return nat(r, "How many generators does the cyclic group Z_%d (addition mod %d) have?" % (n, n), phi(n), "The generators are the residues coprime to %d: %s. That is φ(%d) = %d." % (n, ", ".join(str(k) for k in range(1, n) if math.gcd(k, n) == 1), n, phi(n)))
    if kind == "order":
        a = r.randint(1, n - 1)
        g = math.gcd(a, n)
        return nat(r, "What is the order of the element %d in the group Z_%d under addition modulo %d?" % (a, n, n), n // g, "The order of a in Z_n is n / gcd(a, n) = %d / %d = %d." % (n, g, n // g))
    if kind == "subs":
        return nat(r, "How many subgroups does the cyclic group Z_%d have?" % n, len(divs(n)), "A cyclic group has exactly one subgroup for each divisor of its order. The divisors of %d are %s: %d subgroups." % (n, ", ".join(map(str, divs(n))), len(divs(n))))
    if kind == "cyc":
        cyc = [r.randint(2, 6) for _ in range(r.randint(2, 3))]
        o = 1
        for c in cyc:
            o = o * c // math.gcd(o, c)
        return nat(r, "A permutation is a product of disjoint cycles of lengths %s. What is its order?" % ", ".join(map(str, cyc)), o, "The order is the lcm of the cycle lengths: lcm(%s) = %d." % (", ".join(map(str, cyc)), o))
    if kind == "lagr":
        k = r.choice(divs(n))
        return mcq(r, "A group has order %d. Which of the following CANNOT be the order of a subgroup?" % n, str(next(x for x in range(2, n) if n % x)), [str(d) for d in divs(n) if d > 1][:5],
                   "By Lagrange's theorem the order of a subgroup divides the order of the group. The divisors of %d are %s; the number %d does not divide %d." % (n, ", ".join(map(str, divs(n))), next(x for x in range(2, n) if n % x), n))
    if kind == "abelian":
        p = r.choice([3, 5, 7, 11])
        return mcq(r, "A group has order %d (a prime). Which statement is true?" % p, "It is cyclic and abelian", ["It may be non-abelian", "It has a proper non-trivial subgroup", "It has more than one identity"],
                   "Pick any non-identity element: its order divides %d and is not 1, so it equals %d, and the element generates the whole group. Hence the group is cyclic, therefore abelian, and has no proper non-trivial subgroup." % (p, p))
    return nat(r, "How many elements of order %d are there in the cyclic group Z_%d?" % (n // 1 if False else r.choice(divs(n)), n) if False else "How many elements of Z_%d have order exactly %d?" % (n, divs(n)[len(divs(n)) // 2]), phi(divs(n)[len(divs(n)) // 2]),
               "In a cyclic group of order n, for each divisor d of n there are exactly φ(d) elements of order d. Here d = %d, so φ(%d) = %d." % (divs(n)[len(divs(n)) // 2], divs(n)[len(divs(n)) // 2], phi(divs(n)[len(divs(n)) // 2])))


# ============================ GRAPH THEORY ============================
@gen(S, GRAPH, "Graph identities", n=80, diff="easy")
def gr_ident(r):
    kind = r.choice(["hand", "edges_k", "tree", "planar", "euler", "bip", "span", "bipmax", "deg", "forest"])
    n = r.randint(5, 14)
    if kind == "hand":
        degs = [r.randint(1, 5) for _ in range(n - 1)]
        s = sum(degs)
        last = r.randint(1, 5)
        if (s + last) % 2:
            last += 1
        return nat(r, "A graph with %d vertices has degrees %s and one more vertex of degree %d. How many edges does it have?" % (n, ", ".join(map(str, degs)), last), (s + last) // 2,
                   "Handshake lemma: the sum of degrees is twice the number of edges. Sum = %d + %d = %d, so edges = %d." % (s, last, s + last, (s + last) // 2))
    if kind == "edges_k":
        return nat(r, "How many edges does the complete graph K%d have?" % n, n * (n - 1) // 2, "Every pair of vertices is joined: C(%d, 2) = %d." % (n, n * (n - 1) // 2))
    if kind == "tree":
        return nat(r, "A tree has %d vertices. How many edges does it have?" % n, n - 1, "A tree is connected and acyclic; n vertices need exactly n − 1 edges.")
    if kind == "forest":
        c = r.randint(2, 4)
        return nat(r, "A forest has %d vertices and %d components (trees). How many edges does it have?" % (n + c, c), n, "Each tree on k vertices has k − 1 edges, so the forest has (vertices − components) = %d − %d = %d edges." % (n + c, c, n))
    if kind == "planar":
        return nat(r, "What is the maximum number of edges of a simple connected planar graph with %d vertices (n ≥ 3)?" % n, 3 * n - 6, "Euler's formula gives e ≤ 3n − 6 for simple planar graphs: 3·%d − 6 = %d." % (n, 3 * n - 6))
    if kind == "euler":
        e = r.randint(n, 2 * n)
        return nat(r, "A connected planar graph has %d vertices and %d edges. How many faces (including the outer face) does any planar drawing have?" % (n, e), e - n + 2, "Euler's formula V − E + F = 2, so F = 2 − V + E = 2 − %d + %d = %d." % (n, e, e - n + 2))
    if kind == "bip":
        a, b = r.randint(2, 7), r.randint(2, 7)
        return nat(r, "How many edges does the complete bipartite graph K_{%d,%d} have?" % (a, b), a * b, "Each of the %d vertices on one side is joined to each of the %d on the other: %d·%d = %d." % (a, b, a, b, a * b))
    if kind == "span":
        k = r.randint(3, 7)
        return nat(r, "By Cayley's formula, how many labelled spanning trees does K%d have?" % k, k ** (k - 2), "Cayley: n^(n−2) labelled trees on n vertices: %d^%d = %d." % (k, k - 2, k ** (k - 2)))
    if kind == "bipmax":
        return nat(r, "What is the maximum number of edges of a simple bipartite graph on %d vertices?" % (2 * (n // 2) + 0 if False else n), (n // 2) * (n - n // 2),
                   "The best split is as even as possible: ⌊%d/2⌋·⌈%d/2⌉ = %d·%d = %d." % (n, n, n // 2, n - n // 2, (n // 2) * (n - n // 2)))
    d = r.randint(3, 6)
    return nat(r, "A %d-regular graph has %d vertices (%d·%d is even). How many edges does it have?" % (d, 2 * n, d, 2 * n), d * n, "Sum of degrees = %d·%d = %d, so edges = %d." % (d, 2 * n, 2 * n * d, d * n))


# ============================ COMBINATORICS ============================
@gen(S, COMB, "Counting techniques", n=80, diff="medium")
def cb_tech(r):
    kind = r.choice(["stars", "circ", "word", "derange", "nonneg", "pos", "committee", "digits", "bound"])
    if kind == "stars":
        n, k = r.randint(8, 20), r.randint(3, 5)
        return nat(r, "How many non-negative integer solutions does x₁ + … + x%d = %d have?" % (k, n), math.comb(n + k - 1, k - 1), "Stars and bars: C(n + k − 1, k − 1) = C(%d, %d) = %d." % (n + k - 1, k - 1, math.comb(n + k - 1, k - 1)))
    if kind == "pos":
        n, k = r.randint(8, 20), r.randint(3, 5)
        return nat(r, "How many solutions in POSITIVE integers does x₁ + … + x%d = %d have?" % (k, n), math.comb(n - 1, k - 1), "Put y = x − 1 ≥ 0: the sum becomes %d − %d = %d. Stars and bars: C(%d, %d) = %d." % (n, k, n - k, n - 1, k - 1, math.comb(n - 1, k - 1)))
    if kind == "bound":
        k = 3
        n = r.randint(10, 14)
        m = r.randint(4, 6)
        cnt = sum(1 for a in range(n + 1) for b in range(n + 1 - a) if n - a - b <= n and a >= m and b >= 0 and n - a - b >= 0)
        # x1 >= m, others >= 0
        v = math.comb(n - m + k - 1, k - 1)
        return nat(r, "How many non-negative integer solutions does x + y + z = %d have with x ≥ %d?" % (n, m), v, "Substitute x = x′ + %d with x′ ≥ 0: x′ + y + z = %d, giving C(%d, 2) = %d." % (m, n - m, n - m + 2, v))
    if kind == "circ":
        n = r.randint(4, 9)
        return nat(r, "In how many ways can %d people sit around a circular table (rotations are the same arrangement)?" % n, math.factorial(n - 1), "Fix one person to remove rotations, then arrange the rest: (n − 1)! = %d! = %d." % (n - 1, math.factorial(n - 1)))
    if kind == "word":
        w = r.choice(["MISSISSIPPI", "BANANA", "ENGINEER", "COMMITTEE", "ALGORITHM", "STATISTICS"])
        from collections import Counter
        c = Counter(w)
        v = math.factorial(len(w))
        for x in c.values():
            v //= math.factorial(x)
        return nat(r, "How many distinct arrangements of the letters of %s are there?" % w, v, "%d! divided by the factorial of each repeated letter count (%s): %d." % (len(w), ", ".join("%s×%d" % (k, x) for k, x in c.items() if x > 1) or "none", v))
    if kind == "derange":
        n = r.randint(3, 8)
        d = round(math.factorial(n) / math.e)
        return nat(r, "How many derangements (no element in its original position) are there of %d objects?" % n, d, "D(n) = n!·Σ(−1)^k/k! ≈ n!/e rounded: D(%d) = %d. (Recurrence D(n) = (n−1)(D(n−1) + D(n−2)).)" % (n, d))
    if kind == "nonneg":
        n = r.randint(6, 10)
        return nat(r, "How many different 4-letter strings over the alphabet of %d letters have no repeated letter?" % n, math.perm(n, 4), "P(%d, 4) = %s = %d." % (n, " × ".join(str(n - i) for i in range(4)), math.perm(n, 4)))
    if kind == "committee":
        a, b = r.randint(4, 8), r.randint(4, 8)
        i, j = r.randint(2, 3), r.randint(2, 3)
        return nat(r, "A committee of %d men and %d women is chosen from %d men and %d women. How many committees are possible?" % (i, j, a, b), math.comb(a, i) * math.comb(b, j), "Choose the men and women independently: C(%d, %d)·C(%d, %d) = %d·%d = %d." % (a, i, b, j, math.comb(a, i), math.comb(b, j), math.comb(a, i) * math.comb(b, j)))
    d = r.randint(3, 5)
    return nat(r, "How many %d-digit numbers (first digit non-zero) have all digits different?" % d, 9 * math.perm(9, d - 1), "First digit: 9 choices (1–9). Each later digit: one fewer each time from the remaining 9, 8, … : 9 × P(9, %d) = %d." % (d - 1, 9 * math.perm(9, d - 1)))


# ============================ CALCULUS ============================
@gen(S, LIM, "Limits by technique", n=70, diff="medium")
def ca_lim(r):
    kind = r.choice(["lhop", "lhop2", "series", "ratio", "taylor", "sandwich"])
    a = r.randint(2, 5)
    if kind == "lhop":
        return nat(r, "Evaluate lim (x→0) (e^{%dx} − 1 − %dx) / x²." % (a, a), F(a * a, 2), "Both numerator and denominator → 0. L'Hôpital: (a·e^{ax} − a)/(2x) → still 0/0; again: a²e^{ax}/2 → a²/2 = %s." % fm(F(a * a, 2)))
    if kind == "lhop2":
        return nat(r, "Evaluate 6 × lim (x→0) (x − sin x) / x³.", 1, "Taylor: sin x = x − x³/6 + …, so x − sin x ≈ x³/6 and the limit is 1/6. Times 6 gives 1.")
    if kind == "series":
        return mcq(r, "The p-series Σ 1/n^p (n = 1, 2, 3, …) converges exactly when", "p > 1", ["p ≥ 1", "p < 1", "p > 0"],
                   "Compare with the integral ∫ dx/x^p, which converges iff p > 1. At p = 1 the harmonic series diverges, so p ≥ 1 is wrong.")
    if kind == "ratio":
        c = r.randint(2, 6)
        return mcq(r, "Does the series Σ n!/%d^n converge or diverge?" % c, "diverges", ["converges", "converges only for c > 10", "cannot be decided"],
                   "Ratio test: a_{n+1}/a_n = (n + 1)/%d → ∞ > 1, so the series diverges. (Factorials beat any exponential.)" % c)
    if kind == "taylor":
        n = r.randint(3, 6)
        return nat(r, "The coefficient of x^%d in the Maclaurin series of e^x is 1/%d!. What is %d!?" % (n, n, n), math.factorial(n), "%d! = %d." % (n, math.factorial(n)))
    return nat(r, "Evaluate lim (x→∞) (%dx + sin x) / x." % a, a, "sin x is bounded by −1 and 1, so (sin x)/x → 0 (squeeze theorem) and the limit is %d." % a)


@gen(S, INT, "Optimisation on an interval", n=70, diff="medium")
def ca_opt(r):
    p, q = r.sample(range(-3, 5), 2)
    if p == q:
        raise Skip()
    lo, hi = min(p, q), max(p, q)
    f = lambda x: F(x ** 3, 3) - F(p + q, 2) * x * x + p * q * x
    a, b = lo - 1, hi + 1
    vals = {x: f(x) for x in sorted({a, b, lo, hi})}
    kind = r.choice(["max", "min", "second", "area"])
    ws = "; ".join("f(%d) = %s" % (x, fm(v)) for x, v in vals.items())
    base = "f′(x) = (x − %d)(x − %d), so the critical points are x = %d and x = %d. Compare f at the critical points and the endpoints: %s." % (p, q, p, q, ws)
    fx = "x³/3 − (%s)x²/2 + %d·x" % (p + q, p * q)
    if kind == "max":
        return nat(r, "Find the maximum value of f(x) = %s on the closed interval [%d, %d]. (3 decimals)" % (fx, a, b), round(float(max(vals.values())), 3), base + " The largest is %s." % fm(max(vals.values())), tol=0.002)
    if kind == "min":
        return nat(r, "Find the minimum value of f(x) = %s on the closed interval [%d, %d]. (3 decimals)" % (fx, a, b), round(float(min(vals.values())), 3), base + " The smallest is %s." % fm(min(vals.values())), tol=0.002)
    if kind == "second":
        return nat(r, "For f(x) = %s, evaluate f″ at the larger critical point." % fx, hi - lo, "f″(x) = 2x − %d. At x = %d it equals %d. Positive means a local minimum there." % (p + q, hi, 2 * hi - (p + q)) if False else "f″(x) = 2x − (%d) = 2x − %d. At x = %d this is %d, positive, so that point is a local minimum." % (p + q, p + q, hi, 2 * hi - (p + q)) if 2 * hi - (p + q) == hi - lo else "f″ at the larger critical point equals %d." % (hi - lo))
    k = r.randint(1, 4)
    n = r.randint(2, 4)
    v = F(k * 2 ** (n + 1), n + 1)
    return nat(r, "Find ∫ from 0 to 2 of %dx^%d dx. (3 decimals)" % (k, n), round(float(v), 3), "Antiderivative k·x^(n+1)/(n+1) = %dx^%d/%d evaluated at 2 minus at 0: %s." % (k, n + 1, n + 1, fm(v)), tol=0.002)


# ============================ PROBABILITY ============================
@gen(S, PROB, "Bayes with tables", n=70, diff="medium", marks=2)
def pb_bayes(r):
    kind = r.choice(["test", "urn", "total", "indep", "cond"])
    if kind == "test":
        pd, se, sp = r.choice([1, 2, 5, 10]), r.choice([90, 95, 99]), r.choice([90, 95, 98])
        pd_, se_, sp_ = F(pd, 100), F(se, 100), F(sp, 100)
        pos = pd_ * se_ + (1 - pd_) * (1 - sp_)
        post = pd_ * se_ / pos
        return nat(r, "A disease affects %d%% of people. A test is positive for %d%% of those who have it and gives a false positive for %d%% of those who do not. A person tests positive. What is the probability (3 decimals) that they have the disease?" % (pd, se, 100 - sp), round(float(post), 3),
                   "P(D) = %s, P(+|D) = %s, P(+|¬D) = %s. P(+) = P(D)P(+|D) + P(¬D)P(+|¬D) = %s·%s + %s·%s = %s. Bayes: P(D|+) = %s·%s / %s = %s ≈ %.3f." % (fm(pd_), fm(se_), fm(1 - sp_), fm(pd_), fm(se_), fm(1 - pd_), fm(1 - sp_), fm(pos), fm(pd_), fm(se_), fm(pos), fm(post), float(post)), tol=0.002)
    if kind == "urn":
        a, b, c, d = r.randint(2, 6), r.randint(2, 6), r.randint(2, 6), r.randint(2, 6)
        p1 = F(a, a + b)
        p2 = F(c, c + d)
        tot = (p1 + p2) / 2
        post = (p1 / 2) / tot
        return nat(r, "Urn 1 has %d red and %d blue balls; urn 2 has %d red and %d blue. An urn is chosen at random and a ball drawn: it is red. What is the probability (3 decimals) it came from urn 1?" % (a, b, c, d), round(float(post), 3),
                   "P(red) = ½·%s + ½·%s = %s. P(urn 1 | red) = (½·%s) / %s = %s ≈ %.3f." % (fm(p1), fm(p2), fm(tot), fm(p1), fm(tot), fm(post), float(post)), tol=0.002)
    if kind == "total":
        p, q, s = r.randint(2, 5), r.randint(2, 5), r.randint(1, 3)
        pa, pb = F(1, 2), F(1, 2)
        t = pa * F(p, 10) + pb * F(q, 10)
        return nat(r, "Machine A makes half the items and %d%% of its items are defective; machine B makes the other half with %d%% defective. What is the probability (3 decimals) a random item is defective?" % (p * 10, q * 10), round(float(t), 3),
                   "Law of total probability: P(D) = P(A)P(D|A) + P(B)P(D|B) = ½·%s + ½·%s = %s." % (fm(F(p, 10)), fm(F(q, 10)), fm(t)), tol=0.002)
    if kind == "indep":
        p, q = r.choice([(F(1, 2), F(1, 3)), (F(2, 5), F(1, 4)), (F(3, 4), F(1, 5)), (F(1, 6), F(1, 2))])
        return nat(r, "A and B are independent with P(A) = %s and P(B) = %s. Find P(A ∪ B) (3 decimals)." % (fm(p), fm(q)), round(float(p + q - p * q), 3),
                   "P(A ∪ B) = P(A) + P(B) − P(A)P(B) = %s + %s − %s = %s." % (fm(p), fm(q), fm(p * q), fm(p + q - p * q)), tol=0.002)
    pab, pb = F(r.randint(1, 3), 12), F(r.randint(4, 8), 12)
    return nat(r, "P(A ∩ B) = %s and P(B) = %s. Find P(A | B) (3 decimals)." % (fm(pab), fm(pb)), round(float(pab / pb), 3), "P(A|B) = P(A ∩ B)/P(B) = %s / %s = %s." % (fm(pab), fm(pb), fm(pab / pb)), tol=0.002)


@gen(S, RV, "Distribution formulas", n=80, diff="medium")
def pb_dist(r):
    kind = r.choice(["binmean", "binvar", "binp", "geo", "pois", "unif", "expo", "fixed", "sum"])
    n, p = r.randint(5, 12), r.choice([F(1, 2), F(1, 3), F(1, 4), F(2, 5)])
    if kind == "binmean":
        return nat(r, "X ~ Binomial(n = %d, p = %s). Find E[X]." % (n, fm(p)), float(n * p), "E[X] = np = %d·%s = %s." % (n, fm(p), fm(n * p)), tol=0.002)
    if kind == "binvar":
        return nat(r, "X ~ Binomial(n = %d, p = %s). Find Var(X)." % (n, fm(p)), round(float(n * p * (1 - p)), 3), "Var(X) = np(1 − p) = %d·%s·%s = %s." % (n, fm(p), fm(1 - p), fm(n * p * (1 - p))), tol=0.002)
    if kind == "binp":
        k = r.randint(0, 2)
        v = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
        return nat(r, "X ~ Binomial(n = %d, p = %s). Find P(X = %d). (4 decimals)" % (n, fm(p), k), round(float(v), 4), "P(X = k) = C(n, k)p^k(1 − p)^(n−k) = C(%d, %d)·%s^%d·%s^%d = %s ≈ %.4f." % (n, k, fm(p), k, fm(1 - p), n - k, fm(v), float(v)), tol=0.0006)
    if kind == "geo":
        return nat(r, "X is the number of independent trials until the first success, each with success probability %s. Find E[X]." % fm(p), float(1 / p), "Geometric: E[X] = 1/p = %s." % fm(1 / p), tol=0.002)
    if kind == "pois":
        lam = r.randint(2, 6)
        return nat(r, "X ~ Poisson(λ = %d). Find E[X²]." % lam, lam * lam + lam, "For Poisson, E[X] = Var(X) = λ, so E[X²] = Var + E² = %d + %d = %d." % (lam, lam * lam, lam * lam + lam))
    if kind == "unif":
        a, b = r.randint(0, 5), r.randint(8, 20)
        return nat(r, "X is uniform on [%d, %d]. Find Var(X). (3 decimals)" % (a, b), round((b - a) ** 2 / 12, 3), "Var = (b − a)²/12 = %d²/12 = %.3f." % (b - a, (b - a) ** 2 / 12), tol=0.002)
    if kind == "expo":
        lam = r.randint(2, 5)
        return nat(r, "X is exponential with rate λ = %d. Find E[X]. (3 decimals)" % lam, round(1 / lam, 3), "E[X] = 1/λ = 1/%d." % lam, tol=0.002)
    if kind == "fixed":
        m = r.randint(4, 12)
        return nat(r, "A random permutation of %d distinct items is chosen. What is the expected number of items left in their original position?" % m, 1,
                   "Let I_k be 1 if item k is fixed. P(I_k = 1) = 1/%d, so E[Σ I_k] = %d·(1/%d) = 1, by linearity of expectation (independence not needed)." % (m, m, m))
    a, b = r.randint(2, 9), r.randint(2, 9)
    return nat(r, "X and Y are independent with E[X] = %d, Var(X) = %d, E[Y] = %d, Var(Y) = %d. Find Var(2X − Y)." % (a, a + 1, b, b + 1), 4 * (a + 1) + (b + 1),
               "For independent variables Var(aX + bY) = a²Var(X) + b²Var(Y) = 4·%d + 1·%d = %d. Means do not enter, and the minus sign disappears when squared." % (a + 1, b + 1, 4 * (a + 1) + (b + 1)))
