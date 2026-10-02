"""Own credited exact polynomial kernel, trimmed from REVIEW9506; no author code."""
from fractions import Fraction as F


def pair(x):
    if isinstance(x,tuple):return (F(x[0]),F(x[1]))
    return (F(x),F(0))

def plus(a,b):return (a[0]+b[0],a[1]+b[1])
def times(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def mono(a,b):
    out=dict(a)
    for k,v in b:out[k]=out.get(k,0)+v
    return tuple(sorted((k,v) for k,v in out.items() if v))

class Poly:
    def __init__(self,terms=()):
        self.terms={tuple(k):pair(v) for k,v in dict(terms).items() if pair(v)!=(0,0)}
    @staticmethod
    def constant(value):return Poly({():pair(value)})
    @staticmethod
    def variable(name):return Poly({((name,1),):(1,0)})
    def __add__(self,other):
        other=cast(other);out=self.terms.copy()
        for k,v in other.terms.items():out[k]=plus(out.get(k,(0,0)),v)
        return Poly(out)
    __radd__=__add__
    def __neg__(self):return Poly({k:(-v[0],-v[1]) for k,v in self.terms.items()})
    def __sub__(self,other):return self+-cast(other)
    def __rsub__(self,other):return cast(other)+-self
    def __mul__(self,other):
        other=cast(other);out={}
        for a,x in self.terms.items():
            for b,y in other.terms.items():
                k=mono(a,b);out[k]=plus(out.get(k,(0,0)),times(x,y))
        return Poly(out)
    __rmul__=__mul__
    def __truediv__(self,other):
        other=F(other)
        if not other:raise ValueError('nonzero scalar divisor required')
        return Poly({k:(v[0]/other,v[1]/other) for k,v in self.terms.items()})
    def __pow__(self,n):
        if type(n)!=int:raise ValueError('integral degree required')
        if n<0:
            if len(self.terms)!=1:raise ValueError('inverse requires one t monomial')
            ((key,value),)=self.terms.items()
            if value[1] or not value[0] or any(name!='t' for name,_ in key):raise ValueError('only t or scalar may be inverted')
            return Poly({tuple((name,degree*n) for name,degree in key):(value[0]**n,0)})
        out=cast(1);base=self
        while n:
            if n&1:out=out*base
            base=base*base;n//=2
        return out
    def substitute(self,mapping):
        out=cast(0)
        for k,v in self.terms.items():
            term=cast(v)
            for name,n in k:term=term*cast(mapping.get(name,Poly.variable(name)))**n
            out=out+term
        return out
    def coefficient(self,name,exponent):
        out={}
        for k,v in self.terms.items():
            m=dict(k)
            if m.pop(name,0)==exponent:out[tuple(sorted(m.items()))]=v
        return Poly(out)
    def derivative(self,name):
        out={}
        for k,v in self.terms.items():
            m=dict(k);n=m.get(name,0)
            if not n:continue
            m[name]=n-1;out[tuple(sorted((x,y) for x,y in m.items() if y))]=(n*v[0],n*v[1])
        return Poly(out)
    def integral(self,name):
        out={}
        for k,v in self.terms.items():
            m=dict(k);n=m.get(name,0)+1;m[name]=n
            out[tuple(sorted(m.items()))]=(v[0]/n,v[1]/n)
        return Poly(out)
    def divide_monomial(self,factors):
        out={}
        for k,v in self.terms.items():
            m=dict(k)
            for name,n in factors.items():
                if m.get(name,0)<n:raise ValueError('whole polynomial is not divisible by '+name)
                m[name]=m.get(name,0)-n
            out[tuple(sorted((x,y) for x,y in m.items() if y))]=v
        return Poly(out)
    def conjugate_coefficients(self):return Poly({k:(v[0],-v[1]) for k,v in self.terms.items()})
    def norm(self,bounds):
        out=F(0)
        for k,v in self.terms.items():
            term=abs(v[0])+abs(v[1])
            for name,n in k:term*=F(bounds[name])**n
            out+=term
        return out
    def reduce_square(self,name,value):
        out=cast(0)
        for k,v in self.terms.items():
            m=dict(k);n=m.pop(name,0)
            out+=Poly({tuple(sorted(m.items())):v})*cast(value)**(n//2)*Poly.variable(name)**(n%2)
        return out
    def __eq__(self,other):return self.terms==cast(other).terms
    def record(self):
        return {'*'.join(name+(('^'+str(n)) if n!=1 else '') for name,n in k) or '1':[str(v[0]),str(v[1])] for k,v in sorted(self.terms.items())}

def cast(x):return x if isinstance(x,Poly) else Poly.constant(x)
def symbol(name):return Poly.variable(name)
def need(test,label):
    if not test:raise ValueError(label)
