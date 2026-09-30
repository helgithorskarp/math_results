#!/usr/bin/env python3
"""Definition-level twofold-design audit; no researcher code or CAS import.

The centered matrix is built by the full incidence Gram factorization,
then every entry is checked by literal intersections and completion counts.
All PSD checks use the complete matrices, with no affine compression.
"""
import argparse
import hashlib
import itertools as it
import json
import math
import random
import sys
from fractions import Fraction as Q
from pathlib import Path
from algebra import require, certificates


def product(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def transpose(a):
    return list(map(list, zip(*a)))


def psd_rank(a, cap=5_000_000):
    """Exact integer Bareiss Schur rank with symmetric positive pivoting.

    Adapted from this reviewer's earlier independent linear.py. A zero
    diagonal with a nonzero residual row is rejected. Every division is
    checked. Reaching an operation cap raises INCOMPLETE, never a verdict.
    """
    n = len(a)
    require(all(len(r)==n for r in a), 'matrix dimensions')
    require(all(a[i][j]==a[j][i] for i in range(n) for j in range(n)), 'symmetry')
    scale = math.lcm(*(Q(x).denominator for row in a for x in row)) if n else 1
    work = [[int(Q(x)*scale) for x in row] for row in a]
    last = 1; rank = 0; operations = 0
    for k in range(n):
        for i in range(k, n):
            require(work[i][i]>=0, 'negative Schur diagonal')
            if not work[i][i]:
                require(not any(work[i][j] for j in range(k, n)), 'zero diagonal nonzero row')
        p = next((i for i in range(k, n) if work[i][i]), None)
        if p is None:
            return rank
        if p != k:
            work[p], work[k] = work[k], work[p]
            for row in work:
                row[p], row[k] = row[k], row[p]
        pivot = work[k][k]
        for i in range(k+1, n):
            for j in range(i, n):
                operations += 1
                if operations > cap:
                    raise RuntimeError('INCOMPLETE: exact PSD operation cap')
                value, rem = divmod(pivot*work[i][j]-work[i][k]*work[k][j], last)
                require(not rem, 'nonexact Bareiss division')
                work[i][j] = work[j][i] = value
        rank += 1; last = pivot
    return rank


def determinant(a):
    # Small permutation expansion is independent of the elimination code.
    n = len(a); total = 0
    for p in it.permutations(range(n)):
        inversions = sum(p[i]>p[j] for i in range(n) for j in range(i+1, n))
        total += (-1)**inversions * math.prod(a[i][p[i]] for i in range(n))
    return total


def controls():
    count = 0
    for vals in it.product((-1, 0, 1), repeat=6):
        a,b,c,d,e,f = vals; matrix = [[a,b,c],[b,d,e],[c,e,f]]
        truth = all(determinant([[matrix[i][j] for j in subset] for i in subset])>=0
                    for k in (1,2,3) for subset in it.combinations(range(3), k))
        try:
            psd_rank(matrix); actual = True
        except ValueError:
            actual = False
        require(truth==actual, 'independent principal-minor control')
        count += 1
    for matrix in [[[0,1],[1,0]], [[1,2],[2,1]], [[1,1],[0,1]]]:
        rejects(lambda: psd_rank(matrix))
    return count


def rejects(call):
    try:
        call()
    except ValueError:
        return
    raise ValueError('damaged input accepted')


def design(v, blocks):
    require(type(v) is int and v>=13, 'order at least thirteen')
    require(all(isinstance(a,tuple) and len(a)==3 and
                all(type(x) is int and 0<=x<v for x in a) and
                tuple(sorted(set(a)))==a for a in blocks), 'simple ordered triples')
    require(len(blocks)==len(set(blocks)), 'duplicate triples')
    pairs = list(it.combinations(range(v), 2))
    third = {p:[] for p in pairs}
    for a in blocks:
        for p in it.combinations(a, 2):
            third[p].append(next(x for x in a if x not in p))
    require(all(len(xs)==2 and len(set(xs))==2 for xs in third.values()), 'pair degree two')
    completion = [tuple(sorted(third[p])) for p in pairs]
    P = [[int(x in p) for p in pairs] for x in range(v)]
    C = [[int(x in q) for q in completion] for x in range(v)]
    B = [[int(x in a) for a in blocks] for x in range(v)]
    H = [[sum(x in third[p] for p in it.combinations(a, 2)) if x not in a else 0
          for a in blocks] for x in range(v)]
    R = [[int(set(p)<=set(a)) for a in blocks] for p in pairs]
    counts = {p:completion.count(p) for p in pairs}
    Z = [[counts[tuple(sorted((x,y)))]-1 if x!=y else 0 for y in range(v)] for x in range(v)]
    require(len(blocks)==v*(v-1)//3, 'block count')
    for matrix, column_sum in [(P,2),(C,2),(B,3),(H,3)]:
        require(all(sum(row)==v-1 for row in matrix), 'incidence row sums')
        require(all(sum(col)==column_sum for col in zip(*matrix)), 'incidence column sums')
    require(all(sum(row)==2 for row in R) and all(sum(col)==3 for col in zip(*R)), 'R regularity')
    require(all(sum(row)==0 for row in Z), 'Z row sums')
    grams = [
        (P,P,lambda i,j:(v-2)*(i==j)+1),
        (B,B,lambda i,j:(v-3)*(i==j)+2),
        (C,C,lambda i,j:(v-2)*(i==j)+1+Z[i][j]),
        (P,C,lambda i,j:2*(i!=j)),
        (C,P,lambda i,j:2*(i!=j)),
        (B,H,lambda i,j:3*(i!=j)+Z[i][j]),
        (H,B,lambda i,j:3*(i!=j)+Z[i][j]),
    ]
    for left,right,value in grams:
        require(product(left,transpose(right))==[[value(i,j) for j in range(v)] for i in range(v)], 'incidence Gram')
    require(product(P,R)==[[2*x for x in row] for row in B], 'PR=2B')
    require(product(C,R)==[[B[i][j]+H[i][j] for j in range(len(blocks))] for i in range(v)], 'CR=B+H')
    require(product(R,transpose(B))==[[2*P[x][i]+C[x][i] for x in range(v)] for i in range(len(pairs))], 'RBt=2Pt+Ct')
    return pairs,completion,P,B,R,H,Z


def matrix(v, blocks):
    pairs,completion,P,B,R,H,Z = design(v, blocks)
    m = len(pairs); b = len(blocks); n = 1+v+m+b; s = 2*v-1
    c = 1+Q(4,3*(v-2)*(v-3)); d = Q(v*v-v-4,(v-3)*(v-4)); t = Q(v-1,v-4)
    a = Q(-2,3); w = 1+Q(4*v*(2*v-5),3*(v-2)*(v-3)*(v-4)); h = Q(v*v-7,(v-3)*(v-4))
    pp = product(transpose(P),P); pb = product(transpose(P),B)
    bb = product(transpose(B),B); rr = product(transpose(R),R)
    K22 = [[(s+c)*(i==j)-c*pp[i][j]+c-1 for j in range(m)] for i in range(m)]
    K23 = [[d*R[i][j]-d*pb[i][j]+d-1 for j in range(b)] for i in range(m)]
    K33 = [[(s-t)*(i==j)+t*rr[i][j]-t*bb[i][j]+t-1 for j in range(b)] for i in range(b)]
    K = [K22[i]+K23[i] for i in range(m)] + [list(row)+K33[j] for j,row in enumerate(zip(*K23))]
    T = [P[i]+B[i] for i in range(v)]; TK = product(T,K); TKT = product(TK,transpose(T))
    L = [TKT[i]+[-x for x in TK[i]] for i in range(v)]
    L += [[-TK[j][i] for j in range(v)]+K[i] for i in range(m+b)]
    centered = [[Q(1)]*n] + [[Q(1)]+[1+x for x in row] for row in L]
    family = [()] + [(x,) for x in range(v)] + pairs + list(blocks)
    require(n==(5*v*v+v+6)//6, 'N formula')
    blockset = set(blocks)
    for i,A in enumerate(family):
        for j,B0 in enumerate(family):
            if not A or not B0: literal = Q(1)
            elif i==j: literal = Q(s)
            elif set(A)&set(B0): literal = Q(0)
            else:
                X,Y = (A,B0) if len(A)<=len(B0) else (B0,A)
                sizes = len(X),len(Y)
                if sizes==(1,1): literal = a+t*Z[X[0]][Y[0]]
                elif sizes==(1,2): literal = w-d*int(tuple(sorted(X+Y)) in blockset)
                elif sizes==(1,3): literal = h-t*H[X[0]][blocks.index(Y)]
                elif sizes==(2,2): literal = c
                elif sizes==(2,3): literal = d
                else: literal = t
            require(centered[i][j]==literal, 'factor/literal entry mismatch')
    return family,centered,{'distinct_completion_pairs':len(set(completion)),
                           'total_pairs':m,'outside_multiplicities':sorted({x for row in H for x in row})}


def trade(v, family):
    m = v*(v-1)//2; k = (v-2)*(v-3)//2
    result = []
    for A in family:
        row = []
        for B in family:
            if set(A)&set(B): e = 0
            elif not A and not B: e = m*k
            elif not A or not B:
                sizes = len(A)+len(B)
                e = -(v-1)*k if sizes==1 else k if sizes==2 else 0
            else:
                sizes = tuple(sorted((len(A),len(B))))
                e = 2*k if sizes==(1,1) else -(v-3) if sizes==(1,2) else 1 if sizes==(2,2) else 0
            row.append(e)
        result.append(row)
    require(all(sum(row)==0 for row in result), 'trade rows')
    require(max(sum(abs(x) for x in row) for row in result)==4*m*k, 'trade absolute row norm')
    for x in range(v):
        columns = [j for j,A in enumerate(family) if x in A]
        require(all(sum(row[j] for j in columns)==0 for row in result), 'trade stars')
    return result


def definition(v, family, matrix0):
    n = len(family); s = 2*v-1
    require(all(sum(row)==n for row in matrix0), 'full row sums')
    require(all(matrix0[i][j]==(s if i==j else 0) for i,A in enumerate(family)
                for j,B in enumerate(family) if set(A)&set(B)), 'H support/diagonal')
    for x in range(v):
        columns = [j for j,A in enumerate(family) if x in A]
        require(len(columns)==s, 'star size')
        require(all(sum(row[j] for j in columns)==s for row in matrix0), 'full star identities')


def matrix_hash(family, matrix0):
    order = sorted(range(len(family)),key=lambda i:(len(family[i]),sum(1<<x for x in family[i])))
    data = [[str(matrix0[i][j]) for j in order] for i in order]
    return hashlib.sha256(json.dumps(data,separators=(',',':')).encode()).hexdigest()


def field13():
    return sorted({tuple(sorted((x,(x+d)%13,(x+4*d)%13))) for x in range(13) for d in range(1,13)})


def field16():
    def times(a,b):
        # Direct polynomial product followed by long division by X4+X+1.
        poly = 0
        for i in range(4):
            for j in range(4):
                if a>>i&1 and b>>j&1: poly ^= 1<<(i+j)
        for i in range(6,3,-1):
            if poly>>i&1: poly ^= 0b10011<<(i-4)
        return poly
    require(all({times(a,b) for b in range(16)}==set(range(16)) for a in range(1,16)), 'field multiplication')
    roots = [r for r in range(16) if times(r,r)^r^1==0]
    require(roots==[6,7], 'field roots')
    sets = [{tuple(sorted((x,x^d,x^times(r,d)))) for x in range(16) for d in range(1,16)} for r in roots]
    require(sets[0]==sets[1], 'two roots same unordered system')
    return sorted(sets[0])


def nonbijective13():
    # A cyclic STS(13), independently permuted; no author fixture imported.
    first = {tuple(sorted((x,(x+i)%13,(x+j)%13))) for x in range(13) for i,j in [(1,4),(2,7)]}
    counts = {p:sum(set(p)<=set(a) for a in first) for p in it.combinations(range(13),2)}
    require(len(first)==26 and all(x==1 for x in counts.values()), 'cyclic STS baseline')
    rng = random.Random(2713)
    for attempt in range(1000):
        perm = list(range(13)); rng.shuffle(perm)
        second = {tuple(sorted(perm[x] for x in a)) for a in first}
        if not first&second:
            blocks = sorted(first|second)
            data = design(13,blocks)
            if len(set(data[1]))<78:
                return blocks,perm,attempt+1
    raise RuntimeError('INCOMPLETE: bounded fixture generator')


def audit(v, blocks, label):
    family,qc,info = matrix(v,blocks); n = len(family); m = v*(v-1)//2; k = (v-2)*(v-3)//2
    E = trade(v,family); oldgap = Q(n-7*v); newgap = n-Q(28*v,5)
    eta0 = oldgap/(8*m*k); eta1 = newgap/(8*m*k)
    definition(v,family,qc)
    if label=='independent_nonbijective13':
        pairs,completion,P,B,R,H,Z = design(v,blocks)
        damaged = [row[:] for row in qc]
        for x in range(v):
            for y in range(v):
                damaged[1+x][1+y] -= Q(v-1,v-4)*Z[x][y]
        rejects(lambda: definition(v,family,damaged))
    if label=='binary_field16':
        pairs,completion,P,B,R,H,Z = design(v,blocks)
        damaged = [row[:] for row in qc]
        for x in range(v):
            for j,A in enumerate(blocks):
                if H[x][j]>1:
                    index = 1+v+len(pairs)+j
                    damaged[1+x][index] = damaged[index][1+x] = qc[1+x][index]+Q(v-1,v-4)*(H[x][j]-1)
        rejects(lambda: definition(v,family,damaged))
    require(psd_rank(qc)==n-v-1, 'centered full lower rank')
    upper = [[n*(i==j)-qc[i][j]-newgap*((i==j)-Q(1,n)) for j in range(n)] for i in range(n)]
    require(psd_rank(upper)==n-1, 'stronger centered full upper buffer')
    variants = {}
    for name,eta in [('published',eta0),('larger_endpoint',eta1)]:
        qr = [[qc[i][j]+eta*E[i][j] for j in range(n)] for i in range(n)]
        definition(v,family,qr)
        require(psd_rank(qr)==n-v, 'repaired full lower rank')
        gap = newgap-eta*4*m*k
        upper = [[n*(i==j)-qr[i][j]-gap*((i==j)-Q(1,n)) for j in range(n)] for i in range(n)]
        require(psd_rank(upper)==n-1, 'repaired full upper buffer')
        variants[name] = {'eta':str(eta),'upper_buffer':str(gap),'lower_rank':n-v,'buffered_upper_rank':n-1,
                          'canonical_matrix_sha256':matrix_hash(family,qr)}
    print('completed '+label, file=sys.stderr, flush=True)
    return {'label':label,'v':v,'N':n,'s':2*v-1,'blocks':len(blocks),**info,
            'centered_lower_rank':n-v-1,'centered_buffered_upper_rank':n-1,
            'old_gap':str(oldgap),'stronger_gap':str(newgap),'eta_ratio':str(eta1/eta0),
            'centered_canonical_matrix_sha256':matrix_hash(family,qc),'variants':variants}


def run():
    signs = certificates(); small = controls(); blocks13 = field13(); fixture,perm,attempts = nonbijective13()
    rejects(lambda: design(13,blocks13[:-1]))
    rejects(lambda: design(13,blocks13+[blocks13[0]]))
    bad = blocks13[:];bad[0] = (0,0,1);rejects(lambda: design(13,bad))
    rejects(lambda: design(13.0,blocks13))
    rejects(lambda: design(12,blocks13))
    rows = [audit(13,blocks13,'field13'),audit(13,fixture,'independent_nonbijective13'),audit(16,field16(),'binary_field16')]
    require(rows[1]['distinct_completion_pairs']<78, 'nonbijective control')
    require(rows[2]['outside_multiplicities']==[0,3], 'repeated outside multiplicity control')
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer','arithmetic':'CPython integer/Fraction only',
            'universal_algebra':signs,'principal_minor_control_matrices':small,'negative_controls':10,
            'independent_nonbijective_fixture':{'permutation':perm,'attempts':attempts},
            'full_matrix_PSD_rank_checks':18,'instances':rows}


def main():
    p = argparse.ArgumentParser();p.add_argument('--check',type=Path);args = p.parse_args()
    result = run()
    if args.check:
        require(result==json.loads(args.check.read_text()), 'complete expected output mismatch')
    print(json.dumps(result,sort_keys=True,separators=(',',':')))


if __name__=='__main__':
    main()
