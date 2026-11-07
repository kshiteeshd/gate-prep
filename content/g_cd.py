"""Compiler Design — parametric generators."""
import re

from content.kit import *

S = "CD"
LX, PS, SD, IC, OP = ("Lexical Analysis", "Parsing (LL & LR)", "Syntax-Directed Translation", "Intermediate Code & Runtime", "Code Optimization & Data Flow")

# ---------------- lexical ----------------
TOK = re.compile(r"\s*(?:(?P<num>\d+\.\d+|\d+)|(?P<id>[A-Za-z_]\w*)|(?P<str>\"[^\"]*\")|(?P<op>\+\+|--|==|!=|<=|>=|&&|\|\||\+=|-=|\*=|/=|<<|>>|->|[-+*/%=<>!&|^~?:;,.(){}\[\]#]))")


def tokens(src):
    pos, out = 0, []
    while pos < len(src):
        m = TOK.match(src, pos)
        if not m: break
        if m.group(0).strip() == "" : break
        out.append(m.group(0).strip())
        pos = m.end()
    return out


SNIPS = ["for (i = 0; i < %d; i++) s += a[i] * %d;", "if (x >= %d && y != %d) z = x - y;", "while (n > %d) { n = n / 2; c++; }", "int %s = %d, %s = %d;",
         "printf(\"%%d\", %s + %d);", "%s = %s++ + %d;", "a[%d] = b[%d] <= c ? %d : %d;", "x = y<<%d | z>>%d;", "p->next = q->val + %d;", "return %s * (%d + %s);"]


@gen(S, LX, "Token counting", n=90, diff="easy")
def lx_tokens(r):
    t = r.choice(SNIPS)
    names = ["alpha", "beta", "cnt", "sum", "k", "tmp", "idx"]
    args = []
    for ph in re.findall(r"%[ds]", t.replace("%%d", "")):
        args.append(r.choice(names) if ph == "%s" else r.randint(2, 99))
    try:
        src = t % tuple(args)
    except TypeError:
        raise Skip()
    n = len(tokens(src))
    return nat(r, "How many tokens will a C lexer (maximal munch) produce for the statement below? (Count every identifier, keyword, constant, operator and punctuator; string literals are one token.)\n```c\n%s\n```" % src, n,
               "Tokens: %s" % " ".join("[%s]" % x for x in tokens(src)))


@gen(S, LX, "Maximal munch", n=20, diff="medium")
def lx_munch(r):
    c = [("a+++b", ["a", "++", "+", "b"]), ("x---y", ["x", "--", "-", "y"]), ("a<<=b", ["a", "<<", "=", "b"]), ("p->q", ["p", "->", "q"]), ("a=+b", ["a", "=", "+", "b"]), ("i+++++j", ["i", "++", "++", "+", "j"]),
         ("x>=y", ["x", ">=", "y"]), ("a&&b||c", ["a", "&&", "b", "||", "c"]), ("1.5e3", ["1.5", "e3"]), ("a== b", ["a", "==", "b"])]
    src, toks = r.choice(c)
    got = tokens(src)
    return nat(r, "A lexer using the maximal-munch (longest match) rule scans  %s  with the token classes: identifiers, decimal numbers, and C operators of one or two characters (++ -- == != <= >= && || += -= *= /= << >> ->) and single-character operators. How many tokens are produced?" % src, len(got), "Tokens: %s." % got)


# ---------------- grammars ----------------
def G(txt):
    g = []
    for line in txt.strip().split(";"):
        lhs, rhs = line.split("→")
        for alt in rhs.split("|"):
            alt = alt.strip()
            g.append((lhs.strip(), [] if alt in ("ε", "") else alt.split()))
    return g


GRAMMARS = {
    "g1": G("E → T Ep ; Ep → + T Ep | ε ; T → F Tp ; Tp → * F Tp | ε ; F → ( E ) | id"),
    "g2": G("S → A a A b | B b B a ; A → ε ; B → ε"),
    "g3": G("S → i E t S Sp | a ; Sp → e S | ε ; E → b"),
    "g4": G("E → E + T | T ; T → T * F | F ; F → ( E ) | id"),
    "g5": G("S → L = R | R ; L → * R | id ; R → L"),
    "g6": G("S → C C ; C → c C | d"),
    "g7": G("S → A B ; A → a A | ε ; B → b B | b"),
    "g8": G("S → a S b | a b"),
    "g9": G("S → ( S ) S | ε"),
    "g10": G("S → a A | b B ; A → c A | d ; B → c B | e"),
    "g11": G("S → A ; A → A a | b"),
    "g12": G("E → E + E | E * E | id"),
    "g13": G("S → x S y | z"),
    "g14": G("S → a S | b"),
}


