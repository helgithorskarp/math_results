"""Cold source-only reconstruction: serial children, native threads1."""
import argparse, hashlib, json, os, resource, shutil, subprocess, sys, time
from pathlib import Path

def need(c,m):
    if not c:raise ValueError(m)
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def strip_timing(x):
    if isinstance(x,dict):return {k:strip_timing(v) for k,v in x.items() if k!='elapsed_seconds'}
    if isinstance(x,list):return [strip_timing(v) for v in x]
    return x

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,required=True);args=parser.parse_args()
    source=Path(__file__).resolve().parent;work=args.work.resolve();need(not work.exists(),'fresh work directory required')
    expected=json.loads((source/'EXPECTED.json').read_text())
    files=list((source/'source').glob('*.py'))+list((source/'baseline').iterdir())+[source/'EXPECTED.json']
    seal={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    R=Path('round-two/six-code-3');S=R/'scratch';B=R/'four_hub_p21_endpoint_cut';work.mkdir(parents=True)
    for p in files:
        if p.parent.name=='source':target=work/S/p.name
        elif p.parent.name=='baseline':target=work/B/p.name
        else:continue
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    interpreter=[sys.executable]+(['-O'] if sys.flags.optimize else [])
    env=dict(os.environ)
    for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS']:env[k]='1'
    env['PYTHONDONTWRITEBYTECODE']='1'
    stages=[];start=time.monotonic()
    for step in expected['stages']:
        begun=time.monotonic();name=step['name']
        cmd=interpreter+[str(S/(name+'.py'))]+step.get('arguments',[])
        result=subprocess.run(cmd,cwd=work,env=env,capture_output=True,text=True,timeout=60)
        (work/(name+'.stdout')).write_text(result.stdout);(work/(name+'.stderr')).write_text(result.stderr)
        need(result.returncode==0,'failed/incomplete stage is not mathematical absence: '+name+'\n'+result.stderr)
        stages.append(dict(stage=name,elapsed_seconds=time.monotonic()-begun))
        print(json.dumps(dict(stage=name,status='PASS')),flush=True)
    whole={}
    for name in expected['outputs']:
        data=json.loads((work/S/(name+'.json')).read_text())
        if name=='pass20-independent-full-T2-N':
            need(data['author_result_sha256']==hashlib.sha256((work/S/'pass20-full-T2-N-producer.json').read_bytes()).hexdigest(),'raw independent author provenance checked before mathematical normalization')
            data={k:v for k,v in data.items() if k!='author_result_sha256'}
        normalized=strip_timing(data);digest=hashlib.sha256(canonical(normalized)).hexdigest()
        need(digest==expected['mathematical_output_sha256'][name],'entire mathematical output differs: '+name)
        whole[name]=normalized
    raw=canonical(whole)+b'\n';digest=hashlib.sha256(raw).hexdigest()
    need(digest==expected['whole_mathematical_sha256'],'whole mathematical record differs')
    need(seal=={str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'source/input changed during replay')
    (work/'MATHEMATICAL.json').write_bytes(raw)
    validation=dict(agent='six-code-3',role='researcher',status='PUBLIC_SOURCE_COMPLETE_T2_REPLAY_PASS',mode='optimized' if sys.flags.optimize else 'normal',python=sys.version,complete_mathematical_sha256=digest,whole_records_matched=len(whole),elapsed_seconds=time.monotonic()-start,peak_RUSAGE_CHILDREN_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,native_threads=1,serial_children=True,stage_timeout_seconds=60,stages=stages,source_seal=seal,independent_person_review=False,ordinary_bridges_formalized=False)
    (work/'VALIDATION.json').write_text(json.dumps(validation,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in validation.items() if k not in ['source_seal','stages','python']},sort_keys=True))
if __name__=='__main__':main()
