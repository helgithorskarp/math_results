"""Four whole-byte replays and deliberately defective mathematical gates."""
from pathlib import Path
import subprocess,json,sys,os,tempfile,shutil,hashlib,time
here=Path(__file__).resolve().parent
dest=Path(sys.argv[1]).resolve();dest.mkdir(parents=True,exist_ok=True)
env=os.environ.copy()
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:env[name]='1'
records=[];reference=None
def run(folder,optimized,name,positive=True,required=''):
    global reference
    out=dest/(name+'.json');cmd=[sys.executable,'-I','-B']+(['-O']if optimized else[])+[str(folder/'verify.py'),str(out)]
    start=time.monotonic();p=subprocess.run(cmd,capture_output=True,text=True,env=env,timeout=45)
    record={'name':name,'optimized':optimized,'seconds':round(time.monotonic()-start,6),'returncode':p.returncode}
    if positive:
        if p.returncode:raise ValueError('positive full replay failed '+p.stderr)
        data=out.read_bytes()
        if reference is None:reference=data
        if data!=reference:raise ValueError('four complete records differ')
        record.update(json.loads(p.stdout));record['whole_bytes_equal']=True
    else:
        if p.returncode==0 or required not in p.stderr:raise ValueError('intended mathematical rejection failed '+name+' '+p.stderr)
        record.update(intended_gate=required,rejected=True)
    records.append(record)
for opt in [False,True]:run(here,opt,'local-'+('optimized'if opt else'normal'))
with tempfile.TemporaryDirectory(prefix='central-double-cold-')as tmp:
    cold=Path(tmp)
    for p in here.iterdir():
        if p.is_file():shutil.copyfile(p,cold/p.name)
    for opt in [False,True]:run(cold,opt,'cold-'+('optimized'if opt else'normal'))
faults=[
 ('original-derivative','integers.py','scale(D,-16)','scale(D,-15)','whole original derivative identity'),
 ('original-norm','integers.py','r[-1]!=constant(64)','r[-1]!=constant(63)','complete degree-five norm-one residue'),
 ('mass-first-coefficient','integers.py','R=bezout(H,r);det=','R=bezout(H,[scale(v,2)for v in r]);det=','complete determinant first mass coefficient'),
 ('cap-clearing','integers.py','8**(I-i+k)','8**(I-i+k+1)','complete independently reconstructed written minima'),
 ('cap-q-factor','integers.py','(e[0]-20,e[1],e[2])','(e[0]-19,e[1],e[2])','whole reduced cap degree'),
 ('tensor-control','integers.py','controls=a\n    b=a','controls=a\n    a=a.copy();a[(0,0,0)]+=1\n    b=a','entire reverse tensor coefficient identity'),
 ('original-reality','controls.py','Q(1,10**9)','Q(1,10)','actual six simple real originals and all active criticals'),
 ('quantitative-constant','controls.py','c<=Q(1,2**106)','c<=Q(1,2**100)','new quantitative central margin')]
for name,file,old,new,gate in faults:
    with tempfile.TemporaryDirectory(prefix='central-double-fault-')as tmp:
        fault=Path(tmp)
        for p in here.iterdir():
            if p.is_file():shutil.copyfile(p,fault/p.name)
        text=(fault/file).read_text()
        if old not in text:raise ValueError('exact fault location absent '+name)
        (fault/file).write_text(text.replace(old,new,1))
        # Reseal defective source so the named mathematical gate must reject it.
        seal={'files':{n:hashlib.sha256((fault/n).read_bytes()).hexdigest()for n in ['integers.py','controls.py','check.py']}}
        (fault/'PRIMARY_SEAL.json').write_text(json.dumps(seal))
        for opt in [False,True]:run(fault,opt,name+('-optimized'if opt else'-normal'),False,gate)
with tempfile.TemporaryDirectory(prefix='central-double-unsealed-')as tmp:
    fault=Path(tmp)
    for p in here.iterdir():
        if p.is_file():shutil.copyfile(p,fault/p.name)
    (fault/'integers.py').write_text('raise RuntimeError("IMPORTED DEFECTIVE SOURCE")\n'+(fault/'integers.py').read_text())
    for opt in [False,True]:run(fault,opt,'preimport-seal-'+str(opt),False,'source seal before import')
summary={'agent':'six-reviewer-1','role':'independent mathematical reviewer','four_entire_records_equal':True,
 'mathematical_defects_rejected':16,'preimport_seal_rejections':2,'native_threads':1,'maximum_concurrent_CPU_children':1,
 'per_child_timeout_seconds':45,'resource_limit_hit':False,'records':records}
(dest/'VALIDATION.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items()if k!='records'}))
