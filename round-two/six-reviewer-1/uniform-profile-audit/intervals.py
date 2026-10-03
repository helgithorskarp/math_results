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


def scalar_receipt():
    c=physical_cosine();d=2*c*c-1;y=1/(3*(1+c));x=Q(2,3)-y
    H=14*y;k=-Q(7,18)*(1+2*c);rho=(c-5)/3;ell=k+rho
    alpha=-Q(527,360)+Q(41,90)*c+Q(13,90)*c*c;tau=ell*ell/2
    B=Q(2311,108)+Q(4934,27)*c-Q(1976,9)*c*c
    K1=B-alpha*H*H/2
    maximum=K1+(Q(43,56)*alpha+Q(9,14)*tau)*H*H
    w4=1/(c+d);w3=Q(2,3)*(7-(1-d)*w4)
    quantities={'c':c,'d':d,'e':2*d*d-1,'H':H,'alpha':alpha,'alpha_plus_tau':alpha+tau,
                'even_determinant':3*H*(c+d)/14,'one_minus_two_c':1-2*c,
                'Kmax':maximum,'Kmax_minus9':maximum-9,'10_minus_Kmax':10-maximum,
                'w3':w3,'w4':w4,'y':y,'x':x}
    for name in ('d','e','H','alpha_plus_tau','even_determinant','Kmax_minus9','10_minus_Kmax','w3','w4','x','y'):
        need(quantities[name].lo>0,'positive exact scalar '+name)
    need(alpha.hi<0 and quantities['one_minus_two_c'].hi<0,'negative exact scalar signs')
    return {k:v.record()for k,v in quantities.items()}
