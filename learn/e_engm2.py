"""Textbook-style long-form teaching text: Engineering Mathematics (linear algebra, calculus, probability)."""
from learn import elab

elab("engm-matrices-determinants",
 ("What a matrix is", """
A **matrix** is a rectangular table of numbers with $m$ rows and $n$ columns (an $m\\times n$ matrix). Matrices describe linear transformations, systems of equations and data tables. We add matrices of the same size entry by entry, and multiply a matrix by a number entry by entry.

**Matrix multiplication.** The product $AB$ exists only when the number of columns of $A$ equals the number of rows of $B$; the entry in row $i$, column $j$ of $AB$ is the dot product of row $i$ of $A$ with column $j$ of $B$. An $m\\times n$ times an $n\\times p$ matrix gives an $m\\times p$ matrix. Multiplication is associative but **not commutative**: usually $AB\\ne BA$. The **transpose** $A^T$ swaps rows and columns, and $(AB)^T=B^TA^T$.
"""),
 ("Determinants", """
For a square matrix the **determinant** is a single number that tells whether the matrix is invertible and how it scales volume. For $2\\times2$: $\\det\\begin{pmatrix}a&b\\\\c&d\\end{pmatrix}=ad-bc$. For larger matrices expand along a row or column using **cofactors**: multiply each entry by its minor with alternating signs $(+,-,+,\\dots)$.

Rules that save time:

- Swapping two rows changes the sign; multiplying a row by $k$ multiplies the determinant by $k$; adding a multiple of one row to another changes nothing.
- A matrix with two equal rows, or a zero row, has determinant 0.
- For a triangular matrix the determinant is the product of the diagonal.
- $\\det(AB)=\\det A\\det B$, $\\det(A^T)=\\det A$, $\\det(kA)=k^n\\det A$ for $n\\times n$.
"""),
 ("Inverse and rank", """
$A$ is **invertible** exactly when $\\det A\\ne0$, and then $A^{-1}=\\frac1{\\det A}\\operatorname{adj}A$, with $AA^{-1}=I$. The **rank** of a matrix is the number of linearly independent rows (equal to the number of independent columns); it is found by reducing to row-echelon form and counting non-zero rows. An $n\\times n$ matrix is invertible iff its rank is $n$.
"""),
)

elab("engm-linear-systems-eigen",
 ("Systems of linear equations", """
A system $A\\mathbf x=\\mathbf b$ of $m$ equations in $n$ unknowns is solved by row-reducing the **augmented matrix** $[A\\mid\\mathbf b]$. Compare ranks: if $\\operatorname{rank}A<\\operatorname{rank}[A\\mid\\mathbf b]$ there is **no solution**; if both equal $n$ there is a **unique solution**; if both equal $r<n$ there are **infinitely many**, with $n-r$ free parameters.

A **homogeneous** system $A\\mathbf x=\\mathbf 0$ always has the trivial solution $\\mathbf x=\\mathbf 0$; it has non-trivial solutions iff $\\operatorname{rank}A<n$ (for a square matrix, iff $\\det A=0$).
"""),
 ("Eigenvalues and eigenvectors", """
Multiplying a vector by a matrix usually changes its direction. An **eigenvector** $\\mathbf v\\ne\\mathbf0$ is special: $A\\mathbf v=\\lambda\\mathbf v$; the matrix only *stretches* it by the **eigenvalue** $\\lambda$. To find them, solve the **characteristic equation** $\\det(A-\\lambda I)=0$, then solve $(A-\\lambda I)\\mathbf v=\\mathbf0$ for each eigenvalue.

Facts: the sum of the eigenvalues equals the **trace** (sum of diagonal entries); their product equals $\\det A$; the eigenvalues of a triangular matrix are its diagonal entries; $A$ is singular iff 0 is an eigenvalue; eigenvalues of $A^k$ are $\\lambda^k$, of $A^{-1}$ are $1/\\lambda$; $A$ and $A^T$ have the same eigenvalues. **Cayley–Hamilton:** every matrix satisfies its own characteristic equation.
"""),
)

