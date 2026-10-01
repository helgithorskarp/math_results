"""Exact top-band affine seeds and the credited uniform core/trade/lift.

six-downset-2, researcher. New certificate scope: D(20,10), width4.
The affine generator alone makes no PSD claim. Python3.11+ stdlib only.
Core/sectors/trade/lift credited to source9121638 and its predecessors.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations
from math import comb


def require(condition, message):
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class Parameters:
    n: int
    r: int
    width: int
    N: int
    s: int
    beta: tuple
    epsilon: Q


def counts(n,r):
    require(type(n) is int and type(r) is int and r>=2 and n>=2*r,
            "Integer domain r>=2,n>=2r")
    return sum(comb(n,a) for a in range(r+1)),sum(comb(n-1,a) for a in range(r))


def affine(n,r,width):
    """Exact RREF of all center/star moment constraints, symmetric beta."""
    N,s=counts(n,r)
    require(type(width) is int and 1<=width<=r,"Band width")
    pairs=[(a,b) for a in range(1,r+1) for b in range(a,r+1) if b>=r-width+1]
    B=[comb(n,a) for a in range(r+1)]; dim=len(pairs);rows=[]
    for a in range(1,r+1):
        for moment in (0,1):
            row=[Q(0)]*dim
            for k,(i,j) in enumerate(pairs):
                if a==i:row[k]+=Q(j if moment else 1)
                elif a==j:row[k]+=Q(B[i],B[j])*(i if moment else 1)
            row.append(Q(n-a) if moment else Q(N-1-s,s))
            rows.append(row)
    piv=[];pos=0
    for col in range(dim):
        idx=next((i for i in range(pos,len(rows)) if rows[i][col]),None)
        if idx is None:continue
        rows[pos],rows[idx]=rows[idx],rows[pos]
        v=rows[pos][col];rows[pos]=[x/v for x in rows[pos]]
        for i in range(len(rows)):
            if i!=pos and rows[i][col]:
                v=rows[i][col];rows[i]=[x-v*y for x,y in zip(rows[i],rows[pos])]
        piv.append(col);pos+=1
    require(all(any(row[:-1]) or not row[-1] for row in rows),"Consistent affine equations")
    free=[i for i in range(dim) if i not in piv]
    meta={'n':n,'r':r,'width':width,'first_active':r-width+1,
          'variables':dim,'rank':len(piv),'free_pairs':[[*pairs[k]] for k in free]}
    def recover(values):
        require(len(values)==len(free) and all(type(v) is Q for v in values),"Exact free values")
        z=[Q(0)]*dim
        for k,v in zip(free,values):z[k]=v
        for i,col in enumerate(piv):z[col]=rows[i][-1]-sum(rows[i][k]*z[k] for k in free)
        beta=[[Q(0)]*(r+1) for _ in range(r+1)]
        for (a,b),v in zip(pairs,z):beta[a][b]=beta[b][a]=Q(s,comb(n-a,b))*v
        epsilon=Q(n,72*(N-1)*(n-1)*(n-2)*(n-3))
        return Parameters(n,r,width,N,s,tuple(tuple(row) for row in beta),epsilon)
    return meta,recover


def trade(n,a,b):
    if a==b==1:return (n-2)*(n-3)
    if {a,b}=={1,2}:return -(n-3)
    return int(a==b==2)


def sectors(P,*,repaired=False):
    """Complete harmonic blocks (positive metric G); not a PSD verdict."""
    out=[]
    for j in range(P.r+1):
        aa=list(range(max(1,j),P.r+1));g=[comb(P.n-2*j,a-j) for a in aa]
        K=[[Q(P.s*int(a==b)-(comb(P.n,b) if j==0 else 0))+
            (-1)**j*(P.beta[a][b]+(P.epsilon*trade(P.n,a,b) if repaired else 0))*
            comb(P.n-a-j,b-j) for b in aa] for a in aa]
        U=[[P.N*int(i==k)-(comb(P.n,b) if j==0 else 0)-K[i][k]
            for k,b in enumerate(aa)] for i,a in enumerate(aa)]
        out.append((j,aa,g,K,U))
    return out


def slack_entry(P,A,B,*,repaired=True):
    for v in (A,B):
        require(type(v) is int and 0<=v<2**P.n and v.bit_count()<=P.r,"Downset vertex")
    t=P.epsilon if repaired else Q(0);n=P.n
    if A==B==0:return 1+t*Q(n*(n-1)*(n-2)*(n-3),4)
    if A==0 or B==0:
        a=(A|B).bit_count()
        row=Q((n-1)*(n-2)*(n-3),2) if a==1 else -Q((n-2)*(n-3),2) if a==2 else Q(0)
        return 1-t*row
    if A==B:return Q(P.s)
    if A&B:return Q(0)
    a,b=A.bit_count(),B.bit_count()
    return P.beta[a][b]+t*trade(n,a,b)


def literal_matrix(P):
    require(P.N<=256,"Literal matrix guard")
    V=[sum(1<<i for i in A) for a in range(P.r+1) for A in combinations(range(P.n),a)]
    return V,[[slack_entry(P,A,B) for B in V] for A in V]
