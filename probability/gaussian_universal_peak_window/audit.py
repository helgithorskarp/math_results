#!/usr/bin/env python3
"""Exact arithmetic audit accompanying PROOF.md; not a proof replay.

Python 3.11+, standard library only. No data inputs or output files.
"""

from fractions import Fraction as F
from math import factorial


def stirling_second(n, k):
    if n == k == 0:
        return 1
    if k == 0 or k > n:
        return 0
    return k * stirling_second(n - 1, k) + stirling_second(n - 1, k - 1)


def require(condition):
    if not condition:
        raise AssertionError("Exact arithmetic audit failed")


def main():
    delta = F(1, 2**32)
    eta = 8192 * delta
    e0 = 256 * eta
    eps = 32 * e0
    require(eps == F(1, 64))
    require(eta <= 1 and e0 <= F(1, 4))
    require(9 * 320 < 4096 and 10**5 < 320**2)
    require(32 * delta < F(1, 16))
    print(f"PASS: universal cutoff delta={delta}")

    partition_sums = [
        sum(stirling_second(n, k) * factorial(k - 1) for k in range(1, n + 1))
        for n in range(1, 6)
    ]
    require(partition_sums == [1, 2, 6, 26, 150])
    require(max(partition_sums) < 256)
    print(f"PASS: log-derivative partition sums {partition_sums}")

    q = F(1, 4)
    require((1 + 4 * q + q*q) / (1-q)**4 < 8)
    require(F(1, 2) + 3 * eps / 16 < F(3, 4))
    require(16 + 54 * eps <= 17)
    require(204 + 864 * eps <= 256)
    require(F(5, 2) + 72 <= 75)
    require(6 + 12 + 256 <= 288)
    require(36 + 150 * (1 + eps) <= 192)
    require(36864 * eps**2 + 1728 * eps == 36)
    print("PASS: inverse-chart and Jacobian bounds")
    print("PASS: uniform marked-midpoint Helmholtz bound Lambda<=36")

    # For x<=1 the largest series ratios occur at their first indices.
    require(F(1, 4*1*3) == F(1, 12) < 1)
    require(F(1, 4*1*4) == F(1, 16) < 1)
    b_lower = 1 - F(1, 12)
    log_derivative_lower = -F(1, 6) / b_lower
    require(4 + log_derivative_lower == F(42, 11) > 0)
    require(72 * delta < 1)  # x^2=36r^2<=72delta
    print("PASS: spherical derivative margin >=42/11")

    # Centered Gaussian, constant h=D: C6 A(l)=D*l^2/2.
    # I(l)=4*l^(3/2)/(3*sqrt(pi)); Gamma(5/2)=3*sqrt(pi)/4.
    # The 1/4 factor then gives moments D/[4*k^(5/2)].
    beta_2_half = F(4, 3)
    gamma_five_half_over_sqrt_pi = F(3, 4)
    require(F(1, 4) * beta_2_half * gamma_five_half_over_sqrt_pi == F(1, 4))
    # A(l)~(l-sigma)^2, A'(l)~(l-sigma): both mode values vanish.
    require(6 - 2 == 4 and F(6-2, 2) == 2 and F(6-4, 2) == 1)
    print("PASS: Abel calibration and no mode boundary term")


if __name__ == "__main__":
    main()
