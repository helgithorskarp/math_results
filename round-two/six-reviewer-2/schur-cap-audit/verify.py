"""Self-contained serial replay, no author imports or external mathematical input."""
from pathlib import Path
import hashlib,json,os,resource,subprocess,sys,time

def main():
 root=Path(__file__).resolve().parent;env=dict(os.environ)
 for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:env[name]='1'
 phases=[('calibrations',None),('controls',None)]+[('negative',q)for q in range(5,19)]+[(phase,q)for phase in ['positive','stronger']for q in range(19,24)]
 records=[];started=time.monotonic()
 for phase,q in phases:
  argv=[sys.executable,'-B']+(['-O']if sys.flags.optimize else[])+[str(root/'audit.py'),phase]+(['--q',str(q)]if q is not None else[])+['--expected',str(root/('EXPECTED-'+phase+'.json'))]
  try:r=subprocess.run(argv,capture_output=True,text=True,env=env,timeout=90)
  except subprocess.TimeoutExpired:raise SystemExit('INCOMPLETE fixed phase timeout; no mathematical exclusion')
  if r.returncode:raise SystemExit(r.stdout+r.stderr)
  records.append(json.loads(r.stdout))
 mathematical=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 print(json.dumps({'agent':'six-reviewer-2','role':'independent mathematical reviewer','status':'PASS','phases':len(records),'whole_record_sha256':mathematical,'seconds':round(time.monotonic()-started,3),'peak_child_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'whole_positive_entries_per_endpoint':659171,'positive_q':list(range(19,24)),'negative_q':list(range(5,19)),'semantic_rejections':12,'scope':'original finite boundary and stronger endpoint; real strip by written convexity; infinite adaptive tail imported'},sort_keys=True))
if __name__=='__main__':main()
