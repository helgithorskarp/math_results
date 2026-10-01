"""Standard-library exact reproduction and optional bounded fresh proposals."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import codec_controls
import verify


def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--fresh',action='store_true');a=p.parse_args()
    started=time.monotonic();env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    out=verify.verify(a.work);expected=json.loads((verify.HERE/'expected.json').read_text())
    if out!=expected:raise ValueError('Exact result differs from the published expected result')
    python=[str(Path(sys.executable).absolute())]+(['-O'] if sys.flags.optimize else [])
    command=python+[str(verify.HERE/'controls.py'),'--base',str(verify.HERE/'base/phase611.json'),
             '--shared',str(a.work/'shared-expanded.json'),'--packing',str(verify.HERE/'certificates/packing.json'),
             '--trace',str(a.work/'exclusion-expanded.json'),'--output',str(a.work/'mathematical-controls.json')]
    r=subprocess.run(command,check=True,capture_output=True,text=True,env=env)
    controls=json.loads(r.stdout);codec=codec_controls.check()
    summary={'agent':'six-vdw-3','role':'researcher','status':out['status'],'phase':611,'total_lower_bound':396,'total_upper_bound':3302,
             'new_W_bound':False,'python':sys.version.split()[0],'optimized':not __debug__,'seconds':time.monotonic()-started,
             'mathematical_controls':controls,'logical_tuple_controls':codec}
    if a.fresh:
        command=python+[str(verify.HERE/'generate.py'),'--work',str(a.work/'fresh')]
        r=subprocess.run(command,check=True,capture_output=True,text=True,env=env)
        summary['fresh']=json.loads(r.stdout)
    (a.work/'reproduction.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
