"""Ten serialized bounded mathematical phases; whole-record comparison.

Fixed60s each internal guard,90s outer phase; native threads1. One child
at a time, no target code import. Entire expected object regenerated in
both modes. --emit builds own record before author program inspection.
"""
from pathlib import Path
import hashlib,json,os,resource,subprocess,sys,time
root=Path(__file__).resolve().parent;env=dict(os.environ)
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[key]='1'
env['PYTHONDONTWRITEBYTECODE']='1'
commands=[['endpoint.py'],['scalar.py'],['finite.py','zero'],['finite.py','repair']]
commands+=[['finite.py','original',str(q),str(k),mode]for q,k in [(4,1),(7,2),(12,3)]for mode in ['old','new']]
records=[];timings=[];total=time.monotonic()
for args in commands:
 cmd=[sys.executable]+(['-O']if sys.flags.optimize else[])+[str(root/args[0]),*args[1:]];t=time.monotonic();r=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=90)
 if r.returncode:raise ValueError({'phase':args,'code':r.returncode,'stderr':r.stderr})
 records.append({'phase':args,'record':json.loads(r.stdout)});timings.append({'phase':args,'seconds':time.monotonic()-t})
value={'agent':'six-reviewer-2','role':'independent mathematical reviewer','records':records,'scope':'universal zero coefficient endpoint and ordinary adaptive proof; positive1/8 floor9145 and complete harmonic framework8757 credited premises; three finite old/new repair endpoints; no feasibility outsideB0 theorem'}
raw=(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()
if '--emit'in sys.argv:sys.stdout.buffer.write(raw)
else:
 expected=json.loads((root/'EXPECTED.json').read_text())
 if value!=expected:raise ValueError('whole ten-phase record differs')
 print(json.dumps({'agent':'six-reviewer-2','role':'independent mathematical reviewer','status':'PASS','phases':len(records),'whole_record_sha256':hashlib.sha256(raw).hexdigest(),'seconds':round(time.monotonic()-total,3),'peak_child_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'timings':timings},sort_keys=True))
