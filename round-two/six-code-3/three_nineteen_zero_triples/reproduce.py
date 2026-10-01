"""Bounded sequential source and independent-certificate reproduction."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent


def require(ok,message):
    if not ok:
        raise ValueError(message)


def run(work,reuse=False):
    work=work.resolve();work.mkdir(parents=True,exist_ok=True)
    environment=dict(os.environ)
    for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
        environment[key]='1'
    expected=json.loads((HERE/'expected.json').read_text())
    stages=[]
    started=time.monotonic()
    def child(name,arguments,seconds,optimized=False):
        command=[sys.executable,'-B']+(['-O'] if optimized else [])
        command += [str(HERE/name)]+arguments
        start=time.monotonic()
        completed=subprocess.run(command,env=environment,text=True,capture_output=True,
                                 timeout=seconds,check=False)
        log=work/f'run-{len(stages)}.log'
        log.write_text(completed.stdout+completed.stderr)
        require(completed.returncode==0,'INCOMPLETE source check; see '+str(log))
        lines=[json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
        require(bool(lines),'missing source-check record')
        stages.append({'command':command,'seconds':time.monotonic()-start,'result':lines[-1]})
        print(json.dumps({'stage':name,'optimized':optimized,'seconds':stages[-1]['seconds'],
                          'result':lines[-1]}),flush=True)
        return lines[-1]
    if not reuse:
        child('produce.py',['--work',str(work)],90)
    summary=json.loads((work/'summary.json').read_text())
    require(summary==expected['enumeration'],'whole primary summary mismatch')
    for k in range(6):
        result=child('verify.py',['--work',str(work),'--cases',str(k)],70)
        require(result['status']=='COMPLETE_ENTRYWISE' and result['cases']==[k],
                'wrong independent case coverage')
    capacity=child('verify_capacity.py',['--work',str(work)],30)
    require(capacity==expected['capacity'],'exact capacity result mismatch')
    optimized=child('verify_capacity.py',['--work',str(work)],30,True)
    require(optimized==capacity,'normal/optimized integer capacity disagreement')
    controls=child('controls.py',['--work',str(work)],30,True)
    require(controls==expected['controls'],'control result mismatch')
    result={'status':'COMPLETE','python':platform.python_version(),'platform':platform.platform(),
            'threads':1,'intensive_jobs':1,'seconds':time.monotonic()-started,
            'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'reused_primary_carrier':reuse,'stages':stages,
            'expected_sha256':hashlib.sha256((HERE/'expected.json').read_bytes()).hexdigest(),
            'capacity_sha256':hashlib.sha256((HERE/'capacity.json').read_bytes()).hexdigest()}
    (work/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='stages'}),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--reuse-primary',action='store_true',
                        help='Continue independent stages after a completed primary run')
    args=parser.parse_args()
    run(args.work,args.reuse_primary)
