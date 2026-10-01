"""Cleared Gram forms and exact coefficient sign checks over Z[u]."""
import math
from fractions import Fraction as F
from systems import R,ST,QT,DEGREES,disjoint,read_r,sector,serial,require,choose
from poly import add,neg,mul,exact_divide,gcd
from exact import digest

ZERO=(F(0),);ONE=(F(1),)
def poly(x):
 x=R(x);require(x.d==ONE,'non-polynomial coefficient');return x.n
def psum(seq):
 result=ZERO
 for x in seq:result=add(result,x)
 return result
def pmul(*seq):
 result=ONE
 for x in seq:result=mul(result,x)
 return result
def constant(x):return (F(x),)
def common_den(seq):
 result=ONE
 for x in seq:result=mul(result,exact_divide(x.d,gcd(result,x.d)))
 result=tuple(v/result[-1] for v in result);R(result).coefficients_positive();return result
def numerator(x,den):return mul(x.n,exact_divide(den,x.d))

def forms(q,p,r,d,degree):
 j,ell=degree;s=3*q+4;n=(q*q+11*q+18)/2;m=(q+2)*(q+3)/2+1
 valid=lambda t:j<=t[0]<=2-j and ell<=t[2]
 si=[i for i,t in enumerate(ST) if valid(t)];qi=[i for i,t in enumerate(QT) if valid(t)]
 norm=lambda t:choose(2-2*j,t[0]-j)*choose(q-1-2*ell,t[2]-ell)
 ns=[poly(norm(ST[i])) for i in si];nq=[poly(norm(QT[i])) for i in qi];triv=j==ell==0
 cb=common_den(p+r);cd=common_den(d)
 pn=[numerator(x,cb) for x in p];rn=[numerator(x,cb) for x in r];dn=[numerator(x,cd) for x in d]
 HB=[]
 for i in si:
  row=[]
  for b,k in enumerate(qi):
   z=mul(psum([pn[i],rn[k],cb]),poly(disjoint(q,ST[i],QT[k],j,ell)))
   if triv:z=add(z,neg(mul(nq[b],cb)))
   row.append(z)
  HB.append(row)
 square=[[psum(pmul(ns[h],HB[h][a],HB[h][b]) for h in range(len(si))) for b in range(len(qi))] for a in range(len(qi))]
 GD=[];GP=[]
 mp=poly(m) if triv else ONE
 for a,i in enumerate(qi):
  dr=[];pr=[]
  for b,k in enumerate(qi):
   base=add(poly(s*int(a==b)),neg(nq[b]) if triv else ZERO)
   z=add(mul(base,cd),mul(add(dn[i],dn[k]),poly(disjoint(q,QT[i],QT[k],j,ell))))
   dr.append(mul(nq[a],z))
   pr.append(add(mul(mp,nq[a]) if a==b else ZERO,neg(mul(nq[a],nq[b])) if triv else ZERO))
  GD.append(dr);GP.append(pr)
 for name,matrix in [('D',GD),('P',GP),('square',square)]:
  require(all(matrix[a][b]==matrix[b][a] for a in range(len(qi)) for b in range(len(qi))),name+' polynomial symmetry')
  if triv:require(all(psum(row)==ZERO for row in matrix),name+' polynomial constant kernel')
 hl=poly(4*s-1);hu=poly(4*(n-s)-1);nn=poly(4*n-1)
 dl=pmul(constant(4),mp,cd,cb,cb,hl);du=pmul(constant(4),mp,cd,cb,cb,hu)
 R(dl).coefficients_positive();R(du).coefficients_positive()
 low=[];up=[]
 for a in range(len(qi)):
  lr=[];ur=[]
  for b in range(len(qi)):
   lr.append(psum([pmul(constant(4),mp,cb,cb,hl,GD[a][b]),neg(pmul(cd,cb,cb,hl,GP[a][b])),neg(pmul(constant(16),mp,cd,square[a][b]))]))
   ur.append(psum([pmul(nn,cd,cb,cb,hu,GP[a][b]),neg(pmul(constant(4),mp,cb,cb,hu,GD[a][b])),neg(pmul(constant(16),mp,cd,square[a][b]))]))
  low.append(lr);up.append(ur)
 return {'degree':degree,'S_types':[ST[i] for i in si],'Q_types':[QT[i] for i in qi],
  'cross_denominator':cb,'internal_denominator':cd,'lower_denominator':dl,'upper_denominator':du,'lower':low,'upper':up}

def itrim(p):
 p=list(p)
 while len(p)>1 and p[-1]==0:p.pop()
 return tuple(p or [0])
def imul(a,b):
 result=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):result[i+j]+=x*y
 return itrim(result)
def isub(a,b):return itrim((a[i] if i<len(a) else 0)-(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b))))
def idiv(a,b):
 require(b!=(0,),'zero integer polynomial divisor')
 rem=list(a);quot=[0]*max(1,len(a)-len(b)+1)
 while len(rem)>=len(b) and itrim(rem)!=(0,):
  degree=len(rem)-len(b);c,r=divmod(rem[-1],b[-1]);require(r==0,'nonintegral polynomial quotient coefficient')
  quot[degree]=c
  for h,x in enumerate(b):rem[degree+h]-=c*x
  rem=list(itrim(rem))
 require(itrim(rem)==(0,),'nonexact integer polynomial division')
 return itrim(quot)

def integer_minors(matrix):
 n=len(matrix);require(n>0 and all(len(row)==n for row in matrix),'nonsquare polynomial matrix')
 require(all(matrix[i][j]==matrix[j][i] for i in range(n) for j in range(n)),'asymmetric polynomial matrix')
 require(all(isinstance(x,(int,F)) for row in matrix for p in row for x in p),'inexact polynomial coefficient')
 scale=math.lcm(*(x.denominator for row in matrix for p in row for x in p))
 a=[[itrim(int(x*scale) for x in p) for p in row] for row in matrix]
 previous=(1,);records=[]
 for k in range(n):
  pivot=a[k][k];require(pivot!=(0,),'zero leading determinant')
  records.append({'order':k+1,'degree':len(pivot)-1,'constant':str(pivot[0]),'coefficient_positive':pivot[0]>0 and all(x>=0 for x in pivot),
   'negative_coefficients':sum(x<0 for x in pivot),'max_coefficient_bits':max(abs(x).bit_length() for x in pivot),'polynomial_sha256':digest([str(x) for x in pivot])})
  require(records[-1]['coefficient_positive'],'nonpositive generated polynomial coefficient')
  if k==n-1:break
  for i in range(k+1,n):
   for j in range(i,n):
    a[i][j]=idiv(isub(imul(pivot,a[i][j]),imul(a[i][k],a[k][j])),previous);a[j][i]=a[i][j]
   a[i][k]=a[k][i]=(0,)
  previous=pivot
 return {'positive_coefficient_scale':str(scale),'minors':records}

def evaluate(p,u):
 z=F(0)
 for x in reversed(p):z=z*u+x
 return z
