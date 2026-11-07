/* GATE Prep — learning modules: page behaviour + interactive tools */
(function () {
const G = typeof window !== 'undefined' ? window : globalThis;
const LW = {};
G.LW = LW;

/* ======================= pure logic (unit-tested with node) ======================= */
// ---- boolean expression parser ----
LW.parseBool = function (src) {
  const toks = []; const re = /\s*(<->|<=>|↔|->|=>|→|&&|\|\||[&|^!~¬∧∨⊕()]|[pqrsPQRS]|T|F|1|0)/y; let m; re.lastIndex = 0;
  const s = src.trim();
  while (re.lastIndex < s.length && (m = re.exec(s))) toks.push(m[1]);
  if (toks.join('').replace(/\s/g, '').length !== s.replace(/\s/g, '').length) throw new Error('Unrecognised symbol');
  const OP = {'&': 'and', '∧': 'and', '&&': 'and', '|': 'or', '∨': 'or', '||': 'or', '^': 'xor', '⊕': 'xor', '!': 'not', '~': 'not', '¬': 'not', '->': 'imp', '=>': 'imp', '→': 'imp', '<->': 'iff', '<=>': 'iff', '↔': 'iff'};
  let i = 0; const peek = () => toks[i], take = () => toks[i++];
  const iff = () => { let a = imp(); while (OP[peek()] === 'iff') { take(); const b = imp(); const x = a; a = e => x(e) === b(e); } return a; };
  const imp = () => { const a = or(); if (OP[peek()] === 'imp') { take(); const b = imp(); return e => !a(e) || b(e); } return a; };
  const or = () => { let a = xor(); while (OP[peek()] === 'or') { take(); const b = xor(); const x = a; a = e => x(e) || b(e); } return a; };
  const xor = () => { let a = and(); while (OP[peek()] === 'xor') { take(); const b = and(); const x = a; a = e => x(e) !== b(e); } return a; };
  const and = () => { let a = not(); while (OP[peek()] === 'and') { take(); const b = not(); const x = a; a = e => x(e) && b(e); } return a; };
  const not = () => { if (OP[peek()] === 'not') { take(); const a = not(); return e => !a(e); } return atom(); };
  const atom = () => {
    const t = take(); if (t === undefined) throw new Error('Unexpected end');
    if (t === '(') { const a = iff(); if (take() !== ')') throw new Error('Missing )'); return a; }
    if (t === 'T' || t === '1') return () => true; if (t === 'F' || t === '0') return () => false;
    if (/^[pqrsPQRS]$/.test(t)) { const v = t.toLowerCase(); return e => !!e[v]; }
    throw new Error('Unexpected ' + t);
  };
  const f = iff(); if (i < toks.length) throw new Error('Unexpected ' + toks[i]);
  const vars = [...new Set(toks.filter(t => /^[pqrsPQRS]$/.test(t)).map(t => t.toLowerCase()))].sort();
  return {f, vars};
};
LW.truthTable = function (src) {
  const {f, vars} = LW.parseBool(src); const rows = [];
  for (let m = (1 << vars.length) - 1; m >= 0; m--) { const env = {}; vars.forEach((v, k) => env[v] = !!(m >> (vars.length - 1 - k) & 1)); rows.push({env, val: f(env)}); }
  return {vars, rows};
};
// ---- matrices ----
LW.det = function (M) {
  const n = M.length; if (n === 1) return M[0][0]; if (n === 2) return M[0][0] * M[1][1] - M[0][1] * M[1][0];
  let d = 0; for (let j = 0; j < n; j++) d += (j % 2 ? -1 : 1) * M[0][j] * LW.det(M.slice(1).map(r => r.filter((_, k) => k !== j))); return d;
};
LW.rank = function (A) {
  const M = A.map(r => r.slice()), n = M.length, m = M[0].length; let rk = 0;
  for (let c = 0; c < m && rk < n; c++) {
    let p = rk; for (let i = rk + 1; i < n; i++) if (Math.abs(M[i][c]) > Math.abs(M[p][c])) p = i;
    if (Math.abs(M[p][c]) < 1e-9) continue; [M[rk], M[p]] = [M[p], M[rk]];
    for (let i = rk + 1; i < n; i++) { const f = M[i][c] / M[rk][c]; for (let j = c; j < m; j++) M[i][j] -= f * M[rk][j]; } rk++;
  } return rk;
};
LW.inv = function (M) {
  const n = M.length, d = LW.det(M); if (Math.abs(d) < 1e-12) return null;
  const A = M.map((r, i) => r.concat(Array.from({length: n}, (_, j) => +(i === j))));
  for (let c = 0; c < n; c++) {
    let p = c; for (let i = c + 1; i < n; i++) if (Math.abs(A[i][c]) > Math.abs(A[p][c])) p = i; [A[c], A[p]] = [A[p], A[c]];
    const pv = A[c][c]; for (let j = 0; j < 2 * n; j++) A[c][j] /= pv;
    for (let i = 0; i < n; i++) if (i !== c) { const f = A[i][c]; for (let j = 0; j < 2 * n; j++) A[i][j] -= f * A[c][j]; }
  } return A.map(r => r.slice(n));
};
LW.eig = function (M) {  // returns [[re,im],...]
  const n = M.length;
  const tr = M.reduce((s, r, i) => s + r[i], 0);
  if (n === 1) return [[M[0][0], 0]];
  if (n === 2) { const d = LW.det(M), disc = tr * tr - 4 * d; return disc >= 0 ? [[(tr + Math.sqrt(disc)) / 2, 0], [(tr - Math.sqrt(disc)) / 2, 0]] : [[tr / 2, Math.sqrt(-disc) / 2], [tr / 2, -Math.sqrt(-disc) / 2]]; }
  const c2 = M[0][0] * M[1][1] - M[0][1] * M[1][0] + M[0][0] * M[2][2] - M[0][2] * M[2][0] + M[1][1] * M[2][2] - M[1][2] * M[2][1];
  const co = [1, -tr, c2, -LW.det(M)];  // λ³ + aλ² + bλ + c
  const mul = (a, b) => [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]], sub = (a, b) => [a[0] - b[0], a[1] - b[1]];
  const div = (a, b) => { const d = b[0] * b[0] + b[1] * b[1]; return [(a[0] * b[0] + a[1] * b[1]) / d, (a[1] * b[0] - a[0] * b[1]) / d]; };
  const P = z => { let r = [1, 0]; r = [co[0], 0]; for (let k = 1; k < 4; k++) { r = mul(r, z); r = [r[0] + co[k], r[1]]; } return r; };
  let z = [[0.4, 0.9], [-0.65, 0.7], [-0.3, -0.8]].map(a => [a[0] * (1 + Math.abs(tr)), a[1] * (1 + Math.abs(tr))]);
  for (let it = 0; it < 500; it++) z = z.map((zi, i) => { let d = [1, 0]; z.forEach((zj, j) => { if (j !== i) d = mul(d, sub(zi, zj)); }); return sub(zi, div(P(zi), d)); });
  return z.map(a => [Math.abs(a[0]) < 1e-9 ? 0 : a[0], Math.abs(a[1]) < 1e-9 ? 0 : a[1]]).sort((a, b) => b[0] - a[0] || b[1] - a[1]);
};
// ---- number theory / groups / lattices ----
LW.gcd = (a, b) => b ? LW.gcd(b, a % b) : a;
LW.divisors = n => { const r = []; for (let d = 1; d <= n; d++) if (n % d === 0) r.push(d); return r; };
LW.omega = n => { let c = 0; for (let p = 2; n > 1; p++) while (n % p === 0) { n /= p; c++; } return c; };
LW.squarefree = n => { for (let p = 2; p * p <= n; p++) if (n % (p * p) === 0) return false; return true; };
LW.phi = n => { let c = 0; for (let k = 1; k <= n; k++) if (LW.gcd(k, n) === 1) c++; return c; };
LW.groupElems = (n, op) => op === '+' ? Array.from({length: n}, (_, i) => i) : Array.from({length: n - 1}, (_, i) => i + 1).filter(a => LW.gcd(a, n) === 1);
LW.groupOp = (n, op, a, b) => op === '+' ? (a + b) % n : (a * b) % n;
LW.cyclic = (n, op, a) => { const id = op === '+' ? 0 : 1; const s = [id]; let x = a; while (x !== id) { s.push(x); x = LW.groupOp(n, op, x, a); } return s; };
// ---- graphs ----
LW.graphInfo = function (edges) {
  const vs = [...new Set(edges.flat())].sort(), idx = Object.fromEntries(vs.map((v, i) => [v, i])), n = vs.length;
  const adj = vs.map(() => new Set()); edges.forEach(([a, b]) => { if (a !== b) { adj[idx[a]].add(idx[b]); adj[idx[b]].add(idx[a]); } });
  const m = adj.reduce((s, a) => s + a.size, 0) / 2, deg = adj.map(a => a.size);
  const comp = Array(n).fill(-1); let c = 0;
  for (let i = 0; i < n; i++) if (comp[i] < 0) { const st = [i]; comp[i] = c; while (st.length) { const u = st.pop(); adj[u].forEach(v => { if (comp[v] < 0) { comp[v] = c; st.push(v); } }); } c++; }
  const col = Array(n).fill(-1); let bip = true;
  for (let i = 0; i < n; i++) if (col[i] < 0) { col[i] = 0; const q = [i]; while (q.length) { const u = q.shift(); adj[u].forEach(v => { if (col[v] < 0) { col[v] = 1 - col[u]; q.push(v); } else if (col[v] === col[u]) bip = false; }); } }
  const odd = deg.filter(d => d % 2).length;
  let chi = null;
  if (n <= 8) { for (let k = 1; k <= n && chi === null; k++) { const a = Array(n).fill(0); const ok = i => { if (i === n) return true; for (let x = 0; x < k; x++) { if ([...adj[i]].every(v => v >= i || a[v] !== x)) { a[i] = x; if (ok(i + 1)) return true; } } return false; }; if (ok(0)) chi = k; } }
  return {vs, n, m, deg, comps: c, bip, odd, connected: c === 1, euler: c === 1 && odd === 0 ? 'circuit' : (c === 1 && odd === 2 ? 'path' : 'none'), tree: c === 1 && m === n - 1, chi, adj};
};
// ---- counting ----
LW.fact = n => { let r = 1n; for (let i = 2n; i <= BigInt(n); i++) r *= i; return r; };
LW.nPr = (n, k) => k > n ? 0n : LW.fact(n) / LW.fact(n - k);
LW.nCr = (n, k) => k > n || k < 0 ? 0n : LW.fact(n) / (LW.fact(k) * LW.fact(n - k));
LW.derange = n => { let a = 1n, b = 0n; if (n === 0) return 1n; for (let i = 2n; i <= BigInt(n); i++) { const t = (i - 1n) * (a + b); a = b; b = t; } return b; };

if (typeof document === 'undefined') return;

/* ======================= DOM helpers ======================= */
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const fmtN = x => { if (!isFinite(x)) return String(x); const r = Math.round(x * 10000) / 10000; return (Object.is(r, -0) ? 0 : r).toString(); };
const fmtC = z => Math.abs(z[1]) < 1e-9 ? fmtN(z[0]) : fmtN(z[0]) + (z[1] < 0 ? ' − ' : ' + ') + fmtN(Math.abs(z[1])) + 'i';
function toast(t) { const d = document.createElement('div'); d.textContent = t; ($('#toast') || document.body).appendChild(d); setTimeout(() => d.remove(), 3100); }
const post = (u, b) => fetch(u, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(b || {})}).then(r => r.json());

