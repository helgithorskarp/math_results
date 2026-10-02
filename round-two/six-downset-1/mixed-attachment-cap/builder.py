"""Bounded literal mixed-profile builder, credited to source c718a6f93f944d1a7513856d2e9c2233743a125c. No function changes.

The exact primitives are credited to published source8a32f730...,
triangle-profile-cap/exact.py. Baseline projection formulas specialize to
the prior9408 mixed facet seed; the new mean-orthogonal residual is a
restricted hypothesis, not a complete feasibility search.
"""
from pathlib import Path
from fractions import Fraction as F
import sys, json, signal, time, resource
sys.path.insert(0, str(Path(__file__).resolve().parent))
from exact import require, gram, matvec, dot, vecadd, scale, unit, psd_rank, lift, check, fingerprint

def build(n, r, l, own_leaf=None, class_full=None, class_pendant=None, mean_recipe='legacy'):
    require(type(n) is int and 3 <= n <= 6, 'literal order guard')
    require(type(r) is int and type(l) is int and r >= 1 and l >= 1 and r+l <= n,
            'two positive distinct-mark classes')
    require(mean_recipe in ('legacy','cap-min','cap-harmonic'),'mean recipe')
    q=1<<(n-1); s=q+3; w=F(q+2); N=2*q+6*r+2*l
    require(N<=80, 'literal N80 guard')
    old=list(range(1,2*q)); oldN=len(old); full=2*q-1; m=3*r+l; ell=m+1; dim=oldN+m
    C0=[[F(s*(a==b)+(q-3)*(a^b==full)-1) for b in old] for a in old]
    H=[[-F(bool(a&(1<<j))) for a in old] for j in range(r+l)]
    marks=[j for j in range(r) for _ in range(3)]+list(range(r,r+l))
    co=[unit(oldN,i) for i in range(oldN)]+[scale(F(1,3),H[j]) for j in marks]
    residual=[[F(0)]*dim for _ in range(dim)]
    for i in range(m):
        for j in range(m):
            if marks[i]==marks[j]: residual[oldN+i][oldN+j]=F(s)*((i==j)-F(1,3))
    B=gram(C0,co,residual)
    G=[F(i<oldN) for i in range(dim)]
    V=[unit(dim,oldN+i) for i in range(m)]
    h=[scale(F(1,3),vecadd(*V[3*j:3*j+3])) for j in range(r)]
    T=[vecadd(V[3*j+a],scale(-1,h[j])) for j in range(r) for a in range(3)]
    havg=scale(F(1,r),vecadd(*h)); vavg=scale(F(1,l),vecadd(*V[3*r:]))
    rho=F(q-1,q+1); E=vecadd(havg,scale(-rho,vavg)); K=vecadd(G,*V)
    d=F(3*(q-ell-1),ell*q); g=F(q-ell+1,ell*(q+2))
    D=d if class_full is None else F(class_full)
    Fp=-g/rho if class_pendant is None else F(class_pendant)
    A=(-D-F(l,r)*Fp)/2
    require(r!=1 or D==d, 'r1 class full fixed by support')
    require(l!=1 or Fp==-g/rho, 'l1 class pendant fixed by support')
    a=A if r==1 else (-d/3 if own_leaf is None else F(own_leaf))
    require(r!=1 or own_leaf is None or F(own_leaf)==a,'r1 own leaf fixed by balance')
    a_std=(r*a-A)/(r-1) if r>1 else F(0)
    d_std=(r*d-D)/(r-1) if r>1 else F(0)
    g_std=(l*g+rho*Fp)/(l-1) if l>1 else F(0)
    c=(a-d)*q/s
    common=scale(F(-1,ell),K)
    P=[]
    for i in range(r):
        Di=vecadd(h[i],scale(-1,havg))
        leaf=vecadd(common,scale(A,E),scale(a_std,Di))
        transfer=vecadd(*(T[3*j+2] for j in range(r) if j!=i)) if r>1 else [F(0)]*dim
        P.extend([vecadd(leaf,scale(c,T[3*i+1])),vecadd(leaf,scale(c,T[3*i])),
                  vecadd(common,scale(D,E),scale(d_std,Di),scale(c/F(r+l-1),transfer))])
    for j in range(l):
        Lj=vecadd(V[3*r+j],scale(-1,vavg))
        P.append(vecadd(common,scale(Fp,E),scale(g_std,Lj),
                       scale(c/F(r+l-1),vecadd(*(T[3*i+2] for i in range(r))))))
    require(vecadd(*P)==scale(F(-m,ell),K), 'exact private projection balance')
    require(dot(K,matvec(B,K))==F(ell*q+2-6*r), 'actual mixed K norm')
    for p in P:
        require(dot(K,matvec(B,vecadd(p,scale(F(1,ell),K))))==0, 'K orthogonal contrast')
    for i in range(r):
        for a0 in range(3):
            for b0 in range(3):
                if a0==2 or b0==2 or a0==b0:
                    require(dot(P[3*i+a0],matvec(B,V[3*i+b0]))==-1,'every own triangle marked support')
    for j in range(l): require(dot(P[3*r+j],matvec(B,V[3*r+j]))==-1,'every pendant marked support')
    PG=gram(B,P,[[F(0)]*m for _ in range(m)])
    etaL=w-PG[0][0]; etaF=w-PG[2][2]; etaP=w-PG[3*r][3*r]
    R=-1-PG[0][2]; mu=(2*R+etaF)/3; alpha=2*(2*etaL-R-etaF); beta=etaF-mu
    pars=dict(n=n,r=r,l=l,q=q,N=N,m=m,s=s,d=d,g=g,A=A,D=D,Fp=Fp,a=a,c=c,
              etaL=etaL,etaF=etaF,etaP=etaP,R=R,mu=mu,alpha=alpha,beta=beta)
    # A deliberately restricted residual with class means orthogonal to
    # local internal triangle directions. Failure is only failure of this model.
    W=[[F(0)]*m for _ in range(m)]
    if r==1: cross=3*mu/l
    elif l==1: cross=etaP/(3*r)
    else:
        first=3*r*mu/l;second=l*etaP/(3*r)
        if mean_recipe=='legacy':cross=min(first,second)/2
        elif mean_recipe=='cap-min':cross=min(first,second,F(q,m))/2
        else:cross=1/(2*(1/first+1/second+F(m,q)))
    a_mean=(l*cross-3*mu)/(3*(r-1)) if r>1 else None
    b_mean=(3*r*cross-etaP)/(l-1) if l>1 else None
    pars.update(cross=cross,a_mean=a_mean,b_mean=b_mean)
    for i in range(m):
        for j in range(m):
            if i<3*r and j<3*r:
                if i//3!=j//3: z=a_mean
                elif i==j: z=etaF if i%3==2 else etaL
                elif i%3==2 or j%3==2: z=R
                else: z=mu+(-alpha+beta)/4
            elif i>=3*r and j>=3*r: z=etaP if i==j else b_mean
            else: z=-cross
            require(z is not None,'nonexistent class standard accessed')
            W[i][j]=z
    if r==l==1:
        # Credited9408 baseline uses a nonorthogonal group mean/internal
        # coupling; etaP=9mu is NOT a necessary condition for any H seed.
        t=(etaF+2*R-etaP)/2
        W=[[etaL,-etaL-R-t,R,t],[-etaL-R-t,etaL,R,t],
           [R,R,etaF,-etaF-2*R],[t,t,-etaF-2*R,etaP]]
        pars['baseline_internal_mean_coupling']=True
    family=list(range(2*q))
    for j in range(r):
        u=1<<(n+2*j); v=1<<(n+2*j+1); mark=1<<j
        family.extend([u,mark|u,v,mark|v,u|v,mark|u|v])
    for j in range(l):
        bmask=1<<(n+2*r+j); mark=1<<(r+j)
        family.extend([bmask,mark|bmask])
    coeff=[unit(dim,i) for i in range(oldN)]
    for i in range(m): coeff.extend([P[i],V[i]])
    private=[oldN+2*i for i in range(m)]
    totalres=[[F(0)]*(N-1) for _ in range(N-1)]
    for i in range(m):
        for j in range(m): totalres[private[i]][private[j]]=W[i][j]
    C=gram(B,coeff,totalres)
    for i,A0 in enumerate(family[1:]):
        require(C[i][i]==w,'every nonempty norm')
        for j,B0 in enumerate(family[1:]):
            if i!=j and A0&B0:require(C[i][j]==-1,'every nonempty mandatory entry')
    return family,C,W,pars,B,P,V,K

