"""Definition-level verifier for a literal red-edge list, independent of generators."""
import argparse
import json
from itertools import combinations
from pathlib import Path


def verify(doc):
    n = doc.get('n')
    if type(n) is not int or not 5 <= n <= 49:
        raise ValueError('order must be an integer in 5..49')
    raw = doc.get('edges')
    if type(raw) is not list or not all(type(e) is list and len(e) == 2
                                      and all(type(x) is int for x in e) for e in raw):
        raise ValueError('edge format')
    edges = [tuple(e) for e in raw]
    if edges != sorted(set(edges)) or not all(0 <= u < v < n for u, v in edges):
        raise ValueError('canonical simple edges')
    red = set(edges)
    counts = [0, 0]
    for q in combinations(range(n), 5):
        c = int((q[0], q[1]) in red)
        if all(int(pair in red) == c for pair in combinations(q, 2)):
            counts[c] += 1
    return {'n': n, 'red_edges': len(edges), 'blue_red_five_sets': counts,
            'ramsey_5_5_graph': counts == [0, 0]}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('graph', type=Path)
    args = ap.parse_args()
    print(json.dumps(verify(json.loads(args.graph.read_text())), indent=2, sort_keys=True))
