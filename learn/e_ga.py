"""Textbook-style long-form teaching text: General Aptitude."""
from learn import elab

elab("ga-verbal",
 ("What the verbal section tests", """
General Aptitude carries 15 marks in GATE, and about five of them come from verbal ability. The questions are short, but they reward habits rather than cramming: reading slowly enough to catch what a sentence is *actually* saying, and knowing a small set of grammar rules that account for most of the traps.

The verbal questions fall into five families:

- **Grammar and usage** — choose the correct verb form, article, preposition or tense.
- **Sentence completion** — fill one or two blanks so the whole sentence makes sense.
- **Vocabulary** — synonyms, antonyms, analogies, odd-one-out, idioms and one-word substitutions.
- **Para-jumbles and sentence ordering** — put shuffled sentences into a logical paragraph.
- **Reading comprehension and critical reasoning** — read a short passage and decide what it supports, assumes, or contradicts.

Each family has one simple way of thinking about it, which the next parts explain from scratch.
"""),
 ("Grammar from the ground up", """
A sentence needs a **subject** (who or what the sentence is about) and a **verb** (what the subject does or is). Almost every grammar error in an exam is a mismatch between the two, or between a word and the words around it.

**Rule 1 — the verb agrees with the subject, not with the nearest noun.** In "The *list* of items *is* long", the subject is *list* (singular), even though *items* is plural and sits right next to the verb. Phrases such as *along with*, *as well as*, *together with* and *in addition to* do not make the subject plural: "The teacher, along with her students, **is** going."

**Rule 2 — some words are always singular.** *Each, every, either, neither, one, everyone, nobody* take singular verbs: "Neither of the answers **is** correct."

**Rule 3 — "the number of" is singular, "a number of" is plural.** "The number of applicants **has** grown" but "A number of applicants **have** withdrawn."

**Rule 4 — tense sequence.** If one past event happened before another past event, use the **past perfect** for the earlier one: "By the time we arrived, the film **had started**."

**Rule 5 — articles depend on sound.** Use *an* before a vowel *sound* (an hour, an MBA) and *a* before a consonant sound (a university, a one-way street).

**Rule 6 — fixed prepositions.** Some words just go together: *allergic to*, *good at*, *interested in*, *capable of*, *different from*. These are learned by reading, not derived.

**Rule 7 — parallel structure.** Items in a list must have the same grammatical form: "She likes **reading**, **writing** and **painting**", not "reading, writing and to paint".
"""),
 ("Vocabulary as a skill, not a list", """
Memorising word lists helps a little, but exam vocabulary questions are mostly solved by **meaning clues** and **word parts**.

**Word parts.** Many English words are built from Latin and Greek pieces. *Bene-* means good (benevolent, benefit), *mal-* means bad (malevolent, malice), *anti-* means against, *pre-* means before, *-phobia* means fear, *-cracy* means rule (democracy, oligarchy). If you meet an unfamiliar word, take it apart.

**Synonyms and antonyms.** Read the question word carefully: some ask for the *opposite*. A common trap is giving the synonym as a wrong option in an antonym question. Always check which one is being asked before choosing.

**Analogies.** An analogy asks you to find a *relationship*. First say the relationship in a sentence: "A doctor works in a hospital." Then test each option with the same sentence. Common relationships are: tool and function (knife–cut), part and whole (page–book), cause and effect, degree (warm–hot), and person and workplace.

**Odd one out.** Find the category that three words share, then name it. "Sonnet, haiku, ode, novella": the first three are forms of poetry; the novella is prose.

**Idioms.** An idiom's meaning cannot be guessed from the individual words ("to burn the midnight oil" is about working late). The best way to retain them is to see each in a sentence.
"""),
 ("Sentence completion and para-jumbles", """
**Sentence completion.** Treat the blank as a missing clue. Read the *whole* sentence first and ask three things:

1. Is there a **contrast word** (*although, but, however, despite, yet*)? Then the blank is the opposite of the clue.
2. Is there a **support word** (*and, because, therefore, so*)? Then the blank agrees with the clue.
3. What is the **tone** — positive or negative? Eliminate options that go the other way.

For two-blank questions, check the first blank against the contrast or support word, eliminate, then verify the second blank on the remaining options.

**Para-jumbles.** A paragraph has a hidden logical order. Look for:

- **The opening sentence**: it introduces the topic and uses no pronoun that needs a previous sentence ("This", "These", "Such", "He").
- **Connectors**: *however, therefore, as a result, for example, yet* link a sentence to the one before it.
- **Pronouns and references**: "This reduces the risk" must come after the thing being reduced was mentioned.
- **Chronology and cause–effect**: events usually run in time order, and a cause comes before its effect.

Find the opening sentence and the closing sentence first; the middle usually falls into place.
"""),
 ("Critical reasoning and comprehension", """
Passages in GATE are short, so the real skill is **separating what the text says from what you imagine**.

**Reading comprehension.** Read the question first, then the passage. For *inference* questions, an option is correct only if the passage *supports* it directly. Be suspicious of options that use extreme words (*always, never, all, only*) when the passage is cautious (*often, some, may*).

**Critical reasoning** deals with arguments. An argument has a **conclusion** and **premises**; often there is an unstated **assumption** that connects them. The standard question types are:

- **Assumption**: what must be true for the conclusion to follow? (Try negating the option: if the argument collapses, it was an assumption.)
- **Strengthen / weaken**: give new information that makes the conclusion more or less likely. For a causal argument ("A happened, then B fell, so A caused the fall"), weakeners offer another cause (a confounding factor), and strengtheners rule such causes out.
- **Inference / deduction**: pick the statement that *must* be true if the premises are true.

**Deduction with 'all/some/no'.** Draw circles: "All A are B" puts the A-circle inside the B-circle. A conclusion follows only if it is true in *every* possible drawing.
"""),
 ("A practice routine that works", """
Verbal improves slowly and steadily; it does not respond to last-minute cramming. A simple routine:

- Read one good editorial or article each day, and underline every word whose meaning you only half know. Look them up and write one sentence each.
- Do five grammar items daily, and for every mistake write down the rule you broke.
- Practise para-jumbles by hiding the answer: find the opening sentence first, then the closing one.
- In the exam, verbal questions are the quickest marks in the paper. Aim to finish them in about 6 minutes in total, then spend the saved time elsewhere.
"""),
)

