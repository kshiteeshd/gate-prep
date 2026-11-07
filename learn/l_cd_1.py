"""Compiler Design part 1: lexical analysis, LL parsing, LR parsing."""
import re

from learn import Ex, lesson
from learn.refs import ref_ll1, ref_lr0, ref_sets, ref_slr

S = "CD"


def grammar(text):
    rules, nts = [], []
    for line in text.strip().split("\n"):
        lhs, rhs = [x.strip() for x in line.split("->")]
        if lhs not in nts:
            nts.append(lhs)
        for alt in rhs.split("|"):
            toks = [t for t in alt.split() if t != "e"]
            rules.append((lhs, toks))
    return nts, rules


def first_follow(text):
    nts, rules = grammar(text)
    nullable, first, follow, _ = ref_sets(nts, rules)
    return nts, nullable, first, follow


def fmt(sets, nts):
    return "; ".join("%s = {%s}" % (n, ", ".join(sorted(sets[n]))) for n in nts)


TOKEN_RE = re.compile(r"\s*(?:(?P<kw>\b(?:if|else|while|int|return)\b)|(?P<id>[A-Za-z_]\w*)|(?P<num>\d+\.\d+|\d+)|(?P<op>>=|<=|==|!=|&&|\|\||[-+*/=<>!;(){},]))")


def tokenize(src):
    pos, out = 0, []
    while pos < len(src):
        m = TOKEN_RE.match(src, pos)
        if not m:
            break
        if m.lastgroup:
            out.append((m.lastgroup, m.group(m.lastgroup)))
        pos = m.end()
    return out


EXPR_LR = "E -> E + T | T\nT -> T * F | F\nF -> ( E ) | id"
EXPR_LL = "E -> T X\nX -> + T X | e\nT -> F Y\nY -> * F Y | e\nF -> ( E ) | id"
LR_CLASSIC = "S -> L = R | R\nL -> * R | id\nR -> L"
SAA = "S -> A A\nA -> a A | b"

