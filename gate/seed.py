"""First-run setup: syllabus, content pack, legacy question banks + past attempts, test series."""
import glob
import json
import os

from . import builder, db, game, syllabus

# Bump TESTS_VER only for a full reform of the test series. Attempted tests and all progress are always kept; only
# tests nobody has opened are regenerated. Minor content changes must NOT bump it (new questions are added, old
# tests stay as they are).
TESTS_VER = 5
PACK = os.path.join(db.APP_DIR, "content", "pack.json")


def seed_syllabus():
    db.many("INSERT OR REPLACE INTO subjects(code,name,glyph,color,ord,fq) VALUES(?,?,?,?,?,?)",
            [(s["code"], s["name"], s["glyph"], s["color"], i, s["fq"]) for i, s in enumerate(syllabus.SUBJECTS)])
    db.many("INSERT OR IGNORE INTO topics(subject,name,ord) VALUES(?,?,?)",
            [(c, t, i) for c, ts in syllabus.TOPICS.items() for i, t in enumerate(ts)])


def _qtuple(d):
    return (d["id"], d["subject"], d["topic"], d.get("subtopic") or "", d["qtype"], d["text"],
            json.dumps(d.get("options", []), ensure_ascii=False), json.dumps(d.get("answer", []), ensure_ascii=False),
            d.get("numeric"), d.get("tol", 0), d["marks"], d.get("neg", 0), d["diff"], d.get("expl", ""),
            d["pool"], d.get("src", "pack"))


def pack_files():
    if os.environ.get("GATEPREP_NO_PYQ"):          # public site build: past-paper questions are left out
        return [PACK]
    return [PACK] + sorted(glob.glob(os.path.join(os.path.dirname(PACK), "pyq_*.json")))


