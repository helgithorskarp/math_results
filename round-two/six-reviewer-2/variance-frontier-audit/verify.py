"""Seven exact serialized phases, whole frozen comparison; original guards.

No arbitrary all-q physical allocation. Every child has a60s internal
alarm and90s outer deadline. At most one mathematical child at a time.
"""
from pathlib import Path
import hashlib,json,os,resource,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
PHASES=[['symbolic.py'],['variance.py'],['physical.py','baseline'],['physical.py','point','24','6'],['physical.py','point','19','5'],['physical.py','point','19','5','new'],['controls.py']]
NATIVE=['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']
if any(os.environ.get(k)!='1'for k in NATIVE):raise ValueError('every native thread variable must explicitly be1')
records=[];timings=[];start=time.monotonic()
for phase in PHASES:
 t=time.monotonic();argv=[sys.executable]+(['-O']if sys.flags.optimize else[])+[str(ROOT/phase[0])]+phase[1:]
 r=subprocess.run(argv,capture_output=True,text=True,timeout=90)
 if r.returncode:raise ValueError({'phase':phase,'code':r.returncode,'stderr':r.stderr})
 records.append({'phase':phase,'record':json.loads(r.stdout)});timings.append({'phase':phase,'seconds':time.monotonic()-t})
record={'agent':'six-reviewer-2','role':'independent mathematical reviewer','scope':'9546 new whole-count/unbounded signs/192closure/physical23+422complete complement/actual empty+refinements; explicit owned9552/9488/9508 and8757/9145 premises','records':records}
raw=json.dumps(record,sort_keys=True,separators=(',',':'))+'\n';path=ROOT/'EXPECTED.json'
if '--emit'in sys.argv:path.write_text(raw)
if not path.exists()or json.loads(path.read_text())!=record:raise ValueError('whole frozen mathematical record differs')
print(json.dumps({'agent':'six-reviewer-2','role':'independent mathematical reviewer','status':'PASS','mode':'optimized'if sys.flags.optimize else'normal','whole_expected_equal':True,'whole_record_sha256':hashlib.sha256(raw.encode()).hexdigest(),'phases':len(PHASES),'seconds':time.monotonic()-start,'peak_child_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'timings':timings},sort_keys=True))
