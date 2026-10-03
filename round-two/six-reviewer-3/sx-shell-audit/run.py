"""Serial source-only normal/optimized WHOLE mathematical replay."""
import hashlib,json,os,resource,subprocess,sys,time
from pathlib import Path

def main():
    root=Path(__file__).resolve().parent;fix=json.loads((root/'RESULTS.json').read_text());receipts=[];normal={}
    env=os.environ.copy()
    for n in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[n]='1'
    for optimized in [False,True]:
        for name,file in [('primary','check.py'),('controls','controls.py')]:
            begin=time.monotonic();p=subprocess.run([sys.executable]+(['-O'] if optimized else [])+[file],cwd=root,env=env,capture_output=True,timeout=30)
            if p.returncode:raise RuntimeError(file+' failed: '+p.stderr.decode())
            json.loads(p.stdout);sha=hashlib.sha256(p.stdout).hexdigest();expected=fix['records'][name]
            if len(p.stdout)!=expected['whole_stdout_bytes'] or sha!=expected['whole_stdout_sha256']:raise ValueError('whole mathematical output differs')
            if name in normal and normal[name]!=p.stdout:raise ValueError('whole normal/optimized bytes differ')
            normal[name]=p.stdout;receipts.append({'name':name,'optimized':optimized,'whole_stdout_bytes':len(p.stdout),'whole_stdout_sha256':sha,'seconds':time.monotonic()-begin,'cumulative_peak_child_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
    print(json.dumps({'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','all_whole_records_verified':True,'python':sys.version.split()[0],'native_threads':1,'serial':True,'fixed_child_guard_seconds':30,'successful_children':len(receipts),'children':receipts},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
