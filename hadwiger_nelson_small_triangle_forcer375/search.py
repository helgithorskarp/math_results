"""Optional deterministic single-pass discovery; raw history remains in out/."""
from pathlib import Path
from itertools import combinations
from pysat.solvers import Glucose3
from geometry import reference,edges as make_edges
import json,time

w=Path(__file__).resolve().parent/'out';w.mkdir(exist_ok=True)
pts=reference();edges=make_edges(pts);n=len(pts)
if n!=627 or len(edges)!=2982:raise RuntimeError('Reference mismatch')
degree=[0]*n
for i,j in edges:degree[i]+=1;degree[j]+=1
order=sorted(range(3,n),key=lambda i:(degree[i],i))
(w/'deletion_order.json').write_text(json.dumps(order)+'\n')
def var(v,c):return 4*v+c+1
def selector(v):return 4*n+v+1
s=Glucose3()
for v in range(n):
 s.add_clause([var(v,c) for c in range(4)])
 for c,d in combinations(range(4),2):s.add_clause([-var(v,c),-var(v,d)])
for i,j in edges:
 for c in range(4):s.add_clause([-selector(i),-selector(j),-var(i,c),-var(j,c)])
for v in range(3):s.add_clause([var(v,0)])
keep=set(range(n));history=[];started=time.monotonic()
def query(active):return s.solve(assumptions=[selector(v) if v in active else -selector(v) for v in range(n)])
def colouring():
 pos=set(x for x in s.get_model() if x>0)
 return ''.join(str(next(c for c in range(4) if var(v,c) in pos)) for v in range(n))
def save(status):
 (w/'reduction.json').write_text(json.dumps({'status':status,'retained':sorted(keep),'history':history,'seconds':round(time.monotonic()-started,3)},separators=(',',':'))+'\n')
if query(keep):raise RuntimeError('Reference does not force triangle')
print('BASELINE_UNSAT',flush=True)
for step,v in enumerate(order):
 active=keep-{v}
 satisfiable=query(active)
 item={'vertex':v,'deleted':not satisfiable}
 if satisfiable:
  word=colouring()
  if word[0:3]!='000' or any(word[i]==word[j] for i,j in edges if i in active and j in active):raise RuntimeError('Bad deletion witness')
  item['colouring']=word
 else:keep.remove(v)
 history.append(item)
 save('running')
 if step%25==0:print('STEP',step+1,'retained',len(keep),'seconds',round(time.monotonic()-started,2),flush=True)
save('complete');s.delete()
print('COMPLETE',len(keep),sum(i in keep and j in keep for i,j in edges),round(time.monotonic()-started,2),flush=True)
