"""Whole literal-set/physical/original reader, without producer imports.

six-downset-1 / researcher. Same author, separate algorithm, NOT an
independent mathematical review. The all-count/real theorem is ordinary.
Matrices/vectors supplied by geometry.py are entirely untrusted input.
"""
import os
for _name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
              'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_name]='1'
from fractions import Fraction as Q
from hashlib import sha256
from math import lcm
from pathlib import Path
import argparse
import json
import resource
import signal
import time

LIMIT_BYTES=32*1024*1024

def require(ok,message):
    if not ok:
        raise ValueError(message)

def rational(x):
    require(type(x) is str,'exact canonical rational string')
    try:
        v=Q(x)
    except (ValueError,ZeroDivisionError):
        raise ValueError('exact canonical rational string') from None
    require(str(v)==x,'exact canonical rational string')
    return v

def matrix(raw,n,m=None):
    m=n if m is None else m
    require(type(raw) is list and len(raw)==n and
            all(type(row) is list and len(row)==m for row in raw),'whole matrix dimensions')
    return [[rational(x) for x in row] for row in raw]

def vec(raw,n):
    require(type(raw) is list and len(raw)==n,'whole vector dimensions')
    return [rational(x) for x in raw]

def dot(a,b):
    return sum((x*y for x,y in zip(a,b)),Q(0))

def apply(A,x):
    return [dot(row,x) for row in A]

def product(A,B):
    return [[dot(row,col) for col in zip(*B)] for row in A]

def total(rows):
    return [sum(col,Q(0)) for col in zip(*rows)]

def combine(a,b,t=Q(1)):
    return [x+t*y for x,y in zip(a,b)]

def scale(t,a):
    return [t*x for x in a]

def fingerprint(value):
    if value and isinstance(value[0],list):
        value=[[str(x) for x in row] for row in value]
    else:
        value=[str(x) for x in value]
    return sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()

