"""Authored subjects: every sub-chapter is written as ONE coherent lesson (no stitching of older lessons).

    A = Author("ENGM")
    A.section("Discrete Mathematics")
    A.chapter("Propositional & First-Order Logic")
    A.lesson(slug, title, key, analogy=(emoji, title, text), defs=[(term, definition)], parts=[dict(h=, md=, call=[])],
             examples=[Ex(...)], traps=[(title, text)], quick=[(question, options, answer_index, why)], summary=[...],
             subs=[question sub-topics], widget=None, hint="")

Reading order of a sub-chapter (docs/CONTENT_RULES.md): key idea → definitions → parts that go from intuition to
results to method → worked examples (easy → GATE level) → mistakes → quick checks → summary."""

AUTHORED = {}      # subject -> [("sec", name) | ("ch", topic, name) | ("lesson", dict)]


class Author:
    def __init__(self, subject):
        self.subject = subject
        self.items = AUTHORED.setdefault(subject, [])

    def section(self, name):
        self.items.append(("sec", name))

    def chapter(self, topic, name=None):
        self.items.append(("ch", topic, name or topic))

    def lesson(self, slug, title, key, summary, parts, examples, traps, quick, defs, subs=(), analogy=None, widget=None, hint="",
               proofs=(), notes=(), weight=4):
        self.items.append(("lesson", dict(slug=slug, title=title, key=key, summary=list(summary), parts=list(parts), examples=list(examples),
                                          traps=list(traps), quick=list(quick), defs=list(defs), subs=list(subs), analogy=analogy,
                                          widget=widget or "none", hint=hint, proofs=list(proofs), notes=list(notes), weight=weight)))


    def extend(self, slug, parts=(), examples=(), proofs=(), notes=(), quick=(), traps=()):
        """Append material to a lesson written earlier (used for the 'How GATE asks this' parts and extra examples)."""
        for it in self.items:
            if it[0] == "lesson" and it[1]["slug"] == slug:
                d = it[1]
                d["parts"] += list(parts)
                d["examples"] += list(examples)
                d["proofs"] += list(proofs)
                d["notes"] += list(notes)
                d["quick"] += list(quick)
                d["traps"] += list(traps)
                return
        raise KeyError(slug)


def _words(l):
    import re
    t = [l["key"]] + [p["md"] for p in l["sections"]] + [x[1] for x in l["proofs"] + l["notes"]]
    t += [e.problem + " ".join(e.steps) for e in l["examples"]]
    return sum(len(re.sub(r"[#*`|$]", " ", str(x)).split()) for x in t)


def finalize(LESSONS):
    for subject, items in AUTHORED.items():
        out, section, ch_no, topic, chname, no = [], "", 0, None, None, 0
        for it in items:
            if it[0] == "sec":
                section = it[1]
            elif it[0] == "ch":
                ch_no += 1
                topic, chname, no = it[1], it[2], 0
            else:
                d = it[1]
                no += 1
                l = dict(subject=subject, section=section, chapter=chname, ch_no=ch_no, no=no, slug=d["slug"], title=d["title"], topic=topic,
                         subs=d["subs"], key=d["key"], summary=d["summary"], analogy=d["analogy"], widget=d["widget"], widget_hint=d["hint"],
                         book=[], sections=d["parts"], examples=d["examples"], quick=d["quick"], traps=d["traps"], proofs=d["proofs"], notes=d["notes"],
                         defs=d["defs"], credits=10, weight=d["weight"], sources=[])
                l["minutes"] = max(8, round(_words(l) / 150 + 2 * len(l["examples"]) + 3))
                out.append(l)
        LESSONS[:] = [l for l in LESSONS if l["subject"] != subject] + out
