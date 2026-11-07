"""General Aptitude — curated verbal ability + reasoning questions."""
from content.kit import C

C("GA", "Verbal Ability", "Sentence completion", [
    ("e", 1, "s", "The committee was ______ in its decision; not a single member disagreed.", ["unanimous", "divided", "reluctant", "arbitrary"], 0, "'Not a single member disagreed' means all agreed: unanimous."),
    ("e", 1, "s", "Despite her ______ efforts, she could not finish the project on time.", ["strenuous", "negligible", "careless", "lazy"], 0, "'Despite' signals contrast with failure, so the efforts were great."),
    ("e", 1, "s", "He is so ______ that he never accepts help from anyone.", ["independent", "dependent", "generous", "talkative"], 0, "Refusing help ⇒ independent."),
    ("e", 1, "s", "The new policy will ______ the rules to make them simpler.", ["streamline", "complicate", "confuse", "bury"], 0, "Make simpler = streamline."),
    ("m", 1, "s", "Although the film received ______ reviews from critics, it was a box-office success.", ["lukewarm", "glowing", "exuberant", "enthusiastic"], 0, "'Although' contrasts poor reviews with success."),
    ("m", 1, "s", "The scientist's theory, once ______ as absurd, is now widely accepted.", ["dismissed", "praised", "endorsed", "adopted"], 0, "Contrast with 'now widely accepted'."),
    ("m", 1, "s", "Her ______ remarks offended many, though she claimed she meant no harm.", ["tactless", "diplomatic", "gracious", "polite"], 0, "Offended many ⇒ lacking tact."),
    ("m", 2, "s", "The company's profits, which had ______ for years, finally began to recover.", ["stagnated", "soared", "flourished", "multiplied"], 0, "'Finally began to recover' implies a prior period of no growth."),
    ("h", 2, "s", "The author's prose is so ______ that readers often need to re-read sentences to grasp their meaning.", ["convoluted", "lucid", "succinct", "lyrical"], 0, "Needing to re-read implies tangled, hard-to-follow writing."),
    ("h", 2, "s", "Far from being ______, the new CEO proved to be an exceptionally decisive leader.", ["vacillating", "resolute", "assertive", "determined"], 0, "'Far from being X' + 'decisive' ⇒ X is indecisive."),
])

C("GA", "Verbal Ability", "Synonyms & antonyms", [
    ("e", 1, "s", "Choose the word most nearly SAME in meaning to 'ABUNDANT'.", ["Plentiful", "Scarce", "Rare", "Meagre"], 0, "Abundant = plentiful."),
    ("e", 1, "s", "Choose the word most nearly OPPOSITE in meaning to 'BENEVOLENT'.", ["Malevolent", "Kind", "Charitable", "Generous"], 0, "Benevolent = well-meaning; opposite = malevolent."),
    ("e", 1, "s", "Synonym of 'CANDID':", ["Frank", "Secretive", "Deceptive", "Shy"], 0, "Candid = open and honest."),
    ("e", 1, "s", "Antonym of 'EXPAND':", ["Contract", "Enlarge", "Stretch", "Grow"], 0, "Expand ↔ contract."),
    ("m", 1, "s", "Synonym of 'EPHEMERAL':", ["Transient", "Permanent", "Eternal", "Solid"], 0, "Ephemeral = short-lived."),
    ("m", 1, "s", "Antonym of 'VERBOSE':", ["Concise", "Wordy", "Talkative", "Lengthy"], 0, "Verbose = using too many words."),
    ("m", 1, "s", "Synonym of 'PRUDENT':", ["Cautious", "Reckless", "Hasty", "Careless"], 0, "Prudent = acting with care for the future."),
    ("m", 1, "s", "Antonym of 'OBSCURE':", ["Clear", "Vague", "Hidden", "Doubtful"], 0, "Obscure = unclear; opposite = clear."),
    ("h", 2, "s", "Synonym of 'LACONIC':", ["Brief", "Eloquent", "Verbose", "Argumentative"], 0, "Laconic = using very few words."),
    ("h", 2, "s", "Antonym of 'MAGNANIMOUS':", ["Petty", "Generous", "Noble", "Forgiving"], 0, "Magnanimous = generous in forgiving; opposite = petty."),
    ("h", 2, "s", "Synonym of 'OBSEQUIOUS':", ["Servile", "Rebellious", "Arrogant", "Independent"], 0, "Obsequious = excessively eager to please."),
    ("h", 2, "s", "Antonym of 'PERFUNCTORY':", ["Thorough", "Casual", "Superficial", "Hasty"], 0, "Perfunctory = done with minimal effort."),
])

