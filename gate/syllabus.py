"""GATE CS syllabus: subjects -> topics. Topic names here are the single source of truth."""

SUBJECTS = [
    # code, name, glyph, colour, full-test questions (of the 55 CS marks-questions)
    dict(code="ENGM", name="Engineering Mathematics", glyph="∑", color="#8b5cf6", fq=9),
    dict(code="DL", name="Digital Logic", glyph="⊕", color="#06b6d4", fq=3),
    dict(code="COA", name="Computer Organization & Architecture", glyph="⌬", color="#f59e0b", fq=5),
    dict(code="PDS", name="Programming & Data Structures", glyph="{ }", color="#10b981", fq=5),
    dict(code="ALGO", name="Algorithms", glyph="O(n)", color="#ef4444", fq=6),
    dict(code="TOC", name="Theory of Computation", glyph="δ", color="#ec4899", fq=5),
    dict(code="CD", name="Compiler Design", glyph="λ", color="#14b8a6", fq=4),
    dict(code="OS", name="Operating Systems", glyph="⚙", color="#3b82f6", fq=6),
    dict(code="DBMS", name="Databases", glyph="DB", color="#f97316", fq=6),
    dict(code="CN", name="Computer Networks", glyph="⇄", color="#22c55e", fq=6),
    dict(code="GA", name="General Aptitude", glyph="Aa", color="#a855f7", fq=0),
]

TOPICS = {
    "ENGM": ["Propositional & First-Order Logic", "Sets, Relations & Functions", "Partial Orders & Lattices",
             "Groups & Monoids", "Graph Theory", "Combinatorics & Recurrences", "Matrices & Determinants",
             "Linear Equations & Eigenvalues", "Limits, Continuity & Differentiation", "Maxima, Minima & Integration",
             "Probability Basics & Bayes", "Random Variables & Distributions"],
    "DL": ["Boolean Algebra & Minimization", "Combinational Circuits", "Number Systems & Arithmetic",
           "Sequential Circuits"],
    "COA": ["Instruction Formats & Addressing Modes", "Datapath & Control Unit", "Pipelining",
            "Cache & Memory Hierarchy", "I/O, Interrupts & DMA"],
    "PDS": ["C Programming & Pointers", "Recursion", "Arrays, Stacks & Queues", "Linked Lists",
            "Trees & BST", "Heaps & Hashing", "Graph Representation"],
    "ALGO": ["Asymptotic Analysis", "Recurrences & Divide and Conquer", "Sorting & Searching", "Greedy Algorithms",
             "Dynamic Programming", "Graph Algorithms", "Complexity Classes"],
    "TOC": ["Regular Languages & Finite Automata", "Context-Free Languages & PDA", "Closure & Pumping Lemma",
            "Turing Machines & Decidability"],
    "CD": ["Lexical Analysis", "Parsing (LL & LR)", "Syntax-Directed Translation", "Intermediate Code & Runtime",
           "Code Optimization & Data Flow"],
    "OS": ["Processes, Threads & Syscalls", "CPU Scheduling", "Synchronization", "Deadlocks",
           "Memory Management & Paging", "File Systems & Disk Scheduling"],
    "DBMS": ["ER Model", "Relational Algebra & Calculus", "SQL", "Functional Dependencies & Normalization",
             "Indexing & File Organization", "Transactions & Concurrency"],
    "CN": ["Layering & Physical Layer", "Data Link & Error Control", "MAC & Ethernet", "IP Addressing & Subnetting",
           "Routing", "Transport Layer (TCP/UDP)", "Application Layer & Security"],
    "GA": ["Verbal Ability", "Numerical Ability", "Logical & Analytical Reasoning", "Data Interpretation"],
}

DIFFS = ["easy", "medium", "hard"]
SUBJECT_BY_CODE = {s["code"]: s for s in SUBJECTS}

# legacy folder names -> (subject, topic) mapping used by the importer
LEGACY_MAP = {
    ("Maths", "Calculus"): ("ENGM", "Limits, Continuity & Differentiation"),
    ("Maths", "Combinatorics"): ("ENGM", "Combinatorics & Recurrences"),
    ("Maths", "Graph_Theory"): ("ENGM", "Graph Theory"),
    ("Maths", "Groups_Lattices"): ("ENGM", "Groups & Monoids"),
    ("Maths", "Linear_Algebra"): ("ENGM", "Linear Equations & Eigenvalues"),
    ("Maths", "Logic_Sets_Relations"): ("ENGM", "Sets, Relations & Functions"),
    ("Maths", "Probability"): ("ENGM", "Probability Basics & Bayes"),
    ("DBMS", "Concurrency_and_Recovery"): ("DBMS", "Transactions & Concurrency"),
    ("DBMS", "ER_Model"): ("DBMS", "ER Model"),
    ("DBMS", "File_Organization"): ("DBMS", "Indexing & File Organization"),
    ("DBMS", "Indexing_and_B_Trees"): ("DBMS", "Indexing & File Organization"),
    ("DBMS", "Keys_and_Constraints"): ("DBMS", "Functional Dependencies & Normalization"),
    ("DBMS", "Normalization"): ("DBMS", "Functional Dependencies & Normalization"),
    ("DBMS", "Relational_Algebra"): ("DBMS", "Relational Algebra & Calculus"),
    ("DBMS", "SQL"): ("DBMS", "SQL"),
    ("DBMS", "Transactions"): ("DBMS", "Transactions & Concurrency"),
    ("DBMS", "Tuple_Calculus"): ("DBMS", "Relational Algebra & Calculus"),
    ("CN", "Application_Layer"): ("CN", "Application Layer & Security"),
    ("CN", "Data_Link"): ("CN", "Data Link & Error Control"),
    ("CN", "IP_Addressing"): ("CN", "IP Addressing & Subnetting"),
    ("CN", "Layering_Switching"): ("CN", "Layering & Physical Layer"),
    ("CN", "MAC_Ethernet"): ("CN", "MAC & Ethernet"),
    ("CN", "Routing"): ("CN", "Routing"),
    ("CN", "Support_NAT"): ("CN", "IP Addressing & Subnetting"),
    ("CN", "TCP_UDP"): ("CN", "Transport Layer (TCP/UDP)"),
}
