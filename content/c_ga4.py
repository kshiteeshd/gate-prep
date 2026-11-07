"""General Aptitude — curated NUMERICAL ABILITY and DATA INTERPRETATION.
Row: (difficulty, marks, kind[s=single,n=numerical], text, options, answer, full explanation[, tolerance])."""
from content.kit import C

N = "Numerical Ability"
D = "Data Interpretation"

C("GA", N, "Pipes & cisterns", [
    ("e", 1, "n", "Pipe A fills a tank in 12 hours and pipe B fills it in 18 hours. If both are opened together, in how many hours is the tank full? (up to 2 decimals)", [], 7.2,
     "Rates add. In one hour A fills 1/12 of the tank and B fills 1/18.\nTogether: 1/12 + 1/18 = 3/36 + 2/36 = 5/36 per hour.\nTime = 36/5 = 7.2 hours.", 0.01),
    ("m", 1, "n", "Pipe A fills a tank in 10 hours; pipe B empties it in 15 hours. Both are opened together with the tank initially empty. In how many hours is the tank full?", [], 30,
     "Net rate = 1/10 − 1/15 = 3/30 − 2/30 = 1/30 per hour, so it takes 30 hours."),
    ("h", 2, "n", "A tap fills a tank in 6 hours. Because of a leak at the bottom it takes 8 hours. If the tap is closed, in how many hours would the leak alone empty the full tank?", [], 24,
     "Leak rate = tap rate − net rate = 1/6 − 1/8 = 4/24 − 3/24 = 1/24 per hour.\nSo the leak empties a full tank in 24 hours."),
])

C("GA", N, "Boats & streams", [
    ("m", 1, "n", "A boat goes 30 km upstream in 6 hours and 30 km downstream in 3 hours. What is the speed of the boat in still water (km/h)?", [], 7.5,
     "Upstream speed = 30/6 = 5 km/h; downstream speed = 30/3 = 10 km/h.\nStill-water speed = (upstream + downstream)/2 = (5 + 10)/2 = 7.5 km/h. (The current is (10 − 5)/2 = 2.5 km/h.)", 0.01),
    ("m", 2, "n", "A boat's speed in still water is 12 km/h and the stream flows at 3 km/h. How many hours does it take to travel 45 km downstream and return the same 45 km upstream?", [], 8,
     "Downstream speed = 12 + 3 = 15 km/h → 45/15 = 3 h.\nUpstream speed = 12 − 3 = 9 km/h → 45/9 = 5 h.\nTotal = 3 + 5 = 8 hours."),
])

C("GA", N, "Partnerships", [
    ("m", 1, "n", "A, B and C invest Rs 5000, Rs 8000 and Rs 12000 for the same period. The profit is Rs 25000. What is C's share (in Rs)?", [], 12000,
     "Profit is shared in the ratio of investments (equal time): 5 : 8 : 12, a total of 25 parts.\nC gets 12/25 × 25000 = Rs 12000."),
    ("h", 2, "n", "A invests Rs 6000 for 12 months and B invests Rs 9000 for 8 months. The profit is Rs 4200. What is A's share (in Rs)?", [], 2100,
     "Share is proportional to investment × time: A = 6000 × 12 = 72000; B = 9000 × 8 = 72000. The ratio is 1 : 1, so A gets half of 4200 = Rs 2100."),
])

C("GA", N, "Mixtures & alligation", [
    ("m", 1, "n", "How many litres of water must be added to 20 litres of a 40% alcohol solution to make it a 25% solution?", [], 12,
     "Alcohol in 20 L = 0.40 × 20 = 8 L. For this to be 25% of the final mixture, the total volume must be 8 / 0.25 = 32 L.\nWater to add = 32 − 20 = 12 L."),
    ("m", 1, "s", "In what ratio should rice costing Rs 40 per kg be mixed with rice costing Rs 60 per kg to obtain a mixture worth Rs 52 per kg?", ["2 : 3", "3 : 2", "1 : 2", "3 : 4"], 0,
     "By alligation: (dearer − mean) : (mean − cheaper) = (60 − 52) : (52 − 40) = 8 : 12 = 2 : 3 (cheaper : dearer)."),
])

