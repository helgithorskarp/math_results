#!/usr/bin/env python3
"""Complete exact certificate for the two- and three-pair origin corners.

Python >=3.11, standard library only. The universal analytic and geometric
reductions are ordinary written mathematics in PROOF.md, not formalized.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product, combinations
from math import comb, factorial
from pathlib import Path
import argparse
import hashlib
import json
from polynomials import (
    add, mul, power, profile_products, bernstein, transform_axis
)


def profile_beta(pair_count, k):
    """Binomial/Beta integration in variables (a,u,v...), without a t variable."""
    n_real = 8-2*pair_count
    m = n_real-k
    dim = pair_count+2
    one = {(0,)*dim: Q(1)}
    def var(axis):
        e = [0]*dim
        e[axis] = 1
        return {tuple(e): Q(1)}
    a, u = var(0), var(1)
    D = add(one,a)
    b = add(one,power(a,2),Q(-1))
    residual = one
    radii = []
    for axis in range(2,dim):
        v = var(axis)
        radii.append(add(one,mul(mul(a,residual),v),Q(4)))
        residual = mul(residual,add(one,v,Q(-1)))
    C = add(one,mul(mul(a,u),residual),Q(8,m))
    a_powers = [power(a,j) for j in range(9)]
    D_powers = [power(D,j) for j in range(9)]
    C_powers = [power(C,j) for j in range(m+1)]
    b_powers = [power(b,j) for j in range(pair_count+1)]
    R_squared = [power(R,2) for R in radii]
    pair_terms = []
    for ell in range(pair_count+1):
        subset_sum = {}
        for subset in combinations(range(pair_count),ell):
            term = one
            for axis in subset:
                term = mul(term,R_squared[axis])
            subset_sum = add(subset_sum,term)
        pair_terms.append(mul(D_powers[2*(pair_count-ell)],subset_sum))
    out = {}
    for i in range(k+1):
        for j in range(m+1):
            n = i+j
            real_term = mul(mul(a_powers[n],D_powers[n_real-n]),C_powers[j])
            scale = Q(9*(-1)**n*comb(k,i)*comb(m,j))
            for ell in range(pair_count+1):
                for h in range(ell+1):
                    beta = Q(factorial(n+ell+h)*factorial(pair_count-ell),
                             factorial(n+pair_count+h+1))
                    term = mul(mul(real_term,pair_terms[ell]),
                               mul(b_powers[ell-h],a_powers[2*h]))
                    out = add(out,term,scale*comb(ell,h)*beta)
    radius_product = C_powers[m]
    for R2 in R_squared:
        radius_product = mul(radius_product,R2)
    return add(out,radius_product,Q(-1))


def to_power(basis,degree):
    """Expand every tensor Bernstein basis element back to ordinary powers."""
    out = dict(basis)
    for axis,n in enumerate(degree):
        coefficients = defaultdict(Q)
        for e,c in out.items():
            i = e[axis]
            for h in range(n-i+1):
                f = list(e)
                f[axis] = i+h
                coefficients[tuple(f)] += c*comb(n,i)*comb(n-i,h)*(-1)**h
        out = {e:c for e,c in coefficients.items() if c}
    return out


def digest(basis):
    encoded = ''.join(','.join(map(str,e))+':'+str(c.numerator)+'/'+str(c.denominator)+'\n'
                      for e,c in sorted(basis.items())).encode('ascii')
    return hashlib.sha256(encoded).hexdigest()


UNIT = (Q(0),Q(1))
LOWER = (Q(0),Q(1,2))
UPPER = (Q(1,2),Q(1))
THREE_PAIR_BOXES = [
    (UNIT,LOWER,UPPER),
    (UNIT,UPPER,LOWER),
    (UNIT,UPPER,UPPER),
    (UPPER,LOWER,LOWER),
    (LOWER,LOWER,LOWER),
]


def check_coverage(boxes):
    """Each atomic open subbox is covered exactly once; closure covers faces."""
    assert boxes and all(len(box)==3 for box in boxes)
    breakpoints = []
    for axis in range(3):
        assert all(Q(0)<=box[axis][0]<box[axis][1]<=Q(1) for box in boxes)
        points = sorted({Q(0),Q(1)} | {q for box in boxes for q in box[axis]})
        breakpoints.append(points)
    intervals = [list(zip(points,points[1:])) for points in breakpoints]
    for cell in product(*intervals):
        midpoint = tuple((left+right)/2 for left,right in cell)
        covering = sum(all(left<x<right for x,(left,right) in zip(midpoint,box))
                       for box in boxes)
        assert covering==1, ('uncovered or overlapping atomic subbox',cell,covering)
    return {'breakpoints':[[str(q) for q in row] for row in breakpoints],
            'atomic_subboxes':len(list(product(*intervals))),
            'multiplicity':1,'boundary_coverage':'closure of the atomic subboxes'}


def check_coefficients(degree,basis,expected_zeros):
    assert len(basis)==product_count(degree)
    assert [e for e,c in basis.items() if c==0]==expected_zeros
    assert all(c>=Q(4) for c in basis.values() if c)
    assert all(c==8 for e,c in basis.items() if e[0]==0)
    assert all(e[0]==degree[0] for e in expected_zeros)
    assert degree[0]>=9


def product_count(degree):
    out = 1
    for n in degree:
        out *= n+1
    return out


def derive():
    coverage = check_coverage(THREE_PAIR_BOXES)
    summaries = []
    derived = []
    for p,k,degree in [
        (2,0,(16,4,10,8)),(2,1,(15,3,7,5)),
        (2,2,(14,2,6,4)),(2,3,(13,1,8,8)),
        (3,0,(16,2,10,8,6)),(3,1,None),
    ]:
        polynomial = profile_beta(p,k)
        assert polynomial==profile_products(p,k), ('Beta versus factor identity',p,k)
        boxes = THREE_PAIR_BOXES if (p,k)==(3,1) else [(UNIT,)*p]
        for cell_index,box in enumerate(boxes):
            local = polynomial
            for axis,(left,right) in enumerate(box,2):
                local = transform_axis(local,axis,left,right)
            local_degree = degree if degree is not None else (
                (15,1,10,10,10) if cell_index==4 else (15,1,8,8,8))
            _,basis = bernstein(local,local_degree)
            zeros = []
            if (p,k)==(2,3):
                zeros = [(13,1,0,0)]
            if (p,k,cell_index)==(3,1,4):
                zeros = [(15,1,0,0,0)]
            check_coefficients(local_degree,basis,zeros)
            assert to_power(basis,local_degree)==local, ('reverse identity',p,k,cell_index)
            # The strengthened claim is checked by all coefficients of
            # P-8(1-a^9), not by a sampled comparison or the minima of P.
            scalar = {i: 8*(1-Q(comb(i,9) if i>=9 else 0,
                               comb(local_degree[0],9)))
                      for i in range(local_degree[0]+1)}
            target = {(0,)*len(local_degree):Q(8),
                      (9,)+(0,)*(len(local_degree)-1):Q(-8)}
            _,target_basis = bernstein(target,local_degree)
            assert all(c==scalar[e[0]] for e,c in target_basis.items())
            strengthened = {e:c-scalar[e[0]] for e,c in basis.items()}
            assert all(c>=0 for c in strengthened.values())
            assert to_power(strengthened,local_degree)==add(local,target,Q(-1)), (
                'strengthened reverse identity',p,k,cell_index)
            row = {'pair_count':p,'k':k,'cell':cell_index,
                   'radial_box':[[str(left),str(right)] for left,right in box],
                   'degree':list(local_degree),'coefficients':len(basis),
                   'minimum_positive':str(min(c for c in basis.values() if c)),
                   'zero_indices':[list(e) for e in zeros],
                   'sha256':digest(basis),
                   'gap8_certificate':{
                       'all_coefficients_nonnegative':True,
                       'zero_coefficients':sum(c==0 for c in strengthened.values()),
                       'minimum_positive':str(min(c for c in strengthened.values() if c)),
                       'sha256':digest(strengthened)}}
            summaries.append(row)
            derived.append((local,local_degree,basis))
    rejected = 0
    try:
        check_coverage(THREE_PAIR_BOXES[:-1])
    except AssertionError:
        rejected += 1
    corrupted = dict(profile_beta(2,1))
    corrupted[(0,0,0,0)] += 1
    if corrupted != profile_products(2,1):
        rejected += 1
    local,degree,basis = derived[1]
    corrupted = dict(basis)
    corrupted[(0,)*len(degree)] += 1
    if to_power(corrupted,degree)!=local:
        rejected += 1
    assert rejected==3
    return {'schema':1,'arithmetic':'Python Fraction, all exact',
            'uniform_positive_coefficient_bound':'4',
            'profiles':summaries,'total_coefficients':sum(x['coefficients'] for x in summaries),
            'strengthened_total_coefficients':sum(x['coefficients'] for x in summaries),
            'origin_gap_coefficient':'8',
            'independent_polynomial_identities':6,
            'complete_reverse_basis_identities':len(summaries),
            'strengthened_reverse_basis_identities':len(summaries),
            'subdivision_coverage':coverage,'mutation_rejections':rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-expected',type=Path)
    args = parser.parse_args()
    result = derive()
    if args.write_expected:
        args.write_expected.write_text(json.dumps(result,indent=2)+'\n')
    else:
        expected = json.loads(Path(__file__).with_name('expected.json').read_text())
        assert result==expected, 'evidence mismatch'
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
