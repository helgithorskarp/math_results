"""Serial exact verification and external fixture damages, fixed45s per child.
Generated fixtures live in a temporary directory; no new source is mutated.
"""
import os,json,subprocess,tempfile,time,copy,resource
from pathlib import Path
def main():
 root=Path(__file__).resolve().parent;env=os.environ.copy()
 for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):env[k]='1'
 import sys
 base=json.loads((root/'EXPECTED.json').read_text());runs=[]
 def run(label,path=None,optimized=False,reject=False):
  cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(root/'verify.py')]+(['--expected',str(path)] if path else []);start=time.monotonic();p=subprocess.run(cmd,capture_output=True,text=True,env=env,timeout=45)
  if reject:
   if p.returncode==0 or not any(s in p.stderr for s in ['whole typed independent fixture mismatch','duplicate expected key','nonfinite expected value']):raise ValueError('specific mathematical fixture damage not rejected '+label)
   result='REJECTED'
  else:
   if p.returncode:raise ValueError(p.stderr)
   result=json.loads(p.stdout)
  runs.append({'label':label,'optimized':optimized,'seconds':round(time.monotonic()-start,6),'result':result})
 for opt in [False,True]:run('full independent record',optimized=opt)
 with tempfile.TemporaryDirectory(prefix='quartic-mass-controls-') as tmp:
  for label in ['matrix coefficient','last determinant value','omitted eliminant tail','typed prime coefficient','unit coefficient','duplicate key']:
   d=copy.deepcopy(base)
   if label=='matrix coefficient':d['whole_s0_matrix'][0][0]['1'][0]='0'
   if label=='last determinant value':d['resultants'][0]['values'][-1]=str(int(d['resultants'][0]['values'][-1])+1)
   if label=='omitted eliminant tail':d['whole_A'][0].pop(next(reversed(d['whole_A'][0])))
   if label=='typed prime coefficient':d['new_modular_unit']['leading_coefficients'][0]=True
   if label=='unit coefficient':d['new_modular_unit']['U'][-1]=(d['new_modular_unit']['U'][-1]+1)%263
   txt=json.dumps(d)
   if label=='duplicate key':txt='{"actual_agent":"six-reviewer-3",'+txt[1:]
   p=Path(tmp)/(label.replace(' ','_')+'.json');p.write_text(txt)
   for opt in [False,True]:run(label,p,opt,True)
 out={'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','runs':runs,'external_damages_rejected':12,'normal_optimized_whole_match':runs[0]['result']==runs[1]['result'],'native_threads':1,'max_simultaneous_math_children':1,'per_child_guard_seconds':45,'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
 if not out['normal_optimized_whole_match']:raise ValueError('mode mismatch')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
