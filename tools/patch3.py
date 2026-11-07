R = "E:/Test Platform/"


def rd(p): return open(R + p, encoding="utf-8").read()
def wr(p, s): open(R + p, "w", encoding="utf-8").write(s)


# ---- CSS
s = rd("static/css/app.css")
s += """
/* choice cards + DPP tiles */
.choice{display:flex;flex-direction:column;gap:6px;padding:28px;transition:.2s;position:relative;overflow:hidden}
.choice::after{content:"";position:absolute;right:-60px;top:-60px;width:200px;height:200px;border-radius:50%;background:radial-gradient(circle,color-mix(in srgb,var(--c) 28%,transparent),transparent 70%)}
.choice:hover{transform:translateY(-4px);border-color:var(--c);box-shadow:0 18px 40px color-mix(in srgb,var(--c) 25%,transparent)}
.choice .ci{width:54px;height:54px;border-radius:16px;display:grid;place-items:center;background:var(--c);color:#fff;margin-bottom:8px}
.choice .ci svg{width:26px;height:26px}
.choice p{margin:2px 0 8px;max-width:46ch}
.dtile{display:flex;flex-direction:column;gap:9px;padding:16px;transition:.15s}
.dtile:hover{border-color:var(--c);transform:translateY(-2px)}
.dtile .no{font-weight:850;font-size:1.25rem;color:var(--c)}
.dtile.done{border-color:rgba(52,211,153,.4)}
"""
wr("static/css/app.css", s)

# ---- base nav
s = rd("templates/base.html")
a = s.index('   {% set ep = request.endpoint or \'\' %}')
b = s.index("  </nav>")
s = s[:a] + '''   {% set ep = request.endpoint or '' %}
   <a href="/" class="{{ 'on' if ep in ('dashboard','subject_page','subject_test_choice','subject_test_list','subject_practice','topic_page') }}">{{ ic('home') }}Subjects</a>
   <a href="/mocks" class="{{ 'on' if ep=='mocks_page' }}">{{ ic('trophy') }}GATE Mocks</a>
   <div class="sec">Track</div>
   <a href="/analytics" class="{{ 'on' if ep=='analytics' }}">{{ ic('chart') }}Analytics</a>
   <a href="/history" class="{{ 'on' if ep=='history' }}">{{ ic('clock') }}History</a>
   <div class="sec">Manage</div>
   <a href="/library" class="{{ 'on' if ep=='library' }}">{{ ic('upload') }}Import</a>
   <a href="/settings" class="{{ 'on' if ep=='settings' }}">{{ ic('cog') }}Settings</a>
''' + s[b:]
wr("templates/base.html", s)

# ---- dashboard: subjects first
s = rd("templates/dashboard.html")
i_run = s.index("{% if running %}")
i_subj = s.index('<div class="sech"><div><h2 class="h2">Subjects</h2>')
i_tail = s.index('<div class="grid g2" style="margin-top:34px">')
missions = s[i_run:i_subj]
subj = s[i_subj:i_tail]
subj = subj.replace('<h2 class="h2">Subjects</h2><p>Level up in each subject to unlock its mini tests</p></div><a class="small muted" href="/tests">All tests →</a>',
                    '<h2 class="h2">Choose a subject</h2><p>Open a subject to practise topic-wise DPPs or take a test</p></div><a class="small muted" href="/mocks">Full GATE mocks →</a>')
s = s[:i_run] + subj + missions + s[i_tail:]
s = s.replace('/tests', '/mocks')
wr("templates/dashboard.html", s)

# ---- result / history / macros labels
s = rd("templates/result.html")
s = s.replace("a.kind|replace('dpp','Practice')|replace('mini','Mini test')|replace('full','Full mock')|replace('legacy','Earlier test')",
              "a.kind|replace('dpp','Practice')|replace('small','Small test')|replace('sfull','Full test')|replace('full','GATE mock')|replace('legacy','Earlier test')")
s = s.replace('<a class="btn" href="/tests">All tests</a>', '<a class="btn" href="/">Subjects</a>')
wr("templates/result.html", s)
s = rd("templates/history.html")
s = s.replace("(('', 'All'), ('dpp','DPP'), ('mini','Mini'), ('full','Full'), ('legacy','Earlier'))",
              "(('', 'All'), ('dpp','Practice'), ('small','Small'), ('sfull','Full test'), ('full','GATE mock'), ('legacy','Earlier'))")
wr("templates/history.html", s)
s = rd("templates/_m.html")
s = s.replace("in {{ t.subject }}{% else %} overall{% endif %}", "in {{ t.subject }}{% else %} overall{% endif %}")
wr("templates/_m.html", s)

# ---- exam page: DPP timer chip
s = rd("templates/exam.html")
s = s.replace('<span class="chip" id="combo"', '<span class="chip" id="pTimer" hidden>⏱ <b>30:00</b></span>\n  <span class="chip" id="combo"')
wr("templates/exam.html", s)
s = rd("static/js/exam.js")
s = s.replace("  pRender();\n}\n\n/* ---------- wiring", """  if (P.minutes) {
    remain = P.remaining; $('#pTimer').hidden = false;
    const t = () => { $('#pTimer b').textContent = fmt(remain).replace(/^00:/, ''); if (remain < 300) $('#pTimer').style.color = 'var(--bad)'; if (remain <= 0) { clearInterval(tmr); toast('⏰ Time is up'); pFinish(); } remain--; };
    t(); tmr = setInterval(t, 1000);
  }
  pRender();
}

/* ---------- wiring""")
wr("static/js/exam.js", s)
print("ok")
