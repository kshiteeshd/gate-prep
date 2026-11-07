R = "E:/Test Platform/"
s = open(R + "app.py", encoding="utf-8").read()

# ---- tests_for_ui: dpp awareness
a = s.index("def tests_for_ui():")
b = s.index("def fmt_time(sec):")
s = s[:a] + '''def tests_for_ui(subject=None, kinds=None):
    snap = game.snapshot()
    done = {}
    for r in db.rows("SELECT test_id, COUNT(*) n, MAX(score) best, MAX(max_marks) mx, MAX(correct) bc FROM attempts "
                     "WHERE status='submitted' AND test_id IS NOT NULL GROUP BY test_id"):
        done[r["test_id"]] = dict(r)
    running = {r["test_id"]: r["id"] for r in db.rows("SELECT id, test_id FROM attempts WHERE status='running' AND test_id IS NOT NULL")}
    sql, args = "SELECT id,kind,subject,topic,no,title,minutes,unlock_level,json_array_length(items) n FROM tests", []
    cond = []
    if subject:
        cond.append("subject=?"); args.append(subject)
    if kinds:
        cond.append("kind IN (%s)" % ",".join("?" * len(kinds))); args += list(kinds)
    if cond:
        sql += " WHERE " + " AND ".join(cond)
    out = []
    for t in db.rows(sql + " ORDER BY kind, subject, topic, no", args):
        d = dict(t)
        if d["kind"] == "dpp":
            d["unlocked"] = True
        else:
            lv = snap["overall"]["level"] if d["kind"] == "full" else snap["subjects"][d["subject"]]["level"]
            d["unlocked"] = lv >= d["unlock_level"]
        d["done"] = done.get(d["id"])
        d["running"] = running.get(d["id"])
        out.append(d)
    return out, snap


''' + s[b:]

# ---- subject pages
a = s.index('@app.route("/subject/<code>")')
b = s.index('@app.route("/topic/<int:tid>")')
s = s[:a] + '''def _subject_or_404(code):
    sj = db.one("SELECT * FROM subjects WHERE code=?", (code,))
    if not sj:
        abort(404)
    return dict(sj)


@app.route("/subject/<code>")
def subject_page(code):
    """Step 1 inside a subject: choose Test or Practice."""
    s_ = _subject_or_404(code)
    tests, snap = tests_for_ui(code)
    cnt = lambda kind: sum(1 for t in tests if t["kind"] == kind)
    doneN = lambda kinds: sum(1 for t in tests if t["kind"] in kinds and t["done"])
    return render_template("subject.html", s=s_, lv=snap["subjects"][code], prog=subject_progress().get(code, {}),
                           n_dpp=cnt("dpp"), n_topics=db.one("SELECT COUNT(*) n FROM topics WHERE subject=?", (code,))["n"],
                           n_small=cnt("small"), n_sfull=cnt("sfull"), done_dpp=doneN(("dpp",)), done_tests=doneN(("small", "sfull")))


@app.route("/subject/<code>/test")
def subject_test_choice(code):
    """Step 2 (Test): choose Small test or Full test."""
    s_ = _subject_or_404(code)
    tests, snap = tests_for_ui(code, ("small", "sfull"))
    info = {}
    for k in ("small", "sfull"):
        ts = [t for t in tests if t["kind"] == k]
        info[k] = {"n": len(ts), "open": sum(1 for t in ts if t["unlocked"]), "done": sum(1 for t in ts if t["done"])}
    return render_template("subject_test.html", s=s_, lv=snap["subjects"][code], info=info)


@app.route("/subject/<code>/test/<kind>")
def subject_test_list(code, kind):
    """Step 3 (Test): the list of small or full tests."""
    if kind not in ("small", "sfull"):
        abort(404)
    s_ = _subject_or_404(code)
    tests, snap = tests_for_ui(code, (kind,))
    return render_template("test_list.html", s=s_, kind=kind, tests=tests, lv=snap["subjects"][code])


@app.route("/subject/<code>/practice")
def subject_practice(code):
    """Practice: topic-wise list of DPPs (30 questions / 30 min each)."""
    s_ = _subject_or_404(code)
    tests, snap = tests_for_ui(code, ("dpp",))
    by_topic = {}
    for t in tests:
        by_topic.setdefault(t["topic"], []).append(t)
    topics = []
    for t in db.rows("SELECT id, name FROM topics WHERE subject=? ORDER BY ord", (code,)):
        ds = by_topic.get(t["name"], [])
        if ds:
            topics.append({"id": t["id"], "name": t["name"], "dpps": ds, "done": sum(1 for d in ds if d["done"])})
    return render_template("practice.html", s=s_, topics=topics, lv=snap["subjects"][code])


''' + s[b:]

# ---- mocks page (old tests page)
a = s.index('@app.route("/tests")')
b = s.index('@app.route("/analytics")')
s = s[:a] + '''@app.route("/mocks")
@app.route("/tests")
def mocks_page():
    full, snap = tests_for_ui(None, ("full",))
    return render_template("mocks.html", full=full, snap=snap)


''' + s[b:]

s = s.replace('''    nxt_mini = [t for t in tests if t["kind"] == "mini" and t["unlocked"] and not t["done"]][:3]\n''', '')
s = s.replace("nxt_full=nxt_full, nxt_mini=nxt_mini,", "nxt_full=nxt_full,")
s = s.replace("    tests, _ = tests_for_ui()\n    nxt_full", "    tests, _ = tests_for_ui(None, (\"full\",))\n    nxt_full")
s = s.replace("AND kind IN ('full','legacy','mini')", "AND kind IN ('full','sfull','small','legacy')")
open(R + "app.py", "w", encoding="utf-8").write(s)
print("app.py patched")
