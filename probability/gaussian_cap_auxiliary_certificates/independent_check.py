#!/usr/bin/env python3
"""Separate obstruction audit via rational row space, without the disk chain.

This checker covers Theorem B. The positive-class interval certificate and
motion control are covered by verify.py and the written universal proof.
"""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def phi_product_sum(u, v):
    # Expand the three products and reduce phi^2=phi+1 in one step.
    return (sum(a*c+b*d for (a, b), (c, d) in zip(u, v)),
            sum(a*d+b*c+b*d for (a, b), (c, d) in zip(u, v)))


def row_combination(rows, target):
    """Exact row elimination with an explicit reconstruction vector."""
    basis = []
    count = len(rows)
    width = len(target)
    for index, row in enumerate(rows):
        work = list(map(Q, row))
        combo = [Q(j == index) for j in range(count)]
        for pivot, vector, coefficients in basis:
            factor = work[pivot]
            work = [a-factor*b for a, b in zip(work, vector)]
            combo = [a-factor*b for a, b in zip(combo, coefficients)]
        pivot = next((j for j, value in enumerate(work) if value), None)
        if pivot is not None:
            factor = work[pivot]
            basis.append((pivot, [x/factor for x in work], [x/factor for x in combo]))
    work = list(map(Q, target))
    dual = [Q(0)]*count
    for pivot, vector, coefficients in basis:
        factor = work[pivot]
        work = [a-factor*b for a, b in zip(work, vector)]
        dual = [a+factor*b for a, b in zip(dual, coefficients)]
    require(not any(work), 'half-cycle is not forced to vanish')
    require(all(sum(dual[j]*rows[j][k] for j in range(count)) == target[k]
                for k in range(width)), 'row-space dual failed direct substitution')
    return len(basis), dual


def audit(path):
    data = json.loads(path.read_text())['icosahedron']
    points = data['vertices_phi_basis']
    require(len(points) == 12 and all(len(p) == 3 for p in points), 'wrong dimension')
    require(all(phi_product_sum(p, p) == (2, 1) for p in points), 'wrong normalization')
    anti = []
    for p in points:
        opposite = [[-a, -b] for a, b in p]
        matches = [i for i, q in enumerate(points) if q == opposite]
        require(len(matches) == 1, 'missing or repeated antipode')
        anti.append(matches[0])
    require(anti == data['antipodes'], 'antipode metadata mismatch')
    edges = [e for e in combinations(range(12), 2)
             if phi_product_sum(points[e[0]], points[e[1]]) == (0, 1)]
    require(len(edges) == 30 and edges == list(map(tuple, data['edges'])), 'incorrect edge list')
    faces = [t for t in combinations(range(12), 3)
             if all(e in edges for e in combinations(t, 2))]
    require(len(faces) == 20 and faces == list(map(tuple, data['faces'])), 'incorrect triangle list')
    edge_number = {e: i for i, e in enumerate(edges)}

    def directed_edge(a, b):
        vector = [Q(0)]*len(edges)
        pair = tuple(sorted((a, b)))
        require(pair in edge_number, 'nonedge in angular identity')
        vector[edge_number[pair]] = Q(1 if a < b else -1)
        return vector

    def sum_vectors(vectors):
        return [sum(values) for values in zip(*vectors)]

    rows = [sum_vectors([directed_edge(a, b), directed_edge(b, c), directed_edge(c, a)])
            for a, b, c in faces]
    antipodal_equations = 0
    for a, b in edges:
        opposite = tuple(sorted((anti[a], anti[b])))
        if (a, b) < opposite:
            rows.append([x-y for x, y in zip(directed_edge(anti[a], anti[b]), directed_edge(a, b))])
            antipodal_equations += 1
    require(antipodal_equations == 15, 'incomplete antipodal-edge coverage')
    cycle = data['cycle']
    require(len(cycle) == len(set(cycle)) == 10, 'invalid half-cycle path')
    require(all(anti[cycle[i]] == cycle[(i+5) % 10] for i in range(10)),
            'path lacks antipodal half-shift')
    for i in range(10):
        directed_edge(cycle[i], cycle[(i+1) % 10])
    half = sum_vectors([directed_edge(cycle[i], cycle[i+1]) for i in range(5)])
    rank, dual = row_combination(rows, half)
    # The separate proof needs only the path, triangles and antipodal edges.
    # It deliberately never reads disk_triangles.
    sparse = [[j, str(c)] for j, c in enumerate(dual) if c]
    digest = hashlib.sha256(json.dumps(sparse, separators=(',', ':')).encode()).hexdigest()
    return {'status': 'SEPARATE_WINDING_ROWSPACE_PASS', 'edge_variables': len(edges),
            'triangle_equations': len(faces), 'antipodal_equations': antipodal_equations,
            'equation_rank': rank, 'half_cycle_dual_terms': len(sparse),
            'half_cycle_dual': sparse, 'dual_sha256': digest,
            'scope': 'Theorem B finite obligations; circle-angle interpretation remains written proof'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path,
                        default=Path(__file__).with_name('CERTIFICATE.json'))
    args = parser.parse_args()
    print(json.dumps(audit(args.certificate), sort_keys=True))
