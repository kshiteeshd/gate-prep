R = "E:/Test Platform/"


def rd(p): return open(R + p, encoding="utf-8").read()
def wr(p, s): open(R + p, "w", encoding="utf-8").write(s)


s = rd("gate/db.py")
s = s.replace("CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT);",
              "CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT);\nCREATE TABLE IF NOT EXISTS learn_progress(slug TEXT PRIMARY KEY, ts TEXT);")
wr("gate/db.py", s)

s = rd("app.py")
s = s.replace("from gate import db, game, seed, service, syllabus, updater, version", "import learn\nfrom gate import db, game, seed, service, syllabus, updater, version")
s = s.replace('app.jinja_env.filters["rt"] = rich_text', 'app.jinja_env.filters["rt"] = rich_text\napp.jinja_env.filters["md"] = learn.md')
marker = '@app.route("/api/bookmark/<qid>", methods=["POST"])'
new = '''# ---------- learning modules ----------
def _learn_done():
    return {r["slug"] for r in db.rows("SELECT slug FROM learn_progress")}


def _learn_practice(l, n=5):
    """Deterministic mix of practice questions for a lesson's syllabus topic (from the DPP pool)."""
    import random
    rows = db.rows("SELECT id, diff FROM questions WHERE pool='dpp' AND active=1 AND subject=? AND topic=? AND src!='legacy' ORDER BY id",
                   (l["subject"], l["topic"])) or db.rows("SELECT id, diff FROM questions WHERE pool='dpp' AND active=1 AND subject=? AND topic=? ORDER BY id", (l["subject"], l["topic"]))
    rng = random.Random(l["slug"])
    by = {"easy": [], "medium": [], "hard": []}
    for r in rows:
        by[r["diff"]].append(r["id"])
    pick = []
    for d, k in (("easy", 2), ("medium", 2), ("hard", 1)):
        pick += rng.sample(by[d], min(k, len(by[d])))
    rest = [i for d in by.values() for i in d if i not in pick]
    pick += rng.sample(rest, min(n - len(pick), len(rest)))
    qm = service.get_questions(pick)
    out = []
    for i in pick:
        q = qm[i]
        out.append({"id": q["id"], "qtype": q["qtype"], "text": q["text"], "options": q["options"], "marks": q["marks"], "diff": q["diff"]})
    return out


@app.route("/learn")
def learn_home():
    learn.load_all()
    done = _learn_done()
    cards = []
    for s in subjects():
        ls = [l for l in learn.LESSONS if l["subject"] == s["code"]]
        cards.append({"s": s, "n": len(ls), "done": sum(1 for l in ls if l["slug"] in done), "minutes": sum(l["minutes"] for l in ls),
                      "chapters": len({l["ch_no"] for l in ls})})
    return render_template("learn_home.html", cards=cards)


@app.route("/learn/<code>")
def learn_subject(code):
    s_ = _subject_or_404(code)
    tr = learn.tree(code)
    return render_template("learn_subject.html", s=s_, tree=tr, done=_learn_done(), lv=game.snapshot()["subjects"][code])


@app.route("/learn/<code>/<slug>")
def learn_topic(code, slug):
    l = learn.by_slug(slug)
    if not l or l["subject"] != code:
        abort(404)
    s_ = _subject_or_404(code)
    prev, nxt = learn.neighbours(l)
    return render_template("learn_topic.html", s=s_, l=l, tree=learn.tree(code), done=_learn_done(), prev=prev, nxt=nxt,
                           practice=_learn_practice(l), topic_row=db.one("SELECT id FROM topics WHERE subject=? AND name=?", (code, l["topic"])))


@app.route("/api/learn/complete/<slug>", methods=["POST"])
def api_learn_complete(slug):
    l = learn.by_slug(slug)
    if not l:
        return jsonify(error="unknown"), 404
    if db.one("SELECT 1 FROM learn_progress WHERE slug=?", (slug,)):
        return jsonify(already=True, credit=0)
    db.run("INSERT INTO learn_progress(slug, ts) VALUES(?,?)", (slug, datetime.now().isoformat(timespec="seconds")))
    ev = game.award("learn:" + slug, [(l["subject"], 20, "lesson")])
    return jsonify(credit=20, events=ev)


@app.route("/api/learn/check", methods=["POST"])
def api_learn_check():
    d = request.get_json(force=True) or {}
    qm = service.get_questions([d.get("qid")])
    q = qm.get(d.get("qid"))
    if not q:
        return jsonify(error="unknown question"), 404
    texts = [q["options"][i] for i in (d.get("sel") or []) if isinstance(i, int) and 0 <= i < len(q["options"])]
    state, got = service.score(q, texts, d.get("num"))
    credit = service._credit_for(q, state)
    ev = []
    with db.tx():
        if state != "skipped":
            service._stat_update(q["id"], state == "correct")
        if credit:
            ev = game.award("learn", [(q["subject"], credit, "learn")])
    return jsonify(state=state, credit=credit, correct=service.correct_display(q), answer=q["answer"], expl=q["expl"], events=ev)


'''
s = s.replace(marker, new + marker)
wr("app.py", s)

s = rd("templates/base.html")
s = s.replace('''   <a href="/mocks" class="{{ 'on' if ep=='mocks_page' }}">''', '''   <a href="/learn" class="{{ 'on' if ep in ('learn_home','learn_subject','learn_topic') }}">{{ ic('book') }}Learn</a>
   <a href="/mocks" class="{{ 'on' if ep=='mocks_page' }}">''')
s = s.replace(' <symbol id="i-arrow"', ' <symbol id="i-book" viewBox="0 0 24 24"><path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2zM4 19V5M9 7h6M9 11h6"/></symbol>\n <symbol id="i-arrow"')
wr("templates/base.html", s)
print("ok")
