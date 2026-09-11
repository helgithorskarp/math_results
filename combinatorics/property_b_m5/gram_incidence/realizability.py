from itertools import combinations
from functools import lru_cache
from math import gcd

def psd(matrix):
 """Exact symmetric Schur complements, with positive common scaling removed."""
 A=[list(row) for row in matrix]
 while A:
  if any(A[i][i]<0 for i in range(len(A))):return False
  p=A[0][0]
  if p==0:
   if any(A[0][j] for j in range(1,len(A))):return False
   A=[r[1:] for r in A[1:]];continue
  B=[[p*A[i][j]-A[i][0]*A[0][j] for j in range(1,len(A))] for i in range(1,len(A))]
  g=0
  for row in B:
   for x in row:g=gcd(g,x)
  A=[[x//g for x in row] for row in B] if g>1 else B
 return True

@lru_cache(None)
def support_fits(N,sizes,edges):
 d=len(sizes);adj=[0]*d
 for i,j in edges:adj[i]|=1<<j;adj[j]|=1<<i
 rem=(1<<d)-1;lower=0
 while rem:
  seed=rem&-rem;comp=seed;old=0
  while old!=comp:
   old=comp
   for i in range(d):
    if comp>>i&1:comp|=adj[i]
  rem&=~comp;vs=[i for i in range(d) if comp>>i&1]
  best=0
  for bits in range(1<<len(vs)):
   S=[vs[j] for j in range(len(vs)) if bits>>j&1]
   if all(not(adj[i]>>j&1) for i,j in combinations(S,2)):
    best=max(best,sum(sizes[i] for i in S))
  for i,j in combinations(vs,2):
   cap=min(sizes[i],sizes[j],3) if adj[i]>>j&1 else 0
   best=max(best,sizes[i]+sizes[j]-cap)
  lower+=best
 return lower<=N

def matrix_fits(N,sizes,edges,weights):
 d=len(sizes);e=sum(sizes)-N;parent=list(range(d))
 def root(x):
  while parent[x]!=x:x=parent[x]
  return x
 tree=0
 for (i,j),w in sorted(zip(edges,weights),key=lambda x:-x[1]):
  i=root(i);j=root(j)
  if i!=j:parent[i]=j;tree+=w
 if tree>e:return False
 A=[[0]*(d+1) for _ in range(d+1)]
 for i,a in enumerate(sizes):A[i][i]=a;A[i][d]=A[d][i]=a
 A[d][d]=N
 for (i,j),w in zip(edges,weights):A[i][j]=A[j][i]=w
 return psd(A)
