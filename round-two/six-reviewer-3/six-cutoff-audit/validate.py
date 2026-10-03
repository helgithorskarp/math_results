"""Entire independent record replay. Exactly one serial45s math child at once."""
import argparse,json,os,resource,subprocess,sys,tempfile,time,hashlib
from pathlib import Path
from joint_input import load

PHASES=['uniform','generic']+['negative-'+str(q) for q in range(6,22)]+['positive-22','positive-23','joint-21']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--receipt',type=Path);a=ap.parse_args();here=Path(__file__).resolve().parent
 seal=load(here/'INDEPENDENCE.json')
 for name,h in seal['files'].items():
  if hashlib.sha256((here/name).read_bytes()).hexdigest()!=h:raise ValueError('sealed independent core changed: '+name)
 expected={name:load(here/('EXPECTED-'+name+'.json')) for name in ['uniform','generic','negative','positive-22','positive-23','joint-21']}
 def frozen(phase):return expected['negative'][phase] if phase.startswith('negative') else expected[phase]
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONPATH',None)
 for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[name]='1'
 runs=[];modes=[]
 with tempfile.TemporaryDirectory(prefix='independent-six-cutoff-') as tmp:
  for mode,flags in [('normal',[]),('optimized',['-O'])]:
   records={}
   for phase in PHASES:
    output=Path(tmp)/(mode+'-'+phase+'.json');cmd=[sys.executable,*flags,str(here/'run_phase.py'),phase,'--emit',str(output)]
    if phase=='joint-21':cmd+=['--joint-input',str(here/'JOINT-INPUT.json')]
    start=time.monotonic();r=subprocess.run(cmd,capture_output=True,text=True,timeout=45,env=env);row={'mode':mode,'phase':phase,'exit_code':r.returncode,'seconds':round(time.monotonic()-start,6)}
    if r.returncode:raise ValueError(r.stderr)
    x=load(output)
    if json.dumps(x,sort_keys=True,separators=(',',':'))!=json.dumps(frozen(phase),sort_keys=True,separators=(',',':')):raise ValueError('entire typed phase differs: '+phase)
    records[phase]=x;row['summary']=json.loads(r.stdout);runs.append(row)
   start=time.monotonic();r=subprocess.run([sys.executable,*flags,str(here/'damage.py')],capture_output=True,text=True,timeout=45,env=env)
   if r.returncode:raise ValueError(r.stderr)
   controls=json.loads(r.stdout)
   if not controls['all14_semantic_controls_rejected']:raise ValueError('incomplete semantic controls')
   runs.append({'mode':mode,'phase':'damage','exit_code':r.returncode,'seconds':round(time.monotonic()-start,6),'summary':controls});modes.append(records)
 if modes[0]!=modes[1]:raise ValueError('entire normal/O mathematical records differ')
 whole=json.dumps(modes[0],sort_keys=True,separators=(',',':')).encode();receipt={'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','python':sys.version.split()[0],'whole_validation':True,'complete_normal_optimized_frozen_equal':True,'independent_record_sha256':hashlib.sha256(whole).hexdigest(),'serial_child_runs':runs,'guard_seconds':45,'native_threads':1,'unchanged_scope':'1CPU2GiB','peak_child_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'active_math_jobs':0,'ordinary_imports_and_lift_not_formalized':True}
 if a.receipt:a.receipt.write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({k:v for k,v in receipt.items() if k!='serial_child_runs'}))
if __name__=='__main__':main()
