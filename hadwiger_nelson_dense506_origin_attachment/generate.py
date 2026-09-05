from pathlib import Path
from itertools import combinations,permutations
from collections import defaultdict
from hashlib import sha256
import json,time
import pysat
from pysat.solvers import Solver
import argparse
import verify as M
parser=argparse.ArgumentParser(description="Regenerate the four positive colouring repairs.")
parser.add_argument('--work',type=Path,required=True)
args=parser.parse_args();W=args.work;W.mkdir(parents=True,exist_ok=False)
def sources():return M.construction()
def libraries():
 B,V,D,inc,EB,EV=sources();lb,lv=M.libraries(B,V,EB,EV)
 return lb[:1],lv[:10]
perms=[(0,)+p for p in permutations((1,2,3))]
def witness(ee,q,lb,lv):
 return next(((i,j,k) for i,cb in enumerate(lb) for j,cv in enumerate(lv) for k,p in enumerate(perms) if all(cb[b]!=p[cv[v]^cv[q]] for b,v in ee)),None)
def digest(x):return sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
B,V,D,inc,EB,EV=sources();lb,lv=libraries();start=time.monotonic()
counts,groups,ch=M.F.enumerate_groups(B,D)
# Test a compact mask per component-signature to avoid millions of nested loops.
from functools import cache
choices=[(i,j,k) for i in range(len(lb)) for j in range(len(lv)) for k in range(6)];full=(1<<len(choices))-1
@cache
def mask(b,q,v):return sum(1<<r for r,(i,j,k) in enumerate(choices) if b[i]!=perms[k][v[j]^q[j]])
sb=list(zip(*lb));sv=list(zip(*lv));residual=[]
for gi,ee in enumerate(sorted(groups.values())):
 proj=defaultdict(list)
 for b,d in ee:
  for q,v in inc[d]:proj[q].append((b,v))
 for q,qe in sorted(proj.items()):
  ok=full
  for b,v in qe:ok&=mask(sb[b],sv[q],sv[v])
  if not ok:residual.append((gi,q,qe))
print('initial misses',len(residual),flush=True);assert len(residual)==1309
(W/'initial_residuals.json').write_text(json.dumps(residual,separators=(',',':'))+'\n')
initial=(len(lb),len(lv));records=[]
for step in range(20):
 if not residual:break
 gi,q,qe=min(residual,key=lambda r:(-len(r[2]),r[1],r[0]))
 def lab(v):return 0 if v==q else 293+v-(v>q)
 edges=sorted(set(EB+[(min(lab(i),lab(j)),max(lab(i),lab(j))) for i,j in EV]+[(min(b,lab(v)),max(b,lab(v))) for b,v in qe]))
 assert len(edges)==1389+977+len(qe) and all(i<j for i,j in edges)
 var=lambda v,c:4*v+c+1
 clauses=[]
 for v in range(506):
  clauses.append([var(v,c) for c in range(4)])
  clauses.extend([-var(v,a),-var(v,b)] for a,b in combinations(range(4),2))
 clauses.extend([-var(i,c),-var(j,c)] for i,j in edges for c in range(4));clauses.append([var(0,0)])
 t=time.monotonic()
 with Solver(name='cadical195',bootstrap_with=clauses) as sat:
  sat.conf_budget(1000000);answer=sat.solve_limited()
  record={'step':step,'ambient_class':gi,'anchor':q,'cross_edges':qe,'vertices':506,'edges':len(edges),'variables':2024,'clauses':len(clauses),'cnf_array_sha256':digest(clauses),'solver':'cadical195','python_sat':pysat.__version__,'conflict_budget':1000000,'answer':answer,'seconds':time.monotonic()-t}
  if answer is not True:
   records.append(record);break
  model=set(sat.get_model());c=[next(k for k in range(4) if var(v,k) in model) for v in range(506)]
  assert c[0]==0 and all(c[i]!=c[j] for i,j in edges)
  cb=tuple(c[:293]);cv=tuple(c[lab(v)]^c[lab(0)] for v in range(214))
  lb.append(cb);lv.append(cv);assert witness(qe,q,lb,lv)
  residual=[r for r in residual if witness(r[2],r[1],lb,lv) is None]
  record['remaining']=len(residual);record['colouring_sha256']=digest(c);records.append(record)
  for side,rows in [('B',lb[initial[0]:]),('V',lv[initial[1]:])]:
   (W/f'new_{side}.txt').write_text(''.join(''.join(map(str,row))+'\n' for row in rows))
  (W/'solver_provenance.json').write_text(json.dumps(records,indent=2)+'\n')
  print('step',step,'cross',len(qe),'remaining',len(residual),'SAT seconds',record['seconds'],flush=True)
(W/'solver_provenance.json').write_text(json.dumps(records,indent=2)+'\n')
(W/'remaining.json').write_text(json.dumps(residual)+'\n')
print('done seconds',time.monotonic()-start,'remaining',len(residual),flush=True)

if residual:raise RuntimeError('bounded generator did not close the family')
for side,n in [('B',1),('V',10)]:
 expected=(Path(__file__).resolve().parent/f'colors_{side}.txt').read_text().splitlines()[n:]
 if (W/f'new_{side}.txt').read_text().splitlines()!=expected:raise ValueError('regenerated positive rows differ')
