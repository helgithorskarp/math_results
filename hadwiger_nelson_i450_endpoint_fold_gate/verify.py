"""Exact preflight obstruction; no colouring search or producer import."""
from pathlib import Path
from itertools import combinations, product
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'hadwiger_nelson_overlapping_forcing_seed' / 'certificate.json'
SOURCE_HASH = '3a487318d1d417e812791a1fd66d679151a7816fcf325a5bfd6a0351a0663237'


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sq(p, q):
    a, b, c, d = (x-y for x, y in zip(p, q))
    return (3*a*a+11*b*b+c*c+33*d*d, 2*(a*b+c*d))


def reflect(p):
    a, b, c, d = p
    return (a, b, -c, 12-d)


def difference(p, o, v):
    return tuple(a-b for a, b in zip(sq(p, o), sq(p, v)))


def preserves_path(points, flags):
    image = [reflect(p) if f else p for p, f in zip(points, flags)]
    return (all(sq(p, q) == (1296, 0) for p, q in zip(image, image[1:])),
            image[0] == image[-1])


def source():
    raw = SOURCE.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == SOURCE_HASH, 'source provenance')
    data = json.loads(raw)['unequal']
    need(data['denominator'] == 1, 'coordinate denominator')
    p = [tuple(row) for row in data['points']]
    need(len(p) == 450 and len(set(p)) == 450, 'source order or collisions')
    need(all(len(row) == 4 and all(type(c) is int for c in row) for row in p), 'integer coordinates')
    need(p[:2] == [(0, 0, 0, 0), (0, 0, 0, 12)], 'marked points')
    return p, data['colouring']


def verify(cert):
    need(set(cert) == {'schema', 'source_sha256', 'off_axis_unit_path',
                      'path_points', 'path_squared_distance_differences'}, 'certificate schema')
    need(type(cert['schema']) is int and cert['schema'] == 1, 'schema version')
    need(cert['source_sha256'] == SOURCE_HASH, 'pinned source hash')
    p, word = source()
    edges = [(a, b) for a, b in combinations(range(450), 2) if sq(p[a], p[b]) == (1296, 0)]
    need(len(edges) == 2290, 'complete source unit edges')
    need(len(word) == 450 and all(type(c) is int and 0 <= c < 4 for c in word), 'source positive word')
    need(word[0] != word[1] and all(word[a] != word[b] for a, b in edges), 'positive source colouring')
    path = cert['off_axis_unit_path']
    need(path == [0, 10, 16, 1], 'fixed path labels')
    points = [p[i] for i in path]
    need(cert['path_points'] == [list(q) for q in points], 'path membership')
    deltas = [difference(q, p[0], p[1]) for q in points]
    need(cert['path_squared_distance_differences'] == [list(d) for d in deltas], 'distance differences')
    need(all(d != (0, 0) for d in deltas), 'on-axis path vertex')
    need(all(sq(a, b) == (1296, 0) for a, b in zip(points, points[1:])), 'path edge')
    need(sq(p[0], p[1]) == (4752, 0), 'endpoint distance sqrt(11/3)')
    # Independent finite application of the fold criterion to this short path.
    valid, collisions = [], []
    for flags in product((0, 1), repeat=4):
        ok, hit = preserves_path(points, flags)
        if ok:
            valid.append(flags)
            if hit:
                collisions.append(flags)
    need(valid == [(0, 0, 0, 0), (1, 1, 1, 1)] and not collisions, 'fold truth table')
    on = [i for i, q in enumerate(p) if difference(q, p[0], p[1]) == (0, 0)]
    need(on == [2, 3, 67, 97, 181, 306, 438], 'full on-axis census')
    return {'status': 'VERIFIED_I450_ENDPOINT_FOLD_FAILURE', 'source_points': 450,
            'source_unit_edges': len(edges), 'complete_pair_checks': 450*449//2,
            'on_axis_vertices': on, 'path': path, 'path_unit_edges': 3,
            'path_fold_assignments': 16, 'edge_preserving_path_assignments': len(valid),
            'endpoint_identifying_assignments': len(collisions),
            'declared_image_budget_if_realizable': 449, 'fold_realizable': False,
            'new_physical_support': False, 'record_signal': False}


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--check-expected', action='store_true')
    args = ap.parse_args()
    out = verify(json.loads((HERE/'certificate.json').read_text()))
    if args.check_expected:
        need(out == json.loads((HERE/'expected.json').read_text()), 'expected result')
    print(json.dumps(out, indent=2))
