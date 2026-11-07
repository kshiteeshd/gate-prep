"""Textbook-style long-form teaching text: Theory of Computation and Compiler Design."""
from learn import elab

elab("toc-finite-automata",
 ("Machines that recognise languages", """
In this subject a **language** is simply a set of strings over an **alphabet** $\\Sigma$ (a finite set of symbols, such as $\\{0,1\\}$). The question "is this string in the language?" is a yes/no question, and an **automaton** is a very simple machine that answers it by reading the string one symbol at a time.

A **deterministic finite automaton (DFA)** has a finite set of **states**, a **start state**, a set of **accepting (final) states**, and a **transition** rule: in each state, on each symbol, exactly one next state. The machine starts in the start state, follows the transitions for each input symbol, and accepts if it ends in an accepting state. It has no memory apart from which state it is in, which is why DFAs can only recognise simple languages.
"""),
 ("Designing a DFA", """
The trick is to decide what **information each state must remember**. For "binary strings with an even number of 1s" two states are enough: *even so far* and *odd so far*. For "strings ending in 01" you must remember how much of the pattern you have just seen: nothing, a 0, or 01. For "binary numbers divisible by 3", remember the remainder modulo 3 (three states): reading a bit $b$ in remainder $r$ moves to $(2r+b)\\bmod3$.

A **dead (trap) state** absorbs strings that can no longer be accepted. Always check that every state has a transition on every symbol.
"""),
 ("NFAs and equivalence", """
A **nondeterministic finite automaton (NFA)** may have several (or no) transitions for a symbol, and may have **$\\varepsilon$-transitions** that move without reading input. It accepts if **some** sequence of choices leads to an accepting state. NFAs are often much easier to design.

Yet NFAs recognise exactly the same languages as DFAs. The **subset construction** converts an NFA with $n$ states into a DFA whose states are *sets* of NFA states; in the worst case it needs $2^n$ states. The languages recognised are called **regular languages**.

**Minimising a DFA** merges states that no string can tell apart. Start by separating accepting from non-accepting states and keep splitting groups until the transitions agree; the number of resulting groups is the minimum number of states.
"""),
)

elab("toc-regular-expressions",
 ("Describing languages with expressions", """
A **regular expression** describes a language using three operations on strings:

- **Union** $r+s$ (or $r|s$): a string from either language.
- **Concatenation** $rs$: a string from $r$ followed by one from $s$.
- **Kleene star** $r^*$: zero or more repetitions of strings from $r$.

Base cases: $\\emptyset$ (no strings), $\\varepsilon$ (only the empty string) and a single symbol $a$. For example $(0+1)^*01$ describes all binary strings that end in 01, and $a^*b^*$ describes any number of $a$s followed by any number of $b$s.
"""),
 ("Regular expressions and automata are equivalent", """
**Theorem (Kleene):** a language is described by a regular expression if and only if it is accepted by a finite automaton.

*Expression → NFA* (Thompson's construction): build a small NFA for each symbol and combine them for union, concatenation and star.

*DFA → expression* (state elimination, or Arden's rule): to solve equations of the form $R=Q+RP$ where $P$ does not contain $\\varepsilon$, the solution is $R=QP^*$. Write one equation per state, then solve step by step.

**Useful identities:** $(a^*)^*=a^*$, $(a+b)^*=(a^*b^*)^*$, $\\varepsilon r=r$, $\\emptyset r=\\emptyset$, $r+r=r$, $(r^*)^+=r^*$.
"""),
 ("Languages that are not regular", """
A finite automaton cannot count without limit. The language $\\{0^n1^n:n\\ge0\\}$ needs to remember how many 0s were seen, which requires unlimited memory; so it is **not regular**. The same goes for balanced parentheses and for $\\{ww:w\\in\\{a,b\\}^*\\}$.

To *prove* a language is not regular, use the **pumping lemma** (next lessons), or show that closure properties would force it to be regular.
"""),
)

