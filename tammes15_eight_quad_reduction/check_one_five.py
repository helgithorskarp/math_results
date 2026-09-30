#!/usr/bin/env python3
"""Exact angle certificates and necessary cover for ONE_FIVE.md.

CPython >=3.11, standard library. Geometry-to-equations is a written hand
proof. This does not enumerate full contact graphs or formalize geometry.
"""
from copy import deepcopy
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from pathlib import Path
import json
import sys

import check as prior
import check_two_fives as two


def cmul(a, b):
    return a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0]


def derivative(poly, index):
    out = {}
    for e, coef in poly.terms.items():
        if e[index]:
            f = list(e)
            f[index] -= 1
            out[tuple(f)] = coef * e[index]
    return prior.Poly(out)


def polynomials_and_identities():
    c, h, U, V, z = [prior.variable(i) for i in range(5)]
    D, H = 1 + 2*c - c**2, 1 + 2*c
    checked = []

    def identity(poly, name, reduce_h=False):
        if reduce_h:
            poly = prior.reduce_square(poly, 1, H)
        prior.need(not poly.terms, name)
        checked.append(name)

    # Separated-star tangent numerator, cleared by positive denominators.
    A, B = h - c**2*U, h - c**2*V
    E, G = h*U + 1, h*V + 1
    N = h*A*B - c**3*(A*G+B*E) - h*c**4*E*G
    identity(N - (1+c)**3*(h*(1-c)-c**2*(U+V)),
             'separated-star tangent numerator', True)
    R = 1+3*c-2*c**2-9*c**3-c**4
    identity(H*(1-c)*D-c**2*D-2*H*c**3-R, 'separated endpoint gap')
    identity(derivative(R, 0)-(3-4*c-27*c**2-4*c**3), 'R first derivative')
    identity(derivative(derivative(R, 0), 0)-(-4-54*c-12*c**2),
             'R second derivative')

    # Direct complex product for the sum of four half-angles.
    real, imag = prior.Poly(1), prior.Poly()
    for pair in [(prior.Poly(1), V),
                 (c**2*(U+V), 1-c**2*U*V),
                 (c**2*(1+h*V), h-c**2*V), (h, prior.Poly(1))]:
        real, imag = cmul((real, imag), pair)
    imag = prior.reduce_square(imag, 1, H)
    a = h*(1-c)
    denominator, numerator = a+(1+3*c)*V, 1+3*c-a*V
    substituted = prior.Poly()
    for e, coef in imag.terms.items():
        prior.need(e[2] <= 1, 'unexpected U degree')
        f = list(e)
        f[2] = 0
        substituted += prior.Poly({tuple(f): coef}) * (numerator if e[2] else denominator)
    PV = (1-4*c**2-2*c**3-3*c**4 + 2*h*(1-c)*D*V
          + (1+4*c-14*c**3-9*c**4+2*c**5)*V**2
          + 2*c**2*h*(1-c)*D*V**3-2*c**4*(1+3*c)*V**4)
    identity(substituted+(1+c)*PV, 'adjacent complex-product reduction', True)
    cleared = prior.Poly()
    for e, coef in PV.terms.items():
        prior.need(e[3] <= 4 and not e[4], 'V substitution domain')
        f = list(e)
        f[1] += 4-e[3]
        f[4] = e[3]
        f[3] = 0
        cleared += prior.Poly({tuple(f): coef})
    P = (H**2*(1-4*c**2-2*c**3-3*c**4) + 2*(1-c)*D*H**2*z
         + H*(1+4*c-14*c**3-9*c**4+2*c**5)*z**2
         + 2*c**2*(1-c)*D*H*z**3-2*c**4*(1+3*c)*z**4)
    identity(cleared-P, 'adjacent radical elimination z=hV', True)
    identity(3*D-4*c*H-(3+2*c-11*c**2), 'rectangle upper bound')

    # Seventh half-angle multiple used in y+alpha+2x>2pi.
    real, imag = prior.Poly(1), prior.Poly()
    for _ in range(7):
        real, imag = cmul((real, imag), (h, prior.Poly(1)))
    f7, g7 = H**3-21*H**2+35*H-7, 7*H**3-35*H**2+21*H-1
    identity(real-h*f7, 'seventh multiple real part', True)
    identity(imag-g7, 'seventh multiple imaginary part', True)
    J = -1-c+10*c**2+2*c**3-25*c**4+15*c**5
    identity(D*f7-2*c**2*g7+8*J, 'large-corner tangent comparison')
    return P, J, checked


