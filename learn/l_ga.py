"""General Aptitude: verbal ability, numerical ability, logical reasoning, data interpretation."""
import itertools
import math
from fractions import Fraction

from learn import Ex, lesson

S = "GA"


def syllogism_valid():
    """All A are B; some B are C. Does 'some A are C' follow? Search tiny models for a counter-example."""
    for bits in itertools.product((0, 1), repeat=8):
        # four universe elements, each in sets (A,B,C) encoded by 3 bits -> use 8 possible element types, choose a subset present
        types = [t for t in range(8) if bits[t]]
        if not types:
            continue
        A = lambda t: t & 1
        B = lambda t: t >> 1 & 1
        C = lambda t: t >> 2 & 1
        if all((not A(t)) or B(t) for t in types) and any(B(t) and C(t) for t in types) and not any(A(t) and C(t) for t in types):
            return False
    return True


def seatings_circular(n, together=None):
    perms = set()
    for p in itertools.permutations(range(n)):
        if p[0] == 0:
            perms.add(p)
    if together is None:
        return len(perms)
    a, b = together
    return sum(1 for p in perms if abs(p.index(a) - p.index(b)) in (1, n - 1))


# ======================================================================================================
lesson(subject=S, chapter="Verbal Ability", ch_no=1, no=1, slug="ga-verbal", title="Verbal Ability: Grammar, Vocabulary & Reading",
       topic="Verbal Ability", minutes=18, weight=3, widget="none",
       key="GATE verbal questions test grammar (tenses, agreement, prepositions), vocabulary (synonyms, antonyms, analogies, word usage), sentence completion and reading comprehension. A handful of rules and a systematic method — read, predict, eliminate — are enough for most of them.",
       analogy=("🧩", "Fitting the missing piece", "A sentence-completion question is a jigsaw with one gap. The surrounding words tell you the shape of the piece (positive or negative, contrast or support); you then look for the option with that shape rather than reading all options first."),
       sections=[
           dict(h="Grammar rules that decide most questions", md="""- **Subject–verb agreement:** the verb agrees with the true subject, not the nearest noun (*The list of items **is** long*). *Neither … nor* / *either … or* agree with the nearer subject; *each, every, one of, neither of* take singular verbs; *a number of* + plural, *the number of* + singular.
- **Tenses:** sequence of tenses (*If it rained, the match was cancelled*; *had been* for earlier past); *since* + point in time, *for* + duration with perfect tenses.
- **Conditionals:** type 1 *If + present, will*; type 2 *If + past, would*; type 3 *If + past perfect, would have*.
- **Articles:** *a/an* by sound (an hour, a university); *the* for specific or unique things.
- **Pronouns:** case (*between you and **me***), clear antecedents, *who* (people, subject) vs *whom* (object).
- **Prepositions & idioms:** *prefer A to B*, *different from*, *capable of*, *responsible for*, *comprise* (no *of*).
- **Parallel structure:** *He likes swimming, running and to cycle* ✘ → *swimming, running and cycling* ✔.
- **Modifiers:** a modifier must sit next to what it modifies (dangling-participle trap)."""),
           dict(h="Vocabulary: synonyms, antonyms, analogies and usage", md="""Learn words in families (roots, prefixes, suffixes: *bene-* good, *mal-* bad, *anti-* against, *-phobia* fear). For **antonyms** first find the meaning, then flip it; check the *connotation* (positive/negative). **Analogies** — identify the relationship (part–whole, cause–effect, degree, tool–use, synonym/antonym) in the stem and test each option with the same sentence: *"Drought is to famine as flood is to ___"*. **Word usage:** words that look alike (*affect/effect*, *principle/principal*, *complement/compliment*) — decide the part of speech needed first.

**Idioms and phrasal verbs** are best settled by elimination: remove options that are literally absurd, then choose by context."""),
           dict(h="Sentence completion and para-jumbles", md="""**Sentence completion:** (1) read the sentence with a blank, (2) note signal words — *but, although, however* signal contrast; *and, moreover, hence* signal continuation; *despite* flips the expected direction; (3) predict a word of the right tone before looking at options; (4) check both blanks if there are two.

**Para-jumbles:** find the **opening** sentence (introduces the topic, no pronoun without a referent), the **closing** (conclusion), and pairs linked by pronouns (*it, this, they*), connectors (*however, therefore*), or chronology. Build the chain of mini-pairs, then verify the whole order reads naturally."""),
           dict(h="Reading comprehension and critical reasoning", md="""Read the passage once for the **main idea** (first and last paragraphs, topic sentences); do not memorise details — return to the text for specific questions. Question types: main idea, inference (must be supported, not merely possible), tone, vocabulary-in-context, and *except/NOT* questions. Eliminate options that are **too extreme** (always, never, only), **out of scope**, or **reversed**.

**Critical reasoning:** identify the conclusion and premises, then decide whether the option *strengthens, weakens* or *assumes* it — an assumption is something that must be true for the argument to hold (negate it: if the argument collapses, it was necessary)."""),
       ],
       examples=[
           Ex("Subject–verb agreement", "Choose the correct form: ‘The number of applicants (is / are) increasing, but a number of them (is / are) unqualified.’",
              ["‘The number of’ refers to one quantity ⇒ singular **is**.", "‘A number of them’ means several people ⇒ plural **are**."],
              "**is … are**", verify=lambda: "is … are"),
           Ex("Conditional", "Complete: ‘If the committee had acted earlier, the damage ______ avoided.’",
              ["The past perfect in the if-clause signals a third conditional (unreal past).", "The main clause takes *would have* + past participle: ‘would have been avoided’."],
              "**would have been**", verify=lambda: "would have been"),
           Ex("Analogy", "Drought : Famine :: Flood : ?  (options: Rain, Displacement, River, Water)",
              ["Relationship: cause → consequence (drought causes famine).", "A flood causes displacement of people ⇒ **Displacement**."],
              "**Displacement**", verify=lambda: "Displacement"),
           Ex("Necessary assumption", "Argument: ‘The city should ban cars from the centre because pollution there exceeds safe limits.’ Which is a necessary assumption: (a) cars are the main source of that pollution, or (b) all citizens use public transport?",
              ["Negation test: if cars were *not* a significant source, banning them would not reduce pollution and the argument collapses ⇒ (a) is necessary.", "(b) is irrelevant: the argument does not require everyone to use public transport."],
              "**(a)**", verify=lambda: "(a)"),
       ],
       traps=[("Nearest-noun agreement", "Ignore interrupting phrases: ‘The box of apples is…’."),
              ("Extreme words", "Options with ‘always/never/only’ are rarely right in reading comprehension."),
              ("Confusable words", "Decide the part of speech first (effect = noun, affect = verb)."),
              ("Para-jumble starts", "A sentence that begins with a pronoun or connector cannot be the opener.")],
       quick=[("‘Neither the teacher nor the students ___ present.’", ["was", "were", "is", "has been"], 1, "Agrees with the nearer subject (students)."),
              ("‘He prefers tea ___ coffee.’", ["than", "to", "from", "over"], 1, "Prefer A to B."),
              ("A necessary assumption can be tested by", ["repeating it", "negating it", "ignoring it", "quoting the passage"], 1, "Negate it: if the argument fails it is necessary."),
              ("‘Although the plan was costly, it proved ___.’ The best word is", ["wasteful", "worthwhile", "unaffordable", "expensive"], 1, "‘Although’ signals contrast.")],
       summary=["Agreement: true subject, ‘the number of’ singular, ‘a number of’ plural, nearer subject with either/neither.", "Conditionals types 1–3; since/for; parallel structure; modifiers.", "Analogies: name the relationship, test each option.",
                "Sentence completion: signal words, predict first.", "Para-jumbles: opener, pronoun links, connectors, closing.", "RC: main idea first; eliminate extreme / out-of-scope options."])


