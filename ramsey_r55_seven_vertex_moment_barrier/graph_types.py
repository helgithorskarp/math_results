"""Exact labeled-graph orbit enumeration under explicit vertex swaps."""
from itertools import combinations
import numpy as np

def canon_table(n,gens):
 E=list(combinations(range(n),2));index={e:i for i,e in enumerate(E)};N=1<<len(E);maps=[]
 for u,v in gens:
  perm=list(range(n));perm[u],perm[v]=v,u
  bits=[1<<index[tuple(sorted((perm[a],perm[b])))] for a,b in E]
  table=np.zeros(N,dtype=np.int32)
  for m in range(1,N):
   b=m&-m;table[m]=table[m^b]+bits[b.bit_length()-1]
  maps.append(table)
 canonical=np.full(N,-1,dtype=np.int32);reps=[];sizes=[]
 for m in range(N):
  if canonical[m]>=0:continue
  reps.append(m);q=[m];canonical[m]=m
  for t in q:
   for g in maps:
    w=int(g[t])
    if canonical[w]<0:canonical[w]=m;q.append(w)
  sizes.append(len(q))
 return canonical,reps,sizes

def adj(n,mask):
 a=[0]*n
 for i,(u,v) in enumerate(combinations(range(n),2)):
  if mask>>i&1:a[u]|=1<<v;a[v]|=1<<u
 return a

def induced(a,vertices):
 return sum(((a[u]>>v)&1)<<i for i,(u,v) in enumerate(combinations(vertices,2)))
