#!/usr/bin/env python3
"""Independent nine-point nonstar audit; six-reviewer-1, reviewer.

Decode disjoint-pair orbit data by block-count canonical signatures, without
permutation-orbit traversal. Verify exact matrices with integer congruence,
and exhaust all 512 singleton coefficient patterns for Boolean kernel vectors.
No author module or solver is imported. An incomplete guard is an exception.
"""
import argparse
import copy
import hashlib
import itertools as it
import json
import math
import resource
import time
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


def domain(flag):
    # Membership predicates over all masks; no author set lists are used.
    members=[];family=[]
    for a in range(512):
        k=(a&7).bit_count();b=(a>>3).bit_count();size=k+b
        include=(size<=2 or (size==3 and k==2) or
                 (size==3 and k==0 and (flag or a not in (56,448))) or
                 (flag and a==7))
        if include:
            members.append(a)
            if (size==2 and k==2) or (size==3 and k>=2):
                family.append(a)
    return members,family


def signature(a,b,flag):
    masks=(7,504) if flag else (7,56,448)
    ca=tuple((a&m).bit_count() for m in masks)
    cb=tuple((b&m).bit_count() for m in masks)
    signatures=[ca+cb,cb+ca]
    if not flag:
        sa=(ca[0],ca[2],ca[1]);sb=(cb[0],cb[2],cb[1])
        signatures.extend((sa+sb,sb+sa))
    return min(signatures)


def decode(case):
    flag=case['inside_triple_present']
    check(type(flag) is bool,'non-Boolean case flag')
    members,family=domain(flag);s=21+flag
    check(case['N']==len(members)==82+3*flag and case['s']==s,'case metadata')
    allowed={(a,b) for a,b in it.combinations(members[1:],2) if not a&b}
    table={};counts={}
    reps,values=case['orbit_representatives'],case['orbit_values']
    check(len(reps)==len(values),'unequal orbit table lengths')
    for rep,value in zip(reps,values):
        check(isinstance(rep,list) and len(rep)==2 and
              all(type(x) is int for x in rep) and tuple(rep) in allowed,
              'malformed disjoint-pair representative')
        key=signature(*rep,flag)
        check(key not in table,'duplicate block signature')
        check(type(value) is str,'rational value must be a string')
        table[key]=Q(value);counts[key]=0
    entries={}
    for a,b in allowed:
        key=signature(a,b,flag)
        check(key in table,'missing block signature')
        counts[key]+=1;entries[a,b]=table[key]
    check(all(counts.values()),'unused signature')
    check(len(table)==(28 if flag else 44) and len(allowed)==(1695 if flag else 1593),
          'orbit/domain coverage mismatch')
    c=[[Q(s-1) if a==b else Q(-1) if a&b else entries[tuple(sorted((a,b)))]
        for b in members[1:]] for a in members[1:]]
    return members,family,s,c,[(list(k),counts[k]) for k in sorted(counts)]


def lift(c):
    row_sums=[sum(r) for r in c]
    return [[Q(1)+sum(row_sums)]+[Q(1)-x for x in row_sums]]+[
        [Q(1)-row_sums[i]]+[Q(1)+x for x in r] for i,r in enumerate(c)]


def matrix_gap(matrix,projector):
    # Only the successful exact PSD inequality is claimed. A failed candidate
    # threshold says nothing about feasibility of the original H problem.
    rejected=0
    for exponent in range(11):
        gap=Q(1,2**exponent)
        shifted=[[matrix[i][j]-gap*projector[i][j] for j in range(len(matrix))]
                 for i in range(len(matrix))]
        try:rank=psd_rank(shifted)
        except ValueError:rejected+=1
        else:return gap,rank,rejected
    raise RuntimeError('INCOMPLETE bounded exact gap recovery')


