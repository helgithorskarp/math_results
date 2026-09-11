"""Exact link unions, parameterized by incidence excess; see proof.md."""
from functools import lru_cache
from itertools import combinations,permutations,product
from math import comb,factorial
from fractions import Fraction as F

def canonical(rows,columns):
 q=len(columns)
 # Permuting shared vertices and incident edges leaves the coloring count invariant.
 if not q:return tuple(sorted((a,f,0) for a,f in rows))
 best=None
 for order in permutations(range(q)):
  z=tuple(sorted((a,f,sum(1<<j for j,i in enumerate(order) if columns[i]>>u&1)) for u,(a,f) in enumerate(rows)))
  if best is None or z<best:best=z
 return best

@lru_cache(None)
def overlap_types(rows,e):
 d=len(rows);caps=[a for a,f in rows]
 choices=[]
 for k in range(2,min(e+1,d)+1):
  for vs in combinations(range(d),k):choices.append((sum(1<<u for u in vs),vs,k-1))
 choices.sort();out=set()
 def rec(i,left,cols):
  if left==0:out.add(canonical(rows,cols));return
  for j in range(i,len(choices)):
   mask,vs,cost=choices[j]
   if cost>left or any(caps[u]==0 for u in vs):continue
   for u in vs:caps[u]-=1
   rec(j,left-cost,cols+[mask])
   for u in vs:caps[u]+=1
 rec(0,e,[])
 return tuple(out)

@lru_cache(None)
def count_critical(rows,L):
 q=max((mask.bit_length() for a,f,mask in rows),default=0)
 N=q+sum(a-mask.bit_count() for a,f,mask in rows)
 total=0
 for colors in range(1<<q):
  nleft=colors.bit_count()
  if nleft>L:continue
  dp={(nleft,0):1}
  for a,f,mask in rows:
   a-=mask.bit_count()
   allowL=f&1 and mask&~colors==0
   allowR=f&2 and mask&colors==0
   nxt={}
   for (t,flags),cnt in dp.items():
    for j in range(min(a,L-t)+1):
     ff=flags|(1 if allowL and j==a else 0)|(2 if allowR and j==0 else 0)
     key=(t+j,ff);nxt[key]=nxt.get(key,0)+cnt*comb(a,j)
   dp=nxt
  total+=dp.get((L,3),0)
 return total,N

@lru_cache(None)
def envelope(rows,N,L,max_excess=3):
 rows=tuple(sorted(rows));e=sum(a for a,f in rows)-N
 if e<0:return None
 if e>max_excess:return None
 types=overlap_types(rows,e)
 if not types:return None
 vals=[]
 for key in types:
  count,n=count_critical(key,L);assert n==N
  vals.append(count)
 return max(vals),comb(N,L),len(types)
