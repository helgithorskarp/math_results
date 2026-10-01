#!/usr/bin/env python3
"""Pendant closure of centered nonnegative cone cores.

The generic input must be PSD, as stated in PENDANT_EXTENSIONS.md; the
constructor checks algebraic/domain hypotheses but is not a PSD verifier.
The three seed wrappers use credited all-order PSD cores.
"""
from fractions import Fraction as F

import certificates as base
import friendship
import clique_centers
from maxrank_mixtures import integer_at_least, partition_core, repaired_core


def validate_seed(family, core, center):
    if not isinstance(family, (list, tuple)) or not family:
        raise ValueError('Nonempty rank-two family required')
    if any(not isinstance(a, int) or isinstance(a, bool) or a < 0 for a in family):
        raise ValueError('Members must be nonnegative integer masks')
    if list(family) != sorted(set(family)) or family[0] != 0:
        raise ValueError('Family must be sorted, distinct and include empty')
    support = 0
    for a in family: support |= a
    n = support.bit_length()
    integer_at_least(n, 3, 'Ground order')
    integer_at_least(center, 0, 'Center')
    if center >= n or support != (1 << n)-1:
        raise ValueError('Contiguous support and a valid center required')
    if any(a.bit_count() > 2 for a in family) or any(1 << i not in family for i in range(n)):
        raise ValueError('Rank two with every singleton required')
    bit = 1 << center
    if any(bit | (1 << i) not in family for i in range(n) if i != center):
        raise ValueError('Center must be universal')
    m = len(family)-1
    if not isinstance(core, (list, tuple)) or len(core) != m or any(len(row) != m for row in core):
        raise ValueError('Core dimensions differ')
    if any(not isinstance(x, (int, F)) or isinstance(x, bool) for row in core for x in row):
        raise ValueError('Exact rational core entries required')
    C = [[F(x) for x in row] for row in core]
    S = [i for i,a in enumerate(family[1:]) if a & bit]
    B = [i for i,a in enumerate(family[1:]) if not a & bit]
    if len(S) != n or len(B) < n:
        raise ValueError('Centered nonnegative seed requires b>=n')
    for i,a in enumerate(family[1:]):
        if C[i][i] != n-1 or sum(C[i]) or sum(C[i][j] for j in S):
            raise ValueError('Diagonal, centering or center-star equation fails')
        for j,b in enumerate(family[1:]):
            if C[i][j] != C[j][i] or C[i][j] < -1 or i != j and a & b and C[i][j] != -1:
                raise ValueError('Symmetry, sign or intersection support fails')
    return C, n, S, B


def step_parameters(n, b):
    integer_at_least(n, 3, 'n'); integer_at_least(b, n, 'b')
    return dict(alpha=1-F(1,n*b), beta=1-F(1,b), chi=1+F(n,b),
                tau=1+F(1,b), h=1+F(1,n), q=1-F(n,b),
                standard_S_margin=1+F(1,b), standard_B_margin=F(1,n)+F(n,b))


def extend_once(family, core, center):
    C,n,S,B = validate_seed(family, core, center)
    b = len(B); m = len(C); p = step_parameters(n,b)
    K = [[x+1 for x in row] for row in C]
    old = family[1:]
    ordered = [old[i] for i in S+B] + [(1 << center) | (1 << n), 1 << n]
    T = [[F(0)]*(m+2) for _ in range(m+2)]
    for i in range(n):
        T[i][i] = F(n+1)
        T[i][-1] = T[-1][i] = p['h']
        for j in range(b):
            T[i][n+j] = T[n+j][i] = p['alpha']*K[S[i]][B[j]]
    for i in range(b):
        for j in range(b):
            T[n+i][n+j] = p['beta']*K[B[i]][B[j]] + p['chi']*int(i==j)
        T[n+i][-2] = T[-2][n+i] = p['tau']
        T[n+i][-1] = T[-1][n+i] = p['q']
    T[-2][-2] = T[-1][-1] = F(n+1)
    result = sorted([0]+ordered); position = {a:i for i,a in enumerate(ordered)}
    answer = [[T[position[a]][position[b]]-1 for b in result[1:]] for a in result[1:]]
    return result, answer, dict(n=n,b=b,new_N=len(result),**p)


def raw_extensions(family, core, center, count):
    integer_at_least(count,1,'Pendant count')
    D,C = list(family),core
    history = []
    for _ in range(count):
        D,C,data = extend_once(D,C,center); history.append(data)
    return D,C,history


def detecting_colors(family, center):
    n = (max(family)).bit_length()
    pendant = n-1; bit = 1 << pendant
    if sorted(a for a in family if a & bit) != sorted([bit,bit | (1 << center)]):
        raise ValueError('The newest coordinate must be a pendant leaf')
    labels = {center:0,pendant:n-1}
    labels.update({i:j for j,i in enumerate([i for i in range(n) if i not in labels],1)})
    colors = []
    for a in family[1:]:
        values = [labels[i] for i in range(n) if a >> i & 1]
        colors.append((2*values[0] if len(values)==1 else sum(values)) % n)
    counts = [colors.count(c) for c in range(n)]
    recolored = min(counts) == max(counts)
    if recolored:
        colors[family[1:].index(bit)] = 0
    return colors,recolored


def finish(family, core, center):
    C,n,_,_ = validate_seed(family,core,center)
    colors,recolored = detecting_colors(family,center)
    answer,epsilon = repaired_core(C,colors,n)
    N = len(family); beta = max(0,n*max(colors.count(c) for c in range(n))-N)
    return answer,dict(colors=colors,recolored=recolored,beta=beta,epsilon=epsilon,
                       extra_quotient=n*sum(colors.count(c)**2 for c in range(n))-(N-1)**2)


def certificate(family, core, center, count, shift=0):
    integer_at_least(shift,0,'Shift')
    D,C,_ = raw_extensions(family,core,center,count)
    C,_ = finish(D,C,center)
    s = max(D).bit_length()
    return [a << shift for a in D],base.lift(C,s),s


def clique_pendants(t,count,shift=0):
    integer_at_least(t,3,'Clique order')
    D,M,s = base.uniform_rank_two_certificate(t)
    return certificate(D,base.extract_core(M,s),0,count,shift)


def friendship_pendants(k,count,shift=0):
    integer_at_least(k,1,'Triangle count')
    D,M,s = friendship.certificate(k)
    return certificate(D,base.extract_core(M,s),2*k,count,shift)


def clique_center_pendants(r,t,count,shift=0):
    return certificate(clique_centers.family(r,t),clique_centers.core(r,t),0,count,shift)
