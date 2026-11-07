"""General Aptitude — curated LOGICAL / ANALYTICAL / SPATIAL reasoning.
Row: (difficulty, marks, kind[s=single,n=numerical], text, options, answer, full explanation)."""
from content.kit import C

L = "Logical & Analytical Reasoning"
SYL = ["Only conclusion I follows", "Only conclusion II follows", "Both I and II follow", "Neither I nor II follows"]

C("GA", L, "Syllogisms", [
    ("e", 1, "s", "Statements: All pens are books. All books are tables.\nConclusions: I. All pens are tables. II. Some tables are pens.", SYL, 2,
     "Chaining 'All pens are books' and 'All books are tables' gives 'All pens are tables' (I follows).\nIf every pen is a table, then at least one table is a pen, so 'Some tables are pens' also follows (II). Both follow."),
    ("e", 1, "s", "Statements: Some doctors are teachers. All teachers are engineers.\nConclusions: I. Some doctors are engineers. II. All engineers are teachers.", SYL, 0,
     "The doctors who are teachers are engineers (all teachers are), so I follows.\nII reverses the second statement ('All teachers are engineers' does not mean all engineers are teachers). Only I follows."),
    ("m", 1, "s", "Statements: No cat is a dog. All dogs are animals.\nConclusions: I. No cat is an animal. II. Some animals are not cats.", SYL, 1,
     "Dogs are animals and no dog is a cat, so those animals (the dogs) are not cats: II follows.\nI would need cats to be outside the animal class, which the statements do not say. Only II follows."),
    ("m", 1, "s", "Statements: All flowers are plants. Some plants are trees.\nConclusions: I. Some flowers are trees. II. Some trees are plants.", SYL, 1,
     "'Some plants are trees' converts directly to 'Some trees are plants' (II follows).\nThe trees among the plants may not be flowers, so I is not guaranteed. Only II follows."),
    ("m", 1, "s", "Statements: Some A are B. Some B are C.\nConclusions: I. Some A are C. II. Some C are A.", SYL, 3,
     "Two 'some' statements share the middle term B, but the B's that are A need not be the B's that are C. Nothing definite can be said about A and C, so neither conclusion follows."),
    ("m", 1, "s", "Statements: All A are B. No B is C.\nConclusions: I. No A is C. II. No C is A.", SYL, 2,
     "Every A is a B, and no B is a C, so no A is a C (I). A universal negative is symmetric, so 'No C is A' (II) also follows. Both follow."),
    ("h", 2, "s", "Statements: Some books are pens. No pen is a pencil.\nConclusions: I. Some books are not pencils. II. Some pencils are not books.", SYL, 0,
     "The books that are pens cannot be pencils, so some books are not pencils: I follows.\nNothing is known about pencils outside books: II does not follow. Only I follows."),
    ("h", 2, "s", "Statements: All A are B. All C are B.\nConclusions: I. All A are C. II. Some A are C.", SYL, 3,
     "A and C are both inside B but may be completely separate regions of it. Neither 'All A are C' nor 'Some A are C' is forced. Neither follows."),
    ("h", 2, "s", "Statements: No X is Y. Some X are Z.\nConclusions: I. Some Z are not Y. II. Some Y are Z.", SYL, 0,
     "The X's that are Z cannot be Y (no X is Y), so some Z are not Y: I follows. II would need a Y that is also Z, which the statements do not provide. Only I follows."),
])

C("GA", L, "Blood relations", [
    ("e", 1, "s", "Pointing to a man, Rita says, 'He is the son of my mother's only brother.' How is the man related to Rita?", ["Cousin", "Brother", "Uncle", "Nephew"], 0,
     "Rita's mother's brother is her maternal uncle. The uncle's son is Rita's cousin."),
    ("e", 1, "s", "P is the brother of Q. Q is the sister of R. R is the father of S. How is P related to S?", ["Uncle", "Father", "Cousin", "Brother"], 0,
     "P and Q are siblings, and Q and R are siblings, so P is R's brother. R is S's father, so P is S's uncle."),
    ("m", 1, "s", "A is B's sister. C is B's mother. D is C's father. How is A related to D?", ["Granddaughter", "Daughter", "Niece", "Sister"], 0,
     "A and B are siblings, so A is also C's child — a daughter of C. D is C's father, so D is A's grandfather and A is D's granddaughter."),
    ("m", 1, "s", "Pointing to a woman, a man says, 'She is the daughter of my mother's only son.' How is the woman related to the man?", ["Daughter", "Sister", "Niece", "Wife"], 0,
     "The man's mother's only son is the man himself. So the woman is his daughter."),
    ("m", 1, "s", "Introducing a man, a woman says, 'His wife is the only daughter of my father.' How is the woman related to the man?", ["Wife", "Sister", "Mother", "Daughter"], 0,
     "The only daughter of the woman's father is the woman herself. She is therefore the man's wife."),
    ("h", 2, "s", "In a code, 'A + B' means A is the mother of B; 'A − B' means A is the brother of B; 'A × B' means A is the sister of B. Which expression means P is the maternal uncle of R?", ["P − Q + R", "P + Q − R", "P × Q + R", "R + Q − P"], 0,
     "A maternal uncle is a brother of one's mother. P − Q: P is the brother of Q. Q + R: Q is the mother of R. So 'P − Q + R' says P is brother of Q, who is the mother of R.\nP + Q − R makes P the mother of R; P × Q + R makes P a maternal aunt; R + Q − P points the other way."),
])

