"""Fixed original q24/k6 certificate, complete23 weighted orbits and whole pairs."""
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from math import comb
from pathlib import Path
import json
import sys

import pins
from literal import table as raw_table, typ, require
from exact import schur_psd, polynomial_psd, digest

Q, K = 24, 6
KAPPA, TRADE = F(1, 4096), F(5)
LOWER_FLOOR, CAP_FLOOR = F(1, 2**30), F(1, 2**20)
table = lru_cache(maxsize=2)(raw_table)


def member(A):
    require(type(A) is int and 0 <= A < 1 << (Q+3), 'original bitmask')
    return (A.bit_count() <= 2 or A.bit_count() == 3 and (A & 7).bit_count() >= 2) and not (
        A & 7 == 6 and (A >> 3).bit_count() == 1 and (A >> 3).bit_length() <= K)


def domain(q, k):
    require(type(q) is int and type(k) is int and (q, k) == (24, 6),
            'new singleton domain q24/k6 ONLY')
    X = [0]+sorted(sum(1 << i for i in pts)
                   for size in (1, 2, 3) for pts in combinations(range(q+3), size)
                   if member(sum(1 << i for i in pts)))
    require(len(X) == 446, 'fixed original dimension446')
    return X


def entry(A, B):
    if A == B:
        return F(3*Q+3)
    if A & B:
        return F(-1)
    a, d = table(Q)[tuple(sorted((typ(A), typ(B))))]
    r = {(1, 2): 1, (1, 4): 1, (2, 5): -1, (3, 4): -1}.get(tuple(sorted((A, B))), 0)
    return a-1+KAPPA*d+TRADE*r


def key(A):
    return A & 7, ((A >> 3) & ((1 << K)-1)).bit_count(), (A >> (K+3)).bit_count()


