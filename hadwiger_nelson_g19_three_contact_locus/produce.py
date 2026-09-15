"""Enumerate all external unit-circle centres with three G19 neighbours.

G19 geometry adapted from its original author source at
2e26eadaa928d089c86462f567e3e29dfa9f0511.
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

from functools import lru_cache
@lru_cache(None)
def inverse(a):
 if a==Z:raise ZeroDivisionError('zero field element')
 cols=[mul(a,tuple(F(int(i==j)) for i in range(8))) for j in range(8)]
 mat=[[cols[j][i] for j in range(8)]+[F(i==0)] for i in range(8)]
 for j in range(8):
  k=next(i for i in range(j,8) if mat[i][j]);mat[j],mat[k]=mat[k],mat[j]
  q=mat[j][j];mat[j]=[v/q for v in mat[j]]
  for i in range(8):
   if i==j:continue
   q=mat[i][j]
   if q:mat[i]=[x-q*y for x,y in zip(mat[i],mat[j])]
 result=tuple(mat[i][8] for i in range(8))
 if mul(a,result)!=ONE:raise ValueError('inverse identity')
 return result

def produce():
 g,_,_,_=geometry();points=g[:];on=coll=0;stream=sha256();centre_counts={}
 for a,b,c in combinations(range(19),3):
  u=psub(g[b],g[a]);v=psub(g[c],g[a]);A=norm(u);B=norm(v);C=norm(psub(u,v));det=sub(mul(u[0],v[1]),mul(u[1],v[0]))
  good=det!=Z and mul(mul(A,B),C)==scale(mul(det,det),4)
  stream.update((f'{a},{b},{c}:{int(det==Z)}{int(good)}\n').encode());coll+=det==Z
  if not good:continue
  on+=1;factor=inverse(scale(det,2))
  off=(mul(sub(mul(A,v[1]),mul(B,u[1])),factor),mul(sub(mul(B,u[0]),mul(A,v[0])),factor))
  p=padd(g[a],off)
  if any(norm(psub(p,g[j]))!=ONE for j in [a,b,c]):raise ValueError('circumcentre')
  if p not in points:points.append(p)
  i=points.index(p);centre_counts[str(i)]=centre_counts.get(str(i),0)+1
 edges=[(a,b) for a,b in combinations(range(len(points)),2) if norm(psub(points[a],points[b]))==ONE]
 known=tuple(map(int,'0120123210111020202'));word=known+(3,3);five=(4,)+word[1:]
 if len(points)!=21 or any(word[a]==word[b] for a,b in edges):raise ValueError('frozen known-word extension')
 return {'schema':'g19-three-contact-locus-v1','new_points':[[[str(v) for v in co] for co in p] for p in points[19:]],
  'edges':edges,'collinear_triples':coll,'unit_radius_triples':on,'triple_truth_sha256':stream.hexdigest(),
  'centre_multiplicities':centre_counts,'four_colouring':word,'five_colouring':five}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--cnf',type=Path);a=p.parse_args()
 if a.out.exists():raise ValueError('output already exists')
 c=produce();a.out.write_text(json.dumps(c,indent=2,sort_keys=True)+'\n')
 if a.cnf:
  if a.cnf.exists():raise ValueError('CNF output exists')
  n=19+len(c['new_points']);clauses=[]
  def var(v,k):return 4*v+k+1
  for v in range(n):
   clauses.append([var(v,k) for k in range(4)])
   for j,k in combinations(range(4),2):clauses.append([-var(v,j),-var(v,k)])
  for u,v in c['edges']:
   for k in range(4):clauses.append([-var(u,k),-var(v,k)])
  for v,k in enumerate(c['four_colouring'][:19]):clauses.append([var(v,k)])
  a.cnf.write_text(f'p cnf {4*n} {len(clauses)}\n'+''.join(' '.join(map(str,x))+' 0\n' for x in clauses))
 print(json.dumps({'new_points':len(c['new_points']),'edges':len(c['edges']),'unit_radius_triples':c['unit_radius_triples'],'collinear_triples':c['collinear_triples']},sort_keys=True))
