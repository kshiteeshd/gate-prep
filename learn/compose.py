"""Subject → section → chapter → sub-chapter.

A subject spec (learn/s_<code>.py) lists sections, chapters (one per syllabus topic) and sub-chapters (one per
sub-topic). Each sub-chapter is assembled from named pieces of the authored lessons (book parts B, sections S,
examples E, quick checks Q, traps T, proofs P, notes N) plus any new material written in the spec itself.
After composing, the subject's source lessons are removed, so every lesson the reader sees is one sub-chapter."""
import re

SPECS = {}          # subject -> list of ("sec", name) / ("ch", topic, name) / ("sub", dict)
MOVED = {}          # old slug -> [new slugs]   (lets the apps carry completed lessons over)
UNUSED = {}         # subject -> ["slug X3", ...] pieces of source lessons that no sub-chapter took


class Spec:
    def __init__(self, subject):
        self.subject = subject
        self.items = SPECS.setdefault(subject, [])

    def section(self, name):
        self.items.append(("sec", name))

    def chapter(self, topic, name=None):
        self.items.append(("ch", topic, name or topic))

    def sub(self, slug, title, key, summary, take=(), subs=(), analogy=None, widget=None, hint="", **new):
        """take = [(source_slug, "B0 S1 S2 E0 Q3 T1 P0 N1"), ...]; analogy = source slug or a (emoji, title, text) tuple;
        new = extra sections / examples / quick / traps / proofs / notes / book written directly for this sub-chapter."""
        self.items.append(("sub", dict(slug=slug, title=title, key=key, summary=list(summary), take=list(take), subs=list(subs),
                                       analogy=analogy, widget=widget, hint=hint, new=new)))


    def more(self, slug, take=(), **new):
        """Add pieces or new material to a sub-chapter declared earlier."""
        d = next(it[1] for it in self.items if it[0] == "sub" and it[1]["slug"] == slug)
        d["take"] += list(take)
        for f, v in new.items():
            d["new"][f] = list(d["new"].get(f, [])) + list(v)


FIELD = {"B": "book", "S": "sections", "E": "examples", "Q": "quick", "T": "traps", "P": "proofs", "N": "notes"}


def _words(l):
    t = [l["key"]] + [b[1] for b in l["book"]] + [s["md"] for s in l["sections"]] + [x[1] for x in l["proofs"] + l["notes"]]
    t += [e.problem + " ".join(e.steps) for e in l["examples"]]
    return sum(len(re.sub(r"[#*`|$]", " ", str(x)).split()) for x in t)


def compose(LESSONS):
    for subject, items in SPECS.items():
        src = {l["slug"]: l for l in LESSONS if l["subject"] == subject}
        if not src:
            continue
        used = set()
        out, section, ch_no, topic, chname, no = [], "", 0, None, None, 0
        for it in items:
            if it[0] == "sec":
                section = it[1]
                continue
            if it[0] == "ch":
                ch_no += 1
                topic, chname, no = it[1], it[2], 0
                continue
            d = it[1]
            no += 1
            l = dict(subject=subject, section=section, chapter=chname, ch_no=ch_no, no=no, slug=d["slug"], title=d["title"], topic=topic,
                     subs=d["subs"], key=d["key"], summary=d["summary"], widget=d["widget"] or "none", widget_hint=d["hint"],
                     book=[], sections=[], examples=[], quick=[], traps=[], proofs=[], notes=[], credits=10, weight=4, sources=[])
            for s_slug, picks in d["take"]:
                s = src[s_slug]
                l["sources"].append(s_slug)
                l["weight"] = max(l["weight"], s.get("weight", 3))
                for tok in picks.split():
                    f, i = FIELD[tok[0]], int(tok[1:])
                    l[f].append(s[f][i])
                    used.add((s_slug, tok[0], i))
            for f, v in d["new"].items():
                l[f] += list(v)
            a = d["analogy"]
            l["analogy"] = src[a]["analogy"] if isinstance(a, str) else a
            if d["widget"] is None:
                ws = [src[s]["widget"] for s in l["sources"] if src[s]["widget"] != "none"]
                l["widget"], l["widget_hint"] = (ws[0], src[l["sources"][0]].get("widget_hint", "")) if ws and len(l["sources"]) == 1 else ("none", "")
            l["minutes"] = max(8, round(_words(l) / 150 + 2 * len(l["examples"]) + 3))
            out.append(l)
        UNUSED[subject] = ["%s %s%d" % (s, k, i) for s, sl in src.items() for k, f in FIELD.items() for i in range(len(sl.get(f, []))) if (s, k, i) not in used]
        new = {l["slug"] for l in out}
        for s in src:
            if s not in new:
                MOVED[s] = [l["slug"] for l in out if s in l["sources"]]
        LESSONS[:] = [l for l in LESSONS if l["subject"] != subject] + out
