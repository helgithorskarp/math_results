"""Ordinary isolated-deficit-two row capacity certificates for all29 cases."""
import hashlib
import json
from pathlib import Path

R=Path('round-two/six-code-3');S=R/'scratch';WS=S
def need(test,message):
 if not test:raise ValueError(message)
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def certificate(case):
 m=dict(case['population']).get(18,0);N=case['N4'];roles=[a for a,n in enumerate(N) if n>=5];capacity=sum(N[a] for a in roles)
 return dict(live_case_ordinal=case['live_case_ordinal'],survivor_ordinal=case['survivor_ordinal'],branch=case['branch'],population=case['population'],N4=N,type18_multiplicity=m,eligible_hub_roles=roles,positive_entry_capacity=capacity,gap=m-capacity,excluded=m>capacity)
def main():
 out=S/'pass21-T1-capacity-producer.json';need(not out.exists(),'fresh capacity output')
 seal=json.loads((S/'pass21-T1-capacity-source-preparation.json').read_text());livepath=S/'pass21-T1-live-column-cases.json';catpath=WS/'pass21-T1-hub-friend-catalogue.json';basispath=R/'four_hub_p21_endpoint_cut/expected.json'
 for path,key in [(livepath,'live_cases_sha256'),(catpath,'catalogue_sha256'),(basispath,'type_basis_sha256')]:need(hashlib.sha256(path.read_bytes()).hexdigest()==seal[key],'frozen whole input differs')
 basis=json.loads(basispath.read_text())['types'];row=basis[18]
 need(row['h']==4 and row['e']==1 and row['k']==1 and row['hub_weight']==2 and row['eligible'] is True and row['q']==0 and row['ss_excess']==0,'actual isolated-deficit-two type18 definition')
 cat=json.loads(catpath.read_text());physical=[r for r in cat['records'] if r['type_id']==18];need(physical,'nonempty physical type18 domain')
 for r in physical:
  high=[a for a,d in enumerate(r['hub_deficits']) if d>0]
  need(len(high)==1 and r['hub_deficits'][high[0]]==2 and r['eligible_hub_mask']==1<<high[0],'every type18 physical role has one isolated deficit-two hub')
  need(r['low_sat_friend_degrees'][high[0]]>=4,'seven leave neighbours minus at most three other hubs')
 cases=json.loads(livepath.read_text())['live_cases'];need(len(cases)==29,'all29 necessary coupled support choices')
 records=[certificate(c) for c in cases];need([r['live_case_ordinal'] for r in records]==list(range(29)),'every actual candidate exactly once');need(all(r['excluded'] for r in records),'positive or unexcluded candidate is not nonexistence')
 need(certificate(dict(live_case_ordinal=0,survivor_ordinal=0,branch=[],population=[[18,5]],N4=[5,3,3,3]))['excluded'] is False,'abstract equal-capacity positive allocation control')
 need(certificate(dict(live_case_ordinal=0,survivor_ordinal=0,branch=[],population=[[18,4]],N4=[5,4,4,4]))['excluded'] is False,'abstract spare-capacity positive allocation control')
 result=dict(agent='six-code-3',role='researcher',status='ALL29_T1_COMMON_ROW_CAPACITY_CERTIFICATES_EXCLUDE',input_live_cases_sha256=seal['live_cases_sha256'],records=records,physical_type18_signatures_checked=len(physical),threshold_N=5,all29_excluded=True,catalogue_frequency_used_as_global_cap=False,ordinary_bridge_formalized=False,external_review=False,abstract_positive_controls=2)
 out.write_bytes(canonical(result)+b'\n');print(json.dumps({k:v for k,v in result.items() if k!='records'},sort_keys=True))
if __name__=='__main__':main()
