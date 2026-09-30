"""Exact invariant-space PSD and rank reduction for the full affine group.

The indexed sets are subsets of F_p, p prime, closed under every affine map.
Q must be real symmetric and affine-equivariant. AFFINE_REDUCTION.md proves
that positivity is equivalent to its restrictions to translation-fixed and
multiplication-fixed spaces. All arithmetic here is Fraction or integer.
"""
from fractions import Fraction as F
from math import isqrt

from verify import exact_psd_rank, relabel


def affine_maps(p):
    assert isinstance(p, int) and p >= 2
    assert all(p % d for d in range(2, isqrt(p)+1)), 'prime required'
    return [tuple((a*x+b) % p for x in range(p))
            for a in range(1, p) for b in range(p)]


def orbit_partition(D, maps):
    idx = {a: i for i, a in enumerate(D)}
    assert len(idx) == len(D)
    actions = [[idx[relabel(a, g)] for a in D] for g in maps]
    remaining = set(range(len(D)))
    parts = []
    while remaining:
        i = min(remaining)
        part = {g[i] for g in actions}
        assert part <= remaining
        parts.append(sorted(part))
        remaining -= part
    return parts


def invariant_partitions(D, p):
    assert all(isinstance(a, int) and 0 <= a < 1 << p for a in D)
    G = affine_maps(p)
    T = [tuple((x+b) % p for x in range(p)) for b in range(p)]
    H = [tuple(a*x % p for x in range(p)) for a in range(1, p)]
    return {'T': orbit_partition(D, T), 'H': orbit_partition(D, H),
            'G': orbit_partition(D, G)}


def check_equivariance(D, p, Q):
    affine_maps(p)  # Check the prime-order hypothesis.
    assert all(isinstance(a, int) and 0 <= a < 1 << p for a in D)
    assert len(Q) == len(D) and all(len(row) == len(D) for row in Q)
    assert all(Q[i][j] == Q[j][i] for i in range(len(D)) for j in range(len(D)))
    idx = {a: i for i, a in enumerate(D)}
    # Translations and all multiplications generate the full affine group.
    maps = [tuple((x+1) % p for x in range(p))]
    maps += [tuple(a*x % p for x in range(p)) for a in range(1, p)]
    for g in maps:
        action = [idx[relabel(a, g)] for a in D]
        assert all(Q[action[i]][action[j]] == Q[i][j]
                   for i in range(len(D)) for j in range(len(D))), 'not affine-equivariant'


def compression(Q, parts):
    """C^T Q C in the basis of disjoint orbit indicators, without rounding."""
    return [[sum((Q[i][j] for i in a for j in b), F(0))
             for b in parts] for a in parts]


def affine_psd_rank(D, p, Q, parts=None):
    """Exact PSD and full rank, trusting the written invariant-space bridge."""
    check_equivariance(D, p, Q)
    if parts is None:
        parts = invariant_partitions(D, p)
    ranks = {k: exact_psd_rank(compression(Q, part)) for k, part in parts.items()}
    rank = ranks['T'] + (p-1)*(ranks['H']-ranks['G'])
    assert 0 <= rank <= len(D)
    return rank, ranks
