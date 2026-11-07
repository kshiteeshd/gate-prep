"""DBMS part 1: data modelling, relational algebra, SQL."""
import itertools
import math

from learn import Ex, lesson, sampledb as DB

S = "DBMS"


def _superkeys(n, key_sizes):
    """# of superkeys of an n-attribute relation whose candidate keys are the given attribute subsets (tuples of indexes)."""
    c = 0
    for m in range(1, 1 << n):
        if any(all(m >> i & 1 for i in k) for k in key_sizes):
            c += 1
    return c


# ======================================================================================================
lesson(subject=S, chapter="Data Modelling", ch_no=1, no=1, slug="dbms-er-relational", title="ER Model, Keys & the Relational Model",
       topic="ER Model", minutes=22, weight=4, widget="none",
       key="A database models real-world entities and the relationships between them. The ER model draws them as entities, attributes and relationships with cardinality constraints; it is then mapped to relations (tables) whose keys and foreign keys enforce integrity.",
       analogy=("🏫", "Designing a school's records", "Students, courses and teachers are the things you keep records about (entities). Each has properties (name, credits). The links — a student *enrols in* a course — are relationships, and the rules (a student can take many courses, a course has many students) are the cardinalities. The ER diagram is the blueprint; tables are the filing cabinets built from it."),
       sections=[
           dict(h="Why a DBMS, and the three-schema architecture", md="""A DBMS replaces scattered files with a **managed, shared, consistent** store: it gives data independence, controlled redundancy, concurrent access, security, backup/recovery and a declarative query language.

The **three-schema architecture** separates:

- **External schema (view level):** what each user sees.
- **Conceptual (logical) schema:** the whole database structure — tables, constraints.
- **Internal (physical) schema:** files, indexes, storage.

**Logical data independence** = change the conceptual schema without rewriting external views/applications; **physical data independence** = change the storage layout without changing the logical schema."""),
           dict(h="Entities, attributes and keys (ER model)", md="""- **Entity:** a distinguishable object (a student); an **entity set** is a collection of similar entities. Drawn as a rectangle.
- **Attributes** (ovals): *simple* vs *composite* (Address = Street + City), *single-valued* vs **multivalued** (phone numbers; double oval), **derived** (Age from DateOfBirth; dashed oval), **key** attribute (underlined).
- **Weak entity set:** has no key of its own; identified by the key of an *owner* entity plus its own **partial key (discriminator)**, through an **identifying relationship** (double rectangle / double diamond). Example: Dependent of Employee.
- **Specialisation / generalisation (ISA):** subclasses inherit attributes; constraints: *disjoint* vs *overlapping*, *total* vs *partial*."""),
           dict(h="Relationships, cardinality and participation", md="""A **relationship** (diamond) associates entities. Its **degree** is the number of entity sets involved (binary, ternary…).

| Cardinality | Meaning | Max relationship instances (m = ∣A∣, n = ∣B∣) |
|---|---|---|
| **1 : 1** | each entity on either side is in at most one relationship | min(m, n) |
| **1 : N** | one A relates to many B, each B to at most one A | n |
| **M : N** | many-to-many | m·n |

**Participation:** *total* (double line) = every entity must take part (at least one instance); *partial* = optional. Total participation of B in a 1:N relationship means every B has exactly one A — which makes a foreign key in B's table NOT NULL."""),
           dict(h="Mapping ER to relations", md="""| ER construct | Becomes |
|---|---|
| Strong entity set | a table; key attribute → primary key |
| Composite attribute | one column per simple component |
| **Multivalued** attribute | a separate table (owner key + the value) |
| **Weak entity** | a table with the owner's key + partial key as the primary key |
| **1 : N** relationship | put the key of the **1** side as a foreign key in the **N** side's table (no new table) |
| **1 : 1** relationship | foreign key on either side (prefer the side with total participation) |
| **M : N** relationship | a **new table** with both keys (together the primary key) + relationship attributes |
| ISA hierarchy | one table per class (key shared), or a single table with a type column |

**Minimum number of tables** = entity sets + M:N relationships + multivalued attributes (1:N, 1:1 and identifying relationships merge into existing tables).""",
                formulas=[("tables = #entities + #(M:N relationships) + #multivalued attributes", "minimum count for an ER diagram")]),
           dict(h="The relational model: keys and integrity", md="""A **relation** is a set of tuples over a schema R(A₁, …, Aₙ): no duplicate tuples, no order. The number of tuples is the **cardinality**, the number of attributes the **degree**.

- **Superkey:** a set of attributes that uniquely identifies tuples. **Candidate key:** a *minimal* superkey. **Primary key:** the chosen candidate key (NOT NULL). **Alternate keys:** the other candidates. **Prime attribute:** belongs to some candidate key.
- **Foreign key:** attributes of one relation that reference the primary key of another (or the same) relation.
- **Entity integrity:** no primary-key attribute may be NULL. **Referential integrity:** every non-NULL foreign-key value must exist in the referenced table.

**Referential actions** on delete/update of the referenced row: `RESTRICT/NO ACTION` (reject), `CASCADE` (propagate), `SET NULL`, `SET DEFAULT`. A relation with n attributes and exactly one candidate key of k attributes has **2^(n−k)** superkeys.""",
                call=[("trap", "Super vs candidate", "Every candidate key is a superkey, not the other way round. A superkey can contain redundant attributes; a candidate key cannot.")]),
       ],
       examples=[
           Ex("Minimum number of tables", "An ER diagram has 5 entity sets (one of them weak, via an identifying 1:N relationship), 2 M:N relationships, 3 one-to-many relationships and 2 multivalued attributes. What is the minimum number of relational tables?",
              ["One table per entity set: 5 (the weak entity's identifying relationship merges into its table).", "Each M:N relationship needs its own table: +2. Each multivalued attribute needs its own table: +2.", "1:N relationships merge into the N-side table, adding nothing. Total = 5 + 2 + 2 = **9**."],
              "**9** tables.", verify=lambda: str(5 + 2 + 2)),
           Ex("Number of superkeys", "R(A, B, C, D) has exactly one candidate key, {A, B}. How many superkeys does R have?",
              ["A superkey must contain A and B; C and D are free to be in or out.", "Number = 2^(4 − 2) = **4**: {A,B}, {A,B,C}, {A,B,D}, {A,B,C,D}."],
              "**4**", verify=lambda: str(_superkeys(4, [(0, 1)]))),
           Ex("Maximum relationship instances", "Entity sets A (12 instances) and B (20 instances) are in a 1 : N relationship (one A to many B). What is the maximum number of relationship instances?",
              ["Each B instance can be related to at most one A instance, so there can be at most one relationship instance per B.", "Maximum = |B| = **20**."],
              "**20**", verify=lambda: str(20)),
           Ex("Foreign key and join size", "In the sample database every row of Enroll has a sid that exists in Student (a foreign key). How many rows does Enroll ⋈ Student have?",
              ["Each Enroll row matches exactly one Student row (the primary key), so the join has as many rows as Enroll.", "Enroll has 17 rows ⇒ **17** (checked below with the live query)."],
              "**17** rows.", verify=lambda: str(DB.scalar("SELECT COUNT(*) FROM Student s JOIN Enroll e ON s.sid = e.sid"))),
       ],
       traps=[("Forgetting the M:N table", "A many-to-many relationship always needs its own table; you cannot put a single foreign key anywhere."),
              ("Weak entity key", "Its primary key is the **owner's key plus the partial key**, not the partial key alone."),
              ("Superkey vs candidate key", "Candidate keys are minimal; count superkeys with 2^(n − k) only when there is a single candidate key of size k."),
              ("Participation vs cardinality", "Cardinality = max (1 or N); participation = min (total or partial).")],
       quick=[("A many-to-many relationship in an ER diagram is mapped to", ["a foreign key in one table", "a separate table", "an attribute", "a view"], 1, "A relationship table holding both keys."),
              ("Which attribute type needs its own table when mapping to relations?", ["composite", "derived", "multivalued", "key"], 2, "Multivalued attributes become a separate table."),
              ("The primary key of a weak entity table is", ["its partial key only", "the owner's key only", "owner's key + partial key", "any attribute"], 2, "Identification depends on the owner."),
              ("Referential integrity ensures that", ["no key is NULL", "foreign-key values match an existing primary key (or are NULL)", "tuples are unique", "attributes are atomic"], 1, "FK values must exist in the referenced table.")],
       summary=["Three-schema architecture gives logical and physical data independence.", "ER: entities, attributes (simple, composite, multivalued, derived), weak entities (owner key + partial key), ISA.",
                "Cardinality 1:1, 1:N, M:N; max instances min(m,n), n (many side), m·n; participation total/partial.", "Mapping: 1:N → FK on the N side; M:N → new table; multivalued → new table. Min tables = entities + M:N + multivalued.",
                "Keys: superkey ⊃ candidate key; one candidate key of size k in n attributes ⇒ 2^(n−k) superkeys.", "Entity integrity (PK not NULL) and referential integrity (FK values exist)."])


