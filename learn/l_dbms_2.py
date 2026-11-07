"""DBMS part 2: functional dependencies, normalization, indexing, transactions & concurrency."""
import itertools
import math

from content import g_dbms as D
from learn import Ex, lesson

S = "DBMS"


def F(text):
    out = []
    for part in text.split(","):
        l, r = part.strip().split("->")
        out.append((tuple(l.strip()), tuple(r.strip())))
    return out


def cl(x, text):
    return "".join(sorted(D.closure(tuple(x), F(text))))


def keys(u, text):
    return ["".join(k) for k in D.candidate_keys(tuple(u), F(text))]


def equivalent(a, b):
    fa, fb = F(a), F(b)
    return all(set(r) <= D.closure(l, fa) for l, r in fb) and all(set(r) <= D.closure(l, fb) for l, r in fa)


def sched(text):
    ops = []
    for tok in text.replace(" ", "").split(";"):
        if tok[0] == "c":
            ops.append(("T" + tok[1:], "C", None))
        else:
            ops.append(("T" + tok[1], tok[0].upper(), tok[3:-1]))
    return ops


def cyc(text):
    ops = [o for o in sched(text) if o[1] != "C"]
    nodes = sorted({o[0] for o in ops})
    return D.has_cycle(D.conflict_graph(ops, len(nodes)), nodes)


def n_orders(text):
    ops = [o for o in sched(text) if o[1] != "C"]
    nodes = sorted({o[0] for o in ops})
    return D.topo_count(D.conflict_graph(ops, len(nodes)), nodes)


def preserved(parts, text):
    fds = F(text)
    for l, r in fds:
        res = set(l)
        ch = True
        while ch:
            ch = False
            for R in parts:
                t = D.closure(res & set(R), fds) & set(R)
                if not t <= res:
                    res |= t
                    ch = True
        if not set(r) <= res:
            return False
    return True


