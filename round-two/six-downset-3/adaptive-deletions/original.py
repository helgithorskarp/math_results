"""Bounded original-domain validation of adaptive-kappa deletions.

No sector decoder builds these matrices. Each exact congruence is a
separate resumable phase. Original q<=12 full domains have at most158 vertices; retained N<=155.
"""
from pathlib import Path
import sys, json, hashlib
from fractions import Fraction as F
from itertools import combinations

import bootstrap
from weights import formula
from exact import require, schur_psd, lift, digest
from parameters import parameters

def allocate(q, k):
    p = parameters(q, k)
    require(4 <= q <= 12 and p['N'] <= 155,
            'original-domain guard: q<=12 and retained N<=155')
    return p


def typ(A):
    return (A & 7).bit_count(), (A >> 3).bit_count()


def audit_whole(q,k,X,L):
    p=allocate(q,k);N=p['N'];s=p['s']
    expected=[0]+sorted(sum(1<<i for i in points)
        for size in (1,2,3) for points in combinations(range(q+3),size)
        if (size<3 or sum(i<3 for i in points)>=2)
        and not(size==3 and set(points[:2])=={1,2} and 3<=points[2]<3+k))
    require(all(type(A) is int for A in X) and X==expected,'whole original domain including empty differs')
    require(len(L)==N and all(len(row)==N for row in L),'whole dimensions')
    require(all(isinstance(x,(int,F)) for row in L for x in row),'whole exact entries')
    require(all(L[i][j]==L[j][i] for i in range(N) for j in range(N)),'whole symmetry')
    require(all(sum(row)==N for row in L),'whole row sums')
    require(all(L[i][j]==s*int(i==j) for i in range(N) for j in range(N) if X[i]&X[j]),'whole support')
    star=[int(bool(A&1)) for A in X]
    require(all(sum(row[i]*star[i] for i in range(N))==s for row in L),'whole forced centered star kernel')
    return p


