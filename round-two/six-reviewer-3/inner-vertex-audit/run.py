"""Serial normal/optimized source-only replay of entire mathematical outputs."""
import argparse,hashlib,json,os,resource,subprocess,sys,time
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--records-directory');args=ap.parse_args()
    root=Path(__file__).resolve().parent;fixture=json.loads((root/'RESULTS.json').read_text())
    commands=[(name,[file+'.py']) for name,file in [('engine','engine_controls'),('geometry','geometric_checks'),
        ('bindings','bindings'),('gram','gram'),('systems','systems'),('raw','raw'),('control','control'),('damages','damages')]]
    signs=fixture['sign_names']
    for name in signs:commands.append(('sign_'+name,['sign_checks.py',name]))
    if [name for name,command in commands]!=list(fixture['records']):raise ValueError('entire expected command domain differs')
    destination=Path(args.records_directory) if args.records_directory else None
    if destination:destination.mkdir(parents=True,exist_ok=False)
    env=os.environ.copy()
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[key]='1'
    receipts=[];first={}
    for optimized in [False,True]:
        for name,command in commands:
            begin=time.monotonic();p=subprocess.run([sys.executable]+(['-O'] if optimized else [])+command,cwd=root,env=env,capture_output=True,timeout=30)
            if p.returncode:raise RuntimeError(name+' mathematical child failed: '+p.stderr.decode())
            json.loads(p.stdout);sha=hashlib.sha256(p.stdout).hexdigest();expected=fixture['records'][name]
            if sha!=expected['whole_stdout_sha256'] or len(p.stdout)!=expected['whole_stdout_bytes']:raise ValueError('entire mathematical record changed: '+name)
            if name in first and p.stdout!=first[name]:raise ValueError('whole normal/optimized bytes differ: '+name)
            first[name]=p.stdout
            if destination:(destination/(name+('-O' if optimized else '')+'.json')).write_bytes(p.stdout)
            receipts.append({'name':name,'optimized':optimized,'whole_stdout_sha256':sha,'seconds':time.monotonic()-begin,
                'cumulative_peak_child_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
    print(json.dumps({'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','all_whole_records_verified':True,
        'reproduction_fixture_sha256':hashlib.sha256((root/'RESULTS.json').read_bytes()).hexdigest(),
        'resources':{'python':sys.version.split()[0],'threads':1,'serial':True,'child_guard_seconds':30,'successful_children':len(receipts),'children':receipts}},sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