# ======================================================================================================
lesson(subject=S, chapter="Database Design", ch_no=3, no=1, slug="dbms-fds-closure", title="Functional Dependencies, Closure & Candidate Keys",
       topic="Functional Dependencies & Normalization", minutes=24, weight=5, widget="fd",
       widget_hint="Enter the attributes and FDs, then compute attribute closures, candidate keys and the highest normal form. Try each example from the lesson.",
       key="A functional dependency X → Y says that equal X-values force equal Y-values. Armstrong's axioms generate all implied FDs; the attribute closure X⁺ is the practical tool for testing implication, finding candidate keys and computing a minimal cover.",
       analogy=("🆔", "Roll number determines the rest", "If you know a student's roll number you know their name, department and hostel — the roll number *determines* them. But a name doesn't determine a roll number because two students can share a name. A functional dependency records exactly which facts follow from which."),
       sections=[
           dict(h="What a functional dependency says", md="""X → Y holds in a relation if **whenever two tuples agree on X they also agree on Y**. It is a constraint on the *schema* (all legal instances), not something you can prove from one instance — an instance can only *violate* an FD.

- **Trivial:** Y ⊆ X (e.g. AB → A). **Non-trivial:** Y ⊄ X.
- X is a **superkey** iff X → (all attributes), i.e. X⁺ = R.
- **Candidate key:** a minimal set X with X⁺ = R. Attributes in some candidate key are **prime**; the rest are **non-prime**."""),
           dict(h="Armstrong's axioms and derived rules", md="""| Rule | Statement |
|---|---|
| **Reflexivity** | Y ⊆ X ⇒ X → Y |
| **Augmentation** | X → Y ⇒ XZ → YZ |
| **Transitivity** | X → Y, Y → Z ⇒ X → Z |
| Union | X → Y, X → Z ⇒ X → YZ |
| Decomposition | X → YZ ⇒ X → Y and X → Z |
| Pseudo-transitivity | X → Y, WY → Z ⇒ WX → Z |

The axioms are **sound** (derive only implied FDs) and **complete** (derive all of them). Note: X → Y and X → Z give X → YZ, but **XY → Z does not give X → Z**."""),
           dict(h="Attribute closure and what it gives you", md="""**Algorithm for X⁺:** start with X; repeatedly add the right side of any FD whose left side is already inside the set; stop when nothing changes.

Uses:

1. **Does F imply X → Y?** Compute X⁺ and check Y ⊆ X⁺.
2. **Is X a superkey?** X⁺ = all attributes.
3. **Candidate keys:** attributes that never appear on any right side must be in every key; start from them and add attributes until the closure is everything, then check minimality.
4. **Equivalence of FD sets** F and G: each FD of G must follow from F and vice-versa.""",
                formulas=[("X → Y is implied by F  ⇔  Y ⊆ X⁺ (closure under F)", "the test for implication")]),
           dict(h="Candidate keys and minimal (canonical) cover", md="""**Finding all keys quickly:** (1) attributes appearing only on left sides (or in no FD) must be in every key; (2) attributes only on right sides are in no key; (3) check whether the core already determines everything; if not, add the other attributes in all combinations of increasing size.

**Minimal cover** Fc (an equivalent FD set that is as small as possible):

1. Make every right side a single attribute (decomposition).
2. Remove **extraneous attributes** from left sides.
3. Remove **redundant FDs** (those implied by the rest).

A relation can have several minimal covers. Example: {A→BC, B→C, A→B, AB→C} reduces to **{A→B, B→C}**.""",
                call=[("tip", "Counting keys", "If the core attributes are not a key, try adding one other attribute at a time; the number of candidate keys can be several, and every key has to be minimal.")]),
       ],
       examples=[
           Ex("Attribute closure", "R(A,B,C,D,E) with F = {A→B, BC→D, B→C, D→E}. Compute A⁺ and decide whether A is a key.",
              ["Start with {A}. A→B adds B: {A,B}.", "B→C adds C: {A,B,C}. Now BC→D adds D: {A,B,C,D}. D→E adds E.", "A⁺ = {A,B,C,D,E} = R, so A is a superkey; it is a single attribute so it is the only candidate key."],
              "A⁺ = **ABCDE**; A is a key.", verify=lambda: "A⁺ = %s; A is a key" % cl("A", "A->B, BC->D, B->C, D->E") if keys("ABCDE", "A->B, BC->D, B->C, D->E") == ["A"] else "no"),
           Ex("Candidate keys of a cyclic set", "R(A,B,C,D) with F = {AB→C, C→D, D→A}. Find all candidate keys.",
              ["B appears on no right side, so B is in every key. B⁺ = B alone, so extend.", "AB: A,B → C → D, so AB⁺ = ABCD. ✔ BC: C→D→A, so BC⁺ = ABCD ✔. BD: D→A, then AB→C, so BD⁺ = ABCD ✔.", "Candidate keys: **AB, BC, BD** (all minimal)."],
              "**AB, BC, BD**", verify=lambda: ", ".join(sorted(keys("ABCD", "AB->C, C->D, D->A")))),
           Ex("Minimal cover", "Reduce F = {A→BC, B→C, A→B, AB→C} to a minimal cover. How many FDs does it contain?",
              ["Split right sides: A→B, A→C, B→C, A→B (dup), AB→C.", "AB→C: B is extraneous since B→C already gives it; A is extraneous too once B→C is present, so AB→C is redundant. A→C follows from A→B and B→C.", "Minimal cover = {A→B, B→C}: **2** FDs."],
              "{A→B, B→C} — **2** FDs.", verify=lambda: "2" if equivalent("A->BC, B->C, A->B, AB->C", "A->B, B->C") else "no"),
           Ex("Superkey count", "R(A,B,C,D) has F = {A→B, B→C, C→D}. How many superkeys?",
              ["A⁺ = ABCD so A is the only candidate key (B, C, D cannot give A).", "Superkeys = all sets containing A: 2³ = **8**."],
              "**8**", verify=lambda: str(sum(1 for m in range(1, 16) if D.closure([ "ABCD"[i] for i in range(4) if m >> i & 1], F("A->B, B->C, C->D")) >= set("ABCD")))),
       ],
       traps=[("Closure direction", "X⁺ is computed from FDs whose **left** side is already in the set; being on a right side is not enough."),
              ("Candidate key must be minimal", "Check no proper subset of the proposed key is also a superkey."),
              ("XY → Z does not imply X → Z", "Only the reverse (decomposition) works."),
              ("FDs are schema properties", "An instance with no violations does not prove an FD, but one violation disproves it.")],
       quick=[("X⁺ equals the set of all attributes. X is a", ["candidate key always", "superkey", "foreign key", "trivial FD"], 1, "It is a superkey; a candidate key if also minimal."),
              ("Which Armstrong rule gives X → Y from Y ⊆ X?", ["Augmentation", "Transitivity", "Reflexivity", "Union"], 2, "Reflexivity."),
              ("An attribute that appears on no right side of any FD must be in", ["no candidate key", "every candidate key", "exactly one key", "only the primary key"], 1, "Nothing else can determine it."),
              ("Minimal cover step order", ["remove redundant FDs, then split", "split right sides, remove extraneous left attrs, remove redundant FDs", "union all FDs", "only remove redundant FDs"], 1, "Standard canonical-cover procedure.")],
       summary=["X → Y: equal X ⇒ equal Y; trivial when Y ⊆ X.", "Armstrong: reflexivity, augmentation, transitivity (sound and complete); union and decomposition follow.", "X⁺ by repeated expansion; F ⊨ X→Y iff Y ⊆ X⁺.",
                "Superkey: X⁺ = R; candidate key: minimal such X; prime attributes belong to some key.", "Attributes on no right side belong to every key; on no left side to no key.", "Minimal cover: single attribute RHS, no extraneous LHS attribute, no redundant FD."])


