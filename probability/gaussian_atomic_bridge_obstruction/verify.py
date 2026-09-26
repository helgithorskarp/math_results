#!/usr/bin/env python3
"""Exact finite audits for PROOF.md. Standard-library integer/rational arithmetic.

The written proof carries the universal and continuous-motion statements.
This checker does not claim to decide Gaussian majorisation.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations, product
import json
from math import factorial
from pathlib import Path

A = ((1,0,1),(0,1,1),(-1,0,1),(0,-1,1))
B = ((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1))
X = ((0,0,0),) + A + tuple(tuple(-v for v in p) for p in B)
Y = ((0,0,0),) + A + B
K = (8,12,7,15,44,21,11,23,43)
W = tuple(F(k,sum(K)) for k in K)
MX = ((21911,-1939,4308),(-1939,27407,-13124),(4308,-13124,31984))
MY = ((22271,77,216),(77,22375,-568),(216,-568,1408))

def require(condition, message):
    if not condition:
        raise ArithmeticError(message)

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def distance(a,b):
    return sum((x-y)**2 for x,y in zip(a,b))

def rank(rows):
    a=[list(map(F,row)) for row in rows]
    r=0
    for c in range(len(a[0])):
        piv=next((i for i in range(r,len(a)) if a[i][c]),None)
        if piv is None:
            continue
        a[r],a[piv]=a[piv],a[r]
        q=a[r][c];a[r]=[x/q for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                q=a[i][c];a[i]=[x-q*y for x,y in zip(a[i],a[r])]
        r+=1
    return r

def determinant(a):
    if len(a)==1:
        return a[0][0]
    return sum((-1)**j*a[0][j]*determinant(
        [[row[k] for k in range(len(a)) if k!=j] for row in a[1:]])
        for j in range(len(a)))

def covariance_numerator(z):
    n=sum(K)
    mean=[sum(k*p[j] for k,p in zip(K,z)) for j in range(3)]
    return tuple(tuple(n*sum(k*p[i]*p[j] for k,p in zip(K,z))-mean[i]*mean[j]
        for j in range(3)) for i in range(3))

def ldl(a):
    n=len(a);l=[[F(i==j) for j in range(n)] for i in range(n)];d=[]
    for i in range(n):
        q=a[i][i]-sum(l[i][j]**2*d[j] for j in range(i))
        require(q!=0,'Zero pivot in advertised inertia certificate')
        d.append(q)
        for j in range(i+1,n):
            l[j][i]=(a[j][i]-sum(l[j][h]*l[i][h]*d[h] for h in range(i)))/q
    require(all(sum(l[i][h]*d[h]*l[j][h] for h in range(n))==a[i][j]
        for i in range(n) for j in range(n)), 'LDL reconstruction failed')
    return l,d

def paired_rank(p):
    return rank([X[i]+Y[p[i]] for i in range(9)])

def contraction(p,dx,dy):
    return all(dx[i][j]>=dy[p[i]][p[j]] for i,j in combinations(range(9),2))

def audits():
    require(sum(K)==184 and len(set(K))==9,'Weight specification failed')
    require(len(set(X))==len(set(Y))==9,'Support is not injective')
    require(all(k>0 for k in K),'Nonpositive weight')
    dx=[[distance(a,b) for b in X] for a in X]
    dy=[[distance(a,b) for b in Y] for a in Y]
    losses=Counter(dx[i][j]-dy[i][j] for i,j in combinations(range(9),2))
    require(losses=={0:28,8:8},'Distance loss mismatch')

    # Definition-level enumeration, without the geometric classification's pruning.
    maps=[p for p in permutations(range(9)) if contraction(p,dx,dy)]
    symmetries=[]
    for z in (A,B):
        symmetries.append([p for p in permutations(range(4))
            if all(distance(z[i],z[j])==distance(z[p[i]],z[p[j]])
                   for i,j in combinations(range(4),2))])
    predicted={(0,)+tuple(1+i for i in p)+tuple(5+i for i in q)
               for p,q in product(*symmetries)}
    require(set(maps)==predicted and len(maps)==64,'Bijection classification failed')
    ranks=Counter(paired_rank(p) for p in maps)
    require(ranks=={4:8,5:32,6:24},'Paired rank distribution failed')

    ident=tuple(range(9));norm=dot(W,W)
    margins={p:norm-dot(W,tuple(W[j] for j in p)) for p in maps}
    require(all(norm==sum(W[j]**2 for j in p) for p in maps),
            'Permutation mass norm failed')
    require([p for p in maps if margins[p]==0]==[ident],
            'Distinct mass matching failed')
    minimum=min(margins[p] for p in maps if p!=ident)
    witness=(0,1,2,3,4,7,6,5,8)
    require(minimum==F(1,8464) and margins[witness]==minimum,
            'Separating margin failed')
    require(paired_rank(witness)==5,'Margin witness must be liftable')
    output_radius=minimum/(F(max(K)-min(K),2*sum(K)))
    require(output_radius==F(1,851),'Approximate output bound failed')

    # Eight zero incidences determine the projection matrix up to a scalar.
    incidences=[(i,j) for i,j in product(range(4),repeat=2) if dot(A[i],B[j])==0]
    constraints=[[A[i][k]*B[j][h] for k,h in product(range(3),repeat=2)]
                 for i,j in incidences]
    identity_vector=tuple(int(i==j) for i,j in product(range(3),repeat=2))
    require(len(incidences)==8 and rank(constraints)==8,'Projection rank failed')
    require(all(dot(row,identity_vector)==0 for row in constraints),
            'Scalar projection not in nullspace')
    circuit=(1,-1,1,-1)
    require(all(sum(c*p[j] for c,p in zip(circuit,B))==0 for j in range(3)),
            'Moving circuit failed')
    gram=[[dot(b,c) for c in B[:3]] for b in B[:3]]
    require(determinant(gram)==16 and rank(A)==rank(B)==3,'Frame ranks failed')
    origin_removed=[tuple(v-u for v,u in zip(X[i]+Y[i],X[1]+Y[1]))
                    for i in range(1,9)]
    require(rank(origin_removed)==5,'Origin-free affine rank must be five')

    covariance=[]
    expected_pivots=(('6079/846400','-4015263/13981700','-1340459009/2308776225'),
                     ('1323/169280','127/12420','-1853737/2862580'))
    for z,m,t,expected,positives in zip((X,Y),(MX,MY),(F(16,25),F(13,20)),
                                      expected_pivots,(1,2)):
        require(covariance_numerator(z)==m,'Covariance numerator mismatch')
        shifted=[[F(m[i][j],sum(K)**2)-t*int(i==j) for j in range(3)]
                 for i in range(3)]
        _,d=ldl(shifted)
        require(tuple(d)==tuple(map(F,expected)),'Exact pivot mismatch')
        require(sum(v>0 for v in d)==positives,'Wrong inertia')
        integer_shift=[[t.denominator*m[i][j]-t.numerator*sum(K)**2*int(i==j)
                        for j in range(3)] for i in range(3)]
        minors=[determinant([row[:k] for row in integer_shift[:k]]) for k in (1,2,3)]
        signs=[minors[0]>0]+[minors[i]*minors[i-1]>0 for i in (1,2)]
        require(sum(signs)==positives,'Independent principal minor inertia failed')
        covariance.append(dict(matrix_numerator=m,denominator=sum(K)**2,
            threshold=str(t),ldl_pivots=list(map(str,d)),
            integer_shift_leading_minors=minors,positive_eigenvalues=positives))

    delta=F(1,4000)
    gap=F(1,100)-18*delta
    require(gap==F(11,2000)>0,'Robust eigenvalue gap failed')
    require(F(min(K),sum(K))-delta>0,'Robust positivity failed')
    require(min(abs(a-b) for a,b in combinations(W,2))-2*delta>0,
            'Robust distinctness failed')

    # Boundary and invalid controls: the distinct-mass assumption matters.
    fold=(0,1,2,3,4,7,8,5,6)
    require(fold in maps and paired_rank(fold)==4,'Balanced fold control failed')
    uniform=(F(1,9),)*9
    require(dot(uniform,uniform)-dot(uniform,tuple(uniform[j] for j in fold))==0,
            'Repeated-weight control failed')
    bad=(1,0,2,3,4,5,6,7,8)
    require(not contraction(bad,dx,dy),'Noncontraction accepted')
    rejected=False
    try:
        ldl([[F(0),F(1)],[F(1),F(0)]])
    except ArithmeticError:
        rejected=True
    require(rejected,'Zero-pivot certificate not rejected')
    return dict(status='ATOMIC_BRIDGE_OBSTRUCTION_EXACT_AUDITS_PASS',
        weights={'numerators':K,'denominator':sum(K)},pair_losses=dict(sorted(losses.items())),
        permutations_examined=factorial(9),bijective_contractions=len(maps),
        paired_rank_distribution=dict(sorted(ranks.items())),
        minimum_nonidentity_mass_margin=str(minimum),margin_witness=witness,
        approximate_output_l1_bound=str(output_radius),
        projection_constraint_rank=rank(constraints),moving_gram_minor=determinant(gram),
        origin_removed_affine_rank=rank(origin_removed),covariance_certificates=covariance,
        weight_l1_radius=str(delta),robust_middle_eigenvalue_gap=str(gap),
        controls={'balanced_rank_four_fold':True,'noncontraction_rejected':True,
                  'zero_pivot_rejected':True})

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    result=audits()
    encoded=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.check:
        expected=Path(__file__).with_name('EXPECTED.json').read_text()
        require(json.loads(encoded)==json.loads(expected),'Expected output mismatch')
        print(result['status'])
    else:
        print(encoded,end='')

if __name__=='__main__':
    main()