elab("engm-limits-continuity",
 ("The idea of a limit", """
$\\lim_{x\\to a}f(x)=L$ means that $f(x)$ gets as close as we like to $L$ when $x$ gets close enough to $a$ (but not necessarily equal to $a$). The value of $f$ *at* $a$ does not matter, only the behaviour *near* it. A limit exists only if the **left** and **right** limits agree.

Standard limits to know:

$$\\lim_{x\\to0}\\frac{\\sin x}{x}=1,\\qquad\\lim_{x\\to0}\\frac{e^x-1}{x}=1,\\qquad\\lim_{x\\to\\infty}\\left(1+\\frac1x\\right)^x=e$$
"""),
 ("Evaluating limits", """
If direct substitution gives a determinate number, that is the limit. If it gives $\\frac00$ or $\\frac\\infty\\infty$ (**indeterminate forms**), try: factorising and cancelling; multiplying by the conjugate; the standard limits above; or **L'Hôpital's rule**: differentiate numerator and denominator separately and try again, $\\lim\\frac{f}{g}=\\lim\\frac{f'}{g'}$. For limits at infinity of a ratio of polynomials, compare the highest powers.
"""),
 ("Continuity", """
A function $f$ is **continuous at $a$** if $\\lim_{x\\to a}f(x)=f(a)$: the limit exists, the function is defined there, and the two agree. Polynomials, $\\sin$, $\\cos$ and $e^x$ are continuous everywhere. A function is **discontinuous** at a *removable* point (limit exists but differs from the value), at a *jump* (left and right limits differ) or at an *infinite* discontinuity. A continuous function on a closed interval takes every value between its endpoint values (**intermediate value theorem**) and attains a maximum and minimum.
"""),
)

elab("engm-differentiation-mvt",
 ("The derivative", """
The **derivative** $f'(x)$ is the instantaneous rate of change of $f$: the slope of the tangent line, defined as

$$f'(x)=\\lim_{h\\to0}\\frac{f(x+h)-f(x)}{h}$$

Basic rules: $(x^n)'=nx^{n-1}$; $(e^x)'=e^x$; $(\\ln x)'=\\frac1x$; $(\\sin x)'=\\cos x$; $(\\cos x)'=-\\sin x$. **Sum rule**: $(f+g)'=f'+g'$. **Product rule**: $(fg)'=f'g+fg'$. **Quotient rule**: $\\left(\\frac fg\\right)'=\\frac{f'g-fg'}{g^2}$. **Chain rule**: $\\bigl(f(g(x))\\bigr)'=f'(g(x))\\cdot g'(x)$.
"""),
 ("Mean value theorems", """
**Rolle's theorem.** If $f$ is continuous on $[a,b]$, differentiable on $(a,b)$ and $f(a)=f(b)$, then there is a $c\\in(a,b)$ with $f'(c)=0$ (a flat tangent somewhere between two equal heights).

**Lagrange's mean value theorem.** Under the same conditions without $f(a)=f(b)$, there is a $c$ with

$$f'(c)=\\frac{f(b)-f(a)}{b-a}$$

(at some point the tangent is parallel to the chord). The conditions matter: $f(x)=|x|$ on $[-1,1]$ fails because it is not differentiable at 0. A consequence: if $f'\\equiv0$ on an interval then $f$ is constant there.
"""),
)

elab("engm-maxima-minima-integration",
 ("Finding maxima and minima", """
A **critical point** is where $f'(x)=0$ (or $f'$ does not exist). To classify it: if $f''(x)>0$ it is a **local minimum**; if $f''(x)<0$ a **local maximum**; if $f''=0$ the test is inconclusive (check the sign change of $f'$). The maximum of $f$ on a closed interval is the largest of the values at critical points and at the endpoints. A **point of inflection** is where the concavity changes.
"""),
 ("Integration", """
Integration reverses differentiation and measures accumulated quantity. The **indefinite integral** $\\int f(x)\\,dx=F(x)+C$ where $F'=f$. The **definite integral** $\\int_a^bf(x)\\,dx$ is the signed area under the curve, and by the **fundamental theorem of calculus**

$$\\int_a^bf(x)\\,dx=F(b)-F(a)$$

Basic integrals: $\\int x^n\\,dx=\\frac{x^{n+1}}{n+1}$ $(n\\ne-1)$, $\\int\\frac1x\\,dx=\\ln|x|$, $\\int e^x\\,dx=e^x$. Techniques: **substitution** (undoing the chain rule) and **integration by parts**, $\\int u\\,dv=uv-\\int v\\,du$.

The **average value** of $f$ on $[a,b]$ is $\\frac1{b-a}\\int_a^bf$. For an **odd** function (like $x^3$) $\\int_{-a}^a=0$; for an **even** function, $2\\int_0^a$.
"""),
)

