#!/usr/bin/env python3
"""Rational centered signed cores for rank-two K_2 join I_t downsets."""
from fractions import Fraction as F
import certificates as base


def family(t, shift=0):
    if not isinstance(t, int) or isinstance(t, bool) or t < 1 or not isinstance(shift, int) or isinstance(shift, bool) or shift < 0:
        raise ValueError("Positive integer leaf count and nonnegative shift required")
    a, b = 1 << t, 1 << (t + 1)
    leaves = [1 << i for i in range(t)]
    return sorted(x << shift for x in [0, a, b, a | b] + leaves +
                  [c | center for c in leaves for center in (a, b)])


def core(t):
    if not isinstance(t, int) or isinstance(t, bool) or t < 1:
        raise ValueError("The centered two-center formula requires t>=1")
    members = family(t)[1:]
    centers = (1 << t) | (1 << (t + 1))
    answer = []
    for x in members:
        row = []
        for y in members:
            if x == y:
                z = F(t + 1)
            elif x & y:
                z = F(-1)
            elif x.bit_count() == y.bit_count() == 1:
                cx, cy = bool(x & centers), bool(y & centers)
                z = F(-1) if cx and cy else F(-1, t) if cx or cy else F(-t - 1, t)
            elif x.bit_count() == y.bit_count() == 2:
                z = F(2, t)
            else:
                single, edge = (x, y) if x.bit_count() == 1 else (y, x)
                z = F(2, t) if single & centers else F(t + 1, t) if edge == centers else F(0)
            row.append(z)
        answer.append(row)
    return answer


def certificate(t, shift=0):
    members = family(t, shift)
    return members, base.lift(core(t), t + 2), t + 2
