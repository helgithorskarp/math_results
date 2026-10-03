"""One bounded exact phase; optimized mode keeps all explicit checks."""
from pathlib import Path
import hashlib, json, os, sys, time
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
import reduction, terminal
start=time.monotonic()
def require(t,m):
    if not t:raise ValueError(m)
def guard():
    if time.monotonic()-start>30:raise RuntimeError('30s mathematical guard; incomplete, no exclusion')
def digest(x):
    return hashlib.sha256(reduction.canonical(x)).hexdigest()
name,path=sys.argv[1:]
out=Path(path);require(not out.exists(),'preserve existing mathematical phase')
record=(terminal.run(require,guard,digest) if name=='terminal' else
        reduction.transports(require,guard,digest) if name=='transports' else
        reduction.run(require,guard,digest) if name=='reduction' else None)
require(record is not None and record['complete'] is True,'known completed phase')
guard();raw=reduction.canonical(record);out.write_bytes(raw)
print(json.dumps({'phase':name,'complete':True,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}))
