"""literal full original invariant spread repair and dual control."""
from pathlib import Path
from fractions import Fraction as F
import json,time,signal,resource
from completion_harmonic import build,alarm
from exact import require,psd_rank,matvec,dot,vecadd,scale,lift,check,fingerprint
from linear import solve
from probe import whole_lift

def spread(n,h,l,sector_record):
    seed,defining,C,M,family=build(n,h,l)
    N,s=seed['N'],seed['s'];m=3*(h+l);offset=2**n-1+m
    require(seed['full_core']==dict(psd=True,rank=N-3),'whole seed core rank')
    record=json.loads(Path(sector_record).read_text())
    require((record['n'],record['h'],record['N'],record['s'])==(n,h,N,s)
            and record['seed_matrix_sha256']==seed['matrix_sha256'],'whole original control binding')
    start=0
    for block in record['blocks']:
        if block['name']=='aggregate':break
        start+=block['dimension']
    else:raise ValueError('complete aggregate physical basis missing')
    basis=[[F(x) for x in row] for row in record['basis']]
    rows=[[F(x) for x in row] for row in defining['all_physical_rows']]
    metric=[[F(x) for x in row] for row in defining['physical_metric']]
    tau=F(seed['tau']);beta=F(seed['scalar_groups'][1]['beta'])
    mux,muy=[F(g['mu']) for g in seed['scalar_groups']]
    Z=vecadd(scale(F(1,h*l)/tau,basis[start+9]),scale(F(-2,l)/beta,basis[start+8]))
    u=[F(offset<=i<offset+3*h) for i in range(N-1)]
    v=[F(i>=offset+3*h and (i-offset)%3==2) for i in range(N-1)]
    a=scale(F(1,h),u);b=scale(F(1,l),v);p=vecadd(a,scale(-3,b));c=scale(F(1,6),vecadd(a,scale(3,b)))
    r=[F(m,m+1) if i<offset else F(1) for i in range(N-1)]
    heavy=[F(bool(A&1)) for A in family[1:]]
    require(dot(p,r)==0 and dot(c,r)==1 and dot(p,heavy)==dot(c,heavy)==0,'all completion/star scores')
    scores=[dot(row,matvec(metric,Z)) for row in rows]
    require(scores==[F(0)]+p,'EVERY spread physical dual score including actual empty')
    kappa=F(1,h*l)/tau+F(4,l)/beta
    require(dot(Z,matvec(metric,Z))==kappa
            and kappa==F(1,h)/mux+F(1,l)/muy+F(4,l)/beta
            and 0<kappa<F(49,78),'complete new mean-dual norm and bound')
    last=N-2;keep=[i for i in range(N-1) if i not in (0,last)]
    A=[[C[i][j] for j in keep] for i in keep]
    require(psd_rank(A)==N-3,'whole original basis principal PD')
    inv=solve(A,[p[i] for i in keep]);dual=[F(0)]*(N-1)
    for i,x in zip(keep,inv):dual[i]=x
    require(matvec(C,dual)==p and dot(p,dual)==kappa,'EVERY original pseudoinverse equation and energy')
    Q=whole_lift(C);P=[[F(i==j)-F(1,N) for j in range(N)] for i in range(N)]
    require(psd_rank([[(N-1)*P[i][j]-Q[i][j] for j in range(N)] for i in range(N)])==N-1,'ENTIRE seed cap floor1')
    af=[F(-3)]+a;bf=[F(-1)]+b
    require(sum(af)==sum(bf)==0 and dot(af,bf)==3 and dot(af,af)==9+F(3,h)
            and dot(bf,bf)==1+F(1,l),'whole actual-empty perturbation norm inputs')
    results=[];whole=[]
    for delta in (F(1,32),F(1,8)):
        sharp=[[C[i][j]+delta*(a[i]*b[j]+b[i]*a[j]) for j in range(N-1)] for i in range(N-1)]
        QR=whole_lift(sharp);perturb=[[delta*(af[i]*bf[j]+bf[i]*af[j]) for j in range(N)] for i in range(N)]
        require(QR==[[Q[i][j]+perturb[i][j] for j in range(N)] for i in range(N)],'EVERY full lift perturbation entry')
        require(QR[0][0]==Q[0][0]+6*delta and not any(matvec(sharp,heavy)),'actual empty change and sole forced star')
        out=lift(sharp,s);final=check(family,out,s)
        require(psd_rank(sharp)==N-2 and final['lower_rank']==final['upper_rank']==N-1,'both greatest original ranks')
        floor=1-7*delta
        require(psd_rank([[(N-floor)*P[i][j]-QR[i][j] for j in range(N)] for i in range(N)])==N-1,'ENTIRE rational repaired cap floor')
        require(1-delta*kappa/6>0,'whole range downdate factor')
        swaps=[]
        for fi in range(h+l):swaps.append(((n+2*fi,n+2*fi+1),))
        for lo,hi in ((0,h),(h,h+l)):
            for fi in range(lo,hi-1):swaps.append(((n+2*fi,n+2*(fi+1)),(n+2*fi+1,n+2*(fi+1)+1)))
        for z in range(2,n-1):swaps.append(((z,z+1),))
        lookup={A:i for i,A in enumerate(family)}
        for swap in swaps:
            def image(A):
                for x,y in swap:
                    if bool(A&(1<<x))!=bool(A&(1<<y)):A^=(1<<x)|(1<<y)
                return A
            perm=[lookup[image(A)] for A in family]
            require(all(out[i][j]==out[perm[i]][perm[j]] for i in range(N) for j in range(N)),
                    'EVERY original symmetry-generator matrix entry')
        results.append(dict(delta=str(delta),cap_floor=str(floor),final=final,
            empty_norm=str(QR[0][0]),whole_matrix_positions=N*N,whole_perturbation_positions=N*N,symmetry_generators=len(swaps),symmetry_positions=len(swaps)*N*N))
        whole.append(dict(delta=str(delta),M=[[str(x) for x in row] for row in out],
            perturbation=[[str(x) for x in row] for row in perturb],dual=[str(x) for x in dual],
            full_physical_dual=[str(x) for x in Z],full_physical_scores=[str(x) for x in scores]))
    endpoint=6/kappa
    end=[[C[i][j]+endpoint*(a[i]*b[j]+b[i]*a[j]) for j in range(N-1)] for i in range(N-1)]
    require(psd_rank(end)==N-3,'whole lower endpoint rank, no upper endpoint assertion')
    return dict(agent='six-downset-1',role='researcher',n=n,h=h,l=l,N=N,s=s,
        kappa_bar=str(kappa),closed_mean_dual_verified=True,all_original_inverse_equations=True,
        all_actual_empty_dual_scores=True,records=results,endpoint=str(endpoint),endpoint_lower_rank=N-2,
        group_invariant_repair=True,uniform_proof_not_from_finite_control=True,independent_review=False),whole

if __name__=='__main__':
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    folder=Path(__file__).resolve().parent
    result,whole=spread(3,5,2,folder/'UNRESTRICTED-FIRST-SECTOR-CONTROL.json')
    raw=json.dumps(whole,separators=(',',':'))+'\n'
    require(len(raw.encode())<=32*1024*1024,'unchanged32MiB whole control guard')
    (folder/'SPREAD-WHOLE.json').write_text(raw)
    result.update(seconds=time.monotonic()-start,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=not __debug__)
    (folder/'SPREAD-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    signal.alarm(0);print(json.dumps(result),flush=True)