# ======================================================================================================
lesson(subject=S, chapter="Query Languages", ch_no=2, no=1, slug="dbms-relational-algebra", title="Relational Algebra & Relational Calculus",
       topic="Relational Algebra & Calculus", minutes=22, weight=5, widget="sql",
       widget_hint="Every relational-algebra expression has an SQL equivalent. Try the ‘Division’ example, which is the classic hard operator, and modify the queries to see how the results change.",
       key="Relational algebra is a procedural query language built from a handful of operators — select σ, project π, union, difference, Cartesian product and rename — with join, intersection and division derived from them. Relational calculus states *what* you want, and SQL combines both ideas.",
       analogy=("🧰", "A toolkit for tables", "Think of tables as sheets of paper. Selection σ cuts out some rows, projection π cuts out some columns, a join glues two sheets together along matching values, and union/difference stack or subtract sheets. Any question you can ask of the data is a short recipe of these tools."),
       sections=[
           dict(h="The fundamental operators", md="""| Operator | Symbol | Meaning | SQL |
|---|---|---|---|
| **Selection** | σ_cond(R) | rows satisfying a condition | `WHERE` |
| **Projection** | π_A,B(R) | chosen columns, **duplicates removed** | `SELECT DISTINCT` |
| **Union** | R ∪ S | tuples in either (union-compatible) | `UNION` |
| **Set difference** | R − S | tuples in R but not S | `EXCEPT` |
| **Cartesian product** | R × S | all pairs of tuples, ∣R∣·∣S∣ rows | `CROSS JOIN` |
| **Rename** | ρ | rename relation/attributes | `AS` |

Relations are **sets**, so projection and union eliminate duplicates (SQL's bag semantics keeps them unless DISTINCT/UNION is used). Union and difference need **union-compatible** relations (same degree, matching domains)."""),
           dict(h="Derived operators: joins, intersection, division", md="""- **Intersection** R ∩ S = R − (R − S).
- **Theta join** R ⋈_θ S = σ_θ(R × S); **equi-join** uses only equality; **natural join** R ⋈ S joins on all common attributes and keeps one copy of each (a *cross product* if there are no common attributes).
- **Outer joins** keep unmatched tuples padded with NULL: left, right, full.
- **Semi-join** R ⋉ S = tuples of R that join with some tuple of S (no columns of S).
- **Division** R ÷ S (R(A, B), S(B)): the A-values related in R to **every** B-value of S — the operator for *‘for all’* queries.

Division can be expressed with the fundamental operators: R ÷ S = π_A(R) − π_A((π_A(R) × S) − R).""",
                formulas=[("R ÷ S = π_A(R) − π_A((π_A(R) × S) − R)", "division from the primitives")]),
           dict(h="Size bounds and properties", md="""For relations with |R| = m and |S| = n tuples:

| Expression | Minimum | Maximum |
|---|---|---|
| R ∪ S | max(m, n) | m + n |
| R ∩ S | 0 | min(m, n) |
| R − S | max(0, m − n) | m |
| R × S | m·n | m·n |
| R ⋈ S (common attribute) | 0 | m·n |
| R ⋈ S where S's key is R's foreign key | m | m |
| π_A(R) | 1 (if m ≥ 1) | m |
| σ(R) | 0 | m |

Useful equivalences: selections can be cascaded and reordered; σ_c(R × S) = R ⋈_c S; push selections and projections **down** before joins to shrink intermediate results (query optimisation)."""),
           dict(h="Tuple and domain relational calculus", md="""**Tuple relational calculus (TRC)** is declarative: { t | P(t) } is the set of tuples t for which the formula P holds, using ∃ and ∀ over tuple variables. Example — names of students with CGPA above 9: { t.name | Student(t) ∧ t.cgpa > 9 }.

An expression is **safe** if it produces a finite result (every variable ranges over the database). Unsafe example: { t | ¬Student(t) } (infinitely many tuples). Safe TRC and relational algebra have **equal expressive power** (Codd's theorem). **Domain relational calculus (DRC)** uses variables over attribute *values* instead of tuples (QBE is based on it).

*‘For all’ in calculus:* ∀x P(x) ≡ ¬∃x ¬P(x) — e.g. students enrolled in **every** CSE course = students s such that there is **no** CSE course c without an enrolment of s."""),
       ],
       examples=[
           Ex("Division with the sample data", "Which students (sid) are enrolled in every course of the CSE department?",
              ["CSE courses are DB101, OS101, DS101. Division asks for sids paired in Enroll with all three.", "Group Enroll rows for CSE courses by sid and keep sids with 3 distinct courses: students 1 and 6.", "Answer: **{1, 6}** (the SQL form uses GROUP BY sid HAVING COUNT(DISTINCT cid) = 3)."],
              "**{1, 6}**", verify=lambda: "{%s}" % ", ".join(str(r[0]) for r in DB.rows("SELECT sid FROM Enroll WHERE cid IN (SELECT cid FROM Course WHERE dept='CSE') GROUP BY sid HAVING COUNT(DISTINCT cid) = (SELECT COUNT(*) FROM Course WHERE dept='CSE') ORDER BY sid"))),
           Ex("Size of a join", "R has 30 tuples and S has 20 tuples and they share one attribute. State the minimum and maximum number of tuples in R ⋈ S.",
              ["Minimum: no value of the common attribute matches: 0 tuples.", "Maximum: every R tuple matches every S tuple (all the same value): 30 × 20 = 600."],
              "Minimum **0**, maximum **600**.", verify=lambda: "0, %d" % (30 * 20)),
           Ex("Distinct projection", "How many tuples does π_dept(Student) have in the sample database (set semantics)?",
              ["Student has 10 rows but the department values repeat: CSE, ECE, MECH, EEE.", "Duplicates are removed in the algebra: **4** tuples."],
              "**4**", verify=lambda: str(DB.scalar("SELECT COUNT(*) FROM (SELECT DISTINCT dept FROM Student)"))),
           Ex("Difference", "How many departments appear in Student but not in Dept?",
              ["π_dept(Student) − π_dept(Dept): Student uses CSE, ECE, MECH, EEE; Dept lists CSE, ECE, MECH, CIVIL.", "Only EEE is missing from Dept: **1** department."],
              "**1**", verify=lambda: str(DB.scalar("SELECT COUNT(*) FROM (SELECT dept FROM Student EXCEPT SELECT dept FROM Dept)"))),
       ],
       traps=[("Projection removes duplicates", "In relational algebra π is set-based; SQL needs DISTINCT to match."),
              ("Division semantics", "R ÷ S returns A-values related to **all** B-values of S — not ‘some’. An empty S makes every A-value qualify."),
              ("Union compatibility", "Union, intersection and difference require the same number of attributes with compatible domains."),
              ("Natural join with no common attribute", "It degenerates to the Cartesian product, m·n tuples.")],
       quick=[("σ_{cond}(R × S) is equivalent to", ["R ∪ S", "R ⋈_cond S", "R − S", "π(R)"], 1, "A theta join."),
              ("Which operator expresses ‘for all’ queries?", ["Selection", "Projection", "Division", "Union"], 2, "Division."),
              ("R has 10 tuples and S has 7. The maximum size of R ∪ S is", ["7", "10", "17", "70"], 2, "No overlap: 17."),
              ("Safe tuple calculus and relational algebra have", ["equal expressive power", "TRC stronger", "algebra stronger", "no relation"], 0, "Codd's theorem.")],
       summary=["Primitives: σ, π, ∪, −, ×, ρ; derived: ∩, joins, division.", "Projection and union remove duplicates (set semantics).", "Division R ÷ S = A-values related to every B in S; π_A(R) − π_A((π_A(R) × S) − R).",
                "Size bounds: ∪ [max, m+n]; ∩ [0, min]; − [max(0, m−n), m]; × = mn; join [0, mn] or m with an FK to a key.", "Push selection/projection down for optimisation.", "TRC/DRC are declarative; safe expressions = algebra (Codd)."])


