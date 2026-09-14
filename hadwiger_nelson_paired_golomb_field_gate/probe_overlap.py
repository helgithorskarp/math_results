from prepare import *
from pysat.solvers import Cadical195
import random
st=time.time();x=json.loads((W/'inventory.json').read_text());g=json.loads((W/'geometry.json').read_text());P,old=seed();out=[]
for cl in [5,20,32,33]:
 ids=[i for i,p in enumerate(x['points'])if p[0]==cl];ix={v:i for i,v in enumerate(ids)};copies=[(i,[ix[v]for v in c['points']])for i,c in enumerate(x['copies'])if c['class']==cl];n=len(ids);cnf=[];active=lambda i:4*n+i+1;group=lambda i:5*n+i+1
 for i,v in enumerate(ids):
  allowed=set(range(4))-{int(old[r])for r in g['neighbours'][v]};cnf.append([-active(i)]+[4*i+c+1 for c in allowed])
  for a,b in combinations(range(4),2):cnf.append([-4*i-a-1,-4*i-b-1])
 for a,b in g['edges']:
  if a not in ix or b not in ix:continue
  i,j=ix[a],ix[b]
  for c in range(4):cnf.append([-active(i),-active(j),-4*i-c-1,-4*j-c-1])
 for k,(ci,vs)in enumerate(copies):
  for v in vs:cnf.append([-group(k),active(v)])
 with Cadical195(bootstrap_with=cnf)as s:
  activecopies=list(range(len(copies)));require(s.solve(assumptions=[group(k)for k in activecopies])is False,'expected conditional obstruction');core=[k for k in activecopies if group(k)in set(s.get_core())];initial=len(core);queries=1
  for k in list(core):
   if k not in core:continue
   trial=[j for j in core if j!=k];res=s.solve(assumptions=[group(j)for j in trial]);queries+=1
   if res is False:
    ks=set(s.get_core());core=[j for j in trial if group(j)in ks]
  vs=sorted({ids[v]for k in core for v in copies[k][1]});record={'class':cl,'initial_copy_core':initial,'minimal_copy_indices':[copies[k][0]for k in core],'new_points':len(vs),'point_ids':vs,'queries':queries,'conditional_unsat_only':True};out.append(record);print('CORE',record,'sec',time.time()-st,flush=True)
 (W/'core_probe.json').write_text(json.dumps({'records':out,'seconds':time.time()-st},separators=(',',':'))+'\n')
