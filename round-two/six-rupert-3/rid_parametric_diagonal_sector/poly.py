"""Exact two-variable polynomial utilities over the pinned ordered field.
No sampled sign decisions: tensor Bernstein convex-hull bounds certify boxes.
"""
from math import comb
from fractions import Fraction as Q

class P:
    F=None
    def __init__(self,data=0):
        if isinstance(data,P):data=data.c
        if not isinstance(data,dict):data={(0,0):self.F.coerce(data)}
        Z=self.F(0);self.c={k:self.F.coerce(v) for k,v in data.items() if self.F.coerce(v)!=Z}
    def __add__(self,b):
        b=P(b);d=dict(self.c)
        for k,v in b.c.items():d[k]=d.get(k,self.F(0))+v
        return P(d)
    __radd__=__add__
    def __neg__(self):return P({k:-v for k,v in self.c.items()})
    def __sub__(self,b):return self+-P(b)
    def __rsub__(self,b):return P(b)+-self
    def __mul__(self,b):
        b=P(b);d={}
        for (i,j),v in self.c.items():
            for (k,l),w in b.c.items():d[i+k,j+l]=d.get((i+k,j+l),self.F(0))+v*w
        return P(d)
    __rmul__=__mul__
    def __truediv__(self,b):return P({k:v/self.F.coerce(b) for k,v in self.c.items()})
    def __pow__(self,n):
        if not isinstance(n,int) or n<0:raise ValueError('nonnegative integer power required')
        a=P(1)
        for _ in range(n):a*=self
        return a
    def __eq__(self,b):return self.c==P(b).c
    def __bool__(self):return bool(self.c)
    def evaluate(self,u,v):
        return sum((a*self.F.coerce(u)**i*self.F.coerce(v)**j for (i,j),a in self.c.items()),self.F(0))
    def order_u(self):return min((i for i,j in self.c),default=999)
    def cancel_u(self,n):
        if self.order_u()<n:raise ValueError('polynomial numerator lacks common u factor')
        return P({(i-n,j):a for (i,j),a in self.c.items()})
    def encode(self):return [{'powers':[i,j],'coefficient':a.encode()} for (i,j),a in sorted(self.c.items())]
    def bounds(self,box):
        lu,hu,lv,hv=map(self.F.coerce,box);power={}
        if not(lu<hu and lv<hv):raise ValueError('nondegenerate ordered box required')
        for (i,j),a in self.c.items():
            for k in range(i+1):
                for l in range(j+1):
                    key=(k,l);b=a*comb(i,k)*lu**(i-k)*(hu-lu)**k*comb(j,l)*lv**(j-l)*(hv-lv)**l
                    power[key]=power.get(key,self.F(0))+b
        m=max((i for i,j in self.c),default=0);n=max((j for i,j in self.c),default=0)
        values=[]
        for k in range(m+1):
            for l in range(n+1):
                values.append(sum((a*Q(comb(k,i),comb(m,i))*Q(comb(l,j),comb(n,j)) for (i,j),a in power.items() if i<=k and j<=l),self.F(0)))
        # Independently re-expand the Bernstein basis in ordinary powers.
        # A wrong conversion cannot be accepted merely because its minima pass.
        reconstructed={}
        for k in range(m+1):
            for l in range(n+1):
                a=values[k*(n+1)+l]*comb(m,k)*comb(n,l)
                for i in range(k,m+1):
                    for j in range(l,n+1):
                        t=a*comb(m-k,i-k)*comb(n-l,j-l)*((-1)**(i-k+j-l))
                        reconstructed[i,j]=reconstructed.get((i,j),self.F(0))+t
        clean=lambda d:{key:a for key,a in d.items() if a!=self.F(0)}
        if clean(reconstructed)!=clean(power):raise ValueError('Bernstein polynomial identity differs')
        return min(values),max(values),values

def dot(a,b):return sum((P(x)*P(y) for x,y in zip(a,b)),P(0))
def cross(a,b):
    a=tuple(map(P,a));b=tuple(map(P,b))
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def determinant(a,b,c):return dot(a,cross(b,c))
