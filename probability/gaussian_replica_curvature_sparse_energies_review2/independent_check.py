#!/usr/bin/env python3
"""Independent exact algebra checks for the replica-curvature review.

This script does not import the submitted verifier or any sibling package.
The universal inequalities still rest on the analytic argument in README.md.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, product
from math import factorial
import json


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def add(left: dict[int, F], right: dict[int, F], scale: F = F(1)) -> dict[int, F]:
    out = defaultdict(F, left)
    for degree, coefficient in right.items():
        out[degree] += scale * coefficient
    return {degree: coefficient for degree, coefficient in out.items() if coefficient}


def multiply(left: dict[int, F], right: dict[int, F]) -> dict[int, F]:
    out: dict[int, F] = defaultdict(F)
    for i, x in left.items():
        for j, y in right.items():
            out[i + j] += x * y
    return {degree: coefficient for degree, coefficient in out.items() if coefficient}


def scale(poly: dict[int, F], value: F) -> dict[int, F]:
    return {degree: value * coefficient for degree, coefficient in poly.items() if value * coefficient}


def two_atom_expression(m: int) -> dict[F, F]:
    """Return coefficients w_c in B_m/s = sum_c w_c E_c by sign enumeration."""
    coefficients: dict[F, F] = defaultdict(F)
    for signs in product((-1, 1), repeat=m):
        if signs[0] == signs[1]:
            continue
        plus = sum(sign == 1 for sign in signs)
        c = F(2 * plus * (m - plus), m)
        coefficients[c] += F(4, 2**m) / c
    return dict(sorted(coefficients.items()))


def normalized_series_coefficient(expression: dict[F, F], order: int) -> dict[int, F]:
    """Coefficient of u^(order-1) in B_m/D, as a polynomial in L=lambda^2."""
    # E_c=sum_{k>=1}(-c)^k(L^k-1)u^k/k! and D=2su(1-L).
    common = -sum(weight * (-c) ** order for c, weight in expression.items()) / (2 * factorial(order))
    return {degree: common for degree in range(order)} if common else {}


def bernoulli_audit() -> dict[str, object]:
    expressions = {m: two_atom_expression(m) for m in (2, 3, 4)}
    expected = {
        2: {F(1): F(2)},
        3: {F(4, 3): F(3, 2)},
        4: {F(3, 2): F(2, 3), F(2): F(1, 2)},
    }
    require(expressions == expected, "two-atom replica formulas")

    first = {m: normalized_series_coefficient(expressions[m], 1) for m in expressions}
    linear = {m: normalized_series_coefficient(expressions[m], 2) for m in expressions}
    require(all(poly == {0: F(1)} for poly in first.values()), "B_m/D leading term")
    require(linear == {
        2: {0: F(-1, 2), 1: F(-1, 2)},
        3: {0: F(-2, 3), 1: F(-2, 3)},
        4: {0: F(-7, 8), 1: F(-7, 8)},
    }, "B_m/D first correction")
    log_curvature = add(add(linear[2], linear[4]), linear[3], F(-2))
    require(log_curvature == {0: F(-1, 24), 1: F(-1, 24)}, "sharp logarithmic coefficient")

    # For lambda=0 put x=exp(-u/6), hence E_c=1-x^(6c).
    b2 = {0: F(2), 6: F(-2)}
    b3 = {0: F(3, 2), 8: F(-3, 2)}
    b4 = {0: F(7, 6), 9: F(-2, 3), 12: F(-1, 2)}
    curvature = scale(add(multiply(b2, b4), multiply(b3, b3), F(-1)), F(12))
    target = {0: F(1), 6: F(-28), 8: F(54), 9: F(-16),
              12: F(-12), 15: F(16), 16: F(-27), 18: F(12)}
    require(curvature == target, "enumerated two-atom curvature polynomial")
    obstruction = {
        0: F(-1), 1: F(-2), 2: F(-4), 3: F(-6), 4: F(-9), 5: F(-12),
        6: F(12), 7: F(36), 8: F(33), 9: F(46), 10: F(32),
        11: F(34), 12: F(21), 13: F(24), 14: F(12),
    }
    factor = multiply(multiply({0: F(-1), 1: F(3), 2: F(-3), 3: F(1)},
                               {0: F(1), 1: F(1)}), obstruction)
    require(factor == target, "obstruction factorization")
    positive = sum(value for value in obstruction.values() if value > 0)
    negative = -sum(value for value in obstruction.values() if value < 0)
    lower_bound = positive * F(9, 10) ** 14 - negative
    require((positive, negative) == (250, 34) and lower_bound > 0,
            "obstruction interval sign")
    return {
        "expressions": {
            str(m): {str(c): str(weight) for c, weight in expression.items()}
            for m, expression in expressions.items()
        },
        "log_curvature_linear_coefficient": ["-1/24", "-1/24"],
        "factorization_verified": True,
        "obstruction_lower_bound_at_9_over_10": str(lower_bound),
    }


def two_extra_replica_audit() -> dict[str, int]:
    count = 0
    exchangeability = 0
    for m in range(2, 201):
        # Coefficients of |u|^2, |v|^2, and <u,v>.
        direct = (F(1, m + 1) - F(1, m + 2),
                  F(1, m + 1) - F(1, m + 2), F(-2, m + 2))
        claimed = (F(1, 2 * (m + 1)) - F(m, 2 * (m + 1) * (m + 2)),
                   F(1, 2 * (m + 1)) - F(m, 2 * (m + 1) * (m + 2)),
                   F(-1, m + 1) - F(m, (m + 1) * (m + 2)))
        require(direct == claimed, "two-extra identity")
        variance_coefficient = 2 * direct[0]
        mean_coefficient = 2 * direct[0] + direct[2]
        require(variance_coefficient == F(2, (m + 1) * (m + 2)), "tilted variance coefficient")
        require(mean_coefficient == F(-2 * m, (m + 1) * (m + 2)), "tilted mean coefficient")
        count += 1
        require(F(1, 2 * m) * F(m * (m - 1), 2) == F(m - 1, 4),
                "replica exchangeability factor")
        exchangeability += 1
    return {"m_values": count, "relative_gap_exchangeability_values": exchangeability}


def polynomial_audit() -> dict[str, object]:
    # 32 V''=(2t-1)^2(24t^5+24t^4+18t^3+12t^2+4t+1).
    curvature_factor = multiply({0: F(1), 1: F(-4), 2: F(4)},
                                {0: F(1), 1: F(4), 2: F(12), 3: F(18),
                                 4: F(24), 5: F(24)})
    require(curvature_factor == {0: F(1), 3: F(-14), 7: F(96)},
            "degree-nine curvature factorization")
    # Squaring clears the two positive square roots in the failed prefix test.
    require(F(1, 128**2 * 2) < F(49, 400**2 * 5), "weighted prefix sign")
    quartic_log_margin = F(5, 2) * F(2, 3 * 17**3)
    require(quartic_log_margin == F(5, 14739), "quartic logarithmic margin")

    sequence = [F(1), F(1, 2), F(1, 3), F(1, 4), F(19, 100)]
    require(all(sequence[i] * sequence[i + 2] > sequence[i + 1] ** 2 for i in range(3)),
            "abstract strict log-convexity")
    determinant = (sequence[0] * sequence[2] * sequence[4]
                   + 2 * sequence[1] * sequence[2] * sequence[3]
                   - sequence[0] * sequence[3] ** 2
                   - sequence[2] ** 3
                   - sequence[4] * sequence[1] ** 2)
    require(determinant == F(-1, 2700), "abstract Hankel determinant")

    moment_triples = 0
    hilbert_minors = 0
    a = [F(1, n + 1) for n in range(31)]
    for p, q, r in combinations(range(11), 3):
        m_value, n_value = a[q] / a[p], a[r] / a[p]
        require(0 < n_value < m_value < 1, "decreasing moment triple")
        require(m_value ** (r - p) < n_value ** (q - p), "strict secant inequality")
        moment_triples += 1
    for p in range(11):
        for u in range(1, 10):
            for v in range(1, 10):
                require(a[p] * a[p + u + v] > a[p + u] * a[p + v],
                        "arbitrary-offset Hankel minor")
                hilbert_minors += 1

    # Exact controls for the endpoint-square decomposition of nonnegative quadratics.
    decompositions = 0
    for root0 in range(6):
        for root1 in range(6):
            endpoint0, endpoint1 = F(root0**2), F(root1**2)
            for linear in range(-20, 21):
                quadratic = endpoint1 - endpoint0 - linear
                minimum = min(endpoint0, endpoint1)
                if quadratic > 0:
                    vertex = F(-linear, 2 * quadratic)
                    if 0 < vertex < 1:
                        minimum = endpoint0 + linear * vertex + quadratic * vertex**2
                if minimum < 0:
                    continue
                square = {0: F(root0**2),
                          1: F(-2 * root0 * (root0 + root1)),
                          2: F((root0 + root1) ** 2)}
                original = {0: endpoint0, 1: F(linear), 2: quadratic}
                difference = add(original, square, F(-1))
                c = difference.get(1, F(0))
                require(c >= 0 and difference == ({1: c, 2: -c} if c else {}),
                        "quadratic interval decomposition")
                decompositions += 1

    return {
        "degree_nine_factorization_verified": True,
        "weighted_prefix_is_negative": True,
        "quartic_log_margin": str(quartic_log_margin),
        "abstract_hankel_determinant": str(determinant),
        "strict_moment_triples": moment_triples,
        "positive_arbitrary_offset_minors": hilbert_minors,
        "quadratic_interval_decompositions": decompositions,
    }


def main() -> None:
    report = {
        "status": "INDEPENDENT_REPLICA_CURVATURE_AUDIT_PASSED",
        "arithmetic": "exact rational; standard library only",
        "scope": "Finite algebra checks support, but do not replace, the universal analytic proof.",
        "two_extra_replica": two_extra_replica_audit(),
        "bernoulli_sharpness": bernoulli_audit(),
        "polynomial_and_hankel": polynomial_audit(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
