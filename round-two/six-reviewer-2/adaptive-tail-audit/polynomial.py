"""Independent univariate Q[u] / Q(u) arithmetic; no CAS or author helper.

Ascending coefficients; fractions exact; normalized monic denominator;
Euclidean polynomial gcd. Closed operations, no interpolation/evaluation
used to prove universal coefficient identities.
"""
from fractions import Fraction as F
from itertools import permutations

def trim(a):
 a=list(map(F,a))
 while a and a[-1]==0:a.pop()
 return tuple(a)
def add(a,b):return trim([(a[i]if i<len(a)else 0)+(b[i]if i<len(b)else 0)for i in range(max(len(a),len(b)))])
def neg(a):return tuple(-v for v in a)
def mul(a,b):
 if not a or not b:return ()
 c=[F(0)]*(len(a)+len(b)-1)
 for i,v in enumerate(a):
  for j,w in enumerate(b):c[i+j]+=v*w
 return trim(c)
def divmodp(a,b):
 if not b:raise ZeroDivisionError('zero polynomial')
 r=list(a);q=[F(0)]*max(0,len(a)-len(b)+1)
 while r and len(r)>=len(b):
  i=len(r)-len(b);v=r[-1]/b[-1];q[i]=v
  for j,w in enumerate(b):r[i+j]-=v*w
  r=list(trim(r))
 return trim(q),trim(r)
def gcd(a,b):
 while b:a,b=b,divmodp(a,b)[1]
 return tuple(v/a[-1]for v in a)if a else()
def quotient(a,b):
 q,r=divmodp(a,b)
 if r:raise ValueError('nonexact polynomial quotient')
 return q
def evalp(a,u):
 out=F(0)
 for v in reversed(a):out=out*u+v
 return out
class Rat:
 def __init__(self,n=0,d=1):
  if isinstance(n,Rat):self.n,self.d=n.n,n.d;return
  n=trim(n if isinstance(n,(tuple,list))else[n]);d=trim(d if isinstance(d,(tuple,list))else[d])
  if not d:raise ZeroDivisionError('rational function denominator')
  if not n:self.n,self.d=(),(F(1),);return
  g=gcd(n,d);n=quotient(n,g);d=quotient(d,g);z=d[-1];self.n=tuple(v/z for v in n);self.d=tuple(v/z for v in d)
 def __add__(self,other):
  b=Rat(other);return Rat(add(mul(self.n,b.d),mul(b.n,self.d)),mul(self.d,b.d))
 __radd__=__add__
 def __neg__(self):return Rat(neg(self.n),self.d)
 def __sub__(self,other):return self+-Rat(other)
 def __rsub__(self,other):return Rat(other)+-self
 def __mul__(self,other):
  b=Rat(other);return Rat(mul(self.n,b.n),mul(self.d,b.d))
 __rmul__=__mul__
 def __truediv__(self,other):
  b=Rat(other);return Rat(mul(self.n,b.d),mul(self.d,b.n))
 def __rtruediv__(self,other):return Rat(other)/self
 def __pow__(self,n):
  if n<0:return (1/self)**(-n)
  out=Rat(1)
  for unused in range(n):out=out*self
  return out
 def __eq__(self,other):
  b=Rat(other);return self.n==b.n and self.d==b.d
 def polynomial(self):
  if self.d!=(F(1),):raise ValueError('not polynomial after clearing positive multiplier')
  return self.n
 def value(self,u):return evalp(self.n,u)/evalp(self.d,u)
 def record(self):return {'numerator':[str(v)for v in self.n],'denominator':[str(v)for v in self.d]}
 def sign(self):
  if not self.n:return 0
  if not all(v>=0 for v in self.d)or not self.d[0]>0:raise ValueError('denominator not coefficient-positive on u>=0')
  if all(v>=0 for v in self.n):return 1
  if all(v<=0 for v in self.n):return -1
  raise ValueError('numerator sign not coefficient-certified')

def determinant(A):
 n=len(A);total=()
 for p in permutations(range(n)):
  term=(F((-1)**sum(p[i]>p[j]for i in range(n)for j in range(i+1,n))),)
  for i,j in enumerate(p):term=mul(term,A[i][j])
  total=add(total,term)
 return total