# ======================================================================================================
lesson(subject=S, chapter="Query Languages", ch_no=2, no=2, slug="dbms-sql-basics", title="SQL: Queries, Joins, Grouping & Aggregation",
       topic="SQL", minutes=24, weight=5, widget="sql",
       widget_hint="Run the examples against the sample tables and edit them. Predict the result before you press Run — that is the best GATE practice.",
       key="A SELECT statement is evaluated in a fixed logical order — FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY. Joins combine tables, GROUP BY collapses rows into groups, aggregates summarise, and HAVING filters the groups.",
       analogy=("🏭", "An assembly line", "Think of the query as a factory line: first gather the raw tables (FROM), throw away rows you don't want (WHERE), sort the rest into piles (GROUP BY), throw away whole piles (HAVING), pick the columns you will ship (SELECT), and finally arrange the boxes (ORDER BY). Knowing the order explains why you cannot use a SELECT alias inside WHERE."),
       sections=[
           dict(h="The shape of a query and its evaluation order", md="""    SELECT   [DISTINCT] columns / expressions / aggregates
    FROM     table [JOIN table ON condition] ...
    WHERE    row condition
    GROUP BY columns
    HAVING   group condition
    ORDER BY columns [ASC | DESC]

**Logical evaluation order:** FROM (and joins) → WHERE → GROUP BY → HAVING → SELECT (and DISTINCT) → ORDER BY → LIMIT.

- **WHERE** filters **rows before** grouping and cannot use aggregates; **HAVING** filters **groups after** aggregation.
- A column in SELECT that is not inside an aggregate must appear in GROUP BY.
- Operators: `=, <>, <, <=`, `BETWEEN a AND b` (inclusive), `IN (list)`, `LIKE` with `%` (any string) and `_` (one character), `IS NULL`."""),
           dict(h="Joins", md="""| Join | Rows returned |
|---|---|
| **INNER JOIN … ON** | only matching pairs |
| **LEFT OUTER JOIN** | all left rows; right side NULL when unmatched |
| **RIGHT / FULL OUTER JOIN** | all right rows / all rows of both |
| **CROSS JOIN** (or comma) | every pair, ∣R∣·∣S∣ rows |
| **NATURAL JOIN** | equality on all same-named columns |
| **Self-join** | a table joined to itself with aliases (pairs, hierarchies) |

Counting: INNER JOIN of Enroll and Student on sid gives one row per enrolment; a LEFT JOIN of Student with Enroll also keeps the student with no enrolments (as one row with NULLs). An **outer join's row count ≥ the inner join's**.""",
                call=[("tip", "Join condition placement", "For OUTER joins a condition in ON keeps unmatched rows (padded with NULL), while the same condition in WHERE removes them again — the two are not interchangeable.")]),
           dict(h="Aggregates, GROUP BY and HAVING", md="""Aggregates: `COUNT(*)`, `COUNT(col)`, `COUNT(DISTINCT col)`, `SUM`, `AVG`, `MIN`, `MAX`. They **ignore NULLs** (except `COUNT(*)`), and over an empty set return NULL (COUNT returns 0).

- `COUNT(*)` counts rows; `COUNT(col)` counts **non-NULL** values of col.
- With GROUP BY, the aggregate is computed once **per group**; without GROUP BY the whole table is one group.
- `HAVING COUNT(*) > 1` keeps only groups with more than one row.
- Order of results is undefined unless you use ORDER BY."""),
           dict(h="Set operations, ORDER BY, LIMIT, DDL and DML", md="""- **UNION** (removes duplicates), **UNION ALL** (keeps them), **INTERSECT**, **EXCEPT/MINUS** — both queries must be union-compatible.
- `ORDER BY col [DESC]`, `LIMIT n` / `FETCH FIRST n ROWS` for top-n.
- **DDL:** `CREATE TABLE` (with `PRIMARY KEY`, `UNIQUE`, `NOT NULL`, `CHECK`, `FOREIGN KEY … REFERENCES … ON DELETE CASCADE`), `ALTER TABLE`, `DROP TABLE`, `CREATE INDEX`, `CREATE VIEW`.
- **DML:** `INSERT INTO t VALUES …`, `UPDATE t SET … WHERE …`, `DELETE FROM t WHERE …`. A DELETE without WHERE removes every row (table stays); DROP removes the table; TRUNCATE empties it quickly."""),
       ],
       examples=[
           Ex("COUNT(*) versus COUNT(column)", "In the sample database, what does SELECT COUNT(*), COUNT(cgpa), COUNT(DISTINCT dept) FROM Student return?",
              ["Student has 10 rows, so COUNT(*) = 10.", "One student (Gita) has a NULL cgpa, which COUNT(cgpa) skips: 9.", "The distinct departments are CSE, ECE, MECH, EEE: 4."],
              "**10, 9, 4**", verify=lambda: "%d, %d, %d" % DB.rows("SELECT COUNT(*), COUNT(cgpa), COUNT(DISTINCT dept) FROM Student")[0]),
           Ex("GROUP BY with HAVING", "SELECT dept, COUNT(*) FROM Student GROUP BY dept HAVING COUNT(*) > 1 — how many rows does it return?",
              ["Group sizes: CSE 4, ECE 3, MECH 2, EEE 1.", "HAVING keeps groups with more than one row: CSE, ECE, MECH → **3** rows."],
              "**3** rows.", verify=lambda: str(len(DB.rows("SELECT dept, COUNT(*) FROM Student GROUP BY dept HAVING COUNT(*) > 1")))),
           Ex("Inner versus left join", "How many rows do Student INNER JOIN Enroll and Student LEFT JOIN Enroll (both on sid) return?",
              ["Inner join: one row per matching enrolment = **17** (every Enroll row has a student).", "Left join adds the one student with no enrolment (Jay): **18**."],
              "Inner **17**, left **18**.", verify=lambda: "Inner %d, left %d" % (DB.scalar("SELECT COUNT(*) FROM Student s JOIN Enroll e ON s.sid = e.sid"), DB.scalar("SELECT COUNT(*) FROM Student s LEFT JOIN Enroll e ON s.sid = e.sid"))),
           Ex("UNION versus UNION ALL", "How many rows do SELECT dept FROM Student UNION SELECT dept FROM Dept and the UNION ALL version return?",
              ["Student has 10 rows and Dept has 4, so UNION ALL gives 10 + 4 = 14 rows.", "UNION removes duplicates: the distinct values are CSE, ECE, MECH, EEE, CIVIL = 5."],
              "UNION **5**, UNION ALL **14**.", verify=lambda: "UNION %d, UNION ALL %d" % (DB.scalar("SELECT COUNT(*) FROM (SELECT dept FROM Student UNION SELECT dept FROM Dept)"), DB.scalar("SELECT COUNT(*) FROM (SELECT dept FROM Student UNION ALL SELECT dept FROM Dept)"))),
           Ex("Cross join size", "How many rows are in Student CROSS JOIN Course?",
              ["Student has 10 rows and Course has 5 rows.", "A cross join pairs every row with every row: 10 × 5 = **50** rows."],
              "**50**", verify=lambda: str(DB.scalar("SELECT COUNT(*) FROM Student s CROSS JOIN Course"))),
       ],
       traps=[("WHERE vs HAVING", "Aggregates are not allowed in WHERE; use HAVING for conditions on groups."),
              ("COUNT(col) ignores NULLs", "COUNT(*) counts rows; COUNT(col) skips NULLs; COUNT(DISTINCT col) counts distinct non-NULL values."),
              ("Non-grouped columns", "Every selected column must be in GROUP BY or inside an aggregate."),
              ("UNION removes duplicates", "UNION ALL is faster and keeps duplicates; counts differ.")],
       quick=[("Which clause filters groups after aggregation?", ["WHERE", "HAVING", "GROUP BY", "ORDER BY"], 1, "HAVING."),
              ("A LEFT JOIN returns", ["only matching rows", "all left rows, NULL-padded when unmatched", "all right rows", "the Cartesian product"], 1, "Keeps unmatched left rows."),
              ("COUNT(*) vs COUNT(col): COUNT(col) counts", ["all rows", "non-NULL values of col", "distinct values", "NULL values"], 1, "NULLs are skipped."),
              ("The logical order of evaluation starts with", ["SELECT", "WHERE", "FROM", "ORDER BY"], 2, "FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY.")],
       summary=["Evaluation order: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY.", "WHERE filters rows, HAVING filters groups; aggregates only in SELECT/HAVING.", "Aggregates ignore NULLs; COUNT(*) counts rows; COUNT(DISTINCT col) distinct non-NULL.",
                "Outer join rows ≥ inner join rows; CROSS JOIN = |R|·|S|.", "UNION removes duplicates, UNION ALL keeps them; INTERSECT/EXCEPT need union-compatibility.", "DELETE removes rows, DROP removes the table."])


