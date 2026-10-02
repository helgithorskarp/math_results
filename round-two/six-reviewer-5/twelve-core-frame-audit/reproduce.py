"""Rebuild the entire independent record, strictly serial; no author imports."""
import argparse,hashlib,json,os,pathlib,resource,shutil,subprocess,sys,tempfile,time

def rebuild(base,optimized=False):
    env=dict(os.environ)
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[k]='1'
    expected=json.loads((base/'EVIDENCE.json').read_text())
    pins=json.loads((base/'INPUTS.json').read_text())
    for name,digest in pins['certificate_sha256'].items():
        if hashlib.sha256((base/'author'/name).read_bytes()).hexdigest()!=digest:raise ValueError('pinned certificate changed')
    records={};costs=[]
    with tempfile.TemporaryDirectory(prefix='twelve-frame-review-') as directory:
        root=pathlib.Path(directory);shutil.copytree(base/'core',root/'core',ignore=shutil.ignore_patterns('__pycache__'))
        (root/'author').mkdir()
        for name in ('PLAN.json','LITERALS.json'):shutil.copyfile(base/'author'/name,root/'author'/name)
        def run(name,*args):
            cmd=[sys.executable]+(['-O'] if optimized else [])+[str(root/'core'/name),*map(str,args)]
            clock=time.monotonic();r=subprocess.run(cmd,cwd=root,env=env,capture_output=True,timeout=45)
            if r.returncode:raise RuntimeError(r.stderr.decode())
            costs.append(dict(program=name,args=list(args),seconds=time.monotonic()-clock,maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss))
            return json.loads(r.stdout)
        for name in ('identities.py','controls.py','damages.py','positive.py'):records[name]=run(name)
        records['ranges']=[run('replay.py',start,stop) for start,stop in ((0,2500),(2500,5000),(5000,7500),(7500,10000),(10000,12091))]
    if records!=expected:raise ValueError('entire independent mathematical record changed')
    digest=hashlib.sha256((json.dumps(records,sort_keys=True,indent=2)+'\n').encode()).hexdigest()
    return dict(whole_record_sha256=digest,full_record_matches=True,complete_predicates=12091,identities=63,
                structural_damages=len(records['damages.py']['structural_damages']),mode='optimized' if optimized else 'normal',children=costs)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--optimized',action='store_true');args=parser.parse_args()
    print(json.dumps(rebuild(pathlib.Path(__file__).resolve().parent,args.optimized),sort_keys=True,indent=2))
