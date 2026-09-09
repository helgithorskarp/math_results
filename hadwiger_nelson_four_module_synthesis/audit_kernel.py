#!/usr/bin/env python3
"""Independent certificate coverage via complements and a degree polynomial."""
from itertools import combinations,permutations
from functools import lru_cache
import hashlib,json

def need(x,msg):
 if not x:raise ValueError(msg)

@lru_cache(None)
def matchings(vs):
 if not vs:return ((),)
 a,*rest=vs;out=[]
 for b in rest:
  tail=tuple(x for x in rest if x!=b)
  out.extend(((a,b),)+p for p in matchings(tail))
 return tuple(out)

@lru_cache(None)
def two_factors(vs):
 if not vs:return ((),)
 if len(vs)<3:return ()
 a=vs[0];out=[]
 for length in range(3,len(vs)+1):
  for subset in combinations(vs[1:],length-1):
   tails=two_factors(tuple(x for x in vs if x!=a and x not in subset))
   for order in permutations(subset):
    if order[0]>order[-1]:continue
    cycle=(a,)+order
    edges=tuple(tuple(sorted((cycle[i],cycle[(i+1)%length]))) for i in range(length))
    out.extend(edges+tail for tail in tails)
 return tuple(out)

def degree_coefficient(n,d):
 # Coefficient [x_0^d ... x_(n-1)^d] product_(i<j)(1+x_i*x_j).
 # This counts all labelled simple regular graphs without generating them.
 if d==0:return 1
 width=d.bit_length();mask=(1<<width)-1
 counts={0:1}
 for i,j in combinations(range(n),2):
  increment=(1<<(width*i))+(1<<(width*j));nxt=counts.copy()
  for state,count in counts.items():
   if (state>>(width*i)&mask)<d and (state>>(width*j)&mask)<d:
    nxt[state+increment]=nxt.get(state+increment,0)+count
  counts=nxt
 target=sum(d<<(width*i) for i in range(n))
 return counts.get(target,0)

def run():
 results=[]
 for n in range(5,9):
  es=list(combinations(range(n),2));idx={e:k for k,e in enumerate(es)};full=(1<<len(es))-1
  def bits(edges):return sum(1<<idx[tuple(sorted(e))] for e in edges)
  witnesses={}
  if n==5:witnesses[0]=None
  elif n==6:
   for m in matchings(tuple(range(n))):witnesses[bits(m)]=m
  elif n==7:
   for factor in two_factors(tuple(range(n))):
    f=bits(factor)
    pairs=next((m for single in range(n) for m in matchings(tuple(i for i in range(n) if i!=single)) if bits(m)&f==bits(m)),None)
    need(pairs is not None,'uncovered degree2 complement');witnesses[f]=pairs
  else:
   factors=[bits(f) for f in two_factors(tuple(range(n)))]
   for m in matchings(tuple(range(n))):
    b=bits(m)
    for f in factors:
     if not b&f:witnesses.setdefault(b|f,m)
  total=degree_coefficient(n,n-5)
  need(len(witnesses)==total,'positive complement cover is incomplete')
  coloured=0
  for mask,m in witnesses.items():
   degree=[0]*n
   for k,(i,j) in enumerate(es):
    if mask>>k&1:degree[i]+=1;degree[j]+=1
   need(degree==[n-5]*n,'complement degree')
   if m is None:need(n==5 and mask==0,'K5 exception');continue
   word=[-1]*n
   for c,(i,j) in enumerate(m):word[i]=word[j]=c
   for i in range(n):
    if word[i]<0:word[i]=len(m)
   need(max(word)<4 and all(word[i]!=word[j] for k,(i,j) in enumerate(es) if not(mask>>k&1)),'bad positive colouring')
   coloured+=1
  graph_masks=sorted(full^m for m in witnesses)
  results.append({'vertices':n,'degree_polynomial_count':total,'positive_covered_graphs':coloured,'graph_set_sha256':hashlib.sha256((','.join(map(str,graph_masks))+'\n').encode()).hexdigest()})
 # K5 unit-edge masks independently generated as equivalence partitions.
 partitions=[]
 def add(prefix):
  if len(prefix)==5:
   if all(prefix.count(c)<=3 for c in set(prefix)):partitions.append(prefix)
   return
  for c in range(1+max(prefix,default=-1)+1):add(prefix+[c])
 add([])
 es=list(combinations(range(5),2));masks=sorted(sum(1<<k for k,(i,j) in enumerate(es) if p[i]==p[j]) for p in partitions)
 need(len(masks)==len(set(masks))==46,'partition count')
 return {'method':'matching-plus-cycle covers compared with exact degree-polynomial coefficients','finite_kernels':results,'K5_geometry':{'equivalence_partitions':len(masks),'minimum_long_edges':min(10-m.bit_count() for m in masks),'surviving_masks_sha256':hashlib.sha256((','.join(map(str,masks))+'\n').encode()).hexdigest()}}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
