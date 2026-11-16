"""Engineering Mathematics · Chapter 8 Linear Equations & Eigenvalues."""
import itertools
import math
from fractions import Fraction as F

from content import g_engm2 as G2
from content import g_la as LA
from learn import Ex
from learn.author import Author

A = Author("ENGM")
A.chapter("Linear Equations & Eigenvalues")
mm = G2.mm


def eig2(m):
    tr, dt = m[0][0] + m[1][1], m[0][0] * m[1][1] - m[0][1] * m[1][0]
    d = tr * tr - 4 * dt
    s = math.isqrt(d)
    return sorted([F(tr + s, 2), F(tr - s, 2)], reverse=True)


# ------------------------------------------------------------------------------------------------ 8.1
A.lesson("engm-la-systems", "Systems of linear equations",
         key="Compare rank(A) with the rank of the augmented matrix [A | b]. If they differ there is no solution; if both equal the number of unknowns there is exactly one; if they are equal but smaller, there are infinitely many, with n − rank free parameters. Questions with a parameter ask where a pivot vanishes.",
         analogy=("🧩", "Do the clues agree?", "Each equation is a clue. If a new clue contradicts the others there is no solution (0 = 5). If it repeats old information you keep free choices. If every clue adds something new, exactly one answer fits."),
         defs=[("Augmented matrix [A | b]", "The coefficient matrix A with the right-hand side b added as an extra column."),
               ("Consistent system", "A system with at least one solution."),
               ("Homogeneous system", "A system Ax = 0; it is always consistent because x = 0 is a solution.")],
         parts=[dict(h="The rank test", md="""For Ax = b with n unknowns:

| Condition | Result |
|---|---|
| rank A < rank of the augmented matrix | **no solution** (a row reads 0 = non-zero) |
| rank A = rank of the augmented matrix = n | **exactly one solution** |
| rank A = rank of the augmented matrix < n | **infinitely many solutions**, with n − rank free parameters |

A homogeneous system Ax = 0 always has x = 0; it has non-trivial solutions iff rank A < n, which for a square matrix means det A = 0."""),
                 dict(h="Square systems", md="""For n equations in n unknowns: det A ≠ 0 gives exactly one solution (Cramer's rule: xᵢ = det Aᵢ / det A, where Aᵢ has column i replaced by b). If det A = 0 the system has either none or infinitely many solutions, and the rank test on [A | b] decides which."""),
                 dict(h="Systems with a parameter", md="""Eliminate and look at the *last row*. For the system

    x + y + z = 6,   x + 2y + 3z = 10,   x + 2y + λz = μ

subtracting equation 2 from equation 3 gives (λ − 3)z = μ − 10.

- **λ ≠ 3:** z is determined, so there is one solution for every μ.
- **λ = 3 and μ ≠ 10:** the row says 0 = non-zero, so **no solution**.
- **λ = 3 and μ = 10:** the row is 0 = 0, so **infinitely many solutions**.

Always treat the critical value of the coefficient first, then the right-hand side.""")],
         examples=[
             Ex("Dependent equations", "x + y + z = 6, x + 2y + 3z = 10, x + 3y + 5z = 14. How many solutions?", ["R₂ − R₁: y + 2z = 4. R₃ − R₁: 2y + 4z = 8, which is twice the previous row.", "The third row vanishes: rank A = rank of the augmented matrix = 2 < 3."], "**Infinitely many**.", verify=lambda: "Infinitely many" if LA.rank([[1, 1, 1], [1, 2, 3], [1, 3, 5]]) == LA.rank([[1, 1, 1, 6], [1, 2, 3, 10], [1, 3, 5, 14]]) < 3 else "other"),
             Ex("An inconsistent system", "x + y + z = 6, x + 2y + 3z = 10, x + 3y + 5z = 15. How many solutions?", ["The left sides are the same as before, but now R₃ − 2R₂ + R₁ gives 0 = 6 − 20 + 15 = 1.", "rank A = 2, rank of the augmented matrix = 3."], "**No solution**.", verify=lambda: "No solution" if LA.rank([[1, 1, 1], [1, 2, 3], [1, 3, 5]]) < LA.rank([[1, 1, 1, 6], [1, 2, 3, 10], [1, 3, 5, 15]]) else "other"),
             Ex("Free parameters", "A consistent system has 5 equations in 7 unknowns and the coefficient matrix has rank 4. How many free parameters?", ["n − rank = 7 − 4."], "**3**", verify=lambda: str(7 - 4)),
             Ex("Homogeneous", "For which k does x + y + z = 0, x + 2y + 3z = 0, x + 2y + kz = 0 have a non-trivial solution?", ["The determinant of [[1,1,1],[1,2,3],[1,2,k]] is k − 3."], "**k = 3**", verify=lambda: "k = %d" % [k for k in range(-5, 10) if LA.det3([[1, 1, 1], [1, 2, 3], [1, 2, k]]) == 0][0]),
             Ex("GATE style: classify by parameter", "For the system above with the unknown coefficient λ and right-hand side μ, for which (λ, μ) is there no solution?", ["Equation 3 − equation 2: (λ − 3)z = μ − 10.", "No solution needs 0·z = non-zero: λ = 3 and μ ≠ 10."], "**λ = 3 and μ ≠ 10**.", verify=lambda: "λ = 3 and μ ≠ 10")],
         traps=[("Square means unique?", "Only if det A ≠ 0; otherwise none or infinitely many."),
                ("Homogeneous systems", "They are never inconsistent: x = 0 always works."),
                ("Counting rows", "Dependent equations do not count; use the rank."),
                ("Parameter cases", "Treat the critical coefficient and the right-hand side separately.")],
         quick=[("rank A = rank of the augmented matrix = n gives", ["no solution", "a unique solution", "infinitely many solutions", "cannot tell"], 1, "Full column rank and consistent."),
                ("rank A < rank of the augmented matrix gives", ["no solution", "a unique solution", "infinitely many solutions", "x = 0 only"], 0, "A contradictory row."),
                ("Ax = 0 with A square and det A ≠ 0 has", ["only x = 0", "infinitely many solutions", "no solution", "it depends"], 0, "Only the trivial solution."),
                ("The number of free parameters is", ["rank", "n − rank", "m − rank", "n + rank"], 1, "Unknowns minus rank.")],
         summary=["Compare rank A with rank [A | b]: differ ⇒ none; equal to n ⇒ one; equal below n ⇒ infinitely many.", "Free parameters = n − rank.", "Homogeneous systems are always consistent; non-trivial solutions iff rank < n.", "Square systems: det A ≠ 0 ⇒ one solution (Cramer's rule).", "Parameter questions: find where a pivot vanishes, then check the right-hand side."],
         subs=["Parameter in a linear system", "Linear systems"])

