import json,time,sys
from pathlib import Path
from itertools import combinations
from pysat.solvers import Glucose3
w=Path(__file__).resolve().parent/'out';w.mkdir(exist_ok=True)
limit=int(sys.argv[3]) if len(sys.argv)>3 else None
name=sys.argv[1];mode=sys.argv[2];raw=json.loads((w/(name+'.json')).read_text());pts=raw['points'];es=raw['edges'];n=len(pts)
if mode not in ('equal','different','free'):raise ValueError('Unknown pin mode')
term=[0,1] if mode!='free' else []
def var(v,c):return 4*v+c+1
def sel(v):return 4*n+v+1
s=Glucose3()
for v in range(n):
 s.add_clause([var(v,c) for c in range(4)])
 for c,d in combinations(range(4),2):s.add_clause([-var(v,c),-var(v,d)])
for a,b in es:
 for c in range(4):s.add_clause([-sel(a),-sel(b),-var(a,c),-var(b,c)])
if mode=='equal':s.add_clause([var(0,0)]);s.add_clause([var(1,0)])
if mode=='different':s.add_clause([var(0,0)]);s.add_clause([var(1,1)])
if mode=='free':s.add_clause([var(0,0)])
keep=set(range(n));history=[];started=time.monotonic();deg=[0]*n
for a,b in es:deg[a]+=1;deg[b]+=1
order=sorted(set(range(n))-set(term),key=lambda v:(deg[v],v))
def query(active,budget=200000):
 s.conf_budget(budget)
 return s.solve_limited(assumptions=[sel(v) if v in active else -sel(v) for v in range(n)],expect_interrupt=True)
def model(active):
 pos=set(i for i in s.get_model() if i>0)
 cs=''.join(str(next(c for c in range(4) if var(v,c) in pos)) for v in range(n))
 if any(cs[a]==cs[b] for a,b in es if a in active and b in active):raise ValueError('Bad edge')
 if mode=='equal' and (cs[0]!=cs[1]):raise ValueError('Bad pins')
 if mode=='different' and (cs[0]==cs[1]):raise ValueError('Bad pins')
 return cs
def core(active):
 lits=set(s.get_core())
 return {v for v in active if sel(v) in lits}|set(term)
def save(status):
 ids=sorted(keep);ix={v:i for i,v in enumerate(ids)}
 data={'status':status,'mode':mode,'source':name,'retained':ids,'denominator':raw['denominator'],'points':[pts[v] for v in ids], 'edges':[[ix[a],ix[b]] for a,b in es if a in ix and b in ix], 'history':history,'seconds':time.monotonic()-started}
 destination=w/(name+'_reduced.json');temporary=destination.with_suffix('.tmp')
 temporary.write_text(json.dumps(data,separators=(',',':'))+'\n');temporary.replace(destination)
result=query(keep)
if result is not False:
 save('baseline_sat' if result else 'baseline_unknown');print('BASELINE',result,flush=True);sys.exit(2)
keep=core(keep);print('BASE_CORE',len(keep),time.monotonic()-started,flush=True);save('running')
for v in order:
 if v not in keep:continue
 active=keep-{v};res=query(active);entry={'vertex':v,'result':res}
 if res is False:
  nxt=core(active);entry['removed']=sorted(keep-nxt);keep=nxt
 elif res is True:entry['colouring']=model(active)
 history.append(entry)
 if len(history)%10==0 or res is False:
  print('STEP',len(history),'keep',len(keep),'last',res,'seconds',round(time.monotonic()-started,2),flush=True);save('running')
 if limit is not None and len(history)>=limit:
  save('frozen_for_target_gate');print('FROZEN',len(keep),len(history),flush=True);sys.exit(0)
save('complete');print('COMPLETE',len(keep),len(history),time.monotonic()-started,flush=True)
