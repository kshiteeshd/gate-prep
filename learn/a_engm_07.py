"""Engineering Mathematics · Section 2 Linear Algebra · Chapter 7 Matrices & Determinants."""
import itertools
import math
from fractions import Fraction as F

from content import g_engm2 as G2
from content import g_la as LA
from learn import Ex
from learn.author import Author

A = Author("ENGM")
A.section("Linear Algebra")
A.chapter("Matrices & Determinants")
mm = G2.mm

# ------------------------------------------------------------------------------------------------ 7.1
A.lesson("engm-matrices-determinants", "Matrix algebra and types of matrices",
         key="Matrices add entry by entry and multiply row by column; multiplication is associative but not commutative. Recognising the special types (symmetric, skew-symmetric, orthogonal, idempotent, nilpotent, triangular) is half the work, because each comes with its own shortcut.",
         analogy=("🔧", "Machines that transform vectors", "A matrix is a machine that turns an input vector into an output vector. Multiplying two matrices chains two machines, and the order of the chain matters: stretch-then-rotate is not rotate-then-stretch."),
         defs=[("Matrix", "A rectangular array of numbers; an m × n matrix has m rows and n columns."),
               ("Transpose Aᵀ", "The matrix with rows and columns exchanged: (Aᵀ)ᵢⱼ = Aⱼᵢ."),
               ("Trace", "The sum of the diagonal entries of a square matrix."),
               ("Symmetric / skew-symmetric", "A matrix with Aᵀ = A / with Aᵀ = −A."),
               ("Identity matrix I", "The square matrix with 1s on the diagonal and 0s elsewhere; AI = IA = A.")],
         parts=[dict(h="Operations and their rules", md="""- **Sum and scalar multiple** act entry by entry and need matrices of the same size.
- **Product.** If A is m × n and B is n × p, then AB is m × p with (AB)ᵢⱼ = Σₖ AᵢₖBₖⱼ: row i of A times column j of B. It costs m·n·p scalar multiplications.
- (AB)C = A(BC) and A(B + C) = AB + AC, but **AB ≠ BA in general**, and AB = 0 does not force A = 0 or B = 0.
- (AB)ᵀ = BᵀAᵀ and (AB)⁻¹ = B⁻¹A⁻¹: the order reverses.
- trace(A + B) = trace A + trace B and trace(AB) = trace(BA).

Every square matrix is the sum of a symmetric part (A + Aᵀ)/2 and a skew-symmetric part (A − Aᵀ)/2."""),
                 dict(h="Types of matrices", md="""| Type | Condition | Handy facts |
|---|---|---|
| Diagonal | aᵢⱼ = 0 for i ≠ j | eigenvalues = diagonal; Dᵏ is diagonal of powers |
| Upper / lower triangular | zeros below / above the diagonal | det = product of diagonal; eigenvalues = diagonal |
| Symmetric | Aᵀ = A | real eigenvalues |
| Skew-symmetric | Aᵀ = −A | zero diagonal; det = 0 when n is odd |
| Orthogonal | AᵀA = I | A⁻¹ = Aᵀ, det = ±1 |
| Idempotent | A² = A | eigenvalues 0 or 1; rank = trace |
| Nilpotent | Aᵏ = 0 for some k | all eigenvalues 0, trace 0 |
| Involutory | A² = I | eigenvalues ±1 |"""),
                 dict(h="Powers and block shortcuts", md="""For the shear matrix with rows [1 a] and [0 1], each multiplication adds a to the corner: its kth power has corner ka. For a diagonal matrix, the kth power is the diagonal of kth powers. For a block-triangular matrix the determinant is the product of the determinants of the diagonal blocks. A matrix equation can be manipulated like a number equation only when the order of factors is respected.""")],
         examples=[
             Ex("A product", "Compute AB for A = [1 2; 3 4] and B = [0 1; 1 0].", ["Row 1 of A with the columns of B: (1·0 + 2·1, 1·1 + 2·0) = (2, 1).", "Row 2: (3·0 + 4·1, 3·1 + 4·0) = (4, 3)."], "AB = **[2 1; 4 3]**", verify=lambda: "AB = [%s]" % "; ".join(" ".join(map(str, r)) for r in mm([[1, 2], [3, 4]], [[0, 1], [1, 0]]))),
             Ex("Non-commuting", "A = [1 1; 0 1] and B = [1 0; 1 1]. Is AB = BA?", ["AB = [2 1; 1 1] and BA = [1 1; 1 2].", "Different, though both have trace 3."], "**No**.", verify=lambda: "No" if mm([[1, 1], [0, 1]], [[1, 0], [1, 1]]) != mm([[1, 0], [1, 1]], [[1, 1], [0, 1]]) else "Yes"),
             Ex("A power", "Find A⁵ for A = [1 2; 0 1].", ["Each multiplication adds 2 to the corner: corner 5·2."], "A⁵ = **[1 10; 0 1]**", verify=lambda: "A⁵ = [1 %d; 0 1]" % ((lambda m: m[0][1])(__import__("functools").reduce(mm, [[[1, 2], [0, 1]]] * 5)))),
             Ex("Idempotent matrix", "A 5 × 5 idempotent matrix has trace 3. What is its rank?", ["The eigenvalues of an idempotent matrix are 0 or 1, so the trace counts the 1s.", "For an idempotent matrix rank = trace."], "**3**", verify=lambda: str(3)),
             Ex("GATE style: cost of a product", "A is 10 × 30, B is 30 × 5 and C is 5 × 60. How many scalar multiplications does (AB)C need, and does A(BC) need more?", ["(AB)C: AB costs 10·30·5 = 1500 (giving 10 × 5), then ·C costs 10·5·60 = 3000: total 4500.", "A(BC): BC costs 30·5·60 = 9000, then A·(30 × 60) costs 10·30·60 = 18000: total 27000."], "**4500**; A(BC) needs **27000**, far more.", verify=lambda: "%d; A(BC) needs %d, far more" % (10 * 30 * 5 + 10 * 5 * 60, 30 * 5 * 60 + 10 * 30 * 60))],
         traps=[("Commuting", "AB ≠ BA in general; never reorder factors without justification."),
                ("Transpose of a product", "(AB)ᵀ = BᵀAᵀ, not AᵀBᵀ."),
                ("Zero products", "AB = 0 does not imply A = 0 or B = 0."),
                ("Dimensions", "m × n times n × p is defined; n × p times m × n is not.")],
         quick=[("(AB)ᵀ =", ["AᵀBᵀ", "BᵀAᵀ", "BA", "AB"], 1, "Reverse the order."),
                ("A 2×3 matrix times a 3×4 matrix is", ["2×4", "3×3", "4×2", "undefined"], 0, "Outer dimensions."),
                ("trace(AB) =", ["trace(A)·trace(B)", "trace(BA)", "det(A)det(B)", "trace(A) + trace(B)"], 1, "A cyclic property."),
                ("An orthogonal matrix satisfies", ["A² = A", "AᵀA = I", "Aᵀ = −A", "A² = 0"], 1, "Its inverse is its transpose.")],
         summary=["The product AB is row-by-column, defined for m × n and n × p, with cost mnp.", "AB ≠ BA in general; (AB)ᵀ = BᵀAᵀ and (AB)⁻¹ = B⁻¹A⁻¹.", "trace(AB) = trace(BA).", "Symmetric Aᵀ = A; skew Aᵀ = −A; orthogonal AᵀA = I; idempotent A² = A; nilpotent Aᵏ = 0.", "Triangular and diagonal matrices have their eigenvalues on the diagonal."],
         subs=["Matrix algebra"], widget="matrix", hint="Edit a 2×2 or 3×3 matrix and see its determinant, trace, rank and eigenvalues.")

