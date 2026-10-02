#!/usr/bin/env python3
"""Exact controls for a continuous small-hole pair, not sample extrapolation.

T_m and T_m+(+/- (4-r),4+r), m>=2, 0<r<2 seal area16r.
The all-real/all-m proof is ordinary and separate; controls check the
affine owners, four triangles and emptiness at exact rational fixtures.
Author six-heesch-3, researcher; shared convex polygon primitives.
"""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib
import json
import geometry as b
from copy import deepcopy

SCALE = 8


def check(m, r, sign=-1, cycle_override=None, owners_override=None, triangles_override=None):
    r = Fraction(r)
    b.require(m >= 2 and 0 < r < 2, 'continuous pair is outside proved parameter domain')
    k = r*SCALE
    b.require(k.denominator == 1, 'fixture requires integer eightfold scale')
    k = int(k)
    dx, dy = sign*(4*SCALE-k), 4*SCALE+k
    aa = tuple(tuple((SCALE*x, SCALE*y) for x, y in atom) for atom in b.atoms(m))
    bb = tuple(tuple((x+dx, y+dy) for x, y in atom) for atom in aa)
    b.require(not any(b.boxes_meet(b.box(a), b.box(c), False) and b.convex_intersection(a, c, False)
                      for a in aa for c in bb), 'continuous parallel copies overlap')
    cycle = ((80, 16), (80+k, 16+k), (48+k, 16+k), (32+k, 32+k), (32, 32), (48, 16))
    triangles = [tuple(cycle[i] for i in indices) for indices in [(5, 0, 1), (5, 1, 2), (2, 3, 4), (2, 4, 5)]]
    if sign == 1:
        cycle = b.ccw(tuple((128-x, y) for x, y in cycle))
        triangles = [b.ccw(tuple((128-x, y) for x, y in triangle)) for triangle in triangles]
    if cycle_override is not None:
        cycle = tuple(tuple(v) for v in cycle_override)
    if triangles_override is not None:
        triangles = [tuple(tuple(v) for v in triangle) for triangle in triangles_override]
    b.require(len(cycle) == 6 and len(triangles) == 4, 'wrong hole or triangulation length')
    b.require(b.twice_area(cycle) == 16*r*SCALE*SCALE, 'continuous hole area differs from16r')
    b.require(all(b.twice_area(t) == 4*r*SCALE*SCALE for t in triangles), 'affine triangle area differs')
    for i, j in combinations(range(6), 2):
        if (i-j) % 6 in (1, 5):
            continue
        b.require(not b.segments_meet(cycle[i], cycle[(i+1) % 6], cycle[j], cycle[(j+1) % 6]), 'hole cycle self-intersects')
    for a, c in combinations(triangles, 2):
        b.require(not b.convex_intersection(a, c, False), 'hole triangulation overlaps')
    triangulated, unused = b.boundary(triangles)
    b.require(set(triangulated) == set(cycle) and b.twice_area(triangulated) == b.twice_area(cycle), 'hole triangle union boundary differs')
    owners = []
    if owners_override is not None:
        b.require(len(owners_override) == 6, 'wrong owner count')
    for edge_index, (a, c) in enumerate(zip(cycle, cycle[1:]+cycle[:1])):
        choices = [(copy, atom_index) for copy, atoms in enumerate((aa, bb)) for atom_index, atom in enumerate(atoms)
                   if any(b.on_segment(a, v, w) and b.on_segment(c, v, w) for v, w in zip(atom, atom[1:]+atom[:1]))]
        b.require(choices, 'hole segment lacks one whole atom owner')
        owner = min(choices) if owners_override is None else tuple(owners_override[edge_index])
        b.require(owner in choices, 'specified atom does not own the entire hole edge')
        b.require(owner[1] < 5, 'hole uses a length-dependent later owner')
        owners.append(owner)
    b.require(all(not b.convex_intersection(t, a, False) for t in triangles for a in aa+bb), 'hole interior not empty')
    b.require(0 < b.twice_area(cycle) < sum(b.twice_area(a) for a in aa), 'hole area cannot exclude a whole tile')
    return {'m': m, 'r': str(r), 'sign': sign, 'scaled_translation': [dx, dy],
            'hole_twice_area_unscaled': str(16*r), 'cycle_scaled': cycle,
            'triangles_scaled': triangles, 'edge_owners_first_five_atoms': owners,
            'interiors_disjoint': True, 'hole_empty_and_sealed': True}


def evidence():
    rows = [check(m, r, sign) for m in (2, 7)
            for r in (Fraction(1, 8), Fraction(1, 2), 1, Fraction(3, 2), Fraction(15, 8))
            for sign in (-1, 1)]
    rejected = []
    for r in (0, 2, -1):
        try:
            check(2, r)
        except ValueError:
            rejected.append({'r': r, 'outside_scope_rejected': True})
        else:
            raise ValueError('unsupported parameter accepted')
    fixture = check(2, Fraction(1, 2))
    bad_cycle = deepcopy(fixture['cycle_scaled'])
    bad_cycle = list(bad_cycle)
    bad_cycle[0] = (bad_cycle[0][0]+1, bad_cycle[0][1])
    bad_owners = deepcopy(fixture['edge_owners_first_five_atoms'])
    bad_owners[0] = (0, 0)
    bad_triangles = deepcopy(fixture['triangles_scaled'])
    bad_triangles[1] = bad_triangles[0]
    damaged = []
    for name, kwargs in [('shifted_cycle', {'cycle_override': bad_cycle}),
                         ('wrong_whole_edge_owner', {'owners_override': bad_owners}),
                         ('duplicated_triangle', {'triangles_override': bad_triangles})]:
        try:
            check(2, Fraction(1, 2), **kwargs)
        except ValueError:
            damaged.append(name)
        else:
            raise ValueError('damaged geometry accepted: '+name)
    return {'agent': 'six-heesch-3', 'role': 'researcher', 'rational_fixture_count': len(rows),
            'fixture_sha256': hashlib.sha256(json.dumps(rows, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
            'outside_scope_controls': rejected, 'damaged_geometry_rejected': damaged,
            'all_real_all_m_coverage_requires_ordinary_proof': True,
            'independent_geometry_claimed': False, 'shape_Heesch_upper_claimed': False}


if __name__ == '__main__':
    out = evidence()
    expected = json.loads(Path(__file__).with_name('expected.json').read_text())
    b.require(out == expected, 'deterministic evidence differs from expected.json')
    print(json.dumps(out, indent=2))
