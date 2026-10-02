"""Small bridges, whole-entry comparisons and certificate damage controls."""
import bootstrap
from fractions import Fraction as F
from itertools import combinations
from tempfile import TemporaryDirectory
from pathlib import Path
from weights import formula,credited_formula,model
from poly import R,exact_divide,mul
from signs import lower_sign
from exact import require,digest,schur_psd,polynomial_psd,lift
from endpoint import endpoint
from parameters import parameters
from entries import certificate
from original import original,audit_whole,allocate


def bridge():
    q=4;s=16
    require(formula(F(q),F(1,2))==credited_formula(F(q)),'credited fixed-parameter baseline differs')
    X=[0]+sorted(sum(1<<i for i in pts) for size in (1,2,3)
        for pts in combinations(range(q+3),size) if size<3 or sum(i<3 for i in pts)>=2)
    typ=lambda A:((A&7).bit_count(),(A>>3).bit_count())
    w=formula(F(q),F(0))
    C=[[F(s-1) if A==B else F(-1) if A&B else w[tuple(sorted((typ(A),typ(B))))]-1 for B in X[1:]] for A in X[1:]]
    kernels=[[F(bool(A&(1<<i))) for A in X[1:]] for i in range(3)]
    kernels.append([F(A.bit_count()==3 or A.bit_count()==2 and A&7==A) for A in X[1:]])
    kernels.append([F(1)]*len(C))
    require(all(sum(row[i]*v[i] for i in range(len(C)))==0 for row in C for v in kernels),'zero original five kernel actions')
    rank=schur_psd(C);require(rank==36,'zero q4 original rank')
    data=model(F(q),formula(F(q),F(0)));secondary=[]
    for item in data:
        degree=item['degree'];levels=item['levels'];G=item['lower']
        anchors=[(0,1),(1,0),(2,0)] if degree==(0,0) else [(1,0)] if degree==(1,0) else []
        keep=[i for i in range(len(levels)) if levels[i] not in anchors]
        quotient=[[G[i][j].at(0) for j in keep] for i in keep]
        secondary_rank,sha,den=polynomial_psd(quotient)
        require(secondary_rank==len(keep),'zero quotient characteristic rank')
        secondary.append({'degree':degree,'rank':secondary_rank,'coefficient_sha256':sha,'denominator':den})
    return {'q':4,'full_N':42,'nonempty_rank':rank,'nullity':5,
            'core_sha256':digest([[str(x) for x in row] for row in C]),
            'credited_fixed_kappa_half_table_exact':True,'secondary_zero_quotients':secondary}


def entry_checks():
    records=[]
    for q,k in ((4,1),(7,2),(12,3)):
        p,X,C,Ct,L=original(q,k);info,entry=certificate(q,k);N=p['N'];s=p['s']
        require(info==p,'entry/matrix parameter agreement')
        values=[[entry(A,B) for B in X] for A in X]
        require(all(values[i][j]==(L[i][j]-s*int(i==j))/(N-s) for i in range(N) for j in range(N)),
                'whole direct-entry/original-matrix discrepancy')
        records.append({'q':q,'k':k,'compared_entries':N*N,'matrix_sha256':digest([[str(x) for x in row] for row in values])})
    p,entry=certificate(1000000,100000,F(1,10**12))
    # Scalar and constant-size type-table inputs only; no domain allocation.
    values=[str(entry(A,B)) for A,B in ((0,0),(0,1),(1,2),(2,5),(8,16),(24,32))]
    require(entry(1,1)==0 and entry(1,3)==0,'large scalar support checks')
    return {'original_comparisons':records,'large_scalar_only':{'q':1000000,'k':100000,'t':'1/1000000000000','entries':values}}


def damages():
    rejected=[]
    def reject(name,call):
        try:call()
        except (ValueError,TypeError,FileNotFoundError):rejected.append(name)
        else:raise ValueError('accepted damaged certificate: '+name)
    for q,k in ((True,1),(4.0,1),(3,1),(7,0),(7,8),(4,2),(6,2),(11,3)):
        reject('parameters '+repr((q,k)),lambda q=q,k=k:parameters(q,k))
    reject('literal q beyond bound',lambda:allocate(13,3))
    reject('literal N beyond bound',lambda:allocate(12,1))
    for t in (F(0),F(-1),0.001,F(1)):
        reject('t '+str(t),lambda t=t:certificate(4,1,t))
    p,entry=certificate(4,1)
    for A in (True,-1,1<<7,14,56):
        reject('invalid member '+str(A),lambda A=A:entry(0,A))
    reject('negative sign constant',lambda:lower_sign((F(-1),F(1))))
    reject('zero sign constant',lambda:lower_sign((F(0),F(1))))
    with TemporaryDirectory() as tmp:
        path=Path(tmp)/'bad.py';path.write_text('changed source\n')
        reject('dependency changed',lambda:bootstrap.setup(Path(tmp),{'bad.py':'0'*64}))
    p,X,C,Ct,L=original(4,1)
    reject('missing actual empty',lambda:audit_whole(4,1,X[1:],L))
    bad=[row[:] for row in L];bad[0][0]=float(bad[0][0])
    reject('inexact empty loop',lambda:audit_whole(4,1,X,bad))
    bad=[row[:] for row in L];bad[0][1]+=1
    reject('asymmetric entry',lambda:audit_whole(4,1,X,bad))
    bad=[row[:] for row in L];bad[0][0]+=1
    reject('wrong whole row sum',lambda:audit_whole(4,1,X,bad))
    # A row-balanced symmetric error on intersecting members violates support.
    bad=[row[:] for row in L];i=X.index(1);j=X.index(3)
    bad[i][j]+=1;bad[j][i]+=1;bad[i][i]-=1;bad[j][j]-=1
    reject('row-balanced support damage',lambda:audit_whole(4,1,X,bad))
    bad=[row[:] for row in Ct];i=X[1:].index(1);j=X[1:].index(2)
    bad[i][j]-=p['tau'];bad[j][i]-=p['tau']
    reject('missing repair balance edge',lambda:audit_whole(4,1,X,lift(bad)))
    # The two smaller-star difference has negative quadratic form on this
    # disjoint edge; positivity must fail even though lift rows/support hold.
    bad=[row[:] for row in C];i=X[1:].index(2);j=X[1:].index(4)
    bad[i][j]+=p['tau'];bad[j][i]+=p['tau']
    reject('indefinite smaller-singleton substitute',lambda:schur_psd(bad))
    reject('negative exact PSD pivot',lambda:schur_psd([[F(-1)]]))
    reject('singular PSD zero-row inconsistency',lambda:schur_psd([[F(0),F(1)],[F(1),F(0)]]))
    require(schur_psd([[F(0)]])==0 and schur_psd([[F(2),F(1)],[F(1),F(2)]])==2,'positive checker controls')
    return {'rejection_count':len(rejected),'rejected':rejected,'positive_checker_controls':2}
