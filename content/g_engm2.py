"""ENGM: generators for sub-chapters that had no question family of their own. Every explanation shows the working."""
import itertools
import math
from collections import Counter
from fractions import Fraction as F

from content.kit import *

S = "ENGM"
LOGIC, SETS, POSET, GROUP, GRAPH, COMB, MAT, LIN, LIM, INT, PROB, RV = (
    "Propositional & First-Order Logic", "Sets, Relations & Functions", "Partial Orders & Lattices", "Groups & Monoids",
    "Graph Theory", "Combinatorics & Recurrences", "Matrices & Determinants", "Linear Equations & Eigenvalues",
    "Limits, Continuity & Differentiation", "Maxima, Minima & Integration", "Probability Basics & Bayes",
    "Random Variables & Distributions")
C = math.comb


def fm(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)


def J(a, s=", "):
    return s.join(map(str, a))


# ---------------------------------------------------------------- logic: rules of inference
RULES = [
    ("P → Q, P ⊢ Q", "modus ponens", True), ("P → Q, ¬Q ⊢ ¬P", "modus tollens", True),
    ("P → Q, Q → R ⊢ P → R", "hypothetical syllogism", True), ("P ∨ Q, ¬P ⊢ Q", "disjunctive syllogism", True),
    ("P ∨ Q, ¬P ∨ R ⊢ Q ∨ R", "resolution", True), ("P ⊢ P ∨ Q", "addition", True), ("P ∧ Q ⊢ P", "simplification", True),
    ("P → Q, Q ⊢ P", "affirming the consequent", False), ("P → Q, ¬P ⊢ ¬Q", "denying the antecedent", False),
    ("P ∨ Q, P ⊢ ¬Q", "affirming a disjunct", False), ("P → Q ⊢ Q → P", "converse error", False),
]


def valid(premises, concl):
    """Brute-force validity of an argument over variables P, Q, R."""
    for P, Q, R in itertools.product((0, 1), repeat=3):
        env = dict(P=P, Q=Q, R=R)
        if all(f(env) for f in premises) and not concl(env):
            return False, (P, Q, R)
    return True, None


@gen(S, LOGIC, "Rules of inference", n=60, diff="medium")
def lg_infer(r):
    kind = r.choice(["name", "valid", "valid", "chain"])
    if kind == "name":
        f, nm, ok = r.choice([x for x in RULES if x[2]])
        return mcq(r, "The inference %s is called" % f, nm, [x[1] for x in RULES if x[1] != nm],
                   "%s is %s, one of the standard valid rules. Learn the shapes: modus ponens (P → Q, P ⊢ Q), modus tollens (P → Q, ¬Q ⊢ ¬P), hypothetical syllogism (chain two implications), disjunctive syllogism (P ∨ Q, ¬P ⊢ Q), resolution (P ∨ Q, ¬P ∨ R ⊢ Q ∨ R)." % (f, nm))
    if kind == "valid":
        f, nm, ok = r.choice(RULES)
        why = ("It is %s, a valid rule: in every row where all premises are true, the conclusion is true." % nm if ok else
               "It is the fallacy of %s. A counter-example row makes every premise true and the conclusion false, so the argument is invalid." % nm)
        return mcq(r, "Is the argument %s valid?" % f, "Valid" if ok else "Invalid", ["Invalid" if ok else "Valid", "Valid only if P is true", "Cannot be decided without a truth table"], why)
    a, b, c = r.sample(["it rains", "the ground is wet", "the match is cancelled", "the shop is closed", "the bus is late"], 3)
    return mcq(r, "Premises: (1) if %s then %s; (2) if %s then %s; (3) %s is false. Which conclusion follows?" % (a, b, b, c, c),
               "%s is false" % a, ["%s is true" % a, "%s is true" % b, "nothing can be concluded"],
               "Chain (1) and (2) by hypothetical syllogism: if %s then %s. With (3), modus tollens gives: %s is false." % (a, c, a))


# ---------------------------------------------------------------- sets
@gen(S, SETS, "Set operations", n=70, diff="easy")
def st_ops(r):
    kind = r.choice(["union", "inter", "diff", "sym", "prod", "power", "powinter", "subsetk"])
    U = list(range(1, 13))
    A = sorted(r.sample(U, r.randint(4, 7)))
    B = sorted(r.sample(U, r.randint(4, 7)))
    sA, sB = set(A), set(B)
    show = "A = {%s}, B = {%s}" % (J(A), J(B))
    if kind == "union":
        return nat(r, "%s. Find |A ∪ B|." % show, len(sA | sB), "A ∪ B = {%s}. Check: |A| + |B| − |A ∩ B| = %d + %d − %d = %d." % (J(sorted(sA | sB)), len(sA), len(sB), len(sA & sB), len(sA | sB)))
    if kind == "inter":
        return nat(r, "%s. Find |A ∩ B|." % show, len(sA & sB), "Common elements: {%s}, so %d." % (J(sorted(sA & sB)) or "", len(sA & sB)))
    if kind == "diff":
        return nat(r, "%s. Find |A − B|." % show, len(sA - sB), "A − B keeps the elements of A not in B: {%s}, so %d. (|A − B| = |A| − |A ∩ B| = %d − %d.)" % (J(sorted(sA - sB)), len(sA - sB), len(sA), len(sA & sB)))
    if kind == "sym":
        return nat(r, "%s. Find |A Δ B| (symmetric difference)." % show, len(sA ^ sB), "A Δ B = (A − B) ∪ (B − A) = {%s}: %d elements = |A| + |B| − 2|A ∩ B| = %d + %d − 2·%d." % (J(sorted(sA ^ sB)), len(sA ^ sB), len(sA), len(sB), len(sA & sB)))
    if kind == "prod":
        m, n = r.randint(2, 7), r.randint(2, 7)
        return nat(r, "|A| = %d and |B| = %d. How many elements does A × B have?" % (m, n), m * n, "A × B is the set of ordered pairs (a, b): %d·%d = %d." % (m, n, m * n))
    if kind == "power":
        n = r.randint(3, 9)
        return nat(r, "A set has %d elements. How many elements does its power set have?" % n, 2 ** n, "Each element is in or out of a subset: 2^%d = %d." % (n, 2 ** n))
    if kind == "powinter":
        m, n, k = r.randint(4, 7), r.randint(4, 7), r.randint(1, 3)
        return nat(r, "|A| = %d, |B| = %d and |A ∩ B| = %d. How many elements does P(A) ∩ P(B) have?" % (m, n, k), 2 ** k,
                   "A set lies in both power sets iff it is a subset of A ∩ B, so P(A) ∩ P(B) = P(A ∩ B) with 2^%d = %d elements." % (k, 2 ** k))
    n, k = r.randint(5, 10), r.randint(2, 4)
    return nat(r, "How many subsets of a %d-element set contain a fixed element x and have exactly %d elements?" % (n, k), C(n - 1, k - 1),
               "x is forced in; choose the remaining %d elements from the other %d: C(%d, %d) = %d." % (k - 1, n - 1, n - 1, k - 1, C(n - 1, k - 1)))


