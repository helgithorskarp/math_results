"""Exact coefficient certificate for the active balanced-triangle endpoint.

Actual author six-downset-1/researcher. QQ[h,q], characteristic0,
factor-preserving exact arithmetic; no interpolation reconstruction or CAS.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name]='1'
from pathlib import Path
import sys,json,signal,time,resource
sys.path.insert(0,str(Path(__file__).resolve().parent))
from bivariate import P,R,ATOMS,PROBES,DEN_CACHE,atom
from clearing import encode,shift

DOMAIN='auxiliary real h>=2,q>=4; original integer h>=2,q=2^(n-1),integer n>=3'
def require(ok,msg):
    if not ok:raise ValueError(msg)
def coded(z):
    z=R(z)
    return {'numerator':encode(z.num),'denominator_factors':[{'factor':encode(ATOMS[k]),'power':e} for k,e in sorted(z.den.items())]}
def generate():
    ATOMS.clear();PROBES.clear();DEN_CACHE.clear()
    h=R(P({(1,0):1}));q=R(P({(0,1):1}));s=q+3*h;N=2*q+12*h;ell=6*h+1
    for z in (h,h-1,2*h-1,s,N,ell):atom(z.num)
    c=9*(ell-q+1)/(2*ell*s)
    common=(q-1+(2*q-3)*3*h)/(ell**2)
    mu=(s-3)/3-common-2*s*c*c/(9*(h-1))
    beta=2*s/3-4*s*c*c*(h+3)/(27*(h-1))
    nu=2*h*mu/(2*h-1)
    for z in (mu,beta,nu):
        require(shift(z.num).positive(),'seed numerator sign');atom(z.num)
    D=(6*h+1)*(2*h-1);r=(D+1)/D;Z=6*h*h-2*h-1;atom(Z.num)
    upper=r*N/6-nu
    gap=2*h/(2*h-1)*(h*(1-3/(ell**2))+2*s*c*c/(9*(h-1)))
    require(upper==gap,'complete uniform mean-bound identity')
    theta=1-1/(2*h)
    a0=(12*N+9*theta*nu)/(N**2)
    b0=(2*N+beta+theta*nu)/(N**2)
    c0=(3-(3*h-1)/Z)/N
    kappa=2/nu+4/beta
    comparison=36*a0*b0-(kappa-6*c0)**2
    fields={'beta':beta,'nu':nu,'kappa':kappa,'a0':a0,'b0':b0,'c0':c0,'upper_gap':gap,'nu_upper':upper,'comparison':comparison}
    for name,z in fields.items():
        require(shift(z.num).positive(),'strict shifted numerator '+name)
        require(all(shift(ATOMS[k]).positive() for k in z.den),'strict denominator factors '+name)
    return {'domain':DOMAIN,'fields':{name:coded(z) for name,z in sorted(fields.items())}}
def main():
    state=Path('/scratch/research-team-sol61-six-20260929/state')
    require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational barrier')
    def alarm(a,b):raise TimeoutError('unchanged60s symbolic child')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    c=generate();signal.alarm(0)
    work=Path(__file__).resolve().parent/'work';work.mkdir(exist_ok=True)
    raw=(json.dumps(c,indent=2,sort_keys=True)+'\n').encode();(work/'CERTIFICATE.json').write_bytes(raw)
    from hashlib import sha256
    out={'status':'COMPLETE exact positive coefficient candidate; independent checker required','certificate_bytes':len(raw),'certificate_sha256':sha256(raw).hexdigest(),'seconds':time.monotonic()-start,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'optimized':sys.flags.optimize}
    print(json.dumps(out),flush=True)
if __name__=='__main__':main()
