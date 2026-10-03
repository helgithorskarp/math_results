"""Original literal C5 neighbours and independent weighted positive-slot matching.

Credits the literal-check mechanism in published9803. Author and checker
are by six-code-3, not an external-person review. The same complete
T0 candidates survive unless a necessary weighted capacity fails.
"""
import argparse,hashlib,json
from pathlib import Path
R=Path('round-two/six-code-3');S=R/'scratch';W=Path('.');WS=S
canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def need(x,m):
 if not x:raise ValueError(m)
def matching(multiplicity,roles,N,D):
 slots=[(a,j) for a in roles for j in range(min(N[a],D[a]-N[a]))];owners={}
 def augment(row,seen):
  for slot in slots:
   if slot in seen:continue
   seen.add(slot)
   if slot not in owners or augment(owners[slot],seen):owners[slot]=row;return True
  return False
 for row in range(multiplicity):augment(row,set())
 return sorted([[row,list(slot)] for slot,row in owners.items()])
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--author',default=str(S/'pass23-T0-capacity-producer.json'));parser.add_argument('--output',default=str(S/'pass23-T0-capacity-independent.json'));args=parser.parse_args();out=Path(args.output);need(not out.exists(),'fresh independent capacity image')
 livepath=S/'pass23-T0-live-column-cases.json';catpath=WS/'pass23-T0-hub-friend-catalogue.json';fixturepath=R/'four_hub_p21_endpoint_cut/fixtures.json';firstpath=Path(args.author)
 first=json.loads(firstpath.read_text());need(first['status']=='PRIVATE_COMPLETE_T0_COMMON_ROW_CAPACITY_IMAGE_NOT_PACKING_SUFFICIENCY','author entire image complete')
 need(first['input_live_cases_sha256']==hashlib.sha256(livepath.read_bytes()).hexdigest() and first['catalogue_sha256']==hashlib.sha256(catpath.read_bytes()).hexdigest(),'entire raw author input provenance')
 need(hashlib.sha256(fixturepath.read_bytes()).hexdigest()=='c188200792c201bdb44ea1667a8a70255c4e40f04fee6c334c98ecfa650113e7','original credited fixtures')
 fixtures=json.loads(fixturepath.read_text())['stars'];catalogue=json.loads(catpath.read_text())['records'];selected=[r for r in catalogue if r['type_id']==18];compiled={};neighbour_records=[];role_friends=[set() for _ in range(4)]
 for r in selected:
  fi=r['witness']['fixture'];roles=r['witness']['hub_roles']
  if fi not in compiled:
   masks=[sum(1<<p for p in word) for word in fixtures[fi]];rep=[sum(bool(mask&(1<<p)) for mask in masks) for p in range(17)];leave=[]
   for p in range(17):
    covered=0
    for mask in masks:
     if mask&(1<<p):covered|=mask^(1<<p)
    leave.append(((1<<17)-1)^(1<<p)^covered)
   compiled[fi]=(rep,leave)
  rep,leave=compiled[fi];deficits=[5-rep[p] for p in roles];high_roles=[a for a,d in enumerate(deficits) if d];need(len(high_roles)==1 and deficits[high_roles[0]]==2 and deficits==r['hub_deficits'],'original actual C role deficits')
  a=high_roles[0];point=roles[a];high_points=[p for p in range(17) if rep[p]<5];neighbours=[p for p in range(17) if leave[point]&(1<<p)]
  need(len(high_points)==4 and len(neighbours)==7 and all(rep[p]==5 for p in neighbours),'original isolated HIGH hub seven LOW neighbours')
  sat_friends=[p for p in neighbours if p not in roles];need(len(sat_friends)>=4 and len(sat_friends)==r['low_sat_friend_degrees'][a],'original actual LOW-SAT friend list')
  role_friends[a].add(len(sat_friends));neighbour_records.append(dict(fixture=fi,hub_roles=roles,positive_role=a,leave_neighbours=neighbours,low_sat_friends=sat_friends))
 need(selected and all(min(x)==4 for x in role_friends),'literal minimum4 in every role')
 data=json.loads(livepath.read_text());live=data['live_cases'];need(len(first['records'])==len(live) and data['complete_carrier_population_records']==66462,'entire T0 input domain')
 records=[]
 for i,(case,given) in enumerate(zip(live,first['records'])):
  need(case['live_case_ordinal']==i,'whole original candidate order')
  m=next((c for tid,c in case['population'] if tid==18),0);N=case['N4'];D=case['carrier']['D4'];need(all(0<=n<=d for n,d in zip(N,D)),'exact support/excess bounds')
  allowed=[a for a,values in enumerate(role_friends) if any(L<N[a] for L in values)];assignment=matching(m,allowed,N,D);slots=[min(N[a],D[a]-N[a]) if a in allowed else 0 for a in range(4)]
  common=dict(live_case_ordinal=i,survivor_ordinal=case['survivor_ordinal'],branch=case['branch'],population=case['population'],carrier_index=case['carrier_index'],carrier=case['carrier'],N4=N,type18_multiplicity=m,eligible_hub_roles=allowed,C5_positive_entry_capacity=sum(N[a] for a in allowed),weighted_role_capacities=slots,weighted_positive_entry_capacity=sum(slots),gap=m-sum(slots),excluded_by_C5=m>sum(N[a] for a in allowed),excluded_by_weighted_capacity=len(assignment)<m)
  need(canonical(common)==canonical(given),'all original fields/weighted capacity match independent literal matching')
  records.append(dict(**common,maximum_partial_matching=assignment))
 need(len(matching(5,[0],[5,3,3,3],[10,4,5,5]))==5 and len(matching(4,[0],[5,4,4,4],[10,5,5,5]))==4,'two valid matching controls')
 need(len(matching(4,[0],[5,3,3,3],[8,4,5,7]))==3,'negative excess-token matching control')
 result=dict(agent='six-code-3',role='researcher',status='PRIVATE_COMPLETE_T0_CAPACITY_IMAGE_INDEPENDENTLY_COMPARED',author_result_sha256=hashlib.sha256(firstpath.read_bytes()).hexdigest(),input_live_cases_sha256=hashlib.sha256(livepath.read_bytes()).hexdigest(),records=records,all_actual_capacity_records_match=True,candidate_cases=len(live),excluded=sum(r['excluded_by_weighted_capacity'] for r in records),surviving_cases=sum(not r['excluded_by_weighted_capacity'] for r in records),original_literal_neighbour_records=neighbour_records,original_literal_neighbour_records_sha256=hashlib.sha256(canonical(neighbour_records)).hexdigest(),original_physical_type18_signatures=len(selected),all_original_role_minima=sorted(min(x) for x in role_friends),ordinary_bridge_formalized=False,independent_person_review=False,positive_controls=2,negative_controls=1)
 out.write_bytes(canonical(result)+b'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('records','original_literal_neighbour_records')},sort_keys=True))
if __name__=='__main__':main()
