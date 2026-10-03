"""Common type18 C5 and weighted-deficit capacity, complete candidate image.

The threshold/injection mechanism is credited prior work9803/9754. Each
actual C row has one isolated deficit2 hub and at least4 LOW-SAT friends.
Its hub support N must be>=5. In that column every C row consumes both
one positive entry and one unit of excess D-N. Thus at most min(N,D-N)
such rows can be allocated there. This is a necessary condition only.
"""
import argparse,hashlib,json
from pathlib import Path
R=Path('round-two/six-code-3');S=R/'scratch';W=Path('.');WS=S
canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def need(x,m):
 if not x:raise ValueError(m)
def certificate(case):
 m=dict(case['population']).get(18,0);N=case['N4'];D=case['carrier']['D4']
 need(all(0<=n<=d for n,d in zip(N,D)),'positive support inside deficit total')
 roles=[a for a,n in enumerate(N) if n>=5];slots=[min(N[a],D[a]-N[a]) if a in roles else 0 for a in range(4)]
 cap=sum(slots);oldcap=sum(N[a] for a in roles)
 return dict(live_case_ordinal=case['live_case_ordinal'],survivor_ordinal=case['survivor_ordinal'],branch=case['branch'],population=case['population'],carrier_index=case['carrier_index'],carrier=case['carrier'],N4=N,type18_multiplicity=m,eligible_hub_roles=roles,C5_positive_entry_capacity=oldcap,weighted_role_capacities=slots,weighted_positive_entry_capacity=cap,gap=m-cap,excluded_by_C5=m>oldcap,excluded_by_weighted_capacity=m>cap)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',default=str(S/'pass23-T0-capacity-producer.json'));args=parser.parse_args();out=Path(args.output);need(not out.exists(),'fresh capacity image')
 livepath=S/'pass23-T0-live-column-cases.json';catpath=WS/'pass23-T0-hub-friend-catalogue.json';basispath=R/'four_hub_p21_endpoint_cut/expected.json'
 data=json.loads(livepath.read_text());scopepath=WS/'pass23-T0-column-scope.json';scope=json.loads(scopepath.read_text())
 need(data['scope_sha256']==hashlib.sha256(scopepath.read_bytes()).hexdigest() and data['catalogue_sha256']==hashlib.sha256(catpath.read_bytes()).hexdigest(),'whole raw scope/catalogue provenance')
 need(data['complete_preliminary_populations']==11077 and data['canonical_carriers']==6 and data['complete_carrier_population_records']==66462,'full T0 necessary carrier image')
 basis=json.loads(basispath.read_text())['types'];r=basis[18];need((r['h'],r['e'],r['k'],r['hub_weight'],r['eligible'],r['q'],r['ss_excess'])==(4,1,1,2,True,0,0),'definition of type18')
 cat=json.loads(catpath.read_text());physical=[r for r in cat['records'] if r['type_id']==18]
 need(physical,'actual physical type18 domain')
 for r in physical:
  high=[a for a,d in enumerate(r['hub_deficits']) if d]
  need(len(high)==1 and r['hub_deficits'][high[0]]==2 and r['eligible_hub_mask']==1<<high[0] and r['low_sat_friend_degrees'][high[0]]>=4,'every actual C5 physical role')
 cases=data['live_cases'];need([c['live_case_ordinal'] for c in cases]==list(range(len(cases))),'complete ordered actual positive choices')
 records=[certificate(c) for c in cases]
 def control(m,N,D):return certificate(dict(live_case_ordinal=0,survivor_ordinal=0,branch=[],population=[[18,m]],carrier_index=0,carrier={'D4':D},N4=N))
 need(not control(5,[5,3,3,3],[10,4,5,5])['excluded_by_weighted_capacity'],'positive equal-capacity control')
 need(not control(4,[5,4,4,4],[10,5,5,5])['excluded_by_weighted_capacity'],'positive spare-capacity control')
 need(control(4,[5,3,3,3],[8,4,5,7])['excluded_by_weighted_capacity'],'negative exact excess-token control')
 result=dict(agent='six-code-3',role='researcher',status='PRIVATE_COMPLETE_T0_COMMON_ROW_CAPACITY_IMAGE_NOT_PACKING_SUFFICIENCY',input_live_cases_sha256=hashlib.sha256(livepath.read_bytes()).hexdigest(),catalogue_sha256=hashlib.sha256(catpath.read_bytes()).hexdigest(),type_basis_sha256=hashlib.sha256(basispath.read_bytes()).hexdigest(),records=records,physical_type18_signatures_checked=len(physical),threshold_N=5,candidate_cases=len(cases),C5_excluded=sum(r['excluded_by_C5'] for r in records),weighted_capacity_excluded=sum(r['excluded_by_weighted_capacity'] for r in records),surviving_cases=sum(not r['excluded_by_weighted_capacity'] for r in records),catalogue_frequency_used_as_global_cap=False,ordinary_bridge_formalized=False,independent_person_review=False,positive_controls=2,negative_controls=1)
 out.write_bytes(canonical(result)+b'\n');print(json.dumps({k:v for k,v in result.items() if k!='records'},sort_keys=True))
if __name__=='__main__':main()
