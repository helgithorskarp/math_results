#!/usr/bin/env python3
"""Check the fixed Parts503 + five-point double-triangle stopping certificates."""
import argparse,hashlib,json
from pathlib import Path
from itertools import combinations,product
from fractions import Fraction
from math import gcd
from collections import Counter
HERE=Path(__file__).resolve().parent;REPO=HERE.parent
D=(310,313,316,319,322,325);H=tuple(v for v in range(509) if v not in D)
RAD=(1,3,5,15,11,33,55,165);MOD=1321;ROOTS=(321,416,501)
TERMS=[(i,j,RAD.index(RAD[i]*RAD[j]//gcd(RAD[i],RAD[j])**2),2*gcd(RAD[i],RAD[j])) for i in range(8) for j in range(i+1,8)]
def require(v,m):
 if not v:raise ValueError(m)
def norm(p,q):
 a=[x-y for x,y in zip(p[:8],q[:8])];b=[x-y for x,y in zip(p[8:],q[8:])]
 out=[sum(d*(x*x+y*y) for d,x,y in zip(RAD,a,b))]+[0]*7
 for i,j,k,c in TERMS:out[k]+=c*(a[i]*a[j]+b[i]*b[j])
 return out

def geometry(rows):
 require(all(x*x%MOD==d for x,d in zip(ROOTS,(3,5,11))),'modular radical identities')
 basis=[1]*8
 for mask in range(8):
  for bit,x in enumerate(ROOTS):
   if mask>>bit&1:basis[mask]=basis[mask]*x%MOD
 ev=[(sum(a*b for a,b in zip(p[:8],basis))%MOD,sum(a*b for a,b in zip(p[8:],basis))%MOD) for p in rows]
 out=[];survivors=0
 for i,j in combinations(range(len(rows)),2):
  dx=ev[i][0]-ev[j][0];dy=ev[i][1]-ev[j][1]
  if (dx*dx+dy*dy-288**2)%MOD:continue
  survivors+=1
  if norm(rows[i],rows[j])==[288**2]+[0]*7:out.append((i,j))
 return out,survivors

def extend(lists,edges):
 order=sorted(range(5),key=lambda i:(lists[i].bit_count(),i));word=[-1]*5
 earlier=[[] for _ in range(5)];rank={v:i for i,v in enumerate(order)}
 for a,b in edges:
  if rank[a]>rank[b]:a,b=b,a
  earlier[b].append(a)
 def dfs(k):
  if k==5:return word.copy()
  v=order[k]
  for c in range(4):
   if lists[v]>>c&1 and all(word[u]!=c for u in earlier[v]):
    word[v]=c;a=dfs(k+1)
    if a is not None:return a
  word[v]=-1;return None
 return dfs(0)

def run(emit=None):
 manifest=json.loads((HERE/'manifest.json').read_text());data={}
 for path,expected in manifest.items():
  raw=(REPO/path).read_bytes();require(hashlib.sha256(raw).hexdigest()==expected,'pinned input '+path);data[path]=raw
 p=[tuple(3*int(x) for x in line.split()) for line in data['hadwiger_nelson_parts509_fold264_438_stop/points.tsv'].decode().splitlines() if line and not line.startswith('#')]
 pool=json.loads(data['hadwiger_nelson_parts509_swap_closure/completion_points.json'])['points'];q=[]
 for row in pool:
  z=[288*Fraction(x) for x in row['x']+row['y']];require(len(z)==16 and all(x.denominator==1 for x in z),'exact pool scale');q.append(tuple(map(int,z)))
 rows=p+q;require(len(p)==509 and len(q)==1158 and len(rows)==len(set(rows))==1667,'all source points distinct')
 all_edges,mod_survivors=geometry(rows)
 imported=json.loads(data['hadwiger_nelson_parts509_pair_closure/ambient_w3_edges.json'])['edges'];require(all_edges==[tuple(x) for x in imported],'every exact ambient edge compared')
 old=[(a,b) for a,b in all_edges if b<509];require(len(old)==2442,'strict positive parent edges')
 degrees=Counter(v for e in old for v in e);require(tuple(v for v in range(509) if degrees[v]==4)==D,'six degree-four vertices')
 require(not any(a in D and b in D for a,b in old),'deleted stars independent')
 hi={v:i for i,v in enumerate(H)};he=[(hi[a],hi[b]) for a,b in old if a not in D and b not in D]
 states=json.loads(data['hadwiger_nelson_parts509_degree4_list_kernel/certificate.json'])['states'];words=[r['core_coloring'] for r in states]
 require(len(he)==2418 and len(words)==22 and all(len(w)==503 for w in words),'fixed host fixtures')
 require(all(set(w)<=set('0123') and all(w[a]!=w[b] for a,b in he) for w in words),'all host words checked')
 adj=[set() for _ in q];neigh=[set() for _ in q]
 for a,b in all_edges:
  if a>=509:adj[a-509].add(b-509);adj[b-509].add(a-509)
  elif b>=509 and a not in D:neigh[b-509].add(hi[a])
 lists=[]
 for w in words:
  masks=[]
  for ns in neigh:
   used=0
   for v in ns:used|=1<<int(w[v])
   masks.append(15^used)
  lists.append(masks)
 cases=set()
 # Every eligible five-set has a marked common centre and two disjoint neighbour edges.
 for centre in range(1158):
  ts=[(a,b) for a,b in combinations(sorted(adj[centre]),2) if b in adj[a]]
  for u,v in combinations(ts,2):
   if not set(u)&set(v):cases.add(tuple(sorted((centre,*u,*v))))
 hist=Counter();counts={};selected=json.loads((HERE/'certificate.json').read_text());chosen=tuple(selected['selected_q3_indices']);actual_selected=None;edge_counts=[]
 for ids in sorted(cases):
  ie=[(a,b) for a,b in combinations(range(5),2) if ids[b] in adj[ids[a]]]
  surviving=[]
  for wi,m in enumerate(lists):
   masks=[m[v] for v in ids];extension=extend(masks,ie)
   if extension is not None:
    require(all(masks[i]>>c&1 for i,c in enumerate(extension)) and all(extension[a]!=extension[b] for a,b in ie),'direct extension witness')
    surviving.append((wi,extension))
  require(surviving,'every complete physical support has an explicit four-word')
  hist[len(surviving)]+=1;counts[ids]=len(surviving);edge_counts.append(2418+len(ie)+sum(len(neigh[v]) for v in ids))
  if ids==chosen:actual_selected=(ie,surviving)
 require(chosen==min(cases,key=lambda ids:(counts[ids],ids)),'frozen fixture-minimum selector')
 ie,surviving=actual_selected
 require(selected['removed_original']==list(D),'frozen deleted vertices')
 require([i for i,_ in surviving]==selected['surviving_fixture_indices'],'selected fixture survival set')
 require([i for i,_ in selected['surviving_fixture_extensions']]==selected['surviving_fixture_indices'],'stored extension coverage')
 for wi,tail in selected['surviving_fixture_extensions']:
  require(len(tail)==5 and all(type(c) is int and 0<=c<4 for c in tail),'stored local word domain')
  require(all(lists[wi][v]>>tail[i]&1 for i,v in enumerate(chosen)) and all(tail[a]!=tail[b] for a,b in ie),'stored local word is proper')
 require(selected['fixture_index'] in selected['surviving_fixture_indices'] and selected['four_word'][:503]==words[selected['fixture_index']],'full word extends named host fixture')
 # Check the selected negative cases by a separate exhaustive 4^5 assignment enumeration.
 for wi,m in enumerate(lists):
  masks=[m[v] for v in chosen]
  possible=any(all(masks[i]>>w[i]&1 for i in range(5)) and all(w[a]!=w[b] for a,b in ie) for w in product(range(4),repeat=5))
  require(possible==(wi in selected['surviving_fixture_indices']),'selected full local brute-force gate')
 joint_only=[wi for wi,m in enumerate(lists) if wi not in selected['surviving_fixture_indices'] and all(m[v] for v in chosen)]
 support=[p[v] for v in H]+[q[v] for v in chosen]
 physical=[(i,j) for i,j in combinations(range(508),2) if norm(support[i],support[j])==[288**2]+[0]*7]
 word=selected['four_word'];require(len(word)==508 and set(word)<=set('0123') and all(word[a]!=word[b] for a,b in physical),'literal word on all selected physical pairs')
 expected=set(he)|{(v,503+i) for i,u in enumerate(chosen) for v in neigh[u]}|{(503+i,503+j) for i,j in ie}
 require(set(physical)==expected,'complete selected contact decomposition')
 out=dict(parent_points=509,parent_edges=2442,host_points=503,host_edges=2418,removed_original=list(D),ambient_points=1667,ambient_edges=len(all_edges),ambient_pairs=1667*1666//2,exact_norm_tests_after_modular_filter=mod_survivors,double_triangle_supports=len(cases),all_supports_points=508,complete_edge_count_range=[min(edge_counts),max(edge_counts)],fixture_survival_histogram={str(k):v for k,v in sorted(hist.items())},minimum_surviving_fixtures=min(counts.values()),selected_q3_indices=list(chosen),selected_points=508,selected_edges=len(physical),selected_new_old_contacts=sum(len(neigh[v]) for v in chosen),selected_new_new_edges=len(ie),selected_surviving_fixtures=selected['surviving_fixture_indices'],selected_rejected_fixtures=22-len(surviving),selected_joint_only_fixture_rejections=joint_only,selected_single_star_fixture_rejections=22-len(surviving)-len(joint_only),all_supports_four_colourable=True,selected_full_host_relation_strictly_restricted=bool(22-len(surviving)),record_candidate=False,full_unrestricted_host_relation_enumerated=False)
 require(out==json.loads((HERE/'expected.json').read_text()),'expected result')
 if emit:
  emit.mkdir(parents=True,exist_ok=True);(emit/'selected_geometry.json').write_text(json.dumps(dict(points=support,denominator=288,edges=physical),separators=(',',':'))+'\n')
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--emit',type=Path);a=ap.parse_args();print(json.dumps(run(a.emit),indent=2))
