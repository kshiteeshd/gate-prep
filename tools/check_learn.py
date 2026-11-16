"""Cross-check every learning module.   python tools/check_learn.py [SUBJECT]
   - structure (required fields, widget names, topic exists in the syllabus, slug uniqueness)
   - quick-check answer indexes + explanations, practice-question availability
   - every worked example's final answer is recomputed in Python (Ex.verify) and must appear in the written answer
   - markdown sanity (balanced ** and `), minimum depth (words, examples)
   - every lesson page renders through Flask (HTTP 200, no template artefacts)
   - JS widget logic unit tests (node) if node is available"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault("GATEPREP_HOME", os.path.join(ROOT, "data_check"))
import learn  # noqa: E402
from gate import syllabus  # noqa: E402

only = sys.argv[1] if len(sys.argv) > 1 else None
learn.load_all()
errs, warns = [], []
E = lambda l, m: errs.append("%s: %s" % (l["slug"], m))
W = lambda l, m: warns.append("%s: %s" % (l["slug"], m))
REQ = ["subject", "chapter", "ch_no", "no", "slug", "title", "topic", "key", "analogy", "sections", "summary", "quick", "examples", "traps"]
slugs = set()


def texts(l):
    t = [l["key"], (l.get("analogy") or ("", "", ""))[2]] + [s["md"] for s in l["sections"]] + list(l["summary"])
    for s in l["sections"]:
        t += [c[2] for c in s.get("call", [])]
    t += [x[1] for x in l["traps"]]
    t += [x[1] for x in l.get("proofs", [])] + [x[1] for x in l.get("notes", [])]
    for e in l["examples"]:
        t += [e.problem] + list(e.steps) + [e.answer]
    return t


SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")


def norm(x):
    return re.sub(r"[\s,*_`^]", "", str(x).translate(SUP).replace("−", "-")).lower()


NUM = re.compile(r"-?\d+(?:\.\d+)?(?:/\d+)?")


def nums(t):
    out = []
    for m in NUM.findall(re.sub(r"(?<=\d),(?=\d{3})", "", str(t).translate(SUP)).replace("−", "-")):
        try:
            out.append(float(m) if "/" not in m else int(m.split("/")[0]) / int(m.split("/")[1]))
        except (ValueError, ZeroDivisionError):
            pass
    return out


def matches(v, answer):
    """verify() output agrees with the written answer: every number it produced appears (numerically) in the answer,
    otherwise fall back to a whitespace/markdown-insensitive substring test."""
    vn, an = nums(v), nums(answer)
    pure = re.fullmatch(r"[\s\d.,/\-−andx=\[\]()+]*", str(v)) is not None or len(vn) >= 1 and not re.search(r"[A-Za-zͰ-Ͽ∀-⋿]{3,}", str(v))
    if vn and pure:
        return all(any(abs(x - y) <= 1e-3 * max(1, abs(y)) for y in an) for x in vn)
    return norm(v) in norm(answer)


def template_rules(l):
    """docs/CONTENT_RULES.md: hard rules for sub-chapters of subjects organised into sections."""
    wc = lambda t: len(re.sub(r"[#*`|$]", " ", str(t)).split())
    if not l.get("defs"):
        E(l, "RULE no definitions")
    for t, d in l.get("defs", []):
        if wc(d) > 45:
            E(l, "RULE definition of %r longer than 45 words" % t)
    if wc(l["key"]) > 70:
        E(l, "RULE key idea longer than 70 words")
    heads = [h for h, _ in l.get("book", [])] + [x["h"] for x in l["sections"]]
    if len(heads) < 2:
        E(l, "RULE fewer than 2 concept blocks")
    for group in ([h for h, _ in l.get("book", [])], [x["h"] for x in l["sections"]]):   # a section repeating a book heading is folded in at export
        if len(set(group)) != len(group):
            E(l, "RULE repeated concept heading")
    for t in [b for _, b in l.get("book", [])] + [x["md"] for x in l["sections"]]:
        for para in re.split(r"\n\s*\n", t):
            if not para.lstrip().startswith(("|", "-", "    ", "1.", "$$")) and wc(para) > 110 and len(re.findall(r"\*\*[^*]{2,48}?[:.]\*\*", para)) < 2:
                E(l, "RULE paragraph of %d words (max 110): %s" % (wc(para), para.strip()[:50]))
    seen = {}
    for src, t in [("part", x["md"]) for x in l["sections"]] + [("example", e.problem + " " + " ".join(e.steps)) for e in l["examples"]]:
        for sent in re.split(r"(?<=[.!?])\s+|\n+", re.sub(r"[*`$|]", "", t)):
            key = re.sub(r"\W+", " ", sent.lower()).strip()
            if len(key.split()) >= 9:
                if key in seen:
                    E(l, "RULE repeated sentence: %s" % sent.strip()[:60])
                seen[key] = src
    if len(l["examples"]) < 3:
        E(l, "RULE fewer than 3 worked examples")
    titles = [e.title for e in l["examples"]]
    if len(set(titles)) != len(titles):
        E(l, "RULE repeated example title")
    for e in l["examples"]:
        if len(e.steps) < 2 and len(e.steps[0] if e.steps else "") < 40:
            pass
        if not e.verify and re.search(r"\d", re.sub(r"[A-Za-z]\w*\d+|\d+[A-Za-z]", "", e.answer)):
            E(l, "RULE example %r has a numeric answer but no verify()" % e.title)
    if len(l["quick"]) < 3:
        E(l, "RULE fewer than 3 quick checks")
    if len(l["traps"]) < 3:
        E(l, "RULE fewer than 3 common mistakes")
    if not 4 <= len(l["summary"]) <= 7:
        E(l, "RULE summary has %d bullets (4-7)" % len(l["summary"]))
    for b in l["summary"]:
        if wc(b) > 30:
            E(l, "RULE summary bullet longer than 30 words: %s" % b[:40])


n_ex = n_ver = 0
for l in learn.LESSONS:
    if l.get("section") and (not only or l["subject"] == only):
        template_rules(l)
    if only and l["subject"] != only:
        continue
    for k in REQ:
        if k not in l:
            E(l, "missing field " + k)
    if l["slug"] in slugs:
        E(l, "duplicate slug")
    slugs.add(l["slug"])
    if l["widget"] not in learn.WIDGETS:
        E(l, "unknown widget " + l["widget"])
    if l["topic"] not in syllabus.TOPICS.get(l["subject"], []):
        E(l, "topic %r not in syllabus" % l["topic"])
    if len(l["sections"]) < 3:
        W(l, "only %d explanation sections" % len(l["sections"]))
    if len(l["examples"]) < 2:
        W(l, "fewer than 2 worked examples")
    if len(l["quick"]) < 3:
        W(l, "fewer than 3 quick checks")
    if len(l["traps"]) < 3:
        W(l, "fewer than 3 traps")
    if len(l["summary"]) < 4:
        W(l, "summary too short")
    for q in l["quick"]:
        if not (len(q) == 4 and len(q[1]) >= 3 and isinstance(q[2], int) and 0 <= q[2] < len(q[1]) and q[3]):
            E(l, "bad quick-check: %s" % str(q[0])[:50])
        if len(set(q[1])) != len(q[1]):
            E(l, "duplicate options in quick-check: %s" % str(q[0])[:50])
    for t in texts(l):
        if t.count("**") % 2 or t.count("`") % 2:
            E(l, "unbalanced markdown in: %s" % t[:60].replace("\n", " "))
    for t in texts(l):   # markdown tables: every row must have the header's number of cells
        rows = [r for r in t.split("\n") if r.strip().startswith("|")]
        if rows:
            n = len(rows[0].strip().strip("|").split("|"))
            for r in rows:
                if len(r.strip().strip("|").split("|")) != n:
                    E(l, "table row has %d cells, header has %d: %s" % (len(r.strip().strip("|").split("|")), n, r[:50]))
    words = sum(len(t.split()) for t in texts(l))
    if words < 650:
        W(l, "only %d words (aim for 650+)" % words)
    if not l.get("proofs"):
        W(l, "no proofs/derivations yet")
    if not l.get("notes"):
        W(l, "no detailed notes yet")
    for e in l["examples"]:
        n_ex += 1
        if len(e.steps) < 2:
            W(l, "example %r has < 2 steps" % e.title)
        if e.verify:
            n_ver += 1
            try:
                v = e.verify()
            except Exception as ex:
                E(l, "verify crashed for %r: %s" % (e.title, ex))
                continue
            if not matches(v, e.answer):
                E(l, "EXAMPLE MISMATCH %r: recomputed %r but the written answer is %r" % (e.title, v, e.answer))
        else:
            W(l, "example %r has no verify()" % e.title)

# render every page
try:
    from gate import db  # noqa
    import app as appmod
    c = appmod.app.test_client()
    for l in learn.LESSONS:
        if only and l["subject"] != only:
            continue
        r = c.get("/learn/%s/%s" % (l["subject"], l["slug"]))
        h = r.get_data(as_text=True)
        if r.status_code != 200:
            E(l, "page returned %s" % r.status_code)
        elif "{{" in h or "{%" in h or "Undefined" in h:
            E(l, "template artefact in rendered page")
        elif h.count('class="card q prac"') < 3:
            W(l, "fewer than 3 practice questions available for topic %r" % l["topic"])
    for p in ["/learn", "/learn/ENGM"]:
        if c.get(p).status_code != 200:
            errs.append("page %s failed" % p)
except Exception as ex:
    errs.append("render check crashed: %r" % ex)

# JS logic
for jsname in ("test_widgets.js", "test_widgets_cs.js", "test_widgets_dbos.js", "test_widgets_toc.js", "test_widgets_hw.js", "test_widgets_net.js"):
    js = os.path.join(ROOT, "tools", jsname)
    if os.path.exists(js):
        try:
            out = subprocess.run(["node", js], cwd=ROOT, capture_output=True, text=True, timeout=120).stdout
            bad = [x for x in out.splitlines() if x.startswith("FAIL")]
            print("%s: %d passed, %d failed" % (jsname, out.count("PASS"), len(bad)))
            errs += ["JS " + b for b in bad]
        except FileNotFoundError:
            print("(node not found, skipping widget tests)")

print("\nlessons checked: %d | worked examples: %d (auto-verified: %d)" % (len([l for l in learn.LESSONS if not only or l["subject"] == only]), n_ex, n_ver))
for w in warns:
    print("WARN ", w)
for e in errs:
    print("ERROR", e)
print("\nRESULT:", "OK" if not errs else "%d ERROR(S)" % len(errs), "| %d warning(s)" % len(warns))
sys.exit(1 if errs else 0)
