"""Exact controls for the ordinary blue-C root-defect-eight argument.

CPython 3.11 standard library. These coefficient/domain/placement controls
validate the written argument; they are not a census of 22-vertex hosts.
Generated records stay outside this source directory. Checks survive -O.
Actual author six-books-1, role researcher.
"""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path


def require(test, reason):
    if not test:
        raise RuntimeError(reason)


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


PAIRS = list(it.combinations(range(6), 2))
WORDS = [tuple((w >> i) & 1 for i in range(6)) for w in range(64)]
DELTA = [sum(x[:4]) - sum(x[4:]) for x in WORDS]
PATH = [(0, 3), (1, 2), (2, 3)]
EXTRAS = [[], [(3, 5)], [(2, 5), (3, 5)], [(2, 5), (3, 4)]]
NAMES = ['zero_AC', 'one_AC', 'two_same_C', 'two_different_C']


def matrix(edges, n=6):
    R = [[0] * n for _ in range(n)]
    for i, j in edges:
        R[i][j] = R[j][i] = 1
    return R


def root_f(R):
    return [2 * (sum(R[i][:4]) - sum(R[i][4:]) + (-1 if i < 4 else 1)) for i in range(6)]


def root_classification():
    star = [(0, 3), (1, 3), (2, 3)]
    profiles = [star, star + [(3, 5)], star + [(3, 4), (3, 5)]] + [PATH + x for x in EXTRAS]
    orbits = []
    for edges in profiles:
        orbit = set()
        for a in it.permutations(range(4)):
            for c in ((4, 5), (5, 4)):
                p = a + c
                orbit.add(tuple(sorted(tuple(sorted((p[i], p[j]))) for i, j in edges)))
        orbits.append(orbit)
    union = set().union(*orbits)
    require(sum(map(len, orbits)) == len(union) == 124, 'root-orbit overlap/count')
    scanned = set()
    for bits in it.product((0, 1), repeat=15):
        R = matrix([p for p, x in zip(PAIRS, bits) if x])
        f = root_f(R)
        if not R[4][5] and min(f) >= 0 and sum(f) == 8:
            scanned.add(tuple(p for p, x in zip(PAIRS, bits) if x))
    require(scanned == union, 'literal root classification')
    require(list(map(len, orbits)) == [4, 8, 4, 12, 48, 24, 24], 'root orbit sizes')
    return {'all_edge_words': 32768, 'valid_labeled_roots': 124,
            'orbit_sizes': list(map(len, orbits)), 'three_leaf_union_lower_bound': 18}


def specification(profile, W):
    R = matrix(PATH + EXTRAS[profile])
    f = root_f(R)
    d = [8] * 4 + [10] * 2
    s = [d[i] - sum(R[i]) for i in range(6)]
    G = [[s[i] if i == j else d[i] + d[j] - 14 + (17 - d[i] - d[j]) * R[i][j]
          - sum(R[i][k] * R[k][j] for k in range(6)) - W[i][j]
          for j in range(6)] for i in range(6)]
    t = [1] * 4 + [-1] * 2
    tau = [sum(G[i][j] * t[j] for j in range(6)) for i in range(6)]
    second = sum(t[i] * tau[i] for i in range(6))
    ell = [3] * 4 + [5] * 2
    Z = [[s[i] * ell[j] - sum(G[i][k] * (R[k][j] + (2 if k == j and j >= 4 else 0))
                              for k in range(6)) for j in range(6)] for i in range(6)]
    return {'profile': NAMES[profile], 'R': R, 'f': f, 'W': W, 'G': G,
            'tau': tau, 'second': second, 'Z': Z,
            'outside_column_sums': [f[i] - sum(W[i]) for i in range(6)]}


def root_weights(profile):
    f = root_f(matrix(PATH + EXTRAS[profile]))
    active = [i for i in range(6) if f[i]]
    pairs = list(it.combinations(active, 2))
    for values in it.product(*(range(min(f[i], f[j]) + 1) for i, j in pairs)):
        W = [[0] * 6 for _ in range(6)]
        for (i, j), value in zip(pairs, values):
            W[i][j] = W[j][i] = value
        if all(sum(W[i]) <= f[i] for i in range(6)):
            yield specification(profile, W)


def partitions():
    return [tuple(d for d in range(1, 5) for _ in range(c[d-1]))
            for c in it.product(range(7), repeat=4)
            if sum(d * c[d-1] for d in range(1, 5)) == 6]


