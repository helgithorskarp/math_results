"""Frozen and optional fresh checks; every compute child is serial and capped."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE=Path(__file__).absolute().parent
for _name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_name]='1'


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--fresh',action='store_true');a=p.parse_args()
    if a.work.exists() and any(a.work.iterdir()):raise ValueError('Use a fresh work directory; failed or incomplete runs are preserved')
    a.work.mkdir(parents=True,exist_ok=True);a.work=a.work.absolute();started=time.monotonic();jobs=[]
    # Keep the virtual-environment executable path. Resolving this symlink
    # could silently switch to a Python without the pinned proposal packages.
    py=str(Path(sys.executable).absolute());provenance=json.loads((HERE/'provenance.json').read_text())
    for item in provenance['copied_unchanged_files']:
        if hashlib.sha256((HERE/item['path']).read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Changed historical proof input '+item['path'])
    def run(name,script,args,optimized=False):
        cmd=[py]+(['-O'] if optimized else [])+[str(HERE/script)]+list(map(str,args));begin=time.monotonic()
        try:r=subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=30,env=os.environ.copy())
        except (subprocess.TimeoutExpired,subprocess.CalledProcessError) as e:
            failure={'agent':'six-vdw-3','role':'researcher','job':name,'status':'operational_failure_no_exclusion','seconds':time.monotonic()-begin,'error':str(e),'completed_jobs':jobs}
            (a.work/'failure.json').write_text(json.dumps(failure,indent=2)+'\n');raise
        summary=json.loads(r.stdout)
        jobs.append({'name':name,'optimized':optimized,'seconds':time.monotonic()-begin,'summary':summary})
        (a.work/'journal.json').write_text(json.dumps(jobs,indent=2)+'\n')
        print(json.dumps({'completed':name,'seconds':jobs[-1]['seconds']}),flush=True)
    for optimized,label in ((False,'normal'),(True,'optimized')):
        run('frozen-'+label,'verify.py',['--expected',HERE/'expected.json','--output',a.work/f'frozen-{label}.json'],optimized)
        run('controls-'+label,'controls.py',['--work',a.work/('controls-'+label)],optimized)
    if a.fresh:
        manifest=json.loads((HERE/'manifest.json').read_text())
        for phase in manifest['phases']:
            for root in sorted(phase['new_roots']):
                s=phase['phase'];run(f'generate-{s}-{root}','generate.py',['--phase',s,'--root',root,'--outdir',a.work/f'fresh/phase-{s}-root-{root}'])
        for optimized,label in ((False,'normal'),(True,'optimized')):
            run('fresh-'+label,'verify.py',['--new-root-dir',a.work/'fresh','--output',a.work/f'fresh-{label}.json'],optimized)
        frozen=json.loads((a.work/'frozen-normal.json').read_text());fresh=json.loads((a.work/'fresh-normal.json').read_text())
        if frozen['combined_profile']!=fresh['combined_profile'] or fresh!=json.loads((a.work/'fresh-optimized.json').read_text()):raise ValueError('Fresh exact scope or optimized replay mismatch')
    result={'agent':'six-vdw-3','role':'researcher','completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'python':sys.version,'executable':py,'fresh':a.fresh,'all_jobs_completed':True,'serial_compute_jobs':len(jobs),
            'seconds':time.monotonic()-started,'largest_child_seconds':max(j['seconds'] for j in jobs),
            'parent_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'maximum_child_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'threads':1,'native_seconds_per_LP':15,'external_child_seconds':30,
            'selection_seconds':8,'selection_candidates':2000000,'maximum_triple_rows':20000,
            'maximum_cut_rounds':4,'resource_caps_raised':False,'new_W_bound':False,
            'fresh_coefficient_bytes_required_identical':False,'jobs':jobs}
    (a.work/'reproduction.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='jobs'}),flush=True)


if __name__=='__main__':main()
