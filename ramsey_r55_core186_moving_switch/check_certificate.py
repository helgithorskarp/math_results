#!/usr/bin/env python3
"""Direct physical check for arbitrary switches of the pinned induced core.

No generator, full-formula auditor, solver or proof trimmer is imported.
The small RUP/RAT kernel is explicitly vendored from the teammate's
Paley-family package; this is reuse, not a new independent DRAT algorithm.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from drat import clause, require, verify_proof

HERE = Path(__file__).resolve().parent
PARENT_SHA = 'f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441'


def input_rows():
    data = (HERE/'parent.edges').read_bytes()
    require(sha256(data).hexdigest() == PARENT_SHA, 'parent identity')
    lines = data.decode().splitlines()
    require(lines and lines[0] == '43', 'parent order')
    edges = [tuple(map(int, s.split())) for s in lines[1:]]
    require(all(len(e) == 2 and 0 <= e[0] < e[1] < 43 for e in edges), 'parent pairs')
    require(edges == sorted(set(edges)), 'canonical parent pairs')
    original_rows = [0]*43
    for u, v in edges:
        original_rows[u] |= 1 << v
        original_rows[v] |= 1 << u
    labels = list(range(33))
    rows = [sum(1 << j for j, w in enumerate(labels) if original_rows[v] & (1 << w)) for v in labels]
    return rows, labels


def physical_core(path):
    rows, _ = input_rows()
    lines = Path(path).read_text().splitlines()
    require(lines, 'empty physical formula')
    header = lines[0].split()
    require(len(header) == 4 and header[:2] == ['p', 'cnf'], 'CNF header')
    require(int(header[2]) == 32 and int(header[3]) == len(lines)-1, 'CNF dimensions')
    database = set()
    colors, widths = Counter(), Counter()
    for line in lines[1:]:
        literals = clause(line)
        require(len(literals) in (4, 5), 'physical width')
        require(all(1 <= abs(x) <= 32 for x in literals), 'physical switch variable')
        spins = {abs(x): int(x < 0) for x in literals}
        if len(literals) == 4:
            spins[0] = 0
        require(len(spins) == 5, 'five physical vertices')
        values = {int(bool(rows[u] & (1 << v))) ^ spins[u] ^ spins[v]
                  for u, v in combinations(sorted(spins), 2)}
        require(len(values) == 1, 'false physical K5 clause')
        frozen = frozenset(literals)
        require(frozen not in database, 'duplicate physical clause')
        database.add(frozen)
        colors[values.pop()] += 1
        widths[len(literals)] += 1
    return database, {'physical_clauses': len(database), 'physical_colors_blue_red': [colors[0], colors[1]],
                       'physical_widths': dict(sorted(widths.items())),
                       'physical_variables': sorted({abs(x) for row in database for x in row})}


def audit(core, proof):
    database, report = physical_core(core)
    report['proof'] = verify_proof(database, proof)
    report.update({'status': 'VERIFIED_CORE186_MOVING_SWITCH_EXCLUSION',
                   'parent_sha256': PARENT_SHA, 'obstruction_sha256': sha256(core.read_bytes()).hexdigest(),
                   'proof_sha256': sha256(proof.read_bytes()).hexdigest()})
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('core', type=Path)
    p.add_argument('proof', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    report = audit(a.core, a.proof)
    a.output.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(report['status'], report['physical_clauses'], 'physical clauses;', report['proof'])