def audit(case):
    members,family,s,c,orbits=decode(case)
    n=len(members);m=n-1;flag=case['inside_triple_present'];l=lift(c)
    present=set(members)
    check(all(a^(1<<i) in present for a in members for i in range(9) if a>>i&1),
          'downward closure')
    check(len(family)==s and all(a&b for a,b in it.combinations(family,2)),
          'nonstar maximum-family premise')
    check(not any(all(a>>i&1 for a in family) for i in range(9)),'nonstar common point')
    xs=[[Q(a>>i&1) for a in members[1:]] for i in range(9)]
    y=[Q(a in family) for a in members[1:]]
    check([sum(x) for x in xs]==[s]*9,'actual largest-star counts')
    basis=xs+[y]
    check(span_rank(basis)==10 and all(not any(image(c,x)) for x in basis),
          'ten complete forced core kernels')
    check(all(sum(r)==n for r in l),'row normalization')
    check(all(l[i][j]==(s if i==j else 0) for i,a in enumerate(members)
              for j,b in enumerate(members) if a&b),'supported core lift')
    rank=psd_rank(c);check(rank==m-10,'lower PSD rank')
    u=[[Q(n*(i==j)-1)-c[i][j] for j in range(m)] for i in range(m)]
    check(psd_rank(u)==m,'upper PSD rank')
    M=[[(l[i][j]-s*(i==j))/(n-s) for j in range(n)] for i in range(n)]
    check(all(sum(r)==1 for r in M),'row-one M')
    check(all(M[i][j]==0 for i,a in enumerate(members) for j,b in enumerate(members) if a&b),
          'supported M')
    # Rational projector onto the complement of all ten forced core kernels.
    rows=list(map(list,zip(*basis)));g=product(basis,rows);gi=inverse(g)
    active=[[i for i,v in enumerate(r) if v] for r in rows]
    projector=[[Q(i==j)-sum(gi[a][b] for a in active[i] for b in active[j])
                for j in range(m)] for i in range(m)]
    check(product(projector,projector)==projector and
          all(not any(image(projector,x)) for x in basis),'exact lower projector')
    alpha,_,lower_rejections=matrix_gap(c,projector)
    metric=[[Q(i==j)-Q(1,n) for j in range(m)] for i in range(m)]
    gamma,_,upper_rejections=matrix_gap(u,metric)
    patterns=[]
    for selected in range(512):
        coefficient=1-selected.bit_count()
        values=[(a&selected).bit_count()+coefficient*(a in family) for a in members]
        if not all(v in (0,1) for v in values):continue
        support=[a for a,v in zip(members,values) if v]
        check(values[0]==0 and len(support)==s,'Boolean affine-kernel normalization')
        centered=[Q(n*v-s) for v in values]
        check(not any(image(l,centered)),'Boolean kernel image')
        intersecting=all(a&b for a,b in it.combinations(support,2))
        patterns.append({'singleton_pattern':selected,'nonstar_coefficient':coefficient,
                         'intersecting':intersecting,'family':support})
    check(len(patterns)==14 and sum(p['intersecting'] for p in patterns)==10,
          'complete Boolean kernel classification')
    expected_patterns={0}|{1<<i for i in range(9)}|{3,5,6,7}
    check({p['singleton_pattern'] for p in patterns}==expected_patterns,
          'unexpected singleton coefficient pattern')
    # The nonintersecting K-singleton/K-B-pair family is already forced by
    # 1_T=sum_{i in K}1_star_i-2*1_I; it creates no extra rank obstruction.
    T=[a for a in members if (a&7).bit_count()==1 and a.bit_count()<=2 or (flag and a==7)]
    check(T==next(p['family'] for p in patterns if p['singleton_pattern']==7),
          'explicit auxiliary family')
    indices=[members.index(a) for a in T]
    check(sum(M[i][j] for i in indices for j in indices)==0,'auxiliary signed sum')
    positive=sum(M[i][j] for i in indices for j in indices if M[i][j]>0)
    negative=sum(M[i][j] for i in indices for j in indices if M[i][j]<0)
    check(positive==-negative>0,'auxiliary cancellation witness')
    return {'N':n,'s':s,'inside_triple_present':flag,'orbits':orbits,
            'disjoint_nonempty_pairs':sum(v for _,v in orbits),
            'core_rank':rank,'full_L_rank':rank+1,'upper_core_rank':m,
            'core_sha256':digest(c),'L_sha256':digest(l),'M_sha256':digest(M),
            'M_empty_diagonal':str(M[0][0]),
            'minimum_offdiagonal_M_entry':str(min(M[i][j] for i in range(n) for j in range(i+1,n))),
            'C_positive_gap':str(alpha),'full_upper_slack_gap':str(gamma),
            'M_unit_endpoint_gap':str(gamma/(n-s)),
            'lower_gap_candidates_rejected':lower_rejections,
            'upper_gap_candidates_rejected':upper_rejections,
            'Boolean_kernel_patterns':patterns,
            'auxiliary_T_positive_mass':str(positive),'auxiliary_T_negative_mass':str(negative)}


