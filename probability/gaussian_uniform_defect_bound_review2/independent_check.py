#!/usr/bin/env python3
"""Independent exact certificate for the shifted-Gamma envelope.

This checker imports no reviewed code or certificate.  It uses a different
critical-point reduction: the Gamma(3/2) closed form turns the value at the
unique critical point into 1-w*erf(sqrt(x_star)).  Low-degree rational Taylor
bounds then prove the two finite inequalities needed for the global envelope.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from math import factorial
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def alternating_atan_bounds(x, even):
    require(0 < x < 1 and even % 2 == 0, "arctangent parameters")
    upper = sum(((-1) ** j * x ** (2 * j + 1) / (2 * j + 1)
                 for j in range(even + 1)), F(0))
    lower = upper - x ** (2 * even + 3) / (2 * even + 3)
    return lower, upper


def build_record():
    q, w, c = F(17, 50), F(57, 50), F(7, 50)
    require(c == w - 1, "infinite-end error")

    # A Machin identity different from the reviewed checker:
    # pi = 8 atan(1/3)+4 atan(1/7).  Indeed tan(2 atan(1/3))=3/4,
    # and adding atan(1/7) gives tangent one in (0,pi/2).
    tan_double = 2 * F(1, 3) / (1 - F(1, 3) ** 2)
    tan_sum = (tan_double + F(1, 7)) / (1 - tan_double * F(1, 7))
    require(tan_double == F(3, 4) and tan_sum == 1, "Machin identity")
    a = alternating_atan_bounds(F(1, 3), 4)
    b = alternating_atan_bounds(F(1, 7), 4)
    pi = 8 * a[0] + 4 * b[0], 8 * a[1] + 4 * b[1]
    pi_lo, pi_hi = F(314159, 100000), F(3927, 1250)
    require(pi_lo < pi[0] < pi[1] < pi_hi, "coarse pi enclosure")

    # At t=0, F_(3/2)(q) is bounded above by integrating the degree-four
    # even Taylor upper bound for exp(-u).  Squaring positive quantities
    # removes both square roots from w F(q)<c.
    gamma_poly = sum(((-q) ** j / (factorial(j) * (2 * j + 3))
                      for j in range(5)), F(0))
    require(gamma_poly > 0, "positive Gamma upper factor")
    finite_endpoint_margin = (
        c * c * pi_lo - 16 * w * w * q ** 3 * gamma_poly ** 2
    )
    require(finite_endpoint_margin > 0, "d(0)>-c")

    # Put x_star=t_star+q=pi*exp(2q)/(4w^2).  A degree-four positive
    # Taylor lower bound for exp(2q) proves x_star>1191/1000.
    x0 = F(1191, 1000)
    exp_lower = sum(((2 * q) ** j / factorial(j) for j in range(5)), F(0))
    critical_location_margin = pi_lo * exp_lower - 4 * w * w * x0
    require(critical_location_margin > 0, "critical-point lower bound")

    # Integration of the degree-seven odd Taylor lower bound for exp(-u^2)
    # gives erf(sqrt(x0)) >= 2 sqrt(x0/pi) E_7(x0).  At the actual critical
    # point the derivative relation cancels the exponential terms exactly:
    # d(t_star)=1-w*erf(sqrt(x_star)).
    erf_poly = sum(((-x0) ** j / (factorial(j) * (2 * j + 1))
                     for j in range(8)), F(0))
    require(erf_poly > 0, "positive erf lower factor")
    critical_value_margin = 4 * w * w * x0 * erf_poly ** 2 - pi_hi
    require(critical_value_margin > 0, "critical maximum below zero")

    record = {
        "status": "INDEPENDENT_UNIFORM_DEFECT_ENVELOPE_PASS",
        "parameters": {"q": str(q), "w": str(w), "c": str(c)},
        "coarse_pi_interval": [str(pi_lo), str(pi_hi)],
        "critical_x_lower_bound": str(x0),
        "exact_positive_margins": {
            "finite_endpoint": str(finite_endpoint_margin),
            "critical_location": str(critical_location_margin),
            "critical_value": str(critical_value_margin),
        },
        "critical_identity": "d(t_star)=1-w*erf(sqrt(t_star+q))",
        "global_envelope": [str(-c), "0"],
        "scope": (
            "Independent scalar-envelope certificate only; the stochastic "
            "density-value transfer remains a written analytic obligation."
        ),
        "zero_defect_verified": False,
    }
    raw = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    return {"record": record, "record_sha256": sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    rendered = json.dumps(build_record(), indent=2, sort_keys=True) + "\n"
    if args.emit:
        print(rendered, end="")
        return
    expected = (HERE / "EXPECTED.json").read_text(encoding="utf-8")
    require(rendered == expected, "EXPECTED.json differs from recomputation")
    print("INDEPENDENT_UNIFORM_DEFECT_ENVELOPE_PASS")


if __name__ == "__main__":
    main()
