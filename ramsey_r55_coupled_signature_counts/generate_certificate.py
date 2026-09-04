#!/usr/bin/env python3
"""Generate exact primal/dual certificates for the coupled signature systems.

SciPy discovers certificates; integer verification below authorizes output.
No solver status alone is used as mathematical evidence. Output is compact TSV.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
from math import gcd, lcm
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp


HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / 'ramsey_r55_exceptional_signature_capacity'
PINS = {
    'classify_small_cores.py':'9ea9464a21da61b22b2e66b83e6da1a161badf107d233a50889520aeaf640e71',
    'CENSUS.tsv':'08a4a09b677031faf9dc7c7dc403e8e06e3245e39d13ca260b251a5c34ed5363',
}
HEADER = 'counts_18_to_24\tM\tred_mask\torbit_size\tkind\tpayload'


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


for name,digest in PINS.items():
    require(sha256((PRIOR/name).read_bytes()).hexdigest() == digest, name)
sys.path.insert(0,str(PRIOR))
from classify_small_cores import B, input_rows, screen, signature_caps


def adjacency(mask,k):
    adj = [0]*k
    for bit,(i,j) in enumerate(combinations(range(k),2)):
        if mask >> bit & 1:
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    return adj


def passing_cores(ds,M):
    k, eps = len(ds), [d-21 for d in ds]
    answer = []
    for mask in range(1 << (k*(k-1)//2)):
        adj = adjacency(mask,k)
        sums = [sum(eps[j] for j in range(k) if adj[i] >> j & 1) for i in range(k)]
        if any(s > M-B[d] for s,d in zip(sums,ds)):
            continue
        if sum(e*(d-a.bit_count()) for e,d,a in zip(eps,ds,adj)) > (43-k)*(M-220):
            continue
        if screen(adj,ds,M)['reason'] == 'pass':
            answer.append(mask)
    return answer


def degree_orbits(masks,ds):
    """Only rename exceptional vertices within equal global-degree classes."""
    k = len(ds)
    edges = list(combinations(range(k),2))
    index = {edge:i for i,edge in enumerate(edges)}
    groups = [[i for i,d in enumerate(ds) if d == degree] for degree in sorted(set(ds))]
    maps = []
    for images in product(*(permutations(group) for group in groups)):
        permutation = tuple(i for group in images for i in group)
        maps.append([index[tuple(sorted((permutation[i],permutation[j])))] for i,j in edges])
    seen, allowed = set(), set(masks)
    for mask in masks:
        if mask in seen:
            continue
        ones = [i for i in range(len(edges)) if mask >> i & 1]
        orbit = {sum(1 << mapping[i] for i in ones) for mapping in maps}
        require(orbit <= allowed and min(orbit) == mask and not orbit & seen, 'orbit partition')
        seen |= orbit
        yield mask,len(orbit)
    require(seen == allowed, 'complete orbit coverage')


def solve(ds,M,mask):
    k, n = len(ds), 43-len(ds)
    adj = adjacency(mask,k)
    caps = signature_caps(adj,ds,M)
    require(caps is not None and bool(caps), 'admissible signature domain')
    signatures, upper = list(caps), list(caps.values())
    b = [n]+[d-a.bit_count() for d,a in zip(ds,adj)]
    matrix = [[1]*len(signatures)]+[[int(x >> i & 1) for x in signatures] for i in range(k)]
    A, target = np.array(matrix,dtype=float), np.array(b,dtype=float)
    answer = milp(np.zeros(len(signatures)), integrality=np.ones(len(signatures)),
                  bounds=Bounds(0,upper), constraints=LinearConstraint(A,target,target),
                  options={'time_limit':20})
    if answer.success:
        y = [round(x) for x in answer.x]
        require(all(0 <= value <= cap for value,cap in zip(y,upper)), 'exact primal boxes')
        require([sum(a*x for a,x in zip(row,y)) for row in matrix] == b, 'exact primal equalities')
        return 'primal', ','.join(f'{sig}:{value}' for sig,value in zip(signatures,y) if value)
    require(answer.status == 2, 'MILP did not finish: '+str(answer.message))

    # Find lambda.b > sum_X c_X max(0,lambda.a_X).
    # z_X >= lambda.a_X, z_X >= 0; bounded lambda is only a discovery normalization.
    dimension, count = k+1, len(signatures)
    objective = np.array([-v for v in b]+upper,dtype=float)
    inequalities = np.concatenate((A.T,-np.eye(count)),axis=1)
    dual = linprog(objective,A_ub=inequalities,b_ub=np.zeros(count),
                   bounds=[(-1,1)]*dimension+[(0,None)]*count,method='highs')
    require(dual.success and dual.fun < -1e-7, 'no certified linear exclusion found')
    rationals = [Fraction(float(x)).limit_denominator(10000) for x in dual.x[:dimension]]
    scale = lcm(*(x.denominator for x in rationals))
    weights = [int(x*scale) for x in rationals]
    common = gcd(*weights)
    require(common > 0, 'nonzero dual')
    weights = [x//common for x in weights]
    lhs = sum(x*y for x,y in zip(weights,b))
    rhs = sum(cap*max(0,sum(weights[i]*matrix[i][j] for i in range(dimension)))
              for j,cap in enumerate(upper))
    require(lhs > rhs, ('exact dual failed',weights,lhs,rhs))
    return 'dual', ','.join(map(str,weights))


def main():
    records, total = [], Counter()
    profile_count = 0
    for row,ds in input_rows():
        if len(ds) > 6:
            continue
        M = int(row['M'])
        masks = passing_cores(ds,M)
        if not masks:
            continue
        profile_count += 1
        for mask,size in degree_orbits(masks,ds):
            kind,payload = solve(ds,M,mask)
            total[kind] += size
            records.append('\t'.join((row['counts_18_to_24'],str(M),str(mask),str(size),kind,payload)))
    require(profile_count == 25 and len(records) == 374, 'input orbit universe')
    require(total == Counter(primal=4800,dual=137), total)
    print(HEADER)
    print('\n'.join(records))


if __name__ == '__main__':
    main()