def permitted_moments(spec, parts):
    answer = []
    G = spec['G']
    neither_C = 16 - G[4][4] - G[5][5] + G[4][5]
    for values in parts:
        if sum(v*v for v in values) != spec['second']:
            continue
        reachable = {sum(sub) for n in range(len(values) + 1) for sub in it.combinations(values, n)}
        if all(x in reachable for x in spec['tau']) and neither_C >= values.count(4):
            answer.append(list(values))
    return sorted(answer)


def positive_words(spec, values):
    domains = [list(it.combinations_with_replacement([w for w in range(64) if DELTA[w] == d], values.count(d)))
               for d in range(1, 5)]
    answer = []
    for product in it.product(*domains):
        words = sorted(w for group in product for w in group)
        if any(sum(DELTA[w] * WORDS[w][i] for w in words) != spec['tau'][i] for i in range(6)):
            continue
        H = [[spec['G'][i][j] - sum(WORDS[w][i] * WORDS[w][j] for w in words)
              for j in range(6)] for i in range(6)]
        if min(map(min, H)) >= 0:
            answer.append((words, H))
    return answer


def phi(word):
    h, k = sum(WORDS[word][:4]), sum(WORDS[word][4:])
    return 1 + 3 * h * (h-1) // 2 - h * k


def empty_count(G, positive):
    return 16 + 3 * sum(G[i][j] for i, j in it.combinations(range(4), 2)) - sum(G[i][c] for i in range(4) for c in (4, 5)) - sum(phi(w) for w in positive)


def decode_zero(H, positive):
    counts = [0] * 64
    for w in positive:
        counts[w] += 1
    for i, j in it.combinations(range(4), 2):
        counts[(1 << i) + (1 << j) + 48] = H[i][j]
    for i in range(4):
        for c in (4, 5):
            counts[(1 << i) + (1 << c)] = H[i][c] - sum(H[i][j] for j in range(4) if i != j)
    counts[0] = 16 - sum(counts)
    require(min(counts) >= 0, 'negative decoded zero count')
    return counts


def final_form(spec, positive, H):
    counts = decode_zero(H, positive)
    full = [w for w, n in enumerate(counts) for _ in range(n)]
    require(len(full) == 16 and not counts[0], 'final incidence size/empty count')
    require([[sum(WORDS[w][i] * WORDS[w][j] for w in full) for j in range(6)] for i in range(6)] == spec['G'], 'decoded full Gram')
    require(empty_count(spec['G'], positive) == 0, 'empty identity in last state')
    eligible = [[v for v, w in enumerate(full) if WORDS[w][0] and WORDS[w][1] and not WORDS[w][c]] for c in (4, 5)]
    pairs = [(v, u) for v in eligible[0] for u in eligible[1]
             if WORDS[full[u]][4] - WORDS[full[v]][5] == spec['Z'][4][5] - spec['Z'][5][4]]
    x = full.index(15)
    require(pairs == [(x, x)], 'C unit columns must coincide on delta four')
    checked, C_only, min_A, survivors = 0, 0, None, 0
    for neighbors in it.combinations([v for v in range(16) if v != x], 5):
        checked += 1
        column_counts = [sum(WORDS[full[v]][j] for v in neighbors) for j in range(6)]
        if column_counts[4:] != [4, 4]:
            continue
        C_only += 1
        total_A = sum(column_counts[:4])
        min_A = total_A if min_A is None else min(min_A, total_A)
        require(total_A >= 8, 'written neighbor-count lower bound')
        survivors += int(all(column_counts[j] <= [2, 2, 1, 1][j] for j in range(4)))
    require(checked == 3003 and C_only and survivors == 0, 'last root-spine contradiction')
    return {'positive_words': positive, 'word_counts': counts, 'unit_column_pairs': [list(p) for p in pairs],
            'all_five_neighbor_subsets': checked, 'C_only_star_candidates': C_only,
            'minimum_A_incidence': min_A, 'root_spine_survivors': survivors}


