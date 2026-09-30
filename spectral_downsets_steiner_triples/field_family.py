"""Exact input construction/counts for prime equilateral twofold designs.

This constructs designs and fixed-space dimension formulas, not H matrices.
The uniform proof is in FIELD_FAMILY_COUNTS.md. Standard library only.
"""
from itertools import combinations
from math import isqrt

from certificates import mask


def prime_field_order(p):
    assert isinstance(p, int) and p >= 7 and p % 6 == 1
    assert all(p % d for d in range(2, isqrt(p)+1)), 'prime required'


def field_counts(p):
    prime_field_order(p)
    return {'p': p, 'blocks': p*(p-1)//3,
            'N': (5*p*p+p+6)//6, 's': 2*p-1,
            'affine_subgroup_order': p*(p-1),
            'fixed_space_dimensions': {'T': (5*p+7)//6,
                                       'H': (5*p+25)//6, 'G': 4},
            'centered_complement_dimensions': {'T': (5*p-11)//6,
                                              'H': (5*p+1)//6}}


def field_downset(p):
    prime_field_order(p)
    roots = [rho for rho in range(p) if (rho*rho-rho+1) % p == 0]
    assert len(roots) == 2
    families = [{mask((x, (x+d) % p, (x+rho*d) % p))
                 for x in range(p) for d in range(1, p)} for rho in roots]
    assert families[0] == families[1]
    U = families[0]
    pairs = [mask(a) for a in combinations(range(p), 2)]
    counts = dict.fromkeys(pairs, 0)
    for block in U:
        pts = [i for i in range(p) if block >> i & 1]
        assert len(pts) == 3
        for pair in combinations(pts, 2):
            counts[mask(pair)] += 1
    assert set(counts.values()) == {2}
    D = sorted({0} | {1 << i for i in range(p)} | set(pairs) | U,
               key=lambda a: (a.bit_count(), a))
    expected = field_counts(p)
    assert len(U) == expected['blocks'] and len(D) == expected['N']
    assert all(sum(bool(a >> i & 1) for a in D) == expected['s'] for i in range(p))
    return D, roots
