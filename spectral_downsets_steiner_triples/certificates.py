"""Exact weighted-Hoffman matrices; Python 3.11+, standard library only.

Sets are nonnegative integer masks, bit i denotes point i. Matrices use
Fraction throughout. Q=(N-s)M+sI is returned in cardinality/mask order.
"""
from fractions import Fraction as F
from itertools import combinations, product


def mask(points):
    return sum(1 << p for p in points)


def ordered(sets):
    return sorted(sets, key=lambda a: (a.bit_count(), a))


def check_sts(v, blocks):
    if v < 3 or len(set(blocks)) != len(blocks):
        raise ValueError("require distinct triples on v>=3 points")
    counts = {mask(p): 0 for p in combinations(range(v), 2)}
    for a in blocks:
        if a < 0 or a >= 1 << v or a.bit_count() != 3:
            raise ValueError("malformed triple")
        for p in combinations([i for i in range(v) if a & (1 << i)], 2):
            counts[mask(p)] += 1
    if any(x != 1 for x in counts.values()):
        raise ValueError("every pair must belong to exactly one block")


def downset(v, systems):
    triples = set()
    for blocks in systems:
        check_sts(v, blocks)
        if triples.intersection(blocks):
            raise ValueError("the systems must be block-disjoint")
        triples.update(blocks)
    if not systems:
        raise ValueError("at least one system is required")
    return ordered({0} | {1 << i for i in range(v)} |
                   {mask(p) for p in combinations(range(v), 2)} | triples)


def complement_cube(v):
    if v < 1:
        raise ValueError("nontrivial cube required")
    D = ordered(range(1 << v))
    s = 1 << (v - 1)
    full = (1 << v) - 1
    Q = [[F(s * ((a == b) + (a ^ b == full))) for b in D] for a in D]
    return D, s, Q


def steiner_certificate(v, systems):
    """Construction for any block-disjoint list of STS(v), v>=9."""
    if v < 9:
        raise ValueError("the layered formula requires v>=9")
    D = downset(v, systems)
    n = len(D)
    r = F(v - 1, 2)
    s = F(v) + len(systems) * r
    assert s.denominator == 1
    s = int(s)
    layers = [(1, F(1), [1 << i for i in range(v)], F(s))]
    layers.append((2, F(v - 1), [mask(p) for p in combinations(range(v), 2)], F(s, v - 3)))
    layers.extend((3, r, list(blocks), F(2 * s, v - 7)) for blocks in systems)
    pos = {a: i for i, a in enumerate(D)}
    Q = [[F(0) for _ in D] for _ in D]
    for k, t, members, edge_weight in layers:
        q = F(n) - F(s * v, k)
        Q[0][0] += t * q * q / s
        for a in members:
            i = pos[a]
            Q[0][i] = Q[i][0] = q
            for b in members:
                j = pos[b]
                if a == b:
                    Q[i][j] = F(s)
                elif not a & b:
                    Q[i][j] = edge_weight
    return D, s, Q


def fano_blocks():
    """Nonzero vectors of F_2^3 are labelled 0..6 by integer vector minus1."""
    return sorted({mask((a - 1, b - 1, (a ^ b) - 1))
                   for a, b in combinations(range(1, 8), 2)})


def fano_certificate(balanced=True):
    """Eleven rational orbit weights. Default also satisfies Q<=36I.

    balanced=False reproduces the initial rank29 certificate; the strengthened
    default has rank28 and makes tensor-product closure applicable.
    """
    blocks = set(fano_blocks())
    D = downset(7, [list(blocks)])
    full = (1 << 7) - 1
    w = ([22, -2, 0, 4, 0, 2, F(3, 2), 1, F(1, 2), 4, 3]
         if balanced else [22, -5, 2, 1, 2, 1, F(1, 2), F(5, 2), 1, 4, F(5, 2)])
    Q = [[F(0) for _ in D] for _ in D]
    for i, a in enumerate(D):
        for j, b in enumerate(D):
            if a & b:
                Q[i][j] = F(10 if a == b else 0)
            elif a == b == 0:
                Q[i][j] = F(w[0])
            elif not a or not b:
                Q[i][j] = F(w[(a | b).bit_count()])
            else:
                sizes = sorted((a.bit_count(), b.bit_count()))
                if sizes == [1, 1]:
                    Q[i][j] = F(w[4])
                elif sizes == [1, 2]:
                    Q[i][j] = F(w[5] if (a | b) in blocks else w[6])
                elif sizes == [1, 3]:
                    Q[i][j] = F(w[7])
                elif sizes == [2, 2]:
                    Q[i][j] = F(w[9] if (full ^ (a | b)) in blocks else w[8])
                elif sizes == [2, 3]:
                    Q[i][j] = F(w[10])
                else:
                    raise AssertionError("distinct Fano blocks cannot be disjoint")
    return D, 10, Q


def normalized(D, s, Q):
    n = len(D)
    return [[(Q[i][j] - (s if i == j else 0)) / (n - s)
             for j in range(n)] for i in range(n)]


def affine_sts9():
    pts = list(product(range(3), repeat=2))
    idx = {p: i for i, p in enumerate(pts)}
    return sorted({mask(idx[((p[0] + t * d[0]) % 3,
                            (p[1] + t * d[1]) % 3)] for t in range(3))
                   for p in pts for d in pts if d != (0, 0)})


def cyclic_sts13():
    return sorted({mask((x + t) % 13 for x in base)
                   for base in ((0, 1, 4), (0, 2, 7)) for t in range(13)})
