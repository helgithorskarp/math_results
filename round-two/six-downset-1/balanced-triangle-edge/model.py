"""PRIVATE original n2 balanced-repeat candidate, not a uniform theorem."""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[name]='1'
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from fractions import Fraction as F
from exact import require,psd_rank,dot,matvec,unit,scale,vecadd,zero,lift,fingerprint,check
from linear import solve
import argparse,json,signal,time,resource

def construct(h):
    require(type(h) is int and 2<=h<=10,'unchanged literal h guard10')
    s=F(3*h+2);N=12*h+4;require(N<=80,'unchanged literal N guard80')
    w=s-1;ell=F(6*h+1);m=6*h;B2=s*F(h-1,3*h)
    a=F(9*h*h)/(ell*s*(h-1));b=-2*a;c=F(27*h)/(ell*s)
    common2=w/(ell*ell)
    etal=w-common2-a*a*B2-F(2,3)*s*c*c
    etaf=w-common2-b*b*B2-F(2,3)*s*c*c/(h-1)
    p=-1-common2-a*b*B2
    mu=(2*p+etaf)/3;alpha=2*(2*etal-p-etaf);beta=etaf-mu;nu=mu*F(2*h,2*h-1)
    require(min(mu,alpha,beta)>0,'candidate positive W scalar')
    size=12*h;wi=6*h+1;Gamma=zero(size,size)
    for i,value in enumerate((F(1),F(3*h),F(3*h))):Gamma[i][i]=value
    e=lambda i:unit(size,i)
    gp,h0,A=[e(i) for i in range(3)];Hx=vecadd(h0,A);Hy=vecadd(h0,scale(-1,A));K=vecadd(gp,h0);common=scale(-1/ell,K)
    Bs=[]
    for group in range(2):
        offset=3+group*(h-1)
        for i in range(h-1):
            for j in range(h-1):Gamma[offset+i][offset+j]=s/3*(F(i==j)-F(1,h))
        B=[e(offset+i) for i in range(h-1)];B.append(scale(-1,vecadd(*B)));Bs.append(B)
    ts=2*h+1;Ts=[]
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
    old=[vecadd(gp,scale(-1,A)),vecadd(gp,A),scale(-1,K)]
    require(vecadd(*(old+V))==K,'balanced total old plus marked K')
    require(not any(vecadd(old[0],old[2],*V[:3*h])) and not any(vecadd(old[1],old[2],*V[3*h:])),'two literal original maximum-star relations')
    R=old+V+U;images=[matvec(Gamma,r) for r in R]
    C=[[dot(r,v) for v in images] for r in R]
    whole=[common]+R;images_whole=[matvec(Gamma,r) for r in whole]
    require(not any(vecadd(*whole)),'actual empty is negative entire row sum')
    S=[[sum(v[i]*v[j] for v in images_whole) for j in range(size)] for i in range(size)]
    cap=[[(N-1)*Gamma[i][j]-S[i][j] for j in range(size)] for i in range(size)]
    params=dict(h=h,N=N,s=s,w=w,ell=ell,a=a,b=b,c=c,common=common2,etal=etal,etaf=etaf,p=p,mu=mu,alpha=alpha,beta=beta,nu=nu)
    return params,Gamma,S,cap,C,dict(R=R,P=P,V=V,U=U,W=W,wi=wi,Bs=Bs,Ts=Ts)

def whole_lift(C):
    sums=[sum(row) for row in C]
    return [[sum(sums)]+[-v for v in sums]]+[[-sums[i]]+row for i,row in enumerate(C)]