elab("toc-cfg-pda",
 ("Going beyond regular languages", """
Regular languages cannot express nesting, like matching brackets. **Context-free grammars (CFGs)** can. A grammar has **variables** (non-terminals), **terminals** (the actual symbols), a **start variable**, and **production rules** that rewrite a variable into a string of variables and terminals. For instance

$$S\\to aSb\\mid\\varepsilon$$

generates $\\{a^nb^n:n\\ge0\\}$: each use of $S\\to aSb$ adds one $a$ on the left and one $b$ on the right.
"""),
 ("Derivations, parse trees and ambiguity", """
A **derivation** applies rules starting from $S$ until only terminals remain. A **parse tree** shows the structure; a **leftmost derivation** always expands the leftmost variable. A grammar is **ambiguous** if some string has two different parse trees (equivalently two leftmost derivations). The classic example is $E\\to E+E\\mid E*E\\mid id$, where $id+id*id$ can be grouped two ways. Ambiguity is removed by encoding precedence and associativity into the grammar. Some languages are **inherently ambiguous**: every grammar for them is ambiguous.

A **normal form** such as **Chomsky normal form** (rules $A\\to BC$ or $A\\to a$) is useful for algorithms and proofs: in CNF, a string of length $n$ is derived in exactly $2n-1$ steps.
"""),
 ("Pushdown automata", """
A **pushdown automaton (PDA)** is an NFA with a **stack**. Transitions can push and pop symbols, so the machine can count and match: to recognise $a^nb^n$ push a symbol for each $a$ and pop one for each $b$; accept if the stack is empty at the end.

Context-free languages are exactly the languages accepted by PDAs. **Deterministic** PDAs are strictly weaker than non-deterministic ones: for example, palindromes $\\{ww^R\\}$ need non-determinism (the machine must *guess* the middle).
"""),
)

elab("toc-closure-pumping",
 ("Closure properties", """
A class of languages is **closed** under an operation if applying the operation to members always gives a member. Closure properties are used both to build new languages and to prove that some language is not in a class.

- **Regular languages** are closed under union, intersection, complement, difference, concatenation, star, reversal and homomorphism.
- **Context-free languages** are closed under union, concatenation, star and reversal, but **not** under intersection or complement. (The intersection of two CFLs with a regular language is context-free.)
- **Deterministic CFLs** are closed under complement but not union or intersection.
"""),
 ("The pumping lemma for regular languages", """
**Statement.** If $L$ is regular, there is a **pumping length** $p$ such that every string $s\\in L$ with $|s|\\ge p$ can be written $s=xyz$ with (1) $|xy|\\le p$, (2) $|y|\\ge1$, and (3) $xy^iz\\in L$ for every $i\\ge0$.

**Why it is true.** Reading $p$ symbols passes through $p+1$ states of a DFA with only $p$ states, so some state repeats; the part of the string read between the two visits can be repeated any number of times.

**How to use it (a game).** To prove $L$ is *not* regular: assume it is regular with pumping length $p$. *You* choose a string $s\\in L$ of length at least $p$ (cleverly, in terms of $p$). The adversary splits it $s=xyz$ in any way allowed by (1) and (2). You show some $i$ (often 0 or 2) makes $xy^iz\\notin L$. For $\\{0^n1^n\\}$ take $s=0^p1^p$: since $|xy|\\le p$, $y$ is all 0s, and pumping changes the number of 0s but not 1s.
"""),
 ("Pumping for context-free languages", """
The CFL pumping lemma splits $s=uvxyz$ with $|vxy|\\le p$, $|vy|\\ge1$ and $uv^ixy^iz\\in L$ for all $i\\ge0$ — two parts are pumped *together*. It shows that $\\{a^nb^nc^n\\}$ is not context-free: any window $vxy$ of length at most $p$ can touch at most two of the three kinds of symbols, so pumping unbalances the counts. Remember that the lemma can only **disprove**; satisfying it proves nothing.
"""),
)

elab("toc-turing-decidability",
 ("The Turing machine", """
A **Turing machine (TM)** has a finite control and an **infinite tape** of cells, with a head that reads a symbol, writes a symbol, and moves left or right. Unlike a PDA, it can read the tape repeatedly and change it, which makes it as powerful as any computer. The **Church–Turing thesis** says that anything that can be computed by an algorithm can be computed by a Turing machine.

A TM can **accept** (halt in an accepting state), **reject**, or **loop forever**. A language is **recursively enumerable (RE)** if some TM accepts exactly its strings (it may loop on others), and **recursive (decidable)** if some TM *halts* on every input with the right answer.
"""),
 ("Decidable and undecidable problems", """
A problem is **decidable** if an algorithm always halts with a yes or no. Decidable examples: does a DFA accept a string? Is the language of a DFA empty? Are two DFAs equivalent? Is the language of a CFG empty?

The **halting problem** — given a program and its input, does it halt? — is **undecidable**. The proof is by contradiction: if a program $H(P,x)$ decided halting, build $D(P)$ that runs $H(P,P)$ and does the *opposite*; then $D(D)$ halts exactly when it does not, a contradiction.

**Rice's theorem:** every non-trivial question about *what a program computes* (is its language empty? finite? regular?) is undecidable. Undecidability is proved by **reduction**: if a known undecidable problem reduces to $X$, then $X$ is undecidable.
"""),
 ("The Chomsky hierarchy", """
The language classes nest inside each other:

| Type | Language class | Machine | Grammar |
|---|---|---|---|
| 3 | Regular | Finite automaton | $A\\to aB$, $A\\to a$ |
| 2 | Context-free | Pushdown automaton | $A\\to\\alpha$ |
| 1 | Context-sensitive | Linear-bounded automaton | $\\alpha\\to\\beta$ (right side never shorter) |
| 0 | Recursively enumerable | Turing machine | any |

Between types 1 and 0 lie the **recursive (decidable)** languages. Each step up gains power but loses decidability of questions like emptiness and equivalence.
"""),
)

