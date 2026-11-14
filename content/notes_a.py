"""Concept notes appended to question explanations: (idea, method, trap) per sub-topic. Part A: ALGO, CD, CN."""
N = {}


def n(subject, sub, idea, method, trap, topic=None):
    N[(subject, topic, sub)] = (idea, method, trap)


# ---------------- ALGO ----------------
n("ALGO", "Asymptotic notation", "O gives an upper bound, Ω a lower bound and Θ a tight bound. f = O(g) when f ≤ c·g beyond some n₀; little-o and little-ω are the strict versions (limit of f/g is 0 or ∞).",
  "Compare growth by the limit f(n)/g(n): 0 means f = o(g), a finite positive constant means f = Θ(g), ∞ means f = ω(g). Drop constants and lower-order terms first.",
  "Θ is only true when both O and Ω hold; 2ⁿ and 2²ⁿ differ by more than a constant factor, and log(n!) = Θ(n log n) but n! ≠ Θ(nⁿ).")
n("ALGO", "Growth rates", "Standard growth ladder: 1 < log n < √n < n < n log n < n² < n³ < 2ⁿ < n! < nⁿ. Polynomials lose to exponentials, exponentials to factorials.",
  "Take logs of both functions: the one with the larger logarithm grows faster (log nⁿ = n log n vs log 2ⁿ = n). Compare exponents when the bases match.",
  "n^(log n) is faster than any polynomial but slower than 2ⁿ; (log n)^k is slower than n^ε for every ε > 0.")
n("ALGO", "Loop analysis", "Count how often the innermost statement runs as a function of n. Additive updates (i += c) give linear counts, multiplicative updates (i *= c) give logarithmic counts.",
  "Write the loop bounds as a sum and evaluate it; for dependent loops use Σ i = n(n+1)/2. For i doubling from 1 to n the body runs ⌊log₂ n⌋ + 1 times.",
  "Check whether the inner bound depends on the outer variable, and whether the loop condition is < or ≤; off-by-one changes exact counts but not the order.")
n("ALGO", "Classification", "P ⊆ NP ⊆ PSPACE ⊆ EXP; NP-complete problems are the hardest in NP and all are polynomially equivalent. P = NP is open, so none of the inclusions is known to be strict except P ≠ EXP.",
  "Place the problem by what is known: a polynomial algorithm → P; a certificate checkable in polynomial time → NP; a reduction from a known NP-complete problem plus membership in NP → NP-complete.",
  "NP does not mean 'not polynomial'; a problem can be NP-hard without being in NP (halting problem); decision versions are classified, not optimisation versions.")
n("ALGO", "NP problems on small graphs", "Vertex cover, independent set and clique are tightly linked: S is an independent set iff V − S is a vertex cover, and a clique in G is an independent set in the complement.",
  "On a small graph test candidates by size: minimum vertex cover = n − maximum independent set; maximum clique of G = maximum independent set of the complement.",
  "Greedy choices (take the highest-degree vertex) do not always give the minimum cover; verify by exhaustive search on small instances.")
n("ALGO", "Reductions", "A ≤ₚ B means an efficient transformation maps instances of A to instances of B with the same answer; hardness flows from A to B, easiness flows from B to A.",
  "To prove B NP-hard, reduce a known NP-hard problem TO B (not the other way round). Check that the reduction runs in polynomial time and preserves yes/no answers.",
  "Reducing B to A proves nothing about B's hardness; also a reduction must map all instances, not just some.")
n("ALGO", "Subset sum & SAT", "Subset sum and 3-SAT are NP-complete. Subset sum has a pseudo-polynomial dynamic program O(n·S), which is exponential in the number of bits of S.",
  "For subset sum fill a table reach[s] over sums 0..S; for SAT count satisfying assignments by splitting on variables or checking each clause.",
  "Pseudo-polynomial is not polynomial; 2-SAT is in P while 3-SAT is NP-complete; a satisfiable formula needs only one satisfying assignment.")
