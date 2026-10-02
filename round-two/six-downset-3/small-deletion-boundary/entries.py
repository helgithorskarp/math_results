"""Whole rational M entries, including actual empty-loop and row.

No domain allocation; only the at-most-two outside points of A are read.
For q8,k3 accept the full real rectangle at exact rational endpoints/inputs.
All other default parameters have the proved real interval 0<t<=tau.
"""
from fractions import Fraction as F
from boundary_parameters import parameters
from literal import require,table,typ,member

EDGES={(1,2):1,(1,4):1,(2,5):-1,(3,4):-1}


def certificate(q,k,kappa=None,t=None):
    p=parameters(q,k)
    kap=p['kappa'] if kappa is None else kappa
    t=p['tau'] if t is None else t
    require(isinstance(kap,F) and isinstance(t,F),'exact rational kappa,t required by evaluator')
    if (q,k)==(8,3):
        require(0<kap<=F(1,4096) and F(3,8)<=t<=F(1,2),'q8 positive rectangle premises')
    else:
        require(kap==p['kappa'] and 0<t<=p['tau'],'positive repair interval premises')
    w={key:x+kap*y for key,(x,y) in table(q).items()}
    h=F(1,3*q+5);alpha=F(q*(q+1),2)+3*(q+1)*h
    def row(A):
        a,b=typ(A);r=F(1) if a==0 else h if a<3 else -3*(q+1)*h
        if A&6:removed=F(-k)
        else:
            out=A>>3;hits=0
            while out:
                low=out&-out;hits+=int(low.bit_length()<=k);out-=low
            removed=-hits+(k-hits)*(w[tuple(sorted((typ(A),(2,1))))]-1)
        return kap*r-removed+t*(2 if A==1 else -1 if A in (3,5) else 0)
    total=kap*(alpha-2*k*h)+k*(p['s']-k)
    def entry(A,B):
        require(member(q,k,A) and member(q,k,B),'nonmember supplied')
        if A==B==0:L=1+total
        elif A==0:L=1-row(B)
        elif B==0:L=1-row(A)
        else:
            C=F(p['s']-1) if A==B else F(-1) if A&B else w[tuple(sorted((typ(A),typ(B))))]-1
            L=1+C+t*EDGES.get(tuple(sorted((A,B))),0)
        return (L-p['s']*int(A==B))/(p['N']-p['s'])
    return {**p,'kappa':kap,'t':t},entry
