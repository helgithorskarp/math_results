"""Exact sparse endpoint polynomials, rational box transforms and basis conversion."""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product
from math import comb

def add(p,q,scale=Q(1)):
    out=defaultdict(Q,p)
    for e,c in q.items():out[e]+=scale*c
    return {e:c for e,c in out.items() if c}

def mul(p,q):
    out=defaultdict(Q)
    for e,c in p.items():
        for f,d in q.items():out[tuple(x+y for x,y in zip(e,f))]+=c*d
    return {e:c for e,c in out.items() if c}

def power(p,n):
    one={(0,)*len(next(iter(p))):Q(1)}
    for _ in range(n):one=mul(one,p)
    return one

def profile_products(pair_count,k):
    n_real=8-2*pair_count;m=n_real-k;dim=pair_count+3
    assert m>=1
    one={(0,)*dim:Q(1)}
    def var(axis):
        e=[0]*dim;e[axis]=1
        return {tuple(e):Q(1)}
    a,u,t=var(0),var(1),var(dim-1)
    D=add(one,a);b=add(one,power(a,2),Q(-1))
    residual=one;radii=[]
    for j in range(pair_count):
        v=var(2+j)
        radii.append(add(one,mul(mul(a,residual),v),Q(4)))
        residual=mul(residual,add(one,v,Q(-1)))
    C=add(one,mul(mul(a,u),residual),Q(8,m))
    lower=add(D,mul(a,t),Q(-1))
    free=add(D,mul(mul(a,t),C),Q(-1))
    f=mul(power(lower,k),power(free,m))
    radius_product=power(C,m)
    for R in radii:
        paired=add(mul(power(D,2),add(one,t,Q(-1))),
                   mul(add(mul(b,t),mul(power(a,2),power(t,2))),power(R,2)))
        f=mul(f,paired);radius_product=mul(radius_product,power(R,2))
    out=defaultdict(Q)
    for e,c in f.items():out[e[:-1]]+=9*c/(e[-1]+1)
    for e,c in radius_product.items():
        assert e[-1]==0
        out[e[:-1]]-=c
    return {e:c for e,c in out.items() if c}

def evaluate(p,variables):
    return sum((c*prod_values(x**i for x,i in zip(variables,e)) for e,c in p.items()),Q(0))

def prod_values(values):
    out=Q(1)
    for v in values:out*=v
    return out

def bernstein(p,degree=None):
    dim=len(next(iter(p)))
    actual=tuple(max(e[i] for e in p) for i in range(dim))
    if degree is None:degree=actual
    assert len(degree)==dim and all(n>=d for n,d in zip(degree,actual))
    out=dict(p)
    for axis,n in enumerate(degree):
        basis=defaultdict(Q)
        for e,c in out.items():
            for i in range(e[axis],n+1):
                f=list(e);f[axis]=i
                basis[tuple(f)]+=c*Q(comb(i,e[axis]),comb(n,e[axis]))
        out=dict(basis)
    return degree,{e:out.get(e,Q(0)) for e in product(*(range(n+1) for n in degree))}

def transform_axis(p,axis,left,right):
    out=defaultdict(Q)
    for e,c in p.items():
        for i in range(e[axis]+1):
            f=list(e);f[axis]=i
            out[tuple(f)]+=c*comb(e[axis],i)*left**(e[axis]-i)*(right-left)**i
    return {e:c for e,c in out.items() if c}
