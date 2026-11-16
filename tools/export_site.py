"""Export the question bank, tests and lessons to static JSON for the web app (web/data).

    python tools/export_site.py             # everything present locally (desktop build)
    python tools/export_site.py --public    # leaves out past-paper (PYQ) questions: used for GitHub Pages

The same files are served by GitHub Pages and by the desktop app, so both always show the same content.
"""
import argparse
import re
import hashlib
import json
import os
import shutil
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))


def _pick(rng, pool, n):
    """n questions from pool, balanced by difficulty (30% easy, 50% medium, 20% hard) and spread over sub-topics."""
    by = {"easy": [], "medium": [], "hard": []}
    for q in pool:
        by.setdefault(q["diff"], []).append(q)
    for v in by.values():
        rng.shuffle(v)
    want = {"easy": round(n * .3), "hard": round(n * .2)}
    want["medium"] = n - want["easy"] - want["hard"]
    out = []
    for d in ("easy", "medium", "hard"):
        out += by[d][:want[d]]
    rest = [q for d in by for q in by[d] if q not in out]
    rng.shuffle(rest)
    out += rest[:n - len(out)]
    order = {"easy": 0, "medium": 1, "hard": 2}
    return sorted(out, key=lambda q: (order.get(q["diff"], 1), q["id"]))


