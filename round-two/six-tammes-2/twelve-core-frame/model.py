"""Validated enclosures for the twelve-point G20 prefix certificates.

Actual author six-tammes-2, researcher. The arithmetic and formulas
derive from the attributed G22 kernel; label13 construction and
literal permissions are removed, while interval primitives agree.

80-bit dyadic outward rounding. Zero square-root arguments are allowed.
The necessary g>=0 and proven 1-s^2>49/625 conditions justify clipping
intervals only on the feasible subset of a parameter rectangle.
"""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import json,signal,sys,time
S=1<<80
def require(ok,message):
    if not ok:raise ValueError(message)
class I:
    def __init__(self,a=0,b=None):
        a,b=Q(a),Q(a if b is None else b);require(a<=b,'ordered endpoints')
        self.l=a.numerator*S//a.denominator;self.h=-((-b.numerator*S)//b.denominator)
    @classmethod
    def raw(cls,l,h):
        require(l<=h,'ordered raw endpoints');v=object.__new__(cls);v.l,v.h=l,h;return v
    @staticmethod
    def cv(v):return v if isinstance(v,I) else I(v)
    def __add__(self,v):
        v=I.cv(v);return I.raw(self.l+v.l,self.h+v.h)
    __radd__=__add__
    def __neg__(self):return I.raw(-self.h,-self.l)
    def __sub__(self,v):return self+-I.cv(v)
    def __rsub__(self,v):return I.cv(v)+-self
    def __mul__(self,v):
        v=I.cv(v);rows=[a*b for a in (self.l,self.h) for b in (v.l,v.h)]
        return I.raw(min(rows)//S,-((-max(rows))//S))
    __rmul__=__mul__
    def __truediv__(self,v):
        v=I.cv(v)
        if v.l<=0<=v.h:raise ArithmeticError('interval denominator contains zero')
        rows=[Q(a*S,b) for a in (self.l,self.h) for b in (v.l,v.h)]
        low,high=min(rows),max(rows)
        return I.raw(low.numerator//low.denominator,-((-high.numerator)//high.denominator))
    def __rtruediv__(self,v):return I.cv(v)/self
    def __pow__(self,n):
        require(type(n)is int and n>=0,'nonnegative integral power')
        if n==2:
            a=min(self.l*self.l,self.h*self.h) if not self.l<=0<=self.h else 0
            b=max(self.l*self.l,self.h*self.h)
            return I.raw(a//S,-((-b)//S))
        v=I(1)
        for _ in range(n):v=v*self
        return v
    def sqrt(self):
        require(self.l>=0,'nonnegative square-root argument')
        low=isqrt(self.l*S);high=isqrt(self.h*S)
        if high*high<self.h*S:high+=1
        return I.raw(low,high)
def clip(a,b):
    low,high=max(a.l,b.l),min(a.h,b.h)
    if low>high:raise ArithmeticError('empty necessary intersection')
    return I.raw(low,high)
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def dot(a,b,t):return (1-t)*sum((x*y for x,y in zip(a,b)),I())+t*sum(a,I())*sum(b,I())
def him(a,t):return [x/(1-t)-t*sum(a,I())/((1-t)*(1+2*t)) for x in a]
CONTACTS={(5, 7), (0, 5), (9, 11), (10, 12), (0, 11), (2, 8), (1, 12), (6, 11), (4, 8), (5, 9), (9, 10), (0, 7), (2, 4), (1, 2), (2, 10), (7, 12), (5, 11), (1, 4), (0, 6), (1, 10)}
PAIRS=[(6, 8), (0, 1), (0, 2), (0, 4), (0, 8), (0, 10), (0, 12), (5, 1), (5, 2), (5, 4), (5, 8), (5, 10), (5, 12), (6, 1), (6, 2), (6, 4), (6, 10), (6, 12), (7, 2), (7, 4), (7, 8), (7, 10), (9, 1), (9, 2), (9, 4), (9, 8), (9, 12), (11, 1), (11, 2), (11, 4), (11, 8), (11, 10), (11, 12)]
def frame(t,z,epsilon,eta):
    D=(1-t)**2*(1+2*t);r=2*t/(1+t)
    k=clip(t*(9*t*t-2*t-3)/(1+t)**2,I(Q(-3,10),Q(-1,5)))
    gam=k/(1+k)
    mu=(t-1)*(t+1)*(2*t+1)*(3*t-1)/((1+t)**2*(1+k))
    den=(2*r-1)*(r+1)
    B={i:[I(1 if j==s else 0) for j in range(3)] for s,i in enumerate((1,2,4))}
    for n,i,j,o in ((8,2,4,1),(10,1,2,4),(12,1,10,2)):B[n]=[r*(a+b)-c for a,b,c in zip(B[i],B[j],B[o])]
    C=1+D*z**2;d=him(cross(B[12],B[1]),t)
    W=[t*a+(D*z**2-1)/C*(b-t*a)+2*D*z/C*v for a,b,v in zip(B[12],B[1],d)]
    s=clip((D*(t*z**2-2*z)+t*(2*t-1))/C,I(Q(-24,25),Q(7,10)))
    g=1-s**2-k**2-t**2+2*s*k*t
    return B,W,s,g,k,gam,mu,den,D,r
def verify_witness(t,z,epsilon,eta,mode,instruction):
    kind=instruction[0]
    if instruction==['chart']:return ((1-t)**2*z**2-1).l>0
    try:B,W,s,g,k,gam,mu,den,D,r=frame(t,z,epsilon,eta)
    except ArithmeticError as error:
        return instruction==['empty-necessary-intersection'] and str(error)=='empty necessary intersection'
    if instruction==['empty-necessary-intersection']:return False
    if instruction==['no-real-V']:return g.h<0
    if instruction==['outside-target-g-half']:return mode=='g-half' and g.l>S//2
    if kind=='W-pair':
        require(len(instruction)==3 and instruction[1]==7 and instruction[2] in (1,2,4,8,10),'specified W packing pair')
        j=instruction[2]
        return (s-t if j==10 else dot(W,B[j],t)-t).l>0
    require(kind=='pair' and len(instruction)==3 and tuple(instruction[1:]) in PAIRS,'specified intercluster pair')
    if g.h<0:return False
    try:
        g=I.raw(max(0,g.l),g.h)
        de=clip(1-s**2,I(Q(49,625),1))
        radical=(D*g).sqrt();normal=him(cross(W,B[10]),t)
        V=[((k-s*t)*a+(t-s*k)*b+epsilon*radical*n)/de for a,b,n in zip(W,B[10],normal)]
        U=[gam*(a+b)+eta*mu*n for a,b,n in zip(W,V,him(cross(W,V),t))]
        P={6:U,7:W,9:V}
        for label,co in ((0,(r,r,1-r)),(5,(1-r,r,r)),(11,(r,1-r,r))):
            P[label]=[sum((a*v[j] for a,v in zip(co,(U,W,V))),I())/den for j in range(3)]
        i,j=instruction[1:]
        return dot(P[i],B[j],t).l>t.h
    except ArithmeticError:return False

def box(td,ti,zd,zi):
    lo,hi=Q(14,25),Q(593,1000);width=(hi-lo)/2**td
    za,zb=Q(-5,2),Q(5,2);zw=(zb-za)/2**zd
    return I(lo+ti*width,lo+(ti+1)*width),I(za+zi*zw,za+(zi+1)*zw)
