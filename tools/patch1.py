import re
R = "E:/Test Platform/"


def sub(path, pairs):
    s = open(R + path, encoding="utf-8").read()
    for a, b in pairs:
        if a not in s:
            print("MISSING in", path, ":", a[:60])
        s = s.replace(a, b)
    open(R + path, "w", encoding="utf-8").write(s)


sub("gate/game.py", [
    ('BONUS = {"dpp": 5, "mini": 10, "full": 40}', 'BONUS = {"dpp": 5, "small": 10, "sfull": 25, "full": 40}'),
    ('MINIS_PER_SUBJECT = 10', 'SMALL_PER_SUBJECT = 10\nSFULL_PER_SUBJECT = 4\nDPP_SIZE = 30\nMAX_DPP_PER_TOPIC = 8'),
    ('def mini_unlock_level(no):\n    return 1 + (no - 1) // 2', 'def small_unlock_level(no):\n    return 1 + (no - 1) // 2\n\n\ndef sfull_unlock_level(no):\n    return 1 + 2 * no'),
    ("WHERE kind='mini' AND subject=? AND unlock_level>? AND unlock_level<=? ORDER BY no", "WHERE kind IN ('small','sfull') AND subject=? AND unlock_level>? AND unlock_level<=? ORDER BY kind, no"),
])
sub("gate/db.py", [
    ("id TEXT PRIMARY KEY, kind TEXT, subject TEXT, no INT, title TEXT, minutes INT, items TEXT, unlock_level INT);",
     "id TEXT PRIMARY KEY, kind TEXT, subject TEXT, topic TEXT, no INT, title TEXT, minutes INT, items TEXT, unlock_level INT);"),
    ("def init():\n    conn().executescript(SCHEMA)",
     'def init():\n    conn().executescript(SCHEMA)\n    if "topic" not in [r["name"] for r in rows("PRAGMA table_info(tests)")]:\n        run("ALTER TABLE tests ADD COLUMN topic TEXT")'),
])
sub("gate/service.py", [
    ('''    db.run("INSERT INTO attempts(id,kind,mode,title,subject,test_id,minutes,created_at,status,items,state,events)"
           " VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
           (aid, t["kind"], "exam", t["title"], t["subject"], test_id, t["minutes"], _now(), "running",
            t["items"], "{}", "[]"))''',
     '''    db.run("INSERT INTO attempts(id,kind,mode,title,subject,topic,test_id,minutes,created_at,status,items,state,events)"
           " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
           (aid, t["kind"], "practice" if t["kind"] == "dpp" else "exam", t["title"], t["subject"], t["topic"], test_id,
            t["minutes"], _now(), "running", t["items"], "{}", "[]"))'''),
    ('''    snap = game.snapshot()
    lv = snap["overall"]["level"] if test["kind"] == "full" else snap["subjects"][test["subject"]]["level"]
    return lv >= test["unlock_level"]''',
     '''    if test["kind"] == "dpp":
        return True
    snap = game.snapshot()
    lv = snap["overall"]["level"] if test["kind"] == "full" else snap["subjects"][test["subject"]]["level"]
    return lv >= test["unlock_level"]'''),
    ('a["kind"] == "mini" and a["subject"]', 'a["kind"] in ("small", "sfull") and a["subject"]'),
])
sub("gate/seed.py", [
    ('''    if db.one("SELECT COUNT(*) n FROM tests")["n"] == 0 or db.get_setting("tests_sig") != pack_sig:''',
     '''    TESTS_VER = 3   # bump when the test structure changes
    if db.get_setting("tests_ver") != TESTS_VER:
        db.run("DELETE FROM tests WHERE id NOT IN (SELECT test_id FROM attempts WHERE test_id IS NOT NULL)")
        db.run("DELETE FROM tests WHERE kind='mini'")
        db.set_setting("tests_ver", TESTS_VER)
        db.set_setting("tests_sig", None)
    if db.one("SELECT COUNT(*) n FROM tests")["n"] == 0 or db.get_setting("tests_sig") != pack_sig:'''),
])
