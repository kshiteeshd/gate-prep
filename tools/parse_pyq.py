"""Parse the PW 'GATE CSE topic-wise PYQs 2008-2023' text (tools/pdf_cols.py output) into question records.
   usage: python tools/parse_pyq.py data_check/txt/pw_cols.txt content/pyq_cs.json
   Only cleanly parsed questions are kept (options present, answer found, no figure/table dependence, no garbled math)."""
import hashlib
import json
import re
import sys
import unicodedata

SUBJ_ORDER = [("DBMS", 5), ("OS", 5), ("CN", 6), ("COA", 5), ("PDS", 8), ("ALGO", 6), ("CD", 7), ("TOC", 6), ("DL", 4), ("ENGM", 4)]

QH = re.compile(r"^\s*(\d+)\s*\.\s*\[\s*(MCQ|NAT|MSQ)\s*\]\s*\[\s*GATE\s*-\s*([\d\s]+?)\s*(?:\([^)]*\))?\s*:\s*(\d)\s*M\s*\]\s*$")
AH = re.compile(r"^\s*(\d+)\s*\.\s*\(\s*([a-dA-D](?:\s*[,;&]\s*[a-dA-D])*|[-+]?\d[\d.,]*(?:\s*to\s*[-+]?\d[\d.,]*)?)\s*\)\s*(.*)$")
CH = re.compile(r"^\s*C\s*H\s*A\s*P\s*T\s*E\s*R\s*$")
NOISE = re.compile(r"GATE Wallah|^\s*\d+\.\d+\s*$|^<<PAGE|^\s*Key Concepts\s*$|^\f|Embedded QR", re.I)
BAD = re.compile(r"[�-]|figure|diagram|graph shown|shown below|following graph|image|picture|table below|following table|given below in the table|as shown|following (circuit|network|tree|dfa|nfa|automaton|pda|machine|flow ?chart|code fragment is shown)", re.I)
HEAD = re.compile(r"^(?:[A-Z][A-Za-z&/()\-]*)(?:\s+(?:[A-Z][A-Za-z&/()\-]*|of|and|in|the|to|for|on|with|from|vs|&|\(.*\)))+$")


VOCAB = {}


def build_vocab(paths):
    from collections import Counter
    c = Counter()
    for p in paths:
        for w in re.findall(r"[A-Za-z]{2,}", open(p, encoding="utf-8").read().lower()):
            c[w] += 1
    VOCAB.update(c)


def fix_spaces(t):
    """re-join words split by the PDF extractor ('sur gery', 'orde r', 'in dustrial')"""
    if not VOCAB:
        return t
    toks = t.split(" ")
    out, i = [], 0
    while i < len(toks):
        a = toks[i]
        if i + 1 < len(toks) and a.isalpha() and toks[i + 1].isalpha():
            b = toks[i + 1]
            j = (a + b).lower()
            fa, fb, fj = VOCAB.get(a.lower(), 0), VOCAB.get(b.lower(), 0), VOCAB.get(j, 0)
            if fj >= 3 and fj >= 0.5 * min(max(fa, 1), max(fb, 1)) and (min(fa, fb) < 40 or min(len(a), len(b)) <= 2) and not (fa > 400 and fb > 400):
                out.append(a + b)
                i += 2
                continue
        out.append(a)
        i += 1
    return " ".join(out)


def norm(s):
    s = fix_spaces(unicodedata.normalize("NFKC", s))
    s = s.replace("→", "→")
    s = re.sub(r"[ \t]+", " ", s).strip()
    return s


def load(path):
    return [l.rstrip("\n") for l in open(path, encoding="utf-8").read().split("\n")]


SUBJ_HDR = [("DBMS", r"Database Management System"), ("OS", r"Operating Systems?"), ("CN", r"Computer Networks?"), ("COA", r"Computer Organi[sz]ation(?: and Architecture)?"),
            ("PDS", r"Programming and|Programming and Data Structures?|Data Structures?"), ("ALGO", r"Algorithms?"), ("CD", r"Compiler(?: Design)?"),
            ("TOC", r"Theory of Computation"), ("DL", r"Digital Logic"), ("ENGM", r"Discrete Mathematics")]


