#!/usr/bin/env python3
"""Exact structural audits for PROOF.md; no numerical integration.

CPython 3.11.2, standard library only. All mathematical decisions use
integers or Fraction. The universal analytic proof is not encoded here.
Run --check to compare deterministic output to EXPECTED.json.
"""

from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def plus(a, b):
    return tuple(x + y for x, y in zip(a, b))


def minus(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm2(a):
    return dot(a, a)


def bary(weights, points):
    require(len(weights) == len(points), "barycenter length mismatch")
    return tuple(sum(w * x[k] for w, x in zip(weights, points))
                 for k in range(3))


def p_add(*polynomials):
    out = {}
    for poly in polynomials:
        for exponent, coefficient in poly.items():
            out[exponent] = out.get(exponent, F(0)) + coefficient
    return {e: c for e, c in out.items() if c}


def p_scale(poly, c):
    return {e: c * a for e, a in poly.items() if c * a}


def p_mul(a, b):
    out = {}
    for e, c in a.items():
        for f, d in b.items():
            ef = plus(e, f)
            out[ef] = out.get(ef, F(0)) + c * d
    return {e: c for e, c in out.items() if c}


def point_poly(points):
    out = {}
    for x in points:
        out[x] = out.get(x, F(0)) + F(1, len(points))
    return out


def audit():
    anchors = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    labels = [(i, j) for i in range(4) for j in range(4) if i != j]
    src = [minus(anchors[j], anchors[i]) for i, j in labels]
    dst = [plus(anchors[j], anchors[i]) for i, j in labels]
    axes = sorted(set(dst))
    require(len(src) == len(set(src)) == 12, "source must have 12 sites")
    require(len(axes) == 6, "output must have six sites")
    require(set(Counter(dst).values()) == {2}, "output multiplicities")
    require({norm2(x) for x in src} == {8}, "source radius")
    require({norm2(x) for x in dst} == {4}, "output radius")
    require({norm2(x) for x in anchors} == {3}, "anchor radius")
    for i in range(4):
        for j in range(4):
            require(dot(anchors[i], anchors[j]) == 4 * (i == j) - 1,
                    "tetrahedron Gram matrix")
    for (i, j), x in zip(labels, src):
        require(dot(anchors[i], x) == -4, "flap outside tetrahedron")
        require(min(dot(anchors[i], u) for u in anchors) == -1,
                "supporting tetrahedron halfspace")

    # Direct distances and the two closed formulas must agree entrywise.
    flap_losses = Counter()
    for m, n in combinations(range(12), 2):
        i, j = labels[m]
        k, ell = labels[n]
        loss = norm2(minus(src[m], src[n])) - norm2(minus(dst[m], dst[n]))
        formula = 16 * ((j == k) + (ell == i))
        require(loss == formula and loss >= 0, "flap distance identity")
        flap_losses[loss] += 1
    anchor_losses = Counter()
    for (i, _), x, y in zip(labels, src, dst):
        for k, u in enumerate(anchors):
            loss = norm2(minus(x, u)) - norm2(minus(y, u))
            require(loss == 16 * (i == k), "anchor distance identity")
            anchor_losses[loss] += 1

    # Four exact convex combinations. Every coefficient <= 3/12,
    # certifying exp(z.u_i) <= 3 F(z), for every real z by Jensen.
    jensen_rows = []
    for i in range(4):
        w = [F(1, 4) if b == i else
             F(1, 24) if a != i and b != i else F(0)
             for a, b in labels]
        require(sum(w) == 1 and min(w) >= 0, "Jensen mass")
        require(bary(w, src) == anchors[i], "Jensen barycenter")
        require(max(w) <= F(1, 4), "Jensen domination coefficient")
        jensen_rows.append([int(24 * a) for a in w])

    # Independent martingale coupling: six target rows, four sources
    # per row. Each row conditional mean is its target; joint column
    # masses are exactly 1/12.
    martingale_rows = []
    columns = [F(0)] * 12
    cost = F(0)
    for y in axes:
        nonzero = [k for k in range(3) if y[k]]
        require(len(nonzero) == 1, "axis support")
        k = nonzero[0]
        chosen = [i for i, x in enumerate(src) if x[k] == y[k]]
        require(len(chosen) == 4, "martingale conditional size")
        weights = [F(1, 4) if i in chosen else F(0) for i in range(12)]
        require(bary(weights, src) == y, "martingale conditional mean")
        for i, w in enumerate(weights):
            columns[i] += w / 6
            cost += w * norm2(minus(src[i], y)) / 6
        martingale_rows.append({"target": list(y), "source_indices": chosen})
    require(columns == [F(1, 12)] * 12, "martingale input marginal")
    require(cost == 4, "martingale squared cost")

    # Laurent-polynomial identities in exp(z_1), exp(z_2), exp(z_3).
    cosh = []
    for k in range(3):
        positive = tuple(2 if j == k else 0 for j in range(3))
        negative = tuple(-a for a in positive)
        cosh.append({positive: F(1, 2), negative: F(1, 2)})
    f_formula = p_scale(p_add(*(p_mul(cosh[i], cosh[j])
                               for i, j in combinations(range(3), 2))), F(1, 3))
    g_formula = p_scale(p_add(*cosh), F(1, 3))
    require(point_poly(src) == f_formula, "F Laurent identity")
    require(point_poly(dst) == g_formula, "G Laurent identity")

    # In independent variables v_k >= 0, verify the gap decomposition.
    zero = (0, 0, 0)
    one = {zero: F(1)}
    v = [{tuple(int(k == j) for j in range(3)): F(1)} for k in range(3)]
    c = [p_add(one, q) for q in v]
    e1 = p_add(*c)
    e2 = p_add(*(p_mul(c[i], c[j]) for i, j in combinations(range(3), 2)))
    gap = p_add(e2, p_scale(e1, -1))
    expected_gap = p_add(*v, *(p_mul(v[i], v[j])
                               for i, j in combinations(range(3), 2)))
    require(gap == expected_gap, "F-G positive polynomial")
    require(all(a > 0 for a in gap.values()), "gap coefficient signs")

    # This identity proves (23) without discarding the sign of a remainder:
    # (e2-e1)(3+2V) - V e2 = (3+V) sum_(i<j) v_i v_j.
    V = p_add(*v)
    P = p_add(*(p_mul(v[i], v[j]) for i, j in combinations(range(3), 2)))
    lhs = p_add(p_mul(gap, p_add(p_scale(one, 3), p_scale(V, 2))),
                p_scale(p_mul(V, e2), -1))
    rhs = p_mul(p_add(p_scale(one, 3), V), P)
    require(lhs == rhs, "ratio-gap remainder identity")
    require(all(a > 0 for a in rhs.values()), "ratio-gap remainder signs")

    # Dimensionless joining constants.
    lambda_R = F(1, 2)
    variance_R2 = F(8)
    uniform_error = 8 + 6 / lambda_R + 6 / lambda_R**2
    require(uniform_error == 44, "uniform tail error")
    require(lambda_R**2 * variance_R2 >= 1, "tail first regime")
    require(lambda_R * variance_R2 >= 4, "tail second regime")
    overlap = F(9, 64) - lambda_R**2 / 2
    require(overlap == F(1, 64) and overlap > 0, "threshold overlap")
    t0 = lambda_R**2 / 8
    require(t0 == F(1, 32), "flap join parameter")
    ratio = 2 * t0 / (3 + 4 * t0)
    require(ratio == F(1, 50), "flap margin")

    # Rational variance bounds: log(1+q) >= q/(1+q), proved in PROOF.md.
    table = []
    for alpha in [F(1, 100), F(1, 4), F(1, 2), F(3, 4), F(1)]:
        q = alpha / (50 * (3 - 2 * alpha))
        lower = q / (1 + q)
        require(lower == alpha / (150 - 99 * alpha), "margin simplification")
        s_r2 = 352 * (150 - 99 * alpha) / alpha
        require(s_r2 == 44 * 8 / lower, "variance bound")
        require(s_r2 >= 64, "window and tail regime")
        table.append({"alpha": str(alpha), "kappa_lower": str(lower),
                      "s_over_r_squared": str(s_r2)})

    return {
        "status": "exact structural and constant audits passed",
        "scope": "written analytic proof; no universal numerical hinge certification",
        "labels": [list(x) for x in labels],
        "flap_pair_count": sum(flap_losses.values()),
        "flap_squared_distance_loss_histogram": dict(sorted(flap_losses.items())),
        "anchor_flap_pair_count": sum(anchor_losses.values()),
        "anchor_squared_distance_loss_histogram": dict(sorted(anchor_losses.items())),
        "jensen_weights_numerators_denominator_24": jensen_rows,
        "martingale_conditionals": martingale_rows,
        "martingale_squared_cost": str(cost),
        "laurent_identity_monomial_counts": [len(f_formula), len(g_formula)],
        "positive_gap_polynomial_terms": len(gap),
        "positive_ratio_remainder_terms": len(rhs),
        "uniform_tail_error_constant": str(uniform_error),
        "overlap_exponent_coefficient": str(overlap),
        "flap_join_squared_parameter": str(t0),
        "flap_ratio_lower_at_join": str(ratio),
        "variance_table": table,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="compare output byte-for-byte with EXPECTED.json")
    args = parser.parse_args()
    result = audit()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check:
        expected = Path(__file__).with_name("EXPECTED.json").read_text()
        require(encoded == expected, "EXPECTED.json mismatch")
        print("PASS " + hashlib.sha256(encoded.encode()).hexdigest())
    else:
        sys.stdout.write(encoded)


if __name__ == "__main__":
    main()
