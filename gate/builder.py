"""Builds the fixed test series from the question pools.
   DPP sets   : per subject/topic, 30 questions / 30 min each, drawn from the DPP pool (progressively harder)
   Small tests: per subject, 30 questions / 30 min, mixed topics, from the TEST pool
   Full tests : per subject, 65 questions / 120 min, mixed topics, from the TEST pool
   GATE mocks : 30 all-subject papers (10 GA + 55 CS, 100 marks, 180 min)"""
import json
import random
import re
from collections import Counter

from . import db, game, syllabus

SMALL_Q, SMALL_MIN = 30, 30
SFULL_Q, SFULL_MIN = 65, 120
FULL_MIN = 180


def _tpl(text):
    """Template fingerprint: wording with every number removed, so generated look-alikes share a key."""
    return re.sub(r"\d+(?:\.\d+)?", "#", re.sub(r"\s+", " ", (text or "").lower()))[:48]


def _pool(which):
    out = {}
    for r in db.rows("SELECT id, subject, topic, subtopic, diff, marks, src, substr(text,1,120) txt FROM questions WHERE pool=? AND active=1", (which,)):
        d = dict(r)
        d["tpl"] = _tpl(d.pop("txt"))
        out.setdefault(r["subject"], []).append(d)
    return out


def _pick(cands, n, used, topic_ct, diff_ct, target, rng, chosen, marks=None):
    res = []
    spread = Counter()          # how often each sub-topic / wording template is already in this paper
    for _ in range(n):
        pool = [c for c in cands if c["id"] not in chosen and (marks is None or (c["marks"] == 1) == (marks == 1))]
        if not pool:
            pool = [c for c in cands if c["id"] not in chosen]
        if not pool:
            break
        best = min(pool, key=lambda c: (used[c["id"]], spread[("t", c.get("tpl"))] >= 2, spread[("s", c.get("subtopic"))],
                                        0 if (str(c.get("src", "")).startswith("GATE") and rng.random() < 0.5) else 1,
                                        diff_ct[c["diff"]] >= target.get(c["diff"], 99), topic_ct[(c["subject"], c["topic"])],
                                        spread[("t", c.get("tpl"))], rng.random()))
        spread[("t", best.get("tpl"))] += 1
        spread[("s", best.get("subtopic"))] += 1
        chosen.add(best["id"])
        used[best["id"]] += 1
        topic_ct[(best["subject"], best["topic"])] += 1
        diff_ct[best["diff"]] += 1
        res.append(best)
    return res


def _split_ones(counts, total_ones, rng):
    tot = sum(counts.values())
    raw = {k: v * total_ones / tot for k, v in counts.items()}
    ones = {k: int(x) for k, x in raw.items()}
    for k in sorted(raw, key=lambda k: (raw[k] - ones[k], rng.random()), reverse=True)[:total_ones - sum(ones.values())]:
        ones[k] += 1
    return ones


def _targets(n, t):
    """t in [0, 1]: 0 = easy-heavy, 1 = hard-heavy."""
    hard = round(n * (0.10 + 0.40 * t))
    easy = round(n * (0.55 - 0.45 * t))
    return {"easy": easy, "medium": n - easy - hard, "hard": hard}


def build_full(pool, used, rng):
    chosen, topic_ct, diff_ct, ga_ct = set(), Counter(), Counter(), Counter()
    tgt = {"easy": 17, "medium": 25, "hard": 13}
    ga = pool.get("GA", [])
    items = [{"qid": c["id"], "sec": "GA"} for c in
             _pick(ga, 5, used, ga_ct, Counter(), {}, rng, chosen, 1) + _pick(ga, 5, used, ga_ct, Counter(), {}, rng, chosen, 2)]
    counts = {s["code"]: s["fq"] for s in syllabus.SUBJECTS if s["fq"]}
    ones = _split_ones(counts, 25, rng)
    cs = []
    for code, n in counts.items():
        c = pool.get(code, [])
        cs += _pick(c, ones[code], used, topic_ct, diff_ct, tgt, rng, chosen, 1)
        cs += _pick(c, n - ones[code], used, topic_ct, diff_ct, tgt, rng, chosen, 2)
    rng.shuffle(cs)
    return items + [{"qid": c["id"], "sec": "CS"} for c in cs]


def build_subject_test(code, n, ones, t, pool, used, rng):
    chosen, topic_ct, diff_ct = set(), Counter(), Counter()
    c = pool.get(code, [])
    tgt = _targets(n, t)
    got = _pick(c, ones, used, topic_ct, diff_ct, tgt, rng, chosen, 1) + _pick(c, n - ones, used, topic_ct, diff_ct, tgt, rng, chosen, 2)
    rng.shuffle(got)
    return [{"qid": x["id"], "sec": code} for x in got]


