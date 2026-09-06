"""Discover a separating basis of E477 proper four-colourings."""
from pathlib import Path
import sys,json,itertools,time,random
from pysat.solvers import Cadical195
ROOT=Path(__file__).resolve().parent
W=ROOT/'out'
W.mkdir(exist_ok=True)
P=ROOT.parent/'hadwiger_nelson_overlapping_forcing_seed'
sys.path.insert(0,str(P))
from lattice import edges

def main():
 start=time.monotonic();g=json.loads((P/'certificate.json').read_text())['equal']
 pts=g['points'];es=edges(pts,g['denominator']);n=len(pts)
 def x(i,c):return 4*i+c+1
 cnf=[]
 for i in range(n):
  cnf.append([x(i,c) for c in range(4)])
  cnf.extend([-x(i,a),-x(i,b)] for a,b in itertools.combinations(range(4),2))
 for i,j in es:cnf.extend([-x(i,c),-x(j,c)] for c in range(4))
 cnf.append([x(0,0)])
 words=[g['colouring']];history=[];nxt=4*n;disabled=[]
 rng=random.Random(0)
 def blocks():
  b={}
  for i in range(n):b.setdefault(tuple(w[i] for w in words),[]).append(i)
  return sorted(b.values())
 def save(status):
  out={'status':status,'vertices':n,'edges':len(es),'words':[''.join(map(str,w)) for w in words],
       'nontrivial_blocks':[b for b in blocks() if len(b)>1],'history':history,'seconds':time.monotonic()-start}
  (W/'partition.json').write_text(json.dumps(out,indent=2)+'\n')
 with Cadical195(bootstrap_with=cnf) as s:
  for step in range(64):
   bs=blocks();pairs=[(b[0],i) for b in bs for i in b[1:] if (b[0],i)!=(0,1)]
   if not pairs:save('complete_using_parent_equal_pair');return
   nxt+=1;act=nxt;ys=[]
   for a,b in pairs:
    for c in range(4):
     nxt+=1;y=nxt;ys.append(y)
     s.add_clause([-y,x(a,c)]);s.add_clause([-y,-x(b,c)])
   s.add_clause([-act]+ys)
   s.set_phases([x(i,rng.randrange(4)) for i in range(n)])
   s.conf_budget(5000000);t=time.monotonic()
   ans=s.solve_limited(assumptions=disabled+[act])
   event={'step':step,'candidate_anchor_pairs':len(pairs),'blocks_before':len(bs),
          'status':{True:'SAT',False:'UNSAT',None:'UNKNOWN'}[ans],'seconds':time.monotonic()-t}
   history.append(event);print(json.dumps(event),flush=True)
   if ans is not True:save('new_forced_partition_unverified' if ans is False else 'incomplete');return
   m=set(z for z in s.get_model() if z>0)
   w=[next(c for c in range(4) if x(i,c) in m) for i in range(n)]
   if any(w[i]==w[j] for i,j in es):raise RuntimeError('Bad model')
   if not any(w[a]!=w[b] for a,b in pairs):raise RuntimeError('No separation')
   words.append(w);disabled.append(-act);save('running')
  save('pilot_limit')
if __name__=='__main__':main()
