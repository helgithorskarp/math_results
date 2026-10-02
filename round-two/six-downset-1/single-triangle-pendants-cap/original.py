"""Bounded original sets/vectors and full-matrix control of the uniform proof.

Uses no reduced formula to construct the seed. Actual n<=6,N<=80 guards
are retained. Larger theorem parameters are covered by PROOF.md and the
uniform signs, not by larger literal matrices.
"""
from fractions import Fraction as F
from exact import require,gram,matvec,dot,vecadd,scale,unit,zero,psd_rank,lift,check,fingerprint,nullspace
from model import reduced,fixed

def build(n,l):
    require(type(n) is int and 3<=n<=6,'literal order3..6 guard')
    require(type(l) is int and 2<=l<=n-1,'distinct one-triangle/pendant marks')
    q=1<<(n-1);s=q+3;w=F(q+2);N=2*q+6+2*l;m=3+l;ell=m+1
    require(N<=80,'literal N80 guard')
    old=list(range(1,2*q));oldN=len(old);full=2*q-1;dim=oldN+m
    C0=[[F(s*(a==b)+(q-3)*(a^b==full)-1) for b in old] for a in old]
    H=[[-F(bool(a&(1<<j))) for a in old] for j in range(l+1)]
    marks=[0,0,0]+list(range(1,l+1))
    co=[unit(oldN,i) for i in range(oldN)]+[scale(F(1,3),H[j]) for j in marks]
    res=zero(dim)
    for i in range(m):
        for j in range(m):
            if marks[i]==marks[j]:res[oldN+i][oldN+j]=F(s)*((i==j)-F(1,3))
    B=gram(C0,co,res)
    G=[F(i<oldN) for i in range(dim)]
    V=[unit(dim,oldN+i) for i in range(m)]
    h=scale(F(1,3),vecadd(*V[:3]));v=scale(F(1,l),vecadd(*V[3:]))
    T=[vecadd(a,scale(-1,h)) for a in V[:3]]
    rho=F(q-1,q+1);E=vecadd(h,scale(-rho,v));K=vecadd(G,*V)
    d=F(3*(q-ell-1),ell*q);g=F(q-ell+1,ell*(q+2));Fp=-g/rho
    A=(-d-l*Fp)/2;c=(A-d)*q/s;common=scale(F(-1,ell),K)
    leaf=vecadd(common,scale(A,E))
    P=[vecadd(leaf,scale(c,T[1])),vecadd(leaf,scale(c,T[0])),vecadd(common,scale(d,E))]
    for j in range(l):
        P.append(vecadd(common,scale(Fp,E),scale(g,vecadd(V[3+j],scale(-1,v))),scale(c/l,T[2])))
    require(vecadd(*P)==scale(F(-m,ell),K),'every actual private projection balanced')
    require(dot(K,matvec(B,K))==F(ell*q-4),'actual K norm')
    for projection in P:
        require(dot(K,matvec(B,vecadd(projection,scale(F(1,ell),K))))==0,'K orthogonal contrast')
    PG=gram(B,P,zero(m));etaL=w-PG[0][0];etaF=w-PG[2][2];etaP=w-PG[3][3]
    pair=-1-PG[0][2];mu=(2*pair+etaF)/3;alpha=2*(2*etaL-pair-etaF);beta=etaF-mu
    Cmean=3*mu/l;bmean=(3*Cmean-etaP)/(l-1);nuL=etaP-bmean
    W=zero(m)
    for i in range(m):
        for j in range(m):
            if i<3 and j<3:
                if i==j:z=etaF if i==2 else etaL
                elif i==2 or j==2:z=pair
                else:z=mu+(-alpha+beta)/4
            elif i>=3 and j>=3:z=etaP if i==j else bmean
            else:z=-Cmean
            W[i][j]=z
    require(all(sum(row)==0 for row in W),'all original residual rows balanced')
    family=list(range(2*q));u=1<<n;b=1<<(n+1);mark=1
    family.extend([u,mark|u,b,mark|b,u|b,mark|u|b])
    for j in range(l):
        bmask=1<<(n+2+j);mark=1<<(j+1);family.extend([bmask,mark|bmask])
    coeff=[unit(dim,i) for i in range(oldN)]
    for i in range(m):coeff.extend([P[i],V[i]])
    totalres=zero(N-1);private=[oldN+2*i for i in range(m)]
    for i in range(m):
        for j in range(m):totalres[private[i]][private[j]]=W[i][j]
    core=gram(B,coeff,totalres)
    for i,a in enumerate(family[1:]):
        require(core[i][i]==w,'actual nonempty norm')
        for j,b in enumerate(family[1:]):
            if i!=j and a&b:require(core[i][j]==-1,'actual mandatory intersection entry')
    p=dict(n=n,l=l,q=q,N=N,m=m,ell=ell,s=s,d=d,g=g,Fp=Fp,A=A,c=c,
           etaL=etaL,etaF=etaF,etaP=etaP,pair=pair,mu=mu,alpha=alpha,beta=beta,
           cross=Cmean,b_mean=bmean,nuL=nuL)
    return family,core,W,p,B,P,V,K

