"""SQLite storage. One file: <DATA_DIR>/gateprep.db (WAL mode)."""
import hashlib
import json
import os
import sqlite3
import sys
import threading

FROZEN = getattr(sys, "frozen", False)
APP_DIR = getattr(sys, "_MEIPASS", None) or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.environ.get("GATEPREP_HOME") or (
    os.path.join(os.environ.get("LOCALAPPDATA", APP_DIR), "GATEPrep") if FROZEN else os.path.join(APP_DIR, "data"))
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "gateprep.db")

_local = threading.local()

SCHEMA = """
CREATE TABLE IF NOT EXISTS subjects(code TEXT PRIMARY KEY, name TEXT, glyph TEXT, color TEXT, ord INT, fq INT);
CREATE TABLE IF NOT EXISTS topics(id INTEGER PRIMARY KEY, subject TEXT, name TEXT, ord INT, UNIQUE(subject,name));
CREATE TABLE IF NOT EXISTS questions(
  id TEXT PRIMARY KEY, subject TEXT, topic TEXT, subtopic TEXT, qtype TEXT, text TEXT,
  options TEXT, answer TEXT, numeric REAL, tol REAL, marks REAL, neg REAL,
  diff TEXT, expl TEXT, pool TEXT, src TEXT, active INT DEFAULT 1);
CREATE INDEX IF NOT EXISTS ix_q_pick ON questions(pool, subject, topic, diff);
CREATE TABLE IF NOT EXISTS tests(
  id TEXT PRIMARY KEY, kind TEXT, subject TEXT, topic TEXT, no INT, title TEXT, minutes INT, items TEXT, unlock_level INT);
CREATE TABLE IF NOT EXISTS attempts(
  id TEXT PRIMARY KEY, kind TEXT, mode TEXT, title TEXT, subject TEXT, topic TEXT, diff TEXT, test_id TEXT,
  minutes INT, created_at TEXT, submitted_at TEXT, status TEXT, items TEXT, state TEXT,
  score REAL DEFAULT 0, max_marks REAL DEFAULT 0, correct INT DEFAULT 0, wrong INT DEFAULT 0, skipped INT DEFAULT 0,
  used_sec INT DEFAULT 0, violations INT DEFAULT 0, credits INT DEFAULT 0, events TEXT);
CREATE INDEX IF NOT EXISTS ix_att ON attempts(status, kind, subject);
CREATE TABLE IF NOT EXISTS answers(
  attempt_id TEXT, pos INT, qid TEXT, subject TEXT, topic TEXT, diff TEXT, selected TEXT, numeric REAL,
  time_sec INT, marked INT, state TEXT, got REAL, credit INT DEFAULT 0, ts TEXT,
  PRIMARY KEY(attempt_id,pos));
CREATE INDEX IF NOT EXISTS ix_ans_q ON answers(qid);
CREATE TABLE IF NOT EXISTS qstats(qid TEXT PRIMARY KEY, seen INT DEFAULT 0, correct INT DEFAULT 0, ever_correct INT DEFAULT 0, last_ts TEXT);
CREATE TABLE IF NOT EXISTS ledger(id INTEGER PRIMARY KEY, ts TEXT, day TEXT, attempt_id TEXT, subject TEXT, amount INT, reason TEXT);
CREATE INDEX IF NOT EXISTS ix_led ON ledger(subject, day);
CREATE TABLE IF NOT EXISTS bookmarks(qid TEXT PRIMARY KEY, ts TEXT);
CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS learn_progress(slug TEXT PRIMARY KEY, ts TEXT);
"""


def conn():
    c = getattr(_local, "c", None)
    if c is None:
        c = sqlite3.connect(DB_PATH, timeout=30, isolation_level=None)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("PRAGMA synchronous=NORMAL")
        _local.c = c
    return c


def rows(sql, args=()):
    return conn().execute(sql, args).fetchall()


def one(sql, args=()):
    return conn().execute(sql, args).fetchone()


def run(sql, args=()):
    return conn().execute(sql, args)


def many(sql, seq):
    return conn().executemany(sql, seq)


class tx:
    """with tx(): ...  -> one transaction."""
    def __enter__(self):
        conn().execute("BEGIN")

    def __exit__(self, et, ev, tb):
        conn().execute("ROLLBACK" if et else "COMMIT")


