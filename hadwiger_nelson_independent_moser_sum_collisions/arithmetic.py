"""Exact E arithmetic, adapted from the preceding weighted-rotation package."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import isqrt, lcm
from pathlib import Path
ZERO = (F(0),) * 4
ONE = (F(1), F(0), F(0), F(0))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def add(x, y):
    return tuple((a + b for a, b in zip(x, y)))

def scale(x, s):
    return tuple((s * a for a in x))

def sub(x, y):
    return add(x, scale(y, -1))

def conj(x):
    return (x[0], x[1], -x[2], -x[3])

def mul(x, y):
    a, b, c, d = x
    A, B, C, D = y
    return (a * A + 33 * b * B - 3 * c * C - 11 * d * D, a * B + b * A - c * D - d * C, a * C + c * A + 11 * (b * D + d * B), a * D + d * A + 3 * (b * C + c * B))

def norm(x):
    return mul(x, conj(x))

def inverse_real(x):
    a, b, c, d = x
    require(c == d == 0, 'nonreal inverse')
    den = a * a - 33 * b * b
    require(den != 0, 'zero inverse')
    return (a / den, -b / den, F(0), F(0))

def rational_sqrt(q):
    if q < 0:
        return None
    a, b = (isqrt(q.numerator), isqrt(q.denominator))
    return F(a, b) if a * a == q.numerator and b * b == q.denominator else None

def sqrt_real(x):
    a, b, c, d = x
    require(c == d == 0, 'nonreal square-root input')
    if not b:
        s = rational_sqrt(a)
        if s is not None:
            return (s, F(0), F(0), F(0))
        s = rational_sqrt(a / 33)
        return None if s is None else (F(0), s, F(0), F(0))
    h = rational_sqrt(a * a - 33 * b * b)
    if h is None:
        return None
    for sign in (-1, 1):
        q = rational_sqrt((a + sign * h) / 2)
        if q:
            z = (q, b / (2 * q), F(0), F(0))
            require(mul(z, z) == x, 'square-root identity')
            return z
    return None

def differences(A):
    pairs = {}
    for i, a in enumerate(A):
        for j, b in enumerate(A):
            pairs.setdefault(sub(a, b), []).append((i, j))
    return pairs

def root33(bits):
    t = 0
    for j in range(max(0, bits - 3)):
        if (4 * t * t + t - 2) % (1 << j + 1):
            t += 1 << j
    r = (1 + 8 * t) % (1 << bits)
    require((r * r - 33) % (1 << bits) == 0, 'Hensel root')
    return r

def residue(z):
    """Reduction in O/4 = (Z/4)[w]/(w^2+w+1); reject nonintegral input."""
    den = lcm(*(x.denominator for x in z))
    a, b, c, d = [int(x * den) for x in z]
    e = (den & -den).bit_length() - 1
    mod = 1 << e + 2
    r = root33(e + 2)
    iv = pow(3 * (den >> e), -1, mod)
    A = (3 * a + 3 * b * r + 3 * c + d * r) * iv % mod
    B = (6 * c + 2 * d * r) * iv % mod
    require(A % (1 << e) == B % (1 << e) == 0, 'point outside O')
    return (A >> e, B >> e)
