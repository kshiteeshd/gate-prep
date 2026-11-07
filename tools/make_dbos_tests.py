"""Generate tools/test_widgets_dbos.js: JS DBMS/OS tool logic vs independent Python reference implementations."""
import itertools
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from content import g_dbms as D, g_os as O  # noqa: E402

rng = random.Random(21)
T = []


def add(name, expr, exp):
    T.append((name, expr, exp))


# ---------- FDs ----------
for _ in range(25):
    U = list("ABCDE"[:rng.choice([4, 5])])
    fds = D.rand_fds(rng, U, rng.randint(2, 5))
    text = ", ".join("%s->%s" % ("".join(l), "".join(r)) for l, r in fds)
    ju = json.dumps(U)
    keys = [list(k) for k in D.candidate_keys(U, fds)]
    add("candidate keys %s" % text, "LW.candidateKeys(%s, LW.fdParse(%s))" % (ju, json.dumps(text)), keys)
    add("highest NF %s" % text, "LW.highestNF(%s, LW.fdParse(%s))" % (ju, json.dumps(text)), D.highest_nf(U, fds))
    X = sorted(rng.sample(U, rng.choice([1, 2])))
    add("closure %s of %s" % ("".join(X), text), "LW.fdClosure(%s, LW.fdParse(%s))" % (json.dumps(X), json.dumps(text)), sorted(D.closure(X, fds)))


def ref_preserved(parts, fds):
    ok = True
    for l, r in fds:
        res = set(l)
        ch = True
        while ch:
            ch = False
            for R in parts:
                t = D.closure(res & set(R), fds) & set(R)
                if not t <= res:
                    res |= t; ch = True
        if not set(r) <= res:
            ok = False
    return ok


for _ in range(20):
    U = list("ABCDE"[:rng.choice([4, 5])])
    fds = D.rand_fds(rng, U, rng.randint(2, 4))
    R1 = sorted(rng.sample(U, rng.randint(2, len(U) - 1)))
    R2 = sorted((set(U) - set(R1)) | set(rng.sample(R1, 1)))
    if set(R1) | set(R2) != set(U):
        continue
    text = ", ".join("%s->%s" % ("".join(l), "".join(r)) for l, r in fds)
    inter = set(R1) & set(R2)
    lossless = D.closure(inter, fds) >= set(R1) or D.closure(inter, fds) >= set(R2)
    add("lossless %s | %s %s" % (R1, R2, text), "LW.lossless2(%s,%s,LW.fdParse(%s))" % (json.dumps(R1), json.dumps(R2), json.dumps(text)), lossless)
    add("preserves %s | %s %s" % (R1, R2, text), "LW.preserves([%s,%s],LW.fdParse(%s))" % (json.dumps(R1), json.dumps(R2), json.dumps(text)), ref_preserved([R1, R2], fds))

# ---------- schedules ----------
for _ in range(40):
    ops, co = D.gen_schedule(rng, rng.choice([2, 3]), rng.randint(5, 8))
    if len({t for t, _, _ in ops}) < 2:
        continue
    full = D.with_commits(rng, ops)
    s = D.sched_str(full)
    nodes = sorted({t for t, _, _ in ops})
    g = D.conflict_graph(ops, 3)
    cyc = D.has_cycle(g, nodes)
    add("serializable? %s" % s, "LW.schedInfo(LW.parseSched(%s)).cyc" % json.dumps(s), cyc)
    add("class %s" % s, "LW.schedInfo(LW.parseSched(%s)).cls" % json.dumps(s), D.classify_full(full))
    if not cyc and len(nodes) <= 4:
        add("serial orders %s" % s, "LW.schedInfo(LW.parseSched(%s)).orders" % json.dumps(s), D.topo_count(g, nodes))

# ---------- CPU scheduling ----------
def fcfs_ct(ps):
    t, ct = 0, {}
    for p in sorted(ps, key=lambda p: (p[1], p[0])):
        t = max(t, p[1]) + p[2]; ct[p[0]] = t
    return ct


for _ in range(18):
    n = rng.randint(3, 5)
    ps = O.mkprocs(rng, n, 6, 9)
    js = json.dumps([{"at": a, "bt": b, "pr": 0} for _, a, b in ps])
    for algo, fn in (("fcfs", fcfs_ct), ("sjf", O.sjf_np), ("srtf", O.srtf)):
        ct = fn(ps)
        add("%s CT %s" % (algo, ps), "LW.cpuSched('%s',%s,3).ct" % (algo, js), [ct[i + 1] for i in range(n)])
    q = rng.choice([2, 3, 4])
    ct = O.rr(ps, q)
    add("rr q=%d CT %s" % (q, ps), "LW.cpuSched('rr',%s,%d).ct" % (js, q), [ct[i + 1] for i in range(n)])

