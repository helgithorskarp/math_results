#!/usr/bin/env python3
"""Exact multiplicity, sign-change, product and affine equality scope controls."""
import argparse
import json
from pathlib import Path
from fractions import Fraction as F


def multiply(p, q):
    result = [F(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            result[i + j] += x*y
    return result


def power(p, n):
    result = [F(1)]
    for _ in range(n):
        result = multiply(result, p)
    return result


def compose(p, q):
    result = [p[-1]]
    for coefficient in reversed(p[:-1]):
        result = multiply(result, q)
        result[0] += coefficient
    return result


def evaluate(p, x):
    result = F(0)
    for coefficient in reversed(p):
        result = result*x + coefficient
    return result


def require(ok, message):
    if not ok:
        raise ValueError(message)


def derive():
    a = F(3, 4)
    w = [a, F(1)]
    polynomial = multiply(multiply([-a, F(1)], power(w, 6)),
                          [F(5, 8), F(3, 2), F(1)])
    derivative = [(i + 1)*c for i, c in enumerate(polynomial[1:])]
    cubic = [F(-9, 16), F(7, 16), F(-12), F(9)]
    proposed = multiply(power(w, 5), compose(cubic, w))
    require(derivative == proposed, "Derivative factorization")
    dd, cc, bb, aa = cubic
    discriminant = bb*bb*cc*cc - 4*aa*cc**3 - 4*bb**3*dd - 27*aa*aa*dd*dd + 18*aa*bb*cc*dd
    require(discriminant == F(-4174875, 1024) < 0, "Critical cubic discriminant")
    require(evaluate(cubic, a) < 0 < evaluate(cubic, 2*a), "Real critical point interval")
    require(evaluate(derivative, 0) < 0 < evaluate(derivative, a), "Sign-change scope")
    require(cubic[0] != 0 and evaluate(polynomial, a) == 0, "Marked/root multiplicities")
    distance_product = (2*a)**6*((2*a)**2 + F(1, 16))
    require(distance_product == F(26973, 1024) > 9, "Outside product criterion")
    require(a*a + F(1, 16) == F(5, 8) < 1, "Complex original roots in disk")
    h, radius = F(3, 5), F(4, 5)
    require(h*h + radius*radius == 1, "Affine chord endpoints in disk")
    affine_sum = 7/(2*radius) + 9/(2*radius)
    require(affine_sum == 8/radius == 10, "Affine equality family")
    return {'scope_example': {'real_critical_multiplicity': 6, 'nonreal_critical_pairs': 1,
                              'cubic_discriminant': str(discriminant),
                              'derivative_at_zero': str(evaluate(derivative, 0)),
                              'derivative_at_marked_root': str(evaluate(derivative, a)),
                              'distance_product': str(distance_product),
                              'nonreal_original_root_radius_squared': '5/8'},
            'affine_equality_example': {'axis_offset': str(h), 'chord_radius': str(radius),
                                        'first_power_sum': str(affine_sum)}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    args = parser.parse_args()
    result = derive()
    require(result == json.loads(args.expected.read_text())['scope_controls'], 'Scope controls differ')
    print(json.dumps(result, indent=2))
