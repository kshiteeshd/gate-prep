"""Independent Python reference implementations of automata and grammar algorithms (used by lessons to verify worked examples
and by tools/make_toc_tests.py to test the JavaScript tools)."""
import itertools


class NFA:
    def __init__(self, start, acc, edges):
        self.start, self.acc = start, set(acc)
        self.edges = edges          # list of (u, a, v), a == 'e' for epsilon
        self.alpha = sorted({a for _, a, _ in edges if a != 'e'})

    def eps(self, S):
        S = set(S)
        while True:
            n = {v for u, a, v in self.edges if a == 'e' and u in S} - S
            if not n:
                return S
            S |= n

    def accepts(self, w):
        S = self.eps({self.start})
        for c in w:
            S = self.eps({v for u, a, v in self.edges if a == c and u in S})
        return bool(S & self.acc)

    def dfa(self):
        start = frozenset(self.eps({self.start}))
        seen, todo, tr = {start}, [start], {}
        while todo:
            S = todo.pop()
            for a in self.alpha:
                N = frozenset(self.eps({v for u, b, v in self.edges if b == a and u in S}))
                tr[(S, a)] = N
                if N not in seen:
                    seen.add(N)
                    todo.append(N)
        return start, seen, tr

    def min_states(self):
        start, states, tr = self.dfa()
        states = list(states)
        # Myhill-Nerode style table of distinguishable pairs
        dist = set()
        for p, q in itertools.combinations(states, 2):
            if bool(p & self.acc) != bool(q & self.acc):
                dist.add(frozenset([p, q]))
        ch = True
        while ch:
            ch = False
            for p, q in itertools.combinations(states, 2):
                if frozenset([p, q]) in dist:
                    continue
                if any(frozenset([tr[(p, a)], tr[(q, a)]]) in dist for a in self.alpha):
                    dist.add(frozenset([p, q]))
                    ch = True
        classes = []
        for s in states:
            for c in classes:
                if frozenset([s, c[0]]) not in dist:
                    c.append(s)
                    break
            else:
                classes.append([s])
        return len(classes)

    def count(self, L):
        return sum(1 for w in itertools.product(self.alpha, repeat=L) if self.accepts(w))

    def kind(self):
        # brute force: strings up to length 2*|DFA|+2 decide empty / finite / infinite
        start, states, tr = self.dfa()
        N = len(states)
        longest = 2 * N + 1
        if any(self.accepts(w) for L in range(0, N + 1) for w in itertools.product(self.alpha, repeat=L)) is False:
            return "empty"
        # infinite iff some accepted string has length in [N, 2N)
        for L in range(N, 2 * N):
            if any(self.accepts(w) for w in itertools.product(self.alpha, repeat=L)):
                return "infinite"
        return "finite"


def ref_sets(nts, rules):
    isnt = lambda t: t in nts
    nullable = set()
    while True:
        new = {l for l, r in rules if all(isnt(t) and t in nullable for t in r)} - nullable
        if not new:
            break
        nullable |= new
    first = {n: set() for n in nts}
    while True:
        before = sum(len(v) for v in first.values())
        for l, r in rules:
            for t in r:
                if isnt(t):
                    first[l] |= first[t]
                    if t not in nullable:
                        break
                else:
                    first[l].add(t)
                    break
        if sum(len(v) for v in first.values()) == before:
            break

    def fseq(seq):
        out, nul = set(), True
        for t in seq:
            if isnt(t):
                out |= first[t]
                if t not in nullable:
                    nul = False
                    break
            else:
                out.add(t)
                nul = False
                break
        return out, nul
    follow = {n: set() for n in nts}
    follow[nts[0]].add("$")
    while True:
        before = sum(len(v) for v in follow.values())
        for l, r in rules:
            for i, t in enumerate(r):
                if isnt(t):
                    f, nul = fseq(r[i + 1:])
                    follow[t] |= f
                    if nul:
                        follow[t] |= follow[l]
        if sum(len(v) for v in follow.values()) == before:
            break
    return nullable, first, follow, fseq


def ref_ll1(nts, rules):
    nullable, first, follow, fseq = ref_sets(nts, rules)
    cells = {}
    for i, (l, r) in enumerate(rules):
        f, nul = fseq(r)
        for t in (f | (follow[l] if nul else set())):
            cells.setdefault((l, t), []).append(i)
    return all(len(v) == 1 for v in cells.values())


def ref_lr0(nts, rules):
    R = [("S'", [nts[0]])] + rules
    isnt = lambda t: t in nts

    def clo(items):
        items = set(items)
        while True:
            new = set()
            for ri, d in items:
                r = R[ri][1]
                if d < len(r) and isnt(r[d]):
                    for j, (l, _) in enumerate(R):
                        if l == r[d] and (j, 0) not in items:
                            new.add((j, 0))
            if not new:
                return frozenset(items)
            items |= new

    def goto(S, X):
        return clo({(ri, d + 1) for ri, d in S if d < len(R[ri][1]) and R[ri][1][d] == X})
    start = clo({(0, 0)})
    states, todo, edges = {start}, [start], {}
    while todo:
        S = todo.pop()
        for X in sorted({R[ri][1][d] for ri, d in S if d < len(R[ri][1])}):
            N = goto(S, X)
            edges[(S, X)] = N
            if N not in states:
                states.add(N)
                todo.append(N)
    return R, states, edges


def ref_slr(nts, rules):
    nullable, first, follow, _ = ref_sets(nts, rules)
    R, states, edges = ref_lr0(nts, rules)
    for S in states:
        seen = {}
        for ri, d in S:
            if ri != 0 and d == len(R[ri][1]):
                for t in follow[R[ri][0]]:
                    if seen.get(t) is not None and seen[t] != ri:
                        return False
                    seen[t] = ri
                    if (S, t) in edges and t not in nts:
                        return False
    return True


