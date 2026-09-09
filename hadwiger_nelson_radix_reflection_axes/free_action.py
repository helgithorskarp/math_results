#!/usr/bin/env python3
"""Exact pair-stabilizer accounting after the physical reflection-axis closure.

This consumes the h4167 survivor list; it does not recompute its completeness.
Curve actions are checked both on Eisenstein rows and on bivariate polynomials.
"""
import argparse
from collections import Counter
import json
from math import comb, gcd
from pathlib import Path
import exact as X
from verify import V

HERE = Path(__file__).resolve().parent
PAIR_SHA = '9aa6caf04379f9e8c9736ad8d287ea51902c63e4d317f9c9c7deb112700f8149'


def primitive(terms):
    terms = {k:v for k,v in terms.items() if v}
    divisor = 0
    for value in terms.values():
        divisor = gcd(divisor, value)
    if terms[max(terms)] < 0:
        divisor = -divisor
    return tuple((i,j,c//divisor) for (i,j),c in sorted(terms.items()))


def substitute(f, rotation):
    # Integer homogenized expansion of 2^d f((-x-3y)/2,(x-y)/2).
    # Conjugation is f(x,-y). Primitive normalization removes the scalar.
    degree = max(i+j for i,j,c in f)
    terms = Counter()
    for i,j,c in f:
        if not rotation:
            terms[i,j] += c*(-1)**j
            continue
        for a in range(i+1):
            for b in range(j+1):
                terms[a+b,i+j-a-b] += (c*2**(degree-i-j)*comb(i,a)*comb(j,b)
                                      *(-1)**a*(-3)**(i-a)*(-1)**(j-b))
    return primitive(terms)


def compose(a,b):
    return tuple(a[b[i]] for i in range(len(a)))


def curve_group():
    rows,factors,circle,monomials,rowids = V.reconstruct_inventory()
    identity = tuple(range(len(factors)))
    rotation,conjugation = list(identity),list(identity)
    for row,c in rowids.items():
        order = max(j for j,digit in enumerate(row) if digit!=(0,0))
        X.need(max(i+j for i,j,t in factors[c])==2*order, 'row order determines norm-curve bidegree')
        power,out = (1,0),[]
        for digit in row:
            out.append(V.e_mul(digit,power))
            power = V.e_mul(power,(-1,1))
        rotation[c] = rowids[V.canonical_row(tuple(out))]
        conjugation[c] = rowids[V.canonical_row(tuple((a+b,-b) for a,b in row))]
    rotation,conjugation = tuple(rotation),tuple(conjugation)
    lookup = {primitive({(i,j):c for i,j,c in f}):k for k,f in enumerate(factors)}
    X.need(len(lookup)==len(factors), 'distinct event polynomials')
    polynomial_rotation = tuple(lookup[substitute(f,True)] for f in factors)
    polynomial_conjugation = tuple(lookup[substitute(f,False)] for f in factors)
    X.need(rotation==polynomial_rotation and conjugation==polynomial_conjugation,
           'independent row and bivariate-polynomial actions agree on all curves')
    rotation2 = compose(rotation,rotation)
    group = (identity,rotation,rotation2,conjugation,
             compose(rotation,conjugation),compose(rotation2,conjugation))
    X.need(len(set(group))==6 and all(sorted(g)==list(identity) for g in group), 'six permutations')
    X.need(compose(rotation,rotation2)==identity and compose(conjugation,conjugation)==identity
           and compose(compose(conjugation,rotation),conjugation)==rotation2, 'D3 relations')
    X.need(all(compose(a,b) in group for a in group for b in group), 'closed six-element group')
    return factors,group


def count(pairs, factors, group):
    X.need(len(pairs)==131356 and X.digest(pairs)==PAIR_SHA, 'accepted h4167 retained pair interface')
    X.need(pairs==sorted(pairs) and len(set(map(tuple,pairs)))==len(pairs), 'unique canonical pairs')
    degrees = [max(i+j for i,j,c in f) for f in factors]
    X.need(all(d in (2,4,6,8) for d in degrees), 'norm-curve degrees are twice radix order')
    histogram,sums,rotation_sums,free_sums = Counter(),Counter(),Counter(),Counter()
    sharp_sums,sharp_rotation,sharp_free = Counter(),Counter(),Counter()
    for a,b in pairs:
        X.need(type(a) is int and type(b) is int and 0<=a<b<len(factors), 'valid distinct curve pair')
        key = (a,b)
        images = [tuple(sorted((g[a],g[b]))) for g in group]
        X.need(min(images)==key, 'global representative without chamber restriction')
        h = sum(p==key for p in images)
        hrot = sum(p==key for p in images[:3])
        X.need(h*len(set(images))==6 and h%hrot==0, 'orbit-stabilizer check')
        bound = degrees[a]*degrees[b]
        histogram[h] += 1
        sums[h] += bound
        rotation_sums[h] += bound//hrot
        free_sums[h] += bound//h
        # In u=x+i*sqrt(3)y, v=x-i*sqrt(3)y, the two curves have
        # bidegrees (k,k),(l,l) on P1 x P1, hence intersection bound 2kl.
        sharp_bound = 2*(degrees[a]//2)*(degrees[b]//2)
        X.need(2*sharp_bound==bound, 'exact product-surface bound')
        sharp_sums[h] += sharp_bound
        sharp_rotation[h] += sharp_bound//hrot
        sharp_free[h] += sharp_bound//h
    output = lambda counts:{str(k):n for k,n in sorted(counts.items())}
    old,rot,new = sum(sums.values()),sum(rotation_sums.values()),sum(free_sums.values())
    sharp,sharp_rot,sharp_new = sum(sharp_sums.values()),sum(sharp_rotation.values()),sum(sharp_free.values())
    return {'global_pair_systems':len(pairs), 'whole_pair_systems_removed':0,
            'pair_stabilizer_histogram':output(histogram),
            'degree_product_sums_by_stabilizer':output(sums),
            'rotation_free_sums_by_stabilizer':output(rotation_sums),
            'free_D3_sums_by_stabilizer':output(free_sums),
            'bidegree_sums_by_stabilizer':output(sharp_sums),
            'bidegree_rotation_free_sums_by_stabilizer':output(sharp_rotation),
            'bidegree_free_D3_sums_by_stabilizer':output(sharp_free),
            'previous_conservative_allowance':old, 'rotation_free_allowance':rot,
            'total_degree_free_D3_allowance':new,
            'total_degree_reflection_allowance_reduction':rot-new,
            'bidegree_allowance':sharp, 'bidegree_rotation_free_allowance':sharp_rot,
            'remaining_nonfour_D3_orbit_allowance':sharp_new,
            'total_allowance_reduction':old-sharp_new,
            'imported_bidegree_allowance_reduction':old-sharp,
            'rotation_fixed_point_allowance_reduction':sharp-sharp_rot,
            'new_reflection_allowance_reduction':sharp_rot-sharp_new,
            'remaining_pairs_sha256':X.digest(pairs), 'curve_inventory_sha256':X.digest(factors),
            'rotation_permutation_sha256':X.digest(group[1]),
            'conjugation_permutation_sha256':X.digest(group[3]),
            'record_improvement':False,
            'scope':'Upper bound on possible non-four-colourable parameter D3 orbits, conditional on the imported complete pair cover. Not a distinct-root census or a full architecture closure.'}


def run(path):
    factors,group = curve_group()
    return count(json.loads(Path(path).read_text()),factors,group)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--pairs',type=Path,required=True)
    parser.add_argument('--check-expected',action='store_true')
    args=parser.parse_args()
    result=run(args.pairs)
    if args.check_expected:
        X.need(result==json.loads((HERE/'FRONTIER_EFFECT.json').read_text()), 'expected free-action bound')
    print(json.dumps(result,indent=2,sort_keys=True))
