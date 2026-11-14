"""Extra textbook-style elaboration for the lessons that had the shortest 'learn it from scratch' text."""
from learn import elab

elab("engm-random-variables-distributions",
 ("Expectation as a balance point, variance as spread", """
Think of a discrete random variable as weights placed on a number line: the probability of each value is the weight at that position. The **expectation** $E[X]=\\sum_x x\\,P(X=x)$ is the point where the line would balance. It is the long-run average over many repetitions, not necessarily a value the variable can take (a fair die has $E[X]=3.5$).

The **variance** $\\mathrm{Var}(X)=E[(X-\\mu)^2]$ measures how far values typically stray from that balance point, in squared units. The computational shortcut $\\mathrm{Var}(X)=E[X^2]-(E[X])^2$ saves time in exams: compute $E[X^2]$ by weighting squares, then subtract the square of the mean. The **standard deviation** $\\sigma=\\sqrt{\\mathrm{Var}(X)}$ returns to the original units.

Three rules cover most questions. **Linearity:** $E[aX+b]=aE[X]+b$, and $E[X+Y]=E[X]+E[Y]$ even when $X,Y$ are dependent. **Scaling:** $\\mathrm{Var}(aX+b)=a^2\\mathrm{Var}(X)$ (adding a constant does not change spread). **Independence:** $\\mathrm{Var}(X+Y)=\\mathrm{Var}(X)+\\mathrm{Var}(Y)$ only when $X$ and $Y$ are independent (more generally add $2\\,\\mathrm{Cov}(X,Y)$).
"""),
 ("Choosing the right distribution in a problem", """
Most GATE problems name the experiment in words; match the words to a distribution before calculating.

| The situation | Distribution | Mean and variance |
|---|---|---|
| One trial, success with probability $p$ | Bernoulli($p$) | $p$, $p(1-p)$ |
| Number of successes in $n$ independent trials | Binomial($n,p$) | $np$, $np(1-p)$ |
| Number of trials until the first success | Geometric($p$) | $1/p$, $(1-p)/p^2$ |
| Number of rare events in a fixed interval | Poisson($\\lambda$) | $\\lambda$, $\\lambda$ |
| Waiting time between Poisson events | Exponential($\\lambda$) | $1/\\lambda$, $1/\\lambda^2$ |
| Every value in $[a,b]$ equally likely | Uniform($a,b$) | $(a+b)/2$, $(b-a)^2/12$ |
| Sums or averages of many independent variables | Normal (central limit theorem) | $\\mu$, $\\sigma^2$ |

For a continuous variable, probabilities are **areas under the density**: $P(a\\le X\\le b)=\\int_a^b f(x)\\,dx$, so $P(X=a)=0$ for any single point, and the density itself may exceed 1. The **CDF** $F(x)=P(X\\le x)$ is non-decreasing from 0 to 1, and $f=F'$ wherever $F$ is differentiable.
"""),
 ("Typical slips to avoid", """
Do not add probabilities of events that can happen together, and do not multiply probabilities of events that are not independent. Check that a proposed PMF sums to 1 (or a density integrates to 1) before using it; many problems ask you to find the missing constant that way. For the exponential and geometric distributions remember the **memoryless property**: having already waited $s$ does not change the distribution of the remaining wait. And when a problem says "variance of $2X-3$", the answer is $4\\,\\mathrm{Var}(X)$: the sign and the constant disappear.
"""),
)

