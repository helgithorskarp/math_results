"""Independent two-STS(9) audit and maximal-rank capped refinement.

six-reviewer-1, independent reviewer. Python 3.11+, standard library only.
Researcher's compact orbit weights are untrusted input; no researcher code
is imported. Census uses whole-point stars, transport uses completion frames,
decoder expands orbits, PSD uses integer fraction-free congruence.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import hashlib
import json
import math


def need(ok, message):
    if not ok:
        raise ValueError(message)


def mask(points):
    return sum(1 << x for x in points)


def moved(a, p):
    return sum(1 << p[i] for i in range(9) if a & (1 << i))


def move_system(T, p):
    return tuple(sorted(moved(a, p) for a in T))


def completion(T):
    out = {}
    for a in T:
        vertices = [i for i in range(9) if a >> i & 1]
        need(len(vertices) == 3 and 0 <= a < 512, 'triple input')
        for x, y in combinations(vertices, 2):
            need((x, y) not in out, 'repeated design pair')
            out[x, y] = next(z for z in vertices if z != x and z != y)
    need(len(out) == 36 and len(T) == 12 and len(set(T)) == 12, 'design coverage')
    return out


@lru_cache(None)
def matchings(vertices):
    if not vertices:
        return ((),)
    x = vertices[0]
    out = []
    for y in vertices[1:]:
        remainder = tuple(z for z in vertices if z != x and z != y)
        out += [((x, y),) + m for m in matchings(remainder)]
    return tuple(out)


def star_census():
    """At point x, fill its entire remaining star by a perfect matching."""
    systems = set(); states = 0

    def recurse(x, free, blocks):
        nonlocal states
        states += 1
        if not free:
            key = tuple(sorted(blocks))
            need(key not in systems, 'duplicate census leaf')
            completion(key)
            systems.add(key)
            return
        need(x < 9, 'unfinished census')
        neighbors = tuple(y for y in range(x+1, 9) if (x, y) in free)
        need(len(neighbors) % 2 == 0, 'odd remaining star')
        for m in matchings(neighbors):
            if not all((a, b) in free for a, b in m):
                continue
            covered = frozenset(p for a, b in m for p in ((x, a), (x, b), (a, b)))
            recurse(x+1, free-covered, blocks+tuple(mask((x, a, b)) for a, b in m))

    recurse(0, frozenset(combinations(range(9), 2)), ())
    return systems, states


def affine_system():
    points = [(i//3, i % 3) for i in range(9)]
    index = {p: i for i, p in enumerate(points)}
    return tuple(sorted({mask((i, j, index[((-points[i][0]-points[j][0]) % 3,
                                           (-points[i][1]-points[j][1]) % 3)]))
                         for i, j in combinations(range(9), 2)}))


def frame(table, a, b, c):
    def third(x, y):
        return table[min(x, y), max(x, y)]
    p = [None] * 9
    p[0], p[1], p[3] = a, b, c
    p[2], p[6] = third(a, b), third(a, c)
    p[4], p[5] = third(p[2], p[6]), third(p[1], p[6])
    p[7], p[8] = third(p[2], p[3]), third(p[1], p[3])
    return tuple(p)


def frames(T, first, fixed=False):
    table = completion(T)
    for a in ([0] if fixed else range(9)):
        for b in ([1] if fixed else range(9)):
            if a == b:
                continue
            line = {a, b, table[min(a, b), max(a, b)]}
            for c in range(9):
                if c in line:
                    continue
                p = frame(table, a, b, c)
                if len(set(p)) == 9 and move_system(first, p) == T:
                    yield p


def complete_coverage(data):
    first = affine_system()
    need(list(first) == data['first_blocks'], 'first affine input')
    systems, states = star_census()
    # Each enumerated system carries an explicit, freshly checked isomorphism.
    normalizers = {}
    for T in sorted(systems):
        p = next(frames(T, first, fixed=True), None)
        need(p is not None and sorted(p) == list(range(9)), 'missing normalization witness')
        normalizers[T] = p
    group = list(frames(first, first))
    need(len(group) == len(set(group)) == 432, 'completion-frame automorphisms')
    disjoint = {T for T in systems if not set(T) & set(first)}
    covered = set(); case_orbits = []
    for case in data['cases']:
        T = tuple(case['second_blocks'])
        need(T in disjoint, 'representative outside cohort')
        orbit = {move_system(T, p) for p in group}
        need(orbit <= disjoint and not orbit & covered, 'relative orbits overlap')
        covered |= orbit; case_orbits.append(orbit)
    need(covered == disjoint, 'uncovered input pair')
    need(len(systems) == 840 and len(disjoint) == 192, 'unexpected complete counts')
    need([len(x) for x in case_orbits] == [144, 48], 'relative orbit counts')
    digest = hashlib.sha256(json.dumps(sorted(systems), separators=(',', ':')).encode()).hexdigest()
    summary = {'labelled_STS9': len(systems), 'whole_star_search_states': states,
               'explicit_normalization_witnesses': len(normalizers),
               'first_automorphisms': len(group), 'disjoint_second_systems': len(disjoint),
               'relative_orbit_sizes': [len(x) for x in case_orbits],
               'all_systems_sha256': digest}
    # All alternative decompositions are checked within the complete census.
    decomposition_data = []
    for case in data['cases']:
        union = set(first) | set(case['second_blocks'])
        subsystems = [T for T in systems if set(T) <= union]
        labels = set()
        for T in subsystems:
            complement = tuple(sorted(union-set(T)))
            need(complement in systems, 'union complement not a system')
            p = normalizers[T]; inverse = tuple(p.index(i) for i in range(9))
            normalized_second = move_system(complement, inverse)
            matching_cases = [j for j, orbit in enumerate(case_orbits) if normalized_second in orbit]
            need(len(matching_cases) == 1, 'alternative decomposition classification')
            labels.update(matching_cases)
        decomposition_data.append({'STS_subsystems': len(subsystems),
                                   'unordered_decompositions': len(subsystems)//2,
                                   'relative_case_labels': sorted(labels)})
    summary['alternative_union_decompositions'] = decomposition_data
    need(all(x['STS_subsystems'] == 2 and x['relative_case_labels'] == [j]
             for j, x in enumerate(decomposition_data)), 'union decomposition uniqueness')
    summary['labelled_union_class_sizes'] = [840*len(o)//2 for o in case_orbits]
    summary['full_union_automorphism_orders'] = [math.factorial(9)//x
                                                for x in summary['labelled_union_class_sizes']]
    summary['distinct_labelled_unions'] = sum(summary['labelled_union_class_sizes'])
    return first, summary


def decode(first, case):
    second = tuple(case['second_blocks']); completion(first); completion(second)
    need(not set(first) & set(second), 'overlapping systems')
    D = sorted([0] + [1 << i for i in range(9)] +
               [mask(p) for p in combinations(range(9), 2)] + list(first) + list(second),
               key=lambda a: (a.bit_count(), a))
    need(len(D) == len(set(D)) == 70, 'downset size')
    pos = {a: i for i, a in enumerate(D)}
    need(all(a ^ (1 << i) in pos for a in D for i in range(9) if a >> i & 1),
         'downset closure')
    group = [tuple(p) for p in case['automorphism_subgroup']]
    need(group and len(group) == len(set(group)), 'orbit subgroup size')
    need(all(sorted(p) == list(range(9)) for p in group), 'subgroup permutation')
    need(tuple(range(9)) in group, 'subgroup identity')
    need(all(tuple(p[q[i]] for i in range(9)) in group for p in group for q in group),
         'subgroup closure')
    need(all({moved(a, p) for a in D} == set(D) for p in group), 'subgroup domain')
    Q = [[F(17 if i == j else 0) if a & b else None
          for j, b in enumerate(D)] for i, a in enumerate(D)]
    assigned = set()
    for a, b, value in case['orbit_entries']:
        need(a in pos and b in pos and not a & b and a <= b, 'orbit seed')
        orbit = {tuple(sorted((moved(a, p), moved(b, p)))) for p in group}
        need(not orbit & assigned, 'repeated disjoint orbit')
        for x, y in orbit:
            Q[pos[x]][pos[y]] = Q[pos[y]][pos[x]] = F(value)
        assigned |= orbit
    need(all(x is not None for row in Q for x in row), 'missing disjoint orbit')
    definition(D, Q)
    need(all(x == 1 for x in Q[0]), 'empty column')
    return D, Q


def definition(D, Q):
    n = len(D)
    need(all(len(row) == n for row in Q), 'matrix dimension')
    need(all(Q[i][j] == Q[j][i] for i in range(n) for j in range(n)), 'symmetry')
    need(all(sum(row) == n for row in Q), 'row sum')
    need(all(sum(bool(a & (1 << i)) for a in D) == 17 for i in range(9)), 'actual stars')
    need(all(Q[i][j] == (17 if i == j else 0)
             for i, a in enumerate(D) for j, b in enumerate(D) if a & b), 'support')


def psd_rank(Q):
    """Integer fraction-free symmetric elimination; no numerical threshold."""
    n = len(Q)
    need(all(len(row) == n for row in Q), 'PSD matrix shape')
    need(all(Q[i][j] == Q[j][i] for i in range(n) for j in range(n)), 'PSD input symmetry')
    scale = math.lcm(*(x.denominator for row in Q for x in row))
    A = [[int(x*scale) for x in row] for row in Q]
    previous = 1; rank = 0
    while rank < n:
        need(all(A[i][i] >= 0 for i in range(rank, n)), 'negative PSD diagonal')
        for i in range(rank, n):
            if A[i][i] == 0:
                need(all(A[i][j] == 0 for j in range(rank, n)), 'zero-diagonal cross term')
        k = next((i for i in range(rank, n) if A[i][i] > 0), None)
        if k is None:
            break
        if k != rank:
            A[rank], A[k] = A[k], A[rank]
            for row in A:
                row[rank], row[k] = row[k], row[rank]
        pivot = A[rank][rank]
        for i in range(rank+1, n):
            for j in range(i, n):
                q, rem = divmod(pivot*A[i][j]-A[i][rank]*A[j][rank], previous)
                need(rem == 0, 'fraction-free division')
                A[i][j] = A[j][i] = q
        previous = pivot; rank += 1
    return rank


def upper(Q):
    n = len(Q)
    return [[F(n if i == j else 0)-Q[i][j] for j in range(n)] for i in range(n)]


def digest_matrix(Q):
    return hashlib.sha256(json.dumps([[str(x) for x in row] for row in Q],
                                    separators=(',', ':')).encode()).hexdigest()


def partition_matrix(first, second, D):
    classes = []
    for T in (first, second):
        remaining = set(T)
        while remaining:
            a = min(remaining)
            c = sorted([a]+[b for b in remaining if not a & b])
            need(len(c) == 3 and sum(c) == 511, 'triple parallel class')
            classes.append(c); remaining -= set(c)
    # A pair's color is its cyclic midpoint; each class has its singleton.
    for c in range(9):
        classes.append([1 << c]+[mask((a, b)) for a, b in combinations(range(9), 2)
                                if (5*(a+b)) % 9 == c])
    need(len(classes) == 17 and sorted(a for c in classes for a in c) == sorted(D[1:]),
         'partition coverage')
    need(all(not a & b for c in classes for a, b in combinations(c, 2)), 'partition intersects')
    colors = {a: i for i, c in enumerate(classes) for a in c}
    P = [[F(0) for _ in D] for _ in D]
    for i, a in enumerate(D[1:], 1):
        P[0][i] = P[i][0] = F(70-17*len(classes[colors[a]]))
        for j, b in enumerate(D[1:], 1):
            P[i][j] = F(17*(colors[a] == colors[b]))
    P[0][0] = F(17*sum(len(c)**2 for c in classes)-70**2+140)
    definition(D, P)
    need(P[0][0] == 289 and psd_rank(P) == 17, 'ordinary partition certificate')
    return P


def kernel_check(D, Q, empty=False):
    n = len(D)
    vectors = [[n*int(bool(a & (1 << j)))-17 for a in D] for j in range(9)]
    if empty:
        vectors.append([n*int(i == 0)-1 for i in range(n)])
    for x in vectors:
        need(sum(x) == 0 and all(sum(a*b for a, b in zip(row, x)) == 0 for row in Q),
             'endpoint kernel vector')


def rejects(fn):
    try:
        fn()
    except ValueError:
        return
    raise ValueError('negative control accepted')


def run():
    data = json.loads(Path(__file__).with_name('source_certificates.json').read_text())
    need((data['N'], data['s']) == (70, 17), 'certificate header')
    first, result = complete_coverage(data)
    result['matrices'] = []
    for case in data['cases']:
        D, Q = decode(first, case)
        ranks = [psd_rank(Q), psd_rank(upper(Q))]
        need(ranks == [60, 69], 'original certificate ranks')
        kernel_check(D, Q, empty=True)
        P = partition_matrix(first, case['second_blocks'], D)
        # Exact prescribed perturbation, not a numerical eigenvalue search.
        refined = [[(1023*Q[i][j]+P[i][j])/1024 for j in range(70)] for i in range(70)]
        definition(D, refined); kernel_check(D, refined)
        refined_ranks = [psd_rank(refined), psd_rank(upper(refined))]
        need(refined_ranks == [61, 69], 'maximal-rank capped refinement')
        need(refined[0][0] == F(41, 32), 'refined empty entry')
        result['matrices'].append({'original_matrix_sha256': digest_matrix(Q),
             'original_ranks': ranks, 'subgroup_order': len(case['automorphism_subgroup']),
             'orbit_seeds': len(case['orbit_entries']), 'partition_rank': 17,
             'partition_empty_diagonal': '289', 'refined_ranks': refined_ranks,
             'refined_empty_diagonal': str(refined[0][0]),
             'refined_matrix_sha256': digest_matrix(refined)})
    rejects(lambda: psd_rank([[F(0), F(1)], [F(1), F(1)]]))
    rejects(lambda: psd_rank([[F(1), F(2)], [F(2), F(1)]]))
    bad = json.loads(json.dumps(data['cases'][0]));bad['orbit_entries'].pop()
    rejects(lambda: decode(first, bad))
    bad = json.loads(json.dumps(data['cases'][0]));bad['orbit_entries'][0][2] = '2'
    rejects(lambda: decode(first, bad))
    bad = json.loads(json.dumps(data['cases'][0]));bad['second_blocks'].pop()
    rejects(lambda: decode(first, bad))
    result['negative_controls'] = 5
    result['refinement'] = {'mixing_parameter': '1/1024', 'maximal_base_rank': 61,
                            'maximal_product_rank': '70^k-9k; every k>=1'}
    return result


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
