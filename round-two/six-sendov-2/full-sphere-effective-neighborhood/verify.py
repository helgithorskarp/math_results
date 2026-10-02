#!/usr/bin/env python3
"""Exact certificates for the effective full-sphere angular neighborhood.

CPython 3.11, standard library only.  The analytic resolvent and representation
arguments are in PROOF.md; finite arithmetic here does not formalize them.
Classical polynomial/Sturm and rational interval arithmetic are implemented
directly.  Compression controls use a nonorthogonal seven-dimensional basis;
spectral witness controls independently use the monotone scalar secular equation.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import comb
from pathlib import Path
import resource
import time


def require(value, message):
    if not value:
        raise ValueError(message)


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(p, q):
    out = [Q(0)] * max(len(p), len(q))
    for i, x in enumerate(p):
        out[i] += x
    for i, x in enumerate(q):
        out[i] += x
    return trim(out)


def scale(p, c):
    return trim([x * c for x in p])


def mul(p, q):
    out = [Q(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return trim(out)


def power(p, n):
    out = [Q(1)]
    for _ in range(n):
        out = mul(out, p)
    return out


def derivative(p):
    return trim([i * x for i, x in enumerate(p)][1:] or [Q(0)])


def evaluate(p, x):
    out = Q(0)
    for c in reversed(p):
        out = out * x + c
    return out


def divide(p, q):
    p, q = trim(p), trim(q)
    require(q != [0], "zero polynomial divisor")
    out = [Q(0)] * max(1, len(p) - len(q) + 1)
    while p != [0] and len(p) >= len(q):
        i, c = len(p) - len(q), p[-1] / q[-1]
        out[i] += c
        p = add(p, scale([Q(0)] * i + q, -c))
    return trim(out), p


def sturm(p):
    out = [p, derivative(p)]
    while out[-1] != [0]:
        nxt = scale(divide(out[-2], out[-1])[1], -1)
        if nxt == [0]:
            break
        out.append(nxt)
    return out


def variations(chain, x):
    signs = [1 if y > 0 else -1 for p in chain if (y := evaluate(p, x))]
    return sum(a != b for a, b in zip(signs, signs[1:]))


def interval_add(a, b):
    return a[0] + b[0], a[1] + b[1]


def interval_mul(a, b):
    values = [x * y for x in a for y in b]
    return min(values), max(values)


def interval_scale(a, c):
    return (a[0] * c, a[1] * c) if c >= 0 else (a[1] * c, a[0] * c)


def interval_div(a, b):
    require(b[0] > 0 or b[1] < 0, "interval division through zero")
    return interval_mul(a, (1 / b[1], 1 / b[0]))


def interval_poly(p, x):
    out = (Q(0), Q(0))
    for c in reversed(p):
        out = interval_add(interval_mul(out, x), (c, c))
    return out


def interval_square(a):
    if a[0] <= 0 <= a[1]:
        return Q(0), max(a[0] ** 2, a[1] ** 2)
    return min(x * x for x in a), max(x * x for x in a)


def outward_dyadic(a, bits=160):
    """Exact directed rounding, keeping portable witness fixtures compact."""
    denominator = 1 << bits
    lower = (a[0].numerator * denominator) // a[0].denominator
    upper = -((-a[1].numerator * denominator) // a[1].denominator)
    result = Q(lower, denominator), Q(upper, denominator)
    require(result[0] <= a[0] <= a[1] <= result[1],
            "directed dyadic enclosure")
    return result


def sqrt_interval(a):
    require(a[0] > 0, "nonpositive square-root input")
    out = []
    for x in a:
        lo, hi = Q(0), max(Q(1), x)
        for _ in range(150):
            mid = (lo + hi) / 2
            if mid * mid < x:
                lo = mid
            else:
                hi = mid
        out.append((lo, hi))
    return out[0][0], out[1][1]


def encoded(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {str(k): encoded(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encoded(v) for v in x]
    return x


QPOLY = list(map(Q, [746, 4737, 11175, 11695, 4575]))
NPOLY = list(map(Q, [12, 24, 20]))
DPOLY = mul(list(map(Q, [10, 24, 15])), list(map(Q, [11, 38, 35])))
FNUM = scale(mul(power([Q(-1), Q(1)], 2),
                 power([Q(3), Q(5)], 2)), Q(8))
A7 = list(map(Q, [12684, 103380, 366599, 751299, 993954,
                 872170, 470475, 117375]))
B7 = list(map(Q, [42424, 326238, 1074965, 2064611, 2726970,
                 2646100, 1685625, 496875]))


def alpha_interval():
    lo, hi = Q(-853410556973738, 10 ** 15), Q(-853410556973736, 10 ** 15)
    chain = sturm(QPOLY)
    require(variations(chain, lo) - variations(chain, hi) == 1,
            "alpha root not uniquely isolated")
    require(evaluate(QPOLY, lo) > 0 > evaluate(QPOLY, hi),
            "alpha endpoint orientation")
    for _ in range(110):
        mid = (lo + hi) / 2
        if evaluate(QPOLY, mid) > 0:
            lo = mid
        else:
            hi = mid
    return lo, hi


def majorant(x):
    return ((Q(25, 4) + x * x) ** 2
            + 2 * (Q(5, 2) + x) ** 4 / (1 - 8 * x) ** 2
            ) / (Q(1, 2) - 2 * x - 5 * x * x - 4 * x ** 3 - x ** 4)


def tail(x):
    return (majorant(x) - Q(1875, 8) - Q(7375, 2) * x
            - Q(205075, 4) * x * x) / x ** 3


def validate_domain(unit_radius=Q(1, 250000), raw_radius=Q(1, 100000),
                    remainder=Q(620000), coefficient=Q(300)):
    require(0 < raw_radius < Q(1, 8), "raw spectral domain")
    require(Q(1, 2) - 2 * raw_radius - 5 * raw_radius ** 2
            - 4 * raw_radius ** 3 - raw_radius ** 4 > 0,
            "denominator majorant domain")
    require(tail(raw_radius) < remainder, "third-order remainder constant")
    require(Q(247, 100) * unit_radius / (1 - unit_radius ** 2 / 2)
            < raw_radius, "unit-to-raw chart inclusion")
    require(340 - remainder * Q(25, 4) * raw_radius > coefficient,
            "normalized quadratic coercivity margin")


def matrix_product(a, b):
    return [[sum(x * y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]


def compression_control(u):
    require(len(u) == 8 and sum(u) == 0, "balanced eight-coordinate input")
    # B=(e_i-e_8)_{i=1}^7; Gram K=I+J, K^{-1}=I-J/8.
    k = [[Q(int(i == j) + 1) for j in range(7)] for i in range(7)]
    ki = [[Q(int(i == j)) - Q(1, 8) for j in range(7)] for i in range(7)]
    m = [[u[i] * int(i == j) + u[7] for j in range(7)] for i in range(7)]
    a = matrix_product(ki, m)
    require(matrix_product(k, a) == m, "Gram selfadjoint compression")
    ident = [[Q(int(i == j)) for j in range(7)] for i in range(7)]
    ap, traces = ident, [Q(7)]
    for _ in range(7):
        ap = matrix_product(ap, a)
        traces.append(sum(ap[i][i] for i in range(7)))
    coeff = [Q(1)]
    for j in range(1, 8):
        coeff.append(-sum(coeff[j - i] * traces[i]
                          for i in range(1, j + 1)) / j)
    characteristic = list(reversed(coeff))
    f = [Q(1)]
    for x in u:
        f = mul(f, [-x, Q(1)])
    require(characteristic == scale(derivative(f), Q(1, 8)),
            "entire degree-seven compression characteristic identity")
    vector = list(u[:7])
    moments = []
    for _ in range(3):
        kv = [sum(x * y for x, y in zip(row, vector)) for row in k]
        moments.append(sum(x * y for x, y in zip(u[:7], kv)))
        vector = [sum(x * y for x, y in zip(row, vector)) for row in a]
    n = sum(x ** 2 for x in u)
    expected = [n, sum(x ** 3 for x in u), sum(x ** 4 for x in u) - n * n / 8]
    require(moments == expected, "full-compression coupling moments")
    return characteristic, moments


def secular_roots(u):
    levels = sorted(set(u))
    roots = []
    for lo, hi in zip(levels, levels[1:]):
        for _ in range(155):
            mid = (lo + hi) / 2
            value = sum(1 / (x - mid) for x in u)
            if value < 0:
                lo = mid
            elif value > 0:
                hi = mid
            else:
                lo = hi = mid
                break
        require(all(not lo <= x <= hi for x in u), "root enclosure meets a pole")
        if lo != hi:
            require(sum(1 / (x - lo) for x in u) < 0
                    < sum(1 / (x - hi) for x in u), "secular root signs")
        roots.append((lo, hi))
    return roots


def root_mass(u, root):
    square_sum = (Q(0), Q(0))
    for x in u:
        pole = (x - root[1], x - root[0])
        inv = interval_div((Q(1), Q(1)), pole)
        square_sum = interval_add(square_sum, interval_square(inv))
    return outward_dyadic(interval_div((Q(64), Q(64)), square_sum))


def witness(name, u, alpha, cbox):
    characteristic, moments = compression_control(u)
    roots = secular_roots(u)
    masses = [root_mass(u, r) for r in roots]
    n = sum(x * x for x in u)
    d = sum(x ** 4 for x in u) - n * n / 8
    require(d > 0, "witness denominator")
    total = tuple(sum(m[i] for m in masses) for i in [0, 1])
    require(total[0] <= n <= total[1], "all full-eigenspace masses sum to N")
    spectral_moments = []
    for j in range(3):
        total_j = (Q(0), Q(0))
        for r, m in zip(roots, masses):
            rpower = (Q(1), Q(1))
            for _ in range(j):
                rpower = interval_mul(rpower, r)
            total_j = interval_add(total_j, interval_mul(rpower, m))
        require(total_j[0] <= moments[j] <= total_j[1],
                "all scalar spectral moments match full matrix compression")
        spectral_moments.append(outward_dyadic(total_j))
    active = [i for i, r in enumerate(roots)
              if Q(-3, 50) < r[0] <= r[1] < Q(-1, 25)
              or Q(3, 5) < r[0] <= r[1] < Q(63, 100)]
    require(len(active) == 2, "exactly two selected active roots")
    active_square = (Q(0), Q(0))
    all_square = (Q(0), Q(0))
    for i, m in enumerate(masses):
        all_square = interval_add(all_square, interval_square(m))
        if i in active:
            active_square = interval_add(active_square, interval_square(m))
    cplus = outward_dyadic(interval_scale(interval_add((n * n, n * n),
                           interval_scale(active_square, -1)), 1 / d))
    actual = outward_dyadic(interval_scale(interval_add((n * n, n * n),
                           interval_scale(all_square, -1)), 1 / d))
    rawbase = [alpha] * 4 + [(Q(1), Q(1))] * 3 + [
        (-4 * alpha[1] - 3, -4 * alpha[0] - 3)]
    inner = (Q(0), Q(0))
    for x, y in zip(u, rawbase):
        inner = interval_add(inner, interval_scale(y, x))
    n0 = interval_poly(NPOLY, alpha)
    norm_product = sqrt_interval(interval_scale(n0, n))
    cosine = interval_div(inner, norm_product)
    distance2 = outward_dyadic(interval_add((Q(2), Q(2)), interval_scale(cosine, -2)))
    require(0 < distance2[0] <= distance2[1] < Q(1, 250000) ** 2,
            "witness unit-orbit neighborhood")
    slack = cbox[0] - cplus[1] - 300 * distance2[1]
    require(slack > 0, "witness actual two-active-mass coercivity")
    omitted = outward_dyadic(interval_scale(interval_add(all_square,
                              interval_scale(active_square, -1)), 1 / d))
    if len(roots) > 2:
        require(omitted[0] > 0, "positive omitted mass-square gap")
    return {"name": name, "u": u, "levels": len(set(u)),
            "characteristic": characteristic, "compression_moments": moments,
            "scalar_spectral_moment_enclosures": spectral_moments,
            "gap_roots": roots, "raw_full_eigenspace_masses": masses,
            "C": actual, "C_plus": cplus, "unit_distance_squared_to_base": distance2,
            "coercivity_slack_lower": slack, "omitted_gap": omitted}


def verify():
    records = {}
    alpha = alpha_interval()
    records["unique_alpha_refinement"] = alpha
    n0 = interval_poly(NPOLY, alpha)
    require(6 < n0[0] <= n0[1] < Q(61, 10) < Q(247, 100) ** 2,
            "base norm and chart bounds")
    records["base_norm_interval"] = outward_dyadic(n0)
    s4 = add(add(scale(power([Q(0), Q(1)], 4), 4), [Q(3)]),
             power([Q(3), Q(4)], 4))
    delta = add(s4, scale(mul(NPOLY, NPOLY), Q(-1, 8)))
    d0 = interval_poly(delta, alpha)
    require(d0[0] > Q(1, 2), "base denominator bound")
    records["base_denominator_interval"] = outward_dyadic(d0)
    s6 = add(add(scale(power([Q(0), Q(1)], 6), 4), [Q(3)]),
             power([Q(3), Q(4)], 6))
    gradient_square = add(add(scale(s6, 16),
                         scale(mul(NPOLY, s4), -4)), scale(power(NPOLY, 3), Q(1, 4)))
    grad = interval_poly(gradient_square, alpha)
    require(0 < grad[0] <= grad[1] < 4, "denominator linear coefficient bound")
    records["denominator_gradient_squared"] = outward_dyadic(grad)
    require(Q(-1) < alpha[0] < alpha[1] < 0
            and 0 < -4 * alpha[1] - 3 < -4 * alpha[0] - 3 < 1,
            "all raw coordinate absolute values at most one")
    records["base_raw_maximum_absolute_coordinate"] = Q(1)
    q = lambda z: interval_add(
        (z * z, z * z), interval_add(
            interval_scale(interval_add(interval_scale(alpha, 3), (Q(2), Q(2))), z),
            interval_scale(interval_square(interval_add(alpha, (Q(1), Q(1)))), Q(-3, 2))))
    negative, positive = (Q(-3, 50), Q(-1, 25)), (Q(3, 5), Q(63, 100))
    require(q(negative[0])[0] > 0 and q(negative[1])[1] < 0
            and q(positive[0])[1] < 0 and q(positive[1])[0] > 0,
            "both distinct active root brackets")
    all_brackets = [alpha, negative, positive, (Q(1), Q(1))]
    gaps = [all_brackets[j][0] - all_brackets[i][1]
            for i in range(4) for j in range(i + 1, 4)]
    require(min(gaps) > Q(1, 4), "active contour separation")
    records["full_base_spectral_brackets"] = {
        "inactive_rank3": alpha, "active_minus": negative,
        "active_plus": positive, "inactive_rank2": [Q(1), Q(1)],
        "all_distinct_cluster_gaps": gaps, "contour_radius": Q(1, 8)}
    # Whole identity, not evaluations, for the imported stationary curve.
    lhs = add(mul(derivative(FNUM), DPOLY),
              scale(mul(FNUM, derivative(DPOLY)), -1))
    rhs = scale(mul(mul([Q(-1), Q(1)], [Q(3), Q(5)]), QPOLY), 16)
    require(lhs == rhs, "entire stationary factor identity")
    records["stationary_numerator_identity"] = lhs
    common = interval_mul(interval_add(alpha, (Q(1), Q(1))),
                          interval_square(interval_poly(DPOLY, alpha)))
    lambda4 = interval_div(interval_scale(
        interval_mul(n0, interval_poly(A7, alpha)), Q(-2, 3)), common)
    lambda3 = interval_div(interval_scale(
        interval_mul(n0, interval_poly(B7, alpha)), Q(-2, 9)), common)
    second_numerator = mul(mul([Q(-1), Q(1)], [Q(3), Q(5)]),
                           derivative(QPOLY))
    fsecond = interval_div(interval_scale(interval_poly(second_numerator, alpha), 16),
                           interval_square(interval_poly(DPOLY, alpha)))
    lambda0 = interval_scale(interval_mul(interval_square(n0), fsecond), Q(-1, 192))
    require(all(box[0] > 340 for box in [lambda4, lambda3, lambda0]),
            "all three inherited normalized quadratic costs exceed 340")
    records["normalized_costs_from_8806"] = {
        "fourfold_dimension3": outward_dyadic(lambda4),
        "threefold_dimension2": outward_dyadic(lambda3),
        "block_constant_dimension1": outward_dyadic(lambda0)}
    cbox = outward_dyadic(interval_div(interval_poly(FNUM, alpha), interval_poly(DPOLY, alpha)))
    records["c3_interval"] = cbox
    validate_domain()
    # Independent formal recurrence reconstructs the first four coefficients.
    dp = [Q(1, 2), Q(-2), Q(-5), Q(-4), Q(-1)]
    inv = [Q(2)]
    for j in range(1, 4):
        inv.append(-sum(dp[i] * inv[j - i]
                        for i in range(1, min(4, j) + 1)) / dp[0])
    mass4 = [2 * Q(comb(4, j)) * Q(5, 2) ** (4 - j) for j in range(5)]
    numerator = [sum(mass4[i] * (j - i + 1) * 8 ** (j - i)
                     for i in range(min(j, 4) + 1))
                 + {0: Q(625, 16), 2: Q(25, 2), 4: Q(1)}.get(j, Q(0))
                 for j in range(4)]
    series = [sum(numerator[i] * inv[j - i] for i in range(j + 1))
              for j in range(4)]
    require(series == [Q(1875, 8), Q(7375, 2), Q(205075, 4), Q(614265)],
            "entire low-degree majorant recurrence")
    records["majorant_first_four_coefficients"] = series
    require(Q(1, 2) - 2 * Q(1, 8) - 5 * Q(1, 8) ** 2
            - 4 * Q(1, 8) ** 3 - Q(1, 8) ** 4 == Q(671, 4096),
            "whole comparison denominator boundary")
    require(tail(Q(1, 100000)) < 614333, "sharper literal tail evaluation")
    records["majorant_tail_at_raw_endpoint"] = tail(Q(1, 100000))
    records["uniform_remainder_constant"] = Q(620000)
    records["raw_normalized_cost_margin_over_300"] = (
        340 - Q(620000) * Q(25, 4) / 100000 - 300)
    require(mul(power([Q(-1), Q(1)], 2), [Q(2), Q(1)])
            == [Q(2), Q(-3), Q(0), Q(1)], "whole chord-to-tangent identity")
    records["chord_identity"] = [Q(2), Q(-3), Q(0), Q(1)]
    damages = {}
    for name, args in [
        ("remainder_ten_times_too_small", {"remainder": Q(62000)}),
        ("larger_unit_ball_not_certified", {"unit_radius": Q(1, 100000)}),
        ("larger_raw_ball_not_certified", {"raw_radius": Q(1, 10000)}),
        ("coefficient340_not_certified_by_this_tail", {"coefficient": Q(340)})]:
        try:
            validate_domain(**args)
        except ValueError as exc:
            damages[name] = str(exc)
        else:
            raise ValueError("damaged certificate accepted: " + name)
    records["four_mathematical_damage_rejections"] = damages
    a = Q(-853410556973737, 10 ** 15)
    base = [a] * 4 + [Q(1)] * 3 + [-4 * a - 3]
    controls = [
        ("three_level_near_base", [0, 0, 0, 0, 0, 0, 0, 0]),
        ("five_level_negative_pair", [-1, 1, 0, 0, 0, 0, 0, 0]),
        ("five_level_positive_pair", [0, 0, 0, 0, -1, 1, 0, 0]),
        ("six_level_two_internal_splits", [-1, -1, 0, 2, -1, -1, 2, 0]),
        ("seven_level_four_and_two", [-3, -1, 1, 3, -1, -1, 2, 0]),
        ("eight_level_four_and_three", [-3, -1, 1, 3, -1, 0, 1, 0])]
    for name, perturbation in controls:
        u = [x + Q(y, 10 ** 7) for x, y in zip(base, perturbation)]
        records["witness_" + name] = witness(name, u, alpha, cbox)
    return encoded(records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected", type=Path)
    parser.add_argument("--write-expected", type=Path)
    args = parser.parse_args()
    started = time.perf_counter()
    records = verify()
    payload = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(payload).hexdigest()
    if args.write_expected:
        args.write_expected.write_text(json.dumps(records, sort_keys=True, indent=2) + "\n")
    if args.expected:
        require(records == json.loads(args.expected.read_text()),
                "entire external fixture differs or contains omitted/additional fields")
    print(json.dumps({"status": "PASS", "records": len(records),
                      "full_compression_and_secular_witnesses": 6,
                      "mathematical_damages_rejected": 4,
                      "unit_radius": "1/250000", "coefficient": 300,
                      "raw_third_order_constant": 620000,
                      "record_sha256": digest,
                      "elapsed_seconds": round(time.perf_counter() - started, 6),
                      "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__ == "__main__":
    main()
