#!/usr/bin/env python3
"""Exact finite premises for the retained-interaction replica proof.

Standard-library Python 3.11+. No floating-point sign, solver, quadrature,
external input, or assert statement is used. See PROOF.md for the universal
analytic argument and the boundary of what this executable verifies.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import comb, isqrt
from pathlib import Path
import json
import sys

DEN = 2**32
CASES = {
    9: (F(13, 20), F(4), F(49, 10), F(4), F(1, 200)),
    12: (F(1, 3), F(23, 10), F(29, 10), F(12, 5), F(1, 2000)),
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def roots():
    result = {}
    for n in range(2, 15):
        k = isqrt(n * DEN**2)
        lo = F(k, DEN)
        hi = lo if lo*lo == n else F(k+1, DEN)
        require(0 <= lo <= hi and lo*lo <= n <= hi*hi, 'Bad radical enclosure')
        result[n] = (lo, hi)
    return result


def power_to_bernstein(power):
    n = len(power)-1
    return [sum((power[k]*F(comb(i, k), comb(n, k)) for k in range(i+1)), F(0))
            for i in range(n+1)]


def direct_interval(power, left, width):
    n = len(power)-1
    local = [sum((power[j]*comb(j, k)*left**(j-k)*width**k
                  for j in range(k, n+1)), F(0)) for k in range(n+1)]
    return power_to_bernstein(local)


def split(control):
    rows = [list(control)]
    while len(rows[-1]) > 1:
        r = rows[-1]
        rows.append([(r[i]+r[i+1])/2 for i in range(len(r)-1)])
    return [r[0] for r in rows], [r[-1] for r in reversed(rows)]


def value(power, x):
    out = F(0)
    for c in reversed(power):
        out = out*x+c
    return out


def bernstein_value(control, t):
    n = len(control)-1
    return sum((c*comb(n, i)*t**i*(1-t)**(n-i)
                for i, c in enumerate(control)), F(0))


def check_rows(power, rows, count):
    require(len(rows) == count, 'Incomplete interval cover')
    for i, row in enumerate(rows):
        require(row == direct_interval(power, F(i, count), F(1, count)),
                'Incorrect coefficient row')
        require(min(row) > 0, 'Positive Bernstein premise failed')


def scalar_certificate(name, power, depth):
    count = 2**depth
    rows = [power_to_bernstein(power)]
    for _ in range(depth):
        rows = [child for row in rows for child in split(row)]
    check_rows(power, rows, count)
    evaluations = 0
    for i, row in enumerate(rows):
        n = len(power)-1
        for j in range(n+1):
            t = F(j, n)
            require(value(power, (i+t)/count) == bernstein_value(row, t),
                    'Polynomial identity mismatch')
            evaluations += 1
    failures = 0
    damaged = [list(row) for row in rows]
    damaged[0][0] += F(1, 10**12)
    for candidate in [rows[:-1], damaged]:
        try:
            check_rows(power, candidate, count)
        except ValueError:
            failures += 1
    require(failures == 2, 'Damaged certificate accepted')
    canonical = json.dumps([[str(c) for c in row] for row in rows],
                           separators=(',', ':')).encode()
    return {
        'name': name, 'degree': len(power)-1, 'subintervals': count,
        'positive_coefficients': count*len(power),
        'minimum': str(min(map(min, rows))),
        'power_coefficients': list(map(str, power)),
        'all_coefficients_sha256': sha256(canonical).hexdigest(),
        'direct_and_de_casteljau_agree': True,
        'exact_identity_evaluations': evaluations,
        'damaged_certificates_rejected': failures,
    }


def variance_controls():
    entries = 0
    parameters = []
    for m in range(2, 7):
        for ell in range(1, 5):
            n = m+ell
            u = [[F(-1, m) if i < m else F(i == m+k)
                  for i in range(n)] for k in range(ell)]
            for i in range(n):
                for j in range(n):
                    base = F(i == j)-F(1, m) if i < m and j < m else F(0)
                    one = sum((v[i]*v[j] for v in u), F(0))
                    cross = sum((u[k][i]*u[h][j]+u[h][i]*u[k][j]
                                 for k in range(ell) for h in range(k+1, ell)), F(0))
                    expected = F(i == j)-F(1, n)
                    require(base+F(n-1, n)*one-cross/n == expected,
                            'Centered block variance identity failed')
                    entries += 1
            alpha = F((n-1)*(m+1), n*m)
            power = ell*alpha
            require(alpha == 1+F(ell-1, m*n), 'Wrong tilt exponent')
            require(power-1 == (ell-1)*(1+F(ell, m*n)), 'Wrong outer Jensen exponent')
            require(alpha >= 1 and power >= 1, 'Jensen convexity lost')
            parameters.append({'base': m, 'added': ell, 'power': str(power)})
    require(F(2*(4-1)*3, 4*2) == F(9, 4), 'Wrong two-replica exponent')
    return {'matrix_entries': entries, 'parameter_controls': parameters}


def certificate():
    enclosure = roots()
    certificates = []
    constants = []
    for q, (a, b, c, lam, epsilon) in CASES.items():
        lower = [comb(q, j)*(enclosure[j+2][0] if j % 2 == 0
                             else -enclosure[j+2][1]) for j in range(q+1)]
        lower[0] -= a
        lower[1] += b
        lower[2] -= c
        lower[3] -= lam
        lower[4] += lam*F(216, 125)
        certificates.append(scalar_certificate('P'+str(q)+' minorant', lower,
                                               4 if q == 9 else 5))
        h = [F(0)]*10
        h[0], h[4], h[9] = a/8-epsilon, -b/27, c/64
        certificates.append(scalar_certificate('h'+str(q)+' minus epsilon', h,
                                               4 if q == 9 else 6))
        require(F(216, 125)/216 == F(1, 125), 'Monotone moment conversion failed')
        beta_coefficient = F(q+1, 4)*epsilon
        d2_coefficient = 8*beta_coefficient
        constants.append({'q': q, 'a': str(a), 'b': str(b), 'c': str(c),
                          'lambda': str(lam), 'epsilon': str(epsilon),
                          'coefficient_of_B2_over_s': str(beta_coefficient),
                          'coefficient_of_sqrt2_d2': str(d2_coefficient)})
    require(constants[0]['coefficient_of_sqrt2_d2'] == '1/10', 'q9 normalization')
    require(constants[1]['coefficient_of_sqrt2_d2'] == '13/1000', 'q12 normalization')
    a, b, c, _, _ = CASES[12]
    old_bound_control = a/8-b*F(4, 5)/27+c*F(4, 5)**3/64
    require(old_bound_control < 0, 'Old exponent rejection control failed')
    return {
        'arithmetic': 'Python integers/Fraction, exact dyadic radical enclosures',
        'root_denominator': DEN,
        'roots': {str(n): list(map(str, bounds)) for n, bounds in enclosure.items()},
        'certificates': certificates,
        'positive_coefficients': sum(x['positive_coefficients'] for x in certificates),
        'variance_controls': variance_controls(),
        'constants': constants,
        'old_cubic_bound_at_r_4_over_5': str(old_bound_control),
        'full_majorisation_proved': False,
        'scope': 'Exact scalar premises/algebra; universal integration and Jensen in PROOF.md',
    }


def main():
    require(sys.argv[1:] in ([], ['--emit']), 'Usage: python3 verify.py [--emit]')
    result = certificate()
    if sys.argv[1:] == ['--emit']:
        print(json.dumps(result, indent=2))
        return
    expected = json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
    require(result == expected, 'Expected certificate mismatch')
    print(json.dumps({'status': 'REPLICA_INTERACTION_PASS',
                      'positive_bernstein_coefficients': result['positive_coefficients'],
                      'bounds': ['b_(9,0)>=sqrt(2)*d2/10',
                                 'b_(12,0)>=13*sqrt(2)*d2/1000'],
                      'unrestricted_hankel_sign_proved': False,
                      'full_majorisation_proved': False}, indent=2))


if __name__ == '__main__':
    main()
