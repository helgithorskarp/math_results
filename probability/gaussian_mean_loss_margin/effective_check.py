#!/usr/bin/env python3
"""Author exact controls; expanded budgets use a different representation.

These checks do not replace the analytic proof or independent review.
"""
import copy
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import sys

import effective as impl

ROOT = Path(__file__).resolve().parent


def need(test, message):
    if not test:
        raise ValueError(message)


def p2(k):
    return F(1 << k) if k >= 0 else F(1, 1 << -k)


def ceilq(x):
    return (x.numerator+x.denominator-1)//x.denominator


def independent_expanded(record):
    """Check sufficient rational inequalities, not regenerated exponent equality."""
    R, k, r = map(F, (record['radius'], record['covariance_floor'], record['volume_radius']))
    q = record['budgets']
    c0, b = p2(-q['c0_neglog2']), p2(-q['one_point_neglog2'])
    K0, K1, K2 = (p2(q[s]) for s in ('K0_log2', 'K1_log2', 'K2_log2'))
    L = p2(q['L_log2'])
    alpha, c = p2(-q['rare_mass_neglog2']), p2(-q['core_margin_neglog2'])
    d1, d2 = p2(-q['anchor_scale_neglog2']), p2(-q['bulk_scale_neglog2'])
    D = p2(-record['loss_cutoff_neglog2'])
    checks = [
        c0 <= F(1, 64)*p2(-2*ceilq((r+R)**2/2+(r+3*R)**2)),
        b <= F(1, 128)*p2(-2*ceilq((r+R)**2/2+(r+4*R)**2+2*R**2)),
        K0 >= 2*R*R/k, K1 >= 16*R/k,
        K2 >= 2*R*p2(2*ceilq((r+R)**2)), L >= 96*R**3/k+6*R,
        alpha <= F(1, 2), alpha <= k/(8*R*R),
        alpha <= k/(16*R)*p2(-2*ceilq((r+6*R)**2/2)),
        alpha <= k/(48*R*R)*p2(-2*ceilq((r+4*R)**2+(r+R)**2)),
        c <= min(c0, b/8), d2 <= min(1, R, c/(4*K1)),
        d1 <= min(d2/2, d2*d2/(12*R), k*d2*d2/(576*R**3), b*k*d2*d2/(48*R*R)),
        D <= k**3/(8*R**4), D <= alpha*d1*d1/K0,
        D <= k*d2/(16*R*(F(1, 2)+12*R*R*K0/(d1*d1))),
        D <= c*d2**4/(8*L*L*K0*K0),
        D <= c*c*d2**4/(64*K2*K2*K0**3),
        p2(-record['margin_neglog2']) <= c/2,
        K1*d2 <= c/4,
        L*L*(K0*D/(d2*d2))**2 <= c*D/8,
        K2*K2*(K0*D/(d2*d2))**2*K0*D <= (c*D/8)**2,
        36*R*R*d1/d2 <= k*d2/(16*R),
        6*R*d1/d2 <= b*k*d2/(8*R),
    ]
    need(all(checks), 'expanded rational sufficient inequality failed')
    return len(checks)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def square(a):
    return dot(a, a)


def rejected(fn):
    try:
        fn()
    except ValueError:
        return 1
    raise ValueError('damaged input accepted')


def record_input(result):
    d = F(result['normalized_loss'])
    return {k: result[k] for k in ('status', 'loss_ceil_log2', 'loss_cutoff_neglog2',
                                  'margin_neglog2', 'volume_radius', 'threshold_left_neglog2')} | {
        'loss_numerator_bits': d.numerator.bit_length(),
        'loss_denominator_bits': d.denominator.bit_length(),
        'loss_sha256': hashlib.sha256(str(d).encode()).hexdigest()}


