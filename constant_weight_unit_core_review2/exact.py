"""Primitives by six-reviewer-2, reused from constant_weight_twenty_eighteen_review2/exact.py
at 45d1c6acf5a7acd86fa4eba942d5376d6753ee91. Original kernel provenance:
constant_weight_support17_review2/audit.py at fad06f63a490bd7541990f1a3d18028ccd6b59d4.
"""

from collections import Counter

from itertools import combinations

import json

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