C("GA", N, "Permutations & combinations", [
    ("e", 1, "n", "In how many distinct ways can the letters of the word LEVEL be arranged?", [], 30,
     "5 letters with E repeated twice and L repeated twice: 5! / (2! × 2!) = 120 / 4 = 30."),
    ("m", 1, "n", "A committee of 3 is to be chosen from 5 men and 4 women so that it contains at least one woman. In how many ways can this be done?", [], 74,
     "Total committees = C(9, 3) = 84. Committees with no woman (all men) = C(5, 3) = 10.\nAt least one woman: 84 − 10 = 74."),
    ("m", 1, "n", "How many 4-digit even numbers can be formed using the digits 1, 2, 3, 4, 5 without repetition?", [], 48,
     "The last digit must be 2 or 4: 2 choices. The remaining three places are filled from the other 4 digits in 4 × 3 × 2 = 24 ways. Total = 2 × 24 = 48."),
    ("h", 2, "n", "In how many distinct ways can the letters of MISSISSIPPI be arranged?", [], 34650,
     "11 letters: I ×4, S ×4, P ×2, M ×1.\n11! / (4! 4! 2!) = 39916800 / (24 × 24 × 2) = 39916800 / 1152 = 34650."),
])

C("GA", N, "Probability", [
    ("e", 1, "s", "Two fair dice are thrown. What is the probability that the sum of the numbers is 9?", ["1/9", "1/12", "5/36", "1/6"], 0,
     "Favourable outcomes: (3,6), (4,5), (5,4), (6,3) = 4 out of 36, so P = 4/36 = 1/9."),
    ("m", 1, "s", "A bag contains 4 red and 6 blue balls. Two balls are drawn one after another without replacement. What is the probability that both are red?", ["2/15", "4/25", "1/5", "3/10"], 0,
     "P(first red) = 4/10. Given that, P(second red) = 3/9.\nProduct = (4/10)(3/9) = 12/90 = 2/15."),
    ("m", 1, "s", "A card is drawn at random from a standard deck of 52 cards. What is the probability that it is a king or a heart?", ["4/13", "17/52", "1/4", "5/13"], 0,
     "There are 4 kings and 13 hearts, but the king of hearts is counted twice: 4 + 13 − 1 = 16 cards.\nP = 16/52 = 4/13."),
    ("m", 1, "s", "In a family with 3 children, assuming each child is equally likely to be a boy or a girl, what is the probability that exactly two are girls?", ["3/8", "1/4", "1/2", "1/8"], 0,
     "Out of 2³ = 8 equally likely sequences, the ones with exactly two girls are GGB, GBG, BGG = 3. P = 3/8."),
    ("h", 2, "s", "A fair coin is tossed 4 times. What is the probability of getting at least 3 heads?", ["5/16", "1/4", "3/8", "1/2"], 0,
     "Exactly 3 heads: C(4,3) = 4 ways; exactly 4 heads: 1 way. Favourable = 5 out of 2⁴ = 16, so P = 5/16."),
])

C("GA", N, "Progressions", [
    ("m", 1, "n", "What is the sum of the first 20 terms of the series 3, 7, 11, 15, ...?", [], 820,
     "Arithmetic progression with a = 3, d = 4. S₂₀ = (20/2)[2·3 + 19·4] = 10 × (6 + 76) = 820."),
    ("m", 1, "n", "What is the sum to infinity of 1 + 1/2 + 1/4 + 1/8 + ...?", [], 2,
     "Geometric series with a = 1 and r = 1/2 (|r| < 1): S = a/(1 − r) = 1/(1/2) = 2."),
    ("h", 2, "n", "In a geometric progression the third term is 12 and the sixth term is 96. What is the first term?", [], 3,
     "T₆ / T₃ = r³ = 96/12 = 8, so r = 2. T₃ = a r² = 4a = 12, so a = 3."),
])

