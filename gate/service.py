"""Attempt lifecycle: create -> (autosave | check) -> submit -> result."""
import json
import random
from datetime import datetime

from . import db, game


def _now():
    return datetime.now().isoformat(timespec="seconds")


def new_id():
    return datetime.now().strftime("%Y%m%d%H%M%S") + "%04x" % random.randrange(65536)


def qrow(r):
    d = dict(r)
    d["options"] = json.loads(d["options"] or "[]")
    d["answer"] = json.loads(d["answer"] or "[]")
    return d


def get_questions(qids):
    if not qids:
        return {}
    marks = ",".join("?" * len(qids))
    return {r["id"]: qrow(r) for r in db.rows("SELECT * FROM questions WHERE id IN (%s)" % marks, qids)}


# ---------- scoring (GATE rules) ----------
def score(q, selected_texts, numeric):
    """-> (state, marks_obtained). state in correct|wrong|skipped"""
    m, neg = float(q["marks"] or 0), float(q["neg"] or 0)
    if q["qtype"] == "numerical":
        if numeric in (None, ""):
            return "skipped", 0.0
        try:
            v = float(numeric)
        except (TypeError, ValueError):
            return "wrong", 0.0
        if q["numeric"] is not None and abs(v - float(q["numeric"])) <= float(q["tol"] or 0) + 1e-9:
            return "correct", m
        return "wrong", 0.0
    if not selected_texts:
        return "skipped", 0.0
    if set(selected_texts) == set(q["answer"]):
        return "correct", m
    return "wrong", (-neg if q["qtype"] == "single" else 0.0)


def correct_display(q):
    if q["qtype"] == "numerical":
        n = q["numeric"]
        s = ("%g" % n) if n is not None else "?"
        return s + (" (±%g)" % q["tol"] if q["tol"] else "")
    return " | ".join(q["answer"])


# ---------- creation ----------
def pick_dpp(subject, topic, subtopic, diff, n):
    """Unseen first, then previously-wrong, then previously-right."""
    sql = ["SELECT q.id FROM questions q LEFT JOIN qstats s ON s.qid=q.id WHERE q.pool='dpp' AND q.active=1"]
    args = []
    for col, val in (("subject", subject), ("topic", topic), ("subtopic", subtopic), ("diff", diff)):
        if val:
            sql.append("AND q.%s=?" % col)
            args.append(val)
    sql.append("ORDER BY CASE WHEN s.seen IS NULL THEN 0 WHEN s.ever_correct=0 THEN 1 ELSE 2 END, RANDOM() LIMIT ?")
    args.append(n)
    return [r["id"] for r in db.rows(" ".join(sql), args)]


def create_dpp(subject=None, topic=None, subtopic=None, diff=None, n=10, title=None):
    qids = pick_dpp(subject, topic, subtopic, diff, n)
    if not qids:
        return None
    qmap = get_questions(qids)
    items = [{"qid": i, "sec": qmap[i]["subject"]} for i in qids]
    t = title or " · ".join(x for x in (subject, topic, (diff or "").title()) if x) or "Daily DPP"
    aid = new_id()
    db.run("INSERT INTO attempts(id,kind,mode,title,subject,topic,diff,minutes,created_at,status,items,state,events)"
           " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
           (aid, "dpp", "practice", t, subject, topic, diff, 0, _now(), "running", json.dumps(items), "{}", "[]"))
    return aid


def create_test_attempt(test_id):
    t = db.one("SELECT * FROM tests WHERE id=?", (test_id,))
    if not t:
        return None
    ex = db.one("SELECT id FROM attempts WHERE test_id=? AND status='running'", (test_id,))
    if ex:
        return ex["id"]
    aid = new_id()
    db.run("INSERT INTO attempts(id,kind,mode,title,subject,topic,test_id,minutes,created_at,status,items,state,events)"
           " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
           (aid, t["kind"], "practice" if t["kind"] == "dpp" else "exam", t["title"], t["subject"], t["topic"], test_id,
            t["minutes"], _now(), "running", t["items"], "{}", "[]"))
    return aid


def is_unlocked(test):
    if test["kind"] == "dpp":
        return True
    snap = game.snapshot()
    lv = snap["overall"]["level"] if test["kind"] == "full" else snap["subjects"][test["subject"]]["level"]
    return lv >= test["unlock_level"]


# ---------- paper ----------
def get_attempt(aid):
    return db.one("SELECT * FROM attempts WHERE id=?", (aid,))


def remaining_sec(a):
    if not a["minutes"]:
        return None
    el = (datetime.now() - datetime.fromisoformat(a["created_at"])).total_seconds()
    return max(0, int(a["minutes"] * 60 - el))


