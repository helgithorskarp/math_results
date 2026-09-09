"""Exact five-digit geometry in Z[omega], omega^2=omega-1.

Sparse bivariate polynomials use (x exponent,y exponent) integer keys.
Point labels are lexicographic words over the ordered triangle (0,1,omega).
"""
from itertools import product
from math import gcd
from functools import reduce
T=((0,0),(1,0),(0,1))
U=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
D=((0,0),)+U
LABELS=tuple(product(range(3),repeat=5))
def emul(z,w):
 a,b=z;c,d=w
 return a*c-b*d,a*d+b*c+b*d
def canon(row):return min(tuple(emul(u,d) for d in row) for u in U)
def add(a,b,scale=1):
 c=dict(a)
 for k,v in b.items():c[k]=c.get(k,0)+scale*v
 return {k:v for k,v in c.items() if v}
def mul(a,b):
 c={}
 for (i,j),v in a.items():
  for (k,l),w in b.items():c[i+k,j+l]=c.get((i+k,j+l),0)+v*w
 return {k:v for k,v in c.items() if v}
def scale(a,s):return {k:v*s for k,v in a.items() if v*s}
def primitive(a):
 a={k:v for k,v in a.items() if v}
 if not a:return ()
 g=reduce(gcd,a.values(),0)
 if a[max(a)]<0:g=-g
 return tuple((i,j,v//g) for (i,j),v in sorted(a.items()))
def decode(p):return {(i,j):c for i,j,c in p}
def powers():
 C,D={ (0,0):1 },{}
 out=[]
 for j in range(5):
  out.append((C,D));C,D=add(mul({(1,0):1},C),mul({(0,1):1},D),-3),add(mul({(0,1):1},C),mul({(1,0):1},D))
 return out
POWERS=powers()
def distance_event(row):
 A,B={},{}
 for (a,b),(C,D) in zip(row,POWERS):
  A=add(A,add(scale(C,2*a+b),scale(D,-3*b)))
  B=add(B,add(scale(C,b),scale(D,2*a+b)))
 return primitive(add(add(mul(A,A),mul(B,B),3),{(0,0):4},-1))
def inventory():
 rows=tuple(sorted({canon(r) for r in product(D,repeat=5) if any(a or b for a,b in r)}))
 ids={r:i for i,r in enumerate(rows)}; edges=[[] for _ in rows]
 for i,a in enumerate(LABELS):
  for j in range(i):
   b=LABELS[j];r=canon(tuple((T[x][0]-T[y][0],T[x][1]-T[y][1]) for x,y in zip(a,b)))
   edges[ids[r]].append((j,i))
 return rows,edges
