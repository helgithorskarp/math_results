#!/usr/bin/env python3
"""six-reviewer-3: exact independent stable uniform H audit and larger interval."""
import argparse
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, lcm
from pathlib import Path
import hashlib
import json


class Failure(Exception):
    pass


def need(ok, message):
    if not ok:
        raise Failure(message)


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def psd_rank(matrix):
    n = len(matrix)
    need(all(len(row) == n for row in matrix), 'square matrix')
    need(all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n)), 'symmetric matrix')
    a = [[Q(x) for x in row] for row in matrix]
    rank = 0
    for k in range(n):
        d = a[k][k]
        need(d >= 0, 'negative Schur pivot')
        if not d:
            need(all(a[k][j] == 0 for j in range(k+1,n)), 'nonzero zero-pivot row')
            continue
        rank += 1
        for i in range(k+1,n):
            for j in range(i,n):
                a[i][j] -= a[i][k] * a[k][j] / d
                a[j][i] = a[i][j]
    return rank


def row_rank(rows):
    basis = {}
    for source in rows:
        row = {i: Q(x) for i,x in enumerate(source) if x}
        while row:
            p = min(row)
            if p not in basis:
                d = row[p]
                basis[p] = {i:x/d for i,x in row.items()}
                break
            d = row[p]
            for i,x in basis[p].items():
                value = row.get(i,0) - d*x
                if value:
                    row[i] = value
                else:
                    row.pop(i,None)
    return len(basis)


def data(n,r):
    need(r >= 2 and n >= 2*r, 'stable uniform parameters')
    N = sum(choose(n,k) for k in range(r+1))
    s = sum(choose(n-1,k) for k in range(r))
    gamma = {(a,b):choose(n-a-1,b-1) for a in range(1,r+1) for b in range(1,r+1)}
    Gmax = choose(n-2,r-1)
    alpha = Q(r,Gmax)
    row_bounds = [sum(Q(n-a) * gamma[a,b] * (Q(1,a)+Q(1,b)) for b in range(1,r+1) if b!=a) for a in range(1,r+1)]
    B = max(row_bounds)
    positive = [Q(n*s,r)]
    zero_multiplicity = 1
    for j in range(1,r+1):
        dimension = choose(n,j)-choose(n,j-1)
        for a in range(j,r+1):
            ratio = Q(choose(n-a-j,a-j),gamma[a,a])
            value = s * (1 + (-1)**j * ratio)
            if value:
                need(value > 0, 'positive baseline sector')
                positive.append(value)
            else:
                zero_multiplicity += dimension
    g = min(positive)
    T = min(Q(1,2*B), alpha*g/(4*B*B))
    old = Q(1,8*N**6)
    need(0 < alpha <= 1 <= B and g >= 1, 'gap/norm normalization')
    need(T >= 4*N*old and T <= Q(1,2), 'interval improvement and positivity')
    need(T*B <= Q(1,2) and g-T*B >= 3*g/4, 'positive lower block')
    need(alpha-T*B*B/(g-T*B) >= 2*alpha/3, 'positive Schur margin')
    expected_zero = 1+r*(n-1)+(sum(choose(n,j)-choose(n,j-1) for j in range(3,r+1,2)) if n==2*r else 0)
    need(zero_multiplicity == expected_zero, 'all baseline zeros, including odd boundary')
    return {'n':n,'r':r,'N':N,'s':s,'gamma':gamma,'Gmax':Gmax,'alpha':alpha,'B':B,'row_bounds':row_bounds,'g':g,'T':T,'old':old,'baseline_nullity':zero_multiplicity}


def betas(d,t):
    r,s,gamma = d['r'],d['s'],d['gamma']
    return {(a,b):t if a!=b else (s-t*sum(gamma[a,c] for c in range(1,r+1) if c!=a))/gamma[a,a] for a in range(1,r+1) for b in range(1,r+1)}


def compressed(d,t):
    n,r,s = d['n'],d['r'],d['s']
    beta = betas(d,t)
    ranks = []
    for j in range(r+1):
        levels = list(range(max(1,j),r+1))
        G = [choose(n-2*j,a-j) for a in levels]
        need(all(x>0 for x in G),'positive harmonic metrics')
        matrix = [[G[i]*(s*int(a==b)+(-1)**j*beta[a,b]*choose(n-a-j,b-j)-int(j==0)*choose(n,b)) for b in levels] for i,a in enumerate(levels)]
        actual = psd_rank(matrix)
        if not t:
            expected = len(levels)-1 if j==0 else (0 if j==1 else len(levels)-int(n==2*r and j%2==1))
        else:
            expected = len(levels)-int(j in (0,1))
        need(actual==expected,'compressed rank')
        ranks.append(actual)
    total = sum((choose(n,j)-choose(n,j-1))*rank for j,rank in enumerate(ranks))
    need(total == d['N']-1-(n if t else d['baseline_nullity']), 'complete multiplicity-weighted rank')
    return ranks


def masks(n,a):
    return [sum(1<<i for i in subset) for subset in combinations(range(n),a)]


