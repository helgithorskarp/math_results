"""Fresh QQ[T]/(T^12-T^6+1); physical T=exp(pi*i/18)."""
from fractions import Fraction as Q

def need(ok,why):
    if not ok:raise ValueError(why)

class E:
    __slots__=('v',)
    def __init__(self,x=0):
        if isinstance(x,E):self.v=x.v
        elif isinstance(x,(tuple,list)):need(len(x)==12,'complete field basis');self.v=tuple(map(Q,x))
        else:self.v=(Q(x),)+(Q(0),)*11
    def __bool__(self):return any(self.v)
    def __eq__(self,o):
        if not isinstance(o,(E,int,Q,tuple,list)):return NotImplemented
        return self.v==E(o).v
    def __add__(self,o):
        if not isinstance(o,(E,int,Q,tuple,list)):return NotImplemented
        o=E(o);return E(tuple(a+b for a,b in zip(self.v,o.v)))
    __radd__=__add__
    def __neg__(self):return E(tuple(-a for a in self.v))
    def __sub__(self,o):
        if not isinstance(o,(E,int,Q,tuple,list)):return NotImplemented
        return self+-E(o)
    def __rsub__(self,o):
        if not isinstance(o,(E,int,Q,tuple,list)):return NotImplemented
        return E(o)+-self
    def __mul__(self,o):
        if not isinstance(o,(E,int,Q,tuple,list)):return NotImplemented
        o=E(o);z=[Q(0)]*23
        for i,a in enumerate(self.v):
            if a:
                for j,b in enumerate(o.v):
                    if b:z[i+j]+=a*b
        for k in range(22,11,-1):
            a=z[k]
            if a:z[k-6]+=a;z[k-12]-=a
        return E(tuple(z[:12]))
    __rmul__=__mul__
    def __truediv__(self,n):return self*Q(1,n)
    def __pow__(self,n):
        need(type(n)is int and n>=0,'nonnegative integer exponent');a=self;z=E(1)
        while n:
            if n&1:z=z*a
            a=a*a;n//=2
        return z
    def conjugate(self):return sum((a*POW[(-j)%36]for j,a in enumerate(self.v)),E())
    def real(self):return(self+self.conjugate())/2
    def json(self):return[str(x)for x in self.v]
T=E((0,1)+(0,)*10)
POW=[T**j for j in range(36)]
I=POW[9];W=POW[4];C=(POW[2]+POW[34])/2
INV1C=(8*C*C-8*C+2)/3
INVCPLUS=(4*C*C+2*C-2)/3*INV1C
need(T**36==1 and T**18==-1 and I*I==-1 and W**6+W**3+1==0,'cyclotomic relations')
need(8*C**3-6*C-1==0 and (1+C)*INV1C==1 and (C+2*C*C-1)*INVCPLUS==1,'real embedding algebra')

class A:
    """Sparse polynomial in independent real parameters M,B, over E."""
    __slots__=('p',)
    def __init__(self,x=0):
        if isinstance(x,A):self.p=x.p.copy()
        elif isinstance(x,dict):self.p={k:E(v)for k,v in x.items()if E(v)}
        else:self.p={(0,0):E(x)}if E(x)else{}
    def __bool__(self):return bool(self.p)
    def __eq__(self,o):return self.p==A(o).p
    def __add__(self,o):
        z=self.p.copy()
        for k,v in A(o).p.items():z[k]=z.get(k,E())+v
        return A(z)
    __radd__=__add__
    def __neg__(self):return A({k:-v for k,v in self.p.items()})
    def __sub__(self,o):return self+-A(o)
    def __rsub__(self,o):return A(o)+-self
    def __mul__(self,o):
        z={}
        for a,v in self.p.items():
            for b,w in A(o).p.items():k=(a[0]+b[0],a[1]+b[1]);z[k]=z.get(k,E())+v*w
        return A(z)
    __rmul__=__mul__
    def __truediv__(self,n):return self*Q(1,n)
    def conjugate(self):return A({k:v.conjugate()for k,v in self.p.items()})
    def real(self):return(self+self.conjugate())/2
    def evaluate(self,m,b):return sum((v*(m**a)*(b**d)for(a,d),v in self.p.items()),E())
    def json(self):
        need(set(self.p)<={(0,0),(1,0),(0,1)},'complete affine parameter map')
        return[self.p.get(k,E()).json()for k in [(0,0),(1,0),(0,1)]]
M=A({(1,0):1});B=A({(0,1):1})

def constant(x):return[A(x)]+[A()for _ in range(4)]
def add(a,b):return[x+y for x,y in zip(a,b)]
def scale(a,k):return[v*k for v in a]
def multiply(a,b):
    z=[A()for _ in range(5)]
    for i,v in enumerate(a):
        if v:
            for j in range(5-i):
                if b[j]:z[i+j]=z[i+j]+v*b[j]
    return z
def power(a,n):
    z=constant(1)
    for _ in range(n):z=multiply(z,a)
    return z
def conjugate(a):return[v.conjugate()for v in a]
def encode(a):return[v.json()for v in a]
