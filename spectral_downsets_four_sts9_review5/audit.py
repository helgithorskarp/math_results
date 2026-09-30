"""Independent four-STS(9) audit, six-reviewer-5, stdlib Python 3.11.

No author code imports. The external rational seed is pinned by SHA-256.
All proof checks use explicit exceptions, including under python -O.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations
import json
from math import lcm
from pathlib import Path
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(x):
    return sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()


def mask(a):
    return sum(1 << i for i in a)


def moved(a, p):
    return sum(1 << p[i] for i in range(len(p)) if a & (1 << i))


def image(U, p):
    return tuple(sorted(moved(a, p) for a in U))


def isomorphisms(U, V, n=9):
    """Exhaustive partial point maps, pruning only decided triple incidence.

    Every bijection extends one branch. At depth k, all triples on assigned
    points have equal incidence. At depth n this is exactly isomorphism.
    """
    U, V = set(U), set(V)
    result = []
    def visit(p, remaining):
        k = len(p)
        if not remaining:
            result.append(tuple(p))
            return
        constraints = [(i, j, ((1 << i) | (1 << j) | (1 << k)) in U)
                       for i, j in combinations(range(k), 2)]
        for x in remaining:
            if all((((1 << p[i]) | (1 << p[j]) | (1 << x)) in V) == yes
                   for i, j, yes in constraints):
                visit(p + [x], remaining - {x})
    visit([], set(range(n)))
    return sorted(result)


def all_systems():
    """MRV exact cover of the 36 pairs by 84 triples, without symmetry cuts."""
    pairs = list(combinations(range(9), 2))
    pair_index = {p: i for i, p in enumerate(pairs)}
    triples = [mask(t) for t in combinations(range(9), 3)]
    boards = []
    for a in triples:
        pts = [i for i in range(9) if a & (1 << i)]
        boards.append(sum(1 << pair_index[p] for p in combinations(pts, 2)))
    by_pair = [[j for j, b in enumerate(boards) if b & (1 << i)] for i in range(36)]
    systems = set()
    def visit(free, picked):
        if not free:
            systems.add(tuple(sorted(triples[j] for j in picked)))
            return
        opts = min(([j for j in by_pair[i] if boards[j] & free == boards[j]]
                    for i in range(36) if free & (1 << i)), key=len)
        for j in opts:
            visit(free ^ boards[j], picked + [j])
    visit((1 << 36) - 1, [])
    require(len(systems) == 840, 'STS enumeration')
    return sorted(systems), triples


def sts(U):
    require(len(U) == len(set(U)) == 12, 'system block count')
    require(all(0 < a < 512 and a.bit_count() == 3 for a in U), 'bad block')
    require(all(sum(a & mask(p) == mask(p) for a in U) == 1
                for p in combinations(range(9), 2)), 'pair multiplicity')


def board(U, triple_index):
    return sum(1 << triple_index[a] for a in U)


def decompositions(U, systems):
    contained = [t for t in systems if set(t) <= set(U)]
    covers = []
    for cs in combinations(contained, 4):
        if len(set().union(*map(set, cs))) == 48:
            covers.append(cs)
    return contained, covers


def census(cases):
    systems, triples = all_systems()
    # Numeric-mask order is the public comparison format. Enumeration itself
    # uses combination order; this bridge permits exact entry-set hashes.
    index = {a: i for i, a in enumerate(sorted(triples))}
    first = tuple(cases[0]['layers'][0])
    sts(first)
    # Regenerate all 9! point images. Check exact-cover equality, not counts.
    transport = {}
    stabilizer = []
    first_triples = [[i for i in range(9) if a & (1 << i)] for a in first]
    for p in permutations(range(9)):
        t = tuple(sorted(sum(1 << p[i] for i in pts) for pts in first_triples))
        transport.setdefault(t, p)
        if t == first:
            stabilizer.append(p)
    require(set(transport) == set(systems), 'orbit/exact-cover mismatch')
    require(len(stabilizer) == 432, 'first stabilizer')
    fixed = board(first, index)
    candidates = [board(t, index) for t in systems if set(t).isdisjoint(first)]
    require(len(candidates) == 192, 'disjoint candidates')
    # Three-cliques in the full disjointness graph, retaining decomposition
    # multiplicities. Bitset common-neighbor enumeration differs from the
    # author's parent extension/canonical-key generator.
    neigh = []
    for i, a in enumerate(candidates):
        neigh.append(sum(1 << j for j in range(i + 1, len(candidates))
                         if a & candidates[j] == 0))
    direct = Counter()
    for i, a in enumerate(candidates):
        rest = neigh[i]
        while rest:
            bbit = rest & -rest
            j = bbit.bit_length() - 1
            rest -= bbit
            third = rest & neigh[j]
            while third:
                cbit = third & -third
                k = cbit.bit_length() - 1
                third -= cbit
                direct[fixed | a | candidates[j] | candidates[k]] += 1
    covered = set()
    unions, details, groups = [], [], []
    for ci, case in enumerate(cases):
        layers = [tuple(t) for t in case['layers']]
        require(len(layers) == 4 and layers[0] == first, 'four input layers')
        for t in layers:
            sts(t)
        U = tuple(sorted(set().union(*map(set, layers))))
        require(len(U) == 48, 'layers not block disjoint')
        require(all(not isomorphisms(U, W) for W in unions), 'duplicate union type')
        group = isomorphisms(U, U)
        require(len(group) == case['full_automorphism_order'], 'full group mismatch')
        contained, decs = decompositions(U, systems)
        participating = set(t for dec in decs for t in dec)
        require(tuple(sorted(layers)) in decs, 'missing given decomposition')
        for t in participating:
            p = transport[t]
            inv = tuple(p.index(i) for i in range(9))
            normalized = image(U, inv)
            for g in stabilizer:
                covered.add(board(image(normalized, g), index))
        details.append({'case': ci, 'group_order': len(group),
                        'contained_systems': len(contained), 'decompositions': len(decs),
                        'participating_systems': len(participating)})
        unions.append(U)
        groups.append(group)
    require(set(direct) == covered and len(direct) == 10048, 'incomplete union coverage')
    labelled = sum(362880 // d['group_order'] for d in details)
    weighted = sum((362880 // d['group_order']) * d['decompositions'] for d in details)
    require(weighted * 4 == 840 * sum(direct.values()), 'decomposition double count')
    return unions, groups, {'labelled_STS9': 840, 'first_stabilizer_order': 432,
                            'fixed_first_candidates': 192, 'fixed_first_unions': len(direct),
                            'fixed_first_decompositions': sum(direct.values()),
                            'fixed_first_union_sha256': digest(sorted(direct)),
                            'labelled_unions': labelled, 'labelled_decompositions': weighted,
                            'union_types': details}


def decode(case, U, group):
    D = sorted([0] + [1 << i for i in range(9)] +
               [mask(p) for p in combinations(range(9), 2)] + list(U),
               key=lambda a: (a.bit_count(), a))
    require(len(D) == 94, 'downset size')
    # Assign a canonical key to every actual supported pair. No seed-orbit
    # expansion, coset group reconstruction or author indexing is imported.
    maps = [{a: moved(a, p) for a in D} for p in group]
    keys = {}
    for i, a in enumerate(D):
        for b in D[i:]:
            if a & b == 0:
                keys[a, b] = min(tuple(sorted((mp[a], mp[b]))) for mp in maps)
    reps = sorted(set(keys.values()))
    nums = case['orbit_numerators']
    den = case['denominator']
    require(type(den) is int and den > 0 and len(nums) == len(reps), 'orbit encoding')
    require(all(type(x) is int for x in nums), 'noninteger numerator')
    weights = dict(zip(reps, (F(x, den) for x in nums)))
    Q = [[F(25 if i == j and a else 0) for j in range(94)] for i, a in enumerate(D)]
    for i, a in enumerate(D):
        for j in range(i, 94):
            b = D[j]
            if not a & b:
                Q[i][j] = Q[j][i] = weights[keys[a, b]]
    require(matrix_hash(Q) == case['centered_matrix_sha256'], 'matrix hash')
    return D, Q, len(reps)


def matrix_hash(A):
    return digest([[str(x) for x in row] for row in A])


def definitions(D, Q):
    n = len(D)
    require(len(Q) == n and all(len(row) == n for row in Q), 'matrix dimensions')
    require(all(sum(bool(a & (1 << i)) for a in D) == 25 for i in range(9)), 'star size')
    require(all(sum(row) == n for row in Q), 'row sum')
    for i, a in enumerate(D):
        for j, b in enumerate(D):
            require(Q[i][j] == Q[j][i], 'asymmetry')
            if a & b:
                require(Q[i][j] == (25 if i == j else 0), 'unsupported entry')
        for k in range(9):
            require(sum(Q[i][j] for j, b in enumerate(D) if b & (1 << k)) == 25,
                    'star kernel equation')


def integer_psd_rank(Q):
    """Fraction-free symmetric elimination, no permutations or floats.

    A positive pivot replaces the residual by (d A_ij-A_i0 A_0j)/prev.
    Bareiss exact division holds; the residual is a positive multiple of
    the rational Schur complement. A zero pivot can be skipped precisely
    when its complete residual row vanishes. A negative pivot, zero pivot
    with nonzero row, or inexact division rejects the certificate.
    """
    require(all(len(row) == len(Q) for row in Q), 'PSD matrix dimensions')
    require(all(Q[i][j] == Q[j][i] for i in range(len(Q)) for j in range(len(Q))),
            'PSD matrix not symmetric')
    scale = lcm(*(x.denominator for row in Q for x in row))
    A = [[int(x * scale) for x in row] for row in Q]
    previous = 1
    rank = 0
    for k in range(len(A)):
        d = A[k][k]
        require(d >= 0, 'negative elimination pivot')
        if d == 0:
            require(all(A[k][j] == 0 for j in range(k, len(A))), 'zero pivot nonzero row')
            continue
        for i in range(k + 1, len(A)):
            for j in range(i, len(A)):
                value = d * A[i][j] - A[i][k] * A[k][j]
                q, r = divmod(value, previous)
                require(r == 0, 'inexact Bareiss division')
                A[i][j] = A[j][i] = q
        previous = d
        rank += 1
    return rank


def upper(Q, delta=F(0)):
    n = len(Q)
    return [[F(n if i == j else 0) - Q[i][j] -
             delta * (F(i == j) - F(1, n)) for j in range(n)] for i in range(n)]


def ordinary(D, layers):
    """Fresh layer formula, separately checked against defining equations."""
    n, s = 94, 25
    layer_of = {a: k + 2 for k, t in enumerate(layers) for a in t}
    def layer(a):
        return a.bit_count() - 1 if a.bit_count() < 3 else layer_of[a]
    qs = {a: F(n) - F(s * 9, a.bit_count()) for a in D if a}
    q00 = (qs[1] ** 2 + 8 * qs[3] ** 2 + 16 * qs[layers[0][0]] ** 2) / s
    Q = []
    for a in D:
        row = []
        for b in D:
            if not a and not b:
                x = q00
            elif not a or not b:
                x = qs[a or b]
            elif a == b:
                x = F(s)
            elif a & b or layer(a) != layer(b):
                x = F(0)
            else:
                x = {1: F(25), 2: F(25, 6), 3: F(25)}[a.bit_count()]
            row.append(x)
        Q.append(row)
    definitions(D, Q)
    require(Q[0][0] == 1027 and sum(Q[i][i] for i in range(n)) == 3352,
            'ordinary trace')
    return Q


def rejected(fn):
    try:
        fn()
    except ValueError:
        return
    raise ValueError('negative control accepted')


def run(args):
    raw = args.input.read_bytes()
    require(sha256(raw).hexdigest() == args.input_sha256, 'external seed hash')
    data = json.loads(raw)
    require((data['N'], data['s'], len(data['cases'])) == (94, 25, 12), 'input parameters')
    start = time.monotonic()
    unions, groups, cov = census(data['cases'])
    print('Complete independent census', cov['fixed_first_unions'], flush=True)
    records = []
    gap = F(16)
    for ci, (case, U, group) in enumerate(zip(data['cases'], unions, groups)):
        D, Q, orbits = decode(case, U, group)
        definitions(D, Q)
        require(all(x == 1 for x in Q[0]), 'centered empty column')
        ranks = [integer_psd_rank(Q), integer_psd_rank(upper(Q, F(1, 2)))]
        require(ranks == [84, 93], 'original endpoint ranks')
        # Consequential strengthening: one fixed new uniform margin, no
        # floating eigenvalue search or tolerance is used.
        gap_rank = integer_psd_rank(upper(Q, gap))
        require(gap_rank == 93, 'stronger centered margin')
        Qo = ordinary(D, case['layers'])
        require(integer_psd_rank(Qo) == 45, 'ordinary lower rank')
        eps0 = F(1, 13408)
        original = [[(1 - eps0) * x + eps0 * y for x, y in zip(row, other)]
                    for row, other in zip(Q, Qo)]
        definitions(D, original)
        require(integer_psd_rank(original) == 85 and
                integer_psd_rank(upper(original, F(1, 4))) == 93, 'original repair')
        eps = gap / (2 * 3352)
        improved = [[(1 - eps) * x + eps * y for x, y in zip(row, other)]
                    for row, other in zip(Q, Qo)]
        definitions(D, improved)
        rr = integer_psd_rank(improved)
        ur = integer_psd_rank(upper(improved, gap / 2))
        require((rr, ur) == (85, 93), 'improved repair')
        records.append({'case': ci, 'supported_pair_orbits': orbits,
                        'centered_matrix_sha256': matrix_hash(Q),
                        'ordinary_matrix_sha256': matrix_hash(Qo),
                        'original_repaired_matrix_sha256': matrix_hash(original),
                        'improved_matrix_sha256': matrix_hash(improved),
                        'ranks_Qc_half_gap_gap16_Qo_original_original_gap':
                        ranks + [gap_rank, 45, 85, 93],
                        'improved_lower_rank': rr, 'improved_gap8_slack_rank': ur})
        print('Checked type', ci, 'gap16 and repaired gap8', flush=True)
    bad = [row[:] for row in Q]
    bad[0][1] += 1
    rejected(lambda: definitions(D, bad))
    rejected(lambda: integer_psd_rank([[F(0), F(1)], [F(1), F(0)]]))
    rejected(lambda: integer_psd_rank([[F(-1)]]))
    rejected(lambda: sts(case['layers'][0][:-1]))
    require(integer_psd_rank([[F(0), F(0)], [F(0), F(2)]]) == 1, 'skip zero pivot')
    require(integer_psd_rank([[F(2), F(2)], [F(2), F(2)]]) == 1, 'singular PSD control')
    require(integer_psd_rank([[F(2), F(1)], [F(1), F(2)]]) == 2, 'PD control')
    output = {'reviewer': 'six-reviewer-5', 'role': 'independent mathematical reviewer',
              'input_sha256': sha256(raw).hexdigest(), 'coverage': cov, 'matrices': records,
              'new_centered_gap': '16', 'new_epsilon': '1/419', 'new_repaired_gap': '8',
              'new_nonconstant_M_upper': '61/69', 'negative_controls': 4,
              'positive_arithmetic_controls': 3}
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + '\n')
    print('Completed', round(time.monotonic() - start, 3), 'seconds', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--input-sha256', required=True)
    parser.add_argument('--output', type=Path, required=True)
    run(parser.parse_args())
