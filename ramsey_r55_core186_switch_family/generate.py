#!/usr/bin/env python3
"""Complete switching-class CNF for the prescribed 41-vertex induced core."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT_SHA = 'f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def parent_core():
    raw = (HERE/'parent.edges').read_bytes()
    need(sha256(raw).hexdigest() == PARENT_SHA, 'parent hash')
    lines = raw.decode().splitlines()
    need(lines[0] == '43', 'parent order')
    pairs = [tuple(map(int, s.split())) for s in lines[1:]]
    need(pairs == sorted(set(pairs)), 'canonical parent pairs')
    need(all(0 <= a < b < 43 for a, b in pairs), 'parent pair range')
    labels = [v for v in range(43) if v not in (33, 35)]
    parent = set(pairs)
    core = {(a, b) for a, b in combinations(range(41), 2) if (labels[a], labels[b]) in parent}
    return labels, core


def patterns(vertices, red):
    """For each color, anchor one spin; all others are forced up to complement."""
    first = vertices[0]
    for color in (0, 1):
        spins = {first: 0}
        for v in vertices[1:]:
            spins[v] = int((first, v) in red) ^ color
        if all((int((a, b) in red) ^ spins[a] ^ spins[b]) == color
               for a, b in combinations(vertices, 2)):
            for flip in (0, 1):
                yield color, {v: bit ^ flip for v, bit in spins.items()}


def full_formula(red, n=41):
    clauses = set()
    colors = Counter()
    for q in combinations(range(n), 5):
        for color, spins in patterns(q, red):
            if spins.get(0, 0) != 0:
                continue
            row = tuple(-v if spins[v] else v for v in q if v != 0)
            need(row not in clauses, 'duplicate physical event')
            clauses.add(row)
            colors[color] += 1
    return sorted(clauses), colors


def parity_histogram(n, red):
    values = {}
    for a, b in combinations(range(n), 2):
        values[a, b] = sum(int((a, b) in red) ^ int(tuple(sorted((a, v))) in red)
                          ^ int(tuple(sorted((b, v))) in red)
                          for v in range(n) if v != a and v != b)
    return [[x, m] for x, m in sorted(Counter(values.values()).items())], values


def run(out):
    out.mkdir(parents=True, exist_ok=False)
    labels, red = parent_core()
    core = ('41\n'+''.join(f'{u} {v}\n' for u, v in sorted(red))).encode()
    (out/'core.edges').write_bytes(core)
    (out/'labels.json').write_text(json.dumps(labels)+'\n')
    clauses, colors = full_formula(red)
    raw = (f'p cnf 40 {len(clauses)}\n'+''.join(' '.join(map(str, row))+' 0\n' for row in clauses)).encode()
    (out/'switch.cnf').write_bytes(raw)
    hist, values = parity_histogram(41, red)
    residues = {x*x % 41 for x in range(1, 41)}
    paley = {(a, b) for a, b in combinations(range(41), 2) if (a-b) % 41 in residues}
    ph, _ = parity_histogram(41, paley)
    possible = {q for q, _ in ph}
    witness = next([a, b, count] for (a, b), count in values.items() if count not in possible)
    summary = {'vertices': 41, 'deleted_parent_vertices': [33, 35], 'red_edges': len(red),
               'parent_sha256': PARENT_SHA, 'core_sha256': sha256(core).hexdigest(),
               'switch_variables': 40, 'normalization': 's_0=0', 'physical_five_sets': 749398,
               'cnf_clauses': len(clauses), 'clause_colors_blue_red': [colors[0], colors[1]],
               'clause_widths': dict(sorted(Counter(map(len, clauses)).items())),
               'cnf_bytes': len(raw), 'cnf_sha256': sha256(raw).hexdigest(),
               'core_pair_odd_triangle_histogram': hist, 'paley_pair_odd_triangle_histogram': ph,
               'distinguishing_pair_local_labels_and_count': witness}
    (out/'summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True)+'\n')
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    run(p.parse_args().out)