def segments(lines):
    """[(subject, chapter_lines)] — walks the known chapter sequence (subject, chapter no.) of the book"""
    expected = [(c, n) for c, k in SUBJ_ORDER for n in range(1, k + 1)]
    segs, cur, e = [], None, 0
    for i, l in enumerate(lines):
        if CH.match(l) and e < len(expected):
            seen, j = [], i + 1
            while j < len(lines) and len(seen) < 3:
                if lines[j].strip():
                    seen.append(lines[j].strip())
                j += 1
            hit = next((k for k in range(e, min(e + 3, len(expected))) if str(expected[k][1]) in seen), None)
            if hit is not None:
                cur = (expected[hit][0], [])
                segs.append(cur)
                e = hit + 1
                continue
        if cur is not None:
            cur[1].append(l)
    return segs


def split_blocks(chapter):
    """returns (questions {n: (type, year, marks, lines)}, answers {n: (ans, explanation lines)})"""
    qs, ans = {}, {}
    cur = None
    expanded = []
    for l in chapter:
        parts = re.split(r"(?<=\S)\s+(?=\d(?:\s?\d)?\s*\.\s*\[\s*(?:MCQ|NAT|MSQ)\s*\]\s*\[\s*GATE)", l)
        expanded.extend(parts)
    for l in expanded:
        if NOISE.search(l):
            continue
        m = QH.match(l)
        if m:
            n = int(m.group(1))
            year = int(re.sub(r"\s", "", m.group(3))[:4]) if re.sub(r"\s", "", m.group(3))[:4].isdigit() else 0
            cur = ("q", n)
            qs[n] = {"type": m.group(2), "year": year, "marks": int(m.group(4)), "lines": []}
            continue
        a = AH.match(l)
        if a and (cur is None or cur[0] != "q" or True):
            n = int(a.group(1))
            # an answer header is only accepted when it looks like a solution (not an option line such as "1. (a)")
            if n not in ans and n in qs or n in qs and not ans.get(n):
                cur = ("a", n)
                ans[n] = {"ans": a.group(2), "lines": [a.group(3)] if a.group(3) else []}
                continue
        if cur:
            (qs[cur[1]] if cur[0] == "q" else ans[cur[1]])["lines"].append(l)
    return qs, ans


def split_options(text_lines):
    text = "\n".join(text_lines)
    text = re.sub(r"[ \t]+", " ", text)
    # find option markers (a) (b) (c) (d) in order
    pos, last = [], -1
    for letter in "abcd":
        m = re.search(r"(?:^|[\s)])\(\s*%s\s*\)\s" % letter, text[last + 1:])
        if not m:
            return text.strip(), None
        s = last + 1 + m.start()
        # position of the '(' itself
        s = text.index("(", s)
        pos.append(s)
        last = s
    stem = text[:pos[0]].strip()
    opts = []
    for i, s in enumerate(pos):
        e = pos[i + 1] if i + 1 < len(pos) else len(text)
        o = re.sub(r"^\(\s*[a-d]\s*\)\s*", "", text[s:e].strip())
        opts.append(o)
    # strip a trailing sub-topic heading glued to the last option
    ol = opts[-1].split("\n")
    if len(ol) > 1 and HEAD.match(ol[-1].strip()) and len(ol[-1].split()) >= 2 and not ol[-1].strip().endswith((".", "?", ")")) :
        ol = ol[:-1]
    opts[-1] = "\n".join(ol)
    opts = [norm(re.sub(r"\s*\n\s*", " ", o)) for o in opts]
    # the last option may have page footers / next-section headings glued on: keep only its first logical line
    last = opts[-1]
    last = re.split(r"\s+\d+\s*\.\s*\d+(?:\s|$)|\s+of springs|\s+System C all|\s+Common [Dd]ata|\s+[A-Z]{2}\s+[A-Z]{2}\s|\s+[❑□]|\s+\d+\s*\.\s*\(|\s+\d\s*\.\s*\[", last)[0]
    last = re.sub(r"[\s❑□]*\d?\s*$", "", last).strip()
    # a trailing run of capitalised words with no punctuation after a complete sentence/option is a section heading
    m = re.match(r"^(.*[.)\]}'\"\d])\s+([A-Z][\w&/()-]*(?:\s+[A-Za-z&/()-]+){1,5})$", last)
    if m and m.group(2).split()[0][0].isupper() and len(m.group(2).split()) >= 2 and not re.search(r"\b(is|are|the|a|an|to|of)\b$", m.group(2)):
        if re.search(r"(Analysis|Syntax|Database|Network|Algorithm|Process|Memory|Transaction|Trees?|Graph|Flow|Solution|Operating|Computer|Systems?|Synchroni\w*)", m.group(2)):
            last = m.group(1)
    others = max(len(o) for o in opts[:-1]) if opts[:-1] else 0
    if others and len(last) > max(70, 3 * others):
        return stem, None
    opts[-1] = last
    return stem, opts


