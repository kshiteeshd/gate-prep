/* GATE Prep — screens: home, learn, lesson, practice, tests, progress. */
'use strict';
(() => {
const V = GP.views;
const S = () => GP.S;
const lessonDone = slug => !!(S().lessons[slug] && S().lessons[slug].done);

/* ---------- what to do next ---------- */
function nextLesson(sub) {
  const ls = GP.lessonsOf(sub); if (!ls.length) return null;
  let start = 0;
  const last = Object.entries(S().lessons).filter(([k, v]) => v.done && ls.some(l => l.slug === k)).sort((a, b) => (b[1].done > a[1].done ? 1 : -1))[0];
  if (last) start = ls.findIndex(l => l.slug === last[0]) + 1;
  return [...ls.slice(start), ...ls.slice(0, start)].find(l => !lessonDone(l.slug)) || null;
}
function weakest(sub) {
  const sj = GP.subj(sub);
  const r = sj.topics.map((t, i) => ({t, i, ...GP.topicStat(sub, t)}));
  const tried = r.filter(x => x.n >= 3).sort((a, b) => a.acc - b.acc)[0];
  return tried || r.find(x => !x.n) || r[0];
}
function running() { const e = Object.entries(S().running).filter(([, r]) => r && r.href).sort((a, b) => (b[1].ts || 0) - (a[1].ts || 0))[0]; return e ? e[1] : null; }
function nextAction() {
  const sub = S().subject, due = GP.dueIds().length, run = running(), nl = nextLesson(sub), w = weakest(sub);
  if (run) return {e: 'In progress', t: run.title, p: 'Your answers are saved' + (run.endAt ? ' and the clock keeps running.' : '. Pick up where you stopped.'), b: 'Resume', h: run.href};
  if (due) return {e: 'Due today', t: `Review ${due} question${due > 1 ? 's' : ''}`, p: 'Questions you missed come back after 1, 3, 7 and 21 days. A few minutes now saves a re-read later.', b: 'Start review', h: '#/review'};
  if (nl) { const started = GP.lessonsOf(sub).some(l => lessonDone(l.slug)); return {e: started ? 'Next lesson' : 'Start here', t: nl.title, p: `${GP.subj(sub).name} · chapter ${nl.ch_no}, ${nl.chapter}. About ${nl.minutes} minutes.`, b: started ? 'Continue lesson' : 'Start lesson', h: '#/lesson/' + nl.slug}; }
  return {e: 'Drill', t: w.t, p: 'Your weakest topic right now. Ten minutes of drills moves it the most.', b: 'Drill this topic', h: `#/drill/${sub}/${w.i}`};
}
V.home = async () => {
  const a = nextAction(), sub = S().subject, due = GP.dueIds().length, nl = nextLesson(sub), w = weakest(sub), also = [];
  if (due && a.h !== '#/review') also.push(['#/review', `Review ${due} due question${due > 1 ? 's' : ''}`, 'Practice']);
  if (nl && a.h !== '#/lesson/' + nl.slug) also.push(['#/lesson/' + nl.slug, 'Next lesson: ' + nl.title, nl.minutes + ' min']);
  if (w && w.n >= 3 && w.acc < 70 && a.h !== `#/drill/${sub}/${w.i}`) also.push([`#/drill/${sub}/${w.i}`, 'Drill: ' + w.t, w.acc + '% accuracy']);
  also.push(['#/tests', 'Take a test or a full mock', 'Tests']);
  const tot = Object.values(S().acc).reduce((x, v) => [x[0] + v[0], x[1] + v[1]], [0, 0]);
  return `<div class="page"><div class="next"><div class="eyebrow">${esc(a.e)}</div><h1 class="h1">${esc(a.t)}</h1><p>${esc(a.p)}</p><a class="btn pri" href="${a.h}">${esc(a.b)} →</a></div>
   <div class="eyebrow" style="margin-bottom:var(--s1)">Also</div><div class="also">${also.slice(0, 3).map(x => `<a href="${x[0]}"><span>${esc(x[1])}</span><span>${esc(x[2])}</span></a>`).join('')}</div>
   <div class="stats"><span><b>${GP.streak()}</b> day streak</span><span><b>${S().cnt[today()] || 0}/${GOAL}</b> today</span><span><b>${S().solved}</b> solved</span><span><b>${tot[0] ? pct(tot[1], tot[0]) + '%' : '—'}</b> accuracy</span></div></div>`;
};

/* ---------- learn: chapters and lessons ---------- */
V.learn = async () => {
  const sub = S().subject, sj = GP.subj(sub), ls = GP.lessonsOf(sub), f = S().tab.learn || 'all';
  if (!ls.length) return `<div class="page"><h1 class="h1">${esc(sj.name)}</h1><p class="mut" style="margin-top:var(--s2)">Lessons for this subject are on the way. You can already practise it.</p><p style="margin-top:var(--s2)"><a class="btn pri" href="#/practice">Go to practice →</a></p></div>`;
  const nl = nextLesson(sub), done = ls.filter(l => lessonDone(l.slug)).length;
  const chapters = [...new Set(ls.map(l => l.ch_no))].map(n => ({n, name: ls.find(l => l.ch_no === n).chapter, ls: ls.filter(l => l.ch_no === n).filter(l => f === 'all' || (f === 'todo' ? !lessonDone(l.slug) : lessonDone(l.slug)))})).filter(c => c.ls.length);
  return `<div class="page"><h1 class="h1">${esc(sj.name)}</h1><p class="mut" style="margin-top:var(--s1)">${ls.length} lessons · about ${Math.round(ls.reduce((a, l) => a + l.minutes, 0) / 60 * 10) / 10} hours · ${done} finished</p>
   <div class="bar" style="margin-top:var(--s2)"><i style="width:${pct(done, ls.length)}%"></i></div>
   <div class="tabs">${[['all', 'All'], ['todo', 'To do'], ['done', 'Finished']].map(([k, n]) => `<button data-f="${k}" class="${f === k ? 'on' : ''}">${n}</button>`).join('')}</div>
   ${chapters.map(c => `<div class="chapter"><div class="eyebrow">Chapter ${c.n} · ${esc(c.name)}</div>${c.ls.map(l => `<a class="lrow" href="#/lesson/${l.slug}"><span class="dot ${lessonDone(l.slug) ? 'done' : ''}">${lessonDone(l.slug) ? '✓' : ''}</span>
      <span><b>${esc(l.title)}</b><span class="sm mut">${l.minutes} min · ${esc(l.topic)}${l.widget !== 'none' ? ' · interactive' : ''}</span></span>
      <span class="btn sm ${nl && nl.slug === l.slug ? 'pri' : ''}">${lessonDone(l.slug) ? 'Read again' : nl && nl.slug === l.slug ? (done ? 'Continue' : 'Start') : 'Open'}</span></a>`).join('')}</div>`).join('') || '<p class="mut" style="margin-top:var(--s3)">Nothing here.</p>'}</div>`;
};
GP.after = null;
const learnAfter = v => $$('.tabs button', v).forEach(b => b.onclick = () => { S().tab.learn = b.dataset.f; GP.save(); GP.route(); });

/* ---------- lesson ---------- */
const WIDGET_JS = ['learn', 'learn_cs', 'learn_dbos', 'learn_hw', 'learn_net', 'learn_toc'];
function loadScript(src) { return new Promise((res, rej) => { const s = document.createElement('script'); s.src = src; s.onload = res; s.onerror = rej; document.head.appendChild(s); }); }
async function ensureWidgets() { if (GP.widgetsReady) return; for (const n of WIDGET_JS) await loadScript('js/widgets/' + n + '.js'); GP.widgetsReady = true; }
function seeded(str) { let h = 2166136261; for (const c of str) h = Math.imul(h ^ c.charCodeAt(0), 16777619); return () => { h = Math.imul(h ^ h >>> 15, 2246822507); h = Math.imul(h ^ h >>> 13, 3266489909); return ((h ^= h >>> 16) >>> 0) / 4294967296; }; }
async function lessonPractice(l) {
  await GP.loadSubjects([l.subject]);
  const subs = l.subs || [], all = Object.values(GP.qi).filter(q => q.sub === l.subject && q.t === l.topic && q.p === 'dpp'), rng = seeded(l.slug);
  const own = subs.length ? all.filter(q => subs.includes(q.s)) : [], pool = own.length >= 6 ? own : all, N = own.length >= 6 ? 8 : 5;
  const by = {e: [], m: [], h: []}; pool.forEach(q => by[q.d].push(q)); Object.values(by).forEach(a => a.sort(() => rng() - .5));
  const pick = N === 8 ? [...by.e.slice(0, 3), ...by.m.slice(0, 3), ...by.h.slice(0, 2)] : [...by.e.slice(0, 2), ...by.m.slice(0, 2), ...by.h.slice(0, 1)];
  return pick.length < N ? [...pick, ...pool.filter(q => !pick.includes(q)).sort(() => rng() - .5)].slice(0, N) : pick;
}
V.lesson = async p => {
  const l = await GP.json('data/lesson/' + p[2] + '.json');
  if (S().subject !== l.subject) { S().subject = l.subject; GP.save(); GP.chrome(); }
  const prac = await lessonPractice(l), secs = [];
  const sec = (id, h, body) => { secs.push([id, h]); return `<section class="sec" id="${id}"><h2 class="h2">${esc(h)}</h2>${body}</section>`; };
  let html = `<div class="read"><i id="readbar"></i></div><div class="page wide"><div class="lesson"><article><div class="eyebrow">Chapter ${l.ch_no} · ${esc(l.chapter)} · ${l.minutes} min · GATE weight ${'★'.repeat(l.weight)}${'☆'.repeat(5 - l.weight)}</div>
   <h1 class="h1" style="margin:var(--s1) 0 var(--s2)">${esc(l.title)}</h1><div class="tocm"><details><summary>Contents</summary><div id="tocm" class="stack" style="padding:var(--s1) 0"></div></details></div>`;
  html += sec('s-idea', 'The idea in one line', `<div class="callout key"><span class="t">Key idea</span>${l.key}</div>` + (l.analogy ? `<div class="analogy"><span class="em">${l.analogy[0]}</span><div><b>${esc(l.analogy[1])}</b><div class="mut">${l.analogy[2]}</div></div></div>` : ''));
  if (l.book.length) html += sec('s-book', 'Learn it from scratch', `<p class="mut">Read this part top to bottom like a textbook chapter. Nothing is assumed — new terms are explained where they first appear.</p><div class="book">${l.book.map(b => `<h3 class="bk">${esc(b[0])}</h3>${b[1]}`).join('')}</div>`);
  l.sections.forEach((s, i) => { html += sec('s-' + (i + 1), s.h, s.html + s.formulas.map(f => `<div class="formula"><div class="texd" data-tex="${esc(f[0])}">${esc(f[0])}</div>${f[1] ? `<small>${esc(f[1])}</small>` : ''}</div>`).join('') + s.call.map(c => `<div class="callout ${c[0]}"><span class="t">${esc(c[1])}</span>${c[2]}</div>`).join('')); });
  if (l.widget !== 'none') html += sec('s-try', 'Try it yourself', (l.hint ? `<p class="mut">${esc(l.hint)}</p>` : '') + `<div class="wgt" data-w="${l.widget}"></div>`);
  if (l.examples.length) html += sec('s-ex', 'Worked examples', l.examples.map((e, i) => `<div style="margin:var(--s2) 0"><div class="eyebrow">Example ${i + 1}</div><b>${esc(e.title)}</b>${e.problem}<details><summary>Show the solution step by step</summary><ol class="steps">${e.steps.map(s => `<li><div>${s}</div></li>`).join('')}</ol><div class="callout tip"><span class="t">Answer</span>${e.answer}</div></details></div>`).join(''));
  if (l.proofs.length) html += sec('s-proofs', 'Proofs and derivations', l.proofs.map(x => `<div class="deep"><h3>${esc(x[0])}</h3>${x[1]}</div>`).join(''));
  if (l.notes.length) html += sec('s-notes', 'Detailed notes', l.notes.map(x => `<div class="deep"><h3>${esc(x[0])}</h3>${x[1]}</div>`).join(''));
  if (l.traps.length) html += sec('s-traps', 'Common mistakes (GATE traps)', l.traps.map(t => `<div class="callout trap"><span class="t">${esc(t[0])}</span>${t[1]}</div>`).join(''));
  if (l.quick.length) html += sec('s-quick', 'Quick check', '<p class="mut">Instant questions to lock the idea in.</p>' + l.quick.map((q, i) => `<div class="check quick" data-i="${i}"><b>${q[0]}</b><div style="margin-top:var(--s1)">${q[1].map((o, k) => `<button class="opt" data-k="${k}"><span class="k">${LET[k]}</span><span>${esc(o)}</span></button>`).join('')}</div><div class="fbq"></div></div>`).join(''));
  html += sec('s-practice', 'GATE-level practice', prac.length ? prac.map((q, i) => `<div class="check" id="pq-${i}"></div>`).join('') : '<p class="mut">No practice questions for this topic yet.</p>');
  html += sec('s-sum', 'Summary — cheat sheet', `<ul>${l.summary.map(b => `<li>${b}</li>`).join('')}</ul>
   <div class="fin"><div class="row sp wrap"><div><b>Finished this topic?</b><div class="mut sm">Mark it complete to earn 20 credits.</div></div><button class="btn pri" id="complete">${lessonDone(l.slug) ? '✓ Completed' : 'Mark as complete'}</button></div></div>`);
  const ls = GP.lessonsOf(l.subject), i = ls.findIndex(x => x.slug === l.slug), pv = ls[i - 1], nx = ls[i + 1];
  html += `<div class="pn">${pv ? `<a class="btn" href="#/lesson/${pv.slug}">← ${esc(pv.title)}</a>` : '<span></span>'}${nx ? `<a class="btn pri" href="#/lesson/${nx.slug}">Next: ${esc(nx.title)} →</a>` : ''}</div></article>
   <nav class="toc">${secs.map(s => `<a data-s="${s[0]}">${esc(s[1])}</a>`).join('')}</nav></div></div>`;
  GP.after = async v => {
    const L = S().lessons[l.slug] || (S().lessons[l.slug] = {}), art = $('article', v);
    $('#tocm', v).innerHTML = secs.map(s => `<a class="link" data-s="${s[0]}">${esc(s[1])}</a>`).join('');
    $$('[data-s]', v).forEach(a => a.onclick = () => { $('#' + a.dataset.s).scrollIntoView({behavior: 'smooth'}); const d = $('.tocm details', v); d && (d.open = false); });
    $$('.quick', art).forEach(card => { const q = l.quick[+card.dataset.i]; $$('.opt', card).forEach(b => b.onclick = () => {
      if (card.dataset.done) return; card.dataset.done = 1; const ok = +b.dataset.k === q[2];
      $$('.opt', card).forEach((x, k) => { x.disabled = true; if (k === q[2]) x.classList.add('right'); else if (x === b) x.classList.add('wrong'); });
      $('.fbq', card).innerHTML = `<div class="fb ${ok ? 'ok' : 'no'}"><p><b class="${ok ? 'ok' : 'no'}">${ok ? 'Correct' : 'Not quite'}</b></p><p>${esc(q[3])}</p></div>`; }); });
    prac.forEach((q, k) => GP.mountQ($('#pq-' + k, art), q, {src: 'lesson', label: `Question ${k + 1} of ${prac.length}`}));
    $('#complete', v).onclick = e => { if (L.done) { toast('Already completed'); return; } L.done = today(); S().credits += 20; S().days[today()] = (S().days[today()] || 0) + 20; GP.save(); e.target.textContent = '✓ Completed'; toast('Lesson complete: +20 credits'); GP.chrome(); };
    typeset(art);
    if (l.widget !== 'none') { try { await ensureWidgets(); const el = $('.wgt', v), f = window.LW_W && window.LW_W[l.widget]; f ? f(el) : el.innerHTML = '<p class="mut">This tool is not available.</p>'; typeset(el); } catch (e) { console.error(e); } }
    const bar = $('#readbar'), tocs = $$('.toc a', v), secEls = secs.map(s => $('#' + s[0]));
    const upd = () => {
      const h = document.documentElement.scrollHeight - innerHeight; bar.style.width = (h > 0 ? 100 * scrollY / h : 0) + '%';
      let cur = secs[0][0]; secEls.forEach((e, k) => { if (e.getBoundingClientRect().top < 140) cur = secs[k][0]; }); tocs.forEach(a => a.classList.toggle('on', a.dataset.s === cur));
      L.y = Math.round(scrollY); clearTimeout(upd.t); upd.t = setTimeout(() => GP.save(), 500);
    };
    window.onscroll = upd;
    const want = p[3] != null ? $('#s-' + (+p[3] || 1)) : null;
    if (want) setTimeout(() => scrollTo({top: want.offsetTop - 60}), 60);
    else if (L.y > 400) setTimeout(() => { scrollTo(0, L.y); toast('Resumed where you left off'); }, 120);
    upd();
  };
  return html;
};

/* ---------- practice ---------- */
V.practice = async () => {
  const sub = S().subject, sj = GP.subj(sub), tests = (await GP.tests()).filter(t => t.k === 'dpp' && t.s === sub), due = GP.dueIds().length;
  const by = [0, 1, 2, 3].map(i => Object.values(S().review).filter(r => r.stage === i));
  const nextDue = Object.values(S().review).map(r => r.due).filter(d => d > today()).sort()[0];
  return `<div class="page"><h1 class="h1">Practice</h1><p class="mut" style="margin-top:var(--s1)">${esc(sj.name)} · spaced review is shared across all subjects</p>
   <div class="tiers">${STEPS.map((d, i) => `<div class="${by[i].some(r => r.due <= today()) ? 'due' : ''}"><b>${by[i].length}</b>every ${d} day${d > 1 ? 's' : ''}</div>`).join('')}</div>
   <div>${due ? `<a class="btn pri" href="#/review">Review ${due} due →</a>` : `<span class="mut">Nothing due${nextDue ? ' — next on ' + nextDue : ' — questions you miss will appear here'}.</span>`}</div>
   <hr class="rule"><div class="eyebrow">Topics</div>
   ${sj.topics.map((t, i) => { const st = GP.topicStat(sub, t), dp = tests.filter(x => x.t === t).sort((a, b) => a.n - b.n);
     return `<div style="border-bottom:1px solid var(--line);padding:var(--s2) 0"><div class="row sp wrap" style="gap:var(--s1) var(--s2)"><div style="min-width:0"><b>${esc(t)}</b><div class="sm mut">${st.n ? st.acc + '% of ' + st.n + ' solved' : 'not started'}</div></div><a class="btn sm" href="#/drill/${sub}/${i}">Drill 10</a></div>
      <div class="bar" style="margin:var(--s1) 0"><i style="width:${st.acc || 0}%"></i></div>
      ${dp.length ? `<div class="chips">${dp.map(d => { const dn = S().done[d.id], rn = S().running[d.id]; return `<a class="chip ${dn ? 'done' : ''}" href="#/dpp/${d.id}" title="${dn ? 'best ' + dn.best + '/' + dn.max : rn ? 'in progress' : '30 questions'}">DPP ${d.n}${dn ? ' ✓' : rn ? ' …' : ''}</a>`; }).join('')}</div>` : ''}</div>`; }).join('')}</div>`;
};

/* ---------- tests ---------- */
V.tests = async () => {
  const sub = S().subject, all = await GP.tests(), mine = all.filter(t => t.s === sub && (t.k === 'small' || t.k === 'sfull')), mocks = all.filter(t => t.k === 'full');
  const row = t => { const dn = S().done[t.id], rn = S().running[t.id], nq = t.q.length;
    return `<div class="trow"><div><b>${esc(t.ti)}</b><span class="sm mut">${nq} questions · ${t.m >= 60 ? (t.m / 60) + ' h' : t.m + ' min'}${dn ? ` · best ${dn.best} / ${dn.max}` : ''}${rn ? ' · in progress' : ''}</span></div><span></span><div class="acts"><a class="btn sm ${rn ? 'pri' : ''}" href="#/test/${t.id}">${rn ? 'Resume' : dn ? 'Retake' : 'Start'}</a></div></div>`; };
  const hist = S().tests.slice().reverse().slice(0, 12);
  return `<div class="page"><h1 class="h1">Tests</h1>
   <label class="row" style="gap:12px;margin:var(--s3) 0;align-items:flex-start;cursor:pointer"><input type="checkbox" id="dry" ${S().dry ? 'checked' : ''} style="margin-top:6px;width:18px;height:18px"><span><b>Exam-day dry run</b><br><span class="mut sm">Hides topic and difficulty tags and the per-question timer, like the real exam.</span></span></label>
   <div class="eyebrow">${esc(GP.subj(sub).name)} tests</div>${mine.map(row).join('') || '<p class="mut">No subject tests for this subject.</p>'}
   <div class="eyebrow" style="margin-top:var(--s4)">GATE CS full mocks · 65 questions · 3 hours</div>${mocks.map(row).join('')}
   <div class="eyebrow" style="margin:var(--s4) 0 var(--s1)">Past attempts</div>
   ${hist.map(h => `<a class="trow" href="#/result/${S().tests.indexOf(h)}"><div><b>${esc(h.title)}</b><span class="sm mut">${h.when}${h.dry ? ' · dry run' : ''}</span></div><span class="mono sm">${(+h.score).toFixed(2)} / ${h.max}</span><span class="link">Results →</span></a>`).join('') || '<p class="mut">None yet.</p>'}</div>`;
};
GP.afterTests = v => { const d = $('#dry', v); d && (d.onchange = e => { S().dry = e.target.checked; GP.save(); }); };

/* ---------- progress ---------- */
V.progress = async () => {
  const st = S(), now = new Date(), first = new Date(now.getTime() - 34 * 864e5); first.setDate(first.getDate() - ((first.getDay() + 6) % 7));
  const mx = Math.max(1, ...Object.values(st.days)), cells = []; let d = new Date(first), act = 0;
  while (d <= now) { const v = st.days[iso(d)] || 0; if (v) act++; cells.push(`<i class="${v ? 'l' + (1 + Math.min(3, Math.floor(4 * v / (mx + 1)))) : ''}" title="${iso(d)} · ${v} credits"></i>`); d = new Date(d.getTime() + 864e5); }
  const tot = Object.values(st.acc).reduce((x, v) => [x[0] + v[0], x[1] + v[1]], [0, 0]), ld = Object.values(st.lessons).filter(l => l.done).length;
  return `<div class="page wide"><h1 class="h1">Progress</h1>
   <div class="stats" style="margin-bottom:var(--s3)"><span><b>${st.solved}</b> solved</span><span><b>${tot[0] ? pct(tot[1], tot[0]) + '%' : '—'}</b> accuracy</span><span><b>${ld}/${GP.meta.lessons.length}</b> lessons</span><span><b>${st.credits}</b> credits</span><span><b>${GP.streak()}</b> day streak</span></div>
   <h2 class="h2" style="margin-top:var(--s3)">Activity</h2><p class="mut sm">Last 5 weeks · ${act} active days</p>
   <div class="dow" style="margin-top:var(--s1)">${['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map(x => `<span>${x}</span>`).join('')}</div><div class="cal">${cells.join('')}</div>
   <h2 class="h2" style="margin-top:var(--s4)">Topic heat-map</h2><p class="mut sm" style="margin-bottom:var(--s1)">Accuracy per topic · grey = not started · tap to drill</p>
   <div class="heat">${GP.meta.subjects.map(s => `<div class="hr"><b>${esc(s.name)}</b><div class="hcs">${s.topics.map((t, i) => { const x = GP.topicStat(s.code, t); return `<a class="hc ${x.acc === null ? 'z' : x.acc < 40 ? 'b' : x.acc < 70 ? 'm' : 'g'}" href="#/drill/${s.code}/${i}" title="${esc(t)}">${esc(t.length > 26 ? t.slice(0, 25) + '…' : t)}${x.acc !== null ? ' · ' + x.acc + '%' : ''}</a>`; }).join('')}</div></div>`).join('')}</div></div>`;
};

/* wrap the views that need a post-render hook */
const wrap = (name, hook) => { const f = V[name]; V[name] = async p => { const h = await f(p); const prev = GP.after; GP.after = v => { prev && prev(v); hook(v); }; return h; }; };
wrap('learn', learnAfter); wrap('tests', v => GP.afterTests(v));
})();
