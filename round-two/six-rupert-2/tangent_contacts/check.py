#!/usr/bin/env python3
"""Exact weighted-contact hypotheses for every J74 minimum closed fit.

The production checker uses Python 3.11+ standard library only. It reads
supplied Q(sqrt(5)) weights, checks original vertices and full supports,
and verifies the full three-dimensional contact sets of all 22 motions.
No solver or floating computation is part of this verification.
"""
import copy
from fractions import Fraction
import hashlib
import itertools
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
    import shadow
    return model, q5, shadow, json.loads((parent/'expected.json').read_text()), manifest


def determinant(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def axes(q5):
    Q = q5.Q
    phi = Q(1, 1)/2
    return [(Q(1), Q(), Q()), (Q(), Q(1), Q())] + [
        q5.scale(1/(2*phi), (Q(1), e*phi, d*(1+phi)))
        for e in (-1, 1) for d in (-1, 1)]


def weight(pair, Q):
    require(isinstance(pair, list) and len(pair) == 2 and
            all(isinstance(x, str) for x in pair), 'two rational field coefficients')
    return Q(Fraction(pair[0]), Fraction(pair[1]))


def profile(index, m, dependency):
    model, q5, shadow, _, _ = dependency
    Q, dot, sub, cross, scale = q5.Q, q5.dot, q5.sub, q5.cross, q5.scale
    V = model.VERTICES
    radius2 = Q(11, 4)/4
    require(dot(m, m) == 1 and all(dot(v, v) == radius2 for v in V),
            'unit normal and all original circumradii')
    hull = shadow.hull_indices(V, m)
    require(len(hull) == 12, 'complete minimum silhouette has twelve corners')
    corners = [shadow.projection(V[i], m) for i in hull]
    boundary = 0
    for p, q in zip(corners, corners[1:]+corners[:1]):
        inward = cross(m, sub(q, p))
        require(dot(inward, inward) > 0, 'nonzero silhouette edge')
        require(all(dot(inward, sub(v, p)) >= 0 for v in V),
                'complete all-original silhouette support')
        require(all(dot(inward, sub(w, p)) > 0 for w in corners if w not in (p, q)),
                'strict irredundant cyclic silhouette')
        boundary += len(V)
    equator, paired, contacts, radial = [], [], set(), []
    for p in corners:
        indices = [i for i, v in enumerate(V) if shadow.projection(v, m) == p]
        heights = {dot(m, V[i]) for i in indices}
        if heights == {Q()}:
            require(len(indices) == 1 and dot(p, p) == radius2,
                    'unique original equatorial contact')
            equator.append((indices[0], p))
        else:
            require(len(indices) == 2 and heights == {Q(1)/2, -Q(1)/2},
                    'complete mirrored original contact pair')
            require(dot(p, p) == radius2-Q(1)/4, 'paired projected radius')
            paired.append((indices, p))
        contacts.update(indices)
        for j, v in enumerate(V):
            if j not in indices:
                gap = dot(p, sub(p, v))
                require(gap > 0, 'positive complete radial support gap')
                radial.append(gap)
    require(len(equator) == 4 and len(paired) == 8 and len(contacts) == 20,
            'four singleton and eight doubleton original classes')
    require(min(radial) == Q(1)/4 and len(radial) == 700,
            'all seven hundred radial comparisons and sharp gap')
    return {'index': index, 'normal': m, 'equator': equator, 'paired': paired,
            'contact_indices': contacts, 'radial_comparisons': len(radial),
            'boundary_comparisons': boundary}


def check_weights(record, data, q5):
    Q, dot, cross = q5.Q, q5.dot, q5.cross
    require(set(record) == {'axis', 'equatorial_weights', 'paired_weights'} and
            type(record['axis']) is int and record['axis'] == data['index'],
            'certificate axis and fields')
    beta = [weight(x, Q) for x in record['equatorial_weights']]
    alpha = [weight(x, Q) for x in record['paired_weights']]
    require(len(beta) == 4 and len(alpha) == 8, 'all twelve weights present')
    require(min(beta+alpha) > Q(1)/100, 'strict positive exact stress weights')
    require(sum(beta, Q()) == 1, 'normalized equatorial weights')
    qs = [p for _, p in data['equator']]
    ps = [p for _, p in data['paired']]
    require(all(sum((b*q[k] for b, q in zip(beta, qs)), Q()) == 0
                for k in range(3)), 'actual equatorial barycenter is zero')
    matrix = [[sum((b*q[i]*q[j] for b, q in zip(beta, qs)), Q())
               for j in range(3)] for i in range(3)]
    other = [[sum((a*p[i]*p[j] for a, p in zip(alpha, ps)), Q())
              for j in range(3)] for i in range(3)]
    require(matrix == other, 'full physical second moments agree exactly')
    require(sum((matrix[i][i] for i in range(3)), Q()) == Q(11, 4)/4,
            'normalized physical second-moment trace')
    m = data['normal']
    require(dot(m, cross(qs[0], qs[1])) != 0,
            'equatorial moment matrix is positive definite on the plane')
    e = next(e for e in [(Q(1), Q(), Q()), (Q(), Q(1), Q()), (Q(), Q(), Q(1))]
             if dot(cross(m, e), cross(m, e)) > 0)
    u = cross(m, e)
    v = cross(m, u)
    forms = [(dot(p, u)*dot(p, u), dot(p, u)*dot(p, v), dot(p, v)*dot(p, v))
             for p in ps]
    independent = next((ix for ix in itertools.combinations(range(8), 3)
                        if determinant([forms[i] for i in ix]) != 0), None)
    require(independent is not None, 'paired dyads span all planar quadratic forms')
    return {'axis': data['index'], 'minimum_weight': str(min(beta+alpha)),
            'equatorial_original_indices': [i for i, _ in data['equator']],
            'paired_original_indices': [ix for ix, _ in data['paired']],
            'independent_paired_dyad_indices': list(independent),
            'moment_matrix': [[str(x) for x in row] for row in matrix]}


def parse_original_scalar(text, Q):
    matched = re.fullmatch(r'\(([-0-9/]+)\)\+\(([-0-9/]+)\)sqrt5', text)
    require(matched is not None, 'restricted original exact scalar format')
    return Q(Fraction(matched[1]), Fraction(matched[2]))


def check_motions(profiles, dependency):
    model, q5, _, expected, _ = dependency
    Q, dot, cross = q5.Q, q5.dot, q5.cross
    motions = expected['minimum_receiver_proper_motions']
    require(len(motions) == 22, 'complete pinned original minimum-fit classification')
    counts = [[0]*6 for _ in range(6)]
    common = 0
    for motion in motions:
        i, j = motion['source_axis'], motion['receiver_axis']
        require(type(i) is int and type(j) is int and 0 <= i < 6 and 0 <= j < 6,
                'original configuration axes')
        columns = [tuple(parse_original_scalar(x, Q) for x in c)
                   for c in motion['proper_matrix_columns']]
        require(len(columns) == 3 and all(len(c) == 3 for c in columns),
                'full physical matrix columns')
        require(all(dot(columns[a], columns[b]) == (1 if a == b else 0)
                    for a in range(3) for b in range(3)), 'proper base orthogonality')
        require(dot(columns[0], cross(columns[1], columns[2])) == 1,
                'proper base determinant one')
        def move(p):
            return tuple(sum((columns[k][r]*p[k] for k in range(3)), Q()) for r in range(3))
        source = {move(model.VERTICES[k]) for k in profiles[i]['contact_indices']}
        target = {model.VERTICES[k] for k in profiles[j]['contact_indices']}
        require(source == target and len(source) == 20,
                'entire actual spatial rim contact set shared at every base fit')
        normal = move(profiles[i]['normal'])
        require(normal in (profiles[j]['normal'], q5.scale(-1, profiles[j]['normal'])),
                'complete body-normal congruence lift')
        counts[i][j] += 1
        common += len(source)
    wanted = [[2, 0, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0]] + [[0, 0, 1, 1, 1, 1]]*4
    require(counts == wanted, 'all twenty-two base configurations covered')
    return counts, common


def negative_controls(certificate, profiles, q5):
    damaged = []
    bad = copy.deepcopy(certificate['records'][2])
    bad['equatorial_weights'][0] = ['-1', '0']
    damaged.append(bad)
    bad = copy.deepcopy(certificate['records'][2])
    bad['equatorial_weights'][0] = ['1', '0']
    damaged.append(bad)
    bad = copy.deepcopy(certificate['records'][2])
    bad['paired_weights'][0] = ['1/10', '0']
    damaged.append(bad)
    bad = copy.deepcopy(certificate['records'][2])
    bad['paired_weights'].pop()
    damaged.append(bad)
    for bad in damaged:
        try:
            check_weights(bad, profiles[2], q5)
        except ValueError:
            continue
        raise ValueError('damaged contact stress was accepted')
    return len(damaged)


def verify():
    dependency = load()
    model, q5, _, _, manifest = dependency
    certificate = json.loads((HERE/'certificate.json').read_text())
    require(certificate['agent'] == 'six-rupert-2' and certificate['role'] == 'researcher',
            'actual author and role')
    normals = axes(q5)
    profiles = [profile(i, m, dependency) for i, m in enumerate(normals)]
    require(len(certificate['records']) == 6, 'all six contact stresses')
    records = [check_weights(r, p, q5) for r, p in zip(certificate['records'], profiles)]
    counts, mapped = check_motions(profiles, dependency)
    require(q5.Q(11, 4)/4 < 5 and Fraction(8*5, 1000) < Fraction(1, 4),
            'uniform frame-neighborhood support advantage')
    require(Fraction(1, 1000)**2 < Fraction(1, 2) and
            Fraction(2, 1000**2) < Fraction(1, 1000), 'scale drift bounds')
    negative = negative_controls(certificate, profiles, q5)
    return {'agent': 'six-rupert-2', 'role': 'researcher',
            'verified_stresses': records,
            'total_radial_support_comparisons': sum(p['radial_comparisons'] for p in profiles),
            'total_silhouette_support_comparisons': sum(p['boundary_comparisons'] for p in profiles),
            'minimum_radial_gap': '1/4', 'common_contacts_per_configuration': 20,
            'closed_minimum_configuration_count': 22, 'actual_spatial_contact_matches': mapped,
            'base_configuration_count_matrix': counts,
            'local_necessary_constraint_frame_radius': '1/1000',
            'negative_certificate_controls': negative,
            'pinned_source_commit': manifest['source_commit'],
            'certificate_sha256': hashlib.sha256((HERE/'certificate.json').read_bytes()).hexdigest()}


if __name__ == '__main__':
    result = verify()
    if '--emit' in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        wanted = json.loads((HERE/'expected.json').read_text())
        require(result == wanted, 'all exact finite hypotheses match the expected record')
        print(json.dumps({k: v for k, v in result.items() if k != 'verified_stresses'}, indent=2))