def paper(a):
    items = json.loads(a["items"])
    qm = get_questions([i["qid"] for i in items])
    practice = a["mode"] == "practice"
    out, secs = [], []
    for pos, it in enumerate(items):
        q = qm[it["qid"]]
        d = {"pos": pos, "sec": it["sec"], "qtype": q["qtype"], "text": q["text"], "options": q["options"],
             "marks": q["marks"], "neg": q["neg"] if q["qtype"] == "single" else 0}
        if str(q["src"] if "src" in q.keys() else "").startswith("GATE"):
            d["src"] = q["src"]
        if practice:
            d.update(topic=q["topic"], subtopic=q["subtopic"], diff=q["diff"], subject=q["subject"])
        out.append(d)
        if it["sec"] not in secs:
            secs.append(it["sec"])
    done = {}
    if practice:
        for r in db.rows("SELECT * FROM answers WHERE attempt_id=?", (a["id"],)):
            q = qm[items[r["pos"]]["qid"]]
            done[r["pos"]] = {"state": r["state"], "got": r["got"], "credit": r["credit"],
                              "selected": json.loads(r["selected"] or "[]"), "numeric": r["numeric"],
                              "correct": correct_display(q), "answer": q["answer"], "expl": q["expl"]}
    return {"id": a["id"], "title": a["title"], "kind": a["kind"], "mode": a["mode"], "minutes": a["minutes"],
            "remaining": remaining_sec(a), "sections": secs, "questions": out,
            "state": json.loads(a["state"] or "{}"), "done": done}


# ---------- practice: check one ----------
def _stat_update(qid, correct, answered=True):
    if not answered:
        return
    ts = _now()
    db.run("INSERT INTO qstats(qid,seen,correct,ever_correct,last_ts) VALUES(?,1,?,?,?) "
           "ON CONFLICT(qid) DO UPDATE SET seen=seen+1, correct=correct+?, ever_correct=MAX(ever_correct,?), last_ts=?",
           (qid, int(correct), int(correct), ts, int(correct), int(correct), ts))


def _credit_for(q, state):
    if state != "correct":
        return 0
    st = db.one("SELECT ever_correct FROM qstats WHERE qid=?", (q["id"],))
    if st and st["ever_correct"]:
        return game.REPEAT_CREDIT
    return game.DIFF_CREDITS.get(q["diff"], 2)


def check(a, pos, sel_idx, numeric, time_sec):
    items = json.loads(a["items"])
    if pos < 0 or pos >= len(items):
        return None
    if db.one("SELECT 1 FROM answers WHERE attempt_id=? AND pos=?", (a["id"], pos)):
        return {"error": "already checked"}
    q = get_questions([items[pos]["qid"]])[items[pos]["qid"]]
    texts = [q["options"][i] for i in (sel_idx or []) if 0 <= i < len(q["options"])]
    state, got = score(q, texts, numeric)
    credit = _credit_for(q, state)
    ev = []
    with db.tx():
        db.run("INSERT INTO answers(attempt_id,pos,qid,subject,topic,diff,selected,numeric,time_sec,marked,state,got,credit,ts)"
               " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
               (a["id"], pos, q["id"], q["subject"], q["topic"], q["diff"], json.dumps(texts),
                None if numeric in (None, "") else float(numeric), int(time_sec or 0), 0, state, got, credit, _now()))
        ev = game.award(a["id"], [(q["subject"], credit, "dpp")]) if credit else []
        _stat_update(q["id"], state == "correct", state != "skipped")
        if ev:
            old = json.loads(a["events"] or "[]")
            db.run("UPDATE attempts SET events=? WHERE id=?", (json.dumps(old + ev), a["id"]))
    snap = game.snapshot()
    return {"state": state, "got": got, "credit": credit, "correct": correct_display(q), "answer": q["answer"],
            "expl": q["expl"], "events": ev, "subject_level": snap["subjects"][q["subject"]],
            "today": game.today_answered()}


