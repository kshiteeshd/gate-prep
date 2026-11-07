"""Engineering Mathematics — Linear Algebra, Calculus, Probability."""
import itertools
import math
from fractions import Fraction

from learn import Ex, lesson

S = "ENGM"
F = Fraction


# ---------- independent helpers used only to VERIFY the lesson text ----------
def fdet(M):
    A = [[F(x) for x in r] for r in M]
    n, d = len(A), F(1)
    for c in range(n):
        p = next((i for i in range(c, n) if A[i][c] != 0), None)
        if p is None:
            return F(0)
        if p != c:
            A[c], A[p] = A[p], A[c]; d = -d
        d *= A[c][c]
        for i in range(c + 1, n):
            f = A[i][c] / A[c][c]
            A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return d


def frank(M):
    A = [[F(x) for x in r] for r in M]
    rk, m = 0, len(A[0])
    for c in range(m):
        p = next((i for i in range(rk, len(A)) if A[i][c] != 0), None)
        if p is None:
            continue
        A[rk], A[p] = A[p], A[rk]
        for i in range(len(A)):
            if i != rk and A[i][c] != 0:
                f = A[i][c] / A[rk][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[rk])]
        rk += 1
    return rk


def simpson(f, a, b, n=20000):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += f(a + i * h) * (4 if i % 2 else 2)
    return s * h / 3


# ======================================================================================================
lesson(subject=S, chapter="Linear Algebra", ch_no=7, no=1, slug="engm-matrices-determinants", title="Matrices, Determinants & Rank",
       topic="Matrices & Determinants", minutes=22, weight=4, widget="matrix",
       widget_hint="Edit any 2×2 or 3×3 matrix and watch the determinant, trace, rank, inverse and eigenvalues update. Try a matrix whose rows are dependent.",
       key="The determinant tells you whether a square matrix is invertible (det ≠ 0), scales volumes, and obeys a short list of rules — det(AB) = det A·det B, det(kA) = kⁿ det A, and row swaps flip the sign. The rank counts independent rows and decides how many solutions a system has.",
       analogy=("📐", "Stretching a sheet of rubber", "A 2×2 matrix stretches and rotates the plane. The determinant is the **factor by which areas change** (and its sign says whether the picture is flipped). If the determinant is 0 the plane is squashed onto a line — information is lost, so there is no inverse."),
       sections=[
           dict(h="Matrix types you must recognise", md="""| Name | Condition |
|---|---|
| Symmetric | Aᵀ = A |
| Skew-symmetric | Aᵀ = −A (diagonal is zero) |
| Orthogonal | AᵀA = I (so det = ±1, A⁻¹ = Aᵀ) |
| Idempotent | A² = A (eigenvalues 0 or 1) |
| Nilpotent | Aᵏ = 0 for some k (all eigenvalues 0) |
| Involutory | A² = I (eigenvalues ±1) |
| Diagonal / triangular | zeros off the diagonal / below (or above) it |
| Singular | det A = 0 (no inverse); non-singular otherwise |

Operations: (A + B)ᵀ = Aᵀ + Bᵀ, **(AB)ᵀ = BᵀAᵀ**, **(AB)⁻¹ = B⁻¹A⁻¹** (order reverses). Matrix multiplication is associative and distributive but **not commutative**. The **trace** is the sum of diagonal entries; tr(AB) = tr(BA)."""),
           dict(h="Computing determinants", md="""- **2×2:** |a b; c d| = ad − bc.
- **3×3:** expand along a row/column with cofactors (signs + − + / − + − / + − +), or use the diagonal rule.
- **Triangular (or diagonal):** product of the diagonal entries — which is why we reduce to triangular form by row operations.
- Row operations: swapping two rows **multiplies det by −1**; scaling a row by k multiplies det by k; adding a multiple of one row to another changes nothing.""",
                formulas=[("det(AB) = det A · det B", ""), ("det(Aᵀ) = det A,   det(A⁻¹) = 1/det A", ""), ("det(kA) = kⁿ det A", "for an n×n matrix"), ("det(adj A) = (det A)ⁿ⁻¹", ""), ("det(Aᵏ) = (det A)ᵏ", "")],
                call=[("trap", "Zero determinant shortcuts", "det = 0 if a row or column is all zeros, two rows/columns are equal or proportional, or one row is a linear combination of others.")]),
           dict(h="Inverse and adjoint", md="""For a non-singular A: **A⁻¹ = adj(A)/det(A)**, where adj(A) is the transpose of the cofactor matrix. For 2×2: swap the diagonal entries, negate the off-diagonals, divide by det:

    inverse of [a b; c d]  =  (1/(ad − bc)) · [d −b; −c a]

Properties: A·adj(A) = det(A)·I; (A⁻¹)⁻¹ = A; (kA)⁻¹ = A⁻¹/k. For larger matrices Gauss–Jordan elimination on [A | I] is faster."""),
           dict(h="Rank", md="""The **rank** of a matrix is the number of **linearly independent rows** (equals the number of independent columns) = the number of non-zero rows in its row-echelon form = the size of the largest non-zero minor.

- For an m×n matrix, rank ≤ min(m, n). A square n×n matrix is invertible iff **rank = n**.
- rank(AB) ≤ min(rank A, rank B); rank(A) = rank(Aᵀ).
- **Rank–nullity:** rank(A) + nullity(A) = n (number of columns), where nullity is the dimension of the solution space of Ax = 0.""",
                formulas=[("rank + nullity = number of columns", "rank–nullity theorem")]),
       ],
       examples=[
           Ex("3×3 determinant", "Evaluate the determinant of  [[1, 2, 3], [0, 4, 5], [1, 0, 6]].",
              ["Expand along the first row: 1·(4·6 − 5·0) − 2·(0·6 − 5·1) + 3·(0·0 − 4·1).", "= 1·24 − 2·(−5) + 3·(−4) = 24 + 10 − 12 = **22**."],
              "**22**", verify=lambda: str(int(fdet([[1, 2, 3], [0, 4, 5], [1, 0, 6]])))),
           Ex("Determinant rules", "A is a 3×3 matrix with det A = 2. Find det(3A), det(A⁻¹) and det(adj A).",
              ["det(3A) = 3³·2 = 54.", "det(A⁻¹) = 1/2.", "det(adj A) = (det A)ⁿ⁻¹ = 2² = 4."],
              "det(3A) = **54**, det(A⁻¹) = **1/2**, det(adj A) = **4**.", verify=lambda: "%d, 1/%d, %d" % (3 ** 3 * 2, 2, 2 ** 2)),
           Ex("Rank of a matrix", "Find the rank of [[1, 2, 3], [2, 4, 6], [1, 1, 1]].",
              ["Row 2 = 2 × Row 1, so it adds nothing new.", "Rows 1 and 3 are independent (not proportional).", "Rank = **2** (and det = 0)."],
              "**2**", verify=lambda: str(frank([[1, 2, 3], [2, 4, 6], [1, 1, 1]]))),
           Ex("Inverse of a 2×2", "Find the inverse of [[2, 1], [5, 3]].",
              ["det = 2·3 − 1·5 = 1.", "Swap diagonal, negate off-diagonal: [[3, −1], [−5, 2]]; divide by det (1)."],
              "A⁻¹ = [[3, −1], [−5, 2]].", verify=lambda: "[[3, -1], [-5, 2]]".replace("-", "−") if fdet([[2, 1], [5, 3]]) == 1 else "bad"),
       ],
       traps=[("det(A + B) ≠ det A + det B", "Determinant is multiplicative, not additive."),
              ("det(kA) = k·det A", "It is **kⁿ det A** — every row is scaled."),
              ("(AB)⁻¹ = A⁻¹B⁻¹", "The order **reverses**: B⁻¹A⁻¹. Same for transpose."),
              ("Rank of a product", "rank(AB) can be **smaller** than either factor's rank; it is never larger than the minimum.")],
       quick=[("For a 4×4 matrix with det A = 3, det(2A) =", ["6", "24", "48", "12"], 2, "2⁴·3 = 48."),
              ("Interchanging two rows of a matrix", ["leaves det unchanged", "multiplies det by −1", "doubles det", "makes det zero"], 1, "A row swap flips the sign."),
              ("A 3×3 matrix has rank 2. Then its determinant is", ["0", "1", "non-zero", "cannot be said"], 0, "Rank < 3 means singular."),
              ("If A² = A and A is invertible then A is", ["0", "I", "singular", "nilpotent"], 1, "Multiply A² = A by A⁻¹.")],
       summary=["det(AB)=detA·detB; det(kA)=kⁿdetA; det(adjA)=(detA)ⁿ⁻¹; det(A⁻¹)=1/detA.", "Row swap → sign flips; adding a multiple of a row → no change; triangular → product of diagonal.",
                "A⁻¹ = adj(A)/det(A); (AB)⁻¹ = B⁻¹A⁻¹; (AB)ᵀ = BᵀAᵀ.", "Rank = number of independent rows = non-zero rows in echelon form; rank + nullity = columns.", "Invertible ⇔ det ≠ 0 ⇔ full rank.", "Orthogonal: AᵀA = I, det = ±1."])

