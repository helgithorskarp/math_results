#!/usr/bin/env python3
"""Exact finite controls, not a formalization of the analytic sign proof."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def add(x, y):
    return tuple(a+b for a, b in zip(x, y))


def scale(a, x):
    return tuple(a*b for b in x)


def norm2(x):
    return dot(x, x)


def mean(points, weights):
    return tuple(sum((w*p[k] for w, p in zip(weights, points)), F(0))
                 for k in range(3))


def center(points, weights):
    b = mean(points, weights)
    return [sub(p, b) for p in points]


def matrix(points, others, weights):
    return [[sum((w*p[i]*q[j] for w, p, q in
                  zip(weights, points, others)), F(0))
             for j in range(3)] for i in range(3)]


def det(a):
    if len(a) == 1:
        return a[0][0]
    return sum(((-1)**j*a[0][j]*det([r[:j]+r[j+1:] for r in a[1:]])
                for j in range(len(a))), F(0))


def psd(a):
    require(all(a[i][j] == a[j][i] for i in range(3) for j in range(3)),
            'matrix not symmetric')
    for k in range(1, 4):
        for idx in combinations(range(3), k):
            require(det([[a[i][j] for j in idx] for i in idx]) >= 0,
                    'negative principal minor')


def covariance_floor(points, weights, floor):
    a = matrix(center(points, weights), center(points, weights), weights)
    for i in range(3):
        a[i][i] -= floor
    psd(a)


def project(z, h, q):
    """Project to q+2 z.h >= 0, without extracting |h|."""
    l2 = norm2(h)
    require(l2 > 0, 'zero projection normal')
    s = q+2*dot(z, h)
    return z if s >= 0 else sub(z, scale(s/(2*l2), h))


def reflect(z, h, q):
    return sub(z, scale((q+2*dot(z, h))/norm2(h), h))


def exponent_guard(m):
    require(type(m) is int and m >= 2, 'm must be an integer at least two')
    return {'loss_exponent': 65536*m*m, 'margin_exponent': 8193*m*m,
            'bulk_displacement_exponent': 8196*m*m}


def validate_budget(bulk, rare, ab, error):
    # Normalize desired margin coefficient to one. Pair mass is AA+2AB+BB.
    require(bulk >= 1 and rare >= 1 and ab >= 2 and error <= F(1, 2),
            'pair-loss or error coefficient budget fails')


def controls():
    # Each universal polynomial bound is certified by its base and a
    # symbolic upper/lower bound on consecutive-integer growth factors.
    triples = [(1, 1, 1), (2, 1, 1), (3, 1, 1), (6, 1, 2),
               (6, 2, 2), (12, 2, 2), (96, 2, 3), (24, 2, 3),
               (16, 2, 2), (2, 3, 2), (102, 4, 4)]
    for a, p, b in triples:
        require(a*2**p <= 2**(4*b), 'polynomial base fails')
        require(F(3, 2)**p <= 2**(5*b), 'polynomial induction fails')

    exponents = {
        'c0_lower': 36+2,
        'tau_lower': 361+3,
        'rho_lower': 364+758+3,
        'beta_prefactor_lower': 2+364+722+2,
        'beta_volume_lower': 3*1125+1,
        'beta_lower': 1090+3376,
        'alpha_upper': 65536-2*8196-2,
        'eta_upper': 65536//2-8196-2,
        'alignment_upper': 65536//2-2,
        'bulk_error_upper': 8196-2,
        'mass_error_upper': 65536-4*8196-8-4,
        'mixed_error_upper': 65536//2-2*8196-9-3,
    }
    require(exponents['beta_lower'] <= 4608, 'beta slack lost')
    require(exponents['eta_upper'] >= 768, 'repair guard fails')
    require(768 >= 761, 'polarization threshold fails')
    require(exponents['alignment_upper'] >= 3, 'alignment guard fails')
    require(exponents['alpha_upper'] >= 4, 'conditional covariance fails')
    require(65536 >= 8198, 'one-label loss restoration fails')
    require((8192-4608)*4 >= 2, 'rare coefficient fails')
    for key, divisor in [('bulk_error_upper', 2), ('mass_error_upper', 3),
                         ('mixed_error_upper', 3)]:
        require((exponents[key]-8192)*4 >= divisor, 'error budget fails')
    require(8193*4 >= 8192*4+1, 'final coefficient fails')
    validate_budget(F(1), F(2), F(2), F(1, 2))

    base = [(-1, 0, 0), (-2, 1, 0), (-2, 0, 1), (-2, -1, -1), (1, 0, 0)]
    source = [tuple(F(t, 6) for t in p) for p in base]
    target = [(-abs(x), y, z) for x, y, z in source]
    cases = []
    pair_checks = projection_checks = reflection_checks = 0
    for k in (1, 4, 8, 16, 24, 40, 64):
        alpha = F(1, 2**k)
        weights = [(1-alpha)/4]*4+[alpha]
        xs, ys = center(source, weights), center(target, weights)
        hs = [sub(y, x) for x, y in zip(xs, ys)]
        psd(matrix(xs, ys, weights))
        covariance_floor(xs, weights, F(1, 384))
        require(max(map(norm2, xs)) <= F(1, 4), 'radius fails')
        loss = [[norm2(sub(x, z))-norm2(sub(y, w))
                 for z, w in zip(xs, ys)] for x, y in zip(xs, ys)]
        d = q2 = F(0)
        for i, j in product(range(5), repeat=2):
            a, dh = sub(xs[i], xs[j]), sub(hs[i], hs[j])
            require(loss[i][j] >= 0, 'fold not contractive')
            require(-2*dot(a, dh) == loss[i][j]+norm2(dh), 'bulk identity')
            d += weights[i]*weights[j]*loss[i][j]
            q2 += weights[i]*weights[j]*loss[i][j]**2
            pair_checks += 1
        ms = sum((w*norm2(h) for w, h in zip(weights, hs)), F(0))
        require(d == F(7, 18)*alpha*(1-alpha), 'mean-loss formula')
        require(ms == alpha*(1-alpha)/9, 'mean displacement formula')
        require(q2/d == F(13, 63), 'quartic ratio formula')
        require(max(map(norm2, hs)) == ((1-alpha)/3)**2, 'rare displacement')
        require(sum(weights[i]*norm2(hs[i]) for i in range(4))
                == alpha**2*(1-alpha)/9, 'bulk displacement formula')
        for i in range(5):
            qi = norm2(xs[i])-norm2(ys[i])
            require(sum(weights[j]*loss[i][j] for j in range(5)) == qi+d/2,
                    'one-label conditional loss')
        # Repair the background against the rare point, using definitions.
        x, y, h = xs[4], ys[4], hs[4]
        q = norm2(x)-norm2(y)
        zs = [project(z, h, q) for z in xs]
        for j, (z, zp, hz) in enumerate(zip(xs, zs, hs)):
            require(q+2*dot(zp, h) >= 0, 'projection on wrong side')
            require(loss[4][j] == q+2*dot(z, h)+2*dot(sub(y, z), hz)-norm2(hz),
                    'defect identity')
            require(norm2(sub(zp, z))*norm2(h) <= 9*F(384)**2*norm2(hz),
                    'projection cost bound')
            projection_checks += 1
        b = mean(zs, weights)
        xp, yp = sub(x, b), sub(y, b)
        qp = norm2(xp)-norm2(yp)
        require(qp == q+2*dot(b, h), 'translated loss')
        for u in [(F(0), F(0), F(0)), xp, yp, (F(1), F(-2), F(3))]:
            su = reflect(u, h, qp)
            require(reflect(su, h, qp) == u, 'reflection involution')
            require(reflect(xp, h, qp) == yp, 'reflection swaps centers')
            require(norm2(sub(u, xp))-norm2(sub(u, yp)) == qp+2*dot(u, h),
                    'Gaussian exponent gap')
            for z in zs:
                zp = sub(z, b)
                lhs = norm2(sub(su, zp))-norm2(sub(u, zp))
                rhs = (qp+2*dot(u, h))*(qp+2*dot(zp, h))/norm2(h)
                require(lhs == rhs, 'reflection product identity')
                reflection_checks += 1
        cases.append({'alpha': str(alpha), 'D': str(d), 'M': str(ms),
                      'Q_over_D': str(q2/d), 'projection_moves': sum(a != b for a, b in zip(xs, zs))})

    # Non-axial normals and non-fold deformation: all checks are rational,
    # including normals of irrational Euclidean length.
    tetra = [tuple(map(F, p)) for p in
             [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]
    targets = [tuple(a*t for a, t in zip((F(3, 4), F(4, 5), F(5, 6)), p))
               for p in tetra]
    for x, y in zip(tetra, targets):
        h = sub(y, x)
        q = norm2(x)-norm2(y)
        require(reflect(x, h, q) == y, 'non-axial reflection')
        for z, w in zip(tetra, targets):
            hz = sub(w, z)
            delta = norm2(sub(x, z))-norm2(sub(y, w))
            require(delta >= 0, 'diagonal contraction')
            require(delta == q+2*dot(z, h)+2*dot(sub(y, z), hz)-norm2(hz),
                    'non-axial defect')
            zp = project(z, h, q)
            require(q+2*dot(zp, h) >= 0, 'non-axial projection')
            require(norm2(sub(zp, z))*norm2(h) <= 36*norm2(hz),
                    'non-axial projection cost')
            projection_checks += 1
            for u in tetra:
                su = reflect(u, h, q)
                require(norm2(sub(su, zp))-norm2(sub(u, zp)) ==
                        (q+2*dot(u, h))*(q+2*dot(zp, h))/norm2(h),
                        'non-axial reflection product')
                reflection_checks += 1

    # Calibration remains in logarithmic/exponent form; do not construct
    # a rational with a multi-billion-bit denominator.
    calibration = exponent_guard(384)
    require(F(7, 18) < 1, 'D<=alpha calibration')
    require(F(13, 63) > F(1, 2**48), 'quartic guard must fail')
    require(F(250, 3) < 384, 'threshold-volume calibration')

    rejected = []
    def rejects(name, fn):
        try:
            fn()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('adverse control was accepted: '+name)
    rejects('m_below_two', lambda: exponent_guard(1))
    rejects('noninteger_m', lambda: exponent_guard(F(5, 2)))
    rejects('covariance_collapse', lambda: covariance_floor(
        [(F(0), F(0), F(0))], [F(1)], F(1, 384)))
    rejects('missing_AB_factor', lambda: validate_budget(F(1), F(2), F(1), F(1, 2)))
    rejects('excess_error', lambda: validate_budget(F(1), F(2), F(2), F(3, 4)))
    rejects('zero_projection_normal', lambda: project((F(0),)*3, (F(0),)*3, F(1)))
    bad = project((F(-2), F(0), F(0)), (F(1), F(0), F(0)), F(2))
    rejects('wrong_projection_orientation', lambda: require(
        2+2*dot(sub(scale(2, (F(-2), F(0), F(0))), bad), (F(1), F(0), F(0))) >= 0,
        'reflected displacement has wrong side'))

    return {'status': 'EXPLICIT_RARE_MOVE_CONTROLS_PASS',
            'scope': 'exact finite algebra and exponent controls; analytic proof not formalized',
            'polynomial_inductions': triples, 'exponent_budget': exponents,
            'rare_fold': cases, 'fold_pair_checks': pair_checks,
            'projection_checks': projection_checks, 'reflection_checks': reflection_checks,
            'symbolic_small_mass_calibration': calibration, 'rejected_controls': rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true', help='print canonical expected record')
    args = parser.parse_args()
    record = controls()
    raw = (json.dumps(record, sort_keys=True, indent=2)+'\n').encode()
    if args.emit:
        print(raw.decode(), end='')
        return
    require(raw == Path(__file__).with_name('PROJECTION_EXPECTED.json').read_bytes(), 'expected record differs')
    print(json.dumps({'status': record['status'], 'expected_sha256': hashlib.sha256(raw).hexdigest(),
                      'pair_checks': record['fold_pair_checks'],
                      'projection_checks': record['projection_checks'],
                      'reflection_checks': record['reflection_checks'],
                      'rejected_controls': len(record['rejected_controls'])}, sort_keys=True))


if __name__ == '__main__':
    main()
