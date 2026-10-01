#!/usr/bin/env python3
"""Exhaustive tiny cover/clique controls and explicit incomplete guards."""
import argparse
from itertools import combinations, product
import json
from pathlib import Path

from covers import group_covers, need
from packing import find_clique


def run():
    graphs = tests = 0
    for n in range(6):
        edges = list(combinations(range(n), 2))
        for code in range(1 << len(edges)):
            adj = [set() for _ in range(n)]
            for bit, (i, j) in enumerate(edges):
                if code >> bit & 1:
                    adj[i].add(j)
                    adj[j].add(i)
            for k in range(n+2):
                brute = any(all(v in adj[u] for u, v in combinations(C, 2))
                            for C in combinations(range(n), k))
                found, _ = find_clique(adj, k)
                need((found is not None) == brute, 'every tiny graph and clique size')
                tests += 1
            graphs += 1
    need(graphs == 1100, 'all undirected graphs through five vertices')
    universe = frozenset(range(3))
    systems = positive = solutions = 0
    for codes in product(range(1, 8), repeat=3):
        options = [[(((g, p),), frozenset({p})) for p in range(3) if code >> p & 1]
                   for g, code in enumerate(codes)]
        brute = sorted(tuple(sorted(tag for alternative in choice for tag in alternative[0]))
                       for choice in product(*options)
                       if len(set().union(*(a[1] for a in choice))) == 3)
        rebuilt, _ = group_covers(options, universe)
        need(brute == rebuilt, 'every tiny grouped cover entry')
        systems += 1
        positive += bool(brute)
        solutions += len(brute)
    need(systems == 343, 'all nonempty three-group atomic cover systems')
    guards = 0
    for call in [lambda: find_clique([{1}, {0}], 2, state_limit=1),
                 lambda: find_clique([{1}, {0}], 2, seconds=0),
                 lambda: group_covers([[(((0,),), frozenset({0}))]], frozenset({0}), state_limit=1),
                 lambda: group_covers([[(((0,),), frozenset({0}))]], frozenset({0}), seconds=0)]:
        rejected = False
        try:
            call()
        except RuntimeError as exc:
            rejected = str(exc).startswith('INCOMPLETE:')
        need(rejected, 'incomplete guard cannot supply a negative verdict')
        guards += 1
    rejected = False
    try:
        find_clique([{1}, set()], 2)
    except ValueError:
        rejected = True
    need(rejected, 'asymmetric graph rejected')
    return {'tiny_undirected_graphs': graphs, 'all_clique_target_tests': tests,
            'complete_atomic_cover_systems': systems, 'positive_cover_systems': positive,
            'full_cover_solutions_compared': solutions, 'actual_incomplete_guards_rejected': guards,
            'asymmetric_graph_rejected': True, 'complete': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path)
    args = parser.parse_args()
    result = run()
    if args.expected:
        need(result == json.loads(args.expected.read_text()), 'controls expected output')
    print(json.dumps(result, indent=2, sort_keys=True))
