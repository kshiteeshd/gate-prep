"""GATE Prep — local desktop app (Flask + SQLite). Run via desktop.py, or `python app.py` for browser mode."""
import json
import os
import shutil
from datetime import date, datetime, timedelta

from flask import Flask, abort, jsonify, redirect, render_template, request, send_file, url_for, flash

import learn
from gate import db, game, seed, service, syllabus, updater, version

app = Flask(__name__, template_folder=os.path.join(db.APP_DIR, "templates"),
            static_folder=os.path.join(db.APP_DIR, "static"))
app.secret_key = os.urandom(16)
seed.ensure_ready()
updater.check_in_background()


# ---------- helpers ----------
def subjects():
    return [dict(r) for r in db.rows("SELECT * FROM subjects ORDER BY ord")]


def topic_stats(code):
    """{topic: {diff: {total, seen, mastered}}} for the DPP pool of a subject."""
    out = {}
    for r in db.rows(
            "SELECT q.topic, q.diff, COUNT(*) total, SUM(s.qid IS NOT NULL) seen, SUM(COALESCE(s.ever_correct,0)) mastered"
            " FROM questions q LEFT JOIN qstats s ON s.qid=q.id WHERE q.pool='dpp' AND q.active=1 AND q.subject=?"
            " GROUP BY q.topic, q.diff", (code,)):
        out.setdefault(r["topic"], {})[r["diff"]] = {"total": r["total"], "seen": r["seen"] or 0,
                                                     "mastered": r["mastered"] or 0}
    return out


def subject_progress():
    """{code: {total, seen, mastered, acc}} from the DPP pool + all-time answer accuracy."""
    out = {}
    for r in db.rows("SELECT q.subject, COUNT(*) total, SUM(s.qid IS NOT NULL) seen, SUM(COALESCE(s.ever_correct,0)) m"
                     " FROM questions q LEFT JOIN qstats s ON s.qid=q.id WHERE q.pool='dpp' AND q.active=1 GROUP BY q.subject"):
        out[r["subject"]] = {"total": r["total"], "seen": r["seen"] or 0, "mastered": r["m"] or 0}
    for r in db.rows("SELECT subject, COUNT(*) n, SUM(state='correct') c FROM answers WHERE state!='skipped' GROUP BY subject"):
        p = out.setdefault(r["subject"], {"total": 0, "seen": 0, "mastered": 0})
        p["acc"] = round(100.0 * r["c"] / r["n"]) if r["n"] else None
        p["answered"] = r["n"]
    return out


def tests_for_ui(subject=None, kinds=None):
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


def fmt_time(sec):
    sec = int(sec or 0)
    h, m, s = sec // 3600, sec % 3600 // 60, sec % 60
    return "%d:%02d:%02d" % (h, m, s) if h else "%d:%02d" % (m, s)


def rich_text(s):
    """Escape, then render ```fences``` and `inline code` (matches the JS renderer in exam.js)."""
    import re
    from markupsafe import Markup, escape
    t = str(escape(s or ""))
    t = re.sub(r"```(?:\w+)?\n?(.*?)```", lambda m: "<pre><code>%s</code></pre>" % m.group(1).rstrip("\n"), t, flags=re.S)
    t = re.sub(r"`([^`\n]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\$\$(.+?)\$\$", lambda m: '<div class="texd" data-tex="%s">%s</div>' % (m.group(1), m.group(1)), t, flags=re.S)
    t = learn.tex_inline(t)
    return Markup(t)


app.jinja_env.filters["rt"] = rich_text
from learn.tex import typeset  # noqa: E402
app.jinja_env.filters["tex"] = typeset
app.jinja_env.filters["md"] = learn.md
app.jinja_env.filters["mdi"] = learn.mdi
app.jinja_env.filters["fmt_time"] = fmt_time
app.jinja_env.filters["pct"] = lambda a, b: round(100.0 * a / b) if b else 0


