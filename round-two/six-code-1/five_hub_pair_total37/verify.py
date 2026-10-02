"""Rebuild both complete mathematical records; explicit exceptions survive -O."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import producer
import oracle

HERE=Path(__file__).resolve().parent

def need(ok,message):
    if not ok:
        raise ValueError(message)

def run(first):
    record,pmeta=producer.build()
    other,ometa=oracle.build()
    need(record==other,'complete independent physical/coefficient/cut records differ')
    counts=Counter();vectors=0;T1=0
    for branch in record['branches']:
        for row in branch['rows']:
            reason=row['certificate']['reason']
            need(reason!='OPEN','P36 necessary population not excluded')
            counts[reason]+=1;vectors+=1
            T1+=branch['case']['T']==1
    calibration=record['deficit_calibration']
    max_rows=max(sum(n) for r in calibration for n in r['eligible_counts'])
    need(max_rows==3,'positive quota control and upper3')
    I5=sum(r['coordinates'][9] for r in record['actual_marks'])
    summary=dict(actual_agent='six-code-1',role='researcher',
        status='EXACT_CONDITIONAL_P36_EXCLUSION_ALL_SCALAR_BRANCHES',
        actual_marks=len(record['actual_marks']),actual_I5_marks=I5,
        conservative_marks=len(record['conservative_marks']),types=len(record['types']),
        scalar_cases=len(record['scalar_cases']),necessary_vectors=vectors,T1_vectors=T1,
        rejection_counts=dict(counts),deficit_calibration_rows=len(calibration),
        admissible_deficit_calibration_rows=sum(r['pair_cap_valid'] for r in calibration),
        eligible_count_assignments=sum(len(r['eligible_counts']) for r in calibration),
        max_eligible_rows=max_rows,max_producer_nodes=pmeta['max_states'],
        max_oracle_states=ometa['max_states'],whole_record_sha256=producer.digest(record))
    if not first:
        need(summary==json.loads((HERE/'EXPECTED.json').read_text()),'sealed first record mismatch')
    print(json.dumps(summary,sort_keys=True,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--first-run',action='store_true')
    run(parser.parse_args().first_run)
