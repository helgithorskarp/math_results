"""Independent definition-level physical model and transport checks.

No producer, solver, model generator or clique-search import.
"""
from collections import Counter
from itertools import combinations
import json


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def points(word):
    return frozenset(p for p in range(18) if word >> p & 1)


def mask(ps):
    return sum(2 ** p for p in ps)


def orbit(ps, g):
    result = {ps}
    new = frozenset(g[p] for p in ps)
    while new != ps:
        need(new not in result, 'nonclosing physical orbit')
        result.add(new)
        new = frozenset(g[p] for p in new)
    return frozenset(result)


def packing(words, size):
    need(len(words) == len(set(words)) == size, 'wrong literal packing cardinality')
    triples = set()
    for word in words:
        ps = points(word)
        need(0 <= word < 2 ** 18 and len(ps) == 5, 'nonphysical word')
        for triple in combinations(sorted(ps), 3):
            need(triple not in triples, 'repeated literal triple')
            triples.add(triple)
    return triples


def full_model(g):
    physical = [frozenset(ps) for ps in combinations(range(18), 5)]
    orbits = {orbit(ps, g) for ps in physical}
    need(len(physical) == 8568 and Counter(map(len, orbits)) == {1: 3, 5: 1713}, 'full physical universe mismatch')
    long, short = [], []
    for ws in orbits:
        if any(len(a & b) >= 3 for a, b in combinations(ws, 2)):
            continue
        key = tuple(sorted(mask(ps) for ps in ws))
        (long if len(ws) == 5 else short).append(key)
    return sorted(long), sorted(short), physical


def transport_cover(g, roots, cover, seed):
    records = cover['point_transports']
    need([r['root_index'] for r in records] == list(range(len(roots))), 'omitted, duplicate or reordered raw-root transport')
    need(cover['seed_words'] == seed, 'transport seed differs from actual proof root')
    for r in records:
        p = tuple(r['seed_to_root_point_map'])
        inv = tuple(r['root_to_seed_point_map'])
        need(sorted(p) == list(range(18)) and p[0] == 0 and
             all(p[g[i]] == g[p[i]] and inv[p[i]] == i for i in range(18)), 'false bijective commuting/inverse point map')
        image = sorted(mask(frozenset(p[i] for i in points(w))) for w in seed)
        need(image == roots[r['root_index']]['words'], 'point map does not produce target literal star')
        packing(image, 20)