n("ALGO", "0/1 Knapsack", "0/1 knapsack picks each item whole or not at all: dp[i][w] = max(dp[i−1][w], v_i + dp[i−1][w − w_i]) when w_i ≤ w.",
  "Fill the table row by row for items and capacities, then read dp[n][W]; to recover the items walk back from dp[n][W] checking where the value changed.",
  "Greedy by value/weight ratio is only optimal for the fractional version; O(nW) is pseudo-polynomial.")
n("ALGO", "Coin change / LIS", "Coin change (minimum coins) uses dp[a] = 1 + min dp[a − c]; the longest increasing subsequence uses dp[i] = 1 + max dp[j] over j < i with a[j] < a[i].",
  "Build the table from small amounts or prefixes upward; initialise unreachable states to ∞ and take the minimum/maximum over valid transitions.",
  "Greedy largest-coin-first fails for general denominations (e.g. {1, 3, 4}); LIS means strictly increasing unless the question says non-decreasing.")
n("ALGO", "Edit distance", "Edit distance counts the fewest insertions, deletions and substitutions to turn one string into another: d[i][j] = min(d[i−1][j]+1, d[i][j−1]+1, d[i−1][j−1] + [a_i ≠ b_j]).",
  "Initialise d[i][0] = i and d[0][j] = j, then fill the grid; the corner cell is the answer, taking diagonals as free when characters match.",
  "Substitution costs 1 (not 2) in the standard definition; transposition is not an allowed operation unless stated.")
n("ALGO", "LCS", "The longest common subsequence keeps order but not contiguity: if a_i = b_j then L[i][j] = L[i−1][j−1] + 1 else max(L[i−1][j], L[i][j−1]).",
  "Fill an (m+1)×(n+1) table; the corner value is the LCS length. Trace back diagonally on matches to read the subsequence.",
  "Subsequence ≠ substring; there may be several LCSs of the same length.")
n("ALGO", "Matrix chain", "Matrix-chain multiplication chooses the parenthesisation with the fewest scalar products; m[i][j] = min over k of m[i][k] + m[k+1][j] + p_{i−1}·p_k·p_j.",
  "Compute chains of increasing length; multiplying a p×q matrix by a q×r matrix costs p·q·r scalar multiplications.",
  "The dimension array has n+1 entries for n matrices; the result is only the minimum cost, not the product.")
n("ALGO", "Graph counting", "Handshake lemma: Σ deg(v) = 2|E|. A tree on n vertices has n−1 edges; a complete graph Kₙ has n(n−1)/2 edges; a simple graph has at most n(n−1)/2 edges.",
  "Translate the statement into degree sums or edge counts, then solve for the unknown.",
  "Check whether the graph is simple, directed or may contain loops/multi-edges before counting.")
n("ALGO", "MST", "Kruskal adds edges in increasing weight order unless they form a cycle; Prim grows a tree from one vertex by the cheapest crossing edge. A spanning tree has V−1 edges and the MST weight is unique even when the tree is not.",
  "Sort edges by weight and use union-find (Kruskal), or keep a min-priority queue of crossing edges (Prim). Stop after V−1 edges.",
  "With equal weights several MSTs exist but they share the same total weight; MST ≠ shortest-path tree.")
n("ALGO", "SCC / components", "A strongly connected component is a maximal set of vertices mutually reachable in a directed graph; contracting SCCs yields a DAG. Kosaraju/Tarjan find them in O(V+E).",
  "Run DFS, record finishing times, transpose the graph and DFS in decreasing finishing order; each tree is one SCC. For undirected graphs count connected components instead.",
  "Weakly connected is not strongly connected; a single vertex with no cycle is its own SCC.")
n("ALGO", "Shortest paths", "Dijkstra settles vertices in order of tentative distance and needs non-negative weights; Bellman–Ford relaxes all edges V−1 times and handles negative edges; BFS suffices for unit weights.",
  "Initialise dist(source) = 0 and ∞ elsewhere, repeatedly relax edges (u,v): dist(v) = min(dist(v), dist(u)+w). Dijkstra picks the smallest unsettled vertex each round.",
  "Dijkstra fails with negative edges; a negative cycle reachable from the source makes shortest paths undefined.")
