"""Source-gated serial normal/-O reproduction, with real child waits."""
from pathlib import Path
from hashlib import sha256
import argparse,json,os,subprocess,sys,time

def require(ok,msg):
    if not ok:raise ValueError(msg)
def source_gate(root):
    expected={}
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        require(len(digest)==64 and len(name)>0 and '/' not in name and name not in expected,'source manifest schema')
        expected[name]=digest
    actual={p.name for p in root.iterdir() if p.is_file()}
    require(actual==set(expected)|{'SHA256SUMS'},'entire publication file census')
    for name,digest in expected.items():require(sha256((root/name).read_bytes()).hexdigest()==digest,'whole source bytes '+name)
    return len(actual)
def run(root,mode):
    env=dict(os.environ)
    for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[name]='1'
    expected=json.loads((root/'RESULTS.json').read_text());execution=[]
    for script,args in (('produce.py',[]),('check.py',['CERTIFICATE.json']),('control.py',[]),('damages.py',[])):
        command=[sys.executable,'-B']+(['-O'] if mode else [])+[script,*args]
        started=time.monotonic();p=subprocess.Popen(command,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        try:out,err=p.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            p.kill();out,err=p.communicate();raise TimeoutError('STOPPED60s; unfinished is not mathematics: '+script)
        require(p.returncode==0,'failed mathematical child '+script+': '+err)
        info=json.loads(out);execution.append({'program':script,'mode':mode,'exit_code':p.returncode,'actually_waited':True,'wall_seconds':time.monotonic()-started,'child':info})
        if script=='produce.py':require((root/'work/CERTIFICATE.json').read_bytes()==(root/'CERTIFICATE.json').read_bytes(),'EVERY regenerated certificate byte')
        print(json.dumps({'phase':script,'mode':mode,'completed':True}),flush=True)
    result={'certificate_sha256':sha256((root/'work/CERTIFICATE.json').read_bytes()).hexdigest(),
            'checker':json.loads((root/f'work/checker-O{mode}.json').read_text()),
            'controls':json.loads((root/f'work/controls-O{mode}.json').read_text()),
            'damages':json.loads((root/f'work/damages-O{mode}.json').read_text())}
    raw=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    require(result==expected and raw==(root/'RESULTS.json').read_bytes(),'EVERY complete mathematical result field and byte')
    (root/f'work/RESULTS-O{mode}.json').write_bytes(raw)
    return execution
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--both',action='store_true');args=parser.parse_args()
    root=Path(__file__).resolve().parent;state=Path('/scratch/research-team-sol61-six-20260929/state')
    require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational barrier')
    files=source_gate(root);execution=[]
    for mode in ((0,1) if args.both else (sys.flags.optimize,)):execution+=run(root,mode)
    source_gate(root)
    receipt={'status':'COMPLETE all source-gated serial replays','source_files':files,'modes':[0,1] if args.both else [sys.flags.optimize],'execution':execution,'max_child_seconds':max(x['child']['seconds'] for x in execution),'peak_KiB':max(x['child']['peak_KiB'] for x in execution),'certificate_sha256':sha256((root/'CERTIFICATE.json').read_bytes()).hexdigest(),'results_sha256':sha256((root/'RESULTS.json').read_bytes()).hexdigest(),'every_certificate_and_result_byte_equal':True,'child_seconds':60,'polynomial_terms':512,'packing_bytes':33554432,'native_threads':1,'serial_math_child':1}
    (root/'work/reproduction.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='execution'}),flush=True)
if __name__=='__main__':main()