def structured_tests(db, LESSONS):
    import random
    subjects = sorted({l["subject"] for l in LESSONS if l.get("section")})
    out = []
    for code in subjects:
        rows = db.rows("SELECT id, topic, subtopic, diff, marks, pool FROM questions WHERE active=1 AND subject=? ORDER BY id", (code,))
        ls = [l for l in LESSONS if l["subject"] == code]

        def pool_for(topics, subs=None):
            cand = [r for r in rows if r["topic"] in topics and (subs is None or r["subtopic"] in subs) and not str(r["subtopic"] or "").startswith("GATE")]
            test = [dict(r) for r in cand if r["pool"] == "test"]
            return test if len(test) >= 12 else test + [dict(r) for r in cand if r["pool"] != "test"]

        def mk(tid, kind, topic, no, title, qs, mins):
            return {"id": tid, "k": kind, "s": code, "t": topic, "n": no, "ti": title, "m": mins, "q": [q["id"] for q in qs], "sec": [""] * len(qs), "u": [code]}
        sections = []
        for l in ls:
            if l["section"] not in sections:
                sections.append(l["section"])
        for si, sec in enumerate(sections, 1):
            sls = [l for l in ls if l["section"] == sec]
            topics = list(dict.fromkeys(l["topic"] for l in sls))
            qs = _pick(random.Random("sect" + code + sec), pool_for(topics), 30)
            if len(qs) >= 15:
                out.append(mk("sect-%s-%d" % (code, si), "sect", "", si, "Section test · " + sec, qs, 75))
            for ch in dict.fromkeys(l["ch_no"] for l in sls):
                cls = [l for l in sls if l["ch_no"] == ch]
                qs = _pick(random.Random("chap" + code + cls[0]["topic"]), pool_for([cls[0]["topic"]]), 20)
                if len(qs) >= 10:
                    out.append(mk("chap-%s-%s" % (code, re.sub(r"[^a-z0-9]+", "-", cls[0]["topic"].lower()).strip("-")), "chap", cls[0]["topic"], ch,
                                  "Chapter %d test · %s" % (ch, cls[0]["chapter"]), qs, 50))
                for l in cls:
                    if not l.get("subs"):
                        continue
                    qs = _pick(random.Random("sub" + l["slug"]), pool_for([l["topic"]], set(l["subs"])), 10)
                    if len(qs) >= 6:
                        out.append(mk("sub-" + l["slug"], "sub", l["topic"], l["no"], "%d.%d %s" % (ch, l["no"], l["title"]), qs, 25))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--public", action="store_true")
    ap.add_argument("--out", default=os.path.join(ROOT, "web", "data"))
    a = ap.parse_args()

    tmp = tempfile.mkdtemp(prefix="gp_export_")
    os.environ["GATEPREP_HOME"] = tmp                     # scratch database, never the user's
    if a.public:
        os.environ["GATEPREP_NO_PYQ"] = "1"
    from gate import db, seed, syllabus, version
    import learn
    from learn.tex import typeset
    seed.ensure_ready()

    if os.path.isdir(a.out):
        shutil.rmtree(a.out)

    # ---- questions, one file per subject ----
    by, subj_of = {}, {}
    for r in db.rows("SELECT * FROM questions WHERE active=1 ORDER BY subject, topic, id"):
        opts = json.loads(r["options"] or "[]")
        ans = json.loads(r["answer"] or "[]")
        q = {"i": r["id"], "t": r["topic"], "s": r["subtopic"] or "", "y": {"single": "s", "multiple": "m", "numerical": "n"}[r["qtype"]],
             "x": r["text"], "m": r["marks"], "d": r["diff"][0], "e": r["expl"] or "", "p": r["pool"]}
        if r["qtype"] == "numerical":
            q["a"] = r["numeric"]
            if r["tol"]:
                q["tol"] = r["tol"]
        else:
            q["o"] = opts
            q["a"] = sorted(opts.index(t) for t in ans if t in opts)
            if r["qtype"] == "single" and r["neg"]:
                q["n"] = round(r["neg"], 4)
        if str(r["src"]).startswith("GATE"):
            q["r"] = r["src"]
        by.setdefault(r["subject"], []).append(q)
        subj_of[r["id"]] = r["subject"]
    for code, qs in by.items():
        dump(os.path.join(a.out, "q", code + ".json"), qs)

    # ---- tests: dpp / small / sfull per subject and the all-subject mocks ----
    tests = []
    for r in db.rows("SELECT * FROM tests ORDER BY kind, subject, topic, no"):
        items = json.loads(r["items"])
        tests.append({"id": r["id"], "k": r["kind"], "s": r["subject"] or "", "t": r["topic"] or "", "n": r["no"], "ti": r["title"],
                      "m": r["minutes"], "q": [x["qid"] for x in items], "sec": [x.get("sec", "") for x in items],
                      "u": sorted({subj_of[x["qid"]] for x in items if x["qid"] in subj_of})})
    dump(os.path.join(a.out, "tests.json"), tests)

    # ---- lessons ----
    learn.load_all()
    from learn import compose
    from learn.chapters import assign_subs
    avail = {}
    for r in db.rows("SELECT DISTINCT subject, topic, subtopic FROM questions WHERE active=1 AND pool='dpp'"):
        if r["subtopic"] and not str(r["subtopic"]).startswith("GATE"):
            avail.setdefault((r["subject"], r["topic"]), []).append(r["subtopic"])
    assign_subs(learn.LESSONS, avail)
    index = []
    for l in learn.LESSONS:
        full = {
            "slug": l["slug"], "subject": l["subject"], "section": l.get("section", ""), "ch_no": l["ch_no"], "chapter": l["chapter"], "no": l["no"], "title": l["title"],
            "topic": l["topic"], "subs": l.get("subs", []), "credits": l.get("credits", 20),"minutes": l["minutes"], "weight": l["weight"], "widget": l["widget"], "hint": l.get("widget_hint", ""),
            "key": str(learn.mdi(l.get("key", ""))),
            "analogy": [l["analogy"][0], l["analogy"][1], str(learn.md(l["analogy"][2]))] if l.get("analogy") else None,
            "book": [[h, str(learn.md(b))] for h, b in l.get("book", [])],
            "sections": [{"h": s["h"], "html": str(learn.md(s["md"])),
                          "formulas": [[typeset(f[0]), f[1] if len(f) > 1 else ""] for f in s.get("formulas", [])],
                          "call": [[c[0], c[1], str(learn.md(c[2]))] for c in s.get("call", [])]} for s in l["sections"]],
            "examples": [{"title": e.title, "problem": str(learn.md(e.problem)), "steps": [str(learn.md(x)) for x in e.steps], "answer": str(learn.md(e.answer))}
                         for e in l["examples"]],
            "proofs": [[p[0], str(learn.md(p[1]))] for p in l.get("proofs", [])],
            "notes": [[p[0], str(learn.md(p[1]))] for p in l.get("notes", [])],
            "traps": [[t[0], str(learn.md(t[1]))] for t in l.get("traps", [])],
            "quick": [[str(learn.mdi(q[0])), list(q[1]), q[2], q[3]] for q in l.get("quick", [])],
            "summary": [str(learn.mdi(b)) for b in l.get("summary", [])],
        }
        dump(os.path.join(a.out, "lesson", l["slug"] + ".json"), full)
        index.append(dict({k: l[k] for k in ("slug", "subject", "ch_no", "chapter", "no", "title", "topic", "minutes", "weight", "widget")}, section=l.get("section", "")))

    # ---- structured tests: one per section, chapter and sub-chapter (subjects organised into sections) ----
    tests += structured_tests(db, learn.LESSONS)
    dump(os.path.join(a.out, "tests.json"), tests)

    # ---- meta ----
    meta = {"version": version.VERSION, "built": time.strftime("%Y-%m-%d"), "public": bool(a.public),
            "subjects": [dict(s, topics=syllabus.TOPICS[s["code"]], n=len(by.get(s["code"], []))) for s in syllabus.SUBJECTS],
            "lessons": index, "questions": sum(len(v) for v in by.values()), "moved": compose.MOVED}
    meta["build"] = hashlib.sha1(json.dumps(meta, sort_keys=True).encode()).hexdigest()[:10]
    dump(os.path.join(a.out, "meta.json"), meta)

    size = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(a.out) for f in fs)
    print("exported %d questions, %d tests, %d lessons -> %s (%.1f MB)%s" % (meta["questions"], len(tests), len(index), a.out, size / 1e6,
                                                                              " [public: no past-paper questions]" if a.public else ""))
    db.conn().close()
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
