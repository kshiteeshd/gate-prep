"""In-depth material for the General Aptitude lessons."""
from learn import deepen

deepen("ga-verbal",
       proofs=[
           ("Why 'the number of applicants is' but 'a number of applicants are': agreement by the head noun",
            """The verb agrees with the **head** of the subject phrase. In 'the number of applicants', the head is *number* (a singular noun) and 'of applicants' only modifies it: 'The number of applicants **is** increasing.' In 'a number of applicants', the phrase 'a number of' works like a quantifier meaning 'several', and the real subject is *applicants*: 'A number of applicants **are** unqualified.' The same logic explains 'the list of items **is** long', 'one of the students **is** absent' (head: *one*), 'neither of the boys **has**' (head: *neither*), and 'either the teacher or the students **are**' (nearest subject for correlative conjunctions). When a long phrase separates subject and verb, strike out the intervening prepositional phrase and test the verb against the head noun."""),
           ("Method for sentence completion by elimination",
            """1. Read the sentence with the blank and decide the **logical relation** from the signal words: contrast (but, although, however, despite), cause (because, since), continuation (and, moreover). 2. Predict the *kind* of word needed (positive/negative, abstract/concrete, verb/adjective) before looking at the options. 3. Eliminate options that break grammar (wrong tense or part of speech), then options that contradict the predicted relation. 4. For two blanks, test each pair: both blanks must fit, and usually one pair preserves the contrast in the sentence. Example: 'Although the plan was costly, it proved ____' signals contrast between costly and the missing word, which must be positive: *worthwhile*."""),
       ],
       notes=[
           ("Grammar rules most often tested",
            """Tenses and their sequence (if-clauses: type 1 present/will, type 2 past/would, type 3 past perfect/would have); subject–verb agreement; pronoun case (between you and me; who vs whom); articles (an hour, a university, the sun); prepositions (prefer to, different from, capable of, responsible for, comprise without of); parallel structure; comparatives (more … than, less/fewer: fewer for countable nouns); modal verbs; active and passive voice; reported speech (backshift of tenses); redundancy (return back, repeat again) and the dangling modifier ('Walking down the street, the trees were beautiful' is wrong because the trees were not walking). Confusable words: affect/effect, principle/principal, complement/compliment, stationary/stationery, elicit/illicit."""),
           ("Reading comprehension strategy",
            """Skim the first and last sentences of each paragraph for the main idea; read the questions before the passage when the passage is long; classify each question (main idea, detail, inference, vocabulary in context, tone, except/not); eliminate options that are too extreme (always, never, only, all), out of scope, or the reverse of what is stated. For inference questions choose the statement that must be true, not merely possible. For critical reasoning identify conclusion and premises; a strengthener supports the link, a weakener attacks the link or the premise, and a necessary assumption is the statement whose negation destroys the argument."""),
       ])

