#!/usr/bin/env python3
"""Exact source gate for host-conditioned odd-cycle compression; no SAT solver."""
from pathlib import Path
from fractions import Fraction
from itertools import combinations
from collections import Counter
from math import gcd
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'hadwiger_nelson_parts509_heule_union_minimum/aligned_510.json'
SOURCE_SHA256 = '84456269b4acb9fa911164f7148eb227e5f30835f03d8cb5d46d6f9602fd8e5b'
RADICALS = (1, 3, 5, 15, 11, 33, 55, 165)
SCALE = 288


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sparse_norm(delta):
    """Use squarefree radicands and gcd reduction, not subset-mask products."""
    result = {}
    for axis in (delta[:8], delta[8:]):
        terms = [(d, c) for d, c in zip(RADICALS, axis) if c]
        for d, x in terms:
            for e, y in terms:
                common = gcd(d, e)
                rad = d * e // (common * common)
                result[rad] = result.get(rad, 0) + common * x * y
    return {d: c for d, c in result.items() if c}


def dense_norm(delta):
    """Separate subset-mask multiplication for entrywise arithmetic comparison."""
    result = [0] * 8
    for axis in (delta[:8], delta[8:]):
        for i, x in enumerate(axis):
            if x:
                for j, y in enumerate(axis):
                    if y:
                        result[i ^ j] += x * y * RADICALS[i & j]
    return {d: c for d, c in zip(RADICALS, result) if c}


def read_points():
    data = SOURCE.read_bytes()
    require(hashlib.sha256(data).hexdigest() == SOURCE_SHA256, 'source pin')
    rows = json.loads(data)['aligned_H']
    points = []
    for row in rows:
        require(len(row) == 2 and all(len(axis) == 8 for axis in row), 'coordinate shape')
        scaled = [Fraction(c) * SCALE for axis in row for c in axis]
        require(all(c.denominator == 1 for c in scaled), 'exact common scale')
        points.append(tuple(map(int, scaled)))
    require(len(points) == len(set(points)) == 510, '510 distinct points')
    return points


def verify():
    points = read_points()
    edges = []
    neighbours = [set() for _ in points]
    checked = 0
    for i, j in combinations(range(len(points)), 2):
        delta = tuple(x - y for x, y in zip(points[i], points[j]))
        a, b = sparse_norm(delta), dense_norm(delta)
        require(a == b, 'distance coefficient comparison')
        checked += 1
        if a == {1: SCALE * SCALE}:
            edges.append([i, j])
            neighbours[i].add(j)
            neighbours[j].add(i)
    degree4 = [i for i, n in enumerate(neighbours) if len(n) == 4]
    degree4_edges = [[i, j] for i, j in edges if i in degree4 and j in degree4]
    require(degree4 == [139, 144, 316, 319, 322, 325, 328, 331], 'degree-four labels')
    require(not degree4_edges, 'degree-four independence')
    require(len(edges) == 2504, 'complete strict edge count')
    edge_bytes = (json.dumps(edges, separators=(',', ':')) + '\n').encode()
    return {
        'status': 'NO_DEGREE_FOUR_ODD_CYCLE_IN_FIXED_HEULE510',
        'source_coordinate_sha256': SOURCE_SHA256,
        'points': len(points),
        'complete_unit_edges': len(edges),
        'unordered_pairs_checked': checked,
        'distance_representations_agree_on_every_pair': True,
        'edge_sha256': hashlib.sha256(edge_bytes).hexdigest(),
        'degree_histogram': {str(k): v for k, v in sorted(Counter(map(len, neighbours)).items())},
        'degree4_vertices': degree4,
        'degree4_neighbours': {str(i): sorted(neighbours[i]) for i in degree4},
        'degree4_induced_edges': degree4_edges,
        'eligible_odd_cycle_components': 0,
        'new_physical_supports': 0,
        'new_solver_queries': 0,
        'record_candidate': False,
    }


if __name__ == '__main__':
    result = verify()
    expected = HERE / 'expected.json'
    if expected.exists():
        require(result == json.loads(expected.read_text()), 'expected output')
    print(json.dumps(result, indent=2))
