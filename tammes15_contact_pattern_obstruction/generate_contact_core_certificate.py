#!/usr/bin/env python3
"""Regenerate the four contact-core factors with SymPy 1.14.0.

This generator uses invariant Gram entries. The separate standard-library
checker instead builds the coefficient vector C and computes all dot products.
No proposed certificate coefficients are inputs to this generator.
"""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
from pathlib import Path
import json
import sympy as s
from sympy.polys.matrices import DomainMatrix


def generate():
    t = s.symbols('t')
    field = s.QQ.frac_field(t)
    zero, one, T = field.zero, field.one, field.from_sympy(t)
    h = [[one if i == j else T for j in range(3)] for i in range(3)]
    a = {0: [one, zero, zero], 5: [zero, one, zero], 11: [zero, zero, one]}
    b = {1: [one, zero, zero], 2: [zero, one, zero], 4: [zero, zero, one]}
    a_steps = ((6, 0, 11, 5), (7, 0, 5, 11), (9, 5, 11, 0))
    b_steps = ((8, 2, 4, 1), (10, 1, 2, 4), (12, 1, 10, 2), (13, 2, 8, 4))
    for group, steps in ((a, a_steps), (b, b_steps)):
        for new, i, j, old in steps:
            group[new] = [2*T/(one+T)*(group[i][k]+group[j][k])-group[old][k]
                          for k in range(3)]
    def dot(x, y):
        return sum((x[i]*h[i][j]*y[j] for i in range(3) for j in range(3)), zero)
    def ordinary(x, y):
        return sum((p*q for p, q in zip(x, y)), zero)
    def cross(x, y):
        return [x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2], x[0]*y[1]-x[1]*y[0]]
    kappa = dot(a[6], a[7])
    if any(dot(a[i], a[j]) != kappa for i, j in ((6, 9), (7, 9))):
        raise ValueError('Reflected triangle mismatch')
    w = dot(b[10], b[13])
    v = [2*T/(one+w)*(x+y)-z for x, y, z in zip(b[10], b[13], b[2])]
    gamma = kappa/(one+kappa)
    q2 = (one+2*kappa)/(one+kappa)**2
    mu0 = (T-one)*(T+one)*(2*T+one)*(3*T-one)/(9*T**3-T*T-T+one)
    if mu0**2 != (one-T)**2*(one+2*T)*q2:
        raise ValueError('Orientation square mismatch')
    m8, m12, d812 = dot(v, b[8]), dot(v, b[12]), dot(b[8], b[12])
    triple = ordinary(b[8], cross(b[12], v))
    incumbent = s.Poly(13*t**5-t**4+6*t**3+2*t**2-3*t-1, t)
    result = {}
    for sign in (-1, 1):
        mixed = gamma*d812+sign*mu0*triple
        contact = T-gamma*m12
        gram = [[one, m8, gamma*m12, kappa],
                [m8, one, mixed, T],
                [gamma*m12, mixed, one-q2*m12*m12, contact],
                [kappa, T, contact, one]]
        determinant = DomainMatrix.from_list(gram, field).det()
        numerator = s.Poly(s.fraction(s.cancel(field.to_sympy(determinant)))[0], t)
        for factor, multiplicity in s.factor_list(numerator)[1]:
            factor = factor.clear_denoms()[1].primitive()[1]
            if factor.LC() < 0:
                factor = -factor
            degree = factor.degree()
            if factor == incumbent or degree not in ((6, 15) if sign == -1 else (5, 14)):
                continue
            name = 'P'+str(degree)
            if multiplicity != 1 or name in result:
                raise ValueError('Unexpected obstruction factor multiplicity')
            result[name] = [int(factor.nth(i)) for i in range(degree+1)]
    if set(result) != {'P5', 'P6', 'P14', 'P15'}:
        raise ValueError('Missing branch factor')
    return result


if __name__ == '__main__':
    path = Path(__file__).with_name('certificate_contact_core.json')
    path.write_text(json.dumps(generate(), sort_keys=True, indent=2)+'\n')
    print('Generated', path.name)
