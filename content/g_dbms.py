"""Databases — parametric generators (SQL answers by executing in SQLite; FD / schedule logic by algorithm)."""
import itertools
import math
import sqlite3

from content.kit import *

S = "DBMS"
ER, RA, SQL, FD, IX, TX = ("ER Model", "Relational Algebra & Calculus", "SQL", "Functional Dependencies & Normalization", "Indexing & File Organization", "Transactions & Concurrency")


# ---------------- ER ----------------
@gen(S, ER, "ER to relational", n=70, diff="medium")
def er_tables(r):
    ents = r.randint(3, 7)
    mn, one_n, one_one, mv, weak = r.randint(0, 3), r.randint(0, 3), r.randint(0, 2), r.randint(0, 2), r.randint(0, 2)
    ents = max(ents, weak + 1)
    tables = ents + mn + mv
    desc = ["%d strong/weak entity sets in total (%d of them are weak entities identified by an owner through a many-to-one identifying relationship)" % (ents, weak)]
    if mn: desc.append("%d many-to-many relationship set(s)" % mn)
    if one_n: desc.append("%d one-to-many relationship set(s) (merged into the 'many' side)" % one_n)
    if one_one: desc.append("%d one-to-one relationship set(s) (merged into one side)" % one_one)
    if mv: desc.append("%d multivalued attribute(s)" % mv)
    return nat(r, "An ER diagram has " + "; ".join(desc) + ". Using the standard mapping rules (one table per entity set, one per many-to-many relationship and one per multivalued attribute; 1:N and 1:1 relationships and identifying relationships are folded into existing tables), the minimum number of relational tables required is", tables,
               "%d entities + %d M:N + %d multivalued = %d." % (ents, mn, mv, tables))


@gen(S, ER, "Cardinality", n=60, diff="easy")
def er_card(r):
    m, n = r.randint(3, 25), r.randint(3, 25)
    kind = r.choice(["mn", "1n", "11", "min_total", "key"])
    if kind == "mn": return nat(r, "Entity set A has %d instances and B has %d instances. What is the maximum number of relationship instances in a many-to-many relationship between A and B?" % (m, n), m * n, "m × n.")
    if kind == "1n": return nat(r, "A has %d instances and B has %d instances. The relationship is one-to-many from A (one) to B (many). What is the maximum number of relationship instances?" % (m, n), n, "Each B instance participates in at most one relationship instance.")
    if kind == "11": return nat(r, "A has %d instances and B has %d instances; relationship A–B is one-to-one. Maximum number of relationship instances?" % (m, n), min(m, n), "min(m, n).")
    if kind == "min_total": return nat(r, "A has %d instances, B has %d instances. A–B is many-to-one (many A to one B) with TOTAL participation of A. Minimum number of relationship instances?" % (m, n), m, "Every A instance participates at least once.")
    return mcq(r, "In an ER diagram, a weak entity set", "has no key of its own and depends on an owner entity set via an identifying relationship", ["always has a composite key attribute", "cannot participate in relationships", "must have partial participation in its identifying relationship"], "Weak entities are identified by the owner's key plus a partial key (discriminator).")


# ---------------- relational algebra (on small relations) ----------------
def rel(r, n, dom, cols=2):
    return sorted({tuple(r.randint(1, dom) for _ in range(cols)) for _ in range(n)})


def show(name, cols, t):
    return "%s(%s) = {%s}" % (name, ",".join(cols), ", ".join("(%s)" % ",".join(map(str, x)) for x in t))


