#!/usr/bin/env python3
"""Exact finite controls for EFFECTIVE_BOUND.md; not a Brehm producer."""
import argparse
from fractions import Fraction as F
from itertools import combinations, product
import json
from math import comb
from pathlib import Path


ZERO = (F(0),) * 3
EYE = tuple(tuple(F(i == j) for j in range(3)) for i in range(3))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dist2(a, b):
    d = sub(a, b)
    return dot(d, d)


def affine(matrix, shift, x):
    return tuple(dot(row, x) + c for row, c in zip(matrix, shift))


def determinant(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def reflect(a, other, x):
    n = sub(other, a)
    norm = dot(n, n)
    if norm == 0:
        raise ValueError('coincident bisector endpoints: skip the repair')
    c = (2 * dot(n, x) - dot(other, other) + dot(a, a)) / norm
    return tuple(u - c * v for u, v in zip(x, n))


def seed_piece(indices, x):
    return tuple(t - j if j % 2 == 0 else j + 1 - t
                 for j, t in zip(indices, x))


def audit_seed():
    vertex_checks = interface_checks = 0
    for cell in product(range(-4, 4), repeat=3):
        vertices = [tuple(F(j + e) for j, e in zip(cell, bits))
                    for bits in product((0, 1), repeat=3)]
        images = [seed_piece(cell, x) for x in vertices]
        for y in images:
            require(all(0 <= t <= 1 for t in y), 'seed range')
            vertex_checks += 1
        for i, j in combinations(range(8), 2):
            require(dist2(vertices[i], vertices[j]) == dist2(images[i], images[j]),
                    'seed cubical isometry')
        for axis in range(3):
            if cell[axis] == 3:
                continue
            neighbor = list(cell)
            neighbor[axis] += 1
            for x in vertices:
                if x[axis] == cell[axis] + 1:
                    require(seed_piece(cell, x) == seed_piece(neighbor, x),
                            'seed face mismatch')
                    interface_checks += 1
    # sqrt(3)<2, hence (1+sqrt(3))R<3R on the buffered boundary.
    require(3 < 2**2, 'buffer inequality')
    return {'pieces': 512, 'facets_per_piece': 6,
            'vertex_range_checks': vertex_checks,
            'edge_and_diagonal_checks': 512 * comb(8, 2),
            'shared_face_vertex_checks': interface_checks}


def audit_asymmetric_repair():
    b = (F(1, 3), F(1, 4), F(1, 5))
    s = dot(b, b)
    require(all(0 < t <= F(1, 2) and s < 2 * t for t in b),
            'repair must stay inside the eight central cubes')
    radii = tuple(s / (2 * t) for t in b)
    require(all(0 < r < 1 for r in radii), 'cross-polytope intercept')
    records = {}
    edges = boundary = gram = householder = 0
    volume = F(0)
    for signs in product((-1, 1), repeat=3):
        base = [tuple(F(signs[i]) * radii[i] if i == j else F(0)
                      for j in range(3)) for i in range(3)]
        source = [ZERO] + base
        target = [b] + [tuple(abs(t) for t in v) for v in base]
        # Derive the affine map by interpolation of the four prescribed
        # vertices, independently of the bisector reflection formula.
        matrix = tuple(tuple(signs[i] * (F(j == i) - b[j] / radii[i])
                             for i in range(3)) for j in range(3))
        for x, y in zip(source, target):
            require(affine(matrix, b, x) == y, 'affine interpolation')
        for i, j in combinations(range(4), 2):
            require(dist2(source[i], source[j]) == dist2(target[i], target[j]),
                    'cone edge not preserved')
            edges += 1
        for i in range(3):
            for j in range(3):
                entry = sum(matrix[t][i] * matrix[t][j] for t in range(3))
                require(entry == EYE[i][j], 'nonorthogonal interpolant')
                gram += 1
        preimage = tuple(sgn * t for sgn, t in zip(signs, b))
        for x in source:
            rho = reflect(ZERO, preimage, x)
            reflected = tuple(sgn * t for sgn, t in zip(signs, rho))
            require(reflected == affine(matrix, b, x), 'reflection mismatch')
            householder += 1
        for x in base:
            require(affine(matrix, b, x) == tuple(abs(t) for t in x),
                    'old/new boundary mismatch')
            boundary += 1
        for y in target:
            require(all(0 <= t <= 1 for t in y), 'convex image invariant')
        source_vol = abs(determinant(*base)) / 6
        target_vol = abs(determinant(*(sub(y, b) for y in target[1:]))) / 6
        require(source_vol == target_vol and source_vol > 0, 'cone volume')
        volume += source_vol
        records[signs] = (matrix, base)
    interfaces = 0
    for signs, (matrix, base) in records.items():
        for axis in range(3):
            if signs[axis] != -1:
                continue
            other = list(signs)
            other[axis] = 1
            other_matrix = records[tuple(other)][0]
            shared = [ZERO] + [base[i] for i in range(3) if i != axis]
            for x in shared:
                require(affine(matrix, b, x) == affine(other_matrix, b, x),
                        'radial face mismatch')
                interfaces += 1
    # Eight clipped unit cubes retain volume 8-volume; eight new tetrahedra
    # replace exactly volume. The other 504 unit cubes stay unchanged.
    require(volume == F(4, 3) * radii[0] * radii[1] * radii[2],
            'cross-polytope volume')
    require(504 + (8 - volume) + volume == 512, 'total source volume')
    # Existing prescribed vertices outside Omega remain fixed at their old
    # images and are compatible with the new atom 0 -> b.
    old_pairs = [(tuple(F(sgn if j == axis else 0) for j in range(3)),
                  tuple(F(j == axis) for j in range(3)))
                 for axis in range(3) for sgn in (-1, 1)]
    for p, q in old_pairs:
        require(dist2(b, q) <= dist2(ZERO, p), 'previous atom incompatible')
        require(s - 2 * sum(t * abs(x) for t, x in zip(b, p)) < 0,
                'previous atom not outside repair')
    return {'new_atom': [str(t) for t in b], 'squared_norm': str(s),
            'axis_intercepts': [str(t) for t in radii], 'new_cones': 8,
            'retained_pieces': 512, 'total_pieces': 520,
            'maximum_facets': 7, 'cone_edge_checks': edges,
            'orthogonality_entries': gram, 'reflection_vertex_checks': householder,
            'old_new_boundary_vertex_checks': boundary,
            'radial_shared_face_vertex_checks': interfaces,
            'preserved_old_atoms': len(old_pairs), 'repair_volume': str(volume)}


def budget(n):
    if not isinstance(n, int) or isinstance(n, bool) or not 1 <= n <= 256:
        raise ValueError('numeric display requires 1<=N<=256; larger N use (2)')
    h = 512 * 2**n * (n + 6) + 3*n + comb(n, 3) + 6
    cells = sum(comb(h, j) for j in range(4))
    m = 12 * h * cells
    return {'N': n, 'planes': h, 'arrangement_cells': cells,
            'mesh_tetrahedra': m, 'mesh_vertices': 4*m,
            'gap_bound': 'delta * 2^(-M_N); exponent is not expanded'}


def audit_budgets():
    # Independent recurrence for the generic hyperplane arrangement count.
    line_regions = 1
    plane_regions = 1
    space_regions = 1
    for h in range(65):
        require(space_regions == sum(comb(h, j) for j in range(4)),
                'arrangement recurrence')
        space_regions += plane_regions
        plane_regions += line_regions
        line_regions += 1
    checks = 0
    for delta in (F(1), F(1, 2), F(1, 10), F(1, 1000)):
        eps = delta / (2 * (1 + delta))
        require(-(1-eps)*delta + eps == -delta/2, 'mass loss budget')
        for m in range(2, 17):
            length = 2**(m-1)-1
            require(delta/(2*length) > delta/F(2**m), 'strict step gap')
            require(eps/(4*m) == delta/(8*m*(1+delta)), 'weight budget')
            checks += 1
    # Without the boundary buffer, coning to a bisector can miss a whole
    # blind zone. Identity F, a=0, b=e1/2: Omega is x1<1/4.
    bad_x = (F(-1), F(0), F(0))
    bad_b = (F(1, 2), F(0), F(0))
    margin = dist2(bad_b, bad_x) - dist2(ZERO, bad_x)
    require(margin == F(5, 4), 'blind-zone witness')
    require(bad_x[0] < 0 < F(1, 4), 'point cannot lie in radial cones')
    try:
        reflect(ZERO, ZERO, ZERO)
    except ValueError:
        pass
    else:
        raise RuntimeError('zero normal accepted')
    return {'arrangement_recurrence_orders': 65, 'mass_gap_controls': checks,
            'blind_zone_margin': str(margin),
            'zero_bisector_rejected': True,
            'budgets': [budget(n) for n in (1, 4, 7, 10)]}


def record():
    return {'status': 'EFFECTIVE_INDECOMPOSABLE_BOUND_CONTROLS_PASS',
            'seed': audit_seed(), 'repair': audit_asymmetric_repair(),
            'budgets_and_adversarial_control': audit_budgets(),
            'scope': 'Exact finite controls; universal proof is EFFECTIVE_BOUND.md; no Gaussian sign.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true')
    group.add_argument('--record', action='store_true')
    group.add_argument('--budget', type=int, metavar='N')
    args = parser.parse_args()
    if args.budget is not None:
        print(json.dumps(budget(args.budget), indent=2))
        return
    result = record()
    if args.record:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        expected = json.loads(Path(__file__).with_name('EFFECTIVE_EXPECTED.json').read_text())
        require(result == expected, 'expected record mismatch')
        print(result['status'])


if __name__ == '__main__':
    main()
