"""Portable serial normal/optimized/cold/damage validation; no producer input."""
from pathlib import Path
import subprocess,tempfile,time,os,json,resource,shutil,sys
D=Path(__file__).resolve().parent
def run(args,cwd,success):
    env=os.environ.copy()
    for n in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[n]='1'
    start=time.monotonic();p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True,timeout=45)
    if (p.returncode==0)!=success:raise ValueError('unexpected validation outcome '+p.stdout+p.stderr)
    return {'returncode':p.returncode,'seconds':round(time.monotonic()-start,6),'peak_children_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'stdout':p.stdout.strip(),'stderr_last':p.stderr.splitlines()[-1]if p.stderr else ''}
def main():
    rows=[]
    for optimized in [False,True]:
        cmd=[sys.executable,'-B']+(['-O']if optimized else [])
        for name in ['core.py','checks.py']:
            rows.append({'case':name,'optimized':optimized,**run(cmd+[str(D/name)],D,True)})
        with tempfile.TemporaryDirectory(prefix='polar-entry-independent-')as tmp:
            T=Path(tmp)
            for name in ['core.py','arithmetic.py','cube.py','checks.py','EXPECTED.json']:shutil.copyfile(D/name,T/name)
            rows.append({'case':'fresh-source-core','optimized':optimized,**run(cmd+[str(T/'core.py')],T,True)})
            base=json.loads((D/'EXPECTED.json').read_text())
            damages=[]
            z=json.loads(json.dumps(base));z['polar']['streams']['phase']['coefficients'][-1]='0';damages.append(('whole-polar-last-coefficient',json.dumps(z)))
            z=json.loads(json.dumps(base));z['Newton'][1]['polynomials']['7'].pop();damages.append(('whole-Newton-term-deletion',json.dumps(z)))
            z=json.loads(json.dumps(base));z['schema']=True;damages.append(('boolean-for-integer',json.dumps(z)))
            damages.append(('duplicate-key','{"schema":1,'+json.dumps(base)[1:]))
            for name,text in damages:
                path=T/(name+'.json');path.write_text(text)
                rows.append({'case':name,'optimized':optimized,**run(cmd+[str(T/'core.py'),str(path)],T,False)})
    record={'agent':'six-reviewer-1','role':'independent mathematical reviewer','status':'PASS','producer_inputs':False,'fixed_child_timeout_seconds':45,'serial_native_threads':1,'runs':rows,'total_runs':len(rows),'peak_children_kib':max(r['peak_children_kib']for r in rows),'maximum_seconds':max(r['seconds']for r in rows),'limits_raised':False}
    (D/'PRIMARY_VALIDATION.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items()if k!='runs'},sort_keys=True))
if __name__=='__main__':main()
