"""PRIVATE complete original repeated-count candidate. No uniform cap theorem.

Six native thread variables are one; literal fixtures stay at n<=6,N<=80.
The recipe is the saved next-frontier algebra, not an independent discovery.
"""
import os
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
    os.environ[name]='1'
from fractions import Fraction as F
from pathlib import Path
import sys,json,signal,time,resource
from exact import require,psd_rank,dot,matvec,gram,unit,scale,vecadd,zero,lift,fingerprint,check
from linear import solve
from recipe import recipe

def construct(h,q):
    require(type(h) is int and 2<=h<=10,'bounded literal heavy multiplicity')
    q=F(q);require(q>=4,'candidate original q domain')
    p=recipe(F(h),q);s,w,N=[p[z] for z in ('s','w','N')];size=6*h+8
    Gamma=zero(size,size)
    Gamma[0][0]=q-1;Gamma[1][1]=3*h
    Gamma[2][2]=Gamma[3][3]=3*h*(q-1);Gamma[2][3]=Gamma[3][2]=-3*h
    for i in range(h-1):
        for j in range(h-1):Gamma[4+i][4+j]=s/3*(F(i==j)-F(1,h))
    heavyT=[h+3+2*i for i in range(h)];yi=3*h+3;lightT=yi+1;wi=3*h+6
    Gamma[yi][yi]=s*F(h-1,3*h)
    for start in heavyT+[lightT]:
        Gamma[start][start]=Gamma[start+1][start+1]=2*s/3
        Gamma[start][start+1]=Gamma[start+1][start]=-s/3
    e=lambda i:unit(size,i)
    gp,h0,Ax,Ay=[e(i) for i in range(4)]
    Hx=vecadd(h0,Ax);Hy=vecadd(h0,Ay);hx=scale(F(1,3*h),Hx);hy=scale(F(1,3*h),Hy)
    B=[e(4+i) for i in range(h-1)];B.append(scale(-1,vecadd(*B)));Y=e(yi)
    Ts=[[e(start),e(start+1),scale(-1,vecadd(e(start),e(start+1)))] for start in heavyT+[lightT]]
    VbarL=vecadd(hy,Y);E=vecadd(hx,scale(-p['rho'],VbarL))
    K=vecadd(gp,scale(-1,h0),Hx,scale(F(1,h),Hy),scale(3,Y))
    common=scale(F(-1,3*h+4),K)
    V=[]
    for i in range(h):V.extend(vecadd(hx,B[i],Ts[i][a]) for a in range(3))
    V.extend(vecadd(VbarL,Ts[h][a]) for a in range(3))
    P=[]
    for i in range(h):
        P.extend(vecadd(common,scale(p['A'],E),scale(p['a'],B[i]),scale(p['cH'],Ts[i][1-a])) for a in range(2))
        P.append(vecadd(common,scale(p['b'],B[i]),scale(p['cH']/F(h-1),vecadd(*(Ts[j][2] for j in range(h) if j!=i))),scale(p['cL']/h,Ts[h][2])))
    P.extend(vecadd(common,scale(p['FF'],E),scale(p['cL'],Ts[h][1-a])) for a in range(2))
    P.append(vecadd(common,scale(p['G'],E)))
    require(vecadd(*P)==scale(F(-3*(h+1),3*h+4),K),'ENTIRE general projection balance')
    count=3*(h+1);W=zero(count,count)
    for i in range(count):
        fi,ai=divmod(i,3)
        for j in range(count):
            fj,aj=divmod(j,3)
            if fi!=fj:z=(p['muL']/h-p['muH'])/(h-1) if fi<h and fj<h else -p['muL']/h
            else:
                mu,alpha,beta=[p[name+('H' if fi<h else 'L')] for name in ['mu','alpha','beta']]
                wa=[F(1,2),F(-1,2),F(0)];wf=[F(-1,2),F(-1,2),F(1)]
                z=mu+wa[ai]*wa[aj]*alpha+wf[ai]*wf[aj]*beta
            W[i][j]=z
    require(all(sum(row)==0 for row in W),'ENTIRE general residual balance')
    for i in range(count-1):
        for j in range(count-1):Gamma[wi+i][wi+j]=W[i][j]
    Wrows=[e(wi+i) for i in range(count-1)];Wrows.append(scale(-1,vecadd(*Wrows)))
    U=[vecadd(a,b) for a,b in zip(P,Wrows)]
    S=zero(size,size);S[0][0]=q*q-1;S[1][1]=9*h*h;S[0][1]=S[1][0]=3*h*(q-1)
    for i in [2,3]:
        for j in [2,3]:S[i][j]=6*h*Gamma[i][j]
    for row in V+U+[common]:
        x=matvec(Gamma,row)
        for i in range(size):
            for j in range(size):S[i][j]+=x[i]*x[j]
    cap=[[(N-1)*Gamma[i][j]-S[i][j] for j in range(size)] for i in range(size)]
    return p,Gamma,S,cap,dict(V=V,P=P,U=U,empty=common,K=K,W=W,Ts=Ts,B=B,E=E,Y=Y,Wrows=Wrows,wi=wi)

