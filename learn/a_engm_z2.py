"""Engineering Mathematics · depth pass for chapters 7-12: how GATE asks each topic, a harder example, and the key proofs."""
import itertools
import math
from fractions import Fraction as F

from content import g_engm2 as G2
from content import g_la as LA
from learn import Ex
from learn.author import Author

A = Author("ENGM")
C = math.comb
mm = G2.mm


def gate(rows, tail=""):
    t = "| Question type | How to attack it |\n|---|---|\n" + "\n".join("| %s | %s |" % tuple(c.replace("|", "∣") for c in r) for r in rows)
    return dict(h="How GATE asks this", md=t + ("\n\n" + tail if tail else ""))


def simpson(f, a, b, n=2000):
    h = (b - a) / n
    return h / 3 * (f(a) + f(b) + 4 * sum(f(a + (2 * i - 1) * h) for i in range(1, n // 2 + 1)) + 2 * sum(f(a + 2 * i * h) for i in range(1, n // 2)))


# ----------------------------------------------------------------------------- 7
A.extend("engm-matrices-determinants",
         parts=[gate([("Properties of special matrices", "Use the table: idempotent rank = trace, nilpotent trace 0, orthogonal det ±1."),
                      ("Entries or trace of a product", "Row-by-column; trace(AB) = trace(BA)."),
                      ("Is the product defined / its size", "Inner dimensions must agree; the result has the outer dimensions."),
                      ("Statements about AB, BA, (AB)ᵀ", "AB ≠ BA; (AB)ᵀ = BᵀAᵀ; (AB)⁻¹ = B⁻¹A⁻¹.")])],
         examples=[Ex("GATE style: skew-symmetric", "A is a 3 × 3 real skew-symmetric matrix. What is det A, and what are its possible eigenvalues?", ["Aᵀ = −A gives det A = det(−A) = (−1)³ det A = −det A, so det A = 0.", "Eigenvalues are 0 or purely imaginary pairs ±ib, so one eigenvalue is 0."], "det A = **0**; one eigenvalue is **0**.", verify=lambda: "det A = %d; one eigenvalue is 0" % LA.det3([[0, 1, 2], [-1, 0, 3], [-2, -3, 0]]))],
         proofs=[("Why trace(AB) = trace(BA)", "trace(AB) = Σᵢ (AB)ᵢᵢ = Σᵢ Σₖ AᵢₖBₖᵢ. Swapping the order of the two sums and the factors gives Σₖ Σᵢ BₖᵢAᵢₖ = Σₖ (BA)ₖₖ = trace(BA).")])
A.extend("engm-la-determinants",
         parts=[gate([("Value of a 3×3 or 4×4 determinant", "Expand along the row with most zeros or reduce to triangular form."),
                      ("det of a scaled, transposed or inverse matrix", "kⁿ·det, same, 1/det."),
                      ("Effect of row operations", "Swap −1, scale ×k, add 0."),
                      ("Determinant with a parameter or a pattern", "Factor using row differences, e.g. a Vandermonde-type matrix.")])],
         examples=[Ex("GATE style: a structured determinant", "Evaluate det [[1, 1, 1], [a, b, c], [a², b², c²]] for a = 1, b = 2, c = 3.", ["It is the Vandermonde determinant (b − a)(c − a)(c − b) = 1·2·1."], "**2**", verify=lambda: str(LA.det3([[1, 1, 1], [1, 2, 3], [1, 4, 9]])))],
         proofs=[("Why det(kA) = kⁿ det A", "Multiplying one row by k multiplies the determinant by k. Multiplying every one of the n rows by k does this n times, so the determinant is multiplied by kⁿ.")])
A.extend("engm-la-inverse",
         parts=[gate([("Inverse of a 2×2 or 3×3 matrix", "2×2 swap-negate-divide; 3×3 adjoint over determinant."),
                      ("Determinant of adj A or A⁻¹", "(det A)ⁿ⁻¹ and 1/det A."),
                      ("Which statement about inverses is true", "Order reverses in a product; the inverse of the transpose is the transpose of the inverse."),
                      ("Solve Ax = b using A⁻¹", "x = A⁻¹b; cheaper by elimination.")])],
         examples=[Ex("GATE style: inverse entry", "For A = [[2, 1], [5, 3]] find the entry in row 2, column 1 of A⁻¹.", ["det = 6 − 5 = 1.", "A⁻¹ = [3 −1; −5 2], so the entry is −5."], "**−5**", verify=lambda: str(F(-5, 1)) if 2 * 3 - 1 * 5 == 1 else "?")],
         proofs=[("Why A · adj(A) = det(A) · I", "The (i, j) entry of A·adj A is Σₖ aᵢₖCⱼₖ. For i = j this is the cofactor expansion of det A along row i. For i ≠ j it is the expansion of the determinant of a matrix in which row j has been replaced by row i, which has two equal rows and so equals 0. Hence the product is det A on the diagonal and 0 elsewhere.")])
A.extend("engm-la-rank",
         parts=[gate([("Rank of a numeric matrix", "Row-reduce and count non-zero rows."),
                      ("Rank with a parameter", "Find the values making rows dependent: det = 0 or a pivot vanishing."),
                      ("Nullity and free variables", "Columns minus rank."),
                      ("Rank of products and transposes", "rank(AB) ≤ min; rank(Aᵀ) = rank(A).")])],
         examples=[Ex("GATE style: bounding the rank", "A is 4 × 3 and B is 3 × 4, and AB = I₄ would be needed. Is it possible?", ["rank(AB) ≤ min(rank A, rank B) ≤ 3, but I₄ has rank 4."], "**No**: rank(AB) ≤ 3 < 4.", verify=lambda: "No: rank(AB) ≤ 3 < 4")],
         proofs=[("Why rank + nullity = n", "Row-reduce A to echelon form. The pivot columns number rank A; each of the other n − rank A columns corresponds to a free variable. The solutions of Ax = 0 are parametrised by the free variables, so the null space has dimension n − rank A.")])

# ----------------------------------------------------------------------------- 8
A.extend("engm-la-systems",
         parts=[gate([("How many solutions", "Compare the ranks of A and [A | b]."),
                      ("Values of a parameter giving none/one/infinitely many", "Eliminate and examine the last row."),
                      ("Non-trivial solutions of a homogeneous system", "det A = 0 for square systems."),
                      ("Number of free variables", "n − rank.")])],
         examples=[Ex("GATE style: unique solution", "For which k does x + y = 2, x + ky = 4 have a unique solution?", ["The determinant of [[1, 1], [1, k]] is k − 1.", "A unique solution needs k ≠ 1; for k = 1 the equations conflict (2 ≠ 4)."], "**k ≠ 1**", verify=lambda: "k ≠ 1" if LA.rank([[1, 1], [1, 1]]) == 1 and LA.rank([[1, 1, 2], [1, 1, 4]]) == 2 else "?")],
         proofs=[("Why Cramer's rule works", "If Ax = b with det A ≠ 0, then x = A⁻¹b = adj(A)b/det A. The ith entry of adj(A)b is Σⱼ Cⱼᵢbⱼ, which is the cofactor expansion along column i of the matrix Aᵢ obtained by replacing column i of A by b. So xᵢ = det Aᵢ / det A.")])
A.extend("engm-la-lu",
         parts=[gate([("Entries of L and U", "Multipliers form L; the eliminated matrix is U."),
                      ("Determinant from LU", "Product of the diagonal of U."),
                      ("Solving with LU", "Forward then back substitution."),
                      ("Cost and pivoting", "O(n³); partial pivoting gives PA = LU.")])],
         examples=[Ex("GATE style: determinant via LU", "Gaussian elimination reduces a 3 × 3 matrix to upper-triangular form with diagonal 2, −1, 4 and used one row swap. Find the determinant.", ["The product of the pivots is 2·(−1)·4 = −8.", "One row swap multiplies the determinant by −1."], "**8**", verify=lambda: str(-1 * (2 * -1 * 4)))])
A.extend("engm-la-eigen-compute",
         parts=[gate([("Eigenvalues of a given matrix", "2×2: λ² − tr λ + det; triangular: the diagonal."),
                      ("Sum and product of eigenvalues", "Trace and determinant, with no calculation."),
                      ("Eigenvector for a given eigenvalue", "Solve (A − λI)x = 0."),
                      ("Number of independent eigenvectors", "Nullity of A − λI.")])],
         examples=[Ex("GATE style: missing entry", "A = [[3, a], [1, 2]] has an eigenvalue 4. Find a.", ["4 satisfies λ² − 5λ + (6 − a) = 0: 16 − 20 + 6 − a = 0."], "**a = 2**", verify=lambda: "a = %d" % (16 - 20 + 6))],
         proofs=[("Why Σλ = trace and Πλ = det", "The characteristic polynomial det(A − λI) = (−1)ⁿ(λ − λ₁)⋯(λ − λₙ). Comparing the coefficient of λⁿ⁻¹ gives (−1)ⁿ⁻¹ Σλᵢ on the left by expanding the determinant, which is (−1)ⁿ⁻¹ trace(A). Setting λ = 0 gives det A = Πλᵢ.")])
A.extend("engm-la-eigen-functions",
         parts=[gate([("Eigenvalues of Aᵏ, A⁻¹, A + cI, p(A)", "Apply the function to each eigenvalue."),
                      ("Trace or determinant of such matrices", "Sum or product of the transformed eigenvalues."),
                      ("Singularity and rank from eigenvalues", "0 is an eigenvalue iff singular; idempotent rank = trace."),
                      ("Similar matrices", "Same eigenvalues, trace and determinant.")])],
         examples=[Ex("GATE style: idempotent", "A is 4 × 4 with A² = A and trace 2. Find det A and rank A.", ["Eigenvalues are 0 or 1 with two 1s and two 0s.", "0 is an eigenvalue, so det A = 0; rank = trace = 2."], "det A = **0**, rank = **2**.", verify=lambda: "det A = %d, rank = %d" % (0 ** 2 * 1 * 1, 2))])
A.extend("engm-la-cayley",
         parts=[gate([("Express Aⁿ or A⁻¹ using Cayley–Hamilton", "Reduce with A² = (tr)A − (det)I."),
                      ("Is the matrix diagonalisable", "n independent eigenvectors; repeated eigenvalues need extra care."),
                      ("Power of a diagonalisable matrix", "PDᵏP⁻¹; eigenvalues λᵏ."),
                      ("Minimal polynomial questions", "It divides the characteristic polynomial and has the same roots.")])],
         examples=[Ex("GATE style: a polynomial in A", "A is 2 × 2 with A² = 3A − 2I. Find A⁻¹ in the form αA + βI.", ["Rearrange: 2I = 3A − A² = A(3I − A).", "So A⁻¹ = (3I − A)/2 = −(1/2)A + (3/2)I."], "**A⁻¹ = −½A + (3/2)I**", verify=lambda: "A⁻¹ = −½A + (3/2)I")],
         proofs=[("Cayley–Hamilton for a 2 × 2 matrix", "Let A = [a b; c d]. Then A² = [a² + bc, b(a + d); c(a + d), d² + bc]. Compute (a + d)A − (ad − bc)I = [a² + ad − ad + bc, ab + bd; ca + cd, ad + d² − ad + bc] = [a² + bc, b(a + d); c(a + d), d² + bc]. The two matrices agree, so A² − (tr A)A + (det A)I = 0.")])

# ----------------------------------------------------------------------------- 9, 10
A.extend("engm-limits-continuity",
         parts=[gate([("Value of a limit", "Standard limits, factoring, dividing by the highest power."),
                      ("Does the limit exist", "Compare one-sided limits."),
                      ("Limits at infinity", "Compare growth: logs < powers < exponentials."),
                      ("Squeeze-type limits", "Bounded times vanishing is 0.")])],
         examples=[Ex("GATE style: growth comparison", "Evaluate lim x→∞ (x² + 3x)/(eˣ + x).", ["The exponential in the denominator grows faster than any polynomial."], "**0**", verify=lambda: "0" if (60 ** 2 + 3 * 60) / (math.exp(60) + 60) < 1e-15 else "?")])
A.extend("engm-ca-limits-technique",
         parts=[gate([("Limits needing L'Hôpital", "Identify the form; differentiate top and bottom; repeat."),
                      ("1^∞ limits", "Exponent × (base − 1)."),
                      ("Limits solved by Taylor series", "Replace the functions by leading terms."),
                      ("Forms like x^x, (sin x)^(tan x)", "Take logarithms.")])],
         examples=[Ex("GATE style: a difference of fractions", "Evaluate lim x→0 (1/x − 1/sin x).", ["Combine: (sin x − x)/(x sin x). Both → 0; Taylor: sin x − x ≈ −x³/6 and x sin x ≈ x².", "The ratio ≈ −x/6 → 0."], "**0**", verify=lambda: "0" if abs(1 / 1e-3 - 1 / math.sin(1e-3)) < 1e-3 else "?")])
A.extend("engm-ca-continuity",
         parts=[gate([("Value of a constant making f continuous/differentiable", "Equal values, then equal slopes at the join."),
                      ("Points of discontinuity", "Zeros of denominators, joins of pieces."),
                      ("Differentiable or not at a point", "Corners, cusps, vertical tangents."),
                      ("True/false: continuity vs differentiability", "Differentiable ⇒ continuous only.")])],
         examples=[Ex("GATE style: a function with absolute value", "Where is f(x) = |x² − 4| not differentiable?", ["The inside changes sign at x = ±2 with non-zero slope (±4), giving corners."], "**x = 2 and x = −2**", verify=lambda: "x = 2 and x = −2" if all(abs((abs(x * x - 4) - abs((x - 1e-6) ** 2 - 4)) / 1e-6 - (abs((x + 1e-6) ** 2 - 4) - abs(x * x - 4)) / 1e-6) > 1 for x in (2, -2)) else "?")])
A.extend("engm-differentiation-mvt",
         parts=[gate([("Derivative at a point", "Product, quotient, chain rule, then substitute."),
                      ("nth derivative", "Find the pattern or use Leibniz."),
                      ("Derivative of xˣ, x^(sin x)", "Logarithmic differentiation."),
                      ("Implicit differentiation", "Differentiate both sides; solve for dy/dx.")])],
         examples=[Ex("GATE style: implicit", "Find dy/dx at the point (1, 1) of the curve x³ + y³ = 2.", ["Differentiate: 3x² + 3y² y′ = 0, so y′ = −x²/y².", "At (1, 1): −1."], "**−1**", verify=lambda: str(-(1 ** 2) // (1 ** 2)) if 1 ** 3 + 1 ** 3 == 2 else "?")])
A.extend("engm-ca-mvt",
         parts=[gate([("Find the point c", "Solve f′(c) = average slope and keep roots inside the interval."),
                      ("Do the hypotheses hold", "Check continuity on [a, b] and differentiability on (a, b)."),
                      ("Bound a function using f′", "|f(b) − f(a)| ≤ M(b − a)."),
                      ("Number of roots of f or f′", "Between two roots of f there is one of f′.")])],
         examples=[Ex("GATE style: number of roots", "p(x) is a cubic with three distinct real roots. How many real roots does p′ have?", ["Between consecutive roots Rolle gives a root of p′: at least 2.", "p′ is quadratic, so at most 2."], "**2**", verify=lambda: str(3 - 1))],
         proofs=[("Lagrange's theorem from Rolle's theorem", "Define g(x) = f(x) − f(a) − ((f(b) − f(a))/(b − a))(x − a). Then g(a) = g(b) = 0, g is continuous on [a, b] and differentiable on (a, b). By Rolle there is c with g′(c) = 0, that is f′(c) = (f(b) − f(a))/(b − a).")])
A.extend("engm-ca-taylor",
         parts=[gate([("Coefficient of a term in a series", "Use the standard series and substitution."),
                      ("Does the series converge", "p-test, ratio test, alternating test."),
                      ("Sum of a series", "Geometric or exponential series."),
                      ("Limit by series", "Keep the first non-vanishing terms.")])],
         examples=[Ex("GATE style: sum via eˣ", "Find the sum of Σ₍ₙ₌₀₎^∞ 2ⁿ/n!.", ["Σ xⁿ/n! = eˣ with x = 2."], "**e²**", verify=lambda: "e²" if abs(sum(2 ** n / math.factorial(n) for n in range(40)) - math.exp(2)) < 1e-9 else "?")])
A.extend("engm-ca-maxmin",
         parts=[gate([("Local maximum/minimum of a cubic or quartic", "f′ = 0, then f″ at each root."),
                      ("Global maximum on an interval", "Compare critical points and endpoints."),
                      ("Optimisation word problem", "Express as one variable and differentiate."),
                      ("Number of local extrema", "Count the sign changes of f′.")])],
         examples=[Ex("GATE style: a box", "A rectangle of perimeter 20 has the largest area when its sides are equal. Find that area.", ["Sides x and 10 − x: area x(10 − x), maximum at x = 5."], "**25**", verify=lambda: str(max(x * (10 - x) for x in range(0, 11))))])
A.extend("engm-maxima-minima-integration",
         parts=[gate([("Value of a definite integral", "Antiderivative, then subtract the limits."),
                      ("Symmetric limits", "Odd functions vanish, even ones double."),
                      ("King's property integrals", "Add the integral to its reflected copy."),
                      ("Average value and area", "Integral over the length; integrate the difference of curves.")])],
         examples=[Ex("GATE style: area between curves", "Find the area enclosed by y = x and y = x² between x = 0 and x = 1.", ["x ≥ x² on [0, 1]: ∫₀¹ (x − x²) dx = 1/2 − 1/3."], "**1/6**", verify=lambda: str(F(1, 2) - F(1, 3)))])
A.extend("engm-ca-integration-tech",
         parts=[gate([("Substitution integrals", "Spot g(x) and g′(x); change the limits."),
                      ("Integrals needing parts", "x·eˣ, x sin x, ln x: apply LIATE."),
                      ("Improper integrals", "p-test: converge iff p > 1 at infinity, p < 1 at 0."),
                      ("Convergence of an improper integral", "Compare with a p-integral.")])],
         examples=[Ex("GATE style: a substitution", "Evaluate ∫₀^(π/2) sin x cos x dx.", ["Let u = sin x, du = cos x dx: ∫₀¹ u du."], "**1/2**", verify=lambda: str(F(1, 2)))])

# ----------------------------------------------------------------------------- 11, 12
A.extend("engm-probability-bayes",
         parts=[gate([("Probability with dice, coins, cards", "List equally likely outcomes; count favourable ones."),
                      ("At least one", "1 − P(none)."),
                      ("Union of events", "Inclusion–exclusion."),
                      ("Draws with and without replacement", "Multiply conditional probabilities or use combinations.")])],
         examples=[Ex("GATE style: a birthday-type problem", "In a group of 5 people, find the probability that at least two share a birthday month (12 equally likely months), to 3 decimals.", ["P(all different) = (12/12)(11/12)(10/12)(9/12)(8/12) = 95040/248832.", "1 − 0.382."], "**0.618**", verify=lambda: "%.3f" % (1 - math.perm(12, 5) / 12 ** 5))])
A.extend("engm-pb-conditional",
         parts=[gate([("P(A | B) from a table or sample space", "Restrict to B and count."),
                      ("Are A and B independent", "Check P(A ∩ B) = P(A)P(B)."),
                      ("Draws without replacement", "Chain rule of conditional probabilities."),
                      ("Conditioning on 'at least one'", "List the equally likely outcomes consistent with the statement.")])],
         examples=[Ex("GATE style: independence check", "A die is rolled. A: the result is even; B: the result is at most 4. Are A and B independent?", ["P(A) = 1/2, P(B) = 2/3, P(A ∩ B) = P({2, 4}) = 1/3.", "P(A)P(B) = 1/3."], "**Yes**, independent.", verify=lambda: "Yes, independent" if F(2, 6) == F(1, 2) * F(4, 6) else "No")],
         proofs=[("A and B independent ⇒ A and Bᶜ independent", "P(A ∩ Bᶜ) = P(A) − P(A ∩ B) = P(A) − P(A)P(B) = P(A)(1 − P(B)) = P(A)P(Bᶜ).")])
A.extend("engm-pb-bayes",
         parts=[gate([("Posterior probability of a cause", "Tree: prior × likelihood over the total."),
                      ("Total probability of an event", "Sum over the partition."),
                      ("Test accuracy problems", "Convert to natural frequencies."),
                      ("Sequential evidence", "The posterior after one observation is the prior for the next.")])],
         examples=[Ex("GATE style: two tests", "A disease has prevalence 2%. A test has 95% sensitivity and 90% specificity. Find P(sick | positive) to 3 decimals.", ["P(+) = 0.02·0.95 + 0.98·0.10 = 0.019 + 0.098 = 0.117.", "P(sick | +) = 0.019/0.117."], "**0.162**", verify=lambda: "%.3f" % (0.019 / 0.117))])
A.extend("engm-random-variables-distributions",
         parts=[gate([("Find the constant of a pmf/pdf", "Normalise to total 1."),
                      ("Probability from a pdf or CDF", "Integrate the pdf or subtract CDF values."),
                      ("Median/mode", "F(m) = 1/2; the maximum of the density."),
                      ("Is this a valid pdf/CDF", "Non-negative with integral 1; non-decreasing from 0 to 1.")])],
         examples=[Ex("GATE style: from a CDF", "X has CDF F(x) = x² for 0 ≤ x ≤ 1. Find P(0.3 < X ≤ 0.6) and the density.", ["P = F(0.6) − F(0.3) = 0.36 − 0.09 = 0.27.", "f(x) = F′(x) = 2x on [0, 1]."], "**0.27**; f(x) = **2x**.", verify=lambda: "%.2f; f(x) = 2x" % (0.6 ** 2 - 0.3 ** 2))])
A.extend("engm-pb-expectation",
         parts=[gate([("E[X] and Var(X) for a table or density", "Sum or integrate x·p(x) and x²·p(x)."),
                      ("Expectation of a sum or count", "Linearity with indicator variables."),
                      ("Variance of a linear combination", "Squares of the coefficients; independence needed to add."),
                      ("Bounds on probabilities", "Markov and Chebyshev.")])],
         examples=[Ex("GATE style: expected maximum", "Two fair dice are rolled. Find the expected value of the larger number.", ["P(max = k) = (2k − 1)/36 for k = 1..6.", "E = Σ k(2k − 1)/36 = 161/36."], "**161/36 ≈ 4.47**", verify=lambda: "%s ≈ %.2f" % (F(sum(max(a, b) for a in range(1, 7) for b in range(1, 7)), 36), sum(max(a, b) for a in range(1, 7) for b in range(1, 7)) / 36))],
         proofs=[("Var(X) = E[X²] − (E[X])²", "Var(X) = E[(X − μ)²] = E[X² − 2μX + μ²] = E[X²] − 2μE[X] + μ² = E[X²] − 2μ² + μ² = E[X²] − μ², using linearity of expectation.")])
A.extend("engm-pb-distributions",
         parts=[gate([("Mean/variance of a named distribution", "Table lookup."),
                      ("P(X = k) for binomial/Poisson", "Substitute into the pmf."),
                      ("Which distribution fits the story", "Fixed n: binomial; first success: geometric; rate: Poisson."),
                      ("Expected number of trials/failures", "1/p for trials; (1 − p)/p for failures before success.")])],
         examples=[Ex("GATE style: first success on an even trial", "A fair die is rolled until a six appears. Find the probability that the first six occurs on the 3rd roll.", ["Geometric with p = 1/6: (5/6)²·(1/6)."], "**25/216**", verify=lambda: str(F(5, 6) ** 2 * F(1, 6)))])
A.extend("engm-pb-continuous",
         parts=[gate([("Normal probabilities", "Standardise, then use the given Φ values."),
                      ("Exponential waiting times", "e^(−λt); memoryless."),
                      ("Uniform probabilities and moments", "Length ratios; (b − a)²/12."),
                      ("Sums of independent normals", "Means add and variances add.")])],
         examples=[Ex("GATE style: sum of normals", "X ~ N(10, 3²) and Y ~ N(20, 4²) are independent. State the distribution of X + Y.", ["Means add: 30. Variances add: 9 + 16 = 25."], "**N(30, 5²)**", verify=lambda: "N(%d, %d²)" % (10 + 20, int(math.sqrt(9 + 16))))])
A.extend("engm-pb-stats",
         parts=[gate([("Mean, median or mode of a data set", "Sort first; average the middle pair when the count is even."),
                      ("Variance or standard deviation", "Mean of squares minus the square of the mean."),
                      ("Effect of a linear transformation", "Mean transforms like the data; spread scales by |a|."),
                      ("Combined mean", "Weighted by group sizes.")])],
         examples=[Ex("GATE style: effect of adding a value", "The mean of 5 numbers is 20. A sixth number is added and the mean becomes 22. What is the new number?", ["The old total is 100; the new total is 6·22 = 132.", "132 − 100."], "**32**", verify=lambda: str(6 * 22 - 5 * 20))])
