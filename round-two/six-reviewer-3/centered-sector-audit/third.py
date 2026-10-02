"""Full symmetric third derivative tensors, built on this reviewer's prior D2.

Derivatives are literal derivatives, not Taylor coefficients. All triples of
the seven axes are retained, including every purely parameter triple.
"""
from fractions import Fraction as F
from exact_numbers import D,need


class T:
    def __init__(self,v=0,third=None):
        if isinstance(v,T):self.base=v.base;self.t=dict(v.t)
        else:self.base=D(v);self.t={} if third is None else third
    @property
    def v(self):return self.base.v
    @property
    def g(self):return self.base.g
    @property
    def h(self):return self.base.h
    @classmethod
    def variable(cls,v,axis):return cls(D.variable(v,axis))
    def __add__(self,b):
        b=T(b);t=dict(self.t)
        for ijk,x in b.t.items():t[ijk]=t.get(ijk,0)+x
        return T(self.base+b.base,{i:x for i,x in t.items() if x!=0})
    __radd__=__add__
    def __neg__(self):return T(-self.base,{i:-x for i,x in self.t.items()})
    def __sub__(self,b):return self+-T(b)
    def __rsub__(self,b):return T(b)+-self
    def __mul__(self,b):
        b=T(b);t={}
        for ijk,x in self.t.items():t[ijk]=x*b.v
        for ijk,x in b.t.items():t[ijk]=t.get(ijk,0)+self.v*x
        # For a stored Hessian pair and gradient axis k, the coefficient is
        # the multiplicity of k in the triple: 1, 2 or 3 as appropriate.
        for left,right in ((self,b),(b,self)):
            for ij,x in left.h.items():
                for k,y in right.g.items():
                    ijk=tuple(sorted((*ij,k)))
                    t[ijk]=t.get(ijk,0)+ijk.count(k)*x*y
        return T(self.base*b.base,{i:x for i,x in t.items() if x!=0})
    __rmul__=__mul__
    def __pow__(self,n):
        need(type(n)is int and n>=0,'nonnegative third tensor power');out=T(1)
        for _ in range(n):out*=self
        return out
    def __truediv__(self,b):
        need(not isinstance(b,T),'third tensor division only by rational constant');return self*(F(1)/F(b))
