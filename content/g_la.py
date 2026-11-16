"""ENGM chapter 'Linear Algebra': extra generators; explanations show the working (minors, row operations, polynomials)."""
import math
from fractions import Fraction as F

from content.kit import *

S = "ENGM"
MAT, LIN = "Matrices & Determinants", "Linear Equations & Eigenvalues"


def mx(m):
    return "```\n" + "\n".join("[ " + "  ".join("%3s" % fm(x) for x in row) + " ]" for row in m) + "\n```"


def fm(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else "%d/%d" % (x.numerator, x.denominator)


def det2(a, b, c, d):
    return a * d - b * c


def det3(m):
    return m[0][0] * det2(m[1][1], m[1][2], m[2][1], m[2][2]) - m[0][1] * det2(m[1][0], m[1][2], m[2][0], m[2][2]) + m[0][2] * det2(m[1][0], m[1][1], m[2][0], m[2][1])


def minor(m, i, j):
    return [[m[a][b] for b in range(3) if b != j] for a in range(3) if a != i]


def cof(m, i, j):
    x = minor(m, i, j)
    return (-1) ** (i + j) * det2(x[0][0], x[0][1], x[1][0], x[1][1])


def rref_steps(rows):
    """Row-reduce to echelon form with fractions; returns (rank, list of echelon matrices)."""
    m = [[F(x) for x in row] for row in rows]
    rk, steps = 0, []
    for c in range(len(m[0])):
        piv = next((i for i in range(rk, len(m)) if m[i][c] != 0), None)
        if piv is None:
            continue
        m[rk], m[piv] = m[piv], m[rk]
        for i in range(rk + 1, len(m)):
            if m[i][c] != 0:
                f = m[i][c] / m[rk][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[rk])]
        rk += 1
    return rk, m


def rank(rows):
    return rref_steps(rows)[0]


@gen(S, MAT, "Determinant by expansion", n=70, diff="easy")
def la_det(r):
    m = [[r.randint(-4, 6) for _ in range(3)] for _ in range(3)]
    d = det3(m)
    i = r.randint(0, 2)
    kind = r.choice(["val", "val", "cof", "tri", "swap", "row"])
    terms = " + ".join("%d·(%d)" % (m[0][j] * (-1) ** j, det2(*[x for rw in minor(m, 0, j) for x in rw])) for j in range(3))
    work = "Expand along the first row: det = a₁₁M₁₁ − a₁₂M₁₂ + a₁₃M₁₃ = %s = %d." % (terms, d)
    if kind == "val":
        return nat(r, "Determinant of\n%s" % mx(m), d, work)
    if kind == "cof":
        j = r.randint(0, 2)
        return nat(r, "For the matrix\n%s\nwhat is the cofactor C%d%d (row %d, column %d)?" % (mx(m), i + 1, j + 1, i + 1, j + 1), cof(m, i, j),
                   "Delete row %d and column %d, take the 2 × 2 determinant of what is left (the minor %d) and multiply by (−1)^(%d+%d) = %d: cofactor = %d." % (i + 1, j + 1, abs(cof(m, i, j)) if False else (cof(m, i, j) * (-1) ** (i + j)), i + 1, j + 1, (-1) ** (i + j), cof(m, i, j)))
    if kind == "tri":
        t = [[r.randint(1, 5) if j >= i else 0 for j in range(3)] for i in range(3)]
        return nat(r, "Determinant of the triangular matrix\n%s" % mx(t), t[0][0] * t[1][1] * t[2][2], "For a triangular matrix the determinant is the product of the diagonal: %d·%d·%d = %d." % (t[0][0], t[1][1], t[2][2], t[0][0] * t[1][1] * t[2][2]))
    if kind == "swap":
        m2 = [m[1], m[0], m[2]]
        return nat(r, "det of A is %d. The first two rows of A are interchanged to give B. Find det(B)." % d, -d, "Swapping two rows multiplies the determinant by −1: %d." % (-d))
    k = r.choice([2, 3, -2, 5])
    m2 = [[k * x for x in m[0]], m[1], m[2]]
    return nat(r, "det of A is %d. The first row of A is multiplied by %d to give B (other rows unchanged). Find det(B)." % (d, k), k * d, "Scaling ONE row by k scales the determinant by k (not kⁿ): %d·%d = %d." % (k, d, k * d))