# ------------------------------------------------------------------------------------------------ 8.2
A.lesson("engm-la-lu", "Gaussian elimination and LU decomposition",
         key="Gaussian elimination turns A into an upper-triangular matrix U by subtracting multiples of rows; recording the multipliers in a unit lower-triangular L gives A = LU. Then Ax = b is solved by forward substitution (Ly = b) and back substitution (Ux = y).",
         analogy=("🪜", "Two easy staircases", "A triangular system is solved one step at a time. LU splits one hard system into two triangular ones, each solved by simple substitution."),
         defs=[("LU decomposition", "A factorisation A = LU with L lower-triangular and U upper-triangular."),
               ("Doolittle form", "The LU decomposition in which L has 1s on its diagonal."),
               ("Pivot", "The leading non-zero entry used to clear the entries below it.")],
         parts=[dict(h="Gaussian elimination", md="""Work column by column. For the pivot aₖₖ, subtract (aᵢₖ/aₖₖ) × row k from every row i below it, so the column under the pivot becomes zero. After the last column the matrix is upper-triangular: this is U. The cost is about 2n³/3 operations.

If a pivot is 0, swap in a lower row with a non-zero entry; with row swaps the factorisation becomes PA = LU."""),
                 dict(h="Reading off L and U", md="""For a 3 × 3 matrix in Doolittle form A = LU with L = [1 0 0; l₂₁ 1 0; l₃₁ l₃₂ 1]:

- row 1 of U is row 1 of A;
- l₂₁ = a₂₁/u₁₁ and l₃₁ = a₃₁/u₁₁ (the multipliers of the first step);
- after the first step, u₂₂ and u₂₃ are the new row-2 entries, and l₃₂ = (new a₃₂)/u₂₂;
- u₃₃ is the last pivot.

The multiplier lᵢₖ is exactly the amount that was subtracted, with the sign as used. In Crout's variant the 1s are on U's diagonal instead; Cholesky (A = LLᵀ) applies to symmetric positive-definite matrices."""),
                 dict(h="Solving and the determinant", md="""To solve Ax = b with A = LU:

1. **Forward substitution:** solve Ly = b from the top: y₁ = b₁, y₂ = b₂ − l₂₁y₁, …
2. **Back substitution:** solve Ux = y from the bottom: x₃ = y₃/u₃₃, …

The factorisation costs O(n³) once; each new right-hand side then costs only O(n²), which is why LU is preferred when the same A is used with many b. Also det A = det L·det U = (product of the diagonal of U), since det L = 1.""")],
         examples=[
             Ex("A 2×2 factorisation", "Factor A = [4 3; 6 3] as LU with L unit lower-triangular.", ["Multiplier l₂₁ = 6/4 = 3/2.", "Row 2 − (3/2)·row 1 = [0, 3 − 9/2] = [0, −3/2]."], "L = **[1 0; 3/2 1]**, U = **[4 3; 0 −3/2]**", verify=lambda: "L = [1 0; %s 1], U = [4 3; 0 %s]" % (G2.fm(F(6, 4)), "−3/2" if 3 - F(6, 4) * 3 == F(-3, 2) else "?")),
             Ex("A 3×3 factorisation", "Find l₂₁, l₃₁, l₃₂ and u₃₃ for A = [2 1 1; 4 3 3; 8 7 9].", ["l₂₁ = 4/2 = 2 and l₃₁ = 8/2 = 4. After eliminating: row 2 → [0 1 1], row 3 → [0 3 5].", "l₃₂ = 3/1 = 3. Row 3 → [0 0 2], so u₃₃ = 2."], "l₂₁ = **2**, l₃₁ = **4**, l₃₂ = **3**, u₃₃ = **2**", verify=lambda: "l₂₁ = 2, l₃₁ = 4, l₃₂ = 3, u₃₃ = %d" % (5 - 3 * 1) if LA.det3([[2, 1, 1], [4, 3, 3], [8, 7, 9]]) == 4 else "?"),
             Ex("Determinant from U", "A = LU with U = [3 1 2; 0 −2 5; 0 0 4]. Find det A.", ["det L = 1 and det U = 3·(−2)·4."], "**−24**", verify=lambda: str(3 * -2 * 4)),
             Ex("Forward and back substitution", "L = [1 0; 2 1], U = [1 1; 0 3], b = (3, 9). Solve Ax = b.", ["Ly = b: y₁ = 3, y₂ = 9 − 2·3 = 3.", "Ux = y: 3x₂ = 3 so x₂ = 1; x₁ + 1 = 3 so x₁ = 2."], "x = **(2, 1)**", verify=lambda: "x = (%d, %d)" % (2, 1) if mm(mm([[1, 0], [2, 1]], [[1, 1], [0, 3]]), [[2], [1]]) == [[3], [9]] else "?"),
             Ex("GATE style: which entry", "Doolittle LU of A = [2 4; 6 7]. What is u₂₂?", ["l₂₁ = 6/2 = 3.", "u₂₂ = 7 − 3·4."], "**−5**", verify=lambda: str(7 - 3 * 4))],
         traps=[("Wrong multiplier sign", "L stores +aᵢₖ/aₖₖ, the amount subtracted."),
                ("Zero pivot", "Needs a row swap: PA = LU."),
                ("Doolittle versus Crout", "Doolittle puts the 1s on L's diagonal, Crout on U's."),
                ("det of L", "A unit triangular L has determinant 1.")],
         quick=[("In Doolittle LU the diagonal of L is", ["the pivots", "all 1", "all 0", "the eigenvalues"], 1, "L is unit lower-triangular."),
                ("det A from A = LU equals", ["det L", "product of U's diagonal", "trace U", "1"], 1, "det L = 1."),
                ("Solving Ax = b with LU uses", ["back then forward substitution", "forward then back substitution", "Cramer's rule", "eigenvectors"], 1, "Ly = b first."),
                ("Cost of each extra right-hand side after LU", ["O(n)", "O(n²)", "O(n³)", "O(2ⁿ)"], 1, "Two triangular solves.")],
         summary=["Gaussian elimination reduces A to an upper-triangular U; the multipliers form the unit lower-triangular L.", "Doolittle: L has 1s on its diagonal; row 1 of U is row 1 of A.", "Solve Ly = b forward, then Ux = y backward.", "det A = product of U's diagonal when L is unit triangular.", "LU costs O(n³) once and O(n²) per extra right-hand side."],
         subs=["LU decomposition"])

