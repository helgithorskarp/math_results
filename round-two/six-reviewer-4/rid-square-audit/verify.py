"""Check complete declared source before a guarded fresh mathematical child."""
import argparse,hashlib,json,os,subprocess,sys
from pathlib import Path

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source-only',action='store_true');parser.add_argument('--controls',action='store_true');args=parser.parse_args()
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'MANIFEST.json').read_text())
    if {p.name for p in root.iterdir()if p.is_file()}!=set(manifest['files'])|{'MANIFEST.json'}:raise ValueError('complete declared source inventory mismatch')
    for name,entry in manifest['files'].items():
        p=root/name
        if not p.is_file()or p.stat().st_size!=entry['bytes']or hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:raise ValueError('declared source mismatch: '+name)
    if args.source_only:
        print(json.dumps({'source_files_verified':len(manifest['files']),'actual_agent':'six-reviewer-4'},sort_keys=True));return
    env=dict(os.environ)
    for key in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[key]='1'
    program='controls.py'if args.controls else'audit.py';expected='controls-expected.json'if args.controls else'expected.json'
    command=[sys.executable,'-B',*(['-O']if sys.flags.optimize else[]),str(root/program)]
    result=subprocess.run(command,env=env,capture_output=True,text=True,timeout=30,check=True)
    actual=json.loads(result.stdout)
    if actual!=json.loads((root/expected).read_text()):raise ValueError('whole fresh mathematical summary mismatch')
    print(result.stdout,end='')

if __name__=='__main__':main()