@gen(S, RA, "Operator results", n=100, diff="medium")
def ra_eval(r):
    R = rel(r, r.randint(4, 7), 4)
    Sx = rel(r, r.randint(3, 6), 4)
    kind = r.choice(["join", "union", "diff", "inter", "proj", "sel", "cross", "semi", "div"])
    ctx = show("R", "AB", R) + "\n" + show("S", "BC", Sx)
    if kind == "join":
        v = sum(1 for a, b in R for b2, c in Sx if b == b2)
        return nat(r, ctx + "\nHow many tuples are in the natural join R ⋈ S?", v, "Match on B.")
    if kind == "cross": return nat(r, ctx + "\nHow many tuples are in R × S?", len(R) * len(Sx), "|R|·|S|.")
    if kind == "proj": return nat(r, ctx + "\nHow many tuples are in π_B(R) (set semantics)?", len({b for a, b in R}), "Distinct B values.")
    if kind == "sel": return nat(r, ctx + "\nHow many tuples are in σ_{A < B}(R)?", sum(1 for a, b in R if a < b), "Count tuples with A < B.")
    if kind == "semi":
        bs = {b for b, c in Sx}
        return nat(r, ctx + "\nHow many tuples are in the semijoin R ⋉ S (tuples of R that join with some tuple of S)?", sum(1 for a, b in R if b in bs), "Tuples of R whose B appears in S.")
    if kind == "div":
        A = sorted({a for a, b in R})
        Bs = {b for b, c in Sx}
        res = [a for a in A if Bs <= {b for a2, b in R if a2 == a}]
        S1 = sorted({(b,) for b, c in Sx})
        return nat(r, show("R", "AB", R) + "\n" + show("S", "B", S1) + "\nHow many tuples are in R ÷ S?", len([a for a in A if {x[0] for x in S1} <= {b for a2, b in R if a2 == a}]), "Values of A related in R to every B of S.")
    R2 = rel(r, r.randint(3, 6), 4)
    ctx = show("R", "AB", R) + "\n" + show("T", "AB", R2)
    return nat(r, ctx + "\nHow many tuples are in %s?" % {"union": "R ∪ T", "diff": "R − T", "inter": "R ∩ T"}[kind], len({"union": set(R) | set(R2), "diff": set(R) - set(R2), "inter": set(R) & set(R2)}[kind]), "Set operations on the tuples.")


@gen(S, RA, "Size bounds", n=80, diff="easy")
def ra_bounds(r):
    m, n = r.randint(5, 60), r.randint(5, 60)
    kind = r.choice(["cross", "join_max", "join_fk", "union_max", "union_min", "inter_max", "diff_min", "diff_max", "proj_max", "sel_max"])
    if kind == "cross": return nat(r, "|R| = %d, |S| = %d (no common attributes). Number of tuples in R × S?" % (m, n), m * n, "m·n.")
    if kind == "join_max": return nat(r, "R has %d tuples, S has %d tuples and they share one attribute. Maximum number of tuples in R ⋈ S?" % (m, n), m * n, "All tuples may share the same join value.")
    if kind == "join_fk": return nat(r, "R(A,B) has %d tuples with B a foreign key referencing the primary key B of S (which has %d tuples). Number of tuples in R ⋈ S?" % (m, n), m, "Each R tuple matches exactly one S tuple.")
    if kind == "union_max": return nat(r, "|R| = %d, |S| = %d (union-compatible). Maximum |R ∪ S|?" % (m, n), m + n, "No overlap.")
    if kind == "union_min": return nat(r, "|R| = %d, |S| = %d (union-compatible). Minimum |R ∪ S|?" % (m, n), max(m, n), "Smaller set contained in the larger.")
    if kind == "inter_max": return nat(r, "|R| = %d, |S| = %d (union-compatible). Maximum |R ∩ S|?" % (m, n), min(m, n), "Smaller set fully contained.")
    if kind == "diff_min": return nat(r, "|R| = %d, |S| = %d (union-compatible). Minimum |R − S|?" % (m, n), max(0, m - n), "At most n tuples removed.")
    if kind == "diff_max": return nat(r, "|R| = %d, |S| = %d (union-compatible). Maximum |R − S|?" % (m, n), m, "No tuple in common.")
    if kind == "proj_max": return nat(r, "R has %d tuples. Maximum number of tuples in π_A(R) (set semantics)?" % m, m, "All A values distinct.")
    return nat(r, "R has %d tuples. Minimum number of tuples in σ_{cond}(R) over all possible conditions?" % m, 0, "A condition may select nothing.")


# ---------------- SQL on sqlite ----------------
def make_db(r):
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE R(a INT, b INT, c INT)")
    c.execute("CREATE TABLE S(b INT, d INT)")
    nr, ns = r.randint(5, 8), r.randint(3, 6)
    Rrows = [(i + 1, r.randint(1, 4), r.choice([None, r.randint(1, 9), r.randint(1, 9)])) for i in range(nr)]
    Srows = [(r.choice([1, 2, 3, 5, 6, None]) if r.random() < 0.9 else None, r.randint(1, 9)) for _ in range(ns)]
    c.executemany("INSERT INTO R VALUES(?,?,?)", Rrows)
    c.executemany("INSERT INTO S VALUES(?,?)", Srows)
    return c, Rrows, Srows


def tbl(name, cols, rows):
    return "%s(%s): %s" % (name, ", ".join(cols), "  ".join("(%s)" % ",".join("NULL" if v is None else str(v) for v in x) for x in rows))


