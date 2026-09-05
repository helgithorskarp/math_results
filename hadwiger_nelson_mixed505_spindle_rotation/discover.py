from pathlib import Path
import sys,json,time
from itertools import combinations
from hashlib import sha256
from pysat.solvers import Solver
import pysat
import argparse
parser=argparse.ArgumentParser(description='Optional bounded generation of positive colouring rows; not needed for proof replay.')
parser.add_argument('--out',type=Path,required=True)
args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=False)
HERE=args.out
PKG=Path(__file__).resolve().parent
import census as C
B,V,EB,EV=C.sources();I,J=C.differences(B),C.differences(V)
pairs,_=C.contact_pairs(I,J);edges=C.project(I,J,pairs);libs=C.libraries(B,V,EB,EV,new=False)
initial=list(map(len,libs));trials=[]
for label in sorted(range(len(edges)),key=lambda k:(-len(edges[k]),k)):
 m,n=divmod(label,214);ee=edges[label]
 if C.witness(m,n,ee,libs) is not None:continue
 if len(trials)>=20:raise RuntimeError('bounded twenty-query pilot exhausted; checkpoint retained')
 def right(j):return m if j==n else 292+j-(j>n)
 def var(v,c):return 4*v+c+1
 full_edges=sorted(set(tuple(sorted(e)) for e in EB+[(right(i),right(j)) for i,j in EV]+[(i,right(j)) for i,j in ee]))
 assert all(i!=j for i,j in full_edges)
 clauses=[]
 for v in range(505):
  clauses.append([var(v,c) for c in range(4)])
  clauses.extend([-var(v,a),-var(v,b)] for a,b in combinations(range(4),2))
 clauses.extend([-var(i,c),-var(j,c)] for i,j in full_edges for c in range(4))
 clauses.append([var(m,0)])
 start=time.monotonic()
 with Solver(name='cadical195',bootstrap_with=clauses) as sat:
  sat.conf_budget(200000);answer=sat.solve_limited()
  if answer is not True:
   (HERE/'candidate.json').write_text(json.dumps({'anchor':[m,n],'new_cross_edges':ee,'clauses':clauses,'answer':answer})+'\n')
   raise RuntimeError('No positive witness; candidate checkpoint retained, no UNSAT claim')
  model=set(sat.get_model());col=tuple(next(c for c in range(4) if var(v,c) in model) for v in range(505))
 assert all(col[i]!=col[j] for i,j in full_edges)
 cb=tuple(col[i]^col[0] for i in range(292));cv=tuple(col[right(j)]^col[right(0)] for j in range(214))
 for lib,c in zip(libs,(cb,cv)):
  if c not in lib:lib.append(c)
 assert C.witness(m,n,ee,libs) is not None
 trials.append({'anchor':[m,n],'new_cross_edges':ee,'strict_edges':len(full_edges),'variables':2020,'clauses':len(clauses),'cnf_array_sha256':C.digest(clauses),'answer':'SAT','seconds':time.monotonic()-start})
 (HERE/'solver_trials.json').write_text(json.dumps({'python_sat':pysat.__version__,'solver':'cadical195','conflict_budget':200000,'trials':trials},indent=2)+'\n')
 for side,lib,count in zip(('B','V'),libs,initial):
  (HERE/f'new_{side}.txt').write_text(''.join(''.join(map(str,c))+'\n' for c in lib[count:]))
 print(json.dumps(trials[-1]),flush=True)
print('completed',len(trials),'positive queries; libraries',list(map(len,libs)),flush=True)
