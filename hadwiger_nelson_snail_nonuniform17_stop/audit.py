"""Compare exact entries in different bases; diagnose this one frozen support."""
import hashlib,json
from itertools import combinations
import geometry as P
import verify as V
s,gs,fs,pts,addr,edges,false=P.reconstruct()
data,other,addr2,edges2=V.reconstruct()
V.need(pts==[V.to_a(x) for x in other],'entrywise coordinates')
V.need(addr==addr2 and edges==edges2,'entrywise collisions and complete edges')
source_edges,_=P.F.graph(s)
inherited=set()
for row in addr:
 inherited.update(tuple(sorted((row[i],row[j]))) for i,j in source_edges)
extra=sorted(set(edges)-inherited)
# Standard low-link articulation/bridge calculation, used only for diagnostics.
n=len(pts);adj=[[] for _ in pts]
for i,j in edges:adj[i].append(j);adj[j].append(i)
seen=[-1]*n;low=[0]*n;clock=0;arts=set();bridges=[];components=[]
def dfs(v,parent,comp):
 global clock
 seen[v]=low[v]=clock;clock+=1;comp.append(v);children=0
 for w in adj[v]:
  if w==parent:continue
  if seen[w]<0:
   children+=1;dfs(w,v,comp);low[v]=min(low[v],low[w])
   if parent>=0 and low[w]>=seen[v]:arts.add(v)
   if low[w]>seen[v]:bridges.append(sorted([v,w]))
  else:low[v]=min(low[v],seen[w])
 if parent<0 and children>1:arts.add(v)
for v in range(n):
 if seen[v]<0:
  comp=[];dfs(v,-1,comp);components.append(comp)
transitions=[];selected=set(fs)
for f in fs:
 transitions.append(sum(P.F.compose(f,g) in selected for g in gs+[P.inverse(g) for g in gs]))
out={'entrywise_coordinates_equal':True,'entrywise_address_ids_equal':True,'entrywise_edges_equal':True,'source_edges':len(source_edges),'inherited_distinct_edges':len(inherited),'additional_complete_edges':len(extra),'component_sizes':sorted(map(len,components),reverse=True),'articulation_vertices':sorted(arts),'bridges':sorted(bridges),'minimum_degree':min(map(len,adj)),'maximum_degree':max(map(len,adj)),'selected_eight_motion_internal_outdegrees':transitions,'distinct_motion_outdegrees':sorted(set(transitions)),'extra_edges':extra,'pairwise_copy_overlap_sizes':[[i,j,len(set(addr[i])&set(addr[j]))] for i,j in combinations(range(17),2) if set(addr[i])&set(addr[j])]}
print(json.dumps(out,indent=2,sort_keys=True))
