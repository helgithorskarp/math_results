#!/usr/bin/env python3
"""Catalogue-free enumeration of the 25 facet incidence types."""
from itertools import combinations, permutations

PAIRS = list(combinations(range(6), 2))
INDEX = {p: i for i, p in enumerate(PAIRS)}


def decode(mask):
    return [p for i, p in enumerate(PAIRS) if mask >> i & 1]


def admissible(mask, k):
    if mask.bit_count() != k:
        return False
    degrees = [0] * 6
    for u, v in decode(mask):
        degrees[u] += 1
        degrees[v] += 1
    return (k != 5 or min(degrees) >= 1) and (k != 6 or degrees == [2] * 6)


def enumerate_cases():
    maps = [[INDEX[tuple(sorted((p[u], p[v])))] for u, v in PAIRS]
            for p in permutations(range(6))]
    result = []
    for k in (3, 4, 5, 6):
        pending = {m for m in range(1 << 15) if admissible(m, k)}
        while pending:
            rep = min(pending)
            bits = [i for i in range(15) if rep >> i & 1]
            orbit = {sum(1 << p[i] for i in bits) for p in maps}
            assert orbit <= pending
            pending.difference_update(orbit)
            result.append({'id': f'{k}_{rep:04x}', 'k': k, 'mask': rep,
                           'edges': [list(e) for e in decode(rep)],
                           'orbit_size': len(orbit)})
    assert len(result) == 25
    assert [sum(c['k'] == k for c in result) for k in (3, 4, 5, 6)] == [5, 9, 9, 2]
    assert [sum(c['orbit_size'] for c in result if c['k'] == k)
            for k in (3, 4, 5, 6)] == [455, 1365, 1581, 70]
    return result


if __name__ == '__main__':
    import json
    print(json.dumps(enumerate_cases(), indent=2))
