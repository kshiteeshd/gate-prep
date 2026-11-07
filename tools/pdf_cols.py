"""Column-aware text extraction for the PYQ books (pypdf visitor). usage: python pdf_cols.py in.pdf out.txt"""
import sys
import pypdf


def page_lines(p):
    fr = []

    def v(text, cm, tm, fd, fs):
        if text.strip():
            x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
            y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
            fr.append((x, y, text, fs or 10))
    p.extract_text(visitor_text=v)
    if not fr:
        return []
    w = float(p.mediabox.width)
    mid = w / 2
    cross = sum(1 for x, y, t, fs in fr if x < mid - 6 and x + len(t.strip()) * fs * 0.36 > mid + 6)
    two = cross <= 5 and sum(1 for a in fr if a[0] > mid + 2) >= 8 and sum(1 for a in fr if a[0] < mid - 2) >= 8

    def mk(items):
        items = sorted(items, key=lambda a: (-round(a[1] / 3), a[0]))
        lines, cur, cy = [], [], None
        for x, y, t, fs in items:
            if cy is None or abs(y - cy) <= 3:
                cur.append(t.strip('\n'))
                cy = y if cy is None else cy
            else:
                lines.append(" ".join(cur))
                cur, cy = [t.strip('\n')], y
        if cur:
            lines.append(" ".join(cur))
        return lines
    if two:
        return mk([a for a in fr if a[0] < mid + 2]) + [""] + mk([a for a in fr if a[0] >= mid + 2])
    return mk(fr)


def main(src, dst):
    r = pypdf.PdfReader(src)
    with open(dst, "w", encoding="utf-8") as f:
        for i, p in enumerate(r.pages):
            try:
                ls = page_lines(p)
            except Exception as e:
                ls = ["<<page error %s>>" % e]
            f.write("\n".join(ls) + "\n\f<<PAGE %d>>\n" % (i + 1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
