from collections import Counter,defaultdict
from hashlib import sha256
from itertools import permutations
from functools import cache
import json,struct,sys

def cover(groups,inc,libB,libV,progress=False):
 perms=[(0,)+p for p in permutations((1,2,3))]
 choices=[(i,j,k) for i in range(len(libB)) for j in range(len(libV)) for k in range(6)]
 FULL=(1<<len(choices))-1;block=6*len(libV)
 sigB=list(zip(*libB));sigV=list(zip(*libV))
 @cache
 def right_masks(qs,vs):
  out=[0]*4
  for j,(a,b) in enumerate(zip(qs,vs)):
   value=a^b
   for k,p in enumerate(perms):out[p[value]] |=1<<(6*j+k)
  return out
 def mask(bs,qs,vs):
  right=right_masks(qs,vs);bad=0
  for i,c in enumerate(bs):bad |=right[c]<<(i*block)
  return FULL^bad
 partition,coverage=sha256(),sha256();hist=[Counter() for _ in sigV];residual=[0]*len(sigV);top=[];total=0;maximum=0
 for gi,ee in enumerate(sorted(groups.values())):
  partition.update((';'.join(f'{b},{d}' for b,d in ee)+'\n').encode())
  by_anchor=defaultdict(list)
  for b,d in ee:
   for q,v in inc[d]:by_anchor[q].append((b,v))
  for q,qe in sorted(by_anchor.items()):
   hist[q][len(qe)]+=1;total+=1;maximum=max(maximum,len(qe));ok=FULL
   for b,v in qe:
    ok &=mask(sigB[b],sigV[q],sigV[v])
    if not ok:break
   if ok:
    w=(ok&-ok).bit_length()-1;i,j,k=choices[w];pi=perms[k]
    if not all(libB[i][b]!=pi[libV[j][v]^libV[j][q]] for b,v in qe):raise ValueError('invalid selected coloring')
   else:
    w=-1;residual[q]+=1
    top.append({'anchor':q,'ambient_class':gi,'cross_edges':sorted(qe),'ambient_edges':ee})
    top.sort(key=lambda x:(-len(x['cross_edges']),x['anchor'],x['ambient_class']));top=top[:20]
   coverage.update(struct.pack('<IIi',gi,q,w))
  if progress and gi and gi%100000==0:print('projected',gi,'cases',total,'residuals',sum(residual),file=sys.stderr,flush=True)
 return {'ambient_edge_partition_sha256':partition.hexdigest(),'coverage_sha256':coverage.hexdigest(),'anchor_classes_total':total,'maximum_cross_edges':maximum,'uncovered_total':sum(residual),'anchors':[{'anchor':q,'classes':sum(h.values()),'unit_multipliers':2*sum(h.values()),'histogram':dict(sorted(h.items())),'uncovered':residual[q]} for q,h in enumerate(hist)]},top