def navinfo():
    """Where-am-I data for every page: sidebar section, breadcrumb trail, active subject + sub-tab, back target."""
    ep, va = request.endpoint or "", request.view_args or {}
    names = {s["code"]: s["name"] for s in subjects()}
    code, tab, sec_, trail = va.get("code"), None, "home", [("Home", "/")]
    if ep == "topic_page":
        t = db.one("SELECT subject, name FROM topics WHERE id=?", (va.get("tid"),))
        code = t["subject"] if t else None
    if ep == "learn_topic":
        l = learn.by_slug(va.get("slug"))
    sj = (names.get(code), "/subject/%s" % code) if code in names else None
    if ep == "dashboard":
        trail = [("Home", None)]
    elif ep == "subject_page":
        sec_, tab, trail = "subj", "overview", trail + [(sj[0], None)]
    elif ep in ("subject_test_choice", "subject_test_list"):
        sec_, tab = "subj", "tests"
        trail += [sj, ("Tests", "/subject/%s/test" % code if ep == "subject_test_list" else None)]
        if ep == "subject_test_list":
            trail.append(("Small tests" if va.get("kind") == "small" else "Full tests", None))
    elif ep in ("subject_practice", "topic_page"):
        sec_, tab = "subj", "practice"
        trail += [sj, ("Practice", "/subject/%s/practice" % code if ep == "topic_page" else None)]
        if ep == "topic_page":
            trail.append((t["name"], None))
    elif ep == "learn_home":
        sec_, trail = "learn", trail + [("Learn", None)]
    elif ep in ("learn_subject", "learn_topic"):
        sec_, tab = "learn", "learn"
        trail += [("Learn", "/learn"), (sj[0], "/learn/%s" % code if ep == "learn_topic" else None)]
        if ep == "learn_topic" and l:
            trail.append((l["title"], None))
    elif ep == "mocks_page":
        sec_, trail = "mocks", trail + [("Mock exams", None)]
    elif ep in ("analytics", "history", "library", "settings", "result"):
        sec_ = "history" if ep == "result" else ep
        lab = {"analytics": "Progress", "history": "History", "library": "Import", "settings": "Settings", "result": "Result"}[ep]
        trail += ([("History", "/history")] if ep == "result" else []) + [(lab, None)]
    elif ep == "run_page":
        sec_ = "exam"
    parent = next((u for _, u in reversed(trail[:-1]) if u), "/") if len(trail) > 1 else None
    return {"crumbs": trail, "nav_sec": sec_, "nav_code": code if code in names else None, "nav_tab": tab, "nav_parent": parent}


@app.context_processor
def inject():
    snap = game.snapshot()
    return {**navinfo(), "G": snap, "SUBJ": subjects(), "streak": game.streak(), "today_n": game.today_answered(),
            "daily_goal": db.get_setting("daily_goal", 20), "TITLES": game.TITLES,
            "strict": db.get_setting("strict", False), "now_year": datetime.now().year,
            "update": updater.state()["available"], "APP_VERSION": version.VERSION, "ui": ui_prefs()}


UI_CHOICES = {"theme": ("paper", "sepia", "mist", "forest", "slate", "midnight"), "size": ("sm", "md", "lg", "xl"),
              "density": ("comfortable", "compact"), "side": ("full", "rail")}


def ui_prefs():
    out = {}
    for k, ok in UI_CHOICES.items():
        v = db.get_setting("ui_" + k, ok[0] if k != "size" else "md")
        out[k] = v if v in ok else (ok[0] if k != "size" else "md")
    return out


