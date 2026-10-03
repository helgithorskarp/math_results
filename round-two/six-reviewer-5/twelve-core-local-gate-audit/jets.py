"""Forward derivatives through unconstrained formulas, then exact specialization.

The interval mode covers a whole rectangle without clipping; exact mode
uses a separately derived positive radical and whole square identity.
"""
from algebra import A
from enclosure import Box

class Jet:
    __slots__=('v','d')
    def __init__(self,v,dt=0,dz=0):
        self.v=v;self.d=(v*0+dt,v*0+dz)
    def cast(self,x):return x if isinstance(x,Jet) else Jet(self.v*0+x)
    def __add__(self,x):
        y=self.cast(x);return Jet(self.v+y.v,self.d[0]+y.d[0],self.d[1]+y.d[1])
    __radd__=__add__
    def __neg__(self):return Jet(-self.v,-self.d[0],-self.d[1])
    def __sub__(self,x):return self+(-self.cast(x))
    def __rsub__(self,x):return self.cast(x)+(-self)
    def __mul__(self,x):
        y=self.cast(x);return Jet(self.v*y.v,self.d[0]*y.v+self.v*y.d[0],self.d[1]*y.v+self.v*y.d[1])
    __rmul__=__mul__
    def __truediv__(self,x):
        y=self.cast(x);den=y.v*y.v
        return Jet(self.v/y.v,(self.d[0]*y.v-self.v*y.d[0])/den,(self.d[1]*y.v-self.v*y.d[1])/den)
    def __rtruediv__(self,x):return self.cast(x)/self
    def square(self):return Jet(self.v.square() if isinstance(self.v,Box) else self.v*self.v,2*self.v*self.d[0],2*self.v*self.d[1])
    def sqrt(self,exact=None):
        if isinstance(self.v,Box):
            if self.v.lo<=0:raise ArithmeticError('strict derivative radical required')
            root=self.v.sqrt()
        else:
            if not isinstance(exact,A) or exact*exact!=self.v:raise ValueError('whole exact radical-square identity')
            root=exact
        return Jet(root,self.d[0]/(2*root),self.d[1]/(2*root))

def add(*vectors):return [sum(v[i] for v in vectors) for i in range(3)]
def scale(a,v):return [a*x for x in v]
def cross(v,w):return [v[1]*w[2]-v[2]*w[1],v[2]*w[0]-v[0]*w[2],v[0]*w[1]-v[1]*w[0]]
def dot(v,w,t):return (1-t)*sum(x*y for x,y in zip(v,w))+t*sum(v)*sum(w)
def inverse_metric(v,t):return [(x-t*sum(v)/(1+2*t))/(1-t) for x in v]

def frame(t,z,exact_root=None):
    one=t*0+1;zero=t*0;r=2*t/(1+t)
    b={1:[one,zero,zero],2:[zero,one,zero],4:[zero,zero,one]}
    b[8]=add(scale(r,add(b[2],b[4])),scale(-1,b[1]))
    b[10]=add(scale(r,add(b[1],b[2])),scale(-1,b[4]))
    b[12]=add(scale(r,add(b[1],b[10])),scale(-1,b[2]))
    determinant=(1-t).square()*(1+2*t);chart=1+determinant*z.square()
    d=inverse_metric(cross(b[12],b[1]),t)
    w=add(scale(t,b[12]),scale((determinant*z.square()-1)/chart,add(b[1],scale(-t,b[12]))),scale(2*determinant*z/chart,d))
    k=t*(9*t.square()-2*t-3)/(1+t).square();s=dot(w,b[10],t)
    g=1-s.square()-k.square()-t.square()+2*s*k*t
    radical=(determinant*g).sqrt(exact_root)
    v=scale(1/(1-s.square()),add(scale(k-s*t,w),scale(t-s*k,b[10]),scale(-radical,inverse_metric(cross(w,b[10]),t))))
    mu=(t-1)*(t+1)*(2*t+1)*(3*t-1)/((1+t).square()*(1+k))
    u=add(scale(k/(1+k),add(w,v)),scale(mu,inverse_metric(cross(w,v),t)))
    denominator=(2*r-1)*(r+1)
    b[6]=u;b[7]=w;b[9]=v
    b[0]=scale(1/denominator,add(scale(r,u),scale(r,w),scale(1-r,v)))
    b[5]=scale(1/denominator,add(scale(1-r,u),scale(r,w),scale(r,v)))
    b[11]=scale(1/denominator,add(scale(r,u),scale(1-r,w),scale(r,v)))
    return b,dict(metric_determinant=determinant,chart_denominator=chart,k=k,s=s,g=g,one_minus_s_squared=1-s.square(),chart_domain_gap=1-(1-t).square()*z.square(),original_radical=radical)
