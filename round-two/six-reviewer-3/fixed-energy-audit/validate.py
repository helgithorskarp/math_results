"""Run normal/O and typed-fixture rejection checks, one mathematical child at a time."""
import json,sys,subprocess,time,resource,tempfile,os
from pathlib import Path
def run():
 here=Path(__file__).resolve().parent
 expected=json.loads((here/'EXPECTED.json').read_text())
 for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:os.environ[name]='1'
 originals=[];rejections=[]
 def command(flags,path=None):
  return [sys.executable,'-I','-B',*flags,str(here/'verify.py')]+([] if path is None else [str(path)])
 for flags in [[],['-O']]:
  start=time.monotonic();p=subprocess.run(command(flags),capture_output=True,text=True,timeout=45)
  if p.returncode:raise ValueError(p.stderr)
  originals.append({'mode':flags,'seconds':time.monotonic()-start,'result':json.loads(p.stdout)})
 if originals[0]['result']!=originals[1]['result']:raise ValueError('mode disagreement')
 changes=[]
 x=json.loads(json.dumps(expected));x['counts']['strict_scalar_margins']=True;changes.append(('typed count',json.dumps(x),'whole typed'))
 x=json.loads(json.dumps(expected));del x['quantities'];changes.append(('missing complete section',json.dumps(x),'whole typed'))
 x=json.loads(json.dumps(expected));x['quantities']['variance_divisors']['initial']='0';changes.append(('initial positive divisor',json.dumps(x),'whole typed'))
 x=json.loads(json.dumps(expected));x['literal_controls'][0]['polynomial'][9][0]='2';changes.append(('literal leading coefficient',json.dumps(x),'whole typed'))
 x=json.loads(json.dumps(expected));x['identities']['individual_actual_normal']['coefficients']['1']=['1','0'];changes.append(('complex normal coefficient',json.dumps(x),'whole typed'))
 x=json.loads(json.dumps(expected));x['literal_controls']=x['literal_controls'][:-1];changes.append(('lost coverage row',json.dumps(x),'whole typed'))
 changes.append(('duplicate key','{"counts":0,"counts":1}','duplicate JSON key'))
 changes.append(('nonfinite','{"invalid":NaN}','nonfinite JSON value'))
 with tempfile.TemporaryDirectory(prefix='fixed-energy-check-',dir=here) as temp:
  for name,body,reason in changes:
   f=Path(temp)/'fixture.json';f.write_text(body)
   for flags in [[],['-O']]:
    p=subprocess.run(command(flags,f),capture_output=True,text=True,timeout=45)
    if p.returncode==0 or reason not in p.stderr:raise ValueError('fixture rejection failed:'+name)
    rejections.append({'name':name,'mode':flags,'expected_failure':reason})
 return {'normal_optimized':originals,'typed_fixture_rejections':rejections,'peak_child_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'resource_contract':'one serial child/native1/fixed45s/unchanged1CPU2GiB','fixture_scope':'Record/input sensitivity, not a claim that every changed bound is mathematically false.'}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
