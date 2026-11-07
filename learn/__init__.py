"""Learning modules: Subject -> Chapter -> Lesson (topic).  Lessons are authored as Python data (see learn/l_*.py)."""
import importlib
import pkgutil
import re
from collections import OrderedDict

from markupsafe import Markup, escape

LESSONS = []
WIDGETS = {"truth", "relation", "matrix", "prob", "func", "graph", "counting", "hasse", "group", "venn", "none",
           "sort", "growth", "master", "dp", "traverse", "bst", "heap", "hash", "rectree", "bits", "llist", "stackq",
           "sql", "fd", "sched", "cpusched", "pagerep", "disk", "banker", "addr", "automata", "grammar", "ieee", "numsys", "kmap", "cache", "pipeline", "subnet", "crc", "tcp"}


class Ex:
    """A worked example. `verify` (optional) is a zero-arg callable returning the expected final answer; the validator
    recomputes it and compares with `answer`, so numeric slips are caught automatically."""
    def __init__(self, title, problem, steps, answer, verify=None):
        self.title, self.problem, self.steps, self.answer, self.verify = title, problem, steps, answer, verify


def lesson(**kw):
    kw.setdefault("widget", "none")
    kw.setdefault("traps", [])
    kw.setdefault("examples", [])
    kw.setdefault("quick", [])
    kw.setdefault("summary", [])
    kw.setdefault("weight", 3)
    kw.setdefault("minutes", 12)
    LESSONS.append(kw)
    return kw


EXTRA = {}


def deepen(slug, proofs=(), notes=()):
    """Attach in-depth material to a lesson: proofs = [(title, md)] full derivations/proofs, notes = [(title, md)] detailed notes."""
    EXTRA.setdefault(slug, {"proofs": [], "notes": []})
    EXTRA[slug]["proofs"] += list(proofs)
    EXTRA[slug]["notes"] += list(notes)


BOOK = {}


def elab(slug, *parts):
    """Textbook-style long-form teaching text for a lesson: parts = (heading, markdown) pairs, read top to bottom."""
    BOOK.setdefault(slug, []).extend(parts)


def load_all():
    if LESSONS:
        return
    for m in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
        if m.name.startswith("l_"):
            importlib.import_module("learn." + m.name)
    for m in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
        if m.name.startswith(("d_", "e_")):
            importlib.import_module("learn." + m.name)
    for l in LESSONS:
        x = EXTRA.get(l["slug"], {})
        l["proofs"] = x.get("proofs", [])
        l["notes"] = x.get("notes", [])
        l["book"] = BOOK.get(l["slug"], [])
    LESSONS.sort(key=lambda l: (l["subject"], l["ch_no"], l["no"]))


def by_slug(slug):
    load_all()
    return next((l for l in LESSONS if l["slug"] == slug), None)


def tree(subject):
    """[(chapter_no, chapter_name, [lessons])] for a subject."""
    load_all()
    out = OrderedDict()
    for l in LESSONS:
        if l["subject"] == subject:
            out.setdefault((l["ch_no"], l["chapter"]), []).append(l)
    return [(k[0], k[1], v) for k, v in out.items()]


def neighbours(l):
    load_all()
    seq = [x for x in LESSONS if x["subject"] == l["subject"]]
    i = seq.index(l)
    return (seq[i - 1] if i > 0 else None, seq[i + 1] if i + 1 < len(seq) else None)


# ---------- tiny markdown: paragraphs, **bold**, *italic*, `code`, - bullets, 1. lists, | tables, 4-space code ----------
def tex_inline(s):
    """$...$ -> a span KaTeX typesets in the browser (source stays readable if scripts fail)."""
    return re.sub(r"\$(?=\S)([^$\n]+?)(?<=\S)\$", lambda m: '<span class="tex" data-tex="%s">%s</span>' % (m.group(1), m.group(1)), s)


def _inline(s):
    s = str(escape(s))
    s = tex_inline(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?!\w)", r"<i>\1</i>", s)
    return s


def mdi(text):
    return Markup(_inline(text))


def md(text):
    out = []
    para, tbl, code = [], [], []
    lst = [None, []]

    def flush_p():
        if para:
            out.append("<p>%s</p>" % _inline(" ".join(para)))
            del para[:]

    def flush_l():
        if lst[0]:
            out.append("<%s>%s</%s>" % (lst[0], "".join("<li>%s</li>" % _inline(x) for x in lst[1]), lst[0]))
            lst[0], lst[1] = None, []

    def flush_c():
        if code:
            out.append('<pre class="tr">%s</pre>' % escape("\n".join(code)))
            del code[:]

    def flush_t():
        if tbl:
            rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in tbl if not re.match(r"^\s*\|?[\s:\-|]+\|?\s*$", r)]
            if rows:
                head, body = rows[0], rows[1:]
                out.append('<div class="tw"><table class="rt"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (
                    "".join("<th>%s</th>" % _inline(c) for c in head),
                    "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % _inline(c) for c in r) for r in body)))
            del tbl[:]

    for line in str(text).strip("\n").split("\n"):
        ln = line.rstrip()
        m = re.match(r"^\s*\$\$(.+?)\$\$\s*$", ln)
        if m:                                   # $$ formula $$ on its own line = centred display equation
            flush_p(); flush_l(); flush_t(); flush_c()
            tx = str(escape(m.group(1).strip()))
            out.append('<div class="texd" data-tex="%s">%s</div>' % (tx, tx))
            continue
        if ln.startswith("    ") or ln.startswith("\t"):
            flush_p(); flush_l(); flush_t()
            code.append(ln[4:] if ln.startswith("    ") else ln[1:])
            continue
        flush_c()
        if not ln.strip():
            flush_p(); flush_l(); flush_t()
        elif ln.lstrip().startswith("|"):
            flush_p(); flush_l(); tbl.append(ln)
        elif re.match(r"^\s*[-•] ", ln):
            flush_p(); flush_t()
            if lst[0] != "ul":
                flush_l(); lst[0] = "ul"
            lst[1].append(re.sub(r"^\s*[-•] ", "", ln))
        elif re.match(r"^\s*\d+[.)] ", ln):
            flush_p(); flush_t()
            if lst[0] != "ol":
                flush_l(); lst[0] = "ol"
            lst[1].append(re.sub(r"^\s*\d+[.)] ", "", ln))
        else:
            flush_l(); flush_t(); para.append(ln.strip())
    flush_c(); flush_p(); flush_l(); flush_t()
    return Markup("\n".join(out))
