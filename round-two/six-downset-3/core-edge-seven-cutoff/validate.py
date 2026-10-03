"""Complete source-only exact replay, one serial 60-second child at a time."""
from pathlib import Path
import sourcecheck
HERE=Path(__file__).resolve().parent
SOURCE=sourcecheck.check_bundle(HERE)
import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
import time

PHASES=[('absence',None),('positive',None),('damage',None),('baseline',None),('empty',None)]
PHASES.extend(('literal',q) for q in range(7,28))
NATIVE_THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')


def validate(out):
    out.mkdir(parents=True,exist_ok=True)
    expected=json.loads((HERE/'EXPECTED.json').read_text())
    frozen=expected['phase_records']
    if len(frozen)!=26 or [(x['phase'],x['q']) for x in frozen]!=PHASES:
        raise ValueError('complete deterministic phase coverage changed')
    env=dict(os.environ)
    for name in NATIVE_THREADS:env[name]='1'
    env['PYTHONDONTWRITEBYTECODE']='1'
    receipt={'actual_agent':'six-downset-3','role':'researcher','python':sys.version,
             'all_six_native_thread_variables':1,'one_serial_intensive_child':True,
             'per_child_timeout_seconds':60,'source_gate_before':SOURCE,
             'complete':False,'completed':[],'independent_person_review':False,'formalized':False}
    mathematics=[]
    def save():
        (out/'VALIDATION.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    def pair(label,args,expected_phase=None):
        values=[];runs=[]
        for mode in ('normal','optimized'):
            target=out/(label+'-'+mode+'.json')
            # Remove a previous receipt so a failing child cannot reuse stale output.
            if target.exists():target.unlink()
            command=[sys.executable]+(['-O'] if mode=='optimized' else [])+args+['--out',str(target)]
            start=time.monotonic()
            try:child=subprocess.run(command,cwd=HERE,env=env,capture_output=True,text=True,timeout=60)
            except subprocess.TimeoutExpired:
                receipt['incomplete_operational_limit']={'phase':label,'mode':mode,'timeout_seconds':60,'no_mathematical_absence_conclusion':True}
                save();raise
            if child.returncode:
                receipt['failed_child']={'phase':label,'mode':mode,'exit_code':child.returncode,'stdout':child.stdout,'stderr':child.stderr}
                save();raise ValueError('failed exact verification phase: '+label)
            raw=target.read_bytes();value=json.loads(raw)
            digest=hashlib.sha256(raw).hexdigest()
            if expected_phase and (len(raw)!=expected_phase['whole_record_bytes'] or digest!=expected_phase['whole_record_sha256']):
                receipt['frozen_record_mismatch']={'phase':label,'mode':mode,'bytes':len(raw),'sha256':digest}
                save();raise ValueError('ENTIRE frozen mathematical record changed: '+label)
            values.append(raw)
            runs.append({'mode':mode,'seconds':time.monotonic()-start,'whole_record_bytes':len(raw),
                         'whole_record_sha256':digest,'peak_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
        if values[0]!=values[1]:
            raise ValueError('ENTIRE normal/optimized record mismatch: '+label)
        receipt['completed'].append({'phase':label,'entire_normal_optimized_records_equal':True,'runs':runs})
        save();print(json.dumps({'phase':label,'whole_record_bytes':len(values[0]),'whole_record_sha256':runs[0]['whole_record_sha256'],'seconds':[r['seconds'] for r in runs]}),flush=True)
        return json.loads(values[0])
    save()
    source=pair('source-damage',[str(HERE/'source_damage.py')])
    if source['count']!=14:raise ValueError('incomplete source damage coverage')
    for (phase,q),frozen_phase in zip(PHASES,frozen):
        label=phase if q is None else phase+'-'+str(q)
        args=[str(HERE/'verify.py'),phase]+(['--q',str(q)] if q is not None else [])
        value=pair(label,args,frozen_phase)
        mathematics.append({'phase':phase,'q':q,'record':value})
    raw=(json.dumps(mathematics,sort_keys=True,indent=2)+'\n').encode()
    digest=hashlib.sha256(raw).hexdigest()
    if len(raw)!=expected['complete_math_record_bytes'] or digest!=expected['complete_math_record_sha256']:
        raise ValueError('ENTIRE assembled mathematical record changed')
    final=sourcecheck.check_bundle(HERE)
    if final!=SOURCE:raise ValueError('source closure changed during exact replay')
    (out/'RESULT.json').write_bytes(raw)
    receipt.update(complete=True,phase_count=26,source_damage_phase_count=1,complete_normal_optimized_children=54,
                   complete_math_record_bytes=len(raw),complete_math_record_sha256=digest,
                   source_gate_after=final,semantic_damages_per_mode=11,source_damages_per_mode=14,
                   all_original_nonempty_ordered_pair_checks=sum(x['record'].get('all_ordered_original_nonempty_member_pairs',0) for x in mathematics))
    save();print(json.dumps({k:receipt[k] for k in ('complete','phase_count','complete_normal_optimized_children','complete_math_record_bytes','complete_math_record_sha256','all_original_nonempty_ordered_pair_checks')}))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=HERE/'work');args=ap.parse_args()
    validate(args.out.resolve())
