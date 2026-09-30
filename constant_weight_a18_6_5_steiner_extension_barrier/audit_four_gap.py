"""Small complete kernel audit and direct checks of new actual record pairs."""
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import json
import random
import time

from geometry import classical_design, points, require
from generate_three_gap import find_clique
from verify_two_gap import enumerate_sets
from verify_three_gap import pair_graph
from verify_four_gap import clique_census, check_witness


def kernel_audit():
    start = time.monotonic()
    edges = list(combinations(range(6), 2))
    checked = 0
    for bits in range(1 << len(edges)):
        require(time.monotonic() - start < 45, 'INCOMPLETE: kernel audit guard')
        adjacency = [0] * 6
        for i, (u, v) in enumerate(edges):
            if bits >> i & 1:
                adjacency[u] |= 1 << v
                adjacency[v] |= 1 << u
        direct = {}
        for size in (3, 4, 5, 6):
            direct[size] = sum(all(adjacency[u] >> v & 1 for u, v in combinations(c, 2))
                               for c in combinations(range(6), size))
            witness, _ = find_clique(adjacency, size)
            require((witness is not None) == bool(direct[size]), 'production kernel disagrees with definition')
        try:
            census = clique_census(adjacency)
        except ValueError as e:
            require(str(e) == 'six-clique found' and direct[6] == 1, 'unexpected census rejection')
        else:
            require(direct[6] == 0 and census['triangles'] == direct[3]
                    and census['four_cliques'] == direct[4] and census['five_cliques'] == direct[5],
                    'independent census disagrees with direct enumeration')
        checked += 1
    return {'all_graphs_on_six_vertices': checked, 'production_targets': [3, 4, 5, 6],
            'seconds': time.monotonic() - start}


def actual_pairs(circles, expected):
    rng = random.Random(186507)
    summaries = []
    for kind, index in [('four', 0), ('single', 1), ('single', 6)]:
        entry = expected['four_cases' if kind == 'four' else 'single_cases'][index]
        records, _ = enumerate_sets(circles, entry['gaps'], 45)
        fixed = None
        if kind == 'single':
            fixed = expected['single_normalization']['fixed_old_four_set']
            fixed_set = frozenset(points(fixed))
            records = [(b, qs) for b, qs in records
                       if len(frozenset(points(b)) & fixed_set) <= 2
                       and all(len(frozenset(points(q)) & fixed_set) <= 1 for q in qs)]
        adjacency, _ = pair_graph(records)
        sample = sorted(rng.sample(range(len(records)), 48))
        pairs = set(combinations(sample, 2))
        positives = shared = 0
        for i, row in enumerate(adjacency):
            later = row & ~((1 << (i + 1)) - 1)
            if later:
                j = (later & -later).bit_length() - 1
                pairs.add((i, j))
                positives += 1
                if positives == 48:
                    break
        for i, j in sorted(pairs):
            b, qs = records[i]
            c, rs = records[j]
            b_set, c_set = frozenset(points(b)), frozenset(points(c))
            q_sets = [frozenset(points(q)) for q in qs]
            r_sets = [frozenset(points(r)) for r in rs]
            direct = b != c and len(b_set & c_set) <= 2 and all(
                q == r or len(q & r) <= 1 for q in q_sets for r in r_sets)
            require(direct == bool(adjacency[i] >> j & 1), 'record adjacency disagrees with direct sets')
            require(not direct or all(len(b_set & r) <= 2 for r in r_sets)
                    and all(len(c_set & q) <= 2 for q in q_sets), 'outsider/replacement bridge fails')
            if direct and set(qs) & set(rs):
                shared += 1
        witness_checks = 0
        if entry.get('witness'):
            check_witness(circles, records, entry['gaps'], entry['witness'], fixed)
            for corruption in ('duplicate', 'weight', 'parameter'):
                fixture = deepcopy(entry['witness'])
                if corruption == 'duplicate':
                    fixture['words'][-1] = fixture['words'][0]
                elif corruption == 'weight':
                    fixture['words'][0] ^= fixture['words'][0] & -fixture['words'][0]
                else:
                    fixture['g'] += 1
                try:
                    check_witness(circles, records, entry['gaps'], fixture, fixed)
                except ValueError:
                    witness_checks += 1
                else:
                    raise ValueError('corrupted witness was accepted')
        require(positives == 48, 'insufficient positive record controls')
        summaries.append({'kind': kind, 'case': index, 'direct_pairs': len(pairs),
                          'forced_positive_pairs': positives, 'shared_replacement_positive_pairs': shared,
                          'corrupted_witnesses_rejected': witness_checks})
    return summaries


def main():
    expected = json.loads(Path(__file__).with_name('four_gap_expected.json').read_text())
    kernels = kernel_audit()
    circles, _ = classical_design()
    print(json.dumps({'kernel_audit': kernels, 'actual_controls': actual_pairs(circles, expected)},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
