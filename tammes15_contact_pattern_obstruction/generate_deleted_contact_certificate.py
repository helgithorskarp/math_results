#!/usr/bin/env python3
"""Generate the 29-contact rational tables with SymPy 1.14.0.

The independent standard-library checker verifies every proposed identity.
"""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
from itertools import combinations_with_replacement
from pathlib import Path
import json
import sympy as s
from sympy.polys.matrices import DomainMatrix as DM
from verify import model


def generate():
    t = s.symbols('t')
    k = s.QQ.frac_field(t)
    zero, one, T = k.zero, k.one, k.from_sympy(t)
    h = [[one if i == j else T for j in range(3)] for i in range(3)]
    hi = [[(one/(one-T) if i == j else zero)-T/((one-T)*(one+2*T))
           for j in range(3)] for i in range(3)]
    a = {0: [one, zero, zero], 5: [zero, one, zero], 11: [zero, zero, one]}
    b = {1: [one, zero, zero], 2: [zero, one, zero], 4: [zero, zero, one]}
    ap, bp, cross = model('asymmetric')
    for group, steps in ((a, ap), (b, bp)):
        for new, i, j, old in steps:
            group[new] = [2*T/(one+T)*(group[i][j0]+group[j][j0])-group[old][j0]
                          for j0 in range(3)]
    cross = [edge for edge in cross if edge != (7, 3)]
    v = [[a[i][j]*b[q][ell] for j in range(3) for ell in range(3)] for i, q in cross]
    pivot, free = (1, 2, 3, 4, 5), (0, 6, 7, 8)
    v0 = DM.from_list([[row[j] for j in pivot] for row in v], k)
    rhs = DM.from_list([[T]+[-row[j] for j in free] for row in v], k)
    u = [[zero]*5 for _ in range(9)]
    for j, row in zip(pivot, v0.inv().matmul(rhs).to_list()):
        u[j] = row
    for i, j in enumerate(free):
        u[j] = [zero]+[one if ell == i else zero for ell in range(4)]
    quad = tuple(combinations_with_replacement(range(1, 5), 2))
    mon = ((0, 0),) + tuple((0, i) for i in range(1, 5)) + quad
    equations = []
    for side in ('columns', 'rows'):
        for i in range(3):
            for j in range(i, 3):
                row = [zero]*15
                for q in range(3):
                    for ell in range(3):
                        x, y = ((u[3*q+i], u[3*ell+j]) if side == 'columns'
                                else (u[3*i+q], u[3*j+ell]))
                        for n, (p, r) in enumerate(mon):
                            row[n] += hi[q][ell]*(x[p]*y[r]+(x[r]*y[p] if p != r else zero))
                row[0] -= h[i][j]
                equations.append(row)
    c = DM.from_list([row[5:] for row in equations[:10]], k)
    normal = c.inv().matmul(DM.from_list([row[:5] for row in equations[:10]], k)).neg().to_list()
    def compact(rows):
        denominator = one.denom
        for row in rows:
            for p in row:
                denominator = denominator.lcm(p.denom)
        nums = [[p.numer*denominator.exquo(p.denom) for p in row] for row in rows]
        polys = [denominator]+[p for row in nums for p in row]
        multiplier = s.ilcm(*[int(c.denominator) for p in polys for c in p.values()])
        def coefficients(p):
            return [int(multiplier*p.get((i,), s.QQ.zero)) for i in range(p.degree()+1)] if p else []
        return {'den': coefficients(denominator),
                'num': [[coefficients(p) for p in row] for row in nums]}
    return {'linear': compact(u), 'quadratic': compact(normal)}


if __name__ == '__main__':
    path = Path(__file__).with_name('certificate_deleted_contact.json')
    path.write_text(json.dumps(generate(), sort_keys=True, indent=2)+'\n')
    print('Generated', path.name)
