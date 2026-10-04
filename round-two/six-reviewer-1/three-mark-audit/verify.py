"""Serial, bounded complete replays; no producer or unlisted input imported."""
from pathlib import Path
import argparse,hashlib,json,os,resource,shutil,subprocess,sys,time

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work-dir',type=Path,required=True);a=parser.parse_args()
    root=Path(__file__).resolve().parent;work=a.work_dir.resolve()
    if work.exists():raise ValueError('choose a fresh output directory')
    for n,h in json.loads((root/'PRIMARY_SEAL.json').read_text())['files'].items():
        if hashlib.sha256((root/n).read_bytes()).hexdigest()!=h:raise ValueError('preimport primary source binding')
    expected=(root/'EXPECTED.json').read_bytes();work.mkdir(parents=True);env=os.environ.copy()
    for n in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']:env[n]='1'
    declared=['PRIMARY_SEAL.json','CERTIFICATE_INPUT.json','polynomials.py','certificate.py','geometry.py','check.py','validate.py']
    runs=[]
    def run(label,source,entry,optimized=False,reject=False):
        dest=work/(label+'.json');args=[sys.executable,'-I','-B']+(['-O']if optimized else [])+[str(source/entry),str(dest)]
        started=time.monotonic();p=subprocess.run(args,capture_output=True,text=True,timeout=45,env=env)
        if reject:
            if p.returncode==0 or 'preimport primary source binding'not in p.stderr:raise ValueError('source-binding defect not rejected before import')
        elif p.returncode:raise ValueError('child failed '+label+'\n'+p.stderr)
        raw=dest.read_bytes()if dest.exists()else b''
        if entry=='check.py'and not reject and raw!=expected:raise ValueError('whole mathematical record differs')
        r={'label':label,'seconds':round(time.monotonic()-started,6),'returncode':p.returncode,
           'whole_bytes':len(raw),'whole_sha256':hashlib.sha256(raw).hexdigest(),
           'child_cumulative_maxrss_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
        runs.append(r)
        return raw
    for cold in [False,True]:
        source=root
        if cold:
            source=work/'cold-sources';source.mkdir()
            for n in declared:shutil.copyfile(root/n,source/n)
        for optimized in [False,True]:run(('cold'if cold else'local')+('-O'if optimized else'-normal'),source,'check.py',optimized)
    negatives=[]
    for optimized in [False,True]:
        raw=run('defects'+('-O'if optimized else'-normal'),work/'cold-sources','validate.py',optimized)
        records=json.loads(raw)
        if len(records)!=10 or not all(r['rejected']for r in records):raise ValueError('whole invalid-fixture census')
        negatives.extend(records)
    altered=work/'altered-source';shutil.copytree(work/'cold-sources',altered)
    with (altered/'polynomials.py').open('a')as handle:handle.write('\n# intentional binding defect\n')
    for optimized in [False,True]:run('source-defect'+('-O'if optimized else'-normal'),altered,'check.py',optimized,True)
    summary={'agent':'six-reviewer-1','role':'independent mathematical reviewer','runtime':sys.version,
      'complete_positive_replays':4,'distinct_mathematical_defects':10,'actual_mathematical_rejections':len(negatives),
      'preimport_source_rejections':2,'full_mathematical_record_bytes':len(expected),
      'full_mathematical_record_sha256':hashlib.sha256(expected).hexdigest(),'all_whole_records_equal':True,
      'fixed_child_timeout_seconds':45,'native_threads':1,'maximum_simultaneous_mathematical_children':1,
      'runs':runs,'negative_records':negatives,'any_resource_limit_hit':False}
    (work/'VALIDATION.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items()if k not in ['runs','negative_records','runtime']},indent=2))

if __name__=='__main__':main()
