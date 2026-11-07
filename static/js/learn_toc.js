/* GATE Prep — learning modules: automata (TOC) and grammar/parsing (Compiler Design) tools */
(function () {
const G = typeof window !== 'undefined' ? window : globalThis;
const LW = G.LW = G.LW || {};

/* ======================= pure logic (unit-tested with node) ======================= */
// ---- finite automata ----
// text: lines "start q0", "accept q2 q3", "q0 a q1" (use e for epsilon; repeat a line for nondeterminism)
LW.nfaParse = text => {
  const m = {start: null, acc: [], trans: {}, states: [], alpha: []}; const S = new Set(), A = new Set();
  text.split(/\n+/).map(l => l.trim()).filter(l => l && !l.startsWith('#')).forEach(l => {
    const p = l.split(/\s+/);
    if (p[0].toLowerCase() === 'start' && p.length === 2) { m.start = p[1]; S.add(p[1]); }
    else if (p[0].toLowerCase() === 'accept') { p.slice(1).forEach(x => { m.acc.push(x); S.add(x); }); }
    else if (p.length === 3) { const k = p[0] + '|' + p[1]; (m.trans[k] = m.trans[k] || []).push(p[2]); S.add(p[0]); S.add(p[2]); if (p[1] !== 'e') A.add(p[1]); }
  });
  m.states = [...S]; m.alpha = [...A].sort(); m.acc = [...new Set(m.acc)]; return m;
};
LW.epsClose = (m, set) => { const out = new Set(set), st = [...set]; while (st.length) { const u = st.pop(); (m.trans[u + '|e'] || []).forEach(v => { if (!out.has(v)) { out.add(v); st.push(v); } }); } return out; };
LW.nfaAccepts = (m, s) => { if (m.start === null) return false; let cur = LW.epsClose(m, [m.start]); for (const ch of s) { const nx = new Set(); cur.forEach(u => (m.trans[u + '|' + ch] || []).forEach(v => nx.add(v))); cur = LW.epsClose(m, nx); if (!cur.size) return false; } return m.acc.some(a => cur.has(a)); };
LW.isDeterministic = m => !Object.keys(m.trans).some(k => k.endsWith('|e') || m.trans[k].length > 1);
// subset construction -> complete DFA over m.alpha (the empty subset is the dead state, kept if reachable)
LW.subsetDfa = m => {
  const key = s => [...s].sort().join(','), start = LW.epsClose(m, m.start === null ? [] : [m.start]), names = {}, order = [], trans = {}, acc = new Set(); const q = [start]; names[key(start)] = start; order.push(key(start));
  while (q.length) { const s = q.shift(), ks = key(s); if (m.acc.some(a => s.has(a))) acc.add(ks);
    m.alpha.forEach(a => { const nx = new Set(); s.forEach(u => (m.trans[u + '|' + a] || []).forEach(v => nx.add(v))); const t = LW.epsClose(m, nx), kt = key(t); trans[ks + '|' + a] = kt; if (!(kt in names)) { names[kt] = t; order.push(kt); q.push(t); } }); }
  return {start: order[0], states: order, trans, acc, alpha: m.alpha};
};
// number of states of the minimal complete DFA (partition refinement)
LW.minDfaStates = m => {
  const d = LW.subsetDfa(m); let part = {}; d.states.forEach(s => part[s] = d.acc.has(s) ? 1 : 0); let n = new Set(Object.values(part)).size;
  for (;;) { const sig = {}; const np = {}; let c = 0; d.states.forEach(s => { const k = part[s] + '#' + d.alpha.map(a => part[d.trans[s + '|' + a]]).join(','); if (!(k in sig)) sig[k] = c++; np[s] = sig[k]; }); const nn = new Set(Object.values(np)).size; part = np; if (nn === n) break; n = nn; }
  return n;
};
// number of accepted strings of exactly length L
LW.countAccepted = (m, L) => { const d = LW.subsetDfa(m); let cur = {}; cur[d.start] = 1; for (let i = 0; i < L; i++) { const nx = {}; Object.keys(cur).forEach(s => d.alpha.forEach(a => { const t = d.trans[s + '|' + a]; nx[t] = (nx[t] || 0) + cur[s]; })); cur = nx; } return Object.keys(cur).filter(s => d.acc.has(s)).reduce((x, s) => x + cur[s], 0); };
// language emptiness / finiteness via useful states of the DFA
LW.langKind = m => {
  const d = LW.subsetDfa(m), succ = s => d.alpha.map(a => d.trans[s + '|' + a]); const reach = new Set([d.start]), st = [d.start]; while (st.length) { const u = st.pop(); succ(u).forEach(v => { if (!reach.has(v)) { reach.add(v); st.push(v); } }); }
  const useful = new Set([...reach].filter(s => d.acc.has(s))); let ch = true; while (ch) { ch = false; reach.forEach(s => { if (!useful.has(s) && succ(s).some(v => useful.has(v))) { useful.add(s); ch = true; } }); }
  if (!useful.has(d.start)) return 'empty'; const color = {}; const dfs = u => { color[u] = 1; for (const v of succ(u)) { if (!useful.has(v)) continue; if (color[v] === 1 || (!color[v] && dfs(v))) return true; } color[u] = 2; return false; };
  return dfs(d.start) ? 'infinite' : 'finite';
};

// ---- context-free grammars, FIRST/FOLLOW, LL(1), LR(0), SLR(1) ----
// text: "S -> A B | a | e"   (tokens separated by spaces; Uppercase-initial tokens are non-terminals; e / ε = epsilon)
LW.gParse = text => {
  const rules = [], nts = []; text.split(/\n+/).map(l => l.trim()).filter(Boolean).forEach(l => {
    const m = l.split(/->|→/); if (m.length !== 2) return; const lhs = m[0].trim(); if (!/^[A-Z][A-Za-z0-9']*$/.test(lhs)) return; if (!nts.includes(lhs)) nts.push(lhs);
    m[1].split('|').forEach(alt => { const toks = alt.trim().split(/\s+/).filter(Boolean).filter(t => !['e', 'ε', '#'].includes(t)); rules.push([lhs, toks]); });
  });
  const isNT = t => /^[A-Z]/.test(t); const ts = []; rules.forEach(r => r[1].forEach(t => { if (!isNT(t) && !ts.includes(t)) ts.push(t); }));
  return {start: nts[0], rules, nts, ts: ts.sort(), isNT};
};
LW.gSets = g => {
  const nullable = new Set(); let ch = true; while (ch) { ch = false; g.rules.forEach(([l, r]) => { if (!nullable.has(l) && r.every(t => g.isNT(t) && nullable.has(t))) { nullable.add(l); ch = true; } }); }
  const first = {}; g.nts.forEach(n => first[n] = new Set()); ch = true; while (ch) { ch = false; g.rules.forEach(([l, r]) => { for (const t of r) { if (!g.isNT(t)) { if (!first[l].has(t)) { first[l].add(t); ch = true; } break; } first[t].forEach(x => { if (!first[l].has(x)) { first[l].add(x); ch = true; } }); if (!nullable.has(t)) break; } }); }
  const firstSeq = seq => { const out = new Set(); let allNull = true; for (const t of seq) { if (!g.isNT(t)) { out.add(t); allNull = false; break; } first[t].forEach(x => out.add(x)); if (!nullable.has(t)) { allNull = false; break; } } return {set: out, nullable: allNull}; };
  const follow = {}; g.nts.forEach(n => follow[n] = new Set()); follow[g.start].add('$'); ch = true;
  while (ch) { ch = false; g.rules.forEach(([l, r]) => r.forEach((t, i) => { if (!g.isNT(t)) return; const f = firstSeq(r.slice(i + 1)); f.set.forEach(x => { if (!follow[t].has(x)) { follow[t].add(x); ch = true; } }); if (f.nullable) follow[l].forEach(x => { if (!follow[t].has(x)) { follow[t].add(x); ch = true; } }); })); }
  const srt = o => Object.fromEntries(g.nts.map(n => [n, [...o[n]].sort()]));
  return {nullable: g.nts.filter(n => nullable.has(n)), first: srt(first), follow: srt(follow), firstSeq};
};
LW.ll1 = g => {
  const s = LW.gSets(g), table = {}; g.rules.forEach(([l, r], i) => { const f = s.firstSeq(r), put = t => { const k = l + '|' + t; (table[k] = table[k] || []).push(i); }; f.set.forEach(put); if (f.nullable) s.follow[l].forEach(put); });
  const conflicts = Object.keys(table).filter(k => table[k].length > 1).sort(); return {ok: conflicts.length === 0, table, conflicts, sets: s};
};
LW.lr0 = g => {
  const R = [['S′', [g.start]]].concat(g.rules), all = n => R.map((r, i) => [r, i]).filter(([r]) => r[0] === n).map(([, i]) => i);
  const closure = items => { const out = new Set(items), st = [...items]; while (st.length) { const it = st.pop(), [ri, d] = it.split('.').map(Number), r = R[ri][1]; if (d < r.length && g.isNT(r[d])) all(r[d]).forEach(j => { const k = j + '.0'; if (!out.has(k)) { out.add(k); st.push(k); } }); } return out; };
  const key = s => [...s].sort().join(' '), go = (s, X) => { const nx = new Set(); s.forEach(it => { const [ri, d] = it.split('.').map(Number), r = R[ri][1]; if (d < r.length && r[d] === X) nx.add(ri + '.' + (d + 1)); }); return nx.size ? closure(nx) : null; };
  const start = closure(new Set(['0.0'])), states = [start], idx = {[key(start)]: 0}, edges = {}; for (let i = 0; i < states.length; i++) { const syms = new Set(); states[i].forEach(it => { const [ri, d] = it.split('.').map(Number), r = R[ri][1]; if (d < r.length) syms.add(r[d]); });
    [...syms].sort().forEach(X => { const t = go(states[i], X); if (!t) return; const k = key(t); if (!(k in idx)) { idx[k] = states.length; states.push(t); } edges[i + '|' + X] = idx[k]; }); }
  return {R, states, edges, n: states.length};
};
LW.slr = g => {
  const L = LW.lr0(g), s = LW.gSets(g), conflicts = [];
  L.states.forEach((st, i) => { const reds = {}; st.forEach(it => { const [ri, d] = it.split('.').map(Number), r = L.R[ri]; if (d === r[1].length && ri !== 0) s.follow[r[0]].forEach(t => (reds[t] = reds[t] || []).push(ri)); });
    Object.keys(reds).sort().forEach(t => { if (reds[t].length > 1) conflicts.push(i + ':reduce/reduce on ' + t); if ((i + '|' + t) in L.edges && !g.isNT(t)) conflicts.push(i + ':shift/reduce on ' + t); }); });
  return {ok: conflicts.length === 0, conflicts, lr0: L};
};

if (typeof document === 'undefined') return;

/* ======================= widgets ======================= */
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const W = G.LW_W = G.LW_W || {};
const pill = (t, c) => '<span class="pill ' + (c || '') + '">' + t + '</span>';

W.automata = el => {
  const P = [['DFA: ends in 01', 'start A\naccept C\nA 0 B\nA 1 A\nB 0 B\nB 1 C\nC 0 B\nC 1 A', '0101'], ['NFA: third symbol from end is 1', 'start p\naccept s\np 0 p\np 1 p\np 1 q\nq 0 r\nq 1 r\nr 0 s\nr 1 s', '10100'], ['NFA with ε', 'start s\naccept f\ns e a\ns e b\na 0 a\na 0 f\nb 1 b\nb 1 f', '0011'], ['Even number of 0s', 'start E\naccept E\nE 0 O\nE 1 E\nO 0 E\nO 1 O', '1001']];
  el.innerHTML = '<div class="row" id="pre" style="margin-bottom:8px"></div><div class="row" style="align-items:flex-start"><textarea id="t" rows="9" style="flex:1;min-width:230px;font-family:ui-monospace,monospace"></textarea><svg class="gsvg" id="sv" viewBox="0 0 400 260" style="flex:1;min-width:260px;height:260px"></svg></div><div class="row" style="margin:8px 0"><label>Test string</label><input type="text" id="w" style="width:200px" value="0101"><span class="mut" style="font-size:.78rem">format: <code>start q0</code>, <code>accept q1 q2</code>, <code>q0 a q1</code>, e = ε</span></div><div class="out" id="o"></div><div style="overflow-x:auto"><table class="tt" id="dt"></table></div>';
  $('#pre', el).innerHTML = P.map(p => '<button class="btn sm">' + p[0] + '</button>').join(''); $$('#pre .btn', el).forEach((b, i) => b.onclick = () => { $('#t', el).value = P[i][1]; $('#w', el).value = P[i][2]; run(); });
  $('#t', el).value = P[0][1];
  function run() { const m = LW.nfaParse($('#t', el).value), w = $('#w', el).value.trim(); if (m.start === null || !m.alpha.length) { $('#o', el).innerHTML = pill('Define “start X”, “accept Y” and transitions like “X a Y”.', 'n'); return; }
    const n = m.states.length, pos = {}; m.states.forEach((s, i) => pos[s] = [200 + 150 * Math.cos(2 * Math.PI * i / n - Math.PI / 2), 130 + 95 * Math.sin(2 * Math.PI * i / n - Math.PI / 2)]);
    const lab = {}; Object.keys(m.trans).forEach(k => { const [u, a] = k.split('|'); m.trans[k].forEach(v => { const kk = u + '>' + v; (lab[kk] = lab[kk] || []).push(a === 'e' ? 'ε' : a); }); });
    let svg = '<defs><marker id="ar2" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7z" fill="#7aa2c0"/></marker></defs>';
    Object.keys(lab).forEach(k => { const [u, v] = k.split('>'), p = pos[u], q = pos[v]; if (u === v) { svg += '<path d="M' + (p[0] - 8) + ',' + (p[1] - 17) + ' c-12,-30 28,-30 16,0" fill="none" stroke="#7aa2c0" stroke-width="1.6" marker-end="url(#ar2)"/><text x="' + p[0] + '" y="' + (p[1] - 36) + '" text-anchor="middle" font-size="11" fill="var(--txt)">' + lab[k].join(',') + '</text>'; return; }
      const dx = q[0] - p[0], dy = q[1] - p[1], L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L, x1 = p[0] + ux * 19, y1 = p[1] + uy * 19, x2 = q[0] - ux * 21, y2 = q[1] - uy * 21, cx = (x1 + x2) / 2 - uy * 18, cy = (y1 + y2) / 2 + ux * 18;
      svg += '<path d="M' + x1 + ',' + y1 + ' Q' + cx + ',' + cy + ' ' + x2 + ',' + y2 + '" fill="none" stroke="#7aa2c0" stroke-width="1.6" marker-end="url(#ar2)"/><text x="' + cx + '" y="' + cy + '" text-anchor="middle" font-size="11" fill="var(--txt)">' + lab[k].join(',') + '</text>'; });
    m.states.forEach(s => { const p = pos[s], a = m.acc.includes(s); svg += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="17" fill="var(--bg)" stroke="#22d3ee" stroke-width="2"/>' + (a ? '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="21" fill="none" stroke="#22d3ee" stroke-width="1.5"/>' : '') + '<text x="' + p[0] + '" y="' + (p[1] + 4) + '" text-anchor="middle" font-size="12" font-weight="700" fill="var(--txt)">' + esc(s) + '</text>'; });
    const sp = pos[m.start]; svg += '<path d="M' + (sp[0] - 45) + ',' + sp[1] + ' L' + (sp[0] - 22) + ',' + sp[1] + '" stroke="#34d399" stroke-width="2" marker-end="url(#ar2)"/>'; $('#sv', el).innerHTML = svg;
    const d = LW.subsetDfa(m), kind = LW.langKind(m), min = LW.minDfaStates(m), cnt = [0, 1, 2, 3, 4, 5, 6].map(L => LW.countAccepted(m, L)), ok = LW.nfaAccepts(m, w);
    $('#o', el).innerHTML = pill('“' + esc(w) + '” is ' + (ok ? '<b>accepted ✔</b>' : '<b>rejected ✘</b>'), ok ? 'y' : 'n') + pill(LW.isDeterministic(m) ? 'deterministic' : 'nondeterministic') + pill('subset-construction DFA states: <b>' + d.states.length + '</b>') + pill('minimal complete DFA states: <b>' + min + '</b>', 'y') + pill('language is <b>' + kind + '</b>') + pill('accepted strings of length 0…6: ' + cnt.join(', '));
    const nm = s => s === '' ? '∅' : '{' + s + '}'; $('#dt', el).innerHTML = '<tr><th>DFA state</th>' + m.alpha.map(a => '<th>' + esc(a) + '</th>').join('') + '</tr>' + d.states.map(s => '<tr><td>' + (s === d.start ? '→ ' : '') + (d.acc.has(s) ? '* ' : '') + esc(nm(s)) + '</td>' + m.alpha.map(a => '<td>' + esc(nm(d.trans[s + '|' + a])) + '</td>').join('') + '</tr>').join(''); }
  $('#t', el).oninput = run; $('#w', el).oninput = run; run();
};

W.grammar = el => {
  const P = [['Expression (LL(1) after removing left recursion)', "E -> T X\nX -> + T X | e\nT -> F Y\nY -> * F Y | e\nF -> ( E ) | id"], ['Left-recursive expression (SLR)', "E -> E + T | T\nT -> T * F | F\nF -> ( E ) | id"], ['Ambiguous / not LL(1)', "S -> i E t S | i E t S e S | a\nE -> b"], ['Not SLR(1)', "S -> L = R | R\nL -> * R | id\nR -> L"], ['Nullable chain', "S -> A B\nA -> a A | e\nB -> b B | e"]];
  el.innerHTML = '<div class="row" id="pre" style="margin-bottom:8px"></div><textarea id="g" rows="6" style="width:100%;font-family:ui-monospace,monospace"></textarea><div class="mut" style="font-size:.78rem;margin:4px 0 8px">One rule per line, tokens separated by spaces, alternatives with |, <code>e</code> = ε, Uppercase tokens = non-terminals, the first rule’s left side is the start symbol.</div><div class="out" id="o"></div><div style="overflow-x:auto"><table class="tt" id="fs"></table></div><div style="overflow-x:auto;margin-top:8px"><table class="tt" id="tb"></table></div>';
  $('#pre', el).innerHTML = P.map(p => '<button class="btn sm">' + esc(p[0]) + '</button>').join(''); $$('#pre .btn', el).forEach((b, i) => b.onclick = () => { $('#g', el).value = P[i][1]; run(); }); $('#g', el).value = P[0][1];
  function run() { const g = LW.gParse($('#g', el).value); if (!g.rules.length) { $('#o', el).innerHTML = pill('Enter rules like  S -> a S | b', 'n'); return; }
    const l = LW.ll1(g), s = l.sets, sl = LW.slr(g), cell = (nt, t) => (l.table[nt + '|' + t] || []).map(i => g.rules[i][0] + '→' + (g.rules[i][1].join(' ') || 'ε')).join('<br>');
    $('#o', el).innerHTML = pill(l.ok ? '✔ LL(1)' : '✘ not LL(1): conflicts at ' + l.conflicts.map(esc).join(', '), l.ok ? 'y' : 'n') + pill('LR(0) automaton: <b>' + sl.lr0.n + '</b> states (augmented grammar)') + pill(sl.ok ? '✔ SLR(1)' : '✘ not SLR(1): ' + sl.conflicts.slice(0, 3).map(esc).join('; '), sl.ok ? 'y' : 'n') + pill('nullable: ' + (s.nullable.join(', ') || 'none'));
    $('#fs', el).innerHTML = '<tr><th>Non-terminal</th><th>FIRST</th><th>FOLLOW</th></tr>' + g.nts.map(n => '<tr><td><b>' + esc(n) + '</b></td><td>{ ' + s.first[n].map(x => esc(x)).join(', ') + (s.nullable.includes(n) ? ', ε' : '') + ' }</td><td>{ ' + s.follow[n].map(esc).join(', ') + ' }</td></tr>').join('');
    const cols = g.ts.concat(['$']); $('#tb', el).innerHTML = '<tr><th>LL(1) table</th>' + cols.map(t => '<th>' + esc(t) + '</th>').join('') + '</tr>' + g.nts.map(n => '<tr><td><b>' + esc(n) + '</b></td>' + cols.map(t => { const c = cell(n, t); const bad = (l.table[n + '|' + t] || []).length > 1; return '<td style="' + (bad ? 'background:rgba(251,113,133,.18)' : '') + '">' + c + '</td>'; }).join('') + '</tr>').join(''); }
  $('#g', el).oninput = run; run();
};
$$('.wgt').forEach(el => { const f = W[el.dataset.w]; if (f && !el.dataset.done && ['automata', 'grammar'].includes(el.dataset.w)) { el.dataset.done = 1; try { f(el); } catch (e) { el.innerHTML = '<div class="pill n">Tool failed to load: ' + esc(e.message) + '</div>'; console.error(e); } } });
})();
