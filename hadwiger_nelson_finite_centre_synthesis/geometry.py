from fractions import Fraction as F
from math import isqrt
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json,time
Z=(F(0),F(0));ONE=(F(1),F(0))
def c(n):return F(n),F(0)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def neg(x):return -x[0],-x[1]
def sub(x,y):return add(x,neg(y))
def mul(x,y):return x[0]*y[0]+33*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def scale(x,n):return x[0]*n,x[1]*n
def div(x,y):
 d=y[0]*y[0]-33*y[1]*y[1]
 return scale(mul(x,(y[0],-y[1])),1/d)
def sign(x):
 a,b=x
 if b==0:return (a>0)-(a<0)
 if a==0:return (b>0)-(b<0)
 if (a>0)==(b>0):return (a>0)-(a<0)
 d=a*a-33*b*b
 return ((a>0)-(a<0))*((d>0)-(d<0))
def qs(n):
 if n<0:return None
 a,b=isqrt(n.numerator),isqrt(n.denominator)
 return F(a,b) if a*a==n.numerator and b*b==n.denominator else None
@lru_cache(None)
def sqrt(x):
 a,b=x
 if b==0:
  r=qs(a)
  if r is not None:return r,F(0)
  r=qs(a/33)
  return None if r is None else (F(0),r)
 n=qs(a*a-33*b*b)
 if n is None:return None
 for z in [n,-n]:
  r=qs((a+z)/2)
  if r is not None and r:
   out=(r,b/(2*r))
   if mul(out,out)!=x:raise RuntimeError('sqrt wrong')
   return out
 return None
def dist(p,q):
 dx,dy=sub(p[0],q[0]),sub(p[1],q[1])
 return add(scale(mul(dx,dx),3),mul(dy,dy))
def centres(p,q):
 dx,dy=sub(q[0],p[0]),sub(q[1],p[1]);L=add(scale(mul(dx,dx),3),mul(dy,dy))
 if L==Z or sign(sub(c(5184),L))<0:return []
 k=sqrt(div(sub(c(5184),L),scale(L,12)))
 if k is None:return []
 m=(scale(add(p[0],q[0]),F(1,2)),scale(add(p[1],q[1]),F(1,2)))
 shifts=(neg(mul(dy,k)),scale(mul(dx,k),3))
 out=[(add(m[0],shifts[0]),add(m[1],shifts[1]))]
 if k!=Z:out.append((sub(m[0],shifts[0]),sub(m[1],shifts[1])))
 for v in out:
  if dist(v,p)!=c(1296) or dist(v,q)!=c(1296):raise RuntimeError('bad centre')
 return out
def enc(p):return [[str(v) for v in xy] for xy in p]
def seed():
 rows=json.loads(Path(__file__).with_name('seed.json').read_text())
 return [((F(a),F(b,3)),(F(cc),F(d))) for a,b,cc,d in rows]
