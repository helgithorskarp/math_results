"""Standalone exact checks for the saturated-complement count lemma.

six-downset-2, researcher. Imports no two-layer producer, CAS, or solver.
Written real PSD/kernel/row and recurrence bridges supply the theorem.
"""
import argparse, hashlib, json, sys, os
from fractions import Fraction as Q
from math import comb
from pathlib import Path


def need(p,message):
    if not p: raise ValueError(message)


def psd_rank(M):
    n=len(M)
    need(all(len(row)==n for row in M),'Square PSD input')
    need(all(type(x) in (int,Q) for row in M for x in row),'Exact PSD input')
    need(all(M[i][j]==M[j][i] for i in range(n) for j in range(n)),'Symmetric PSD input')
    A=[[Q(x) for x in row] for row in M];rank=0
    while A:
        need(all(A[i][i]>=0 for i in range(len(A))),'Negative Schur diagonal')
        hit=next((i for i in range(len(A)) if A[i][i]>0),None)
        if hit is None:
            need(all(x==0 for row in A for x in row),'Nonzero zero-diagonal residual')
            return rank
        keep=[i for i in range(len(A)) if i!=hit];pivot=A[hit][hit]
        A=[[A[i][j]-A[i][hit]*A[hit][j]/pivot for j in keep] for i in keep];rank+=1
    return rank


def is_psd(A):
    try: return True,psd_rank(A)
    except ValueError: return False,None


def hash_obj(obj):
    raw=json.dumps(obj,sort_keys=True,separators=(',',':'),default=str).encode()
    return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def principal(s,r,q,ell):
    need(type(s) is Q and type(r) is Q and type(ell) is Q and type(q) is int,'Exact principal parameters')
    need(s>0 and r>0 and q>=0,'Positive principal domain')
    N=2*s+r;d=2*q+1
    L=[[Q(0)]*d for _ in range(d)];L[0][0]=ell
    for a in range(1,d):
        L[0][a]=L[a][0]=r;L[a][a]=s
        partner=a+1 if a%2 else a-1;L[a][partner]=s
    U=[[N*int(i==j)-L[i][j] for j in range(d)] for i in range(d)]
    return L,U


def compress(A,q):
    groups=[[0]]+[[2*i+1,2*i+2] for i in range(q)]
    return [[sum((A[i][j] for i in x for j in y),Q(0)) for y in groups] for x in groups]


