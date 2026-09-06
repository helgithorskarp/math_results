#!/usr/bin/env python3
"""Independent truth-table reconstruction; no generator import."""
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


def cliques(rows, k, candidates=None, chosen=()):
    """Bit-intersection recursion, separate from literal five-set counting."""
    if not k:
        yield chosen
        return
    if candidates is None:
        candidates = (1 << len(rows))-1
    while candidates.bit_count() >= k:
        bit = candidates & -candidates
        candidates ^= bit
        v = bit.bit_length()-1
        yield from cliques(rows, k-1, candidates & rows[v], chosen+(v,))


def audit(work):
    rows, labels = input_rows()
    require(len(rows) == 33 and labels == list(range(33)), 'all moving vertices')
    action = [3*(v//3)+(v+1)%3 for v in range(33)]
    require(all(((rows[u] >> v) & 1) == ((rows[action[u]] >> action[v]) & 1)
                for u, v in combinations(range(33), 2)), 'parent C3 invariance')
    expected_core = ('33\n'+''.join(f'{u} {v}\n' for u, v in combinations(range(33), 2)
                                   if rows[u] & (1 << v))).encode()
    require((work/'core.edges').read_bytes() == expected_core, 'induced core reconstruction')
    require(json.loads((work/'labels.json').read_text()) == labels, 'original labels')
    table = lookup()
    expected, colors = set(), Counter()
    for q in combinations(range(33), 5):
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
    require(lines[0] == f'p cnf 32 {len(expected)}', 'complete formula header')
    require([tuple(clause(line)) for line in lines[1:]] == sorted(expected), 'complete clause equality')
    mask = (1 << 33)-1
    blue = [mask ^ row ^ (1 << u) for u, row in enumerate(rows)]
    defects = [len(list(cliques(color, 5))) for color in (blue, rows)]
    free_pairs = [(u, v) for u, v in combinations(range(43), 2) if v >= 33]
    # Explicit pair-orbit reconstruction checks the 155 free C3 contacts.
    g = action + list(range(33, 43))
    todo = set(free_pairs)
    orbit_sizes = Counter()
    while todo:
        u, v = min(todo)
        orbit = {tuple(sorted((u, v))), tuple(sorted((g[u], g[v]))),
                 tuple(sorted((g[g[u]], g[g[v]])))}
        require(orbit <= todo, 'whole attachment orbit')
        todo -= orbit
        orbit_sizes[len(orbit)] += 1
    require(orbit_sizes == {1: 45, 3: 110}, 'free C3 attachment orbit counts')
    expected_summary = {'vertices': 33, 'deleted_parent_vertices': list(range(33, 43)),
        'red_edges': sum(row.bit_count() for row in rows)//2,
        'parent_sha256': sha256((Path(__file__).resolve().parent/'parent.edges').read_bytes()).hexdigest(),
        'core_sha256': sha256(expected_core).hexdigest(), 'switch_variables': 32,
        'normalization': 's_0=0', 'physical_five_sets': 237336,
        'cnf_clauses': len(expected), 'clause_colors_blue_red': [colors[0], colors[1]],
        'clause_widths': dict(sorted(Counter(map(len, expected)).items())),
        'cnf_bytes': len(raw), 'cnf_sha256': sha256(raw).hexdigest(),
        'original_defects_blue_red': defects, 'free_attachment_pairs': len(free_pairs),
        'labeled_43_family_size': str(2**(32+len(free_pairs))),
        'same_C3_action_labeled_subfamily_size': str(2**(10+sum(orbit_sizes.values())))}
    require(json.loads((work/'summary.json').read_text()) == json.loads(json.dumps(expected_summary)), 'complete summary')
    return {'status': 'VERIFIED_EXACT_CORE_SWITCH_FORMULA', 'physical_five_sets': 237336,
        'base_graph_truth_cases': 32768, 'cnf_sha256': sha256(raw).hexdigest(),
        'clauses': len(expected), 'core_sha256': sha256(expected_core).hexdigest(),
        'original_defects_blue_red': defects,
        'free_attachment_orbit_sizes': dict(sorted(orbit_sizes.items()))}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = audit(a.work)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(result['status'], result['clauses'], 'clauses')
