/* GATE Prep — core: helpers, saved state, data loading, shell, router, search, shortcuts. */
'use strict';
const GP = window.GP = {views: {}, loaded: {}, qi: {}, cache: {}};
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = t => String(t == null ? '' : t).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const pct = (a, b) => b ? Math.round(100 * a / b) : null;
const mmss = t => { t = Math.max(0, Math.round(t)); return (t / 60 | 0) + ':' + String(t % 60).padStart(2, '0'); };
const hms = t => { t = Math.max(0, t | 0); return String(t / 3600 | 0).padStart(2, '0') + ':' + String(t % 3600 / 60 | 0).padStart(2, '0') + ':' + String(t % 60).padStart(2, '0'); };
const iso = d => d.toLocaleDateString('en-CA');
const today = () => iso(new Date());
const addDays = n => iso(new Date(Date.now() + n * 864e5));
const LET = 'ABCDEFGH';
const STEPS = [1, 3, 7, 21], GOAL = 20;

/* ---------- text: ```code```, `code`, $$display$$, $inline$ ---------- */
function inline(s) {
  return esc(s).replace(/`([^`\n]+)`/g, '<code>$1</code>').replace(/\$(?=\S)([^$\n]+?)(?<=\S)\$/g, (m, x) => `<span class="tex" data-tex="${x}">${x}</span>`);
}
function fx(text) {
  const out = []; let last = 0; const re = /```(?:\w+)?\n?([\s\S]*?)```/g; let m;
  const plain = s => inline(s).replace(/\$\$([\s\S]+?)\$\$/g, (a, t) => `<div class="texd" data-tex="${t.trim()}">${t.trim()}</div>`);
  while ((m = re.exec(text))) { out.push(plain(text.slice(last, m.index))); out.push('<pre><code>' + esc(m[1].replace(/\n$/, '')) + '</code></pre>'); last = m.index + m[0].length; }
  out.push(plain(text.slice(last)));
  return out.join('');
}
const para = t => fx(t).split(/\n{2,}/).map(p => /^<(pre|div)/.test(p.trim()) ? p : '<p>' + p.replace(/\n/g, '<br>') + '</p>').join('').replace(/<p>(Concept|Method|Watch out):/g, '<p class="note"><span class="lab">$1</span>');
function typeset(root) {
  if (!window.katex || !root) return;
  $$('.tex', root).forEach(e => { try { katex.render(e.dataset.tex, e, {throwOnError: false}); } catch (_) {} });
  $$('.texd', root).forEach(e => { if (e.dataset.done) return; e.dataset.done = 1; try { katex.render(e.dataset.tex || e.textContent, e, {displayMode: true, throwOnError: false}); } catch (_) {} });
}
function toast(m) { const d = document.createElement('div'); d.className = 'toast'; d.textContent = m; document.body.appendChild(d); setTimeout(() => d.remove(), 2600); }
window.toast = toast;

/* ---------- saved state ---------- */
const KEY = 'gateprep:v1';
const blank = () => ({v: 1, theme: 'paper', size: 'md', density: 'comfortable', dry: false, subject: 'ALGO', days: {}, cnt: {}, credits: 0, solved: 0,
  acc: {}, qs: {}, review: {}, lessons: {}, tests: [], running: {}, done: {}, tab: {}});
let S = blank(), saveT = null;
GP.desktop = false;
function save() {
  clearTimeout(saveT);
  saveT = setTimeout(() => {
    const j = JSON.stringify(S);
    try { localStorage.setItem(KEY, j); } catch (e) {}
    if (GP.desktop) fetch('api/state', {method: 'PUT', headers: {'Content-Type': 'application/json'}, body: j}).catch(() => {});
  }, 250);
}
window.addEventListener('pagehide', () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} if (GP.desktop && navigator.sendBeacon) navigator.sendBeacon('api/state', new Blob([JSON.stringify(S)], {type: 'application/json'})); });
async function loadState() {
  let local = null;
  try { local = JSON.parse(localStorage.getItem(KEY)); } catch (e) {}
  try {
    const r = await fetch('api/state', {cache: 'no-store'});
    if (r.ok && /json/.test(r.headers.get('content-type') || '')) {
      GP.desktop = true; const d = await r.json();
      if (d && d.v) local = d;                       // the app's own database is the source of truth on the desktop
    }
  } catch (e) {}
  S = Object.assign(blank(), local || {});
  if (GP.desktop) save();
}
GP.save = save;
Object.defineProperty(GP, 'S', {get: () => S, set: v => { S = v; }});

/* ---------- data ---------- */
const J = p => GP.cache[p] || (GP.cache[p] = fetch(p).then(r => { if (!r.ok) { delete GP.cache[p]; throw new Error(p + ' ' + r.status); } return r.json(); }));
GP.json = J;
GP.subj = code => GP.meta.subjects.find(s => s.code === code);
GP.lessonsOf = code => GP.meta.lessons.filter(l => l.subject === code);
async function loadSubjects(codes) {
  await Promise.all(codes.filter(c => !GP.loaded[c]).map(async c => {
    const arr = await J('data/q/' + c + '.json'); arr.forEach(q => { q.sub = c; GP.qi[q.i] = q; }); GP.loaded[c] = 1;
  }));
}
GP.loadSubjects = loadSubjects;
GP.tests = async () => GP.testList || (GP.testList = await J('data/tests.json'));
const Qget = id => GP.qi[id];
GP.Q = Qget;

/* ---------- grading, credits, review queue ---------- */
function judge(q, sel, num) {
  if (q.y === 'n') { if (num === '' || num == null) return 'skip'; const v = parseFloat(num); return Math.abs(v - q.a) <= (q.tol || 0) + 1e-9 ? 'ok' : 'bad'; }
  if (!sel || !sel.length) return 'skip';
  return sel.slice().sort().join() === q.a.join() ? 'ok' : 'bad';
}
const marksFor = (q, st) => st === 'ok' ? q.m : st === 'bad' && q.y === 's' ? -(q.n || 0) : 0;
function record(q, ok, src) {
  const k = q.sub + '|' + q.t, a = S.acc[k] || (S.acc[k] = [0, 0]);
  a[0]++; if (ok) a[1]++; S.solved++;
  const c = ok ? ({e: 2, m: 4, h: 7}[q.d] || 3) : 1;
  S.credits += c; S.days[today()] = (S.days[today()] || 0) + c; S.cnt[today()] = (S.cnt[today()] || 0) + 1;
  const st = S.qs[q.i] || (S.qs[q.i] = [0, 0, '']); st[0]++; if (ok) st[1]++; st[2] = today();
  const r = S.review[q.i];
  if (src === 'review' && r) { r.stage = ok ? Math.min(3, r.stage + 1) : 0; r.due = addDays(STEPS[r.stage]); }
  else if (!ok && !r) S.review[q.i] = {stage: 0, due: addDays(1)};
  save(); return c;
}
GP.judge = judge; GP.marksFor = marksFor; GP.record = record;
const dueIds = () => Object.entries(S.review).filter(([, r]) => r.due <= today()).map(([id]) => id);
GP.dueIds = dueIds;
const streak = () => { let n = 0, d = new Date(); if (!S.days[iso(d)]) d = new Date(d.getTime() - 864e5); while (S.days[iso(d)]) { n++; d = new Date(d.getTime() - 864e5); } return n; };
GP.streak = streak;
const topicStat = (sub, topic) => { const a = S.acc[sub + '|' + topic] || [0, 0]; return {n: a[0], c: a[1], acc: pct(a[1], a[0])}; };
const subjStat = sub => { let n = 0, c = 0; Object.entries(S.acc).forEach(([k, v]) => { if (k.startsWith(sub + '|')) { n += v[0]; c += v[1]; } }); return {n, c, acc: pct(c, n)}; };
GP.topicStat = topicStat; GP.subjStat = subjStat;

/* ---------- prefs, sheets, window ---------- */
function applyPrefs() { const r = document.documentElement; r.dataset.theme = S.theme; r.dataset.size = S.size; r.dataset.density = S.density; }
const THEMES = [['paper', 'Paper'], ['sepia', 'Sepia'], ['mist', 'Mist'], ['forest', 'Forest'], ['slate', 'Slate (dark)'], ['midnight', 'Midnight (dark)']];
const setPref = (k, v) => { S[k] = v; save(); applyPrefs(); };
function sheet(html, cls = '') {
  $$('.sheetov').forEach(x => x.remove());
  const o = document.createElement('div'); o.className = 'sheetov ' + cls; o.innerHTML = `<div class="sheet">${html}</div>`; document.body.appendChild(o);
  o.onmousedown = e => { if (e.target === o) o.remove(); };
  return o;
}
GP.sheet = sheet;
const inShell = () => window.pywebview && window.pywebview.api;
function fullscreen() {
  if (inShell() && window.pywebview.api.toggle_fullscreen) return window.pywebview.api.toggle_fullscreen();
  if (document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen && document.documentElement.requestFullscreen().catch(() => {});
}
function quit() { const o = sheet('<h2 class="h2">Exit GATE Prep?</h2><p class="mut">Your progress is saved automatically.</p><div class="row" style="margin-top:24px;justify-content:flex-end"><button class="btn" data-x="no">Stay</button><button class="btn pri" data-x="yes">Exit</button></div>'); $('[data-x=no]', o).onclick = () => o.remove(); $('[data-x=yes]', o).onclick = () => { save(); inShell() && window.pywebview.api.quit ? window.pywebview.api.quit() : window.close(); }; }
function exportProgress() {
  const b = new Blob([JSON.stringify(S)], {type: 'application/json'}), a = document.createElement('a');
  a.href = URL.createObjectURL(b); a.download = 'gateprep-progress-' + today() + '.json'; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 4000);
}
function importProgress() {
  const i = document.createElement('input'); i.type = 'file'; i.accept = 'application/json,.json';
  i.onchange = async () => { try { const d = JSON.parse(await i.files[0].text()); if (!d || !d.v) throw 0; S = Object.assign(blank(), d); save(); applyPrefs(); toast('Progress imported'); route(); } catch (e) { toast('That file is not a GATE Prep progress file'); } };
  i.click();
}
function resetAll() { if (confirm('Erase ALL progress on this device? Export a backup first if unsure.')) { S = blank(); save(); applyPrefs(); location.hash = '#/home'; route(); toast('Progress erased'); } }
function subjectSheet() {
  const o = sheet('<h2 class="h2">Subject</h2><div class="opts">' + GP.meta.subjects.map(s => {
    const n = GP.lessonsOf(s.code).length; return `<button data-s="${s.code}" class="${s.code === S.subject ? 'on' : ''}"><span>${esc(s.name)}</span><span class="mut sm">${n} lesson${n === 1 ? '' : 's'}</span></button>`;
  }).join('') + '</div>');
  $$('button', o).forEach(b => b.onclick = () => { S.subject = b.dataset.s; save(); o.remove(); const h = location.hash; if (/^#\/(lesson|drill|dpp)/.test(h)) location.hash = '#/learn'; else route(); });
}
function menuSheet() {
  const sz = {sm: 'Small', md: 'Default', lg: 'Large', xl: 'Extra large'};
  const o = sheet(`<h2 class="h2">Menu</h2><div class="opts">
    <div class="eyebrow" style="padding:8px 12px 4px">Theme</div>${THEMES.map(([k, n]) => `<button data-t="${k}" class="${S.theme === k ? 'on' : ''}"><span>${n}</span><span>${S.theme === k ? '✓' : ''}</span></button>`).join('')}<hr>
    <button data-a="size"><span>Text size</span><span class="mut">${sz[S.size]} →</span></button>
    <button data-a="density"><span>Spacing</span><span class="mut">${S.density === 'compact' ? 'Compact' : 'Comfortable'} →</span></button>
    <button data-a="dry"><span>Exam-day dry run for tests</span><span class="mut">${S.dry ? 'On' : 'Off'}</span></button>
    <button data-a="full"><span>Full screen</span><span class="kbd">F11</span></button><hr>
    <button data-a="exp"><span>Export progress</span><span class="mut">backup / move to another device</span></button>
    <button data-a="imp"><span>Import progress</span></button>
    <button data-a="reset"><span style="color:var(--bad)">Erase progress on this device</span></button>
    ${inShell() ? '<hr><button data-a="quit"><span>Exit app</span><span class="kbd">Ctrl Q</span></button>' : ''}
    <hr><div class="mut sm" style="padding:8px 12px">GATE Prep ${esc(GP.meta.version)} · ${GP.meta.questions.toLocaleString()} questions · ${GP.meta.lessons.length} lessons · ${GP.desktop ? 'desktop app' : 'web'}</div></div>`);
  $$('button[data-t]', o).forEach(b => b.onclick = () => { setPref('theme', b.dataset.t); o.remove(); menuSheet(); });
  $$('button[data-a]', o).forEach(b => b.onclick = () => {
    const a = b.dataset.a;
    if (a === 'size') { setPref('size', {md: 'lg', lg: 'xl', xl: 'sm', sm: 'md'}[S.size]); o.remove(); menuSheet(); }
    else if (a === 'density') { setPref('density', S.density === 'compact' ? 'comfortable' : 'compact'); o.remove(); menuSheet(); }
    else if (a === 'dry') { setPref('dry', !S.dry); o.remove(); menuSheet(); }
    else { o.remove(); ({full: fullscreen, exp: exportProgress, imp: importProgress, reset: resetAll, quit})[a](); }
  });
}
GP.menu = menuSheet; GP.fullscreen = fullscreen;

/* ---------- search (Ctrl+K) ---------- */
function cmdk() {
  const items = [['Page', 'Home', '#/home'], ['Page', 'Learn', '#/learn'], ['Page', 'Practice', '#/practice'], ['Page', 'Review due questions', '#/review'], ['Page', 'Tests and mock exams', '#/tests'], ['Page', 'Progress', '#/progress'],
    ...GP.meta.subjects.flatMap(s => [['Subject', s.name, 'subject:' + s.code], ...s.topics.map((t, i) => ['Drill', `${s.name} — ${t}`, `#/drill/${s.code}/${i}`])]),
    ...GP.meta.lessons.map(l => ['Lesson', `${l.title}`, '#/lesson/' + l.slug, GP.subj(l.subject).name + ' ' + l.topic]),
    ['Action', 'Full screen', fullscreen], ['Action', 'Menu and settings', menuSheet]];
  const o = sheet('<input placeholder="Search lessons, topics, subjects…" autocomplete="off" spellcheck="false"><ul></ul>', 'cmd');
  const inp = $('input', o), ul = $('ul', o); let hits = [], c = 0;
  const draw = () => { ul.innerHTML = hits.map((h, i) => `<li class="${i === c ? 'on' : ''}" data-i="${i}"><span class="k">${h[0]}</span><span>${esc(h[1])}</span></li>`).join('') || '<li class="mut">No matches</li>'; const e = $('li.on', ul); e && e.scrollIntoView({block: 'nearest'}); };
  const filt = () => { const w = inp.value.toLowerCase().split(/\s+/).filter(Boolean); hits = items.filter(h => w.every(x => (h[0] + ' ' + h[1] + ' ' + (h[3] || '')).toLowerCase().includes(x))).slice(0, 40); c = 0; draw(); };
  const run = i => { const h = hits[i]; if (!h) return; o.remove(); if (typeof h[2] === 'function') h[2](); else if (h[2].startsWith('subject:')) { S.subject = h[2].slice(8); save(); location.hash = '#/learn'; route(); } else location.hash = h[2]; };
  inp.oninput = filt; ul.onclick = e => { const li = e.target.closest('li[data-i]'); if (li) run(+li.dataset.i); };
  inp.onkeydown = e => { if (e.key === 'ArrowDown') { e.preventDefault(); c = Math.min(hits.length - 1, c + 1); draw(); } else if (e.key === 'ArrowUp') { e.preventDefault(); c = Math.max(0, c - 1); draw(); } else if (e.key === 'Enter') run(c); };
  filt(); inp.focus();
}
GP.search = cmdk;
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') $$('.sheetov').forEach(x => x.remove());
  if (e.ctrlKey && !e.shiftKey && e.key.toLowerCase() === 'k') { e.preventDefault(); cmdk(); }
  if (e.ctrlKey && !e.shiftKey && e.key.toLowerCase() === 'q' && inShell()) { e.preventDefault(); quit(); }
  if (e.key === 'F11' && !GP.locked) { e.preventDefault(); fullscreen(); }
  if (e.altKey && e.key === 'ArrowLeft') { e.preventDefault(); history.back(); }
  if (e.altKey && /^[1-5]$/.test(e.key) && !GP.locked) { e.preventDefault(); location.hash = ['#/home', '#/learn', '#/practice', '#/tests', '#/progress'][+e.key - 1]; }
});