def analyze_zero(spec, moments):
    W, Z = spec['W'], spec['Z']
    a, b = W[2][3], W[4][5]
    cross = [W[i][c] for i in (2, 3) for c in (4, 5)]
    for c in (4, 5):
        require([Z[i][c] - Z[c][i] for i in (0, 1)] == [1-W[3][c], 1-W[2][c]], 'endpoint C correlations')
    failing = [c for c in (4, 5) if spec['outside_column_sums'][c] == 0
               and any(Z[i][c] != Z[c][i] for i in (0, 1))]
    result = {'a': a, 'b': b, 'cross': cross, 'moments': moments}
    if failing:
        result.update(reason='zero_C_column_nonzero_endpoint_moment', failing_C=failing)
        return result
    require(not any(cross), 'unclassified zero attachment state')
    require(len(moments) == 1, 'remaining moment profile uniqueness')
    candidates = positive_words(spec, moments[0])
    if (a, b) == (2, 1):
        require(moments == [[1, 2, 3]] and spec['tau'] == [5, 5, 3, 3, 1, 1], 'surplus-one contradiction coefficients')
        require(not candidates, 'surplus-one capacity contradiction')
        result.update(reason='delta_one_meets_both_C_but_at_most_two_A', positive_candidates=0)
    elif (a, b) == (1, 0):
        require(moments == [[1, 1, 4]] and len(candidates) == 1 and candidates[0][0] == [1, 2, 15], 'forced singleton positive rows')
        n = empty_count(spec['G'], candidates[0][0])
        require(n == -1, 'negative empty row contradiction')
        result.update(reason='negative_empty_count', positive_words=[1, 2, 15], empty_count=n)
    elif (a, b) == (0, 1):
        require(moments == [[1, 1, 4]] and len(candidates) == 4, 'four final positive patterns')
        forms = [final_form(spec, p, H) for p, H in candidates]
        result.update(reason='C_unit_columns_force_impossible_delta_four_star', forms=forms)
    else:
        raise RuntimeError('unclassified necessary moment state')
    return result


# The control generator is reproduced from degree98_root_four_check.py.
def signed_controls():
    """32 deterministic Havel--Hakimi/two-edge-switch controls, validation only."""
    degrees = [8] * 4 + [9] * 16 + [10] * 2
    todo, adj = degrees[:], [set() for _ in range(22)]
    while max(todo):
        v = max(range(22), key=lambda i: (todo[i], -i))
        candidates = sorted((i for i in range(22) if i != v and todo[i]), key=lambda i: (-todo[i], i))[:todo[v]]
        require(len(candidates) == todo[v], 'non-graphical control degrees')
        todo[v] = 0
        for i in candidates:
            require(i not in adj[v], 'repeated control edge')
            adj[v].add(i)
            adj[i].add(v)
            todo[i] -= 1
    state, records = 104733, []
    perm = list(range(4)) + [20, 21] + list(range(4, 20))
    d = [8] * 4 + [10] * 2 + [9] * 16
    for sample in range(32):
        changed = 0
        for trial in range(20000):
            edges = [(i, j) for i in range(22) for j in sorted(adj[i]) if i < j]
            state = (1664525 * state + 1013904223) % (1 << 32)
            a, z = edges[state % len(edges)]
            state = (1664525 * state + 1013904223) % (1 << 32)
            x, y = edges[state % len(edges)]
            if len({a, z, x, y}) != 4 or x in adj[a] or y in adj[z]:
                continue
            for i, j in ((a, z), (x, y)):
                adj[i].remove(j); adj[j].remove(i)
            for i, j in ((a, x), (z, y)):
                adj[i].add(j); adj[j].add(i)
            changed += 1
            if changed == 16:
                break
        require(changed == 16, 'unfinished control construction')
        R = [[int(perm[j] in adj[perm[i]]) for j in range(22)] for i in range(22)]
        require(list(map(sum, R)) == d, 'control degree mismatch')
        F = [[0 if i == j else d[i] + d[j] - 14 + (17 - d[i] - d[j]) * R[i][j]
              - sum(R[i][k] * R[k][j] for k in range(22)) for j in range(22)] for i in range(22)]
        M = [row[:6] for row in R[6:]]
        G = [[sum(x[i] * x[j] for x in M) for j in range(6)] for i in range(6)]
        root = [row[:6] for row in R[:6]]
        for i in range(16):
            for j in range(6):
                rhs = (3 if j < 4 else 5 - 2 * M[i][j]) - sum(M[i][k] * root[k][j] for k in range(6)) - F[i + 6][j]
                require(sum(R[i + 6][k + 6] * M[k][j] for k in range(16)) == rhs, 'signed spine identity')
        f = [sum(row) for row in F]
        require(f[:6] == root_f(root), 'signed root incidence')
        require(f[6:] == [1 + 2 * (sum(x[:4]) - sum(x[4:])) for x in M], 'signed B incidence')
        require(sum(f[:6]) == -4 + 4 * (sum(root[i][j] for i, j in it.combinations(range(4), 2)) - root[4][5]), 'root budget identity')
        records.append({'R': R, 'F': F, 'G': G})
    return records