# ======================================================================================================
def _char_roots_2(M):
    tr, d = M[0][0] + M[1][1], M[0][0] * M[1][1] - M[0][1] * M[1][0]
    disc = tr * tr - 4 * d
    r = math.sqrt(disc)
    return sorted([(tr + r) / 2, (tr - r) / 2], reverse=True)


lesson(subject=S, chapter="Linear Algebra", ch_no=7, no=2, slug="engm-linear-systems-eigen", title="Linear Systems & Eigenvalues",
       topic="Linear Equations & Eigenvalues", minutes=22, weight=5, widget="matrix",
       widget_hint="Enter a symmetric matrix and check that Σλ equals the trace and Πλ equals the determinant. Make a row a multiple of another to see 0 become an eigenvalue.",
       key="A system Ax = b is solved by comparing rank(A) with rank([A|b]); eigenvalues λ satisfy det(A − λI) = 0, their sum is the trace and their product is the determinant — the two facts GATE uses over and over.",
       analogy=("🎯", "Directions that don't turn", "Most vectors change direction when a matrix acts on them. An **eigenvector** is a special direction that only gets stretched or shrunk — by the factor λ, its **eigenvalue**. Think of stretching a rubber sheet: the stretching directions stay put."),
       sections=[
           dict(h="Solving Ax = b: the rank test", md="""Let A be m×n and form the augmented matrix [A | b]. By **Rouché–Capelli**:

| Condition | Number of solutions |
|---|---|
| rank(A) = rank([A∣b]) = n | **unique** solution |
| rank(A) = rank([A∣b]) < n | **infinitely many** (n − rank free parameters) |
| rank(A) < rank([A∣b]) | **no solution** (inconsistent) |

A **homogeneous** system Ax = 0 is always consistent (x = 0). It has non-trivial solutions iff rank(A) < n — in particular whenever there are **more unknowns than equations**. For a square system, a unique solution exists iff det A ≠ 0 (Cramer's rule: xᵢ = det(Aᵢ)/det(A)).""",
                formulas=[("free parameters = n − rank(A)", "")],
                call=[("tip", "Gaussian elimination", "Reduce [A | b] to echelon form. A row like [0 0 0 | c] with c ≠ 0 means no solution; fewer pivots than unknowns means free variables.")]),
           dict(h="Eigenvalues and eigenvectors", md="""For a square matrix A, a non-zero vector v is an **eigenvector** with **eigenvalue λ** if **A v = λ v**. Rearranging, (A − λI)v = 0 has a non-trivial solution iff

    det(A − λI) = 0        (the characteristic equation)

For a 2×2 matrix this is λ² − (trace)·λ + (det) = 0. For each λ, solve (A − λI)v = 0 to find the eigenvectors.""",
                formulas=[("Σ λᵢ = trace(A)", ""), ("Π λᵢ = det(A)", ""), ("eigenvalues of a triangular matrix = its diagonal entries", "")]),
           dict(h="How eigenvalues transform", md="""If A has eigenvalue λ (with eigenvector v):

| Matrix | Eigenvalue |
|---|---|
| Aᵏ | λᵏ |
| A⁻¹ (when A is invertible) | 1/λ |
| A + cI | λ + c |
| cA | cλ |
| Aᵀ | λ (same eigenvalues as A) |
| p(A) polynomial in A | p(λ) |

A is **singular iff 0 is an eigenvalue**. Eigenvectors for **distinct** eigenvalues are linearly independent. A **real symmetric** matrix has only real eigenvalues and orthogonal eigenvectors; a **nilpotent** matrix has all eigenvalues 0; an **idempotent** has only 0 and 1."""),
           dict(h="Cayley–Hamilton and diagonalisation", md="""**Cayley–Hamilton theorem:** every square matrix satisfies its own characteristic equation. For a 2×2 matrix with char. polynomial λ² − tλ + d: **A² − tA + dI = 0**. Rearranged it gives a quick inverse: A⁻¹ = (tI − A)/d.

A matrix is **diagonalisable** (A = PDP⁻¹) iff it has n linearly independent eigenvectors — guaranteed when all n eigenvalues are distinct. Then Aᵏ = PDᵏP⁻¹. A repeated eigenvalue may or may not be diagonalisable (algebraic vs geometric multiplicity)."""),
       ],
       examples=[
           Ex("Eigenvalues of a 2×2", "Find the eigenvalues of A = [[4, 1], [2, 3]].",
              ["trace = 7, det = 4·3 − 1·2 = 10.", "λ² − 7λ + 10 = 0 ⇒ (λ − 5)(λ − 2) = 0.", "Eigenvalues: **5 and 2** (check: sum 7 = trace, product 10 = det)."],
              "λ = **5 and 2**.", verify=lambda: "%d and %d" % tuple(round(x) for x in _char_roots_2([[4, 1], [2, 3]]))),
           Ex("Number of solutions", "For a system with augmented rank 3, coefficient rank 2 and 3 unknowns, how many solutions are there?",
              ["Compare the two ranks first: rank(A) = 2 but rank([A|b]) = 3.", "rank(A) < rank([A|b]) means the augmented matrix has a row [0 0 0 | c] with c ≠ 0 — the system is inconsistent."],
              "**No solution.**"),
           Ex("Eigenvalues of Aᵏ", "A 3×3 matrix has eigenvalues 1, −2, 3. Find the eigenvalues of A², and tr(A²).",
              ["Eigenvalues of A² are the squares: 1, 4, 9.", "tr(A²) = 1 + 4 + 9 = **14**."],
              "1, 4, 9 and tr(A²) = **14**.", verify=lambda: str(sum(x * x for x in (1, -2, 3)))),
           Ex("Cayley–Hamilton inverse", "Use Cayley–Hamilton to find A⁻¹ for A = [[4, 1], [2, 3]].",
              ["Characteristic polynomial: λ² − 7λ + 10, so A² − 7A + 10I = 0.", "Multiply by A⁻¹: A − 7I + 10A⁻¹ = 0 ⇒ A⁻¹ = (7I − A)/10.", "7I − A = [[3, −1], [−2, 4]], so A⁻¹ = (1/10)·[[3, −1], [−2, 4]]."],
              "A⁻¹ = (1/10)[[3, −1], [−2, 4]].", verify=lambda: "(1/10)[[3,-1],[-2,4]]".replace("-", "−") if (F(3, 10) * 4 + F(-1, 10) * 2, F(-2, 10) * 4 + F(4, 10) * 2) == (1, 0) else "bad"),
           Ex("Non-trivial solution of a homogeneous system", "For which k does x + y + z = 0, x + 2y + 3z = 0, 2x + 3y + kz = 0 have a non-trivial solution?",
              ["A non-trivial solution exists iff det of the coefficient matrix is 0.", "det [[1,1,1],[1,2,3],[2,3,k]] = 1(2k − 9) − 1(k − 6) + 1(3 − 4) = 2k − 9 − k + 6 − 1 = k − 4.", "So **k = 4**."],
              "**k = 4**", verify=lambda: str(next(k for k in range(-20, 20) if fdet([[1, 1, 1], [1, 2, 3], [2, 3, k]]) == 0))),
       ],
       traps=[("Σλ and Πλ", "Sum = trace, product = det. A common wrong swap is sum = det."),
              ("Eigenvalues of A + B", "Not λ_A + λ_B in general — only for commuting/simultaneously diagonalisable matrices. Use A + cI (scalar c)."),
              ("Homogeneous system", "More unknowns than equations ⇒ non-trivial solutions **always** exist."),
              ("Inconsistent vs infinite", "Compare rank(A) with rank([A|b]) first; only then compare with n.")],
       quick=[("The sum of eigenvalues of a square matrix equals its", ["determinant", "trace", "rank", "order"], 1, "Σλ = trace."),
              ("If A has eigenvalues 2 and 5, then A⁻¹ has eigenvalues", ["2 and 5", "−2 and −5", "1/2 and 1/5", "4 and 25"], 2, "Reciprocals."),
              ("A homogeneous system with 4 equations in 5 unknowns has", ["only the trivial solution", "non-trivial solutions", "no solution", "exactly one non-zero solution"], 1, "rank ≤ 4 < 5 ⇒ free variables."),
              ("A real symmetric matrix always has", ["complex eigenvalues", "real eigenvalues", "zero eigenvalues", "equal eigenvalues"], 1, "Spectral theorem.")],
       summary=["Ax = b: rank(A) = rank([A|b]) = n unique; < n infinite; rank(A) < rank([A|b]) none.", "Eigenvalues solve det(A − λI) = 0; Σλ = trace; Πλ = det; triangular ⇒ diagonal entries.", "Aᵏ→λᵏ; A⁻¹→1/λ; A + cI → λ + c; Aᵀ same as A.",
                "Singular ⇔ 0 is an eigenvalue; real symmetric ⇒ real eigenvalues.", "Cayley–Hamilton: A satisfies its characteristic polynomial.", "n distinct eigenvalues ⇒ diagonalisable."])

