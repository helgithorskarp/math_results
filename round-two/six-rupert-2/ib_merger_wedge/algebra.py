"""Exact polynomial/matrix primitives adapted with credit to local9677/9918.

Only geometry.py and its two pinned original inputs are imported. No finite
domain, dual labels, mass bound or source theorem is inherited here.
"""
from fractions import Fraction as F
from math import factorial
import geometry as g
Q=g.Q
ZERO=(0,0,0)
def add(p,q):
    out=p.copy()
    for e,v in q.items():
        out[e]=out.get(e,Q())+v
        if out[e]==0:del out[e]
    return out
def scale(p,v):return {e:x*v for e,x in p.items() if x*v!=0}
def mul(p,q):
    out={}
    for e,u in p.items():
        for f,v in q.items():
            h=tuple(x+y for x,y in zip(e,f));out[h]=out.get(h,Q())+u*v
    return {e:v for e,v in out.items() if v!=0}
def linear(values):return {tuple(int(i==k) for i in range(3)):v for k,v in enumerate(values) if v!=0}
def sum_polys(polys):
    out={}
    for x in polys:out=add(out,x)
    return out
def det(M):
    states={0:{ZERO:Q(1)}}
    for row in range(5):
        nxt={}
        for mask,v in states.items():
            for k in range(5):
                if mask>>k&1:continue
                sign=(-1)**sum(mask>>i&1 for i in range(k+1,5));key=mask|(1<<k)
                nxt[key]=add(nxt.get(key,{}),scale(mul(v,M[row][k]),sign))
        states=nxt
    return states[31]
def controls(poly,degree):
    g.require(all(sum(e)==degree for e in poly),'literal homogeneous triangular degree')
    return [(e,poly.get(e,Q())/Q(F(factorial(degree),factorial(e[0])*factorial(e[1])*factorial(e[2]))))
            for i in range(degree+1) for j in range(degree-i+1) for e in [(i,j,degree-i-j)]]
def powq(x,k):
    v=Q(1)
    for i in range(k):v=v*x
    return v
def value(poly,t):return sum((v*powq(t[0],e[0])*powq(t[1],e[1])*powq(t[2],e[2]) for e,v in poly.items()),Q())
def directdet(A):
    M=[list(row) for row in A];out=Q(1)
    for k in range(5):
        r=next((i for i in range(k,5) if M[i][k]!=0),None)
        if r is None:return Q()
        if r!=k:M[k],M[r]=M[r],M[k];out=-out
        v=M[k][k];out=out*v
        for i in range(k+1,5):
            f=M[i][k]/v
            for j in range(k+1,5):M[i][j]-=f*M[k][j]
    return out
def inverse(A):
    n=len(A);M=[list(row)+[Q(int(i==j)) for j in range(n)] for i,row in enumerate(A)]
    for k in range(n):
        r=next((i for i in range(k,n) if M[i][k]!=0),None)
        if r is None:raise ValueError('singular original matrix')
        M[k],M[r]=M[r],M[k];v=M[k][k];M[k]=[x/v for x in M[k]]
        for i in range(n):
            if i==k:continue
            v=M[i][k];M[i]=[x-v*y for x,y in zip(M[i],M[k])]
    out=tuple(tuple(row[n:]) for row in M)
    g.require(all(sum((A[i][k]*out[k][j] for k in range(n)),Q())==int(i==j) for i in range(n) for j in range(n)),'independent original full inverse product')
    return out
class P:
    """Ordinary sparse ring in three free Cayley variables, credited to HB10107."""
    def __init__(self,v=0):self.terms={e:Q(x) for e,x in v.items() if x!=0} if isinstance(v,dict) else ({ZERO:Q(v)} if v!=0 else {})
    @classmethod
    def variable(cls,i):return cls({tuple(int(k==i) for k in range(3)):Q(1)})
    def lift(self,x):return x if isinstance(x,P) else P(x)
    def __add__(self,x):return P(add(self.terms,self.lift(x).terms))
    __radd__=__add__
    def __neg__(self):return P(scale(self.terms,-1))
    def __sub__(self,x):return self+-self.lift(x)
    def __rsub__(self,x):return self.lift(x)+-self
    def __mul__(self,x):return P(mul(self.terms,self.lift(x).terms))
    __rmul__=__mul__
    def __eq__(self,x):return self.terms==self.lift(x).terms
def dot(u,v):return sum((y*x if isinstance(y,P) else x*y for x,y in zip(u,v)),0)
def cross(u,v):return (u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
def rot_num(c):
    c2=dot(c,c);K=((0,-c[2],c[1]),(c[2],0,-c[0]),(-c[1],c[0],0))
    return tuple(tuple((1-c2)*int(i==j)+c[i]*c[j]*2+K[i][j]*2 for j in range(3)) for i in range(3))
