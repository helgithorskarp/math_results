#!/usr/bin/env python3
"""Exact endpoint classification. No old motion/no-lift checker is executed.

CPython3.11, standard library. No arguments checks EXPECTED.json; one JSON
path classifies two supplied full-dimensional rigid endpoint groups.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def sub(a, b):
    return [x-y for x, y in zip(a, b)]


def add(a, b):
    return [x+y for x, y in zip(a, b)]


def scale(a, s):
    return [s*x for x in a]


def norm(a):
    return dot(a, a)


def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


def eye(n=3):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return list(map(list, zip(*a)))


def mv(a, x):
    return [dot(row, x) for row in a]


def mm(a, b):
    bt = transpose(b)
    return [[dot(row, col) for col in bt] for row in a]


def ms(a, b):
    return [sub(x, y) for x, y in zip(a, b)]


def det(a):
    return dot(a[0], cross(a[1], a[2]))


def inverse(a):
    d = det(a)
    need(d != 0, 'singular matrix')
    return transpose([scale(cross(a[1], a[2]), 1/d),
                      scale(cross(a[2], a[0]), 1/d),
                      scale(cross(a[0], a[1]), 1/d)])


def basis(rows):
    ans = []
    for row in rows:
        v = row[:]
        for u in ans:
            v = sub(v, scale(u, dot(v, u)/norm(u)))
        if norm(v):
            ans.append(v)
    return ans


def rank(rows):
    return len(basis(rows))


def fit(source, target):
    need(len(source) >= 4 and len(source) == len(target), 'group sizes')
    directions, images = [], []
    for x, y in zip(source[1:], target[1:]):
        u = sub(x, source[0])
        if rank(directions+[u]) > len(directions):
            directions.append(u)
            images.append(sub(y, target[0]))
        if len(directions) == 3:
            break
    need(len(directions) == 3, 'group must affinely span R3')
    q = mm(transpose(images), inverse(transpose(directions)))
    t = sub(target[0], mv(q, source[0]))
    need(mm(transpose(q), q) == eye(), 'group is not rigid')
    need(all(add(mv(q, x), t) == y for x, y in zip(source, target)),
         'group endpoint does not match its rigid anchors')
    return q, t


def rational(v):
    need(isinstance(v, (str, int)) and not isinstance(v, bool), 'rational input required')
    return F(v)


def parse(data):
    need(isinstance(data, dict) and set(data) == {'groups'}, 'expected groups object')
    need(isinstance(data['groups'], list) and len(data['groups']) == 2, 'two groups required')
    groups = []
    for g in data['groups']:
        need(isinstance(g, dict) and set(g) == {'source', 'target'}, 'group fields')
        x = [[rational(a) for a in row] for row in g['source']]
        y = [[rational(a) for a in row] for row in g['target']]
        need(all(len(row) == 3 for row in x+y), 'three coordinates required')
        groups.append((x, y))
    return groups


def derivative_rank(groups):
    """Independent linear orbit-contact system in twelve generator variables."""
    rows = []
    e = eye()
    for x, y in groups:
        for i in range(len(x)):
            for j in range(len(x)):
                if i == j:
                    continue
                dx, dy = sub(x[i], x[j]), sub(y[i], y[j])
                rows.append([dot(dx, cross(e[k], x[i])) for k in range(3)]
                            + dx
                            + [-dot(dy, cross(e[k], y[i])) for k in range(3)]
                            + scale(dy, -1))
    return rank(rows)


def classify(data):
    groups = parse(data)
    qa, ta = fit(*groups[0]); qb, tb = fit(*groups[1])
    q = mm(transpose(qa), qb)
    t = mv(transpose(qa), sub(tb, ta))
    need(det(q) == 1, 'relative orientation must be proper')
    a, b = groups[0][0], groups[1][0]
    x = a+b
    y = a+[add(mv(q, u), t) for u in b]
    losses = [norm(sub(x[i], x[j]))-norm(sub(y[i], y[j]))
              for i, j in combinations(range(len(x)), 2)]
    need(min(losses) >= 0, 'endpoint expansion')
    crossloss = [norm(sub(u, w))-norm(sub(u, add(mv(q, w), t))) for u in a for w in b]
    paired = [u+v for u, v in zip(x, y)]
    paired_rank = rank([sub(z, paired[0]) for z in paired[1:]])
    generator_rank = derivative_rank(groups)
    output = {'sites': len(x), 'endpoint_pairs': len(losses),
              'tight_pairs': sum(v == 0 for v in losses),
              'paired_affine_rank': paired_rank,
              'orbit_derivative_rank': generator_rank,
              'minimum_cross_loss': str(min(crossloss)),
              'relative_rotation': serial(q), 'relative_translation': serial(t)}
    if q == eye():
        trivial = norm(t) == 0
        need(paired_rank == (3 if trivial else 4), 'translation paired rank')
        need(generator_rank == (6 if trivial else 8), 'translation generator rank')
        output.update(relative_type='identity' if trivial else 'translation',
                      equivariant_completion=True, untwisted_completion=True,
                      norm_anchors=trivial, scalar_defect=True)
        return output
    qm = ms(q, eye())
    w = next((cross(qm[i], qm[j]) for i, j in combinations(range(3), 2)
              if norm(cross(qm[i], qm[j]))), None)
    need(w is not None, 'nonidentity rotation axis')
    w2 = norm(w)
    p = [[w[i]*w[j]/w2 for j in range(3)] for i in range(3)]
    perpendicular = ms(eye(), p)
    v = mv(p, t)
    h2 = norm(v)
    c = mv(inverse([add(row, pp) for row, pp in zip(ms(eye(), q), p)]),
           mv(perpendicular, t))
    need(mv(p, c) == [0]*3 and sub(add(mv(q, c), t), c) == v, 'axis identity')
    chi = 3-sum(q[i][i] for i in range(3))
    need(chi > 0, 'rotation chord factor')
    orbit = []
    for i, u in enumerate(a):
        for j, z in enumerate(b):
            ua, ub = mv(perpendicular, sub(u, c)), mv(perpendicular, sub(z, c))
            ra2, rb2 = norm(ua), norm(ub)
            ell = 2*dot(v, sub(u, z))-h2
            bound2 = 4*chi*ra2*rb2
            # Independent sine/cosine reconstruction of the circular minimum.
            cosine = dot(ua, mv(qm, ub))
            sine_unscaled = dot(ua, mv(qm, cross(w, ub)))
            amplitude2 = cosine*cosine+sine_unscaled*sine_unscaled/w2
            need(amplitude2 == chi*ra2*rb2, 'orbit amplitude identity')
            need(ell+2*cosine == norm(sub(u, z))-norm(sub(u, add(mv(q, z), t))),
                 'displayed azimuth loss identity')
            orbit.append({'pair': [i, j], 'ell': str(ell), 'squared_margin': str(ell*ell-bound2),
                          'passes': ell >= 0 and ell*ell >= bound2})
    completion = all(o['passes'] for o in orbit)
    need(paired_rank == (6 if h2 else 5), 'screw paired rank')
    need(generator_rank == 10, 'screw generator rank')
    if not h2:
        need(not completion, 'zero-pitch exclusion')
    output.update(relative_type='pitched_screw' if h2 else 'zero_pitch_rotation',
                  axis_projection=serial(p), axis_base=serial(c), axial_translation=serial(v),
                  pitch_squared=str(h2), chord_factor=str(chi),
                  equivariant_completion=completion, untwisted_completion=False,
                  norm_anchors=not bool(h2), scalar_defect=min(crossloss) >= h2,
                  orbit_pairs=len(orbit), failed_orbit_pairs=sum(not o['passes'] for o in orbit),
                  minimum_orbit_squared_margin=str(min(F(o['squared_margin']) for o in orbit)),
                  first_failed_orbit=next((o for o in orbit if not o['passes']), None))
    return output


def serial(data):
    if isinstance(data, F):
        return str(data)
    if isinstance(data, dict):
        return {k: serial(v) for k, v in data.items()}
    if isinstance(data, (list, tuple)):
        return [serial(v) for v in data]
    return data


QUARTER = [[F(v) for v in row] for row in [(0, -1, 0), (1, 0, 0), (0, 0, 1)]]


def control8(q=QUARTER, shift=None, pure=False):
    if shift is None:
        shift = [F(0), F(0), F(1)]
    a = [[F(v) for v in row] for row in
         ([(0, 0, F(3, 2)), (1, 0, F(3, 2)), (0, 1, F(3, 2)), (0, 0, F(5, 2))]
          if not pure else [(-2, 0, 2), (-3, 0, 2), (-2, 1, 2), (-2, 0, 3)])]
    b = [[F(v) for v in row] for row in [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]]
    return {'groups': [{'source': a, 'target': a},
                       {'source': b, 'target': [add(mv(q, x), shift) for x in b]}]}


def control24():
    file = HERE/'../gaussian_two_body_screw_obstruction/WITNESS.json'
    sites = json.loads(file.read_text())['sites']
    return {'groups': [{'source': [s['source'] for s in sites if s['group'] == g],
                        'target': [s['target'] for s in sites if s['group'] == g]}
                       for g in ('A', 'B')]}


def reframe(data):
    p = [[F(v) for v in row] for row in [(0, 0, 1), (1, 0, 0), (0, 1, 0)]]
    o = [[F(v) for v in row] for row in [(1, 0, 0), (0, 0, 1), (0, 1, 0)]]
    need(det(p) == 1 and det(o) == -1, 'proper/improper independent frame control')
    answer = {'groups': []}
    for x, y in parse(serial(data)):
        answer['groups'].append({'source': [add(mv(p, v), [F(2), F(-3), F(5)]) for v in x],
                                 'target': [add(mv(o, v), [F(-7), F(4), F(1)]) for v in y]})
    return answer


def dependency_checks():
    data = json.loads((HERE/'INPUTS.json').read_text())
    for entry in data['files']:
        digest = hashlib.sha256((HERE/entry['path']).read_bytes()).hexdigest()
        need(digest == entry['sha256'], 'dependency content changed: '+entry['path'])
    return len(data['files'])


def controls():
    pinned = dependency_checks()
    examples = {'positive_R5_screw': control8(), 'obstructed_R5_screw': control24(),
                'zero_pitch_rotation': control8(shift=[F(0)]*3, pure=True),
                'pure_translation': control8(q=eye()),
                'identity': control8(q=eye(), shift=[F(0)]*3)}
    records = {k: classify(serial(v)) for k, v in examples.items()}
    fields = ('paired_affine_rank', 'orbit_derivative_rank', 'equivariant_completion',
              'untwisted_completion', 'norm_anchors', 'scalar_defect')
    signatures = {
        'positive_R5_screw': (6, 10, False, False, False, False),
        'obstructed_R5_screw': (6, 10, True, False, False, False),
        'zero_pitch_rotation': (5, 10, False, False, True, True),
        'pure_translation': (4, 8, True, True, False, True),
        'identity': (3, 6, True, True, True, True)}
    for k, out in records.items():
        need(tuple(out[f] for f in fields) == signatures[k], 'classification control '+k)
    reframes = 0
    for name in ('positive_R5_screw', 'obstructed_R5_screw', 'zero_pitch_rotation'):
        out = classify(serial(reframe(examples[name])))
        need(tuple(out[f] for f in fields) == signatures[name], 'endpoint-frame invariance')
        reframes += 1
    # Explicit rational adverse orbit pair, independent of the orbit guard.
    rotated = [F(3, 5), F(-4, 5), F(3, 2)]
    b, tb = [F(1), F(0), F(0)], [F(0), F(1), F(1)]
    before, after = norm(sub(rotated, b)), norm(sub(rotated, tb))
    need((before, after, before-after) == (F(61, 20), F(77, 20), F(-4, 5)),
         'rational orbit obstruction')
    # Universal squared radius identity, checked by polynomial coefficients.
    def multiply(a, b):
        ans = {}
        for (i, j), x in a.items():
            for (k, l), y in b.items():
                ans[i+k, j+l] = ans.get((i+k, j+l), 0)+x*y
        return {m: v for m, v in ans.items() if v}
    plus = multiply({(1, 0): 1, (0, 1): 2}, {(1, 0): 1, (0, 1): 2})
    plus[1, 1] -= 8
    minus = multiply({(1, 0): 1, (0, 1): -2}, {(1, 0): 1, (0, 1): -2})
    need(plus == minus, 'universal paraboloid orbit identity')
    rejected = 0
    cases = []
    bad = serial(control8()); bad['groups'][0]['source'] = bad['groups'][0]['source'][:3]
    bad['groups'][0]['target'] = bad['groups'][0]['target'][:3]; cases.append(bad)
    bad = serial(control8()); bad['groups'][1]['target'][0][0] = '1/3'; cases.append(bad)
    bad = serial(control8()); bad['groups'][0]['source'][0][0] = 0.5; cases.append(bad)
    bad = serial(control8()); bad['groups'][1]['target'] = [[str(-F(v[0])), v[1], v[2]]
                                                          for v in bad['groups'][1]['source']]
    cases.append(bad)
    bad = serial(control8()); bad['groups'][1]['target'] = [serial(add(list(map(F, v)), [0, 0, 9]))
                                                          for v in bad['groups'][1]['source']]
    cases.append(bad)
    for case in cases:
        try:
            classify(case)
        except (ValueError, ZeroDivisionError):
            rejected += 1
        else:
            raise ValueError('invalid control accepted')
    return {'status': 'EXACT_SCREW_MERIDIAN_BOUNDARY_PASS', 'records': records,
            'independent_endpoint_reframes': reframes, 'rejected_inputs': rejected,
            'pinned_public_inputs': pinned,
            'rational_orbit_before': str(before), 'rational_orbit_after': str(after),
            'rational_orbit_loss': str(before-after),
            'paraboloid_identity': '(r_A^2-2r_B^2)^2',
            'old_motion_checks_replayed': False}


def main():
    if len(sys.argv) == 2:
        answer = classify(json.loads(Path(sys.argv[1]).read_text()))
    else:
        need(len(sys.argv) == 1, 'usage: python3 -B verify.py [INPUT.json]')
        answer = controls()
        need(answer == json.loads((HERE/'EXPECTED.json').read_text()), 'expected result mismatch')
    print(json.dumps(answer, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
