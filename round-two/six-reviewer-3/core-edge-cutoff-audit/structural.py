"""Late independent six-edge classification, prior9735 credit; no author imports."""
from fractions import Fraction as F
from itertools import combinations
import json

def need(ok,label):
 if not ok:raise ValueError(label)
def run():
 vertices=list(range(1,8));edges=[(a,b) for a,b in combinations(vertices,2) if not a&b];need(len(edges)==6,'every disjoint plain-core edge')
 star={a:int(bool(a&1)) for a in vertices};columns=[]
 for a,b in edges:columns.append([star[b] if v==a else star[a] if v==b else 0 for v in vertices])
 equations=[[F(c[i]) for c in columns] for i in range(7)];rref=[r[:] for r in equations];piv=[];r=0
 for j in range(6):
  p=next((i for i in range(r,7) if rref[i][j]),None)
  if p is None:continue
  rref[r],rref[p]=rref[p],rref[r];d=rref[r][j];rref[r]=[x/d for x in rref[r]]
  for i in range(7):
   if i!=r:
    d=rref[i][j];rref[i]=[x-d*y for x,y in zip(rref[i],rref[r])]
  piv.append(j);r+=1
 need(r==3,'rank three original star constraints, complete three-dimensional kernel')
 bases=[]
 for prescribed in [{(1,2):1,(2,5):-1},{(1,4):1,(3,4):-1},{(2,4):1}]:
  v=[prescribed.get(e,0) for e in edges];need(all(sum(a*b for a,b in zip(row,v))==0 for row in equations),'entire prescribed core trade star action');bases.append(v)
 # Explicit free coefficient positions separate the three displayed generators.
 need([[bases[j][edges.index(e)] for j in range(3)] for e in [(1,2),(1,4),(2,4)]]==[[1,0,0],[0,1,0],[0,0,1]],'three independent basis coordinate columns')
 rows={v:0 for v in vertices}
 for a,b in [(1,2),(2,5),(1,4),(3,4),(2,4)]:rows[a]+=1;rows[b]+=1
 need(max(rows.values())==3,'whole combined absolute correction row bound')
 return {'all_plain_core_disjoint_edges':[list(e) for e in edges],'whole_star_constraint_matrix':[[str(v) for v in row] for row in equations],'whole_RREF':[[str(v) for v in row] for row in rref],'rank':r,'complete_kernel_dimension':6-r,'basis':bases,'absolute_combined_trade_row_counts':rows,'credited_prior':'9735 complete plain-core classification','late_addendum_not_part_of_first_sealed_core':True}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
