#!/usr/bin/env python3
"""Audit sufficient literal CNF clauses, without importing any old encoder.

Coverage is reconstructed from clause supports; small gates are checked by
truth tables rather than comparison with the encoder's clause templates.
"""
import argparse
import hashlib
import json
from itertools import combinations, product
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parent
N = 43
BASE_CLAUSES = 1931140
RAMSEY_START = 3241                 # zero-based clause positions, no header
RAMSEY_END = 1378507
COUNTER_START = 1404955
COUNTER_END = 1531160
GUARD_END = 1532672
VARIABLES = 40351


def need(ok, message):
    if not ok:
        raise ValueError(message)


def fixed(u, v):
    if u < 40 and v < 40 and u // 4 == v // 4:
        return 1
    if u >= 40 and v >= 40:
        return 0
    return None


def physical_layout():
    pairs = [e for e in combinations(range(N), 2) if fixed(*e) is None]
    need(len(pairs) == 840, 'physical variable dimension')
    return {e: i + 2 for i, e in enumerate(pairs)}


def physical_literal(mapping, u, v):
    u, v = sorted((u, v))
    c = fixed(u, v)
    return (1 if c else -1) if c is not None else mapping[u, v]


def state(v, i, j):
    need(0 <= v < 43 and 1 <= i <= 42 and 1 <= j <= min(i, 25),
         'counter coordinate')
    prefix = i * (i - 1) // 2 if i <= 26 else 325 + 25 * (i - 26)
    return 7442 + 750 * v + prefix + j - 1


def guard(color, degree, step=42):
    need(color in (0, 1) and 19 <= degree <= 24 and 1 <= step <= 42,
         'guard coordinate')
    return 39692 + 252 * color + 42 * (degree - 19) + step - 1


def rank5(vertices):
    return sum(comb(v, i + 1) for i, v in enumerate(vertices))


def check_gate(clauses, output, inputs, kind):
    """Prove exact Boolean equivalence for one gate by complete enumeration.

    Input values are SIGNED-literal values. Treat the constant variable 1
    as free here: the equivalence must also hold after the unit 1 fixes it.
    """
    variables = [abs(x) for x in inputs] + [output]
    need(len(set(variables)) == len(variables), 'gate variable collision')
    need(all(c and all(abs(x) in variables for x in c) for c in clauses),
         'gate support')
    for bits in product((False, True), repeat=len(variables)):
        values = dict(zip(variables, bits))
        args = [values[abs(x)] == (x > 0) for x in inputs]
        if kind == 'copy':
            expected = args[0]
        elif kind == 'or':
            expected = args[0] or args[1]
        elif kind == 'and':
            expected = args[0] and args[1]
        elif kind == 'or_and':
            expected = args[0] or (args[1] and args[2])
        else:
            raise ValueError('unknown gate')
        satisfied = all(any(values[abs(x)] == (x > 0) for x in c) for c in clauses)
        need(satisfied == (bits[-1] == expected), 'gate truth table')


class Coverage:
    def __init__(self, mapping):
        self.mapping = mapping
        self.inverse = {var: edge for edge, var in mapping.items()}
        self.seen = [bytearray(comb(N, 5)), bytearray(comb(N, 5))]
        self.counts = [0, 0]          # forbidden blue, forbidden red

    def consume(self, clause):
        need(clause and all(x > 0 for x in clause) or
             clause and all(x < 0 for x in clause), 'five-clause signs')
        color = int(clause[0] < 0)
        variables = {abs(x) for x in clause}
        need(len(variables) == len(clause) and variables <= self.inverse.keys(),
             'five-clause physical support')
        vertices = tuple(sorted({v for x in variables for v in self.inverse[x]}))
        need(len(vertices) == 5, 'five-clause vertex support')
        expected = set()
        for edge in combinations(vertices, 2):
            c = fixed(*edge)
            if c is None:
                expected.add(self.mapping[edge])
            else:
                need(c == color, 'five-clause fixed conflict')
        need(variables == expected, 'five-clause missing pair')
        rank = rank5(vertices)
        need(not self.seen[color][rank], 'duplicate five-clause')
        self.seen[color][rank] = 1
        self.counts[color] += 1

    def finish(self):
        needed = [0, 0]
        for vertices in combinations(range(N), 5):
            fixed_colors = {fixed(*edge) for edge in combinations(vertices, 2)} - {None}
            rank = rank5(vertices)
            for color in (0, 1):
                required = 1 - color not in fixed_colors
                need(bool(self.seen[color][rank]) == required, 'incomplete five-set coverage')
                needed[color] += int(required)
        need(needed == self.counts, 'five-clause count')
        return {'physical_five_sets': comb(N, 5), 'blue_forbidding_clauses': needed[0],
                'red_forbidding_clauses': needed[1],
                'clauses': sum(needed), 'coverage': 'EVERY_REQUIRED_PHYSICAL_FIVE_SET'}


