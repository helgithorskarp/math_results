#!/usr/bin/env python3
"""Small exact positive and negative controls for the independent auditor."""
import json
import hashlib
import tempfile
from pathlib import Path
from itertools import combinations, product
import audit


def rejects(fn, fragment):
    try:
        fn()
    except ValueError as exc:
        audit.need(fragment in str(exc), 'wrong rejection: ' + str(exc))
        return 1
    raise ValueError('accepted corrupt control: ' + fragment)


def main():
    gates = [
        ('copy', [2], [(-5, 2), (5, -2)]),
        ('or', [2, 3], [(-2, 5), (-3, 5), (-5, 2, 3)]),
        ('and', [2, 3], [(-5, 2), (-5, 3), (5, -2, -3)]),
        ('or_and', [2, 3, 4], [(-2, 5), (-3, -4, 5), (-5, 2, 3), (-5, 2, 4)]),
    ]
    good_gates = bad_gates = 0
    # Independently exercise every sign convention, omitted clause, and flipped
    # literal on these tiny gates. Every old gate has an essential CNF clause.
    for kind, inputs, original in gates:
        for signs in product((-1, 1), repeat=len(inputs)):
            remap = {v: v*s for v, s in zip(inputs, signs)}
            clauses = [tuple((remap.get(abs(x), abs(x))) * (1 if x > 0 else -1)
                             for x in c) for c in original]
            signed_inputs = [remap[x] for x in inputs]
            audit.check_gate(clauses, 5, signed_inputs, kind)
            good_gates += 1
            for i in range(len(clauses)):
                bad_gates += rejects(lambda i=i: audit.check_gate(clauses[:i]+clauses[i+1:], 5,
                                                                  signed_inputs, kind), 'gate truth table')
                for j in range(len(clauses[i])):
                    corrupt = list(clauses)
                    corrupt[i] = tuple(-x if k == j else x for k, x in enumerate(clauses[i]))
                    bad_gates += rejects(lambda: audit.check_gate(corrupt, 5, signed_inputs, kind),
                                         'gate truth table')
    coordinates = [audit.state(v, i, j) for v in range(43) for i in range(1, 43)
                   for j in range(1, min(i, 25)+1)]
    audit.need(coordinates == list(range(7442, 39692)), 'state layout exact enumeration')
    all_guards = [audit.guard(c, d, s) for c in (0, 1) for d in range(19, 25)
                  for s in range(1, 43)]
    audit.need(all_guards == list(range(39692, 40196)), 'guard layout exact enumeration')
    # Colexicographic ranking is checked against sorted combination masks at a
    # smaller complete boundary, independently of the binomial expression.
    ranked = sorted(combinations(range(10), 5), key=lambda x: sum(1 << v for v in x))
    audit.need([audit.rank5(v) for v in ranked] == list(range(252)), 'colex boundary')
    mapping = audit.physical_layout()
    independent_pairs = {(u, v) for u in range(43) for v in range(u+1, 43)
                         if u // 4 != v // 4}
    audit.need(set(mapping) == independent_pairs, 'fixed block physical map')
    vertices = (0, 4, 8, 12, 16)
    positive = tuple(mapping[e] for e in combinations(vertices, 2))
    negative = tuple(-x for x in positive)
    coverage = audit.Coverage(mapping)
    coverage.consume(positive); coverage.consume(negative)
    physical_bad = rejects(lambda: coverage.consume(positive), 'duplicate five-clause')
    physical_bad += rejects(lambda: audit.Coverage(mapping).consume(positive[:-1]), 'five-clause missing pair')
    physical_bad += rejects(lambda: audit.Coverage(mapping).consume((-positive[0],)+positive[1:]), 'five-clause signs')
    physical_bad += rejects(lambda: audit.Coverage(mapping).consume((999,)), 'five-clause physical support')
    physical_bad += rejects(lambda: audit.Coverage(mapping).consume(positive+(positive[0],)), 'five-clause physical support')
    wrong_fixed = tuple(mapping[e] for e in combinations((0, 1, 4, 8, 12), 2) if e in mapping)
    physical_bad += rejects(lambda: audit.Coverage(mapping).consume(wrong_fixed), 'five-clause fixed conflict')
    physical_bad += rejects(lambda: audit.Coverage(mapping).finish(), 'incomplete five-set coverage')
    input_bad = 0
    for bad, message in [(b'2 -3\n', 'DIMACS line ending'), (b'2 0 -3 0\n', 'DIMACS literal range'),
                         (b'40352 0\n', 'DIMACS literal range'), (b'x 0\n', 'DIMACS integer')]:
        input_bad += rejects(lambda: audit.parse(bad), message)
    audit.need(audit.parse(b'2 -3 0\n') == (2, -3), 'valid DIMACS')
    for red, unit in ((18, 40195), (24, 39943)):
        suffix = audit.expected_suffix(red)
        audit.need(audit.suffix_bridge(suffix, red)['unit'] == unit, 'endpoint unit')
        wrong = [c for c in suffix if c != (unit,)]
        input_bad += rejects(lambda: audit.suffix_bridge(wrong, red), 'branch suffix')
    binding_bad = 0
    with tempfile.TemporaryDirectory(prefix='q10-audit-controls-') as tmp:
        path = Path(tmp) / 'tiny.cnf'
        raw = b'p cnf 40351 1\n1 0\n'
        path.write_bytes(raw)
        expected = {'clauses': 1, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        def tiny_check(row):
            reader = audit.Reader(path, row)
            audit.need(reader.take() == (1,), 'tiny constant')
            return reader.finish()
        tiny_check(expected)
        binding_bad += rejects(lambda: tiny_check(dict(expected, sha256='0'*64)), 'CNF hash')
        binding_bad += rejects(lambda: tiny_check(dict(expected, bytes=len(raw)+1)), 'CNF byte count')
        binding_bad += rejects(lambda: tiny_check(dict(expected, clauses=2)), 'DIMACS header')
    print(json.dumps({'status': 'PASSED_EXACT_AUDITOR_CONTROLS', 'positive_signed_gates': good_gates,
                      'rejected_gate_corruptions': bad_gates, 'rejected_physical_corruptions': physical_bad,
                      'rejected_dimacs_or_suffix_corruptions': input_bad,
                      'rejected_hash_size_header_corruptions': binding_bad,
                      'counter_states_checked': len(coordinates), 'guard_states_checked': len(all_guards),
                      'colex_boundary_combinations': len(ranked)}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
