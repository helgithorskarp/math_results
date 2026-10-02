"""Independent exact coefficient arithmetic for facial alias obstructions.
No target code, expected certificate or external algebra library is imported.
"""
from fractions import Fraction as Q
from itertools import combinations,permutations
from math import comb,gcd
from functools import reduce
import json,hashlib

def trim(a):
 a=list(a)
 while len(a)>1 and a[-1]==0:a.pop()
 return tuple(a)
def add(a,b):return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return trim(c)
def scale(a,x):return trim([t*x for t in a])
def power(a,n):
 c=(1,)
 for _ in range(n):c=mul(c,a)
 return c
def value(a,x):
 v=0
 for y in reversed(a):v=v*x+y
 return v
def divexact(a,b):
 a=list(a);c=[0]*max(1,len(a)-len(b)+1)
 for j in range(len(a)-len(b),-1,-1):
  z=Q(a[j+len(b)-1],b[-1]);c[j]=z
  for k,bk in enumerate(b):a[j+k]-=z*bk
 if any(a):raise ValueError('inexact polynomial division')
 return trim(c)
def bernstein(a,lo,hi):
 n=len(a)-1;p=[Q(0)]*(n+1)
 for i,v in enumerate(a):
  for j in range(i+1):p[j]+=v*comb(i,j)*lo**(i-j)*(hi-lo)**j
 return [sum(p[j]*Q(comb(k,j),comb(n,j)) for j in range(k+1)) for k in range(n+1)]
def determinant(M):
 n=len(M);c=(0,)
 for order in permutations(range(n)):
  z=(1,);sign=(-1)**sum(order[i]>order[j] for i in range(n) for j in range(i+1,n))
  for i in range(n):z=mul(z,M[i][order[i]])
  c=add(c,scale(z,sign))
 return c
R=(0,1);D=(2,-1);ZERO=(0,);ONE=(1,)
def vadd(a,b):return tuple(add(x,y) for x,y in zip(a,b))
def vsub(a,b):return tuple(sub(x,y) for x,y in zip(a,b))
def vmul(a):return tuple(mul(R,x) for x in a)
L={1:(ONE,ZERO,ZERO),2:(ZERO,ONE,ZERO),4:(ZERO,ZERO,ONE)}
L[10]=vsub(vmul(vadd(L[1],L[2])),L[4]);L[8]=vsub(vmul(vadd(L[2],L[4])),L[1]);L[13]=vsub(vmul(vadd(L[2],L[8])),L[4]);L[12]=vsub(vmul(vadd(L[1],L[10])),L[2])
B={0:(ONE,ZERO,ZERO),5:(ZERO,ONE,ZERO),11:(ZERO,ZERO,ONE)}
B[6]=vsub(vmul(vadd(B[0],B[11])),B[5]);B[7]=vsub(vmul(vadd(B[0],B[5])),B[11]);B[9]=vsub(vmul(vadd(B[5],B[11])),B[0])
def dotN(a,b):
 z=(0,)
 for i in range(3):
  for j in range(3):z=add(z,mul(mul(a[i],b[j]),D if i==j else R))
 return z

def rational_out(a):return [str(x) for x in a]
def factor_roots(a):
 p=a;roots=[]
 for root in [0,1,2,-1]:
  m=0
  while len(p)>1 and value(p,root)==0:p=divexact(p,(-root,1));m+=1
  roots.append((root,m))
 if any(x.denominator!=1 for x in p):raise ValueError('noninteger quotient')
 g=reduce(gcd,[abs(int(x)) for x in p]);q=tuple(int(x)//g for x in p)
 rebuilt=scale(q,g)
 for root,m in roots:rebuilt=mul(rebuilt,power((-root,1),m))
 if trim(rebuilt)!=trim(a):raise ValueError('whole coefficient reconstruction')
 return dict(constant=g,roots=roots,reduced=list(q))

def run():
 old=(Q(28,39),Q(1186,1593));wide=(Q(2,3),Q(3,4))
 internal=[]
 for name,V in [('L',L),('R',B)]:
  for i,v in sorted(V.items()):
   if dotN(v,v)!=D:raise ValueError('unit norm '+str(i))
  for i,j in combinations(sorted(V),2):
   q=sub(R,dotN(V[i],V[j]));row=dict(patch=name,pair=[i,j],gap=list(q))
   for label,(lo,hi) in [('old',old),('wide',wide)]:
    row[label]=rational_out(bernstein(q,lo,hi));row[label+'_positive']=q==(0,) or all(x>0 for x in bernstein(q,lo,hi))
   internal.append(row)
 k=dotN(B[6],B[7]);
 if dotN(B[6],B[9])!=k or dotN(B[7],B[9])!=k:raise ValueError('right k equalities')
 dets=[]
 for alias in [4,8,13]:
  A=dotN(L[alias],L[10]);BB=dotN(L[alias],L[12]);DD=power(D,2)
  PN=sub(DD,power(A,2));QN=sub(DD,power(BB,2));UN=sub(mul(R,D),mul(A,BB));RN=sub(DD,power(k,2));VN=sub(mul(k,D),power(k,2));WN=sub(mul(R,D),mul(BB,k));ZN=sub(mul(R,D),mul(A,k))
  cf=sub(add(mul(PN,power(WN,2)),mul(RN,power(UN,2))),mul(mul(PN,QN),RN))
  cg=sub(add(mul(RN,power(ZN,2)),mul(PN,power(VN,2))),mul(PN,power(RN,2)))
  f=[QN,scale(mul(UN,WN),-2),cf];g=[RN,scale(mul(VN,ZN),-2),cg]
  F=determinant([f+[ZERO],[ZERO]+f,g+[ZERO],[ZERO]+g]);fact=factor_roots(F)
  row=dict(alias=alias,A=list(A),B=list(BB),k=list(k),quadratics=[list(map(list,f)),list(map(list,g))],full=list(F),factor=fact)
  for label,(lo,hi) in [('old',old),('wide',wide)]:
   bc=bernstein(fact['reduced'],lo,hi);row[label]=rational_out(bc);row[label+'_negative']=all(x<0 for x in bc)
  dets.append(row)
 return dict(norms=13,internal=internal,obstructions=dets,old_interval=rational_out(old),wide_interval=rational_out(wide))
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
