"""Reviewer-authored exact linear primitives; psd/determinant reused unchanged
from own source77e859b56ee1808932766c83bb6e428cb6ac0415. No researcher import.
"""
from fractions import Fraction as F
from itertools import permutations
import hashlib,json

def need(ok,why):
    if not ok:raise ValueError(why)
def exact(v):
    need(type(v) is int or isinstance(v,F),'exact input')
    return F(v)
def canonical(v):
    if isinstance(v,F):return str(v)
    if isinstance(v,dict):return {str(k):canonical(w) for k,w in v.items()}
    if isinstance(v,(list,tuple)):return [canonical(w) for w in v]
    return v
def digest(v):
    return hashlib.sha256(json.dumps(canonical(v),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def mv(A,v):return [sum(a*b for a,b in zip(row,v)) for row in A]
def dot(v,w):return sum(a*b for a,b in zip(v,w))
def form(A,v,w):return dot(v,mv(A,w))
def inverse(A):
    n=len(A);B=[[exact(v) for v in row]+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        p=next((i for i in range(j,n) if B[i][j]),None);need(p is not None,'invertible')
        B[j],B[p]=B[p],B[j];v=B[j][j];B[j]=[x/v for x in B[j]]
        for i in range(n):
            if i==j:continue
            a=B[i][j];B[i]=[x-a*y for x,y in zip(B[i],B[j])]
    return [r[n:] for r in B]
def psd(A):
    """Exact rational Schur congruence with largest-diagonal pivoting.

    Unlike the author's denominator-cleared fixed-order engine, the
    reference keeps Fraction entries and chooses new physical pivots.
    """
    n=len(A);need(all(len(r)==n for r in A),'square form')
    B=[[exact(v) for v in row] for row in A]
    need(all(B[i][j]==B[j][i] for i in range(n) for j in range(n)),'symmetric form')
    pivots=[];labels=list(range(n))
    while B:
        m=len(B);need(all(B[i][i]>=0 for i in range(m)),'negative Schur diagonal')
        p=max(range(m),key=lambda i:B[i][i]);d=B[p][p]
        if d==0:
            need(all(v==0 for row in B for v in row),'zero-diagonal nonzero residual')
            break
        pivots.append([labels[p],d]);ix=[i for i in range(m) if i!=p]
        ratios=[B[i][p]/d for i in ix]
        new=[[F(0)]*len(ix) for _ in ix]
        for i,ii in enumerate(ix):
            for j in range(i,len(ix)):
                value=B[ii][ix[j]]-ratios[i]*B[p][ix[j]]
                new[i][j]=new[j][i]=value
        B=new;labels=[labels[i] for i in ix]
    return {'dimension':n,'rank':len(pivots),'pivot_record_sha256':digest(pivots)}

def determinant(A):
    n=len(A);total=F(0)
    for p in permutations(range(n)):
        inversions=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term=F((-1)**inversions)
        for i in range(n):term*=A[i][p[i]]
        total+=term
    return total

