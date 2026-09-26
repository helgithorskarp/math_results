#!/usr/bin/env python3
"""Separate replay via rational polynomial inequalities.

This reads no certificate and imports no primary checker. Square roots are
eliminated by squaring positive expressions. The wider root bracket, lower
Taylor degree, and coarser pi interval leave ample slack. It is a second
author implementation, not independent mathematical acceptance.
"""

from fractions import Fraction as F
from hashlib import sha256
import json
from math import factorial


def check(condition, label):
    if not condition:
        raise ValueError(label)


def exp_poly(x, n):
    return sum(((-x) ** j / factorial(j) for j in range(n + 1)), F(0))


def integrated_poly(x, n):
    return sum(((-x) ** j / (factorial(j) * (2 * j + 3))
                for j in range(n + 1)), F(0))


def atan_poly(x, n):
    return sum(((-1) ** j * x ** (2 * j + 1) / (2 * j + 1)
                for j in range(n + 1)), F(0))


def main():
    q, w, c = F(17, 50), F(57, 50), F(7, 50)
    left, right = F(533, 625), F(853, 1000)
    pi_lo, pi_hi = F(314159, 100000), F(3927, 1250)
    check(w - 1 == c, "infinite endpoint")
    mach_lo = 16 * atan_poly(F(1, 5), 7) - 4 * atan_poly(F(1, 239), 6)
    mach_hi = 16 * atan_poly(F(1, 5), 6) - 4 * atan_poly(F(1, 239), 7)
    check(pi_lo < mach_lo < mach_hi < pi_hi, "coarse pi enclosure")

    # Positive derivative at left and negative derivative at right.
    dl = pi_lo - 4 * w * w * exp_poly(2 * q, 8) * (left + q)
    dr = 4 * w * w * exp_poly(2 * q, 9) * (right + q) - pi_hi
    check(dl > 0 and dr > 0, "wide critical bracket")

    # w F(q) < c, after eliminating sqrt(q/pi) by squaring.
    uq = integrated_poly(q, 8)
    check(uq > 0, "positive CDF upper factor")
    zero_margin = c * c * pi_lo - 16 * w * w * q ** 3 * uq * uq
    check(zero_margin > 0, "finite endpoint lower envelope")

    # h(right) < w F(left+q), using a lower CDF Taylor bound.
    x = left + q
    lower_cdf_factor = integrated_poly(x, 9)
    upper_hinge = 1 - exp_poly(right, 9)
    check(lower_cdf_factor > 0 and upper_hinge > 0, "positive peak factors")
    peak_margin = (16 * w * w * x ** 3 * lower_cdf_factor ** 2
                   - pi_hi * upper_hinge ** 2)
    check(peak_margin > 0, "global upper envelope")

    record = {
        "status": "SEPARATE_POLYNOMIAL_ENVELOPE_PASS",
        "shift": str(q), "multiplier": str(w), "error": str(c),
        "wide_critical_bracket": [str(left), str(right)],
        "coarse_pi_interval": [str(pi_lo), str(pi_hi)],
        "positive_rational_margins": {
            "left_derivative": str(dl), "right_derivative": str(dr),
            "finite_endpoint": str(zero_margin), "critical_maximum": str(peak_margin)
        }
    }
    encoded = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    print(json.dumps({"record": record, "record_sha256": sha256(encoded).hexdigest()},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