def solve(A,b):
    A=[list(map(F,row))+[F(z)] for row,z in zip(A,b)];length=len(A)
    for j in range(length):
        i=next((i for i in range(j,length) if A[i][j]),None)
        require(i is not None,'invertible deleted residual')
        A[j],A[i]=A[i],A[j];z=A[j][j];A[j]=[x/z for x in A[j]]
        for i in range(length):
            if i!=j:
                z=A[i][j];A[i]=[x-z*y for x,y in zip(A[i],A[j])]
    return [row[-1] for row in A]

def record(n,r,l,mean_recipe='legacy'):
    family,C,W,p,*_=build(n,r,l,mean_recipe=mean_recipe)
    out={'parameters':{k:str(v) for k,v in p.items()},'support_exact':True,
         'W_row_sums':[str(sum(row)) for row in W], 'projection_scope':'specified class/standard coefficients only'}
    if any(sum(row) for row in W):
        out['status']='restricted residual not balanced';return out
    try: out['residual_rank']=psd_rank(W)
    except ValueError as e: out['status']='restricted residual failed: '+str(e);return out
    out['status']='strict original seed pending cap'
    M=lift(C,p['s']);out['seed']=check(family,M,p['s'])
    N=p['N']; Q=[[(N-p['s'])*M[i][j]+p['s']*int(i==j)-1 for j in range(N)] for i in range(N)]
    gap=[[F(N-1)*(int(i==j)-F(1,N))-Q[i][j] for j in range(N)] for i in range(N)]
    try: out['gap_rank']=psd_rank(gap);out['status']='whole seed cap gap>=1'
    except ValueError as e:
        out['status']='original H seed; gap1 failed: '+str(e);return out
    out['actual_empty_norm']=str(sum(map(sum,C)))
    out['expected_balanced_empty_norm']=str(F(p['m']+1,1)**-2*( (p['m']+1)*p['q']+2-6*r))
    out['gap_sha256']=fingerprint(gap)
    # Independent Gaussian deleted solve, compared to the scalar spectral
    # quadratic only on the mean-orthogonal new mixed profiles.
    m=p['m']; A=[row[:-1] for row in W[:-1]];u=[F(i<3) for i in range(m-1)]
    require(psd_rank(A)==m-1,'deleted strict residual PD')
    x=solve(A,u);kappa=dot(u,x);require(kappa>0,'positive inverse quadratic')
    if (r,l)!=(1,1):
        predicted=3/(r*l*p['cross'])
        if r>1: predicted+=(r-1)/(r*(p['mu']-p['a_mean']))
        if l>1: predicted+=9*(l-1)/(l*(p['etaP']-p['b_mean']))
        require(kappa==predicted,'mixed mean spectral inverse identity')
    delta=1/(12*N*(1+kappa));private=[2*p['q']-1+2*i for i in range(m)]
    repaired=[row[:] for row in C];RW=[row[:] for row in W];v=private[-1]
    for i in range(3):
        j=private[i];require(family[j+1]&family[v+1]==0,'actual repair entry free')
        repaired[j][v]+=delta;repaired[v][j]+=delta
        RW[i][-1]+=delta;RW[-1][i]+=delta
    require(psd_rank(RW)==m,'repaired residual PD')
    require(6*delta-kappa*delta**2>0,'exact repaired Schur positive')
    repairedM=lift(repaired,p['s']);out['repair']=check(family,repairedM,p['s'])
    require(out['repair']['lower_rank']==N-r,'greatest forced-star lower rank')
    require(out['repair']['upper_rank']==N-1,'simple unit eigenvalue')
    RQ=[[(N-p['s'])*repairedM[i][j]+p['s']*int(i==j)-1 for j in range(N)] for i in range(N)]
    RG=[[F(4*N-3,4)*(int(i==j)-F(1,N))-RQ[i][j] for j in range(N)] for i in range(N)]
    require(psd_rank(RG)==N-1,'entire repaired gap3/4 includes empty')
    out.update(kappa=str(kappa),delta=str(delta),repaired_gap='3/4',repaired_gap_sha256=fingerprint(RG))
    out['status']='literal repaired cap at greatest rank; no uniform theorem'
    return out
