#!/usr/bin/env python3
"""Exact finite controls, not a verifier of the analytic contact theorem.

Standard library only. Gaussian moments are expanded from independent
increments, rather than supplied through a covariance formula. No simulation.
"""

import argparse
import json
from fractions import Fraction as F
from math import comb, prod
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def clean(p):
    return {e: c for e, c in p.items() if c}


def add(*polys):
    out = {}
    for p in polys:
        for e, c in p.items():
            out[e] = out.get(e, F(0)) + c
    return clean(out)


def scale(p, c):
    return clean({e: c * v for e, v in p.items()})


def mul(p, q):
    out = {}
    for e, a in p.items():
        for f, b in q.items():
            ef = tuple(x + y for x, y in zip(e, f))
            out[ef] = out.get(ef, F(0)) + a * b
    return clean(out)


def monomial(n, variable=None, power=1):
    e = [0] * n
    if variable is not None:
        e[variable] = power
    return {tuple(e): F(1)}


def gaussian_moment(k):
    if k % 2:
        return 0
    return prod(range(1, k, 2))


def expectation(p, increments_only=False):
    """Variables: three W_s coordinates, three increments, formal s.

    Independent coordinate variances are s and 1-s. Output remains a
    polynomial in the same seven variables, possibly with only s left.
    """
    out = {}
    for e, coeff in p.items():
        first = 3 if increments_only else 0
        powers = e[first:6]
        if any(k % 2 for k in powers):
            continue
        factor = coeff * prod(gaussian_moment(k) for k in powers)
        base = list(e)
        for j in range(first, 6):
            base[j] = 0
        old_power = 0 if increments_only else sum(e[:3]) // 2
        new_power = sum(e[3:6]) // 2
        for k in range(new_power + 1):
            term = base.copy()
            term[6] += old_power + k
            key = tuple(term)
            out[key] = out.get(key, F(0)) + factor * comb(new_power, k) * (-1) ** k
    return clean(out)


def univariate(p):
    require(all(not any(e[:6]) for e in p), "unexpected unaveraged variables")
    return {str(e[6]): str(c) for e, c in sorted(p.items())}


def rejection_check(actual, false_expected):
    try:
        require(actual == false_expected, "deliberately false certificate")
    except ValueError:
        return 1
    raise ValueError("corrupted certificate was accepted")


def audit():
    one = monomial(7)
    s = monomial(7, 6)
    s2 = mul(s, s)
    xs = [monomial(7, i) for i in range(3)]
    ys = [monomial(7, i + 3) for i in range(3)]
    ns = add(*(mul(x, x) for x in xs), scale(s, -3))
    n1 = add(*(mul(add(x, y), add(x, y)) for x, y in zip(xs, ys)), scale(one, -3))
    increment = add(n1, scale(ns, -1))
    moment_checks = {
        "mean_Ns": (expectation(ns), {}),
        "mean_increment": (expectation(increment), {}),
        "variance_Ns": (expectation(mul(ns, ns)), scale(s2, 6)),
        "variance_increment": (expectation(mul(increment, increment)), add(scale(one, 6), scale(s2, -6))),
        "covariance_Ns_increment": (expectation(mul(ns, increment)), {}),
        "variance_N1": (expectation(mul(n1, n1)), scale(one, 6)),
    }
    for name, (actual, expected) in moment_checks.items():
        require(actual == expected, name)
    require(expectation(n1, increments_only=True) == ns, "conditional martingale identity")
    variance_increment = moment_checks["variance_increment"][0]
    slack = add(scale(add(one, scale(s, -1)), 12), scale(variance_increment, -1))
    require(slack == scale(mul(add(one, scale(s, -1)), add(one, scale(s, -1))), 6), "variance upper-bound slack")

    # Independent scalar derivation of the chosen-time remainder:
    # 6[1-(1-k^2/48)^2] = k^2/4-k^4/384.
    one_k = monomial(1)
    k2 = monomial(1, 0, 2)
    k4 = monomial(1, 0, 4)
    chosen_s = add(one_k, scale(k2, -F(1, 48)))
    chosen_variance = scale(add(one_k, scale(mul(chosen_s, chosen_s), -1)), 6)
    require(chosen_variance == add(scale(k2, F(1, 4)), scale(k4, -F(1, 384))), "chosen-time variance")

    # Expand w^2=(A-B)^2/2 against sign(A_1)sign(B_1).
    # Even powers vanish by symmetry; E[A_s sign(A_1)]=s*m,
    # m=E|A_1|. The written Gaussian integral gives m^2=2/pi.
    a = monomial(2, 0)
    b = monomial(2, 1)
    w_squared = scale(mul(add(a, scale(b, -1)), add(a, scale(b, -1))), F(1, 2))
    sign_coefficient = F(0)
    for e, c in w_squared.items():
        if all(power % 2 for power in e):
            require(e == (1, 1), "unexpected signed moment")
            sign_coefficient += c
    require(sign_coefficient == -1, "orientation of signed Gaussian control")
    control_coefficient = 2 * sign_coefficient
    require(control_coefficient == -2, "coefficient of s^2/pi")

    # Rational constants used in the first-hit, signed-event and tail bounds.
    require(6 < 4**2 and 48 < 7**2, "square-root majorants")
    require(F(4, 16) == F(1, 4), "first-hit threshold allowance")
    require(16 * 6 == 96, "one-sided Cauchy--Schwarz denominator")
    require(F(8, 1536) == F(1, 192), "six-dimensional tail allocation")
    require(F(1, 96) - F(1, 192) == F(1, 192), "retained event probability")
    require((F(47, 48)) ** 2 > F(1, 2), "control covariance at selected time")
    kappa = F(7, 11)  # 3<pi<22/7 gives kappa<2/pi<2/3.
    time = 1 - kappa**2 / 48
    theta = kappa / 16
    require(0 < kappa <= 1 and 0 < time < 1, "nonvacuous parameter control")
    require(6 * (1 - time**2) <= kappa**2 / 4, "control remainder")
    require(kappa * time**2 > kappa / 2, "negative preterminal control")

    rejected = 0
    rejected += rejection_check(moment_checks["variance_Ns"][0], scale(s2, 3))
    rejected += rejection_check(variance_increment, scale(add(one, scale(s, -1)), 6))
    rejected += rejection_check(control_coefficient, 2)
    rejected += rejection_check(F(8, 1536), F(1, 384))
    require(rejected == 4, "corruption checks")

    return {
        "status": "EXACT_CONTACT_CONTROLS_PASS",
        "analytic_proof_checked_by_code": False,
        "full_majorisation_proved": False,
        "gaussian_moment_identities": {name: univariate(actual) for name, (actual, _) in moment_checks.items()},
        "conditional_martingale_identity": True,
        "variance_slack_polynomial_in_s": univariate(slack),
        "chosen_time_variance_polynomial_in_kappa": {str(e[0]): str(c) for e, c in sorted(chosen_variance.items())},
        "signed_control_coefficient_of_s_squared_over_pi": str(control_coefficient),
        "rational_control": {
            "kappa": str(kappa),
            "time": str(time),
            "threshold": str(theta),
            "event_probability_lower_bound": str(kappa**2 / 96),
            "bounded_state_probability_lower_bound": str(kappa**2 / 192),
        },
        "corruptions_rejected": rejected,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="emit exact controls without reading EXPECTED.json")
    args = parser.parse_args()
    result = audit()
    if not args.emit:
        expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
        require(result == expected, "EXPECTED.json mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
