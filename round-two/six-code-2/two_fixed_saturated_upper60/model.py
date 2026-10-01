"""Exact weighted word-orbit packing for cycle type2^8*1^2.

six-code-2, researcher. Exact orbit carrier and literal witness checker for the scoped
both-fixed-points-saturated theorem. Standard-library generator and checker.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json

G = tuple(v ^ 1 if v < 16 else v for v in range(18))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def mask(points):
    return sum(1 << v for v in points)


def points(word):
    return tuple(v for v in range(18) if word >> v & 1)


def image(word):
    return sum(1 << G[v] for v in points(word))


def triples(word):
    return tuple(mask(t) for t in combinations(points(word), 3))


def canonical(t):
    return min(t, image(t))


def orbit_carrier():
    resources = tuple(sorted({canonical(mask(t)) for t in combinations(range(18), 3)}))
    resource_index = {t: i for i, t in enumerate(resources)}
    rows = []
    for word in sorted(mask(w) for w in combinations(range(18), 5)):
        conjugate = image(word)
        if word > conjugate:
            continue
        orbit = tuple(sorted({word, conjugate}))
        occupied = Counter(t for w in orbit for t in triples(w))
        if max(occupied.values()) > 1:
            continue
        used = tuple(sorted({resource_index[canonical(t)] for t in occupied}))
        rows.append(dict(representative=word, words=orbit, weight=len(orbit), resources=used,
                         replications=tuple(sum(w >> v & 1 for w in orbit) for v in range(18))))
    require(len(resources) == 416 and len(rows) == 3416, 'whole carrier counts')
    require(sum(r['weight'] == 1 for r in rows) == 56 and
            sum(r['weight'] == 2 for r in rows) == 3360, 'whole orbit weights')
    require(sum(image(t) == t for t in resources) == 16, 'fixed triple count')
    return resources, tuple(rows)


def check_code(words, minimum=0):
    require(isinstance(words, (list, tuple)), 'word container')
    words = tuple(words)
    require(len(words) == len(set(words)) >= minimum and all(type(w) is int and
            0 <= w < 1 << 18 and w.bit_count() == 5 for w in words), 'invalid five-subset code')
    # Direct definition check, not a replay of canonical triple resources.
    literal = tuple(frozenset(points(w)) for w in words)
    require(all(len(a & b) <= 2 for a, b in combinations(literal, 2)), 'code repeats a triple')
    require({frozenset(G[v] for v in w) for w in literal} == set(literal), 'code not invariant')
    replications = tuple(sum(v in w for w in literal) for v in range(18))
    require(max(replications, default=0) <= 20, 'point cap violated')
    return dict(words=len(words), replications=replications,
                fixed_words=sum(image(w) == w for w in words), minimum_distance=6 if len(words) > 1 else None)


def residual(anchor, resources, rows):
    check_code(anchor)
    occupied = {canonical(t) for w in anchor for t in triples(w)}
    output = tuple(row for row in rows if not {resources[i] for i in row['resources']} & occupied)
    return output


def verify_literal_model(resources, rows):
    """Scan all actual subsets and compare each closed orbit and resource."""
    literal_resources = {frozenset({tuple(t), tuple(sorted(G[v] for v in t))})
                         for t in combinations(range(18), 3)}
    # Lexicographic tuple order differs from mask order. Compare whole actual orbits.
    require({frozenset({tuple(points(t)), tuple(sorted(G[v] for v in points(t)))}) for t in resources}
            == literal_resources, 'literal triple orbit universe')
    other = {}
    for word in combinations(range(18), 5):
        moved = tuple(sorted(G[v] for v in word))
        orbit = tuple(sorted({word, moved}))
        if word != min(orbit):
            continue
        covered = Counter(t for w in orbit for t in combinations(w, 3))
        if max(covered.values()) > 1:
            continue
        key = min(mask(w) for w in orbit)
        used = {min(mask(t), mask(tuple(sorted(G[v] for v in t)))) for t in covered}
        other[key] = (tuple(sorted(mask(w) for w in orbit)), used)
    require(len(other) == len(rows), 'literal candidate count')
    for row in rows:
        orbit, used = other[row['representative']]
        require(orbit == row['words'] and used == {resources[i] for i in row['resources']},
                'literal row differs entrywise')
