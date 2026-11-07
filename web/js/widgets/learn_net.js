/* GATE Prep — learning modules: computer-network tools (IPv4 subnetting, CRC, TCP congestion window, shortest paths) */
(function () {
const G = typeof window !== 'undefined' ? window : globalThis;
const LW = G.LW = G.LW || {};

/* ======================= pure logic (unit-tested with node) ======================= */
LW.ipToInt = s => { const p = s.trim().split('.').map(Number); if (p.length !== 4 || p.some(x => !(x >= 0 && x <= 255) || !Number.isInteger(x))) return null; return ((p[0] * 256 + p[1]) * 256 + p[2]) * 256 + p[3]; };
LW.intToIp = n => [Math.floor(n / 16777216) % 256, Math.floor(n / 65536) % 256, Math.floor(n / 256) % 256, n % 256].join('.');
LW.subnet = (ip, prefix) => { const a = LW.ipToInt(ip); if (a === null || !(prefix >= 0 && prefix <= 32)) return null; const size = Math.pow(2, 32 - prefix), net = Math.floor(a / size) * size, bc = net + size - 1, mask = prefix === 0 ? 0 : 4294967296 - size;
  return {network: LW.intToIp(net), broadcast: LW.intToIp(bc), mask: LW.intToIp(mask), first: prefix >= 31 ? LW.intToIp(net) : LW.intToIp(net + 1), last: prefix >= 31 ? LW.intToIp(bc) : LW.intToIp(bc - 1), hosts: prefix >= 31 ? size : size - 2, size}; };
LW.ipClass = ip => { const a = +ip.split('.')[0]; return a < 128 ? 'A' : a < 192 ? 'B' : a < 224 ? 'C' : a < 240 ? 'D' : 'E'; };
// CRC: data and generator as bit strings; returns remainder (len(gen)-1 bits) and the transmitted codeword
LW.crc = (data, gen) => { const r = gen.length - 1, bits = (data + '0'.repeat(r)).split('').map(Number), g = gen.split('').map(Number);
  for (let i = 0; i < data.length; i++) if (bits[i]) for (let j = 0; j < g.length; j++) bits[i + j] ^= g[j];
  const rem = bits.slice(data.length).join(''); return {remainder: rem, codeword: data + rem}; };
LW.crcCheck = (word, gen) => { const g = gen.split('').map(Number), bits = word.split('').map(Number); for (let i = 0; i + g.length <= bits.length; i++) if (bits[i]) for (let j = 0; j < g.length; j++) bits[i + j] ^= g[j]; return bits.every(b => b === 0); };
// TCP congestion window per transmission round: events {round: 'timeout' | 'dup'}
LW.tcp = (rounds, ssthresh, events) => { events = events || {}; let cwnd = 1, ss = ssthresh; const out = [];
  for (let r = 1; r <= rounds; r++) { out.push(cwnd); const ev = events[r];
    if (ev === 'timeout') { ss = Math.max(2, Math.floor(cwnd / 2)); cwnd = 1; } else if (ev === 'dup') { ss = Math.max(2, Math.floor(cwnd / 2)); cwnd = ss; } else if (cwnd < ss) cwnd = Math.min(cwnd * 2, ss); else cwnd = cwnd + 1; }
  return out; };
// shortest paths: edges [u, v, w] undirected or directed; returns distance map from src (Dijkstra)
LW.dijkstra = (nodes, edges, src, directed) => { const d = {}; nodes.forEach(n => d[n] = Infinity); d[src] = 0; const done = new Set();
  for (;;) { let u = null; nodes.forEach(n => { if (!done.has(n) && d[n] < Infinity && (u === null || d[n] < d[u])) u = n; }); if (u === null) break; done.add(u);
    edges.forEach(([a, b, w]) => { if (a === u && d[a] + w < d[b]) d[b] = d[a] + w; if (!directed && b === u && d[b] + w < d[a]) d[a] = d[b] + w; }); }
  return d; };

if (typeof document === 'undefined') return;

/* ======================= widgets ======================= */
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const W = G.LW_W = G.LW_W || {};
const pill = (t, c) => '<span class="pill ' + (c || '') + '">' + t + '</span>';
const NAMES = ['subnet', 'crc', 'tcp'];

W.subnet = el => {
  el.innerHTML = '<div class="row"><label>IP address</label><input type="text" id="ip" value="192.168.10.77" style="width:150px"><label>Prefix /</label><input type="number" id="p" value="26" min="0" max="32" style="width:70px"><label>Subnets wanted</label><input type="number" id="n" value="4" min="1" max="1024" style="width:70px"></div><div class="out" id="o"></div><div class="out" id="o2"></div>';
  function run() { const ip = $('#ip', el).value, p = +$('#p', el).value, s = LW.subnet(ip, p); if (!s) { $('#o', el).innerHTML = pill('Enter a valid IPv4 address and a prefix 0–32', 'n'); $('#o2', el).innerHTML = ''; return; }
    $('#o', el).innerHTML = pill('class ' + LW.ipClass(ip)) + pill('network <b>' + s.network + '/' + p + '</b>', 'y') + pill('mask ' + s.mask) + pill('broadcast ' + s.broadcast) + pill('hosts ' + s.first + ' … ' + s.last) + pill('usable hosts = <b>' + s.hosts + '</b>');
    const n = Math.max(1, +$('#n', el).value | 0), b = Math.ceil(Math.log2(n)), np = p + b; $('#o2', el).innerHTML = np > 32 ? pill('cannot split into ' + n + ' subnets', 'n') : pill('borrow ⌈log₂ ' + n + '⌉ = <b>' + b + '</b> bits → new prefix /' + np) + pill('subnets created = ' + Math.pow(2, b)) + pill('hosts per subnet = ' + LW.subnet(ip, np).hosts); }
  $$('input', el).forEach(i => i.oninput = run); run();
};
W.crc = el => {
  el.innerHTML = '<div class="row"><label>Data bits</label><input type="text" id="d" value="1101011011" style="flex:1;min-width:200px"><label>Generator</label><input type="text" id="g" value="10011" style="width:140px"></div><div class="out" id="o"></div><div class="row" style="margin-top:8px"><label>Received word</label><input type="text" id="r" style="flex:1;min-width:200px" placeholder="paste the codeword (flip a bit to see detection)"><span id="v"></span></div>';
  function run() { const d = $('#d', el).value.replace(/[^01]/g, ''), g = $('#g', el).value.replace(/[^01]/g, ''); if (!d || g.length < 2 || g[0] !== '1') { $('#o', el).innerHTML = pill('Generator must start with 1 and have ≥ 2 bits', 'n'); return; } const r = LW.crc(d, g);
    $('#o', el).innerHTML = pill('appended zeros = ' + (g.length - 1)) + pill('remainder (CRC) = <b>' + r.remainder + '</b>', 'y') + pill('transmitted = <b>' + r.codeword + '</b>'); const rx = $('#r', el).value.replace(/[^01]/g, ''); $('#v', el).innerHTML = rx.length >= g.length ? pill(LW.crcCheck(rx, g) ? '✔ no error detected' : '✘ error detected', LW.crcCheck(rx, g) ? 'y' : 'n') : ''; }
  $$('input', el).forEach(i => i.oninput = run); run();
};
W.tcp = el => {
  el.innerHTML = '<div class="row"><label>Initial ssthresh</label><input type="number" id="s" value="16" style="width:70px"><label>Rounds</label><input type="number" id="n" value="20" min="5" max="40" style="width:70px"><label>Timeout at rounds</label><input type="text" id="t" value="11" style="width:100px"><label>3 dup-ACKs at rounds</label><input type="text" id="d" value="" style="width:100px"></div><svg class="gsvg" id="sv" viewBox="0 0 560 220" style="height:220px;margin-top:8px"></svg><div class="out" id="o"></div>';
  function run() { const ev = {}; ($('#t', el).value.match(/\d+/g) || []).forEach(x => ev[+x] = 'timeout'); ($('#d', el).value.match(/\d+/g) || []).forEach(x => ev[+x] = 'dup'); const n = Math.min(40, Math.max(5, +$('#n', el).value | 0)), c = LW.tcp(n, Math.max(2, +$('#s', el).value | 0), ev), mx = Math.max(...c);
    let svg = '<polyline fill="none" stroke="#22d3ee" stroke-width="2.5" points="' + c.map((v, i) => (30 + i * (510 / (n - 1))) + ',' + (200 - v / mx * 180)).join(' ') + '"/>'; c.forEach((v, i) => svg += '<circle cx="' + (30 + i * (510 / (n - 1))) + '" cy="' + (200 - v / mx * 180) + '" r="3.5" fill="' + (ev[i + 1] ? '#fb7185' : '#22d3ee') + '"/>'); $('#sv', el).innerHTML = svg;
    $('#o', el).innerHTML = pill('cwnd per round: ' + c.join(', ')) + pill('max cwnd = ' + mx); }
  $$('input', el).forEach(i => i.oninput = run); run();
};
$$('.wgt').forEach(el => { const f = W[el.dataset.w]; if (f && !el.dataset.done && NAMES.includes(el.dataset.w)) { el.dataset.done = 1; try { f(el); } catch (e) { el.innerHTML = '<div class="pill n">Tool failed to load: ' + esc(e.message) + '</div>'; console.error(e); } } });
})();
