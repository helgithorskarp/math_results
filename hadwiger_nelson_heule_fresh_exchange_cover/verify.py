#!/usr/bin/env python3
"""Solver-free exact verifier for two Heule fresh-centre exchange covers."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import base64
import json


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
RAD = (1, 3, 5, 15, 11, 33, 55, 165)
ZERO = (F(0),) * 8
ONE = (F(1),) + (F(0),) * 7


def require(ok, detail):
    if not ok:
        raise ValueError(detail)


def add(a, b): return tuple(x+y for x, y in zip(a, b))
def sub(a, b): return tuple(x-y for x, y in zip(a, b))


def mul(a, b):
    out = [F(0)] * 8
    for i, x in enumerate(a):
        if not x:
            continue
        for j, y in enumerate(b):
            if y:
                out[i ^ j] += x*y*RAD[i & j]
    return tuple(out)


def point(row):
    require(len(row) == 2 and all(len(axis) == 8 for axis in row), 'point shape')
    return tuple(tuple(F(x) for x in axis) for axis in row)


def norm2(p, q):
    dx = sub(p[0], q[0]); dy = sub(p[1], q[1])
    return add(mul(dx, dx), mul(dy, dy))


def exact_edges(points):
    return tuple((a, b) for a, b in combinations(range(len(points)), 2)
                 if norm2(points[a], points[b]) == ONE)


def decode_packed(row, length):
    raw = base64.b64decode(row, validate=True)
    require(len(raw) == (length+3)//4, 'packed word length')
    return tuple((raw[i//4] >> (2*(i % 4))) & 3 for i in range(length))


def word_hash(words):
    h = sha256()
    for omitted, colours in enumerate(words):
        text = ''.join('.' if i == omitted else str(c) for i, c in enumerate(colours))
        h.update(f'{omitted} {text}\n'.encode('ascii'))
    return h.hexdigest()


def source_points():
    manifest = json.loads((HERE/'manifest.json').read_text())
    for name, digest in manifest['inputs'].items():
        require(sha256((REPO/name).read_bytes()).hexdigest() == digest, ('input hash', name))
    union = json.loads((REPO/'hadwiger_nelson_parts509_heule_union_minimum/union_510.json').read_text())
    labels = [v for v, provenance in enumerate(union['provenance']) if '510' in provenance]
    require(len(labels) == 510, 'H510 labels')
    old = tuple(point(union['points'][v]) for v in labels)
    require(len(set(old)) == 510, 'H510 distinctness')
    rows = json.loads((REPO/'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json').read_text())
    fresh = {row['centre_index']: row for row in rows}
    require(len(fresh) == len(rows) == 122, 'fresh table')
    return old, fresh


def check_support(spec, old, fresh):
    ids = spec['centre_ids']
    require(ids in ([319], [1074, 1269]), 'support identity')
    rows = [fresh[v] for v in ids]
    points = old + tuple(point(row['coordinates']) for row in rows)
    require(len(set(points)) == len(points), 'support point collision')
    edges = exact_edges(points)
    expected_edges = 2510 if ids == [319] else 2518
    require(len(edges) == expected_edges == spec['edges'], 'support edge count')
    require(len(points) == spec['vertices'], 'support vertex count')
    old_edges = [(a, b) for a, b in edges if b < 510]
    require(len(old_edges) == 2504, 'H510 strict edges')
    for j, row in enumerate(rows):
        v = 510+j
        neighbours = sorted(a if b == v else b for a, b in edges if v in (a, b) and max(a, b) < 510+len(rows))
        old_neighbours = sorted(x for x in neighbours if x < 510)
        require(old_neighbours == row['neighbors'], ('fresh neighbours', ids[j]))
    if len(ids) == 2:
        require((510, 511) in edges, 'fresh mutual unit edge')
    packed = spec['packed_singleton_words']
    require(len(packed) == 510, 'singleton word count')
    words = [decode_packed(row, len(points)) for row in packed]
    require(word_hash(words) == spec['word_stream_sha256'], 'word stream hash')
    checks = 0
    for omitted, colours in enumerate(words):
        for a, b in edges:
            if omitted in (a, b):
                continue
            require(colours[a] != colours[b], ('monochromatic edge', ids, omitted, a, b))
            checks += 1
    # Any support subgraph on at most 508 vertices omits an old H510 vertex:
    # the support has at most two fresh vertices, but 510 old ones.  Its
    # corresponding singleton word restricts to the subgraph.
    require(len(points)-508 >= len(ids)+1, 'old omission at target order')
    return {'centre_ids': ids, 'vertices': len(points), 'edges': len(edges),
            'singleton_colourings': len(words), 'edge_inequalities_checked': checks,
            'word_stream_sha256': spec['word_stream_sha256'],
            'every_at_most_508_subgraph_four_colourable': True}


def validate(data):
    require(data.get('schema') == 1, 'schema')
    old, fresh = source_points()
    specs = data.get('supports')
    require(isinstance(specs, list) and len(specs) == 2, 'supports')
    reports = [check_support(spec, old, fresh) for spec in specs]
    require([x['centre_ids'] for x in reports] == [[319], [1074, 1269]], 'support order')
    result = {'status': 'PASS', 'source_vertices': len(old), 'supports': reports,
              'total_singleton_colourings': sum(x['singleton_colourings'] for x in reports),
              'total_edge_inequalities_checked': sum(x['edge_inequalities_checked'] for x in reports),
              'non_four_signal': False, 'record_improved': False,
              'scope': 'two fixed fresh-centre supports and all their at-most-508 subgraphs'}
    return result


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--certificate', type=Path, default=HERE/'certificate.json')
    ap.add_argument('--check-expected', action='store_true'); args = ap.parse_args()
    result = validate(json.loads(args.certificate.read_text()))
    if args.check_expected:
        require(result == json.loads((HERE/'expected.json').read_text()), 'expected result')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__': main()