C("GA", N, "Number system", [
    ("m", 1, "n", "What is the remainder when 7¹⁰⁰ is divided by 5?", [], 1,
     "7 ≡ 2 (mod 5). Powers of 2 modulo 5 cycle with period 4 (2, 4, 3, 1). Since 100 is a multiple of 4, 2¹⁰⁰ ≡ 1."),
    ("m", 1, "n", "What is the remainder when 2⁵⁰ is divided by 7?", [], 4,
     "2³ = 8 ≡ 1 (mod 7), so powers repeat every 3. 50 = 3 × 16 + 2, hence 2⁵⁰ ≡ 2² = 4."),
    ("m", 1, "n", "The product of two positive integers is 2160 and their HCF is 12. What is their LCM?", [], 180,
     "For two numbers, HCF × LCM = product. LCM = 2160 / 12 = 180."),
    ("m", 1, "n", "How many positive divisors does 900 have?", [], 27,
     "900 = 2² × 3² × 5². The number of divisors is (2 + 1)(2 + 1)(2 + 1) = 27."),
    ("h", 2, "n", "How many trailing zeros does 100! have?", [], 24,
     "Trailing zeros come from factors of 5: ⌊100/5⌋ + ⌊100/25⌋ = 20 + 4 = 24 (there are always enough 2s)."),
    ("m", 1, "n", "What is the smallest positive integer that leaves remainder 3 when divided by each of 4, 5 and 6?", [], 63,
     "The number minus 3 must be a common multiple of 4, 5, 6: LCM = 60. So the smallest such number is 60 + 3 = 63."),
])

C("GA", N, "Logarithms & indices", [
    ("e", 1, "n", "If log₂ x = 5 and log₃ y = 3, what is x + y?", [], 59,
     "x = 2⁵ = 32 and y = 3³ = 27, so x + y = 59."),
    ("e", 1, "n", "If 2^(x+1) = 32, what is x?", [], 4,
     "32 = 2⁵, so x + 1 = 5 and x = 4."),
    ("m", 1, "n", "What is the value of 8^(2/3) × 27^(1/3)?", [], 12,
     "8^(2/3) = (8^(1/3))² = 2² = 4, and 27^(1/3) = 3. Product = 4 × 3 = 12."),
    ("m", 1, "s", "What is the value of log₁₀(0.001)?", ["−3", "3", "−2", "0.001"], 0,
     "0.001 = 10⁻³, so log₁₀ 0.001 = −3."),
])

C("GA", N, "Mensuration & coordinate geometry", [
    ("e", 1, "n", "A cylinder has radius 7 cm and height 10 cm. What is its volume in cm³? (take π = 22/7)", [], 1540,
     "V = πr²h = (22/7) × 49 × 10 = 22 × 7 × 10 = 1540 cm³."),
    ("m", 1, "s", "A cone has base radius 3 cm and slant height 5 cm. What is its curved surface area?", ["15π cm²", "30π cm²", "12π cm²", "24π cm²"], 0,
     "Curved surface area = πrl = π × 3 × 5 = 15π cm²."),
    ("m", 1, "n", "A rectangle has perimeter 40 cm and area 96 cm². What is the length of its longer side (in cm)?", [], 12,
     "l + w = 20 and lw = 96, so l and w are roots of t² − 20t + 96 = 0 → (t − 12)(t − 8) = 0. The longer side is 12 cm."),
    ("e", 1, "n", "What is the distance between the points (1, 2) and (4, 6)?", [], 5,
     "Distance = √((4 − 1)² + (6 − 2)²) = √(9 + 16) = 5."),
    ("m", 1, "n", "What is the area of the triangle with vertices (0, 0), (4, 0) and (0, 3)?", [], 6,
     "It is a right triangle with legs 4 and 3: area = ½ × 4 × 3 = 6."),
    ("m", 1, "n", "What is the slope of the line passing through (2, 3) and (6, 11)?", [], 2,
     "Slope = (11 − 3)/(6 − 2) = 8/4 = 2."),
    ("h", 2, "s", "What is the length of the diagonal of a cube of side 6 cm?", ["6√3 cm", "6√2 cm", "12 cm", "36 cm"], 0,
     "The space diagonal of a cube of side a is a√3. For a = 6, it is 6√3 ≈ 10.39 cm."),
])

