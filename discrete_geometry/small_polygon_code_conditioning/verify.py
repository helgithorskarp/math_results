#!/usr/bin/env python3
"""Exact supporting checks; the universal theorems are proved in PROOF.md.

Python 3.11+, standard library only. No floating-point proof decisions.
The rational short-arc fixtures do not enumerate the feasible code space.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def norm2(v):
    return sum(x*x for x in v)


def unit(t):
    """u(2 atan t), increasing in angle for the rational fixtures used."""
    return ((1-t*t)/(1+t*t), 2*t/(1+t*t))


def linear_sum(coefficients, vectors):
    require(len(coefficients) == len(vectors), "coefficient length")
    return tuple(sum(a*v[k] for a, v in zip(coefficients, vectors))
                 for k in range(2))


def switch_coefficients(code):
    require(len(code) >= 3 and all(type(c) is int and c in (-1, 1)
                                  for c in code), "malformed code")
    return [-(code[0]+code[-1])] + [code[j-1]-code[j]
                                  for j in range(1, len(code))]


def alternating(signs):
    return bool(signs) and all(abs(s) == 1 for s in signs) and all(
        a == -b for a, b in zip(signs, signs[1:]))


def short_arc_checks():
    grid = [Q(k, 16) for k in range(-4, 5)]
    points = [unit(t) for t in grid]
    require(all(norm2(p) == 1 for p in points), "unit-circle parametrization")
    # Both angles lie in (-pi/2,pi/2). The positive endpoint dot product
    # exceeding 1/2 certifies that this containing arc has length < pi/3.
    require(sum(x*y for x, y in zip(points[0], points[-1])) > Q(1, 2),
            "containing arc too long")
    require(norm2(tuple(b-a for a, b in zip(points[0], points[-1])))
            == Q(16, 17)**2, "endpoint chord")
    even = odd = 0
    for size in range(1, len(points)+1):
        for indices in combinations(range(len(points)), size):
            chosen = [points[j] for j in indices]
            vector = linear_sum([(-1)**j for j in range(size)], chosen)
            if size % 2:
                require(norm2(vector) > 0, "vanishing odd short-arc sum")
                odd += 1
            else:
                chord = tuple(b-a for a, b in zip(chosen[0], chosen[-1]))
                require(norm2(vector) <= norm2(chord) < 1,
                        "even short-arc chord bound")
                even += 1
    require(linear_sum([], []) == (0, 0), "empty paired sum")
    return {"even_subsets": even, "odd_subsets": odd, "empty_sum": 1,
            "containing_chord_squared": str(Q(16, 17)**2)}


def cut_checks():
    count = 0
    for length in (1, 3, 5, 7, 9):
        for start in (-1, 1):
            signs = [start*(-1)**j for j in range(length)]
            for cut in range(length+1):
                # A term is (original label, sign, vector orientation).
                moved = [(j, -signs[j], -1) for j in range(cut, length)]
                kept = [(j, signs[j], 1) for j in range(cut)]
                terms = moved + kept
                require(alternating([s for _, s, _ in terms]),
                        "cut broke alternating signs")
                require(sorted((j, s*o) for j, s, o in terms)
                        == list(enumerate(signs)), "cut changed a vector term")
                count += 1
    # Code fixtures cover a fixed nonzero coefficient, an omitted one,
    # additional zero coefficients, and the empty free-switch case.
    fixtures = [(1, -1, 1), (1, -1, 1, -1),
                (1, 1, -1, -1, 1), (-1, -1, 1, 1, -1, 1), (1, 1, 1)]
    for code in fixtures:
        coefficients = switch_coefficients(code)
        full = [a//2 for a in coefficients if a]
        require(len(full) % 2 == 1 and alternating(full), "full switch parity")
        free = [a//2 for a in coefficients[1:] if a]
        require(len(free) % 2 == (0 if coefficients[0] else 1),
                "omitted fixed coefficient parity")
    require(not alternating([-1, 1, 1]), "wrong-cut negative control")
    return {"half_circle_cuts": count, "code_fixtures": len(fixtures),
            "wrong_cut_detected": True}


# Exact Q(sqrt(3)) arithmetic for the sharp three-switch fixture.
def qadd(x, y):
    return (x[0]+y[0], x[1]+y[1])


def qscale(a, x):
    return (a*x[0], a*x[1])


def qmul(x, y):
    return (x[0]*y[0]+3*x[1]*y[1], x[0]*y[1]+x[1]*y[0])


def sharpness_checks():
    zero, one = (Q(0), Q(0)), (Q(1), Q(0))
    half, sqrt3half = (Q(1, 2), Q(0)), (Q(0), Q(1, 2))
    points = [(one, zero), (half, sqrt3half),
              (qscale(-1, half), sqrt3half)]
    coefficients = switch_coefficients((1, -1, 1))
    total = [zero, zero]
    for a, p in zip(coefficients, points):
        require(qadd(qmul(p[0], p[0]), qmul(p[1], p[1])) == one,
                "sharp fixture not on circle")
        total = [qadd(total[k], qscale(a, p[k])) for k in range(2)]
    require(total == [zero, zero], "sharp fixture closure")
    columns = [(qscale(-a, p[1]), qscale(a, p[0]))
               for a, p in zip(coefficients[1:], points[1:])]
    require([col[1] for col in columns] == [one, one],
            "sharp infinity norm with vertical unit multiplier")
    gram = [[zero, zero], [zero, zero]]
    for col in columns:
        for i in range(2):
            for j in range(2):
                gram[i][j] = qadd(gram[i][j], qmul(col[i], col[j]))
    require(gram == [[(Q(6), Q(0)), zero], [zero, (Q(2), Q(0))]],
            "fixture Gram matrix")
    # Strict order alone is not enough for the conditioning theorem.
    infeasible_points = [(Q(1), Q(0)), unit(Q(1, 100)), unit(Q(2, 100))]
    require(linear_sum(coefficients, infeasible_points) != (0, 0),
            "infeasible control accidentally closed")
    horizontal_projections = [-a*p[1] for a, p in
                              zip(coefficients[1:], infeasible_points[1:])]
    require(max(abs(x) for x in horizontal_projections) < 1,
            "feasibility-omission control did not violate bound")
    return {"sharp_fixture": "n=3, (+,-,+), pi/3 gaps; vertical multiplier",
            "gram_diagonal": [6, 2], "infeasible_countercontrol": True}


def poincare_checks():
    identities = fixtures = 0
    for n in range(3, 21):
        increments = [Q((j % 3)-1) for j in range(n-1)]
        increments.append(-sum(increments))
        values = [Q(0)]
        for d in increments:
            values.append(values[-1]+d)
        require(values[-1] == 0, "Dirichlet endpoint")
        for k in range(1, n):
            coefficients = [Q(int(j < k))-Q(k, n) for j in range(n)]
            require(norm2(coefficients) == Q(k*(n-k), n),
                    "Poincare coefficient norm identity")
            require(sum(a*d for a, d in zip(coefficients, increments))
                    == values[k], "Poincare reconstruction")
            identities += 1
        require(norm2(values) <= Q(n*n, 4)*norm2(increments),
                "Dirichlet Poincare bound")
        fixtures += 1
    unpinned = [Q(1)]*4
    require(norm2(unpinned) > 0 and
            norm2([b-a for a, b in zip(unpinned, unpinned[1:])]) == 0,
            "unpinned path negative control")
    return {"coefficient_identities": identities, "path_fixtures": fixtures,
            "unpinned_kernel_detected": True}


def constant_checks():
    pi_upper = Q(22, 7)
    margins = {
        # pi>3 and n>=3 suffice for the band inclusion, after multiplying n^4.
        "gap_band_margin": Q(9*9, 4)-Q(3, 200),
        "squared_gradient_constant_margin": 25-Q(27, 16)*pi_upper**2,
        "uniqueness_margin_coefficient": 1-2*Q(1, 4),
        "lagrangian_margin_coefficient": 1-2*Q(1, 4),
        "bingane_cutoff_margin": 2**17-Q(400, 18)*pi_upper**7,
        # 1/(400n^5)<1/(100n^3), multiplied by 400n^5, at n>=3.
        "saturation_threshold_margin": 4*3**2-1,
    }
    for label, value in margins.items():
        require(value > 0, label)
    require(25*Q(1, 400) == Q(1, 4)**2, "multiplier constant")
    # Integrated lower Taylor curvature, in rational units of 1/(12 pi),
    # for x<=t: (t-x)^2*(x+2t)>=2t*(t-x)^2.
    taylor = 0
    for t in (Q(1, 3), Q(1), Q(2)):
        for k in range(9):
            x = t*Q(k, 8)
            exact_integral_times_12pi = x**3-3*x*t*t+2*t**3
            factored = (t-x)**2*(x+2*t)
            require(exact_integral_times_12pi == factored
                    and factored >= 2*t*(t-x)**2, "Taylor lower curvature")
            taylor += 1
    rejected = 0
    for code in ((1, 1), (1, 0, -1), (True, -1, 1), (1, Q(1), -1)):
        try:
            switch_coefficients(code)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("malformed-code negative control accepted")
    return {"positive_margins": {k: str(v) for k, v in margins.items()},
            "multiplier_identity": True, "taylor_fixtures": taylor,
            "malformed_codes_rejected": rejected}


def main():
    result = {"status": "PASS", "arithmetic": "exact rational and Q(sqrt(3))",
              "short_arc": short_arc_checks(), "cut_convention": cut_checks(),
              "sharpness": sharpness_checks(), "poincare": poincare_checks(),
              "constants": constant_checks(),
              "scope": "Supporting fixtures and constants; universal proof is PROOF.md"}
    expected_path = Path(__file__).with_name("expected.json")
    if expected_path.exists():
        require(result == json.loads(expected_path.read_text()), "expected output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