def clean_stem(s):
    s = re.sub(r"\n\s*\n", "\n", s)
    ls = [norm(x) for x in s.split("\n") if x.strip()]
    while ls and re.fullmatch(r"\d{1,3}", ls[-1]):
        ls.pop()
    return "\n".join(ls).strip()


def truncated(stem, qtype):
    return qtype == "NAT" and not re.search(r"(\?|\.|:|_|\)|;|-)\s*$", stem.rstrip())


KEYS = {
    "DBMS": [("Indexing & File Organization", r"b\+? ?tree|b-tree|index|blocking factor|disk block|file organi|hashing|record size|sparse|dense"),
             ("Transactions & Concurrency", r"schedule|serializab|transaction|two.phase|2pl|recoverab|timestamp|lock|commit|rollback|log record|checkpoint|deadlock"),
             ("SQL", r"select |from |where |group by|having|sql|inner join|outer join|nested quer|trigger|view "),
             ("Relational Algebra & Calculus", r"relational algebra|relational calculus|tuple calculus|σ|π|⋈|natural join|projection|selection operator|division"),
             ("Functional Dependencies & Normalization", r"functional dependenc|candidate key|normal form|bcnf|3nf|2nf|decomposition|lossless|closure|minimal cover|superkey|super key|fd set|→"),
             ("ER Model", r"entity|er model|er diagram|relationship set|cardinality|participation|weak entity|foreign key|primary key|relational schema|tables? .*required")],
    "OS": [("Deadlocks", r"deadlock|banker|resource allocation|safe state"),
           ("Synchronization", r"semaphore|mutex|critical section|peterson|monitor|race condition|test.and.set|wait\(|signal\("),
           ("CPU Scheduling", r"schedul|turnaround|waiting time|round robin|sjf|fcfs|priority|quantum|burst"),
           ("File Systems & Disk Scheduling", r"disk|file system|inode|sector|cylinder|seek|raid|block pointer|directory|fat "),
           ("Memory Management & Paging", r"page|frame|tlb|segment|virtual|memory|thrash|fragmentation|swap|translation|belady"),
           ("Processes, Threads & Syscalls", r"fork|process|thread|system call|interrupt|context switch|kernel|zombie|orphan")],
    "CN": [("IP Addressing & Subnetting", r"subnet|ip address|cidr|netmask|ipv4|ipv6|fragment|mtu|header length|datagram|nat |arp|dhcp|icmp|class [abc]"),
           ("Routing", r"routing|rip |ospf|bgp|distance vector|link state|bellman|dijkstra|router"),
           ("Transport Layer (TCP/UDP)", r"tcp|udp|congestion|window|slow start|sequence number|handshake|port|segment|rtt"),
           ("MAC & Ethernet", r"ethernet|csma|aloha|collision|mac |token|switch|bridge|vlan|backoff|frame size|slot"),
           ("Data Link & Error Control", r"crc|hamming|parity|checksum|sliding window|go.back|selective repeat|stop.and.wait|error|framing|stuffing|generator polynomial"),
           ("Application Layer & Security", r"http|smtp|dns|ftp|pop|imap|rsa|aes|des |cipher|encrypt|signature|hash|firewall|ssl|tls|email|e-mail|url|cookie"),
           ("Layering & Physical Layer", r"osi|layer|bandwidth|latency|propagation|transmission delay|nyquist|shannon|snr|baud|encoding|manchester|multiplex|throughput")],
    "COA": [("Pipelining", r"pipelin|hazard|stall|forwarding|speedup|stage"),
            ("Cache & Memory Hierarchy", r"cache|tag|hit ratio|miss|associative|block size|main memory|interleav|memory access time|virtual memory"),
            ("I/O, Interrupts & DMA", r"dma|interrupt|i/o|io device|polling|bus |transfer rate"),
            ("Datapath & Control Unit", r"microprogram|control (word|unit|store)|hardwired|micro-?operation|microinstruction|datapath|register transfer|alu|control signal"),
            ("Instruction Formats & Addressing Modes", r"addressing mode|instruction format|opcode|effective address|operand|register|instruction|isa|risc|cisc|cpi|mips|clock")],
    "PDS": [("Heaps & Hashing", r"hash|heap|priority queue|collision|probing|chaining"),
            ("Trees & BST", r"binary tree|bst|search tree|avl|tree|inorder|preorder|postorder|traversal|height"),
            ("Graph Representation", r"adjacency|incidence|graph"),
            ("Linked Lists", r"linked list|node|pointer to|next pointer|list"),
            ("Arrays, Stacks & Queues", r"stack|queue|array|push|pop|enqueue|dequeue|circular"),
            ("Recursion", r"recurs|function call|f\(n\)|factorial|fibonacci"),
            ("C Programming & Pointers", r"printf|int |char |pointer|\*p|malloc|struct|union|static|void|main\(|#define|sizeof|output of|program")],
    "ALGO": [("Complexity Classes", r"np-?(hard|complete)|p = np|polynomial time|reduction|sat\b|decidab|vertex cover|clique|hamiltonian"),
             ("Graph Algorithms", r"dijkstra|bellman|floyd|bfs|dfs|breadth|depth first|spanning|prim|kruskal|shortest path|topological|strongly connected|graph"),
             ("Dynamic Programming", r"dynamic programming|knapsack|matrix chain|lcs|longest common|memoiz|optimal substructure|edit distance|subproblem"),
             ("Greedy Algorithms", r"greedy|huffman|activity selection|job sequencing|fractional"),
             ("Sorting & Searching", r"sort|merge|quick|binary search|heap|selection|insertion|bubble|median|partition|comparison"),
             ("Recurrences & Divide and Conquer", r"recurrence|master theorem|divide and conquer|t\(n\)|strassen|closest pair"),
             ("Asymptotic Analysis", r"asymptotic|big.?o|θ|ω|growth|time complexity|order of|o\(|loop")],
    "CD": [("Lexical Analysis", r"lexical|token|lexeme|regular expression|lex |scanner|input buffer"),
           ("Parsing (LL & LR)", r"parser|parsing|ll\(1\)|lr|slr|lalr|first|follow|shift|reduce|grammar|ambiguous|left recursion|handle|production"),
           ("Syntax-Directed Translation", r"syntax.directed|attribute|synthesized|inherited|translation scheme|sdt|sdd"),
           ("Intermediate Code & Runtime", r"three.address|intermediate|quadruple|triple|activation record|runtime|stack frame|parameter passing|call by|scope|symbol table"),
           ("Code Optimization & Data Flow", r"optimi|basic block|live variable|data.flow|dead code|common subexpression|register allocation|available expression|reaching definition|loop")],
    "TOC": [("Turing Machines & Decidability", r"turing|decidab|undecidab|recursive|halting|rice|reduction|recursively enumerable|np"),
            ("Context-Free Languages & PDA", r"context.free|pushdown|pda|cfg|cfl|chomsky|ambiguous|derivation|parse tree"),
            ("Closure & Pumping Lemma", r"pumping|closure|closed under|complement|intersection|union of|homomorphism"),
            ("Regular Languages & Finite Automata", r"dfa|nfa|finite automat|regular|minimal|myhill|states|regex|expression")],
    "DL": [("Sequential Circuits", r"flip.?flop|latch|counter|register|sequential|clock|shift register|state machine|mealy|moore|jk|\bt flip"),
           ("Number Systems & Arithmetic", r"complement|ieee|floating|binary number|bcd|overflow|gray|radix|excess|decimal|hexadecimal|octal|sign"),
           ("Combinational Circuits", r"multiplexer|mux|decoder|encoder|adder|subtractor|comparator|half adder|full adder|rom|pla|combinational|carry"),
           ("Boolean Algebra & Minimization", r"boolean|minimi|k-?map|sop|pos|minterm|maxterm|prime implicant|simplif|nand|nor|gate|expression")],
    "ENGM": [("Partial Orders & Lattices", r"lattice|poset|partial order|hasse|lub|glb|maximal element"),
             ("Groups & Monoids", r"group|monoid|subgroup|abelian|cyclic|semigroup|isomorphi"),
             ("Propositional & First-Order Logic", r"propositional|predicate|logic|tautolog|satisf|∀|∃|quantifier|valid|implies|equivalent|modus"),
             ("Graph Theory", r"graph|vertex|vertices|edge|degree|planar|chromatic|tree|euler|hamilton|connected|bipartite|matching"),
             ("Combinatorics & Recurrences", r"permutation|combination|ways|arrange|recurrence|pigeonhole|inclusion|binomial|generating function|counting|derangement|choose"),
             ("Sets, Relations & Functions", r"relation|function|set|reflexive|symmetric|transitive|equivalence|injective|surjective|bijective|cardinality|partition|power set")],
}
DEFAULT_TOPIC = {"DBMS": "ER Model", "OS": "Processes, Threads & Syscalls", "CN": "Layering & Physical Layer", "COA": "Instruction Formats & Addressing Modes",
                 "PDS": "C Programming & Pointers", "ALGO": "Asymptotic Analysis", "CD": "Parsing (LL & LR)", "TOC": "Regular Languages & Finite Automata",
                 "DL": "Boolean Algebra & Minimization", "ENGM": "Sets, Relations & Functions"}