# ======================================================================================================
lesson(subject=S, chapter="Query Languages", ch_no=2, no=3, slug="dbms-sql-nulls-subqueries", title="SQL: NULLs, Subqueries & the Classic Traps",
       topic="SQL", minutes=24, weight=5, widget="sql",
       widget_hint="Run ‘NOT IN with NULL’ and then remove the NULL with IS NOT NULL — the result jumps from 0 rows to 10. Try the correlated subquery too.",
       key="SQL uses three-valued logic (TRUE, FALSE, UNKNOWN): any comparison with NULL is UNKNOWN, and WHERE keeps only TRUE rows. This explains the famous NOT IN trap; subqueries — scalar, IN, EXISTS and correlated — answer most ‘nth-highest’ and ‘all/any’ style questions.",
       analogy=("❓", "A form with blank answers", "If someone leaves their age blank, is their age equal to 30? You can't say yes or no — it's *unknown*. SQL treats every comparison with a blank (NULL) the same way, even ‘blank = blank’. A filter only lets through rows where the answer is definitely *yes*, so unknowns quietly vanish."),
       sections=[
           dict(h="Three-valued logic", md="""Any comparison involving NULL (`=, <>, <, >, …`) yields **UNKNOWN**, including `NULL = NULL` and `NULL <> NULL`. Use `IS NULL` / `IS NOT NULL` to test for nulls.

| A | B | A AND B | A OR B | NOT A |
|---|---|---|---|---|
| TRUE | UNKNOWN | UNKNOWN | TRUE | FALSE |
| FALSE | UNKNOWN | FALSE | UNKNOWN | TRUE |
| UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

`WHERE` and `HAVING` keep a row only if the condition is **TRUE** — UNKNOWN rows are dropped. Consequences: `WHERE cgpa > 8 OR cgpa <= 8` does **not** return rows with NULL cgpa; `col = col` is not always true; aggregates (except COUNT(*)) skip NULLs; `DISTINCT`, `GROUP BY` and set operations treat NULLs as **equal** to each other (one NULL group).""",
                call=[("trap", "Arithmetic with NULL", "5 + NULL is NULL. `SUM(a + b)` skips any row where either is NULL, which can differ from `SUM(a) + SUM(b)`.")]),
           dict(h="Subqueries: scalar, IN, EXISTS, ANY/ALL", md="""- **Scalar subquery** returns one value and can be used where a value is expected: `WHERE cgpa = (SELECT MAX(cgpa) FROM Student)`.
- **IN / NOT IN** test membership in the subquery's result column.
- **EXISTS / NOT EXISTS** test whether the subquery returns *any row*; it ignores the selected columns and is unaffected by NULLs.
- **ANY / SOME / ALL:** `x > ALL (subquery)` means greater than every value; `x = ANY (…)` is the same as `IN`.
- A subquery in FROM is a **derived table** (needs an alias); `WITH` defines a named *common table expression*."""),
           dict(h="The NOT IN trap and how to avoid it", md="""`x NOT IN (a, b, NULL)` expands to `x <> a AND x <> b AND x <> NULL`, and the last term is UNKNOWN, so the whole condition is never TRUE — **the query returns no rows** whenever the subquery's column contains a NULL.

Fixes: add `WHERE col IS NOT NULL` inside the subquery, or use **NOT EXISTS**, which is NULL-safe:

    SELECT name FROM Student s
    WHERE NOT EXISTS (SELECT 1 FROM Dept d WHERE d.hod = s.name);

In the sample data, `name NOT IN (SELECT hod FROM Dept)` returns **0 rows** because one hod is NULL; with `WHERE hod IS NOT NULL` inside the subquery it returns all 10 students."""),
           dict(h="Correlated subqueries and ‘nth highest’", md="""A **correlated subquery** refers to a column of the outer query, so it is (conceptually) re-evaluated **for every outer row** — e.g. students whose CGPA is above their own department's average:

    SELECT name FROM Student s
    WHERE cgpa > (SELECT AVG(cgpa) FROM Student WHERE dept = s.dept);

**Second-highest value** (three standard answers): `SELECT MAX(x) FROM T WHERE x < (SELECT MAX(x) FROM T)`; or `… WHERE 1 = (SELECT COUNT(DISTINCT x) FROM T t2 WHERE t2.x > t1.x)`; or `ORDER BY x DESC LIMIT 1 OFFSET 1` (which counts duplicate values separately, so it can return the *same* value twice).

**Views** (`CREATE VIEW`) store a query, not data; simple single-table views are updatable. **Constraints** are enforced by the DBMS; **triggers** run procedural code automatically on INSERT/UPDATE/DELETE (BEFORE/AFTER, row/statement level)."""),
       ],
       examples=[
           Ex("The NOT IN trap", "How many rows does SELECT name FROM Student WHERE name NOT IN (SELECT hod FROM Dept) return, and what if the subquery adds WHERE hod IS NOT NULL?",
              ["Dept.hod contains Rao, Iyer, Khan and **NULL** (the CIVIL row).", "name NOT IN (…, NULL) is never TRUE ⇒ **0** rows.", "Without the NULL the filter works: no student is a hod, so all **10** students are returned."],
              "**0** rows, then **10** rows.", verify=lambda: "%d rows, then %d rows" % (len(DB.rows("SELECT name FROM Student WHERE name NOT IN (SELECT hod FROM Dept)")), len(DB.rows("SELECT name FROM Student WHERE name NOT IN (SELECT hod FROM Dept WHERE hod IS NOT NULL)")))),
           Ex("Three-valued WHERE", "How many students satisfy cgpa > 8 OR cgpa <= 8? (one student has cgpa NULL)",
              ["For Gita, both comparisons are UNKNOWN and UNKNOWN OR UNKNOWN is UNKNOWN, so she is dropped.", "9 of the 10 students are returned: **9**, not 10."],
              "**9**", verify=lambda: str(DB.scalar("SELECT COUNT(*) FROM Student WHERE cgpa > 8 OR cgpa <= 8"))),
           Ex("Correlated subquery", "Which students have a CGPA above their own department's average? (give the count)",
              ["Department averages (ignoring NULLs): CSE 8.85, ECE 7.83, EEE 7.5, MECH 7.2.", "Above their average: Asha (9.1), Farhan (9.5) in CSE; Chitra (7.9) and Dev (8.8) in ECE. Jay equals the EEE average, Gita's NULL is unknown.", "Count = **4**."],
              "**4**", verify=lambda: str(len(DB.rows("SELECT name FROM Student s WHERE cgpa > (SELECT AVG(cgpa) FROM Student WHERE dept = s.dept)")))),
           Ex("Second highest CGPA", "Using MAX with a nested MAX, who has the second-highest CGPA?",
              ["The highest is 9.5 (Farhan). The largest value below it is 9.1.", "That belongs to **Asha**."],
              "**Asha** (9.1)", verify=lambda: "%s (%s)" % (DB.scalar("SELECT name FROM Student WHERE cgpa = (SELECT MAX(cgpa) FROM Student WHERE cgpa < (SELECT MAX(cgpa) FROM Student))"), DB.scalar("SELECT MAX(cgpa) FROM Student WHERE cgpa < (SELECT MAX(cgpa) FROM Student)"))),
           Ex("COUNT with NULL grades", "What does SELECT COUNT(grade), COUNT(*) FROM Enroll return? (two enrolments have a NULL grade)",
              ["Enroll has 17 rows ⇒ COUNT(*) = 17.", "COUNT(grade) skips the two NULL grades ⇒ 15."],
              "**15, 17**", verify=lambda: "%d, %d" % DB.rows("SELECT COUNT(grade), COUNT(*) FROM Enroll")[0]),
       ],
       traps=[("NOT IN with a NULL in the subquery", "Returns nothing. Use NOT EXISTS or filter the NULLs out."),
              ("Equality with NULL", "`col = NULL` is never true — write `col IS NULL`."),
              ("OFFSET for second highest", "`ORDER BY x DESC LIMIT 1 OFFSET 1` can return the same value as the highest if it is duplicated; use DISTINCT or the nested-MAX form."),
              ("WHERE on a nullable column", "`WHERE grade <> 'A'` drops rows where grade is NULL (UNKNOWN).")],
       quick=[("NULL = NULL evaluates to", ["TRUE", "FALSE", "UNKNOWN", "an error"], 2, "Use IS NULL."),
              ("x NOT IN (SELECT y FROM S) returns no rows whenever", ["S is empty", "S.y contains a NULL", "x is large", "S has duplicates"], 1, "The NULL makes every comparison UNKNOWN."),
              ("Which is NULL-safe?", ["NOT IN", "NOT EXISTS", "<> ALL with NULLs", "= NULL"], 1, "EXISTS ignores NULLs."),
              ("A correlated subquery is conceptually evaluated", ["once", "once per outer row", "never", "twice"], 1, "It depends on the outer row.")],
       summary=["Comparisons with NULL are UNKNOWN; WHERE/HAVING keep only TRUE; use IS NULL.", "Aggregates skip NULLs except COUNT(*); DISTINCT/GROUP BY treat NULLs as equal.", "NOT IN + NULL in the subquery ⇒ empty result; use NOT EXISTS.",
                "EXISTS tests for any row; IN tests membership; ANY/ALL compare with every value.", "Correlated subquery: re-evaluated per outer row.", "Second highest: nested MAX, COUNT(DISTINCT) trick, or ORDER BY … OFFSET 1."])
