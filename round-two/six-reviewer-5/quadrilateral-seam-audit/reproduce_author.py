"""Optional pinned native reproduction, strictly serial; no author files published here."""
import argparse,hashlib,json,os,pathlib,subprocess,sys,urllib.request
P=pathlib.Path(__file__).resolve().parent
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=pathlib.Path,required=True);args=ap.parse_args()
    if args.work.exists():raise ValueError('choose a fresh work directory')
    args.work.mkdir(parents=True);pin=json.loads((P/'AUTHOR-PINS.json').read_text())
    for row in pin['files']:
        url='https://raw.githubusercontent.com/helgithorskarp/math_results/'+pin['commit']+'/'+pin['base']+'/'+row['name']
        b=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'six-reviewer-5 exact native replay'}),timeout=20).read()
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:raise ValueError('entire pinned source mismatch')
        (args.work/row['name']).write_bytes(b)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[k]='1'
    for mode in ([],['-O']):
        for n in ('check.py','audit.py','controls.py'):
            r=subprocess.run([sys.executable]+mode+['-B',str((args.work/n).resolve())],cwd=args.work,env=env,capture_output=True,text=True,timeout=45)
            if r.returncode:raise ValueError('incomplete or failed native replay: '+r.stderr)
    r=subprocess.run([sys.executable,'-B',str(P/'compare_author.py'),'--author-dir',str(args.work.resolve())],env=env,capture_output=True,text=True,timeout=45)
    if r.returncode:raise ValueError('full independent comparison: '+r.stderr)
    print(r.stdout.strip())
if __name__=='__main__':main()
