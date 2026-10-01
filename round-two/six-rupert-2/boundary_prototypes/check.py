#!/usr/bin/env python3
"""Exact J74 boundary prototypes and interior-margin hypotheses.

Production verification reads literal corner and boundary indices, then
checks all original supports without invoking a hull finder. Python 3.11+
standard library only; every mathematical guard remains active under -O.
The normal-transport and support-function bridges are in PROOF.md.
"""
import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load():
    manifest = json.loads((HERE/'DEPENDENCIES.json').read_text())
    parent = (HERE/manifest['directory']).resolve()
    require(set(manifest['sha256']) ==
            {'q5.py', 'model.py', 'shadow.py', 'PROOF.md', 'expected.json'},
            'complete pinned original geometry inputs')
    for name, wanted in manifest['sha256'].items():
        require(hashlib.sha256((parent/name).read_bytes()).hexdigest() == wanted,
                'changed pinned input: '+name)
    sys.path.insert(0, str(parent))
    import model
    import q5
    return model, q5, json.loads((parent/'expected.json').read_text()), manifest


def axes(q5):
    Q = q5.Q
    phi = Q(1, 1)/2
    return [(Q(1), Q(), Q()), (Q(), Q(1), Q())] + [
        q5.scale(1/(2*phi), (Q(1), e*phi, d*(1+phi)))
        for e in (-1, 1) for d in (-1, 1)]


def project(v, m, q5):
    return q5.sub(v, q5.scale(q5.dot(v, m), m))


def reflect(v, m, q5):
    return q5.sub(v, q5.scale(2*q5.dot(v, m), m))


def literal_indices(xs, total, message):
    require(isinstance(xs, list) and all(type(i) is int and 0 <= i < total for i in xs)
            and len(set(xs)) == len(xs), message)
    return xs


def check_profile(record, m, model, q5):
    Q, dot, sub, cross = q5.Q, q5.dot, q5.sub, q5.cross
    V = model.VERTICES
    require(set(record) == {'axis', 'corner_original_indices', 'boundary_original_indices'},
            'complete prototype record fields')
    require(type(record['axis']) is int and 0 <= record['axis'] < 6,
            'prototype axis index')
    require(dot(m, m) == 1, 'physical unit normal')
    corner_ix = literal_indices(record['corner_original_indices'], len(V), 'literal corner indices')
    boundary_ix = literal_indices(record['boundary_original_indices'], len(V), 'literal boundary indices')
    require(len(corner_ix) == 12, 'twelve declared original shadow corners')
    points = [project(V[i], m, q5) for i in corner_ix]
    require(len(set(points)) == 12, 'distinct physical shadow corners')
    boundary = set(boundary_ix)
    require(boundary_ix == sorted(boundary_ix), 'canonical prototype index order')
    edges = []
    actual_boundary = set()
    supports = 0
    for e, (p, q) in enumerate(zip(points, points[1:]+points[:1])):
        inward = cross(m, sub(q, p))
        length2 = dot(inward, inward)
        require(length2 > 0, 'nondegenerate physical projected edge')
        require(all(dot(inward, sub(r, p)) > 0 for r in points if r not in (p, q)),
                'strict irredundant full cyclic polygon')
        gaps = [dot(inward, sub(v, p)) for v in V]
        require(all(g >= 0 for g in gaps), 'all-original polygon edge support')
        actual_boundary.update(i for i, gap in enumerate(gaps) if gap == 0)
        edges.append((length2, gaps))
        supports += len(V)
    gamma2 = Q(3, -1)/8
    distances = []
    for i in range(len(V)):
        if i not in boundary:
            for e, (length2, gaps) in enumerate(edges):
                gap = gaps[i]
                require(gap > 0, 'every omitted original has strict interior support')
                distance2 = gap*gap/length2
                require(distance2 >= gamma2, 'complete physical interior-distance lower bound')
                distances.append((distance2, i, e))
    require(boundary == actual_boundary and len(boundary) == 28,
            'complete twenty-eight actual boundary originals')
    require(len(distances) == 32*12, 'all thirty-two omitted originals against all edges')
    minimum, witness_i, witness_e = min(distances)
    require(minimum == gamma2, 'sharp minimum physical interior distance')
    corner_preimages = {i for i, v in enumerate(V) if project(v, m, q5) in points}
    edge_interior = sorted(boundary-corner_preimages)
    require(len(corner_preimages) == 20 and len(edge_interior) == 8,
            'all corner preimages and additional edge-interior originals retained')
    W = {V[i] for i in boundary}
    require({reflect(v, m, q5) for v in W} == W,
            'actual prototype reflection permutes every original')
    reflection_permutation = [next(j for j in boundary_ix if V[j] == reflect(V[i], m, q5))
                              for i in boundary_ix]
    require(len(set(reflection_permutation)) == 28, 'full prototype reflection bijection')
    qix = [i for i in boundary_ix if dot(m, V[i]) == 0]
    require(len(qix) == 4, 'four actual equatorial originals')
    a, b, c = (V[i] for i in qix[:3])
    nonflat = next(i for i in boundary_ix if dot(m, V[i]) != 0)
    require(dot(cross(sub(b, a), sub(c, a)), sub(V[nonflat], a)) != 0,
            'full affine dimension of the twenty-eight-point prototype')
    reflected_body = {reflect(v, m, q5) for v in V}
    full_body = reflected_body == set(V)
    witness = None if full_body else next(i for i, v in enumerate(V) if reflect(v, m, q5) not in V)
    output = {'axis': record['axis'], 'corner_original_indices': corner_ix,
              'boundary_original_indices': boundary_ix,
              'edge_interior_original_indices': edge_interior,
              'omitted_original_count': 32, 'full_support_comparisons': supports,
              'strict_interior_distance_comparisons': len(distances),
              'minimum_squared_interior_edge_distance': str(minimum),
              'sharp_distance_witness': {'original': witness_i, 'edge': witness_e},
              'reflection_permutation_original_indices': reflection_permutation,
              'full_body_reflection': full_body,
              'full_body_reflection_counterexample_original': witness}
    return {'normal': m, 'boundary': W, 'output': output}