@app.route("/api/search-index")
def api_search_index():
    """Everything the Ctrl+K command bar can jump to."""
    learn.load_all()
    items = [{"t": n, "k": "Page", "u": u} for n, u in (("Home", "/"), ("Learn — all subjects", "/learn"), ("Mock exams", "/mocks"), ("Progress", "/analytics"),
                                                          ("History", "/history"), ("Import questions", "/library"), ("Settings", "/settings"))]
    for sj in subjects():
        c = sj["code"]
        items += [{"t": "%s — %s" % (sj["name"], lab), "k": "Subject", "u": u, "s": c} for lab, u in
                  (("overview", "/subject/" + c), ("learn", "/learn/" + c), ("practice", "/subject/%s/practice" % c), ("tests", "/subject/%s/test" % c))]
    items += [{"t": l["title"], "k": "Lesson", "u": "/learn/%s/%s" % (l["subject"], l["slug"]), "s": l["subject"], "x": l["topic"]} for l in learn.LESSONS]
    return jsonify(items)


@app.route("/api/ui", methods=["POST"])
def api_ui():
    for k, v in (request.get_json(silent=True) or {}).items():
        if k in UI_CHOICES and v in UI_CHOICES[k]:
            db.set_setting("ui_" + k, v)
    return jsonify(ok=True)


def _next_lesson(code=None):
    """The lesson to study next: the first unfinished one after the most recently completed lesson (in course order)."""
    learn.load_all()
    done = _learn_done()
    ls = [l for l in learn.LESSONS if not code or l["subject"] == code]
    pos = {l["slug"]: i for i, l in enumerate(ls)}
    start = 0
    for r in db.rows("SELECT slug FROM learn_progress ORDER BY ts DESC"):
        if r["slug"] in pos:
            start = pos[r["slug"]] + 1
            break
    for l in ls[start:] + ls[:start]:
        if l["slug"] not in done:
            return l
    return None


# ---------- pages ----------
@app.route("/")
def dashboard():
    prog = subject_progress()
    snap = game.snapshot()
    recent = [dict(r) for r in db.rows("SELECT * FROM attempts WHERE status='submitted' ORDER BY submitted_at DESC LIMIT 6")]
    running = [dict(r) for r in db.rows("SELECT id,title,kind,mode FROM attempts WHERE status='running' ORDER BY created_at DESC LIMIT 3")]
    weak = db.rows("SELECT subject, topic, COUNT(*) n, SUM(state='correct') c FROM answers WHERE state!='skipped' "
                   "GROUP BY subject, topic HAVING n>=5 ORDER BY 1.0*c/n LIMIT 4")
    tests, _ = tests_for_ui(None, ("full",))
    nxt_full = next((t for t in tests if t["kind"] == "full" and not t["done"]), None)
    week = db.rows("SELECT day, SUM(amount) c FROM ledger WHERE day >= date('now','-6 day','localtime') GROUP BY day")
    return render_template("dashboard.html", prog=prog, recent=recent, running=running, weak=weak,
                           nxt_full=nxt_full, week={r["day"]: r["c"] for r in week},
                           week_days=[(date.today() - timedelta(days=i)).isoformat() for i in range(6, -1, -1)],
                           levels=snap["subjects"], tot_answered=sum(v.get("answered", 0) for v in prog.values()),
                           nl=_next_lesson())


def _subject_or_404(code):
    sj = db.one("SELECT * FROM subjects WHERE code=?", (code,))
    if not sj:
        abort(404)
    return dict(sj)