@gen(S, MAT, "Rank by row reduction", n=70, diff="medium")
def la_rank(r):
    m, n = r.choice([(3, 3), (3, 4), (4, 3)]), None
    rows_n, cols = m
    base = [[r.randint(-3, 4) for _ in range(cols)] for _ in range(2)]
    rows = [list(b) for b in base]
    while len(rows) < rows_n:
        a, b = r.choice([-2, -1, 1, 2]), r.choice([-1, 0, 1, 2])
        if r.random() < .6:
            rows.append([a * x + b * y for x, y in zip(*base)])
        else:
            rows.append([r.randint(-3, 4) for _ in range(cols)])
    r.shuffle(rows)
    rk, ech = rref_steps(rows)
    return mcq(r, "Rank of the %d × %d matrix\n%s" % (rows_n, cols, mx(rows)), rk, [x for x in range(0, 4) if x != rk],
               "Eliminate below each pivot (row operations never change the rank). Echelon form:\n%s\nThe number of non-zero rows is %d, so the rank is %d. (Rank ≤ min(%d, %d).)" % (mx(ech), rk, rk, rows_n, cols))


@gen(S, MAT, "Inverse and adjoint", n=70, diff="medium")
def la_inv(r):
    kind = r.choice(["inv2", "invdet", "adjdet", "entry", "ainv_tr"])
    if kind == "inv2":
        while True:
            a, b, c, d = [r.randint(-4, 5) for _ in range(4)]
            if a * d - b * c in (1, -1, 2, -2, 3, 5):
                break
        dt = a * d - b * c
        i = r.randint(0, 1)
        j = r.randint(0, 1)
        inv = [[F(d, dt), F(-b, dt)], [F(-c, dt), F(a, dt)]]
        return mcq(r, "For A = [[%d, %d], [%d, %d]], the (%d, %d) entry of A⁻¹ is" % (a, b, c, d, i + 1, j + 1), inv[i][j],
                   [inv[1 - i][1 - j], -inv[i][j], F(inv[i][j]) * dt if dt not in (1,) else inv[i][j] + 1, inv[j][i] + 1],
                   "For a 2 × 2 matrix A⁻¹ = (1/det)·[[d, −b], [−c, a]] with det = %d·%d − %d·%d = %d. So A⁻¹ = %s and the (%d, %d) entry is %s." % (a, d, b, c, dt, [[fm(x) for x in row] for row in inv], i + 1, j + 1, fm(inv[i][j])))
    n = r.choice([2, 3, 3])
    d = r.choice([-3, -2, 2, 3, 4, 5])
    if kind == "invdet":
        return nat(r, "A is an invertible %d × %d matrix with det(A) = %d. Find det(2A⁻¹)·det(A)." % (n, n, d), 2 ** n,
                   "det(2A⁻¹) = 2ⁿ·det(A⁻¹) = 2^%d/%d. Multiplying by det(A) = %d gives 2^%d = %d." % (n, d, d, n, 2 ** n))
    if kind == "adjdet":
        return nat(r, "A is %d × %d with det(A) = %d. Find det(adj A)." % (n, n, d), d ** (n - 1), "A·adj(A) = det(A)·I; taking determinants, det(A)·det(adj A) = det(A)ⁿ, so det(adj A) = det(A)^(n−1) = %d." % d ** (n - 1))
    if kind == "ainv_tr":
        m = [[r.randint(1, 4) for _ in range(3)] for _ in range(3)]
        dt = det3(m)
        if dt == 0:
            raise Skip()
        adj = [[cof(m, j, i) for j in range(3)] for i in range(3)]
        t = sum(adj[i][i] for i in range(3))
        return nat(r, "Find the trace of adj(A) for\n%s" % mx(m), t,
                   "adj(A) is the transpose of the cofactor matrix. Its diagonal entries are the cofactors C11, C22, C33 = %d, %d, %d, so the trace is %d." % (cof(m, 0, 0), cof(m, 1, 1), cof(m, 2, 2), t))
    m = [[r.randint(1, 4) for _ in range(3)] for _ in range(3)]
    dt = det3(m)
    if dt == 0:
        raise Skip()
    i, j = r.randint(0, 2), r.randint(0, 2)
    adj = [[cof(m, jj, ii) for jj in range(3)] for ii in range(3)]
    return mcq(r, "For\n%s\nthe (%d, %d) entry of adj(A) is" % (mx(m), i + 1, j + 1), adj[i][j],
               [adj[j][i] + 1 if adj[j][i] == adj[i][j] else adj[j][i], -adj[i][j] if adj[i][j] else 7, adj[i][j] + dt, cof(m, i, j) + 2],
               "adj(A) is the TRANSPOSE of the cofactor matrix, so adj(A)[%d][%d] = cofactor C%d%d = %d. (Using C%d%d = %d would be the classic mistake.)" % (i + 1, j + 1, j + 1, i + 1, adj[i][j], i + 1, j + 1, cof(m, i, j)))