C("GA", "Verbal Ability", "Grammar & usage", [
    ("e", 1, "s", "Choose the grammatically correct sentence.", ["Neither of the answers is correct.", "Neither of the answers are correct.", "Neither of the answer is correct.", "Neither of the answers were correct."], 0, "'Neither' takes a singular verb."),
    ("e", 1, "s", "Fill in the blank: She is good ______ mathematics.", ["at", "in", "on", "with"], 0, "'Good at' is the standard collocation."),
    ("e", 1, "s", "Select the correct sentence.", ["He has been working here since 2015.", "He is working here since 2015.", "He works here since 2015.", "He worked here since 2015."], 0, "'Since' with a point in time needs present perfect (continuous)."),
    ("e", 1, "s", "Fill in the blank: ______ honest man is respected by all.", ["An", "A", "The one", "No article"], 0, "'Honest' begins with a vowel sound."),
    ("m", 1, "s", "Choose the correct sentence.", ["The team has announced its decision.", "The team have announced its decision.", "The team has announced their decision.", "The team are announced its decision."], 0, "A collective noun treated as a unit takes a singular verb and pronoun."),
    ("m", 1, "s", "Choose the correct option: If I ______ you, I would apologise.", ["were", "was", "am", "be"], 0, "Subjunctive mood in a hypothetical condition."),
    ("m", 1, "s", "Select the sentence with correct usage of 'its/it's'.", ["It's clear that the company lost its way.", "Its clear that the company lost it's way.", "It's clear that the company lost it's way.", "Its clear that the company lost its' way."], 0, "'It's' = it is; 'its' = possessive."),
    ("m", 2, "s", "Identify the sentence free of errors.", ["Hardly had he arrived when the meeting began.", "Hardly he had arrived when the meeting began.", "Hardly had he arrived than the meeting began.", "Hardly did he arrived when the meeting began."], 0, "'Hardly … when' with inversion."),
    ("h", 2, "s", "Choose the correct sentence.", ["Each of the students has submitted his or her assignment.", "Each of the students have submitted their assignment.", "Each of the students are submitting his assignment.", "Each students has submitted their assignments."], 0, "'Each' is singular."),
    ("h", 2, "s", "Select the correctly punctuated sentence.", ["The manager, who was late, apologised.", "The manager who was late, apologised.", "The manager, who was late apologised.", "The manager who, was late apologised."], 0, "A non-restrictive clause is set off by commas on both sides."),
    ("h", 2, "s", "Choose the correct sentence.", ["The number of applicants has increased.", "The number of applicants have increased.", "A number of applicants has increased.", "The numbers of applicants has increased."], 0, "'The number of' takes a singular verb."),
])

