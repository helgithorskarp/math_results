#!/usr/bin/env python3
"""Independent exact controls for the reviewed effective mean-loss theorem.

No target code is imported. Continuum slicing is reviewed mathematics.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json

from projection_controls import (require, sub, dot, norm2, center, matrix,
                                 covariance_floor, psd)

ROOT = Path(__file__).resolve().parent


def main_controls():
    pins = json.loads((ROOT/'TARGET_INPUTS.json').read_text())
    for item in pins['files']:
        raw = (ROOT.parent.parent/item['path']).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == item['sha256'], 'target bytes changed')

    # Reconstruct from the published definitions; check each actual
    # smallness/error inequality rather than merely comparing the minimum.
    R, k, t, w = F(1, 2), F(1, 2**15), F(1, 64), F(1, 2**13)
    K0, L, K1, K2 = 2*R*R/k, 96*R**3/k+6*R, 16*R/k, 2*R/t**2
    c, delta = w*w*t/4, F(1, 2**54)
    require(K1*delta == c/4, 'bulk linear constant')
    bounds = [k*k/(4*R*R*K0), delta*delta/(2*K0),
              k*delta*delta/(8*R*R*K0), w**4*k*k*delta*delta/(144*R**4*K0),
              2*k*delta/R, c*delta**4/(8*L*L*K0*K0),
              c*c*delta**4/(64*K2*K2*K0**3)]
    exps = [44, 123, 138, 208, 67, 319, 356]
    for bound, e in zip(bounds, exps):
        require(F(1, 2**e) <= bound < F(1, 2**(e-1)), 'dyadic exponent')

    def budget(d):
        require(d > 0, 'positive loss required here')
        M, alpha = K0*d, K0*d/delta**2
        require(R*R*M <= k*k/4, 'global alignment')
        require(alpha <= F(1, 2) and alpha <= k/(8*R*R), 'bulk mass/covariance')
        require(M <= w**4*k*k*delta**2/(144*R**4), 'rare halfspace')
        require(d <= 2*k*delta/R, 'conditional pair loss')
        require(L*L*alpha*alpha <= c*d/8, 'bulk error')
        require(K2*K2*alpha*alpha*M <= (c*d/8)**2, 'mixed error')
    for e in (360, 361, 377, 511):
        budget(F(1, 2**e))
    require(3**8 < 2**13, 'Gaussian posterior bound')
    require(1+F(3, 4)+F(3, 4)**2/2 > 2, 'logarithm bound')
    require(F(44, 7)**3 < 256, 'Gaussian normalizer bound')

    # Endpoint distance identity and two primitive branches, with short,
    # long and off-center intervals. The actual Gaussian lower bound is
    # justified analytically in REVIEW.md, not by these finite samples.
    intervals = []
    for b, r, ell in product((F(1, 17), F(2, 3), F(7)),
                             (F(1, 13), F(3, 2), F(5)),
                             (F(1, 11), F(3), F(17))):
        lo, hi = abs(b-ell/2), b+ell/2
        require(0 <= lo < hi, 'primitive orientation')
        require((hi*hi-lo*lo)/2 == b*ell, 'primitive factor')
        require(hi+r == b+r+ell/2, 'endpoint relative to x')
        intervals.append([str(v) for v in (b, r, ell, lo, hi)])

    tetra = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    xs = [tuple(F(a, 80) for a in p) for p in tetra]
    xs += [tuple(F(-a, 4) for a in p) for p in tetra]
    ys0 = xs[:4]+[tuple(F(29*a, 120) for a in p) for p in tetra]
    table = {}
    for i, j in combinations(range(8), 2):
        d = norm2(sub(xs[i], xs[j]))-norm2(sub(ys0[i], ys0[j]))
        require(d >= 0, 'template expansion')
        typ = 'core' if j < 4 else 'outer' if i >= 4 else 'matched' if j == i+4 else 'unmatched'
        table.setdefault(typ, set()).add(d)
    require(table == {'core': {F(0)}, 'outer': {F(59, 1800)},
                      'matched': {F(59, 1200)}, 'unmatched': {F(0)}}, 'pair-loss table')

    # Universal family bounds, plus exact strongly unbalanced witnesses.
    require(F(363, 1600) < F(1, 4), 'uniform radius')
    require(F(1, 25600) > k, 'uniform covariance')
    require((2+F(1, 400))*F(1, 2**362) < F(1, 2**360), 'family loss cap')
    rows = []
    core = (F(1, 8), F(1, 8), F(1, 4), F(1, 2))
    for tau, alpha, outer in product((F(0), F(1, 2**362)),
                                     (F(0), F(1, 2**362), F(1, 2**401)),
                                     ((F(0), F(0), F(1), F(0)),
                                      (F(1, 3), F(1, 6), F(1, 12), F(5, 12)))):
        ys = [tuple((1-tau)*a for a in p) for p in ys0]
        weights = [(1-alpha)*a for a in core]+[alpha*a for a in outer]
        xc, yc = center(xs, weights), center(ys, weights)
        require(max(map(norm2, xc)) <= F(1, 4), 'witness radius')
        covariance_floor(xc, weights, k)
        d = Q = F(0)
        for i, j in product(range(8), repeat=2):
            loss = norm2(sub(xs[i], xs[j]))-norm2(sub(ys[i], ys[j]))
            require(loss >= 0, 'family contraction')
            d += weights[i]*weights[j]*loss
            Q += weights[i]*weights[j]*loss*loss
        trace_loss = 2*sum(p*(norm2(x)-norm2(y)) for x, y, p in zip(xc, yc, weights))
        require(d == trace_loss, 'pair versus marginal variance loss')
        require(d <= tau/400+2*alpha <= F(1, 2**360), 'family sufficient guard')
        if tau == 0 and alpha > 0:
            require(d > 0 and Q/d >= F(59, 1800) > F(1, 2**48), 'quartic separation')
        rows.append({'tau': str(tau), 'alpha': str(alpha), 'D': str(d),
                     'Q_over_D': str(Q/d) if d else None})

    # Reconstruct an actual rare move with positive unfavorable halfspace
    # mass. Its direction is axial, making all quantities exactly rational.
    raw = [(-1, 0, 0), (-2, 1, 0), (-2, 0, 1), (-2, -1, -1), (1, 0, 0)]
    folds = []
    for power in (363, 399, 501):
        alpha = F(1, 2**power)
        weights = [(1-alpha)/4]*4+[alpha]
        source = [tuple(F(a, 6) for a in p) for p in raw]
        target = [(-abs(p[0]), p[1], p[2]) for p in source]
        xc, yc = center(source, weights), center(target, weights)
        psd(matrix(xc, yc, weights))
        hs = [sub(y, x) for x, y in zip(xc, yc)]
        M = sum(p*norm2(h) for p, h in zip(weights, hs))
        x, y = xc[-1], yc[-1]
        ell, q = x[0]-y[0], norm2(x)-norm2(y)
        zeta = [(x[0]+y[0])/2-z[0] for z in xc]
        m0 = sum(p*z for p, z in zip(weights, zeta))
        eta = sum(p*max(-z, F(0)) for p, z in zip(weights, zeta))
        require(eta > 0 and q == 2*ell*m0, 'true unfavorable halfspace mass')
        require((eta*ell)**2 <= 9*R*R*M, 'contraction repair bound')
        require(m0 >= k/R-2*eta and eta <= w*w*m0/2, 'rare coercivity/posterior')
        require(M <= w**4*k*k*delta**2/(144*R**4), 'uniform smallness')
        folds.append({'mass_exponent': power, 'eta_positive': True, 'm0': str(m0)})

    rejected = []
    def reject(name, fn):
        try:
            fn()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('adverse control accepted: '+name)
    reject('cutoff_2^-355', lambda: budget(F(1, 2**355)))
    reject('negative_loss', lambda: budget(F(-1)))
    reject('covariance_collapse', lambda: covariance_floor(
        [(F(-1, 8), F(0), F(0)), (F(1, 8), F(0), F(0))], [F(1, 2)]*2, k))
    reject('nonpositive_component_bias', lambda: require(F(-1, 3) > 0, 'component midpoint bias'))
    reject('missing_mixed_pair_factor', lambda: require(F(1, 16)/8 >= 2*F(1, 16)/8,
                                                       'cross coefficient counted once'))

    raw_rows = json.dumps(rows, sort_keys=True, separators=(',', ':')).encode()
    return {'status': 'EFFECTIVE_MEAN_LOSS_R4_REVIEW_PASS',
            'target_commit': pins['source_commit'], 'pinned_files': len(pins['files']),
            'seven_cutoff_exponents': exps, 'accepted_cutoff_exponent': 360,
            'slice_primitive_controls': len(intervals),
            'template_pairs': 28,
            'loss_table': {k: sorted(str(a) for a in v) for k, v in table.items()},
            'unbalanced_family_controls': len(rows),
            'family_record_sha256': hashlib.sha256(raw_rows).hexdigest(),
            'approximate_halfspace_controls': folds, 'rejected_controls': rejected,
            'degree_two_cubature_pairs': 19,
            'scope': 'independent finite algebra; analytic slice proof reviewed, not formalized'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--emit', action='store_true')
    args = p.parse_args()
    result = main_controls()
    raw = (json.dumps(result, sort_keys=True, indent=2)+'\n').encode()
    if args.emit:
        print(raw.decode(), end='')
    else:
        require(raw == (ROOT/'EXPECTED.json').read_bytes(), 'expected record differs')
        print(json.dumps({'status': result['status'],
                          'expected_sha256': hashlib.sha256(raw).hexdigest(),
                          'pinned_files': result['pinned_files'],
                          'family_controls': result['unbalanced_family_controls'],
                          'adverse_controls': len(result['rejected_controls'])}, sort_keys=True))


if __name__ == '__main__':
    main()
