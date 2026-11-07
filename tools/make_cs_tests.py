"""Generate tools/test_widgets_cs.js: JS tool logic vs the independent Python implementations in content/g_algo.py & g_pds.py."""
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from content import g_algo as A, g_pds as P  # noqa: E402

rng = random.Random(7)
T = []


def add(name, js_expr, expected):
    T.append((name, js_expr, expected))


# sorting counters
for a in ([5, 2, 9, 1, 7, 3, 8], [3, 1, 2], [9, 8, 7, 6, 5], [1, 2, 3, 4], [4, 4, 2, 9, 1, 1, 6]):
    js = json.dumps(a)
    # python reference
    def bub(x):
        x = list(x); c = 0; s = 0
        for i in range(len(x) - 1):
            sd = False
            for j in range(len(x) - 1 - i):
                c += 1
                if x[j] > x[j + 1]:
                    x[j], x[j + 1] = x[j + 1], x[j]; s += 1; sd = True
            if not sd: break
        return c, s
    add("bubble cmp/swaps %s" % js, "(r=LW.sortRun('bubble',%s),[r.cmp,r.sw])" % js, list(bub(a)))
    add("insertion cmp %s" % js, "LW.sortRun('insertion',%s).cmp" % js, A.insertion_cmp(a))
    add("insertion shifts = inversions %s" % js, "LW.sortRun('insertion',%s).sw" % js, A.inversions(a))
    add("selection swaps %s" % js, "LW.sortRun('selection',%s).sw" % js, A.selection_swaps(a))
    add("selection cmp n(n-1)/2 %s" % js, "LW.sortRun('selection',%s).cmp" % js, len(a) * (len(a) - 1) // 2)
    add("all algos sort %s" % js, "['bubble','insertion','selection','merge','quick'].every(al=>LW.sortRun(al,%s).sorted.join()==%s.slice().sort((x,y)=>x-y).join())" % (js, js), True)
for a in ([5, 2, 9, 1, 7, 3, 8], [8, 3, 5, 1]):
    # merge comparisons reference
    def mc(x):
        c = [0]
        def ms(v):
            if len(v) <= 1: return v
            m = len(v) // 2; L, R = ms(v[:m]), ms(v[m:]); o = []; i = j = 0
            while i < len(L) and j < len(R):
                c[0] += 1
                if L[i] <= R[j]: o.append(L[i]); i += 1
                else: o.append(R[j]); j += 1
            return o + L[i:] + R[j:]
        ms(x); return c[0]
    add("merge cmp %s" % json.dumps(a), "LW.sortRun('merge',%s).cmp" % json.dumps(a), mc(a))
    _, pos, sw = A.lomuto(a)
    add("quick first partition swaps agree (frames exist)", "LW.sortRun('quick',%s).frames.length>1" % json.dumps(a), True)

# master theorem
for a, b, k, exp in ((2, 2, 1, "Θ(n^1 log^1 n)"), (1, 2, 0, "Θ(log^1 n)"), (4, 2, 1, "Θ(n^2)"), (1, 2, 1, "Θ(n)"), (8, 2, 2, "Θ(n^3)")):
    add("master a=%d b=%d k=%d" % (a, b, k), "LW.master(%d,%d,%d,0).res" % (a, b, k), {"Θ(n^1 log^1 n)": "Θ(n log^1 n)"}.get(exp, exp).replace("Θ(log^1 n)", "Θ(log^1 n)"))

# DP
for s, t in (("ABCBDAB", "BDCABA"), ("AGGTAB", "GXTXAYB"), ("kitten", "sitting"), ("SUNDAY", "SATURDAY")):
    add("lcs %s/%s" % (s, t), "LW.lcs(%s,%s).at(-1).at(-1)" % (json.dumps(s), json.dumps(t)), A.lcs(s, t))
    add("edit %s/%s" % (s, t), "LW.edit(%s,%s).at(-1).at(-1)" % (json.dumps(s), json.dumps(t)), A.edit(s, t))
add("knapsack classic", "LW.knap([[60,10],[100,20],[120,30]],50).at(-1).at(-1)", 220)
add("knapsack small", "LW.knap([[10,5],[40,4],[30,6],[50,3]],10).at(-1).at(-1)", 90)

# graphs
for _ in range(4):
    n = rng.randint(5, 7)
    e = A.rand_wgraph(rng, n, rng.randint(2, 4))
    txt = ", ".join("%s-%s:%d" % (chr(65 + a), chr(65 + b), w) for a, b, w in e)
    d = A.dijkstra(n, e, 0)
    js = "LW.parseG(%s,false)" % json.dumps(txt)
    add("dijkstra %s" % txt, "(g=%s, r=LW.dijkstra(g,'A'), g.vs.map(v=>r.d[v]))" % js, [d.get(i, None) for i in range(n)] if len(d) == n else [d.get(i) for i in range(n)])
    add("kruskal = prim = reference %s" % txt, "[LW.kruskal(%s).w, LW.prim(%s,'A').w]" % (js, js), [A.mst_weight(n, e)] * 2)
    add("bfs visits all connected", "LW.bfs(%s,'A').length" % js, n)
# traversal order vs PDS reference
for seed in range(3):
    r2 = random.Random(seed + 11)
    n = 6
    e = P.rand_dgraph(r2, n, 0.4)
    if len(e) < n - 1: continue
    a = P.adj(n, e, False)
    nm = lambda i: chr(65 + i)
    txt = ", ".join("%s-%s" % (nm(x), nm(y)) for x, y in e)
    js = "LW.parseG(%s,false)" % json.dumps(txt)
    add("bfs order %s" % txt, "(g=%s, g.vs.includes('A')?LW.bfs(g,'A').join(''):'')" % js, "".join(map(nm, P.bfs(a, 0))) if any(0 in x for x in e) else "")
    add("dfs order %s" % txt, "(g=%s, g.vs.includes('A')?LW.dfs(g,'A').join(''):'')" % js, "".join(map(nm, P.dfs(a, 0))) if any(0 in x for x in e) else "")
add("topological order", "LW.topo(LW.parseG('A->B, A->C, B->D, C->D, D->E', true)).join('')", "ABCDE")
add("topological cycle -> null", "LW.topo(LW.parseG('A->B, B->C, C->A', true))", None)
add("scc count", "LW.scc(LW.parseG('A->B, B->C, C->A, C->D, D->E, E->D', true)).length", 2)
add("bellman negative cycle", "LW.bellman(LW.parseG('A->B:1, B->C:-3, C->A:1', true),'A').neg", True)
add("bellman distances", "(r=LW.bellman(LW.parseG('A->B:4, A->C:5, B->C:-2', true),'A'), [r.d.B,r.d.C])", [4, 2])

# trees
for keys in ([50, 30, 70, 20, 40, 60, 80, 10], [10, 20, 30, 40, 50], [8, 3, 10, 1, 6, 14, 4, 7, 13], [31, 5, 40, 12, 3, 44, 9]):
    t = P.BST()
    for k in keys: t.insert(k)
    js = json.dumps(keys)
    add("bst height %s" % js, "(r=null,%s.forEach(k=>r=LW.bstInsert(r,k)),LW.height(r))" % js, P.height(t.root))
    add("bst preorder %s" % js, "(r=null,%s.forEach(k=>r=LW.bstInsert(r,k)),LW.preorder(r))" % js, P.preorder(t.root))
    add("bst postorder %s" % js, "(r=null,%s.forEach(k=>r=LW.bstInsert(r,k)),LW.postorder(r))" % js, P.postorder(t.root))
    rot, ht = P.avl_insert_rotations(keys)
    add("avl rotations/height %s" % js, "(r=LW.avlBuild(%s),[r.rot,LW.height(r.root)])" % js, [rot, ht])

# heaps
for arr in ([9, 4, 7, 1, 8, 2, 6], [5, 3, 8, 1, 9, 2], [20, 15, 30, 10, 5, 25]):
    h, sw = A.build_heap(arr)
    add("buildHeap(max) %s" % json.dumps(arr), "(r=LW.buildHeap(%s,false),[r.a,r.sw])" % json.dumps(arr), [h, sw])
    import heapq
    arr2 = []
    for k in arr:
        arr2.append(k); i = len(arr2) - 1
        while i > 0 and arr2[(i - 1) // 2] > arr2[i]:
            arr2[(i - 1) // 2], arr2[i] = arr2[i], arr2[(i - 1) // 2]; i = (i - 1) // 2
    add("min-heap insert sequence %s" % json.dumps(arr), "%s.reduce((a,k)=>LW.heapInsert(a,k,true),[])" % json.dumps(arr), arr2)
add("heap pop min order", "(a=[5,3,8,1,9,2].reduce((a,k)=>LW.heapInsert(a,k,true),[]),o=[],[1,2,3,4,5,6].forEach(()=>{const r=LW.heapPop(a,true);o.push(r.top);a=r.a}),o)", [1, 2, 3, 5, 8, 9])

# hashing
for keys, m in (([12, 25, 38, 51, 64, 9, 22], 11), ([10, 22, 31, 4, 15, 28, 17, 88, 59], 11), ([5, 28, 19, 15, 20, 33, 12, 17, 10], 9)):
    t, c = A.hash_insert(keys, m, lambda k, i, mm: (k + i) % mm)
    add("linear probing %s m=%d" % (keys, m), "(r=LW.hashRun(%s,%d,'linear'),[r.t,r.coll])" % (json.dumps(keys), m), [t, c])
    chains = [[] for _ in range(m)]
    for k in keys: chains[k % m].append(k)
    add("chaining longest %s" % keys, "Math.max(...LW.hashRun(%s,%d,'chain').chains.map(c=>c.length))" % (json.dumps(keys), m), max(map(len, chains)))

# recursion / stacks
for n in (5, 10, 15, 20):
    add("fib naive calls n=%d" % n, "LW.fibCalls(%d,false).calls" % n, P.calls(n))
    add("fib memo calls n=%d" % n, "LW.fibCalls(%d,true).calls" % n, 2 * n - 1)
for ex in ("a+b*c", "(a+b)*c", "a+b*c-d/e", "a^b^c", "(a+b)*(c-d)", "a-b-c"):
    toks = P.to_postfix(list(ex.replace(" ", "")))
    add("postfix %s" % ex, "LW.toPostfix(%s).join(' ')" % json.dumps(ex), " ".join(toks))
add("postfix eval", "LW.evalPostfix(LW.toPostfix('(2+3)*4-6/2'))", 17)
add("postfix eval 2", "LW.evalPostfix(LW.toPostfix('2+3*4-5'))", 9)

out = ["// AUTO-GENERATED by tools/make_cs_tests.py — JS tool logic vs the independent Python reference.   node tools/test_widgets_cs.js",
       "require('../static/js/learn.js'); require('../static/js/learn_cs.js'); const L = globalThis.LW; let r, g, a, o;",
       "const eq = (x, y) => JSON.stringify(x) === JSON.stringify(y);", "const T = (n, c, got, exp) => console.log((c ? 'PASS ' : 'FAIL ') + n + (c ? '' : '  got=' + JSON.stringify(got) + ' expected=' + JSON.stringify(exp)));",
       "const LW = L;"]
for name, expr, exp in T:
    out.append("try { const got = %s; T(%s, eq(got, %s), got, %s); } catch (e) { T(%s, false, String(e), %s); }" % (expr, json.dumps(name), json.dumps(exp), json.dumps(exp), json.dumps(name), json.dumps(exp)))
open(os.path.join(ROOT, "tools", "test_widgets_cs.js"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("generated %d tests" % len(T))
