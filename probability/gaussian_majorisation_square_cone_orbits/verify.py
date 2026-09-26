#!/usr/bin/env python3
"""Exact constructor and monotone-matching verifier; CPython >=3.11, stdlib.

The finite certificate is a premise of the computer-assisted author proof.
No numerical quadrature or sample of Gaussian variances is used.
"""
from fractions import Fraction
from itertools import permutations, product
from math import comb
from pathlib import Path
import argparse
import hashlib
import json

A = ((1,0,1),(0,1,1),(-1,0,1),(0,-1,1))
B = ((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1))
BASE_A = (12,7,15,44)
BASE_B = (21,11,23,43)
GROUP = tuple(product(permutations(range(3)), product((-1,1), repeat=3)))
KEYS = tuple(product(range(3), range(5), range(7)))
N = 48
FULL = (1 << N) - 1


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True)+'\n').encode()


def basis(points):
    """Individual-center coefficients after clearing and shifting variables."""
    result = []
    for perm, signs in GROUP:
        row = []
        for point in points:
            e = [0,0,0]
            for i in range(3):
                e[perm[i]] += signs[i]*point[i]
            powers = (e[0]+1, e[0]+e[1]+2, sum(e)+3)
            require(all(0 <= d <= m for d,m in zip(powers,(2,4,6))),
                    'Laurent exponents outside the certified box')
            row.append(tuple(comb(powers[0], k[0])*comb(powers[1], k[1])
                             *comb(powers[2], k[2])
                             if all(j <= d for j,d in zip(k,powers)) else 0
                             for k in KEYS))
        result.append(row)
    return result


def make_order(points, weights):
    polynomials = basis(points)
    up = []
    margin = None
    witness = None
    for i in range(N):
        row = 0
        for j in range(N):
            forms = [tuple(polynomials[j][m][k]-polynomials[i][m][k]
                           for m in range(4)) for k in range(len(KEYS))]
            values = [sum(c*w for c,w in zip(form, weights)) for form in forms]
            if any(v < 0 or (v == 0 and any(form))
                   for form,v in zip(forms,values)):
                continue
            row |= 1 << j
            for k,form,value in zip(KEYS,forms,values):
                if any(form):
                    bound = Fraction(value,184*max(map(abs,form)))
                    if margin is None or bound < margin:
                        margin = bound
                        witness = {'lower':i,'upper':j,'monomial':k,
                                   'linear_form':form,'raw_value':value}
        up.append(row)
    require(margin is not None and margin > 0, 'No positive coefficient margin')
    return {'up':up, 'ordered_pairs':sum(row.bit_count() for row in up),
            'weight_L1_margin':str(margin), 'margin_witness':witness}


def audit_order(up):
    for i in range(N):
        require(up[i] >> i & 1, 'Order is not reflexive')
        for j in range(N):
            if up[i] >> j & 1:
                require(up[j] & ~up[i] == 0, 'Order is not transitive')
                require(i == j or not (up[j] >> i & 1), 'Order is not antisymmetric')


def upper_sets(up):
    """Disjoint complete branching: include the up-set or exclude the down-set."""
    down = [sum(1 << i for i in range(N) if up[i] >> j & 1) for j in range(N)]
    out = []
    def visit(remaining, included):
        if not remaining:
            out.append(included)
            return
        v = max((i for i in range(N) if remaining >> i & 1),
                key=lambda i:(down[i]&remaining).bit_count()
                            *(up[i]&remaining).bit_count())
        visit(remaining & ~up[v], included | (up[v]&remaining))
        visit(remaining & ~down[v], included)
    visit(FULL,0)
    require(len(out) == len(set(out)), 'Upper-set enumeration has duplicates')
    for s in out:
        require(all(not (s >> v & 1) or up[v] & ~s == 0 for v in range(N)),
                'Enumerated set is not upper')
    return sorted(out)


def antipode(mask):
    return sum(1 << (v ^ 7) for v in range(N) if mask >> v & 1)


def monotone_matching(s, up_b):
    opposite = antipode(s)
    positive = s & ~opposite
    negative = opposite & ~s
    matching = {}
    def augment(n, visited):
        for q in range(N):
            if positive >> q & 1 and up_b[n] >> q & 1 and q not in visited:
                visited.add(q)
                if q not in matching or augment(matching[q],visited):
                    matching[q] = n
                    return True
        return False
    for n in range(N):
        if negative >> n & 1:
            require(augment(n,set()), 'No monotone matching for an A-upper set')
    require(len(matching) == negative.bit_count() == positive.bit_count(),
            'Matching has wrong cardinality')
    require(len(set(matching.values())) == len(matching), 'Repeated matching source')
    for q,n in matching.items():
        require(negative >> n & 1 and positive >> q & 1 and up_b[n] >> q & 1,
                'Invalid monotone matching edge')
    return sorted(matching.items())


