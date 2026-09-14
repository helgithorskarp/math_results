"""Exact multiquadratic field; no floating point or external algebra system."""
from fractions import Fraction as F
from functools import lru_cache
from math import isqrt

def add(a,b):return tuple(x+y for x,y in zip(a,b,strict=True))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def scale(a,s):return tuple(x*s for x in a)

class Field:
    def __init__(self,radicals=(3,5,11)):
        self.radicals=tuple(radicals)
        self.sqrt=lru_cache(None)(self._sqrt)
    def mul(self,a,b):
        n=len(a)
        if n!=len(b):raise ValueError('field dimensions')
        if n==1:return (a[0]*b[0],)
        h=n//2;d=self.radicals[n.bit_length()-2]
        x,y=a[:h],a[h:];u,v=b[:h],b[h:]
        return add(self.mul(x,u),scale(self.mul(y,v),d))+add(self.mul(x,v),self.mul(y,u))
    def inv(self,a):
        if len(a)==1:
            if not a[0]:raise ZeroDivisionError
            return (1/F(a[0]),)
        h=len(a)//2;d=self.radicals[len(a).bit_length()-2];x,y=a[:h],a[h:]
        q=self.inv(sub(self.mul(x,x),scale(self.mul(y,y),d)))
        return self.mul(x,q)+neg(self.mul(y,q))
    def div(self,a,b):return self.mul(a,self.inv(b))
    def _sqrt(self,a):
        """Return a root in this real field, or None after exhaustive recursion."""
        if not any(a):return a
        n=len(a)
        if n==1:
            q=F(a[0])
            if q<0:return None
            p,r=isqrt(q.numerator),isqrt(q.denominator)
            return (F(p,r),) if p*p==q.numerator and r*r==q.denominator else None
        h=n//2;d=self.radicals[n.bit_length()-2];A,B=a[:h],a[h:];zero=(F(0),)*h
        if not any(B):
            x=self.sqrt(A)
            if x is not None:return x+zero
            y=self.sqrt(scale(A,F(1,d)))
            return zero+y if y is not None else None
        t=self.sqrt(sub(self.mul(A,A),scale(self.mul(B,B),d)))
        if t is None:return None
        for u in (t,neg(t)):
            x=self.sqrt(scale(add(A,u),F(1,2)))
            if x is not None and any(x):
                y=self.div(B,scale(x,2));r=x+y
                if self.mul(r,r)==a:return r
        return None