/* ---------- shell ---------- */
const NAV = [['home', 'Home', '#/home'], ['learn', 'Learn', '#/learn'], ['practice', 'Practice', '#/practice'], ['tests', 'Tests', '#/tests'], ['progress', 'Progress', '#/progress']];
function sectionOf(h) { const p = (h || '#/home').split('/')[1] || 'home'; return {lesson: 'learn', review: 'practice', drill: 'practice', dpp: 'practice', result: 'tests', test: 'tests'}[p] || p; }
function chrome() {
  const sec = sectionOf(location.hash), due = dueIds().length, sj = GP.subj(S.subject);
  $('#rail').innerHTML = `<a class="logo" href="#/home"><b>GP</b> GATE Prep</a>
    <button class="subjbtn" id="subjBtn"><span><small>Subject</small>${esc(sj.name)}</span><span>▾</span></button>
    <nav class="nav">${NAV.map(([k, n, h]) => `<a href="${h}" class="${sec === k ? 'on' : ''}">${n}${k === 'practice' && due ? `<span class="n">${due}</span>` : ''}</a>`).join('')}</nav>
    <div class="grow"></div><div class="status">${streak()}-day streak · ${S.cnt[today()] || 0}/${GOAL} today</div>
    <button class="railbtn" id="menuBtn">⋯ &nbsp;Menu</button>`;
  $('#tabbar').innerHTML = NAV.map(([k, n, h]) => `<a href="${h}" class="${sec === k ? 'on' : ''}">${n}${k === 'practice' && due ? `<span class="n">${due}</span>` : ''}</a>`).join('');
  $('#subjBtn').onclick = subjectSheet; $('#menuBtn').onclick = menuSheet;
  $('#mSubj').textContent = sj.code;
}
GP.chrome = chrome;