def nts(g):
    return {l for l, _ in g}


def first_follow(g, start):
    N = nts(g)
    first = {n: set() for n in N}
    nullable = set()
    ch = True
    while ch:
        ch = False
        for l, rhs in g:
            before = (len(first[l]), l in nullable)
            allnull = True
            for s in rhs:
                if s in N:
                    first[l] |= first[s]
                    if s not in nullable: allnull = False; break
                else:
                    first[l].add(s); allnull = False; break
            if allnull: nullable.add(l)
            if (len(first[l]), l in nullable) != before: ch = True
    follow = {n: set() for n in N}
    follow[start].add("$")
    ch = True
    while ch:
        ch = False
        for l, rhs in g:
            for i, s in enumerate(rhs):
                if s not in N: continue
                b = len(follow[s])
                nl = True
                for t in rhs[i + 1:]:
                    if t in N:
                        follow[s] |= first[t]
                        if t not in nullable: nl = False; break
                    else:
                        follow[s].add(t); nl = False; break
                if nl: follow[s] |= follow[l]
                if len(follow[s]) != b: ch = True
    return first, follow, nullable


def first_of(seq, first, nullable, N):
    out = set()
    for s in seq:
        if s in N:
            out |= first[s]
            if s not in nullable: return out, False
        else:
            out.add(s); return out, False
    return out, True


def ll1_table(g, start):
    N = nts(g)
    first, follow, nullable = first_follow(g, start)
    table, conflicts = {}, 0
    for i, (l, rhs) in enumerate(g):
        f, nl = first_of(rhs, first, nullable, N)
        for a in (f | (follow[l] if nl else set())):
            if (l, a) in table: conflicts += 1
            table[(l, a)] = table.get((l, a), set()) | {i}
    return table, conflicts


def lr0(g, start):
    N = nts(g)
    prods = [("S'", [start])] + g

    def closure(items):
        items = set(items)
        ch = True
        while ch:
            ch = False
            for (p, d) in list(items):
                rhs = prods[p][1]
                if d < len(rhs) and rhs[d] in N:
                    for j, (l, _) in enumerate(prods):
                        if l == rhs[d] and (j, 0) not in items:
                            items.add((j, 0)); ch = True
        return frozenset(items)

    def goto(I, X):
        return closure({(p, d + 1) for (p, d) in I if d < len(prods[p][1]) and prods[p][1][d] == X})
    I0 = closure({(0, 0)})
    states, q, trans = [I0], [I0], {}
    while q:
        I = q.pop(0)
        syms = {prods[p][1][d] for (p, d) in I if d < len(prods[p][1])}
        for X in sorted(syms):
            J = goto(I, X)
            if J not in states:
                states.append(J); q.append(J)
            trans[(states.index(I), X)] = states.index(J)
    return prods, states, trans


def lr_conflicts(g, start):
    N = nts(g)
    prods, states, trans = lr0(g, start)
    first, follow, nullable = first_follow(g, start)
    lr0c = slrc = 0
    for I in states:
        red = [(p, d) for (p, d) in I if d == len(prods[p][1]) and p != 0]
        shifts = {prods[p][1][d] for (p, d) in I if d < len(prods[p][1]) and prods[p][1][d] not in N}
        if red and (len(red) > 1 or shifts): lr0c += 1
        seen = set()
        bad = False
        for (p, d) in red:
            fl = follow[prods[p][0]]
            if fl & shifts or fl & seen: bad = True
            seen |= fl
        slrc += bad
    return len(states), lr0c, slrc


def gtxt(g):
    out = {}
    for l, rhs in g:
        out.setdefault(l, []).append(" ".join(rhs) or "ε")
    return "\n".join("%s → %s" % (l, " | ".join(v)) for l, v in out.items())