C("GA", "Verbal Ability", "Analogies & odd one out", [
    ("e", 1, "s", "Doctor : Hospital :: Teacher : ?", ["School", "Student", "Book", "Chalk"], 0, "Workplace relation."),
    ("e", 1, "s", "Bird : Fly :: Fish : ?", ["Swim", "Water", "Scale", "Gill"], 0, "Primary mode of movement."),
    ("e", 1, "s", "Choose the odd one out.", ["Apple", "Banana", "Carrot", "Mango"], 2, "Carrot is a vegetable; the rest are fruits."),
    ("m", 1, "s", "Hot : Cold :: Light : ?", ["Dark", "Bright", "Lamp", "Sun"], 0, "Antonym pairs."),
    ("m", 1, "s", "Author : Book :: Composer : ?", ["Symphony", "Orchestra", "Note", "Concert"], 0, "Creator : creation."),
    ("m", 1, "s", "Choose the odd one out.", ["Triangle", "Square", "Sphere", "Pentagon"], 2, "A sphere is three-dimensional."),
    ("m", 2, "s", "Pen : Write :: Knife : ?", ["Cut", "Sharp", "Steel", "Kitchen"], 0, "Tool : function."),
    ("h", 2, "s", "Cacophony : Harmony :: Chaos : ?", ["Order", "Noise", "Confusion", "Disorder"], 0, "Antonym pairs: discord/harmony, chaos/order."),
    ("h", 2, "s", "Choose the odd one out.", ["Hydrogen", "Oxygen", "Water", "Nitrogen"], 2, "Water is a compound; the others are elements."),
    ("h", 2, "s", "Fossil : Past :: Seed : ?", ["Future", "Plant", "Soil", "Growth"], 0, "A fossil bears evidence of the past; a seed holds the promise of the future."),
])

C("GA", "Verbal Ability", "Idioms, critical reasoning & paragraphs", [
    ("e", 1, "s", "The idiom 'to bite the bullet' means", ["to face a painful situation bravely", "to eat quickly", "to speak harshly", "to avoid danger"], 0, "Endure something unpleasant."),
    ("e", 1, "s", "'A blessing in disguise' means", ["something good that seemed bad at first", "a curse", "a hidden enemy", "a religious ceremony"], 0, "A misfortune with a good outcome."),
    ("e", 1, "s", "'Once in a blue moon' means", ["very rarely", "very often", "at night", "never"], 0, "Rare occurrence."),
    ("m", 1, "s", "'To burn the midnight oil' means", ["to work late into the night", "to waste fuel", "to cause a fire", "to sleep early"], 0, "Studying/working at night."),
    ("m", 2, "s", "All the managers in the firm attended the workshop. Ravi did not attend. Which conclusion MUST be true?", ["Ravi is not a manager of the firm", "Ravi is a manager who was ill", "Ravi works in another firm", "The workshop was cancelled for Ravi"], 0, "If Ravi were a manager of the firm he would have attended."),
    ("m", 2, "s", "'Increasing the price of fuel will reduce its consumption.' Which statement WEAKENS this claim?", ["There are no substitutes for fuel for most users, so demand is largely unaffected by price", "Fuel is expensive", "Some people walk to work", "Fuel prices fluctuate every year"], 0, "Inelastic demand undercuts the claim."),
    ("h", 2, "s", "Arrange the sentences to form a coherent paragraph: (P) The invention of the printing press changed this. (Q) Before it, books were copied by hand and were rare. (R) Knowledge spread rapidly across Europe. (S) Printed books became cheap and plentiful.", ["Q P S R", "P Q R S", "Q S P R", "R S Q P"], 0, "Rare hand-copied books → printing press changed this → cheap books → spread of knowledge."),
    ("h", 2, "s", "A study found that people who drink coffee live longer. Which assumption must be questioned before concluding that coffee causes longer life?", ["Coffee drinkers may differ in other health-related ways (confounding variables)", "Coffee is a liquid", "Longevity is measured in years", "The study had more than one participant"], 0, "Correlation does not imply causation."),
    ("h", 2, "s", "The author argues that remote work boosts productivity, citing a survey of employees. The main weakness of this evidence is that", ["employees' self-reports may be biased and are not objective measures", "surveys are always illegal", "remote work is new", "productivity cannot be defined"], 0, "Self-reported data can be biased."),
])