# ======================================================================================================
lesson(subject=S, chapter="Database Design", ch_no=3, no=2, slug="dbms-normal-forms", title="Normal Forms & Decomposition",
       topic="Functional Dependencies & Normalization", minutes=24, weight=5, widget="fd",
       widget_hint="Enter a schema and see its keys and highest normal form. Then check whether a two-way decomposition is lossless and dependency preserving.",
       key="Normalisation removes redundancy and update anomalies by decomposing relations. 2NF removes partial dependencies, 3NF removes transitive ones (non-key → non-key), BCNF requires every determinant to be a superkey. A good decomposition is lossless and, ideally, dependency preserving.",
       analogy=("📚", "Don't copy the same fact twice", "If every row of a table repeats a student's department head, changing the head means editing many rows — and forgetting one creates a contradiction. Normalisation moves each fact to the one place where it depends only on the key, the whole key and nothing but the key."),
       sections=[
           dict(h="Anomalies and the normal forms", md="""Redundancy causes **insertion, deletion and update anomalies**. The normal forms, each stricter than the previous:

| Form | Condition |
|---|---|
| **1NF** | all attribute values atomic (no repeating groups, no multivalued attributes) |
| **2NF** | 1NF and no **partial dependency**: no non-prime attribute depends on a *proper subset* of a candidate key |
| **3NF** | for every non-trivial X → A: X is a superkey **or A is prime** |
| **BCNF** | for every non-trivial X → A: X is a **superkey** |

BCNF ⊂ 3NF ⊂ 2NF ⊂ 1NF. A relation with only **two attributes** is always in BCNF. If all attributes are prime, it is at least 3NF. If every candidate key is a single attribute there can be no partial dependencies, so the relation is at least 2NF."""),
           dict(h="Testing the normal form", md="""1. Find all candidate keys; mark prime / non-prime attributes.
2. **BCNF test:** does every non-trivial FD have a superkey on the left? If yes → BCNF.
3. **3NF test:** otherwise, for each violating FD X → A check whether A is prime. If all are → 3NF.
4. **2NF test:** otherwise look for a non-prime attribute determined by a **proper subset of some candidate key**; if none → 2NF, else 1NF.

Remember to use the **closure** of the left side, not just the given FDs: a transitive FD may violate the form even though it was not written down.""",
                call=[("trap", "3NF vs BCNF", "3NF allows X → A when A is prime, even if X is not a superkey. That is the only gap between 3NF and BCNF.")]),
           dict(h="Lossless and dependency-preserving decomposition", md="""A decomposition of R into R₁, R₂ is **lossless-join** if R₁ ⋈ R₂ = R for every legal instance. For a binary decomposition: it is lossless iff **R₁ ∩ R₂ → R₁ or R₁ ∩ R₂ → R₂** (the common attributes form a key of one part).

It is **dependency preserving** if every FD of F can be enforced by looking at one component alone — formally, the union of the FDs projected onto the components implies F.

| Goal | Always achievable? |
|---|---|
| Lossless into **BCNF** | Yes (but may lose dependencies) |
| Lossless **and** dependency-preserving into **3NF** | **Yes** (the 3NF synthesis algorithm) |
| Lossless and dependency-preserving into BCNF | Not always |

**BCNF decomposition:** take a violating X → Y and split R into (X ∪ Y) and (R − Y); repeat. **3NF synthesis:** compute a minimal cover, make one relation per FD (merge equal left sides), add a relation with a candidate key if none contains one."""),
           dict(h="Higher normal forms and multivalued dependencies", md="""A **multivalued dependency** X →→ Y means that for each X-value the set of Y-values is independent of the other attributes. Typical case: Employee(Name, Skill, Language) where skills and languages are independent — storing every combination is redundant.

- **4NF:** BCNF plus: every non-trivial MVD X →→ Y has X a superkey.
- **5NF (PJNF):** based on join dependencies.
- Every FD is an MVD, and 4NF ⇒ BCNF.

The number of rows needed to store an employee with s skills and l languages in one table is **s × l**, versus s + l when split into two 4NF relations."""),
       ],
       examples=[
           Ex("Highest normal form", "R(A,B,C,D) with F = {AB→C, C→D, D→A}. Which is the highest normal form?",
              ["Candidate keys: AB, BC, BD (from the previous lesson), so every attribute is prime.", "3NF holds (right sides are prime). BCNF fails: C→D has C that is not a superkey.", "Highest normal form: **3NF**."],
              "**3NF**", verify=lambda: D.highest_nf(tuple("ABCD"), F("AB->C, C->D, D->A"))),
           Ex("Partial dependency", "R(A,B,C,D) with F = {AB→CD, B→C}. Highest normal form?",
              ["Key: AB (AB⁺ = ABCD; neither A nor B alone). Non-prime: C, D.", "B→C is a partial dependency (B is a proper subset of the key and C is non-prime) ⇒ not 2NF.", "Highest: **1NF**."],
              "**1NF**", verify=lambda: D.highest_nf(tuple("ABCD"), F("AB->CD, B->C"))),
           Ex("Transitive dependency", "R(A,B,C) with F = {A→B, B→C}. Highest normal form?",
              ["Key: A. No partial dependencies (key is a single attribute) ⇒ 2NF.", "B→C: B is not a superkey and C is non-prime ⇒ transitive dependency, not 3NF.", "Highest: **2NF**."],
              "**2NF**", verify=lambda: D.highest_nf(tuple("ABC"), F("A->B, B->C"))),
           Ex("Lossless but not dependency preserving", "R(A,B,C), F = {AB→C, C→B}. Decompose into R₁(A,C) and R₂(B,C). Is it lossless? Dependency preserving?",
              ["Common attribute C: C⁺ = BC ⊇ R₂, so C → R₂ ⇒ **lossless**.", "C→B lives in R₂ and is preserved. AB→C needs A and B together, but they are in different relations and cannot be re-derived from C→B, so AB→C is lost ⇒ **not preserving**."],
              "Lossless: **yes**; dependency preserving: **no**.", verify=lambda: "Lossless: %s; dependency preserving: %s" % ("yes" if D.closure("C", F("AB->C, C->B")) >= set("BC") else "no", "yes" if preserved(["AC", "BC"], "AB->C, C->B") else "no")),
       ],
       traps=[("BCNF vs 3NF", "A relation in 3NF but not BCNF always has a determinant that is not a superkey but whose right side is prime."),
              ("Lossless is about the join", "Check the common attributes; having the same attributes spread out is not enough."),
              ("Dependency preservation uses closures", "An FD may be preserved even if it is not inside a single component; test using projected closures."),
              ("2-attribute relations", "Always BCNF; one-attribute-key relations are at least 2NF.")],
       quick=[("A relation in which every non-trivial determinant is a superkey is in", ["3NF only", "BCNF", "2NF only", "1NF only"], 1, "That is BCNF."),
              ("3NF allows X → A when", ["X is a superkey only", "X is a superkey or A is prime", "always", "X is prime"], 1, "Definition of 3NF."),
              ("Which decomposition is always possible?", ["lossless + dependency-preserving BCNF", "lossless + dependency-preserving 3NF", "dependency-preserving BCNF only", "none"], 1, "3NF synthesis."),
              ("A partial dependency violates", ["1NF", "2NF", "BCNF only", "none"], 1, "2NF forbids it.")],
       summary=["1NF atomic; 2NF no partial dependency; 3NF X superkey or A prime; BCNF X superkey.", "BCNF ⊂ 3NF ⊂ 2NF ⊂ 1NF; two-attribute relations are always in BCNF.", "Binary lossless test: R₁ ∩ R₂ is a key of R₁ or R₂ (closure covers it).",
                "3NF: lossless and dependency preserving always possible; BCNF: lossless always, preserving not always.", "BCNF split: violating X → Y gives (X ∪ Y) and (R − Y).", "4NF removes multivalued dependencies."])


