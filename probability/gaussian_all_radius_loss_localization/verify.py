#!/usr/bin/env python3
"""Exact compact controls; no Gaussian quadrature or sign oracle."""
from fractions import Fraction as F
from itertools import product
from math import comb, factorial, isqrt
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent


def require(ok, why):
    if not ok:
        raise ValueError(why)


def integer(x, low=0):
    require(type(x) is int and x >= low, 'invalid integer')
    return x


def rational(x):
    require(type(x) in (str, int), 'use exact fraction strings or integers')
    return F(x)


def pow2(n):
    return F(2**n) if n >= 0 else F(1, 2**(-n))


def ceil_log2(x):
    require(x > 0, 'positive logarithm argument required')
    n = x.numerator.bit_length() - x.denominator.bit_length()
    if pow2(n) < x:
        n += 1
    require(pow2(n-1) < x <= pow2(n), 'log ceiling check failed')
    return n


def constants(R, kappa, L):
    integer(R, 1); integer(L)
    require(type(kappa) in (F, int), 'exact covariance floor required')
    kappa = F(kappa)
    require(kappa > 0, 'positive covariance floor required')
    c = isqrt(2*(L+1))
    c += c*c < 2*(L+1)
    B = 2*R+c
    lam = 1+4*R*R/kappa
    return {'B': B, 'r': 32*B*B-1, 'lambda': lam,
            'K': 56*B**3*pow2(3*L)*lam,
            'tail': 4*(2*R+3)**3*lam*pow2(296*R*R)}


def middle_budget(R, kappa, L, eta):
    require(type(eta) in (F, int), 'exact margin required')
    eta = F(eta)
    require(0 < eta <= 1, 'margin must be in (0,1]')
    c = constants(R, kappa, L)
    J = ceil_log2(2*c['K']/eta)
    require(c['K']*pow2(-J) <= eta/2, 'mesh budget failed')
    return {'R': R, 'kappa': str(kappa), 'L': L,
            'eta': str(eta), 'B': c['B'], 'holder_denominator': c['r'],
            'mesh_negative_log2': c['r']*J, 'J': J}


def whole_curve_budget(R, kappa, zeta):
    require(type(zeta) in (F, int), 'exact tolerance required')
    zeta = F(zeta)
    require(0 < zeta <= 1, 'tolerance must be in (0,1]')
    tail = constants(R, kappa, 0)['tail']
    t = ceil_log2(16*tail/zeta)
    L = 2*t
    c = constants(R, kappa, L)
    p = ceil_log2(8*c['K']/zeta)
    exponent = 2*c['r']*p
    b = ceil_log2(2/zeta)
    prefactor = 3*R*R+b+exponent+1
    require(2*tail*pow2(-t) <= zeta/8, 'tail budget failed')
    require(c['K']*pow2(-p) <= zeta/8, 'reconstruction budget failed')
    require(pow2(-b) <= zeta/2, 'cubature tolerance failed')
    # q=prefactor*2^exponent is kept symbolic. For the cubature guard:
    # q>=3R^2*2^exponent, and
    # (prefactor-2)*2^exponent >= b+exponent-4.
    require(exponent >= 1 and prefactor >= 3*R*R, 'degree guard failed')
    require(prefactor-2 >= b+exponent-4, 'symbolic degree guard failed')
    return {'R': R, 'kappa': str(kappa), 'zeta': str(zeta), 'L': L,
            'B': c['B'], 'holder_denominator': c['r'], 'p': p,
            'log2_N_plus_2': exponent, 'cubature_b': b,
            'q_equals_prefactor_times_2_to_exponent': prefactor,
            'q_exponent': exponent,
            'atom_cap': '2*binom(2*q+3,3)-1',
            'status': 'SYMBOLIC_BUDGET_ONLY_NO_ENUMERATION'}


def norm2(x):
    return sum(z*z for z in x)


def sub(x, y):
    return [a-b for a, b in zip(x, y)]


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def det(A):
    if not A:
        return F(1)
    return sum((-1)**j*A[0][j]*det([row[:j]+row[j+1:] for row in A[1:]])
               for j in range(len(A)))


def covariance(points, weights):
    mean = [sum(w*x[j] for w, x in zip(weights, points)) for j in range(3)]
    centered = [sub(x, mean) for x in points]
    cov = [[sum(w*x[i]*x[j] for w, x in zip(weights, centered))
            for j in range(3)] for i in range(3)]
    return centered, cov


