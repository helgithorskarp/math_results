#!/usr/bin/env python3
"""Exact audit of one global shifted-Gamma envelope; standard library only.

The mathematical reduction of an infinite domain to these endpoint and
critical-point inequalities is in PROOF.md. This program uses no floating
point arithmetic, numerical integration, solver, or external certificate.
"""

import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import isqrt
from pathlib import Path


class InvalidCertificate(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidCertificate(message)


def sqrt_bounds(x, bits):
    """Dyadic enclosure, checked by exact squaring."""
    require(x >= 0, "negative radicand")
    scale = 1 << bits
    root = isqrt((x.numerator * scale * scale) // x.denominator)
    lo, hi = Q(root, scale), Q(root + 1, scale)
    require(lo * lo <= x < hi * hi, "sqrt enclosure")
    return lo, hi


def alternating_exp(x, even):
    """Odd/even Taylor bounds for exp(-x), by signed Lagrange remainder."""
    require(x >= 0 and even >= 0 and even % 2 == 0, "exp parameters")
    term = total = Q(1)
    for k in range(1, even + 1):
        term *= -x / k
        total += term
    upper = total
    lower = total + term * (-x) / (even + 1)
    require(0 < lower <= upper, "exp Taylor positivity")
    return lower, upper


def arctan_bounds(x, even):
    """Integrated finite geometric series for 0<x<1."""
    require(0 < x < 1 and even >= 0 and even % 2 == 0, "atan parameters")
    upper = sum(((-1) ** k * x ** (2 * k + 1) / (2 * k + 1)
                 for k in range(even + 1)), Q(0))
    lower = upper - x ** (2 * even + 3) / (2 * even + 3)
    return lower, upper


def pi_bounds(even):
    # Machin's identity: pi = 16 atan(1/5) - 4 atan(1/239).
    u, v = Q(1, 5), Q(1, 239)
    tan2 = 2 * u / (1 - u * u)
    tan4 = 2 * tan2 / (1 - tan2 * tan2)
    require((tan4 - v) / (1 + tan4 * v) == 1, "Machin tangent identity")
    a, b = arctan_bounds(Q(1, 5), even), arctan_bounds(Q(1, 239), even)
    return 16 * a[0] - 4 * b[1], 16 * a[1] - 4 * b[0]


def gamma_cdf_bounds(x, pi_interval, even, bits):
    """F_(3/2)(x), integrating the signed exp Taylor bounds exactly."""
    if x <= 0:
        return Q(0), Q(0)
    term = Q(1)
    total = Q(1, 3)
    for k in range(1, even + 1):
        term *= -x / k
        total += term / (2 * k + 3)
    lower_series = total + term * (-x) / ((even + 1) * (2 * even + 5))
    require(0 < lower_series <= total, "integrated Taylor positivity")
    sx = sqrt_bounds(x, bits)
    sp_lo = sqrt_bounds(pi_interval[0], bits)[0]
    sp_hi = sqrt_bounds(pi_interval[1], bits)[1]
    lo = 4 * x * sx[0] * lower_series / sp_hi
    hi = 4 * x * sx[1] * total / sp_lo
    require(0 <= lo <= hi <= 1, "Gamma enclosure range")
    return lo, hi


def rational_pair(value):
    require(isinstance(value, list) and len(value) == 2, "interval format")
    lo, hi = map(Q, value)
    require(lo <= hi, "interval orientation")
    return lo, hi


def contained(actual, claimed, label):
    lo, hi = rational_pair(claimed)
    require(lo <= actual[0] <= actual[1] <= hi, label + " enclosure claim")


def audit(data):
    require(data.get("schema") == "shifted-gamma-envelope-v1", "schema")
    q, w, error = (Q(data[k]) for k in ("shift", "multiplier", "error"))
    require(q > 0 and w > 1 and error == w - 1, "envelope parameters")
    tlo, thi = rational_pair(data["critical_bracket"])
    require(0 < tlo < thi, "positive critical bracket")
    even, atan_even, bits = (data[k] for k in
                            ("even_taylor_degree", "even_arctan_index", "sqrt_bits"))
    require(all(type(v) is int for v in (even, atan_even, bits)), "integer precision")
    require(2 <= even <= 200 and even % 2 == 0, "Taylor degree")
    require(2 <= atan_even <= 200 and atan_even % 2 == 0, "atan degree")
    require(16 <= bits <= 1000, "sqrt precision")
    pi = pi_bounds(atan_even)
    require(3 < pi[0] <= pi[1] < 4, "pi range")
    contained(pi, data["claims"]["pi"], "pi")

    # d'(t) has the sign of 1 - (2w exp(-q)/sqrt(pi))*sqrt(t+q).
    # Squaring positive quantities gives the following two strict signs.
    exp2q = alternating_exp(2 * q, even)
    derivative_at_lo = w * w * exp2q[1] * (tlo + q) - pi[0] / 4
    derivative_at_hi = w * w * exp2q[0] * (thi + q) - pi[1] / 4
    require(derivative_at_lo < 0 < derivative_at_hi, "critical root isolation")

    fq = gamma_cdf_bounds(q, pi, even, bits)
    d0 = -w * fq[1], -w * fq[0]
    require(-error < d0[0] <= d0[1] < 0, "negative-side lower envelope")
    contained(d0, data["claims"]["d_zero"], "d(0)")

    # h and F are increasing: evaluate opposite ends to enclose d(t*)
    # throughout the isolated root interval. No sampling is involved.
    flo = gamma_cdf_bounds(tlo + q, pi, even, bits)
    fhi = gamma_cdf_bounds(thi + q, pi, even, bits)
    elo, ehi = alternating_exp(tlo, even), alternating_exp(thi, even)
    peak = 1 - elo[1] - w * fhi[1], 1 - ehi[0] - w * flo[0]
    require(peak[1] < 0, "positive-side upper envelope")
    contained(peak, data["claims"]["critical_value"], "critical value")

    # Only validated outward rational claims enter this short canonical record.
    return {
        "status": "UNIFORM_GAUSSIAN_DEFECT_BOUND_PASS",
        "schema": data["schema"],
        "shift": str(q),
        "multiplier": str(w),
        "error": str(error),
        "critical_bracket": [str(tlo), str(thi)],
        "verified_enclosures": data["claims"],
        "critical_derivative_signs": ["positive", "negative"],
        "global_envelope": [str(-error), "0"],
        "global_defect_upper_bound": str(error),
        "trust": "written global reduction + exact Python rational arithmetic; not independent acceptance"
    }


def canonical_record(record):
    raw = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    return {"record": record, "record_sha256": sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path,
                        default=Path(__file__).with_name("CERTIFICATE.json"))
    args = parser.parse_args()
    print(json.dumps(canonical_record(audit(json.loads(args.certificate.read_text()))),
                     sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
