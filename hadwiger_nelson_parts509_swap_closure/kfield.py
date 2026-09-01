#!/usr/bin/env python3
"""Exact arithmetic in the tower Q < Q(sqrt3) < Q(sqrt3,sqrt5) < Q(sqrt3,sqrt5,sqrt11).

Elements of K_k are tuples of 2^k Fractions indexed by subset masks over
PRIMES[:k]; the coefficient at mask m multiplies prod_{bit in m} sqrt(PRIMES[bit]).
This matches the basis convention of parts509.py (bit 0 = sqrt3, bit 1 = sqrt5,
bit 2 = sqrt11).  No floating point is used anywhere in this module.
"""
from __future__ import annotations
from fractions import Fraction
from math import isqrt

PRIMES = (3, 5, 11)
F0 = Fraction(0)
F1 = Fraction(1)


def zero(k):
    return (F0,) * (1 << k)


def one(k):
    return (F1,) + (F0,) * ((1 << k) - 1)


def const(k, r):
    return (Fraction(r),) + (F0,) * ((1 << k) - 1)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def neg(x):
    return tuple(-a for a in x)


def scale(x, r):
    r = Fraction(r)
    return tuple(a * r for a in x)


def is_zero(x):
    return not any(x)


def mul(x, y, k):
    n = 1 << k
    out = [F0] * n
    for sx, a in enumerate(x):
        if not a:
            continue
        for sy, b in enumerate(y):
            if not b:
                continue
            c = a * b
            common = sx & sy
            for bit in range(k):
                if (common >> bit) & 1:
                    c *= PRIMES[bit]
            out[sx ^ sy] += c
    return tuple(out)


def split(x, k):
    """x in K_k -> (a, b) in K_{k-1}^2 with x = a + b*sqrt(PRIMES[k-1])."""
    h = 1 << (k - 1)
    return tuple(x[:h]), tuple(x[h:])


def join(a, b):
    return tuple(a) + tuple(b)


def lift(x, k_from, k_to):
    """Embed x in K_{k_from} into K_{k_to} (k_to >= k_from)."""
    return tuple(x) + (F0,) * ((1 << k_to) - (1 << k_from))


def inv(x, k):
    if is_zero(x):
        raise ZeroDivisionError("field inverse of zero")
    if k == 0:
        return (F1 / x[0],)
    p = PRIMES[k - 1]
    a, b = split(x, k)
    if is_zero(b):
        return join(inv(a, k - 1), zero(k - 1))
    conj = join(a, neg(b))
    norm = sub(mul(a, a, k - 1), scale(mul(b, b, k - 1), p))  # in K_{k-1}, nonzero
    ninv = inv(norm, k - 1)
    return mul(conj, join(ninv, zero(k - 1)), k)


def rat_sqrt(r):
    r = Fraction(r)
    if r < 0:
        return None
    p, q = r.numerator, r.denominator
    sp, sq = isqrt(p), isqrt(q)
    if sp * sp == p and sq * sq == q:
        return Fraction(sp, sq)
    return None


def field_sqrt(x, k):
    """Return s in K_k with s*s == x, or None when x is not a square in K_k.

    Completeness argument (k >= 1, p = PRIMES[k-1], x = a + b sqrt p):
    a root s + t sqrt p satisfies s^2 + p t^2 = a and 2 s t = b.
    If b = 0 then s = 0 or t = 0, giving the two sub-cases tested.
    If b != 0 then s, t != 0 and 4 s^4 - 4 a s^2 + p b^2 = 0, so
    s^2 = (a +- r)/2 with r^2 = a^2 - p b^2; every candidate is tested and
    the returned root is confirmed by exact squaring.
    """
    if k == 0:
        r = rat_sqrt(x[0])
        return None if r is None else (r,)
    p = PRIMES[k - 1]
    a, b = split(x, k)
    if is_zero(b):
        s = field_sqrt(a, k - 1)
        if s is not None:
            return join(s, zero(k - 1))
        t = field_sqrt(scale(a, Fraction(1, p)), k - 1)
        if t is not None:
            return join(zero(k - 1), t)
        return None
    norm = sub(mul(a, a, k - 1), scale(mul(b, b, k - 1), p))
    r = field_sqrt(norm, k - 1)
    if r is None:
        return None
    for sign in (1, -1):
        c = scale(add(a, scale(r, sign)), Fraction(1, 2))
        if is_zero(c):
            continue
        s = field_sqrt(c, k - 1)
        if s is None:
            continue
        t = mul(b, inv(scale(s, 2), k - 1), k - 1)
        root = join(s, t)
        if mul(root, root, k) == tuple(x):
            return root
    return None


