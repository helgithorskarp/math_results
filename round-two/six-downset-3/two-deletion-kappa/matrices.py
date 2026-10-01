"""Separate bounded original-set matrices; no symbolic sector decoder here."""
import bootstrap
from fractions import Fraction as F
from itertools import combinations
from weights import formula,credited_formula,KAPPA,scalar
from entries import EDGES
from exact import require,schur_psd,lift,digest

def allocation_parameter(q):
    require(type(q) is int and 4<=q<=9,'literal allocation guard: integer4<=q<=9')

def literal_base(q,kappa=KAPPA,weights=None):
    allocation_parameter(q)
    require(isinstance(kappa,F),'exact kappa required')
    X=[0]+sorted(sum(1<<i for i in a) for size in [1,2,3] for a in combinations(range(q+3),size) if size<3 or sum(i<3 for i in a)>=2)
    typ=lambda x:((x&7).bit_count(),(x>>3).bit_count())
    weights=formula(F(q),kappa) if weights is None else weights;s=3*q+4
    C=[[F(s-1) if x==y else F(-1) if x&y else weights[tuple(sorted((typ(x),typ(y))))]-1 for y in X[1:]] for x in X[1:]]
    require(all(isinstance(x,(int,F)) for row in C for x in row),'inexact literal base entry')
    families=[[F(bool(x&(1<<i))) for x in X[1:]] for i in range(3)]
    families.append([F(x.bit_count()==3 or (x.bit_count()==2 and x&7==x)) for x in X[1:]])
    require(len(X)==(q*q+13*q+16)//2,'full base domain size')
    require(all(sum(row[i]*v[i] for i in range(len(C)))==0 for row in C for v in families),'four literal family kernels')
    h=F(1,3*q+5);resid=[F(1) if typ(x)[0]==0 else h if typ(x)[0]<3 else -3*(q+1)*h for x in X[1:]]
    require(all(sum(row)==kappa*v for row,v in zip(C,resid)),'literal variable-kappa constant action')
    return X,C,families

def trade(X):
    size=len(X)-1;index={A:i for i,A in enumerate(X[1:])};R=[[F(0)]*size for _ in range(size)]
    for (A,B),v in EDGES.items():
        require(A in index and B in index and not A&B,'four-edge domain/support')
        i,j=index[A],index[B];R[i][j]=R[j][i]=v
    point=lambda A:[F(x==A) for x in X[1:]]
    a,b,c,ab,ac=map(point,[1,2,4,3,5])
    ell=[[x-y+z for x,y,z in zip(b,a,ac)],[x-y+z for x,y,z in zip(c,a,ab)]]
    positive=[[x+y-z for x,y,z in zip(b,a,ac)],[x+y-z for x,y,z in zip(c,a,ab)]]
    require(all(R[i][j]==sum((v[i]*v[j]-w[i]*w[j])/2 for v,w in zip(positive,ell)) for i in range(size) for j in range(size)),'four-edge exact PSD split')
    return R,ell,positive

def prepare(q):
    info=scalar(q);allocation_parameter(q)
    X,C,families=literal_base(q);deleted={6|(1<<i) for i in [3,4]}
    keep=[i for i,x in enumerate(X[1:]) if x not in deleted]
    Y=[0]+[X[i+1] for i in keep];core=[[C[i][j] for j in keep] for i in keep]
    star=[families[0][i] for i in keep];N=len(Y)
    require(N==info['N'] and sum(star)==info['s'],'two-deletion domain/star size')
    require(sum(bool(x&2) for x in Y)==sum(bool(x&4) for x in Y)==info['s']-2,'the smaller marked stars')
    R,ell,positive=trade(Y);t=info['tau']
    repaired=[[core[i][j]+t*R[i][j] for j in range(N-1)] for i in range(N-1)]
    L=lift(repaired)
    return info,Y,core,star,L

def check_whole(q,X,L):
    info=scalar(q);allocation_parameter(q);N=info['N'];s=info['s']
    require(len(X)==N and X[0]==0 and len(set(X))==N,'whole domain and empty vertex')
    require(all(type(A) is int for A in X),'integer literal domain')
    canonical=[0]+[A for A in literal_base(q)[0][1:] if A not in (14,22)]
    require(X==canonical,'whole canonical downset differs')
    require(len(L)==N and all(len(row)==N for row in L),'whole matrix dimensions')
    require(all(isinstance(x,(int,F)) for row in L for x in row),'inexact whole entry')
    require(all(L[i][j]==L[j][i] for i in range(N) for j in range(N)),'whole symmetry')
    require(all(sum(row)==N for row in L),'whole original row sums')
    require(all(L[i][j]==s*int(i==j) for i in range(N) for j in range(N) if X[i]&X[j]),'whole original support')
    return info

def fixture(q):
    oldX,oldC,_=literal_base(4,F(1,2));XX,CC,_=literal_base(4,F(1,2),credited_formula(F(4)))
    require(oldX==XX and oldC==CC,'literal published fixed-kappa baseline differs')
    info,X,core,star,L=prepare(q);N=info['N'];s=info['s'];size=N-1;gamma=info['gamma']
    seed_rank=schur_psd(core);require(seed_rank==N-4,'three-dimensional inherited kernel rank')
    U=[[F(N*int(a==b)-1)-core[a][b] for b in range(size)] for a in range(size)]
    floor_rank=schur_psd([[U[a][b]-gamma*F(a==b) for b in range(size)] for a in range(size)])
    repaired=[[L[a+1][b+1]-1 for b in range(size)] for a in range(size)]
    require(all(sum(row[h]*star[h] for h in range(size))==0 for row in repaired),'repaired star kernel')
    check_whole(q,X,L);V=[[F(N*int(a==b))-L[a][b] for b in range(N)] for a in range(N)]
    ranks=[schur_psd(L),schur_psd(V)];require(ranks==[N-1,N-1],'whole greatest lower/upper ranks')
    gap_rank=schur_psd([[V[a][b]-(gamma/2)*(F(a==b)-F(1,N)) for b in range(N)] for a in range(N)])
    return {'q':q,'deletions':2,'N':N,'s':s,'kappa':str(KAPPA),'baseline_q4_fixed_kappa_exact':True,'core_sha256':digest([[str(x) for x in row] for row in core]),'seed_rank':seed_rank,'gamma':str(gamma),'gamma_source':'unbounded chi bound','cap_floor_rank':floor_rank,'closed_interval':'0<t<='+str(info['tau']),'checked_endpoint':str(info['tau']),'scaled_whole_gap':str(gamma/2),'normalized_unit_gap':str(gamma/(2*(N-s))),'whole_ranks':ranks,'whole_gap_slack_rank':gap_rank,'actual_empty_M_loop':str((L[0][0]-s)/(N-s))}