def construction():
    require(len(GROUP) == N and len(set(GROUP)) == N, 'Group enumeration failed')
    for i,(perm,signs) in enumerate(GROUP):
        require(GROUP[i ^ 7] == (perm,tuple(-s for s in signs)), 'Wrong antipodal label')
    orders = {'A':make_order(A,BASE_A), 'B':make_order(B,BASE_B)}
    for item in orders.values():
        audit_order(item['up'])
    certificate = {
        'schema':'square-cone-orbit-orders-v1', 'group_size':N,
        'group_order':'lexicographic (permutation of (0,1,2), signs in (-1,1)^3)',
        'group_action':'(g x)_i = signs_i * x_(perm_i)',
        'clearing_monomial_powers':[1,2,3], 'coefficient_degree_box':[2,4,6],
        'base_probability_numerators':[8,*BASE_A,*BASE_B], 'base_denominator':184,
        'points_A':A, 'points_B':B, 'orders':orders
    }
    sets = upper_sets(orders['A']['up'])
    digest = hashlib.sha256()
    matched_edges = 0
    nonempty = 0
    for s in sets:
        matching = monotone_matching(s,orders['B']['up'])
        matched_edges += len(matching)
        nonempty += bool(matching)
        digest.update((str(s)+':'+str(matching)+'\n').encode())

    # Direct geometry: all 36 source pairs are legitimate contractions.
    x = ((0,0,0),)+A+tuple(tuple(-v for v in b) for b in B)
    y = ((0,0,0),)+A+B
    losses = {}
    for i in range(9):
        require(sum(v*v for v in x[i]) == sum(v*v for v in y[i]), 'Norm changed')
        for j in range(i):
            loss = sum((u-v)**2 for u,v in zip(x[i],x[j]))-sum((u-v)**2 for u,v in zip(y[i],y[j]))
            require(loss >= 0,'Not a contraction')
            losses[loss] = losses.get(loss,0)+1
    require(losses == {0:28,8:8}, 'Unexpected distance losses')

    # A false order makes the universal matching claim fail.
    reversed_b = [sum(1 << j for j in range(N) if orders['B']['up'][j] >> i & 1)
                  for i in range(N)]
    rejected = False
    for s in sets:
        try:
            monotone_matching(s,reversed_b)
        except RuntimeError:
            rejected = True
            break
    require(rejected, 'Reversing the B-order was not rejected')

    record = {
        'status':'SQUARE_CONE_ORBIT_MATCHING_CERTIFICATE_PASS',
        'certificate_sha256':hashlib.sha256(encode(certificate)).hexdigest(),
        'A_ordered_pairs':orders['A']['ordered_pairs'],
        'B_ordered_pairs':orders['B']['ordered_pairs'],
        'A_upper_sets':len(sets), 'nonempty_monotone_matchings':nonempty,
        'matched_edges_total':matched_edges, 'matching_digest':digest.hexdigest(),
        'A_weight_L1_margin':orders['A']['weight_L1_margin'],
        'B_weight_L1_margin':orders['B']['weight_L1_margin'],
        'all_variance_weight_ball_radius':'1/552',
        'preserved_pairs':losses[0], 'strict_pairs':losses[8],
        'reversed_order_control_rejected':True,
        'trust_boundary':'Exact finite certificate plus the analytic orbit/hinge reduction in PROOF.md; no independent peer review or proof-assistant formalization.'
    }
    return certificate,record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--certificate',action='store_true',help='print the regenerated certificate')
    args = parser.parse_args()
    certificate,record = construction()
    here = Path(__file__).resolve().parent
    if args.check:
        require(encode(certificate) == (here/'CERTIFICATE.json').read_bytes(),
                'Regenerated certificate differs')
        require(encode(record) == (here/'EXPECTED.json').read_bytes(), 'Audit record differs')
        print(record['status'],hashlib.sha256(encode(record)).hexdigest())
    else:
        print(encode(certificate if args.certificate else record).decode(),end='')


if __name__=='__main__':
    main()