def validate(points, images, weights, R, kappa, s=F(1)):
    integer(R, 1)
    require(kappa > 0 and s > 0, 'positive covariance and variance required')
    require(len(points) == len(images) == len(weights) > 0, 'bad lengths')
    require(all(len(x) == 3 for x in points+images), 'dimension must be three')
    require(all(w >= 0 for w in weights) and sum(weights) == 1, 'bad masses')
    X, cov = covariance(points, weights)
    require(max(norm2(x) for x in X) <= R*R*s, 'centered radius guard failed')
    A = [[cov[i][j]/s-(kappa if i == j else 0) for j in range(3)]
         for i in range(3)]
    from itertools import combinations
    for k in (1, 2, 3):
        for inds in combinations(range(3), k):
            require(det([[A[i][j] for j in inds] for i in inds]) >= 0,
                    'covariance guard failed')
    losses = []
    D = F(0)
    identities = 0
    for i, x in enumerate(points):
        for j, xp in enumerate(points):
            a = sub(x, xp); b = sub(images[i], images[j]); h = sub(b, a)
            loss = norm2(a)-norm2(b)
            require(loss >= 0, 'not a contraction on retained support')
            losses.append(loss/s)
            D += weights[i]*weights[j]*loss/s
            for t in (F(0), F(1, 4), F(1, 2), F(3, 4), F(1)):
                z = [v+t*w for v, w in zip(a, h)]
                require(-2*dot(z, h) == loss+(1-2*t)*norm2(h),
                        'straight-path loss identity failed')
                identities += 1
    return D, cov, identities