def fixture_controls(cases):
    rejected=0
    bad=copy.deepcopy(cases[0]);bad['orbit_values'][0]=str(Q(bad['orbit_values'][0])+1)
    for damaged in [bad]:
        try:audit(damaged)
        except ValueError:rejected+=1
        else:raise ValueError('damaged matrix accepted')
    for mode in ('duplicate','omission','unsupported','nonBoolean'):
        bad=copy.deepcopy(cases[0])
        if mode=='duplicate':
            bad['orbit_representatives'].append(bad['orbit_representatives'][0]);bad['orbit_values'].append(bad['orbit_values'][0])
        elif mode=='omission':
            bad['orbit_representatives'].pop();bad['orbit_values'].pop()
        elif mode=='unsupported':bad['orbit_representatives'][0]=[1,3]
        else:bad['inside_triple_present']=1
        try:decode(bad)
        except (ValueError,KeyError):rejected+=1
        else:raise ValueError('damaged orbit decoder accepted')
    check(rejected==5,'fixture rejection count')
    return rejected


def product_constants():
    r0,r1=Q(21,61),Q(22,63)
    delta=r1-r0;q=Q(62,63)
    check(delta==Q(19,3843) and 0<r0<r1<q<1,'density endpoint separation')
    check(Q(1,126)>delta and r0*(1-q)>delta,
          'all remaining product eigenvalues separated more strongly')
    check(Q(1,61)>=Q(1,63) and q>=Q(60,61),'unit gap arithmetic')
    return {'uniform_unit_gap':'1/63','uniform_lower_endpoint_gap':str(delta),
            'mixed_lower_gap_is_sharp':True,
            'individual_nonlower_gap_lower_bound':'1/126',
            'nontrivial_other_factor_lower_gap':str(r0*(1-q)),
            'intersecting_family_kernel_distance_squared_per_deficit':str(r1/delta)}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--fixture',type=Path,default=Path(__file__).with_name('certificates.json'))
    p.add_argument('--output',type=Path);p.add_argument('--check',type=Path)
    p.add_argument('--compare-author',type=Path)
    args=p.parse_args();started=time.monotonic();raw=args.fixture.read_bytes()
    fixture=json.loads(raw);cases=fixture['cases']
    check(len(cases)==2 and [c['inside_triple_present'] for c in cases]==[False,True],
          'two-case input coverage')
    result={'status':'COMPLETE','agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'fixture_sha256':hashlib.sha256(raw).hexdigest(),'PSD_controls':controls(),
            'cases':[audit(c) for c in cases],'fixture_rejections':fixture_controls(cases),
            'product_gap_arithmetic':product_constants()}
    if args.compare_author:
        old=json.loads(args.compare_author.read_text())['cases']
        check(len(old)==2,'author bridge case coverage')
        fields=['N','s','core_rank','full_L_rank','upper_core_rank','core_sha256','L_sha256',
                'M_sha256','M_empty_diagonal','minimum_offdiagonal_M_entry','disjoint_nonempty_pairs']
        check(all(a[k]==b[k] for a,b in zip(result['cases'],old) for k in fields),
              'author all-entry hash/metadata bridge')
    payload=json.dumps(result,sort_keys=True,separators=(',',':'))+'\n'
    if args.check:check(json.loads(payload)==json.loads(args.check.read_text()),'expected-result mismatch')
    if args.output:args.output.write_text(payload)
    print(json.dumps({'status':'COMPLETE','sha256':hashlib.sha256(payload.encode()).hexdigest(),
                     'seconds':time.monotonic()-started,'rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                     'cases':[(c['N'],c['C_positive_gap'],c['full_upper_slack_gap'],
                               len(c['Boolean_kernel_patterns'])) for c in result['cases']]}))


if __name__=='__main__':main()