# ---------- page replacement ----------
for _ in range(25):
    ref = O.refstring(rng, rng.randint(10, 18), rng.randint(4, 7))
    k = rng.choice([2, 3, 4])
    for algo, fn in (("fifo", O.fifo), ("lru", O.lru), ("opt", O.opt)):
        add("%s faults %s k=%d" % (algo, ref, k), "LW.pageRep('%s',%s,%d).faults" % (algo, json.dumps(ref), k), fn(ref, k))
add("Belady anomaly", "[LW.pageRep('fifo',[1,2,3,4,1,2,5,1,2,3,4,5],3).faults, LW.pageRep('fifo',[1,2,3,4,1,2,5,1,2,3,4,5],4).faults]", [9, 10])

# ---------- disk ----------
for _ in range(20):
    reqs = rng.sample(range(5, 195), rng.randint(5, 8))
    h = rng.randint(30, 120)
    js = json.dumps(reqs)
    add("fcfs %s h=%d" % (reqs, h), "LW.diskSched('fcfs',%d,%s,199).total" % (h, js), O.disk_fcfs(h, reqs))
    add("sstf %s h=%d" % (reqs, h), "LW.diskSched('sstf',%d,%s,199).total" % (h, js), O.disk_sstf(h, reqs))
    add("scan %s h=%d" % (reqs, h), "LW.diskSched('scan',%d,%s,199).total" % (h, js), O.disk_scan(h, reqs, 199))
    add("look %s h=%d" % (reqs, h), "LW.diskSched('look',%d,%s,199).total" % (h, js), O.disk_look(h, reqs))
add("textbook FCFS 640", "LW.diskSched('fcfs',53,[98,183,37,122,14,124,65,67],199).total", 640)
add("textbook SSTF 236", "LW.diskSched('sstf',53,[98,183,37,122,14,124,65,67],199).total", 236)

# ---------- banker ----------
def ref_banker(alloc, mx, av):
    n, m = len(alloc), len(av)
    need = [[mx[i][j] - alloc[i][j] for j in range(m)] for i in range(n)]
    work, fin, seq = list(av), [False] * n, []
    while True:
        for i in range(n):
            if not fin[i] and all(need[i][j] <= work[j] for j in range(m)):
                fin[i] = True; seq.append(i)
                work = [work[j] + alloc[i][j] for j in range(m)]
                break
        else:
            break
    return {"need": need, "safe": all(fin), "seq": seq}


A0 = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
M0 = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
add("banker textbook state: lowest-index safe sequence (another valid one is 1,3,4,0,2)", "LW.banker(%s,%s,[3,3,2]).seq" % (json.dumps(A0), json.dumps(M0)), [1, 3, 0, 2, 4])
for _ in range(15):
    n, m = rng.randint(3, 5), 3
    al = [[rng.randint(0, 3) for _ in range(m)] for _ in range(n)]
    mx = [[al[i][j] + rng.randint(0, 4) for j in range(m)] for i in range(n)]
    av = [rng.randint(0, 4) for _ in range(m)]
    r = ref_banker(al, mx, av)
    add("banker random", "LW.banker(%s,%s,%s)" % (json.dumps(al), json.dumps(mx), json.dumps(av)), r)

out = ["// AUTO-GENERATED by tools/make_dbos_tests.py — JS DBMS/OS tool logic vs independent Python references.   node tools/test_widgets_dbos.js",
       "require('../static/js/learn.js'); require('../static/js/learn_dbos.js'); const LW = globalThis.LW;",
       "const eq = (x, y) => JSON.stringify(x) === JSON.stringify(y);", "const T = (n, c, got, exp) => console.log((c ? 'PASS ' : 'FAIL ') + n + (c ? '' : '  got=' + JSON.stringify(got) + ' expected=' + JSON.stringify(exp)));"]
for name, expr, exp in T:
    out.append("try { const got = %s; T(%s, eq(got, %s), got, %s); } catch (e) { T(%s, false, String(e), %s); }" % (expr, json.dumps(name), json.dumps(exp), json.dumps(exp), json.dumps(name), json.dumps(exp)))
open(os.path.join(ROOT, "tools", "test_widgets_dbos.js"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("generated %d tests" % len(T))