@gen(S, SETS, "Function properties", n=70, diff="medium")
def st_fprop(r):
    kind = r.choice(["table", "real", "comp", "inv"])
    if kind == "table":
        m = r.randint(3, 5)
        n = r.choice([m - 1, m, m + 1])
        img = [r.randint(1, n) for _ in range(m)]
        inj, sur = len(set(img)) == m, len(set(img)) == n
        ans = "bijective" if inj and sur else "one-to-one but not onto" if inj else "onto but not one-to-one" if sur else "neither one-to-one nor onto"
        mp = ", ".join("%s→%d" % (chr(97 + i), v) for i, v in enumerate(img))
        return mcq(r, "f: {%s} → {%s} is given by %s. Then f is" % (J([chr(97 + i) for i in range(m)]), J(range(1, n + 1)), mp), ans,
                   [x for x in ["bijective", "one-to-one but not onto", "onto but not one-to-one", "neither one-to-one nor onto"] if x != ans],
                   "Images used: {%s}. One-to-one needs %d distinct images (%s); onto needs every one of the %d codomain elements to be hit (%s)." % (J(sorted(set(img))), m, "yes" if inj else "no, a value repeats", n, "yes" if sur else "no"))
    if kind == "real":
        f, ans, why = r.choice([
            ("f(x) = 2x + 3 on ℝ → ℝ", "bijective", "Linear with non-zero slope: strictly increasing (one-to-one) and every y has x = (y − 3)/2 (onto)."),
            ("f(x) = x² on ℝ → ℝ", "neither one-to-one nor onto", "f(−1) = f(1) breaks one-to-one; negative numbers are never hit."),
            ("f(x) = x² on [0, ∞) → [0, ∞)", "bijective", "On non-negative numbers x² is strictly increasing and every y ≥ 0 has √y."),
            ("f(x) = eˣ on ℝ → ℝ", "one-to-one but not onto", "eˣ is strictly increasing, but it never takes values ≤ 0."),
            ("f(x) = x³ − x on ℝ → ℝ", "onto but not one-to-one", "A cubic takes every real value, but f(0) = f(1) = 0."),
            ("f(n) = 2n on ℤ → ℤ", "one-to-one but not onto", "Distinct n give distinct 2n, but odd integers are never hit."),
            ("f(n) = ⌊n/2⌋ on ℤ → ℤ", "onto but not one-to-one", "Every m is ⌊2m/2⌋, but f(0) = f(1) = 0.")])
        return mcq(r, "The function %s is" % f, ans, [x for x in ["bijective", "one-to-one but not onto", "onto but not one-to-one", "neither one-to-one nor onto"] if x != ans], why)
    if kind == "comp":
        a, b, c, d = r.randint(1, 5), r.randint(-4, 6), r.randint(1, 5), r.randint(-4, 6)
        x = r.randint(-3, 4)
        return nat(r, "f(x) = %dx %+d and g(x) = %dx %+d. Find (g∘f)(%d)." % (a, b, c, d, x), c * (a * x + b) + d,
                   "(g∘f)(x) = g(f(x)): first f(%d) = %d, then g(%d) = %d. Composition applies the RIGHT function first." % (x, a * x + b, a * x + b, c * (a * x + b) + d))
    a, b = r.choice([2, 3, 4, 5]), r.randint(-6, 6)
    y = r.randint(-5, 9)
    v = F(y - b, a)
    return nat(r, "f(x) = %dx %+d is a bijection on ℝ. Find f⁻¹(%d) (2 decimals)." % (a, b, y), round(float(v), 2),
               "Solve y = %dx %+d for x: x = (y %+d)/%d. At y = %d: %s." % (a, b, -b, a, y, fm(v)), tol=0.01)


# ---------------------------------------------------------------- posets
def divs(n):
    return [d for d in range(1, n + 1) if n % d == 0]


