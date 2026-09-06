import json,time
from pathlib import Path
from itertools import combinations
from pysat.solvers import Cadical195
from lattice import edges
w=Path(__file__).resolve().parent/'out';w.mkdir(exist_ok=True);x=json.loads((w/'equality_frozen.json').read_text());pts=x['points'];den=x['denominator'];n=len(pts);es=edges(pts,den);ids=x['retained'];ix={v:i for i,v in enumerate(ids)}
known={};old={}
for h in x['history']:
 if h['result'] is True and h['vertex'] in ix:
  v=ix[h['vertex']];word=''.join(h['colouring'][i] for i in ids);old[v]=word
  if word[:2]=='01' and all(word[a]!=word[b] for a,b in es if v not in (a,b)):known[v]=word
print('REUSED',len(known),'of',n-2,'need',253,flush=True)
s=Cadical195()
def var(v,c):return 4*v+c+1
def sel(v):return 4*n+v+1
for v in range(n):
 s.add_clause([var(v,c) for c in range(4)])
 for c,d in combinations(range(4),2):s.add_clause([-var(v,c),-var(v,d)])
for a,b in es:
 for c in range(4):s.add_clause([-sel(a),-sel(b),-var(a,c),-var(b,c)])
s.add_clause([1]);s.add_clause([6]);hist=[];t=time.monotonic()
deg=[0]*n
for a,b in es:deg[a]+=1;deg[b]+=1
def score(v):
 if v in old:return sum(old[v][a]==old[v][b] for a,b in es if v not in (a,b)),deg[v],v
 return n,deg[v],v
order=sorted(set(range(2,n))-set(known),key=score)
initial=len(known)
def save(status):
 out={'status':status,'vertices':n,'unit_edges':len(es),'needed_nonterminal_mandatory_vertices':253,'initial_reused':initial,'colourings':[{'deleted':v,'colouring':known[v]} for v in sorted(known)],'history':hist,'seconds':time.monotonic()-t}
 p=w/'gate_colourings.json';q=p.with_suffix('.tmp');q.write_text(json.dumps(out,separators=(',',':'))+'\n');q.replace(p)
for v in order:
 if len(known)>=253:break
 if v in old:s.set_phases([var(i,int(c)) for i,c in enumerate(old[v])])
 s.conf_budget(100000);r=s.solve_limited(assumptions=[sel(i) if i!=v else -sel(i) for i in range(n)])
 if r:
  pos=set(s.get_model());word=''.join(str(next(c for c in range(4) if var(i,c) in pos)) for i in range(n))
  if word[:2]!='01' or any(word[a]==word[b] for a,b in es if v not in (a,b)):raise ValueError('Bad certificate')
  known[v]=word
 hist.append({'vertex':v,'result':r})
 save('running');print('DECISION',len(hist),'mandatory',len(known),'status',r,'seconds',round(time.monotonic()-t,2),flush=True)
save('target_closed' if len(known)>=253 else 'gate_not_met');print('COMPLETE',len(known),time.monotonic()-t,flush=True)
