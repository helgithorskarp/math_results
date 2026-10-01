#!/usr/bin/env python3
"""Finite exact validation of the written, quantified general-r argument.

No sample set proves the infinite theorem. That theorem uses the explicit
binomial-tail estimates and quotient argument in PROOF.md. Python3.11+,
standard library only, no assertions or floating point in proof checks.
"""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from math import comb
from pathlib import Path
import argparse
import json

from matrices import parameters, sectors, quotients, residuals, literal_matrix, slack_entry, require
from exact import psd_rank, fails_psd, matrix_product, transpose


def radius(A, s):
    return max((sum(abs(v-Q(s*int(i == k))) for k,v in enumerate(row))/s
                for i,row in enumerate(A)), default=Q(0))


def finite_checks(P, quantitative):
    n,r,N,s,p = P.n,P.r,P.N,P.s,P.r-1
    b,T = P.beta,N-1-s
    for a in range(1,r+1):
        require(sum(b[a][k]*comb(n-a-1,k-1) for k in range(1,r+1)) == s, "Star count")
        require(sum(b[a][k]*comb(n-a,k) for k in range(1,r+1)) == T, "Center count")
    require(sum(a*comb(n,a) for a in range(1,r+1)) == n*s, "Cardinality identity")
    require(N-2*s == comb(n-1,r) > 0, "Strict density")
    centered, repaired = sectors(P), sectors(P,repaired=True)
    scalar, records = residuals(P)
    ranks = []; repaired_ranks = []; upper_ranks = []
    total_center = total_repaired = total_upper = 0
    h = r-2
    Q0 = [[Q(int(a == k)+(a-r)*int(k == p)+(p-a)*int(k == r))
           for k in range(1,r+1)] for a in range(1,p)]
    Q1 = [[Q(int(a == k)-int(k == r)) for k in range(1,r+1)] for a in range(1,r)]
    quotient = quotients(P)
    radii = [radius(A,s) for A in quotient]
    residual_count = 0
    for j,aa,g,K,U in centered:
        d=len(aa)
        HC=[[g[i]*v for v in row] for i,row in enumerate(K)]
        HU=[[g[i]*v for v in row] for i,row in enumerate(U)]
        if j <= 1:
            require(all(sum(row) == 0 for row in K), "Forced constant-sector kernel")
            if j == 0:
                require(all(sum(a*v for a,v in zip(aa,row)) == 0 for row in K), "Cardinality kernel")
                if h:
                    A=[[s*comb(n,a)*int(a == k)-comb(n,a)*comb(n,k)
                        for k in range(1,p)] for a in range(1,p)]
                    require(matrix_product(matrix_product(transpose(Q0),A),Q0) == HC,
                            "Zero-sector congruence")
                    require(matrix_product(Q0,K) == matrix_product(quotient[0],Q0), "Zero quotient intertwining")
                else:
                    require(all(v == 0 for row in HC for v in row), "Empty zero-sector quotient")
            else:
                require(matrix_product(Q1,K) == matrix_product(quotient[1],Q1), "One quotient intertwining")
        rank=psd_rank(HC); urank=psd_rank(HU)
        require(rank == d-(2 if j == 0 else 1 if j == 1 else 0), "Centered rank")
        require(urank == d, "Centered strict upper rank")
        _,low,Cres,Ures=records[j]
        require(len(Ures) <= 2 and psd_rank(Ures)+low == urank, "Cap residual")
        residual_count += 1
        if j:
            require(len(Cres) <= 2 and psd_rank(Cres)+low == rank, "Core residual")
            residual_count += 1
        else:
            require(scalar > 0 and rank == h, "Degree-zero scalar criterion")
        _,_,_,KR,UR=repaired[j]
        HR=[[g[i]*v for v in row] for i,row in enumerate(KR)]
        HUR=[[g[i]*v for v in row] for i,row in enumerate(UR)]
        rr=psd_rank(HR); ru=psd_rank(HUR)
        require(rr == d-int(j <= 1) and ru == d, "Repaired sector ranks")
        multiplicity=comb(n,j)-(comb(n,j-1) if j else 0)
        total_center += multiplicity*rank
        total_repaired += multiplicity*rr
        total_upper += multiplicity*ru
        ranks.append(rank);repaired_ranks.append(rr);upper_ranks.append(ru)
    require(total_center == N-n-2 and total_repaired == N-n-1 and total_upper == N-1,
            "Full rank accounting")
    require(P.epsilon*P.trade_bound == Q(n,48*(N-1)) <= Q(1,48), "Repair size")
    require(P.epsilon == Q(n,72*(N-1)*(n-1)*(n-2)*(n-3)), "Repair formula")
    if quantitative:
        require(n >= 32*r*r, "Quantitative domain")
        B = comb(n,r-2)
        z = sum(comb(n,k) for k in range(r-1))
        z_weighted = sum((p-a+1)*comb(n,a) for a in range(1,p))
        require(z <= Q(9,8)*B and z_weighted <= Q(9,4)*B, "Weighted binomial tails")
        require(B <= Q(4*r,n)*s, "Low-layer ratio")
        require(s <= Q(8,7)*comb(n,p) and T <= 2*comb(n,r), "Top tails")
        Utail=sum(comb(n-1,k) for k in range(1,r-1))
        D=p*s-(n-r)*Utail-n
        require(abs(D) <= Q(12*r*r,n)*s, "Cancellation bound")
        for a in range(1,r+1):
            for k in [p,r]:
                require(comb(n-a,k) >= Q(6,7)*comb(n,k), "Binomial displacement")
            require(Q(s,comb(n-a,p)) <= Q(4,3), "Core denominator ratio")
        require(Q(s,comb(n,r)) <= Q(4*r,n), "Top size ratio")
        for a in range(1,p):
            require(abs(b[a][p]) <= Q(4,3)*(p-a+1) and abs(b[a][r]) <= 3,
                    "Individual lower-layer weights")
        require(abs(b[p][p]) <= Q(48*r*r,n) and abs(b[p][r]) <= 3 and abs(b[r][r]) <= 3,
                "Top weights")
        require(max(abs(v) for row in b for v in row) <= 2*r, "Uniform weight bound")
        Lp=sum((b[p][a]*comb(n-p,a) for a in range(1,p)),Q(0))
        Hp=sum((a*b[p][a]*comb(n-p,a) for a in range(1,p)),Q(0))
        X=r*(T-Lp)-((n-p)*s-Hp)
        require(abs(Lp) <= Q(12*r,n)*s and abs(X) <= Q(36*r*r,n)*s, "Top cancellation control")
        require(radii[0] <= Q(51*r*r,2*n), "Zero quotient radius")
        require(radii[1] <= Q(63*r*r,4*n), "One quotient radius")
        require(all(x <= Q(9*r*r,n) for x in radii[2:]), "Higher sector radius")
        require(max(radii) <= Q(51,64) < Q(7,8), "Uniform spectral window")
        require(s >= n and Q(s,8) >= 1 and N-Q(15*s,8) >= 1, "Repair and cap gaps")
    return {"n":n,"r":r,"N":N,"s":s,"centered_sector_ranks":ranks,
            "repaired_sector_ranks":repaired_ranks,"upper_sector_ranks":upper_ranks,
            "lower_full_rank":total_repaired+1,"upper_full_rank":total_upper,
            "quotient_row_radii":[str(x) for x in radii],"residual_checks":residual_count,
            "epsilon":str(P.epsilon)}