QUERIES = [
    ("SELECT COUNT(*) FROM R WHERE c > 4", "WHERE comparisons with NULL are unknown ⇒ rows with c = NULL are dropped.", "easy"),
    ("SELECT COUNT(c) FROM R", "COUNT(col) ignores NULLs.", "easy"),
    ("SELECT COUNT(*) FROM R", "COUNT(*) counts all rows.", "easy"),
    ("SELECT COUNT(DISTINCT b) FROM R", "Distinct non-NULL b values.", "easy"),
    ("SELECT SUM(c) FROM R", "SUM ignores NULLs.", "easy"),
    ("SELECT COUNT(*) FROM R, S WHERE R.b = S.b", "Equi-join on b (NULL never equals NULL).", "medium"),
    ("SELECT COUNT(*) FROM R LEFT JOIN S ON R.b = S.b", "Left join keeps unmatched R rows once.", "medium"),
    ("SELECT COUNT(*) FROM R WHERE b IN (SELECT b FROM S)", "Rows of R whose b appears in S.", "medium"),
    ("SELECT COUNT(*) FROM R WHERE b NOT IN (SELECT b FROM S)", "If S.b contains NULL, NOT IN is never true.", "hard"),
    ("SELECT COUNT(*) FROM R WHERE NOT EXISTS (SELECT 1 FROM S WHERE S.b = R.b)", "NOT EXISTS is not affected by NULLs in S.", "medium"),
    ("SELECT COUNT(*) FROM (SELECT b FROM R GROUP BY b HAVING COUNT(*) > 1)", "Groups of b with more than one row.", "medium"),
    ("SELECT COUNT(*) FROM (SELECT b FROM R UNION SELECT b FROM S)", "UNION removes duplicates (NULLs are equal for duplicate elimination).", "hard"),
    ("SELECT COUNT(*) FROM (SELECT b FROM R UNION ALL SELECT b FROM S)", "UNION ALL keeps duplicates.", "easy"),
    ("SELECT COUNT(*) FROM (SELECT b FROM R INTERSECT SELECT b FROM S)", "Distinct common b values.", "medium"),
    ("SELECT COUNT(*) FROM (SELECT b FROM R EXCEPT SELECT b FROM S)", "Distinct b in R but not in S.", "medium"),
    ("SELECT MAX(a) FROM R WHERE b = (SELECT MIN(b) FROM S)", "Scalar subquery then filter.", "medium"),
    ("SELECT COUNT(*) FROM R WHERE c IS NULL", "IS NULL counts missing values.", "easy"),
    ("SELECT COUNT(*) FROM R WHERE c = c", "c = c is unknown for NULL.", "medium"),
    ("SELECT COUNT(*) FROM R r1 WHERE c > (SELECT AVG(c) FROM R r2 WHERE r2.b = r1.b)", "Correlated subquery: compare with the group average (NULL ignored).", "hard"),
    ("SELECT COUNT(*) FROM R r1, R r2 WHERE r1.b = r2.b AND r1.a < r2.a", "Self-join counting ordered pairs in the same b group.", "hard"),
    ("SELECT COUNT(*) FROM R WHERE b > 1 AND (c < 5 OR c >= 5)", "OR over a NULL c is unknown.", "hard"),
]


@gen(S, SQL, "Query results", n=180, diff="medium")
def sql_run(r):
    c, Rr, Sr = make_db(r)
    q, why, d = r.choice(QUERIES)
    v = c.execute(q).fetchone()[0]
    if v is None: v = 0
    return nat(r, tbl("R", "abc", Rr) + "\n" + tbl("S", "bd", Sr) + "\n(NULL = missing value)\n```sql\n%s;\n```\nWhat is the (single) value returned?" % q, v, why)


@gen(S, SQL, "Query results", n=120, diff="hard", marks=2)
def sql_run_h(r):
    c, Rr, Sr = make_db(r)
    q, why, d = r.choice([x for x in QUERIES if x[2] != "easy"])
    v = c.execute(q).fetchone()[0]
    if v is None: v = 0
    return nat(r, tbl("R", "abc", Rr) + "\n" + tbl("S", "bd", Sr) + "\n(NULL = missing value)\n```sql\n%s;\n```\nWhat is the value returned?" % q, v, why)


