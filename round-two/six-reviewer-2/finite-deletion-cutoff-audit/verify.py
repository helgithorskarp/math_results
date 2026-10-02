"""Five exact serial phases, ENTIRE frozen comparison, fixed original guards."""
from pathlib import Path
import hashlib,json,os,resource,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
PHASES=['coefficient.py','boundary.py','literal.py','baselines.py','controls.py']
NATIVE=['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']
if any(os.environ.get(k)!='1'for k in NATIVE):raise ValueError('all six native thread variables must be1')
records=[];timings=[];start=time.monotonic()
for phase in PHASES:
 t=time.monotonic();argv=[sys.executable]+(['-O']if sys.flags.optimize else[])+[str(ROOT/phase)]
 r=subprocess.run(argv,capture_output=True,text=True,timeout=90)
 if r.returncode:raise ValueError({'phase':phase,'code':r.returncode,'stderr':r.stderr,'incomplete_is_not_exclusion':True})
 records.append({'phase':phase,'record':json.loads(r.stdout)});timings.append({'phase':phase,'seconds':time.monotonic()-t})
record={'agent':'six-reviewer-2','role':'independent mathematical reviewer','scope':'9582 all20 finite decisions with credited unbounded tails/complete weighted23+complement/actual-empty lift/original3space dual plus NEW entire original integerdomain and ANY whole-floor enlarged repair; explicit8757/9145 and owned9488/9508/9552/9586 premises','records':records}
raw=json.dumps(record,sort_keys=True,separators=(',',':'))+'\n'
if json.loads((ROOT/'EXPECTED.json').read_text())!=record:raise ValueError('ENTIRE frozen mathematical record differs')
print(json.dumps({'agent':'six-reviewer-2','role':'independent mathematical reviewer','status':'PASS','mode':'optimized'if sys.flags.optimize else'normal','whole_expected_equal':True,'whole_record_sha256':hashlib.sha256(raw.encode()).hexdigest(),'phases':len(PHASES),'seconds':time.monotonic()-start,'peak_child_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'timings':timings},sort_keys=True))