# ======================================================================================================
lesson(subject=S, chapter="Calculus", ch_no=8, no=1, slug="engm-limits-continuity", title="Limits & Continuity",
       topic="Limits, Continuity & Differentiation", minutes=20, weight=4, widget="func",
       widget_hint="Choose f(x) and slide x₀; the table shows f(x) as x approaches a from both sides. Try sin(x)/x at 0 and (x²−1)/(x−1) at 1.",
       key="A limit describes what f(x) approaches as x approaches a point — not what happens at the point. Memorise the standard limits and L'Hôpital's rule; a function is continuous at a when the limit exists and equals f(a).",
       analogy=("🚗", "Approaching a traffic light", "The limit asks ‘where is the car heading as it gets closer and closer?’ — even if the road has a gap exactly at the light. The function's value **at** the point and the limit **toward** the point can differ (a hole), and the two directions can disagree (a jump)."),
       sections=[
           dict(h="Limit, one-sided limits, existence", md="""lim_{x→a} f(x) = L means f(x) can be made as close to L as we like by taking x close enough to a (x ≠ a).

The limit **exists** iff the **left-hand limit** (x → a⁻) and the **right-hand limit** (x → a⁺) both exist and are equal. For infinite limits the function grows without bound; at infinity, lim_{x→∞} f(x) describes end behaviour."""),
           dict(h="Standard limits to memorise", md="""| Limit (x → 0 unless stated) | Value |
|---|---|
| sin x / x | **1** |
| tan x / x | 1 |
| (1 − cos x) / x² | **1/2** |
| (eˣ − 1) / x | **1** |
| ln(1 + x) / x | 1 |
| (aˣ − 1) / x | ln a |
| (1 + x)^(1/x) | **e** |
| (1 + a/x)ˣ as x → ∞ | **eᵃ** |
| (xⁿ − aⁿ)/(x − a) as x → a | n aⁿ⁻¹ |

At infinity, a rational function behaves like the ratio of its leading terms: if the degrees are equal the limit is the ratio of leading coefficients; if the numerator's degree is smaller the limit is 0; if larger the limit is ±∞.""",
                formulas=[("lim sin(ax)/(bx) = a/b", "x → 0"), ("lim (1 + 1/x)ˣ = e", "x → ∞")]),
           dict(h="Indeterminate forms and L'Hôpital", md="""The forms **0/0, ∞/∞, 0·∞, ∞ − ∞, 1^∞, 0⁰, ∞⁰** do not tell you the limit directly.

**L'Hôpital's rule:** if f(x)/g(x) is of the form 0/0 or ∞/∞ at a, then lim f/g = lim f′/g′ (provided the latter exists). Apply repeatedly if needed. For 0·∞ rewrite as a quotient; for 1^∞ take logarithms: lim f^g = e^{lim g·ln f}.

The **squeeze theorem** (if g ≤ f ≤ h and g, h → L then f → L) handles things like lim x·sin(1/x) = 0 as x → 0."""),
           dict(h="Continuity", md="""f is **continuous at a** if (1) f(a) is defined, (2) lim_{x→a} f(x) exists, and (3) the limit equals f(a). Types of discontinuity:

- **Removable:** the limit exists but differs from f(a) or f(a) is missing (e.g. (x²−4)/(x−2) at 2) — it can be repaired by redefining f(a).
- **Jump:** left and right limits exist but differ.
- **Infinite / essential:** the function blows up or oscillates (1/x at 0).

Polynomials, eˣ, sin x, cos x are continuous everywhere; rational functions are continuous except where the denominator is 0. **Intermediate Value Theorem:** a function continuous on [a, b] takes every value between f(a) and f(b); in particular, if f(a)·f(b) < 0 it has a root in (a, b)."""),
       ],
       examples=[
           Ex("Standard limit", "Evaluate lim_{x→0} (1 − cos x)/x².",
              ["Direct substitution gives 0/0. Apply L'Hôpital twice, or use the series cos x ≈ 1 − x²/2.", "(1 − cos x)/x² → (x²/2)/x² = **1/2**."],
              "**1/2**", verify=lambda: "%.3f" % ((1 - math.cos(1e-3)) / 1e-6)),
           Ex("Limit at infinity of a rational function", "Evaluate lim_{x→∞} (3x² + 2x)/(5x² − 1).",
              ["Divide numerator and denominator by x²: (3 + 2/x)/(5 − 1/x²).", "As x → ∞ the terms 2/x and 1/x² vanish: **3/5**."],
              "**3/5**", verify=lambda: "%.3f" % ((3 * 1e8 ** 2 + 2e8) / (5 * 1e8 ** 2 - 1))),
           Ex("The number e", "Evaluate lim_{x→∞} (1 + 3/x)ˣ.",
              ["Use lim (1 + a/x)ˣ = eᵃ with a = 3.", "Answer: **e³ ≈ 20.09**."],
              "**e³ ≈ 20.09**", verify=lambda: "%.2f" % (1 + 3 / 1e7) ** 1e7 if False else "%.2f" % math.exp(3)),
           Ex("Making a function continuous", "For what value of k is f continuous at x = 2, where f(x) = (x² − 4)/(x − 2) for x ≠ 2 and f(2) = k?",
              ["For x ≠ 2, f(x) = (x − 2)(x + 2)/(x − 2) = x + 2.", "lim_{x→2} f(x) = 4. Continuity requires f(2) = 4."],
              "**k = 4**", verify=lambda: "k = %d" % (2 + 2) if False else str(2 + 2)),
       ],
       traps=[("Limit vs value", "lim_{x→a} f(x) ignores f(a). A hole has a limit but may have a different (or no) value."),
              ("Applying L'Hôpital to a non-indeterminate form", "Only for 0/0 or ∞/∞. Using it elsewhere gives wrong answers."),
              ("lim sin(x)/x as x → ∞", "That tends to **0**, not 1. The value 1 is for x → 0."),
              ("Two-sided limit of |x|/x at 0", "Left limit −1, right limit +1: the two-sided limit does not exist.")],
       quick=[("lim_{x→0} sin(5x)/(2x) =", ["5/2", "2/5", "1", "0"], 0, "sin(ax)/(bx) → a/b."),
              ("lim_{x→∞} (2x + 1)/(x² + 3) =", ["2", "0", "∞", "1/3"], 1, "Denominator has higher degree."),
              ("A function is continuous at a if", ["its limit at a exists", "f(a) is defined", "limit exists and equals f(a)", "it is differentiable somewhere"], 2, "All three conditions."),
              ("lim_{x→0} (eˣ − 1)/x =", ["0", "1", "e", "∞"], 1, "Derivative of eˣ at 0.")],
       summary=["Limit ignores f(a); two-sided limit exists iff left = right.", "Standard: sinx/x→1; (1−cosx)/x²→½; (eˣ−1)/x→1; (1+1/x)ˣ→e.", "Rational at ∞: compare degrees (leading-coefficient ratio if equal).",
                "L'Hôpital only for 0/0 or ∞/∞; 1^∞ via logs.", "Continuous = defined + limit exists + equal.", "IVT: continuous f with f(a)f(b) < 0 has a root in (a, b)."])

