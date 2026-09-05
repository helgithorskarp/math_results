from pathlib import Path
from itertools import combinations
from hashlib import sha256
import json,sys,pickle,time
from pysat.solvers import Solver
import pysat
import argparse
parser=argparse.ArgumentParser(description='Optional bounded positive-colouring generation for the one inherited-library residual.')
parser.add_argument('--out',type=Path,required=True);args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=False)
HERE=args.out
import geometry as G
C=G.C
B,V,EB,EV=C.sources()
key=(16,-14,0,-3,0,-9,0,-2,0)
contacts=[17073,18143,19132,44679,53453,61585]
edges=EB+[(292+i,292+j) for i,j in EV]+[(e//214,292+e%214) for e in contacts]
def var(v,c):return 4*v+c+1
clauses=[]
for v in range(506):
 clauses.append([var(v,c) for c in range(4)])
 clauses.extend([-var(v,a),-var(v,b)] for a,b in combinations(range(4),2))
clauses.extend([-var(i,c),-var(j,c)] for i,j in edges for c in range(4));clauses.append([var(0,0)])
t=time.monotonic()
with Solver(name='cadical195',bootstrap_with=clauses) as sat:
 sat.conf_budget(1000000);answer=sat.solve_limited()
 result={'translation':key,'contacts':contacts,'vertices':506,'edges':len(edges),'variables':2024,'clauses':len(clauses),'cnf_array_sha256':C.digest(clauses),'solver':'cadical195','python_sat':pysat.__version__,'conflict_budget':1000000,'answer':answer,'seconds':time.monotonic()-t}
 if answer is True:
  model=set(sat.get_model());colors=[next(c for c in range(4) if var(v,c) in model) for v in range(506)]
  assert all(colors[i]!=colors[j] for i,j in edges)
  cb=colors[:292];cv=[c^colors[292] for c in colors[292:]]
  for side,row in [('B',cb),('V',cv)]:(HERE/f'new_{side}.txt').write_text(''.join(map(str,row))+'\n')
  result['colouring']=colors
 (HERE/'repair_result.json').write_text(json.dumps(result,indent=2)+'\n')
 print({k:v for k,v in result.items() if k!='colouring'},flush=True)
