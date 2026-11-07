"""Databases — curated concept questions."""
from content.kit import C

C("DBMS", "ER Model", "Concepts", [
    ("e", 1, "s", "A multivalued attribute in an ER diagram is mapped to a relational schema by", ["creating a separate relation with the owner's key", "adding repeated columns", "storing a comma-separated string", "ignoring it"], 0, "A separate table (key + attribute) preserves 1NF."),
    ("e", 1, "s", "Which symbol/idea represents a weak entity?", ["Double rectangle with an identifying (double-line) relationship", "A dashed oval", "A single rectangle", "A diamond"], 0, "Weak entities have a double rectangle and depend on an owner."),
    ("m", 1, "s", "In a one-to-many relationship between DEPARTMENT (1) and EMPLOYEE (N), the foreign key is placed in", ["EMPLOYEE", "DEPARTMENT", "a separate relation always", "both relations"], 0, "The 'many' side stores the key of the 'one' side."),
    ("m", 2, "s", "Specialisation/generalisation with disjoint, total constraints means", ["each superclass instance belongs to exactly one subclass", "an instance may belong to several subclasses", "some instances belong to no subclass", "subclasses have no attributes of their own"], 0, "Disjoint = at most one; total = at least one."),
    ("m", 1, "s", "A composite attribute such as Address(Street, City, PIN) is typically stored as", ["its simple component attributes", "a single atomic column only", "a multivalued relation", "a derived attribute"], 0, "Only the leaf attributes become columns."),
    ("h", 2, "s", "Total participation of an entity set in a relationship is shown by", ["a double line from the entity to the relationship", "an arrow", "a dashed line", "a thick diamond"], 0, "Every entity instance must participate."),
])

C("DBMS", "Relational Algebra & Calculus", "Concepts", [
    ("e", 1, "s", "Which relational algebra operator is NOT among the fundamental (primitive) operators?", ["Natural join", "Union", "Cartesian product", "Selection"], 0, "Join can be derived as σ over ×; the primitives are σ, π, ∪, −, ×, ρ."),
    ("m", 1, "s", "The relational algebra expression π_A(R) − π_A(S) returns", ["values of A in R but not in S", "values of A in both", "all of A in R ∪ S", "tuples of R not in S"], 0, "Set difference on the projections."),
    ("m", 2, "s", "Which relational algebra query finds the students who enrolled in ALL courses of a relation COURSE(c)?", ["Enroll(s,c) ÷ COURSE(c)", "Enroll ⋈ COURSE", "Enroll ∪ COURSE", "π_s(Enroll) − COURSE"], 0, "Division expresses universal quantification."),
    ("m", 1, "s", "Tuple relational calculus expressions that can lead to infinite results are called", ["unsafe expressions", "ambiguous expressions", "recursive queries", "correlated queries"], 0, "Safe expressions are restricted to a finite domain."),
    ("h", 2, "m", "Which of the following operators are NOT expressible without the set-difference operator? (select all)", ["Relational division", "Intersection", "Natural join", "Anti-join / 'not exists' queries"], [0, 1, 3], "Intersection = R − (R − S); division and 'for all'/'not exists' need negation."),
    ("m", 1, "s", "Relational algebra is a", ["procedural query language", "non-procedural query language", "graphical language", "data definition language"], 0, "Relational calculus is the declarative counterpart."),
])

