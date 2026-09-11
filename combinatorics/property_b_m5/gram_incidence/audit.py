"""Deterministic controls using different exact representations."""
import sys,json,random
from fractions import Fraction
from itertools import combinations
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]/'incidence_forests'))
import core
from graphs import all_graphs
from realizability import psd,support_fits,matrix_fits
from exact_union import count_critical

def det(matrix):
 A=[[Fraction(x) for x in r] for r in matrix];ans=Fraction(1)
 for i in range(len(A)):
  p=next((j for j in range(i,len(A)) if A[j][i]),None)
  if p is None:return 0
  if p!=i:A[i],A[p]=A[p],A[i];ans=-ans
  z=A[i][i];ans*=z
  for j in range(i+1,len(A)):
   f=A[j][i]/z
   for k in range(i+1,len(A)):A[j][k]-=f*A[i][k]
 return ans

def run():
 rng=random.Random(270035);matrices=0
 for n in range(1,6):
  for t in range(80):
   if t%2:
    B=[[rng.randrange(-3,4) for _ in range(n+1)] for _ in range(n)]
    A=[[sum(a*b for a,b in zip(B[i],B[j])) for j in range(n)] for i in range(n)]
   else:
    A=[[0]*n for _ in range(n)]
    for i in range(n):
     for j in range(i+1):A[i][j]=A[j][i]=rng.randrange(-4,6)
   exact=all(det([[A[i][j] for j in S] for i in S])>=0 for k in range(1,n+1) for S in combinations(range(n),k))
   assert psd(A)==exact
   matrices+=1
 links=counts=0
 while links<426:
  d=rng.randrange(2,8);sets=[set(rng.sample(range(8),rng.randrange(1,5))) for _ in range(d)]
  sizes=tuple(map(len,sets))
  if any(len(sets[i]&sets[j])>3 for i,j in combinations(range(d),2)):continue
  N=len(set.union(*sets));edges=tuple((i,j) for i,j in combinations(range(d),2) if sets[i]&sets[j]);weights=[len(sets[i]&sets[j]) for i,j in edges]
  assert support_fits(N,sizes,edges) and matrix_fits(N,sizes,edges,weights)
  assert sum(weights)>=sum(sizes)-N
  assert all(sum(weights[k] for k in ix)<=sizes[u] for u,ix in core.independence_tests(d,edges))
  links+=1
  if counts<120:
   rows=tuple((a,rng.randrange(4)) for a in sizes)
   columns=[tuple(i for i in range(d) if u in sets[i]) for u in sorted(set.union(*sets))]
   shared=[c for c in columns if len(c)>1];L=N//2
   assert count_critical(rows,shared,L)==core.count_critical(rows,shared,L)
   # Direct subsets of the original labeled union, a third representation.
   direct=0
   for ss in combinations(sorted(set.union(*sets)),L):
    C=set(ss)
    direct+=bool(any(f&1 and sets[i]<=C for i,(a,f) in enumerate(rows)) and any(f&2 and not sets[i]&C for i,(a,f) in enumerate(rows)))
   assert count_critical(rows,shared,L)==(direct,N)
   counts+=1
 canonical=[]
 for n,k in [(4,6),(5,10),(6,15),(7,7)]:
  fast,_=all_graphs(n,k);old,_=core.all_graphs(n,k)
  assert {core.canonical(n,g) for g in fast}==set(old)
  canonical.append({'n':n,'max_edges':k,'graphs':len(fast)})
 rows=((4,3),)*8
 columns=[p for tri in [(0,1,2),(3,4,5)] for p in combinations(tri,2) for _ in range(2)]
 a=count_critical(rows,columns,10);assert a==core.count_critical(rows,columns,10)==(29972,20)
 return {'principal_minor_controls':matrices,'covering_link_controls':links,'three_way_event_counts':counts,'canonical_controls':canonical,'two_triangle_exact_count':list(a)}
if __name__=='__main__':
 assert __debug__,'Run without -O'
 print(json.dumps(run(),indent=2,sort_keys=True))
