"""Exact integer polynomial/Cramer and positive-factor clearing helpers.

All three-slot polynomials here use only the first slot (t). Exact
division checks remainders and integral quotients. Every canceled factor
is strictly positive throughout the stated closed interval.
"""
from fractions import Fraction as Q
from math import gcd
from polynomials import P,cross
from model import make,positive_factors,NORMAL,CUT,SECOND_NORMAL,SECOND_CUT

LO,HI=Q(14,25),Q(593,1000)

def require(ok,message):
    if not ok:raise ValueError(message)

def divide(n,d):
    require(all(k[1:]==(0,0) for p in (n,d) for k in p.c),'univariate polynomial')
    n={k[0]:Q(v) for k,v in n.c.items()};d={k[0]:Q(v) for k,v in d.c.items()}
    require(bool(d),'nonzero divisor');out={}
    while n and max(n)>=max(d):
        j=max(n)-max(d);c=n[max(n)]/d[max(d)];out[j]=c
        for k,v in d.items():
            n[k+j]=n.get(k+j,Q())-c*v
            if not n[k+j]:del n[k+j]
    require(not n and all(v.denominator==1 for v in out.values()),'exact integral division')
    return P({(k,0,0):v.numerator for k,v in out.items()})

def deflate(p,known):
    """Return a sign-equivalent primitive polynomial and exact clearing."""
    original=p;counts=[]
    for f in known:
        n=0
        while p.c:
            try:q=divide(p,f)
            except ValueError:break
            p=q;n+=1
        counts.append(n)
    content=0
    for x in p.c.values():content=gcd(content,abs(x))
    content=content or 1
    p=P({k:v//content for k,v in p.c.items()})
    rebuilt=p*content
    for f,n in zip(known,counts):rebuilt=rebuilt*f**n
    require(rebuilt==original,'exact positive-factor clearing identity')
    return p,counts,content

def primitive(p,known):return deflate(p,known)[0]

def row_planes(t):
    Y,O,_=make(t);a=1+t;Q4=(1-t*t)*(1+3*t)+8*t**4;L=1+2*t-t*t;out={}
    for i,y in Y.items():
        original=list(y);y=list(y);den=O
        for f in (a,Q4,L):
            while True:
                try:ny=[divide(x,f) for x in y];nd=divide(den,f)
                except ValueError:break
                y,den=ny,nd
        require(all(y[j]*O==original[j]*den for j in range(3)),'exact point denominator clearing')
        out[i]=([(1-t)*x+t*sum(y,t*0) for x in y],t*den)
    n=[t*0+x for x in NORMAL]
    out[99]=([(1-t)*x+t*sum(n,t*0) for x in n],t*0+CUT)
    n2=[t*0+x for x in SECOND_NORMAL]
    out[98]=([(1-t)*x+t*sum(n2,t*0) for x in n2],t*0+SECOND_CUT)
    return out,Y,O

def determinant(M,t):return sum((M[0][j]*cross(M[1],M[2])[j] for j in range(3)),t*0)

def cramer(M,rhs,t):
    D=determinant(M,t)
    if not D.c:return D,[]
    W=[determinant([[rhs[i] if j==k else M[i][j] for j in range(3)] for i in range(3)],t) for k in range(3)]
    for f in positive_factors(t):
        while True:
            try:nD=divide(D,f);nW=[divide(x,f) for x in W]
            except ValueError:break
            D,W=nD,nW
    content=0
    for p in [D]+W:
        for x in p.c.values():content=gcd(content,abs(x))
    D=P({k:v//content for k,v in D.c.items()});W=[P({k:v//content for k,v in p.c.items()}) for p in W]
    require(all(sum((M[i][j]*W[j] for j in range(3)),t*0)==rhs[i]*D for i in range(3)),'complete generic Cramer identity')
    return D,W

def vertex(planes,inds,t):
    return cramer([planes[i][0] for i in inds],[planes[i][1] for i in inds],t)

def parameter_box(path):
    lo,hi=LO,HI
    for bit in path:
        require(type(bit)is int and bit in (0,1),'binary subdivision path')
        mid=(lo+hi)/2
        if bit==0:hi=mid
        else:lo=mid
    return lo,hi
