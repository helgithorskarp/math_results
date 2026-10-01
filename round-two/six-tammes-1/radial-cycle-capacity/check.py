#!/usr/bin/env python3
"""Exact scalar checks for the written radial and regular-hexagon proofs.

No numerical sampling is a proof step. All polynomial comparisons below are
identities plus signs on explicit intervals, as explained in the proof files.
"""

from collections import Counter
from fractions import Fraction as Q
from itertools import zip_longest
import json


def require(condition, label):
    if not condition:
        raise ValueError(label)


def qs(value):
    return str(value)


# Polynomials in c: exact rational coefficients in increasing degree order.
def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def add(p, r):
    return trim([sum(v) for v in zip_longest(p, r, fillvalue=Q(0))])


def scale(p, s):
    return trim([s * x for x in p])


def sub(p, r):
    return add(p, scale(r, -1))


def mul(p, r):
    out = [Q(0)] * (len(p) + len(r) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(r):
            out[i + j] += a * b
    return trim(out)


def peval(p, c):
    out = Q(0)
    for a in reversed(p):
        out = out * c + a
    return out


def identity(left, right, label):
    require(trim(left) == trim(right), label)


# Exact arithmetic in Q(sqrt(3)), represented as (a,b) for a+b*sqrt(3).
def radd(x, y):
    return x[0] + y[0], x[1] + y[1]


def rscale(x, s):
    return x[0] * s, x[1] * s


def rmul(x, y):
    return x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def sign(x):
    a, b = x
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0 or (a > 0) == (b > 0):
        return (b > 0) - (b < 0)
    gap = a * a - 3 * b * b
    s = (gap > 0) - (gap < 0)
    return s if a > 0 else -s


def check_radial():
    lo, hi, a, eps = Q(1, 2), Q(3, 5), Q(1, 6), Q(1, 40)
    hmin = min(lo - lo * lo, hi - hi * hi)
    require(hmin == Q(6, 25), "concave numerator endpoints")
    denominator = 1 - a * a
    B = (hmin - eps) / denominator
    rho2 = (1 + B) / 2
    beta2 = (1 - hi * hi) * rho2
    beta0 = Q(6251, 10000)
    require(B == Q(387, 1750) > 0, "tangent edge cosine")
    require(rho2 == Q(2137, 3500), "tangent coverage cosine squared")
    require(beta2 == Q(8548, 21875), "scalar coefficient squared")
    gap = beta2 - beta0 * beta0
    require(gap == Q(10993, 700000000) > 0, "strict coefficient gap")
    require(35 - Q(11, 2) ** 2 > 0, "sqrt(35) lower bound")
    margin = a * hi + beta0 * Q(4, 5)
    low_endpoint = a * a + beta0 * Q(11, 12)
    require(margin == hi + Q(1, 12500), "upper scalar endpoint")
    require(low_endpoint - margin == Q(1271, 1800000) > 0, "lower scalar endpoint")
    simplicity_gap = 1 - hi - eps
    require(simplicity_gap == Q(3, 8) > 0, "automatic simplicity")

    # Failure of this scalar certificate, not a counterexample to a geometric claim.
    wide_beta2 = (1 - hi * hi) * (1 + (hmin - Q(1, 30)) / denominator) / 2
    wide_gap = wide_beta2 - Q(5, 8) ** 2
    require(wide_gap < 0, "widened tolerance must fail this endpoint certificate")
    return {
        "edge_tolerance": qs(eps), "radial_floor": qs(a),
        "tangent_edge_cosine_lower": qs(B), "tangent_cover_cosine_squared": qs(rho2),
        "beta_squared": qs(beta2), "beta_rational_lower": qs(beta0),
        "beta_squared_gap": qs(gap), "strict_covering_lower": qs(margin),
        "lower_endpoint_extra_gap": qs(low_endpoint - margin),
        "automatic_simplicity_gap": qs(simplicity_gap),
        "negative_control_epsilon_1_30_endpoint_squared_gap": qs(wide_gap),
    }


def check_regular():
    one, c = (Q(1),), (Q(0), Q(1))
    omc = sub(one, c)
    z2 = sub(scale(c, 2), one)
    b2 = scale(omc, Q(3, 2))
    K2 = scale(add(one, c), Q(1, 2))
    G2 = scale(add(one, scale(c, 2)), Q(1, 3))
    identities = []

    def record(left, right, name):
        identity(left, right, name)
        identities.append(name)

    record(add(z2, b2), K2, "z2_plus_b2_equals_K2")
    record(sub(K2, mul(c, c)), scale(mul(omc, add(scale(c, 2), one)), Q(1, 2)),
           "root_discriminant_factor")
    record(sub(mul(G2, K2), z2),
           scale(mul(sub(scale(c, 2), (Q(7),)), sub(c, one)), Q(1, 6)),
           "G_is_above_peak")
    record(mul(b2, sub(one, G2)), mul(omc, omc), "gG_second_term_is_one_minus_c")
    record(sub(scale(sub(scale(mul(c, c), 4), one), Q(1, 3)), mul(z2, z2)),
           scale(mul(z2, omc), Q(4, 3)), "gG_strict_squared_gap")
    record(sub(mul(K2, K2), z2),
           scale(mul(omc, sub((Q(5),), c)), Q(1, 4)), "K_is_above_peak")
    record(mul(b2, sub(one, K2)), scale(mul(omc, omc), Q(3, 4)),
           "gK_second_term_squared")

    # Compare the rational and sqrt(3) coefficients of the transition identity.
    A = scale(mul(add(one, c), z2), Q(1, 2))
    real_lhs = sub(add(mul(c, c), scale(mul(omc, omc), Q(3, 4))), A)
    rad_lhs = scale(mul(c, omc), -1)
    record(real_lhs, scale(mul(omc, sub((Q(5),), scale(c, 3))), Q(1, 4)),
           "transition_identity_rational_coefficient")
    record(rad_lhs, scale(mul(omc, scale(c, -4)), Q(1, 4)),
           "transition_identity_sqrt3_coefficient")

    star = (Q(-5, 13), Q(20, 39))
    star_poly = radd(radd(rscale(rmul(star, star), 39), rscale(star, 30)), (Q(-25), Q(0)))
    require(star_poly == (0, 0), "transition quadratic")
    require(rmul(star, (Q(3), Q(4))) == (5, 0), "transition rationalization")
    require(sign(radd(star, (Q(-1, 2), Q(0)))) > 0, "transition above one half")
    require(sign(radd(star, (Q(-63, 125), Q(0)))) < 0, "transition below 63/125")
    require(Q(63, 125) < Q(14, 25), "benchmark outside improvement strip")
    poly = (Q(-25), Q(30), Q(39))
    p_control = peval(poly, Q(14, 25))
    require(p_control > 0, "K-height two-point fixture fails at 14/25")
    return {
        "polynomial_identities": identities,
        "transition_quadratic_coefficients": [qs(x) for x in poly],
        "transition_root_Q_sqrt3": [qs(x) for x in star],
        "transition_bracket": ["1/2", "63/125"],
        "capacity_2_interval": "1/2<c<=c_star",
        "capacity_1_interval": "c_star<c<1",
        "negative_control_c_14_25_transition_polynomial": qs(p_control),
    }


def check_center():
    a, b, lo, eps = Q(2, 5), Q(3, 5), Q(1, 2), Q(1, 40)
    B = (lo - eps - b * b) / (1 - a * a)
    rho2 = (1 + B) / 2
    beta2 = (1 - b * b) * rho2
    beta0 = Q(601, 1000)
    gap = beta2 - beta0 * beta0
    require(B == Q(23, 168) > 0, "center tangent edge lower bound")
    require(rho2 == Q(191, 336), "center tangent cover cosine squared")
    require(beta2 == Q(191, 525), "center coefficient squared")
    require(gap == Q(54779, 21000000) > 0, "center coefficient strict gap")
    require(21 > 4 ** 2 and 19 > 4 ** 2, "center endpoint radical lower bounds")
    lower = a * a + beta0 * Q(4, 5)
    upper = a * Q(9, 10) + beta0 * Q(2, 5)
    require(lower == Q(801, 1250) > upper == Q(1501, 2500) > b,
            "center scalar endpoints")
    pair_lower = 2 * Q(9, 10) ** 2 - 1
    require(pair_lower == Q(31, 50) > b, "common cap pair margin")
    require(2 * Q(29, 50) - 1 == a * a, "regular family center lower endpoint")
    require(2 * b - 1 <= b * b, "regular family center upper endpoint")
    return {
        "radial_interval": [qs(a), qs(b)],
        "tangent_edge_cosine_lower": qs(B), "tangent_cover_cosine_squared": qs(rho2),
        "beta_squared": qs(beta2), "beta_rational_lower": qs(beta0),
        "beta_squared_gap": qs(gap), "strict_covering_lower": qs(upper),
        "lower_endpoint_lower": qs(lower), "strict_insertion_cap_cosine": "9/10",
        "strict_pair_cosine_lower": qs(pair_lower), "pair_margin_above_3_5": qs(pair_lower - b),
        "regular_family_witness_interval": ["29/50", "3/5"],
    }


def check_fixture():
    c = Q(501, 1000)
    z2, R2 = 2 * c - 1, 2 - 2 * c
    A2, D2 = (1 + c) / 2, (1 - c) / 2
    require(z2 + R2 == A2 + D2 == 1, "fixture unit norms")
    require(A2 - D2 == c, "fixture interior contact")
    require(z2 * A2 == Q(1501, 1000000), "fixture axial radical")
    require(R2 * D2 == (1 - c) ** 2, "fixture horizontal product")
    require(1501 < 39 ** 2 and 3 < Q(7, 4) ** 2, "fixture radical upper bounds")
    cosine = [Q(1), Q(1, 2), Q(-1, 2), Q(-1), Q(-1, 2), Q(1, 2)]
    counts = Counter()
    contact_count = 0
    for i in range(6):
        for j in range(i + 1, 6):
            step = min(j - i, 6 - (j - i))
            dot = z2 + R2 * cosine[j - i]
            expected = {1: c, 2: 3 * c - 2, 3: 4 * c - 3}[step]
            require(dot == expected <= c, "boundary pair")
            counts[f"boundary_step_{step}"] += 1
            contact_count += dot == c
    # At q's azimuth pi/6, the six cosines are sqrt(3) times these coefficients.
    halfgap = [Q(1, 2), Q(1, 2), Q(0), Q(-1, 2), Q(-1, 2), Q(0)]
    cross_bounds = []
    for orientation in (1, -1):
        for coeff in halfgap:
            bound = Q(39, 1000) + (1 - c) * max(orientation * coeff, Q(0)) * Q(7, 4)
            require(bound < c, "insertion-boundary pair")
            cross_bounds.append(bound)
            counts["insertion_boundary"] += 1
    counts["insertion_insertion"] = 1
    contact_count += 1
    require(sum(counts.values()) == 28 and contact_count == 7, "complete fixture pair count")
    max_bound = max(cross_bounds)
    require(max_bound == Q(3805, 8000), "largest strict cross upper bound")
    require(3 > Q(5, 3) ** 2, "sqrt(3) strict lower bound")
    min_dot_upper = Q(39, 1000) - (1 - c) * Q(5, 6)
    require(min_dot_upper < Q(1, 6), "both fixture insertions violate radial hypothesis")
    interior_gap = 3 * (1 - c) / (2 * (2 * c - 1)) - (1 - c) / (1 + c)
    require(interior_gap > 0, "strict gnomonic interiority")
    p = 39 * c * c + 30 * c - 25
    require(p < 0, "fixture lies below capacity transition")
    return {
        "c": qs(c), "pair_categories": dict(sorted(counts.items())),
        "pairs_checked": 28, "contacts": contact_count,
        "strict_cross_dot_upper": qs(max_bound),
        "cross_dot_slack_lower": qs(c - max_bound),
        "minimum_boundary_dot_strict_upper_for_each_insertion": qs(min_dot_upper),
        "gnomonic_squared_apothem_minus_radius": qs(interior_gap),
        "transition_polynomial": qs(p),
    }


def main():
    output = {
        "author": "six-tammes-1", "role": "researcher",
        "evidence": "exact scalar checks; geometric arguments are written proofs",
        "radial_criterion": check_radial(),
        "geometric_center_criterion": check_center(),
        "regular_hexagon": check_regular(),
        "eight_point_control": check_fixture(),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
