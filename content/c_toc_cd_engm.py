"""TOC + Compiler Design + Engineering Mathematics — curated concept questions."""
from content.kit import C

# ===================== TOC =====================
C("TOC", "Regular Languages & Finite Automata", "Concepts", [
    ("e", 1, "s", "Which of the following languages over {a, b} is regular?", ["Strings with an even number of a's", "{aⁿbⁿ | n ≥ 0}", "{ww | w ∈ {a,b}*}", "Strings with equal numbers of a's and b's"], 0, "A DFA with two states counting parity suffices."),
    ("e", 1, "s", "An NFA and a DFA are", ["equal in language-recognising power", "such that NFAs recognise more languages", "such that DFAs recognise more languages", "unrelated"], 0, "Subset construction converts NFA to DFA."),
    ("m", 1, "s", "The regular expression (a + b)*abb describes", ["strings ending in abb", "strings starting with abb", "strings containing abb exactly once", "strings of length 3"], 0, "Any prefix followed by abb."),
    ("m", 2, "s", "The minimal DFA for the language of strings over {0,1} that end in 01 has how many states (complete DFA)?", ["3", "2", "4", "5"], 0, "States track the longest suffix matching a prefix of 01."),
    ("m", 1, "s", "Myhill–Nerode theorem characterises regular languages via", ["a finite number of equivalence classes of strings", "pumping length", "closure under complement", "stack depth"], 0, "The number of classes equals the number of states of the minimal DFA."),
    ("h", 2, "s", "The reversal of a regular language", ["is regular", "may be non-regular", "is always finite", "is context-free but not regular"], 0, "Reverse the NFA and swap start/final states."),
    ("h", 2, "s", "A Moore machine with n states and a Mealy machine for the same function relate as", ["a Mealy machine can have fewer states", "a Moore machine always has fewer states", "they are never equivalent", "a Mealy machine cannot have output"], 0, "Converting Mealy to Moore may increase states."),
    ("h", 2, "m", "Which of the following are TRUE for regular languages? (select all)", ["Every finite language is regular", "The complement of a regular language is regular", "Every subset of a regular language is regular", "Regular languages are closed under union"], [0, 1, 3], "Subsets of regular languages need not be regular."),
    ("h", 2, "s", "How many states can the minimal DFA equivalent to an n-state NFA have at most?", ["2^n", "n²", "n", "n!"], 0, "Worst case exponential blow-up."),
])

C("TOC", "Context-Free Languages & PDA", "Concepts", [
    ("e", 1, "s", "A pushdown automaton uses", ["a stack as memory", "a queue as memory", "two tapes", "no memory"], 0, "Gives power to count and match."),
    ("m", 1, "s", "Which language is context-free but not regular?", ["{aⁿbⁿ | n ≥ 0}", "{aⁿ | n ≥ 0}", "a*b*", "{w | |w| is even}"], 0, "Needs unbounded counting."),
    ("m", 2, "s", "Deterministic and non-deterministic PDAs are", ["not equivalent in power", "equivalent in power", "both only recognise regular languages", "both equivalent to Turing machines"], 0, "e.g., {wwᴿ} needs nondeterminism."),
    ("m", 1, "s", "A grammar is ambiguous if", ["some string has more than one parse tree (or leftmost derivation)", "it has epsilon productions", "it has left recursion", "it generates a finite language"], 0, "Ambiguity can sometimes be removed by rewriting."),
    ("m", 2, "s", "A CFG in Chomsky Normal Form generates a string of length n ≥ 1 using exactly how many derivation steps?", ["2n − 1", "n", "n − 1", "2n"], 0, "n − 1 binary rules plus n terminal rules."),
    ("h", 2, "s", "Which of the following CFLs is inherently ambiguous?", ["{aⁱbʲcᵏ | i = j or j = k}", "{aⁿbⁿ}", "{wwᴿ}", "balanced parentheses"], 0, "Strings with i = j = k have two essentially different derivations."),
    ("h", 2, "s", "The intersection of a context-free language and a regular language is", ["context-free", "regular", "not necessarily context-free", "empty"], 0, "Product construction of a PDA and a DFA."),
    ("h", 2, "s", "Greibach normal form productions have the shape", ["A → aα (a terminal followed by non-terminals)", "A → BC or A → a", "A → ε", "A → αβ with any symbols"], 0, "Useful for converting to PDAs without ε-moves."),
])

