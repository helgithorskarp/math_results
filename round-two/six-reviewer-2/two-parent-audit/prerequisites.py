"""Fresh BASE177/five-tail120/pair28/25 and complete inactive-state controls."""
from itertools import combinations,product
from math import comb,lcm
import hashlib,json
P=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
D=tuple(d for d in range(2,316)if 315%d==0)
def need(ok,why):
 if not ok:raise ValueError(why)
def wire(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def compute():
 R=tuple(n for n in range(2520)if all(n%m!=a for m,a in P));full=(1<<len(R))-1
 labels=tuple(m for m in range(8,2521)if 2520%m==0 and m not in {m for m,a in P});masks={}
 for m in labels:
  masks[m]=[0]*m
  for j,n in enumerate(R):masks[m][n%m]|=1<<j
 marginal=[]
 for a,b in product(range(15),range(18)):
  union=masks[15][a]|masks[18][b];rem=full^union
  values=[[m,max((z&rem).bit_count()for z in masks[m])]for m in labels if m not in(15,18)]
  marginal.append([a,b,union.bit_count(),values,union.bit_count()+sum(v for m,v in values)])
 cap={r:{d:max(sum(n%8==r and n%d==a for n in R)for a in range(d))for d in(1,)+D}for r in(1,2,4,6)}
 five=[[f,g,q,cap[2][f]+cap[6][lcm(g,q)]]for f,g in product(D,repeat=2)if f!=g for q in D]
 # Odd parents use identical capacities, verified separately by incidence/direct.
 # Rebuild them here rather than assume their residue populations.
 pair=[]
 for r in(1,3,4,5,7):
  for a,b in combinations(D,2):
   m=lcm(a,b);v=max(sum(n%8==r and n%m==phase for n in R)for phase in range(m));pair.append([r,a,b,v])
 controls=[]
 for parent,placed,lo,hi in ((2,3,1,3),(6,1,2,4),(4,0,2,4)):
  for length in range(lo,hi+1):
   for h in range(length+1):
    q=length-h
    for hs,qs in product(product((0,3,12),repeat=h),product((0,1,2,4,8),repeat=q)):
     initial=placed
     for v in hs+qs:initial|=v
     nh=tuple(12 if v else 0 for v in hs)if parent==2 else hs
     nq=tuple((4 if v and(v&placed)else v)for v in qs)if parent==2 else tuple((2 if v==1 else v)for v in qs)if parent==6 else qs
     modified=placed
     for v in nh+nq:modified|=v
     need(initial!=15 or modified==15,'moving already-filled footprints never destroys complete four-lift repair')
     # Direct active-footprint redundancy at the marked32 parent.
     without=0
     for v in hs+qs:without|=v
     if parent==6 and q==0 and initial==15:need(without==15,'all-H repair makes the placed32 redundant')
     controls.append([parent,h,q,list(hs),list(qs),initial,modified])
 return dict(BASE_rows=marginal,BASE_holes_lower=len(R)-max(v[-1]for v in marginal),five_rows=five,five_max=max(v[-1]for v in five),pair_rows=pair,pair_max={str(r):max(v[-1]for v in pair if v[0]==r)for r in(1,3,4,5,7)},binary_controls=controls,binary_control_count=len(controls),native_imported=False)
if __name__=='__main__':
 import sys
 from pathlib import Path
 p=Path(sys.argv[1]);p.mkdir(parents=True,exist_ok=False);x=compute();(p/'record.json').write_bytes(wire(x)+b'\n');print(wire({k:x[k]for k in('BASE_holes_lower','five_max','pair_max','binary_control_count')}).decode())