@gen(S, POSET, "Extremal elements", n=70, diff="medium")
def po_ext(r):
    base = r.sample([2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36], r.randint(5, 7))
    X = sorted(base)
    mins = [a for a in X if not any(b != a and a % b == 0 for b in X)]
    maxs = [a for a in X if not any(b != a and b % a == 0 for b in X)]
    kind = r.choice(["min", "max", "least", "greatest", "ub"])
    s = "({%s}, |) ordered by divisibility" % J(X)
    if kind == "min":
        return nat(r, "How many minimal elements does the poset %s have?" % s, len(mins), "A minimal element has nothing below it, i.e. no other element of the set divides it: %s." % J(mins))
    if kind == "max":
        return nat(r, "How many maximal elements does the poset %s have?" % s, len(maxs), "A maximal element divides no other element of the set: %s." % J(maxs))
    if kind == "least":
        ans = "yes, " + str(mins[0]) if len(mins) == 1 and all(x % mins[0] == 0 for x in X) else "no least element"
        return mcq(r, "Does the poset %s have a least element?" % s, ans, ["yes, " + str(X[0]) if ans == "no least element" else "no least element", "yes, 1", "yes, " + str(X[-1])],
                   "A least element must divide every element. The minimal elements are %s; %s" % (J(mins), "exactly one, and it divides everything." if ans != "no least element" else "there is more than one, so none is least."))
    if kind == "greatest":
        ans = "yes, " + str(maxs[0]) if len(maxs) == 1 and all(maxs[0] % x == 0 for x in X) else "no greatest element"
        return mcq(r, "Does the poset %s have a greatest element?" % s, ans, ["yes, " + str(X[-1]) if ans == "no greatest element" else "no greatest element", "yes, " + str(X[0]), "yes, the lcm of all elements"],
                   "A greatest element must be divisible by every element. The maximal elements are %s; %s" % (J(maxs), "exactly one, divisible by everything." if ans != "no greatest element" else "there is more than one, so none is greatest."))
    a, b = r.sample(X, 2)
    ubs = [x for x in X if x % a == 0 and x % b == 0]
    return nat(r, "In the poset %s, how many upper bounds do %d and %d have inside the set?" % (s, a, b), len(ubs),
               "An upper bound must be a multiple of both %d and %d (a multiple of lcm = %d) that lies in the set: %s." % (a, b, a * b // math.gcd(a, b), J(ubs) if ubs else "none"))


@gen(S, POSET, "Boolean lattices", n=60, diff="medium")
def po_bool(r):
    kind = r.choice(["size", "atoms", "compl", "dn", "sqfree", "count"])
    if kind == "size":
        k = r.randint(2, 6)
        return nat(r, "A Boolean lattice has %d atoms. How many elements does it have?" % k, 2 ** k, "A finite Boolean lattice with k atoms is isomorphic to the power set of a k-set: 2^%d = %d elements." % (k, 2 ** k))
    if kind == "atoms":
        n = r.choice([8, 16, 32, 64, 128])
        k = int(math.log2(n))
        return nat(r, "A Boolean lattice has %d elements. How many atoms does it have?" % n, k, "2^k = %d gives k = %d atoms (the singletons of the underlying set)." % (n, k))
    if kind == "compl":
        n = r.choice([30, 42, 66, 70, 105, 110])
        a = r.choice([d for d in divs(n) if 1 < d < n])
        return nat(r, "In the Boolean lattice (D_%d, |), what is the complement of %d?" % (n, a), n // a,
                   "%d is square-free, so complements exist: the complement of a is n/a, since gcd(a, n/a) = 1 (meet = bottom) and lcm(a, n/a) = n (join = top). Here %d/%d = %d." % (n, n, a, n // a))
    if kind == "dn":
        n = r.choice([12, 18, 20, 24, 28, 36, 40, 45, 50, 54])
        bad = [d for d in divs(n) if not any(math.gcd(d, e) == 1 and d * e // math.gcd(d, e) == n for e in divs(n))]
        return nat(r, "In the divisor lattice (D_%d, |), how many elements have NO complement?" % n, len(bad),
                   "The complement of d must satisfy gcd(d, e) = 1 and lcm(d, e) = %d. That is possible only when d and n/d share no prime. Elements without one: %s." % (n, J(bad)))
    if kind == "sqfree":
        n = r.choice([6, 10, 12, 15, 18, 21, 30, 36, 42, 45, 70, 72])
        sf = all(n % (p * p) for p in range(2, n + 1) if all(p % q for q in range(2, p)))
        return mcq(r, "Is (D_%d, |) a Boolean algebra?" % n, "Yes" if sf else "No", ["No" if sf else "Yes", "Only if %d is even" % n, "Only if %d is prime" % n],
                   "D_n is Boolean iff n is square-free (no squared prime factor). %d %s." % (n, "is square-free" if sf else "has a squared prime factor"))
    k = r.randint(2, 5)
    return mcq(r, "Which of these is NOT possible as the number of elements of a finite Boolean algebra?", str(2 ** k + 2), [str(2 ** k), str(2 ** (k + 1)), str(2 ** (k - 1))],
               "Every finite Boolean algebra has 2ⁿ elements. %d is not a power of 2." % (2 ** k + 2))


# ---------------------------------------------------------------- groups: permutations
def cycles(p):
    seen, out = set(), []
    for i in range(len(p)):
        if i not in seen:
            c, j = [], i
            while j not in seen:
                seen.add(j); c.append(j); j = p[j]
            out.append(c)
    return out


@gen(S, GROUP, "Permutation cycles", n=60, diff="medium")
def gp_perm(r):
    n = r.randint(5, 8)
    p = list(range(n)); r.shuffle(p)
    cy = cycles(p)
    lens = [len(c) for c in cy]
    order = 1
    for x in lens:
        order = order * x // math.gcd(order, x)
    par = sum(x - 1 for x in lens) % 2
    two = " ".join("%d→%d" % (i + 1, p[i] + 1) for i in range(n))
    cs = "".join("(" + " ".join(str(x + 1) for x in c) + ")" for c in cy if len(c) > 1) or "identity"
    kind = r.choice(["order", "parity", "fixed", "ncyc"])
    if kind == "order":
        return nat(r, "The permutation %s on {1, …, %d}: what is its order?" % (two, n), order, "Disjoint cycles: %s. Order = lcm of the cycle lengths %s = %d." % (cs, J([x for x in lens if x > 1]) or "1", order))
    if kind == "parity":
        return mcq(r, "Is the permutation %s even or odd?" % two, "odd" if par else "even", ["even" if par else "odd", "neither", "both"],
                   "Cycles: %s. A k-cycle is k − 1 transpositions, total %d, which is %s." % (cs, sum(x - 1 for x in lens), "odd" if par else "even"))
    if kind == "fixed":
        return nat(r, "How many fixed points does the permutation %s have?" % two, lens.count(1), "Fixed points are the 1-cycles. Cycle form %s leaves %d elements in place." % (cs, lens.count(1)))
    return nat(r, "How many cycles (counting fixed points as 1-cycles) does %s have?" % two, len(cy), "Following each element until it returns: %s plus %d fixed point(s): %d cycles." % (cs, lens.count(1), len(cy)))


# ---------------------------------------------------------------- graphs
@gen(S, GRAPH, "Connectivity & paths", n=70, diff="medium")
def gr_conn(r):
    kind = r.choice(["euler", "eulerpath", "hamk", "connmin", "maxdisc", "comps", "bridge"])
    if kind == "euler":
        n = r.randint(4, 9)
        return mcq(r, "Does the complete graph K%d have an Euler circuit?" % n, "Yes" if (n - 1) % 2 == 0 else "No", ["No" if (n - 1) % 2 == 0 else "Yes", "Only if it is planar", "Only for n = 3"],
                   "Every vertex of K%d has degree %d. An Euler circuit exists iff the graph is connected and every degree is even: %s." % (n, n - 1, "even, yes" if (n - 1) % 2 == 0 else "odd, no"))
    if kind == "eulerpath":
        degs = [r.choice([2, 2, 3, 4, 3]) for _ in range(r.randint(5, 7))]
        if sum(degs) % 2:
            degs[0] += 1
        odd = sum(d % 2 for d in degs)
        ans = "Euler circuit" if odd == 0 else "Euler path but no circuit" if odd == 2 else "neither"
        return mcq(r, "A connected graph has degree sequence %s. It has" % J(degs), ans, [x for x in ["Euler circuit", "Euler path but no circuit", "neither", "a Hamilton cycle for sure"] if x != ans],
                   "Number of odd-degree vertices: %d. 0 → Euler circuit; 2 → Euler path between the two odd vertices; more → neither." % odd)
    if kind == "hamk":
        n = r.randint(4, 8)
        return nat(r, "How many distinct Hamilton cycles does K%d have (a cycle and its reverse are the same)?" % n, math.factorial(n - 1) // 2,
                   "Fix a start vertex, order the other %d: (n − 1)! sequences, each cycle counted twice (two directions): %d!/2 = %d." % (n - 1, n - 1, math.factorial(n - 1) // 2))
    if kind == "connmin":
        n = r.randint(5, 12)
        return nat(r, "What is the minimum number of edges that GUARANTEES a simple graph on %d vertices is connected?" % n, C(n - 1, 2) + 1,
                   "The worst disconnected graph is K%d plus an isolated vertex, with C(%d, 2) = %d edges. One more edge forces connectivity: %d." % (n - 1, n - 1, C(n - 1, 2), C(n - 1, 2) + 1))
    if kind == "maxdisc":
        n, k = r.randint(6, 12), r.randint(2, 3)
        return nat(r, "What is the maximum number of edges in a simple graph with %d vertices and %d components?" % (n, k), C(n - k + 1, 2),
                   "Put k − 1 isolated vertices and a complete graph on the remaining n − k + 1 = %d vertices: C(%d, 2) = %d." % (n - k + 1, n - k + 1, C(n - k + 1, 2)))
    if kind == "comps":
        n, e = r.randint(8, 15), r.randint(3, 6)
        return nat(r, "A forest has %d vertices and %d edges. How many connected components does it have?" % (n, e), n - e, "Each tree with k vertices has k − 1 edges, so components = vertices − edges = %d − %d = %d." % (n, e, n - e))
    n = r.randint(5, 10)
    return nat(r, "A tree has %d vertices. How many of its edges are bridges (removal disconnects the graph)?" % n, n - 1, "In a tree every edge is a bridge, because there is exactly one path between any two vertices: all %d edges." % (n - 1))


@gen(S, GRAPH, "Trees & spanning trees", n=70, diff="medium")
def gr_tree(r):
    kind = r.choice(["edges", "leaves", "cayley", "cycle", "kmn", "deg", "internal"])
    if kind == "edges":
        n = r.randint(6, 30)
        return nat(r, "How many edges does a tree with %d vertices have?" % n, n - 1, "A tree is connected and acyclic, so it has exactly n − 1 = %d edges." % (n - 1))
    if kind == "leaves":
        a, b = r.randint(1, 4), r.randint(1, 4)
        L = 2 + a + 2 * b
        return nat(r, "A tree has %d vertices of degree 3, %d vertices of degree 4, and all other vertices are leaves. How many leaves?" % (a, b), L,
                   "Let L be the number of leaves, n = %d + %d + L. Σdeg = 2(n − 1): 3·%d + 4·%d + L = 2(%d + L − 1). So L = 2 + %d + 2·%d = %d." % (a, b, a, b, a + b, a, b, L))
    if kind == "cayley":
        n = r.randint(3, 8)
        return nat(r, "How many labelled trees are there on %d vertices?" % n, n ** (n - 2), "Cayley's formula n^(n−2) = %d^%d = %d (also the number of spanning trees of K%d)." % (n, n - 2, n ** (n - 2), n))
    if kind == "cycle":
        n = r.randint(4, 12)
        return nat(r, "How many spanning trees does the cycle graph C%d have?" % n, n, "Removing any one of the %d edges of a cycle leaves a spanning path; removing two disconnects it. So %d spanning trees." % (n, n))
    if kind == "kmn":
        m, n = r.randint(2, 4), r.randint(2, 4)
        return nat(r, "How many spanning trees does the complete bipartite graph K_{%d,%d} have? (Formula m^(n−1)·n^(m−1).)" % (m, n), m ** (n - 1) * n ** (m - 1),
                   "Spanning trees of K_{m,n}: m^(n−1)·n^(m−1) = %d^%d·%d^%d = %d." % (m, n - 1, n, m - 1, m ** (n - 1) * n ** (m - 1)))
    if kind == "deg":
        n = r.randint(5, 15)
        return nat(r, "What is the sum of the degrees of all vertices of a tree with %d vertices?" % n, 2 * (n - 1), "Σdeg = 2e = 2(n − 1) = %d." % (2 * (n - 1)))
    k, i = r.randint(2, 4), r.randint(3, 12)
    return nat(r, "A full %d-ary tree (every internal node has %d children) has %d internal nodes. How many vertices in total?" % (k, k, i), k * i + 1,
               "Every vertex except the root is a child: n = k·i + 1 = %d·%d + 1 = %d." % (k, i, k * i + 1))


@gen(S, GRAPH, "Planar graphs", n=70, diff="medium")
def gr_planar(r):
    kind = r.choice(["faces", "maxe", "trifree", "nonplanar", "degface", "comps"])
    n = r.randint(5, 14)
    if kind == "faces":
        e = r.randint(n, 3 * n - 6)
        return nat(r, "A connected planar graph has %d vertices and %d edges. How many regions (faces, including the outer one) does a planar drawing have?" % (n, e), e - n + 2,
                   "Euler: v − e + f = 2, so f = 2 − %d + %d = %d." % (n, e, e - n + 2))
    if kind == "maxe":
        return nat(r, "Maximum number of edges of a simple planar graph on %d vertices?" % n, 3 * n - 6, "Each face has at least 3 edges and each edge borders 2 faces: 3f ≤ 2e. With Euler this gives e ≤ 3v − 6 = %d." % (3 * n - 6))
    if kind == "trifree":
        return nat(r, "Maximum number of edges of a simple planar graph on %d vertices that has NO triangle?" % n, 2 * n - 4, "Without triangles each face has at least 4 edges: 4f ≤ 2e, giving e ≤ 2v − 4 = %d." % (2 * n - 4))
    if kind == "nonplanar":
        g, ans = r.choice([("K5", "not planar"), ("K3,3", "not planar"), ("K4", "planar"), ("K2,5", "planar"), ("the cube graph Q3", "planar"), ("K6", "not planar"), ("the Petersen graph", "not planar")])
        return mcq(r, "Is %s planar?" % g, ans, ["planar" if ans == "not planar" else "not planar", "planar only without its outer face", "cannot be decided"],
                   "K5 (10 edges > 3·5 − 6 = 9) and K3,3 (9 edges > 2·6 − 4 = 8, triangle-free) are the two basic non-planar graphs; any graph containing a subdivision of either is non-planar (Kuratowski). K4, K2,n and Q3 can be drawn without crossings.")
    if kind == "degface":
        f = r.randint(4, 10)
        k = r.choice([3, 4])
        return nat(r, "A connected planar graph has %d faces and every face is bounded by exactly %d edges. How many edges does it have?" % (f, k), f * k // 2 if f * k % 2 == 0 else (f * k + k) // 2,
                   "Each edge borders exactly two faces, so Σ(face lengths) = 2e: %d·%d = 2e, e = %d." % (f, k, f * k // 2)) if f * k % 2 == 0 else (_ for _ in ()).throw(Skip())
    c = r.randint(2, 3)
    e = r.randint(n, 2 * n)
    return nat(r, "A planar graph (not connected) has %d vertices, %d edges and %d components. How many faces?" % (n, e, c), e - n + 1 + c,
               "For c components Euler's formula is v − e + f = 1 + c, so f = 1 + %d − %d + %d = %d." % (c, n, e, e - n + 1 + c))


@gen(S, GRAPH, "Matching & covers", n=60, diff="medium")
def gr_match(r):
    kind = r.choice(["kn", "kmn", "path", "cycle", "indep", "konig", "perfect"])
    n = r.randint(4, 12)
    if kind == "kn":
        return nat(r, "What is the size of a maximum matching in K%d?" % n, n // 2, "A matching uses disjoint edges; each covers 2 vertices, so at most ⌊n/2⌋ = %d, and K%d achieves it." % (n // 2, n))
    if kind == "kmn":
        a, b = r.randint(2, 7), r.randint(2, 7)
        return nat(r, "What is the size of a maximum matching in K_{%d,%d}?" % (a, b), min(a, b), "Each matched edge uses one vertex from each side, so at most min(%d, %d) = %d, and it is attainable." % (a, b, min(a, b)))
    if kind == "path":
        return nat(r, "What is the maximum matching size in the path P%d (%d vertices)?" % (n, n), n // 2, "Take every other edge: ⌊%d/2⌋ = %d." % (n, n // 2))
    if kind == "cycle":
        return nat(r, "What is the independence number (largest set of pairwise non-adjacent vertices) of the cycle C%d?" % n, n // 2, "Pick every second vertex: ⌊%d/2⌋ = %d." % (n, n // 2))
    if kind == "indep":
        a = r.randint(2, n - 2)
        return nat(r, "A graph on %d vertices has independence number %d. What is the size of its minimum vertex cover?" % (n, a), n - a,
                   "A set is independent iff its complement is a vertex cover (Gallai): α + β = n, so β = %d − %d = %d." % (n, a, n - a))
    if kind == "konig":
        m = r.randint(2, 8)
        return nat(r, "A bipartite graph has a maximum matching of size %d. What is the size of its minimum vertex cover?" % m, m,
                   "König's theorem: in a bipartite graph, maximum matching size = minimum vertex cover size = %d." % m)
    m = 2 * r.randint(2, 4)
    v = math.factorial(m) // (2 ** (m // 2) * math.factorial(m // 2))
    return nat(r, "How many perfect matchings does K%d have?" % m, v, "Pair the first unmatched vertex with any of the others repeatedly: (n − 1)(n − 3)…1 = %d!! = %d." % (m - 1, v))


# ---------------------------------------------------------------- combinatorics
@gen(S, COMB, "Arrangements", n=70, diff="medium")
def cb_arr(r):
    kind = r.choice(["word", "together", "apart", "circ", "necklace", "vowels"])
    if kind == "word":
        w = r.choice(["LETTER", "BALLOON", "SUCCESS", "PEPPER", "BANANA", "PARALLEL", "ASSESS", "COFFEE"])
        c = Counter(w)
        v = math.factorial(len(w))
        for x in c.values():
            v //= math.factorial(x)
        return nat(r, "How many distinct arrangements of the letters of %s are there?" % w, v,
                   "%d letters with repeats %s: %d!/(%s) = %d." % (len(w), ", ".join("%s×%d" % (k, x) for k, x in c.items() if x > 1), len(w), "·".join("%d!" % x for x in c.values() if x > 1), v))
    if kind == "together":
        n, k = r.randint(5, 8), r.randint(2, 3)
        v = math.factorial(n - k + 1) * math.factorial(k)
        return nat(r, "In how many ways can %d people stand in a row if %d particular people must stand together?" % (n, k), v,
                   "Glue the %d into one block: %d units arranged in %d! ways, and the block arranged inside in %d! ways: %d·%d = %d." % (k, n - k + 1, n - k + 1, k, math.factorial(n - k + 1), math.factorial(k), v))
    if kind == "apart":
        n = r.randint(4, 8)
        v = math.factorial(n) - 2 * math.factorial(n - 1)
        return nat(r, "In how many ways can %d people stand in a row if two particular people must NOT stand next to each other?" % n, v,
                   "Total %d! = %d minus the arrangements with the two together, 2·(%d − 1)! = %d: %d." % (n, math.factorial(n), n, 2 * math.factorial(n - 1), v))
    if kind == "circ":
        n = r.randint(4, 9)
        return nat(r, "In how many ways can %d people sit around a round table (rotations equal)?" % n, math.factorial(n - 1), "Fix one person's seat to remove the %d rotations: (n − 1)! = %d." % (n, math.factorial(n - 1)))
    if kind == "necklace":
        n = r.randint(4, 8)
        return nat(r, "How many different necklaces can be made from %d distinct beads (rotations and reflections equal)?" % n, math.factorial(n - 1) // 2,
                   "Circular arrangements (n − 1)! = %d; turning the necklace over pairs them up: %d/2 = %d." % (math.factorial(n - 1), math.factorial(n - 1), math.factorial(n - 1) // 2))
    m, k = r.randint(3, 5), r.randint(2, 3)
    if k > m + 1:
        raise Skip()
    v = math.factorial(m) * math.perm(m + 1, k)
    return nat(r, "%d boys and %d girls stand in a row so that no two girls are adjacent. How many arrangements?" % (m, k), v,
               "Arrange the boys: %d! ways. That leaves %d gaps (ends included); put the girls in distinct gaps in order: P(%d, %d). Total %d·%d = %d." % (m, m + 1, m + 1, k, math.factorial(m), math.perm(m + 1, k), v))


@gen(S, COMB, "Binomial coefficients", n=60, diff="medium")
def cb_binom(r):
    kind = r.choice(["coef", "sum", "path", "pathvia", "const", "pascal"])
    if kind == "coef":
        n, k, a, b = r.randint(4, 8), None, r.randint(1, 3), r.randint(1, 3)
        k = r.randint(1, n - 1)
        v = C(n, k) * a ** (n - k) * b ** k
        return nat(r, "Coefficient of x^%d·y^%d in (%dx + %dy)^%d?" % (n - k, k, a, b, n), v, "Term C(n, k)(ax)^(n−k)(by)^k: C(%d, %d)·%d^%d·%d^%d = %d." % (n, k, a, n - k, b, k, v))
    if kind == "sum":
        n = r.randint(5, 12)
        return nat(r, "Evaluate C(%d,0) + C(%d,1) + … + C(%d,%d)." % (n, n, n, n), 2 ** n, "Put x = 1 in (1 + x)^n: the sum of all binomial coefficients is 2^%d = %d." % (n, 2 ** n))
    if kind == "path":
        a, b = r.randint(2, 6), r.randint(2, 6)
        return nat(r, "How many shortest lattice paths go from (0, 0) to (%d, %d) using unit steps right and up?" % (a, b), C(a + b, a),
                   "Any shortest path is a word of %d R's and %d U's: C(%d, %d) = %d." % (a, b, a + b, a, C(a + b, a)))
    if kind == "pathvia":
        a, b = r.randint(1, 3), r.randint(1, 3)
        c, d = a + r.randint(1, 3), b + r.randint(1, 3)
        v = C(a + b, a) * C(c - a + d - b, c - a)
        return nat(r, "How many shortest right/up lattice paths go from (0, 0) to (%d, %d) passing through (%d, %d)?" % (c, d, a, b), v,
                   "Multiply the two legs: C(%d, %d)·C(%d, %d) = %d·%d = %d." % (a + b, a, c - a + d - b, c - a, C(a + b, a), C(c - a + d - b, c - a), v))
    if kind == "const":
        n = 2 * r.randint(2, 5)
        return nat(r, "Find the constant term in the expansion of (x + 1/x)^%d." % n, C(n, n // 2), "Term C(n, k)x^(n−k)x^(−k) is constant when n − 2k = 0, k = %d: C(%d, %d) = %d." % (n // 2, n, n // 2, C(n, n // 2)))
    n, k = r.randint(5, 12), r.randint(2, 4)
    return nat(r, "C(%d, %d) + C(%d, %d) equals C(%d, m). Find m (choose m ≤ %d/2 + 1 if two values work, i.e. the smaller)." % (n, k - 1, n, k, n + 1, n + 1), min(k, n + 1 - k),
               "Pascal's identity: C(n, k − 1) + C(n, k) = C(n + 1, k), so C(%d, %d) = C(%d, %d); the smaller index is %d." % (n + 1, k, n + 1, n + 1 - k, min(k, n + 1 - k)))


@gen(S, COMB, "Derangements & exclusion", n=60, diff="medium")
def cb_der(r):
    D = [1, 0]
    for k in range(2, 11):
        D.append((k - 1) * (D[-1] + D[-2]))
    kind = r.choice(["der", "exactk", "prob", "atleast", "none3"])
    n = r.randint(4, 8)
    if kind == "der":
        return nat(r, "How many derangements of %d letters are there (no letter in its own envelope)?" % n, D[n], "Dₙ = (n − 1)(Dₙ₋₁ + Dₙ₋₂): D = %s, so D%d = %d." % (J(D[:n + 1]), n, D[n]))
    if kind == "exactk":
        k = r.randint(1, 3)
        v = C(n, k) * D[n - k]
        return nat(r, "%d letters are placed at random in %d addressed envelopes. In how many placements are EXACTLY %d letters in the right envelope?" % (n, n, k), v,
                   "Choose the %d correct ones, C(%d, %d), and derange the other %d: D%d = %d. Total %d·%d = %d." % (k, n, k, n - k, n - k, D[n - k], C(n, k), D[n - k], v))
    if kind == "prob":
        v = F(D[n], math.factorial(n))
        return nat(r, "A random permutation of %d items is chosen. Probability (4 decimals) that no item stays in place?" % n, round(float(v), 4), "D%d/%d! = %d/%d ≈ %.4f (close to 1/e ≈ 0.3679)." % (n, n, D[n], math.factorial(n), float(v)), tol=0.0006)
    if kind == "atleast":
        v = math.factorial(n) - D[n]
        return nat(r, "In how many permutations of %d items is AT LEAST one item in its original place?" % n, v, "Complement of derangements: %d! − D%d = %d − %d = %d." % (n, n, math.factorial(n), D[n], v))
    N = r.choice([60, 100, 120, 200, 210])
    a, b, c = r.choice([(2, 3, 5), (2, 3, 7), (3, 5, 7), (2, 5, 7)])
    v = sum(1 for x in range(1, N + 1) if x % a and x % b and x % c)
    return nat(r, "How many integers from 1 to %d are divisible by none of %d, %d and %d?" % (N, a, b, c), v,
               "Inclusion–exclusion: N − (⌊N/%d⌋ + ⌊N/%d⌋ + ⌊N/%d⌋) + (⌊N/%d⌋ + ⌊N/%d⌋ + ⌊N/%d⌋) − ⌊N/%d⌋ = %d." % (a, b, c, a * b, a * c, b * c, a * b * c, v))


@gen(S, COMB, "Generating functions", n=60, diff="hard", marks=2)
def cb_gf(r):
    kind = r.choice(["geom", "coef", "dice", "seq", "closed"])
    if kind == "geom":
        a, n = r.randint(2, 5), r.randint(3, 8)
        return nat(r, "What is the coefficient of x^%d in 1/(1 − %dx)?" % (n, a), a ** n, "1/(1 − ax) = Σ aⁿxⁿ, so the coefficient is %d^%d = %d." % (a, n, a ** n))
    if kind == "coef":
        k, n = r.randint(2, 4), r.randint(3, 8)
        return nat(r, "What is the coefficient of x^%d in 1/(1 − x)^%d?" % (n, k), C(n + k - 1, k - 1),
                   "1/(1 − x)^k = Σ C(n + k − 1, k − 1) xⁿ (stars and bars): C(%d, %d) = %d." % (n + k - 1, k - 1, C(n + k - 1, k - 1)))
    if kind == "dice":
        t = r.randint(5, 10)
        v = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == t)
        return nat(r, "Using (x + x² + … + x⁶)², find the coefficient of x^%d (the number of ways two dice show a total of %d)." % (t, t), v,
                   "The coefficient of x^t counts pairs (a, b) with a + b = %d and 1 ≤ a, b ≤ 6: %d." % (t, v))
    if kind == "seq":
        a = r.randint(2, 4)
        n = r.randint(3, 6)
        return nat(r, "The generating function of a sequence is x/(1 − x)². What is its term a%d?" % n, n, "x/(1 − x)² = Σ n xⁿ, so aₙ = n and a%d = %d." % (n, n))
    c, n = r.randint(2, 4), r.randint(2, 6)
    v = c ** (n + 1) - 1
    return nat(r, "aₙ = %d·aₙ₋₁ + 1 with a₀ = %d − 1 = %d … more simply a₀ = %d. Using generating functions (or iteration), find a%d." % (c, c, c - 1, c - 1, n) if False else
               "aₙ = %d·aₙ₋₁ + %d with a₀ = %d. Find a%d." % (c, c - 1, c - 1, n), v,
               "Guess aₙ = %d^(n+1) − 1: a₀ = %d − 1 = %d ✓ and %d(%d^n − 1) + %d = %d^(n+1) − 1 ✓. So a%d = %d." % (c, c, c - 1, c, c, c - 1, c, n, v))


# ---------------------------------------------------------------- linear algebra
def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def mstr(m):
    return "[" + "; ".join(" ".join(fm(x) for x in row) for row in m) + "]"


@gen(S, MAT, "Matrix algebra", n=70, diff="easy")
def la_alg(r):
    kind = r.choice(["prod", "entry", "trace", "dim", "symm", "transp", "powers"])
    if kind in ("prod", "entry"):
        A = [[r.randint(-3, 4) for _ in range(2)] for _ in range(2)]
        B = [[r.randint(-3, 4) for _ in range(2)] for _ in range(2)]
        P = mm(A, B)
        i, j = r.randint(0, 1), r.randint(0, 1)
        return nat(r, "A = %s and B = %s (rows separated by ;). Find the (%d, %d) entry of AB." % (mstr(A), mstr(B), i + 1, j + 1), P[i][j],
                   "Entry (i, j) of AB = row i of A · column j of B = %d·%d + %d·%d = %d." % (A[i][0], B[0][j], A[i][1], B[1][j], P[i][j]))
    if kind == "trace":
        A = [[r.randint(-3, 5) for _ in range(3)] for _ in range(3)]
        B = [[r.randint(-3, 5) for _ in range(3)] for _ in range(3)]
        t = sum(mm(A, B)[i][i] for i in range(3))
        return nat(r, "A = %s, B = %s. Find trace(AB)." % (mstr(A), mstr(B)), t, "trace(AB) = Σᵢ Σₖ aᵢₖbₖᵢ = %d. (Also trace(AB) = trace(BA) even though AB ≠ BA in general.)" % t)
    if kind == "dim":
        m, n, p = r.randint(2, 6), r.randint(2, 6), r.randint(2, 6)
        return nat(r, "A is %d × %d and B is %d × %d. How many scalar multiplications does computing AB take by the definition?" % (m, n, n, p), m * n * p, "AB is %d × %d; each entry is a dot product of length %d: %d·%d·%d = %d." % (m, p, n, m, p, n, m * n * p))
    if kind == "symm":
        n = r.randint(2, 6)
        return nat(r, "How many independent entries does an n × n symmetric matrix have for n = %d?" % n, n * (n + 1) // 2, "The diagonal and the entries above it determine the rest: n(n + 1)/2 = %d." % (n * (n + 1) // 2))
    if kind == "transp":
        return mcq(r, "For conformable matrices A and B, (AB)ᵀ equals", "BᵀAᵀ", ["AᵀBᵀ", "BA", "(BA)ᵀ"], "Transposing reverses the order: (AB)ᵀ = BᵀAᵀ. The same reversal holds for inverses.")
    a, k = r.randint(2, 4), r.randint(2, 5)
    return nat(r, "A = [1 %d; 0 1]. Find the (1, 2) entry of A^%d." % (a, k), a * k, "[1 a; 0 1]ᵏ = [1 ka; 0 1] (each multiplication adds a to the corner): %d·%d = %d." % (k, a, a * k))


@gen(S, LIN, "LU decomposition", n=60, diff="medium", marks=2)
def la_lu(r):
    while True:
        l21, l31, l32 = r.randint(-3, 3), r.randint(-3, 3), r.randint(-3, 3)
        u = [[r.randint(1, 4), r.randint(-3, 4), r.randint(-3, 4)], [0, r.randint(1, 4), r.randint(-3, 4)], [0, 0, r.randint(1, 5)]]
        L = [[1, 0, 0], [l21, 1, 0], [l31, l32, 1]]
        A = mm(L, u)
        if max(abs(x) for row in A for x in row) <= 20:
            break
    kind = r.choice(["l21", "l31", "u33", "det", "u22"])
    show = "A = %s" % mstr(A)
    m21 = F(A[1][0], A[0][0])
    if kind == "l21":
        return nat(r, "Doolittle LU decomposition (L has 1s on its diagonal) of %s. Find l21." % show, l21,
                   "Eliminate below the first pivot %d: l21 = a21/a11 = %d/%d = %s, l31 = a31/a11 = %s. These multipliers are exactly the entries of L." % (A[0][0], A[1][0], A[0][0], fm(m21), fm(F(A[2][0], A[0][0]))))
    if kind == "l31":
        return nat(r, "Doolittle LU decomposition of %s. Find l31." % show, l31, "l31 = a31/a11 = %d/%d = %s (the multiplier used to clear row 3, column 1)." % (A[2][0], A[0][0], fm(F(A[2][0], A[0][0]))))
    if kind == "u22":
        return nat(r, "Doolittle LU decomposition of %s. Find u22." % show, u[1][1], "U's first row is A's first row. Row 2 − l21·row 1 with l21 = %s gives u22 = a22 − l21·u12 = %d − (%s)(%d) = %d." % (fm(m21), A[1][1], fm(m21), u[0][1], u[1][1]))
    if kind == "u33":
        return nat(r, "Doolittle LU decomposition of %s. Find u33." % show, u[2][2],
                   "Eliminate column 1 (multipliers %s, %s), then column 2 (multiplier %s). The last pivot is u33 = %d. Check: det A = u11·u22·u33 = %d." % (fm(m21), fm(F(A[2][0], A[0][0])), fm(l32), u[2][2], u[0][0] * u[1][1] * u[2][2]))
    return nat(r, "A = LU with L unit lower-triangular and U = %s. Find det A." % mstr(u), u[0][0] * u[1][1] * u[2][2],
               "det A = det L · det U = 1 · (product of U's diagonal) = %d·%d·%d = %d." % (u[0][0], u[1][1], u[2][2], u[0][0] * u[1][1] * u[2][2]))


@gen(S, LIN, "Cayley–Hamilton & diagonalisation", n=60, diff="medium")
def la_ch(r):
    a, b, c, d = [r.randint(-3, 4) for _ in range(4)]
    tr, dt = a + d, a * d - b * c
    kind = r.choice(["inv", "a3", "diag", "power", "rep"])
    A = "[%d %d; %d %d]" % (a, b, c, d)
    if kind == "inv":
        if dt == 0:
            raise Skip()
        i, j = r.randint(0, 1), r.randint(0, 1)
        inv = [[F(d, dt), F(-b, dt)], [F(-c, dt), F(a, dt)]]
        return nat(r, "Use Cayley–Hamilton to find A⁻¹ for A = %s. What is its (%d, %d) entry? (3 decimals)" % (A, i + 1, j + 1), round(float(inv[i][j]), 3),
                   "A² − %dA + %dI = 0 ⇒ A(A − %dI) = −%dI ⇒ A⁻¹ = (%dI − A)/%d. Entry (%d, %d) = %s." % (tr, dt, tr, dt, tr, dt, i + 1, j + 1, fm(inv[i][j])), tol=0.002)
    if kind == "a3":
        A2 = mm([[a, b], [c, d]], [[a, b], [c, d]])
        A3 = mm(A2, [[a, b], [c, d]])
        return nat(r, "A = %s. Using A² = %dA − %dI, find the (1, 1) entry of A³." % (A, tr, dt), A3[0][0],
                   "A³ = A·A² = %dA² − %dA = %d(%dA − %dI) − %dA = %dA − %dI. Entry (1, 1) = %d·%d − %d = %d." % (tr, dt, tr, tr, dt, dt, tr * tr - dt, tr * dt, tr * tr - dt, a, tr * dt, A3[0][0]))
    if kind == "diag":
        l1, l2 = r.sample(range(-3, 6), 2)
        return mcq(r, "A 2 × 2 matrix has eigenvalues %d and %d. Is it diagonalisable?" % (l1, l2), "Yes, always", ["No, never", "Only if it is symmetric", "Only if both eigenvalues are positive"],
                   "Distinct eigenvalues give independent eigenvectors, so a 2 × 2 matrix with distinct eigenvalues is always diagonalisable: A = PDP⁻¹ with D = diag(%d, %d)." % (l1, l2))
    if kind == "power":
        l1, l2 = r.randint(1, 3), r.randint(-2, 2)
        k = r.randint(2, 5)
        return nat(r, "A is diagonalisable with eigenvalues %d and %d. Find trace(A^%d)." % (l1, l2, k), l1 ** k + l2 ** k, "A = PDP⁻¹ ⇒ Aᵏ = PDᵏP⁻¹, whose eigenvalues are λᵏ: %d^%d + (%d)^%d = %d." % (l1, k, l2, k, l1 ** k + l2 ** k))
    return mcq(r, "A = [%d 1; 0 %d] (upper-triangular, repeated eigenvalue %d). Is A diagonalisable?" % (a, a, a), "No", ["Yes", "Only if %d = 0" % a, "Yes, because it is triangular"],
               "A − %dI = [0 1; 0 0] has rank 1, so the eigenspace has dimension 1 < 2: only one independent eigenvector, hence not diagonalisable." % a)


# ---------------------------------------------------------------- calculus
@gen(S, LIM, "Mean value theorems", n=60, diff="medium")
def ca_mvt(r):
    kind = r.choice(["sq", "cube", "rolle", "cauchy", "hyp"])
    if kind == "sq":
        a = r.randint(0, 4); b = a + r.randint(1, 6)
        return nat(r, "Find c from Lagrange's mean value theorem for f(x) = x² on [%d, %d]." % (a, b), (a + b) / 2, "f′(c) = 2c = (b² − a²)/(b − a) = a + b = %d, so c = %s, the midpoint." % (a + b, fm(F(a + b, 2))), tol=0.001)
    if kind == "cube":
        b = r.randint(1, 4)
        c = b / math.sqrt(3)
        return nat(r, "Find c in (0, %d) from the mean value theorem for f(x) = x³ on [0, %d] (3 decimals)." % (b, b), round(c, 3), "3c² = (%d³ − 0)/%d = %d, so c = %d/√3 ≈ %.3f." % (b, b, b * b, b, c), tol=0.002)
    if kind == "rolle":
        p, q = sorted(r.sample(range(-3, 6), 2))
        return nat(r, "Find the point c guaranteed by Rolle's theorem for f(x) = (x − %d)(x − %d) on [%d, %d]." % (p, q, p, q), (p + q) / 2, "f(%d) = f(%d) = 0. f′(x) = 2x − %d = 0 at c = %s." % (p, q, p + q, fm(F(p + q, 2))), tol=0.001)
    if kind == "cauchy":
        a, b = 1, r.randint(2, 4)
        return nat(r, "Cauchy's mean value theorem for f(x) = x² and g(x) = x on [%d, %d]: find c (f′(c)/g′(c) = (f(b) − f(a))/(g(b) − g(a)))." % (a, b), (a + b) / 2,
                   "2c/1 = (%d − 1)/(%d − 1) = %d, so c = %s." % (b * b, b, a + b, fm(F(a + b, 2))), tol=0.001)
    f, ans, why = r.choice([("f(x) = |x| on [−1, 1]", "No", "|x| is not differentiable at 0, so Rolle's theorem does not apply (and indeed f′ is never 0)."),
                            ("f(x) = x² − 4 on [−2, 2]", "Yes", "Polynomial: continuous and differentiable, f(−2) = f(2) = 0. c = 0."),
                            ("f(x) = 1/x on [−1, 1]", "No", "1/x is not continuous at 0."),
                            ("f(x) = sin x on [0, π]", "Yes", "sin 0 = sin π = 0 and sin is smooth; c = π/2.")])
    return mcq(r, "Do the hypotheses of Rolle's theorem hold for %s?" % f, ans, ["No" if ans == "Yes" else "Yes", "Only on the open interval", "Only if f is odd"], why)


@gen(S, LIM, "Series & Taylor", n=60, diff="medium")
def ca_series(r):
    kind = r.choice(["mac", "geo", "conv", "coef", "approx"])
    if kind == "mac":
        f, n, v, why = r.choice([("eˣ", 3, F(1, 6), "eˣ = 1 + x + x²/2! + x³/3! + …"), ("sin x", 3, F(-1, 6), "sin x = x − x³/3! + x⁵/5! − …"),
                                 ("cos x", 2, F(-1, 2), "cos x = 1 − x²/2! + x⁴/4! − …"), ("ln(1 + x)", 2, F(-1, 2), "ln(1 + x) = x − x²/2 + x³/3 − …"),
                                 ("1/(1 − x)", 4, F(1), "1/(1 − x) = 1 + x + x² + x³ + …"), ("e^(2x)", 2, F(2), "e^(2x) = 1 + 2x + (2x)²/2! + … , so x² has 4/2 = 2")])
        return nat(r, "Coefficient of x^%d in the Maclaurin series of %s? (3 decimals)" % (n, f), round(float(v), 3), "%s, so the coefficient is %s." % (why, fm(v)), tol=0.002)
    if kind == "geo":
        a, num, den = r.randint(1, 6), 1, r.randint(2, 5)
        s = F(a) / (1 - F(num, den))
        return nat(r, "Sum of the infinite geometric series %d + %d·(1/%d) + %d·(1/%d)² + …? (3 decimals)" % (a, a, den, a, den), round(float(s), 3), "a/(1 − r) = %d/(1 − 1/%d) = %s." % (a, den, fm(s)), tol=0.002)
    if kind == "conv":
        s, ans, why = r.choice([("Σ 1/n", "diverges", "harmonic series (p = 1)"), ("Σ 1/n²", "converges", "p-series with p = 2 > 1"),
                                ("Σ (−1)ⁿ/n", "converges", "alternating series with terms decreasing to 0 (conditionally)"), ("Σ n/2ⁿ", "converges", "ratio test: (n + 1)/(2n) → 1/2 < 1"),
                                ("Σ 2ⁿ/n!", "converges", "ratio test: 2/(n + 1) → 0"), ("Σ n!/nⁿ", "converges", "ratio test: (n/(n + 1))ⁿ → 1/e < 1"),
                                ("Σ 1/√n", "diverges", "p-series with p = 1/2 ≤ 1"), ("Σ n/(n + 1)", "diverges", "terms tend to 1, not 0")])
        return mcq(r, "The series %s" % s, ans, ["converges" if ans == "diverges" else "diverges", "oscillates boundedly", "cannot be determined"], "It %s: %s." % (ans, why))
    if kind == "coef":
        k = r.randint(2, 5)
        return nat(r, "f(x) = x^%d. What is the coefficient of (x − 1)² in its Taylor series about x = 1?" % k, C(k, 2), "f″(1)/2! = %d·%d/2 = %d (equivalently C(%d, 2))." % (k, k - 1, C(k, 2), k))
    x = r.choice([0.1, 0.2, 0.05])
    v = 1 + x + x * x / 2
    return nat(r, "Approximate e^%s using the Maclaurin polynomial 1 + x + x²/2 (4 decimals)." % x, round(v, 4), "1 + %s + %s²/2 = %.4f (true value %.4f)." % (x, x, v, math.exp(x)), tol=0.0006)


@gen(S, INT, "Integration techniques", n=70, diff="medium")
def ca_tech(r):
    kind = r.choice(["parts", "sub", "improper", "even", "odd", "pf", "ln"])
    if kind == "parts":
        n = r.randint(1, 3)
        v = [None, F(1), F(1), None][n] if n < 3 else None
        if n == 1:
            return nat(r, "Evaluate ∫₀¹ x eˣ dx.", 1, "By parts with u = x, dv = eˣ dx: [x eˣ]₀¹ − ∫₀¹ eˣ dx = e − (e − 1) = 1.")
        if n == 2:
            return nat(r, "Evaluate ∫₁^e ln x dx.", 1, "By parts with u = ln x, dv = dx: [x ln x − x]₁^e = (e − e) − (0 − 1) = 1.")
        return nat(r, "Evaluate ∫₀^(π/2) x cos x dx (3 decimals).", round(math.pi / 2 - 1, 3), "By parts: [x sin x]₀^(π/2) − ∫₀^(π/2) sin x dx = π/2 − 1 ≈ %.3f." % (math.pi / 2 - 1), tol=0.002)
    if kind == "sub":
        a = r.randint(2, 5)
        return nat(r, "Evaluate ∫₀¹ %dx(x² + 1)^%d dx … with the substitution u = x² + 1 (3 decimals)." % (2, a - 1) if False else "Evaluate ∫₀¹ 2x(x² + 1)^%d dx (3 decimals)." % (a - 1), round((2 ** a - 1) / a, 3),
                   "Put u = x² + 1, du = 2x dx, limits 1 → 2: ∫₁² u^%d du = (2^%d − 1)/%d = %s." % (a - 1, a, a, fm(F(2 ** a - 1, a))), tol=0.002)
    if kind == "improper":
        p = r.choice([2, 3, 4])
        return nat(r, "Evaluate the improper integral ∫₁^∞ x^(−%d) dx (3 decimals)." % p, round(1 / (p - 1), 3), "For p > 1, ∫₁^∞ x^(−p) dx = 1/(p − 1) = 1/%d." % (p - 1), tol=0.002)
    if kind == "even":
        a, n = r.randint(1, 3), 2
        v = F(2 * a ** 3, 3)
        return nat(r, "Evaluate ∫₋%d^%d x² dx (3 decimals)." % (a, a), round(float(v), 3), "x² is even, so the integral is 2∫₀^%d x² dx = 2·%d³/3 = %s." % (a, a, fm(v)), tol=0.002)
    if kind == "odd":
        a = r.randint(1, 5)
        return nat(r, "Evaluate ∫₋%d^%d (x³ + sin x) dx." % (a, a), 0, "x³ + sin x is odd (f(−x) = −f(x)), and an odd function integrates to 0 over a symmetric interval.")
    if kind == "pf":
        return nat(r, "Evaluate ∫₁² dx/(x(x + 1)) (4 decimals).", round(math.log(4 / 3), 4), "Partial fractions: 1/(x(x + 1)) = 1/x − 1/(x + 1). Integral = [ln x − ln(x + 1)]₁² = ln(2/3) − ln(1/2) = ln(4/3) ≈ %.4f." % math.log(4 / 3), tol=0.0006)
    k = r.randint(2, 6)
    return nat(r, "Evaluate ∫₁^(e^%d) (ln x)/x dx." % k, k * k / 2, "Substitute u = ln x, du = dx/x, limits 0 → %d: ∫₀^%d u du = %d²/2 = %s." % (k, k, k, fm(F(k * k, 2))), tol=0.001)


# ---------------------------------------------------------------- probability / statistics
@gen(S, RV, "Random variables", n=70, diff="medium")
def rv_basic(r):
    kind = r.choice(["k", "cdf", "mean", "pdfk", "pdfp", "median"])
    if kind == "k":
        n = r.randint(3, 5)
        w = list(range(1, n + 1))
        return nat(r, "A random variable takes values 1, …, %d with P(X = x) = kx. Find k (4 decimals)." % n, round(1 / sum(w), 4), "Probabilities sum to 1: k(1 + … + %d) = %dk = 1, so k = 1/%d." % (n, sum(w), sum(w)), tol=0.0006)
    if kind == "cdf":
        p = [F(r.randint(1, 4)) for _ in range(4)]
        s = sum(p); p = [x / s for x in p]
        k = r.randint(1, 3)
        v = sum(p[:k])
        return nat(r, "X takes values 1, 2, 3, 4 with probabilities %s. Find F(%d) = P(X ≤ %d) (3 decimals)." % (J([fm(x) for x in p]), k, k), round(float(v), 3), "Add the probabilities of 1 … %d: %s." % (k, fm(v)), tol=0.002)
    if kind == "mean":
        p = [F(r.randint(1, 4)) for _ in range(3)]
        s = sum(p); p = [x / s for x in p]
        vals = r.sample(range(-2, 7), 3)
        m = sum(a * b for a, b in zip(vals, p))
        return nat(r, "X takes values %s with probabilities %s. Find E[X] (3 decimals)." % (J(vals), J([fm(x) for x in p])), round(float(m), 3), "E[X] = Σ x·p(x) = %s = %s." % (" + ".join("%d·%s" % (a, fm(b)) for a, b in zip(vals, p)), fm(m)), tol=0.002)
    if kind == "pdfk":
        n = r.randint(1, 3)
        return nat(r, "f(x) = c·x^%d on [0, 1] (zero elsewhere) is a probability density. Find c." % n, n + 1, "∫₀¹ c x^%d dx = c/%d = 1, so c = %d." % (n, n + 1, n + 1))
    if kind == "pdfp":
        a = r.choice([F(1, 2), F(1, 3), F(1, 4), F(3, 4)])
        v = a * a
        return nat(r, "X has density f(x) = 2x on [0, 1]. Find P(X ≤ %s) (4 decimals)." % fm(a), round(float(v), 4), "F(x) = ∫₀ˣ 2t dt = x², so P(X ≤ %s) = %s." % (fm(a), fm(v)), tol=0.0006)
    lam = r.choice([1, 2, 3, 4])
    return nat(r, "X is exponential with rate λ = %d. Find its median (4 decimals)." % lam, round(math.log(2) / lam, 4), "Solve 1 − e^(−λm) = 1/2: m = ln 2/λ = %.4f." % (math.log(2) / lam), tol=0.0006)


def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


@gen(S, RV, "Continuous distributions", n=70, diff="medium")
def rv_cont(r):
    kind = r.choice(["unifp", "unifmean", "expp", "memo", "normz", "normp", "normrule"])
    if kind == "unifp":
        a, b = r.randint(0, 4), r.randint(8, 16)
        c, d = sorted(r.sample(range(a, b + 1), 2))
        return nat(r, "X is uniform on [%d, %d]. Find P(%d ≤ X ≤ %d) (4 decimals)." % (a, b, c, d), round((d - c) / (b - a), 4), "Length ratio: (%d − %d)/(%d − %d) = %s." % (d, c, b, a, fm(F(d - c, b - a))), tol=0.0006)
    if kind == "unifmean":
        a, b = r.randint(0, 5), r.randint(8, 20)
        return nat(r, "X is uniform on [%d, %d]. Find E[X²] (3 decimals)." % (a, b), round((a * a + a * b + b * b) / 3, 3), "E[X²] = Var + mean² = (b − a)²/12 + ((a + b)/2)² = (a² + ab + b²)/3 = %.3f." % ((a * a + a * b + b * b) / 3), tol=0.002)
    if kind == "expp":
        lam, t = r.choice([F(1, 2), F(1), F(2), F(1, 3)]), r.randint(1, 3)
        v = math.exp(-float(lam) * t)
        return nat(r, "X is exponential with rate λ = %s. Find P(X > %d) (4 decimals)." % (fm(lam), t), round(v, 4), "P(X > t) = e^(−λt) = e^(−%s) ≈ %.4f." % (fm(lam * t), v), tol=0.0006)
    if kind == "memo":
        lam, s, t = r.choice([F(1, 2), F(1), F(1, 4)]), r.randint(1, 5), r.randint(1, 3)
        v = math.exp(-float(lam) * t)
        return nat(r, "A bulb's life is exponential with rate %s per year. Given it has already lasted %d years, what is the probability (4 decimals) it lasts at least %d more?" % (fm(lam), s, t), round(v, 4),
                   "Memoryless: P(X > s + t | X > s) = P(X > t) = e^(−%s) ≈ %.4f; the %d years already survived do not matter." % (fm(lam * t), v, s), tol=0.0006)
    if kind == "normz":
        mu, sd = r.randint(40, 80), r.choice([2, 4, 5, 10])
        k = r.choice([-2, -1, 1, 2, 3])
        x = mu + k * sd
        return nat(r, "X ~ N(μ = %d, σ = %d). What is the z-score of x = %d?" % (mu, sd, x), k, "z = (x − μ)/σ = (%d − %d)/%d = %d." % (x, mu, sd, k))
    if kind == "normp":
        mu, sd = r.randint(40, 80), r.choice([2, 4, 5, 10])
        k = r.choice([1, 2])
        v = phi(k) - phi(-k)
        return nat(r, "X ~ N(%d, %d²). Using Φ(1) = 0.8413 and Φ(2) = 0.9772, find P(%d < X < %d) (4 decimals)." % (mu, sd, mu - k * sd, mu + k * sd), round(2 * [0, 0.8413, 0.9772][k] - 1, 4),
                   "Standardise: P(−%d < Z < %d) = 2Φ(%d) − 1 = %.4f." % (k, k, k, 2 * [0, 0.8413, 0.9772][k] - 1), tol=0.0006)
    return mcq(r, "For a normal distribution, approximately what fraction of values lie within 2 standard deviations of the mean?", "95%", ["68%", "99.7%", "50%"],
               "The 68–95–99.7 rule: about 68% within 1σ, 95% within 2σ, 99.7% within 3σ.")


@gen(S, RV, "Descriptive statistics", n=70, diff="easy")
def rv_stats(r):
    data = [r.randint(1, 20) for _ in range(r.choice([5, 6, 7, 8]))]
    s = sorted(data)
    n = len(s)
    mean = F(sum(s), n)
    med = F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)
    kind = r.choice(["mean", "median", "mode", "var", "sd", "range", "shift"])
    show = J(data)
    if kind == "mean":
        return nat(r, "Find the mean of %s (3 decimals)." % show, round(float(mean), 3), "Sum %d divided by %d = %s." % (sum(s), n, fm(mean)), tol=0.002)
    if kind == "median":
        return nat(r, "Find the median of %s." % show, float(med), "Sorted: %s. %s" % (J(s), "Odd count: the middle value %s." % fm(med) if n % 2 else "Even count: average of the two middle values = %s." % fm(med)), tol=0.001)
    if kind == "mode":
        c = Counter(data)
        top = max(c.values())
        if top == 1 or list(c.values()).count(top) > 1:
            raise Skip()
        m = [k for k, v in c.items() if v == top][0]
        return nat(r, "Find the mode of %s." % show, m, "The value that occurs most often: %d (%d times)." % (m, top))
    var = sum((F(x) - mean) ** 2 for x in s) / n
    if kind == "var":
        return nat(r, "Find the (population) variance of %s (3 decimals)." % show, round(float(var), 3), "Mean = %s. Variance = average squared deviation = Σ(x − x̄)²/n = %s ≈ %.3f. (Equivalently mean of squares − square of mean.)" % (fm(mean), fm(var), float(var)), tol=0.002)
    if kind == "sd":
        return nat(r, "Find the (population) standard deviation of %s (3 decimals)." % show, round(math.sqrt(float(var)), 3), "Variance = %s, standard deviation = √%s ≈ %.3f." % (fm(var), fm(var), math.sqrt(float(var))), tol=0.002)
    if kind == "range":
        return nat(r, "Find the range of %s." % show, s[-1] - s[0], "Maximum − minimum = %d − %d = %d." % (s[-1], s[0], s[-1] - s[0]))
    a, b = r.randint(2, 4), r.randint(1, 10)
    return nat(r, "A data set has standard deviation %d. Every value is multiplied by %d and then %d is added. What is the new standard deviation?" % (n, a, b), a * n,
               "Adding a constant shifts every value and leaves the spread unchanged; multiplying by %d multiplies the standard deviation by %d: %d·%d = %d." % (a, a, a, n, a * n))