C("GA", N, "Work, age & average problems", [
    ("m", 1, "n", "A can do a job in 10 days and B in 15 days. They work together for 4 days and then A leaves. In how many more days does B finish the remaining work?", [], 5,
     "Together they do 1/10 + 1/15 = 1/6 of the work per day; in 4 days, 4/6 = 2/3 is done. Remaining 1/3 at B's rate 1/15 per day takes (1/3)/(1/15) = 5 days."),
    ("m", 1, "n", "3 men or 6 women can finish a job in 20 days. How many days will 2 men and 4 women take?", [], 15,
     "3 men = 6 women, so 1 man = 2 women. The job is 6 × 20 = 120 woman-days. 2 men + 4 women = 4 + 4 = 8 women, so the time is 120/8 = 15 days."),
    ("m", 1, "n", "A father is three times as old as his son. After 12 years he will be twice as old as the son. What is the son's present age?", [], 12,
     "Let the son be x years, the father 3x. After 12 years: 3x + 12 = 2(x + 12) = 2x + 24, so x = 12."),
    ("m", 1, "n", "The average of five numbers is 20. When one number is removed, the average of the remaining four becomes 18. What is the removed number?", [], 28,
     "The sum of five numbers is 100; the sum of the remaining four is 4 × 18 = 72. The removed number is 100 − 72 = 28."),
    ("e", 1, "n", "A's salary is 25% more than B's. By what percent is B's salary less than A's?", [], 20,
     "Take B = 100, so A = 125. B is 25 less than A: 25/125 = 20%.", 0.01),
])

C("GA", N, "Speed, interest & algebra", [
    ("m", 1, "n", "A train 150 m long crosses a pole in 10 seconds. How long (in seconds, up to 2 decimals) will it take to cross a platform 250 m long?", [], 26.67,
     "Speed = 150/10 = 15 m/s. Distance to cover = train + platform = 150 + 250 = 400 m. Time = 400/15 = 26.67 s.", 0.02),
    ("m", 1, "n", "Two trains of lengths 120 m and 180 m run in opposite directions at 54 km/h and 36 km/h. How many seconds do they take to cross each other?", [], 12,
     "Relative speed = 54 + 36 = 90 km/h = 25 m/s. Distance = 120 + 180 = 300 m. Time = 300/25 = 12 s."),
    ("m", 1, "n", "A car covers the first half of a journey at 40 km/h and the second half (same distance) at 60 km/h. What is its average speed in km/h?", [], 48,
     "For equal distances the average speed is the harmonic mean: 2 × 40 × 60 / (40 + 60) = 4800/100 = 48 km/h."),
    ("m", 1, "n", "What is the compound interest (in Rs) on Rs 10000 at 10% per annum for 2 years, compounded annually?", [], 2100,
     "Amount = 10000 × 1.1² = 12100. Interest = 12100 − 10000 = Rs 2100."),
    ("h", 2, "n", "What is the difference (in Rs) between the compound interest and the simple interest on Rs 5000 at 8% per annum for 2 years?", [], 32,
     "For two years the difference is P(r/100)² = 5000 × (0.08)² = 5000 × 0.0064 = Rs 32."),
    ("m", 1, "n", "If x + 1/x = 5, what is x² + 1/x²?", [], 23,
     "Square both sides: x² + 2 + 1/x² = 25, so x² + 1/x² = 23."),
    ("m", 1, "n", "If α and β are the roots of x² − 5x + 6 = 0, what is α² + β²?", [], 13,
     "α + β = 5 and αβ = 6, so α² + β² = (α + β)² − 2αβ = 25 − 12 = 13. (The roots are 2 and 3: 4 + 9 = 13.)"),
])

