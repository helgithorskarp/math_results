#!/usr/bin/env python3
"""Rational capped cores for the families in FRIENDSHIP.md."""
from fractions import Fraction as F
import certificates as build


def family(k):
    if not isinstance(k, int) or k < 1:
        raise ValueError("Friendship family requires integer k>=1")
    center = 1 << (2 * k)
    return sorted([0, center] + [1 << v for v in range(2 * k)] +
                  [center | (1 << v) for v in range(2 * k)] +
                  [(1 << (2 * j)) | (1 << (2 * j + 1)) for j in range(k)])


def kind(k, a):
    center = 1 << (2 * k)
    if a == center:
        return "a", None
    if a.bit_count() == 1:
        return "c", (a.bit_length() - 1) // 2
    if a & center:
        leaf = a ^ center
        return "b", (leaf.bit_length() - 1) // 2
    return "d", ((a & -a).bit_length() - 1) // 2


def certificate(k, shift=0):
    members = family(k)
    if k == 1:
        return build.uniform_rank_two_certificate(3, shift)
    f = F(1, k - 1)
    core = []
    for a in members[1:]:
        ta, ja = kind(k, a)
        row = []
        for b in members[1:]:
            tb, jb = kind(k, b)
            types = {ta, tb}
            if a == b:
                value = F(2 * k)
            elif a & b:
                value = F(-1)
            elif "a" in types:
                value = F(0)
            elif "b" in types:
                value = F(-1) if ja == jb else f
            elif ta == tb == "c":
                value = F(k - 2) if ja == jb else F(-1)
            elif types == {"c", "d"}:
                value = F(-1)
            elif ta == tb == "d":
                value = F(0)
            else:
                raise ValueError("Uncovered friendship core entry")
            row.append(value)
        core.append(row)
    return [a << shift for a in members], build.lift(core, 2 * k + 1), 2 * k + 1