elab("ga-numerical",
 ("What 'numerical ability' means in GATE", """
These are questions you could solve with school mathematics, but under time pressure. The topics are percentages, ratio and proportion, averages, profit and loss, simple and compound interest, time–speed–distance, time and work, mixtures, ages, simple algebra, number properties, counting and probability, and basic geometry and mensuration.

The marks are modest (about 5 per paper), so the right goal is to be **fast and accurate on routine questions** and to skip the occasional long one. Every topic here reduces to one or two *ideas*; once you own the idea, the numbers are easy.
"""),
 ("Percentages, ratios and averages", """
A **percentage** is just a fraction with denominator 100. "$p\\%$ of $x$" is $\\frac{p}{100}\\times x$. Everything else follows.

**Percentage change.** If a value goes from $a$ to $b$, the change is $\\frac{b-a}{a}\\times 100\\%$. Always divide by the **old** value.

**Successive changes multiply.** A rise of 20% followed by a fall of 20% does *not* cancel: the factor is $1.2\\times 0.8 = 0.96$, a net fall of 4%.

**Ratios.** "A : B = 3 : 5" means that for every 3 parts of A there are 5 parts of B. Let A = 3k and B = 5k, then use the other facts of the problem to find k.

**Averages.** $\\text{average}=\\frac{\\text{sum}}{\\text{count}}$. The most useful trick is to work with the **sum**: if the average of 5 numbers is 20, their sum is 100. Removing a number changes the sum, then you recompute the average.

**Weighted average.** When groups of different sizes are combined, weight each group's average by its size.
"""),
 ("Time, speed, distance and work", """
**Speed = distance ÷ time.** Keep units consistent: to convert km/h to m/s multiply by $\\frac{5}{18}$; to convert m/s to km/h multiply by $\\frac{18}{5}$.

**Average speed** is *total distance ÷ total time*, never the average of speeds. When the two halves of a journey cover equal distances at speeds $u$ and $v$, the average speed is the harmonic mean $\\frac{2uv}{u+v}$.

**Trains.** To cross a pole, a train covers its own length. To cross a platform or another train, it covers the sum of the lengths. For trains moving in opposite directions, add the speeds; in the same direction, subtract them.

**Boats and streams.** Downstream speed = boat + stream; upstream speed = boat − stream.

**Time and work.** Think in **rates**. If A finishes a job in 10 days, A does $\\frac{1}{10}$ of the job per day. Rates of people working together *add*:

$$\\frac{1}{t}=\\frac{1}{a}+\\frac{1}{b}\\quad\\Longrightarrow\\quad t=\\frac{ab}{a+b}$$

The same idea handles pipes and cisterns: a filling pipe contributes a positive rate and a draining pipe a negative one.
"""),
 ("Interest, profit, mixtures and ages", """
**Simple interest** is $SI=\\frac{P\\,r\\,t}{100}$. **Compound interest** grows on the interest as well: the amount after $n$ years is $A=P\\left(1+\\frac{r}{100}\\right)^n$, and the interest is $A-P$. For two years the difference between CI and SI is $P\\left(\\frac{r}{100}\\right)^2$.

**Profit and loss.** Profit % is calculated on the **cost price**: $\\frac{SP-CP}{CP}\\times100$. A discount is calculated on the **marked price**. If goods are marked $m\\%$ above cost and sold at a $d\\%$ discount, the selling price is $CP(1+m/100)(1-d/100)$.

**Mixtures and alligation.** To mix two things of values $a<b$ to reach a mean $m$, the ratio of the quantities is $(b-m):(m-a)$ — the *distances* of the mean from the other value. A picture helps: put $a$ and $b$ on a number line with $m$ in between.

**Ages.** Translate the sentence into equations. Let the present ages be $x$ and $y$, then "after 5 years" means $x+5$ and $y+5$. Remember that the *difference* between two people's ages never changes.
"""),
 ("Number properties, counting and probability", """
**Divisibility and remainders.** A number's remainder repeats in a cycle when you take powers. To find the remainder of $7^{100}$ when divided by 5, note $7\\equiv2$ (mod 5), and the powers of 2 modulo 5 go $2,4,3,1,2,4,\\dots$ with a cycle of 4. Since $100$ is a multiple of 4, the remainder is 1.

**HCF and LCM.** For two numbers, $\\text{HCF}\\times\\text{LCM}=\\text{product}$. To count the divisors of $n=p^a q^b r^c$, use $(a+1)(b+1)(c+1)$.

**Counting.** The product rule: if one choice can be made in $m$ ways and then another in $n$ ways, together they can be made in $m\\times n$ ways. Arranging $n$ distinct things gives $n!$; if some are identical, divide by the factorial of each repeated group. Choosing $r$ items from $n$ (order irrelevant) gives $\\binom{n}{r}$.

**Probability.** $P(E)=\\frac{\\text{favourable outcomes}}{\\text{total equally likely outcomes}}$. For "at least one", compute the *complement*: $1-P(\\text{none})$. For draws without replacement, the probabilities for each draw change: $P(\\text{two reds})=\\frac{4}{10}\\times\\frac{3}{9}$.
"""),
 ("Exam strategy", """
- **Estimate first.** Many questions can be answered by rounding. If the options are far apart, a 5% error will not change your choice.
- **Use the options.** For tricky algebra, try substituting the options.
- **Check units** before you write the answer (hours vs minutes, km/h vs m/s).
- **Skip long calculations.** If a question needs more than about two minutes, mark it and come back.
"""),
)

