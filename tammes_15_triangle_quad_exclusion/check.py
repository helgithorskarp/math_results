#!/usr/bin/env python3
"""Exact auxiliary checks for PROOF.md; CPython 3.11+, standard library only.

The hand proof supplies spherical geometry. No floating point is used here.
Polynomial positivity also receives a Bernstein check, different from the
derivative/monotonicity arguments in the hand proof.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from math import comb
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def trim(p):
    p = list(map(F, p))
    while len(p) > 1 and not p[-1]:
        p.pop()
    return tuple(p)


def add(p, q):
    return trim(tuple((p[i] if i < len(p) else 0)
                      + (q[i] if i < len(q) else 0)
                      for i in range(max(len(p), len(q)))))


def scale(p, k):
    return trim(tuple(k * x for x in p))


def mul(p, q):
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            r[i + j] += x * y
    return trim(r)


def power(p, n):
    require(n >= 0, "negative polynomial power")
    r = (F(1),)
    for _ in range(n):
        r = mul(r, p)
    return r


def evaluate(p, x):
    r = F(0)
    for a in reversed(p):
        r = r * x + a
    return r


def bernstein(p, lo, hi):
    """Convert p(lo+(hi-lo)t) to degree-n Bernstein coefficients on [0,1]."""
    require(lo < hi, "empty interval")
    affine = (lo, hi - lo)
    a = (F(0),)
    for x in reversed(p):
        a = add(mul(a, affine), (x,))
    n = len(p) - 1
    a += (F(0),) * (n + 1 - len(a))
    return tuple(sum((a[k] * F(comb(j, k), comb(n, k))
                      for k in range(j + 1)), F(0)) for j in range(n + 1))


def field_add(x, y):
    return x[0] + y[0], x[1] + y[1]


def field_mul(x, y):
    # Exact arithmetic in Q[c]/(c^2-1/3).
    return x[0] * y[0] + x[1] * y[1] / 3, x[0] * y[1] + x[1] * y[0]


def field_div(x, y):
    norm = y[0] * y[0] - y[1] * y[1] / 3
    require(norm != 0, "zero field denominator")
    return field_mul(x, (y[0] / norm, -y[1] / norm))


def field_eval(p):
    r = (F(0), F(0))
    for a in reversed(p):
        r = field_add(field_mul(r, (F(0), F(1))), (a, F(0)))
    return r


def polynomial_checks():
    c, one, h2 = (F(0), F(1)), (F(1),), (F(1), F(2))
    D = (F(1), F(2), F(-1))
    Q = add(mul(power(h2, 3), power((1, -1), 2)),
            scale(mul(power(c, 3), power((1, 3), 2)), -1))
    require(Q == trim((1, 4, 1, -11, -10, -1)), "Q expansion")
    require(evaluate(Q, F(3, 5)) == F(32, 3125), "Q endpoint")

    y_numerator = add(power(D, 2),
                      scale(mul(h2, power(c, 4)), -12))
    hi = F(119, 200)
    y_margin = evaluate(y_numerator, hi) / (4 * evaluate(h2, hi) * hi**4)
    require(y_margin == F(3081381928, 43916928699), "y endpoint")
    Q_bernstein = bernstein(Q, F(1, 2), F(3, 5))
    y_bernstein = bernstein(y_numerator, F(1, 2), hi)
    require(all(x > 0 for x in Q_bernstein), "Q positivity certificate")
    require(all(x > 0 for x in y_bernstein), "y positivity certificate")

    root_equation = add(mul(power(c, 2), (1, 3)),
                        scale(mul(h2, (1, -1)), -1))
    require(root_equation == mul((1, 1), (-1, 0, 3)), "root factorization")
    diagonal_numerator = add(mul(power(c, 2), (3, 2)), (-1,))
    require(diagonal_numerator == mul((-1, 2), power((1, 1), 2)),
            "diagonal numerator factorization")

    y2_field = field_div(field_eval(power(D, 2)),
                        field_eval(scale(mul(h2, power(c, 4)), 4)))
    require(y2_field == (F(0), F(6)), "special-root y half-angle")
    cos_y = field_div(field_add(field_eval(one), (-y2_field[0], -y2_field[1])),
                      field_add(field_eval(one), y2_field))
    cos_y_squared = field_mul(cos_y, cos_y)
    require(cos_y_squared == field_div(field_eval((13, -12)),
                                        field_eval((13, 12))),
            "special-root cosine square")
    incompatible = add(scale(mul((1, 1), (13, -12)), 2), (-13, -12))
    require(field_eval(incompatible) == (F(5), F(-10)),
            "incompatible equality reduction")
    require(F(1, 2)**2 != F(1, 3), "final contradictory root")

    return {
        "Q_at_3_over_5": str(evaluate(Q, F(3, 5))),
        "Q_Bernstein_coefficients": list(map(str, Q_bernstein)),
        "y_margin_at_119_over_200": str(y_margin),
        "y_numerator_Bernstein_coefficients": list(map(str, y_bernstein)),
        "special_root_equation": "(1+c)(3c^2-1)=0",
        "second_equality_in_Q_c": ["5", "-10"],
        "diagonal_positive_numerator": "(2c-1)(1+c)^2",
    }


def corner_checks():
    profiles = []
    surviving = []
    for n3, n4, n5 in product(range(16), repeat=3):
        if n3 + n4 + n5 != 15 or 3*n3 + 4*n4 + 5*n5 != 66:
            continue
        profiles.append([n3, n4, n5])
        if n5 % 2 == 0 and n5 <= n4 + 2*n3:
            surviving.append([n3, n4, n5])
    require(surviving == [[0, 9, 6], [2, 5, 8]], "degree-profile exhaustion")

    # Enumerate marked y positions directly, retaining labeled degree-4 vertices
    # and labeled degree-3 vertices, rather than solving a summarized inequality.
    arrangements = []
    signatures = set()
    for v4 in product(range(2), repeat=5):
        for v3 in product(range(3), repeat=2):
            if sum(v4) + sum(v3) == 8:
                arrangements.append([list(v4), list(v3)])
                signatures.add((sum(v4), *sorted(v3)))
    require(len(arrangements) == 7, "marked corner exhaustion")
    require(signatures == {(4, 2, 2), (5, 1, 2)}, "marked corner distributions")

    # Column order: degree-4 deficit-one, degree-5 deficit-one,
    # degree-4 deficit-two, degree-5 deficit-two. This is the q=7 frontier.
    deficits = [list(a) for a in product(range(3), repeat=4)
                if a[0] + a[1] + 2*a[2] + 2*a[3] == 2]
    require(len(deficits) == 5, "q=7 deficit cover")
    return {
        "q6_degree_profiles_before_corner_screen": profiles,
        "q6_profiles_after_pairing_and_capacity": surviving,
        "profile_2_5_8_labeled_marked_arrangements": len(arrangements),
        "profile_2_5_8_marked_distributions": [list(a) for a in sorted(signatures)],
        "q7_deficit_columns": ["n4_delta1", "n5_delta1", "n4_delta2", "n5_delta2"],
        "q7_deficit_cover": deficits,
        "q6_geometry_status": "both surviving profiles excluded by PROOF.md",
        "q7_geometry_status": "open; deficit cover only",
    }


def coordinate_check(path=None):
    path = Path(path) if path is not None else Path(__file__).with_name("incumbent_decimal.csv")
    raw = path.read_bytes()
    vertices = [tuple(F(x) for x in line.split(","))
                for line in raw.decode("ascii").splitlines()]
    require(len(vertices) == 15 and all(len(v) == 3 for v in vertices),
            "coordinate dimension and point count")
    norms = [sum(x*x for x in v) for v in vertices]
    require(all(n > 0 for n in norms), "zero coordinate vector")
    bound = F(119, 200)
    checked = 0
    for i, v in enumerate(vertices):
        for j in range(i):
            dot = sum(x*y for x, y in zip(v, vertices[j]))
            if dot > 0:
                require(dot*dot < bound*bound*norms[i]*norms[j],
                        f"normalized pair {j},{i} fails cosine threshold")
            checked += 1
    require(checked == 105, "incomplete pair check")
    return {"points": 15, "all_pairs": checked,
            "strict_normalized_cosine_upper_bound": str(bound),
            "decimal_input_sha256": sha256(raw).hexdigest(),
            "input_interpretation": "exact decimal rationals, normalized individually",
            "global_optimality_claim": False}


def main():
    result = {"agent": "six-tammes-1", "role": "researcher",
              "arithmetic": "exact Python integers and Fraction; no floats",
              "polynomial_checks": polynomial_checks(),
              "corner_checks": corner_checks(),
              "coordinate_prerequisite": coordinate_check()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