n("ALGO", "Topological order", "A topological ordering exists exactly for DAGs and places every edge from an earlier to a later vertex; the number of valid orders depends on how constrained the DAG is.",
  "Repeatedly remove a vertex of in-degree 0 (Kahn) or output vertices in reverse DFS finishing order. If vertices remain when no in-degree-0 vertex exists, there is a cycle.",
  "Topological orders are generally not unique; undirected graphs have no topological order.")
n("ALGO", "Activity selection", "Choosing the compatible activity that finishes earliest is optimal for maximising the number of activities (greedy-choice property with an exchange argument).",
  "Sort by finish time, pick the first activity, then repeatedly pick the next whose start is at least the last chosen finish.",
  "Sorting by start time or by shortest duration is not optimal in general.")
n("ALGO", "Huffman coding", "Huffman builds an optimal prefix code by repeatedly merging the two least frequent nodes; frequent symbols get shorter codes. Cost = Σ frequency × code length.",
  "Merge the two smallest weights, push the sum back, repeat; the total weighted external path length equals the sum of all internal-node weights created.",
  "Different tie-breaking gives different trees but the same optimal cost; the code is prefix-free, not unique.")
n("ALGO", "Job sequencing", "Job sequencing with deadlines maximises profit when each job takes one unit slot and must finish by its deadline; greedily schedule by decreasing profit into the latest free slot ≤ deadline.",
  "Sort by profit, for each job place it in the latest unfilled slot not after its deadline; skip it if none exists. Total profit = sum of scheduled jobs.",
  "Deadlines are inclusive; scheduling earliest instead of latest slots wastes room for later jobs.")
n("ALGO", "Knapsack (fractional)", "In the fractional knapsack items can be split, so taking items in decreasing value/weight order is optimal.",
  "Sort by v/w, take whole items while they fit, then a fraction of the next item to fill the capacity exactly.",
  "The 0/1 version is NP-hard and not solved by this greedy rule.")
n("ALGO", "Binary search / merge", "Binary search halves the search range each step (⌊log₂ n⌋ + 1 comparisons worst case); merging two sorted lists of sizes m and n takes at most m + n − 1 comparisons.",
  "Count how many times the interval can be halved until size 1, or count the comparisons of the merge routine directly.",
  "Binary search needs sorted data; unsuccessful searches also take about log₂ n steps.")
n("ALGO", "Divide and conquer", "Divide and conquer solves a problem by splitting it, recursing and combining: T(n) = aT(n/b) + f(n).",
  "Identify a, b and the cost f(n) of dividing/combining, then solve with the master theorem or by expanding the recurrence.",
  "Unbalanced splits (as in worst-case quicksort) change the recurrence to T(n) = T(n−1) + n.")
n("ALGO", "Master theorem", "For T(n) = aT(n/b) + f(n) compare f(n) with n^(log_b a): smaller by a polynomial factor → Θ(n^(log_b a)); equal → Θ(n^(log_b a) log n); larger (and regular) → Θ(f(n)).",
  "Compute log_b a, compare it with the exponent of f(n), then read off the case. For f(n) = n^k log^p n with k equal to log_b a the answer is n^k log^(p+1) n.",
  "The theorem does not apply when f(n) is not polynomially comparable (e.g. n/log n) or a is not constant.")
n("ALGO", "Recurrence evaluation", "Evaluate a recurrence by unrolling it or by substituting small values until a pattern (or closed form) appears.",
  "Expand T(n) a few steps, spot the series (arithmetic, geometric, harmonic) and sum it; verify with base cases.",
  "Keep the base case values exact; an off-by-one in the starting index changes the final number.")
n("ALGO", "Hashing", "A hash table maps keys to slots with h(k); collisions are resolved by chaining or open addressing (linear probing, quadratic probing, double hashing).",
  "Insert keys in order, applying the probe sequence on collisions; for chaining the load factor α = n/m gives expected search cost 1 + α/2 (successful).",
  "Probing wraps around modulo the table size; deletions in open addressing need tombstones.")
