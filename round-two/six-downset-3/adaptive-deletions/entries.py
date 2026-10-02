"""Whole rational certificate entries without allocating the downset.

Canonical Z consists of the first k outside points (bit positions3..k+2).
Only at most two outside points in the requested member are examined.
"""
import bootstrap
from fractions import Fraction as F
from weights import formula
from exact import require
from parameters import parameters

EDGES={(1,2):1,(1,4):1,(2,5):-1,(3,4):-1}


def certificate(q,k,t=None):
    p=parameters(q,k)
    t=p['tau'] if t is None else t
    require(isinstance(t,F) and 0<t<=p['tau'],'exact rational 0<t<=tau required')
    w=formula(F(q),p['kappa'])
    def typ(A):return (A&7).bit_count(),(A>>3).bit_count()
    def member(A):
        require(type(A) is int and A>=0 and A.bit_length()<=q+3,'literal member bitmask out of ground set')
        a,b=typ(A)
        require(a+b<=2 or a+b==3 and a>=2,'member outside the original downset')
        outside=A>>3
        require(not(A&7==6 and b==1 and outside.bit_length()<=k),'deleted triangle supplied as member')
    def row(A):
        a,b=typ(A);h=p['h']
        r=F(1) if a==0 else h if a<3 else -3*(q+1)*h
        if A&6:removed=F(-k)
        else:
            outside=A>>3;hits=0
            while outside:
                low=outside&-outside;hits+=int(low.bit_length()<=k);outside-=low
            removed=-hits+(k-hits)*(w[tuple(sorted((typ(A),(2,1))))]-1)
        trade_row=2 if A==1 else -1 if A in (3,5) else 0
        return p['kappa']*r-removed+t*trade_row
    total=p['kappa']*p['alpha']-2*k*p['kappa']*p['h']+k*(p['s']-k)
    def entry(A,B):
        member(A);member(B)
        if A==B==0:L=1+total
        elif A==0:L=1-row(B)
        elif B==0:L=1-row(A)
        else:
            C=F(p['s']-1) if A==B else F(-1) if A&B else w[tuple(sorted((typ(A),typ(B))))]-1
            L=1+C+t*EDGES.get(tuple(sorted((A,B))),0)
        return (L-p['s']*int(A==B))/(p['N']-p['s'])
    return p,entry