def run():
    root_summary = root_classification()
    parts = partitions()
    require(sorted(set(sum(v*v for v in p) for p in parts)) == [6, 8, 10, 12, 14, 18, 20], 'square sum range')
    require([p for p in parts if sum(v*v for v in p) == 20] == [(2, 4)], 'maximal square profile')
    for w in range(64):
        if DELTA[w] == 0:
            require(phi(w) == int(w == 0), 'zero-row empty-indicator polynomial')
    records, summaries = [], []
    expected_states = {(0, 1, 0, 0, 0, 0), (1, 0, 0, 0, 0, 0), (1, 2, 0, 0, 0, 0),
                       (2, 1, 0, 0, 0, 0), (2, 2, 0, 0, 0, 0)}
    expected_states |= {(1, 1) + tuple(int(i == j) for i in range(4)) for j in range(4)}
    seen = set()
    for profile in range(4):
        all_specs = list(root_weights(profile))
        kept = []
        for spec in all_specs:
            W = spec['W']
            if profile == 0:
                a, b = W[2][3], W[4][5]
                cross = [W[i][c] for i in (2, 3) for c in (4, 5)]
                require(spec['second'] == 20 - 2 * (a+b-sum(cross)) and spec['tau'][:2] == [5, 5], 'zero AC second-moment coefficients')
            elif profile == 1:
                require(spec['second'] == 24 + 2 * (W[2][4]+W[2][5]) - 2 * W[4][5], 'one AC second moment')
            elif profile == 2:
                require(spec['second'] == 26 - 2 * W[4][5], 'same C second moment')
            else:
                require(spec['second'] == 28 - 2 * W[4][5], 'different C second moment')
                require(16-spec['G'][4][4]-spec['G'][5][5]+spec['G'][4][5] == 4-W[4][5], 'different C neither count')
            moments = permitted_moments(spec, parts)
            entry = dict(spec, moments=moments)
            if moments:
                require(profile == 0, 'attached path contradicts written moment argument')
                key = (W[2][3], W[4][5]) + tuple(W[i][c] for i in (2, 3) for c in (4, 5))
                seen.add(key)
                entry['exclusion'] = analyze_zero(spec, moments)
                kept.append(entry['exclusion'])
            records.append(entry)
        summaries.append({'profile': NAMES[profile], 'root_pair_capacity_states': len(all_specs),
                          'necessary_moment_states': len(kept), 'exclusions': kept})
    require(seen == expected_states and len(seen) == 9, 'nine-state analytic classification')
    require([s['root_pair_capacity_states'] for s in summaries] == [56, 14, 3, 5], 'root capacity domains')
    controls = signed_controls()
    record = {'root_summary': root_summary, 'partitions_of_six_parts_at_most_four': sorted(parts),
              'root_pair_records': records, 'signed_controls': controls}
    summary = {'agent': 'six-books-1', 'role': 'researcher', 'complete': True,
               'scope': 'exact controls for a written ordinary argument; no host enumeration',
               'root_summary': root_summary, 'profiles': summaries,
               'signed_controls': len(controls), 'records_sha256': fingerprint(record),
               'ordinary_argument_controls_passed': True}
    return record, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records', type=Path, help='optional generated records outside the source directory')
    parser.add_argument('--report', type=Path, help='optional summary output')
    args = parser.parse_args()
    record, summary = run()
    expected = Path(__file__).with_name('degree98_root_eight_blue_expected.json')
    if expected.exists():
        require(json.loads(expected.read_text()) == summary, 'compact expected-output mismatch')
    if args.records:
        args.records.write_text(json.dumps(record, sort_keys=True, indent=2) + '\n')
    if args.report:
        args.report.write_text(json.dumps(summary, sort_keys=True, indent=2) + '\n')
    print(json.dumps(summary, sort_keys=True))


if __name__ == '__main__':
    main()