def actual(h):
    p,G,S,cap,C,v=construct(h);N=p['N'];s=p['s'];core=N-1
    old=[1,2,3];private=[];marked=[]
    for f in range(2*h):
        masks=[1<<(2+2*f),1<<(3+2*f),3<<(2+2*f)];private+=masks
        mark=1 if f<h else 2;marked.extend(mark|a for a in masks)
    family=[0]+old+marked+private;require(len(set(family))==N,'exact original distinct family')
    M=lift(C,s);Q=whole_lift(C);P0=[[F(i==j)-F(1,N) for j in range(N)] for i in range(N)]
    seed=check(family,M,s);require(psd_rank(C)==N-4,'balanced seed core rank')
    require(seed['lower_rank']==N-3 and seed['upper_rank']==N-1,'balanced seed endpoint ranks')
    require(psd_rank(G)==N-4,'full physical metric positive definite')
    require(psd_rank(cap)==N-4,'ENTIRE original physical cap floor1')
    require(psd_rank([[(N-1)*P0[i][j]-Q[i][j] for j in range(N)] for i in range(N)])==N-1,'ENTIRE original whole cap floor1')
    require(Q[0][0]==p['common'],'actual recomputed empty norm')
    # Reconstruct every physical basis vector from original row coefficients.
    e=lambda i:unit(core,i)
    gp=scale(F(1,2),vecadd(e(0),e(1)));A=scale(F(1,2),vecadd(e(1),scale(-1,e(0))));h0=vecadd(scale(-1,e(2)),scale(-1,gp))
    Hx=vecadd(h0,A);Hy=vecadd(h0,scale(-1,A));basis=[gp,h0,A];Bs=[]
    for group,H in enumerate((Hx,Hy)):
        avg=scale(F(1,3*h),H);B=[]
        for i in range(h):B.append(vecadd(scale(F(1,3),vecadd(*(e(3+3*(group*h+i)+a) for a in range(3)))),scale(-1,avg)))
        Bs.append(B);basis+=B[:-1]
    for group,H in enumerate((Hx,Hy)):
        avg=scale(F(1,3*h),H)
        for i in range(h):basis.extend(vecadd(e(3+3*(group*h+i)+a),scale(-1,avg),scale(-1,Bs[group][i])) for a in range(2))
    require(len(basis)==v['wi'],'every original projected coordinate alignment')
    offset=3+6*h
    for i in range(6*h-1):
        projection=vecadd(*(scale(a,b) for a,b in zip(v['P'][i][:v['wi']],basis[:v['wi']])))
        basis.append(vecadd(e(offset+i),scale(-1,projection)))
    original_images=[matvec(C,b) for b in basis]
    actualG=[[dot(a,image) for image in original_images] for a in basis]
    require(actualG==G,'ENTIRE original physical Gram correspondence')
    paired=[[-sum(row)]+row for row in original_images]
    actualS=[[dot(a,b) for b in paired] for a in paired]
    require(actualS==S,'ENTIRE physical frame including actual empty')
    last=core-1;keep=[i for i in range(core) if i not in (0,1,last)];A0=[[C[i][j] for j in keep] for i in keep]
    require(psd_rank(A0)==N-4,'direct original deleted principal positive definite')
    z=[F(6*h)/(6*h+1) if i==2 else F(-1) if offset<=i<last else F(0) for i in keep]
    b0=[C[i][last] for i in keep];require(matvec(A0,z)==b0 and dot(z,b0)==s-1,'entire original deleted-column dependency')
    r=[F(offset<=i<offset+3) for i in keep];rinv=solve(A0,r);kappa=dot(r,rinv)
    require(kappa==2/p['nu']+4/p['beta'] and dot(r,z)==-3,'original deleted inverse/overlap formula')
    delta=1/(4*(8+kappa));repaired_b=vecadd(b0,scale(delta,r));repaired_inv=vecadd(z,scale(delta,rinv))
    require(matvec(A0,repaired_inv)==repaired_b and s-1-dot(repaired_b,repaired_inv)==6*delta-kappa*delta*delta,'full original repair Schur identity')
    require(6*delta-kappa*delta*delta>0,'strict positive repair')
    sharp=[row[:] for row in C]
    for i in range(offset,offset+3):sharp[i][last]+=delta;sharp[last][i]+=delta
    for mark in (1,2):
        kernel=[F(bool(a&mark)) for a in family[1:]]
        require(not any(matvec(C,kernel)) and not any(matvec(sharp,kernel)),'BOTH literal star relations survive repair')
    repaired=lift(sharp,s);status=check(family,repaired,s)
    require(psd_rank(sharp)==N-3 and status['lower_rank']==N-2 and status['upper_rank']==N-1,'literal greatest balanced endpoint ranks')
    floor=1-8*delta;require(floor>F(3,4),'literal scaled gap')
    QS=whole_lift(sharp)
    require(psd_rank([[(N-floor)*P0[i][j]-QS[i][j] for j in range(N)] for i in range(N)])==N-1,'ENTIRE repaired whole cap floor')
    L=[[(N-s)*repaired[i][j]+s*F(i==j) for j in range(N)] for i in range(N)]
    for mark in (1,2):
        centered=[F(bool(a&mark))-s/N for a in family]
        require(not any(matvec(L,centered)),'both actual centered largest-star lower kernels')
    return dict(h=h,n=2,N=N,s=str(s),parameters={k:str(z) for k,z in p.items()},seed=seed,sharp=status,core_sha256=fingerprint(C),original_positions=N*N,full_physical_dimension=len(G),full_Gram_positions=len(G)**2,full_frame_positions=len(S)**2,direct_original_deleted_principal_dimension=N-4,kappa=str(kappa),delta=str(delta),floor=str(floor),two_original_star_kernels=True,actual_empty_recomputed=True,full_original_dependency_inverse_Schur_verified=True)

def main():
    def alarm(sig,frame):raise TimeoutError('unchanged60s balanced literal guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    state=Path('/scratch/research-team-sol61-six-20260929/state');require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational barrier')
    ap=argparse.ArgumentParser();ap.add_argument('--h',type=int,default=2);args=ap.parse_args()
    fixture=actual(args.h);signal.alarm(0)
    out=dict(agent='six-downset-1',role='researcher',scope='PRIVATE exact original balanced n2 fixture only; no uniform h theorem',fixture=fixture,seconds=time.monotonic()-start,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=sys.flags.optimize)
    root=Path(__file__).resolve().parent;(root/'work').mkdir(exist_ok=True)
    (root/'work'/f'original-h{args.h}-O{sys.flags.optimize}.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
    print(json.dumps(out,default=str))
if __name__=='__main__':main()
