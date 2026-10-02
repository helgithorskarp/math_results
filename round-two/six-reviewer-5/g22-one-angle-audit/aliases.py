"""Literal 8^6 cube and Held--Karp rotation completion, independently written.
Boundary lists and the visible claim are mathematical inputs, not a blind test.
"""
from itertools import combinations
from functools import lru_cache
from collections import Counter
import hashlib,json
LEFT=(1,2,4,8,10,12,13);RIGHT=(0,5,6,7,9,11)
FACES=((2,10,1),(2,1,4),(2,4,8),(2,8,13),(1,10,12),(0,5,11),(0,11,6),(5,0,7),(11,5,9),(12,10,9,5,7))
KNOWN={frozenset((f[i-1],f[i])) for f in FACES for i in range(len(f))}
INTERNAL={frozenset(x) for side in (LEFT,RIGHT) for x in combinations(side,2) if frozenset(x) in KNOWN}

def rotation_count(neighbors,arcs):
 """Count directed Hamiltonian cycles extending all selected corners by mask DP.
 A singleton rotation on one neighbor is allowed only for calibration.
 """
 if len(set(a for a,b in arcs))!=len(arcs) or len(set(b for a,b in arcs))!=len(arcs):return 0
 N=tuple(sorted(neighbors));n=len(N);idx={v:i for i,v in enumerate(N)}
 allowed=[[i!=j for j in range(n)] for i in range(n)]
 for a,b in arcs:
  if a not in idx or b not in idx:return 0
  i,j=idx[a],idx[b]
  for t in range(n):
   if t!=j:allowed[i][t]=False
   if t!=i:allowed[t][j]=False
 if n==1:return int(not arcs or arcs==[(N[0],N[0])])
 if n==0:return 0
 table={(1,0):1}
 for mask in range(1,1<<n,2):
  for end in range(n):
   amount=table.get((mask,end),0)
   if not amount:continue
   for nxt in range(1,n):
    if not (mask>>nxt&1) and allowed[end][nxt]:
     key=(mask|(1<<nxt),nxt);table[key]=table.get(key,0)+amount
 return sum(table.get(((1<<n)-1,end),0) for end in range(n) if allowed[end][0])

def test(mapping,convex="all"):
 faces=[tuple(mapping.get(v,v) for v in f) for f in FACES]
 if any(len(set(f))!=len(f) for f in faces):return 'nonsimple'
 if len({frozenset(f) for f in faces[:-1]})!=9:return 'repeated_triangle'
 edges={frozenset((f[i-1],f[i])) for f in faces for i in range(len(f))}
 vertices={v for f in faces for v in f};adj={v:set() for v in vertices};corners={v:[] for v in vertices}
 for a,b in edges:adj[a].add(b);adj[b].add(a)
 if any(len(t)>5 for t in adj.values()):return 'degree'
 for f in faces:
  for i,v in enumerate(f):corners[v].append((f[i-1],f[(i+1)%len(f)],len(f)))
 if any(sum(t==3 for a,b,t in cs)>=5 for cs in corners.values()):return 'five_triangles'
 for v,cs in corners.items():
  if not rotation_count(adj[v],[(a,b) for a,b,t in cs]):return 'rotation'
  if len(cs)==len(adj[v]):
   if all(t==3 for a,b,t in cs):return 'triangle_seal'
   if len(adj[v])<=3 and (convex=='all' or (convex=='at7' and v==mapping.get(7,7))):return 'pentagon_seal'
 # Map physical patch-pair back to every distinct original within-patch pair.
 for side in (LEFT,RIGHT):
  for a,b in combinations(side,2):
   if frozenset((mapping.get(a,a),mapping.get(b,b))) in edges and frozenset((a,b)) not in INTERNAL:return 'internal_noncontact'
 return 'accepted'

def cube():
 for code in range(8**6):
  x=code;digits=[]
  for _ in RIGHT:digits.append(x%8);x//=8
  used=[d for d in digits if d]
  if len(set(used))!=len(used):continue
  yield code,{a:LEFT[d-1] for a,d in zip(RIGHT,digits) if d}

def run():
 counts=Counter();accepted=[];without_convex=[];only_seven=[];digest=hashlib.sha256();hist=Counter()
 for code,m in cube():
  verdict=test(m);counts[verdict]+=1;hist[len(m)]+=1
  digest.update(json.dumps([code,verdict],separators=(',',':')).encode()+b'\n')
  if verdict=='accepted':accepted.append(sorted(m.items()))
  if test(m,'none')=='accepted':without_convex.append(sorted(m.items()))
  if test(m,'at7')=='accepted':only_seven.append(sorted(m.items()))
 n=sum(counts.values())
 if n!=sum(__import__('math').comb(6,k)*__import__('math').factorial(7)//__import__('math').factorial(7-k) for k in range(7)):raise ValueError('cube count')
 return dict(cube=8**6,partial_injections=n,by_identified_count=dict(sorted(hist.items())),first_failures=dict(sorted(counts.items())),accepted=accepted,without_convex=without_convex,only_angle7_nonreflex=only_seven,whole_decision_sha256=digest.hexdigest())
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
