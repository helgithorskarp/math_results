"""Outward dyadic intervals; no floating-point operations in predicates."""
from math import isqrt
BITS = 128
S = 1 << BITS

def ceildiv(a, b):
    assert b > 0
    return -((-a) // b)

class I:
    __slots__ = ('lo', 'hi')
    def __init__(self, lo, hi):
        assert isinstance(lo, int) and isinstance(hi, int) and lo <= hi
        self.lo, self.hi = lo, hi
    @staticmethod
    def q(a, b=1):
        assert b > 0
        return I(a*S//b, ceildiv(a*S, b))
    def __add__(self, b):
        return I(self.lo+b.lo, self.hi+b.hi)
    def __neg__(self):
        return I(-self.hi, -self.lo)
    def __sub__(self, b):
        return self + -b
    def __mul__(self, b):
        products = [x*y for x in (self.lo,self.hi) for y in (b.lo,b.hi)]
        return I(min(products)//S, ceildiv(max(products),S))
    def __truediv__(self, b):
        assert not b.lo <= 0 <= b.hi, 'unresolved division'
        if b.hi < 0:
            return (-self)/(-b)
        return I(min(x*S//y for x in (self.lo,self.hi) for y in (b.lo,b.hi)),
                 max(ceildiv(x*S,y) for x in (self.lo,self.hi) for y in (b.lo,b.hi)))
    def sqrt(self):
        assert self.lo >= 0, 'unresolved square root'
        lo, hi = isqrt(self.lo*S), isqrt(self.hi*S)
        return I(lo, hi+(hi*hi < self.hi*S))
    def square(self):
        lo = 0 if self.lo <= 0 <= self.hi else min(self.lo*self.lo,self.hi*self.hi)
        hi = max(self.lo*self.lo,self.hi*self.hi)
        return I(lo//S,ceildiv(hi,S))
    def meets(self,b):
        return max(self.lo,b.lo) <= min(self.hi,b.hi)
    def data(self):
        return [self.lo,self.hi]

Q=I.q

def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def scale(a,t): return (a[0]*t,a[1]*t)
def turn(a): return (-a[1],a[0])
def norm(a): return a[0].square()+a[1].square()
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def boxdata(a): return [a[0].data(),a[1].data()]