# ======================================================================================================
lesson(subject=S, chapter="Numerical Ability", ch_no=2, no=1, slug="ga-numerical", title="Numerical Ability: Percentages, Ratios, Work, Speed & Counting",
       topic="Numerical Ability", minutes=26, weight=5, widget="none",
       key="GATE numerical questions reduce to a few templates: percentages and ratios, profit and interest, time–speed–distance, time and work, mixtures, averages, and basic counting and probability. Set up the relation, convert to fractions, and compute carefully.",
       analogy=("🧮", "Having a few reliable tools", "A craftsman who owns a hammer, a saw and a tape measure can build almost anything. In aptitude, ‘part ÷ whole’, ‘rate × time = amount’ and ‘total = sum of parts’ solve nearly every word problem."),
       sections=[
           dict(h="Percentages, ratios and averages", md="""- **Percentage change** = (new − old)/old × 100. Successive changes of a% and b%: net = a + b + ab/100 %. An increase of x% followed by a decrease of x% leaves **−x²/100 %**.
- **Ratio a : b** — parts of a whole total T are aT/(a+b) and bT/(a+b). Compounded ratios multiply. **Proportion:** if a:b = c:d then ad = bc.
- **Average** = sum / count; the *weighted* average uses weights. If the mean of n numbers changes by δ when one number is replaced, the number changed by nδ.
- **Mixtures (alligation):** mixing two quantities of means m₁ < m < m₂ in the ratio q₁ : q₂ = (m₂ − m) : (m − m₁).
- **Profit and loss:** profit % = (SP − CP)/CP × 100; marked price, discount % on marked price; successive discounts d₁, d₂ give net 1 − (1−d₁)(1−d₂).
- **Interest:** SI = PRT/100; CI amount = P(1 + r/100)ᵗ; difference CI − SI for 2 years = P(r/100)²."""),
           dict(h="Time, speed, distance and work", md="""- **Speed = distance / time.** Average speed for equal distances at speeds u and v = **2uv/(u + v)** (harmonic mean). Convert km/h → m/s by × 5/18.
- **Relative speed:** same direction subtract, opposite directions add. A train of length L crossing a pole takes L/v; crossing a platform of length P takes (L + P)/v. Boats: downstream u + v, upstream u − v.
- **Work:** if A alone takes a days, her rate is 1/a per day; rates add. A and B together: 1/(1/a + 1/b) = ab/(a + b). Pipes: inlet positive, outlet negative rate. Wages are shared in proportion to work done.
- **Clocks and calendars:** the minute hand gains 5.5° per minute on the hour hand; a non-leap year has 365 = 52 weeks + 1 odd day, a leap year 2 odd days.""",
                formulas=[("time together = ab / (a + b)", "two workers, a and b days alone"), ("average speed (equal distances) = 2uv / (u + v)", "harmonic mean")]),
           dict(h="Number properties and counting", md="""- **Divisibility:** by 3/9 digit sum; by 11 alternating digit sum; by 4 last two digits; by 8 last three. **LCM × HCF = product of the two numbers.** Number of divisors of p^a q^b is (a+1)(b+1). Remainders: (a·b) mod m = ((a mod m)(b mod m)) mod m. Unit digits cycle with period 4.
- **Permutations and combinations:** nPr = n!/(n−r)!, nCr = n!/(r!(n−r)!); arrangements of n objects with repeats n!/(a!b!…); circular arrangements (n − 1)!; objects together: treat as one block, multiply by the block's internal arrangements.
- **Probability:** favourable/total for equally likely outcomes; P(A or B) = P(A) + P(B) − P(A∩B); independent events multiply; conditional probability P(A∣B) = P(A∩B)/P(B).
- **Sequences:** AP aₙ = a + (n−1)d, sum n(a + l)/2; GP aₙ = arⁿ⁻¹, sum a(rⁿ − 1)/(r − 1)."""),
           dict(h="Approach for the exam", md="""Convert the words to equations first; use **fractions** instead of decimals (1/3, not 0.33); check units; estimate to eliminate options; and substitute option values in 'which of these' questions. Typical traps: base of a percentage (increase *on what*), 'and' vs 'or' in probability, forgetting to convert minutes to hours."""),
       ],
       examples=[
           Ex("Percentage trap", "A price is increased by 20% and then decreased by 20%. What is the net change?",
              ["Net factor = 1.2 × 0.8 = 0.96.", "The price is 4% lower: **−4 %** (matches −x²/100 = −4)."],
              "**−4 %**", verify=lambda: "%d %%" % round((1.2 * 0.8 - 1) * 100)),
           Ex("Time and work", "A can do a job in 12 days and B in 18 days. They work together for 4 days, then A leaves. How many more days does B need to finish?",
              ["In 4 days they do 4 × (1/12 + 1/18) = 4 × 5/36 = 5/9 of the job.", "Remaining 4/9 at B's rate 1/18 per day ⇒ 4/9 × 18 = **8** days."],
              "**8** days.", verify=lambda: str(float((1 - 4 * (Fraction(1, 12) + Fraction(1, 18))) / Fraction(1, 18))).rstrip("0").rstrip(".")),
           Ex("Average speed", "A car drives to a city at 60 km/h and returns over the same road at 40 km/h. What is its average speed for the round trip?",
              ["Equal distances ⇒ harmonic mean 2 × 60 × 40 / (60 + 40).", "= 4800/100 = **48 km/h** (not 50)."],
              "**48 km/h**", verify=lambda: "%d km/h" % (2 * 60 * 40 / (60 + 40))),
           Ex("Compound interest", "₹10,000 is invested at 10% compound interest per annum. What is the amount after 2 years, and how much more than simple interest is the interest?",
              ["Amount = 10,000 × 1.1² = 12,100. CI = 2,100.", "SI = 10,000 × 10 × 2/100 = 2,000, so CI − SI = **100**."],
              "Amount **12,100**; CI − SI = **100**.", verify=lambda: "Amount %d; CI − SI = %d" % (round(10000 * 1.1 ** 2), round(10000 * 1.1 ** 2 - 10000 - 2000))),
           Ex("Circular arrangement", "In how many ways can 6 people sit around a circular table if two particular people must sit together?",
              ["Treat the pair as one block: 5 objects in a circle ⇒ 4! = 24 arrangements; the pair can swap places: × 2.", "Total = **48**."],
              "**48**", verify=lambda: str(seatings_circular(6, (1, 2)))),
       ],
       traps=[("Percentage base", "A decrease after an increase is computed on the new value, not the original."),
              ("Average speed", "Use the harmonic mean for equal distances, total distance / total time otherwise."),
              ("Circular arrangements", "(n − 1)! because rotations are identical."),
              ("Probability: independence", "Multiply only independent events; for ‘at least one’ use 1 − P(none).")],
       quick=[("A 25% increase followed by what decrease restores the original?", ["20%", "25%", "30%", "15%"], 0, "1/1.25 = 0.8."),
              ("A and B finish in 6 and 12 days respectively. Together:", ["9 days", "4 days", "8 days", "3 days"], 1, "72/18."),
              ("Number of divisors of 72 = 2³·3²", ["6", "10", "12", "9"], 2, "(3+1)(2+1)."),
              ("The probability of getting at least one head in 3 tosses", ["1/8", "7/8", "3/8", "1/2"], 1, "1 − 1/8.")],
       summary=["Net percentage change a + b + ab/100; ±x% round trip = −x²/100 %.", "Rates add; two workers together ab/(a+b); equal-distance average speed 2uv/(u+v).", "Alligation for mixtures; profit/discount/interest formulas.",
                "nCr, nPr, circular (n−1)!, blocks ×internal arrangements.", "Divisor count (a+1)(b+1); LCM × HCF = product.", "Probability: add for ‘or’ (minus overlap), multiply for ‘and’ (independent)."])