/* ---------- router ---------- */
let after = null;
function crumbs(p) {
  const sj = GP.subj(S.subject).name, c = {home: ['Home'], learn: [sj, 'Learn'], practice: [sj, 'Practice'], review: ['Practice', 'Review'], tests: ['Tests'], progress: ['Progress'], result: ['Tests', 'Results'], drill: ['Practice', 'Drill'], dpp: ['Practice', 'DPP'], lesson: [sj, 'Learn', (GP.meta.lessons.find(l => l.slug === p[2]) || {}).title || 'Lesson']}[p[1]] || ['Home'];
  return `<span class="cr">${c.slice(0, -1).map(esc).join(' › ')}${c.length > 1 ? ' › ' : ''}</span><b>${esc(c[c.length - 1])}</b>`;
}
GP.rid = 0;
async function route() {
  const my = ++GP.rid;
  window.onscroll = null; GP.cleanup && GP.cleanup(); GP.cleanup = null; GP.locked = false;
  const h = location.hash || '#/home', p = h.split('/');
  const full = GP.views.full && GP.views.full[p[1]];
  if (full) { $('#shell').hidden = true; const rt = $('#run'); rt.hidden = false; await full(p, rt); return; }
  $('#run').hidden = true; $('#run').innerHTML = ''; $('#shell').hidden = false;
  chrome();
  const f = GP.views[p[1]] || GP.views.home, v = $('#view');
  v.innerHTML = '<div class="loading">Loading…</div>';
  try {
    const html = await f(p);
    if (my !== GP.rid) return;                                                                          // navigated away while loading
    v.innerHTML = html; $('#crumbs').innerHTML = crumbs(p); $('#back').hidden = !p[1] || p[1] === 'home';
    typeset(v); const a = GP.after; GP.after = null; a && a(v);
    if (p[1] !== 'lesson') scrollTo(0, 0);
  } catch (e) { console.error(e); v.innerHTML = `<div class="page"><div class="err"><b>Could not load this page.</b><p class="mut">${esc(e.message)}. If you are offline, open it once while connected so it can be saved for later.</p></div></div>`; }
}
GP.route = route;

