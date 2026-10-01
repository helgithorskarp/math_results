"""Frozen/optional fresh exact checks, with only serial capped children."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE=Path(__file__).absolute().parent
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[name]='1'

def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--fresh',action='store_true');a=p.parse_args()
    if a.work.exists() and any(a.work.iterdir()):raise ValueError('Use a fresh work directory; preserve failed/incomplete runs')
    a.work.mkdir(parents=True,exist_ok=True);a.work=a.work.absolute();start=time.monotonic();jobs=[]
    py=str(Path(sys.executable).absolute()) # Preserve virtual-environment executable; never resolve its symlink.
    provenance=json.loads((HERE/'provenance.json').read_text())
    for item in provenance['copied_unchanged_files']:
        if hashlib.sha256((HERE/item['path']).read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Changed historical input '+item['path'])
    def run(name,script,args,optimized=False):
        cmd=[py]+(['-O'] if optimized else [])+[str(HERE/script)]+list(map(str,args));begin=time.monotonic()
        try:r=subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=30,env=os.environ.copy())
        except (subprocess.TimeoutExpired,subprocess.CalledProcessError) as e:
            failure={'agent':'six-vdw-3','role':'researcher','job':name,'status':'operational_failure_no_exclusion','seconds':time.monotonic()-begin,'error':str(e),'completed_jobs':jobs}
            (a.work/'failure.json').write_text(json.dumps(failure,indent=2)+'\n');raise
        jobs.append({'name':name,'optimized':optimized,'seconds':time.monotonic()-begin,'summary':json.loads(r.stdout)})
        (a.work/'journal.json').write_text(json.dumps(jobs,indent=2)+'\n');print(json.dumps({'completed':name,'seconds':jobs[-1]['seconds']}),flush=True)
    for optimized,label in ((False,'normal'),(True,'optimized')):
        run('frozen-'+label,'verify.py',['--expected',HERE/'expected.json','--output',a.work/f'frozen-{label}.json'],optimized)
        run('controls-'+label,'controls.py',['--work',a.work/f'controls-{label}'],optimized)
    if a.fresh:
        for root in (605,3405):run(f'generate-{root}','generate.py',['--root',root,'--outdir',a.work/f'fresh/root-{root}'])
        for optimized,label in ((False,'normal'),(True,'optimized')):
            run('fresh-'+label,'verify.py',['--new-root-dir',a.work/'fresh','--output',a.work/f'fresh-{label}.json'],optimized)
        frozen=json.loads((a.work/'frozen-normal.json').read_text());fresh=json.loads((a.work/'fresh-normal.json').read_text())
        if frozen['combined_profile']!=fresh['combined_profile'] or fresh!=json.loads((a.work/'fresh-optimized.json').read_text()):raise ValueError('Fresh exact scope/optimized replay mismatch')
    out={'agent':'six-vdw-3','role':'researcher','completed_at':datetime.now(timezone.utc).isoformat(),'python':sys.version,
         'executable':py,'fresh':a.fresh,'all_jobs_completed':True,'serial_compute_jobs':len(jobs),'seconds':time.monotonic()-start,
         'longest_child_seconds':max(j['seconds'] for j in jobs),'parent_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'maximum_child_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'threads':1,'native_LP_limit_seconds':15,
         'external_child_seconds':30,'no_triple_search_for_new_roots':True,'resource_caps_raised':False,'new_W_bound':False,
         'fresh_coefficient_bytes_required_identical':False,'jobs':jobs}
    (a.work/'reproduction.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='jobs'}),flush=True)

if __name__=='__main__':main()
