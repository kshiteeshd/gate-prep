/* GATE Prep — question component, practice runner (DPP / drill / review), CBT exam runner, results. */
'use strict';
(() => {
const V = GP.views, F = V.full = {};
const S = () => GP.S;
const DIFF = {e: 'easy', m: 'medium', h: 'hard'};
const TYPE = {s: 'MCQ', m: 'MSQ', n: 'NAT'};
const mk = q => `+${q.m}${q.y === 's' && q.n ? ', −' + (+q.n).toFixed(2).replace(/\.?0+$/, '') : ''}`;
const secName = c => ({GA: 'General Aptitude', CS: 'Computer Science'}[c] || (GP.subj(c) || {}).name || c);

/* ---------- one question with a Check button (lessons) ---------- */
GP.mountQ = (el, q, o = {}) => {
  let sel = [], num = '', done = false; const n = q.y === 'n', multi = q.y === 'm';
  el.innerHTML = `<div class="q">${o.label ? `<div class="qhead"><span>${esc(o.label)}</span><span>${DIFF[q.d]} · ${TYPE[q.y]} · ${mk(q)}</span></div>` : ''}<div class="text">${fx(q.x)}</div>
    <div class="opts">${n ? '<input class="nat" type="number" step="any" placeholder="Your answer">' : q.o.map((t, i) => `<button class="opt ${multi ? 'multi' : ''}" data-i="${i}"><span class="k">${LET[i]}</span><span>${fx(t)}</span></button>`).join('')}</div>
    <div class="fbw"></div><div class="acts"><button class="btn pri chk" disabled>Check answer</button></div></div>`;
  const chk = $('.chk', el), upd = () => { chk.disabled = n ? num === '' : !sel.length; };
  if (n) $('.nat', el).oninput = e => { num = e.target.value; upd(); };
  else $$('.opt', el).forEach(b => b.onclick = () => { if (done) return; const i = +b.dataset.i; if (multi) sel = sel.includes(i) ? sel.filter(x => x !== i) : [...sel, i]; else sel = [i]; $$('.opt', el).forEach((x, k) => x.classList.toggle('sel', sel.includes(k))); upd(); });
  chk.onclick = () => {
    if (done) return; done = true; const st = GP.judge(q, sel, num), ok = st === 'ok';
    if (n) $('.nat', el).disabled = true; else $$('.opt', el).forEach((b, i) => { b.disabled = true; b.classList.remove('sel'); if (q.a.includes(i)) b.classList.add('right'); else if (sel.includes(i)) b.classList.add('wrong'); });
    $('.fbw', el).innerHTML = `<div class="fb ${ok ? 'ok' : 'no'}"><p><b class="${ok ? 'ok' : 'no'}">${ok ? 'Correct' : 'Not quite'}</b>${n && !ok ? ` — the answer is <span class="mono">${q.a}${q.tol ? ' (±' + q.tol + ')' : ''}</span>` : ''}</p>${q.e ? para(q.e) : '<p class="mut">No written explanation for this question.</p>'}</div>`;
    typeset($('.fbw', el)); GP.record(q, ok, o.src); chk.remove(); GP.chrome();
  };
  typeset(el);
};

/* ---------- shared runner chrome ---------- */
function exitRun() { const r = document.referrer; if (history.length > 1) history.back(); else location.hash = '#/home'; }
function palToggle() { const a = $('aside.pal-aside'); a && a.classList.toggle('open'); }
function runShell(root, o) {
  root.innerHTML = `<div class="run"><div class="head"><button class="ghost" id="rx">← Exit</button><div class="ti"><b class="mono">${esc(o.title)}</b><div class="sm mut">${esc(o.sub || '')}</div></div><div class="grow"></div>
    ${o.noPal ? '' : '<button class="ghost palbtn" id="rpal">Questions</button>'}${o.timer ? '<div class="timer" id="rtimer">--:--</div>' : ''}${o.full ? '<button class="ghost only-d" id="rfs" title="Full screen (F11)">⛶</button>' : ''}<button class="btn ${o.finishPri ? 'pri' : ''} sm" id="rfin">${o.finishLabel}</button></div>
    ${o.tabs ? '<div class="tabs" id="rtabs" style="margin:0;padding:0 var(--s3)"></div>' : ''}
    <div class="body" ${o.noPal ? 'style="grid-template-columns:minmax(0,1fr)"' : ''}><main id="rmain"></main>${o.noPal ? '' : '<aside class="pal-aside"><h3 class="row sp"><span id="rpt">Questions</span><button class="ghost sm only-m" id="rpalx">Close</button></h3><div class="pgrid" id="rgrid"></div><div class="legend" id="rleg"></div><div class="legend" id="rcnt"></div></aside>'}</div></div>`;
  $('#rx').onclick = o.onExit || exitRun; $('#rfin').onclick = o.onFinish;
  $('#rpal') && ($('#rpal').onclick = palToggle); $('#rpalx') && ($('#rpalx').onclick = palToggle); $('#rfs') && ($('#rfs').onclick = GP.fullscreen);
}

/* ---------- practice runner: DPP, drill, review (instant feedback) ---------- */
async function practiceRun(cfg, root) {
  root.innerHTML = '<div class="loading">Loading questions…</div>';
  const need = new Set(); cfg.qids.forEach(id => { /* subjects resolved below */ });
  await GP.loadSubjects(cfg.subjects);
  const qids = cfg.qids.filter(id => GP.Q(id));
  if (!qids.length) { root.innerHTML = '<div class="page"><p class="mut">No questions available.</p><a class="btn" href="#/practice">Back</a></div>'; return; }
  const R = S().running[cfg.key] || (S().running[cfg.key] = {title: cfg.title, href: cfg.href, kind: cfg.kind, qids, idx: 0, ans: {}, started: Date.now()});
  R.ts = Date.now();
  let sel = [], num = '', t0 = Date.now(), tick = null;
  const review = cfg.kind === 'review';
  runShell(root, {title: cfg.title, sub: review ? 'Spaced review' : cfg.kind === 'drill' ? 'Instant feedback' : 'Practice · instant feedback', noPal: review, timer: !review, finishLabel: review ? 'End session' : 'Finish', onFinish: () => finish(false)});
  const q = () => GP.Q(R.qids[R.idx]), A = () => R.ans[q().i];
  function pal() {
    if (review) return;
    $('#rgrid').innerHTML = R.qids.map((id, i) => { const a = R.ans[id]; return `<button class="pal ${a ? (a.ok ? 'ok' : 'no') : 'nv'} ${i === R.idx ? 'cur' : ''}" data-i="${i}">${i + 1}</button>`; }).join('');
    $$('#rgrid .pal').forEach(b => b.onclick = () => { R.idx = +b.dataset.i; sel = []; num = ''; draw(); $('aside.pal-aside').classList.remove('open'); });
    $('#rleg').innerHTML = '<span><i style="background:var(--pal-ok)"></i>Correct</span><span><i style="background:var(--pal-no)"></i>Wrong</span><span><i style="background:var(--bg);border:1px solid var(--line2)"></i>Not attempted</span>';
    $('#rcnt').innerHTML = `<span>Attempted <b>${Object.keys(R.ans).length}</b> / ${R.qids.length}</span>`;
  }
  function draw() {
    const x = q(), a = A(), n = x.y === 'n', multi = x.y === 'm', last = R.idx === R.qids.length - 1;
    t0 = Date.now();
    $('#rmain').innerHTML = `<div class="qpanel"><div class="qhead"><span>${review ? 'Review ' : 'Question '}${R.idx + 1} of ${R.qids.length}${x.r ? ' · ' + esc(x.r) : ''}</span><span>${esc(x.t)} · ${DIFF[x.d]} · ${TYPE[x.y]} · ${mk(x)}</span></div>
      <div class="q"><div class="text">${fx(x.x)}</div><div class="opts">${n ? `<input class="nat" type="number" step="any" placeholder="Enter value" value="${a ? a.num ?? '' : ''}" ${a ? 'disabled' : ''}>` : x.o.map((t, i) => `<button class="opt ${multi ? 'multi' : ''}" data-i="${i}" ${a ? 'disabled' : ''}><span class="k">${LET[i]}</span><span>${fx(t)}</span></button>`).join('')}</div><div id="fbw"></div></div></div>
      <div class="acts"><button class="btn" id="bskip" ${a ? 'hidden' : ''}>Skip</button><span class="grow"></span><button class="btn pri" id="bchk" ${a ? 'hidden' : 'disabled'}>Check answer</button><button class="btn pri" id="bnext" ${a ? '' : 'hidden'}>${last ? 'Finish' : 'Next'} →</button></div>`;
    if (a) { if (!n) $$('.opt').forEach((b, i) => { if (x.a.includes(i)) b.classList.add('right'); else if ((a.sel || []).includes(i)) b.classList.add('wrong'); }); fb(x, a); }
    else if (n) $('.nat').oninput = e => { num = e.target.value; $('#bchk').disabled = num === ''; };
    else $$('.opt').forEach(b => b.onclick = () => { const i = +b.dataset.i; if (multi) sel = sel.includes(i) ? sel.filter(v => v !== i) : [...sel, i]; else sel = [i]; $$('.opt').forEach((o, k) => o.classList.toggle('sel', sel.includes(k))); $('#bchk').disabled = !sel.length; });
    $('#bchk').onclick = check; $('#bnext').onclick = next; $('#bskip').onclick = () => { const j = R.qids.findIndex((id, i) => i > R.idx && !R.ans[id]); R.idx = j >= 0 ? j : (R.idx + 1) % R.qids.length; sel = []; num = ''; draw(); };
    typeset($('#rmain')); pal(); GP.save();
  }
  function fb(x, a) {
    const n = x.y === 'n', ok = a.ok;
    let note = '';
    if (review) { const r = S().review[x.i]; note = ok ? `<p class="mut sm">Moved up — you will see it again in ${STEPS[r.stage]} day${STEPS[r.stage] > 1 ? 's' : ''}.</p>` : '<p class="mut sm">Back to the start — you will see it again tomorrow.</p>'; }
    else if (!ok) note = '<p class="mut sm">Added to your review queue — it comes back tomorrow.</p>';
    $('#fbw').innerHTML = `<div class="fb ${ok ? 'ok' : 'no'}"><p><b class="${ok ? 'ok' : 'no'}">${ok ? 'Correct' : 'Not quite'}</b>${n && !ok ? ` — the answer is <span class="mono">${x.a}${x.tol ? ' (±' + x.tol + ')' : ''}</span>` : ''}</p>${x.e ? para(x.e) : '<p class="mut">No written explanation for this question.</p>'}${note}</div>`;
  }
  function check() {
    const x = q(), st = GP.judge(x, sel, num); if (st === 'skip') return; const ok = st === 'ok';
    R.ans[x.i] = {ok, sel: sel.slice(), num: x.y === 'n' ? num : undefined, t: Math.round((Date.now() - t0) / 1000)};
    GP.record(x, ok, review ? 'review' : ''); sel = []; num = ''; draw(); GP.chrome();
  }
  function next() { if (R.idx >= R.qids.length - 1) return finish(true); R.idx++; sel = []; num = ''; draw(); window.scrollTo(0, 0); }
  function finish(auto) {
    const left = R.qids.filter(id => !R.ans[id]).length;
    if (!auto && left && !review && !confirm(`${left} question${left > 1 ? 's' : ''} not attempted yet. Finish and see results?`)) return;
    clearInterval(tick); GP.cleanup = null;
    const items = R.qids.map(id => { const a = R.ans[id]; return {id, ok: !!(a && a.ok), skipped: !a, t: a ? a.t : 0}; });
    const attempted = items.filter(i => !i.skipped);
    if (review) {
      const right = attempted.filter(i => i.ok).length; delete S().running[cfg.key]; GP.save();
      root.innerHTML = `<div class="page"><div class="next"><div class="eyebrow">Done</div><h1 class="h1">${right} of ${attempted.length} correct</h1><p>${attempted.length - right ? `${attempted.length - right} will come back tomorrow.` : 'All of these move to a longer interval.'}</p><div class="row wrap"><a class="btn pri" href="${GP.dueIds().length ? '#/review' : '#/practice'}">${GP.dueIds().length ? 'More due questions' : 'Back to practice'}</a><a class="btn" href="#/home">Home</a></div></div></div>`;
      return;
    }
    const score = items.reduce((a, i) => a + (i.skipped ? 0 : GP.marksFor(GP.Q(i.id), i.ok ? 'ok' : 'bad')), 0), max = items.reduce((a, i) => a + GP.Q(i.id).m, 0);
    S().tests.push({id: Date.now().toString(36), tid: cfg.tid || cfg.key, title: cfg.title, kind: cfg.kind, when: today(), dry: false, used: Math.round((Date.now() - R.started) / 1000), minutes: 0, items, score, max});
    if (cfg.tid) { const d = S().done[cfg.tid] || {best: -1e9, max, n: 0}; d.best = Math.max(d.best, Math.round(score * 100) / 100); d.max = max; d.n++; S().done[cfg.tid] = d; }
    delete S().running[cfg.key]; GP.save(); location.hash = '#/result/' + (S().tests.length - 1);
  }
  if (!review) { const el = $('#rtimer'); const t = () => { el.textContent = mmss((Date.now() - R.started) / 1000); }; t(); tick = setInterval(t, 1000); GP.cleanup = () => clearInterval(tick); }
  const keyH = e => {
    if ($('.sheetov') || e.ctrlKey || e.altKey || e.metaKey) return;
    const typing = /INPUT|TEXTAREA/.test((e.target || {}).tagName);
    if (e.key === 'Enter') { e.preventDefault(); const nx = $('#bnext'), ck = $('#bchk'); if (nx && !nx.hidden) next(); else if (ck && !ck.hidden && !ck.disabled) check(); return; }
    if (typing || q().y === 'n' || A()) return;
    const k = '12345678'.indexOf(e.key) >= 0 ? '12345678'.indexOf(e.key) : 'abcdefgh'.indexOf(e.key.toLowerCase());
    const o = k >= 0 && $$('#rmain .opt')[k]; if (o) o.click();
  };
  document.addEventListener('keydown', keyH);
  const prevClean = GP.cleanup; GP.cleanup = () => { prevClean && prevClean(); document.removeEventListener('keydown', keyH); };
  draw();
}

F.dpp = async (p, root) => {
  const t = (await GP.tests()).find(x => x.id === p[2]); if (!t) { root.innerHTML = '<div class="page"><p>Test not found.</p></div>'; return; }
  practiceRun({key: t.id, tid: t.id, title: t.ti, href: '#/dpp/' + t.id, kind: 'dpp', qids: t.q, subjects: t.u}, root);
};
F.drill = async (p, root) => {
  const sub = p[2], sj = GP.subj(sub), topic = sj && sj.topics[+p[3]]; if (!topic) { root.innerHTML = '<div class="page"><p>Unknown topic.</p></div>'; return; }
  const key = `drill:${sub}:${p[3]}`;
  if (!S().running[key]) {
    root.innerHTML = '<div class="loading">Picking questions…</div>'; await GP.loadSubjects([sub]);
    const pool = Object.values(GP.qi).filter(q => q.sub === sub && q.t === topic && q.p === 'dpp');
    const w = q => { const s = S().qs[q.i]; return s ? (s[1] < s[0] ? 1 : 2) + Math.random() : Math.random(); };     // unseen first, then ones you got wrong, then the rest
    const pick = pool.map(q => [w(q), q]).sort((a, b) => a[0] - b[0]).slice(0, 10).map(x => x[1]);
    S().running[key] = null; var ids = pick.map(q => q.i);
  }
  practiceRun({key, title: 'Drill · ' + topic, href: `#/drill/${sub}/${p[3]}`, kind: 'drill', qids: (S().running[key] || {}).qids || ids, subjects: [sub]}, root);
};
F.review = async (p, root) => {
  const due = GP.dueIds().slice(0, 20); if (!due.length) { location.hash = '#/practice'; return; }
  const key = 'review'; const keep = S().running[key];
  const ids = keep ? keep.qids : due;
  root.innerHTML = '<div class="loading">Loading…</div>';
  await GP.loadSubjects(GP.meta.subjects.map(s => s.code));      // review items can come from any subject
  practiceRun({key, title: 'Review', href: '#/review', kind: 'review', qids: ids, subjects: []}, root);
};

/* ---------- CBT exam runner ---------- */
F.test = async (p, root) => {
  const t = (await GP.tests()).find(x => x.id === p[2]); if (!t) { root.innerHTML = '<div class="page"><p>Test not found.</p></div>'; return; }
  root.innerHTML = '<div class="loading">Loading the paper…</div>'; await GP.loadSubjects(t.u);
  const dryNow = S().dry, qs = t.q.map(id => GP.Q(id));
  let R = S().running[t.id];
  const secs = [...new Set(t.sec)], multi = secs.length > 1, tm = qs.reduce((a, q) => a + q.m, 0);
  const boot = () => { root.innerHTML = `<div class="page" style="max-width:680px"><div class="eyebrow">${t.k === 'full' ? 'Full GATE mock' : 'Subject test'}${R ? ' · resumed' : ''}</div><h1 class="h1" style="margin:var(--s1) 0">${esc(t.ti)}</h1>
    <div class="score" style="margin:var(--s3) 0"><div><b>${qs.length}</b><span>questions</span></div><div><b>${tm}</b><span>marks</span></div><div><b>${t.m}</b><span>minutes</span></div></div>
    <ul style="padding-left:20px;display:grid;gap:6px"><li>${multi ? secs.map(s => `${secName(s)}: ${t.sec.filter(x => x === s).length}`).join(' · ') : 'Single section'}</li><li>MCQ: negative marking ⅓ for 1-mark and ⅔ for 2-mark questions. MSQ and NAT: none.</li><li>Answers save automatically. You can leave and resume — the clock keeps running.</li>${S().dry ? '<li><b>Dry run:</b> tags and the question timer are hidden, as in the real exam.</li>' : ''}</ul>
    <div class="row wrap" style="margin-top:var(--s3)"><button class="btn pri" id="go">${R ? 'Resume test' : 'Start test'} →</button><a class="btn" href="#/tests">Back</a></div></div>`; $('#go').onclick = start; };
  let qstart = 0, tmr = null;
  const order = () => qs.map((q, i) => i).filter(i => t.sec[i] === R.sec);
  const cur = () => qs[R.order[R.pos]];
  const idOf = i => qs[i].i;
  const ans = id => R.ans[id] || (R.ans[id] = {});
  const has = id => { const a = R.ans[id]; return !!a && (a.sel && a.sel.length > 0 || a.num !== undefined && a.num !== ''); };
  const status = id => { const a = has(id), m = R.marked.includes(id); return a && m ? 'mk an' : a ? 'an' : m ? 'mk' : R.visited.includes(id) ? 'na' : 'nv'; };
  const stamp = () => { const q = cur(); if (!q) return; const a = ans(q.i); a.t = (a.t || 0) + Math.round((Date.now() - qstart) / 1000); qstart = Date.now(); };
  function start() {
    if (!R) R = S().running[t.id] = {title: t.ti, href: '#/test/' + t.id, kind: t.k, ans: {}, marked: [], visited: [], sec: secs[0], endAt: Date.now() + t.m * 60000, dry: dryNow, started: Date.now(), pos: 0};
    R.ts = Date.now(); R.order = order(); R.pos = Math.min(R.pos || 0, R.order.length - 1);
    runShell(root, {title: t.ti, sub: R.dry ? 'Dry run · exam conditions' : 'Exam mode', timer: true, tabs: multi, finishLabel: 'Submit test', finishPri: true, full: true, onFinish: summary, onExit: () => { stamp(); GP.save(); location.hash = '#/tests'; }});
    if (multi) { $('#rtabs').innerHTML = secs.map(s => `<button data-s="${s}" class="${s === R.sec ? 'on' : ''}">${esc(secName(s))}</button>`).join(''); $$('#rtabs button').forEach(b => b.onclick = () => setSec(b.dataset.s)); }
    qstart = Date.now();
    const tk = () => { const r = Math.round((R.endAt - Date.now()) / 1000); const el = $('#rtimer'); if (!el) return; el.textContent = hms(r); el.classList.toggle('low', r < 300); if (r <= 0) submit(); if (!R.dry) { const q = cur(), a = R.ans[q.i]; const e = $('#qt'); e && (e.textContent = 'This question ' + mmss(((a && a.t) || 0) + (Date.now() - qstart) / 1000)); } };
    clearInterval(tmr); tmr = setInterval(tk, 1000); tk(); GP.cleanup = () => { clearInterval(tmr); document.removeEventListener('keydown', keys); }; document.addEventListener('keydown', keys); draw();
  }
  function setSec(s) { stamp(); R.sec = s; R.order = order(); R.pos = 0; $$('#rtabs button').forEach(b => b.classList.toggle('on', b.dataset.s === s)); draw(); GP.save(); }
  function go(d) { stamp(); R.pos = Math.min(R.order.length - 1, Math.max(0, R.pos + d)); draw(); GP.save(); }
  function jump(pred) { stamp(); const all = []; secs.forEach(s => qs.forEach((q, i) => { if (t.sec[i] === s) all.push(i); })); const here = all.indexOf(R.order[R.pos]);
    for (let k = 1; k <= all.length; k++) { const j = all[(here + k) % all.length]; if (pred(qs[j])) { if (t.sec[j] !== R.sec) { R.sec = t.sec[j]; R.order = order(); $$('#rtabs button').forEach(b => b.classList.toggle('on', b.dataset.s === R.sec)); } R.pos = R.order.indexOf(j); draw(); GP.save(); return true; } } return false; }
  const keys = e => {
    if (/INPUT|TEXTAREA/.test((e.target || {}).tagName) || $('.sheetov') || e.ctrlKey || e.altKey || e.metaKey) return;
    if (e.key === 'ArrowRight') go(1); else if (e.key === 'ArrowLeft') go(-1);
    else {
      const q = cur(), k = '12345678'.indexOf(e.key) >= 0 ? '12345678'.indexOf(e.key) : 'abcdefgh'.indexOf(e.key.toLowerCase());
      if (q.y !== 'n' && k >= 0 && k < q.o.length) { const x = ans(q.i); x.sel = q.y === 'm' ? ((x.sel || []).includes(k) ? x.sel.filter(v => v !== k) : [...(x.sel || []), k]) : [k]; draw(); GP.save(); }
    }
  };
  function draw() {
    const q = cur(), a = R.ans[q.i] || {}, n = q.y === 'n', m = q.y === 'm'; if (!R.visited.includes(q.i)) R.visited.push(q.i);
    $('#rmain').innerHTML = `<div class="qpanel"><div class="qhead"><span>Question ${R.pos + 1} of ${R.order.length}${q.r && !R.dry ? ' · ' + esc(q.r) : ''}</span><span>${R.dry ? '' : `<span id="qt"></span> · ${esc(q.t)} · ${DIFF[q.d]} · `}${TYPE[q.y]} · ${mk(q)}</span></div>
      <div class="q"><div class="text">${fx(q.x)}</div>${n ? `<input class="nat" type="number" step="any" placeholder="Enter value" value="${a.num ?? ''}">` : q.o.map((o, i) => `<button class="opt ${m ? 'multi' : ''} ${(a.sel || []).includes(i) ? 'sel' : ''}" data-i="${i}"><span class="k">${m && (a.sel || []).includes(i) ? '✓' : LET[i]}</span><span>${fx(o)}</span></button>`).join('')}
      <p class="mut sm" style="margin-top:var(--s1)">${{s: 'Choose one option.', m: 'One or more options may be correct. Full marks only for the exact set.', n: 'Type a number. No negative marking.'}[q.y]}</p></div></div>
      <div class="acts"><button class="btn" id="bmk">Mark for review &amp; next</button><button class="btn" id="bclr">Clear response</button><button class="btn" id="bun">Next unanswered ⇥</button><span class="grow"></span><button class="btn" id="bprev">← Previous</button><button class="btn pri" id="bnext">Save &amp; next →</button></div>`;
    if (n) $('.nat').oninput = e => { ans(q.i).num = e.target.value; pal(); GP.save(); };
    else $$('.opt').forEach(b => b.onclick = () => { const i = +b.dataset.i, x = ans(q.i); x.sel = m ? ((x.sel || []).includes(i) ? x.sel.filter(v => v !== i) : [...(x.sel || []), i]) : [i]; draw(); GP.save(); });
    $('#bprev').onclick = () => go(-1); $('#bnext').onclick = () => go(1); $('#bmk').onclick = () => { if (!R.marked.includes(q.i)) R.marked.push(q.i); go(1); };
    $('#bclr').onclick = () => { delete R.ans[q.i]; draw(); GP.save(); }; $('#bun').onclick = () => { if (!jump(x => !has(x.i))) toast('Every question has an answer'); };
    typeset($('#rmain')); pal();
    if (!R.dry) { const a2 = R.ans[q.i], e = $('#qt'); e && (e.textContent = 'This question ' + mmss(((a2 && a2.t) || 0))); }
  }
  function pal() {
    $('#rpt').textContent = multi ? secName(R.sec) : 'Questions';
    $('#rgrid').innerHTML = R.order.map((i, k) => `<button class="pal ${status(idOf(i))} ${k === R.pos ? 'cur' : ''}" data-k="${k}">${k + 1}</button>`).join('');
    $$('#rgrid .pal').forEach(b => b.onclick = () => { stamp(); R.pos = +b.dataset.k; draw(); GP.save(); $('aside.pal-aside').classList.remove('open'); });
    $('#rleg').innerHTML = '<span><i style="background:var(--pal-ok)"></i>Answered</span><span><i style="background:var(--pal-no)"></i>Not answered</span><span><i style="background:var(--bg);border:1px solid var(--line2)"></i>Not visited</span><span><i style="background:var(--pal-mk);border-radius:50%"></i>Marked for review</span>';
    $('#rcnt').innerHTML = `<span>Answered <b>${R.order.filter(i => has(idOf(i))).length}</b> / ${R.order.length}</span>`;
  }
  function summary() {
    stamp(); const rows = secs.map(s => { const idx = qs.map((q, i) => i).filter(i => t.sec[i] === s); let A = 0, N = 0, V = 0, M = 0, T = 0; idx.forEach(i => { const id = idOf(i), st = status(id); if (st.includes('an')) A++; else if (st === 'na') N++; else if (st === 'nv') V++; if (R.marked.includes(id)) M++; T += (R.ans[id] || {}).t || 0; }); return `<tr><td>${esc(secName(s))}</td><td>${idx.length}</td><td style="color:var(--pal-ok)">${A}</td><td style="color:var(--pal-no)">${N}</td><td>${V}</td><td style="color:var(--pal-mk)">${M}</td><td>${mmss(T)}</td></tr>`; }).join('');
    const o = GP.sheet(`<h2 class="h2">Review before you submit</h2><div class="tw2"><table class="t"><tr><th>Section</th><th>Qs</th><th>Answered</th><th>Not answered</th><th>Not visited</th><th>Marked</th><th>Time</th></tr>${rows}</table></div>
      <div class="row wrap" style="margin:var(--s2) 0"><button class="btn sm" id="rUn">Go to unanswered</button><button class="btn sm" id="rMk">Go to marked</button></div><div class="row"><button class="btn pri" id="rOk" style="flex:1">Yes, submit</button><button class="btn" id="rNo" style="flex:1">Keep working</button></div>`);
    $('#rNo', o).onclick = () => o.remove(); $('#rOk', o).onclick = () => { o.remove(); submit(); };
    $('#rUn', o).onclick = () => { o.remove(); if (!jump(q => !has(q.i))) toast('Nothing left unanswered'); }; $('#rMk', o).onclick = () => { o.remove(); if (!jump(q => R.marked.includes(q.i))) toast('Nothing is marked for review'); };
  }
  function submit() {
    if (!R || R.done) return; R.done = true; stamp(); clearInterval(tmr); document.removeEventListener('keydown', keys);
    const items = qs.map(q => { const a = R.ans[q.i] || {}, got = has(q.i), st = got ? GP.judge(q, a.sel, a.num) : 'skip'; return {id: q.i, ok: st === 'ok', skipped: !got, t: a.t || 0, sec: t.sec[qs.indexOf(q)]}; });
    items.forEach(x => { if (!x.skipped) GP.record(GP.Q(x.id), x.ok, ''); });
    const score = items.reduce((a, x) => a + (x.skipped ? 0 : GP.marksFor(GP.Q(x.id), x.ok ? 'ok' : 'bad')), 0);
    S().tests.push({id: Date.now().toString(36), tid: t.id, title: t.ti, kind: t.k, when: today(), dry: R.dry, used: Math.max(0, Math.round(t.m * 60 - (R.endAt - Date.now()) / 1000)), minutes: t.m, items, score, max: tm});
    const d = S().done[t.id] || {best: -1e9, max: tm, n: 0}; d.best = Math.max(d.best, Math.round(score * 100) / 100); d.max = tm; d.n++; S().done[t.id] = d;
    delete S().running[t.id]; GP.save(); location.hash = '#/result/' + (S().tests.length - 1);
  }
  if (R && R.endAt - Date.now() <= 0) { R.order = order(); start(); submit(); return; }
  boot();
};

/* ---------- results ---------- */
V.result = async p => {
  const h = S().tests[+p[2]]; if (!h) return '<div class="page"><p>Result not found.</p></div>';
  const items = h.items || [], n = items.length, ans = items.filter(x => !x.skipped), acc = pct(ans.filter(x => x.ok).length, ans.length);
  const subs = [...new Set(items.map(x => (GP.qi[x.id] || {}).sub).filter(Boolean))];
  const tot = items.reduce((a, x) => a + x.t, 0), avg = tot / (n || 1) || 1, mx = Math.max(...items.map(x => x.t), 1);
  const num = x => items.indexOf(x) + 1;
  const slow = items.filter(x => x.t > avg * 1.6 && x.t > 20).sort((a, b) => b.t - a.t).slice(0, 3);
  const slowWrong = items.filter(x => !x.ok && !x.skipped && x.t > avg * 1.3), fastWrong = items.filter(x => !x.ok && !x.skipped && x.t < avg * 0.5 && tot > 0);
  const lines = [];
  if (slow.length) lines.push(['', `<b>Slowest:</b> ${slow.map(x => `Q${num(x)} (${mmss(x.t)}, ${(x.t / avg).toFixed(1)}× your average)`).join(', ')}. Decide earlier when to skip and come back.`]);
  if (slowWrong.length) lines.push(['no', `<b>Slow and wrong</b> (concept gap): ${slowWrong.slice(0, 8).map(x => 'Q' + num(x)).join(', ')}. Re-read the lesson for these.`]);
  if (fastWrong.length) lines.push(['no', `<b>Fast and wrong</b> (careless or guessing): ${fastWrong.slice(0, 8).map(x => 'Q' + num(x)).join(', ')}. Slow down and re-read the question.`]);
  if (!lines.length && tot) lines.push(['', 'Pacing was even and there were no obvious careless errors.']);
  const byTopic = {}; items.forEach(x => { const q = GP.qi[x.id]; if (!q) return; const k = q.sub + '|' + q.t; (byTopic[k] || (byTopic[k] = [0, 0]))[0]++; if (x.ok) byTopic[k][1]++; });
  const topicRows = Object.entries(byTopic).sort((a, b) => a[1][1] / a[1][0] - b[1][1] / b[1][0]).slice(0, 12);
  const missed = items.filter(x => !x.ok && !x.skipped).length;
  const compact = n > 40;      // 65-question mocks: show only the slowest 40 bars to keep the page short
  const shown = items.map((x, k) => [x, k]).filter(([x]) => !x.skipped || x.t > 0), bars = compact ? shown.sort((a, b) => b[0].t - a[0].t).slice(0, 25) : shown;
  return `<div class="page wide"><div class="eyebrow">${esc(h.title)} · ${h.when}${h.dry ? ' · dry run' : ''}</div><h1 class="h1" style="margin-top:var(--s1)">Results</h1>
   <div class="score"><div><b>${(+h.score).toFixed(2)}</b><span>score / ${h.max}</span></div><div><b>${acc ?? '—'}${acc !== null ? '%' : ''}</b><span>accuracy on attempted</span></div><div><b>${h.used ? mmss(h.used) : '—'}</b><span>${h.minutes ? 'of ' + h.minutes + ' min' : 'time taken'}</span></div><div><b>${items.filter(x => x.skipped).length}</b><span>unattempted</span></div></div>
   ${n && tot ? `<div class="cols"><div><h2 class="h2" style="margin-bottom:var(--s2)">Where the time went</h2><div class="tbars">${bars.map(([x, k]) => `<div class="tbar"><span>Q${k + 1}</span><div class="tr"><i class="${x.t > avg * 1.6 ? 'slow' : ''}" style="width:${100 * x.t / mx}%"></i><u style="left:${100 * avg / mx}%"></u></div><span>${mmss(x.t)}</span><span class="ck ${x.skipped ? '' : x.ok ? 'ok' : 'no'}">${x.skipped ? '–' : x.ok ? '✓' : '✗'}</span></div>`).join('')}</div>
    <p class="mut sm" style="margin-top:var(--s1)">${compact ? 'The 25 slowest questions. ' : ''}The dark line is your average (${mmss(avg)}). Amber bars took much longer than that.</p></div>
    <div><h2 class="h2" style="margin-bottom:var(--s2)">What to change</h2><div class="stack">${lines.map(l => `<p class="fb ${l[0]}">${l[1]}</p>`).join('')}</div>
    ${topicRows.length ? `<h2 class="h2" style="margin:var(--s3) 0 var(--s1)">Weakest topics here</h2>${topicRows.map(([k, v]) => { const [s, t] = k.split('|'); return `<div class="trow k2" style="padding:var(--s1) 0"><span>${esc(t)}<span class="sm mut"> · ${esc(s)}</span></span><span class="mono sm">${v[1]}/${v[0]}</span></div>`; }).join('')}` : ''}</div></div>` : (n ? '' : '<p class="mut">The detailed breakdown is not available for this older attempt.</p>')}
   <hr class="rule"><div class="row wrap">${missed ? '<a class="btn pri" href="#/review">Review the ' + missed + ' missed →</a>' : ''}<a class="btn ${missed ? '' : 'pri'}" href="#/tests">All tests</a><a class="btn" href="#/practice">Practice</a></div></div>`;
};
})();
