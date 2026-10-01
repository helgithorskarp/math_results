#!/usr/bin/env python3
"""Finite exact validation of the written, quantified linear-range argument.

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


def finite_checks(P):
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



def weighted_radius(A, h, s):
    require(len(A) == len(h) and all(type(v) is Q and v>0 for v in h), "Positive rational scaling")
    require(all(len(row) == len(A) for row in A), "Weighted row shape")
    require(all(type(v) in (int,Q) for row in A for v in row), "Exact weighted rows")
    return max((sum(abs(v-Q(s*int(i==k)))*h[k]/h[i]
                    for k,v in enumerate(row))/s
                for i,row in enumerate(A)), default=Q(0))


def gap_matrix(H,g,kernels,gamma):
    """Gram form of H-gamma*G plus gamma times its forced-kernel projector."""
    d=len(g); k=len(kernels)
    V=[[Q(col[i]) for col in kernels] for i in range(d)]
    Gram=[[sum((g[i]*V[i][a]*V[i][b] for i in range(d)),Q(0))
           for b in range(k)] for a in range(k)]
    if k==1:
        Inv=[[1/Gram[0][0]]]
    elif k==2:
        det=Gram[0][0]*Gram[1][1]-Gram[0][1]**2
        require(det>0,"Independent forced kernels")
        Inv=[[Gram[1][1]/det,-Gram[0][1]/det],
             [-Gram[1][0]/det,Gram[0][0]/det]]
    else:
        require(k==0,"Kernel dimension")
        Inv=[]
    return [[H[i][b]-gamma*g[i]*int(i==b)+gamma*g[i]*g[b]*
             sum((V[i][a]*Inv[a][c]*V[b][c] for a in range(k) for c in range(k)),Q(0))
             for b in range(d)] for i in range(d)]


def linear_checks(P):
    n,r,N,s,p=P.n,P.r,P.N,P.s,P.r-1
    require(n>=8*r,"Linear theorem domain")
    T=N-1-s
    D=(p-1)+2*sum((p-k)*comb(n-1,k) for k in range(1,p))
    require(D==r*T-(n-p)*s,"Positive weighted-tail identity")
    d=Q(D,s); tau=Q(T,s); kappa=Q(comb(n,p),comb(n,r))
    aa=list(range(1,p)); R=[Q(comb(n,a),comb(n,p)) for a in aa]
    f=[d-(p-a) for a in aa]; h=[Q(r-a) for a in aa]
    require(0<=d<=Q(2,5),"Cancellation moment")
    require(all(v<=Q(1,7)**(p-a) for a,v in zip(aa,R)),"Tail ratio")
    sumR=sum(R,Q(0)); W=sum((u*v for u,v in zip(h,R)),Q(0))
    F0=sum((abs(u)*v for u,v in zip(f,R)),Q(0))
    F1=sum((h0*abs(u)*v for h0,u,v in zip(h,f,R)),Q(0))
    require(sumR<=Q(1,6) and W<=Q(3,8) and F0<=Q(1,3) and F1<=Q(3,5),"Finite weighted tails")
    ell=sum((u*v for u,v in zip(f,R)),Q(0))
    x=d-sum((h0*u*v for h0,u,v in zip(h,f,R)),Q(0))
    y=tau-ell-x; z=kappa*y
    ellr=kappa*sum(((tau-u)*v for u,v in zip(f,R)),Q(0))
    v=tau-ellr-z
    require(tau<=Q(n,r) and kappa<=Q(1,7) and kappa*tau<=Q(8,7),"Top-tail ratios")
    require(abs(ell)<=Q(1,3) and abs(x)<=1 and abs(z)<=Q(4,3) and abs(ellr)<=Q(1,4),"Normalized corners")
    require(kappa*tau*W+kappa*F1<=Q(18,35),"Reverse weighted tail")
    for a,f0,R0 in zip(aa,f,R):
        require(Q(P.beta[a][p]*comb(n-a,p),s)==f0,"Forward p cancellation")
        require(Q(P.beta[p][a]*comb(n-p,a),s)==f0*R0,"Reverse p cancellation")
        require(Q(P.beta[a][r]*comb(n-a,r),s)==tau-f0,"Forward r cancellation")
        require(Q(P.beta[r][a]*comb(n-r,a),s)==kappa*(tau-f0)*R0,"Reverse r cancellation")
    for a,b,u in [(p,p,x),(p,r,y),(r,p,z),(r,r,v)]:
        require(Q(P.beta[a][b]*comb(n-a,b),s)==u,"Corner identity")
    A=quotients(P)
    radii=[weighted_radius(A[0],h,s),
           weighted_radius(A[1],[Q(r-a) for a in range(1,r)],s)]
    require(radii[0]<=Q(39,35) and radii[1]<=Q(3,5),"Forced-quotient weighted radii")
    mlow=sum(comb(n,a) for a in aa)
    require(Q(mlow,s)<=Q(4,21),"Zero-sector lower gap")
    sectors0=sectors(P)
    gaps=[]
    for j,bb,g,K,U in sectors0:
        dim=len(bb)
        HC=[[g[i]*entry for entry in row] for i,row in enumerate(K)]
        if j==0:
            gamma=Q(17*s,21); kernels=[[1]*dim,bb]
        elif j==1:
            gamma=Q(2*s,5); kernels=[[1]*dim]
        else:
            gamma=Q(2*s,3); kernels=[]
            hJ=[Q(max(1,r-a)) for a in bb]
            rad=weighted_radius(K,hJ,s)
            require(rad<=Q(1,3),"All higher weighted radii")
            radii.append(rad)
        require(psd_rank(gap_matrix(HC,g,kernels,gamma))==dim-len(kernels),"Exact projected lower spectral gap")
        capgap=[[Q(74*s,35)*g[i]*int(i==k)-HC[i][k]
                 for k in range(dim)] for i in range(dim)]
        require(psd_rank(capgap)==dim,"Exact upper core spectral gap")
        gaps.append(str(gamma))
        for a in bb:
            for b in bb:
                theta=Q(comb(n-a-j,b-j),comb(n-a,b)) if j else Q(1)
                if j:
                    require(theta<=Q(1,6)**j and tau*theta<=Q(8,7)*Q(1,6)**(j-1),"Every falling-ratio inequality")
    require(N>=8*s+1 and s>=n and Q(2*s,5)>=1,"Full core/cap repair gaps")
    record=finite_checks(P)
    record['linear_bounds']={'d':str(d),'weighted_tail':str(W),'F0':str(F0),'F1':str(F1),
                             'x':str(x),'y':str(y),'z':str(z),'v':str(v),
                             'weighted_radii':[str(rad) for rad in radii],
                             'verified_sector_lower_gaps':gaps,'upper_core_bound':str(Q(74*s,35))}
    return record


def constants_check():
    rho,q=Q(1,7),Q(1,6)
    require(2*rho/(1-rho)**2==Q(7,18)<Q(2,5),"Infinite d sum")
    require(rho*(2-rho)/(1-rho)**2==Q(13,36)<Q(3,8),"Infinite first tail sum")
    require(rho/(1-rho)**2+Q(2,5)*rho/(1-rho)==Q(47,180)<Q(1,3),"Infinite absolute tail sum")
    require(2*rho/(1-rho)**3+Q(2,5)*rho*(2-rho)/(1-rho)**2==Q(323,540)<Q(3,5),"Infinite weighted absolute sum")
    require(Q(3,5)+Q(18,35)==Q(39,35),"Zero upper radius arithmetic")
    require(q*(Q(18,35)/2+1+Q(2,3))==Q(101,315)<Q(1,3),"One low radius arithmetic")
    require(q*(Q(39,35)+1+Q(4,3))==Q(181,315)<Q(3,5),"One top radius arithmetic")
    require(Q(8,7)*q+Q(4,3)*q*q==Q(43,189)<Q(1,4),"Higher off-diagonal arithmetic")
    require(Q(8,7)*q+Q(5,3)*q*q==Q(179,756)<Q(1,4),"Higher diagonal arithmetic")
    require(2*q*q+Q(4,7)*q==Q(19,126)<Q(1,6),"Higher low radius arithmetic")
    require(Q(8,5)*q*q+Q(1,4)==Q(53,180)<Q(1,3),"Higher p radius arithmetic")
    require((Q(18,35)+Q(4,3))*q*q+Q(1,4)==Q(1139,3780)<Q(1,3),"Higher r radius arithmetic")
    return {'exact_infinite_sum_and_radius_identities':12,'tail_ratio':'1/7','falling_ratio':'1/6'}


def baseline_check():
    data=json.loads(Path(__file__).with_name('BASELINE.json').read_text())
    for rec in data['rank_five']['cases']:
        P=parameters(rec['n'],5,certified=False)
        got={key:str(P.beta[int(key[0])][int(key[1])]) for key in rec['beta']}
        require(got==rec['beta'],"Published rank-five generic baseline")
    for rec in data['quadratic']['cases']:
        require(finite_checks(parameters(rec['n'],rec['r']))==rec,"Published quadratic exact baseline")
    return {'rank_five_commit':data['rank_five']['source_commit'],
            'rank_five_orders':[rec['n'] for rec in data['rank_five']['cases']],
            'quadratic_commit':data['quadratic']['source_commit'],
            'quadratic_pairs':[[rec['n'],rec['r']] for rec in data['quadratic']['cases']]}


def negative_controls():
    from dataclasses import replace
    count=0
    def reject(fn):
        nonlocal count
        try: fn()
        except (ValueError,TypeError): count+=1
        else: raise ValueError("A negative control passed")
    reject(lambda: parameters(15,2))
    reject(lambda: parameters(3,2,certified=False))
    reject(lambda: parameters(128.0,2))
    reject(lambda: parameters(128,True))
    reject(lambda: psd_rank([[0,1],[1,0]]))
    reject(lambda: psd_rank([[1,0],[0,-1]]))
    reject(lambda: psd_rank([[1.0]]))
    reject(lambda: psd_rank([[1,1],[0,1]]))
    P=parameters(16,2)
    reject(lambda: slack_entry(P,1<<16,0))
    reject(lambda: slack_entry(P,7,0))
    reject(lambda: literal_matrix(parameters(128,2)))
    V,L=literal_matrix(P); L[0][0]+=1
    reject(lambda: require(all(sum(row)==len(V) for row in L),"Damaged empty loop"))
    reject(lambda: weighted_radius([[Q(1)]],[Q(0)],1))
    reject(lambda: weighted_radius([[1.0]],[Q(1)],1))
    reject(lambda: linear_checks(parameters(15,2,certified=False)))
    beta=list(map(list,P.beta)); beta[1][1]+=1
    reject(lambda: finite_checks(replace(P,beta=tuple(tuple(row) for row in beta))))
    bad=parameters(20,10,certified=False)
    mlow=sum(comb(20,a) for a in range(1,9))
    require(bad.s-mlow==-1805 and mlow*(bad.s-mlow)==-476427945,"Prior sparse failure witness")
    j,aa,g,K,U=sectors(bad)[0]
    require(fails_psd([[g[i]*v for v in row] for i,row in enumerate(K)]),"Prior sparse failure must reject")
    count+=1
    return {'rejected':count,'credited_sparse_failure':{'n':20,'r':10,'negative_full_core_form':-476427945}}


def run():
    baseline=baseline_check(); constants=constants_check()
    pairs=[(n,r) for r in range(2,15) for n in (8*r,8*r+1)]
    pairs += [(160,20),(161,20),(192,24),(193,24),(48,3),(112,7),(192,12)]
    cases=[linear_checks(parameters(n,r)) for n,r in pairs]
    literal=[literal_checks(4,2),literal_checks(16,2)]
    controls=negative_controls()
    return {'agent':'six-downset-2','role':'researcher',
            'scope':'All integer r>=2,n>=8r; exact finite checks validate the written unbounded proof',
            'baseline':baseline,'constants':constants,'linear_cases':cases,
            'literal':literal,'controls':controls,
            'trust_boundary':'Unformalized positive-tail, rescaled quotient, degree-zero singular-value, harmonic exhaustion, Schur repair, full lift and product arguments in PROOF.md; no numerical or solver inference'}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path); parser.add_argument('--check',type=Path)
    args=parser.parse_args(); result=run()
    if args.check: require(result==json.loads(args.check.read_text()),"Expected results mismatch")
    if args.output: args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'ok':True,'linear_cases':len(result['linear_cases']),
                      'max_r':max(z['r'] for z in result['linear_cases']),
                      'literal_orders':[z['N'] for z in result['literal']],
                      'rejected_controls':result['controls']['rejected'],
                      'exact_constant_identities':result['constants']['exact_infinite_sum_and_radius_identities']}))
