"""One bounded exact corroboration phase, with an explicit completion marker."""
from pathlib import Path
import hashlib,json,os,sys,time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS',
             'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[name]='1'
start=time.monotonic()
def require(t,m):
    if not t:raise ValueError(m)
def guard():
    if time.monotonic()-start>30:raise RuntimeError('30s mathematical guard; incomplete, no exclusion')
def digest(x):return hashlib.sha256((json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
def main():
    name,output=sys.argv[1:3]
    if name=='reduction':
        from reduction import run
    elif name=='transports':
        from reduction import transports as run
    elif name=='terminal':
        from terminal import run
    else:raise ValueError('unknown phase')
    out=run(require,guard,digest);guard()
    require(out.get('complete') is True,'whole phase completion')
    raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode()
    Path(output).write_bytes(raw)
    print(json.dumps({'complete':True,'phase':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}))
if __name__=='__main__':main()
