#!/usr/bin/env python3
"""six-reviewer-4 independent ordinary-profile and labeled H audit.
Defining proof/counts visible; target source/executable/fixtures unread.
Not an enumeration of22-vertex hosts and not a replay of earlier cohorts.
"""
from itertools import product,combinations,permutations
from collections import Counter
from math import comb
import hashlib,json

def need(ok,message):
 if not ok:raise RuntimeError(message)
def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def orbit_edge(i,j):
 rotate=lambda x:3*(x//3)+(x%3+1)%3
 e=set()
 for _ in range(3):e.add(tuple(sorted((i,j))));i=rotate(i);j=rotate(j)
 return tuple(sorted(e))
def budget(ds):
 full=[9]+[d for v in ds for d in (v,v,v)]
 doubled=-6468+120*99-3*sum(d*d for d in full)
 if sum(full)==198:need(doubled%2==0,'integer full22 budget')
 return doubled//2
def main():
 degree_digest=hashlib.sha256();profiles=Counter();sum_matches=nonnegative=0
 for ds in product(range(7,11),repeat=7):
  match=sum(ds)==63;W=budget(ds)
  keep=match and W>=0;degree_digest.update(canonical([ds,match,keep,W if match else None]))
  if match:sum_matches+=1
  if keep:nonnegative+=1;profiles[tuple(sorted(ds))]+=1
 need(sum_matches==1128 and nonnegative==498 and len(profiles)==5,'full degree coverage; no zero/missing new domain')
 rootcases=[]
 for ds in sorted(profiles):
  W=budget(ds)
  if W!=6:continue
  seen=set()
  for inds in permutations(range(7),3):
   a=tuple(ds[i] for i in inds);b=tuple(ds[i] for i in range(7) if i not in inds)
   if (a,b) in seen:continue
   seen.add((a,b));DA=3*sum(a);Dx=165-2*DA
   if DA<=81 and Dx<=W:
    need(DA==81 and Dx==3,'root cut forced81/3')
    rootcases.append({'A':a,'B':b,'W':W,'overlap':3*sum(comb(d-5,2) for d in b)})
 need(len(rootcases)==10 and {c['overlap'] for c in rootcases}=={72,78,81},'every new ordered root case')
 orbits=sorted({orbit_edge(i,j) for i,j in combinations(range(9),2)})
 need(len(orbits)==12 and all(len(o)==3 for o in orbits),'complete C3 edge-orbits')
 need(set().union(*(set(o) for o in orbits))==set(combinations(range(9),2)),'entire original36 pair partition')
 digest=hashlib.sha256();counts=Counter();parityrows=0;Hwords=0;allH=4096
 for word in range(allH):
  edges={e for k,o in enumerate(orbits) if word>>k&1 for e in o};adj=[set() for _ in range(9)]
  for i,j in edges:adj[i].add(j);adj[j].add(i)
  deg=list(map(len,adj));chosen=len(edges)==12 and max(deg)<=3
  if not chosen:continue
  Hwords+=1;need(sorted(deg[::3])==[2,3,3],'only local orbit degrees233')
  for case in rootcases:
   marks=[case['A'][i//3] for i in range(9)];caps=[];common={}
   for i,j in combinations(range(9),2):
    q=len(adj[i]&adj[j]);common[i,j]=q
    caps.append(2-q if (i,j) in edges else marks[i]+marks[j]-15-q)
   capacity=sum(caps);literalformula=108-12-sum((marks[i]-9)*deg[i]+comb(deg[i],2) for i in range(9))
   need(capacity==literalformula,'full36 pair capacity-sum identity')
   overlap=case['overlap'];A=case['A'];stage=''
   if capacity<overlap:stage='capacity_below_overlap'
   elif 7 in A:
    need(capacity-overlap+3>6,'disjoint root plus A-pair deficits exceed total6');stage='disjoint_deficit_budget'
   else:
    need(capacity==overlap==78,'three-pair equality case');need(all(deg[i]==(2 if marks[i]==10 else 3) for i in range(9)),'forced local degree placement')
    for i in range(9):
     if marks[i]!=8:continue
     ell=len(adj[i]&set(range(3*(i//3),3*(i//3)+3)))
     need(ell in (0,2),'C3 internal triangle/independent')
     rowsum=4+sum(caps[k] for k,(a,b) in enumerate(combinations(range(9),2)) if i in (a,b))
     need(rowsum==15+ell and rowsum%2==1,'literal tight capacity row odd')
     need((marks[i]-1-deg[i])%2==0 and all((d-5)%2==1 for d in case['B']),'odd columns force even row');parityrows+=1
    stage='odd_column_Gram_parity'
   counts[stage]+=1;digest.update(canonical([word,case,capacity,stage]))
 odd_columns=0;odd_row_checks=0
 for size in (3,5):
  for column in combinations(range(9),size):
   s=set(column);odd_columns+=1
   for i in range(9):need(((i in s)*size)%2==(i in s),'literal odd-column contribution parity');odd_row_checks+=1
 need(Hwords==174 and sum(counts.values())==1740 and parityrows==1044,'complete nonempty new-case physical H coverage')
 result={'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','complete':True,'degree_domain_words':4**7,'degree_sum_matches':sum_matches,'nonnegative_budget_words':nonnegative,'entire_degree_decisions_sha256':degree_digest.hexdigest(),'profiles':[{'free_degrees':ds,'ordered_words':n,'W':budget(ds)} for ds,n in sorted(profiles.items())],'all_new_profile_ordered_root_cases':rootcases,'literal_H_domain':allH,'literal_H_words_h12_degree_at_most3':Hwords,'new_profile_H_case_checks':sum(counts.values()),'reasons':dict(counts),'literal_parity_rows':parityrows,'all_new_H_rootcase_records_sha256':digest.hexdigest(),'odd_columns':odd_columns,'odd_column_row_checks':odd_row_checks,'host_enumeration':False,'earlier_cohort_computations_replayed':False}
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
