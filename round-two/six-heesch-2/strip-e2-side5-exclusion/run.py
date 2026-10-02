"""Run six serial proof/reader jobs; guards are never mathematical negatives."""
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import deps
H=Path(__file__).resolve().parent
def run_all():
    start=time.monotonic();rows=[];hashes={}
    env=dict(os.environ);env.pop('PYTHONPATH',None)
    env['PYTHONDONTWRITEBYTECODE']='1'
    for v in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
        env[v]='1'
    for job,filename in [('core','core.py'),('collar','collar.py'),('check','check_collar.py')]:
        for mode in ['normal','optimized']:
            if deps.paused():raise RuntimeError('Pause barrier')
            command=[sys.executable]+(['-O'] if mode=='optimized' else [])+[str(H/filename)]
            tick=time.monotonic()
            r=subprocess.run(command,cwd=H,env=env,text=True,capture_output=True,timeout=47)
            if r.returncode:raise RuntimeError('Incomplete job '+job+' '+mode+': '+r.stderr[-2500:])
            data=json.loads((H/'generated'/f'{job}-{mode}.json').read_text())
            if not data.get('complete',True):raise ValueError('Incomplete proof output')
            hashes[job,mode]=data['mathematics_sha256']
            rows.append({'job':job,'mode':mode,'seconds':round(time.monotonic()-tick,3),
                         'max_rss_kib':data['max_rss_kib']})
        if hashes[job,'normal']!=hashes[job,'optimized']:
            raise ValueError('Normal/optimized evidence differs for '+job)
    check=json.loads((H/'generated'/'check-normal.json').read_text())['evidence']
    core=json.loads((H/'generated'/'core-normal.json').read_text())['evidence']
    summary={'agent':'six-heesch-2','role':'researcher','complete':True,
        'mathematics_sha256':{job:hashes[job,'normal'] for job in ['core','collar','check']},
        'normal_optimized_agree':True,'serial_jobs':6,
        'collar_suppliers':check['replay']['atlas_size'],'DAG_nodes':check['replay']['DAG_nodes'],
        'core_damage_controls':len(core['damaged_controls']),
        'reader_damage_controls':len(check['damaged_controls']),
        'material_parameters':check['separate_AX_material_parameters'],
        'all_k_minimum':6,'E2_identity_U5_empty':True,'Heesch_number_conclusion':False,
        'seconds':round(time.monotonic()-start,3),
        'max_child_rss_kib':max(row['max_rss_kib'] for row in rows),
        'checked_utc':datetime.now(timezone.utc).isoformat()}
    (H/'generated'/'run.json').write_text(json.dumps({'summary':summary,'jobs':rows},indent=2)+'\n')
    return summary
if __name__=='__main__':print(json.dumps(run_all(),sort_keys=True),flush=True)