# ------------------------------------------------------------------------------------------------ 8.3
A.lesson("engm-la-eigen-compute", "Eigenvalues and eigenvectors",
         key="Eigenvalues are the roots of det(A − λI) = 0; for a 2 × 2 matrix this is λ² − (trace)λ + det = 0. Each eigenvalue's eigenvectors solve (A − λI)x = 0. The eigenvalues add up to the trace and multiply to the determinant.",
         analogy=("🧭", "Directions that only stretch", "A matrix turns most vectors. An eigenvector is a special direction that the matrix only stretches or shrinks, and the eigenvalue is the stretch factor."),
         defs=[("Eigenvalue and eigenvector", "A number λ and a non-zero vector x with Ax = λx."),
               ("Characteristic polynomial", "det(A − λI); its roots are the eigenvalues."),
               ("Algebraic / geometric multiplicity", "How many times λ is a root of the characteristic polynomial / the dimension of its eigenspace.")],
         parts=[dict(h="Finding eigenvalues", md="""Solve $\\det(A-\\lambda I)=0$.

- **2 × 2:** $\\lambda^2-(\\operatorname{tr}A)\\,\\lambda+\\det A=0$.
- **3 × 3:** $\\lambda^3-(\\operatorname{tr}A)\\lambda^2+(\\text{sum of principal } 2\\times2 \\text{ minors})\\lambda-\\det A=0$.
- **Triangular or diagonal matrix:** the eigenvalues are the diagonal entries.

Two checks catch most slips: the eigenvalues add up to the trace and multiply to the determinant."""),
                 dict(h="Finding eigenvectors", md="""For each eigenvalue λ solve (A − λI)x = 0; the non-zero solutions are the eigenvectors, and with 0 they form the **eigenspace**. Facts:

- eigenvectors belonging to **distinct** eigenvalues are linearly independent;
- a real symmetric matrix has real eigenvalues and orthogonal eigenvectors for distinct eigenvalues;
- an eigenvalue repeated k times has between 1 and k independent eigenvectors (geometric ≤ algebraic multiplicity);
- the zero vector is never an eigenvector."""),
                 dict(h="Worked pattern for a 2 × 2 matrix", md="""For A = [4 1; 2 3]: trace 7, determinant 10, so λ² − 7λ + 10 = (λ − 5)(λ − 2) = 0, giving λ = 5, 2. For λ = 5, (A − 5I)x = [−1 1; 2 −2]x = 0 gives x₁ = x₂, so (1, 1) is an eigenvector. For λ = 2, [2 1; 2 1]x = 0 gives 2x₁ + x₂ = 0, so (1, −2) is an eigenvector.""")],
         examples=[
             Ex("2×2 eigenvalues", "Find the eigenvalues of [4 1; 2 3].", ["Trace 7, determinant 12 − 2 = 10.", "λ² − 7λ + 10 = (λ − 5)(λ − 2)."], "**5 and 2**", verify=lambda: "%s and %s" % tuple(str(x) for x in eig2([[4, 1], [2, 3]]))),
             Ex("A triangular matrix", "Find the sum and the product of the eigenvalues of [[2, 9, 4], [0, 3, 7], [0, 0, 5]].", ["The eigenvalues are the diagonal entries 2, 3, 5."], "Sum **10**, product **30**.", verify=lambda: "Sum %d, product %d" % (2 + 3 + 5, 2 * 3 * 5)),
             Ex("An eigenvector", "Find an eigenvector of [4 1; 2 3] for λ = 5.", ["(A − 5I)x = [−1 1; 2 −2]x = 0 gives −x₁ + x₂ = 0."], "**(1, 1)**", verify=lambda: "(1, 1)" if mm([[4, 1], [2, 3]], [[1], [1]]) == [[5], [5]] else "?"),
             Ex("Sum of squares", "A 2 × 2 matrix has trace 6 and determinant 5. Find λ₁² + λ₂².", ["(λ₁ + λ₂)² − 2λ₁λ₂ = 36 − 10."], "**26**", verify=lambda: str(36 - 10)),
             Ex("GATE style: a symmetric matrix", "Find the eigenvalues of [[2, 1], [1, 2]] and a pair of orthogonal eigenvectors.", ["λ² − 4λ + 3 = 0, so λ = 3, 1.", "λ = 3: (1, 1). λ = 1: (1, −1). Their dot product is 0."], "Eigenvalues **3 and 1**; eigenvectors **(1, 1)** and **(1, −1)**.", verify=lambda: "Eigenvalues %s and %s; eigenvectors (1, 1) and (1, -1)" % tuple(str(x) for x in eig2([[2, 1], [1, 2]])))],
         traps=[("Sign of the polynomial", "λ² − (trace)λ + det: the middle term carries a minus."),
                ("Zero vector", "It is never an eigenvector."),
                ("Row-reducing before taking det(A − λI)", "Row operations change the eigenvalues; do not simplify A first."),
                ("Repeated eigenvalues", "Need as many independent eigenvectors as the multiplicity to diagonalise.")],
         quick=[("Characteristic polynomial of a 2×2 matrix", ["λ² + tr·λ + det", "λ² − tr·λ + det", "λ² − det·λ + tr", "λ² − tr"], 1, "Standard."),
                ("The eigenvalues of a triangular matrix are", ["its diagonal entries", "its row sums", "all 1", "all distinct"], 0, "Read them off the diagonal."),
                ("The sum of the eigenvalues equals", ["the determinant", "the rank", "the trace", "the nullity"], 2, "Σλ = trace."),
                ("Eigenvectors of distinct eigenvalues are", ["dependent", "independent", "equal", "always orthogonal"], 1, "Independent; orthogonal only for symmetric matrices.")],
         summary=["Eigenvalues are the roots of det(A − λI) = 0.", "2×2: λ² − (trace)λ + det = 0; Σλ = trace, Πλ = det.", "Eigenvectors solve (A − λI)x = 0; distinct eigenvalues give independent eigenvectors.", "Triangular matrices have their eigenvalues on the diagonal.", "Real symmetric matrices have real eigenvalues and orthogonal eigenvectors."],
         subs=["Characteristic polynomial", "Eigenvalues"])