C("TOC", "Closure & Pumping Lemma", "Concepts", [
    ("e", 1, "s", "The pumping lemma for regular languages is used to prove that a language is", ["not regular", "regular", "context-free", "decidable"], 0, "It gives a necessary condition only."),
    ("m", 1, "s", "Context-free languages are NOT closed under", ["intersection", "union", "concatenation", "Kleene star"], 0, "{aⁿbⁿcᵐ} ∩ {aᵐbⁿcⁿ} = {aⁿbⁿcⁿ}."),
    ("m", 2, "s", "Deterministic context-free languages are closed under", ["complementation", "union", "concatenation", "Kleene star"], 0, "DCFLs are closed under complement but not union/intersection."),
    ("m", 1, "s", "Regular languages are closed under", ["complement, union, intersection and Kleene star", "union only", "intersection but not complement", "none of these"], 0, "All Boolean and regular operations."),
    ("h", 2, "s", "To show L = {aⁿbⁿ} is not regular with the pumping lemma, we choose the string", ["aᵖbᵖ", "a^p", "b^p a^p", "(ab)^p"], 0, "Pumping the a-prefix breaks the equality."),
    ("h", 2, "s", "The language {aⁿ² | n ≥ 0} is", ["not context-free", "regular", "context-free but not regular", "finite"], 0, "Gaps between squares grow; the CFL pumping lemma fails."),
    ("h", 2, "m", "Which of these languages are NOT regular? (select all)", ["{0ⁿ1ⁿ | n ≥ 0}", "{w | w has equal numbers of 0s and 1s}", "{w | w contains 001 as a substring}", "{0ⁱ1ʲ | i ≠ j}"], [0, 1, 3], "Containing 001 is a simple DFA language."),
    ("h", 2, "s", "The set of regular languages is closed under", ["homomorphism and inverse homomorphism", "homomorphism only", "neither", "inverse homomorphism only"], 0, "Both preserve regularity."),
])

C("TOC", "Turing Machines & Decidability", "Concepts", [
    ("e", 1, "s", "A language is recursively enumerable if", ["some Turing machine accepts exactly its strings (may loop on others)", "some TM halts on all inputs deciding it", "it is regular", "it is finite"], 0, "Decidable (recursive) languages need halting always."),
    ("m", 1, "s", "The halting problem is", ["undecidable but recursively enumerable", "decidable", "not recursively enumerable", "regular"], 0, "Simulate the machine; halting is semi-decidable."),
    ("m", 2, "s", "Rice's theorem states that", ["every non-trivial semantic property of the language of a TM is undecidable", "the halting problem is decidable for total functions", "emptiness of DFAs is undecidable", "TM equivalence is decidable"], 0, "'Is L(M) finite/regular/empty?' are undecidable."),
    ("m", 1, "s", "Multi-tape TMs compared with single-tape TMs are", ["equivalent in computational power", "strictly more powerful", "strictly less powerful", "decidable only"], 0, "A single tape can simulate multiple tapes with polynomial slowdown."),
    ("h", 2, "s", "A language is decidable iff", ["both it and its complement are recursively enumerable", "its complement is regular", "it is context-free", "it is in NP"], 0, "Run both enumerators in parallel."),
    ("h", 2, "s", "Which problem is undecidable?", ["Whether a CFG is ambiguous", "Whether a DFA accepts a given string", "Whether a PDA's language is empty", "Whether two regular expressions are equivalent"], 0, "The others have decision procedures."),
    ("h", 2, "m", "Which are decidable? (select all)", ["Membership for context-sensitive grammars", "Emptiness of a CFG", "Equivalence of two DFAs", "Equivalence of two Turing machines"], [0, 1, 2], "TM equivalence is undecidable."),
    ("h", 2, "s", "A linear bounded automaton recognises", ["context-sensitive languages", "regular languages", "context-free languages only", "all recursively enumerable languages"], 0, "A TM whose tape is restricted to the input length."),
])

