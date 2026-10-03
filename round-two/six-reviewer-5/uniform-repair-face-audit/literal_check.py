"""Separate stdlib Fraction original-member binding of every sector Gram entry."""
import json, math
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

def require(ok,message):
    if not ok: raise ValueError(message)

def table(q):
    q=F(q);s=3*q+4;h=1/(3*q+5)
    o,p,a,b,c,d,e=(0,1),(0,2),(1,0),(1,1),(2,0),(2,1),(3,0)
    T={}
    def put(x,y,v,w=F(0)):T[tuple(sorted((x,y)))]=(F(v),F(w))
    put(o,o,(6/q-q-4)/(q-1),1/(q-1))
    put(o,p,q*(q-3)/((q-1)*(q-2)))
    den=(q-2)*(q-3)/2
    put(p,p,(6/q+2*q/(q-1)-s+q*(q-1)/2)/den,(1-6*h*(q+1)/(q*(q-1)))/den)
    for leaf,vals in ((o,((1-1/q,0),(1+1/q,0),(1+6/q,0))),
                      (p,((1,2*h/(q*(q-1))),(1+2*(q-1)/(q*(q-2)),2*h/((q-1)*(q-2))),
                          (1+6/q,-6*h*(q+1)/(q*(q-1)))))):
        for core,i in ((a,0),(c,0),(b,1),(d,1),(e,2)):put(leaf,core,*vals[i])
    r=3+2/q;w=(s-r)/(q-1)
    for x,y,v in ((a,a,0),(a,b,0),(b,b,0),(a,c,2),(a,d,r),(b,c,r),(b,d,w)):put(x,y,v)
    return T

def members(q,k):
    return [sum(1<<i for i in pts) for n in (1,2,3) for pts in combinations(range(q+3),n)
            if (n<=2 or sum(i<3 for i in pts)>=2) and not(n==3 and pts[:2]==(1,2) and 3<=pts[2]<3+k)]

def typ(A):return ((A&7).bit_count(),(A>>3).bit_count())

def entry(A,B,q,T):
    if A==B:return F(3*q+3),F(0)
    if A&B:return F(-1),F(0)
    a,b=T[tuple(sorted((typ(A),typ(B))))];return a-1,b

def pair(A,V):
    m=len(V[0]);Y=[[sum(A[i][j]*V[j][a] for j in range(len(A)) if V[j][a]) for a in range(m)] for i in range(len(A))]
    return [[sum(V[i][a]*Y[i][b] for i in range(len(A)) if V[i][a]) for b in range(m)] for a in range(m)]

def solve(A,B):
    n=len(A);r=len(B[0]);W=[list(A[i])+list(B[i]) for i in range(n)]
    for p in range(n):
        t=next((i for i in range(p,n) if W[i][p]),None);require(t is not None,'actual rational solve nonsingular')
        W[p],W[t]=W[t],W[p];d=W[p][p];W[p]=[v/d for v in W[p]]
        for i in range(p+1,n):
            v=W[i][p]
            if v: W[i]=[W[i][j]-v*W[p][j] for j in range(n+r)]
    X=[[F(0)]*r for _ in range(n)]
    for i in range(n-1,-1,-1):
        for a in range(r):X[i][a]=W[i][n+a]-sum(W[i][j]*X[j][a] for j in range(i+1,n))
    require(all(sum(A[i][j]*X[j][a] for j in range(n))==B[i][a] for i in range(n) for a in range(r)), 'all literal stationary equations')
    return X

def short(A,ix,excluded=()):
    others=[i for i in range(len(A)) if i not in ix and i not in excluded]
    W=solve([[A[i][j] for j in others] for i in others],[[-A[i][j] for j in ix] for i in others])
    V=[[F(i==j) for j in ix] for i in range(len(A))]
    for i,j in enumerate(others):V[j]=W[i]
    return pair(A,V),V

