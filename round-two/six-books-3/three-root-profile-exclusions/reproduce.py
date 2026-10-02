"""Serial reproducible exact source replay;45s guards on each math child."""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--optimized',action='store_true');a=p.parse_args()
    a.work=a.work.resolve();a.work.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy()
    for v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[v]='1'
    python=[sys.executable]+(['-O'] if a.optimized else [])
    results=[]
    for index in (0,1):
        for script in ('derive.py','verify.py'):
            command=python+[str(ROOT/script),'--profile',str(index),'--work',str(a.work/'generated')]
            run=subprocess.run(command,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=45)
            (a.work/f'{index}-{script}.stdout').write_bytes(run.stdout)
            (a.work/f'{index}-{script}.stderr').write_bytes(run.stderr)
            if run.returncode:raise RuntimeError(f'{script},profile{index} failed; no exclusion verdict: '+run.stderr.decode()[:1000])
            results.append({'profile':index,'program':script,'mathematics':json.loads(run.stdout)})
    run=subprocess.run(python+[str(ROOT/'baseline.py')],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=45)
    if run.returncode:raise RuntimeError('Primary baseline failed: '+run.stderr.decode()[:1000])
    results.append({'program':'baseline.py','mathematics':json.loads(run.stdout)})
    print(json.dumps(results,sort_keys=True,separators=(',',':')))
