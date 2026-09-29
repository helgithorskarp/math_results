#!/usr/bin/env python3
"""Exact algebra and constants for PROOF.md; no universal sampling claim.

Python 3.11+, standard library only. All numerical quantities are Fraction.
The written Taylor, Schur, and compactness arguments are trust boundaries.
"""

from fractions import Fraction as F
from math import comb


class Checks:
    def __init__(self):
        self.count = 0

    def require(self, condition, name):
        if not condition:
            raise AssertionError(name)
        self.count += 1


def add(p, q):
    """Sparse bivariate polynomials over Q, indexed by exponent pairs."""
    result = p.copy()
    for monomial, coefficient in q.items():
        result[monomial] = result.get(monomial, F(0)) + coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def scale(p, coefficient):
    return {m: coefficient * c for m, c in p.items() if coefficient * c}


def multiply(p, q):
    result = {}
    for (i, j), c in p.items():
        for (k, ell), d in q.items():
            m = (i + k, j + ell)
            result[m] = result.get(m, F(0)) + c * d
    return {m: c for m, c in result.items() if c}


def polynomial_checks(checks):
    one = {(0, 0): F(1)}
    x = {(1, 0): F(1)}
    y = {(0, 1): F(1)}
    x2, y2 = multiply(x, x), multiply(y, y)
    norm2 = add(x2, y2)
    u = add(scale(x, 2), scale(norm2, -1))
    expanded = add(add(one, scale(u, F(1, 2))),
                   scale(multiply(u, u), F(3, 8)))
    quadratic = add(add(one, x),
                    add(x2, scale(y2, F(-1, 2))))
    tail = add(scale(multiply(x, norm2), F(-3, 2)),
               scale(multiply(norm2, norm2), F(3, 8)))
    checks.require(expanded == add(quadratic, tail),
                   "Taylor polynomial and cubic/quartic tail identity")

    # The Schur/Taylor combination is an exact symbolic identity in X,Y.
    schur_quadratic = add(scale(x, F(-4, 7)), scale(y, F(4, 7)))
    taylor_quadratic = add(x, scale(y, F(-1, 2)))
    checks.require(add(schur_quadratic, taylor_quadratic)
                   == add(scale(x, F(3, 7)), scale(y, F(1, 14))),
                   "positive quadratic identity")

    # Recover integration weights from the derivative independently of
    # the displayed integer list in the coefficient bound.
    recovered = [F(9 * comb(8, k), 9 - k) for k in range(2, 9)]
    checks.require(recovered == list(map(F, [36, 84, 126, 126, 84, 36, 9])),
                   "integrated symmetric-coefficient weights")
    for k in range(2, 9):
        multiplicity = F(comb(6, k - 2), comb(k, 2)) * F(7, 2)
        checks.require(multiplicity == F(comb(8, k), 8),
                       f"pair-counting identity k={k}")

    # Directly expand a rational critical multiset, integrate, and
    # compare its top two coefficients with the moment formulas.
    critical = [F(k, 100000) for k in [-4, -3, -2, -1, 0, 1, 2, 5]]
    derivative = [F(9)]  # ascending powers after repeated multiplication
    for z in critical:
        new = [F(0)] * (len(derivative) + 1)
        for i, c in enumerate(derivative):
            new[i] -= z * c
            new[i + 1] += c
        derivative = new
    integrated = [F(0)] + [c / (i + 1) for i, c in enumerate(derivative)]
    moment1 = sum(critical, F(0))
    moment2 = sum((z * z for z in critical), F(0))
    checks.require(integrated[9] == 1, "monic coefficient after integration")
    checks.require(integrated[8] == F(-9, 8) * moment1,
                   "first moment coefficient")
    checks.require(integrated[7] == F(9, 14) * (moment1**2 - moment2),
                   "second moment coefficient")
    for i in range(9):
        checks.require((i + 1) * integrated[i + 1] == derivative[i],
                       f"derivative recovery coefficient {i}")


