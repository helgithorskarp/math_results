#!/usr/bin/env python3
"""Exact signed-rectangle reduction and first test of a full-growth mechanism.

The mechanism would repair strict odd/even interleavings by increasing their
strong Bruhat down degree via even-value swaps. Stop at the first nonavoiding
local optimum. Infinite statements are separate author arguments, not finite
conclusions. No source from another executable is imported.
"""

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import time

from rectangle_checker import boxed_occurrences


def graph(permutation):
    return tuple((i, j) for i, j in itertools.combinations(range(len(permutation)), 2)
                 if not any(min(permutation[i], permutation[j]) < permutation[k] <
                            max(permutation[i], permutation[j]) for k in range(i + 1, j)))


def negative_edges(permutation):
    return tuple((i, j) for i, j in graph(permutation) if permutation[i] > permutation[j])


def inversion_length(permutation):
    return sum(permutation[i] > permutation[j] for i, j in itertools.combinations(range(len(permutation)), 2))


def transpose(permutation, i, j):
    result = list(permutation)
    result[i], result[j] = result[j], result[i]
    return tuple(result)


def interleave(permutation, scaffold):
    return tuple(y for i, x in enumerate(permutation) for y in
                 ((2 * x - 1, 2 * scaffold[i]) if i < len(scaffold) else (2 * x - 1,)))


def controls():
    parents = swaps = quads = 0
    stream = hashlib.sha256()
    clique_types = Counter()
    for n in range(8):
        for permutation in itertools.permutations(range(1, n + 1)):
            edges = set(graph(permutation))
            minus = {(i, j) for i, j in edges if permutation[i] > permutation[j]}
            if n <= 6:
                length = inversion_length(permutation)
                for i, j in itertools.combinations(range(n), 2):
                    delta = inversion_length(transpose(permutation, i, j)) - length
                    assert (abs(delta) == 1) == ((i, j) in edges)
                    assert ((delta == -1) == ((i, j) in minus))
                    swaps += 1
            selected = []
            for indices in itertools.combinations(range(n), 4):
                pairs = tuple(itertools.combinations(indices, 2))
                if all(pair in edges for pair in pairs):
                    values = tuple(permutation[i] for i in indices)
                    pattern = tuple(1 + sum(y < x for y in values) for x in values)
                    assert pattern in ((2, 1, 4, 3), (2, 4, 1, 3), (3, 1, 4, 2), (3, 4, 1, 2))
                    clique_types[pattern] += 1
                    if sum(pair in minus for pair in pairs) == 2:
                        selected.append(indices)
                quads += 1
            actual = boxed_occurrences(permutation)
            assert tuple(selected) == actual
            stream.update((json.dumps([permutation, sorted(edges), sorted(minus), actual],
                                     separators=(',', ':')) + '\n').encode())
            parents += 1
    return {'complete_permutations_through7': parents, 'transpositions_through6': swaps,
            'quadruples_checked': quads, 'signed_graph_stream_sha256': stream.hexdigest(),
            'all_K4_relative_patterns': {''.join(map(str, k)): v for k, v in sorted(clique_types.items())}}


def test_ascent():
    histories = []
    tested = forbidden = 0
    for m in range(2, 6):
        complete = 0
        for permutation in itertools.permutations(range(1, m + 1)):
            for scaffold in itertools.permutations(range(1, m)):
                word = interleave(permutation, scaffold)
                occurrence_set = boxed_occurrences(word)
                complete += 1
                tested += 1
                if not occurrence_set:
                    continue
                forbidden += 1
                degree = len(negative_edges(word))
                neighbors = []
                for i, j in itertools.combinations(range(m - 1), 2):
                    changed = transpose(scaffold, i, j)
                    child = interleave(permutation, changed)
                    neighbors.append({'scaffold_positions_swapped': (i, j), 'rho': changed,
                                      'word': child, 'down_degree': len(negative_edges(child)),
                                      'occurrences': boxed_occurrences(child)})
                if all(row['down_degree'] <= degree for row in neighbors):
                    all_scaffolds = []
                    for rho in itertools.permutations(range(1, m)):
                        child = interleave(permutation, rho)
                        all_scaffolds.append({'rho': rho, 'down_degree': len(negative_edges(child)),
                                              'avoids': not boxed_occurrences(child)})
                    histories.append({'m': m, 'complete_input_scaffold_pairs': complete, 'complete_length': False})
                    return {'scope_rows': histories, 'input_scaffold_pairs_tested': tested,
                            'nonavoiding_pairs_tested': forbidden,
                            'strict_ascent_failure': {'m': m, 'pi': permutation, 'rho': scaffold,
                                'word': word, 'down_degree': degree,
                                'negative_edges_zero_based_positions': negative_edges(word),
                                'boxed_occurrences': occurrence_set, 'all_even_transposition_neighbors': neighbors,
                                'all_scaffold_scores_for_this_input': all_scaffolds,
                                'is_global_down_degree_maximizer_for_input':
                                     degree == max(row['down_degree'] for row in all_scaffolds)}}
        histories.append({'m': m, 'complete_input_scaffold_pairs': complete, 'complete_length': True})
    return {'scope_rows': histories, 'input_scaffold_pairs_tested': tested,
            'nonavoiding_pairs_tested': forbidden, 'strict_ascent_failure': None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    began = time.perf_counter()
    result = {'actor': 'literature-researcher-4', 'checker': None, 'decision_message_id': 410,
              'full_target_solved': False, 'status': 'new exact partial reduction/mechanism test awaiting separate review',
              'graph_controls': controls(), 'ascent_probe': test_ascent(),
              'python': platform.python_version(), 'seconds': time.perf_counter() - began,
              'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'processes': 1, 'native_threads': 1}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
