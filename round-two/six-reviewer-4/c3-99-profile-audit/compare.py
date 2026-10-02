#!/usr/bin/env python3
"""Post-seal comparison with author fixtures; never imported by sealed cores.
Requires unchanged author's reproduced MATHEMATICAL and ordered-degree-domain.
"""
from pathlib import Path
from itertools import product,combinations
from collections import Counter
from math import comb
import argparse,hashlib,json
from core import orbit_edge,need

def main():
 p=argparse.ArgumentParser();p.add_argument('--author-work',type=Path,required=True);args=p.parse_args()
 raw=(args.author_work/'MATHEMATICAL.json').read_bytes();a=json.loads(raw);analytic=a['analytic']
 domains=json.loads((args.author_work/'ordered-degree-domain.json').read_text())
 matched=[];kept=[];hist=Counter();Ws={}
 for ds in product(range(7,11),repeat=7):
  full=[9]+[v for d in ds for v in (d,d,d)]
  if sum(full)!=198:continue
  W=(-6468+120*99-3*sum(d*d for d in full))//2
  matched.append(list(ds));hist[tuple(sorted(ds))]+=1;Ws[tuple(sorted(ds))]=W
  if W>=0:kept.append(list(ds))
 need(domains=={'all':matched,'retained':kept},'entire ordered author domains')
 observed=[]
 for r in analytic['histograms']:
  ds=tuple(sorted(int(d) for d,n in r['free_degree_counts'].items() for _ in range(n)))
  need(ds in hist,'unknown author histogram')
  need(r['a']==ds.count(8) and r['b']==ds.count(7),'histogram keys')
  need(r['ordered_placements']==hist[ds] and r['deficit_weight']==Ws[ds] and r['retained']==(Ws[ds]>=0),'full histogram count/budget/retention')
  need(r['variance']==sum((d-9)**2 for d in [9]+[x for v in ds for x in (v,v,v)]),'actual22 variance')
  observed.append(ds)
 need(len(observed)==len(hist) and len(set(observed))==len(hist),'complete eight histograms')
 for r in analytic['new_profile_root_placements']:
  words=[ds for ds in kept if ds.count(8)==r['a'] and ds.count(7)==r['b']];reasons=Counter();survive=Counter()
  for ds in words:
   DA=sum(ds[:3])*3
   if DA>81:reasons['root_cut']+=1
   elif 165-2*DA>6:reasons['root_budget']+=1
   else:survive[tuple(sorted(ds[:3]))+tuple(sorted(ds[3:]))]+=1
  expect=[{'A':list(k[:3]),'B':list(k[3:]),'ordered_placements':v} for k,v in sorted(survive.items())]
  need(r['ordered_placements']==len(words) and r['rejected']==dict(reasons) and r['survivors']==expect,'whole new-root fields')
 orbits=sorted({orbit_edge(i,j) for i,j in combinations(range(9),2)})
 # Translate physical orbit sets into author's bit convention, bijectively.
 def bit(o):
  i,j=o[0];I,t=divmod(i,3);J,s=divmod(j,3)
  return I if I==J else {(0,1):3,(0,2):6,(1,2):9}[I,J]+(s-t)%3
 positions=[bit(o) for o in orbits];need(sorted(positions)==list(range(12)),'physical word translation bijection')
 parities=[];groups=Counter();cases_seen=set();capacity_checks=0
 for word in range(4096):
  edges={e for k,o in enumerate(orbits) if word>>k&1 for e in o};adj=[set() for _ in range(9)]
  for i,j in edges:adj[i].add(j);adj[j].add(i)
  hd=list(map(len,adj))
  if len(edges)!=12 or max(hd)>3:continue
  groups[tuple(hd[::3])]+=1
  for marks in ((7,7,7,10,10,10,10,10,10),(8,8,8,9,9,9,10,10,10)):
   caps={}
   for u,v in combinations(range(9),2):
    q=len(adj[u]&adj[v]);caps[u,v]=2-q if v in adj[u] else marks[u]+marks[v]-15-q
   match=[r for r in analytic['marked_capacity_cases'] if r['A']==list(marks[::3]) and r['H_orbit_degrees']==hd[::3]]
   need(len(match)==1,'one exact marked capacity record');r=match[0];ranks=(4,4,4,4) if marks[0]==7 else (3,3,5,5)
   overlap=3*sum(comb(s,2) for s in ranks);capacity=sum(caps.values())
   need(r['capacity']==capacity and r['actual_overlap']==overlap and r['slack']==capacity-overlap,'literal full capacity record')
   need(r['B_column_ranks']==list(ranks) and r['root_deficit']==3 and r['total_deficit']==6,'column/rule constants')
   reason='capacity_below_actual_overlap' if capacity<overlap else ('A_pair_slack_plus_root_exceeds_total_budget' if marks[0]==7 else 'all_A_pairs_tight_then_odd_column_parity')
   need(r['reason']==reason,'actual obstruction label');cases_seen.add((tuple(r['A']),tuple(r['H_orbit_degrees'])));capacity_checks+=1
   if marks[0]==8 and hd[::3]==[3,3,2]:
    rs=[4+sum(v for pair,v in caps.items() if u in pair) for u in range(3)]
    translated=sum(1<<positions[k] for k in range(12) if word>>k&1)
    parities.append({'word':translated,'low_Gram_row_sums':rs})
 need(len(cases_seen)==6 and len(analytic['marked_capacity_cases'])==6,'all six complete marked cases')
 need(sorted(parities,key=lambda r:r['word'])==a['literal_H_audit']['whole_parity_records'],'all58 full physical parity rows after relabeling')
 need(a['literal_H_audit']['local_degree_groups']==[{'degrees':list(k),'words':v} for k,v in sorted(groups.items())],'all local groups')
 need(analytic['exceptional_all_nine']=={'A':[9,9,9],'B':[7,9,10,10],'B_column_ranks':[2,4,5,5],'capacity':75,'actual_overlap':81},'exceptional all-nine complete fields')
 pc=[]
 for ell in (0,2):
  for high in range(4-ell):
   pc.append({'low_internal_neighbors':ell,'high_neighbors':high,'pair_capacity_sum':11+ell,'tight_Gram_row_sum':15+ell,'odd_column_required_parity':0})
 need(analytic['low_row_parity_cases']==pc,'all six low-row fields')
 print(json.dumps({'complete':True,'postseal_author_fixture_comparison':True,'author_entire_record_bytes':len(raw),'author_entire_record_sha256':hashlib.sha256(raw).hexdigest(),'whole_ordered_degree_domains_equal':True,'degree_sum_words':len(matched),'retained_words':len(kept),'entire_histogram_fields':len(hist),'entire_new_root_record_fields_equal':True,'literal_marked_capacity_checks':capacity_checks,'whole58_original_parity_records_equal':True,'physical_bit_translation_bijection':True,'source_imported_into_sealed_core':False},sort_keys=True))
if __name__=='__main__':main()
