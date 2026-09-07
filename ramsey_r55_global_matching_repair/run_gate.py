"""One declared complete 21-reference gate; no escalation after node budget."""
import argparse
import hashlib
import json
from pathlib import Path
import time

import produce
import verify


def run(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    source=Path(__file__).with_name('parents.json')
    parents=json.loads(source.read_text())
    if (parents.get('schema') != 1 or parents.get('edge_order') !=
            'combinations(range(43),2), bit k from least significant bit' or len(parents['records'])!=21):
        raise ValueError('parent schema')
    budget=[2_000_000]
    records=[]
    start=time.monotonic()
    words=[]
    for i,parent in enumerate(parents['records']):
        word=int(parent['red_edge_bits_hex'],16)
        words.append(word)
        begin=time.monotonic()
        proof=produce.decide(43,word,5,budget)
        payload=produce.encode(proof)
        filename=f'parent_{i:02}.json'
        (out/filename).write_bytes(payload)
        row={'index':i,'name':parent['name'],'status':proof['status'],
             'discovery_nodes':proof['discovery_nodes'],'proof_sha256':hashlib.sha256(payload).hexdigest(),
             'proof_bytes':len(payload),'proof_file':filename}
        if proof['status']!='UNKNOWN':
            row['independent_check']=verify.check(43,word,proof,5)
        row['elapsed_seconds']=time.monotonic()-begin
        records.append(row)
        print(json.dumps(row,sort_keys=True),flush=True)
        if proof['status']!='UNSAT':
            break
    status='COMPLETE_GLOBAL_MATCHING_FAMILY_EXCLUDED' if len(records)==21 and all(r['status']=='UNSAT' for r in records) else 'TARGET_FOUND' if records[-1]['status']=='SAT' else 'GLOBAL_GATE_UNDECIDED'
    telephone=[1,1]
    for n in range(2,44): telephone.append(telephone[-1]+(n-1)*telephone[-2])
    result={'status':status,'parents_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'reference_records':21,'completed_records':len(records),'distinct_processed_physical_parents':len(set(words)),
            'matching_assignments_per_fixed_parent':telephone[43],
            'node_budget':2_000_000,'discovery_nodes':2_000_000-budget[0],
            'proof_bytes':sum(r['proof_bytes'] for r in records),
            'elapsed_seconds':time.monotonic()-start,'records':records}
    (out/'gate.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2,sort_keys=True),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('fresh_output_directory')
    args=parser.parse_args()
    run(args.fresh_output_directory)