# ---------------------------------------------------------------- Compiler design
elab("cd-phases-lexical",
 ("What a compiler does", """
A **compiler** translates a program written in a high-level language into machine code. Because the task is large it is split into **phases**, each transforming the program into a different representation:

1. **Lexical analysis** — group characters into **tokens** (keywords, identifiers, numbers, operators).
2. **Syntax analysis (parsing)** — check the tokens form a valid program according to the grammar and build a **parse tree**.
3. **Semantic analysis** — check meaning: types match, variables are declared.
4. **Intermediate code generation** — produce a machine-independent form such as three-address code.
5. **Optimisation** — improve the code.
6. **Code generation** — produce target code.

The **symbol table** and the **error handler** serve all phases. The first three phases are the **front end**; the last ones form the **back end**.
"""),
 ("Lexical analysis in detail", """
The **lexer** reads characters and outputs tokens. A token is a pair of a **token name** and (optionally) an **attribute** (for an identifier, a pointer to its symbol-table entry). The text matching a token is a **lexeme**. Token patterns are written as regular expressions and implemented with a DFA.

Two rules decide ambiguous cases: **longest match** (`>=` is one token, not `>` then `=`) and, among equal-length matches, **priority** (a keyword like `if` beats the identifier pattern). The lexer also discards whitespace and comments. A common exam question counts the number of tokens in a line of code.
"""),
)

elab("cd-top-down-parsing",
 ("Parsing from the top", """
A **top-down parser** starts at the start symbol and tries to derive the input by expanding non-terminals from the left. A **recursive-descent** parser has one function per non-terminal. The problem is deciding *which production to use*, and the **predictive (LL(1)) parser** solves it by looking at one input symbol.

Two problems must be removed first: **left recursion** ($A\\to A\\alpha\\mid\\beta$ makes the parser loop forever; rewrite as $A\\to\\beta A'$, $A'\\to\\alpha A'\\mid\\varepsilon$) and **common prefixes** (**left factoring**).
"""),
 ("FIRST and FOLLOW", """
$\\mathrm{FIRST}(\\alpha)$ is the set of terminals that can begin a string derived from $\\alpha$ (plus $\\varepsilon$ if $\\alpha$ can vanish). $\\mathrm{FOLLOW}(A)$ is the set of terminals that can appear immediately after $A$ in some derivation (the end-of-input marker belongs to the FOLLOW set of the start symbol).

Rules for FOLLOW: for a production $A\\to\\alpha B\\beta$, add $\\mathrm{FIRST}(\\beta)\\setminus\\{\\varepsilon\\}$ to $\\mathrm{FOLLOW}(B)$; and if $\\beta$ can vanish (or is empty), add $\\mathrm{FOLLOW}(A)$ to $\\mathrm{FOLLOW}(B)$.
"""),
 ("The LL(1) table", """
Build the **parsing table** $M[A,a]$: for each production $A\\to\\alpha$, put it in $M[A,a]$ for every terminal $a\\in\\mathrm{FIRST}(\\alpha)$; and if $\\varepsilon\\in\\mathrm{FIRST}(\\alpha)$, also for every $a\\in\\mathrm{FOLLOW}(A)$. A grammar is **LL(1)** exactly when no table cell has more than one production. An ambiguous or left-recursive grammar is never LL(1). The parser uses a stack: match terminals, and replace a non-terminal on top by the right-hand side chosen from the table.
"""),
)

