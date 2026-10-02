"""Native Q[x]/(P) operations; both real embeddings have exact isolators."""
from fractions import Fraction as F
from claims import POLY
import inputs
from literal import require
A,B,C=POLY;qb=F(B,A);qc=F(C,A)
class Q:
    def __init__(self,a=0,b=0):
        if isinstance(a,Q):self.a,self.b=a.a,a.b
        else:self.a,self.b=F(a),F(b)
    def __add__(self,y):
        y=Q(y);return Q(self.a+y.a,self.b+y.b)
    __radd__=__add__
    def __neg__(self):return Q(-self.a,-self.b)
    def __sub__(self,y):return self+-Q(y)
    def __rsub__(self,y):return Q(y)+-self
    def __mul__(self,y):
        y=Q(y);return Q(self.a*y.a-qc*self.b*y.b,self.a*y.b+self.b*y.a-qb*self.b*y.b)
    __rmul__=__mul__
    def __truediv__(self,y):
        y=Q(y);norm=y.a*y.a-qb*y.a*y.b+qc*y.b*y.b
        require(norm!=0,'nonzero quadratic field denominator')
        return self*Q((y.a-qb*y.b)/norm,-y.b/norm)
    def __eq__(self,y):y=Q(y);return self.a==y.a and self.b==y.b
    def record(self):return [str(self.a),str(self.b)]

def sign(x,which):
    x=Q(x)
    if x==0:return 0
    lo,hi=map(F,('1/4','3/8') if which=='lower' else ('6','8'))
    for step in range(128):
        values=(x.a+x.b*lo,x.a+x.b*hi)
        if min(values)>0:return 1
        if max(values)<0:return -1
        mid=(lo+hi)/2;p=A*mid*mid+B*mid+C
        require(p!=0,'irrational root not rational midpoint')
        if (which=='lower' and p>0) or (which=='upper' and p<0):lo=mid
        else:hi=mid
    raise ValueError('bounded algebraic sign isolation incomplete, no mathematical conclusion')
