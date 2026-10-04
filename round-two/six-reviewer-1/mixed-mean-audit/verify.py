"""Entire staged reconstruction; seals precede all local mathematical imports."""
from pathlib import Path
import sys,json,hashlib,signal,time,resource,subprocess,os
here=Path(__file__).resolve().parent
NAMES={'field.py','intervals.py','constants.py','series.py','family.py','root.py','scalar.py','controls.py'}
seal=json.loads((here/'PRIMARY_SEAL.json').read_text())
if set(seal)!= {'files'} or set(seal['files'])!=NAMES:raise ValueError('exact primary source census')
for n,h in seal['files'].items():
    if hashlib.sha256((here/n).read_bytes()).hexdigest()!=h:raise ValueError('source seal before import')
expected=json.loads((here/'EXPECTED.json').read_text())
keys={f'root-{j}-{t}'for t in range(2)for j in range(9)}|{'scalar-0','scalar-1','controls'}
if set(expected)!= {'stages','whole_bytes','whole_sha256'} or set(expected['stages'])!=keys:raise ValueError('exact entire expectation schema')
for row in expected['stages'].values():
    if set(row)!={'bytes','sha256'}or type(row['bytes'])is not int or row['bytes']<=0 or type(row['sha256'])is not str or len(row['sha256'])!=64:raise ValueError('entire stage expectation schema')
def encoded(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def checked(key,raw):
    r=expected['stages'][key]
    if len(raw)!=r['bytes']or hashlib.sha256(raw).hexdigest()!=r['sha256']:raise ValueError('entire regenerated stage record agreement '+key)
mode=sys.argv[1];start=time.monotonic()
if mode=='all':
    dest=Path(sys.argv[2]).resolve();dest.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy()
    for n in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:env[n]='1'
    rows={};metrics=[]
    for key in sorted(keys-{'controls'})+['controls']:
        out=dest/(key+'.json');cmd=[sys.executable,'-I','-B']+(['-O']if sys.flags.optimize else[])+[str(here/'verify.py'),'stage',key,str(out),str(dest)]
        p=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=45)
        if p.returncode:raise ValueError('bounded entire child failed '+key+' '+p.stderr)
        data=out.read_bytes();checked(key,data);rows[key]=json.loads(data);metrics.append(json.loads(p.stdout))
    raw=encoded(rows)
    if len(raw)!=expected['whole_bytes']or hashlib.sha256(raw).hexdigest()!=expected['whole_sha256']:raise ValueError('entire combined record agreement')
    (dest/'whole.json').write_bytes(raw)
    print(json.dumps({'whole_bytes':len(raw),'whole_sha256':hashlib.sha256(raw).hexdigest(),'stage_count':len(metrics),'whole_equations_before_digests':True,'seconds':round(time.monotonic()-start,6),'maximum_child_seconds':max(m['seconds']for m in metrics),'maximum_child_peak_RSS_KiB':max(m['peak_RSS_KiB']for m in metrics),'metrics':metrics}))
elif mode=='stage':
    signal.alarm(45);key=sys.argv[2];out=Path(sys.argv[3]);sys.path.insert(0,str(here))
    if key.startswith('root-'):
        from root import run
        _,j,t=key.split('-');record=run(int(j),int(t))
    elif key.startswith('scalar-'):
        from scalar import run
        record=run(int(key.split('-')[1]))
    elif key=='controls':
        from controls import run
        dest=Path(sys.argv[4]);record=run([[json.loads((dest/f'root-{j}-{t}.json').read_text())for j in range(9)]for t in range(2)],[json.loads((dest/f'scalar-{t}.json').read_text())for t in range(2)])
    else:raise ValueError('unknown stage')
    for n in NAMES:
        name=n[:-3]
        if name in sys.modules and Path(sys.modules[name].__file__).resolve()!=here/n:raise ValueError('local mathematical import origin')
    raw=encoded(record);checked(key,raw);out.write_bytes(raw)
    print(json.dumps({'stage':key,'seconds':round(time.monotonic()-start,6),'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}))
else:raise ValueError('unknown mode')
