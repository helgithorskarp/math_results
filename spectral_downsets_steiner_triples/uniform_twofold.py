"""Completion-sensitive capped H construction for every simple 2-(v,3,2).

The all-orders proof is UNIFORM_TWOFOLD_PROOF.md. Standard library only;
no search, numerical eigensolver or CAS is part of this constructor.
Author: six-downset-2, researcher.
"""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter

from certificates import check_sts, mask, ordered, steiner_certificate
from field_family import field_downset


def weights(v):
    assert isinstance(v, int) and v >= 13
    den = (v-3)*(v-4)
    return {'a': F(-2, 3),
            'b': F(1)+F(4*v*(2*v-5), 3*(v-2)*den),
            'c': F(1)+F(4, 3*(v-2)*(v-3)),
            'd': F(v*v-v-4, den),
            'h': F(v*v-7, den), 't': F(v-1, v-4)}


def design_data(v, blocks):
    """Check every input block and every pair's two distinct completing points."""
    assert isinstance(v, int) and v >= 13
    assert len(set(blocks)) == len(blocks)
    pairs = [mask(p) for p in combinations(range(v), 2)]
    completing = {p: [] for p in pairs}
    for block in blocks:
        assert isinstance(block, int) and 0 < block < 1 << v
        assert block.bit_count() == 3
        points = [i for i in range(v) if block >> i & 1]
        for p in combinations(points, 2):
            pair = mask(p)
            completing[pair].append(block ^ pair)
    assert all(len(xs) == 2 and xs[0] != xs[1]
               for xs in completing.values()), 'simple twofold design required'
    completion = {p: xs[0] | xs[1] for p, xs in completing.items()}
    outside = {}
    for block in blocks:
        counts = {}
        points = [i for i in range(v) if block >> i & 1]
        for p in combinations(points, 2):
            for x in completing[mask(p)]:
                if not x & block:
                    point = x.bit_length()-1
                    counts[point] = counts.get(point, 0)+1
        assert sum(counts.values()) == 3
        outside[block] = counts
    return pairs, completion, outside


def centered_certificate(v, blocks):
    pairs, completion, outside = design_data(v, blocks)
    w = weights(v)
    D = ordered({0} | {1 << i for i in range(v)} | set(pairs) | set(blocks))
    n, s = len(D), 2*v-1
    assert n == (5*v*v+v+6)//6
    block_set = set(blocks)
    completion_counts = Counter(completion.values())
    zero, one, diagonal = F(0), F(1), F(s)
    Q = [[zero]*n for _ in D]
    for i, a in enumerate(D):
        for j in range(i, n):
            b = D[j]
            if a & b:
                value = diagonal if i == j else zero
            elif not a or not b:
                value = one
            else:
                ka, kb = a.bit_count(), b.bit_count()
                if ka > kb:
                    a0, b0, ka, kb = b, a, kb, ka
                else:
                    a0, b0 = a, b
                if (ka, kb) == (1, 1):
                    value = w['a']+w['t']*(completion_counts[a0 | b0]-1)
                elif (ka, kb) == (1, 2):
                    value = w['b']-w['d']*int(a0 | b0 in block_set)
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
    assert isinstance(v, int) and v >= 13
    delta = F(5*v*v-41*v+6, 6)
    assert delta > 0
    return delta


def maximal_certificate(v, blocks, centered=None):
    """Uniform pair-layer perturbation: no Steiner decomposition required."""
    if centered is None:
        centered = centered_certificate(v, blocks)
    D, s, Qc = centered
    assert s == 2*v-1 and len(D) == (5*v*v+v+6)//6
    m, k = v*(v-1)//2, (v-2)*(v-3)//2
    eta = gap(v)/(8*m*k)
    assert 0 < eta < F(1, v*v)
    Qr = [row[:] for row in Qc]
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
            Qr[i][j] = Qr[j][i] = Qc[i][j]+eta*change
    return D, s, Qr, eta


def nonbijective_fixture(v):
    """Two literal labelled validation inputs, not a census of all designs."""
    if v == 13:
        first, second = prime_decomposition(13)[3]
        perm = [10, 6, 4, 12, 9, 3, 5, 1, 11, 7, 8, 0, 2]
    else:
        assert v == 15
        first = sorted({mask((a-1, b-1, (a ^ b)-1))
                        for a, b in combinations(range(1, 16), 2)})
        second = first
        perm = [9, 2, 14, 11, 12, 5, 10, 1, 8, 3, 6, 0, 7, 13, 4]
    moved = sorted(mask(perm[x] for x in range(v) if block >> x & 1)
                   for block in second)
    check_sts(v, first)
    check_sts(v, moved)
    assert set(first).isdisjoint(moved)
    blocks = sorted(set(first) | set(moved))
    pairs, completion, _ = design_data(v, blocks)
    assert len(set(completion.values())) < len(pairs)
    return blocks, perm


def repaired_certificate(v, systems, centered=None):
    """Requires a supplied decomposition into two block-disjoint STS(v)."""
    assert len(systems) == 2
    Do, so, Qo = steiner_certificate(v, systems)
    if centered is None:
        centered = centered_certificate(v, sorted(set(systems[0]) | set(systems[1])))
    D, s, Qc = centered
    assert (D, s) == (Do, so)
    trace = sum(Qo[i][i] for i in range(len(D)))
    epsilon = gap(v)/(2*trace)
    assert 0 < epsilon < 1
    Qr = [[(1-epsilon)*Qc[i][j]+epsilon*Qo[i][j] for j in range(len(D))]
          for i in range(len(D))]
    return D, s, Qr, Qo, epsilon, trace


def prime_decomposition(p):
    """One deterministic two-STS decomposition, not an exponential census."""
    D, roots = field_downset(p)
    blocks = [a for a in D if a.bit_count() == 3]
    rho = roots[0]
    remaining = set(range(1, p))
    systems = [set(), set()]
    while remaining:
        d = min(remaining)
        coset = {d*pow(rho, k, p) % p for k in range(6)}
        assert len(coset) == 6 and coset <= remaining
        remaining -= coset
        for j, step in enumerate((d, (-d) % p)):
            systems[j].update(mask((x, (x+step) % p, (x+rho*step) % p))
                              for x in range(p))
    systems = [sorted(system) for system in systems]
    for system in systems:
        check_sts(p, system)
    assert set(systems[0]).isdisjoint(systems[1])
    assert set(systems[0]) | set(systems[1]) == set(blocks)
    return D, roots, blocks, systems


def binary_field16():
    """F16=F2[X]/(X^4+X+1), with elements encoded by four bits."""
    def multiply(a, b):
        out = 0
        while b:
            if b & 1:
                out ^= a
            b >>= 1
            a <<= 1
            if a & 16:
                a ^= 0b10011
        return out

    # Multiplication in the displayed quotient, and absence of zero divisors.
    assert all({multiply(a, b) for b in range(16)} == set(range(16))
               for a in range(1, 16))
    roots = [r for r in range(16) if multiply(r, r) ^ r ^ 1 == 0]
    assert len(roots) == 2
    families = [{mask((x, x ^ d, x ^ multiply(r, d)))
                 for x in range(16) for d in range(1, 16)} for r in roots]
    assert families[0] == families[1]
    blocks = sorted(families[0])
    design_data(16, blocks)
    return roots, blocks
