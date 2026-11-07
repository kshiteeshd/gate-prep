"""Compiler Design part 2: syntax-directed translation, intermediate code & runtime, optimisation & data flow."""
import ast
import itertools

from learn import Ex, lesson

S = "CD"


def value_numbering(expr):
    """number of distinct operator nodes in the DAG of an arithmetic expression (common sub-expressions shared)"""
    seen = {}

    def go(n):
        if isinstance(n, ast.Name):
            return n.id
        if isinstance(n, ast.Constant):
            return repr(n.value)
        if isinstance(n, ast.BinOp):
            key = (type(n.op).__name__, go(n.left), go(n.right))
            seen.setdefault(key, len(seen))
            return "t%d" % seen[key]
        if isinstance(n, ast.UnaryOp):
            key = (type(n.op).__name__, go(n.operand))
            seen.setdefault(key, len(seen))
            return "t%d" % seen[key]
        raise ValueError
    go(ast.parse(expr, mode="eval").body)
    return len(seen)


def tree_operators(expr):
    return sum(1 for n in ast.walk(ast.parse(expr, mode="eval")) if isinstance(n, (ast.BinOp, ast.UnaryOp)))


def leaders(code, jumps):
    """code: list of instruction strings; jumps: {index: target index (0-based)}; conditional/unconditional both listed"""
    L = {0}
    for i, t in jumps.items():
        L.add(t)
        if i + 1 < len(code):
            L.add(i + 1)
    return sorted(L)


def call(mode):
    """f(x, y) { x = x + 1; y = y + x }  called as f(a, a) with a = 2"""
    a = [2]
    if mode == "value":
        x, y = a[0], a[0]
        x = x + 1
        y = y + x
        return a[0]
    # reference: x and y alias a
    a[0] = a[0] + 1
    a[0] = a[0] + a[0]
    return a[0]


def liveness(blocks, succ):
    """blocks: {name: (use set, def set)}; returns live-in sets by fixpoint"""
    live_in = {b: set() for b in blocks}
    live_out = {b: set() for b in blocks}
    ch = True
    while ch:
        ch = False
        for b, (use, dfn) in blocks.items():
            out = set().union(*[live_in[s] for s in succ[b]]) if succ[b] else set()
            inn = use | (out - dfn)
            if out != live_out[b] or inn != live_in[b]:
                live_out[b], live_in[b] = out, inn
                ch = True
    return live_in, live_out


def chromatic(n, edges):
    for k in range(1, n + 1):
        for col in itertools.product(range(k), repeat=n):
            if all(col[a] != col[b] for a, b in edges):
                return k
    return n


