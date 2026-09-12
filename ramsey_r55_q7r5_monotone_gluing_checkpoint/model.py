"""Complete q7,r5 family and within-original root-star criticality normalization."""

if not __debug__:
    raise RuntimeError('Run this research program without -O or -OO; its exact checks require assertions.')
from pathlib import Path
from itertools import combinations
from collections import Counter
import json,hashlib,time,argparse
Q,R,N=7,5,43
EDGES=tuple(combinations(range(N),2))
FIXED={e:int(b<R) for b in range(Q) for e in combinations(range(4*b,4*b+4),2)}
V={e:i+2 for i,e in enumerate(e for e in EDGES if e not in FIXED)}
CORE_FIRST,CORE_LAST=758,862
assert min(V[e] for e in EDGES if e[0]>=28)==CORE_FIRST and max(V.values())==CORE_LAST
COMPARISONS=((1,2),(2,3),(3,4),(5,6))
BASE_VARS=922
CAT_SHA='53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1'
def inputs(repo,cache):
 p=Path(repo)/'ramsey_r55_q7r5_tail_decisions';idx=json.loads((p/'TASKS.json').read_text())['retained_core_indices'];raw=(Path(cache)/'r44_15.g6').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=CAT_SHA or len(idx)!=122 or len(set(idx))!=122:raise ValueError('pinned input/family')
 lines=raw.splitlines();cores={}
 for k in idx:
  line=lines[k];bits=[(c-63)>>b&1 for c in line[1:] for b in range(5,-1,-1)]
  if line[0]-63!=15 or any(bits[105:]):raise ValueError('graph6')
  g={(28+i,28+j):bits[j*(j-1)//2+i] for j in range(1,15) for i in range(j)}
  for S in combinations(range(28,43),4):
   if len({g[e] for e in combinations(S,2)})!=2:raise ValueError('core monochromatic four')
  cores[k]=g
 return idx,cores

def lex(left,right,first):
 p=1
 for i,(x,y) in enumerate(zip(left,right)):
  yield (-p,x,-y)
  if i<15:
   z=first+i;yield (-z,p);yield(-z,-x,y);yield(-z,x,-y);yield(z,-p,x,y);yield(z,-p,-x,-y);p=z

def base():
 yield 'constant',(1,)
 for b in range(1,Q):
  for col in range(3):
   for lo in range(16):
    for hi in range(lo+1,16):
     yield 'root',tuple((-1 if val>>row&1 else 1)*V[row,4*b+c] for c,val in ((col,lo),(col+1,hi)) for row in range(4))
 for S in combinations(range(N),5):
  pairs=tuple(combinations(S,2));colors={FIXED[e] for e in pairs if e in FIXED};free=tuple(V[e] for e in pairs if e not in FIXED)
  for c in (1,0):
   if not colors or colors=={c}:yield 'red5' if c else 'blue5',tuple(-v if c else v for v in free)
 for S in combinations(range(20,N),4):
  pairs=tuple(combinations(S,2))
  if not any(e in FIXED for e in pairs):yield 'red4',tuple(-V[e] for e in pairs)
 first=863
 for a,b in COMPARISONS:
  aa=[V[u,4*a+v] for u in reversed(range(4)) for v in reversed(range(4))];bb=[V[u,4*b+v] for u in reversed(range(4)) for v in reversed(range(4))]
  for clause in lex(aa,bb,first):yield 'order',clause
  first+=15
 assert first-1==BASE_VARS

def witnesses():
 # Every set is checked against all fixed edges, without a catalogue-dependent pruning rule.
 for c in range(28,43):
  e=(0,c)
  for S in combinations([v for v in range(N) if v not in e],3):
   K=tuple(sorted(e+S));pairs=[x for x in combinations(K,2) if x!=e]
   if any(FIXED.get(x)==1 for x in pairs):continue
   yield c,S,tuple(V[x] for x in pairs if x not in FIXED)

def clauses(idx,cores):
 yield from base()
 selectors={c:BASE_VARS+i+1 for i,c in enumerate(idx)}
 yield 'selector_or',tuple(selectors.values())
 for c in idx:
  for e in combinations(range(28,43),2):yield 'selector',(-selectors[c],V[e] if cores[c][e] else -V[e])
 first=BASE_VARS+len(idx)+1;by_core={c:[] for c in range(28,43)}
 for c,S,lits in witnesses():
  z=first;first+=1;by_core[c].append(z)
  for v in lits:yield 'witness',(-z,-v)
 for c in range(28,43):yield 'critical',tuple([-V[0,c]]+by_core[c])

def generate(repo,cache,out):
 out=Path(out);out.mkdir(exist_ok=False);idx,cores=inputs(repo,cache);start=time.monotonic();counts=Counter();nv=0;nc=0;body=out/'clauses.tmp'
 with body.open('w') as f:
  for group,cl in clauses(idx,cores):
   counts[group]+=1;nc+=1;nv=max(nv,max(map(abs,cl),default=0));f.write(' '.join(map(str,cl))+' 0\n')
 h=hashlib.sha256();dst=out/'input.cnf'
 with dst.open('wb') as f:
  raw=f'p cnf {nv} {nc}\n'.encode();f.write(raw);h.update(raw)
  with body.open('rb') as g:
   for buf in iter(lambda:g.read(2**20),b''):f.write(buf);h.update(buf)
 body.unlink()
 doc={'status':'GENERATED_WHOLE_FAMILY_NO_VERDICT','original_ids':[f'bo1-q7-r5-c{c:06d}' for c in idx],'variables':nv,'physical_variables':861,'clauses':nc,'groups':dict(counts),'input_bytes':dst.stat().st_size,'input_sha256':h.hexdigest(),'base_variables':BASE_VARS,'core_variable_range':[CORE_FIRST,CORE_LAST],'selected_edges':[[0,c] for c in range(28,43)],'generation_seconds':time.monotonic()-start,'limits':{'wall_seconds':1800,'proof_bytes':20*1024**3},'new_original_exclusions':[]}
 (out/'INPUT.json').write_text(json.dumps(doc,indent=2)+'\n');print(json.dumps(doc,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--cache',required=True);p.add_argument('--out',required=True);a=p.parse_args();generate(a.repo,a.cache,a.out)
