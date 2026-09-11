"""Complete intersection-weight box certification; all arithmetic exact."""
import sys
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations,permutations
sys.path.append(str(Path(__file__).resolve().parents[1]/'incidence_forests'))
from core import C,forest_numerator,independence_tests
from graphs import all_graphs
from realizability import support_fits,matrix_fits
from exact_union import incidence_envelope
@lru_cache(None)
def graphs(d,k):return all_graphs(d,k)[0]

def certify(N,L,rows,target):
 d=len(rows);sizes0=tuple(a for a,f in rows);den=C(N,L);e=sum(sizes0)-N
 removals=[]
 for i,j in combinations(range(d),2):
  a,fi=rows[i];b,fj=rows[j]
  removals.append((C(N-a-b,L-a) if fi&1 and fj&2 else 0)+(C(N-a-b,L-b) if fj&1 and fi&2 else 0))
 removals.sort();base=sum(removals);cut=0
 while F(base-sum(removals[:cut]),den)>=target:
  cut+=1
  assert cut<=14, 'Certificate outside the published finite scope'
 best=base-sum(removals[:cut]);nodes=leaves=pre=gram_rejected=exact_count=0;bad=[]
 gs=graphs(d,cut-1);types=sorted(set(permutations(rows)))
 for gi,edges in enumerate(gs):
  if 3*len(edges)<e:continue
  tests=independence_tests(d,edges)
  for rr in types:
   sizes=tuple(a for a,f in rr)
   if not support_fits(N,sizes,edges):continue
   caps=[min(sizes[i],sizes[j],3) for i,j in edges]
   def rec(lo,hi):
    nonlocal best,nodes,leaves,pre,gram_rejected,exact_count
    nodes+=1
    # Bounds consistency for row-capacity inequalities and incidence excess.
    lo=lo.copy();hi=hi.copy();changed=True
    while changed:
     changed=False
     if sum(hi)<e:return
     for u,ix in tests:
      low=sum(lo[i] for i in ix)
      if low>sizes[u]:return
      for i in ix:
       up=min(hi[i],sizes[u]-low+lo[i])
       if up<hi[i]:hi[i]=up;changed=True
       if hi[i]<lo[i]:return
     for i in range(len(lo)):
      low=max(lo[i],e-sum(hi)+hi[i])
      if low>lo[i]:lo[i]=low;changed=True
      if lo[i]>hi[i]:return
    # Every overlap forest has total weight <= incidence excess.
    parent=list(range(d));tree=0
    def rt(x):
     while parent[x]!=x:x=parent[x]
     return x
    for (i,j),w in sorted(zip(edges,lo),key=lambda z:-z[1]):
     i=rt(i);j=rt(j)
     if i!=j:parent[i]=j;tree+=w
    if tree>e:return
    val=forest_numerator(N,L,rr,edges,lo)
    if F(val,den)<target:
     best=max(best,val);pre+=1;return
    split=max(range(len(lo)),key=lambda i:hi[i]-lo[i]) if lo else None
    if split is None or lo[split]==hi[split]:
     leaves+=1
     if not matrix_fits(N,sizes,edges,lo):gram_rejected+=1;return
     exact,n,cols=incidence_envelope(N,L,rr,edges,lo);exact_count+=1
     if not n:return
     if F(exact,den)>=target:
      bad.append({'rows':rr,'edges':edges,'weights':lo,'columns':cols,'bound':str(F(exact,den))});raise ValueError('realization exceeds threshold')
     best=max(best,exact);return
    for w in range(hi[split],lo[split]-1,-1):
     ll=lo.copy();hh=hi.copy();ll[split]=hh[split]=w;rec(ll,hh)
   try:rec([1]*len(edges),caps)
   except ValueError as exc:
    return {'status':type(exc).__name__,'graph_index':gi,'graph_total':len(gs),'rows':rows,'cut':cut,'nodes':nodes,'leaves':leaves,'exact':exact_count,'gram_rejected':gram_rejected,'bad':bad}
 return {'status':'certified','N':N,'L':L,'rows':rows,'target':str(target),'bound':str(F(best,den)),'cut':cut,'nodes':nodes,'leaves':leaves,'exact':exact_count,'gram_rejected':gram_rejected,'preclosed':pre}
