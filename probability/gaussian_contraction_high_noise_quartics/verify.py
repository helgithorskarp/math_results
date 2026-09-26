#!/usr/bin/env python3
"""Finite exact audits for PROOF.md; no universal theorem is inferred here.

Python 3.11+ standard library. The teammate's rational enclosure and
multinomial replica code is reused explicitly and pinned by SHA256.
All failure checks survive python -O. No floating-point calculations.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import comb
from pathlib import Path
from random import Random
import json
import sys


HERE = Path(__file__).resolve().parent
PROBABILITY = HERE.parent
DEPENDENCIES = {
    "gaussian_majorisation_hankel_transport/bounds.py":
        "60ff5166c623797055f37442d5532b1a29c06275b8871fa4fdf34dcd12f54fc7",
    "gaussian_majorisation_hankel_transport/certify.py":
        "71af430dbbecc055471b9f72b288cf4ff4d60ff797aacce8acd08ce7ca14551e",
    "gaussian_majorisation_hankel_transport/example.json":
        "0c96a1d144417e0a4262e7d6d8a5a1d6d206d10679d627a474fcad16c16bc8c9",
    "gaussian_majorisation_rank_abel/flap_fixture.json":
        "2edec28b8738cb0713c0ba70e4e8ec80147857503fbe2d801b43dbef4861ac08",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


for relative, expected in DEPENDENCIES.items():
    require(sha256((PROBABILITY / relative).read_bytes()).hexdigest() == expected,
            "dependency changed: " + relative)

sys.path.insert(0, str(PROBABILITY / "gaussian_majorisation_hankel_transport"))
from bounds import I, exp_negative, sqrt_integer  # noqa: E402
from certify import difference_histogram, distance_matrix, moment_gap  # noqa: E402


def squared(v):
    return sum(x*x for x in v)


def variance(points):
    mean = [sum(row[j] for row in points) / len(points)
            for j in range(len(points[0]))]
    return sum(squared([x-y for x, y in zip(row, mean)]) for row in points)


def variance_audit():
    random = Random(260907041)
    count = 0
    for m in range(2, 13):
        for _ in range(20):
            points = [[F(random.randrange(-3, 4), 8) for _ in range(6)]
                      for _ in range(m+2)]
            require(all(squared(row) <= 1 for row in points), "radius check")
            first, extra, other = points[:m], points[m], points[m+1]
            mean = [sum(row[j] for row in first) / m for j in range(6)]
            u = [x-y for x, y in zip(extra, mean)]
            v = [x-y for x, y in zip(other, mean)]
            h = [(x-y)/2 for x, y in zip(u, v)]
            k = [(x+y)/2 for x, y in zip(u, v)]
            lhs = (variance(first) + variance(points)
                   - variance(first+[extra]) - variance(first+[other]))
            rhs = (F(2, m+1)*squared(h)
                   - F(2*m, (m+1)*(m+2))*squared(k))
            require(lhs == rhs, "two-extra-replica identity")
            require(lhs <= F(2, m+1), "radius estimate")
            require(variance(first+[extra])-variance(first)
                    == F(m, m+1)*squared(u), "online variance identity")
            count += 1
    return count


def gram_entry(i, j):
    return F(2, (i+j+2)*(i+j+3)*(i+j+4))


def jacobi_audit():
    rows = [[F((-1)**(k-j)*comb(k+1, j+1)*comb(k+j+3, j))
             for j in range(k+1)] for k in range(7)]
    norms = [F(k+1, 2*(k+2)*(k+3)) for k in range(7)]
    for k, p in enumerate(rows):
        for l, q in enumerate(rows):
            value = sum(p[i]*q[j]*gram_entry(i, j)
                        for i in range(len(p)) for j in range(len(q)))
            require(value == (norms[k] if k == l else 0),
                    "Jacobi orthogonality or norm")
    table = []
    for ell in range(7):
        inv = [[sum(rows[k][i]*rows[k][j]/norms[k]
                    for k in range(max(i, j), ell+1))
                for j in range(ell+1)] for i in range(ell+1)]
        for i, j in product(range(ell+1), repeat=2):
            value = sum(gram_entry(i, k)*inv[k][j] for k in range(ell+1))
            require(value == int(i == j), "exact inverse Gram product")
        trace = sum(inv[i][i] for i in range(ell+1))
        table.append({"ell": ell, "trace_inverse": str(trace),
                      "variance_radius_ratio": str(F(3, 8)*(ell+1)*trace)})
    require([row["variance_radius_ratio"] for row in table] ==
            ["9/2", "270", "12015", "497070", "19676475",
             "755720280", "28418013540"], "published constants")
    return table


def quartic_algebra_audit():
    # q = (a(1-t)-e*t)^2 + c*t(1-t). The roots are rational here;
    # the proof of completeness of this cone is analytic, not sampled.
    count = 0
    for a, e, c in product([F(0), F(1, 3), F(1), F(2)], repeat=3):
        coeff = [a*a, -2*a*(a+e)+c, (a+e)**2-c]
        require(sum(coeff) == e*e, "right endpoint")
        require(coeff[1]+2*coeff[0]+2*a*e == c, "cone decomposition")
        for t in [F(0), F(1, 7), F(1, 2), F(6, 7), F(1)]:
            require(sum(v*t**i for i, v in enumerate(coeff))
                    == (a*(1-t)-e*t)**2+c*t*(1-t), "quadratic identity")
        count += 1
    # Positive omitted terms in the atanh series give strict inequalities.
    first_two = F(2, 17)+F(2, 3*17**3)
    require(F(5, 2)*first_two-F(5, 17) == F(5, 14739),
            "rational determinant margin")
    return count


def interval_ldl(matrix):
    n = len(matrix)
    lower = [[I.of(int(i == j)) for j in range(n)] for i in range(n)]
    pivots = []
    for j in range(n):
        pivot = matrix[j][j]
        for k in range(j):
            pivot -= lower[j][k]*lower[j][k]*pivots[k]
        pivot = pivot.rounded(55)
        require(pivot.lo > 0, "positive LDL pivot not certified")
        pivots.append(pivot)
        for i in range(j+1, n):
            value = matrix[i][j]
            for k in range(j):
                value -= lower[i][k]*lower[j][k]*pivots[k]
            lower[i][j] = (value/pivot).rounded(55)
    return pivots


def check_fixture(name, x, y, w, radius_squared, s, max_m, hankel_level):
    x = [[F(c) for c in row] for row in x]
    y = [[F(c) for c in row] for row in y]
    w = [F(c) for c in w]
    require(all(v > 0 for v in w) and sum(w) == 1, "probability weights")
    require(all(squared(row) <= radius_squared for row in x), "input radius")
    require(s > 0, "positive variance")
    dx, dy = distance_matrix(x), distance_matrix(y)
    require(all(dx[i][j] >= dy[i][j]
                for i in range(len(w)) for j in range(len(w))), "contraction")
    deficit = sum(w[i]*w[j]*(dx[i][j]-dy[i][j])
                  for i in range(len(w)) for j in range(len(w)))
    require(deficit > 0, "fixture must have positive deficit")
    moments, weighted = {}, {}
    for m in range(2, max_m+1):
        hist = difference_histogram(dx, dy, w, m, s)
        moments[m] = moment_gap(hist, m, 65)
        require(moments[m].lo > 0, "positive moment gap")
        weighted[m] = (4*s*m*sqrt_integer(m, 65)*moments[m]/(m-1)).rounded(60)
    minor_margins = {}
    for m in range(2, max_m-1):
        margin = (weighted[m]*weighted[m+2]
                  - exp_negative(-radius_squared/((m+1)*s), 65)
                  * weighted[m+1]*weighted[m+1]).rounded(55)
        require(margin.lo > 0, "two-replica inequality not certified")
        minor_margins[str(m)] = margin.strings(24)
    a = {j: moments[j+2]/((j+1)*(j+2)) for j in range(max_m-1)}
    quartic_margin = (a[0]*a[2]-(1+F(5, 14739))*a[1]*a[1]).rounded(55)
    require(s >= F(17, 15)*radius_squared, "quartic variance condition")
    require(quartic_margin.lo > 0, "strengthened quartic determinant")
    require((a[1]-a[2]).lo > 0, "interval-localizing curvature")
    matrix = [[a[i+j] for j in range(hankel_level+1)]
              for i in range(hankel_level+1)]
    pivots = interval_ldl(matrix)
    return {"name": name, "atoms": len(w), "D": str(deficit),
            "radius_squared": str(radius_squared), "variance": str(s),
            "moments_computed_through": max_m,
            "weighted_log_convexity_margins": minor_margins,
            "strengthened_quartic_determinant": quartic_margin.strings(24),
            "hankel_level": hankel_level,
            "positive_LDL_pivots": [v.strings(24) for v in pivots]}


def main():
    variance_checks = variance_audit()
    table = jacobi_audit()
    cone_checks = quartic_algebra_audit()
    fold = json.loads((PROBABILITY /
                      "gaussian_majorisation_hankel_transport/example.json").read_text())
    flap = json.loads((PROBABILITY /
                      "gaussian_majorisation_rank_abel/flap_fixture.json").read_text())
    fixtures = [
        check_fixture("seven-point coordinate fold, quartic threshold",
                      fold["x"], fold["y"], fold["weights"], F(1), F(17, 15), 8, 1),
        check_fixture("sixteen-point simplex flap, quartic threshold",
                      flap["input"], flap["output"], flap["weights"], F(8), F(136, 15), 4, 1),
        check_fixture("seven-point coordinate fold, level-two threshold",
                      fold["x"], fold["y"], fold["weights"], F(1), F(12015), 6, 2),
    ]
    dx = distance_matrix([[F(c) for c in row] for row in fold["x"]])
    for m in range(2, 7):
        hist = difference_histogram(dx, dx, [F(c) for c in fold["weights"]], m, F(1))
        require(not hist and moment_gap(hist, m, 65) == I.of(0), "isometry boundary")
    print(json.dumps({"status": "ALL_FINITE_CHECKS_PASSED",
                      "scope": "Analytic universal proofs are in PROOF.md; finite checks alone prove no majorisation theorem.",
                      "arithmetic": "exact Fractions and outward rational intervals; no floating point",
                      "pinned_dependencies": DEPENDENCIES,
                      "variance_identity_checks": variance_checks,
                      "quadratic_cone_checks": cone_checks,
                      "isometry_zero_gap_checks": 5,
                      "jacobi_constant_table": table,
                      "fixtures": fixtures}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
