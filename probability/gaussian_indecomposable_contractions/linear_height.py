#!/usr/bin/env python3
"""Exact small controls for LINEAR_HEIGHT.md; not a Gaussian sign oracle."""

import argparse
from collections import deque
from fractions import Fraction as F
from itertools import combinations
import json
from math import comb
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def det(a, b, c):
    return dot(a, cross(b, c))


def dist2(a, b):
    z = sub(a, b)
    return dot(z, z)


def distances(points):
    return tuple(dist2(points[i], points[j])
                 for i, j in combinations(range(len(points)), 2))


def below(a, b):
    return all(x <= y for x, y in zip(a, b))


def points(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def reflect(x, face):
    a, b, c = face
    normal = cross(sub(b, a), sub(c, a))
    norm = dot(normal, normal)
    require(norm > 0, 'degenerate face')
    scale = 2*dot(sub(x, a), normal)/norm
    return tuple(z-scale*n for z, n in zip(x, normal))


def transport(x, source_tet, placed_tet):
    """Affine interpolation, independently of the face-reflection rule."""
    a, b, c = (sub(p, source_tet[0]) for p in source_tet[1:])
    t = sub(x, source_tet[0])
    volume = det(a, b, c)
    require(volume != 0, 'degenerate interpolation cell')
    coefficients = (det(t, b, c)/volume, det(a, t, c)/volume,
                    det(a, b, t)/volume)
    basis = [sub(p, placed_tet[0]) for p in placed_tet[1:]]
    return tuple(placed_tet[0][j] + sum(coefficients[i]*basis[i][j]
                 for i in range(3)) for j in range(3))


def framework(source, target, cells):
    require(len(source) == len(target), 'endpoint label mismatch')
    require(len(source) >= 4 and 1 <= len(cells) <= 12,
            'control requires at least four labels and 1..12 cells')
    require(all(len(p) == 3 for p in source+target), 'dimension mismatch')
    require(len(set(tuple(sorted(t)) for t in cells)) == len(cells),
            'duplicate cells')
    require(all(len(t) == 4 and len(set(t)) == 4 for t in cells),
            'invalid tetrahedron labels')
    require(set().union(*(set(t) for t in cells)) == set(range(len(source))),
            'cells must cover precisely the declared labels')
    mesh_edges = set()
    for t in cells:
        require(det(*(sub(source[i], source[t[0]]) for i in t[1:])) != 0,
                'degenerate tetrahedron')
        mesh_edges.update(tuple(sorted(e)) for e in combinations(t, 2))
    for i, j in mesh_edges:
        require(dist2(source[i], source[j]) == dist2(target[i], target[j]),
                'endpoint changed a mesh edge')
    require(below(distances(target), distances(source)),
            'endpoints are not a contraction')
    adjacent = []
    for i, j in combinations(range(len(cells)), 2):
        face = tuple(sorted(set(cells[i]) & set(cells[j])))
        if len(face) != 3:
            continue
        u = next(iter(set(cells[i])-set(face)))
        w = next(iter(set(cells[j])-set(face)))
        reflected = reflect(source[w], [source[k] for k in face])
        low, high = sorted((dist2(source[u], source[w]),
                            dist2(source[u], reflected)))
        require(low < high, 'binary opposite distances collapsed')
        a, b, c = (source[k] for k in face)
        normal = cross(sub(b, a), sub(c, a))
        norm = dot(normal, normal)
        hu2 = dot(sub(source[u], a), normal)**2/norm
        hw2 = dot(sub(source[w], a), normal)**2/norm
        require((high-low)**2 == 16*hu2*hw2, 'height gap identity')
        changed = dist2(source[u], source[w]) != dist2(target[u], target[w])
        adjacent.append({'i': i, 'j': j, 'face': face, 'pair': (u, w),
                         'low': low, 'high': high, 'cost': int(changed)})

    # Minimum zero/one cost tree: zero-edge components are joined first.
    parent = list(range(len(cells)))

    def root(i):
        while parent[i] != i:
            i = parent[i]
        return i

    tree = []
    for edge in sorted(adjacent, key=lambda e: (e['cost'], e['i'], e['j'])):
        i, j = root(edge['i']), root(edge['j'])
        if i != j:
            parent[j] = i
            tree.append(edge)
    require(len(tree) == len(cells)-1, 'disconnected facet graph')
    zero_components = 1+sum(e['cost'] for e in tree)
    order, reached = [], {0}
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for edge in tree:
            if i not in (edge['i'], edge['j']):
                continue
            j = edge['j'] if edge['i'] == i else edge['i']
            if j not in reached:
                reached.add(j)
                queue.append(j)
                order.append((i, j, edge))
    introduced = set(cells[0])
    selected = []
    for i, j, edge in order:
        new = next(iter(set(cells[j])-set(edge['face'])))
        if new not in introduced:
            selected.append(edge)
            introduced.add(new)
    require(introduced == set(range(len(source))), 'missing introduced label')
    require(len(selected) == len(source)-4, 'wrong number of selected bits')
    return mesh_edges, order, selected, zero_components


def all_placements(source, cells, mesh_edges, order):
    partial = [{i: source[i] for i in cells[0]}]
    for i, j, edge in order:
        new = next(iter(set(cells[j])-set(edge['face'])))
        next_partial = []
        for placed in partial:
            continued = transport(source[new], [source[k] for k in cells[i]],
                                  [placed[k] for k in cells[i]])
            folded = reflect(continued, [placed[k] for k in edge['face']])
            require(continued != folded, 'child lost nondegeneracy')
            for candidate in (continued, folded):
                if new in placed and placed[new] != candidate:
                    continue
                extended = dict(placed)
                extended[new] = candidate
                next_partial.append(extended)
        partial = next_partial
    result = []
    for placed in partial:
        candidate = tuple(placed[i] for i in range(len(source)))
        if all(dist2(candidate[i], candidate[j]) == dist2(source[i], source[j])
               for i, j in mesh_edges):
            result.append(candidate)
    require(len(set(result)) == len(result), 'duplicate generated placements')
    return result


def encoding(placement, selected):
    result = []
    for e in selected:
        u, w = e['pair']
        bit = (dist2(placement[u], placement[w])-e['low'])/(e['high']-e['low'])
        require(bit in (0, 1), 'invalid binary measurement')
        result.append(int(bit))
    return tuple(result)


def audit_fixture(name, source, target, cells, expected_states, expected_height):
    mesh_edges, order, selected, components = framework(source, target, cells)
    placements = all_placements(source, cells, mesh_edges, order)
    coded = [(encoding(z, selected), distances(z), z) for z in placements]
    require(len({x[0] for x in coded}) == len(coded), 'encoding not injective')
    require(len({x[1] for x in coded}) == len(coded), 'duplicate distance states')
    lower, upper = distances(target), distances(source)
    bp, bq = encoding(source, selected), encoding(target, selected)
    r = sum(bp)-sum(bq)
    require(below(bq, bp), 'endpoint bits reversed')
    require(0 <= r <= min(len(source)-4, components-1), 'wrong refined bound')
    interval = sorted((x for x in coded if below(lower, x[1]) and below(x[1], upper)))
    require(len(interval) == expected_states, 'unexpected interval size')
    require(len(interval) <= 2**r, 'interval exceeds bit budget')
    require(any(d == lower for _, d, _ in interval), 'target state missing')
    require(any(d == upper for _, d, _ in interval), 'source state missing')
    order_checks = 0
    for ba, da, _ in coded:
        for bb, db, _ in coded:
            if below(da, db):
                require(below(ba, bb), 'nonmonotone encoding')
                require(da == db or sum(ba) < sum(bb), 'nonstrict potential')
                order_checks += 1
    longest = {}
    covers = []
    # Increasing integer potential gives a topological order, checked above.
    for bits, d, _ in sorted(interval, key=lambda x: (sum(x[0]), x[0])):
        predecessors = [other for other in interval if other[1] != d and below(other[1], d)]
        longest[bits] = 0 if not predecessors else 1+max(longest[b] for b, _, _ in predecessors)
        for b, e, _ in predecessors:
            if not any(e != f != d and below(e, f) and below(f, d)
                       for _, f, _ in interval):
                covers.append([''.join(map(str, bits)), ''.join(map(str, b))])
    height = max(longest.values())
    require(height == expected_height and height <= r, 'chain height mismatch')
    # A concrete check that bitwise decrease is not sufficient for contraction.
    false_converses = sorted([''.join(map(str, b)) for b, d, _ in coded
                             if below(b, bp) and not below(d, upper)])
    return {'name': name, 'vertices': len(source), 'tetrahedra': len(cells),
            'all_framework_states': len(coded), 'selected_pairs': [list(e['pair']) for e in selected],
            'binary_distance_values': [[str(e['low']), str(e['high'])] for e in selected],
            'zero_edge_components': components, 'r': r, 'interval_states': len(interval),
            'longest_strict_chain': height, 'covers': sorted(covers),
            'order_comparisons_checked': order_checks,
            'bit_decrease_without_contraction': false_converses,
            'states': [{'bits': ''.join(map(str, b)),
                        'distance_vector': [str(z) for z in d]} for b, d, _ in interval]}


def ceil_log2_fraction(x):
    require(x >= 1, 'logarithm budget requires x>=1')
    k = max(0, x.numerator.bit_length()-x.denominator.bit_length())
    while F(2**k) < x:
        k += 1
    while k > 0 and F(2**(k-1)) >= x:
        k -= 1
    return k


def budget(n, delta=F(1, 1000)):
    require(isinstance(n, int) and not isinstance(n, bool) and 1 <= n <= 256,
            'display budget requires 1<=N<=256')
    require(0 < delta <= 1, 'delta must lie in (0,1]')
    h = 512*2**n*(n+6)+3*n+comb(n, 3)+6
    m = 12*h*sum(comb(h, j) for j in range(4))
    digits = ceil_log2_fraction(8*(m-1)/delta)
    coarse = 47+4*n+4*ceil_log2_fraction(F(n+6))+ceil_log2_fraction(1/delta)
    gap = delta/(2*(m-1))
    require(m < 2**44*16**n*(n+6)**4, 'coarse mesh bound failed')
    require(F(1, 2**digits) <= gap/4, 'insufficient absolute-error digits')
    require(digits <= coarse, 'coarse digit bound failed')
    return {'N': n, 'delta': str(delta), 'M_N': m, 'labels_at_most': m+3,
            'minimum_mass': str(delta/(2*(m+3)*(1+delta))),
            'minimum_negative_gap': str(gap), 'absolute_error_digits': digits,
            'coarse_absolute_error_digits': coarse}


def record():
    core = points([(0, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1)])
    star = core+points([(1, -1, -1), (-1, 1, -1), (-1, -1, 1)])
    target = core+points([(-1, -1, -1)]*3)
    cells = ((0, 1, 2, 3), (0, 2, 3, 4), (0, 1, 3, 5), (0, 1, 2, 6))
    partial_target = star[:4]+target[4:5]+star[5:]
    joint = points([(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
                    (-1, 10, 0), (-10, -1, 0)])
    joint_target = joint[:4]+points([(1, 10, 0), (-10, 1, 0)])
    joint_cells = ((0, 1, 2, 3), (0, 2, 3, 4), (0, 1, 3, 5))
    cycle = points([(0, 0, -1), (0, 0, 1), (1, 0, 0), (0, 1, 0), (-1, -1, 0)])
    cycle_cells = ((0, 1, 2, 3), (0, 1, 3, 4), (0, 1, 2, 4))
    fixtures = [
        audit_fixture('eight_states_height_three', star, target, cells, 8, 3),
        audit_fixture('two_zero_dual_edges', star, partial_target, cells, 2, 1),
        audit_fixture('other_pairs_exclude_mixed_bits', joint, joint_target, joint_cells, 2, 1),
        audit_fixture('cycle_consistency', cycle, cycle, cycle_cells, 1, 0),
    ]
    require(fixtures[0]['r'] == 3 and len(fixtures[0]['covers']) == 12, 'cube control')
    require(fixtures[1]['zero_edge_components'] == 2, 'zero component control')
    require(fixtures[2]['bit_decrease_without_contraction'], 'missing false converse')
    require(fixtures[3]['all_framework_states'] == 1, 'cycle was not enforced')
    rejected = {}

    def reject(name, p, q, t):
        try:
            framework(p, q, t)
        except ValueError as error:
            rejected[name] = str(error)
        else:
            raise RuntimeError('damaged fixture accepted: '+name)

    degenerate = star[:4]+points([(0, -1, -1)])+star[5:]
    reject('zero_cell_height', degenerate, degenerate, cells)
    changed = points([(F(1, 10), 0, 0)])+target[1:]
    reject('changed_tight_edge', star, changed, cells)
    disjoint = core+tuple(tuple(x+10 for x in p) for p in core)
    reject('disconnected_framework', disjoint, disjoint, ((0, 1, 2, 3), (4, 5, 6, 7)))
    bad_target = joint[:4]+joint_target[4:5]+joint[5:]
    reject('bits_decrease_but_pair_expands', joint, bad_target, joint_cells)
    budget_checks = 0
    for delta in (F(1), F(1, 2), F(1, 10), F(1, 1000)):
        eps = delta/(2*(1+delta))
        require(-(1-eps)*delta+eps == -delta/2, 'endpoint perturbation budget')
        for v in range(5, 25):
            require(eps/v == delta/(2*v*(1+delta)), 'mass floor')
            for length in range(1, v-3):
                require(delta/(2*length) >= delta/(2*(v-4)), 'step gap')
                budget_checks += 1
    budgets = [budget(n) for n in (1, 4, 7, 10)]
    require(budgets[2]['absolute_error_digits'] == 93, 'seven-atom precision control')
    return {'status': 'LINEAR_CHAIN_HEIGHT_CONTROLS_PASS', 'fixtures': fixtures,
            'damaged_inputs_rejected': rejected, 'mass_gap_checks': budget_checks,
            'budgets': budgets,
            'scope': 'Exact small geometry and budget controls; universal proof pending independent review; no Gaussian sign.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--check', action='store_true')
    modes.add_argument('--record', action='store_true')
    modes.add_argument('--budget', type=int, metavar='N')
    args = parser.parse_args()
    if args.budget is not None:
        print(json.dumps(budget(args.budget), indent=2))
        return
    result = record()
    if args.record:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        expected = json.loads(Path(__file__).with_name('LINEAR_HEIGHT_EXPECTED.json').read_text())
        require(result == expected, 'expected record mismatch')
        print(result['status'])


if __name__ == '__main__':
    main()
