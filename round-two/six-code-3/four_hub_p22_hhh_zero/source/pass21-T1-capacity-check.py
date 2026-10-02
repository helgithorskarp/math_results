"""Literal leave-neighbour audits and independent positive-slot matching."""
import hashlib
import json
from pathlib import Path

R=Path('round-two/six-code-3');S=R/'scratch';WS=S
def need(test,message):
 if not test:raise ValueError(message)
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def matching(multiplicity,roles,N):
 slots=[(a,j) for a in roles for j in range(N[a])];owners={}
 def augment(row,seen):
  for slot in slots:
   if slot in seen:continue
   seen.add(slot)
   if slot not in owners or augment(owners[slot],seen):owners[slot]=row;return True
  return False
 for row in range(multiplicity):augment(row,set())
 return sorted([[row,list(slot)] for slot,row in owners.items()])
def main():
 out=S/'pass21-T1-capacity-independent.json';need(not out.exists(),'fresh independent capacity output')
 seal=json.loads((S/'pass21-T1-capacity-source-preparation.json').read_text());livepath=S/'pass21-T1-live-column-cases.json';catpath=WS/'pass21-T1-hub-friend-catalogue.json';fixturepath=R/'four_hub_p21_endpoint_cut/fixtures.json';firstpath=S/'pass21-T1-capacity-producer.json'
 for path,key in [(livepath,'live_cases_sha256'),(catpath,'catalogue_sha256'),(fixturepath,'fixture_sha256')]:need(hashlib.sha256(path.read_bytes()).hexdigest()==seal[key],'whole frozen physical input')
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
  rep,leave=compiled[fi];deficits=[5-rep[p] for p in roles];high_roles=[a for a,d in enumerate(deficits) if d];need(len(high_roles)==1 and deficits[high_roles[0]]==2 and deficits==r['hub_deficits'],'original literal role deficits')
  a=high_roles[0];point=roles[a];high_points=[p for p in range(17) if rep[p]<5];neighbours=[p for p in range(17) if leave[point]&(1<<p)]
  need(len(high_points)==4 and len(neighbours)==7 and all(rep[p]==5 for p in neighbours),'original isolated HIGH hub has seven LOW neighbours')
  sat_friends=[p for p in neighbours if p not in roles];need(len(sat_friends)>=4 and len(sat_friends)==r['low_sat_friend_degrees'][a],'original saturated friend list and degree')
  role_friends[a].add(len(sat_friends));neighbour_records.append(dict(fixture=fi,hub_roles=roles,positive_role=a,leave_neighbours=neighbours,low_sat_friends=sat_friends))
 need(all(min(values)==4 for values in role_friends),'definition-level minimum4 in every hub role')
 live=json.loads(livepath.read_text())['live_cases'];first=json.loads(firstpath.read_text());need(first['status']=='ALL29_T1_COMMON_ROW_CAPACITY_CERTIFICATES_EXCLUDE' and len(first['records'])==len(live)==29,'complete original29 capacity certificates')
 records=[]
 for case,given in zip(live,first['records']):
  m=next((count for tid,count in case['population'] if tid==18),0);N=case['N4'];allowed=[a for a,values in enumerate(role_friends) if any(L<N[a] for L in values)];assignment=matching(m,allowed,N)
  need(len(assignment)<m,'a complete matching would survive this relaxation')
  common=dict(live_case_ordinal=case['live_case_ordinal'],survivor_ordinal=case['survivor_ordinal'],branch=case['branch'],population=case['population'],N4=N,type18_multiplicity=m,eligible_hub_roles=allowed,positive_entry_capacity=sum(N[a] for a in allowed),gap=m-sum(N[a] for a in allowed),excluded=len(assignment)<m)
  need(canonical(common)==canonical(given),'entire actual capacity record matches independent physical matching')
  records.append(dict(**common,maximum_partial_matching=assignment))
 need(len(matching(5,[0],[5,3,3,3]))==5 and len(matching(4,[0],[5,4,4,4]))==4,'two valid abstract matching controls')
 result=dict(agent='six-code-3',role='researcher',status='ALL29_T1_CAPACITY_CERTIFICATES_INDEPENDENTLY_CHECKED',author_result_sha256=hashlib.sha256(firstpath.read_bytes()).hexdigest(),records=records,all29_excluded=True,original_literal_neighbour_records=neighbour_records,original_literal_neighbour_records_sha256=hashlib.sha256(canonical(neighbour_records)).hexdigest(),original_physical_type18_signatures=len(selected),all_original_role_minima=sorted(min(x) for x in role_friends),ordinary_bridge_formalized=False,external_review=False,abstract_positive_controls=2)
 out.write_bytes(canonical(result)+b'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['records','original_literal_neighbour_records']},sort_keys=True))
if __name__=='__main__':main()
