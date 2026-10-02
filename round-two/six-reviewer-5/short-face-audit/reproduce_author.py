"""Optional pinned native replay, then the independent late certificate audit."""
from pathlib import Path
import argparse,urllib.request,json,hashlib,os,subprocess,sys,time,resource
import compare_author

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--scratch',type=Path,required=True);args=parser.parse_args()
    p=Path(__file__).resolve().parent;directory=args.scratch.resolve()
    directory.mkdir(parents=True,exist_ok=True)
    if any(directory.iterdir()):raise ValueError('use a fresh empty scratch directory')
    source=json.loads((p/'AUTHOR_SOURCE.json').read_text());sha=source['commit']
    for row in source['files']:
        url='https://raw.githubusercontent.com/helgithorskarp/math_results/'+sha+'/'+row['path']
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'independent-short-face-replay'}),timeout=20) as response:raw=response.read()
        if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:raise ValueError('wrong source bytes:'+row['name'])
        (directory/row['name']).write_bytes(raw)
    env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
    runs=[]
    for mode in ('normal','optimized'):
        for name in ('check.py','audit.py','controls.py'):
            started=time.monotonic()
            child=subprocess.run([sys.executable,'-B']+(['-O'] if mode=='optimized' else [])+[str(directory/name)],cwd=directory,env=env,capture_output=True,timeout=45)
            if child.returncode:raise ValueError(child.stderr.decode())
            runs.append(dict(mode=mode,program=name,result=json.loads(child.stdout),seconds=time.monotonic()-started))
    for name in ('check.py','audit.py','controls.py'):
        pair=[r['result'] for r in runs if r['program']==name]
        if pair[0]!=pair[1]:raise ValueError('native mode disagreement:'+name)
    for row in source['files']:
        if hashlib.sha256((directory/row['name']).read_bytes()).hexdigest()!=row['sha256']:raise ValueError('changed native source:'+row['name'])
    raw=(directory/'CERTIFICATE.json').read_bytes();data=json.loads(raw)
    result=dict(pinned_commit=sha,native_source_files=len(source['files']),strictly_serial_native_stages=len(runs),
        native_normal_optimized_match=True,certificate_sha256=hashlib.sha256(raw).hexdigest(),
        independent_comparison=compare_author.verify(data),independent_damage_controls=compare_author.controls(data),
        maximum_native_seconds=max(r['seconds'] for r in runs),max_native_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