@gen(S, SQL, "Aggregates", n=60, diff="easy")
def sql_agg(r):
    vals = [r.choice([None, r.randint(1, 20)]) for _ in range(r.randint(5, 8))]
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE T(x INT)")
    c.executemany("INSERT INTO T VALUES(?)", [(v,) for v in vals])
    agg = r.choice(["AVG(x)", "SUM(x)", "COUNT(x)", "COUNT(*)", "MIN(x)", "MAX(x)", "SUM(x)/COUNT(*)"])
    v = c.execute("SELECT %s FROM T" % agg).fetchone()[0]
    if v is None: raise Skip()
    return nat(r, "Table T has a single column x holding %s (NULL = missing). What does SELECT %s FROM T return? (integer division wherever both operands are integers; give AVG to 2 decimals)" % (["NULL" if v2 is None else v2 for v2 in vals], agg), round(float(v), 2), "SQL aggregates ignore NULLs (except COUNT(*)).", tol=0.01)


# ---------------- FDs & normalization ----------------
def closure(attrs, fds):
    c = set(attrs)
    ch = True
    while ch:
        ch = False
        for l, rr in fds:
            if set(l) <= c and not set(rr) <= c:
                c |= set(rr); ch = True
    return c


def candidate_keys(U, fds):
    keys = []
    for k in range(1, len(U) + 1):
        for sub in itertools.combinations(sorted(U), k):
            if closure(sub, fds) >= set(U) and not any(set(x) <= set(sub) for x in keys):
                keys.append(sub)
    return keys


def highest_nf(U, fds):
    keys = candidate_keys(U, fds)
    prime = {a for k in keys for a in k}
    nonprime = set(U) - prime
    def is_super(X): return closure(X, fds) >= set(U)
    nontrivial = [(l, rr) for l, rr in fds if not set(rr) <= set(l)]
    if all(is_super(l) for l, _ in nontrivial): return "BCNF"
    if all(is_super(l) or set(rr) - set(l) <= prime for l, rr in nontrivial): return "3NF"
    for k in keys:
        for n in range(1, len(k)):
            for X in itertools.combinations(k, n):
                if (closure(X, fds) - set(X)) & nonprime: return "1NF"
    return "2NF"


def fdstr(fds): return ", ".join("%s → %s" % ("".join(l), "".join(rr)) for l, rr in fds)


def rand_fds(r, U, k):
    fds = set()
    while len(fds) < k:
        l = tuple(sorted(r.sample(U, r.choice([1, 1, 2]))))
        rhs = r.choice([a for a in U if a not in l])
        fds.add((l, (rhs,)))
    return sorted(fds)


@gen(S, FD, "Closure & keys", n=120, diff="medium")
def fd_keys(r):
    U = list("ABCDE"[:r.choice([4, 5])])
    fds = rand_fds(r, U, r.randint(3, 5))
    keys = candidate_keys(U, fds)
    kind = r.choice(["nkeys", "closure", "super", "primes", "keysize"])
    ctx = "Relation R(%s) with functional dependencies { %s }." % (",".join(U), fdstr(fds))
    if kind == "nkeys": return nat(r, ctx + " How many candidate keys does R have?", len(keys), "Candidate keys: %s." % ", ".join("".join(k) for k in keys))
    if kind == "closure":
        X = tuple(sorted(r.sample(U, r.choice([1, 2]))))
        return nat(r, ctx + " What is the number of attributes in the closure (%s)⁺?" % "".join(X), len(closure(X, fds)), "(%s)⁺ = %s." % ("".join(X), "".join(sorted(closure(X, fds)))))
    if kind == "super":
        sup = sum(1 for n in range(1, len(U) + 1) for s in itertools.combinations(U, n) if closure(s, fds) >= set(U))
        return nat(r, ctx + " How many superkeys does R have (non-empty attribute subsets that determine all attributes)?", sup, "Count subsets whose closure is all of R.")
    if kind == "primes": return nat(r, ctx + " How many prime attributes (attributes that belong to some candidate key) does R have?", len({a for k in keys for a in k}), "Candidate keys: %s." % ", ".join("".join(k) for k in keys))
    return nat(r, ctx + " What is the size (number of attributes) of the smallest candidate key?", min(len(k) for k in keys), "Candidate keys: %s." % ", ".join("".join(k) for k in keys))


