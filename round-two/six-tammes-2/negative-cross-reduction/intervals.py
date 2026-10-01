"""Validated interval experiment selecting packing candidates.

Every interval operation rounds outward on an 80-bit dyadic lattice. Root
brackets cover each t piece by exact Bernstein signs; completeness depends
on the separately checked global root counts and rank-exception certificate.
The algebra/root-count certificate must be checked with check.py first.
"""
from fractions import Fraction as Q
from pathlib import Path
from functools import lru_cache
import json,math,time
S=1<<80
def require(ok,message):
 if not ok:raise ValueError(message)
def floorq(x):return x.numerator*S//x.denominator
def ceilq(x):return -((-x.numerator*S)//x.denominator)
class I:
 def __init__(self,a=0,b=None):
  a,b=Q(a),Q(a if b is None else b);require(a<=b,'valid interval')
  self.l,self.h=floorq(a),ceilq(b)
 @classmethod
 def raw(cls,l,h):
  r=object.__new__(cls);r.l,r.h=l,h;require(l<=h,'outward endpoints');return r
 @staticmethod
 def cv(x):return x if isinstance(x,I) else I(x)
 def __add__(self,x):
  x=I.cv(x);return I.raw(self.l+x.l,self.h+x.h)
 __radd__=__add__
 def __neg__(self):return I.raw(-self.h,-self.l)
 def __sub__(self,x):return self+-I.cv(x)
 def __rsub__(self,x):return I.cv(x)+-self
 def __mul__(self,x):
  x=I.cv(x);v=[a*b for a in (self.l,self.h) for b in (x.l,x.h)]
  return I.raw(min(v)//S,-((-max(v))//S))
 __rmul__=__mul__
 def __truediv__(self,x):
  x=I.cv(x)
  if x.l<=0<=x.h:raise ArithmeticError('unresolved interval denominator')
  v=[Q(a*S,b) for a in (self.l,self.h) for b in (x.l,x.h)]
  return I.raw(min(v).numerator//min(v).denominator,-((-max(v).numerator)//max(v).denominator))
 def __rtruediv__(self,x):return I.cv(x)/self
 def __pow__(self,n):
  require(type(n)is int and n>=0,'nonnegative interval power');r=I(1)
  for _ in range(n):r=r*self
  return r
 def sign(self):return 1 if self.l>0 else -1 if self.h<0 else 0
 def fractions(self):return Q(self.l,S),Q(self.h,S)

def dot(x,y,H):return sum((x[i]*H[i][j]*y[j] for i in range(3) for j in range(3)),I())
def mv(A,x):return [sum((a*b for a,b in zip(row,x)),I()) for row in A]
def cross(x,y):return [x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]]
def det(A):
 return A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])-A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])+A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0])
def solve(A,z):
 D=det(A)
 return [det([[z[i] if j==a else A[i][j] for j in range(3)] for i in range(3)])/D for a in range(3)]
def build(t,q,sign):
 H=[[I(1) if i==j else t for j in range(3)] for i in range(3)]
 HI=[[(1/(1-t) if i==j else 0)-t/((1-t)*(1+2*t)) for j in range(3)] for i in range(3)]
 D=(1-t)**2*(1+2*t);r=2*t/(1+t)
 k=t*(9*t*t-2*t-3)/(1+t)**2;gamma=k/(1+k)
 mu=(t-1)*(t+1)*(2*t+1)*(3*t-1)/(9*t**3-t*t-t+1)
 B={i:[I(1 if j==s else 0) for j in range(3)] for s,i in enumerate((1,2,4))}
 for n,i,j,o in ((8,2,4,1),(10,1,2,4),(12,1,10,2),(13,2,8,4)):
  B[n]=[r*(a+b)-c for a,b,c in zip(B[i],B[j],B[o])]
 d=mv(HI,cross(B[8],B[2]))
 if q.l>S or q.h<-S:
  x=1/q;L=1+D*x*x
  alpha=(D*x*x-1)/L;beta=2*D*x/L
 else:
  L=D+q*q;alpha=(D-q*q)/L;beta=2*D*q/L
 U=[t*a+alpha*(b-t*a)+beta*c for a,b,c in zip(B[8],B[2],d)]
 C=[gamma*a+sign*mu*b for a,b in zip(B[12],mv(HI,cross(B[12],U)))]
 A=[mv(H,v) for v in (U,B[10],C)]
 V=solve(A,[k,t,t-gamma*dot(U,B[12],H)])
 W=[gamma*(u+v)+sign*mu*c for u,v,c in zip(U,V,mv(HI,cross(U,V)))]
 P=dict(B);den=(2*r-1)*(r+1)
 for label,coeffs in ((0,(r,r,1-r)),(5,(1-r,r,r)),(11,(r,1-r,r))):
  P[label]=[sum((a*v[i] for a,v in zip(coeffs,(U,W,V))),I())/den for i in range(3)]
 P.update({6:U,7:W,9:V})
 return P,H

