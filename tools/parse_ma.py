"""Parse the General Aptitude part of the 'Mathematics & Aptitude PYQs' book (tools/pdf_cols.py output) into question records.
   GA questions are common to every GATE paper, so questions from all branch tags are usable.
   usage: python tools/parse_ma.py data_check/txt/ma_cols.txt content/pyq_ga.json"""
import hashlib
import json
import re
import sys

sys.path.insert(0, __file__.rsplit("tools", 1)[0] + "tools")
import parse_pyq as P  # noqa: E402

QH = re.compile(r"^\s*(\d+)\s*\.\s*\[\s*(MCQ|NAT|MSQ)\s*\]\s*\[\s*GATE\s*-\s*(?:[A-Z]{2}\s*-\s*)?([\d\s]+?)\s*[:\-]\s*(\d)\s*M\s*\]\s*$")
PAIR = re.compile(r"(\d[\d ]{0,3})\s*\.\s*\(\s*([^)]*?)\s*\)")
TOPIC = {"Data Interpretation": "Data Interpretation", "Logical Reasoning": "Logical & Analytical Reasoning", "Transformations of Shapes": "Logical & Analytical Reasoning",
         "Basic English Grammar": "Verbal Ability"}


def main(src, dst):
    P.build_vocab([src, src.replace('ma_cols', 'pw_cols')])
    lines = P.load(src)
    start = next(i for i, l in enumerate(lines) if l.strip() == "Data Interpretation" and i > 40000)
    start = max(0, start - 3)
    chs, cur = [], None
    for l in lines[start:]:
        if P.CH.match(l):
            cur = []
            chs.append(cur)
        elif cur is not None:
            cur.append(l)
    out, stats, seen = [], {"seen": 0, "bad": 0, "no_ans": 0, "garbled": 0, "dup": 0}, set()
    for ch in chs:
        title = next((x.strip() for x in ch[1:6] if re.search(r"[A-Za-z]{4}", x)), "")
        topic = TOPIC.get(title, "Numerical Ability" if title not in TOPIC else TOPIC[title])
        qs, keys = {}, {}
        curq = None
        for l in ch:
            if P.NOISE.search(l):
                continue
            exp = re.split(r"(?<=\S)\s+(?=\d(?:\s?\d)?\s*\.\s*\[\s*(?:MCQ|NAT|MSQ)\s*\]\s*\[\s*GATE)", l)
            for part in exp:
                m = QH.match(part)
                if m:
                    n = int(m.group(1))
                    ys = re.sub(r"\s", "", m.group(3))
                    qs[n] = {"type": m.group(2), "year": int(ys[:4]) if ys[:4].isdigit() else 0, "marks": int(m.group(4)), "lines": []}
                    curq = n
                    continue
                pairs = PAIR.findall(part)
                if pairs and len(re.sub(r"[\d\s.()a-dA-Dto,+\-Marks]", "", part)) <= 4 and len(pairs) >= 1 and re.fullmatch(r"\s*(\d[\d ]{0,3}\s*\.\s*\([^)]*\)\s*)+", part):
                    for a, b in pairs:
                        keys[int(a.replace(" ", ""))] = b
                    continue
                if curq is not None:
                    qs[curq]["lines"].append(part)
        for n, q in sorted(qs.items()):
            stats["seen"] += 1
            if q["type"] == "NAT":
                stem, options = P.clean_stem("\n".join(q["lines"])), []
            else:
                stem, options = P.split_options(q["lines"])
                if options is None:
                    stats["bad"] += 1
                    continue
                stem = P.clean_stem(stem)
            full = stem + " " + " ".join(options)
            if P.truncated(stem, q["type"]) or P.BAD.search(full) or len(stem) < 25 or any(not o for o in options):
                stats["bad"] += 1
                continue
            if P.garbled(stem, options):
                stats["garbled"] += 1
                continue
            if n not in keys:
                stats["no_ans"] += 1
                continue
            pa = P.parse_answer(keys[n], q["type"], options)
            if not pa:
                stats["no_ans"] += 1
                continue
            h = re.sub(r"\W+", "", stem.lower())[:120]
            if h in seen:
                stats["dup"] += 1
                continue
            seen.add(h)
            marks = q["marks"]
            rec = {"qtype": {"MCQ": "single", "MSQ": "multiple", "NAT": "numerical"}[q["type"]], "text": stem, "options": options, "answer": pa.get("answer", []),
                   "subject": "GA", "topic": topic, "subtopic": "GATE %d" % q["year"], "diff": "medium" if marks == 1 else "hard", "marks": marks, "src": "GATE %d" % q["year"],
                   "neg": 0 if q["type"] != "MCQ" else (0.33 if marks == 1 else 0.66), "pool": "test",
                   "expl": "Official GATE %d answer: %s." % (q["year"], (" / ".join(options["abcd".index(x)] for x in re.findall("[a-d]", keys[n].lower())) if options else keys[n].replace(" to ", " – ")))}
            if "numeric" in pa:
                rec["numeric"], rec["tol"] = pa["numeric"], pa["tol"]
            rec["id"] = "pyqga" + hashlib.sha1((stem + "|".join(options)).encode("utf-8")).hexdigest()[:10]
            out.append(rec)
    json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(stats, "kept", len(out), "chapters", len(chs))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
