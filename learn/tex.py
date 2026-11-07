"""Plain-text formula (unicode sub/superscripts, a / b, Σ ...) -> TeX, so lesson formulas can be typeset as real maths."""
import re

SUP = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹ⁿⁱ⁺⁻ᵏˣ", "0123456789ni+-kx"))
SUB = dict(zip("₀₁₂₃₄₅₆₇₈₉ᵢₙₖⱼₐₓ₊₋ₘ", "0123456789inkjax+-m"))
SYM = {"·": r" \cdot ", "×": r" \times ", "−": "-", "–": "-", "≤": r" \le ", "≥": r" \ge ", "≠": r" \ne ", "≈": r" \approx ",
       "≡": r" \equiv ", "→": r" \to ", "⇔": r" \iff ", "⇒": r" \Rightarrow ", "∈": r" \in ", "∉": r" \notin ", "⊆": r" \subseteq ",
       "⊂": r" \subset ", "∪": r" \cup ", "∩": r" \cap ", "∨": r" \lor ", "∧": r" \land ", "¬": r" \lnot ", "∀": r" \forall ",
       "∃": r" \exists ", "∞": r" \infty ", "π": r" \pi ", "θ": r" \theta ", "λ": r" \lambda ", "μ": r" \mu ", "σ": r" \sigma ",
       "α": r" \alpha ", "β": r" \beta ", "γ": r" \gamma ", "δ": r" \delta ", "ε": r" \varepsilon ", "φ": r" \varphi ", "ρ": r" \rho ",
       "τ": r" \tau ", "ω": r" \omega ", "Σ": r" \sum ", "Π": r" \prod ", "Θ": r" \Theta ", "Ω": r" \Omega ", "Δ": r" \Delta ",
       "Λ": r" \Lambda ", "Γ": r" \Gamma ", "Φ": r" \Phi ", "∫": r" \int ", "√": r" \sqrt ", "⊕": r" \oplus ", "⊗": r" \otimes ",
       "∅": r" \emptyset ", "∑": r" \sum ", "′": "'", "ⁿ": "^n", "÷": r" \div ", "⌈": r" \lceil ", "⌉": r" \rceil ", "⌊": r" \lfloor ",
       "⌋": r" \rfloor ", "…": r" \ldots ", "≪": r" \ll ", "≫": r" \gg ", "∝": r" \propto ", "±": r" \pm ", "↔": r" \leftrightarrow ",
       "⇐": r" \Leftarrow ", "∖": r" \setminus ", "∣": r" \mid ", "⟨": r" \langle ", "⟩": r" \rangle ", "ℝ": r" \mathbb{R} ",
       "ℕ": r" \mathbb{N} ", "ℤ": r" \mathbb{Z} ", "⊢": r" \vdash ", "⊨": r" \models ", "≅": r" \cong ", "∘": r" \circ "}
FUN = {"log", "lim", "det", "min", "max", "sin", "cos", "tan", "mod", "rank", "gcd", "ln", "exp", "arg", "sup", "inf", "deg", "dim"}
_NUM = r"(?:\\[A-Za-z]+|[\w.]+)(?:\^\{[^{}]*\}|_\{[^{}]*\})*(?:\([^()]*(?:\([^()]*\)[^()]*)*\))?|\((?:[^()]|\([^()]*\))*\)"


def _runs(s, table, mark):
    out, i = [], 0
    while i < len(s):
        if s[i] in table:
            j = i
            while j < len(s) and s[j] in table:
                j += 1
            out.append("%s{%s}" % (mark, "".join(table[c] for c in s[i:j])))
            i = j
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def _unparen(x):
    return x[1:-1] if x.startswith("(") and x.endswith(")") and x.count("(") == 1 else x


def totex(s):
    t = _runs(_runs(s, SUP, "^"), SUB, "_")
    t = re.sub(r"\^\(([^()]*)\)", r"^{\1}", t)
    t = re.sub(r"\^(\w)", r"^{\1}", t)
    t = re.sub(r"_(\w)(?![\w{])", r"_{\1}", t)
    t = re.sub(r"Σ_\{([^{}]*?)=([^{}=]*?)\.\.([^{}]*)\}", r"\\sum_{\1=\2}^{\3}", t)
    t = re.sub(r"\bC\(([^()]*)\)", r"\\binom{\1}", t)
    t = re.sub(r"\\binom\{([^{},]*),\s*([^{}]*)\}", r"\\binom{\1}{\2}", t)
    for k, v in SYM.items():
        t = t.replace(k, v)
    t = t.replace("%", r"\%").replace("#", r"\#").replace("&", r"\&")
    t = re.sub(r"\bsqrt\(([^()]*)\)", r"\\sqrt{\1}", t)
    for _ in range(3):
        t = re.sub(r"(%s)\s*/\s*(%s)" % (_NUM, _NUM), lambda m: r"\frac{%s}{%s}" % (_unparen(m.group(1)), _unparen(m.group(2))), t)

    def word(m):
        w = m.group(0)
        if w.strip() in FUN:
            return r"\operatorname{%s}" % w.strip()
        return r"\text{%s}" % w.rstrip() + (" " if w.endswith(" ") else "")
    t = re.sub(r"(?<![\\A-Za-z{])(?:[A-Za-z]{3,}|[A-Za-z]{1,2}(?= [A-Za-z]{3,}))(?: [A-Za-z]{2,})*(?![A-Za-z]*[_^{(])(?<!\\)", word, t)
    t = re.sub(r"\\text\{(log|lim|det|min|max|sin|cos|tan|mod|rank|gcd|ln)\}", r"\\operatorname{\1}", t)
    t = re.sub(r" {2,}", r" \\quad ", t)
    t = t.replace(";", r";\ ").replace("  ", " ").strip()
    return t


def typeset(src):
    from .tex_data import TEX
    return TEX.get(src) or totex(src)