def literal_checks(n,r):
    P=parameters(n,r,certified=False)
    V,L=literal_matrix(P)
    N,s=P.N,P.s
    require(len(V) == N and V[0] == 0 and len(set(V)) == N, "Literal vertex order")
    require(all(sum(row) == N for row in L), "Literal row sums")
    require(all(L[i][j] == L[j][i] for i in range(N) for j in range(N)), "Literal symmetry")
    require(all(L[i][i] == s for i in range(1,N)), "Literal nonempty diagonal")
    require(all(L[i][j] == 0 for i in range(N) for j in range(N) if i != j and V[i]&V[j]), "Literal support")
    U=[[Q(N*int(i == j))-L[i][j] for j in range(N)] for i in range(N)]
    require(psd_rank(L) == N-n and psd_rank(U) == N-1, "Literal endpoint ranks")
    for k in range(n):
        z=[Q(int(A>>k&1))-Q(s,N) for A in V]
        require(all(sum(x*y for x,y in zip(row,z)) == 0 for row in L), "Literal centered star")
    # Reconstruct the full lift independently from its nonempty core.
    m=N-1
    C=[[L[i+1][j+1]-1 for j in range(m)] for i in range(m)]
    row_sums=list(map(sum,C))
    require(L[0][0] == 1+sum(row_sums), "Literal empty loop lift")
    require(all(L[0][i+1] == 1-row_sums[i] for i in range(m)), "Literal empty row lift")
    digest=sha256(json.dumps([[str(v) for v in row] for row in L],separators=(',',':')).encode()).hexdigest()
    return {"n":n,"r":r,"N":N,"lower_rank":N-n,"upper_rank":N-1,"literal_L_sha256":digest}


