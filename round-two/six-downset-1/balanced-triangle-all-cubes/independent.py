"""PRIVATE separate closed aggregate forms and conservative bidegrees.

No imports from the producer, recipe, physical sector module or polynomial
engine. Actual evaluation uses exact Fractions; the same expressions also
propagate rigorous numerator/denominator bidegree bounds without guessing
cancelled factors. This is same-author checking, not independent review.
"""
from fractions import Fraction as F

def require(ok,msg):
    if not ok:raise ValueError(msg)

def add_degree(a,b):
    return None if a is None or b is None else tuple(x+y for x,y in zip(a,b))
def max_degree(a,b):
    if a is None:return b
    if b is None:return a
    return tuple(max(x,y) for x,y in zip(a,b))

class Degree:
    def __init__(self,value=0,numerator=None,denominator=(0,0)):
        if isinstance(value,Degree):self.n,self.d=value.n,value.d;return
        self.n=numerator if numerator is not None else (0,0) if value else None
        self.d=denominator
    def __neg__(self):return Degree(1,self.n,self.d) if self.n is not None else Degree()
    def __add__(self,other):
        other=Degree(other)
        if self.n is None:return other
        if other.n is None:return self
        return Degree(1,max_degree(add_degree(self.n,other.d),add_degree(other.n,self.d)),add_degree(self.d,other.d))
    __radd__=__add__
    def __sub__(self,other):return self+-Degree(other)
    def __rsub__(self,other):return Degree(other)+-self
    def __mul__(self,other):
        other=Degree(other)
        if self.n is None or other.n is None:return Degree()
        return Degree(1,add_degree(self.n,other.n),add_degree(self.d,other.d))
    __rmul__=__mul__
    def __truediv__(self,other):
        other=Degree(other);require(other.n is not None,'nonzero divisor in conservative degree expression')
        if self.n is None:return Degree()
        return Degree(1,add_degree(self.n,other.d),add_degree(self.d,other.n))
    def __rtruediv__(self,other):return Degree(other)/self
    def __pow__(self,n):
        require(type(n) is int and n>=0,'nonnegative degree exponent')
        out=Degree(1)
        for _ in range(n):out=out*self
        return out

def zero(n):return [[F(0) for _ in range(n)] for _ in range(n)]
def diagonal(values):
    a=zero(len(values))
    for i,z in enumerate(values):a[i][i]=z
    return a

def forms(q,h):
    if type(q) is int:q=F(q)
    if type(h) is int:h=F(h)
    D=3*h;s=q+D;N=2*q+12*h;ell=6*h+1
    a=3*h*(ell-q+1)/(2*ell*s*(h-1));b=-2*a;c=9*(ell-q+1)/(2*ell*s)
    common=(q-1+(2*q-3)*D)/(ell*ell)
    mu=(s-3)/3-common-2*s*c*c/(9*(h-1))
    alpha=2*s*(1-2*(2*h-3)*c*c/(3*(h-1)))
    beta=2*s/3-4*s*c*c*(h+3)/(27*(h-1))
    nu=2*h*mu/(2*h-1)
    grams={};frames={}
    grams['anti']=diagonal([2*s,alpha])
    frames['anti']=[[2*s*s*(1+c*c),-s*c*alpha],[-s*c*alpha,alpha*alpha/2]]
    grams['standard']=diagonal([2*s/3,12*s,2*beta,2*nu])
    S=zero(4)
    S[0][0]=2*s*s/3+4*a*a*s*s/3
    S[0][1]=S[1][0]=4*a*c*s*s*(h-3)/(3*(h-1))
    S[0][2]=S[2][0]=-2*a*s*beta
    S[1][1]=12*s*s+4*c*c*s*s+8*c*c*s*s/((h-1)*(h-1))
    S[1][2]=S[2][1]=-2*c*s*beta*(h-3)/(h-1)
    S[1][3]=S[3][1]=4*h*c*s*nu/(h-1)
    S[2][2]=3*beta*beta;S[3][3]=6*nu*nu
    frames['standard']=S
    trace=[[12*h*s*s*(1+c*c),-6*h*c*s*beta],[-6*h*c*s*beta,3*h*beta*beta]]
    grams['fixed-even']=diagonal([4*(q-1),4*D,2*D*(q-2),12*h*s,2*h*beta])
    S=zero(5)
    S[0][0]=4*(q*q-1)+4*(q-1)*(q-1)/ell
    S[0][1]=S[1][0]=-4*D*(q-1)-4*D*(q-1)/ell
    S[0][2]=S[2][0]=4*D*(q-1)*(q-2)/ell
    S[1][1]=4*D*D+8*D+4*D*D/ell
    S[1][2]=S[2][1]=-4*D*(q-2)-4*D*D*(q-2)/ell
    S[2][2]=4*D*D*(q-2)+2*D*(q-2)*(q-2)+4*D*D*(q-2)*(q-2)/ell
    for i in range(2):
        for j in range(2):S[3+i][3+j]=trace[i][j]
    frames['fixed-even']=S
    grams['fixed-odd']=diagonal([2*q*D,12*h*s,2*h*beta,2*h*nu])
    S=zero(4);S[0][0]=2*q*D*(2*D+q);S[3][3]=6*h*nu*nu
    for i in range(2):
        for j in range(2):S[1+i][1+j]=trace[i][j]
    frames['fixed-odd']=S
    grams['untouched-even']=[[8*q]];frames['untouched-even']=[[16*q*q]]
    grams['untouched-odd']=[[4*D]];frames['untouched-odd']=[[8*D*D]]
    caps={name:[[(N-1)*F(i==j)-frames[name][i][j]/G[i][i] for j in range(len(G))] for i in range(len(G))] for name,G in grams.items()}
    return dict(alpha=[[alpha]],beta=[[beta]],mu=[[mu]])|caps
