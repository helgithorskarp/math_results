#!/usr/bin/env python3
"""Exact primal, one-vector obstruction, and literal harmonic validation.

six-downset-2, researcher. Standard library only; no numerical solver.
All proof checks survive -O. Harmonic exhaustion and infinite band barrier
are ordinary mathematical bridges written in PROOF.md, not extrapolation.
"""
from dataclasses import replace
from fractions import Fraction as Q
from hashlib import sha256
from math import comb
from pathlib import Path
import argparse
import copy
import json

from matrices import Parameters,affine,counts,sectors,trade,slack_entry,literal_matrix,require
from exact import psd_rank


def schur_rank(A):
    """Independent rational Schur algorithm (no Bareiss recurrence)."""
    d=len(A)
    require(all(len(row)==d for row in A),"Schur shape")
    require(all(type(v) in (int,Q) for row in A for v in row),"Exact Schur input")
    require(all(A[i][b]==A[b][i] for i in range(d) for b in range(d)),"Schur symmetry")
    Z=[[Q(v) for v in row] for row in A];rank=0
    while Z:
        d=len(Z);require(all(Z[i][i]>=0 for i in range(d)),"Negative rational Schur diagonal")
        k=next((i for i in range(d) if Z[i][i]>0),None)
        if k is None:
            require(all(v==0 for row in Z for v in row),"Nonzero rational zero-diagonal residual")
            break
        keep=[i for i in range(d) if i!=k];pivot=Z[k][k]
        Z=[[Z[i][b]-Z[i][k]*Z[k][b]/pivot for b in keep] for i in keep];rank+=1
    return rank


def rank_check(H,expected):
    require(psd_rank(H)==schur_rank(H)==expected,"Two independent exact PSD/rank criteria")


def gram(g,K):return [[g[i]*v for v in row] for i,row in enumerate(K)]


def energy(g,K,v):
    require(len(g)==len(K)==len(v),"Energy dimensions")
    return sum((g[i]*v[i]*sum(x*y for x,y in zip(row,v)) for i,row in enumerate(K)),Q(0))


def projected_gap(H,g,kernels):
    """H-G+G V(V^T G V)^(-1)V^T G; credited projector algebra."""
    d=len(g);k=len(kernels)
    V=[[Q(col[i]) for col in kernels] for i in range(d)]
    A=[[sum(g[i]*V[i][a]*V[i][b] for i in range(d)) for b in range(k)] for a in range(k)]
    if k==2:
        det=A[0][0]*A[1][1]-A[0][1]**2;require(det>0,"Independent projector columns")
        Inv=[[A[1][1]/det,-A[0][1]/det],[-A[1][0]/det,A[0][0]/det]]
    elif k==1:Inv=[[1/A[0][0]]]
    else:require(k==0,"Projector dimension");Inv=[]
    return [[H[i][b]-g[i]*int(i==b)+g[i]*g[b]*
             sum((V[i][a]*Inv[a][c]*V[b][c] for a in range(k) for c in range(k)),Q(0))
             for b in range(d)] for i in range(d)]