n("ALGO", "Heaps", "A binary heap stores a complete tree in an array with parent(i) = ⌊i/2⌋ (1-indexed); a min-heap keeps every parent ≤ its children. Insertion and extract-min cost O(log n); building takes O(n).",
  "Insert at the end and sift up; extract the root, move the last element to the root and sift down, always swapping with the smaller child in a min-heap.",
  "A heap is not sorted; the number of heaps with n distinct keys is far more than 1; leaves are indices ⌊n/2⌋+1..n.")
n("ALGO", "Quicksort partition", "Partition rearranges elements around a pivot so that smaller ones precede it; Lomuto and Hoare schemes differ in swaps and final pivot position.",
  "Simulate the pointer movement step by step, counting comparisons and swaps; the pivot ends in its final sorted position.",
  "Worst case O(n²) occurs for already sorted input with a first/last pivot; the partition result depends on the scheme.")
n("ALGO", "Sorting counts", "Comparison sorts need Ω(n log n) comparisons in the worst case; bubble sort makes about n(n−1)/2 comparisons and a number of swaps equal to the inversion count.",
  "Count inversions (pairs i < j with a_i > a_j) for swap counts of adjacent-swap sorts; count comparisons by simulating the algorithm.",
  "Selection sort does at most n−1 swaps; merge sort is stable but quicksort is not.")
n("ALGO", "Lower bounds", "Any comparison sort corresponds to a decision tree with n! leaves, so it needs at least ⌈log₂ n!⌉ = Ω(n log n) comparisons.",
  "Count outcomes (leaves) and take log₂ to get the minimum depth.",
  "The bound applies to comparison sorts only; counting and radix sort can beat it.")
for sub in ("Concepts",):
    n("ALGO", sub, "Algorithms are judged by correctness and by how running time and space grow with the input size; asymptotic notation hides constants.",
      "Reduce the statement to a growth-rate or definition check, then test it on a small example.",
      "Memorising a result without its conditions (sorted input, non-negative weights) is the usual source of mistakes.")

# ---------------- CD ----------------
n("CD", "Common subexpressions (DAG)", "A DAG for a basic block shares identical subexpressions: nodes are operations on value-numbered operands, and a repeated operation on the same operands maps to one node.",
  "Process statements in order, reusing a node when an identical (operator, operands) node already exists and no operand has been redefined in between.",
  "Reassigning a variable invalidates earlier nodes that used its old value; the number of DAG nodes counts operators plus leaves.")
n("CD", "Liveness", "A variable is live at a point if its current value may be used later before being redefined. Live-in(i) = use(i) ∪ (live-out(i) − def(i)).",
  "Work backwards through the code: start with the live-out set, remove definitions, add uses.",
  "A variable used only after being redefined is not live before the redefinition.")
n("CD", "Basic blocks", "A basic block is a maximal straight-line sequence with one entry and one exit. Leaders are the first instruction, every jump target, and every instruction after a jump.",
  "Mark the leaders, then each block runs from a leader to just before the next leader.",
  "Count the target of a jump and the instruction following a jump as leaders.")
n("CD", "Register need (Sethi–Ullman)", "The Sethi–Ullman numbering gives the minimum registers to evaluate an expression tree without spilling: leaves = 1 (or 0 for right operands), an inner node takes max(l, r) if they differ, otherwise l + 1.",
  "Label the tree bottom-up and read the root label; evaluate the larger-labelled subtree first.",
  "Commutative operations may swap operands to reduce the need; a left leaf that must be loaded costs 1.")
n("CD", "Runtime environments", "Activation records on the stack hold parameters, return address, saved registers and locals; the access link or display reaches non-local variables in nested-scope languages.",
  "Trace calls and returns to see the stack depth or frame contents at a point.",
  "Static scope uses the access chain of definition, dynamic scope the call chain.")
