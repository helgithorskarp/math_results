"""80-bit outward dyadic intervals and t,z derivative enclosures.

The interval primitive is adapted from credited mathematical code in
six-tammes-2 twelve-core-frame/model.py; the dual enclosure layer is new.
No rounding mode, floating operation or solver supplies a predicate.
"""
from fractions import Fraction as Q
from math import isqrt

S=1<<80
def require(ok,message):
    if not ok:raise ValueError(message)
class I:
    def __init__(self,a=0,b=None):
        a,b=Q(a),Q(a if b is None else b);require(a<=b,'ordered endpoints')
        self.l=a.numerator*S//a.denominator;self.h=-((-b.numerator*S)//b.denominator)
    @classmethod
    def raw(cls,l,h):
        require(l<=h,'ordered raw endpoints');v=object.__new__(cls);v.l,v.h=l,h;return v
    @staticmethod
    def cv(v):return v if isinstance(v,I) else I(v)
    def __add__(self,v):
        v=I.cv(v);return I.raw(self.l+v.l,self.h+v.h)
    __radd__=__add__
    def __neg__(self):return I.raw(-self.h,-self.l)
    def __sub__(self,v):return self+-I.cv(v)
    def __rsub__(self,v):return I.cv(v)+-self
    def __mul__(self,v):
        v=I.cv(v);rows=[a*b for a in (self.l,self.h) for b in (v.l,v.h)]
        return I.raw(min(rows)//S,-((-max(rows))//S))
    __rmul__=__mul__
    def __truediv__(self,v):
        v=I.cv(v)
        if v.l<=0<=v.h:raise ArithmeticError('interval denominator contains zero')
        rows=[Q(a*S,b) for a in (self.l,self.h) for b in (v.l,v.h)]
        low,high=min(rows),max(rows)
        return I.raw(low.numerator//low.denominator,-((-high.numerator)//high.denominator))
    def __rtruediv__(self,v):return I.cv(v)/self
    def __pow__(self,n):
        require(type(n)is int and n>=0,'nonnegative integral power')
        if n==2:
            a=min(self.l*self.l,self.h*self.h) if not self.l<=0<=self.h else 0
            b=max(self.l*self.l,self.h*self.h)
            return I.raw(a//S,-((-b)//S))
        v=I(1)
        for _ in range(n):v=v*self
        return v
    def sqrt(self):
        require(self.l>=0,'nonnegative square-root argument')
        low=isqrt(self.l*S);high=isqrt(self.h*S)
        if high*high<self.h*S:high+=1
        return I.raw(low,high)
class A:
 def __init__(self,v=0,dt=0,dz=0):self.v=I.cv(v);self.dt=I.cv(dt);self.dz=I.cv(dz)
 @staticmethod
 def cv(x):return x if isinstance(x,A) else A(x)
 def __add__(self,x):
  x=A.cv(x);return A(self.v+x.v,self.dt+x.dt,self.dz+x.dz)
 __radd__=__add__
 def __neg__(self):return A(-self.v,-self.dt,-self.dz)
 def __sub__(self,x):return self+-A.cv(x)
 def __rsub__(self,x):return A.cv(x)+-self
 def __mul__(self,x):
  x=A.cv(x);return A(self.v*x.v,self.dt*x.v+self.v*x.dt,self.dz*x.v+self.v*x.dz)
 __rmul__=__mul__
 def __truediv__(self,x):
  x=A.cv(x);v=self.v/x.v;return A(v,(self.dt-v*x.dt)/x.v,(self.dz-v*x.dz)/x.v)
 def __rtruediv__(self,x):return A.cv(x)/self
 def __pow__(self,n):
  if type(n)is not int or n<0:raise ValueError('nonnegative integral power')
  if not n:return A(1)
  return A(self.v**n,n*(self.v**(n-1))*self.dt,n*(self.v**(n-1))*self.dz)
 def sqrt(self):
  v=self.v.sqrt()
  if v.l<=0:raise ValueError('strict positive root for differentiated formula')
  return A(v,self.dt/(2*v),self.dz/(2*v))
