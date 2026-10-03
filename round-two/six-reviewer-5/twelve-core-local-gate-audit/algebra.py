"""Fresh quotient algebra: five rational coordinates; inverses by Gaussian solve.

No target arithmetic imports. A successful inverse is checked by a whole
product identity, so irreducibility of the quintic is not a premise.
"""
from fractions import Fraction as F
from functools import lru_cache
from enclosure import Box,SCALE

class A:
    __slots__=('c',)
    def __init__(self,x=0):
        if isinstance(x,A):self.c=x.c;return
        if isinstance(x,(int,F,str)):x=[F(x)]
        if not isinstance(x,(tuple,list)) or len(x)>5:raise TypeError('five exact coefficients')
        self.c=tuple(F(v) for v in x)+(F(0),)*(5-len(x))
    @staticmethod
    def cast(x):return x if isinstance(x,A) else A(x)
    def __bool__(self):return any(self.c)
    def __eq__(self,x):
        try:return self.c==self.cast(x).c
        except TypeError:return False
    def __add__(self,x):
        try:y=self.cast(x)
        except TypeError:return NotImplemented
        return A([a+b for a,b in zip(self.c,y.c)])
    __radd__=__add__
    def __neg__(self):return A([-v for v in self.c])
    def __sub__(self,x):return self+(-self.cast(x))
    def __rsub__(self,x):return self.cast(x)+(-self)
    def __mul__(self,x):
        try:y=self.cast(x)
        except TypeError:return NotImplemented
        out=[F(0)]*9
        for i,a in enumerate(self.c):
            for j,b in enumerate(y.c):out[i+j]+=a*b
        reduction=[F(1,13),F(3,13),F(-2,13),F(-6,13),F(1,13)]
        for i in range(8,4,-1):
            for j,a in enumerate(reduction):out[i-5+j]+=out[i]*a
        return A(out[:5])
    __rmul__=__mul__
    def __truediv__(self,x):return self*inverse(self.cast(x).c)
    def __rtruediv__(self,x):return self.cast(x)*inverse(self.c)
    def __pow__(self,n):
        if not isinstance(n,int) or n<0:raise ValueError('nonnegative exact power')
        out=A(1);b=self
        while n:
            if n&1:out=out*b
            b=b*b;n//=2
        return out
    def enclosure(self,root):
        out=Box(0)
        for v in reversed(self.c):out=out*root+v
        return out
    def encode(self):return [str(x) for x in self.c]

@lru_cache(maxsize=4096)
def inverse(coeff):
    x=A(coeff)
    if not x:raise ZeroDivisionError('zero quotient element')
    columns=[(x*A([0]*i+[1])).c for i in range(5)]
    mat=[[columns[j][i] for j in range(5)]+[F(i==0)] for i in range(5)]
    for k in range(5):
        pivot=next((i for i in range(k,5) if mat[i][k]),None)
        if pivot is None:raise ValueError('noninvertible quotient element')
        mat[k],mat[pivot]=mat[pivot],mat[k];v=mat[k][k];mat[k]=[a/v for a in mat[k]]
        for i in range(5):
            if i!=k:
                v=mat[i][k]
                if v:mat[i]=[a-v*b for a,b in zip(mat[i],mat[k])]
    out=A([row[-1] for row in mat])
    if x*out!=1:raise ValueError('whole inverse product')
    return out

T=A([0,1])
def solve(a,b):
    n=len(a);m=[[A.cast(v) for v in row]+[A.cast(b[i])] for i,row in enumerate(a)]
    for k in range(n):
        pivot=next((i for i in range(k,n) if m[i][k]),None)
        if pivot is None:raise ValueError('singular original linear system')
        m[k],m[pivot]=m[pivot],m[k];v=m[k][k];m[k]=[x/v for x in m[k]]
        for i in range(n):
            if i!=k:
                v=m[i][k]
                if v:m[i]=[x-v*y for x,y in zip(m[i],m[k])]
    out=[row[-1] for row in m]
    if any(sum((A.cast(x)*y for x,y in zip(row,out)),A())!=A.cast(v) for row,v in zip(a,b)):raise ValueError('whole solved system')
    return out
def determinant(a):
    if len(a)!=3:raise ValueError('three-dimensional determinant')
    return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])+a[0][1]*(a[1][2]*a[2][0]-a[1][0]*a[2][2])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])
def dot(a,b):return (1-T)*sum((x*y for x,y in zip(a,b)),A())+T*sum(a,A())*sum(b,A())
def sign(x,root):
    x=A.cast(x)
    if not x:return 0
    v=x.enclosure(root)
    if v.lo>0:return 1
    if v.hi<0:return -1
    lo,hi=refined_root(root.lo,root.hi)
    a=b=F(0)
    for c in reversed(x.c):
        products=(a*lo,a*hi,b*lo,b*hi)
        a,b=min(products)+c,max(products)+c
    if a>0:return 1
    if b<0:return -1
    raise ArithmeticError('unresolved root-polynomial sign')

@lru_cache(maxsize=8)
def refined_root(raw_lo,raw_hi):
    """Fixed 64 exact rational bisections; never infer sign from overlap."""
    lo,hi=F(raw_lo,SCALE),F(raw_hi,SCALE)
    def f(t):return 13*t**5-t**4+6*t**3+2*t**2-3*t-1
    if not f(lo)<0<f(hi):raise ArithmeticError('bisection bracket signs')
    for unused in range(64):
        m=(lo+hi)/2;y=f(m)
        if y==0:return m,m
        if y<0:lo=m
        else:hi=m
    return lo,hi