# ======================================================================================================
lesson(subject=S, chapter="Front End", ch_no=1, no=1, slug="cd-phases-lexical", title="Compiler Phases & Lexical Analysis",
       topic="Lexical Analysis", minutes=20, weight=3, widget="automata",
       widget_hint="A lexical analyser is a big DFA. Try an automaton for identifiers or for numbers like ‘digits then optional . digits’ and test strings.",
       key="A compiler translates source to target code in phases: lexical analysis (tokens), syntax analysis (parse tree), semantic analysis, intermediate code, optimisation and code generation. The lexer groups characters into tokens using regular expressions and the maximal-munch rule.",
       analogy=("📖", "Reading a sentence", "Before you understand a sentence you split it into words (lexing), then work out the grammar (parsing), then check that it makes sense (semantic analysis). A compiler does the same to a program before it can translate it."),
       sections=[
           dict(h="Phases of a compiler", md="""| Phase | Input → output | Typical errors found |
|---|---|---|
| **Lexical analysis** (scanner) | character stream → **tokens** | illegal characters, malformed numbers |
| **Syntax analysis** (parser) | tokens → **parse tree** | missing ‘;’, unbalanced brackets |
| **Semantic analysis** | tree + symbol table → annotated tree | type mismatch, undeclared variable |
| **Intermediate code generation** | → three-address code | – |
| **Code optimisation** | IR → better IR | – |
| **Code generation** | IR → target machine code | – |

Front end = analysis (language dependent); back end = synthesis (machine dependent). The **symbol table** is used by all phases; **error handling** too. A **pass** is one reading of the whole program; a **one-pass** compiler fuses phases. Interpreters execute without producing target code; **assemblers** translate assembly; **linkers/loaders** combine object modules."""),
           dict(h="Tokens, lexemes and patterns", md="""- **Lexeme:** the actual character sequence (`count`, `3.14`). **Token:** the category plus an optional attribute (`<id, pointer>`, `<num, 3.14>`). **Pattern:** the rule (a regular expression) describing the lexemes of a token.
- The scanner removes whitespace and comments, and records line numbers.
- **Maximal munch (longest match):** among all prefixes matching some pattern, choose the longest; ties are broken by rule order (keywords listed before identifiers). So `>=` is one token, not `>` then `=`; `iffy` is an identifier, not `if` followed by `fy`.
- Tools like **Lex/Flex** convert a list of regular expressions into a DFA-driven scanner.

**Input buffering** uses two buffer halves with sentinels so that scanning needs only one test per character in the common case."""),
           dict(h="Counting tokens (a GATE staple)", md="""To count tokens, split the code into the **longest-matching lexemes**; every identifier, keyword, constant, operator, punctuation symbol and string literal is one token, **whitespace and comments are not**. Watch for:

- Multi-character operators: `==`, `!=`, `>=`, `&&`, `++`, `->`.
- Strings: `"a b c"` is **one** token.
- `x+++y` scans as `x ++ + y` (maximal munch).
- Floating constants like `2.5e-3` are one token.

Lexical errors are rare (illegal characters, an unterminated string); mismatched parentheses or a missing semicolon are **syntax** errors."""),
           dict(h="Regular definitions and lexical DFAs", md="""Typical token definitions:

    letter  → [A-Za-z_]
    digit   → [0-9]
    id      → letter (letter | digit)*
    number  → digit+ (. digit+)? (E [+-]? digit+)?

The scanner is a DFA with one accepting state per token kind; when the DFA gets stuck, it returns the **last accepting state** it passed through and pushes the extra characters back. This explains why **backtracking** may be needed even with a DFA (e.g. recognising `12..` as `12` followed by `..`)."""),
       ],
       examples=[
           Ex("Counting tokens", "How many tokens does the C fragment `if (a1 >= 10) x = y + 2.5;` contain?",
              ["Tokens: if, (, a1, >=, 10, ), x, =, y, +, 2.5, ;", "That is **12** tokens (>= counts once by maximal munch)."],
              "**12** tokens.", verify=lambda: str(len(tokenize("if (a1 >= 10) x = y + 2.5;")))),
           Ex("Maximal munch", "How is `x+++y` tokenised by a C scanner, and how many tokens is that?",
              ["Maximal munch takes `++` first, then `+`: x, ++, +, y.", "**4** tokens."],
              "x ++ + y — **4** tokens.", verify=lambda: "x ++ + y — %d tokens" % len(re.findall(r"\+\+|\+|[a-z]", "x+++y"))),
           Ex("Compiler phase of an error", "Which phase detects the error in `int x = ;` and in `int y = \"s\" + 3;`?",
              ["`int x = ;` has a missing expression: a **syntax** error found by the parser.", "`\"s\" + 3` is grammatical but adds a string and an integer: a **semantic (type)** error."],
              "Syntax; semantic.", verify=lambda: "Syntax; semantic"),
           Ex("Lexeme vs token", "In `count = count + 1;`, how many distinct lexemes and how many distinct token types (id, assign, plus, num, semicolon) are there?",
              ["Lexemes: count, =, +, 1, ; ⇒ 5 distinct (count appears twice).", "Token types: id, assign, plus, num, semicolon ⇒ 5 as well (the token count is 6)."],
              "**5** distinct lexemes, **5** token types (6 tokens in total).", verify=lambda: "%d distinct lexemes, %d token types (%d tokens in total)" % (len(set(t[1] for t in tokenize("count = count + 1;"))), len(set(t[0] for t in tokenize("count = count + 1;"))) + 2, len(tokenize("count = count + 1;")))),
       ],
       traps=[("Strings and comments", "A string literal is one token; comments and whitespace produce no tokens."),
              ("Longest match", "Keywords listed first win ties; `ifx` is an identifier."),
              ("Syntax vs lexical errors", "Missing semicolon or bracket is a syntax error, not a lexical one."),
              ("Token vs lexeme", "Count tokens, not distinct lexemes, unless asked.")],
       quick=[("The output of the lexer is", ["parse tree", "tokens", "assembly", "symbol table"], 1, "A token stream."),
              ("Which rule resolves `>=` versus `>` `=`?", ["shortest match", "maximal munch", "alphabetical", "random"], 1, "Longest match wins."),
              ("A type mismatch is detected during", ["lexical analysis", "syntax analysis", "semantic analysis", "code generation"], 2, "Needs the symbol table."),
              ("Regular expressions are used to specify", ["grammar rules", "token patterns", "intermediate code", "types"], 1, "Lexical patterns.")],
       summary=["Phases: lexical, syntax, semantic, intermediate code, optimisation, code generation; front end vs back end.", "Lexeme = text, token = category, pattern = regular expression.", "Maximal munch with rule priority resolves ambiguity.",
                "Count tokens by longest matches; ignore whitespace/comments; strings are one token.", "Lex/Flex build a DFA scanner from regular expressions.", "Type errors are semantic; missing delimiters are syntax errors."])