def whole_lift(C):
    sums=[sum(row) for row in C]
    return [[sum(sums)]+[-z for z in sums]]+[[-sums[i]]+row for i,row in enumerate(C)]

def actual(h,n):
    require(3<=n<=6,'unchanged literal n6 guard');q=1<<(n-1);N=2*q+6*h+6;require(N<=80,'unchanged literal N80 guard')
    p,G,S,cap,v=construct(h,q);size=N-1;old=list(range(1,2*q));marked=[];private=[]
    for i in range(h+1):
        masks=[1<<(n+2*i),1<<(n+2*i+1),3<<(n+2*i)];private+=masks
        mark=1<<(0 if i<h else 1);marked.extend(mark|a for a in masks)
    family=[0]+old+marked+private;require(len(set(family))==N,'distinct literal sets')
    C=zero(size,size);full=2*q-1;D=3*h
    for i,A in enumerate(old):
        for j,B in enumerate(old):C[i][j]=p['s']*(A==B)+(q-D)*(A^B==full)-1
    newvec=v['V']+v['U'];images=[matvec(G,z) for z in newvec]
    for i,A in enumerate(old):
        for j,z in enumerate(newvec):
            pairing=z[0]+D*z[2]*(1-2*bool(A&1))+D*z[3]*(1-2*bool(A&2)) if A!=full else -(q-1)*z[0]-D*z[1]
            C[i][len(old)+j]=C[len(old)+j][i]=pairing
    for i,z in enumerate(newvec):
        for j,x in enumerate(newvec):C[len(old)+i][len(old)+j]=dot(z,images[j])
    Q=whole_lift(C);M=lift(C,p['s']);P0=[[F(i==j)-F(1,N) for j in range(N)] for i in range(N)]
    seed=check(family,M,p['s']);require(psd_rank(C)==N-3,'ENTIRE seed core rank')
    require(psd_rank([[(N-1)*P0[i][j]-Q[i][j] for j in range(N)] for i in range(N)])==N-1,'ENTIRE literal cap floor1')
    require(Q[0][0]==p['common'],'actual empty row norm and loop')
    ec=lambda i:unit(size,i)
    oldG=vecadd(*(ec(i) for i in range(len(old))));oldf=ec(len(old)-1)
    gp=scale(F(1,2),vecadd(oldG,scale(-1,oldf)));h0=scale(F(-1,2),vecadd(oldG,oldf))
    Hx=scale(-1,vecadd(*(ec(i) for i,A in enumerate(old) if A&1)));Hy=scale(-1,vecadd(*(ec(i) for i,A in enumerate(old) if A&2)))
    hx=scale(F(1,D),Hx);hy=scale(F(1,D),Hy)
    basis=[gp,h0,vecadd(Hx,scale(-1,h0)),vecadd(Hy,scale(-1,h0))]
    count=3*(h+1);V=[ec(len(old)+i) for i in range(count)];U=[ec(len(old)+count+i) for i in range(count)]
    Bs=[vecadd(scale(F(1,3),vecadd(*V[3*i:3*i+3])),scale(-1,hx)) for i in range(h)]
    basis+=Bs[:-1]
    for i in range(h):basis.extend(vecadd(V[3*i+a],scale(-1,hx),scale(-1,Bs[i])) for a in range(2))
    Y=vecadd(scale(F(1,3),vecadd(*V[3*h:])),scale(-1,hy));basis.append(Y)
    basis.extend(vecadd(V[3*h+a],scale(-1,hy),scale(-1,Y)) for a in range(2))
    olddim=len(basis);require(olddim==v['wi'],'EVERY original basis position alignment')
    for i in range(count-1):
        projection=vecadd(*(scale(a,b) for a,b in zip(v['P'][i][:olddim],basis[:olddim])))
        basis.append(vecadd(U[i],scale(-1,projection)))
    images_basis=[matvec(C,z) for z in basis]
    actualG=[[dot(a,z) for z in images_basis] for a in basis];require(actualG==G,'ENTIRE literal physical Gram correspondence')
    pairings=[[-sum(z)]+z for z in images_basis]
    actualS=[[dot(a,b) for b in pairings] for a in pairings];require(actualS==S,'ENTIRE physical frame including actual empty')
    require(psd_rank(G)==6*h+8 and psd_rank(cap)==6*h+8,'complete changed space positive definite')
    smallW=[row[:-1] for row in v['W'][:-1]];rhs=[F(i<3) for i in range(count-1)];kappa=dot(rhs,solve(smallW,rhs))
    require(kappa==F(h-1,h)/p['nu']+1/p['muL']+4/p['betaL'],'general deleted inverse formula')
    delta=1/(4*(8+kappa));require(6*delta-kappa*delta*delta>0,'positive rank-raising Schur')
    sharp=[row[:] for row in C];offset=len(old)+count;last=offset+count-1
    for i in range(offset,offset+3):sharp[i][last]+=delta;sharp[last][i]+=delta
    MS=lift(sharp,p['s']);QS=whole_lift(sharp);status=check(family,MS,p['s'])
    require(psd_rank(sharp)==N-2 and status['lower_rank']==N-1,'greatest literal lower rank')
    floor=1-8*delta;require(floor>F(3,4),'literal cap gap')
    require(psd_rank([[(N-floor)*P0[i][j]-QS[i][j] for j in range(N)] for i in range(N)])==N-1,'ENTIRE sharp cap lower bound')
    star=[F(bool(A&1))-F(p['s'],N) for A in family]
    L=[[(N-p['s'])*MS[i][j]+p['s']*(i==j) for j in range(N)] for i in range(N)]
    require(not any(matvec(L,star)),'actual heavy maximum-star kernel')
    return dict(h=h,n=n,q=q,N=N,s=str(p['s']),seed=seed,sharp=status,core_sha256=fingerprint(C),sharp_sha256=fingerprint(MS),original_positions=N*N,physical_Gram_positions=len(G)**2,physical_frame_positions=len(S)**2,kappa=str(kappa),delta=str(delta),floor=str(floor))

def main():
    def alarm(signum,frame):raise TimeoutError('unchanged60s original-count guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--h',type=int,default=3);ap.add_argument('--n',type=int,default=3);args=ap.parse_args()
    out=actual(args.h,args.n);signal.alarm(0)
    result=dict(agent='six-downset-1',role='researcher',status='PRIVATE literal construction only; arbitrary h cap not proved',fixture=out)
    Path(f'work/original-h{args.h}-n{args.n}.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
    print(json.dumps(result,default=str))
if __name__=='__main__':main()
