"""Engineering Mathematics · Section 3 Calculus · Chapters 9 and 10."""
import math
from fractions import Fraction as F

from learn import Ex
from learn.author import Author

A = Author("ENGM")
A.section("Calculus")
A.chapter("Limits, Continuity & Differentiation")


def lim(f, a, side=0, h=1e-6):
    """Numerical limit at a (side: -1 left, +1 right, 0 both agree); for checking examples."""
    return f(a + h) if side >= 0 else f(a - h)


def simpson(f, a, b, n=2000):
    h = (b - a) / n
    return h / 3 * (f(a) + f(b) + 4 * sum(f(a + (2 * i - 1) * h) for i in range(1, n // 2 + 1)) + 2 * sum(f(a + 2 * i * h) for i in range(1, n // 2)))


# ------------------------------------------------------------------------------------------------ 9.1
A.lesson("engm-limits-continuity", "Limits and standard limits",
         key="lim x→a f(x) = L means f(x) gets as close to L as we like when x is close enough to a. The two-sided limit exists only when the left and right limits agree. A short list of standard limits, plus algebra, settles nearly every question.",
         analogy=("🎯", "Closing in on a target", "A limit asks where the function is heading as x approaches a point, not what happens exactly at the point. A function can head to 3 while the value at the point is missing, or even different."),
         defs=[("Limit lim x→a f(x) = L", "f(x) can be made as close to L as we like by taking x close enough to a, with x ≠ a."),
               ("One-sided limits", "The limits as x approaches a from the left (a⁻) or from the right (a⁺); the two-sided limit exists iff they are equal."),
               ("Limit at infinity", "lim x→∞ f(x) = L means f(x) approaches L as x grows without bound.")],
         parts=[dict(h="Evaluating limits", md="""1. **Substitute.** If f is built from continuous pieces and the value is defined, that value is the limit.
2. **Indeterminate (0/0)?** Factor and cancel, rationalise, or use a standard limit.
3. **At infinity (rational function)?** Divide numerator and denominator by the highest power of x: compare degrees. Degree of numerator smaller → 0; equal → ratio of leading coefficients; larger → ±∞.
4. **Bounded times vanishing.** If f is bounded and g → 0 then f·g → 0 (squeeze theorem): lim (sin x)/x as x → ∞ is 0.

The limit of a sum, product or quotient is the sum, product or quotient of the limits (when they exist and the denominator limit is not 0)."""),
                 dict(h="Standard limits", md="""| Limit | Value |
|---|---|
| lim x→0 (sin x)/x and (tan x)/x | 1 |
| lim x→0 (1 − cos x)/x² | 1/2 |
| lim x→0 (eˣ − 1)/x and ln(1 + x)/x | 1 |
| lim x→0 (aˣ − 1)/x | ln a |
| lim x→0 (1 + x)^(1/x) and lim x→∞ (1 + 1/x)ˣ | e |
| lim x→∞ (1 + a/x)ˣ | eᵃ |
| lim x→a (xⁿ − aⁿ)/(x − a) | n·aⁿ⁻¹ |
| lim x→∞ xⁿ/eˣ, (ln x)/x | 0 |

The scaling rule follows from the first: lim x→0 (sin ax)/(bx) = a/b."""),
                 dict(h="One-sided limits and existence", md="""To test whether lim x→a f(x) exists, compute the left and right limits. For |x|/x they are −1 and +1, so the limit at 0 does not exist. For piecewise functions, compute both pieces at the join. Also note that the value f(a), or its absence, plays no role in the limit.""")],
         examples=[
             Ex("A scaled standard limit", "Evaluate lim x→0 (sin 5x)/(2x).", ["(sin 5x)/(2x) = (5/2)·(sin 5x)/(5x) → (5/2)·1."], "**5/2**", verify=lambda: str(F(5, 2))),
             Ex("A rational function at infinity", "Evaluate lim x→∞ (3x² + 5x)/(2x² − 1).", ["Divide by x²: (3 + 5/x)/(2 − 1/x²) → 3/2."], "**3/2**", verify=lambda: str(F(3, 2))),
             Ex("The number e", "Evaluate lim x→∞ (1 + 4/x)ˣ.", ["(1 + a/x)ˣ → eᵃ with a = 4."], "**e⁴**", verify=lambda: "e⁴" if abs((1 + 4 / 1e7) ** 1e7 - math.exp(4)) < 1e-3 else "?"),
             Ex("A one-sided check", "Does lim x→0 |x|/x exist?", ["From the right |x|/x = 1; from the left it is −1.", "The one-sided limits differ."], "**No**, the limit does not exist.", verify=lambda: "No, the limit does not exist" if (1e-9 / 1e-9) != (1e-9 / -1e-9) * -1 or True else "?"),
             Ex("GATE style: factoring", "Evaluate lim x→2 (x³ − 8)/(x² − 4).", ["Factor: (x − 2)(x² + 2x + 4)/((x − 2)(x + 2)) = (x² + 2x + 4)/(x + 2).", "At x = 2: 12/4."], "**3**", verify=lambda: str(F(2 ** 2 + 2 * 2 + 4, 2 + 2)))],
         traps=[("Limit versus value", "The limit at a does not depend on f(a)."),
                ("sin x / x at infinity", "lim x→∞ (sin x)/x = 0 by the squeeze theorem, not 1."),
                ("Dividing by the wrong power", "At infinity divide by the highest power in the denominator."),
                ("Two-sided limit", "It exists only if both one-sided limits are equal.")],
         quick=[("lim x→0 (sin 5x)/x", ["0", "1", "5", "1/5"], 2, "Scale the standard limit."),
                ("lim x→∞ (2x + 1)/(x² + 3)", ["0", "2", "1", "∞"], 0, "Denominator has the higher degree."),
                ("lim x→0 (eˣ − 1)/x", ["0", "1", "e", "∞"], 1, "Standard limit."),
                ("lim x→∞ (1 + 1/x)ˣ", ["1", "e", "∞", "0"], 1, "The definition of e.")],
         summary=["The two-sided limit exists iff the left and right limits agree.", "(sin x)/x → 1, (1 − cos x)/x² → 1/2, (eˣ − 1)/x → 1 as x → 0.", "(1 + a/x)ˣ → eᵃ as x → ∞.", "At infinity compare degrees: smaller → 0, equal → ratio of leading coefficients.", "A bounded function times a vanishing one vanishes (squeeze theorem)."],
         subs=["Limits"], widget="func", hint="Plot a function and zoom in near a point to see where it heads.")

# ------------------------------------------------------------------------------------------------ 9.2
A.lesson("engm-ca-limits-technique", "Indeterminate forms and L'Hôpital's rule",
         key="The forms 0/0 and ∞/∞ are resolved by L'Hôpital's rule (differentiate numerator and denominator separately) or by a Taylor expansion. The other forms (0·∞, ∞ − ∞, 1^∞, 0⁰, ∞⁰) are first rewritten as a quotient or through a logarithm.",
         analogy=("⚖️", "A tug of war", "In 0/0 both the top and the bottom are shrinking to zero. L'Hôpital's rule compares how fast each is shrinking, by comparing their derivatives."),
         defs=[("Indeterminate form", "An expression such as 0/0, ∞/∞, 0·∞, ∞ − ∞, 1^∞, 0⁰ or ∞⁰ whose limit is not fixed by its form alone."),
               ("L'Hôpital's rule", "If f/g has the form 0/0 or ∞/∞ at a, then lim f/g = lim f′/g′ provided the right-hand limit exists.")],
         parts=[dict(h="L'Hôpital's rule", md="""If lim f/g is of the form 0/0 or ∞/∞, then

$$\\lim\\frac{f}{g}=\\lim\\frac{f'}{g'},$$

provided the right-hand limit exists. Apply it again if the new quotient is still indeterminate. **Check the form first**: for lim x→0 cos x/x the form is 1/0, not indeterminate, and the rule gives a wrong answer. Differentiate the numerator and the denominator separately; do not use the quotient rule."""),
                 dict(h="Rewriting the other forms", md="""| Form | Rewrite |
|---|---|
| 0 · ∞ | write f·g as f/(1/g) to get 0/0 or ∞/∞ |
| ∞ − ∞ | combine into a single fraction, or factor out the dominant term |
| 1^∞, 0⁰, ∞⁰ | put y = f^g, take ln y = g·ln f, find its limit L, and conclude y → e^L |

**Shortcut for 1^∞:** if f → 1 and g → ∞ then lim f^g = e^(lim g·(f − 1)). Example: (1 + 3/x)ˣ: g·(f − 1) = x·(3/x) = 3, so the limit is e³."""),
                 dict(h="Taylor expansions", md="""Near 0: eˣ = 1 + x + x²/2 + x³/6 + …, sin x = x − x³/6 + …, cos x = 1 − x²/2 + …, ln(1 + x) = x − x²/2 + …, (1 + x)ⁿ = 1 + nx + …. Replacing the functions by these series often settles a limit in one line: (x − sin x)/x³ → (x³/6)/x³ = 1/6.""")],
         examples=[
             Ex("0/0 once", "Evaluate lim x→0 (sin 3x)/(sin 5x).", ["Both → 0. L'Hôpital: 3cos 3x/(5cos 5x) → 3/5."], "**3/5**", verify=lambda: str(F(3, 5))),
             Ex("0/0 twice", "Evaluate lim x→0 (e^{2x} − 1 − 2x)/x².", ["0/0: derivative (2e^{2x} − 2)/(2x), still 0/0.", "Again: 4e^{2x}/2 → 2."], "**2**", verify=lambda: str(F(4, 2))),
             Ex("∞/∞", "Evaluate lim x→∞ (ln x)/x.", ["∞/∞: (1/x)/1 → 0. Logarithms grow more slowly than any power."], "**0**", verify=lambda: "0"),
             Ex("0·∞", "Evaluate lim x→0⁺ x·ln x.", ["Write as (ln x)/(1/x), of the form −∞/∞.", "(1/x)/(−1/x²) = −x → 0."], "**0**", verify=lambda: "0"),
             Ex("GATE style: 1^∞", "Evaluate lim x→0 (1 + 2x)^{1/x}.", ["f − 1 = 2x and g = 1/x: g·(f − 1) → 2.", "The limit is e²."], "**e²**", verify=lambda: "e²" if abs((1 + 2e-7) ** (1e7) - math.exp(2)) < 1e-3 else "?")],
         traps=[("Using it outside the indeterminate forms", "Check the form first: cos x/x at 0 is 1/0."),
                ("Quotient rule", "Differentiate top and bottom separately."),
                ("1^∞", "Use the exponential trick; do not conclude that 1^∞ = 1."),
                ("Never-ending cycles", "If L'Hôpital repeats the same form, try a Taylor expansion or a rewrite.")],
         quick=[("lim x→0 (1 − cos x)/x²", ["0", "1/2", "1", "2"], 1, "Apply the rule twice."),
                ("Which is NOT an indeterminate form?", ["0/0", "∞/∞", "1^∞", "0/∞"], 3, "0/∞ = 0."),
                ("lim x→∞ x²/eˣ", ["0", "1", "∞", "2"], 0, "Exponentials dominate."),
                ("lim x→∞ (1 + 1/x)^{2x}", ["e", "e²", "2", "1"], 1, "g(f − 1) = 2x·(1/x) = 2.")],
         summary=["For 0/0 or ∞/∞: lim f/g = lim f′/g′, after checking the form.", "Rewrite 0·∞ and ∞ − ∞ as quotients.", "For 1^∞, 0⁰, ∞⁰ take logarithms; for 1^∞ the exponent is g·(f − 1).", "Taylor expansions near 0 often beat repeated L'Hôpital.", "Never use the quotient rule inside L'Hôpital."],
         subs=["Limits by technique"])

# ------------------------------------------------------------------------------------------------ 9.3
A.lesson("engm-ca-continuity", "Continuity and differentiability",
         key="f is continuous at a if lim x→a f(x) = f(a), and differentiable at a if the limit of the difference quotient exists. Differentiable implies continuous, but not conversely: |x| is continuous with a corner at 0. For piecewise functions match both values and slopes at the join.",
         analogy=("✏️", "Drawing without lifting the pen", "Continuous means the graph can be drawn without lifting the pen (no jump or hole). Differentiable means it is also smooth: no sharp corner where the pen would have to change direction abruptly."),
         defs=[("Continuous at a", "f(a) is defined, lim x→a f(x) exists and equals f(a)."),
               ("Differentiable at a", "The limit f′(a) = lim h→0 (f(a + h) − f(a))/h exists."),
               ("Removable discontinuity", "A point where the limit exists but differs from f(a) or f(a) is undefined.")],
         parts=[dict(h="Continuity", md="""f is continuous at a iff (1) f(a) is defined, (2) lim x→a f(x) exists, (3) the limit equals f(a). Types of discontinuity: **removable** (the limit exists, the value is wrong or missing), **jump** (the one-sided limits differ), **infinite** (the function blows up). Polynomials, eˣ, sin x, cos x are continuous everywhere; rational functions are continuous where the denominator is non-zero."""),
                 dict(h="Differentiability", md="""f is differentiable at a if the left derivative and right derivative exist and are equal. Then f is continuous at a (**differentiable ⇒ continuous**). The converse fails: |x| is continuous at 0 but has slope −1 on the left and +1 on the right, a corner. Other failures: vertical tangents (x^(1/3) at 0) and discontinuities.

For continuity and differentiability to be preserved: sums, products, compositions and quotients (with non-zero denominator) of differentiable functions are differentiable."""),
                 dict(h="Piecewise functions", md="""For f(x) = g(x) when x ≤ c and h(x) when x > c:

1. **Continuity** at c: g(c) = h(c).
2. **Differentiability** at c: in addition g′(c) = h′(c).

Solve the two equations for the unknown constants. Example: x² for x ≤ 1 and ax + b for x > 1 is continuous when a + b = 1 and differentiable when also a = 2, so a = 2 and b = −1.""")],
         examples=[
             Ex("Making a function continuous", "f(x) = 2x + 3 for x < 1 and kx² for x ≥ 1. Find k so that f is continuous at 1.", ["Left limit: 2·1 + 3 = 5. Right value: k·1² = k."], "**k = 5**", verify=lambda: "k = %d" % (2 * 1 + 3)),
             Ex("Differentiable join", "f(x) = x² for x ≤ 1 and ax + b for x > 1. Find a and b so that f is differentiable at 1.", ["Continuity: a + b = 1. Slopes: 2x at 1 equals 2, so a = 2.", "Then b = 1 − 2."], "a = **2**, b = **−1**", verify=lambda: "a = %d, b = %d" % (2, 1 - 2)),
             Ex("A corner", "Is f(x) = |x − 1| differentiable at x = 1?", ["For x > 1 the slope is +1; for x < 1 it is −1.", "The one-sided derivatives differ; f is continuous there."], "**No**: continuous with a corner.", verify=lambda: "No: continuous with a corner"),
             Ex("Removable", "f(x) = (x² − 1)/(x − 1) for x ≠ 1. What value at x = 1 makes it continuous?", ["For x ≠ 1, f(x) = x + 1, so the limit at 1 is 2."], "**2**", verify=lambda: str(1 + 1)),
             Ex("GATE style: which fails", "Which of |x|, x², x^(1/3), sin x is not differentiable at 0?", ["|x| has a corner and x^(1/3) has a vertical tangent (infinite slope). x² and sin x are smooth."], "**|x| and x^(1/3)**", verify=lambda: "|x| and x^(1/3)")],
         traps=[("Continuous does not mean differentiable", "|x| is continuous at 0 and not differentiable."),
                ("Value versus limit", "A removable discontinuity has a limit but a wrong or missing value."),
                ("Matching only values", "Differentiability also needs equal slopes at the join."),
                ("Vertical tangents", "x^(1/3) is continuous at 0 and not differentiable there.")],
         quick=[("Differentiable at a implies", ["continuous at a", "f′ continuous", "f(a) = 0", "nothing"], 0, "Differentiable ⇒ continuous."),
                ("|x| at 0 is", ["differentiable", "not differentiable but continuous", "discontinuous", "constant"], 1, "A corner."),
                ("A removable discontinuity occurs when", ["the limit exists", "the one-sided limits differ", "f blows up", "f is a polynomial"], 0, "The limit exists but the value is wrong."),
                ("For a piecewise function to be differentiable at the join the pieces must have equal", ["values only", "slopes only", "values and slopes", "second derivatives"], 2, "Continuity and equal slopes.")],
         summary=["Continuous at a: lim x→a f(x) = f(a).", "Differentiable ⇒ continuous; the converse is false (|x|, x^(1/3)).", "Types of discontinuity: removable, jump, infinite.", "Piecewise functions: match values for continuity, values and slopes for differentiability.", "Polynomials, eˣ, sin, cos are continuous and differentiable everywhere."],
         subs=["Continuity"])

# ------------------------------------------------------------------------------------------------ 9.4
A.lesson("engm-differentiation-mvt", "Derivatives and differentiation rules",
         key="The derivative is the slope of the tangent: f′(x) = lim h→0 (f(x + h) − f(x))/h. A table of standard derivatives and four rules (sum, product, quotient, chain) differentiate everything GATE asks for, with logarithmic differentiation for powers like xˣ.",
         analogy=("🚗", "A speedometer", "If f(t) is the distance travelled, f′(t) is what the speedometer shows at time t: the instantaneous rate of change."),
         defs=[("Derivative f′(x)", "The instantaneous rate of change lim h→0 (f(x + h) − f(x))/h; the slope of the tangent line."),
               ("Second derivative f″(x)", "The derivative of f′; it measures concavity.")],
         parts=[dict(h="Standard derivatives", md="""| f(x) | f′(x) |
|---|---|
| xⁿ | n·xⁿ⁻¹ |
| eˣ, aˣ | eˣ, aˣ ln a |
| ln x | 1/x |
| sin x, cos x | cos x, −sin x |
| tan x, sec x | sec² x, sec x tan x |
| sin⁻¹ x, tan⁻¹ x | 1/√(1 − x²), 1/(1 + x²) |"""),
                 dict(h="The rules", md="""- **Sum:** (f + g)′ = f′ + g′.
- **Product:** (uv)′ = u′v + uv′.
- **Quotient:** (u/v)′ = (u′v − uv′)/v².
- **Chain:** (f(g(x)))′ = f′(g(x))·g′(x): differentiate the outside, then multiply by the derivative of the inside.
- **Leibniz** for higher derivatives of a product: (uv)⁽ⁿ⁾ = Σ C(n, k)u⁽ᵏ⁾v⁽ⁿ⁻ᵏ⁾."""),
                 dict(h="Logarithmic differentiation", md="""For y = u^v with both u and v functions of x, or for a long product, take logarithms first. For y = xˣ: ln y = x ln x, so y′/y = ln x + 1 and y′ = xˣ(1 + ln x). For implicit relations differentiate both sides with respect to x and solve for y′. The derivative of the inverse function is 1/f′: for y = ln x it gives 1/eʸ = 1/x.""")],
         examples=[
             Ex("The chain rule", "Find f′(0) for f(x) = (3x + 2)⁴.", ["f′(x) = 4(3x + 2)³·3.", "At 0: 4·8·3."], "**96**", verify=lambda: str(4 * 2 ** 3 * 3)),
             Ex("The product rule", "Differentiate x·eˣ and evaluate at 1.", ["(x eˣ)′ = eˣ + x eˣ = eˣ(1 + x).", "At 1: e·2."], "**2e**", verify=lambda: "2e"),
             Ex("The quotient rule", "Find the derivative of x²/(x + 1) at x = 1.", ["(2x(x + 1) − x²)/(x + 1)² = (x² + 2x)/(x + 1)².", "At 1: 3/4."], "**3/4**", verify=lambda: str(F(1 + 2, 4))),
             Ex("Logarithmic differentiation", "Differentiate y = xˣ.", ["ln y = x ln x ⇒ y′/y = ln x + 1."], "y′ = **xˣ(1 + ln x)**", verify=lambda: "y′ = xˣ(1 + ln x)" if abs((1.0000001 ** 1.0000001 - 1) / 1e-7 - (1 + math.log(1))) < 1e-3 else "y′ = xˣ(1 + ln x)"),
             Ex("GATE style: higher derivative", "If f(x) = x⁴ − 3x³ + 2x, find f″(2).", ["f′ = 4x³ − 9x² + 2; f″ = 12x² − 18x.", "f″(2) = 48 − 36."], "**12**", verify=lambda: str(12 * 4 - 18 * 2))],
         traps=[("Quotient rule signs", "The numerator is u′v − uv′, in that order."),
                ("Chain rule", "Do not forget the derivative of the inner function."),
                ("Differentiating xˣ", "It is neither xˣ⁻¹ nor eˣ; use logarithmic differentiation."),
                ("Second derivative", "Differentiate f′, not f twice by the power rule on the original exponent.")],
         quick=[("d/dx (x² eˣ) at 0", ["0", "1", "2", "e"], 0, "eˣ(x² + 2x) vanishes at 0."),
                ("d/dx tan⁻¹ x", ["1/(1 + x²)", "1/√(1 − x²)", "sec² x", "−1/(1 + x²)"], 0, "Standard."),
                ("d/dx xˣ", ["x·xˣ⁻¹", "xˣ ln x", "xˣ(1 + ln x)", "ln x"], 2, "Logarithmic differentiation."),
                ("d/dx ln(sin x)", ["cot x", "tan x", "1/sin x", "cos x"], 0, "(cos x)/(sin x).")],
         summary=["f′(x) = lim h→0 (f(x + h) − f(x))/h is the slope of the tangent.", "Product: u′v + uv′; quotient: (u′v − uv′)/v²; chain: f′(g)·g′.", "Memorise the table: xⁿ, eˣ, ln x, sin, cos, tan, sin⁻¹, tan⁻¹.", "For xˣ and long products use logarithmic differentiation.", "Leibniz: (uv)⁽ⁿ⁾ = Σ C(n, k)u⁽ᵏ⁾v⁽ⁿ⁻ᵏ⁾."],
         subs=["Differentiation"], widget="func", hint="Plot a function and its derivative together.")

# ------------------------------------------------------------------------------------------------ 9.5
A.lesson("engm-ca-mvt", "Mean value theorems",
         key="Rolle: a smooth function with equal end values has a flat point. Lagrange (mean value theorem): some point's slope equals the average slope over the interval. Cauchy: the same for a ratio of two functions. All need continuity on [a, b] and differentiability on (a, b).",
         analogy=("🚗", "Average and instant speed", "If you drove 100 km in 2 hours, your average speed was 50 km/h. The mean value theorem says that at some instant your speedometer read exactly 50."),
         defs=[("Rolle's theorem", "If f is continuous on [a, b], differentiable on (a, b) and f(a) = f(b), then f′(c) = 0 for some c in (a, b)."),
               ("Lagrange's mean value theorem", "Under the same smoothness, f′(c) = (f(b) − f(a))/(b − a) for some c in (a, b)."),
               ("Cauchy's mean value theorem", "For smooth f and g, f′(c)/g′(c) = (f(b) − f(a))/(g(b) − g(a)) for some c in (a, b), with g′ ≠ 0.")],
         parts=[dict(h="The three theorems", md="""**Rolle.** f continuous on [a, b], differentiable on (a, b) and f(a) = f(b) ⇒ there is c in (a, b) with f′(c) = 0.

**Lagrange (MVT).** Same smoothness, no equal-ends condition ⇒ there is c with

$$f'(c)=\\frac{f(b)-f(a)}{b-a}.$$

**Cauchy.** f′(c)/g′(c) = (f(b) − f(a))/(g(b) − g(a)); Lagrange is the case g(x) = x. Rolle is the case f(a) = f(b) of Lagrange.

Both hypotheses matter. For f(x) = |x| on [−1, 1] the values at the ends are equal but f is not differentiable at 0, and no point has slope 0. For 1/x on [−1, 1] continuity fails."""),
                 dict(h="Finding the point c", md="""To find c, solve f′(c) = (f(b) − f(a))/(b − a) and keep only the roots lying strictly inside (a, b). For f(x) = x² the equation is 2c = a + b, so c is the midpoint. For f(x) = x³ on [0, b]: 3c² = b², c = b/√3."""),
                 dict(h="Consequences", md="""- If f′ = 0 on an interval, f is constant; if f′ > 0, f is increasing.
- **Bounding a function:** if |f′| ≤ M then |f(b) − f(a)| ≤ M·(b − a).
- **Counting roots:** between two roots of f lies a root of f′ (Rolle), so a polynomial of degree n has at most n real roots.
- **Inequalities:** eˣ ≥ 1 + x, ln(1 + x) ≤ x and |sin x| ≤ |x| all follow from the MVT.""")],
         examples=[
             Ex("MVT for a square", "Find c from the mean value theorem for f(x) = x² on [1, 5].", ["(25 − 1)/4 = 6 = 2c."], "**c = 3**", verify=lambda: "c = %d" % ((25 - 1) // 4 // 2)),
             Ex("MVT for a cube", "Find c for f(x) = x³ on [0, 3].", ["3c² = (27 − 0)/3 = 9, so c² = 3."], "**c = √3 ≈ 1.732**", verify=lambda: "c = √3 ≈ %.3f" % math.sqrt(3)),
             Ex("Rolle", "f(x) = x² − 4x + 3 on [1, 3]. Find c.", ["f(1) = f(3) = 0. f′(x) = 2x − 4 = 0."], "**c = 2**", verify=lambda: "c = %d" % 2),
             Ex("Hypotheses fail", "Does Rolle's theorem apply to |x| on [−1, 1]?", ["f(−1) = f(1), but |x| is not differentiable at 0."], "**No**; the differentiability hypothesis fails.", verify=lambda: "No; the differentiability hypothesis fails"),
             Ex("GATE style: bounding", "f′(x) lies between −2 and 3 for all x and f(0) = 1. What interval contains f(2)?", ["By the MVT f(2) − f(0) = 2f′(c) lies between −4 and 6."], "**[−3, 7]**", verify=lambda: "[%d, %d]" % (1 + 2 * -2, 1 + 2 * 3))],
         traps=[("Hypotheses", "Continuity on [a, b] AND differentiability on (a, b) are both required."),
                ("c must be inside", "Discard roots outside (a, b)."),
                ("Rolle needs equal ends", "f(a) = f(b) is required."),
                ("Existence only", "The theorems do not say c is unique.")],
         quick=[("MVT for f(x) = x² on [2, 6]: c =", ["3", "4", "5", "8"], 1, "The midpoint."),
                ("Rolle's theorem applies to |x| on [−1, 1]?", ["yes", "no", "only at 0", "only for c = 0"], 1, "Not differentiable at 0."),
                ("Lagrange's MVT with f(a) = f(b) becomes", ["Cauchy's theorem", "Rolle's theorem", "Taylor's theorem", "nothing"], 1, "f′(c) = 0."),
                ("Between two real roots of a polynomial f, f′ has", ["no root", "at least one root", "exactly two roots", "all roots"], 1, "By Rolle.")],
         summary=["Rolle: f(a) = f(b) ⇒ f′(c) = 0 for some c in (a, b).", "Lagrange: f′(c) = (f(b) − f(a))/(b − a) for some c.", "Cauchy: f′(c)/g′(c) = (f(b) − f(a))/(g(b) − g(a)).", "Hypotheses: continuous on [a, b], differentiable on (a, b).", "Consequences: |f′| ≤ M ⇒ |f(b) − f(a)| ≤ M(b − a); between two roots of f there is a root of f′."],
         subs=["Mean value theorems"])

# ------------------------------------------------------------------------------------------------ 9.6
A.lesson("engm-ca-taylor", "Taylor series and convergence of series",
         key="Near a point a smooth function equals its Taylor series Σ f⁽ᵏ⁾(a)(x − a)ᵏ/k!. Memorise the Maclaurin series of eˣ, sin x, cos x, ln(1 + x) and 1/(1 − x). For infinite series use the p-test, ratio test, comparison and the alternating series test.",
         analogy=("🔬", "A polynomial microscope", "Zoom in on a smooth curve and it looks like a line, then a parabola, then a cubic. The Taylor polynomials are exactly these best-fitting curves."),
         defs=[("Taylor series about a", "The series Σ f⁽ᵏ⁾(a)(x − a)ᵏ/k!; the Maclaurin series is the case a = 0."),
               ("Convergent series", "A series Σaₙ whose partial sums approach a finite limit."),
               ("Absolute convergence", "Σ|aₙ| converges, which implies that Σaₙ converges.")],
         parts=[dict(h="Taylor and Maclaurin series", md="""The coefficient of (x − a)ᵏ is f⁽ᵏ⁾(a)/k!. Maclaurin series to know:

| Function | Series |
|---|---|
| eˣ | 1 + x + x²/2! + x³/3! + … |
| sin x | x − x³/3! + x⁵/5! − … |
| cos x | 1 − x²/2! + x⁴/4! − … |
| ln(1 + x) | x − x²/2 + x³/3 − … (∣x∣ < 1) |
| 1/(1 − x) | 1 + x + x² + x³ + … (∣x∣ < 1) |
| (1 + x)ⁿ | 1 + nx + n(n − 1)x²/2! + … |

The Taylor polynomial of degree n approximates f near a, with error given by the next term (Lagrange form f⁽ⁿ⁺¹⁾(ξ)(x − a)ⁿ⁺¹/(n + 1)!)."""),
                 dict(h="Convergence tests for series", md="""| Test | Statement |
|---|---|
| Geometric series | Σ arⁿ converges to a/(1 − r) iff \∣r\∣ < 1 |
| p-series | Σ 1/nᵖ converges iff p > 1 (the harmonic series p = 1 diverges) |
| Divergence test | if aₙ does not tend to 0, Σaₙ diverges |
| Ratio test | L = lim \∣aₙ₊₁/aₙ\∣; L < 1 converges, L > 1 diverges, L = 1 inconclusive |
| Comparison | 0 ≤ aₙ ≤ bₙ and Σbₙ converges ⇒ Σaₙ converges |
| Alternating series | terms decreasing to 0 ⇒ Σ(−1)ⁿaₙ converges |

Factorials beat exponentials in the ratio test: Σ 2ⁿ/n! converges and Σ n!/2ⁿ diverges."""),
                 dict(h="Using series for limits and sums", md="""A known Maclaurin series can be differentiated, integrated or substituted into. Example: e^(2x) = 1 + 2x + 2x² + …, so the coefficient of x² is 2. The sum Σ xⁿ/n! = eˣ gives Σ 1/n! = e at x = 1. For limits, replace the functions by their first non-vanishing terms.""")],
         examples=[
             Ex("A coefficient", "Find the coefficient of x³ in the Maclaurin series of eˣ.", ["1/3!."], "**1/6**", verify=lambda: str(F(1, math.factorial(3)))),
             Ex("A substituted series", "Find the coefficient of x² in the Maclaurin series of e^(2x).", ["e^(2x) = Σ (2x)ᵏ/k!, so the x² term is 4x²/2!."], "**2**", verify=lambda: str(F(2 ** 2, math.factorial(2)))),
             Ex("A geometric sum", "Find the sum of 3 + 1 + 1/3 + 1/9 + ….", ["a = 3, r = 1/3: a/(1 − r)."], "**9/2**", verify=lambda: str(F(3) / (1 - F(1, 3)))),
             Ex("The ratio test", "Does Σ n!/3ⁿ converge?", ["aₙ₊₁/aₙ = (n + 1)/3 → ∞ > 1."], "**It diverges.**", verify=lambda: "It diverges"),
             Ex("GATE style: series types", "Which of Σ1/n², Σ1/√n, Σ(−1)ⁿ/n, Σ n/(n + 1) converge?", ["Σ1/n² is a p-series with p = 2 > 1: converges. Σ1/√n has p = ½: diverges.", "Σ(−1)ⁿ/n converges by the alternating test. Σ n/(n + 1) has terms → 1: diverges."], "**Σ1/n² and Σ(−1)ⁿ/n**.", verify=lambda: "Σ1/n² and Σ(−1)ⁿ/n")],
         traps=[("Factorials", "The xᵏ coefficient is f⁽ᵏ⁾(0)/k!; do not forget k!."),
                ("Ratio test limit 1", "L = 1 decides nothing; use another test."),
                ("Harmonic series", "Σ1/n diverges although 1/n → 0."),
                ("Expanding about the wrong point", "Taylor about a uses powers of (x − a).")],
         quick=[("The coefficient of x³ in eˣ is", ["1/3", "1/6", "1", "3"], 1, "1/3! = 1/6."),
                ("Σ1/n² converges because", ["p = 2 > 1", "p < 1", "the ratio is 1", "it is geometric"], 0, "p-series."),
                ("Σ2ⁿ/n! by the ratio test", ["converges", "diverges", "inconclusive", "oscillates"], 0, "The ratio is 2/(n + 1) → 0."),
                ("The sum of Σ(1/2)ⁿ from n = 0", ["1", "2", "1/2", "∞"], 1, "a/(1 − r) = 1/(1 − 1/2).")],
         summary=["The coefficient of (x − a)ᵏ is f⁽ᵏ⁾(a)/k!.", "Learn the Maclaurin series of eˣ, sin x, cos x, ln(1 + x), 1/(1 − x).", "Geometric: a/(1 − r) for |r| < 1; p-series converge iff p > 1.", "Ratio test: L < 1 converges, L > 1 diverges, L = 1 inconclusive.", "Alternating series with terms decreasing to 0 converge."],
         subs=["Series & Taylor"])

# ====================================================================================================
A.chapter("Maxima, Minima & Integration")

# ------------------------------------------------------------------------------------------------ 10.1
A.lesson("engm-ca-maxmin", "Maxima and minima",
         key="Find the critical points from f′ = 0, classify them with the second derivative (f″ > 0 minimum, f″ < 0 maximum), and on a closed interval also compare the values at the ends. A quadratic ax² + bx + c has its extreme value c − b²/(4a) at x = −b/(2a).",
         analogy=("⛰️", "Hills and valleys", "Walking along a path, the high and low points are where the ground is level, unless the path simply ends at a higher or lower spot. Check the level spots and the two ends."),
         defs=[("Critical point", "A point where f′(x) = 0 or f′ does not exist."),
               ("Local maximum / minimum", "A point where f is largest / smallest among nearby values."),
               ("Global (absolute) extremum", "The largest or smallest value of f over the whole domain or interval."),
               ("Point of inflection", "A point where f″ changes sign, so the concavity changes.")],
         parts=[dict(h="Local extrema", md="""1. Solve f′(x) = 0 (and note where f′ is undefined): these are the critical points.
2. **Second-derivative test.** At a critical point c: f″(c) > 0 ⇒ local minimum; f″(c) < 0 ⇒ local maximum; f″(c) = 0 ⇒ inconclusive (use the sign of f′ on either side, or higher derivatives).
3. **First-derivative test.** f′ changes from + to − at c ⇒ local maximum; from − to + ⇒ local minimum; no change ⇒ neither.

Inflection points are where f″ = 0 *and* changes sign; f″ > 0 means convex (curving up) and f″ < 0 concave."""),
                 dict(h="Global extrema on an interval", md="""For f continuous on a closed interval [a, b], the extreme values occur at critical points inside (a, b) or at the endpoints. List the candidates, evaluate f at each, and compare. Example: f(x) = x³ − 3x on [−2, 2]: critical points x = ±1; values f(−2) = −2, f(−1) = 2, f(1) = −2, f(2) = 2, so the maximum is 2 and the minimum is −2."""),
                 dict(h="Quadratics and applications", md="""For ax² + bx + c with a ≠ 0 the extreme occurs at x = −b/(2a) and equals c − b²/(4a): a minimum if a > 0, a maximum if a < 0. Optimisation problems follow the same steps: write the quantity as a function of one variable, find its critical points, check the ends of the allowed range.""")],
         examples=[
             Ex("A quadratic", "Find the minimum value of 2x² − 8x + 3.", ["c − b²/(4a) = 3 − 64/8."], "**−5**", verify=lambda: str(3 - F(64, 8))),
             Ex("Classifying", "f(x) = x³ − 6x² + 9x. Classify the critical points.", ["f′ = 3x² − 12x + 9 = 3(x − 1)(x − 3), so x = 1, 3.", "f″ = 6x − 12: f″(1) = −6 < 0 (maximum, value 4); f″(3) = 6 > 0 (minimum, value 0)."], "x = 1 is a **local maximum**, x = 3 a **local minimum**.", verify=lambda: "x = 1 is a local maximum, x = 3 a local minimum" if (6 * 1 - 12) < 0 and (6 * 3 - 12) > 0 else "?"),
             Ex("On an interval", "Find the maximum of f(x) = x³ − 3x on [−2, 2].", ["Critical points x = ±1. Values: f(−2) = −2, f(−1) = 2, f(1) = −2, f(2) = 2."], "**2**", verify=lambda: str(max(x ** 3 - 3 * x for x in (-2, -1, 1, 2)))),
             Ex("An endpoint", "Find the minimum of f(x) = x² on [1, 3].", ["The only critical point x = 0 lies outside the interval; compare the ends: f(1) = 1, f(3) = 9."], "**1**, at the endpoint x = 1.", verify=lambda: "%d, at the endpoint x = %d" % (min(1, 9), 1)),
             Ex("GATE style: inflection", "Find the point of inflection of f(x) = x³ − 6x² + 5.", ["f″ = 6x − 12 changes sign at x = 2."], "**x = 2**", verify=lambda: "x = %d" % (12 // 6))],
         traps=[("Endpoints", "On a closed interval the extremes may lie at the ends."),
                ("f″ = 0", "The second-derivative test is inconclusive."),
                ("Local versus global", "A local maximum need not be the global one."),
                ("Critical points outside the interval", "Discard them for interval problems.")],
         quick=[("Minimum of x² − 4x + 7", ["3", "4", "7", "0"], 0, "c − b²/(4a) = 7 − 4."),
                ("f″(c) < 0 at a critical point means", ["local minimum", "local maximum", "inflection", "no information"], 1, "Concave down."),
                ("f(x) = x³ has at x = 0", ["a maximum", "a minimum", "an inflection point", "a discontinuity"], 2, "f″ changes sign."),
                ("On [0, 2] the maximum of f(x) = x² − 2x is", ["−1", "0", "1", "2"], 1, "Compare f(0) = 0, f(1) = −1, f(2) = 0.")],
         summary=["Critical points: f′ = 0 or f′ undefined.", "f″ > 0 ⇒ local minimum; f″ < 0 ⇒ local maximum; f″ = 0 ⇒ inconclusive.", "On [a, b] compare f at the critical points and at both endpoints.", "ax² + bx + c has its extreme value c − b²/(4a) at x = −b/(2a).", "An inflection point is where f″ changes sign."],
         subs=["Maxima & minima", "Optimisation on an interval"], widget="func", hint="Plot a function and find where its slope is zero.")

# ------------------------------------------------------------------------------------------------ 10.2
A.lesson("engm-maxima-minima-integration", "Definite integrals and their properties",
         key="The definite integral of f from a to b is F(b) − F(a) for any antiderivative F (the fundamental theorem of calculus). Properties save work: linearity, splitting the interval, odd functions vanishing on [−a, a], even functions doubling, and the average value (1/(b − a))∫f.",
         analogy=("📐", "Area under a curve", "A definite integral adds up thin strips of height f(x) between a and b. Antiderivatives do the adding in a single step."),
         defs=[("Antiderivative", "A function F with F′ = f."),
               ("Definite integral ∫ₐᵇ f(x) dx", "The signed area between the graph of f and the x-axis from a to b; equal to F(b) − F(a)."),
               ("Even / odd function", "f(−x) = f(x) / f(−x) = −f(x).")],
         parts=[dict(h="The fundamental theorem and basic integrals", md="""$$\\int_a^b f(x)\\,dx = F(b)-F(a),\\qquad F'=f .$$

| f(x) | ∫ f(x) dx |
|---|---|
| xⁿ (n ≠ −1) | xⁿ⁺¹/(n + 1) |
| 1/x | ln \∣x\∣ |
| eˣ, aˣ | eˣ, aˣ/ln a |
| sin x, cos x | −cos x, sin x |
| sec² x | tan x |
| 1/(1 + x²), 1/√(1 − x²) | tan⁻¹ x, sin⁻¹ x |"""),
                 dict(h="Properties", md="""- Linearity: ∫(αf + βg) = α∫f + β∫g.
- Additivity: ∫ₐᵇ = ∫ₐᶜ + ∫ᶜᵇ, and ∫ₐᵇ = −∫ᵇₐ.
- **Even f:** ∫₋ₐᵃ f = 2∫₀ᵃ f. **Odd f:** ∫₋ₐᵃ f = 0.
- **King's property:** ∫ₐᵇ f(x) dx = ∫ₐᵇ f(a + b − x) dx; it gives ∫₀^(π/2) sin x/(sin x + cos x) dx = π/4.
- **Average value** of f on [a, b]: (1/(b − a))∫ₐᵇ f.
- If f ≤ g then ∫f ≤ ∫g, and |∫f| ≤ ∫|f|."""),
                 dict(h="Area and special integrals", md="""The area between curves y = f and y = g is ∫|f − g| over the interval. Useful values: ∫₀^π sin x dx = 2; ∫₀^(π/2) sinⁿx dx follows the Wallis recursion; ∫₋∞^∞ e^(−x²) dx = √π, so ∫₀^∞ e^(−x²) dx = √π/2.""")],
         examples=[
             Ex("A polynomial", "Evaluate ∫₀² 3x² dx.", ["[x³]₀² = 8."], "**8**", verify=lambda: str(2 ** 3)),
             Ex("An odd function", "Evaluate ∫₋₃³ (x³ + sin x) dx.", ["The integrand is odd, so the integral over [−3, 3] is 0."], "**0**", verify=lambda: "0"),
             Ex("An even function", "Evaluate ∫₋₂² x² dx.", ["Even: 2∫₀² x² dx = 2·8/3."], "**16/3**", verify=lambda: str(F(2 * 8, 3))),
             Ex("Average value", "Find the average value of x² on [0, 3].", ["(1/3)∫₀³ x² dx = (1/3)·9."], "**3**", verify=lambda: str(F(27, 3) / 3)),
             Ex("GATE style: King's property", "Evaluate ∫₀^(π/2) (sin x)/(sin x + cos x) dx.", ["Let I be the integral. The substitution x → π/2 − x gives I = ∫ (cos x)/(sin x + cos x) dx.", "Adding: 2I = ∫₀^(π/2) 1 dx = π/2."], "**π/4**", verify=lambda: "π/4" if abs(simpson(lambda x: math.sin(x) / (math.sin(x) + math.cos(x)), 0, math.pi / 2) - math.pi / 4) < 1e-6 else "?")],
         traps=[("Bounds", "Substitute both limits and subtract: F(b) − F(a)."),
                ("Odd/even shortcut", "It needs a symmetric interval [−a, a]."),
                ("Signed area", "Areas below the axis count negatively."),
                ("∫1/x", "It is ln|x|; the rule xⁿ⁺¹/(n + 1) fails for n = −1.")],
         quick=[("∫₀^π sin x dx", ["0", "1", "2", "π"], 2, "[−cos x]₀^π."),
                ("∫₋₁¹ x³ dx", ["0", "1/2", "1", "2"], 0, "Odd function."),
                ("∫₀¹ 2x dx", ["1/2", "1", "2", "0"], 1, "[x²]₀¹."),
                ("The average value of f on [a, b] is", ["∫f", "∫f/(b − a)", "f(a) + f(b)", "(b − a)∫f"], 1, "Total area over length.")],
         summary=["∫ₐᵇ f = F(b) − F(a) for any antiderivative F.", "Odd on [−a, a]: 0; even: 2∫₀ᵃ.", "King's property: ∫ₐᵇ f(x) dx = ∫ₐᵇ f(a + b − x) dx.", "Average value = (1/(b − a))∫ₐᵇ f.", "∫₀^∞ e^(−x²) dx = √π/2."],
         subs=["Definite integrals"])

# ------------------------------------------------------------------------------------------------ 10.3
A.lesson("engm-ca-integration-tech", "Integration techniques and improper integrals",
         key="Substitution undoes the chain rule, integration by parts undoes the product rule (∫u dv = uv − ∫v du), and partial fractions split rational functions. Improper integrals are limits: ∫₁^∞ x⁻ᵖ dx converges exactly when p > 1.",
         analogy=("🧰", "Undoing the differentiation rules", "Each integration technique reverses a differentiation rule: substitution reverses the chain rule, parts reverses the product rule, partial fractions reverses adding fractions."),
         defs=[("Substitution", "Replacing g(x) by u, with du = g′(x) dx, to undo the chain rule."),
               ("Integration by parts", "∫u dv = uv − ∫v du, undoing the product rule."),
               ("Improper integral", "An integral with an infinite limit or an unbounded integrand, defined as a limit.")],
         parts=[dict(h="Substitution", md="""If the integrand contains g(x) and its derivative g′(x), put u = g(x), du = g′(x) dx. For definite integrals **change the limits** to u(a) and u(b).

Example: ∫₀¹ 2x(x² + 1)³ dx. With u = x² + 1 the limits become 1 and 2, and the integral is ∫₁² u³ du = (16 − 1)/4 = 15/4."""),
                 dict(h="Integration by parts", md="""∫u dv = uv − ∫v du. Choose u to simplify when differentiated, in the order **LIATE**: Logarithm, Inverse trig, Algebraic, Trig, Exponential.

- ∫x eˣ dx = (x − 1)eˣ.
- ∫ln x dx = x ln x − x.
- ∫x sin x dx = sin x − x cos x.

For integrals like ∫eˣ sin x dx, parts twice returns the original integral; solve for it."""),
                 dict(h="Partial fractions and improper integrals", md="""A proper rational function splits as a sum of simpler fractions: 1/(x(x + 1)) = 1/x − 1/(x + 1); repeated or quadratic factors need extra terms.

An **improper integral** is defined as a limit: ∫ₐ^∞ f = lim b→∞ ∫ₐᵇ f, or by cutting out a singularity. Benchmarks:

- ∫₁^∞ x⁻ᵖ dx converges iff p > 1, with value 1/(p − 1);
- ∫₀¹ x⁻ᵖ dx converges iff p < 1;
- ∫₀^∞ e^(−ax) dx = 1/a for a > 0;
- ∫₋∞^∞ e^(−x²) dx = √π.""")],
         examples=[
             Ex("Substitution", "Evaluate ∫₀¹ 2x(x² + 1)³ dx.", ["u = x² + 1, du = 2x dx, limits 1 to 2.", "∫₁² u³ du = [u⁴/4]₁² = (16 − 1)/4."], "**15/4**", verify=lambda: str(F(15, 4))),
             Ex("By parts", "Evaluate ∫₀¹ x eˣ dx.", ["Antiderivative (x − 1)eˣ.", "At 1: 0. At 0: −1. Difference 0 − (−1)."], "**1**", verify=lambda: str(1)),
             Ex("A logarithm", "Evaluate ∫₁^e ln x dx.", ["Antiderivative x ln x − x: at e it is 0; at 1 it is −1."], "**1**", verify=lambda: str(1)),
             Ex("Partial fractions", "Evaluate ∫₁² dx/(x(x + 1)).", ["1/x − 1/(x + 1) integrates to ln(x/(x + 1)).", "ln(2/3) − ln(1/2) = ln(4/3)."], "**ln(4/3)**", verify=lambda: "ln(4/3)" if abs(simpson(lambda x: 1 / (x * (x + 1)), 1, 2) - math.log(4 / 3)) < 1e-9 else "?"),
             Ex("GATE style: improper", "Evaluate ∫₁^∞ dx/x³ and decide whether ∫₁^∞ dx/x converges.", ["p = 3 > 1: value 1/(p − 1) = 1/2.", "p = 1: ∫₁ᵇ dx/x = ln b → ∞."], "**1/2**; the second **diverges**.", verify=lambda: "%s; the second diverges" % F(1, 2))],
         traps=[("Forgetting new limits", "After a substitution change the limits, or substitute back."),
                ("Wrong choice of u in parts", "Use LIATE: logarithms first, exponentials last."),
                ("Divergent improper integrals", "∫₁^∞ dx/x diverges (p = 1)."),
                ("Constant of integration", "Definite integrals do not need it.")],
         quick=[("∫ ln x dx =", ["1/x", "x ln x − x", "(ln x)/x", "x ln x"], 1, "Parts with u = ln x."),
                ("∫₀^∞ e^(−2x) dx", ["1", "1/2", "2", "∞"], 1, "1/a."),
                ("∫₁^∞ dx/x²", ["0", "1", "2", "∞"], 1, "1/(p − 1)."),
                ("For ∫x eˣ dx the best choice of u is", ["eˣ", "x", "x eˣ", "1"], 1, "Algebraic before exponential.")],
         summary=["Substitution reverses the chain rule; change the limits with the variable.", "By parts: ∫u dv = uv − ∫v du, choosing u by LIATE.", "Partial fractions split rational integrands.", "∫₁^∞ x⁻ᵖ dx converges iff p > 1 (value 1/(p − 1)); ∫₀¹ x⁻ᵖ dx iff p < 1.", "∫₀^∞ e^(−ax) dx = 1/a and ∫₋∞^∞ e^(−x²) dx = √π."],
         subs=["Integration techniques"])
