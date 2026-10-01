"""Sequential bounded reproduction, or explicit reuse of own complete checkpoints."""
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
CASE_SOURCES=('produce.py','verify.py','native.py','clique_server.cpp')


def require(ok,message):
    if not ok:
        raise ValueError(message)


def fingerprint():
    return {name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in CASE_SOURCES}


def seal(work):
    checks=[json.loads((work/f'verified-case-{case}.json').read_text()) for case in range(40)]
    require(all(c['status']=='COMPLETE_ENTRYWISE' and c['case']==i for i,c in enumerate(checks)),
            'cannot seal incomplete case checks')
    result={'status':'COMPLETE_CASES','source_fingerprints':fingerprint(),
            'checkpoints':{str(i):hashlib.sha256((work/f'verified-case-{i}.json').read_bytes()).hexdigest()
                           for i in range(40)}}
    (work/'complete-case-checks.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')


def run(work,completed=False,reuse_primary=False):
    work=work.resolve();work.mkdir(parents=True,exist_ok=True)
    environment=dict(os.environ)
    for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
        environment[name]='1'
    environment['ASAN_OPTIONS']='detect_leaks=1'
    environment['UBSAN_OPTIONS']='halt_on_error=1'
    expected=json.loads((HERE/'expected.json').read_text())
    stages=[];started=time.monotonic()
    def command(name,arguments,seconds,optimized=False):
        cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(HERE/name)]+arguments
        start=time.monotonic()
        result=subprocess.run(cmd,text=True,capture_output=True,env=environment,timeout=seconds)
        log=work/f'reproduction-{len(stages)}.log';log.write_text(result.stdout+result.stderr)
        require(result.returncode==0,'INCOMPLETE source check; see '+str(log))
        rows=[json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        require(bool(rows),'missing completion record')
        stages.append({'command':cmd,'seconds':time.monotonic()-start,'result':rows[-1]})
        print(json.dumps({'stage':name,'optimized':optimized,'result':rows[-1]}),flush=True)
        return rows[-1]
    def compile_native(output,sanitized=False):
        cmd=['g++','-std=c++17','-O1' if sanitized else '-O2','-Wall','-Wextra','-Wpedantic']
        if sanitized:cmd+=['-g','-fno-omit-frame-pointer','-fsanitize=address,undefined']
        cmd+=[str(HERE/'clique_server.cpp'),'-o',str(output)]
        result=subprocess.run(cmd,text=True,capture_output=True,env=environment,timeout=40)
        (work/('sanitized-build.log' if sanitized else 'native-build.log')).write_text(result.stdout+result.stderr)
        require(result.returncode==0,'INCOMPLETE native source build')
    executable=work/'clique_server'
    compile_native(executable)
    if completed:
        marker=json.loads((work/'complete-case-checks.json').read_text())
        require(marker['status']=='COMPLETE_CASES' and marker['source_fingerprints']==fingerprint(),
                'complete checks belong to different source')
        for case in range(40):
            require(marker['checkpoints'][str(case)]==hashlib.sha256((work/f'verified-case-{case}.json').read_bytes()).hexdigest(),
                    'changed completed checkpoint')
    elif not reuse_primary:
        for case in range(40):command('produce.py',['--work',str(work),'--case',str(case)],70)
        command('produce.py',['--work',str(work),'--summarize'],20)
    require(json.loads((work/'summary.json').read_text())==expected['enumeration'],'whole primary summary mismatch')
    for case in range(40):
        if completed:
            record=json.loads((work/f'verified-case-{case}.json').read_text())
        else:
            record=command('verify.py',['--work',str(work),'--executable',str(executable),'--case',str(case)],70)
        target=expected['enumeration']['cases'][case]
        require(record['status']=='COMPLETE_ENTRYWISE' and record['case']==case and
                record['header_sha256']==target['header_sha256'] and record['joints_sha256']==target['joints_sha256'] and
                record['cores']==target['joint_count'],'independent case coverage mismatch')
        require(all(target['counts'][key]==value for key,value in record['counts'].items()),'independent case census mismatch')
    seal(work)
    for optimized in (False,True):
        result=command('verify_residual.py',['--work',str(work)],70,optimized)
        require(result==expected['residual'],'normal/optimized exact certificate mismatch')
    result=command('controls.py',['--work',str(work),'--executable',str(executable)],40,True)
    require(result==expected['controls'],'literal control mismatch')
    sanitized=work/'clique_server_sanitized'
    compile_native(sanitized,True)
    command('verify.py',['--work',str(work),'--executable',str(sanitized),'--case','0'],70)
    seal(work)
    compiler=subprocess.run(['g++','--version'],text=True,capture_output=True,timeout=5,check=True).stdout.splitlines()[0]
    record={'status':'COMPLETE','python':platform.python_version(),'compiler':compiler,
            'platform':platform.platform(),'threads':1,'intensive_jobs':1,
            'reused_primary':completed or reuse_primary,'reused_complete_case_checks':completed,
            'seconds':time.monotonic()-started,'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'case_source_fingerprints':fingerprint(),'expected_sha256':hashlib.sha256((HERE/'expected.json').read_bytes()).hexdigest(),
            'residual_sha256':hashlib.sha256((HERE/'residual.json').read_bytes()).hexdigest(),'stages':stages}
    (work/'validation.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k!='stages'}),flush=True)
    return record


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--reuse-primary',action='store_true',help='Reuse a complete primary carrier; repeat all independent checks')
    parser.add_argument('--completed-cases',action='store_true',help='Explicitly reuse own sealed complete case checks; no new case enumeration')
    args=parser.parse_args()
    run(args.work,args.completed_cases,args.reuse_primary)
