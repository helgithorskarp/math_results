"""Exact projection and lazy colour-library coverage; no solver or geometry input."""
from collections import defaultdict,Counter
from hashlib import sha256
from itertools import permutations
import struct
PERMS=[(0,)+p for p in permutations((1,2,3))]
ALLOWED=[[sum(1<<k for k,p in enumerate(PERMS) if a!=p[b]) for b in range(4)] for a in range(4)]

def witness(q,edges,lb,lv):
 for i,cb in enumerate(lb):
  for j,cv in enumerate(lv):
   mask=63;cq=cv[q]
   for b,v in edges:
    mask &= ALLOWED[cb[b]][cv[v]^cq]
    if not mask:break
   if mask:
    k=(mask&-mask).bit_length()-1
    if not all(cb[b]!=PERMS[k][cv[v]^cq] for b,v in edges):raise ValueError('invalid selected witness')
    return (i*len(lv)+j)*6+k
 raise ValueError('uncovered anchor/class case')

def cover(groups,inc,lb,lv):
 partition,coverage=sha256(),sha256();hist=[Counter() for _ in lv[0]];total=0;maximum=0
 for gi,ee in enumerate(sorted(groups.values())):
  partition.update((';'.join(f'{b},{d}' for b,d in ee)+'\n').encode())
  by_anchor=defaultdict(list)
  for b,d in ee:
   for q,v in inc[d]:by_anchor[q].append((b,v))
  for q,qe in sorted(by_anchor.items()):
   w=witness(q,qe,lb,lv);hist[q][len(qe)]+=1;total+=1;maximum=max(maximum,len(qe))
   coverage.update(struct.pack('<IIi',gi,q,w))
 return {'ambient_edge_partition_sha256':partition.hexdigest(),'coverage_sha256':coverage.hexdigest(),'anchor_classes_total':total,'maximum_cross_edges':maximum,'uncovered_total':0,'anchors':[{'anchor':q,'classes':sum(h.values()),'unit_multipliers':2*sum(h.values()),'histogram':dict(sorted(h.items())),'uncovered':0} for q,h in enumerate(hist)]}
