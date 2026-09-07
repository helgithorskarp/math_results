from pathlib import Path
from itertools import combinations
import json,sys,time
from pysat.solvers import Cadical195
W=Path(__file__).resolve().parent/'out'

def formula(n,edges):
 x=lambda v,c:4*v+c+1
 clauses=[]
 for v in range(n):
  clauses.append([x(v,c) for c in range(4)])
  clauses.extend([-x(v,a),-x(v,b)] for a,b in combinations(range(4),2))
 for a,b in edges:clauses.extend([-x(a,c),-x(b,c)] for c in range(4))
 # A largest-degree vertex and two adjacent neighbours form a triangle.
 adj=[set() for _ in range(n)]
 for a,b in edges:adj[a].add(b);adj[b].add(a)
 a=max(range(n),key=lambda i:(len(adj[i]),-i));pins=[(a,0)]
 for b in sorted(adj[a]):
  common=adj[a]&adj[b]
  if common:pins=[(a,0),(b,1),(min(common),2)];break
 clauses.extend([x(v,c)] for v,c in pins)
 return clauses,pins

def main():
 path=Path(sys.argv[1]);g=json.loads(path.read_text());n=len(g['points']);es=g['edges'];t=time.monotonic()
 cnf,pins=formula(n,es)
 with Cadical195(bootstrap_with=cnf) as s:
  budget=int(sys.argv[2]) if len(sys.argv)>2 else 3000000
  s.conf_budget(budget);res=s.solve_limited();stats=s.accum_stats()
  out={'status':{True:'SAT',False:'UNSAT_unverified',None:'UNKNOWN'}[res],
       'vertices':n,'edges':len(es),'pins':pins,'conflict_budget':budget,'statistics':stats,'seconds':time.monotonic()-t}
  if res:
   m=set(s.get_model());word=[next(c for c in range(4) if 4*i+c+1 in m) for i in range(n)]
   if any(word[a]==word[b] for a,b in es):raise RuntimeError('Bad colouring')
   out['colouring']=''.join(map(str,word))
 (path.parent/(path.stem+'_colour.json')).write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k!='colouring'},indent=2),flush=True)
if __name__=='__main__':main()
