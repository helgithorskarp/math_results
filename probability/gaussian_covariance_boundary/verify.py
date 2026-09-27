#!/usr/bin/env python3
"""Author algebra controls; they do not independently verify the analysis."""
import argparse
import copy
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from pathlib import Path

from certificate import finite_guard, schedule, floor_log2, ceil_log2


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def dyadic(k):
    return F(1, 1 << k) if k >= 0 else F(1 << -k)


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def n2(x):
    return sum((a*a for a in x), F(0))


def pair_loss(xs, ys, ps):
    return sum((2*ps[i]*ps[j]*(n2(sub(xs[i], xs[j]))-n2(sub(ys[i], ys[j])))
                for i, j in combinations(range(len(ps)), 2)), F(0))


def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    return sum(((-1)**j*matrix[0][j]*determinant(
        [[row[k] for k in range(len(matrix)) if k != j] for row in matrix[1:]])
        for j in range(len(matrix))), F(0))


def fixture(h):
    xs = [(-F(1, 2), -F(1, 2), 0), (0, -F(1, 2), 0),
          (F(1, 2), -F(1, 2), 0), (-F(1, 2), 0, 0),
          (F(1, 2), 0, 0), (-F(1, 2), F(1, 2), 0),
          (F(1, 2), F(1, 2), h)]
    y0 = [(0, 0, 0), (F(1, 32), 0, 0), (0, F(1, 32), 0),
          (0, 0, F(1, 32)), (0, 0, 0), (0, 0, 0),
          (F(1, 32), F(1, 32), F(1, 32))]
    ys = list(y0)
    ys[-1] = (F(1, 32), F(1, 32), F(1, 32)+h/2)
    x0 = [(x, y, F(0)) for x, y, z in xs]
    return xs, ys, [F(1, 7)]*7, x0, y0


def compact_guard(result):
    result = dict(result)
    for name in ['normalized_mean_loss', 'normalized_directional_variance']:
        value = F(result.pop(name))
        result[name+'_sha256'] = hashlib.sha256(str(value).encode()).hexdigest()
        result[name+'_bits'] = [value.numerator.bit_length(), value.denominator.bit_length()]
    return result


