"""Independent exact cubic field, rational endpoints and dense derivative tensors."""
from fractions import Fraction as F
from math import isqrt


def need(ok,label):
    if not ok:raise ValueError(label)


class K:
    def __init__(self,value=0):
        if isinstance(value,K):self.a=value.a
        elif isinstance(value,(tuple,list)):
            need(len(value)==3,'three cubic coefficients');self.a=tuple(map(F,value))
        else:self.a=(F(value),F(0),F(0))
    def __add__(self,b):
        b=K(b);return K(tuple(x+y for x,y in zip(self.a,b.a)))
    __radd__=__add__
    def __neg__(self):return K(tuple(-x for x in self.a))
    def __sub__(self,b):return self+-K(b)
    def __rsub__(self,b):return K(b)+-self
    def __mul__(self,b):
        b=K(b);v=[F(0)]*5
        for i,x in enumerate(self.a):
            for j,y in enumerate(b.a):v[i+j]+=x*y
        for i in (4,3):v[i-3]+=v[i]/8;v[i-2]+=3*v[i]/4
        return K(v[:3])
    __rmul__=__mul__
    def __pow__(self,n):
        need(type(n)is int and n>=0,'nonnegative field power');out=K(1)
        for _ in range(n):out*=self
        return out
    def inv(self):
        # Invert the multiplication matrix in the fixed three-element basis.
        columns=[(self*K(tuple(int(i==j) for i in range(3)))).a for j in range(3)]
        a,b,c=zip(*columns)
        determinant=a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
        need(determinant!=0,'nonzero cubic field divisor')
        out=K(((b[1]*c[2]-b[2]*c[1])/determinant,
               (b[2]*c[0]-b[0]*c[2])/determinant,
               (b[0]*c[1]-b[1]*c[0])/determinant))
        need(self*out==1,'literal three-basis inverse product');return out
    def __truediv__(self,b):return self*K(b).inv()
    def __rtruediv__(self,b):return K(b)*self.inv()
    def __eq__(self,b):return self.a==K(b).a
    def record(self):return list(map(str,self.a))