# ======================================================================================================
lesson(subject=S, chapter="Reasoning", ch_no=3, no=1, slug="ga-logical-reasoning", title="Logical & Analytical Reasoning",
       topic="Logical & Analytical Reasoning", minutes=24, weight=4, widget="none",
       key="Reasoning questions test whether you can draw only the conclusions that necessarily follow: syllogisms and Venn diagrams, series and patterns, arrangements, directions, blood relations and truth-teller puzzles. Systematic diagrams and case-elimination beat intuition.",
       analogy=("🔍", "A detective's rule", "A detective accepts only what the clues force to be true. ‘Possible’ is not ‘certain’. Every reasoning question asks the same thing: given these statements, what must be true no matter how the unknowns are filled in?"),
       sections=[
           dict(h="Syllogisms and Venn diagrams", md="""Statements use **All A are B**, **No A is B**, **Some A are B**, **Some A are not B**.

- Draw the **most general** diagram consistent with the statements; a conclusion is valid only if it holds in **every** such diagram.
- ‘All A are B’ and ‘Some B are C’ ⇒ **no** certain relation between A and C (the C's of B may lie outside A). The classic valid chain is ‘All A are B’, ‘All B are C’ ⇒ ‘All A are C’; and ‘All A are B’, ‘Some A are C’ ⇒ ‘Some B are C’.
- ‘Some A are B’ is **symmetric** (⇒ ‘Some B are A’); ‘All A are B’ is not (‘All B are A’ does not follow).
- Negative statements: ‘No A is B’ ⇒ ‘No B is A’, and also ‘Some A are not B’ when A exists.
- With **either–or** conclusions, a pair of complementary conclusions may together be true when neither alone is."""),
           dict(h="Series, coding and number puzzles", md="""**Number series:** look at first differences, second differences, ratios, squares/cubes (n² ± k), primes, alternating patterns or the sum of the previous two terms. **Letter series:** convert letters to positions (A = 1 … Z = 26) and look for the same patterns. **Coding–decoding:** find the rule that maps letters/digits (shift by k, reverse order, position sum).

**Odd-one-out and analogies** in numbers: compare digit sums, parity, divisibility."""),
           dict(h="Arrangements, directions and relations", md="""- **Linear and circular seating:** make a skeleton diagram, place the most-constrained person first, then branch on cases. In a circle of n people the person opposite is n/2 positions away; ‘to the left’ depends on facing direction (facing the centre vs outside).
- **Direction sense:** track coordinates; distance = √(Δx² + Δy²); a right turn from North is East.
- **Blood relations:** build a family tree; ‘mother’s brother’ = maternal uncle; ‘father’s sister’s son’ = cousin. Use symbols (+ male, − female, = married).
- **Truth-teller / liar puzzles:** assume one statement true and check consistency; the number of consistent cases is often 1.
- **Venn counting:** |A ∪ B| = |A| + |B| − |A ∩ B|; with three sets include the triple intersection."""),
           dict(h="Logic problems and conditional statements", md="""‘If P then Q’ is equivalent to its **contrapositive** ‘if not Q then not P’; it is **not** equivalent to its converse (‘if Q then P’). ‘P only if Q’ means P ⇒ Q; ‘P if and only if Q’ is two-way. ‘Not (A and B)’ = ‘not A or not B’ (De Morgan). ‘Some’ means *at least one*, and does not imply ‘not all’."""),
       ],
       examples=[
           Ex("Syllogism", "Statements: All engineers are graduates. Some graduates are artists. Does it follow that some engineers are artists?",
              ["Draw engineers inside graduates; the artists that overlap graduates may be in the part outside engineers.", "So the conclusion does not necessarily follow: **No**."],
              "**No**", verify=lambda: "No" if not syllogism_valid() else "Yes"),
           Ex("Number series", "Find the next term: 2, 6, 12, 20, 30, ?",
              ["Differences are 4, 6, 8, 10 — increasing by 2.", "Next difference 12 ⇒ 30 + 12 = **42** (the terms are n(n+1))."],
              "**42**", verify=lambda: str(6 * 7)),
           Ex("Direction sense", "A man walks 4 km north, turns right and walks 3 km, then turns right and walks 4 km. How far is he from the start and in what direction?",
              ["After 4 km N and 3 km E he is at (3, 4); the last leg southwards 4 km brings him to (3, 0).", "Distance = **3 km**, due East of the start."],
              "**3 km**, east.", verify=lambda: "%d km, east" % math.hypot(3, 0)),
           Ex("Venn counting", "In a class of 60, 35 like cricket, 30 like football and 10 like neither. How many like both?",
              ["Students liking at least one sport = 60 − 10 = 50.", "|C ∩ F| = 35 + 30 − 50 = **15**."],
              "**15**", verify=lambda: str(35 + 30 - (60 - 10))),
       ],
       traps=[("Possible vs certain", "A conclusion must hold in every consistent diagram."),
              ("Converse error", "‘If P then Q’ does not give ‘if Q then P’."),
              ("Left and right", "Depends on which way the person faces."),
              ("‘Some’", "Means at least one — it may include ‘all’.")],
       quick=[("‘All A are B’ implies", ["All B are A", "Some B are A", "No B is A", "Some A are not B"], 1, "Some B are A (if A exists)."),
              ("The contrapositive of ‘If it rains, the road is wet’", ["If the road is wet it rains", "If the road is not wet it does not rain", "If it does not rain the road is dry", "none"], 1, "Negate and swap."),
              ("Next in 1, 4, 9, 16, ?", ["20", "24", "25", "36"], 2, "Squares."),
              ("A person turns right while facing north and now faces", ["west", "east", "south", "north"], 1, "East.")],
       summary=["Syllogisms: most general diagram; ‘some’ is symmetric; All–Some chains give no certain link.", "Series: differences, ratios, squares, alternating patterns.", "Arrangements: skeleton diagram, constrained person first; directions: coordinates.",
                "Blood relations via family tree; Venn: inclusion–exclusion.", "If P then Q ≡ contrapositive, not converse.", "Truth-teller puzzles: test cases for consistency."])


