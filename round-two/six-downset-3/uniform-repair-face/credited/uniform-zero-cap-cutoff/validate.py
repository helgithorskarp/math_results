"""Serial complete normal/O validation; bulky regenerated outputs stay local."""
from pathlib import Path
import sourcecheck
SOURCE=sourcecheck.check_bundle()
import os,sys,json,time,subprocess,hashlib,resource

HERE=Path(__file__).resolve().parent
PHASES=('uniform','zero-fields','coefficients','frame','fields','branch',
        'original','lower-structure','baseline','minor1','minor2','minor3',
        'damage','coefficient-damage','source-damage','recover7','recover19','recover100')


def validate(out):
    out.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ)
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[name]='1'
    env['PYTHONDONTWRITEBYTECODE']='1'
    records={};times=[]
    for phase in PHASES:
        for optimized in (False,True):
            mode='optimized' if optimized else 'normal'
            target=out/(phase+'-'+mode+'.json')
            command=[sys.executable]+(['-O'] if optimized else [])+[str(HERE/'verify.py'),'--phase',phase,'--out',str(target)]
            start=time.monotonic()
            try:run=subprocess.run(command,cwd=HERE,env=env,capture_output=True,text=True,timeout=60)
            except subprocess.TimeoutExpired:
                (out/'INCOMPLETE.json').write_text(json.dumps({'actual_agent':'six-downset-3','role':'researcher','status':'PAUSED expensive route at unchanged60s timeout; no mathematical absence','phase':phase,'mode':mode,'times_completed':times},indent=2)+'\n')
                raise SystemExit(1)
            if run.returncode:
                (out/'INCOMPLETE.json').write_text(json.dumps({'actual_agent':'six-downset-3','role':'researcher','phase':phase,'mode':mode,'returncode':run.returncode,'stdout':run.stdout,'stderr':run.stderr,'times_completed':times},indent=2)+'\n')
                print(run.stderr);raise SystemExit(1)
            value=json.loads(target.read_text());encoded=json.dumps(value,sort_keys=True,separators=(',',':')).encode()
            if optimized and value!=records[phase]:raise ValueError('WHOLE normal/O mathematical record mismatch: '+phase)
            records[phase]=value
            times.append({'phase':phase,'mode':mode,'seconds':round(time.monotonic()-start,6),'whole_record_sha256':hashlib.sha256(encoded).hexdigest()})
            (out/'PROGRESS.json').write_text(json.dumps({'times':times,'completed_whole_phases':len(records)},indent=2)+'\n')
            print(json.dumps(times[-1]),flush=True)
    complete=json.dumps(records,indent=2,sort_keys=True)+'\n'
    (out/'VERIFICATION.json').write_text(complete)
    expected=json.loads((HERE/'EXPECTED.json').read_text())
    digest=hashlib.sha256(complete.encode()).hexdigest()
    if expected.get('complete_verification_sha256') is not None and digest!=expected['complete_verification_sha256']:
        raise ValueError('complete verification record differs from compact expected evidence')
    value={'actual_agent':'six-downset-3','role':'researcher','phase_count':len(records),'complete_normal_optimized_record_agreement':True,
           'whole_verification_bytes':len(complete.encode()),'whole_verification_sha256':digest,
           'times':times,'all_native_threads':1,'one_CPU_intensive_job_at_a_time':True,'serial_child_guard_seconds':60,
           'tested_Python_version':sys.version.split()[0],'peak_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
           'ordinary_original_fullspace_lift_complement_rank_bridges_unformalized':True,'independent_person_review':False,
           'complete_source_file_count':SOURCE['complete_source_file_count']}
    (out/'VALIDATION.json').write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'all_complete_phases':len(records),'complete_normal_O_agreement':True,'record_sha256':digest}))


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=HERE/'work');args=ap.parse_args()
    validate(args.out.resolve())