elab("engm-probability-bayes",
 ("Probability from the ground up", """
An **experiment** has a **sample space** $S$ of all possible outcomes, and an **event** is a subset of it. If all outcomes are equally likely, $P(E)=\\frac{|E|}{|S|}$. In general probabilities satisfy $0\\le P\\le1$, $P(S)=1$, and for any events

$$P(A\\cup B)=P(A)+P(B)-P(A\\cap B),\\qquad P(\\bar A)=1-P(A)$$
"""),
 ("Conditional probability and independence", """
The probability of $A$ *given that* $B$ has occurred is $P(A\\mid B)=\\frac{P(A\\cap B)}{P(B)}$: we restrict attention to the outcomes where $B$ happened. Rearranged, $P(A\\cap B)=P(B)\\,P(A\\mid B)$. Events are **independent** if knowing one tells you nothing about the other, i.e. $P(A\\cap B)=P(A)P(B)$. **Mutually exclusive** events (cannot both happen) with positive probabilities are *never* independent.
"""),
 ("Total probability and Bayes' theorem", """
If $B_1,\\dots,B_n$ partition the sample space, then **total probability**: $P(A)=\\sum_iP(B_i)P(A\\mid B_i)$. **Bayes' theorem** turns it around:

$$P(B_k\\mid A)=\\frac{P(B_k)P(A\\mid B_k)}{\\sum_iP(B_i)P(A\\mid B_i)}$$

*Example.* A factory has two machines: $M_1$ makes 60% of items with 2% defective, $M_2$ makes 40% with 5% defective. A defective item is found: the probability it came from $M_1$ is $\\frac{0.6\\cdot0.02}{0.6\\cdot0.02+0.4\\cdot0.05}=\\frac{0.012}{0.032}=0.375$. A tree diagram helps: branch on the cause first, then on the evidence.
"""),
)

elab("engm-random-variables-distributions",
 ("Random variables", """
A **random variable** $X$ assigns a number to each outcome of an experiment (the number of heads in 3 tosses). A **discrete** variable takes countably many values with probabilities given by the **probability mass function** $p(x)=P(X=x)$; a **continuous** variable has a **density** $f(x)$ with $P(a\\le X\\le b)=\\int_a^bf$, and the total area is 1.

The **expected value** is the long-run average: $E[X]=\\sum x\\,p(x)$ (or $\\int xf$). **Linearity:** $E[aX+b]=aE[X]+b$ and $E[X+Y]=E[X]+E[Y]$ — true always, even if dependent. The **variance** $\\operatorname{Var}(X)=E[X^2]-(E[X])^2$ measures spread; $\\operatorname{Var}(aX+b)=a^2\\operatorname{Var}(X)$, and for **independent** $X,Y$, $\\operatorname{Var}(X+Y)=\\operatorname{Var}X+\\operatorname{Var}Y$.
"""),
 ("Distributions to know", """
- **Bernoulli($p$):** one trial, success with probability $p$; mean $p$, variance $p(1-p)$.
- **Binomial($n,p$):** number of successes in $n$ independent trials: $P(X=k)=\\binom nkp^k(1-p)^{n-k}$; mean $np$, variance $np(1-p)$.
- **Geometric($p$):** trials until the first success: $P(X=k)=(1-p)^{k-1}p$; mean $\\frac1p$.
- **Poisson($\\lambda$):** counts of rare events: $P(X=k)=\\frac{e^{-\\lambda}\\lambda^k}{k!}$; mean and variance both $\\lambda$.
- **Uniform($a,b$):** constant density on $[a,b]$; mean $\\frac{a+b}2$, variance $\\frac{(b-a)^2}{12}$.
- **Exponential($\\lambda$):** waiting times; mean $\\frac1\\lambda$; **memoryless**.
- **Normal($\\mu,\\sigma^2$):** the bell curve, symmetric about $\\mu$; about 68%, 95%, 99.7% of the probability lies within 1, 2, 3 standard deviations.
"""),
)
