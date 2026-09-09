"""Fresh complete replay with externally stored catalogues and profiles."""
from pathlib import Path
import argparse,gzip,hashlib,json,platform,subprocess,sys,time,urllib.request
HERE=Path(__file__).resolve().parent
def need(ok,why):
    if not ok:raise ValueError(why)
def stable(obj):
    if isinstance(obj,dict):return {k:stable(v) for k,v in obj.items() if k!='seconds'}
    if isinstance(obj,list):return list(map(stable,obj))
    return obj
def inputs(data,fetch):
    data.mkdir(parents=True,exist_ok=True)
    for item in json.loads((HERE/'INPUTS.json').read_text()):
        file=data/item['file']
        if not file.exists():
            need(fetch,'missing '+str(file)+'; provide pinned data or --fetch')
            with urllib.request.urlopen(item['url'],timeout=60) as r:raw=r.read()
            need(hashlib.sha256(raw).hexdigest()==item['download_sha256'],'download identity')
            body=gzip.decompress(raw) if item['url'].endswith('.gz') else raw
            need(hashlib.sha256(body).hexdigest()==item['sha256'],'decompressed catalogue identity');file.write_bytes(body)
        need(hashlib.sha256(file.read_bytes()).hexdigest()==item['sha256'],'catalogue hash')
def run(data,out,fetch=False):
    data,out=Path(data).resolve(),Path(out).resolve();inputs(data,fetch);out.mkdir();start=time.monotonic()
    def call(args,label):
        with (out/(label+'.log')).open('xb') as f:r=subprocess.run(list(map(str,args)),stdout=f,stderr=subprocess.STDOUT)
        need(r.returncode==0,'failed '+label+'; inspect '+str(out/(label+'.log')))
        print(json.dumps(dict(completed=label,seconds=time.monotonic()-start)),flush=True)
    for mode,flags in [('release',['-O3']),('sanitized',['-O1','-g','-fno-omit-frame-pointer','-fsanitize=address,undefined'])]:
        for name in ('produce','independent'):
            label='build-'+name+'-'+mode
            call(['g++','-std=c++20','-Wall','-Wextra','-Wpedantic',*flags,HERE/(name+'.cpp'),'-o',out/(name+'-'+mode)],label)
            need((out/(label+'.log')).stat().st_size==0,'compiler warnings')
    python=[sys.executable,'-B']
    call(python+[HERE/'census.py',data,out/'census',out/'produce-release',out/'independent-release'],'census')
    call(python+[HERE/'global_bound.py',out/'census',data,out/'GLOBAL.json'],'global')
    call(python+[HERE/'sanitize.py',data,out/'census',out/'sanitizer',out/'produce-sanitized',out/'independent-sanitized'],'sanitizer')
    results=[]
    for optimized in (False,True):
        tag='optimized' if optimized else 'normal';p=[sys.executable]+(['-O'] if optimized else [])+['-B'];native='sanitized' if optimized else 'release'
        call(p+[HERE/'verify_global.py',out/'census',data,out/'GLOBAL.json'],tag+'-arithmetic')
        call(p+[HERE/'corruptions.py',out/'census',data,out/'GLOBAL.json',out/(tag+'-corruptions')],tag+'-corruptions')
        call(p+[HERE/'validate.py',out/(tag+'-literal'),out/('produce-'+native),out/('independent-'+native)],tag+'-literal')
        call(p+[HERE/'physical_controls.py',data,out/(tag+'-physical')],tag+'-physical')
        results.append(stable(dict(census=json.loads((out/'census/CENSUS.json').read_text()),global_bound=json.loads((out/'GLOBAL.json').read_text()),
            independent=json.loads((out/(tag+'-arithmetic.log')).read_text()),global_corruptions=json.loads((out/(tag+'-corruptions.log')).read_text()),
            literal=json.loads((out/(tag+'-literal/VALIDATION.json')).read_text()),physical=json.loads((out/(tag+'-physical/PHYSICAL.json')).read_text()),
            sanitized=json.loads((out/'sanitizer/SANITIZED.json').read_text()))))
    need(results[0]==results[1],'normal/-O evidence differs')
    need(results[0]==json.loads((HERE/'EXPECTED.json').read_text()),'public expected result differs')
    need((out/'normal-physical/FIXTURES.json').read_bytes()==(HERE/'FIXTURES.json').read_bytes(),'public fixture bytes')
    (out/'RESULT.json').write_text(json.dumps(results[0],sort_keys=True,indent=2)+'\n')
    result=dict(status='REPRODUCED_COMPLETE_MAXIMAL_RESIDUAL_BOUND',gate=results[0]['global_bound']['gate'],seconds=time.monotonic()-start,
                result_sha256=hashlib.sha256((out/'RESULT.json').read_bytes()).hexdigest(),python=sys.version,platform=platform.platform(),
                solver_calls=0,new_task_decisions=0,q10_child_inputs_inspected=0,target_found=False)
    (out/'REPLAY.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--data',required=True);p.add_argument('--out',required=True);p.add_argument('--fetch',action='store_true');a=p.parse_args()
    print(json.dumps(run(a.data,a.out,a.fetch),sort_keys=True))
