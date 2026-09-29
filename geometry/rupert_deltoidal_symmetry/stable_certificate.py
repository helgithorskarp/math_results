#!/usr/bin/env python3
"""Exact stable-contact coverage outside 45 exceptional unoriented axes.

Python 3.11+, standard library only. All geometric decisions use Q(sqrt(5)).
The choices in stable_data.py are checked, not trusted. See stable_proof.md
for the perturbation, neighborhood, compactness, and reverse-local arguments.
"""

import argparse
from collections import deque
from copy import deepcopy
from itertools import product
import json

from verify import (Q5, S, PHI, ZERO, vec, vertices, dot, cross, sub, add,
                    mul, convex_hull_2d, self_check)
from orientation_certificate import (CERTIFICATES, CORNER, build_cells,
                                     determinant, row_at, verify_orientation)
from stable_data import CELL_EXPOSURES, EDGE_CERTIFICATES, VERTEX_CERTIFICATES


SECOND = vec(((3 * S - 5) / 10, (5 - S) / 10, 1))
WALLS = [vec((1, 0, 0)), vec((0, 1, 0)), vec((-PHI, -PHI**2, 1))]


def strata(polygons):
    nodes = sorted(set(v for p in polygons for v in p))
    edges = sorted(set(tuple(sorted((p[j], p[(j + 1) % len(p)])))
                       for p in polygons for j in range(len(p))))
    assert len(nodes) == 14 and len(edges) == 25
    assert nodes[0] == CORNER and nodes[3] == SECOND
    assert SECOND == mul(1 / (1 + 3 * PHI), vec((1, PHI, 1 + 3 * PHI)))
    return nodes, edges


def exposing_chord(V, chord, j, endpoints):
    """An affine gap is positive throughout the region's relative interior."""
    a, b = chord
    assert a != b and all(0 <= k < len(V) for k in (a, b, j))
    for k, w in enumerate(V):
        if k == j:
            continue
        gaps = [dot(cross(sub(V[b], V[a]), u), sub(V[j], w))
                for u in endpoints]
        assert all(g.sign() >= 0 for g in gaps)
        assert any(g.sign() > 0 for g in gaps)
    return (len(V) - 1) * len(endpoints)


def edge_rows(V, contact, endpoints):
    a, b, j = contact
    assert a != b and all(0 <= k < len(V) for k in (a, b, j))
    rows, supports = [], []
    for u in endpoints:
        n = cross(sub(V[b], V[a]), u)
        support = dot(n, V[j])
        assert support.sign() >= 0
        assert dot(n, V[a]) == support == dot(n, V[b])
        assert all((support - dot(n, w)).sign() >= 0 for w in V)
        rows.append(cross(V[j], n))
        supports.append(support)
    assert any(b.sign() > 0 for b in supports)
    return rows


def binary_cofactors(G, sign):
    """Coefficients of t0^(3-k)t1^k, k=0,...,3, for four cofactors."""
    assert sign in (-1, 1)
    out = []
    for omitted in range(4):
        ids = [i for i in range(4) if i != omitted]
        row = []
        for k in range(4):
            value = sum((determinant(G[ids[0]][a], G[ids[1]][b], G[ids[2]][c])
                         for a, b, c in product(range(2), repeat=3)
                         if a + b + c == k), ZERO)
            row.append(sign * (-1 if omitted % 2 else 1) * value)
        assert all(x.sign() >= 0 for x in row)
        assert any(x.sign() > 0 for x in row)
        out.append(row)
    return out


def canonical_ray(u):
    return mul(1 / next(x for x in u if x != ZERO), u)


def orbit(u):
    """Complete projective orbit under the verified three wall reflections."""
    first = canonical_ray(u)
    seen, pending = {first}, deque([first])
    while pending:
        v = pending.popleft()
        for wall in WALLS:
            w = canonical_ray(sub(v, mul(2 * dot(v, wall) / dot(wall, wall), wall)))
            if w not in seen:
                seen.add(w)
                pending.append(w)
    return seen


def projected_extremes(V, u):
    """Exact hull in an oriented basis; no normalized square roots needed."""
    e1 = vec((-u[1], u[0], 0)) if u[0] != ZERO or u[1] != ZERO else vec((1, 0, 0))
    e2 = cross(u, e1)
    classes = {}
    for j, v in enumerate(V):
        classes.setdefault((dot(v, e1), dot(v, e2)), []).append(j)
    hull = convex_hull_2d(list(classes))
    assert all(len(classes[p]) == 1 for p in hull)
    return [classes[p][0] for p in hull]


def exceptional_checks(V):
    a, e = orbit(CORNER), orbit(SECOND)
    assert len(a) == 15 and len(e) == 30 and not (a & e)
    maximum = max(dot(v, v) for v in V)
    assert maximum == (25 + 10 * S) / 9
    largest = [v for v in V if dot(v, v) == maximum]
    assert len(largest) == 12
    assert all(any(dot(u, v) == ZERO for v in largest) for u in a | e)

    # The vertex-unique support-probe criterion really does degenerate at
    # both representative axes. This is not failure of the older full-contact
    # criterion, which can also use non-extreme projected contact points.
    H = projected_extremes(V, CORNER)
    assert len(H) == 12 and all(dot(CORNER, V[j]) == ZERO for j in H)
    H = projected_extremes(V, SECOND)
    assert len(H) == 12
    omega = vec((-(1 + 3 * S) / 4, Q5(1) / 2 - S, (1 + S) / 4))
    assert omega != vec((0, 0, 0)) and dot(SECOND, omega) == ZERO
    rows = set()
    for k, j in enumerate(H):
        b = H[(k + 1) % len(H)]
        for v in (j, b):
            rows.add(row_at(V, (j, b, v), SECOND))
    signs = [dot(omega, g).sign() for g in rows]
    assert len(rows) == 12 and signs.count(-1) == 7 and signs.count(0) == 5
    assert all(s <= 0 for s in signs)
    return len(a), len(e), maximum


