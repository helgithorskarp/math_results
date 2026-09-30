#!/usr/bin/env python3
"""Exact finite checks supporting PROOF.md; analytic reductions are written.

Python >= 3.11, standard library only. No numerical roots, solver or CAS.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from math import comb, factorial, isqrt
from pathlib import Path
import argparse
import json

from matching import minimum_cost, partition_cost, partitions

HERE = Path(__file__).resolve().parent
NVAR = 7
NAMES = ('a', 'r1', 'r2', 'x1', 'x2', 'd2', 's')
ZERO = (0,) * NVAR


class Poly:
    """Small exact sparse polynomial for complete algebraic identities."""
    def __init__(self, terms):
        if isinstance(terms, Poly):
            self.terms = terms.terms.copy()
        elif isinstance(terms, dict):
            self.terms = {e: F(c) for e, c in terms.items() if c}
        else:
            self.terms = {ZERO: F(terms)} if terms else {}

    def __add__(self, other):
        other = Poly(other)
        result = self.terms.copy()
        for e, c in other.terms.items():
            result[e] = result.get(e, F(0)) + c
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        other = Poly(other)
        result = {}
        for e, c in self.terms.items():
            for f, d in other.terms.items():
                key = tuple(x + y for x, y in zip(e, f))
                result[key] = result.get(key, F(0)) + c * d
        return Poly(result)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        if not isinstance(exponent, int) or exponent < 0:
            raise ValueError('Only nonnegative integer powers')
        result = Poly(1)
        for _ in range(exponent):
            result = result * self
        return result


def variable(index):
    exponents = list(ZERO)
    exponents[index] = 1
    return Poly({tuple(exponents): F(1)})


def serialization(poly):
    return ''.join(','.join(map(str, e)) + ':' + str(c) + '\n'
                   for e, c in sorted(poly.terms.items())).encode()


def require_identity(lhs, rhs):
    assert not (lhs - rhs).terms, 'Complete polynomial identity failed'


def algebra_checks():
    a, r1, r2, x1, x2, d2, s = map(variable, range(NVAR))
    r = F(1, 2) * (r1 + r2)
    delta = r1 - r2
    g2 = delta**2 + r1*r2*d2
    f1 = (1-a**2)*r1**2 + 2*a*r1*x1 - 1
    f2 = (1-a**2)*r2**2 + 2*a*r2*x2 - 1
    fw = (1-a**2)*r**2 + a*r*(x1+x2) - 1
    norm_product_error = F(1, 16)*delta**4 + r**2*r1*r2*d2
    identities = {
        'disk_preserving_lift':
            (4*r1*r2*fw, 2*r*(r2*f1+r1*f2)+delta**2),
        'real_product_error':
            (r1*r2*(1-F(1, 2)*d2)-r**2,
             -F(1, 2)*g2+F(1, 4)*delta**2),
        'product_error_nonnegative_gap':
            (r**2*g2-norm_product_error,
             F(1, 16)*delta**2*(3*r1**2+10*r1*r2+3*r2**2)),
        'paired_radius_proxy':
            ((1+s*r)**2-(1+s*r1)*(1+s*r2), F(1, 4)*s**2*delta**2),
        'direction_displacement_gap':
            (g2-r**2*d2, (1-F(1, 4)*d2)*delta**2),
    }
    result = {}
    for name, (lhs, rhs) in identities.items():
        require_identity(lhs, rhs)
        result[name] = {'terms': len(lhs.terms),
                        'sha256': sha256(serialization(lhs)).hexdigest()}
    return result, identities


def integral_binomial(n, power, c):
    return sum(F(comb(n, j))*c**j/F(j+power+1) for j in range(n+1))


def integral_substitution(n, power, c):
    # y=1+ct; expansion of (y-1)^power needs only power+1 terms.
    return sum(F(comb(power, j))*(-1)**(power-j)
               *((1+c)**(n+j+1)-1)/F(n+j+1)
               for j in range(power+1))/c**(power+1)


def constants():
    k1 = 9*integral_binomial(7, 1, F(8, 7))
    k2 = 72*integral_binomial(6, 2, F(4, 3))
    assert k1 == 9*integral_substitution(7, 1, F(8, 7))
    assert k2 == 72*integral_substitution(6, 2, F(4, 3))
    assert k1 == F(570801247, 1647086)
    assert k2 == F(9598808, 5103)
    assert k1 < 350 and k2 < 1900 and k1+k2 < 2250
    k1_coeff = [9*F(comb(7, j))*F(8, 7)**j/F(j+2) for j in range(8)]
    k2_coeff = [72*F(comb(6, j))*F(4, 3)**j/F(j+3) for j in range(7)]
    assert all(c > 0 for c in k1_coeff + k2_coeff)
    assert F(9, 32)-F(2250, 9000) == F(1, 32)
    return {'K1_at_one': str(k1), 'K2_at_one': str(k2),
            'sum_at_one': str(k1+k2), 'uniform_upper_bound': 2250,
            'squared_defect_denominator': 9000,
            'retained_margin_coefficient': '1/32',
            'independent_integral_formulas': 2,
            'positive_K1_coefficients': len(k1_coeff),
            'positive_K2_coefficients': len(k2_coeff)}


def square_root_rational(value):
    numerator, denominator = isqrt(value.numerator), isqrt(value.denominator)
    assert numerator**2 == value.numerator and denominator**2 == value.denominator
    return F(numerator, denominator)


def matching_checks():
    all_partitions = tuple(partitions(8))
    counts = Counter(sum(len(g) == 2 for g in p) for p in all_partitions)
    expected = {k: factorial(8)//(2**k*factorial(k)*factorial(8-2*k))
                for k in range(5)}
    assert dict(counts) == expected == {0: 1, 1: 28, 2: 210, 3: 420, 4: 105}
    assert len(set(all_partitions)) == len(all_partitions) == 764
    for p in all_partitions:
        assert sorted(i for g in p for i in g) == list(range(8))
        assert all(len(g) in (1, 2) and tuple(sorted(g)) == g for g in p)
        assert [g[0] for g in p] == sorted(g[0] for g in p)
    # Two deterministic abstract nonnegative rational cost tables.
    tables = []
    for seed in (3, 17):
        singles = [F((seed+7*i*i+5*i)%23, i+1) for i in range(8)]
        pairs = {(i, j): F((seed+3*i*i+11*j+5*i*j)%31, i+j+1)
                 for i in range(8) for j in range(i+1, 8)}
        tables.append((singles, pairs))
    # An exact geometric reciprocal fixture, not an actual polynomial:
    # large individual phases, zero matching defect, feasible disk/budget.
    u, v = (F(7, 25), F(24, 25)), (F(7, 25), F(-24, 25))
    q = [(F(1), F(0))]*2 + [u]*3 + [v]*3
    assert all(x*x+y*y == 1 and F(3, 4)+x-1 >= 0 for x, y in q)
    singles = [square_root_rational((x-1)**2+y*y) for x, y in q]
    pairs = {(i, j): square_root_rational((q[i][0]-q[j][0])**2
                                         +(q[i][1]+q[j][1])**2)
             for i in range(8) for j in range(i+1, 8)}
    assert max(singles) == F(6, 5)
    tables.append((singles, pairs))
    minima = []
    for singles, pairs in tables:
        enumerated = min((partition_cost(p, singles, pairs), p) for p in all_partitions)
        dynamic = minimum_cost(singles, pairs)
        assert dynamic == enumerated
        assert partition_cost(dynamic[1], singles, pairs) == dynamic[0]
        minima.append(str(dynamic[0]))
    assert minima[-1] == '0'
    for n in range(9):
        assert len(tuple(partitions(n))) == sum(factorial(n)//(2**k*factorial(k)
                                              *factorial(n-2*k))
                                             for k in range(n//2+1))
    return {'partitions': 764, 'counts_by_pairs': dict(sorted(counts.items())),
            'cost_tables_checked': len(tables), 'exact_minima': minima,
            'maximum_subset_states': 256,
            'large_phase_fixture_singleton_defect': '6/5'}, all_partitions


def example_checks():
    a, t, eps = F(9, 10), F(99, 100), F(1, 50000)
    d0 = a*a+t*t
    delta0 = 64*a*a-36*t*t
    assert d0 == F(17901, 10000) and delta0 == F(41391, 2500)
    assert F(4)**2 < delta0 < F(5)**2
    assert t+eps < 1 and t-eps >= F(49, 50)
    # All perturbation estimates hold on the larger eps interval [0,1/100].
    eps_max = F(1, 100)
    assert 2*a+eps_max < 2 and d0-2*eps_max > 1
    assert delta0-64*eps_max**2 > 15
    assert F(128, 4) == 32 and F(10+32, 2) == 21
    assert 10*a+5 == 14
    assert F(6)/(a*a) < 8 and 140+8 == 148
    assert (148*eps)**2 < (1-a)/9000
    baseline = a*a+F(49, 50)**2
    assert baseline == F(2213, 1250) and baseline**2 > 3 and baseline**4 > 9
    assert a*a+1 < 2 and F(2)**2 > 2 and 2+a < 3
    angular_lower = 6*F(49, 50)**2/6
    assert angular_lower == F(2401, 2500) > (1-a)/2400
    # Complete derivative and reciprocal substitution identities.
    # Use the existing sparse engine with formal w,A,t,q; no numeric roots.
    w, A, tvar, q = map(variable, range(4))
    h = w**2+tvar**2
    derivative_expanded = h**4 + 8*w*(w-A)*h**3
    derivative_factored = h**3*(9*w**2-8*A*w+tvar**2)
    require_identity(derivative_expanded, derivative_factored)
    # Multiply the w=A-1/q substitution by q^2 before expanding.
    require_identity(9*(A*q-1)**2-8*A*q*(A*q-1)+tvar**2*q**2,
                     (A**2+tvar**2)*q**2-10*A*q+9)
    return {'a': str(a), 't': str(t), 'epsilon': str(eps),
            'matching_defect_upper': str(148*eps),
            'matching_defect_squared_upper': str((148*eps)**2),
            'criterion_squared_bound': str((1-a)/9000),
            'other_root_distance_product_lower': str(baseline**4),
            'angular_loss_lower': str(angular_lower),
            'complete_symbolic_example_identities': 2}


DEPENDENCY_HASHES = {
    'PROOF.md': 'bcd66b92a3c663b320bc96a252cf025a5d491c61478083579a448bd6ebbea24e',
    'verify.py': '245eb19e6764f626ef18957ddea5eea65dfeb2ccbba6f73d31da42e49e89e013',
    'polynomials.py': '0312cb3ab63085caa01ebe82558fcd2965298157ee5dfa1dff25cb6a32ca3a33',
    'expected.json': 'b04d2c3993e8904f107cd4d508b00ab3206fb41422dacd729e2f5db166e8d27f',
}


def dependency_source_checks():
    directory = HERE.parent/'sendov_degree9_real_root_first_power'
    for name, digest in DEPENDENCY_HASHES.items():
        assert sha256((directory/name).read_bytes()).hexdigest() == digest, name
    return {'source_commit': '617624389fad738f3ce930d5afec15787c39c61c',
            'graph_ref': 'bafkreie6w53bbcvsyfhecljn6fvpppkmluk7frumbhpspu2d5qjywb3x3i',
            'sha256': DEPENDENCY_HASHES,
            'scope': 'source identity only; replay input verify.py separately'}


def mutation_checks(identities, all_partitions):
    rejected = 0
    lhs, rhs = identities['disk_preserving_lift']
    try:
        require_identity(lhs+1, rhs)
    except AssertionError:
        rejected += 1
    try:
        assert 72*integral_binomial(6, 2, F(4, 3)) < 1500
    except AssertionError:
        rejected += 1
    try:
        assert len(set(all_partitions[:-1])) == 764
    except AssertionError:
        rejected += 1
    assert rejected == 3
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-expected', action='store_true',
                        help='write compact expected output after all exact assertions')
    args = parser.parse_args()
    algebra, identities = algebra_checks()
    matching, all_partitions = matching_checks()
    result = {'arithmetic': 'fractions.Fraction; Python integers',
              'polynomial_variables': NAMES, 'complete_algebraic_identities': algebra,
              'constants': constants(), 'matching': matching,
              'example': example_checks(), 'dependency': dependency_source_checks(),
              'mutation_rejections': mutation_checks(identities, all_partitions)}
    result = json.loads(json.dumps(result))  # canonical JSON key/tuple representation
    expected = HERE/'expected.json'
    if args.write_expected:
        expected.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    else:
        assert json.loads(expected.read_text()) == result, 'Expected finite output differs'
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
