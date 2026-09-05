"""Exact real biquadratic F=Q(sqrt33,sqrt5), K=F(alpha), alpha^2=-3."""
from fractions import Fraction as Q
from math import isqrt
Z=(Q(0),)*4;ONE=(Q(1),Q(0),Q(0),Q(0));RAD=(33,5)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def sub(x,y):return add(x,neg(y))
def scale(x,c):return tuple(c*a for a in x)
def mul(x,y):
 z=[Q(0)]*4
 for i,a in enumerate(x):
  if a:
   for j,b in enumerate(y):
    if b:z[i^j]+=a*b*(33 if i&j&1 else 1)*(5 if i&j&2 else 1)
 return tuple(z)
def radd(x,y):return x[0]+y[0],x[1]+y[1]
def rscale(x,c):return x[0]*c,x[1]*c
def rmul(x,y):return x[0]*y[0]+33*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def rinv(x):
 d=x[0]*x[0]-33*x[1]*x[1]
 if not d:raise ZeroDivisionError()
 return x[0]/d,-x[1]/d

def inv(x):
 a,b=x[:2],x[2:];n=radd(rmul(a,a),rscale(rmul(b,b),-5));ni=rinv(n)
 return rmul(a,ni)+rscale(rmul(b,ni),-1)

def qs(v):
 v=Q(v)
 if v<0:return None
 a,b=isqrt(v.numerator),isqrt(v.denominator)
 return Q(a,b) if a*a==v.numerator and b*b==v.denominator else None

def rs(x):
 a,b=x
 if b==0:
  t=qs(a)
  if t is not None:return t,Q(0)
  t=qs(a/33)
  return None if t is None else (Q(0),t)
 n=qs(a*a-33*b*b)
 if n is None:return None
 for sign in (1,-1):
  c=qs((a+sign*n)/2)
  if c is not None and c:
   out=(c,b/(2*c))
   if rmul(out,out)==x:return out
 return None

def sqrt(x):
 a,b=x[:2],x[2:]
 if b==(0,0):
  c=rs(a)
  if c is not None:return c+(Q(0),Q(0))
  c=rs(rscale(a,Q(1,5)))
  return None if c is None else (Q(0),Q(0))+c
 n=rs(radd(rmul(a,a),rscale(rmul(b,b),-5)))
 if n is None:return None
 for sign in (1,-1):
  c=rs(rscale(radd(a,rscale(n,sign)),Q(1,2)))
  if c is not None and c!=(0,0):
   out=c+rmul(b,rscale(rinv(c),Q(1,2)))
   if mul(out,out)==x:return out
 return None

KZ=(Z,Z);KONE=(ONE,Z)
def kadd(x,y):return add(x[0],y[0]),add(x[1],y[1])
def kneg(x):return neg(x[0]),neg(x[1])
def ksub(x,y):return kadd(x,kneg(y))
def kscale(x,c):return scale(x[0],c),scale(x[1],c)
def kmul(x,y):return sub(mul(x[0],y[0]),scale(mul(x[1],y[1]),3)),add(mul(x[0],y[1]),mul(x[1],y[0]))
def norm(x):return add(mul(x[0],x[0]),scale(mul(x[1],x[1]),3))
def e(x):
 a,b,c,d=x
 return (Q(a,72),Q(b,72),Q(0),Q(0)),(Q(c,72),Q(d,216),Q(0),Q(0))
U=((Q(7,8),Q(0),Q(0),Q(0)),(Q(0),Q(0),Q(1,8),Q(0)))

def circles(x,y):
 w=ksub(e(x),kmul(U,e(y)));d=norm(w)
 if d==Z:
  assert w==KZ
  return []
 f=scale(mul(d,sub(scale(ONE,4),d)),Q(1,3));t=sqrt(f)
 if t is None:return []
 assert mul(t,t)==f
 alpha_term=(Z,scale(mul(t,inv(d)),Q(1,2)))
 off=kmul(w,alpha_term);mid=kscale(w,Q(1,2))
 out=list(dict.fromkeys((kadd(mid,off),ksub(mid,off))))
 for h in out:assert norm(h)==ONE and norm(ksub(h,w))==ONE
 return out

def encode(x):return [[str(c) for c in z] for z in x]