def validate(P):
    n,r,N,s,w=P.n,P.r,P.N,P.s,P.width
    require((N,s)==counts(n,r),"Exact downset counts")
    require(type(w) is int and 1<=w<=r,"Exact width")
    b=P.beta
    require(len(b)==r+1 and all(len(row)==r+1 for row in b),"Weight shape")
    require(all(type(v) is Q for row in b for v in row),"Rational weights")
    require(all(b[a][k]==b[k][a] for a in range(r+1) for k in range(r+1)),"Weight symmetry")
    require(all(b[0][a]==0 for a in range(r+1)),"No empty seed weights")
    require(all(b[a][k]==0 for a in range(1,r-w+1) for k in range(1,r-w+1)),"Inactive band")
    for a in range(1,r+1):
        require(sum(b[a][k]*comb(n-a,k) for k in range(1,r+1))==N-1-s,"Center equation")
        require(sum(b[a][k]*comb(n-a-1,k-1) for k in range(1,r+1))==s,"Star equation")
        require(sum(trade(n,a,k)*comb(n-a-1,k-1) for k in range(1,r+1))==0,"Trade kills stars")
    epsilon=Q(n,72*(N-1)*(n-1)*(n-2)*(n-3))
    require(P.epsilon==epsilon>0,"Prescribed positive rational repair")
    mass=sum(comb(n,a)*trade(n,a,k)*comb(n-a,k) for a in range(1,r+1) for k in range(1,r+1))
    require(mass==Q(n*(n-1)*(n-2)*(n-3),4),"Trade mass")
    for a in range(1,r+1):
        row=P.epsilon*sum(trade(n,a,k)*comb(n-a,k) for k in range(1,r+1))
        A=(1<<a)-1
        require(slack_entry(P,0,A)==1-row,"All empty layer rows")
        nonempty=s+sum((b[a][k]+P.epsilon*trade(n,a,k))*comb(n-a,k) for k in range(1,r+1))
        require(nonempty+slack_entry(P,0,A)==N,"All original nonempty row sums")
    require(slack_entry(P,0,0)+sum(comb(n,a)*slack_entry(P,0,(1<<a)-1) for a in range(1,r+1))==N,
            "Whole empty row and loop")
    rank0=[];upper0=[];repaired0=[];upper1=[];tot=[0,0,0,0];dimension=0
    repaired=sectors(P,repaired=True)
    for j,aa,g,K,U in sectors(P):
        d=len(aa);mult=comb(n,j)-(comb(n,j-1) if j else 0);dimension+=mult*d
        require(all(type(v) is int and v>0 for v in g),"Positive complete-sector metric")
        kernels=[[1]*d,aa] if j==0 else [[1]*d] if j==1 else []
        for v in kernels:
            require(all(sum(x*y for x,y in zip(row,v))==0 for row in K),"All forced centered kernels")
        rc=d-len(kernels);H=gram(g,K);HU=gram(g,U)
        rank_check(H,rc);rank_check(HU,d)
        rank_check(projected_gap(H,g,kernels),rc)
        rank_check([[HU[i][k]-g[i]*int(i==k) for k in range(d)] for i in range(d)],d-int(j==0))
        _,_,_,KR,UR=repaired[j];rr=d-int(j<=1)
        repaired_kernel=aa if j==0 else [1]*d if j==1 else None
        if repaired_kernel is not None:
            require(all(sum(x*y for x,y in zip(row,repaired_kernel))==0 for row in KR),"All repaired star kernels")
        rank_check(gram(g,KR),rr);rank_check(gram(g,UR),d)
        rank0.append(rc);upper0.append(d);repaired0.append(rr);upper1.append(d)
        for i,v in enumerate((rc,d,rr,d)):tot[i]+=mult*v
    require(dimension==N-1,"Complete nonempty dimension sum")
    require(tot==[N-n-2,N-1,N-n-1,N-1],"Complete centered/repaired rank accounting")
    return {'N':N,'s':s,'centered_sector_ranks':rank0,'upper_sector_ranks':upper0,
            'repaired_sector_ranks':repaired0,'repaired_upper_sector_ranks':upper1,
            'lower_full_rank':tot[2]+1,'upper_full_rank':tot[3],
            'centered_projected_lower_gap':'1','centered_upper_core_gap':'1',
            'epsilon':str(epsilon),'complete_nonempty_dimension':dimension}


def load_certificate(data):
    require((data['n'],data['r'],data['width'])==(20,10,4),"Certificate stated scope")
    meta,recover=affine(data['n'],data['r'],data['width'])
    require(meta['free_pairs']==data['free_pairs'],"Free coordinate order")
    require(all(type(v) is str for v in data['free_values']),"Exact string coordinates")
    P=recover([Q(v) for v in data['free_values']])
    require([[str(v) for v in row] for row in P.beta]==data['beta'],"Independent affine reconstruction")
    require(str(P.epsilon)==data['epsilon'],"Certificate repair coefficient")
    result=validate(P)
    require(all(result[k]==v for k,v in data['expected_ranks'].items()),"Certificate ranks")
    return P,meta,result