C("GA", "Logical & Analytical Reasoning", "Syllogisms & statements", [
    ("e", 1, "s", "All cats are animals. Some animals are pets. Which conclusion follows?", ["No definite conclusion about cats being pets", "All cats are pets", "Some cats are pets", "No cat is a pet"], 0, "The overlap of 'animals' and 'pets' may not include cats."),
    ("e", 1, "s", "All engineers are graduates. All graduates are educated. Therefore", ["All engineers are educated", "All educated persons are engineers", "Some graduates are not educated", "No engineer is educated"], 0, "Transitivity of 'all'."),
    ("e", 1, "s", "Statement: Some books are pens. All pens are pencils. Conclusion: Some books are pencils.", ["Follows", "Does not follow", "Cannot be said", "Contradicts"], 0, "Books that are pens are pencils."),
    ("m", 1, "s", "No dog is a cat. All cats are mammals. Which must be true?", ["Some mammals are not dogs", "All mammals are cats", "No mammal is a dog", "All dogs are mammals"], 0, "Cats are mammals that are not dogs."),
    ("m", 2, "s", "If it rains, the match is cancelled. The match was not cancelled. What can be concluded?", ["It did not rain", "It rained", "The pitch was dry", "The match was played at night"], 0, "Modus tollens."),
    ("m", 2, "s", "Some A are B. All B are C. No C is D. Which MUST be true?", ["Some A are not D", "All A are C", "Some C are D", "No A is C"], 0, "Some A are B, hence C, hence not D."),
    ("h", 2, "s", "Five people P, Q, R, S, T stand in a line. P is to the left of Q. S is at the left end. Q is immediately to the left of T. How many different orders are possible?", ["3", "1", "2", "4"], 0, "With S first, the block QT and the persons P and R can be ordered with P before the block in 3 ways: S P R Q T, S P Q T R, S R P Q T."),
    ("h", 2, "s", "Statements: (I) Every member of the club is a voter. (II) Some voters are teachers. Conclusions: (A) Some members are teachers. (B) Some teachers are voters.", ["Only B follows", "Only A follows", "Both follow", "Neither follows"], 0, "B is the converse of II; A cannot be inferred."),
])

C("GA", "Logical & Analytical Reasoning", "Relations & arrangements", [
    ("e", 1, "s", "Pointing to a man, Rita says, 'He is the son of my mother's only brother.' How is the man related to Rita?", ["Cousin", "Brother", "Uncle", "Nephew"], 0, "Mother's brother's son = maternal cousin."),
    ("e", 1, "s", "A is B's sister. B is C's father. How is A related to C?", ["Paternal aunt", "Mother", "Maternal aunt", "Grandmother"], 0, "Sister of one's father is a paternal aunt."),
    ("m", 1, "s", "In a family, P is the father of Q, and Q is the sister of R. S is R's mother. How is S related to P?", ["Wife", "Sister", "Mother", "Daughter"], 0, "Q and R are siblings with father P and mother S."),
    ("m", 1, "s", "Four friends A, B, C, D sit around a square table facing the centre. A is opposite C. B is to the right of A. Who sits to the left of A?", ["D", "B", "C", "Cannot be determined"], 0, "Facing the centre, A's right is B, the left must be D."),
    ("m", 2, "s", "In a row of 40 students, Anil is 15th from the left and Binu is 12th from the right. How many students are between them?", ["12", "13", "11", "14"], 1, "Binu is 40 − 12 + 1 = 29th from the left; students between = 29 − 15 − 1 = 13."),
    ("h", 2, "s", "Among five people A, B, C, D, E: A is taller than B but shorter than C. D is taller than C. E is shorter than B. Who is the second tallest?", ["C", "A", "D", "B"], 0, "Order: D > C > A > B > E."),
    ("h", 2, "s", "Six people sit in a row. A and B must sit together. In how many ways can they be arranged?", ["240", "120", "720", "360"], 0, "Treat AB as a block: 5! × 2 = 240."),
])
