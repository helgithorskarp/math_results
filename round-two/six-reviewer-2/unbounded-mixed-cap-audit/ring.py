"""Three-variable exact rational arithmetic; adapted from OWN9723 quadrant.py.
Original-variable factoring precedes substitution. No new author imports.
Fixed: 512 final monomials per polynomial, degree 180; no modular arithmetic.
"""
from fractions import Fraction as F
from math import gcd,lcm,comb
from itertools import product,permutations
from linear import need,digest
FACTORS=[];INDEX={};ZERO=(0,0,0)
def clean(p):
 need(all(type(v)!=float for v in p.values()),'floats are not exact coefficient inputs')
 p={k:F(v) for k,v in p.items() if v};need(len(p)<=512,'fixed 512 monomial guard');need(all(len(k)==3 and min(k)>=0 and max(k)<=180 for k in p),'fixed degree guard');return p
def const(x):return clean({ZERO:x})
def add(p,q):
 z=dict(p)
 for k,v in q.items():z[k]=z.get(k,F(0))+v
 return clean(z)
def mul(p,q):
 z={}
 for a,v in p.items():
  for b,w in q.items():
   k=tuple(x+y for x,y in zip(a,b));z[k]=z.get(k,F(0))+v*w
 return clean(z)
def div(p,q):
 need(q,'nonzero divisor');out={};z=dict(p);lead=max(q)
 while z:
  top=max(z);d=tuple(a-b for a,b in zip(top,lead))
  if min(d)<0:return None
  v=z[top]/q[lead];out[d]=out.get(d,F(0))+v
  for a,w in q.items():
   k=tuple(x+y for x,y in zip(a,d));z[k]=z.get(k,F(0))-v*w
   if not z[k]:del z[k]
 return clean(out)
def register(p):
 d=lcm(*(v.denominator for v in p.values()));g=0
 for v in p.values():g=gcd(g,int(v*d))
 scale=F(g,d);p={k:v/scale for k,v in p.items()};key=tuple(sorted(p.items()))
 if key not in INDEX:INDEX[key]=len(FACTORS);FACTORS.append(p)
 return INDEX[key],scale
def times(p,e):
 for i,k in sorted(e.items()):
  for _ in range(k):p=mul(p,FACTORS[i])
 return p
class R:
 def __init__(self,p=0,e=None):
  if isinstance(p,R):self.p=p.p;self.e=p.e;return
  p=clean(p if isinstance(p,dict) else const(p));e={i:k for i,k in (e or {}).items() if k}
  if not p:e={}
  else:
   for i in sorted(tuple(e)):
    while e.get(i,0):
     new=div(p,FACTORS[i])
     if new is None:break
     p=new;e[i]-=1
     if not e[i]:del e[i]
  self.p=p;self.e=e
 def __add__(a,b):
  b=R(b);e={i:max(a.e.get(i,0),b.e.get(i,0)) for i in a.e.keys()|b.e.keys()};return R(add(times(a.p,{i:k-a.e.get(i,0) for i,k in e.items()}),times(b.p,{i:k-b.e.get(i,0) for i,k in e.items()})),e)
 __radd__=__add__
 def __neg__(a):return R({k:-v for k,v in a.p.items()},a.e)
 def __sub__(a,b):return a+-R(b)
 def __rsub__(a,b):return R(b)+-a
 def __mul__(a,b):
  b=R(b);ap=a.p;bp=b.p;ae=dict(a.e);be=dict(b.e)
  for p,e,which in [(ap,be,0),(bp,ae,1)]:
   for i in sorted(tuple(e)):
    while e.get(i,0):
     new=div(p,FACTORS[i])
     if new is None:break
     p=new;e[i]-=1
     if not e[i]:del e[i]
   if which==0:ap=p
   else:bp=p
  return R(mul(ap,bp),{i:ae.get(i,0)+be.get(i,0) for i in ae.keys()|be.keys()})
 __rmul__=__mul__
 def __truediv__(a,b):
  b=R(b);need(b.p,'nonzero rational divisor')
  if len(b.p)==1 and ZERO in b.p:return R({k:v/b.p[ZERO] for k,v in times(a.p,b.e).items()},a.e)
  e=dict(a.e);bp=dict(b.p);powers=tuple(min(k[j] for k in bp) for j in range(3))
  for j,k in enumerate(powers):
   if k:
    unit=tuple(int(i==j) for i in range(3));i,sc=register({unit:1});e[i]=e.get(i,0)+k
  bp={tuple(k[j]-powers[j] for j in range(3)):v for k,v in bp.items()}
  if len(bp)==1 and ZERO in bp:s=bp[ZERO]
  else:
   i,s=register(bp);e[i]=e.get(i,0)+1
  return R({k:v/s for k,v in times(a.p,b.e).items()},e)
 def __rtruediv__(a,b):return R(b)/a
 def __pow__(a,k):
  need(type(k)==int and k>=0,'integer exponent');z=R(1)
  for _ in range(k):z=z*a
  return z
 def __eq__(a,b):return not (a-R(b)).p

def shifted(p,boundary=False):
 """r=3+u,l=2+v,q=12+4u+4v+w; boundary r=2,q=8+4v+w.
Expand original monomials by multinomial coefficients; guard final result.
"""
 out={};r0=2 if boundary else 3;q0=8 if boundary else 12
 for (a,b,c),v in p.items():
  for i in (range(a+1) if not boundary else (0,)):
   ra=F(r0**a) if boundary else F(comb(a,i)*3**(a-i))
   for j in range(b+1):
    lb=comb(b,j)*2**(b-j)
    for x in (range(c+1) if not boundary else (0,)):
     for y in range(c-x+1):
      for z in range(c-x-y+1):
       d=c-x-y-z;mult=comb(c,x)*comb(c-x,y)*comb(c-x-y,z)*q0**d*4**(x+y)
       k=(i+x,j+y,z);out[k]=out.get(k,F(0))+v*ra*lb*mult
 return clean(out)
def record(p):return [[*k,str(v)] for k,v in sorted(p.items())]
def evaluate(p,x):return sum(v*product_power(k,x) for k,v in p.items())
def product_power(k,x):
 z=F(1)
 for a,b in zip(k,x):z*=b**a
 return z

def determinant(A):
 total=R(0);n=len(A)
 for p in permutations(range(n)):
  z=R((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))
  for i in range(n):z*=A[i][p[i]]
  total+=z
 return total

def positive(r,boundary=False):
 p=shifted(r.p,boundary);need(p.get(ZERO,0)>0 and all(v>0 for v in p.values()),'complete shifted coefficient positivity')
 den=[]
 for i,k in sorted(r.e.items()):
  f=shifted(FACTORS[i],boundary);need(f.get(ZERO,0)>0 and all(v>0 for v in f.values()),'positive denominator factor');den.append({'power':k,'coefficients':record(f)})
 return {'original_numerator':record(r.p),'numerator':record(p),'denominator_factors':den,'terms':len(p),'numerator_sha256':digest(record(p))}