elab("ga-logical-reasoning",
 ("What logical reasoning tests", """
Logical and analytical reasoning questions give you a small set of facts and ask what *must* follow. There is no outside knowledge involved; the whole skill is **organising information** so the answer becomes visible. A neat table or a quick diagram beats mental juggling every time.

The main families are: syllogisms; seating and ordering puzzles; blood relations; direction sense; coding and decoding; series and patterns; truth-teller/liar puzzles; counting figures; and (newer in GATE) **spatial** questions such as paper folding, cubes and transformations.
"""),
 ("Syllogisms and Venn diagrams", """
A syllogism gives statements using **all, some, no** and asks which conclusions *definitely* follow. The safe method is to draw circles.

- "All A are B": draw A completely inside B.
- "No A is B": draw two separate circles.
- "Some A are B": draw two overlapping circles (and the overlap is non-empty).

Then check each conclusion: it follows only if it is true in **every** diagram consistent with the statements. If you can draw one valid picture in which the conclusion fails, it does not follow.

Three useful facts: "No A is B" is the same as "No B is A"; "Some A are B" is the same as "Some B are A"; but "All A are B" does **not** give "All B are A". And two "some" statements, like "Some A are B" and "Some B are C", **never** give a definite link between A and C.
"""),
 ("Arrangements, rankings and relations", """
**Seating and ordering.** Draw the row or circle first. Place the people whose position is certain (a fixed end, or "opposite to"), then place the rest one clue at a time. In a circle of $n$ people, the person opposite position $i$ is at $i+\\frac{n}{2}$.

**Rank from both ends.** If a person is $a$-th from one end and $b$-th from the other, the total is $a+b-1$ (the person is counted twice).

**Blood relations.** Work in small steps and draw a family tree. Be careful with phrases like "my mother's only son", which means *the speaker himself* (or his brother if there is more than one son, but "only son" settles it). Translate each relation to a link, e.g. "father's brother" = paternal uncle.

**Direction sense.** Draw a compass cross and follow each turn. Facing north, a right turn leads to east; facing east, a right turn leads to south. For the final distance use Pythagoras' theorem when the path ends at a right angle from the start.
"""),
 ("Coding, series and puzzles", """
**Coding–decoding.** Compare the original word with its code letter by letter and look for a shift (+1, −1), a mirror (A↔Z, B↔Y), a reversal, or an alternating pattern. Once the rule is clear, apply it to the new word.

**Number and letter series.** Look at differences, then differences of differences; try ratios; check for squares, cubes or primes; and for letters convert to positions (A = 1 ... Z = 26).

**Truth-teller and liar puzzles.** Assume one person is honest, deduce what everyone else must be, and check whether any statement is contradicted. If it is, that assumption was wrong. Work systematically through the cases.

**Counting figures.** For an $n\\times n$ grid the number of squares of all sizes is $1^2+2^2+\\dots+n^2$, and the number of rectangles is $\\binom{n+1}{2}^2$.
"""),
 ("Spatial reasoning: folding, cubes and transformations", """
These questions train you to *picture* a change.

**Paper folding and punching.** Each fold doubles the number of layers. After folding twice there are 4 layers, so one hole punched through all of them yields 4 holes when you unfold. When a shape is cut from a folded edge, unfolding *reflects* it across the fold line.

**Painted cubes.** Cut an $n\\times n\\times n$ cube into unit cubes. Then: three painted faces = the 8 corners; two painted faces = $12(n-2)$ edge cubes; one painted face = $6(n-2)^2$; no painted face = $(n-2)^3$.

**Dice.** On a standard die opposite faces sum to 7. If you see three faces, the hidden faces are the opposites of the visible ones.

**Transformations of points.** Reflection in the line $y=x$ swaps the coordinates. A 90° anticlockwise rotation about the origin maps $(x,y)\\to(-y,x)$, and a clockwise one maps $(x,y)\\to(y,-x)$. Apply the steps in the order given.
"""),
)

