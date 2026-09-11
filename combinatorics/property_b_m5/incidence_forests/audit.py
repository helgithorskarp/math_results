"""Direct-definition controls supplement the proof; they are not peer review."""
from itertools import combinations,product
from random import Random
from core import C,canonical,all_graphs,forest_numerator,incidence_envelope

def masks(n,k):return [sum(1<<i for i in s) for s in combinations(range(n),k)]
def direct_count(n,L,sets,rows):
 return sum(any(f&1 and s&~c==0 for s,(_,f) in zip(sets,rows))
        and any(f&2 and s&c==0 for s,(_,f) in zip(sets,rows)) for c in masks(n,L))
def overlaps(sets):
 edges=[];weights=[]
 for i,j in combinations(range(len(sets)),2):
  w=(sets[i]&sets[j]).bit_count()
  if w:edges.append((i,j));weights.append(w)
 return tuple(edges),tuple(weights)

def audit():
 graph_checks=0
 for n in range(1,6):
  pairs=tuple(combinations(range(n),2));expected=set()
  for bits in range(1<<len(pairs)):
   es=tuple(p for i,p in enumerate(pairs) if bits>>i&1)
   expected.add(canonical(n,es));graph_checks+=1
  actual,_=all_graphs(n,len(pairs));assert expected==set(actual)
 envelope_groups=labeled_families=0
 for n,sizes,flags in [(5,(3,3,2),(1,3,2)),(6,(3,3,3),(3,3,3))]:
  rows=tuple(zip(sizes,flags));maxima={}
  for sets in product(*(masks(n,a) for a in sizes)):
   union=0
   for s in sets:union|=s
   if union!=(1<<n)-1:continue
   labeled_families+=1;key=overlaps(sets);value=direct_count(n,n//2,sets,rows)
   maxima[key]=max(maxima.get(key,-1),value)
  for (edges,weights),wanted in maxima.items():
   actual,count,_=incidence_envelope(n,n//2,rows,edges,weights)
   assert count>0 and actual==wanted
   envelope_groups+=1
 rng=Random(260911);forest_checks=nonzero_corrections=0
 for _ in range(800):
  n=rng.randrange(6,13);L=rng.randrange(1,n);d=rng.randrange(2,8)
  rows=tuple((rng.randrange(1,min(4,n)+1),rng.randrange(4)) for _ in range(d))
  sets=tuple(sum(1<<i for i in rng.sample(range(n),a)) for a,_ in rows)
  edges,weights=overlaps(sets);actual=direct_count(n,L,sets,rows)
  bound=forest_numerator(n,L,rows,edges,weights);assert actual<=bound
  zero=forest_numerator(n,L,rows,edges,[0]*len(edges));assert bound<=zero
  pair_sum=0
  for i,(a,fi) in enumerate(rows):
   for j,(b,fj) in enumerate(rows):
    if fi&1 and fj&2 and sets[i]&sets[j]==0:pair_sum+=C(n-a-b,L-a)
  nonzero_corrections+=bound<pair_sum;forest_checks+=1
 rows=((3,1),)+((4,3),)*6
 sets=(7,120,1920,30720,(3<<15)|(3<<17),(3<<15)|(3<<19),(3<<17)|(3<<19))
 assert tuple(s.bit_count() for s in sets)==tuple(a for a,_ in rows)
 edges,weights=overlaps(sets)
 assert edges==((4,5),(4,6),(5,6)) and weights==(2,2,2)
 direct=direct_count(21,10,sets,rows)
 exact,count,_=incidence_envelope(21,10,rows,edges,weights)
 assert count==1 and direct==exact==49068
 return {'labeled_graphs_checked':graph_checks,'covering_labeled_families_checked':labeled_families,
  'complete_incidence_envelope_groups':envelope_groups,'forest_direct_counts':forest_checks,
  'forest_controls_with_positive_correction':nonzero_corrections,'residual_direct_count':direct,
  'residual_denominator':C(21,10)}