# ===================== COMPILER DESIGN =====================
C("CD", "Lexical Analysis", "Concepts", [
    ("e", 1, "s", "The lexical analyser's main output is", ["a stream of tokens", "a parse tree", "intermediate code", "machine code"], 0, "Tokens carry a type and a lexeme/attribute."),
    ("e", 1, "s", "Lexical analysis is usually specified using", ["regular expressions", "context-free grammars", "attribute grammars", "type systems"], 0, "Implemented as DFAs (e.g., lex/flex)."),
    ("m", 1, "s", "The 'longest match' (maximal munch) rule means", ["the lexer takes the longest prefix of input that matches some token pattern", "the lexer picks the shortest token", "keywords are matched last", "tokens are matched right to left"], 0, "'<=' is one token, not '<' then '='."),
    ("m", 2, "s", "Which of the following tasks is NOT performed by the lexical analyser?", ["Checking that parentheses are balanced", "Removing comments and whitespace", "Recognising identifiers and keywords", "Reporting illegal characters"], 0, "Balanced parentheses require a context-free parser."),
    ("m", 1, "s", "A symbol table is used to", ["store information about identifiers such as type and scope", "store the parse tree", "hold generated assembly", "store token patterns"], 0, "Built during lexing/parsing and used in semantic analysis."),
    ("h", 2, "s", "Two-buffer schemes with sentinels are used in lexical analysers to", ["speed up character scanning by avoiding end-of-buffer tests per character", "implement parsing", "reduce symbol table size", "store tokens"], 0, "A sentinel EOF marks the end of each buffer."),
])

C("CD", "Parsing (LL & LR)", "Concepts", [
    ("e", 1, "s", "A grammar with left recursion cannot be parsed by", ["a top-down recursive-descent (LL) parser without transformation", "an LR parser", "an LALR parser", "an SLR parser"], 0, "Left recursion causes infinite recursion in LL parsers."),
    ("m", 1, "s", "Every LL(1) grammar is", ["unambiguous", "ambiguous", "left recursive", "not context-free"], 0, "A parsing table with no conflicts implies a unique derivation."),
    ("m", 2, "s", "Which of the following is the most powerful parser?", ["Canonical LR(1)", "SLR(1)", "LALR(1)", "LL(1)"], 0, "CLR ⊃ LALR ⊃ SLR ⊃ LR(0), and LL(1) ⊂ LR(1)."),
    ("m", 2, "s", "LALR(1) parsers are created by merging LR(1) states with identical", ["cores (LR(0) items)", "lookaheads", "goto actions", "reductions"], 0, "Merging can introduce reduce–reduce conflicts but never shift–reduce conflicts that were absent."),
    ("m", 1, "s", "Shift–reduce parsers use a", ["stack and an input buffer", "queue and a heap", "symbol table only", "parse table without a stack"], 0, "Handles are reduced when on top."),
    ("h", 2, "s", "FOLLOW sets are used in", ["SLR(1) parsing table construction and LL(1) table construction for ε-productions", "lexical analysis", "register allocation", "type checking"], 0, "Reduce entries are placed under terminals in FOLLOW(A)."),
    ("h", 2, "m", "Which of these grammar classes are subsets of unambiguous grammars? (select all)", ["LL(1)", "LR(1)", "SLR(1)", "All context-free grammars"], [0, 1, 2], "Ambiguous grammars are never LR(k)/LL(k)."),
    ("h", 2, "s", "An operator-precedence grammar must not have", ["ε-productions or two adjacent non-terminals on a right-hand side", "terminals", "left recursion on operators", "unit productions only"], 0, "Required for the precedence relations to be defined."),
])

