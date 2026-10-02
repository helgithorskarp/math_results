"""Frozen cold replay of whole catalog, independent templates and controls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
from datetime import datetime,timezone

def require(test,message):
    if not test:
        raise ValueError(message)
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--work',type=Path,required=True)
    a=p.parse_args()
    root=Path(__file__).resolve().parent
    expected=json.loads((root/'expected.json').read_text())
    require(expected['frozen_before_cold_replays'] is True,'expected must be pre-existing frozen source')
    certificate=json.loads((root/'certificate.json').read_text())
    require(certificate['row_coefficient']==3 and certificate['maximum_high_hub_marks']==4,
            'exact certificate scope differs')
    require(not a.work.exists(),'choose a fresh empty cold work directory')
    a.work.mkdir(parents=True)
    primary=a.work/'primary'
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
    commands=[('catalog',root/'produce.py',['--work',str(primary)]),
              ('boundaries',root/'boundaries.py',['--catalog',str(primary/'catalog.json'),'--output',str(primary/'boundaries.json')]),
              ('independent',root/'verify.py',['--primary',str(primary),'--output',str(a.work/'independent.json')]),
              ('controls',root/'controls.py',['--primary',str(primary),'--output',str(a.work/'controls.json')])]
    receipts=[];start=time.monotonic()
    for label,script,args in commands:
        for name in ('PAUSED','PAUSED.json'):
            require(not Path('/scratch/research-team-sol61-six-20260929/state',name).exists(),
                    'Standing pause barrier: save work and stop')
        cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(script),*args]
        before=time.monotonic()
        proc=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=10)
        (a.work/(label+'.stdout')).write_text(proc.stdout)
        (a.work/(label+'.stderr')).write_text(proc.stderr)
        receipts.append(dict(label=label,command=cmd,exit_code=proc.returncode,seconds=time.monotonic()-before))
        require(proc.returncode==0,'Incomplete or failed stage: '+label)
    result=dict(independent=json.loads((a.work/'independent.json').read_text()),
                controls=json.loads((a.work/'controls.json').read_text()))
    require(result==expected['mathematical_result'],'whole frozen mathematical RESULT differs')
    raw=json.dumps(result,sort_keys=True,indent=2)+'\n'
    (a.work/'RESULT.json').write_text(raw)
    hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in root.iterdir() if f.is_file()}
    metadata=dict(agent='six-code-3',role='researcher',finished_utc=datetime.now(timezone.utc).isoformat(),
        optimized=bool(sys.flags.optimize),python=sys.version,seconds=time.monotonic()-start,
        peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        receipts=receipts,source_sha256=hashes,threads=1,cpu_intensive_jobs=1,
        guards='10s/subprocess;100000 category states;10s/category branch',
        scope='Unchanged1CPU2GiB',result_sha256=hashlib.sha256(raw.encode()).hexdigest())
    (a.work/'METADATA.json').write_text(json.dumps(metadata,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(status='PASS_COMPLETE_FROZEN_COLD_REPLAY',seconds=metadata['seconds'],
        peak_child_rss_kib=metadata['peak_child_rss_kib'],result_sha256=metadata['result_sha256'],stages=len(receipts))))
if __name__=='__main__':
    main()
