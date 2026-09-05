#!/usr/bin/env python3
"""Reproduce one bounded selector query; no automatic continuation."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time
from verify import compute


def limits():
    resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--kissat',type=Path,required=True);args=ap.parse_args()
    work=args.work.resolve();work.mkdir(parents=True,exist_ok=False)
    facts,cnf,meta=compute()
    (work/'residual.cnf').write_bytes(cnf)
    (work/'residual_instance.json').write_text(json.dumps(meta,indent=2,sort_keys=True)+'\n')
    cmd=[str(args.kissat.resolve()),'--time=300',str(work/'residual.cnf'),str(work/'residual.drat')]
    t=time.monotonic()
    with (work/'solver.log').open('w') as log:
        proc=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,preexec_fn=limits)
    result=dict(command=cmd,exit_code=proc.returncode,wall_seconds=time.monotonic()-t,
                maximum_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                cnf_sha256=sha256(cnf).hexdigest(),proof_bytes=(work/'residual.drat').stat().st_size,
                negative_answer_verified=False)
    if proc.returncode==10:
        model={int(x) for line in (work/'solver.log').read_text().splitlines() if line.startswith('v ')
               for x in line.split()[1:] if x!='0'}
        X={v for i,v in enumerate(meta['free_vertices'],1) if i in model}
        from build import REPO
        old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
        if len(X)>56 or X&set(meta['omitted_vertices']):raise ValueError('invalid selector')
        if not all(X&set(old['family'][i]['D']) for i in meta['hitting_rows']):raise ValueError('unhit row')
        result.update(status='SAT_SELECTOR_CHECKED_NOT_A_GRAPH_CHROMATICITY_RESULT',selector=sorted(X))
    elif proc.returncode==20:result['status']='UNSAT_PENDING_INDEPENDENT_PROOF_CHECK'
    elif proc.returncode==0:result['status']='UNKNOWN'
    else:result['status']='ERROR'
    (work/'result.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
    if result['status']=='ERROR':raise RuntimeError('native query failed')


if __name__=='__main__':main()
