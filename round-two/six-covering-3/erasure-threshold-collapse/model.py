"""Exact finite collapse of the credited9241 common-q free12/12 hierarchy.

Distinct labels in an erasure witness are ability tests, not allocations.
Ordinary proofs of normalization and completeness are in proof.md.
"""
from itertools import combinations, product
from math import comb

D = (1, 3, 5, 7, 9, 15, 21, 35, 45, 63, 105, 315)
PREFIX = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 10))
BASE = tuple(n for n in range(8, 2521) if 2520 % n == 0 and
             n not in {n for n, a in PREFIX})
# (threshold q, forbidden-label cardinality, required qualified parents).
ROWS = ((2, 1, 3), (2, 3, 2), (2, 6, 1),
        (3, 2, 3), (3, 4, 2), (3, 7, 1),
        (4, 5, 2), (5, 3, 3), (6, 1, 4))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def threshold(q, b):
    need(type(q) is int and q >= 2 and type(b) is int and 0 <= b <= 12,
         "invalid scalar threshold domain")
    numerator = (16 - 2*b)*q + b - 12
    return max(0, -((-numerator)//(4*q)))


def collapse():
    table = [[b] + [threshold(q, b) for q in range(2, 7)] for b in range(13)]
    rays = []
    for b in range(13):
        k = threshold(6, b)
        upper_slope = 4*k - (16 - 2*b)
        upper_at6 = 6*upper_slope + 12 - b
        need(upper_slope >= 0 and upper_at6 >= 0, "upper infinite ray failed")
        if k:
            lower_slope = (16 - 2*b) - 4*(k - 1)
            lower_at6 = 6*lower_slope + b - 12
            need(lower_slope >= 0 and lower_at6 > 0, "strict lower infinite ray failed")
        else:
            lower_slope = lower_at6 = None
        rays.append([b, k, upper_slope, upper_at6, lower_slope, lower_at6])
    implications = 0; trivial_one = 0; trivial_zero = 0
    for q in range(2, 7):
        for B in range(1 << len(D)):
            b = B.bit_count(); k = threshold(q, b)
            if not B & 1:
                # Label1 gives a one-class erasure of EVERY nonempty parent.
                need(4*q*7 + (2*q - 1)*b >= 16*q - 12, "legal1 cut failed")
                trivial_one += 1
            elif not k:
                trivial_zero += 1
            else:
                choices = [(j, row) for j, row in enumerate(ROWS)
                           if row[0] <= q and row[1] >= b and row[2] >= k]
                need(choices, "finite family misses a literal forbidden subset")
                j, (small_q, big_b, required) = choices[0]
                enlarged = B
                for i in range(len(D)):
                    if enlarged.bit_count() == big_b:
                        break
                    enlarged |= 1 << i
                need(enlarged & B == B and enlarged & 1 and
                     enlarged.bit_count() == big_b and small_q - 1 <= q - 1 and
                     required >= k, "invalid monotone implication witness")
                implications += 1
    counts = [comb(11, b - 1) for q, b, k in ROWS]
    need(sum(counts) == 1542 and sum(counts[-3:]) == 386,
         "wrong finite original-subset count")
    return {"scalar_threshold_table": table, "infinite_affine_rays": rays,
            "finite_families": [list(row) + [count] for row, count in zip(ROWS, counts)],
            "original_predicates": sum(counts), "new_predicates_beyond_q2_q3": 386,
            "five_threshold_subset_cases": 5*(1 << 12),
            "monotone_subset_implications": implications,
            "trivial_legal1_cases": trivial_one, "trivial_zero_cases": trivial_zero}


def capacities(fibers):
    M = []
    for d in D:
        M.append(max((max((sum(y % d == a for y in H) for a in range(d)), default=0)
                      for H in fibers), default=0))
    return sorted([[16*d, 2*c] for d, c in zip(D, M)] +
                  [[32*d, c] for d, c in zip(D, M)])


def hitting_clause(kernel):
    points = [x for x in range(2520) if x % 8 != 0 and
              x % 315 in kernel[x % 8 - 1]]
    need(len(points) == sum(map(len, kernel)), "wrong lower-period point inventory")
    return [[n, a] for n in BASE for a in sorted({x % n for x in points})]


def mono_minimality():
    # Four supported parents in order2/4/6/7;2and6 are monochromaticmod3.
    # No rainbow restriction is used in this universal <=12-point lower bound.
    vectors = 0
    for h in product(range(13), repeat=4):
        N = sum(h)
        if N > 12:
            continue
        vectors += 1
        if N:
            u = max(h[0], h[2], (h[1]+2)//3, (h[3]+2)//3)
            need(3*(max(h) + u + 10) >= 4*N,
                 "monochromatic-parent cardinality lower bound failed")
    return vectors


def point_shapes():
    # Entirely abstract truth controls for arbitrary monotone qualifications.
    cases = 0
    for values in combinations(range(12), 5):
        Q = [values[i] - i for i in range(5)]
        for b in range(1, 13):
            full = all(4*q*Q[q-2] + (2*q-1)*b >= 16*q-12 for q in range(2, 7))
            # Scalar retained rows are also allowed at larger B. Their
            # implication is checked above; here keep all q2/q3 B tests and
            # only the genuinely later critical changes at this same B.
            sparse = (all(4*q*Q[q-2] + (2*q-1)*b >= 16*q-12 for q in (2, 3)) and
                      (b != 5 or Q[2] >= 2) and (b != 3 or Q[3] >= 3) and
                      (b != 1 or Q[4] >= 4))
            need(full == sparse, "critical-change truth table failed")
            cases += 1
    return cases
