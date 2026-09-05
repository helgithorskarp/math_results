#!/usr/bin/env python3
"""Generate all four complete certificates with a bounded serial pilot."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time
from engine import HERE,SELECTION,compute,require


def limits():resource.setrlimit(resource.RLIMIT_AS,(4294967296,4294967296))


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--roundingsat',type=Path,required=True);args=ap.parse_args()
    args.work.mkdir(parents=True,exist_ok=False);facts,instances,_=compute()
    require(facts==json.loads((HERE/'expected.json').read_text()),'expected exact facts differ')
    result={'status':'running','cases':[]}
    for q in SELECTION:
        d=args.work/str(q);d.mkdir();(d/'selector.opb').write_bytes(instances[q]);t=time.monotonic()
        cmd=[str(args.roundingsat.resolve()),str((d/'selector.opb').resolve()),'--time-limit=120',
             '--print-sol=1','--proof-log='+str((d/'selector.pb').resolve())]
        with (d/'solver.log').open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,preexec_fn=limits)
        text=(d/'solver.log').read_text();out=dict(q=q,exit_code=r.returncode,wall_seconds=time.monotonic()-t,
            status='UNSAT_PENDING_CHECK' if 's UNSATISFIABLE' in text else 'INCOMPLETE_OR_UNEXPECTED',
            proof_sha256=sha256((d/'selector.pb').read_bytes()).hexdigest())
        result['cases'].append(out);(args.work/'regeneration.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(out),flush=True)
        require(out['status']=='UNSAT_PENDING_CHECK',('bounded regeneration incomplete',q))
    result['status']='COMPLETE_NATIVE_PROOFS_REQUIRE_VERIFICATION'
    (args.work/'regeneration.json').write_text(json.dumps(result,indent=2)+'\n')