# ======================================================================================================
lesson(subject=S, chapter="Front End", ch_no=1, no=2, slug="cd-top-down-parsing", title="Top-Down Parsing: FIRST, FOLLOW & LL(1)",
       topic="Parsing (LL & LR)", minutes=26, weight=6, widget="grammar",
       widget_hint="Paste a grammar to see FIRST, FOLLOW, the LL(1) table and conflicts. The presets include the expression grammar before and after removing left recursion.",
       key="A top-down parser builds the parse tree from the start symbol and predicts which production to use from the next input token. LL(1) parsers need FIRST and FOLLOW sets, a grammar free of left recursion and common prefixes, and one table cell per (non-terminal, terminal).",
       analogy=("🧭", "Reading a menu top-down", "You start with ‘a meal’ and decide which course to expand into, looking at just the next item on the order slip. If the next item is soup, the rule ‘Meal → Starter …’ is the only one that fits — a one-token look-ahead is enough, if the menu is designed so no two rules begin the same way."),
       sections=[
           dict(h="Recursive descent and left recursion", md="""**Recursive-descent** parsing writes one procedure per non-terminal. **Predictive** parsing needs no backtracking: the next token chooses the production.

Problems for top-down parsers:

- **Left recursion** A → Aα | β causes infinite recursion. Remove it: A → βA′, A′ → αA′ | ε. (Indirect left recursion needs ordering the non-terminals first.)
- **Common prefixes** A → αβ₁ | αβ₂ cannot be predicted. **Left-factor**: A → αA′, A′ → β₁ | β₂.

Example: E → E + T | T becomes E → T E′, E′ → + T E′ | ε."""),
           dict(h="FIRST and FOLLOW", md="""**FIRST(α)** = set of terminals that can begin a string derived from α (include ε if α ⇒* ε).
**FOLLOW(A)** = set of terminals that can appear immediately to the right of A in some sentential form; $ ∈ FOLLOW(start).

Rules:

1. FIRST(a) = {a}; FIRST(A) includes FIRST of the first symbol of each production; if that symbol is nullable continue with the next one; add ε if the whole right side is nullable.
2. For A → αBβ: FOLLOW(B) ⊇ FIRST(β) − {ε}; if β ⇒* ε (or is empty) then FOLLOW(B) ⊇ FOLLOW(A).
3. FOLLOW never contains ε.""",
                formulas=[("FOLLOW(B) ⊇ FIRST(β)∖{ε} for A → αBβ;  ⊇ FOLLOW(A) if β ⇒* ε", "the two FOLLOW rules")]),
           dict(h="LL(1) grammars and the parsing table", md="""Table construction: for each production A → α
- for every terminal a ∈ FIRST(α): put A → α in M[A, a];
- if ε ∈ FIRST(α): put A → α in M[A, b] for every b ∈ FOLLOW(A) (including $).

The grammar is **LL(1)** iff no cell has two productions; equivalently, for A → α | β: FIRST(α) ∩ FIRST(β) = ∅, at most one alternative derives ε, and if β ⇒* ε then FIRST(α) ∩ FOLLOW(A) = ∅.

Facts: an LL(1) grammar is **unambiguous** and not left-recursive; ambiguous grammars (the dangling else) are never LL(1); LL(1) ⊂ LR(1). The table-driven parser keeps a stack, pops the matching terminal or expands via the table; an error is an empty cell.""",
                call=[("tip", "Count entries", "A common question: how many non-empty entries does the LL(1) table have? Count one for each (A, terminal) pair created by each production, including the FOLLOW entries for ε-productions.")]),
           dict(h="Error recovery and LL(k)", md="""**Panic-mode** recovery discards tokens until a *synchronising* token (from FOLLOW sets) is found. **LL(k)** looks k tokens ahead; the LL(k) languages grow with k, but every LL(k) grammar is also LR(k). A grammar is LL(1) only after left recursion and left factoring have been dealt with."""),
       ],
       examples=[
           Ex("FIRST and FOLLOW of the expression grammar", "E → T X, X → + T X | ε, T → F Y, Y → * F Y | ε, F → ( E ) | id. Compute FOLLOW(E), FOLLOW(X), FOLLOW(T), FOLLOW(Y) and FOLLOW(F).",
              ["E is the start symbol and appears in F → ( E ): FOLLOW(E) = { $, ) }. X appears at the end of E → T X and X → + T X: FOLLOW(X) = FOLLOW(E) = { $, ) }.", "FOLLOW(T) = FIRST(X) − ε + FOLLOW(X) (X is nullable) = { +, $, ) }; Y is last in T → F Y: FOLLOW(Y) = FOLLOW(T) = { +, $, ) }.", "FOLLOW(F) = FIRST(Y) − ε + FOLLOW(Y) = { *, +, $, ) }."],
              "FOLLOW(E) = FOLLOW(X) = {$, )}; FOLLOW(T) = FOLLOW(Y) = {+, $, )}; FOLLOW(F) = {*, +, $, )}.", verify=lambda: "FOLLOW(E) = FOLLOW(X) = {$, )}; FOLLOW(T) = FOLLOW(Y) = {+, $, )}; FOLLOW(F) = {*, +, $, )}" if all(sorted(first_follow(EXPR_LL)[3][n]) == sorted(v) for n, v in {"E": "$)", "X": "$)", "T": "+$)", "Y": "+$)", "F": "*+$)"}.items()) else "mismatch"),
           Ex("LL(1) test", "Is S → i E t S | i E t S e S | a, E → b LL(1)?",
              ["Both S alternatives start with i, so FIRST sets are not disjoint ⇒ a conflict in M[S, i].", "Not LL(1) (it is the ambiguous dangling-else grammar)."],
              "**Not** LL(1).", verify=lambda: "Not" if not ref_ll1(*grammar("S -> i E t S | i E t S e S | a\nE -> b")) else "Is"),
           Ex("Number of table entries", "How many non-empty entries does the LL(1) table of the expression grammar E → T X, X → + T X | ε, T → F Y, Y → * F Y | ε, F → ( E ) | id have?",
              ["E → T X: FIRST = { (, id } ⇒ 2. X → + T X: 1; X → ε: FOLLOW(X) = { $, ) } ⇒ 2.", "T → F Y: 2. Y → * F Y: 1; Y → ε: FOLLOW(Y) = { +, $, ) } ⇒ 3. F → ( E ): 1; F → id: 1.", "Total = 2 + 1 + 2 + 2 + 1 + 3 + 1 + 1 = **13**."],
              "**13** entries.", verify=lambda: str(sum(len(f) for f in [first_follow(EXPR_LL)[2]["E"]])  # E row via FIRST only
                                                    + 1 + len(first_follow(EXPR_LL)[3]["X"]) + sum(len(first_follow(EXPR_LL)[2]["T"]) for _ in [0]) + 1 + len(first_follow(EXPR_LL)[3]["Y"]) + 1 + 1)),
       ],
       traps=[("Left recursion", "Top-down parsers loop forever on it; remove it before building the table."),
              ("FOLLOW with ε-productions", "ε ∈ FIRST(α) means you must also put entries under FOLLOW(A)."),
              ("FOLLOW(start) contains $", "Always include the end marker."),
              ("Ambiguity", "No ambiguous grammar is LL(1) (or LR(1)).")],
       quick=[("FOLLOW(S) of the start symbol always contains", ["ε", "$", "id", "nothing"], 1, "The end marker."),
              ("Left recursion is removed by", ["left factoring", "introducing a new non-terminal A′", "adding ε", "making it ambiguous"], 1, "A → βA′, A′ → αA′ | ε."),
              ("An LL(1) grammar can be", ["ambiguous", "left-recursive", "neither", "both"], 2, "Neither."),
              ("To fill ε-productions in the LL(1) table we use", ["FIRST", "FOLLOW", "LAST", "PREFIX"], 1, "FOLLOW(A).")],
       summary=["Predictive parsers need no backtracking: eliminate left recursion, left-factor.", "FIRST: starting terminals (+ε); FOLLOW: terminals that can follow (+$ for start).", "Table: FIRST(α) entries; if α nullable add FOLLOW(A).",
                "LL(1) ⇒ unambiguous, not left-recursive; each cell has at most one production.", "LL(1) ⊂ LR(1); LL(k) ⊂ LR(k).", "Panic-mode recovery uses FOLLOW sets."])


