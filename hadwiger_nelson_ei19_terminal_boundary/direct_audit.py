"""Directly extend all labelled pin colourings, without reading witnesses.

Uses ordinary domain backtracking, no SAT, colour symmetry, or restricted-growth
pattern generator. This is author-side algorithmic checking, not peer review.
"""
from pathlib import Path
from collections import Counter
import json
import time

HERE = Path(__file__).resolve().parent


def run():
    edge_list = json.loads((HERE / 'geometry_certificate.json').read_text())['edge_equations']
    adjacency = [set() for _ in range(19)]
    for a, b in edge_list:
        adjacency[a].add(b)
        adjacency[b].add(a)
    terminals = [v for v in range(19) if len(adjacency[v]) == 3]
    colours = [-1] * 19
    search_nodes = 0

    def extend(k):
        nonlocal search_nodes
        search_nodes += 1
        choice = None
        domain = None
        for v in range(19):
            if colours[v] >= 0:
                continue
            available = set(range(k)) - {colours[w] for w in adjacency[v]}
            if not available:
                return None
            if domain is None or len(available) < len(domain):
                choice, domain = v, available
        if choice is None:
            if any(colours[a] == colours[b] for a, b in edge_list):
                raise RuntimeError('bad direct colouring')
            return tuple(colours)
        for c in sorted(domain):
            colours[choice] = c
            result = extend(k)
            colours[choice] = -1
            if result is not None:
                return result
        return None

    # Complete no-symmetry exhaustion also rechecks the known chi=4 status.
    if extend(3) is not None:
        raise RuntimeError('unexpected three-colouring')
    three_nodes = search_nodes
    search_nodes = 0
    histogram = Counter()
    edge_checks = 0

    def pin(i):
        nonlocal edge_checks
        if i == len(terminals):
            before = tuple(colours[v] for v in terminals)
            word = extend(4)
            if word is None:
                raise RuntimeError(('nonextendible labelled pattern', before))
            if (tuple(word[v] for v in terminals) != before
                    or any(word[a] == word[b] for a, b in edge_list)):
                raise RuntimeError('direct extension does not check')
            histogram[len(set(before))] += 1
            edge_checks += len(edge_list)
            return
        v = terminals[i]
        for c in range(4):
            if any(colours[w] == c for w in adjacency[v]):
                continue
            colours[v] = c
            pin(i + 1)
            colours[v] = -1

    pin(0)
    if sum(histogram.values()) != 103680:
        raise RuntimeError('labelled enumeration count')
    return {'status': 'ALL LABELLED TERMINAL COLOURINGS EXTEND',
            'labelled_terminal_colourings': sum(histogram.values()),
            'patterns_by_colours_used': dict(sorted(histogram.items())),
            'edge_inequalities_checked': edge_checks,
            'four_colour_search_nodes': search_nodes,
            'three_colour_exhaustion_nodes': three_nodes,
            'chromatic_number': 4, 'reads_completion_certificate': False,
            'SAT_imported': False, 'colour_symmetry_pruning': False}


if __name__ == '__main__':
    start = time.perf_counter()
    result = run()
    result['seconds'] = time.perf_counter() - start
    print(json.dumps(result, indent=2))
