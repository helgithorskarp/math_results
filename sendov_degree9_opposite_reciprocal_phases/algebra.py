"""Exact Q[b,c,Q] arithmetic and the opposite-phase origin norm.

Arithmetic patterns adapted from six-sendov-1's
sendov_degree9_coalesced_origin_minimum/algebra.py, source commit
1cf1ac65f3bc7ea5422b988365c506678e5adbd4, file SHA256
8bc673018e558179ba626e617a8736456cc811121f2fbeb78fe9510cb5be0211.
This smaller ring constructs the face directly, without importing it.
Characteristic zero, ordinary monomials, variable order (b,c,Q).
"""
from collections import defaultdict
from fractions import Fraction as F
from math import comb

ZERO=(0,0,0)
ONE={ZERO:F(1)}


def add(*items):
    out=defaultdict(F)
    for p in items:
        for e,v in p.items():
            out[e]+=v
    return {e:v for e,v in out.items() if v}


def scale(p,k):
    return {e:v*k for e,v in p.items() if v*k}


def mul(p,q):
    out=defaultdict(F)
    for e,v in p.items():
        for f,w in q.items():
            out[tuple(x+y for x,y in zip(e,f))]+=v*w
    return {e:v for e,v in out.items() if v}


def power(p,n):
    out=ONE
    while n:
        if n&1:
            out=mul(out,p)
        p=mul(p,p)
        n//=2
    return out


def variable(i):
    e=list(ZERO)
    e[i]=1
    return {tuple(e):F(1)}


def derivative(p,axis):
    out={}
    for e,v in p.items():
        if e[axis]:
            f=list(e)
            f[axis]-=1
            out[tuple(f)]=v*e[axis]
    return out


def substitute(p,axis,image):
    if not p:
        return {}
    powers=[power(image,j) for j in range(max(e[axis] for e in p)+1)]
    out={}
    for e,v in p.items():
        f=list(e)
        f[axis]=0
        out=add(out,scale(mul({tuple(f):F(1)},powers[e[axis]]),v))
    return out


def evaluate(p,values):
    degrees=[max((e[i] for e in p),default=0) for i in range(3)]
    powers=[[values[i]**j for j in range(degrees[i]+1)] for i in range(3)]
    return sum(v*powers[0][e[0]]*powers[1][e[1]]*powers[2][e[2]]
               for e,v in p.items())


def canonical(p):
    return [[list(e),str(v)] for e,v in sorted(p.items())]


def origin_norm():
    """Four polynomial convolutions in Q[b,c,Q][i beta], beta^2=Q(1-c^2)."""
    b,c,Q=[variable(j) for j in range(3)]
    B=mul(Q,add(ONE,scale(power(c,2),-1)))
    pair=[(ONE,{}),(scale(mul(b,c),-2),scale(b,-2)),
          (mul(power(b,2),add(ONE,scale(Q,-1))),{})]
    coeff=[(ONE,{})]
    for _ in range(4):
        out=[({},{}) for _ in range(len(coeff)+2)]
        for j,(p,r) in enumerate(coeff):
            for k,(s,t) in enumerate(pair):
                real=add(mul(p,s),scale(mul(B,mul(r,t)),-1))
                odd=add(mul(p,t),mul(r,s))
                out[j+k]=(add(out[j+k][0],real),add(out[j+k][1],odd))
        coeff=out
    P=add(*(scale(p,F(9,k+1)) for k,(p,_) in enumerate(coeff)))
    T=add(*(scale(t,F(9,k+1)) for k,(_,t) in enumerate(coeff)))
    E=add(mul(P,P),mul(B,mul(T,T)))
    K=add(mul(add(ONE,scale(Q,-1)),derivative(E,2)),scale(E,8))
    return E,K


def bernstein(p,degrees=None):
    """Full tensor coefficients; zero entries are retained."""
    if degrees is None:
        degrees=tuple(max(e[i] for e in p) for i in range(3))
    out=p
    for axis,d in enumerate(degrees):
        converted=defaultdict(F)
        for e,v in out.items():
            if e[axis]>d:
                raise ArithmeticError('Degree bound violated')
            for i in range(e[axis],d+1):
                f=list(e)
                f[axis]=i
                converted[tuple(f)]+=v*F(comb(i,e[axis]),comb(d,e[axis]))
        out=dict(converted)
    return out,degrees


def cells(K):
    b,t,v=[variable(j) for j in range(3)]
    image=add(b,mul(add(ONE,scale(b,-1)),t))
    box=substitute(substitute(K,1,image),2,scale(v,F(1,4)))
    out=[]
    for left,right in [(F(0),F(1,2)),(F(1,2),F(1))]:
        cell=substitute(box,0,add(scale(ONE,left),scale(b,right-left)))
        coeff,degrees=bernstein(cell,(16,8,7))
        out.append((left,right,coeff,degrees))
    return out


def divide_one_minus_b(p):
    if any(e[1] or e[2] for e in p):
        raise ArithmeticError('Univariate polynomial required')
    row={e[0]:v for e,v in p.items()}
    out={}
    value=F(0)
    for j in range(max(row)):
        value+=row.get(j,F(0))
        if value:
            out[(j,0,0)]=value
    if value+row.get(max(row),F(0)):
        raise ArithmeticError('Nonzero division remainder')
    return out


def weak_mean_certificate():
    """Re-certify the credited weak polar mean filter, not a new claim."""
    a=variable(0)
    D=add(ONE,scale(power(a,2),-1))
    L=add(ONE,a)
    pair=[mul(power(a,2),power(L,2)),
          scale(mul(mul(power(a,2),D),power(L,2)),2),
          mul(power(D,2),add(power(L,2),power(a,2)))]
    coeff=[ONE]
    for _ in range(4):
        out=[{} for _ in range(len(coeff)+2)]
        for j,p in enumerate(coeff):
            for k,q in enumerate(pair):
                out[j+k]=add(out[j+k],mul(p,q))
        coeff=out
    defect=add(power(L,8),scale(add(*(scale(p,F(1,k+1))
                                    for k,p in enumerate(coeff))),-1))
    quotient=divide_one_minus_b(divide_one_minus_b(defect))
    coeff,degrees=bernstein(quotient,(22,0,0))
    if mul(power(add(ONE,scale(a,-1)),2),quotient)!=defect:
        raise ArithmeticError('Weak mean division identity failed')
    return quotient,coeff,degrees