def interpolation_controls():
    checks = 0
    for n in range(2, 12):
        # Uneven rational nodes, independently checked by monomial reproduction.
        nodes = [F(j*j+2*j, n*n+n) for j in range(n)]
        point = F(2)
        coeff = []
        for j, x in enumerate(nodes):
            a = F(1)
            for k, y in enumerate(nodes):
                if k != j:
                    a *= (point-y)/(x-y)
            coeff.append(a)
        for degree in range(n):
            require(sum(a*x**degree for a, x in zip(coeff, nodes)) == point**degree,
                    'interpolation reproduction failed')
            checks += 1
        r = n-1
        require(sum(F(1, factorial(j)*factorial(r-j)) for j in range(n))
                == F(2**r, factorial(r)), 'Lagrange coefficient sum failed')
        checks += 1
    # Exact small controls of the two formulas for even Gaussian moments.
    moment = 1
    for m in range(1, 25):
        moment *= 2*m-1
        require(moment == factorial(2*m)//(2**m*factorial(m)), 'Gaussian moment failed')
        checks += 1
    # Direct factorial remainders at actual choices m=16 B^2.
    remainders = []
    for B in (1, 2, 3, 4, 6):
        m = 16*B*B
        remainder = F((2*B*B)**m, factorial(m))
        require(remainder <= F(3, 8)**m <= pow2(-m), 'remainder failed')
        remainders.append({'B': B, 'm': m, 'bound': 'at_most_2^-m'})
    for R, L in product((1, 2, 3, 8), (0, 1, 4, 16, 100)):
        c = constants(R, F(1, 100), L)
        B = c['B']; m = 16*B*B
        require((B-2*R)**2 >= 2*(L+1) and m >= L+2, 'far-anchor bound failed')
        checks += 1
    return checks, remainders


def beta_variance_controls():
    checks = 0
    for N in range(13):
        for u in (F(0), F(1, 8), F(1, 3), F(1, 2), F(7, 8), F(1)):
            # Two independent calculations: exact mixture and moment expansion.
            second = sum(F(comb(N, j))*u**j*(1-u)**(N-j)
                         * (F((j+1)*(j+2), (N+2)*(N+3))
                            -2*u*F(j+1, N+2)+u*u) for j in range(N+1))
            formula = F(2)*((N-3)*u*(1-u)+1)/((N+2)*(N+3))
            require(second == formula and second <= F(1, N+2), 'beta variance failed')
            checks += 1
    return checks


def pins():
    records = json.loads((HERE/'INPUTS.json').read_text())
    for record in records:
        path = HERE/record['path']
        require(hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256'],
                'dependency drift: '+record['path'])
    return len(records)


def run_controls():
    pin_count = pins()
    require(constants(2, 1, 4) == constants(2, F(1), 4), 'integer covariance alias failed')
    require(middle_budget(2, 1, 4, 1) == middle_budget(2, F(1), 4, F(1)),
            'integer middle-budget aliases failed')
    require(whole_curve_budget(2, 1, 1) == whole_curve_budget(2, F(1), F(1)),
            'integer whole-curve aliases failed')
    interpolation, remainders = interpolation_controls()
    beta = beta_variance_controls()
    cube = [[F(z, 2) for z in p] for p in product((-1, 1), repeat=3)]
    weights = [F(1, 8)]*8
    records = []
    total_identities = 0
    for j in (0, 2, 10, 40):
        t = F(0) if j == 0 else pow2(-j)
        target = [[(1-t)*z for z in x] for x in cube]
        D, cov, count = validate(cube, target, weights, 1, F(1, 4))
        total_identities += count
        M = sum(w*norm2(sub(x, y)) for w, x, y in zip(weights, cube, target))
        require(M <= 2*D/F(1, 4), 'aligned Procrustes bound failed')
        require(D == F(3, 2)*(2*t-t*t), 'ordered loss normalization failed')
        records.append({'t': str(t), 'D': str(D), 'M': str(M)})
    # Actual accepted obstruction fixture: only hypotheses and pair algebra are
    # consumed here, not a replay of its motion barrier or any Gaussian sign.
    raw = json.loads((HERE/'../gaussian_strict_screw_motion_barrier/WITNESS.json').read_text())
    source = [[rational(z) for z in row['source']] for row in raw['sites']]
    target = [[rational(z) for z in row['target']] for row in raw['sites']]
    w = [F(1, len(source))]*len(source)
    D, cov, count = validate(source, target, w, 8, F(1, 1000))
    total_identities += count
    require(D > 0, 'strict fixture lost positive loss')
    centered, _ = covariance(source, w)
    # Frame and variance normalization: signed coordinate permutation and
    # separate translations, scaling both clouds and s by consistent factors.
    frame = lambda x: [2*x[2]+F(7, 3), -2*x[0]-5, 2*x[1]+11]
    frame_y = lambda x: [-2*x[1]-3, 2*x[2]+8, -2*x[0]+F(1, 5)]
    D2, _, count = validate(list(map(frame, source)), list(map(frame_y, target)),
                            w, 8, F(1, 1000), F(4))
    total_identities += count
    require(D == D2, 'independent frame or variance invariance failed')
    bad = []
    def reject(name, fn):
        try:
            fn()
        except (ValueError, ZeroDivisionError):
            bad.append(name)
        else:
            raise ValueError('invalid input accepted: '+name)
    reject('zero_covariance', lambda: constants(2, F(0), 4))
    reject('zero_radius_integer', lambda: constants(0, F(1), 4))
    reject('noninteger_radius', lambda: constants(F(3, 2), F(1), 4))
    reject('negative_level_index', lambda: constants(2, F(1), -1))
    reject('zero_margin', lambda: middle_budget(2, F(1), 4, F(0)))
    reject('zero_tolerance', lambda: whole_curve_budget(2, F(1), F(0)))
    reject('inflated_covariance', lambda: validate(cube, cube, weights, 1, F(1)))
    reject('undersized_radius', lambda: validate(source, target, w, 1, F(1, 1000)))
    reject('expansive_map', lambda: validate(cube, [[2*z for z in x] for x in cube],
                                            weights, 1, F(1, 4)))
    reject('wrong_mass', lambda: validate(cube, cube, [F(1, 9)]*8, 1, F(1, 4)))
    reject('zero_variance', lambda: validate(cube, cube, weights, 1, F(1, 4), F(0)))
    reject('floating_input', lambda: rational(0.5))
    reject('floating_covariance', lambda: constants(2, 0.5, 4))
    reject('floating_margin', lambda: middle_budget(2, F(1, 4), 4, 0.5))
    reject('floating_tolerance', lambda: whole_curve_budget(2, F(1, 4), 0.5))
    return {'status': 'ALL_RADIUS_LOSS_LOCALIZATION_CONTROLS_PASS',
            'pins': pin_count, 'interpolation_and_gaussian_controls': interpolation,
            'direct_remainder_controls': remainders, 'beta_variance_controls': beta,
            'straight_path_pair_identities': total_identities,
            'vanishing_and_zero_loss': records,
            'strict_screw_hypothesis_control': {
                'sites': len(source), 'R': 8, 'kappa': '1/1000', 's': 1,
                'max_centered_radius_squared': str(max(norm2(x) for x in centered)),
                'covariance': [[str(z) for z in row] for row in cov],
                'D': str(D), 'Gaussian_sign': 'NOT_TESTED'},
            'middle_budgets': [middle_budget(R, k, L, eta) for R, k, L, eta in (
                (1, F(1, 64), 4, F(1, 256)), (2, F(1, 64), 4, F(1, 256)),
                (8, F(1, 1000), 6, F(1, 1024)))],
            'whole_curve_budgets': [whole_curve_budget(R, k, zeta) for R, k, zeta in (
                (1, F(1, 64), F(1, 16)), (2, F(1, 64), F(1, 16)))],
            'rejected': bad,
            'trust': 'Exact finite controls; universal analytic theorem unformalized.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', type=Path,
                        help='write computed record; never changes the expected record implicitly')
    args = parser.parse_args()
    record = run_controls()
    text = json.dumps(record, indent=2, sort_keys=True)+'\n'
    if args.record:
        args.record.write_text(text)
    else:
        require(text == (HERE/'EXPECTED.json').read_text(), 'expected-record mismatch')
    print(record['status'])
    print('SHA256 '+hashlib.sha256(text.encode()).hexdigest())


if __name__ == '__main__':
    main()