C("CD", "Syntax-Directed Translation", "Concepts", [
    ("e", 1, "s", "A synthesized attribute of a node is computed from", ["the attributes of its children", "the attributes of its parent and siblings", "the symbol table only", "the input stream only"], 0, "Inherited attributes flow from parent/siblings."),
    ("m", 2, "s", "An S-attributed definition uses", ["only synthesized attributes, so it can be evaluated during bottom-up parsing", "only inherited attributes", "both, with arbitrary dependencies", "no attributes"], 0, "Evaluated at reduce actions."),
    ("m", 2, "s", "An L-attributed definition allows inherited attributes that depend on", ["the parent's inherited attributes and left siblings' attributes", "right siblings", "any node in the tree", "only synthesized attributes"], 0, "Suitable for top-down, left-to-right evaluation."),
    ("h", 2, "s", "A dependency graph of an attribute grammar must be ___ for attributes to be evaluable.", ["acyclic", "a tree", "strongly connected", "bipartite"], 0, "A cycle means circular definitions."),
    ("m", 1, "s", "A syntax tree differs from a parse tree in that it", ["omits non-essential grammar symbols and chain productions", "includes every derivation step", "has more nodes", "includes tokens' regular expressions"], 0, "It is a condensed representation."),
])

C("CD", "Intermediate Code & Runtime", "Concepts", [
    ("e", 1, "s", "Three-address code for a = b + c * d is", ["t1 = c * d; a = b + t1", "a = b + c; a = a * d", "t1 = b + c; a = t1 * d", "a = b c d + *"], 0, "Respects operator precedence."),
    ("m", 1, "s", "Static scoping means", ["a name's binding is determined by the program text structure", "binding is determined by the call chain at run time", "all variables are global", "scopes are created dynamically on the heap"], 0, "Dynamic scoping uses the call stack."),
    ("m", 2, "s", "The activation record usually contains", ["return address, parameters, local variables and links", "only global variables", "the symbol table", "the entire object code"], 0, "Allocated on the control stack."),
    ("m", 1, "s", "Which parameter-passing mechanism lets the callee modify the caller's variable directly?", ["Call by reference", "Call by value", "Call by constant", "Call by copy of copy"], 0, "Call by value passes a copy."),
    ("h", 2, "s", "Quadruples differ from triples in that quadruples", ["explicitly name the result (temporary) and so can be reordered more easily", "use no operator field", "need fewer fields", "cannot represent jumps"], 0, "Triples refer to results by instruction position."),
    ("h", 2, "s", "In a language with nested procedures, a procedure accesses non-local variables through", ["access (static) links or a display", "dynamic links only", "global registers only", "the heap"], 0, "Static links follow lexical nesting."),
])

C("CD", "Code Optimization & Data Flow", "Concepts", [
    ("e", 1, "s", "Constant folding is the optimisation that", ["evaluates constant expressions at compile time", "moves invariant code out of loops", "removes unreachable code", "replaces multiplication by shifts"], 0, "e.g., 2 * 3 → 6."),
    ("m", 1, "s", "Loop-invariant code motion", ["moves computations that do not change within a loop to before the loop", "unrolls loops", "inlines functions", "removes dead stores"], 0, "Reduces repeated work."),
    ("m", 2, "s", "Strength reduction replaces", ["expensive operations (e.g. multiplication) by cheaper ones (e.g. addition/shift)", "functions by macros", "loops by recursion", "registers by memory"], 0, "i * 2 → i << 1."),
    ("m", 2, "s", "Live variable analysis is a ___ data-flow problem.", ["backward", "forward", "bidirectional", "flow-insensitive"], 0, "Liveness at a point depends on future uses."),
    ("m", 2, "s", "Reaching definitions analysis is a ___ data-flow problem with the meet operator ___.", ["forward, union", "backward, union", "forward, intersection", "backward, intersection"], 0, "May-analysis: union at joins."),
    ("h", 2, "s", "Available expressions analysis is a ___ data-flow problem with meet operator ___.", ["forward, intersection", "forward, union", "backward, intersection", "backward, union"], 0, "Must-analysis: an expression must be available on all paths."),
    ("h", 2, "s", "Dead code elimination removes", ["code whose results are never used", "all unreachable loops only", "comments", "unused functions from libraries only"], 0, "Often combined with liveness."),
    ("h", 2, "s", "A basic block is a sequence of instructions with", ["a single entry at the first instruction and a single exit at the last", "multiple entries", "no branches at all in the program", "only straight-line floating-point code"], 0, "Optimisations are first applied locally within blocks."),
    ("h", 2, "s", "Peephole optimisation works by", ["examining a small window of instructions and replacing inefficient patterns", "analysing the whole program graph", "reordering functions", "global register allocation only"], 0, "e.g., removing redundant loads/stores."),
])

