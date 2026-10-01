"""Independent factor/integrate and cyclotomic residual-root audit.

This route uses neither the sparse primitive nor Chebyshev evaluation to
form the polynomial or its roots. The only shared mathematical inputs are
the solved parameter coefficients, explicit cubic arithmetic and the
degree-nine boundary pattern inherited from8921.
"""
from fractions import Fraction as F

from series import series_ring
from arithmetic import K,Z,require


def factor_integrate(eta,u0,u1,T):
    S=type(eta)
    factors=[[-eta*u0,S(1)] for _ in range(6)]
    factors.append([(eta*u1)**2+eta*T,-2*eta*u1,S(1)])
    derivative=[S(9)]
    for factor in factors:
        out=[S(0) for _ in range(len(derivative)+len(factor)-1)]
        for i,x in enumerate(derivative):
            for j,y in enumerate(factor):
                out[i+j]+=x*y
        derivative=out
    primitive=[S(0)]+[x/F(j+1) for j,x in enumerate(derivative)]
    a=1-eta
    primitive[0]-=sum((primitive[j]*a**j for j in range(1,10)),S(0))
    return primitive


def residual_root(coefficients,omega,order,audit=None):
    check = audit.check if audit is not None else require
    q=omega.q
    A=series_ring(order,lambda v:Z(v,q=q))
    r=A(omega)
    def evaluate():
        value=A(0)
        for row in reversed(coefficients):
            value=value*r+A(row.a)
        return value
    for j in range(1,order+1):
        value=evaluate().a[j]
        r=r.with_coefficient(j,-omega*value/F(9))
    residual=evaluate()
    check(residual==0,'direct cyclotomic root residual')
    radius=r*A([x.conj() for x in r.a])-1
    check(all(v.a[1]==v.a[2]==v.a[3]==0 for v in radius.a),
        'squared modulus fully descends to real cubic field')
    return r,[v.a[0]/2 for v in radius.a]

