#!/usr/bin/env python3
"""Literal closed-contact fan hypotheses for J74 local mirror rigidity.

No hull finder, contact search, solver or floating-point arithmetic is used.
The continuous bilinear and compactness arguments are written in PROOF.md.
"""
import copy
from fractions import Fraction
from functools import cmp_to_key
import hashlib
from itertools import combinations
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
    required = {'q5.py', 'model.py', 'shadow.py', 'PROOF.md', 'expected.json',
                'boundary_prototypes/PROOF.md', 'boundary_prototypes/certificate.json',
                'boundary_prototypes/expected.json'}
    require(set(manifest['sha256']) == required, 'complete pinned dependency inputs')
    for name, digest in manifest['sha256'].items():
        require(hashlib.sha256((parent/name).read_bytes()).hexdigest() == digest,
                'changed pinned input: '+name)
    sys.path.insert(0, str(parent))
    import q5
    import model
    boundary = json.loads((parent/'boundary_prototypes/expected.json').read_text())
    return model, q5, boundary, manifest


def determinant(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def scalar(text, Q):
    require(isinstance(text, str), 'literal field string')
    match = re.fullmatch(r'\(([-0-9/]+)\)\+\(([-0-9/]+)\)sqrt5', text)
    require(match is not None, 'restricted exact field scalar')
    return Q(Fraction(match[1]), Fraction(match[2]))


def indices(xs, n):
    require(isinstance(xs, list) and all(type(x) is int and 0 <= x < n for x in xs)
            and len(set(xs)) == len(xs), 'distinct valid literal original indices')
    return xs


def unit_axes(q5):
    Q = q5.Q
    phi = Q(1, 1)/2
    return [(Q(1), Q(), Q()), (Q(), Q(1), Q()),
            q5.scale(1/(2*phi), (Q(1), -phi, -(1+phi)))]


def verify_profile(record, axis, inputs):
    model, q5, boundary, _ = inputs
    Q, add, sub, dot, cross, scale = q5.Q, q5.add, q5.sub, q5.dot, q5.cross, q5.scale
    V = model.VERTICES
    m = unit_axes(q5)[axis]
    require(set(record) == {'axis', 'equatorial_original_indices', 'equatorial_weights',
                            'receiver_wall_rays', 'fans'} and record['axis'] == axis,
            'complete representative profile')
    require(dot(m, m) == 1, 'physical unit minimum normal')
    def project(v):
        return sub(v, scale(dot(m, v), m))
    def vector(xs):
        require(isinstance(xs, list) and len(xs) == 3, 'three exact physical coordinates')
        return tuple(scalar(x, Q) for x in xs)
    def norm1(v):
        return sum((x if x >= 0 else -x for x in v), Q())
    radius2 = Q(11, 4)/4
    W = set(boundary['profiles'][axis]['boundary_original_indices'])
    qix = indices(record['equatorial_original_indices'], len(V))
    require(set(qix) == {i for i, v in enumerate(V) if dot(m, v) == 0} and len(qix) == 4,
            'all four actual equatorial originals')
    require(set(qix).issubset(W), 'equatorial originals belong to the actual prototype')
    beta = []
    for pair in record['equatorial_weights']:
        require(isinstance(pair, list) and len(pair) == 2 and
                all(isinstance(x, str) for x in pair), 'two literal rational weight coefficients')
        beta.append(Q(Fraction(pair[0]), Fraction(pair[1])))
    require(len(beta) == 4 and min(beta) > 0 and sum(beta, Q()) == 1,
            'positive normalized actual singleton stress')
    require(all(sum((b*V[i][k] for b, i in zip(beta, qix)), Q()) == 0 for k in range(3)),
            'actual singleton barycenter zero')
    require(dot(m, cross(V[qix[0]], V[qix[1]])) != 0, 'singleton span of the physical plane')
    M = [[sum((b*V[i][j]*V[i][k] for b, i in zip(beta, qix)), Q())
          for k in range(3)] for j in range(3)]
    P = [[Q(j == k)-m[j]*m[k] for k in range(3)] for j in range(3)]
    A = [[P[j][k]-M[j][k]/radius2 for k in range(3)] for j in range(3)]
    require(sum((M[j][j] for j in range(3)), Q()) == radius2, 'physical moment trace')
    traceA = sum((A[j][j] for j in range(3)), Q())
    require(traceA == 1 and all(sum((A[j][k]*m[k] for k in range(3)), Q()) == 0
                              for j in range(3)), 'normalized planar bilinear matrix')
    planar_det = (traceA*traceA-sum((A[j][k]*A[k][j] for j in range(3) for k in range(3)), Q()))/2
    require(planar_det > 0, 'bilinear matrix positive definite on the physical plane')
    def metric(a, b):
        return sum((a[j]*A[j][k]*b[k] for j in range(3) for k in range(3)), Q())
    def valid_ray(v):
        require(dot(m, v) == 0 and norm1(v) == 1, 'nonzero physical l1-normalized tangent ray')
        return v
    rays = [valid_ray(vector(v)) for v in record['receiver_wall_rays']]
    require(len(rays) >= 3 and len(set(rays)) == len(rays), 'distinct complete receiver-wall cycle')
    e1 = project((Q(), Q(1), Q()))
    if dot(e1, e1) == 0:
        e1 = project((Q(), Q(), Q(1)))
    e2 = cross(m, e1)
    def half(v):
        x, y = dot(e1, v), dot(e2, v)
        return 0 if y > 0 or (y == 0 and x >= 0) else 1
    def compare(a, b):
        if half(a) != half(b):
            return -1 if half(a) < half(b) else 1
        return -dot(m, cross(a, b)).sign()
    require(rays == sorted(rays, key=cmp_to_key(compare)), 'single ordered polar circle coverage')
    require(all(dot(m, cross(a, b)) > 0 for a, b in zip(rays, rays[1:]+rays[:1])),
            'all closed angular intervals have width strictly below pi')
    require(len(record['fans']) == len(rays) and
            [f['interval'] for f in record['fans']] ==
            [[i, (i+1) % len(rays)] for i in range(len(rays))],
            'each closed circular interval covered exactly once including the wrap')
    fans = []
    supports = 0
    corners = []
    for index, fan in enumerate(record['fans']):
        require(set(fan) == {'interval', 'original_edges', 'critical_tilt_rays'},
                'complete literal contact fan')
        d0, d1 = (rays[i] for i in fan['interval'])
        rows = []
        edge_list = fan['original_edges']
        require(isinstance(edge_list, list) and len({tuple(e) for e in edge_list}) == len(edge_list),
                'distinct actual selected edges')
        for edge in edge_list:
            require(len(indices(edge, len(V))) == 2 and set(edge).issubset(W),
                    'two actual prototype originals per contact edge')
            a, b = edge
            delta = sub(V[b], V[a])
            require(dot(delta, delta) == 1, 'actual original unit edge')
            h = dot(cross(delta, m), V[a])
            require(h > 0, 'positive fixed support normalization')
            m0 = scale(1/h, cross(delta, m))
            for direction in ((Q(), Q(), Q()), d0, d1):
                u = add(m, scale(Fraction(1, 100), direction))
                normal = scale(1/h, cross(delta, u))
                require(dot(normal, u) == 0 and dot(normal, V[a]) > 0,
                        'nonzero physical projected supporting direction')
                require(all(dot(normal, sub(V[a], v)) >= 0 for v in V),
                        'all sixty originals enclosed at every closed triangle corner')
                supports += len(V)
            for source in edge:
                require(dot(m0, V[source]) == 1, 'actual source contact at the base')
                rows.append({'source': source, 'edge': edge, 'm0': m0,
                             'g0': cross(V[source], m0), 'k': dot(delta, m)/h})
        common = []
        for source, weight in zip(qix, beta):
            pair = [row for row in rows if row['source'] == source]
            require(len(pair) == 2, 'two retained actual edges at every equatorial contact')
            left, right = [row['m0'] for row in pair]
            require(dot(m, cross(left, right)) != 0, 'independent actual singleton support lines')
            difference = sub(left, right)
            wanted = scale(1/radius2, V[source])
            theta = dot(sub(wanted, right), difference)/dot(difference, difference)
            require(0 < theta < 1 and add(scale(theta, left), scale(1-theta, right)) == wanted,
                    'strict positive actual radial normal decomposition')
            common += [(pair[0], weight*theta), (pair[1], weight*(1-theta))]
        require(sum((weight for _, weight in common), Q()) == 1,
                'normalized positive common weights')
        require(all(sum((weight*row[key][k] for row, weight in common), Q()) == 0
                    for key in ('m0', 'g0') for k in range(3)),
                'physical common translation and torque balances')
        require(all(project(row['g0']) == (Q(), Q(), Q()) for row, _ in common),
                'common torques involve only axial rotation')
        S = [[sum((weight*V[row['source']][j]*row['m0'][k] for row, weight in common), Q())
              for k in range(3)] for j in range(3)]
        require(S == [[x/radius2 for x in row] for row in M],
                'all actual common second-moment entries')
        linear = [[dot(row['g0'], m), dot(row['m0'], e1), dot(row['m0'], e2)]
                  for row, _ in common]
        rank_ix = next((ix for ix in combinations(range(8), 3)
                        if determinant([linear[i] for i in ix]) != 0), None)
        require(rank_ix is not None, 'common rows span all actual normal and translation variables')
        a0, a1 = [valid_ray(vector(v)) for v in fan['critical_tilt_rays']]
        require(dot(m, cross(a0, a1)) != 0, 'independent actual critical tilt generators')
        require(all(dot(row['g0'], a) <= 0 for row in rows for a in (a0, a1)),
                'both critical rays satisfy every original contact inequality')
        facet_ix = []
        for a, other in ((a0, a1), (a1, a0)):
            found = next((i for i, row in enumerate(rows)
                          if dot(row['g0'], a) < 0 and dot(row['g0'], other) == 0), None)
            require(found is not None, 'actual facet cuts the negative critical coordinate')
            facet_ix.append(found)
        values = [metric(a, b) for a in (a0, a1) for b in (a0, a1)]
        require(min(values) > Q(1)/20, 'every exact bilinear cone corner exceeds one twentieth')
        corners += values
        B = [sum((weight*row['k']*V[row['source']][j] for row, weight in common), Q())
             for j in range(3)]
        Kc = sum((weight*row['k'] for row, weight in common), Q())
        fans.append({'fan': index, 'actual_edges': len(edge_list), 'actual_contact_rows': len(rows),
                     'common_rank_indices': list(rank_ix),
                     'common_rank_determinant': str(determinant([linear[i] for i in rank_ix])),
                     'critical_facet_contact_indices': facet_ix,
                     'bilinear_corners': [str(x) for x in values],
                     'B': [str(x) for x in B], 'Kc': str(Kc)})
    return {'axis': axis, 'closed_receiver_fans': len(fans), 'all_original_support_checks': supports,
            'minimum_bilinear_corner': str(min(corners)),
            'physical_moment_matrix': [[str(x) for x in row] for row in M],
            'bilinear_planar_determinant': str(planar_det), 'fans': fans}


def verify():
    inputs = load()
    model, q5, _, manifest = inputs
    Q, dot = q5.Q, q5.dot
    radius2 = Q(11, 4)/4
    require(len(model.VERTICES) == len(set(model.VERTICES)) == 60 and
            all(dot(v, v) == radius2 for v in model.VERTICES), 'complete common-sphere original model')
    certificate = json.loads((HERE/'certificate.json').read_text())
    require(certificate['agent'] == 'six-rupert-2' and certificate['role'] == 'researcher'
            and len(certificate['records']) == 3, 'actual role and all three marked representatives')
    profiles = [verify_profile(record, axis, inputs)
                for axis, record in enumerate(certificate['records'])]
    require([p['closed_receiver_fans'] for p in profiles] == [18, 12, 16],
            'all forty-six verified closed receiver fans')
    damaged = []
    r = copy.deepcopy(certificate['records'][0]); r['fans'].pop(); damaged.append(r)
    r = copy.deepcopy(certificate['records'][0]); r['equatorial_weights'][0] = ['-1', '0']; damaged.append(r)
    r = copy.deepcopy(certificate['records'][0])
    r['fans'][0]['critical_tilt_rays'][0] = [str(-scalar(x, Q))
                                          for x in r['fans'][0]['critical_tilt_rays'][0]]
    damaged.append(r)
    r = copy.deepcopy(certificate['records'][0])
    r['fans'][0]['original_edges'][0][0] = r['fans'][0]['original_edges'][0][1]
    damaged.append(r)
    rejected = 0
    for record in damaged:
        try:
            verify_profile(record, 0, inputs)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('damaged geometric certificate accepted')
    return {'agent': 'six-rupert-2', 'role': 'researcher', 'pinned_source_commit': manifest['source_commit'],
            'certificate_sha256': hashlib.sha256((HERE/'certificate.json').read_bytes()).hexdigest(),
            'uniform_bilinear_corner_lower_bound': '1/20',
            'finite_support_triangle_ray_length': '1/100',
            'total_closed_receiver_fans': sum(p['closed_receiver_fans'] for p in profiles),
            'total_all_original_support_checks': sum(p['all_original_support_checks'] for p in profiles),
            'total_bilinear_corner_checks': sum(4*p['closed_receiver_fans'] for p in profiles),
            'negative_geometric_controls': rejected, 'profiles': profiles}


if __name__ == '__main__':
    result = verify()
    if '--emit' in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        require(result == json.loads((HERE/'expected.json').read_text()), 'complete exact finite record')
        print(json.dumps({k: v for k, v in result.items() if k != 'profiles'}, indent=2))
