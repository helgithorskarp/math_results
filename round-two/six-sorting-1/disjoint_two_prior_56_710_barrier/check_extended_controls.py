"""Six semantic controls, including an actual equality-boundary witness set."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from controls import operations_allow
from inputs import digest, need

ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work'
ENV=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',
         BLIS_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',PYTHONHASHSEED='0')


def transport(record):
    record['finite']['extended_cases_sha256']=digest(record['cases'])
    record['finite_sha256']=digest(record['finite'])


def main():
    operations_allow()
    first,last=map(int,sys.argv[1:3])
    path=WORK/f'extended-{first:05}-{last:05}.json'
    raw=path.read_bytes();proposal=json.loads(raw);changes=[]
    changed=copy.deepcopy(proposal);case=changed['cases'][0];w=case['selected_witnesses'][0]
    w['outer_record'][4]+=1;w['label']+=1
    case['selected_mass']=sum(1<<r['label'] for r in case['selected_witnesses'])
    transport(changed)
    changes.append(('false_original_deletion',changed,'Whole original scalar record differs'))
    changed=copy.deepcopy(proposal);case=changed['cases'][0]
    case['selected_witnesses'].append(copy.deepcopy(case['selected_witnesses'][0]))
    case['selected_mass']=sum(1<<r['label'] for r in case['selected_witnesses'])
    transport(changed)
    changes.append(('duplicate_actual_current_class',changed,'Duplicate current dyadic class'))
    changed=copy.deepcopy(proposal);case=changed['cases'][0];remainder=1<<44;subset=[]
    for w in sorted(case['selected_witnesses'],key=lambda w:-w['label']):
        if (1<<w['label'])<=remainder:subset.append(w);remainder-=1<<w['label']
    need(remainder==0,'No genuine exact-equality subset; do not fabricate a boundary')
    case['selected_witnesses']=subset;case['selected_mass']=1<<44
    transport(changed)
    changes.append(('genuine_equal_mass_not_strict',changed,'Strict extended original inequality fails'))
    records=[]
    for label,changed,reason in changes:
        for optimized in (False,True):
            operations_allow();need(path.read_bytes()==raw,'Original valid proposal was not restored')
            path.write_text(json.dumps(changed,indent=2)+'\n')
            args=[sys.executable]+(['-O'] if optimized else [])+[str(ROOT/'verify_extended.py'),str(first),str(last)]
            start=time.monotonic()
            try:result=subprocess.run(args,env=ENV,capture_output=True,text=True,timeout=55)
            finally:path.write_bytes(raw)
            output=result.stdout+result.stderr
            need(result.returncode!=0 and reason in output,'Semantic damage did not reject for intended reason: '+label)
            records.append({'label':label,'optimized':optimized,'intended_reason':reason,
                            'rejected':True,'seconds':time.monotonic()-start})
            (WORK/('extended-control-'+label+('-O' if optimized else '')+'.log')).write_text(output)
    need(path.read_bytes()==raw,'Valid extended proposal bytes changed')
    finite={'retained_interval':[first,last],
            'records':[{k:v for k,v in r.items() if k!='seconds'} for r in records],
            'all6_semantic_checks_reject':len(records)==6,'entire_transport_hashes_repaired':True,
            'genuine_equality_mass':1<<44,'genuine_equality_selected_originals':len(subset),
            'valid_original_proposal_bytes_preserved':True}
    out={'agent':'six-sorting-1','role':'researcher','status':'COMPLETE_EXTENDED_ORIGINAL_SEMANTIC_BOUNDARY_CONTROLS',
         'finite':finite,'finite_sha256':digest(finite),'timings':records,
         'external_person_review_claimed':False}
    (WORK/f'extended-controls-{first:05}-{last:05}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
