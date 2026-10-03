"""Sparse integral polynomials in three named local indeterminates."""

class P:
 def __init__(self,terms=None):
  if any(type(v)is not int for v in (terms or {}).values()):raise TypeError('integral polynomial coefficients')
  self.c={k:v for k,v in (terms or {}).items() if v}
  if any(len(k)!=3 or any(type(x)is not int or x<0 for x in k) for k in self.c):raise ValueError('three nonnegative exponent slots')
 @staticmethod
 def cv(x):
  if isinstance(x,P):return x
  if type(x)is not int:raise TypeError('integral polynomial scalar')
  return P({(0,0,0):x})
 @staticmethod
 def var(i):
  if type(i)is not int or not 0<=i<3:raise ValueError('one of three local indeterminates')
  return P({tuple(int(j==i) for j in range(3)):1})
 def __add__(self,x):
  x=P.cv(x);d=dict(self.c)
  for k,v in x.c.items():
   d[k]=d.get(k,0)+v
   if not d[k]:del d[k]
  return P(d)
 __radd__=__add__
 def __neg__(self):return P({k:-v for k,v in self.c.items()})
 def __sub__(self,x):return self+-P.cv(x)
 def __rsub__(self,x):return P.cv(x)+-self
 def __mul__(self,x):
  x=P.cv(x);d={}
  for (a,b,c),v in self.c.items():
   for (i,j,k),w in x.c.items():
    key=(a+i,b+j,c+k);d[key]=d.get(key,0)+v*w
  return P(d)
 __rmul__=__mul__
 def __pow__(self,n):
  if type(n)is not int or n<0:raise ValueError('nonnegative integral exponent')
  y=P.cv(1);x=self
  while n:
   if n&1:y=y*x
   n//=2
   if n:x=x*x
  return y
 def __eq__(self,x):return self.c==P.cv(x).c
 def deriv(self,i):return P({tuple(v-int(j==i) for j,v in enumerate(k)):x*k[i] for k,x in self.c.items() if k[i]})
 def evaluate(self,values):
  maxima=[max((k[i] for k in self.c),default=0) for i in range(3)]
  powers=[[values[i]*0+1] for i in range(3)]
  for i in range(3):
   for j in range(maxima[i]):powers[i].append(powers[i][-1]*values[i])
  result=values[0]*0
  for k,c in self.c.items():result+=c*powers[0][k[0]]*powers[1][k[1]]*powers[2][k[2]]
  return result
 def reduced(self,R):
  if any(k[2] for k in R.c):raise ValueError('monic radical relation has root-independent right side')
  groups={}
  for (a,b,w),c in self.c.items():groups.setdefault(w,{})[(a,b,0)]=c
  result=P.cv(0)
  for w,terms in groups.items():result+=P(terms)*(R**(w//2))*(P.var(2)**(w%2))
  return result
 def rows(self):return [[*k,str(v)] for k,v in sorted(self.c.items())]

def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def dot(a,b,t):return (1-t)*sum((x*y for x,y in zip(a,b)),t*0)+t*sum(a,t*0)*sum(b,t*0)
def scale(v,x):return [a*x for a in v]
def add(a,b):return [x+y for x,y in zip(a,b)]