# ===================== ENGINEERING MATHEMATICS =====================
C("ENGM", "Propositional & First-Order Logic", "Concepts", [
    ("e", 1, "s", "The proposition p → q is logically equivalent to", ["¬p ∨ q", "p ∨ ¬q", "¬p ∧ q", "q → p"], 0, "Material implication."),
    ("e", 1, "s", "The contrapositive of 'if it rains, the match is cancelled' is", ["if the match is not cancelled, it did not rain", "if the match is cancelled, it rained", "if it does not rain, the match is not cancelled", "it rains and the match is not cancelled"], 0, "¬q → ¬p."),
    ("m", 1, "s", "The negation of ∀x P(x) is", ["∃x ¬P(x)", "∀x ¬P(x)", "∃x P(x)", "¬∃x ¬P(x)"], 0, "De Morgan for quantifiers."),
    ("m", 2, "s", "Which of the following is a tautology?", ["(p → q) ∨ (q → p)", "p → ¬p", "p ∧ ¬p", "(p ∨ q) → p"], 0, "One of the two implications is always true."),
    ("m", 2, "m", "Which of the following are true in general? (select all)", ["∃x ∀y P(x,y) → ∀y ∃x P(x,y)", "∀x ∃y P(x,y) → ∃y ∀x P(x,y)", "∀x (P(x) ∧ Q(x)) ↔ (∀x P(x) ∧ ∀x Q(x))", "∃x (P(x) ∨ Q(x)) ↔ (∃x P(x) ∨ ∃x Q(x))"], [0, 2, 3], "Swapping ∀∃ to ∃∀ is invalid."),
    ("h", 2, "s", "A set of connectives is functionally complete. Which set is NOT?", ["{∧, ∨}", "{¬, ∧}", "{¬, →}", "{↑ (NAND)}"], 0, "{∧, ∨} cannot express negation."),
    ("h", 2, "s", "The formula (p ∨ q) ∧ (¬p ∨ r) → (q ∨ r) is", ["a tautology (resolution rule)", "a contradiction", "satisfiable but not valid", "invalid"], 0, "The resolution principle."),
])

C("ENGM", "Sets, Relations & Functions", "Concepts", [
    ("e", 1, "s", "A relation that is reflexive, symmetric and transitive is called", ["an equivalence relation", "a partial order", "a function", "a total order"], 0, "It partitions the set into classes."),
    ("m", 1, "s", "A function f: A → B is invertible iff it is", ["a bijection", "an injection only", "a surjection only", "constant"], 0, "One-to-one and onto."),
    ("m", 2, "s", "The relation 'x divides y' on positive integers is", ["a partial order", "an equivalence relation", "a total order", "symmetric"], 0, "Reflexive, antisymmetric and transitive."),
    ("m", 1, "s", "The cardinality of the Cartesian product A × B with |A| = m, |B| = n is", ["mn", "m + n", "2^(m+n)", "m^n"], 0, "Ordered pairs."),
    ("h", 2, "s", "A set S is countably infinite. Which set is uncountable?", ["The power set of S", "S × S", "The set of finite subsets of S", "The set of rationals"], 0, "Cantor's theorem."),
    ("h", 2, "m", "Which of the following are TRUE for functions f: A → B and g: B → C? (select all)", ["If g∘f is injective then f is injective", "If g∘f is surjective then g is surjective", "If g∘f is injective then g is injective", "If f and g are bijections then g∘f is a bijection"], [0, 1, 3], "g need not be injective."),
])

