"""One frozen physical exchange; no chromatic candidate sweep."""
import json,sys,time
from pathlib import Path
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import argparse
PACKAGE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);parser.add_argument('--repo',default=str(PACKAGE.parent));args=parser.parse_args()
HERE=Path(args.output).resolve();HERE.mkdir(parents=True,exist_ok=True)
REPO=Path(args.repo).resolve()
(HERE/'ARCHITECTURE.json').write_bytes((PACKAGE/'ARCHITECTURE.json').read_bytes())
INPUTS={
 'base':'hadwiger_nelson_h516_degree4_surgeries/SOURCE.json',
 'old':'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json',
 'fresh':'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json',
 'host560':'hadwiger_nelson_heule632_minimize/certificate.json'}
EXPECTED={'base':'3f60fe94c7cd3d9c70b7cc52124fa185d4b46d54bb59b21bca0c45d2b181fd51','old':'bc8e0f5f5ec7fa5f2376cc77ba0e65f6023b340cf48990370d5eda575d30ae79','fresh':'89345930e1bea184ce2457b0e14a015bcd9a2901cfc609a6468cf050234a8317'}
def require(ok,why):
 if not ok: raise ValueError(why)
def write(name,obj):
 (HERE/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def load():
 data={};pins={}
 frozen=json.loads((PACKAGE/'PROVENANCE.json').read_text())['input_hashes']
 for k,p in INPUTS.items():
  b=(REPO/p).read_bytes();h=sha256(b).hexdigest();require(k not in EXPECTED or h==EXPECTED[k],k)
  require(h==frozen[p],'all frozen input bytes')
  data[k]=json.loads(b);pins[p]=h
 old=data['old']; lab=[v for v in sorted(map(int,old['coordinates'])) if '510' in old['provenance'][v]]
 raw=[old['coordinates'][str(v)] for v in lab]+[a['coordinates'] for a in data['fresh']]
 P=[]
 for p in raw:
  axes=[]
  for a in p:
   vals=[96*Fraction(x) for x in a];require(all(x.denominator==1 for x in vals),'denominator');axes.append([int(x) for x in vals])
  P.append(axes)
 require(len(P)==632 and len({tuple(p[0]+p[1]) for p in P})==632,'support632')
 return data,pins,P
RAD=[1,3,5,15,11,33,55,165]
def norm(p,q):
 out=[0]*8
 for a,b in zip(p,q):
  d=[(i,x-y) for i,(x,y) in enumerate(zip(a,b)) if x!=y]
  for i,x in d:
   for j,y in d: out[i^j]+=x*y*RAD[i&j]
 return out
def edges(P):
 return [[u,v] for u,v in combinations(range(len(P)),2) if norm(P[u],P[v])==[9216,0,0,0,0,0,0,0]]
def main():
 start=time.monotonic();data,pins,P=load(); E=edges(P);require(len(E)==3112,'H632 graph')
 B=data['base']; labels=B['labels'];bs=set(labels);h560=set(data['host560']['retained'])
 require(len(bs)==516 and bs<=h560 and len(h560)==560,'source sets')
 require([P[x] for x in labels]==B['coordinates'],'base coordinates')
 BE=[e for e in E if set(e)<=bs];require(BE==B['edges'] and len(BE)==2538,'base graph')
 adj=[set() for p in P]
 for u,v in E:adj[u].add(v);adj[v].add(u)
 D=[v for v in labels if len(adj[v]&bs)==4]
 architecture=json.loads((HERE/'ARCHITECTURE.json').read_text());require(D==architecture['removed_host_labels'],'fixed deletion')
 R=bs-set(D);newpair=None
 for u,v in E:
  if u not in h560 and v not in h560 and len(adj[u]&R)>=3 and len(adj[v]&R)>=3:newpair=[u,v];break
 write('input_hashes.json',pins)
 if newpair is None:
  write('result.json',{'status':'GEOMETRY_STOP_NO_QUALIFYING_EDGE','colour_queries':0});print('GEOMETRY_STOP',flush=True);return
 L=sorted(R|set(newpair));Q=[P[v] for v in L];QE=edges(Q)
 require(len(L)==508,'cap');require(len(QE)==sum(u in L and v in L for u,v in E),'complete edges')
 pointbytes=''.join(','.join(map(str,p[0]+p[1]))+'\n' for p in Q).encode()
 edgebytes=''.join(f'{u},{v}\n' for u,v in QE).encode()
 (HERE/'points.csv').write_bytes(pointbytes);(HERE/'edges.csv').write_bytes(edgebytes)
 S={'labels':L,'coordinates':Q,'edges':QE,'removed':D,'added':newpair,'new_old_contacts':{str(v):sorted(adj[v]&R) for v in newpair},'point_sha256':sha256(pointbytes).hexdigest(),'edge_sha256':sha256(edgebytes).hexdigest(),'architecture_sha256':sha256((HERE/'ARCHITECTURE.json').read_bytes()).hexdigest(),'input_hashes':pins,'complete_pair_count':508*507//2}
 write('selected_support.json',S)
 print('FROZEN',len(Q),len(QE),'pair',newpair,'contacts',S['new_old_contacts'],flush=True)
 # No solver is imported or called before all graph bytes and geometry are frozen.
 from pysat.solvers import Cadical195
 clauses=[]
 for v in range(508):
  names=[4*v+c+1 for c in range(4)];clauses.append(names);clauses.extend([[-a,-b] for a,b in combinations(names,2)])
 for u,v in QE:clauses.extend([[-(4*u+c+1),-(4*v+c+1)] for c in range(4)])
 # Fix first vertex only: colour-name symmetry is sound for every graph.
 clauses.append([1]);raw=(f'p cnf 2032 {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()
 (HERE/'four.cnf').write_bytes(raw)
 with Cadical195(bootstrap_with=clauses) as solver:
  sat=solver.solve();model=set(solver.get_model() or [])
 result={'status':'SAT_FOUR' if sat else 'UNSAT_SIGNAL_REQUIRES_CERTIFICATE','vertices':508,'unit_edges':len(QE),'added':newpair,'removed':D,'colour_queries':1,'point_sha256':S['point_sha256'],'edge_sha256':S['edge_sha256'],'cnf_sha256':sha256(raw).hexdigest(),'runtime_seconds':time.monotonic()-start,'record_certified':False}
 if sat:
  word=''.join(str(next(c for c in range(4) if 4*v+c+1 in model)) for v in range(508));require(all(word[u]!=word[v] for u,v in QE),'word');result['four_word']=word
 write('result.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':main()