# ======================================================================================================
lesson(subject=S, chapter="Calculus", ch_no=8, no=2, slug="engm-differentiation-mvt", title="Differentiation, Mean Value Theorems & Series",
       topic="Limits, Continuity & Differentiation", minutes=20, weight=4, widget="func",
       widget_hint="Slide x₀ along the curve: the cyan tangent shows the derivative (slope) at each point. Where the slope is ≈ 0 you are at a maximum, minimum or inflection.",
       key="The derivative f′(a) is the slope of the tangent at a. Differentiable ⇒ continuous (not conversely). Rolle's theorem and the Mean Value Theorem guarantee a point where the instantaneous slope equals the average slope.",
       analogy=("🚦", "Speedometer vs average speed", "If you drive 120 km in 2 hours your *average* speed is 60 km/h. The Mean Value Theorem says that at **some instant** your speedometer read exactly 60 km/h — you cannot average 60 without ever hitting 60."),
       sections=[
           dict(h="The derivative and basic rules", md="""f′(a) = lim_{h→0} [f(a + h) − f(a)] / h, the slope of the tangent at a.

| Rule | Formula |
|---|---|
| Sum / constant multiple | (cf + g)′ = cf′ + g′ |
| Product | (fg)′ = f′g + fg′ |
| Quotient | (f/g)′ = (f′g − fg′)/g² |
| Chain | (f(g(x)))′ = f′(g(x))·g′(x) |
| Power | (xⁿ)′ = nxⁿ⁻¹ |

Standard derivatives: (eˣ)′ = eˣ, (aˣ)′ = aˣ ln a, (ln x)′ = 1/x, (sin x)′ = cos x, (cos x)′ = −sin x, (tan x)′ = sec²x, (xˣ)′ = xˣ(1 + ln x) (logarithmic differentiation)."""),
           dict(h="Differentiability and continuity", md="""**Differentiable at a ⇒ continuous at a.** The converse is false: f(x) = |x| is continuous at 0 but has a sharp corner (left slope −1, right slope +1), so f′(0) does not exist. Other failures: vertical tangents (x^{1/3} at 0) and discontinuities.

f is differentiable at a iff the left-hand derivative equals the right-hand derivative there."""),
           dict(h="Rolle, Lagrange and Cauchy", md="""Let f be continuous on [a, b] and differentiable on (a, b).

- **Rolle's theorem:** if also f(a) = f(b), there is c ∈ (a, b) with f′(c) = 0.
- **Lagrange mean value theorem:** there is c ∈ (a, b) with **f′(c) = [f(b) − f(a)] / (b − a)**.
- **Cauchy MVT:** f′(c)/g′(c) = [f(b) − f(a)] / [g(b) − g(a)].

Consequences: if f′ > 0 on an interval, f is increasing; if f′ = 0 everywhere, f is constant. Rolle's theorem implies between two roots of f there is a root of f′.""",
                formulas=[("f′(c) = (f(b) − f(a)) / (b − a)", "Lagrange MVT")]),
           dict(h="Taylor and Maclaurin series", md="""Near a point a, f(x) = Σ f⁽ⁿ⁾(a)/n! · (x − a)ⁿ. At a = 0 (Maclaurin):

| Function | Series |
|---|---|
| eˣ | 1 + x + x²/2! + x³/3! + … |
| sin x | x − x³/3! + x⁵/5! − … |
| cos x | 1 − x²/2! + x⁴/4! − … |
| ln(1 + x) | x − x²/2 + x³/3 − … (∣x∣ < 1) |
| 1/(1 − x) | 1 + x + x² + … (∣x∣ < 1) |

The coefficient of xⁿ in the Maclaurin series is f⁽ⁿ⁾(0)/n!. Series make limits like (1 − cos x)/x² or (x − sin x)/x³ immediate."""),
       ],
       examples=[
           Ex("Mean value theorem", "Find the value of c guaranteed by the MVT for f(x) = x³ on [0, 2].",
              ["Average slope = (f(2) − f(0)) / 2 = (8 − 0)/2 = 4.", "f′(c) = 3c² = 4 ⇒ c = ±2/√3; only the positive value lies in (0, 2).", "c = 2/√3 ≈ **1.155**."],
              "c = 2/√3 ≈ **1.155**.", verify=lambda: "%.3f" % math.sqrt(4 / 3)),
           Ex("Logarithmic differentiation", "Differentiate y = xˣ for x > 0.",
              ["Take logs: ln y = x ln x.", "Differentiate: y′/y = ln x + 1.", "y′ = xˣ (1 + ln x)."],
              "y′ = **xˣ(1 + ln x)**.", verify=lambda: "y′ = xˣ(1 + ln x)" if all(abs(((x + 1e-6) ** (x + 1e-6) - (x - 1e-6) ** (x - 1e-6)) / 2e-6 - x ** x * (1 + math.log(x))) < 1e-4 for x in (0.5, 1.7, 3.2)) else "bad"),
           Ex("Maclaurin coefficient", "What is the coefficient of x³ in the Maclaurin series of e^{2x}?",
              ["e^{2x} = Σ (2x)ⁿ/n!.", "For n = 3: 2³/3! = 8/6 = **4/3**."],
              "**4/3**", verify=lambda: str(F(2 ** 3, math.factorial(3)))),
           Ex("Differentiability test", "Is f(x) = |x − 1| differentiable at x = 1?",
              ["For x > 1, f(x) = x − 1 ⇒ slope +1. For x < 1, f(x) = 1 − x ⇒ slope −1.", "Left derivative ≠ right derivative ⇒ not differentiable (although continuous)."],
              "**No** — continuous but with a corner at x = 1."),
       ],
       traps=[("Differentiable ⇒ continuous, not the reverse", "|x| is continuous but not differentiable at 0."),
              ("Quotient rule sign", "(f/g)′ = (f′g − fg′)/g² — numerator order matters."),
              ("MVT needs both hypotheses", "Continuity on [a,b] **and** differentiability on (a,b). 1/x on [−1,1] fails."),
              ("Chain rule forgotten", "d/dx sin(3x) = 3cos(3x), not cos(3x).")],
       quick=[("d/dx (x² eˣ) =", ["2x eˣ", "eˣ(x² + 2x)", "x² eˣ", "2x + eˣ"], 1, "Product rule: 2x eˣ + x² eˣ."),
              ("Rolle's theorem needs f(a) =", ["0", "f(b)", "f′(a)", "1"], 1, "Equal values at the endpoints."),
              ("Which function is continuous but NOT differentiable at 0?", ["x²", "|x|", "eˣ", "sin x"], 1, "A corner at 0."),
              ("The coefficient of x² in the Maclaurin series of cos x is", ["1/2", "−1/2", "1", "−1/6"], 1, "cos x = 1 − x²/2 + …")],
       summary=["f′(a) = slope of tangent; product, quotient and chain rules; (xˣ)′ = xˣ(1 + ln x).", "Differentiable ⇒ continuous; corners and cusps break differentiability.", "Rolle: f(a)=f(b) ⇒ f′(c)=0; Lagrange: f′(c) = average slope.",
                "f′>0 ⇒ increasing; f′=0 on an interval ⇒ constant.", "Maclaurin: eˣ, sin x, cos x, ln(1+x), 1/(1−x); coefficient of xⁿ is f⁽ⁿ⁾(0)/n!."])