C("ENGM", "Partial Orders & Lattices", "Concepts", [
    ("e", 1, "s", "A lattice is a poset in which every pair of elements has", ["a least upper bound and a greatest lower bound", "a maximum only", "a minimum only", "a complement"], 0, "Join and meet."),
    ("m", 1, "s", "A Hasse diagram omits", ["reflexive edges and edges implied by transitivity", "the top element", "antisymmetric pairs", "maximal elements"], 0, "Only covering relations are drawn."),
    ("m", 2, "s", "In a finite Boolean algebra with n atoms, the number of elements is", ["2^n", "n²", "n!", "2n"], 0, "Isomorphic to the power set of the atoms."),
    ("h", 2, "s", "The lattice (D₃₀, |) is", ["a Boolean algebra", "a chain", "not distributive", "not complemented"], 0, "30 = 2·3·5 is square-free."),
    ("h", 2, "s", "Which of the following lattices is NOT distributive?", ["The pentagon lattice N5", "A chain", "A Boolean algebra", "(D₁₂, |)"], 0, "N5 and M3 are the forbidden sublattices."),
])

C("ENGM", "Groups & Monoids", "Concepts", [
    ("e", 1, "s", "A group must satisfy", ["closure, associativity, identity and inverses", "closure and commutativity only", "associativity only", "identity only"], 0, "Commutativity makes it abelian."),
    ("m", 1, "s", "Lagrange's theorem says the order of a subgroup H of a finite group G", ["divides |G|", "equals |G|", "is a multiple of |G|", "is prime"], 0, "[G : H] = |G|/|H|."),
    ("m", 2, "s", "Every group of prime order is", ["cyclic", "non-abelian", "trivial", "of order 1"], 0, "Any non-identity element generates it."),
    ("h", 2, "s", "The number of generators of the cyclic group Z₁₀ is", ["4", "2", "5", "9"], 0, "φ(10) = 4."),
    ("h", 2, "s", "A semigroup with an identity element is called a", ["monoid", "group", "ring", "lattice"], 0, "Groups additionally need inverses."),
])

C("ENGM", "Graph Theory", "Concepts", [
    ("e", 1, "s", "A connected graph has an Euler circuit iff", ["every vertex has even degree", "exactly two vertices have odd degree", "it is bipartite", "it has a Hamiltonian cycle"], 0, "Exactly two odd vertices gives an Euler path."),
    ("m", 1, "s", "A graph is bipartite iff it contains no", ["odd-length cycle", "even-length cycle", "triangle only", "bridge"], 0, "Equivalent to 2-colourability."),
    ("m", 2, "s", "A planar graph with n ≥ 3 vertices has at most how many edges?", ["3n − 6", "2n − 4", "n²", "3n"], 0, "From Euler's formula."),
    ("m", 1, "s", "Number of edges in a tree with n vertices is", ["n − 1", "n", "n + 1", "n(n − 1)/2"], 0, "A tree is a connected acyclic graph."),
    ("h", 2, "s", "The chromatic number of the Petersen graph is", ["3", "2", "4", "5"], 0, "It contains odd cycles, but is 3-colourable."),
    ("h", 2, "m", "Which of the following are TRUE? (select all)", ["Every tree is bipartite", "K₄ is planar", "K₅ is planar", "K₃,₃ is non-planar"], [0, 1, 3], "K₅ and K₃,₃ are the Kuratowski graphs."),
])

