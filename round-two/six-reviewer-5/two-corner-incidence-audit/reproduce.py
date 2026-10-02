"""Serial portable owned evidence/controls, normal and optimized."""
import pathlib,os,subprocess,sys,json,time,resource
P=pathlib.Path(__file__).resolve().parent
env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1')
runs=[]
for optimized in (False,True):
 for program in ('controls.py','verify.py'):
  start=time.monotonic();r=subprocess.run([sys.executable,'-B']+(['-O'] if optimized else [])+[str(P/program)],cwd=P,env=env,capture_output=True,text=True,timeout=45)
  if r.returncode:raise ValueError(r.stderr)
  runs.append(dict(program=program,optimized=optimized,result=json.loads(r.stdout),seconds=time.monotonic()-start,maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,guard_seconds=45))
for program in ('controls.py','verify.py'):
 out=[r['result'] for r in runs if r['program']==program]
 if out[0]!=out[1]:raise ValueError('normal/optimized difference')
print(json.dumps(dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',serial=True,native_threads=1,runs=runs),sort_keys=True))
