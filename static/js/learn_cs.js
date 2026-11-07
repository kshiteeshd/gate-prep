/* GATE Prep — learning modules: algorithms & data-structure tools (loaded after learn.js) */
(function () {
const G = typeof window !== 'undefined' ? window : globalThis;
const LW = G.LW = G.LW || {};

/* ======================= pure logic (unit-tested with node) ======================= */
LW.sortRun = function (algo, input) {
  const a = input.slice(); let cmp = 0, sw = 0; const frames = [{a: a.slice(), mark: [], note: 'start'}];
  const snap = (mark, note) => frames.push({a: a.slice(), mark: mark || [], note: note || ''});
  const swap = (i, j) => { [a[i], a[j]] = [a[j], a[i]]; sw++; snap([i, j], 'swap'); };
  if (algo === 'bubble') { for (let i = 0; i < a.length - 1; i++) { let sd = false; for (let j = 0; j < a.length - 1 - i; j++) { cmp++; if (a[j] > a[j + 1]) { swap(j, j + 1); sd = true; } } if (!sd) break; } }
  else if (algo === 'insertion') { for (let i = 1; i < a.length; i++) { const k = a[i]; let j = i - 1; while (j >= 0) { cmp++; if (a[j] > k) { a[j + 1] = a[j]; sw++; j--; snap([j + 1, j + 2], 'shift'); } else break; } a[j + 1] = k; snap([j + 1], 'insert'); } }
  else if (algo === 'selection') { for (let i = 0; i < a.length - 1; i++) { let m = i; for (let j = i + 1; j < a.length; j++) { cmp++; if (a[j] < a[m]) m = j; } if (m !== i) swap(i, m); } }
  else if (algo === 'merge') {
    const ms = (lo, hi) => { if (hi - lo < 1) return; const mid = (lo + hi) >> 1; ms(lo, mid); ms(mid + 1, hi); const L = a.slice(lo, mid + 1), R = a.slice(mid + 1, hi + 1); let i = 0, j = 0, k = lo;
      while (i < L.length && j < R.length) { cmp++; a[k++] = L[i] <= R[j] ? L[i++] : R[j++]; } while (i < L.length) a[k++] = L[i++]; while (j < R.length) a[k++] = R[j++]; snap(Array.from({length: hi - lo + 1}, (_, t) => lo + t), 'merge'); };
    ms(0, a.length - 1);
  } else if (algo === 'quick') {
    const qs = (lo, hi) => { if (lo >= hi) return; const p = a[hi]; let i = lo - 1; for (let j = lo; j < hi; j++) { cmp++; if (a[j] <= p) { i++; if (i !== j) swap(i, j); } } if (i + 1 !== hi) swap(i + 1, hi); else snap([hi], 'pivot'); qs(lo, i); qs(i + 2, hi); };
    qs(0, a.length - 1);
  }
  return {frames, cmp, sw, sorted: a};
};
LW.master = function (a, b, k, p) {   // T(n) = a T(n/b) + Θ(n^k log^p n)
  const L = Math.log(a) / Math.log(b), eps = 1e-9; let res, why;
  if (Math.abs(L - k) < eps) { res = 'Θ(n^' + k + ' log^' + (p + 1) + ' n)'; why = 'Case 2 (log_b a = k)'; }
  else if (L > k) { const e = Number.isInteger(Math.round(L * 1e6) / 1e6) ? Math.round(L) : Math.round(L * 1000) / 1000; res = 'Θ(n^' + e + ')'; why = 'Case 1 (leaves dominate: log_b a > k)'; }
  else { res = p >= 0 ? 'Θ(n^' + k + (p ? ' log^' + p + ' n' : '') + ')' : 'Θ(n^' + k + ')'; why = p >= 0 ? 'Case 3 (root dominates: log_b a < k)' : 'Case 3 with p < 0 not covered'; }
  return {L, res: res.replace('n^1 ', 'n ').replace('n^1)', 'n)').replace('n^0 ', '').replace('Θ(n^0)', 'Θ(1)'), why};
};
LW.lcs = function (s, t) { const d = Array.from({length: s.length + 1}, () => Array(t.length + 1).fill(0)); for (let i = 1; i <= s.length; i++) for (let j = 1; j <= t.length; j++) d[i][j] = s[i - 1] === t[j - 1] ? d[i - 1][j - 1] + 1 : Math.max(d[i - 1][j], d[i][j - 1]); return d; };
LW.edit = function (s, t) { const d = Array.from({length: s.length + 1}, (_, i) => Array.from({length: t.length + 1}, (_, j) => i === 0 ? j : j === 0 ? i : 0)); for (let i = 1; i <= s.length; i++) for (let j = 1; j <= t.length; j++) d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (s[i - 1] !== t[j - 1])); return d; };
LW.knap = function (items, W) { const d = Array.from({length: items.length + 1}, () => Array(W + 1).fill(0)); items.forEach(([v, w], i) => { for (let c = 0; c <= W; c++) d[i + 1][c] = Math.max(d[i][c], c >= w ? d[i][c - w] + v : 0); }); return d; };
// ---- graphs (weighted, optional direction) ----
LW.parseG = function (text, directed) {
  const edges = []; text.split(/[,;\n]+/).forEach(s => { const m = s.trim().match(/^(\w+)\s*-+>?\s*(\w+)(?:\s*:\s*(-?\d+(?:\.\d+)?))?$/); if (m) edges.push([m[1], m[2], m[3] === undefined ? 1 : +m[3]]); });
  const vs = [...new Set(edges.flatMap(e => [e[0], e[1]]))].sort(); const adj = Object.fromEntries(vs.map(v => [v, []]));
  edges.forEach(([u, v, w]) => { adj[u].push([v, w]); if (!directed) adj[v].push([u, w]); }); vs.forEach(v => adj[v].sort((a, b) => a[0] < b[0] ? -1 : 1));
  return {vs, edges, adj, directed};
};
LW.bfs = (g, s) => { const seen = new Set([s]), q = [s], out = []; while (q.length) { const u = q.shift(); out.push(u); g.adj[u].forEach(([v]) => { if (!seen.has(v)) { seen.add(v); q.push(v); } }); } return out; };
LW.dfs = (g, s) => { const seen = new Set(), out = []; const go = u => { seen.add(u); out.push(u); g.adj[u].forEach(([v]) => { if (!seen.has(v)) go(v); }); }; go(s); return out; };
LW.dijkstra = (g, s) => { const d = Object.fromEntries(g.vs.map(v => [v, Infinity])), prev = {}, done = new Set(); d[s] = 0; for (;;) { let u = null; g.vs.forEach(v => { if (!done.has(v) && d[v] < Infinity && (u === null || d[v] < d[u])) u = v; }); if (u === null) break; done.add(u); g.adj[u].forEach(([v, w]) => { if (d[u] + w < d[v]) { d[v] = d[u] + w; prev[v] = u; } }); } return {d, prev}; };
LW.bellman = (g, s) => { const d = Object.fromEntries(g.vs.map(v => [v, Infinity])); d[s] = 0; const E = []; g.edges.forEach(([u, v, w]) => { E.push([u, v, w]); if (!g.directed) E.push([v, u, w]); }); for (let i = 0; i < g.vs.length - 1; i++) E.forEach(([u, v, w]) => { if (d[u] + w < d[v]) d[v] = d[u] + w; }); const neg = E.some(([u, v, w]) => d[u] + w < d[v]); return {d, neg}; };
LW.kruskal = g => { const p = Object.fromEntries(g.vs.map(v => [v, v])), f = x => p[x] === x ? x : (p[x] = f(p[x])); const T = []; let w = 0; g.edges.slice().sort((a, b) => a[2] - b[2]).forEach(([u, v, c]) => { if (f(u) !== f(v)) { p[f(u)] = f(v); T.push([u, v, c]); w += c; } }); return {T, w}; };
LW.prim = (g, s) => { const inT = new Set([s]), T = []; let w = 0; while (inT.size < g.vs.length) { let best = null; g.edges.forEach(([u, v, c]) => { if (inT.has(u) !== inT.has(v) && (best === null || c < best[2])) best = [u, v, c]; }); if (!best) break; T.push(best); w += best[2]; inT.add(best[0]); inT.add(best[1]); } return {T, w}; };
LW.topo = g => { const indeg = Object.fromEntries(g.vs.map(v => [v, 0])); g.edges.forEach(([u, v]) => indeg[v]++); const out = []; const ready = g.vs.filter(v => indeg[v] === 0); while (ready.length) { ready.sort(); const u = ready.shift(); out.push(u); g.adj[u].forEach(([v]) => { if (--indeg[v] === 0) ready.push(v); }); } return out.length === g.vs.length ? out : null; };
LW.scc = g => { const seen = new Set(), order = []; const d1 = u => { seen.add(u); g.adj[u].forEach(([v]) => { if (!seen.has(v)) d1(v); }); order.push(u); }; g.vs.forEach(v => { if (!seen.has(v)) d1(v); });
  const rev = Object.fromEntries(g.vs.map(v => [v, []])); g.edges.forEach(([u, v]) => rev[v].push(u)); const comp = []; const s2 = new Set(); order.reverse().forEach(u => { if (s2.has(u)) return; const c = []; const d2 = x => { s2.add(x); c.push(x); rev[x].forEach(y => { if (!s2.has(y)) d2(y); }); }; d2(u); comp.push(c.sort()); }); return comp; };
// ---- BST / AVL ----
LW.bstInsert = (root, k) => { if (!root) return {k, l: null, r: null}; if (k < root.k) root.l = LW.bstInsert(root.l, k); else if (k > root.k) root.r = LW.bstInsert(root.r, k); return root; };
LW.height = n => n ? 1 + Math.max(LW.height(n.l), LW.height(n.r)) : -1;
LW.inorder = n => n ? [...LW.inorder(n.l), n.k, ...LW.inorder(n.r)] : []; LW.preorder = n => n ? [n.k, ...LW.preorder(n.l), ...LW.preorder(n.r)] : []; LW.postorder = n => n ? [...LW.postorder(n.l), ...LW.postorder(n.r), n.k] : [];
LW.avlBuild = keys => { let rot = 0; const h = n => n ? n.h : 0, up = n => { n.h = 1 + Math.max(h(n.l), h(n.r)); };
  const rr = y => { const x = y.l; y.l = x.r; x.r = y; up(y); up(x); rot++; return x; }, rl = x => { const y = x.r; x.r = y.l; y.l = x; up(x); up(y); rot++; return y; };
  const ins = (n, k) => { if (!n) return {k, l: null, r: null, h: 1}; if (k < n.k) n.l = ins(n.l, k); else if (k > n.k) n.r = ins(n.r, k); else return n; up(n); const b = h(n.l) - h(n.r);
    if (b > 1) { if (k > n.l.k) n.l = rl(n.l); return rr(n); } if (b < -1) { if (k < n.r.k) n.r = rr(n.r); return rl(n); } return n; };
  let root = null; keys.forEach(k => root = ins(root, k)); return {root, rot}; };
// ---- heap ----
LW.heapInsert = (a, k, min) => { a = a.slice(); a.push(k); let i = a.length - 1; const bad = (p, c) => min ? a[p] > a[c] : a[p] < a[c]; while (i > 0 && bad((i - 1) >> 1, i)) { const p = (i - 1) >> 1;[a[p], a[i]] = [a[i], a[p]]; i = p; } return a; };
LW.heapPop = (a, min) => { a = a.slice(); if (!a.length) return {a, top: null}; const top = a[0]; a[0] = a[a.length - 1]; a.pop(); const n = a.length; let i = 0; for (;;) { const l = 2 * i + 1, r = l + 1; let m = i; const better = (x, y) => min ? a[x] < a[y] : a[x] > a[y]; if (l < n && better(l, m)) m = l; if (r < n && better(r, m)) m = r; if (m === i) break;[a[i], a[m]] = [a[m], a[i]]; i = m; } return {a, top}; };
LW.buildHeap = (a, min) => { a = a.slice(); const n = a.length; let sw = 0; const better = (x, y) => min ? a[x] < a[y] : a[x] > a[y]; for (let s = (n >> 1) - 1; s >= 0; s--) { let i = s; for (;;) { const l = 2 * i + 1, r = l + 1; let m = i; if (l < n && better(l, m)) m = l; if (r < n && better(r, m)) m = r; if (m === i) break;[a[i], a[m]] = [a[m], a[i]]; sw++; i = m; } } return {a, sw}; };
// ---- hashing ----
LW.hashRun = (keys, m, mode) => { const t = Array(m).fill(null), chains = Array.from({length: m}, () => []); let coll = 0; const log = [];
  keys.forEach(k => { if (mode === 'chain') { if (chains[k % m].length) coll++; chains[k % m].push(k); log.push([k, k % m]); return; }
    for (let i = 0; i < m; i++) { const pos = mode === 'linear' ? (k + i) % m : mode === 'quad' ? (k + i * i) % m : (k % m + i * (1 + k % (m - 1))) % m; if (t[pos] === null) { t[pos] = k; log.push([k, pos, i]); return; } coll++; } log.push([k, null]); });
  return {t, chains, coll, log}; };
// ---- recursion ----
LW.fibCalls = (n, memo) => { let calls = 0; const seen = {}; const f = k => { calls++; if (k < 2) return k; if (memo && k in seen) return seen[k]; const v = f(k - 1) + f(k - 2); if (memo) seen[k] = v; return v; }; const v = f(n); return {v, calls}; };
// ---- stacks ----
LW.toPostfix = s => { const prec = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}, out = [], st = []; const toks = s.match(/[A-Za-z0-9]+|[-+*/^()]/g) || []; toks.forEach(t => { if (/^[A-Za-z0-9]+$/.test(t)) out.push(t); else if (t === '(') st.push(t); else if (t === ')') { while (st.length && st[st.length - 1] !== '(') out.push(st.pop()); st.pop(); } else { while (st.length && st[st.length - 1] !== '(' && (prec[st[st.length - 1]] > prec[t] || (prec[st[st.length - 1]] === prec[t] && t !== '^'))) out.push(st.pop()); st.push(t); } }); while (st.length) out.push(st.pop()); return out; };
LW.evalPostfix = toks => { const st = []; toks.forEach(t => { if (/^-?\d+(\.\d+)?$/.test(t)) st.push(+t); else { const b = st.pop(), a = st.pop(); st.push(t === '+' ? a + b : t === '-' ? a - b : t === '*' ? a * b : t === '/' ? Math.trunc(a / b) : Math.pow(a, b)); } }); return st[0]; };