# ======================================================================================================
lesson(subject=S, chapter="Semantics & Back End", ch_no=2, no=1, slug="cd-syntax-directed", title="Syntax-Directed Translation & Attribute Grammars",
       topic="Syntax-Directed Translation", minutes=22, weight=4, widget="grammar",
       widget_hint="Use the grammar tool to study how a grammar is parsed; then compute attributes by hand on the parse tree following the examples.",
       key="A syntax-directed definition attaches attributes and semantic rules to grammar symbols. Synthesized attributes flow up the tree, inherited attributes flow down or sideways; S-attributed definitions evaluate in bottom-up parsers, L-attributed ones in a single left-to-right pass.",
       analogy=("🧮", "Adding up a receipt", "Each line item knows its own price. A sub-total is computed from the lines beneath it, and the grand total from the sub-totals — information flows upward from the leaves. A tax rate that is printed at the top and used by every line is information flowing downward. Syntax-directed translation is the same bookkeeping attached to a parse tree."),
       sections=[
           dict(h="Attributes and definitions", md="""A **syntax-directed definition (SDD)** associates each grammar symbol with attributes and each production with semantic rules.

- **Synthesized attribute:** computed from the attributes of the node's **children** (e.g. `E.val = E₁.val + T.val`).
- **Inherited attribute:** computed from the node's **parent and/or left siblings** (e.g. the declared type passed down a declaration list).
- **S-attributed:** only synthesized attributes — evaluated by a bottom-up parser during reductions (works with LR parsing; the value stack holds the attributes).
- **L-attributed:** each inherited attribute depends only on the parent and the siblings to its **left**; evaluated in one depth-first left-to-right traversal, compatible with LL parsing. Every S-attributed definition is L-attributed.

An **annotated parse tree** shows attribute values at every node. If the dependency graph has a cycle the SDD is circular; checking for circularity is decidable but exponential."""),
           dict(h="Syntax-directed translation schemes", md="""A **translation scheme (SDT)** embeds *semantic actions* inside productions in `{ }` at specific positions. In an LR parser, actions at the **end** of a production run on reduction; for L-attributed definitions, actions that use inherited attributes are placed immediately before the symbol they need.

Typical uses: expression evaluation, building syntax trees, **postfix translation**, converting infix to postfix, type checking, generating three-address code, filling the symbol table from declarations (`D → T L`, `L.in = T.type`).

Postfix of `a + b * c` is `a b c * +`; prefix is `+ a * b c`."""),
           dict(h="Evaluating on a parse tree", md="""Procedure: draw the parse tree, then evaluate attributes in an order that respects dependencies — for synthesized attributes, post-order. The number of **reductions** equals the number of internal nodes; with an LR parser every reduction can print or compute something.

For `E → E + T | T, T → T * F | F, F → num`, the input `3 + 4 * 5` is parsed with the shifts and reduces determined by precedence encoded in the grammar (`*` binds tighter), giving value 23. Executing a semantic action printing the operator after its operands produces postfix `3 4 5 * +`.""",
                call=[("tip", "Counting actions", "If every production has an action that prints something, the number of outputs equals the number of reductions in the parse (one per production used).")]),
           dict(h="Type checking and the symbol table", md="""Semantic analysis uses a **symbol table** (hash table of identifier → type, scope, offset). Type checking: each expression gets a type attribute; operators check operand compatibility; **type coercion** inserts implicit conversions (int → float). **Static scoping** resolves names by the program text (most languages); **dynamic scoping** by the call chain — the same program can print different values under the two rules."""),
       ],
       examples=[
           Ex("Synthesized attribute", "For E → E₁ + T {E.val = E₁.val + T.val}, T → T₁ * F {T.val = T₁.val * F.val}, F → num, what is E.val for input 3 + 4 * 5 and how many reductions occur?",
              ["The tree is E(E(T(F(3))) + T(T(F(4)) * F(5))): evaluating T = 4 * 5 = 20, E = 3 + 20 = 23.", "Reductions: F→num ×3, T→F ×2 (for 3 and 4), T→T*F ×1, E→T ×1, E→E+T ×1 = 3 + 2 + 1 + 1 + 1 = **8**."],
              "E.val = **23**; **8** reductions.", verify=lambda: "E.val = %d; %d reductions" % (eval("3+4*5"), 3 + 2 + 1 + 1 + 1)),
           Ex("Postfix translation", "A translation scheme prints the operator after both operands. What is the output for 2 * 3 + 4 * 5?",
              ["Postfix of (2*3) + (4*5) is 2 3 * 4 5 * +.", "Evaluating gives 6 + 20 = 26."],
              "`2 3 * 4 5 * +` (value 26)", verify=lambda: "`2 3 * 4 5 * +` (value %d)" % eval("2*3+4*5")),
           Ex("Static versus dynamic scope", "int x = 10; void f() { print(x); } void g() { int x = 20; f(); } main() { g(); }. What does f print under static and under dynamic scoping?",
              ["Static scoping: f's x refers to the global x declared where f is defined ⇒ 10.", "Dynamic scoping: f uses the most recent binding in the call chain, g's x ⇒ 20."],
              "Static **10**, dynamic **20**.", verify=lambda: "Static %d, dynamic %d" % (10, 20)),
       ],
       traps=[("Synthesized vs inherited", "Synthesized flows from children up; inherited from parent or left siblings."),
              ("S-attributed ⊂ L-attributed", "Every S-attributed SDD is also L-attributed."),
              ("Action placement", "An action using an inherited attribute of a symbol must come before that symbol."),
              ("Static vs dynamic scope", "Output differs only when a non-local name is resolved in different environments.")],
       quick=[("Which attributes can a bottom-up (LR) parser evaluate easily?", ["only inherited", "synthesized (S-attributed)", "none", "circular ones"], 1, "S-attributed."),
              ("Inherited attributes depend on", ["only children", "parent and left siblings", "right siblings", "nothing"], 1, "For L-attributed definitions."),
              ("Postfix of a + b * c is", ["a b c * +", "a b + c *", "+ a * b c", "a + b c *"], 0, "Operands first."),
              ("Type coercion is", ["a syntax error", "an implicit type conversion", "a loop optimisation", "register allocation"], 1, "int → float.")],
       summary=["Attributes: synthesized (children → parent), inherited (parent/left siblings).", "S-attributed ⊂ L-attributed; S-attributed works with LR parsing.", "SDT embeds actions; end-of-production actions run at reduction.",
                "Evaluate on the annotated parse tree; the number of reductions equals the number of internal nodes.", "Symbol table stores names, types, scopes; type checking adds coercions.", "Static scoping resolves non-locals lexically, dynamic by the call chain."])


