"""Exact square roots and order in F=Q(z,r), z²=33, r²=-408+72z."""
from fractions import Fraction as Q
from math import isqrt
Z=(Q(0),)*4; O=(Q(1),)+Z[1:]; L=(-408,72)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def scale(a,k):return tuple(x*k for x in a)
def mul2(a,b):return a[0]*b[0]+33*a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def inv2(a):
 d=a[0]*a[0]-33*a[1]*a[1]
 if not d:raise ZeroDivisionError('zero element')
 return Q(a[0],d),Q(-a[1],d)
def mul(a,b):return add(mul2(a[:2],b[:2]),mul2(mul2(a[2:],b[2:]),L))+add(mul2(a[:2],b[2:]),mul2(a[2:],b[:2]))
def inv(a):
 c=inv2(sub(mul2(a[:2],a[:2]),mul2(mul2(a[2:],a[2:]),L)))
 return mul2(a[:2],c)+neg(mul2(a[2:],c))
def sign(a):return (a>0)-(a<0)
def sign2(a):
 x,y=a;sx,sy=sign(x),sign(y)
 if not sx:return sy
 if not sy or sx==sy:return sx
 return sx*sign(x*x-33*y*y)
def sign4(a):
 A,B=a[:2],a[2:];sx,sy=sign2(A),sign2(B)
 if not sx:return sy
 if not sy or sx==sy:return sx
 return sx*sign2(sub(mul2(A,A),mul2(mul2(B,B),L)))
def sqrtQ(a):
 a=Q(a)
 if a<0:return None
 n,d=isqrt(a.numerator),isqrt(a.denominator)
 return Q(n,d) if n*n==a.numerator and d*d==a.denominator else None
def sqrt2(a):
 x,y=map(Q,a)
 if y==0:
  u=sqrtQ(x)
  if u is not None:return u,Q(0)
  v=sqrtQ(x/33)
  return (Q(0),v) if v is not None else None
 delta=sqrtQ(x*x-33*y*y)
 if delta is None:return None
 for epsilon in [1,-1]:
  u=sqrtQ((x+epsilon*delta)/2)
  if u:
   out=u,y/(2*u)
   if mul2(out,out)!=(x,y):raise AssertionError('quadratic root')
   return out
 return None
def sqrt4(a):
 a=tuple(map(Q,a));A,B=a[:2],a[2:]
 if B==(0,0):
  u=sqrt2(A)
  if u is not None:out=u+(Q(0),Q(0))
  else:
   v=sqrt2(mul2(A,inv2(L)))
   if v is None:return None
   out=(Q(0),Q(0))+v
 else:
  d=sqrt2(sub(mul2(A,A),mul2(mul2(B,B),L)))
  if d is None:return None
  out=None
  for epsilon in [1,-1]:
   u=sqrt2(scale(add(A,scale(d,epsilon)),Q(1,2)))
   if u is not None and u!=(0,0):
    v=mul2(B,inv2(scale(u,2)));out=u+v;break
  if out is None:return None
 if mul(out,out)!=a:raise AssertionError('quartic root')
 return neg(out) if sign4(out)<0 else out

def norm(x,y):return add(mul(x,x),scale(mul(y,y),3))
def sigma(a):return tuple(a[:2])+neg(a[2:])