def original(q, k):
    p = allocate(q, k)
    base = [0] + sorted(sum(1 << i for i in points)
        for size in (1, 2, 3)
        for points in combinations(range(q + 3), size)
        if size < 3 or sum(i < 3 for i in points) >= 2)
    deleted = {6 | (1 << i) for i in range(3, 3 + k)}
    X = [A for A in base if A not in deleted]
    require(len(base) == (q*q+13*q+16)//2 and len(X) == p['N'], 'original sizes')
    require(X[0] == 0 and len(set(X)) == len(X), 'original actual empty vertex')
    pool = set(X)
    require(all((A ^ (1 << i)) in pool for A in X for i in range(q+3) if A & (1 << i)),
            'original downward closure')
    stars = [sum(bool(A & (1 << i)) for A in X) for i in range(q+3)]
    require(stars[:3] == [p['s'], p['s']-k, p['s']-k], 'core star sizes')
    require(stars[3:] == [q+5]*k + [q+6]*(q-k), 'outside star sizes')
    require(stars.count(max(stars)) == 1 and max(stars) == p['s'], 'largest star')
    w = formula(F(q), p['kappa'])
    def entry(A, B):
        return F(p['s']-1) if A == B else F(-1) if A & B else w[tuple(sorted((typ(A),typ(B))))]-1
    full = [[entry(A,B) for B in base[1:]] for A in base[1:]]
    families = [[F(bool(A & (1 << i))) for A in base[1:]] for i in range(3)]
    families.append([F(A.bit_count()==3 or A.bit_count()==2 and A & 7 == A) for A in base[1:]])
    require(all(sum(row[j]*v[j] for j in range(len(full))) == 0
                for row in full for v in families), 'four original base kernel actions')
    h = F(1, 3*q+5)
    residual = [F(1) if typ(A)[0] == 0 else h if typ(A)[0] < 3 else -3*(q+1)*h for A in base[1:]]
    require(all(sum(row) == p['kappa']*r for row,r in zip(full,residual)), 'original constant action')
    keep = [i for i,A in enumerate(base[1:]) if A not in deleted]
    core = [[full[i][j] for j in keep] for i in keep]
    f = [[v[i] for i in keep] for v in families]
    kernels = [f[0], [x-y for x,y in zip(f[1],f[3])], [x-y for x,y in zip(f[2],f[3])]]
    require(all(sum(row[j]*v[j] for j in range(len(core))) == 0
                for row in core for v in kernels), 'three restricted kernel actions')
    index = {A:i for i,A in enumerate(X[1:])}
    e = lambda A: [F(B==A) for B in X[1:]]
    a,b,c,ab,ac = map(e,(1,2,4,3,5))
    ell = [[x-y+z for x,y,z in zip(b,a,ac)], [x-y+z for x,y,z in zip(c,a,ab)]]
    pos = [[x+y-z for x,y,z in zip(b,a,ac)], [x+y-z for x,y,z in zip(c,a,ab)]]
    n = len(core)
    R = [[F(0)]*n for _ in range(n)]
    for A,B,v in ((1,2,1),(1,4,1),(2,5,-1),(4,3,-1)):
        require(A in index and B in index and not A & B, 'balanced trade support')
        i,j = index[A],index[B]
        R[i][j] = R[j][i] = F(v)
    require(all(R[i][j] == sum((v[i]*v[j]-w[i]*w[j])/2 for v,w in zip(pos,ell))
                for i in range(n) for j in range(n)), 'balanced trade PSD split')
    require(all(sum(v[i]*kernels[0][i] for i in range(n)) == 0 for v in ell+pos), 'trade star action')
    require([[sum(v[i]*z[i] for i in range(n)) for z in kernels[1:]] for v in pos] == [[2,0],[0,2]],
            'positive part removes both extra kernels')
    require(all(sum(v[i]*z[i] for i in range(n)) == 0 for v in ell for z in kernels), 'negative part kernel action')
    repaired = [[core[i][j]+p['tau']*R[i][j] for j in range(n)] for i in range(n)]
    require(all(sum(row[i]*kernels[0][i] for i in range(n)) == 0 for row in repaired), 'repaired star action')
    L = lift(repaired)
    N,s = p['N'],p['s']
    audit_whole(q,k,X,L)
    # Direct deleted-column and empty-entry formulas are separately compared.
    marked = sum(1 << i for i in range(3,3+k))
    def closed_row(A):
        r = F(1) if typ(A)[0]==0 else h if typ(A)[0]<3 else -3*(q+1)*h
        hits = k if A & 6 else (A & marked).bit_count()
        removed_sum = F(-k) if hits==k else -hits+(k-hits)*(w[tuple(sorted((typ(A),(2,1))))]-1)
        trade_row = 2 if A==1 else -1 if A in (3,5) else 0
        return p['kappa']*r-removed_sum+p['tau']*trade_row
    rows = [closed_row(A) for A in X[1:]]
    alpha = F(q*(q+1),2)+3*(q+1)*h
    total = p['kappa']*alpha-2*k*p['kappa']*h+k*(s-k)
    require(rows==[sum(row) for row in repaired] and sum(rows)==total, 'closed row and total formulas')
    require(L[0][0]==1+total and L[0][1:]==[1-r for r in rows], 'actual empty lift entries')
    return p,X,core,repaired,L


def phase(q,k,which):
    p,X,C,Ct,L = original(q,k)
    N=p['N'];n=N-1;gamma=p['gamma']
    if which=='seed':
        rank=schur_psd(C);require(rank==N-4,'restricted seed rank')
    elif which=='core-gap':
        rank=schur_psd([[F(N*int(i==j)-1)-C[i][j]-gamma*int(i==j) for j in range(n)] for i in range(n)])
        require(rank==n,'quantitative original core cap')
    elif which=='lower':
        rank=schur_psd(L);require(rank==N-1,'whole greatest lower rank')
    elif which=='upper':
        rank=schur_psd([[F(N*int(i==j))-L[i][j] for j in range(N)] for i in range(N)])
        require(rank==N-1,'whole greatest upper rank')
    elif which=='whole-gap':
        rank=schur_psd([[F(N*int(i==j))-L[i][j]-(gamma/2)*(F(i==j)-F(1,N)) for j in range(N)] for i in range(N)])
        require(rank==N-1,'whole projected gap')
    else:
        raise ValueError('unknown exact phase')
    return {'agent':'six-downset-3','role':'researcher','q':q,'k':k,'N':N,'s':p['s'],
            'phase':which,'rank':rank,'kappa':str(p['kappa']),'chi':str(p['chi']),
            'gamma':str(gamma),'tau':str(p['tau']),
            'core_sha256':digest([[str(x) for x in row] for row in C]),
            'whole_sha256':digest([[str(x) for x in row] for row in L]),
            'actual_empty_M_loop':str((L[0][0]-p['s'])/(N-p['s'])),
            'scaled_whole_gap':str(gamma/2),'normalized_unit_gap':str(gamma/(2*(N-p['s']))),
            'domain_checks':'downward closure, all stars, base and restricted kernels, split repair, rows/support and closed empty formulas'}


if __name__=='__main__':
    require(len(sys.argv)==4,'usage: original.py q k phase')
    print(json.dumps(phase(int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]),sort_keys=True,indent=2))
