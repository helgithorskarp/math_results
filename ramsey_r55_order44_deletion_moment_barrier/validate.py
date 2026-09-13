"""Compare lifted seven-deck tensors to direct counts in literal 8-vertex graphs."""
from generate_base import build as base_build
from generate_integer import augment
from generate_squares import build as square_build
from graph_types import canon_table,adj,induced
from itertools import combinations,permutations
from collections import Counter,defaultdict
from math import comb
from pathlib import Path
import numpy as np,json,time
P=Path(__file__).resolve().parent

def outer(f):return np.outer(f,f)
def evaluate(cs,x):return sum(c*comb(x,s) for s,c in enumerate(cs))
def direct(a,polys,meta,base_meta):
 n=len(a);base=[np.zeros((d,d),dtype=np.int64) for d in (20,20,6,6,6)]
 ints=[np.zeros((d,d),dtype=np.int64) for d in [6]*5+[4]*13]
 rows=np.zeros(len(polys),dtype=np.int64)
 sq=[np.zeros((v['dimension'],v['dimension']),dtype=np.int64) for v in meta['matrices']]
 ef,_,_=canon_table(4,[(2,3)]);ei={int(f):i for i,f in enumerate(base_meta['edge_flag_types'])}
 vf,_,_=canon_table(3,[(1,2)]);vi={int(f):i for i,f in enumerate(base_meta['vertex_flag_types'])}
 vf4,_,_=canon_table(4,[(1,2),(2,3)]);vi4={int(f):i for i,f in enumerate(meta['vertex_flags'])}
 tf,_,_=canon_table(5,[(3,4)]);ti={int(r):{int(f):i for i,f in enumerate(fs)} for r,fs in meta['three_root_flags'].items()}
 for a0 in [a,[((1<<n)-1)^(1<<v)^a[v] for v in range(n)]]:
  for u in range(n):
   d=a0[u].bit_count();outs=[v for v in range(n) if v!=u];f=np.zeros(6,dtype=np.int64)
   for S in combinations(outs,2):f[vi[int(vf[induced(a0,[u]+list(S))])]]+=1
   R=outer(f);base[2]+=R;base[3]+=(24-d)*R;base[4]+=(d-19)*R
   for j in range(19,24):ints[j-19]+=(d-j)*(d-j-1)*R
   f4=np.zeros(20,dtype=np.int64)
   for S in combinations(outs,3):f4[vi4[int(vf4[induced(a0,[u]+list(S))])]]+=1
   sq[0]+=outer(f4)
   for i,(kind,label,cs) in enumerate(polys):
    if kind=='degree_indicator':rows[i]+=420*evaluate(cs,d)
  for u,v in combinations(range(n),2):
   if not a0[u]>>v&1:continue
   co=(a0[u]&a0[v]).bit_count()
   for i,(kind,label,cs) in enumerate(polys):
    if kind=='book_support':rows[i]+=60*evaluate(cs,co)
  for u,v in permutations(range(n),2):
   if not a0[u]>>v&1:continue
   outs=[w for w in range(n) if w not in (u,v)];co=(a0[u]&a0[v]).bit_count();f=np.zeros(20,dtype=np.int64);fb=np.zeros(4,dtype=np.int64)
   for S in combinations(outs,2):f[ei[int(ef[induced(a0,[u,v]+list(S))])]]+=1
   for w in outs:fb[((a0[u]>>w)&1)+2*((a0[v]>>w)&1)]+=1
   R=outer(f);base[0]+=R;base[1]+=(13-co)*R
   for j in range(13):ints[5+j]+=(co-j)*(co-j-1)*outer(fb)
  for ix,matmeta in enumerate(meta['matrices'][1:],1):
   label=matmeta['label'];keep=matmeta['kept_indices'];t=3 if label.startswith('three') else 5;root=int(label.rsplit('_',1)[1]);dim=len(ti[root]) if t==3 else 32
   for R in permutations(range(n),t):
    if induced(a0,R)!=root:continue
    outs=[v for v in range(n) if v not in R];f=np.zeros(dim,dtype=np.int64)
    if t==3:
     for S in combinations(outs,2):f[ti[root][int(tf[induced(a0,list(R)+list(S))])]]+=1
    else:
     for v in outs:f[sum(((a0[u]>>v)&1)<<i for i,u in enumerate(R))]+=1
    f=f[keep];sq[ix]+=outer(f)
 for i in range(5):base[i]*=60 if i<2 else 420
 for i in range(18):ints[i]*=420 if i<5 else 60
 for i in range(len(sq)):sq[i]*=420 if i==0 else 60 if i<3 else 6
 return rows,base+ints+sq

