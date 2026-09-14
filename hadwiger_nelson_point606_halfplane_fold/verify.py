#!/usr/bin/env python3
"""Exact physical 508-point fold and a literal proper four-colouring.

Standard library only. No solver answer or imported non-four theorem is
required for this negative construction gate.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RAD = (1, 3, 5, 15, 11, 33, 55, 165)
SCALE = 288
# 2c = -(sqrt(3)+sqrt(11))/3, represented at SCALE.
TWICE_C = (0, -96, 0, 0, -96, 0, 0, 0)


def require(ok, why):
    if not ok:
        raise ValueError(why)


def sign(v):
    """Certified real sign using rational enclosures of each positive radical."""
    if not any(v):
        return 0
    bits = 16
    while bits <= 4096:
        scale = 1 << bits
        lo = hi = 0
        for coefficient, radicand in zip(v, RAD, strict=True):
            root = isqrt(radicand*scale*scale)
            upper = root + (root*root != radicand*scale*scale)
            if coefficient >= 0:
                lo += coefficient*root
                hi += coefficient*upper
            else:
                lo += coefficient*upper
                hi += coefficient*root
        if lo > 0:
            return 1
        if hi < 0:
            return -1
        bits *= 2
    raise ValueError('sign isolation did not finish')


def load_parent():
    pins = json.loads((HERE/'inputs.json').read_text())
    for name, wanted in pins.items():
        require(sha256((REPO/name).read_bytes()).hexdigest() == wanted,
                ('input changed', name))
    all_points = []
    for line in (REPO/'hadwiger_nelson_parts509_completion_census_degree9/points.tsv').read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        row = tuple(3*int(x) for x in line.split())
        require(len(row) == 16, 'original coordinate width')
        all_points.append((row[:8], row[8:]))
    require(len(all_points) == 509, 'original order')
    catalogue = json.loads((REPO/'hadwiger_nelson_parts509_swap_closure/completion_points.json').read_text())
    for p in catalogue['points']:
        axes = []
        for axis in ('x', 'y'):
            values = [SCALE*Fraction(x) for x in p[axis]]
            require(len(values) == 8 and all(v.denominator == 1 for v in values),
                    'completion coordinate domain')
            axes.append(tuple(map(int, values)))
        all_points.append(tuple(axes))
    certificate = json.loads((REPO/'hadwiger_nelson_point606_criticality_gate/certificate.json').read_text())
    labels = [v for v in list(range(585))+[606]
              if v not in certificate['deleted_labels']]
    points = [all_points[v] for v in labels]
    require(len(points) == len(set(points)) == 530, 'source point set')
    return labels, points


def fold(points):
    images, sides = [], []
    for x, y in points:
        side = sign(tuple(2*a-b for a, b in zip(y, TWICE_C, strict=True)))
        sides.append(side)
        new_y = tuple(a-b for a, b in zip(TWICE_C, y, strict=True)) if side < 0 else y
        images.append((x, new_y))
    support = sorted(set(images))
    positions = {p: i for i, p in enumerate(support)}
    mapping = [positions[p] for p in images]
    return support, mapping, sides


def norm(p, q):
    out = [0]*8
    for axis in range(2):
        d = [a-b for a, b in zip(p[axis], q[axis], strict=True)]
        for i in range(8):
            out[0] += RAD[i]*d[i]*d[i]
            for j in range(i+1, 8):
                out[i ^ j] += 2*RAD[i & j]*d[i]*d[j]
    return tuple(out)


def unit_edges(points):
    unit = (SCALE*SCALE,)+(0,)*7
    return [e for e in combinations(range(len(points)), 2)
            if norm(points[e[0]], points[e[1]]) == unit]


def check_word(word, n, edges):
    require(type(word) is str and len(word) == n and set(word) <= set('0123'),
            'four-colouring domain')
    require(all(word[a] != word[b] for a, b in edges), 'monochromatic edge')


def compute(certificate=None):
    if certificate is None:
        certificate = json.loads((HERE/'certificate.json').read_text())
    require(type(certificate) is dict, 'certificate object')
    require(set(certificate) == {'four_colouring', 'point_order'}, 'certificate keys')
    require(certificate['point_order'] == 'sorted tuple(x coefficients, y coefficients)',
            'point order')
    labels, parent = load_parent()
    points, mapping, sides = fold(parent)
    edges = unit_edges(points)
    old_edges = unit_edges(parent)
    check_word(certificate['four_colouring'], len(points), edges)
    edge_set = set(edges)
    mapped = [tuple(sorted((mapping[a], mapping[b]))) for a, b in old_edges]
    retained = sum(e in edge_set for e in mapped)
    fibres = {v: [] for v in range(len(points))}
    for v, image in enumerate(mapping):
        fibres[image].append(v)
    require(max(map(len, fibres.values())) <= 2, 'fold fibre size')
    facts = {
        'all_checks': True,
        'source_vertices': len(parent), 'source_edges': len(old_edges),
        'vertices': len(points), 'unit_edges': len(edges),
        'complete_image_pair_checks': len(points)*(len(points)-1)//2,
        'moved_source_points': sides.count(-1), 'axis_points': sides.count(0),
        'merged_source_pairs': sum(len(v) == 2 for v in fibres.values()),
        'new_positions_outside_source': len(set(points)-set(parent)),
        'retained_source_edges_with_multiplicity': retained,
        'lost_source_unit_edges': len(old_edges)-retained,
        'new_image_unit_edges_without_source_edge': len(edge_set-set(mapped)),
        'proper_four_colouring_checked': True,
        'inherited_non_four_theorem_required': False,
        'edge_sha256': sha256(''.join(f'{a} {b}\n' for a, b in edges).encode()).hexdigest(),
        'record_candidate': False,
        'whole_fold_class_decided': False,
    }
    require((facts['source_vertices'], facts['source_edges']) == (530, 2648), 'source graph')
    require((facts['vertices'], facts['unit_edges']) == (508, 2215), 'image graph')
    return facts


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path)
    args = parser.parse_args()
    data = json.loads(args.certificate.read_text()) if args.certificate else None
    result = compute(data)
    require(result == json.loads((HERE/'EXPECTED.json').read_text()), 'expected facts')
    print(json.dumps(result, sort_keys=True))
