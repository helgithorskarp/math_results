#!/usr/bin/env python3
"""Two-worker, fixed-budget experiment with per-core durable outputs."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import time

ROOT=Path(__file__).resolve().parent


def identity(path):
    b=path.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}


def atomic(path,value):
    tmp=path.with_suffix(path.suffix+'.tmp')
    with tmp.open('w') as f:
        f.write(json.dumps(value,indent=2,sort_keys=True)+'\n');f.flush();os.fsync(f.fileno())
    tmp.replace(path)


def main():
    p=argparse.ArgumentParser();p.add_argument('--binary',type=Path,required=True)
    p.add_argument('--work',type=Path,required=True);p.add_argument('--resume',action='store_true')
    a=p.parse_args();w=a.work.resolve();binary=a.binary.resolve()
    if w.is_relative_to(ROOT.parent):raise ValueError('external work required')
    contract={'format':'r55-c3-eleven-structured-experiment-v1','restarts_per_core':4,
              'steps_per_restart':25000,'base_seed':20260906,'check_interval':5000,'workers':2,
              'python':platform.python_version(),'binary':identity(binary),
              'sources':{x.name:identity(x) for x in sorted(ROOT.iterdir()) if x.suffix in ('.py','.cpp','.tsv') or x.name in ('inputs.json','EXPERIMENT.md')}}
    if a.resume:
        if json.loads((w/'contract.json').read_text())!=contract:raise ValueError('changed contract')
    else:
        if w.exists():raise ValueError('fresh work required')
        w.mkdir(parents=True);atomic(w/'contract.json',contract)
    cores=[int(line.split()[0]) for line in (ROOT/'cores.tsv').read_text().splitlines()]
    rows={};start=time.monotonic()
    def job(i,core):
        dst=w/f'core{core}'
        if (dst/'status.json').exists():
            status=json.loads((dst/'status.json').read_text())
            if status.get('complete') or status.get('candidate_target'):
                return core,dict(status=status,retained=True)
        if (w/'STOP').exists():return core,{'status':{'complete':False,'queued_stopped':True}}
        # A failed/interrupted core can be reproduced from its original seed;
        # retain all earlier outputs and make the retry explicit.
        attempt=0
        while dst.exists():
            attempt+=1;dst=w/f'core{core}_retry{attempt}'
        args=[str(binary),str(ROOT/'cores.tsv'),str(dst),str(i),str(i+1),'4','25000','20260906','5000']
        with (w/f'core{core}_attempt{attempt}.log').open('w') as log:
            r=subprocess.run(args,stdout=log,stderr=subprocess.STDOUT)
        if r.returncode!=0:raise RuntimeError(f'core {core}: exit {r.returncode}, see log')
        status=json.loads((dst/'status.json').read_text())
        if status.get('candidate_target'):(w/'STOP').touch()
        return core,dict(status=status,directory=dst.name,attempt=attempt)
    def save():
        atomic(w/'result.json',{'contract':contract,'cores':{str(k):v for k,v in sorted(rows.items())},
          'complete':len(rows)==17 and all(v['status'].get('complete') for v in rows.values()),
          'candidate_target':any(v['status'].get('candidate_target') for v in rows.values()),
          'seconds':round(time.monotonic()-start,6)})
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(job,i,c) for i,c in enumerate(cores)]
        for f in as_completed(futures):
            c,row=f.result();rows[c]=row;save();print(c,row,flush=True)
    save()


if __name__=='__main__':main()
