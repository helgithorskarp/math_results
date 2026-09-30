"""Exact primitives by six-reviewer-2, reused from source fad06f6 with attribution."""

from collections import Counter

from hashlib import sha256

from itertools import combinations

import json

import time

def insist(ok, message):
    if not ok:
        raise ValueError(message)

def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()

def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask -= low

def mask(points):
    return sum(1 << x for x in points)

def pairs(word):
    return frozenset(combinations(bits(word), 2))

def words_json(words):
    return sorted([list(bits(w)) for w in words])

def packing(words, center=None, size=None):
    insist(len(words) == len(set(words)), 'duplicate word')
    insist(all(0 <= w < 1 << 18 and w.bit_count() == 5 for w in words), 'word domain')
    insist(all((a & b).bit_count() <= 2 for a, b in combinations(words, 2)), 'repeated triple')
    if center is not None:
        insist(all(w >> center & 1 for w in words), 'wrong center')
    if size is not None:
        insist(len(words) == size, 'wrong star size')

def mul(a, b):
    # Multiply the two degree-one binary polynomials, then reduce z^2=z+1.
    lo = (a & 1) * (b & 1)
    mid = ((a & 1) * (b >> 1)) ^ ((a >> 1) * (b & 1))
    hi = (a >> 1) * (b >> 1)
    return (lo ^ hi) | ((mid ^ hi) << 1)

def plane():
    # Generate translates of one-dimensional subspaces, with no line equations.
    directions = [(1, t) for t in range(4)] + [(0, 1)]
    lines = {mask(4 * (x ^ mul(s, dx)) + (y ^ mul(s, dy)) for s in range(4))
             for dx, dy in directions for x in range(4) for y in range(4)}
    counts = Counter(p for w in lines for p in pairs(w))
    insist(len(lines) == 20 and len(counts) == 120 and set(counts.values()) == {1}, 'plane')
    return tuple(sorted(lines))

AXES = {mask(range(4)), mask((0, 4, 8, 12))}

def first_star(replacement):
    result = tuple(sorted((line ^ 1 | 1 << replacement | 1 << 17)
                          if line & 1 and line not in AXES else line | 1 << 17
                          for line in plane()))
    packing(result, 17, 20)
    return result

def valid_extension(word, star):
    return all((word & old).bit_count() <= 2 for old in star if old != word)

def saturated_row(words, center, expected):
    insist(sum(w >> center & 1 for w in words) == 20, 'saturated replication changed')
    actual = {x: 5 - sum((w >> center & 1) and (w >> x & 1) for w in words)
              for x in range(18) if x != center}
    insist({x: d for x, d in actual.items() if d} == expected, 'saturated deficit pattern changed')

def compatibility(columns):
    supports = list(map(pairs, columns))
    adjacency = [0] * len(columns)
    for i, j in combinations(range(len(columns)), 2):
        if not supports[i] & supports[j]:
            adjacency[i] |= 1 << j
            adjacency[j] |= 1 << i
    return adjacency

def colored_order(active, adjacency):
    """Greedy independent color classes: their count bounds every clique."""
    order, bounds, color = [], [], 0
    while active:
        color += 1
        eligible = active
        while eligible:
            v = (eligible & -eligible).bit_length() - 1
            bit = 1 << v
            order.append(v)
            bounds.append(color)
            active ^= bit
            eligible &= ~bit & ~adjacency[v]
    return order, bounds

def clique_census(adjacency, target, cap=200000, seconds=10):
    """All target cliques, each once; no reliance on a cover-search routine."""
    insist(target >= 0 and cap >= 0, 'invalid clique parameters')
    n = len(adjacency)
    insist(all(a >= 0 and a < 1 << n and not (a >> i & 1)
               for i, a in enumerate(adjacency)), 'bad graph mask or loop')
    insist(all(bool(adjacency[i] >> j & 1) == bool(adjacency[j] >> i & 1)
               for i, j in combinations(range(n), 2)), 'asymmetric graph')
    answers, states = [], 0
    started = time.monotonic()

    def walk(active, chosen):
        nonlocal states
        states += 1
        if states > cap or time.monotonic() - started > seconds:
            raise RuntimeError('INCOMPLETE: clique census guard')
        need = target - len(chosen)
        if not need:
            answers.append(tuple(sorted(chosen)))
            return
        if active.bit_count() < need:
            return
        order, bounds = colored_order(active, adjacency)
        for k in range(len(order) - 1, -1, -1):
            if bounds[k] < need:
                return
            v = order[k]
            walk(active & adjacency[v], chosen + (v,))
            active &= ~(1 << v)

    walk((1 << n) - 1, ())
    insist(len(answers) == len(set(answers)), 'repeated clique')
    insist(all(len(q) == target and all(adjacency[i] >> j & 1 for i, j in combinations(q, 2))
               for q in answers), 'false clique witness')
    return sorted(answers), states

def point_capacity(columns, vertices):
    union = set().union(*(pairs(q) for q in columns)) if columns else set()
    degrees = [sum(x in p for p in union) for x in vertices]
    return sum(d // 3 for d in degrees) // 4, degrees