def controls():
    budgets = 0
    schedules = []
    for R in [1, 2, 3, 5, 8]:
        for m in [1, 2, 6, 19]:
            for k in [0, 1, 7]:
                c = schedule(R, m, k)
                q, B, Z = c['root_ceiling'], c['reference_margin_neglog2'], c['peak_gap_neglog2']
                d, z, eta, beta = dyadic(k), dyadic(Z), dyadic(B+2), dyadic(B)
                inequalities = [
                    (q-1)**2 < 2*(m+1) <= q*q,
                    eta <= d/(12*R), eta <= z, eta <= beta/4,
                    6*R*eta <= d/2,
                    dyadic(9*R*R)*d/8-eta >= z,
                    z <= d/16,
                    dyadic(2*R*R)*z <= d/2,
                    dyadic(11)*z**5*dyadic(2*R*R+2*(2*R+q)**2) == beta,
                    beta-2*eta == dyadic(B+1),
                    eta*eta == dyadic(c['directional_variance_ceiling_neglog2']),
                ]
                need(all(inequalities), 'an expanded sufficient budget failed')
                budgets += len(inequalities)
                schedules.append(c)
    log_controls = 0
    for a in range(1, 48):
        for b in range(1, 48):
            z = F(a, b)
            lo, hi = floor_log2(z), ceil_log2(z)
            need(dyadic(-lo) <= z < dyadic(-lo-1), 'floor logarithm')
            need(dyadic(-hi+1) < z <= dyadic(-hi), 'ceiling logarithm')
            log_controls += 1
    c = schedule(1, 6, 1)
    h = dyadic(c['projection_error_neglog2']+1)
    xs, ys, ps, x0, y0 = fixture(h)
    result = finite_guard(c, xs, ys, ps, (0, 0, 1))
    need(result['status'] == 'SIGNED_ABOVE_THRESHOLD', 'new sufficient branch')
    D, D0 = pair_loss(xs, ys, ps), pair_loss(x0, y0, ps)
    lam = 6*h*h/49
    need(F(result['normalized_mean_loss']) == D, 'direct pair loss')
    need(F(result['normalized_directional_variance']) == lam, 'centered directional variance')
    need(abs(D-D0) <= 6*h and D0 >= F(1, 4), 'projected loss budget')
    allx, ally = xs+x0, ys+y0
    extension_pairs = 0
    for i, j in combinations(range(len(allx)), 2):
        need(n2(sub(ally[i], ally[j])) <= n2(sub(allx[i], allx[j])), 'explicit joint extension data expand')
        extension_pairs += 1
    rows = [sub(xs[i]+ys[i], xs[0]+ys[0]) for i in range(1, 7)]
    det = determinant(rows)
    need(det != 0, 'control must have paired affine rank six')
    uncentered = [sub(x, (F(3), F(-5), F(8))) for x in xs]
    shifted_y = [sub(y, (F(-7), F(4), F(2))) for y in ys]
    need(finite_guard(c, uncentered, shifted_y, ps, (0, 0, 7)) == result, 'independent translations and direction rescaling')
    need(finite_guard(c, [tuple(2*z for z in x) for x in xs],
                      [tuple(2*z for z in y) for y in ys], ps, (0, 0, 1), 4) == result,
         'Gaussian variance normalization')
    perm = lambda x: (x[2], -x[0], x[1])
    need(finite_guard(c, list(map(perm, xs)), list(map(perm, ys)), ps, (1, 0, 0)) == result,
         'rigid coordinate change')
    need(finite_guard(c, xs+[(999, 999, 999)], ys+[(-999, 999, 999)],
                      ps+[F(0)], (0, 0, 1)) == result, 'zero-weight label')
    planar = finite_guard(c, x0, y0, ps, (0, 0, 1))
    iso = finite_guard(c, xs, xs, ps, (0, 0, 1))
    outside_cov = finite_guard(c, *fixture(F(1, 16))[:3], (0, 0, 1))
    low_loss = finite_guard(c, xs, [tuple((1-F(1, 1024))*z for z in x) for x in xs], ps, (0, 0, 1))
    need(planar['status'] == 'PLANAR_FULL_MAJORISATION', 'credited planar branch')
    need(iso['status'] == 'ISOMETRIC_ZERO', 'rigid branch')
    need(outside_cov['status'] == low_loss['status'] == 'UNRESOLVED', 'failed sufficient guards')

    # The target branch is tested beyond the R2 radius and threshold range.
    ct = schedule(3, 19, 0)
    ht = dyadic(ct['projection_error_neglog2']+1)
    raw_x, _, pt, _, raw_y = fixture(F(1, 16))
    xt = [tuple(3*z for z in x) for x in raw_x]
    yt = [(3*y[0], 3*y[1], ht if i == 3 else F(0))
          for i, y in enumerate(raw_y)]
    yt0 = [(x, y, F(0)) for x, y, z in yt]
    target = finite_guard(ct, xt, yt, pt, (0, 0, 1), side='target')
    target_D = pair_loss(xt, yt, pt)
    target_lam = 6*ht*ht/49
    need(target['status'] == 'SIGNED_ABOVE_THRESHOLD', 'target sufficient branch')
    need(F(target['normalized_mean_loss']) == target_D, 'target direct pair loss')
    need(F(target['normalized_directional_variance']) == target_lam, 'target centered variance')
    need(pair_loss(xt, yt0, pt) == target_D+2*target_lam, 'target projected loss identity')
    need(finite_guard(ct, xt, yt, pt, (0, 0, 1))['status'] == 'UNRESOLVED', 'the supplied source direction is not thin')
    target_det = determinant([sub(xt[i]+yt[i], xt[0]+yt[0]) for i in range(1, 7)])
    need(target_det != 0, 'target control must have paired affine rank six')
    target_pair_controls = 0
    for i, j in combinations(range(len(pt)), 2):
        need(n2(sub(yt[i], yt[j])) <= n2(sub(xt[i], xt[j])), 'target data expand')
        need(n2(sub(yt0[i], yt0[j])) <= n2(sub(yt[i], yt[j])), 'target projection expands')
        target_pair_controls += 1
    need(finite_guard(ct, [sub(x, (4, -1, 7)) for x in xt],
                      [sub(y, (3, 2, -5)) for y in yt], pt, (0, 0, 11), side='target') == target,
         'target translations and direction rescaling')
    need(finite_guard(ct, [tuple(2*z for z in x) for x in xt],
                      [tuple(2*z for z in y) for y in yt], pt, (0, 0, 1), 4, 'target') == target,
         'target variance normalization')
    need(finite_guard(ct, list(map(perm, xt)), list(map(perm, yt)), pt, (1, 0, 0), side='target') == target,
         'target coordinate change')
    target_planar = finite_guard(ct, xt, yt0, pt, (0, 0, 1), side='target')
    need(target_planar['status'] == 'PLANAR_FULL_MAJORISATION', 'credited planar target')

    eta = dyadic(c['projection_error_neglog2'])
    boundary_x = [(a, F(0), z) for a in [-F(1, 2), F(1, 2)] for z in [-eta, eta]]
    boundary_y = [(F(0), F(0), z) for a, b, z in boundary_x]
    boundary = finite_guard(c, boundary_x, boundary_y, [F(1, 4)]*4, (0, 0, 1))
    need(boundary['status'] == 'SIGNED_ABOVE_THRESHOLD' and
         F(boundary['normalized_mean_loss']) == F(1, 2) and
         F(boundary['normalized_directional_variance']) == dyadic(c['directional_variance_ceiling_neglog2']),
         'equality at both sufficient cutoffs is included')
    rejected = 0
    bad = copy.deepcopy(c)
    bad['hinge_margin_neglog2'] -= 1
    cases = [
        lambda: finite_guard(bad, xs, ys, ps, (0, 0, 1)),
        lambda: finite_guard(c, xs, ys, ps, (0, 0, 0)),
        lambda: finite_guard(c, xs, ys, ps, (0, 0, 1), 0),
        lambda: finite_guard(c, xs, ys, [F(1, 8)]*7, (0, 0, 1)),
        lambda: finite_guard(c, xs, ys, ps, (0, 0, 1.0)),
        lambda: finite_guard(c, xs, [tuple(10*z for z in x) for x in xs], ps, (0, 0, 1)),
        lambda: finite_guard(c, [tuple(10*z for z in x) for x in xs], ys, ps, (0, 0, 1)),
        lambda: finite_guard(c, xs, ys[:-1], ps, (0, 0, 1)),
        lambda: finite_guard(c, xs, ys, ps, (0, 0, 1), side='either'),
        lambda: schedule(0, 6, 1), lambda: schedule(1, 0, 1),
        lambda: schedule(1, 6, -1), lambda: schedule(True, 6, 1),
    ]
    for fn in cases:
        try:
            fn()
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError('damaged input accepted')
    huge = schedule(10**12, 10**9, 80)
    need(len(str(huge['directional_variance_ceiling_neglog2'])) < 30, 'compact exponent encoding')
    return {
        'status': 'COVARIANCE_BOUNDARY_EXACT_CONTROLS_PASS',
        'parameter_schedules': len(schedules), 'expanded_rational_budgets': budgets,
        'logarithm_controls': log_controls, 'joint_extension_pair_controls': extension_pairs,
        'fixture_paired_affine_rank': 6, 'fixture_determinant_over_h': str(det/h),
        'fixture_variance_over_h_squared': '6/49',
        'finite_guard': compact_guard(result),
        'target_guard': compact_guard(target),
        'target_schedule': ct, 'target_pair_controls': target_pair_controls,
        'target_fixture_paired_affine_rank': 6,
        'target_fixture_determinant_over_h': str(target_det/ht),
        'cutoff_equality_guard': compact_guard(boundary),
        'known_branches': [planar['status'], iso['status'], target_planar['status']],
        'unresolved_controls': [outside_cov['status'], low_loss['status']],
        'damaged_inputs_rejected': rejected,
        'headline_schedule': c, 'huge_radius_schedule': huge,
        'scope': 'Exact budgets, projected loss, labelled contractions and branch controls. Gaussian translation, peak comparison and the R5 hinge theorem are written mathematics, not independently verified here.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--record', action='store_true')
    args = parser.parse_args()
    record = controls()
    data = (json.dumps(record, indent=2, sort_keys=True)+'\n').encode()
    expected = Path(__file__).with_name('EXPECTED.json')
    if args.record:
        expected.write_bytes(data)
    else:
        need(expected.read_bytes() == data, 'expected record differs')
    print(record['status'])
    print('record_sha256='+hashlib.sha256(data).hexdigest())


if __name__ == '__main__':
    main()
