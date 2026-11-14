"""Every topic becomes a chapter: the full lesson stays as the overview, followed by focused parts (each with its own
examples, quick checks and practice) and a review. Chapters written by hand lesson by lesson are left untouched."""
import re

HAND_CHAPTERS = {"Binary Trees, BST & AVL"}
_STOP = set("the and for that with this from are was were not but all any can has have its into than then them they their there what when which will your you one two out per also each both only over such more most some very just like".split())


def _words(t):
    return len(re.sub(r"[#*`|$-]+", " ", str(t)).split())


def _utext(u):
    return u[2]["md"] if u[0] == "sec" else u[2]


def chapterize(LESSONS):
    if any(l.get("part") for l in LESSONS):
        return
    parents = sorted((l for l in LESSONS if l["chapter"] not in HAND_CHAPTERS),
                     key=lambda l: (l["subject"], l["ch_no"], l["no"]))
    children, split = [], set()
    for l in parents:
        units = [("book", h, b) for h, b in l.get("book", [])] + [("sec", s["h"], s) for s in l["sections"]]
        words = [_words(_utext(u)) for u in units]
        k = min(len(units), max(2, min(8, round(sum(words) / 280)))) if units else 0
        if k < 2:
            continue
        groups, cur, acc, target = [], [], 0, sum(words) / k
        for u, w in zip(units, words):
            if cur and acc + w / 2 > target * (len(groups) + 1) and len(groups) < k - 1:
                groups.append(cur)
                cur = []
            cur.append(u)
            acc += w
        groups.append(cur)
        n = len(groups)
        E, Q = l["examples"], l["quick"]
        title0 = l["title"]
        split.add(l["slug"])
        for gi, g in enumerate(groups):
            heads = [u[1] for u in g]
            name = heads[0]
            first = re.sub(r"[#*`$|]", "", _utext(g[0])).strip().split("\n")[0][:230]
            c = dict(subject=l["subject"], chapter=title0, ch_no=l["ch_no"], no=2 + gi, slug="%s-p%d" % (l["slug"], gi + 1),
                     title="%d · %s" % (gi + 1, name), topic=l["topic"], weight=l["weight"], widget="none", traps=[], summary=[],
                     minutes=max(5, round(sum(_words(_utext(u)) for u in g) / 160 + 3)), key=first or title0,
                     analogy=("🔖", "Part %d of %d" % (gi + 1, n + 1), "A focused piece of the chapter on %s. Read the parts in order; the last one is a review with mixed practice." % title0),
                     book=[(u[1], u[2]) for u in g if u[0] == "book"], sections=[u[2] for u in g if u[0] == "sec"],
                     examples=E[gi * len(E) // n:(gi + 1) * len(E) // n], quick=Q[gi * len(Q) // n:(gi + 1) * len(Q) // n],
                     proofs=[], notes=[], credits=5, part=gi + 1, parts=n + 1, parent=l["slug"])
            if gi == n - 1:
                c["proofs"] = [(x[0], x[1]) for x in l.get("proofs", [])]
                c["notes"] = [(x[0], x[1]) for x in l.get("notes", [])]
            children.append(c)
        children.append(dict(subject=l["subject"], chapter=title0, ch_no=l["ch_no"], no=2 + n, slug="%s-review" % l["slug"],
                             title="Review and mixed practice", topic=l["topic"], weight=l["weight"], widget="none", minutes=15,
                             key=l["key"], analogy=("🔁", "Part %d of %d" % (n + 1, n + 1), "Bring the parts together: the cheat sheet, the common mistakes, every quick check and a larger set of practice questions."),
                             book=[], sections=[], examples=[], quick=list(Q), traps=list(l["traps"]), summary=list(l["summary"]),
                             proofs=[], notes=[], credits=10, part=n + 1, parts=n + 1, parent=l["slug"], review=True))
    LESSONS.extend(children)
    for l in LESSONS:
        if l["slug"] in split:
            l["chapter"] = l["title"]
            l["no"] = 1
    for subj in {l["subject"] for l in LESSONS}:
        order = []
        ls = [x for x in LESSONS if x["subject"] == subj]
        for l in sorted(ls, key=lambda x: (x["ch_no"], x["chapter"] in HAND_CHAPTERS, x["no"])):
            l["_ck"] = (l["chapter"],) if l["chapter"] in HAND_CHAPTERS else (l.get("parent") or l["slug"],)
        seen = []
        for l in sorted(ls, key=lambda x: (x["ch_no"], x["no"])):
            if l["_ck"] not in seen:
                seen.append(l["_ck"])
        for l in ls:
            l["ch_no"] = seen.index(l["_ck"]) + 1


def assign_subs(LESSONS, avail):
    """avail: {(subject, topic): [subtopic, ...]}. Each part gets the subtopics that best match its text; the review gets all."""
    tok = lambda t: {w for w in re.findall(r"[a-z]{4,}", str(t).lower()) if w not in _STOP}
    for p in {l["parent"] for l in LESSONS if l.get("parent")}:
        kids = [l for l in LESSONS if l.get("parent") == p]
        parts = [c for c in kids if not c.get("review")]
        subs = avail.get((parts[0]["subject"], parts[0]["topic"]), [])
        texts = [tok(c["title"] + " " + " ".join(b[0] + " " + b[1] for b in c["book"]) + " " + " ".join(s["h"] + " " + s["md"] for s in c["sections"])
                     + " " + " ".join(e.title + " " + e.problem for e in c["examples"])) for c in parts]
        load = [0] * len(parts)
        for sname in subs:
            st = tok(sname)
            sc = [len(st & t) for t in texts]
            best = max(range(len(parts)), key=lambda i: (sc[i], -load[i]))
            parts[best].setdefault("subs", []).append(sname)
            load[best] += 1
        for c in kids:
            if c.get("review"):
                c["subs"] = list(subs)
