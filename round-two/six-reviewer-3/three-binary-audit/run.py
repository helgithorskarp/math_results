"""Portable source-only reproduction, one guarded mathematical child at a time."""
import subprocess,sys,os,time,json,resource,argparse
from pathlib import Path
from hashlib import sha256
from merge import summary
from engine import require,digest
p=argparse.ArgumentParser();p.add_argument('--mode',choices=('normal','optimized','both'),default='both');p.add_argument('--output',default='generated');args=p.parse_args()
base=Path(__file__).resolve().parent;output=Path(args.output).resolve();output.mkdir(parents=True,exist_ok=True)
env=os.environ.copy()
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):env[key]='1'
results={};receipts=[]
for mode in (('normal','optimized') if args.mode=='both' else (args.mode,)):
    root=output/mode;root.mkdir(parents=True,exist_ok=True);flags=['-B']+(['-O'] if mode=='optimized' else [])
    def child(name,program,*argv):
        t=time.monotonic();cmd=[sys.executable,*flags,str(base/program),*map(str,argv)]
        try:r=subprocess.run(cmd,capture_output=True,env=env,timeout=45)
        except subprocess.TimeoutExpired:
            raise RuntimeError('45-second guard: incomplete verification, no mathematical exclusion; stop work')
        receipts.append({'mode':mode,'name':name,'seconds':time.monotonic()-t,'returncode':r.returncode,'peak_child_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'guard_seconds':45,'threads':1})
        if r.returncode:raise RuntimeError(r.stderr.decode()+r.stdout.decode())
        print(mode,name,'passed',round(receipts[-1]['seconds'],3),flush=True)
    child('cover','cover.py',root/'cover.json')
    for start in range(0,1042,128):child('audit'+str(start),'audit.py',root/'cover.json',base/'INSTANCE.json',root/f'audit-{start}.json',start,min(start+128,1042))
    child('merge','merge.py',root,root/'primary.json')
    for kind,total in [('base',442),('cubes',4336)]:
        for start in range(0,total,128):child('scalar'+kind+str(start),'corroborate.py',root/'primary.json',root/'cover.json',kind,start,min(start+128,total),root/f'scalar-{kind}-{start}.json')
    child('controls','controls.py',root/'primary.json',root/'cover.json',base/'INSTANCE.json',root/'controls.json')
    results[mode]=summary(root);(root/'MATHEMATICS.json').write_text(json.dumps(results[mode],indent=2)+'\n')
if len(results)==2:require(results['normal']==results['optimized'],'whole mathematical records differ across modes')
(output/'RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n');print(json.dumps({'mathematics':results,'whole_mathematics_sha256':{m:digest(v) for m,v in results.items()}},indent=2))
