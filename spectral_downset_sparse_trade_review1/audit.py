#!/usr/bin/env python3
"""Independent sparse-trade audit; six-reviewer-1, reviewer, 2026-09-30.

Standard-library exact arithmetic. Uniform cores are rebuilt as orthogonal
Gram projections, not read from an entry table. PSD/rank uses fraction-free
symmetric elimination. No author/campaign module or fixture is imported.
The infinite claims require the written proof; finite checks are controls.
"""
import argparse
import hashlib
import itertools as it
import json
import math
import resource
import time
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path


def check(ok, message):
    if not ok:
        raise ValueError(message)


def vertex(points):
    return sum(1 << p for p in points)


def digest(matrix):
    return hashlib.sha256(json.dumps([[str(Q(x)) for x in row] for row in matrix],
                                    separators=(',',':')).encode()).hexdigest()


def product(a,b):
    check(not a or len(a[0])==len(b),'matrix product dimension')
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def image(a,v):
    return [sum(x*y for x,y in zip(row,v)) for row in a]


def quadratic(a,v):
    return sum(x*y for x,y in zip(v,image(a,v)))


def inverse(a):
    n=len(a)
    check(all(len(r)==n for r in a),'inverse shape')
    work=[[Q(x) for x in r]+[Q(i==j) for j in range(n)] for i,r in enumerate(a)]
    for j in range(n):
        i=next((i for i in range(j,n) if work[i][j]),None)
        check(i is not None,'singular inverse')
        work[j],work[i]=work[i],work[j]
        p=work[j][j]
        work[j]=[x/p for x in work[j]]
        for i in range(n):
            if i!=j and work[i][j]:
                c=work[i][j]
                work[i]=[x-c*y for x,y in zip(work[i],work[j])]
    result=[r[n:] for r in work]
    check(product(a,result)==[[Q(i==j) for j in range(n)] for i in range(n)],
          'inverse identity')
    return result


def psd_rank(a, operation_cap=5_000_000):
    """Integer Bareiss Schur elimination, valid under symmetric pivoting.

    After positive pivots the current block is a positive multiple of the
    Schur complement. A zero diagonal with nonzero row is indefinite.
    All divisions are required exact. Exceeding a cap raises INCOMPLETE.
    """
    n=len(a)
    check(all(len(r)==n for r in a),'PSD shape')
    check(all(a[i][j]==a[j][i] for i in range(n) for j in range(n)),'PSD symmetry')
    scale=math.lcm(*(Q(x).denominator for r in a for x in r)) if n else 1
    b=[[int(Q(x)*scale) for x in r] for r in a]
    previous=1
    rank=0
    operations=0
    for k in range(n):
        for i in range(k,n):
            check(b[i][i]>=0,'negative Schur diagonal')
            if not b[i][i]:
                check(not any(b[i][j] for j in range(k,n)),'zero diagonal nonzero row')
        p=next((i for i in range(k,n) if b[i][i]),None)
        if p is None:
            return rank
        if p!=k:
            b[k],b[p]=b[p],b[k]
            for r in b:
                r[k],r[p]=r[p],r[k]
        pivot=b[k][k]
        for i in range(k+1,n):
            for j in range(i,n):
                operations+=1
                if operations>operation_cap:
                    raise RuntimeError('INCOMPLETE integer PSD operation cap')
                value,remainder=divmod(pivot*b[i][j]-b[i][k]*b[k][j],previous)
                check(not remainder,'nonexact Bareiss division')
                b[i][j]=b[j][i]=value
        previous=pivot
        rank+=1
    return rank


def span_rank(columns):
    if not columns:
        return 0
    a=[[Q(v) for v in row] for row in zip(*columns)]
    rank=0
    for col in range(len(columns)):
        i=next((i for i in range(rank,len(a)) if a[i][col]),None)
        if i is None:
            continue
        a[rank],a[i]=a[i],a[rank]
        p=a[rank][col]
        a[rank]=[x/p for x in a[rank]]
        for j in range(rank+1,len(a)):
            if a[j][col]:
                c=a[j][col]
                a[j]=[x-c*y for x,y in zip(a[j],a[rank])]
        rank+=1
    return rank


def lift(c):
    # Explicit multiplication E C E^T; do not assume the new core is centered.
    m=len(c)
    row=[sum(r) for r in c]
    return [[Q(1)+sum(row)]+[Q(1)-x for x in row]]+[
        [Q(1)-row[i]]+[Q(1)+x for x in r] for i,r in enumerate(c)]