elab("engm-differentiation-mvt",
 ("Reading the derivative as a slope, a rate and a linear approximation", """
The derivative $f'(a)=\\lim_{h\\to0}\\frac{f(a+h)-f(a)}{h}$ answers three questions at once. Geometrically it is the **slope of the tangent line** at $a$. Physically it is the **instantaneous rate of change** (velocity is the derivative of position). Analytically it gives the best straight-line approximation near $a$: $f(a+h)\\approx f(a)+f'(a)h$. That last view explains why differentiable functions look straight when you zoom in, and why Taylor series simply add more terms to the approximation.

A function can fail to be differentiable at a point in three ways: a **corner** (the left and right slopes differ, as for $|x|$ at 0), a **vertical tangent** (the slope is infinite, as for $\\sqrt[3]{x}$ at 0), or a **discontinuity**. Differentiability always implies continuity; the converse is false.
"""),
 ("The derivatives to know by heart, and why", """
$\\frac{d}{dx}x^n=nx^{n-1}$ (the power rule, valid for every real $n$); $\\frac{d}{dx}e^x=e^x$ (the only function equal to its own derivative, up to a constant); $\\frac{d}{dx}\\ln x=\\frac1x$; $\\frac{d}{dx}\\sin x=\\cos x$ and $\\frac{d}{dx}\\cos x=-\\sin x$. Combine them with the **product rule** $(uv)'=u'v+uv'$, the **quotient rule** $\\left(\\frac uv\\right)'=\\frac{u'v-uv'}{v^2}$ and the **chain rule** $(f\\circ g)'=f'(g)\\,g'$. For a product of many factors or a variable exponent, take logarithms first (**logarithmic differentiation**): $y=x^x\\Rightarrow\\ln y=x\\ln x\\Rightarrow y'=x^x(\\ln x+1)$.

When two quantities are tied by an equation, differentiate both sides with respect to the independent variable and solve for the derivative (implicit differentiation), remembering that every $y$ contributes a factor $\\frac{dy}{dx}$.
"""),
 ("Why the mean value theorems matter", """
**Rolle's theorem** says: if $f$ is continuous on $[a,b]$, differentiable on $(a,b)$ and $f(a)=f(b)$, then $f'(c)=0$ for some $c$ in between. Picture a hill: climbing and returning to the same height forces a flat point. **Lagrange's mean value theorem** tilts the picture: somewhere the tangent is parallel to the chord, $f'(c)=\\frac{f(b)-f(a)}{b-a}$. Its consequences are the workhorses of analysis: if $f'>0$ on an interval then $f$ is increasing there; if $f'=0$ everywhere then $f$ is constant; and bounds on $f'$ give bounds on how fast $f$ can change.

In exam questions the hypotheses matter more than the conclusion. Always check continuity on the closed interval and differentiability on the open interval: $f(x)=|x|$ on $[-1,1]$ satisfies $f(-1)=f(1)$ but has no point with $f'(c)=0$, because it is not differentiable at 0.
"""),
)

elab("engm-probability-bayes",
 ("Bayes' theorem with natural frequencies", """
Probabilities in Bayes problems are easier to trust when translated into counts. Suppose 1% of items are defective, a test catches 90% of defective items and wrongly flags 5% of good ones. Imagine 10,000 items: 100 are defective and 90 of them are flagged; 9,900 are good and $0.05\\times9900=495$ are flagged. Among the $90+495=585$ flagged items only 90 are truly defective, so $P(\\text{defective}\\mid\\text{flagged})=90/585\\approx15.4\\%$. The formula $\\frac{P(F|D)P(D)}{P(F|D)P(D)+P(F|\\bar D)P(\\bar D)}$ gives the same number; the counts show **why** a positive result from a good test can still be weak evidence when the condition is rare.

Always identify the partition first (defective/good, urn A/urn B, machine 1/2/3), write the prior and the likelihood for each cell, and only then divide by the total probability of the observed event.
"""),
 ("Patterns that recur in GATE questions", """
Expect four patterns. **Urn problems:** choose an urn at random, then a ball; the posterior uses the number of balls of the observed colour in each urn. **Two children / dice and coins:** list the equally likely outcomes (for example 36 for two dice) and count those consistent with the information; conditioning on "at least one" and on "a specific one" give different answers. **Independence checks:** events $A$ and $B$ are independent iff $P(A\\cap B)=P(A)P(B)$; mutually exclusive events with positive probabilities are never independent. **Complement trick:** "at least one" is $1-P(\\text{none})$, which turns a long union into one product.
"""),
)

elab("engm-functions",
 ("Quick tests for one-to-one and onto on finite sets", """
For a function $f:A\\to B$ between finite sets, compare sizes first. If $|A|>|B|$ the function cannot be one-to-one (pigeonhole). If $|A|<|B|$ it cannot be onto. If $|A|=|B|$ then one-to-one, onto and bijective are all equivalent, so checking one suffices.

To test **injectivity** from a table or rule, look for two inputs with the same output (one repeated output is enough to fail). To test **surjectivity**, list the outputs and check that every element of the codomain appears. For real functions use calculus: a function that is strictly increasing or strictly decreasing is injective, and the range found from the extreme values tells you whether it is onto the stated codomain. Always read the **codomain** carefully: $f(x)=x^2$ is not onto $\\mathbb R$ but is onto $[0,\\infty)$.
"""),
 ("Counting functions: a checklist", """
With $|A|=m$ and $|B|=n$: all functions $n^m$ (each input independently chooses an output); one-to-one functions $\\frac{n!}{(n-m)!}$ for $m\\le n$ (the first input has $n$ choices, the next $n-1$, and so on); bijections $n!$ when $m=n$; onto functions need inclusion–exclusion, $\\sum_{k=0}^{n}(-1)^k\\binom nk(n-k)^m$. For **subsets** of $A$ there are $2^m$, which is also the number of functions from $A$ to a two-element set. Composition $g\\circ f$ is injective whenever both $f$ and $g$ are, and a function has an inverse exactly when it is a bijection.
"""),
)