HERE=Path(__file__).resolve().parent
certificate=json.loads((HERE/'certificate.json').read_text())
require(certificate['format']==1 and certificate['interval']==['14/25','593/1000'], 'fixed closed parameter interval')
require(certificate['deleted_edge']==[9,13], 'literal deleted cross edge')
data=certificate['loci']
def bernstein(p,lo,hi):
 n=len(p)-1
 a=[sum(Q(p[j])*math.comb(j,k)*lo**(j-k)*(hi-lo)**k for j in range(k,n+1)) for k in range(n+1)]
 return [sum(a[k]*Q(math.comb(i,k),math.comb(n,k)) for k in range(i+1)) for i in range(n+1)]
LO,HI=Q(14,25),Q(593,1000)
# factor index, q root bracket, and a strict packing-violation witness.
BRANCHES=[(-1,0,Q(-19),Q(-4),(9,13)),
          (-1,1,Q(38,100),Q(42,100),(6,13)),
          (-1,1,Q(18,10),Q(57,10),(2,9)),
          (1,1,Q(-12),Q(-22,5),(2,9)),
          (1,2,Q(-37,10),Q(-7,2),(8,11)),
          (1,2,Q(-17,10),Q(-31,20),(1,9))]
@lru_cache(maxsize=100)
def factor_bernstein(sign,index,left,right):
 table=data[str(sign)]['factors'][index]['table'];degree=max(len(c) for c in table)-1
 polys=[]
 for c in table:
  coefficients=bernstein(tuple(c),left,right)
  # Elevate every polynomial to the same Bernstein degree in t.
  d=len(coefficients)-1
  elevated=[sum(coefficients[j]*Q(math.comb(d,j)*math.comb(degree-d,i-j),math.comb(degree,i))
     for j in range(max(0,i-(degree-d)),min(d,i)+1)) for i in range(degree+1)]
  polys.append(elevated)
 return [[I(polys[j][i]) for j in range(len(polys))] for i in range(degree+1)]
def point_sign(rows,x):
 values=[]
 for row in rows:
  v=I()
  for c in reversed(row):v=v*x+c
  values.append(v)
 return I.raw(min(v.l for v in values),max(v.h for v in values)).sign()
def root_bracket(rows,a,b):
 sa,sb=point_sign(rows,a),point_sign(rows,b)
 require(sa*sb==-1,'uniform endpoint signs for full parameter piece')
 low=a;high=b
 for _ in range(22):
  m=(low+high)/2
  if point_sign(rows,m)==sa:low=m
  else:high=m
 aa=low
 low=a;high=b
 for _ in range(22):
  m=(low+high)/2
  if point_sign(rows,m)==sb:high=m
  else:low=m
 bb=high
 require(aa<bb and point_sign(rows,aa)==sa and point_sign(rows,bb)==sb,'outward refined root bracket')
 return aa,bb
def prove(branch,left,right,depth=0):
 sign,index,a,b,pair=branch
 rows=factor_bernstein(sign,index,left,right)
 aa,bb=root_bracket(rows,a,b)
 try:
  P,H=build(I(left,right),I(aa,bb),sign)
  gap=dot(P[pair[0]],P[pair[1]],H)-I(left,right)
  if gap.l>0:
   return [(left,right,aa,bb,gap.l,depth)]
 except ArithmeticError:pass
 if depth>=14:raise RuntimeError('bounded interval refinement unresolved; no exclusion')
 mid=(left+right)/2
 return prove(branch,left,mid,depth+1)+prove(branch,mid,right,depth+1)
def manifest(rows):return [[str(a),str(b),str(c),str(d),str(Q(g,S)),depth] for a,b,c,d,g,depth in rows]