def solve(A,b):
    """Independent Fraction Gaussian solve, not the3x3 adjugate."""
    A=[list(map(F,row))+[F(z)] for row,z in zip(A,b)];length=len(A)
    for j in range(length):
        i=next((i for i in range(j,length) if A[i][j]),None)
        require(i is not None,'invertible deleted residual')
        A[j],A[i]=A[i],A[j];z=A[j][j];A[j]=[x/z for x in A[j]]
        for i in range(length):
            if i!=j:
                z=A[i][j];A[i]=[x-z*y for x,y in zip(A[i],A[j])]
    return [row[-1] for row in A]

def forms(C,vs):
    images=[matvec(C,v) for v in vs]
    G=[[dot(v,x) for x in images] for v in vs]
    S=[[dot(u,v)+sum(u)*sum(v) for v in images] for u in images]
    return G,S

def original(n,l):
    family,C,W,p,B,P,V,K=build(n,l);N=p['N'];q=p['q'];m=p['m'];oldN=2*q-1
    small,expected=reduced(q,l)
    for name in ('d','g','A','Fp','c','etaL','etaF','etaP','mu','alpha','beta','nuL'):
        require(p[name]==expected[name],'independent original/reduced parameter '+name)
    def embed(v):
        out=[F(0)]*(N-1);out[:oldN]=v[:oldN]
        for i in range(m):out[oldN+2*i+1]=v[oldN+i]
        return out
    V=[embed(v) for v in V]
    H=[[-F(i<oldN and bool((i+1)&(1<<j))) for i in range(N-1)] for j in range(l+1)]
    G0=[F(i<oldN) for i in range(N-1)];f=unit(N-1,oldN-1)
    gp=scale(F(1,2),vecadd(G0,scale(-1,f)));h0=scale(F(-1,2),vecadd(G0,f))
    As=[vecadd(a,scale(-1,h0)) for a in H]
    h=scale(F(1,3),vecadd(*V[:3]));T=[vecadd(a,scale(-1,h)) for a in V[:3]]
    TA=vecadd(T[0],scale(-1,T[1]));TS=vecadd(T[0],T[1],scale(-2,T[2]))
    Z=[vecadd(V[3+j],scale(F(-1,3),H[j+1])) for j in range(l)]
    private=[oldN+2*i for i in range(m)]
    Ws=[vecadd(unit(N-1,private[i]),scale(-1,embed(P[i]))) for i in range(m)]
    mean=scale(F(1,3),vecadd(*Ws[:3]));WA=vecadd(Ws[0],scale(-1,Ws[1]));WF=vecadd(Ws[2],scale(-1,mean))
    features={'anti':[TA,WA],
              'fixed':[gp,h0,As[0],vecadd(*As[1:]),TS,vecadd(*Z),WF,mean],
              'standard':[vecadd(v[0],scale(-1,v[1])) for v in (As[1:],Z,Ws[3:])]}
    positions=0
    for label,vs in features.items():
        G,S=forms(C,vs)
        require((G,S)==small[label],'ALL original/reduced Gram/complete-frame entries '+label)
        require(psd_rank(G)==len(G),'positive actual physical sector Gram')
        require(psd_rank([[(N-1)*G[i][j]-S[i][j] for j in range(len(G))] for i in range(len(G))])==len(G),'strict actual cap sector')
        positions+=len(vs)**2
    changed=[gp,h0]+As+[TA,TS]+Z+[WA,WF,mean]+Ws[3:-1]
    dim=3*l+7;require(len(changed)==dim,'exhaustive independent changed count')
    G,S=forms(C,changed);require(psd_rank(G)==dim,'entire actual changed Gram')
    require(psd_rank([[(N-1)*G[i][j]-S[i][j] for j in range(dim)] for i in range(dim)])==dim,'entire actual changed cap')
    seed=lift(C,p['s']);seed_report=check(family,seed,p['s'])
    require(seed_report['lower_rank']==N-2,'balanced seed rankN-2')
    Q=[[(N-p['s'])*seed[i][j]+p['s']*int(i==j)-1 for j in range(N)] for i in range(N)]
    gap=[[(N-1)*(int(i==j)-F(1,N))-Q[i][j] for j in range(N)] for i in range(N)]
    require(psd_rank(gap)==N-1,'entire original seed gap1')
    require(sum(map(sum,C))==F(p['ell']*q-4,p['ell']**2),'actual empty norm')
    pairs=[(a,(2*q-1)^a) for a in range(1,2*q-1) if a<((2*q-1)^a)]
    high=[]
    for a,b in pairs[1:]:
        v=[F(0)]*N
        for z in (a,b):v[z]+=1
        for z in pairs[0]:v[z]-=1
        high.append(v)
    kernel=nullspace([[F(bool(a&(1<<j)))-F(bool(b&(1<<j))) for a,b in pairs] for j in range(l+1)],len(pairs))
    low=[]
    for z in kernel:
        v=[F(0)]*N
        for value,(a,b) in zip(z,pairs):v[a]+=value;v[b]-=value
        low.append(v)
    require(len(high)==q-2 and len(low)==q-l-2,'all actual untouched dimensions')
    for vs,eigenvalue in ((high,2*q),(low,6)):
        for v in vs:require(matvec(Q,v)==scale(eigenvalue,v),'complete actual eigenaction including empty')
    require(psd_rank(W)==m-1,'exact balanced private residual rank')
    deleted=[row[:-1] for row in W[:-1]];u=[F(i<3) for i in range(m-1)]
    require(psd_rank(deleted)==m-1,'deleted residual positive definite')
    kappa=dot(u,solve(deleted,u))
    predicted=9*F(l-1,l)/p['nuL']+3/(l*p['cross'])
    require(kappa==predicted and kappa>0,'independent deleted inverse quadratic')
    delta=1/(12*N*(1+kappa));RW=[row[:] for row in W];repaired=[row[:] for row in C];v=private[-1]
    for i in range(3):
        j=private[i];require(family[j+1]&family[v+1]==0,'actual repair entries disjoint')
        repaired[j][v]+=delta;repaired[v][j]+=delta;RW[i][-1]+=delta;RW[-1][i]+=delta
    require(psd_rank(RW)==m and 6*delta-kappa*delta**2>0,'repaired residual and scalar Schur strict')
    M=lift(repaired,p['s']);repair_report=check(family,M,p['s'])
    require(repair_report['lower_rank']==N-1 and repair_report['upper_rank']==N-1,'complete repaired ranks')
    RQ=[[(N-p['s'])*M[i][j]+p['s']*int(i==j)-1 for j in range(N)] for i in range(N)]
    RG=[[F(4*N-3,4)*(int(i==j)-F(1,N))-RQ[i][j] for j in range(N)] for i in range(N)]
    require(psd_rank(RG)==N-1,'complete repaired gap3/4 with new empty row')
    lower=[[RQ[i][j]+1 for j in range(N)] for i in range(N)]
    star=[F(bool(a&1))-F(p['s'],N) for a in family]
    require(matvec(lower,star)==[0]*N and any(star),'actual centered maximum-star kernel')
    return {'n':n,'l':l,'q':q,'N':N,'parameters':{k:str(v) for k,v in p.items()},
            'reduced_Gram_positions':positions,'reduced_frame_positions':positions,
            'changed_dimension':dim,'changed_Gram_positions':dim**2,'changed_frame_positions':dim**2,
            'untouched_high':len(high),'untouched_low':len(low),'full_original_positions':N*N,
            'seed':seed_report,'repair':repair_report,'kappa':str(kappa),'delta':str(delta),
            'seed_gap_sha256':fingerprint(gap),'repaired_gap_sha256':fingerprint(RG)}

