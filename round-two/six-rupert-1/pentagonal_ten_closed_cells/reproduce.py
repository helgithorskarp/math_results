#!/usr/bin/env python3
"""Fresh single-thread, serial exact replay; each numeric child has <=45s guard."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,time
HERE=Path(__file__).resolve().parent
def require(b,s):
    if not b:raise ValueError(s)
def main(args):
    start=time.monotonic();mode='optimized'if args.optimized else'normal';work=HERE/'.generated'/mode;work.mkdir(exist_ok=True,parents=True)
    config=json.loads((HERE/'configuration.json').read_text());python=[sys.executable]+(['-O']if args.optimized else[]);receipts=[]
    compared=Path(args.compare).parent if args.compare else None
    def same(path):
        if compared:
            old=compared/path.relative_to(work);require(path.read_bytes()==old.read_bytes(),'entire relocated normal/O mathematical record: '+str(path.relative_to(work)))
    def run(file,*options,guard=45):
        begun=time.monotonic();p=subprocess.run(python+[str(HERE/file),*map(str,options)],capture_output=True,text=True,timeout=guard+5)
        entry=dict(stage=file,options=list(map(str,options)),exit_code=p.returncode,wall_seconds=time.monotonic()-begun,stdout=p.stdout.strip(),stderr=p.stderr.strip())
        receipts.append(entry);(work/'receipts.json').write_text(json.dumps(receipts,indent=2,sort_keys=True)+'\n')
        print(json.dumps(dict(stage=file,exit_code=p.returncode,stdout=p.stdout.strip(),stderr=p.stderr.strip())),flush=True)
        require(p.returncode==0,'guarded fresh mathematical child failed; no theorem')
    cache=work/'named_geometry.json'
    if cache.exists():cache.unlink()
    run('local.py','--model-only','--seconds','45','--output',work/'model.json','--geometry-output',cache)
    same(cache);same(work/'model.json')
    for cell in (19,18,16,33):
        where=work/str(cell);where.mkdir(exist_ok=True);cfg=config['cells'][str(cell)]
        run('expand.py','--cell',cell,'--output',where/'forest.json',guard=20);same(where/'forest.json')
        run('local.py','--cell',cell,'--from-fresh-cache',cache,'--seconds','40','--output',where/'local.json','--geometry-output',cache,guard=40);same(where/'local.json')
        run('local_controls.py','--cell',cell,'--work',where,'--seconds','40','--output',where/'local_controls.json',guard=40);same(where/'local_controls.json')
        run('prepare.py','--cell',cell,'--work',where,'--seconds','40',guard=40);same(where/'geometry.json');same(where/'source.json')
        geometry_sha=hashlib.sha256((where/'geometry.json').read_bytes()).hexdigest()
        for i in range(0,cfg['source_leaves'],1000):
            out=where/f'leaves_{i}.json'
            run('verify_shell.py','--geometry',where/'geometry.json','--geometry-sha',geometry_sha,'--forest',where/'forest.json','--start',i,'--count',min(1000,cfg['source_leaves']-i),'--seconds','45','--output',out)
            same(out)
        run('source_controls.py','--cell',cell,'--work',where,'--geometry',where/'geometry.json','--geometry-sha',geometry_sha,'--forest',where/'forest.json','--seconds','40','--output',where/'source_controls.json',guard=40);same(where/'source_controls.json')
    options=['--work',work,'--output',work/'complete.json']
    if args.compare:options+=['--compare',args.compare]
    run('aggregate.py',*options,guard=45)
    print(json.dumps(dict(mode=mode,complete=True,wall_seconds=time.monotonic()-start,threads=1,maximum_cpu_intensive_children=1,guard_max_seconds=45,generated='.generated/'+mode)))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--optimized',action='store_true');p.add_argument('--compare');main(p.parse_args())
