#!/usr/bin/env python3
"""Exact labelled 4-regular kernel enumeration and positive pair colourings."""
from itertools import combinations
from functools import lru_cache
import hashlib,json

def require(x,msg):
 if not x:raise ValueError(msg)

@lru_cache(None)
def pairings(vertices):
 if not vertices:return ((),)
 a=vertices[0];out=[]
 for j in range(1,len(vertices)):
  b=vertices[j];rest=vertices[1:j]+vertices[j+1:]
  out.extend((((a,b),)+p) for p in pairings(rest))
 return tuple(out)

def regular_graphs(n,d):
 """Select each row's later neighbours, with exact residual degrees."""
 adj=[0]*n;degrees=[d]*n
 def visit(i):
  if i==n:
   if not any(degrees):yield tuple(adj)
   return
  eligible=[j for j in range(i+1,n) if degrees[j]>0]
  if degrees[i]<0 or degrees[i]>len(eligible):return
  for choice in combinations(eligible,degrees[i]):
   old=degrees[i];degrees[i]=0
   for j in choice:
    degrees[j]-=1;adj[i]|=1<<j;adj[j]|=1<<i
   # Every remaining unsatisfied vertex has at most n-i-2 future peers.
   if all(0<=degrees[j]<=n-i-2 for j in range(i+1,n)) and sum(degrees)%2==0:
    yield from visit(i+1)
   for j in choice:
    degrees[j]+=1;adj[i]^=1<<j;adj[j]^=1<<i
   degrees[i]=old
 yield from visit(0)

def colour_from_pairs(adj):
 n=len(adj)
 if n%2:
  candidates=((s,p) for s in range(n) for p in pairings(tuple(v for v in range(n) if v!=s)))
 else:candidates=((None,p) for p in pairings(tuple(range(n))))
 for singleton,pairs in candidates:
  if all(not(adj[a]>>b&1) for a,b in pairs):
   word=[-1]*n
   for colour,(a,b) in enumerate(pairs):word[a]=word[b]=colour
   if singleton is not None:word[singleton]=len(pairs)
   require(max(word)<4,'palette overflow')
   require(all(word[i]!=word[j] for i in range(n) for j in range(i+1,n) if adj[i]>>j&1),'invalid pair colouring')
   return word
 return None

def clique_masks():
 """U/L labels on all ten K5 edges; unit wedges cannot close with L."""
 edges=list(combinations(range(5),2));good=[];hist={}
 for mask in range(1<<10):
  u={e for k,e in enumerate(edges) if mask>>k&1}
  def unit(a,b):return tuple(sorted((a,b))) in u
  if any(sum(unit(a,b) for a,b in combinations(t,2))==2 for t in combinations(range(5),3)):continue
  if any(all(unit(a,b) for a,b in combinations(t,2)) for t in combinations(range(5),4)):continue
  long=10-len(u);good.append(mask);hist[long]=hist.get(long,0)+1
 require(min(hist)==6,'K5 long-edge threshold')
 return {'masks_examined':1024,'surviving_masks':len(good),'long_edge_histogram':{str(k):hist[k] for k in sorted(hist)},'minimum_long_edges':min(hist),'surviving_masks_sha256':hashlib.sha256((','.join(map(str,good))+'\n').encode()).hexdigest()}

def run():
 out=[]
 for n in range(5,9):
  count=0;coloured=0;excluded=0;receipt=hashlib.sha256();hist={};masks=[]
  for adj in regular_graphs(n,4):
   require(all(a.bit_count()==4 for a in adj),'degree4 enumeration')
   count+=1;word=colour_from_pairs(adj)
   masks.append(sum((1<<k) for k,(i,j) in enumerate(combinations(range(n),2)) if adj[i]>>j&1))
   if word is None:
    require(n==5 and all(adj[i]==((1<<n)-1)^(1<<i) for i in range(n)),'uncoloured non-K5 kernel');excluded+=1
   else:
    coloured+=1;nc=1+max(word);hist[nc]=hist.get(nc,0)+1
   receipt.update((','.join(map(str,adj))+':'+('K5' if word is None else ''.join(map(str,word)))+'\n').encode())
  out.append({'vertices':n,'labelled_four_regular_graphs':count,'positive_four_colourings':coloured,'K5_exceptions':excluded,'used_colours_histogram':{str(k):hist[k] for k in sorted(hist)},'receipt_sha256':receipt.hexdigest(),'graph_set_sha256':hashlib.sha256((','.join(map(str,sorted(masks)))+'\n').encode()).hexdigest()})
 require([r['labelled_four_regular_graphs'] for r in out]==[1,15,465,19355],'regular graph counts')
 return {'K5_geometry':clique_masks(),'finite_kernels':out,'four_module_obstruction':True,'claimed_record_improvement':False}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
