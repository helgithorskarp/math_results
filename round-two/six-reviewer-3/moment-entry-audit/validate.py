import os,sys,subprocess,json,hashlib,time,resource,tempfile,copy
from pathlib import Path
root=Path(__file__).resolve().parent;env=os.environ.copy()
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[k]='1'
(root/'.generated').mkdir(exist_ok=True)
rows=[]
def run(label,flags,path,okay):
 start=time.monotonic();r=subprocess.run(['/scratch/venvs/discovery-team/bin/python','-I','-B',*flags,str(root/'verify.py'),'--fixture',str(path)],capture_output=True,text=True,timeout=45,env=env)
 if (r.returncode==0)!=okay:raise ValueError(label+r.stdout+r.stderr)
 rows.append({'label':label,'returncode':r.returncode,'seconds':round(time.monotonic()-start,6),'expected_acceptance':okay,'stdout':r.stdout,'rejection':r.stderr.strip().splitlines()[-1] if r.stderr else None});print(label,r.returncode,round(time.monotonic()-start,3),flush=True)
run('normal complete record',[],root/'EXPECTED.json',True);run('optimized complete record',['-O'],root/'EXPECTED.json',True)
x=json.loads((root/'EXPECTED.json').read_text())
with tempfile.TemporaryDirectory(dir=root/'.generated') as t:
 d=Path(t);run('missing fixture',[],d/'missing.json',False)
 p=d/'bad.json';p.write_text('{bad');run('malformed JSON fixture',['-O'],p,False)
 y=copy.deepcopy(x);y['proved_scope']['both_feasible_inward_families']=False
 p=d/'changed.json';p.write_text(json.dumps(y));run('changed feasibility record',[],p,False)
 y=copy.deepcopy(x);y['universal_polynomial_and_energy_identities']['universal_identities'].pop('literal physical first h moment')
 p=d/'omitted.json';p.write_text(json.dumps(y));run('omitted complete identity',['-O'],p,False)
 y=copy.deepcopy(x);y['whole_joint_original_root_majorants']['impulse']['exact_norm']='1'
 p=d/'norm.json';p.write_text(json.dumps(y));run('altered exact whole original norm',[],p,False)
 y=copy.deepcopy(x);y['ignored_padding']='not silently accepted'
 p=d/'extra.json';p.write_text(json.dumps(y));run('unexpected entire-field padding',['-O'],p,False)
print('WHOLE VALIDATION PASS',len(rows),flush=True)
