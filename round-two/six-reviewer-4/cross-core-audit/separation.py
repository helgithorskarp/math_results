"""Independent exact missing-set sums and convex separation certificates."""
from itertools import product
from core import require, CYCLE

TARGET = (3, 3, 2, 2, 2, 2)
TABLE = {
    'A0': ((0, 1), (0, 3), (3, 5), (0, 2, 3)),
    'A1U': ((0, 2), (0, 3)), 'A1V': ((0, 3),),
    'B': ((1,), (0, 1), (1, 4), (2, 4)),
    'C': ((0, 1), (1, 4, 5)),
    'D': ((0, 1), (2, 4), (0, 2, 3))}
CASES = {'U': ('A0', 'A1U', 'B', 'B', 'C', 'C'),
         'V': ('A0', 'A1V', 'B', 'B', 'C', 'D')}


def independent_sets():
    return [tuple(i for i in range(6) if mask >> i & 1) for mask in range(64)
            if all(not (mask >> i & 1 and mask >> j & 1) for i, j in CYCLE)]


def relaxed_certificates():
    ind = independent_sets()
    require(len(ind) == 18, 'six-cycle domain')
    domains = {
        'U': [ind, TABLE['A1U'],
              [s for s in ind if 5 not in s and set(s) & {1, 4, 5}],
              [s for s in ind if 5 not in s and set(s) & {1, 4, 5}],
              TABLE['C'], TABLE['C']],
        'V': [[s for s in ind if set(s) & {0, 2, 3}], TABLE['A1V'],
              [s for s in ind if 5 not in s], [s for s in ind if 5 not in s],
              ind, [s for s in ind if 5 not in s]]}
    weights = {'U': (0, 0, 1, 1, -1, 1), 'V': (0, 1, 1, 0, 0, 1)}
    result = {}
    for case, ds in domains.items():
        w = weights[case]
        require(all(set(TABLE[r]) <= set(d) for r,d in zip(CASES[case], ds)),
                'original domain is contained in relaxation')
        maxima = [max(score(w,s) for s in d) for d in ds]
        target = sum(x*y for x,y in zip(w,TARGET))
        require(target > sum(maxima), 'relaxed separation')
        result[case] = {'weights': list(w), 'domains': [list(map(list,d)) for d in ds],
                        'sizes': [len(d) for d in ds], 'maxima': maxima,
                        'upper': sum(maxima), 'target': target,
                        'gap': target-sum(maxima),
                        'fractional_mixtures_excluded': True}
    return result


def totals(sets):
    return tuple(sum(i in s for s in sets) for i in range(6))


def score(weights, missing):
    return sum(weights[i] for i in missing)


def certificate(weights, case):
    roles = CASES[case]
    maxima = [max(score(weights, s) for s in TABLE[role]) for role in roles]
    target = sum(a * b for a, b in zip(weights, TARGET))
    return {'weights': list(weights), 'roles': list(roles), 'maxima': maxima,
            'upper': sum(maxima), 'target': target, 'gap': target - sum(maxima)}


def discover():
    # This finite discovery is not a proof of globally minimal coefficients.
    best = {}
    for w in product(range(-2, 3), repeat=6):
        for case in CASES:
            cert = certificate(w, case)
            if cert['gap'] > 0:
                quality = (sum(abs(x) for x in w), max(abs(x) for x in w), w)
                if case not in best or quality < best[case][0]:
                    best[case] = (quality, cert)
    require(set(best) == set(CASES), 'small separation discovery incomplete')
    return {case: best[case][1] for case in CASES}


def sums():
    out = {}
    for case, roles in CASES.items():
        vectors = [totals(t) for t in product(*(TABLE[r] for r in roles))]
        out[case] = {'count': len(vectors), 'distinct_totals': len(set(vectors)),
                     'hits': sum(v == TARGET for v in vectors),
                     'vectors': [list(v) for v in vectors]}
    return out
