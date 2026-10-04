"""separate closed aggregate forms and conservative bidegrees.

No imports from the producer, recipe, physical sector module or polynomial
engine. Actual evaluation uses exact Fractions; the same expressions also
propagate rigorous numerator/denominator bidegree bounds without guessing
cancelled factors. This is same-author checking, not independent review.
"""
from fractions import Fraction as F

def require(ok,msg):
    if not ok:raise ValueError(msg)

def add_degree(a,b):
    return None if a is None or b is None else tuple(x+y for x,y in zip(a,b))
def max_degree(a,b):
    if a is None:return b
    if b is None:return a
    return tuple(max(x,y) for x,y in zip(a,b))

class Degree:
    def __init__(self,value=0,numerator=None,denominator=(0,0)):
        if isinstance(value,Degree):self.n,self.d=value.n,value.d;return
        self.n=numerator if numerator is not None else (0,0) if value else None
        self.d=denominator
    def __neg__(self):return Degree(1,self.n,self.d) if self.n is not None else Degree()
    def __add__(self,other):
        other=Degree(other)
        if self.n is None:return other
        if other.n is None:return self
        return Degree(1,max_degree(add_degree(self.n,other.d),add_degree(other.n,self.d)),add_degree(self.d,other.d))
    __radd__=__add__
    def __sub__(self,other):return self+-Degree(other)
    def __rsub__(self,other):return Degree(other)+-self
    def __mul__(self,other):
        other=Degree(other)
        if self.n is None or other.n is None:return Degree()
        return Degree(1,add_degree(self.n,other.n),add_degree(self.d,other.d))
    __rmul__=__mul__
    def __truediv__(self,other):
        other=Degree(other);require(other.n is not None,'nonzero divisor in conservative degree expression')
        if self.n is None:return Degree()
        return Degree(1,add_degree(self.n,other.d),add_degree(self.d,other.n))
    def __rtruediv__(self,other):return Degree(other)/self
    def __pow__(self,n):
        require(type(n) is int and n>=0,'nonnegative degree exponent')
        out=Degree(1)
        for _ in range(n):out=out*self
        return out


# Degree propagation copied from author source2252; no old forms are imported.
