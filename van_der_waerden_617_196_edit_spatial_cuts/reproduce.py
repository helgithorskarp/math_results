"""Optional bounded sequential certificate rediscovery, followed by exact checks.

Ordinary proof checking only needs check_all.py and Python's standard library.
Generated guidance and certificates belong in an explicit local work directory.
"""
import argparse
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import check_all


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--seconds',type=float,default=15)
    p.add_argument('--fresh',action='store_true')
    args=p.parse_args()
    if not 0<args.seconds<=60:raise ValueError('Bounded guidance time')
    args.work.mkdir(parents=True,exist_ok=True)
    root=Path(__file__).resolve().parent
    env=os.environ.copy()
    env.update({k:'1' for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS',
                              'MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']})
    begin=time.monotonic()
    for s in check_all.PHASES:
        cert=args.work/f'phase-{s:03d}.json'
        guid=args.work/f'guidance-{s:03d}.json'
        if args.fresh or not cert.exists():
            cmd=[sys.executable,str(root/'generate.py'),str(s),str(cert),
                 '--seconds',str(args.seconds),'--budget','196','--guidance',str(guid)]
            r=subprocess.run(cmd,capture_output=True,text=True,env=env,
                             timeout=args.seconds+15)
            if r.returncode:raise RuntimeError(r.stderr)
            print(r.stdout.strip(),flush=True)
        r=subprocess.run([sys.executable,str(root/'verify.py'),str(cert),
                          '--output',str(args.work/f'check-{s:03d}.json')],
                         capture_output=True,text=True,env=env,timeout=10)
        if r.returncode:raise RuntimeError(r.stderr)
        print(r.stdout.strip(),flush=True)
        if guid.exists() and json.loads(guid.read_text())['status']!='Optimal':
            raise RuntimeError('Nonoptimal guidance: stop bounded sweep; no mathematical exclusion inferred')
    out=check_all.check_directory(args.work)
    (args.work/'validation.json').write_text(json.dumps(out,sort_keys=True)+'\n')
    run={'agent':'six-vdw-3','role':'researcher','seconds':time.monotonic()-begin,
         'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
         'threads':1,'sequential_math_jobs':True,
         'manifest_sha256':out['canonical_certificate_manifest_sha256'],
         'verified_far_bounds':out['far_bounds_per_reference_color'],
         'solver_trusted':False}
    (args.work/'reproduction.json').write_text(json.dumps(run,indent=2)+'\n')
    print(json.dumps(run),flush=True)


if __name__=='__main__':main()