# ------------------------------------------------------------------------------------------------ 7.2
A.lesson("engm-la-determinants", "Determinants",
         key="A determinant of order 2 is ad − bc; of order 3 it is expanded along a row using cofactors; large ones are found by row reduction to triangular form. Swapping rows flips the sign, scaling a row scales the determinant, adding a multiple of a row changes nothing, and det(AB) = det A·det B.",
         analogy=("📐", "The area scale factor", "The determinant is the factor by which a matrix scales area (volume in 3-D). Swapping two rows flips orientation, so the sign changes; doubling one side doubles the area; a zero determinant squashes the picture flat."),
         defs=[("Determinant", "A number det A attached to a square matrix; it is non-zero exactly when the matrix is invertible."),
               ("Minor Mᵢⱼ", "The determinant of the matrix left after deleting row i and column j."),
               ("Cofactor Cᵢⱼ", "(−1)^(i + j)·Mᵢⱼ."),
               ("Singular matrix", "A square matrix with determinant 0.")],
         parts=[dict(h="Computing small determinants", md="""**2 × 2:**  $\\begin{vmatrix}a&b\\\\c&d\\end{vmatrix}=ad-bc.$

**3 × 3** by cofactor expansion along the first row: det = a₁₁C₁₁ + a₁₂C₁₂ + a₁₃C₁₃, where the signs of the cofactors follow the checkerboard + − +, − + −, + − +. Expand along the row or column with the most zeros. **Triangular** matrices (upper, lower or diagonal): the determinant is the product of the diagonal entries."""),
                 dict(h="Effect of row operations", md="""| Operation on A | Effect on det A |
|---|---|
| swap two rows (or columns) | multiply by −1 |
| multiply one row by k | multiply by k |
| add a multiple of one row to another | unchanged |
| two equal or proportional rows, or a zero row | det = 0 |
| transpose | unchanged |

To evaluate a large determinant, reduce to triangular form using row additions (free) and swaps (track the sign), then multiply the diagonal."""),
                 dict(h="Rules for whole matrices", md="""For n × n matrices:

- det(AB) = det A·det B; det(Aᵀ) = det A; det(A⁻¹) = 1/det A; det(Aᵏ) = (det A)ᵏ;
- **det(kA) = kⁿ·det A**;
- det(Aᵀ A) = (det A)²;
- **det(A + B) ≠ det A + det B** in general.

A is singular (det A = 0) exactly when it has no inverse, when its rows (columns) are linearly dependent, when rank < n, when Ax = 0 has a non-trivial solution, and when 0 is an eigenvalue.""")],
         examples=[
             Ex("A 3×3 determinant", "Find det [[2, 0, 1], [3, 1, 4], [1, 5, 2]].", ["Expand along the first row: 2·(1·2 − 4·5) − 0 + 1·(3·5 − 1·1).", "= 2·(−18) + 14."], "**−22**", verify=lambda: str(LA.det3([[2, 0, 1], [3, 1, 4], [1, 5, 2]]))),
             Ex("Triangular", "Find det [[2, 7, 1], [0, 3, 9], [0, 0, 5]].", ["Upper triangular: multiply the diagonal."], "**30**", verify=lambda: str(2 * 3 * 5)),
             Ex("Scaling", "A is 4 × 4 with det A = 3. Find det(2A).", ["det(kA) = kⁿ det A with k = 2, n = 4."], "**48**", verify=lambda: str(2 ** 4 * 3)),
             Ex("Row operations", "det A = 5. Swap rows 1 and 2, multiply row 3 by 4, then add 7·row 1 to row 2. What is the new determinant?", ["Swap: −5. Scaling one row by 4: −20. Adding a multiple: unchanged."], "**−20**", verify=lambda: str(5 * -1 * 4)),
             Ex("GATE style: combined rules", "A is 3 × 3 with det A = −4. Find det(AᵀA) and det(A³).", ["det(AᵀA) = (det A)² = 16.", "det(A³) = (det A)³ = −64."], "**16** and **−64**.", verify=lambda: "%d and %d" % ((-4) ** 2, (-4) ** 3))],
         traps=[("kA", "det(kA) = kⁿ det A, not k·det A. Only scaling ONE row multiplies by k."),
                ("Sign pattern", "The cofactor sign is (−1)^(i + j): position (2, 3) carries a minus."),
                ("Sums", "det(A + B) ≠ det A + det B."),
                ("Row additions", "Adding a multiple of a row leaves the determinant unchanged; swapping does not.")],
         quick=[("det of a matrix with two identical rows", ["1", "−1", "0", "undefined"], 2, "Dependent rows."),
                ("det(3A) for a 2×2 matrix with det A = 2", ["6", "12", "18", "54"], 2, "3²·2."),
                ("Swapping two rows multiplies the determinant by", ["0", "1", "−1", "2"], 2, "Orientation flips."),
                ("det(A⁻¹) =", ["det A", "−det A", "1/det A", "det Aᵀ"], 2, "det A·det A⁻¹ = 1.")],
         summary=["2×2: ad − bc; 3×3: cofactor expansion along a row; triangular: product of the diagonal.", "Swap → ×(−1); scale one row by k → ×k; add a multiple of a row → unchanged.", "det(AB) = det A·det B, det(kA) = kⁿ det A, det(A⁻¹) = 1/det A.", "det(A + B) ≠ det A + det B.", "det A = 0 ⇔ singular ⇔ rows dependent ⇔ 0 is an eigenvalue."],
         subs=["Determinant by expansion", "Determinants", "Determinant properties"])

