#!/usr/bin/env python3
"""Regenerate and check the non-four proof outside the repository."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time
from verify import compute, require

def limit():
    resource.setrlimit(resource.RLIMIT_AS,(4<<30,4<<30))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--kissat',type=Path,required=True);ap.add_argument('--drat-trim',type=Path,required=True)
    ap.add_argument('--seconds',type=int,default=120);args=ap.parse_args()
    require(1<=args.seconds<=120,'one bounded native query, at most 120 seconds')
    require(not args.work.exists(),'choose a fresh external work directory')
    args.work.mkdir(parents=True)
    facts,cnf,_=compute();instance=args.work/'core.cnf';instance.write_bytes(cnf)
    proof=args.work/'core.drat';log=args.work/'solver.log';checklog=args.work/'checker.log'
    tic=time.monotonic()
    with log.open('w') as out:
        p=subprocess.run([str(args.kissat.resolve()),f'--time={args.seconds}',str(instance.resolve()),str(proof.resolve())],stdout=out,stderr=subprocess.STDOUT,preexec_fn=limit)
    result=dict(facts=facts,solver_returncode=p.returncode,solver_seconds=time.monotonic()-tic,
                cnf_sha256=sha256(cnf).hexdigest(),non_four_proof_checked=False,status='UNKNOWN')
    if p.returncode==20:
        tic=time.monotonic()
        with checklog.open('w') as out:
            c=subprocess.run([str(args.drat_trim.resolve()),str(instance.resolve()),str(proof.resolve())],stdout=out,stderr=subprocess.STDOUT,preexec_fn=limit)
        require(c.returncode==0 and 's VERIFIED' in checklog.read_text(),'proof rejected')
        result.update(non_four_proof_checked=True,proof_sha256=sha256(proof.read_bytes()).hexdigest(),
                      proof_bytes=proof.stat().st_size,checker_seconds=time.monotonic()-tic,
                      status='530-POINT FIVE-CHROMATIC VERTEX-CRITICAL CORE VERIFIED; CAP MISSED')
    elif p.returncode==10:
        raise RuntimeError('SAT contradicts the recorded non-four result; preserve the native model for investigation')
    (args.work/'result.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
