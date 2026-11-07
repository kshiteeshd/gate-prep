/* GATE Prep runner: CBT exam mode + instant-feedback practice mode */
(() => {
const A = window.ATT, $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const rt = s => esc(s).replace(/\u0060\u0060\u0060(?:\w+)?\n?([\s\S]*?)\u0060\u0060\u0060/g, (m, c) => '<pre><code>' + c.replace(/\n$/, '') + '</code></pre>').replace(/\u0060([^\u0060\n]+)\u0060/g, '<code>$1</code>')
  .replace(/\$\$([\s\S]+?)\$\$/g, (m, t) => '<div class="texd" data-tex="' + t.trim() + '">' + t.trim() + '</div>')
  .replace(/\$(?=\S)([^$\n]+?)(?<=\S)\$/g, (m, t) => '<span class="tex" data-tex="' + t + '">' + t + '</span>');
/* explanation text: blank line = new paragraph, single newline = line break */
const rtx = s => rt(s).split(/\n{2,}/).map(p => /^<(pre|div)/.test(p.trim()) ? p : '<p>' + p.replace(/\n/g, '<br>') + '</p>').join('');
const typeset = el => window.GPMath && GPMath.render(el);
const api = (p, body) => fetch(`/api/attempt/${A.id}/${p}`, body === undefined ? {cache: 'no-store'} :
  {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)}).then(r => r.json());
const fmt = s => { s = Math.max(0, s | 0); const h = String(s / 3600 | 0).padStart(2, '0'), m = String(s % 3600 / 60 | 0).padStart(2, '0'), x = String(s % 60).padStart(2, '0'); return `${h}:${m}:${x}`; };
const TYPE = {single: ['MCQ', 'Choose one option. Wrong answers carry negative marks.'], multiple: ['MSQ', 'One or more options may be correct. Full marks only for the exact set — no negative marking.'], numerical: ['NAT', 'Type a number. No negative marking.']};
const LET = 'ABCDEFGH';
let P, order = [], idx = 0, sec = null, st = {ans: {}, marked: [], visited: []}, marked = new Set(), visited = new Set();
let remain = 0, tmr = null, submitted = false, violations = 0, qstart = Date.now(), saveT = null, sesCr = 0, combo = 0;

function toast(msg) { const d = document.createElement('div'); d.textContent = msg; $('#toast').appendChild(d); setTimeout(() => d.remove(), 4200); }
$$('[data-exit]').forEach(b => b.onclick = () => { const r = document.referrer; if (history.length > 1 && r && r.indexOf(location.origin) === 0 && !/\/run\//.test(r)) history.back(); else location.href = '/'; });

/* ---------- shared question rendering ---------- */
function ansOf(q) { return st.ans[q.pos] || (st.ans[q.pos] = {sel: [], num: '', t: 0}); }
function isAns(q) { const a = st.ans[q.pos]; if (!a) return false; return q.qtype === 'numerical' ? a.num !== '' && a.num != null : a.sel.length > 0; }
function drawOptions(q, box, onchange, opts = {}) {
  box.innerHTML = '';
  const a = ansOf(q);
  if (q.qtype === 'numerical') {
    const i = document.createElement('input'); i.className = 'nat'; i.type = 'number'; i.step = 'any'; i.placeholder = 'Enter value';
    i.value = a.num || ''; i.disabled = !!opts.locked; i.oninput = e => { a.num = e.target.value; onchange(); };
    box.appendChild(i); if (!opts.locked) setTimeout(() => i.focus(), 30); return;
  }
  const multi = q.qtype === 'multiple';
  q.options.forEach((o, k) => {
    const b = document.createElement('button'); b.className = 'opt' + (multi ? ' multi' : '') + (a.sel.includes(k) ? ' sel' : '');
    b.innerHTML = `<span class="k">${multi && a.sel.includes(k) ? '✓' : LET[k]}</span><span>${rt(o)}</span>`;
    if (opts.locked) {
      b.classList.add('lock'); b.classList.remove('sel');
      const right = opts.answer.includes(o), chosen = a.sel.includes(k);
      if (right) b.classList.add('right'); else if (chosen) b.classList.add('bad');
    }
    b.onclick = () => { if (opts.locked) return; if (!multi) a.sel = [k]; else { const j = a.sel.indexOf(k); j >= 0 ? a.sel.splice(j, 1) : a.sel.push(k); } onchange(true); };
    box.appendChild(b);
  });
}
function qMeta(q) { return `Marks +${q.marks}${q.qtype === 'single' && q.neg ? `, −${(+q.neg).toFixed(2).replace(/\.?0+$/, '')}` : ''}`; }

/* ---------- EXAM MODE ---------- */
const secName = c => ({GA: 'General Aptitude', CS: 'Computer Science'}[c] || c);
function status(q) { const a = isAns(q), m = marked.has(q.pos), v = visited.has(q.pos); return a && m ? 'ansmarked' : a ? 'answered' : m ? 'marked' : !v ? 'notvis' : 'notans'; }
function stamp() { const q = order[idx]; if (q) { const a = ansOf(q); a.t += Math.round((Date.now() - qstart) / 1000); qstart = Date.now(); } }
function saveSoon() { clearTimeout(saveT); saveT = setTimeout(save, 700); }
function save() { st.marked = [...marked]; st.visited = [...visited]; return api('save', st).catch(() => {}); }
function setSection(s) { stamp(); sec = s; order = P.questions.filter(q => q.sec === s); idx = 0; $$('#secTabs button').forEach(b => b.classList.toggle('on', b.dataset.s === s)); render(); }
function render() {
  const q = order[idx]; if (!q) return;
  visited.add(q.pos);
  $('#qnum').textContent = `Question ${idx + 1} of ${order.length}` + (q.src ? ` · previous year: ${q.src}` : '');
  const [tag, tip] = TYPE[q.qtype]; $('#qtype').textContent = tag; $('#qmarks').textContent = qMeta(q);
  $('#qtext').innerHTML = rt(q.text); $('#qtip').textContent = tip;
  drawOptions(q, $('#opts'), re => { drawPal(); saveSoon(); if (re) render(); });
  typeset($('.qpanel'));
  $('#palSec').textContent = secName(sec); drawPal();
}
function drawPal() {
  $('#palette').innerHTML = order.map((q, i) => `<button class="pal ${status(q)}${i === idx ? ' cur' : ''}" data-i="${i}">${i + 1}</button>`).join('');
  $$('#palette .pal').forEach(b => b.onclick = () => { stamp(); idx = +b.dataset.i; render(); });
  $('#cA').textContent = order.filter(isAns).length; $('#cT').textContent = order.length;
  if ($('#cV')) $('#cV').textContent = violations;
}
function jump(pred) {
  stamp(); const all = []; P.sections.forEach(x => P.questions.filter(q => q.sec === x).forEach(q => all.push(q)));
  const cur = all.indexOf(order[idx]);
  for (let k = 1; k <= all.length; k++) {
    const q = all[(cur + k) % all.length];
    if (pred(q)) { if (q.sec !== sec) setSection(q.sec); idx = order.indexOf(q); render(); saveSoon(); return true; }
  }
  return false;
}
const mmss = t => { t = Math.round(t); return (t / 60 | 0) + ':' + String(t % 60).padStart(2, '0'); };
function nav(d) { stamp(); idx = Math.min(order.length - 1, Math.max(0, idx + d)); render(); saveSoon(); }
function tick() { remain--; $('#timer').textContent = fmt(remain); if (remain < 300) $('#timer').classList.add('low'); if (remain === 300) toast('⏰ 5 minutes left'); if (remain <= 0) doSubmit(); }
function bootExam() {
  const secs = P.sections, byS = s => P.questions.filter(q => q.sec === s);
  const tm = P.questions.reduce((a, q) => a + q.marks, 0);
  const resumed = Object.keys(st.ans).length > 0;
  $('#boot').innerHTML = `<div class="card bootcard"><span class="tag">${P.kind === 'full' ? 'Full GATE mock' : 'Mini test'}${resumed ? ' · resumed' : ''}</span>
   <h1 class="h1" style="margin:10px 0 4px">${esc(P.title)}</h1><div class="muted">Exam mode · mixed topics · instant results at the end</div>
   <div class="bgrid"><div><b>${P.questions.length}</b><span class="muted small">questions</span></div><div><b>${tm}</b><span class="muted small">marks</span></div><div><b>${P.minutes}</b><span class="muted small">minutes</span></div></div>
   <ul><li>${secs.map(s => `${secName(s)}: ${byS(s).length}`).join(' · ')}</li><li>MCQ: negative marking ⅓ (1-mark) and ⅔ (2-mark). MSQ and NAT: none.</li>
   <li>Answers are auto-saved — you can close the app and resume; the clock keeps running.</li>${A.strict ? '<li><b>Strict mode:</b> fullscreen is required; leaving it counts as a violation (5 = auto-submit).</li>' : ''}</ul>
   <button class="btn pri block" id="startBtn" style="padding:15px;font-size:1.05rem">${resumed ? 'Resume test' : 'Start test'} ${'→'}</button></div>`;
  $('#startBtn').onclick = startExam;
}
function startExam() {
  $('#boot').hidden = true; $('#exam').hidden = false;
  $('#xTitle').textContent = P.title; $('#xSub').textContent = `${P.questions.length} questions`;
  if (P.sections.length > 1) $('#secTabs').innerHTML = P.sections.map(s => `<button data-s="${s}">${secName(s)}</button>`).join('');
  else $('#secTabs').hidden = true;
  $$('#secTabs button').forEach(b => b.onclick = () => setSection(b.dataset.s));
  remain = P.remaining; if (remain <= 0) return doSubmit();
  if (A.strict) document.documentElement.requestFullscreen && document.documentElement.requestFullscreen().catch(() => {});
  qstart = Date.now(); $('#timer').textContent = fmt(remain); tmr = setInterval(tick, 1000); setInterval(save, 15000);
  setSection(P.sections[0]);
}
function showSummary() {
  stamp(); let a = 0, na = 0, nv = 0, m = 0;
  P.questions.forEach(q => { const s = status(q); if (s === 'answered' || s === 'ansmarked') a++; else if (s === 'notans') na++; else if (s === 'notvis') nv++; if (marked.has(q.pos)) m++; });
  const c = (v, l, col) => `<div><b style="color:${col}">${v}</b><small>${l}</small></div>`;
  $('#sumGrid').innerHTML = c(a, 'Answered', 'var(--pal-ok)') + c(na, 'Not answered', 'var(--pal-no)') + c(nv, 'Not visited', 'var(--mut)') + c(m, 'Marked', 'var(--pal-mk)') + c(P.questions.length, 'Total', 'var(--txt)');
  $('#revTab').innerHTML = '<table class="revtab"><tr><th>Section</th><th>Qs</th><th>Answered</th><th>Not answered</th><th>Not visited</th><th>Marked</th><th>Time</th></tr>' + P.sections.map(x => {
    const qs = P.questions.filter(q => q.sec === x); let A1 = 0, N1 = 0, V1 = 0, M1 = 0, T1 = 0;
    qs.forEach(q => { const t = status(q); if (t === 'answered' || t === 'ansmarked') A1++; else if (t === 'notans') N1++; else if (t === 'notvis') V1++; if (marked.has(q.pos)) M1++; T1 += (st.ans[q.pos] || {}).t || 0; });
    return `<tr><td>${secName(x)}</td><td>${qs.length}</td><td class="a">${A1}</td><td class="n">${N1}</td><td class="v">${V1}</td><td class="m">${M1}</td><td>${mmss(T1)}</td></tr>`;
  }).join('') + '</table>';
  $('#subModal').classList.add('on');
}
async function doSubmit() {
  if (submitted) return; submitted = true; clearInterval(tmr); stamp(); st.marked = [...marked]; st.visited = [...visited];
  const used = Math.max(0, P.minutes * 60 - remain);
  const r = await api('submit', {state: st, violations, used_sec: used});
  if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
  location.replace(r.result);
}

/* ---------- PRACTICE MODE ---------- */
let done = {}, pq0 = Date.now(), lastIdx = -1;
function pstate(q) { return done[q.pos]; }
function drawSeg() {
  $('#pPal').innerHTML = P.questions.map((q, i) => { const d = done[q.pos]; return `<button class="pal ${d ? (d.state === 'correct' ? 'correct' : 'wrong') : 'notvis'}${i === idx ? ' cur' : ''}" data-i="${i}">${i + 1}</button>`; }).join('');
  $$('#pPal .pal').forEach(e => e.onclick = () => { idx = +e.dataset.i; pRender(); });
  $('#pA').textContent = Object.keys(done).length; $('#pT').textContent = P.questions.length;
}
function pRender() {
  const q = P.questions[idx], d = pstate(q); if (idx !== lastIdx) { pq0 = Date.now(); lastIdx = idx; }
  $('#pmeta').innerHTML = `<span class="tag">${q.subject}</span><span class="tag">${esc(q.topic)}</span><span class="tag ${q.diff}">${q.diff}</span><span class="tag">${TYPE[q.qtype][0]}</span><span class="tag">${qMeta(q)}</span>`;
  $('#pnum').textContent = `Question ${idx + 1} of ${P.questions.length}` + (q.src && q.src.startsWith('GATE') ? ` · previous year: ${q.src}` : '');
  $('#pqtext').innerHTML = rt(q.text);
  const a = ansOf(q); if (d) { a.sel = d.selected.map(t => q.options.indexOf(t)); a.num = d.numeric == null ? '' : d.numeric; }
  drawOptions(q, $('#popts'), re => { $('#pcheck').disabled = !isAns(q); if (re) pRender(); }, d ? {locked: true, answer: d.answer} : {});
  $('#pcheck').hidden = !!d; $('#pnext').hidden = !d; $('#pskip').hidden = !!d;
  $('#pcheck').disabled = !d && !isAns(q);
  $('#pnext').textContent = idx === P.questions.length - 1 ? 'Finish ✓' : 'Next →';
  showFb(d, q); drawSeg(); typeset($('.qpanel'));
}
function showFb(d, q) {
  const fb = $('#pfb'); if (!d) { fb.hidden = true; return; }
  fb.hidden = false; const ok = d.state === 'correct';
  fb.className = 'fb ' + (ok ? 'ok' : 'no');
  fb.innerHTML = `${d.credit ? `<span class="cr">+${d.credit} credits</span>` : ''}<h3>${d.state === 'correct' ? '✓ Correct!' : d.state === 'skipped' ? 'Skipped' : '✗ Not quite'}</h3>
   ${ok && q.qtype !== 'numerical' ? '' : `<div>Correct answer: <b>${esc(d.correct)}</b></div>`}<div class="ex">${d.expl ? rtx(d.expl) : '<span class="muted">No written explanation for this question yet.</span>'}</div>`;
}
function floatCr(n) { const e = document.createElement('div'); e.className = 'floatcr'; e.textContent = '+' + n; const r = $('#pcheck').getBoundingClientRect(); e.style.left = (r.left + r.width / 2 - 14) + 'px'; e.style.top = (r.top - 10) + 'px'; document.body.appendChild(e); setTimeout(() => e.remove(), 1300); }
async function pCheck() {
  const q = P.questions[idx]; if (pstate(q) || !isAns(q)) return;
  $('#pcheck').disabled = true; const a = ansOf(q);
  const r = await api('check', {pos: q.pos, sel: a.sel, num: a.num, time: Math.round((Date.now() - pq0) / 1000)});
  if (r.error) { toast(r.error); return; }
  done[q.pos] = {state: r.state, credit: r.credit, correct: r.correct, answer: r.answer, expl: r.expl, selected: a.sel.map(i => q.options[i]), numeric: a.num === '' ? null : a.num};
  if (r.credit) { sesCr += r.credit; $('#sesCr').textContent = sesCr; floatCr(r.credit); }
  combo = r.state === 'correct' ? combo + 1 : 0; const cb = $('#combo'); cb.style.display = combo >= 2 ? '' : 'none'; cb.querySelector('span').textContent = combo;
  (r.events || []).forEach(e => toast(e.scope === 'ALL' ? `🎉 Overall level ${e.to}: ${e.title}!${e.unlocked.length ? ' Unlocked ' + e.unlocked.length + ' mock test(s)' : ''}` : `🎉 ${e.scope} reached Level ${e.to}!${e.unlocked.length ? ' Unlocked: ' + e.unlocked.join(', ') : ''}`));
  pRender();
}
async function pNext() {
  if (idx < P.questions.length - 1) { idx = P.questions.findIndex((q, i) => i > idx && !done[q.pos]); if (idx < 0) idx = P.questions.findIndex(q => !done[q.pos]); if (idx < 0) return pFinish(); pRender(); }
  else { const j = P.questions.findIndex(q => !done[q.pos]); if (j >= 0 && confirm('Some questions are unanswered. Go back to them? (Cancel = finish)')) { idx = j; pRender(); } else pFinish(); }
}
async function pFinish() { if (submitted) return; submitted = true; const r = await api('submit', {state: {}, used_sec: 0}); location.replace(r.result); }
function bootPractice() {
  $('#boot').hidden = true; $('#prac').hidden = false; $('#pTitle').textContent = P.title; $('#pSub').textContent = 'Practice · instant feedback';
  done = P.done || {}; Object.keys(done).forEach(k => { done[k] = done[k]; }); done = Object.fromEntries(Object.entries(done).map(([k, v]) => [+k, v]));
  sesCr = Object.values(done).reduce((s, d) => s + d.credit, 0); $('#sesCr').textContent = sesCr;
  idx = Math.max(0, P.questions.findIndex(q => !done[q.pos])); if (Object.keys(done).length === P.questions.length) idx = P.questions.length - 1;
  $('#pcheck').onclick = pCheck; $('#pnext').onclick = pNext;
  $('#pFinishBtn').onclick = () => { const left = P.questions.filter(q => !done[q.pos]).length; if (!left || confirm(left + ' question(s) not attempted yet. Finish and see results?')) pFinish(); };
  $('#pskip').onclick = () => { const j = P.questions.findIndex((q, i) => i > idx && !done[q.pos]); idx = j >= 0 ? j : (idx + 1) % P.questions.length; pRender(); };
  document.addEventListener('keydown', e => {
    if (e.target.tagName === 'INPUT' && e.key !== 'Enter') return;
    const q = P.questions[idx], d = pstate(q);
    if (e.key === 'Enter') { d ? pNext() : pCheck(); return; }
    const k = '1234567'.indexOf(e.key) >= 0 ? '1234567'.indexOf(e.key) : 'abcdefg'.indexOf(e.key.toLowerCase());
    if (!d && q.qtype !== 'numerical' && k >= 0 && k < q.options.length) $$('#popts .opt')[k].click();
  });
  setInterval(() => { $('#ptime').textContent = ((Date.now() - pq0) / 60000 | 0) + ':' + String((Date.now() - pq0) / 1000 % 60 | 0).padStart(2, '0'); }, 1000);
  if (P.minutes) {
    remain = P.remaining; $('#pTimer').hidden = false;
    const t = () => { $('#pTimer b').textContent = fmt(remain).replace(/^00:/, ''); if (remain < 300) $('#pTimer').style.color = 'var(--bad)'; if (remain <= 0) { clearInterval(tmr); toast('⏰ Time is up'); pFinish(); } remain--; };
    t(); tmr = setInterval(t, 1000);
  }
  pRender();
}

/* ---------- wiring ---------- */
async function init() {
  P = await api('paper');
  if (P.error) { if (P.result) location.replace(P.result); else $('#boot').innerHTML = '<div class="card bootcard">This attempt could not be loaded. <a href="/">Back</a></div>'; return; }
  if (A.mode === 'practice') return bootPractice();
  st = Object.assign({ans: {}, marked: [], visited: []}, P.state || {}); marked = new Set(st.marked); visited = new Set(st.visited);
  bootExam();
}
$('#prevBtn').onclick = () => nav(-1);
$('#nextBtn').onclick = () => nav(1);
$('#markBtn').onclick = () => { marked.add(order[idx].pos); nav(1); };
$('#clearBtn').onclick = () => { const q = order[idx]; delete st.ans[q.pos]; render(); saveSoon(); };
$('#submitBtn').onclick = showSummary;
$('#unBtn').onclick = () => { if (!jump(q => !isAns(q))) toast('Every question has an answer'); };
const review = (pred, none) => () => { $('#subModal').classList.remove('on'); if (!jump(pred)) { toast(none); } };
$('#revUn').onclick = review(q => !isAns(q), 'Nothing left unanswered');
$('#revMk').onclick = review(q => marked.has(q.pos), 'No questions are marked for review');
setInterval(() => { const q = order[idx]; if (q && !$('#exam').hidden) $('#qtime').textContent = 'This question ' + mmss(((st.ans[q.pos] || {}).t || 0) + (Date.now() - qstart) / 1000); }, 1000);
$('#cancelSubmit').onclick = () => $('#subModal').classList.remove('on');
$('#doSubmit').onclick = doSubmit;
$('#calcBtn').onclick = () => { $('#calc').hidden = !$('#calc').hidden; $('#calcIn').focus(); };
$('#calcX').onclick = () => $('#calc').hidden = true;
$('#calcIn').onkeydown = e => {
  if (e.key !== 'Enter') return;
  try {
    let s = e.target.value.replace(/\^/g, '**').replace(/\bln\(/g, 'Math.log(').replace(/\blog\(/g, 'Math.log10(').replace(/\bpi\b/gi, 'Math.PI').replace(/\be\b/g, 'Math.E').replace(/\b(sin|cos|tan|sqrt|abs|asin|acos|atan|exp|floor|ceil|round)\(/g, 'Math.$1(');
    if (!/^[\d\s+\-*/().,%A-Za-z]*$/.test(s) || /[A-Za-z_]+/.test(s.replace(/Math\.(PI|E|log10|log|sin|cos|tan|sqrt|abs|asin|acos|atan|exp|floor|ceil|round)/g, ''))) throw 0;
    $('#calcOut').textContent = '= ' + +Function('"use strict";return (' + s + ')')().toPrecision(12);
  } catch (_) { $('#calcOut').textContent = '= invalid'; }
};
document.addEventListener('keydown', e => {
  if (A.mode !== 'exam' || $('#exam').hidden || e.target.tagName === 'INPUT') return;
  if (e.key === 'ArrowRight') nav(1); if (e.key === 'ArrowLeft') nav(-1);
});
if (A.strict) {
  $('#fsBack').onclick = () => { document.documentElement.requestFullscreen().catch(() => {}); $('#fsWarn').classList.remove('on'); };
  document.addEventListener('fullscreenchange', () => { if (submitted || $('#exam').hidden || document.fullscreenElement) return; violations++; $('#vcount').textContent = violations; $('#fsWarn').classList.add('on'); drawPal(); if (violations >= 5) doSubmit(); });
  document.addEventListener('visibilitychange', () => { if (document.hidden && !submitted && !$('#exam').hidden) { violations++; drawPal(); } });
}
init();
})();
