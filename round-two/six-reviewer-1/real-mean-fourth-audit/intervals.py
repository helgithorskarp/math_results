"""Exact rational closed intervals, fixed 60 bisections, no floating point."""
from fractions import Fraction as Q
from field import need


class Box:
    def __init__(self,lo,hi=None):
        self.lo=Q(lo);self.hi=Q(lo if hi is None else hi)
        need(self.lo<=self.hi,'interval endpoint order')
    def __add__(self,b):
        b=b if isinstance(b,Box)else Box(b)
        return Box(self.lo+b.lo,self.hi+b.hi)
    __radd__=__add__
    def __neg__(self):
        return Box(-self.hi,-self.lo)
    def __sub__(self,b):
        return self+-Box(b) if not isinstance(b,Box)else self+-b
    def __rsub__(self,b):
        return Box(b)+-self
    def __mul__(self,b):
        b=b if isinstance(b,Box)else Box(b)
        endpoints=[self.lo*b.lo,self.lo*b.hi,self.hi*b.lo,self.hi*b.hi]
        return Box(min(endpoints),max(endpoints))
    __rmul__=__mul__
    def reciprocal(self):
        need(self.hi<0 or self.lo>0,'interval divisor crosses zero')
        return Box(1/self.hi,1/self.lo)
    def __truediv__(self,b):
        b=b if isinstance(b,Box)else Box(b)
        return self*b.reciprocal()
    def __rtruediv__(self,b):
        return Box(b)*self.reciprocal()
    def __pow__(self,n):
        out=Box(1)
        for _ in range(n):out=out*self
        return out
    def record(self):
        return [str(self.lo),str(self.hi)]


def physical_cosine():
    f=lambda x:8*x**3-6*x-1
    lo,hi=Q(939,1000),Q(940,1000)
    need(f(lo)<0<f(hi) and 24*lo*lo-6>0,'unique positive physical cosine root')
    # cos(pi/9)>cos(pi/6)>1/2 and cos triple angle=1/2 identify this root.
    for _ in range(60):
        mid=(lo+hi)/2
        if f(mid)<0:lo=mid
        else:hi=mid
    need(f(lo)<0<f(hi),'exact bracketing after fixed bisection')
    return Box(lo,hi)
