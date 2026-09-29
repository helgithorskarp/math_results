#!/usr/bin/env python3
"""Produce an exact stress and a proposed rational inverse; verify independently."""
import argparse
import json
import os
from pathlib import Path

for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[name] = '1'

import numpy as np
from scipy.linalg import qr
import sympy as s
from sympy.polys.matrices import DomainMatrix


def generate():
    t = s.symbols('t')
    F = 13*t**5-t**4+6*t**3+2*t**2-3*t-1
    K = s.QQ.algebraic_field((s.Poly(F, t), s.Symbol('a')))

    def reduce(e):
        numerator, denominator = s.fraction(s.cancel(e))
        return s.rem(numerator*s.invert(denominator, F, t), F, t)

    def into_field(e):
        value = K.zero
        for (exp,), coefficient in s.Poly(e, t).terms():
            value += K.convert(coefficient)*K.unit**exp
        return value

    def from_field(e):
        return K.to_sympy(e).subs(K.ext.as_expr(), t)

    def coefficients(e):
        return [str(s.Poly(e, t).nth(i)) for i in range(5)]

    H = (1-t)*s.eye(3)+t*s.ones(3)
    a = (117*t**4-48*t**3+70*t**2-6*t-27)/2
    b = (195*t**4-106*t**3+136*t**2-38*t-31)/4
    c = (-429*t**4+202*t**3-276*t**2+42*t+81)/4
    M = s.Matrix([[a, b, c], [c, a, b], [b, c, a]])
    C = (H.inv()*M).applyfunc(reduce)
    V = {0:s.eye(3)[:,0], 5:s.eye(3)[:,1], 11:s.eye(3)[:,2],
         1:C[:,0], 2:C[:,1], 4:C[:,2]}
    steps = ((6,0,11,5), (7,0,5,11), (9,5,11,0), (14,0,6,11),
             (3,1,4,2), (8,2,4,1), (10,1,2,4), (12,1,10,2), (13,2,8,4))
    for new, i, j, old in steps:
        V[new] = (2*t/(1+t)*(V[i]+V[j])-V[old]).applyfunc(reduce)
    G = s.Matrix(15, 15, lambda i,j:reduce((V[i].T*H*V[j])[0]))
    edges = [(i,j) for i in range(15) for j in range(i+1,15) if G[i,j] == t]
    if len(edges) != 30:
        raise ValueError('unexpected contact graph')
    E = s.zeros(45, 30)
    for k, (i,j) in enumerate(edges):
        E[3*i:3*i+3,k] = (V[j]-t*V[i]).applyfunc(reduce)
        E[3*j:3*j+3,k] = (V[i]-t*V[j]).applyfunc(reduce)
    rows = [[into_field(E[i,j]) for j in range(30)] for i in range(45)]
    basis = DomainMatrix(rows, (45,30), K).nullspace().to_list()
    if len(basis) != 3:
        raise ValueError('unexpected stress dimension')
    # A numerical LP suggested that these three contact weights should be one.
    pick = (4,9,13)
    small = DomainMatrix([[basis[j][pick[i]] for j in range(3)] for i in range(3)], (3,3), K)
    factors = small.inv().matmul(DomainMatrix([[K.one]]*3, (3,1), K)).to_list()
    stress = [sum((factors[j][0]*basis[j][i] for j in range(3)), K.zero) for i in range(30)]
    result = {'vectors':[[coefficients(v) for v in V[i]] for i in range(15)],
              'weights':[coefficients(from_field(w)) for w in stress], 'edges':[list(e) for e in edges]}
    # Numerical steps below propose a certificate, never a proof.
    tn = 0.5926059029250738
    VV = np.array([[float(v.subs(t, tn)) for v in V[i]] for i in range(15)])
    HH = np.full((3,3), tn)
    np.fill_diagonal(HH, 1)
    HV = VV@HH
    norm = np.zeros((15,45))
    for i in range(15):
        norm[i,3*i:3*i+3] = HV[i]
    contact = np.zeros((30,45))
    for k, (i,j) in enumerate(edges):
        contact[k,3*i:3*i+3] = HV[j]
        contact[k,3*j:3*j+3] = HV[i]
    gauge = np.zeros((3,45))
    gauge[0,1] = gauge[1,2] = gauge[2,17] = 1
    Q = np.linalg.qr(np.vstack((norm,gauge)).T, mode='complete')[0]
    _, _, pivots = qr((contact@Q[:,18:]).T, pivoting=True)
    chosen = sorted(int(i) for i in pivots[:27])
    R = np.vstack((norm,contact[chosen],gauge))
    inverse = np.linalg.inv(R)
    result.update(selected_edges=chosen, inverse_scale=10**8,
                  inverse_numerators=np.round(inverse*10**8).astype(np.int64).tolist())
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = generate()
    args.output.write_text(json.dumps(data, separators=(',',':')))
    from verify import verify
    verify(data)
    print('Generated and independently verified '+str(args.output))
