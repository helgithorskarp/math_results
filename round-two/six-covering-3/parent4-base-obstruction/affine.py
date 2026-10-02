"""Complete prefix-stabilizing affine normal form for ORIGINAL15 and18.

Modulo2520, u is a unit with u=1mod3; v=0mod72, v=1-u mod35.
These288 maps preserve the five literal P classes, parent4, original resources,
CRT coordinate distinction and mod3 colors. The original15 and18 orbit
parameters are independent. No peer prefix/presence/phase bound is imported.
"""
from math import gcd

REPS15 = (0, 1, 2, 4, 6, 11)
REPS18 = (0, 1, 2, 3, 4, 5, 6, 9, 12, 15)


def group():
    return [(u, 72 * (((1 - u) * pow(72, -1, 35)) % 35))
            for u in range(2520) if gcd(u, 2520) == 1 and u % 3 == 1]


def normalizer(a15, a18):
    if type(a15) is not int or type(a18) is not int or not (0 <= a15 < 15 and 0 <= a18 < 18):
        raise ValueError('Invalid original15/18 phase pair')
    images = [((u * a15 + v) % 15, (u * a18 + v) % 18, u, v)
              for u, v in group()]
    eligible = [row for row in images if row[0] in REPS15 and row[1] in REPS18]
    if not eligible:
        raise ValueError('Incomplete simultaneous original15/18 normal form')
    a, b, u, v = min(eligible)
    return u, v


def normalize(phases):
    expected = [n for n in range(8, 2521) if 2520 % n == 0 and n not in (8, 9, 10, 12, 14)]
    if not isinstance(phases, list) or len(phases) != 36 or [n for n, a in phases] != expected or any(type(a) is not int or not 0 <= a < n for n, a in phases):
        raise ValueError("Normalizer requires the entire original BASE inventory")
    values = dict(phases)
    if len(values) != len(phases) or 15 not in values or 18 not in values:
        raise ValueError('Normalizer needs unique originals15 and18')
    u, v = normalizer(values[15], values[18])
    return [[n, (u * a + v) % n] for n, a in phases], [u, v]
