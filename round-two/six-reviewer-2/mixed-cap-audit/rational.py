"""Reviewer rational polynomial ring with known positive linear factors.

No author engine or CAS. Variable t=q-4; denominators are powers of
t+4,t+3,t+5,t+6,t+7, strictly positive for every t>=0.
"""
from fractions import Fraction as F
from math import lcm
from linear import need,digest
ROOTS=(4,3,5,6,7)

def trim(p):
    p=list(map(F,p))
    while len(p)>1 and not p[-1]:p.pop()
    return tuple(p)
def add(a,b):
    p=[F(0)]*max(len(a),len(b))
    for i,v in enumerate(a):p[i]+=v
    for i,v in enumerate(b):p[i]+=v
    return trim(p)
def mul(a,b):
    p=[F(0)]*(len(a)+len(b)-1)
    for i,v in enumerate(a):
        for j,w in enumerate(b):p[i+j]+=v*w
    return trim(p)
def ev(p,x):
    out=F(0)
    for v in reversed(p):out=out*x+v
    return out
def divlinear(p,c):
    if len(p)==1:return None
    b=[F(0)]*(len(p)-1);b[-1]=p[-1]
    for i in range(len(b)-2,-1,-1):b[i]=p[i+1]-c*b[i+1]
    return trim(b) if p[0]==c*b[0] else None
def factors(p,e):
    for c,k in zip(ROOTS,e):
        for _ in range(k):p=mul(p,(c,1))
    return p

class R:
    def __init__(self,p=0,e=(0,0,0,0,0)):
        if isinstance(p,R):self.p=p.p;self.e=p.e;return
        p=trim(p if isinstance(p,(tuple,list)) else (p,));e=list(e)
        need(len(e)==5 and all(type(k)is int and k>=0 for k in e),'known denominator factors')
        if p==(0,):e=[0]*5
        else:
            for i,c in enumerate(ROOTS):
                while e[i]:
                    z=divlinear(p,c)
                    if z is None:break
                    p=z;e[i]-=1
        self.p=p;self.e=tuple(e)
    def __add__(a,b):
        b=R(b);e=tuple(max(x,y)for x,y in zip(a.e,b.e))
        x=factors(a.p,tuple(x-y for x,y in zip(e,a.e)))
        y=factors(b.p,tuple(x-y for x,y in zip(e,b.e)))
        return R(add(x,y),e)
    __radd__=__add__
    def __neg__(a):return R(tuple(-v for v in a.p),a.e)
    def __sub__(a,b):return a+-R(b)
    def __rsub__(a,b):return R(b)+-a
    def __mul__(a,b):
        b=R(b);return R(mul(a.p,b.p),tuple(x+y for x,y in zip(a.e,b.e)))
    __rmul__=__mul__
    def __truediv__(a,b):
        # Only explicitly known linear or nonzero scalar divisions occur.
        b=R(b)
        if len(b.p)==1 and b.e==(0,)*5:
            need(b.p[0]!=0,'nonzero divisor');return R(tuple(v/b.p[0]for v in a.p),a.e)
        for i,c in enumerate(ROOTS):
            if len(b.p)==2 and b.p[1] and b.p[0]==c*b.p[1] and b.e==(0,)*5:
                e=list(a.e);e[i]+=1;return R(tuple(v/b.p[1]for v in a.p),e)
        raise ValueError('unsupported rational division')
    def __eq__(a,b):
        z=a-R(b);return z.p==(0,)
    def value(a,t):
        return ev(a.p,t)/ev(factors((1,),a.e),t)
    def record(a):return {'p':[str(x)for x in a.p],'positive_factors':a.e}

def clear_rows(A):
    out=[];clearing=[]
    for row in A:
        e=tuple(max(x.e[i]for x in row)for i in range(5))
        polys=[factors(x.p,tuple(a-b for a,b in zip(e,x.e)))for x in row]
        integer=lcm(*(v.denominator for p in polys for v in p))
        polys=[tuple(int(v*integer)for v in p)for p in polys]
        out.append(polys);clearing.append({'positive_integer':integer,'positive_factor_exponents':e})
    return out,clearing

def determinant(A):
    """Scalar Fraction Gaussian elimination with adaptive row swaps."""
    B=[list(map(F,r))for r in A];n=len(B);out=F(1)
    for j in range(n):
        p=next((i for i in range(j,n)if B[i][j]),None)
        if p is None:return F(0)
        if p!=j:B[j],B[p]=B[p],B[j];out=-out
        pivot=B[j][j];out*=pivot
        for i in range(j+1,n):
            if not B[i][j]:continue
            z=B[i][j]/pivot
            for k in range(j+1,n):B[i][k]-=z*B[j][k]
    return out

def reconstruct(A):
    """Proven row degree bound + forward differences recover the whole det."""
    n=len(A);bound=sum(max(len(p)-1 for p in row)for row in A)
    need(bound<=180,'fixed degree guard')
    values=[determinant([[ev(p,x)for p in row]for row in A])for x in range(bound+1)]
    differences=[];temp=values
    while temp:
        differences.append(temp[0]);temp=[b-a for a,b in zip(temp,temp[1:])]
    polynomial=(F(0),);binomial=(F(1),)
    for j,v in enumerate(differences):
        polynomial=add(polynomial,tuple(v*b for b in binomial))
        binomial=tuple(b/F(j+1)for b in mul(binomial,(-j,1)))
    need(len(polynomial)-1<=bound,'interpolation degree bound')
    need(all(ev(polynomial,x)==v for x,v in enumerate(values)),'every interpolation residual')
    need(all(v.denominator==1 for v in polynomial),'integer determinant coefficients')
    return tuple(int(v)for v in polynomial),bound,values

def positive_certificate(A,name):
    # Sylvester applies to the original symmetric rational matrix. Clearing
    # may destroy symmetry but multiplies determinants by positive scalars.
    need(all(A[i][j]==A[j][i]for i in range(len(A))for j in range(len(A))),'original rational symmetry')
    B,clearing=clear_rows(A);rows=[]
    for k in range(1,len(A)+1):
        C=[r[:k]for r in B[:k]];p,bound,values=reconstruct(C)
        need(p[0]>0 and all(v>0 for v in p),'strict positive coefficient certificate')
        rows.append({'order':k,'degree':len(p)-1,'degree_bound':bound,'coefficient_count':len(p),
                     'coefficient_sha256':digest(p),'coefficient_min':min(p),
                     'constant':p[0],'identity_evaluations':len(values),'evaluation_sha256':digest(values)})
    return {'name':name,'dimension':len(A),'row_clearing':clearing,'leading_minors':rows,
            'rational_matrix_sha256':digest([[x.record()for x in row]for row in A])}
