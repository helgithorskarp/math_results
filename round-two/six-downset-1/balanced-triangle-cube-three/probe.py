"""PRIVATE balanced old-cube recipe: exact finite probes, no uniform cap theorem."""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[name]='1'
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from exact import require,psd_rank,dot,matvec,unit,scale,vecadd,zero,lift,fingerprint,check
from linear import solve
import argparse,json,signal,time,resource

def construct(n,h):
    require(type(h) is int and 2<=h<=10,'unchanged literal h guard10')
    require(type(n) is int and 2<=n<=6,'unchanged literal n guard6')
    q=2**(n-1);s=F(q+3*h);N=2*q+12*h;require(N<=80,'unchanged literal N guard80')
    w=s-1;ell=F(6*h+1);m=6*h;B2=s*F(h-1,3*h)
    a=F(3*h)*(ell-q+1)/(2*ell*s*(h-1));b=-2*a;c=9*(ell-q+1)/(2*ell*s)
    common2=F(q-1+(2*q-3)*3*h)/(ell*ell)
    etal=w-common2-a*a*B2-F(2,3)*s*c*c
    etaf=w-common2-b*b*B2-F(2,3)*s*c*c/(h-1)
    p=-1-common2-a*b*B2
    mu=(2*p+etaf)/3;alpha=2*(2*etal-p-etaf);beta=etaf-mu;nu=mu*F(2*h,2*h-1)
    require(min(mu,alpha,beta)>0,'candidate positive W scalar')
    size=N-4;oldsize=2*q-1;wi=oldsize+6*h-2;Gamma=zero(size,size)
    for i in range(oldsize):
        for j in range(oldsize):
            Gamma[i][j]=s*F(i==j)+(q-3*h)*F((i+1)^(j+1)==oldsize)-1
    e=lambda i:unit(size,i)
    old=[e(i) for i in range(oldsize)]
    Hx=scale(-1,vecadd(*(old[i] for i in range(oldsize) if (i+1)&1)))
    Hy=scale(-1,vecadd(*(old[i] for i in range(oldsize) if (i+1)&2)))
    K=vecadd(*old,Hx,Hy);common=scale(-1/ell,K)
    Bs=[]
    for group in range(2):
        offset=oldsize+group*(h-1)
        for i in range(h-1):
            for j in range(h-1):Gamma[offset+i][offset+j]=s/3*(F(i==j)-F(1,h))
        B=[e(offset+i) for i in range(h-1)];B.append(scale(-1,vecadd(*B)));Bs.append(B)
    ts=oldsize+2*(h-1);Ts=[]
    for facet in range(2*h):
        start=ts+2*facet
        Gamma[start][start]=Gamma[start+1][start+1]=2*s/3
        Gamma[start][start+1]=Gamma[start+1][start]=-s/3
        Ts.append([e(start),e(start+1),scale(-1,vecadd(e(start),e(start+1)))])
    V=[];P=[]
    for group,H in enumerate((Hx,Hy)):
        avg=scale(F(1,3*h),H)
        for i in range(h):
            facet=group*h+i
            V.extend(vecadd(avg,Bs[group][i],Ts[facet][leaf]) for leaf in range(3))
            P.extend(vecadd(common,scale(a,Bs[group][i]),scale(c,Ts[facet][1-leaf])) for leaf in range(2))
            other=vecadd(*(Ts[group*h+j][2] for j in range(h) if j!=i))
            P.append(vecadd(common,scale(b,Bs[group][i]),scale(c/F(h-1),other)))
    require(vecadd(*P)==scale(m,common),'entire private projection balance')
    W=zero(m,m);wa=(F(1,2),F(-1,2),F(0));wf=(F(-1,2),F(-1,2),F(1))
    for i in range(m):
        fi,ai=divmod(i,3)
        for j in range(m):
            fj,aj=divmod(j,3)
            W[i][j]=mu if fi==fj else -mu/F(2*h-1)
            if fi==fj:W[i][j]+=wa[ai]*wa[aj]*alpha+wf[ai]*wf[aj]*beta
    require(all(sum(row)==0 for row in W),'entire W sum relation')
    require(psd_rank(W)==m-1,'candidate W exactly one kernel')
    for i in range(m-1):
        for j in range(m-1):Gamma[wi+i][wi+j]=W[i][j]
    Wrows=[e(wi+i) for i in range(m-1)];Wrows.append(scale(-1,vecadd(*Wrows)))
    U=[vecadd(p,r) for p,r in zip(P,Wrows)]
    require(vecadd(*(old+V))==K,'balanced total old plus marked K')
    for group,mark in enumerate((1,2)):
        require(not any(vecadd(*(old[i] for i in range(oldsize) if (i+1)&mark),*V[group*3*h:(group+1)*3*h])),'two literal original maximum-star relations')
    R=old+V+U;images=[matvec(Gamma,r) for r in R]
    C=[[dot(r,v) for v in images] for r in R]
    whole=[common]+R;images_whole=[matvec(Gamma,r) for r in whole]
    require(not any(vecadd(*whole)),'actual empty is negative entire row sum')
    S=[[sum(v[i]*v[j] for v in images_whole) for j in range(size)] for i in range(size)]
    cap=[[(N-1)*Gamma[i][j]-S[i][j] for j in range(size)] for i in range(size)]
    params=dict(n=n,q=q,h=h,N=N,s=s,w=w,ell=ell,a=a,b=b,c=c,common=common2,etal=etal,etaf=etaf,p=p,mu=mu,alpha=alpha,beta=beta,nu=nu)
    return params,Gamma,S,cap,C,dict(R=R,P=P,V=V,U=U,W=W,wi=wi,Bs=Bs,Ts=Ts,oldsize=oldsize,Hx=Hx,Hy=Hy,K=K,common=common)

