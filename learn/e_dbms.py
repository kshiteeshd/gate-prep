"""Textbook-style long-form teaching text: Databases."""
from learn import elab

elab("dbms-er-relational",
 ("Why databases exist", """
Imagine keeping a college's records in separate spreadsheets: one for students, one for courses, one for marks. The same student's name appears in several files; fixing a spelling in one file leaves the others wrong; two people editing at once can overwrite each other. A **database management system (DBMS)** solves these problems: it stores data in one organised place, lets many users read and write safely at the same time, and enforces rules about what data is allowed.

Designing a database starts with a question: *what are the things we need to record, and how are they related?* The answer is drawn as an **entity–relationship (ER) diagram**, and later converted to **tables**.
"""),
 ("The ER model", """
An **entity** is a thing we keep information about: a Student, a Course. An **attribute** is a property of an entity: a student's roll number, name, phone numbers. A **key attribute** uniquely identifies an entity (roll number). Some attributes are **multivalued** (a student may have several phone numbers) and some are **derived** (age can be computed from date of birth).

A **relationship** connects entities: a student *enrols in* a course. Its **cardinality** tells how many of one side can be linked to the other: **one-to-one (1:1)**, **one-to-many (1:N)** or **many-to-many (M:N)**. Participation is **total** if every entity must take part (every course must have at least one instructor) and **partial** otherwise.

A **weak entity** cannot be identified by its own attributes alone (a dependent of an employee is identified by the employee's key plus the dependent's name); it depends on an **owner entity**.
"""),
 ("From ER diagram to tables", """
The relational model stores data in **tables** (relations). Each **row** (tuple) is one record and each **column** (attribute) has a name and a domain. A **superkey** is any set of attributes that uniquely identifies rows; a **candidate key** is a *minimal* superkey; the **primary key** is the candidate key chosen as the main identifier. A **foreign key** is an attribute (or set) that refers to the primary key of another table, which links the tables and lets the DBMS enforce **referential integrity**.

Conversion rules:

- Each entity becomes a table whose primary key is its key attribute.
- A **multivalued** attribute becomes its own table (with the entity's key as a foreign key).
- A **1:N** relationship adds the key of the "one" side as a foreign key on the "many" side's table.
- An **M:N** relationship becomes a new table whose key combines the keys of both entities.
- A **weak entity** table includes the owner's key as part of its own key.
"""),
)

elab("dbms-relational-algebra",
 ("A language for asking questions of tables", """
Relational algebra is a small set of operators that take tables and produce tables. Because each operator returns a table, operators can be chained like functions. It is the theory behind SQL: every SQL query can be understood as a relational-algebra expression.

In relational algebra a table is a **set**, so duplicate rows never appear in an answer. (SQL, by contrast, keeps duplicates unless told otherwise.)
"""),
 ("The core operators", """
- **Selection** $\\sigma_{\\text{condition}}(R)$ keeps the **rows** that satisfy the condition. $\\sigma_{\\text{age}>20}(\\text{Student})$.
- **Projection** $\\pi_{A_1,\\dots}(R)$ keeps the chosen **columns** and removes duplicates.
- **Union, intersection, difference** work on tables with the same columns ("union-compatible").
- **Cartesian product** $R\\times S$ pairs every row of $R$ with every row of $S$; if $R$ has $m$ rows and $S$ has $n$, the result has $mn$.
- **Rename** $\\rho$ gives a table or its columns a new name, needed when a table is joined with itself.

The set $\\{\\sigma,\\pi,\\cup,-,\\times,\\rho\\}$ is enough to express everything; the other operators are conveniences.
"""),
 ("Joins and division", """
A **natural join** $R\\bowtie S$ takes the product and keeps only rows that agree on all common attributes, merging those columns. A **theta join** uses any condition instead. An **outer join** also keeps the unmatched rows of one or both sides, padding with `NULL`.

**Division** $R\\div S$ answers "for all" questions: "which students took *all* the courses in S?" It returns those values of $R$'s extra attributes that are paired with *every* row of $S$. It can be written using the basic operators:

$$R\\div S=\\pi_A(R)-\\pi_A\\bigl((\\pi_A(R)\\times S)-R\\bigr)$$

**Size questions.** For tables $R$ ($m$ rows) and $S$ ($n$ rows), the natural join has between $0$ rows (nothing matches) and $mn$ rows (the join attribute has the same value in every row of both). If the join attribute is the primary key of $S$ and a foreign key in $R$, every row of $R$ matches exactly one row of $S$, so the result has exactly $m$ rows. A Cartesian product always has exactly $mn$ rows.
"""),
)

