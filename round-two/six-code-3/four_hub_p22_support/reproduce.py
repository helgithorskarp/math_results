"""Fresh public-source reconstruction; serial, native threads1, 60s stages."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import time

def need(condition,message):
    if not condition:raise ValueError(message)

def strip_timing(x):
    if isinstance(x,dict):return {k:strip_timing(v) for k,v in x.items() if k!='elapsed_seconds'}
    if isinstance(x,list):return [strip_timing(v) for v in x]
    return x

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args();source=Path(__file__).resolve().parent;work=args.work.resolve()
    need(not work.exists(),'fresh replay directory required')
    expected=json.loads((source/'EXPECTED.json').read_text())
    files=list((source/'source').glob('*.py'))+list((source/'baseline').iterdir())+[source/'EXPECTED.json']
    seal={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    work.mkdir(parents=True)
    root=Path('round-two/six-code-3');scratch=root/'scratch';baseline=root/'four_hub_p21_endpoint_cut'
    for p in files:
        if p.parent.name=='source':target=work/scratch/p.name
        elif p.parent.name=='baseline':target=work/baseline/p.name
        else:continue
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    env=dict(os.environ)
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        env[key]='1'
    env['PYTHONDONTWRITEBYTECODE']='1'
    interpreter=[sys.executable]+(['-O'] if sys.flags.optimize else [])
    begun=time.monotonic();steps=[]
    for name in expected['stages']:
        started=time.monotonic()
        result=subprocess.run(interpreter+[str(scratch/(name+'.py'))],cwd=work,env=env,capture_output=True,text=True,timeout=60)
        (work/(name+'.stdout')).write_text(result.stdout);(work/(name+'.stderr')).write_text(result.stderr)
        need(result.returncode==0,'failed/incomplete stage is not mathematical absence: '+name+'\n'+result.stderr)
        steps.append(dict(stage=name,elapsed_seconds=time.monotonic()-started))
        print(json.dumps(dict(stage=name,status='PASS')),flush=True)
    whole={}
    for name in expected['outputs']:
        data=strip_timing(json.loads((work/scratch/(name+'.json')).read_text()))
        need(hashlib.sha256(canonical(data)).hexdigest()==expected['mathematical_output_sha256'][name],
             'whole mathematical stage output differs: '+name)
        whole[name]=data
    raw=canonical(whole)+b'\n';digest=hashlib.sha256(raw).hexdigest()
    need(digest==expected['whole_mathematical_sha256'],'entire mathematical record differs')
    need(seal=={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'source/input changed during replay')
    (work/'MATHEMATICAL.json').write_bytes(raw)
    validation=dict(agent='six-code-3',role='researcher',status='PUBLIC_SOURCE_COMPLETE_REPLAY_PASS',
                    mode='optimized' if sys.flags.optimize else 'normal',python=sys.version,
                    complete_mathematical_sha256=digest,whole_records_matched=len(whole),
                    elapsed_seconds=time.monotonic()-begun,peak_RUSAGE_CHILDREN_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                    native_threads=1,serial_children=True,stage_timeout_seconds=60,stages=steps,source_seal=seal,
                    independent_peer_review=False,ordinary_bridges_formalized=False)
    (work/'VALIDATION.json').write_text(json.dumps(validation,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in validation.items() if k not in ('source_seal','stages','python')},sort_keys=True))

if __name__=='__main__':main()
