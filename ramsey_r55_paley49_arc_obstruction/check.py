"""Check the literal 714-case certificate; Hill--Love completeness is imported.

No imports from the producer, extractor, or SAT code. Field colors use the
norm character rather than an enumerated square set.
"""
import argparse
import json
from collections import Counter
from itertools import combinations
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def points():
    return [(0, 0, 1)]+[(0, 1, a) for a in range(7)]+[(1, a, b) for a in range(7) for b in range(7)]


def incidence(p, line):
    return (p[0]*line[0]+p[1]*line[1]+p[2]*line[2]) % 7


def image(arc, line, z):
    omit = max(i for i in range(3) if line[i])
    axes = [i for i in range(3) if i != omit]
    out = []
    for p in arc:
        denominator = incidence(p, line)
        need(denominator != 0, 'empty line required')
        scale = pow(denominator, 5, 7)
        x, y = p[axes[0]]*scale % 7, p[axes[1]]*scale % 7
        out.append((x+(z % 7)*y) % 7+7*((z//7)*y % 7))
    need(len(set(out)) == len(arc), 'injective affine image')
    return out


def red(u, v):
    dx, dy = u % 7-v % 7, u//7-v//7
    return int(pow((dx*dx-3*dy*dy) % 7, 3, 7) == 1)


def check(doc):
    need(set(doc) == {'schema', 'arcs', 'cases'} and doc['schema'] == 1, 'certificate schema')
    plane = points()
    need(len(doc['arcs']) == 3, 'three representative arcs')
    profiles = []
    expected = set()
    arcs = []
    for ci, raw in enumerate(doc['arcs']):
        need(all(isinstance(p, list) and len(p) == 3 and all(type(x) is int for x in p) for p in raw), 'point format')
        arc = [tuple(p) for p in raw]
        need(len(arc) == 22 and sorted(set(arc)) == arc and set(arc) <= set(plane), '22 distinct canonical points')
        sizes = [sum(incidence(p, line) == 0 for p in arc) for line in plane]
        need(max(sizes) == 4, 'four-arc property on every projective line')
        profiles.append([sizes.count(j) for j in range(5)])
        expected.update((ci, li, z) for li, size in enumerate(sizes) if size == 0 for z in range(7, 49))
        arcs.append(arc)
    need(len(set(tuple(p) for p in profiles)) == 3, 'three inequivalent projective types')
    seen = set()
    colors = Counter()
    for row in doc['cases']:
        need(isinstance(row, list) and len(row) == 9 and all(type(x) is int for x in row), 'case row')
        ci, li, z, color, *witness = row
        key = ci, li, z
        need(key in expected and key not in seen, 'exact case key coverage')
        need(color in (0, 1), 'edge color')
        need(witness == sorted(set(witness)) and all(0 <= v < 22 for v in witness), 'five witness indices')
        mapped = image(arcs[ci], plane[li], z)
        need(all(red(mapped[u], mapped[v]) == color for u, v in combinations(witness, 2)), 'ten physical witness pairs')
        seen.add(key)
        colors[color] += 1
    need(seen == expected, 'missing affine case')
    need(len(seen) == 714, '714 affine cases')
    return {'status': 'VERIFIED_714_ARC_CASES_CLASSIFICATION_IMPORTED',
            'projective_points_and_lines': 57, 'arc_size': 22,
            'line_intersection_profiles': profiles, 'empty_lines': [p[0] for p in profiles],
            'normalized_linear_maps_per_chart': 42, 'affine_cases': len(seen),
            'physical_witness_pairs': 10*len(seen), 'blue_red_witnesses': [colors[0], colors[1]],
            'imported_theorem': 'Hill--Love (2003): PG(2,7) has exactly three projective equivalence classes of 22-point four-arcs.',
            'classification_recomputed': False}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('certificate', type=Path)
    args = ap.parse_args()
    print(json.dumps(check(json.loads(args.certificate.read_text())), indent=2, sort_keys=True))