def positive(A):
    """Sylvester test by full fraction-free symmetric leading-minor elimination."""
    n=len(A)
    require(n>0 and all(len(row)==n for row in A),'whole positive form dimension')
    require(all(A[i][j]==A[j][i] for i in range(n) for j in range(n)),
            'whole positive form symmetry')
    denominator=1
    for row in A:
        for x in row:
            denominator=lcm(denominator,x.denominator)
    B=[[x.numerator*(denominator//x.denominator) for x in row] for row in A]
    previous=1;pivots=[]
    for k in range(n):
        pivot=B[k][k]
        require(pivot>0,'exact positive leading minor')
        pivots.append(pivot)
        if k==n-1:
            break
        for i in range(k+1,n):
            for j in range(i,n):
                numerator=B[i][j]*pivot-B[i][k]*B[k][j]
                value,remainder=divmod(numerator,previous)
                require(remainder==0,'WHOLE exact fraction-free division')
                B[i][j]=value;B[j][i]=value
        previous=pivot
    return dict(dimension=n,all_positive=True,denominator=str(denominator),
        complete_leading_minors_sha256=fingerprint(pivots))

def inverse(A):
    n=len(A)
    B=[list(row)+[Q(i==j) for j in range(n)] for i,row in enumerate(A)]
    for k in range(n):
        i=next((j for j in range(k,n) if B[j][k]),None)
        require(i is not None,'whole original inverse nonsingular')
        B[k],B[i]=B[i],B[k];p=B[k][k]
        B[k]=[x/p for x in B[k]]
        for i in range(n):
            if i!=k:
                p=B[i][k]
                if p:
                    B[i]=[x-p*y for x,y in zip(B[i],B[k])]
    R=[row[n:] for row in B]
    I=[[Q(i==j) for j in range(n)] for i in range(n)]
    require(product(A,R)==I and product(R,A)==I,'BOTH WHOLE original inverse products')
    return R

def preimage(rows,target):
    """Solve R' x=target by complete exact rectangular elimination."""
    width=len(rows)
    A=[list(col)+[target[i]] for i,col in enumerate(zip(*rows))]
    pivots=[];row=0
    for col in range(width):
        j=next((j for j in range(row,len(A)) if A[j][col]),None)
        if j is None:
            continue
        A[row],A[j]=A[j],A[row];p=A[row][col]
        A[row]=[x/p for x in A[row]]
        for j in range(len(A)):
            if j!=row:
                p=A[j][col]
                if p:
                    A[j]=[x-p*y for x,y in zip(A[j],A[row])]
        pivots.append(col);row+=1
        if row==len(A):
            break
    require(row==len(target),'full original row preimage span')
    x=[Q(0)]*width
    for j,col in enumerate(pivots):
        x[col]=A[j][-1]
    require([dot(col,x) for col in zip(*rows)]==target,'ALL original preimage coordinates')
    return x

def literal(n,counts):
    require(type(n) is int and 4<=n<=6,'unchanged literal n<=6')
    require(type(counts) is list and 3<=len(counts)<=n and all(type(k) is int for k in counts),
            'literal distinct count/mark types')
    h=counts[0]
    require(3<=h<=10 and all(2<=k<h for k in counts[1:]),'unique heavy literal h<=10')
    F=sum(counts);N=2**n+6*F
    require(F>=9,'qualified total F>=9')
    require(N<=80,'unchanged original N80 parent guard BEFORE construction')
    oldsize=2**n-1;facetgroups=[g for g,k in enumerate(counts) for _ in range(k)]
    private=[];marked=[]
    for f,g in enumerate(facetgroups):
        leaves=(1<<(n+2*f),1<<(n+2*f+1))
        for A in (*leaves,leaves[0]|leaves[1]):
            private.append(A);marked.append(A|(1<<g))
    return [0]+list(range(1,2**n))+marked+private,facetgroups

def check(raw):
    needed={'version','agent','role','n','counts','N','s','q','F','ell','dimension',
            'retained_dimension','family','metric','rows','group_scalars','common_norm',
            'meanS','light_meanS','kappa','a','b','p','c','dual_vector'}
    require(type(raw) is dict and set(raw)==needed and type(raw['version']) is int
            and raw['version']==1 and raw['agent']=='six-downset-1'
            and raw['role']=='researcher','whole geometry schema')
    family,facetgroups=literal(raw['n'],raw['counts'])
    n,counts=raw['n'],raw['counts'];r,h=len(counts),counts[0]
    q,F,L=2**(n-1),sum(counts),sum(counts[1:])
    s,D0,m,ell=q+3*h,3*h,3*F,3*F+1
    N,d=len(family),len(family)-3
    expected_ints=dict(N=N,s=s,q=q,F=F,ell=ell,dimension=d,retained_dimension=2*q+m-2)
    require(all(type(raw[k]) is int and raw[k]==v for k,v in expected_ints.items()),
            'whole original dimensions/counts')
    require(type(raw['family']) is list and all(type(x) is int for x in raw['family'])
            and raw['family']==family and len(set(family))==N,'ENTIRE literal original family')
    present=set(family)
    for A in family:
        sub=A
        while True:
            require(sub in present,'literal downset completeness')
            if sub==0:
                break
            sub=(sub-1)&A
    stars=[sum(bool(A&(1<<j)) for A in family) for j in range(n+2*F)]
    require(stars[0]==s and all(v<s for v in stars[1:]),'unique largest ORIGINAL point star')
    Gamma=matrix(raw['metric'],d);rows=matrix(raw['rows'],N,d)
    require(rows[0]==scale(Q(-1),total(rows[1:])),'ACTUAL empty negative proper-row sum')
    sparse_metric=[[(j,x) for j,x in enumerate(row) if x] for row in Gamma]
    def image(v):
        return [sum((x*v[j] for j,x in row),Q(0)) for row in sparse_metric]
    images=[image(row) for row in rows]
    Qfull=[[dot(row,im) for im in images] for row in rows]
    C=[row[1:] for row in Qfull[1:]]
    require(all(sum(row,Q(0))==0 for row in Qfull),'ALL original lifted row sums')
    sums=[sum(row,Q(0)) for row in C]
    lifted=[[sum(sums,Q(0))]+[-x for x in sums]]
    lifted+=[[-sums[i]]+row for i,row in enumerate(C)]
    require(Qfull==lifted,'ENTIRE ACTUAL empty/loop original lift')
    mandatory=0
    for i,A in enumerate(family[1:],1):
        for j,B in enumerate(family[1:],1):
            if A&B:
                require(Qfull[i][j]==s*Q(i==j)-1,'ALL original mandatory norm/intersection positions')
                mandatory+=1
    oldsize=2*q-1;private_start=1+oldsize+m
    c0=Q(q*ell+9*sum(k*(h-k) for k in counts[1:])+3*h-6*F-1,ell*ell)
    require(Qfull[0][0]==c0==rational(raw['common_norm']),'ACTUAL empty norm and complete variable-count centroid')
    computed=[]
    fields={'k','v','R','B2','a','b','c','etaL','etaF','pair','mu','alpha','beta','off','nu'}
    for k in counts:
        R=Q(ell+1-q-3*(h-k),ell);v=R-1
        B2=Q(s*(k-1),3*k);a=R/(2*B2);b=-2*a;c=9*R/(2*s)
        etaL=s-1-c0-a*a*B2-Q(2*s,3)*c*c
        etaF=s-1-c0-b*b*B2-Q(2*s,3*(k-1))*c*c
        pair=-1-c0-a*b*B2
        mu=Q(s-3,3)-c0-9*R*R/(2*s*(k-1))
        alpha=2*s-27*(2*k-3)*R*R/(s*(k-1))
        beta=Q(2*s,3)-3*(k+3)*R*R/(s*(k-1))
        require(mu==(2*pair+etaF)/3 and alpha==2*(2*etaL-pair-etaF)
                and beta==etaF-mu,'complete original local scalar identities')
        require(mu-Q(s,5)>Q(1123,9180) and mu<Q(s,3) and s<alpha<=2*s
                and Q(s,2)<beta<=Q(2*s,3),'proved uniform local scalar bounds')
        computed.append(dict(k=Q(k),v=v,R=R,B2=B2,a=a,b=b,c=c,
            etaL=etaL,etaF=etaF,pair=pair,mu=mu,alpha=alpha,beta=beta))
    S=sum((k*g['mu'] for k,g in zip(counts,computed)),Q(0));SL=S-h*computed[0]['mu']
    for k,g in zip(counts,computed):
        g['off']=-k*g['mu']**2/(S*(k-1));g['nu']=g['mu']-g['off']
    require(type(raw['group_scalars']) is list and len(raw['group_scalars'])==r
            and all(type(g) is dict and set(g)==fields for g in raw['group_scalars']),
            'whole original scalar group census')
    require([{k:rational(v) for k,v in g.items()} for g in raw['group_scalars']]==computed,
            'ALL variable-count original scalar fields')
    require(rational(raw['meanS'])==S and rational(raw['light_meanS'])==SL,
            'weighted whole light mean sums')
    a=[Q(0)]*(N-1);b=[Q(0)]*(N-1)
    for f,g in enumerate(facetgroups):
        for j in range(3):
            if g==0:
                a[private_start-1+3*f+j]=Q(1,h)
            elif j==2:
                b[private_start-1+3*f+j]=computed[g]['mu']/SL
    p=combine(a,b,Q(-3));c=scale(Q(1,6),combine(a,b,Q(3)))
    require(vec(raw['a'],N-1)==a and vec(raw['b'],N-1)==b
            and vec(raw['p'],N-1)==p and vec(raw['c'],N-1)==c,
            'ALL ORIGINAL COUNT-WEIGHTED repair coefficients')
    chi=[Q(bool(A&1)) for A in family[1:]]
    rho=[Q(m,ell) if j<private_start-1 else Q(1) for j in range(N-1)]
    proper=rows[1:]
    require([dot(col,chi) for col in zip(*proper)]==[Q(0)]*d
            and [dot(col,rho) for col in zip(*proper)]==[Q(0)]*d,
            'BOTH complete original proper kernel relations')
    require(dot(p,chi)==dot(c,chi)==dot(p,rho)==0 and dot(c,rho)==1,
            'complete ORIGINAL rank-repair null pairings')
    dual=vec(raw['dual_vector'],d);dual_image=image(dual)
    require([dot(row,dual_image) for row in rows]==[Q(0)]+p,
            'EVERY original dual score INCLUDING ACTUAL empty')
    kappa=1/(h*computed[0]['mu'])+1/SL+4*sum(
        (k*g['mu']**2/(SL*SL*g['beta']) for k,g in zip(counts[1:],computed[1:])),Q(0))
    require(dot(dual,dual_image)==kappa==rational(raw['kappa']) and 0<kappa<Q(25,68),
            'WHOLE original weighted dual inverse energy and uniform bound')
    # The complete frame is built from every original row image, including empty.
    sparse_images=[[(j,x) for j,x in enumerate(im) if x] for im in images]
    frame=[[Q(0) for j in range(d)] for i in range(d)]
    for im in sparse_images:
        for i,x in im:
            for j,y in im:
                frame[i][j]+=x*y
    physical_cap=[[2*s*Gamma[i][j]-frame[i][j] for j in range(d)] for i in range(d)]
    pd_metric=positive(Gamma);pd_span=positive(frame);pd_physical_cap=positive(physical_cap)
    # FIRST means are RECOVERED from ORIGINAL marked and old rows, not supplied.
    old=rows[1:1+oldsize];G=total(old);K=total(rows[1:private_start]);W=combine(K,G,Q(-1))
    first=list(old);start=0
    for g,k in enumerate(counts):
        H=scale(Q(-1),total([row for A,row in enumerate(old,1) if A&(1<<g)]))
        marked=rows[1+oldsize+3*start:1+oldsize+3*(start+k)]
        Bmean=combine(scale(Q(1,3*k),total(marked)),H,Q(-1,D0))
        if g==0:
            require(not any(Bmean),'actual heavy retained B mean zero')
        else:
            first.append(Bmean)
        start+=k
    first_images=[image(v) for v in first];f=len(first)
    metric1=[[dot(u,im) for im in first_images] for u in first]
    scores=[[dot(row,im) for im in first_images] for row in rows]
    GS=[dot(G,im) for im in first_images];KS=[dot(K,im) for im in first_images]
    WS=[x-y for x,y in zip(KS,GS)]
    require(all(row==scale(Q(-1,ell),KS) for row in [scores[0]]+scores[private_start:]),
            'ALL private/ACTUAL-empty FIRST common projections')
    S1=[[sum((v[i]*v[j] for v in scores),Q(0)) for j in range(f)] for i in range(f)]
    A1=[[sum((v[i]*v[j] for v in scores[1:private_start]),Q(0))+GS[i]*GS[j]
         for j in range(f)] for i in range(f)]
    require(S1==[[A1[i][j]-GS[i]*GS[j]+KS[i]*KS[j]/ell for j in range(f)] for i in range(f)],
            'ENTIRE growing FIRST original frame identity with ACTUAL empty')
    D1=[[2*s*metric1[i][j]-A1[i][j] for j in range(f)] for i in range(f)]
    B1=[[D1[i][j]+GS[i]*GS[j] for j in range(f)] for i in range(f)]
    pd_first_metric,pd_first_D=positive(metric1),positive(D1)
    invD,invB=inverse(D1),inverse(B1)
    ge=dot(GS,apply(invD,GS));ze=dot(GS,apply(invD,WS));we=dot(WS,apply(invD,WS))
    require(ge==Q(q-1,6*h)+Q(3*h,2*q)+Q(3*F,2*q*q) and ze==Q(-m,q) and we==m,
            'ALL WHOLE original FIRST inverse energies, unequal counts retained')
    margin=ell-dot(KS,apply(invB,KS))
    require(margin==(1-ze)**2/(1+ge)>0,'EXACT positive-square original FIRST Schur margin')
    P=[[Q(i==j)-Q(1,N) for j in range(N)] for i in range(N)]
    M0=[[(Qfull[i][j]+1-s*Q(i==j))/(N-s) for j in range(N)] for i in range(N)]
    C_hash=fingerprint(C);M_hash=fingerprint(M0)
    baseline=None
    if n==4 and counts==[3,2,2,2]:
        require(C_hash=='47e30a001115f44b844c3b96f1d56aea5f275967e0951cf947759441d41fa547'
                and M_hash=='dbc032cf5347ef51b104532270d23166136897b9b4b924a73598fe0797b3bb2c',
                'ENTIRE published FOUR original core and seed reproduced')
        baseline=dict(source_commit='9e7ada1cd3b0b966815e1711c9212e94dad2881f',graph='10316/0',
            scope='original r4/n4/h3/l2 full C and seedM only; NO cap/certificate/verdict transport')
    seed_cap=[[2*s*P[i][j]-Qfull[i][j] for j in range(N)] for i in range(N)]
    require(all(sum(row,Q(0))==0 for row in seed_cap),'original seed cap ones kernel')
    pd_seed_cap=positive([row[1:] for row in seed_cap[1:]])
    # A literal original preimage pays inverse energy/negative witnesses without
    # replacing the original vertex space by a reduced pseudoinverse.
    x=preimage(proper,dual)
    require(apply(C,x)==p and dot(x,p)==kappa,'ALL original preimage rows and inverse energy')
    v=combine(x,rho,-dot(c,x))
    require(dot(c,v)==0 and dot(p,v)==kappa and apply(C,v)==p,
            'full original distant-endpoint witness equations')
    far=6/kappa
    Cfar=[[C[i][j]+far*(a[i]*b[j]+b[i]*a[j]) for j in range(N-1)] for i in range(N-1)]
    require(apply(Cfar,v)==[Q(0)]*(N-1),'ENTIRE exact original far-endpoint kernel')
    def centered(v):
        w=[Q(0)]+v;t=sum(w,Q(0))/N
        return [x-t for x in w]
    A=[Q(-3)]+a;B=[Q(-1)]+b
    aa,bb,ab=dot(A,A),dot(B,B),dot(A,B)
    require(sum(A)==sum(B)==0 and aa<=10 and bb<Q(17,12) and ab==3
            and aa*bb<16,'whole ACTUAL perturbation norm below7delta')
    repairs=[]
    for delta in (Q(1,32),Q(1,8)):
        require(0<delta*kappa<6,'selected repair inside ENTIRE lower interval')
        Qd=[[Qfull[i][j]+delta*(A[i]*B[j]+B[i]*A[j]) for j in range(N)] for i in range(N)]
        Cd=[[C[i][j]+delta*(a[i]*b[j]+b[i]*a[j]) for j in range(N-1)] for i in range(N-1)]
        degree=[sum(row,Q(0)) for row in Cd]
        lifted=[[sum(degree,Q(0))]+[-x for x in degree]]
        lifted+=[[-degree[i]]+row for i,row in enumerate(Cd)]
        require(Qd==lifted,'ENTIRE repaired ACTUAL empty/loop original lift')
        Md=[[(Qd[i][j]+1-s*Q(i==j))/(N-s) for j in range(N)] for i in range(N)]
        for i in range(N):
            require(sum(Md[i],Q(0))==1,'ALL repaired ORIGINAL stochastic row sums')
            for j in range(N):
                require(Md[i][j]==Md[j][i],'ALL repaired ORIGINAL symmetry')
                if family[i]&family[j]:
                    require(Md[i][j]==0,'ALL repaired ORIGINAL support positions')
        surplus=[[(2*s+7*delta)*P[i][j]-Qd[i][j] for j in range(N)] for i in range(N)]
        require(all(sum(row,Q(0))==0 for row in surplus),'actual repaired cap ones kernel')
        pd=positive([row[1:] for row in surplus[1:]])
        repairs.append(dict(delta=str(delta),cap_floor=str(6*L-7*delta),
            lower_rank=N-1,upper_rank=N-1,whole_original_lift_positions=N*N,
            whole_original_support_and_symmetry_positions=N*N,original_cap=pd,
            M_sha256=fingerprint(Md),proper_C_sha256=fingerprint(Cd),actual_Q_sha256=fingerprint(Qd)))
    negative=[]
    for delta,w,energy in ((Q(-1,32),centered(rho),Q(-6,32)),
                           (far+Q(1,32),centered(v),-kappa*kappa/Q(192))):
        Qd=[[Qfull[i][j]+delta*(A[i]*B[j]+B[i]*A[j])+1 for j in range(N)] for i in range(N)]
        actual=dot(w,apply(Qd,w))
        require(actual==energy<0 and sum(w)==0,'EXACT FULL ORIGINAL outside-line negative energy')
        negative.append(dict(delta=str(delta),energy=str(actual),original_witness_sha256=fingerprint(w),
                             meaning='outside this candidate lower line, not H nonexistence'))
    return dict(agent='six-downset-1',role='researcher',status='COMPLETE EXACT ORIGINAL CONTROL; generic theorem ordinary/unformalized',
        n=n,counts=counts,N=N,s=s,F=F,L=L,physical_dimension=d,FIRST_dimension=f,
        all_original_metric_and_frame_positions=2*d*d,all_original_core_positions=(N-1)**2,
        all_original_actual_lift_positions=N*N,mandatory_nonempty_positions=mandatory,
        all_first_metric_and_frame_positions=2*f*f,first_inverse_product_positions=4*f*f,
        all_first_frame_identity_positions=f*f,all_original_dual_scores=N,all_original_preimage_rows=N-1,
        kappa=str(kappa),g=str(ge),z=str(ze),w=str(we),rank_one_margin=str(margin),
        weighted_b=[str(computed[g]['mu']/SL) for g in range(1,r)],
        seed_lower_rank=N-2,seed_upper_rank=N-1,lower_interval=['0',str(far)],
        endpoint_lower_ranks=[N-2,N-2],proof_of_finite_lower_ranks='full positive physical span + ORIGINAL dual/null congruence',
        positive_forms=dict(metric=pd_metric,full_span=pd_span,full_physical_2s_cap=pd_physical_cap,
            original_2s_cap=pd_seed_cap,FIRST_metric=pd_first_metric,FIRST_D=pd_first_D),
        metric_sha256=fingerprint(Gamma),frame_sha256=fingerprint(frame),C_sha256=C_hash,M0_sha256=M_hash,
        FIRST_metric_sha256=fingerprint(metric1),FIRST_frame_sha256=fingerprint(S1),
        known_original_baseline=baseline,repairs=repairs,outside_line_original_negative_witnesses=negative,
        original_point_stars=stars,new_source_commit=None,new_graph_ref=None,formalized=False,independent_review=False)

def load(path):
    require(path.stat().st_size<=LIMIT_BYTES,'unchanged32MiB input guard')
    def no_float(value):
        raise ValueError('floating input is not an exact certificate')
    return json.loads(path.read_text(),parse_float=no_float,parse_constant=no_float)

def main():
    def expire(a,b):
        raise TimeoutError('unchanged60s original reader guard; incomplete is not nonexistence')
    signal.signal(signal.SIGALRM,expire);signal.alarm(60)
    state=os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT')
    if state:
        require(not any((Path(state)/n).exists() for n in
            ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational barrier')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();require(not args.out.exists(),'unique actual reader output')
    started=time.monotonic();result=check(load(args.input))
    result['observed_seconds']=time.monotonic()-started
    result['peak_RSS_KiB']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result['optimized']=not __debug__
    raw=json.dumps(result,indent=2).encode()+b'\n'
    require(len(raw)<=LIMIT_BYTES,'unchanged32MiB output guard')
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_bytes(raw)
    signal.alarm(0)
    print(json.dumps({k:v for k,v in result.items() if k in
        ('status','N','counts','FIRST_dimension','physical_dimension','kappa','observed_seconds','peak_RSS_KiB')}))

if __name__=='__main__':
    main()
