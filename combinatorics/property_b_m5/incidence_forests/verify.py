"""Complete finite certification used in the proof of m(5) >= 34."""
import json,sys
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations,permutations,product
from pathlib import Path
from core import C,all_graphs,forest_numerator,independence_tests,feasible,incidence_envelope
ROOT=Path(__file__).resolve().parent
sys.path.append(str(ROOT.parent/'link_envelopes'))
from forest import tail

@lru_cache(None)
def graphs(d,max_edges):return all_graphs(d,max_edges)

def certify(N,L,rows,target,name):
 d=len(rows);den=C(N,L);excess=sum(a for a,_ in rows)-N
 # In these applications every pair intersection is at most three.
 assert all(a in (3,4) for a,_ in rows) and sum(a==3 for a,_ in rows)<=1
 removals=[]
 for i,j in combinations(range(d),2):
  a,fi=rows[i];b,fj=rows[j];value=0
  if fi&1 and fj&2:value+=C(N-a-b,L-a)
  if fj&1 and fi&2:value+=C(N-a-b,L-b)
  removals.append(value)
 removals.sort();base=sum(removals);cut=0
 while F(base-sum(removals[:cut]),den)>=target:
  cut+=1;assert cut<=len(removals)
 max_num=base-sum(removals[:cut])
 gs,level_counts=graphs(d,cut-1)
 row_types=tuple(sorted(set(permutations(rows))))
 preclosed=weighted=0;residuals=[]
 for edges in gs:
  if 3*len(edges)<excess:continue
  tests=independence_tests(d,edges)
  for rr in row_types:
   value=forest_numerator(N,L,rr,edges,[0]*len(edges))
   if F(value,den)<target:
    preclosed+=1;max_num=max(max_num,value);continue
   ranges=[range(1,min(rr[i][0],rr[j][0],3)+1) for i,j in edges]
   for weights in product(*ranges):
    if not feasible(rr,weights,excess,tests):continue
    weighted+=1;value=forest_numerator(N,L,rr,edges,weights)
    if F(value,den)>=target:
     exact,count,columns=incidence_envelope(N,L,rr,edges,weights)
     residuals.append({'rows':rr,'edges':edges,'weights':weights,
       'forest_bound':str(F(value,den)),'incidence_types':count,
       'exact_bound':None if not count else str(F(exact,den)),'columns':columns})
     if not count:continue
     value=exact
    assert F(value,den)<target,(name,rr,edges,weights,value,target)
    max_num=max(max_num,value)
 return {'name':name,'N':N,'L':L,'rows':rows,'target':str(target),'excess':excess,
  'dense_cutoff':cut,'graph_level_counts':level_counts,'row_assignments_per_graph':len(row_types),
  'preclosed_graph_assignments':preclosed,'weighted_matrices_checked':weighted,
  'maximum_certified_bound':str(F(max_num,den)),'residuals':residuals}

def theorem_cases():
 results=[]
 for v,d in [(20,7),(20,8),(21,7)]:
  N,L=v-1,(v-1)//2;tt=tail(N,L,5,33-d)
  result=certify(N,L,((4,3),)*d,1-tt,f'v{v}_degree{d}')
  result['tail_bound']=str(tt)
  result['whole_failure_bound']=str(tt+F(result['maximum_certified_bound']))
  assert F(result['whole_failure_bound'])<1
  results.append(result)
 for v in (22,23):
  N,L=v-2,(v-2)//2;tt=tail(N,L,5,20);pair=[]
  for flag in (1,2):
   result=certify(N,L,((3,flag),)+((4,3),)*6,(1-tt)/2,f'v{v}_degree7_pair1_flag{flag}')
   results.append(result);pair.append(F(result['maximum_certified_bound']))
  results[-1]['tail_bound']=str(tt)
  results[-1]['whole_failure_bound']=str(tt+sum(pair))
  assert tt+sum(pair)<1
  low_vertices=v-(165-7*v);repeated_neighbors=28-(v-1)
  assert low_vertices-1>repeated_neighbors
 return results

def main():
 assert __debug__,'Run without -O: assertions are part of certification.'
 from audit import audit
 result={'claim':'Every finite simple 5-uniform hypergraph with at most 33 edges is two-colorable; m(5)>=34.',
         'cases':theorem_cases(),'controls':audit()}
 encoded=json.dumps(result,indent=2,sort_keys=True)+'\n'
 if sys.argv[1:]==['--generate']:print(encoded,end='')
 else:
  assert not sys.argv[1:]
  assert json.loads(encoded)==json.loads((ROOT/'expected.json').read_text())
  print(encoded,end='')
if __name__=='__main__':main()