deepen("ga-numerical",
       proofs=[
           ("Successive percentage change: a + b + ab/100, and −x²/100 for an increase followed by the same decrease",
            """A change of a% multiplies the quantity by (1 + a/100) and a change of b% by (1 + b/100). Two successive changes multiply to (1 + a/100)(1 + b/100) = 1 + (a + b + ab/100)/100, so the net change is a + b + ab/100 percent. Setting b = −a gives a − a − a²/100 = −a²/100: a 20% rise followed by a 20% fall leaves the value 4% lower (1.2 × 0.8 = 0.96). To restore the original value after an increase of a% the required decrease is 100a/(100 + a)% (25% up needs a 20% fall because 1/1.25 = 0.8)."""),
           ("Average speed for equal distances is the harmonic mean",
            """Let the distance each way be d and the speeds u and v. Total time = d/u + d/v = d(u + v)/(uv). Average speed = total distance/total time = 2d / [d(u + v)/(uv)] = **2uv/(u + v)**. For 60 km/h and 40 km/h: 2·60·40/100 = 48 km/h, not the arithmetic mean 50, because more time is spent at the lower speed. If equal *times* are spent at each speed the average is the arithmetic mean (u + v)/2. For several equal-distance legs the harmonic mean generalises to n/(Σ 1/vᵢ)."""),
           ("Time and work: working together takes ab/(a + b)",
            """If A alone completes a job in a days his rate is 1/a of the job per day, and B's rate is 1/b. Working together their rates add: 1/a + 1/b = (a + b)/(ab) jobs per day, so the job takes the reciprocal ab/(a + b) days. For a = 12, b = 18: 216/30 = 7.2 days. Working together for 4 days they finish 4 × 5/36 = 5/9 of the job, leaving 4/9 for B alone at 1/18 per day: 8 days. Pipes and leaks use the same idea with negative rates for outlets; wages are shared in proportion to the work done (rate × time)."""),
           ("Circular permutations and the 'together' trick",
            """Arranging n distinct people on a line gives n! orders. Around a circle a rotation of everyone gives the same arrangement, and each circular arrangement corresponds to exactly n linear orders (its n rotations), so there are n!/n = (n − 1)! circular arrangements. If two particular people must sit together, glue them into one block: n − 1 objects in a circle give (n − 2)! arrangements, times 2 for the internal order of the block. For n = 6: (6 − 2)!·2 = 48. If they must **not** sit together: (n − 1)! − 2(n − 2)! = 120 − 48 = 72."""),
       ],
       notes=[
           ("Formula sheet",
            """Percentage = part/whole × 100; profit% = (SP − CP)/CP × 100; SP = CP(1 ± p/100); discount on marked price; SI = PRT/100; CI amount = P(1 + r/100)ᵗ; CI − SI for two years = P(r/100)²; ratio sharing: parts = T·aᵢ/Σa; alligation: quantities in the ratio (m₂ − m) : (m − m₁); speed = distance/time, km/h × 5/18 = m/s; train crossing a platform: (L + P)/v; relative speed: add for opposite directions, subtract for the same; boats: downstream u + v, upstream u − v; average of n numbers = sum/n; LCM × HCF = product of two numbers; number of divisors of p^a q^b = (a + 1)(b + 1); nCr = n!/(r!(n − r)!); AP sum n(a + l)/2, GP sum a(rⁿ − 1)/(r − 1)."""),
           ("Speed techniques",
            """Convert to fractions (1/8 = 12.5%, 1/6 = 16.67%); use the options to back-solve; estimate and eliminate; check units and the base of every percentage; for work problems use LCM of the days as the total work; for ratio problems introduce a multiplier (3x, 5x); for probability use complements ('at least one' = 1 − none); for counting draw cases and avoid double counting."""),
       ])

deepen("ga-logical-reasoning",
       proofs=[
           ("Contrapositive equivalence and the converse error",
            """The statement 'if P then Q' is false only when P is true and Q is false. Its contrapositive 'if not Q then not P' is false only when not Q is true and not P is false, i.e. when Q is false and P is true — the same single situation — so they are equivalent. The converse 'if Q then P' is false when Q is true and P is false, a different situation: for 'if it rains, the road is wet' the road may be wet because of a tanker, so the converse does not follow. 'P only if Q' means P ⇒ Q, 'P if Q' means Q ⇒ P, and 'P if and only if Q' is both. The negation of 'P ⇒ Q' is 'P and not Q'; the negation of 'All A are B' is 'Some A is not B'."""),
           ("Why 'All A are B' and 'Some B are C' give no conclusion about A and C",
            """Draw circle A inside circle B (all A are B). 'Some B are C' says circle C overlaps circle B somewhere. The overlap can lie in the part of B outside A (so no A is C) or can include part of A (so some A are C). Both diagrams satisfy the statements, so neither 'Some A are C' nor 'No A is C' is certain. A conclusion is valid only if it holds in **every** diagram consistent with the premises. By contrast, 'All A are B' and 'All B are C' force circle A inside C: 'All A are C' is certain. A systematic check: try to construct a counter-model; if you find one, the conclusion is not valid."""),
           ("Venn diagram counting for two and three sets",
            """For two sets, |A ∪ B| = |A| + |B| − |A ∩ B| because the intersection is counted twice in |A| + |B|. In a class of 60 with 35 in cricket, 30 in football and 10 in neither, |A ∪ B| = 50, so |A ∩ B| = 35 + 30 − 50 = 15. For three sets add the triple intersection back: |A ∪ B ∪ C| = Σ|A| − Σ|A ∩ B| + |A ∩ B ∩ C|. The number of elements in exactly one set is Σ|A| − 2Σ|A ∩ B| + 3|A ∩ B ∩ C|, in exactly two sets Σ|A ∩ B| − 3|A ∩ B ∩ C|. Fill the region with the triple intersection first and work outwards."""),
       ],
       notes=[
           ("Series, coding and arrangement problems",
            """Number series: examine differences (first and second), ratios, squares and cubes (n² ± k), alternating series, Fibonacci-like sums, primes. Letter series: convert to positions (A = 1 … Z = 26). Coding–decoding: find the rule by comparing a word and its code letter by letter (shift, reverse, position sum). Seating: draw the skeleton, place the most constrained person first, branch on the cases; in a circle facing the centre, 'left' of a person is the clockwise neighbour. Direction sense: track coordinates and compute the distance with Pythagoras. Blood relations: build the tree from the end of the statement and keep gender and generation straight. Truth-teller puzzles: assume a statement is true and test consistency."""),
           ("Common traps",
            """'Some' means at least one (it can include all). Possible is not certain. Check whether the question wants a valid inference, an assumption or a conclusion. For 'either–or' conclusions both complementary conclusions together may be valid even when neither is individually. In arrangements, double-check every given condition against the final layout. In series questions verify the pattern on all given terms, not just the first three."""),
       ])

