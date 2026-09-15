"""Reconstruct the one fixed host placement with flat-basis arithmetic.

G19 formulas adapted from the source 2e26eadaa928d089c86462f567e3e29dfa9f0511.
"""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import sys
import argparse
from hashlib import sha256
from math import factorial

# Basis s^a t^b y^c, s^2=3,t^2=11,y^2=2-s/2, a,b,c in {0,1}.
def scalar(x): return (F(x),)+(F(0),)*7
Z=scalar(0); ONE=scalar(1)
S=(F(0),F(1))+(F(0),)*6
T=(F(0),)*2+(F(1),)+(F(0),)*5
Y=(F(0),)*4+(F(1),)+(F(0),)*3
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def scale(a,k):return tuple(x*k for x in a)
def mul(a,b):
 out=[F(0)]*8
 for i,x in enumerate(a):
  if not x:continue
  for j,y in enumerate(b):
   if not y:continue
   k=i^j;coef=x*y*(3 if i&j&1 else 1)*(11 if i&j&2 else 1)
   if i&j&4:
    out[k]+=2*coef
    out[k^1]-=coef*F(3 if k&1 else 1,2)
   else:out[k]+=coef
 return tuple(out)
def psub(p,q):return sub(p[0],q[0]),sub(p[1],q[1])
def padd(p,q):return add(p[0],q[0]),add(p[1],q[1])
def cmul(p,q):return sub(mul(p[0],q[0]),mul(p[1],q[1])),add(mul(p[0],q[1]),mul(p[1],q[0]))
def norm(p):return add(mul(p[0],p[0]),mul(p[1],p[1]))

MROWS=((0,0,0,0),(12,0,0,0),(6,0,6,0),(18,0,6,0),(10,0,0,2),(5,-1,5,1),(15,-1,5,3),(6,0,-6,0),(12,0,12,0),(20,0,0,4),(-5,-1,5,-1))
def geometry():
 m=[(scale(add(scalar(a),scale(mul(S,T),b)),F(1,12)),scale(add(scale(S,c),scale(T,d)),F(1,12))) for a,b,c,d in MROWS]
 caps=[(Z,Z),(scale(add(ONE,S),F(1,2)),Y),(scale(sub(ONE,S),F(1,2)),Y),(ONE,Z)]
 p=caps[1:3]
 for a,b in zip(caps,caps[1:]):
  dx,dy=psub(b,a);mid=tuple(scale(v,F(1,2)) for v in padd(a,b));off=(scale(mul(neg(dy),S),F(1,6)),scale(mul(dx,S),F(1,6)))
  p.extend([padd(mid,off),psub(mid,off)])
 u=(scale(S,F(-1,2)),scalar(F(-1,2)))
 p=[padd((Z,ONE),cmul(u,psub(v,caps[1]))) for v in p]
 raw=m+p;pts=list(dict.fromkeys(raw));mp=[pts.index(v) for v in raw]
 edges=[(i,j) for i,j in combinations(range(len(pts)),2) if norm(psub(pts[i],pts[j]))==ONE]
 inherited=set()
 for block in [mp[:11],mp[11:]]:
  for i,j in combinations(block,2):
   if norm(psub(pts[i],pts[j]))==ONE:inherited.add(tuple(sorted((i,j))))
 return pts,mp,edges,sorted(inherited)

from math import lcm
HERE=Path(__file__).resolve().parent

def twice_product(a,b):
 out=[0]*8
 for i,x in enumerate(a):
  if not x:continue
  for j,y in enumerate(b):
   if not y:continue
   k=i^j;z=x*y*(3 if i&j&1 else 1)*(11 if i&j&2 else 1)
   if i&j&4:out[k]+=4*z;out[k^1]-=(3 if k&1 else 1)*z
   else:out[k]+=2*z
 return tuple(out)

def twice_norm(p,q):
 dx=tuple(a-b for a,b in zip(p[0],q[0]));dy=tuple(a-b for a,b in zip(p[1],q[1]))
 return tuple(a+b for a,b in zip(twice_product(dx,dx),twice_product(dy,dy)))

def generate():
 g,_,ge,_=geometry();rows=[list(map(int,line.split()))[1:] for line in (HERE/'host_points.tsv').read_text().splitlines() if line and not line.startswith('#')]
 ST=mul(S,T);u=cmul(psub(g[10],g[7]),(Z,scale(ST,F(-1,11))))
 if norm(u)!=ONE:raise ValueError('rotation norm')
 h=[]
 for a,b,c,d in rows:
  z=(scale(add(scale(S,a),scale(T,b)),F(1,36)),scale(add(scalar(c),scale(ST,d)),F(1,36)))
  h.append(padd(g[7],cmul(u,z)))
 if h[0]!=g[7] or h[1]!=g[10]:raise ValueError('anchor match')
 points=list(dict.fromkeys(g+h));mapping=[points.index(p) for p in g+h]
 D=lcm(*(x.denominator for p in points for v in p for x in v));ip=[tuple(tuple(int(x*D) for x in v) for v in p) for p in points]
 target=(2*D*D,)+(0,)*7
 edges=[(a,b) for a,b in combinations(range(len(ip)),2) if twice_norm(ip[a],ip[b])==target]
 return ip,D,edges,mapping

def cnf(n,edges,k=4):
 def var(v,c):return k*v+c+1
 out=[]
 for v in range(n):
  out.append([var(v,c) for c in range(k)])
  for a,b in combinations(range(k),2):out.append([-var(v,a),-var(v,b)])
 for a,b in edges:
  for c in range(k):out.append([-var(a,c),-var(b,c)])
 for v in range(3):out.append([var(v,v)])
 return f'p cnf {k*n} {len(out)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in out)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--cnf',type=Path);a=p.parse_args();points,D,edges,mapping=generate()
 if a.cnf:
  if a.cnf.exists():raise ValueError('output exists')
  a.cnf.write_text(cnf(len(points),edges))
 print(json.dumps({'points':len(points),'edges':len(edges),'denominator':D,'shared':[ [j,k] for j,k in enumerate(mapping[19:]) if k<19]},sort_keys=True))
