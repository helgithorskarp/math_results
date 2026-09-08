#!/usr/bin/env python3
"""A necessary physical-edge filter. Passing this filter is not Ramsey validity."""
import argparse
import json
from pathlib import Path


def assess(obj):
    if not isinstance(obj, dict) or set(obj) != {'n', 'red_edges'} or type(obj['n']) is not int or obj['n'] != 43:
        raise ValueError('expected exactly n:43 and red_edges')
    edges = obj['red_edges']
    if not isinstance(edges, list):
        raise ValueError('red_edges must be a list')
    previous = None
    for edge in edges:
        if (not isinstance(edge, list) or len(edge) != 2 or
                any(type(x) is not int for x in edge) or not 0 <= edge[0] < edge[1] < 43):
            raise ValueError('invalid physical edge')
        current = tuple(edge)
        if previous is not None and current <= previous:
            raise ValueError('edges must be strictly lexicographically increasing')
        previous = current
    m = len(edges)
    return {'n': 43, 'red_edges': m, 'blue_edges': 903 - m,
            'status': ('NOT_EXCLUDED_BY_EDGE_WINDOW' if 390 <= m <= 513
                       else 'EXCLUDED_BY_GLOBAL_EDGE_WINDOW'),
            'necessary_red_edge_interval': [390, 513], 'is_target_certificate': False}


def self_check():
    from itertools import combinations
    pairs = [list(p) for p in combinations(range(43), 2)]
    checked = 0
    for m in [0, 386, 387, 388, 389, 390, 430, 451, 473, 513, 514, 515, 516, 517, 903]:
        obj = {'n': 43, 'red_edges': pairs[:m]}
        result = assess(obj)
        if (result['status'] == 'NOT_EXCLUDED_BY_EDGE_WINDOW') != (390 <= m <= 513):
            raise ValueError('edge boundary control')
        reverse = assess({'n': 43, 'red_edges': pairs[m:]})
        if reverse['status'] != result['status']:
            raise ValueError('color reversal control')
        checked += 2
    malformed = [None, {}, {'n': 42, 'red_edges': []}, {'n': True, 'red_edges': []},
                 {'n': 43, 'red_edges': [[0, 0]]}, {'n': 43, 'red_edges': [[0, 43]]},
                 {'n': 43, 'red_edges': [[1, 0]]}, {'n': 43, 'red_edges': [[0, True]]},
                 {'n': 43, 'red_edges': [[0, 1], [0, 1]]},
                 {'n': 43, 'red_edges': [[0, 2], [0, 1]]},
                 {'n': 43, 'red_edges': [], 'extra': 1}]
    for obj in malformed:
        try:
            assess(obj)
        except ValueError:
            continue
        raise ValueError('malformed input was accepted')
    return {'status': 'VERIFIED_EDGE_WINDOW_INTERFACE', 'boundary_and_color_controls': checked,
            'malformed_inputs_rejected': len(malformed)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--graph', type=Path)
    group.add_argument('--self-check', action='store_true')
    args = parser.parse_args()
    result = self_check() if args.self_check else assess(json.loads(args.graph.read_text()))
    print(json.dumps(result, sort_keys=True))