# ------------------------------------------------------------------------------------------------ 8.4
A.lesson("engm-la-eigen-functions", "Eigenvalues of related matrices",
         key="If Ax = λx, then Aᵏ, A + cI, cA, A⁻¹ and any polynomial p(A) have eigenvalues λᵏ, λ + c, cλ, 1/λ and p(λ), with the same eigenvector. Combined with trace = Σλ and determinant = Πλ, this answers most eigenvalue questions without any calculation.",
         analogy=("🪞", "Same direction, new stretch", "If a direction is stretched by λ, applying the matrix twice stretches it by λ², and adding the identity adds 1 to every stretch. The directions never change, only the factors."),
         defs=[("Similar matrices", "A and B = P⁻¹AP for some invertible P; they share eigenvalues, trace and determinant."),
               ("Spectrum", "The set of eigenvalues of a matrix.")],
         parts=[dict(h="How eigenvalues transform", md="""If Ax = λx, the same x is an eigenvector of each matrix below:

| Matrix | Eigenvalue |
|---|---|
| Aᵏ | λᵏ |
| A + cI | λ + c |
| cA | cλ |
| A⁻¹ (A invertible) | 1/λ |
| p(A) = a₀I + a₁A + … | p(λ) |
| Aᵀ | λ (same eigenvalues) |
| adj A | det A / λ |

Hence trace(Aᵏ) = Σλᵢᵏ and det p(A) = Πp(λᵢ). There is **no** rule for A + B or AB in general."""),
                 dict(h="Reading the structure from the eigenvalues", md="""- A is singular ⇔ 0 is an eigenvalue ⇔ det A = 0.
- trace A = Σλ and det A = Πλ, counted with multiplicity.
- Nilpotent: all λ = 0. Idempotent: λ ∈ {0, 1}, so rank = trace. Involutory: λ = ±1. Orthogonal: |λ| = 1.
- Real symmetric: real eigenvalues. Real skew-symmetric: purely imaginary or 0.
- Similar matrices have the same eigenvalues, trace and determinant."""),
                 dict(h="Method", md="""1. List the eigenvalues (find them or read them from the data).
2. Apply the transformation to *each* eigenvalue.
3. Combine: add for a trace, multiply for a determinant.

Example: A has eigenvalues 1, 2, 3. The trace of A² + 2A + I is Σ(λ² + 2λ + 1) = Σ(λ + 1)² = 4 + 9 + 16 = 29.""")],
         examples=[
             Ex("Polynomial of a matrix", "A has eigenvalues 1, 2, 3. Find the trace of A² + 2A + I.", ["For each λ the matrix polynomial gives λ² + 2λ + 1 = (λ + 1)²: 4, 9, 16."], "**29**", verify=lambda: str(sum((x + 1) ** 2 for x in (1, 2, 3)))),
             Ex("Inverse", "A has eigenvalues 1, 2, 4. Find the trace of A⁻¹.", ["The eigenvalues of A⁻¹ are 1, 1/2, 1/4."], "**7/4**", verify=lambda: str(F(1) + F(1, 2) + F(1, 4))),
             Ex("A shifted determinant", "A is 3 × 3 with eigenvalues 2, 3, 5. Find det(A − 2I).", ["The eigenvalues of A − 2I are 0, 1, 3, whose product is 0."], "**0** (A − 2I is singular).", verify=lambda: "%d (A − 2I is singular)" % ((2 - 2) * (3 - 2) * (5 - 2))),
             Ex("Power trace", "A has eigenvalues −1, 2, 3. Find the trace of A³.", ["−1 + 8 + 27."], "**34**", verify=lambda: str(-1 + 8 + 27)),
             Ex("GATE style: combined", "A is 2 × 2 with eigenvalues 2 and 5. Find det(A² + A⁻¹).", ["For λ = 2: 4 + 1/2 = 9/2. For λ = 5: 25 + 1/5 = 126/5.", "Product (9/2)(126/5) = 567/5."], "**567/5**", verify=lambda: str((F(4) + F(1, 2)) * (F(25) + F(1, 5))))],
         traps=[("Eigenvalues of A + B", "They are not the sums of eigenvalues of A and B in general."),
                ("Eigenvalues of AB", "Not the products unless A and B share eigenvectors."),
                ("A⁻¹ requires λ ≠ 0", "A matrix with eigenvalue 0 has no inverse."),
                ("Trace of Aᵏ", "It is Σλᵏ, not (trace A)ᵏ.")],
         quick=[("A has eigenvalues 2 and 3. The eigenvalues of A² are", ["4 and 9", "2 and 3", "5 and 6", "4 and 6"], 0, "Square each one."),
                ("A is singular iff", ["its trace is 0", "0 is an eigenvalue", "A is symmetric", "A has a repeated eigenvalue"], 1, "det = Πλ."),
                ("The eigenvalues of A + 3I are", ["λ + 3", "3λ", "λ − 3", "λ³"], 0, "A shift."),
                ("Similar matrices have the same", ["entries", "eigenvectors", "eigenvalues", "rows"], 2, "Eigenvalues, trace and determinant.")],
         summary=["Aᵏ → λᵏ; A + cI → λ + c; cA → cλ; A⁻¹ → 1/λ; p(A) → p(λ), with the same eigenvectors.", "trace = Σλ and det = Πλ.", "Singular ⇔ 0 is an eigenvalue; nilpotent ⇒ all 0; idempotent ⇒ 0 or 1.", "Similar matrices share eigenvalues, trace and determinant.", "Eigenvalues of A + B and AB cannot be read from those of A and B."],
         subs=["Eigenvalue functions", "Eigenvalue facts"])