def run(return_state=False):
    X = domain(Q, K)[1:]
    N, s = len(X)+1, 3*Q+4
    groups = {}
    for A in X:
        groups.setdefault(key(A), []).append(A)
    keys = sorted(groups)
    sizes = [len(groups[a]) for a in keys]
    require(len(keys) == 23 and all(sizes[i] == comb(K, a[1])*comb(Q-K, a[2])
                                  for i, a in enumerate(keys)), 'complete23 original orbits')
    G = [[sizes[i]*sum(entry(groups[a][0], B) for B in groups[b]) for b in keys]
         for i, a in enumerate(keys)]
    U = [[F(N*sizes[i]*int(i == j)-sizes[i]*sizes[j])-G[i][j]
          for j in range(23)] for i in range(23)]
    require(all(G[i][j] == G[j][i] and U[i][j] == U[j][i]
                for i in range(23) for j in range(23)), 'all weighted Gram symmetry')
    star = [F(bool(a[0] & 1)) for a in keys]
    require(sum(size*x for size, x in zip(sizes, star)) == s and
            all(sum(G[i][j]*star[j] for j in range(23)) == 0 for i in range(23)),
            'exact greatest-star Gram kernel')
    A = [[G[i][j]-LOWER_FLOOR*(sizes[i]*int(i == j)-sizes[i]*star[i]*sizes[j]*star[j]/s)
          for j in range(23)] for i in range(23)]
    B = [[U[i][j]-CAP_FLOOR*sizes[i]*int(i == j) for j in range(23)] for i in range(23)]
    floors = [schur_psd(a) for a in (A, B)]
    require(floors == [22, 23], 'both strict exact fixed-space floors')
    poly = [polynomial_psd(a) for a in (G, U)]
    require([a[0] for a in poly] == [22, 23], 'separate characteristic-polynomial ranks')
    # A second, full-pair aggregation does not reuse representative row sums.
    index = {a: i for i, a in enumerate(keys)}
    full = [[F(0) for j in range(23)] for i in range(23)]
    row_sums = []
    for a in X:
        rsum = F(0)
        star_action = F(0)
        for b in X:
            value = entry(a, b)
            full[index[key(a)]][index[key(b)]] += value
            rsum += value
            star_action += value*bool(b & 1)
            if a & b:
                require(1+value == s*int(a == b), 'every original intersecting support position')
        require(star_action == 0, 'every actual original star row')
        row_sums.append(rsum)
    require(full == G, 'all529 independent full-pair original Gram entries')
    h = F(1, 3*Q+5)
    alpha = F(Q*(Q+1), 2)+3*(Q+1)*h
    empty_loop = 1+sum(row_sums)
    require(empty_loop == 1+K*(s-K)+KAPPA*(alpha-2*K*h), 'actual independent empty loop')
    for a, actual in zip(X, row_sums):
        core = (a & 7).bit_count()
        r = F(1) if core == 0 else h if core < 3 else -3*(Q+1)*h
        z = K if a & 6 else ((a >> 3) & ((1 << K)-1)).bit_count()
        if z == K:
            deleted = F(-K)
        else:
            base, slope = table(Q)[tuple(sorted((typ(a), (2, 1))))]
            deleted = -z+(K-z)*(base+KAPPA*slope-1)
        repair = 2 if a == 1 else -1 if a in (3, 5) else 0
        require(actual == KAPPA*r-deleted+TRADE*repair, 'every direct empty-row formula')
    expected_stars = [s, s-K, s-K]+[Q+5]*K+[Q+6]*(Q-K)
    require([sum(bool(a & (1 << i)) for a in X) for i in range(Q+3)] == expected_stars,
            'all actual original stars')
    require(all(sizes[i] == 1 for i, a in enumerate(keys) if a[0] in (1, 2, 4, 3, 5)
                and a[1:] == (0, 0)), 'entire repair support in fixed singleton orbits')
    require(LOWER_FLOOR <= KAPPA/2 and CAP_FLOOR < N-2*s,
            'inherited whole omitted-complement floors')
    e = F(23*23+(13-6*K)*23+2*K*K-10*K+14, 2)
    gap = F(23*23+7*23+8-2*K, 2)
    g = F(23*24, 2)-K
    r = 3+F(2, 23)
    ww = (3*23+4-r)/22
    a0 = F((2*K+1)*23+K)-F(2*K, 23)
    Q0 = e-a0*a0/(23*gap)-K*(23-K)*ww*ww/(23*gap)-F(4*23*(K-1)**2)/(g+r)
    require(Q0 == F(-91568355216, 12536354677) < 0, 'original9434 q23/k6 all-real necessary negative')
    record = {'agent': 'six-downset-3', 'role': 'researcher',
              'status': 'Exact q24/k6 certificate; ordinary complete-space/lift bridges unformalized and independently unreviewed',
              'q': Q, 'k': K, 'N': N, 's': s, 'kappa': str(KAPPA), 't': str(TRADE),
              'orbit_count': 23, 'orbit_keys': [list(a) for a in keys], 'orbit_sizes': sizes,
              'complement_dimension': N-1-23, 'whole_lower_rank': N-1, 'whole_cap_rank': N-1,
              'lower_nonempty_floor': str(LOWER_FLOOR), 'physical_projected_cap_floor': str(CAP_FLOOR),
              'complement_lower_floor': str(KAPPA/2), 'complement_cap_floor': N-2*s,
              'strict_fixed_floor_ranks': floors,
              'all_full_pair_Gram_entries_match': True, 'original_nonempty_positions': (N-1)**2,
              'all_original_support_star_and_empty_rows_match': True, 'star_census': expected_stars,
              'M_empty_empty': str((empty_loop-s)/(N-s)),
              'Gram_digest': digest([[[str(x) for x in row] for row in a] for a in (G, U)]),
              'characteristic_checks': [{'rank': a[0], 'digest': a[1], 'denominator': a[2]} for a in poly],
              'q23_k6_Q0': str(Q0), 'scope': 'New singleton point; all-Z transport and full omitted-space bridge in PROOF.md',
              'failed_variance_bound_did_not_prove_infeasibility': True}
    if return_state:
        return record, {'X': X, 'keys': keys, 'sizes': sizes, 'G': G, 'U': U, 'star': star}
    return record


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, indent=2))
