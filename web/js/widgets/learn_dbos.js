/* GATE Prep — learning modules: DBMS and OS tools (loaded after learn.js and learn_cs.js) */
(function () {
const G = typeof window !== 'undefined' ? window : globalThis;
const LW = G.LW = G.LW || {};

/* ======================= pure logic (unit-tested with node) ======================= */
// ---- functional dependencies ----
LW.fdParse = text => text.split(/[,;\n]+/).map(s => s.trim()).filter(Boolean).map(s => { const m = s.split(/->|→/); if (m.length !== 2) return null; const f = x => [...new Set(x.toUpperCase().replace(/[^A-Z]/g, '').split(''))].sort(); return [f(m[0]), f(m[1])]; }).filter(x => x && x[0].length && x[1].length);
LW.fdClosure = (attrs, fds) => { const c = new Set(attrs); let ch = true; while (ch) { ch = false; fds.forEach(([l, r]) => { if (l.every(a => c.has(a)) && !r.every(a => c.has(a))) { r.forEach(a => c.add(a)); ch = true; } }); } return [...c].sort(); };
LW.subsets = (U, k) => { const out = []; const go = (i, cur) => { if (cur.length === k) { out.push(cur.slice()); return; } for (let j = i; j < U.length; j++) { cur.push(U[j]); go(j + 1, cur); cur.pop(); } }; go(0, []); return out; };
LW.candidateKeys = (U, fds) => { const keys = []; for (let k = 1; k <= U.length; k++) LW.subsets(U, k).forEach(s => { if (LW.fdClosure(s, fds).length === U.length && !keys.some(x => x.every(a => s.includes(a)))) keys.push(s); }); return keys; };
LW.highestNF = (U, fds) => { const keys = LW.candidateKeys(U, fds), prime = new Set(keys.flat()), nonprime = U.filter(a => !prime.has(a)); const isSuper = X => LW.fdClosure(X, fds).length === U.length; const nt = fds.filter(([l, r]) => !r.every(a => l.includes(a)));
  if (nt.every(([l]) => isSuper(l))) return 'BCNF'; if (nt.every(([l, r]) => isSuper(l) || r.filter(a => !l.includes(a)).every(a => prime.has(a)))) return '3NF';
  for (const k of keys) for (let n = 1; n < k.length; n++) for (const X of LW.subsets(k, n)) if (LW.fdClosure(X, fds).some(a => !X.includes(a) && nonprime.includes(a))) return '1NF'; return '2NF'; };
LW.lossless2 = (R1, R2, fds) => { const inter = R1.filter(a => R2.includes(a)); const c = LW.fdClosure(inter, fds); return R1.every(a => c.includes(a)) || R2.every(a => c.includes(a)); };
LW.preserves = (parts, fds) => fds.every(([l, r]) => { let res = new Set(l), ch = true; while (ch) { ch = false; parts.forEach(R => { const t = LW.fdClosure(l.length ? [...res].filter(a => R.includes(a)) : [], fds).filter(a => R.includes(a)); t.forEach(a => { if (!res.has(a)) { res.add(a); ch = true; } }); }); } return r.every(a => res.has(a)); });
// ---- schedules ----
LW.parseSched = text => { const out = []; const re = /([rwca])\s*(\d+)\s*(?:\(\s*([A-Za-z]\w*)\s*\))?/gi; let m; while ((m = re.exec(text))) out.push({op: m[1].toLowerCase(), t: +m[2], x: m[3] || null}); return out; };
LW.schedInfo = ops => { const txns = [...new Set(ops.map(o => o.t))].sort((a, b) => a - b); let full = ops.slice(); txns.forEach(t => { if (!full.some(o => o.t === t && (o.op === 'c' || o.op === 'a'))) full.push({op: 'c', t, x: null}); });
  const E = new Set(); const rw = full.filter(o => o.op === 'r' || o.op === 'w'); rw.forEach((a, i) => rw.slice(i + 1).forEach(b => { if (a.t !== b.t && a.x === b.x && (a.op === 'w' || b.op === 'w')) E.add(a.t + '>' + b.t); }));
  const edges = [...E].map(s => s.split('>').map(Number)); const adj = Object.fromEntries(txns.map(t => [t, edges.filter(e => e[0] === t).map(e => e[1])])); const st = {}; const dfs = u => { st[u] = 1; for (const v of adj[u]) { if (st[v] === 1 || (!st[v] && dfs(v))) return true; } st[u] = 2; return false; }; const cyc = txns.some(t => !st[t] && dfs(t));
  let orders = null; if (!cyc && txns.length <= 6) { orders = 0; const perm = (a, cur) => { if (!a.length) { if (edges.every(([u, v]) => cur.indexOf(u) < cur.indexOf(v))) orders++; return; } a.forEach((x, i) => perm(a.filter((_, j) => j !== i), cur.concat(x))); }; perm(txns, []); }
  const cpos = {}; full.forEach((o, i) => { if (o.op === 'c' || o.op === 'a') cpos[o.t] = i; }); let rec = true, aca = true, strict = true; const lw = {};
  full.forEach((o, i) => { if (o.op === 'c' || o.op === 'a') return; const w = lw[o.x]; if (o.op === 'r' && w !== undefined && w !== o.t) { if (cpos[w] > cpos[o.t]) rec = false; if (cpos[w] > i) { aca = false; strict = false; } } if (o.op === 'w') { if (w !== undefined && w !== o.t && cpos[w] > i) strict = false; lw[o.x] = o.t; } });
  return {txns, edges, cyc, orders, cls: !rec ? 'non-recoverable' : !aca ? 'recoverable but not cascadeless (ACA)' : !strict ? 'cascadeless (ACA) but not strict' : 'strict', rec, aca, strict, full}; };
// ---- CPU scheduling ----
LW.cpuSched = function (algo, procs, q) {
  const n = procs.length, rem = procs.map(p => p.bt), first = Array(n).fill(null), ct = Array(n).fill(null), tl = []; let t = 0, done = 0, cur = null, used = 0, queue = [], added = Array(n).fill(false);
  const key = {fcfs: i => [procs[i].at, i], sjf: i => [procs[i].bt, procs[i].at, i], prio: i => [procs[i].pr || 0, procs[i].at, i], srtf: i => [rem[i], procs[i].at, i]};
  const less = (a, b) => { for (let k = 0; k < a.length; k++) if (a[k] !== b[k]) return a[k] < b[k]; return false; };
  while (done < n && t < 400) {
    if (algo === 'rr') { procs.map((p, i) => [p.at, i]).sort((a, b) => a[0] - b[0] || a[1] - b[1]).forEach(([at, i]) => { if (!added[i] && at <= t) { added[i] = true; queue.push(i); } });
      if (cur !== null) { if (rem[cur] === 0) { ct[cur] = t; done++; cur = null; } else if (used === q) { queue.push(cur); cur = null; } }
      if (cur === null && queue.length) { cur = queue.shift(); used = 0; if (first[cur] === null) first[cur] = t; } }
    else if (algo === 'srtf') { if (cur !== null && rem[cur] === 0) { ct[cur] = t; done++; cur = null; } let best = null; for (let i = 0; i < n; i++) if (rem[i] > 0 && procs[i].at <= t && (best === null || less(key.srtf(i), key.srtf(best)))) best = i; cur = best; if (cur !== null && first[cur] === null) first[cur] = t; }
    else { if (cur !== null && rem[cur] === 0) { ct[cur] = t; done++; cur = null; } if (cur === null) { let best = null; for (let i = 0; i < n; i++) if (rem[i] > 0 && procs[i].at <= t && (best === null || less(key[algo](i), key[algo](best)))) best = i; cur = best; if (cur !== null && first[cur] === null) first[cur] = t; } }
    if (done >= n) break; tl.push(cur); if (cur !== null) { rem[cur]--; used++; } t++;
  }
  if (cur !== null && rem[cur] === 0 && ct[cur] === null) { ct[cur] = t; done++; }
  const tat = ct.map((c, i) => c - procs[i].at), wt = tat.map((x, i) => x - procs[i].bt), rt = first.map((f, i) => f - procs[i].at); let sw = 0, last = null; tl.forEach(x => { if (x !== null) { if (last !== null && last !== x) sw++; last = x; } });
  return {tl, ct, tat, wt, rt, sw, avgWT: wt.reduce((a, b) => a + b, 0) / n, avgTAT: tat.reduce((a, b) => a + b, 0) / n};
};
// ---- page replacement ----
LW.pageRep = function (algo, ref, k) { let fr = [], faults = 0; const steps = [];
  ref.forEach((x, i) => { let fault = false, ev = null;
    if (fr.includes(x)) { if (algo === 'lru') { fr = fr.filter(y => y !== x); fr.push(x); } }
    else { fault = true; faults++; if (fr.length === k) { if (algo === 'opt') { const nxt = p => { const j = ref.indexOf(p, i + 1); return j < 0 ? 1e9 : j; }; let v = fr[0]; fr.forEach(p => { if (nxt(p) > nxt(v)) v = p; }); ev = v; fr = fr.filter(y => y !== v); } else { ev = fr.shift(); } } fr.push(x); }
    steps.push({ref: x, frames: fr.slice(), fault, ev}); });
  return {faults, steps}; };
// ---- disk scheduling ----
LW.diskSched = function (algo, head, reqs, top) { let order = [], tot = 0; const R = reqs.slice(), up = R.filter(x => x >= head).sort((a, b) => a - b), low = R.filter(x => x < head).sort((a, b) => b - a);
  if (algo === 'fcfs') order = R; else if (algo === 'sstf') { const left = R.slice(); let h = head; while (left.length) { left.sort((a, b) => Math.abs(a - h) - Math.abs(b - h) || a - b); h = left.shift(); order.push(h); } }
  else if (algo === 'scan') { order = up.concat(low.length ? [top] : [], low); } else if (algo === 'look') order = up.concat(low); else if (algo === 'cscan') { order = up.concat([top, 0], low.slice().reverse()); } else if (algo === 'clook') order = up.concat(low.slice().reverse());
  let h = head; const path = [head]; order.forEach(x => { tot += Math.abs(x - h); h = x; path.push(x); });
  if (algo === 'scan' && !low.length && up.length) { /* no reversal needed beyond last request */ } return {order, total: tot, path}; };
// ---- Banker's algorithm ----
LW.banker = function (alloc, max, avail) { const n = alloc.length, m = avail.length, need = alloc.map((a, i) => a.map((x, j) => max[i][j] - x)); const work = avail.slice(), fin = Array(n).fill(false), seq = []; let prog = true;
  while (prog) { prog = false; for (let i = 0; i < n; i++) if (!fin[i] && need[i].every((x, j) => x <= work[j])) { fin[i] = true; seq.push(i); alloc[i].forEach((x, j) => work[j] += x); prog = true; break; } }
  return {need, safe: fin.every(Boolean), seq}; };

if (typeof document === 'undefined') return;

/* ======================= widgets ======================= */
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const W = G.LW_W = G.LW_W || {};
const COL = ['#22d3ee', '#a78bfa', '#34d399', '#fbbf24', '#fb7185', '#f97316'];
const pill = (t, c) => '<span class="pill ' + (c || '') + '">' + t + '</span>';
const nums = s => s.split(/[\s,;]+/).filter(Boolean).map(Number).filter(x => !isNaN(x));

// ---------- SQL playground ----------
W.sql = el => {
  const EX = [['All CSE students', "SELECT name, cgpa FROM Student WHERE dept = 'CSE' ORDER BY cgpa DESC"], ['Join', "SELECT s.name, c.title, e.grade FROM Student s JOIN Enroll e ON s.sid = e.sid JOIN Course c ON c.cid = e.cid"],
    ['GROUP BY / HAVING', "SELECT dept, COUNT(*) AS n, AVG(cgpa) AS avg_cgpa FROM Student GROUP BY dept HAVING COUNT(*) > 1"], ['NULL trap: COUNT', "SELECT COUNT(*), COUNT(cgpa), COUNT(DISTINCT dept) FROM Student"],
    ['NOT IN with NULL', "SELECT name FROM Student WHERE name NOT IN (SELECT hod FROM Dept)"], ['Left join', "SELECT d.dept, COUNT(s.sid) AS students FROM Dept d LEFT JOIN Student s ON s.dept = d.dept GROUP BY d.dept"],
    ['Correlated subquery', "SELECT name, cgpa FROM Student s WHERE cgpa > (SELECT AVG(cgpa) FROM Student WHERE dept = s.dept)"], ['Division (all courses of CSE)', "SELECT sid FROM Enroll WHERE cid IN (SELECT cid FROM Course WHERE dept='CSE') GROUP BY sid HAVING COUNT(DISTINCT cid) = (SELECT COUNT(*) FROM Course WHERE dept='CSE')"]];
  el.innerHTML = '<div class="small muted" id="schema">Tables: Dept(dept, hod) · Student(sid, name, dept, cgpa, age) · Course(cid, title, credits, dept) · Enroll(sid, cid, grade) — Student has a NULL cgpa (Gita), Enroll has NULL grades, Dept CIVIL has no HOD, Student Jay is in dept EEE which is not in Dept.</div><div class="row" id="ex" style="margin:8px 0"></div><textarea id="q" rows="3"></textarea><div class="row" style="margin-top:8px"><button class="btn pri sm" id="go">▶ Run query</button><span class="muted small">read-only · one SELECT at a time</span></div><div style="overflow-x:auto;margin-top:10px"><table class="tt" id="res"></table></div><div class="out" id="info"></div>';
  $('#ex', el).innerHTML = EX.map(e => '<button class="btn sm">' + e[0] + '</button>').join(''); $$('#ex .btn', el).forEach((b, i) => b.onclick = () => { $('#q', el).value = EX[i][1]; run(); });
  $('#q', el).value = EX[2][1];
  async function run() { const r = await fetch('/api/learn/sql', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({sql: $('#q', el).value})}).then(x => x.json()).catch(() => ({error: 'The SQL playground needs the desktop app (it runs a real SQLite database). Everything else on this page works here.'}));
    if (r.error) { $('#res', el).innerHTML = ''; $('#info', el).innerHTML = pill(esc(r.error), 'n'); return; }
    $('#res', el).innerHTML = '<tr>' + r.cols.map(c => '<th>' + esc(c) + '</th>').join('') + '</tr>' + r.rows.map(row => '<tr>' + row.map(v => '<td' + (v === null ? ' style="color:var(--mut2);font-style:italic"' : '') + '>' + (v === null ? 'NULL' : esc(v)) + '</td>').join('') + '</tr>').join('');
    $('#info', el).innerHTML = pill(r.rows.length + ' row' + (r.rows.length === 1 ? '' : 's') + (r.more ? '+' : ''), 'y'); }
  $('#go', el).onclick = run; $('#q', el).onkeydown = e => { if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) run(); }; run();
};
// ---------- FD / normalisation ----------
W.fd = el => {
  el.innerHTML = '<div class="row"><label>Attributes</label><input type="text" id="u" value="ABCDE" style="width:110px"><label>FDs</label><input type="text" id="f" value="AB->C, C->D, D->E, E->A" style="flex:1;min-width:240px"></div><div class="row" id="pre" style="margin:8px 0"></div>' +
    '<div class="row"><label>Check closure of</label><input type="text" id="x" value="AB" style="width:90px"><label>Decompose into R1</label><input type="text" id="r1" value="ABC" style="width:90px"><label>R2</label><input type="text" id="r2" value="CDE" style="width:90px"></div><div class="out" id="o"></div>';
  const P = [['Chain', 'ABCDE', 'A->B, B->C, C->D, D->E'], ['Cyclic keys', 'ABCDE', 'AB->C, C->D, D->E, E->A'], ['Partial dependency', 'ABCD', 'AB->C, A->D'], ['Transitive', 'ABC', 'A->B, B->C'], ['3NF not BCNF', 'ABC', 'AB->C, C->B']];
  $('#pre', el).innerHTML = P.map(p => '<button class="btn sm">' + p[0] + '</button>').join(''); $$('#pre .btn', el).forEach((b, i) => b.onclick = () => { $('#u', el).value = P[i][1]; $('#f', el).value = P[i][2]; run(); });
  function run() { const U = [...new Set($('#u', el).value.toUpperCase().replace(/[^A-Z]/g, '').split(''))].sort(), fds = LW.fdParse($('#f', el).value); if (U.length < 2 || U.length > 8 || !fds.length) { $('#o', el).innerHTML = pill('Enter 2–8 attributes and FDs like A->B, BC->D', 'n'); return; }
    const keys = LW.candidateKeys(U, fds), prime = [...new Set(keys.flat())].sort(), nf = LW.highestNF(U, fds), X = $('#x', el).value.toUpperCase().replace(/[^A-Z]/g, '').split('').filter(a => U.includes(a)), R1 = $('#r1', el).value.toUpperCase().replace(/[^A-Z]/g, '').split('').filter(a => U.includes(a)), R2 = $('#r2', el).value.toUpperCase().replace(/[^A-Z]/g, '').split('').filter(a => U.includes(a));
    let sup = 0; for (let k = 1; k <= U.length; k++) LW.subsets(U, k).forEach(s => { if (LW.fdClosure(s, fds).length === U.length) sup++; });
    let h = pill('candidate keys: <b>' + keys.map(k => k.join('')).join(', ') + '</b>', 'y') + pill('prime attributes: ' + (prime.join(', ') || '—')) + pill('superkeys: ' + sup) + pill('highest normal form: <b>' + nf + '</b>', nf === 'BCNF' ? 'y' : '') + pill('(' + X.join('') + ')⁺ = <b>' + LW.fdClosure(X, fds).join('') + '</b>');
    if (R1.length && R2.length && new Set(R1.concat(R2)).size === U.length) h += pill(LW.lossless2(R1, R2, fds) ? '✔ lossless-join' : '✘ lossy decomposition', LW.lossless2(R1, R2, fds) ? 'y' : 'n') + pill(LW.preserves([R1, R2], fds) ? '✔ dependency preserving' : '✘ not dependency preserving', LW.preserves([R1, R2], fds) ? 'y' : 'n'); else h += pill('R1 ∪ R2 must equal all attributes for the decomposition test');
    $('#o', el).innerHTML = h; }
  $$('input', el).forEach(i => i.oninput = run); run();
};
// ---------- schedule analyser ----------
W.sched = el => {
  el.innerHTML = '<label>Schedule (r1(X) = T1 reads X, w2(Y) = T2 writes Y, c1 = T1 commits, a1 = abort). If a transaction has no commit, it commits at the end.</label><input type="text" id="s" value="r1(X) r2(X) w1(X) w2(X) c1 c2" style="width:100%"><div class="row" id="pre" style="margin:8px 0"></div><svg class="gsvg" id="sv" viewBox="0 0 560 220" style="height:220px"></svg><div class="out" id="o"></div>';
  const P = [['Lost update', 'r1(X) r2(X) w1(X) w2(X) c1 c2'], ['Serializable', 'r1(X) w1(X) r2(X) w2(X) r1(Y) w1(Y) c1 c2'], ['Dirty read', 'w1(X) r2(X) c2 c1'], ['Cascadeless', 'w1(X) c1 r2(X) w2(X) c2'], ['Strict', 'w1(X) w1(Y) c1 r2(X) w2(Y) c2'], ['Cycle of 3', 'r1(A) w2(A) r2(B) w3(B) r3(C) w1(C) c1 c2 c3']];
  $('#pre', el).innerHTML = P.map(p => '<button class="btn sm">' + p[0] + '</button>').join(''); $$('#pre .btn', el).forEach((b, i) => b.onclick = () => { $('#s', el).value = P[i][1]; run(); });
  function run() { const ops = LW.parseSched($('#s', el).value); if (!ops.length) { $('#o', el).innerHTML = pill('type a schedule like r1(X) w2(X) c1 c2', 'n'); return; } const r = LW.schedInfo(ops), n = r.txns.length, pos = {}; r.txns.forEach((t, i) => pos[t] = [280 + 160 * Math.cos(2 * Math.PI * i / n - Math.PI / 2), 110 + 80 * Math.sin(2 * Math.PI * i / n - Math.PI / 2)]);
    let svg = '<defs><marker id="ar" markerWidth="10" markerHeight="8" refX="26" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8z" fill="var(--mut)"/></marker></defs>'; r.edges.forEach(([u, v]) => { const p = pos[u], q = pos[v]; svg += '<line x1="' + p[0] + '" y1="' + p[1] + '" x2="' + q[0] + '" y2="' + q[1] + '" stroke="' + (r.cyc ? '#fb7185' : '#22d3ee') + '" stroke-width="2.5" marker-end="url(#ar)"/>'; });
    r.txns.forEach(t => svg += '<circle cx="' + pos[t][0] + '" cy="' + pos[t][1] + '" r="20" fill="var(--bg)" stroke="#22d3ee" stroke-width="2"/><text x="' + pos[t][0] + '" y="' + (pos[t][1] + 5) + '" text-anchor="middle" fill="var(--txt)" font-weight="800">T' + t + '</text>'); $('#sv', el).innerHTML = svg;
    $('#o', el).innerHTML = pill('precedence edges: <b>' + (r.edges.map(e => 'T' + e[0] + '→T' + e[1]).join(', ') || 'none') + '</b>') + pill(r.cyc ? '✘ cycle ⇒ NOT conflict serializable' : '✔ acyclic ⇒ conflict serializable', r.cyc ? 'n' : 'y') + (r.orders !== null ? pill('equivalent serial orders: <b>' + r.orders + '</b>') : '') + pill('recoverability: <b>' + r.cls + '</b>', r.cls === 'strict' || r.cls.startsWith('cascadeless') ? 'y' : r.rec ? '' : 'n'); }
  $('#s', el).oninput = run; run();
};
// ---------- CPU scheduling ----------
W.cpusched = el => {
  const D = [[0, 8, 3], [1, 4, 1], [2, 9, 4], [3, 5, 2]];
  el.innerHTML = '<div class="row"><label>Algorithm</label><select id="al"><option value="fcfs">FCFS</option><option value="sjf">SJF (non-preemptive)</option><option value="srtf">SRTF (preemptive SJF)</option><option value="prio">Priority (non-preemptive, lower number = higher)</option><option value="rr">Round Robin</option></select><label>Quantum</label><input type="number" id="q" value="3" min="1" max="10" style="width:70px"></div><table class="pt" style="margin:8px 0"><thead><tr><th></th><th>Arrival</th><th>Burst</th><th>Priority</th></tr></thead><tbody>' + D.map((d, i) => '<tr><td><b style="color:' + COL[i] + '">P' + (i + 1) + '</b></td>' + d.map(v => '<td><input type="number" min="0" max="20" value="' + v + '" style="width:64px"></td>').join('') + '</tr>').join('') + '</tbody></table><div class="gantt" id="g" style="display:flex;gap:2px;overflow-x:auto;padding-bottom:22px"></div><div style="overflow-x:auto"><table class="tt" id="tb"></table></div><div class="out" id="o"></div>';
  function run() { const procs = $$('tbody tr', el).map(tr => { const v = $$('input', tr).map(i => Math.max(0, +i.value || 0)); return {at: v[0], bt: Math.max(1, v[1]), pr: v[2]}; }); const al = $('#al', el).value, r = LW.cpuSched(al, procs, Math.max(1, +$('#q', el).value | 0));
    $('#g', el).innerHTML = r.tl.map((x, i) => '<div style="flex:none;width:28px;height:34px;border-radius:5px;display:grid;place-items:center;font-size:.7rem;font-weight:800;position:relative;background:' + (x === null ? 'var(--bg2)' : COL[x]) + ';color:#04121f">' + (x === null ? '' : 'P' + (x + 1)) + '<span style="position:absolute;top:100%;left:0;font-size:.62rem;color:var(--mut2);font-weight:600">' + i + '</span></div>').join('');
    $('#tb', el).innerHTML = '<tr><th>Process</th><th>AT</th><th>BT</th><th>CT</th><th>TAT</th><th>WT</th><th>RT</th></tr>' + procs.map((p, i) => '<tr><td style="color:' + COL[i] + '">P' + (i + 1) + '</td><td>' + p.at + '</td><td>' + p.bt + '</td><td>' + r.ct[i] + '</td><td>' + r.tat[i] + '</td><td>' + r.wt[i] + '</td><td>' + r.rt[i] + '</td></tr>').join('');
    $('#o', el).innerHTML = pill('avg waiting time = <b>' + r.avgWT.toFixed(2) + '</b>', 'y') + pill('avg turnaround = <b>' + r.avgTAT.toFixed(2) + '</b>') + pill('context switches = ' + r.sw) + pill('TAT = CT − AT · WT = TAT − BT · RT = first run − AT'); }
  $$('input,select', el).forEach(i => { i.oninput = run; i.onchange = run; }); run();
};
// ---------- page replacement ----------
W.pagerep = el => {
  el.innerHTML = '<div class="row"><label>Reference string</label><input type="text" id="r" value="1 2 3 4 1 2 5 1 2 3 4 5" style="flex:1;min-width:220px"><label>Frames</label><input type="number" id="k" value="3" min="1" max="6" style="width:70px"></div><div class="row" id="pre" style="margin:8px 0"><button class="btn sm">Belady string (1 2 3 4 1 2 5 1 2 3 4 5)</button><button class="btn sm">Textbook (7 0 1 2 0 3 0 4 2 3 0 3 2)</button></div><div style="overflow-x:auto"><table class="tt" id="tb"></table></div><div class="out" id="o"></div>';
  $$('#pre .btn', el)[0].onclick = () => { $('#r', el).value = '1 2 3 4 1 2 5 1 2 3 4 5'; run(); }; $$('#pre .btn', el)[1].onclick = () => { $('#r', el).value = '7 0 1 2 0 3 0 4 2 3 0 3 2'; run(); };
  function run() { const ref = nums($('#r', el).value).slice(0, 30), k = Math.max(1, Math.min(6, +$('#k', el).value | 0)); if (!ref.length) return; const R = {fifo: LW.pageRep('fifo', ref, k), lru: LW.pageRep('lru', ref, k), opt: LW.pageRep('opt', ref, k)}, S = R.lru.steps;
    let h = '<tr><th>algorithm</th>' + ref.map(x => '<th>' + x + '</th>').join('') + '<th>faults</th></tr>'; ['fifo', 'lru', 'opt'].forEach(a => { h += '<tr><td><b>' + a.toUpperCase() + '</b></td>' + R[a].steps.map(s => '<td style="color:' + (s.fault ? 'var(--bad)' : 'var(--ok)') + '" title="frames: ' + s.frames.join(',') + '">' + (s.fault ? '✘' : '✔') + '</td>').join('') + '<td><b>' + R[a].faults + '</b></td></tr>'; });
    $('#tb', el).innerHTML = h; const f3 = LW.pageRep('fifo', ref, 3).faults, f4 = LW.pageRep('fifo', ref, 4).faults;
    $('#o', el).innerHTML = pill('FIFO faults <b>' + R.fifo.faults + '</b>') + pill('LRU faults <b>' + R.lru.faults + '</b>') + pill('Optimal faults <b>' + R.opt.faults + '</b>', 'y') + pill('hit ratio (LRU) = ' + ((ref.length - R.lru.faults) / ref.length).toFixed(2)) + pill('FIFO with 3 frames: ' + f3 + ' · with 4 frames: ' + f4 + (f4 > f3 ? ' ← Belady\'s anomaly!' : ''), f4 > f3 ? 'n' : '') + '<div class="small muted" style="margin-top:8px;width:100%">Hover a cell to see the frame contents after that reference (final LRU frames: ' + S[S.length - 1].frames.join(', ') + ').</div>'; }
  $$('input', el).forEach(i => i.oninput = run); run();
};
// ---------- disk scheduling ----------
W.disk = el => {
  el.innerHTML = '<div class="row"><label>Requests</label><input type="text" id="r" value="98 183 37 122 14 124 65 67" style="flex:1;min-width:200px"><label>Head</label><input type="number" id="h" value="53" style="width:75px"><label>Cylinders 0–</label><input type="number" id="m" value="199" style="width:75px"></div><svg class="gsvg" id="sv" viewBox="0 0 560 250" style="margin-top:10px"></svg><div style="overflow-x:auto"><table class="tt" id="tb"></table></div>';
  function run() { const reqs = nums($('#r', el).value).slice(0, 12), head = +$('#h', el).value || 0, top = +$('#m', el).value || 199, algos = [['fcfs', 'FCFS'], ['sstf', 'SSTF'], ['scan', 'SCAN (up first)'], ['look', 'LOOK (up first)'], ['cscan', 'C-SCAN'], ['clook', 'C-LOOK']];
    let tb = '<tr><th>algorithm</th><th>total head movement</th><th>service order</th></tr>', best = Infinity; const res = algos.map(([a, n]) => { const r = LW.diskSched(a, head, reqs, top); best = Math.min(best, r.total); return [a, n, r]; });
    res.forEach(([a, n, r]) => tb += '<tr><td><b>' + n + '</b></td><td' + (r.total === best ? ' style="color:var(--ok);font-weight:800"' : '') + '>' + r.total + '</td><td style="text-align:left">' + r.order.join(' → ') + '</td></tr>'); $('#tb', el).innerHTML = tb + '<tr><td colspan="3" class="muted small" style="text-align:left;border:0">C-SCAN counts the head jump from the last cylinder back to 0; many textbooks exclude that jump.</td></tr>';
    const r = res[0][2], X = c => 20 + c / top * 520; let svg = ''; for (let i = 0; i < r.path.length - 1; i++) { const y1 = 20 + i * 215 / Math.max(1, r.path.length - 1), y2 = 20 + (i + 1) * 215 / Math.max(1, r.path.length - 1); svg += '<line x1="' + X(r.path[i]) + '" y1="' + y1 + '" x2="' + X(r.path[i + 1]) + '" y2="' + y2 + '" stroke="#22d3ee" stroke-width="2"/><circle cx="' + X(r.path[i + 1]) + '" cy="' + y2 + '" r="4" fill="#22d3ee"/><text x="' + (X(r.path[i + 1]) + 6) + '" y="' + (y2 - 4) + '" fill="var(--mut)" font-size="10">' + r.path[i + 1] + '</text>'; } svg += '<circle cx="' + X(head) + '" cy="20" r="5" fill="#fbbf24"/><text x="20" y="245" fill="var(--mut)" font-size="11">FCFS head path (top to bottom = time) · cylinders 0 → ' + top + '</text>'; $('#sv', el).innerHTML = svg; }
  $$('input', el).forEach(i => i.oninput = run); run();
};
// ---------- Banker's algorithm ----------
W.banker = el => {
  el.innerHTML = '<div class="small muted">Resources A B C — classic textbook state (5 processes). Edit any number.</div><div style="overflow-x:auto;margin-top:8px"><table class="pt" id="t"><thead><tr><th></th><th colspan="3">Allocation</th><th colspan="3">Max</th></tr></thead><tbody></tbody></table></div><div class="row" style="margin-top:8px"><label>Available</label><input type="text" id="av" value="3 3 2" style="width:110px"></div><div class="out" id="o"></div>';
  const A = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]], M = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]];
  $('#t tbody', el).innerHTML = A.map((a, i) => '<tr><td><b>P' + i + '</b></td>' + a.concat(M[i]).map(v => '<td><input type="number" min="0" value="' + v + '" style="width:52px"></td>').join('') + '</tr>').join('');
  function run() { const rows = $$('#t tbody tr', el).map(tr => $$('input', tr).map(i => Math.max(0, +i.value || 0))), alloc = rows.map(r => r.slice(0, 3)), max = rows.map(r => r.slice(3)), av = nums($('#av', el).value).slice(0, 3); while (av.length < 3) av.push(0); const r = LW.banker(alloc, max, av);
    $('#o', el).innerHTML = pill('Need = Max − Allocation: ' + r.need.map((n, i) => 'P' + i + '(' + n.join(',') + ')').join(' ')) + pill(r.safe ? '✔ SAFE — safe sequence: <b>' + r.seq.map(i => 'P' + i).join(' → ') + '</b>' : '✘ UNSAFE state (stuck after: ' + (r.seq.map(i => 'P' + i).join(' → ') || 'nothing') + ')', r.safe ? 'y' : 'n') + (r.safe ? '' : pill('an unsafe state does not always deadlock, but deadlock is now possible')); }
  $$('input', el).forEach(i => i.oninput = run); run();
};
// ---------- address translation ----------
W.addr = el => {
  el.innerHTML = '<div class="row"><label>Logical address bits</label><input type="number" id="la" value="32" style="width:75px"><label>Physical address bits</label><input type="number" id="pa" value="28" style="width:75px"><label>Page size</label><select id="ps"><option>1 KB</option><option>2 KB</option><option selected>4 KB</option><option>8 KB</option><option>16 KB</option></select><label>PTE size (bytes)</label><input type="number" id="pte" value="4" style="width:70px"></div><div class="out" id="o"></div><div class="small muted" style="margin-top:8px">Also try: logical address → (page number, offset) with the box below.</div><div class="row" style="margin-top:6px"><label>Logical address</label><input type="number" id="ad" value="123456" style="width:130px"></div><div class="out" id="o2"></div>';
  function run() { const la = +$('#la', el).value, pa = +$('#pa', el).value, ps = parseInt($('#ps', el).value) * 1024, pte = +$('#pte', el).value || 4, off = Math.log2(ps), np = 2 ** (la - off), nf = 2 ** (pa - off), pt = np * pte;
    $('#o', el).innerHTML = pill('offset bits = <b>' + off + '</b>') + pill('page-number bits = <b>' + (la - off) + '</b>') + pill('pages = <b>' + np.toLocaleString() + '</b>') + pill('frame-number bits = <b>' + (pa - off) + '</b>') + pill('frames = <b>' + nf.toLocaleString() + '</b>') + pill('page-table size = <b>' + (pt >= 1048576 ? (pt / 1048576).toFixed(2) + ' MB' : (pt / 1024).toFixed(1) + ' KB') + '</b>', 'y') + pill('page table pages = ' + Math.ceil(pt / ps)) + pill('levels needed (each table in one page) = ' + Math.ceil((la - off) / Math.log2(ps / pte)));
    const ad = Math.floor(+$('#ad', el).value) || 0; $('#o2', el).innerHTML = pill('page number = ⌊' + ad + ' / ' + ps + '⌋ = <b>' + Math.floor(ad / ps) + '</b>') + pill('offset = ' + ad + ' mod ' + ps + ' = <b>' + (ad % ps) + '</b>', 'y'); }
  $$('input,select', el).forEach(i => { i.oninput = run; i.onchange = run; }); run();
};
$$('.wgt').forEach(el => { const f = W[el.dataset.w]; if (f && !el.dataset.done) { el.dataset.done = 1; try { f(el); } catch (e) { el.innerHTML = '<div class="pill n">Tool failed to load: ' + esc(e.message) + '</div>'; console.error(e); } } });
})();
