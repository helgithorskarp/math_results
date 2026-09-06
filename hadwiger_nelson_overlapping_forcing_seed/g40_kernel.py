import sys,json,time
from pathlib import Path
from itertools import combinations
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'hadwiger_nelson_small_triangle_forcer375'))
import geometry as g
from colour_check import solve
from pysat.solvers import Glucose3
w=Path(__file__).resolve().parent/'out';w.mkdir(exist_ok=True)
pts=g.read('g40.json');es=g.edges(pts);pairs=g.edges(pts,4752);n=len(pts)
s=Glucose3()
def var(v,c):return 4*v+c+1
for v in range(n):
 s.add_clause([var(v,c) for c in range(4)])
 for c,d in combinations(range(4),2):s.add_clause([-var(v,c),-var(v,d)])
for a,b in es:
 for c in range(4):s.add_clause([-var(a,c),-var(b,c)])
for i,(a,b) in enumerate(pairs):
 for c in range(4):s.add_clause([-161-i,-var(a,c),-var(b,c)])
s.add_clause([var(0,0)]);s.add_clause([var(1,1)]);keep=set(range(len(pairs)));history=[]
for i in range(len(pairs)):
 active=keep-{i}
 sat=s.solve(assumptions=[161+j if j in active else -161-j for j in range(len(pairs))])
 if not sat:keep=active
 history.append({'pair':i,'sat':sat})
ks=[pairs[i] for i in sorted(keep)]
a,stat=solve(40,es+ks,pins=[(0,0),(1,1)])
if a is not None:raise ValueError('Kernel fails independent check')
x={'pairs':ks,'pair_indices':sorted(keep),'unit_edges':es,'points':pts,'search':stat,'history':history}
(w/'g40_kernel.json').write_text(json.dumps(x,separators=(',',':'))+'\n')
print('KERNEL',len(ks),stat,flush=True)