def obstruction():
    n,r=20,10;N,s=counts(n,r);aa=list(range(1,r+1));B=[comb(n,a) for a in aa]
    a1=sum(a*b for a,b in zip(aa,B));a2=sum(a*a*b for a,b in zip(aa,B))
    q=[Q(9-a) if a<=7 else Q(0) for a in aa]
    q0=sum(b*v for b,v in zip(B,q));qa=sum(a*b*v for a,b,v in zip(aa,B,q));q2=sum(b*v*v for b,v in zip(B,q))
    D=N*a2-a1*a1;require(D>0,"Positive cap projection denominator")
    p=Q(N*qa-a1*q0,D);v=[x-p*a for a,x in zip(aa,q)]
    e=(N-s)*q2-Q((N*qa-a1*q0)**2,D)
    require(e==Q(-177337417554617019686,9539792883)<0,"Exact universal cap obstruction")
    delta=Q(n*(n-1)*(n-2)*(n-3),4)
    trade_energy=sum((B[i]*q[i]*trade(n,a,b)*comb(n-a,b)*q[b-1]
                      for i,a in enumerate(aa) for b in aa),Q(0))
    require(trade_energy==81*delta==2354670,"Universal nonnegative trade worsens cap")
    meta,recover=affine(n,r,3);size=len(meta['free_pairs'])
    P0=recover([Q(0)]*size);K0=sectors(P0)[0][3];U0=sectors(P0)[0][4]
    require(energy(B,U0,v)==e,"Independent full degree-zero cap energy")
    for k in range(size):
        P=recover([Q(i==k) for i in range(size)]);K=sectors(P)[0][3]
        require(energy(B,[[x-y for x,y in zip(row,base)] for row,base in zip(K,K0)],v)==0,
                "Every free coefficient cancels in the obstruction")
    require(energy(B,sectors(P0,repaired=True)[0][4],v)==e-P0.epsilon*trade_energy,
            "Exact repaired cap obstruction")
    _,old=affine(n,r,2);Pold=old([]);vv=[Q(a>=9) for a in aa]
    old_energy=energy(B,sectors(Pold)[0][3],vv)
    require(old_energy==energy(B,sectors(Pold,repaired=True)[0][3],vv)==-476427945,
            "Published centered two-layer failure reproduced")
    return {'n':n,'r':r,'N':N,'s':s,'inactive_through':7,'q':[str(x) for x in q],
            'cardinality_first_moment':a1,'cardinality_second_moment':a2,
            'q_sum':str(q0),'q_cardinality_moment':str(qa),'q_squared_norm':str(q2),
            'denominator':D,'projection_coefficient':str(p),
            'upper_energy_at_zero_trade':str(e),'upper_energy_trade_coefficient':str(-trade_energy),
            'affine_three_layer':meta,'all_free_directions_canceled':size,
            'old_two_layer_negative_form':str(old_energy)}


def check_obstruction_fixture(data,ob):
    require(all(ob[k]==v for k,v in data['obstruction'].items() if k!='scope'),"Exact obstruction fixture")