async function boot() {
  document.body.insertAdjacentHTML('afterbegin', `<div id="shell" class="shell"><aside class="rail" id="rail"></aside><div class="main"><header class="top">
    <button class="ghost" id="back" hidden>← Back</button><button class="ghost only-m" id="mSubj" title="Subject"></button><div class="crumbs" id="crumbs"></div>
    <button class="ghost" id="srch" title="Search (Ctrl+K)"><span class="only-m">⌕ Search</span><span class="only-d">Search <span class="kbd" style="margin-left:6px">Ctrl K</span></span></button><button class="ghost only-m" id="mMenu">⋯</button></header>
    <div id="view"></div></div><nav class="tabbar" id="tabbar"></nav></div><div id="run" hidden></div>`);
  $('#back').onclick = () => { if (history.length > 1) history.back(); else location.hash = '#/home'; };
  $('#srch').onclick = cmdk; $('#mMenu').onclick = () => menuSheet(); $('#mSubj').onclick = () => subjectSheet();
  await loadState(); applyPrefs();
  try { GP.meta = await J('data/meta.json'); } catch (e) { document.body.innerHTML = '<div class="page"><div class="err"><b>Content could not be loaded.</b><p class="mut">Check your connection and reload.</p></div></div>'; return; }
  if (!GP.subj(S.subject)) S.subject = 'ALGO';
  window.addEventListener('hashchange', route);
  if ('serviceWorker' in navigator && location.protocol.startsWith('http') && !GP.desktop) navigator.serviceWorker.register('sw.js').catch(() => {});
  route();
}
document.addEventListener('DOMContentLoaded', () => setTimeout(boot, 0));