C("GA", L, "Seating arrangements", [
    ("e", 1, "s", "Five persons A, B, C, D, E sit in a row facing north. C sits at the extreme left. E sits at the extreme right. B sits immediately to the right of A. D sits between B and E. Who sits in the middle?", ["B", "A", "D", "C"], 0,
     "Positions 1–5 from the left: C is 1 and E is 5. A and B are adjacent with B to the right of A, and D is between B and E, so the three middle seats are A, B, D in that order: C A B D E.\nThe middle (3rd) person is B."),
    ("m", 2, "s", "Six friends P, Q, R, S, T, U sit around a circular table facing the centre. P is opposite S. Q is the next person clockwise from P. R is opposite Q. T is not adjacent to P. Who sits opposite T?", ["U", "P", "Q", "S"], 0,
     "Number seats 1–6 clockwise. P = 1, so S (opposite) = 4. Q is the next clockwise from P: Q = 2, and R (opposite Q) = 5. Seats 3 and 6 remain for T and U; seat 6 is adjacent to P, so T = 3 and U = 6.\nT (3) is opposite seat 6, which is U."),
    ("e", 1, "s", "Five books are stacked. The Maths book is above Physics but below Chemistry. Biology is immediately above Physics. English is at the bottom. Which book is third from the top?", ["Biology", "Maths", "Physics", "Chemistry"], 0,
     "English is 5th. Among the top four, Chemistry is above Maths, which is above Physics, and Biology sits directly on Physics. The only fit is Chemistry, Maths, Biology, Physics from the top.\nThe third from the top is Biology."),
    ("m", 1, "n", "In a queue, Aman is 7th from the front and 12th from the back. How many people are in the queue?", [], 18,
     "Total = (position from front) + (position from back) − 1 = 7 + 12 − 1 = 18, because Aman is counted in both."),
    ("m", 1, "n", "Rohan ranks 9th from the top and 18th from the bottom in a class. How many students are in the class?", [], 26,
     "Total = 9 + 18 − 1 = 26."),
])

C("GA", L, "Ranking & order", [
    ("e", 1, "s", "A is taller than B but shorter than C. D is taller than C. E is shorter than B. Who is the second tallest?", ["C", "A", "D", "E"], 0,
     "Chaining the statements: D > C > A > B > E. The second tallest is C."),
    ("m", 1, "s", "In a race of five runners, B finished ahead of A but behind C. D finished immediately ahead of E but behind A. Who finished second?", ["B", "A", "C", "D"], 0,
     "C is ahead of B, and B is ahead of A. D and E come after A, with D directly ahead of E. The finishing order is C, B, A, D, E, so B is second."),
    ("h", 2, "n", "In a row of boys facing north, Ajay is 6th from the left and Vijay is 9th from the right. If they interchange positions, Ajay becomes 14th from the left. How many boys are in the row?", [], 22,
     "After interchanging, Ajay stands where Vijay stood, so Vijay's original place was 14th from the left. He was also 9th from the right, so the row has 14 + 9 − 1 = 22 boys."),
    ("h", 2, "n", "In a class, Ravi ranks 12th from the top. Sita ranks 8 places below Ravi and is 5th from the bottom. How many students are in the class?", [], 24,
     "Sita's rank from the top is 12 + 8 = 20. She is 5th from the bottom, so the class has 20 + 5 − 1 = 24 students."),
])