def garbled(stem, options):
    txt = [stem] + options
    if any(re.fullmatch(r"[\d\s]+", ln.strip()) and len(ln.strip()) <= 14 for ln in stem.split("\n")):
        return True
    for t in txt:
        if re.search(r"(?:^|\s)(?:[A-Za-z0-9]\s){2,}[A-Za-z0-9]?(?:\s|$)", t) and not re.search(r"O\(|\d\s*[+*/-]", t[:0]):
            return True
        if re.search(r"(?:\s[a-z0-9]){3,}\s*$", t):
            return True
        if re.search(r"[a-z]{3,} (?:s|ed|es|ing|ly|ion|ent|er|ers|ant)", t):
            return True
        if t.count("{") != t.count("}") or t.count("(") != t.count(")") or t.count("[") != t.count("]"):
            return True
        if re.search(r"\[\s*(MCQ|NAT|MSQ)\s*\]|GATE\s*-", t):
            return True
    return False


def clean_expl(lines):
    t = " ".join(norm(x) for x in lines if x.strip())
    t = re.sub(r"\s+", " ", t).strip()
    if 25 <= len(t) <= 700 and not garbled(t, []) and not BAD.search(t):
        return t
    return ""


def topic_of(subject, text):
    t = text.lower()
    best, bs = None, 0
    for name, pat in KEYS.get(subject, []):
        n = len(re.findall(pat, t))
        if n > bs:
            best, bs = name, n
    return best or DEFAULT_TOPIC[subject]


