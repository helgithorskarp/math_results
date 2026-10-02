"""Optional pinned author replay. No author helper enters independent audit."""
import argparse,hashlib,json,os,pathlib,subprocess,sys,urllib.request
P=pathlib.Path(__file__).resolve().parent
def need(ok,message):
    if not ok:raise ValueError(message)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=pathlib.Path,required=True);args=ap.parse_args();work=args.work.resolve()
    need(not work.exists(),'fresh work directory required');work.mkdir(parents=True)
    source=json.loads((P/'target-source.json').read_text());base=pathlib.PurePosixPath(source['base']);root=work/'author';root.mkdir()
    for f in source['files']:
        rel=pathlib.PurePosixPath(f['path']).relative_to(base);need('..' not in rel.parts,'source path')
        url='https://raw.githubusercontent.com/helgithorskarp/math_results/'+source['commit']+'/'+f['path']
        with urllib.request.urlopen(url,timeout=20) as r:raw=r.read()
        need(len(raw)==f['bytes'] and hashlib.sha256(raw).hexdigest()==f['sha256'],'pinned author bytes')
        target=root/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[key]='1'
    for mode,flags in (('normal',[]),('optimized',['-O'])):
        r=subprocess.run([sys.executable]+flags+['-B',str(root/'reproduce.py'),'--work',str(work/mode)],env=env,capture_output=True,text=True,timeout=45)
        need(r.returncode==0,'incomplete author replay is not mathematical absence: '+r.stderr)
    need((work/'normal/MATHEMATICAL.json').read_bytes()==(work/'optimized/MATHEMATICAL.json').read_bytes(),'every native normal/O record')
    print(json.dumps(dict(status='PASS',whole_native_sha256=hashlib.sha256((work/'normal/MATHEMATICAL.json').read_bytes()).hexdigest(),ordinary_bridges_formalized=False,independent_checker=False)))
if __name__=='__main__':main()
