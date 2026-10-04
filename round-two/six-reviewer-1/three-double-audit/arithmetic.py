"""Fresh reviewer arithmetic; no author modules or expected-output input."""
from fractions import Fraction as F
from math import comb, isqrt


def require(ok, label):
    if not ok:
        raise ValueError(label)


def add(a, b):
    return [(a[i] if i < len(a) else F(0)) + (b[i] if i < len(b) else F(0))
            for i in range(max(len(a), len(b)))]


def scale(a, k):
    return [k * x for x in a]


def mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def power(a, n):
    out = [F(1)]
    for _ in range(n):
        out = mul(out, a)
    return out


def integrate(a):
    return sum((x / (i + 1) for i, x in enumerate(a)), F(0))


def pad(a, n):
    require(len(a) <= n + 1, 'polynomial degree')
    return a + [F(0)] * (n + 1 - len(a))


def bproduct(a, b):
    """Bernstein product, separately implemented from monomial convolution."""
    m, n = len(a) - 1, len(b) - 1
    return [sum((a[i] * b[k-i] * F(comb(m, i) * comb(n, k-i), comb(m+n, k))
                 for i in range(max(0, k-n), min(m, k)+1)), F(0))
            for k in range(m+n+1)]


def bpower(a, n):
    out = [F(1)]
    for _ in range(n):
        out = bproduct(out, a)
    return out


def elevate(a, n):
    require(n >= len(a)-1, 'Bernstein elevation degree')
    return bproduct(a, [F(1)] * (n - len(a) + 2))


def btopower(a):
    n = len(a)-1
    return [sum((a[i] * comb(n, i) * comb(n-i, k-i) * (-1)**(k-i)
                 for i in range(k+1)), F(0)) for k in range(n+1)]


def bintegrate(a):
    return sum(a, F(0)) / len(a)


def kernel_bernstein(terms, n):
    """Direct t^r(1-t)^s coefficients in Bernstein degree n."""
    out = [F(0)] * (n+1)
    for r, s, weight in terms:
        require(r+s <= n, 'kernel degree')
        for i in range(r, n-s+1):
            out[i] += weight * F(comb(n-r-s, i-r), comb(n, i))
    return out


def ceiling(x, denominator):
    require(x >= 0 and denominator > 0, 'ceiling domain')
    target = x * denominator**2
    k = isqrt(target.numerator // target.denominator)
    if k*k < target:
        k += 1
    # A second, binary-search construction uses no isqrt.
    lo, hi = 0, max(1, target.numerator + 1)
    while lo < hi:
        mid = (lo+hi)//2
        if mid*mid >= target:
            hi = mid
        else:
            lo = mid+1
    require(k == lo and F(k*k) >= target and
            (k == 0 or F((k-1)**2) < target), 'entire square ceiling')
    return F(k, denominator)


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {k: encode(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [encode(v) for v in x]
    return x
