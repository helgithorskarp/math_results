"""Portable serial source-only normal/optimized mathematical verification."""
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def main():
    root=Path(__file__).resolve().parent
    expected=root/'RESULTS.json'
    baseline=json.loads(expected.read_text()) if expected.exists() else None
    results={};receipts=[]
    env=os.environ.copy()
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS']:
        env[key]='1'
    for optimized in [False,True]:
        command=[sys.executable]+(['-O'] if optimized else [])
        for name,args in [('engine',['engine_controls.py']),('original',['audit.py']),
                          ('stronger',['audit.py','--cut','1399/1000']),('damages',['controls.py'])]:
            begin=time.monotonic()
            p=subprocess.run(command+args,cwd=root,env=env,capture_output=True,text=True,timeout=30)
            if p.returncode:
                raise RuntimeError(name+' mathematical child failed: '+p.stderr)
            record=json.loads(p.stdout)
            if baseline is not None and record!=baseline[name]:
                raise ValueError('whole result differs from compact expected record')
            if name in results and results[name]!=record:
                raise ValueError('whole normal/optimized mathematical record differs')
            results[name]=record
            receipts.append({'name':name,'optimized':optimized,'seconds':time.monotonic()-begin,
                             'whole_bytes_SHA256':hashlib.sha256(p.stdout.encode()).hexdigest(),
                             'peak_cumulative_child_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
    # The output includes all mathematical records, not just matching counts.
    result={'mathematics':results,'resources':{'children':receipts,'threads':1,'serial':True,
            'guard_seconds':30,'python':sys.version.split()[0]}}
    print(json.dumps(result,sort_keys=True,separators=(',',':')))


if __name__=='__main__':
    main()