def harmonic_pairs(n,j):
    """Ballot top sets, disjoint companions, signed product-difference harmonics."""
    if j==0:
        return [()]
    result = []
    for top in combinations(range(n),j):
        if any(b+1 < 2*(i+1) for i,b in enumerate(top)):
            continue
        free = set(range(n))-set(top)
        pairs = []
        for b in top:
            a = min(i for i in free if i<b)
            free.remove(a)
            pairs.append((a,b))
        result.append(tuple(pairs))
    need(len(result)==choose(n,j)-choose(n,j-1),'ballot harmonic basis count')
    return result


def evaluate(mask,pairs):
    value = 1
    for a,b in pairs:
        value *= int(bool(mask & (1<<b)))-int(bool(mask & (1<<a)))
    return value


def literal(d):
    n,r,N,s = d['n'],d['r'],d['N'],d['s']
    levels = {a:masks(n,a) for a in range(1,r+1)}
    labels = [a for level in levels.values() for a in level]
    index = {a:i for i,a in enumerate(labels)}
    # Independently obtain harmonics by integer products, not lowering nullspaces.
    entries = []
    basis_vectors = []
    for j in range(r+1):
        hs = harmonic_pairs(n,j)
        base_masks = [0] if j==0 else levels[j]
        base_rows = [[evaluate(a,pairs) for a in base_masks] for pairs in hs]
        need(row_rank(base_rows)==len(hs),'independent harmonic rank')
        if j:
            for pairs in hs:
                for a in masks(n,j-1):
                    need(sum(evaluate(b,pairs) for b in levels[j] if a & b == a)==0,'literal lowering-zero cancellation')
        for a in range(max(1,j),r+1):
            for h,pairs in enumerate(hs):
                vector = [evaluate(b,pairs) if b.bit_count()==a else 0 for b in labels]
                entries.append((j,a,h,pairs,vector))
                basis_vectors.append(vector)
    need(len(basis_vectors)==N-1 and row_rank(basis_vectors)==N-1,'complete literal basis exhaustion')
    # Full entry-wise Gram comparisons, including cross-degree orthogonality.
    for j,a,h,pairs,u in entries:
        for k,b,h2,pairs2,v in entries:
            actual = sum(x*y for x,y in zip(u,v))
            expected = 0
            if j==k and a==b:
                base = [0] if j==0 else levels[j]
                expected = choose(n-2*j,a-j)*sum(evaluate(x,pairs)*evaluate(x,pairs2) for x in base)
            need(actual==expected,'every literal harmonic Gram entry')
    actions = 0
    dense_checks = []
    gap_checks = []
    for label,t in [('zero',Q(0)),('original',d['old']),('enlarged',d['T']),('half_enlarged',d['T']/2)]:
        beta = betas(d,t)
        C = [[Q(s*int(a==b)-1)+(beta[a.bit_count(),b.bit_count()] if not a & b else 0) for b in labels] for a in labels]
        Delta = [[Q(0) if a & b else (Q(1) if a.bit_count()!=b.bit_count() else -Q(sum(d['gamma'][a.bit_count(),c] for c in range(1,r+1) if c!=a.bit_count()),d['gamma'][a.bit_count(),a.bit_count()])) for b in labels] for a in labels]
        need(max(sum(abs(x) for x in row) for row in Delta)==d['B'],'literal exact row-norm equality')
        for i in range(n):
            star = [int(bool(a & (1<<i))) for a in labels]
            need(all(sum(x*y for x,y in zip(row,star))==0 for row in C),'literal full stars')
        sums = [sum(row) for row in C]
        L = [[1+sum(sums)]+[1-v for v in sums]]
        L += [[1-sums[i]]+[1+x for x in row] for i,row in enumerate(C)]
        need(all(sum(row)==N for row in L),'full affine lift row normalization')
        all_labels = [0]+labels
        need(all(L[i][k]==(s if i==k else 0) for i,a in enumerate(all_labels) for k,b in enumerate(all_labels) if a & b),'full H support including nonempty diagonals')
        denominator = lcm(*(x.denominator for row in C for x in row))
        integer_C = [[int(x*denominator) for x in row] for row in C]
        for j,a,h,pairs,v in entries:
            actual = [sum(x*y for x,y in zip(row,v)) for row in integer_C]
            predicted = []
            for b in labels:
                size = b.bit_count()
                coefficient = s*int(size==a)+(-1)**j*beta[size,a]*choose(n-size-j,a-j)-int(j==0)*choose(n,a)
                predicted.append(int(coefficient*denominator)*evaluate(b,pairs))
            need(actual==predicted,'every full literal action agrees with complete block reduction')
            actions += 1
        upper_form = N-n*s+t*(n-1)*sum(d['gamma'][1,b] for b in range(2,r+1))
        singleton_indices = [index[a] for a in levels[1]]
        actual_upper = sum(N*int(i==k)-1-C[i][k] for i in singleton_indices for k in singleton_indices)
        need(actual_upper==n*upper_form and upper_form<0,'exact upper-cap witness')
        if n<=6:
            cr = psd_rank(C);lr = psd_rank(L)
            expected = N-1-(n if t else d['baseline_nullity'])
            need(cr==expected and lr==expected+1,'dense exact core and lift ranks')
            dense_checks.append({'parameter':label,'core_rank':cr,'lower_rank':lr})
            if not t:
                # Eigenvalue polynomial, checked literally: C0(C0-gI) is PSD.
                gap_matrix = [[sum(C[i][k]*C[k][j] for k in range(N-1))-d['g']*C[i][j] for j in range(N-1)] for i in range(N-1)]
                psd_rank(gap_matrix)
                excess = []
                for j,a,h,pairs,vector in entries:
                    if j==1 and a>=2:
                        G = choose(n-2,a-1)
                        excess.append([evaluate(b,pairs)*(int(b.bit_count()==a)-G*int(b.bit_count()==1)) for b in labels])
                    if n==2*r and a==r and j>=3 and j%2:
                        excess.append(vector)
                need(row_rank(excess)==d['baseline_nullity']-n,'complete explicit excess kernel')
                need(all(sum(x*y for x,y in zip(row,v))==0 for row in C for v in excess),'literal excess vectors in baseline kernel')
                Dv = [[sum(x*y for x,y in zip(row,v)) for row in Delta] for v in excess]
                restriction = [[sum(x*y for x,y in zip(u,dv))-d['alpha']*sum(x*y for x,y in zip(u,v)) for v,dv in zip(excess,Dv)] for u in excess]
                psd_rank(restriction)
                gap_checks.append({'baseline_polynomial_PSD':True,'excess_restriction_PSD':True,'excess_dimension':len(excess)})
    return {'n':n,'r':r,'N':N,'s':s,'basis_size':len(entries),'all_gram_entries':len(entries)**2,'full_basis_actions':actions,'dense_checks':dense_checks,'literal_gap_checks':gap_checks,'coupled_lower_rank':N-n,'baseline_nullity':d['baseline_nullity']}