elab("dbms-sql-basics",
 ("SQL in one picture", """
SQL (Structured Query Language) is how we talk to relational databases. A basic query has the shape:

    SELECT   columns
    FROM     tables
    WHERE    row condition
    GROUP BY columns
    HAVING   group condition
    ORDER BY columns

Remember that the **logical order of evaluation** is different from the order in which it is written: `FROM` (and joins) first, then `WHERE`, then `GROUP BY`, then `HAVING`, then `SELECT`, and finally `ORDER BY`. This explains why you cannot use a `SELECT` alias inside `WHERE`.
"""),
 ("Grouping and aggregates", """
Aggregate functions summarise many rows into one value: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. With `GROUP BY`, rows with the same value in the grouping columns are collected into groups and each aggregate is computed per group.

`WHERE` filters **rows before** grouping; `HAVING` filters **groups after** aggregation, so only `HAVING` can use an aggregate: `HAVING COUNT(*) > 3`.

Every column in `SELECT` must be either a grouping column or inside an aggregate. `COUNT(*)` counts rows; `COUNT(col)` counts the non-`NULL` values of `col`; `COUNT(DISTINCT col)` counts distinct non-`NULL` values.
"""),
 ("Joins, set operations and DDL", """
A **join** combines tables: `INNER JOIN` keeps matched pairs; `LEFT/RIGHT/FULL OUTER JOIN` keep unmatched rows of one or both sides. `UNION`, `INTERSECT` and `EXCEPT` combine query results and remove duplicates (add `ALL` to keep them).

**DDL** (data definition) creates the structure: `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`, with constraints such as `PRIMARY KEY`, `UNIQUE`, `NOT NULL`, `CHECK` and `FOREIGN KEY ... REFERENCES ... ON DELETE CASCADE`. **DML** modifies the data: `INSERT`, `UPDATE`, `DELETE`.
"""),
)

elab("dbms-sql-nulls-subqueries",
 ("NULL: unknown, not zero", """
`NULL` represents a missing or unknown value. It is not zero and not an empty string. Any comparison with `NULL` — even `NULL = NULL` — gives **unknown** rather than true or false. Use `IS NULL` and `IS NOT NULL` to test for it.

SQL uses **three-valued logic**: true, false and unknown. `unknown AND true` is unknown; `unknown OR true` is true; `NOT unknown` is unknown. A `WHERE` clause keeps only rows for which the condition is **true**; unknown rows are discarded, just like false ones.

Aggregates ignore `NULL` (except `COUNT(*)`). `AVG` divides by the number of non-null values.
"""),
 ("Subqueries", """
A **subquery** is a query inside another. A **scalar** subquery returns one value; an `IN` subquery returns a set to test membership; `EXISTS` checks whether the subquery returns any row at all.

A **correlated** subquery refers to a column of the outer query, so it is re-evaluated for each outer row. "Employees earning more than the average of their own department" is correlated; "employees earning more than the overall average" is not.

`ANY`/`SOME` and `ALL` compare against a set: `salary > ALL (subquery)` means greater than every value, which is the same as greater than the maximum.
"""),
 ("Typical traps", """
- **`NOT IN` with NULL:** `x NOT IN (1, 2, NULL)` is never true, because for any `x` the comparison `x <> NULL` is unknown. `NOT EXISTS` avoids this.
- **Count of an empty group.** `COUNT(*)` over zero rows is 0, but `SUM` and `AVG` over zero rows are `NULL`.
- **Division queries** ("all courses") are usually written with a double `NOT EXISTS`.
- **Duplicates.** `SELECT` keeps duplicates; add `DISTINCT` to remove them.
"""),
)

