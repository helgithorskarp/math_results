#!/usr/bin/env python3
"""Definition-level and polynomial certificate checks; CPython 3.11+ only.

Author: six-downset-2, researcher. The characteristic coefficients are
computed by principal determinants using standard-library arithmetic,
independently of the SymPy DomainMatrix generator. The fraction-free PSD
checker and harmonic audit pattern are adapted with credit from the
published rank-four verifier by six-downset-3. All claims for unbounded n
also require the ordinary harmonic-completeness and rank-repair proof.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, lcm, prod
from hashlib import sha256
from pathlib import Path
from copy import deepcopy
import argparse
import json

from poly import P, require, determinant, elementary
from matrices import choose, sizes, parts, weights, generic_weights, sectors, repair_constants, matrix


def psd_rank(A):
    N = len(A)
    require(N > 0 and all(len(row) == N for row in A), 'PSD matrix shape')
    require(all(A[i][j] == A[j][i] for i in range(N) for j in range(N)), 'PSD asymmetry')
    d = lcm(*(Q(x).denominator for row in A for x in row))
    z = [[int(Q(x)*d) for x in row] for row in A]
    previous, rank = 1, 0
    for k in range(N):
        require(all(z[i][i] >= 0 for i in range(k,N)), 'negative Schur diagonal')
        pivot_index = next((i for i in range(k,N) if z[i][i] > 0), None)
        if pivot_index is None:
            require(all(z[i][j] == 0 for i in range(k,N) for j in range(k,N)), 'zero diagonal with nonzero residual')
            break
        if pivot_index != k:
            z[k], z[pivot_index] = z[pivot_index], z[k]
            for row in z:
                row[k], row[pivot_index] = row[pivot_index], row[k]
        pivot = z[k][k]
        for i in range(k+1,N):
            for j in range(i,N):
                v = pivot*z[i][j]-z[i][k]*z[k][j]
                require(v % previous == 0, 'nonintegral Bareiss step')
                z[i][j] = z[j][i] = v//previous
        previous = pivot
        rank += 1
    return rank


def shifted_coefficients(N, K):
    j, A = K
    d = len(A)-(2 if j == 0 else 1 if j == 1 else 0)
    e = elementary(A)
    require(all(v == 0 for v in e[d+1:]), 'characteristic kernel mismatch')
    lower = [sum((-1)**(k-l)*comb(d-l,k-l)*e[l] for l in range(k+1)) for k in range(1,d+1)]
    upper = [sum((-1)**l*comb(d-l,k-l)*(N-1)**(k-l)*e[l] for l in range(k+1)) for k in range(1,d+1)]
    require(all(v > 0 for v in lower+upper), 'spectral gap not greater than one')
    return d, e, lower, upper


def polynomial_check(certificate):
    n = P([12,1])
    N, s = sizes(n)
    D = 120*prod(n-i for i in range(2,10))
    B = [[P(0) for _ in range(5)] for _ in range(5)]
    for (a,b),(p,factors) in parts(n).items():
        v = 120*p*prod(n-i for i in range(2,10) if i not in factors)
        B[a-1][b-1] = B[b-1][a-1] = v
    sD, mD = s*D, (N-1)*D
    count = 0
    for a in range(1,6):
        require(sum(B[a-1][b-1]*choose(n-a-1,b-1) for b in range(1,6)) == sD, 'symbolic star equation')
        require(sum(B[a-1][b-1]*choose(n-a,b) for b in range(1,6)) == mD-sD, 'symbolic centering equation')
        count += 2
    records = {}
    expected_names = set()
    for j in range(6):
        layers = list(range(max(1,j),6))
        G = [choose(n-2*j,a-j) for a in layers]
        H = [[sD*int(a == b) + (-1)**j*B[a-1][b-1]*choose(n-a-j,b-j) -
              (choose(n,b)*D if j == 0 else 0) for b in layers] for a in layers]
        for row in H:
            for v in row:
                v.integers()
        for i in range(len(layers)):
            for k in range(len(layers)):
                require(G[i]*H[i][k] == G[k]*H[k][i], 'symbolic harmonic self-adjointness')
                count += 1
        if j <= 1:
            for row in H:
                require(sum(row) == 0, 'symbolic constant kernel')
                count += 1
                if j == 0:
                    require(sum(a*v for a,v in zip(layers,row)) == 0, 'symbolic cardinality kernel')
                    count += 1
        d = len(layers)-(2 if j == 0 else 1 if j == 1 else 0)
        e = elementary(H)
        require(all(v == 0 for v in e[d+1:]), 'symbolic characteristic zeros')
        count += len(e)-1-d
        degrees = []
        for k in range(1,d+1):
            low = sum((-1)**(k-l)*comb(d-l,k-l)*e[l]*D**(k-l) for l in range(k+1))
            high = sum((-1)**l*comb(d-l,k-l)*e[l]*mD**(k-l) for l in range(k+1))
            for kind,v in [('lower',low),('upper',high)]:
                label = f'{kind}_{j}_{k}'
                expected_names.add(label)
                rec = certificate[label]
                require(type(rec['shift']) is int and rec['shift'] == 12, 'incorrect shift')
                p,q = rec['numerator_ascending'], rec['denominator_ascending']
                require(type(p) is list and type(q) is list and p and q, 'coefficient arrays required')
                require(all(type(x) is int and x >= 0 for x in p+q), 'nonnegative integer sign coefficients required')
                require(p[0] > 0 and q[0] > 0 and p[-1] > 0 and q[-1] > 0, 'positive constants and leading terms required')
                require(P(p)*D**k == P(q)*v, 'wrong polynomial identity: '+label)
                count += 1
                degrees.append([label,len(p)-1,len(q)-1])
        records[str(j)] = {'sector_size':len(layers), 'positive_rank':d, 'certificate_degrees':degrees}
    require(set(certificate) == expected_names, 'unexpected certificate margin')
    require(N-2*s == choose(n-1,5), 'strict half-density identity')
    count += 1
    return {'identities':count, 'spectral_margins':len(expected_names), 'shift':12, 'sectors':records}


def finite_case(n):
    B = weights(n)
    N,s,blocks = sectors(n,B)
    for a in range(1,6):
        require(sum(B[a-1][b-1]*(comb(n-a-1,b-1) if n-a-1 >= b-1 >= 0 else 0) for b in range(1,6)) == s, 'finite star equation')
        require(sum(B[a-1][b-1]*(comb(n-a,b) if n-a >= b >= 0 else 0) for b in range(1,6)) == N-1-s, 'finite centering equation')
    lower_rank = 0
    margin_count = 0
    finite_sectors = []
    for j,(K,G,layers) in enumerate(blocks):
        require(all(G[i]*K[i][k] == G[k]*K[k][i] for i in range(len(G)) for k in range(len(G))), 'finite self-adjointness')
        d, e, low, high = shifted_coefficients(N,(j,K))
        finite_sectors.append({'j':j,'positive_rank':d,
                               'characteristic_elementary':[str(x) for x in e],
                               'lower_shift_elementary':[str(x) for x in low],
                               'upper_shift_elementary':[str(x) for x in high]})
        margin_count += len(low)+len(high)
        multiplicity = comb(n,j)-(comb(n,j-1) if j else 0)
        lower_rank += d*multiplicity
    require(lower_rank == N-n-2, 'centered core rank')
    eps,delta,bound = repair_constants(n)
    require(eps > 0 and eps*bound == Q(n,48*(N-1)) and eps*bound <= Q(1,48), 'repair norm identity')
    repaired_rank = 0
    repaired_U_rank = 0
    _,_,repaired = sectors(n,B,repaired=True)
    for j,(K,G,layers) in enumerate(repaired):
        A = [[G[i]*K[i][k] for k in range(len(G))] for i in range(len(G))]
        U = [[G[i]*(N*int(a == b)-(comb(n,b) if j == 0 else 0)-K[i][k])
              for k,b in enumerate(layers)] for i,a in enumerate(layers)]
        d = len(G)-(1 if j <= 1 else 0)
        require(psd_rank(A) == d, 'repaired lower sector rank')
        require(psd_rank(U) == len(G), 'repaired upper sector rank')
        multiplicity = comb(n,j)-(comb(n,j-1) if j else 0)
        repaired_rank += d*multiplicity
        repaired_U_rank += len(G)*multiplicity
    require(repaired_rank == N-1-n and repaired_U_rank == N-1, 'repaired core ranks')
    return {'n':n,'N':N,'s':s,'sector_sizes':[len(x[0]) for x in blocks],
            'centered_core_rank':lower_rank, 'repaired_full_lower_rank':repaired_rank+1,
            'repaired_full_upper_rank':repaired_U_rank,'strict_spectral_margins':margin_count,
            'epsilon':str(eps),'sectors':finite_sectors}


def definition_check(n,V,L):
    N,s = map(int,sizes(Q(n)))
    require(len(V) == N and V[0] == 0 and len(set(V)) == N, 'vertex ordering')
    require(all((A & ~(1 << i)) in V for A in V for i in range(n) if A >> i & 1), 'downward closure')
    require(all(len(row) == N for row in L), 'literal matrix shape')
    require(all(L[i][j] == L[j][i] for i in range(N) for j in range(N)), 'literal symmetry')
    require(all(sum(row) == N for row in L), 'literal row sum')
    require(all(L[i][j] == s*int(i == j) for i,A in enumerate(V) for j,B in enumerate(V) if A & B), 'literal support/diagonal')
    for p in range(n):
        star = [i for i,A in enumerate(V) if A >> p & 1]
        require(len(star) == s and all(sum(row[i] for i in star) == s for row in L), 'literal forced stars')


def full_case(n=7):
    V,L = matrix(n)
    definition_check(n,V,L)
    N,s = map(int,sizes(Q(n)))
    U = [[N*int(i == j)-L[i][j] for j in range(N)] for i in range(N)]
    require(psd_rank(L) == N-n and psd_rank(U) == N-1, 'full literal slack ranks')
    raw = json.dumps([[str(v) for v in row] for row in L],separators=(',',':')).encode()
    return {'n':n,'N':N,'lower_rank':N-n,'upper_rank':N-1,'L_sha256':sha256(raw).hexdigest()}


def nullspace(A, width):
    R = [[Q(x) for x in row] for row in A]
    r = 0
    pivots = []
    for k in range(width):
        pivot = next((i for i in range(r,len(R)) if R[i][k] != 0),None)
        if pivot is None:
            continue
        R[r],R[pivot] = R[pivot],R[r]
        v = R[r][k]
        R[r] = [x/v for x in R[r]]
        for i in range(len(R)):
            if i != r:
                v = R[i][k]
                R[i] = [x-v*y for x,y in zip(R[i],R[r])]
        pivots.append(k)
        r += 1
    out = []
    for k in range(width):
        if k in pivots:
            continue
        v = [Q(0)]*width
        v[k] = Q(1)
        for i,p in enumerate(pivots):
            v[p] = -R[i][k]
        d = lcm(*(x.denominator for x in v))
        out.append([int(x*d) for x in v])
    require(all(sum(x*y for x,y in zip(row,v)) == 0 for row in A for v in out), 'nullspace residual')
    return out


def harmonic_audit(n=7):
    """All basis vectors, lifts and disjointness actions at the dense boundary."""
    level = {a:[sum(1 << i for i in A) for A in combinations(range(n),a)] for a in range(6)}
    dimensions = []
    action_count = 0
    norms = 0
    total_lifts = 0
    all_level_lifts = {a:[] for a in range(1,6)}
    for j in range(min(5,n//2)+1):
        basis = [[1]] if j == 0 else nullspace([[int(S & T == S) for T in level[j]] for S in level[j-1]],len(level[j]))
        mult = comb(n,j)-(comb(n,j-1) if j else 0)
        require(len(basis) == mult, 'complete harmonic dimension')
        dimensions.append(mult)
        gram = [[sum(x*y for x,y in zip(v,w)) for w in basis] for v in basis]
        require(psd_rank(gram) == mult, 'harmonic independence')
        layers = list(range(max(1,j),min(5,n-j)+1))
        lifts = {a:[[sum(h[k] for k,T in enumerate(level[j]) if T & A == T) for A in level[a]] for h in basis] for a in layers}
        for a in layers:
            all_level_lifts[a].extend((j,v) for v in lifts[a])
            for i,v in enumerate(lifts[a]):
                if j:
                    require(sum(v) == 0, 'nontrivial harmonic mean')
                for k,w in enumerate(lifts[a]):
                    require(sum(x*y for x,y in zip(v,w)) == comb(n-2*j,a-j)*gram[i][k], 'exact harmonic norm')
                    norms += 1
            total_lifts += mult
        for a in range(1,6):
            for b in layers:
                for hidx,v in enumerate(lifts[b]):
                    image = [sum(v[k] for k,T in enumerate(level[b]) if A & T == 0) for A in level[a]]
                    if a not in layers:
                        require(all(x == 0 for x in image), 'disjoint action outside harmonic range')
                    else:
                        c = (-1)**j*(comb(n-a-j,b-j) if n-a-j >= b-j >= 0 else 0)
                        require(image == [c*x for x in lifts[a][hidx]], 'literal disjoint harmonic action')
                    action_count += 1
    require(total_lifts == sum(comb(n,a) for a in range(1,6)), 'complete lifted dimension')
    cross_norms = 0
    for vectors in all_level_lifts.values():
        for i,(j,v) in enumerate(vectors):
            for k,w in vectors[:i]:
                if j != k:
                    require(sum(x*y for x,y in zip(v,w)) == 0, 'cross-degree harmonic orthogonality')
                    cross_norms += 1
    return {'n':n,'harmonic_dimensions':dimensions,'all_lifted_vectors':total_lifts,
            'norm_identities':norms,'cross_degree_norm_identities':cross_norms,
            'literal_disjoint_basis_actions':action_count}


def controls(certificate):
    accepted_psd = 0
    for v in product((-1,0,1),repeat=6):
        a,b,c,d,e,f = v
        A = [[a,b,c],[b,d,e],[c,e,f]]
        truth = all(determinant([[A[i][j] for j in ix] for i in ix]) >= 0
                    for k in range(1,4) for ix in combinations(range(3),k))
        try:
            psd_rank(A)
            actual = True
        except ValueError:
            actual = False
        require(actual == truth, 'PSD checker/principal-minor disagreement')
        accepted_psd += actual
    require(accepted_psd == 24, 'ternary PSD control count')
    rejected = []
    def reject(label, fn):
        try:
            fn()
        except (ValueError,KeyError):
            rejected.append(label)
        else:
            raise ValueError('Malformed control accepted: '+label)
    for label, field, value in [('corrupt_constant','numerator_ascending',certificate['lower_0_1']['numerator_ascending'][0]+1),
                                 ('negative_coefficient','numerator_ascending',-1),
                                 ('zero_denominator_constant','denominator_ascending',0)]:
        data = deepcopy(certificate)
        data['lower_0_1'][field][0] = value
        reject(label,lambda data=data:polynomial_check(data))
    data = deepcopy(certificate)
    data['lower_0_1']['shift'] = 11
    reject('wrong_shift',lambda:polynomial_check(data))
    reject('outside_order',lambda:weights(6))
    reject('float_order',lambda:weights(7.0))
    reject('generic_below_range',lambda:generic_weights(11))
    reject('indefinite_zero_diagonal',lambda:psd_rank([[0,1],[1,0]]))
    V,L = matrix(7)
    L[0][0] += 1
    reject('corrupt_empty_loop',lambda:definition_check(7,V,L))
    return {'ternary_symmetric_matrices':729,'psd_count':accepted_psd,'rejected':rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check',type=Path)
    args = parser.parse_args()
    cert = json.loads(Path(__file__).with_name('POSITIVITY_CERTIFICATE.json').read_text())
    result = {'agent':'six-downset-2','role':'researcher',
              'status':'Exact identities/certificates plus ordinary all-order proof; author-checked, unformalized.',
              'symbolic':polynomial_check(cert),'finite':[finite_case(n) for n in range(7,13)],
              'literal':full_case(),'harmonic_audit':harmonic_audit(),'controls':controls(cert)}
    if args.check:
        require(result == json.loads(args.check.read_text()), 'expected-output mismatch')
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'ok':True,'symbolic_identities':result['symbolic']['identities'],
                      'infinite_spectral_margins':result['symbolic']['spectral_margins'],
                      'finite_orders':[x['n'] for x in result['finite']],
                      'literal_lower_rank':result['literal']['lower_rank'],
                      'literal_upper_rank':result['literal']['upper_rank'],
                      'harmonic_basis_actions':result['harmonic_audit']['literal_disjoint_basis_actions'],
                      'rejected_controls':len(result['controls']['rejected'])}))


if __name__ == '__main__':
    main()