def reject(call):
    try:
        call()
    except Failure:
        return
    raise Failure('invalid control accepted')


def run():
    result = {'agent':'six-reviewer-3','role':'independent mathematical reviewer','arithmetic':'stdlib integers/Fraction','compressed_cases':[],'literal_cases':[]}
    for r in range(2,11):
        for n in (2*r,2*r+1,3*r):
            d = data(n,r)
            ranks = {}
            for name,t in [('zero',Q(0)),('original',d['old']),('enlarged',d['T']),('half_enlarged',d['T']/2)]:
                ranks[name] = compressed(d,t)
                beta = betas(d,t)
                need(all(x>0 for x in beta.values()) if t else all(beta[a,a]>0 for a in range(1,r+1)), 'positive disjoint weights')
                need(all(sum(beta[a,b]*d['gamma'][a,b] for b in range(1,r+1))==d['s'] for a in range(1,r+1)),'star count equations')
            result['compressed_cases'].append({'n':n,'r':r,'N':d['N'],'s':d['s'],'row_norm_B':str(d['B']),'baseline_gap_g':str(d['g']),'excess_gap_alpha':str(d['alpha']),'old_interval':str(d['old']),'enlarged_interval':str(d['T']),'enlargement_factor':str(d['T']/d['old']),'baseline_nullity':d['baseline_nullity'],'harmonic_core_ranks':ranks})
    for n,r in [(4,2),(5,2),(6,3),(7,3),(8,4)]:
        result['literal_cases'].append(literal(data(n,r)))
    controls = []
    trials = [('negative-pivot',lambda:psd_rank([[1,2],[2,1]])),('zero-pivot-row',lambda:psd_rank([[0,1],[1,1]])),('nonsymmetric',lambda:psd_rank([[1,1],[0,1]])),('nonsquare',lambda:psd_rank([[1,0]])),('unstable-parameters',lambda:data(5,3)),('invalid-rank-one',lambda:data(4,1)),('overlarge-coupling',lambda:compressed(data(4,2),Q(3))),('zero-coupling-wrong-kernel',lambda:need(data(6,3)['baseline_nullity']==6,'baseline star-only false')),('omit-boundary-odd-kernel',lambda:need(data(6,3)['baseline_nullity']==1+3*5,'missing oddH3'))]
    for name,call in trials:
        reject(call);controls.append(name)
    result['negative_controls_rejected'] = controls
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',type=Path)
    parser.add_argument('--check',type=Path)
    args = parser.parse_args()
    result = run()
    encoded = json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.check:
        need(json.loads(args.check.read_text())==result,'expected summary mismatch')
    if args.write:
        args.write.write_text(encoded)
    print(json.dumps({'verified':True,'agent':result['agent'],'compressed_cases':len(result['compressed_cases']),'literal_cases':len(result['literal_cases']),'basis_sizes':[c['basis_size'] for c in result['literal_cases']],'negative_controls':len(result['negative_controls_rejected']),'summary_sha256':hashlib.sha256(encoded.encode()).hexdigest()},sort_keys=True))


if __name__=='__main__':
    main()
