"""Separate exact field jet specialization at the incumbent chart.

Ascending coefficient vectors in Q[T]/F with a distinguished real root.
The t,z derivatives are taken before specializing; the quotient arithmetic
only reduces their evaluated values. No derivative of F(T)=0 is imposed.
"""
from fractions import Fraction as Q
import field as f

def scalar(x):return x if isinstance(x,tuple) else f.scalar(Q(x))
def power(x,n):
    v=f.ONE
    for _ in range(n):v=f.mul(v,x)
    return v
class E:
    positive_root=None
    def __init__(self,v=0,dt=0,dz=0):self.v=scalar(v);self.dt=scalar(dt);self.dz=scalar(dz)
    @staticmethod
    def cv(x):return x if isinstance(x,E) else E(x)
    def __add__(self,x):
        x=E.cv(x);return E(f.add(self.v,x.v),f.add(self.dt,x.dt),f.add(self.dz,x.dz))
    __radd__=__add__
    def __neg__(self):return E(f.scale(self.v,-1),f.scale(self.dt,-1),f.scale(self.dz,-1))
    def __sub__(self,x):return self+-E.cv(x)
    def __rsub__(self,x):return E.cv(x)+-self
    def __mul__(self,x):
        x=E.cv(x);return E(f.mul(self.v,x.v),f.add(f.mul(self.dt,x.v),f.mul(self.v,x.dt)),f.add(f.mul(self.dz,x.v),f.mul(self.v,x.dz)))
    __rmul__=__mul__
    def __truediv__(self,x):
        x=E.cv(x);inverse=f.inverse(x.v);v=f.mul(self.v,inverse)
        return E(v,f.mul(f.sub(self.dt,f.mul(v,x.dt)),inverse),f.mul(f.sub(self.dz,f.mul(v,x.dz)),inverse))
    def __rtruediv__(self,x):return E.cv(x)/self
    def __pow__(self,n):
        f.require(type(n)is int and n>=0,'nonnegative integral power')
        if n==0:return E(1)
        v=power(self.v,n);derivative=f.scale(power(self.v,n-1),n)
        return E(v,f.mul(derivative,self.dt),f.mul(derivative,self.dz))
    def sqrt(self):
        v=E.positive_root
        f.require(v is not None and f.mul(v,v)==self.v and f.sign(v)>0,'exact positive square-root specialization')
        inverse=f.inverse(f.scale(v,2))
        return E(v,f.mul(self.dt,inverse),f.mul(self.dz,inverse))