def upper(c):
    n=len(c)+1
    return [[Q(n*(i==j)-1)-x for j,x in enumerate(r)] for i,r in enumerate(c)]


def validate(domain,s,c):
    n=len(domain)
    check(domain[0]==0 and len(set(domain))==n,'downset domain')
    included=set(domain)
    check(all((a & ~(1<<i)) in included for a in domain
              for i in range(a.bit_length()) if a>>i&1),'downward closure')
    l=lift(c)
    check(all(sum(r)==n for r in l),'H row sums')
    check(all(l[i][j]==(s if i==j else 0) for i,a in enumerate(domain)
              for j,b in enumerate(domain) if a&b),'H supported entries')
    check(all(c[i][j]==c[j][i] for i in range(n-1) for j in range(n-1)),
          'core symmetry')
    counts=[sum(a>>i&1 for a in domain) for i in range(max(domain).bit_length())]
    check(max(counts)==s and 0<2*s<n,'actual largest star / strict density')
    stars=[i for i,v in enumerate(counts) if v==s]
    xs=[[Q(a>>i&1) for a in domain[1:]] for i in stars]
    check(all(not any(image(c,x)) for x in xs),'core largest-star equation')
    return l,stars,xs


def incidence_trade(nonempty,n):
    """Build the three incidence blocks J-I, J-R, J-R^T R+I."""
    a=(n-2)*(n-3)
    b=n-3
    answer=[]
    for x in nonempty:
        row=[]
        for y in nonempty:
            sx,sy=x.bit_count(),y.bit_count()
            common=(x&y).bit_count()
            if sx==sy==1:
                value=a*(1-int(x==y))
            elif {sx,sy}=={1,2}:
                value=-b*(1-common)
            elif sx==sy==2:
                value=1-common+int(x==y)
            else:
                value=0
            row.append(Q(value))
        answer.append(row)
    return answer


def uniform(n):
    domain=sorted([0]+[1<<i for i in range(n)]+[vertex(p) for p in it.combinations(range(n),2)],
                  key=lambda x:(x.bit_count(),x))
    rows=[[Q(1)]+[Q(a>>i&1) for i in range(n)] for a in domain[1:]]
    gram=product(list(map(list,zip(*rows))),rows)
    gi=inverse(gram)
    active=[[i for i,v in enumerate(r) if v] for r in rows]
    kappa=Q(n*(n-1),n-2)
    c=[[kappa*(Q(i==j)-sum(gi[a][b] for a in active[i] for b in active[j]))
        for j in range(len(rows))] for i in range(len(rows))]
    return domain,c,kappa


