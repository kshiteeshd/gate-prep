"""Credits, levels and unlock rules."""
from datetime import date, datetime, timedelta

from . import db

DIFF_CREDITS = {"easy": 2, "medium": 4, "hard": 7}
REPEAT_CREDIT = 1
BONUS = {"dpp": 5, "small": 10, "sfull": 25, "full": 40}
MAX_LEVEL = 12
SUBJ_SCALE, ALL_SCALE = 25, 60
SMALL_PER_SUBJECT = 10
SFULL_PER_SUBJECT = 4
DPP_SIZE = 30
MAX_DPP_PER_TOPIC = 8
FULL_TESTS = 30
TITLES = ["Rookie", "Learner", "Practitioner", "Solver", "Strategist", "Specialist",
          "Expert", "Master", "Grandmaster", "Champion", "Legend", "GATE Topper"]


def thresh(n, scale):
    """Credits needed to reach level n."""
    return scale * (n - 1) * (n + 2)


def level_info(credits, scale):
    lv = 1
    while lv < MAX_LEVEL and credits >= thresh(lv + 1, scale):
        lv += 1
    lo = thresh(lv, scale)
    hi = thresh(lv + 1, scale) if lv < MAX_LEVEL else lo
    pct = 100 if lv == MAX_LEVEL else int((credits - lo) * 100 / (hi - lo))
    return {"level": lv, "title": TITLES[lv - 1], "credits": credits, "lo": lo, "hi": hi,
            "pct": pct, "to_next": max(0, hi - credits), "max": lv == MAX_LEVEL}


def small_unlock_level(no):
    return 1 + (no - 1) // 2


def sfull_unlock_level(no):
    return 1 + 2 * no


def full_unlock_level(no):
    return 1 + (no - 1) * (MAX_LEVEL - 1) // (FULL_TESTS - 1)


def subject_credits():
    out = {r["subject"]: r["t"] for r in db.rows("SELECT subject, SUM(amount) t FROM ledger GROUP BY subject")}
    return out


def snapshot():
    sc = subject_credits()
    total = sum(sc.values())
    subj = {s["code"]: level_info(sc.get(s["code"], 0), SUBJ_SCALE) for s in db.rows("SELECT code FROM subjects")}
    return {"subjects": subj, "overall": level_info(total, ALL_SCALE), "total": total}


def award(attempt_id, entries):
    """entries: [(subject_code_or_ALL, amount, reason)]. Returns list of event dicts (level-ups / unlocks)."""
    entries = [e for e in entries if e[1]]
    if not entries:
        return []
    before = snapshot()
    now = datetime.now()
    db.many("INSERT INTO ledger(ts,day,attempt_id,subject,amount,reason) VALUES(?,?,?,?,?,?)",
            [(now.isoformat(timespec="seconds"), now.date().isoformat(), attempt_id, s, a, r) for s, a, r in entries])
    after = snapshot()
    ev = []
    for code, inf in after["subjects"].items():
        b = before["subjects"][code]["level"]
        if inf["level"] > b:
            names = [r["title"] for r in db.rows(
                "SELECT title FROM tests WHERE kind IN ('small','sfull') AND subject=? AND unlock_level>? AND unlock_level<=? ORDER BY kind, no",
                (code, b, inf["level"]))]
            ev.append({"type": "level", "scope": code, "from": b, "to": inf["level"],
                       "title": inf["title"], "unlocked": names})
    if after["overall"]["level"] > before["overall"]["level"]:
        b, a = before["overall"]["level"], after["overall"]["level"]
        names = [r["title"] for r in db.rows(
            "SELECT title FROM tests WHERE kind='full' AND unlock_level>? AND unlock_level<=? ORDER BY no", (b, a))]
        ev.append({"type": "level", "scope": "ALL", "from": b, "to": a,
                   "title": after["overall"]["title"], "unlocked": names})
    return ev


def streak():
    days = {r["day"] for r in db.rows("SELECT DISTINCT day FROM ledger")}
    d = date.today()
    if d.isoformat() not in days:
        d -= timedelta(days=1)
    n = 0
    while d.isoformat() in days:
        n += 1
        d -= timedelta(days=1)
    return n


def today_answered():
    t = date.today().isoformat()
    return db.one("SELECT COUNT(*) n FROM answers WHERE substr(ts,1,10)=? AND state!='skipped'", (t,))["n"]
