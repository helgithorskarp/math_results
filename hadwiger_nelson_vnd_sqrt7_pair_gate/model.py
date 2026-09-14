"""Fixed L10,2 + u L10,2 geometry; exact integer multiquadratic coefficients."""
from itertools import product,combinations
PRIMES=(2,3,7)
BASIS=(1,2,3,6,7,14,21,42)
ZERO=(0,)*8
def r(a=0):return (a,)+(0,)*7
def surd(mask,a=1):return tuple(a if i==mask else 0 for i in range(8))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,n):return tuple(n*x for x in a)
def mul(a,b):
 c=[0]*len(a)
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:c[i^j]+=x*y*BASIS[i&j]
 return tuple(c)
def sign(a):
 """Exact sign in the positive-real square-root embedding."""
 if len(a)==1:return (a[0]>0)-(a[0]<0)
 h=len(a)//2;p,q=a[:h],a[h:];sp,sq=sign(p),sign(q)
 if not sp:return sq
 if not sq:return sp
 if sp==sq:return sp
 D=PRIMES[len(a).bit_length()-2]
 return sp*sign(sub(mul(p,p),scale(mul(q,q),D)))
def sqrt7(a):return mul(a,surd(4))
def atom():
 # Coordinates multiplied by6.
 L=[(r(),r()),(r(6),r()),(r(),surd(1,6)),(r(6),surd(1,6)),
    (surd(1,-3),surd(1,3)),(add(r(6),surd(1,-3)),surd(1,3))]
 for s,t in product((-1,1),repeat=2):L.append((add(r(3),surd(3,s)),add(surd(1,3),surd(2,t))))
 return L

def build():
 L=atom();P=[]
 for (a,b),(c,d) in product(L,repeat=2):
  P.append((sub(sub(scale(a,4),scale(c,3)),sqrt7(d)),add(sub(scale(b,4),scale(d,3)),sqrt7(c))))
 # Coordinates multiplied by24.
 if len(set(P))!=100:raise ValueError('source collision')
 E=[];norms=[]
 for i,j in combinations(range(100),2):
  dx,dy=(sub(P[i][k],P[j][k]) for k in range(2))
  n=add(mul(dx,dx),mul(dy,dy));norms.append(n)
  if n==r(576):E.append((i,j))
 return P,E,norms