# ======================================================================================================
lesson(subject=S, chapter="Semantics & Back End", ch_no=2, no=2, slug="cd-intermediate-runtime", title="Intermediate Code & Run-Time Environments",
       topic="Intermediate Code & Runtime", minutes=24, weight=5, widget="none",
       key="Intermediate representations (syntax trees, DAGs, three-address code) decouple the front end from the back end. Run-time support organises memory into code, static data, heap and stack with activation records, and defines parameter-passing modes.",
       analogy=("🏗️", "Blueprints before bricks", "An architect draws a neutral blueprint (intermediate code) that any builder (target machine) can follow. On site, each task (function call) gets its own temporary workspace (activation record) on a stack of workspaces; when it finishes the workspace is cleared."),
       sections=[
           dict(h="Three-address code and its representations", md="""**Three-address code (TAC)** has at most three addresses per instruction: `x = y op z`, `x = op y`, `x = y`, `goto L`, `if x relop y goto L`, `param x`, `call p, n`, `return x`, array and pointer forms `x = y[i]`, `x[i] = y`.

| Representation | Stores |
|---|---|
| **Quadruples** | (op, arg1, arg2, result) — 4 fields, easy to reorder |
| **Triples** | (op, arg1, arg2) — results referred to by instruction position, harder to move |
| **Indirect triples** | a list of pointers to triples — allows reordering |

For `a = b * c + b * c`: the tree/quadruple form needs **4 instructions** (two multiplications, one add, one assignment); using a **DAG** (common sub-expression shared) needs **3**: t1 = b * c; t2 = t1 + t1; a = t2. A DAG for an expression has one node per distinct operator/operand combination."""),
           dict(h="Control flow and boolean expressions", md="""Boolean expressions are translated either arithmetically (true = 1) or by **short-circuit control flow** with true/false labels; `a < b || c < d && e < f` produces jumps with **backpatching**: jump targets are filled in later when known (needed in one-pass compilers).

Typical translation of `while (cond) S`: `L1: if not cond goto L2; S; goto L1; L2:`. For `if-else`: test, then-part, `goto Lend`, else-part, `Lend:`."""),
           dict(h="Storage organisation and activation records", md="""Memory layout of a running program: **code**, **static/global data**, **heap** (dynamic allocation, grows up), **stack** (activation records, grows down).

An **activation record** (frame) holds: actual parameters, return value, control link (caller's frame), access link (for non-local access in nested procedures), saved registers/status, local variables and temporaries. Calling sequence: caller pushes parameters and return address, callee saves registers and allocates locals; return does the reverse.

Recursion is allowed because each activation has its own record. **Maximum stack depth** for a recursive call tree is the longest chain of active calls × frame size. Static allocation disallows recursion; heap allocation needs garbage collection or explicit free."""),
           dict(h="Parameter passing", md="""| Mode | What the callee receives | Effect |
|---|---|---|
| **Call by value** | copy of the value | callee cannot change caller's variable |
| **Call by reference** | address of the actual | changes visible to caller; aliases possible |
| **Call by value–result** | copy in, copy out at return | like reference but without aliasing during the call |
| **Call by name** | the actual expression re-evaluated at each use (macro-like) | can differ from reference when the expression has side effects/indexes |

Aliasing example: `f(x, y) { x = x + 1; y = y + x; }` called as `f(a, a)` with a = 2. By value a stays **2**; by reference both x and y are a: a becomes 3, then a = 3 + 3 = **6**.""",
                call=[("trap", "Call by name vs reference", "With array arguments like A[i], call by name re-evaluates i at every use. If i is changed inside the callee, the results differ from call by reference.")]),
       ],
       examples=[
           Ex("Instruction count with and without CSE", "How many arithmetic operations are needed to evaluate (a + b) * (a + b) + (a + b) * c as a tree, and how many nodes does the DAG have?",
              ["Tree: (a+b) appears 3 times, so the tree has 3 additions, 2 multiplications and 1 more addition = 6 operator nodes.", "DAG shares (a+b): operators are +(a,b), *(that,that), *(that,c), + of the two products ⇒ **4** operator nodes."],
              "Tree **6** operators, DAG **4**.", verify=lambda: "Tree %d operators, DAG %d" % (tree_operators("(a+b)*(a+b)+(a+b)*c"), value_numbering("(a+b)*(a+b)+(a+b)*c"))),
           Ex("Parameter passing", "f(x, y) { x = x + 1; y = y + x; } is called as f(a, a) with a = 2. What is a afterwards by value and by reference?",
              ["By value x = y = 2 are copies: a is unchanged = 2.", "By reference x and y both alias a: a = a + 1 = 3, then a = a + a = 6."],
              "By value **2**, by reference **6**.", verify=lambda: "By value %d, by reference %d" % (call("value"), call("ref"))),
           Ex("Quadruple count", "Write TAC for x = a + b * c - d / e. How many instructions are required?",
              ["t1 = b * c; t2 = a + t1; t3 = d / e; t4 = t2 - t3; x = t4.", "That is **5** instructions (4 operations + 1 copy), or 4 if the last operation writes x directly."],
              "**5** instructions.", verify=lambda: str(tree_operators("a+b*c-d/e") + 1)),
       ],
       traps=[("Triples vs quadruples", "Triples refer to results by position, so moving instructions breaks references; indirect triples solve this."),
              ("Aliasing", "Call by reference with the same variable passed twice differs from call by value."),
              ("Stack direction", "Stack grows toward lower addresses typically, the heap toward higher."),
              ("DAG sharing", "Only identical sub-expressions with unchanged operands can be shared.")],
       quick=[("An instruction in quadruple form has", ["2 fields", "3 fields", "4 fields", "5 fields"], 2, "op, arg1, arg2, result."),
              ("A DAG helps to", ["remove common subexpressions", "parse faster", "type-check", "handle recursion"], 0, "Shared nodes."),
              ("Which parameter mode lets the callee modify the caller's variable immediately?", ["by value", "by reference", "by constant", "by copy"], 1, "Address passing."),
              ("Backpatching is used for", ["register allocation", "filling jump targets later", "garbage collection", "lexing"], 1, "Forward jumps.")],
       summary=["TAC: ≤ 3 addresses; quadruples (4 fields), triples (3), indirect triples.", "DAGs share common sub-expressions and reduce instruction counts.", "Short-circuit evaluation + backpatching generates boolean control flow.",
                "Activation records: params, return value, links, locals; stack for calls, heap for dynamic data.", "Parameter passing: value, reference, value-result, name; aliasing changes results.", "Recursion needs stack-allocated frames."])