elab("ga-data-interpretation",
 ("What data interpretation asks", """
You are given a table, a bar graph, a line graph or a pie chart (in this app, charts are shown as small tables of numbers) and asked to compute something: a total, an average, a percentage, a growth rate or a ratio. The mathematics is simple — the difficulty is *reading* the data correctly and not mixing up what each number represents.
"""),
 ("Reading data without mistakes", """
Before calculating anything, spend ten seconds on three checks:

1. **What are the units?** Are the numbers in rupees, in thousands, in units, in percentages?
2. **What does each row and column mean?** A common error is to read the wrong year or the wrong series.
3. **What exactly is the question asking for?** "How much more" is a difference; "how many times" is a ratio; "what percent more" divides the difference by the *base*.

Write down the formula you need *before* you read numbers into it.
"""),
 ("The calculations that appear again and again", """
$$\\text{percentage change}=\\frac{\\text{new}-\\text{old}}{\\text{old}}\\times100$$

$$\\text{share of the total}=\\frac{\\text{part}}{\\text{total}}\\times100$$

$$\\text{average}=\\frac{\\text{sum of values}}{\\text{number of values}}$$

**Ratio.** To compare two numbers, divide them. "Ratio of A to B" is $A:B$, not $B:A$.

**Growth over several years.** A total change over several years is *not* the sum of yearly percentage changes. Compute it from the start and end values.

**Pie charts.** A pie chart gives percentages of a total. To convert to an angle multiply by 3.6° per percentage point; to convert to an amount multiply the percentage by the total.
"""),
 ("Estimation and shortcuts", """
Exact arithmetic is often unnecessary. If the options are 12.5%, 25%, 37.5% and 50%, you only need to know roughly whether the answer is a quarter or a third. Round numbers (49.8 → 50), compare fractions by cross-multiplying, and compare two percentages by comparing the underlying fractions.

For "which is the largest" questions, compute only the candidates that could win. For "how many" questions over a table, mark the cells that satisfy the condition with a quick tick as you go.
"""),
 ("Data sufficiency", """
Some questions ask only whether the given statements are *enough* to answer a question, without asking for the answer. Test each statement alone, then both together. A statement that gives two possible values (like $x^2=9$) is **not** sufficient for "What is $x$?" on its own. Be careful not to use outside knowledge: judge only what the statements say.
"""),
)
