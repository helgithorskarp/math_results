"""Local helper copied from our separately implemented outside-degree source.
Actual author six-books-3, researcher; original commit5ac6c693382a19253fa867f91d74f112e015a3a1.
No external source or catalogue. Retained functions are listed in provenance.
"""
from collections import Counter

from fractions import Fraction

from itertools import combinations, combinations_with_replacement, permutations

from math import factorial, gcd, lcm

from pathlib import Path

import argparse

import hashlib

import json

HERE = Path(__file__).resolve().parent

PAIRS = tuple(combinations(range(6), 2))

INDEX = {p: k for k, p in enumerate(PAIRS)}

PERM_BITS = tuple(tuple(1 << INDEX[tuple(sorted((p[i], p[j])))]
                       for i, j in PAIRS) for p in permutations(range(6)))

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def rows(mask):
    out = [set() for _ in range(6)]
    for k, (i, j) in enumerate(PAIRS):
        if mask >> k & 1:
            out[i].add(j)
            out[j].add(i)
    return out

def orbit(mask):
    bits = [k for k in range(15) if mask >> k & 1]
    return {sum(image[k] for k in bits) for image in PERM_BITS}

def local_matrix(mask, stars):
    f = rows(mask)
    local = [{4 + x for x in star} for star in stars]
    local += [{4 + j for j in f[i]} | {l for l, star in enumerate(stars) if i in star}
              for i in range(6)]
    h = list(map(len, local))
    need(h == [2] * 4 + [3] * 6, 'wrong local degree sequence')
    return [[h[i] + 2 if i == j else h[i] + h[j] -
             (5 if j in local[i] else 2) - len(local[i] & local[j])
             for j in range(10)] for i in range(10)]

def core_census():
    domain = set()
    for selected in combinations(range(15), 5):
        mask = sum(1 << k for k in selected)
        f = rows(mask)
        if max(map(len, f)) <= 3 and all(len(f[i] & f[j]) <= 1
                                        for i, j in PAIRS if j in f[i]):
            domain.add(mask)
    unseen = set(domain)
    records = []
    while unseen:
        mask = min(unseen)
        images = orbit(mask)
        need(images <= unseen, 'F orbit cover overlaps or omits an eligible graph')
        unseen -= images
        f = rows(mask)
        target = [3 - len(row) for row in f]
        nonedges = [p for p in PAIRS if p[1] not in f[p[0]]]
        profiles = []
        for stars in combinations_with_replacement(nonedges, 4):
            if [sum(i in star for star in stars) for i in range(6)] != target:
                continue
            full = local_matrix(mask, stars)
            if any(x < 0 for row in full for x in row):
                continue
            weight = factorial(4)
            for amount in Counter(stars).values():
                weight //= factorial(amount)
            compatible = all(full[i][j] >= 1 for i, j in combinations(range(4, 10), 2))
            profiles.append({'stars': [list(x) for x in stars],
                             'ordered_low_multiplicity': weight,
                             'all_cubic_row_compatible': compatible})
        records.append({'F_mask': mask, 'orbit_size': len(images),
                        'lambda': target, 'profiles': profiles})
    return domain, records

def weighted_stars(degrees, capacities):
    """Decide a vertex's entire remaining star before processing the next."""
    remaining = list(degrees)
    edges = []

    def visit():
        i = next((i for i, d in enumerate(remaining) if d), None)
        if i is None:
            yield tuple(edges)
            return
        amount = remaining[i]
        neighbors = [j for j in range(i + 1, len(degrees))
                     if remaining[j] and capacities[i][j] > 0]
        if sum(min(remaining[j], capacities[i][j]) for j in neighbors) < amount:
            return
        remaining[i] = 0

        def distribute(k, left):
            if k == len(neighbors):
                if left == 0:
                    yield from visit()
                return
            j = neighbors[k]
            future = sum(min(remaining[v], capacities[i][v]) for v in neighbors[k + 1:])
            for weight in range(max(0, left - future), min(left, remaining[j], capacities[i][j]) + 1):
                remaining[j] -= weight
                if weight:
                    edges.append((i, j, weight))
                yield from distribute(k + 1, left - weight)
                if weight:
                    edges.pop()
                remaining[j] += weight
        yield from distribute(0, amount)
        remaining[i] = amount
    yield from visit()

def primitive(vector):
    scale = lcm(*(x.denominator for x in vector))
    out = [int(x * scale) for x in vector]
    divisor = gcd(*out)
    need(divisor > 0, 'zero vector')
    out = [x // divisor for x in out]
    if next(x for x in out if x) < 0:
        out = [-x for x in out]
    return out

def quadratic(a, vector):
    return sum(a[i][j] * vector[i] * vector[j]
               for i in range(len(a)) for j in range(len(a)))

def negative_vector(original):
    n = len(original)
    a = [[Fraction(x) for x in row] for row in original]
    columns = [[Fraction(i == j) for i in range(n)] for j in range(n)]
    for k in range(n):
        pivot = a[k][k]
        if pivot < 0:
            out = primitive(columns[k])
            need(quadratic(original, out) < 0, 'invalid negative pivot witness')
            return out
        if pivot == 0:
            j = next((j for j in range(k + 1, n) if a[k][j]), None)
            if j is not None:
                cross = a[k][j]
                multiple = -(1 if cross > 0 else -1) * (int(abs(a[j][j]) / (2 * abs(cross))) + 1)
                out = primitive([multiple * x + y for x, y in zip(columns[k], columns[j])])
                need(quadratic(original, out) < 0, 'invalid zero pivot witness')
                return out
            continue
        multipliers = {j: a[k][j] / pivot for j in range(k + 1, n)}
        for j, multiplier in multipliers.items():
            columns[j] = [x - multiplier * y for x, y in zip(columns[j], columns[k])]
        for i in range(k + 1, n):
            for j in range(i, n):
                a[i][j] -= a[k][i] * multipliers[j]
                a[j][i] = a[i][j]
    raise RuntimeError('unexpected positive semidefinite survivor')
