"""Serial complete H36 exports and four semantic whole-fixture damages."""
import json,os,resource,subprocess,sys,tempfile,time,hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
env=os.environ.copy()
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[k]='1'

def run(mode,extra):
    start=time.monotonic()
    p=subprocess.run([sys.executable,'-I','-B']+mode+[str(root/'refine.py')]+extra,capture_output=True,env=env,timeout=45)
    return p,time.monotonic()-start

def main():
    positive=[];raw=None
    for mode in [[],['-O']]:
        p,seconds=run(mode,['--emit'])
        if p.returncode:raise ValueError(p.stderr.decode())
        if raw is not None and raw!=p.stdout:raise ValueError('complete refinement records differ')
        raw=p.stdout;positive.append({'mode':'optimized' if mode else 'normal','seconds':seconds,'whole_record_sha256':hashlib.sha256(raw.rstrip(b'\n')).hexdigest()})
    original=json.loads((root/'REFINEMENT.json').read_text());rejections=[]
    with tempfile.TemporaryDirectory(prefix='entry-refine-') as td:
        for i,label in enumerate(['changed radius','changed entire favorable coefficient','boolean energy alias','extra global conclusion']):
            a=json.loads(json.dumps(original))
            if i==0:a['budgets']['radius']='3/128'
            if i==1:a['budgets']['favorable_alpha']='151/1024'
            if i==2:a['energy_cutoff']=True
            if i==3:a['global_first_power']=True
            path=Path(td)/(str(i)+'.json');path.write_text(json.dumps(a))
            for mode in [[],['-O']]:
                p,seconds=run(mode,['--expected',str(path)])
                if not p.returncode or b'entire typed refinement fixture differs' not in p.stderr:raise ValueError('specific refinement rejection failed')
                rejections.append({'case':label,'mode':'optimized' if mode else 'normal','reason':'entire typed refinement fixture differs'})
    print(json.dumps({'positive':positive,'fixture_rejections':rejections,'peak_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss},indent=2))

if __name__=='__main__':main()