# ---------- submit ----------
def submit(a, state, violations=0, used_sec=0):
    if a["status"] == "submitted":
        return a["id"]
    items = json.loads(a["items"])
    qm = get_questions([i["qid"] for i in items])
    practice = a["mode"] == "practice"
    entries, subj_credit = [], {}
    sc = mx = 0.0
    cc = wc = sk = 0
    rows = []
    stored = {r["pos"]: r for r in db.rows("SELECT * FROM answers WHERE attempt_id=?", (a["id"],))} if practice else {}
    ans = (state or {}).get("ans", {})
    marked = set(int(x) for x in (state or {}).get("marked", []))
    for pos, it in enumerate(items):
        q = qm[it["qid"]]
        mx += float(q["marks"] or 0)
        if practice:
            r = stored.get(pos)
            if r:
                sc += r["got"]
                cc += r["state"] == "correct"
                wc += r["state"] == "wrong"
                sk += r["state"] == "skipped"
            else:
                sk += 1
            continue
        an = ans.get(str(pos), {}) or {}
        texts = [q["options"][i] for i in an.get("sel", []) if 0 <= i < len(q["options"])]
        num = an.get("num")
        s, got = score(q, texts, num)
        credit = _credit_for(q, s)
        sc += got
        cc += s == "correct"
        wc += s == "wrong"
        sk += s == "skipped"
        try:
            numv = float(num) if num not in (None, "") else None
        except (TypeError, ValueError):
            numv = None
        rows.append((a["id"], pos, q["id"], q["subject"], q["topic"], q["diff"], json.dumps(texts), numv,
                     int(an.get("t", 0) or 0), int(pos in marked), s, got, credit, _now()))
        if credit:
            subj_credit[q["subject"]] = subj_credit.get(q["subject"], 0) + credit
        if s != "skipped":
            _stat_update(q["id"], s == "correct")
    answered = cc + wc
    events = json.loads(a["events"] or "[]")
    total_credit = sum(r["credit"] for r in stored.values()) if practice else sum(subj_credit.values())
    with db.tx():
        if not practice:
            db.many("INSERT OR REPLACE INTO answers(attempt_id,pos,qid,subject,topic,diff,selected,numeric,time_sec,marked,state,got,credit,ts)"
                    " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
            entries = [(s, c, a["kind"]) for s, c in subj_credit.items()]
        bonus = 0
        if answered >= max(1, len(items) // 2):
            bonus = game.BONUS.get(a["kind"], 0)
            if answered >= 5 and cc / answered >= 0.7:
                bonus += int(round(0.2 * total_credit))
        if bonus:
            entries.append((a["subject"] if a["kind"] in ("small", "sfull") and a["subject"] else
                            ("ALL" if a["kind"] == "full" else (a["subject"] or "ALL")), bonus, "bonus"))
        ev = game.award(a["id"], entries)
        total_credit += bonus
        db.run("UPDATE attempts SET status='submitted', submitted_at=?, score=?, max_marks=?, correct=?, wrong=?, skipped=?,"
               " used_sec=?, violations=?, credits=?, events=?, state=? WHERE id=?",
               (_now(), sc, mx, cc, wc, sk, int(used_sec or 0), int(violations or 0), total_credit,
                json.dumps(events + ev), json.dumps(state or {}), a["id"]))
    return a["id"]


# ---------- result ----------
def result(a):
    items = json.loads(a["items"])
    qm = get_questions([i["qid"] for i in items])
    ans = {r["pos"]: r for r in db.rows("SELECT * FROM answers WHERE attempt_id=?", (a["id"],))}
    review, by_sub, by_topic, by_diff = [], {}, {}, {}
    for pos, it in enumerate(items):
        q = qm[it["qid"]]
        r = ans.get(pos)
        state = r["state"] if r else "skipped"
        got = r["got"] if r else 0
        sel = json.loads(r["selected"]) if r and r["selected"] else []
        review.append({"pos": pos + 1, "qid": q["id"], "sec": it["sec"], "subject": q["subject"], "topic": q["topic"],
                       "diff": q["diff"], "qtype": q["qtype"], "text": q["text"], "options": q["options"],
                       "answer": q["answer"], "correct": correct_display(q), "expl": q["expl"], "state": state,
                       "got": got, "marks": q["marks"], "selected": sel,
                       "numeric": r["numeric"] if r else None, "time": r["time_sec"] if r else 0,
                       "marked": bool(r["marked"]) if r else False})
        for d, key in ((by_sub, q["subject"]), (by_topic, q["subject"] + " · " + q["topic"]), (by_diff, q["diff"])):
            x = d.setdefault(key, {"name": key, "n": 0, "c": 0, "w": 0, "s": 0, "marks": 0.0, "max": 0.0, "t": 0})
            x["n"] += 1
            x["c"] += state == "correct"
            x["w"] += state == "wrong"
            x["s"] += state == "skipped"
            x["marks"] += got
            x["max"] += q["marks"]
            x["t"] += r["time_sec"] if r else 0
    srt = lambda d, k: sorted(d.values(), key=k)
    return {"a": dict(a), "review": review, "events": json.loads(a["events"] or "[]"),
            "by_subject": srt(by_sub, lambda x: x["name"]),
            "by_topic": srt(by_topic, lambda x: (x["c"] / x["n"], x["name"])),
            "by_diff": [by_diff[k] for k in ("easy", "medium", "hard") if k in by_diff]}
