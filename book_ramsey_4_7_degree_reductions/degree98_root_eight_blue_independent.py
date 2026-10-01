"""Separate exact controls for degree98_root_eight_blue.md, by its author.

Literal colored root quotas, recursive capacity/partition generation, generic
rational zero-word elimination, grouped literal stars and signed intersections.
No import of the primary implementation. This is not independent peer review.
Actual author six-books-1, role researcher. CPython 3.11; checks survive -O.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools as it
import json
from math import comb
from pathlib import Path


def check(test, reason):
    if not test:
        raise RuntimeError(reason)


def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


A, C, ROOTS = set(range(4)), {4, 5}, set(range(6))
SETS = [frozenset(i for i in range(6) if w & (1 << i)) for w in range(64)]
SURPLUS = [len(s & A) - len(s & C) for s in SETS]
COORDS = [(i, j) for i in range(6) for j in range(i, 6)]
EDGES = [[(0, 3), (1, 2), (2, 3)], [(0, 3), (1, 2), (2, 3), (3, 5)],
         [(0, 3), (1, 2), (2, 3), (2, 5), (3, 5)],
         [(0, 3), (1, 2), (2, 3), (2, 5), (3, 4)]]
NAMES = ['zero_AC', 'one_AC', 'two_same_C', 'two_different_C']


def neighbors(edges):
    adj = [set() for _ in range(6)]
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    return adj


def literal_spec(profile, W):
    red = neighbors(EDGES[profile])
    blue = [ROOTS - red[i] - {i} for i in range(6)]
    f = [2 * (len(red[i] & A) - len(red[i] & C) + (-1 if i in A else 1)) for i in range(6)]
    s = [(8 if i in A else 10) - len(red[i]) for i in range(6)]
    G = [[0]*6 for _ in range(6)]
    for i in range(6):
        G[i][i] = s[i]
        for j in range(i+1, 6):
            if j in red[i]:
                value = 3 - W[i][j] - len(red[i] & red[j])
            else:
                outside_blue = 6 - W[i][j] - len(blue[i] & blue[j])
                value = outside_blue - 16 + s[i] + s[j]
            G[i][j] = G[j][i] = value
    tau = [sum(G[i][j] for j in A) - sum(G[i][j] for j in C) for i in range(6)]
    Z = [[(3 if j in A else 5) * s[i] - sum(G[i][k] for k in red[j])
          - (2*G[i][j] if j in C else 0) for j in range(6)] for i in range(6)]
    return {'profile': NAMES[profile], 'R': [[int(j in red[i]) for j in range(6)] for i in range(6)],
            'f': f, 'W': W, 'G': G, 'tau': tau, 'second': sum(tau[:4])-sum(tau[4:]),
            'Z': Z, 'outside_column_sums': [f[i]-sum(W[i]) for i in range(6)]}


def capacity_matrices(profile):
    zero = [[0]*6 for _ in range(6)]
    cap = literal_spec(profile, zero)['f']
    pairs = list(it.combinations(range(6), 2))
    def walk(k, left, W):
        if k == len(pairs):
            yield [row[:] for row in W]
            return
        i, j = pairs[k]
        for weight in range(min(left[i], left[j])+1):
            W[i][j] = W[j][i] = weight
            next_left = left[:]
            next_left[i] -= weight; next_left[j] -= weight
            yield from walk(k+1, next_left, W)
        W[i][j] = W[j][i] = 0
    yield from walk(0, cap, zero)


def partitions(left=6, ceiling=4):
    if not left:
        yield ()
    else:
        for d in range(min(left, ceiling), 0, -1):
            for p in partitions(left-d, d):
                yield tuple(sorted((d,)+p))


def necessary_moments(spec, parts):
    answer = []
    G = spec['G']
    for p in parts:
        if sum(v*v for v in p) != spec['second']:
            continue
        sums = {0}
        for v in p:
            sums |= {s+v for s in sums}
        if any(t not in sums for t in spec['tau']):
            continue
        if p.count(4) > 16-G[4][4]-G[5][5]+G[4][5]:
            continue
        answer.append(list(p))
    return sorted(answer)


def positive_patterns(spec, values):
    answer = set()
    domains = {d: [w for w in range(64) if SURPLUS[w] == d] for d in set(values)}
    def walk(k, picked, target):
        if k == len(values):
            if any(target):
                return
            key = tuple(sorted(picked))
            if all(sum(int(i in SETS[w] and j in SETS[w]) for w in key) <= spec['G'][i][j] for i, j in COORDS):
                answer.add(key)
            return
        d = values[k]
        for w in domains[d]:
            if k and values[k-1] == d and w < picked[-1]:
                continue
            rest = [target[i]-(d if i in SETS[w] else 0) for i in range(6)]
            if min(rest) >= 0:
                walk(k+1, picked+[w], rest)
    walk(0, [], spec['tau'])
    return sorted(answer)


def zero_solution(spec, positive):
    """Generic rational solve of row-count plus 21 Gram feature equations."""
    zero_words = [w for w in range(64) if SURPLUS[w] == 0]
    check(len(zero_words) == 15, 'zero word domain')
    features = lambda w: [1]+[int(i in SETS[w] and j in SETS[w]) for i, j in COORDS]
    columns = [features(w) for w in zero_words]
    target = [16]+[spec['G'][i][j] for i, j in COORDS]
    for w in positive:
        target = [a-b for a, b in zip(target, features(w))]
    rows = [[Fraction(col[r]) for col in columns]+[Fraction(target[r])] for r in range(22)]
    pivots, rank = {}, 0
    for col in range(15):
        pivot = next((r for r in range(rank, 22) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][col]
        rows[rank] = [v/scale for v in rows[rank]]
        for r in range(22):
            if r != rank and rows[r][col]:
                factor = rows[r][col]
                rows[r] = [a-factor*b for a, b in zip(rows[r], rows[rank])]
        pivots[col] = rank
        rank += 1
    check(rank == 15 and all(any(row[:15]) or not row[15] for row in rows), 'full-rank consistent zero solve')
    solution = [rows[pivots[c]][15] for c in range(15)]
    check(all(v.denominator == 1 for v in solution), 'integral signed zero solution')
    counts = [0]*64
    for w, v in zip(zero_words, solution):
        counts[w] = int(v)
    for w in positive:
        counts[w] += 1
    return counts


def grouped_stars(full, x):
    available = Counter(full)
    available[full[x]] -= 1
    classes = [(w, n) for w, n in sorted(available.items()) if n]
    def walk(k, left, picked, weight):
        if k == len(classes):
            if left == 0:
                yield picked, weight
            return
        w, n = classes[k]
        for take in range(min(left, n)+1):
            yield from walk(k+1, left-take, picked+[w]*take, weight*comb(n, take))
    yield from walk(0, 5, [], 1)


def literal_final_form(spec, positive):
    counts = zero_solution(spec, positive)
    check(min(counts) >= 0 and not counts[0], 'last case nonnegative/no-empty incidence')
    full = [w for w, n in enumerate(counts) for _ in range(n)]
    x = full.index(15)
    possible = []
    for v, w in enumerate(full):
        if {0, 1} <= SETS[w] and 4 not in SETS[w]:
            for u, z in enumerate(full):
                if {0, 1} <= SETS[z] and 5 not in SETS[z]:
                    if int(4 in SETS[z])-int(5 in SETS[w]) == spec['Z'][4][5]-spec['Z'][5][4]:
                        possible.append([v, u])
    check(possible == [[x, x]], 'separate complete C-unit placement')
    root_red = neighbors(EDGES[0])
    root_neighbors = [root_red[j] | {6+v for v, w in enumerate(full) if j in SETS[w]} for j in range(6)]
    universe = set(range(22))
    all_weight, C_weight, min_A, survivors, grouped = 0, 0, None, 0, 0
    for chosen_words, weight in grouped_stars(full, x):
        grouped += 1; all_weight += weight
        required = Counter(chosen_words)
        chosen = []
        for v, w in enumerate(full):
            if v != x and required[w]:
                chosen.append(v); required[w] -= 1
        check(len(chosen) == 5 and not any(required.values()), 'grouped literal star expansion')
        red_x = A | {6+v for v in chosen}
        blue_x = universe-red_x-{6+x}
        defects = []
        for j in range(6):
            if j in A:
                defects.append(3-len(red_x & root_neighbors[j]))
            else:
                blue_j = universe-root_neighbors[j]-{j}
                defects.append(6-len(blue_x & blue_j))
        if defects[4:] != [1, 1]:
            continue
        C_weight += weight
        total_A = sum(len(SETS[w] & A) for w in chosen_words)
        min_A = total_A if min_A is None else min(min_A, total_A)
        check(total_A >= 8, 'separate literal A-incidence lower bound')
        if min(defects[:4]) >= 0:
            survivors += weight
    check(all_weight == 3003 and C_weight == 250 and min_A == 8 and survivors == 0, 'literal final local obstruction')
    return {'positive_words': list(positive), 'word_counts': counts, 'unit_column_pairs': possible,
            'all_five_neighbor_subsets': all_weight, 'C_only_star_candidates': C_weight,
            'minimum_A_incidence': min_A, 'root_spine_survivors': survivors}, grouped


def literal_roots():
    counts = [0]*7
    A_pairs, AC_pairs = list(it.combinations(range(4), 2)), list(it.product(range(4), (4, 5)))
    for a_bits in it.product((0, 1), repeat=6):
        A_edges = [p for p, b in zip(A_pairs, a_bits) if b]
        for ac_bits in it.product((0, 1), repeat=8):
            edges = A_edges+[p for p, b in zip(AC_pairs, ac_bits) if b]
            red = neighbors(edges)
            f = [2*(len(red[i]&A)-len(red[i]&C)+(-1 if i in A else 1)) for i in range(6)]
            if min(f) < 0 or sum(f) != 8:
                continue
            degrees = sorted(len(red[i]&A) for i in A)
            attachments = sum(ac_bits)
            if degrees == [1, 1, 1, 3]:
                check(attachments <= 2, 'star attachment range')
                counts[attachments] += 1
            else:
                check(degrees == [1, 1, 2, 2] and attachments <= 2, 'path classification')
                case = 3+attachments
                if attachments == 2 and all(len(red[c]&A) == 1 for c in C):
                    case = 6
                counts[case] += 1
    check(counts == [4, 8, 4, 12, 48, 24, 24], 'separate root classification')
    return sum(counts)


def signed_audit(controls):
    compared = 0
    for control in controls:
        R = control['R']
        red = [{j for j, b in enumerate(row) if b} for row in R]
        blue = [set(range(22))-red[i]-{i} for i in range(22)]
        check(list(map(len, red)) == [8]*4+[10]*2+[9]*16, 'signed control degree histogram')
        F = [[0 if i == j else 3-len(red[i]&red[j]) if j in red[i]
              else 6-len(blue[i]&blue[j]) for j in range(22)] for i in range(22)]
        check(F == control['F'], 'all literal signed defects')
        compared += 484
        G = [[len(red[i]&red[j]&set(range(6, 22))) for j in range(6)] for i in range(6)]
        check(G == control['G'], 'signed literal incidence Gram')
        for i in range(22):
            h, k = len(red[i]&A), len(red[i]&C)
            f = 2*(h-k-1) if i in A else 2*(h-k+1) if i in C else 1+2*(h-k)
            check(sum(F[i]) == f, 'signed incident defect')
            red_triangles = sum(int(v in red[u]) for u, v in it.combinations(red[i], 2))
            check(sum(F[i][j] for j in red[i]) == 3*len(red[i])-2*red_triangles, 'exact red incident parity bridge')
        root_edges = [(i, j) for i, j in it.combinations(range(6), 2) if j in red[i]]
        W = [row[:6] for row in F[:6]]
        red0 = neighbors(root_edges)
        blue0 = [ROOTS-red0[i]-{i} for i in range(6)]
        for i in range(6):
            for j in range(i+1, 6):
                target = 3-W[i][j]-len(red0[i]&red0[j]) if j in red0[i] else 6-W[i][j]-len(blue0[i]&blue0[j])-16+G[i][i]+G[j][j]
                check(G[i][j] == target, 'signed literal Gram quota')
        Z = [[(3 if j in A else 5)*G[i][i]-sum(G[i][k] for k in red0[j])
              -(2*G[i][j] if j in C else 0) for j in range(6)] for i in range(6)]
        for i in range(6):
            for j in range(6):
                lhs = Z[i][j]-sum(int(i in red[v])*F[v][j] for v in range(6, 22))
                rhs = Z[j][i]-sum(int(j in red[v])*F[v][i] for v in range(6, 22))
                check(lhs == rhs, 'signed symmetric outside-column bridge')
        for v in range(6, 22):
            for j in range(6):
                required = 3 if j in A else 5-2*int(j in red[v])
                check(len(red[v]&red[j]) == required-F[v][j], 'signed literal spine quota')
        root_sum = sum(sum(F[i]) for i in range(6))
        check(root_sum == -4+4*(sum(int(j in red[i]) for i, j in it.combinations(range(4), 2))-int(5 in red[4])), 'signed root budget')
        check(sum(sum(F[i])-1 for i in range(6, 22)) == 20-root_sum, 'signed B surplus budget')
    return compared


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    records = json.loads(args.records.read_text())
    expected = json.loads(Path(__file__).with_name('degree98_root_eight_blue_expected.json').read_text())
    check(digest(records) == expected['records_sha256'], 'generated record hash')
    root_count = literal_roots()
    parts = sorted(set(partitions()))
    check([list(p) for p in parts] == records['partitions_of_six_parts_at_most_four'], 'separate positive partitions')
    entries, coefficient_entries, patterns, grouped, multiplicity_entries = 0, 0, 0, 0, 0
    for profile in range(4):
        actual = [r for r in records['root_pair_records'] if r['profile'] == NAMES[profile]]
        key = lambda W: tuple(W[i][j] for i, j in it.combinations(range(6), 2))
        supplied = {key(r['W']): r for r in actual}
        matrices = list(capacity_matrices(profile))
        check(len(matrices) == len(supplied) == [56, 14, 3, 5][profile], 'complete recursive capacity domain')
        check({key(W) for W in matrices} == set(supplied), 'all root defect matrices agree')
        for W in matrices:
            spec = literal_spec(profile, W)
            record = supplied[key(W)]
            for field, value in spec.items():
                check(record[field] == value, 'literal specification: '+field)
            coefficient_entries += 36*2+6*3+1
            moments = necessary_moments(spec, parts)
            check(moments == record['moments'], 'all moment restrictions agree')
            entries += 1
            if not moments:
                continue
            exclusion = record['exclusion']
            a, b = W[2][3], W[4][5]
            if exclusion['reason'] == 'zero_C_column_nonzero_endpoint_moment':
                failing = [c for c in C if spec['outside_column_sums'][c] == 0 and any(spec['Z'][i][c] != spec['Z'][c][i] for i in (0, 1))]
                check(failing == exclusion['failing_C'] and failing, 'zero-column correlation contradiction')
                continue
            check(len(moments) == 1, 'remaining positive moment profile')
            positive = positive_patterns(spec, moments[0])
            patterns += len(positive)
            if (a, b) == (2, 1):
                check(not positive and moments == [[1, 2, 3]], 'separate surplus-one impossibility')
            elif (a, b) == (1, 0):
                check(positive == [(1, 2, 15)], 'separate forced singleton words')
                counts = zero_solution(spec, positive[0])
                check(counts[0] == exclusion['empty_count'] == -1, 'generic rational negative empty count')
            else:
                check((a, b) == (0, 1) and len(positive) == 4, 'last positive pattern domain')
                forms = []
                for p in positive:
                    form, n = literal_final_form(spec, p)
                    forms.append(form); grouped += n; multiplicity_entries += 64
                check(forms == exclusion['forms'], 'all final multiplicities, units and star counts agree')
    signed = signed_audit(records['signed_controls'])
    check(entries == 78 and patterns == 5 and multiplicity_entries == 256, 'complete audit totals')
    report = {'agent': 'six-books-1', 'role': 'researcher', 'complete': True,
              'ordinary_argument_controls_passed': True, 'scope': 'separate author validation, no host census or independent peer review',
              'labeled_roots': root_count, 'capacity_states': entries, 'coefficient_entries': coefficient_entries,
              'positive_patterns': patterns, 'full_multiplicity_entries': multiplicity_entries,
              'grouped_star_vectors': grouped, 'labeled_five_neighbor_subsets': 12012,
              'C_only_star_candidates': 1000, 'root_spine_survivors': 0,
              'signed_F_entries': signed, 'records_sha256': digest(records)}
    if args.report:
        args.report.write_text(json.dumps(report, sort_keys=True, indent=2)+'\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