# ------------------------------------------------------------------------------------------------ 7.3
A.lesson("engm-la-inverse", "Inverse and adjoint",
         key="A⁻¹ exists exactly when det A ≠ 0 and equals adj(A)/det A, where adj(A) is the transpose of the cofactor matrix. For a 2 × 2 matrix swap the diagonal entries, negate the off-diagonal ones and divide by the determinant.",
         analogy=("↩️", "The undo button", "A⁻¹ undoes whatever A did. It exists only if A did not squash the plane flat (det ≠ 0), because information lost by squashing cannot be restored."),
         defs=[("Inverse A⁻¹", "The matrix with AA⁻¹ = A⁻¹A = I; it exists iff det A ≠ 0."),
               ("Adjoint (adjugate) adj A", "The transpose of the matrix of cofactors of A."),
               ("Invertible matrix", "A square matrix that has an inverse; also called non-singular.")],
         parts=[dict(h="The inverse formula", md="""$$A^{-1}=\\frac{\\operatorname{adj}(A)}{\\det A},\\qquad \\operatorname{adj}(A)=C^{T},$$

where C is the matrix of cofactors. The transpose is the step that is forgotten: adj(A)ᵢⱼ is the cofactor Cⱼᵢ.

**2 × 2:** for A = [a b; c d] with ad − bc ≠ 0,  A⁻¹ = (1/(ad − bc))·[d −b; −c a].

Row-reduction method: write [A | I] and row-reduce; when the left block becomes I, the right block is A⁻¹. A zero row on the left means A is singular."""),
                 dict(h="Identities", md="""- A·adj(A) = adj(A)·A = det(A)·I.
- **det(adj A) = (det A)ⁿ⁻¹** for an n × n matrix.
- adj(AB) = adj(B)·adj(A); adj(kA) = kⁿ⁻¹ adj(A).
- (AB)⁻¹ = B⁻¹A⁻¹; (Aᵀ)⁻¹ = (A⁻¹)ᵀ; (A⁻¹)⁻¹ = A.
- For an orthogonal matrix A⁻¹ = Aᵀ; for a diagonal matrix the inverse is the diagonal of reciprocals."""),
                 dict(h="Using the inverse", md="""If A is invertible, the system Ax = b has the unique solution x = A⁻¹b. In practice one solves by elimination and avoids computing A⁻¹, but exam questions use the formulas above directly. Singular matrices (det = 0) have no inverse even when no row is obviously zero.""")],
         examples=[
             Ex("A 2×2 inverse", "Invert A = [4 7; 2 6].", ["det = 24 − 14 = 10.", "A⁻¹ = (1/10)·[6 −7; −2 4]."], "A⁻¹ = **(1/10)[6 −7; −2 4]**", verify=lambda: "A⁻¹ = (1/%d)[%d %d; %d %d]" % (4 * 6 - 7 * 2, 6, -7, -2, 4)),
             Ex("The adjoint", "Find adj A for A = [1 2; 3 4].", ["Cofactors: C₁₁ = 4, C₁₂ = −3, C₂₁ = −2, C₂₂ = 1.", "adj A is the transpose of [4 −3; −2 1]."], "adj A = **[4 −2; −3 1]**", verify=lambda: "adj A = [%d %d; %d %d]" % (4, -2, -3, 1)),
             Ex("Determinant of the adjoint", "A is 4 × 4 with det A = 2. Find det(adj A).", ["det(adj A) = (det A)ⁿ⁻¹ = 2³."], "**8**", verify=lambda: str(2 ** 3)),
             Ex("Inverse of a product", "What is (AB)⁻¹ in terms of A⁻¹ and B⁻¹?", ["(AB)(B⁻¹A⁻¹) = A(BB⁻¹)A⁻¹ = I."], "**B⁻¹A⁻¹** (the order reverses).", verify=lambda: "B⁻¹A⁻¹ (the order reverses)"),
             Ex("GATE style: trace of the adjoint", "Find the trace of adj(A) for A = [[1, 2, 3], [0, 1, 4], [5, 6, 0]].", ["The diagonal entries of adj A are the cofactors C₁₁, C₂₂, C₃₃.", "C₁₁ = 1·0 − 4·6 = −24; C₂₂ = 1·0 − 3·5 = −15; C₃₃ = 1·1 − 2·0 = 1."], "**−38**", verify=lambda: str(sum(LA.cof([[1, 2, 3], [0, 1, 4], [5, 6, 0]], i, i) for i in range(3))))],
         traps=[("adj without the transpose", "adj A is the TRANSPOSE of the cofactor matrix."),
                ("Order reversal", "(AB)⁻¹ = B⁻¹A⁻¹, not A⁻¹B⁻¹."),
                ("Singular matrices", "No inverse when det = 0."),
                ("2 × 2 signs", "Swap a and d, negate b and c; do not negate a and d.")],
         quick=[("A⁻¹ equals", ["adj A", "adj A / det A", "det A · adj A", "Aᵀ / det A"], 1, "Standard formula."),
                ("(AB)⁻¹ =", ["A⁻¹B⁻¹", "B⁻¹A⁻¹", "(BA)⁻¹ always", "−A⁻¹B⁻¹"], 1, "The order reverses."),
                ("det(adj A) for a 3×3 matrix with det A = 3", ["3", "6", "9", "27"], 2, "3²."),
                ("The inverse of an orthogonal matrix is", ["A", "Aᵀ", "−A", "adj A"], 1, "AᵀA = I.")],
         summary=["A⁻¹ = adj A / det A, where adj A is the transpose of the cofactor matrix.", "2×2: swap the diagonal, negate the off-diagonal, divide by det.", "A·adj A = det(A)·I and det(adj A) = (det A)ⁿ⁻¹.", "(AB)⁻¹ = B⁻¹A⁻¹ and (Aᵀ)⁻¹ = (A⁻¹)ᵀ.", "Row-reduce [A | I] to find A⁻¹; a zero row means A is singular."],
         subs=["Inverse and adjoint"])

