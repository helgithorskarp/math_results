"""Fresh source-only, serial normal/O proof checks, fixed30s/mathchild."""
import argparse,hashlib,json,os,platform,resource,subprocess,sys,time
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True);a=parser.parse_args()
if a.work.exists():raise ValueError('output work path must not exist')
a.work.mkdir(parents=True);base=Path(__file__).resolve().parent
env=os.environ.copy()
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[k]='1'
receipts=[];results={}
for mode in ('normal','optimized'):
 p=a.work/mode;p.mkdir();record=p/'record.json'
 for name,args in [('produce.py',[str(record)]),('check.py',[str(record)]),('controls.py',[str(record)])]:
  cmd=[sys.executable,'-B',*(['-O']if mode=='optimized'else[]),str(base/name),*args];t=time.monotonic()
  try:r=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=30)
  except subprocess.TimeoutExpired as e:
   (a.work/'TIMEOUT.json').write_text(json.dumps({'command':cmd,'guard_seconds':30,'no_nonexistence_conclusion':True})+'\n');raise
  (p/(name+'.stdout')).write_text(r.stdout);(p/(name+'.stderr')).write_text(r.stderr)
  receipts.append({'mode':mode,'program':name,'exit_code':r.returncode,'seconds':time.monotonic()-t,'peak_child_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
  if r.returncode:raise ValueError('failed math child '+name)
  value=json.loads(r.stdout)
  if name!='produce.py':results[mode+':'+name]=value
 for name in ('check.py','controls.py'):
  if mode=='optimized'and results[mode+':'+name]!=results['normal:'+name]:raise ValueError('whole normal/O result mismatch')
 if mode=='optimized'and record.read_bytes()!=(a.work/'normal/record.json').read_bytes():raise ValueError('whole normal/O raw record mismatch')
raw=(a.work/'normal/record.json').read_bytes()
out={'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','python':platform.python_version(),'schema':'cubic-motion-audit-v1','guard_seconds_per_math_child':30,'native_thread_variables':{k:env[k]for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')},'single_serial_math_child':True,'record_bytes':len(raw),'whole_record_sha256':hashlib.sha256(raw).hexdigest(),'whole_normal_optimized_records_equal':True,'results':results,'receipts':receipts}
(a.work/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'complete','math_children':6,'whole_record_sha256':out['whole_record_sha256'],'record_bytes':len(raw),'maximum_child_seconds':max(q['seconds']for q in receipts),'peak_child_kib':max(q['peak_child_kib']for q in receipts)}))