def load_pack():
    qs = []
    for fn in pack_files():
        if os.path.exists(fn):
            with open(fn, encoding="utf-8") as f:
                qs += json.load(f)
    if not qs:
        return 0
    db.many("INSERT OR IGNORE INTO questions(id,subject,topic,subtopic,qtype,text,options,answer,numeric,tol,marks,neg,diff,expl,pool,src)"
            " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [_qtuple(q) for q in qs])
    # explanations / subtopics may improve between releases: refresh text-only fields, never ids, pools or stats
    db.many("UPDATE questions SET expl=?, subtopic=?, text=? WHERE id=?",
            [(q.get("expl", ""), q.get("subtopic") or "", q["text"], q["id"]) for q in qs])
    # a question dropped from the pack is retired (not deleted): old attempts keep working, new tests skip it
    ids = [q["id"] for q in qs]
    db.run("CREATE TEMP TABLE IF NOT EXISTS packids(id TEXT PRIMARY KEY)")
    db.run("DELETE FROM packids")
    db.many("INSERT OR IGNORE INTO packids VALUES(?)", [(i,) for i in ids])
    db.run("UPDATE questions SET active=0 WHERE src!='legacy' AND id NOT IN (SELECT id FROM packids)")
    db.run("UPDATE questions SET active=1 WHERE id IN (SELECT id FROM packids)")
    return len(qs)


def _pack_sig():
    """Content hash of the question packs (file times change on every rebuild, content does not)."""
    import hashlib
    h = hashlib.sha1()
    for f in pack_files():
        if os.path.exists(f):
            with open(f, "rb") as fh:
                h.update(fh.read())
    return h.hexdigest()


# ---------- legacy (v1 file-based app) ----------
def _norm_type(t):
    t = str(t or "single").lower().strip()
    if t in ("msq", "multi", "multiple", "multiple_correct", "multiselect"):
        return "multiple"
    if t in ("nat", "numeric", "integer", "numerical"):
        return "numerical"
    return "single"


def _legacy_q(raw, subject, topic):
    qt = _norm_type(raw.get("type", raw.get("qtype")))
    opts = list(raw.get("options") or [])
    ans = raw.get("answer", raw.get("correct_options", [])) or []
    if isinstance(ans, str):
        ans = [ans]
    num = None
    if qt == "numerical":
        try:
            num = float(raw.get("answer", raw.get("correct_numeric")))
        except (TypeError, ValueError):
            return None
        ans, opts = [], []
    elif not ans or not opts:
        return None
    try:
        marks = float(raw.get("marks", 1))
        neg = float(raw.get("negative", 0)) if qt == "single" else 0.0
        tol = float(raw.get("tolerance", 0))
    except (TypeError, ValueError):
        marks, neg, tol = 1.0, 0.0, 0.0
    d = (raw.get("difficulty") or "medium").lower()
    text = raw.get("q", raw.get("question", ""))
    return {"id": db.qid_for(text, opts, ans if qt != "numerical" else num), "subject": subject, "topic": topic,
            "subtopic": "", "qtype": qt, "text": text, "options": opts, "answer": ans, "numeric": num, "tol": tol,
            "marks": marks, "neg": neg, "diff": d if d in syllabus.DIFFS else "medium", "expl": "",
            "pool": "dpp", "src": "legacy"}


def import_legacy(base):
    tests = os.path.join(base, "Tests")
    n = 0
    batch = []
    for (sub, subdir), (code, topic) in syllabus.LEGACY_MAP.items():
        for path in glob.glob(os.path.join(tests, sub, subdir, "*.json")):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            for raw in data.get("questions", []):
                q = _legacy_q(raw, code, topic)
                if q:
                    q["subtopic"] = subdir.replace("_", " ")
                    batch.append(_qtuple(q))
    db.many("INSERT OR IGNORE INTO questions(id,subject,topic,subtopic,qtype,text,options,answer,numeric,tol,marks,neg,diff,expl,pool,src)"
            " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", batch)
    n = len(batch)
    # past attempts -> history + retroactive credits
    for path in sorted(glob.glob(os.path.join(base, "Results", "attempt_*.json"))):
        try:
            with open(path, encoding="utf-8") as f:
                a = json.load(f)
        except Exception:
            continue
        aid = "L" + str(a.get("id", os.path.basename(path)))
        if a.get("status") != "submitted" or db.one("SELECT 1 FROM attempts WHERE id=?", (aid,)):
            continue
        sc = a.get("scope", {})
        mp = syllabus.LEGACY_MAP.get((sc.get("subject"), sc.get("subdir")))
        subject = mp[0] if mp else (sc.get("subject") if sc.get("subject") in syllabus.SUBJECT_BY_CODE else None)
        with db.tx():
            ans, credit = [], {}
            for pos, r in enumerate(a.get("rows", [])):
                m = syllabus.LEGACY_MAP.get((sc.get("subject"), (r.get("bank") or "/").split("/")[0]))
                code, topic = m if m else (subject, r.get("topic", "General"))
                if not code:
                    continue
                qt = _norm_type(r.get("qtype"))
                key = r.get("correct_numeric") if qt == "numerical" else r.get("correct_options")
                qid = db.qid_for(r.get("question_text", ""), r.get("options"), key)
                if not db.one("SELECT 1 FROM questions WHERE id=?", (qid,)):
                    continue
                st = "skipped" if (not r.get("selected_options") and r.get("numeric_answer") is None) else (
                    "correct" if r.get("is_correct") else "wrong")
                diff = r.get("difficulty") if r.get("difficulty") in syllabus.DIFFS else "medium"
                c = 0
                if st == "correct":
                    ever = db.one("SELECT ever_correct FROM qstats WHERE qid=?", (qid,))
                    c = game.REPEAT_CREDIT if ever and ever["ever_correct"] else game.DIFF_CREDITS[diff]
                    credit[code] = credit.get(code, 0) + c
                if st != "skipped":
                    db.run("INSERT INTO qstats(qid,seen,correct,ever_correct,last_ts) VALUES(?,1,?,?,?) ON CONFLICT(qid) DO UPDATE SET"
                           " seen=seen+1, correct=correct+excluded.correct, ever_correct=MAX(ever_correct,excluded.ever_correct)",
                           (qid, int(st == "correct"), int(st == "correct"), a.get("submitted_at", "")))
                ans.append((aid, pos, qid, code, topic, diff, json.dumps(r.get("selected_options") or []),
                            r.get("numeric_answer"), r.get("time_spent_sec", 0), 0, st, r.get("marks_obtained", 0), c,
                            a.get("submitted_at", "")))
            db.run("INSERT INTO attempts(id,kind,mode,title,subject,minutes,created_at,submitted_at,status,items,state,score,max_marks,"
                   "correct,wrong,skipped,used_sec,violations,credits,events) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (aid, "legacy", "exam", sc.get("title", "Earlier test"), subject, a.get("minutes", 0),
                    a.get("created_at"), a.get("submitted_at"), "submitted",
                    json.dumps([{"qid": x[2], "sec": x[3]} for x in ans]), "{}", a.get("score", 0), a.get("max_marks", 0),
                    a.get("correct_count", 0), a.get("wrong_count", 0), a.get("skipped_count", 0),
                    a.get("duration_used_sec", 0), a.get("violations", 0), sum(credit.values()), "[]"))
            db.many("INSERT OR REPLACE INTO answers(attempt_id,pos,qid,subject,topic,diff,selected,numeric,time_sec,marked,state,got,credit,ts)"
                    " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", ans)
            day = (a.get("submitted_at") or "")[:10]
            db.many("INSERT INTO ledger(ts,day,attempt_id,subject,amount,reason) VALUES(?,?,?,?,?,?)",
                    [(a.get("submitted_at"), day, aid, c, v, "legacy") for c, v in credit.items()])
    return n


def ensure_ready():
    db.heal()
    db.init()
    from . import version
    pack_sig = _pack_sig()
    if db.get_setting("app_version") != version.VERSION or db.get_setting("pack_sig") != pack_sig or db.get_setting("tests_ver") != TESTS_VER:
        db.backup("pre-update")           # progress is never lost: a restorable copy before every migration
        db.set_setting("app_version", version.VERSION)
    seed_syllabus()
    if db.get_setting("pack_sig") != pack_sig:
        load_pack()
        db.set_setting("pack_sig", pack_sig)
    if not db.get_setting("legacy_done") and not os.environ.get("GATEPREP_NO_PYQ"):
        for base in {db.APP_DIR, os.path.dirname(db.DATA_DIR)}:
            if os.path.isdir(os.path.join(base, "Tests")):
                import_legacy(base)
        db.set_setting("legacy_done", True)
    if db.get_setting("tests_ver") != TESTS_VER:
        db.run("DELETE FROM tests WHERE id NOT IN (SELECT test_id FROM attempts WHERE test_id IS NOT NULL)")
        db.run("DELETE FROM tests WHERE kind='mini'")
        db.set_setting("tests_ver", TESTS_VER)
        db.set_setting("tests_sig", None)
    if db.one("SELECT COUNT(*) n FROM tests")["n"] == 0 or db.get_setting("tests_sig") != pack_sig:
        builder.build_tests()
        db.set_setting("tests_sig", pack_sig)