class I:
    def __init__(self,lo=0,hi=None):
        if isinstance(lo,I):self.lo,self.hi=lo.lo,lo.hi;return
        need(not isinstance(lo,float) and not isinstance(hi,float),'no floating interval input')
        self.lo=F(lo);self.hi=self.lo if hi is None else F(hi)
        need(self.lo<=self.hi,'ordered exact rational interval')
    def __add__(self,b):b=I(b);return I(self.lo+b.lo,self.hi+b.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,b):return self+-I(b)
    def __rsub__(self,b):return I(b)+-self
    def __mul__(self,b):
        b=I(b)
        if self==0 or b==0:return I(0)
        if self==1:return b
        if b==1:return self
        ends=[x*y for x in (self.lo,self.hi) for y in (b.lo,b.hi)];return I(min(ends),max(ends))
    __rmul__=__mul__
    def __pow__(self,n):
        need(type(n)is int and n>=0,'nonnegative interval power');out=I(1)
        for _ in range(n):out*=self
        return out
    def square(self):return I(0 if self.lo<=0<=self.hi else min(self.lo**2,self.hi**2),max(self.lo**2,self.hi**2))
    def inv(self):
        need(not self.lo<=0<=self.hi,'nonzero interval divisor');return I(1/self.hi,1/self.lo)
    def __truediv__(self,b):return self*I(b).inv()
    def __rtruediv__(self,b):return I(b)*self.inv()
    def sqrt(self):
        need(self.lo>=0,'nonnegative interval square root');scale=1<<128
        lo=isqrt((self.lo.numerator*scale*scale)//self.lo.denominator)
        hi=isqrt((self.hi.numerator*scale*scale)//self.hi.denominator)
        if F(hi*hi,scale*scale)<self.hi:hi+=1
        return I(F(lo,scale),F(hi,scale))
    def absmax(self):return max(abs(self.lo),abs(self.hi))
    def __eq__(self,b):b=I(b);return (self.lo,self.hi)==(b.lo,b.hi)
    def record(self):return [str(down(self.lo,128)),str(up(self.hi,128))]


def down(x,bits=64):
    x=F(x);scale=1<<bits;return F((x.numerator*scale)//x.denominator,scale)


def up(x,bits=64):return -down(-F(x),bits)


def embedding():
    lo,hi=F(3,4),F(1);f=lambda c:8*c**3-6*c-1
    for _ in range(112):
        m=(lo+hi)/2
        if f(m)<0:lo=m
        else:hi=m
    need(f(lo)<0<f(hi) and 24*lo*lo>6,'exact unique positive cubic embedding');return I(lo,hi)


def enclose(k,c):
    k=K(k);return k.a[0]+k.a[1]*c+k.a[2]*c.square()


class D:
    """Full gradient and symmetric Hessian (actual derivatives, not Taylor jets)."""
    def __init__(self,v=0,g=None,h=None):
        if isinstance(v,D):self.v,self.g,self.h=v.v,v.g,v.h;return
        self.v=v;self.g={} if g is None else g;self.h={} if h is None else h
    @classmethod
    def variable(cls,v,axis):return cls(v,{axis:1})
    def __add__(self,b):
        b=D(b);g=dict(self.g);h=dict(self.h)
        for i,x in b.g.items():g[i]=g.get(i,0)+x
        for i,x in b.h.items():h[i]=h.get(i,0)+x
        return D(self.v+b.v,{i:x for i,x in g.items() if x!=0},{i:x for i,x in h.items() if x!=0})
    __radd__=__add__
    def __neg__(self):return D(-self.v,{i:-x for i,x in self.g.items()},{i:-x for i,x in self.h.items()})
    def __sub__(self,b):return self+-D(b)
    def __rsub__(self,b):return D(b)+-self
    def __mul__(self,b):
        b=D(b);g={};h={}
        for i,x in self.g.items():g[i]=x*b.v
        for i,x in b.g.items():g[i]=g.get(i,0)+self.v*x
        for i,x in self.h.items():h[i]=x*b.v
        for i,x in b.h.items():h[i]=h.get(i,0)+self.v*x
        for i,x in self.g.items():
            for j,y in b.g.items():
                ij=tuple(sorted((i,j)));h[ij]=h.get(ij,0)+(2 if i==j else 1)*x*y
        return D(self.v*b.v,{i:x for i,x in g.items() if x!=0},{i:x for i,x in h.items() if x!=0})
    __rmul__=__mul__
    def __pow__(self,n):
        need(type(n)is int and n>=0,'nonnegative tensor power');out=D(1)
        for _ in range(n):out*=self
        return out
    def __truediv__(self,b):
        need(not isinstance(b,D),'tensor division only by constant rational');return self*(F(1)/F(b))


class Z:
    def __init__(self,re=0,im=0):
        if isinstance(re,Z):self.re,self.im=re.re,re.im
        else:self.re,self.im=I(re),I(im)
    def __add__(self,b):b=Z(b);return Z(self.re+b.re,self.im+b.im)
    __radd__=__add__
    def __neg__(self):return Z(-self.re,-self.im)
    def __sub__(self,b):return self+-Z(b)
    def __mul__(self,b):b=Z(b);return Z(self.re*b.re-self.im*b.im,self.re*b.im+self.im*b.re)
    __rmul__=__mul__
    def conjugate(self):return Z(self.re,-self.im)
    def __truediv__(self,b):
        b=Z(b);den=b.re.square()+b.im.square();need(den.lo>0,'complex original-root divisor');out=self*b.conjugate();return Z(out.re/den,out.im/den)


def convolution(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out


def power(a,n):
    out=[1]
    for _ in range(n):out=convolution(out,a)
    return out


def derivative(a):return [(i+1)*x for i,x in enumerate(a[1:])]


def evaluate(a,t):
    out=0
    for x in reversed(a):out=out*t+x
    return out


def chebyshev(first):
    out=[[1],first]
    for n in range(2,10):
        row=[0]+[2*x for x in out[-1]]
        for j,x in enumerate(out[-2]):row[j]-=x
        out.append(row)
    return out


def equations(eta,v,c):
    x,y,T,xi3,xi4,omega=v;r=eta*x;delta=eta*(x-y);opening=delta*delta+eta*T
    shifted=[-r,D(1)]
    def polynomial(rows):
        result=[D(0) for _ in range(10)]
        for n,m in rows:
            for j,a in enumerate(power(shifted,n)):result[j]+=m*a
        result[0]-=sum((m*(1-eta-r)**n for n,m in rows),D(0))
        return result
    poly=polynomial([(9,D(1)),(8,F(9,4)*delta),(7,F(9,7)*opening)])
    px=polynomial([(8,D(-F(27,4))),(7,-F(108,7)*delta),(6,-9*opening)])
    py=polynomial([(8,D(-F(9,4))),(7,-F(18,7)*delta)])
    pT=polynomial([(7,D(F(9,7)))])
    Ts=chebyshev([0,1]);Us=chebyshev([0,2]);phases=[-F(1,2)+eta*xi3,D(-c)+eta*xi4];Irows=[];Rrows=[];normals=[];Its=[]
    for t in phases:
        imaginary=[D(0)]+[evaluate(Us[j-1],t) for j in range(1,10)]
        real=[evaluate(Ts[j],t) for j in range(10)]
        ip=[D(0)]+[evaluate(derivative(Us[j-1]),t) for j in range(1,10)]
        rp=[evaluate(derivative(Ts[j]),t) for j in range(10)]
        im=sum((a*b for a,b in zip(poly,imaginary)),D(0));re=sum((a*b for a,b in zip(poly,real)),D(0));it=sum((a*b for a,b in zip(poly,ip)),D(0));rt=sum((a*b for a,b in zip(poly,rp)),D(0))
        normal=[]
        for partial in (px,py,pT):normal.append(sum((a*b for a,b in zip(partial,real)),D(0))*it-rt*sum((a*b for a,b in zip(partial,imaginary)),D(0)))
        Irows.append(im);Rrows.append(re);normals.append(normal);Its.append(it)
    A=1-eta*(1+x);W=1+eta*omega;distance=1-eta*(1+y);P=[6*W**3,2*distance*A**2,-A**2];N,M=normals
    stationary=sum((P[i]*(N[(i+1)%3]*M[(i+2)%3]-N[(i+2)%3]*M[(i+1)%3]) for i in range(3)),D(0))
    G=[*Irows,*Rrows,W**2-distance**2-eta*T,stationary]
    return G,{'poly':poly,'partials':[px,py,pT],'normals':normals,'phases':phases,'Its':Its,'A':A,'D':distance,'W':W}