def parse(line):
    need(line.endswith(b' 0\n'), 'DIMACS line ending')
    words = line.split()
    try:
        literals = tuple(map(int, words))
    except ValueError as exc:
        raise ValueError('DIMACS integer') from exc
    need(literals[-1] == 0 and all(0 < abs(x) <= VARIABLES for x in literals[:-1]),
         'DIMACS literal range')
    return literals[:-1]


class Reader:
    def __init__(self, path, expected):
        self.stream = path.open('rb')
        header = self.stream.readline()
        need(header == f'p cnf {VARIABLES} {expected["clauses"]}\n'.encode(), 'DIMACS header')
        self.full_hash = hashlib.sha256(header)
        self.base_hash = hashlib.sha256()
        self.size = len(header)
        self.position = 0
        self.expected = expected

    def take(self):
        line = self.stream.readline()
        need(line, 'truncated CNF')
        self.full_hash.update(line)
        self.size += len(line)
        if self.position < BASE_CLAUSES:
            self.base_hash.update(line)
        self.position += 1
        return parse(line)

    def skip_to(self, position):
        need(self.position <= position, 'section order')
        while self.position < position:
            self.take()

    def finish(self):
        need(not self.stream.read(1), 'extra CNF content')
        self.stream.close()
        need(self.position == self.expected['clauses'], 'DIMACS clause count')
        need(self.size == self.expected['bytes'], 'CNF byte count')
        need(self.full_hash.hexdigest() == self.expected['sha256'], 'CNF hash')
        return self.base_hash.hexdigest()


def degree_subset(reader, mapping):
    need(reader.position == COUNTER_START, 'counter start')
    gates = 0
    for v in range(N):
        inputs = [physical_literal(mapping, v, w) for w in range(N) if w != v]
        for i in range(1, 43):
            for j in range(1, min(i, 25) + 1):
                if i == 1:
                    args, kind, count = [inputs[0]], 'copy', 2
                elif j == 1:
                    args, kind, count = [state(v, i-1, 1), inputs[i-1]], 'or', 3
                elif j == i:
                    args, kind, count = [state(v, i-1, j-1), inputs[i-1]], 'and', 3
                else:
                    args = [state(v, i-1, j), state(v, i-1, j-1), inputs[i-1]]
                    kind, count = 'or_and', 4
                check_gate([reader.take() for _ in range(count)], state(v, i, j), args, kind)
                gates += 1
        need(reader.take() == (state(v, 42, 18),), 'degree lower window')
        need(reader.take() == (-state(v, 42, 25),), 'degree upper window')
    need(reader.position == COUNTER_END, 'counter end')
    guard_gates = 0
    for color in (0, 1):
        for degree in range(19, 25):
            literals = [(state(v, 42, degree) if color == 0 else
                         -state(v, 42, 43-degree)) for v in range(N)]
            previous = literals[0]
            for step in range(1, 43):
                out = guard(color, degree, step)
                check_gate([reader.take() for _ in range(3)], out,
                           [previous, literals[step]], 'and')
                previous = out
                guard_gates += 1
    need(reader.position == GUARD_END, 'guard end')
    return {'exact_threshold_gates': gates, 'counter_definition_clauses': 126119,
            'degree_window_units': 86, 'guard_and_gates': guard_gates,
            'guard_definition_clauses': 1512, 'method': 'EXHAUSTIVE_GATE_TRUTH_TABLES'}


