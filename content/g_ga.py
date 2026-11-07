"""General Aptitude — numerical, reasoning and data-interpretation generators."""
import datetime
import math
from fractions import Fraction

from content.kit import *

S = "GA"
VB, NU, LR, DI = "Verbal Ability", "Numerical Ability", "Logical & Analytical Reasoning", "Data Interpretation"
F = Fraction


def pc(x):
    return fmt(round(float(x), 2))


# ---------------- numerical ----------------
@gen(S, NU, "Percentages", n=50, diff="easy")
def n_pct(r):
    kind = r.choice(["of", "inc_dec", "succ_disc", "growth", "change", "reverse", "share"])
    p, x = r.choice([5, 10, 12, 15, 20, 25, 30, 35, 40, 45, 60, 75]), r.choice([80, 120, 200, 240, 360, 400, 500, 640, 800, 1200])
    q = r.choice([10, 20, 25, 30, 40, 50])
    if kind == "of": return nat(r, "What is %d%% of %d?" % (p, x), p * x / 100, "p/100 × x.", tol=0.01)
    if kind == "inc_dec":
        net = (1 + p / 100) * (1 - q / 100) - 1
        return mcq(r, "A price is increased by %d%% and then decreased by %d%%. The net change is" % (p, q), "%s%%" % pc(net * 100), ["%s%%" % pc((p - q)), "%s%%" % pc(-net * 100), "%s%%" % pc(p * q / 100), "0%"], "Net factor (1 + %d/100)(1 − %d/100)." % (p, q))
    if kind == "succ_disc":
        v = 100 * (1 - p / 100) * (1 - q / 100)
        return nat(r, "Successive discounts of %d%% and %d%% are equivalent to a single discount of how many percent? (up to 2 decimals)" % (p, q), round(100 - v, 2), "1 − (1−p)(1−q).", tol=0.01)
    if kind == "growth":
        n = r.randint(2, 4)
        return nat(r, "A town's population of %d grows by %d%% every year (compound). Population after %d years, rounded to the nearest integer?" % (x * 10, p, n), round(x * 10 * (1 + p / 100) ** n), "P(1 + r)^n.", tol=1)
    if kind == "change":
        a, b = r.randint(50, 500), r.randint(50, 500)
        return nat(r, "A value rises from %d to %d. Percentage change? (up to 2 decimals; negative if it falls)" % (a, b), round((b - a) / a * 100, 2), "(new − old)/old × 100.", tol=0.01)
    if kind == "reverse":
        return nat(r, "After a %d%% increase a quantity becomes %d. What was the original quantity?" % (p, x * (100 + p) // 100 if (x * (100 + p)) % 100 == 0 else x), x if (x * (100 + p)) % 100 == 0 else x * 100 / (100 + p), "Original = new / (1 + p/100).", tol=0.01)
    return nat(r, "In a class of %d students, %d%% are girls. How many boys are there?" % (x, p), x - x * p / 100, "x − p% of x.", tol=0.01)


@gen(S, NU, "Profit & loss", n=40, diff="medium")
def n_profit(r):
    cp, pr = r.choice([200, 250, 400, 500, 800, 1000, 1500, 2000]), r.choice([10, 12.5, 15, 20, 25, 30, 40])
    disc = r.choice([5, 10, 15, 20, 25])
    kind = r.choice(["sp", "pct", "marked", "cp_from_sp", "two_items", "mp_given"])
    if kind == "sp": return nat(r, "An article bought for %d is sold at %g%% profit. Selling price?" % (cp, pr), cp * (1 + pr / 100), "CP(1 + p/100).", tol=0.01)
    if kind == "pct":
        sp = cp + r.choice([-1, 1]) * r.choice([20, 40, 50, 100])
        return nat(r, "An article bought for %d is sold for %d. Profit percentage (negative for loss)? (up to 2 decimals)" % (cp, sp), round((sp - cp) / cp * 100, 2), "(SP − CP)/CP × 100.", tol=0.01)
    if kind == "marked":
        mp = cp * 1.5
        return nat(r, "A shopkeeper marks an item at %g, gives a %d%% discount. Selling price? (up to 2 decimals)" % (mp, disc), round(mp * (1 - disc / 100), 2), "MP(1 − d).", tol=0.01)
    if kind == "cp_from_sp": return nat(r, "An item is sold for %g, making a %g%% profit. Cost price? (up to 2 decimals)" % (round(cp * (1 + pr / 100), 2), pr), cp, "SP / (1 + p/100).", tol=0.01)
    if kind == "two_items":
        sp, x = r.choice([1000, 1200, 2000, 2400]), r.choice([10, 20, 25])
        loss = (x / 100) ** 2 * 100
        return mcq(r, "Two articles are each sold for %d; one at a %d%% profit and the other at a %d%% loss. The overall result is" % (sp, x, x), "a loss of %s%%" % pc(x * x / 100), ["a profit of %s%%" % pc(x * x / 100), "no profit no loss", "a loss of %d%%" % x], "Equal-percentage profit and loss on equal selling prices always gives a loss of x²/100 %%.")
    mp_prof = r.choice([(20, 10, 10), (25, 20, 0), (50, 20, 20), (40, 25, 5)])
    return nat(r, "A trader marks goods %d%% above cost and allows a %d%% discount. His profit percentage is (up to 2 decimals; negative for loss)" % mp_prof[:2], round(((1 + mp_prof[0] / 100) * (1 - mp_prof[1] / 100) - 1) * 100, 2), "Net factor (1 + m)(1 − d) − 1.", tol=0.01)


@gen(S, NU, "Ratio & mixtures", n=40, diff="medium")
def n_ratio(r):
    kind = r.choice(["divide", "alligation", "age", "ratio_change", "mix_concentration", "ratio_total"])
    a, b, c = r.randint(1, 7), r.randint(2, 9), r.randint(1, 5)
    tot = (a + b) * r.choice([6, 8, 10, 12, 15])
    if kind == "divide": return nat(r, "Rs. %d is divided between two people in the ratio %d : %d. The smaller share is" % (tot, a, b), tot * min(a, b) // (a + b), "Share = total × part/(sum of parts).")
    if kind == "alligation":
        p1, p2, mean = r.choice([(20, 30, 24), (40, 60, 52), (10, 25, 16), (50, 80, 62)])
        return mcq(r, "Two varieties of rice costing Rs. %d and Rs. %d per kg are mixed to produce a blend worth Rs. %d per kg. In what ratio (cheaper : dearer) are they mixed?" % (p1, p2, mean), "%d : %d" % tuple((lambda g: ((p2 - mean) // g, (mean - p1) // g))(math.gcd(p2 - mean, mean - p1))),
                   ["%d : %d" % tuple((lambda g: ((mean - p1) // g, (p2 - mean) // g))(math.gcd(p2 - mean, mean - p1))), "1 : 1", "%d : %d" % (p1, p2), "%d : %d" % (mean, p2)], "Alligation: (dearer − mean) : (mean − cheaper).")
    if kind == "age":
        x, y = r.randint(2, 6), r.randint(2, 6)
        return nat(r, "The ages of A and B are in the ratio %d : %d. Their total age is %d years. What is A's age?" % (x, y, (x + y) * r.randint(4, 9)), 0, "") if False else \
            (lambda k: nat(r, "The ages of A and B are in the ratio %d : %d and the sum of their ages is %d years. What is A's age?" % (x, y, (x + y) * k), x * k, "Age = ratio × (sum / (x + y))."))(r.randint(4, 9))
    if kind == "ratio_change":
        x, y = r.randint(2, 5), r.randint(3, 8)
        k = r.randint(2, 6)
        return nat(r, "Two numbers are in the ratio %d : %d. When %d is added to each, the ratio becomes %d : %d. What is the smaller number?" % (x, y, 10 * k, x + k, y + k) if False else
                   "Two numbers are in the ratio %d : %d and their difference is %d. Find the larger number." % (x, y, abs(y - x) * k * 2), max(x, y) * k * 2, "Difference corresponds to |y − x| parts.")
    if kind == "mix_concentration":
        v1, c1, v2, c2 = r.choice([(10, 20, 20, 50), (30, 10, 20, 40), (40, 25, 10, 75)])
        return nat(r, "%d litres of %d%% acid solution is mixed with %d litres of %d%% acid solution. The concentration (in %%) of the mixture is (up to 2 decimals)" % (v1, c1, v2, c2), round((v1 * c1 + v2 * c2) / (v1 + v2), 2), "Weighted average.", tol=0.01)
    x, y, z = r.randint(1, 5), r.randint(2, 6), r.randint(3, 8)
    return nat(r, "A : B = %d : %d and B : C = %d : %d. If A = %d, what is C? (give exact value, up to 2 decimals)" % (x, y, y, z, x * 6), round(6 * z, 2), "Chain the ratios: A : B : C = %d : %d : %d." % (x, y, z), tol=0.01)


@gen(S, NU, "Time, speed, distance", n=50, diff="medium")
def n_tsd(r):
    kind = r.choice(["avg", "train_pole", "train_train", "boat", "meet", "relative", "catch"])
    v1, v2 = r.choice([20, 30, 40, 60, 24, 36]), r.choice([30, 40, 60, 80, 45, 90])
    if kind == "avg": return nat(r, "A car covers a distance at %d km/h and returns the same distance at %d km/h. Average speed for the whole trip (km/h, up to 2 decimals)?" % (v1, v2), round(2 * v1 * v2 / (v1 + v2), 2), "Harmonic mean 2ab/(a+b).", tol=0.01)
    if kind == "train_pole":
        L, v = r.choice([150, 200, 300, 400]), r.choice([36, 54, 72, 90, 108])
        return nat(r, "A train %d m long passes a pole in %s seconds. What is its speed in km/h?" % (L, pc(L / (v / 3.6))), v, "v = L/t converted to km/h.", tol=0.01)
    if kind == "train_train":
        L1, L2, va, vb = r.choice([100, 150, 200]), r.choice([100, 150, 250]), r.choice([36, 54, 72]), r.choice([18, 27, 36])
        return nat(r, "Two trains of lengths %d m and %d m run in opposite directions at %d km/h and %d km/h. Time (seconds, up to 2 decimals) taken to cross each other completely?" % (L1, L2, va, vb), round((L1 + L2) / ((va + vb) / 3.6), 2), "Relative speed (sum) and combined length.", tol=0.01)
    if kind == "boat":
        b, s = r.choice([(12, 3), (15, 5), (20, 4), (10, 2)])
        d = r.choice([24, 30, 40, 60])
        return nat(r, "A boat's speed in still water is %d km/h and the stream flows at %d km/h. Time taken (hours, up to 2 decimals) to go %d km downstream and come back?" % (b, s, d), round(d / (b + s) + d / (b - s), 2), "d/(b+s) + d/(b−s).", tol=0.01)
    if kind == "meet":
        d = r.choice([180, 240, 300, 420])
        return nat(r, "Two towns are %d km apart. Two cars start towards each other at %d km/h and %d km/h at the same time. After how many hours (up to 2 decimals) do they meet?" % (d, v1, v2), round(d / (v1 + v2), 2), "Distance / sum of speeds.", tol=0.01)
    if kind == "relative":
        return nat(r, "A person walks at %d km/h. At what speed (km/h) must a cyclist travel to cover the same distance in 1/%d of the time?" % (v1, 3), v1 * 3, "Speed is inversely proportional to time.")
    h = r.choice([2, 3, 4])
    return nat(r, "A thief runs at %d km/h and a policeman who starts %d hours later chases at %d km/h (same direction). After how many hours (from the policeman's start, up to 2 decimals) does the policeman catch the thief? (use %d and %d km/h; policeman must be faster)" % (v1, h, v1 + 20, v1, v1 + 20) if False else
               "A thief escapes at %d km/h. The police start chasing %d hour(s) later at %d km/h. After how many hours from the police start (up to 2 decimals) do they catch him?" % (v1, h, v1 + 20), round(h * v1 / 20, 2), "Head start distance / relative speed.", tol=0.01)


@gen(S, NU, "Time & work", n=40, diff="medium")
def n_work(r):
    a, b = r.choice([(10, 15), (12, 24), (6, 12), (20, 30), (8, 24), (15, 30), (9, 18)])
    kind = r.choice(["together", "leave", "pipe", "leak", "men_days", "efficiency"])
    if kind == "together": return nat(r, "A can do a job in %d days and B in %d days. Working together, how many days (up to 2 decimals) do they take?" % (a, b), round(a * b / (a + b), 2), "1/(1/a + 1/b).", tol=0.01)
    if kind == "leave":
        x = r.randint(1, 3)
        return nat(r, "A and B can complete a job in %d and %d days respectively. They start together but A leaves %d days before the job is finished. In how many days (up to 2 decimals) is the job completed?" % (a, b, x), round((1 + x / a) / (1 / a + 1 / b), 2), "B works all days, A works (T − x) days: (T − x)/a + T/b = 1.", tol=0.01)
    if kind == "pipe": return nat(r, "Pipe A fills a tank in %d hours and pipe B fills it in %d hours. Both are opened together. Time (hours, up to 2 decimals) to fill the tank?" % (a, b), round(a * b / (a + b), 2), "Combined rate.", tol=0.01)
    if kind == "leak":
        L = a * 3
        return nat(r, "A pipe fills a tank in %d hours. A leak empties the full tank in %d hours. With both active, time (hours, up to 2 decimals) to fill the empty tank?" % (a, L), round(a * L / (L - a), 2), "1/(1/a − 1/L).", tol=0.01)
    if kind == "men_days":
        m, d, m2 = r.choice([(10, 12, 15), (8, 15, 12), (6, 20, 10), (12, 10, 20)])
        return nat(r, "%d men can finish a job in %d days. How many days will %d men take (same efficiency)?" % (m, d, m2), round(m * d / m2, 2), "Man-days are constant.", tol=0.01)
    return nat(r, "A is twice as efficient as B. Together they finish a job in %d days. How many days would A alone take?" % r.choice([6, 8, 10, 12]) if False else
               "A is twice as efficient as B and together they finish a job in 12 days. How many days would A alone take?", 18, "Rates 2x and x: 3x·12 = 1 ⇒ A alone: 12·3/2 = 18.")


@gen(S, NU, "Interest", n=35, diff="medium")
def n_interest(r):
    P, rate, t = r.choice([1000, 2000, 5000, 8000, 10000]), r.choice([5, 8, 10, 12, 15]), r.randint(2, 4)
    kind = r.choice(["si", "ci", "diff", "rate", "double"])
    if kind == "si": return nat(r, "Simple interest on Rs. %d at %d%% per annum for %d years?" % (P, rate, t), P * rate * t / 100, "PRT/100.", tol=0.01)
    if kind == "ci": return nat(r, "Compound interest (compounded annually) on Rs. %d at %d%% p.a. for %d years, rounded to 2 decimals?" % (P, rate, t), round(P * ((1 + rate / 100) ** t - 1), 2), "P[(1+r)^n − 1].", tol=0.01)
    if kind == "diff": return nat(r, "Difference between the compound and simple interest on Rs. %d at %d%% p.a. for 2 years? (up to 2 decimals)" % (P, rate), round(P * (rate / 100) ** 2, 2), "P(r/100)².", tol=0.01)
    if kind == "rate": return nat(r, "Rs. %d becomes Rs. %d in %d years at simple interest. Rate per annum (%%)?" % (P, P + P * rate * t // 100, t), rate, "R = SI·100/(P·T).")
    return nat(r, "At what simple interest rate (%% per annum) will a sum double itself in %d years?" % (r.choice([4, 5, 8, 10, 20])), 100 / r.choice([4]) if False else 25, "") if False else \
        (lambda yrs: nat(r, "At what simple interest rate (%% per annum) will a sum double itself in %d years? (up to 2 decimals)" % yrs, round(100 / yrs, 2), "Interest = principal ⇒ R = 100/T.", tol=0.01))(r.choice([4, 5, 8, 10, 20]))


@gen(S, NU, "Averages & ages", n=40, diff="easy")
def n_avg(r):
    kind = r.choice(["new_avg", "missing", "weighted", "age_after", "consec", "age_sum"])
    n, a = r.randint(4, 12), r.randint(20, 60)
    if kind == "new_avg":
        x = r.randint(60, 120)
        return nat(r, "The average of %d numbers is %d. A new number %d is added. The new average (up to 2 decimals) is" % (n, a, x), round((n * a + x) / (n + 1), 2), "(sum + x)/(n + 1).", tol=0.01)
    if kind == "missing":
        vals = [r.randint(10, 60) for _ in range(n - 1)]
        return nat(r, "The average of %d numbers is %d. Of them, %d are %s. Find the remaining number." % (n, a, n - 1, vals), n * a - sum(vals), "n·avg − sum of the others.")
    if kind == "weighted":
        n2, a2 = r.randint(4, 12), r.randint(20, 60)
        return nat(r, "A class of %d students has average marks %d and another class of %d students has average %d. Combined average (up to 2 decimals)?" % (n, a, n2, a2), round((n * a + n2 * a2) / (n + n2), 2), "Weighted mean.", tol=0.01)
    if kind == "age_after":
        y, k = r.randint(20, 40), r.randint(3, 10)
        return nat(r, "A father is %d years older than his son; the father's age is currently %d. In how many years will the father be exactly twice the son's age? (son's age = %d)" % (y, y + 20, 20) if False else
                   "The present age of a father is 3 times that of his son. After %d years the father will be twice as old as the son. Find the son's present age." % k, k, "3x + k = 2(x + k) ⇒ x = k.")
    if kind == "consec":
        m = r.randint(3, 9)
        s = r.randint(3, 20)
        return nat(r, "The average of %d consecutive integers is %d. What is the largest of them?" % (2 * m + 1, s + m), s + 2 * m, "Average is the middle term; largest = middle + m.")
    x = r.randint(10, 30)
    return nat(r, "The sum of the ages of 5 children born at intervals of %d years each is %d years. What is the age of the youngest?" % (3, 50 + 15 * 3 - 15 * 0) if False else
               "The sum of the ages of 5 children born at 3-year intervals is 50 years. Find the age of the youngest child.", 4, "x + (x+3) + … + (x+12) = 5x + 30 = 50 ⇒ x = 4.")


@gen(S, NU, "Number properties", n=50, diff="medium")
def n_number(r):
    kind = r.choice(["lcm", "hcf", "unit", "fact", "trail", "rem", "div", "sumdigits", "primes"])
    a, b = r.randint(12, 90), r.randint(12, 90)
    if kind == "lcm": return nat(r, "LCM of %d and %d?" % (a, b), a * b // math.gcd(a, b), "ab/gcd.")
    if kind == "hcf": return nat(r, "HCF of %d and %d?" % (a * 3, b * 3), math.gcd(a, b) * 3, "Euclid's algorithm.")
    if kind == "unit":
        base, e = r.randint(2, 9), r.randint(10, 99)
        return nat(r, "Units digit of %d^%d?" % (base, e), pow(base, e, 10), "Cycle of units digits.")
    if kind == "fact":
        n = r.randint(12, 360)
        return nat(r, "Number of positive divisors of %d?" % n, sum(1 for d in range(1, n + 1) if n % d == 0), "Count the divisors.")
    if kind == "trail":
        n = r.randint(20, 200)
        z, d = 0, 5
        while n // d: z += n // d; d *= 5
        return nat(r, "Number of trailing zeros in %d! ?" % n, z, "Σ ⌊n/5^k⌋.")
    if kind == "rem":
        m, e, d = r.randint(2, 9), r.randint(20, 100), r.choice([5, 7, 9, 11, 13])
        return nat(r, "Remainder when %d^%d is divided by %d?" % (m, e, d), pow(m, e, d), "Modular exponentiation.")
    if kind == "div":
        lo, hi, k = r.randint(10, 100), r.randint(200, 800), r.choice([3, 4, 6, 7, 9, 11])
        return nat(r, "How many integers between %d and %d (inclusive) are divisible by %d?" % (lo, hi, k), hi // k - (lo - 1) // k, "⌊hi/k⌋ − ⌊(lo−1)/k⌋.")
    if kind == "sumdigits":
        n = r.randint(2, 6)
        return nat(r, "Sum of the first %d odd positive integers?" % (n * 5), (n * 5) ** 2, "n².")
    lo = r.randint(2, 60)
    hi = lo + r.randint(20, 40)
    return nat(r, "How many prime numbers lie between %d and %d (inclusive)?" % (lo, hi), sum(1 for x in range(lo, hi + 1) if x > 1 and all(x % d for d in range(2, int(x ** 0.5) + 1))), "Test each number.")


@gen(S, NU, "Algebra", n=40, diff="medium")
def n_alg(r):
    kind = r.choice(["linear", "quad_sum", "quad_prod", "ap_term", "ap_sum", "gp", "inequality", "pair"])
    a, b, c = r.randint(2, 9), r.randint(1, 20), r.randint(1, 9)
    if kind == "linear":
        x = r.randint(2, 12)
        return nat(r, "Solve for x:  %dx + %d = %d" % (a, b, a * x + b), x, "x = (rhs − b)/a.")
    p, q = r.randint(-6, 8), r.randint(-6, 8)
    if kind == "quad_sum": return nat(r, "The roots of x² %+dx %+d = 0 are %d and %d. What is the sum of the roots?" % (-(p + q), p * q, p, q), p + q, "−b/a.")
    if kind == "quad_prod": return nat(r, "For x² %+dx %+d = 0, find the product of the roots." % (-(p + q), p * q), p * q, "c/a.")
    n = r.randint(5, 25)
    if kind == "ap_term": return nat(r, "The first term of an arithmetic progression is %d and the common difference is %d. Find the %d-th term." % (a, c, n), a + (n - 1) * c, "a + (n−1)d.")
    if kind == "ap_sum": return nat(r, "Sum of the first %d terms of the AP with first term %d and common difference %d?" % (n, a, c), n * (2 * a + (n - 1) * c) // 2, "n/2 (2a + (n−1)d).")
    if kind == "gp":
        t = r.randint(3, 7)
        return nat(r, "Sum of the first %d terms of the geometric progression 2, 6, 18, …?" % t, (3 ** t - 1), "a(r^n − 1)/(r − 1) = 3^n − 1.")
    if kind == "inequality":
        return nat(r, "How many positive integers x satisfy %dx + %d < %d?" % (a, b, a * 10 + b), 9, "x < 10 ⇒ 1..9.")
    return nat(r, "If x + y = %d and xy = %d, find x² + y²." % (a + c, a * c), (a + c) ** 2 - 2 * a * c, "(x + y)² − 2xy.")


@gen(S, NU, "Geometry & mensuration", n=45, diff="easy")
def n_geo(r):
    kind = r.choice(["circle", "cyl", "tri", "poly_angle", "pyth", "cube", "sector", "diag"])
    a, b = r.randint(3, 15), r.randint(4, 20)
    if kind == "circle": return nat(r, "Area of a circle of radius %d (use π = 3.14159; answer to 2 decimals)?" % a, round(math.pi * a * a, 2), "πr².", tol=0.05)
    if kind == "cyl": return nat(r, "Volume of a cylinder with radius %d and height %d (π = 3.14159; to the nearest integer)?" % (a, b), round(math.pi * a * a * b), "πr²h.", tol=1)
    if kind == "tri":
        s1, s2, s3 = r.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15), (8, 15, 17)])
        return nat(r, "Area of a triangle with sides %d, %d, %d?" % (s1, s2, s3), s1 * s2 / 2, "Right triangle: ½ × legs.")
    if kind == "poly_angle":
        n = r.randint(5, 12)
        return nat(r, "Sum of interior angles (degrees) of a convex polygon with %d sides?" % n, (n - 2) * 180, "(n − 2)·180.")
    if kind == "pyth":
        s1, s2, s3 = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)])
        return nat(r, "A ladder of length %d m leans against a wall with its foot %d m from the wall. How high up the wall (m) does it reach?" % (s3, s1), s2, "Pythagoras.")
    if kind == "cube": return nat(r, "A cube has a surface area of %d square units. Find its volume." % (6 * a * a), a ** 3, "Side = √(SA/6).")
    if kind == "sector":
        d = r.choice([30, 45, 60, 90, 120, 180])
        return nat(r, "Area of a sector of angle %d° in a circle of radius %d (π = 3.14159; to 2 decimals)?" % (d, a), round(math.pi * a * a * d / 360, 2), "(θ/360)·πr².", tol=0.05)
    return nat(r, "The diagonal of a rectangle with sides %d and %d is √k. Find k." % (a, b), a * a + b * b, "Pythagoras.")


@gen(S, NU, "Clocks & calendars", n=30, diff="medium")
def n_clock(r):
    kind = r.choice(["angle", "day", "leap", "gain", "overlap"])
    if kind == "angle":
        h, m = r.randint(1, 12), r.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        ang = abs(30 * (h % 12) + 0.5 * m - 6 * m)
        ang = min(ang, 360 - ang)
        return nat(r, "What is the smaller angle (in degrees) between the hands of a clock at %d:%02d?" % (h, m), ang, "|30H − 5.5M|, taking the smaller angle.", tol=0.01)
    if kind == "day":
        d = datetime.date(r.randint(1990, 2030), r.randint(1, 12), r.randint(1, 28))
        return mcq(r, "On which day of the week did/will %s fall?" % d.strftime("%d %B %Y"), d.strftime("%A"), [x for x in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] if x != d.strftime("%A")], "Count odd days from a known reference date.")
    if kind == "leap":
        y1 = r.randint(1900, 2000)
        y2 = y1 + r.randint(20, 150)
        c = sum(1 for y in range(y1, y2 + 1) if (y % 4 == 0 and y % 100 != 0) or y % 400 == 0)
        return nat(r, "How many leap years are there from %d to %d (both inclusive)?" % (y1, y2), c, "Divisible by 4, except centuries not divisible by 400.")
    if kind == "gain":
        g = r.choice([2, 3, 5, 6])
        return nat(r, "A clock gains %d minutes every hour. How many minutes does it gain in one day (24 h)?" % g, g * 24, "Rate × time.")
    return nat(r, "How many times do the hour and minute hands of a clock overlap in a 12-hour period?", 11, "They overlap 11 times in 12 hours.")


@gen(S, NU, "Counting & probability (GA)", n=35, diff="medium")
def n_prob(r):
    kind = r.choice(["arr", "sel", "coin", "dice", "handshake", "diag"])
    n, k = r.randint(5, 10), r.randint(2, 4)
    if kind == "arr": return nat(r, "In how many ways can %d different books be arranged in a row?" % n, math.factorial(n), "n!.")
    if kind == "sel": return nat(r, "A committee of %d is to be chosen from %d people. In how many ways?" % (k, n), math.comb(n, k), "C(n,k).")
    if kind == "coin": return nat(r, "A fair coin is tossed %d times. Probability (as a decimal, up to 4 decimals) of getting exactly %d heads?" % (n, k), round(math.comb(n, k) / 2 ** n, 4), "C(n,k)/2^n.", tol=0.0006)
    if kind == "dice":
        s = r.randint(5, 9)
        return nat(r, "Two fair dice are rolled. Probability (up to 4 decimals) that the sum is %d?" % s, round(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s) / 36, 4), "Favourable/36.", tol=0.0006)
    if kind == "handshake": return nat(r, "%d people each shake hands once with every other person. Total handshakes?" % (n + 3), math.comb(n + 3, 2), "C(n,2).")
    return nat(r, "Number of diagonals of a convex polygon with %d sides?" % (n + 3), (n + 3) * n // 2, "n(n−3)/2.")


# ---------------- logical & analytical ----------------
def seq_gen(r):
    kind = r.choice(["ap", "gp", "sq", "cube", "fib", "alt", "diff2", "prime", "tri"])
    a, d = r.randint(1, 9), r.randint(2, 8)
    n = 6
    if kind == "ap": s = [a + i * d for i in range(n + 1)]
    elif kind == "gp": s = [a * (d % 3 + 2) ** i for i in range(n + 1)]
    elif kind == "sq": s = [(i + a) ** 2 for i in range(n + 1)]
    elif kind == "cube": s = [(i + 1) ** 3 + a for i in range(n + 1)]
    elif kind == "fib":
        s = [a, d]
        for _ in range(n - 1): s.append(s[-1] + s[-2])
    elif kind == "alt": s = [(a + i * d) if i % 2 == 0 else (a * 2 + i * 3) for i in range(n + 1)]
    elif kind == "diff2": s = [a + i * d + i * (i - 1) // 2 * 3 for i in range(n + 1)]
    elif kind == "prime":
        pr = [x for x in range(2, 60) if all(x % q for q in range(2, int(x ** 0.5) + 1))]
        s = pr[a % 5:a % 5 + n + 1]
    else: s = [i * (i + 1) // 2 + a for i in range(1, n + 2)]
    return kind, s


@gen(S, LR, "Number series", n=50, diff="easy")
def l_series(r):
    kind, s = seq_gen(r)
    shown, ans = s[:-1], s[-1]
    if r.random() < 0.4 and kind not in ("alt",):
        i = r.randint(1, len(s) - 2)
        ans = s[i]
        shown = [x if j != i else "?" for j, x in enumerate(s[:-1])]
        return nat(r, "Find the missing term in the series:  %s" % ", ".join(map(str, shown)), ans, "Identify the rule (%s)." % kind)
    return nat(r, "What comes next in the series:  %s, ?" % ", ".join(map(str, shown)), ans, "Identify the rule (%s)." % kind)


@gen(S, LR, "Coding & ordering", n=45, diff="easy")
def l_coding(r):
    kind = r.choice(["shift", "pos", "rank", "between", "alpha_pos", "mirror"])
    if kind == "shift":
        k, w = r.randint(1, 5), r.choice(["GATE", "CODE", "BYTE", "LOGIC", "STACK", "QUEUE", "GRAPH"])
        c = "".join(chr((ord(x) - 65 + k) % 26 + 65) for x in w)
        q = r.choice([w, c])
        if q == w:
            return mcq(r, "In a certain code each letter is replaced by the letter %d places ahead in the alphabet. How is %s written?" % (k, w), c, ["".join(chr((ord(x) - 65 - k) % 26 + 65) for x in w), "".join(chr((ord(x) - 65 + k + 1) % 26 + 65) for x in w), w[::-1], "".join(chr((ord(x) - 65 + 2 * k) % 26 + 65) for x in w)], "Shift each letter by %d." % k)
        return mcq(r, "In a certain code each letter is replaced by the letter %d places ahead in the alphabet. What is the original word for the code %s?" % (k, c), w, ["".join(chr((ord(x) - 65 + k) % 26 + 65) for x in c), c[::-1], "".join(chr((ord(x) - 65 - k - 1) % 26 + 65) for x in c), "".join(chr((ord(x) - 65 - 2 * k) % 26 + 65) for x in c)], "Shift back by %d." % k)
    n, p = r.randint(20, 60), r.randint(3, 17)
    if kind == "pos": return nat(r, "In a row of %d students, Ravi is %d-th from the left. What is his position from the right?" % (n, p), n - p + 1, "n − p + 1.")
    if kind == "rank": return nat(r, "Arun ranks %d-th from the top and %d-th from the bottom in a class. How many students are in the class?" % (p, p + 7), p + (p + 7) - 1, "top + bottom − 1.")
    if kind == "between": return nat(r, "In a row of %d people, A is %d-th from the left and B is %d-th from the right. How many people are between them (A is to the left of B)?" % (n, p, p + 4), n - p - (p + 4), "n − pos_left − pos_right.")
    if kind == "alpha_pos":
        k = r.randint(2, 6)
        return nat(r, "If A = 1, B = 2, … Z = 26, what is the sum of the values of the letters in the word %s?" % r.choice(["GATE", "CODE", "BYTE", "STACK"]), 0, "") if False else \
            (lambda w: nat(r, "If A = 1, B = 2, …, Z = 26, what is the sum of the letter values of the word %s?" % w, sum(ord(c) - 64 for c in w), "Add the positions."))(r.choice(["GATE", "CODE", "BYTE", "STACK", "QUEUE", "GRAPH"]))
    w = r.choice(["CAT", "DOG", "BAT", "LOGIC", "GATE"])
    return mcq(r, "What is the mirror-image alphabet code of %s, where A↔Z, B↔Y, C↔X, …?" % w, "".join(chr(155 - ord(c)) for c in w), [w[::-1], "".join(chr(154 - ord(c)) for c in w), "".join(chr((ord(c) - 64) % 26 + 65) for c in w), w], "Letter x maps to 27 − x.")


@gen(S, LR, "Directions & distances", n=35, diff="medium")
def l_dir(r):
    moves = []
    x = y = 0
    dirs = {"north": (0, 1), "south": (0, -1), "east": (1, 0), "west": (-1, 0)}
    for _ in range(r.randint(3, 5)):
        d = r.choice(list(dirs))
        k = r.randint(1, 9)
        moves.append((d, k)); x += dirs[d][0] * k; y += dirs[d][1] * k
    dist2 = x * x + y * y
    s = ", then ".join("%d km %s" % (k, d) for d, k in moves)
    if r.random() < 0.5:
        return nat(r, "A man starts walking: %s. How far (in km, up to 2 decimals) is he from the starting point?" % s, round(math.sqrt(dist2), 2), "Net displacement (%d, %d) ⇒ √(x² + y²)." % (x, y), tol=0.01)
    return nat(r, "A man starts walking: %s. Total distance walked (km)?" % s, sum(k for _, k in moves), "Add the legs.")


@gen(S, LR, "Venn & sets", n=40, diff="medium")
def l_venn(r):
    n = r.choice([100, 120, 150, 200])
    a, b = r.randint(30, 80), r.randint(30, 80)
    both = r.randint(5, min(a, b) - 5)
    kind = r.choice(["either", "neither", "only_a", "total_from_both"])
    if kind == "either": return nat(r, "In a group, %d like tea, %d like coffee and %d like both. How many like at least one of the two?" % (a, b, both), a + b - both, "|A| + |B| − |A∩B|.")
    if kind == "neither": return nat(r, "Of %d people, %d like tea, %d like coffee and %d like both. How many like neither?" % (n, a, b, both), n - (a + b - both), "Total − union.") if n >= a + b - both else (_ for _ in ()).throw(Skip())
    if kind == "only_a": return nat(r, "%d people like tea, %d like coffee, %d like both. How many like ONLY tea?" % (a, b, both), a - both, "|A| − |A∩B|.")
    return nat(r, "In a survey, %d people like only tea, %d like only coffee and %d like both. How many were surveyed (everyone likes at least one)?" % (a - both, b - both, both), a + b - both, "Sum of the three disjoint regions.")


@gen(S, LR, "Cubes & counting figures", n=20, diff="easy")
def l_cube(r):
    n = r.randint(3, 8)
    kind = r.choice(["three", "two", "one", "zero", "total", "squares", "tri"])
    if kind == "three": return nat(r, "A cube of side %d is painted on all faces and cut into unit cubes. How many unit cubes have exactly three faces painted?" % n, 8, "The 8 corner cubes.")
    if kind == "two": return nat(r, "A cube of side %d is painted on all faces and cut into unit cubes. How many unit cubes have exactly two faces painted?" % n, 12 * (n - 2), "12(n − 2).")
    if kind == "one": return nat(r, "A cube of side %d is painted on all faces and cut into unit cubes. How many unit cubes have exactly one face painted?" % n, 6 * (n - 2) ** 2, "6(n − 2)².")
    if kind == "zero": return nat(r, "A cube of side %d is painted on all faces and cut into unit cubes. How many unit cubes have no face painted?" % n, (n - 2) ** 3, "(n − 2)³.")
    if kind == "total": return nat(r, "How many unit cubes are obtained by cutting a cube of side %d into unit cubes?" % n, n ** 3, "n³.")
    if kind == "squares": return nat(r, "How many squares of all sizes are there on a %d × %d chessboard?" % (n, n), sum(i * i for i in range(1, n + 1)), "Σk².")
    return nat(r, "How many rectangles of all sizes are there on a %d × %d grid of squares?" % (n, n), (n * (n + 1) // 2) ** 2, "(n(n+1)/2)².")


# ---------------- data interpretation ----------------
@gen(S, DI, "Tables", n=40, diff="hard", marks=2)
def di_table(r):
    years = list(range(2018, 2018 + r.randint(4, 6)))
    items = r.sample(["Product A", "Product B", "Product C", "Product D"], 3)
    data = {it: [r.randint(20, 150) * 10 for _ in years] for it in items}
    head = "Sales (in units):\n```\nYear   " + "  ".join("%-9s" % it for it in items) + "\n" + "\n".join("%d   " % y + "  ".join("%-9d" % data[it][i] for it in items) for i, y in enumerate(years)) + "\n```\n"
    kind = r.choice(["total", "pct_change", "avg", "max_year", "ratio", "share", "cagr_like", "diff"])
    it = r.choice(items)
    i = r.randint(1, len(years) - 1)
    if kind == "total": return nat(r, head + "Total sales of %s over all years?" % it, sum(data[it]), "Add the column.")
    if kind == "pct_change":
        a, b = data[it][i - 1], data[it][i]
        return nat(r, head + "Percentage change in sales of %s from %d to %d? (up to 2 decimals, negative for decrease)" % (it, years[i - 1], years[i]), round((b - a) / a * 100, 2), "(new − old)/old × 100.", tol=0.01)
    if kind == "avg": return nat(r, head + "Average yearly sales of %s? (up to 2 decimals)" % it, round(sum(data[it]) / len(years), 2), "Mean of the column.", tol=0.01)
    if kind == "max_year":
        tot = [sum(data[x][j] for x in items) for j in range(len(years))]
        if tot.count(max(tot)) > 1: raise Skip()
        return mcq(r, head + "In which year were the combined sales of all three products highest?", years[tot.index(max(tot))], [y for y in years if y != years[tot.index(max(tot))]], "Row totals: %s." % tot)
    if kind == "ratio":
        a, b = r.sample(items, 2)
        j = r.randrange(len(years))
        g = math.gcd(data[a][j], data[b][j])
        return mcq(r, head + "In %d, the ratio of sales of %s to %s is" % (years[j], a, b), "%d : %d" % (data[a][j] // g, data[b][j] // g), ["%d : %d" % (data[b][j] // g, data[a][j] // g), "%d : %d" % (data[a][j] // g + 1, data[b][j] // g), "%d : %d" % (data[a][j] // g, data[b][j] // g + 1), "1 : 1"], "Divide by the gcd.")
    if kind == "share":
        j = r.randrange(len(years))
        tot = sum(data[x][j] for x in items)
        return nat(r, head + "In %d, what percentage of the combined sales is contributed by %s? (up to 2 decimals)" % (years[j], it), round(data[it][j] / tot * 100, 2), "part/total × 100.", tol=0.01)
    if kind == "cagr_like":
        a, b = data[it][0], data[it][-1]
        return nat(r, head + "By what percentage did the sales of %s change between %d and %d (first to last year)? (up to 2 decimals)" % (it, years[0], years[-1]), round((b - a) / a * 100, 2), "(last − first)/first × 100.", tol=0.01)
    a, b = r.sample(items, 2)
    return nat(r, head + "By how many units did the total sales of %s exceed (or fall short of, if negative) those of %s over all years?" % (a, b), sum(data[a]) - sum(data[b]), "Difference of column totals.")


@gen(S, DI, "Percent-split charts", n=20, diff="medium")
def di_pie(r):
    cats = ["Salary", "Rent", "Food", "Travel", "Savings"]
    parts = [r.choice([10, 15, 20, 25, 30]) for _ in range(4)]
    if sum(parts) >= 100: raise Skip()
    parts.append(100 - sum(parts))
    tot = r.choice([20000, 30000, 40000, 50000, 60000])
    cat = r.randrange(5)
    desc = "A family's monthly expenditure of Rs. %d is distributed as: %s." % (tot, ", ".join("%s %d%%" % (c, p) for c, p in zip(cats, parts)))
    kind = r.choice(["amount", "angle", "diff", "ratio"])
    if kind == "amount": return nat(r, desc + " How much (Rs.) is spent on %s?" % cats[cat], tot * parts[cat] / 100, "Percent × total.", tol=0.01)
    if kind == "angle": return nat(r, desc + " In a pie chart of this data, what is the central angle (degrees) for %s?" % cats[cat], parts[cat] * 3.6, "% × 3.6.", tol=0.01)
    a, b = r.sample(range(5), 2)
    if kind == "diff": return nat(r, desc + " By how much (Rs.) does the spending on %s exceed that on %s? (negative if less)" % (cats[a], cats[b]), tot * (parts[a] - parts[b]) / 100, "Difference of percentages × total.", tol=0.01)
    return nat(r, desc + " The expenditure on %s is how many times that on %s? (up to 2 decimals)" % (cats[a], cats[b]), round(parts[a] / parts[b], 2), "Ratio of percentages.", tol=0.01)