# ======================================================================================================
lesson(subject=S, chapter="Front End", ch_no=1, no=3, slug="cd-bottom-up-parsing", title="Bottom-Up Parsing: LR(0), SLR, LALR & LR(1)",
       topic="Parsing (LL & LR)", minutes=26, weight=7, widget="grammar",
       widget_hint="The tool builds the LR(0) automaton for any grammar and reports its number of states and whether it is SLR(1). Try the ‘Not SLR(1)’ preset.",
       key="Bottom-up (shift–reduce) parsers build the tree from the leaves by reducing handles. LR parsers use a DFA over LR items; the family LR(0) ⊂ SLR(1) ⊂ LALR(1) ⊂ LR(1) differs in how lookahead is used to resolve shift–reduce and reduce–reduce conflicts.",
       analogy=("🧱", "Assembling bricks into a wall", "A bottom-up parser holds a pile of already-recognised pieces (the stack). When the top of the pile matches the right side of a rule — a handle — it replaces them with the rule's left side. Deciding whether to keep shifting new bricks or to reduce is the whole difficulty; lookahead tells it which."),
       sections=[
           dict(h="Shift–reduce parsing", md="""A shift–reduce parser has a **stack** and an **input buffer**. Actions: **shift** (move next token to the stack), **reduce** by A → β (pop β, push A), **accept**, **error**. It builds a **rightmost derivation in reverse**. The substring reduced at each step is the **handle**; the stack contents are **viable prefixes**.

Conflicts: **shift–reduce** (can't decide whether to shift or reduce) and **reduce–reduce** (two completed productions possible). Operator-precedence parsers resolve them using precedence/associativity tables (they work on operator grammars with no ε or adjacent non-terminals)."""),
           dict(h="LR items and the canonical collection", md="""An **LR(0) item** is a production with a dot: A → α·β. The **closure** of a set adds B → ·γ for each item with a non-terminal B after the dot; **goto(I, X)** moves the dot over X and takes the closure. The **canonical collection** of LR(0) item sets, starting from the augmented production S′ → S, is the set of DFA states of the parser.

- Items with the dot at the end (A → α·) are *reduce* items; an item with a terminal after the dot is a *shift* item.
- For the expression grammar E → E + T | T, T → T * F | F, F → ( E ) | id the LR(0) automaton has **12 states**; for S → A A, A → a A | b it has **7**.""",
                call=[("tip", "State count", "Do not forget the augmented grammar S′ → S: state I₀ includes S′ → ·S and the accept item S′ → S· appears in a state of its own.")]),
           dict(h="LR(0), SLR(1), LALR(1), CLR(1)", md="""| Parser | Reduce A → α when… | Power |
|---|---|---|
| **LR(0)** | the state contains A → α· (no lookahead) | weakest |
| **SLR(1)** | next token ∈ **FOLLOW(A)** | stronger |
| **LALR(1)** | next token ∈ the **LR(1) lookahead** of the merged state | between SLR and CLR |
| **CLR / LR(1)** | next token ∈ the exact lookahead for this item | strongest |

- **LALR** merges LR(1) states having the same core; it has the **same number of states as LR(0)/SLR**, while CLR(1) can have many more. Merging can introduce *reduce–reduce* conflicts, never shift–reduce ones that weren't already in the CLR table.
- Strictly: LR(0) ⊂ SLR(1) ⊂ LALR(1) ⊂ LR(1); every LL(1) grammar is LR(1) but not necessarily SLR(1) or LALR(1).
- LR parsers handle left recursion directly and a larger class of languages (all deterministic CFLs) than LL parsers.
- **YACC/Bison** generate LALR(1) parsers and resolve conflicts by precedence declarations, shift preferred over reduce, and earlier rule for reduce–reduce."""),
           dict(h="Constructing a parsing table", md="""ACTION[state, terminal] ∈ {shift j, reduce r, accept, error}; GOTO[state, non-terminal] = state.

- If A → α·aβ is in I and goto(I, a) = J: ACTION[I, a] = shift J.
- If A → α· (A ≠ S′) is in I: for **SLR**, ACTION[I, a] = reduce A → α for all a ∈ FOLLOW(A); for LR(1) use the item's lookahead set; for LR(0), all terminals.
- S′ → S· on $ gives accept.

A cell with two actions is a conflict, so the grammar is not of that class. The classic grammar S → L = R | R, L → * R | id, R → L is **not SLR(1)**: in the state with S → L·= R and R → L·, '=' ∈ FOLLOW(R) leads to a shift–reduce conflict, though it is LR(1)."""),
       ],
       examples=[
           Ex("LR(0) states", "How many states does the LR(0) automaton of E → E + T | T, T → T * F | F, F → ( E ) | id have (augmented grammar)?",
              ["Starting from I₀ = closure(E′ → ·E), the collection contains states for goto on E, T, F, (, id, +, * and the subsequent combinations.", "The well-known count is **12** states (I₀ … I₁₁)."],
              "**12** states.", verify=lambda: str(len(ref_lr0(*grammar(EXPR_LR))[1]))),
           Ex("Another count", "How many LR(0) states does S → A A, A → a A | b have?",
              ["The augmented grammar S′ → S gives I₀; goto on S, A, a, b generate the remaining sets; states from `A → a·A` and `A → b·` repeat across contexts.", "Total = **7** states (a standard textbook example)."],
              "**7** states.", verify=lambda: str(len(ref_lr0(*grammar(SAA))[1]))),
           Ex("Is it SLR(1)?", "Is S → L = R | R, L → * R | id, R → L SLR(1)?",
              ["FOLLOW(R) = { =, $ } because R can end L and L is followed by = in S → L = R.", "The state containing S → L·= R and R → L· has a shift on '=' and a reduce on '=' (since '=' ∈ FOLLOW(R)) ⇒ shift–reduce conflict ⇒ **not SLR(1)** (but LR(1))."],
              "**Not** SLR(1).", verify=lambda: "Not" if not ref_slr(*grammar(LR_CLASSIC)) else "Is"),
           Ex("SLR for the expression grammar", "Is E → E + T | T, T → T * F | F, F → ( E ) | id SLR(1)?",
              ["The only state with a possible conflict, E → E·+ T together with E′ → E·, resolves because the reduce on $ and shift on + use different symbols; the others are conflict-free.", "Yes, it is SLR(1) (and hence LALR(1) and LR(1))."],
              "**Yes**, SLR(1).", verify=lambda: "Yes" if ref_slr(*grammar(EXPR_LR)) else "No"),
       ],
       traps=[("Hierarchy", "LR(0) ⊂ SLR ⊂ LALR ⊂ LR(1); LALR has the same number of states as SLR/LR(0)."),
              ("LALR conflicts", "Merging can add reduce–reduce conflicts, never shift–reduce."),
              ("Handle", "Reduce the leftmost simple phrase of the rightmost derivation in reverse — not just any matching right side."),
              ("Augmented production", "Always count the S′ → S state(s) in the LR(0) automaton.")],
       quick=[("Which parser uses FOLLOW sets to place reduce actions?", ["LR(0)", "SLR(1)", "CLR(1)", "LL(1)"], 1, "SLR."),
              ("LALR(1) has the same number of states as", ["CLR(1)", "LR(0)", "LL(1)", "operator precedence"], 1, "States with the same core are merged."),
              ("A shift–reduce parser builds", ["a leftmost derivation", "a rightmost derivation in reverse", "a leftmost derivation in reverse", "a random derivation"], 1, "Rightmost reversed."),
              ("YACC generates", ["LL(1) parsers", "LALR(1) parsers", "recursive descent parsers", "SLR(0) parsers"], 1, "LALR(1).")],
       summary=["Shift–reduce: shift, reduce, accept, error; handle = reducible substring; produces a rightmost derivation in reverse.", "LR items A → α·β; closure + goto give the automaton; augment with S′ → S.", "LR(0): reduce always; SLR: FOLLOW(A); LALR: merged lookaheads; CLR: exact lookaheads.",
                "LR(0) ⊂ SLR ⊂ LALR ⊂ LR(1); LALR states = LR(0) states.", "Merging LR(1) states may create reduce–reduce conflicts only.", "YACC = LALR(1) with precedence-based conflict resolution."])
