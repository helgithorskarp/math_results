#!/usr/bin/env python3
"""Bounded native QBF controls; no full-pool solve or new closure claim."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time
import controls
import encode


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--solver',type=Path,required=True)
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--real-seconds',type=int,default=30)
    args=ap.parse_args()
    encode.require(args.real_seconds>0,'time bound')
    args.work.mkdir(parents=True,exist_ok=True)
    encode.require(not (args.work/'result.json').exists(),'use fresh output directory')
    result=dict(status='bounded controls running',solver_sha256=sha256(args.solver.read_bytes()).hexdigest(),
                real_seconds_limit=args.real_seconds,rows=[])
    started=time.monotonic()

    def save():
        result['seconds']=time.monotonic()-started
        (args.work/'result.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')

    def run(name,instance,budget,expected,seconds,fixed=None):
        raw,meta=encode.encode(**instance,budget=budget,fixed=fixed)
        path=args.work/(name+'.qdimacs')
        path.write_bytes(raw)
        cmd=[str(args.solver.resolve()),'--qdo','--max-secs='+str(seconds),str(path.resolve())]
        begin=time.monotonic()
        with (args.work/(name+'.log')).open('w') as stream:
            try:
                rc=subprocess.run(cmd,stdout=stream,stderr=subprocess.STDOUT,timeout=seconds+5).returncode
            except subprocess.TimeoutExpired:
                rc='watchdog_timeout'
        elapsed=time.monotonic()-begin
        truth=True if rc==10 else False if rc==20 else None
        encode.require(truth is None or truth==expected,('native control contradiction',name,rc))
        result['rows'].append(dict(name=name,expected=expected,returncode=rc,truth=truth,
                                   seconds=elapsed,meta=meta,command=cmd))
        save()
        print(json.dumps(dict(name=name,truth=truth,seconds=elapsed)),flush=True)

    save()
    for c in controls.controls():
        instance={k:c[k] for k in ['n','edges','cross','patterns']}
        run(c['name'],instance,c['budget'],c['expected'],5)
    source,U=encode.pool_input()
    for name,deleted,expected in [('record509',None,True),('delete397',397,False)]:
        indices=[i for i,v in enumerate(U) if v<509 and v!=deleted]
        instance=encode.restrict(source,indices)
        run(name,instance,instance['n'],expected,args.real_seconds,fixed=set(range(instance['n'])))
    result['status']='bounded controls completed; native answers are calibration only'
    save()


if __name__=='__main__':
    main()
