"""Six serial guarded source checks; generated receipts only in caller scratch."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--scratch',type=Path,required=True)
    args=ap.parse_args();args.scratch.mkdir(parents=True,exist_ok=True)
    here=Path(__file__).resolve().parent
    manifest=json.loads((here/'manifest.json').read_text())
    for name in ('fixture.json','expected.json','fixture-phases.json'):
        if sha256((here/name).read_bytes()).hexdigest()!=manifest[name+'_sha256']:
            raise ValueError('frozen input hash differs')
    if json.loads((here/'fixture-phases.json').read_text())!=json.loads((here/'fixture.json').read_text())['base_phases']:
        raise ValueError('standalone phases differ from the checked fixture')
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',
             NUMEXPR_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    receipts=[];observed={};start=time.monotonic()
    for script in ('check.py','audit.py','controls.py'):
        for optimized in (False,True):
            cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(here/script)]
            t=time.monotonic()
            p=subprocess.run(cmd,cwd=here,env=env,capture_output=True,text=True,timeout=20)
            label=script+('-O' if optimized else '-normal')
            (args.scratch/(label+'.stdout')).write_text(p.stdout)
            (args.scratch/(label+'.stderr')).write_text(p.stderr)
            if p.returncode:raise RuntimeError(label+' failed: '+p.stderr)
            result=json.loads(p.stdout)
            if script in observed and observed[script]!=result:raise ValueError('normal/O mismatch')
            observed[script]=result
            receipts.append({'script':script,'optimized':optimized,'seconds':round(time.monotonic()-t,6)})
    if observed['check.py']!=observed['audit.py']:raise ValueError('different finite engines disagree')
    record={'agent':'six-covering-3','role':'researcher','status':'ALL_CHECKS_PASS','children':receipts,
            'seconds':round(time.monotonic()-start,6),'max_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'child_guard_seconds':20,'threads':1,'no_parallel_children':True,'python':sys.version.split()[0]}
    (args.scratch/'verification.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps(record,sort_keys=True))


if __name__=='__main__':main()