elab("dbms-fds-closure",
 ("Redundancy and what causes it", """
A badly designed table repeats facts. If a table stores (student, department, department head) on every row, then the head of a department is stored once per student; changing it means many updates, and deleting the last student of a department loses the head. These problems are called **update, insertion and deletion anomalies**.

The cause is a hidden dependency: the department determines its head. We capture such rules as **functional dependencies**.
"""),
 ("Functional dependencies", """
A functional dependency $X\\to Y$ says: *whenever two rows agree on $X$, they must agree on $Y$.* So roll number $\\to$ name holds because a roll number identifies a student, but name $\\to$ roll number does not, since two students may share a name.

**Armstrong's axioms** let us derive new dependencies from given ones:

- **Reflexivity:** if $Y\\subseteq X$ then $X\\to Y$.
- **Augmentation:** if $X\\to Y$ then $XZ\\to YZ$.
- **Transitivity:** if $X\\to Y$ and $Y\\to Z$ then $X\\to Z$.

From these follow union ($X\\to Y,\\,X\\to Z\\Rightarrow X\\to YZ$), decomposition and pseudo-transitivity.
"""),
 ("Attribute closure: the one skill to master", """
The **closure** $X^+$ of a set $X$ under the dependencies $F$ is the set of all attributes that $X$ determines. To compute it: start with $X^+=X$, then repeat: for every dependency $A\\to B$ in $F$ with $A\\subseteq X^+$, add $B$ to $X^+$, until nothing changes.

Everything is answered with closures:

- **Is $X\\to Y$ implied by $F$?** Compute $X^+$ and check whether $Y\\subseteq X^+$.
- **Is $X$ a superkey?** Check whether $X^+$ is all attributes. It is a **candidate key** if additionally no proper subset has that property.
- **Candidate keys:** attributes that never appear on a right-hand side must be in every key; start from them and add attributes as needed.
- A **minimal cover** has single attributes on the right, no extraneous attributes on the left, and no redundant dependency.
"""),
)

elab("dbms-normal-forms",
 ("Normalisation: removing redundancy", """
**Normalisation** splits a table into smaller ones so that each fact is stored once. Each *normal form* is a stricter rule about which dependencies are allowed.

- **1NF:** every cell holds a single atomic value (no lists, no repeating groups).
- **2NF:** 1NF, and no non-prime attribute depends on *part of* a candidate key (no **partial dependency**).
- **3NF:** 2NF, and no non-prime attribute depends on another non-prime attribute (no **transitive dependency**). Equivalently: for every dependency $X\\to A$, either $X$ is a superkey or $A$ is a prime attribute.
- **BCNF:** for every nontrivial dependency $X\\to Y$, $X$ must be a **superkey**. This is stricter than 3NF.

A **prime attribute** is one that belongs to some candidate key.
"""),
 ("Checking a table, step by step", """
1. Find all candidate keys using closures.
2. Mark prime and non-prime attributes.
3. For each dependency, test: is the left side a superkey? If yes, it does no harm. If no, then check whether the right side is prime (violates BCNF but OK for 3NF) or non-prime (violates 3NF; if the left side is a proper part of a key it is a partial dependency violating 2NF).

The highest normal form is the strongest one that passes. Every BCNF relation is in 3NF, every 3NF in 2NF, every 2NF in 1NF.
"""),
 ("Decomposition: what makes it good", """
Decomposing a relation $R$ into $R_1,R_2$ should be **lossless** (joining them back gives exactly $R$, with no spurious rows) and, ideally, **dependency preserving** (every original dependency can be checked inside one of the smaller tables).

Lossless test for a binary split: the common attributes $R_1\\cap R_2$ must determine all of $R_1$ or all of $R_2$, i.e. $R_1\\cap R_2\\to R_1$ or $R_1\\cap R_2\\to R_2$.

A decomposition into **BCNF** is always lossless but may lose dependency preservation. A decomposition into **3NF** can always be made both lossless and dependency preserving, which is why 3NF is often the practical goal.
"""),
)

