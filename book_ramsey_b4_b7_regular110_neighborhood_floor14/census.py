"""Local helper copied from our separately implemented outside-degree source.
Actual author six-books-3, researcher; original commit5ac6c693382a19253fa867f91d74f112e015a3a1.
No external source or catalogue. Retained functions are listed in provenance.
"""
from collections import Counter

from itertools import combinations, permutations

from math import gcd

from pathlib import Path

import argparse

import hashlib

import json

HERE = Path(__file__).resolve().parent

P = tuple(combinations(range(6), 2))

POSITION = {edge: k for k, edge in enumerate(P)}

POINT_MAPS = tuple(permutations(range(6)))

LOW_MAPS = tuple(permutations(range(4)))

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def f_neighbors(mask):
    bits = [0] * 6
    for bit, (u, v) in enumerate(P):
        if mask & (1 << bit):
            bits[u] |= 1 << v
            bits[v] |= 1 << u
    return bits

def transform(mask, point):
    return sum(1 << POSITION[tuple(sorted((point[u], point[v])))]
               for bit, (u, v) in enumerate(P) if mask & (1 << bit))

def formula(mask, stars):
    """Class-by-class pair counts; no general adjacency formula is used."""
    f = f_neighbors(mask)
    low = [sum(1 << x for x in star) for star in stars]
    need(len(stars) == 4 and all(len(set(s)) == 2 for s in stars), 'invalid low pairs')
    need(all(not (f[s[0]] >> s[1] & 1) for s in stars), 'low pair is a red F edge')
    need(all(f[i].bit_count() + sum(x >> i & 1 for x in low) == 3 for i in range(6)),
         'wrong cubic degree')
    a = [[0] * 10 for _ in range(10)]
    for i in range(10):
        a[i][i] = 4 if i < 4 else 5
    for i, j in combinations(range(4), 2):
        a[i][j] = a[j][i] = 2 - (low[i] & low[j]).bit_count()
    for i in range(4):
        for j in range(6):
            value = 0 if low[i] >> j & 1 else 3 - (low[i] & f[j]).bit_count()
            a[i][4 + j] = a[4 + j][i] = value
    for i, j in P:
        common = (f[i] & f[j]).bit_count() + sum(x >> i & 1 and x >> j & 1 for x in low)
        value = (1 if f[i] >> j & 1 else 4) - common
        a[4 + i][4 + j] = a[4 + j][4 + i] = value
    return a

def ordered_profiles(mask):
    f = f_neighbors(mask)
    deficit = [3 - x.bit_count() for x in f]
    nonedges = [edge for edge in P if not (f[edge[0]] >> edge[1] & 1)]
    chosen = []

    def visit():
        if len(chosen) == 4:
            if not any(deficit):
                yield tuple(chosen)
            return
        for u, v in nonedges:
            if deficit[u] and deficit[v]:
                deficit[u] -= 1
                deficit[v] -= 1
                chosen.append((u, v))
                if max(deficit) <= 4 - len(chosen):
                    yield from visit()
                chosen.pop()
                deficit[u] += 1
                deficit[v] += 1
    yield from visit()

