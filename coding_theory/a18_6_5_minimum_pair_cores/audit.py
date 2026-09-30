#!/usr/bin/env python3
"""Audit both clique enumerators against brute force on every graph of order <=5."""
import itertools
import json

import generate
import verify


def main():
    graphs = queries = 0
    for n in range(6):
        edges = list(itertools.combinations(range(n), 2))
        for graph in range(1 << len(edges)):
            graphs += 1
            for labels in (list(range(n)), [3 * v + 2 for v in range(n)]):
                size = max(labels, default=-1) + 1
                sets = [set() for _ in range(size)]
                for i, (a, b) in enumerate(edges):
                    if graph >> i & 1:
                        sets[labels[a]].add(labels[b])
                        sets[labels[b]].add(labels[a])
                bits = [sum(1 << v for v in neighbors) for neighbors in sets]
                active = sum(1 << v for v in labels)
                maximum = 0
                for target in range(n + 2):
                    expected = [chosen for chosen in itertools.combinations(labels, target)
                                if all(b in sets[a] for a, b in itertools.combinations(chosen, 2))]
                    if expected:
                        maximum = target
                    if generate.cliques(bits, active, target) != expected:
                        raise ValueError('ordered enumeration differs from brute force')
                    if verify.cliques(sets, labels, target) != expected:
                        raise ValueError('maximal-clique enumeration differs from brute force')
                    queries += 1
                if generate.cover_bound(bits, active) < maximum:
                    raise ValueError('conflict cover is not an upper bound')
    if graphs != 1100 or queries != 15210:
        raise ValueError('audit coverage differs')
    print(json.dumps({'simple_graphs': graphs, 'labelings_per_graph': 2,
                      'target_queries_per_algorithm': queries,
                      'comparison': 'exact brute-force compatible subsets'}))


if __name__ == '__main__':
    main()
