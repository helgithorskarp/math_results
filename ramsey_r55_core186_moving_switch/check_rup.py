#!/usr/bin/env python3
"""Standalone physical, addition-only RUP check; no project imports.

This checker uses positive/negative bit masks and retains every clause.
It imports neither the DRAT kernel nor the generator nor their parsers.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT_SHA = 'f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def masks(line, variables=32):
    values = [int(x) for x in line.split()]
    need(values and values[-1] == 0, 'missing final zero')
    values = values[:-1]
    need(all(1 <= abs(x) <= variables for x in values), 'variable out of range')
    need(len({abs(x) for x in values}) == len(values), 'repetition or tautology')
    positive = sum(1 << (x-1) for x in values if x > 0)
    negative = sum(1 << (-x-1) for x in values if x < 0)
    return positive, negative


def rup(database, candidate):
    false, true = candidate
    while True:
        before = true | false
        for positive, negative in database:
            if (positive & true) or (negative & false):
                continue
            unassigned = (positive | negative) & ~(true | false)
            if not unassigned:
                return True
            if unassigned & (unassigned-1) == 0:
                if unassigned & positive:
                    true |= unassigned
                else:
                    false |= unassigned
        if (true | false) == before:
            return False


def physical(path):
    raw = (HERE/'parent.edges').read_bytes()
    need(sha256(raw).hexdigest() == PARENT_SHA, 'parent identity')
    lines = raw.decode().splitlines()
    need(lines and lines[0] == '43', 'parent order')
    graph = [[False]*43 for _ in range(43)]
    previous = (-1, -1)
    for line in lines[1:]:
        pair = tuple(int(x) for x in line.split())
        need(len(pair) == 2 and 0 <= pair[0] < pair[1] < 43 and pair > previous, 'parent pair')
        u, v = pair
        graph[u][v] = graph[v][u] = True
        previous = pair
    lines = Path(path).read_text().splitlines()
    need(lines, 'empty physical formula')
    header = lines[0].split()
    need(len(header) == 4 and header[:3] == ['p', 'cnf', '32'], 'physical header')
    need(int(header[3]) == len(lines)-1, 'physical clause count')
    database, colors, widths = [], Counter(), Counter()
    for line in lines[1:]:
        positive, negative = masks(line)
        vertices = [v for v in range(1, 33) if (positive | negative) & (1 << (v-1))]
        width = len(vertices)
        need(width in (4, 5), 'physical width')
        if width == 4:
            vertices = [0]+vertices
        spins = {v: int(bool(negative & (1 << (v-1)))) if v else 0 for v in vertices}
        edge_colors = [int(graph[u][v]) ^ spins[u] ^ spins[v] for u, v in combinations(vertices, 2)]
        need(edge_colors == [edge_colors[0]]*10, 'false physical event')
        database.append((positive, negative))
        colors[edge_colors[0]] += 1
        widths[width] += 1
    need(len(set(database)) == len(database), 'duplicate physical clause')
    return database, {'physical_clauses': len(database),
                      'colors_blue_red': [colors[0], colors[1]],
                      'widths': dict(sorted(widths.items()))}


def proof(database, path):
    rows = Path(path).read_text().splitlines()
    need(rows, 'empty proof')
    clauses = list(database)
    for index, line in enumerate(rows):
        candidate = masks(line)
        need(rup(clauses, candidate), 'RUP failure at addition '+str(index+1))
        need(candidate != (0, 0) or index == len(rows)-1, 'continuation after empty')
        clauses.append(candidate)
    need(clauses[-1] == (0, 0), 'missing final empty clause')
    return len(rows)


def controls():
    possible = [(sum(1 << i for i, s in enumerate(signs) if s == 1),
                 sum(1 << i for i, s in enumerate(signs) if s == -1))
                for signs in product((-1, 0, 1), repeat=2)]
    checked = accepted = 0
    for selection in range(1 << len(possible)):
        database = [c for j, c in enumerate(possible) if selection & (1 << j)]
        models = [bits for bits in range(4)
                  if all((p & bits) or (n & (3 ^ bits)) for p, n in database)]
        for candidate in possible:
            if rup(database, candidate):
                p, n = candidate
                need(all((p & bits) or (n & (3 ^ bits)) for bits in models), 'RUP soundness control')
                accepted += 1
            checked += 1
    rejected = 0
    for line in ('1 0 0', '33 0', '1 -1 0', '1 1 0', '1', 'd 1 0'):
        try:
            masks(line)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('bad clause accepted')
    return {'databases': 512, 'implication_checks': checked,
            'accepted_RUP': accepted, 'parser_rejections': rejected}


def audit(core, certificate):
    database, report = physical(core)
    report['RUP_additions'] = proof(database, certificate)
    report['controls'] = controls()
    report.update({'status': 'VERIFIED_MOVING33_ADDITION_ONLY_RUP_EXCLUSION',
        'physical_variables': 32, 'proof_deletions': 0, 'RAT_steps': 0,
        'parent_sha256': PARENT_SHA, 'obstruction_sha256': sha256(core.read_bytes()).hexdigest(),
        'rup_sha256': sha256(certificate.read_bytes()).hexdigest()})
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('core', type=Path)
    p.add_argument('certificate', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = audit(a.core, a.certificate)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))
