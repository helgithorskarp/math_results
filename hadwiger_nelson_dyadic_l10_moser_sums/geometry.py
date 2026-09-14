"""Exact physical construction; real multiquadratic coefficients, no numerics."""
from fractions import Fraction as F
from itertools import product
from math import lcm

PRIMES=(2,3,5,11)
RAD=tuple(__import__('math').prod(p for k,p in enumerate(PRIMES)if i>>k&1)for i in range(16))
ZERO=(0,)*32
ONE=(1,)+(0,)*31

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,c):return tuple(x*c for x in a)
def conj(a):return a[:16]+tuple(-x for x in a[16:])
def rmul(a,b):
 out=[0]*16
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:out[i^j]+=RAD[i&j]*x*y
 return tuple(out)
def mul(a,b):
 x,y=a[:16],a[16:];u,v=b[:16],b[16:]
 return sub(rmul(x,u),rmul(y,v))+add(rmul(x,v),rmul(y,u))
def norm(a):return add(rmul(a[:16],a[:16]),rmul(a[16:],a[16:]))
def make(x=None,y=None):
 a=[0]*32
 for i,c in (x or {}).items():a[i]=F(c)
 for i,c in (y or {}).items():a[16+i]=F(c)
 return tuple(a)

OMEGA=make({0:F(1,2)},{2:F(1,2)})
ETA=make({0:F(5,6)},{8:F(1,6)})

def atoms():
 # Four corners of a 1 by sqrt(2) rectangle; two external tips;
 # two common-neighbour pairs on the diagonals.
 q=make(y={1:1});tip=make({1:F(-1,2)},{1:F(1,2)})
 L=[ZERO,ONE,q,add(ONE,q),tip,add(ONE,tip)]
 for sx,sy in product((-1,1),repeat=2):
  L.append(make({0:F(1,2),3:F(sx,6)},{1:F(1,2),2:F(sy,6)}))
 diamond=[ZERO,ONE,OMEGA,add(ONE,OMEGA)]
 M=diamond+[mul(ETA,p)for p in diamond[1:]]
 return L,M

def integral(points):
 den=lcm(*(F(x).denominator for p in points for x in p))
 return den,[tuple(int(x*den)for x in p)for p in points]

def exact_edges(den,points):
 es=[];target=den*den;weights=RAD+RAD
 for i,p in enumerate(points):
  for j in range(i+1,len(points)):
   d=sub(p,points[j])
   # Rational coefficient of x^2+y^2; a necessary exact equality.
   if sum(r*a*a for r,a in zip(weights,d))!=target:continue
   if norm(d)==(target,)+(0,)*15:es.append((i,j))
 return es
