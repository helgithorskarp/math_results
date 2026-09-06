#!/usr/bin/env python3
"""Separate literal verifier. Imports no extractor or mathematical bounds."""
import json
import sys


def verify(graph, certificate):
    def need(ok):
        if not ok:
            raise ValueError('invalid physical graph or five-set certificate')
    need(type(graph) is dict and set(graph) == {'n', 'red_edges', 'module', 'deleted'})
    need(type(graph['n']) is int and graph['n'] == 43)
    matrix = [[False] * 43 for _ in range(43)]
    last = (-1, -1)
    need(type(graph['red_edges']) is list)
    for pair in graph['red_edges']:
        need(type(pair) is list and len(pair) == 2)
        need(all(type(x) is int for x in pair))
        u, v = pair
        need(0 <= u < v < 43 and (u, v) > last)
        last = (u, v)
        matrix[u][v] = matrix[v][u] = True
    # Family membership is deliberately not a premise of a physical K5 check.
    need(type(certificate) is dict and set(certificate) == {'vertices', 'color', 'reason'})
    q, c = certificate['vertices'], certificate['color']
    need(type(c) is int and c in (0, 1))
    need(type(q) is list and len(q) == 5)
    need(all(type(v) is int and 0 <= v < 43 for v in q))
    need(len(set(q)) == 5 and q == sorted(q))
    for i in range(5):
        for j in range(i):
            need(matrix[q[i]][q[j]] == bool(c))
    return 'VERIFIED_PHYSICAL_MONOCHROMATIC_FIVE'


if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf8') as f:
        graph = json.load(f)
    with open(sys.argv[2], encoding='utf8') as f:
        certificate = json.load(f)
    print(verify(graph, certificate))