C("GA", L, "Truth & lies puzzles", [
    ("m", 1, "s", "On an island, knights always tell the truth and knaves always lie. A says, 'B is a knave.' B says, 'A and I are of the same type.' What are A and B?", ["A is a knight and B is a knave", "Both are knights", "Both are knaves", "A is a knave and B is a knight"], 0,
     "Try A = knave: then A's statement is false, so B is a knight. But then B's statement ('same type') would be false, which a knight cannot say. Contradiction.\nTry A = knight: B is a knave, and B's statement 'same type' is indeed false, as a knave would say. Consistent."),
    ("h", 2, "s", "Exactly one of A, B, C tells the truth. A: 'B is a liar.' B: 'C is a liar.' C: 'A and B are both liars.' Who tells the truth?", ["B", "A", "C", "Nobody"], 0,
     "Test each: if A were truthful, B is a liar, so B's claim 'C is a liar' is false, making C truthful as well — two truth-tellers, contradiction. If C were truthful, A and B are liars, but then A's claim 'B is a liar' would be true — contradiction.\nIf B is truthful, C is a liar, and A's claim is false (A liar) and C's claim is false (C liar). Exactly one truth-teller: B."),
    ("h", 2, "s", "Four friends Arun, Bala, Chitra and Divya each own a different pet: dog, cat, parrot, fish. Arun owns neither the cat nor the fish. Bala owns the parrot. Chitra does not own the fish. Who owns the fish?", ["Divya", "Arun", "Bala", "Chitra"], 0,
     "Arun cannot have cat, fish, or the parrot (Bala's), so Arun has the dog. The cat and fish remain for Chitra and Divya; Chitra does not own the fish, so Chitra has the cat and Divya has the fish."),
])

C("GA", L, "Coding-decoding", [
    ("e", 1, "s", "In a code, COMPUTER is written as DPNQVUFS. How is MONITOR written in that code?", ["NPOJUPS", "LNMHSNQ", "NPOJTPS", "OPOJUPS"], 0,
     "Each letter is moved one place forward: C→D, O→P, M→N, ... So M→N, O→P, N→O, I→J, T→U, O→P, R→S, giving NPOJUPS."),
    ("m", 1, "s", "In a code, FLOWER is written as EMNXDS. How is GARDEN written in that code?", ["FBQEDO", "HBSEFO", "FBSEDO", "HZQCFM"], 0,
     "Compare letter by letter: F→E (−1), L→M (+1), O→N (−1), W→X (+1), E→D (−1), R→S (+1): the shifts alternate −1, +1.\nApply to GARDEN: G−1=F, A+1=B, R−1=Q, D+1=E, E−1=D, N+1=O → FBQEDO."),
    ("e", 1, "n", "If A = 1, B = 2, C = 3, ..., Z = 26, what is the sum of the letter values of the word GATE?", [], 33,
     "G = 7, A = 1, T = 20, E = 5. Sum = 7 + 1 + 20 + 5 = 33."),
    ("m", 1, "s", "In a code language, 'sky is blue' is 'pa ne ki', 'blue sea deep' is 'ki ro la', and 'deep is dark' is 'ro ne mo'. What is the code for 'sea'?", ["la", "ro", "ki", "pa"], 0,
     "'blue' is the only word common to the first two sentences, and 'ki' is the only code common to them: blue = ki. Likewise 'deep' = ro (second and third), and 'is' = ne (first and third).\nIn the second sentence 'blue sea deep' = ki, ro, la, so 'sea' = la."),
    ("h", 2, "s", "In a certain code, CAT is written as XZG. How is DOG written in that code?", ["WLT", "WLS", "XLT", "VLT"], 0,
     "C(3)→X(24), A(1)→Z(26), T(20)→G(7): each letter is replaced by its mirror in the alphabet (position p → 27 − p).\nD(4)→23=W, O(15)→12=L, G(7)→20=T, so DOG → WLT."),
])