def expected_suffix(red):
    """Pin all original branch clauses; only positive endpoint guards are needed."""
    units, witnesses = [], []
    for color, d in ((0, red), (1, 42-red)):
        if d == 18:
            units.append((-guard(color, 19),))
        else:
            units.append((guard(color, d),))
            if d < 24:
                units.append((-guard(color, d+1),))
        if d < 24:
            witnesses.append(tuple(-state(v, 42, d+1) if color == 0 else
                                   state(v, 42, 42-d) for v in range(N)))
    return units + witnesses


def suffix_bridge(suffix, red):
    need(suffix == expected_suffix(red), 'branch suffix')
    if red == 18:
        need((40195,) in suffix, 'blue degree24 guard unit')
        return {'unit': 40195, 'forces_each_vertex': ['red_degree>=18', 'red_degree<19'],
                'red_regular_degree': 18}
    if red == 24:
        need((39943,) in suffix, 'red degree24 guard unit')
        return {'unit': 39943, 'forces_each_vertex': ['red_degree>=24', 'red_degree<25'],
                'red_regular_degree': 24}
    return None


def shared_file(path, expected, base_hash):
    """Hash-bind the already audited full base bytes; parse the short suffix."""
    full, body = hashlib.sha256(), hashlib.sha256()
    with path.open('rb') as stream:
        header = stream.readline()
        need(header == f'p cnf {VARIABLES} {expected["clauses"]}\n'.encode(), 'shared header')
        full.update(header)
        size = len(header)
        for _ in range(BASE_CLAUSES):
            line = stream.readline()
            need(line, 'shared body truncated')
            full.update(line); body.update(line); size += len(line)
        suffix = []
        for line in stream:
            full.update(line); size += len(line); suffix.append(parse(line))
    need(len(suffix) + BASE_CLAUSES == expected['clauses'], 'shared clause count')
    need(body.hexdigest() == base_hash, 'shared audited body hash')
    need(full.hexdigest() == expected['sha256'] and size == expected['bytes'], 'shared file hash/size')
    return suffix


def audit(directory):
    directory = Path(directory)
    data = json.loads((ROOT / 'INPUTS.json').read_text())
    rows = data['rows']
    need([r['red_degree'] for r in rows] == [18, 20, 22, 24], 'complete four-job inventory')
    mapping = physical_layout()
    reader = Reader(directory / rows[0]['filename'], rows[0])
    need(reader.take() == (1,), 'true constant unit')
    reader.skip_to(RAMSEY_START)
    coverage = Coverage(mapping)
    while reader.position < RAMSEY_END:
        coverage.consume(reader.take())
    five = coverage.finish()
    need(five['clauses'] == RAMSEY_END - RAMSEY_START, 'Ramsey section count')
    reader.skip_to(COUNTER_START)
    degree = degree_subset(reader, mapping)
    reader.skip_to(BASE_CLAUSES)
    suffix = [reader.take() for _ in range(rows[0]['clauses']-BASE_CLAUSES)]
    base_hash = reader.finish()
    suffixes = [suffix] + [shared_file(directory / r['filename'], r, base_hash) for r in rows[1:]]
    bridges = []
    for row, suff in zip(rows, suffixes):
        bridge = suffix_bridge(suff, row['red_degree'])
        bridges.append({'branch': row['branch'], 'sha256': row['sha256'],
                        'good43_forced_by_common_base': True, 'regular_endpoint_bridge': bridge})
    return {'status': 'CHECKED_FOUR_FROZEN_FILES_AND_TWO_REGULAR_ENDPOINT_BRIDGES',
            'task': data['task'], 'audited_base_body_sha256': base_hash,
            'physical_variables': 840, 'fixed_red_pairs': 60, 'fixed_blue_pairs': 3,
            'ramsey': five, 'degree': degree, 'files': bridges,
            'extra_clauses_semantics_used': False, 'solver_calls': 0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branches', required=True)
    args = parser.parse_args()
    print(json.dumps(audit(args.branches), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
