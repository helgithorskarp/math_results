#!/usr/bin/env python3
"""Independent primary-orbit reconstruction and byte-exact full cube audit."""
from itertools import combinations


def need(ok, message):
    if not ok:
        raise ValueError(message)


def units(bits):
    need(len(bits) == 18 and set(bits) <= {'0', '1'}, 'core encoding')
    def sigma(v):
        return 3*(v//3)+(v+1) % 3 if v < 33 else v
    mapping, count = {}, 0
    for a, b in combinations(range(33), 2):
        if a//3 == b//3 or (a, b) in mapping:
            continue
        count += 1
        pair = (a, b)
        while pair not in mapping:
            mapping[pair] = count
            pair = tuple(sorted((sigma(pair[0]), sigma(pair[1]))))
    need(count == 165, 'moving cross orbits')
    for pair in combinations(range(33, 43), 2):
        count += 1
        mapping[pair] = count
    for fixed in range(33, 43):
        for i in range(11):
            count += 1
            for phase in range(3):
                mapping[3*i+phase, fixed] = count
    need(count == 320 and len(mapping) == 903-33, 'complete primary edge meanings')
    variables = [mapping[3*i, 3*j+d] for i, j in combinations(range(4), 2) for d in range(3)]
    need(len(set(variables)) == 18, 'distinct minority coordinates')
    return [v if b == '1' else -v for v, b in zip(variables, bits)]


def check(parent, formula, bits):
    with parent.open('rb') as source, formula.open('rb') as target:
        need(source.readline() == b'p cnf 34280 615920\n', 'parent header')
        need(target.readline() == b'p cnf 34280 615938\n', 'cube header')
        while data := source.read(1 << 20):
            need(target.read(len(data)) == data, 'complete parent prefix')
        expected = units(bits)
        for literal in expected:
            need(target.readline() == f'{literal} 0\n'.encode(), 'primary unit assignment')
        need(target.read() == b'', 'cube extra bytes')
    return dict(variables=34280, clauses=615938, appended_units=18, entire_parent=True, primary_variables=320)
