"""Produce a degree-exact two-outside graph for the already selected types."""
import argparse
import itertools as it
import json
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from discover import core, interface

p=argparse.ArgumentParser();p.add_argument('--selection',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args()
if a.output.exists():raise ValueError('fresh output')
types=json.loads(a.selection.read_text())['types']
g=core(5388912);full,has,force,bad,loops=interface(g,types)
fixed={};free=[]
for i,j in it.combinations(range(32),2):
    nr=has[True,3][types[i]&types[j]];nb=has[False,3][full^(types[i]|types[j])]
    if nr and nb:raise ValueError('incompatible pair')
    if nr or nb:fixed[i,j]=int(nb)
    else:free.append((i,j))
D=np.array([[int(i in e) for e in free] for i in range(32)])
b=np.array([21-t.bit_count()-sum(v for e,v in fixed.items() if i in e) for i,t in enumerate(types)])
r=milp(np.zeros(len(free)),integrality=np.ones(len(free)),bounds=Bounds(0,1),
       constraints=LinearConstraint(D,b,b),options={'time_limit':30})
if r.x is None:raise ValueError(r.message)
val=np.rint(r.x).astype(int)
if not(np.all((val==0)|(val==1)) and np.all(D@val==b)):raise ValueError('primal')
R={(u,v) for u,v in it.combinations(range(11),2) if g[u]>>v&1}
R|={(v,11+i) for i,t in enumerate(types) for v in range(11) if t>>v&1}
R|={(11+i,11+j) for (i,j),c in fixed.items() if c}
R|={(11+i,11+j) for (i,j),c in zip(free,val) if c}
a.output.write_text(json.dumps({'n':43,'red_edges':sorted(R)},indent=2,sort_keys=True)+'\n')
print(r.message, 'red_edges',len(R))
