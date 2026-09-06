#!/usr/bin/env python3
"""Truth-table reconstruction of all physical switching clauses and parity data."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from check_certificate import input_rows
from drat import clause, require


def lookup():
    pairs = list(combinations(range(5), 2))
    table = []
    for graph in range(1024):
        patterns = []
        for spins in range(32):
            colors = {((graph >> bit) ^ (spins >> u) ^ (spins >> v)) & 1
                      for bit, (u, v) in enumerate(pairs)}
            if len(colors) == 1:
                patterns.append((colors.pop(), spins))
        table.append(patterns)
    return table


def triangle_counts(rows):
    counts = Counter({pair: 0 for pair in combinations(range(41), 2)})
    for a, b, c in combinations(range(41), 3):
        odd = ((rows[a] >> b) ^ (rows[a] >> c) ^ (rows[b] >> c)) & 1
        if odd:
            counts[a, b] += 1
            counts[a, c] += 1
            counts[b, c] += 1
    return counts


def audit(work):
    rows, labels = input_rows()
    expected_core = ('41\n'+''.join(f'{u} {v}\n' for u, v in combinations(range(41), 2)
                                   if rows[u] & (1 << v))).encode()
    require((work/'core.edges').read_bytes() == expected_core, 'induced core reconstruction')
    require(json.loads((work/'labels.json').read_text()) == labels, 'original labels')
    table = lookup()
    expected, colors = set(), Counter()
    for q in combinations(range(41), 5):
        code = sum(int(bool(rows[u] & (1 << v))) << j for j, (u, v) in enumerate(combinations(q, 2)))
        for color, spins in table[code]:
            if q[0] == 0 and spins & 1:
                continue
            literals = tuple(-v if spins & (1 << i) else v for i, v in enumerate(q) if v)
            require(literals not in expected, 'duplicate reconstructed clause')
            expected.add(literals)
            colors[color] += 1
    raw = (work/'switch.cnf').read_bytes()
    lines = raw.decode().splitlines()
    require(lines[0] == f'p cnf 40 {len(expected)}', 'complete formula header')
    actual = [tuple(clause(line)) for line in lines[1:]]
    require(actual == sorted(expected), 'complete physical formula equality')
    counts = triangle_counts(rows)
    # Independent Paley implementation uses Euler's criterion, not residue sets.
    paley_rows = [sum(1 << v for v in range(41) if v != u and pow((u-v) % 41, 20, 41) == 1) for u in range(41)]
    paley = triangle_counts(paley_rows)
    ch = [[k, m] for k, m in sorted(Counter(counts.values()).items())]
    ph = [[k, m] for k, m in sorted(Counter(paley.values()).items())]
    witness = next([u, v, value] for (u, v), value in sorted(counts.items()) if value not in set(paley.values()))
    expected_summary = {'vertices': 41, 'deleted_parent_vertices': [33, 35],
        'red_edges': sum(row.bit_count() for row in rows)//2,
        'parent_sha256': sha256((Path(__file__).resolve().parent/'parent.edges').read_bytes()).hexdigest(),
        'core_sha256': sha256(expected_core).hexdigest(), 'switch_variables': 40, 'normalization': 's_0=0',
        'physical_five_sets': 749398, 'cnf_clauses': len(expected),
        'clause_colors_blue_red': [colors[0], colors[1]],
        'clause_widths': dict(sorted(Counter(map(len, expected)).items())),
        'cnf_bytes': len(raw), 'cnf_sha256': sha256(raw).hexdigest(),
        'core_pair_odd_triangle_histogram': ch, 'paley_pair_odd_triangle_histogram': ph,
        'distinguishing_pair_local_labels_and_count': witness}
    require(json.loads((work/'summary.json').read_text()) == json.loads(json.dumps(expected_summary)), 'complete summary')
    return {'status': 'VERIFIED_EXACT_CORE_SWITCH_FORMULA', 'physical_five_sets': 749398,
            'base_graph_truth_cases': 32768, 'cnf_sha256': sha256(raw).hexdigest(),
            'clauses': len(expected), 'core_sha256': sha256(expected_core).hexdigest(),
            'parity_data_verified': True, 'outside_paley_switching_class': True,
            'distinguishing_pair_local_labels_and_count': witness}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = audit(a.work)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(result['status'], result['clauses'], 'clauses')
