"""Sample database used by the SQL playground and by lesson examples (so worked examples are verified on real query results)."""
import sqlite3

SCHEMA = """
CREATE TABLE Dept(dept TEXT PRIMARY KEY, hod TEXT);
CREATE TABLE Student(sid INTEGER PRIMARY KEY, name TEXT, dept TEXT, cgpa REAL, age INTEGER);
CREATE TABLE Course(cid TEXT PRIMARY KEY, title TEXT, credits INTEGER, dept TEXT);
CREATE TABLE Enroll(sid INTEGER, cid TEXT, grade TEXT);
"""
DEPTS = [("CSE", "Rao"), ("ECE", "Iyer"), ("MECH", "Khan"), ("CIVIL", None)]
STUDENTS = [(1, "Asha", "CSE", 9.1, 20), (2, "Bala", "CSE", 8.4, 21), (3, "Chitra", "ECE", 7.9, 20), (4, "Dev", "ECE", 8.8, 22), (5, "Esha", "MECH", 7.2, 21),
            (6, "Farhan", "CSE", 9.5, 22), (7, "Gita", "MECH", None, 20), (8, "Hari", "ECE", 6.8, 23), (9, "Isha", "CSE", 8.4, 20), (10, "Jay", "EEE", 7.5, 21)]
COURSES = [("DB101", "Databases", 4, "CSE"), ("OS101", "Operating Systems", 4, "CSE"), ("DS101", "Data Structures", 3, "CSE"), ("EC201", "Signals", 3, "ECE"), ("ME301", "Thermodynamics", 3, "MECH")]
ENROLLS = [(1, "DB101", "A"), (1, "OS101", "A"), (1, "DS101", "B"), (2, "DB101", "B"), (2, "OS101", "C"), (3, "EC201", "A"), (3, "DS101", "B"), (4, "EC201", "B"),
           (4, "DB101", "A"), (5, "ME301", "C"), (6, "DB101", "A"), (6, "OS101", "A"), (6, "DS101", "A"), (7, "ME301", None), (8, "EC201", "D"), (9, "DB101", "B"), (9, "DS101", None)]


def make():
    c = sqlite3.connect(":memory:")
    c.executescript(SCHEMA)
    c.executemany("INSERT INTO Dept VALUES(?,?)", DEPTS)
    c.executemany("INSERT INTO Student VALUES(?,?,?,?,?)", STUDENTS)
    c.executemany("INSERT INTO Course VALUES(?,?,?,?)", COURSES)
    c.executemany("INSERT INTO Enroll VALUES(?,?,?)", ENROLLS)
    return c


def scalar(sql, *args):
    c = make()
    try:
        r = c.execute(sql, args).fetchall()
        return r[0][0] if len(r) == 1 and len(r[0]) == 1 else r
    finally:
        c.close()


def rows(sql):
    c = make()
    try:
        return c.execute(sql).fetchall()
    finally:
        c.close()


_ALLOWED = {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION, sqlite3.SQLITE_RECURSIVE}


def run_query(sql, limit=200):
    """Execute a single read-only statement. Returns {cols, rows, error}."""
    sql = (sql or "").strip().rstrip(";")
    if not sql or ";" in sql:
        return {"error": "Enter exactly one SELECT statement."}
    if sql.split(None, 1)[0].upper() not in ("SELECT", "WITH"):
        return {"error": "Only SELECT queries are allowed in this playground."}
    c = make()
    c.set_authorizer(lambda action, a, b, db, src: sqlite3.SQLITE_OK if action in _ALLOWED else sqlite3.SQLITE_DENY)
    budget = [2_000_000]

    def tick():
        budget[0] -= 1
        return 1 if budget[0] < 0 else 0
    c.set_progress_handler(tick, 1000)
    try:
        cur = c.execute(sql)
        cols = [d[0] for d in cur.description or []]
        data = cur.fetchmany(limit + 1)
        return {"cols": cols, "rows": [list(r) for r in data[:limit]], "more": len(data) > limit}
    except Exception as e:
        return {"error": str(e)[:200]}
    finally:
        c.close()