def basis(n, i, normalized_variable):
    return comb(n, i) * normalized_variable**i * (1-normalized_variable)**(n-i)


def certificate_checks(certificate):
    prior.need(set(certificate) == {'schema', 'c_interval', 'z_interval',
               'adjacent_P_degree', 'adjacent_P_bernstein', 'large_corner_J_degree',
               'large_corner_J_bernstein'}, 'certificate schema fields')
    prior.need(certificate['schema'] == 1 and certificate['c_interval'] == ['1/2', '3/5']
               and certificate['z_interval'] == ['1', '3/2'], 'certificate intervals')
    prior.need(certificate['adjacent_P_degree'] == [6, 4]
               and certificate['large_corner_J_degree'] == 5, 'certificate degrees')
    rows, line = certificate['adjacent_P_bernstein'], certificate['large_corner_J_bernstein']
    prior.need(isinstance(rows, list) and len(rows) == 7
               and all(isinstance(r, list) and len(r) == 5 for r in rows), 'P table dimensions')
    prior.need(isinstance(line, list) and len(line) == 6, 'J table dimensions')
    prior.need(all(type(v) is str for row in rows for v in row)
               and all(type(v) is str for v in line), 'rational entries must be strings')
    table, vector = [[F(v) for v in row] for row in rows], [F(v) for v in line]
    prior.need(all(v > 0 for row in table for v in row) and all(v > 0 for v in vector),
               'nonpositive Bernstein coefficient')
    P, J, identities = polynomials_and_identities()
    c, z = prior.variable(0), prior.variable(4)
    C, Z = 10*c-5, 2*z-2
    reconstructed = prior.Poly()
    for i, row in enumerate(table):
        for j, coef in enumerate(row):
            reconstructed += coef * basis(6, i, C) * basis(4, j, Z)
    prior.need(not (reconstructed-P).terms, 'P Bernstein reconstruction mismatch')
    reconstructed = prior.Poly()
    for i, coef in enumerate(vector):
        reconstructed += coef*basis(5, i, C)
    prior.need(not (reconstructed-J).terms, 'J Bernstein reconstruction mismatch')
    margins = {'separated_R_at_three_fifths': F(4, 625),
               'minus_R_prime_at_one_half': F(25, 4),
               'rectangle_gap_at_three_fifths': F(6, 25),
               'two_large_angles_pi_units': F(1, 12)}
    r = lambda t: 1+3*t-2*t**2-9*t**3-t**4
    rp = lambda t: 3-4*t-27*t**2-4*t**3
    prior.need(r(F(3,5)) == margins['separated_R_at_three_fifths'], 'R endpoint')
    prior.need(-rp(F(1,2)) == margins['minus_R_prime_at_one_half'], 'R derivative endpoint')
    prior.need(3+2*F(3,5)-11*F(3,5)**2 == margins['rectangle_gap_at_three_fifths'],
               'rectangle endpoint')
    prior.need(2*F(2,3)+2*F(3,8)-2 == margins['two_large_angles_pi_units'],
               'two-large-corner endpoint')
    return {'polynomial_identities': identities, 'positive_P_coefficients': 35,
            'minimum_P_coefficient': str(min(v for row in table for v in row)),
            'positive_J_coefficients': 6, 'minimum_J_coefficient': str(min(vector)),
            'strict_rational_margins': {k: str(v) for k, v in sorted(margins.items())}}


def legal(labels, edges):
    return not ('5/1' in labels and '4/2' in labels) and two.legal(labels, edges)