n("CD", "Maximal munch", "The scanner takes the longest prefix that matches a token pattern; ties go to the rule listed first.",
  "Scan from the current position, extend while some rule still matches, then emit the longest match.",
  "'==' beats '=' ; 'iffy' is one identifier, not the keyword 'if' followed by 'fy'.")
n("CD", "Token counting", "The lexical analyser splits the character stream into tokens (keywords, identifiers, constants, operators, punctuation); whitespace and comments are discarded.",
  "Scan left to right applying longest match, counting each lexeme once.",
  "String literals are one token even if they contain spaces; multi-character operators (<<, ++) are single tokens.")
n("CD", "FIRST & FOLLOW", "FIRST(α) is the set of terminals that can begin a string derived from α (plus ε if α is nullable); FOLLOW(A) is the set of terminals that can appear right after A in some sentential form.",
  "Compute FIRST bottom-up, propagating through nullable symbols; for FOLLOW add FIRST of what follows each occurrence, FOLLOW of the head when the tail is nullable, and $ for the start symbol.",
  "ε never belongs to FOLLOW sets; FOLLOW is defined for non-terminals only.")
n("CD", "LL(1)", "A grammar is LL(1) if for each non-terminal the FIRST sets of its alternatives are disjoint, and if one alternative is nullable its FIRST is disjoint from the FOLLOW set. Left recursion and common prefixes break LL(1).",
  "Build FIRST and FOLLOW, fill the parse table cell [A, a] for each production A → α with a ∈ FIRST(α) (and FOLLOW(A) when α is nullable), and look for conflicts.",
  "Ambiguous grammars are never LL(1).")
n("CD", "LR parsing", "LR parsers are bottom-up: shift tokens onto a stack and reduce when a handle appears. SLR < LALR < LR(1) in power; LALR merges LR(1) states with identical cores.",
  "Build item sets with closure and goto, then check conflicts: a shift/reduce or reduce/reduce conflict in a state means the grammar is not in that class.",
  "LALR can introduce reduce/reduce conflicts absent from LR(1) but never shift/reduce ones.")
n("CD", "Shift-reduce counts", "A shift-reduce parser makes one shift per input token and one reduce per production applied; the number of reduces equals the number of internal nodes in the parse tree.",
  "Count tokens for shifts and productions used in the rightmost derivation (in reverse) for reduces.",
  "Unit productions and ε-productions still count as reduces.")
n("CD", "Synthesized attributes", "A synthesized attribute is computed from the attributes of a node's children (bottom-up); inherited attributes flow from parents/siblings. S-attributed definitions use only synthesized attributes.",
  "Annotate the parse tree bottom-up, evaluating each semantic rule once its inputs are available.",
  "Check the order of evaluation; an inherited attribute may need a left-to-right pass.")
n("CD", "Ambiguity & parse trees", "A grammar is ambiguous if some string has two different parse trees (or leftmost derivations); ambiguity can sometimes be removed by rewriting with precedence and associativity levels.",
  "Search for a string with two derivation trees; fix by layering the grammar (E → E+T | T ...).",
  "Ambiguity is a property of the grammar, not of the language.")
for t in ("Code Optimization & Data Flow", "Intermediate Code & Runtime", "Lexical Analysis", "Parsing (LL & LR)", "Syntax-Directed Translation"):
    n("CD", "Concepts", "Compiler phases transform source code step by step: lexical analysis → syntax analysis → semantic analysis → intermediate code → optimisation → code generation.",
      "Decide which phase the statement belongs to, then recall that phase's input, output and typical algorithm.",
      "Mixing up what each phase can detect (syntax errors in the parser, type errors in semantic analysis) is the common slip.", topic=t)

# ---------------- CN ----------------
n("CN", "Cryptography arithmetic", "RSA: n = pq, φ = (p−1)(q−1), choose e coprime to φ, d ≡ e⁻¹ (mod φ); encrypt c = mᵉ mod n, decrypt m = cᵈ mod n. Diffie–Hellman agrees on gˣʸ mod p without sending the secret.",
  "Compute φ(n), find d with e·d ≡ 1 (mod φ) by the extended Euclidean algorithm, and do modular exponentiation by repeated squaring, reducing at every step.",
  "Never compute mᵉ before reducing; the public key is (e, n) and the private key is (d, n).")
