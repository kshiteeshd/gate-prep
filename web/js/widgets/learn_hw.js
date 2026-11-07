/* GATE Prep — learning modules: computer organisation and digital logic tools (IEEE 754, cache, pipeline, Quine–McCluskey, number systems) */
(function () {
const G = typeof window !== 'undefined' ? window : globalThis;
const LW = G.LW = G.LW || {};

/* ======================= pure logic (unit-tested with node) ======================= */
// ---- IEEE 754 ----
LW.ieeeEncode = (x, bits) => { bits = bits || 32; const dv = new DataView(new ArrayBuffer(8)); if (bits === 32) { dv.setFloat32(0, x); let s = ''; for (let i = 0; i < 4; i++) s += dv.getUint8(i).toString(2).padStart(8, '0'); return s; } dv.setFloat64(0, x); let s = ''; for (let i = 0; i < 8; i++) s += dv.getUint8(i).toString(2).padStart(8, '0'); return s; };
LW.ieeeDecode = (s, bits) => { bits = bits || s.length; const eb = bits === 32 ? 8 : 11, sign = s[0], e = s.slice(1, 1 + eb), f = s.slice(1 + eb), bias = (1 << (eb - 1)) - 1, ev = parseInt(e, 2); let kind, value;
  if (ev === 0) { kind = /^0*$/.test(f) ? 'zero' : 'denormal'; value = (sign === '1' ? -1 : 1) * (parseInt(f || '0', 2) / Math.pow(2, f.length)) * Math.pow(2, 1 - bias); }
  else if (ev === (1 << eb) - 1) { kind = /^0*$/.test(f) ? 'infinity' : 'NaN'; value = kind === 'NaN' ? NaN : (sign === '1' ? -Infinity : Infinity); }
  else { kind = 'normal'; value = (sign === '1' ? -1 : 1) * (1 + parseInt(f, 2) / Math.pow(2, f.length)) * Math.pow(2, ev - bias); }
  return {sign, exp: e, frac: f, bias, expValue: ev, kind, value}; };
// ---- number systems ----
LW.toBase = (n, b) => (n < 0 ? '-' : '') + Math.abs(n).toString(b).toUpperCase();
LW.fromBase = (s, b) => parseInt(s, b);
LW.twos = (n, bits) => { const m = Math.pow(2, bits); return ((n % m + m) % m).toString(2).padStart(bits, '0'); };
LW.fromTwos = (s) => { const n = s.length, v = parseInt(s, 2); return s[0] === '1' ? v - Math.pow(2, n) : v; };
LW.addSigned = (a, b, bits) => { const m = Math.pow(2, bits), ua = ((a % m) + m) % m, ub = ((b % m) + m) % m, raw = ua + ub, carry = raw >= m ? 1 : 0, res = raw % m, sa = ua >> (bits - 1) & 1, sb = ub >> (bits - 1) & 1, sr = res >> (bits - 1) & 1;
  return {sum: res.toString(2).padStart(bits, '0'), value: LW.fromTwos(res.toString(2).padStart(bits, '0')), carry, overflow: sa === sb && sr !== sa ? 1 : 0}; };
// ---- Quine–McCluskey with exact minimum cover ----
LW.qm = (n, on, dc) => {
  dc = dc || []; const bits = m => m.toString(2).padStart(n, '0'); let cur = new Set([...on, ...dc].map(bits)); const primes = new Set();
  while (cur.size) { const nxt = new Set(), used = new Set(), arr = [...cur];
    for (let i = 0; i < arr.length; i++) for (let j = i + 1; j < arr.length; j++) { let d = -1, ok = true; for (let k = 0; k < n; k++) if (arr[i][k] !== arr[j][k]) { if (d >= 0) { ok = false; break; } d = k; } if (ok && d >= 0) { nxt.add(arr[i].slice(0, d) + '-' + arr[i].slice(d + 1)); used.add(arr[i]); used.add(arr[j]); } }
    arr.forEach(t => { if (!used.has(t)) primes.add(t); }); cur = nxt; }
  const P = [...primes].sort(), covers = (p, m) => { const b = bits(m); for (let k = 0; k < n; k++) if (p[k] !== '-' && p[k] !== b[k]) return false; return true; };
  const lits = p => p.replace(/-/g, '').length; let need = on.slice(); if (!need.length) return {primes: P, cover: [], terms: 0, literals: 0};
  // exact minimum cover: iterate over sizes, then minimise literals
  let best = null; const cov = P.map(p => need.filter(m => covers(p, m)));
  const search = (k, start, chosen, covered) => { if (best && chosen.length > best.k) return; if (covered.size === need.length) { const L = chosen.reduce((s, i) => s + lits(P[i]), 0); if (!best || chosen.length < best.k || (chosen.length === best.k && L < best.L)) best = {k: chosen.length, L, sel: chosen.slice()}; return; } if (chosen.length >= k) return;
    for (let i = start; i < P.length; i++) { const nc = new Set(covered); cov[i].forEach(m => nc.add(m)); if (nc.size === covered.size) continue; chosen.push(i); search(k, i + 1, chosen, nc); chosen.pop(); } };
  for (let k = 1; k <= P.length && !best; k++) search(k, 0, [], new Set());
  // keep searching only within the minimal size for min literals
  return {primes: P, cover: best.sel.map(i => P[i]), terms: best.k, literals: best.L};
};
LW.sopString = (cover, names) => { names = names || 'ABCDEFGH'; if (!cover.length) return '0'; return cover.map(p => { const s = [...p].map((c, i) => c === '-' ? '' : names[i] + (c === '0' ? '′' : '')).join(''); return s || '1'; }).join(' + '); };
// ---- cache simulator ----
LW.cacheSim = (addrs, cfg) => {
  const sets = Math.max(1, Math.floor(cfg.size / (cfg.block * cfg.assoc))), S = Array.from({length: sets}, () => []), seq = []; let hits = 0;
  addrs.forEach(a => { const blk = Math.floor(a / cfg.block), set = blk % sets, tag = Math.floor(blk / sets), line = S[set], i = line.indexOf(tag);
    if (i >= 0) { hits++; if (cfg.policy === 'lru') { line.splice(i, 1); line.push(tag); } seq.push({addr: a, hit: true, set}); }
    else { if (line.length === cfg.assoc) line.shift(); line.push(tag); seq.push({addr: a, hit: false, set}); } });
  return {hits, misses: addrs.length - hits, sets, seq};
};
// ---- 5-stage pipeline (IF ID EX MEM WB) ----
// instr: {op, dst, src:[...]} ; opts: {forwarding, branchPenalty}
LW.parseInstr = line => { const t = line.trim().replace(/,/g, ' ').split(/\s+/).filter(Boolean); if (!t.length) return null; const op = t[0].toUpperCase(), r = (t.slice(1).join(' ').match(/[Rr]\d+/g) || []).map(x => x.toUpperCase());
  if (op === 'LW' || op === 'LD') return {op, dst: r[0], src: r.slice(1), load: true, text: line.trim()}; if (op === 'SW' || op === 'SD') return {op, dst: null, src: r, text: line.trim()}; if (op === 'BEQ' || op === 'BNE') return {op, dst: null, src: r, branch: true, text: line.trim()}; return {op, dst: r[0], src: r.slice(1), text: line.trim()}; };
LW.pipeline = (ins, opts) => {
  const fwd = !!opts.forwarding, bp = opts.branchPenalty || 0, id = [], res = []; let prev = 1; // IF of first instruction at cycle 1, ID at 2
  ins.forEach((x, i) => { let t = i === 0 ? 2 : id[i - 1] + 1; if (i > 0 && ins[i - 1].branch) t += bp;
    new Set(x.src).forEach(s => { for (let j = i - 1; j >= 0; j--) { const w = ins[j]; if (w.dst === s) { const need = fwd ? (w.load ? id[j] + 2 : id[j] + 1) : id[j] + 3; t = Math.max(t, need); break; } } });
    id.push(t); res.push({id: t, stalls: t - (i === 0 ? 2 : id[i - 1] + 1) - (i > 0 && ins[i - 1].branch ? bp : 0)}); });
  const total = ins.length ? id[ins.length - 1] + 3 : 0; return {id, total, stalls: res.map(r => r.stalls), totalStalls: res.reduce((s, r) => s + Math.max(0, r.stalls), 0)};
};

if (typeof document === 'undefined') return;

/* ======================= widgets ======================= */
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const W = G.LW_W = G.LW_W || {};
const pill = (t, c) => '<span class="pill ' + (c || '') + '">' + t + '</span>';
const NAMES = ['ieee', 'numsys', 'kmap', 'cache', 'pipeline'];

W.ieee = el => {
  el.innerHTML = '<div class="row"><label>Format</label><select id="f"><option value="32">single (32-bit)</option><option value="64">double (64-bit)</option></select><label>Decimal value</label><input type="text" id="x" value="-5.75" style="width:150px"><label>or bits</label><input type="text" id="b" style="flex:1;min-width:220px" placeholder="1 10000001 01110000000000000000000"></div><div class="out" id="o"></div><div id="bx" style="display:flex;gap:2px;flex-wrap:wrap;margin-top:8px"></div>';
  const show = bits => { const f = +$('#f', el).value, d = LW.ieeeDecode(bits, f), eb = f === 32 ? 8 : 11;
    $('#bx', el).innerHTML = [...bits].map((c, i) => '<span style="width:15px;text-align:center;font-family:ui-monospace,monospace;border-radius:3px;background:' + (i === 0 ? 'rgba(251,113,133,.3)' : i <= eb ? 'rgba(34,211,238,.28)' : 'rgba(167,139,250,.25)') + '">' + c + '</span>').join('');
    $('#o', el).innerHTML = pill('sign = <b>' + d.sign + '</b>') + pill('exponent = <b>' + d.exp + '</b> = ' + d.expValue + (d.kind === 'normal' ? ' → ' + d.expValue + ' − ' + d.bias + ' = <b>' + (d.expValue - d.bias) + '</b>' : '')) + pill('fraction = ' + d.frac.slice(0, 24) + (d.frac.length > 24 ? '…' : '')) + pill(d.kind, d.kind === 'normal' ? 'y' : '') + pill('value = <b>' + d.value + '</b>', 'y') + pill('hex = ' + parseInt(bits.slice(0, 32), 2).toString(16).toUpperCase().padStart(8, '0') + (f === 64 ? parseInt(bits.slice(32), 2).toString(16).toUpperCase().padStart(8, '0') : '')); };
  const fromX = () => { const f = +$('#f', el).value, x = parseFloat($('#x', el).value); if (isNaN(x)) return; const b = LW.ieeeEncode(x, f); $('#b', el).value = b; show(b); };
  $('#x', el).oninput = fromX; $('#f', el).onchange = fromX;
  $('#b', el).oninput = () => { const f = +$('#f', el).value, b = $('#b', el).value.replace(/[^01]/g, ''); if (b.length === f) show(b); }; fromX();
};
W.numsys = el => {
  el.innerHTML = '<div class="row"><label>Decimal</label><input type="number" id="n" value="-37" style="width:110px"><label>Bits</label><select id="w"><option>4</option><option>5</option><option>6</option><option selected>8</option><option>16</option></select></div><div class="out" id="o"></div><div class="row" style="margin-top:10px"><label>Add</label><input type="number" id="a" value="100" style="width:90px"><label>+</label><input type="number" id="c" value="45" style="width:90px"><label>(two’s complement, same width)</label></div><div class="out" id="o2"></div>';
  function run() { const n = Math.trunc(+$('#n', el).value), w = +$('#w', el).value, lo = -Math.pow(2, w - 1), hi = Math.pow(2, w - 1) - 1, ok = n >= lo && n <= hi, t = LW.twos(n, w);
    $('#o', el).innerHTML = pill('binary = <b>' + LW.toBase(n, 2) + '</b>') + pill('octal = ' + LW.toBase(n, 8)) + pill('hex = ' + LW.toBase(n, 16)) + pill(w + '-bit two’s complement = <b>' + t + '</b>' + (ok ? '' : ' (out of range!)'), ok ? 'y' : 'n') + pill('one’s complement = ' + (n < 0 ? [...LW.twos(-n, w)].map(c => c === '0' ? '1' : '0').join('') : LW.twos(n, w))) + pill('range = [' + lo + ', ' + hi + ']');
    const a = Math.trunc(+$('#a', el).value), c = Math.trunc(+$('#c', el).value), r = LW.addSigned(a, c, w); $('#o2', el).innerHTML = pill(LW.twos(a, w) + ' + ' + LW.twos(c, w) + ' = <b>' + r.sum + '</b> (' + r.value + ')') + pill('carry out = ' + r.carry) + pill(r.overflow ? 'signed overflow ✘' : 'no signed overflow ✔', r.overflow ? 'n' : 'y'); }
  $$('input,select', el).forEach(i => { i.oninput = run; i.onchange = run; }); run();
};
W.kmap = el => {
  el.innerHTML = '<div class="row"><label>Variables</label><select id="n"><option>2</option><option>3</option><option selected>4</option><option>5</option></select><label>Minterms</label><input type="text" id="m" value="0 1 2 5 6 7 8 9 10 14" style="flex:1;min-width:200px"><label>Don’t-cares</label><input type="text" id="d" value="" style="width:120px"></div><div class="row" id="pre" style="margin:8px 0"><button class="btn sm">Textbook (4 vars)</button><button class="btn sm">With don’t cares</button><button class="btn sm">XOR (no simplification)</button></div><div id="km" style="overflow-x:auto"></div><div class="out" id="o"></div>';
  const P = [[4, '0 1 2 5 6 7 8 9 10 14', ''], [4, '4 8 10 11 12 15', '9 14'], [3, '1 2 4 7', '']];
  $$('#pre .btn', el).forEach((b, i) => b.onclick = () => { $('#n', el).value = P[i][0]; $('#m', el).value = P[i][1]; $('#d', el).value = P[i][2]; run(); });
  const gray = k => k === 1 ? ['0', '1'] : gray(k - 1).map(x => '0' + x).concat(gray(k - 1).slice().reverse().map(x => '1' + x));
  function run() { const n = +$('#n', el).value, lim = Math.pow(2, n), ON = [...new Set($('#m', el).value.split(/[\s,]+/).filter(Boolean).map(Number).filter(x => x >= 0 && x < lim))].sort((a, b) => a - b), DC = [...new Set($('#d', el).value.split(/[\s,]+/).filter(Boolean).map(Number).filter(x => x >= 0 && x < lim && !ON.includes(x)))];
    const rb = Math.floor(n / 2), cb = n - rb, rows = gray(Math.max(1, rb)), cols = gray(Math.max(1, cb)), names = 'ABCDE'; const R = n === 2 ? ['0', '1'] : rows, C = n === 2 ? ['0', '1'] : cols;
    let h = '<table class="tt" style="text-align:center"><tr><th>' + names.slice(0, n === 2 ? 1 : rb) + ' \\ ' + names.slice(n === 2 ? 1 : rb, n) + '</th>' + C.map(c => '<th>' + c + '</th>').join('') + '</tr>';
    R.forEach(r => { h += '<tr><th>' + r + '</th>' + C.map(c => { const m = parseInt(r + c, 2), on = ON.includes(m), d = DC.includes(m); return '<td style="background:' + (on ? 'rgba(34,211,238,.25)' : d ? 'rgba(251,191,36,.2)' : '') + '" title="m' + m + '">' + (on ? '1' : d ? '×' : '0') + '</td>'; }).join('') + '</tr>'; }); h += '</table>'; $('#km', el).innerHTML = h;
    if (!ON.length) { $('#o', el).innerHTML = pill('f = 0'); return; } const q = LW.qm(n, ON, DC);
    $('#o', el).innerHTML = pill('prime implicants: <b>' + q.primes.map(p => LW.sopString([p])).join(', ') + '</b>') + pill('minimal SOP: <b>' + LW.sopString(q.cover) + '</b>', 'y') + pill(q.terms + ' terms, ' + q.literals + ' literals'); }
  $$('input,select', el).forEach(i => { i.oninput = run; i.onchange = run; }); run();
};
W.cache = el => {
  el.innerHTML = '<div class="row"><label>Cache size (B)</label><input type="number" id="s" value="64" style="width:80px"><label>Block (B)</label><input type="number" id="b" value="16" style="width:70px"><label>Ways</label><input type="number" id="w" value="1" min="1" style="width:60px"><label>Policy</label><select id="p"><option value="lru">LRU</option><option value="fifo">FIFO</option></select></div><div class="row" style="margin-top:8px"><label>Address sequence (bytes)</label><input type="text" id="a" value="0 16 32 48 64 0 16 80 0 64" style="flex:1;min-width:260px"></div><div class="out" id="o"></div><div style="overflow-x:auto"><table class="tt" id="tb"></table></div>';
  function run() { const cfg = {size: +$('#s', el).value || 64, block: Math.max(1, +$('#b', el).value || 16), assoc: Math.max(1, +$('#w', el).value || 1), policy: $('#p', el).value}, addrs = $('#a', el).value.split(/[\s,]+/).filter(Boolean).map(Number).filter(x => x >= 0).slice(0, 40), r = LW.cacheSim(addrs, cfg), ob = Math.log2(cfg.block), ib = Math.log2(r.sets);
    $('#o', el).innerHTML = pill('sets = <b>' + r.sets + '</b> (index bits ' + (Number.isInteger(ib) ? ib : '?') + ', offset bits ' + (Number.isInteger(ob) ? ob : '?') + ')') + pill('hits <b>' + r.hits + '</b>', 'y') + pill('misses <b>' + r.misses + '</b>', 'n') + pill('hit ratio = ' + (addrs.length ? (r.hits / addrs.length).toFixed(2) : '–'));
    $('#tb', el).innerHTML = '<tr><th>address</th>' + r.seq.map(s => '<td>' + s.addr + '</td>').join('') + '</tr><tr><th>set</th>' + r.seq.map(s => '<td>' + s.set + '</td>').join('') + '</tr><tr><th>result</th>' + r.seq.map(s => '<td style="color:' + (s.hit ? 'var(--ok)' : 'var(--bad)') + '">' + (s.hit ? 'hit' : 'miss') + '</td>').join('') + '</tr>'; }
  $$('input,select', el).forEach(i => { i.oninput = run; i.onchange = run; }); run();
};
W.pipeline = el => {
  el.innerHTML = '<div class="row"><label>Instructions (one per line)</label></div><textarea id="c" rows="5" style="width:100%;font-family:ui-monospace,monospace">LW R1, 0(R2)\nADD R3, R1, R4\nSUB R5, R3, R6\nSW R5, 0(R7)</textarea><div class="row" style="margin:8px 0"><label><input type="checkbox" id="f"> operand forwarding</label><label>Branch penalty (cycles)</label><input type="number" id="bp" value="0" min="0" max="5" style="width:60px"></div><div class="out" id="o"></div><div style="overflow-x:auto"><table class="tt" id="tb"></table></div>';
  function run() { const ins = $('#c', el).value.split('\n').map(LW.parseInstr).filter(Boolean).slice(0, 12), r = LW.pipeline(ins, {forwarding: $('#f', el).checked, branchPenalty: +$('#bp', el).value || 0}), N = r.total;
    $('#o', el).innerHTML = pill('total cycles = <b>' + N + '</b>', 'y') + pill('stall cycles = <b>' + r.totalStalls + '</b>', r.totalStalls ? 'n' : 'y') + pill('CPI = ' + (N / Math.max(1, ins.length)).toFixed(2)) + pill('ideal = ' + (ins.length + 4) + ' cycles');
    let h = '<tr><th>instruction</th>' + Array.from({length: N}, (_, i) => '<th>' + (i + 1) + '</th>').join('') + '</tr>'; ins.forEach((x, i) => { const id = r.id[i], cells = Array(N).fill(''); cells[id - 2] = 'IF'; for (let c = (i ? r.id[i - 1] + 1 : 2); c < id; c++) cells[c - 1] = cells[c - 1] || '—'; cells[id - 1] = 'ID'; cells[id] = 'EX'; cells[id + 1] = 'MEM'; cells[id + 2] = 'WB'; h += '<tr><td>' + esc(x.text) + '</td>' + cells.map(c => '<td style="' + (c === '—' ? 'color:var(--bad)' : '') + '">' + c + '</td>').join('') + '</tr>'; }); $('#tb', el).innerHTML = h; }
  $$('input,textarea', el).forEach(i => { i.oninput = run; i.onchange = run; }); run();
};
$$('.wgt').forEach(el => { const f = W[el.dataset.w]; if (f && !el.dataset.done && NAMES.includes(el.dataset.w)) { el.dataset.done = 1; try { f(el); } catch (e) { el.innerHTML = '<div class="pill n">Tool failed to load: ' + esc(e.message) + '</div>'; console.error(e); } } });
})();
