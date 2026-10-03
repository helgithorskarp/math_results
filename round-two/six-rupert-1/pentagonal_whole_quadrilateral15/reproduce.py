#!/usr/bin/env python3
"""Fresh serial replay: one numeric child, one thread, existing <=45s guards."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
            'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,time
HERE=Path(__file__).resolve().parent
def require(value,message):
    if not value:raise ValueError(message)
def main(args):
    begun=time.monotonic();mode='optimized' if args.optimized else 'normal'
    work=HERE/'.generated'/mode;work.mkdir(parents=True,exist_ok=True)
    cfg=json.loads((HERE/'configuration.json').read_text())['cells']['15']
    python=[sys.executable]+(['-O'] if args.optimized else [])
    comparison=Path(args.compare).resolve().parent if args.compare else None
    receipts=[];paired=[]
    def same(path):
        if comparison:
            old=comparison/path.relative_to(work)
            require(path.read_bytes()==old.read_bytes(),
                    'entire normal/optimized mathematical record: '+str(path.relative_to(work)))
            paired.append(str(path.relative_to(work)))
    def run(filename,*options,guard):
        start=time.monotonic()
        row=dict(stage=filename,guard_seconds=guard,maximum_cpu_intensive_children=1)
        try:
            p=subprocess.run(python+[str(HERE/filename),*map(str,options)],
                             capture_output=True,text=True,timeout=guard+3)
            row.update(exit_code=p.returncode,stdout=p.stdout.strip(),stderr=p.stderr.strip(),
                       status='CHILD_COMPLETED' if p.returncode==0 else 'CHILD_FAILED_NO_THEOREM')
        except subprocess.TimeoutExpired:
            row.update(exit_code=None,status='WALL_GUARD_STOP_NO_MATHEMATICAL_NONEXISTENCE')
        row['wall_seconds']=time.monotonic()-start;receipts.append(row)
        (work/'receipts.json').write_text(json.dumps(receipts,indent=2,sort_keys=True)+'\n')
        print(json.dumps(row),flush=True)
        require(row['status']=='CHILD_COMPLETED','guarded child incomplete; no complete certificate')
    cache=work/'named_geometry.json'
    if cache.exists():cache.unlink()
    run('local.py','--model-only','--seconds',45,'--output',work/'model.json',
        '--geometry-output',cache,guard=45)
    same(cache);same(work/'model.json')
    run('domain.py','--work',work,'--output',work/'domain.json',guard=20);same(work/'domain.json')
    run('expand.py','--cell',15,'--output',work/'forest.json',guard=20);same(work/'forest.json')
    run('local.py','--from-fresh-cache',cache,'--seconds',40,
        '--output',work/'local.json',guard=40);same(work/'local.json')
    run('local_controls.py','--work',work,'--seconds',40,
        '--output',work/'local_controls.json',guard=40);same(work/'local_controls.json')
    run('prepare.py','--cell',15,'--work',work,'--seconds',40,guard=40)
    same(work/'source.json');same(work/'geometry.json')
    digest=hashlib.sha256((work/'geometry.json').read_bytes()).hexdigest()
    for start in range(0,cfg['source_leaves'],200):
        output=work/f'leaves_{start}.json'
        run('verify_shell.py','--geometry',work/'geometry.json','--geometry-sha',digest,
            '--forest',work/'forest.json','--start',start,
            '--count',min(200,cfg['source_leaves']-start),'--seconds',45,
            '--output',output,guard=45);same(output)
    run('source_controls.py','--work',work,'--geometry',work/'geometry.json',
        '--geometry-sha',digest,'--forest',work/'forest.json',
        '--output',work/'source_controls.json',guard=40);same(work/'source_controls.json')
    options=['--work',work,'--output',work/'complete.json']
    if args.compare:options+=['--compare',args.compare]
    run('aggregate.py',*options,guard=20);same(work/'complete.json')
    print(json.dumps(dict(mode=mode,complete=True,wall_seconds=time.monotonic()-begun,
        threads=1,maximum_cpu_intensive_children=1,per_child_guard_max_seconds=45,
        mathematical_whole_record_pairs=paired,generated='.generated/'+mode)),flush=True)
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--optimized',action='store_true');parser.add_argument('--compare')
    main(parser.parse_args())
