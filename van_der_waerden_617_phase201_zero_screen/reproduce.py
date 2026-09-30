"""Standard-library replay; optional single-thread numerical re-generation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE=Path(__file__).parent


def need(ok,message):
    if not ok:raise ValueError(message)


def main():
    p=argparse.ArgumentParser();p.add_argument('--fresh-guide',action='store_true')
    p.add_argument('--work',type=Path,default=HERE/'build');p.add_argument('--output',type=Path)
    a=p.parse_args();begin=time.monotonic()
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        sha,name=line.split('  ',1)
        need(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==sha,'Manifest mismatch: '+name)
    env=dict(os.environ)
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):env[k]='1'
    prefix=[sys.executable]+(['-'+'O'*sys.flags.optimize] if sys.flags.optimize else [])
    jobs=[['zero/verify.py','--expected','zero/expected.json'],['zero/controls.py'],
          ['verify.py','--expected','expected.json'],['controls.py']]
    summaries=[]
    for job in jobs:
        r=subprocess.run(prefix+job,cwd=HERE,env=env,text=True,capture_output=True,timeout=30)
        need(r.returncode==0,'Failed exact replay: '+str(job)+'\n'+r.stdout+r.stderr)
        summaries.append({'command':job,'result':json.loads(r.stdout.strip().splitlines()[-1])})
    fresh=None
    if a.fresh_guide:
        a.work.mkdir(parents=True,exist_ok=True)
        target=(a.work/'root1427.json').absolute()
        r=subprocess.run(prefix+['generate.py','--output',str(target)],cwd=HERE,env=env,text=True,capture_output=True,timeout=30)
        need(r.returncode==0,'Failed optional guide\n'+r.stdout+r.stderr)
        guide=json.loads(r.stdout.strip().splitlines()[-1])
        import verify
        checked=verify.check_all(document=json.loads(target.read_text()))
        frozen=json.loads((HERE/'expected.json').read_text())
        fresh={'guide':guide,'exact_result_matches_frozen':checked==frozen,
               'certificate_bytes_match_frozen':target.read_bytes()==(HERE/'root1427.json').read_bytes(),
               'independent_exact_replay_passed':True}
    out={'agent':'six-vdw-3','role':'researcher','success':True,'python_version':sys.version.split()[0],
         'python_optimization':sys.flags.optimize,'steps':summaries,'fresh':fresh,
         'solver_threads':1,'native_solve_time_limit_seconds':15,'one_CPU_intensive_local_job':True,
         'elapsed_seconds':time.monotonic()-begin,'child_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'agent':'six-vdw-3','role':'researcher','success':True,
                      'python_version':out['python_version'],'python_optimization':sys.flags.optimize,
                      'exact_steps':len(summaries),'fresh':fresh,'elapsed_seconds':out['elapsed_seconds'],
                      'child_peak_rss_kib':out['child_peak_rss_kib']}))


if __name__=='__main__':main()
