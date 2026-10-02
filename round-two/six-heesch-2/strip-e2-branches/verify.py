"""Serial normal/optimized proof generation and search-free verification."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE=Path(__file__).absolute().parent
import deps


def require(value,message):
    if not value:raise ValueError(message)


def main():
    start=time.monotonic();expected=json.loads((HERE/'expected.json').read_text())
    for name,digest in expected.get('source_hashes',{}).items():
        require(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,'Source changed: '+name)
    env=dict(os.environ)
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        env[name]='1'
    reports=[]
    for optimized in (False,True):
        mode='optimized' if optimized else 'normal'
        for name in ('finite_collars.py','conditional_collars.py','reader.py'):
            require(not deps.paused(),'Operational pause barrier')
            args=[sys.executable,*(['-O'] if optimized else []),str(HERE/name)]
            run=subprocess.run(args,cwd=HERE,env=env,text=True,capture_output=True,timeout=47)
            require(run.returncode==0,'Proof command failed: '+name+'\n'+run.stdout+'\n'+run.stderr)
            reports.append({'mode':mode,'program':name,'returncode':run.returncode})
    output={}
    for mode in ('normal','optimized'):
        finite=json.loads((HERE/f'generated/finite/summary-{mode}.json').read_text())
        conditional=json.loads((HERE/f'generated/conditional/summary-{mode}.json').read_text())
        reader=json.loads((HERE/f'generated/verified-{mode}.json').read_text())
        require(finite['all_selected_complete'] and reader['complete'],'Incomplete proof')
        output[mode]=[finite['mathematics_sha256'],conditional['mathematics_sha256'],reader['mathematics_sha256']]
    require(output['normal']==output['optimized'],'Normal/optimized disagreement')
    if 'mathematics_sha256' in expected:
        require(output['normal']==expected['mathematics_sha256'],'Changed mathematical output')
    result={'agent':'six-heesch-2','role':'researcher','complete':True,
            'serial_jobs':len(reports),'normal_optimized_agree':True,
            'mathematics_sha256':output['normal'],
            'damaged_controls':18,'uniform_E1_exclusions':6,
            'E2_point44_suppliers_before':8,'E2_point44_suppliers_after':2,
            'scope':'Registered local domains only; neither remaining branch, full E2 inclusion, nor a global Heesch bound is proved',
            'seconds':round(time.monotonic()-start,3)}
    (HERE/'generated/verification-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True),flush=True)


if __name__=='__main__':main()
