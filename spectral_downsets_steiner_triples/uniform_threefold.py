"""Completion-sensitive capped H for simple2-(v,3,3), v>=13.

Rational constructor only; no search, floating eigenvalues or CAS. The complete
proof is UNIFORM_THREEFOLD_PROOF.md. Author: six-downset-2, researcher.
The predecessor is the credited uniform_twofold.py completion-sensitive formula.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from certificates import mask, ordered, check_sts


def weights(v):
    assert isinstance(v, int) and v >= 13 and v % 2 == 1
    return {'a': F(-1),
            'w': F(v**3-6*v*v+23*v-36, (v-4)*(v-3)*(v-2)),
            'c': F(v*v-6*v+11, (v-3)*(v-2)),
            'd': F(v*v-v-4, (v-4)*(v-3)),
            'h': F(v*v+2*v-11, (v-5)*(v-3)), 't': F(v-1, v-5)}


def design_data(v, blocks):
    """Every pair has exactly three distinct completing points; no duplicates."""
    assert isinstance(v, int) and v >= 13 and v % 2 == 1
    assert len(set(blocks)) == len(blocks)
    pairs = [mask(p) for p in combinations(range(v), 2)]
    completing = {p: [] for p in pairs}
    for block in blocks:
        assert isinstance(block, int) and 0 < block < 1 << v and block.bit_count() == 3
        points = [x for x in range(v) if block >> x & 1]
        for pair in combinations(points, 2):
            p = mask(pair)
            completing[p].append(block ^ p)
    assert all(len(xs) == len(set(xs)) == 3 for xs in completing.values()), 'simple threefold design required'
    assert len(blocks) == len(pairs)
    codegrees = Counter()
    for xs in completing.values():
        codegrees.update(x | y for x, y in combinations(xs, 2))
    outside = {}
    for block in blocks:
        counts = Counter()
        points = [x for x in range(v) if block >> x & 1]
        for pair in combinations(points, 2):
            for x in completing[mask(pair)]:
                if not x & block:
                    counts[x.bit_length()-1] += 1
        assert sum(counts.values()) == 6
        outside[block] = counts
    return pairs, completing, codegrees, outside


def centered_certificate(v, blocks):
    pairs, _, codegrees, outside = design_data(v, blocks)
    w = weights(v)
    D = ordered({0} | {1 << x for x in range(v)} | set(pairs) | set(blocks))
    N, s = len(D), (5*v-3)//2
    assert N == v*v+1
    U = set(blocks)
    Q = [[F(0)]*N for _ in D]
    for i, a in enumerate(D):
        for j in range(i, N):
            b = D[j]
            if a & b:
                value = F(s if i == j else 0)
            elif not a or not b:
                value = F(1)
            else:
                ka, kb = a.bit_count(), b.bit_count()
                if ka > kb:
                    a0, b0, ka, kb = b, a, kb, ka
                else:
                    a0, b0 = a, b
                if (ka, kb) == (1, 1):
                    value = w['a']+w['t']*(codegrees[a0 | b0]-3)
                elif (ka, kb) == (1, 2):
                    value = w['w']-w['d']*int(a0 | b0 in U)
                elif (ka, kb) == (1, 3):
                    value = w['h']-w['t']*outside[b0].get(a0.bit_length()-1, 0)
                elif (ka, kb) == (2, 2):
                    value = w['c']
                elif (ka, kb) == (2, 3):
                    value = w['d']
                else:
                    assert (ka, kb) == (3, 3)
                    value = w['t']
            Q[i][j] = Q[j][i] = value
    return D, s, Q


def gap(v):
    weights(v)
    delta = F(2*v*v-25*v+2, 2)
    assert delta > 0
    return delta


def maximal_certificate(v, blocks, centered=None):
    """Prior full-two-skeleton sparse trade; explicit smaller perturbation."""
    if centered is None:
        centered = centered_certificate(v, blocks)
    D, s, Qc = centered
    assert s == (5*v-3)//2 and len(D) == v*v+1
    m, k = v*(v-1)//2, (v-2)*(v-3)//2
    eta = gap(v)/(16*m*k)
    assert 0 < eta < F(1, 2*v*v)
    Qm = [row[:] for row in Qc]
    for i, a in enumerate(D):
        for j in range(i, len(D)):
            b = D[j]
            if a & b:
                change = 0
            elif not a and not b:
                change = m*k
            elif not a or not b:
                size = (a | b).bit_count()
                change = -(v-1)*k if size == 1 else (k if size == 2 else 0)
            else:
                sizes = sorted((a.bit_count(), b.bit_count()))
                change = 2*k if sizes == [1, 1] else (-(v-3) if sizes == [1, 2]
                                                      else (1 if sizes == [2, 2] else 0))
            Qm[i][j] = Qm[j][i] = Qc[i][j]+eta*change
    return D, s, Qm, eta


def fixtures():
    """Three literal inputs, including a non-STS-decomposable design; no census."""
    seeds = [(0, 1, 2), (0, 1, 4), (0, 2, 6), (0, 2, 7), (0, 3, 7), (0, 3, 8)]
    blocks = sorted({mask((x+j) % 13 for x in seed) for seed in seeds for j in range(13)})
    design_data(13, blocks)
    yield 'cyclic13', 13, blocks, {'modulus': 13, 'seeds': [list(p) for p in seeds]}
    seeds = [(0, 1, 3), (0, 1, 9), (0, 3, 9), (1, 3, 9), (0, 1, 4), (0, 2, 7)]
    blocks = sorted({mask((x+j) % 13 for x in seed) for seed in seeds for j in range(13)})
    design_data(13, blocks)
    # These four faces pairwise share a pair, so require four STS colours.
    tetrahedron = [0, 1, 3, 9]
    assert all(mask(face) in blocks for face in combinations(tetrahedron, 3))
    yield 'nondecomposable13', 13, blocks, {'modulus': 13, 'seeds': [list(p) for p in seeds],
                                         'tetrahedron_witness': tetrahedron}
    first = sorted({mask((a-1, b-1, (a ^ b)-1)) for a, b in combinations(range(1, 16), 2)})
    permutations = [list(range(15)), [9, 2, 14, 11, 12, 5, 10, 1, 8, 3, 6, 0, 7, 13, 4],
                    [1, 13, 12, 10, 6, 14, 3, 0, 8, 11, 5, 7, 4, 9, 2]]
    systems = []
    for perm in permutations:
        system = sorted(mask(perm[x] for x in range(15) if a >> x & 1) for a in first)
        check_sts(15, system)
        assert all(set(system).isdisjoint(old) for old in systems)
        systems.append(system)
    blocks = sorted(a for system in systems for a in system)
    design_data(15, blocks)
    yield 'three_STS15', 15, blocks, {'first': 'projective F2^4 triples {a,b,a+b}, labelled a-1',
                                    'permutations': permutations}