C("GA", L, "Direction sense", [
    ("e", 1, "s", "A man walks 5 km north, turns right and walks 3 km, then turns right again and walks 5 km. Where is he with respect to the starting point?", ["3 km east", "3 km west", "8 km east", "13 km north"], 0,
     "North 5 km, then east 3 km (a right turn from north), then south 5 km (a right turn from east). The north and south legs cancel, leaving him 3 km east of the start."),
    ("m", 1, "n", "Rahul walks 10 m south, turns left and walks 20 m, then turns left and walks 10 m. How far (in m) is he from the starting point?", [], 20,
     "Facing south, a left turn points east: 20 m east. Facing east, a left turn points north: 10 m north, which cancels the 10 m south. He ends 20 m east of the start."),
    ("e", 1, "n", "A starts from point O, walks 8 m north, then turns east and walks 6 m. How far (in m) is A from O?", [], 10,
     "The path forms a right triangle with legs 8 and 6, so the straight-line distance is √(8² + 6²) = √100 = 10 m."),
    ("m", 1, "s", "A person faces north. He turns 135° clockwise and then 180° anticlockwise. Which direction is he facing now?", ["North-west", "South-west", "North-east", "South-east"], 0,
     "Measure bearings clockwise from north: 135° clockwise puts him at 135° (south-east). Turning 180° anticlockwise subtracts 180°: 135° − 180° = −45° ≡ 315°, which is north-west."),
    ("h", 1, "s", "One morning, after sunrise, Ram and Shyam stand facing each other at a crossing. Ram's shadow falls exactly to his right. Which direction is Shyam facing?", ["North", "South", "East", "West"], 0,
     "In the morning the sun is in the east, so shadows fall towards the west. Ram's right-hand side is west, which means he is facing south (facing south, west is on your right). Shyam faces Ram, so he faces north."),
])

C("GA", L, "Series & patterns", [
    ("e", 1, "s", "Find the next term: B, E, H, K, ?", ["N", "M", "O", "L"], 0,
     "The letters advance by 3 each time (B=2, E=5, H=8, K=11), so the next is 14 = N."),
    ("e", 1, "s", "Find the next term: AZ, BY, CX, ?", ["DW", "DX", "EW", "DV"], 0,
     "The first letters go forwards A, B, C, D and the second letters go backwards Z, Y, X, W. Next: DW."),
    ("m", 1, "s", "Find the next term: Z, X, U, Q, ?", ["L", "M", "K", "N"], 0,
     "Positions: 26, 24, 21, 17. The differences are −2, −3, −4, so the next difference is −5: 17 − 5 = 12 = L."),
    ("m", 1, "s", "Find the odd one out: 8, 27, 64, 100, 125, 216", ["100", "64", "125", "216"], 0,
     "8, 27, 64, 125 and 216 are perfect cubes (2³, 3³, 4³, 5³, 6³). 100 is a square, not a cube."),
    ("h", 2, "n", "In the sequence 2, 6, 12, 20, 30, ... what is the 10th term?", [], 110,
     "The terms are n(n + 1): 1·2, 2·3, 3·4, 4·5, 5·6. The 10th term is 10 × 11 = 110."),
    ("h", 2, "n", "How many squares of all sizes are there in a 4 × 4 grid of unit squares?", [], 30,
     "Count by size: 1×1 → 16, 2×2 → 9, 3×3 → 4, 4×4 → 1. Total 16 + 9 + 4 + 1 = 30."),
    ("h", 2, "n", "How many rectangles (including squares) are there in a 3 × 3 grid of unit squares?", [], 36,
     "A rectangle is fixed by choosing 2 of the 4 vertical lines and 2 of the 4 horizontal lines: C(4,2) × C(4,2) = 6 × 6 = 36."),
    ("h", 2, "n", "An equilateral triangle has each side divided into 3 equal parts and lines are drawn parallel to the sides through the division points, forming 9 small triangles. How many triangles of all sizes are in the figure?", [], 13,
     "Upward-pointing triangles: side 1 → 6, side 2 → 3, side 3 → 1, total 10. Downward-pointing: side 1 → 3 (none of side 2 fits). Total 10 + 3 = 13."),
])

C("GA", L, "Paper folding & cutting", [
    ("m", 1, "n", "A square paper is folded in half along a vertical line and then in half again along a horizontal line. One hole is punched through all layers, away from the folds. How many holes are there when the paper is unfolded?", [], 4,
     "Two folds make 2 × 2 = 4 layers. A punch through all layers makes one hole per layer, so 4 holes, one in each quarter."),
    ("m", 1, "n", "A rectangular paper is folded in half three times. A hole is punched through all the layers, away from any fold. How many holes appear when it is fully unfolded?", [], 8,
     "Each fold doubles the number of layers: 2³ = 8 layers, so 8 holes."),
    ("m", 1, "s", "A square paper is folded in half. A semicircle is cut out with its diameter along the fold line. What is the shape of the hole after unfolding?", ["A full circle", "A semicircle", "An ellipse", "Two separate semicircles"], 0,
     "The unfolded paper is the mirror image of the folded one across the fold line. A semicircle with its diameter on the fold joins its mirror image to form a complete circle."),
    ("h", 1, "s", "A square paper is folded in half. From the fold, a small square (one side lying along the fold) is cut out. After unfolding, the hole is", ["a rectangle twice as long as it is wide", "a square", "a triangle", "two separate squares"], 0,
     "The cut square lies along the fold. Unfolding reflects it, producing two squares joined along the fold line: a rectangle whose length along the perpendicular is twice the side."),
])

