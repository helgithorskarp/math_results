"""Independent Q(sqrt(5)) arithmetic and definition-level matrix operations."""
from fractions import Fraction as F
from functools import total_ordering

@total_ordering
class E:
    __slots__ = ('a', 'b')
    def __init__(self,a=0,b=0): self.a,self.b=F(a),F(b)
    def __add__(self,o):
        o=as_e(o); return E(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self): return E(-self.a,-self.b)
    def __sub__(self,o): return self+-as_e(o)
    def __rsub__(self,o): return as_e(o)+-self
    def __mul__(self,o):
        o=as_e(o); return E(self.a*o.a+5*self.b*o.b,self.a*o.b+self.b*o.a)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=as_e(o); n=o.a*o.a-5*o.b*o.b
        if not n: raise ZeroDivisionError('zero algebraic denominator')
        return self*E(o.a/n,-o.b/n)
    def __rtruediv__(self,o): return as_e(o)/self
    def __eq__(self,o):
        o=as_e(o); return (self.a,self.b)==(o.a,o.b)
    def sign(self):
        if not self.b: return (self.a>0)-(self.a<0)
        if not self.a: return (self.b>0)-(self.b<0)
        if (self.a>0)==(self.b>0): return 1 if self.a>0 else -1
        gap=self.a*self.a-5*self.b*self.b
        if not gap: raise ValueError('impossible rational sqrt5 equality')
        return ((self.a>0)-(self.a<0)) * ((gap>0)-(gap<0))
    def __lt__(self,o): return (self-as_e(o)).sign()<0
    def __hash__(self): return hash((self.a,self.b))
    def __repr__(self): return str(self.pair())
    def pair(self): return [str(self.a),str(self.b)]
    def phi_key(self): return (self.a-self.b,2*self.b)

def as_e(v): return v if isinstance(v,E) else E(v)
PHI=E(F(1,2),F(1,2)); ZERO=E(0); ONE=E(1)
def dot(a,b): return sum((x*y for x,y in zip(a,b)),ZERO)
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def mv(a,v): return tuple(dot(r,v)for r in a)
def tr(a): return tuple(zip(*a))
def mm(a,b): return tuple(tuple(dot(r,c)for c in tr(b))for r in a)
def det(a): return dot(a[0],cross(a[1],a[2]))
ID=tuple(tuple(E(int(i==j))for j in range(3))for i in range(3))
def inverse(a):
    d=det(a)
    adj=tr((cross(a[1],a[2]),cross(a[2],a[0]),cross(a[0],a[1])))
    return tuple(tuple(x/d for x in r)for r in adj)
def cayley(c):
    x,y,z=c; k=((ZERO,-z,y),(z,ZERO,-x),(-y,x,ZERO))
    plus=tuple(tuple(ID[i][j]+k[i][j]for j in range(3))for i in range(3))
    minus=tuple(tuple(ID[i][j]-k[i][j]for j in range(3))for i in range(3))
    return mm(plus,inverse(minus))
def rodrigues(c,v):
    n=ONE+dot(c,c);cv=cross(c,v);cvdot=dot(c,v)
    return tuple(((ONE-dot(c,c))*v[i]+2*c[i]*cvdot+2*cv[i])/n for i in range(3))
def encode(v):
    if isinstance(v,E): return v.pair()
    if isinstance(v,F): return str(v)
    if isinstance(v,dict): return {k:encode(x)for k,x in v.items()}
    if isinstance(v,(tuple,list)): return [encode(x)for x in v]
    return v
