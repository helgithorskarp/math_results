"""Fraction-endpoint recomputation of the complete dyadic enclosure record.

The equations and Taylor jet are shared with the main calculation. Products,
reciprocals and input rounding are independently evaluated as exact rational
endpoint operations, then rounded to the same fixed grid. This is an arithmetic
cross-check by the same author, not an independent review or second proof.
"""
from fractions import Fraction as F
from math import isqrt

import interval as iv
import bounds


Original=iv.I


def floor(value):
    return value.numerator//value.denominator


def ceil(value):
    quotient,remainder=divmod(value.numerator,value.denominator)
    return quotient+int(remainder!=0)


class R(Original):
    def __init__(self,value=0):
        if isinstance(value,Original):
            self.lo,self.hi=value.lo,value.hi
        else:
            iv.require(not isinstance(value,float),'reference rejects floating input')
            value=F(value)*iv.DEN
            self.lo,self.hi=floor(value),ceil(value)

    @classmethod
    def hull(cls,lo,hi):
        return cls.raw(floor(lo*iv.DEN),ceil(hi*iv.DEN))

    def __mul__(self,other):
        other=R(other)
        a,b=F(self.lo,iv.DEN),F(self.hi,iv.DEN)
        c,d=F(other.lo,iv.DEN),F(other.hi,iv.DEN)
        ends=[a*c,a*d,b*c,b*d]
        return R.hull(min(ends),max(ends))

    __rmul__=__mul__

    def inv(self):
        iv.require(not(self.lo<=0<=self.hi),'reference reciprocal excludes zero')
        return R.hull(1/F(self.hi,iv.DEN),1/F(self.lo,iv.DEN))

    def square(self):
        a,b=F(self.lo,iv.DEN),F(self.hi,iv.DEN)
        return R.hull(0 if a<=0<=b else min(a*a,b*b),max(a*a,b*b))

    def sqrt(self):
        iv.require(self.lo>=0,'reference square root excludes negatives')
        lower=isqrt(self.lo*iv.DEN);upper=isqrt(self.hi*iv.DEN)
        upper+=int(upper*upper<self.hi*iv.DEN)
        return R.raw(lower,upper)


def recompute(values,jac,Y,invB):
    saved=(iv.I,iv.ZERO,iv.ONE,iv.GZERO,bounds.I)
    try:
        iv.I=R;iv.ZERO=R(0);iv.ONE=R(1);iv.GZERO=(iv.ZERO,)*6;bounds.I=R
        return bounds.certify(values,jac,Y,invB)
    finally:
        iv.I,iv.ZERO,iv.ONE,iv.GZERO,bounds.I=saved