def literal_audit(n,r):
    _,recover=affine(n,r,2);P=recover([]);V,L=literal_matrix(P);N=P.N;s=P.s
    def matrix_check(V,L):
        require(len(V)==N and len(set(V))==N and V[0]==0,"Literal original vertex list")
        require(len(L)==N and all(len(row)==N for row in L),"Literal shape")
        require(all(sum(row)==N for row in L),"Literal original row sums")
        require(all(L[i][b]==L[b][i] for i in range(N) for b in range(N)),"Literal original symmetry")
        require(all(L[i][i]==s for i in range(1,N)),"Literal diagonal")
        require(all(L[i][b]==0 for i in range(N) for b in range(N) if i!=b and V[i]&V[b]),"Literal intersecting support")
        U=[[Q(N*int(i==b))-L[i][b] for b in range(N)] for i in range(N)]
        require(psd_rank(L)==N-n and psd_rank(U)==N-1,"Literal full endpoint ranks")
        C=[[L[i+1][b+1]-1 for b in range(N-1)] for i in range(N-1)]
        rows=list(map(sum,C))
        require(L[0][0]==1+sum(rows) and all(L[0][i+1]==1-rows[i] for i in range(N-1)),"Literal empty lift")
        for k in range(n):
            z=[Q(int(A>>k&1))-Q(s,N) for A in V]
            require(all(sum(x*y for x,y in zip(row,z))==0 for row in L),"Literal whole centered stars")
    matrix_check(V,L)
    if N==11:rank_check(L,N-n)
    action_count=0
    for repaired in (False,True):
        F=V[1:];C=[[slack_entry(P,A,B,repaired=repaired)-1 for B in F] for A in F]
        for j,aa,g,K,U in sectors(P,repaired=repaired):
            def harmonic(A):
                v=1
                for i in range(j):v*=int(A>>(2*i)&1)-int(A>>(2*i+1)&1)
                return v
            basis=[[Q(harmonic(A)) if A.bit_count()==a else Q(0) for A in F] for a in aa]
            for k,f in enumerate(basis):
                require(sum(x*x for x in f)==2**j*g[k],"Literal harmonic lifted norm")
                got=[sum(x*y for x,y in zip(row,f)) for row in C]
                expected=[sum(K[i][k]*basis[i][b] for i in range(len(aa))) for b in range(len(F))]
                require(got==expected,"Literal centered/repaired harmonic disjointness action")
                action_count+=1
    digest=sha256(json.dumps([[str(x) for x in row] for row in L],separators=(',',':')).encode()).hexdigest()
    return {'n':n,'r':r,'N':N,'lower_rank':N-n,'upper_rank':N-1,
            'literal_L_sha256':digest,'literal_harmonic_columns':action_count},matrix_check,V,L