def parse(text, Q):
    matched = re.fullmatch(r'\(([-0-9/]+)\)\+\(([-0-9/]+)\)sqrt5', text)
    require(matched is not None, 'restricted exact original matrix scalar')
    return Q(Fraction(matched[1]), Fraction(matched[2]))


def check_motions(motions, profiles, model, q5):
    Q, dot, cross = q5.Q, q5.dot, q5.cross
    require(len(motions) == 22, 'complete pinned original base catalogue')
    counts = [[0]*6 for _ in range(6)]
    rows = []
    full_body_count = 0
    for index, motion in enumerate(motions):
        i, j = motion['source_axis'], motion['receiver_axis']
        require(type(i) is int and type(j) is int and 0 <= i < 6 and 0 <= j < 6,
                'source and receiving axis indices')
        cols = [tuple(parse(x, Q) for x in c) for c in motion['proper_matrix_columns']]
        require(len(cols) == 3 and all(len(c) == 3 for c in cols), 'full actual matrix')
        require(all(dot(cols[a], cols[b]) == (1 if a == b else 0)
                    for a in range(3) for b in range(3)), 'actual base motion orthogonal')
        require(dot(cols[0], cross(cols[1], cols[2])) == 1, 'actual base motion proper')
        def move(v):
            return tuple(sum((cols[k][r]*v[k] for k in range(3)), Q()) for r in range(3))
        moved = {move(v) for v in profiles[i]['boundary']}
        require(moved == profiles[j]['boundary'] and len(moved) == 28,
                'entire actual spatial boundary set maps to the target prototype')
        normal = move(profiles[i]['normal'])
        require(normal in (profiles[j]['normal'], q5.scale(-1, profiles[j]['normal'])),
                'proper marked-plane transport')
        is_body = {move(v) for v in model.VERTICES} == set(model.VERTICES)
        full_body_count += is_body
        rows.append({'configuration': index, 'source_axis': i, 'receiver_axis': j,
                     'normal_sign': 1 if normal == profiles[j]['normal'] else -1,
                     'matched_actual_boundary_originals': len(moved),
                     'full_body_symmetry': is_body})
        counts[i][j] += 1
    wanted = [[2, 0, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0]]+[[0, 0, 1, 1, 1, 1]]*4
    require(counts == wanted, 'all twenty-two original configurations covered')
    representatives = [0, 1, 2, 2, 2, 2]
    require(all(any(r['source_axis'] == representatives[i] and r['receiver_axis'] == i
                    for r in rows) for i in range(6)),
            'three representative prototypes suffice by verified proper maps')
    return {'motions': rows, 'configuration_count_matrix': counts,
            'proper_marked_prototype_representatives': representatives,
            'full_body_symmetry_configuration_count': full_body_count,
            'actual_spatial_boundary_matches': 22*28}