def init():
    conn().executescript(SCHEMA)
    if "topic" not in [r["name"] for r in rows("PRAGMA table_info(tests)")]:
        run("ALTER TABLE tests ADD COLUMN topic TEXT")


def backup(reason="manual", keep=8):
    """Consistent copy of the database into <DATA_DIR>/backups (oldest pruned). Called before anything that rewrites data."""
    import time
    d = os.path.join(DATA_DIR, "backups")
    os.makedirs(d, exist_ok=True)
    dst = os.path.join(d, "gateprep-%s-%s.db" % (time.strftime("%Y%m%d-%H%M%S"), reason))
    if not os.path.exists(DB_PATH) or not one("SELECT 1 FROM sqlite_master WHERE name='attempts'"):
        return None
    b = sqlite3.connect(dst)
    try:
        conn().backup(b)
    finally:
        b.close()
    old = sorted(f for f in os.listdir(d) if f.endswith(".db"))
    for f in old[:-keep]:
        try:
            os.remove(os.path.join(d, f))
        except OSError:
            pass
    return dst


def _is_healthy():
    try:
        return conn().execute("PRAGMA quick_check(1)").fetchone()[0] == "ok"
    except sqlite3.DatabaseError:
        return False


def heal():
    """Open-time safety net. If the database file is damaged, keep a copy of the damaged files, rebuild a clean file and
    salvage every readable row (progress tables first). Content tables are re-seeded from the shipped packs afterwards.
    Returns True when a rebuild happened."""
    import shutil
    import time
    if not os.path.exists(DB_PATH) or _is_healthy():
        return False
    c = getattr(_local, "c", None)
    if c is not None:
        try:
            c.close()
        except sqlite3.Error:
            pass
        _local.c = None
    keep = os.path.join(DATA_DIR, "backups", "damaged-" + time.strftime("%Y%m%d-%H%M%S"))
    os.makedirs(keep, exist_ok=True)
    for ext in ("", "-wal", "-shm"):
        if os.path.exists(DB_PATH + ext):
            shutil.copy2(DB_PATH + ext, os.path.join(keep, "gateprep.db" + ext))
    new_path = DB_PATH + ".rebuild"
    for ext in ("", "-wal", "-shm"):
        if os.path.exists(new_path + ext):
            os.remove(new_path + ext)
    old = sqlite3.connect(DB_PATH, timeout=30)
    old.row_factory = sqlite3.Row
    new = sqlite3.connect(new_path, isolation_level=None)
    new.executescript(SCHEMA)
    new.execute("BEGIN")
    for t in ("attempts", "answers", "qstats", "ledger", "bookmarks", "settings", "learn_progress", "tests", "questions"):
        cols = [r[1] for r in new.execute("PRAGMA table_info(%s)" % t)]
        sql = "INSERT OR IGNORE INTO %s(%s) VALUES(%s)" % (t, ",".join(cols), ",".join("?" * len(cols)))
        try:
            cur = old.execute("SELECT %s FROM %s" % (",".join(cols), t))
            while True:
                try:
                    r = cur.fetchone()
                except sqlite3.DatabaseError:
                    break                      # rest of this damaged table is unreadable
                if r is None:
                    break
                new.execute(sql, tuple(r))
        except sqlite3.DatabaseError:
            pass
    for k in ("pack_sig", "tests_sig", "tests_ver"):   # force content to be re-seeded and tests re-checked
        new.execute("DELETE FROM settings WHERE key=?", (k,))
    new.execute("COMMIT")
    new.close()
    old.close()
    for ext in ("", "-wal", "-shm"):
        if os.path.exists(DB_PATH + ext):
            os.remove(DB_PATH + ext)
    os.replace(new_path, DB_PATH)
    return True


def get_setting(key, default=None):
    r = one("SELECT value FROM settings WHERE key=?", (key,))
    return json.loads(r["value"]) if r else default


def set_setting(key, value):
    run("INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, json.dumps(value)))


def qid_for(text, options, answer):
    s = json.dumps([text, sorted(options or []), answer], sort_keys=True, ensure_ascii=False)
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:12]
