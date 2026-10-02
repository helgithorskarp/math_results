#!/usr/bin/env python3
"""Sequential, single-thread source regeneration and exact complete replay."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,time
HERE=Path(__file__).resolve().parent
def main(args):
    begun=time.monotonic();work=HERE/'.generated';work.mkdir(exist_ok=True)
    expected=json.loads((HERE/'expected.json').read_text());mode='optimized'if args.optimized else'normal'
    python=[sys.executable]+(['-O']if args.optimized else[])
    def run(file,*options):
        subprocess.run(python+[str(file),*map(str,options)],check=True)
    # Both guarded stages are mandatory. A failed fresh reconstruction stops
    # this driver before any previous cache or local record can be consumed.
    cache=work/'named_geometry.json'
    if cache.exists():cache.unlink()
    run(HERE/'local.py','--model-only','--seconds','45','--output',work/f'model_{mode}.json','--geometry-output',cache)
    run(HERE/'local.py','--from-fresh-cache',cache,'--seconds','45','--output',work/'local.json')
    run(HERE/'prepare.py','--seconds','40')
    if hashlib.sha256((work/'local.json').read_bytes()).hexdigest()!=expected['local_whole_record_sha256']:raise ValueError('fresh current local proof differs')
    if hashlib.sha256((work/'geometry.json').read_bytes()).hexdigest()!=expected['geometry_sha256']:raise ValueError('fresh geometry record differs')
    run(HERE/'generate.py','--seconds','40','--depth','18','--nodes','10000')
    batches=[]
    for start,count in [(0,740),(740,740)]:
        out=work/f'leaves_{mode}_{start}.json';batches.append(out)
        run(HERE/'verify_shell.py','--geometry-sha',expected['geometry_sha256'],'--start',start,'--count',count,'--seconds','45','--output',out)
    controls=work/f'controls_{mode}.json'
    run(HERE/'controls.py','--geometry-sha',expected['geometry_sha256'],'--output',controls)
    options=[*batches,'--controls',controls,'--local',work/'local.json','--output',work/f'complete_{mode}.json']
    if args.compare:options+=['--compare',args.compare]
    run(HERE/'aggregate.py',*options)
    print(json.dumps(dict(mode=mode,total_elapsed_seconds=time.monotonic()-begun,threads=1,subprocesses='strictly sequential',generated_state='private ignored .generated directory')))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--optimized',action='store_true');p.add_argument('--compare');main(p.parse_args())