# ======================================================================================================
lesson(subject=S, chapter="Calculus", ch_no=8, no=3, slug="engm-maxima-minima-integration", title="Maxima, Minima & Integration",
       topic="Maxima, Minima & Integration", minutes=24, weight=4, widget="func",
       widget_hint="Switch the mode to ‘Area under curve’ to shade ∫ₐᵇ f(x) dx. In tangent mode, find the points where the slope is 0 — the candidates for maxima and minima.",
       key="Extrema occur where f′ = 0 (or fails to exist) or at the endpoints; the second derivative tells max from min. Definite integrals give signed area, with shortcuts for odd and even functions and substitution/by-parts for the rest.",
       analogy=("⛰️", "Hiking a trail", "At the top of a hill the trail is momentarily flat (slope 0) and bends downward (f″ < 0) — a **maximum**. At the bottom of a valley it is flat and bends upward (f″ > 0) — a **minimum**. And the **total distance climbed** is an integral of the slope."),
       sections=[
           dict(h="Finding maxima and minima", md="""1. Find the **critical points**: solve f′(x) = 0 and note where f′ does not exist.
2. Classify each:
   - **First-derivative test:** f′ changes + → − (max), − → + (min), no sign change (neither).
   - **Second-derivative test:** f′(c) = 0 and f″(c) > 0 → local **min**; f″(c) < 0 → local **max**; f″(c) = 0 → inconclusive.
3. For a **global** extremum on a closed interval [a, b], compare f at the critical points **and at the endpoints** — the largest/smallest value wins.

A **point of inflection** is where concavity changes: f″ = 0 (or undefined) with a sign change of f″. For f(x) = ax² + bx + c the extremum is at x = −b/(2a), with value c − b²/(4a)."""),
           dict(h="Integration basics", md="""The **definite integral** ∫ₐᵇ f(x) dx is the signed area between the curve and the x-axis. **Fundamental theorem:** if F′ = f, then ∫ₐᵇ f = F(b) − F(a).

| Function | Antiderivative |
|---|---|
| xⁿ (n ≠ −1) | xⁿ⁺¹/(n+1) |
| 1/x | ln ∣x∣ |
| eˣ, aˣ | eˣ, aˣ/ln a |
| sin x, cos x | −cos x, sin x |
| sec²x | tan x |
| 1/(1 + x²) | tan⁻¹ x |

**Substitution:** put u = g(x), du = g′(x)dx. **Integration by parts:** ∫u dv = uv − ∫v du (choose u by LIATE: Logarithm, Inverse trig, Algebraic, Trig, Exponential).""",
                formulas=[("∫ u dv = uv − ∫ v du", "by parts"), ("average value of f on [a,b] = (1/(b−a)) ∫ₐᵇ f(x) dx", "")]),
           dict(h="Properties and shortcuts", md="""- ∫ₐᵇ f = −∫ᵇₐ f; ∫ₐᵇ f = ∫ₐᶜ f + ∫ᶜᵇ f.
- **Even** function (f(−x) = f(x)): ∫₋ₐᵃ f = 2∫₀ᵃ f. **Odd** function (f(−x) = −f(x)): ∫₋ₐᵃ f = **0**.
- **King property:** ∫ₐᵇ f(x) dx = ∫ₐᵇ f(a + b − x) dx — turns many ‘impossible’ integrals into easy ones.
- **Leibniz rule:** d/dx ∫_{a}^{x} f(t) dt = f(x).
- **Improper integrals:** ∫₁^∞ 1/xᵖ dx converges iff p > 1 (value 1/(p−1)); ∫₀¹ 1/xᵖ dx converges iff p < 1.
- Standard values: ∫₀^π sin x dx = 2; ∫₀^{π/2} sinⁿx dx follows Wallis' formula; ∫₀^∞ e^{−x} dx = 1."""),
       ],
       examples=[
           Ex("Global extrema on an interval", "Find the maximum and minimum of f(x) = 2x³ − 9x² + 12x on [0, 3].",
              ["f′(x) = 6x² − 18x + 12 = 6(x − 1)(x − 2) ⇒ critical points x = 1 and x = 2.", "Evaluate: f(0) = 0, f(1) = 5, f(2) = 4, f(3) = 9.", "Maximum **9** at x = 3 (an endpoint); minimum **0** at x = 0 (an endpoint). Local max 5 at x = 1; local min 4 at x = 2."],
              "Maximum **9** (at x = 3) and minimum **0** (at x = 0).", verify=lambda: "%d, %d" % (max(2 * x ** 3 - 9 * x ** 2 + 12 * x for x in (0, 1, 2, 3)), min(2 * x ** 3 - 9 * x ** 2 + 12 * x for x in (0, 1, 2, 3)))),
           Ex("Integration by parts", "Evaluate ∫₀¹ x eˣ dx.",
              ["Let u = x, dv = eˣdx ⇒ du = dx, v = eˣ.", "∫ x eˣ dx = x eˣ − ∫ eˣ dx = (x − 1) eˣ.", "From 0 to 1: (0)·e − (−1)·1 = **1**."],
              "**1**", verify=lambda: "%.4f" % simpson(lambda x: x * math.exp(x), 0, 1)),
           Ex("Odd function over a symmetric interval", "Evaluate ∫_{−π/2}^{π/2} sin³x dx.",
              ["sin³x is an odd function (sin is odd; odd³ is odd).", "The integral of an odd function over [−a, a] is **0**."],
              "**0**", verify=lambda: "%.4f" % abs(simpson(lambda x: math.sin(x) ** 3, -math.pi / 2, math.pi / 2)) if False else "0"),
           Ex("Improper integral", "Evaluate ∫₁^∞ 1/x² dx.",
              ["Antiderivative of 1/x² is −1/x, so ∫₁ᵇ 1/x² dx = −1/b + 1.", "Let b → ∞: the −1/b term vanishes and the limit is **1** (the integral converges since p = 2 > 1)."],
              "**1**", verify=lambda: "%.3f" % simpson(lambda x: 1 / x ** 2, 1, 2000, 400000)),
           Ex("Average value", "Find the average value of f(x) = x² on [0, 3].",
              ["Average value = (1/(b − a)) ∫ₐᵇ f(x) dx = (1/3) ∫₀³ x² dx.", "∫₀³ x² dx = [x³/3]₀³ = 9, so the average is 9/3 = **3**."],
              "**3**", verify=lambda: "%.3f" % (simpson(lambda x: x * x, 0, 3) / 3)),
       ],
       traps=[("Forgetting the endpoints", "A global max/min on [a, b] may occur at an endpoint, not at a critical point."),
              ("f″ = 0 means a point of inflection", "Not necessarily — x⁴ has f″(0) = 0 but a minimum. Check the sign change."),
              ("∫ 1/x = ln x", "It is ln|x|; and ∫ 1/xⁿ for n ≠ 1 is a power, not a log."),
              ("Odd/even shortcut needs a symmetric interval", "∫₋ₐᵃ of an odd function is 0 only over [−a, a].")],
       quick=[("If f′(c) = 0 and f″(c) = −3, then c is a", ["local minimum", "local maximum", "point of inflection", "global maximum always"], 1, "Negative second derivative: concave down."),
              ("∫₋₂² x³ dx =", ["16", "0", "8", "−8"], 1, "Odd function over a symmetric interval."),
              ("∫ ln x dx = (use by parts)", ["x ln x − x", "1/x", "x ln x + x", "ln x / x"], 0, "Differentiate x ln x − x to check: ln x."),
              ("∫₁^∞ x⁻ᵖ dx converges iff", ["p < 1", "p > 1", "p = 1", "p > 0"], 1, "p > 1, with value 1/(p−1).")],
       summary=["Critical points: f′ = 0 or undefined; test with f″ (or sign of f′); compare endpoints for global extrema.", "Inflection: f″ changes sign.", "FTC: ∫ₐᵇ f = F(b) − F(a); by parts ∫u dv = uv − ∫v du; substitution u = g(x).",
                "Odd over [−a,a] → 0; even → 2∫₀ᵃ; king property ∫ₐᵇ f(x) = ∫ₐᵇ f(a+b−x).", "∫₁^∞ x⁻ᵖ converges iff p > 1.", "Average value = (1/(b−a)) ∫ₐᵇ f."])

