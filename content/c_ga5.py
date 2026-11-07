"""General Aptitude — more data-interpretation sets (each set is a small table with several questions)."""
from content.kit import C

D = "Data Interpretation"
POP = "Population of five towns (in thousands):\n```\nTown   2011   2021\nP      120    150\nQ      200    230\nR      80     120\nS      150    165\nT      90     99\n```\n"
BUD = "A state's budget is divided as: Education 24%, Health 16%, Defence 20%, Agriculture 18%, Others 22%.\n"
WHT = "Wheat production (lakh tonnes):\n```\nYear   2018  2019  2020  2021  2022\nOutput 40    46    44    52    58\n```\n"
STU = "Students in a college:\n```\nStream    Boys   Girls\nScience   120    80\nCommerce  90     110\nArts      60     90\n```\n"

C("GA", D, "Table interpretation", [
    ("m", 1, "s", POP + "Which town had the highest percentage growth between 2011 and 2021?", ["R", "P", "Q", "S"], 0,
     "Percentage growth = (2021 − 2011)/2011: P = 30/120 = 25%, Q = 30/200 = 15%, R = 40/80 = 50%, S = 15/150 = 10%, T = 9/90 = 10%. Town R is highest."),
    ("e", 1, "n", POP + "What was the total population of the five towns in 2021 (in thousands)?", [], 764,
     "150 + 230 + 120 + 165 + 99 = 764."),
    ("h", 2, "n", POP + "By what percent did the total population of the five towns grow from 2011 to 2021? (up to 2 decimals)", [], 19.38,
     "Total 2011 = 120 + 200 + 80 + 150 + 90 = 640; total 2021 = 764. Growth = (764 − 640)/640 × 100 = 124/640 × 100 = 19.375 ≈ 19.38%.", 0.02),
    ("m", 1, "n", STU + "What percentage of all the students are girls? (up to 2 decimals)", [], 50.91,
     "Girls = 80 + 110 + 90 = 280; total students = (120 + 80) + (90 + 110) + (60 + 90) = 550. 280/550 × 100 = 50.909 ≈ 50.91%.", 0.02),
    ("m", 1, "s", STU + "In which stream is the ratio of girls to boys the highest?", ["Arts", "Science", "Commerce", "It is the same in all"], 0,
     "Girls : boys = Science 80/120 = 0.67, Commerce 110/90 = 1.22, Arts 90/60 = 1.5. Arts is highest."),
    ("m", 1, "n", STU + "How many more boys than girls are there in the Science stream?", [], 40,
     "120 − 80 = 40."),
])

C("GA", D, "Pie charts & data sufficiency", [
    ("e", 1, "n", BUD + "If the total budget is Rs 5000 crore, how much (in Rs crore) is allotted to Health and Agriculture together?", [], 1700,
     "Health + Agriculture = 16% + 18% = 34%. 34% of 5000 = 1700."),
    ("m", 1, "n", BUD + "What is the central angle (in degrees) of the Defence sector in a pie chart of this budget?", [], 72,
     "A full circle is 360° for 100%, so 1% = 3.6°. Defence = 20% → 20 × 3.6 = 72°."),
    ("m", 1, "s", BUD + "What is the ratio of the amount spent on Education to the amount spent on Others?", ["12 : 11", "11 : 12", "6 : 5", "5 : 6"], 0,
     "Education : Others = 24 : 22 = 12 : 11."),
])

C("GA", D, "Bar & line graphs (tabulated)", [
    ("m", 1, "s", WHT + "In which year was the percentage increase in production over the previous year the greatest?", ["2021", "2019", "2020", "2022"], 0,
     "Percent change: 2019 = 6/40 = 15%; 2020 = −2/46 = −4.3%; 2021 = 8/44 = 18.2%; 2022 = 6/52 = 11.5%. The greatest is 2021."),
    ("e", 1, "n", WHT + "What is the average annual production over the five years (lakh tonnes)?", [], 48,
     "(40 + 46 + 44 + 52 + 58)/5 = 240/5 = 48."),
    ("m", 1, "n", WHT + "In how many of the five years did production exceed the five-year average?", [], 2,
     "The average is 48. Only 52 (2021) and 58 (2022) exceed it: 2 years."),
])