def census(expected):
    domain = []
    for mask in range(1 << 15):
        if mask.bit_count() != 5:
            continue
        f = f_neighbors(mask)
        if max(x.bit_count() for x in f) <= 3 and all((f[u] & f[v]).bit_count() <= 1
                    for bit, (u, v) in enumerate(P) if mask >> bit & 1):
            domain.append(mask)
    need(len(domain) == expected['eligible_labeled_F'], 'F domain size mismatch')
    digest = hashlib.sha256(''.join(str(x) + '\n' for x in domain).encode()).hexdigest()
    need(digest == expected['F_domain_sha256'], 'F domain mismatch')
    owner = {}
    declared = {}
    for rec in expected['catalog']:
        rep = rec['F_mask']
        images = {}
        for point in POINT_MAPS:
            image = transform(rep, point)
            if image not in images:
                inverse = tuple(point.index(i) for i in range(6))
                images[image] = inverse
        need(rep == min(images) and len(images) == rec['orbit_size'], 'invalid F orbit representative')
        need(not (set(images) & set(owner)), 'overlapping F orbits')
        for image, inverse in images.items():
            owner[image] = (rep, inverse)
        need(rec['lambda'] == [3 - x.bit_count() for x in f_neighbors(rep)], 'lambda mismatch')
        declared[rep] = {tuple(tuple(x) for x in p['stars']): p for p in rec['profiles']}
        need(len(declared[rep]) == len(rec['profiles']), 'duplicate declared profile')
    need(set(owner) == set(domain), 'incomplete F orbit cover')
    need(len(expected['catalog']) == expected['F_orbits'], 'F orbit count mismatch')
    observed = Counter()
    labeled = 0
    entry_comparisons = 0
    for mask in domain:
        rep, point = owner[mask]
        for stars in ordered_profiles(mask):
            a = formula(mask, stars)
            if any(x < 0 for row in a for x in row):
                continue
            mapped = [tuple(sorted(point[i] for i in s)) for s in stars]
            low_order = sorted(range(4), key=lambda i: mapped[i])
            canonical = tuple(mapped[i] for i in low_order)
            need(canonical in declared[rep], 'uncovered labeled local core')
            image = [low_order.index(i) for i in range(4)] + [4 + point[i] for i in range(6)]
            b = formula(rep, canonical)
            need(all(a[i][j] == b[image[i]][image[j]] for i in range(10) for j in range(10)),
                 'core relabeling changes a matrix entry')
            observed[(rep, canonical)] += 1
            labeled += 1
            entry_comparisons += 100
    need(labeled == expected['labeled_local_cores'], 'labeled core census mismatch')
    need(len(observed) == expected['normalized_profiles'], 'normalized profile count mismatch')
    for rec in expected['catalog']:
        rep = rec['F_mask']
        need({key[1] for key in observed if key[0] == rep} == set(declared[rep]), 'profile cover mismatch')
        for stars, profile in declared[rep].items():
            need(observed[(rep, stars)] == rec['orbit_size'] * profile['ordered_low_multiplicity'],
                 'profile multiplicity mismatch')
            a = formula(rep, stars)
            flag = all(a[i][j] >= 1 for i, j in combinations(range(4, 10), 2))
            need(flag == profile['all_cubic_row_compatible'], 'all-cubic row compatibility mismatch')
    return observed, {'labeled_local_cores_replayed': labeled,
                      'core_matrix_entries_compared': entry_comparisons}

def single_edge_weights(degrees, capacities):
    """Decide successive edge weights, with remaining-capacity pruning."""
    pairs = [(u, v, capacities[u][v]) for u, v in combinations(range(10), 2)
             if capacities[u][v] and degrees[u] and degrees[v]]
    n = len(pairs)
    future = [[0] * 10 for _ in range(n + 1)]
    pending = [[[] for _ in range(10)] for _ in range(n + 1)]
    for k in range(n - 1, -1, -1):
        u, v, cap = pairs[k]
        future[k] = future[k + 1][:]
        future[k][u] += cap
        future[k][v] += cap
        pending[k] = [r[:] for r in pending[k + 1]]
        pending[k][u].append((v, cap))
        pending[k][v].append((u, cap))
    remaining = list(degrees)
    chosen = []

    def visit(k):
        if any(remaining[i] > future[k][i] for i in range(10)):
            return
        if k == n:
            if not any(remaining):
                yield tuple(chosen)
            return
        u, v, cap = pairs[k]
        if k == 0 or pairs[k - 1][0] != u:
            if any(remaining[i] > sum(min(c, remaining[j]) for j, c in pending[k][i])
                   for i in range(10) if remaining[i]):
                return
        lo = max(0, remaining[u] - future[k + 1][u], remaining[v] - future[k + 1][v])
        hi = min(cap, remaining[u], remaining[v])
        for weight in range(lo, hi + 1):
            remaining[u] -= weight
            remaining[v] -= weight
            if weight:
                chosen.append((u, v, weight))
            yield from visit(k + 1)
            if weight:
                chosen.pop()
            remaining[u] += weight
            remaining[v] += weight
    yield from visit(0)

def baseline():
    data = (HERE / 'baseline21.rows').read_bytes()
    need(hashlib.sha256(data).hexdigest() == '4f1dd2bc743590a0553107936656e469db6e7d742db0456d697353ce50aac5ec',
         'baseline hash mismatch')
    lines = data.decode().splitlines()
    need(len(lines) == 21 and all(len(s) == 21 and set(s) <= {'0', '1'} for s in lines), 'bad baseline dimensions')
    red = [{j for j, x in enumerate(s) if x == '1'} for s in lines]
    need(all(i not in red[i] and all((j in red[i]) == (i in red[j]) for j in range(21))
             for i in range(21)), 'bad baseline adjacency')
    blue = [set(range(21)) - r - {i} for i, r in enumerate(red)]
    need(sum(map(len, red)) == 186, 'wrong baseline size')
    need(max(len(red[i] & red[j]) for i, j in combinations(range(21), 2) if j in red[i]) == 3,
         'baseline red cap failed')
    need(max(len(blue[i] & blue[j]) for i, j in combinations(range(21), 2) if j in blue[i]) == 6,
         'baseline blue cap failed')
    return 'verified existing 21-vertex construction, not a new construction'