C("GA", L, "Cubes & dice", [
    ("m", 1, "n", "A cube painted red on all faces is cut into 27 equal small cubes (3 × 3 × 3). How many small cubes have exactly two faces painted?", [], 12,
     "Cubes with exactly two painted faces lie on the edges, excluding corners. A 3 × 3 × 3 cube has 12 edges and (3 − 2) = 1 such cube per edge: 12 × 1 = 12."),
    ("m", 1, "n", "A cube painted on all faces is cut into 64 equal small cubes (4 × 4 × 4). How many small cubes have no face painted?", [], 8,
     "The unpainted cubes form the inner (4 − 2)³ = 2³ = 8 cube."),
    ("h", 2, "n", "A cube of side 5 cm is painted on all faces and cut into 1 cm cubes. How many of the small cubes have exactly one face painted?", [], 54,
     "Each face contributes an inner (5 − 2)² = 9 cubes with only that face painted. 6 faces × 9 = 54."),
    ("m", 1, "n", "The numbers on opposite faces of a die add up to 7. Three mutually adjacent faces show 2, 3 and 6. What is the sum of the numbers on the three hidden faces?", [], 10,
     "The hidden faces are opposite to the visible ones: opposite of 2 is 5, of 3 is 4, of 6 is 1. Their sum is 5 + 4 + 1 = 10. (Check: all faces total 21, and 21 − 11 = 10.)"),
])

C("GA", L, "Spatial transformation", [
    ("m", 1, "s", "The point (2, 3) is reflected in the line y = x and then rotated 90° anticlockwise about the origin. Where does it end up?", ["(−2, 3)", "(2, −3)", "(−3, 2)", "(3, −2)"], 0,
     "Reflection in y = x swaps the coordinates: (2, 3) → (3, 2). A 90° anticlockwise rotation sends (x, y) → (−y, x): (3, 2) → (−2, 3)."),
    ("m", 1, "s", "The point (4, −1) is rotated 90° clockwise about the origin and then reflected in the x-axis. Where does it end up?", ["(−1, 4)", "(1, 4)", "(−1, −4)", "(4, 1)"], 0,
     "A 90° clockwise rotation sends (x, y) → (y, −x): (4, −1) → (−1, −4). Reflection in the x-axis changes the sign of y: (−1, −4) → (−1, 4)."),
    ("h", 1, "s", "A square with vertices (0, 0), (2, 0), (2, 2), (0, 2) is translated by (3, −1) and then reflected in the y-axis. Where does the vertex that started at (2, 2) end up?", ["(−5, 1)", "(5, 1)", "(−1, 1)", "(−5, −1)"], 0,
     "Translate: (2, 2) → (5, 1). Reflect in the y-axis (x → −x): (5, 1) → (−5, 1)."),
])

C("GA", L, "Calendars & clocks", [
    ("m", 1, "s", "If 5 March 2024 is a Tuesday, what day of the week is 5 March 2025?", ["Wednesday", "Tuesday", "Thursday", "Monday"], 0,
     "The leap day (29 Feb 2024) falls before 5 March 2024, so the span 5 Mar 2024 → 5 Mar 2025 has 365 days = 52 weeks + 1 day. The weekday moves forward by one: Wednesday."),
    ("m", 1, "s", "At what time between 4 o'clock and 5 o'clock are the hands of a clock together?", ["4:21 9/11", "4:20", "4:22", "4:24"], 0,
     "At 4:00 the minute hand is 20 minute-spaces behind the hour hand. The minute hand gains 55/60 of a space per minute, so it needs 20 ÷ (55/60) = 240/11 = 21 9/11 minutes."),
    ("m", 1, "n", "What is the angle (in degrees) between the hour and minute hands of a clock at 3:40?", [], 130,
     "Hour hand: 3 × 30 + 40 × 0.5 = 110°. Minute hand: 40 × 6 = 240°. Difference = 130° (already less than 180°)."),
])