def verify_stable(cells=CELL_EXPOSURES, edges=EDGE_CERTIFICATES,
                  corners=VERTEX_CERTIFICATES, check_prior=True):
    self_check()
    V = vertices()
    assert len(V) == 62 and set(V) == {mul(-1, v) for v in V}
    polygons, triangles = build_cells()
    nodes, segments = strata(polygons)
    assert [(c, j) for c, j, _ in cells] == list(triangles)
    assert [i for i, _, _, _ in edges] == list(range(len(segments)))
    assert [i for i, _, _, _ in corners] == [i for i in range(14) if i not in (0, 3)]
    assert [(c, f) for c, f, _, _ in CERTIFICATES] == list(triangles)

    comparisons = 0
    for (cell, fan, chords), (c, f, _, contacts) in zip(cells, CERTIFICATES):
        assert (cell, fan) == (c, f) and len(chords) == 4
        for chord, (_, _, j) in zip(chords, contacts):
            comparisons += exposing_chord(V, chord, j, polygons[cell])

    coefficient_count = positive_count = support_comparisons = 0
    edge_summary = []
    for index, sign, contacts, chords in edges:
        assert len(contacts) == len(chords) == 4 and len(set(contacts)) == 4
        G = [edge_rows(V, c, segments[index]) for c in contacts]
        C = binary_cofactors(G, sign)
        coefficient_count += 16
        positive = sum(x.sign() > 0 for row in C for x in row)
        positive_count += positive
        support_comparisons += 4 * 2 * len(V)
        for chord, (_, _, j) in zip(chords, contacts):
            comparisons += exposing_chord(V, chord, j, segments[index])
        edge_summary.append(positive)
    assert coefficient_count == 400

    for index, sign, contacts, chords in corners:
        assert sign in (-1, 1)
        assert len(contacts) == len(chords) == 4 and len(set(contacts)) == 4
        G = [row_at(V, c, nodes[index]) for c in contacts]
        for omitted in range(4):
            value = determinant(*(G[j] for j in range(4) if j != omitted))
            assert (sign * (-1 if omitted % 2 else 1) * value).sign() > 0
        support_comparisons += 4 * len(V)
        for chord, (_, _, j) in zip(chords, contacts):
            comparisons += exposing_chord(V, chord, j, [nodes[index]])

    twofold, second, maximum = exceptional_checks(V)
    prior = verify_orientation() if check_prior else None
    return {
        'agent': 'six-rupert-1', 'role': 'researcher',
        'arithmetic': 'exact Q(sqrt(5)); standard library; no floating-point decisions',
        'claim': 'stable varying-receiver local exclusion outside 45 axes; no reverse-local Rupert orientation',
        'global_Rupert_property': 'unresolved',
        'cells': len(polygons), 'cell_fan_certificates': len(cells),
        'open_edge_certificates': len(edges), 'nonexceptional_corner_certificates': len(corners),
        'exposure_gap_comparisons': comparisons,
        'new_support_comparisons': support_comparisons,
        'new_binary_cofactor_coefficients': coefficient_count,
        'strictly_positive_binary_coefficients': positive_count,
        'positive_coefficient_counts_by_edge': edge_summary,
        'exceptional_axis_orbits': [twofold, second],
        'exceptional_axes_total': twofold + second,
        'exceptional_maximum_radius_sq': str(maximum),
        'prior_fixed_outer_certificate_rechecked': prior is not None,
        'neighborhood_bounds': 'existential and pointwise; uniform on compact sets avoiding the exceptional axes',
        'trust_boundary': 'exact field kernel and coordinates; unformalized analytic bridges in stable_proof.md',
    }


def negative_tests():
    cases = []
    e = deepcopy(EDGE_CERTIFICATES)
    e.pop()
    cases.append(('missing open edge', CELL_EXPOSURES, e, VERTEX_CERTIFICATES))
    c = deepcopy(CELL_EXPOSURES)
    a, b = c[0][2][0]
    c[0][2][0] = (b, a)
    cases.append(('reversed exposing chord', c, EDGE_CERTIFICATES, VERTEX_CERTIFICATES))
    e = deepcopy(EDGE_CERTIFICATES)
    i, sign, contacts, chords = e[0]
    e[0] = (i, -sign, contacts, chords)
    cases.append(('reversed edge cofactor sign', CELL_EXPOSURES, e, VERTEX_CERTIFICATES))
    v = deepcopy(VERTEX_CERTIFICATES)
    v.pop()
    cases.append(('missing nonexceptional corner', CELL_EXPOSURES, EDGE_CERTIFICATES, v))
    rejected = []
    for name, c, e, v in cases:
        try:
            verify_stable(c, e, v, check_prior=False)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('malformed certificate accepted: ' + name)
    return rejected


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    result = verify_stable()
    if args.self_test:
        result['malformed_certificates_rejected'] = negative_tests()
    print(json.dumps(result, indent=2, sort_keys=True))
