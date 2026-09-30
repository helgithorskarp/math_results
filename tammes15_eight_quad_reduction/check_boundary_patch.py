#!/usr/bin/env python3
"""Exact angle certificates and necessary cover for FIVE_BOUNDARY.md.

Geometry-to-equations remains an explicit unformalized hand proof.
CPython >=3.11, standard library; no full contact-graph enumeration.
"""
from copy import deepcopy
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import sys

import check as prior
import check_one_five as one


def eliminate(poly, expected_powers):
    """Substitute U=(1+3c-h(1-c)V)/L, then V=z/h, h^2=1+2c.

    Returns L^m h^n times the original rational expression exactly.
    Every clearing factor is positive in the written angle domain.
    """
    c, h, U, V, z = [prior.variable(i) for i in range(5)]
    H = 1+2*c
    poly = prior.reduce_square(poly, 1, H)
    m = max(e[2] for e in poly.terms)
    L, numerator = h*(1-c)+(1+3*c)*V, 1+3*c-h*(1-c)*V
    substituted = prior.Poly()
    for e, a in poly.terms.items():
        prior.need(len(e)==prior.NV and not e[4] and not e[5], 'unexpected variables')
        f = list(e)
        f[2] = 0
        substituted += prior.Poly({tuple(f):a})*numerator**e[2]*L**(m-e[2])
    substituted = prior.reduce_square(substituted, 1, H)
    n = max(e[3] for e in substituted.terms)
    prior.need((m,n)==expected_powers, 'substitution clearing powers')
    cleared = prior.Poly()
    for e, a in substituted.terms.items():
        f = list(e)
        f[1] += n-e[3]
        f[4], f[3] = e[3], 0
        cleared += prior.Poly({tuple(f):a})
    cleared = prior.reduce_square(cleared, 1, H)
    prior.need(all(not any(e[i] for i in (1,2,3,5)) for e in cleared.terms),
               'radical or unexpected variable remains')
    return cleared


def derived_polynomials():
    c, h, U, V, z = [prior.variable(i) for i in range(5)]
    H = 1+2*c
    A, B = c**2*(U+V), 1-c**2*U*V
    cube = one.cmul(one.cmul((h,prior.Poly(1)), (h,prior.Poly(1))),
                    (h,prior.Poly(1)))
    for actual, expected in zip(cube, (h*(H-3), 3*H-1)):
        prior.need(not prior.reduce_square(actual-expected,1,H).terms,
                   'third-multiple identity')
    real, imag = one.cmul(cube, (prior.Poly(1), -U))
    R = eliminate(A*imag-B*real, (2,3))

    Fu = one.cmul(one.cmul((h,prior.Poly(1)), (prior.Poly(1),U)), (A,B))
    Fv = one.cmul(one.cmul((h,prior.Poly(1)), (prior.Poly(1),V)), (A,B))
    product = (prior.Poly(1), prior.Poly())
    for factor in [(B,c*(U+V)), (c*Fu[1],-Fu[0]), (c*Fv[1],-Fv[0]),
                   (h,prior.Poly(1))]:
        product = one.cmul(product, factor)
    # A second derivation uses symmetric tangent addition, without cmul.
    p, q = U+V, U*V
    r, s = h*A-B, h*B+A
    pair_real = (1-c**2*q)*r**2+(q-c**2)*s**2-(1+c**2)*p*r*s
    pair_cross = 2*(1-q)*r*s+p*(r**2-s**2)
    alternative = (B+h*c*p)*pair_real+c*(h*B-c*p)*pair_cross
    prior.need(not prior.reduce_square(alternative+product[1],1,H).terms,
               'symmetric tangent numerator mismatch')
    closing = eliminate(-product[1], (4,8))
    return R, closing


def certificate_checks(cert):
    fields = {'schema','c_interval','z_interval','small_corner_R_degree',
              'small_corner_R_bernstein','closing_S_degree','closing_S_bernstein'}
    prior.need(set(cert)==fields, 'certificate fields')
    prior.need(type(cert['schema']) is int and cert['schema']==1
               and cert['c_interval']==['1/2','3/5']
               and cert['z_interval']==['1','3/2'], 'certificate intervals/schema')
    c,z = prior.variable(0),prior.variable(4)
    C,Z = 10*c-5,2*z-2
    reconstructed, minima = {}, {}
    for name, degree in [('small_corner_R',[7,3]),('closing_S',[13,8])]:
        prior.need(cert[name+'_degree']==degree, 'certificate degree')
        rows = cert[name+'_bernstein']
        prior.need(isinstance(rows,list) and len(rows)==degree[0]+1
                   and all(isinstance(row,list) and len(row)==degree[1]+1 for row in rows),
                   'coefficient table dimensions')
        prior.need(all(type(v) is str for row in rows for v in row), 'rational string required')
        table = [[F(v) for v in row] for row in rows]
        prior.need(all(v>0 for row in table for v in row), 'nonpositive Bernstein coefficient')
        polynomial = prior.Poly()
        for i,row in enumerate(table):
            for j,a in enumerate(row):
                polynomial += a*one.basis(degree[0],i,C)*one.basis(degree[1],j,Z)
        reconstructed[name] = polynomial
        minima[name] = str(min(v for row in table for v in row))
    R, closing = derived_polynomials()
    prior.need(not (reconstructed['small_corner_R']-R).terms,
               'R Bernstein reconstruction mismatch')
    prior.need(not ((1+c)**3*reconstructed['closing_S']-closing).terms,
               'S Bernstein reconstruction mismatch')
    return {'polynomial_identities':['third multiple real part','third multiple imaginary part',
                                    'small-corner product reduction L^2 h^3',
                                    'symmetric tangent numerator equals minus imaginary part',
                                    'closing product reduction L^4 h^8'],
            'positive_R_coefficients':32,'positive_S_coefficients':126,
            'minimum_R_coefficient':minima['small_corner_R'],
            'minimum_S_coefficient':minima['closing_S'],
            'closing_positive_factor':'(1+c)^3'}


