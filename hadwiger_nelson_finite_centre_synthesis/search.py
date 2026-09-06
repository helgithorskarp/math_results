"""Optional original bounded discovery procedure; raw history stays in out/."""
from geometry import *
from pysat.solvers import Glucose3
from collections import Counter
import sys
w=Path(__file__).resolve().parent/'out';w.mkdir(exist_ok=True);pts=seed();known=set(pts);pool={};edges=[];history=[];started=time.monotonic()
def var(i,col):return 4*i+col+1
def vclauses(i):return [[var(i,k) for k in range(4)]]+[[-var(i,k),-var(i,l)] for k,l in combinations(range(4),2)]
def eclauses(i,j):return [[-var(i,k),-var(j,k)] for k in range(4)]
sat=Glucose3()
for i in range(len(pts)):
 sat.append_formula(vclauses(i))
for i,j in combinations(range(len(pts)),2):
 if dist(pts[i],pts[j])==c(1296):edges.append((i,j));sat.append_formula(eclauses(i,j))
 for v in centres(pts[i],pts[j]):
  if v not in known:pool.setdefault(v,set()).update([i,j])
for i in range(3):sat.add_clause([var(i,0)])
def save(status,model=None):
 out={'status':status,'points':[enc(p) for p in pts],'edges':edges,'history':history,'model':model,'seconds':round(time.monotonic()-started,3),'seed_size':51,'cap':1024,'pool_size':len(pool)}
 (w/'synthesis.json').write_text(json.dumps(out,indent=2)+'\n')
for step in range(974):
 if not sat.solve():
  print('CONDITIONAL_UNSAT',len(pts),len(edges),round(time.monotonic()-started,2),flush=True);save('conditional_unsat');break
 model=sat.get_model();chosen=set(x for x in model if x>0);col=[next(k for k in range(4) if var(i,k) in chosen) for i in range(len(pts))]
 if any(col[i]==col[j] for i,j in edges) or any(col[i]!=0 for i in range(3)):raise RuntimeError('bad model')
 if len(pts)>=1024:save('cap_reached',col);print('CAP',len(pts),flush=True);break
 best=None
 for v,ns in pool.items():
  colours={col[i] for i in ns}
  if len(colours)<3:continue
  complexity=sum(x.numerator.bit_length()+x.denominator.bit_length() for xy in v for x in xy)
  score=(-len(colours),-len(ns),complexity,v)
  if best is None or score<best[0]:best=(score,v,ns)
 if best is None:
  save('no_forced_centre',col);print('NO_FORCED_CENTRE',len(pts),len(pool),flush=True);break
 _,v,ns=best;ns=sorted(ns);i=len(pts)
 direct=[j for j,p in enumerate(pts) if dist(v,p)==c(1296)]
 if direct!=ns:raise RuntimeError(('neighbour mismatch',direct,ns))
 history.append({'point':enc(v),'neighbours':ns,'prior_colouring':''.join(map(str,col)),'neighbour_colours':sorted({col[j] for j in ns})})
 pts.append(v);known.add(v);pool.pop(v);sat.append_formula(vclauses(i))
 for j in ns:edges.append((j,i));sat.append_formula(eclauses(j,i))
 for j in range(i):
  for v2 in centres(pts[j],v):
   if v2 not in known:pool.setdefault(v2,set()).update([i,j])
 if i%25==0:
  save('running');print('STEP',len(pts),'edges',len(edges),'pool',len(pool),'time',round(time.monotonic()-started,2),flush=True)
sat.delete()
