from fractions import Fraction as F
from pathlib import Path
from itertools import product,combinations
import json,time
PRIMES=(2,3,11)
RAD=[1,2,3,6,11,22,33,66]
FAC=[[RAD[i&j] for j in range(8)] for i in range(8)]
ZERO=(0,)*8
PZERO=(0,)*16
ONE=(1,)+(0,)*15

def radd(a,b):return tuple(x+y for x,y in zip(a,b))
def rneg(a):return tuple(-v for v in a)
def mul(a,b):
 out=[0]*8
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:out[i^j]+=FAC[i][j]*x*y
 return tuple(out)
def cmul(a,b):
 x,y=a[:8],a[8:];u,v=b[:8],b[8:]
 return radd(mul(x,u),rneg(mul(y,v)))+radd(mul(x,v),mul(y,u))
def conj(a):return a[:8]+rneg(a[8:])
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def norm(a):return radd(mul(a[:8],a[:8]),mul(a[8:],a[8:]))
def power(a,k):
 if k<0:a=conj(a);k=-k
 p=ONE
 for _ in range(k):p=cmul(p,a)
 return p

def palette():
 rho=(F(1,2),0,0,0,0,0,0,0)+(0,0,F(1,2),0,0,0,0,0)
 eta=(0,0,0,0,0,0,F(1,6),0)+(0,0,F(1,6),0,0,0,0,0)
 sigma=(0,F(1,4),0,F(1,4),0,0,0,0)+(0,F(-1,4),0,F(1,4),0,0,0,0)
 tau=(0,0,0,F(1,3),0,0,0,0)+(0,0,F(1,3),0,0,0,0,0)
 for a in (rho,eta,sigma,tau):
  if norm(a)!=(1,0,0,0,0,0,0,0):raise ValueError('Nonunit generator')
 if power(rho,6)!=ONE or power(sigma,24)!=ONE:raise ValueError('Order')
 A={cmul(power(rho,k),power(eta,j)) for k,j in product(range(6),range(-2,3))}
 B={cmul(power(sigma,k),power(tau,j)) for k,j in product(range(24),range(-1,2))}
 def integer(p):
  if any(F(x*12).denominator!=1 for x in p):raise ValueError('Noninteger direction')
  return tuple(int(x*12) for x in p)
 return sorted(map(integer,A)),sorted(map(integer,B))

def unit_edges(points,directions):
 idx={tuple(p):i for i,p in enumerate(points)};es=[]
 if len(idx)!=len(points):raise ValueError('Repeated point')
 for i,p in enumerate(points):
  for d in directions:
   j=idx.get(add(p,d))
   if j is not None and i<j:es.append([i,j])
 return sorted(es)