def deal_dpps(code, topic, ks, K, pool, used, rng):
    """Build the still-missing DPP sets of one topic together: every sub-topic is dealt evenly across the sets
    (so no set is a block of look-alike questions) while later sets get the harder questions."""
    rank = {"easy": 0, "medium": 1, "hard": 2}
    buckets = {}
    for x in pool.get(code, []):
        if x["topic"] == topic and used[x["id"]] == 0:
            buckets.setdefault(x.get("subtopic") or "", []).append(x)
    decks = {k: [] for k in ks}
    m = len(ks)
    for sub in sorted(buckets):
        b = buckets[sub]
        rng.shuffle(b)
        b.sort(key=lambda x: rank.get(x["diff"], 1))
        for i, x in enumerate(b):
            decks[ks[min(m - 1, i * m // len(b))]].append(x)
    out = {}
    for k, lst in decks.items():
        by = {}
        for x in lst:
            by.setdefault(x.get("subtopic") or "", []).append(x)
        pick, rnd = [], 0
        while len(pick) < game.DPP_SIZE and any(by.values()):
            for sub in sorted(by):
                if by[sub] and len(pick) < game.DPP_SIZE:
                    pick.append(by[sub].pop())
            rnd += 1
        rng.shuffle(pick)
        for x in pick:
            used[x["id"]] += 1
        out[k] = [{"qid": x["id"], "sec": code} for x in pick]
    return out


def build_tests(seed=2026):
    """Create any missing tests; existing tests (and their attempts) are never touched."""
    rng = random.Random(seed)
    tp, dp = _pool("test"), _pool("dpp")
    used_t, used_d = Counter(), Counter()
    for r in db.rows("SELECT kind, items FROM tests"):
        for it in json.loads(r["items"]):
            (used_d if r["kind"] == "dpp" else used_t)[it["qid"]] += 1
    have = {r["id"] for r in db.rows("SELECT id FROM tests")}
    rows = []

    for no in range(1, game.FULL_TESTS + 1):
        tid, items = "F%02d" % no, build_full(tp, used_t, rng)
        if tid not in have:
            rows.append((tid, "full", None, None, no, "GATE CS Full Mock %02d" % no, FULL_MIN, json.dumps(items), game.full_unlock_level(no)))
    for s in syllabus.SUBJECTS:
        code = s["code"]
        for no in range(1, game.SFULL_PER_SUBJECT + 1):
            tid = "SF-%s-%02d" % (code, no)
            items = build_subject_test(code, SFULL_Q, 30, (no - 1) / max(1, game.SFULL_PER_SUBJECT - 1), tp, used_t, rng)
            if tid not in have and len(items) >= 20:
                rows.append((tid, "sfull", code, None, no, "%s · Full Test %02d" % (code, no), SFULL_MIN, json.dumps(items), game.sfull_unlock_level(no)))
        for no in range(1, game.SMALL_PER_SUBJECT + 1):
            tid = "S-%s-%02d" % (code, no)
            items = build_subject_test(code, SMALL_Q, 14, (no - 1) / max(1, game.SMALL_PER_SUBJECT - 1), tp, used_t, rng)
            if tid not in have and len(items) >= 10:
                rows.append((tid, "small", code, None, no, "%s · Small Test %02d" % (code, no), SMALL_MIN, json.dumps(items), game.small_unlock_level(no)))
        for t in db.rows("SELECT id, name FROM topics WHERE subject=? ORDER BY ord", (code,)):
            n = sum(1 for x in dp.get(code, []) if x["topic"] == t["name"])
            K = max(1, min(game.MAX_DPP_PER_TOPIC, n // game.DPP_SIZE))
            tids = ["D-%s-%d-%02d" % (code, t["id"], k + 1) for k in range(K)]
            miss = [k for k in range(K) if tids[k] not in have]
            if not miss:
                continue
            decks = deal_dpps(code, t["name"], miss, K, dp, used_d, rng)
            for k in miss:
                if len(decks[k]) >= 5:
                    rows.append((tids[k], "dpp", code, t["name"], k + 1, "%s · DPP %d" % (t["name"], k + 1), 30, json.dumps(decks[k]), 0))
    db.many("INSERT INTO tests(id,kind,subject,topic,no,title,minutes,items,unlock_level) VALUES(?,?,?,?,?,?,?,?,?)", rows)
    return len(rows)