@gen(S, FD, "Normal forms", n=120, diff="hard", marks=2)
def fd_nf(r):
    U = list("ABCDE"[:r.choice([4, 5])])
    fds = rand_fds(r, U, r.randint(2, 4))
    nf = highest_nf(U, fds)
    return mcq(r, "Relation R(%s) with FDs { %s }. The highest normal form R satisfies is" % (",".join(U), fdstr(fds)), nf, [x for x in ["1NF", "2NF", "3NF", "BCNF"] if x != nf], "Candidate keys: %s." % ", ".join("".join(k) for k in candidate_keys(U, fds)))


@gen(S, FD, "Decomposition", n=100, diff="hard", marks=2)
def fd_decomp(r):
    U = list("ABCDE"[:r.choice([4, 5])])
    fds = rand_fds(r, U, r.randint(3, 4))
    cut = r.sample(U, r.randint(2, len(U) - 1))
    R1 = sorted(set(cut) | set(r.sample(U, 1)))
    R2 = sorted((set(U) - set(R1)) | set(r.sample(R1, 1)))
    if set(R1) | set(R2) != set(U) or set(R1) <= set(R2) or set(R2) <= set(R1): raise Skip()
    inter = set(R1) & set(R2)
    lossless = closure(inter, fds) >= set(R1) or closure(inter, fds) >= set(R2)
    kind = r.choice(["lossless", "preserve"])
    ctx = "R(%s) with FDs { %s } is decomposed into R1(%s) and R2(%s)." % (",".join(U), fdstr(fds), ",".join(R1), ",".join(R2))
    if kind == "lossless": return mcq(r, ctx + " The decomposition is", "lossless-join" if lossless else "lossy", ["lossy" if lossless else "lossless-join", "lossless-join only if R1 ∩ R2 is empty", "not decidable from FDs"], "R1 ∩ R2 = {%s}; its closure is %s." % ("".join(sorted(inter)), "".join(sorted(closure(inter, fds)))))
    pres = True
    for l, rr in fds:
        res = set(l)
        ch = True
        while ch:
            ch = False
            for Ri in (R1, R2):
                t = closure(res & set(Ri), fds) & set(Ri)
                if not t <= res: res |= t; ch = True
        if not set(rr) <= res: pres = False
    return mcq(r, ctx + " The decomposition is", "dependency preserving" if pres else "not dependency preserving", ["not dependency preserving" if pres else "dependency preserving", "dependency preserving only if lossless", "dependency preserving only for BCNF"], "Test each FD with the projection-closure algorithm.")


