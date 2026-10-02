"""Fresh relocated source-only replay, serial native threads one.
Large outputs are regenerated in the explicitly named local work directory.
"""
from pathlib import Path
import argparse,json,hashlib,os,resource,shutil,subprocess,sys,time

def need(ok,message):
    if not ok:raise ValueError(message)

def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
    root=Path(__file__).resolve().parent;work=a.work.resolve()
    need(not work.exists(),'fresh work directory required')
    source=work/'source';source.mkdir(parents=True)
    names=['rows.py','fixtures.json','populations.py','physical.py','audit.py','controls.py']
    pins={n:hashlib.sha256((root/n).read_bytes()).hexdigest()for n in names}
    for n in names:shutil.copy2(root/n,source/n)
    expected=json.loads((root/'EXPECTED.json').read_bytes())
    env=dict(os.environ)
    for n in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[n]='1'
    env['PYTHONDONTWRITEBYTECODE']='1'
    interpreter=[sys.executable]+(['-O']if sys.flags.optimize else [])
    steps=[['physical.py'],['audit.py','--physical',str(source/'physical-local.json'),'--out',str(work/'audit.json')],['controls.py']]
    stages=[];start=time.monotonic()
    for arguments in steps:
        begun=time.monotonic()
        r=subprocess.run(interpreter+[str(source/arguments[0])]+arguments[1:],env=env,capture_output=True,text=True,timeout=60)
        (work/(arguments[0]+'.stdout')).write_text(r.stdout)
        (work/(arguments[0]+'.stderr')).write_text(r.stderr)
        need(r.returncode==0,'incomplete/failed stage provides no absence: '+arguments[0]+'\n'+r.stderr)
        stages.append({'stage':arguments[0],'seconds':time.monotonic()-begun,'exit':r.returncode})
        print(json.dumps({'stage':arguments[0],'status':'PASS'}),flush=True)
    outputs={'physical':(source/'physical-local.json').read_bytes(),'audit':(work/'audit.json').read_bytes(),
             'controls':json.dumps(json.loads((work/'controls.py.stdout').read_text()),sort_keys=True,separators=(',',':')).encode()+b'\n'}
    hashes={n:hashlib.sha256(raw).hexdigest()for n,raw in outputs.items()}
    need(hashes==expected['whole_output_sha256'],'entire independent output differs')
    need(pins=={n:hashlib.sha256((root/n).read_bytes()).hexdigest()for n in names},'source mutation')
    record={'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','python':sys.version,
            'mode':'optimized'if sys.flags.optimize else 'normal','outputs':hashes,'stages':stages,
            'total_seconds':time.monotonic()-start,'child_peak_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'serial_children':True,'native_threads':1,'child_timeout_seconds':60,'status':'COMPLETE'}
    (work/'VALIDATION.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,sort_keys=True))

if __name__=='__main__':main()