# --- rigorous real-embedding bounds (rational interval arithmetic) ---------

def _sqrt_bounds(n, digits=40):
    """Rational lower/upper bounds for sqrt(n) with width 10^-digits."""
    scale_ = 10 ** digits
    lo = isqrt(n * scale_ * scale_)
    return Fraction(lo, scale_), Fraction(lo + 1, scale_)


_RAD_BOUNDS = None


def real_bounds(x, k=3, digits=40):
    """Rational interval [lo, hi] certainly containing the real embedding of x."""
    global _RAD_BOUNDS
    if _RAD_BOUNDS is None:
        _RAD_BOUNDS = {p: _sqrt_bounds(p, digits) for p in PRIMES}
    lo_total = F0
    hi_total = F0
    for mask, a in enumerate(x):
        if not a:
            continue
        blo, bhi = F1, F1
        for bit in range(k):
            if (mask >> bit) & 1:
                slo, shi = _RAD_BOUNDS[PRIMES[bit]]
                blo, bhi = blo * slo, bhi * shi  # all positive
        if a > 0:
            lo_total += a * blo
            hi_total += a * bhi
        else:
            lo_total += a * bhi
            hi_total += a * blo
    return lo_total, hi_total


def sign(x, k=3):
    """Exact sign of the real embedding of x (nonzero elements are separated
    from zero by increasing precision; zero is detected exactly)."""
    if is_zero(x):
        return 0
    digits = 40
    while True:
        lo, hi = real_bounds(x, k, digits)
        if lo > 0:
            return 1
        if hi < 0:
            return -1
        digits *= 2
        global _RAD_BOUNDS
        _RAD_BOUNDS = {p: _sqrt_bounds(p, digits) for p in PRIMES}


def to_float(x, k=3):
    import math
    total = 0.0
    for mask, a in enumerate(x):
        if not a:
            continue
        v = float(a)
        for bit in range(k):
            if (mask >> bit) & 1:
                v *= math.sqrt(PRIMES[bit])
        total += v
    return total


def to_strings(x):
    return [str(a) for a in x]


def from_strings(strs):
    return tuple(Fraction(s) for s in strs)


if __name__ == "__main__":
    # self-test
    import random
    random.seed(1)
    k = 3
    for _ in range(200):
        x = tuple(Fraction(random.randint(-9, 9), random.randint(1, 7)) for _ in range(8))
        if is_zero(x):
            continue
        assert mul(x, inv(x, k), k) == one(k)
        sq = mul(x, x, k)
        r = field_sqrt(sq, k)
        assert r is not None and mul(r, r, k) == sq, (x, r)
    # non-square examples
    assert field_sqrt(const(3, 2), 3) is None
    assert field_sqrt(const(3, 7), 3) is None
    assert field_sqrt(const(3, 15), 3) is not None
    assert field_sqrt(const(3, 165), 3) is not None
    assert field_sqrt(const(3, -1), 3) is None
    assert field_sqrt(const(3, 2 * 165), 3) is None
    assert sign(sub(const(3, 2), (F0, F1, F0, F0, F0, F0, F0, F0))) == 1  # 2 - sqrt3 > 0
    assert sign(sub(const(3, 1), (F0, F1, F0, F0, F0, F0, F0, F0))) == -1  # 1 - sqrt3 < 0
    print("kfield self-test ok")
