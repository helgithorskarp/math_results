"""Bounded serial cold replay; exact outputs, one mathematical child at a time."""
from pathlib import Path
import subprocess,os,sys,time,resource,json,hashlib,tempfile

HERE=Path(__file__).resolve().parent

def require(ok,msg):
    if not ok:raise ValueError(msg)

def main():
    env={**os.environ,**{k:'1' for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS',
         'MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']},
         'PYTHONDONTWRITEBYTECODE':'1'}
    manifest=json.loads((HERE/'provenance.json').read_text())['original_files']
    for entry in manifest:
        b=(HERE/'original'/entry['name']).read_bytes()
        require(hashlib.sha256(b).hexdigest()==entry['sha256'],'unchanged original '+entry['name'])
    original=(HERE/'original'/'EXPECTED.json').read_bytes()
    expected=(HERE/'expected.json').read_bytes()
    runs=[]
    for optimized in [False,True]:
        python=[sys.executable]+(['-O'] if optimized else [])
        for name,args,wanted in [
            ('independent',['verify.py'],expected),
            ('original-producer',['original/derive.py'],original),
            ('original-checker',['original/verify.py','--emit'],original),
            ('original-controls',['original/verify.py','--self-test'],None)]:
            started=time.monotonic()
            p=subprocess.run(python+args,cwd=HERE,env=env,capture_output=True,timeout=60)
            require(p.returncode==0,'failed complete stage '+name+': '+p.stderr.decode())
            if wanted is not None:require(p.stdout==wanted,'entire output '+name)
            else:require(json.loads(p.stdout)=={'six_point_subset_pairs':4096,'rejected_damages':14},'original damages')
            runs.append({'stage':name,'optimized':optimized,'seconds':round(time.monotonic()-started,6),
                'sha256':hashlib.sha256(p.stdout).hexdigest(),'output_bytes':len(p.stdout),
                'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
            print(json.dumps(runs[-1],sort_keys=True),file=sys.stderr,flush=True)
    print(json.dumps({'verified':True,'python':sys.version.split()[0],
        'serial_math_children':1,'numerical_threads':1,'guard_seconds_per_stage':60,
        'scope':'unchanged1CPU2GiB','runs':runs},sort_keys=True))

if __name__=='__main__':main()
