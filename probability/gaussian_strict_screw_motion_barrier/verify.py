#!/usr/bin/env python3
"""Exact controls and a finite R5-obstruction consumer; CPython3.11 stdlib.

No previous verifier is imported. The universal perturbation theorem is
the written PROOF.md, not a consequence of testing these finite controls.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
DELTA = F(1, 2**136)
ETA = F(1, 2**56)
ERR = F(1, 2**20)
FACTOR = 1-F(1, 2**145)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def dot(x, y):
    return sum((u*v for u, v in zip(x, y)), F(0))


def sub(x, y):
    return [u-v for u, v in zip(x, y)]


def distances(x):
    return [[dot(sub(u, v), sub(u, v)) for v in x] for u in x]


def determinant(a):
    a = [row[:] for row in a]
    answer = F(1)
    for j in range(len(a)):
        k = next((i for i in range(j, len(a)) if a[i][j]), None)
        if k is None:
            return F(0)
        if k != j:
            a[k], a[j] = a[j], a[k]
            answer = -answer
        pivot = a[j][j]
        answer *= pivot
        for i in range(j+1, len(a)):
            ratio = a[i][j]/pivot
            a[i] = [u-ratio*v for u, v in zip(a[i], a[j])]
    return answer


def rank(a):
    a = [row[:] for row in a]
    r = 0
    for j in range(len(a[0])):
        k = next((i for i in range(r, len(a)) if a[i][j]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        for i in range(r+1, len(a)):
            ratio = a[i][j]/a[r][j]
            a[i] = [u-ratio*v for u, v in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def serial(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {k: serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serial(v) for v in x]
    return x


def rational(x):
    need(isinstance(x, (str, int)) and not isinstance(x, bool), 'rational coordinates required')
    return F(x)


def reference():
    data = json.loads((HERE/'../gaussian_two_body_screw_obstruction/WITNESS.json').read_text())
    return [{'label': p['label'], 'group': p['group'],
             'source': list(map(F, p['source'])), 'target': list(map(F, p['target'])),
             'parameter': list(map(F, p['parameter']))} for p in data['sites']]


def make_instance(factor=FACTOR):
    return {'sites': [{'label': p['label'], 'source': p['source'],
                       'target': [factor*v for v in p['target']]} for p in reference()]}


def parse(data):
    need(isinstance(data, dict) and set(data) == {'sites'}, 'expected sites object')
    need(isinstance(data['sites'], list) and len(data['sites']) == 24, '24 labelled sites required')
    lookup = {}
    for site in data['sites']:
        need(isinstance(site, dict) and set(site) == {'label', 'source', 'target'}, 'site fields')
        label = site['label']
        need(isinstance(label, str) and label not in lookup, 'unique string labels required')
        x, y = site['source'], site['target']
        need(isinstance(x, list) and isinstance(y, list) and len(x) == len(y) == 3, 'R3 coordinates required')
        lookup[label] = [list(map(rational, x)), list(map(rational, y))]
    labels = [p['label'] for p in reference()]
    need(set(lookup) == set(labels), 'reference labels required')
    return [lookup[k][0] for k in labels], [lookup[k][1] for k in labels]


def consume(data):
    x, y = parse(data)
    ref = reference()
    px, qx = distances([p['source'] for p in ref]), distances([p['target'] for p in ref])
    dx, dy = distances(x), distances(y)
    pairs = list(combinations(range(24), 2))
    need(all(dx[i][j] > 0 for i, j in pairs), 'distinct source points required')
    losses = [dx[i][j]-dy[i][j] for i, j in pairs]
    ep = max(abs(dx[i][j]-px[i][j]) for i, j in pairs)
    eq = max(abs(dy[i][j]-qx[i][j]) for i, j in pairs)
    status = 'NO_R5_MOTION' if min(losses) >= 0 and max(ep, eq) <= DELTA else 'NOT_CERTIFIED'
    reason = 'metric_box' if status == 'NO_R5_MOTION' else ('endpoint_expansion' if min(losses) < 0 else 'outside_metric_box')
    return serial({'status': status, 'reason': reason, 'sites': 24, 'pairs': len(pairs),
                   'source_squared_distance_error': ep, 'target_squared_distance_error': eq,
                   'strict_pairs': sum(a > 0 for a in losses), 'tight_pairs': sum(a == 0 for a in losses),
                   'minimum_squared_distance_loss': min(losses),
                   'maximum_squared_distance_ratio': max(dy[i][j]/dx[i][j] for i, j in pairs)})


def polynomial_identity():
    # Direct determinant expansion in Q[alpha,v1,v2], independent of the
    # Schur-complement calculation in the manuscript.
    def add(a, b):
        out = a.copy()
        for k, v in b.items():
            out[k] = out.get(k, F(0))+v
        return {k: v for k, v in out.items() if v}
    def mul(a, b):
        out = {}
        for i, u in a.items():
            for j, v in b.items():
                k = tuple(s+t for s, t in zip(i, j))
                out[k] = out.get(k, F(0))+u*v
        return {k: v for k, v in out.items() if v}
    def scale(a, c):
        return {k: v*c for k, v in a.items() if v*c}
    one = {(0, 0, 0): F(1)}
    a, x, y = {(1, 0, 0): F(1)}, {(0, 1, 0): F(1)}, {(0, 0, 1): F(1)}
    k = add(one, scale(mul(a, a), -2))
    r2 = add(mul(x, x), mul(y, y))
    minus, plus = add(one, scale(a, -1)), add(one, a)
    c1 = add(mul(minus, x), scale(mul(plus, y), -1))
    c2 = add(mul(plus, x), mul(minus, y))
    h = [[k, {}, c1], [{}, k, c2], [c1, c2, add(scale(one, F(1, 4)), scale(r2, -1))]]
    det = {}
    for p in permutations(range(3)):
        inversions = sum(p[i] > p[j] for i in range(3) for j in range(i+1, 3))
        term = one
        for i in range(3):
            term = mul(term, h[i][p[i]])
        det = add(det, scale(term, (-1)**inversions))
    rhs = mul(k, add(scale(k, F(1, 4)), scale(r2, -3)))
    need(det == rhs, 'universal determinant polynomial')
    return {'variables': 3, 'nonzero_coefficients': len(det),
            'identity': 'det H0=(1-2alpha^2)[(1-2alpha^2)/4-3(v1^2+v2^2)]'}


def dependency_checks():
    pins = json.loads((HERE/'INPUTS.json').read_text())['files']
    for p in pins:
        need(hashlib.sha256((HERE/p['path']).read_bytes()).hexdigest() == p['sha256'], 'public input changed: '+p['path'])
    return len(pins)


def controls():
    pinned = dependency_checks()
    ref = reference()
    x, y = [p['source'] for p in ref], [p['target'] for p in ref]
    dx, dy = distances(x), distances(y)
    diameter = max(v for d in (dx, dy) for row in d for v in row)
    need(diameter == F(369, 4) and diameter < 128, 'diameter bound')
    need(max(dot(p['source'], p['source']) for p in ref if p['group'] == 'B') == 20, 'B norm bound')
    k = F(1, 16)
    scatter = {}
    for group in ('A', 'B'):
        pts = [p['source'] for p in ref if p['group'] == group]
        n = len(pts); center = [sum(v[j] for v in pts)/n for j in range(3)]
        centered = [sub(p, center) for p in pts]
        mat = [[sum(v[i]*v[j] for v in centered)-(k if i == j else 0) for j in range(3)] for i in range(3)]
        minors = [determinant([row[:m] for row in mat[:m]]) for m in (1, 2, 3)]
        need(all(t > 0 for t in minors), 'scatter floor')
        scatter[group] = serial(minors)
    # Exact arithmetic for every slack used in the perturbation proof.
    root_delta, root_eta = F(1, 2**68), F(1, 2**28)
    guards = {
        'sqrt_delta': root_delta**2 == DELTA,
        'sqrt_eta': root_eta**2 == ETA,
        'polar_invertibility': 2*16*DELTA/k < F(1, 2),
        'polar_error_budget': DELTA <= k*k/(12*16*128),
        'pointwise_error': 3*16**2 < 32**2,
        'pair_displacement': 64*root_delta <= 1,
        'rigidified_interval': DELTA+1600*root_delta < ETA,
        'distance_cap': 128+ETA < 12**2,
        'axis_rotation': 2*ETA/3 <= root_eta**2,
        'axis_interval': ETA+145*root_eta < ERR,
        'height_error': 4800*root_delta < ERR,
        'endpoint_height_crossing': 3*DELTA < F(1, 2),
        'v_probe': F(1, 16)+5*ERR <= F(9, 128),
        'alpha_probe': F(1, 8)+14*ERR <= F(9, 64),
        'gram_entry': 1+12*ERR <= 2,
        'strict_example_radius': (1-FACTOR**2)*128 < DELTA,
    }
    need(all(guards.values()), 'perturbation constant guard')
    k_floor = 1-2*F(41, 64)**2
    v_ceiling = 2*F(9, 128)**2
    det_floor = k_floor*(k_floor/4-3*v_ceiling)
    det_error = 6*3*12*4*ERR
    need((k_floor, v_ceiling, det_floor-det_error) ==
         (F(367, 2048), F(81, 8192), F(7921, 2**22)), 'determinant margin')
    need(det_floor > det_error, 'rank-three contradiction margin')
    # Distance functional reconstructed from the actual labelled points.
    lookup = {(p['group'], tuple(p['parameter'])): i for i, p in enumerate(ref)}
    a0, ap, am, b0 = [lookup[v] for v in [('A', (F(0), F(0))), ('A', (F(1), F(-1))),
                                        ('A', (F(-1), F(1))), ('B', (F(0), F(0)))]]
    r = {b0: F(1), a0: F(-3, 2), ap: F(1, 4), am: F(1, 4)}
    s = {a0: F(-1), ap: F(1, 2), am: F(1, 2)}
    heights = [-sum(ri*sj*d[i][j] for i, ri in r.items() for j, sj in s.items())/2 for d in (dx, dy)]
    need(heights == [0, 1] and sum(abs(v) for v in r.values())*sum(abs(v) for v in s.values())/2 == 3, 'intrinsic height')
    required_probes = [(F(1, 4), F(0)), (F(0), F(1, 4)), (F(5, 4), F(-1))]
    need(all(('A', p) in lookup for p in required_probes), 'probe sites')
    # The saved strict input is reconstructed, not trusted as an oracle.
    witness = json.loads((HERE/'WITNESS.json').read_text())
    need(witness == serial(make_instance()), 'saved strict witness changed')
    strict = consume(witness); original = consume(serial(make_instance(F(1))))
    need(strict['status'] == original['status'] == 'NO_R5_MOTION', 'metric-box controls')
    need(strict['strict_pairs'] == 276 and strict['tight_pairs'] == 0, 'strict endpoint input')
    need(F(strict['maximum_squared_distance_ratio']) == FACTOR**2, 'exact Lipschitz factor')
    need(original['tight_pairs'] == 156, 'reference contacts')
    xx, yy = parse(witness)
    norm_matrix = [p+q+[F(1), dot(p, p)-dot(q, q)] for p, q in zip(xx, yy)]
    anchor_rank = rank(norm_matrix)
    need(anchor_rank == 8, 'strict norm-anchor obstruction')
    paired_rank = rank([row[:7] for row in norm_matrix])-1
    need(paired_rank == 6, 'strict paired affine rank')
    frame = {'sites': [{'label': p['label'],
                       'source': [p['source'][2]+2, p['source'][0]-3, p['source'][1]+5],
                       'target': [p['target'][0]-7, p['target'][2]+4, p['target'][1]+1]}
                      for p in make_instance()['sites']]}
    need(consume(serial(frame)) == strict, 'independent endpoint isometries')
    # Known R3-positive inputs must lie outside this negative guard.
    outside = {}
    for name, factor in (('identity', F(1)), ('global_homothety', F(1, 2))):
        data = {'sites': [{'label': p['label'], 'source': p['source'],
                           'target': [factor*v for v in p['source']]} for p in ref]}
        ans = consume(serial(data))
        need(ans['status'] == 'NOT_CERTIFIED' and ans['reason'] == 'outside_metric_box', 'positive control excluded')
        outside[name] = ans['status']
    malformed = []
    bad = serial(make_instance()); bad['sites'][0]['source'][0] = 0.5; malformed.append(bad)
    bad = serial(make_instance()); bad['sites'][0]['label'] = bad['sites'][1]['label']; malformed.append(bad)
    bad = serial(make_instance()); bad['sites'].pop(); malformed.append(bad)
    rejected = 0
    for data in malformed:
        try:
            consume(data)
        except (ValueError, ZeroDivisionError):
            rejected += 1
        else:
            raise ValueError('malformed input accepted')
    return serial({'status': 'STRICT_SCREW_R5_BARRIER_PASS', 'reference_diameter_squared': diameter,
                   'metric_box_radius': DELTA, 'scale_factor': FACTOR,
                   'scatter_floor_minors': scatter, 'constant_guards': len(guards),
                   'halfway_heights': heights, 'determinant_polynomial': polynomial_identity(),
                   'gram_determinant_floor': det_floor, 'determinant_error_bound': det_error,
                   'remaining_determinant_margin': det_floor-det_error,
                   'strict_control': strict, 'original_control': original,
                   'strict_anchor_augmented_rank': anchor_rank,
                   'paired_affine_rank': paired_rank,
                   'independent_frame_controls': 1, 'positive_controls': outside,
                   'malformed_inputs_rejected': rejected, 'public_input_pins': pinned,
                   'old_motion_checkers_replayed': False,
                   'mixed_chain_radius_certified': False, 'gaussian_sign_certified': False})


def main():
    if len(sys.argv) == 2:
        dependency_checks()
        answer = consume(json.loads(Path(sys.argv[1]).read_text()))
    else:
        need(len(sys.argv) == 1, 'usage: python3 -B verify.py [CANDIDATE.json]')
        answer = controls()
        need(answer == json.loads((HERE/'EXPECTED.json').read_text()), 'expected record mismatch')
    print(json.dumps(answer, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
