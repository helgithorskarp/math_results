"""Exact diagonal section by active-coordinate strata, not hull enumeration."""
from fractions import Fraction as F
from functools import lru_cache
from math import comb, factorial


def monomial_integral(power, lo, hi):
    if hi <= lo:
        return F(0)
    return (F(hi) ** (power + 1) - F(lo) ** (power + 1)) / (power + 1)


def two_sided(a, b, m, s, radius):
    """Unbounded inactive coordinates after inclusion-exclusion.

    Integrate P^(a-1) M^(b-1) (s-P+M)^(m-1) on
    P,M>=0, P+M<=radius, P-M<=s, with factorial denominators.
    """
    top = min(F(radius), F(s))
    if top <= -radius:
        return F(0)
    ans = F(0)
    for i in range(a):
        for j in range(b):
            rp = a + b - 2 - i - j
            vbase = i + j
            coef = comb(a - 1, i) * comb(b - 1, j) * (-1) ** j
            for k in range(m):
                c = F(coef * comb(m - 1, k) * (-1) ** k) * F(s) ** (m - 1 - k)
                vp = vbase + k
                for lo, hi, sign in ((-F(radius), min(top, F(0)), -1),
                                     (F(0), top, 1)):
                    ans += c / (rp + 1) * (
                        F(radius) ** (rp + 1) * monomial_integral(vp, lo, hi)
                        - sign ** (rp + 1) * monomial_integral(vp + rp + 1, lo, hi))
    return ans / (2 ** (a + b - 1) * factorial(a - 1) * factorial(b - 1) * factorial(m - 1))


@lru_cache(None)
def stratum(a, b, m, radius):
    """Delta-normalized volume, sum x_i=0; a positive/b negative tails."""
    radius = F(radius)
    if min(a, b, m) < 0 or a + b + m < 2 or radius < 0:
        raise ValueError("invalid stratum")
    if a == b == 0:
        return sum(F((-1) ** j * comb(m, j) * max(m - 2 * j, 0) ** (m - 1),
                     factorial(m - 1)) for j in range(m + 1))
    if m == 0:
        if not a or not b:
            return F(0)
        s = b - a
        if abs(s) >= radius:
            return F(0)
        ans = F(0)
        for i in range(a):
            for j in range(b):
                ans += (comb(a - 1, i) * comb(b - 1, j) * (-1) ** j
                        * F(s) ** (i + j)
                        * monomial_integral(a + b - 2 - i - j, abs(s), radius))
        return ans / (2 ** (a + b - 1) * factorial(a - 1) * factorial(b - 1))
    if a == 0:
        return stratum(b, a, m, radius)
    ans = F(0)
    for j in range(m + 1):
        s = m - a + b - 2 * j
        if b:
            part = two_sided(a, b, m, s, radius)
        else:
            cap = min(radius, F(s))
            part = sum((F(comb(m - 1, k) * (-1) ** k) * F(s) ** (m - 1 - k)
                        * monomial_integral(a - 1 + k, 0, cap)
                        for k in range(m)), F(0)) / (factorial(a - 1) * factorial(m - 1))
        ans += (-1) ** j * comb(m, j) * part
    if ans < 0:
        raise ArithmeticError("negative stratum volume")
    return ans


def section(N, radius=None):
    """vol_(N-1)({sum x=0, sum (|x|-1)+<=radius}) / sqrt(N)."""
    if type(N) is not int or N < 2:
        raise ValueError("N must be an integer >=2")
    radius = F(N if radius is None else radius)
    if radius < 0:
        raise ValueError("negative radius")
    return sum((F(factorial(N), factorial(a) * factorial(b) * factorial(N - a - b))
                * stratum(a, b, N - a - b, radius)
                for a in range(N + 1) for b in range(N + 1 - a)), F(0))


def sharp_constant(n):
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")
    return section(n + 1) * F(factorial(n), (n + 1) ** n)


if __name__ == '__main__':
    import json
    print(json.dumps({str(n): str(sharp_constant(n)) for n in range(1, 13)}, indent=2))