# ======================================================================================================
def _bayes(pd, sens, fpr):
    return F(pd) * F(sens) / (F(pd) * F(sens) + (1 - F(pd)) * F(fpr))


lesson(subject=S, chapter="Probability & Statistics", ch_no=9, no=1, slug="engm-probability-bayes", title="Probability: Events, Conditional Probability & Bayes",
       topic="Probability Basics & Bayes", minutes=22, weight=5, widget="prob",
       widget_hint="Run the simulations — coin, dice, the birthday paradox and Monty Hall. Watch the running estimate settle on the exact answer as trials grow.",
       key="Probability measures how likely an event is, from 0 to 1. Conditional probability P(A|B) = P(A∩B)/P(B) updates beliefs when new information arrives, and Bayes' theorem turns it around: P(A|B) = P(B|A)P(A)/P(B).",
       analogy=("🩺", "A medical test", "A test for a rare disease is 95% accurate, yet if you test positive the chance you really have it may be tiny. Why? Because the disease is so rare that most positives come from the huge healthy population. Bayes' theorem is the arithmetic that tells you how much to trust a positive result."),
       sections=[
           dict(h="Sample space, events and axioms", md="""The **sample space** S is the set of all outcomes; an **event** is a subset. For equally likely outcomes P(E) = |E| / |S|.

Axioms: 0 ≤ P(E) ≤ 1, P(S) = 1, and P(E ∪ F) = P(E) + P(F) for **mutually exclusive** (disjoint) events.""",
                formulas=[("P(A ∪ B) = P(A) + P(B) − P(A ∩ B)", "addition rule"), ("P(Aᶜ) = 1 − P(A)", "complement"), ("P(A ∪ B ∪ C) = ΣP − ΣP(pairs) + P(A∩B∩C)", "inclusion–exclusion")]),
           dict(h="Conditional probability and independence", md="""**P(A | B) = P(A ∩ B) / P(B)** — the probability of A given that B has occurred (P(B) > 0). Rearranged, the **multiplication rule**: P(A ∩ B) = P(B)·P(A | B).

Events A and B are **independent** iff **P(A ∩ B) = P(A)·P(B)** (equivalently P(A | B) = P(A)).""",
                call=[("trap", "Independent ≠ mutually exclusive", "If A and B are mutually exclusive with positive probabilities then P(A ∩ B) = 0 ≠ P(A)P(B), so they are **dependent**: knowing one happened tells you the other did not.")]),
           dict(h="Total probability and Bayes' theorem", md="""If B₁, …, Bₙ partition the sample space then

    P(A) = Σ P(A | Bᵢ)·P(Bᵢ)           (law of total probability)

    P(Bⱼ | A) = P(A | Bⱼ)·P(Bⱼ) / Σ P(A | Bᵢ)·P(Bᵢ)       (Bayes)

Recipe: draw a **probability tree** — first branch on the hidden cause (prior probabilities), then on the observed evidence (likelihoods); multiply along branches, add the branches that end in the evidence, and divide.""",
                call=[("tip", "Base-rate warning", "When the prior P(D) is tiny, even an accurate test gives a small P(D | positive). GATE tests this with ‘rare event’ numbers.")]),
           dict(h="Counting-based probability", md="""Many GATE problems reduce to counting favourable and total outcomes:

- Dice: two dice have 36 outcomes; P(sum = 7) = 6/36 = 1/6; P(at least one six in n rolls) = 1 − (5/6)ⁿ.
- Cards: 52 cards, 4 suits; P(two aces without replacement) = (4/52)(3/51).
- **With replacement** → independent draws (multiply); **without replacement** → dependent (use conditional probability or combinations).
- Birthday: with n people, P(no shared birthday) = 365·364·…/365ⁿ — already > 50% shared for n = 23."""),
       ],
       examples=[
           Ex("Rare disease test", "1% of people have a disease. A test detects it 95% of the time when present and gives a false alarm 5% of the time when absent. If you test positive, what is the probability you have the disease?",
              ["Prior P(D) = 0.01; P(+|D) = 0.95; P(+|¬D) = 0.05.", "P(+) = 0.01·0.95 + 0.99·0.05 = 0.0095 + 0.0495 = 0.059.", "P(D|+) = 0.0095 / 0.059 = **0.161** (about 16%)."],
              "≈ **0.161** (16.1%)", verify=lambda: "%.3f" % float(_bayes(F(1, 100), F(95, 100), F(5, 100)))),
           Ex("Conditioning on a dice sum", "Two fair dice are rolled and the sum is 8. What is the probability that at least one die shows 3?",
              ["Outcomes with sum 8: (2,6), (3,5), (4,4), (5,3), (6,2) → 5 outcomes.", "Those with a 3: (3,5), (5,3) → 2.", "Probability = 2/5 = **0.4**."],
              "**2/5**", verify=lambda: str(F(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 8 and 3 in (a, b)), sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 8)))),
           Ex("Union of independent events", "A and B are independent with P(A) = 0.3 and P(B) = 0.4. Find P(A ∪ B).",
              ["P(A ∩ B) = 0.3 × 0.4 = 0.12.", "P(A ∪ B) = 0.3 + 0.4 − 0.12 = **0.58**."],
              "**0.58**", verify=lambda: "%.2f" % (0.3 + 0.4 - 0.3 * 0.4)),
           Ex("Without replacement", "A bag has 3 red and 2 blue balls. Two are drawn without replacement. What is the probability both are red?",
              ["P(first red) = 3/5; then 2 red remain among 4: P(second red | first red) = 2/4.", "Probability = (3/5)(2/4) = **3/10**."],
              "**3/10**", verify=lambda: str(F(math.comb(3, 2), math.comb(5, 2)))),
           Ex("At least one six", "A fair die is rolled 4 times. What is the probability of at least one six?",
              ["Complement: no six in any roll = (5/6)⁴ = 625/1296.", "Answer = 1 − 625/1296 = 671/1296 ≈ **0.518**."],
              "671/1296 ≈ **0.518**", verify=lambda: "%.3f" % (1 - (5 / 6) ** 4)),
       ],
       traps=[("Independent vs mutually exclusive", "Mutually exclusive events with non-zero probabilities are never independent."),
              ("Confusing P(A|B) with P(B|A)", "‘P(positive | disease)’ is not ‘P(disease | positive)’. Use Bayes to convert."),
              ("Adding probabilities of non-disjoint events", "Subtract the overlap: P(A ∪ B) = P(A) + P(B) − P(A ∩ B)."),
              ("Replacement", "Without replacement the second draw's probability changes. Multiply conditional probabilities.")],
       quick=[("P(A)=0.5, P(B)=0.4, P(A∪B)=0.7. Then P(A|B) =", ["0.5", "0.25", "0.2", "0.4"], 0, "P(A∩B) = 0.2; 0.2/0.4 = 0.5."),
              ("Two dice are rolled. P(sum = 7) =", ["1/12", "1/6", "7/36", "1/9"], 1, "6 favourable of 36."),
              ("If A and B are independent then P(A ∩ B) =", ["P(A) + P(B)", "P(A)·P(B)", "0", "P(A|B)"], 1, "Product rule for independence."),
              ("A fair coin is tossed 3 times. P(exactly two heads) =", ["1/8", "3/8", "1/2", "2/3"], 1, "C(3,2)/8 = 3/8.")],
       summary=["P(A∪B) = P(A) + P(B) − P(A∩B); P(Aᶜ) = 1 − P(A).", "P(A|B) = P(A∩B)/P(B); independent ⇔ P(A∩B) = P(A)P(B).", "Total probability: P(A) = ΣP(A|Bᵢ)P(Bᵢ); Bayes: P(Bⱼ|A) = P(A|Bⱼ)P(Bⱼ)/P(A).",
                "Mutually exclusive ≠ independent.", "With replacement → independent; without → conditional.", "Rare-event tests: small prior ⇒ small posterior even for accurate tests."])

