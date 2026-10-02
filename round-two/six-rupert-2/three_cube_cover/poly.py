"""Small exact rational polynomial ring; no numerical or CAS dependency."""
from fractions import Fraction as F

class Poly:
    def __init__(self,value=0,n=7):
        self.n=n
        self.terms={k:F(v) for k,v in value.items() if v} if isinstance(value,dict) else ({(0,)*n:F(value)} if value else {})
    @classmethod
    def variable(cls,i,n=7):
        e=[0]*n;e[i]=1
        return cls({tuple(e):1},n)
    def lift(self,x):
        return x if isinstance(x,Poly) else Poly(x,self.n)
    def __add__(self,x):
        x=self.lift(x)
        if self.n!=x.n:raise ValueError('different exact polynomial rings')
        t=self.terms.copy()
        for e,v in x.terms.items():t[e]=t.get(e,F())+v
        return Poly(t,self.n)
    __radd__=__add__
    def __neg__(self):return Poly({e:-v for e,v in self.terms.items()},self.n)
    def __sub__(self,x):return self+-self.lift(x)
    def __rsub__(self,x):return self.lift(x)+-self
    def __mul__(self,x):
        x=self.lift(x)
        if self.n!=x.n:raise ValueError('different exact polynomial rings')
        t={}
        for a,u in self.terms.items():
            for b,v in x.terms.items():
                e=tuple(i+j for i,j in zip(a,b));t[e]=t.get(e,F())+u*v
        return Poly(t,self.n)
    __rmul__=__mul__
    def __eq__(self,x):return self.terms==self.lift(x).terms
    def coefficients(self):return [[list(e),str(v)] for e,v in sorted(self.terms.items())]
    def evaluate(self,x):
        return sum((v*product(t**i for t,i in zip(x,e)) for e,v in self.terms.items()),F())
    def bidegree(self,left):
        return [max((sum(e[i] for i in left) for e in self.terms),default=0),max((sum(e[i] for i in range(self.n) if i not in left) for e in self.terms),default=0)]

def product(xs):
    a=1
    for x in xs:a*=x
    return a

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def qmul(a,b):
    h,x=a[0],a[1:];k,y=b[0],b[1:]
    c=cross(x,y)
    return (h*k-dot(x,y),*(h*v+k*u+w for u,v,w in zip(x,y,c)))
def conj(q):return (q[0],*(-x for x in q[1:]))
def rotation_homogeneous(q):
    h,x,y,z=q
    return ((h*h+x*x-y*y-z*z,2*(x*y-h*z),2*(x*z+h*y)),
            (2*(x*y+h*z),h*h-x*x+y*y-z*z,2*(y*z-h*x)),
            (2*(x*z-h*y),2*(y*z+h*x),h*h-x*x-y*y+z*z))
def mm(a,b):return tuple(tuple(dot(row,col) for col in zip(*b)) for row in a)
def transpose(a):return tuple(zip(*a))
def act(a,x):return tuple(dot(row,x) for row in a)
def scaled(a,k):return tuple(tuple(k*x for x in row) for row in a)
def det(a):return dot(a[0],cross(a[1],a[2]))
def identity():return ((1,0,0),(0,1,0),(0,0,1))