C("GA", N, "Estimation & comparison", [
    ("e", 1, "s", "Estimate the value of (49.8 × 20.1) / 9.9.", ["About 100", "About 110", "About 90", "About 125"], 0,
     "Round to 50 × 20 / 10 = 100. The exact value is 1000.98/9.9 ≈ 101."),
    ("m", 1, "s", "Which is larger, 2³⁰ or 3²⁰?", ["3²⁰", "2³⁰", "They are equal", "Cannot be determined"], 0,
     "Write both with exponent 10: 2³⁰ = (2³)¹⁰ = 8¹⁰ and 3²⁰ = (3²)¹⁰ = 9¹⁰. Since 9 > 8, 3²⁰ is larger."),
    ("m", 1, "s", "The value of √50 is closest to", ["7.07", "6.5", "7.5", "8.0"], 0,
     "7² = 49 and 7.1² = 50.41, so √50 is just above 7, about 7.07."),
    ("m", 1, "n", "In a group of 100 people, 60 like tea, 50 like coffee and 20 like neither. How many like both?", [], 30,
     "People who like at least one drink: 100 − 20 = 80. By inclusion–exclusion: 60 + 50 − both = 80, so both = 30."),
])

C("GA", D, "Table interpretation", [
    ("m", 1, "n", "Annual sales (units) of four products:\n```\nYear   P     Q     R     S\n2021   120   150   90    200\n2022   140   135   110   220\n2023   160   180   100   210\n```\nWhat were the total sales of all products in 2022?", [], 605,
     "Add the 2022 row: 140 + 135 + 110 + 220 = 605."),
    ("m", 1, "s", "Annual sales (units) of four products:\n```\nYear   P     Q     R     S\n2021   120   150   90    200\n2022   140   135   110   220\n2023   160   180   100   210\n```\nWhich product showed the highest percentage growth in sales from 2021 to 2023?", ["P", "Q", "R", "S"], 0,
     "Growth from 2021 to 2023: P = 40/120 = 33.3%, Q = 30/150 = 20%, R = 10/90 = 11.1%, S = 10/200 = 5%. P is highest."),
    ("h", 2, "s", "Annual sales (units) of four products:\n```\nYear   P     Q     R     S\n2021   120   150   90    200\n2022   140   135   110   220\n2023   160   180   100   210\n```\nIn which year was product Q's share of the total sales highest?", ["2023", "2021", "2022", "It is the same every year"], 0,
     "Totals: 2021 = 560, 2022 = 605, 2023 = 650.\nQ's share: 150/560 = 26.8%, 135/605 = 22.3%, 180/650 = 27.7%. The highest is 2023."),
    ("m", 2, "s", "Marks of five students:\n```\nStudent  Maths  Physics  Chem\nA        80     70       90\nB        60     85       75\nC        90     65       70\nD        70     75       80\nE        100    90       60\n```\nWhich student has the highest average mark?", ["E", "A", "C", "D"], 0,
     "Totals: A = 240, B = 220, C = 225, D = 225, E = 250. E has the highest total and hence the highest average (83.3)."),
    ("m", 1, "n", "Marks of five students:\n```\nStudent  Maths  Physics  Chem\nA        80     70       90\nB        60     85       75\nC        90     65       70\nD        70     75       80\nE        100    90       60\n```\nWhat is the class average in Physics?", [], 77,
     "(70 + 85 + 65 + 75 + 90) / 5 = 385 / 5 = 77."),
    ("m", 1, "n", "Marks of five students:\n```\nStudent  Maths  Physics  Chem\nA        80     70       90\nB        60     85       75\nC        90     65       70\nD        70     75       80\nE        100    90       60\n```\nThe highest Chemistry mark is what percent more than the lowest Chemistry mark?", [], 50,
     "Highest = 90 (A), lowest = 60 (E). Increase = 30, and 30/60 = 50%."),
])

