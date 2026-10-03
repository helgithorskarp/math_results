"""Compare two complete actualT0 HH domains before any column output."""
from collections import Counter
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import time

R=Path('round-two/six-code-3');W=Path('.');S=R/'scratch'
def need(test,message):
 if not test:raise ValueError(message)
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
out=S/'pass23-T0-column-scope.json';need(not out.exists(),'fresh frozen actualT0 scope')
source_only_replay=True
def load(name):
 path=S/name
 spec=importlib.util.spec_from_file_location(name[:-3],path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
begin=time.monotonic()
# reproduce.py verifies every source/input hash before and after all stages.
first=load('pass23-T0-N-produce.py');second=load('pass23-T0-N-check.py')
labelled,domain=first.carriers();other_labelled,other=second.carriers()
need(labelled==other_labelled and canonical(domain)==canonical(other),'every complete actualT0 carrier record differs')
need(len({(c['global_HHH_mask'],tuple(c['lambda6'])) for c in domain})==len(domain),'canonical domain duplicate')
need(all(c['T']==0 and c['global_HHH_mask'].bit_count()==0 and c['four_hub_words']==0 and sum(c['lambda6'])==22 and sum(c['D4'])==24 for c in domain),'actualT0 statistics')
need(all(first.new_macro_failure(c)==second.macro_failure(c) for c in domain),'every ordinary macro failure differs')
censuspath=S/'pass23-T0-producer.json';census=json.loads(censuspath.read_text());other_census=json.loads((S/'pass23-T0-polynomial.json').read_text())
need(canonical(census['inventory'])==canonical(other_census['inventory']),'full fresh two-engine census')
supplied=[dict(branch=[b[k] for k in ['Q','T','X','tau']],population=t['population']) for b in census['inventory']['branches'] for t in b['templates'] if not t['failures']]
need(len(census['inventory']['branches'])==84 and sum(len(b['templates']) for b in census['inventory']['branches'])==30944 and len(supplied)==11077,'complete actualT0 scalar scope')
catpath=S/'pass23-T0-hub-friend-catalogue.json';cat=json.loads(catpath.read_text());audit=json.loads((S/'pass23-T0-independent-friend-catalogue.json').read_text())
needed=sorted({tid for r in supplied for tid,count in r['population']})
need(needed==cat['relevant_type_ids'] and len(needed)==46,'all actualT0 physical row types covered')
need(audit['status']=='PRIVATE_COMPLETE_TWO_ENGINE_FRIEND_SIGNATURE_AGREEMENT' and audit['records_sha256']==hashlib.sha256(canonical(cat['records'])).hexdigest(),'all exact physical signature records agree')
need(cat['frequency_caps_global_centers'] is False,'local frequencies cannot cap global multiplicity')
partitions=[[start,min(start+64,len(supplied))] for start in range(0,len(supplied),64)]
need([i for start,stop in partitions for i in range(start,stop)]==list(range(len(supplied))),'partition coverage without gaps or repetitions')
record=dict(agent='six-code-3',role='researcher',status='FROZEN_COMPLETE_TWO_ENGINE_T0_INPUT_SCOPE_NO_COLUMN_OR_PACKING_EXCLUSION',sealed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_parent_commit='265ed7a6abe8a15769322f6c1075e12afa94a0f3',catalogue_sha256=hashlib.sha256(catpath.read_bytes()).hexdigest(),catalogue_records_sha256=audit['records_sha256'],catalogue_signatures=len(cat['records']),catalogue_needed_type_ids=needed,census_sha256=hashlib.sha256(censuspath.read_bytes()).hexdigest(),scalar_branches=84,raw_vectors=30944,preliminary_populations=len(supplied),input_populations_sha256=hashlib.sha256(canonical(supplied)).hexdigest(),labelled_carriers=labelled,canonical_carriers=len(domain),canonical_carriers_sha256=hashlib.sha256(canonical(domain)).hexdigest(),carriers_by_HHH_mask=dict(Counter(c['global_HHH_mask'] for c in domain)),macro_pass_carriers=sum(first.new_macro_failure(c) is None for c in domain),every_carrier_record_matched=True,partitions=partitions,partition_size=64,state_guard_per_population=500000,time_guard_seconds_per_population=20,wrapper_stage_timeout_seconds=60,ordinary_bridges_formalized=False,independent_person_review=False,elapsed_seconds=time.monotonic()-begin)
out.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
(S/'pass23-T0-canonical-carriers.json').write_bytes(canonical(domain)+b'\n')
print(json.dumps({k:v for k,v in record.items() if k not in ['partitions','catalogue_needed_type_ids']},sort_keys=True))
