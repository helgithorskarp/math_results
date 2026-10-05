"""Free-level count resolvent and unique FIRST-root isolation (PRIVATE).

six-downset-1/researcher; exact stdlib Fractions; same-author validation.
The scalar definitions and shift identities are explicitly credited to
6b95f73178cfbdfcac4ff993f4eb92970f5605ee. This new module never builds
an original matrix and never reads an expected record or old checker.
Large count controls validate formulas, not universal completeness.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
             'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name]='1'
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import argparse
import json
import resource
import signal
import time
from hashlib import sha256


def require(ok,message):
    if not ok:
        raise ValueError(message)


def barrier():
    state=Path('/scratch/research-team-sol61-six-20260929/state')
    require(not any((state/n).exists() for n in
        ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational barrier')


def scalars(q,counts):
    require(type(q) is int and 0<q<=2**20 and type(counts) in (list,tuple) and 3<=len(counts)<=20 and all(type(k) is int and 0<k<=2**20 for k in counts),
            'bounded count inputs before scalar lists')
    h,r=counts[0],len(counts)
    require(r>=3 and all(2<=k<h for k in counts[1:]) and sum(counts)>=9,
            'unique-heavy domain')
    total=sum(counts); s=q+3*h; ell=3*total+1
    c0=F(q*ell+9*sum(k*(h-k) for k in counts[1:])+3*h-6*total-1,ell**2)
    R=[F(ell+1-q-3*(h-k),ell) for k in counts]
    mu=[F(s-3,3)-c0-F(9,2*s*(k-1))*v*v for k,v in zip(counts,R)]
    beta=[F(2*s,3)-F(3*(k+3),s*(k-1))*v*v for k,v in zip(counts,R)]
    c=[F(9,2*s)*v for v in R]
    S=sum((k*u for k,u in zip(counts,mu)),F(0)); SL=S-h*mu[0]
    WL=sum((k*u*u for k,u in zip(counts[1:],mu[1:])),F(0))
    require(all(v>0 for v in mu+beta+[S,SL]),'positive seed scalar denominators')
    return dict(q=q,counts=counts,h=h,r=r,s=s,N=2*q+6*total,ell=ell,m=3*total,
                L=total-h,mu=mu,beta=beta,c=c,S=S,SL=SL,WL=WL)


def shift(q,counts,theta):
    h=counts[0]; r=len(counts); m=3*sum(counts)
    det=[2*q*q+(6*h-3*theta)*q+theta*theta-3*theta*(h+k) for k in counts[1:]]
    # A derivative jet also supports exact value comparison through its base.
    val=lambda x:x.value if hasattr(x,'value') else x
    require(all(val(x)>0 for x in [6*h-theta,2*q-theta,q-theta]+det),
            'all original shifted poles positive')
    w=m+3*h*theta/(q-theta)+sum((3*k*theta*(2*q+6*k-theta)/d
        for k,d in zip(counts[1:],det)),F(0))
    z=-F(3*h)/(q-theta)-sum((3*k*(2*q+6*h-theta)/d
        for k,d in zip(counts[1:],det)),F(0))
    g=F(q-1)/(6*h-theta)+F(3*h*(q-r),q)/(2*q-theta)+F(3*h,q)/(q-theta) \
        +sum((3*((h+k)*q+3*h*(h+k)-h*theta)/(q*d)
              for k,d in zip(counts[1:],det)),F(0))
    return dict(w=w,z=z,g=g,sigma=m-w+(1-z)**2/(1+g),det=det)


def level(seed,x):
    counts=seed['counts']; h=seed['h']; s=seed['s']; mu=seed['mu']; beta=seed['beta']; c=seed['c']
    S=seed['S']; SL=seed['SL']; WL=seed['WL']
    d=[x-3*u for u in mu]; require(all(v>0 for v in d),'free-level mean poles')
    T=sum((k*u*u/dg for k,u,dg in zip(counts,mu,d)),F(0))
    TL=T-h*mu[0]**2/d[0]; Z=S/3+T
    H=[x*x-x*(s*(1*F(1)+cg*cg)+3*b/2)+3*s*b/2 for cg,b in zip(c,beta)]
    require(Z>0 and all(v>0 for v in H),'free-level full trace poles')
    E=[k*(b*(x-s)+F(2,3)*x*cg*cg*s)/v for k,b,cg,v in zip(counts,beta,c,H)]
    a=9+3*x/(h*d[0])-3*x*mu[0]**2/(d[0]**2*Z)
    b=1+2*WL/(3*SL**2)+x*(TL-TL**2/Z)/(3*SL**2) \
        +sum((u*u*e/SL**2 for u,e in zip(mu[1:],E[1:])),F(0))
    cbar=3-x*mu[0]*TL/(d[0]*SL*Z)
    require(a>0 and b>0 and a*b>cbar*cbar,'strict restricted two-vector Gram')
    return dict(x=x,d=d,T=T,TL=TL,Z=Z,H=H,E=E,abar=a,bbar=b,cbar=cbar,
                inverse_Gram=[a/x,b/x,cbar/x])


def sqrt_bounds(value,bits=72):
    require(value>0,'positive rational radical')
    scale=1<<bits
    integer=isqrt((value.numerator*scale*scale)//value.denominator)
    lo,hi=F(integer,scale),F(integer+1,scale)
    require(lo*lo<=value<hi*hi,'full exact radical inequalities')
    return lo,hi


def positive_bounds(seed,x):
    f=level(seed,x); lo,hi=sqrt_bounds(f['abar']*f['bbar'])
    require(f['cbar']+lo>0,'positive denominator of isolated root')
    return F(x)/(f['cbar']+hi),F(x)/(f['cbar']+lo)


def isolate(n,counts):
    require(type(n) is int and 4<=n<=20 and 3<=len(counts)<=min(n,20),
            'bounded count-only input; not a literal original request')
    q=2**(n-1); seed=scalars(q,counts); h=seed['h']
    require(q>=200*h,'large-cube theorem domain for count-only root')
    baseline=shift(q,counts,F(0)); g0=F(q-1,6*h)+F(3*h,2*q)+F(3*sum(counts),2*q*q)
    require((baseline['w'],baseline['z'],baseline['g'])==(F(seed['m']),-F(seed['m'],q),g0),
            'exact useful original Schur baseline')
    require(baseline['sigma']==(1+F(seed['m'],q))**2/(1+g0)>0,'baseline full positive Schur')
    lo=F(0); hi=None; bracket_trials=[]
    for j in range(1,33):
        test=F(6*h)* (1-F(1,1<<j)); sig=shift(q,counts,test)['sigma']
        bracket_trials.append([str(test),str(sig)])
        if sig<0:
            hi=test; break
    require(hi is not None,'bounded root bracketing incomplete is not nonexistence')
    for _ in range(56):
        mid=(lo+hi)/2; value=shift(q,counts,mid)['sigma']
        require(value!=0,'exact rational root needs a separate explicit record')
        if value>0: lo=mid
        else: hi=mid
    siglo,sighi=shift(q,counts,lo)['sigma'],shift(q,counts,hi)['sigma']
    require(0<lo<hi<6*h and siglo>0>sighi,'both exact complete root signs')
    tlo,thi=2*seed['s']-hi,2*seed['s']-lo
    dlo=positive_bounds(seed,tlo)[0]; dhi=positive_bounds(seed,thi)[1]
    ulo,uhi=positive_bounds(seed,F(seed['N']))
    require(F(q,200)<dlo<dhi<ulo<uhi,'whole strict FIRST/upper boundary ordering')
    return dict(n=n,counts=counts,N=seed['N'],large_original_constructed=False,
        baseline={key:str(baseline[key]) for key in ('w','z','g','sigma')},
        negative_bracket_trials=bracket_trials,gamma_interval=[str(lo),str(hi)],
        gamma_endpoint_sigma=[str(siglo),str(sighi)],top_FIRST_interval=[str(tlo),str(thi)],
        delta_FIRST_interval=[str(dlo),str(dhi)],delta_upper_interval=[str(ulo),str(uhi)],
        exact_cap_interval=[str(6*seed['L']+lo),str(6*seed['L']+hi)],
        root_bisections=56,radical_bits=72,positive_order_verified=True,
        universal_scope='ORDINARY unformalized proof, not these finite count controls')


def stringify(value):
    if isinstance(value,F): return str(value)
    if isinstance(value,dict): return {k:stringify(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [stringify(x) for x in value]
    return value


def calculate():
    controls=[isolate(11,list(counts)) for counts in ((4,3,2),(5,2,2),(3,2,2,2))]
    small=[]
    for counts in ((4,3,2),(5,2,2),(3,2,2,2)):
        for theta in (F(3,2),F(5,2)):
            f=shift(8,counts,theta); small.append(dict(counts=counts,theta=str(theta),sigma=str(f['sigma'])))
    result=dict(agent='six-downset-1',role='researcher',status='NEW EXACT COUNT ROOT/BOUNDARY CONTROLS',
        large_original_matrices_constructed=0,controls=controls,new_small_level_preflight=small,
        source_commit=None,graph_ref=None,formalized=False,independent_review=False)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args(); barrier(); require(not args.out.exists(),'unique fresh output')
    def expire(a,b): raise TimeoutError('unchanged60s; incomplete is not nonexistence')
    signal.signal(signal.SIGALRM,expire); signal.alarm(60); started=time.monotonic()
    result=calculate()
    raw=json.dumps(stringify(result),sort_keys=True,separators=(',',':')).encode()+b'\n'
    require(len(raw)<=32*1024*1024,'32MiB whole record'); args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_bytes(raw); signal.alarm(0)
    print(json.dumps(dict(status=result['status'],bytes=len(raw),sha256=sha256(raw).hexdigest(),
        seconds=time.monotonic()-started,peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        small_shift_signs=[(x['counts'],x['theta'],F(x['sigma'])>0) for x in small])))


if __name__=='__main__': main()