def negative_controls():
    count=0
    def reject(fn):
        nonlocal count
        try:
            fn()
        except (ValueError,TypeError):
            count+=1
        else:
            raise ValueError("A negative control passed")
    reject(lambda: parameters(12,6))
    reject(lambda: parameters(3,2,certified=False))
    reject(lambda: parameters(128.0,2))
    reject(lambda: parameters(128,True))
    reject(lambda: psd_rank([[0,1],[1,0]]))
    reject(lambda: psd_rank([[1,0],[0,-1]]))
    reject(lambda: psd_rank([[1.0]]))
    reject(lambda: psd_rank([[1,1],[0,1]]))
    P=parameters(128,2)
    reject(lambda: slack_entry(P,1<<128,0))
    reject(lambda: slack_entry(P,7,0))
    reject(lambda: literal_matrix(P))
    V,L=literal_matrix(parameters(4,2,certified=False))
    L[0][0] += 1
    reject(lambda: require(all(sum(row) == len(V) for row in L),"Damaged empty loop"))
    # Exact failure of this unique centered sparse ansatz at (n,r)=(20,10).
    P=parameters(20,10,certified=False)
    mlow=sum(comb(20,a) for a in range(1,9))
    require(P.s-mlow == -1805, "Sparse boundary witness")
    vector_form=mlow*(P.s-mlow)
    j,aa,g,K,U=sectors(P)[0]
    require(vector_form < 0 and fails_psd([[g[i]*v for v in row] for i,row in enumerate(K)]),
            "Sparse boundary did not reject")
    count+=1
    return {"rejected":count,"sparse_failure":{"n":20,"r":10,"s":P.s,"lower_layer_size":mlow,
                                               "s_minus_lower":-1805,"negative_full_core_form":vector_form}}


def baseline_check():
    path=Path(__file__).with_name('BASELINE.json')
    data=json.loads(path.read_text())
    for rec in data['cases']:
        P=parameters(rec['n'],5,certified=False)
        expected={key:str(P.beta[int(key[0])][int(key[1])]) for key in rec['beta']}
        require(expected == rec['beta'], "Published rank-five generic baseline mismatch")
    return {"source_commit":data['source_commit'],"orders":[z['n'] for z in data['cases']]}


def run():
    baseline=baseline_check()
    large=[]
    for r in range(2,13):
        for n in (32*r*r,32*r*r+1):
            large.append(finite_checks(parameters(n,r),True))
    examples=[finite_checks(parameters(n,r,certified=False),False)
              for n,r in [(4,2),(6,3),(8,4),(12,5),(18,6),(21,7)]]
    literal=[literal_checks(n,r) for n,r in [(4,2),(6,3),(8,4)]]
    controls=negative_controls()
    return {"agent":"six-downset-2","role":"researcher","scope":"Every integer r>=2,n>=32r^2; finite checks are validation",
            "baseline":baseline,"quantitative_cases":large,"smaller_examples":examples,
            "literal":literal,"controls":controls,"max_residual_size":2,
            "trust_boundary":"Unbounded binomial estimates, harmonic completeness, quotient spectrum, Schur repair and tensor/rank bridges are the written unformalized proof"}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    result=run()
    if args.check:
        require(result == json.loads(args.check.read_text()), "Expected results mismatch")
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({"ok":True,"quantitative_cases":len(result['quantitative_cases']),
                      "smaller_examples":len(result['smaller_examples']),"literal_orders":[x['N'] for x in result['literal']],
                      "max_residual_size":2,"rejected_controls":result['controls']['rejected']}))
