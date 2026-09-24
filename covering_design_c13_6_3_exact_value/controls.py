"""Positive residual completions from a known 21-block cover, and mutations."""
from itertools import combinations
import json
from pathlib import Path

import residual
import reference_star as audit_residual
import native_star

ROOT = Path(__file__).resolve().parent


def check(blocks, total, targets, bounds):
    if len(blocks) != total or len(set(blocks)) != total or any(b.bit_count() != 6 for b in blocks):
        raise ValueError('wrong block family')
    if [sum(b >> p & 1 for b in blocks) for p in range(13)] != targets:
        raise ValueError('wrong point degrees')
    if any(not any(b & t == t for b in blocks) for t in residual.TRIPLES):
        raise ValueError('uncovered triple')
    if any(sum(b & t == t for b in blocks) > bound for t, bound in bounds.items()):
        raise ValueError('pair bound exceeded')


def main():
    blocks = [sum(1 << (p - 1) for p in b) for b in json.loads((ROOT / 'UPPER21.json').read_text())['blocks']]
    targets = [sum(b >> p & 1 for b in blocks) for p in range(13)]
    bounds = {sum(1 << p for p in pair): sum(all(b >> p & 1 for p in pair) for b in blocks)
              for pair in combinations(range(13), 2)}
    check(blocks, 21, targets, bounds)
    p, r, h, q = 12, 8, 11, 1
    free = [b for b in blocks if not b & ((1 << p) | (1 << r))]
    if len(free) != 7:
        raise ValueError('unexpected fixture residual size')
    first = residual.Space(p, r)
    second = audit_residual.Space(p, r)
    third = native_star.Space(p, r)
    results = []
    for missing in range(1, 8):
        removed = set(free[:missing])
        fixed = [b for b in blocks if b not in removed]
        for name, space, solver in [('primary', first, residual.solve), ('python_star', second, audit_residual.solve), ('native_star', third, native_star.solve)]:
            answer = solver(space, fixed, h, q, total_blocks=21, target_degrees=targets, pair_bounds=bounds)
            if answer['status'] != 'SAT':
                raise ValueError('known feasible completion rejected')
            check(fixed + answer['witness'], 21, targets, bounds)
            results.append(dict(missing_blocks=missing, method=name, status='SAT',
                                witness=sorted(answer['witness'])))
    fixed = [b for b in blocks if b != free[0]]
    impossible = targets.copy()
    x = next(p for p in range(13) if free[0] >> p & 1)
    impossible[x] -= 1
    for space, solver in [(first, residual.solve), (second, audit_residual.solve), (third, native_star.solve)]:
        answer = solver(space, fixed, h, q, total_blocks=21, target_degrees=impossible, pair_bounds=bounds)
        if answer['status'] != 'UNSAT':
            raise ValueError('inconsistent degree sum accepted')
    print(json.dumps(dict(status='POSITIVE_COMPLETIONS_AND_MUTATIONS_PASSED',
                          positive_cases=21, inconsistent_degree_cases=3, results=results), indent=2))


if __name__ == '__main__':
    main()
