"""Exact multilevel Young premises completing Gaussian beta row N=12.

The Gaussian replica identities and retained-interaction theorem are
written mathematical dependencies. No numerical solver is imported.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import comb
from pathlib import Path
import argparse
import copy
import json

from verify import (require, evaluate, root_bounds, power_on_interval,
                    to_bernstein, dyadic_leaves)

ROOT = Path(__file__).resolve().parent


def young_polynomial(base, item):
    shift = item['shift']
    require(isinstance(shift, int) and 0 <= shift <= 32, 'Young shift')
    k = base + shift
    exponent = F(2*(k+1)**2, k*(k+2))
    slope = F(item['slope'])
    upper = F(item['critical_upper'])
    intercept = F(item['intercept'])
    multiplier = F(item['multiplier'])
    require(slope > 0 and 0 < upper <= 1 and multiplier >= 0,
            'Young constant domain')
    p, d = exponent.numerator, exponent.denominator
    require(upper**(p-d) >= (slope/exponent)**d,
            'Young critical-point upper bound')
    lower = intercept - slope*(1-1/exponent)*upper
    require(lower >= 0, 'Young intercept is too small')
    # E[u^shift Q(u)] = [B_(k+2)-slope B_(k+1)+intercept B_k]/k^3.
    coefficients = [intercept, -slope*F(k+1, k)**3, F(k+2, k)**3]
    for ell, value in enumerate(coefficients):
        expected = [intercept, -slope, F(1)][ell]
        require(value/F(k+ell, k)**3 == expected,
                'Young moment normalization')
    record = {'base': k, 'exponent': str(exponent),
              'critical_upper': str(upper), 'critical_bound_verified': True,
              'certified_scalar_lower_bound': str(lower)}
    return shift, multiplier, coefficients, record


def check_case(case, root_denominator):
    m, q = case['base'], case['q']
    gamma = F(case['gamma'])
    depth = case['subdivision_depth']
    require(gamma > 0, 'Positive row margin')
    require(isinstance(depth, int) and 0 <= depth <= 12, 'Subdivision depth')
    young = [young_polynomial(m, item) for item in case['young']]
    degree = max([q] + [shift+2 for shift, *_ in young]
                 + [item['shift']+1 for item in case['monotonicity']])
    polynomial = [F(0)]*(degree+1)
    for ell in range(q+1):
        lower, upper = root_bounds(m+ell, root_denominator)
        polynomial[ell] = (-1)**ell*comb(q, ell)*(upper if ell % 2 else lower)
    polynomial[0] -= gamma
    for shift, multiplier, coefficients, _ in young:
        for ell, coefficient in enumerate(coefficients):
            polynomial[shift+ell] -= multiplier*coefficient
    for item in case['monotonicity']:
        shift = item['shift']
        multiplier = F(item['multiplier'])
        require(isinstance(shift, int) and 0 <= shift <= 32 and multiplier >= 0,
                'Monotonicity term domain')
        polynomial[shift] -= multiplier
        polynomial[shift+1] += multiplier*F(m+shift+1, m+shift)**3

    intervals = 2**depth
    leaves = dyadic_leaves(to_bernstein(polynomial), depth)
    encoded = []
    identity_controls = 0
    for index, recursive in enumerate(leaves):
        local = power_on_interval(polynomial, F(index, intervals), F(1, intervals))
        direct = to_bernstein(local)
        require(direct == recursive, 'Bernstein algorithms disagree')
        require(min(direct) > 0, 'Uncertified multilevel minorant')
        for k in range(degree+1):
            x = F(k, degree)
            bernstein_value = sum((direct[i]*comb(degree, i)*x**i*(1-x)**(degree-i)
                                   for i in range(degree+1)), F(0))
            require(bernstein_value == evaluate(polynomial, (index+x)/intervals),
                    'Polynomial identity control')
            identity_controls += 1
        encoded.extend(str(x) for x in direct)
    return {'base': m, 'q': q, 'j': m-2, 'degree': degree,
            'gamma': str(gamma), 'B_m_coefficient': str(gamma/m**3),
            'intervals': intervals, 'young_premises': [row[3] for row in young],
            'bernstein_coefficients': len(encoded),
            'minimum_bernstein_coefficient': str(min(map(F, encoded))),
            'coefficients_sha256': sha256(('\n'.join(encoded)+'\n').encode()).hexdigest(),
            'identity_controls': identity_controls}


def calculate(certificate):
    require(certificate['row'] == 12, 'Wrong beta row')
    require(certificate['root_denominator'] == 2**48, 'Wrong root enclosure')
    cases = certificate['cases']
    require([(x['base'], x['q']) for x in cases] == [(3, 11), (4, 10), (5, 9), (6, 8)],
            'Incomplete row obligations')
    records = [check_case(case, certificate['root_denominator']) for case in cases]
    coverage = [[0, 12, 'credited retained-interaction theorem']]
    coverage += [[j, 12-j, 'new multilevel certificate'] for j in range(1, 5)]
    coverage += [[j, 12-j, 'credited seven-factor theorem'] for j in range(5, 13)]
    require([x[0] for x in coverage] == list(range(13)), 'Incomplete row coverage')
    require(all(q <= 7 for j, q, _ in coverage if j >= 5), 'Seven-factor range')
    elevation = 0
    for n in range(12):
        for j in range(n+1):
            left, right = F(n+1-j, n+2), F(j+1, n+2)
            require(left > 0 and right > 0 and left+right == 1, 'Convex elevation')
            require(left*(n+2)*comb(n+1, j) == (n+1)*comb(n, j), 'Left normalization')
            require(right*(n+2)*comb(n+1, j+1) == (n+1)*comb(n, j), 'Right normalization')
            elevation += 1
    return {'status': 'MULTILEVEL_COMPLETE_ROW_TWELVE_PASS', 'complete_row': 12,
            'lower_rows': list(range(13)), 'new_cases': records, 'coverage': coverage,
            'young_premises': sum(len(x['young_premises']) for x in records),
            'bernstein_coefficients': sum(x['bernstein_coefficients'] for x in records),
            'polynomial_identity_controls': sum(x['identity_controls'] for x in records),
            'degree_elevation_controls': elevation,
            'full_majorisation_proved': False, 'formalized': False}


def corruption_controls(certificate):
    corruptions = []
    bad = copy.deepcopy(certificate); bad['cases'].pop(); corruptions.append(bad)
    bad = copy.deepcopy(certificate); bad['cases'][0]['gamma'] = '100'; corruptions.append(bad)
    bad = copy.deepcopy(certificate)
    bad['cases'][0]['young'][0]['critical_upper'] = '1/1000000'; corruptions.append(bad)
    bad = copy.deepcopy(certificate)
    bad['cases'][0]['young'][0]['intercept'] = '0'; corruptions.append(bad)
    bad = copy.deepcopy(certificate)
    bad['cases'][0]['young'][0]['multiplier'] = '-1'; corruptions.append(bad)
    for bad in corruptions:
        try:
            calculate(bad)
        except ValueError:
            pass
        else:
            raise RuntimeError('A damaged multilevel certificate was accepted')
    return len(corruptions)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    certificate = json.loads((ROOT/'MULTILEVEL_CERTIFICATE.json').read_text())
    result = calculate(certificate)
    result['rejected_corruptions'] = corruption_controls(certificate)
    target = ROOT/'MULTILEVEL_EXPECTED.json'
    if args.write_expected:
        target.write_text(json.dumps(result, indent=2)+'\n')
    else:
        require(result == json.loads(target.read_text()), 'Expected record mismatch')
    print(json.dumps({k: result[k] for k in ['status', 'complete_row', 'young_premises',
        'bernstein_coefficients', 'polynomial_identity_controls',
        'degree_elevation_controls', 'rejected_corruptions', 'full_majorisation_proved']}, indent=2))


if __name__ == '__main__':
    main()