C("ENGM", "Combinatorics & Recurrences", "Concepts", [
    ("e", 1, "s", "The number of ways to arrange the letters of the word 'LEVEL' is", ["30", "120", "60", "20"], 0, "5!/(2!·2!) = 30."),
    ("m", 1, "s", "The number of non-negative integer solutions of x + y + z = 10 is", ["66", "45", "120", "100"], 0, "C(12, 2) = 66."),
    ("m", 2, "s", "The number of derangements of 4 objects is", ["9", "12", "6", "24"], 0, "D₄ = 4!(1 − 1 + 1/2 − 1/6 + 1/24) = 9."),
    ("h", 2, "s", "The recurrence aₙ = 2aₙ₋₁ + 1 with a₀ = 0 has solution", ["2ⁿ − 1", "2ⁿ + 1", "n·2ⁿ", "2ⁿ⁺¹"], 0, "Iterating: 0, 1, 3, 7, …"),
    ("h", 2, "s", "How many positive integers up to 100 are divisible by neither 2 nor 3?", ["33", "34", "32", "50"], 0, "100 − 50 − 33 + 16 = 33."),
])

C("ENGM", "Matrices & Determinants", "Concepts", [
    ("e", 1, "s", "If a square matrix has two identical rows then its determinant is", ["0", "1", "−1", "undefined"], 0, "Rows are linearly dependent."),
    ("m", 1, "s", "For an n × n matrix A and scalar k, det(kA) equals", ["kⁿ det(A)", "k det(A)", "n k det(A)", "det(A)/k"], 0, "Each of n rows is scaled by k."),
    ("m", 2, "s", "If A is a 3 × 3 matrix with det(A) = 4, then det(adj A) is", ["16", "4", "64", "2"], 0, "det(adj A) = det(A)^(n−1)."),
    ("h", 2, "s", "A square matrix is invertible iff its rank is", ["n (full rank)", "less than n", "0", "1"], 0, "Equivalent to det ≠ 0."),
    ("h", 2, "s", "A matrix A with A² = A is called", ["idempotent", "nilpotent", "orthogonal", "involutory"], 0, "Its eigenvalues are 0 or 1."),
])

C("ENGM", "Linear Equations & Eigenvalues", "Concepts", [
    ("e", 1, "s", "The sum of the eigenvalues of a square matrix equals its", ["trace", "determinant", "rank", "nullity"], 0, "The product equals the determinant."),
    ("m", 1, "s", "A homogeneous system Ax = 0 with more unknowns than equations has", ["non-trivial solutions", "only the trivial solution", "no solution", "exactly one solution"], 0, "rank < number of unknowns."),
    ("m", 2, "s", "The eigenvalues of a real symmetric matrix are always", ["real", "purely imaginary", "complex with non-zero imaginary part", "zero"], 0, "Spectral theorem."),
    ("h", 2, "s", "If λ is an eigenvalue of an invertible matrix A, then an eigenvalue of A⁻¹ is", ["1/λ", "λ", "−λ", "λ²"], 0, "A⁻¹v = (1/λ)v."),
    ("h", 2, "m", "Which statements are TRUE for an n × n matrix A? (select all)", ["A and Aᵀ have the same eigenvalues", "Eigenvectors for distinct eigenvalues are linearly independent", "A is diagonalisable iff it has n linearly independent eigenvectors", "A matrix with a zero eigenvalue is invertible"], [0, 1, 2], "A zero eigenvalue ⇒ singular."),
])

C("ENGM", "Limits, Continuity & Differentiation", "Concepts", [
    ("e", 1, "s", "lim (x→0) sin x / x equals", ["1", "0", "∞", "does not exist"], 0, "Standard limit."),
    ("m", 1, "s", "A function that is differentiable at a point is necessarily", ["continuous at that point", "twice differentiable there", "monotonic", "bounded everywhere"], 0, "The converse is false (|x| at 0)."),
    ("m", 2, "s", "Rolle's theorem requires the function to be continuous on [a,b], differentiable on (a,b) and", ["f(a) = f(b)", "f(a) = 0", "f′(a) = 0", "monotonic"], 0, "Then f′(c) = 0 for some c."),
    ("h", 2, "s", "lim (x→∞) (1 + 1/x)ˣ equals", ["e", "1", "∞", "0"], 0, "Definition of e."),
    ("h", 2, "s", "The derivative of f(x) = xˣ (x > 0) is", ["xˣ (1 + ln x)", "x·xˣ⁻¹", "xˣ ln x", "xˣ"], 0, "Use logarithmic differentiation."),
])