def check_radius(gamma2, radius2, cap):
    require(gamma2 > 0 and radius2 > 0 and cap > 0,
            'positive support-transport constants')
    require(gamma2 > 4*radius2*cap*cap,
            'strict interior clearance exceeds twice the projection drift')


def controls(certificate, profiles, normals, model, q5, motions):
    damaged = []
    record = copy.deepcopy(certificate['records'][2])
    edge_original = profiles[2]['output']['edge_interior_original_indices'][0]
    record['boundary_original_indices'].remove(edge_original)
    damaged.append(record)
    record = copy.deepcopy(certificate['records'][2])
    record['boundary_original_indices'].remove(edge_original)
    extra = next(i for i in range(60) if i not in profiles[2]['output']['boundary_original_indices'])
    record['boundary_original_indices'].append(extra)
    record['boundary_original_indices'].sort()
    damaged.append(record)
    rejected = 0
    for record in damaged:
        try:
            check_profile(record, normals[2], model, q5)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('omitted edge-interior original was accepted')
    bad = copy.deepcopy(motions)
    bad[0]['proper_matrix_columns'][0][0] = '(2)+(0)sqrt5'
    try:
        check_motions(bad, profiles, model, q5)
    except ValueError:
        rejected += 1
    else:
        raise ValueError('incorrect spatial motion was accepted')
    try:
        check_radius(q5.Q(3, -1)/8, q5.Q(11, 4)/4, Fraction(1, 14))
    except ValueError:
        rejected += 1
    else:
        raise ValueError('unsupported proof radius was accepted')
    return rejected


def verify():
    model, q5, original, manifest = load()
    Q, dot = q5.Q, q5.dot
    V = model.VERTICES
    radius2 = Q(11, 4)/4
    gamma = Q(-1, 1)/4
    gamma2 = Q(3, -1)/8
    cap = Fraction(1, 15)
    require(len(V) == len(set(V)) == 60 and all(dot(v, v) == radius2 for v in V),
            'all sixty distinct originals have the exact common circumradius')
    require(gamma > 0 and gamma*gamma == gamma2, 'positive physical interior radius')
    check_radius(gamma2, radius2, cap)
    require(gamma2-4*radius2*cap*cap == Q(587, -257)/1800 and
            587*587-5*257*257 == 14324 > 0,
            'independently ordered positive squared transport gap')
    certificate = json.loads((HERE/'certificate.json').read_text())
    require(certificate['agent'] == 'six-rupert-2' and certificate['role'] == 'researcher',
            'actual author and role')
    require(len(certificate['records']) == 6, 'all six prototype certificates')
    normals = axes(q5)
    profiles = []
    for i, (record, m) in enumerate(zip(certificate['records'], normals)):
        require(record['axis'] == i, 'complete ordered axis coverage')
        profiles.append(check_profile(record, m, model, q5))
    require([p['output']['full_body_reflection'] for p in profiles] ==
            [True, True, False, False, False, False],
            'prototype reflection distinguished from full-body reflection')
    motions = original['minimum_receiver_proper_motions']
    motion_record = check_motions(motions, profiles, model, q5)
    negative = controls(certificate, profiles, normals, model, q5, motions)
    return {'agent': 'six-rupert-2', 'role': 'researcher',
            'pinned_source_commit': manifest['source_commit'],
            'certificate_sha256': hashlib.sha256((HERE/'certificate.json').read_bytes()).hexdigest(),
            'profiles': [p['output'] for p in profiles],
            'circumradius_squared': str(radius2), 'uniform_interior_radius': str(gamma),
            'closed_normal_chord_shadow_reduction_radius': str(cap),
            'squared_support_transport_gap': str(gamma2-4*radius2*cap*cap),
            'total_full_support_comparisons': sum(p['output']['full_support_comparisons'] for p in profiles),
            'total_strict_interior_distance_comparisons':
                sum(p['output']['strict_interior_distance_comparisons'] for p in profiles),
            'prototype_reflection_original_matches': 6*28,
            'negative_certificate_controls': negative, **motion_record}


if __name__ == '__main__':
    result = verify()
    if '--emit' in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        require(result == json.loads((HERE/'expected.json').read_text()),
                'every exact finite certificate field matches the expected record')
        print(json.dumps({k: v for k, v in result.items() if k not in ('profiles', 'motions')}, indent=2))
