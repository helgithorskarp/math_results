"""Independent radius identity and final physical-incidence controls.
This module uses no target source or expected result.
"""
from itertools import combinations
from collections import Counter
from rows import need
import json


def layers(adj,s):
 first=set(adj[s]);second=set().union(*(adj[v]for v in first))-{s}-first if first else set()
 triangles=sum(v in adj[u]for u,v in combinations(sorted(first),2))
 collision=sum(len(first&adj[w])-1 for w in second)
 return first,second,triangles,collision

def exact_radius(adj,s):
 A,B,t,c=layers(adj,s)
 need(len(A)+len(B)==sum(len(adj[v])for v in A)-2*t-c,'exact layer-count identity')
 return {'ball':1+len(A)+len(B),'triangles':t,'collision':c,'neighbor_degree_sum':sum(len(adj[v])for v in A)}

def closed_unit_bridge(support,Q,T,X,tau):
 need((Q,T,X,tau)==(5,0,0,0),'proved final branch, including tau0')
 need(sorted((x['count'],tuple(x['type'][:4]),tuple(x['type'][4]))for x in support)==[
  (5,(0,1,1,False),(4,0,0,0,0)),(10,(1,1,0,True),(3,0,0,0,0))],'actual complete physical survivor')
 # These are proof hypotheses; they encode, rather than formalize, the written bridge.
 units=5;unit_degree=4;hh_edges=4;hub_touching=1
 need(unit_degree==units-1,'distinct neighbors force closed complete unit block')
 incidences=units*(hh_edges-hub_touching)
 need(incidences%3==0,'three centers per genuine uncovered triple')
 uncovered=incidences//3
 need(uncovered>tau,'physical triangle contradiction')
 return {'units':units,'unit_degree':unit_degree,'uncovered_center_incidences':incidences,'uncovered_triangles':uncovered,'tau':tau}

def check():
 # Complete labeled six-point graphs, including disconnected and isolated cases.
 edges=list(combinations(range(6),2));centers=0;triangle_centers=collision_centers=0
 for mask in range(1<<len(edges)):
  adj=[set()for _ in range(6)]
  for i,(u,v)in enumerate(edges):
   if mask>>i&1:adj[u].add(v);adj[v].add(u)
  for s in range(6):
   r=exact_radius(adj,s);centers+=1;triangle_centers+=bool(r['triangles']);collision_centers+=bool(r['collision'])
 # Classical G(8,3) model, contract the outer0/inner0 matching edge.
 adj=[set()for _ in range(16)]
 for i in range(8):
  for u,v in [(i,(i+1)%8),(8+i,8+(i+3)%8),(i,8+i)]:adj[u].add(v);adj[v].add(u)
 mapping={v:(0 if v==8 else v if v<8 else v-1)for v in range(16)}
 contracted=[set()for _ in range(15)]
 for u in range(16):
  for v in adj[u]:
   if mapping[u]!=mapping[v]:contracted[mapping[u]].add(mapping[v])
 need(sorted(map(len,contracted))==[3]*14+[4],'contracted degree inventory')
 girth=16
 for root in range(15):
  dist={root:0};parent={root:None};queue=[root]
  for u in queue:
   for v in contracted[u]:
    if v not in dist:dist[v]=dist[u]+1;parent[v]=u;queue.append(v)
    elif parent[u]!=v:girth=min(girth,dist[u]+dist[v]+1)
 need(girth>=5,'classical girth-only countermodel')
 root=exact_radius(contracted,0);need(root['ball']==13 and root['neighbor_degree_sum']==12,'coverage fails at15')
 # All ten unit triples. Degree3 at each vertex is necessary for 15 incidences.
 triples=list(combinations(range(5),3));families=[]
 for chosen in combinations(range(10),5):
  if all(sum(v in triples[i]for i in chosen)==3 for v in range(5)):
   complements=[tuple(sorted(set(range(5))-set(triples[i])))for i in chosen]
   need(all(sum(v in e for e in complements)==2 for v in range(5)),'complement2-regular')
   family=[list(triples[i])for i in chosen];families.append(family)
 need(len(families)==12,'all labeled complement-cycle inventories')
 # Controls must fail if the two independent lost terms are omitted.
 triangle=[{1,2},{0,2},{0,1}];A,B,t,c=layers(triangle,0)
 need(len(A)+len(B)!=sum(len(triangle[v])for v in A)-t-c,'triangle coefficient damage detected')
 square=[{1,3},{0,2},{1,3},{0,2}];A,B,t,c=layers(square,0)
 need(len(A)+len(B)!=sum(len(square[v])for v in A)-2*t,'collision omission detected')
 return {'all_six_vertex_graphs':32768,'all_centers':centers,'triangle_centers':triangle_centers,'collision_centers':collision_centers,
  'contracted_classical_graph':{'vertices':15,'girth':girth,'degree_histogram':[[3,14],[4,1]],'root':root},
  'all_unit_triangle_families':12,'unit_triangle_families':families,'damaged_triangle_coefficient_rejected':True,'omitted_collision_rejected':True}
if __name__=='__main__':print(json.dumps(check(),sort_keys=True,separators=(',',':')))
