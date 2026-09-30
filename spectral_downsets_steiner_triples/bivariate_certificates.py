"""Small exact Q(v,l) arithmetic; coefficient cross-multiplication, no CAS.

Sparse polynomial dictionaries map (v exponent,l exponent) to Fraction.
No numerical sampling, polynomial GCD or inferred denominator sign. Explicit
shifted coefficient certificates supply signs in lambda_identities.py.
Author: six-downset-2, researcher.
"""
from fractions import Fraction as F
from math import comb


def poly(value):
    if isinstance(value, dict):
        return {p: F(c) for p,c in value.items() if c}
    return {(0,0):F(value)} if value else {}


def add(a,b):
    out=a.copy()
    for p,c in b.items():out[p]=out.get(p,F(0))+c
    return {p:c for p,c in out.items() if c}


def multiply(a,b):
    out={}
    for (i,j),x in a.items():
        for (k,l),y in b.items():
            p=(i+k,j+l)
            out[p]=out.get(p,F(0))+x*y
    return {p:c for p,c in out.items() if c}


class RF:
    def __init__(self,numerator,denominator=1):
        self.n,self.d=poly(numerator),poly(denominator)
        assert self.d
        if not self.n:self.d=poly(1)
        elif set(self.d)=={(0,0)}:
            scale=self.d[(0,0)]
            self.n={p:c/scale for p,c in self.n.items()}
            self.d=poly(1)

    @staticmethod
    def coerce(value):return value if isinstance(value,RF) else RF(value)

    def __add__(self,other):
        other=self.coerce(other)
        if not self.n:return other
        if not other.n:return self
        return RF(add(multiply(self.n,other.d),multiply(other.n,self.d)),multiply(self.d,other.d))

    __radd__=__add__

    def __neg__(self):return RF({p:-c for p,c in self.n.items()},self.d)

    def __sub__(self,other):return self+-self.coerce(other)

    def __rsub__(self,other):return self.coerce(other)+-self

    def __mul__(self,other):
        other=self.coerce(other)
        return RF(multiply(self.n,other.n),multiply(self.d,other.d))

    __rmul__=__mul__

    def __truediv__(self,other):
        other=self.coerce(other)
        assert other.n
        return RF(multiply(self.n,other.d),multiply(self.d,other.n))

    def __rtruediv__(self,other):return self.coerce(other)/self

    def __pow__(self,exponent):
        assert isinstance(exponent,int) and exponent>=0
        out=RF(1)
        for _ in range(exponent):out*=self
        return out

    def is_zero(self):return not self.n

    def substitute_l(self,value):
        def sub(p):
            out={}
            for (i,j),c in p.items():out[(i,0)]=out.get((i,0),F(0))+c*F(value)**j
            return poly(out)
        return RF(sub(self.n),sub(self.d))


def shifted(p,domain='base'):
    """base: v=13+x,l=2+y; cap: v=24l+x,l=2+y; x,y>=0."""
    assert domain in ('base','cap')
    out={}
    for (pv,pl),c in p.items():
        for i in range(pv+1):
            if domain=='base':
                power=pl
                factor=comb(pv,i)*13**(pv-i)
            else:
                power=pv-i+pl
                factor=comb(pv,i)*24**(pv-i)
            for j in range(power+1):
                key=(i,j)
                out[key]=out.get(key,F(0))+c*factor*comb(power,j)*2**(power-j)
    return poly(out)


def positive(p,domain='base'):
    out=shifted(p,domain)
    assert out.get((0,0),F(0))>0
    assert all(c>=0 for c in out.values())
    return out


def terms(p):return [[i,j,str(c)] for (i,j),c in sorted(p.items())]