def legal(labels, edges):
    return '5/1' not in labels and one.legal(labels,edges)


def cover():
    baseline = one.cover()
    rows, profiles = [], []
    for before in baseline['distributions']:
        d41,d42,d51 = before['d41'],before['d42'],before['d51']
        labels = ['4/1']*d41+['4/2']*d42+['5/1']*d51
        pairs = tuple(combinations(range(len(labels)),2))
        codes, signatures = set(),set()
        for mask in range(1<<len(pairs)):
            edges = frozenset(e for i,e in enumerate(pairs) if (mask>>i)&1)
            if legal(labels,edges):
                codes.add(prior.code(labels,edges))
                signatures.add(prior.signature(labels,edges))
        independent = prior.component_cover(labels) if d51==0 else set()
        prior.need(signatures==independent and len(codes)==len(signatures),
                   'independent colored cover mismatch')
        prior.need(sorted(codes)==(before['allowed_H_codes'] if d51==0 else []),
                   'entry-level prior cover comparison')
        added = [p for p in baseline['profiles']
                 if (p['d41'],p['d42'],p['d51'])==(d41,d42,d51) and codes]
        profiles.extend(added)
        rows.append({'d41':d41,'d42':d42,'d51':d51,
                     'allowed_H_codes':sorted(codes),'surviving_degree_profiles':len(added)})
    prior.need(profiles==[p for p in baseline['profiles'] if p['d51']==0],
               'entry-level degree profiles mismatch')
    prior.need(len(profiles)==17 and sum(len(r['allowed_H_codes']) for r in rows)==13
               and sum(bool(r['allowed_H_codes']) for r in rows)==3, 'cover totals')
    removed = [p for p in baseline['profiles'] if p['d51']]
    prior.need(len(removed)==6 and [p['n3'] for p in removed]==list(range(6)),
               'removed one-five profiles')
    return {'previous_degree_profiles':23,'remaining_degree_profiles':17,
            'previous_colored_H_types':16,'remaining_colored_H_types':13,
            'remaining_deficit_distributions':3,
            'restriction':'Every degree five is ordinary: four triangles and one quadrilateral',
            'removed_profiles':removed,'distributions':rows,'profiles':profiles}


def selftest(cert):
    controls = 0
    for name,message in [('small_corner_R','R'),('closing_S','S')]:
        bad = deepcopy(cert)
        bad[name+'_bernstein'][0][0] = str(F(bad[name+'_bernstein'][0][0])+1)
        try:
            certificate_checks(bad)
        except ValueError as exc:
            prior.need(message+' Bernstein reconstruction mismatch' in str(exc),
                       'wrong polynomial corruption rejection')
            controls += 1
        else:
            raise ValueError('corrupted positive coefficient accepted')
    def test(condition,message):
        nonlocal controls
        prior.need(condition,message)
        controls += 1
    labels = ['4/1','5/1','4/1','4/1']
    for edges in [((0,1),(1,2)),((0,1),(1,2),(2,3)),
                  ((0,1),(1,2),(2,3),(3,0))]:
        graph = prior.normalized_edges(edges)
        test(one.legal(labels,graph), 'one-five type survives prior stage')
        test(not legal(labels,graph), 'one-five type now excluded')
    test(legal(['4/1']*4,prior.normalized_edges(((0,1),(1,2),(2,3),(3,0)))),
         'all-four cycle retained')
    test(legal(['4/2','4/2'],frozenset()), 'all-four empty graph retained')
    test(legal(['4/1','4/1','4/2'],prior.normalized_edges(((0,2),(1,2)))),
         'mixed all-four path retained')
    test(len(cover()['profiles'])==17, 'complete updated cover')
    return controls


def main():
    prior.need(sys.argv[1:] in ([],['--selftest']), 'usage: check_boundary_patch.py [--selftest]')
    cert = json.loads(Path(__file__).with_name('BOUNDARY_CERTIFICATE.json').read_text())
    checks = certificate_checks(cert)
    if sys.argv[1:]:
        print(json.dumps({'status':'PASS','controls':selftest(cert),
                          'degree_profiles':17,'colored_H_types':13,
                          'positive_angle_coefficients':158},sort_keys=True))
    else:
        print(json.dumps({'agent':'six-tammes-1','role':'researcher',
                          'scope':'exact angle certificates and necessary cover; written geometry separate',
                          'angle_checks':checks,'cover':cover()},indent=2,sort_keys=True))


if __name__=='__main__': main()
