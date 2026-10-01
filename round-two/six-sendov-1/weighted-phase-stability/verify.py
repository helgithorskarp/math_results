#!/usr/bin/env python3
"""Exact finite checks for the degree-nine weighted-phase stability proof.

Standard-library Python 3.10+. The logarithm/product/complex-segment arguments
remain ordinary written proof. --emit explicitly writes expected.json;
default invocation is read-only. Inherited lemmas are not rebuilt here.
"""
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from math import comb
from pathlib import Path
import argparse
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def clean(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(p, q):
    out = [F(0)] * max(len(p), len(q))
    for source in [p, q]:
        for i, value in enumerate(source):
            out[i] += value
    return clean(out)


def scale(p, c):
    return clean([c * value for value in p])


def mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, value in enumerate(p):
        for j, other in enumerate(q):
            out[i + j] += value * other
    return clean(out)


def power(p, n):
    out = [F(1)]
    for _ in range(n):
        out = mul(out, p)
    return out


def evaluate(p, x):
    out = F(0)
    for value in reversed(p):
        out = out * x + value
    return out


def derivative(p):
    return clean([i * p[i] for i in range(1, len(p))] or [F(0)])


def affine(p, lo, hi):
    degree = len(p) - 1
    return clean([sum(p[k] * comb(k, j) * lo**(k-j) * (hi-lo)**j
                      for k in range(j, degree+1)) for j in range(degree+1)])


def bernstein(p, degree):
    return [sum(p[k] * F(comb(i, k), comb(degree, k))
                for k in range(min(i, len(p)-1)+1)) for i in range(degree+1)]


def inverse(controls):
    degree = len(controls) - 1
    out = [F(0)]
    for i, value in enumerate(controls):
        basis = [F(0)] * i + [F(comb(degree, i))]
        basis = mul(basis, power([F(1), F(-1)], degree-i))
        out = add(out, scale(basis, value))
    return out


def midpoint(controls):
    rows = [controls]
    while len(rows[-1]) > 1:
        row = rows[-1]
        rows.append([(row[i]+row[i+1])/2 for i in range(len(row)-1)])
    return [row[0] for row in rows], [row[-1] for row in reversed(rows)]


def integral_bound_polynomial(factors, t_weight, a_weight):
    convolution = power([F(1), F(-1, 2)], factors)
    route1 = [F(0)] * a_weight + [9 * c / (k+t_weight+1)
                                                 for k, c in enumerate(convolution)]
    route2 = [F(0)] * a_weight + [F(9*comb(factors, k), k+t_weight+1)
                                * F(-1, 2)**k for k in range(factors+1)]
    need(route1 == route2, "complete integral coefficient routes")
    return clean(route1)


def generate():
    # A nonnegative cubic identity for e^s - [(16/5)s - 1].
    q = [F(2), F(-11, 5), F(1, 2), F(1, 6)]
    rhs = add(scale(power([F(-71, 50), F(1)], 2), F(5, 6)), [F(959, 3000)])
    rhs = add(rhs, scale(mul([F(0), F(1)], power([F(-1), F(1)], 2)), F(1, 6)))
    need(q == rhs, "full cubic positive identity")
    denominator = add(mul([F(1), F(-1)], [F(1), F(1, 2)]), [F(-5, 8)])
    need(denominator == mul([F(1, 2), F(-1)], [F(3, 4), F(1, 2)]),
         "full logarithmic ratio denominator identity")
    f = integral_bound_polynomial(3, 1, 1)
    g = integral_bound_polynomial(2, 2, 2)
    need(f == [F(0), F(9, 2), F(-9, 2), F(27, 16), F(-9, 40)], "f polynomial")
    need(g == [F(0), F(0), F(3), F(-9, 4), F(9, 20)], "g polynomial")
    gap = add([F(3, 2)], scale(f, -1))
    global_controls = bernstein(gap, 4)
    left, right = midpoint(global_controls)
    middle, last = midpoint(right)
    intervals = [(F(0), F(1, 2)), (F(1, 2), F(3, 4)), (F(3, 4), F(1))]
    records = []
    for (lo, hi), direct in zip(intervals, [left, middle, last]):
        local = affine(gap, lo, hi)
        controls = bernstein(local, 4)
        need(controls == direct, "power and de Casteljau coefficient routes")
        need(inverse(controls) == local, "full local inverse")
        need(min(controls) > 0, "negative/zero f-gap control")
        records.append({"interval": [str(lo), str(hi)],
                        "coefficients": [str(x) for x in controls],
                        "minimum": str(min(controls))})
    derivative_rhs = scale(mul([F(0), F(1)],
                               add([F(7)], mul([F(1), F(-1)], [F(33), F(-12)]))), F(3, 20))
    need(derivative(g) == derivative_rhs, "full positive g derivative factorization")
    need(evaluate(g, 1) == F(6, 5), "g endpoint")
    gamma, delta = F(1, 10**6), F(1, 10**7)
    cap = (1+24*gamma+37500*gamma**2)/(1-30*gamma)
    e2_lower = 28*(1-3*gamma)**2-16*cap
    spread_lower = F(1, 2048)-(F(288, 5)+F(1, 1024))*delta
    radius_gap = F(17, 1024)*spread_lower
    phase_upper = F(17712, 245)*delta
    comparisons = {
        "sos_floor_positive": F(959, 3000) > 0,
        "logarithmic_ratio_cap": F(2) / F(5, 8) == F(16, 5),
        "Hessian_cap": F(6, 5)/(1-2*F(1, 100)) == F(60, 49),
        "phase_coupling": (F(3, 2)+F(480, 49))*F(32, 5) == F(17712, 245),
        "unweighted_small_phase": F(3, 2)+F(30, 49) == F(207, 98),
        "signed_phase_margin": F(9, 32)-F(1107, 98*41) == F(369, 64288) > 0,
        "e2_floor": e2_lower > F(119, 10),
        "Newton_penalty": F(119, 10)/14 == F(17, 20),
        "radius_gap_coefficient": 5*F(17, 20)/256 == F(17, 1024),
        "spread_positive": spread_lower > 0,
        "collar_gap_positive": radius_gap > phase_upper,
        "epsilon_cap": F(512, 5)*delta < F(1, 100)**2,
        "inherited_tube_collar": 1-delta >= F(511, 512),
        "inherited_variance_collar": delta <= gamma,
    }
    for name, condition in comparisons.items():
        need(condition, "finite comparison " + name)
    return {
        "status": "ordinary author proof: exact finite certificate",
        "SOS_cubic": [str(x) for x in q],
        "log_denominator": [str(x) for x in denominator],
        "f": [str(x) for x in f], "g": [str(x) for x in g],
        "f_gap_bernstein_cells": records,
        "constants": {"gamma": str(gamma), "delta": str(delta),
                      "variance_cap": str(cap), "e2_lower": str(e2_lower),
                      "spread_lower": str(spread_lower), "radius_gap_lower": str(radius_gap),
                      "phase_upper": str(phase_upper), "annulus_slack": str(radius_gap-phase_upper)},
        "summary": {"full_integral_routes": 2, "SOS_coefficients": 4,
                    "f_gap_coefficients": 15, "inverse_cells": 3,
                    "finite_comparisons": len(comparisons)},
    }


def check_fixture(fixture, actual):
    need(fixture == actual, "fixture differs from complete exact regeneration")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    path = Path(__file__).with_name("expected.json")
    actual = generate()
    if args.emit:
        path.write_text(json.dumps(actual, indent=2)+"\n")
    fixture = json.loads(path.read_text())
    check_fixture(fixture, actual)
    mutations = []
    for key in ["f", "g", "SOS_cubic"]:
        damage = deepcopy(actual)
        damage[key][1] = "999"
        mutations.append(damage)
    damage = deepcopy(actual)
    damage["f_gap_bernstein_cells"][1]["coefficients"][2] = "-1"
    mutations.append(damage)
    damage = deepcopy(actual)
    damage["constants"]["annulus_slack"] = "0"
    mutations.append(damage)
    for damage in mutations:
        try:
            check_fixture(damage, actual)
        except ValueError:
            continue
        raise ValueError("corruption accepted")
    canonical = json.dumps(actual, sort_keys=True, separators=(",", ":")).encode()
    print(json.dumps({"status": "PASS: weighted phase finite checks",
                      **actual["summary"], "rejected_corruptions": len(mutations),
                      "canonical_sha256": sha256(canonical).hexdigest(),
                      "annulus_slack": actual["constants"]["annulus_slack"]}, sort_keys=True))


if __name__ == "__main__":
    main()
