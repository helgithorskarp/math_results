#!/usr/bin/env python3
"""Independent integer Heron-triangle audit of all unit-circle centers."""
from pathlib import Path
from fractions import Fraction as Q
from math import comb
from collections import Counter,defaultdict
from hashlib import sha256
import json,time
ROOT=Path(__file__).resolve().parent.parent
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def sub(x,y):return (x[0]-y[0],x[1]-y[1])
def mul(x,y):return (x[0]*y[0]+33*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def scale(x,c):return tuple(c*a for a in x)
def inv(x):
 n=x[0]*x[0]-33*x[1]*x[1];return (Q(x[0],n),Q(-x[1],n))
def positive(x):
 a,b=x
 if a>=0 and b>=0:return bool(a or b)
 if a<=0 and b<=0:return False
 return a*a>33*b*b if a>0 else 33*b*b>a*a

def inputs():
 pts={}
 for n,pin in [(159,'4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02'),(214,'97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f')]:
  raw=(ROOT/f'hadwiger_nelson_nonmono159_214_lowden2/points{n}.tsv').read_bytes();assert sha256(raw).hexdigest()==pin
  rows=[]
  for line in raw.decode().splitlines():
   if not line or line.startswith('#'):continue
   x=list(map(int,line.split()));assert len(x)==16 and all(x[k]==0 for k in range(16) if k not in (0,5,9,12));rows.append(tuple(x[k] for k in (0,5,9,12)))
  assert len(rows)==len(set(rows))==n;pts[n]=rows
 A=[tuple(6*x for x in p) for p in pts[159]]
 # (5+i sqrt(11))/6 multiplication at scale 72.
 for a,b,c,d in pts[159]:
  p=(5*a-11*d,5*b-c,5*c+11*b,5*d+a)
  if p not in A:A.append(p)
 assert len(A)==292
 return [('B',A,72),('V',pts[214],12)]

def center(P,S,i,j,k):
 # Coordinates X+i sqrt(3) Y, with both X,Y in Q(sqrt(33)), at scale 3*S.
 xy=[((3*a,3*b),(3*c,d)) for a,b,c,d in (P[i],P[j],P[k])]
 (ax,ay),(bx,by),(cx,cy)=xy
 dx,dy=sub(bx,ax),sub(by,ay);ex,ey=sub(cx,ax),sub(cy,ay)
 det=sub(mul(dx,ey),mul(ex,dy));assert det!=(0,0)
 nd=add(mul(dx,dx),scale(mul(dy,dy),3));ne=add(mul(ex,ex),scale(mul(ey,ey),3))
 wx=mul(sub(mul(nd,ey),mul(ne,dy)),inv(scale(det,2)))
 wy=mul(sub(mul(dx,ne),mul(ex,nd)),inv(scale(det,6)))
 X,Y=add(ax,wx),add(ay,wy)
 return (Q(X[0],3*S),Q(X[1],3*S),Q(Y[0],3*S),Q(Y[1],S))

def audit(name,P,S,expected):
 n=len(P);dist={};near=[set() for _ in P]
 for i in range(n):
  for j in range(i+1,n):
   a,b,c,d=[x-y for x,y in zip(P[i],P[j])]
   v=(a*a+33*b*b+3*c*c+11*d*d,2*(a*b+c*d));dist[i,j]=v
   if not positive((v[0]-4*S*S,v[1])):near[i].add(j)
 tested=0;accepted=0;hits=defaultdict(set);freq=Counter()
 for i in range(n):
  for j in sorted(near[i]):
   a=dist[i,j]
   for k in sorted(near[i]&near[j]):
    tested+=1;b,c=dist[i,k],dist[j,k]
    ab=mul(a,b);abc=mul(ab,c);d=sub(add(a,b),c);heron=sub(scale(ab,4),mul(d,d))
    if abc!=scale(heron,S*S):continue
    assert heron!=(0,0);accepted+=1
    p=center(P,S,i,j,k);hits[p].update((i,j,k));freq[p]+=1
 actual=[];Ps={tuple(Q(x,S) for x in p) for p in P}
 for p,ns in sorted(hits.items()):
  assert freq[p]==comb(len(ns),3)
  actual.append({'point':[str(x) for x in p],'neighbors':sorted(ns),'internal':p in Ps})
 target=[{k:r[k] for k in ('point','neighbors','internal')} for r in expected]
 assert actual==target,'center/neighbor disagreement'
 return {'vertices':n,'all_triples':comb(n,3),'triples_with_sides_at_most_two':tested,'unit_circumradius_triples':accepted,'centers_ge3':len(actual),'geometric_incidence_sha256':sha256((json.dumps(actual,separators=(',',':'))+'\n').encode()).hexdigest(),'complete_catalog_matches':True}

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--catalog-dir',type=Path,required=True)
 args=parser.parse_args();out={}
 for name,P,S in inputs():
  expected=json.loads((args.catalog_dir/f'centers_{name}.json').read_text())
  out[name]=audit(name,P,S,expected)
 print(json.dumps(out,indent=2))
