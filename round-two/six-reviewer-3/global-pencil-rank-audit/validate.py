"""Serial full normal/O replay and six changed-fixture trust-boundary cases."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):os.environ[key]='1'
import json,subprocess,time,copy,tempfile,sys,resource
from pathlib import Path

def main():
 root=Path(__file__).resolve().parent;expected=json.loads((root/'EXPECTED.json').read_text());results=[]
 for optimized in (False,True):
  cmd=[sys.executable]+(['-O'] if optimized else [])+[str(root/'verify.py')];t=time.monotonic();p=subprocess.run(cmd,text=True,capture_output=True,timeout=45,check=True);results.append({'optimized':optimized,'seconds':time.monotonic()-t,'result':json.loads(p.stdout)})
  changes=[]
  bad=copy.deepcopy(expected);bad['derived_P20'][7]+=1;changes.append(('degree20_factor',json.dumps(bad)))
  bad=copy.deepcopy(expected);bad['full_modular_units'][0]['U'][-1]=(bad['full_modular_units'][0]['U'][-1]+1)%257;changes.append(('whole_modular_multiplier',json.dumps(bad)))
  bad=copy.deepcopy(expected);row=bad['whole_matrix'][0][0];key=next(iter(row));row[key][0]=str(-__import__('fractions').Fraction(row[key][0]));changes.append(('matrix_coefficient_sign',json.dumps(bad)))
  bad=copy.deepcopy(expected);bad['integer_determinant_values'][0]=False;changes.append(('int_boolean_type',json.dumps(bad)))
  changes.append(('duplicate_key','{"derived_P20":[],"derived_P20":[]}'));changes.append(('nonfinite_json','{"x":NaN}'))
  with tempfile.TemporaryDirectory(prefix='rank-two-audit-') as tmp:
   for name,text in changes:
    path=Path(tmp)/'changed.json';path.write_text(text);t=time.monotonic();p=subprocess.run(cmd+['--expected',str(path)],text=True,capture_output=True,timeout=45)
    message='duplicate fixture key' if name=='duplicate_key' else 'nonfinite fixture' if name=='nonfinite_json' else 'whole typed fixture mismatch'
    if p.returncode==0 or message not in p.stderr:raise ValueError('intended fixture rejection missing '+name)
    results.append({'optimized':optimized,'changed_fixture':name,'intended_rejection':message,'seconds':time.monotonic()-t})
 print(json.dumps({'status':'PASS','stages':results,'changed_cases':6,'intended_fixture_rejections':12,'no_claim_of_12_false_math_theorems':True,'peak_child_rss_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss},sort_keys=True))
if __name__=='__main__':main()
