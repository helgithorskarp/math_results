"""Small independent QQ[h,q] arithmetic; exact division only by known factors."""
from fractions import Fraction as F
from polycheck import P
ONE=P({(0,0):F(1)});ZERO=P({})
def exact_div(a,b):
 if not b.t:raise ZeroDivisionError
 r=a.t.copy();out={};m=max(b.t);c=b.t[m]
 while r:
  u=max(r)
  if any(u[i]<m[i]for i in range(2)):return None
  v=tuple(u[i]-m[i]for i in range(2));z=r[u]/c;out[v]=out.get(v,0)+z
  for w,d in b.t.items():
   t=tuple(w[i]+v[i]for i in range(2));r[t]=r.get(t,0)-z*d
   if not r[t]:del r[t]
 return P(out)
def key(p):return tuple(sorted(p.t.items()))
class R:
 def __init__(self,n=0,d=None):
  self.n=n if isinstance(n,P)else P({(0,0):F(n)})
  self.d={}if d is None else d.copy()
  if not self.n.t:self.d={};return
  for k,(p,e)in list(self.d.items()):
   while e:
    z=exact_div(self.n,p)
    if z is None:break
    self.n=z;e-=1
   if e:self.d[k]=(p,e)
   else:del self.d[k]
 @staticmethod
 def coerce(o):return o if isinstance(o,R)else R(o)
 @staticmethod
 def monic(p):
  if not p.t:raise ZeroDivisionError
  c=p.t[max(p.t)];return P({m:v/c for m,v in p.t.items()}),c
 def __neg__(self):return R(-self.n,self.d)
 def __add__(self,o):
  o=R.coerce(o);d=self.d.copy()
  for k,(p,e)in o.d.items():d[k]=(p,max(e,d.get(k,(p,0))[1]))
  def factor(side):
   f=ONE
   for k,(p,e)in d.items():
    for _ in range(e-side.d.get(k,(p,0))[1]):f=f*p
   return f
  return R(self.n*factor(self)+o.n*factor(o),d)
 __radd__=__add__
 def __sub__(self,o):return self+-R.coerce(o)
 def __rsub__(self,o):return R.coerce(o)+-self
 def __mul__(self,o):
  o=R.coerce(o);d=self.d.copy()
  for k,(p,e)in o.d.items():d[k]=(p,e+d.get(k,(p,0))[1])
  return R(self.n*o.n,d)
 __rmul__=__mul__
 def __truediv__(self,o):
  o=R.coerce(o);n=self.n
  for p,e in o.d.values():
   for _ in range(e):n=n*p
  p,c=R.monic(o.n);n=n*P({(0,0):1/c});d=self.d.copy()
  if len(p.t)==1 and (0,0)in p.t:return R(n,d)
  k=key(p);d[k]=(p,1+d.get(k,(p,0))[1]);return R(n,d)
 def __rtruediv__(self,o):return R.coerce(o)/self
 def __pow__(self,k):
  if type(k)is not int or k<0:raise ValueError('power')
  r=R(1)
  for _ in range(k):r=r*self
  return r
 def denominator(self):
  d=ONE
  for p,e in self.d.values():
   for _ in range(e):d=d*p
  return d
 def value(self,h,q):return self.n.evaluate(h,q)/self.denominator().evaluate(h,q)
 def same_pair(self,n,d):return not (self.n*d-n*self.denominator()).t
 def iszero(self):return not self.n.t
H=R(P({(1,0):1}));Q=R(P({(0,1):1}))