def constant_checks(checks):
    t = F(1, 100)
    inva = F(4, 3)
    ucap = 2 * inva * t + inva**2 * t**2
    checks.require(ucap < F(1, 10), "Taylor parameter domain")
    checks.require(F(5, 16) * F(10, 9)**4 < 1,
                   "third-order Taylor remainder coefficient")
    checks.require(2 + inva * t < 3, "u bounded by three times normalized norm")
    remainder = (27 + F(3, 2)) * inva**4 + F(3, 8) * inva**5 * t
    checks.require(remainder == F(182432, 2025), "exact Taylor error constant")
    checks.require(remainder < 100, "rounded Taylor error constant")
    checks.require(inva**3 / 2 + 100 * t < 4,
                   "coarse first-order lower bound")
    checks.require(inva**2 < 2, "inverse square bound")
    checks.require(2 + 4 * t <= 3, "eta bounded by three T")

    high = sum((F(w, 8) * t**k
                for k, w in enumerate([84, 126, 126, 84, 36, 9])), F(0))
    checks.require(high == F(852726843609, 80000000000),
                   "exact low-degree coefficient factor")
    checks.require(high < 13, "low-degree coefficient bound")
    checks.require(F(9, 8) * t**5 < 2, "linear coefficient bound")

    checks.require(27 + 168 * t < 29, "Z-c-b first moment coefficient")
    checks.require(21 + 13 == 34, "Z-c-b energy coefficient")
    checks.require(F(243, 8) + 216 * t < 33,
                   "a9 replacement first moment coefficient")
    checks.require(27 * (1 + 13 * t) < 31,
                   "a9 replacement energy coefficient")
    checks.require(29 + 33 == 62, "combined replacement first moment")
    checks.require(34 + 31 == 65, "combined replacement energy")
    checks.require(124 + F(72, 7) < 135, "constant-term square moment bound")

    checks.require(F(9, 8) / 18 == F(1, 16), "Schur first-moment gain")
    checks.require(F(144, 18) == 8, "Schur eta coefficient")
    checks.require(F(72, 7) / 18 == F(4, 7), "Schur quadratic coefficient")
    checks.require(F(1080, 18) == 60, "Schur error first moment")
    checks.require(F(1042, 18) == F(521, 9) < 58, "Schur error energy")

    # (a^-k - 1)/(1-a) = (1+a+...+a^(k-1))/a^k is decreasing on
    # (0,1]; its maximum on [3/4,1] is the exact value used here.
    a = F(3, 4)
    checks.require((1 + a) / a**2 < 4, "inverse-square comparison")
    checks.require((1 + a + a*a) / a**3 < 8, "inverse-cube comparison")
    checks.require(4 * 3 == 12, "Taylor first moment comparison error")
    checks.require(8 * 3 + 100 == 124, "Taylor energy comparison error")
    checks.require(60 + 12 == 72, "final first moment error")
    checks.require(58 + 124 == 182, "final energy error")
    checks.require(F(3, 7) > F(1, 14), "quadratic minimum coefficient")


def positivity_margins(t, energy_error=182):
    first = F(1, 16) - 72 * t
    energy = F(1, 14) - energy_error * t
    if first <= 0 or energy <= 0:
        raise AssertionError("nonpositive local-theorem margin")
    return first, energy


def controls(checks):
    threshold = F(1, 10000)
    checks.require(positivity_margins(threshold)
                   == (F(553, 10000), F(1863, 35000)),
                   "exact margins at theorem threshold")
    # Every root of z^9-r^9 has critical distance r. These controls
    # include the boundary equality and two strict interior cases.
    for r in [F(1), F(3, 4), F(1, 2)]:
        total = F(8) / r
        checks.require((total == 8) == (r == 1), f"binomial equality r={r}")
        checks.require(total >= 8, f"binomial lower bound r={r}")
    # For (z-h)^9-r^9, |h|+r<=1 certifies all nine roots in the disk.
    # All critical points are h and every critical distance is r.
    for h, r in [(F(1, 20000), F(19999, 20000)),
                 (F(-1, 20000), F(9, 10))]:
        checks.require(abs(h) <= threshold and abs(h) + r <= 1,
                       "shifted-binomial disk and cluster hypotheses")
        checks.require(F(8) / r > 8, "shifted-binomial strict bound")


def main():
    checks = Checks()
    polynomial_checks(checks)
    constant_checks(checks)
    controls(checks)
    rejected = False
    try:
        positivity_margins(F(1, 10000), energy_error=800)
    except AssertionError:
        rejected = True
    checks.require(rejected, "corrupted positivity margin must be rejected")
    print(f"PASS: {checks.count} exact checks; margin mutation rejected.")


if __name__ == "__main__":
    main()
