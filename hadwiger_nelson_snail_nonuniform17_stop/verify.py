#!/usr/bin/env python3
"""Independent w-basis reconstruction and all-pairs positive-word verification."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
import argparse, hashlib, importlib.util, json
HERE=Path(__file__).resolve().parent

def need(ok,msg):
 if not ok:raise ValueError(msg)
def pinned(rel):
 p=HERE.parent/rel;expected=json.loads((HERE/'SOURCE_PINS.json').read_text())[rel]
 need(hashlib.sha256(p.read_bytes()).hexdigest()==expected,'source pin '+rel)
 return p
source=pinned('hadwiger_nelson_snail_mixed_boxes/field_base.py')
pinned('hadwiger_nelson_snail_mixed_boxes/seed.json')
spec=importlib.util.spec_from_file_location('wfield',source);W=importlib.util.module_from_spec(spec);spec.loader.exec_module(W)
N=16;ZERO=tuple(map(Q,W.ZERO));ONE=tuple(map(Q,W.ONE))
def inv(x):
 cols=[W.mul(x,W.basis(i)) for i in range(N)]
 m=[[Q(cols[j][i]) for j in range(N)]+[Q(i==0)] for i in range(N)]
 for j in range(N):
  p=next((i for i in range(j,N) if m[i][j]),None);need(p is not None,'invertible field element')
  m[j],m[p]=m[p],m[j];q=m[j][j];m[j]=[x/q for x in m[j]]
  for i in range(N):
   if i!=j:
    q=m[i][j]
    if q:m[i]=[a-q*b for a,b in zip(m[i],m[j])]
 out=tuple(row[-1] for row in m);need(W.mul(x,out)==ONE,'inverse check');return out

def apply(f,x):
 t,u,k=f;return W.add(t,W.mul(u,W.conjugate(x) if k else x))
def compose(f,g):
 t,u,k=f;s,v,l=g
 return W.add(t,W.mul(u,W.conjugate(s) if k else s)),W.mul(u,W.conjugate(v) if k else v),k^l

def inverse(f):
 t,u,k=f;v=u if k else W.conjugate(u)
 return W.scale(W.mul(v,W.conjugate(t) if k else t),-1),v,k

def anchor_motion(seed,row):
 i,j,k,l,flip=row;x=W.sub(seed[j],seed[i]);y=W.sub(seed[l],seed[k])
 need(W.norm(x)==W.norm(y) and x!=ZERO,'pair congruence')
 u=W.mul(y,inv(W.conjugate(x) if flip else x));t=W.sub(seed[k],W.mul(u,W.conjugate(seed[i]) if flip else seed[i]));f=t,u,flip
 need(W.norm(u)==ONE and apply(f,seed[i])==seed[k] and apply(f,seed[j])==seed[l],'physical pair motion')
 need(compose(f,inverse(f))==(ZERO,ONE,0),'inverse identity');return f

def to_a(x):
 # w=(1+A)/2; the other generators B,C,E are unchanged.
 out=[Q(0)]*N
 for i,v in enumerate(x):
  if i&1:out[i]+=v/2;out[i^1]+=v/2
  else:out[i]+=v
 return tuple(out)

def evaluate(x):
 z=0
 for a,r in zip(x,W.RESIDUES):
  a=Q(a);need(a.denominator%W.PRIME!=0,'residue denominator')
  z=(z+a.numerator*pow(a.denominator,-1,W.PRIME)*r)%W.PRIME
 return z

def reconstruct():
 c=json.loads((HERE/'CONTRACT.json').read_text());rows=json.loads((HERE/'seed.json').read_text())['moser_rows']
 need(rows==json.loads((source.parent/'seed.json').read_text())['moser_rows'],'same published source rows')
 seed=[W.scale(x,Q(1,384)) for x in W.seed()];need(len(seed)==len(set(seed))==29,'source order')
 gs=[anchor_motion(seed,r) for r in c['generator_anchors']];fs=[]
 for word in c['words']:
  f=ZERO,ONE,0
  for j in word:
   need(type(j) is int and 1<=abs(j)<=4,'word generator')
   f=compose(f,gs[j-1] if j>0 else inverse(gs[-j-1]))
  fs.append(f)
 need(len(fs)==len(set(fs))==17,'17 distinct isometries')
 formal=[[apply(f,x) for x in seed] for f in fs]
 points=sorted(set(x for group in formal for x in group),key=to_a);need(len(points)<=508,'cap')
 ids={x:i for i,x in enumerate(points)};addresses=[[ids[x] for x in group] for group in formal]
 vals=[evaluate(x) for x in points];bars=[evaluate(W.conjugate(x)) for x in points];edges=[];false=0
 for i,j in combinations(range(len(points)),2):
  if (vals[i]-vals[j])*(bars[i]-bars[j])%W.PRIME==1:
   if W.norm(W.sub(points[i],points[j]))==ONE:edges.append((i,j))
   else:false+=1
 coords='\n'.join(','.join(map(str,to_a(x))) for x in points)+'\n'
 edgebytes=''.join(f'{i} {j}\n' for i,j in edges)
 return {'physical_vertices':len(points),'strict_edges':len(edges),'coordinate_sha256':hashlib.sha256(coords.encode()).hexdigest(),'edge_sha256':hashlib.sha256(edgebytes.encode()).hexdigest(),'copies':len(fs),'formal_addresses':493,'all_pairs':len(points)*(len(points)-1)//2,'modular_false_edges':false},points,addresses,edges

def check_words(cert,data,edges):
 need(type(cert) is dict and set(cert)=={'four_word','five_word','coordinate_sha256','edge_sha256','physical_vertices','strict_edges'},'certificate schema')
 for key in ('physical_vertices','strict_edges','coordinate_sha256','edge_sha256'):need(cert[key]==data[key],'certificate '+key)
 for k,name in [(4,'four_word'),(5,'five_word')]:
  word=cert[name];need(type(word) is str and len(word)==data['physical_vertices'],'word length')
  need(set(word)==set(map(str,range(k))),'word colours')
  need(all(word[i]!=word[j] for i,j in edges),'proper complete-graph '+name)

def main():
 p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'certificate.json');p.add_argument('--check-expected',action='store_true');a=p.parse_args()
 data,points,addresses,edges=reconstruct();check_words(json.loads(a.certificate.read_text()),data,edges)
 data.update(verified=True,ordinary_four_colourable=True,proper_five_word=True,record_certified=False,independent_modulus=W.PRIME)
 if a.check_expected:need(data==json.loads((HERE/'EXPECTED.json').read_text()),'expected result')
 print(json.dumps(data,indent=2,sort_keys=True))
if __name__=='__main__':main()