def scalar_direct(a,labels):
 n=len(a);cv,_,_=canon_table(6,[(i,i+1) for i in range(1,5)]);ce,_,_=canon_table(6,[(0,1),(2,3),(3,4),(4,5)]);values=defaultdict(int)
 for a0 in [a,[((1<<n)-1)^(1<<v)^a[v] for v in range(n)]]:
  for F in combinations(range(n),6):
   for v in F:
    flag=int(cv[induced(a0,[v]+[w for w in F if w!=v])]);d=a0[v].bit_count();values[('upper_degree',flag)]+=2*(24-d);values[('lower_degree',flag)]+=2*(d-19)
   for u,v in combinations(F,2):
    if a0[u]>>v&1:
     flag=int(ce[induced(a0,[u,v]+[w for w in F if w not in (u,v)])]);values[('codegree',flag)]+=2*(13-(a0[u]&a0[v]).bit_count())
 return np.array([values[tuple(label)] for label in labels],dtype=np.int64)

def run(output):
 start=time.monotonic();A,graphs,labels,Q,bmeta=base_build(n=8);AA,QQ,polys=augment(graphs,n=8);Qs,smeta=square_build(graphs,n=8);c,_,_=canon_table(7,[(i,i+1) for i in range(6)]);index={g:i for i,g in enumerate(graphs)};tests=[]
 fixtures={'cycle8':[(i,(i+1)%8) for i in range(8)],'cube3':[(i,j) for i in range(8) for j in range(i+1,8) if (i^j).bit_count()==1]}
 for name,edges in fixtures.items():
  a=[0]*8
  for u,v in edges:a[u]|=1<<v;a[v]|=1<<u
  assert all(induced(a,S) not in (0,1023) for S in combinations(range(8),5))
  counts=np.zeros(len(graphs),dtype=np.int64)
  for S in combinations(range(8),7):
   m=induced(a,S);r=min(int(c[m]),int(c[((1<<21)-1)^m]));counts[index[r]]+=1
  dr,dq=direct(a,polys,smeta,bmeta);assert np.array_equal(A@counts,scalar_direct(a,labels)),name+' scalar rows';assert np.array_equal(AA@counts,dr),name+' integer scalar rows'
  for i,(tensor,direct_q) in enumerate(zip(Q+QQ+Qs,dq)):
   computed=np.einsum('g,gij->ij',counts,tensor);assert np.array_equal(computed,direct_q),(name,'matrix',i,int(np.max(abs(computed-direct_q))))
  tests.append({'fixture':name,'edges':edges,'order':8,'induced_seven_subsets':int(counts.sum()),'scalar_rows_checked':len(A)+len(AA),'matrices_checked':len(dq),'status':'EXACT_ENTRYWISE_MATCH'})
 out={'status':'DIRECT_COUNT_IDENTITIES_VERIFIED','tests':tests,'seconds':time.monotonic()-start,'scope':'Definition-level checks of finite lifting identities on two literal graphs; not a formal proof or physical good44 decision.'};Path(output).write_text(json.dumps(out,indent=2)+'\n');print(out,flush=True);return out