def original(q,k):
    X=members(q,k);T=table(q);N=(q*q+13*q+16)//2-k
    require(len(X)==N-1,'literal original carrier incl actual empty')
    keys=sorted(set((A&7,((A>>3)&((1<<k)-1)).bit_count(),(A>>(3+k)).bit_count()) for A in X))
    ix={v:i for i,v in enumerate(keys)}
    orbit=[ix[(A&7,((A>>3)&((1<<k)-1)).bit_count(),(A>>(3+k)).bit_count())] for A in X]
    mass=[orbit.count(i) for i in range(len(keys))]
    C=[[F(0)]*len(keys) for _ in keys];D=[[F(0)]*len(keys) for _ in keys];U=[[F(0)]*len(keys) for _ in keys]
    star=[int(A&1!=0) for A in X]
    zeta=[1 if A&7==0 else -1 if A&7==7 else 0 for A in X]
    zs=[];ss=[];ze=F(0)
    for ai,A in enumerate(X):
        i=orbit[ai];cz=F(0);cs=F(0)
        for bj,B in enumerate(X):
            j=orbit[bj];a,b=entry(A,B,q,T)
            C[i][j]+=a;D[i][j]+=b;U[i][j]+=N*int(ai==bj)-1-a
            cz+=a*zeta[bj];cs+=a*star[bj];ze+=zeta[ai]*b*zeta[bj]
        zs.append(cz);ss.append(cs)
    require(all(v==0 for v in zs+ss),'every actual original zero-kernel equation')
    require(ze==F(q*(q+1),2)+F(3*(q+1),3*q+5),'entire literal physical zeta Delta energy')
    # Independently compare ordered distinct-set counts, every C/Delta/U position.
    def ch(n,r):return math.comb(n,r) if 0<=r<=n else 0
    for i,(c,z,w) in enumerate(keys):
        require(mass[i]==ch(k,z)*ch(q-k,w),'whole actual orbit mass')
        for j,(d,zz,ww) in enumerate(keys):
            n=0 if c&d else ch(k-z,zz)*ch(q-k-w,ww)
            a,b=T[tuple(sorted(((c.bit_count(),z+w),(d.bit_count(),zz+ww))))] if n else (F(0),F(0))
            expected=(3*q+4)*mass[i]*int(i==j)-mass[i]*mass[j]+mass[i]*n*a
            require(C[i][j]==expected and D[i][j]==mass[i]*n*b and U[i][j]==N*mass[i]*int(i==j)-mass[i]*mass[j]-expected,'all original coefficient orbit entries')
    return dict(q=q,k=k,N=N,positions=(N-1)**2,coefficient_positions=3*len(keys)**2,keys=keys,mass=mass,C=C,D=D,U=U)

def main():
    rec=original(21,7)
    # Actual full-space values give a 23x23 Gram; b/c invariant anchors retain17 modes.
    keys=rec['keys']
    def flip(c):return(c&1)|((c&2)<<1)|((c&4)>>1)
    reps=sorted(set((min(c,flip(c)),z,w) for c,z,w in keys))
    groups=[[i for i,(c,z,w) in enumerate(keys) if (min(c,flip(c)),z,w)==rep] for rep in reps]
    def even(A):return [[sum(A[i][j] for i in g for j in h) for h in groups] for g in groups]
    C,D,U=(even(rec[n]) for n in ('C','D','U'))
    cap,Vc=short(U,[reps.index(t) for t in ((1,0,0),(3,0,0),(2,0,0))])
    lo,Vl=short(C,[reps.index(t) for t in ((2,0,0),(3,0,0))],[reps.index((1,0,0)),reps.index((0,1,0))])
    require(lo[0][0]==lo[0][1]==lo[1][0]==lo[1][1],'actual lower short normalization')
    z=[F(1) if c==0 else F(-1) if c==7 else F(0) for c,z,w in reps]
    alpha=sum(z[i]*D[i][j]*z[j] for i in range(17) for j in range(17)); ed=pair(D,Vl)[0][0]
    cross=sum(z[i]*D[i][j]*Vl[j][0] for i in range(17) for j in range(17))
    prime=ed-cross*cross/alpha
    out=dict(q=21,k=7,N=rec['N'],original_positions=rec['positions'],all_original_gram_entries=rec['coefficient_positions'],
             a0=lo[0][0],a_prime0=prime,M0=cap,Delta_cap=pair(D,Vc))
    def encode(x):
        if isinstance(x,dict):return {a:encode(b) for a,b in x.items()}
        if isinstance(x,list):return [encode(y) for y in x]
        return str(x) if isinstance(x,F) else x
    P=Path(__file__).resolve().parent/'literal-original.json';P.write_text(json.dumps(encode(out),indent=2)+'\n')
    print(json.dumps({'status':'all original literal entries/zero-kernels/full17-mode shorts checked','q':21,'k':7,
                      'N':rec['N'],'pair_positions':rec['positions'],'gram_entries':rec['coefficient_positions']},indent=2))

if __name__=='__main__':main()