def uniform_audit(n):
    domain,c,kappa=uniform(n)
    m=len(c);q=n*(n-1)//2;N=m+1
    l,stars,xs=validate(domain,n,c)
    check(not any(map(sum,c)),'uniform centering')
    check(psd_rank(c)==q-1 and psd_rank(upper(c))==m,'uniform base ranks')
    # Check the incidence expression independently of the Gram projection.
    incidence=[]
    for a in domain[1:]:
        row=[]
        for b in domain[1:]:
            sa,sb=a.bit_count(),b.bit_count();t=(a&b).bit_count()
            if sa==sb==1:
                v=Q(n*int(a==b)-1)
            elif sa==sb==2:
                v=kappa*int(a==b)-Q(n,n-2)*t+Q(2,n-2)
            else:
                v=Q(2,n-2)-Q(n,n-2)*t
            row.append(v)
        incidence.append(row)
    check(incidence==c,'uniform Gram/incidence formula mismatch')
    d=incidence_trade(domain[1:],n)
    check(all(not any(image(d,x)) for x in xs),'trade star annihilation')
    check(sum(map(sum,d))==Q(n*(n-1)*(n-2)*(n-3),4),'trade total')
    h=[Q(1)-Q(n,2*n-1)*a.bit_count() for a in domain[1:]]
    check(not any(image(c,h)),'uniform extra kernel')
    records=[]
    if n==3:
        check(not any(any(r) for r in d),'triangle zero trade')
        return {'n':n,'N':N,'base_rank':q,'base_L_sha256':digest(l),'parameters':[]}
    cap=Q(2*(n*n+n+2),(n-2)*(n-3)*(n*n+3*n-2))
    nn=Q(2,(n-1)*(n-2)*(n-3))
    lower_end=Q(n,(n-2)*(n-3))
    author=Q(n,36*(n+1)*(n-2)**2*(n-3))
    check(0<author<nn<cap<lower_end and cap<1<=N-kappa,'uniform exact endpoint order')
    hnorm=sum(x*x for x in h)
    check(hnorm==Q(q,2*n-1),'uniform h norm')
    eig=Q((n-2)*(n-3)*(2*n-1),2)
    check(image(d,h)==[eig*x for x in h],'trivial trade eigenvalue')
    w=[Q((n-1)*(n+2) if a.bit_count()==1 else (n-2)*(n+1)) for a in domain[1:]]
    for name,e in [('author_closed',author),('nonnegative_endpoint',nn),
                   ('half_cap',cap/2),('cap_endpoint',cap)]:
        new=[[c[i][j]+e*d[i][j] for j in range(m)] for i in range(m)]
        nl,_,_=validate(domain,n,new)
        lo,up=psd_rank(new),psd_rank(upper(new))
        check(lo==q and up==m-int(e==cap),'uniform new ranks')
        offdiag=min(nl[i][j] for i in range(N) for j in range(N) if i!=j)
        check((offdiag>=0)==(e<=nn),'uniform exact off-diagonal threshold')
        if e==cap:
            check(not any(image(upper(new),w)),'uniform upper endpoint kernel')
        records.append({'parameter':name,'epsilon':str(e),'lower_L_rank':lo+1,
                        'upper_rank':up,'nonnegative_off_diagonal':offdiag>=0,
                        'L_sha256':digest(nl)})
    beyond=(cap+lower_end)/2
    new=[[c[i][j]+beyond*d[i][j] for j in range(m)] for i in range(m)]
    check(psd_rank(new)==q,'upper-only endpoint obstruction lower PSD')
    check(quadratic(upper(new),w)<0,'uniform above-cap rational obstruction')
    try:
        psd_rank(upper(new))
    except ValueError:
        pass
    else:
        raise ValueError('above-cap PSD wrongly accepted')
    lower_boundary=[[c[i][j]+lower_end*d[i][j] for j in range(m)] for i in range(m)]
    check(psd_rank(lower_boundary)==q-(n-1),'lower endpoint rank drop')
    u=[Q(1 if i==0 else -1 if i==1 else 0) for i in range(n)]
    standard=[u[a.bit_length()-1] if a.bit_count()==1 else
              -sum(u[i] for i in range(n) if a>>i&1)/(n-2) for a in domain[1:]]
    too_large=[[c[i][j]+2*lower_end*d[i][j] for j in range(m)] for i in range(m)]
    check(quadratic(too_large,standard)<0,'above-lower-endpoint rational obstruction')
    negative=[[c[i][j]-d[i][j]/(n+1) for j in range(m)] for i in range(m)]
    check(quadratic(negative,h)<0,'uniform negative-parameter obstruction')
    return {'n':n,'N':N,'base_rank':q,'base_L_sha256':digest(l),
            'epsilon_cap':str(cap),'epsilon_nonnegative':str(nn),'epsilon_lower':str(lower_end),
            'parameters':records,'lower_endpoint_core_rank':q-(n-1),
            'three_rational_endpoint_obstructions':True}


def friendship(k):
    center=1<<(2*k)
    domain=sorted([0,center]+[1<<i for i in range(2*k)]+
                  [center|(1<<i) for i in range(2*k)]+
                  [vertex((2*j,2*j+1)) for j in range(k)],key=lambda a:(a.bit_count(),a))
    def kind(a):
        if a==center:return 'a',-1
        p=next(i for i in range(2*k) if a>>i&1)
        return ('c' if a.bit_count()==1 else 'b' if a&center else 'd'),p//2
    c=[]
    for x in domain[1:]:
        tx,jx=kind(x);row=[]
        for y in domain[1:]:
            ty,jy=kind(y);types={tx,ty}
            if x==y:v=2*k
            elif tx==ty=='b' or types=={'a','b'}:v=-1
            elif 'a' in types:v=0
            elif 'b' in types:v=-1 if jx==jy else Q(1,k-1)
            elif tx==ty=='c':v=k-2 if jx==jy else -1
            elif types=={'c','d'}:v=-1
            else:v=0
            row.append(Q(v))
        c.append(row)
    return domain,c


