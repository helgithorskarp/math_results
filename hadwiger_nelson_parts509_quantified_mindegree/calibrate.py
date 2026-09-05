#!/usr/bin/env python3
"""Native calibration of changed finite fixtures only; never runs the full family."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time
import encode_degree as enc
import verify_degree as audit


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--solver',type=Path,required=True)
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--seconds',type=int,default=5)
    args=ap.parse_args()
    enc.base.require(args.seconds>0,'positive bound')
    args.work.mkdir(parents=True,exist_ok=True)
    enc.base.require(not (args.work/'result.json').exists(),'fresh work directory required')
    enc.check_inputs()
    expected={c['name']:c['family_truth'] for c in json.loads((enc.HERE/'expected.json').read_text())['abstract_controls']}
    result=dict(status='running changed finite controls',solver_sha256=sha256(args.solver.read_bytes()).hexdigest(),
                per_control_solver_seconds=args.seconds,rows=[])
    started=time.monotonic()
    for case in audit.fixtures():
        raw,meta=enc.encode(**{k:case[k] for k in ['n','edges','cross','patterns','budget']})
        row=dict(name=case['name'],expected=expected[case['name']],qdimacs_sha256=meta['qdimacs_sha256'])
        if meta['qdimacs_sha256']==meta['base_qdimacs_sha256']:
            row['status']='unchanged base fixture; native rerun omitted'
        else:
            path=args.work/(case['name']+'.qdimacs');path.write_bytes(raw)
            command=[str(args.solver.resolve()),'--qdo',f'--max-secs={args.seconds}',str(path.resolve())]
            begin=time.monotonic()
            with (args.work/(case['name']+'.log')).open('w') as f:
                try:rc=subprocess.run(command,stdout=f,stderr=subprocess.STDOUT,timeout=args.seconds+5).returncode
                except subprocess.TimeoutExpired:rc='watchdog_timeout'
            row.update(status='native control completed',returncode=rc,seconds=time.monotonic()-begin,
                       command=command,truth=True if rc==10 else False if rc==20 else None)
            enc.base.require(row['truth'] is None or row['truth']==row['expected'],('native contradiction',case['name']))
        result['rows'].append(row)
        result['total_seconds']=time.monotonic()-started
        (args.work/'result.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    result['status']='changed finite controls completed; full family unstarted'
    result['maximum_child_rss_kib']=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    (args.work/'result.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status=result['status'],native_calls=sum('truth' in r for r in result['rows']),
        skipped=sum('truth' not in r for r in result['rows']),seconds=result['total_seconds'])),flush=True)


if __name__=='__main__':main()
