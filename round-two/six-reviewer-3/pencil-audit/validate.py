"""Cold full-record normal/O and six complete damaged-fixture checks."""
import json, os, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def main():
    env=os.environ.copy()
    for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[key]='1'
    outputs=[]
    for opt in (False,True):
        argv=[sys.executable,'-I','-B']+(['-O'] if opt else [])+[str(ROOT/'verify.py'),'--emit']
        result=subprocess.run(argv,env=env,capture_output=True,timeout=45)
        if result.returncode:raise ValueError(result.stderr.decode())
        outputs.append(result.stdout)
    if outputs[0]!=outputs[1]:raise ValueError('whole normal/optimized records differ')
    original=json.loads(outputs[0]);fixtures={}
    def clone():return json.loads(outputs[0])
    x=clone();p=x['algebra']['whole_matrix'][0][0];p[next(iter(p))][0]='999';fixtures['coefficient']=json.dumps(x)
    x=clone();del x['algebra']['whole_matrix'];fixtures['missing']=json.dumps(x)
    x=clone();x['unexpected']=True;fixtures['extra']=json.dumps(x)
    x=clone();x['algebra']['rank_controls'][0]['positive_scalar_root']=1;fixtures['type_alias']=json.dumps(x)
    fixtures['duplicate']='{"actual_agent":"duplicate",'+outputs[0].decode().lstrip()[1:]
    fixtures['nonfinite']='{"unexpected":NaN,'+outputs[0].decode().lstrip()[1:]
    receipts=[]
    with tempfile.TemporaryDirectory(prefix='six-reviewer-3-pencil-') as tmp:
        for name,text in fixtures.items():
            fixture=Path(tmp)/(name+'.json');fixture.write_text(text)
            for opt in (False,True):
                argv=[sys.executable,'-I','-B']+(['-O'] if opt else [])+[str(ROOT/'verify.py'),'--expected',str(fixture)]
                result=subprocess.run(argv,env=env,capture_output=True,timeout=45)
                if result.returncode!=1:raise ValueError('damaged whole fixture survived '+name)
                receipts.append({'case':name,'optimized':opt,'rejected':True})
    print(json.dumps({'status':'PASS','whole_normal_optimized_equal':True,'entire_fixture_rejections':receipts,'serial_children':True,'native_threads':1,'guard_seconds_per_child':45}))
if __name__=='__main__':main()