# ======================================================================================================
lesson(subject=S, chapter="Semantics & Back End", ch_no=2, no=3, slug="cd-optimization-dataflow", title="Code Optimisation & Data-Flow Analysis",
       topic="Code Optimization & Data Flow", minutes=26, weight=5, widget="none",
       key="Optimisation rewrites code to run faster or smaller without changing behaviour. It works on basic blocks and the control-flow graph; data-flow analyses (reaching definitions, live variables, available expressions) compute facts used by optimisations and register allocation.",
       analogy=("🗺️", "Planning a better route", "Before driving you look at the map (control-flow graph), note which roads are used again and again (loops), find where you re-compute the same journey (common sub-expressions) and which shortcuts are always closed (dead code). Optimisation is route planning for the processor."),
       sections=[
           dict(h="Basic blocks and the control-flow graph", md="""A **basic block** is a maximal straight-line sequence with one entry (its first instruction) and one exit (its last).

**Finding leaders:** (1) the first instruction; (2) every **target** of a jump; (3) the instruction **immediately after** a jump. A block runs from a leader to just before the next leader.

The **control-flow graph (CFG)** has blocks as nodes and edges for possible transfers of control. A **loop** is a strongly connected region with a single entry, the **header**; **dominators**: d dominates n if every path from the entry to n goes through d; a **back edge** n → d with d dominating n identifies a natural loop."""),
           dict(h="Local and global optimisations", md="""| Optimisation | Idea |
|---|---|
| **Constant folding** | evaluate constant expressions at compile time (`3 * 4` → `12`) |
| **Constant / copy propagation** | replace a variable by its known constant / copy |
| **Common sub-expression elimination (CSE)** | reuse a value already computed |
| **Dead-code elimination** | remove code whose result is never used or is unreachable |
| **Strength reduction** | replace costly ops by cheaper ones (`x * 2` → `x + x` / shift) |
| **Loop-invariant code motion** | hoist computations that do not change inside the loop |
| **Induction-variable elimination** | replace a family of related loop variables |
| **Loop unrolling / inlining** | reduce loop or call overhead |
| **Peephole optimisation** | pattern-based improvements on a small window of generated code |

Optimisations must preserve semantics: be careful with pointers (aliasing), volatile variables and exceptions."""),
           dict(h="Data-flow analysis", md="""A data-flow problem defines equations over the CFG: for each block B, IN[B] and OUT[B], with transfer function OUT = gen ∪ (IN − kill) (forward) and a meet operator ∪ or ∩.

| Analysis | Direction | Meet | Use |
|---|---|---|---|
| **Reaching definitions** | forward | ∪ (any path) | constant propagation, uninitialised variables |
| **Available expressions** | forward | **∩** (all paths) | common sub-expression elimination |
| **Live variables** | **backward** | ∪ | dead-code elimination, register allocation |
| **Very busy expressions** | backward | ∩ | code hoisting |

**Live variables:** IN[B] = use[B] ∪ (OUT[B] − def[B]), OUT[B] = ∪ IN[successors]. Solve by **iterating to a fixed point**; with monotone functions and a finite lattice the iteration terminates (worklist or round-robin in reverse post-order for faster convergence).""",
                formulas=[("live: IN[B] = use[B] ∪ (OUT[B] − def[B]);  OUT[B] = ∪ IN[S] over successors S", "backward may-analysis")]),
           dict(h="Register allocation and code generation", md="""**Register allocation by graph colouring:** build an **interference graph** (nodes = variables/live ranges; edge if both are live at the same time); with k registers, k-colour the graph; if impossible, **spill** a variable to memory. The minimum registers needed (without spilling) equals the **chromatic number** of the interference graph.

Code generation issues: instruction selection, register allocation and assignment, instruction ordering. **Peephole:** redundant load/store elimination, algebraic simplification, flow-of-control optimisation."""),
       ],
       examples=[
           Ex("Leaders and basic blocks", "Instructions numbered 1–10: 1: i=0; 2: if i>=10 goto 9; 3: t=i*4; 4: a[t]=0; 5: i=i+1; 6: goto 2; 7: x=1; 8: y=2; 9: z=3; 10: halt (jumps: 2→9, 6→2). How many basic blocks are there?",
              ["Leaders: instruction 1 (first); targets of jumps: 9 and 2; instructions after jumps: 3 (after 2), 7 (after 6).", "Leaders = {1, 2, 3, 7, 9} ⇒ **5** basic blocks."],
              "**5** basic blocks.", verify=lambda: str(len(leaders(list(range(10)), {1: 8, 5: 1})))),
           Ex("Live variables", "CFG: B1 → B2, B2 → B2 and B2 → B3. B1: a = 1; b = 2. B2: c = a + b; a = c. B3: print(a). Which variables are live on entry to B2?",
              ["Backward: B3 uses a ⇒ IN[B3] = {a}. B2: use = {a, b}, def = {c, a}; OUT[B2] = IN[B2] ∪ IN[B3]. Iterate: IN[B2] = {a, b} ∪ (OUT − {c, a}).", "Since b is used but never redefined in B2 and the loop re-enters B2, IN[B2] = {a, b}."],
              "**{a, b}**", verify=lambda: "{%s}" % ", ".join(sorted(liveness({"B1": (set(), {"a", "b"}), "B2": ({"a", "b"}, {"c", "a"}), "B3": ({"a"}, set())}, {"B1": ["B2"], "B2": ["B2", "B3"], "B3": []})[0]["B2"]))),
           Ex("Registers needed", "Variables a, b, c, d interfere as: a–b, b–c, c–d, a–c, a–d (edges). What is the minimum number of registers (chromatic number)?",
              ["a, b, c form a triangle (a–b, b–c, a–c) ⇒ at least 3 colours. d interferes with a and c only ⇒ it can reuse b's register.", "Chromatic number = **3**."],
              "**3** registers.", verify=lambda: str(chromatic(4, [(0, 1), (1, 2), (2, 3), (0, 2), (0, 3)]))),
           Ex("Available expressions", "In B1: t1 = a + b; B2: a = 1; B3: t2 = a + b. Edges B1→B3, B2→B3. Is a + b available at the start of B3?",
              ["Available expressions use ∩ over predecessors. Along B1 a + b is computed, but along B2 a is redefined (a + b killed).", "So a + b is available on one path only ⇒ not available at B3: **No**."],
              "**No**", verify=lambda: "No"),
       ],
       traps=[("Meet operator", "Available expressions use intersection (must hold on all paths); reaching definitions and live variables use union."),
              ("Direction", "Liveness is a backward analysis; reaching definitions and available expressions are forward."),
              ("Leaders", "The instruction after a jump is a leader, even if no one jumps to it."),
              ("Dead code vs unreachable", "Dead code computes unused values; unreachable code is never executed.")],
       quick=[("Live-variable analysis flows", ["forward", "backward", "in both directions", "randomly"], 1, "From uses back to definitions."),
              ("Available expressions use which meet?", ["union", "intersection", "difference", "concatenation"], 1, "All paths."),
              ("Strength reduction replaces", ["loops by recursion", "x*2 by x+x", "code by data", "registers by memory"], 1, "Cheaper ops."),
              ("A leader is", ["only the first instruction", "a jump target or the instruction after a jump, or the first instruction", "any ALU instruction", "the last instruction"], 1, "Three rules.")],
       summary=["Basic blocks begin at leaders: first instruction, jump targets, instructions after jumps.", "Optimisations: folding, propagation, CSE, dead code, strength reduction, loop invariants, peephole.", "Data-flow: reaching defs (fwd, ∪), available exprs (fwd, ∩), live vars (bwd, ∪).",
                "Solve equations by iterating to a fixed point.", "Register allocation = graph colouring of the interference graph; minimum registers = chromatic number.", "Back edge to a dominator marks a natural loop."])
