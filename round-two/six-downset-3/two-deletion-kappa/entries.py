"""Constant-size rational entry formula on the entire two-deletion downset.

No full domain or matrix is allocated. Core bits are a=1,b=2,c=4;
the two deleted triples have masks14 and22. See PROOF.md for the
closed row-sum and total-energy identities used at the empty vertex.
"""
import bootstrap
from fractions import Fraction as F
from weights import KAPPA,formula,scalar
from exact import require

EDGES={(1,2):F(1),(1,4):F(1),(2,5):F(-1),(3,4):F(-1)}
ROW={1:F(2),3:F(-1),5:F(-1)}

def member(q,mask):
    if type(mask) is not int or mask<0 or mask.bit_length()>q+3:return False
    size=mask.bit_count()
    return mask not in (14,22) and (size<=2 or size==3 and (mask&7).bit_count()>=2)

def make_entries(q,t=None):
    info=scalar(q);N=info['N'];s=info['s'];t=info['tau'] if t is None else t
    require(type(t) is int or isinstance(t,F),'repair parameter must be exact rational')
    t=F(t);require(0<t<=info['tau'],'repair parameter outside closed interval')
    weights=formula(F(q));h=F(1,3*q+5)
    alpha=F(q*(q+1),2)+3*(q+1)*h
    total=KAPPA*alpha-4*KAPPA*h+2*(s-2)
    typ=lambda A:((A&7).bit_count(),(A>>3).bit_count())
    def raw(A,B):
        if A==B:return F(s-1)
        if A&B:return F(-1)
        return weights[tuple(sorted((typ(A),typ(B))))]-1
    def row(A):
        a=typ(A)[0];p1=F(1) if a==0 else h if a<3 else -3*(q+1)*h
        return KAPPA*p1-raw(A,14)-raw(A,22)+t*ROW.get(A,F(0))
    def scaled(A,B):
        require(member(q,A) and member(q,B),'entry index is not in the full downset')
        if not A and not B:return 1+total
        if not A or not B:return 1-row(A or B)
        return 1+raw(A,B)+t*EDGES.get(tuple(sorted((A,B))),F(0))
    def normalized(A,B):return (scaled(A,B)-s*int(A==B))/(N-s)
    return {**info,'t':t},scaled,normalized

def entry(q,A,B,t=None):
    """Evaluate M[A,B] without allocating the downset."""
    return make_entries(q,t)[2](A,B)