C("DBMS", "SQL", "Concepts", [
    ("e", 1, "s", "Which clause is used to filter GROUPS after GROUP BY?", ["HAVING", "WHERE", "ORDER BY", "DISTINCT"], 0, "WHERE filters rows before grouping; HAVING filters groups."),
    ("e", 1, "s", "COUNT(*) differs from COUNT(column) in that COUNT(column)", ["ignores NULL values in that column", "counts duplicates only", "is faster", "returns a string"], 0, "COUNT(*) counts all rows."),
    ("m", 1, "s", "In SQL, the result of comparing NULL = NULL is", ["UNKNOWN", "TRUE", "FALSE", "an error"], 0, "Use IS NULL to test for nulls."),
    ("m", 2, "s", "The query SELECT * FROM R WHERE x NOT IN (SELECT y FROM S) returns no rows whenever", ["S.y contains a NULL", "S is empty", "R.x is never NULL", "S.y has duplicates"], 0, "x NOT IN (…, NULL) evaluates to UNKNOWN for non-matching values."),
    ("m", 1, "s", "Which JOIN returns all rows from the left table even if there is no match in the right table?", ["LEFT OUTER JOIN", "INNER JOIN", "CROSS JOIN", "NATURAL JOIN"], 0, "Unmatched right columns are NULL."),
    ("m", 2, "m", "Which statements about UNION and UNION ALL are TRUE? (select all)", ["UNION removes duplicates", "UNION ALL keeps duplicates", "UNION ALL is generally faster than UNION", "Both require union-compatible column lists", "UNION ALL always sorts its result"], [0, 1, 2, 3], "The first four statements are correct; UNION ALL does not sort."),
    ("h", 2, "s", "Which statement about a correlated subquery is correct?", ["It is evaluated once per row of the outer query (conceptually)", "It cannot reference outer-query columns", "It is always faster than a join", "It must return exactly one row"], 0, "The inner query depends on the outer row."),
    ("m", 1, "s", "A view in SQL is", ["a stored query presented as a virtual table", "a physical copy of data", "an index", "a constraint"], 0, "Views may be updatable under conditions."),
    ("h", 2, "s", "Which of the following SQL features guarantees uniqueness of a set of columns and permits at most one NULL in many systems?", ["UNIQUE constraint", "PRIMARY KEY constraint", "CHECK constraint", "FOREIGN KEY constraint"], 0, "PRIMARY KEY disallows NULL; UNIQUE (system-dependent) allows NULLs."),
    ("m", 1, "s", "ON DELETE CASCADE on a foreign key means", ["deleting a parent row deletes the referencing child rows", "deleting a child row deletes the parent", "deletes are blocked", "the key becomes NULL"], 0, "Referential action propagates the delete."),
    ("h", 2, "m", "Which of the following queries can find the second-highest salary in table Emp(sal)? (select all that are valid standard SQL)", ["SELECT MAX(sal) FROM Emp WHERE sal < (SELECT MAX(sal) FROM Emp)", "SELECT sal FROM Emp e1 WHERE 1 = (SELECT COUNT(DISTINCT sal) FROM Emp e2 WHERE e2.sal > e1.sal)", "SELECT sal FROM Emp ORDER BY sal DESC OFFSET 1 ROW FETCH FIRST 1 ROW ONLY", "SELECT MAX(sal) FROM Emp"], [0, 1, 2], "The last query returns the highest salary."),
])

C("DBMS", "Functional Dependencies & Normalization", "Concepts", [
    ("e", 1, "s", "A relation is in BCNF if for every non-trivial FD X → Y", ["X is a superkey", "Y is a prime attribute", "X is a candidate key and Y a non-key attribute only", "X is a subset of a key"], 0, "BCNF is stricter than 3NF: no prime-attribute exception."),
    ("m", 1, "s", "Which normal form removes partial dependencies of non-prime attributes on a candidate key?", ["2NF", "1NF", "BCNF", "4NF"], 0, "2NF = 1NF + no partial dependencies."),
    ("m", 2, "s", "Every relation in BCNF is also in", ["3NF", "4NF", "5NF", "none of these"], 0, "BCNF ⊂ 3NF ⊂ 2NF ⊂ 1NF; BCNF does not imply 4NF."),
    ("m", 2, "s", "A lossless-join decomposition of R into R1 and R2 is guaranteed if", ["R1 ∩ R2 → R1 or R1 ∩ R2 → R2 holds", "R1 and R2 have no common attributes", "R1 and R2 are in 3NF", "every FD is preserved"], 0, "The common attributes must be a key of one of the parts."),
    ("m", 1, "s", "Which of the following is NOT an Armstrong axiom?", ["Union", "Reflexivity", "Augmentation", "Transitivity"], 0, "Union, decomposition and pseudo-transitivity are derived rules."),
    ("h", 2, "s", "Decomposing a relation into BCNF", ["always gives a lossless join but may lose dependency preservation", "always preserves dependencies but may be lossy", "is always dependency preserving and lossless", "is never possible"], 0, "3NF synthesis guarantees both lossless join and dependency preservation."),
    ("h", 2, "m", "Which of the following are true for a relation R(A,B,C) with FDs {AB → C, C → B}? (select all)", ["Candidate keys are AB and AC", "R is in 3NF", "R is in BCNF", "B is a prime attribute"], [0, 1, 3], "C → B violates BCNF (C is not a superkey) but B is prime, so 3NF holds."),
    ("m", 1, "s", "An attribute that is part of some candidate key is called", ["prime", "derived", "composite", "multivalued"], 0, "Otherwise it is a non-prime attribute."),
    ("h", 2, "s", "A relation with a multivalued dependency that is not implied by a key violates", ["4NF", "BCNF", "2NF", "1NF"], 0, "4NF removes non-trivial multivalued dependencies."),
])