n("CN", "HTTP response time", "Total time adds connection set-up, request/response round trips and transmission delays; non-persistent HTTP pays 2 RTT per object, persistent HTTP with pipelining far fewer.",
  "Count RTTs for TCP handshake, each request/response and parallel connections, then add transmission times.",
  "Transmission time = size / bandwidth, separate from propagation time (RTT/2 each way).")
n("CN", "Protocol facts", "Each protocol has a standard role, port and layer: DNS (UDP/TCP 53), HTTP (80), HTTPS (443), SMTP (25), IMAP/POP3 mail retrieval, FTP (21), DHCP (UDP 67/68), ARP (IP → MAC).",
  "Recall the layer and service of the named protocol, then eliminate options belonging to other layers.",
  "Mixing up similar protocols (ARP vs DNS, SMTP vs POP3) is the standard trap.")
n("CN", "CRC", "CRC treats data as a polynomial, appends zeros equal to the generator degree, divides modulo 2 and sends data plus remainder; the receiver divides again and expects remainder 0.",
  "Append r zeros (r = degree of the generator), perform XOR long division, and the final r bits are the CRC.",
  "Subtraction is XOR with no borrow; the generator must have its highest and lowest term equal to 1.")
n("CN", "Error detection & Hamming", "Hamming distance d detects up to d−1 errors and corrects ⌊(d−1)/2⌋. Hamming code puts parity bits at power-of-two positions; the Internet checksum is a ones'-complement sum.",
  "For the Hamming distance between codewords count differing bits; for the checksum add 16-bit words with end-around carry and complement the result.",
  "Check bits needed r satisfies 2^r ≥ m + r + 1.")
n("CN", "Framing", "Framing marks frame boundaries: character count, byte stuffing with an escape, or bit stuffing (insert a 0 after five consecutive 1s with flag 01111110).",
  "Scan the data for the flag pattern or run of 1s, stuffing as needed; count the stuffed bits to get the final length.",
  "Bit stuffing is applied to the data including checksums and is removed by the receiver.")
n("CN", "Sliding window", "Window protocols keep several frames in flight: Go-Back-N uses a send window up to 2ᵏ − 1 and receiver window 1; Selective Repeat uses windows of 2ᵏ⁻¹. Efficiency = window × Tₜ / (Tₜ + 2Tₚ), capped at 1.",
  "Compute Tₜ = L/B and Tₚ = d/v, then the number of frames needed to keep the pipe full: 1 + 2Tₚ/Tₜ.",
  "Sequence-number bits limit the window size; retransmission in Go-Back-N resends the failed frame and all after it.")
n("CN", "CIDR & VLSM", "CIDR describes a network by address and prefix length; the block size is 2^(32 − prefix) addresses, of which two are reserved (network and broadcast). VLSM allocates different prefix lengths per subnet.",
  "Convert requirements to host counts, round up to a power of two (hosts + 2), assign largest subnets first and keep blocks aligned.",
  "Usable hosts = 2^h − 2; blocks must start at multiples of their size.")
n("CN", "Fragmentation", "IP fragments a datagram that exceeds the MTU; every fragment except the last carries a multiple of 8 bytes of data, the offset field counts 8-byte units, and MF = 1 on all but the last fragment.",
  "Data per fragment = ⌊(MTU − header)/8⌋ × 8; compute the number of fragments by dividing the payload, and offsets as bytes ÷ 8.",
  "The IP header is repeated in every fragment; the last fragment can be shorter and has MF = 0.")
n("CN", "Subnetting", "A subnet mask splits an address into network and host parts. Borrowing b host bits gives 2^b subnets, each with 2^(h−b) − 2 usable hosts.",
  "AND the address with the mask for the network address, set host bits to 1 for broadcast, and count 2^h − 2 hosts.",
  "Subnet 0 and the all-ones subnet are usable in classless addressing; usable hosts exclude network and broadcast.")
