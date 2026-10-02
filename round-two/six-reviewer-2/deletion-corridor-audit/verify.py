"""Regenerate and compare the entire sealed record; checks survive-O."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time,resource
root=Path(__file__).resolve().parent
started=time.monotonic()
env=dict(os.environ)
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[key]='1'
env['PYTHONDONTWRITEBYTECODE']='1'
cmd=[sys.executable]+(['-O']if sys.flags.optimize else[])+[str(root/'audit.py')]
r=subprocess.run(cmd,capture_output=True,text=True,timeout=90,env=env)
if r.returncode:raise ValueError({'code':r.returncode,'stderr':r.stderr})
raw=r.stdout.encode();value=json.loads(raw);expected=json.loads((root/'EXPECTED.json').read_text())
if value!=expected:raise ValueError('whole independent record mismatch')
print(json.dumps({'agent':'six-reviewer-2','role':'independent mathematical reviewer','status':'PASS','whole_record_sha256':hashlib.sha256(raw).hexdigest(),'seconds':round(time.monotonic()-started,3),'peak_child_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'algebra_records':len(value['algebra']),'all_labeled_deletions':len(value['baseline']['all_labeled_deletions']),'original_matrix_positions':value['baseline']['original_matrix_positions'],'transported_original_entries':value['baseline']['transported_original_entries'],'Pell_calibration_orders':sum(len(p['six_orders'])for p in value['Pell']['calibrations']),'semantic_rejections':len(value['semantic_rejections'])},sort_keys=True))
