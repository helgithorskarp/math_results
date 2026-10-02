"""Four independent whole-fixture controls, serial normal and optimized.
An operational timeout or signal is an error, never an accepted rejection.
"""
from pathlib import Path
import json,os,signal,subprocess,sys,tempfile
signal.alarm(90)
root=Path(__file__).resolve().parent;env=os.environ.copy()
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[name]='1'
record=[]
with tempfile.TemporaryDirectory(prefix='critical-phase-fixture-') as directory:
    d=Path(directory);altered=json.loads((root/'expected.json').read_text());altered['extra_unverified_claim']='not part of regenerated mathematics';(d/'altered.json').write_text(json.dumps(altered))
    for optimized in (False,True):
        for mode in ('missing','altered'):
            p=d/(mode+'.json');args=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(root/'check.py'),'--expected',str(p)]
            r=subprocess.run(args,capture_output=True,text=True,timeout=90,env=env)
            wanted='expected fixture unreadable' if mode=='missing' else 'entire regenerated fixture comparison'
            if r.returncode!=1 or wanted not in r.stderr:raise RuntimeError('invalid fixture did not give mathematical/input rejection '+str((mode,optimized,r.returncode,r.stderr)))
            record.append({'mode':mode,'optimized':optimized,'exit':r.returncode,'diagnostic':r.stderr.strip()})
print(json.dumps({'status':'PASS','external_rejections':record,'count':len(record),'signal_or_timeout_is_not_rejection':True},sort_keys=True))