def cover():
    baseline = two.cover()
    rows, profiles = [], []
    for before in baseline['distributions']:
        d41, d42, d51 = before['d41'], before['d42'], before['d51']
        labels = before['vertex_colors']
        pairs = tuple(combinations(range(len(labels)), 2))
        codes, signatures = set(), set()
        for mask in range(1 << len(pairs)):
            edges = frozenset(e for i, e in enumerate(pairs) if (mask >> i) & 1)
            if legal(labels, edges):
                codes.add(prior.code(labels, edges))
                signatures.add(prior.signature(labels, edges))
        allowed = d51 <= 1 and not (d51 and d42)
        independent = prior.component_cover(labels) if allowed else set()
        prior.need(signatures == independent and len(codes) == len(signatures),
                   'independent colored cover mismatch')
        prior.need(sorted(codes) == (before['allowed_H_codes'] if allowed else []),
                   'previous cover comparison')
        for p in baseline['profiles']:
            if (p['d41'], p['d42'], p['d51']) == (d41, d42, d51) and codes:
                profiles.append(p)
        rows.append({'d41': d41, 'd42': d42, 'd51': d51,
                     'allowed_H_codes': sorted(codes),
                     'surviving_degree_profiles': sum(
                         (p['d41'], p['d42'], p['d51']) == (d41, d42, d51)
                         for p in profiles)})
    prior.need(profiles == [p for p in baseline['profiles'] if not (p['d51'] and p['d42'])],
               'entry-level profile comparison')
    prior.need(len(profiles) == 23, 'profile count')
    prior.need(sum(len(row['allowed_H_codes']) for row in rows) == 16, 'type count')
    prior.need(sum(bool(row['allowed_H_codes']) for row in rows) == 4, 'distribution count')
    removed = [p for p in baseline['profiles'] if p['d51'] and p['d42']]
    prior.need(len(removed) == 6 and [p['n3'] for p in removed] == list(range(6)),
               'removed mixed profiles')
    return {'previous_degree_profiles': 29, 'remaining_degree_profiles': 23,
            'previous_colored_H_types': 17, 'remaining_colored_H_types': 16,
            'remaining_deficit_distributions': 4,
            'five_star_restriction': 'Any deficient degree five has adjacent rhombi; not an H-edge-mask condition',
            'removed_profiles': removed, 'distributions': rows, 'profiles': profiles}


def selftest(cert):
    controls = 0
    for field, location in [('adjacent_P_bernstein', (6, 0)), ('large_corner_J_bernstein', (0,))]:
        bad = deepcopy(cert)
        if len(location) == 2:
            i, j = location
            bad[field][i][j] = str(F(bad[field][i][j])+1)
        else:
            i = location[0]
            bad[field][i] = str(F(bad[field][i])+1)
        try:
            certificate_checks(bad)
        except ValueError as exc:
            prior.need('Bernstein reconstruction mismatch' in str(exc), 'wrong corruption rejection')
            controls += 1
        else:
            raise ValueError('corrupted certificate accepted')
    def test(condition, name):
        nonlocal controls
        prior.need(condition, name)
        controls += 1
    centered = prior.normalized_edges(((0,1), (1,2)))
    path = prior.normalized_edges(((0,1), (1,2), (2,3)))
    cycle = prior.normalized_edges(((0,1), (1,2), (2,3), (3,0)))
    mixed = ['4/1', '5/1', '4/2']
    test(two.legal(mixed, centered), 'mixed path survives prior stage')
    test(not legal(mixed, centered), 'mixed path now excluded')
    test(legal(['4/1', '5/1', '4/1', '4/1'], centered), 'one-five centered path retained')
    test(legal(['4/1', '5/1', '4/1', '4/1'], path), 'one-five full path retained')
    test(legal(['5/1', '4/1', '4/1', '4/1'], cycle), 'one-five cycle retained')
    test(legal(['4/1']*4, cycle), 'all-four cycle retained')
    test(legal(['4/2', '4/2'], frozenset()), 'all-four empty graph retained')
    test(len(cover()['profiles']) == 23, 'complete updated cover')
    return controls


def main():
    prior.need(sys.argv[1:] in ([], ['--selftest']), 'usage: check_one_five.py [--selftest]')
    cert = json.loads(Path(__file__).with_name('ANGLE_CERTIFICATE.json').read_text())
    checks = certificate_checks(cert)
    if sys.argv[1:]:
        print(json.dumps({'status': 'PASS', 'controls': selftest(cert),
                          'degree_profiles': 23, 'colored_H_types': 16,
                          'positive_angle_coefficients': 41}, sort_keys=True))
    else:
        print(json.dumps({'agent': 'six-tammes-1', 'role': 'researcher',
                          'scope': 'exact angle certificates and necessary cover; written geometry separate',
                          'angle_checks': checks, 'cover': cover()}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
