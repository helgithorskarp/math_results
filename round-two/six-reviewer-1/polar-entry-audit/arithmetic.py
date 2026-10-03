"""Credited OWN exact arithmetic only, extracted from source74977ee1.
Polynomial primitives originate in OWN25187d5; Gaussian primitives in
OWN785f5208. No old target budgets, outputs, fixtures or executable builds.
"""
from fractions import Fraction as Q
from math import comb
def need(ok,what):
    if not ok:raise ValueError(what)
def poly(c=0):return {(0,0):Q(c)} if c else {}
def atom(i):return {(int(i==0),int(i==1)):Q(1)}
def clean(p):return {k:v for k,v in p.items() if v}
def add(*ps):
    r={}
    for p in ps:
        for k,v in p.items():r[k]=r.get(k,Q(0))+v
    return clean(r)
def sc(p,c):return clean({k:v*c for k,v in p.items()})
def mul(p,q):
    r={}
    for (i,j),v in p.items():
        for (k,l),w in q.items():r[i+k,j+l]=r.get((i+k,j+l),Q(0))+v*w
    return clean(r)
def pw(p,n):
    r=poly(1)
    for _ in range(n):r=mul(r,p)
    return r
def integrate(p,coordinate=1):
    # Full integral on [0,1], not formal degree truncation.
    r={}
    for ij,v in p.items():
        k=list(ij);degree=k[coordinate];k[coordinate]=0;k=tuple(k)
        r[k]=r.get(k,Q(0))+v/(degree+1)
    return clean(r)
def ev(p,x,y=0):return sum((v*x**i*y**j for (i,j),v in p.items()),Q(0))
def pack(p):return [[i,j,str(v)] for (i,j),v in sorted(p.items())]
def uni(p):
    need(all(j==0 for i,j in p),'univariate support')
    return [p.get((i,0),Q(0)) for i in range(1+max((i for i,j in p),default=0))]
def coefficients(p):return list(map(str,uni(p)))
def sub(p,x,y):
    return add(*(sc(mul(pw(x,i),pw(y,j)),v)for (i,j),v in p.items()))
def strict(margins,k,v):need(v>0,k);margins[k]=str(v)

def ga(x,y=0):return Q(x),Q(y)
def gadd(x,y):return x[0]+y[0],x[1]+y[1]
def gmul(x,y):return x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def gsc(x,q):return x[0]*q,x[1]*q
def gcj(x):return x[0],-x[1]
def gn(x):return x[0]**2+x[1]**2
def gp(x,n):
    out=ga(1)
    for _ in range(n):out=gmul(out,x)
    return out
def gsum(xs):
    out=ga(0)
    for x in xs:out=gadd(out,x)
    return out
def gpoly(roots):
    p=[ga(1)]
    for x in roots:
        n=[ga(0) for _ in range(len(p)+1)]
        for j,c in enumerate(p):n[j]=gadd(n[j],gsc(gmul(c,x),-1));n[j+1]=gadd(n[j+1],c)
        p=n
    return p
def ge(p,x):return gsum(gmul(c,gp(x,j)) for j,c in enumerate(p))
