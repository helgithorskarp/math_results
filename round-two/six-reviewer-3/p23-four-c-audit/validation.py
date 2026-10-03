"""Serial source-only normal/O checks and semantic damage controls, guard45s."""
import subprocess,tempfile,json,hashlib,time,resource,os,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
def run(script,*args,opt=False,valid=True):
    env=os.environ.copy()
    for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS']:env[k]='1'
    cmd=[sys.executable,'-B']+(['-O'] if opt else [])+[str(BASE/script),*map(str,args)]
    t=time.monotonic();p=subprocess.run(cmd,capture_output=True,env=env,timeout=45)
    if (p.returncode==0)!=valid:raise ValueError('unexpected child outcome: '+p.stderr.decode()[:500])
    return p.stdout,time.monotonic()-t
with tempfile.TemporaryDirectory() as td:
    root=Path(td);outputs=[];runs=[];controls=[]
    for opt in [False,True]:
        d=root/('optimized' if opt else 'normal')
        b,t=run('produce.py',d,opt=opt);runs.append({'script':'produce','optimized':opt,'seconds':t})
        check,t=run('check.py',d,opt=opt);runs.append({'script':'check','optimized':opt,'seconds':t});outputs.append((b,check,(d/'flags.bin').read_bytes(),(d/'records.json').read_bytes()))
        original=json.loads((d/'records.json').read_text());flags=(d/'flags.bin').read_bytes()
        for label in ['lost_positive','false_flag','lost_case','duplicate_edge','bad_edge','false_capacity','lost_equality','false_support']:
            packet=json.loads(json.dumps(original));bits=flags
            if label=='lost_positive':packet['records'].pop()
            elif label=='false_flag':bits=bytes([1-flags[0]])+flags[1:]
            elif label=='lost_case':bits=flags[:-1]
            elif label=='duplicate_edge':packet['records'][0]['witness'][0]=[0,0]
            elif label=='bad_edge':packet['records'][0]['witness'][0]=[6]
            elif label=='false_capacity':packet['records'][0]['witness']=[[0,1,2]]*4
            elif label=='lost_equality':packet['equality'].pop()
            elif label=='false_support':packet['records'][0]['n'][0]-=1
            (d/'flags.bin').write_bytes(bits);(d/'records.json').write_text(json.dumps(packet,sort_keys=True,separators=(',',':'))+'\n')
            _,t=run('check.py',d,opt=opt,valid=False);runs.append({'script':label,'optimized':opt,'seconds':t});controls.append({'damage':label,'optimized':opt,'rejected':True})
        (d/'flags.bin').write_bytes(flags);(d/'records.json').write_text(json.dumps(original,sort_keys=True,separators=(',',':'))+'\n')
    if outputs[0]!=outputs[1]:raise ValueError('whole normal/O mismatch')
    result=json.loads(outputs[0][1]);result.update({'python':sys.version.split()[0],'independent_primary_modes':2,'semantic_controls':controls,'child_runs':runs,'whole_mode_bytes_identical':True,'guard_seconds_per_child':45,'threads':1,'peak_child_rss_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
    print(json.dumps(result,indent=2,sort_keys=True))