def friendship_audit(k):
    domain,c=friendship(k);s=2*k+1;m=len(c)
    l,stars,xs=validate(domain,s,c)
    check(not any(map(sum,c)),'friendship centering')
    check(all(v>=-1 for i,r in enumerate(c) for j,v in enumerate(r) if i!=j),
          'friendship baseline nonnegative weights')
    check(psd_rank(c)==m-2 and psd_rank(upper(c))==m,'friendship base ranks')
    determinant=Q(6*k*k*(2*k+1))-Q(14*k**3,(k-1)**2)
    adjtrace=Q(16*k*k+5*k)-Q(6*k*k,(k-1)**2)
    check(determinant>0 and adjtrace>0,'friendship centered block minors')
    alpha=min(Q(k+2),Q(2*k+1),Q(3*k),determinant/adjtrace)
    epsilon=alpha/(8*m)
    check(0<epsilon<=1 and epsilon<=alpha/4 and epsilon<=Q(1,4)
          and epsilon<=alpha/(4*m),'friendship abstract trade inequalities')
    cases=[]
    for j in (1,2):
        a,b=domain[1:].index(1),domain[1:].index(1<<j)
        new=[r[:] for r in c]
        new[a][b]+=epsilon;new[b][a]+=epsilon
        nl,_,_=validate(domain,s,new)
        check(psd_rank(new)==m-1 and psd_rank(upper(new))==m,'friendship repaired ranks')
        check(all(nl[i][j]>=0 for i in range(m+1) for j in range(m+1) if i!=j),
              'friendship repaired negative off-diagonal')
        cases.append({'leaf_pair':[0,j],'lower_L_rank':m,'upper_rank':m,'L_sha256':digest(nl)})
    return {'k':k,'N':m+1,'s':s,'base_L_sha256':digest(l),'alpha':str(alpha),
            'epsilon':str(epsilon),'same_and_different_matched_pair_controls':cases}


def boundary_audit():
    records=[]
    for flag in (0,1):
        # Build directly from membership predicates, not source lists.
        triples=[vertex(c) for c in it.combinations(range(9),3)
                 if sum(p<3 for p in c)==2
                 or (all(p>=3 for p in c) and (flag or c not in [(3,4,5),(6,7,8)]))
                 or (flag and c==(0,1,2))]
        domain=sorted([0]+[1<<i for i in range(9)]+[vertex(c) for c in it.combinations(range(9),2)]+
                      triples,key=lambda a:(a.bit_count(),a))
        family=[a for a in domain if (a.bit_count()==2 and a<8)
                or (a.bit_count()==3 and (a&7).bit_count()>=2)]
        N=len(domain);s=21+flag
        check(N==82+3*flag and len(family)==s,'boundary size')
        check(all(a&b for a,b in it.combinations(family,2)),'boundary intersection')
        stars=[[Q(N*(a>>i&1)-s) for a in domain] for i in range(9)]
        empty=[Q(N*(a==0)-1) for a in domain]
        maximum=[Q(N*(a in family)-s) for a in domain]
        check(span_rank(stars+[empty])==10 and span_rank(stars+[empty,maximum])==11,
              'boundary centered kernel independence')
        d=incidence_trade(domain[1:],9)
        y=[Q(a in family) for a in domain[1:]]
        dy=image(d,y)
        check(sum(x*z for x,z in zip(y,dy))==0 and sum(z*z for z in dy)==2205,
              'boundary zero form / nonzero image')
        check(Counter(dy)==Counter({Q(-6):3,Q(-18):6,Q(0):len(triples)+3,Q(1):18,Q(3):15}),
              'boundary actual image values')
        check([sum(a>>i&1 for a in triples) for i in range(9)]==[12+flag]*9,
              'boundary degrees')
        records.append({'type':flag,'N':N,'s':s,'centered_forced_kernel_rank':11,
                        'centered_H_rank_at_most':N-11,'trade_image_squared_norm':2205,
                        'trade_quadratic_form':0,'family':family})
    return records


