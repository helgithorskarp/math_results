"""Exhaustive finite CSP, with a hard node budget and explicit incomplete status."""
from pathlib import Path
from itertools import combinations
import json,time
import geometry as G
import argparse
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args();w=a.work;x=json.loads((w/'graph.json').read_text());H=list(map(tuple,x['host']));D=list(map(tuple,x['points']));idx={p:i for i,p in enumerate(D)};rep={idx[G.ZERO]:()}
for a,b in combinations(range(21),2):
 rep[idx[G.sub(H[a],H[b])]]=(a,b);rep[idx[G.sub(H[b],H[a])]]=(a,b)
constraints=sorted({tuple(sorted(set(rep[a])^set(rep[b]))) for a,b in x['edges']});assert len(constraints)==84
inc=[[] for _ in range(21)]
for row in constraints:
 for a in row:inc[a].append(row)
colors=[-1]*21;colors[0]=0;colors[7]=1;colors[14]=2
assert {tuple(sorted(e)) for e in [(0,7),(0,14),(7,14)]}<=set(map(tuple,x['host_edges']))
nodes=0;solutions=[];complete=True;t=time.perf_counter();limit=2000000
class Limit(Exception):pass
def dfs():
 global nodes
 nodes+=1
 if nodes>limit:raise Limit
 best=None;allowed=None
 for a in range(21):
  if colors[a]>=0:continue
  domain={0,1,2,3}
  for row in inc[a]:
   others=[colors[b] for b in row if b!=a]
   if -1 not in others:
    c=0
    for b in others:c^=b
    domain.discard(c)
  if not domain:return
  if best is None or (len(domain),-len(inc[a]),a)<(len(allowed),-len(inc[best]),best):best,allowed=a,domain
 if best is None:
  for row in constraints:
   c=0
   for a in row:c^=colors[a]
   assert c
  solutions.append(colors.copy());return
 for c in sorted(allowed):colors[best]=c;dfs()
 colors[best]=-1
try:dfs()
except Limit:complete=False
# Test each of the126 designated pairs across every enumerated lift.
masks=[]
for a,b in x['sqrt3_pairs']:
 seen=set()
 for row in solutions:
  c=0
  for v in set(rep[a])^set(rep[b]):c^=row[v]
  seen.add(c)
 masks.append(sum(1<<v for v in seen))
(w/'normalized_lifts.json').write_text(json.dumps(solutions,separators=(',',':'))+'\n')
out={'complete':complete,'nodes':nodes,'solutions':len(solutions),'normalization':{'0':0,'7':1,'14':2},'sqrt3_xor_masks':masks,'seconds':time.perf_counter()-t}
(w/'count_lifts.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
