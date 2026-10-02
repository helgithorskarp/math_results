"""Local erasure supports and a necessary two-layer hypergraph cut.

Exact integers only. Resource labels are cofactors; each layer has its
own original modulus corresponding to a label. No label is cloned within
one layer. A passing cut is inconclusive.
"""

from itertools import combinations, product
from math import gcd


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def signature(n, points):
    if not points:
        raise ValueError("a target must be nonempty")
    g = n
    for x in points:
        g = gcd(g, x - points[0])
    return g


def cheap_supports(n, points, labels, q):
    if q < 2 or not points or sorted(set(points)) != list(points):
        raise ValueError("invalid cost cutoff or target")
    if any(type(x) is not int or not 0 <= x < n for x in points):
        raise ValueError("invalid cofactor point")
    if sorted(set(labels)) != list(labels) or any(n % d for d in labels):
        raise ValueError("invalid resource labels")
    full = (1 << len(points)) - 1
    families = {
        d: sorted({sum(1 << j for j, x in enumerate(points) if x % d == a)
                   for a in range(d)}) for d in labels
    }
    supports = []
    for size in range(1, min(q - 1, len(labels)) + 1):
        for indices in combinations(range(len(labels)), size):
            good = False
            for masks in product(*(families[labels[j]] for j in indices)):
                union = 0
                for mask in masks:
                    union |= mask
                if union == full:
                    good = True
                    break
            if good:
                supports.append(sum(1 << j for j in indices))
    return supports


def parent_cut(n, fibers, labels, p=2, q=3):
    if type(p) is not int or p < 2 or type(q) is not int or q < 2:
        raise ValueError("invalid replication or cost cutoff")
    if not fibers:
        return {"value": 0, "threshold": -((p * (q - 1) + 1) * len(labels)),
                "excluded": False, "exceptional_parents": [], "right_labels": [],
                "supports": [], "first_erasure_lower_bound": 0}
    if len(labels) > 20:
        raise ValueError("bounded exact right-subset search supports <=20 labels")
    supports = [cheap_supports(n, v, labels, q) for v in fibers]
    left_cost = p * p * q * (q - 1)
    right_cost = (q - 1) * (p * (q - 1) + 1)
    best = None
    for right in range(1 << len(labels)):
        exceptional = [i for i, options in enumerate(supports)
                       if any(s & right == 0 for s in options)]
        value = left_cost * len(exceptional) + right_cost * right.bit_count()
        candidate = (value, right, tuple(exceptional))
        if best is None or candidate < best:
            best = candidate
    value, right, exceptional = best
    t, k = p * len(fibers), len(labels)
    erased_min = max(0, t - k // p)
    threshold = p * q * t + p * q * (q - 2) * erased_min - p * (q - 1) * k - k
    return {"value": value, "threshold": threshold, "excluded": value < threshold,
            "exceptional_parents": list(exceptional),
            "right_labels": [d for j, d in enumerate(labels) if right & (1 << j)],
            "supports": supports, "first_erasure_lower_bound": erased_min}