# ======================================================================================================
lesson(subject=S, chapter="Data Interpretation", ch_no=4, no=1, slug="ga-data-interpretation", title="Data Interpretation: Tables, Charts & Estimation",
       topic="Data Interpretation", minutes=20, weight=3, widget="none",
       key="Data-interpretation questions give a table or chart (bar, line, pie, scatter) and ask for percentages, ratios, growth rates, averages or comparisons. Read the title, units and axes first, then compute only what the question needs and estimate to save time.",
       analogy=("📊", "Reading a map", "A chart is a map of numbers. Before looking for a route, check the legend (units), the scale (axes) and what the map actually covers (title). Most wrong answers come from misreading the legend, not from bad arithmetic."),
       sections=[
           dict(h="Reading the data correctly", md="""1. Read the **title, units** (thousands? crores? percent of what?) and **axis scales** (does the axis start at zero?).
2. Identify whether values are **absolute** or **relative** (percentages of a total that differs by category).
3. For **pie charts** each slice is part of a total; the angle of a slice for p% is 3.6° per percent.
4. Check for **missing information**: some questions are unanswerable and the correct option says ‘cannot be determined’.
5. Combine two sources carefully (percentage × total from another chart)."""),
           dict(h="Core calculations", md="""- **Percentage share** = part / total × 100; **percentage of a percentage** multiply fractions.
- **Growth rate** = (final − initial)/initial × 100; **CAGR** over n periods = (final/initial)^(1/n) − 1; average annual growth is not the arithmetic mean of yearly rates.
- **Ratio comparison:** compare fractions by cross-multiplication (a/b > c/d ⇔ ad > bc), not by decimals.
- **Average / weighted average** across categories; **percentage-point difference** vs **percentage change** (from 20% to 25% is 5 points, a 25% rise).
- **Estimation:** round numbers (e.g. 48.7 → 50, 123 → 120) when options are far apart; use approximate fractions (1/8 = 12.5%, 1/6 ≈ 16.7%, 1/7 ≈ 14.3%)."""),
           dict(h="Chart-specific hints", md="""- **Bar and line charts:** slope shows rate of change; steepest segment = largest change; read values at the same x-position for comparisons; stacked bars show part and total.
- **Tables:** compute only the cells needed; use column totals to cross-check.
- **Scatter plots:** look at the trend, not individual values; correlation is not causation.
- **Mixed (pie + table) sets:** convert everything to absolute numbers once, then answer the questions from a small worked table."""),
           dict(h="Common pitfalls", md="""Mixing **units** (thousands vs lakhs); computing the percentage with the wrong base; averaging percentages without weights; reading **cumulative** values as yearly values; misreading a truncated axis as a huge difference. Always ask: *percentage of what?* Finally, sanity-check each answer against the chart: a result larger than the total, a share above 100%, or a growth figure that contradicts the visible trend means a slip in reading the data."""),
       ],
       examples=[
           Ex("Growth rate", "Sales were 250 units in 2022 and 320 in 2023. What is the percentage growth, and what would 2024 sales be if the same percentage growth continues?",
              ["Growth = (320 − 250)/250 = 28 %.", "2024 = 320 × 1.28 = **409.6** ≈ 410 units."],
              "**28 %**; ≈ **410** units.", verify=lambda: "%d %%; ≈ %d units" % (round((320 - 250) / 250 * 100), round(320 * 1.28))),
           Ex("Pie chart", "A pie chart shows spending: Rent 30%, Food 25%, Travel 15%, Savings 20%, Others 10%. For a total income of ₹80,000, how much is saved, and what angle does Travel subtend?",
              ["Savings = 20% × 80,000 = ₹16,000.", "Travel angle = 15 × 3.6° = **54°**."],
              "₹**16,000** and **54°**.", verify=lambda: "₹%d and %d°" % (0.20 * 80000, 15 * 3.6)),
           Ex("Percentage points", "A party's vote share rose from 20% to 25%. What is the increase in percentage points, and the percentage increase in share?",
              ["Percentage points: 25 − 20 = 5.", "Relative increase: 5/20 = 25 %."],
              "**5** points; **25 %** increase.", verify=lambda: "%d points; %d %% increase" % (25 - 20, (25 - 20) / 20 * 100)),
           Ex("Weighted average", "Class A (40 students) averages 70 marks and class B (60 students) averages 80. What is the combined average?",
              ["Total marks = 40 × 70 + 60 × 80 = 2800 + 4800 = 7600.", "Average = 7600/100 = **76** (not 75)."],
              "**76**", verify=lambda: "%d" % ((40 * 70 + 60 * 80) / 100)),
       ],
       traps=[("Percent vs percentage points", "A rise from 20% to 25% is 5 points but a 25% increase."),
              ("Average of averages", "Weight by group sizes."),
              ("Wrong base", "Always check what the percentage is of."),
              ("Units and axes", "Look for thousands/crores and truncated axes before comparing.")],
       quick=[("A pie-chart slice of 25% subtends", ["25°", "60°", "90°", "100°"], 2, "25 × 3.6."),
              ("Compare fractions a/b and c/d by", ["subtracting", "cross-multiplying", "adding", "guessing"], 1, "ad vs bc."),
              ("Mean of 40 values at 70 and 60 values at 80", ["75", "76", "77", "78"], 1, "Weighted."),
              ("From 40 to 50 is a rise of", ["10 %", "20 %", "25 %", "50 %"], 2, "10/40.")],
       summary=["Read title, units and axes first.", "Share = part/total; growth = (final − initial)/initial; CAGR uses roots.", "Percentage points differ from percentage change.",
                "Use weighted averages; compare fractions by cross-multiplication.", "Estimate with round numbers and common fractions.", "Pie slice angle = percentage × 3.6°."])
