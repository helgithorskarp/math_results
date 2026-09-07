"""Construct and transport the forced vertex packing; no isomorphism claim."""
from itertools import combinations,permutations
from pathlib import Path
import argparse,json
import census,domains,model,verify_target

def monochrome(matrix,vertices,color):return all(matrix[u][v]==color for u,v in combinations(vertices,2))

def greedy_partition(matrix):
 remaining=list(range(43));blocks=[]
 for size,required in [(4,1)]*5+[(4,None)]*2+[(3,None)]*4:
  chosen=None
  for color in ([required] if required is not None else [1,0]):
   chosen=next((list(q) for q in combinations(remaining,size) if monochrome(matrix,q,color)),None)
   if chosen is not None:break
  if chosen is None:raise ValueError('required clique missing; input is not certified good43')
  blocks.append(chosen);remaining=[v for v in remaining if v not in chosen]
 if len(remaining)!=3:raise ValueError('packing remainder')
 return blocks+[remaining]

def normalize(graph,partition=None):
 matrix=verify_target.adjacency(graph)
 blocks=greedy_partition(matrix) if partition is None else partition
 if not isinstance(blocks,list) or len(blocks)!=12 or any(not isinstance(b,list) or len(b)!=(4 if i<7 else 3) for i,b in enumerate(blocks)):raise ValueError('packing sizes')
 flat=[v for block in blocks for v in block]
 if any(type(v) is not int for v in flat) or sorted(flat)!=list(range(43)):raise ValueError('packing vertex partition')
 def classify(block):
  if monochrome(matrix,block,1):return 1
  if monochrome(matrix,block,0):return 0
  raise ValueError('nonmonochromatic forced block')
 four=[(classify(b),sorted(b)) for b in blocks[:7]];three=[(classify(b),sorted(b)) for b in blocks[7:11]]
 r=sum(c for c,b in four);s=sum(c for c,b in three)
 if r<5:raise ValueError('five red four-cliques required')
 four.sort(key=lambda z:(-z[0],z[1]));three.sort(key=lambda z:(-z[0],z[1]))
 last=blocks[-1];t=sum(matrix[u][v] for u,v in combinations(last,2));wanted=(0,1,3,7)[t]
 canonical=min(tuple(order) for order in permutations(last) if sum(matrix[order[u]][order[v]]<<k for k,(u,v) in enumerate(combinations(range(3),2)))==wanted)
 arranged=[b for c,b in four+three]+[list(canonical)];root=arranged[0]
 for j,block in enumerate(arranged[1:],1):
  def signature(v):return sum(matrix[root[i]][v]<<i for i in range(4))
  if j<11 or t in (0,3):arranged[j]=sorted(block,key=lambda v:(-signature(v),v))
  else:
   a,b=(0,1) if t==1 else (1,2)
   if (signature(block[a]),-block[a])<(signature(block[b]),-block[b]):block[a],block[b]=block[b],block[a]
 order=[v for block in arranged for v in block]
 normalized=[[matrix[order[u]][order[v]] for v in range(43)] for u in range(43)]
 packing=model.Packing([r,s,t]);parameters=packing.extract(normalized,False)
 try:packing.check_matrices(parameters['matrices']);holds=True
 except ValueError:holds=False
 result=packing.graph(parameters['matrices'],False)
 return {'parameters':parameters,'new_to_old':order,'graph':result,'pair_domains_hold':holds}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('graph');p.add_argument('--partition');a=p.parse_args()
 result=normalize(json.loads(Path(a.graph).read_text()),json.loads(Path(a.partition).read_text()) if a.partition else None)
 print(json.dumps(result,sort_keys=True))