def band_barrier():
    # This exact polynomial coefficient identity supports the written induction.
    def mul(a,b):
        c=[0]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b):c[i+j]+=x*y
        return c
    left=mul(mul([2,2],[2,2]),[1,3]);right=mul(mul([1,2],[1,2]),[4,3])
    require([x-y for x,y in zip(left,right)]==[0,1,0,0],"Central binomial induction identity")
    require(Q(1,48)<Q(1,36),"All-width quantitative tail constant")
    probes=[]
    for k in range(1,6):
        r=16*k*k;N,s=counts(2*r,r);low=sum(comb(2*r,a) for a in range(3,r-k+1))
        require(s==4**r//4 and low>s,"Fixed band/trade obstruction corroboration")
        require(Q(comb(2*r,r)**2,16**r)<=Q(1,3*r+1),"Inductive central binomial bound at probe")
        require(Q(4**r,12)>1+2*r*r+r,"Excluded singleton/pair layer bound")
        probes.append({'width':k,'r':r,'n':2*r,'inactive_count_exceeds_s':True})
    require(4**5>12*(1+2*5*5+5),"Polynomial tail base")
    # 4(1+2r^2+r)-(1+2(r+1)^2+(r+1))=6r^2-r.
    base_poly=[1,1,2];next_poly=[4,5,2]
    require([4*x-y for x,y in zip(base_poly,next_poly)]==[0,-1,6],"Polynomial growth identity")
    return {'ordinary_scope':'all integers k>=1,r>=16k^2,n=2r; top-band plus any real singleton/pair trade',
            'inactive_layers':'3..r-k','polynomial_difference_coefficients':[0,1,0,0],
            'polynomial_growth_coefficients':[0,-1,6],'finite_corroboration':probes}


def controls(P,data,literal,ob):
    rejected=[]
    def reject(name,f):
        try:f()
        except (ValueError,KeyError,IndexError,TypeError):rejected.append(name);return
        raise ValueError('Corruption accepted: '+name)
    bad=copy.deepcopy(data);bad['free_values'][0]=0.2
    reject('floating free coordinate',lambda:load_certificate(bad))
    bad=copy.deepcopy(data);bad['free_pairs']=bad['free_pairs'][::-1]
    reject('changed free coordinate order',lambda:load_certificate(bad))
    bad=copy.deepcopy(data);bad['beta'][3][9]='1'
    reject('changed certificate weight',lambda:load_certificate(bad))
    b=[list(row) for row in P.beta];b[3][9]+=1;b[9][3]+=1
    reject('changed symmetric moment weight',lambda:validate(replace(P,beta=tuple(tuple(row) for row in b))))
    b=[list(row) for row in P.beta];b[3][9]+=1
    reject('asymmetric seed',lambda:validate(replace(P,beta=tuple(tuple(row) for row in b))))
    b=[list(row) for row in P.beta];b[1][1]=Q(1)
    reject('nonzero inactive weight',lambda:validate(replace(P,beta=tuple(tuple(row) for row in b))))
    reject('negative repair scalar',lambda:validate(replace(P,epsilon=-P.epsilon)))
    reject('missing seed row',lambda:validate(replace(P,beta=P.beta[:-1])))
    bad=copy.deepcopy(data);bad['obstruction']['upper_energy_at_zero_trade']='0'
    reject('changed obstruction energy',lambda:check_obstruction_fixture(bad,ob))
    bad=copy.deepcopy(data);bad['obstruction']['projection_coefficient']='1'
    reject('changed cap projection',lambda:check_obstruction_fixture(bad,ob))
    for label,A in [('negative diagonal',[[-1]]),('zero diagonal nonzero residual',[[0,1],[1,0]]),
                    ('asymmetric form',[[1,0],[1,1]]),('floating form',[[1.0]])]:
        reject('Bareiss '+label,lambda A=A:psd_rank(A))
        reject('Schur '+label,lambda A=A:schur_rank(A))
    checker,V,L=literal;bad=[row[:] for row in L];bad[0][0]+=1
    reject('literal empty loop',lambda:checker(V,bad))
    bad=[row[:] for row in L];bad[1][1]+=1
    reject('literal intersecting diagonal',lambda:checker(V,bad))
    reject('omitted literal empty vertex',lambda:checker(V[1:],L))
    return rejected


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-results',action='store_true')
    args=parser.parse_args();root=Path(__file__).resolve().parent
    raw=(root/'CERTIFICATE.json').read_bytes();data=json.loads(raw)
    P,meta,result=load_certificate(data);ob=obstruction()
    check_obstruction_fixture(data,ob)
    literal=[];last=None
    for n,r in ((4,2),(6,3)):
        rec,checker,V,L=literal_audit(n,r);literal.append(rec);last=(checker,V,L)
    result={'agent':'six-downset-2','role':'researcher','certificate_sha256':sha256(raw).hexdigest(),
            'scope':'Minimum width4 at D(20,10) within C=sI-J+W+tDelta,t>=0; unrestricted W off the inactive prefix',
            'affine_four_layer':meta,'primal':result,'obstruction':ob,'fixed_band_trade_barrier':band_barrier(),
            'literal_baseline_validation':literal,'rejected_controls':controls(P,data,last,ob),
            'proof_trust':'Exact rational arithmetic plus ordinary complete harmonic/kernel/moment and infinite-binomial bridges; unformalized'}
    expected=root/'RESULTS.json'
    if args.write_results:expected.write_text(json.dumps(result,indent=2)+'\n')
    else:require(json.loads(expected.read_text())==result,"Published exact result fixture")
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