/* ======================= page behaviour ======================= */
$('#outlineBtn') && ($('#outlineBtn').onclick = () => { $('#outline').hidden = !$('#outline').hidden; });
const spy = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) $$('.toc a').forEach(a => a.classList.toggle('on', a.dataset.s === e.target.id)); }), {rootMargin: '-20% 0px -70% 0px'});
$$('.sec').forEach(s => spy.observe(s));
$$('.toc a').forEach(a => a.onclick = () => document.getElementById(a.dataset.s).scrollIntoView({behavior: 'smooth'}));

$$('.quick').forEach(card => {
  const a = +card.dataset.a;
  $$('.opt', card).forEach(b => b.onclick = () => {
    $$('.opt', card).forEach((x, i) => { x.classList.add('lock'); if (i === a) x.classList.add('right'); else if (x === b) x.classList.add('bad'); });
    const ok = +b.dataset.i === a, fb = $('.fb', card); fb.className = 'fb on ' + (ok ? 'ok' : 'no');
    fb.innerHTML = '<b>' + (ok ? '✓ Correct!' : '✗ Not quite') + '</b><div class="muted" style="margin-top:4px">' + esc(card.dataset.e) + '</div>';
  });
});
let nOK = 0, earned = 0; const nPrac = $$('.prac').length;
$$('.prac').forEach(card => {
  const type = card.dataset.type, sel = new Set(); let done = false;
  $$('.opt', card).forEach(b => b.onclick = () => {
    if (done) return; const i = +b.dataset.i;
    if (type === 'single') { sel.clear(); sel.add(i); $$('.opt', card).forEach(x => x.classList.toggle('sel', x === b)); }
    else { sel.has(i) ? sel.delete(i) : sel.add(i); b.classList.toggle('sel'); }
  });
  $('.chk', card).onclick = async () => {
    if (done) return;
    const body = {qid: card.dataset.id};
    if (type === 'numerical') { const v = $('.nat', card).value; if (v === '') { toast('Type your answer first'); return; } body.num = v; }
    else { if (!sel.size) { toast('Select an option first'); return; } body.sel = [...sel]; }
    const r = await post('/api/learn/check', body); if (r.error) { toast(r.error); return; }
    done = true; $('.chk', card).disabled = true;
    if (type !== 'numerical') $$('.opt', card).forEach((x, i) => { x.classList.add('lock'); x.classList.remove('sel'); const txt = x.children[1].textContent; if (r.answer.includes(txt)) x.classList.add('right'); else if (sel.has(i)) x.classList.add('bad'); });
    const ok = r.state === 'correct'; if (ok) { nOK++; earned += r.credit; }
    const fb = $('.fb', card); fb.className = 'fb on ' + (ok ? 'ok' : 'no');
    fb.innerHTML = (r.credit ? '<span class="cr">+' + r.credit + ' credits</span>' : '') + '<b>' + (ok ? '✓ Correct!' : '✗ Not quite — correct answer: ' + esc(r.correct)) + '</b>\n' + (r.expl ? esc(r.expl) : '<span class="muted">No written explanation for this question.</span>');
    $('#scoreChip').textContent = nOK + ' / ' + nPrac + ' correct'; $('#earned').textContent = earned;
    if (r.credit) toast('+' + r.credit + ' credits'); (r.events || []).forEach(e => toast('🎉 ' + (e.scope === 'ALL' ? 'Overall' : e.scope) + ' reached Level ' + e.to + '!'));
  };
});
const cb = $('#complete');
if (cb) cb.onclick = async () => {
  if (cb.dataset.done === '1') { toast('Already completed ✔'); return; }
  const r = await post('/api/learn/complete/' + cb.dataset.slug); cb.dataset.done = '1'; cb.textContent = '✔ Completed';
  if (r.credit) toast('Topic complete! +' + r.credit + ' credits'); (r.events || []).forEach(e => toast('🎉 ' + (e.scope === 'ALL' ? 'Overall' : e.scope) + ' reached Level ' + e.to + '!'));
};