@app.route("/subject/<code>")
def subject_page(code):
    """Overview of a subject: where you stand per topic, what to do next, and the way into Practice and Tests."""
    s_ = _subject_or_404(code)
    tests, snap = tests_for_ui(code)
    cnt = lambda kind: sum(1 for t in tests if t["kind"] == kind)
    doneN = lambda kinds: sum(1 for t in tests if t["kind"] in kinds and t["done"])
    learn.load_all()
    ldone = _learn_done()
    acc = {r["topic"]: (r["n"], r["c"]) for r in db.rows(
        "SELECT topic, COUNT(*) n, SUM(state='correct') c FROM answers WHERE subject=? AND state!='skipped' GROUP BY topic", (code,))}
    rows = []
    for t in db.rows("SELECT name FROM topics WHERE subject=? ORDER BY ord", (code,)):
        nm = t["name"]
        ls = [l for l in learn.LESSONS if l["subject"] == code and l["topic"] == nm]
        dp = [x for x in tests if x["kind"] == "dpp" and x["topic"] == nm]
        n, c = acc.get(nm, (0, 0))
        rows.append({"name": nm, "lessons": len(ls), "ldone": sum(1 for l in ls if l["slug"] in ldone),
                     "next": next((l for l in ls if l["slug"] not in ldone), None), "dpps": len(dp),
                     "ddone": sum(1 for x in dp if x["done"]), "n": n, "acc": round(100.0 * c / n) if n else None})
    weak = sorted((r for r in rows if r["n"] >= 5 and r["acc"] < 70), key=lambda r: r["acc"])
    return render_template("subject.html", s=s_, lv=snap["subjects"][code], prog=subject_progress().get(code, {}),
                           n_dpp=cnt("dpp"), n_topics=len(rows), rows=rows, weak=weak[0] if weak else None, nl=_next_lesson(code),
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


@app.route("/topic/<int:tid>")
def topic_page(tid):
    t = db.one("SELECT * FROM topics WHERE id=?", (tid,))
    if not t:
        abort(404)
    s = db.one("SELECT * FROM subjects WHERE code=?", (t["subject"],))
    st = topic_stats(t["subject"]).get(t["name"], {})
    subs = db.rows("SELECT q.subtopic, q.diff, COUNT(*) n, SUM(s.qid IS NOT NULL) seen FROM questions q LEFT JOIN qstats s ON s.qid=q.id"
                   " WHERE q.pool='dpp' AND q.active=1 AND q.subject=? AND q.topic=? GROUP BY q.subtopic, q.diff ORDER BY q.subtopic",
                   (t["subject"], t["name"]))
    subtopics = {}
    for r in subs:
        d = subtopics.setdefault(r["subtopic"] or "General", {"name": r["subtopic"] or "General", "n": 0, "seen": 0})
        d["n"] += r["n"]
        d["seen"] += r["seen"] or 0
    acc = db.one("SELECT COUNT(*) n, SUM(state='correct') c FROM answers WHERE subject=? AND topic=? AND state!='skipped'",
                 (t["subject"], t["name"]))
    return render_template("topic.html", s=dict(s), t=dict(t), st=st, subtopics=list(subtopics.values()),
                           acc=round(100.0 * acc["c"] / acc["n"]) if acc["n"] else None, answered=acc["n"],
                           others=[dict(r) for r in db.rows("SELECT id,name FROM topics WHERE subject=? ORDER BY ord", (t["subject"],))])


@app.route("/mocks")
@app.route("/tests")
def mocks_page():
    full, snap = tests_for_ui(None, ("full",))
    return render_template("mocks.html", full=full, snap=snap)


@app.route("/analytics")
def analytics():
    prog = subject_progress()
    daily = db.rows("SELECT day, SUM(amount) c FROM ledger WHERE day >= date('now','-29 day','localtime') GROUP BY day ORDER BY day")
    topics = db.rows("SELECT subject, topic, COUNT(*) n, SUM(state='correct') c, AVG(time_sec) t FROM answers WHERE state!='skipped' "
                     "GROUP BY subject, topic ORDER BY 1.0*c/n")
    diffs = db.rows("SELECT diff, COUNT(*) n, SUM(state='correct') c, AVG(time_sec) t FROM answers WHERE state!='skipped' GROUP BY diff")
    scores = db.rows("SELECT title, submitted_at, score, max_marks FROM attempts WHERE status='submitted' AND kind IN ('full','sfull','small','legacy') "
                     "AND max_marks>0 ORDER BY submitted_at DESC LIMIT 15")
    # topic heat-map: every syllabus topic, grey until attempted
    stat = {(r["subject"], r["topic"]): (r["n"], r["c"]) for r in db.rows(
        "SELECT subject, topic, COUNT(*) n, SUM(state='correct') c FROM answers WHERE state!='skipped' GROUP BY subject, topic")}
    heat = []
    for sj in subjects():
        cells = []
        for t in db.rows("SELECT name FROM topics WHERE subject=? ORDER BY ord", (sj["code"],)):
            n, c = stat.get((sj["code"], t["name"]), (0, 0))
            cells.append({"name": t["name"], "n": n, "acc": round(100.0 * c / n) if n else None})
        heat.append({"s": sj, "cells": cells})
    # 5-week activity calendar (Monday first), shaded by credits earned that day
    credits = {r["day"]: r["c"] for r in db.rows("SELECT day, SUM(amount) c FROM ledger WHERE day >= date('now','-41 day','localtime') GROUP BY day")}
    today = date.today()
    first = today - timedelta(days=34)
    first -= timedelta(days=first.weekday())
    mx = max(credits.values()) if credits else 0
    cal = []
    d = first
    while d <= today:
        v = credits.get(d.isoformat(), 0)
        cal.append({"day": d.isoformat(), "c": v, "lvl": 0 if not v else 1 + min(3, int(4 * v / (mx + 1))), "m": d.strftime("%d %b")})
        d += timedelta(days=1)
    return render_template("analytics.html", heat=heat, cal=cal, active_days=sum(1 for c in cal if c["c"]), prog=prog, daily=[dict(r) for r in daily], topics=[dict(r) for r in topics],
                           diffs={r["diff"]: dict(r) for r in diffs}, scores=[dict(r) for r in scores][::-1])


@app.route("/history")
def history():
    kind = request.args.get("kind", "")
    sql = "SELECT * FROM attempts WHERE status='submitted'" + (" AND kind=?" if kind else "") + " ORDER BY submitted_at DESC LIMIT 200"
    return render_template("history.html", atts=[dict(r) for r in db.rows(sql, (kind,) if kind else ())], kind=kind)


@app.route("/library", methods=["GET", "POST"])
def library():
    if request.method == "POST":
        f = request.files.get("file")
        code, topic = request.form.get("subject"), request.form.get("topic")
        pool = request.form.get("pool", "dpp")
        if not f or code not in syllabus.SUBJECT_BY_CODE or topic not in syllabus.TOPICS[code]:
            flash("Choose a file, subject and topic.", "err")
            return redirect(url_for("library"))
        try:
            n = import_file(f, code, topic, pool)
            flash("Imported %d new questions into %s · %s." % (n, code, topic), "ok")
        except Exception as e:
            flash("Import failed: %s" % e, "err")
        return redirect(url_for("library"))
    counts = db.rows("SELECT subject, pool, COUNT(*) n FROM questions WHERE active=1 GROUP BY subject, pool")
    return render_template("library.html", counts=counts, topics=syllabus.TOPICS)


def import_file(f, code, topic, pool):
    import csv, io
    name = (f.filename or "").lower()
    text = f.read().decode("utf-8-sig")
    if name.endswith(".json"):
        data = json.loads(text)
        raws = data if isinstance(data, list) else data.get("questions", [])
    elif name.endswith(".csv"):
        raws = []
        for row in csv.DictReader(io.StringIO(text)):
            opts = [(row.get("option_" + c) or "").strip() for c in "abcd"]
            opts = [o for o in opts if o]
            corr = [p.strip().upper() for p in (row.get("correct") or "").replace(";", ",").split(",") if p.strip()]
            qt = (row.get("type") or "single").lower()
            ans = [opts["ABCD".index(p)] for p in corr if p in "ABCD" and "ABCD".index(p) < len(opts)]
            raws.append({"q": row.get("question", ""), "type": qt, "options": opts, "answer": ans if qt != "numerical" else row.get("correct"),
                         "marks": row.get("marks") or 1, "negative": row.get("negative") or 0,
                         "difficulty": row.get("difficulty") or "medium", "tolerance": row.get("tolerance") or 0})
    else:
        raise ValueError("upload .json or .csv")
    batch = []
    for raw in raws:
        q = seed._legacy_q(raw, code, topic)
        if q:
            q.update(pool=pool, src="import", subtopic="Imported", expl=raw.get("explanation", ""))
            batch.append(seed._qtuple(q))
    before = db.one("SELECT COUNT(*) n FROM questions")["n"]
    db.many("INSERT OR IGNORE INTO questions(id,subject,topic,subtopic,qtype,text,options,answer,numeric,tol,marks,neg,diff,expl,pool,src)"
            " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", batch)
    return db.one("SELECT COUNT(*) n FROM questions")["n"] - before


@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        db.set_setting("strict", request.form.get("strict") == "on")
        db.set_setting("auto_update", request.form.get("auto_update") == "on")
        db.set_setting("update_feed", (request.form.get("update_feed") or "").strip())
        try:
            db.set_setting("daily_goal", max(5, min(500, int(request.form.get("daily_goal", 20)))))
        except ValueError:
            pass
        flash("Settings saved.", "ok")
        return redirect(url_for("settings"))
    return render_template("settings.html", db_path=db.DB_PATH, auto_update=db.get_setting("auto_update", True),
                           feed=updater.feed_url(), ustate=updater.state())


@app.route("/update/check", methods=["POST"])
def update_check():
    info = updater.check(True)
    st = updater.state()
    flash(("Version %s is available — use the banner or the button below to install." % info["version"]) if info else
          ("Could not check: %s" % st["error"] if st["error"] else "You are on the latest version (%s)." % version.VERSION), "ok" if not st["error"] else "err")
    return redirect(url_for("settings"))


@app.route("/update/install", methods=["POST"])
def update_install():
    try:
        v = updater.install()
        return "Installing version %s … the app will close and reopen automatically." % v
    except Exception as e:
        flash("Update failed: %s" % e, "err")
        return redirect(url_for("settings"))


@app.route("/settings/backup")
def backup():
    dst = os.path.join(db.DATA_DIR, "backup_%s.db" % datetime.now().strftime("%Y%m%d_%H%M%S"))
    db.conn().execute("VACUUM INTO ?", (dst,))
    return send_file(dst, as_attachment=True, download_name=os.path.basename(dst))


@app.route("/settings/reset", methods=["POST"])
def reset_progress():
    if request.form.get("confirm") == "RESET":
        with db.tx():
            for t in ("attempts", "answers", "qstats", "ledger", "bookmarks"):
                db.run("DELETE FROM " + t)
        flash("All progress cleared. Questions and tests are untouched.", "ok")
    else:
        flash("Type RESET to confirm.", "err")
    return redirect(url_for("settings"))


# ---------- start / run ----------
@app.route("/start/dpp", methods=["POST"])
def start_dpp():
    f = request.form
    try:
        n = max(5, min(50, int(f.get("n", 10))))
    except ValueError:
        n = 10
    aid = service.create_dpp(f.get("subject") or None, f.get("topic") or None, f.get("subtopic") or None,
                             f.get("diff") or None, n, f.get("title") or None)
    if not aid:
        flash("No questions available for that selection yet.", "err")
        return redirect(request.referrer or url_for("dashboard"))
    return redirect(url_for("run_page", aid=aid))


@app.route("/start/test/<tid>", methods=["POST"])
def start_test(tid):
    t = db.one("SELECT * FROM tests WHERE id=?", (tid,))
    if not t:
        abort(404)
    if not service.is_unlocked(t):
        flash("That test is still locked — keep earning credits!", "err")
        return redirect(request.referrer or url_for("mocks_page"))
    return redirect(url_for("run_page", aid=service.create_test_attempt(tid)))


@app.route("/run/<aid>")
def run_page(aid):
    a = service.get_attempt(aid)
    if not a:
        abort(404)
    if a["status"] == "submitted":
        return redirect(url_for("result", aid=aid))
    return render_template("exam.html", a=dict(a))


@app.route("/result/<aid>")
def result(aid):
    a = service.get_attempt(aid)
    if not a:
        abort(404)
    if a["status"] != "submitted":
        return redirect(url_for("run_page", aid=aid))
    r = service.result(a)
    r["n_marked"] = sum(1 for x in r["review"] if x["marked"])
    seen_key = "seen_events_" + aid
    r["new_events"] = [] if db.get_setting(seen_key) else r["events"]
    if r["events"]:
        db.set_setting(seen_key, True)
    return render_template("result.html", **r)


@app.route("/api/attempt/<aid>/paper")
def api_paper(aid):
    a = service.get_attempt(aid)
    if not a:
        return jsonify(error="not found"), 404
    if a["status"] == "submitted":
        return jsonify(error="submitted", result=url_for("result", aid=aid)), 410
    return jsonify(service.paper(a))


@app.route("/api/attempt/<aid>/save", methods=["POST"])
def api_save(aid):
    a = service.get_attempt(aid)
    if not a or a["status"] != "running":
        return jsonify(ok=False), 404
    db.run("UPDATE attempts SET state=? WHERE id=?", (json.dumps(request.get_json(force=True) or {}), aid))
    return jsonify(ok=True)


@app.route("/api/attempt/<aid>/check", methods=["POST"])
def api_check(aid):
    a = service.get_attempt(aid)
    if not a or a["status"] != "running" or a["mode"] != "practice":
        return jsonify(error="bad attempt"), 400
    d = request.get_json(force=True) or {}
    out = service.check(a, int(d.get("pos", -1)), d.get("sel") or [], d.get("num"), d.get("time"))
    return jsonify(out or {"error": "bad question"})


@app.route("/api/attempt/<aid>/submit", methods=["POST"])
def api_submit(aid):
    a = service.get_attempt(aid)
    if not a:
        return jsonify(error="not found"), 404
    d = request.get_json(force=True) or {}
    service.submit(a, d.get("state"), d.get("violations", 0), d.get("used_sec", 0))
    return jsonify(result=url_for("result", aid=aid))


# ---------- learning modules ----------
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
    return render_template("learn_subject.html", s=s_, tree=tr, done=_learn_done(), lv=game.snapshot()["subjects"][code], nl=_next_lesson(code))


@app.route("/learn/<code>/<slug>")
def learn_topic(code, slug):
    l = learn.by_slug(slug)
    if not l or l["subject"] != code:
        abort(404)
    s_ = _subject_or_404(code)
    prev, nxt = learn.neighbours(l)
    return render_template("learn_topic.html", s=s_, l=l, tree=learn.tree(code), done=_learn_done(), prev=prev, nxt=nxt,
                           practice=_learn_practice(l), topic_row=db.one("SELECT id FROM topics WHERE subject=? AND name=?", (code, l["topic"])))


@app.route("/api/learn/sql", methods=["POST"])
def api_learn_sql():
    from learn import sampledb
    return jsonify(sampledb.run_query((request.get_json(force=True) or {}).get("sql", "")))


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


@app.route("/api/bookmark/<qid>", methods=["POST"])
def api_bookmark(qid):
    if db.one("SELECT 1 FROM bookmarks WHERE qid=?", (qid,)):
        db.run("DELETE FROM bookmarks WHERE qid=?", (qid,))
        return jsonify(on=False)
    db.run("INSERT INTO bookmarks VALUES(?,?)", (qid, datetime.now().isoformat(timespec="seconds")))
    return jsonify(on=True)


@app.after_request
def no_cache(resp):
    if request.path.startswith(("/api/", "/run/", "/result/")):
        resp.headers["Cache-Control"] = "no-store"
    return resp


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
