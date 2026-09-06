#!/usr/bin/env python3
"""Direct hereditary obstruction inside the input's 33 moving vertices."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def audit():
    raw = (HERE/'input.edges').read_bytes()
    if hashlib.sha256(raw).hexdigest() != 'f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441':
        raise ValueError('input identity')
    lines = raw.decode().splitlines()
    if lines[0] != '43':
        raise ValueError('input order')
    red = {tuple(map(int, line.split())) for line in lines[1:]}
    bad = [[], []]
    for q in combinations(range(33), 5):
        edge_colors = {e in red for e in combinations(q, 2)}
        if len(edge_colors) == 1:
            bad[int(edge_colors.pop())].append(list(q))
    complete = json.loads((HERE/'verification.json').read_text())['graphs'][0]['bad_sets_blue_red']
    expected = [[q for q in color if max(q) < 33] for color in complete]
    if expected != bad:
        raise ValueError('moving-only/whole-graph physical list mismatch')
    distribution = [dict(sorted(Counter(sum(v >= 33 for v in q) for q in group).items())) for group in complete]
    return {'fixed_induced_vertices': list(range(33)), 'moving_only_counts_blue_red': list(map(len, bad)),
            'moving_only_total': sum(map(len, bad)), 'one_witness_per_color_blue_red': [qs[0] for qs in bad],
            'base_bad_sets_by_fixed_vertex_count_blue_red': distribution,
            'no_ramsey_graph_can_preserve_this_induced_coloring': sum(map(len, bad)) > 0}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    result = audit()
    a.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print('VERIFIED moving-only obstruction:', result['moving_only_counts_blue_red'], 'blue/red')
