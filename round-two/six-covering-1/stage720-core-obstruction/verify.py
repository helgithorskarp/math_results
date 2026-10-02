"""Five serial guarded replays; no solver, network or ledger dependency."""
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent

def main():
    manifest=json.loads((ROOT/'manifest.json').read_text())
    for name,digest in manifest['source_sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise ValueError('source hash differs: '+name)
    env=os.environ.copy()
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):env[k]='1'
    runs=[];start=time.monotonic()
    for args in ([str(ROOT/'check.py')],['-O',str(ROOT/'check.py')],[str(ROOT/'audit.py')],['-O',str(ROOT/'audit.py')],[str(ROOT/'audit.py'),'--sanitizers']):
        tick=time.monotonic();p=subprocess.run([sys.executable,*args],env=env,capture_output=True,text=True,timeout=20)
        if p.returncode or p.stderr:raise ValueError('required replay failed: '+p.stderr)
        runs.append({'arguments':args,'seconds':time.monotonic()-tick,'result':json.loads(p.stdout)})
    print(json.dumps({'status':'ALL5_REQUIRED_REPLAYS_PASSED','runs':runs,'seconds':time.monotonic()-start,
                      'max_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'numeric_threads':1,
                      'one_intensive_job_at_a_time':True,'independent_review':False}))

if __name__=='__main__':main()