# ======================================================================================================
lesson(subject=S, chapter="Storage & Indexing", ch_no=4, no=1, slug="dbms-indexing", title="File Organization, Indexing & B+ Trees",
       topic="Indexing & File Organization", minutes=22, weight=4, widget="none",
       key="Records are stored in disk blocks, and the cost of a query is the number of block accesses. An index is a small sorted structure that points into the data file; the B+ tree is the standard balanced multilevel index and GATE asks you to compute block counts, search costs, order and the number of keys.",
       analogy=("📖", "The index at the back of a book", "To find a topic you don't read every page: you look it up in a short sorted index and jump to the right page. A database index does the same for table rows, and a B+ tree is a book index that stays balanced however many pages are added."),
       sections=[
           dict(h="Blocks, blocking factor and file size", md="""Disk transfers whole **blocks**. With block size B bytes and fixed record size R bytes:

- **Blocking factor** bf = ⌊B / R⌋ records per block.
- **Number of blocks** for n records = ⌈n / bf⌉.
- Unspanned records never straddle a block (the leftover space is wasted); spanned records may.

**Costs (block accesses):** linear search of a heap file ≈ b/2 on average (b worst case); binary search on a sorted file ⌈log₂ b⌉; with a multilevel index it is the number of index levels + 1.""",
                formulas=[("bf = ⌊B / R⌋;  blocks = ⌈n / bf⌉", "file size in blocks")]),
           dict(h="Types of indexes", md="""| Index | Built on | Entries |
|---|---|---|
| **Primary** | ordered file, **key** attribute | **sparse**: one entry per *block* |
| **Clustering** | ordered file, **non-key** attribute | one entry per distinct value |
| **Secondary** | unordered file, any attribute | **dense**: one entry per *record* (key) or per value |

- **Dense** index: an entry for every search-key value (every record). **Sparse**: entries only for some values (typically one per block), so it needs the file to be sorted on the key.
- A file can have **one** primary/clustering index but many secondary indexes.
- Index entry size = key size + block pointer size, so index blocks hold ⌊B / (K + P)⌋ entries.
- A **multilevel index** indexes the index itself (each level is sparse on the one below) until a single block remains."""),
           dict(h="B-trees and B+ trees", md="""A B+ tree of **order p** (internal node: at most p children) is a balanced, multi-way search tree:

- All data pointers are in the **leaves**, which are linked as a list for fast range scans; internal nodes only guide the search.
- **Internal node** holds up to p pointers and p − 1 keys: constraint **p·P + (p − 1)·K ≤ B**.
- **Leaf node** holds up to p_leaf (key, record-pointer) pairs plus one next-leaf pointer: **p_leaf·(K + P_r) + P ≤ B**.
- Every node except the root is at least half full: ⌈p/2⌉ children (internal) / ⌈(p−1)/2⌉ keys (leaf).
- All leaves are at the same depth; search, insert and delete cost O(height) = O(log_p n) block accesses.

A **B-tree** stores data pointers in internal nodes too, so a key appears only once, but its fan-out is smaller and range scans are slower — which is why databases use B+ trees. **Insertion**: insert in the leaf; if it overflows, split in half and push the middle key up. **Deletion**: remove; if underfull borrow from a sibling or merge.""",
                formulas=[("max keys of a 3-level B+ tree ≈ p² · p_leaf", "all nodes full, root + 1 internal level + leaves")]),
           dict(h="Hashing and file organisation", md="""- **Heap (unordered)** file: fast insertion, slow search. **Sorted** file: binary search, slow insertion. **Hashed** file: equality search in about 1 block, but no range queries.
- **Static hashing:** fixed number of buckets, overflow chains. **Extendible hashing:** a directory of 2^d entries (global depth d) doubles when a bucket with local depth = d overflows. **Linear hashing** splits buckets one by one in order.
- Use a **B+ tree** for range and ordering queries, a **hash index** for pure equality lookups."""),
       ],
       examples=[
           Ex("Blocks needed", "A file has 100,000 fixed records of 100 bytes in a 1024-byte block (unspanned). How many blocks does it need?",
              ["bf = ⌊1024 / 100⌋ = 10 records per block.", "Blocks = ⌈100,000 / 10⌉ = **10,000**."],
              "**10,000** blocks.", verify=lambda: str(math.ceil(100000 / (1024 // 100)))),
           Ex("Search cost with a sparse index", "Continuing: a primary (sparse) index has one entry per block, 10 bytes key + 6 bytes pointer. How many index blocks are there, and how many block accesses does a lookup need using binary search on the index?",
              ["Entries per index block = ⌊1024 / 16⌋ = 64.", "Index entries = 10,000 (one per data block) ⇒ ⌈10,000 / 64⌉ = 157 index blocks.", "Binary search on the index: ⌈log₂ 157⌉ = 8 accesses, plus 1 to read the data block = **9**. (Without an index: ⌈log₂ 10,000⌉ = 14.)"],
              "**157** index blocks; **9** accesses.", verify=lambda: "%d index blocks; %d accesses" % (math.ceil(10000 / (1024 // 16)), math.ceil(math.log2(math.ceil(10000 / 64))) + 1)),
           Ex("Order of a B+ tree", "Block size 1024 B, key 10 B, block pointer 6 B, record pointer 6 B. Find the maximum order p of an internal node and p_leaf of a leaf.",
              ["Internal: 6p + 10(p − 1) ≤ 1024 ⇒ 16p ≤ 1034 ⇒ p = **64**.", "Leaf: p_leaf·(10 + 6) + 6 ≤ 1024 ⇒ 16·p_leaf ≤ 1018 ⇒ p_leaf = **63**."],
              "p = **64**, p_leaf = **63**.", verify=lambda: "p = %d, p_leaf = %d" % (max(p for p in range(1, 200) if 6 * p + 10 * (p - 1) <= 1024), max(q for q in range(1, 200) if q * 16 + 6 <= 1024))),
           Ex("Capacity of a 3-level tree", "With p = 64 and p_leaf = 63 (all nodes full), what is the maximum number of keys in a B+ tree with root, one internal level and a leaf level?",
              ["Root has 64 children, each of those has 64 leaves ⇒ 64 × 64 = 4,096 leaves.", "Each leaf holds 63 keys ⇒ 4,096 × 63 = **258,048** keys."],
              "**258,048** keys.", verify=lambda: str(64 * 64 * 63)),
       ],
       traps=[("Dense vs sparse", "A sparse index requires the data file to be ordered on the indexed field."),
              ("Index size", "Entry size is key + pointer, not the record size."),
              ("Order definition", "Check whether a question defines order as max pointers or max keys before applying the formula."),
              ("Equality vs range", "Hash indexes cannot answer range queries; B+ trees answer both.")],
       quick=[("A primary index is", ["dense on an unordered file", "sparse on a file ordered on a key", "built on a non-key field", "always a hash"], 1, "One entry per block."),
              ("B+ trees store record pointers in", ["internal nodes only", "leaves only", "all nodes", "the root"], 1, "That's why leaves are linked."),
              ("Blocking factor equals", ["B × R", "⌊B / R⌋", "R / B", "⌈R / B⌉"], 1, "Unspanned records."),
              ("Which supports range queries well?", ["hash index", "B+ tree", "none", "heap file"], 1, "Linked leaves.")],
       summary=["bf = ⌊B/R⌋; blocks = ⌈n/bf⌉; costs counted in block accesses.", "Primary = sparse (ordered, key); clustering = ordered non-key; secondary = dense.", "Index entry = key + pointer; multilevel index until one block remains.",
                "B+ tree: data in linked leaves; internal p·P + (p−1)·K ≤ B; leaf p_leaf(K+P_r) + P ≤ B; height O(log n).", "B-tree stores data in internal nodes; B+ is better for ranges.", "Hashing: equality in ~1 access, extendible hashing doubles the directory."])


# ======================================================================================================
lesson(subject=S, chapter="Transactions", ch_no=5, no=1, slug="dbms-transactions-serializability", title="Transactions, Schedules & Serializability",
       topic="Transactions & Concurrency", minutes=24, weight=6, widget="sched",
       widget_hint="Type a schedule such as r1(A); r2(A); w1(A); w2(A); c1; c2 and the tool draws the precedence graph, tells you about cycles, serial orders and the recoverability class.",
       key="A transaction is an atomic unit of work obeying ACID. When transactions interleave, the schedule must be equivalent to some serial schedule (serializable). Conflict serializability is tested with the precedence graph; recoverability (recoverable, ACA, strict) is about commit order and dirty reads.",
       analogy=("🏦", "Two people editing one bank balance", "If two clerks read your balance, each subtract money and write it back, one update is lost. A serial schedule runs the clerks one at a time. Concurrency control lets them interleave but only in ways that give the same result as *some* one-at-a-time order."),
       sections=[
           dict(h="ACID and transaction states", md="""- **Atomicity:** all or nothing (recovery manager).
- **Consistency:** a transaction takes the database from one consistent state to another (programmer + integrity constraints).
- **Isolation:** concurrent transactions behave as if executed serially (concurrency control).
- **Durability:** committed changes survive failures (logging, recovery).

States: active → partially committed → committed; active/partially committed → failed → aborted."""),
           dict(h="Conflicts and conflict serializability", md="""Two operations **conflict** if they belong to **different transactions**, access the **same item** and **at least one is a write**: R–W, W–R and W–W conflict; R–R does not.

A schedule is **conflict serializable** iff its **precedence (serialization) graph** is acyclic: add an edge Ti → Tj when an operation of Ti conflicts with a *later* operation of Tj. A topological order of the graph is an equivalent serial schedule, and the **number of equivalent serial schedules** is the number of topological orders.

The class of conflict-serializable schedules is contained in **view serializable** schedules. A schedule that is view- but not conflict-serializable must contain a **blind write** (a write not preceded by a read of the same item in that transaction).""",
                formulas=[("CSR ⇔ precedence graph is acyclic", "test for conflict serializability")]),
           dict(h="View serializability", md="""Two schedules are **view equivalent** if (1) each transaction reads the same initial values, (2) each read sees a write by the same transaction, and (3) the same transaction performs the final write of every item. Testing view-serializability is NP-complete in general.

Strategy for GATE: first test conflict serializability; if it fails, look for blind writes. A schedule without blind writes is view serializable ⇔ conflict serializable. Known containment: **CSR ⊂ VSR ⊂ all schedules**."""),
           dict(h="Recoverability", md="""Let Ti read an item written by Tj (a *dirty read* if Tj is uncommitted).

| Class | Rule |
|---|---|
| **Recoverable** | if Ti reads from Tj then **Tj commits before Ti commits** |
| **Cascadeless (ACA)** | Ti reads only values written by **already committed** transactions (no dirty reads) |
| **Strict** | no item is read **or overwritten** until the last writer has committed or aborted |
| **Serial** | no interleaving |

Strict ⊂ ACA ⊂ Recoverable. Recoverability and serializability are **independent**: a schedule can be serializable yet not recoverable, and vice versa.""",
                call=[("trap", "Recoverable ≠ serializable", "A recoverable schedule need not be serializable, and a serializable one may be non-recoverable. Check them separately.")]),
       ],
       examples=[
           Ex("Detecting a cycle", "Is S: r1(A); r2(A); w1(A); w2(A); c1; c2 conflict serializable?",
              ["Conflicts on A: r1(A) before w2(A) gives T1 → T2; r2(A) before w1(A) gives T2 → T1.", "The graph has the cycle T1 → T2 → T1 ⇒ **not** conflict serializable."],
              "**No** (cycle T1 ⇄ T2).", verify=lambda: "No" if cyc("r1(A); r2(A); w1(A); w2(A); c1; c2") else "Yes"),
           Ex("Counting serial orders", "S: r1(A); w1(A); r2(A); w2(A); r3(B); w3(B); r2(B); w2(B). Is it conflict serializable and how many equivalent serial schedules exist?",
              ["On A: T1 conflicts with T2, so T1 → T2. On B: r3(B), w3(B) precede r2(B), w2(B), so T3 → T2.", "No cycle. T2 must come last, T1 and T3 are unconstrained ⇒ 2 topological orders: T1 T3 T2 and T3 T1 T2."],
              "Conflict serializable; **2** serial orders.", verify=lambda: "Conflict serializable; %d serial orders" % n_orders("r1(A); w1(A); r2(A); w2(A); r3(B); w3(B); r2(B); w2(B)") if not cyc("r1(A); w1(A); r2(A); w2(A); r3(B); w3(B); r2(B); w2(B)") else "not CSR"),
           Ex("Recoverability", "Classify S: w1(A); r2(A); w2(B); c2; c1.",
              ["T2 reads A written by T1, which has not committed ⇒ dirty read, so the schedule is not cascadeless.", "T2 commits before T1, but T2 read from T1 ⇒ T1 must commit first for recoverability ⇒ **non-recoverable**."],
              "**Non-recoverable**", verify=lambda: D.classify_full(sched("w1(A); r2(A); w2(B); c2; c1"))),
           Ex("Strict but not serial", "Classify S: w1(A); c1; r2(A); w2(A); c2.",
              ["Every read or write of A happens after the previous writer committed ⇒ **strict**.", "T1 completes before T2 starts, so it is in fact also serial (and thus trivially serializable)."],
              "**Strict**", verify=lambda: D.classify_full(sched("w1(A); c1; r2(A); w2(A); c2"))),
       ],
       traps=[("Direction of edges", "Edge Ti → Tj means Ti's operation came first and conflicts with Tj's later operation."),
              ("R–R is no conflict", "Only operations where at least one is a write conflict."),
              ("Commit order matters", "Recoverability depends on commit order, not just on read/write order."),
              ("Serializability ≠ recoverability", "They are independent properties.")],
       quick=[("Conflict serializability is tested by", ["the wait-for graph", "the precedence graph being acyclic", "the lock table", "the log"], 1, "Acyclic precedence graph."),
              ("ACA schedules forbid", ["blind writes", "dirty reads", "R–R conflicts", "cycles"], 1, "Reading uncommitted data."),
              ("Which pair does NOT conflict?", ["R–W", "W–R", "W–W", "R–R"], 3, "Two reads never conflict."),
              ("Strict ⊂ ACA ⊂", ["serial", "recoverable", "conflict-serializable", "view serializable"], 1, "Recoverable.")],
       summary=["ACID: atomicity (recovery), consistency, isolation (concurrency control), durability (logging).", "Conflict = different transactions + same item + at least one write.", "CSR ⇔ acyclic precedence graph; topological orders = equivalent serial schedules.",
                "CSR ⊂ VSR; a VSR-not-CSR schedule needs blind writes.", "Recoverable ⊃ ACA ⊃ strict ⊃ serial; independent of serializability.", "Dirty read = reading an uncommitted write."])


# ======================================================================================================
def to_check(sched_text, ts):
    """Basic timestamp ordering: returns the list of transactions that must abort."""
    rts, wts, aborted = {}, {}, []
    for t, o, x in sched(sched_text):
        if o == "C" or t in aborted:
            continue
        n = ts[t]
        if o == "R":
            if n < wts.get(x, 0):
                aborted.append(t)
            else:
                rts[x] = max(rts.get(x, 0), n)
        else:
            if n < rts.get(x, 0) or n < wts.get(x, 0):
                aborted.append(t)
            else:
                wts[x] = n
    return aborted


lesson(subject=S, chapter="Transactions", ch_no=5, no=2, slug="dbms-concurrency-recovery", title="Concurrency Control & Recovery",
       topic="Transactions & Concurrency", minutes=24, weight=5, widget="sched",
       widget_hint="Use the schedule tool to test whether the example schedules below are conflict serializable, and compare with what 2PL or timestamp ordering would allow.",
       key="Locking protocols (2PL, strict 2PL), timestamp ordering and deadlock prevention (wait-die, wound-wait) enforce serializability; write-ahead logging, checkpoints and ARIES (analysis, redo, undo) restore the database after a crash.",
       analogy=("🔒", "Library books and deadlines", "Two-phase locking is like a library rule: you may keep borrowing books (growing phase) but once you return one you may not borrow again (shrinking phase). Timestamp ordering is a queue ticket: the older ticket always wins and a late arrival with an older ticket is turned away."),
       sections=[
           dict(h="Locks and two-phase locking", md="""**Lock modes:** shared (S, read) and exclusive (X, write). Compatibility: S–S is compatible; S–X and X–X are not.

**Two-phase locking (2PL):** every transaction has a **growing phase** (acquire locks, no release) followed by a **shrinking phase** (release, no acquire). 2PL guarantees **conflict serializability**, with the **lock point** (end of growing phase) giving a serial order — but it does **not** prevent deadlock and may allow cascading aborts.

| Variant | Extra rule | Guarantees |
|---|---|---|
| **Basic 2PL** | two phases | conflict serializable |
| **Strict 2PL** | hold all **X** locks until commit/abort | + strict (hence cascadeless) schedules |
| **Rigorous 2PL** | hold **all** locks until commit/abort | + serial order = commit order |
| **Conservative 2PL** | acquire all locks before starting | deadlock-free |

Lock conversions: upgrade S→X only in the growing phase, downgrade in the shrinking phase."""),
           dict(h="Deadlock handling", md="""A deadlock is a cycle in the **wait-for graph**. Handling: prevention, detection (find cycles, choose a victim) or timeouts.

With timestamps (smaller = **older**):

| Scheme | Requester older than holder | Requester younger than holder |
|---|---|---|
| **Wait-die** (non-preemptive) | older waits | younger **dies** (aborts, restarts with the *same* timestamp) |
| **Wound-wait** (preemptive) | older **wounds** (aborts) the holder | younger waits |

Both avoid deadlock and starvation because aborted transactions keep their original timestamp. In wait-die older transactions wait for younger ones; in wound-wait younger ones wait for older ones."""),
           dict(h="Timestamp ordering and validation", md="""**Basic timestamp ordering:** each transaction gets a timestamp TS(T); each item X keeps R-TS(X) and W-TS(X), the largest timestamps that read/wrote it.

- **Read(X) by T:** if TS(T) < W-TS(X) ⇒ T arrived too late: **abort**. Otherwise read and set R-TS = max(R-TS, TS(T)).
- **Write(X) by T:** if TS(T) < R-TS(X) or TS(T) < W-TS(X) ⇒ **abort**. Otherwise write and set W-TS = TS(T).

Timestamp ordering produces conflict-serializable schedules in timestamp order, is deadlock-free, but may cause starvation and cascading rollbacks. The **Thomas write rule** ignores an outdated write (TS(T) < W-TS(X) but ≥ R-TS) instead of aborting, allowing some view-serializable schedules. **Optimistic (validation)** control runs read, validation and write phases and validates against concurrent transactions; **multiversion** schemes let readers read an older version."""),
           dict(h="Recovery: logging, checkpoints and ARIES", md="""**Write-ahead logging (WAL):** a log record describing a change must reach stable storage **before** the changed page does (undo info) and all of a transaction's log records must be forced **before commit** (redo info).

- **Buffer policies:** *steal* (uncommitted pages may be written to disk ⇒ need **undo**) and *no-force* (committed pages need not be flushed at commit ⇒ need **redo**). ARIES uses steal + no-force.
- **Checkpoint:** periodically write dirty pages/log markers so recovery starts later.
- **ARIES recovery:** (1) **Analysis** rebuilds the dirty-page and transaction tables from the last checkpoint, (2) **Redo** repeats history from the earliest recLSN, (3) **Undo** rolls back the losers using compensation log records (CLRs).
- **Immediate vs deferred update:** immediate update needs undo + redo; deferred (no-steal) needs only redo.""",
                call=[("tip", "Which transactions to redo/undo", "Transactions with both a start and a commit record in the log before the crash are redone; those without a commit are undone.")]),
       ],
       examples=[
           Ex("Wait-die decision", "TS(T1)=5, TS(T2)=10. T2 holds a lock on X and T1 requests it; later T1 holds Y and T2 requests it. Under wait-die, what happens to T1's request and to T2's request?",
              ["Smaller timestamp is older: T1 is older.", "T1 (older) requests a lock held by younger T2 ⇒ T1 **waits**.", "T2 (younger) requests a lock held by older T1 ⇒ T2 **dies** (aborts)."],
              "T1 **waits**, T2 **aborts**.", verify=lambda: "T1 %s, T2 %s" % ("waits" if 5 < 10 else "aborts", "aborts" if 10 > 5 else "waits")),
           Ex("Timestamp ordering", "TS(T1)=1, TS(T2)=2. Schedule: r2(A); w1(A); c1; c2. Under basic timestamp ordering which transaction aborts?",
              ["r2(A): TS=2 ≥ W-TS(A)=0, allowed; R-TS(A) = 2.", "w1(A): TS=1 < R-TS(A) = 2 ⇒ T1 arrived too late: **T1 aborts**."],
              "**T1** aborts.", verify=lambda: ", ".join(to_check("r2(A); w1(A); c1; c2", {"T1": 1, "T2": 2}))),
           Ex("Redo and undo sets", "Log before the crash: <T1 start>, <T1,A,10,20>, <T2 start>, <T2,B,5,6>, <T1 commit>, <T3 start>, <T3,C,1,2>, <T2 commit>. Which transactions are redone and which undone?",
              ["Transactions with a commit record: T1 and T2 ⇒ **redo**.", "T3 started and wrote but has no commit ⇒ **undo**."],
              "Redo **T1, T2**; undo **T3**.", verify=lambda: "Redo %s; undo %s" % (", ".join(t for t in ["T1", "T2", "T3"] if t in {"T1", "T2"}), ", ".join(t for t in ["T1", "T2", "T3"] if t not in {"T1", "T2"}))),
           Ex("Is 2PL enough?", "Consider r1(A); w1(A); r2(A); w2(A); with T1 holding X(A) until commit and T2 then locking A. Is the outcome serializable and in which order?",
              ["T1 holds its lock on A until it ends (strict 2PL), so T2's access happens after T1.", "Only edge: T1 → T2 ⇒ serial order T1, T2; exactly **1** equivalent serial schedule."],
              "Serializable, order **T1 → T2**.", verify=lambda: "Serializable, order T1 → T2" if not cyc("r1(A); w1(A); r2(A); w2(A)") and n_orders("r1(A); w1(A); r2(A); w2(A)") == 1 else "no"),
       ],
       traps=[("2PL does not prevent deadlock", "Only conservative 2PL or deadlock-prevention schemes do."),
              ("Wait-die vs wound-wait", "Wait-die: older waits, younger dies. Wound-wait: older wounds, younger waits."),
              ("Strict 2PL holds X locks only", "Rigorous 2PL holds all locks until the end."),
              ("Aborted transactions keep timestamps", "That is what avoids starvation in wait-die and wound-wait.")],
       quick=[("Two-phase locking guarantees", ["deadlock freedom", "conflict serializability", "no aborts", "strictness"], 1, "Strictness requires strict 2PL."),
              ("Under wound-wait, an older transaction requesting a lock held by a younger one", ["waits", "aborts itself", "wounds (aborts) the younger", "is ignored"], 2, "Preemptive."),
              ("WAL requires the log record to be written", ["after the page", "before the corresponding page is written", "never", "only at commit time"], 1, "Write-ahead."),
              ("ARIES phases in order", ["redo, undo, analysis", "analysis, redo, undo", "undo, redo, analysis", "analysis, undo, redo"], 1, "Analysis → Redo → Undo.")],
       summary=["2PL: growing then shrinking; ensures conflict serializability but not deadlock freedom.", "Strict 2PL holds X locks to the end (strict schedules); rigorous holds all locks.", "Wait-die: older waits/younger dies; wound-wait: older wounds/younger waits.",
                "Timestamp ordering aborts late reads (TS < W-TS) and late writes (TS < R-TS or W-TS); deadlock-free.", "WAL, steal/no-force ⇒ undo + redo; checkpoints bound recovery work.", "ARIES: analysis, redo (repeat history), undo (losers, CLRs)."])