@gen(S, PS, "FIRST & FOLLOW", n=70, diff="medium")
def p_ff(r):
    name = r.choice(["g1", "g2", "g3", "g5", "g6", "g7", "g10", "g4"])
    g = GRAMMARS[name]
    first, follow, nullable = first_follow(g, g[0][0])
    X = r.choice(sorted(nts(g)))
    if r.random() < 0.5:
        return nat(r, "For the grammar (ε = empty string, start symbol %s)\n```\n%s\n```\nHow many terminals are in FIRST(%s)? (do not count ε)" % (g[0][0], gtxt(g), X), len(first[X]), "FIRST(%s) = {%s}." % (X, ", ".join(sorted(first[X]))))
    return nat(r, "For the grammar (start symbol %s)\n```\n%s\n```\nHow many symbols are in FOLLOW(%s)? (count $ if present)" % (g[0][0], gtxt(g), X), len(follow[X]), "FOLLOW(%s) = {%s}." % (X, ", ".join(sorted(follow[X]))))


@gen(S, PS, "LL(1)", n=40, diff="medium", marks=2)
def p_ll1(r):
    name = r.choice(list(GRAMMARS))
    g = GRAMMARS[name]
    t, conf = ll1_table(g, g[0][0])
    kind = r.choice(["is", "entries"])
    if kind == "is":
        return mcq(r, "Consider the grammar\n```\n%s\n```\nIs it LL(1)?" % gtxt(g), "Yes" if conf == 0 else "No", ["No" if conf == 0 else "Yes", "Yes, but only after left factoring", "Cannot be determined without FOLLOW sets"], "LL(1) table has %d multiply-defined entries." % conf)
    if conf: raise Skip()
    return nat(r, "For the LL(1) grammar\n```\n%s\n```\nHow many non-empty entries does its LL(1) parsing table contain?" % gtxt(g), len(t), "One entry per (non-terminal, lookahead) pair derived from FIRST/FOLLOW.")


@gen(S, PS, "LR parsing", n=60, diff="hard", marks=2)
def p_lr(r):
    name = r.choice(list(GRAMMARS))
    g = GRAMMARS[name]
    n, c0, cs = lr_conflicts(g, g[0][0])
    kind = r.choice(["states", "lr0c", "slr"])
    pre = "Consider the grammar\n```\n%s\n```\n(augmented with S' → %s)\n" % (gtxt(g), g[0][0])
    if kind == "states": return nat(r, pre + "How many states does the canonical LR(0) automaton have?", n, "Build closure/goto item sets: %d states." % n)
    if kind == "lr0c": return nat(r, pre + "In how many LR(0) states is there a shift-reduce or reduce-reduce conflict (LR(0) parsing, no lookahead)?", c0, "Count states containing a complete item together with another item.")
    return mcq(r, pre + "Is the grammar SLR(1)?", "Yes" if cs == 0 else "No", ["No" if cs == 0 else "Yes", "Only LALR(1)", "Only LL(1)"], "SLR(1) conflict states using FOLLOW sets: %d." % cs)


# ---------------- syntax-directed translation ----------------
def count_reductions(toks):
    """Number of reductions of a bottom-up parse for E→E+T|T, T→T*F|F, F→(E)|id."""
    pos = [0]
    cnt = [0]

    def E():
        T(); cnt[0] += 1
        while pos[0] < len(toks) and toks[pos[0]] == "+":
            pos[0] += 1; T(); cnt[0] += 1

    def T():
        F(); cnt[0] += 1
        while pos[0] < len(toks) and toks[pos[0]] == "*":
            pos[0] += 1; F(); cnt[0] += 1

    def F():
        t = toks[pos[0]]; pos[0] += 1
        if t == "(":
            E(); pos[0] += 1
        cnt[0] += 1
    E()
    return cnt[0]


def rand_expr(r, depth):
    if depth == 0 or r.random() < 0.35: return ["id"]
    k = r.choice([1, 2])
    out = []
    for i in range(k + 1):
        if i: out.append(r.choice("+*"))
        sub = rand_expr(r, depth - 1)
        out += (["("] + sub + [")"]) if len(sub) > 1 and r.random() < 0.4 else sub
    return out


@gen(S, SD, "Shift-reduce counts", n=80, diff="hard", marks=2)
def sd_reduce(r):
    t = rand_expr(r, 3)
    if len(t) < 4: raise Skip()
    sh, rd = len(t), count_reductions(t)
    s = " ".join(t)
    g = "E → E + T | T\nT → T * F | F\nF → ( E ) | id"
    if r.random() < 0.5: return nat(r, "Grammar:\n```\n%s\n```\nA bottom-up (LR) parser parses the string  %s . How many REDUCE actions are performed (the final acceptance step is not counted)?" % (g, s), rd, "Every production application in the parse tree is one reduction: %d." % rd)
    return nat(r, "Grammar:\n```\n%s\n```\nA shift-reduce parser parses  %s . How many SHIFT actions occur?" % (g, s), sh, "One shift per input token: %d." % sh)


