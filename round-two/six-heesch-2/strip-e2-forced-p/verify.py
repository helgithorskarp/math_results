"""Run the generator and assertion-independent reader in both modes."""
import json
import os
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).absolute().parent


def main():
    env=dict(os.environ)
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        env[name]='1'
    for optimized in (False,True):
        prefix=[sys.executable]+(['-O'] if optimized else [])
        for script in ('generate.py','check.py'):
            subprocess.run(prefix+[str(HERE/script)],env=env,check=True,timeout=47)
    for role in ('generator','reader'):
        if role=='generator':paths=[HERE/f'generated/{mode}/generator-summary.json' for mode in ('normal','optimized')]
        else:paths=[HERE/f'generated/reader-{mode}.json' for mode in ('normal','optimized')]
        data=[json.loads(p.read_text()) for p in paths]
        if not all(d['complete'] for d in data) or data[0]['mathematics_sha256']!=data[1]['mathematics_sha256']:
            raise ValueError('Normal/optimized mathematical evidence differs')
        print(json.dumps({'role':role,'normal_optimized_agree':True,
                          'mathematics_sha256':data[0]['mathematics_sha256']}),flush=True)


if __name__=='__main__':main()
