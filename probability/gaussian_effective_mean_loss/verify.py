#!/usr/bin/env python3
"""Exact controls for PROOF.md; the analytic proof is not formalized."""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib
import json
import sys

from certificate import (need, constants, rational_schedule, dyadic_exponent,
                         audit_cutoff, finite_guard, dot, sub, norm2,
                         center, cross, psd, pair_losses)

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    return x


def digest(x):
    return hashlib.sha256(json.dumps(encode(x), sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def rejected(fn):
    try:
        fn()
    except ValueError:
        return 1
    raise ValueError('bad input was accepted')


def family(tau, alpha, core, outer):
    v = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    xs = [tuple(F(a, 80) for a in v0) for v0 in v]
    xs += [tuple(-F(a, 4) for a in v0) for v0 in v]
    ys = [tuple((1-tau)*F(a, 80) for a in v0) for v0 in v]
    ys += [tuple((1-tau)*F(29*a, 120) for a in v0) for v0 in v]
    p = [(1-alpha)*a for a in core]+[alpha*a for a in outer]
    return xs, ys, p


def run():
    pins = json.loads((ROOT/'INPUTS.json').read_text())
    for pin in pins['files']:
        need(hashlib.sha256((REPO/pin['path']).read_bytes()).hexdigest() == pin['sha256'],
             'changed dependency '+pin['path'])
    c = constants(F(1, 2), F(1, 2**15), F(1, 64), F(1, 2**13))
    need(3**8 < 2**13, 'w bound from e<3')
    need(F(1)+F(3, 4)+F(3, 4)**2/2 > 2, 'log 2 <3/4')
    need((F(44, 7))**3 < 256, 'C>1/16 from pi<22/7')
    need(c['delta'] == F(1, 2**54) and c['c0'] == F(1, 2**34), 'dyadic coefficients')
    exponents = {k: dyadic_exponent(v) for k, v in c['bounds'].items()}
    need(list(exponents.values()) == [44, 123, 138, 208, 67, 319, 356], 'seven cutoff budgets')
    for d in [F(1, 2**360), F(1, 2**400), F(1, 7*2**360)]:
        audit_cutoff(c, d)
    schedule_rows = []
    for R, ratio, m in product([F(1, 4), F(1, 2), F(1), F(2), F(3)],
                                [16, 128], [1, 6, 12]):
        s = rational_schedule(R, R*R/ratio, m)
        need(2*s['J']**2 >= 3*m, 'containing ball')
        need(s['exponential_ceiling'] >= (s['B']+R)**2/2, 'posterior weight ceiling')
        d = F(1, 2**s['cutoff_exponent'])
        audit_cutoff(s, d)
        schedule_rows.append({'R': R, 'kappa': R*R/ratio, 'm': m,
                              'cutoff_exponent': s['cutoff_exponent']})

    # The Gaussian comparison is analytic. These exact controls specifically
    # exercise its two branches |b-l/2| and its factor of two.
    slice_count = 0
    for b, r, l in product([F(1, 10), F(1, 2), F(1), F(3)], repeat=3):
        lo, hi = abs(b-l/2), b+l/2
        need(hi >= lo >= 0, 'slice integration orientation')
        need(r*(hi*hi-lo*lo) == 2*r*b*l, 'interval primitive factor')
        slice_count += 1

    core_priors = [[F(1, 4)]*4, [F(1, 2)]+[F(1, 6)]*3,
                   [F(1, 8)]*3+[F(5, 8)]]
    outer_priors = [[F(1, 4)]*4, [F(1), F(0), F(0), F(0)],
                    [F(1, 2), F(1, 4), F(1, 8), F(1, 8)]]
    xs0, ys0, p0 = family(F(0), F(1, 8), core_priors[0], outer_priors[0])
    table = {}
    for i, j in combinations(range(8), 2):
        a, b = norm2(sub(xs0[i], xs0[j])), norm2(sub(ys0[i], ys0[j]))
        need(a >= b, 'template contraction')
        typ = 'core' if j < 4 else ('outer' if i >= 4 else ('same' if i == j-4 else 'different'))
        table.setdefault(typ, set()).add((a*6400, b*6400))
    need(table == {'core': {(F(8), F(8))}, 'outer': {(F(3200), F(26912, 9))},
                   'same': {(F(1323), F(3025, 3))}, 'different': {(F(1163), F(1163))}},
         'complete template table')
    need(F(363, 1600) < F(1, 4) and F(1, 25600) > F(1, 2**15), 'uniform radius/covariance')
    need((F(1, 400)+2)*F(1, 2**362) < F(1, 2**360), 'independent-parameter loss cap')
    family_rows, ratio_checks = [], 0
    for tau, alpha, core, outer in product([F(0), F(1, 2**362), F(1, 2**400)],
                                          [F(0), F(1, 2**362), F(1, 2**400)],
                                          core_priors, outer_priors):
        xs, ys, p = family(tau, alpha, core, outer)
        d, Q, losses = pair_losses(xs, ys, p)
        result = finite_guard(xs, ys, p)
        need(result['status'] == ('ZERO_LOSS' if not d else 'SIGNED_MIDDLE'), 'whole-family guard')
        need(d <= tau/400+2*alpha, 'family loss inequality')
        if tau == 0 and alpha > 0:
            need({z for row in losses for z in row if z} == {F(59, 1200), F(59, 1800)}, 'rare-only loss levels')
            need(Q/d >= F(59, 1800) > F(1, 2**48), 'old quartic guard excluded')
            ratio_checks += 1
        family_rows.append([tau, alpha, core, outer, d, Q, result['status']])

    # Genuine approximate-half-space controls: the moved point has a negative
    # half-space contribution from its own small mass, rather than eta=0.
    raw_x = [(-1, 0, 0), (-2, 1, 0), (-2, 0, 1), (-2, -1, -1), (1, 0, 0)]
    raw_y = raw_x[:-1]+[(-1, 0, 0)]
    fold_rows, posterior_checks, pair_identities = [], 0, 0
    for ealpha in [370, 400, 512]:
        alpha = F(1, 2**ealpha)
        p = [(1-alpha)/4]*4+[alpha]
        xs = center([tuple(F(z, 6) for z in x) for x in raw_x], p)
        ys = center([tuple(F(z, 6) for z in x) for x in raw_y], p)
        d, Q, losses = pair_losses(xs, ys, p)
        need(finite_guard(xs, ys, p)['status'] == 'SIGNED_MIDDLE', 'rare-fold guard')
        need(Q/d == F(13, 63), 'credited rare-fold Q/d')
        need(psd(cross(xs, ys, p)), 'identity is a Procrustes alignment')
        hs = [sub(y, x) for x, y in zip(xs, ys)]
        M = sum((pi*norm2(h) for pi, h in zip(p, hs)), F(0))
        x, y = xs[-1], ys[-1]
        direction = (F(-1), F(0), F(0))
        l = dot(sub(y, x), direction)
        mid = tuple((a+b)/2 for a, b in zip(x, y))
        zeta = [dot(sub(z, mid), direction) for z in xs]
        m0 = sum((pi*z for pi, z in zip(p, zeta)), F(0))
        eta = sum((pi*max(-z, F(0)) for pi, z in zip(p, zeta)), F(0))
        q = norm2(x)-norm2(y)
        need(eta > 0 and q == 2*l*m0, 'nontrivial approximate half-space')
        need((eta*l)**2 <= 9*c['R']**2*M, 'half-space violation bound')
        need(m0 >= c['kappa']/c['R']-2*eta, 'covariance coercivity')
        need(eta <= c['w']**2*m0/2, 'posterior guard')
        need(M <= c['w']**4*c['kappa']**2*c['delta']**2/(144*c['R']**4), 'rare uniform smallness')
        for i in range(5):
            need(sum((p[j]*losses[i][j] for j in range(5)), F(0))
                 == norm2(xs[i])-norm2(ys[i])+d/2, 'conditional loss identity')
            pair_identities += 1
        for tilt in [F(-1, 8), F(0), F(1, 8)]:
            a = list(map(F, [-2, -1, 0, 1, 2]))
            av = sum((pi*z for pi, z in zip(p, a)), F(0))
            posterior = [1+tilt*(z-av) for z in a]
            need(sum((pi*r for pi, r in zip(p, posterior)), F(0)) == 1, 'posterior normalization')
            need(all(c['w'] <= r <= 1/c['w'] for r in posterior), 'posterior envelope')
            zmean = sum((pi*r*z for pi, r, z in zip(p, posterior, zeta)), F(0))
            need(zmean >= c['w']*m0-eta/c['w'] >= c['w']*m0/2, 'posterior lower bound')
            posterior_checks += 1
        fold_rows.append({'alpha_exponent': ealpha, 'd': d, 'Q/d': Q/d,
                           'M': M, 'eta': eta, 'q': q})

    # Separate translations, an orthogonal coordinate permutation, and variance
    # rescaling leave dimensionless mean loss and the sufficient result intact.
    xs, ys, p = family(F(0), F(1, 2**362), core_priors[1], outer_priors[2])
    expected = finite_guard(xs, ys, p)
    for scale in [1, 2, 3]:
        xx = [tuple(scale*x[(j+1)%3]+[2, -3, 1][j] for j in range(3)) for x in xs]
        yy = [tuple(scale*y[(j+1)%3]+[-1, 4, 2][j] for j in range(3)) for y in ys]
        need(finite_guard(xx, yy, p, F(scale*scale)) == expected, 'similarity normalization')

    bad = rejected(lambda: audit_cutoff(c, F(1, 2**355)))
    bad += rejected(lambda: constants(0, F(1, 2**15), F(1, 64), F(1, 8192)))
    bad += rejected(lambda: rational_schedule(F(1, 2), F(1, 2**15), 0))
    bad += rejected(lambda: finite_guard(xs, ys, [F(-1)]+p[1:]))
    bad += rejected(lambda: finite_guard(xs[:-1], ys, p))
    bad += rejected(lambda: finite_guard(xs, ys, p, F(0)))
    bad += rejected(lambda: finite_guard(xs, ys, p, 1.0))
    expanded = [tuple(2*z for z in x) for x in xs]
    bad += rejected(lambda: finite_guard(xs, expanded, p))
    outside = family(F(1, 100), F(0), core_priors[0], outer_priors[0])
    need(finite_guard(*outside)['status'] == 'UNRESOLVED', 'large mean loss unresolved')
    flat_x = [(F(-1, 8), F(0), F(0)), (F(1, 8), F(0), F(0))]
    flat_y = [tuple((1-F(1, 2**400))*z for z in x) for x in flat_x]
    need(finite_guard(flat_x, flat_y, [F(1, 2)]*2)['reason'] == 'covariance', 'covariance collapse unresolved')
    need(finite_guard(flat_x, flat_x, [F(1, 2)]*2)['status'] == 'ZERO_LOSS', 'singular exact equality')

    return {'status': 'EFFECTIVE_MEAN_LOSS_PASS',
            'scope': 'Exact guard/schedule/algebra controls; analytic component comparison is written mathematics, pending independent review.',
            'dependency_pins': len(pins['files']),
            'dyadic': {'cutoff_exponent': 360, 'delta_exponent': 54, 'c0_exponent': 34,
                       'seven_budget_exponents': exponents, 'margin_exponent': 40},
            'all_radius_schedules': schedule_rows,
            'slice_primitive_controls': slice_count,
            'template_pair_checks': 28,
            'family_controls': len(family_rows), 'family_controls_sha256': digest(family_rows),
            'nonvanishing_Q_over_d_controls': ratio_checks,
            'rare_fold_controls': fold_rows,
            'posterior_checks': posterior_checks, 'conditional_loss_identities': pair_identities,
            'variance_scalings': 3, 'malformed_or_failed_schedule_rejections': bad,
            'unresolved_controls': 2, 'singular_zero_loss_control': 1,
            'degree_two_guard_pair_bound': 19}


def main():
    record = (json.dumps(encode(run()), sort_keys=True, indent=2)+'\n').encode()
    expected = ROOT/'EXPECTED.json'
    if sys.argv[1:] == ['--write-expected']:
        need(not expected.exists(), 'refusing to replace expected record')
        expected.write_bytes(record)
    else:
        need(not sys.argv[1:], 'usage: verify.py [--write-expected]')
        need(expected.read_bytes() == record, 'expected record mismatch')
    print('EFFECTIVE_MEAN_LOSS_PASS')
    print('record_sha256='+hashlib.sha256(record).hexdigest())


if __name__ == '__main__':
    main()
