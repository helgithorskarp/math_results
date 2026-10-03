"""Small exact Q(sqrt5) polynomial ring; helpers adapted from public9584.

The ring stores every coefficient explicitly. It does not perform a search,
interval approximation or implicit quotient reduction. Sparse-ring layout:
../three_cube_cover/poly.py; no theorem from that packet is imported.
"""
import geometry as g
Q=g.Q
class P:
    def __init__(self,value=0,n=2):
        self.n=n
        self.terms={e:Q(v) for e,v in value.items() if v!=0} if isinstance(value,dict) else ({(0,)*n:Q(value)} if value!=0 else {})
    @classmethod
    def variable(cls,i,n=2):
        e=[0]*n;e[i]=1;return cls({tuple(e):Q(1)},n)
    def lift(self,x):
        y=x if isinstance(x,P) else P(x,self.n)
        if self.n!=y.n:raise ValueError('different coefficient rings')
        return y
    def __add__(self,x):
        x=self.lift(x);out=self.terms.copy()
        for e,v in x.terms.items():out[e]=out.get(e,Q())+v
        return P(out,self.n)
    __radd__=__add__
    def __neg__(self):return P({e:-v for e,v in self.terms.items()},self.n)
    def __sub__(self,x):return self+-self.lift(x)
    def __rsub__(self,x):return self.lift(x)+-self
    def __mul__(self,x):
        x=self.lift(x);out={}
        for e,u in self.terms.items():
            for f,v in x.terms.items():
                ef=tuple(i+j for i,j in zip(e,f));out[ef]=out.get(ef,Q())+u*v
        return P(out,self.n)
    __rmul__=__mul__
    def __eq__(self,x):return self.terms==self.lift(x).terms
    def coefficients(self):return [[list(e),g.enc(v)] for e,v in sorted(self.terms.items())]
    def at(self,values):
        total=Q()
        for e,v in self.terms.items():
            for x,k in zip(values,e):
                for _ in range(k):v=v*x
            total+=v
        return total
def dot(x,y):return sum((a*b for a,b in zip(x,y)),0)
def cross(x,y):return (x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0])
def act(A,v):return tuple(dot(row,v) for row in A)
def mm(A,B):return tuple(tuple(dot(row,col) for col in zip(*B)) for row in A)
def transpose(A):return tuple(zip(*A))
def det(A):return dot(A[0],cross(A[1],A[2]))
def skew(c):
    zero=c[0]*0
    return ((zero,-c[2],c[1]),(c[2],zero,-c[0]),(-c[1],c[0],zero))
def rot_num(c):
    c2=dot(c,c);K=skew(c)
    return tuple(tuple((1-c2)*int(i==j)+c[i]*c[j]*2+K[i][j]*2 for j in range(3)) for i in range(3))