def run():
    logarithm_checks = 0
    for n, d in itertools.product(range(1, 65), repeat=2):
        x = F(n, d)
        power, exponent = F(1), 0
        while power > x:
            power /= 2
            exponent -= 1
        while 2*power <= x:
            power *= 2
            exponent += 1
        need(impl.floor_log2(x) == exponent, 'independent floor logarithm')
        need(impl.ceil_log2(x) == exponent+(power != x), 'independent ceiling logarithm')
        logarithm_checks += 1
    for k in [-2048, -61, 0, 61, 2048]:
        need(impl.floor_log2(p2(k)) == impl.ceil_log2(p2(k)) == k, 'power-of-two endpoint')
        logarithm_checks += 1

    count, inequalities = 0, 0
    for R, divisor, vfactor in itertools.product([F(1, 4), F(1, 2), F(1), F(2), F(4)],
                                                [4, 8, 32], [F(1, 2), F(1), F(3)]):
        row = impl.schedule(R, R*R/divisor, vfactor*R)
        impl.verify_schedule(row)
        inequalities += independent_expanded(row)
        count += 1
    headline = [impl.schedule(1, '1/32', 1),
                impl.threshold_schedule('1/2', '1/384', 6),
                impl.schedule(3, '3/32', 1)]
    need([(s['loss_cutoff_neglog2'], s['margin_neglog2']) for s in headline]
         == [(567, 69), (967, 123), (2900, 401)], 'headline table')
    for s in headline:
        inequalities += independent_expanded(s)
    huge = impl.schedule(10**12, F(1, 2**80), 10**12+16)
    impl.verify_schedule(huge)
    need(huge['loss_cutoff_neglog2'] == 406000000002752000000006849, 'compressed huge-radius schedule')
    # No 2**huge['loss_cutoff_neglog2'] is evaluated anywhere.

    base = [(-1, 0, 0), (-2, 1, 0), (-2, 0, 1), (-2, -1, -1)]
    fixtures = []
    for scale, sched in [(F(1, 6), headline[1]), (F(1), headline[2])]:
        alpha_bits = sched['loss_cutoff_neglog2']+5
        alpha = p2(-alpha_bits)
        xs = [tuple(scale*v for v in x) for x in base+[(1, 0, 0)]]
        ys = [tuple(scale*v for v in x) for x in base+[(-1, 0, 0)]]
        ws = [(1-alpha)/4]*4+[alpha]
        result = impl.check_input(sched, xs, ys, ws)
        D = F(result['normalized_loss'])
        need(result['status'] == 'SIGNED_BOUNDED_VOLUME', 'rare fold must pass the effective guard')
        need(D == 14*scale*scale*alpha*(1-alpha), 'independent rare loss formula')
        Q = sum((ws[i]*ws[j]*(square(sub(xs[i], xs[j]))-square(sub(ys[i], ys[j])))**2
                 for i in range(5) for j in range(5)), F(0))
        need(Q/D == scale*scale*F(52, 7), 'non-small second loss ratio remains')
        fixtures.append({'kind': 'known rare fold', 'alpha_bits': alpha_bits,
                         'scale': str(scale), 'second_to_first_loss': str(Q/D),
                         'guard': record_input(result)})
        moved_x = [tuple(2*x[j]+[7, -3, 11][j] for j in range(3)) for x in xs]
        moved_y = [tuple(2*y[j]+[-5, 2, 1][j] for j in range(3)) for y in ys]
        transformed = impl.check_input(sched, moved_x, moved_y, ws, variance=4)
        need(transformed == result, 'translation and variance scaling')

    tet = [(F(a, 2), F(b, 2), F(c, 2)) for a, b, c in
           [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]
    weights = [F(1, 4)]*4
    eps = p2(-headline[0]['loss_cutoff_neglog2']-5)
    contracted = [tuple((1-eps)*v for v in x) for x in tet]
    result = impl.check_input(headline[0], tet, contracted, weights)
    need(result['status'] == 'SIGNED_BOUNDED_VOLUME', 'near-isometry homothety passes')
    fixtures.append({'kind': 'known homothety', 'guard': record_input(result)})
    zero = impl.check_input(headline[0], tet, tet, weights)
    need(zero['status'] == 'ISOMETRIC_ZERO', 'isometry branch')
    unresolved = impl.check_input(headline[0], tet, [tuple(v/2 for v in x) for x in tet], weights)
    need(unresolved['status'] == 'UNRESOLVED', 'failed guard must not imply an adverse sign')

    # Direct exact geometry controls for the approximate-contraction repair.
    repair_count = 0
    x = (F(1), F(0), F(0))
    for p, q in itertools.product(range(-8, 9), repeat=2):
        y = (F(0), F(p, 2), F(q, 2))
        length2 = square(sub(x, y))
        eta = max(F(0), *(square(sub(y, a))-square(sub(x, a)) for a in base))
        if not (0 < eta < length2):
            continue
        t = eta/length2
        repaired = tuple((1-t)*b+t*a for a, b in zip(x, y))
        for a in base:
            lhs = square(sub(repaired, a))
            rhs = (1-t)*square(sub(y, a))+t*square(sub(x, a))-t*(1-t)*length2
            need(lhs == rhs and lhs <= square(sub(x, a)), 'exact repair for every background center')
        need(square(sub(repaired, y)) == eta*eta/length2, 'repair distance')
        repair_count += 1
    need(repair_count > 0, 'nontrivial repair controls needed')

    reflection_count = 0
    for t, b, w in itertools.product([F(1, 7), F(1, 2), F(2)],
                                     [F(-2), F(0), F(1, 3), F(3)],
                                     [F(0), F(2, 5)]):
        z, reflected, a = (-t, w, F(1, 3)), (t, w, F(1, 3)), (-b, F(1, 4), F(0))
        need(square(sub(reflected, a))-square(sub(z, a)) == 4*t*b,
             'reflection exponent difference')
        reflection_count += 1

    rejects = 0
    bad = copy.deepcopy(headline[0]);bad['loss_cutoff_neglog2'] -= 1
    rejects += rejected(lambda: impl.verify_schedule(bad))
    bad2 = copy.deepcopy(headline[0]);bad2['budgets']['K2_log2'] += 1
    rejects += rejected(lambda: impl.verify_schedule(bad2))
    rejects += rejected(lambda: impl.schedule(0, F(1, 32), 1))
    rejects += rejected(lambda: impl.schedule(1, 1, 1))
    rejects += rejected(lambda: impl.schedule(1.0, '1/32', 1))
    rejects += rejected(lambda: impl.threshold_schedule(1, '1/32', 0))
    rejects += rejected(lambda: impl.check_input(headline[0], tet, tet, [-1, 1, 1, 0]))
    rejects += rejected(lambda: impl.check_input(headline[0], tet, [tuple(2*v for v in x) for x in tet], weights))
    flat = [(F(-1), F(0), F(0)), (F(1), F(0), F(0))]
    rejects += rejected(lambda: impl.check_input(headline[0], flat, flat, [F(1, 2)]*2))
    rejects += rejected(lambda: impl.check_input(headline[0], tet, tet, weights, variance=0))
    return {'status': 'EFFECTIVE_MEAN_LOSS_CHECKS_PASS',
            'scope': 'Exact sufficient-budget and finite-input controls; universal reflection, posterior and Procrustes arguments remain the written author proof.',
            'independent_logarithm_controls': logarithm_checks,
            'expanded_parameter_schedules': count+len(headline),
            'expanded_rational_inequalities': inequalities,
            'headline_schedules': headline, 'compressed_large_schedule': huge,
            'finite_geometry_controls': fixtures,
            'isometric_status': zero['status'], 'outside_guard_status': unresolved['status'],
            'nontrivial_exact_repairs': repair_count, 'reflection_exponent_controls': reflection_count,
            'damaged_input_rejections': rejects}


def main():
    record = (json.dumps(run(), indent=2, sort_keys=True)+'\n').encode()
    expected = ROOT/'EFFECTIVE_EXPECTED.json'
    if sys.argv[1:] == ['--write-expected']:
        need(not expected.exists(), 'refusing to overwrite existing expected output')
        expected.write_bytes(record)
    else:
        need(not sys.argv[1:], 'usage: effective_check.py [--write-expected]')
        need(expected.read_bytes() == record, 'expected record differs')
    print('EFFECTIVE_MEAN_LOSS_CHECKS_PASS')
    print('record_sha256='+hashlib.sha256(record).hexdigest())


if __name__ == '__main__':
    main()