def original_low_rank(q,l):
    sectors,p=reduced(q,l);G,S=sectors['fixed'];N=p['N'];s=p['s'];ell=p['ell'];m=p['m']
    h=scale(F(1,3),vecadd(unit(8,1),unit(8,2)))
    v=vecadd(scale(F(1,3),vecadd(unit(8,1),scale(F(1,l),unit(8,3)))),scale(F(1,l),unit(8,5)))
    K=vecadd(unit(8,0),scale(F(l,3),unit(8,1)),unit(8,2),scale(F(1,3),unit(8,3)),unit(8,5))
    E=vecadd(h,scale(-p['rho'],v))
    Z=vecadd(scale(-l*p['Fp']/3,E),scale(p['c']/9,unit(8,4)),unit(8,7))
    D=vecadd(scale(p['A']-p['d'],E),scale(p['c']/6,unit(8,4)),scale(F(-3,2),unit(8,6)))
    base=zero(8);base[0][0]=q*q-1;base[0][1]=base[1][0]=3*(q-1);base[1][1]=F(9)
    for i in (2,3):
        for j in (2,3):base[i][j]=6*G[i][j]
    for weight,vect in ((F(1,6),unit(8,4)),(F(3),h),(F(l),v),(F(1,ell),K),(F(3*m,l),Z),(F(2,3),D)):
        image=matvec(G,vect)
        for i in range(8):
            for j in range(8):base[i][j]+=weight*image[i]*image[j]
    require(base==S,'ALL64 original fixed-frame positions equal grouped rank decomposition, including actual empty')
    B=[[(N-1)*G[i][j]-S[i][j] for j in range(8)] for i in range(8)]
    require(psd_rank(B)==8,'original fixed8 cap')
    S3,S2,_,info=fixed(q,l)
    require(psd_rank(S3)==3 and psd_rank(S2)==2,'two smaller exact Schur forms positive')
    # Independent full5x5 Gaussian inverse verifies the Woodbury scalar.
    base5=[0,1,2,3,5];Gamma=[[G[i][j] for j in base5] for i in base5]
    baseframe=[[S[i][j] for j in base5] for i in base5]
    for weight,z in ((F(3*m,l),Z),(F(2,3),D)):
        image=matvec(G,z)
        for i,a in enumerate(base5):
            for j,b in enumerate(base5):baseframe[i][j]-=weight*image[a]*image[b]
    A5=[[(N-1)*Gamma[i][j]-baseframe[i][j] for j in range(5)] for i in range(5)]
    require(psd_rank(A5)==5,'old+light5 base positive')
    e=[E[i] for i in base5];b=matvec(Gamma,e);tau=dot(b,solve(A5,b))
    require(tau==info['tau'],'entire rational Woodbury inverse quadratic matches independent Gaussian5')
    return {'q':q,'l':l,'N':int(N),'fixed_positions':64,'tau':str(tau),
            'base3':[[str(z) for z in row] for row in S3],
            'final2':[[str(z) for z in row] for row in S2]}
