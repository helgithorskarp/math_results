"""Exact dense radical geometry for the certificate producer."""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from hashlib import sha256
import json
HERE=Path(__file__).resolve().parent;REPO=HERE.parent
RAD=(1,3,5,15,11,33,55,165)
INPUTS=(
 'hadwiger_nelson_parts509_edge_criticality/reduced_edges.json',
 'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json',
 'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json',
 'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json')
def need(ok,why):
 if not ok:raise ValueError(why)
def read(name):return json.loads((REPO/name).read_text())
def point(row):
 need(len(row)==2 and all(len(a)==8 for a in row),'coordinate dimensions')
 z=[[96*Fraction(v) for v in a] for a in row]
 need(all(c.denominator==1 for a in z for c in a),'scale96')
 return tuple(tuple(int(c) for c in a) for a in z)
def unit(p,q):
 z=[0]*8
 for a,b in zip(p,q):
  d=[(i,x-y) for i,(x,y) in enumerate(zip(a,b)) if x!=y]
  for i,x in d:
   for j,y in d:z[i^j]+=x*y*RAD[i&j]
 return z==[9216,0,0,0,0,0,0,0]
def inputs():
 plan=json.loads((HERE/'inputs.json').read_text())
 for name,digest in plan.items():need(sha256((REPO/name).read_bytes()).hexdigest()==digest,('input hash',name))
 raw=read(INPUTS[0]);se=[tuple(e) for e in raw['edges']]
 need(len(se)==2259 and se==sorted(set(se)) and all(0<=u<v<509 for u,v in se),'source edges')
 sdata=read(INPUTS[1]);sp=[point(sdata['coordinates'][str(v)]) for v in range(509)]
 hdata=read(INPUTS[2]);labels=[v for v in sorted(map(int,hdata['coordinates'])) if '510' in hdata['provenance'][v]]
 fresh=read(INPUTS[3]);need([r['centre_index'] for r in fresh]==sorted({r['centre_index'] for r in fresh}),'fresh labels')
 hp=[point(hdata['coordinates'][str(v)]) for v in labels]+[point(r['coordinates']) for r in fresh]
 need(len(sp)==len(set(sp))==509 and len(hp)==len(set(hp))==632,'distinct points')
 need(all(unit(sp[u],sp[v]) for u,v in se),'source unit edges')
 he=[(u,v) for u,v in combinations(range(632),2) if unit(hp[u],hp[v])]
 need(len(he)==3112,'complete host edge count')
 return se,he
