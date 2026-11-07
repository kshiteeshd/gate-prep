/* GATE Prep — shared UI: themes, text size, density, sidebar rail, fullscreen, exit, keyboard shortcuts. */
(function () {
  const root = document.documentElement;
  const THEMES = ['paper', 'sepia', 'mist', 'forest', 'slate', 'midnight'];
  const save = (k, v) => {
    root.dataset[k] = v;
    try { localStorage.setItem('ui:' + k, v); } catch (e) {}
    fetch('/api/ui', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({[k]: v})}).catch(() => {});
    document.dispatchEvent(new CustomEvent('uichange', {detail: {[k]: v}}));
  };
  const UI = window.UI = {
    set: save,
    get: k => root.dataset[k],
    theme: t => save('theme', t),
    cycleTheme: () => save('theme', THEMES[(THEMES.indexOf(root.dataset.theme) + 1) % THEMES.length]),
    side: () => save('side', root.dataset.side === 'rail' ? 'full' : 'rail'),
  };

  /* ---- fullscreen: native window when running in the desktop shell, DOM fullscreen in a browser ---- */
  const inShell = () => window.pywebview && window.pywebview.api && window.pywebview.api.toggle_fullscreen;
  UI.fullscreen = function () {
    if (inShell()) return window.pywebview.api.toggle_fullscreen();
    if (document.fullscreenElement) document.exitFullscreen(); else root.requestFullscreen && root.requestFullscreen().catch(() => {});
  };

  /* ---- overlays ---- */
  function overlay(id, html) {
    let o = document.getElementById(id);
    if (!o) { o = document.createElement('div'); o.id = id; o.className = 'ovl'; o.innerHTML = '<div class="box">' + html + '</div>'; document.body.appendChild(o); o.addEventListener('mousedown', e => { if (e.target === o) o.classList.remove('on'); }); }
    return o;
  }
  UI.exit = function () {
    const o = overlay('exitOvl', '<h2>Exit GATE Prep?</h2><p style="margin:0">Your progress is saved automatically. A test that is running keeps its clock, so you can resume it later.</p><div class="acts"><button class="btn" data-x="no">Stay</button><button class="btn dng" data-x="yes">Exit app</button></div>');
    o.classList.add('on');
    o.querySelector('[data-x=no]').onclick = () => o.classList.remove('on');
    o.querySelector('[data-x=yes]').onclick = () => { if (window.pywebview && window.pywebview.api && window.pywebview.api.quit) window.pywebview.api.quit(); else window.close(); };
    o.querySelector('[data-x=no]').focus();
  };
  /* ---- Ctrl+K: jump to any page, subject tab or lesson ---- */
  let IDX = null;
  UI.search = function () {
    const o = overlay('cmdk', '<input id="cmdIn" placeholder="Jump to a lesson, subject or page…" autocomplete="off" spellcheck="false"><ul id="cmdList"></ul><div class="foot">↑ ↓ to move · Enter to open · Esc to close</div>');
    o.classList.add('cmdk', 'on');
    const inp = o.querySelector('#cmdIn'), ul = o.querySelector('#cmdList'); let hits = [], cur = 0;
    const esc = t => String(t).replace(/[&<>]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;'}[c]));
    const draw = () => {
      ul.innerHTML = hits.length ? hits.map((h, i) => '<li class="' + (i === cur ? 'on' : '') + '" data-i="' + i + '"><span class="k">' + h.k + '</span><span class="t">' + esc(h.t) + (h.x ? ' <small>· ' + esc(h.x) + '</small>' : '') + '</span></li>').join('') : '<div class="none">No matches</div>';
      const e = ul.querySelector('li.on'); if (e) e.scrollIntoView({block: 'nearest'});
    };
    const filt = () => {
      const q = inp.value.toLowerCase().split(/\s+/).filter(Boolean);
      hits = (IDX || []).filter(h => { const hay = (h.t + ' ' + h.k + ' ' + (h.s || '') + ' ' + (h.x || '')).toLowerCase(); return q.every(w => hay.indexOf(w) >= 0); }).slice(0, 60);
      if (!q.length) hits = IDX.filter(h => h.k === 'Page' || /overview$/.test(h.t)).slice(0, 30);
      cur = 0; draw();
    };
    const go = i => { if (hits[i]) location.href = hits[i].u; };
    inp.oninput = filt;
    inp.onkeydown = e => {
      if (e.key === 'ArrowDown') { e.preventDefault(); cur = Math.min(hits.length - 1, cur + 1); draw(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); cur = Math.max(0, cur - 1); draw(); }
      else if (e.key === 'Enter') { e.preventDefault(); go(cur); }
    };
    ul.onclick = e => { const li = e.target.closest('li'); if (li) go(+li.dataset.i); };
    inp.value = ''; inp.focus();
    if (IDX) filt(); else fetch('/api/search-index').then(r => r.json()).then(d => { IDX = d; filt(); });
  };
  UI.help = function () {
    const rows = [['F11', 'Full screen on / off'], ['Esc', 'Leave full screen · close this panel'], ['Ctrl B', 'Collapse / expand the sidebar'], ['Alt ←', 'Back'],
      ['Alt 1 – 5', 'Home · Learn · Mock exams · Progress · Settings'], ['Ctrl K', 'Search: jump to any lesson, subject or page'], ['Alt T', 'Next theme'], ['Ctrl Q', 'Exit the app'], ['?', 'This list'],
      ['1–4 / A–D', 'In a DPP or test: choose an option'], ['Enter', 'Practice: check, then next question'], ['← →', 'Test: previous / next question']];
    const o = overlay('helpOvl', '<h2>Keyboard shortcuts</h2><div class="keys">' + rows.map(r => '<span>' + r[0].split(' ').map(k => k === '–' || k === '·' ? k : '<kbd>' + k + '</kbd>').join(' ') + '</span><span>' + r[1] + '</span>').join('') + '</div><div class="acts"><button class="btn" data-x="no">Close</button></div>');
    o.classList.add('on'); o.querySelector('[data-x=no]').onclick = () => o.classList.remove('on');
  };

  document.addEventListener('keydown', e => {
    const t = e.target, typing = t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT' || t.isContentEditable);
    const strict = !!(window.ATT && window.ATT.strict);
    if (e.key === 'Escape') { document.querySelectorAll('.ovl.on').forEach(o => o.classList.remove('on')); return; }
    if (e.key === 'F11') { e.preventDefault(); if (!strict) UI.fullscreen(); return; }
    if (e.ctrlKey && !e.shiftKey && !e.altKey && e.key.toLowerCase() === 'b' && document.querySelector('.side')) { e.preventDefault(); UI.side(); return; }
    if (e.ctrlKey && !e.shiftKey && !e.altKey && e.key.toLowerCase() === 'k' && document.querySelector('.side')) { e.preventDefault(); UI.search(); return; }
    if (e.ctrlKey && !e.shiftKey && !e.altKey && e.key.toLowerCase() === 'q') { e.preventDefault(); UI.exit(); return; }
    if (e.altKey && !e.ctrlKey && e.key.toLowerCase() === 't') { e.preventDefault(); UI.cycleTheme(); return; }
    if (e.altKey && !e.ctrlKey && /^[1-5]$/.test(e.key) && document.querySelector('.side')) {
      const to = ['/', '/learn', '/mocks', '/analytics', '/settings'][+e.key - 1]; e.preventDefault(); location.href = to; return;
    }
    if (!typing && e.key === '?') { e.preventDefault(); UI.help(); }
  });

  /* ---- wiring for buttons that carry data-ui attributes ---- */
  document.addEventListener('click', e => {
    const b = e.target.closest('[data-ui]'); if (!b) return;
    const a = b.dataset.ui;
    if (a === 'fullscreen') UI.fullscreen(); else if (a === 'exit') UI.exit(); else if (a === 'side') UI.side(); else if (a === 'help') UI.help(); else if (a === 'search') UI.search();
    else if (a === 'theme') { UI.theme(b.dataset.v); document.querySelectorAll('[data-ui=theme]').forEach(x => x.classList.toggle('on', x === b)); }
    else if (a === 'size' || a === 'density') { UI.set(a, b.dataset.v); b.parentNode.querySelectorAll('button').forEach(x => x.classList.toggle('on', x === b)); }
  });
})();
