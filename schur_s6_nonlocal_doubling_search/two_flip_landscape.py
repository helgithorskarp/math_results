"""Exact one- and two-entry landscape around a doubling-safe 537 word.

The cutoff on individually legal pairs is rigorous: two changed vertices
share at most two distinct-summand triples, each with correction at least -2.
Pairs touching a doubling edge are also checked directly, even if either
single recolouring would break that edge.
"""
from collections import Counter, defaultdict
from pathlib import Path
import sys

s=Path(sys.argv[1]).read_text().strip()
assert len(s)==537 and set(s)==set('123456')
c=[0]+[int(d) for d in s]
assert all(c[v]!=c[2*v] for v in range(1,269))
edges=[];inc=[[] for _ in range(538)];pair_edges=defaultdict(list)
for x in range(1,538):
 for y in range(x+1,538-x):
  z=x+y;id=len(edges);edges.append((x,y,z))
  for v in (x,y,z):inc[v].append(id)
  for v,w in ((x,y),(x,z),(y,z)):pair_edges[v,w].append(id)
bad=[c[x]==c[y]==c[z] for x,y,z in edges]
assert sum(bad)==4
def mono(id,changes=()):
 x,y,z=edges[id]
 a=next((d for v,d in changes if v==x),c[x])
 b=next((d for v,d in changes if v==y),c[y])
 e=next((d for v,d in changes if v==z),c[z])
 return a==b==e
def direct(v,d,w,e):
 t=c.copy();t[v]=d;t[w]=e
 assert all(t[j]!=t[2*j] for j in range(1,269))
 return sum(t[x]==t[y]==t[x+y] for x in range(1,538)
            for y in range(x,538-x))
moves=[];hist=Counter()
for v in range(1,538):
 for d in range(1,7):
  if d==c[v] or (v%2==0 and d==c[v//2]) or (2*v<=537 and d==c[2*v]):continue
  delta=sum(mono(id,((v,d),))-bad[id] for id in inc[v])
  moves.append((v,d,delta));hist[delta]+=1
print('edges',len(edges),'legal_single_moves',len(moves),'minimum_single',4+min(hist),
      'neutral_single',hist[0],flush=True)
best=100;count=0;examples=[];tested=0;audits=0;upper=6
for i,(v,d,dv) in enumerate(moves):
 for w,e,dw in moves[i+1:]:
  if v==w or dv+dw>upper:continue
  if (v*2==w or w*2==v) and d==e:continue
  ids=pair_edges.get((min(v,w),max(v,w)),())
  correction=sum(mono(id,((v,d),(w,e)))-mono(id,((v,d),))-mono(id,((w,e),))+bad[id] for id in ids)
  value=4+dv+dw+correction
  tested+=1
  if tested%2000==0:
   assert direct(v,d,w,e)==value
   audits+=1
  if value<best:best=value;count=1;examples=[(v,d,w,e,value)]
  elif value==best:
   count+=1
   if len(examples)<10:examples.append((v,d,w,e,value))
print('tested_pairs',tested,'direct_audits',audits,'minimum_pair',best,
      'min_count',count,'examples',examples,flush=True)
adjacent=0
for v in range(1,269):
 w=2*v
 for d in range(1,7):
  if d==c[v]:continue
  for e in range(1,7):
   if e==c[w] or d==e:continue
   if v%2==0 and c[v//2]==d:continue
   if 2*w<=537 and c[2*w]==e:continue
   dv=sum(mono(id,((v,d),))-bad[id] for id in inc[v])
   dw=sum(mono(id,((w,e),))-bad[id] for id in inc[w])
   ids=pair_edges.get((v,w),())
   correction=sum(mono(id,((v,d),(w,e)))-mono(id,((v,d),))-mono(id,((w,e),))+bad[id] for id in ids)
   value=4+dv+dw+correction
   adjacent+=1
   if adjacent%100==0:
    assert direct(v,d,w,e)==value
    audits+=1
   if value<best:best=value;count=1;examples=[(v,d,w,e,value)]
   elif value==best:
    count+=1
    if len(examples)<10:examples.append((v,d,w,e,value))
print('adjacent_pair_moves',adjacent,'overall_minimum_pair',best,
      'min_count',count,'direct_audits_total',audits,'examples',examples,flush=True)
# Two distinct vertices occur together in at most two x<y triples, and each
# edge correction has absolute value at most two. A pair with delta sum > 6
# cannot lower a four-defect state. Doubling-adjacent pairs are checked above
# even if either individual recolouring would violate doubling.
for v,d,w,e,value in examples:
 assert direct(v,d,w,e)==value