@gen(S, LIN, "Parameter in a linear system", n=70, diff="hard", marks=2)
def la_param(r):
    s1, t = r.randint(3, 9), r.randint(5, 15)
    c = r.choice([3, 4, 5])        # critical coefficient
    lo = r.choice([2, 3])
    kind = r.choice(["uniq", "noneq", "inf", "hom", "mu"])
    eqs = "x + y + z = %d\nx + %dy + %dz = %d\nx + %dy + λz = μ" % (s1, lo, c, t, lo)
    base = "Subtract equation 2 from equation 3: (λ − %d)z = μ − %d.\n" % (c, t)
    q = "For which values of λ and μ does the system\n```\n%s\n```\nhave " % eqs
    if kind == "uniq":
        return mcq(r, q + "a unique solution?", "λ ≠ %d (any μ)" % c, ["λ = %d and μ = %d" % (c, t), "λ = %d and μ ≠ %d" % (c, t), "λ ≠ %d and μ = %d only" % (c, t)],
                   base + "If λ ≠ %d, z = (μ − %d)/(λ − %d) is determined for every μ, and then y and x follow: a unique solution." % (c, t, c))
    if kind == "noneq":
        return mcq(r, q + "NO solution?", "λ = %d and μ ≠ %d" % (c, t), ["λ = %d and μ = %d" % (c, t), "λ ≠ %d" % c, "μ = %d and λ ≠ %d" % (t, c)],
                   base + "If λ = %d the equation reads 0 = μ − %d, impossible unless μ = %d. So there is no solution when λ = %d and μ ≠ %d." % (c, t, t, c, t))
    if kind == "inf":
        return mcq(r, q + "infinitely many solutions?", "λ = %d and μ = %d" % (c, t), ["λ = %d and μ ≠ %d" % (c, t), "λ ≠ %d and μ = %d" % (c, t), "λ ≠ %d and μ ≠ %d" % (c, t)],
                   base + "If λ = %d and μ = %d the last equation becomes 0 = 0. Two independent equations in three unknowns leave one free variable: infinitely many solutions." % (c, t))
    if kind == "mu":
        return nat(r, "In the system\n```\n%s\n```\nlet λ = %d. For exactly one value of μ the system is consistent. What is that μ?" % (eqs, c), t,
                   base + "With λ = %d the left side is 0, so the system is consistent only if μ − %d = 0, i.e. μ = %d." % (c, t, t))
    k = r.choice([2, 3, 4, 6])
    dk = (lo - 1) * (k - c)
    if dk == 0:
        raise Skip()
    return nat(r, "Find the determinant D of the coefficient matrix of x + y + z = 0, x + %dy + %dz = 0, x + %dy + %dz = 0." % (lo, c, lo, k), dk,
               "Subtract row 1 from rows 2 and 3, then row 2 from row 3: the matrix becomes upper triangular with diagonal 1, %d, %d, so D = (%d − 1)(%d − %d) = %d. It is non-zero, so only the trivial solution exists." % (lo - 1, k - c, lo, k, c, dk))


@gen(S, LIN, "Characteristic polynomial", n=70, diff="medium")
def la_charpoly(r):
    m = [[r.randint(-3, 4) for _ in range(2)] for _ in range(2)]
    tr, dt = m[0][0] + m[1][1], det2(m[0][0], m[0][1], m[1][0], m[1][1])
    kind = r.choice(["poly", "cayley", "pow", "ev", "trsq"])
    sgn = lambda v: "%s %d" % ("+" if v >= 0 else "−", abs(v))
    cp = "λ² %s λ %s" % ("− %d" % tr if tr >= 0 else "+ %d" % -tr, sgn(dt))
    base = "For a 2 × 2 matrix the characteristic polynomial is λ² − (trace)λ + det. Here trace = %d and det = %d·%d − %d·%d = %d, so it is %s." % (tr, m[0][0], m[1][1], m[0][1], m[1][0], dt, cp)
    if kind == "poly":
        return nat(r, "A = [[%d, %d], [%d, %d]]. The characteristic equation is λ² + pλ + q = 0. Find p + q." % (m[0][0], m[0][1], m[1][0], m[1][1]), -tr + dt, base + " So p = %d, q = %d and p + q = %d." % (-tr, dt, -tr + dt))
    if kind == "cayley":
        k = r.randint(2, 4)
        # A^2 = tr*A - dt*I  ->  A^2 - tr A + dt I = 0 ; compute entry (1,1) of A^2 and compare
        a2 = [[sum(m[i][k2] * m[k2][j] for k2 in range(2)) for j in range(2)] for i in range(2)]
        i, j = r.randint(0, 1), r.randint(0, 1)
        return nat(r, "A = [[%d, %d], [%d, %d]]. Using the Cayley–Hamilton theorem, express A² as αA + βI. What is the (%d, %d) entry of A²?" % (m[0][0], m[0][1], m[1][0], m[1][1], i + 1, j + 1), a2[i][j],
                   base + " Cayley–Hamilton: A² − %dA + %dI = 0, so A² = %dA %s %dI. Entry (%d, %d): %d." % (tr, dt, tr, "−" if dt >= 0 else "+", abs(dt), i + 1, j + 1, a2[i][j]))
    if kind == "pow":
        return nat(r, "A has eigenvalues λ₁ and λ₂ with λ₁ + λ₂ = %d and λ₁λ₂ = %d. Find λ₁² + λ₂²." % (tr, dt), tr * tr - 2 * dt, "λ₁² + λ₂² = (λ₁ + λ₂)² − 2λ₁λ₂ = %d − %d = %d. This equals the trace of A²." % (tr * tr, 2 * dt, tr * tr - 2 * dt))
    if kind == "trsq":
        a2 = [[sum(m[i][k2] * m[k2][j] for k2 in range(2)) for j in range(2)] for i in range(2)]
        return nat(r, "A = [[%d, %d], [%d, %d]]. What is the sum of the eigenvalues of A²?" % (m[0][0], m[0][1], m[1][0], m[1][1]), a2[0][0] + a2[1][1],
                   "Eigenvalues of A² are the squares λ², so their sum is trace(A²) = (λ₁ + λ₂)² − 2λ₁λ₂ = %d − %d = %d." % (tr * tr, 2 * dt, tr * tr - 2 * dt))
    disc = tr * tr - 4 * dt
    if disc < 0:
        raise Skip()
    s = math.isqrt(disc)
    if s * s != disc:
        raise Skip()
    l1, l2 = F(tr + s, 2), F(tr - s, 2)
    return mcq(r, "The eigenvalues of A = [[%d, %d], [%d, %d]] are" % (m[0][0], m[0][1], m[1][0], m[1][1]), "%s and %s" % (fm(max(l1, l2)), fm(min(l1, l2))),
               ["%s and %s" % (fm(-l1), fm(-l2)), "%s and %s" % (fm(l1 + 1), fm(l2 - 1)), "%s and %s" % (fm(dt), fm(tr))],
               base + " Roots of the polynomial: λ = (%d ± √%d)/2 = %s and %s." % (tr, disc, fm(l1), fm(l2)))


