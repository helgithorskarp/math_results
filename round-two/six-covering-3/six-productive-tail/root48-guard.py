"""One serial child, fixed20s external guard; no completion inferred on failure."""
from pathlib import Path
import json,os,resource,subprocess,sys,time

out=Path(sys.argv[1]);command=sys.argv[2:]
env=os.environ.copy()
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    env[name]='1'
start=time.monotonic()
try:
    r=subprocess.run(command,capture_output=True,text=True,env=env,timeout=20)
    result={'status':'COMPLETE_CHILD_EXIT0' if r.returncode==0 else 'FAILED_NO_EXCLUSION',
            'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
except subprocess.TimeoutExpired as e:
    decode=lambda v:v.decode(errors='replace') if isinstance(v,bytes) else v
    result={'status':'INCOMPLETE_TIMEOUT_NO_EXCLUSION','exit':None,'stdout':decode(e.stdout),'stderr':decode(e.stderr)}
result.update({'command':command,'seconds':time.monotonic()-start,'guard_seconds':20,'threads':1,
               'one_CPU_child':True,'RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('stdout','stderr')},indent=2))
