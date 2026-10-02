"""Degree-zero necessary forms; credited9365/9269 star face, stdlib only.

No centering equation is present. Ordinary bridges appear in PROOF.md.
"""
from fractions import Fraction as Q
from math import comb

def require(ok, message):
    if not ok:
        raise ValueError(message)

def choose(n,k):
    return comb(n,k) if n>=0 and 0<=k<=n else 0

def parameters(n):
    require(type(n) is int and n>=6,'Domain n>=6')
    return 2**n-n-1,2**(n-1)-n,2**(n-1)-1

def physical(n,B,upper=False):
    """Literal layer-indicator bilinear form of C or U on nonempty sets."""
    N,s,h=parameters(n);aa=list(range(1,n-1))
    F=[[Q(comb(n,a))*((h if upper else s)*int(a==b)
          +(-1 if upper else 1)*B[a][b]*choose(n-a,b)
          -(0 if upper else comb(n,b))) for b in aa] for a in aa]
    require(all(F[i][j]==F[j][i] for i in range(len(aa)) for j in range(len(aa))),
            'Physical layer form symmetry')
    kernel=[Q(a) for a in aa]
    if not upper:
        require(all(sum(x*y for x,y in zip(row,kernel))==0 for row in F),
                'Actual cardinality kernel')
    return aa,F

def quadratic(F,v):
    require(len(F)==len(v) and all(len(row)==len(v) for row in F),'Quadratic shape')
    return sum(F[i][j]*v[i]*v[j] for i in range(len(v)) for j in range(len(v)))
