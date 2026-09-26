#!/usr/bin/env python3
"""Exact arithmetic controls for RELATIVE_TAIL.md; no Gaussian integration.

The analytic derivative, fan-wall, and limit arguments remain written
proof obligations. This script verifies their displayed coefficient
arithmetic, the conservative effective-radius fixture, and an exact
fully asymmetric positive-support example for the all-threshold theorem.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from math import factorial
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def geometry():
    vertices = ((0, 0, 0), (2, 0, 0), (1, 3, 0), (1, 1, 4))
    squared_lengths = [sum((x-y)**2 for x, y in zip(vertices[i], vertices[j]))
                       for i, j in combinations(range(4), 2)]
    nu = F(2)
    require(min(squared_lengths) == nu**2, 'minimum vertex separation')
    heights = (F(1), F(2), F(3), F(5))
    pair_coefficients = []
    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            k, ell = [z for z in range(4) if z not in (i, j)]
            delta = min(heights[k], heights[ell])/2
            rho = min(F(1, 4), delta/40)
            pair_coefficients.append(rho**3/(24*5))
    c_geometry = min(pair_coefficients)
    gamma = sum(heights[i]*F(1, 16)*F(1, 4)
                for i in range(4) for j in range(4) if i != j)
    require(c_geometry == F(1, 61440000), 'geometric coefficient from prior tail bound')
    require(gamma == F(33, 64), 'uniform-weight Gamma')
    require(c_geometry*gamma == F(11, 1310720000), 'coefficient before exponential')
    return nu, c_geometry, gamma, squared_lengths


def coefficient_audit():
    # R>=4M implies |r/R-1|<=1/4. These are worst-case endpoint bounds.
    require(2+F(1, 4) == F(9, 4), 'radial square discrepancy constant')
    require(4+2*F(9, 4) == F(17, 2), 'single-radius derivative discrepancy')
    require(F(10)-F(17, 2) > 0 and 10-4 > 0,
            '10(1+x) dominates 17/2+4x for every x>=0')
    per_sign = F(5, 4)**2*2+1
    require(2*per_sign == F(33, 4) <= 10, 'both-sign bound on fan-wall slabs')
    require(4*6 == 24 and 10*24*2 == 480, 'six slab areas and R-M denominator bound')
    require(F(3, 2)+F(1, 8) <= 2, 'absolute offset exponent constant')
    require(F(3, 2)*3 <= 5, 'boundary posterior score bound')

    # Integral_0^infinity u^n exp(-2u/3) du = n! (3/2)^(n+1).
    # This identity is the analytic input; its arithmetic is checked here.
    moments = [F(factorial(n))*F(3, 2)**(n+1) for n in range(3)]
    require(moments == [F(3, 2), F(9, 4), F(27, 4)], 'exterior derivative integral constants')
    require(moments[1]+moments[2] == 9, 'u plus u squared integral')
    exterior = {'D*M': 5*9, 'D*M/R': 2*9, 'D/R': 9+2*moments[0]}
    require(exterior == {'D*M': 45, 'D*M/R': 18, 'D/R': 12}, 'one-ray derivative bound')
    require(45+18*F(1, 2) <= 60 and 12*F(1, 2) <= 60,
            '60D(M+1) exterior bound for R>=2')

    # The common factor pi D/R is removed; W=(c_T+log R)/nu.
    volume = Counter({'M': 80, 'M*D*T': 80, 'constant': 16, 'W': 480})
    mass = Counter({'M': 480, 'constant': 480})
    total = volume+mass
    require(dict(total) == {'M': 560, 'M*D*T': 80, 'constant': 496, 'W': 480},
            'complete error coefficient collection')
    require(F(80, 12) == F(20, 3) and 480*(1+F(4, 12)) == 640,
            'logarithmic-window coefficient A1')
    return {'error_coefficients': dict(total),
            'exterior_integral_moments': list(map(str, moments)),
            'both_sign_wall_constant_before_rounding': str(2*per_sign)}


def power_ten_upper(value):
    """Smallest nonnegative k for which exact positive value <= 10^k."""
    require(value > 0, 'positive radius requirement')
    exponent = max(0, len(str(value.numerator))-len(str(value.denominator)))
    while F(10)**exponent < value:
        exponent += 1
    while exponent and F(10)**(exponent-1) >= value:
        exponent -= 1
    return exponent


def effective_radius_control():
    nu, c_geometry, gamma, squared_lengths = geometry()
    V, D, M = F(5), F(2), F(7)
    w_min = F(1, 4)
    exponent = 3*(2+M**2)
    require(exponent == 153, 'tail exponential constant')

    # Analytic geometric input pi<4; elementary Taylor proofs of 2<e<3
    # imply log4<2 and exp(-153)>3^-153, as explained in the manuscript.
    e_lower = sum(F(1, factorial(n)) for n in range(3))
    e_upper = sum(F(1, factorial(n)) for n in range(5))+F(1, 100)
    require(e_lower > 2 and e_upper < 3, 'Taylor bounds needed for e and log4')
    pi_upper, log_inverse_w_upper = F(4), F(2)
    g_lower = c_geometry*gamma/F(3)**int(exponent)
    A0_upper = 560*M+496+480/nu*(log_inverse_w_upper+V**2/2)
    A1 = F(20, 3)*M+640/nu
    require(A0_upper == 7896 and A1 == F(1100, 3), 'displayed fixture constants')

    requirements = {
        'radial_regularity': max(F(2), 4*M),
        'T_at_most_R': (12*D)**-2,
        'A0_term': (4*pi_upper*D*A0_upper/g_lower)**2,
        'A1_term': (8*pi_upper*D*A1/g_lower)**4,
    }
    radius = 10**400
    require(all(radius >= bound for bound in requirements.values()),
            '10^400 satisfies every effective growing-window condition')
    smaller_trial = 10**40
    require(any(smaller_trial < bound for bound in requirements.values()),
            'small-radius control must fail the sufficient test')
    # Failure of this test is NOT a negative hinge, merely a missing certificate.
    cutoff_c = F(1, 100)/D**2
    require(cutoff_c == F(1, 400) and 72*D**2*cutoff_c < 1,
            'admissible complete threshold-interval coefficient')
    return {'V': str(V), 'D': str(D), 'M': str(M), 'nu': str(nu),
            'w_min': str(w_min), 'Gamma': str(gamma), 'c_geometry': str(c_geometry),
            'squared_vertex_distances': squared_lengths,
            'g0_lower_bound': '11/(1310720000*3^153)',
            'A0_upper': str(A0_upper), 'A1': str(A1),
            'radius_sufficient': '10^400', 'logarithmic_window_divisor': str(12*D),
            'requirement_power_ten_upper_exponents': {k: power_ten_upper(v) for k, v in requirements.items()},
            'radius_10_pow_40_fails_sufficient_test': True,
            'threshold_cutoff_c': str(cutoff_c),
            'sufficient_test_failure_is_not_a_counterexample': True}


def positive_support_control():
    """A fully asymmetric rational member of the all-threshold class."""
    regular = tuple(tuple(map(F, v)) for v in
                    ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)))

    def dot(a, b):
        return sum(x*y for x, y in zip(a, b))

    def sub(a, b):
        return tuple(x-y for x, y in zip(a, b))

    def matvec(a, x):
        return tuple(dot(row, x) for row in a)

    # With x=z+v+u and y=z+v, the two regular-cone branches in (31)
    # have the following coefficients in the nonnegative variables z,v,u.
    x, y, z = (1, 1, 1), (1, 1, 0), (1, 0, 0)
    total = tuple(a+b+c for a, b, c in zip(x, y, z))
    branch_one = tuple(4*a-2*b+4*c for a, b, c in zip(x, total, z))
    branch_two = tuple(4*a-b for a, b in zip(x, total))
    require(branch_one == (2, 0, 2) and branch_two == (1, 2, 3),
            'universal regular normal-cone sign coefficients')
    require(all(dot(a, b) == (3 if i == j else -1)
                for i, a in enumerate(regular) for j, b in enumerate(regular)),
            'regular normal Gram identities')
    cap_radius = F(1, 12)
    require(6*cap_radius == F(1, 2), 'support Lipschitz cap loss')
    require(8*cap_radius**2 < F(16, 3), 'cap remains inside its fan cell')
    require(2*cap_radius**2 == F(1, 72), 'four-cap integral coefficient of pi/sqrt3')
    require(8+24*10 == 248, 'perturbation error coefficient')

    delta = F(1, 10**8)
    eta = 13*delta
    B = ((0, 1, 0), (0, 1, 1), (1, 0, 2))
    A = tuple(tuple(F(i == j)+delta*B[i][j] for j in range(3)) for i in range(3))
    require(sum(x*x for row in B for x in row) == 8 < 9, 'operator perturbation bound')
    require(delta <= F(1, 39) and 12/(1-3*delta) <= 13, 'normal perturbation bound')
    require(eta < F(1, 35712), 'open positive-support neighborhood')
    geometric_lower = 3*(F(1, 144)-248*eta)
    require(geometric_lower > F(1, 50), 'strict rational support coefficient lower bound')

    # Explicit cofactor inverse, checked independently by multiplying A inverse.
    cofactors = []
    for i in range(3):
        row = []
        for j in range(3):
            rows = [k for k in range(3) if k != i]
            cols = [k for k in range(3) if k != j]
            minor = A[rows[0]][cols[0]]*A[rows[1]][cols[1]]-A[rows[0]][cols[1]]*A[rows[1]][cols[0]]
            row.append((-1)**(i+j)*minor)
        cofactors.append(row)
    determinant = sum(A[0][j]*cofactors[0][j] for j in range(3))
    require(determinant == 1+3*delta+2*delta**2+delta**3 > 0, 'invertible perturbation')
    inverse = tuple(tuple(cofactors[j][i]/determinant for j in range(3)) for i in range(3))
    require(all(sum(A[i][k]*inverse[k][j] for k in range(3)) == (i == j)
                for i in range(3) for j in range(3)), 'inverse matrix multiplication')
    inverse_transpose = tuple(zip(*inverse))
    vertices = tuple(matvec(A, v) for v in regular)
    heights = tuple(4*(1+i*delta) for i in range(4))
    normals = tuple(tuple((1+i*delta)*x for x in matvec(inverse_transpose, v))
                    for i, v in enumerate(regular))
    for i in range(4):
        require(dot(sub(vertices[i], regular[i]), sub(vertices[i], regular[i])) <= eta**2,
                'exact vertex perturbation norm')
        require(dot(sub(normals[i], regular[i]), sub(normals[i], regular[i])) <= eta**2,
                'exact normal perturbation norm')
        require(dot(vertices[i], vertices[i]) < 4 and dot(normals[i], normals[i]) < 4,
                'convenient V=D=2 bounds')
        for k in range(4):
            for j in range(4):
                require(dot(normals[i], sub(vertices[k], vertices[j])) ==
                        heights[i]*((k == i)-(j == i)), 'perturbed normal-edge identity')

    expected = [(8, 32, 36), (8, 24, 40), (8, 16, 12),
                (8, 0, 12), (8, 8, 8), (8, 16, 20)]
    polynomials, lengths = [], []
    for i, j in combinations(range(4), 2):
        edge = sub(regular[i], regular[j]); change = matvec(B, edge)
        coefficients = (dot(edge, edge), 2*dot(edge, change), dot(change, change))
        value = coefficients[0]+coefficients[1]*delta+coefficients[2]*delta**2
        require(value == dot(sub(vertices[i], vertices[j]), sub(vertices[i], vertices[j])),
                'full squared-distance polynomial')
        polynomials.append(tuple(int(x) for x in coefficients)); lengths.append(value)
    require(polynomials == expected and len(set(lengths)) == 6,
            'six distinct edge lengths; no nonidentity core symmetry')
    require(min(lengths) > 4 and max(lengths) < 9, 'edge bounds 2<length<3')

    labels = [('core', i, i) for i in range(4)] + [
        ('flap', i, j) for i in range(4) for j in range(4) if i != j]
    weights = tuple(F(i+1, 136) for i in range(16))
    require(sum(weights) == 1 and min(weights) > 0, 'asymmetric positive probability law')
    w = [sum(p for p, (_, _, tip) in zip(weights, labels) if tip == j) for j in range(4)]
    gamma = sum(heights[i]*p*w[i] for p, (typ, i, j) in zip(weights, labels) if typ == 'flap')
    require(gamma > 0, 'positive contraction loss')
    return {'regular_cone_branch_coefficients': [list(branch_one), list(branch_two)],
            'regular_lower_bound': 'pi/(72 sqrt(3))',
            'delta': str(delta), 'eta': str(eta),
            'matrix_A': [[str(x) for x in row] for row in A],
            'normal_edge_identities': 64,
            'squared_edge_polynomials': [list(x) for x in polynomials],
            'distinct_core_edge_lengths': len(set(lengths)),
            'support_coefficient_strict_lower_bound': '1/50',
            'weights': '(1,2,...,16)/136 in the order of verify.py',
            'Gamma_for_displayed_weights': str(gamma),
            'claim': 'All hinges at every fixed variance for sufficiently small depth; depth depends on weights and variance'}


def run():
    return {'scope': 'Exact coefficient and effectivity controls; the analytic proof is RELATIVE_TAIL.md',
            'coefficient_audit': coefficient_audit(),
            'effective_asymmetric_fixture': effective_radius_control(),
            'all_threshold_asymmetric_control': positive_support_control()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare with RELATIVE_EXPECTED.json')
    args = parser.parse_args()
    result = run()
    canonical = (json.dumps(result, indent=2, sort_keys=True)+'\n').encode()
    if args.check:
        expected = Path(__file__).with_name('RELATIVE_EXPECTED.json').read_bytes()
        require(canonical == expected, 'RELATIVE_EXPECTED.json mismatch')
        print('PASS: radial, posterior, angular and exterior coefficient arithmetic')
        print('PASS: explicit asymmetric growing-window radius and insufficient-radius control')
        print('PASS: positive support coefficient; fully asymmetric rational all-threshold control')
        print('RELATIVE_EXPECTED.json sha256', hashlib.sha256(canonical).hexdigest())
    else:
        print(canonical.decode(), end='')


if __name__ == '__main__':
    main()
