"""Independent fixed 96-bit dyadic interval arithmetic, no author imports."""
from fractions import Fraction
from math import isqrt

BITS = 96
SCALE = 1 << BITS

def ceildiv(a, b):
    return -((-a) // b)

class Box:
    __slots__ = ('lo', 'hi')
    def __init__(self, lo, hi=None, raw=False):
        if raw:
            self.lo, self.hi = lo, hi
        else:
            a, b = Fraction(lo), Fraction(lo if hi is None else hi)
            self.lo = (a.numerator * SCALE) // a.denominator
            self.hi = ceildiv(b.numerator * SCALE, b.denominator)
        if self.lo > self.hi:
            raise ArithmeticError('empty interval')
    @staticmethod
    def cast(x):
        return x if isinstance(x, Box) else Box(x)
    def __add__(self, other):
        y = self.cast(other)
        return Box(self.lo + y.lo, self.hi + y.hi, raw=True)
    __radd__ = __add__
    def __neg__(self):
        return Box(-self.hi, -self.lo, raw=True)
    def __sub__(self, other):
        return self + (-self.cast(other))
    def __rsub__(self, other):
        return self.cast(other) - self
    def __mul__(self, other):
        y = self.cast(other)
        a = (self.lo*y.lo, self.lo*y.hi, self.hi*y.lo, self.hi*y.hi)
        return Box(min(a)//SCALE, ceildiv(max(a), SCALE), raw=True)
    __rmul__ = __mul__
    def __truediv__(self, other):
        y = self.cast(other)
        if y.lo <= 0 <= y.hi:
            raise ArithmeticError('uncertified denominator')
        if y.hi < 0:
            return (-self)/(-y)
        a = (self.lo*SCALE//y.lo, self.lo*SCALE//y.hi,
             self.hi*SCALE//y.lo, self.hi*SCALE//y.hi)
        b = (ceildiv(self.lo*SCALE,y.lo), ceildiv(self.lo*SCALE,y.hi),
             ceildiv(self.hi*SCALE,y.lo), ceildiv(self.hi*SCALE,y.hi))
        return Box(min(a), max(b), raw=True)
    def __rtruediv__(self, other):
        return self.cast(other)/self
    def square(self):
        a = 0 if self.lo <= 0 <= self.hi else min(self.lo*self.lo,self.hi*self.hi)
        b = max(self.lo*self.lo,self.hi*self.hi)
        return Box(a//SCALE,ceildiv(b,SCALE),raw=True)
    def sqrt(self):
        if self.lo < 0:
            raise ArithmeticError('negative radicand')
        a, b = isqrt(self.lo*SCALE), isqrt(self.hi*SCALE)
        return Box(a,b+(b*b<self.hi*SCALE),raw=True)
    def clip(self, lo, hi=None):
        a = self.cast(lo).lo
        b = self.hi if hi is None else self.cast(hi).hi
        return Box(max(self.lo,a),min(self.hi,b),raw=True)
    def endpoints(self):
        return [str(Fraction(self.lo,SCALE)), str(Fraction(self.hi,SCALE))]