n("CN", "Capacity & delay", "Nyquist: C = 2B log₂ V for a noiseless channel; Shannon: C = B log₂(1 + SNR) for a noisy one (SNR as a ratio, 10 log₁₀ for dB). Latency = transmission delay (L/B) + propagation delay (d/v) + queuing.",
  "Convert dB to ratio first, compute the capacity, and use the bandwidth-delay product B·RTT for bits in flight.",
  "Bandwidth in Hz and data rate in bits/s are different; use the lower of Nyquist and Shannon results.")
n("CN", "Ethernet & ALOHA", "Pure ALOHA has maximum efficiency 1/(2e) ≈ 18.4% (at G = 0.5), slotted ALOHA 1/e ≈ 36.8% (at G = 1). CSMA/CD needs frame time ≥ 2 × propagation delay, so minimum frame size = 2·Tₚ·bandwidth.",
  "Plug the offered load into S = G e^(−2G) (pure) or S = G e^(−G) (slotted); for CSMA/CD compute minimum frame length from the round-trip time.",
  "Efficiency peaks at a specific load; do not confuse throughput S with offered load G.")
n("CN", "LAN facts", "Ethernet uses CSMA/CD with binary exponential backoff; switches learn MAC addresses per port and forward within a collision domain; VLANs split broadcast domains.",
  "Identify whether the question is about collision domain, broadcast domain or addressing, then apply the device rules (hubs repeat, switches filter, routers separate broadcasts).",
  "Hubs share one collision domain; switches give one per port.")
n("CN", "Distance vector", "Distance-vector routing exchanges tables with neighbours and updates by Bellman–Ford: d(x,y) = min over neighbours v of c(x,v) + d(v,y). Count-to-infinity arises when a link fails; split horizon and poison reverse help.",
  "Iterate the exchange rounds, updating each entry with the best neighbour estimate until no changes remain.",
  "RIP uses hop count with infinity = 16; convergence can be slow after a failure.")
n("CN", "Shortest paths", "Link-state routing (OSPF) floods topology and every router runs Dijkstra; the result is the least-cost path tree from the source.",
  "Run Dijkstra from the source, updating tentative distances by relaxation and finalising the smallest each round.",
  "Costs must be non-negative; list ties carefully if the question asks for paths.")
n("CN", "TCP congestion control", "TCP slow start doubles cwnd every RTT up to ssthresh, then congestion avoidance adds 1 MSS per RTT. On a timeout ssthresh = cwnd/2 and cwnd = 1; on triple duplicate ACKs (Reno) cwnd = ssthresh = cwnd/2.",
  "Trace cwnd per RTT: apply the growth rule until the loss event, then reset per the event type.",
  "Slow start is exponential per RTT not per segment; after fast recovery growth is linear.")
n("CN", "TCP performance", "TCP throughput is limited by min(window / RTT, bandwidth). Sequence numbers count bytes, ACKs name the next byte expected, and the window field is the receiver's advertised window.",
  "Compare the window-limited rate W/RTT with the link rate; the bottleneck decides.",
  "Window in bytes, rate in bits: convert units consistently.")
n("CN", "UDP & ports", "UDP is connectionless and unreliable with an 8-byte header and checksum; ports (16 bits) identify processes, well-known ports are 0–1023.",
  "Recall the header fields and which services use UDP (DNS, DHCP, streaming).",
  "UDP checksum covers header, data and a pseudo-header; it provides no retransmission.")
for t in ("Application Layer & Security", "Data Link & Error Control", "IP Addressing & Subnetting", "Layering & Physical Layer", "MAC & Ethernet", "Routing", "Transport Layer (TCP/UDP)"):
    n("CN", "Concepts", "Networks are organised in layers; each layer provides a service to the one above and relies on the one below: physical, data link, network, transport, application.",
      "Place the concept at its layer and recall that layer's addressing (MAC, IP, port) and device (switch, router, host).",
      "Confusing the layer a protocol or device belongs to is the typical error.", topic=t)