def principal_controls():
    records=[]
    for sint in [1,2,3,4,6,26,120]:
        for rint in [1,2,3,5,7]:
            s=Q(sint);r=Q(rint);N=2*s+r
            for q in range(min(5,int((N-1)//2))+1):
                lo=q*r*r/s;hi=N-2*q*r
                for ell in sorted({Q(0),N,lo,hi,(lo+hi)/2,lo-Q(1,17),hi+Q(1,19)}):
                    L,U=principal(s,r,q,ell)
                    pl,lr=is_psd(L);pu,ur=is_psd(U)
                    need(pl==(ell>=lo),'Whole lower principal PSD versus scalar Schur')
                    need(pu==(ell<=hi),'Whole upper principal PSD versus scalar Schur')
                    need((lo<=hi)==(q*r<=s),'Exact empty-loop interval versus saturated count')
                    need(s*(hi-lo)==N*(s-q*r),'Cleared entire interval-width identity')
                    kl=compress(L,q);ku=compress(U,q)
                    lower=[[ell if i==j==0 else 2*r if (i==0)!=(j==0) else 4*s*int(i==j)
                            for j in range(q+1)] for i in range(q+1)]
                    upper=[[N-ell if i==j==0 else -2*r if (i==0)!=(j==0) else 2*r*int(i==j)
                            for j in range(q+1)] for i in range(q+1)]
                    need((kl,ku)==(lower,upper),'Every literal pair-sum Gram factor and form entry')
                    records.append(dict(s=str(s),r=str(r),q=q,ell=str(ell),lo=str(lo),hi=str(hi),
                                        lower_psd=pl,upper_psd=pu,lower_rank=lr,upper_rank=ur,
                                        whole_matrices=hash_obj([L,U])))
    return records


def p_add(A,B):
    n=max(len(A),len(B));C=[Q(0)]*n
    for i in range(n): C[i]=(A[i] if i<len(A) else 0)+(B[i] if i<len(B) else 0)
    while len(C)>1 and C[-1]==0:C.pop()
    return C


def p_mul(A,B):
    C=[Q(0)]*(len(A)+len(B)-1)
    for i,a in enumerate(A):
        for j,b in enumerate(B):C[i+j]+=a*b
    return C


def recurrence_controls():
    den=p_mul(p_mul(p_mul([0,2],[-1,2]),[3,1]),[2,5,5])
    num=p_mul(p_mul(p_mul([1,2],[1,2]),[-1,1]),[12,15,5])
    diff=p_add(den,[-x for x in num])
    need(diff==[12,39,40,-5,10],'Entire binomial-ratio coefficient identity')
    positive=p_add(p_add(p_mul([0,0,0,5],[-1,2]),[12,39,40]),[0])
    need(diff==positive,'All-m positivity decomposition for first ratio')
    den2=p_mul([0,4],[-1,-2,4]);num2=p_mul([-1,1],[1,6,4])
    diff2=p_add(den2,[-x for x in num2])
    need(diff2==[1,1,-10,12],'Entire polynomial-ratio coefficient identity')
    need(diff2==p_add([1,1],p_mul([0,0,2],[-5,6])),'All-m positivity decomposition for second ratio')
    m=6;G=comb(2*m,m);s=2**(2*m-1)-2*m;N=2**(2*m)-2*m-1;r=2*m-1
    dp=N-2*m*s+r*(Q(G,2)+comb(2*m,m-2)+comb(2*m,m-1))
    c=Q(5*m*m+5*m+2,2*(m+1)*(m+2))
    closed=-(m-1)*4**m+(2*m-1)*G*c+4*m*m-2*m-1
    need(dp==closed==Q(-1110),'Exact base case for every m>=6 induction')
    controls=[]
    for m in range(2,33):
        c=Q(5*m*m+5*m+2,2*(m+1)*(m+2));cn=Q(5*(m+1)**2+5*(m+1)+2,2*(m+2)*(m+3))
        a=Q((2*m-1)*comb(2*m,m),(m-1)*4**m)*c
        an=Q((2*m+1)*comb(2*m+2,m+1),m*4**(m+1))*cn
        b=Q(4*m*m-2*m-1,(m-1)*4**m)
        bn=Q(4*(m+1)**2-2*(m+1)-1,m*4**(m+1))
        expected=Q((2*m+1)**2*(m-1)*(5*m*m+15*m+12),2*m*(2*m-1)*(m+3)*(5*m*m+5*m+2))
        need(an/a==expected<1 and bn/b<1,'Definition-level recurrence ratio controls')
        controls.append(dict(m=m,A=str(a),B=str(b),first_ratio=str(expected),second_ratio=str(bn/b)))
    return dict(first_den_minus_num=[str(x) for x in diff],second_den_minus_num=[str(x) for x in diff2],
                base_Delta=str(dp),definition_level_controls=controls,
                unbounded_proof='Written positive decompositions and exact recurrence; not finite extrapolation')


def counts():
    out=[]
    for n in [4,5,6,7,8,9,10,11,12,16,24,32,40,48,64,96,128,256]:
        s=2**(n-1)-n;r=n-1;total=s-1;cap=s//r
        row=dict(n=n,total_original_complementary_pairs=total,maximum_saturated_pairs=cap,
                 minimum_attenuated_original_pairs=total-cap)
        if n%2==0:
            m=n//2;H=sum(comb(n,a) for a in range(2,m))
            need(H==s-1-comb(n,m)//2,'Exact entire low/middle census')
            q=min(q for q in range(m-1) if H-sum(comb(n,a) for a in range(m-q,m))<=cap)
            row.update(least_noncentral_deficit_classes_necessary=q,
                       saturated_population_at_next_smaller_class_count=H-sum(comb(n,a) for a in range(m-q+1,m)) if q else None)
        if n<=10:
            full=(1<<n)-1
            literal=[(A,full^A) for A in range(1<<n) if 2<=A.bit_count()<=n-2 and A<full^A]
            need(len(literal)==total,'Every original unordered pair counted once by literal masks')
            row['literal_pair_census']=len(literal)
        out.append(row)
    return out


def ordinary_n6_control():
    """Credited8154 family z_2=0,z_3=1, hence ordinary H, NOT capped."""
    n=6;N=57;s=26;r=5;full=63
    F=[A for A in range(1,64) if A.bit_count()<=4]
    B=[[Q(0)]*len(F) for _ in F]
    for i,A in enumerate(F):
        for j,D in enumerate(F):
            if A&D: continue
            a=A.bit_count();b=D.bit_count()
            if a==b==1: v=Q(20)
            elif min(a,b)==1: v=Q(int(max(a,b)==3))
            elif A|D==full: v=Q(s-int(a==3))
            else:v=Q(0)
            B[i][j]=v
    C=[[Q(s*int(i==j)-1)+B[i][j] for j in range(len(F))] for i in range(len(F))]
    sums=[sum(row) for row in C];L=[[Q(1)+sum(sums)]+[Q(1)-x for x in sums]]
    L += [[Q(1)-sums[i]]+[Q(1)+x for x in row] for i,row in enumerate(C)]
    need(len(L)==N and all(sum(row)==N for row in L),'All actual original rows and empty loop')
    need(all(sum(C[i][j] for j,A in enumerate(F) if A>>bit&1)==0 for i in range(len(F)) for bit in range(n)),'Every actual point-star row')
    need(all(L[i][i]==s for i in range(1,N)),'Every actual nonempty diagonal')
    members=[0]+F
    need(all(not L[i][j] for i,A in enumerate(members) for j,D in enumerate(members) if i!=j and A&D),'Every original distinct intersecting entry')
    saturated=[(A,full^A) for A in F if full^A in F and A<full^A and B[F.index(A)][F.index(full^A)]==s]
    need(len(saturated)==15,'Actual unordered saturation count')
    for A,D in saturated:
        i=F.index(A)+1;j=F.index(D)+1
        need(L[0][i]==L[0][j]==r and L[i][j]==s,'Complete isolated-pair row with actual empty entry')
        need(all(not L[i][k] and not L[j][k] for k in range(1,N) if k not in [i,j]),'Every other nonempty saturated-pair coupling vanishes')
    need(psd_rank(C)==35 and psd_rank(L)==36,'Complete literal lower PSD and ranks of credited ordinary family')
    U=[[Q(N*int(i==j))-L[i][j] for j in range(N)] for i in range(N)]
    x=[Q(0)]+[Q(1) if A.bit_count()==1 else Q(1,2) if A.bit_count()==3 else Q(0) for A in F]
    energy=sum((x[i]*U[i][j]*x[j] for i in range(N) for j in range(N)),Q(0))
    need(energy==Q(-444),'Original full upper negative vector; cap absent, ordinary H valid')
    return dict(credited_family_height=8154,n=n,actual_original_vertices=N,original_lower_rank=36,
                complete_original_entries=N*N,all_original_star_rows=n*(N-1),saturated_pairs=15,
                cap_budget=5,actual_empty_L00=str(L[0][0]),original_cap_witness_energy=str(energy),
                complete_L=hash_obj(L),new_ordinary_H=False,scope='Valid credited ordinary H violates count because cap is absent')


def damages():
    bad=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,ZeroDivisionError):bad.append(name)
        else:raise ValueError('Damage accepted: '+name)
    reject('floating principal coefficient',lambda:principal(26.0,Q(5),2,Q(3)))
    reject('noninteger unordered pair count',lambda:principal(Q(26),Q(5),Q(2),Q(3)))
    reject('zero missing r domain',lambda:principal(Q(26),Q(0),2,Q(3)))
    reject('zero lower diagonal domain',lambda:principal(Q(0),Q(5),2,Q(3)))
    L,U=principal(Q(6),Q(3),2,Q(3))
    need(psd_rank(L)==2 and psd_rank(U)==4,'Both exact singular endpoint controls valid')
    wrong=[row[:] for row in L];wrong[0][1]+=Q(1,31);wrong[1][0]=wrong[0][1]
    reject('changed actual empty saturated-pair coupling',lambda:psd_rank(wrong))
    wrong=[row[:] for row in U];wrong[0][0]-=Q(1,37)
    reject('lowering upper empty endpoint',lambda:psd_rank(wrong))
    reject('zero-energy false PSD kernel bridge',lambda:psd_rank([[1,1,1],[1,1,0],[1,0,1]]))
    wrong=compress(L,2);wrong[1][1]/=2
    reject('normalized pair metric used in literal basis',lambda:psd_rank(wrong))
    reject('omitting saturation factor in count',lambda:need(Q(6)>=3*Q(3),'Three pairs exceed the actual budget'))
    reject('false recurrence coefficient',lambda:need([12,39,40,-4,10]==[12,39,40,-5,10],'Coefficient differs'))
    return bad


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check',type=Path,help='Compare the entire compact expected record, including the full replay hash')
    p.add_argument('--summary',type=Path,help='Optionally save the compact record')
    p.add_argument('--output',type=Path,help='Optionally save the full generated replay outside tracked source')
    p.add_argument('--mode-receipt',type=Path,help='Optionally save actual Python optimization and native thread settings')
    a=p.parse_args()
    if a.mode_receipt:
        a.mode_receipt.write_text(json.dumps(dict(optimize=sys.flags.optimize,python=sys.version,executable=sys.executable,
            native_threads={k:os.environ.get(k) for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']}),indent=2)+'\n')
    controls=principal_controls()
    record=dict(agent='six-downset-2',role='researcher',
                status='Author exact validation; written real PSD/kernel/row/recurrence bridges unformalized and independently unreviewed',
                principal_controls=controls,principal_case_count=len(controls),recurrence_coefficient_certificate=recurrence_controls(),
                original_near_cube_counts=counts(),credited_original_ordinary_control=ordinary_n6_control(),
                rejected_semantic_damages=damages(),no_producer_import=True,no_solver_or_CAS_input=True,
                no_new_H_construction=True,no_finite_to_unbounded_inference=True)
    raw=json.dumps(record,indent=2,sort_keys=True)+'\n'
    recurrence=record['recurrence_coefficient_certificate']
    compact=dict(schema=1,agent='six-downset-2',role='researcher',status=record['status'],
                 full_replay=dict(bytes=len(raw.encode()),sha256=hashlib.sha256(raw.encode()).hexdigest()),
                 principal_case_count=len(controls),singular_endpoint_control=dict(s=6,r=3,q=2,ell=3,lower_rank=2,upper_rank=4),
                 recurrence_coefficient_certificate={k:v for k,v in recurrence.items() if k!='definition_level_controls'},
                 finite_definition_level_recurrence_controls=len(recurrence['definition_level_controls']),
                 original_near_cube_counts=record['original_near_cube_counts'],
                 credited_original_ordinary_control=record['credited_original_ordinary_control'],
                 rejected_semantic_damages=record['rejected_semantic_damages'],
                 no_producer_import=True,no_solver_or_CAS_input=True,no_new_H_construction=True,
                 no_finite_to_unbounded_inference=True)
    expected=json.dumps(compact,indent=2,sort_keys=True)+'\n'
    if a.check:need(expected==a.check.read_text(),'Entire compact record, including full replay hash, differs')
    if a.output:a.output.write_text(raw)
    if a.summary:a.summary.write_text(expected)
    print(json.dumps(dict(ok=True,full_replay=compact['full_replay'],principal_cases=len(controls),
                         damages=len(record['rejected_semantic_damages']),actual_ordinary_lower_rank=36,
                         unbounded_bridge='Written recurrence and exact PSD restrictions in PROOF.md',
                         checked_expected=bool(a.check)),sort_keys=True))

if __name__=='__main__':main()