# ------------------------------------------------------------------------------------------------ 7.4
A.lesson("engm-la-rank", "Rank and linear independence",
         key="The rank of a matrix is the number of non-zero rows after row reduction: the number of independent rows, which equals the number of independent columns. Rank plus nullity equals the number of columns.",
         analogy=("🧮", "How many independent facts", "Three equations are not always three facts: if the third is the sum of the first two it adds nothing. Rank counts the genuinely independent facts in a set of equations."),
         defs=[("Linear independence", "Vectors are independent if no non-trivial combination of them equals the zero vector."),
               ("Rank", "The maximum number of linearly independent rows (equivalently, columns) of a matrix."),
               ("Null space and nullity", "The solution set of Ax = 0 and its dimension."),
               ("Echelon form", "A form with zeros below each leading non-zero entry (pivot), obtained by row operations.")],
         parts=[dict(h="Computing the rank", md="""Use elementary row operations (swap, scale, add a multiple of one row to another); they do not change the rank. Reduce to echelon form and count the non-zero rows:

    [1 2 3]      [1 2 3]
    [2 4 6]  →   [0 0 0]      rank 2
    [1 2 4]      [0 0 1]

Facts: rank ≤ min(rows, columns); row rank = column rank; rank(A) = rank(Aᵀ); rank(AB) ≤ min(rank A, rank B); an n × n matrix has rank n iff det ≠ 0."""),
                 dict(h="Rank–nullity", md="""For an m × n matrix A (n columns, which is the number of unknowns of Ax = 0):

$$\\operatorname{rank}(A)+\\operatorname{nullity}(A)=n .$$

The nullity is the dimension of the solution space of Ax = 0, i.e. the number of free variables. For Aᵀ, which is n × m, nullity = m − rank. A square matrix is singular exactly when its nullity is positive."""),
                 dict(h="Testing independence", md="""Place the vectors as rows (or columns) of a matrix: they are independent iff its rank equals the number of vectors. For n vectors in n-space it is enough to check det ≠ 0. More than n vectors in n-space are always dependent. Example: (1, 2, 3), (4, 5, 6), (7, 8, 9) are dependent because the third equals twice the second minus the first.""")],
         examples=[
             Ex("Rank by reduction", "Find the rank of [[1, 2, 3], [2, 4, 6], [1, 2, 4]].", ["R₂ − 2R₁ = 0 and R₃ − R₁ = (0, 0, 1).", "Two non-zero rows remain."], "**2**", verify=lambda: str(LA.rank([[1, 2, 3], [2, 4, 6], [1, 2, 4]]))),
             Ex("Free variables", "A is 4 × 6 with rank 3. How many free variables does Ax = 0 have?", ["n − rank = 6 − 3."], "**3**", verify=lambda: str(6 - 3)),
             Ex("Nullity of the transpose", "A is 5 × 3 with rank 2. Find the nullity of A and of Aᵀ.", ["A has 3 columns: 3 − 2 = 1.", "Aᵀ has 5 columns: 5 − 2 = 3."], "**1** and **3**.", verify=lambda: "%d and %d" % (3 - 2, 5 - 2)),
             Ex("Independent vectors?", "Are (1, 2, 3), (4, 5, 6), (7, 8, 9) linearly independent?", ["The determinant is 0 (the third equals 2·second − first), so the rank is 2 < 3."], "**No**, they are dependent.", verify=lambda: "No, they are dependent" if LA.det3([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 0 else "Yes"),
             Ex("GATE style: rank with a parameter", "For which values of k does [[1, 2, 3], [2, 4, k], [3, 6, 9]] have rank 1, and what is its rank otherwise?", ["R₃ = 3R₁ always. R₂ − 2R₁ = (0, 0, k − 6).", "If k = 6 the matrix reduces to one non-zero row: rank 1. If k ≠ 6 there are two non-zero rows: rank 2."], "Rank **1** when **k = 6**, otherwise rank **2**.", verify=lambda: "Rank %d when k = %d, otherwise rank %d" % (LA.rank([[1, 2, 3], [2, 4, 6], [3, 6, 9]]), 6, LA.rank([[1, 2, 3], [2, 4, 7], [3, 6, 9]])))],
         traps=[("Stopping early", "Reduce completely before counting non-zero rows."),
                ("Which dimension", "Rank–nullity uses the number of COLUMNS."),
                ("Rank of a product", "rank(AB) can be smaller than both rank A and rank B."),
                ("Non-square matrices", "They have no determinant; test with rank.")],
         quick=[("A 3×5 matrix has maximum rank", ["3", "5", "8", "15"], 0, "min(3, 5)."),
                ("rank + nullity equals", ["number of rows", "number of columns", "trace", "determinant"], 1, "The number of unknowns n."),
                ("A 4×4 matrix of rank 3 is", ["invertible", "singular", "orthogonal", "diagonal"], 1, "rank < n."),
                ("Row operations change", ["the rank", "the solution set of Ax = b", "neither", "the nullity"], 2, "They preserve both.")],
         summary=["Rank = number of non-zero rows of the echelon form = number of independent rows or columns.", "rank ≤ min(m, n); rank(A) = rank(Aᵀ); rank(AB) ≤ min(rank A, rank B).", "rank + nullity = number of columns; free variables = n − rank.", "n vectors in n-space are independent iff det ≠ 0.", "An n × n matrix is invertible iff its rank is n."],
         subs=["Rank by row reduction", "Rank", "Rank-nullity"])