deepen("ga-data-interpretation",
       proofs=[
           ("Percentage points versus percentage change",
            """A share rising from 20% to 25% increases by 5 **percentage points** (the arithmetic difference of the two percentages). The **relative** increase is the change divided by the original value: (25 − 20)/20 = 25%. The two measures answer different questions: points compare shares directly, relative change measures growth of the share itself. A fall from 25% to 20% is 5 points but a 20% relative decrease, showing the asymmetry between the two. Always identify which one a question asks for."""),
           ("Weighted average and the average of averages",
            """The overall average of groups with sizes n₁, n₂ and averages m₁, m₂ is (n₁m₁ + n₂m₂)/(n₁ + n₂), because the totals add: Σx = n₁m₁ + n₂m₂. For 40 students averaging 70 and 60 averaging 80 the combined average is (2800 + 4800)/100 = 76, not (70 + 80)/2 = 75; the simple mean is correct only when the groups have equal size. The weighted average lies between the two group averages, closer to the larger group's average: (m − m₁)/(m₂ − m) = n₂/n₁ (alligation). The same principle applies to mixtures, to average speed over unequal distances and to overall percentages over groups."""),
           ("Growth rates and compound annual growth",
            """If a quantity grows from V₀ to Vₙ over n periods, the **average growth per period** that compounds to the same result is the CAGR r with V₀(1 + r)ⁿ = Vₙ, so r = (Vₙ/V₀)^(1/n) − 1. It is not the arithmetic mean of the yearly percentage growths: growing 100 → 150 (+50%) and then 150 → 120 (−20%) gives a total of +20% over two years, a CAGR of √1.2 − 1 ≈ 9.5%, while the arithmetic mean of +50% and −20% would be +15%. A constant percentage growth of 28% from 250 to 320 predicts 320 × 1.28 ≈ 410 for the next period."""),
       ],
       notes=[
           ("Reading tables and charts",
            """Read the title, units (thousands, crores, percent of what?), axis scales (does the axis start at zero?), legends and footnotes before computing. In pie charts the angle of a slice is percentage × 3.6°. In bar and line charts the steepest segment is the largest change; stacked bars show part and total. For tables compute only what the question requires and cross-check with row and column totals. When several sources are combined (a pie chart percentage and a table total) convert everything into absolute numbers first."""),
           ("Estimation and approximation",
            """Round numbers to convenient values when the options are well separated: 48.7 ≈ 50, 123 ≈ 120. Use fraction equivalents for percentages (12.5% = 1/8, 16.67% = 1/6, 14.3% = 1/7, 8.33% = 1/12). Compare ratios by cross-multiplication: a/b > c/d ⇔ ad > bc (for positive b, d). Beware of questions that cannot be answered from the data ('cannot be determined') and of cumulative values mistaken for per-period values."""),
       ])


deepen("ga-numerical",
       notes=[
           ("Sequences and series (from the Discrete Mathematics notes)",
            """**Arithmetic progression:** aₙ = a + (n − 1)d, Sₙ = (n/2)[2a + (n − 1)d] = n(a + l)/2; the average of the terms equals the average of the first and last. **Geometric progression:** aₙ = a rⁿ⁻¹, Sₙ = a(1 − rⁿ)/(1 − r) (r ≠ 1) and S∞ = a/(1 − r) when |r| < 1. **Harmonic progression:** the reciprocals form an AP, so the nth term is 1/(a + (n − 1)d) where a and d belong to the reciprocal AP, and Sₙ = (1/d) ln((2a + (2n − 1)d)/(2a − d)) approximately for large n. Means of two positive numbers satisfy AM ≥ GM ≥ HM with AM·HM = GM². Standard sums: Σk = n(n + 1)/2, Σk² = n(n + 1)(2n + 1)/6, Σk³ = [n(n + 1)/2]², Σ(2k − 1) = n². Proof of the AP sum: write the series forwards and backwards; each of the n column sums equals a + l, so 2Sₙ = n(a + l)."""),
       ])
