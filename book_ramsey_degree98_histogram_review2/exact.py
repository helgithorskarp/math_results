"""Reviewer2 exact congruence elimination; no authored negative vectors."""
from fractions import Fraction as F
from math import lcm
from incidence import need


def quadratic(a, q):
    return sum(q[i]*a[i][j]*q[j] for i in range(len(q)) for j in range(len(q)))


def psd(a):
    n=len(a);r=[[F(x) for x in row] for row in a]
    need(all(len(row)==n for row in a) and all(a[i][j]==a[j][i] for i in range(n) for j in range(n)), 'invalid symmetric matrix')
    vectors=[[F(i==j) for j in range(n)] for i in range(n)]
    rank=0
    while r:
        for i in range(len(r)):
            if r[i][i]<0:
                q=vectors[i];need(quadratic(a,q)<0,'false negative congruence witness')
                return False,rank,q
            if r[i][i]==0:
                j=next((j for j in range(len(r)) if r[i][j]),None)
                if j is not None:
                    c=-(r[j][j]+1)/(2*r[i][j])
                    q=[c*x+y for x,y in zip(vectors[i],vectors[j])]
                    need(quadratic(a,q)<0,'false zero-pivot witness')
                    return False,rank,q
        if not any(r[i][i] for i in range(len(r))):return True,rank,None
        p=next(i for i in range(len(r)) if r[i][i]>0)
        rest=[i for i in range(len(r)) if i!=p];d=r[p][p]
        vectors=[[vectors[i][z]-r[i][p]/d*vectors[p][z] for z in range(n)] for i in rest]
        r=[[r[i][j]-r[i][p]*r[p][j]/d for j in rest] for i in rest]
        rank+=1
    return True,rank,None


def inverse_integer(a):
    n=len(a);r=[[F(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        p=next((i for i in range(j,n) if r[i][j]),None)
        need(p is not None,'singular Gram');r[j],r[p]=r[p],r[j]
        t=r[j][j];r[j]=[x/t for x in r[j]]
        for i in range(n):
            if i!=j:
                t=r[i][j];r[i]=[x-t*y for x,y in zip(r[i],r[j])]
    inv=[row[n:] for row in r]
    need(all(sum(a[i][k]*inv[k][j] for k in range(n))==(i==j) for i in range(n) for j in range(n)), 'false inverse')
    d=lcm(*(x.denominator for row in inv for x in row))
    return [[int(d*x) for x in row] for row in inv],d
