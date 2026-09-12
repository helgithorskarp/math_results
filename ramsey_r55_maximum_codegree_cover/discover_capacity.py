"""Optional floating LP discovery; not required by the integer checker.
Requires numpy 2.4.6 and scipy 1.17.1. Output must go to a bulk directory.
"""
from itertools import combinations
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
import json,time,argparse
p=None  # Set to the mandatory bulk output directory by the CLI.
R={(1,t):1 for t in range(1,6)}|{(2,t):t for t in range(2,6)}|{(3,3):6,(3,4):9,(3,5):14,(4,4):18,(4,5):25,(5,5):46}
R|={(b,a):v for (a,b),v in list(R.items())}
def config(S,kind):
 n=16;a=[0]*n
 def put(u,v):a[u]|=1<<v;a[v]|=1<<u
 put(0,1)
 for u in [0,1]:
  for v in range(2,15):put(u,v)
 for i,j in combinations(range(13),2):
  if (i-j)%13 in [1,5,8,12]:put(i+2,j+2)
 for i in S:put(15,i+2)
 if kind=='A':put(0,15)
 return a

def run(S,kind):
 started=time.monotonic();a=config(S,kind);n=len(a);U=(1<<n)-1;blue=[U^((1<<v)|a[v]) for v in range(n)];cliques={1:[(0,0)],0:[(0,0)]}
 for c,rows in [(1,a),(0,blue)]:
  for k in range(1,5):
   for Q in combinations(range(n),k):
    if all(rows[u]>>v&1 for u,v in combinations(Q,2)):cliques[c].append((sum(1<<v for v in Q),k))
 domains=np.array([mask for mask in range(1<<n) if mask&3!=3 and not any(mask&q==q for q,k in cliques[1] if k==4) and not any(mask&q==0 for q,k in cliques[0] if k==4)],dtype=np.uint32)
 # Explicitly preserve the same maximum-codegree-domain restrictions as the first probe.
 keep=np.ones(len(domains),dtype=bool)
 for v in range(n):
  for j,mask in enumerate(domains):
   mask=int(mask)
   if (((a[v]&mask) if mask>>v&1 else blue[v]&(U^mask)).bit_count()>13):keep[j]=False
 domains=domains[keep];indices=[];offsets=[0];bounds=[];labels=[];used={}
 for rr,kr in cliques[1]:
  for bb,kb in cliques[0]:
   if rr&bb or kr+kb==0:continue
   inside=sum(((a[v]&rr)==rr and (blue[v]&bb)==bb) for v in range(n) if not (rr|bb)>>v&1)
   cap=R[5-kr,5-kb]-1-inside
   assert cap>=0
   ids=np.flatnonzero((domains&rr==rr)&(domains&bb==0))
   if not len(ids):continue
   # Identical row supports are the same inequality; keep the strongest exact RHS.
   key=ids.astype(np.uint16).tobytes()
   if key in used:
    z=used[key]
    if cap<bounds[z]:bounds[z]=cap;labels[z]=[rr,bb,kr,kb,inside,R[5-kr,5-kb]-1]
   else:
    used[key]=len(bounds);bounds.append(cap);labels.append([rr,bb,kr,kb,inside,R[5-kr,5-kb]-1]);indices.extend(ids.tolist());offsets.append(len(indices))
 print('matrix',S,kind,'domains',len(domains),'rows',len(bounds),'nonzeros',len(indices),'buildsecs',time.monotonic()-started,flush=True)
 A=csr_matrix((np.ones(len(indices)),np.array(indices,dtype=np.int32),np.array(offsets,dtype=np.int64)),shape=(len(bounds),len(domains)))
 res=linprog(-np.ones(len(domains)),A_ub=A,b_ub=bounds,bounds=(0,None),method='highs')
 name=f'mixed-{kind}-{S[3]}'
 out={'S':S,'kind':kind,'variables':len(domains),'rows':len(bounds),'nonzeros':len(indices),'status':int(res.status),'message':res.message,'maximum_extra':-res.fun if res.success else None,'needed':27,'seconds':time.monotonic()-started}
 if res.success:
  out['dual']=[[labels[i],float(-v)] for i,v in enumerate(res.ineqlin.marginals) if abs(v)>1e-9];out['primal']=[[int(domains[j]),float(x)] for j,x in enumerate(res.x) if x>1e-8]
 (p/(name+'.json')).write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ['dual','primal']},flush=True)
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--outdir',type=Path,required=True);ap.add_argument('--kind',choices=['A','T']);ap.add_argument('--seed',type=int,choices=[5,6]);args=ap.parse_args();p=args.outdir;p.mkdir(parents=True,exist_ok=True)
 for S in [[0,1,2,5,6],[0,1,2,6,9]]:
  if args.seed is not None and S[3]!=args.seed:continue
  for kind in ['A','T']:
   if args.kind is not None and kind!=args.kind:continue
   run(S,kind)
