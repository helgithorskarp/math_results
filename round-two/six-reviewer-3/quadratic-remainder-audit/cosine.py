"""New exact three-dimensional cosine field; no producer imports."""
from fractions import Fraction as F

class C:
    def __init__(self, values=()):
        if isinstance(values,C):self.v=values.v;return
        if not isinstance(values,(tuple,list)):values=[values]
        w=list(map(F,values))+[F(0)]*max(0,3-len(values))
        for j in range(len(w)-1,2,-1):
            w[j-3]+=w[j]/8;w[j-2]+=3*w[j]/4
        self.v=tuple(w[:3])
    def __add__(self,b):
        b=C(b);return C([x+y for x,y in zip(self.v,b.v)])
    __radd__=__add__
    def __neg__(self):return C([-x for x in self.v])
    def __sub__(self,b):return self+-C(b)
    def __rsub__(self,b):return C(b)+-self
    def __mul__(self,b):
        b=C(b);w=[F(0)]*5
        for i,x in enumerate(self.v):
            for j,y in enumerate(b.v):w[i+j]+=x*y
        return C(w)
    __rmul__=__mul__
    def inverse(self):
        columns=[(self*C([0]*j+[1])).v for j in range(3)]
        m=[[columns[j][i] for j in range(3)]+[F(i==0)] for i in range(3)]
        for j in range(3):
            k=next((k for k in range(j,3) if m[k][j]),None)
            if k is None:raise ValueError('noninvertible cosine element')
            m[j],m[k]=m[k],m[j];v=m[j][j];m[j]=[x/v for x in m[j]]
            for k in range(3):
                if k!=j:
                    v=m[k][j];m[k]=[x-v*y for x,y in zip(m[k],m[j])]
        return C([m[j][-1] for j in range(3)])
    def __truediv__(self,b):return self*C(b).inverse()
    def __rtruediv__(self,b):return C(b)*self.inverse()
    def __pow__(self,n):
        if n<0:return self.inverse()**(-n)
        w=C(1);x=self
        while n:
            if n&1:w=w*x
            x=x*x;n//=2
        return w
    def __eq__(self,b):return self.v==C(b).v
    def record(self):return list(map(str,self.v))

c=C([0,1]);d=2*c*c-1;y=1/(3*(1+c));x=C(F(2,3))-y
w4=1/(c+d);w3=F(2,3)*(7-(1-d)*w4)

def chebyshev(n):
    if n==0:return C(1)
    a,b=C(1),c
    for _ in range(1,n):a,b=b,2*c*b-a
    return b
