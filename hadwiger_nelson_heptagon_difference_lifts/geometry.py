"""Q(t), t=exp(pi*i/21), Phi42=t^12+t^11-t^9-t^8+t^6-t^4-t^3+t+1."""
from fractions import Fraction as Q
from math import lcm,gcd
PHI=(1,1,0,-1,-1,0,1,0,-1,-1,0,1,1)
ZERO=(0,)*12;ONE=(1,)+ZERO[1:]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def scale(a,k):return tuple(k*x for x in a)
def reduce(v):
 v=list(v)+[0]*max(0,12-len(v))
 for j in range(len(v)-1,11,-1):
  a=v[j]
  if a:
   for k in range(12):v[j-12+k]-=a*PHI[k]
 return tuple(v[:12])
def mul(a,b):
 c=[0]*23
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:c[i+j]+=x*y
 return reduce(c)
def power(n):return reduce([0]*(n%42)+[1])
POW=tuple(power(n) for n in range(42))
def conj(a):
 out=ZERO
 for i,x in enumerate(a):out=add(out,scale(POW[-i%42],x))
 return out
def norm(a):return mul(a,conj(a))
def inv(a):
 # Exact linear solve for a*b=1 in the twelve-dimensional quotient.
 columns=[mul(a,POW[j]) for j in range(12)]
 m=[[Q(columns[j][i]) for j in range(12)]+[Q(i==0)] for i in range(12)]
 for j in range(12):
  k=next((i for i in range(j,12) if m[i][j]),None)
  if k is None:raise ZeroDivisionError
  m[j],m[k]=m[k],m[j];u=m[j][j];m[j]=[x/u for x in m[j]]
  for i in range(12):
   if i!=j and m[i][j]:
    u=m[i][j];m[i]=[x-u*y for x,y in zip(m[i],m[j])]
 b=tuple(row[-1] for row in m)
 assert mul(a,b)==ONE
 return b
def host():
 p=inv(sub(POW[24],POW[-24%42]))
 q=neg(mul(POW[-7%42],inv(sub(POW[6],POW[-6%42]))))
 r=neg(mul(POW[7],inv(sub(POW[12],POW[-12%42]))))
 return [mul(a,POW[6*j%42]) for a in [p,q,r] for j in range(7)]
def integerize(points):
 d=lcm(*(Q(x).denominator for p in points for x in p));out=[tuple(int(x*d) for x in p) for p in points]
 return out,d
def edges(points,d):
 return [(i,j) for i in range(len(points)) for j in range(i+1,len(points)) if norm(sub(points[i],points[j]))==scale(ONE,d*d)]