C("DBMS", "Indexing & File Organization", "Concepts", [
    ("e", 1, "s", "Compared with a B-tree, a B+ tree", ["stores all data pointers in the leaf level and links the leaves", "stores records in internal nodes", "has variable fan-out", "cannot support range queries"], 0, "Leaf chaining supports efficient range scans."),
    ("m", 1, "s", "A primary index is built on", ["the ordering key field of a sorted data file", "any non-ordering field", "a hash of the key", "a foreign key"], 0, "A clustered/primary index on the sort key."),
    ("m", 1, "s", "A dense index has", ["an index entry for every search-key value (record)", "one entry per data block", "one entry per file", "no entries for duplicates"], 0, "A sparse index has one entry per block."),
    ("m", 2, "s", "Hash-based indexing is NOT suitable for", ["range queries", "equality searches", "point lookups on the key", "insertions"], 0, "Hashing destroys order."),
    ("h", 2, "s", "Increasing the order (fan-out) of a B+ tree generally", ["reduces the height of the tree", "increases the height", "has no effect on height", "makes searches unbounded"], 0, "Height ≈ log_fanout(N)."),
    ("h", 2, "s", "In extendible hashing, a bucket overflow always causes the directory to double when", ["the overflowing bucket's local depth equals the global depth", "the bucket is more than half full", "two buckets share a pointer", "the load factor exceeds one"], 0, "Otherwise only the bucket splits and pointers are redistributed."),
])

C("DBMS", "Transactions & Concurrency", "Concepts", [
    ("e", 1, "s", "Which ACID property guarantees 'all or nothing' execution of a transaction?", ["Atomicity", "Consistency", "Isolation", "Durability"], 0, "Rollback undoes partial effects."),
    ("m", 1, "s", "Two-phase locking (2PL) guarantees", ["conflict serializability", "deadlock freedom", "cascadeless schedules", "strict recoverability"], 0, "2PL can deadlock; strict 2PL gives strict schedules."),
    ("m", 2, "s", "In strict 2PL a transaction", ["holds all its exclusive locks until it commits or aborts", "acquires locks only after commit", "releases locks as soon as it has finished using the item", "uses no shared locks"], 0, "This prevents dirty reads and cascading aborts."),
    ("m", 1, "s", "A dirty read is", ["reading data written by a transaction that has not yet committed", "reading the same row twice with different results", "seeing new rows appear in a repeated query", "reading deleted data"], 0, "Phantoms and non-repeatable reads are different anomalies."),
    ("m", 2, "m", "Which isolation anomalies are prevented by the REPEATABLE READ level in the SQL standard? (select all)", ["Dirty read", "Non-repeatable read", "Phantom read", "Lost update across commits"], [0, 1], "Phantoms are prevented only by SERIALIZABLE."),
    ("h", 2, "s", "In the wait-for graph, a deadlock exists iff", ["the graph contains a cycle", "the graph is acyclic", "some node has no outgoing edge", "the number of edges equals the number of nodes"], 0, "Detect with cycle detection and abort a victim."),
    ("h", 2, "s", "The write-ahead logging (WAL) rule requires", ["log records to be flushed before the corresponding data pages are written to disk", "data pages to be written before the log", "both to be written simultaneously", "only commit records to be logged"], 0, "Needed to be able to undo uncommitted changes."),
    ("h", 2, "m", "Which of the following concurrency-control approaches are optimistic or timestamp based? (select all)", ["Basic timestamp ordering", "Validation-based (OCC) protocol", "Strict two-phase locking", "Thomas write rule"], [0, 1, 3], "Strict 2PL is pessimistic locking."),
    ("m", 1, "s", "In a recoverable schedule, if Tj reads data written by Ti, then", ["Ti must commit before Tj commits", "Tj must commit before Ti", "Ti and Tj commit together", "Ti must abort"], 0, "Otherwise a commit could depend on rolled-back data."),
])