C("ENGM", "Maxima, Minima & Integration", "Concepts", [
    ("e", 1, "s", "If f′(c) = 0 and f″(c) > 0, then f has at c a", ["local minimum", "local maximum", "point of inflection", "discontinuity"], 0, "Second-derivative test."),
    ("m", 1, "s", "∫₀¹ x eˣ dx equals", ["1", "e", "e − 1", "0"], 0, "[(x − 1)eˣ]₀¹ = 0 − (−1) = 1."),
    ("m", 2, "s", "∫₀^π sin²x dx equals", ["π/2", "π", "1", "0"], 0, "Average of sin² is 1/2."),
    ("h", 2, "s", "The function f(x) = x³ − 3x has local maximum value", ["2", "−2", "0", "3"], 0, "Critical points ±1: f(−1) = 2."),
    ("h", 2, "s", "∫ from −1 to 1 of x³ dx equals", ["0", "1/2", "2", "1/4"], 0, "Odd function over a symmetric interval."),
])

C("ENGM", "Probability Basics & Bayes", "Concepts", [
    ("e", 1, "s", "If A and B are independent events with P(A) = 0.3 and P(B) = 0.4, then P(A ∩ B) is", ["0.12", "0.7", "0.1", "0.58"], 0, "Product rule."),
    ("m", 1, "s", "Bayes' theorem gives P(A | B) as", ["P(B | A)P(A) / P(B)", "P(A)P(B)", "P(A) + P(B)", "P(B | A) / P(A)"], 0, "Inverting a conditional probability."),
    ("m", 2, "s", "Two fair dice are rolled. Probability that the sum is 7 is", ["1/6", "1/12", "7/36", "1/9"], 0, "6 favourable outcomes out of 36."),
    ("h", 2, "s", "A bag has 3 red and 2 blue balls. Two balls are drawn WITHOUT replacement. Probability that both are red is", ["3/10", "9/25", "1/5", "3/5"], 0, "(3/5)(2/4) = 3/10."),
    ("h", 2, "s", "If P(A) = 0.5, P(B) = 0.4 and P(A ∪ B) = 0.7, then P(A | B) is", ["0.5", "0.2", "0.4", "0.25"], 0, "P(A∩B) = 0.2 ⇒ 0.2/0.4 = 0.5."),
])

C("ENGM", "Random Variables & Distributions", "Concepts", [
    ("e", 1, "s", "The expected value of the number shown on a fair six-sided die is", ["3.5", "3", "4", "6"], 0, "(1+…+6)/6."),
    ("m", 1, "s", "For X ~ Binomial(n, p) the variance is", ["np(1 − p)", "np", "n(1 − p)", "p(1 − p)"], 0, "Mean np."),
    ("m", 2, "s", "A Poisson random variable with mean λ has variance", ["λ", "λ²", "√λ", "1/λ"], 0, "Mean equals variance."),
    ("h", 2, "s", "If X is exponential with rate λ, then E[X] is", ["1/λ", "λ", "1/λ²", "λ²"], 0, "Variance 1/λ²."),
    ("h", 2, "s", "If X and Y are independent, Var(2X − 3Y) equals", ["4Var(X) + 9Var(Y)", "2Var(X) − 3Var(Y)", "4Var(X) − 9Var(Y)", "Var(X) + Var(Y)"], 0, "Var(aX + bY) = a²Var X + b²Var Y for independent X, Y."),
    ("h", 2, "m", "Which statements about the normal distribution N(μ, σ²) are TRUE? (select all)", ["It is symmetric about μ", "About 95% of values lie within μ ± 2σ", "Mean, median and mode coincide", "Its variance is σ"], [0, 1, 2], "The variance is σ² (σ is the standard deviation)."),
])