def whole_lift(C):
    sums=[sum(row) for row in C]
    return [[sum(sums)]+[-v for v in sums]]+[[-sums[i]]+row for i,row in enumerate(C)]

def actual(n,h):
    p,G,S,cap,C,v=construct(n,h);N=p['N'];s=p['s'];core=N-1;oldsize=v['oldsize']
    private=[];marked=[]
    for facet in range(2*h):
        masks=[1<<(n+2*facet),1<<(n+2*facet+1),3<<(n+2*facet)]
        private.extend(masks);marked.extend((1 if facet<h else 2)|a for a in masks)
    family=[0]+list(range(1,2**n))+marked+private
    require(len(family)==N and len(set(family))==N,'entire original distinct family')
    require(sum(bool(a&1) for a in family)==s and sum(bool(a&2) for a in family)==s,'both actual maximum stars')
    seed=check(family,lift(C,s),s)
    require(seed['lower_rank']==N-3 and seed['upper_rank']==N-1,'exact seed endpoint ranks')
    size=N-4;require(psd_rank(G)==size and psd_rank(C)==size,'whole physical metric and seed core rank')
    require(psd_rank(cap)==size,'entire physical floor1')
    Q=whole_lift(C);P0=[[F(i==j)-F(1,N) for j in range(N)] for i in range(N)]
    require(psd_rank([[(N-1)*P0[i][j]-Q[i][j] for j in range(N)] for i in range(N)])==N-1,'original whole floor1')
    require(Q[0][0]==p['common'],'actual empty norm')
    e=lambda i:unit(core,i)
    basis=[e(i) for i in range(oldsize)]
    Hx=scale(-1,vecadd(*(e(i) for i in range(oldsize) if (i+1)&1)))
    Hy=scale(-1,vecadd(*(e(i) for i in range(oldsize) if (i+1)&2)))
    Bs=[]
    for group,H in enumerate((Hx,Hy)):
        avg=scale(F(1,3*h),H);B=[]
        for i in range(h):
            B.append(vecadd(scale(F(1,3),vecadd(*(e(oldsize+3*(group*h+i)+a) for a in range(3)))),scale(-1,avg)))
        Bs.append(B);basis.extend(B[:-1])
    for group,H in enumerate((Hx,Hy)):
        avg=scale(F(1,3*h),H)
        for i in range(h):
            basis.extend(vecadd(e(oldsize+3*(group*h+i)+a),scale(-1,avg),scale(-1,Bs[group][i])) for a in range(2))
    require(len(basis)==v['wi'],'all original projected coordinate alignment')
    offset=oldsize+6*h
    for i in range(6*h-1):
        projection=vecadd(*(scale(a,b) for a,b in zip(v['P'][i][:v['wi']],basis[:v['wi']])))
        basis.append(vecadd(e(offset+i),scale(-1,projection)))
    original_images=[matvec(C,b) for b in basis]
    actualG=[[dot(a,image) for image in original_images] for a in basis]
    require(actualG==G,'ALL original physical Gram entries')
    paired=[[-sum(row)]+row for row in original_images]
    actualS=[[dot(a,b) for b in paired] for a in paired]
    require(actualS==S,'ALL physical frame entries including actual empty')
    last=core-1;keep=[i for i in range(core) if i not in (0,1,last)]
    A0=[[C[i][j] for j in keep] for i in keep]
    require(psd_rank(A0)==size,'original deleted principal PD')
    coeff=lambda i: -F(6*h,6*h+1)*(1-int(bool((i+1)&1))-int(bool((i+1)&2))) if i<oldsize else F(-1) if i>=offset else F(0)
    z=[coeff(i) for i in keep];b0=[C[i][last] for i in keep]
    require(matvec(A0,z)==b0 and dot(z,b0)==s-1,'ENTIRE original deleted column relation')
    r=[F(offset<=i<offset+3) for i in keep];rinv=solve(A0,r);kappa=dot(r,rinv)
    require(kappa==2/p['nu']+4/p['beta'] and dot(r,z)==-3,'entire inverse energy and overlap')
    delta=1/(4*(8+kappa));bb=vecadd(b0,scale(delta,r));zz=vecadd(z,scale(delta,rinv))
    require(matvec(A0,zz)==bb and s-1-dot(bb,zz)==6*delta-kappa*delta*delta,'exact full Schur identity')
    require(6*delta-kappa*delta*delta>0,'strict repaired principal PD')
    sharp=[row[:] for row in C]
    for i in range(offset,offset+3):sharp[i][last]+=delta;sharp[last][i]+=delta
    for mark in (1,2):
        kernel=[F(bool(a&mark)) for a in family[1:]]
        require(not any(matvec(C,kernel)) and not any(matvec(sharp,kernel)),'both original star kernels survive')
    repaired=lift(sharp,s);status=check(family,repaired,s)
    require(psd_rank(sharp)==N-3 and status['lower_rank']==N-2 and status['upper_rank']==N-1,'original repaired ranks')
    floor=1-8*delta;require(floor>F(3,4),'literal scaled gap')
    QR=whole_lift(sharp)
    require(psd_rank([[(N-floor)*P0[i][j]-QR[i][j] for j in range(N)] for i in range(N)])==N-1,'ENTIRE original repaired cap floor')
    return dict(status='PRIVATE EXACT FINITE PROBE ONLY; uniform old-cube cap UNPROVED; independent review pending',
                n=n,h=h,N=N,s=str(s),physical_dimension=size,all_original_entries=N*N,
                all_original_Gram_entries=size*size,all_original_frame_entries=size*size,
                original_deleted_principal=size,seed=seed,repaired=status,
                kappa=str(kappa),delta=str(delta),scaled_upper_gap_floor=str(floor),
                residual_scalars={key:str(p[key]) for key in ('mu','alpha','beta','nu')},
                entire_deleted_relation=True,both_maximum_star_kernels=True,
                lower_rank_comparison='Universal forced-star bound N-2 applies, but ordinary attainment for n>=3 is already9361 strict prior art.'),repaired

def alarm(signum,frame):
    raise TimeoutError('unchanged literal60s guard; unfinished is not nonexistence')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--n',type=int,required=True);parser.add_argument('--h',type=int,required=True)
    args=parser.parse_args();require((args.n,args.h) in ((2,2),(3,2)),'only next bounded original probes authorized here')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    out,M=actual(args.n,args.h)
    if args.n==2:
        require(out['repaired']['matrix_sha256']=='9d60249fa4b4afe7efc7daa93eb1f94c305870cd90bca92f7b2f08fc9b22cd13','entire published baseline original matrix')
        out['entire_published_n2_original_matrix_hash_equal']=True
    out['execution']=dict(seconds=time.monotonic()-start,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                          optimized=not __debug__,one_mathematical_child=True,native_threads={name:os.environ[name] for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')})
    signal.alarm(0)
    destination=Path(__file__).resolve().parent/'work'/f'probe-n{args.n}-h{args.h}-{"O" if not __debug__ else "normal"}.json'
    destination.write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps(out,default=str))
