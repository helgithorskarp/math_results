#!/usr/bin/env python3
"""Definition-level exact checks, matching replay and bounded coverage.

This validates finite instances of the separately proved all-order theorem.
It does not formalize Harris, Hall, or the spanning-tree gap argument.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path

import balanced_pendant_completion as build
from verify import check, psd_ldl, require


def fingerprint(matrix):
    data = [[str(x) for x in row] for row in matrix]
    return sha256(json.dumps(data, separators=(',', ':')).encode()).hexdigest()


def hall_census(E):
    """All Hall inequalities on the original disjointness bipartite graph."""
    require(len(E) <= 16, 'Hall census exceeds explicit finite bound')
    neighbors = [sum(1 << j for j, B in enumerate(E) if not A & B) for A in E]
    unions = [0] * (1 << len(E))
    for subset in range(1, len(unions)):
        bit = subset & -subset
        unions[subset] = unions[subset ^ bit] | neighbors[bit.bit_length() - 1]
        require(unions[subset].bit_count() >= subset.bit_count(),
                'Exact original Hall inequality failed')
    return len(unions)


def independent_edge_matching(S, T, forced_a, forced_b):
    """Bounded direct backtracking with a forced edge, independent of splicing."""
    require(len(S) <= 9, 'Independent forced-edge replay exceeds finite bound')
    pending = tuple(x for x in S if x != forced_a)
    def search(left, available):
        if not left:
            return True
        a = min(left, key=lambda x: (sum(not x & y for y in available), x))
        rest = tuple(x for x in left if x != a)
        for b in available:
            if not a & b and search(rest, tuple(y for y in available if y != b)):
                return True
        return False
    require(not forced_a & forced_b and search(pending, tuple(y for y in T if y != forced_b)),
            'Independent forced-edge matching failed')


def census(D, center, s):
    require(len(D) <= 20, 'Intersecting census exceeds explicit finite bound')
    visited, largest, maxima = 0, 0, []
    def visit(chosen, remaining):
        nonlocal visited, largest, maxima
        visited += 1
        if len(chosen) > largest:
            largest, maxima = len(chosen), [chosen]
        elif len(chosen) == largest:
            maxima.append(chosen)
        for j, a in enumerate(remaining):
            visit(chosen + [a], [b for b in remaining[j + 1:] if a & b])
    visit([], D[1:])
    star = [a for a in D if a >> center & 1]
    require(largest == s and maxima == [star], 'Bounded equality census failed')
    return dict(visited_nonempty_vertex_families_including_empty_family=visited,
                largest_size=largest, maximum_families=len(maxima))


def audit(label, original, center=0, independent=True):
    record = build.completion(original, center)
    D, M = record['family'], build.dense_entries(record)
    N, s, eps = len(D), record['s'], record['epsilon']
    c, p = 1 << center, 1 << max(original).bit_length()
    E = tuple(a for a in original if not a & c)
    S = tuple(a | c for a in E) + (c | p,)
    T = E + (p,)
    require(D == sorted(original + [p, c | p]) and N == 2 * s,
            'Independent augmented geometry differs')
    allowed = {(a, b) for a in S for b in T if not a & b}
    h = len(allowed)
    g = F(2, h * (N - 1) ** 2)
    require(record['edge_count'] == h and record['gap'] == g
            and eps == F(1, 4 * h * (len(E) - 1) * (N - 1) ** 2),
            'Exact gap or perturbation scale differs')
    f = record['base_bijection']
    require(set(f) == set(f.values()) == set(E) and all(not A & B for A, B in f.items()),
            'Bad baseline disjoint bijection')
    counts = [[0] * N for _ in D]
    covered = set()
    ix = {a: i for i, a in enumerate(D)}
    for a, b, targets in build.conditioned_matchings(E, c, p, f):
        require((a, b) not in covered and (a, b) in allowed,
                'Duplicate or forbidden conditioned edge')
        covered.add((a, b))
        require(len(targets) == len(S) and set(targets) == set(T),
                'Conditioned target list is not a bijection')
        pairs = list(zip(S, targets))
        require((a, b) in pairs and all(not x & y for x, y in pairs),
                'Conditioned edge or disjoint matching failed')
        for x, y in pairs:
            i, j = ix[x], ix[y]
            counts[i][j] += 1
            counts[j][i] += 1
        if independent:
            independent_edge_matching(S, T, a, b)
    require(covered == allowed and counts == record['counts'],
            'Complete matching coverage/count replay differs')
    M0 = [[F(x, h) for x in row] for row in counts]
    require(all(sum(row) == 1 for row in M0), 'Matching average is not stochastic')
    require(all(M0[ix[a]][ix[b]] >= F(1, h) for a, b in allowed),
            'Full allowed support or minimum weight failed')
    # Literal sum of row-zero trades, not the producer entry conditions.
    trade = [[F(0)] * N for _ in D]
    for Y in E[1:]:
        for a, b, delta in ((0, Y, 1), (0, p, 1), (p, Y, -1)):
            trade[ix[a]][ix[b]] += delta
            trade[ix[b]][ix[a]] += delta
        trade[0][0] -= 2
    one = [1] * N
    q = [1 if a & c else -1 for a in D]
    require(sum(q) == 0, 'Unbalanced signed constant')
    def mv(A, v):
        return [sum(x * y for x, y in zip(row, v)) for row in A]
    require(mv(M0, one) == one and mv(M0, q) == [-x for x in q],
            'Baseline endpoint vectors failed')
    require(mv(trade, one) == [0] * N and mv(trade, q) == [0] * N,
            'Trade does not preserve both endpoint kernels')
    require(max(sum(abs(x) for x in row) for row in trade) == 4 * (len(E) - 1),
            'Trade absolute-row norm bound differs')
    require(M == [[M0[i][j] + eps * trade[i][j] for j in range(N)] for i in range(N)],
            'Full entry-level independent trade replay differs')
    P1 = [[F(int(i == j)) - F(1, N) for j in range(N)] for i in range(N)]
    Pq = [[F(int(i == j)) - F(q[i] * q[j], N) for j in range(N)] for i in range(N)]
    PZ = [[F(int(i == j)) - F(1 + q[i] * q[j], N)
           for j in range(N)] for i in range(N)]
    for sign, projection in ((-1, P1), (1, Pq)):
        baseline = [[F(int(i == j)) + sign * M0[i][j]
                     for j in range(N)] for i in range(N)]
        require(psd_ldl(baseline) == N - 1, 'Baseline endpoint rank differs')
        psd_ldl([[baseline[i][j] - g * projection[i][j]
                  for j in range(N)] for i in range(N)])
        final = [[F(int(i == j)) + sign * M[i][j]
                  for j in range(N)] for i in range(N)]
        require(psd_ldl(final) == N - 1, 'Final endpoint rank differs')
        psd_ldl([[final[i][j] - g / 2 * PZ[i][j]
                  for j in range(N)] for i in range(N)])
    require(check(D, M, s, upper=True) == N - 1, 'Definition-level H check failed')
    require(min(M[0][1:]) >= eps and all(M[0][j] > 0 for j in range(1, N)),
            'Positive empty margin failed')
    require(mv(M, one) == one and mv(M, q) == [-x for x in q],
            'Final endpoint vectors failed')
    result = dict(case=label, original_family=original, center=center,
                  original_N=len(original), original_s=len(E), total_pendants=1,
                  N=N, s=s, edge_count=h, complete_matching_replays=h,
                  independent_forced_edge_replays=h if independent else 0,
                  baseline_Hall_subfamilies=hall_census(E),
                  gap=str(g), epsilon=str(eps), empty_margin=str(min(M[0][1:])),
                  lower_slack_rank=N - 1, upper_slack_rank=N - 1,
                  whole_final_and_buffered_LDL=True, complete_entry_replay=N * N,
                  matrix_sha256=fingerprint(M),
                  negative_nonempty_offdiagonals=sum(M[i][j] < 0 for i in range(1, N)
                                                   for j in range(i + 1, N)))
    if N <= 20:
        result['bounded_equality_census'] = census(D, center, s)
    return result


def three_point_downsets():
    """Complete labeled power-set enumeration, omitting empty and {empty}."""
    families = []
    for mask in range(1 << 8):
        E = [a for a in range(8) if mask >> a & 1]
        if len(E) < 2 or 0 not in E:
            continue
        present = set(E)
        if all(b in present for a in E for b in range(8) if b & a == b):
            families.append(E)
    require(len(families) == 18, 'Complete labeled three-point downset count differs')
    return families


def rejection_controls():
    bad = [([], 0), ([0, 1], 0), ([0, 1, 2], 0), ([0, 1, 3, 4], 0),
           ([0, 2, 1, 3], 0), ([0, 1, 2, 2], 0), ([0, 1, 2, 3], True),
           ([0, 1, 2, 3], 2), ([0, 1, 2, 3.0], 0),
           ([0, True, 2, 3], 0), ([0, -1, 2, 3], 0)]
    for family, center in bad:
        try:
            build.completion(family, center)
        except ValueError:
            pass
        else:
            raise ValueError('Invalid balanced input accepted')
    record = build.completion(list(range(4)), 0)
    M = build.dense_entries(record)
    for i, j in ((1, 1), (0, 1)):
        broken = [row[:] for row in M]
        broken[i][j] += 1
        try:
            check(record['family'], broken, record['s'], upper=True)
        except ValueError:
            pass
        else:
            raise ValueError('Corrupted H matrix accepted')
    return len(bad) + 2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    small = []
    for E in three_point_downsets():
        original = sorted([a << 1 for a in E] + [(a << 1) | 1 for a in E])
        small.append(audit('E3-' + '-'.join(map(str, E)), original))
    fixtures = [audit('cube4', list(range(16))),
                audit('cube5', list(range(32)), independent=False),
                audit('hole-and-center-relabel', [0, 1, 8, 16, 17, 24], center=4)]
    result = dict(agent='six-downset-1', role='researcher',
                  theorem_scope='finite checks support the separate ordinary all-order proof',
                  complete_labeled_three_point_E_count=len(small),
                  rejected_controls=rejection_controls(), cohort=small, fixtures=fixtures)
    result['canonical_sha256'] = sha256(json.dumps(result, sort_keys=True,
                                      separators=(',', ':')).encode()).hexdigest()
    if args.check:
        expected = json.loads(Path(__file__).with_name('balanced_pendant_expected.json').read_text())
        require(result == expected, 'Complete balanced output differs from frozen fixture')
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
