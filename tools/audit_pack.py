"""Audit the question pack: duplicates, malformed items, thin explanations.

    python tools/audit_pack.py            # summary
    python tools/audit_pack.py -v         # list offenders
"""
import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = "-v" in sys.argv
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ⁺⁻₀₁₂₃₄₅₆₇₈₉", "0123456789n+-0123456789")


def norm(t):
    return re.sub(r"\s+", " ", (t or "").lower()).strip()


def okey(o):
    """Option text with superscript/caret notation and spacing unified, to catch the same answer written twice."""
    o = re.sub(r"\^\(([^)]*)\)", r"\1", o.translate(SUP))
    return re.sub(r"[\s·×]", "", re.sub(r"\^(\w+)", r"\1", o))


def tpl(t):
    return re.sub(r"\d+(?:\.\d+)?", "#", norm(t))


def main():
    qs = json.load(open(os.path.join(ROOT, "content", "pack.json"), encoding="utf-8"))
    bad = collections.defaultdict(list)
    ids = collections.Counter(q["id"] for q in qs)
    bad["duplicate id"] = [i for i, c in ids.items() if c > 1]
    exact, tpls = collections.defaultdict(list), collections.defaultdict(list)
    for q in qs:
        o, a, t = q.get("options") or [], q.get("answer") or [], q["qtype"]
        exact[(q["subject"], norm(q["text"]), tuple(sorted(map(norm, o))))].append(q)
        tpls[(q["subject"], q["topic"], tpl(q["text"]), tuple(sorted(tpl(x) for x in o)))].append(q)
        if t in ("single", "multiple"):
            if len(o) < 2:
                bad["fewer than 2 options"].append(q["id"])
            if len(set(map(okey, o))) != len(o) and "postfix" not in q["text"] and "prefix" not in q["text"]:
                bad["same answer written twice"].append(q["id"])
            if not a or any(x not in o for x in a):
                bad["answer not in options"].append(q["id"])
            if t == "single" and len(a) != 1:
                bad["single with !=1 answers"].append(q["id"])
            if t == "multiple" and len(a) < 1:
                bad["multiple without answer"].append(q["id"])
        elif q.get("numeric") is None:
            bad["numerical without value"].append(q["id"])
        for pat in ("None", "nan", "Undefined", "TODO"):
            if re.search(r"\b%s\b" % pat, q["text"]):
                bad["suspicious text: " + pat].append(q["id"])
        e = q.get("expl") or ""
        if len(e.strip()) < 60:
            bad["thin explanation (<60 chars)"].append(q["id"])
        if q["diff"] not in ("easy", "medium", "hard"):
            bad["bad difficulty"].append(q["id"])
    dup_exact = {k: v for k, v in exact.items() if len(v) > 1}
    print("questions:", len(qs))
    print("exact duplicates (same text and options within a subject): %d groups" % len(dup_exact))
    big = sorted(tpls.values(), key=len, reverse=True)
    print("template families with 4+ variants:", sum(1 for v in big if len(v) >= 4), " largest:", [len(v) for v in big[:8]])
    for k, v in sorted(bad.items()):
        if v:
            print("%-34s %d" % (k, len(v)), (v[:4] if V else ""))
    if V:
        for k, v in list(dup_exact.items())[:15]:
            print("DUP", k[0], k[1][:90], [x["id"] for x in v][:4])
    print("per subject:", dict(collections.Counter(q["subject"] for q in qs)))
    return sum(len(v) for k, v in bad.items() if k not in ("thin explanation (<60 chars)",))


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