elab("cd-bottom-up-parsing",
 ("Parsing from the bottom", """
A **bottom-up parser** starts from the input and repeatedly **reduces** substrings that match the right-hand side of a production to its left-hand side, working back to the start symbol. This traces a **rightmost derivation in reverse**. The usual technique is **shift–reduce parsing**: a stack holds symbols; **shift** moves the next input symbol onto the stack, and **reduce** replaces a **handle** (a right-hand side on top of the stack) by its non-terminal.

Bottom-up parsers handle a larger class of grammars than top-down ones, including left-recursive grammars.
"""),
 ("LR parsers", """
An **LR(k)** parser reads the input left to right, produces a rightmost derivation in reverse, and uses $k$ lookahead symbols. It is driven by a table of **actions** (shift, reduce, accept) and **gotos**, built from sets of **items** like $A\\to\\alpha\\cdot\\beta$ (a dot marks how much of the rule has been seen). The family, from least to most powerful: **LR(0)** $\\subset$ **SLR(1)** $\\subset$ **LALR(1)** $\\subset$ **CLR(1)** (canonical LR). They differ in how they decide when to reduce: LR(0) reduces whenever possible; SLR uses FOLLOW sets; CLR uses precise lookaheads in each item. LALR merges CLR states with identical cores, giving the same size of tables as SLR but more power.
"""),
 ("Conflicts", """
A **shift–reduce conflict** means the parser cannot decide between shifting and reducing; a **reduce–reduce conflict** means two reductions apply. Ambiguous grammars always produce conflicts in LR tables. LR(0) and SLR may report conflicts that CLR avoids. Every LL(1) grammar is LR(1), but not the other way round.
"""),
)

elab("cd-syntax-directed",
 ("Attaching meaning to syntax", """
Parsing only tells us the sentence is well formed. To compute something — a value, a type, generated code — we attach **semantic rules** to grammar productions. This is **syntax-directed translation (SDT)**. Each grammar symbol can carry **attributes**.

A **synthesised** attribute of a node is computed from the attributes of its children (information flows up); an **inherited** attribute is computed from the parent and siblings (information flows down or sideways). A definition using only synthesised attributes is **S-attributed** and can be evaluated during bottom-up parsing; an **L-attributed** definition allows inherited attributes that depend only on the left siblings, which suits top-down evaluation.
"""),
 ("Evaluating an SDT", """
For the grammar $E\\to E_1+T$ with rule $E.val=E_1.val+T.val$, the value of a node is computed after its children. To evaluate, build the parse tree, then compute attributes in an order that respects dependencies (the **dependency graph** must be acyclic). Typical exam questions give an SDT with actions like `print` and ask for the output on a given input: remember that actions placed at the *end* of a production run after the children are reduced (post-order), and actions in the middle run when the parser reaches that point.
"""),
)

elab("cd-intermediate-runtime",
 ("Intermediate code", """
**Three-address code** breaks expressions into simple steps of at most one operator, using temporaries: $a=b+c*d$ becomes `t1 = c * d; t2 = b + t1; a = t2`. It can be stored as **quadruples** (op, arg1, arg2, result), **triples** (no result field; refer to instruction numbers), or **indirect triples**. A **syntax tree** or **DAG** shows the structure and lets us reuse common subexpressions.
"""),
 ("Runtime environment", """
When the program runs, each function call creates an **activation record (stack frame)** holding its parameters, local variables, return address and saved registers; the frames live on a **stack**. **Static scope** resolves names by the program text; **dynamic scope** resolves them by the call chain. Parameter passing: **call by value** (copy), **call by reference** (the address), **call by name** (re-evaluate the expression each use).

**Basic blocks** are straight-line code with a single entry and exit; a **control-flow graph** connects them. A **leader** is the first instruction of a block: the first instruction, any jump target, and any instruction following a jump.
"""),
)

elab("cd-optimization-dataflow",
 ("Making code faster", """
**Optimisation** transforms code to run faster or use less space *without changing its meaning*. Common machine-independent optimisations: **constant folding** (compute `2*3` at compile time), **constant propagation**, **common subexpression elimination**, **dead-code elimination**, **strength reduction** (replace `x*2` by `x<<1`), and **loop optimisations** such as code motion (move invariant computation out of the loop) and induction-variable elimination.
"""),
 ("Data-flow analysis", """
To optimise safely, the compiler must know facts about how values flow. **Data-flow analysis** computes, for each basic block $B$, sets $\\mathrm{IN}[B]$ and $\\mathrm{OUT}[B]$ using the equations

$$\\mathrm{OUT}[B]=\\mathrm{gen}[B]\\cup(\\mathrm{IN}[B]-\\mathrm{kill}[B])$$

with a rule for combining predecessors, solved by iteration until nothing changes. **Reaching definitions** (forward, union), **available expressions** (forward, intersection) and **live variables** (backward, union) are the three classic analyses. A variable is **live** at a point if its current value may be used later; live-variable information drives dead-code elimination and register allocation.
"""),
 ("Register allocation", """
Registers are few and fast. **Register allocation** assigns variables to registers and spills the rest to memory. The **interference graph** has a node per variable and an edge between variables live at the same time; assigning registers is then **graph colouring** with $k$ colours (for $k$ registers). A graph needs at least as many colours as the size of its largest clique.
"""),
)
