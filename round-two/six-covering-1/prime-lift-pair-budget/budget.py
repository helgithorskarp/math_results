"""Exact local coset costs and resource-credit bounds; standard library only."""
from itertools import combinations, product
from math import gcd
from functools import reduce


def pair_cover(points, d, e):
    """Return two phases covering points, or None. Points must be nonempty."""
    a0, b0 = points[0] % d, points[0] % e
    other_b = {x % e for x in points if x % d != a0}
    if len(other_b) <= 1:
        return a0, next(iter(other_b), b0)
    other_a = {x % d for x in points if x % e != b0}
    if len(other_a) <= 1:
        return next(iter(other_a), a0), b0
    return None


def profile(points, resources, cofactor):
    if not points:
        raise ValueError('empty residual group')
    g = reduce(gcd, [cofactor] + [x - points[0] for x in points])
    singleton = [d for d in resources if g % d == 0]
    remaining = [d for d in resources if d not in singleton]
    pairs = [(d, e, pair_cover(points, d, e))
             for d, e in combinations(remaining, 2)]
    feasible = [(d, e, phases) for d, e, phases in pairs if phases is not None]
    return {'gcd': g, 'singleton': singleton,
            'cost': 2 if feasible else 3,
            'pair_count': len(feasible)}


def cost560_gcd1(points):
    """Exact non-singleton cost2/3 test for the full divisor set of560."""
    if not points or reduce(gcd, [560] + [x-points[0] for x in points]) != 1:
        raise ValueError('requires gcd1')
    return 2 if any(pair_cover(points, d, e) is not None
                    for d, e in [(2,4), (2,5), (2,7), (5,7)]) else 3


def charge(profiles, multiplicity, resources, parent_potentials):
    if len(profiles) != len(parent_potentials) or any(u < 0 for u in parent_potentials):
        raise ValueError('invalid parent potentials')
    v = {d: max([0] + [g['cost'] - 1 - u
                       for g, u in zip(profiles, parent_potentials)
                       if d in g['singleton']]) for d in resources}
    baseline = multiplicity * sum(g['cost'] for g in profiles)
    credit = multiplicity * sum(parent_potentials) + sum(v.values())
    return baseline - credit, v


def best_small_charge(profiles, multiplicity, resources):
    """Exhaust this small family of integer potentials; no matching theorem needed."""
    best = None
    for u in product(*(range(g['cost']) for g in profiles)):
        bound, v = charge(profiles, multiplicity, resources, u)
        if best is None or bound > best[0]:
            best = bound, u, v
    return best if best is not None else (0, (), {d: 0 for d in resources})
