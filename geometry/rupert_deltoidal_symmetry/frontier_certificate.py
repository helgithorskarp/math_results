#!/usr/bin/env python3
"""Exact limiting-axis cone and two incident-cell exclusions at E.

This is a necessary-condition certificate for small moving pairs, not a
global non-Rupert certificate. The limit argument is in contact_family_proof.md.
Python 3.11+, standard library only.
"""
import json
from verify import Q5, S, ZERO, vec, vertices, add, sub, mul, dot, cross, convex_hull_2d
from orientation_certificate import build_cells
from contact_family_certificate import E, RAYS, HULL


def row(V, contact):
    a, b, j = contact
    return cross(V[j], cross(sub(V[b], V[a]), E))


def check():
    V = vertices()
    e1, e2 = vec((-E[1], E[0], 0)), cross(E, vec((-E[1], E[0], 0)))
    classes = {}
    for j, v in enumerate(V):
        classes.setdefault((dot(e1, v), dot(e2, v)), []).append(j)
    keys = convex_hull_2d(list(classes))
    assert all(len(classes[p]) == 1 for p in keys)
    actual = tuple(classes[p][0] for p in keys)
    start = actual.index(HULL[0])
    assert actual[start:] + actual[:start] == HULL
    metadata = {}
    for k, a in enumerate(HULL):
        b = HULL[(k + 1) % len(HULL)]
        normal = cross(sub(V[b], V[a]), E)
        assert dot(normal, V[a]).sign() > 0
        assert all(dot(normal, sub(V[a], v)).sign() >= 0 for v in V)
        for j in (a, b):
            metadata.setdefault(cross(V[j], normal), (a, b, j))
    assert len(metadata) == 12
    assert cross(RAYS[0], RAYS[1]) != vec((0, 0, 0))
    assert all(dot(E, r) == ZERO for r in RAYS)
    assert all(dot(g, r).sign() <= 0 for g in metadata for r in RAYS)
    force = ((17, 4, 4), (45, 34, 45))
    left, right = (row(V, c) for c in force)
    assert cross(left, E) == cross(right, E) == vec((0, 0, 0))
    assert dot(left, right).sign() < 0
    boundary = []
    for i in range(2):
        g = next(g for g in metadata if dot(g, RAYS[i]) == ZERO
                 and dot(g, RAYS[1-i]).sign() < 0)
        boundary.append({'contact': list(metadata[g]),
                         'dots_on_rays': [str(dot(g, r)) for r in RAYS]})
    # The opposite row pair forces any polar vector into E-perp. The two
    # boundary inequalities then force its two coefficients to be >=0.
    # Conversely every such combination satisfies all 12 inequalities.

    polygons, _ = build_cells()
    conflicts, comparisons = [], 0
    for cell, contact in [(2, (34, 36, 36)), (4, (61, 59, 59))]:
        p = polygons[cell]
        assert E in p
        a, b, j = contact
        edge = sub(V[b], V[a])
        for u in p:
            normal = cross(edge, u)
            for v in V:
                assert dot(normal, sub(V[a], v)).sign() >= 0
                comparisons += 1
        normal0 = cross(edge, E)
        assert dot(normal0, V[a]).sign() > 0
        g = cross(V[j], normal0)
        coefficients = [-2 * dot(g, r) for r in RAYS]
        assert all(c.sign() < 0 for c in coefficients)
        conflicts.append({'cell': cell, 'contact': list(contact),
                          'gap_derivative_on_rays': list(map(str, coefficients)),
                          'polygon': [list(map(str, u)) for u in p]})
    assert {i for i, p in enumerate(polygons) if E in p} == {0, 2, 4}
    return {
        'status': 'exact necessary limiting-axis cone and local exclusions in two incident cells',
        'receiver_E': list(map(str, E)),
        'polar_cone_generators': [list(map(str, r)) for r in RAYS],
        'distinct_endpoint_torques': len(metadata),
        'opposite_contacts_forcing_axis_perpendicular_to_E': [list(c) for c in force],
        'boundary_contacts_forcing_nonnegative_ray_coefficients': boundary,
        'incident_cell_endpoint_conflicts': conflicts,
        'incident_cells': [0, 2, 4],
        'surviving_incident_cell': 0,
        'incident_cell_support_comparisons': comparisons,
        'solver_or_floating_point_decisions': 0,
    }


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
