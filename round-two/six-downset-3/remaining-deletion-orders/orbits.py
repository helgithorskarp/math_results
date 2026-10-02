"""counted 23-orbit forms, no physical-domain allocation.

Original affine table and exact PSD checker are credited byte-pinned
inputs of the published variance packet. This is a separate frontier.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import sys

SOURCE = Path(__file__).resolve().parent.parent
import dependencies
dependencies.check()
sys.path.insert(0, str(SOURCE / 'variance-deletion-frontier'))
import pins
from literal import table, require
from exact import schur_psd, digest

EDGES = {(1, 2): 1, (1, 4): 1, (2, 5): -1, (3, 4): -1}


def choose(n, r):
    return comb(n, r) if 0 <= r <= n else 0


def forms(q, k):
    require(type(q) is int and type(k) is int and k >= 2 and q-k >= 2,
            'counted 23-orbit domain: integer k>=2,q-k>=2')
    keys = [(c, z, w) for c in range(8) for z in range(3) for w in range(3)
            if 1 <= c.bit_count()+z+w <= 2 or
            c.bit_count()+z+w == 3 and c.bit_count() >= 2]
    keys.remove((6, 1, 0))
    keys.sort()
    sizes = [choose(k, z)*choose(q-k, w) for c, z, w in keys]
    N, s = (q*q+13*q+16)//2-k, 3*q+4
    require(len(keys) == 23 and sum(sizes) == N-1 and min(sizes) > 0,
            'complete nonempty 23-orbit census')
    tab = table(q)
    A, Delta, R = [], [], []
    for i, (c, z, w) in enumerate(keys):
        ar, dr, rr = [], [], []
        for j, (cc, zz, ww) in enumerate(keys):
            count = 0 if c & cc else choose(k-z, zz)*choose(q-k-w, ww)
            reverse = 0 if c & cc else choose(k-zz, z)*choose(q-k-ww, w)
            require(sizes[i]*count == sizes[j]*reverse, 'weighted disjoint reciprocity')
            # Some type pairs can never be disjoint and have no table entry.
            base, slope = tab[tuple(sorted(((c.bit_count(), z+w),
                                           (cc.bit_count(), zz+ww))))] if count else (F(0), F(0))
            ar.append(F(s*sizes[i]*int(i == j)-sizes[i]*sizes[j])+sizes[i]*count*base)
            dr.append(sizes[i]*count*slope)
            repair = EDGES.get(tuple(sorted((c, cc))), 0) if z+w+zz+ww == 0 else 0
            rr.append(F(repair))
        A.append(ar); Delta.append(dr); R.append(rr)
    U0 = [[F(N*sizes[i]*int(i == j)-sizes[i]*sizes[j])-A[i][j]
           for j in range(23)] for i in range(23)]
    require(all(M[i][j] == M[j][i] for M in (A, Delta, R, U0)
                for i in range(23) for j in range(23)), 'all original Gram forms symmetric')
    return {'q': q, 'k': k, 'N': N, 's': s, 'keys': keys,
            'sizes': sizes, 'C0': A, 'Delta': Delta, 'R': R, 'U0': U0}


def evaluate(data, kappa, trade):
    G = [[data['C0'][i][j]+kappa*data['Delta'][i][j]+trade*data['R'][i][j]
          for j in range(23)] for i in range(23)]
    H = [[data['U0'][i][j]-kappa*data['Delta'][i][j]-trade*data['R'][i][j]
          for j in range(23)] for i in range(23)]
    return G, H


def floor(data, kappa, trade, delta):
    G, H = evaluate(data, kappa, trade)
    return schur_psd([[H[i][j]-delta*data['sizes'][i]*int(i == j)
                       for j in range(23)] for i in range(23)])


def encoded(data):
    return {k: [[str(x) for x in row] for row in value] if k in ('C0', 'U0', 'Delta', 'R')
            else value for k, value in data.items()}
