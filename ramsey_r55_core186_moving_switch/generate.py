#!/usr/bin/env python3
"""All K5 conditions for switches of the saved induced moving 33-core."""
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
    need(all(len(e) == 2 and 0 <= e[0] < e[1] < 43 for e in pairs), 'parent pairs')
    return list(range(33)), {(a, b) for a, b in pairs if b < 33}


def patterns(vertices, red):
    """Anchoring one spin forces the others for a monochromatic event."""
    first = vertices[0]
    for color in (0, 1):
        spins = {first: 0}
        for v in vertices[1:]:
            spins[v] = int((first, v) in red) ^ color
        if all((int((a, b) in red) ^ spins[a] ^ spins[b]) == color
               for a, b in combinations(vertices, 2)):
            for flip in (0, 1):
                yield color, {v: bit ^ flip for v, bit in spins.items()}


def full_formula(red, n=33):
    clauses, colors = set(), Counter()
    for q in combinations(range(n), 5):
        for color, spins in patterns(q, red):
            if spins.get(0, 0):
                continue
            row = tuple(-v if spins[v] else v for v in q if v)
            need(row not in clauses, 'duplicate physical event')
            clauses.add(row)
            colors[color] += 1
    return sorted(clauses), colors


def run(out):
    out.mkdir(parents=True, exist_ok=False)
    labels, red = parent_core()
    core = ('33\n'+''.join(f'{u} {v}\n' for u, v in sorted(red))).encode()
    (out/'core.edges').write_bytes(core)
    (out/'labels.json').write_text(json.dumps(labels)+'\n')
    clauses, colors = full_formula(red)
    raw = (f'p cnf 32 {len(clauses)}\n'+''.join(' '.join(map(str, row))+' 0\n' for row in clauses)).encode()
    (out/'switch.cnf').write_bytes(raw)
    defects = Counter()
    for q in combinations(range(33), 5):
        values = {e in red for e in combinations(q, 2)}
        if len(values) == 1:
            defects[int(values.pop())] += 1
    summary = {'vertices': 33, 'deleted_parent_vertices': list(range(33, 43)),
        'red_edges': len(red), 'parent_sha256': PARENT_SHA,
        'core_sha256': sha256(core).hexdigest(), 'switch_variables': 32,
        'normalization': 's_0=0', 'physical_five_sets': 237336,
        'cnf_clauses': len(clauses), 'clause_colors_blue_red': [colors[0], colors[1]],
        'clause_widths': dict(sorted(Counter(map(len, clauses)).items())),
        'cnf_bytes': len(raw), 'cnf_sha256': sha256(raw).hexdigest(),
        'original_defects_blue_red': [defects[0], defects[1]],
        'free_attachment_pairs': 375, 'labeled_43_family_size': str(2**407),
        'same_C3_action_labeled_subfamily_size': str(2**165)}
    (out/'summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True)+'\n')
    print(json.dumps(summary, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    run(parser.parse_args().out)
