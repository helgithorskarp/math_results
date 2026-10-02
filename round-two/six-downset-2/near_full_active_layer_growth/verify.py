"""Portable exact audit of the active-layer growth separator.

Universal polynomial identities and signs are checked by coefficients;
bounded independent RREF and original-vertex checks validate conventions.
The real/averaging and Chernoff bridges remain ordinary unformalized proofs.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import comb
from pathlib import Path

from affine import affine
from certificate import (base, bulk, certified_range, check_rows, choose, forms,
                         moment_upper, parameters, profiles, quadratic, require,
                         scalar, tail)
from poly import FIRST, SECOND, P

ROOT = Path(__file__).resolve().parent


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def symbolic(circle_damage=False, moment_damage=False, margin_damage=False):
    n, z = FIRST, SECOND
    h, V = 2*n+5, 16*n**4+(2*n+5)**2*z*z
    pn = h**3*z**3+int(circle_damage)
    qn = 16*n**4+3*h*h*z*z
    require(pn*pn+4*n**4*qn*qn-(4*n**4+h*h*z*z)*V*V == 0, 'Universal circle coefficient identity')

    b, t = FIRST, SECOND
    polynomial = b*b+4*b*t+4*(1-b)*t*t
    require(polynomial*(1+t)**2-(b*(1+t)+2*t)**2 == 4*t**3*(2+t-b*(1+t)), 'Exact square upper-bound remainder')
    require(polynomial == (b+2*t)**2-4*b*t*t, 'Nonnegative moment integrand')

    n, T = FIRST, SECOND
    B11 = T*n*n-9*T*n+16*T-n**3+9*n*n-8*n-16
    B12 = 2*(-T*n+4*T+2*n*n-4*n-4)
    B22 = -4*(-T*n+2*T+2*n*n-2*n-2)
    s, den, q = T-n, n*(n-1), n-2
    bulk0 = 2*T-2-2*n-n*(n-1)/2
    bulk1 = n*T-2*n*n
    require(B11+q*B12+2*q*n*(T-2*n)-s*den == 0, 'Universal first-row star')
    require((n-1)*B11+(n-1)*q*B12/2+2*q*(n-1)*bulk0-(T-2)*den == 0, 'Universal first-row center')
    require(B12+B22-2*bulk1 == 0, 'Universal second-row star')
    require(q*B12+q*B22/2-2*q*bulk0+s*den-(T-2)*den == 0, 'Universal second-row center')

    lp = n*s-n*n+B11
    lr = n*(n-1)*(n-2)+(n-2)*B22/4
    lpr = (n-2)*B12-2*n*(n-1)*(n-2)
    require(lp+lr+lpr == 4*(T-n-1), 'Exact odd-profile lower energy')
    up = n*(T-1)-B11
    ur = n*(n-1)*(2*n-3)-(n-2)*B22/4
    upr = -(n-2)*B12-2*n*(n-1)*(n-2)
    Ulow = 25*up+(2*n+10)**2*ur+5*(2*n+10)*upr
    bulk_weight = 2*T-n*n-n-2
    # Even Rademacher index multiplicities: one repeated index, or two pairs.
    fourth = n+6*n*(n-1)/2
    require(fourth == 3*n*n-2*n, 'Independent fourth-moment multiplicities')
    if moment_damage:
        fourth += 1
    kappa = (2*n+5)**2
    # Clear 64*n^8*(n-1) in the scalar upper bound from PROOF.md.
    numerator = (256*n**8*(n-1)*(T-n-1)+64*n**4*(n-1)*Ulow
                 -256*n**6*(n-2)**2*bulk_weight
                 +32*T*n**6*(5*n-9)**2
                 -16*T*n**4*(n-1)*(5*n-9)*kappa
                 +T*(n-1)*(2*n*n+3*n-9)*kappa*kappa*fourth.divide_first_monomial(1))
    An = P({(i, 0): v for i, v in enumerate([-11250, 2625, 19075, 8170, -7608, -7952, 592, 192])})
    Rn = P({(i, 0): v for i, v in enumerate([-75, 236, -70, -119, 28, 16])})
    require(numerator == -T*(n-1)*An+64*n**5*Rn, 'Universal closed moment numerator')
    inequalities = {'negative_T_margin': An-(128+int(margin_damage))*n**7,
                    'rest_below20n': 20*n**4*(n-1)-Rn,
                    'tail_cost_below3n': 2*n**3-16*n*n-5*n+25,
                    'exponential_step': n*n-2*n-1}
    shifted = {name: poly.substitute(n+64, 0).integers() for name, poly in inequalities.items()}
    require(all(all(v > 0 for v in row) for row in shifted.values()), 'Strict shifted coefficient signs for n>=64')
    require(2**63 > 40*64**2, 'Exponential domination base T64>40*64^2')
    return {'domain': 'Characteristic0 Q[n,z], Q[b,t], Q[n,T]; T=2^(n-1)',
            'circle_identity': True, 'square_remainder_identity': True,
            'moment_integrand_nonnegative_identity': True, 'low_row_identities': 4,
            'odd_lower_energy': '4*(T-n-1)', 'moment_numerator_identity': True,
            'moments': [[1], [0, 1], fourth.integers()],
            'negative_T_numerator': An.integers(), 'rest_numerator': Rn.integers(),
            'positive_shift64_coefficients': shifted,
            'exponential_base': {'T64': 2**63, 'forty64_squared': 40*64**2},
            'uniform_sign_domain': 'All real n>=64 for rational coefficient bounds; integer n>=64 for exponential induction'}


def finite(n, k, altered=None):
    free_pairs, recover = affine(n)
    _, _, s, _ = parameters(n)
    values = [Q(s) if a+b == n else Q(0) for a, b in free_pairs]
    B = recover(values)
    require(B == base(n), 'Independent full RREF base recovery')
    p, q = profiles(n, k) if altered is None else altered
    K, U = forms(n, B)
    cost = quadratic(K, p)+quadratic(U, q)
    require(quadratic(K, p) == 4*(2**(n-1)-n-1), 'Physical odd-profile lower cost')
    require(cost == scalar(n, k), 'Physical pairing versus separate closed scalar')
    allowed = [i for i, (a, b) in enumerate(free_pairs) if a+b == n or a <= k]
    expected_noncomplements = sum(max(0, n-2*a) for a in range(3, k+1))
    expected_complements = n//2-2
    require(len(allowed) == expected_noncomplements+expected_complements, 'Complete allowed coordinate census')
    c, d = Q(2, n), -Q(2*n+5, n*n)
    f, g = [v-1 for v in p], [v-c-d*a for a, v in enumerate(q, 1)]
    for i in allowed:
        change = list(values); change[i] += 1
        BB = recover(change)
        KK, UU = forms(n, BB)
        DK = [[v-K[a][b] for b, v in enumerate(row)] for a, row in enumerate(KK)]
        require(all(sum(row) == 0 and sum((b+1)*v for b, v in enumerate(row)) == 0 for row in DK), 'Physical affine kernels1,a')
        a, b = free_pairs[i]
        expected = (2-int(a == b))*comb(n, a)*choose(n-a, b)*(f[a-1]*f[b-1]-g[a-1]*g[b-1])
        actual = quadratic(KK, p)+quadratic(UU, q)-cost
        require(expected == actual == 0, 'Every permitted real-face coefficient cancels')
    return {'n': n, 'k': k, 'total_middle_coordinates': len(free_pairs),
            'allowed_noncomplements': expected_noncomplements, 'allowed_complements': expected_complements,
            'permitted_coordinate_checks': len(allowed), 'physical_constant': str(cost),
            'profile_sha256': digest([[str(v) for v in profile] for profile in (p, q)]),
            'finite_constant_negative': cost < 0,
            'finite_sign_not_used_for_uniform_bridge': True}


def literal(empty_damage=False, normalization_damage=False):
    n, k = 7, 2
    r, T, s, m = parameters(n)
    B = base(n); check_rows(n, B)
    masks = [a for a in range(1, 1 << n) if a.bit_count() <= r]
    C = [[Q(s*int(i == j)-1)+B[a.bit_count()][b.bit_count()]*int(not(a&b))
          for j, b in enumerate(masks)] for i, a in enumerate(masks)]
    N, h = m+1, T-1
    require(len(masks) == m and all(sum(row) == 0 for row in C), 'Original-index centered core')
    L = [[Q(1)]*N]+[[Q(1)]+[v+1 for v in row] for row in C]
    if empty_damage:
        L[0][0] += 1
    full = [0]+masks
    M = [[Q(L[i][j]-s*int(i == j), h) for j in range(N)] for i in range(N)]
    require(all(sum(row) == 1 for row in M), 'Original regularity including empty')
    require(all(M[i][j] == 0 for i, a in enumerate(full) for j, b in enumerate(full) if a&b), 'Original intersection support')
    require(M[0][0] == Q(1-s, h) and all(v == 1 for v in L[0]), 'Actual empty loop and row')
    for point in range(n):
        star = [Q(int(bool(a&(1 << point)))) for a in masks]
        require(all(sum(v*x for v, x in zip(row, star)) == 0 for row in C), 'Every original point-star kernel')
    U = [[Q(N*int(i == j)-1)-C[i][j] for j in range(m)] for i in range(m)]
    p, q = profiles(n, k)
    pp, qq = [p[a.bit_count()-1] for a in masks], [q[a.bit_count()-1] for a in masks]
    K0, U0 = forms(n, B)
    require(quadratic(C, pp) == quadratic(K0, p), 'Original lower physical pairing')
    scale = Q(1, 2) if normalization_damage else Q(1)
    require(scale*quadratic(U, qq) == quadratic(U0, q), 'Original upper physical pairing')
    require(quadratic(C, pp)+quadratic(U, qq) == scalar(n, k), 'Original-index closed scalar')
    return {'n': n, 'k': k, 'full_order': N, 'nonempty_order': m,
            'point_stars_checked': n, 'empty_loop': str(M[0][0]),
            'lower_pairing': str(quadratic(C, pp)), 'upper_pairing': str(quadratic(U, qq)),
            'physical_coefficient_has_no_factor2': True,
            'arithmetic_convention_check_not_PSD_claim': True}


def bounded_tail_examples():
    rows = []
    for n in (64, 128, 256):
        largest = max(k for k in range(2, (n-1)//2+1) if certified_range(n, k))
        B, T = tail(n, largest), 2**(n-1)
        require(6*n*n*B <= T and 6*n*n*tail(n, largest+1) > T, 'Exact largest k meeting the stated sufficient condition')
        row = {'n': n, 'largest_certified_k': largest, 'forced_minimum_set_size': largest+1,
               'tail': B, 'six_n_squared_tail': 6*n*n*B, 'T': T}
        if n == 64:
            actual, moment = scalar(n, largest), moment_upper(n)
            require(scalar(n, 2) <= moment < -Q(2*T, n)+20*n, 'Independent exact n64 moment inequality')
            require(actual <= scalar(n, 2)+3*n*B < -Q(T, n), 'Exact n64 tail and negative margin')
            row.update({'constant': str(actual), 'negative_margin_target': str(Q(T, n))})
        rows.append(row)
    return rows


def rejected(function):
    try:
        function()
    except (ValueError, IndexError):
        return True
    return False


def controls():
    tests = [('changed circle numerator', lambda: symbolic(circle_damage=True)),
             ('false fourth moment', lambda: symbolic(moment_damage=True)),
             ('false strong negative coefficient', lambda: symbolic(margin_damage=128)),
             ('changed actual empty loop', lambda: literal(empty_damage=True)),
             ('wrong upper physical factor', lambda: literal(normalization_damage=True)),
             ('oversized RREF allocation', lambda: affine(64))]
    p, q = profiles(8, 3)
    q = list(q); q[2] += 1
    tests.append(('changed allowed three-set profile', lambda: finite(8, 3, (p, q))))
    for label, function in tests:
        require(rejected(function), 'Damage rejected: '+label)
    return [label for label, _ in tests]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = {'agent': 'six-downset-2', 'role': 'researcher',
              'claim': 'Unbounded active-layer growth for all real centered capped H on D(n,n-2)',
              'scope': 'Every integer n>=64 and2<=k<n/2 with6*n^2*sum_{a=3}^k binom(n,a)<=2^(n-1)',
              'proof_status': 'Exact rational/coefficient certificates; ordinary bridges unformalized; independently unreviewed',
              'universal': symbolic(), 'finite_rref_conventions': [finite(8, 3), finite(17, 3), finite(20, 4)],
              'literal': literal(), 'exact_tail_examples': bounded_tail_examples(),
              'rejected_controls': controls(), 'arithmetic': 'CPython integers/fractions.Fraction; no CAS or solver',
              'no_full_large_downset_matrix': True}
    body = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.check:
        require(body == args.check.read_text(), 'Entire frozen expected record mismatch')
    if args.output:
        args.output.write_text(body)
    print(json.dumps({'ok': True, 'result_sha256': sha256(body.encode()).hexdigest(),
                      'unbounded_minimum_n': 64, 'circle_identity': True,
                      'rref_direction_checks': sum(v['permitted_coordinate_checks'] for v in result['finite_rref_conventions']),
                      'literal_order': result['literal']['full_order'],
                      'exact_tail_minimum_sizes': [[v['n'], v['forced_minimum_set_size']] for v in result['exact_tail_examples']],
                      'controls': len(result['rejected_controls'])}, sort_keys=True))


if __name__ == '__main__':
    main()
