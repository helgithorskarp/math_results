#!/usr/bin/env python3
"""Independent transformed-source arithmetic and full graph DSATUR census."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations,product
import json,time,hashlib

# Basis indexed by bits sqrt3,sqrt11,Y, where Y^2=2-sqrt3/2.
def k(x=0):return (Q(x),)+(Q(0),)*7
Z=k();O=k(1);S=tuple(Q(i==1) for i in range(8));T=tuple(Q(i==2) for i in range(8));Y=tuple(Q(i==4) for i in range(8))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def scale(a,x):return tuple(v*Q(x) for v in a)
def mul(a,b):
 r=[Q(0)]*8
 for i,x in enumerate(a):
  if not x:continue
  for j,y in enumerate(b):
   if not y:continue
   common=i&j;out=i^j;v=x*y*(3 if common&1 else 1)*(11 if common&2 else 1)
   if common&4:
    r[out]+=2*v;r[out^1]-=v*Q(3 if out&1 else 1,2)
   else:r[out]+=v
 return tuple(r)
def d2(p,q):
 d=[sub(a,b) for a,b in zip(p,q)];return add(mul(d[0],d[0]),mul(d[1],d[1]))
def geometry():
 G=[(Z,Z),(O,Z),(k(Q(1,2)),scale(S,Q(1,2))),(k(Q(-1,2)),scale(S,Q(1,2))),(k(-1),Z),(k(Q(-1,2)),scale(S,Q(-1,2))),(k(Q(1,2)),scale(S,Q(-1,2))),(k(Q(1,6)),scale(T,Q(1,6))),(add(k(Q(-1,12)),scale(mul(S,T),Q(-1,12))),sub(scale(S,Q(1,12)),scale(T,Q(1,12)))),(add(k(Q(-1,12)),scale(mul(S,T),Q(1,12))),sub(scale(S,Q(-1,12)),scale(T,Q(1,12))))]
 caps=[(Z,Z),(scale(add(O,S),Q(1,2)),Y),(scale(sub(O,S),Q(1,2)),Y),(O,Z)]
 B=caps[1:3];BN=['P1','P2']
 for i,(a,b) in enumerate(zip(caps,caps[1:])):
  mid=tuple(scale(add(x,y),Q(1,2)) for x,y in zip(a,b));dx,dy=[sub(y,x) for x,y in zip(a,b)];off=(scale(mul(neg(dy),S),Q(1,6)),scale(mul(dx,S),Q(1,6)))
  B += [tuple(add(x,y) for x,y in zip(mid,off)),tuple(sub(x,y) for x,y in zip(mid,off))];BN += ['X'+str(i),'Y'+str(i)]
 B=[(add(sub(y,Y),k(Q(1,2))),sub(k(Q(1,2)),x)) for x,y in B]
 pts=list(G);bm=[]
 for b in B:
  if b not in pts:pts.append(b)
  bm.append(pts.index(b))
 edges=[(a,b) for a,b in combinations(range(len(pts)),2) if d2(pts[a],pts[b])==O]
 ge=[e for e in edges if e[1]<10];be=[(i,j) for i,j in combinations(range(8),2) if d2(B[i],B[j])==O]
 inherited=set(ge)|{tuple(sorted((bm[a],bm[b]))) for a,b in be}
 return pts,edges,ge,be,bm,BN,sorted(set(edges)-inherited)
def words(n,E,pins):
 adj=[set() for _ in range(n)]
 for a,b in E:adj[a].add(b);adj[b].add(a)
 c=[-1]*n
 for i,x in pins.items():c[i]=x
 if any(c[a]>=0 and c[a]==c[b] for a,b in E):return []
 out=[]
 def walk():
  U=[v for v in range(n) if c[v]<0]
  if not U:out.append(tuple(c));return
  banned={v:{c[u] for u in adj[v] if c[u]>=0} for v in U}
  v=max(U,key=lambda v:(len(banned[v]),len(adj[v]),-v))
  for col in range(4):
   if col not in banned[v]:c[v]=col;walk()
  c[v]=-1
 walk();return out

def canon(w):
 d={};return ''.join(str(d.setdefault(c,len(d))) for c in w)
def digest(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def sethash(R):return hashlib.sha256(''.join(''.join(map(str,w))+'\n' for w in sorted(R)).encode()).hexdigest()
def main():
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--compare',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args()
 pts,E,GE,BE,bm,BN,extra=geometry();Gterm=[0,1,3,4,5,7,8,9];Bterm=list(range(2,8));iface=Gterm+[bm[x] for x in [2,3,6,7]]
 gw=words(10,GE,{0:0,1:1});bw=words(8,BE,{4:0,5:1});uw=words(len(pts),E,{0:0,1:1})
 gr={tuple(w[v] for v in Gterm) for w in gw};br={tuple(w[v] for v in Bterm) for w in bw}
 base={g+b[:2]+b[4:] for g in gr for b in br};joined={tuple(w[v] for v in iface) for w in uw};lost=base-joined
 if not joined<=base:raise ValueError('projected containment')
 rows=[[[str(v) for v in c] for c in p] for p in pts]
 ds=[[str(v) for v in d2(pts[i],pts[j])] for i,j in combinations(range(len(pts)),2)]
 r={'points':len(pts),'unit_edges':len(E),'point_hash':digest(rows),'edge_hash':digest(E),'distance_hash':digest(ds),'input_joint_edge_pinned':len(base),'composite_joint_edge_pinned':len(joined),'lost_joint_edge_pinned':len(lost),'input_joint_canonical':len({canon(w) for w in base}),'composite_joint_canonical':len({canon(w) for w in joined}),'lost_joint_canonical':len({canon(w) for w in lost}),'union_full_words_edge_pinned':len(uw),'product_relation_hash':sethash(base),'composite_relation_hash':sethash(joined),'lost_relation_hash':sethash(lost)}
 if a.compare:
  expected=json.loads(a.compare.read_text())
  for k,v in r.items():
   if expected[k]!=v:raise ValueError('producer/checker mismatch '+k)
 text=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(text)
 print(text,end='')
if __name__=='__main__':main()