@gen(S, FD, "FD theory", n=40, diff="easy")
def fd_theory(r):
    n = r.randint(3, 8)
    kind = r.choice(["armstrong", "keycount", "bcnf_bin", "max_keys", "trivial"])
    if kind == "armstrong": return mcq(r, "Which of the following is NOT an Armstrong axiom?", "Decomposition (X → YZ implies X → Y)", ["Reflexivity", "Augmentation", "Transitivity"], "Decomposition is a derived rule, not a primitive axiom.")
    if kind == "keycount": return nat(r, "R has %d attributes and exactly one candidate key consisting of ALL attributes. How many superkeys does R have?" % n, 1, "Only the full attribute set is a superkey.")
    if kind == "bcnf_bin": return mcq(r, "Every relation with only two attributes is in", "BCNF", ["1NF only", "2NF but not 3NF", "3NF but not BCNF"], "With two attributes no nontrivial FD can violate BCNF.")
    if kind == "max_keys": return nat(r, "Maximum number of candidate keys possible in a relation with %d attributes?" % n, math.comb(n, n // 2), "Keys form an antichain: C(n, ⌊n/2⌋).")
    return nat(r, "R has %d attributes with no nontrivial FDs. How many candidate keys does it have?" % n, 1, "The only key is the set of all attributes.")


# ---------------- indexing & file organization ----------------
@gen(S, IX, "Blocks & index sizes", n=100, diff="medium")
def ix_blocks(r):
    B, rec, key, ptr, N = r.choice([512, 1024, 2048, 4096]), r.choice([50, 100, 128, 200]), r.choice([4, 8, 10]), r.choice([4, 6, 8]), r.choice([10000, 30000, 100000, 500000])
    bf = B // rec
    blocks = math.ceil(N / bf)
    kind = r.choice(["bf", "blocks", "binsearch", "dense", "sparse", "levels"])
    ctx = "Block size %d B, record size %d B (unspanned), %d records" % (B, rec, N)
    if kind == "bf": return nat(r, ctx.split(",")[0] + ", record size %d B (unspanned). Blocking factor?" % rec, bf, "⌊B/R⌋.")
    if kind == "blocks": return nat(r, ctx + ". Number of data blocks needed?", blocks, "⌈N / bf⌉ with bf = %d." % bf)
    if kind == "binsearch": return nat(r, ctx + ". Worst-case block accesses to find a record by binary search on the sorted key file?", math.ceil(math.log2(blocks)), "⌈log₂ b⌉ with b = %d." % blocks)
    ibf = B // (key + ptr)
    if kind == "dense": return nat(r, ctx + "; key %d B, block pointer %d B. Number of blocks in a DENSE primary index?" % (key, ptr), math.ceil(N / ibf), "Entries = N; index blocking factor = %d." % ibf)
    if kind == "sparse": return nat(r, ctx + "; key %d B, block pointer %d B. Number of blocks in a SPARSE primary index (one entry per data block)?" % (key, ptr), math.ceil(blocks / ibf), "Entries = %d; per block %d." % (blocks, ibf))
    n1 = math.ceil(blocks / ibf)
    lv, cur = 1, n1
    while cur > 1: cur = math.ceil(cur / ibf); lv += 1
    return nat(r, ctx + "; key %d B, pointer %d B. A multilevel sparse index is built until the top level fits in ONE block. How many index levels are there?" % (key, ptr), lv, "Keep dividing the entries by the index blocking factor %d." % ibf)


@gen(S, IX, "B+ trees", n=100, diff="hard", marks=2)
def ix_bplus(r):
    B, K, P, Pr = r.choice([512, 1024, 4096]), r.choice([4, 8, 10, 12]), r.choice([4, 6, 8]), r.choice([6, 8, 10])
    p = (B + K) // (P + K)          # internal node: p*P + (p-1)*K <= B
    leaf = (B - P) // (K + Pr)       # leaf: n*(K+Pr) + P <= B
    h = r.randint(2, 4)
    t = r.randint(2, 6)
    kind = r.choice(["order", "leafkeys", "leaves", "maxkeys", "btree_min", "btree_max", "fanout_keys"])
    if kind == "order": return nat(r, "A B+ tree internal node holds p tree pointers and p−1 keys. Block size %d B, key %d B, tree pointer %d B. Largest possible order p?" % (B, K, P), p, "p·P + (p−1)·K ≤ B ⇒ p = ⌊(B + K)/(P + K)⌋.")
    if kind == "leafkeys": return nat(r, "B+ tree leaf node: stores (key, record pointer) pairs and one next-leaf pointer. Block %d B, key %d B, record pointer %d B, next-leaf pointer %d B. Maximum keys per leaf?" % (B, K, Pr, P), leaf, "n·(K + Pr) + P ≤ B.")
    if kind == "leaves": return nat(r, "In a B+ tree every internal node has at most %d children. What is the maximum number of leaf nodes in a tree of height %d (root = level 0, leaves at level %d)?" % (p, h, h), p ** h, "p^h leaves.")
    if kind == "maxkeys": return nat(r, "A B-tree node can hold at most %d keys. Maximum number of keys in a B-tree of height 1 (a root and its children, root = level 0)?" % (2 * t - 1), (2 * t - 1) * (1 + 2 * t), "Root has 2t−1 keys and 2t children each with 2t−1 keys.")
    if kind == "btree_min": return nat(r, "B-tree with minimum degree t = %d and height h = %d (root at height 0). Minimum possible number of keys in the tree? (root has ≥ 1 key, every other node ≥ t − 1 keys)" % (t, h), 2 * t ** h - 1, "Min keys = 2t^h − 1.")
    if kind == "btree_max": return nat(r, "B-tree with minimum degree t = %d and height h = %d (root at height 0). Maximum possible number of keys?" % (t, h), (2 * t) ** (h + 1) - 1, "Max keys = (2t)^(h+1) − 1.")
    return nat(r, "A B+ tree internal node has order p = %d (at most %d pointers). Maximum number of keys it can hold?" % (p, p), p - 1, "p − 1 keys.")


@gen(S, IX, "Hashing & file organization", n=40, diff="easy")
def ix_file(r):
    kind = r.choice(["heap", "sorted", "hashbuckets", "ext"])
    b = r.randint(100, 5000)
    if kind == "heap": return nat(r, "A heap (unordered) file has %d blocks. Worst-case block accesses to find a record by an unindexed key?" % b, b, "Linear scan of every block.")
    if kind == "sorted": return nat(r, "A sorted file has %d blocks. Worst-case block accesses to find a record by its sort key using binary search?" % b, math.ceil(math.log2(b)), "⌈log₂ b⌉.")
    if kind == "hashbuckets":
        n, bf = r.randint(500, 5000), r.choice([5, 10, 20])
        return nat(r, "A static hash file stores %d records with %d records per bucket block. Minimum number of buckets needed (no overflow, perfectly uniform hashing)?" % (n, bf), math.ceil(n / bf), "⌈n / bf⌉.")
    d = r.randint(2, 6)
    return nat(r, "An extendible hash directory has global depth %d. How many directory entries does it contain?" % d, 2 ** d, "2^d.")


# ---------------- transactions ----------------
def gen_schedule(r, nt=3, nops=7):
    items = ["X", "Y", "Z"][:r.randint(2, 3)]
    ops = []
    for _ in range(nops):
        ops.append(("T%d" % r.randint(1, nt), r.choice("RW"), r.choice(items)))
    # commits at the end in random order
    order = ["T%d" % i for i in range(1, nt + 1)]
    r.shuffle(order)
    return ops, order


def conflict_graph(ops, nt):
    edges = set()
    for i, (t1, o1, x1) in enumerate(ops):
        for t2, o2, x2 in ops[i + 1:]:
            if t1 != t2 and x1 == x2 and "W" in (o1, o2): edges.add((t1, t2))
    return edges


def has_cycle(edges, nodes):
    adj = {n: [b for a, b in edges if a == n] for n in nodes}
    state = {}
    def dfs(u):
        state[u] = 1
        for v in adj[u]:
            if state.get(v) == 1 or (v not in state and dfs(v)): return True
        state[u] = 2
        return False
    return any(n not in state and dfs(n) for n in nodes)


def topo_count(edges, nodes):
    return sum(1 for p in itertools.permutations(nodes) if all(p.index(a) < p.index(b) for a, b in edges))


def with_commits(r, ops):
    last = {t: i for i, (t, o, x) in enumerate(ops)}
    full, pending = [], []
    for i, op in enumerate(ops):
        full.append(op)
        for t in sorted(last):
            if last[t] == i:
                if r.random() < 0.5: full.append((t, "C", None))
                else: pending.append(t)
    r.shuffle(pending)
    return full + [(t, "C", None) for t in pending]


def classify_full(full):
    cpos = {t: i for i, (t, o, x) in enumerate(full) if o == "C"}
    rec = aca = strict = True
    last_writer = {}
    for i, (t, o, x) in enumerate(full):
        if o == "C": continue
        w = last_writer.get(x)
        if o == "R" and w and w != t:
            if cpos[w] > cpos[t]: rec = False
            if cpos[w] > i: aca = False; strict = False
        if o == "W":
            if w and w != t and cpos[w] > i: strict = False
            last_writer[x] = t
    return "non-recoverable" if not rec else ("recoverable but not cascadeless (ACA)" if not aca else ("cascadeless (ACA) but not strict" if not strict else "strict"))


def sched_str(ops, commits=None):
    return "; ".join(("c%s" % t[1:]) if o == "C" else ("%s%s(%s)" % ("r" if o == "R" else "w", t[1:], x)) for t, o, x in ops)


@gen(S, TX, "Serializability", n=150, diff="hard", marks=2)
def tx_ser(r):
    nt = r.choice([2, 3, 3])
    ops, co = gen_schedule(r, nt, r.randint(6, 8))
    nodes = sorted({t for t, _, _ in ops})
    if len(nodes) < 2: raise Skip()
    g = conflict_graph(ops, nt)
    kind = r.choice(["cs", "conf", "serial", "prec"])
    s = sched_str(ops)
    if kind == "cs":
        cs = not has_cycle(g, nodes)
        return mcq(r, "Schedule S: %s. Is S conflict serializable?" % s, "Yes" if cs else "No", ["No" if cs else "Yes", "Yes, but only if all transactions commit", "Cannot be determined without commit order"], "Precedence graph edges: %s%s." % (sorted(g), " (acyclic)" if cs else " (has a cycle)"))
    if kind == "conf": return nat(r, "Schedule S: %s. How many distinct ordered pairs of CONFLICTING operations (different transactions, same item, at least one write) occur in S?" % s, sum(1 for i, (t1, o1, x1) in enumerate(ops) for t2, o2, x2 in ops[i + 1:] if t1 != t2 and x1 == x2 and "W" in (o1, o2)), "Count them directly.")
    if has_cycle(g, nodes): raise Skip()
    if kind == "serial": return nat(r, "Schedule S: %s. S is conflict serializable. How many serial schedules are conflict-equivalent to S?" % s, topo_count(g, nodes), "Number of topological orders of the precedence graph %s." % sorted(g))
    return nat(r, "Schedule S: %s. How many edges does the precedence (serialization) graph of S have?" % s, len(g), "Edges: %s." % sorted(g))


@gen(S, TX, "Recoverability", n=150, diff="hard", marks=2)
def tx_rec(r):
    ops, co = gen_schedule(r, 3, r.randint(5, 7))
    if len({t for t, _, _ in ops}) < 2: raise Skip()
    full = with_commits(r, ops)
    cls = classify_full(full)
    opts = ["non-recoverable", "recoverable but not cascadeless (ACA)", "cascadeless (ACA) but not strict", "strict"]
    return mcq(r, "Schedule S: %s  (r = read, w = write, c = commit). The strongest property S satisfies is" % sched_str(full), cls, [o for o in opts if o != cls],
               "Check every read/write of data written by another still-uncommitted transaction against the commit positions.")


def timestamp_aborts(ops):
    rts, wts, dead = {}, {}, set()
    ts = {t: int(t[1:]) for t, _, _ in ops}
    for t, o, x in ops:
        if t in dead: continue
        if o == "R":
            if ts[t] < wts.get(x, 0): dead.add(t)
            else: rts[x] = max(rts.get(x, 0), ts[t])
        else:
            if ts[t] < rts.get(x, 0) or ts[t] < wts.get(x, 0): dead.add(t)
            else: wts[x] = ts[t]
    return len(dead)


@gen(S, TX, "Timestamp ordering", n=100, diff="hard", marks=2)
def tx_ts(r):
    ops, _ = gen_schedule(r, 3, r.randint(7, 9))
    if len({t for t, _, _ in ops}) < 3: raise Skip()
    return nat(r, "Basic timestamp ordering is used with TS(T1)=1, TS(T2)=2, TS(T3)=3. Schedule: %s. (An aborted transaction's remaining operations are ignored; no restart.) How many transactions are aborted?" % sched_str(ops), timestamp_aborts(ops),
               "Apply the read/write timestamp rules (reject a read if TS < W-ts; reject a write if TS < R-ts or W-ts).")


@gen(S, TX, "Counting schedules", n=60, diff="medium")
def tx_count(r):
    ns = [r.randint(2, 5) for _ in range(r.choice([2, 2, 3]))]
    kind = r.choice(["all", "serial"])
    if kind == "all":
        tot = math.factorial(sum(ns)) // math.prod(math.factorial(x) for x in ns)
        return nat(r, "Transactions have %s operations respectively. How many distinct schedules (interleavings preserving each transaction's own order) exist?" % ns, tot, "Multinomial coefficient (Σn)! / Πnᵢ!.")
    return nat(r, "%d transactions are executed. How many distinct SERIAL schedules exist?" % len(ns), math.factorial(len(ns)), "k!.")


@gen(S, TX, "Concurrency facts", n=30, diff="easy")
def tx_facts(r):
    return r.choice([
        mcq(r, "The ACID property that ensures a committed transaction's effects survive failures is", "Durability", ["Atomicity", "Consistency", "Isolation"], "Durability is implemented using logs and recovery."),
        mcq(r, "Two-phase locking guarantees", "conflict serializability", ["freedom from deadlock", "cascadeless schedules", "strict schedules"], "2PL ensures conflict serializability but may deadlock; strict 2PL also gives strict schedules."),
        mcq(r, "A schedule in which a transaction reads data written by an uncommitted transaction exhibits", "a dirty read", ["a phantom read", "a lost update", "a non-repeatable read"], "Reading uncommitted data = dirty read."),
        mcq(r, "Which isolation level prevents dirty reads, non-repeatable reads and phantoms?", "Serializable", ["Read uncommitted", "Read committed", "Repeatable read (per SQL standard)"], "Only SERIALIZABLE prevents all three anomalies."),
        mcq(r, "In the wait-for graph used for deadlock detection, a deadlock exists iff", "the graph contains a cycle", ["the graph is a tree", "some node has in-degree zero", "all nodes have out-degree one"], "A cycle of waiting transactions."),
        mcq(r, "The write-ahead logging rule says", "log records must reach stable storage before the corresponding data pages", ["data pages must be written before commit", "logs are written after checkpoint only", "no log is needed under no-steal/force"], "WAL."),
    ])