def controls():
    # All 729 symmetric three-by-three integer matrices with entries -1,0,1.
    # PSD iff all principal minors are nonnegative. This independently checks
    # singular, indefinite and pivot-permuted fraction-free elimination.
    tested=0;accepted=0
    for values in it.product((-1,0,1),repeat=6):
        a,b,c,d,e,f=values
        mat=[[a,b,c],[b,d,e],[c,e,f]]
        expected=(a>=0 and d>=0 and f>=0 and a*d-b*b>=0 and a*f-c*c>=0
                  and d*f-e*e>=0 and a*d*f+2*b*c*e-a*e*e-d*c*c-f*b*b>=0)
        try:rank=psd_rank(mat)
        except ValueError:got=False
        else:got=True;accepted+=1
        check(got==expected,'three-by-three PSD minor control')
        tested+=1
    # Test positive rank one and two rational Gram matrices and a forced pivot.
    for rows,want in [([[0,1],[1,2],[2,0]],2),([[Q(1,3)],[Q(-2,5)],[Q(7,11)]],1)]:
        g=product(rows,list(map(list,zip(*rows))))
        check(psd_rank(g)==want,'rational Gram rank control')
    check(psd_rank([[0,0],[0,2]])==1,'symmetric pivot control')
    rejects=0
    for f in [lambda:psd_rank([[1,0],[1,1]]),lambda:psd_rank([[1],[0,1]]),
              lambda:psd_rank([[1,0],[0,1]],operation_cap=0)]:
        try:f()
        except (ValueError,RuntimeError):rejects+=1
    check(rejects==3,'malformed or cap control accepted')
    rectangles=0
    for table in it.product((0,1),repeat=4):
        a,b,c,d=table
        if a+d==b+c:
            check((a==b and c==d) or (a==c and b==d),'additive Boolean rectangle')
            rectangles+=1
    triangle=[1,2,4,3,5,6]
    families=[list(c) for size in range(7) for c in it.combinations(triangle,size)
              if all(a&b for a,b in it.combinations(c,2))]
    maximum=max(map(len,families));ext=[c for c in families if len(c)==maximum]
    check(maximum==3 and len(ext)==4,'triangle equality exception')
    majority=[a for a in range(8) if a.bit_count()>=2]
    check(len(majority)==4 and all(a&b for a,b in it.combinations(majority,2))
          and all(set(majority)!=set(a for a in range(8) if a>>i&1) for i in range(3)),
          'half-density noncylinder')
    return {'all_symmetric_three_by_three_integer_matrices':tested,'accepted_PSD':accepted,
            'rational_Gram_and_pivot_controls':3,'malformed_or_cap_rejections':3,
            'additive_Boolean_rectangles':rectangles,'triangle_maximum_families':ext,
            'half_density_noncylinder':majority}


def run(progress=None):
    tests=controls();uniforms=[];friends=[]
    for n in range(3,11):
        uniforms.append(uniform_audit(n))
        if progress:Path(progress).write_text(json.dumps({'status':'INCOMPLETE','uniform_done':n,'friendship_done':0})+'\n')
    for k in range(2,7):
        friends.append(friendship_audit(k))
        if progress:Path(progress).write_text(json.dumps({'status':'INCOMPLETE','uniform_done':10,'friendship_done':k})+'\n')
    return {'status':'COMPLETE','agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'controls':tests,'uniform_rank_two':uniforms,'friendship':friends,
            'conditional_nine_point_boundaries':boundary_audit()}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path);p.add_argument('--check',type=Path)
    p.add_argument('--progress',type=Path);p.add_argument('--compare-author',type=Path)
    args=p.parse_args();started=time.monotonic();result=run(args.progress)
    if args.compare_author:
        source=json.loads(args.compare_author.read_text())
        rows={r['case']:r['base_H_PSD_sha256'] for r in source['cases']}
        for r in result['uniform_rank_two']:
            if r['n']>8:
                continue  # New independent cases outside the author's fixture.
            # Resolve source tag from unique n and family spelling, no proof inputs.
            names=[k for k in rows if k.startswith('uniform') and k.endswith(str(r['n']))]
            check(len(names)==1 and rows[names[0]]==r['base_L_sha256'],'author uniform base comparison')
        for r in result['friendship']:
            if r['k']<=5:
                names=[k for k in rows if k.startswith('friendship') and k.endswith(str(r['k']))]
                check(len(names)==1 and rows[names[0]]==r['base_L_sha256'],'author friendship base comparison')
    payload=json.dumps(result,sort_keys=True,separators=(',',':'))+'\n'
    if args.check:check(json.loads(payload)==json.loads(args.check.read_text()),'independent full result mismatch')
    if args.output:args.output.write_text(payload)
    print(json.dumps({'status':'COMPLETE','seconds':time.monotonic()-started,
                     'rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                     'sha256':hashlib.sha256(payload.encode()).hexdigest(),
                     'uniform_cases':len(result['uniform_rank_two']),
                     'friendship_cases':len(result['friendship'])}))


if __name__=='__main__':main()
