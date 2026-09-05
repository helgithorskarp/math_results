#!/usr/bin/env python3
"""Solver-free fresh coordinate parse, full pair scan, and colouring certificate.

This imports neither the search engine nor any earlier arithmetic module.
Multiplication uses explicit monomial exponent addition and square reduction.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
MONOMIALS = [(i & 1, (i >> 1) & 1, (i >> 2) & 1) for i in range(8)]
INDEX = {powers: i for i, powers in enumerate(MONOMIALS)}
PRIMES = (3, 5, 11)


def require(ok, detail):
    if not ok:
        raise ValueError(detail)


def multiply(left, right):
    result = [0] * 8
    for powers, x in zip(MONOMIALS, left):
        if not x:
            continue
        for other, y in zip(MONOMIALS, right):
            if not y:
                continue
            exponents = [a + b for a, b in zip(powers, other)]
            coefficient = x * y
            for prime, exponent in zip(PRIMES, exponents):
                coefficient *= prime ** (exponent // 2)
            result[INDEX[tuple(exponent % 2 for exponent in exponents)]] += coefficient
    return tuple(result)


def distance(first, second):
    x = tuple(a - b for a, b in zip(first[0], second[0]))
    y = tuple(a - b for a, b in zip(first[1], second[1]))
    return tuple(a + b for a, b in zip(multiply(x, x), multiply(y, y)))


def check_colour(vertices, colours, edges):
    require(len(colours) == len(vertices) and set(colours) <= set('0123'), 'colour domain')
    mapping = dict(zip(vertices, map(int, colours)))
    for u, v in edges:
        require(mapping[u] != mapping[v], ('monochromatic edge', u, v))
    return mapping


def audit():
    manifest = json.loads((HERE / 'manifest.json').read_text())
    for name, digest in manifest['geometry_inputs'].items():
        require(sha256((REPO / name).read_bytes()).hexdigest() == digest, ('coordinate input hash', name))
    for name, key in [('base_colouring.json', 'base_colouring_sha256'), ('certificate.json', 'certificate_sha256')]:
        require(sha256((HERE / name).read_bytes()).hexdigest() == manifest[key], ('certificate identity', name))
    cert = json.loads((HERE / 'certificate.json').read_text())
    expected = json.loads((HERE / 'expected.json').read_text())
    base = json.loads((HERE / 'base_colouring.json').read_text())
    require(cert['original_omission'] == base['omitted_original'] == 40, 'original omission')
    extras = cert['completion_labels']
    require(extras == sorted(set(extras)) == expected['completion_labels'] and len(extras) == 24, 'completion labels')
    points = {}
    rows = [line for line in (REPO / 'hadwiger_nelson_parts509_completion_census_degree9/points.tsv').read_text().splitlines()
            if line and not line.startswith('#')]
    require(len(rows) == 509, 'original coordinate count')
    for v, line in enumerate(rows):
        coordinates = [3 * int(s) for s in line.split()]
        require(len(coordinates) == 16, 'original coordinate width')
        points[v] = (tuple(coordinates[:8]), tuple(coordinates[8:]))
    pool = json.loads((REPO / 'hadwiger_nelson_parts509_swap_closure/completion_points.json').read_text())['points']
    for v in extras:
        require(509 <= v < 509 + len(pool), 'completion index')
        coordinates = []
        for axis in ('x', 'y'):
            values = [Fraction(c) * 288 for c in pool[v - 509][axis]]
            require(len(values) == 8 and all(c.denominator == 1 for c in values), 'completion scaling')
            coordinates.append(tuple(c.numerator for c in values))
        points[v] = tuple(coordinates)
        require(all(points[v][a][i] == 0 for a in (0, 1) for i in (2, 3, 6, 7)), 'no sqrt5 coefficient')
    originals = sorted(set(range(509)) - {40})
    vertices = sorted(originals + extras)
    require(len(vertices) == len({points[v] for v in vertices}) == 532, 'distinct graph points')
    U = sorted((set(range(374)) - {40}) | set(extras))
    require(sha256(json.dumps(U, separators=(',', ':')).encode()).hexdigest() == cert['seed_U_sha256'], 'native selected labels')
    unit = (288 * 288,) + (0,) * 7
    edges = [(u, v) for u, v in combinations(vertices, 2) if distance(points[u], points[v]) == unit]
    edge_hash = sha256(''.join(f'{u},{v}\n' for u, v in edges).encode()).hexdigest()
    require(len(edges) == expected['seed_edges'] == 2580 and edge_hash == expected['seed_edge_sha256'], 'complete unit graph')
    final_colours = check_colour(vertices, cert['colouring'], edges)
    require(final_colours[0] == 0, 'native colour normalization')
    base_edges = [(u, v) for u, v in edges if u < 509 and v < 509]
    original_colours = check_colour(originals, base['colouring'], base_edges)
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    blocker_certificates = []
    original_degrees = {}
    for v in extras:
        neighbours = sorted(adj[v] & set(originals))
        if distance(points[v], points[40]) == unit:
            neighbours.append(40)
        neighbours.sort()
        require(neighbours == pool[v - 509]['neighbors'] and 4 <= len(neighbours) <= 6, 'original completion degree')
        original_degrees[v] = len(neighbours)
        by_colour = {c: sorted(u for u in neighbours if u != 40 and original_colours[u] == c) for c in range(4)}
        if all(by_colour.values()):
            blocker_certificates.append(dict(point=v, one_neighbour_per_colour=[by_colour[c][0] for c in range(4)]))
    require([r['point'] for r in blocker_certificates] == expected['seed_blockers'], 'five seed blockers')
    # A deliberately improper colouring must be rejected by the edge decoder.
    bad = list(cert['colouring'])
    u, v = edges[0]
    bad[vertices.index(v)] = bad[vertices.index(u)]
    rejected = False
    try:
        check_colour(vertices, ''.join(bad), edges)
    except ValueError as error:
        require('monochromatic edge' in str(error), 'wrong rejection reason')
        rejected = True
    require(rejected, 'bad colouring accepted')
    return dict(status='EXACT 532-POINT SUPPORT AND ALL ITS SUBGRAPHS FOUR-COLOURABLE',
                vertices=532, unit_edges=len(edges), unordered_pairs_checked=532 * 531 // 2,
                extra_pairs_to_omitted_original_checked=24, edge_sha256=edge_hash,
                original_vertices=508, completion_vertices=24, original_degree_by_completion=original_degrees,
                base_colouring_edges_checked=len(base_edges), full_colouring_edges_checked=len(edges),
                seed_blocker_certificates=blocker_certificates, malformed_colour_certificate_rejected=True,
                all_subgraphs_through_508_four_colourable=True, whole_1111_ambient_closed=False,
                native_solver_required=False, native_negative_proof_required=False, record_improvement=False,
                new_independent_author_review_claimed=False)


def controls():
    basis = [tuple(int(i == j) for i in range(8)) for j in range(8)]
    for i in range(8):
        squared = multiply(basis[i], basis[i])
        value = 1
        for bit, prime in enumerate(PRIMES):
            if i & (1 << bit):
                value *= prime
        require(squared == (value,) + (0,) * 7, 'basis square')
        for j in range(8):
            require(multiply(basis[i], basis[j]) == multiply(basis[j], basis[i]), 'basis commutativity')
    zero = (0,) * 8
    O = (zero, zero)
    X = ((288,) + (0,) * 7, zero)
    Y = ((144,) + (0,) * 7, (0, 144) + (0,) * 6)
    unit = (288 * 288,) + (0,) * 7
    require(all(distance(a, b) == unit for a, b in combinations((O, X, Y), 2)), 'unit equilateral control')
    require(distance(O, O) == zero, 'zero distance control')
    require(distance(O, (tuple(2 * c for c in X[0]), zero)) == (4 * 288 * 288,) + (0,) * 7, 'nonunit control')
    return dict(basis_squares=8, commutativity_pairs=64, unit_triangle_edges=3, zero_distance=1, nonunit_distance=1)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--report', type=Path)
    args = ap.parse_args()
    result = audit()
    result['controls'] = controls()
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.report:
        args.report.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
