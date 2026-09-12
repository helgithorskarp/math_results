from graph_types import canon_table,adj,induced
from itertools import combinations,permutations
from math import comb,lcm
from pathlib import Path
import numpy as np,json,time
P=Path(__file__).resolve().parent

def build(graphs,n=43,k=7):
 start=time.monotonic();full=(1<<comb(k,2))-1
 # One-root flags use three unordered additional vertices.
 cv,rv,_=canon_table(4,[(1,2),(2,3)]);vi={f:i for i,f in enumerate(rv)}
 Qv=np.zeros((len(graphs),len(rv),len(rv)),dtype=np.int64)
 wv={s:60*comb(n-1,s)//comb(k-1,s) for s in range(3,7)}
 # Ordered three-root flags use two unordered additional vertices.
 cf,rf,_=canon_table(5,[(3,4)]);types3=[1,7];flagsets={}
 for root in types3:
  flagsets[root]=[f for f in rf if induced(adj(5,f),[0,1,2])==root and f not in (0,1023)]
 fi={root:{f:i for i,f in enumerate(fs)} for root,fs in flagsets.items()}
 Q3={root:np.zeros((len(graphs),len(fs),len(fs)),dtype=np.int64) for root,fs in flagsets.items()}
 w3={s:12*comb(n-3,s)//comb(k-3,s) for s in range(2,5)}
 # Every allowed labeled five-root type, modulo root relabeling. All 32
 # unlabeled types are kept; color-dual redundancy is harmless.
 c5,r5,_=canon_table(5,[(i,i+1) for i in range(4)]);r5=[r for r in r5 if r not in (0,1023)]
 Q5={root:np.zeros((len(graphs),32,32),dtype=np.int64) for root in r5}
 w5={s:2*comb(n-5,s)//comb(k-5,s) for s in (1,2)}
 root3=list(permutations(range(k),3));root5=list(permutations(range(k),5))
 for g,mask in enumerate(graphs):
  for m in (mask,full^mask):
   a=adj(k,m)
   for u in range(k):
    triples=list(combinations([v for v in range(k) if v!=u],3));masks=[sum(1<<t for t in S) for S in triples];flags=[vi[int(cv[induced(a,[u]+list(S))])] for S in triples]
    for x,A in enumerate(masks):
     for y,B in enumerate(masks):Qv[g,flags[x],flags[y]]+=wv[(A|B).bit_count()]
   for R in root3:
    root=induced(a,R)
    if root not in Q3:continue
    outside=[v for v in range(k) if v not in R];pairs=list(combinations(outside,2));masks=[sum(1<<t for t in S) for S in pairs];flags=[fi[root][int(cf[induced(a,list(R)+list(S))])] for S in pairs]
    for x,A in enumerate(masks):
     for y,B in enumerate(masks):Q3[root][g,flags[x],flags[y]]+=w3[(A|B).bit_count()]
   for R in root5:
    root=induced(a,R)
    if root not in Q5:continue
    outside=[v for v in range(k) if v not in R];flags=[sum(((a[u]>>v)&1)<<i for i,u in enumerate(R)) for v in outside]
    for x in range(2):
     for y in range(2):Q5[root][g,flags[x],flags[y]]+=w5[1 if x==y else 2]
  if g%100==0:print('full squares',g,'/',len(graphs),time.monotonic()-start,flush=True)
 matrices=[Qv]+[Q3[r] for r in types3]+[Q5[r] for r in r5];labels=['vertex_triples']+[f'three_root_{r}' for r in types3]+[f'five_root_{r}' for r in r5];meta=[];out=[]
 for label,q in zip(labels,matrices):
  keep=np.where(np.any(q!=0,axis=(0,1)))[0];q=q[:,keep][:,:,keep];out.append(q);meta.append({'label':label,'kept_indices':keep.tolist(),'dimension':len(keep)})
 return out,{'matrices':meta,'three_root_flags':flagsets,'vertex_flags':rv,'n':n,'k':k,'seconds':time.monotonic()-start,'claim':'Additional exact finite rooted-square count matrices; no physical decision.'}
if __name__=='__main__':
 graphs=np.load(P/'M10_sevendeck.npz')['graphs'].tolist();Q,meta=build(graphs);np.savez(P/'M10_full_squares.npz',**{f'Q{i}':q for i,q in enumerate(Q)});(P/'M10_full_squares_meta.json').write_text(json.dumps(meta,indent=2)+'\n');print('DONE',len(Q),meta['seconds'],flush=True)
