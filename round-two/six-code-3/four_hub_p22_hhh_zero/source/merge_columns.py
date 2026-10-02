"""Exact interval coverage/integrity and all positive relaxed candidates."""
from collections import Counter
import datetime
import hashlib
import json
from pathlib import Path
import time

R=Path('round-two/six-code-3');W=Path('.');S=R/'scratch';out=R/'scratch/pass21-T1-column-coverage.json';liveout=R/'scratch/pass21-T1-live-column-cases.json'
if out.exists() or liveout.exists():raise ValueError('fresh full coverage summary')
def need(c,m):
 if not c:raise ValueError(m)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def math_record(x):
 if isinstance(x,dict):return {k:math_record(v) for k,v in x.items() if k!='elapsed_seconds'}
 if isinstance(x,list):return [math_record(v) for v in x]
 return x
begin=time.monotonic();scope=json.loads((S/'pass21-T1-column-scope.json').read_text());progress=json.loads((S/'pass21-T1-column-progress.json').read_text())
need([r['interval'] for r in progress['complete_intervals']]==scope['partitions'],'all28 intended intervals ordered without gaps or repeats')
author_hash=hashlib.sha256();checker_hash=hashlib.sha256();ordinals=[];positive_populations=[];live=[];counts=Counter();indexfiles=[]
for entry in progress['complete_intervals']:
 firstpath=W/entry['author'];secondpath=W/entry['checker'];first=json.loads(firstpath.read_text());second=json.loads(secondpath.read_text())
 need(hashlib.sha256(firstpath.read_bytes()).hexdigest()==entry['author_sha256']==second['author_result_sha256'],'raw author provenance checked before mathematical normalization')
 need(hashlib.sha256(secondpath.read_bytes()).hexdigest()==entry['checker_sha256'],'raw independent provenance')
 need(first['status']=='PRIVATE_COMPLETE_JOINT_N_SUPPLIED_INTERVAL' and second['status']=='PRIVATE_COMPLETE_TWO_ALGORITHM_JOINT_N_INTERVAL','complete intervals only')
 need(first['checked_interval']==second['checked_interval']==entry['interval'],'exact declared interval')
 start,stop=entry['interval'];need(len(first['records'])==len(second['records'])==stop-start,'exact interval size')
 need(hashlib.sha256(canonical(first['canonical_carriers'])).hexdigest()==scope['canonical_carriers_sha256'],'whole ordered actualT1 HH carrier domain')
 for given,checked,i in zip(first['records'],second['records'],range(start,stop)):
  need(given['survivor_ordinal']==checked['survivor_ordinal']==i and given['branch']==checked['branch'],'exact global ordinal and branch')
  need(given['status']=='COMPLETE_SUPPLIED_POPULATION_JOINT_N_RELAXATION' and checked['status']=='COMPLETE' and checked['all_carrier_records_match'],'every original carrier record independently compared')
  need(given['surviving_carriers']==checked['surviving_carriers'] and given['coupled_support_tuples']==checked['coupled_support_tuples'],'positive candidate agreement')
  need(len(given['carrier_results'])==scope['canonical_carriers'],'every carrier inspected')
  ordinals.append(i);author_hash.update(canonical(math_record(given))+b'\n');checker_hash.update(canonical(math_record(checked))+b'\n');counts.update(given['failure_counts'])
  if given['surviving_carriers']:positive_populations.append(dict(survivor_ordinal=i,branch=given['branch'],population=given['population'],surviving_carriers=given['surviving_carriers'],coupled_support_tuples=given['coupled_support_tuples']))
  for carrier in given['carrier_results']:
   for N in carrier['coupled_N4']:
    c=first['canonical_carriers'][carrier['carrier_index']]
    live.append(dict(live_case_ordinal=len(live),survivor_ordinal=i,branch=given['branch'],population=given['population'],carrier_index=carrier['carrier_index'],carrier=c,N4=N))
 indexfiles.append(dict(interval=entry['interval'],author=str(firstpath.relative_to(R)),checker=str(secondpath.relative_to(R)),author_sha256=entry['author_sha256'],checker_sha256=entry['checker_sha256']))
need(ordinals==list(range(1787)),'whole1787 preliminary populations exactly once')
need(len(live)==sum(r['coupled_support_tuples'] for r in positive_populations),'all positive coupled tuples')
payload=dict(agent='six-code-3',role='researcher',status='COMPLETE_T1_JOINT_N_RELAXATION_POSITIVE_CASES_NOT_PACKINGS',source_parent_commit='cd64520ea2aa6f16e31d536bf0605486f5778b8d',scope_sha256=hashlib.sha256((S/'pass21-T1-column-scope.json').read_bytes()).hexdigest(),catalogue_sha256=scope['catalogue_sha256'],complete_preliminary_populations=1787,canonical_carriers=scope['canonical_carriers'],complete_carrier_population_records=1787*scope['canonical_carriers'],live_cases=live)
liveout.write_bytes(canonical(payload)+b'\n')
record=dict(agent='six-code-3',role='researcher',status='COMPLETE_TWO_ENGINE_T1_JOINT_N_RELAXATION_WITH_POSITIVE_CANDIDATES',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),preliminary_populations=1787,canonical_carriers=scope['canonical_carriers'],carrier_population_records=1787*scope['canonical_carriers'],surviving_populations=len(positive_populations),coupled_support_tuples=len(live),positive_populations=positive_populations,all28_intervals_exactly_once=True,all325234_actual_carrier_records_independently_compared=True,author_ordered_mathematical_records_sha256=author_hash.hexdigest(),independent_ordered_mathematical_records_sha256=checker_hash.hexdigest(),failure_counts=dict(counts),live_cases_file=str(liveout),live_cases_sha256=hashlib.sha256(liveout.read_bytes()).hexdigest(),interval_artifacts=indexfiles,ordinary_bridges_formalized=False,independent_person_review=False,packing_realization_claimed=False,elapsed_seconds=time.monotonic()-begin)
out.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in record.items() if k not in ['interval_artifacts']},sort_keys=True))
