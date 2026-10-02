"""Whole-cell two-variable mean-value G22 model.

No necessary-feasible-subset clipping is used here.  Every differentiated
expression and square-root branch is defined on the entire closed box.
Actual author: six-tammes-2, researcher.
"""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json,signal,sys,time
from dependency import e
I,S=e.I,e.S

def intersect(a,b):
    lo,hi=max(a.l,b.l),min(a.h,b.h)
    if lo>hi:raise ArithmeticError('inconsistent whole-cell mean-value enclosure')
    return I.raw(lo,hi)

class D2:
    rt=Q(0);rz=Q(0)
    def __init__(self,v=0,dt=0,dz=0,c=None):
        self.v,self.dt,self.dz=I.cv(v),I.cv(dt),I.cv(dz)
        self.c=self.v if c is None else I.cv(c)
        if D2.rt or D2.rz:
            et=I.raw(-max(abs(self.dt.l),abs(self.dt.h)),max(abs(self.dt.l),abs(self.dt.h)))*I(D2.rt)
            ez=I.raw(-max(abs(self.dz.l),abs(self.dz.h)),max(abs(self.dz.l),abs(self.dz.h)))*I(D2.rz)
            self.v=intersect(self.v,self.c+et+ez)
    @staticmethod
    def cv(x):return x if isinstance(x,D2) else D2(x)
    def __add__(self,x):
        x=D2.cv(x);return D2(self.v+x.v,self.dt+x.dt,self.dz+x.dz,self.c+x.c)
    __radd__=__add__
    def __neg__(self):return D2(-self.v,-self.dt,-self.dz,-self.c)
    def __sub__(self,x):return self+-D2.cv(x)
    def __rsub__(self,x):return D2.cv(x)+-self
    def __mul__(self,x):
        x=D2.cv(x)
        return D2(self.v*x.v,self.dt*x.v+self.v*x.dt,self.dz*x.v+self.v*x.dz,self.c*x.c)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=D2.cv(x)
        return D2(self.v/x.v,(self.dt*x.v-self.v*x.dt)/(x.v**2),
                  (self.dz*x.v-self.v*x.dz)/(x.v**2),self.c/x.c)
    def __rtruediv__(self,x):return D2.cv(x)/self
    def __pow__(self,n):
        e.require(type(n)is int and n>=0,'nonnegative integral power')
        if n==2:return D2(self.v**2,2*self.v*self.dt,2*self.v*self.dz,self.c**2)
        v=D2(1)
        for _ in range(n):v=v*self
        return v
    def sqrt(self):
        if self.v.l<=0:raise ArithmeticError('whole-cell strict square-root domain unresolved')
        value=self.v.sqrt()
        return D2(value,self.dt/(2*value),self.dz/(2*value),self.c.sqrt())

def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def dot(a,b,t):return (1-t)*sum(x*y for x,y in zip(a,b))+t*sum(a)*sum(b)
def him(a,t):return [x/(1-t)-t*sum(a)/((1-t)*(1+2*t)) for x in a]

def preframe(t,z):
    D=(1-t)**2*(1+2*t);r=2*t/(1+t)
    k=t*(9*t*t-2*t-3)/(1+t)**2
    gam=k/(1+k)
    mu=(t-1)*(t+1)*(2*t+1)*(3*t-1)/((1+t)**2*(1+k))
    den=(2*r-1)*(r+1)
    cv=type(t)
    B={i:[cv(1 if j==s else 0) for j in range(3)] for s,i in enumerate((1,2,4))}
    for n,i,j,o in ((8,2,4,1),(10,1,2,4),(12,1,10,2),(13,2,8,4)):
        B[n]=[r*(a+b)-c for a,b,c in zip(B[i],B[j],B[o])]
    C=1+D*z**2;d=him(cross(B[12],B[1]),t)
    W=[t*a+(D*z**2-1)/C*(b-t*a)+2*D*z/C*v for a,b,v in zip(B[12],B[1],d)]
    s=(D*(t*z**2-2*z)+t*(2*t-1))/C
    de=1-s**2
    g=de-k**2-t**2+2*s*k*t
    return B,W,s,g,k,gam,mu,den,D,r,de

def model(t,z):
    B,W,s,g,k,gam,mu,den,D,r,de=preframe(t,z)
    radical=(D*g).sqrt();normal=him(cross(W,B[10]),t)
    V=[((k-s*t)*a+(t-s*k)*b-radical*n)/de for a,b,n in zip(W,B[10],normal)]
    U=[gam*(a+b)+mu*n for a,b,n in zip(W,V,him(cross(W,V),t))]
    P=dict(B);P.update({6:U,7:W,9:V})
    for label,co in ((0,(r,r,1-r)),(5,(1-r,r,r)),(11,(r,1-r,r))):
        P[label]=[sum(a*v[j] for a,v in zip(co,(U,W,V)))/den for j in range(3)]
    return P,g,de

def cell(td,ti,zd,zi):
    tl=Q(14,25)+Q(33,1000)*ti/2**td;th=tl+Q(33,1000)/2**td
    zl=Q(-5,2)+Q(5)*zi/2**zd;zh=zl+Q(5)/2**zd
    return tl,th,zl,zh

def enclosed(left,right,a,b):
    # This preflight is UNCONDITIONAL, without clipping to packing facts.
    raw=preframe(I(left,right),I(a,b))
    g,de=raw[3],raw[-1]
    if g.l<=0 or de.l<=0:raise ArithmeticError('raw whole-box regularity unresolved')
    D2.rt,D2.rz=(right-left)/2,(b-a)/2
    t=D2(I(left,right),1,0,I((left+right)/2))
    z=D2(I(a,b),0,1,I((a+b)/2))
    P,gd,dd=model(t,z)
    return P,t,{'raw_g':g,'raw_de':de,'centered_g':gd.v,'centered_de':dd.v}

def pair_gap(P,t,pair):return dot(P[pair[0]],P[pair[1]],t)-t
def enc(v):return [str(Q(v.l,S)),str(Q(v.h,S))]
