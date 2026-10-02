#!/usr/bin/env python3
"""Independent exact shared-tail resource graph and complete4/5 clique census."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import argparse,json,hashlib
from core import parent,pts,mask,packing,need,canon
def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);args=p.parse_args();data=json.loads((args.work/'cores.json').read_text());cores=data['cores'];D=parent();N=len(cores)
 tripleindex={mask(t):i for i,t in enumerate(combinations(range(17),3))};pairindex={mask(t):i for i,t in enumerate(combinations(range(17),2))}
 tails=sorted({t for C,ss in cores for b,t in ss});tailindex={t:i for i,t in enumerate(tails)}
 def footprint(w,k,index):return sum(1<<index[mask(t)]for t in combinations(pts(w),k))
 features=[]
 for C,ss in cores:
  ts=[t for b,t in ss];tb=0;pb=0;ib=0
  for t in ts:tb|=footprint(t,3,tripleindex);pb|=footprint(t,2,pairindex);ib|=1<<tailindex[t]
  need(pb.bit_count()==6*len(ts),'within-core tail pair resources distinct')
  features.append((footprint(C,3,tripleindex),tb,pb,ib))
 adj=[0]*N;edgecount=0;comparisons=0
 for u in range(N):
  cu,tu,pu,iu=features[u]
  for v in range(u+1,N):
   cv,tv,pv,iv=features[v];comparisons+=1
   # Cap triples cannot repeat; tail triples cannot collide with the other
   # cap; only identical shared tails may repeat their six old pairs.
   if cu&cv or cu&tv or cv&tu:continue
   if (pu&pv).bit_count()!=6*(iu&iv).bit_count():continue
   adj[u]|=1<<v;adj[v]|=1<<u;edgecount+=1
 def bits(m):
  while m:
   b=m&-m;yield b.bit_length()-1;m^=b
 triangles=0;four=[];five=[];edgechecks=0;trianglechecks=0
 for u in range(N):
  for v in bits(adj[u]>> (u+1)):
   v+=u+1;edgechecks+=1
   common=adj[u]&adj[v]
   for w in bits(common>>(v+1)):
    w+=v+1;triangles+=1;trianglechecks+=1
    c4=common&adj[w]
    for z in bits(c4>>(w+1)):
     z+=w+1;four.append((u,v,w,z))
     for q in bits((c4&adj[z])>>(z+1)):five.append((u,v,w,z,q+z+1))
 need(not five,'actual5 clique exists; sharp69 verdict fails')
 codes=[]
 for clique in four:
  Cset={cores[i][0]for i in clique};taildict={}
  for i in clique:
   for b,t in cores[i][1]:
    need(b not in taildict or taildict[b]==t,'same parent must carry identical tail');taildict[b]=t
  words=sorted([b for b in D if b not in data['holes']and b not in taildict]+list(Cset)+[data['Q']|(1<<17)]+[t|(1<<17)for t in taildict.values()])
  need(len(words)==69,'literal normalized69 size');packing(words);codes.append(words)
 need(len({tuple(c)for c in codes})==len(codes),'unique clique-to-normal-form reconstruction')
 spectra=Counter(tuple(sorted(sum(bool(w>>v&1)for w in code)for v in range(18)))for code in codes)
 rowsraw=canon(adj);formsraw=canon({'words':sorted(codes)});(args.work/'graph.json').write_bytes(rowsraw);(args.work/'NORMAL_FORMS.json').write_bytes(formsraw)
 print(json.dumps({'complete':True,'vertices':N,'unordered_original_core_pairs':comparisons,'edges':edgecount,'triangles':triangles,'four_cliques':len(four),'five_cliques':len(five),'original_ordered_graph_rows_sha256':hashlib.sha256(rowsraw).hexdigest(),'normal_forms_bytes':len(formsraw),'normal_forms_sha256':hashlib.sha256(formsraw).hexdigest(),'whole69_pairs_checked':len(codes)*2346,'whole69_distinct_triples_checked':len(codes)*690,'replication_spectra':[{'degrees':list(k),'codes':v}for k,v in sorted(spectra.items())],'edge_common_neighbor_tests':edgechecks,'triangle_common_neighbor_tests':trianglechecks,'shared_identical_tail_rule_verified':True},sort_keys=True))
if __name__=='__main__':main()
