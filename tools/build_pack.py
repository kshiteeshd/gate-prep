"""Run all generators + curated files -> content/pack.json (the question pack shipped with the app).
   Usage: python tools/build_pack.py"""
import collections
import hashlib
import importlib
import json
import os
import pkgutil
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("PYTHONHASHSEED") != "0":      # string-set ordering must not change between builds, or question ids would drift
    os.environ["PYTHONHASHSEED"] = "0"
    sys.exit(__import__("subprocess").call([sys.executable] + sys.argv, env=os.environ))
sys.path.insert(0, ROOT)
from content import kit  # noqa: E402
from gate import db, syllabus  # noqa: E402

for m in sorted(pkgutil.iter_modules([os.path.join(ROOT, "content")]), key=lambda m: m.name):
    if m.name.startswith(("g_", "c_")):
        importlib.import_module("content." + m.name)


def seeded(*parts):
    return random.Random(int(hashlib.sha1("|".join(map(str, parts)).encode()).hexdigest()[:12], 16))


def numeric_to_mcq(q, rng):
    """Turn a NAT question into an MCQ with plausible numeric distractors."""
    v = q["numeric"]
    if abs(v) > 1e12:
        return q
    if float(v).is_integer():
        v = int(v)
        base = [v + 1, v - 1, v + 2, v - 2, v * 2, v // 2, v + 3, v - 3, v + 10, v - 10, v * 3, int(v * 1.5), v + 5, v - 5, v + 4, v - 4]
        base = [b for b in base if b != v and (b >= 0 or v < 0)]
    else:
        d = len(repr(round(v, 6)).split(".")[1].rstrip("0")) if "." in repr(v) else 2
        d = max(1, min(d, 4))
        base = [round(v * f, d) for f in (0.5, 0.75, 1.25, 1.5, 2, 0.25, 0.8, 1.2, 0.9, 1.1)]
        base = [b for b in base if b != round(v, d) and (b >= 0 or v < 0)]
    base = list(dict.fromkeys(base))
    if len(base) < 3:
        return q
    rng.shuffle(base)
    cs = kit.fmt(v if isinstance(v, int) else round(v, 4))
    opts = [cs] + [kit.fmt(x) for x in base[:3]]
    if len(set(opts)) != 4:
        return q
    opts.sort(key=float)
    q.update(qtype="single", options=opts, answer=[cs])
    q.pop("numeric", None)
    q.pop("tol", None)
    return q


def finish(q):
    q["neg"] = 0 if q["qtype"] != "single" else (0.33 if q["marks"] == 1 else 0.66)
    q["id"] = db.qid_for(q["text"], q.get("options"), q["answer"] if q["qtype"] != "numerical" else q["numeric"])
    return q


def validate(q):
    assert q["subject"] in syllabus.SUBJECT_BY_CODE, q
    assert q["topic"] in syllabus.TOPICS[q["subject"]], (q["subject"], q["topic"])
    assert q["diff"] in syllabus.DIFFS and q["marks"] in (1, 2), q
    if q["qtype"] == "numerical":
        assert q.get("numeric") is not None
    else:
        assert len(set(q["options"])) == len(q["options"]) >= 4, q
        assert all(a in q["options"] for a in q["answer"]) and q["answer"], q
        if q["qtype"] == "single":
            assert len(q["answer"]) == 1, q
        else:
            assert 1 <= len(q["answer"]) < len(q["options"]), q


def norm(t):
    return " ".join((t or "").lower().split())


def enrich(q):
    """Append the concept note for the question's sub-topic (what the rule is, how to apply it, the usual trap)."""
    from content import notes_a, notes_b, notes_c  # noqa: F401  (they register into notes_a.N)
    note = notes_a.N.get((q["subject"], q["topic"], q["subtopic"])) or notes_a.N.get((q["subject"], None, q["subtopic"]))
    if not note:
        return False
    idea, method, trap = note
    parts = [(q.get("expl") or "").strip()] if (q.get("expl") or "").strip() else []
    parts += ["Concept: " + idea, "Method: " + method, "Watch out: " + trap]
    q["expl"] = "\n\n".join(parts)
    return True


def main():
    qs, seen_text = [], set()
    stats = collections.Counter()
    for g in kit.REG:
        made = 0
        for i in range(g["n"] * 8):
            if made >= g["n"]:
                break
            r = seeded(g["name"], i)
            try:
                q = g["f"](r)
            except kit.Skip:
                continue
            key = q["text"] + "|" + "|".join(q.get("options", []))
            if key in seen_text:
                continue
            seen_text.add(key)
            hsh = int(hashlib.sha1((g["name"] + str(i)).encode()).hexdigest()[:6], 16)
            marks = 2 if (g["marks"] == 2 or g["diff"] == "hard" or (g["diff"] == "medium" and hsh % 2 == 0)) else 1
            q.update(subject=g["subject"], topic=g["topic"], subtopic=g["sub"], diff=g["diff"], marks=marks, src="gen")
            if q["qtype"] == "numerical" and hsh % 100 < 62:
                q = numeric_to_mcq(q, seeded("mcq", g["name"], i))
            qs.append(q)
            made += 1
        stats[g["name"]] = made
    for g in kit.CUR:
        for q in kit.build_curated(g, seeded("cur", g["subject"], g["topic"], g["sub"])):
            key = q["text"] + "|" + "|".join(q.get("options", []))
            if key not in seen_text:
                seen_text.add(key)
                qs.append(q)
    out, ids, bad, seen_dup, dup_dropped = [], set(), 0, set(), 0
    for q in qs:
        finish(q)
        try:
            validate(q)
        except AssertionError as e:
            bad += 1
            print("INVALID:", str(e)[:200])
            continue
        if q["id"] in ids:
            continue
        ids.add(q["id"])
        dk = (q["subject"], norm(q["text"]), tuple(sorted(q.get("options", []))))      # same question with options in another order
        if dk in seen_dup:
            dup_dropped += 1
            continue
        seen_dup.add(dk)
        out.append(q)
    # alternate pools inside each (subject, topic, diff, marks) bucket => DPP and Test never share a question
    bucket = collections.defaultdict(list)
    for q in out:
        bucket[(q["subject"], q["topic"], q["diff"], q["marks"])].append(q)
    for k, items in bucket.items():
        seeded("pool", *k).shuffle(items)
        for i, q in enumerate(items):
            q["pool"] = "test" if i % 2 == 0 else "dpp"
    noted = sum(1 for q in out if enrich(q))
    print("concept notes attached to %d of %d questions; duplicates dropped: %d" % (noted, len(out), dup_dropped))
    with open(os.path.join(ROOT, "content", "pack.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print("questions: %d (invalid dropped: %d) generators: %d" % (len(out), bad, len(kit.REG)))
    tab = collections.defaultdict(collections.Counter)
    for q in out:
        tab[q["subject"]][q["pool"] + ":" + q["diff"][0]] += 1
        tab[q["subject"]]["total"] += 1
    for s in syllabus.SUBJECTS:
        c = tab[s["code"]]
        print("%-5s total %5d | test %4d (e%3d m%3d h%3d) | dpp %4d (e%3d m%3d h%3d)" % (
            s["code"], c["total"], sum(v for k, v in c.items() if k.startswith("test")),
            c["test:e"], c["test:m"], c["test:h"], sum(v for k, v in c.items() if k.startswith("dpp")),
            c["dpp:e"], c["dpp:m"], c["dpp:h"]))
    if "--gens" in sys.argv:
        for k, v in sorted(stats.items(), key=lambda x: x[1]):
            print("  %3d %s" % (v, k))


if __name__ == "__main__":
    main()
