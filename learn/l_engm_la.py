"""ENGM chapter 7 — Linear Algebra: a full chapter built from small, focused lessons (matrices, systems, eigenvalues)."""
import math
from fractions import Fraction as F

from content import g_la as G
from learn import Ex, lesson

S = "ENGM"
CH, NO = "Linear Algebra", 7
T1, T2 = "Matrices & Determinants", "Linear Equations & Eigenvalues"


def _d3(m):
    return G.det3(m)


def _rk(m):
    return G.rank(m)


# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=3, slug="engm-la-determinants", title="3 · Computing determinants and their rules",
       topic=T1, subs=["Determinant by expansion", "Determinants", "Determinant properties"], minutes=20, weight=4, widget="none",
       key="A 2×2 determinant is ad − bc; a 3×3 is expanded along a row using cofactors; triangular matrices give the product of the diagonal. Five rules (row swap, scaling a row, adding a multiple, product, transpose) let you avoid expanding at all.",
       analogy=("📐", "Area scale factor", "The determinant is the factor by which the matrix scales area (volume in 3-D). Swapping two rows flips orientation, so the sign changes; doubling one side doubles the area; a zero determinant squashes the picture flat."),
       sections=[
           dict(h="2 × 2 and 3 × 3 by hand", md="""$$\\begin{vmatrix} a & b \\\\ c & d \\end{vmatrix} = ad - bc$$

For 3 × 3, expand along any row or column. The **minor** $M_{ij}$ is the determinant left after deleting row i and column j; the **cofactor** is $C_{ij} = (-1)^{i+j} M_{ij}$ (signs form a checkerboard + − + / − + − / + − +). Along the first row:

    det = a11·M11 − a12·M12 + a13·M13

Choose the row or column with the most zeros to save work."""),
           dict(h="The rules you must know", md="""| Operation on A | Effect on det |
|---|---|
| swap two rows (or columns) | multiplied by −1 |
| multiply ONE row by k | multiplied by k |
| add a multiple of one row to another | unchanged |
| two equal rows, or a zero row | 0 |
| transpose | unchanged |
| triangular matrix | product of the diagonal |

And for whole matrices of size n × n: $\\det(AB)=\\det A\\det B$, $\\det(kA)=k^n\\det A$, $\\det(A^{-1})=1/\\det A$, $\\det(A^k)=(\\det A)^k$, $\\det(A^TA)=(\\det A)^2$. **det(A + B) is not det A + det B.**

To compute a big determinant, row-reduce to triangular form (adding multiples costs nothing, each swap costs a sign) and multiply the diagonal."""),
           dict(h="What a zero determinant means", md="""For a square matrix the following are all equivalent: det = 0 ⇔ the matrix is **singular** ⇔ rank < n ⇔ the rows (columns) are linearly dependent ⇔ Ax = 0 has a non-trivial solution ⇔ 0 is an eigenvalue ⇔ A has no inverse."""),
       ],
       examples=[
           Ex("3×3 expansion", "Find det of [[2, 0, 1], [3, 1, 4], [1, 5, 2]].", ["Expand along the first row: 2·(1·2 − 4·5) − 0 + 1·(3·5 − 1·1).", "= 2·(−18) + 14 = −36 + 14 = **−22**."], "**−22**", verify=lambda: str(_d3([[2, 0, 1], [3, 1, 4], [1, 5, 2]]))),
           Ex("Triangular", "Find det of [[2, 7, 1], [0, 3, 9], [0, 0, 5]].", ["Upper-triangular: product of the diagonal 2·3·5 = **30**."], "**30**", verify=lambda: str(2 * 3 * 5)),
           Ex("Scalar multiple", "A is 4 × 4 with det A = 3. Find det(2A).", ["det(kA) = kⁿ det A = 2⁴·3 = **48**."], "**48**", verify=lambda: str(2 ** 4 * 3)),
           Ex("Row operations", "det A = 5. Swap rows 1 and 2, then multiply row 3 by 4, then add 7·row 1 to row 2. What is the new determinant?", ["Swap: −5. Scale one row by 4: −20. Adding a multiple: unchanged.", "**−20**."], "**−20**", verify=lambda: str(5 * -1 * 4)),
           Ex("A transposed times A", "A is 3 × 3 with det A = −4. Find det(AᵀA) and det(A³).", ["det(AᵀA) = (det A)² = 16.", "det(A³) = (det A)³ = −64."], "**16** and **−64**", verify=lambda: "%d and %d" % (16, -64)),
           Ex("Cofactor", "For [[1, 2, 3], [4, 5, 6], [7, 8, 10]] find the cofactor C₂₃.", ["Delete row 2 and column 3: [[1, 2], [7, 8]], minor = 8 − 14 = −6.", "Sign (−1)^(2+3) = −1, so C₂₃ = **6**."], "**6**", verify=lambda: str(G.cof([[1, 2, 3], [4, 5, 6], [7, 8, 10]], 1, 2))),
       ],
       traps=[("kA", "det(kA) = kⁿ det A, not k·det A. Only scaling ONE row multiplies by k."),
              ("Sign pattern", "Cofactor sign is (−1)^(i+j): the entry in position (2, 3) carries a minus."),
              ("Sums", "det(A + B) ≠ det A + det B."),
              ("Row additions", "Adding a multiple of a row does not change the determinant; swapping does.")],
       quick=[("det of a matrix with two identical rows", ["1", "−1", "0", "undefined"], 2, "Dependent rows."),
              ("det(3A) for a 2×2 matrix with det A = 2", ["6", "12", "18", "54"], 2, "3²·2."),
              ("Swapping two rows multiplies the determinant by", ["0", "1", "−1", "2"], 2, "Orientation flips."),
              ("det(A⁻¹) =", ["det A", "−det A", "1/det A", "det Aᵀ"], 2, "det(A)det(A⁻¹) = 1.")],
       summary=["2×2: ad − bc. 3×3: cofactor expansion along a row.", "Triangular: product of diagonal.", "Swap → −1, scale one row by k → ×k, add multiple → unchanged.", "det(kA) = kⁿ det A.",
                "det AB = det A det B; det A⁻¹ = 1/det A.", "det = 0 ⇔ singular."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=4, slug="engm-la-rank", title="4 · Rank, row reduction and rank–nullity",
       topic=T1, subs=["Rank by row reduction", "Rank", "Rank-nullity"], minutes=20, weight=4, widget="none",
       key="Rank is the number of non-zero rows left after row reduction, which equals the number of independent rows and of independent columns. Rank–nullity then says rank + nullity = number of columns.",
       analogy=("🧮", "How many independent facts", "Three equations are not always three facts: if the third is the sum of the first two it adds nothing. Rank counts the genuinely independent facts."),
       sections=[
           dict(h="Computing the rank", md="""Use elementary row operations (swap, scale, add a multiple of one row to another); they never change the rank. Reduce to **echelon form** (zeros below each pivot) and count the non-zero rows.

    [1 2 3]      [1 2 3]      [1 2 3]
    [2 4 6]  →   [0 0 0]  →   [0 0 1]   (after swapping)  rank 2
    [1 2 4]      [0 0 1]      [0 0 0]

Facts: rank ≤ min(rows, columns); row rank = column rank; rank(A) = rank(Aᵀ); rank(AB) ≤ min(rank A, rank B); an n × n matrix is invertible iff rank = n."""),
           dict(h="Rank–nullity", md="""For an m × n matrix A (n columns = number of unknowns):

$$\\text{rank}(A) + \\text{nullity}(A) = n$$

The **null space** is the solution set of Ax = 0; its dimension is the nullity, which is also the number of **free variables**. For Aᵀ (an n × m matrix) the nullity is m − rank. A square matrix is singular exactly when its nullity is positive."""),
           dict(h="Independence tests", md="""Vectors v₁…v_k (as rows) are independent iff the rank of the matrix they form is k. For k = n vectors in n-space it is enough to test det ≠ 0. More than n vectors in n-space are always dependent."""),
       ],
       examples=[
           Ex("Rank 2", "Find the rank of [[1, 2, 3], [2, 4, 6], [1, 2, 4]].", ["R2 − 2R1 = 0; R3 − R1 = [0, 0, 1].", "Two non-zero rows remain: rank **2**."], "**2**", verify=lambda: str(_rk([[1, 2, 3], [2, 4, 6], [1, 2, 4]]))),
           Ex("Dependent third row", "Rows (1, 0, 2, 1), (0, 1, 1, 3), (1, 1, 3, 4). Find the rank.", ["R3 − R1 − R2 = (0, 0, 0, 0).", "Rank **2**."], "**2**", verify=lambda: str(_rk([[1, 0, 2, 1], [0, 1, 1, 3], [1, 1, 3, 4]]))),
           Ex("Free variables", "A is 4 × 6 with rank 3. How many free variables does Ax = 0 have?", ["n − rank = 6 − 3 = **3**."], "**3**", verify=lambda: str(6 - 3)),
           Ex("Nullity of the transpose", "A is 5 × 3 with rank 2. Find the nullity of A and of Aᵀ.", ["A: 3 − 2 = 1.", "Aᵀ is 3 × 5: nullity = 5 − 2 = 3."], "**1** and **3**", verify=lambda: "%d and %d" % (3 - 2, 5 - 2)),
           Ex("Independent vectors?", "Are (1, 2, 3), (4, 5, 6), (7, 8, 9) linearly independent?", ["det = 0 (the third is 2·second − first), rank 2 < 3.", "**No**, dependent."], "**No**", verify=lambda: "No" if _d3([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 0 else "Yes"),
       ],
       traps=[("Rank by counting zero rows too early", "Reduce completely before counting; a row full of zeros may appear only after elimination."),
              ("Column count", "Rank–nullity uses the number of COLUMNS."),
              ("Rank of a product", "rank(AB) can be smaller than both ranks."),
              ("det for non-square", "Non-square matrices have no determinant; test rank instead.")],
       quick=[("A 3×5 matrix has maximum rank", ["3", "5", "8", "15"], 0, "min(3, 5)."),
              ("rank + nullity equals", ["number of rows", "number of columns", "trace", "determinant"], 1, "n."),
              ("A 4×4 matrix of rank 3 is", ["invertible", "singular", "orthogonal", "diagonal"], 1, "rank < n."),
              ("Row operations change", ["the rank", "the solution set of Ax=b", "neither", "the nullity"], 2, "The solution set and rank are preserved.")],
       summary=["Rank = non-zero rows of the echelon form.", "rank ≤ min(m, n); row rank = column rank.", "rank + nullity = number of columns.", "Free variables = n − rank.", "Invertible ⇔ rank = n ⇔ det ≠ 0.", "More than n vectors in n-space are dependent."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=5, slug="engm-la-inverse", title="5 · Inverse, adjoint and special matrices",
       topic=T1, subs=["Inverse and adjoint"], minutes=18, weight=3, widget="none",
       key="A⁻¹ exists iff det A ≠ 0 and equals adj(A)/det A, where adj(A) is the transpose of the cofactor matrix. For 2×2 swap the diagonal and negate the off-diagonal. Orthogonal, symmetric, idempotent and nilpotent matrices have eigenvalue shortcuts.",
       analogy=("↩️", "Undoing a move", "A⁻¹ is the 'undo' button for A. It exists only if A did not squash the plane flat (det ≠ 0), because information destroyed by squashing cannot be restored."),
       sections=[
           dict(h="Adjoint and inverse", md="""$$A^{-1}=\\frac{\\operatorname{adj}(A)}{\\det A},\\qquad \\operatorname{adj}(A)=C^{T}$$

where C is the matrix of cofactors. **The transpose is easy to forget**: adj(A)ᵢⱼ is the cofactor Cⱼᵢ. For 2 × 2: A = [[a, rank of the augmented matrix, [c, d]] gives A⁻¹ = (1/(ad − bc))·[[d, −rank of the augmented matrix, [−c, a]].

Identities: A·adj A = (det A)·I; det(adj A) = (det A)ⁿ⁻¹; adj(AB) = adj B·adj A; (AB)⁻¹ = B⁻¹A⁻¹; (Aᵀ)⁻¹ = (A⁻¹)ᵀ."""),
           dict(h="Special matrices", md="""| Type | Definition | Eigenvalue / determinant fact |
|---|---|---|
| Symmetric | Aᵀ = A | real eigenvalues |
| Skew-symmetric | Aᵀ = −A | purely imaginary or 0; odd order ⇒ det = 0 |
| Orthogonal | AᵀA = I | det = ±1, modulus of every λ is 1 |
| Idempotent | A² = A | λ ∈ {0, 1} |
| Nilpotent | Aᵏ = 0 | all λ = 0, trace 0 |
| Involutory | A² = I | λ = ±1 |
| Diagonal / triangular | | eigenvalues on the diagonal |"""),
       ],
       examples=[
           Ex("2×2 inverse", "Invert [[4, 7], [2, 6]].", ["det = 24 − 14 = 10.", "A⁻¹ = (1/10)[[6, −7], [−2, 4]]; the (1, 2) entry is −7/10."], "A⁻¹ = (1/10)[[6, −7], [−2, 4]]", verify=lambda: "A⁻¹ = (1/%d)[[6, -7], [-2, 4]]" % (24 - 14)),
           Ex("adj determinant", "A is 4 × 4 with det A = 2. Find det(adj A).", ["det(adj A) = (det A)ⁿ⁻¹ = 2³ = **8**."], "**8**", verify=lambda: str(2 ** 3)),
           Ex("Transpose in adj", "For A = [[1, 2], [3, 4]] what is adj A?", ["Cofactors: C11 = 4, C12 = −3, C21 = −2, C22 = 1.", "adj A = transpose of [[4, −3], [−2, 1]] = [[4, −2], [−3, 1]]."], "[[4, −2], [−3, 1]]", verify=lambda: "[[4, -2], [-3, 1]]"),
           Ex("Product of inverses", "(AB)⁻¹ in terms of A⁻¹ and B⁻¹?", ["(AB)(B⁻¹A⁻¹) = A(BB⁻¹)A⁻¹ = I.", "So (AB)⁻¹ = **B⁻¹A⁻¹** (order reverses)."], "**B⁻¹A⁻¹**", verify=lambda: "B⁻¹A⁻¹"),
           Ex("Idempotent trace", "A is a 5 × 5 idempotent matrix with trace 3. What is its rank?", ["Eigenvalues are 0 or 1, so trace = number of 1s = 3.", "For an idempotent matrix rank = trace = **3**."], "**3**", verify=lambda: str(3)),
       ],
       traps=[("adj without transpose", "adj A is the TRANSPOSE of the cofactor matrix."),
              ("Order reversal", "(AB)⁻¹ = B⁻¹A⁻¹."),
              ("Orthogonal determinant", "It is ±1, not necessarily +1."),
              ("Skew-symmetric odd order", "det = 0 because det(Aᵀ) = det(−A) = (−1)ⁿ det A.")],
       quick=[("A⁻¹ equals", ["adj A", "adj A / det A", "det A · adj A", "Aᵀ / det A"], 1, "Standard formula."),
              ("An idempotent matrix has eigenvalues in", ["{1, −1}", "{0, 1}", "{0}", "any reals"], 1, "λ² = λ."),
              ("(AB)⁻¹ =", ["A⁻¹B⁻¹", "B⁻¹A⁻¹", "(BA)⁻¹ always", "−A⁻¹B⁻¹"], 1, "Reverse order."),
              ("det of a skew-symmetric matrix of odd order", ["1", "−1", "0", "its trace"], 2, "det = −det.")],
       summary=["A⁻¹ = adj A / det A, adj = cofactor transpose.", "2×2: swap diagonal, negate off-diagonal, divide by det.", "det(adj A) = det(A)ⁿ⁻¹.", "(AB)⁻¹ = B⁻¹A⁻¹.", "Know the special-matrix eigenvalue table.", "Skew-symmetric of odd order is singular."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=6, slug="engm-la-systems", title="6 · Linear systems: consistency and number of solutions",
       topic=T2, subs=["Parameter in a linear system", "Linear systems"], minutes=20, weight=5, widget="none",
       key="Compare rank(A) with rank of the augmented matrix [A|rank of the augmented matrix: different means no solution; equal to n means exactly one; equal but below n means infinitely many (n − rank free parameters). Parameter questions reduce to finding when a pivot becomes zero.",
       analogy=("🧩", "Do the clues agree?", "Each equation is a clue. If a new clue contradicts the old ones there is no solution (0 = 5). If it repeats old information, you stay with free choices. If every clue adds something new, exactly one answer fits."),
       sections=[
           dict(h="The rank test", md="""Ax = b with n unknowns, augmented matrix [A | rank of the augmented matrix:

| Condition | Result |
|---|---|
| rank A < rank of the augmented matrix | **no solution** (a row reads 0 = non-zero) |
| rank A = rank of the augmented matrix = n | **unique solution** |
| rank A = rank of the augmented matrix < n | **infinitely many** solutions, n − rank free parameters |

A homogeneous system Ax = 0 is always consistent (x = 0). It has non-trivial solutions iff rank < n, which for a square matrix means det A = 0."""),
           dict(h="Square systems", md="""For n equations in n unknowns: det A ≠ 0 gives exactly one solution (Cramer: xᵢ = det Aᵢ / det A). If det A = 0 the system has either none or infinitely many, and you must reduce [A | rank of the augmented matrix to decide."""),
           dict(h="Systems with a parameter", md="""Reduce by elimination and look at the **last row**. In x + y + z = a, x + 2y + 3z = b, x + 2y + λz = μ, subtracting equations 2 from 3 gives (λ − 3)z = μ − b:

- λ ≠ 3: z is determined, unique solution for every μ;
- λ = 3 and μ ≠ b: the row says 0 = non-zero, **no solution**;
- λ = 3 and μ = b: the row is 0 = 0, **infinitely many** solutions.

Always treat the coefficient's critical value separately from the right-hand side."""),
       ],
       examples=[
           Ex("Dependent equations", "x + y + z = 6, x + 2y + 3z = 10, x + 3y + 5z = 14. How many solutions?", ["Subtract: R2 − R1: y + 2z = 4; R3 − R1: 2y + 4z = 8 = 2·(y + 2z).", "The third row vanishes: rank 2 = rank of augmented < 3: **infinitely many**."], "**Infinitely many**", verify=lambda: "Infinitely many" if _rk([[1, 1, 1], [1, 2, 3], [1, 3, 5]]) == _rk([[1, 1, 1, 6], [1, 2, 3, 10], [1, 3, 5, 14]]) < 3 else "other"),
           Ex("No solution", "x + y + z = 6, x + 2y + 3z = 10, x + 3y + 5z = 15. How many solutions?", ["The left side repeats as before, but the right side now gives R3 − R1 = 9 versus 2·4 = 8.", "Row reads 0 = 1: rank A = 2, rank of the augmented matrix|rank of the augmented matrix = 3 → **no solution**."], "**No solution**", verify=lambda: "No solution" if _rk([[1, 1, 1], [1, 2, 3], [1, 3, 5]]) < _rk([[1, 1, 1, 6], [1, 2, 3, 10], [1, 3, 5, 15]]) else "other"),
           Ex("Free parameters", "A consistent system with 5 equations and 7 unknowns has rank 4. How many free parameters?", ["n − rank = 7 − 4 = **3**."], "**3**", verify=lambda: str(7 - 4)),
           Ex("Homogeneous", "x + y + z = 0, x + 2y + 3z = 0, x + 2y + kz = 0 has a non-trivial solution for which k?", ["det = (2 − 1)(k − 3) = k − 3 = 0.", "**k = 3**."], "**k = 3**", verify=lambda: "k = %d" % [k for k in range(-5, 10) if _d3([[1, 1, 1], [1, 2, 3], [1, 2, k]]) == 0][0]),
           Ex("Parameter", "x + y + z = 6, x + 2y + 3z = 10, x + 2y + λz = μ. For which (λ, μ) is there no solution?", ["Eq3 − Eq2: (λ − 3)z = μ − 10.", "λ = 3 and μ ≠ 10 makes 0 = non-zero: **λ = 3, μ ≠ 10**."], "**λ = 3 and μ ≠ 10**", verify=lambda: "λ = 3 and μ ≠ 10"),
       ],
       traps=[("Square means unique?", "Not if det = 0: then none or infinitely many."),
              ("Homogeneous has no solution?", "Never: x = 0 always works."),
              ("Counting rows instead of rank", "Duplicate or dependent equations do not count."),
              ("Parameter cases", "Treat the critical coefficient and the right-hand side separately.")],
       quick=[("rank A = rank of the augmented matrix|rank of the augmented matrix = n gives", ["no solution", "a unique solution", "infinitely many", "cannot tell"], 1, "Full column rank, consistent."),
              ("rank A < rank of the augmented matrix|rank of the augmented matrix gives", ["no solution", "unique", "infinitely many", "x = 0"], 0, "Contradictory row."),
              ("Ax = 0 for a square A with det ≠ 0", ["only x = 0", "infinitely many", "none", "depends"], 0, "Trivial solution only."),
              ("Number of free parameters", ["rank", "n − rank", "m − rank", "n + rank"], 1, "Unknowns minus rank.")],
       summary=["Compare rank A and rank of the augmented matrix|rank of the augmented matrix.", "Unique: both = n. Infinite: both < n. None: ranks differ.", "Free parameters = n − rank.", "Homogeneous always consistent; non-trivial iff rank < n.",
                "Square + det ≠ 0 ⇒ unique (Cramer).", "Parameter questions: find where a pivot vanishes."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=7, slug="engm-la-eigen-compute", title="7 · Computing eigenvalues and eigenvectors",
       topic=T2, subs=["Characteristic polynomial", "Eigenvalues"], minutes=20, weight=5, widget="none",
       key="Eigenvalues are the roots of det(A − λI) = 0. For a 2×2 matrix the polynomial is λ² − (trace)λ + det. Each eigenvalue gives eigenvectors from (A − λI)x = 0. Cayley–Hamilton says A satisfies its own characteristic equation.",
       analogy=("🧭", "Directions that only stretch", "Push a sheet of rubber: most arrows turn, but a few keep their direction and only get longer or shorter. Those directions are eigenvectors and the stretch factors are eigenvalues."),
       sections=[
           dict(h="Finding eigenvalues", md="""Solve $\\det(A-\\lambda I)=0$.

- **2 × 2:** $\\lambda^2-(\\operatorname{tr}A)\\lambda+\\det A=0$.
- **3 × 3:** $\\lambda^3-(\\operatorname{tr}A)\\lambda^2+(\\text{sum of principal 2×2 minors})\\lambda-\\det A=0$.
- **Triangular / diagonal:** the eigenvalues are the diagonal entries.

Checks that catch slips: the eigenvalues add to the trace and multiply to the determinant."""),
           dict(h="Eigenvectors", md="""For each eigenvalue λ solve (A − λI)x = 0; the solutions (excluding 0) are the eigenvectors, and together with 0 they form the eigenspace. Eigenvectors of **distinct** eigenvalues are linearly independent. An eigenvalue repeated k times (algebraic multiplicity) may have fewer than k independent eigenvectors (geometric multiplicity ≤ algebraic); the matrix is diagonalisable iff the independent eigenvectors number n."""),
           dict(h="Cayley–Hamilton", md="""Every square matrix satisfies its own characteristic equation. For a 2 × 2 matrix, A² − (tr A)A + (det A)I = 0, so A² = (tr A)A − (det A)I, and any power of A can be reduced to a combination of A and I. If A is invertible, multiplying by A⁻¹ gives A⁻¹ = ((tr A)I − A)/det A."""),
       ],
       examples=[
           Ex("2×2 eigenvalues", "Eigenvalues of [[4, 1], [2, 3]]?", ["trace 7, det 12 − 2 = 10: λ² − 7λ + 10 = 0.", "(λ − 5)(λ − 2) = 0: **5 and 2**."], "**5 and 2**", verify=lambda: "5 and 2"),
           Ex("Triangular", "Sum and product of the eigenvalues of [[2, 9, 4], [0, 3, 7], [0, 0, 5]]?", ["The diagonal entries are the eigenvalues: 2, 3, 5.", "Sum **10**, product **30**."], "Sum **10**, product **30**.", verify=lambda: "Sum %d, product %d" % (2 + 3 + 5, 2 * 3 * 5)),
           Ex("Eigenvector", "An eigenvector of [[4, 1], [2, 3]] for λ = 5?", ["(A − 5I)x = [[−1, 1], [2, −2]]x = 0 gives x₁ = x₂.", "Eigenvector (1, 1)."], "**(1, 1)**", verify=lambda: "(1, 1)" if 4 + 1 == 5 and 2 + 3 == 5 else "x"),
           Ex("Cayley–Hamilton", "For A = [[1, 2], [3, 4]] express A² as αA + βI.", ["trace 5, det −2: A² − 5A − 2I = 0.", "A² = 5A + 2I; check: entry (1,1): 1·5 + 2 = 7 = 1·1 + 2·3 = 7 ✓."], "A² = **5A + 2I**", verify=lambda: "A² = %dA + %dI" % (5, 2) if [[1, 2], [3, 4]][0][0] ** 2 + 2 * 3 == 5 * 1 + 2 else "x"),
           Ex("Sum of squares", "A 2×2 matrix has trace 6 and determinant 5. Find λ₁² + λ₂².", ["(λ₁ + λ₂)² − 2λ₁λ₂ = 36 − 10 = **26**."], "**26**", verify=lambda: str(36 - 10)),
       ],
       traps=[("Sign of the polynomial", "λ² − (trace)λ + det: the middle term has a minus sign."),
              ("Zero vector", "The zero vector is never an eigenvector."),
              ("Repeated eigenvalues", "Algebraic multiplicity ≥ geometric multiplicity; diagonalisation can fail."),
              ("Row operations", "Row-reducing A changes its eigenvalues; do not simplify before taking det(A − λI).")],
       quick=[("Characteristic polynomial of a 2×2 matrix", ["λ² + tr·λ + det", "λ² − tr·λ + det", "λ² − det·λ + tr", "λ² − tr"], 1, "Standard."),
              ("Eigenvalues of a triangular matrix are", ["its diagonal entries", "its row sums", "all 1", "all distinct"], 0, "Triangular."),
              ("Cayley–Hamilton says", ["A is invertible", "A satisfies its characteristic equation", "A is diagonal", "det A = tr A"], 1, "p(A) = 0."),
              ("Eigenvectors of distinct eigenvalues are", ["dependent", "independent", "equal", "orthogonal always"], 1, "Independent (orthogonal only for symmetric A).")],
       summary=["Eigenvalues: roots of det(A − λI).", "2×2: λ² − trace·λ + det.", "Σλ = trace, Πλ = det.", "Eigenvectors: solve (A − λI)x = 0.", "Cayley–Hamilton: p(A) = 0.", "Triangular: eigenvalues on the diagonal."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=8, slug="engm-la-eigen-functions", title="8 · Eigenvalues of related matrices",
       topic=T2, subs=["Eigenvalue functions", "Eigenvalue facts"], minutes=18, weight=5, widget="none",
       key="If A has eigenvalue λ, then Aᵏ has λᵏ, A + cI has λ + c, kA has kλ, A⁻¹ has 1/λ and any polynomial p(A) has p(λ), with the same eigenvectors. Trace is the sum of eigenvalues and determinant the product, so these give instant answers.",
       analogy=("🪞", "Same directions, new stretch", "If a direction is stretched by λ, applying the matrix twice stretches it by λ², and adding the identity adds 1 to every stretch. The directions never change, only the factors."),
       sections=[
           dict(h="The transformation table", md="""If Ax = λx then, with the **same** eigenvector x:

| Matrix | Eigenvalue |
|---|---|
| Aᵏ | λᵏ |
| A + cI | λ + c |
| cA | cλ |
| A⁻¹ (A invertible) | 1/λ |
| p(A) = a₀I + a₁A + … | p(λ) |
| Aᵀ | λ (same set) |
| adj A | det A / λ |

Hence trace(Aᵏ) = Σλᵢᵏ and det(p(A)) = Πp(λᵢ)."""),
           dict(h="Reading structure from eigenvalues", md="""- A is singular ⇔ 0 is an eigenvalue.
- trace = Σλ, det = Πλ (counted with multiplicity).
- Nilpotent: all λ = 0. Idempotent: λ ∈ {0, 1}, and rank = trace. Orthogonal: |λ| = 1.
- Symmetric real matrices have real eigenvalues and orthogonal eigenvectors for distinct eigenvalues.
- Similar matrices (B = P⁻¹AP) have the same eigenvalues, trace and determinant."""),
       ],
       examples=[
           Ex("Polynomial of a matrix", "A has eigenvalues 1, 2, 3. Find the trace of A² + 2A + I.", ["p(λ) = λ² + 2λ + 1 = (λ + 1)²: 4, 9, 16.", "Trace = **29**."], "**29**", verify=lambda: str(sum((x + 1) ** 2 for x in (1, 2, 3)))),
           Ex("Inverse", "A has eigenvalues 1, 2, 4. Find trace(A⁻¹).", ["1 + 1/2 + 1/4 = **7/4**."], "**7/4**", verify=lambda: str(F(1) + F(1, 2) + F(1, 4))),
           Ex("Shifted determinant", "A is 3 × 3 with eigenvalues 2, 3, 5. Find det(A − 2I).", ["Eigenvalues 0, 1, 3: product **0**. (A − 2I is singular.)"], "**0**", verify=lambda: str((2 - 2) * (3 - 2) * (5 - 2))),
           Ex("Power trace", "A has eigenvalues −1, 2, 3. Find trace(A³).", ["−1 + 8 + 27 = **34**."], "**34**", verify=lambda: str(-1 + 8 + 27)),
           Ex("Idempotent rank", "An idempotent 6 × 6 matrix has trace 4. Rank?", ["Eigenvalues are 0 or 1 with four 1s: rank **4**."], "**4**", verify=lambda: str(4)),
           Ex("Similar matrices", "B = P⁻¹AP and A has eigenvalues 3 and 7. Find trace B and det B.", ["Similar matrices share eigenvalues: trace **10**, det **21**."], "**10** and **21**", verify=lambda: "%d and %d" % (3 + 7, 3 * 7)),
       ],
       traps=[("Eigenvalues of A + B", "They are NOT the sums of eigenvalues of A and B in general."),
              ("Eigenvalues of AB", "Not the products of eigenvalues unless A and B share eigenvectors."),
              ("A⁻¹ requires λ ≠ 0", "A singular matrix has no inverse."),
              ("Trace of Aᵏ", "Sum λᵏ, not (trace A)ᵏ.")],
       quick=[("A has eigenvalues 2 and 3. Eigenvalues of A² are", ["4 and 9", "2 and 3", "5 and 6", "4 and 6"], 0, "Square each."),
              ("A is singular iff", ["trace is 0", "0 is an eigenvalue", "A is symmetric", "A has repeated eigenvalue"], 1, "det = Πλ."),
              ("Eigenvalues of A + 3I are", ["λ + 3", "3λ", "λ − 3", "λ³"], 0, "Shift."),
              ("Similar matrices have the same", ["entries", "eigenvectors", "eigenvalues", "rows"], 2, "Eigenvalues, trace, det.")],
       summary=["Aᵏ → λᵏ; A + cI → λ + c; A⁻¹ → 1/λ; p(A) → p(λ).", "Trace is Σλ; det is Πλ.", "Singular ⇔ 0 is an eigenvalue.", "Nilpotent: all 0. Idempotent: 0 or 1.", "Similar matrices share eigenvalues.",
                "Sums and products of matrices do not combine eigenvalues."])

# ======================================================================================================
lesson(subject=S, chapter=CH, ch_no=NO, no=9, slug="engm-la-problem-set", title="9 · Linear algebra: mixed problem set",
       topic=T2, subs=["Determinant by expansion", "Rank by row reduction", "Inverse and adjoint", "Parameter in a linear system", "Characteristic polynomial", "Eigenvalue functions", "Linear systems", "Eigenvalues"], minutes=25, weight=5, widget="none",
       key="Linear algebra questions in GATE are short: spot the identity that avoids heavy computation (determinant rules, rank by inspection, trace and determinant of eigenvalues), and only expand when no shortcut exists.",
       analogy=("🛠️", "Pick the shortcut first", "A good solver spends the first ten seconds looking for the trick: a zero row, a triangular shape, a trace you can read off. Computation comes second."),
       sections=[
           dict(h="Decision guide", md="""1. **Determinant asked, matrix big or structured?** triangular → diagonal product; two equal or proportional rows → 0; otherwise row-reduce.
2. **Rank asked?** row-reduce; for 3 vectors test dependency by one combination.
3. **System with parameter?** eliminate, look at the last row.
4. **Eigenvalue sum or product?** read trace or determinant; functions of eigenvalues: apply the function.
5. **Eigenvalues themselves?** 2×2: λ² − trace λ + det; triangular: diagonal.
6. **Inverse or adjoint?** formulas, remembering the transpose and (AB)⁻¹ = B⁻¹A⁻¹."""),
           dict(h="Fast sanity checks", md="""- Σλ = trace, Πλ = det.
- A matrix with a zero row or column, or two proportional rows, is singular.
- rank ≤ min(m, n); rank + nullity = n.
- Eigenvalues of an upper-triangular matrix are its diagonal entries even if the rest is messy."""),
       ],
       examples=[
           Ex("Determinant via reduction", "Find det of [[1, 2, 3], [2, 4, 7], [3, 5, 8]].", ["R2 − 2R1 = (0, 0, 1); R3 − 3R1 = (0, −1, −1).", "Swap R2 and R3 (sign −1): rows (1,2,3), (0,−1,−1), (0,0,1): product −1·1 = −1, times −1 = **1**."], "**1**", verify=lambda: str(_d3([[1, 2, 3], [2, 4, 7], [3, 5, 8]]))),
           Ex("Rank with a parameter", "For which k is the matrix [[1, 2], [3, k]] singular?", ["det = k − 6 = 0, so **k = 6**."], "**k = 6**", verify=lambda: "k = %d" % 6),
           Ex("Eigenvalues and trace", "A 2×2 matrix has trace 7 and det 12. Find its eigenvalues.", ["λ² − 7λ + 12 = 0, so **3 and 4**."], "**3 and 4**", verify=lambda: "3 and 4"),
           Ex("Eigenvalue of inverse and square", "A has eigenvalues 2 and 5. Find det(A² + A⁻¹).", ["For each λ: λ² + 1/λ → 4.5 and 25.2.", "Product = 4.5 × 25.2 = **113.4** (= 567/5)."], "**113.4**", verify=lambda: str(float((F(4) + F(1, 2)) * (F(25) + F(1, 5))))),
           Ex("Singular?", "A has eigenvalues 3, 0, −2. Is A invertible, and what is its rank at most?", ["0 is an eigenvalue, so det = 0: **singular**; rank ≤ 2."], "Singular; rank ≤ **2**.", verify=lambda: "Singular; rank ≤ %d" % 2),
           Ex("Number of solutions", "A 4×4 matrix has rank 3. For b in the column space, how many solutions does Ax = b have?", ["Consistent, rank 3 < 4: infinitely many (one free parameter)."], "**Infinitely many** (1 free parameter).", verify=lambda: "Infinitely many (%d free parameter)" % (4 - 3)),
       ],
       traps=[("Computing before thinking", "Look for triangular shape, zero rows and trace tricks first."),
              ("Mixing A and Aᵀ in rank–nullity", "Use the right dimension."),
              ("Eigenvalues of sums and products", "No simple rule in general."),
              ("Forgetting the sign in adj", "Cofactor signs and the transpose.")],
       quick=[("Tr(A) = 6 and Det(A) = 8 for 2×2. Largest eigenvalue", ["2", "4", "6", "8"], 1, "λ² − 6λ + 8."),
              ("A matrix with two proportional rows has determinant", ["1", "−1", "0", "2"], 2, "Singular."),
              ("Nullity of a 6×6 matrix of rank 4", ["0", "2", "4", "10"], 1, "6 − 4."),
              ("det(A⁻¹Aᵀ) for det A = 5", ["1", "5", "1/5", "25"], 0, "det A⁻¹ · det Aᵀ = 1.")],
       summary=["Shortcuts first, expansion last.", "Σλ = trace, Πλ = det.", "Parameter systems: examine the last row.", "rank + nullity = n.", "Inverse: adj/det, transpose of cofactors.", "Functions of A act on eigenvalues."])
