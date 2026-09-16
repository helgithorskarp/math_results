#!/usr/bin/env python3
"""Controls for the independent UD9-3 closure review."""

from fractions import Fraction as Q
from itertools import product
from json import dumps

import verify as V


def require(condition, message):
    if not condition:
        raise ValueError(message)


def evaluate_dense(poly, point):
    answer = poly[0] + sum(poly[1 + index] * point[index] for index in range(4))
    for coefficient, (left, right) in zip(poly[5:], V.QUADRATIC_INDICES):
        answer += coefficient * point[left] * point[right]
    return answer


def main():
    rho = (Q(0), Q(1))
    require(V.kmul(rho, rho) == (Q(-1), Q(1)), "rho square")
    roots = [rho]
    for _ in range(5):
        roots.append(V.kmul(roots[-1], rho))
    require(tuple(roots) == V.ROOTS[1:] + V.ROOTS[:1], "sixth-root cycle")

    probes = (
        (Q(0), Q(0), Q(0), Q(0)),
        (Q(1, 3), Q(-2, 5), Q(7, 4), Q(-1, 2)),
        (Q(-5, 7), Q(11, 13), Q(-3, 2), Q(17, 19)),
    )
    dense_value_controls = 0
    derivative_controls = 0
    for data, poly in zip(V.EQUATION_DATA, V.EQUATION_POLYNOMIALS):
        hessian = V.equation_hessian(data)
        for point in probes:
            require(evaluate_dense(poly, point) == V.equation_value(data, point),
                    "dense/direct equation mismatch")
            dense_value_controls += 1
            step = (Q(1, 17), Q(-1, 23), Q(2, 29), Q(-3, 31))
            moved = tuple(a + b for a, b in zip(point, step))
            gradient = V.equation_gradient(data, point)
            quadratic_remainder = Q(1, 2) * sum(
                hessian[row][column] * step[row] * step[column]
                for row, column in product(range(4), repeat=2)
            )
            require(V.equation_value(data, moved) == V.equation_value(data, point)
                    + sum(a * b for a, b in zip(gradient, step)) + quadratic_remainder,
                    "gradient/Hessian identity")
            derivative_controls += 1

    require(V.interval_product((Q(-2), Q(3)), (Q(-5), Q(7))) == (Q(-15), Q(21)),
            "mixed-sign interval product")
    require(V.interval_product((Q(-4), Q(-1)), (Q(-3), Q(-2))) == (Q(2), Q(12)),
            "negative interval product")
    three_words = V.canonical_colourings(9, V.SOURCE_EDGES, 3)
    four_words = V.canonical_colourings(9, V.SOURCE_EDGES, 4)
    require(not three_words and four_words, "source colour controls")

    source, directions, rounds, _ = V.build_closure()
    require(len(source) == 9 and len(directions) == 30, "formal source controls")
    require(tuple((row["points"], row["complete_unit_edges"]) for row in rounds) == V.EXPECTED_COUNTS,
            "round control")
    require(not V.proper("0" * 432, 432, ((0, 1),)), "bad word accepted")
    require(not V.proper("012", 432, ()), "short word accepted")

    result = {
        "all_controls_passed": True,
        "sixth_root_controls": 2,
        "dense_value_controls": dense_value_controls,
        "derivative_hessian_controls": derivative_controls,
        "interval_sign_controls": 2,
        "source_colour_controls": 2,
        "formal_closure_controls": 3,
        "malformed_word_controls": 2,
    }
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