/* ======================= widgets ======================= */
const W = {};
// ---------- truth table ----------
W.truth = el => {
  el.innerHTML = '<div class="row"><label>Formula</label><input type="text" id="tf" value="(p -> q) <-> (!p | q)" style="flex:1;min-width:240px"></div>' +
    '<div class="row" style="margin-top:8px"><label>Compare with</label><input type="text" id="tg" value="!q -> !p" style="flex:1;min-width:240px"></div>' +
    '<div class="small muted" style="margin-top:6px">Use p q r s · <code>!</code> not · <code>&amp;</code> and · <code>|</code> or · <code>^</code> xor · <code>-&gt;</code> implies · <code>&lt;-&gt;</code> iff · T / F</div>' +
    '<div class="row" style="margin-top:8px" id="ex"></div><div class="out" id="verdict"></div><div id="tbl"></div>';
  const EX = [['p -> q', 'Implication'], ['!(p & q)', "De Morgan"], ['(p -> q) & (q -> r) -> (p -> r)', 'Hypothetical syllogism'], ['p ^ q', 'XOR'], ['p | !p', 'Excluded middle'], ['p & !p', 'Contradiction']];
  $('#ex', el).innerHTML = EX.map(e => '<button class="btn sm" data-f="' + esc(e[0]) + '">' + e[1] + '</button>').join('');
  $$('#ex .btn', el).forEach(b => b.onclick = () => { $('#tf', el).value = b.dataset.f; run(); });
  function run() {
    try {
      const A = LW.truthTable($('#tf', el).value); let tbl = '<table class="tt"><tr>' + A.vars.map(v => '<th>' + v + '</th>').join('') + '<th>Result</th></tr>';
      A.rows.forEach(r => tbl += '<tr>' + A.vars.map(v => '<td class="' + (r.env[v] ? 'T' : 'F') + '">' + (r.env[v] ? 'T' : 'F') + '</td>').join('') + '<td class="' + (r.val ? 'T' : 'F') + '">' + (r.val ? 'T' : 'F') + '</td></tr>');
      $('#tbl', el).innerHTML = tbl + '</table>';
      const t = A.rows.filter(r => r.val).length, kind = t === A.rows.length ? 'Tautology (always true)' : t === 0 ? 'Contradiction (always false)' : 'Contingency (sometimes true)';
      let html = '<span class="pill ' + (t === A.rows.length ? 'y' : t === 0 ? 'n' : '') + '">' + kind + '</span><span class="pill">' + t + ' of ' + A.rows.length + ' rows true</span>';
      const g = $('#tg', el).value.trim(); if (g) { try { const vs = [...new Set(A.vars.concat(LW.parseBool(g).vars))], B = LW.parseBool(g), Aa = LW.parseBool($('#tf', el).value); let eq = true; for (let m = 0; m < (1 << vs.length); m++) { const env = {}; vs.forEach((v, k) => env[v] = !!(m >> (vs.length - 1 - k) & 1)); if (Aa.f(env) !== B.f(env)) eq = false; } html += '<span class="pill ' + (eq ? 'y' : 'n') + '">' + (eq ? '≡ equivalent to the second formula' : '≢ NOT equivalent to the second formula') + '</span>'; } catch (e) { html += '<span class="pill n">second formula: ' + esc(e.message) + '</span>'; } }
      $('#verdict', el).innerHTML = html;
    } catch (e) { $('#verdict', el).innerHTML = '<span class="pill n">' + esc(e.message) + '</span>'; $('#tbl', el).innerHTML = ''; }
  }
  $('#tf', el).oninput = run; $('#tg', el).oninput = run; run();
};
// ---------- relation properties ----------
W.relation = el => {
  const N = 4; let R = Array.from({length: N}, () => Array(N).fill(false));
  el.innerHTML = '<div class="row"><b>Click cells to build a relation R on {1,2,3,4}</b> <span class="muted small">(row = a, column = b means (a,b) ∈ R)</span></div><div class="row" id="pre" style="margin:8px 0"></div><div id="g"></div><div class="out" id="props"></div><div class="row" id="cl" style="margin-top:10px"></div>';
  const PRE = {'Equivalence (mod 2)': (a, b) => a % 2 === b % 2, 'Divisibility (a | b)': (a, b) => b % a === 0, 'Total order (≤)': (a, b) => a <= b, 'Strictly less (<)': (a, b) => a < b, 'Empty': () => false};
  $('#pre', el).innerHTML = Object.keys(PRE).map(k => '<button class="btn sm">' + k + '</button>').join('');
  $$('#pre .btn', el).forEach((b, i) => b.onclick = () => { const f = Object.values(PRE)[i]; R = R.map((r, a) => r.map((_, c) => f(a + 1, c + 1))); draw(); });
  $('#cl', el).innerHTML = ['Reflexive closure', 'Symmetric closure', 'Transitive closure'].map(t => '<button class="btn sm">' + t + '</button>').join('');
  const [bR, bS, bT] = $$('#cl .btn', el);
  bR.onclick = () => { for (let i = 0; i < N; i++) R[i][i] = true; draw(); };
  bS.onclick = () => { for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) if (R[i][j]) R[j][i] = true; draw(); };
  bT.onclick = () => { for (let k = 0; k < N; k++) for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) if (R[i][k] && R[k][j]) R[i][j] = true; draw(); };
  function draw() {
    let h = '<div class="cellgrid" style="grid-template-columns:repeat(' + (N + 1) + ',42px)"><span></span>' + [1, 2, 3, 4].map(x => '<span class="h">' + x + '</span>').join('');
    for (let i = 0; i < N; i++) { h += '<span class="h">' + (i + 1) + '</span>'; for (let j = 0; j < N; j++) h += '<button data-i="' + i + '" data-j="' + j + '" class="' + (R[i][j] ? 'on' : '') + '">' + (R[i][j] ? '1' : '') + '</button>'; }
    $('#g', el).innerHTML = h + '</div>'; $$('#g button', el).forEach(b => b.onclick = () => { R[+b.dataset.i][+b.dataset.j] = !R[+b.dataset.i][+b.dataset.j]; draw(); });
    const all = f => { for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) if (!f(i, j)) return false; return true; };
    const refl = all((i, j) => i !== j || R[i][i]), irr = all((i, j) => i !== j || !R[i][i]), sym = all((i, j) => !R[i][j] || R[j][i]), asym = all((i, j) => !(R[i][j] && R[j][i]) || i === j);
    let trans = true; for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) for (let k = 0; k < N; k++) if (R[i][j] && R[j][k] && !R[i][k]) trans = false;
    const P = [['Reflexive', refl], ['Irreflexive', irr], ['Symmetric', sym], ['Antisymmetric', asym], ['Transitive', trans], ['Equivalence relation', refl && sym && trans], ['Partial order', refl && asym && trans]];
    $('#props', el).innerHTML = P.map(p => '<span class="pill ' + (p[1] ? 'y' : 'n') + '">' + (p[1] ? '✔ ' : '✘ ') + p[0] + '</span>').join('') + '<span class="pill">|R| = ' + R.flat().filter(Boolean).length + '</span>';
  }
  draw();
};
// ---------- matrix ----------
W.matrix = el => {
  el.innerHTML = '<div class="row"><label>Size</label><select id="sz"><option value="2">2 × 2</option><option value="3" selected>3 × 3</option></select><button class="btn sm" id="rnd">Random integer matrix</button><button class="btn sm" id="sym">Symmetric example</button></div><div style="margin:12px 0" id="mx"></div><div class="out" id="mo"></div><div id="inv"></div>';
  let n = 3, M = [[2, 1, 0], [1, 3, 1], [0, 1, 2]];
  function build() {
    $('#mx', el).innerHTML = '<div class="mx" style="grid-template-columns:repeat(' + n + ',62px)">' + Array.from({length: n * n}, (_, k) => '<input type="number" step="any" data-i="' + Math.floor(k / n) + '" data-j="' + k % n + '" value="' + M[Math.floor(k / n)][k % n] + '">').join('') + '</div>';
    $$('#mx input', el).forEach(i => i.oninput = () => { M[+i.dataset.i][+i.dataset.j] = parseFloat(i.value) || 0; calc(); }); calc();
  }
  function calc() {
    const d = LW.det(M), tr = M.reduce((s, r, i) => s + r[i], 0), rk = LW.rank(M), ev = LW.eig(M), iv = LW.inv(M);
    $('#mo', el).innerHTML = '<span class="pill">det = <b>' + fmtN(d) + '</b></span><span class="pill">trace = <b>' + fmtN(tr) + '</b></span><span class="pill">rank = <b>' + rk + '</b></span><span class="pill ' + (Math.abs(d) < 1e-9 ? 'n' : 'y') + '">' + (Math.abs(d) < 1e-9 ? 'singular (not invertible)' : 'invertible') + '</span>' +
      '<span class="pill">eigenvalues: <b>' + ev.map(fmtC).join(', ') + '</b></span><span class="pill">Σλ = ' + fmtN(ev.reduce((s, z) => s + z[0], 0)) + ' (= trace)</span><span class="pill">Πλ = ' + fmtN(ev.reduce((p, z) => [p[0] * z[0] - p[1] * z[1], p[0] * z[1] + p[1] * z[0]], [1, 0])[0]) + ' (= det)</span><span class="pill">nullity = ' + (n - rk) + '</span>';
    $('#inv', el).innerHTML = iv ? '<div class="small muted" style="margin-top:10px">Inverse A⁻¹</div><table class="tt">' + iv.map(r => '<tr>' + r.map(x => '<td>' + fmtN(x) + '</td>').join('') + '</tr>').join('') + '</table>' : '';
  }
  $('#sz', el).onchange = () => { n = +$('#sz', el).value; M = Array.from({length: n}, (_, i) => Array.from({length: n}, (_, j) => i === j ? 2 : (Math.abs(i - j) === 1 ? 1 : 0))); build(); };
  $('#rnd', el).onclick = () => { M = Array.from({length: n}, () => Array.from({length: n}, () => Math.floor(Math.random() * 9) - 3)); build(); };
  $('#sym', el).onclick = () => { M = Array.from({length: n}, () => Array(n).fill(0)); for (let i = 0; i < n; i++) for (let j = i; j < n; j++) M[i][j] = M[j][i] = Math.floor(Math.random() * 7) - 2; build(); };
  build();
};
// ---------- probability simulator ----------
W.prob = el => {
  el.innerHTML = '<div class="row"><label>Experiment</label><select id="ex"><option value="coin">Coin: P(heads)</option><option value="dice7">Two dice: P(sum = 7)</option><option value="six4">P(at least one six in 4 rolls)</option><option value="bday">Birthday: P(two share a birthday)</option><option value="monty">Monty Hall: P(win if you switch)</option></select>' +
    '<span id="bw" style="display:none" class="row"><label>People</label><input type="range" id="bn" min="2" max="60" value="23"><b id="bv">23</b></span><label>Trials</label><select id="nt"><option>100</option><option selected>1000</option><option>10000</option></select><button class="btn pri sm" id="go">▶ Run</button></div><div class="out" id="res"></div><canvas class="cv" id="cv" width="640" height="300"></canvas>';
  const E = {
    coin: [() => Math.random() < .5, () => .5], dice7: [() => Math.floor(Math.random() * 6) + Math.floor(Math.random() * 6) + 2 === 7, () => 1 / 6],
    six4: [() => { for (let i = 0; i < 4; i++) if (Math.random() < 1 / 6) return true; return false; }, () => 1 - Math.pow(5 / 6, 4)],
    bday: [() => { const n = +$('#bn', el).value, s = new Set(); for (let i = 0; i < n; i++) { const d = Math.floor(Math.random() * 365); if (s.has(d)) return true; s.add(d); } return false; }, () => { const n = +$('#bn', el).value; let p = 1; for (let i = 0; i < n; i++) p *= (365 - i) / 365; return 1 - p; }],
    monty: [() => { const car = Math.floor(Math.random() * 3), pick = Math.floor(Math.random() * 3); return pick !== car; }, () => 2 / 3]};
  $('#ex', el).onchange = () => { $('#bw', el).style.display = $('#ex', el).value === 'bday' ? 'flex' : 'none'; };
  $('#bn', el).oninput = () => { $('#bv', el).textContent = $('#bn', el).value; };
  $('#go', el).onclick = () => {
    const [t, th] = E[$('#ex', el).value], n = +$('#nt', el).value, p = th(), pts = []; let h = 0;
    for (let i = 1; i <= n; i++) { if (t()) h++; if (i % Math.max(1, Math.floor(n / 120)) === 0 || i === n) pts.push([i, h / i]); }
    const est = h / n; $('#res', el).innerHTML = '<span class="pill">Simulated: <b>' + est.toFixed(4) + '</b></span><span class="pill y">Exact: <b>' + p.toFixed(4) + '</b></span><span class="pill">Error: ' + Math.abs(est - p).toFixed(4) + '</span>';
    const c = $('#cv', el), g = c.getContext('2d'), w = c.width, hh = c.height; g.clearRect(0, 0, w, hh);
    const css = getComputedStyle(document.documentElement), line = css.getPropertyValue('--acc').trim() || '#22d3ee', ok = css.getPropertyValue('--ok').trim() || '#34d399', mut = css.getPropertyValue('--mut').trim() || '#888';
    const Y = v => hh - 24 - v * (hh - 40), X = i => 30 + i / n * (w - 50);
    g.strokeStyle = mut; g.globalAlpha = .4; g.beginPath(); g.moveTo(30, 10); g.lineTo(30, hh - 24); g.lineTo(w - 10, hh - 24); g.stroke(); g.globalAlpha = 1;
    g.setLineDash([6, 5]); g.strokeStyle = ok; g.beginPath(); g.moveTo(30, Y(p)); g.lineTo(w - 10, Y(p)); g.stroke(); g.setLineDash([]);
    g.strokeStyle = line; g.lineWidth = 2; g.beginPath(); pts.forEach((q, k) => k ? g.lineTo(X(q[0]), Y(q[1])) : g.moveTo(X(q[0]), Y(q[1]))); g.stroke();
    g.fillStyle = mut; g.font = '12px Segoe UI'; g.fillText('running estimate vs exact (dashed) — more trials, closer to the truth', 36, 18);
  };
  $('#go', el).click();
};
// ---------- function plotter ----------
W.func = el => {
  const F = {'x²': [x => x * x], 'x³ − 3x': [x => x ** 3 - 3 * x], 'sin x': [Math.sin], 'eˣ': [Math.exp], 'ln x': [x => x > 0 ? Math.log(x) : NaN], '1/x': [x => x ? 1 / x : NaN], '|x|': [Math.abs], 'sin(x)/x': [x => x ? Math.sin(x) / x : NaN], '(x²−1)/(x−1)': [x => x === 1 ? NaN : (x * x - 1) / (x - 1)]};
  el.innerHTML = '<div class="row"><label>f(x)</label><select id="fn">' + Object.keys(F).map(k => '<option>' + k + '</option>').join('') + '</select><label>Mode</label><select id="md"><option value="tan">Tangent &amp; slope</option><option value="area">Area under curve</option></select></div>' +
    '<div class="row" style="margin-top:8px"><label id="l1">x₀</label><input type="range" id="x0" min="-5" max="5" step="0.05" value="1"><b id="xv">1.00</b><span id="ab" style="display:none" class="row"><label>from</label><input type="number" id="a" value="0" step="0.5" style="width:80px"><label>to</label><input type="number" id="b" value="2" step="0.5" style="width:80px"></span></div>' +
    '<canvas class="cv" id="cv" width="640" height="300" style="margin-top:10px"></canvas><div class="out" id="fo"></div><div id="lim"></div>';
  function draw() {
    const f = F[$('#fn', el).value][0], mode = $('#md', el).value, x0 = +$('#x0', el).value; $('#xv', el).textContent = x0.toFixed(2);
    $('#ab', el).style.display = mode === 'area' ? 'flex' : 'none'; $('#x0', el).style.display = mode === 'area' ? 'none' : ''; $('#xv', el).style.display = mode === 'area' ? 'none' : ''; $('#l1', el).textContent = mode === 'area' ? 'Limits' : 'x₀';
    const c = $('#cv', el), g = c.getContext('2d'), w = c.width, h = c.height; g.clearRect(0, 0, w, h);
    const css = getComputedStyle(document.documentElement), acc = css.getPropertyValue('--acc').trim() || '#22d3ee', c2 = css.getPropertyValue('--acc2').trim() || '#38bdf8', mut = css.getPropertyValue('--mut').trim() || '#888';
    const xs = []; for (let i = 0; i <= 400; i++) xs.push(-5 + i * 10 / 400); let ys = xs.map(f).filter(isFinite).map(v => Math.max(-8, Math.min(8, v)));
    const lo = Math.min(-1, ...ys), hi = Math.max(1, ...ys), X = x => (x + 5) / 10 * (w - 20) + 10, Y = y => h - 10 - (y - lo) / (hi - lo) * (h - 20);
    g.strokeStyle = mut; g.globalAlpha = .45; g.beginPath(); g.moveTo(10, Y(0)); g.lineTo(w - 10, Y(0)); g.moveTo(X(0), 5); g.lineTo(X(0), h - 5); g.stroke(); g.globalAlpha = 1;
    if (mode === 'area') {
      let a = parseFloat($('#a', el).value) || 0, b = parseFloat($('#b', el).value) || 0; if (a > b) [a, b] = [b, a]; let s = 0; const N = 2000, dx = (b - a) / N;
      g.fillStyle = c2; g.globalAlpha = .3; g.beginPath(); g.moveTo(X(a), Y(0)); for (let i = 0; i <= N; i += 10) { const x = a + i * dx, y = f(x); g.lineTo(X(x), Y(isFinite(y) ? Math.max(lo, Math.min(hi, y)) : 0)); } g.lineTo(X(b), Y(0)); g.fill(); g.globalAlpha = 1;
      for (let i = 0; i < N; i++) { const y = f(a + (i + .5) * dx); if (isFinite(y)) s += y * dx; }
      $('#fo', el).innerHTML = '<span class="pill y">∫ from ' + a + ' to ' + b + ' = <b>' + fmtN(s) + '</b> (numerical)</span><span class="pill">Shaded area counts below the x-axis as negative</span>'; $('#lim', el).innerHTML = '';
    }
    g.strokeStyle = acc; g.lineWidth = 2.4; g.beginPath(); let pen = false; xs.forEach(x => { const y = f(x); if (!isFinite(y) || Math.abs(y) > 50) { pen = false; return; } const yy = Math.max(lo - 1, Math.min(hi + 1, y)); pen ? g.lineTo(X(x), Y(yy)) : g.moveTo(X(x), Y(yy)); pen = true; }); g.stroke();
    if (mode === 'tan') {
      const y0 = f(x0), hh = 1e-5, d = (f(x0 + hh) - f(x0 - hh)) / (2 * hh);
      if (isFinite(y0) && isFinite(d)) {
        g.strokeStyle = c2; g.lineWidth = 2; g.beginPath(); g.moveTo(X(-5), Y(y0 + d * (-5 - x0))); g.lineTo(X(5), Y(y0 + d * (5 - x0))); g.stroke(); g.fillStyle = c2; g.beginPath(); g.arc(X(x0), Y(y0), 6, 0, 7); g.fill();
        $('#fo', el).innerHTML = '<span class="pill">f(x₀) = <b>' + fmtN(y0) + '</b></span><span class="pill y">f′(x₀) = slope = <b>' + fmtN(d) + '</b></span><span class="pill">' + (Math.abs(d) < 0.02 ? 'slope ≈ 0 → possible maximum / minimum / inflection' : d > 0 ? 'increasing here' : 'decreasing here') + '</span>';
      } else $('#fo', el).innerHTML = '<span class="pill n">f is undefined or not differentiable at x₀ = ' + x0.toFixed(2) + '</span>';
      const A = Math.round(x0), rows = [-0.1, -0.01, -0.001, 0.001, 0.01, 0.1].map(d => { const v = f(A + d); return '<tr><td>' + fmtN(A + d) + '</td><td>' + (isFinite(v) ? fmtN(v) : 'undefined') + '</td></tr>'; }).join('');
      $('#lim', el).innerHTML = '<div class="small muted" style="margin-top:10px">Limit view: values of f(x) as x → <b>' + A + '</b> from both sides (x₀ rounded)</div><table class="tt"><tr><th>x</th><th>f(x)</th></tr>' + rows + '</table>';
    }
  }
  ['fn', 'md', 'x0', 'a', 'b'].forEach(i => $('#' + i, el).oninput = draw); $('#fn', el).onchange = draw; $('#md', el).onchange = draw; draw();
};
// ---------- graph explorer ----------
W.graph = el => {
  el.innerHTML = '<label>Edges (e.g. <code>A-B, B-C, C-A</code>)</label><textarea id="ed" rows="2">A-B, B-C, C-D, D-A, A-C</textarea><div class="row" style="margin:8px 0" id="pre"></div><svg class="gsvg" id="sv" viewBox="0 0 560 300"></svg><div class="out" id="gi"></div>';
  const PRE = {'Square + diagonal': 'A-B, B-C, C-D, D-A, A-C', 'Triangle (K3)': 'A-B, B-C, C-A', 'K4': 'A-B,A-C,A-D,B-C,B-D,C-D', 'Path': 'A-B, B-C, C-D', 'Cycle C5': 'A-B,B-C,C-D,D-E,E-A', 'K3,3': 'A-D,A-E,A-F,B-D,B-E,B-F,C-D,C-E,C-F', 'Star': 'O-A,O-B,O-C,O-D'};
  $('#pre', el).innerHTML = Object.keys(PRE).map(k => '<button class="btn sm">' + k + '</button>').join(''); $$('#pre .btn', el).forEach((b, i) => b.onclick = () => { $('#ed', el).value = Object.values(PRE)[i]; run(); });
  function run() {
    const edges = $('#ed', el).value.split(/[,;\n]+/).map(s => s.trim().split(/\s*-\s*/)).filter(a => a.length === 2 && a[0] && a[1]);
    if (!edges.length) { $('#gi', el).innerHTML = '<span class="pill n">Enter at least one edge like A-B</span>'; return; }
    const g = LW.graphInfo(edges), R = 105, pos = g.vs.map((_, i) => [280 + R * 1.5 * Math.cos(2 * Math.PI * i / g.n - Math.PI / 2), 150 + R * 1.2 * Math.sin(2 * Math.PI * i / g.n - Math.PI / 2)]);
    let s = ''; const seen = new Set(); edges.forEach(([a, b]) => { const k = [a, b].sort().join('|'); if (a === b || seen.has(k)) return; seen.add(k); const p = pos[g.vs.indexOf(a)], q = pos[g.vs.indexOf(b)]; s += '<line x1="' + p[0] + '" y1="' + p[1] + '" x2="' + q[0] + '" y2="' + q[1] + '" stroke="var(--line2)" stroke-width="2.5"/>'; });
    g.vs.forEach((v, i) => s += '<circle cx="' + pos[i][0] + '" cy="' + pos[i][1] + '" r="20" fill="var(--acc)"/><text x="' + pos[i][0] + '" y="' + (pos[i][1] + 5) + '" text-anchor="middle" fill="#fff" font-weight="800" font-size="15">' + esc(v) + '</text><text x="' + pos[i][0] + '" y="' + (pos[i][1] - 26) + '" text-anchor="middle" fill="var(--mut)" font-size="12">deg ' + g.deg[i] + '</text>');
    $('#sv', el).innerHTML = s;
    const Y = (t, ok) => '<span class="pill ' + (ok ? 'y' : 'n') + '">' + (ok ? '✔ ' : '✘ ') + t + '</span>';
    $('#gi', el).innerHTML = '<span class="pill">V = <b>' + g.n + '</b></span><span class="pill">E = <b>' + g.m + '</b></span><span class="pill">Σdeg = ' + g.deg.reduce((a, b) => a + b, 0) + ' = 2E</span><span class="pill">components: <b>' + g.comps + '</b></span>' + Y('Connected', g.connected) + Y('Tree', g.tree) + Y('Bipartite', g.bip) +
      '<span class="pill ' + (g.euler !== 'none' ? 'y' : 'n') + '">Euler: <b>' + (g.euler === 'circuit' ? 'circuit exists (all degrees even)' : g.euler === 'path' ? 'path only (2 odd vertices)' : 'none (' + g.odd + ' odd vertices)') + '</b></span>' + '<span class="pill">chromatic number χ = <b>' + (g.chi === null ? '(too large)' : g.chi) + '</b></span>' + (g.n >= 3 ? '<span class="pill ' + (g.m <= 3 * g.n - 6 ? 'y' : 'n') + '">planar bound E ≤ 3V − 6 : ' + g.m + ' ≤ ' + (3 * g.n - 6) + '</span>' : '');
  }
  $('#ed', el).oninput = run; run();
};
// ---------- counting calculator ----------
W.counting = el => {
  el.innerHTML = '<div class="row"><label>n</label><input type="number" id="n" min="0" max="20" value="6" style="width:80px"><label>k</label><input type="number" id="k" min="0" max="20" value="3" style="width:80px"></div><div class="out" id="co"></div><div class="small muted" style="margin-top:12px">Pascal\'s triangle — highlighted: C(n, k) (for n ≤ 10)</div><div class="pas" id="pas"></div>';
  function run() {
    const n = Math.max(0, Math.min(20, +$('#n', el).value | 0)), k = Math.max(0, Math.min(20, +$('#k', el).value | 0));
    const row = (t, v, ex) => '<span class="pill" title="' + ex + '">' + t + ' = <b>' + v + '</b></span>';
    $('#co', el).innerHTML = row('n!', LW.fact(n), 'arrangements of n distinct objects') + row('P(n,k)', LW.nPr(n, k), 'ordered selections n!/(n−k)!') + row('C(n,k)', LW.nCr(n, k), 'unordered selections') + row('k identical → n boxes', LW.nCr(n + k - 1, k), 'stars & bars: C(n+k−1,k)') + row('Derangements D(n)', LW.derange(n), 'no object in its own place') + row('Catalan C(n)', LW.nCr(2 * n, n) / BigInt(n + 1), 'binary trees / balanced brackets');
    let h = ''; for (let r = 0; r <= 10; r++) { h += '<div>' + Array.from({length: r + 1}, (_, c) => '<span class="' + (r === n && c === k ? 'hi' : '') + '">' + LW.nCr(r, c) + '</span>').join('') + '</div>'; } $('#pas', el).innerHTML = h;
  }
  $('#n', el).oninput = run; $('#k', el).oninput = run; run();
};
// ---------- Hasse diagram of divisor lattice ----------
W.hasse = el => {
  el.innerHTML = '<div class="row"><label>n (the lattice D<sub>n</sub> of divisors of n)</label><input type="number" id="n" min="2" max="210" value="30" style="width:90px"><span class="muted small">click two elements to see their join (lcm) and meet (gcd)</span></div><svg class="gsvg" id="sv" viewBox="0 0 560 300" style="margin-top:10px"></svg><div class="out" id="hi"></div>';
  let sel = [];
  function run() {
    const n = Math.max(2, Math.min(210, +$('#n', el).value | 0)), ds = LW.divisors(n), lv = {}; ds.forEach(d => (lv[LW.omega(d)] = lv[LW.omega(d)] || []).push(d));
    const L = Math.max(...Object.keys(lv).map(Number)), pos = {}; Object.entries(lv).forEach(([l, a]) => a.forEach((d, i) => pos[d] = [280 + (i - (a.length - 1) / 2) * 70, 270 - l * (230 / Math.max(1, L))]));
    let s = ''; ds.forEach(a => ds.forEach(b => { if (b > a && b % a === 0 && LW.omega(b) === LW.omega(a) + 1) s += '<line x1="' + pos[a][0] + '" y1="' + pos[a][1] + '" x2="' + pos[b][0] + '" y2="' + pos[b][1] + '" stroke="var(--line2)" stroke-width="2"/>'; }));
    ds.forEach(d => s += '<g class="nd" data-d="' + d + '" style="cursor:pointer"><circle cx="' + pos[d][0] + '" cy="' + pos[d][1] + '" r="18" fill="' + (sel.includes(d) ? 'var(--acc2)' : 'var(--acc)') + '"/><text x="' + pos[d][0] + '" y="' + (pos[d][1] + 5) + '" text-anchor="middle" fill="#fff" font-weight="800" font-size="13">' + d + '</text></g>');
    $('#sv', el).innerHTML = s; $$('.nd', el).forEach(g => g.onclick = () => { const d = +g.dataset.d; sel = sel.includes(d) ? sel.filter(x => x !== d) : sel.concat(d).slice(-2); run(); });
    let info = '<span class="pill">|D' + n + '| = <b>' + ds.length + '</b> elements</span><span class="pill ' + (LW.squarefree(n) ? 'y' : 'n') + '">' + (LW.squarefree(n) ? '✔ square-free ⇒ a Boolean algebra' : '✘ not square-free ⇒ not Boolean') + '</span>';
    const comp = ds.filter(a => ds.some(b => LW.gcd(a, b) === 1 && a * b === n)).length; info += '<span class="pill">elements with a complement: <b>' + comp + '</b> of ' + ds.length + '</span>';
    if (sel.length === 2) { const [a, b] = sel; info += '<span class="pill y">join ' + a + ' ∨ ' + b + ' = lcm = <b>' + a * b / LW.gcd(a, b) + '</b></span><span class="pill y">meet ' + a + ' ∧ ' + b + ' = gcd = <b>' + LW.gcd(a, b) + '</b></span>'; }
    $('#hi', el).innerHTML = info;
  }
  $('#n', el).oninput = () => { sel = []; run(); }; run();
};
// ---------- group explorer ----------
W.group = el => {
  el.innerHTML = '<div class="row"><label>Group</label><select id="op"><option value="+">(Zₙ, +) addition mod n</option><option value="*">(Zₙ*, ×) units mod n</option></select><label>n</label><input type="number" id="n" min="2" max="24" value="8" style="width:80px"><label>element a</label><select id="a"></select></div><div class="out" id="gi"></div><div style="overflow-x:auto;margin-top:10px"><table class="ct" id="ct"></table></div>';
  function run() {
    const op = $('#op', el).value, n = Math.max(2, Math.min(24, +$('#n', el).value | 0)), E = LW.groupElems(n, op), id = op === '+' ? 0 : 1;
    const asel = $('#a', el); const keep = asel.value === '' ? NaN : +asel.value; asel.innerHTML = E.map(x => '<option>' + x + '</option>').join(''); asel.value = E.includes(keep) ? keep : E[1] !== undefined ? E[1] : E[0];
    const a = +asel.value, H = LW.cyclic(n, op, a), gens = E.filter(x => LW.cyclic(n, op, x).length === E.length);
    $('#gi', el).innerHTML = '<span class="pill">|G| = <b>' + E.length + '</b></span><span class="pill y">order of ' + a + ' = <b>' + H.length + '</b></span><span class="pill">⟨' + a + '⟩ = {' + H.join(', ') + '}</span><span class="pill ' + (gens.length ? 'y' : 'n') + '">' + (gens.length ? 'cyclic — generators: ' + gens.join(', ') : 'not cyclic') + '</span><span class="pill ' + (E.length % H.length === 0 ? 'y' : 'n') + '">Lagrange: ' + H.length + ' divides ' + E.length + ' ✔</span>';
    $('#ct', el).innerHTML = '<tr><th>' + (op === '+' ? '+' : '×') + '</th>' + E.map(x => '<th>' + x + '</th>').join('') + '</tr>' + E.map(r => '<tr><th>' + r + '</th>' + E.map(c => { const v = LW.groupOp(n, op, r, c); return '<td class="' + (v === id ? 'id' : H.includes(v) && (r === a || c === a) ? 'hi' : '') + '">' + v + '</td>'; }).join('') + '</tr>').join('');
  }
  ['op', 'n'].forEach(i => $('#' + i, el).oninput = run); $('#a', el).onchange = run; run();
};
// ---------- Venn / inclusion–exclusion ----------
W.venn = el => {
  const D = {a: 40, b: 35, c: 30, ab: 12, bc: 10, ac: 8, abc: 5};
  el.innerHTML = '<div class="row">' + Object.keys(D).map(k => '<label>|' + k.toUpperCase().split('').join('∩') + '|</label><input type="number" min="0" data-k="' + k + '" value="' + D[k] + '" style="width:70px">').join('') + '</div><svg class="gsvg" id="sv" viewBox="0 0 560 300" style="margin-top:10px"></svg><div class="out" id="vo"></div>';
  function run() {
    $$('input', el).forEach(i => D[i.dataset.k] = Math.max(0, parseInt(i.value) || 0)); const {a, b, c, ab, bc, ac, abc} = D;
    const R = {A: a - ab - ac + abc, B: b - ab - bc + abc, C: c - ac - bc + abc, AB: ab - abc, BC: bc - abc, AC: ac - abc, ABC: abc}, bad = Object.values(R).some(v => v < 0), U = a + b + c - ab - bc - ac + abc;
    const t = (x, y, v) => '<text x="' + x + '" y="' + y + '" text-anchor="middle" fill="var(--txt)" font-weight="800" font-size="17">' + v + '</text>';
    $('#sv', el).innerHTML = '<circle cx="225" cy="130" r="95" fill="#22d3ee" fill-opacity=".35" stroke="#22d3ee" stroke-width="2"/><circle cx="335" cy="130" r="95" fill="#38bdf8" fill-opacity=".35" stroke="#38bdf8" stroke-width="2"/><circle cx="280" cy="215" r="95" fill="#34d399" fill-opacity=".35" stroke="#34d399" stroke-width="2"/>' +
      t(180, 105, R.A) + t(380, 105, R.B) + t(280, 265, R.C) + t(280, 100, R.AB) + t(235, 190, R.AC) + t(325, 190, R.BC) + t(280, 158, R.ABC) + '<text x="150" y="60" fill="var(--mut)" font-weight="700">A</text><text x="410" y="60" fill="var(--mut)" font-weight="700">B</text><text x="280" y="296" fill="var(--mut)" font-weight="700" text-anchor="middle">C</text>';
    $('#vo', el).innerHTML = bad ? '<span class="pill n">These numbers are inconsistent (a region would be negative)</span>' : '<span class="pill y">|A ∪ B ∪ C| = <b>' + U + '</b></span><span class="pill">= ' + a + ' + ' + b + ' + ' + c + ' − ' + ab + ' − ' + bc + ' − ' + ac + ' + ' + abc + '</span><span class="pill">exactly one set: ' + (R.A + R.B + R.C) + '</span><span class="pill">exactly two: ' + (R.AB + R.BC + R.AC) + '</span>';
  }
  $$('input', el).forEach(i => i.oninput = run); run();
};
G.LW_W = W;
setTimeout(() => $$('.wgt').forEach(el => { if (el.dataset.done) return; const f = (G.LW_W || W)[el.dataset.w]; if (f) { try { f(el); } catch (e) { el.innerHTML = '<div class="pill n">Tool failed to load: ' + esc(e.message) + '</div>'; console.error(e); } } }), 0);
})();
