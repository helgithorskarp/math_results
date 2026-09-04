"""Exact four-coloring of E = Q(sqrt(-3), sqrt(-11)).

An element (a,b,c,d) means a + b*sqrt(33) + c*i*sqrt(3) + d*i*sqrt(11).
See PROOF.md. Only rational and integer arithmetic is used.
"""

from fractions import Fraction
from functools import lru_cache
from math import lcm


def element(a=0, b=0, c=0, d=0):
    return tuple(Fraction(x) for x in (a, b, c, d))


ZERO = element()
ONE = element(1)


def add(x, y):
    return tuple(a+b for a, b in zip(x, y, strict=True))


def negate(x):
    return tuple(-a for a in x)


def conjugate(x):
    return x[0], x[1], -x[2], -x[3]


def multiply(x, y):
    a, b, c, d = x
    A, B, C, D = y
    return (a*A + 33*b*B - 3*c*C - 11*d*D,
            a*B + b*A - c*D - d*C,
            a*C + c*A + 11*(b*D + d*B),
            a*D + d*A + 3*(b*C + c*B))


def inverse(x):
    a, b, c, d = multiply(x, conjugate(x))
    if c or d:
        raise ArithmeticError('norm did not lie in Q(sqrt(33))')
    denominator = a*a - 33*b*b
    if denominator == 0:
        raise ZeroDivisionError('zero field element')
    return multiply(conjugate(x), element(a/denominator, -b/denominator))


@lru_cache(maxsize=None)
def root33_mod_power2(bits):
    """The branch sqrt(33) = 1 mod 8, modulo 2**bits.

    Lift t in 4*t*t+t-2=0 by its unique next binary digit; r=1+8*t.
    """
    if not isinstance(bits, int) or bits < 1:
        raise ValueError('bits must be a positive integer')
    t = 0
    for j in range(max(0, bits-3)):
        if (4*t*t+t-2) % (1 << (j+1)):
            t += 1 << j
        if (4*t*t+t-2) % (1 << (j+1)):
            raise ArithmeticError('Hensel lifting invariant failed')
    modulus = 1 << bits
    r = (1+8*t) % modulus
    if (r*r-33) % modulus:
        raise ArithmeticError('bad square root')
    return r


def color_numerators(numerators, denominator):
    """Color an integer coefficient tuple divided by a positive integer.

    Works for points outside the local integer ring, too. It extracts the
    coefficient of 2**0 in both local coordinates, not just a residue of an
    assumed integral element. Noncanonical integer representations are valid.
    """
    if (not isinstance(denominator, int) or denominator <= 0
            or len(numerators) != 4
            or any(not isinstance(x, int) for x in numerators)):
        raise ValueError('expected four integer numerators and a positive denominator')
    a, b, c, d = numerators
    e = (denominator & -denominator).bit_length()-1
    modulus = 1 << (e+1)
    r = root33_mod_power2(e+1)
    inverse_odd = pow(3*(denominator >> e), -1, modulus)
    # The embedding sends z to A+B*w, w*w+w+1=0, where
    # 3*denominator*A = 3*a+3*b*r+3*c+d*r,
    # 3*denominator*B = 6*c+2*d*r.
    A = ((3*a+3*b*r+3*c+d*r)*inverse_odd) % modulus
    B = ((6*c+2*d*r)*inverse_odd) % modulus
    return (A >> e) + 2*(B >> e)


def color(x):
    denominator = lcm(*(v.denominator for v in x))
    return color_numerators(tuple(int(v*denominator) for v in x), denominator)


def is_unit(x):
    return multiply(x, conjugate(x)) == ONE
