#!/usr/bin/env python3
"""Regenerate the cyclic-core residual with SymPy 1.14.0, no certificate input."""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
from pathlib import Path
import json
import sympy as s


def generate():
    t = s.symbols('t')
    field = s.QQ.frac_field(t)
    zero, one, T = field.zero, field.one, field.from_sympy(t)
    h = [[one if i == j else T for j in range(3)] for i in range(3)]
    a = {0: [one, zero, zero], 5: [zero, one, zero], 11: [zero, zero, one]}
    steps = ((6, 0, 11, 5), (7, 0, 5, 11), (9, 5, 11, 0),
             (12, 5, 7, 0), (13, 11, 9, 5))
    for new, i, j, old in steps:
        a[new] = [2*T/(one+T)*(a[i][k]+a[j][k])-a[old][k] for k in range(3)]
    def dot(x, y):
        return sum((x[i]*h[i][j]*y[j] for i in range(3) for j in range(3)), zero)
    forced = {}
    for new, i, j, old in ((8, 6, 13, 11), (10, 9, 12, 5)):
        w = dot(a[i], a[j])
        forced[new] = [2*T/(one+w)*(x+y)-z for x,y,z in zip(a[i],a[j],a[old])]
    kappa = T*(9*T*T-2*T-3)/(one+T)**2
    residual = field.to_sympy(dot(forced[8],forced[10])-kappa)
    numerator, denominator = s.fraction(s.cancel(residual))
    def coefficients(poly):
        p = s.Poly(poly, t)
        return [int(p.nth(i)) for i in range(p.degree()+1)]
    return {'residual_num': coefficients(numerator), 'residual_den': coefficients(denominator),
            'bad_pair': [1, 9], 'bad_pair_lower': [49, 50]}


if __name__ == '__main__':
    path = Path(__file__).with_name('certificate_cyclic_contact_core.json')
    path.write_text(json.dumps(generate(), sort_keys=True, indent=2)+'\n')
    print('Generated', path.name)
