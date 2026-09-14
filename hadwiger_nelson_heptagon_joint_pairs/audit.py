"""Alternative-basis geometry and direct labelled coverage.

Tensor arithmetic adapted from the parent audit.py; no producer imports.
Authored cross-check, not independent-author review.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json,time
Z=(0,)*12;O=(1,)+Z[1:]
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,k):return tuple(k*x for x in a)
def monomial(i,j):
 # omega²=omega-1, zeta7^6=-(1+...+zeta7^5)
 terms={}
 for jj,v in ([(0,1)] if j==0 else [(1,1)] if j==1 else [(1,1),(0,-1)]):
  ii=i%7
  for k,c in ([(ii,v)] if ii<6 else [(k,-v) for k in range(6)]):terms[k+6*jj]=c
 return terms
TABLE=[[monomial(i%6+j%6,i//6+j//6) for j in range(12)] for i in range(12)]
def mul(a,b):
 out=[0]*12
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:
     for k,c in TABLE[i][j].items():out[k]+=c*x*y
 return tuple(out)
def zp(i):
 i%=7
 return tuple(int(k==i) for k in range(12)) if i<6 else (-1,)*6+(0,)*6
W=(0,)*6+(1,)+(0,)*5
T=mul(zp(6),W);TP=[O]
for _ in range(41):TP.append(mul(TP[-1],T))
def conjugate(a):
 out=Z
 for j,v in enumerate(a):
  b=zp(-j) if j<6 else mul(zp(-(j-6)),sub(O,W))
  out=add(out,scale(b,v))
 return out
def norm(a):return mul(a,conjugate(a))
def inv_sine_numerator(k):
 out=Z
 for j in range(7):out=add(out,scale(zp(k+2*k*j),j))
 if mul(sub(zp(k),zp(-k)),out)!=scale(O,7):raise ValueError("sine inverse")
 return out
p=inv_sine_numerator(4);q=scale(mul(sub(O,W),inv_sine_numerator(1)),-1);r=scale(mul(W,inv_sine_numerator(2)),-1)
h=[mul(a,zp(j)) for a in [p,q,r] for j in range(7)];D=sorted({sub(a,b) for a in h for b in h})

import argparse
from hashlib import sha256
HERE=Path(__file__).resolve().parent
def check(ok,message):
 if not ok:raise ValueError(message)
def audit(work,certificate):
 raw=(work/'graph.json').read_bytes();g=json.loads(raw);cert=json.loads(certificate.read_text())
 check(sha256(raw).hexdigest()==cert['graph_sha256'],'graph identity')
 def decode(row):
  out=Z
  for i,v in enumerate(row):out=add(out,scale(TP[i],v))
  return out
 check(g['denominator']==7,'denominator')
 check([decode(a) for a in g['host']]==h,'independent motif')
 points=list(map(decode,g['points']));check(len(points)==len(set(points))==421 and sorted(points)==D,'independent support')
 edges=[];sqrt3=[]
 for i,j in combinations(range(421),2):
  n=norm(sub(points[i],points[j]))
  if n==scale(O,49):edges.append((i,j))
  if n==scale(O,147):sqrt3.append((i,j))
 check(edges==list(map(tuple,g['edges'])) and len(edges)==1848,'independent full unit graph')
 check(sqrt3==list(map(tuple,g['sqrt3_pairs'])) and len(sqrt3)==126,'independent sqrt3 pairs')
 pairs=list(map(tuple,cert['pairs']));check(len(pairs)==len(set(pairs))==84 and set(pairs)<=set(sqrt3),'designated domain')
 want=set(combinations(range(84),2));covered=set();models=[];where={p:i for i,p in enumerate(points)}
 check(len(cert['words'])==5,'five words')
 for text in cert['words']:
  check(len(text)==421 and set(text)<=set('0123'),'word format');base=list(map(int,text))
  for k in range(14):
   image=[where[mul(TP[3*k],p)] for p in points]
   check(len(set(image))==421,'isometry bijection');c=[-1]*421
   for v,j in enumerate(image):c[j]=base[v]
   check(all(c[a]!=c[b] for a,b in edges),'direct edge check')
   models.append(c)
   # Direct labelled checks: no orbit quotient or coverage routine imported.
   for i,j in want:
    a,b=pairs[i];u,v=pairs[j]
    if c[a]==c[b] and c[u]==c[v]:covered.add((i,j))
 check(covered==want,'direct complete labelled coverage')
 # Distinguish pair-set requests from their equality-partition semantics.
 semantic=set()
 for i,j in want:
  a,b=set(pairs[i]),set(pairs[j])
  blocks=[tuple(sorted(a|b))] if a&b else [tuple(sorted(a)),tuple(sorted(b))]
  semantic.add(tuple(sorted(blocks)))
 return {'status':'DIRECT LABELLED COVERAGE VERIFIED','physical_pair_checks':88410,'words_with_rotations':len(models),'distinct_transported_words':len({tuple(c) for c in models}),'direct_unit_edge_checks':len(models)*len(edges),'direct_two_pair_checks':len(models)*len(want),'covered_labelled_prescriptions':len(covered),'distinct_labelled_equality_partitions':len(semantic),'certificate_sha256':sha256(certificate.read_bytes()).hexdigest()}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--graph-work',type=Path,required=True);parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json');args=parser.parse_args();started=time.perf_counter();result=audit(args.graph_work,args.certificate);result['seconds']=time.perf_counter()-started;print(json.dumps(result,indent=2))
