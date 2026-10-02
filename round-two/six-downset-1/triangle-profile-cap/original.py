"""Literal original-set validation for the distinct-mark triangle candidate.

Bounded n<=6,N<=80. All-n reduced signs and the complete-space proof
are supplied separately by uniform.py and PROOF.md. Credited primitive operations are reused
from f8255e1d617237421c32b3d1e13dd865bffd50c4; not independent review.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import sys,json,signal,time,resource
from exact import require,gram,dot,matvec,vecadd,scale,unit,psd_rank,lift,check,nullspace,fingerprint
from sector import reduced

def build(n,k):
    require(type(n) is int and type(k) is int and 3<=n<=6 and 2<=k<=n,'literal mark/order domain')
    q=1<<(n-1);s=q+3;w=F(q+2);N=2*q+6*k;ell=3*k+1
    require(N<=80,'original N80 guard')
    old=list(range(1,2*q));oldN=len(old);full=2*q-1;m=oldN+3*k
    C0=[[F(s*(a==b)+(q-3)*(a^b==full)-1) for b in old] for a in old]
    H=[[-F(bool(a&(1<<j))) for a in old] for j in range(k)]
    co=[unit(oldN,i) for i in range(oldN)]+[scale(F(1,3),H[j]) for j in range(k) for _ in range(3)]
    residual=[[F(0)]*m for _ in range(m)]
    for j in range(k):
        for a in range(3):
            for b in range(3):residual[oldN+3*j+a][oldN+3*j+b]=F(s)*((a==b)-F(1,3))
    B=gram(C0,co,residual)
    G=[F(i<oldN) for i in range(m)]
    V=[unit(m,oldN+i) for i in range(3*k)]
    h=[scale(F(1,3),vecadd(*V[3*j:3*j+3])) for j in range(k)]
    T=[vecadd(V[3*j+a],scale(-1,h[j])) for j in range(k) for a in range(3)]
    K=vecadd(G,*V)
    d=F(3*(q-3*k-2),ell*q);a=-d/3;c=(a-d)*q/s
    P=[]
    for j in range(k):
        difference=vecadd(h[j],scale(F(-1,k-1),vecadd(*(h[l] for l in range(k) if l!=j))))
        common=scale(F(-1,ell),K)
        transfer=scale(F(1,k-1),vecadd(*(T[3*l+2] for l in range(k) if l!=j)))
        P.extend([vecadd(common,scale(a,difference),scale(c,T[3*j+1])),
                  vecadd(common,scale(a,difference),scale(c,T[3*j])),
                  vecadd(common,scale(d,difference),scale(c,transfer))])
    Pgram=gram(B,P,[[F(0)]*(3*k) for _ in range(3*k)])
    etaL=w-Pgram[0][0];etaF=w-Pgram[2][2];r=-1-Pgram[0][2]
    mu=(2*r+etaF)/3;cross=-etaL+r+etaF
    W=[[F(0)]*(3*k) for _ in range(3*k)]
    for i in range(3*k):
        for j in range(3*k):
            if i==j:W[i][j]=etaF if i%3==2 else etaL
            elif i//3!=j//3:W[i][j]=-mu/(k-1)
            elif i%3==2 or j%3==2:W[i][j]=r
            else:W[i][j]=cross
    require(all(sum(row)==0 for row in W),'complete balanced residual')
    coeff=[unit(m,i) for i in range(oldN)]
    for i in range(3*k):coeff.extend([P[i],V[i]])
    family=list(range(2*q))
    for j in range(k):
        u=1<<(n+2*j);v=1<<(n+2*j+1);mark=1<<j
        family.extend([u,mark|u,v,mark|v,u|v,mark|u|v])
    totalres=[[F(0)]*(N-1) for _ in range(N-1)]
    private=[oldN+2*i for i in range(3*k)]
    for i in range(3*k):
        for j in range(3*k):totalres[private[i]][private[j]]=W[i][j]
    C=gram(B,coeff,totalres)
    require(all(C[i][i]==w for i in range(N-1)),'every original nonempty norm')
    for i,A in enumerate(family[1:]):
        for j,Bmask in enumerate(family[1:]):
            if i!=j and A&Bmask:require(C[i][j]==-1,'every original mandatory support Gram')
    require(sum(map(sum,C))==F(ell*q+2-6*k,ell**2),'ACTUAL empty seed norm')
    # Independent original core coefficient features recover residual vectors
    # by subtracting each displayed base projection from its actual private row.
    def embed(v):
        out=[F(0)]*(N-1)
        out[:oldN]=v[:oldN]
        for i in range(3*k):out[oldN+2*i+1]=v[oldN+i]
        return out
    actualW=[vecadd(unit(N-1,private[i]),scale(-1,embed(P[i]))) for i in range(3*k)]
    actualH=[[-F(i<oldN and bool(old[i]&(1<<j))) for i in range(N-1)] for j in range(k)]
    actualG=[F(i<oldN) for i in range(N-1)];actualf=unit(N-1,oldN-1)
    gp=scale(F(1,2),vecadd(actualG,scale(-1,actualf)))
    h0=scale(F(-1,2),vecadd(actualG,actualf))
    As=[vecadd(z,scale(-1,h0)) for z in actualH]
    Tas=[embed(vecadd(T[3*j],scale(-1,T[3*j+1]))) for j in range(k)]
    Tss=[embed(vecadd(T[3*j],T[3*j+1],scale(-2,T[3*j+2]))) for j in range(k)]
    Was=[vecadd(actualW[3*j],scale(-1,actualW[3*j+1])) for j in range(k)]
    means=[scale(F(1,3),vecadd(*actualW[3*j:3*j+3])) for j in range(k)]
    Wfs=[vecadd(actualW[3*j+2],scale(-1,means[j])) for j in range(k)]
    sectors={'anti':[Tas[0],Was[0]],
             'fixed':[gp,h0,vecadd(*As),vecadd(*Tss),vecadd(*Wfs)],
             'standard':[vecadd(As[0],scale(-1,As[1])),vecadd(Tss[0],scale(-1,Tss[1])),
                         vecadd(means[0],scale(-1,means[1])),vecadd(Wfs[0],scale(-1,Wfs[1]))]}
    changed=[gp,h0]+As+Tas+Tss+Was+Wfs+[vecadd(means[j],scale(-1,means[-1])) for j in range(k-1)]
    return family,s,C,W,private,sectors,changed,{'n':n,'k':k,'q':q,'N':N,'etaL':etaL,'etaF':etaF,'r':r,'mu':mu}

def form(C,coeff):
    images=[matvec(C,v) for v in coeff]
    Gamma=[[dot(v,image) for image in images] for v in coeff]
    frame=[[dot(u,v)+sum(u)*sum(v) for v in images] for u in images]
    return Gamma,frame

def original(n,k):
    family,s,C,W,private,sectors,changed,p=build(n,k)
    q,N=p['q'],p['N'];m=3*k
    prediction=reduced(q,k)
    require([p[x] for x in ['etaL','etaF','r','mu']]==[prediction['parameters'][x] for x in ['etaL','etaF','r','mean_norm']], 'residual scalars match original pairings')
    sector_positions=0
    for label,coeff in sectors.items():
        G,S=form(C,coeff);expected=prediction[label]
        require(G==expected[0] and S==expected[1],'EVERY literal original reduced Gram/frame position '+label)
        sector_positions+=len(coeff)**2
    Gamma,frame=form(C,changed)
    changed_dimension=6*k+1
    require(len(changed)==changed_dimension and psd_rank(Gamma)==changed_dimension,'independent complete changed-space Gram')
    B=[[(N-1)*Gamma[i][j]-frame[i][j] for j in range(changed_dimension)] for i in range(changed_dimension)]
    require(psd_rank(B)==changed_dimension,'whole literal changed cap with ACTUAL empty frame')
    seed=lift(C,s)
    seed_report=check(family,seed,s)
    require(seed_report['lower_rank']==N-k-1 and seed_report['upper_rank']==N-1,'literal seed ranks')
    def wholeQ(M):return [[(N-s)*M[i][j]+s*int(i==j)-1 for j in range(N)] for i in range(N)]
    Q=wholeQ(seed)
    gap=[[N*(int(i==j)-F(1,N))-Q[i][j]-(int(i==j)-F(1,N)) for j in range(N)] for i in range(N)]
    require(psd_rank(gap)==N-1,'whole actual seed gap>=1')
    pairs=[(a,(2*q-1)^a) for a in range(1,2*q-1) if a<((2*q-1)^a)]
    high=[];low=[]
    for a,b in pairs[1:]:
        v=[F(0)]*N
        for A in [a,b]:v[A]+=1
        for A in pairs[0]:v[A]-=1
        high.append(v)
    kernel=nullspace([[F(bool(a&(1<<j)))-F(bool(b&(1<<j))) for a,b in pairs] for j in range(k)],len(pairs))
    for row in kernel:
        v=[F(0)]*N
        for z,(a,b) in zip(row,pairs):v[a]+=z;v[b]-=z
        low.append(v)
    require(len(high)==q-2 and len(low)==q-k-1,'exact untouched counts')
    for vectors,eigenvalue in [(high,2*q),(low,6)]:
        for v in vectors:require(matvec(Q,v)==scale(eigenvalue,v),'full actual untouched eigenaction including empty/new rows')
    # Explicit inverse action for the deleted balanced residual principal.
    # u is the first group's three private rows; v the last full private row.
    nu=prediction['parameters']['k']*p['mu']/(k-1)
    full=prediction['parameters']['full_norm']
    x=[F(1,3)/nu+F(4,3)/full]*m
    for i in range(3):x[i]=F(2,3)/nu+F(4,3)/full
    x[-3]=x[-2]=2/full;x[-1]=F(0)
    target=[F(i<3) for i in range(m)];target[-1]=F(-3)
    require(matvec(W,x)==target,'complete residual inverse action identity, no large inverse')
    kappa=2/nu+4/full
    require(sum(x[:3])==kappa and kappa>0,'exact inverse quadratic')
    delta=1/(12*N*(1+kappa))
    repaired=[row[:] for row in C];repairedW=[row[:] for row in W]
    v=private[-1]
    for i in range(3):
        u=private[i];require(family[u+1]&family[v+1]==0,'modified actual entry is free')
        repaired[u][v]+=delta;repaired[v][u]+=delta
        repairedW[i][-1]+=delta;repairedW[-1][i]+=delta
    require(psd_rank(W)==m-1 and psd_rank(repairedW)==m,'balanced residual rank and repaired PD')
    require(6*delta-kappa*delta*delta>0,'repaired Schur scalar')
    M=lift(repaired,s);repair_report=check(family,M,s)
    require(repair_report['lower_rank']==N-k and repair_report['upper_rank']==N-1,'whole repaired H ranks')
    repairedQ=wholeQ(M)
    cap=[[N*(int(i==j)-F(1,N))-repairedQ[i][j]-F(3,4)*(int(i==j)-F(1,N)) for j in range(N)] for i in range(N)]
    require(psd_rank(cap)==N-1,'whole repaired actual gap>=3/4')
    return {'n':n,'k':k,'q':q,'N':N,'s':s,'reduced_Gram_positions':sector_positions,
            'reduced_frame_positions':sector_positions,'changed_dimension':changed_dimension,
            'changed_Gram_positions':changed_dimension**2,'changed_frame_positions':changed_dimension**2,
            'untouched_high_count':len(high),'untouched_low_count':len(low),
            'seed_lower_rank':seed_report['lower_rank'],'seed_upper_rank':seed_report['upper_rank'],
            'seed_matrix_sha256':seed_report['matrix_sha256'],'repair':repair_report,
            'kappa':str(kappa),'delta':str(delta),'repaired_cap_sha256':fingerprint(cap),
            'scaled_seed_gap':'1','scaled_repaired_gap':'3/4','full_original_positions':N*N}
