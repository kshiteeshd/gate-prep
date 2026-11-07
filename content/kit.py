"""Question-authoring kit: parametric generators (answers computed by code) + compact curated entries."""
import math
import random
from fractions import Fraction

REG = []   # parametric generators
CUR = []   # curated question groups


class Skip(Exception):
    """Raise inside a generator to discard a degenerate random draw."""


def gen(subject, topic, sub, n=40, diff="medium", marks=1):
    def deco(f):
        REG.append(dict(subject=subject, topic=topic, sub=sub, n=n, diff=diff, marks=marks, f=f, name=f.__name__))
        return f
    return deco


def fmt(x):
    if isinstance(x, Fraction):
        return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-9:
            return str(int(round(x)))
        return ("%.4f" % x).rstrip("0").rstrip(".")
    return str(x)


def _sorted_if_numeric(opts):
    try:
        return sorted(opts, key=lambda s: float(Fraction(s)))
    except (ValueError, ZeroDivisionError):
        return opts


def mcq(r, text, correct, wrongs, expl=""):
    c = fmt(correct)
    w = []
    for x in wrongs:
        x = fmt(x)
        if x != c and x not in w:
            w.append(x)
    if len(w) < 3:
        raise Skip()
    if len(w) > 3:
        w = r.sample(w, 3)
    opts = [c] + w
    r.shuffle(opts)
    opts = _sorted_if_numeric(opts)
    return dict(qtype="single", text=text, options=opts, answer=[c], expl=expl)


def msq(r, text, corrects, wrongs, expl=""):
    cs = [fmt(x) for x in corrects]
    ws = [fmt(x) for x in wrongs if fmt(x) not in cs]
    opts = cs + ws
    if len(set(opts)) != len(opts) or len(opts) < 4 or not cs or not ws:
        raise Skip()
    r.shuffle(opts)
    return dict(qtype="multiple", text=text, options=opts, answer=cs, expl=expl)


def nat(r, text, value, expl="", tol=0):
    return dict(qtype="numerical", text=text, options=[], answer=[], numeric=float(value), tol=tol, expl=expl)


def near(r, v, k=3):
    """Plausible wrong values around v."""
    if isinstance(v, Fraction):
        v = float(v)
    if float(v).is_integer():
        v = int(v)
        base = [v + 1, v - 1, v + 2, v - 2, v * 2, v // 2, v + 3, v - 3, v + 10, v - 10, v * 3, v + 4, v - 4]
        base = [b for b in base if b != v and (b >= 0 or v < 0)]
    else:
        base = [v * f for f in (0.5, 0.75, 1.25, 1.5, 2, 0.25, 3, 0.8, 1.2)]
    base = list(dict.fromkeys(base))
    r.shuffle(base)
    return base[:k + 3]


def pick(r, seq, k=1):
    return r.sample(list(seq), k) if k > 1 else r.choice(list(seq))


def C(subject, topic, sub, rows):
    """Curated group. Row = (diff, marks, kind, text, options, answer, explanation[, tolerance])
       kind: s = single (answer = index), m = multiple (answer = list of indexes), n = numerical (answer = number)."""
    CUR.append(dict(subject=subject, topic=topic, sub=sub, rows=rows))


def build_curated(g, rng):
    out = []
    for row in g["rows"]:
        d, marks, kind, text, opts, ans, expl = row[:7]
        tol = row[7] if len(row) > 7 else 0
        diff = {"e": "easy", "m": "medium", "h": "hard"}[d]
        if kind == "n":
            q = dict(qtype="numerical", text=text, options=[], answer=[], numeric=float(ans), tol=tol)
        else:
            idx = [ans] if kind == "s" else list(ans)
            corr = [opts[i] for i in idx]
            o = list(opts)
            rng.shuffle(o)
            q = dict(qtype="single" if kind == "s" else "multiple", text=text, options=o, answer=corr)
        q.update(subject=g["subject"], topic=g["topic"], subtopic=g["sub"], diff=diff, marks=marks, expl=expl, src="curated")
        out.append(q)
    return out
