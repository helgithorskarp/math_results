"""Post-seal mathematical sensitivity controls; no producer imports."""
import pathlib,tempfile,subprocess,sys,json,hashlib,os
P=pathlib.Path(__file__).resolve().parent
SOURCE=(P/'primary.py').read_text()
EXPECTED=(P/'primary.py.out.json').read_bytes()
CAS=pathlib.Path(sys.argv[1]).resolve()
changes={
 'quotient loses forced 8z':('remainder=add(numerator,','Q[1]-=8\nremainder=add(numerator,'),
 'adjoint loses derivative boundary':('out[k-1]-=k*c','out[k-1]-=0*c'),
 'nilpotent inverse wrong coupling':('H[i][i+2]=-diag[i]*p0*(i+2)','H[i][i+2]=-2*diag[i]*p0*(i+2)'),
 'full kernel constant lost':('add(K,[R(4),zero,-4*C','add(K,[R(0),zero,-4*C'),
 'final p5 quotient sign':('drop.append(d)','drop.append(-d)'),
}
rows=[]
env=dict(os.environ)
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[k]='1'
with tempfile.TemporaryDirectory(dir=P) as tmp:
 for optimized in (False,True):
  for label,(old,new) in changes.items():
   if SOURCE.count(old)!=1:raise ValueError('unique mathematical mutation '+label)
   f=pathlib.Path(tmp)/'primary.py';f.write_text(SOURCE.replace(old,new));cmd=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+['-c',"import sys,runpy;sys.path.insert(0,sys.argv.pop(1));runpy.run_path(sys.argv.pop(1),run_name='__main__')",str(CAS),str(f)]
   r=subprocess.run(cmd,env=env,capture_output=True,timeout=55)
   # A mathematical invariant failure or ENTIRE coefficient record mismatch
   # must reject. Resource errors are not counted as successful rejection.
   invariant=b'ValueError' in r.stderr and b'Traceback' in r.stderr
   record=r.returncode==0 and json.loads(r.stdout)!=json.loads(EXPECTED)
   if not (invariant or record):raise ValueError('damage not lawfully rejected '+label)
   rows.append(dict(name=label,optimized=optimized,returncode=r.returncode,rejected_by='explicit exact invariant' if invariant else 'whole canonical record',output_sha256=hashlib.sha256(r.stdout).hexdigest()))
  r=subprocess.run([sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(P/'budgets.py'),'--damage'],env=env,capture_output=True,timeout=55)
  if r.returncode==0 or b'resonance residual' not in r.stderr:raise ValueError('budget damage rejected by exact named inequality')
  rows.append(dict(name='resonance residual exceeds complete closed bound',optimized=optimized,returncode=r.returncode,rejected_by='explicit exact inequality'))
print(json.dumps(dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',mathematical_controls=rows,all_six_damages_per_mode_rejected=True),sort_keys=True,separators=(',',':')))
