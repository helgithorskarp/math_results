"""Bounded serial cold replay and six whole-fixture damage controls."""
import copy,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path

def main():
    root=Path(__file__).resolve().parent;env=os.environ.copy()
    for n in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[n]='1'
    def run(expected=None,optimized=False,emit=False):
        cmd=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(root/'verify.py')]
        if expected is not None:cmd+=['--expected',str(expected)]
        if emit:cmd+=['--emit']
        return subprocess.run(cmd,env=env,capture_output=True,timeout=45)
    a=run(emit=True);b=run(optimized=True,emit=True)
    if a.returncode or b.returncode or a.stdout!=b.stdout:raise ValueError('whole cold normal/optimized replay differs')
    base=json.loads((root/'EXPECTED.json').read_text());cases={}
    x=copy.deepcopy(base);x['algebra']['whole_generic_kernel'][6]['p6'][0]='16';cases['coefficient_sign']=json.dumps(x)
    x=copy.deepcopy(base);del x['algebra']['checks']['sixth kernel coefficient'];cases['missing_identity']=json.dumps(x)
    x=copy.deepcopy(base);x['extra']=True;cases['extra_field']=json.dumps(x)
    x=copy.deepcopy(base);x['controls']['actual_derivative_count']=21.0;cases['numeric_type']=json.dumps(x)
    cases['duplicate_key']='{"actual_agent":"six-reviewer-3",'+json.dumps(base)[1:]
    cases['nonfinite']='{"bad":NaN,'+json.dumps(base)[1:]
    scratch=Path.cwd()/'scratch';scratch.mkdir(exist_ok=True)
    rejected=[]
    with tempfile.TemporaryDirectory(prefix='mass-chart-audit-',dir=scratch) as directory:
        for name,data in cases.items():
            p=Path(directory)/(name+'.json');p.write_text(data)
            for opt in (False,True):
                r=run(p,optimized=opt)
                if r.returncode==0:raise ValueError('damaged whole fixture accepted: '+name)
                rejected.append({'case':name,'optimized':opt})
    print(json.dumps({'status':'PASS','entire_normal_optimized_equal':True,'canonical_sha256':hashlib.sha256(a.stdout.rstrip(b'\n')).hexdigest(),'six_fixtures_rejected_both_modes':rejected},sort_keys=True))

if __name__=='__main__':main()