def tree_value(r, ops=3):
    return None


@gen(S, SD, "Synthesized attributes", n=70, diff="medium")
def sd_eval(r):
    n = r.randint(3, 5)
    ops = [r.choice("+*-") for _ in range(n - 1)]
    vals = [r.randint(1, 9) for _ in range(n)]
    style = r.choice(["post", "pre"])
    expr = str(vals[0])
    for o, v in zip(ops, vals[1:]): expr += " %s %d" % (o, v)
    # SDT with E -> E1 + T {E.val = E1.val + T.val}; T -> T1 * F {T.val = T1.val * F.val}  (left assoc, * higher than + -)
    v = eval(expr)
    return nat(r, "Using the standard attribute grammar  E → E + T | E − T | T,  T → T * F | F,  F → num  with the usual semantic rules (val computed bottom-up), what is the value attribute of the root for the input  %s ?" % expr, v, "Standard precedence: evaluates to %d." % v)


@gen(S, SD, "Ambiguity & parse trees", n=15, diff="medium")
def sd_amb(r):
    k = r.randint(2, 7)
    from math import comb
    return nat(r, "For the ambiguous grammar E → E + E | id, how many distinct parse trees exist for the string consisting of %d occurrences of id separated by +?" % (k + 1), comb(2 * k, k) // (k + 1), "Catalan number C_%d." % k)


# ---------------- intermediate code & runtime ----------------
def rand_tac(r):
    n = r.randint(7, 11)
    labels = {}
    code = []
    ln = []
    for i in range(n):
        code.append(["x%d = a%d op b%d" % (i, i, i), "goto", "if", "assign"][0])
    k = r.randint(2, 3)
    pts = sorted(r.sample(range(1, n), min(k + 1, n - 1)))
    code = ["t%d = a + %d" % (i, i) for i in range(n)]
    jumps = {}
    for p in pts[:k]:
        tgt = r.randint(0, n - 1)
        if tgt == p: tgt = (p + 2) % n
        jumps[p] = (r.choice(["if t%d < 10 goto" % p, "goto"]), tgt)
    return code, jumps


@gen(S, IC, "Basic blocks", n=70, diff="medium")
def ic_bb(r):
    code, jumps = rand_tac(r)
    n = len(code)
    text = []
    targets = {t for _, t in jumps.values()}
    for i in range(n):
        line = ("L%d: " % i if i in targets else "") + code[i]
        text.append("%2d  %s" % (i + 1, line))
        if i in jumps:
            op, t = jumps[i]
            text.append("    %s L%d" % (op, t))
    leaders = {0}
    for p, (op, t) in jumps.items():
        leaders.add(t)
        if p + 1 < n: leaders.add(p + 1)
    return nat(r, "How many basic blocks does the following three-address code contain?\n```\n%s\n```" % "\n".join(text), len(leaders), "Leaders: first instruction, jump targets, instruction after a jump ⇒ %d blocks." % len(leaders))


def value_numbering(block):
    """block: list of (dest, op, a, b). Return number of DAG nodes."""
    node, var, ctr = {}, {}, [0]

    def leaf(v):
        if v not in var:
            var[v] = ("leaf", v)
            node.setdefault(("leaf", v), 1)
        return var[v]
    for d, op, a, b in block:
        na, nb = leaf(a), leaf(b)
        key = (op,) + tuple(sorted([na, nb], key=str)) if op in "+*" else (op, na, nb)
        node.setdefault(key, 1)
        var[d] = key
    return len(node)


@gen(S, OP, "Common subexpressions (DAG)", n=70, diff="hard", marks=2)
def op_dag(r):
    vs = ["a", "b", "c", "d"]
    n = r.randint(4, 6)
    block, lines = [], []
    for i in range(n):
        op = r.choice("+-*")
        a, b = r.choice(vs), r.choice(vs)
        if a == b: b = [x for x in vs if x != a][0]
        d = "t%d" % i
        if r.random() < 0.35 and block:
            _, op0, a0, b0 = r.choice(block); op, a, b = op0, a0, b0
        block.append((d, op, a, b))
        lines.append("%s = %s %s %s" % (d, a, op, b))
    cnt = value_numbering(block)
    return nat(r, "The following basic block is converted to a DAG (common sub-expressions share nodes; + and * are commutative; the variables a, b, c, d are not modified). "
                  "How many nodes does the DAG have (leaves + operator nodes)?\n```\n%s\n```" % "\n".join(lines), cnt, "Leaves + distinct operator nodes = %d." % cnt)


def live_in(block, live_out):
    live = set(live_out)
    for d, uses in reversed(block):
        live.discard(d)
        live |= set(uses)
    return live


@gen(S, OP, "Liveness", n=80, diff="medium")
def op_live(r):
    vs = list("abcdefg")
    n = r.randint(4, 6)
    block, lines = [], []
    for _ in range(n):
        d = r.choice(vs)
        u = r.sample(vs, 2)
        block.append((d, u)); lines.append("%s = %s + %s" % (d, u[0], u[1]))
    out = set(r.sample(vs, r.randint(1, 3)))
    li = live_in(block, out)
    if r.random() < 0.5:
        return nat(r, "A basic block is followed by code that uses exactly the variables {%s} before redefining them. Number of variables live at the START of the block?\n```\n%s\n```" % (", ".join(sorted(out)), "\n".join(lines)), len(li), "Backward pass: live-in = {%s}." % ", ".join(sorted(li)))
    live = set(out)
    after = []
    for d, uses in reversed(block):
        after.append(set(live))
        live.discard(d); live |= set(uses)
    after = after[::-1]
    return nat(r, "Variables {%s} are live after the block. How many variables are live immediately AFTER the first instruction?\n```\n%s\n```" % (", ".join(sorted(out)), "\n".join(lines)), len(after[0]),
               "Live set after instruction 1 = {%s}." % ", ".join(sorted(after[0])))


def rand_tree(r, k):
    if k == 1: return "leaf"
    l = r.randint(1, k - 1)
    return (rand_tree(r, l), rand_tree(r, k - l))


def su_label(t, left=True):
    if t == "leaf": return 1 if left else 0
    a, b = su_label(t[0], True), su_label(t[1], False)
    return a + 1 if a == b else max(a, b)


def tstr(t, it):
    if t == "leaf": return next(it)
    return "(%s %s %s)" % (tstr(t[0], it), "+-*/"[len(str(t)) % 4], tstr(t[1], it))


@gen(S, IC, "Register need (Sethi–Ullman)", n=60, diff="hard", marks=2)
def ic_su(r):
    k = r.randint(4, 8)
    t = rand_tree(r, k)
    e = tstr(t, iter("abcdefghijk"))
    return nat(r, "A machine has instructions OP R_i, R_j (register-register) and OP R_i, M (register-memory); all variables initially reside in memory. Using the Sethi–Ullman/Ershov numbering (a left leaf needs one register, a right leaf operand can be read from memory), the minimum number of registers needed to evaluate %s without spilling is" % e, su_label(t), "Label nodes bottom-up: equal children ⇒ +1, otherwise max.")


@gen(S, IC, "Runtime environments", n=60, diff="easy")
def ic_rt(r):
    kind = r.choice(["depth", "frames", "static_link", "tac", "temps"])
    n = r.randint(3, 12)
    if kind == "depth": return nat(r, "A recursive function f(n) calls f(n−1) when n > 0 and returns otherwise. Maximum number of activation records on the stack when main calls f(%d) (including main's and counting f(0))?" % n, n + 2, "main + f(%d) … f(0) = 1 + %d + 1." % (n, n))
    if kind == "frames":
        loc, par, ra = r.randint(1, 8), r.randint(1, 5), 1
        return nat(r, "Each activation record holds %d local words, %d parameter words, 1 return-address word and 1 saved frame-pointer word. Words in one frame?" % (loc, par), loc + par + 2, "Sum of components.")
    if kind == "static_link":
        d = r.randint(2, 5)
        return nat(r, "In a language with nested procedures (static scoping), a procedure at nesting depth %d accesses a variable declared at nesting depth %d. How many static-link hops are needed?" % (d + 2, d), 2, "Hops = difference in nesting depths.")
    if kind == "tac":
        k = r.randint(3, 7)
        return nat(r, "Minimum number of three-address instructions to compute  x = a1 + a2 + … + a%d  (the final addition may write directly into x)?" % k, k - 1, "k operands need k−1 additions.")
    return nat(r, "Number of temporaries needed in the three-address code for the expression  a*b + c*d − e/f  with a new temporary for every operator?", 5, "Five operators ⇒ five temporaries.")
