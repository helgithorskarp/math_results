"""Serial normal/optimized whole-evidence and semantic fixture rejection."""
import hashlib,json,os,resource,subprocess,sys,tempfile,time
from pathlib import Path
base=Path(__file__).resolve().parent
env=os.environ.copy()
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[k]='1'

def run(args):
    start=time.monotonic();p=subprocess.run([sys.executable,'-I','-B']+args,capture_output=True,env=env,timeout=45)
    return p,time.monotonic()-start

def main():
    positive=[];normal=None
    for mode in [[],['-O']]:
        p,seconds=run(mode+[str(base/'verify.py'),'--emit'])
        if p.returncode:raise ValueError(p.stderr.decode())
        if normal is not None and normal!=p.stdout:raise ValueError('whole normal/O records differ')
        normal=p.stdout
        positive.append({'mode':'optimized' if mode else 'normal','seconds':seconds,'record_sha256':hashlib.sha256(p.stdout.rstrip(b'\n')).hexdigest()})
    original=json.loads((base/'EXPECTED.json').read_text());bad=[]
    with tempfile.TemporaryDirectory(prefix='entry-audit-') as temp:
        def changed(label,mutate):
            obj=json.loads(json.dumps(original));mutate(obj);return label,json.dumps(obj)
        cases=[
            changed('changed Fourier coefficient',lambda a:a['audit']['rows'][1].__setitem__('d0I*d8I',['0','0'])),
            changed('missing complete row',lambda a:a['audit']['rows'].pop()),
            changed('changed widened energy constant',lambda a:a['audit']['budgets']['32'].__setitem__('lower_cap','1/3')),
            changed('boolean integer alias',lambda a:a['audit']['literal_pair_tables'][0][0].__setitem__(0,False)),
            changed('extra root fixture',lambda a:a['audit']['literal_root_controls'].append({})),
            ('duplicate key','{"actual_agent":"six-reviewer-3",'+(base/'EXPECTED.json').read_text().lstrip()[1:]),
            ('nonfinite constant','{"x":NaN}'),
        ]
        for i,(label,text) in enumerate(cases):
            path=Path(temp)/('bad'+str(i)+'.json');path.write_text(text)
            for mode in [[],['-O']]:
                p,seconds=run(mode+[str(base/'verify.py'),'--expected',str(path)])
                reason='duplicate JSON key' if label=='duplicate key' else 'nonfinite JSON constant' if label=='nonfinite constant' else 'entire typed independent fixture mismatch'
                if p.returncode==0 or reason not in p.stderr.decode():raise ValueError(label+' failed intended rejection')
                bad.append({'case':label,'mode':'optimized' if mode else 'normal','reason':reason})
    print(json.dumps({'positive':positive,'fixture_rejections':bad,'peak_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss},indent=2))

if __name__=='__main__':main()
