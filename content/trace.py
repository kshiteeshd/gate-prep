"""Worked, step-by-step traces added to PDS/ALGO question explanations by re-deriving the answer from the question text."""
import re


def _ints(s):
    return [int(x) for x in re.findall(r"-?\d+", s)]


def postfix(q):
    m = re.match(r"Evaluate the postfix expression:\s+(.*)$", q["text"].strip())
    if not m:
        return None
    st, lines = [], []
    for tok in m.group(1).split():
        if re.fullmatch(r"-?\d+", tok):
            st.append(int(tok))
            lines.append("read %s: push, stack %s" % (tok, st))
        else:
            b, a = st.pop(), st.pop()
            r = {"+": a + b, "-": a - b, "*": a * b, "/": a // b if b else 0}[tok]
            st.append(r)
            lines.append("read %s: pop %d (right) and %d (left), compute %d %s %d = %d, stack %s" % (tok, b, a, a, tok, b, r, st))
    return "Step by step:\n" + "\n".join(lines) + "\nThe single value left on the stack is the answer, %d." % st[-1]


class _N:
    def __init__(s, k):
        s.k, s.l, s.r = k, None, None


def bst(q):
    m = re.match(r"Keys ([\d ]+) are inserted in this order into an initially empty BST", q["text"])
    if not m:
        return None
    keys = _ints(m.group(1))
    root, lines = None, []
    for k in keys:
        if root is None:
            root = _N(k)
            lines.append("insert %d: the tree is empty, so it becomes the root" % k)
            continue
        cur, path = root, [root.k]
        while True:
            side = "l" if k < cur.k else "r"
            nxt = getattr(cur, side)
            if nxt is None:
                setattr(cur, side, _N(k))
                break
            cur = nxt
            path.append(cur.k)
        lines.append("insert %d: compare along %s, then place it as the %s child of %d" % (k, " → ".join(map(str, path)), "left" if side == "l" else "right", cur.k))

    def h(n):
        return -1 if n is None else 1 + max(h(n.l), h(n.r))

    def pre(n):
        return [] if n is None else [n.k] + pre(n.l) + pre(n.r)
    return "Build the tree one key at a time (smaller goes left, larger goes right):\n" + "\n".join(lines) + "\nPreorder of the final tree: %s; height = %d edges." % (pre(root), h(root))


def minheap(q):
    m = re.match(r"Keys ([\d ]+) are inserted into an empty (min|max)-heap using sift-up", q["text"])
    if not m:
        return None
    mn = m.group(2) == "min"
    a, lines = [], []
    for k in _ints(m.group(1)):
        a.append(k)
        i, sw = len(a) - 1, []
        while i > 0:
            p = (i - 1) // 2
            if (a[i] < a[p]) if mn else (a[i] > a[p]):
                sw.append("%d↔%d" % (a[p], a[i]))
                a[i], a[p] = a[p], a[i]
                i = p
            else:
                break
        lines.append("insert %d at the end%s -> %s" % (k, (", sift up (" + ", ".join(sw) + ")") if sw else ", no swap needed", a))
    return "Heap array after each insertion (parent of index i is (i-1)//2, 0-based):\n" + "\n".join(lines)


def hashing(q):
    m = re.match(r"Keys ([\d ]+) are inserted into a hash table with chaining, h\(k\) = k mod (\d+)", q["text"])
    if not m:
        return None
    keys, mod = _ints(m.group(1)), int(m.group(2))
    b = {i: [] for i in range(mod)}
    for k in keys:
        b[k % mod].append(k)
    rows = ["%d mod %d = %d" % (k, mod, k % mod) for k in keys]
    tab = ["bucket %d: %s" % (i, b[i] if b[i] else "empty") for i in range(mod)]
    return "Compute each hash value:\n" + ", ".join(rows) + "\nBuckets:\n" + "\n".join(tab) + "\nRead the quantity asked for off this table (%d bucket(s) empty, longest chain %d)." % (sum(1 for v in b.values() if not v), max(len(v) for v in b.values()))


def collatz(q):
    m = re.search(r"What does f\((\d+)\) return\?\s*```c\s*int f\(int n\) \{ if \(n == 1\) return 0; return 1 \+ f\(n % 2 \? 3 \* n \+ 1 : n / 2\); \}", q["text"])
    if not m:
        return None
    n, chain, steps = int(m.group(1)), [], 0
    chain.append(n)
    while n != 1:
        n = 3 * n + 1 if n % 2 else n // 2
        chain.append(n)
        steps += 1
    return "Each call adds 1 and moves to 3n+1 (odd n) or n/2 (even n) until n = 1 returns 0.\nChain: " + " → ".join(map(str, chain)) + "\nThere are %d moves before the base case, so f returns %d." % (steps, steps)


def llist(q):
    m = re.match(r"A singly linked list initially holds \[([\d, ]+)\] \(head first\)\. Operations applied in order: (.*?)\. What is", q["text"])
    if not m:
        return None
    lst, lines = _ints(m.group(1)), []
    for op in m.group(2).split("; "):
        mi = re.match(r"insert (\d+) at the head", op)
        mt = re.match(r"insert (\d+) at the tail", op)
        if mi:
            lst = [int(mi.group(1))] + lst
        elif mt:
            lst = lst + [int(mt.group(1))]
        elif op.startswith("delete the head"):
            lst = lst[1:]
        elif op.startswith("delete the tail"):
            lst = lst[:-1]
        else:
            return None
        lines.append("%s -> %s" % (op, lst))
    return "List after each operation (head first):\n" + "\n".join(lines)


def loop_xor(q):
    m = re.search(r"int x = 0;\s*for \(int i = 1; i <= (\d+); i\+\+\) x \^= i;", q["text"])
    if not m:
        return None
    n, x = int(m.group(1)), 0
    for i in range(1, n + 1):
        x ^= i
    return "XOR of 1..n repeats with period 4: n%%4==0 gives n, 1 gives 1, 2 gives n+1, 3 gives 0. Here n = %d, n mod 4 = %d, so x = %d." % (n, n % 4, x)


ALL = (postfix, bst, minheap, hashing, collatz, llist, loop_xor)


def add(q):
    if q["subject"] not in ("PDS", "ALGO"):
        return False
    for f in ALL:
        try:
            t = f(q)
        except Exception:
            t = None
        if t:
            head = (q.get("expl") or "").strip()
            q["expl"] = (head + "\n\n" if head else "") + t
            return True
    return False