if (typeof document === 'undefined') return;

/* ======================= widgets ======================= */
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const W = G.LW_W = G.LW_W || {};
const COL = ['#22d3ee', '#38bdf8', '#34d399', '#fbbf24', '#fb7185', '#f97316', '#22d3ee', '#e879f9'];
const pill = (t, c) => '<span class="pill ' + (c || '') + '">' + t + '</span>';
const nums = s => s.split(/[\s,;]+/).filter(Boolean).map(Number).filter(x => !isNaN(x));

// ---------- sorting visualiser ----------
W.sort = el => {
  el.innerHTML = '<div class="row"><label>Array</label><input type="text" id="arr" value="5 2 9 1 7 3 8" style="flex:1;min-width:200px"><label>Algorithm</label><select id="al"><option value="bubble">Bubble sort</option><option value="insertion">Insertion sort</option><option value="selection">Selection sort</option><option value="merge">Merge sort</option><option value="quick">Quick sort (Lomuto, last pivot)</option></select></div>' +
    '<div class="row" style="margin-top:8px"><button class="btn sm" id="pv">⏮</button><button class="btn sm" id="nx">⏭ Step</button><button class="btn sm pri" id="pl">▶ Play</button><button class="btn sm" id="rn">Random</button><input type="range" id="fr" min="0" max="0" value="0" style="flex:1"></div><svg class="gsvg" id="sv" viewBox="0 0 560 220" style="margin-top:10px"></svg><div class="out" id="st"></div>';
  let R, f = 0, tm = null;
  function load() { clearInterval(tm); tm = null; $('#pl', el).textContent = '▶ Play'; const a = nums($('#arr', el).value).slice(0, 16); if (a.length < 2) { $('#st', el).innerHTML = pill('Enter at least 2 numbers', 'n'); return; } R = LW.sortRun($('#al', el).value, a); f = 0; $('#fr', el).max = R.frames.length - 1; draw(); }
  function draw() { const fr = R.frames[f], mx = Math.max(...fr.a, 1), w = 520 / fr.a.length; $('#fr', el).value = f;
    $('#sv', el).innerHTML = fr.a.map((v, i) => '<rect x="' + (20 + i * w) + '" y="' + (200 - v / mx * 170) + '" width="' + (w - 6) + '" height="' + (v / mx * 170) + '" rx="5" fill="' + (fr.mark.includes(i) ? '#fbbf24' : f === R.frames.length - 1 ? '#34d399' : '#22d3ee') + '"/><text x="' + (20 + i * w + (w - 6) / 2) + '" y="' + (196 - v / mx * 170) + '" text-anchor="middle" fill="var(--txt)" font-size="13" font-weight="700">' + v + '</text>').join('');
    $('#st', el).innerHTML = pill('step ' + f + ' / ' + (R.frames.length - 1) + (fr.note ? ' · ' + fr.note : '')) + pill('comparisons (total): <b>' + R.cmp + '</b>') + pill('swaps/shifts (total): <b>' + R.sw + '</b>') + (f === R.frames.length - 1 ? pill('sorted ✔', 'y') : ''); }
  $('#arr', el).oninput = load; $('#al', el).onchange = load; $('#fr', el).oninput = () => { f = +$('#fr', el).value; draw(); };
  $('#nx', el).onclick = () => { if (f < R.frames.length - 1) { f++; draw(); } }; $('#pv', el).onclick = () => { if (f > 0) { f--; draw(); } };
  $('#pl', el).onclick = () => { if (tm) { clearInterval(tm); tm = null; $('#pl', el).textContent = '▶ Play'; return; } if (f >= R.frames.length - 1) f = 0; $('#pl', el).textContent = '⏸ Pause'; tm = setInterval(() => { if (f >= R.frames.length - 1) { clearInterval(tm); tm = null; $('#pl', el).textContent = '▶ Play'; return; } f++; draw(); }, 450); };
  $('#rn', el).onclick = () => { $('#arr', el).value = Array.from({length: 8}, () => 1 + Math.floor(Math.random() * 20)).join(' '); load(); }; load();
};
// ---------- growth rates ----------
W.growth = el => {
  const F = [['1', n => 1], ['log n', n => Math.log2(n)], ['√n', n => Math.sqrt(n)], ['n', n => n], ['n log n', n => n * Math.log2(n)], ['n²', n => n * n], ['n³', n => n ** 3], ['2ⁿ', n => 2 ** n], ['n!', n => { let r = 1; for (let i = 2; i <= n; i++) r *= i; return r; }]];
  el.innerHTML = '<div class="row"><label>n</label><input type="range" id="n" min="2" max="30" value="10"><b id="nv">10</b></div><canvas class="cv" id="cv" width="640" height="300" style="margin-top:8px"></canvas><div class="small muted" style="margin-top:6px">Curves are drawn on a log scale so you can see all growth rates at once.</div><div style="overflow-x:auto"><table class="tt" id="tb"></table></div>';
  function draw() { const n = +$('#n', el).value; $('#nv', el).textContent = n; const c = $('#cv', el), g = c.getContext('2d'), w = c.width, h = c.height; g.clearRect(0, 0, w, h);
    const css = getComputedStyle(document.documentElement), mut = css.getPropertyValue('--mut').trim() || '#888', ymax = Math.log10(Math.max(1e3, F[F.length - 1][1](30)));
    const X = x => 30 + (x - 1) / 29 * (w - 50), Y = v => h - 20 - Math.max(0, Math.log10(Math.max(v, 1))) / ymax * (h - 40);
    g.strokeStyle = mut; g.globalAlpha = .4; g.beginPath(); g.moveTo(30, 10); g.lineTo(30, h - 20); g.lineTo(w - 10, h - 20); g.stroke(); g.globalAlpha = 1; g.font = '11px Segoe UI'; g.fillStyle = mut;
    F.forEach(([name, f], k) => { g.strokeStyle = COL[k % COL.length]; g.lineWidth = 2; g.beginPath(); for (let x = 2; x <= 30; x += .5) { const y = Y(f(x)); x === 2 ? g.moveTo(X(x), y) : g.lineTo(X(x), y); } g.stroke(); g.fillStyle = COL[k % COL.length]; g.fillText(name, w - 70, Y(f(30)) + 4 > h - 25 ? h - 25 : Math.max(14, Y(f(30)) + 4) - (k % 3) * 0); });
    g.strokeStyle = mut; g.setLineDash([4, 4]); g.beginPath(); g.moveTo(X(n), 10); g.lineTo(X(n), h - 20); g.stroke(); g.setLineDash([]);
    $('#tb', el).innerHTML = '<tr><th>f(n)</th>' + F.map(f => '<th>' + f[0] + '</th>').join('') + '</tr><tr><td>n = ' + n + '</td>' + F.map(f => '<td>' + (f[1](n) > 1e9 ? f[1](n).toExponential(1) : Math.round(f[1](n) * 100) / 100) + '</td>').join('') + '</tr>'; }
  $('#n', el).oninput = draw; draw();
};
// ---------- master theorem solver ----------
W.master = el => {
  el.innerHTML = '<div class="small muted">Solve  T(n) = a·T(n/b) + Θ(nᵏ logᵖ n)</div><div class="row" style="margin-top:8px"><label>a</label><input type="number" id="a" value="2" min="1" style="width:70px"><label>b</label><input type="number" id="b" value="2" min="2" style="width:70px"><label>k</label><input type="number" id="k" value="1" min="0" step="0.5" style="width:70px"><label>p</label><input type="number" id="p" value="0" min="-3" style="width:70px"></div><div class="row" id="pre" style="margin:8px 0"></div><div class="out" id="mo"></div>';
  const P = [['Merge sort', 2, 2, 1, 0], ['Binary search', 1, 2, 0, 0], ['Strassen', 7, 2, 2, 0], ['Karatsuba', 3, 2, 1, 0], ['Matrix-vector D&C', 4, 2, 2, 0], ['Tree traversal', 2, 2, 0, 0]];
  $('#pre', el).innerHTML = P.map(x => '<button class="btn sm">' + x[0] + '</button>').join(''); $$('#pre .btn', el).forEach((b, i) => b.onclick = () => { ['a', 'b', 'k', 'p'].forEach((id, j) => $('#' + id, el).value = P[i][j + 1]); run(); });
  function run() { const [a, b, k, p] = ['a', 'b', 'k', 'p'].map(i => +$('#' + i, el).value); if (a < 1 || b < 2) { $('#mo', el).innerHTML = pill('need a ≥ 1, b ≥ 2', 'n'); return; } const r = LW.master(a, b, k, p); $('#mo', el).innerHTML = pill('log_b a = ' + (Math.round(r.L * 1000) / 1000)) + pill('f(n) = n^' + k + (p ? ' log^' + p + ' n' : '')) + pill(r.why) + pill('T(n) = <b>' + r.res + '</b>', 'y'); }
  $$('input', el).forEach(i => i.oninput = run); run();
};
// ---------- DP tables ----------
W.dp = el => {
  el.innerHTML = '<div class="row"><label>Problem</label><select id="pr"><option value="lcs">Longest common subsequence</option><option value="edit">Edit distance</option><option value="knap">0/1 knapsack</option></select></div><div class="row" id="in" style="margin-top:8px"></div><div style="overflow-x:auto;margin-top:10px"><table class="tt" id="tb"></table></div><div class="out" id="ro"></div>';
  function inputs() { const p = $('#pr', el).value; $('#in', el).innerHTML = p === 'knap' ? '<label>Items (value:weight)</label><input type="text" id="it" value="10:5, 40:4, 30:6, 50:3" style="flex:1;min-width:220px"><label>Capacity</label><input type="number" id="cap" value="10" style="width:70px">' : '<label>String 1</label><input type="text" id="s" value="ABCBDAB" style="width:150px"><label>String 2</label><input type="text" id="t" value="BDCABA" style="width:150px">'; $$('input', $('#in', el)).forEach(i => i.oninput = run); run(); }
  function run() { const p = $('#pr', el).value; let d, rows, cols, note;
    if (p === 'knap') { const items = $('#it', el).value.split(',').map(s => s.trim().split(':').map(Number)).filter(a => a.length === 2 && a[1] > 0), W_ = Math.max(0, Math.min(25, +$('#cap', el).value | 0)); d = LW.knap(items, W_); rows = ['—'].concat(items.map((x, i) => 'item ' + (i + 1) + ' (' + x[0] + ',' + x[1] + ')')); cols = Array.from({length: W_ + 1}, (_, i) => i); note = pill('best value = <b>' + d[items.length][W_] + '</b>', 'y'); }
    else { const s = $('#s', el).value.slice(0, 12), t = $('#t', el).value.slice(0, 12); d = p === 'lcs' ? LW.lcs(s, t) : LW.edit(s, t); rows = ['ε'].concat([...s]); cols = ['ε'].concat([...t]); note = pill((p === 'lcs' ? 'LCS length' : 'edit distance') + ' = <b>' + d[s.length][t.length] + '</b>', 'y') + pill('table size ' + (s.length + 1) + ' × ' + (t.length + 1)); }
    $('#tb', el).innerHTML = '<tr><th></th>' + cols.map(c => '<th>' + esc(c) + '</th>').join('') + '</tr>' + d.map((r, i) => '<tr><th>' + esc(rows[i]) + '</th>' + r.map((v, j) => '<td' + (i === d.length - 1 && j === r.length - 1 ? ' style="background:rgba(52,211,153,.3)"' : '') + '>' + v + '</td>').join('') + '</tr>').join(''); $('#ro', el).innerHTML = note; }
  $('#pr', el).onchange = inputs; inputs();
};
// ---------- graph algorithms ----------
W.traverse = el => {
  el.innerHTML = '<label>Edges (u-v:weight, directed: u->v:weight)</label><textarea id="ed" rows="2">A-B:4, A-C:2, B-C:1, B-D:5, C-D:8, C-E:10, D-E:2</textarea><div class="row" style="margin-top:8px"><label>Algorithm</label><select id="al"><option value="bfs">BFS</option><option value="dfs">DFS</option><option value="dij">Dijkstra (shortest paths)</option><option value="bf">Bellman–Ford</option><option value="kru">Kruskal (MST)</option><option value="pri">Prim (MST)</option><option value="topo">Topological sort</option><option value="scc">Strongly connected components</option></select><label>Start</label><input type="text" id="st" value="A" style="width:60px"><label><input type="checkbox" id="dir" style="width:auto"> directed</label></div><svg class="gsvg" id="sv" viewBox="0 0 560 300" style="margin-top:10px"></svg><div class="out" id="ro"></div>';
  function run() { const dir = $('#dir', el).checked || ['topo', 'scc'].includes($('#al', el).value); if (['topo', 'scc'].includes($('#al', el).value)) $('#dir', el).checked = true;
    const txt = $('#ed', el).value.replace(/->/g, '->'); const g = LW.parseG($('#dir', el).checked ? txt.replace(/(\w)\s*-\s*(\w)/g, '$1->$2') : txt.replace(/->/g, '-'), $('#dir', el).checked); if (!g.vs.length) { $('#ro', el).innerHTML = pill('enter edges like A-B:3', 'n'); return; }
    let s = $('#st', el).value.trim(); if (!g.vs.includes(s)) s = g.vs[0]; const al = $('#al', el).value; let out = '', hi = new Set();
    if (al === 'bfs') out = pill('BFS order from ' + s + ': <b>' + LW.bfs(g, s).join(' → ') + '</b>', 'y'); if (al === 'dfs') out = pill('DFS order from ' + s + ': <b>' + LW.dfs(g, s).join(' → ') + '</b>', 'y');
    if (al === 'dij') { const r = LW.dijkstra(g, s); out = g.vs.map(v => pill(s + '→' + v + ' = <b>' + (r.d[v] === Infinity ? '∞' : r.d[v]) + '</b>', v === s ? '' : 'y')).join(''); Object.entries(r.prev).forEach(([v, u]) => hi.add(u + '|' + v)); }
    if (al === 'bf') { const r = LW.bellman(g, s); out = g.vs.map(v => pill(s + '→' + v + ' = <b>' + (r.d[v] === Infinity ? '∞' : r.d[v]) + '</b>')).join('') + pill(r.neg ? 'negative cycle detected!' : 'no negative cycle', r.neg ? 'n' : 'y'); }
    if (al === 'kru' || al === 'pri') { const r = al === 'kru' ? LW.kruskal(g) : LW.prim(g, s); out = pill('MST edges: <b>' + r.T.map(e => e[0] + e[1] + '(' + e[2] + ')').join(', ') + '</b>', 'y') + pill('total weight = <b>' + r.w + '</b>', 'y'); r.T.forEach(e => { hi.add(e[0] + '|' + e[1]); hi.add(e[1] + '|' + e[0]); }); }
    if (al === 'topo') { const t = LW.topo(g); out = t ? pill('topological order: <b>' + t.join(' → ') + '</b>', 'y') : pill('graph has a cycle — no topological order', 'n'); }
    if (al === 'scc') { const c = LW.scc(g); out = pill(c.length + ' strongly connected component(s): <b>' + c.map(x => '{' + x.join(',') + '}').join(' ') + '</b>', 'y'); }
    const n = g.vs.length, pos = Object.fromEntries(g.vs.map((v, i) => [v, [280 + 200 * Math.cos(2 * Math.PI * i / n - Math.PI / 2), 150 + 115 * Math.sin(2 * Math.PI * i / n - Math.PI / 2)]]));
    let svg = '<defs><marker id="ar" markerWidth="10" markerHeight="8" refX="26" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8z" fill="var(--mut)"/></marker></defs>';
    g.edges.forEach(([u, v, w]) => { const p = pos[u], q = pos[v], on = hi.has(u + '|' + v) || hi.has(v + '|' + u); svg += '<line x1="' + p[0] + '" y1="' + p[1] + '" x2="' + q[0] + '" y2="' + q[1] + '" stroke="' + (on ? '#34d399' : 'var(--line2)') + '" stroke-width="' + (on ? 4 : 2) + '"' + (g.directed ? ' marker-end="url(#ar)"' : '') + '/><text x="' + ((p[0] + q[0]) / 2) + '" y="' + ((p[1] + q[1]) / 2 - 5) + '" fill="var(--mut)" font-size="12" text-anchor="middle">' + w + '</text>'; });
    g.vs.forEach(v => svg += '<circle cx="' + pos[v][0] + '" cy="' + pos[v][1] + '" r="19" fill="' + (v === s ? '#38bdf8' : '#22d3ee') + '"/><text x="' + pos[v][0] + '" y="' + (pos[v][1] + 5) + '" text-anchor="middle" fill="#fff" font-weight="800">' + esc(v) + '</text>'); $('#sv', el).innerHTML = svg; $('#ro', el).innerHTML = out; }
  $$('input,textarea,select', el).forEach(i => { i.oninput = run; i.onchange = run; }); run();
};
// ---------- BST / AVL ----------
W.bst = el => {
  el.innerHTML = '<div class="row"><label>Insert keys in order</label><input type="text" id="ks" value="50 30 70 20 40 60 80 10" style="flex:1;min-width:200px"><label><input type="checkbox" id="avl" style="width:auto"> AVL (self-balancing)</label></div><svg class="gsvg" id="sv" viewBox="0 0 560 300" style="margin-top:10px"></svg><div class="out" id="ro"></div>';
  function run() { const keys = nums($('#ks', el).value).slice(0, 15), avl = $('#avl', el).checked; let root = null, rot = 0; if (avl) { const r = LW.avlBuild(keys); root = r.root; rot = r.rot; } else keys.forEach(k => root = LW.bstInsert(root, k));
    let svg = ''; const H = LW.height(root); const place = (n, x, y, dx) => { if (!n) return; [[n.l, -1], [n.r, 1]].forEach(([c, s]) => { if (c) { svg += '<line x1="' + x + '" y1="' + y + '" x2="' + (x + s * dx) + '" y2="' + (y + 52) + '" stroke="var(--line2)" stroke-width="2"/>'; place(c, x + s * dx, y + 52, dx / 2); } }); }; place(root, 280, 30, 130);
    const nodes = (n, x, y, dx) => { if (!n) return; svg += '<circle cx="' + x + '" cy="' + y + '" r="17" fill="#22d3ee"/><text x="' + x + '" y="' + (y + 5) + '" text-anchor="middle" fill="#fff" font-weight="800" font-size="13">' + n.k + '</text>'; nodes(n.l, x - dx, y + 52, dx / 2); nodes(n.r, x + dx, y + 52, dx / 2); }; nodes(root, 280, 30, 130); $('#sv', el).innerHTML = svg;
    const lv = (n) => !n ? 0 : (!n.l && !n.r ? 1 : lv(n.l) + lv(n.r));
    $('#ro', el).innerHTML = pill('height = <b>' + H + '</b>') + pill('nodes = <b>' + LW.inorder(root).length + '</b>') + pill('leaves = <b>' + lv(root) + '</b>') + (avl ? pill('rotations = <b>' + rot + '</b>', 'y') : '') + pill('inorder: <b>' + LW.inorder(root).join(' ') + '</b>', 'y') + pill('preorder: ' + LW.preorder(root).join(' ')) + pill('postorder: ' + LW.postorder(root).join(' ')); }
  $('#ks', el).oninput = run; $('#avl', el).onchange = run; run();
};
// ---------- heap ----------
W.heap = el => {
  el.innerHTML = '<div class="row"><label>Heap type</label><select id="ty"><option value="min">Min-heap</option><option value="max">Max-heap</option></select><input type="number" id="v" value="15" style="width:80px"><button class="btn sm pri" id="ins">Insert</button><button class="btn sm" id="pop">Extract root</button><button class="btn sm" id="bld">Build from list →</button><input type="text" id="lst" value="9 4 7 1 8 2 6" style="width:170px"><button class="btn sm" id="clr">Clear</button></div><svg class="gsvg" id="sv" viewBox="0 0 560 250" style="margin-top:10px"></svg><div class="out" id="ro"></div>';
  let a = [4, 9, 7, 15, 12]; const min = () => $('#ty', el).value === 'min';
  function draw(msg) { let svg = ''; const pos = i => { const d = Math.floor(Math.log2(i + 1)), idx = i + 1 - 2 ** d; return [280 + (idx - (2 ** d - 1) / 2) * (500 / 2 ** d), 28 + d * 52]; };
    a.forEach((_, i) => { if (i) { const p = pos((i - 1) >> 1), q = pos(i); svg += '<line x1="' + p[0] + '" y1="' + p[1] + '" x2="' + q[0] + '" y2="' + q[1] + '" stroke="var(--line2)" stroke-width="2"/>'; } }); a.forEach((v, i) => { const p = pos(i); svg += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="17" fill="' + (i === 0 ? '#38bdf8' : '#22d3ee') + '"/><text x="' + p[0] + '" y="' + (p[1] + 5) + '" text-anchor="middle" fill="#fff" font-weight="800" font-size="13">' + v + '</text>'; }); $('#sv', el).innerHTML = svg;
    $('#ro', el).innerHTML = pill('array: <b>[' + a.join(', ') + ']</b>', 'y') + pill('size ' + a.length + ' · height ' + (a.length ? Math.floor(Math.log2(a.length)) : '—')) + (a.length ? pill('children of index i: 2i+1, 2i+2 · parent: ⌊(i−1)/2⌋') : '') + (msg ? pill(msg) : ''); }
  $('#ins', el).onclick = () => { a = LW.heapInsert(a, +$('#v', el).value, min()); draw(); }; $('#pop', el).onclick = () => { const r = LW.heapPop(a, min()); a = r.a; draw(r.top === null ? 'empty' : 'extracted ' + r.top); };
  $('#bld', el).onclick = () => { const r = LW.buildHeap(nums($('#lst', el).value).slice(0, 15), min()); a = r.a; draw('Floyd build-heap used ' + r.sw + ' swaps'); }; $('#clr', el).onclick = () => { a = []; draw(); }; $('#ty', el).onchange = () => { a = LW.buildHeap(a, min()).a; draw(); }; draw();
};
// ---------- hashing ----------
W.hash = el => {
  el.innerHTML = '<div class="row"><label>Keys</label><input type="text" id="ks" value="12 25 38 51 64 9 22" style="flex:1;min-width:200px"><label>Table size m</label><input type="number" id="m" value="11" min="3" max="17" style="width:70px"><label>Method</label><select id="md"><option value="linear">Linear probing</option><option value="quad">Quadratic probing</option><option value="double">Double hashing</option><option value="chain">Chaining</option></select></div><div style="overflow-x:auto;margin-top:10px"><table class="tt" id="tb"></table></div><div class="out" id="ro"></div>';
  function run() { const keys = nums($('#ks', el).value).slice(0, 14), m = Math.max(3, Math.min(17, +$('#m', el).value | 0)), md = $('#md', el).value, r = LW.hashRun(keys, m, md);
    $('#tb', el).innerHTML = '<tr><th>slot</th><th>' + (md === 'chain' ? 'chain' : 'key') + '</th></tr>' + Array.from({length: m}, (_, i) => '<tr><td>' + i + '</td><td style="text-align:left">' + (md === 'chain' ? (r.chains[i].join(' → ') || '—') : (r.t[i] === null ? '—' : r.t[i])) + '</td></tr>').join('');
    $('#ro', el).innerHTML = pill('h(k) = k mod ' + m + (md === 'double' ? ', h₂(k) = 1 + k mod ' + (m - 1) : '')) + pill('collisions: <b>' + r.coll + '</b>', r.coll ? 'n' : 'y') + pill('load factor α = ' + (keys.length / m).toFixed(2)) + (r.log.some(l => l[1] === null) ? pill('some keys could not be placed (table full / probe cycle)', 'n') : ''); }
  $$('input,select', el).forEach(i => { i.oninput = run; i.onchange = run; }); run();
};
// ---------- recursion tree / call counter ----------
W.rectree = el => {
  el.innerHTML = '<div class="row"><label>fib(n), n =</label><input type="range" id="n" min="1" max="30" value="8"><b id="nv">8</b><label><input type="checkbox" id="me" style="width:auto"> memoise</label></div><svg class="gsvg" id="sv" viewBox="0 0 560 300" style="margin-top:10px"></svg><div class="out" id="ro"></div>';
  function run() { const n = +$('#n', el).value; $('#nv', el).textContent = n; const memo = $('#me', el).checked, r = LW.fibCalls(n, memo), t = LW.fibCalls(n, false); let svg = '', cnt = 0; const seen = {};
    const go = (k, x, y, dx, depth) => { if (depth > 4 || cnt > 40) return; cnt++; const cached = memo && k >= 2 && k in seen; svg += '<circle cx="' + x + '" cy="' + y + '" r="15" fill="' + (cached ? '#34d399' : '#22d3ee') + '"/><text x="' + x + '" y="' + (y + 4) + '" text-anchor="middle" fill="#fff" font-size="11" font-weight="800">' + k + '</text>'; if (k >= 2 && !cached) { [[k - 1, -1], [k - 2, 1]].forEach(([c, s]) => { svg += '<line x1="' + x + '" y1="' + y + '" x2="' + (x + s * dx) + '" y2="' + (y + 55) + '" stroke="var(--line2)"/>'; go(c, x + s * dx, y + 55, dx / 2, depth + 1); }); if (memo) seen[k] = 1; } };
    go(Math.min(n, 30), 280, 24, 130, 0); $('#sv', el).innerHTML = svg + '<text x="10" y="292" fill="var(--mut)" font-size="11">(tree shown to depth 4' + (memo ? '; green = answer reused from memo table' : '') + ')</text>';
    $('#ro', el).innerHTML = pill('fib(' + n + ') = <b>' + r.v + '</b>', 'y') + pill((memo ? 'calls with memoisation' : 'calls (naive)') + ' = <b>' + r.calls + '</b>', memo ? 'y' : 'n') + (memo ? pill('naive would need ' + t.calls) : pill('memoised: ' + LW.fibCalls(n, true).calls + ' calls')) + pill('time: ' + (memo ? 'O(n)' : 'O(2ⁿ)')); }
  $('#n', el).oninput = run; $('#me', el).onchange = run; run();
};
// ---------- bit operations ----------
W.bits = el => {
  el.innerHTML = '<div class="row"><label>x</label><input type="number" id="x" value="44" min="0" max="255" style="width:80px"><label>y</label><input type="number" id="y" value="27" min="0" max="255" style="width:80px"><label>shift k</label><input type="number" id="k" value="2" min="0" max="7" style="width:70px"></div><div style="overflow-x:auto"><table class="tt" id="tb" style="text-align:left"></table></div><div class="small muted" style="margin-top:8px">8-bit unsigned view. Signed (two\'s complement) value of the result is shown in brackets.</div>';
  function run() { const x = (+$('#x', el).value & 255), y = (+$('#y', el).value & 255), k = +$('#k', el).value & 7, b = v => (v & 255).toString(2).padStart(8, '0'), sg = v => (v & 255) > 127 ? (v & 255) - 256 : (v & 255);
    const rows = [['x', x], ['y', y], ['x & y', x & y], ['x | y', x | y], ['x ^ y', x ^ y], ['~x', ~x & 255], ['x << k', (x << k) & 255], ['x >> k (logical)', x >> k], ['x >> k (arithmetic)', (sg(x) >> k) & 255], ['−x (two\'s complement)', (-x) & 255]];
    $('#tb', el).innerHTML = '<tr><th>expression</th><th>binary</th><th>unsigned</th><th>signed</th></tr>' + rows.map(r => '<tr><td>' + r[0] + '</td><td class="mono">' + b(r[1]) + '</td><td>' + r[1] + '</td><td>' + sg(r[1]) + '</td></tr>').join(''); }
  $$('input', el).forEach(i => i.oninput = run); run();
};
// ---------- linked list ----------
W.llist = el => {
  el.innerHTML = '<div class="row"><input type="number" id="v" value="7" style="width:80px"><button class="btn sm" id="ih">Insert at head</button><button class="btn sm" id="it">Insert at tail</button><button class="btn sm" id="dh">Delete head</button><button class="btn sm" id="dt">Delete tail</button><button class="btn sm" id="rv">Reverse</button><button class="btn sm" id="cy">Make cycle (tail → node 2)</button><button class="btn sm" id="rs">Reset</button></div><svg class="gsvg" id="sv" viewBox="0 0 560 150" style="margin-top:10px;height:150px"></svg><div class="out" id="ro"></div>';
  let L = [3, 8, 1, 5], cyc = false, note = '';
  function draw() { let svg = '<defs><marker id="ar" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8z" fill="var(--mut)"/></marker></defs>'; const w = Math.min(90, 520 / Math.max(1, L.length));
    L.forEach((v, i) => { const x = 20 + i * w; svg += '<rect x="' + x + '" y="40" width="' + (w - 22) + '" height="40" rx="8" fill="var(--card2)" stroke="' + (i === 0 ? '#38bdf8' : 'var(--line2)') + '" stroke-width="2"/><text x="' + (x + (w - 22) / 2) + '" y="66" text-anchor="middle" fill="var(--txt)" font-weight="800">' + v + '</text>'; if (i < L.length - 1) svg += '<line x1="' + (x + w - 22) + '" y1="60" x2="' + (x + w - 2) + '" y2="60" stroke="var(--mut)" stroke-width="2" marker-end="url(#ar)"/>'; });
    if (L.length) { svg += '<text x="20" y="30" fill="#38bdf8" font-size="12" font-weight="700">head</text>'; if (cyc && L.length > 2) svg += '<path d="M' + (20 + (L.length - 1) * w + (w - 22) / 2) + ' 80 Q' + (20 + (L.length - 1) * w) + ' 130 ' + (20 + w + (w - 22) / 2) + ' 80" fill="none" stroke="#fb7185" stroke-width="2" marker-end="url(#ar)"/>'; else svg += '<text x="' + (20 + L.length * w - 10) + '" y="64" fill="var(--mut)" font-size="12">NULL</text>'; } $('#sv', el).innerHTML = svg;
    $('#ro', el).innerHTML = pill('length = <b>' + L.length + '</b>') + pill(cyc ? 'cycle present — Floyd\'s algorithm would detect it' : 'no cycle', cyc ? 'n' : 'y') + pill('insert at head O(1) · insert at tail O(n) (O(1) with tail pointer) · delete tail O(n) singly linked') + (note ? pill(note) : ''); }
  const act = (f, n) => () => { if (cyc && !/cycle|Reset/.test(n)) { note = 'break the cycle first (Reset)'; draw(); return; } f(); note = n; draw(); };
  $('#ih', el).onclick = act(() => L.unshift(+$('#v', el).value), 'new node linked before head: 2 pointer writes'); $('#it', el).onclick = act(() => L.push(+$('#v', el).value), 'walked n nodes to the tail');
  $('#dh', el).onclick = act(() => L.shift(), 'head advanced'); $('#dt', el).onclick = act(() => L.pop(), 'needed the second-last node'); $('#rv', el).onclick = act(() => L.reverse(), 'three pointers (prev, cur, next): O(n) time, O(1) space');
  $('#cy', el).onclick = () => { if (L.length > 2) { cyc = true; note = 'tail now points to node 2'; draw(); } }; $('#rs', el).onclick = () => { L = [3, 8, 1, 5]; cyc = false; note = ''; draw(); }; draw();
};
// ---------- stacks: infix → postfix ----------
W.stackq = el => {
  el.innerHTML = '<div class="row"><label>Infix expression</label><input type="text" id="ex" value="(2+3)*4-6/2" style="flex:1;min-width:220px"></div><div class="out" id="ro"></div><div class="small muted" style="margin-top:10px">Operators: + − * / ^ and parentheses; operands are letters or numbers. Shunting-yard: * / bind tighter than + −, ^ is right-associative.</div>';
  function run() { const ex = $('#ex', el).value, p = LW.toPostfix(ex); let html = pill('postfix: <b>' + p.join(' ') + '</b>', 'y'); if (p.length && p.every(t => /^-?\d+(\.\d+)?$|^[-+*/^]$/.test(t))) { try { html += pill('value = <b>' + LW.evalPostfix(p) + '</b>', 'y') + pill('stack operations: ' + p.length + ' tokens → ' + p.filter(t => /^\d/.test(t)).length + ' pushes, ' + p.filter(t => !/^\d/.test(t)).length + ' operator reductions'); } catch (e) { } } else html += pill('letters present — evaluation skipped'); $('#ro', el).innerHTML = html; }
  $('#ex', el).oninput = run; run();
};
// init for widgets declared after learn.js has already scanned
$$('.wgt').forEach(el => { const f = W[el.dataset.w]; if (f && !el.dataset.done) { el.dataset.done = 1; try { f(el); } catch (e) { el.innerHTML = '<div class="pill n">Tool failed to load: ' + esc(e.message) + '</div>'; console.error(e); } } });
})();
