"""Optional exact pinned native replay followed by data-only comparison.
The independently sealed core does not need this downloaded source.
"""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys,urllib.request

def main():
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--own',type=Path,required=True);p.add_argument('--physical',type=Path,required=True);a=p.parse_args()
    root=Path(__file__).resolve().parent;work=a.work.resolve()
    if work.exists():raise ValueError('fresh work required')
    source=work/'source';source.mkdir(parents=True)
    pin=json.loads((root/'AUTHOR_SOURCE.json').read_bytes())
    for n,v in pin['files'].items():
        url='https://raw.githubusercontent.com/helgithorskarp/math_results/'+pin['commit']+'/'+pin['prefix']+n
        with urllib.request.urlopen(url,timeout=20)as response:raw=response.read()
        if hashlib.sha256(raw).hexdigest()!=v['sha256']:raise ValueError('whole source SHA mismatch '+n)
        q=source/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
    env=dict(os.environ)
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[k]='1'
    env['PYTHONDONTWRITEBYTECODE']='1'
    for mode in ('normal','optimized'):
        target=work/mode
        interpreter=[sys.executable]+(['-O']if mode=='optimized'else [])
        # Native runner enforces its unchanged 60s per-child and original
        # internal guards; total replay consists of nine serial children.
        subprocess.run(interpreter+[str(source/'reproduce.py'),'--work',str(target)],env=env,check=True)
        subprocess.run(interpreter+[str(root/'compare_author.py'),'--own',str(a.own.resolve()),'--physical',str(a.physical.resolve()),'--native',str(target),'--out',str(work/(mode+'-comparison.json'))],env=env,check=True,timeout=60)
    if (work/'normal/MATHEMATICAL.json').read_bytes()!=(work/'optimized/MATHEMATICAL.json').read_bytes():raise ValueError('entire native modes differ')
    if (work/'normal-comparison.json').read_bytes()!=(work/'optimized-comparison.json').read_bytes():raise ValueError('entire comparisons differ')

if __name__=='__main__':main()