@gen(S, LIN, "Eigenvalue functions", n=60, diff="medium")
def la_evfun(r):
    n = r.randint(3, 4)
    ev = [r.randint(-3, 5) for _ in range(n)]
    kind = r.choice(["poly", "invsum", "det_poly", "tracepow", "sing"])
    if kind == "poly":
        a, b = r.randint(1, 3), r.randint(-3, 4)
        vals = [x * x + a * x + b for x in ev]
        return nat(r, "A %d × %d matrix A has eigenvalues %s. What is the trace of A² + %dA %s %dI?" % (n, n, J(ev), a, "+" if b >= 0 else "−", abs(b)), sum(vals),
                   "Each eigenvalue λ of A becomes λ² + %dλ %s %d for the matrix polynomial: %s. Their sum, the trace, is %d." % (a, "+" if b >= 0 else "−", abs(b), J(vals), sum(vals)))
    if kind == "invsum":
        ev = [x for x in ev if x != 0] or [1, 2, 3]
        s = sum(F(1, x) for x in ev)
        return mcq(r, "An invertible matrix has eigenvalues %s. The trace of A⁻¹ is" % J(ev), s, [sum(ev), F(1, sum(ev)) if sum(ev) else 5, s + 1, -s],
                   "The eigenvalues of A⁻¹ are the reciprocals %s. Their sum is %s." % (", ".join("1/%d" % x for x in ev), fm(s)))
    if kind == "det_poly":
        k = r.randint(1, 3)
        p = math.prod(x - k for x in ev)
        return nat(r, "A %d × %d matrix A has eigenvalues %s. What is det(A − %dI)?" % (n, n, J(ev), k), p,
                   "The eigenvalues of A − %dI are λ − %d: %s. The determinant is their product: %d." % (k, k, J([x - k for x in ev]), p))
    if kind == "tracepow":
        k = r.choice([2, 3])
        return nat(r, "A has eigenvalues %s. The trace of A%s is" % (J(ev), "²" if k == 2 else "³"), sum(x ** k for x in ev), "Eigenvalues of Aᵏ are λᵏ: %s, summing to %d." % (J([x ** k for x in ev]), sum(x ** k for x in ev)))
    return mcq(r, "A %d × %d matrix has eigenvalues %s. Which statement is true?" % (n, n, J(ev)), "A is singular" if 0 in ev else "A is invertible",
               ["A is singular" if 0 not in ev else "A is invertible", "A is nilpotent", "The trace is zero"],
               "A matrix is singular exactly when 0 is an eigenvalue (the product of the eigenvalues, the determinant, is then 0). %s" % ("Here 0 is an eigenvalue." if 0 in ev else "Here no eigenvalue is 0, so det ≠ 0."))


def J(a):
    return ", ".join(map(str, a))
