"""Fixed192-bit outward dyadic intervals and eta/parameter Taylor jets.

Every endpoint is an integer divided by2^192. Integer floor/ceiling gives
outward rounding. No floating-point arithmetic is used in any enclosure.
The jet retains eta degrees0,1,2 and six parameter derivatives through
eta degree2. The new six mixed components carry partial_eta^2 partial_v /2.
Copied from source7bb2d1b6cf6cb3b370ad10023bee018128a1b81f; extended by
six-sendov-3 for the centered-real sector, not the scalar symmetric sector.
"""
from fractions import Fraction
from math import isqrt

BITS=192
DEN=1<<BITS


class EnclosureError(RuntimeError):
    pass


def require(ok,label):
    if not ok:
        raise EnclosureError(label)


class I:
    __slots__=('lo','hi')

    def __init__(self,value=0):
        if isinstance(value,I):
            self.lo,self.hi=value.lo,value.hi
        else:
            require(not isinstance(value,float),'floating-point input forbidden')
            v=Fraction(value)
            num=v.numerator*DEN
            self.lo=num//v.denominator
            self.hi=-((-num)//v.denominator)

    @classmethod
    def raw(cls,lo,hi):
        require(lo<=hi,'ordered interval endpoints')
        obj=object.__new__(cls);obj.lo=lo;obj.hi=hi
        return obj

    @classmethod
    def bounds(cls,lo,hi):
        return cls.raw(I(lo).lo,I(hi).hi)

    def __add__(self,other):
        other=I(other)
        return I.raw(self.lo+other.lo,self.hi+other.hi)

    __radd__=__add__

    def __neg__(self):
        return I.raw(-self.hi,-self.lo)

    def __sub__(self,other):
        return self+-I(other)

    def __rsub__(self,other):
        return I(other)+-self

    def __mul__(self,other):
        other=I(other)
        if self.lo==self.hi==0 or other.lo==other.hi==0:
            return ZERO
        if self.lo==self.hi==DEN:
            return other
        if other.lo==other.hi==DEN:
            return self
        ends=(self.lo*other.lo,self.lo*other.hi,self.hi*other.lo,self.hi*other.hi)
        return I.raw(min(ends)//DEN,-((-max(ends))//DEN))

    __rmul__=__mul__

    def __pow__(self,n):
        require(isinstance(n,int) and n>=0,'nonnegative interval power')
        result=ONE;base=self
        while n:
            if n&1:
                result*=base
            n>>=1
            if n:
                base*=base
        return result

    def square(self):
        upper=max(self.lo*self.lo,self.hi*self.hi)
        lower=0 if self.lo<=0<=self.hi else min(self.lo*self.lo,self.hi*self.hi)
        return I.raw(lower//DEN,-((-upper)//DEN))

    def inv(self):
        require(not(self.lo<=0<=self.hi),'reciprocal excludes zero')
        return I.raw(DEN*DEN//self.hi,-((-DEN*DEN)//self.lo))

    def __truediv__(self,other):
        return self*I(other).inv()

    def __rtruediv__(self,other):
        return I(other)*self.inv()

    def sqrt(self):
        require(self.lo>=0,'nonnegative square-root interval')
        low=isqrt(self.lo*DEN);high=isqrt(self.hi*DEN)
        if high*high<self.hi*DEN:
            high+=1
        return I.raw(low,high)

    def absmax(self):
        return max(abs(self.lo),abs(self.hi))

    def __eq__(self,other):
        other=I(other)
        return self.lo==other.lo and self.hi==other.hi

    def record(self):
        return [str(Fraction(self.lo,DEN)),str(Fraction(self.hi,DEN))]


ZERO=I(0);ONE=I(1);GZERO=(ZERO,)*6


class J:
    __slots__=('f','g','constant')

    def __init__(self,value=0):
        if isinstance(value,J):
            self.f,self.g,self.constant=value.f,value.g,value.constant
        else:
            self.f=(I(value),ZERO,ZERO)
            self.g=(GZERO,GZERO,GZERO)
            self.constant=True

    @classmethod
    def raw(cls,f,g):
        obj=object.__new__(cls);obj.f=tuple(f);obj.g=tuple(tuple(row) for row in g)
        obj.constant=all(v==0 for v in (*obj.f[1:],*obj.g[0],*obj.g[1],*obj.g[2]))
        return obj

    @classmethod
    def eta(cls,value):
        return cls.raw((I(value),ONE,ZERO),(GZERO,GZERO,GZERO))

    @classmethod
    def parameter(cls,value,index):
        gradient=tuple(ONE if j==index else ZERO for j in range(6))
        return cls.raw((I(value),ZERO,ZERO),(gradient,GZERO,GZERO))

    def __add__(self,other):
        other=J(other)
        return J.raw([a+b for a,b in zip(self.f,other.f)],
                     [[a+b for a,b in zip(x,y)] for x,y in zip(self.g,other.g)])

    __radd__=__add__

    def __neg__(self):
        return J.raw([-a for a in self.f],[[-v for v in row] for row in self.g])

    def __sub__(self,other):
        return self+-J(other)

    def __rsub__(self,other):
        return J(other)+-self

    def __mul__(self,other):
        other=J(other)
        if self.constant:
            s=self.f[0]
            return J.raw([s*v for v in other.f],[[s*v for v in row] for row in other.g])
        if other.constant:
            s=other.f[0]
            return J.raw([s*v for v in self.f],[[s*v for v in row] for row in self.g])
        a,b=self.f,other.f;ga,gb=self.g,other.g
        f=[a[0]*b[0],a[1]*b[0]+a[0]*b[1],a[2]*b[0]+a[1]*b[1]+a[0]*b[2]]
        g0=[ga[0][i]*b[0]+a[0]*gb[0][i] for i in range(6)]
        g1=[ga[1][i]*b[0]+ga[0][i]*b[1]+a[1]*gb[0][i]+a[0]*gb[1][i] for i in range(6)]
        g2=[ga[2][i]*b[0]+ga[1][i]*b[1]+ga[0][i]*b[2]+a[2]*gb[0][i]+a[1]*gb[1][i]+a[0]*gb[2][i] for i in range(6)]
        return J.raw(f,[g0,g1,g2])

    __rmul__=__mul__

    def __pow__(self,n):
        require(isinstance(n,int) and n>=0,'nonnegative jet power')
        result=J(1);base=self
        while n:
            if n&1:
                result*=base
            n>>=1
            if n:
                base*=base
        return result


class C:
    __slots__=('re','im')

    def __init__(self,re=0,im=0):
        if isinstance(re,C):
            self.re,self.im=re.re,re.im
        else:
            self.re,self.im=I(re),I(im)

    def __add__(self,other):
        other=C(other)
        return C(self.re+other.re,self.im+other.im)

    __radd__=__add__

    def __neg__(self):
        return C(-self.re,-self.im)

    def __sub__(self,other):
        return self+-C(other)

    def __mul__(self,other):
        other=C(other)
        return C(self.re*other.re-self.im*other.im,self.re*other.im+self.im*other.re)

    __rmul__=__mul__

    def conj(self):
        return C(self.re,-self.im)

    def inv(self):
        denominator=self.re.square()+self.im.square()
        return C(self.re/denominator,-self.im/denominator)

    def __truediv__(self,other):
        return self*C(other).inv()


def evaluate(poly,z):
    result=type(z)(0)
    for coefficient in reversed(poly):
        result=result*z+coefficient
    return result