C("GA", D, "Bar & line graphs (tabulated)", [
    ("m", 1, "n", "A company's revenue and expenses (Rs crore):\n```\nYear   Revenue   Expenses\n2019   400       320\n2020   450       400\n2021   520       404\n2022   600       510\n```\nWhat is the total profit (revenue − expenses) over the four years, in Rs crore?", [], 336,
     "Profit by year: 80, 50, 116, 90. Sum = 80 + 50 + 116 + 90 = 336."),
    ("h", 2, "s", "A company's revenue and expenses (Rs crore):\n```\nYear   Revenue   Expenses\n2019   400       320\n2020   450       400\n2021   520       404\n2022   600       510\n```\nIn which year was profit the highest as a percentage of revenue?", ["2021", "2019", "2020", "2022"], 0,
     "Profit/revenue: 2019 → 80/400 = 20%; 2020 → 50/450 = 11.1%; 2021 → 116/520 = 22.3%; 2022 → 90/600 = 15%. 2021 is highest."),
    ("m", 1, "n", "Daily maximum temperature (°C):\n```\nDay      Mon  Tue  Wed  Thu  Fri\nCity A   28   30   33   31   29\nCity B   25   29   31   34   30\n```\nOn how many days was City B hotter than City A?", [], 2,
     "Compare day by day: Mon 25 < 28, Tue 29 < 30, Wed 31 < 33, Thu 34 > 31, Fri 30 > 29. City B is hotter on Thursday and Friday: 2 days."),
    ("m", 1, "n", "Daily maximum temperature (°C):\n```\nDay      Mon  Tue  Wed  Thu  Fri\nCity A   28   30   33   31   29\nCity B   25   29   31   34   30\n```\nWhat is the mean temperature of City A over the five days (°C)?", [], 30.2,
     "(28 + 30 + 33 + 31 + 29) / 5 = 151 / 5 = 30.2.", 0.01),
    ("h", 2, "n", "Daily maximum temperature (°C):\n```\nDay      Mon  Tue  Wed  Thu  Fri\nCity A   28   30   33   31   29\nCity B   25   29   31   34   30\n```\nWhat is the largest one-day increase in temperature for City B (°C)?", [], 4,
     "City B day-to-day changes: +4 (Mon→Tue), +2 (Tue→Wed), +3 (Wed→Thu), −4 (Thu→Fri). The largest increase is 4."),
])

C("GA", D, "Pie charts & data sufficiency", [
    ("m", 1, "n", "A family's monthly expenditure of Rs 60000 is split as: Rent 30%, Food 25%, Transport 10%, Education 20%, Savings 15%. How much (in Rs) is spent on education?", [], 12000,
     "20% of 60000 = 12000."),
    ("m", 2, "n", "A family's monthly expenditure of Rs 60000 is split as: Rent 30%, Food 25%, Transport 10%, Education 20%, Savings 15%. If the transport expense rises by 50% while every other amount stays the same, what is the new total (in Rs)?", [], 63000,
     "Transport = 10% of 60000 = 6000. A 50% rise makes it 9000, an extra 3000. New total = 60000 + 3000 = 63000."),
    ("m", 1, "s", "What is the value of x? (I) x² = 9. (II) x > 0.", ["Both statements together are sufficient, but neither alone is", "Statement I alone is sufficient", "Statement II alone is sufficient", "Neither statement is sufficient even together"], 0,
     "I alone gives x = 3 or −3. II alone only says x is positive. Together x² = 9 and x > 0 give x = 3."),
    ("m", 1, "s", "Is the integer n even? (I) n + 1 is odd. (II) n/2 is an integer.", ["Each statement alone is sufficient", "Statement I alone is sufficient, II is not", "Statement II alone is sufficient, I is not", "Both are needed together"], 0,
     "If n + 1 is odd then n is even (I is sufficient). If n/2 is an integer then n is a multiple of 2, i.e. even (II is also sufficient)."),
    ("h", 2, "s", "What is Ravi's age? (I) Ravi is 5 years older than Sita. (II) The sum of their ages is 35.", ["Both statements together are sufficient, but neither alone is", "Statement I alone is sufficient", "Statement II alone is sufficient", "Neither statement is sufficient even together"], 0,
     "I gives only R = S + 5; II gives only R + S = 35. Together 2S + 5 = 35, so S = 15 and R = 20."),
])
