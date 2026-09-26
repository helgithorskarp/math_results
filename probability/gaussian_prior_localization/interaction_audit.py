#!/usr/bin/env python3
"""Exact algebra controls for SHIFT_AVERAGING_BOUNDARY.md, not quadrature."""

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


SIGNS = tuple(product((-1, 1), repeat=3))


def q(s):
    return (s[1] * s[2], s[0] * s[2], s[0] * s[1])


def dot(u, v):
    return sum((a * b for a, b in zip(u, v)), F(0))


def minus(u, v):
    return tuple(a - b for a, b in zip(u, v))


def rank(matrix):
    rows = [[F(x) for x in row] for row in matrix]
    require(rows and all(len(r) == len(rows[0]) for r in rows), "matrix shape")
    p = 0
    for col in range(len(rows[0])):
        found = next((i for i in range(p, len(rows)) if rows[i][col]), None)
        if found is None:
            continue
        rows[p], rows[found] = rows[found], rows[p]
        pivot = rows[p][col]
        rows[p] = [x / pivot for x in rows[p]]
        for i in range(len(rows)):
            if i != p:
                scale = rows[i][col]
                rows[i] = [a - scale * b for a, b in zip(rows[i], rows[p])]
        p += 1
        if p == len(rows):
            break
    return p


def polynomial_product(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def audit():
    walsh = [(1, *s, *q(s)) for s in SIGNS]
    for i, j in product(range(7), repeat=2):
        require(sum(r[i] * r[j] for r in walsh) == (8 if i == j else 0),
                "Walsh Gram matrix")
    require(rank(walsh) == 7, "Walsh affine design rank")

    partitions = []
    probability = [[F(0)] * 4 for _ in range(4)]
    for mask in range(8):
        axes = tuple(j for j in range(3) if mask & (1 << j))
        groups = {}
        for s in SIGNS:
            groups.setdefault(tuple(s[j] for j in axes), []).append(s)
        j = len(axes)
        require(len(groups) == 2 ** j, "component count")
        require(all(len(g) == 2 ** (3 - j) for g in groups.values()),
                "component size")
        for group in groups.values():
            mean = [sum((F(s[i]) for s in group), F(0)) / len(group)
                    for i in range(3)]
            for i, k in product(range(3), repeat=2):
                cov = sum(((s[i] - mean[i]) * (s[k] - mean[k]) for s in group),
                          F(0)) / len(group)
                require(cov == (1 if i == k and i not in axes else 0),
                        "conditional covariance")
            for i in range(3):
                require(mean[i] == (group[0][i] if i in axes else 0),
                        "conditional mean")
        # Use z=t/ell. Each axis splits with probability 2z.
        poly = [F(1)]
        for i in range(3):
            poly = polynomial_product(poly, [0, 2] if i in axes else [1, -2])
        probability[j] = [a + b for a, b in zip(probability[j], poly)]
        partitions.append({"mask": mask, "components": 2 ** j,
                           "mass": str(F(1, 2 ** j)),
                           "free_coordinates": 3 - j,
                           "threshold_multiple": 2 ** j})
    require(probability == [[1, -6, 12, -8], [0, 6, -24, 24],
                            [0, 0, 12, -24], [0, 0, 0, 8]],
            "split-count probability polynomials")
    require([sum(row[i] for row in probability) for i in range(4)]
            == [1, 0, 0, 0], "total grid probability")
    # Only J=1 has a nonzero linear probability and a nonzero interaction.
    require(probability[1][1] * F(3, 4) == F(9, 2), "leading factor")

    types = Counter()
    for s, z in combinations(SIGNS, 2):
        h = sum(a != b for a, b in zip(s, z))
        k = sum(a != b for a, b in zip(q(s), q(z)))
        require(k == {1: 2, 2: 2, 3: 0}[h], "Q pair type")
        require(F(k, h) <= 2, "uniform error ratio")
        types[h, k] += 1
    require(sum(types.values()) == 28, "all pairs covered")

    geometries = []
    for t in (F(1, 4), F(1, 8), F(1, 16)):
        xs = [tuple(t * a for a in s) for s in SIGNS]
        ys = [tuple(t * a / 2 + t ** 4 * b for a, b in zip(s, q(s)))
              for s in SIGNS]
        margins = []
        motion = []
        ratios = []
        for i, j in combinations(range(8), 2):
            u, v = minus(xs[i], xs[j]), minus(ys[i], ys[j])
            e = tuple(b - a / 2 for a, b in zip(u, v))
            uu, vv, ee = dot(u, u), dot(v, v), dot(e, e)
            require(0 < vv < uu, "injectivity and strict contraction")
            require(ee / uu <= 2 * t ** 6 < F(1, 4), "perturbation bound")
            require(dot(v, minus(u, v)) == uu / 4 - ee > 0,
                    "strict final derivative")
            # The squared-distance derivative increases with the path parameter;
            # its maximum at the final endpoint is already strictly negative.
            step = minus(v, u)
            d0, d1 = 2 * dot(u, step), 2 * dot(v, step)
            require(d0 <= d1 < 0 and d1 - d0 == 2 * dot(step, step),
                    "all-time linear motion")
            margins.append(uu - vv)
            motion.append(-d1)
            ratios.append(ee / uu)
        ranks = [rank([(1, *x) for x in xs]) - 1,
                 rank([(1, *y) for y in ys]) - 1,
                 rank([(1, *x, *y) for x, y in zip(xs, ys)]) - 1]
        require(ranks == [3, 3, 6], "endpoint and paired affine ranks")
        geometries.append({"t": str(t), "ranks": ranks,
                           "min_squared_distance_loss": str(min(margins)),
                           "min_negative_final_derivative": str(min(motion)),
                           "max_error_ratio_squared": str(max(ratios))})

    square_margin = F(7, 8) ** 3 - F(13, 16) ** 2
    require(square_margin == F(5, 512) > 0, "radical sign margin")
    require(4 * F(13, 16) - 3 == F(1, 4), "bracket lower bound")
    require(F(9, 2) * F(1, 4) == F(9, 8), "strict limit margin")
    return {
        "status": "EXACT_ALGEBRA_CONTROLS_PASS",
        "scope": "No Gaussian integration or finite-t interaction-sign test.",
        "walsh_gram": "8 times identity of size 7",
        "partitions": partitions,
        "split_probability_polynomials_in_t_over_ell":
            [[str(x) for x in row] for row in probability],
        "pair_types": [{"h": h, "k": k, "count": types[h, k]}
                       for h, k in sorted(types)],
        "rational_geometry_controls": geometries,
        "square_margin": str(square_margin),
        "negative_limit_magnitude_over_Ka_strictly_greater_than": "9/8",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--expected", type=Path,
                        default=Path(__file__).with_name("INTERACTION_EXPECTED.json"))
    args = parser.parse_args()
    output = json.dumps(audit(), sort_keys=True, indent=2) + "\n"
    if args.check:
        require(args.expected.read_text() == output, "expected output mismatch")
        print("GAUSSIAN_SHIFT_INTERACTION_EXACT_CONTROLS_PASS",
              hashlib.sha256(output.encode()).hexdigest())
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
