"""Altered8757 type table and the newly proved two-deletion cap parameters.

The symbolic table admits kappa for comparison with the credited1/2 input.
The theorem and construction here use kappa=1/8, exactly two deletions,
and integerq>=7. See PROOF.md for the newly established premises.
"""
import bootstrap
from fractions import Fraction as F
from poly import R
from model import TYPES,formula as credited_formula,model
from exact import require

KAPPA=F(1,8);FLOOR=F(1,16)

def formula(q,kappa=KAPPA):
    require(isinstance(q,(F,R)) and isinstance(kappa,F),'exact table parameters required')
    s=3*q+4;h=kappa/(3*q+5)
    alpha1,beta1=1-1/q,1+1/q
    alpha2=1+2*h/(q*(q-1))
    beta2=1+2*(h+(q-1)**2/q)/((q-1)*(q-2))
    gamma1=1+6/q;gamma2=1+6/q-6*h*(q+1)/(q*(q-1))
    outside11=(kappa+(gamma1-1)+q-(s-q))/(q-1)
    outside12=q/(q-2)-2*q/((q-1)*(q-2))
    outside22=(kappa+(gamma2-1)+2*q/(q-1)-s+q*(q-1)/2)/((q-2)*(q-3)/2)
    out={}
    def put(a,b,x):out[tuple(sorted((a,b)))]=x
    o,p,a,b,c,d,e=TYPES
    put(o,o,outside11);put(o,p,outside12);put(p,p,outside22)
    for leaf,alpha,beta,gamma in [(o,alpha1,beta1,gamma1),(p,alpha2,beta2,gamma2)]:
        put(leaf,a,alpha);put(leaf,c,alpha);put(leaf,b,beta);put(leaf,d,beta);put(leaf,e,gamma)
    rr=3+2/q;ww=(s-rr)/(q-1)
    put(a,a,0);put(a,b,0);put(b,b,0);put(a,c,2);put(a,d,rr);put(b,c,rr);put(b,d,ww)
    return out

def cap_parameters(q,kappa=KAPPA):
    require(isinstance(q,(F,R)) and isinstance(kappa,F),'exact cap parameters required')
    n=(q*q+13*q+12)/2;s=3*q+4;g=n-2*s
    alpha=q*(q+1)/2+3*(q+1)/(3*q+5);h=1/(3*q+5)
    chi=2*g*(n-kappa+kappa*h)**2-((n-kappa)+kappa*alpha)*(n-kappa)*(n-s-2)
    gamma=g*chi/(n*(n-kappa)**2*(n-s-2))
    return n,s,chi,gamma

def scalar(q):
    require(type(q) is int and q>=7,'theorem requires literal integer q>=7')
    n,s,chi,gamma=cap_parameters(F(q))
    require(chi>0 and gamma>0 and n.denominator==1,'cap premise or integer size fails')
    return {'q':q,'N':int(n),'s':int(s),'chi':chi,'gamma':gamma,'tau':min(F(1,192),gamma/4)}

def inverse(matrix):
    """Exact small field inverse, credited8826/floor.py; no numerical step."""
    n=len(matrix);require(n>0 and all(len(row)==n for row in matrix),'nonsquare inverse input')
    a=[[R(x) for x in row]+[R(i==j) for j in range(n)] for i,row in enumerate(matrix)]
    for k in range(n):
        pivot=next((i for i in range(k,n) if a[i][k]!=0),None)
        require(pivot is not None,'singular exact kernel Gram')
        a[k],a[pivot]=a[pivot],a[k];scale=a[k][k];a[k]=[x/scale for x in a[k]]
        for i in range(n):
            if i!=k and a[i][k]!=0:
                scale=a[i][k];a[i]=[x-scale*y for x,y in zip(a[i],a[k])]
    result=[row[n:] for row in a]
    require(all(sum(R(matrix[i][h])*result[h][j] for h in range(n))==int(i==j) for i in range(n) for j in range(n)),'exact inverse residual')
    return result