def parse_answer(raw, qtype, options):
    raw = raw.strip()
    if qtype == "NAT":
        m = re.fullmatch(r"([-+]?\d[\d.,]*)(?:\s*to\s*([-+]?\d[\d.,]*))?", raw)
        if not m:
            return None
        try:
            lo = float(m.group(1).replace(",", ""))
            hi = float(m.group(2).replace(",", "")) if m.group(2) else lo
        except ValueError:
            return None
        return {"numeric": (lo + hi) / 2, "tol": abs(hi - lo) / 2 + 1e-9}
    letters = [x.lower() for x in re.findall(r"[a-dA-D]", raw)]
    if not letters or not options:
        return None
    if qtype == "MCQ" and len(letters) != 1:
        return None
    return {"answer": [options["abcd".index(x)] for x in letters]}


def main(src, dst):
    build_vocab([src.replace("pw_cols", "pw_cols"), src.replace("pw_cols", "ma_cols")])
    lines = load(src)
    segs = segments(lines)
    out, stats = [], {"seen": 0, "no_opts": 0, "no_ans": 0, "bad": 0, "garbled": 0, "chapters": len(segs)}
    for subject, ch in segs:
        qs, ans = split_blocks(ch)
        for n, q in sorted(qs.items()):
            stats["seen"] += 1
            stem_raw = q["lines"]
            if q["type"] == "NAT":
                stem, options = clean_stem("\n".join(stem_raw)), []
            else:
                stem, options = split_options(stem_raw)
                if options is None:
                    stats["no_opts"] += 1
                    continue
                stem = clean_stem(stem)
            full = stem + " " + " ".join(options)
            if truncated(stem, q["type"]) or stem.split("\n")[0].strip().isdigit():
                stats["bad"] += 1
                continue
            if garbled(stem, options):
                stats["garbled"] += 1
                continue
            if re.search(r"Hardware Solution|Operators$|Syntax Analysis|Data Flow Analysis|Common Data|^255\.255\.$|p t hat", options[-1] if options else ""):
                stats["bad"] += 1
                continue
            if BAD.search(full) or len(stem) < 25 or any(len(o) == 0 for o in options):
                stats["bad"] += 1
                continue
            if n not in ans:
                stats["no_ans"] += 1
                continue
            pa = parse_answer(ans[n]["ans"], q["type"], options)
            if not pa:
                stats["no_ans"] += 1
                continue
            topic = topic_of(subject, full)
            marks = q["marks"]
            rec = {"qtype": {"MCQ": "single", "MSQ": "multiple", "NAT": "numerical"}[q["type"]], "text": stem, "options": options,
                   "answer": pa.get("answer", []), "subject": subject, "topic": topic, "subtopic": "GATE %d" % q["year"],
                   "diff": "medium" if marks == 1 else "hard", "marks": marks, "src": "GATE %d" % q["year"],
                   "neg": 0 if q["type"] != "MCQ" else (0.33 if marks == 1 else 0.66), "pool": "test",
                   "expl": "Official GATE %d answer: %s." % (q["year"], (" / ".join(options["abcd".index(x)] for x in re.findall("[a-d]", ans[n]["ans"].lower())) if options else ans[n]["ans"].strip().replace(" to ", " – ")))}
            ce = clean_expl(ans[n]["lines"])
            if ce:
                rec["expl"] += " " + ce
            if "numeric" in pa:
                rec["numeric"], rec["tol"] = pa["numeric"], pa["tol"]
            rec["id"] = "pyq" + hashlib.sha1((subject + stem + "|".join(options)).encode("utf-8")).hexdigest()[:10]
            out.append(rec)
    json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(stats, "kept", len(out))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
