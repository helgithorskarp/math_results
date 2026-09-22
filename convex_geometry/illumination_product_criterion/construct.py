"""Exact finite-family products and greedy covers. Python 3.11+, stdlib.

Ground elements are 0,...,n-1; bit i represents element i.
This module produces certificates. verify.py reconstructs and checks them.
No claim is made that an arbitrary input set family is geometrically realizable.
"""
from fractions import Fraction
from itertools import product


def check_family(n, masks):
    if type(n) is not int or n < 1:
        raise ValueError("positive integer ground-set size required")
    masks = tuple(masks)
    full = (1 << n) - 1
    if not masks or any(type(m) is not int or m <= 0 or m > full for m in masks):
        raise ValueError("nonempty in-range integer masks required")
    if len(set(masks)) != len(masks):
        raise ValueError("duplicate masks")
    union = 0
    for m in masks:
        union |= m
    if union != full:
        raise ValueError("family does not cover the ground set")
    return masks


def check_weights(n, masks, weights):
    masks = check_family(n, masks)
    weights = tuple(Fraction(x) for x in weights)
    if len(weights) != len(masks) or any(x < 0 for x in weights):
        raise ValueError("nonnegative weight for each class required")
    if any(sum(w for m, w in zip(masks, weights) if m >> i & 1) < 1
           for i in range(n)):
        raise ValueError("fractional cover is infeasible")
    return weights


def tensor(n, masks, weights, r):
    """Product ordering is lexicographic, last coordinate varying fastest."""
    masks = check_family(n, masks)
    weights = check_weights(n, masks, weights)
    if type(r) is not int or r < 1:
        raise ValueError("positive integer exponent required")
    choices = [(m, w) for m, w in zip(masks, weights) if w > 0]
    result_masks, result_weights = [], []
    for entries in product(choices, repeat=r):
        current = [0]
        weight = Fraction(1)
        for m, w in entries:
            current = [a * n + b for a in current for b in range(n) if m >> b & 1]
            weight *= w
        result_masks.append(sum(1 << x for x in current))
        result_weights.append(weight)
    return n ** r, tuple(result_masks), tuple(result_weights)


def greedy(n, masks, weights):
    """Produce a cover and exact uncovered-count trace, with fixed tie breaking."""
    masks = check_family(n, masks)
    weights = check_weights(n, masks, weights)
    useful = tuple(i for i, w in enumerate(weights) if w > 0)
    uncovered = (1 << n) - 1
    indices, remaining = [], [n]
    while uncovered:
        i = max(useful, key=lambda j: ((masks[j] & uncovered).bit_count(), -j))
        gain = (masks[i] & uncovered).bit_count()
        if gain == 0:
            raise ValueError("no progress in a declared cover")
        indices.append(i)
        uncovered &= ~masks[i]
        remaining.append(uncovered.bit_count())
    return {"indices": indices, "remaining": remaining}


def power_bound(v, tau, r):
    if type(v) is not int or v < 2 or type(r) is not int or r < 1:
        raise ValueError("v>=2 and r>=1 must be integers")
    tau = Fraction(tau)
    if tau <= 1:
        raise ValueError("bound requires tau>1")
    t = tau ** r
    ceiling = (t.numerator + t.denominator - 1) // t.denominator
    return ceiling * (1 + r * (v - 1).bit_length())


def strict_exponent(v, tau, ordinary):
    """Find a sufficient strict-power exponent, not necessarily the first one."""
    tau = Fraction(tau)
    if type(ordinary) is not int or not 1 < tau < ordinary:
        raise ValueError("a certified strict fractional gap is required")
    r = 1
    while power_bound(v, tau, r) >= ordinary ** r:
        r += 1
    return {"r": r, "upper_bound": power_bound(v, tau, r),
            "ordinary_power": ordinary ** r}
