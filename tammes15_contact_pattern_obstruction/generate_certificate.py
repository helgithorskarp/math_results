#!/usr/bin/env python3
"""Propose the exact tables using SymPy 1.14.0; verify.py checks them independently."""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
from pathlib import Path
import json
import sympy as s
from sympy.polys.matrices import DomainMatrix as DM
from verify import model

t = s.symbols('t')
K = s.QQ.frac_field(t)
zero, one, T = K.zero, K.one, K.from_sympy(t)
H = [[one if i == j else T for j in range(3)] for i in range(3)]
HI = [[(one/(one-T) if i == j else zero)-T/((one-T)*(one+2*T))
       for j in range(3)] for i in range(3)]


def table(rows):
    expressions = [[K.to_sympy(p) for p in row] for row in rows]
    denominator = s.lcm([s.denom(p) for row in expressions for p in row])
    def polynomial(p):
        poly = s.Poly(p, t, domain=s.ZZ)
        return [int(poly.nth(i)) for i in range(poly.degree()+1)] if poly else []
    return {'den': polynomial(denominator),
            'num': [[polynomial(s.cancel(p*denominator)) for p in row]
                    for row in expressions]}


def generate(variant):
    a = {0: [one, zero, zero], 5: [zero, one, zero], 11: [zero, zero, one]}
    b = {1: [one, zero, zero], 2: [zero, one, zero], 4: [zero, zero, one]}
    ap, bp, cross = model(variant)
    q = 2*T/(one+T)
    for group, steps in ((a, ap), (b, bp)):
        for new, i, j, old in steps:
            group[new] = [q*(group[i][k]+group[j][k])-group[old][k] for k in range(3)]
    v = [[a[i][j]*b[k][l] for j in range(3) for l in range(3)] for i, k in cross]
    v0 = DM.from_list([r[:6] for r in v], K)
    rhs = DM.from_list([[T]+[-p for p in r[6:]] for r in v], K)
    u = v0.inv().matmul(rhs).to_list()
    u += [[zero, one, zero, zero], [zero, zero, one, zero], [zero, zero, zero, one]]
    mon = ((0, 0), (0, 1), (0, 2), (0, 3), (1, 1),
           (1, 2), (1, 3), (2, 2), (2, 3), (3, 3))
    e = []
    for i in range(3):
        for j in range(i, 3):
            row = [zero]*10
            for k in range(3):
                for l in range(3):
                    x, y = u[3*k+i], u[3*l+j]
                    for n, (p, q) in enumerate(mon):
                        row[n] += HI[k][l]*(x[p]*y[q]+(x[q]*y[p] if p != q else zero))
            row[0] -= H[i][j]
            e.append(row)
    c = DM.from_list([row[4:] for row in e], K)
    ell = DM.from_list([row[:4] for row in e], K)
    normal = c.inv().matmul(ell).neg().to_list()
    return {'linear': table(u), 'quadratic': table(normal)}


if __name__ == '__main__':
    data = {name: generate(name) for name in ('asymmetric', 'cyclic')}
    path = Path(__file__).with_name('certificate.json')
    path.write_text(json.dumps(data, sort_keys=True, indent=2)+'\n')
    print('Generated', path.name)
