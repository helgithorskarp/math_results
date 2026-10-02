"""Exact whole constant-row variance and rational sufficient parameters.

Unbounded mathematical coverage is proved in PROOF.md. No matrix allocation.
"""
from fractions import Fraction as F
from math import comb, isqrt
from hashlib import sha256
import json

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def bound(k):
    require(type(k) is int and k>=5, 'literal integer k>=5')
    return (6*k-7+isqrt(28*k*k-36*k+17))//2

def row_classes(q, k):
    require(type(q) is int and type(k) is int and q >= 4 and 1 <= k <= q,
         'integer q>=4,1<=k<=q')
    ww = F(3*q+1, q-1)-F(2, q*(q-1))
    beta = F(2*(q-1), q*(q-2))
    out = [(5*q+6-k, F(1-k)), (1, 1+2*k+F(2*k, q)),
           (k, (k-1)*(ww-1)), (q-k, 1+k*(ww-1)),
           (k, F(k-1, q)), (q-k, 1+F(k, q))]
    for z in range(3):
        count = comb(k, z)*comb(q-k, 2-z) if k >= z and q-k >= 2-z else 0
        out.append((count, 1-z+(k-z)*beta))
    return out


def scalar_record(q, k):
    N = (q*q+13*q+16)//2-k
    n = N-1
    s = 3*q+4
    g = N-2*s
    e = F(q*q+(13-6*k)*q+2*k*k-10*k+14, 2)
    classes = row_classes(q, k)
    require(sum(c for c, r in classes) == n, 'original row count')
    require(sum(c*r for c, r in classes) == e, 'original mean polynomial')
    V = sum(c*r*r for c, r in classes)
    h = V-e*e/n
    require(g > 0 and h >= 0, 'positive gap and nonnegative variance')
    margin = e-h/g
    out = {'q': q, 'k': k, 'N': N, 'g': g, 'e': str(e), 'V': str(V),
           'strict_scalar_margin': str(margin), 'variance': str(h)}
    if margin > 0:
        mu = min(F(g, 2), margin/(n+2*h/(g*g)))
        kappa = min(F(1, 8), mu/(4*(16*s+1)))
        t = kappa/24
        loss = 16*s*kappa+2*t
        require(mu > 0 and 0 < kappa <= F(1, 8) and t == kappa/24,
             'strict rational parameters')
        require(loss < mu/4, 'quantitative cap perturbation')
        out.update({'nonempty_cap_floor_at_zero': str(mu),
                    'kappa': str(kappa), 't': str(t),
                    'certified_nonempty_and_projected_cap_floor': str(3*mu/4)})
    return out