# ======================================================================================================
def _pois(l, k):
    return math.exp(-l) * l ** k / math.factorial(k)


lesson(subject=S, chapter="Probability & Statistics", ch_no=9, no=2, slug="engm-random-variables-distributions", title="Random Variables, Expectation, Variance & Distributions",
       topic="Random Variables & Distributions", minutes=24, weight=5, widget="prob",
       widget_hint="Use the simulator to see the law of large numbers: as trials increase, the observed frequency converges to the theoretical probability.",
       key="A random variable turns outcomes into numbers. Its expectation E[X] is the long-run average and its variance measures spread; know the mean and variance of the Binomial, Poisson, Geometric, Uniform, Exponential and Normal distributions cold.",
       analogy=("🎰", "A game with payouts", "You pay ₹10 to roll a die and win ₹5 × the number shown. The payout is a random variable X. Its expectation E[X] is what you win on average per play in the long run (₹17.50); its variance tells you how wildly individual plays swing around that average."),
       sections=[
           dict(h="Random variables, PMF, PDF, CDF", md="""A **random variable** X is a numerical function of the outcome. **Discrete** X has a probability mass function p(x) = P(X = x) with Σp(x) = 1. **Continuous** X has a density f(x) ≥ 0 with ∫f = 1 and P(a ≤ X ≤ b) = ∫ₐᵇ f; the probability of any single point is 0. The **CDF** F(x) = P(X ≤ x) is non-decreasing from 0 to 1."""),
           dict(h="Expectation and variance", md="""E[X] = Σ x·p(x)  (or ∫ x f(x) dx).  Var(X) = E[X²] − (E[X])².""",
                formulas=[("E[aX + b] = a·E[X] + b", "linearity (always true)"), ("E[X + Y] = E[X] + E[Y]", "even if dependent"), ("Var(aX + b) = a²·Var(X)", "shift doesn't matter, scale squares"), ("Var(X + Y) = Var X + Var Y", "only if X, Y independent")],
                call=[("tip", "Indicator trick", "To find the expected number of fixed points of a random permutation, write the count as a sum of indicators; E = Σ P(i is fixed) = n·(1/n) = 1 — no distribution needed.")]),
           dict(h="Discrete distributions", md="""| Distribution | Models | Mean | Variance |
|---|---|---|---|
| **Bernoulli(p)** | one yes/no trial | p | p(1−p) |
| **Binomial(n, p)** | successes in n trials | **np** | **np(1−p)** |
| **Geometric(p)** | trials until first success | **1/p** | (1−p)/p² |
| **Poisson(λ)** | events in a fixed interval | **λ** | **λ** |
| Uniform on {1..n} | equally likely values | (n+1)/2 | (n²−1)/12 |

P(Binomial = k) = C(n,k)pᵏ(1−p)ⁿ⁻ᵏ; P(Geometric = k) = (1−p)ᵏ⁻¹p; P(Poisson = k) = e^{−λ}λᵏ/k!. Poisson approximates Binomial when n is large and p small (λ = np)."""),
           dict(h="Continuous distributions", md="""| Distribution | Density / key fact | Mean | Variance |
|---|---|---|---|
| **Uniform(a, b)** | constant 1/(b−a) on [a,b] | (a+b)/2 | **(b−a)²/12** |
| **Exponential(λ)** | λe^{−λx}, x ≥ 0; P(X > t) = e^{−λt} | **1/λ** | 1/λ² |
| **Normal(μ, σ²)** | bell curve, symmetric about μ | **μ** | **σ²** |

**Normal 68–95–99.7 rule:** about 68%, 95%, 99.7% of values lie within 1, 2, 3 standard deviations of the mean. Standardise Z = (X − μ)/σ. The exponential is **memoryless**: P(X > s + t | X > s) = P(X > t). Sum of independent normals is normal; sum of independent Poissons is Poisson with added rates."""),
       ],
       examples=[
           Ex("Binomial mean and variance", "X ~ Binomial(n = 10, p = 0.3). Find E[X] and Var(X).",
              ["E[X] = np = 10 × 0.3 = **3**.", "Var(X) = np(1 − p) = 10 × 0.3 × 0.7 = **2.1**."],
              "E[X] = **3**, Var(X) = **2.1**.", verify=lambda: "%g, %.1f" % (10 * 0.3, 10 * 0.3 * 0.7)),
           Ex("Poisson probability", "Calls arrive at a rate of 3 per minute (Poisson). Find P(exactly 2 calls in a minute).",
              ["P(X = 2) = e^{−3}·3² / 2! = 9e^{−3} / 2.", "= 4.5 × 0.049787 = **0.224**."],
              "≈ **0.224**", verify=lambda: "%.3f" % _pois(3, 2)),
           Ex("Expected number of trials", "A fair die is rolled until a six appears. What is the expected number of rolls?",
              ["Geometric with p = 1/6.", "E[X] = 1/p = **6**."],
              "**6**", verify=lambda: str(round(sum(k * (5 / 6) ** (k - 1) * (1 / 6) for k in range(1, 4000))))),
           Ex("Exponential tail", "The lifetime of a component is exponential with rate λ = 0.5 per year. Find P(it survives more than 2 years).",
              ["P(X > t) = e^{−λt} = e^{−0.5×2} = e^{−1}.", "= **0.368**."],
              "≈ **0.368**", verify=lambda: "%.3f" % math.exp(-1)),
           Ex("Variance of a linear combination", "X and Y are independent with Var(X) = 4 and Var(Y) = 9. Find Var(2X − 3Y).",
              ["Var(2X − 3Y) = 2²Var(X) + (−3)²Var(Y) (independence).", "= 4·4 + 9·9 = 16 + 81 = **97**."],
              "**97**", verify=lambda: str(2 ** 2 * 4 + 3 ** 2 * 9)),
       ],
       traps=[("Variance of a sum", "Var(X + Y) = Var X + Var Y **only if independent**. Also Var(X − Y) is the **sum** of variances, not the difference."),
              ("Var(aX + b)", "The constant b disappears and a is **squared**: Var(2X + 5) = 4Var X."),
              ("Geometric conventions", "Mean 1/p counts trials **including** the success; the ‘failures before success’ version has mean (1−p)/p. Read the definition."),
              ("σ vs σ²", "N(μ, σ²) is parameterised by the **variance** in most texts. Check whether a question gives σ or σ².")],
       quick=[("X ~ Poisson(4). Var(X) =", ["2", "4", "16", "1/4"], 1, "Mean = variance = λ."),
              ("Var(3X + 7) when Var(X) = 2:", ["6", "18", "25", "9"], 1, "3²·2 = 18."),
              ("Uniform on [0, 12] has variance", ["6", "12", "24", "144"], 1, "(b − a)²/12 = 144/12 = 12."),
              ("An exponential random variable is", ["memoryless", "symmetric", "discrete", "bounded"], 0, "P(X > s + t | X > s) = P(X > t).")],
       summary=["E[aX+b] = aE[X]+b; E[X+Y] = E[X]+E[Y] always; Var(aX+b) = a²Var X.", "Binomial: np, np(1−p); Poisson: λ, λ; Geometric: 1/p; Exponential: 1/λ; Uniform variance (b−a)²/12.", "Var(X+Y) = Var X + Var Y only when independent.",
                "Normal: 68–95–99.7 rule; standardise Z = (X − μ)/σ.", "Exponential is memoryless; Poisson ≈ Binomial for large n, small p.", "Indicator variables make expectations easy (hat-check: E = 1)."])
