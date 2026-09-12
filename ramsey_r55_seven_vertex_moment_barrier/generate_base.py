from graph_types import canon_table,adj,induced
from itertools import combinations
from collections import defaultdict
from math import comb,lcm
from pathlib import Path
import numpy as np,json,time
P=Path(__file__).resolve().parent

def build(k=7,n=43,M=10,lo=18,hi=24):
 start=time.monotonic();c,reps,sizes=canon_table(k,[(i,i+1) for i in range(k-1)]);full=(1<<comb(k,2))-1
 cv,_,_=canon_table(k-1,[(i,i+1) for i in range(1,k-2)])
 ce,_,_=canon_table(k-1,[(0,1)]+[(i,i+1) for i in range(2,k-2)])
 graphs=[]
 for m in reps:
  if m>int(c[full^m]):continue
  a=adj(k,m)
  if any(induced(a,Q) in (0,1023) for Q in combinations(range(k),5)):continue
  graphs.append(m)
 print('enumeration',k,'all_types',len(reps),'labeled',sum(sizes),'good_color_types',len(graphs),'seconds',time.monotonic()-start,flush=True)
 labels=[];index={};cols=[]
 def idx(key):
  if key not in index:index[key]=len(labels);labels.append(key)
  return index[key]
 for m in graphs:
  col=defaultdict(int)
  for mask in (m,full^m):
   a=adj(k,mask)
   for v in range(k):
    for w in range(k):
     if v==w:continue
     F=int(cv[induced(a,[v]+[u for u in range(k) if u not in (v,w)])]);d=a[v].bit_count();I=(a[v]>>w)&1
     col[idx(('upper_degree',F))]+=hi-d-(n-k)*I
     col[idx(('lower_degree',F))]+=d+(n-k)*I-lo
   for u,v in combinations(range(k),2):
    if not a[u]>>v&1:continue
    co=(a[u]&a[v]).bit_count()
    for w in range(k):
     if w in (u,v):continue
     F=int(ce[induced(a,[u,v]+[t for t in range(k) if t not in (u,v,w)])]);I=((a[u]&a[v])>>w)&1
     col[idx(('codegree',F))]+=M-co-(n-k)*I
  cols.append(col)
 A=np.zeros((len(labels),len(graphs)),dtype=np.int64)
 for j,col in enumerate(cols):
  for i,v in col.items():A[i,j]=v
 ef,efs,_=canon_table(4,[(2,3)]);efs=[f for f in efs if f&1];ei={f:i for i,f in enumerate(efs)}
 vf,vfs,_=canon_table(3,[(1,2)]);vi={f:i for i,f in enumerate(vfs)}
 Q=[np.zeros((len(graphs),len(efs),len(efs)),dtype=np.int64) for _ in range(2)]+[np.zeros((len(graphs),len(vfs),len(vfs)),dtype=np.int64) for _ in range(3)]
 def weights(t):
  L=lcm(*[comb(k-t,s) for s in range(2,6)])
  return {s:L*comb(n-t,s)//comb(k-t,s) for s in range(2,6)},L
 we,Le=weights(2);wv,Lv=weights(1)
 for j,m in enumerate(graphs):
  for mask in (m,full^m):
   a=adj(k,mask)
   for u in range(k):
    for v in range(k):
     if u==v or not a[u]>>v&1:continue
     outside=[w for w in range(k) if w not in (u,v)];common=a[u]&a[v];co=common.bit_count();pairs=list(combinations(outside,2));pm=[sum(1<<t for t in pair) for pair in pairs]
     flags=[ei[int(ef[induced(a,[u,v]+list(pair))])] for pair in pairs]
     for x,px in enumerate(pm):
      for y,py in enumerate(pm):
       U=px|py;s=U.bit_count();inside=(common&U).bit_count();w=we[s]
       Q[0][j,flags[x],flags[y]]+=w
       Q[1][j,flags[x],flags[y]]+=(M-inside)*w-(co-inside)*we[s+1]
   for u in range(k):
    outside=[v for v in range(k) if v!=u];pairs=list(combinations(outside,2));pm=[sum(1<<t for t in pair) for pair in pairs];flags=[vi[int(vf[induced(a,[u]+list(pair))])] for pair in pairs];d=a[u].bit_count()
    for x,px in enumerate(pm):
     for y,py in enumerate(pm):
      U=px|py;s=U.bit_count();inside=(a[u]&U).bit_count();w=wv[s];extra=(d-inside)*wv[s+1]
      Q[2][j,flags[x],flags[y]]+=w
      Q[3][j,flags[x],flags[y]]+=(hi-inside)*w-extra
      Q[4][j,flags[x],flags[y]]+=(inside-lo)*w+extra
  if j%100==0:print('gram',j,'/',len(graphs),'seconds',time.monotonic()-start,flush=True)
 return A,graphs,labels,Q,{'k':k,'n':n,'M':M,'degree_window':[lo,hi],'all_graph_types':len(reps),'labeled_graphs':sum(sizes),'allowed_color_types':len(graphs),'edge_flag_types':efs,'vertex_flag_types':vfs,'edge_multiplier':Le,'vertex_multiplier':Lv,'seconds':time.monotonic()-start}
if __name__=='__main__':
 A,g,l,Q,meta=build();np.savez(P/'M10_sevendeck.npz',A=A,graphs=np.array(g),labels=np.array([json.dumps(x) for x in l]),**{f'Q{i}':q for i,q in enumerate(Q)});(P/'M10_sevendeck_meta.json').write_text(json.dumps(meta,indent=2)+'\n');print(meta,flush=True)