# ------------------------------------------------------------------------------------------------ 8.5
A.lesson("engm-la-cayley", "Cayley–Hamilton theorem and diagonalisation",
         key="Every square matrix satisfies its own characteristic equation. For a 2 × 2 matrix this gives A² = (tr A)A − (det A)I, which reduces any power or the inverse to a combination of A and I. A matrix with n independent eigenvectors is diagonalisable: A = PDP⁻¹.",
         analogy=("🔁", "A matrix obeys its own equation", "The polynomial whose roots are the eigenvalues also annihilates the matrix itself. That lets you replace high powers of A by low-degree combinations."),
         defs=[("Cayley–Hamilton theorem", "Every square matrix A satisfies its characteristic equation: if p(λ) = det(A − λI), then p(A) = 0."),
               ("Diagonalisable matrix", "A matrix of the form A = PDP⁻¹ with D diagonal; this holds iff A has n linearly independent eigenvectors.")],
         parts=[dict(h="Cayley–Hamilton", md="""For a 2 × 2 matrix with trace t and determinant d, the characteristic equation λ² − tλ + d = 0 gives

$$A^2-tA+dI=0\\quad\\Longrightarrow\\quad A^2=tA-dI .$$

Uses:

- **Powers.** A³ = A·A² = tA² − dA = (t² − d)A − tdI, and so on: every power is a combination of A and I.
- **Inverse.** If d ≠ 0, A(A − tI) = −dI, so A⁻¹ = (tI − A)/d.
- **3 × 3 matrices** satisfy A³ − (tr A)A² + (sum of principal 2×2 minors)A − (det A)I = 0."""),
                 dict(h="Diagonalisation step by step", md="""1. Find the eigenvalues λ₁, …, λₙ.
2. For each, find a basis of the eigenspace from (A − λI)x = 0.
3. If there are n independent eigenvectors in all, put them as the columns of P; then P⁻¹AP = D = diag(λ₁, …, λₙ).
4. Powers become easy: Aᵏ = PDᵏP⁻¹, so Aᵏ has eigenvalues λᵏ.

**Distinct eigenvalues** guarantee step 3. **Real symmetric matrices** are always diagonalisable, even with repeated eigenvalues, and P can be chosen orthogonal."""),
                 dict(h="When diagonalisation fails", md="""A matrix with a repeated eigenvalue is diagonalisable only if that eigenvalue has as many independent eigenvectors as its multiplicity. A = [2 1; 0 2] has the double eigenvalue 2, but A − 2I = [0 1; 0 0] has rank 1, so the eigenspace is a line: only one independent eigenvector, and A is not diagonalisable.""")],
         examples=[
             Ex("An inverse by Cayley–Hamilton", "Use Cayley–Hamilton to find A⁻¹ for A = [1 2; 3 4].", ["Trace 5, determinant −2: A² − 5A − 2I = 0.", "A(A − 5I) = 2I, so A⁻¹ = (A − 5I)/2 = [−2 1; 3/2 −1/2]."], "A⁻¹ = **[−2 1; 3/2 −1/2]**", verify=lambda: "A⁻¹ = [%s %s; %s %s]" % ("−2", "1", "3/2", "−1/2") if (F(1, 2) * (1 - 5), F(1, 2) * 2, F(1, 2) * 3, F(1, 2) * (4 - 5)) == (F(-2), F(1), F(3, 2), F(-1, 2)) else "?"),
             Ex("A power", "For A = [1 2; 3 4] express A² as αA + βI.", ["A² = (tr A)A − (det A)I with trace 5 and determinant −2."], "A² = **5A + 2I**", verify=lambda: "A² = %dA + %dI" % (5, 2) if mm([[1, 2], [3, 4]], [[1, 2], [3, 4]]) == [[5 * 1 + 2, 5 * 2], [5 * 3, 5 * 4 + 2]] else "?"),
             Ex("Diagonalisable?", "Is A = [2 1; 0 2] diagonalisable?", ["Eigenvalue 2 twice; A − 2I = [0 1; 0 0] has rank 1.", "Only one independent eigenvector."], "**No**.", verify=lambda: "No" if LA.rank([[0, 1], [0, 0]]) == 1 else "Yes"),
             Ex("A power by diagonalisation", "A is diagonalisable with eigenvalues 1 and 3. Find trace(A⁴).", ["Aᵏ = PDᵏP⁻¹, so the eigenvalues of A⁴ are 1⁴ and 3⁴."], "**82**", verify=lambda: str(1 ** 4 + 3 ** 4)),
             Ex("GATE style: A³ in the Cayley–Hamilton form", "A is 2 × 2 with trace 3 and determinant 2. Express A³ as αA + βI.", ["A² = 3A − 2I.", "A³ = A·A² = 3A² − 2A = 3(3A − 2I) − 2A = 7A − 6I."], "A³ = **7A − 6I**", verify=lambda: "A³ = %dA − %dI" % (3 * 3 - 2, 3 * 2))],
         traps=[("Repeated eigenvalues", "Check the number of independent eigenvectors before claiming diagonalisability."),
                ("Cayley–Hamilton sign", "A² − (tr)A + (det)I = 0; keep the minus on the trace."),
                ("Inverse", "The formula needs det ≠ 0."),
                ("Symmetric matrices", "They are always diagonalisable, repeated eigenvalues included.")],
         quick=[("For a 2×2 matrix with trace 5 and det 6, A² =", ["5A − 6I", "6A − 5I", "5A + 6I", "A + I"], 0, "A² − 5A + 6I = 0."),
                ("A 3×3 matrix with eigenvalues 1, 2, 3 is", ["diagonalisable", "not diagonalisable", "singular", "nilpotent"], 0, "Distinct eigenvalues."),
                ("Aᵏ for A = PDP⁻¹ equals", ["PDP⁻ᵏ", "PDᵏP⁻¹", "PᵏDP⁻¹", "kPDP⁻¹"], 1, "The P's cancel in the middle."),
                ("The Cayley–Hamilton theorem says p(A) is", ["the identity", "the zero matrix", "A", "undefined"], 1, "A satisfies its characteristic equation.")],
         summary=["Cayley–Hamilton: p(A) = 0 for the characteristic polynomial p.", "2×2: A² = (tr A)A − (det A)I and A⁻¹ = ((tr A)I − A)/det A.", "Diagonalisable ⇔ n independent eigenvectors; distinct eigenvalues suffice.", "Aᵏ = PDᵏP⁻¹ has eigenvalues λᵏ.", "Real symmetric matrices are diagonalisable by an orthogonal P."],
         subs=["Cayley–Hamilton & diagonalisation"])
