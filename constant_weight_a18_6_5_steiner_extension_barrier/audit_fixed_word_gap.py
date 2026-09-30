"""Direct small-graph, actual-pair and corrupted-witness controls.
Agent: six-code-2, researcher. Standard library exact arithmetic only.
"""
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import json
import random
import time
from geometry import classical_design, points, require
from generate_three_gap import find_clique
from verify_three_gap import pair_graph
from verify_fixed_word_gap import enumerate_sets, clique_census, check_witness


def direct_counts(adjacency):
    n = len(adjacency)
    counts = {}
    for k in range(1, n + 1):
        counts[k] = sum(all(adjacency[i] >> j & 1 for i, j in combinations(c, 2))
                        for c in combinations(range(n), k))
    return counts


def graph_controls():
    start = time.monotonic()
    graphs = []
    pairs = list(combinations(range(5), 2))
    for bits in range(1 << len(pairs)):
        rows = [0] * 5
        for k, (i, j) in enumerate(pairs):
            if bits >> k & 1:
                rows[i] |= 1 << j
                rows[j] |= 1 << i
        graphs.append(rows)
    # Exact eight-vertex controls include complete multipartite graphs,
    # disconnected cliques, and a reproducible varied edge family.
    for parts in range(1, 9):
        graphs.append([sum(1 << j for j in range(8) if i % parts != j % parts)
                       for i in range(8)])
        graphs.append([sum(1 << j for j in range(8) if j != i and i % parts == j % parts)
                       for i in range(8)])
    rng = random.Random(20260930)
    for _ in range(256):
        rows = [0] * 8
        for i, j in combinations(range(8), 2):
            if rng.randrange(2):
                rows[i] |= 1 << j
                rows[j] |= 1 << i
        graphs.append(rows)
    checked = 0
    for adjacency in graphs:
        require(time.monotonic() - start < 45, 'INCOMPLETE: small-graph audit guard')
        counts = direct_counts(adjacency)
        for forbidden in range(2, 9):
            expected_absent = counts.get(forbidden, 0) == 0
            try:
                census = clique_census(adjacency, forbidden)
            except ValueError as e:
                require(str(e) == 'purported forbidden clique exists' and not expected_absent,
                        'incorrect census rejection')
            else:
                require(expected_absent, 'missed direct clique')
                require(all(census['cliques_by_size'][str(k)] == counts.get(k, 0)
                            for k in range(1, forbidden + 1)), 'direct census mismatch')
            if forbidden >= 7:
                indices, coverage = find_clique(adjacency, forbidden)
                require(coverage['complete'] and (indices is None) == expected_absent,
                        'production search/direct definition mismatch')
                if indices is not None:
                    require(len(indices) == len(set(indices)) == forbidden
                            and all(adjacency[i] >> j & 1 for i, j in combinations(indices, 2)),
                            'invalid production small-graph witness')
            checked += 1
    return {'graphs': len(graphs), 'all_five_vertex_graphs': 1024,
            'structured_eight_vertex_graphs': 16, 'seeded_eight_vertex_graphs': 256,
            'seed': 20260930, 'census_checks': checked, 'seconds': time.monotonic() - start}


def actual_controls(expected):
    circles, _ = classical_design()
    comparisons, identical_positives, corruptions = 0, 0, 0
    for branch, case_id in (('pair', 2), ('single', 83)):
        norm = expected[branch + '_normalization']
        case = norm['cases'][case_id]
        fixture = expected[branch + '_cases'][case_id]['witness']
        fixed = (norm['fixed_four_set'],) if branch == 'single' else (norm['fixed_four_set'], case['second_four_set'])
        records, _ = enumerate_sets(circles, case['gaps'], fixed)
        adjacency, _ = pair_graph(records)
        n = len(records)
        selected = {i * (n - 1) // 39 for i in range(40)} | set(fixture['indices'])
        # Include actual compatible pairs sharing an identical replacement.
        added = 0
        for i, row in enumerate(adjacency):
            if added == 12:
                break
            candidates = row
            while candidates:
                bit = candidates & -candidates
                j = bit.bit_length() - 1
                candidates ^= bit
                if set(records[i][1]) & set(records[j][1]):
                    selected.update((i, j))
                    added += 1
                    break
        require(added == 12, 'missing positive shared-word controls')
        for i, j in combinations(sorted(selected), 2):
            b, qs = records[i]
            c, rs = records[j]
            old_b, old_c = frozenset(points(b)), frozenset(points(c))
            replacements = [frozenset(points(q)) | {17} for q in set(qs) | set(rs) | set(fixed)]
            words = [old_b, old_c] + replacements
            directly_compatible = (b != c and all(len(a & d) <= 2 for a, d in combinations(words, 2)))
            require(bool(adjacency[i] >> j & 1) == directly_compatible,
                    'actual graph/direct word compatibility mismatch')
            comparisons += 1
            if directly_compatible and set(qs) & set(rs):
                identical_positives += 1
        check_witness(circles, records, case['gaps'], fixture, fixed)
        damaged = []
        for mode in range(5):
            bad = deepcopy(fixture)
            if mode == 0:
                bad['words'][0] = bad['words'][1]
            elif mode == 1:
                bad['words'][0] = -1
            elif mode == 2:
                bad['words'][0] ^= 1 << 17
            elif mode == 3:
                bad['t'] += 1
            else:
                bad['indices'][0] = len(records)
            damaged.append(bad)
        for bad in damaged:
            try:
                check_witness(circles, records, case['gaps'], bad, fixed)
            except ValueError:
                corruptions += 1
            else:
                raise ValueError('corrupted witness accepted')
    require(identical_positives > 0 and corruptions == 10, 'incomplete actual controls')
    return {'actual_pairs': comparisons, 'positive_shared_replacement_pairs': identical_positives,
            'corrupted_witnesses_rejected': corruptions}


def main():
    expected = json.loads(Path(__file__).with_name('fixed_word_gap_expected.json').read_text())
    print(json.dumps({'graph_controls': graph_controls(), 'actual_controls': actual_controls(expected)}, indent=2))


if __name__ == '__main__':
    main()
