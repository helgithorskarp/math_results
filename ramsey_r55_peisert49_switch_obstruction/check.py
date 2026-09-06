"""Independent literal checker; no producer or field-arithmetic imports.

Colors use slopes {0,1,5,infinity}; controls separately identify this with
the quartic-coset definition of Peisert49. The Hill--Love classification
is an explicitly imported mathematical premise, not verified by this file.
"""
import argparse
import json
from itertools import combinations, product
from pathlib import Path


def need(ok, why):
    if not ok:
        raise ValueError(why)


def plane():
    return [(0, 0, 1)]+[(0, 1, a) for a in range(7)]+[(1, a, b) for a in range(7) for b in range(7)]


def incident(p, line):
    return sum(p[i]*line[i] for i in range(3)) % 7 == 0


def slope(x, y):
    x, y = x % 7, y % 7
    need(x != 0 or y != 0, 'nonzero direction')
    return next(m for m in range(7) if m*x % 7 == y) if x else 7


def transformed_masks():
    # Enumerate ordered independent columns, not assumed graph automorphisms.
    vectors = [(x, y) for x, y in product(range(7), repeat=2) if x or y]
    directions = [(1, m) for m in range(7)]+[(0, 1)]
    masks = set()
    matrices = 0
    for u in vectors:
        for v in vectors:
            if (u[0]*v[1]-u[1]*v[0]) % 7 == 0:
                continue
            matrices += 1
            bits = [int(slope(x*u[0]+y*v[0], x*u[1]+y*v[1]) in (0, 1, 5, 7))
                    for x, y in directions]
            masks.add(sum(bit*2**i for i, bit in enumerate(bits)))
    need(matrices == 2016 and len(masks) == 28, 'complete GL(2,7) pullbacks')
    return sorted(masks)


def image(arc, line):
    omitted = max(i for i in range(3) if line[i])
    axes = [i for i in range(3) if i != omitted]
    out = []
    for p in arc:
        d = sum(a*b for a, b in zip(p, line)) % 7
        need(d != 0, 'empty infinity line')
        scale = pow(d, 5, 7)
        out.append(tuple(p[i]*scale % 7 for i in axes))
    need(len(set(out)) == len(out), 'injective chart')
    return out


def edge(p, q, mask):
    need(p != q, 'distinct vertices')
    return (mask >> slope(p[0]-q[0], p[1]-q[1])) & 1


def check(doc):
    need(type(doc) is dict and set(doc) == {'schema', 'arcs', 'cases'}, 'document format')
    need(type(doc['schema']) is int and doc['schema'] == 1, 'schema')
    need(type(doc['arcs']) is list and len(doc['arcs']) == 3, 'three arcs')
    projective = plane()
    profiles, arcs, charts = [], [], {}
    blocked_extensions = 0
    for ci, raw in enumerate(doc['arcs']):
        need(type(raw) is list and len(raw) == 22, 'arc size')
        need(all(type(p) is list and len(p) == 3 and all(type(x) is int for x in p) for p in raw), 'point format')
        arc = [tuple(p) for p in raw]
        need(arc == sorted(set(arc)) and set(arc) <= set(projective), 'canonical distinct points')
        on_lines = [[i for i, p in enumerate(arc) if incident(p, line)] for line in projective]
        sizes = [len(x) for x in on_lines]
        need(max(sizes) == 4, 'four-arc property')
        profiles.append([sizes.count(j) for j in range(5)])
        for point in projective:
            if point in arc:
                continue
            need(any(len(indices) == 4 and incident(point, line)
                     for line, indices in zip(projective, on_lines)), 'no extension to a 23-point four-arc')
            blocked_extensions += 1
        for li, size in enumerate(sizes):
            if size == 0:
                charts[ci, li] = image(arc, projective[li])
        arcs.append(arc)
    need(len(set(map(tuple, profiles))) == 3, 'projective inequivalence')
    need(len(charts) == 17 and blocked_extensions == 105, 'arc cover and saturation')
    masks = transformed_masks()
    expected = {(ci, li, mask) for ci, li in charts for mask in masks}
    need(type(doc['cases']) is list, 'case list')
    seen = set()
    for row in doc['cases']:
        need(type(row) is list and len(row) == 4, 'case format')
        ci, li, mask, stars = row
        need(all(type(x) is int for x in (ci, li, mask)), 'integer key')
        key = ci, li, mask
        need(key in expected and key not in seen, 'unique complete case key')
        need(type(stars) is list and len(stars) == 7, 'seven forbidden outside points')
        vertices = charts[ci, li]
        seen_outside = set()
        for star in stars:
            need(type(star) is list and len(star) == 6 and all(type(x) is int for x in star), 'star format')
            outside, color, *q = star
            need(0 <= outside < 49 and color in (0, 1), 'point and color')
            point = outside % 7, outside // 7
            need(point not in vertices and outside not in seen_outside, 'distinct outside exclusions')
            need(q == sorted(set(q)) and all(0 <= i < 22 for i in q), 'four distinct anchor indices')
            physical = [(vertices[i], 0) for i in q]+[(point, 1)]
            need(all(edge(p, r, mask) ^ s ^ t == color
                     for (p, s), (r, t) in combinations(physical, 2)), 'ten physical switched pairs')
            seen_outside.add(outside)
        seen.add(key)
    need(seen == expected and len(seen) == 476, 'missing or extra affine case')
    return {'status': 'VERIFIED_PEISERT49_SWITCH_OBSTRUCTION_WITH_HILL_LOVE_PREMISE',
            'classification_recomputed': False, 'arc_profiles': profiles,
            'projective_extension_exclusions': blocked_extensions,
            'linear_maps': 2016, 'direction_masks': 28, 'affine_cases': len(seen),
            'forbidden_opposite_stars_per_case': 7, 'physical_star_witnesses': 3332,
            'physical_witness_pairs': 33320, 'maximum_switch_class_size': 22,
            'opposite_class_upper_bound_when_class_size_22': 20,
            'excluded_switched_orders': '>=43', 'ramsey_bound_improved': False}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('certificate', type=Path)
    args = ap.parse_args()
    print(json.dumps(check(json.loads(args.certificate.read_text())), indent=2, sort_keys=True))
