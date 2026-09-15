"""Produce the frozen G19 union (F29+i); flat-basis exact arithmetic.

G19 geometry/solver adapted from source commit 2e26eadaa928d089c86462f567e3e29dfa9f0511.
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

def solve(n,edges,k,pins=()):
 adj=[set() for _ in range(n)]
 for a,b in edges:adj[a].add(b);adj[b].add(a)
 word=[-1]*n
 for a,c in pins:
  if word[a]>=0 and word[a]!=c:return None
  word[a]=c
 if any(word[a]>=0 and word[a]==word[b] for a,b in edges):return None
 def rec():
  free=[i for i,c in enumerate(word) if c<0]
  if not free:return tuple(word)
  domains={i:[c for c in range(k) if all(word[j]!=c for j in adj[i])] for i in free}
  v=min(free,key=lambda i:(len(domains[i]),-len(adj[i]),i))
  for c in domains[v]:
   word[v]=c;r=rec()
   if r:return r
  word[v]=-1
  return None
 return rec()

HERE=Path(__file__).resolve().parent

def produce():
 pts,_,old_edges,_=geometry()
 rows=[list(map(int,line.split()))[1:] for line in (HERE/'f29_points.tsv').read_text().splitlines() if line and not line.startswith('#')]
 frozen=[(scale(add(scalar(a),scale(mul(S,T),b)),F(1,12)),add(ONE,scale(add(scale(S,c),scale(T,d)),F(1,12)))) for a,b,c,d in rows]
 raw=pts+frozen;points=list(dict.fromkeys(raw));mp=[points.index(p) for p in raw];fm=mp[19:]
 edges=[];distances=[]
 for a,b in combinations(range(len(points)),2):
  d=norm(psub(points[a],points[b]));distances.append([a,b,[str(v) for v in d]])
  if d==ONE:edges.append((a,b))
 fe=[(a,b) for a,b in combinations(range(29),2) if norm(psub(frozen[a],frozen[b]))==ONE]
 inherited=sorted(set(old_edges)|{tuple(sorted((fm[a],fm[b]))) for a,b in fe})
 witnesses=[]
 for c in range(4):
  w=solve(29,fe,4,[(0,0),(25,1),(28,2),(22,c)])
  if w is not None:witnesses.append(w)
 four=solve(len(points),edges,4)
 if four is None:raise ValueError('ordinary four-colour preflight changed')
 five=list(four);five[0]=4
 return {'schema':'g19-f29-translation-gate-v1','coordinates':[[[str(v) for v in p] for p in q] for q in points],
  'edges':edges,'inherited_edges':inherited,'new_edges':sorted(set(edges)-set(inherited)),
  'f29_edges':fe,'f29_map':fm,'shared_vertices':[(i,v) for i,v in enumerate(fm) if v<19],
  'four_colouring':four,'five_colouring':five,'f29_extension_words':witnesses,
  'distance_sha256':sha256(json.dumps(distances,separators=(',',':'),sort_keys=True).encode()).hexdigest()}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 if a.out.exists():raise ValueError('output already exists')
 c=produce();a.out.write_text(json.dumps(c,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'points':len(c['coordinates']),'edges':len(c['edges']),'new_edges':c['new_edges'],'extension_words':len(c['f29_extension_words'])},sort_keys=True))
