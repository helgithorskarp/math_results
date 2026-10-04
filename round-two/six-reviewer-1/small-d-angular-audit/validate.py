"""Bounded serial positive and intended-defect checks of this reviewer source."""
import hashlib,json,os,resource,shutil,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
          'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:
    os.environ[k]='1'
sys.path.insert(0,str(ROOT))
from verify import build
raw=(ROOT/'EXPECTED.json').read_bytes();expected=json.loads(raw)
positives=[];rejects=[]

def run(folder,opt):
    start=time.monotonic()
    result=subprocess.run([sys.executable,'-I','-B',*opt,str(folder/'check.py')],
                          capture_output=True,text=True,timeout=45,env=os.environ.copy())
    return result,time.monotonic()-start

for cold in [False,True]:
    with tempfile.TemporaryDirectory(prefix='independent-collar-')as td:
        dest=Path(td)if cold else ROOT
        if cold:
            for n in ['algebra.py','verify.py','check.py','EXPECTED.json','PRIMARY_SEAL.json']:
                shutil.copyfile(ROOT/n,dest/n)
        for opt in [[],['-O']]:
            result,secs=run(dest,opt)
            if result.returncode or json.loads(result.stdout)['sha256']!=hashlib.sha256(raw).hexdigest():
                raise ValueError('positive replay failed '+result.stderr)
            positives.append({'cold':cold,'optimized':bool(opt),'seconds':round(secs,6),
                              'complete_record':json.loads(result.stdout)})
for defect in ['drop-inverse-tail','underpay-root','underpay-Taylor',
               'omit-seven-remainders','wrong-bound-derivative','delete-original-position',
               'wrong-full-mass-normalization']:
    try:build(defect)
    except ValueError as e:rejects.append({'defect':defect,'rejected':True,'gate':str(e)})
    else:raise ValueError('intended mathematical defect escaped '+defect)
for defect in ['newline','changed-matrix','integer-type']:
    with tempfile.TemporaryDirectory(prefix='collar-fixture-defect-')as td:
        dest=Path(td)
        for n in ['algebra.py','verify.py','check.py','EXPECTED.json','PRIMARY_SEAL.json']:
            shutil.copyfile(ROOT/n,dest/n)
        data=raw
        if defect=='newline':data+=b'\n'
        else:
            d=json.loads(raw)
            if defect=='integer-type':d['gate_count']=float(d['gate_count'])
            else:d['gates'][-5]['value']='changed full mathematical payload'
            data=(json.dumps(d,sort_keys=True,indent=2)+'\n').encode()
        (dest/'EXPECTED.json').write_bytes(data)
        result,_=run(dest,[])
        if result.returncode==0 or 'entire deterministic expected record mismatch'not in result.stderr:
            raise ValueError('fixture defect failed wrong gate')
        rejects.append({'defect':defect,'rejected':True,'gate':'entire deterministic expected record mismatch'})
for name in ['algebra.py','verify.py']:
    with tempfile.TemporaryDirectory(prefix='collar-seal-defect-')as td:
        dest=Path(td)
        for n in ['algebra.py','verify.py','check.py','EXPECTED.json','PRIMARY_SEAL.json']:
            shutil.copyfile(ROOT/n,dest/n)
        (dest/name).write_bytes((dest/name).read_bytes()+b'\nraise RuntimeError("must not import")\n')
        result,_=run(dest,[])
        if result.returncode==0 or 'primary source seal '+name not in result.stderr:
            raise ValueError('preimport source binding failed')
        rejects.append({'defect':'preimport '+name,'rejected':True,'gate':'primary source seal '+name})
record={'agent':'six-reviewer-1','role':'independent mathematical reviewer',
        'python':sys.version.split()[0],'native_threads':1,'CPU_intensive_children_at_once':1,
        'fixed_child_timeout_seconds':45,'process_scope':'existing1CPU2GiB128tasks; unchanged',
        'record_bytes':len(raw),'record_sha256':hashlib.sha256(raw).hexdigest(),
        'gate_count':expected['gate_count'],'positives':positives,'intended_rejections':rejects,
        'max_child_seconds':max(p['seconds']for p in positives),
        'children_max_rss_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        'whole_record_compared':True,'ordinary_bridges_formalized':False,
        'target_author_executable_fixture_or_validation_used':False}
(ROOT/'VALIDATION.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items()if k not in ['positives','intended_rejections']},indent=2))
