"""One-time bridge: turn the progress kept by the previous (Flask) version of GATE Prep into the saved state used by the new web app.

The old tables are only read, never changed, so nothing is lost if this is run again."""
from . import db


def _day(ts):
    return (ts or "")[:10]


def from_legacy():
    S = {"v": 1, "theme": "paper", "size": "md", "density": "comfortable", "dry": False, "subject": "ALGO", "days": {}, "cnt": {}, "credits": 0,
         "solved": 0, "acc": {}, "qs": {}, "review": {}, "lessons": {}, "tests": [], "running": {}, "done": {}, "tab": {}, "migrated": True}
    try:
        for r in db.rows("SELECT slug, ts FROM learn_progress"):
            S["lessons"][r["slug"]] = {"done": _day(r["ts"])}
        ans = db.rows("SELECT attempt_id, qid, subject, topic, state, time_sec, ts FROM answers WHERE state!='skipped' ORDER BY ts")
        last = {}
        for r in ans:
            k = "%s|%s" % (r["subject"], r["topic"])
            a = S["acc"].setdefault(k, [0, 0])
            a[0] += 1
            ok = r["state"] == "correct"
            a[1] += 1 if ok else 0
            S["solved"] += 1
            st = S["qs"].setdefault(r["qid"], [0, 0, ""])
            st[0] += 1
            st[1] += 1 if ok else 0
            st[2] = _day(r["ts"])
            S["cnt"][_day(r["ts"])] = S["cnt"].get(_day(r["ts"]), 0) + 1
            last[r["qid"]] = ok
        today = db.one("SELECT date('now','localtime') d")["d"]
        for qid, ok in last.items():
            if not ok:                                 # questions last answered wrong start in the review queue
                S["review"][qid] = {"stage": 0, "due": today}
        for r in db.rows("SELECT day, SUM(amount) c FROM ledger GROUP BY day"):
            if r["day"]:
                S["days"][r["day"]] = r["c"]
                S["credits"] += r["c"]
        items = {}
        for r in db.rows("SELECT attempt_id, qid, state, time_sec FROM answers ORDER BY attempt_id, pos"):
            items.setdefault(r["attempt_id"], []).append({"id": r["qid"], "ok": r["state"] == "correct", "skipped": r["state"] == "skipped", "t": r["time_sec"] or 0})
        for a in db.rows("SELECT * FROM attempts WHERE status='submitted' ORDER BY submitted_at"):
            S["tests"].append({"id": a["id"], "tid": a["test_id"] or a["id"], "title": a["title"], "kind": a["kind"], "when": _day(a["submitted_at"]), "dry": False,
                               "used": a["used_sec"] or 0, "minutes": a["minutes"] or 0, "items": items.get(a["id"], []), "score": a["score"] or 0, "max": a["max_marks"] or 0})
            if a["test_id"]:
                d = S["done"].setdefault(a["test_id"], {"best": -1e9, "max": a["max_marks"] or 0, "n": 0})
                d["best"] = max(d["best"], round(a["score"] or 0, 2))
                d["n"] += 1
    except Exception as e:                              # a damaged old table must never stop the app from starting
        S["migrate_error"] = str(e)
    return S