elab("dbms-indexing",
 ("The problem indexes solve", """
A table is stored on disk in fixed-size **blocks**. Reading a block from disk is thousands of times slower than reading memory, so the cost of a query is mostly the **number of block accesses**. Without help, finding a row means scanning every block of the table.

An **index** is a separate, smaller structure that maps search-key values to the location of the rows, like the index at the back of a book. With a good index you read a handful of blocks instead of the whole file.
"""),
 ("Types of indexes", """
- **Primary index:** on the field by which the file is physically sorted and which is a key; usually **sparse** (one entry per block).
- **Clustering index:** on a sorted, non-key field.
- **Secondary index:** on a non-ordering field; must be **dense** (an entry for every record) because the file is not sorted by it.

A **dense** index has an entry for every record; a **sparse** index has entries for only some (one per block). Calculations typically ask for the number of blocks needed. With block size $B$, record size $R$, the **blocking factor** is $bf=\\lfloor B/R\\rfloor$ records per block, and a file of $n$ records occupies $\\lceil n/bf\\rceil$ blocks. Searching a sorted file by binary search takes $\\lceil\\log_2(\\text{blocks})\\rceil$ block accesses.
"""),
 ("B-trees and B+ trees", """
Databases use **B+ trees**, balanced multiway trees whose nodes are as large as a disk block. In a B+ tree of order $p$ each internal node holds up to $p$ child pointers and $p-1$ keys; **all records (or record pointers) are in the leaves**, and the leaves are linked in order, so range queries are efficient.

Because each node has a large fan-out (hundreds of children), the tree is very short: three levels can index millions of rows, so a lookup needs only about 3–4 block reads. Insertion splits a full node and pushes a key upward; deletion may merge nodes. In a **B-tree** keys and data may also appear in internal nodes, which makes searches slightly shorter but range scans less convenient.
"""),
)

elab("dbms-transactions-serializability",
 ("What a transaction is", """
A **transaction** is a group of database operations that must be treated as one unit: transferring money means subtracting from one account *and* adding to another, and doing only half would be wrong. The guarantees a DBMS gives are called **ACID**:

- **Atomicity:** all of the transaction happens or none of it does.
- **Consistency:** the database moves from one valid state to another, respecting all rules.
- **Isolation:** concurrent transactions do not see each other's half-finished work.
- **Durability:** once committed, the effect survives crashes.
"""),
 ("Schedules and conflicts", """
When several transactions run together, the interleaving of their reads and writes is a **schedule**. A **serial** schedule runs one transaction at a time and is always correct; we want interleaved schedules that give the same result as some serial one.

Two operations **conflict** if they belong to different transactions, touch the same item, and at least one is a write. A schedule is **conflict serializable** if it can be turned into a serial schedule by swapping adjacent non-conflicting operations.
"""),
 ("The precedence graph test", """
To test conflict serializability, build a **precedence graph**: one node per transaction, and an edge $T_i\\to T_j$ whenever an operation of $T_i$ conflicts with and comes *before* an operation of $T_j$. The schedule is conflict serializable **if and only if the graph has no cycle**. A topological order of the graph gives an equivalent serial order.

Anomalies from poor isolation: **dirty read** (reading uncommitted data), **non-repeatable read**, **lost update**, and **phantom read**. A schedule is **recoverable** if a transaction commits only after every transaction it read from has committed; it is **cascadeless** if transactions read only committed data; and **strict** if no item is read or overwritten until the last writer commits.
"""),
)

elab("dbms-concurrency-recovery",
 ("Locking to enforce isolation", """
Instead of testing schedules afterwards, a DBMS prevents bad ones by **locking**. A **shared (S) lock** allows reading, several transactions can hold S locks on one item; an **exclusive (X) lock** allows writing and excludes all others. A transaction must hold the right lock before it accesses an item.

**Two-phase locking (2PL)** requires every transaction to have a **growing phase** (acquire locks, never release) followed by a **shrinking phase** (release locks, never acquire). 2PL guarantees conflict serializability. **Strict 2PL** holds all exclusive locks until the transaction ends, which also gives strict schedules and avoids cascading aborts. 2PL does not prevent **deadlock**.
"""),
 ("Timestamps and deadlocks", """
In **timestamp ordering**, each transaction gets a timestamp when it starts; every item remembers the largest read and write timestamps that touched it, and an operation that would violate timestamp order causes the transaction to abort and restart. It never deadlocks but may restart many times.

A **deadlock** happens when transactions wait for each other in a cycle; it is detected with a **wait-for graph** (a cycle means deadlock) and resolved by aborting a victim. It can be prevented with **wait–die** and **wound–wait** schemes based on timestamps.
"""),
 ("Recovery after a crash", """
To provide atomicity and durability the DBMS writes a **log** of changes. The **write-ahead logging (WAL)** rule says the log record must reach disk *before* the changed data page does. After a crash the system uses the log in three steps: **analysis** (find what was active), **redo** (repeat the changes of committed transactions), and **undo** (roll back the changes of uncommitted ones). A **checkpoint** periodically records the state so recovery need not start from the beginning of the log.
"""),
)
