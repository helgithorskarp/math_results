"""Original finite domains and exact positive congruence certificates.

One phase per process, q<=11 and N<=137. Enumeration is over actual
bitmask sets, with a separate exhaustive-membership scan and direct table.
The unbounded tails are credited proofs, not an extrapolation of these tests.
"""
import sys,json
from fractions import Fraction as F
import bootstrap
from weights import formula
from exact import schur_psd,lift,digest
from literal import require,core_data,domain,typ,table,action
from boundary_parameters import parameters,NORMS,ETA,RECTANGLE_ETA
from entries import certificate


def audit(q,k,X,L,kap,t):
    N=(q*q+13*q+16)//2-k; s=3*q+4
    require(X==domain(q,k,scan=True),'whole actual original domain including empty')
    require(len(L)==N and all(len(row)==N for row in L),'whole matrix dimensions')
    require(all(isinstance(x,(F,int)) for row in L for x in row),'whole exact entry types')
    require(all(L[i][j]==L[j][i] for i in range(N) for j in range(N)),'whole symmetry')
    require(all(sum(row)==N for row in L),'whole row sums')
    require(all(L[i][j]==s*int(i==j) for i in range(N) for j in range(N) if X[i]&X[j]),'whole support and nonempty diagonal')
    Sa=[int(bool(A&1)) for A in X]
    require(action(L,Sa)==[F(s)]*N,'whole centered maximum star action')
    p,entry=certificate(q,k,kappa=kap,t=t)
    M=[[(L[i][j]-s*int(i==j))/(N-s) for j in range(N)] for i in range(N)]
    require(M==[[entry(A,B) for B in X] for A in X],'every direct whole entry, including empty')
    require(M[0][0]<=1,'actual empty-loop cap')
    return p,M


def build(q,k,kap,t,whole=False):
    X,N,s,C0,delta,R,U0=core_data(q,k)
    require(X==domain(q,k,scan=True),'combination enumeration differs from full bitmask scan')
    pool=set(X)
    require(all((A^(1<<i)) in pool for A in X for i in range(q+3) if A&(1<<i)), 'downward closure')
    stars=[sum(bool(A&(1<<i)) for A in X) for i in range(q+3)]
    require(stars==[s,s-k,s-k]+[q+5]*k+[q+6]*(q-k),'all original star sizes')
    require(stars.count(max(stars))==1 and max(stars)==s,'unique maximum star')
    w=formula(F(q),kap)
    require(w=={key:a+kap*b for key,(a,b) in table(q).items()},'expanded table differs from credited evaluator')
    n=N-1
    C=[[C0[i][j]+kap*delta[i][j] for j in range(n)] for i in range(n)]
    require(C==[[F(s-1) if A==B else F(-1) if A&B else w[tuple(sorted((typ(A),typ(B))))]-1
                 for B in X[1:]] for A in X[1:]], 'all retained core entries')
    fs=[[F(bool(A&(1<<i))) for A in X[1:]] for i in range(3)]
    f=[F(A.bit_count()==3 or A.bit_count()==2 and A&7==A) for A in X[1:]]
    kernels=[fs[0],[a-b for a,b in zip(fs[1],f)],[a-b for a,b in zip(fs[2],f)]]
    require(all(not any(action(C,v)) for v in kernels),'restricted three kernel actions')
    z=[1-fs[1][i]-fs[2][i]+f[i] for i in range(n)]
    require(not any(action(C0,z)) and not any(action(R,z)),'zero endpoint additional kernel')
    require(not any(action(R,fs[0])) and sum(map(sum,R))==0, 'repair star/total actions')
    Ct=[[C[i][j]+t*R[i][j] for j in range(n)] for i in range(n)]
    record={'q':q,'k':k,'N':N,'s':s,'kappa':str(kap),'t':str(t),
            'domain_sha256':digest(X),'core_sha256':digest([[str(x) for x in row] for row in Ct])}
    if whole:
        L=lift(Ct)
        p,M=audit(q,k,X,L,kap,t)
        record.update(whole_sha256=digest([[str(x) for x in row] for row in L]),
                      actual_empty_M_loop=str(M[0][0]),gap=str(p['gap']))
        return record,C0,delta,R,U0,Ct,L,fs[0],z
    return record,C0,delta,R,U0,Ct,None,fs[0],z


def phase(q,k,which,kap=None,t=None):
    if which=='continuity':
        require((q,k) in NORMS,'six finite continuity cases only')
        p=parameters(q,k);rec,C0,delta,R,U0,Ct,_,_,_=build(q,k,p['kappa'],F(0))
        d=max(sum(abs(x) for x in row) for row in delta)
        require(d==NORMS[q,k]==p['delta_norm'],'exact symmetric derivative row norm')
        n=len(U0);rank=schur_psd([[U0[i][j]-ETA*int(i==j) for j in range(n)] for i in range(n)])
        require(rank==n,'strict zero seed cap floor')
        rec.update(phase=which,rank=rank,eta=str(ETA),delta_norm=str(d),
                   tau=str(p['tau']),seed_gamma=str(p['seed_gamma']),gap=str(p['gap']))
    elif which in ('corner-lower','corner-upper'):
        require((q,k)==(8,3) and kap in (F(0),F(1,4096)) and t in (F(3,8),F(1,2)), 'four literal rectangle corners only')
        rec,C0,delta,R,U0,Ct,_,Sa,z=build(q,k,kap,t);n=len(Ct)
        if which=='corner-lower':
            rank=schur_psd(Ct);require(rank==rec['N']-2 if kap else rank==rec['N']-3,'corner lower rank')
            require(not any(action(Ct,Sa)), 'corner star kernel')
            if not kap:require(not any(action(Ct,z)) and z!=Sa,'zero corner second kernel')
        else:
            rank=schur_psd([[U0[i][j]-kap*delta[i][j]-t*R[i][j]-RECTANGLE_ETA*int(i==j)
                             for j in range(n)] for i in range(n)])
            require(rank==n,'corner strict cap floor')
        rec.update(phase=which,rank=rank,eta=str(RECTANGLE_ETA))
    elif which in ('whole-lower','whole-gap'):
        require((q,k) in NORMS or (q,k)==(8,3),'seven original positive finite cases only')
        p=parameters(q,k);rec,_,_,_,_,Ct,L,_,_=build(q,k,p['kappa'],p['tau'],whole=True)
        N=rec['N']
        if which=='whole-lower':rank=schur_psd(L)
        else:rank=schur_psd([[F(N*int(i==j))-L[i][j]-p['gap']*(F(i==j)-F(1,N))
                             for j in range(N)] for i in range(N)])
        require(rank==N-1,'greatest whole rank / strict projected cap')
        rec.update(phase=which,rank=rank,normalized_gap=str(p['gap']/(N-p['s'])))
    else:raise ValueError('unknown finite phase')
    return rec


if __name__=='__main__':
    require(len(sys.argv) in (4,6),'usage: q k phase [kappa t]')
    print(json.dumps(phase(int(sys.argv[1]),int(sys.argv[2]),sys.argv[3],
                          *(F(x) for x in sys.argv[4:])),sort_keys=True,indent=2))
